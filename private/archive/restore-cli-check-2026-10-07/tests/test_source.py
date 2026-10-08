"""Stage 0: inventory, `wgc source init|scan|extract|verify`, default precedence, fixture sync (ADR-0020)."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from wgc import contracts, source
from wgc.__main__ import main
from wgc.canonical import projection, sha256_hex
from wgc.validate import load_documents, validate

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench" / "minigame"
FIXTURES = ROOT / "contracts" / "fixtures" / "valid"

# Self-authored test text (not a game): two sections, a table, a list.
RULES = """\
# Test Rules

## 1.0 Units

**1.1** A unit has a Strength.

**1.2** A unit may move
up to its Movement Allowance.

## 2.0 Combat

**2.1** Roll one die:

| Roll | Result |
|---|---|
| 1–3 | Miss |
| 4–6 | Hit |
"""


def records(path: Path) -> list[dict]:
    return [r for d in load_documents(path) for r in d.get("records") or []]


def make_game(tmp_path: Path, text: str = RULES) -> Path:
    root = tmp_path / "game"
    (root / "private").mkdir(parents=True)
    (root / "private" / "rules.md").write_text(text, encoding="utf-8", newline="\n")
    source.init(root, "tst", [("rules", "private/rules.md")])
    source.extract(root)
    return root


def segments(root: Path) -> dict[str, dict]:
    return {s["id"]: s for s in source.read_inventory(root).segments}


def codes(report, severity="error") -> set[str]:
    return report.codes(severity)


# --- benchmark inventory and fixtures --------------------------------------------------------------------------

def test_committed_benchmark_inventory_is_fresh(tmp_path):
    root = tmp_path / "minigame"
    (root / "source").mkdir(parents=True)
    shutil.copy(BENCH / "rulebook.md", root / "rulebook.md")
    shutil.copy(BENCH / "source" / "inventory.yaml", root / "source" / "inventory.yaml")
    source.extract(root)
    assert (root / "source" / "inventory.yaml").read_bytes() == (BENCH / "source" / "inventory.yaml").read_bytes(), \
        "bench/minigame/source/inventory.yaml is stale: run `python -m wgc source extract --root bench/minigame`"
    assert not source.verify(root).diagnostics


def test_benchmark_inventory_validates_without_text():
    inv = BENCH / "source" / "inventory.yaml"
    assert validate([inv]).diagnostics == []
    body = inv.read_text(encoding="utf-8")
    assert "may not enter a hex adjacent" not in body  # ADR-0012: no segment text in the inventory


def test_fixture_segments_match_benchmark_inventory():
    inv = {r["id"]: r for r in records(BENCH / "source" / "inventory.yaml")}
    fixture = records(FIXTURES / "source.minigame.yaml")
    segs = [r for r in fixture if r["kind"] == "segment"]
    assert segs
    for r in segs:
        assert r["id"] in inv, r["id"]
        assert projection(r, "logic") == projection(inv[r["id"]], "logic"), r["id"]
        assert r["order"] == inv[r["id"]]["order"], r["id"]
    rules = next(r for r in fixture if r["id"] == "SRC-dsk.rules")
    assert rules["file_hash"] == sha256_hex((BENCH / "rulebook.md").read_bytes()) == inv["SRC-dsk.rules"]["file_hash"]
    assert rules["extractor"] == inv["SRC-dsk.rules"]["extractor"]


def test_fixture_anchors_carry_real_segment_hashes():
    inv = {r["id"]: r for r in records(BENCH / "source" / "inventory.yaml")}
    anchors = []

    def walk(o):
        if isinstance(o, dict):
            if "seg" in o and "seg_hash" in o:
                anchors.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(records(FIXTURES / "logic.minigame.yaml"))
    assert len(anchors) >= 30
    for a in anchors:
        assert a["seg_hash"] == inv[a["seg"]]["text_hash"], a["seg"]


# --- init / scan / extract -------------------------------------------------------------------------------------

def test_init_scan_extract(tmp_path):
    root = make_game(tmp_path)
    inv = source.read_inventory(root)
    (doc,) = inv.documents
    assert doc["id"] == "SRC-tst.rules" and doc["seg_prefix"] == "tst" and doc["present"] is True
    assert doc["path"] == "private/rules.md" and doc["extractor"] == "wgc.ingest.markdown@1"
    assert doc["file_hash"] == sha256_hex((root / "private" / "rules.md").read_bytes())
    segs = segments(root)
    assert list(segs) == ["SEG-tst.u1", "SEG-tst.1.0", "SEG-tst.1.1", "SEG-tst.1.2", "SEG-tst.2.0", "SEG-tst.2.1"]
    assert segs["SEG-tst.2.1"]["segment_type"] == "table" and segs["SEG-tst.2.1"]["parent"] == "SEG-tst.2.0"
    assert segs["SEG-tst.1.1"]["label"] == "1.1"
    cache = root / ".glu" / "source" / "SRC-tst.rules"
    assert (cache / "SEG-tst.1.1.txt").read_text(encoding="utf-8") == "A unit has a Strength."
    assert len(list(cache.glob("*.txt"))) == len(segs)
    assert validate([source.inventory_path(root)]).diagnostics == []


def test_extract_is_deterministic(tmp_path):
    a = make_game(tmp_path / "a")
    b = make_game(tmp_path / "b")
    assert source.inventory_path(a).read_bytes() == source.inventory_path(b).read_bytes()
    before = source.inventory_path(a).read_bytes()
    source.extract(a)
    assert source.inventory_path(a).read_bytes() == before
    ca, cb = a / ".glu" / "source" / "SRC-tst.rules", b / ".glu" / "source" / "SRC-tst.rules"
    assert {p.name: p.read_bytes() for p in ca.iterdir()} == {p.name: p.read_bytes() for p in cb.iterdir()}


def test_label_stays_a_string_after_round_trip(tmp_path):
    root = make_game(tmp_path)
    raw = yaml.safe_load(source.inventory_path(root).read_text(encoding="utf-8"))
    labels = [r["label"] for r in raw["records"] if r.get("label")]
    assert labels and all(isinstance(x, str) for x in labels)


def test_extract_keeps_hand_set_fields(tmp_path):
    root = make_game(tmp_path)
    inv = source.read_inventory(root)
    inv.documents[0].update(title="Test Rules", notes="hand note", precedence=45)
    for s in inv.segments:
        if s["id"] in ("SEG-tst.1.1", "SEG-tst.1.2"):
            s["verified_by_render"] = True
            s["corrections"] = [{"what": "joined a split word", "by": "owner"}]
    inv.documents.append({"kind": "source_document", "id": "SRC-tst.faq", "role": "faq", "present": False})
    source.write_inventory(root, inv)
    (root / "private" / "rules.md").write_text(RULES.replace("has a Strength", "has a Strength and a Morale"),
                                               encoding="utf-8", newline="\n")
    messages = source.extract(root)
    assert any("zmienione 1" in m for m in messages)
    inv = source.read_inventory(root)
    assert inv.documents[0]["title"] == "Test Rules" and inv.documents[0]["notes"] == "hand note"
    assert inv.documents[0]["precedence"] == 45
    assert inv.document("SRC-tst.faq") == {"kind": "source_document", "id": "SRC-tst.faq", "role": "faq",
                                          "present": False}
    segs = segments(root)
    assert "verified_by_render" not in segs["SEG-tst.1.1"]  # text changed: the render no longer confirms it
    assert segs["SEG-tst.1.1"]["corrections"] == [{"what": "joined a split word", "by": "owner"}]
    assert segs["SEG-tst.1.2"]["verified_by_render"] is True  # unchanged text keeps the confirmation


def test_extract_drops_removed_segments_and_their_cache(tmp_path):
    root = make_game(tmp_path)
    (root / "private" / "rules.md").write_text(RULES.split("## 2.0")[0], encoding="utf-8", newline="\n")
    assert any("usunięte 2" in m for m in source.extract(root))
    assert "SEG-tst.2.1" not in segments(root)
    assert not (root / ".glu" / "source" / "SRC-tst.rules" / "SEG-tst.2.1.txt").exists()


def test_scan_marks_missing_file(tmp_path):
    root = make_game(tmp_path)
    (root / "private" / "rules.md").unlink()
    assert any("brak pliku" in m for m in source.scan(root))
    assert source.read_inventory(root).documents[0]["present"] is False


def test_init_errors(tmp_path):
    root = make_game(tmp_path)
    with pytest.raises(source.SourceError, match="już istnieje"):
        source.init(root, "tst", [])
    other = tmp_path / "other"
    other.mkdir()
    with pytest.raises(source.SourceError, match="Nieznana rola"):
        source.init(other, "tst", [("rulez", "x.md")])
    with pytest.raises(source.SourceError, match="poza katalogiem"):
        source.init(other, "tst", [("rules", "../game/private/rules.md")])
    with pytest.raises(source.SourceError, match="Brak inwentarza"):
        source.scan(other)


def test_init_ids_and_prefixes(tmp_path):
    root = tmp_path / "g"
    root.mkdir()
    source.init(root, "g1", [("rules", "a.md"), ("rules", "b.md"), ("errata", "c.md")])
    docs = source.read_inventory(root).documents
    assert [d["id"] for d in docs] == ["SRC-g1.rules", "SRC-g1.rules.2", "SRC-g1.errata"]
    assert [source.seg_prefix(d) for d in docs] == ["g1", "g1.rules.2", "g1.errata"]
    assert all(d["present"] is False for d in docs)


# --- verify ------------------------------------------------------------------------------------------------------

def test_verify_ok(tmp_path):
    report = source.verify(make_game(tmp_path))
    assert report.ok and not report.diagnostics


def test_verify_detects_changed_file(tmp_path):
    root = make_game(tmp_path)
    (root / "private" / "rules.md").write_text(RULES.replace("Strength", "Morale"), encoding="utf-8", newline="\n")
    report = source.verify(root)
    assert codes(report) == {"file_hash_mismatch", "segment_hash_mismatch"}
    assert [d.subject for d in report.diagnostics if d.code == "segment_hash_mismatch"] == ["SEG-tst.1.1"]


def test_verify_rewrapping_keeps_text_hash_and_reports_structure_and_new_or_removed_rules(tmp_path):
    root = make_game(tmp_path)
    rules = root / "private" / "rules.md"
    rules.write_text(RULES.replace("may move\nup to", "may move up\nto"), encoding="utf-8", newline="\n")
    report = source.verify(root)
    # same words, other lines: text_hash still matches (no segment_hash_mismatch), struct_hash does not (ADR-0032)
    assert codes(report) == {"file_hash_mismatch", "segment_struct_mismatch"}
    assert [d.subject for d in report.diagnostics if d.code == "segment_struct_mismatch"] == ["SEG-tst.1.2"]
    rules.write_text(RULES + "\n**2.2** Hits remove a unit.\n", encoding="utf-8", newline="\n")
    assert "segment_unlisted" in codes(source.verify(root))
    rules.write_text(RULES.split("**1.2**")[0] + "## 2.0" + RULES.split("## 2.0")[1], encoding="utf-8", newline="\n")
    report = source.verify(root)
    assert "segment_missing" in codes(report)
    assert [d.subject for d in report.diagnostics if d.code == "segment_missing"] == ["SEG-tst.1.2"]


def test_verify_cache(tmp_path):
    root = make_game(tmp_path)
    cache = root / ".glu" / "source" / "SRC-tst.rules"
    (cache / "SEG-tst.1.1.txt").write_text("A unit has no Strength.", encoding="utf-8")
    assert codes(source.verify(root)) == {"cache_mismatch"}
    shutil.rmtree(cache)
    report = source.verify(root)
    assert report.ok and codes(report, "warning") == {"cache_missing"}
    source.extract(root)  # restores the cache deterministically
    assert not source.verify(root).diagnostics


def test_verify_missing_source_and_inventory_errors(tmp_path):
    root = make_game(tmp_path)
    (root / "private" / "rules.md").unlink()
    assert codes(source.verify(root)) == {"source_missing"}
    inv = source.inventory_path(root)
    inv.write_text(inv.read_text(encoding="utf-8").replace("parent: SEG-tst.1.0", "parent: SEG-tst.9.0"),
                   encoding="utf-8", newline="\n")
    assert "unresolved_ref" in codes(validate([inv]))  # segment.parent is a checked reference


def test_verify_extractor_changed_warning(tmp_path):
    root = make_game(tmp_path)
    inv = source.read_inventory(root)
    inv.documents[0]["extractor"] = "wgc.ingest.markdown@old"
    source.write_inventory(root, inv)
    report = source.verify(root)
    assert report.ok and codes(report, "warning") == {"extractor_changed"}


# --- contract: roles and default precedence ----------------------------------------------------------------------

def test_new_roles_in_contract():
    assert {"living_rules", "community_interpretation"} <= set(source.roles())
    for role in ("living_rules", "community_interpretation"):
        doc = {"schema": "wgc/source@0", "records": [
            {"kind": "source_document", "id": f"SRC-x.{role}", "role": role, "present": False, "seg_prefix": "x.l"}]}
        assert contracts.errors(doc) == []
    bad = {"schema": "wgc/source@0", "records": [
        {"kind": "source_document", "id": "SRC-x.r", "role": "rules", "present": False, "seg_prefix": ".bad"}]}
    assert contracts.errors(bad)


def test_default_precedence_chain():
    chain = ["errata", "living_rules", "rules", "faq", "designer_clarification", "community_interpretation"]
    values = [source.DEFAULT_PRECEDENCE[r] for r in chain]
    assert values == sorted(values, reverse=True) and len(set(values)) == len(values)
    assert set(source.DEFAULT_PRECEDENCE) <= set(source.roles())
    for printed in ("scenario_book", "charts", "cards", "counters", "map", "module"):
        assert source.DEFAULT_PRECEDENCE[printed] == source.DEFAULT_PRECEDENCE["rules"]
    for none in ("prior_translation", "other"):
        assert source.effective_precedence({"role": none}) is None


def test_explicit_precedence_overrides_default():
    assert source.effective_precedence({"role": "faq"}) == source.DEFAULT_PRECEDENCE["faq"]
    assert source.effective_precedence({"role": "faq", "precedence": 70}) == 70
    assert source.effective_precedence({"role": "other", "precedence": 5}) == 5


# --- CLI ---------------------------------------------------------------------------------------------------------

def test_cli_source_commands(tmp_path, capsys):
    root = tmp_path / "g"
    (root / "src").mkdir(parents=True)
    (root / "src" / "rules.md").write_text(RULES, encoding="utf-8", newline="\n")
    r = str(root)
    assert main(["source", "init", "--root", r, "--game", "tst", "--doc", "rules:src/rules.md"]) == 0
    assert main(["source", "scan", "--root", r]) == 0
    assert main(["source", "extract", "--root", r]) == 0
    assert "segmenty 6" in capsys.readouterr().out
    assert main(["source", "verify", "--root", r]) == 0
    assert "OK:" in capsys.readouterr().out
    (root / "src" / "rules.md").write_text(RULES.replace("Strength", "Morale"), encoding="utf-8", newline="\n")
    assert main(["source", "verify", "--root", r, "--json"]) == 1
    assert '"file_hash_mismatch"' in capsys.readouterr().out
    assert main(["source", "init", "--root", r, "--game", "tst"]) == 2
    assert "już istnieje" in capsys.readouterr().err


def test_cli_doc_argument_requires_role_and_path(tmp_path):
    with pytest.raises(SystemExit):
        main(["source", "init", "--root", str(tmp_path), "--game", "tst", "--doc", "rules.md"])
