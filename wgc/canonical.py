"""Canonical serialization, content hashes and semantic projections (docs/DATA-CONTRACTS.md §5).

- `canonical_json`: UTF-8, NFC strings (keys too), sorted keys, no whitespace, integral floats as integers,
  dict entries with value `null` dropped (`null` inside lists is kept: table cells use it).
- `content_hash`: `sha256:` + hex of the canonical JSON.
- `text_hash`: hash of normalized source text (NFC, soft hyphens and hyphenated line breaks joined, whitespace collapsed).
  Invariant to line wrapping and to the cell separator: anchors (`seg_hash`) and Markdown ↔ PDF parity use it.
- `struct_hash`: versioned hash of the lines and cells of an extracted segment text (`structure`), i.e. what the
  parsers of the text read (table rows and cells, numbered list lines). Planner keys and `prov.inputs_hash` depend on
  it through the `logic` projection of a segment (ADR-0032).
- `projection`: the fields of a record that a consumer depends on. Field lists are data (`PROJECTIONS`, conditional
  fields in `CONDITIONAL`), versioned with `PROJECTION_VERSION` (ADR-0034); no pair, no projection (`ProjectionError`).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata

# @1: `struct_hash` in the `logic` projection of a segment (ADR-0032). @2: unformalized content of incomplete rules,
# predicate definitions, projections of the kinds read in M10–M14 and E2E, no fallbacks (ADR-0034).
PROJECTION_VERSION = "wgc/projection@2"
STRUCT_VERSION = "wgc/struct@0"  # definition of `structure`; any change to it is a new version (ADR-0032)
CELL_SEP = "\t"  # cell separator of table rows in extracted segment text (wgc.ingest.*, ADR-0032)

# (record kind, consumer) → fields entering the semantic hash besides `kind` and `id`.
# Consumers: `logic` (Stage 1 jobs reading the record as input or context), `digital` (Stage 1.5),
# `publication` (Stage 3 translation of a segment). Glosses of a rule (`statement`) enter only through `CONDITIONAL`;
# `notes`, `refs`, `risk`, `status` and `prov` never enter a projection. A pair missing here has no projection: callers
# get an error naming `PROJECTION_VERSION`, never a fallback (ADR-0034).
_TABLE = ("title", "columns", "rows", "complete")
_PROCEDURE = ("title", "category", "repeat", "steps")
_CASE = ("polarity", "question", "expected", "verdict", "chain")
_INTERPRETATION = ("ambiguity", "reading", "statement")  # the statement of an interpretation is its content
PROJECTIONS: dict[tuple[str, str], tuple[str, ...]] = {
    ("segment", "logic"): ("doc", "label", "segment_type", "text_hash", "struct_hash"),
    ("segment", "publication"): ("segment_type", "text_hash"),
    ("source_document", "logic"): ("role", "seg_prefix", "precedence"),
    ("rule", "logic"): ("label", "section", "layer", "applies_in", "nature", "modality", "bind", "actor", "action",
                        "target", "timing", "conditions", "effects", "limits", "triggers", "formalization", "ambiguities"),
    ("rule", "digital"): ("nature", "modality", "bind", "actor", "action", "target", "timing", "conditions", "effects",
                          "limits", "triggers", "layer", "applies_in", "formalization"),
    ("rule", "publication"): ("nature", "modality", "bind", "actor", "action", "target", "timing", "conditions",
                              "effects", "limits", "triggers"),
    ("concept", "logic"): ("category", "name", "source_terms", "definition", "of", "params", "parent", "value_type",
                           "range", "values", "defined_by"),
    ("concept", "digital"): ("category", "name", "of", "params", "value_type", "range", "values", "parent"),
    ("concept", "publication"): ("category", "name", "source_terms", "definition"),
    ("relation", "logic"): ("type", "from", "to", "when", "priority_basis"),
    ("relation", "digital"): ("type", "from", "to", "when", "priority_basis"),
    ("relation", "publication"): ("type", "from", "to"),
    ("table", "logic"): _TABLE,
    ("table", "digital"): _TABLE,
    ("table", "publication"): ("title", "columns", "rows"),
    ("procedure", "logic"): _PROCEDURE,
    ("procedure", "digital"): _PROCEDURE,
    ("procedure", "publication"): ("title", "steps"),
    ("ambiguity", "logic"): ("scope", "question", "readings", "recommendation", "impact", "resolved_by"),
    ("interpretation", "logic"): _INTERPRETATION,
    ("interpretation", "digital"): _INTERPRETATION,
    ("case", "logic"): _CASE,
    ("case", "digital"): _CASE,
    ("change", "logic"): ("change_kind", "affects", "summary", "from_edition", "to_edition"),
    ("legality", "digital"): ("applies_to", "check", "predicate", "reason_code", "unless", "realizes"),
    ("test", "digital"): ("category", "from_case", "covers", "given", "when", "then", "realizes"),
}
# Fields that enter a projection only when the record says its structure does not carry the whole meaning:
# (kind, consumer) → ((field, value when absent, values that switch it on, extra fields), …) (ADR-0034).
_INCOMPLETE_RULE = (("formalization", "full", ("none", "partial"), ("statement", "unformalized")),)
CONDITIONAL: dict[tuple[str, str], tuple[tuple[str, str | None, tuple[str, ...], tuple[str, ...]], ...]] = {
    ("rule", "logic"): _INCOMPLETE_RULE,
    ("rule", "digital"): _INCOMPLETE_RULE,
    ("rule", "publication"): _INCOMPLETE_RULE,
    ("concept", "digital"): (("category", None, ("predicate",), ("definition", "defined_by")),),
}


def _normalize(obj):
    if obj is None or isinstance(obj, bool):
        return obj
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        if not math.isfinite(obj):
            raise ValueError(f"canonical JSON does not allow {obj!r}")
        return int(obj) if obj.is_integer() else obj
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if not isinstance(k, str):
                raise TypeError(f"canonical JSON keys must be strings, got {k!r}")
            if v is None:
                continue
            nk = unicodedata.normalize("NFC", k)
            if nk in out:
                raise ValueError(f"keys collide after NFC normalization: {k!r}")
            out[nk] = _normalize(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [_normalize(v) for v in obj]
    raise TypeError(f"canonical JSON does not support {type(obj).__name__}: {obj!r}")


def canonical_json(obj) -> bytes:
    return json.dumps(_normalize(obj), ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def content_hash(obj) -> str:
    return sha256_hex(canonical_json(obj))


_SOFT_HYPHEN = re.compile("­\\s*")
# hyphen at a line end between two non-space characters (lookarounds, so consecutive breaks all match)
_HYPHEN_BREAK = re.compile(r"(?<=(\S))[-‐][ \t]*\n\s*(?=(\S))")
_WHITESPACE = re.compile(r"\s+")


def _join_hyphenation(m: re.Match) -> str:
    # A word split between letters continues in lower case ("move-\nment" → "movement"); otherwise the hyphen is real
    # and only the line break goes ("First-\nPlayer" → "First-Player", "3-\nstep" → "3-step").
    return "" if m[1].isalpha() and m[2].islower() else "-"


def normalize_text(text: str) -> str:
    """Normalization behind `text_hash`: invariant to line wrapping and hyphenation at line ends."""
    s = unicodedata.normalize("NFC", text).replace("\r\n", "\n").replace("\r", "\n")
    s = _SOFT_HYPHEN.sub("", s)
    s = _HYPHEN_BREAK.sub(_join_hyphenation, s)
    return _WHITESPACE.sub(" ", s).strip()


def text_hash(text: str) -> str:
    return sha256_hex(normalize_text(text).encode("utf-8"))


def structure(text: str) -> list[list[str]]:
    """Lines of an extracted segment text, each a list of cells (`STRUCT_VERSION`): lines split at line breaks, cells
    at `CELL_SEP`, each cell NFC with whitespace collapsed. A blank line without a cell separator is dropped; a row of
    empty cells is kept (a table row). No hyphenation joining: here a line break is structure."""
    s = unicodedata.normalize("NFC", text).replace("\r\n", "\n").replace("\r", "\n")
    return [[" ".join(c.split()) for c in line.split(CELL_SEP)] for line in s.split("\n")
            if CELL_SEP in line or line.strip()]


def struct_hash(text: str) -> str:
    """Hash of `structure(text)` with its version. Equal `text_hash` and different `struct_hash`: the same words in
    other lines or cells (ADR-0032)."""
    return content_hash({"format": STRUCT_VERSION, "lines": structure(text)})


class ProjectionError(KeyError):
    """No projection for this record kind and consumer in `PROJECTION_VERSION` (ADR-0034)."""

    def __str__(self) -> str:
        return str(self.args[0])


def projection(record: dict, consumer: str) -> dict:
    """Semantic projection of `record` for `consumer` (fields absent from the record are absent from the projection).
    A record kind without a projection for `consumer` raises `ProjectionError`; there is no fallback."""
    kind = record.get("kind")
    try:
        fields = PROJECTIONS[(kind, consumer)]
    except KeyError:
        raise ProjectionError(f"brak projekcji rodzaju `{kind}` dla konsumenta `{consumer}` "
                              f"({PROJECTION_VERSION})") from None
    for field, default, values, extra in CONDITIONAL.get((kind, consumer), ()):
        if record.get(field, default) in values:
            fields = fields + tuple(f for f in extra if f not in fields)
    out = {"kind": kind, "id": record.get("id")}
    out.update({f: record[f] for f in fields if f in record})
    return out


def projection_hash(record: dict, consumer: str) -> str:
    return content_hash(projection(record, consumer))
