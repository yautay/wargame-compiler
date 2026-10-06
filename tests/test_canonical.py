"""Canonical JSON, content and text hashes, semantic projections (docs/DATA-CONTRACTS.md §5)."""
from __future__ import annotations

import math

import pytest

from wgc.canonical import PROJECTIONS, canonical_json, content_hash, normalize_text, projection, projection_hash, text_hash

GOLDEN_INPUT = {
    "kind": "rule", "id": "R-3.4", "modality": "must_not",
    "limits": [{"value": 1.0, "op": "<="}],
    "notes": None,
    "name": "Café",  # decomposed é → NFC
    "cells": [None, 2.5, True],
}
GOLDEN_JSON = '{"cells":[null,2.5,true],"id":"R-3.4","kind":"rule","limits":[{"op":"<=","value":1}],"modality":"must_not","name":"Café"}'
GOLDEN_HASH = "sha256:c0bc6a9ee39ab555f42c188b7ef2aa1af8553ec56c17164802786f942a9fe234"


def test_canonical_json_golden():
    assert canonical_json(GOLDEN_INPUT) == GOLDEN_JSON.encode("utf-8")


def test_content_hash_golden():
    assert content_hash(GOLDEN_INPUT) == GOLDEN_HASH


def test_content_hash_ignores_key_order():
    reordered = dict(reversed(list(GOLDEN_INPUT.items())))
    reordered["limits"] = [{"op": "<=", "value": 1.0}]
    assert content_hash(reordered) == GOLDEN_HASH


def test_null_fields_are_dropped_but_null_list_items_kept():
    assert canonical_json({"a": None, "b": [None]}) == b'{"b":[null]}'
    assert content_hash({"a": 1, "b": None}) == content_hash({"a": 1})


def test_numbers_and_booleans():
    assert canonical_json({"i": 3.0, "f": 0.5, "t": True, "z": 0}) == b'{"f":0.5,"i":3,"t":true,"z":0}'
    for bad in (math.nan, math.inf):
        with pytest.raises(ValueError):
            canonical_json({"x": bad})


def test_nfc_applies_to_keys():
    assert canonical_json({"é": 1}) == canonical_json({"é": 1})


def test_unsupported_values_are_rejected():
    with pytest.raises(TypeError):
        canonical_json({1: "x"})
    with pytest.raises(TypeError):
        canonical_json({"x": {1, 2}})


def test_text_hash_golden():
    assert text_hash("A Routed unit may not enter a hex adjacent to an enemy unit.") == \
        "sha256:177ec5502601b3a5abb755320254288e5abdd391ec4b4f59516d09de836961aa"


@pytest.mark.parametrize("variant", [
    "A Routed unit may not enter a hex adjacent to an enemy unit.",
    "A Routed unit may not enter\na hex adjacent to an enemy unit.",
    "  A Routed unit may not\r\n  enter a hex\tadjacent to an\n\nenemy unit.  ",
    "A Routed unit may not enter a hex adja-\ncent to an enemy unit.",
    "A Routed unit may not enter a hex adja-  \n   cent to an enemy unit.",
    "A Routed unit may not enter a hex adja­\ncent to an enemy unit.",
    "A Rout­ed unit may not enter a hex adjacent to an enemy unit.",
])
def test_text_hash_invariant_to_wrapping_and_hyphenation(variant):
    assert text_hash(variant) == text_hash("A Routed unit may not enter a hex adjacent to an enemy unit.")


@pytest.mark.parametrize("wrapped, flat", [
    ("the First-\nPlayer", "the First-Player"),
    ("a 3-\nstep retreat", "a 3-step retreat"),
    ("one 6-\nsided die", "one 6-sided die"),
    ("re-\ntreat-\ning units", "retreating units"),
    ("units -\nthen", "units - then"),
])
def test_hyphen_at_line_end(wrapped, flat):
    assert normalize_text(wrapped) == flat
    assert text_hash(wrapped) == text_hash(flat)


def test_text_hash_sensitive_to_content():
    assert text_hash("equal to or less than") != text_hash("less than")


RULE = {
    "kind": "rule", "id": "R-5.2", "label": "5.2", "nature": "automatic_effect", "modality": "is",
    "statement": {"lang": "en", "text": "Rally: roll 1d6 …"},
    "effects": [{"op": "leave_state", "state": "CON-routed"}],
    "formalization": "full", "status": "accepted", "notes": "x",
    "prov": {"kind": "explicit_source", "by": {"tier": "local"}}, "risk": {"model": "wgc/risk@0"},
}


def test_projection_for_digital_excludes_glosses_and_audit():
    p = projection(RULE, "digital")
    assert p == {"kind": "rule", "id": "R-5.2", "nature": "automatic_effect", "modality": "is",
                 "effects": [{"op": "leave_state", "state": "CON-routed"}], "formalization": "full"}


def test_projection_hash_ignores_statement_notes_risk():
    changed = {**RULE, "statement": {"lang": "en", "text": "reworded"}, "notes": "y", "risk": None, "status": "proposed"}
    assert projection_hash(changed, "digital") == projection_hash(RULE, "digital")
    semantic = {**RULE, "modality": "may"}
    assert projection_hash(semantic, "digital") != projection_hash(RULE, "digital")


def test_projection_covers_required_kinds():
    from wgc.kb import KIND_FILES
    # every record kind of kb/logic has a `logic` projection: no fallback can come back (ADR-0034)
    assert {k for k, c in PROJECTIONS if c == "logic"} >= set(KIND_FILES) | {"segment", "source_document"}
    for (kind, _consumer), fields in PROJECTIONS.items():
        assert not {"notes", "refs", "risk", "status", "prov", "kind", "id"} & set(fields), kind
        # a rule's gloss enters only through CONDITIONAL; an interpretation's statement is its content
        assert "statement" not in fields or kind == "interpretation", kind


def test_projection_unknown_pair():
    with pytest.raises(KeyError):
        projection({"kind": "segment", "id": "SEG-x.1"}, "digital")
    with pytest.raises(KeyError):
        projection({"kind": "test", "id": "TST-1"}, "logic")
