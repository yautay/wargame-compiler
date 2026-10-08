"""M9a: `wgc.kb.accept()`: provenance given by WGC, validation before writing, idempotence and conflicts (ADR-0025)."""
from __future__ import annotations

import copy
from pathlib import Path

import yaml

from test_tables import game  # noqa: F401  (fixture)
from wgc import kb, manifest as manifests, tasks
from wgc.canonical import PROJECTION_VERSION, content_hash, projection
from wgc.kb import Workspace
from wgc.validate import load_documents, validate, validate_documents

ROOT = Path(__file__).resolve().parent.parent
SEG = "SEG-dsk.4.3"
INPUTS = (SEG,)
BY = {"tier": "deterministic", "tool": "wgc.tables.parse@0"}
SPEC = tasks.get("wgc.tables.parse")


def proposals(root: Path) -> list[dict]:
    return SPEC.deterministic_impl(Workspace(root), INPUTS)


def accept(root: Path, props: list[dict], job: str = "job_000001", by: dict = BY) -> kb.AcceptResult:
    return kb.accept(root, SPEC, INPUTS, props, by=by, job=job)


def tables_file(root: Path) -> Path:
    return root / "kb" / "logic" / "tables.yaml"


def test_accept_writes_record_with_provenance(game):
    res = accept(game, proposals(game))
    assert res.ok and res.created == ["TAB-4.3"] and "kb/logic/tables.yaml" in res.files
    [doc] = load_documents(tables_file(game))
    [rec] = doc["records"]
    ws = Workspace(game)
    seg = ws.segment(SEG)
    planned = manifests.build(ws, SPEC, INPUTS)
    assert rec["status"] == "accepted"
    assert rec["prov"] == {"kind": "explicit_source", "anchors": [{"seg": SEG, "seg_hash": seg["text_hash"]}],
                           "by": BY, "job": "job_000001",
                           "inputs_hash": content_hash({"projection": PROJECTION_VERSION,
                                                        "records": [projection(seg, "logic")]}),
                           "manifest": planned.body, "owner": {"task": SPEC.id, "scope": [SEG]}}
    # one definition of what the job read: the planner's manifest (ADR-0033)
    assert planned.body == {"format": "wgc/manifest@0", "task": "wgc.tables.parse@0", "projection": PROJECTION_VERSION,
                            "inputs": [{"id": SEG, "hash": content_hash(projection(seg, "logic"))}],
                            "authority": [{"id": "SRC-dsk.rules",
                                           "hash": content_hash(projection(ws.document("SRC-dsk.rules"), "logic"))}]}
    assert list(rec)[:3] == ["kind", "id", "title"]  # contract order
    assert validate([game / "source", game / "kb"]).ok


def test_file_is_deterministic_and_lf(game):
    accept(game, proposals(game))
    data = tables_file(game).read_bytes()
    assert b"\r\n" not in data and data.startswith(b"# wgc/logic@0")
    assert kb.dump(load_documents(tables_file(game))) == data.decode("utf-8")


def test_dump_style():
    short = {"kind": "concept", "id": "CON-d6", "category": "die", "name": "die"}
    long = {"kind": "table", "id": "TAB-1", "title": "T" * 100, "rows": [[1, "a"]]}
    assert kb.dump([{"schema": "wgc/logic@0", "records": [short, long]}]).splitlines()[1:] == [
        "schema: wgc/logic@0", "records:",
        "  - {kind: concept, id: CON-d6, category: die, name: die}",
        "  - kind: table", "    id: TAB-1", f"    title: {'T' * 100}", "    rows: [[1, a]]"]
    assert yaml.safe_load(kb.dump([{"schema": "wgc/logic@0", "records": [short, long]}]))["records"] == [short, long]


def test_reaccept_is_idempotent(game):
    accept(game, proposals(game), job="job_000001")
    before = tables_file(game).read_bytes()
    res = accept(game, proposals(game), job="job_000002")
    assert res.ok and res.unchanged == ["TAB-4.3"] and not res.created and not res.updated and res.files == []
    assert tables_file(game).read_bytes() == before  # prov.job of the first acceptance stays


def test_same_task_with_changed_output_replaces_record(game):
    accept(game, proposals(game), job="job_000001")
    props = proposals(game)
    props[0]["record"]["title"] = "CRT"
    res = accept(game, props, job="job_000002")
    assert res.ok and res.updated == ["TAB-4.3"]
    [rec] = load_documents(tables_file(game))[0]["records"]
    assert rec["title"] == "CRT" and rec["prov"]["job"] == "job_000002"


def test_record_of_another_producer_is_a_conflict(game):
    accept(game, proposals(game))
    path = tables_file(game)
    text = path.read_text(encoding="utf-8").replace("tool: wgc.tables.parse@0", "tool: wgc.other@0")
    path.write_text(text, encoding="utf-8", newline="\n")
    props = proposals(game)
    props[0]["record"]["title"] = "CRT"
    res = accept(game, props)
    assert not res.ok and not res.domain_valid and "konflikt" in res.issues[0]
    assert path.read_text(encoding="utf-8") == text


def test_reserved_fields_are_rejected(game):
    props = proposals(game)
    props[0]["record"]["prov"] = {"kind": "explicit_source"}
    props[0]["record"]["status"] = "accepted"
    res = accept(game, props)
    assert not res.ok and not res.schema_valid and "ADR-0014" in res.issues[0]
    assert not (game / "kb").exists()


def test_proposal_shape_errors(game):
    good = proposals(game)[0]
    cases = {
        "record": [{"anchors": [{"seg": SEG}]}],
        "nieznane pola": [{**good, "prov": {}}],
        "rodzaj": [{**good, "record": {**good["record"], "kind": "concept"}}],
        "seg_hash dopisuje WGC": [{**good, "anchors": [{"seg": SEG, "seg_hash": "sha256:00"}]}],
        "provenance": [{"record": good["record"]}],
        "powtarza": [good, copy.deepcopy(good)],
    }
    for expected, props in cases.items():
        res = accept(game, props)
        assert not res.ok and not res.schema_valid and any(expected in i for i in res.issues), (expected, res.issues)
    assert not (game / "kb").exists()


def test_anchor_must_exist_and_quote_must_be_verbatim(game):
    props = proposals(game)
    props[0]["anchors"] = [{"seg": SEG, "quote": "Combat Results Chart"}]
    res = accept(game, props)
    assert not res.ok and res.schema_valid and not res.domain_valid and "dosłownie" in res.issues[0]
    props[0]["anchors"] = [{"seg": "SEG-dsk.9.9"}]
    assert "nie ma w inwentarzu" in accept(game, props).issues[0]
    props[0]["anchors"] = [{"seg": SEG, "quote": "Combat Results Table"}]
    res = accept(game, props)
    assert res.ok
    assert load_documents(tables_file(game))[0]["records"][0]["prov"]["anchors"][0]["quote"] == "Combat Results Table"


def test_derivation_without_anchors_is_deterministic_derivation(game):
    props = proposals(game)
    props[0].pop("anchors")
    props[0]["derived_from"] = [SEG]
    res = accept(game, props)
    assert res.ok
    prov = load_documents(tables_file(game))[0]["records"][0]["prov"]
    assert prov["kind"] == "deterministic_derivation" and prov["derived_from"] == [SEG] and "anchors" not in prov
    # A model without anchors needs an explicit task declaration (ADR-0027).
    props[0]["record"]["id"] = "TAB-x"
    res = accept(game, props, by={"tier": "local", "profile": "local_fast", "prompt": "wgc.tables.parse@0"})
    assert not res.ok and "allow_llm_inference" in res.issues[0]
    from dataclasses import replace
    res = kb.accept(game, replace(SPEC, allow_llm_inference=True), INPUTS, props,
                    by={"tier": "local", "profile": "local_fast", "prompt": "wgc.tables.parse@0"})
    assert res.ok
    recs = {r["id"]: r for r in load_documents(tables_file(game))[0]["records"]}
    assert recs["TAB-x"]["prov"]["kind"] == "llm_inference"


def test_schema_error_is_not_written(game):
    props = proposals(game)
    props[0]["record"]["complete"] = "yes"
    res = accept(game, props)
    assert not res.ok and not res.schema_valid and "schematem" in res.issues[0]
    assert not (game / "kb").exists()


def test_task_domain_rules_block_writing(game):
    props = proposals(game)
    props[0]["record"]["rows"][0].append("extra")
    res = accept(game, props)
    assert not res.ok and res.schema_valid and not res.domain_valid
    assert not (game / "kb").exists()


def test_invalid_kb_blocks_writing(game):
    other = game / "kb" / "logic" / "rules.yaml"
    other.parent.mkdir(parents=True)
    broken = {"schema": "wgc/logic@0", "records": [
        {"kind": "rule", "id": "R-1.1", "nature": "definition", "statement": {"lang": "en", "text": "x"},
         "formalization": "none", "refs": ["CON-missing"],
         "prov": {"kind": "explicit_source", "by": {"tier": "human", "person": "owner"},
                  "anchors": [{"seg": "SEG-dsk.1.1", "seg_hash": Workspace(game).segment("SEG-dsk.1.1")["text_hash"]}]}}]}
    other.write_text(yaml.safe_dump(broken), encoding="utf-8", newline="\n")
    res = accept(game, proposals(game))
    assert not res.ok and any(i.startswith("unresolved_ref R-1.1") for i in res.issues)
    assert not tables_file(game).exists()


def test_record_stays_in_its_file(game):
    accept(game, proposals(game))
    moved = game / "kb" / "logic" / "combat.yaml"
    tables_file(game).rename(moved)
    props = proposals(game)
    props[0]["record"]["title"] = "CRT"
    res = accept(game, props)
    assert res.ok and "kb/logic/combat.yaml" in res.files and not tables_file(game).exists()


def test_validate_documents_matches_validate():
    valid = ROOT / "contracts" / "fixtures" / "valid"
    files = sorted(valid.glob("*.yaml"))
    docs = [(f.as_posix(), d) for f in files for d in load_documents(f)]
    a, b = validate(files), validate_documents(docs)
    assert (a.files, a.records, a.ok) == (b.files, b.records, b.ok)
    bad = ROOT / "contracts" / "fixtures" / "invalid" / "semantic"
    for f in sorted(bad.glob("*.yaml")):
        docs = [(f.as_posix(), d) for d in load_documents(f)]
        assert validate([f]).codes() == validate_documents(docs).codes(), f.name
