"""M-STAB3c: proposal envelope, stage policy, source authority and owned output reconciliation."""
from __future__ import annotations

from dataclasses import replace

import pytest

from test_kb_accept import BY, INPUTS, SEG, SPEC, proposals
from test_tables import game  # noqa: F401
from wgc import contracts, kb, source
from wgc.kb import Workspace
from wgc.validate import load_documents, validate


@pytest.mark.parametrize("role,expected", [
    ("rules", "explicit_source"), ("living_rules", "explicit_source"),
    ("scenario_book", "explicit_source"), ("charts", "explicit_source"),
    ("cards", "explicit_source"), ("counters", "explicit_source"),
    ("map", "explicit_source"), ("module", "explicit_source"),
    ("errata", "errata"), ("faq", "faq"),
    ("designer_clarification", "designer_clarification"),
    ("community_interpretation", None), ("prior_translation", None), ("other", None),
])
def test_changed_source_role_controls_automatic_acceptance(game, role, expected):
    inv = source.read_inventory(game)
    inv.documents[0]["role"] = role
    source.write_inventory(game, inv)
    ws = Workspace(game)
    props = SPEC.deterministic_impl(ws, INPUTS)
    res = kb.accept(game, SPEC, INPUTS, props, by=BY, ws=ws)
    if expected is None:
        assert not res.ok and role in " ".join(res.issues) and not (game / "kb").exists()
    else:
        assert res.ok, res.issues
        records = load_documents(game / "kb" / "logic" / "tables.yaml")[0]["records"]
        assert records[0]["prov"]["kind"] == expected
        assert validate([game / "source", game / "kb"]).ok


@pytest.mark.parametrize("role", [
    "rules", "living_rules", "scenario_book", "charts", "cards", "counters", "map", "module",
    "errata", "faq", "designer_clarification", "community_interpretation", "prior_translation", "other",
])
def test_rebuild_after_source_role_change_reconciles_only_canonical_result(game, role):
    assert kb.accept(game, SPEC, INPUTS, proposals(game), by=BY).ok
    inv = source.read_inventory(game)
    inv.documents[0]["role"] = role
    source.write_inventory(game, inv)
    ws = Workspace(game)
    new = SPEC.deterministic_impl(ws, INPUTS)
    res = kb.accept(game, SPEC, INPUTS, new, by=BY, ws=ws)
    ids = {r["id"] for r in load_documents(game / "kb" / "logic" / "tables.yaml")[0]["records"]}
    if role in {"community_interpretation", "prior_translation", "other"}:
        assert not res.ok and ids == {"TAB-4.3"}
    elif role == "rules":
        assert res.ok and ids == {"TAB-4.3"} and res.retired == []
    else:
        assert res.ok and ids == {"TAB-dsk:4.3"} and res.retired == ["TAB-4.3"]


def test_one_output_vanishes_and_is_tombstoned(game):
    spec = replace(SPEC, validate=lambda ws, inputs, props: [])
    two = proposals(game)
    extra = {"record": {**two[0]["record"], "id": "TAB-extra"}, "anchors": [{"seg": SEG}]}
    first = kb.accept(game, spec, INPUTS, [*two, extra], by=BY)
    assert first.ok and first.created == ["TAB-4.3", "TAB-extra"]
    second = kb.accept(game, spec, INPUTS, two, by=BY)
    assert second.ok and second.retired == ["TAB-extra"] and second.receipt["retired"] == ["TAB-extra"]
    assert [r["id"] for r in load_documents(game / "kb" / "logic" / "tables.yaml")[0]["records"]] == ["TAB-4.3"]
    output = next((d for _, d in kb.kb_documents(game) if d.get("schema") == "wgc/outputs@0"), None)
    assert output["active"] == ["TAB-4.3"] and output["retired"] == ["TAB-extra"]
    assert set(output["hashes"]) == {"TAB-4.3"}
    assert kb.check_receipt(game, second.receipt) == []
    cmp = kb.compare_receipt(game, second.receipt)
    assert cmp.status == "match" and cmp.records["TAB-extra"] == {"state": "missing", "job": None, "retired": True}
    assert validate([game / "source", game / "kb"]).ok


def test_last_output_can_be_retired_with_an_empty_proposal_list(game):
    assert kb.accept(game, SPEC, INPUTS, proposals(game), by=BY).ok
    spec = replace(SPEC, validate=lambda ws, inputs, props: [])
    res = kb.accept(game, spec, INPUTS, [], by=BY)
    assert res.ok and res.records == [] and res.retired == ["TAB-4.3"]
    assert load_documents(game / "kb" / "logic" / "tables.yaml")[0]["records"] == []
    assert validate([game / "source", game / "kb"]).ok


def test_different_input_scope_cannot_take_existing_id(game, monkeypatch):
    spec = replace(SPEC, validate=lambda ws, inputs, props: [])
    assert kb.accept(game, spec, INPUTS, proposals(game), by=BY).ok
    other_inputs = ("SEG-dsk.4.2",)
    candidate = {"record": proposals(game)[0]["record"], "anchors": [{"seg": other_inputs[0]}]}
    # Ownership must be checked before any equality shortcut, even if comparable content matches.
    monkeypatch.setattr(kb, "_comparable", lambda _: b"same")
    res = kb.accept(game, spec, other_inputs, [candidate], by=BY)
    assert not res.ok and "konflikt" in " ".join(res.issues)


def test_legacy_record_with_another_manifest_scope_is_not_claimed(game):
    spec = replace(SPEC, validate=lambda ws, inputs, props: [])
    assert kb.accept(game, spec, INPUTS, proposals(game), by=BY).ok
    path = game / "kb" / "logic" / "tables.yaml"
    [doc] = load_documents(path)
    doc["records"][0]["prov"].pop("owner")
    path.write_text(kb.dump([doc]), encoding="utf-8", newline="\n")
    for output_file in (game / "kb" / "outputs").glob("*.yaml"):
        output_file.unlink()
    other = ("SEG-dsk.4.2",)
    prop = {"record": proposals(game)[0]["record"], "anchors": [{"seg": other[0]}]}
    res = kb.accept(game, spec, other, [prop], by=BY)
    assert not res.ok and "konflikt" in " ".join(res.issues)


def test_manual_change_of_owned_record_is_protected(game):
    assert kb.accept(game, SPEC, INPUTS, proposals(game), by=BY).ok
    path = game / "kb" / "logic" / "tables.yaml"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("Combat Results Table", "Changed by hand"), encoding="utf-8", newline="\n")
    res = kb.accept(game, SPEC, INPUTS, proposals(game), by=BY)
    assert not res.ok and "poza ownerem" in " ".join(res.issues)
    assert path.read_text(encoding="utf-8") != text


def test_proposal_envelope_and_contract_dispatch(game):
    props = proposals(game)
    envelope = {"schema": "wgc/proposal@0", "task": SPEC.name,
                "output_schema": SPEC.output_schema, "proposals": props}
    assert contracts.errors(envelope) == []
    assert kb.accept(game, SPEC, INPUTS, envelope, by=BY).ok
    wrong = {**envelope, "output_schema": "wgc/digital@0#table"}
    rejected = kb.accept(game, SPEC, INPUTS, wrong, by=BY)
    assert not rejected.ok and not rejected.schema_valid and "Envelope" in " ".join(rejected.issues)
    unknown = kb.accept(game, SPEC, INPUTS, {**envelope, "schema": "wgc/unknown@0"}, by=BY)
    assert not unknown.ok and not unknown.schema_valid and "wgc/proposal@0" in " ".join(unknown.issues)
    with pytest.raises(kb.KBError, match="output_schema"):
        kb.accept(game, replace(SPEC, output_schema="wgc/digital@0#table"), INPUTS, props, by=BY)


def test_ambiguity_lifecycle_is_independent_of_resolution(game):
    spec = replace(SPEC, id="test.ambiguity", output_kind="ambiguity", output_schema="wgc/logic@0#ambiguity",
                   validate=lambda ws, inputs, props: [])
    rec = {"kind": "ambiguity", "id": "AMB-test", "question": "Which reading?",
           "readings": [{"id": "a", "gloss": "A"}, {"id": "b", "gloss": "B"}],
           "impact": {"semantic": True}, "resolution": "requires_human_interpretation"}
    res = kb.accept(game, spec, INPUTS, [{"record": rec, "anchors": [{"seg": SEG}]}], by=BY)
    assert res.ok, res.issues
    [stored] = load_documents(game / "kb" / "logic" / "ambiguities.yaml")[0]["records"]
    assert stored["status"] == "accepted" and stored["resolution"] == "requires_human_interpretation"


def test_quote_must_agree_with_span(game):
    prop = proposals(game)[0]
    prop["anchors"] = [{"seg": SEG, "quote": "Combat Results Table", "span": [0, 6]}]
    res = kb.accept(game, SPEC, INPUTS, [prop], by=BY)
    assert not res.ok and "nie odpowiada" in " ".join(res.issues)
    prop["anchors"] = [{"seg": SEG, "quote": "  "}]
    res = kb.accept(game, SPEC, INPUTS, [prop], by=BY)
    assert not res.ok and "pustym cytatem" in " ".join(res.issues)


def test_derived_from_another_output_in_the_same_batch(game):
    spec = replace(SPEC, id="test.concepts", output_kind="concept", output_schema="wgc/logic@0#concept",
                   validate=lambda ws, inputs, props: [])
    first = {"record": {"kind": "concept", "id": "CON-first", "category": "die", "name": "first"},
             "anchors": [{"seg": SEG}]}
    second = {"record": {"kind": "concept", "id": "CON-second", "category": "die", "name": "second"},
              "derived_from": ["CON-first"]}
    result = kb.accept(game, spec, INPUTS, [first, second], by={"tier": "deterministic", "tool": spec.name})
    assert result.ok, result.issues
    records = load_documents(game / "kb" / "logic" / "concepts.yaml")[0]["records"]
    assert next(r for r in records if r["id"] == "CON-second")["prov"]["derived_from"] == ["CON-first"]
    assert validate([game / "source", game / "kb"]).ok
    first["derived_from"] = ["CON-second"]
    rejected = kb.accept(game, spec, INPUTS, [first, second], by={"tier": "deterministic", "tool": spec.name})
    assert not rejected.ok and "cykl" in " ".join(rejected.issues)


def test_digital_stage_uses_its_own_record_contract(game):
    assert kb.accept(game, SPEC, INPUTS, proposals(game), by=BY).ok
    spec = replace(SPEC, id="test.digital", stage="stage1.5", output_kind="legality",
                   output_schema="wgc/digital@0#legality", validate=lambda ws, inputs, props: [])
    rec = {"kind": "legality", "id": "LEG-test", "applies_to": ["TAB-4.3"], "check": "precondition",
           "predicate": True, "reason_code": "test.reason", "realizes": ["TAB-4.3"]}
    res = kb.accept(game, spec, INPUTS, [{"record": rec, "anchors": [{"seg": SEG}]}],
                    by={"tier": "deterministic", "tool": spec.name})
    assert res.ok, res.issues
    path = game / "kb" / "digital" / "legalities.yaml"
    [stored] = load_documents(path)[0]["records"]
    assert stored["status"] == "accepted" and stored["prov"]["owner"]["task"] == "test.digital"
    assert validate([game / "source", game / "kb"]).ok
