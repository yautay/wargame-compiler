"""Canonical serialization, content hashes and semantic projections (docs/DATA-CONTRACTS.md §5).

- `canonical_json`: UTF-8, NFC strings (keys too), sorted keys, no whitespace, integral floats as integers,
  dict entries with value `null` dropped (`null` inside lists is kept: table cells use it).
- `content_hash`: `sha256:` + hex of the canonical JSON.
- `text_hash`: hash of normalized source text (NFC, soft hyphens and hyphenated line breaks joined, whitespace collapsed).
- `projection`: the fields of a record that a consumer depends on. Field lists are data, versioned with the contract.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata

PROJECTION_VERSION = "wgc/projection@0"

# (record kind, consumer) → fields entering the semantic hash besides `kind` and `id`.
# Consumers: `logic` (Stage 1 jobs reading the record as input or context), `digital` (Stage 1.5),
# `publication` (Stage 3 translation of a segment). Glosses (`statement`, `definition` outside publication),
# `notes`, `risk`, `status` and `prov` never enter a projection.
PROJECTIONS: dict[tuple[str, str], tuple[str, ...]] = {
    ("segment", "logic"): ("doc", "label", "segment_type", "text_hash"),
    ("segment", "publication"): ("segment_type", "text_hash"),
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


def projection(record: dict, consumer: str) -> dict:
    """Semantic projection of `record` for `consumer` (fields absent from the record are absent from the projection)."""
    kind = record.get("kind")
    try:
        fields = PROJECTIONS[(kind, consumer)]
    except KeyError:
        raise KeyError(f"no projection for kind {kind!r} and consumer {consumer!r} ({PROJECTION_VERSION})") from None
    out = {"kind": kind, "id": record.get("id")}
    out.update({f: record[f] for f in fields if f in record})
    return out


def projection_hash(record: dict, consumer: str) -> str:
    return content_hash(projection(record, consumer))
