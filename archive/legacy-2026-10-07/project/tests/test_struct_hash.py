"""M-STAB3a: `struct_hash` beside `text_hash` (ADR-0032, review F03).

The same words in other cells or lines keep `text_hash` but change `struct_hash`; verify, the `Workspace` text gate
(planner, parser), the job key and `prov.inputs_hash` all see it. Inventories from extractors @0 are regenerated
explicitly.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from glu import planner
from glu.__main__ import main
from glu.store import db_path
from test_glu_build import build
from test_tables import game  # noqa: F401  (fixture)
from wgc import canonical, kb, manifest as manifests, source, tables, tasks, terms
from wgc.canonical import STRUCT_VERSION, content_hash, projection, struct_hash, structure, text_hash
from wgc.kb import KBError, Workspace
from wgc.validate import load_documents, validate

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench" / "minigame"
TABLE = "SEG-dsk.4.3"
PHASES = "SEG-dsk.2.2"  # numbered list of the four phases (wgc.terms.harvest)
CELLS_BEFORE = "| 4 or less | No effect |"
CELLS_AFTER = "| 4 | or less No effect |"  # same words, other cell boundary
LINES_BEFORE = "2. Movement Phase\n3. Combat Phase\n"
LINES_AFTER = "2. Movement Phase 3. Combat Phase\n"  # same words, other line boundary


def edit_rulebook(root: Path, old: str, new: str) -> None:
    path = root / "rulebook.md"
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")


def keys(root: Path) -> dict[str, dict]:
    """Task name → cache key of the planned Stage 1 jobs."""
    return {j.spec.name: j.cache_key for j in planner.plan(Workspace(root), "1").jobs}


def record(root: Path, file: str, rid: str) -> dict:
    return next(r for d in load_documents(root / "kb" / "logic" / file) for r in d["records"] if r["id"] == rid)


def codes(report, severity="error") -> set[str]:
    return report.codes(severity)


# --- the hash ---------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("a, b", [
    ("4 or less\tNo effect\n5–6\tRouted", "4\tor less No effect\n5–6\tRouted"),        # cell boundary (F03)
    ("1. Rally Phase\n2. Movement Phase", "1. Rally Phase 2. Movement Phase"),          # line boundary
    ("4 or less\tNo effect", "4 or less No effect"),                                    # no separator (before ADR-0024)
    ("Roll\tResult\n4\tHit", "Roll\tResult\n\t\n4\tHit"),                               # a row of empty cells
])
def test_struct_hash_separates_what_text_hash_joins(a, b):
    assert text_hash(a) == text_hash(b)
    assert struct_hash(a) != struct_hash(b)


@pytest.mark.parametrize("a, b", [
    ("4 or less\tNo effect", "4  or less \tNo   effect"),   # whitespace inside a cell
    ("A unit\n\nmoves.", "A unit\n   \nmoves."),             # blank lines
    ("A unit\r\nmoves.", "A unit\nmoves."),                  # line endings
    ("Café", "Café"),                             # NFC
])
def test_struct_hash_ignores_what_no_parser_reads(a, b):
    assert struct_hash(a) == struct_hash(b)


def test_struct_hash_is_versioned():
    assert STRUCT_VERSION == "wgc/struct@0"
    text = "Roll\tResult\n4\tHit"
    assert structure(text) == [["Roll", "Result"], ["4", "Hit"]]
    assert struct_hash(text) == content_hash({"format": STRUCT_VERSION, "lines": structure(text)})
    assert canonical.PROJECTION_VERSION == "wgc/projection@3"  # @3 includes ambiguity resolution (ADR-0035)
    assert "struct_hash" in canonical.PROJECTIONS[("segment", "logic")]


def test_parsers_read_only_the_structure():
    """F03: equal text_hash, other cells → another table; equal struct_hash → the same table and terms."""
    a, b = "Result\tEffect\n4 or less\tNo effect", "Result\tEffect\n4\tor less No effect"
    assert tables.parse(a)[1] == [[{"min": None, "max": 4}, "No effect"]]
    assert tables.parse(b)[1] == [[4, "or less No effect"]]
    assert tables.parse("Result \t Effect\n\n4  or less\tNo effect") == tables.parse(a)
    seg = {"segment_type": "rule"}
    phases = [m[1] for m in terms.matches(seg, "Phases:\n1. Rally Phase\n2. Movement Phase\n3. Combat Phase")]
    joined = [m[1] for m in terms.matches(seg, "Phases:\n1. Rally Phase\n2. Movement Phase 3. Combat Phase")]
    assert phases == ["rally_phase", "movement_phase", "combat_phase"] and joined == ["rally_phase"]


# --- verify and the text gate (planner, parser) -------------------------------------------------------------------

def test_f03_cell_edit_in_cache_is_detected(game):
    """The edit from review F03: `4 or less<TAB>No effect` → `4<TAB>or less No effect` in .glu/source/."""
    ws = Workspace(game)
    path = source.cache_dir(game, "SRC-dsk.rules") / f"{TABLE}.txt"
    old = path.read_text(encoding="utf-8")
    new = old.replace("4 or less\tNo effect", "4\tor less No effect")
    assert new != old and text_hash(new) == ws.segment(TABLE)["text_hash"]
    path.write_text(new, encoding="utf-8", newline="\n")
    report = source.verify(game)
    assert codes(report) == {"cache_mismatch"}
    [d] = report.diagnostics
    assert d.subject == TABLE and "wiersze albo komórki" in d.message
    with pytest.raises(KBError, match="struct_hash"):
        Workspace(game).text(TABLE)
    with pytest.raises(KBError, match="wgc source extract"):
        planner.plan(Workspace(game), "1")
    source.extract(game)
    assert not source.verify(game).diagnostics and Workspace(game).text(TABLE) == old


def test_cell_boundary_change_in_source_changes_job_key_and_provenance(game):
    before = keys(game)
    assert build(game).state == "done"
    rec0 = record(game, "tables.yaml", "TAB-4.3")
    seg0 = Workspace(game).segment(TABLE)

    edit_rulebook(game, CELLS_BEFORE, CELLS_AFTER)
    report = source.verify(game)
    assert codes(report) == {"file_hash_mismatch", "segment_struct_mismatch"}  # no segment_hash_mismatch
    assert [d.subject for d in report.diagnostics if d.code == "segment_struct_mismatch"] == [TABLE]
    assert "zmienione 1" in source.extract(game)[-1]
    seg1 = Workspace(game).segment(TABLE)
    assert seg1["text_hash"] == seg0["text_hash"] and seg1["struct_hash"] != seg0["struct_hash"]

    after = keys(game)
    assert after["wgc.tables.parse@0"]["input_hash"] != before["wgc.tables.parse@0"]["input_hash"]
    assert after["wgc.terms.harvest@0"] == before["wgc.terms.harvest@0"]  # SEG-dsk.4.3 is not its input

    result = build(game)
    assert result.state == "done"
    rec1 = record(game, "tables.yaml", "TAB-4.3")
    assert rec1["rows"][0] == [4, "or less No effect"] and rec0["rows"][0] == [{"min": None, "max": 4}, "No effect"]
    assert rec1["prov"]["anchors"] == rec0["prov"]["anchors"]  # seg_hash is text_hash: the anchor still holds
    assert rec1["prov"]["inputs_hash"] != rec0["prov"]["inputs_hash"]
    assert manifests.Manifest(rec1["prov"]["manifest"]).input_hash == after["wgc.tables.parse@0"]["input_hash"]
    assert validate([game / "source", game / "kb"]).ok


def test_line_boundary_change_changes_harvest_key_and_provenance(game):
    before = keys(game)
    assert build(game).state == "done"
    con0 = record(game, "concepts.yaml", "CON-rally_phase")

    edit_rulebook(game, LINES_BEFORE, LINES_AFTER)
    source.extract(game)
    seg = Workspace(game).segment(PHASES)
    assert seg["text_hash"] == next(s for s in source.read_inventory(BENCH).segments if s["id"] == PHASES)["text_hash"]

    after = keys(game)
    assert after["wgc.terms.harvest@0"]["input_hash"] != before["wgc.terms.harvest@0"]["input_hash"]
    assert after["wgc.tables.parse@0"] == before["wgc.tables.parse@0"]
    ws = Workspace(game)
    names = [p["record"]["name"] for p in tasks.get("wgc.terms.harvest").deterministic_impl(ws, terms._select(
        ws, [PHASES])[0])]
    assert "Combat Phase" not in names and "Rally Phase" in names

    assert build(game).state == "done"
    con1 = record(game, "concepts.yaml", "CON-rally_phase")
    assert con1["prov"]["anchors"] == con0["prov"]["anchors"]
    assert con1["prov"]["inputs_hash"] != con0["prov"]["inputs_hash"]
    # the concept's evidence is its one anchor; what the job read (every input) is its manifest (ADR-0033, F05)
    assert con1["prov"]["inputs_hash"] == kb.evidence_hash([projection(seg, "logic")])
    assert manifests.Manifest(con1["prov"]["manifest"]).input_hash == after["wgc.terms.harvest@0"]["input_hash"]


# --- explicit regeneration of artifacts from extractors @0 ------------------------------------------------------

def downgrade(root: Path, verified: str | None = None) -> None:
    """The inventory as `wgc.ingest.markdown@0` wrote it: no `struct_hash`; `verified` gets `verified_by_render`."""
    inv = source.read_inventory(root)
    for d in inv.documents:
        if "extractor" in d:
            d["extractor"] = d["extractor"].replace("@1", "@0")
    for s in inv.segments:
        s.pop("struct_hash")
        if s["id"] == verified:
            s["verified_by_render"] = True
    source.write_inventory(root, inv)


def test_inventory_from_extractor_0_must_be_regenerated(game, capsys):
    downgrade(game)
    report = source.verify(game)
    assert codes(report) == {"struct_hash_missing"} and codes(report, "warning") == {"extractor_changed"}
    [d] = [d for d in report.diagnostics if d.code == "struct_hash_missing"]
    assert d.subject == "SRC-dsk.rules" and len(d.affected) == 31 and "wgc source extract" in d.message
    with pytest.raises(KBError, match="sprzed ADR-0032"):
        Workspace(game).text(TABLE)
    with pytest.raises(KBError, match="sprzed ADR-0032"):
        planner.plan(Workspace(game), "1")
    assert main(["build", "--root", str(game), "--stage", "1"]) == 2
    assert "sprzed ADR-0032" in capsys.readouterr().err and not db_path(game).exists()

    assert "zmienione 0" in source.extract(game)[-1]  # gaining struct_hash is not a change of the segment
    assert source.inventory_path(game).read_bytes() == source.inventory_path(BENCH).read_bytes()
    assert not source.verify(game).diagnostics
    assert planner.plan(Workspace(game), "1").jobs


def test_verified_by_render_survives_regeneration_but_not_a_structure_change(game):
    downgrade(game, verified=TABLE)
    source.extract(game)
    assert Workspace(game).segment(TABLE)["verified_by_render"] is True
    edit_rulebook(game, CELLS_BEFORE, CELLS_AFTER)
    source.extract(game)
    assert "verified_by_render" not in Workspace(game).segment(TABLE)


def test_committed_inventory_and_fixture_carry_struct_hash():
    inventory = re.findall(r"\{kind: segment, [^}]*\}", source.inventory_path(BENCH).read_text(encoding="utf-8"))
    assert inventory and all("struct_hash: " in s for s in inventory)
    fixture = (ROOT / "contracts" / "fixtures" / "valid" / "source.minigame.yaml").read_text(encoding="utf-8")
    assert fixture.count("struct_hash: ") == fixture.count("kind: segment,") > 0
    assert 'extractor: "wgc.ingest.markdown@1"' in fixture
