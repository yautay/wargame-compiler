"""Validator: valid fixtures are a closed set, each semantic-invalid fixture yields exactly its expected code, CLI."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from wgc import contracts
from wgc.__main__ import main
from wgc.validate import CODES, load_documents, validate

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "contracts" / "fixtures"
SEMANTIC = sorted((FIXTURES / "invalid" / "semantic").glob("*.yaml"))
EXPECT = re.compile(r"^# EXPECT: (\w+)\s*$", re.M)

HD = {"kind": "human_decision", "id": "HD-001", "question": "q", "answer": "a", "by": "owner", "at": "2026-10-05T12:00:00Z"}
BY_HD = {"kind": "human_decision", "by": {"tier": "human", "person": "owner"}, "decision": "HD-001"}


def write(tmp_path: Path, *docs: dict, name: str = "kb.yaml") -> Path:
    import yaml
    p = tmp_path / name
    p.write_text(yaml.safe_dump_all(list(docs), sort_keys=False, allow_unicode=True), encoding="utf-8")
    return p


def logic(*records: dict) -> dict:
    return {"schema": "wgc/logic@0", "records": [HD, *records]}


def concept(id_: str, **extra) -> dict:
    return {"kind": "concept", "id": id_, "category": "other", "name": id_, "prov": BY_HD, **extra}


# ---- fixtures ---------------------------------------------------------------------------------

def test_valid_fixtures_are_a_closed_set():
    report = validate([FIXTURES / "valid"])
    assert report.diagnostics == []
    assert report.ok and report.records > 0


def test_semantic_fixtures_cover_every_l1_and_provenance_code():
    expected = {EXPECT.search(f.read_text(encoding="utf-8")).group(1) for f in SEMANTIC}
    assert expected == set(CODES) - {"load_error", "schema_error"}


@pytest.mark.parametrize("fixture", SEMANTIC, ids=lambda p: p.name)
def test_semantic_fixture_is_schema_valid(fixture):
    for doc in load_documents(fixture):
        assert contracts.errors(doc) == []


@pytest.mark.parametrize("fixture", SEMANTIC, ids=lambda p: p.name)
def test_semantic_fixture_yields_exactly_expected_code(fixture):
    m = EXPECT.search(fixture.read_text(encoding="utf-8"))
    assert m, f"{fixture.name} needs a '# EXPECT: <code>' line"
    report = validate([fixture])
    assert report.codes() == {m.group(1)}, [d.to_dict() for d in report.diagnostics]
    assert not report.ok


@pytest.mark.parametrize("fixture", sorted((FIXTURES / "invalid").glob("*.yaml")), ids=lambda p: p.name)
def test_schema_invalid_fixtures_report_schema_error(fixture):
    assert "schema_error" in validate([fixture]).codes()


# ---- individual checks ------------------------------------------------------------------------

def test_duplicate_across_files(tmp_path):
    write(tmp_path, logic(concept("CON-a")), name="a.yaml")
    write(tmp_path, {"schema": "wgc/logic@0", "records": [concept("CON-a")]}, name="b.yaml")
    report = validate([tmp_path])
    assert report.codes() == {"duplicate_id"}
    # HD-001 is defined once (b.yaml only references it), CON-a twice
    assert [d.subject for d in report.diagnostics] == ["CON-a"]


def test_refs_resolve_across_files_and_documents(tmp_path):
    write(tmp_path, logic(concept("CON-a")), {"schema": "wgc/logic@0", "records": [concept("CON-b", refs=["CON-a"])]},
          name="a.yaml")
    write(tmp_path, {"schema": "wgc/logic@0", "records": [concept("CON-c", refs=["CON-a", "CON-b"])]}, name="b.yaml")
    assert validate([tmp_path]).diagnostics == []


@pytest.mark.parametrize("record, field", [
    (concept("CON-a", refs=["CON-zzz"]), "refs"),
    ({"kind": "concept", "id": "CON-a", "category": "other", "name": "a",
      "prov": {"kind": "llm_inference", "by": {"tier": "local"}, "derived_from": ["CON-zzz"]}}, "prov.derived_from"),
    ({"kind": "relation", "id": "REL-1", "type": "see", "from": "CON-zzz", "to": "HD-001", "prov": BY_HD}, "from"),
    ({"kind": "interpretation", "id": "INT-1", "ambiguity": "AMB-zzz", "reading": "a", "status": "proposed",
      "prov": {"kind": "interpretation", "by": {"tier": "premium"}, "derived_from": ["HD-001"]}}, "ambiguity"),
])
def test_unresolved_ref_in_logic(tmp_path, record, field):
    report = validate([write(tmp_path, logic(record))])
    assert report.codes() == {"unresolved_ref"}
    (d,) = report.diagnostics
    assert d.subject == record["id"] and f"`{field}`" in d.message and d.affected[0].endswith("zzz")


@pytest.mark.parametrize("record, field", [
    ({"kind": "blocker", "id": "BLK-1", "cause": ["AMB-zzz"], "affects": [], "needed": "x", "status": "open"}, "cause"),
    ({"kind": "blocker", "id": "BLK-1", "cause": [], "affects": ["TRG-zzz"], "needed": "x", "status": "open"}, "affects"),
    ({"kind": "modifier", "id": "MOD-1", "applies_to": "DRV-zzz", "value": 1, "realizes": []}, "applies_to"),
    ({"kind": "event", "id": "EVT-1", "name": "E", "payload": [], "realizes": ["R-zzz"]}, "realizes"),
    ({"kind": "entity", "id": "ENT-1", "concept": "CON-x", "fields": [{"name": "f", "type": "int", "realizes": ["R-zzz"]}],
      "realizes": []}, "fields[].realizes"),
    ({"kind": "test", "id": "TST-1", "category": "legal", "from_case": "CASE-zzz", "given": {}, "when": {}, "then": {},
      "realizes": []}, "from_case"),
    ({"kind": "test", "id": "TST-1", "category": "legal", "covers": ["ACT-zzz"], "given": {}, "when": {}, "then": {},
      "realizes": []}, "covers"),
])
def test_unresolved_ref_in_digital(tmp_path, record, field):
    report = validate([write(tmp_path, {"schema": "wgc/digital@0", "records": [record]})])
    assert report.codes() == {"unresolved_ref"}, [d.to_dict() for d in report.diagnostics]
    assert f"`{field}`" in report.diagnostics[0].message


def test_unresolved_segment_doc_and_anchor(tmp_path):
    src = {"schema": "wgc/source@0", "records": [
        {"kind": "segment", "id": "SEG-x.1", "doc": "SRC-zzz", "segment_type": "rule", "text_hash": "sha256:0000000000000001"}]}
    anchored = concept("CON-a", prov={"kind": "explicit_source", "by": {"tier": "deterministic"},
                                      "anchors": [{"seg": "SEG-zzz", "seg_hash": "sha256:0000000000000001"}]})
    report = validate([write(tmp_path, src, logic(anchored))])
    assert report.codes() == {"unresolved_ref"}
    assert sorted(d.affected[0] for d in report.diagnostics) == ["SEG-zzz", "SRC-zzz"]


def test_sequence_nodes_are_defined_ids(tmp_path):
    seq = {"kind": "sequence", "id": "SEQ-turn", "realizes": [], "nodes": [
        {"id": "SEQ-turn", "level": "game_turn"}, {"id": "SEQ-move", "level": "phase"}, {"id": "ACT-x", "level": "step"}]}
    trg = {"kind": "trigger", "id": "TRG-1", "fires_on": "SEQ-move", "response": {}, "mandatory": True, "realizes": [],
           "blocked_by": []}
    report = validate([write(tmp_path, {"schema": "wgc/digital@0", "records": [seq, trg]})])
    # a node reusing the sequence id is a duplicate; a node with a foreign prefix is a mismatch
    assert {(d.code, d.subject) for d in report.diagnostics} == {("duplicate_id", "SEQ-turn"), ("kind_prefix_mismatch", "ACT-x")}


def test_accepted_interpretation_without_decision_field(tmp_path):
    amb = {"kind": "ambiguity", "id": "AMB-1", "question": "q", "readings": [{"id": "a", "gloss": "a"}, {"id": "b", "gloss": "b"}],
           "impact": {}, "status": "open", "prov": BY_HD}
    intp = {"kind": "interpretation", "id": "INT-1", "ambiguity": "AMB-1", "reading": "a", "status": "accepted",
            "prov": {"kind": "interpretation", "by": {"tier": "human"}, "derived_from": ["AMB-1"]}}
    report = validate([write(tmp_path, logic(amb, intp))])
    assert report.codes() == {"schema_error", "missing_decision"}


def test_decision_pointing_to_non_hd_record(tmp_path):
    report = validate([write(tmp_path, logic(concept("CON-a"), concept("CON-b", prov={**BY_HD, "decision": "CON-a"})))])
    assert report.codes() == {"missing_decision"}


def test_non_domain_documents_get_l0_only(tmp_path):
    report = validate([FIXTURES / "valid" / "glu.job.yaml", FIXTURES / "valid" / "igw.api.yaml"])
    assert report.diagnostics == [] and report.records == 0


def test_load_errors(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("schema: [unclosed\n", encoding="utf-8")
    (tmp_path / "empty.yaml").write_text("# nothing\n", encoding="utf-8")
    report = validate([tmp_path, tmp_path / "missing.yaml"])
    assert report.codes() == {"load_error"} and len(report.diagnostics) == 3


def test_unknown_contract_is_schema_error(tmp_path):
    report = validate([write(tmp_path, {"schema": "wgc/nope@0", "records": []})])
    assert report.codes() == {"schema_error"}


def test_schema_error_subject_is_record_id(tmp_path):
    report = validate([write(tmp_path, logic({"kind": "concept", "id": "CON-a", "category": "nope", "name": "a", "prov": BY_HD}))])
    assert {d.subject for d in report.diagnostics if d.code == "schema_error"} == {"CON-a"}


# ---- CLI --------------------------------------------------------------------------------------

def test_cli_valid(capsys):
    assert main(["validate", str(FIXTURES / "valid")]) == 0
    assert "OK" in capsys.readouterr().out


def test_cli_invalid_json(capsys):
    assert main(["validate", "--json", str(FIXTURES / "invalid" / "semantic" / "unresolved_ref.yaml")]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is False and out["errors"] == 1
    (d,) = out["diagnostics"]
    assert set(d) == {"code", "severity", "subject", "message", "affected", "location"}
    assert (d["code"], d["severity"], d["subject"], d["affected"]) == ("unresolved_ref", "error", "REL-001", ["R-2"])


def test_cli_text_is_polish(capsys):
    assert main(["validate", str(FIXTURES / "invalid" / "semantic" / "kind_prefix_mismatch.yaml")]) == 1
    out = capsys.readouterr().out
    assert "BŁĄD kind_prefix_mismatch CON-x" in out and "NIEPOPRAWNE" in out


def test_cli_requires_paths(capsys):
    with pytest.raises(SystemExit) as e:
        main(["validate"])
    assert e.value.code == 2
