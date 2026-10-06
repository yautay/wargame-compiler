"""PDF extractor `wgc.ingest.pdf@1` and page render (ADR-0021, segmentation rules of ADR-0020, @1: ADR-0032).

Text layer (pdfplumber/pdfminer.six): characters are grouped into lines by baseline, lines are read top to bottom
(single column). A space is inserted where the gap between two glyphs exceeds `WORD_GAP` of the font size; a gap over
`CELL_GAP` splits the line into cells (a table row).

Segmentation mirrors `wgc.ingest.markdown@1`:
- a line set in a font larger than the body size (the most frequent size) is a `heading`; consecutive heading lines
  of the same size form one heading; a leading number (`1.0 Components`) becomes its label; the level is the rank of
  the size (largest = 1);
- a line whose first word is bold and is a rule number (`3.4`) opens a numbered segment that runs to the next marker or
  heading; it is a `table` when at least two of its lines are multi-cell rows, else `rule`. A number set in the regular
  weight (a cross-reference wrapped to the start of a line) does not open a segment;
- other content outside a numbered segment is an `other` segment; unlabeled segments get keys `u1`, `u2`, …;
- the label is not part of the text; lines are joined with newlines; cells with a tab (`CELL_SEP`) in a `table`
  segment, with a space elsewhere. Lines and cells enter the segment's `struct_hash` (ADR-0032).

Generated layout fields:
- `pages`: `"3"` or `"3-4"` (1-based, first-last page with a line of the segment);
- `bbox`: `[x0, top, x1, bottom]` in points, origin at the top-left corner of the first page of the segment, union of
  its lines on that page, rounded to 0.1;
- `visual_flags` (from the text glyphs, the label excluded): `changed_color` when a glyph's fill colour differs from
  the base colour (the most frequent colour of non-space glyphs in the document; not set on headings),
  `strikethrough` when a horizontal line or thin filled rectangle crosses the middle band of a glyph (an underline at
  the baseline does not).
"""
from __future__ import annotations

import io
import re
from collections import Counter
from dataclasses import dataclass, field

from wgc.canonical import CELL_SEP
from wgc.ingest import IngestError, Segment

# @1 (ADR-0032): segments get `struct_hash`; text cached by @0 may lack the tab between table cells
NAME = "wgc.ingest.pdf@1"

WORD_GAP = 0.2      # × font size: a wider gap between two glyphs is a space
CELL_GAP = 2.0      # × font size: a wider gap between two words is a cell boundary
LINE_TOLERANCE = 0.3  # × font size: glyphs whose bottoms differ less belong to one line
HEADING_RATIO = 1.1   # a line in a font this much larger than the body size is a heading
STRIKE_BAND = (0.3, 0.7)  # fraction of glyph height (from the top) where a strike line lies
MARK_MAX_THICKNESS = 2.0  # points: a filled rectangle this thin is a line

_LABEL = re.compile(r"^(\d+(?:\.\d+)*[A-Za-z]?)\.?$")
_HEADING_LABEL = re.compile(r"^(\d+(?:\.\d+)*[A-Za-z]?)\.?[ \t]+(.+)$")
_BOLD = re.compile(r"bold|black|heavy|semibold|demi", re.I)
FLAG_ORDER = ("strikethrough", "changed_color")  # order of the contract enum


@dataclass
class _Glyph:
    text: str
    x0: float
    x1: float
    top: float
    bottom: float
    size: float
    bold: bool
    color: tuple
    struck: bool = False


@dataclass
class _Line:
    page: int
    glyphs: list[_Glyph]
    cells: list[list[_Glyph]] = field(default_factory=list)  # non-space glyphs split at wide gaps
    spaced: set[int] = field(default_factory=set)  # id() of glyphs preceded by a space glyph

    @property
    def size(self) -> float:
        return _most_common([g.size for g in self.glyphs if not g.text.isspace()]) or 0.0

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        return (min(g.x0 for g in self.glyphs), min(g.top for g in self.glyphs),
                max(g.x1 for g in self.glyphs), max(g.bottom for g in self.glyphs))


def _most_common(values):
    """Most frequent value; ties go to the smallest value (deterministic)."""
    if not values:
        return None
    counts = Counter(values)
    return min(counts, key=lambda v: (-counts[v], repr(v)))


def _rgb(color) -> tuple:
    """Fill colour as rounded RGB (0–255); pattern or unknown colour spaces stay as their repr."""
    if color is None:
        return (0, 0, 0)
    if isinstance(color, (int, float)):
        color = (color,)
    if isinstance(color, (list, tuple)) and all(isinstance(c, (int, float)) for c in color):
        if len(color) == 1:
            r = g = b = color[0]
        elif len(color) == 3:
            r, g, b = color
        elif len(color) == 4:
            c, m, y, k = color
            r, g, b = (1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k)
        else:
            return (repr(color),)
        return tuple(round(max(0.0, min(1.0, v)) * 255) for v in (r, g, b))
    return (repr(color),)


def _marks(page) -> list[tuple[float, float, float]]:
    """Horizontal strokes on the page as (x0, x1, y), y from the top."""
    out = []
    for ln in page.lines:
        if abs(ln["bottom"] - ln["top"]) <= MARK_MAX_THICKNESS:
            out.append((ln["x0"], ln["x1"], (ln["top"] + ln["bottom"]) / 2))
    for r in page.rects:
        h, w = r["bottom"] - r["top"], r["x1"] - r["x0"]
        if h <= MARK_MAX_THICKNESS and w > 2 * h:
            out.append((r["x0"], r["x1"], (r["top"] + r["bottom"]) / 2))
    return out


def _struck(g: _Glyph, marks) -> bool:
    h = g.bottom - g.top
    lo, hi = g.top + STRIKE_BAND[0] * h, g.top + STRIKE_BAND[1] * h
    mid = (g.x0 + g.x1) / 2
    return any(x0 <= mid <= x1 and lo <= y <= hi for x0, x1, y in marks)


def _page_lines(page, number: int) -> list[_Line]:
    marks = _marks(page)
    glyphs = []
    for c in page.chars:
        if not c["text"]:
            continue
        g = _Glyph(c["text"], c["x0"], c["x1"], c["top"], c["bottom"], round(c["size"], 1),
                   bool(_BOLD.search(c.get("fontname") or "")), _rgb(c.get("non_stroking_color")))
        if not g.text.isspace():
            g.struck = _struck(g, marks)
        glyphs.append(g)
    glyphs.sort(key=lambda g: (g.bottom, g.x0))
    lines: list[_Line] = []
    for g in glyphs:
        if lines and g.bottom - lines[-1].glyphs[0].bottom <= LINE_TOLERANCE * max(g.size, 1.0):
            lines[-1].glyphs.append(g)
        else:
            lines.append(_Line(number, [g]))
    for ln in lines:
        ln.glyphs.sort(key=lambda g: (g.x0, g.top))
        ln.cells = _cells(ln.glyphs)
        ln.spaced = {id(g) for prev, g in zip(ln.glyphs, ln.glyphs[1:]) if prev.text.isspace()}
    return [ln for ln in lines if ln.cells]


def _cells(glyphs: list[_Glyph]) -> list[list[_Glyph]]:
    cells: list[list[_Glyph]] = []
    prev = None
    for g in glyphs:
        if g.text.isspace():
            continue
        if prev is None or g.x0 - prev.x1 > CELL_GAP * max(g.size, prev.size):
            cells.append([])
        cells[-1].append(g)
        prev = g
    return cells


def _word_break(ln: _Line, prev: _Glyph, g: _Glyph) -> bool:
    return id(g) in ln.spaced or g.x0 - prev.x1 > WORD_GAP * max(g.size, prev.size)


def _words(ln: _Line, glyphs: list[_Glyph]) -> str:
    """Text of a run of glyphs: a space where the line has a space glyph or a gap wider than `WORD_GAP`."""
    out = []
    for i, g in enumerate(glyphs):
        if i and _word_break(ln, glyphs[i - 1], g):
            out.append(" ")
        out.append(g.text)
    return "".join(out)


def _line_text(ln: _Line, skip: int = 0, sep: str = " ") -> str:
    """Printed text of a line without its first `skip` non-space glyphs; cells joined with `sep`."""
    parts = []
    n = 0
    for cell in ln.cells:
        kept = []
        for g in cell:
            n += 1
            if n > skip:
                kept.append(g)
        if kept:
            parts.append(_words(ln, kept))
    return sep.join(parts)


def _marker(ln: _Line) -> tuple[str, int] | None:
    """(label, glyph count) when the line's first word is a bold rule number."""
    first = []
    cell = ln.cells[0]
    for i, g in enumerate(cell):
        if i and _word_break(ln, cell[i - 1], g):
            break
        first.append(g)
    if not all(g.bold for g in first):
        return None
    m = _LABEL.match("".join(g.text for g in first))
    return (m[1], len(first)) if m else None


class _Open:
    def __init__(self, key, label, segment_type, parent_key, order):
        self.key, self.label, self.segment_type = key, label, segment_type
        self.parent_key, self.order = parent_key, order
        self.lines: list[_Line] = []
        self.skips: list[int] = []
        self.glyphs: list[_Glyph] = []  # text glyphs (label excluded) for the visual flags

    def add(self, ln: _Line, skip: int = 0) -> None:
        self.lines.append(ln)
        self.skips.append(skip)
        self.glyphs += [g for cell in ln.cells for g in cell][skip:]

    def text(self, sep: str) -> str:
        texts = (_line_text(ln, skip, sep) for ln, skip in zip(self.lines, self.skips))
        return "\n".join(t for t in texts if t)


def _layout(lines: list[_Line]) -> tuple[str, tuple[float, float, float, float]]:
    pages = sorted({ln.page for ln in lines})
    first = [ln.bbox for ln in lines if ln.page == pages[0]]
    bbox = tuple(round(v, 1) for v in (min(b[0] for b in first), min(b[1] for b in first),
                                       max(b[2] for b in first), max(b[3] for b in first)))
    span = str(pages[0]) if pages[0] == pages[-1] else f"{pages[0]}-{pages[-1]}"
    return span, bbox


def _flags(glyphs: list[_Glyph], base: tuple | None) -> tuple[str, ...]:
    """Flags of the text glyphs (labels excluded); `base` None skips `changed_color` (headings)."""
    found = set()
    if any(g.struck for g in glyphs):
        found.add("strikethrough")
    if base is not None and any(g.color != base for g in glyphs):
        found.add("changed_color")
    return tuple(f for f in FLAG_ORDER if f in found)


def _open_pdf(data: bytes):
    try:
        import pdfplumber
        return pdfplumber.open(io.BytesIO(data))
    except Exception as e:  # pdfminer raises many exception types for a damaged file
        raise IngestError(f"Pliku PDF nie da się odczytać: {e}") from None


def _read_lines(data: bytes) -> list[_Line]:
    pdf = _open_pdf(data)
    try:
        lines = []
        for number, page in enumerate(pdf.pages, start=1):
            lines += _page_lines(page, number)
        return lines
    except IngestError:
        raise
    except Exception as e:
        raise IngestError(f"Pliku PDF nie da się odczytać: {e}") from None
    finally:
        pdf.close()


def extract(data: bytes) -> list[Segment]:
    lines = _read_lines(data)
    body = _most_common([g.size for ln in lines for g in ln.glyphs if not g.text.isspace()]) or 0.0
    base = _most_common([g.color for ln in lines for g in ln.glyphs if not g.text.isspace()]) or (0, 0, 0)
    heading_sizes = sorted({ln.size for ln in lines if ln.size > body * HEADING_RATIO}, reverse=True)

    out: list[Segment] = []
    seen: dict[str, int] = {}
    headings: list[tuple[int, str]] = []  # stack of (level, key)
    unlabeled = 0
    current: _Open | None = None

    def close():
        nonlocal current
        if current is not None:
            stype = current.segment_type
            if stype == "rule" and sum(1 for ln in current.lines if len(ln.cells) > 1) >= 2:
                stype = "table"
            pages, bbox = _layout(current.lines)
            # table cells are separated by a tab, other text by a space: same text_hash, own struct_hash (ADR-0032)
            text = current.text(CELL_SEP if stype == "table" else " ")
            out.append(Segment(current.key, current.label, stype, text, current.parent_key, current.order,
                               pages, bbox, _flags(current.glyphs, base)))
            current = None

    def new_key(label: str | None, ln: _Line) -> str:
        nonlocal unlabeled
        if label is None:
            unlabeled += 1
            return f"u{unlabeled}"
        if label in seen:
            raise IngestError(f"Etykieta `{label}` występuje dwukrotnie (strony {seen[label]} i {ln.page}): "
                              "segment musi mieć jednoznaczny klucz.")
        seen[label] = ln.page
        return label

    def parent() -> str | None:
        return headings[-1][1] if headings else None

    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.size in heading_sizes:
            close()
            group = [ln]
            while (i + 1 < len(lines) and lines[i + 1].size == ln.size
                   and not _HEADING_LABEL.match(_line_text(lines[i + 1]))):
                i += 1
                group.append(lines[i])
            title = " ".join(_line_text(g) for g in group)
            lm = _HEADING_LABEL.match(title)
            label, title = (lm[1], lm[2]) if lm else (None, title)
            level = heading_sizes.index(ln.size) + 1
            while headings and headings[-1][0] >= level:
                headings.pop()
            key = new_key(label, ln)
            pages, bbox = _layout(group)
            out.append(Segment(key, label, "heading", title, parent(), len(out) + 1, pages, bbox,
                               _flags([g for h in group for cell in h.cells for g in cell], None)))
            headings.append((level, key))
            i += 1
            continue
        marker = _marker(ln)
        if marker:
            close()
            label, skip = marker
            current = _Open(new_key(label, ln), label, "rule", parent(), len(out) + 1)
            current.add(ln, skip)
            i += 1
            continue
        if current is None:
            current = _Open(new_key(None, ln), None, "other", parent(), len(out) + 1)
        current.add(ln)
        i += 1
    close()
    return out


def page_count(data: bytes) -> int:
    pdf = _open_pdf(data)
    try:
        return len(pdf.pages)
    finally:
        pdf.close()


def render_page(data: bytes, page: int, scale: float = 2.0) -> bytes:
    """PNG of a 1-based page (pypdfium2; `scale` 1.0 = 72 dpi). For manual verification, never committed."""
    import pypdfium2 as pdfium
    try:
        doc = pdfium.PdfDocument(data)
    except Exception as e:
        raise IngestError(f"Pliku PDF nie da się otworzyć do renderu: {e}") from None
    try:
        if not 1 <= page <= len(doc):
            raise IngestError(f"Strona {page} jest poza dokumentem (liczba stron: {len(doc)}).")
        p = doc[page - 1]
        try:
            bitmap = p.render(scale=scale)
            buf = io.BytesIO()
            bitmap.to_pil().save(buf, format="PNG")
            return buf.getvalue()
        finally:
            p.close()
    finally:
        doc.close()
