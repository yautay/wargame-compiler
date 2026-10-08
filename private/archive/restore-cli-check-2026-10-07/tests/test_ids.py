"""IDs: grammar, prefix registry and kind ↔ prefix (docs/DATA-CONTRACTS.md §4)."""
from __future__ import annotations

import json
import re

import pytest

from wgc import contracts, ids


@pytest.mark.parametrize("value, prefix, key", [
    ("R-3.4", "R", "3.4"),
    ("R-SB:2.1", "R", "SB:2.1"),
    ("SEG-dsk.3.4", "SEG", "dsk.3.4"),
    ("SEG-dsk.sb:2.1", "SEG", "dsk.sb:2.1"),
    ("CON-scn.ford", "CON", "scn.ford"),
    ("LEG-move.routed_adjacent", "LEG", "move.routed_adjacent"),
    ("PROC-sequence_of_play", "PROC", "sequence_of_play"),
])
def test_parse_id(value, prefix, key):
    assert ids.parse_id(value) == (prefix, key)
    assert ids.is_id(value)


@pytest.mark.parametrize("value", ["", "R3.4", "r-3.4", "R-", "R-.4", "ABCDE-1", "R-3 4", "build_01JA0000", None, 7])
def test_parse_id_rejects_grammar(value):
    with pytest.raises(ValueError):
        ids.parse_id(value)


def test_parse_id_rejects_unknown_prefix():
    assert ids.is_id("XYZ-1")  # grammatical
    with pytest.raises(ValueError, match="unknown ID prefix"):
        ids.parse_id("XYZ-1")


@pytest.mark.parametrize("kind, value, ok", [
    ("rule", "R-3.4", True),
    ("rule", "CON-x", False),
    ("concept", "CON-x", True),
    ("decision_point", "DP-movement", True),
    ("human_decision", "HD-001", True),
    ("human_decision", "DP-001", False),
    ("segment", "SEG-dsk.3.4", True),
    ("rule", "XYZ-1", False),
    ("rule", "not an id", False),
])
def test_check_kind_prefix(kind, value, ok):
    assert ids.check_kind_prefix(kind, value) is ok


def test_registry_covers_every_domain_record_kind():
    """Every record kind of the domain contracts has exactly one prefix."""
    kinds = set()
    for contract in ("wgc/source@0", "wgc/logic@0", "wgc/digital@0"):
        schema = contracts.schema_for(contract)
        kinds |= set(schema["$defs"]["record"]["properties"]["kind"]["enum"])
    assert kinds == set(ids.KIND_PREFIX)
    assert all(ids.expected_prefix(k) for k in kinds)


@pytest.mark.parametrize("value", ["R-3.4", "R-SB:2.1", "SEG-dsk.3.4", "ABCD-x", "ABCDE-1", "R-", "R-.4", "r-1", "R-3 4", "R-a-b"])
def test_grammar_agrees_with_schema_pattern(value):
    common = json.loads((contracts.SCHEMA_DIR / "common.schema.json").read_text(encoding="utf-8"))
    assert bool(re.match(common["$defs"]["id"]["pattern"], value)) == ids.is_id(value)
