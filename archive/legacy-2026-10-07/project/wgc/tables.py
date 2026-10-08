"""Task `wgc.tables.parse@0` (Tier 0): a segment of type `table` → a `table` record (`TAB-`), ADR-0025.

Input: one table segment. Its extracted text has table rows with cells separated by a tab; lines and cells are
`wgc.canonical.structure`, the content of the segment's `struct_hash` (ADR-0032). The first line with two or more
cells is the header. Output, with an anchor to the segment:
- `id`: `TAB-<label>` for the main rules (`role: rules`), else `TAB-<seg_prefix>:<label>` (the segment key when
  the segment has no label);
- `title`: the capitalized phrase ending in "Table" in the segment text ("Combat Results Table"), else
  `Table <label>`;
- `columns`: header cells as printed; the first column has `role: key` when its cells are numbers or ranges, the
  others then `role: value`;
- `rows`: cells as printed, except numbers and ranges: `4 or less` → `{min: null, max: 4}`, `5–6` → `{min: 5,
  max: 6}`, `7 or more` → `{min: 7, max: null}`, `3` → `3`; an empty cell is `null`;
- `complete: false` when the key column mixes ranges with cells that are not ranges (something was not parsed).
Nothing is interpreted: `No effect` stays `No effect`. Normalizing values to concepts is a Stage 1 model task.
"""
from __future__ import annotations

import re

from wgc import ids
from wgc.canonical import structure
from wgc.tasks import Inputs, TaskSpec

TASK_ID = "wgc.tables.parse"
VERSION = "0"

_NUM = r"[+-]?\d+(?:\.\d+)?"
_UP_TO = re.compile(rf"^(?:(?:≤|<=)\s*({_NUM})|({_NUM})\s*(?:or less|or lower|or fewer|or below|and less|and below|-))$",
                    re.I)
_FROM = re.compile(rf"^(?:(?:≥|>=)\s*({_NUM})|({_NUM})\s*(?:or more|or higher|or greater|or above|and more|and above|"
                   r"and up|\+))$", re.I)
_BETWEEN = re.compile(rf"^({_NUM})\s*(?:[-–—]|to)\s*({_NUM})$", re.I)
_SINGLE = re.compile(rf"^{_NUM}$")
_TITLE = re.compile(r"\b((?:[A-Z][\w'’-]*\s+)+Table)\b")


def _number(s: str) -> int | float:
    v = float(s)
    return int(v) if v.is_integer() else v


def cell(text: str):
    """A printed cell as a value of `wgc/logic@0#/$defs/cell`."""
    t = " ".join(text.split())
    if not t:
        return None
    for rx, make in ((_UP_TO, lambda a: {"min": None, "max": a}), (_FROM, lambda a: {"min": a, "max": None})):
        m = rx.match(t)
        if m:
            return make(_number(m[1] or m[2]))
    m = _BETWEEN.match(t)
    if m:
        return {"min": _number(m[1]), "max": _number(m[2])}
    if _SINGLE.match(t):
        return _number(t)
    return t


def _is_key(value) -> bool:
    return isinstance(value, (int, float, dict))


def table_id(doc: dict, seg: dict) -> str:
    prefix = doc.get("seg_prefix") or ids.parse_id(doc["id"]).key
    key = seg.get("label") or seg["id"][len(f"SEG-{prefix}."):]
    return f"TAB-{key}" if doc.get("role") == "rules" else f"TAB-{prefix}:{key}"


def parse(text: str) -> tuple[list[str], list[list]]:
    """(header cells, body rows) of the lines with two or more cells of a segment text. Reads only `structure(text)`,
    so equal `struct_hash` gives an equal result (ADR-0032)."""
    rows = [line for line in structure(text) if len(line) > 1]
    if not rows:
        return [], []
    return rows[0], [[cell(c) for c in r] for r in rows[1:]]


def _select(ws, segments: list[str]) -> list[Inputs]:
    return [(sid,) for sid in segments if (ws.segment(sid) or {}).get("segment_type") == "table"]


def _run(ws, inputs: Inputs) -> list[dict]:
    (sid,) = inputs
    seg = ws.segment(sid)
    text = ws.text(sid)
    header, rows = parse(text)
    keys = [r[0] for r in rows if r]
    key_column = bool(keys) and any(_is_key(k) for k in keys)
    columns = [{"name": name, **({"role": "key" if i == 0 else "value"} if key_column else {})}
               for i, name in enumerate(header)]
    m = _TITLE.search(" ".join(text.split()))
    title = m[1] if m else f"Table {seg.get('label') or sid}"
    record = {"kind": "table", "id": table_id(ws.document(seg["doc"]), seg), "title": title, "columns": columns,
              "rows": rows, "complete": not key_column or all(_is_key(k) for k in keys)}
    return [{"record": record, "anchors": [{"seg": sid}]}]


def _validate(ws, inputs: Inputs, proposals: list[dict]) -> list[str]:
    issues = []
    for p in proposals:
        rec = p["record"]
        n = len(rec.get("columns") or [])
        if n < 2:
            issues.append(f"{rec.get('id')}: tabela bez co najmniej dwóch kolumn; tekst segmentu {inputs[0]} nie ma "
                          "komórek rozdzielonych tabulatorem (ADR-0032).")
            continue
        if not rec.get("rows"):
            issues.append(f"{rec.get('id')}: tabela bez wierszy danych.")
        for i, row in enumerate(rec.get("rows") or [], 1):
            if len(row) != n:
                issues.append(f"{rec.get('id')}: wiersz {i} ma {len(row)} komórek, a tabela ma {n} kolumn.")
    return issues


PARSE = TaskSpec(id=TASK_ID, version=VERSION, stage="stage1", output_kind="table",
                 output_schema="wgc/logic@0#table", input_selector=_select, validate=_validate,
                 deterministic_impl=_run)
