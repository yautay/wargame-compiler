"""Markdown extractor `wgc.ingest.markdown@0` (ADR-0020).

Segmentation:
- an ATX heading (`#`…`######`) is a `heading` segment; a leading number (`1.0 Components`) becomes its label;
- a line starting with a bold rule number (`**3.4** …`) opens a numbered segment that runs to the next marker or
  heading, blank lines, lists and tables included; it is a `table` when its body contains a Markdown table, else `rule`;
- unnumbered content outside a numbered segment (a preamble, a blockquote) is an `other` segment running to the next
  marker or heading;
- the label is not part of the text; unlabeled segments get keys `u1`, `u2`, … in document order;
- `parent` is the nearest preceding heading (for a heading: the nearest preceding heading of a higher level).

Text is kept as printed: emphasis, code and link markup, blockquote and bullet markers, table pipes and the table
separator row are removed; numbered list markers (`1.`) stay. Table cells are separated by a tab (`CELL_SEP`, empty
cells kept, so columns stay aligned for `wgc.tables.parse`). `text_hash` normalizes whitespace afterwards, so the
separator does not change the hash (ADR-0024).
"""
from __future__ import annotations

import re

from wgc.ingest import IngestError, Segment

NAME = "wgc.ingest.markdown@0"
CELL_SEP = "\t"

_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
_HEADING_LABEL = re.compile(r"^(\d+(?:\.\d+)*[A-Za-z]?)\.?[ \t]+(.+)$")
_MARKER = re.compile(r"^\*\*(\d+(?:\.\d+)*[A-Za-z]?)\.?\*\*[ \t]*(.*)$")
_TABLE_ROW = re.compile(r"^[ \t]*\|.*\|[ \t]*$")
_TABLE_SEPARATOR = re.compile(r"^[ \t]*\|?[ \t]*:?-{3,}:?[ \t]*(\|[ \t]*:?-{3,}:?[ \t]*)*\|?[ \t]*$")
_BLOCKQUOTE = re.compile(r"^[ \t]*>[ \t]?")
_BULLET = re.compile(r"^([ \t]*)[-*+][ \t]+")
_FENCE = re.compile(r"^[ \t]*(```|~~~)")
_THEMATIC_BREAK = re.compile(r"^[ \t]*([-*_])([ \t]*\1){2,}[ \t]*$")

_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
_CODE = re.compile(r"`([^`]*)`")
_STRONG = re.compile(r"(\*\*|__)(.+?)\1", re.S)
_EM = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])|(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", re.S)
_ESCAPE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!|>~])")


def inline_text(s: str) -> str:
    """Inline Markdown markup removed (also across line breaks), text as printed."""
    s = _LINK.sub(r"\1", s)
    s = _CODE.sub(r"\1", s)
    s = _STRONG.sub(r"\2", s)
    s = _EM.sub(lambda m: m[1] if m[1] is not None else m[2], s)
    return _ESCAPE.sub(r"\1", s)


def _body_line(line: str) -> tuple[str | None, bool]:
    """(printed text of a body line or None to drop it, whether it is a table row)."""
    line = _BLOCKQUOTE.sub("", line)
    if _THEMATIC_BREAK.match(line):
        return None, False
    if _TABLE_SEPARATOR.match(line) and "-" in line and "|" in line:
        return None, True
    if _TABLE_ROW.match(line):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        return CELL_SEP.join(cells), True
    return _BULLET.sub(r"\1", line), False


class _Open:
    def __init__(self, key, label, segment_type, parent_key, order, first_line):
        self.key, self.label, self.segment_type = key, label, segment_type
        self.parent_key, self.order = parent_key, order
        self.lines: list[str] = [first_line] if first_line else []
        self.has_table = False


def extract(data: bytes) -> list[Segment]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        raise IngestError(f"Plik Markdown nie jest poprawnym UTF-8: {e}") from None
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    out: list[Segment] = []
    seen: dict[str, int] = {}
    headings: list[tuple[int, str]] = []  # stack of (level, key)
    unlabeled = 0
    current: _Open | None = None
    in_fence = False

    def close():
        nonlocal current
        if current is not None:
            body = inline_text("\n".join(current.lines).strip("\n"))
            stype = current.segment_type
            if stype == "rule" and current.has_table:
                stype = "table"
            out.append(Segment(current.key, current.label, stype, body, current.parent_key, current.order))
            current = None

    def new_key(label: str | None, lineno: int) -> str:
        nonlocal unlabeled
        if label is None:
            unlabeled += 1
            return f"u{unlabeled}"
        if label in seen:
            raise IngestError(f"Etykieta `{label}` występuje dwukrotnie (wiersze {seen[label]} i {lineno}): "
                              "segment musi mieć jednoznaczny klucz.")
        seen[label] = lineno
        return label

    def parent() -> str | None:
        return headings[-1][1] if headings else None

    for lineno, line in enumerate(lines, start=1):
        fence = _FENCE.match(line)
        if fence:
            in_fence = not in_fence
        heading = None if in_fence else _HEADING.match(line)
        marker = None if in_fence or heading else _MARKER.match(line)
        if heading:
            close()
            level = len(heading[1])
            title = heading[2]
            lm = _HEADING_LABEL.match(title)
            label, title = (lm[1], lm[2]) if lm else (None, title)
            while headings and headings[-1][0] >= level:
                headings.pop()
            key = new_key(label, lineno)
            out.append(Segment(key, label, "heading", inline_text(title), parent(), len(out) + 1))
            headings.append((level, key))
            continue
        if marker:
            close()
            label = marker[1]
            current = _Open(new_key(label, lineno), label, "rule", parent(), len(out) + 1, marker[2])
            continue
        printed, is_table = (None, False) if fence else _body_line(line) if not in_fence else (line, False)
        if current is None:
            if not line.strip():
                continue
            current = _Open(new_key(None, lineno), None, "other", parent(), len(out) + 1, None)
        if is_table:
            current.has_table = True
        if printed is not None:
            current.lines.append(printed)
    close()
    return out
