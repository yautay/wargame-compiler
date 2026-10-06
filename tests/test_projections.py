"""M-STAB3b: semantic projections `wgc/projection@2` (ADR-0034, finding F06 of the review after M9a).

The meaning of an incomplete rule (`formalization: none|partial`) is partly in its gloss, so the gloss enters every
projection of such a rule; a predicate's definition and defining rules enter its `digital` projection; every kind
read in M10–M14 and E2E has a projection and nothing falls back to an unversioned one.
"""
from __future__ import annotations

import dataclasses

import pytest

from test_tables import game  # noqa: F401  (fixture)
from wgc import kb, manifest as manifests, tables
from wgc.canonical import CONDITIONAL, PROJECTION_VERSION, PROJECTIONS, ProjectionError, projection, projection_hash
from wgc.kb import KIND_FILES

CONSUMERS = ("logic", "digital", "publication")
RULE = {
    "kind": "rule", "id": "R-3.4", "label": "3.4", "nature": "prohibition", "modality": "must_not",
    "statement": {"lang": "en", "text": "A unit may not enter a hex containing an enemy unit."},
    "formalization": "none", "status": "accepted",
}
PARTIAL = {**RULE, "formalization": "partial", "unformalized": "except when retreating",
           "effects": [{"op": "leave_state", "state": "CON-routed"}]}
PREDICATE = {"kind": "concept", "id": "CON-adjacent", "category": "predicate", "name": "adjacent",
             "definition": {"lang": "en", "text": "two hexes share a side"}, "defined_by": ["R-2.1"],
             "params": [{"type": "CON-hex"}, {"type": "CON-hex"}]}


def test_version():
    assert PROJECTION_VERSION == "wgc/projection@2"


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_gloss_of_an_unformalized_rule_enters_every_projection(consumer):
    changed = {**RULE, "statement": {"lang": "en", "text": "A unit may enter a hex containing an enemy unit."}}
    assert projection_hash(changed, consumer) != projection_hash(RULE, consumer)


@pytest.mark.parametrize("consumer", CONSUMERS)
def test_unformalized_part_of_a_partial_rule_enters_every_projection(consumer):
    assert projection(PARTIAL, consumer)["unformalized"] == "except when retreating"
    changed = {**PARTIAL, "unformalized": "except when attacking"}
    assert projection_hash(changed, consumer) != projection_hash(PARTIAL, consumer)
    reworded = {**PARTIAL, "statement": {"lang": "en", "text": "No entering enemy hexes, except in retreat."}}
    assert projection_hash(reworded, consumer) != projection_hash(PARTIAL, consumer)


@pytest.mark.parametrize("consumer", CONSUMERS)
@pytest.mark.parametrize("formalization", ["full", None])  # absent = full (LOGIC-MODEL)
def test_gloss_of_a_complete_rule_stays_out(consumer, formalization):
    full = {**PARTIAL, "formalization": formalization}
    full.pop("unformalized")
    if formalization is None:
        full.pop("formalization")
    reworded = {**full, "statement": {"lang": "en", "text": "reworded"}, "notes": "x"}
    assert "statement" not in projection(full, consumer)
    assert projection_hash(reworded, consumer) == projection_hash(full, consumer)


def test_change_of_formalization_changes_the_projection():
    assert projection_hash({**RULE, "formalization": "full"}, "digital") != projection_hash(RULE, "digital")


@pytest.mark.parametrize("change", [{"definition": {"lang": "en", "text": "two hexes share a vertex"}},
                                    {"defined_by": ["R-2.1", "R-2.2"]}])
def test_predicate_definition_and_defining_rules_enter_digital(change):
    assert projection_hash({**PREDICATE, **change}, "digital") != projection_hash(PREDICATE, "digital")
    assert projection_hash({**PREDICATE, **change}, "logic") != projection_hash(PREDICATE, "logic")


def test_definition_of_other_concepts_stays_out_of_digital():
    state = {**PREDICATE, "id": "CON-routed", "category": "state"}
    changed = {**state, "definition": {"lang": "en", "text": "other wording"}}
    assert projection_hash(changed, "digital") == projection_hash(state, "digital")
    assert projection_hash(changed, "logic") != projection_hash(state, "logic")


@pytest.mark.parametrize("kind", sorted(KIND_FILES))
def test_every_kb_logic_kind_has_a_logic_projection(kind):
    assert (kind, "logic") in PROJECTIONS


@pytest.mark.parametrize("kind,consumer,field,value", [
    ("table", "logic", "rows", [[1, "x"]]),
    ("table", "digital", "complete", False),
    ("procedure", "logic", "steps", [{"id": "SEQ-1"}]),
    ("ambiguity", "logic", "readings", ["a", "b"]),
    ("interpretation", "digital", "statement", {"lang": "en", "text": "reading A"}),
    ("case", "digital", "expected", "illegal"),
    ("change", "logic", "affects", ["R-1"]),
    ("legality", "digital", "predicate", {"pred": "CON-adjacent"}),
    ("test", "digital", "then", [{"illegal": "LEG-1"}]),
    ("source_document", "logic", "role", "errata"),
])
def test_new_kinds_have_versioned_projections(kind, consumer, field, value):
    rec = {"kind": kind, "id": "X-1", "notes": "n"}
    assert projection_hash({**rec, field: value}, consumer) != projection_hash(rec, consumer)
    assert projection_hash({**rec, "notes": "other"}, consumer) == projection_hash(rec, consumer)


def test_no_projection_is_an_error_naming_the_version():
    with pytest.raises(ProjectionError, match="wgc/projection@2"):
        projection({"kind": "entity", "id": "ENT-unit"}, "digital")


def test_conditional_entries_are_registered_pairs():
    assert set(CONDITIONAL) <= set(PROJECTIONS)


def test_manifest_has_no_fallback_for_kinds_without_projection(game):
    """A record read by a job whose kind has no `logic` projection stops the job; it is never hashed raw."""
    (game / "kb").mkdir()
    (game / "kb" / "digital.yaml").write_text(
        "schema: wgc/digital@0\nrecords:\n  - {kind: entity, id: ENT-unit, concept: CON-unit, status: accepted, "
        "prov: {kind: human_decision, decision: HD-1, by: {tier: human}}}\n", encoding="utf-8")
    spec = dataclasses.replace(tables.PARSE, context_selector=lambda ws, inputs: ["ENT-unit"])
    with pytest.raises(kb.KBError, match="wgc/projection@2"):
        manifests.build(kb.Workspace(game), spec, ("SEG-dsk.4.3",))
