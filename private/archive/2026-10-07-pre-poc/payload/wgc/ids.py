"""Typed stable IDs: grammar `<PREFIX>-<key>` and the prefix → record kind registry (docs/DATA-CONTRACTS.md §4).

The registry is data: the validator (`wgc.validate`) uses it to enforce `kind` ↔ prefix. GLU execution ids
(`build_…`, `job_…`) live outside the KB and are not covered by this grammar.
"""
from __future__ import annotations

import re
from typing import NamedTuple

ID_RE = re.compile(r"^(?P<prefix>[A-Z]{1,4})-(?P<key>[A-Za-z0-9][A-Za-z0-9._:-]*)$")

# prefix → record kinds allowed for that prefix (empty = known prefix with no record kind of its own)
PREFIX_KINDS: dict[str, frozenset[str]] = {
    # Stage 0 (wgc/source)
    "SRC": frozenset({"source_document"}),
    "SEG": frozenset({"segment"}),
    # Stage 1 (wgc/logic)
    "SEC": frozenset(),
    "CON": frozenset({"concept"}),
    "R": frozenset({"rule"}),
    "REL": frozenset({"relation"}),
    "TAB": frozenset({"table"}),
    "PROC": frozenset({"procedure"}),
    "AMB": frozenset({"ambiguity"}),
    "INT": frozenset({"interpretation"}),
    "CASE": frozenset({"case"}),
    "CHG": frozenset({"change"}),
    # all stages (wgc/common)
    "HD": frozenset({"human_decision"}),
    "RR": frozenset({"review_request"}),
    # Stage 1.5 (wgc/digital)
    "ENT": frozenset({"entity"}),
    "DRV": frozenset({"derived"}),
    "ACT": frozenset({"action"}),
    "LEG": frozenset({"legality"}),
    "EVT": frozenset({"event"}),
    "TRG": frozenset({"trigger"}),
    "SEQ": frozenset({"sequence"}),
    "DP": frozenset({"decision_point"}),
    "RNG": frozenset({"random_source"}),
    "MOD": frozenset({"modifier"}),
    "HID": frozenset({"hidden_info"}),
    "INV": frozenset({"invariant"}),
    "PRI": frozenset({"priority"}),
    "BLK": frozenset({"blocker"}),
    "TST": frozenset({"test"}),
}

KIND_PREFIX: dict[str, str] = {kind: prefix for prefix, kinds in PREFIX_KINDS.items() for kind in kinds}


class ParsedId(NamedTuple):
    prefix: str
    key: str


def is_id(value: object) -> bool:
    return isinstance(value, str) and ID_RE.match(value) is not None


def parse_id(value: str) -> ParsedId:
    """Split an ID into prefix and key. Raises ValueError for a string outside the grammar or an unknown prefix."""
    m = ID_RE.match(value) if isinstance(value, str) else None
    if not m:
        raise ValueError(f"not an ID (expected <PREFIX>-<key>): {value!r}")
    if m["prefix"] not in PREFIX_KINDS:
        raise ValueError(f"unknown ID prefix {m['prefix']!r} in {value!r}")
    return ParsedId(m["prefix"], m["key"])


def expected_prefix(kind: str) -> str | None:
    """Prefix a record of this kind must use (None for a kind outside the registry)."""
    return KIND_PREFIX.get(kind)


def check_kind_prefix(kind: str, value: str) -> bool:
    """True when `value` is a well-formed ID whose prefix allows records of `kind`."""
    try:
        prefix, _ = parse_id(value)
    except ValueError:
        return False
    return kind in PREFIX_KINDS[prefix]
