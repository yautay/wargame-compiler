"""Minimal PDF writer for tests: base-14 fonts (WinAnsi), fill colours, lines, filled rectangles.

Independent of the library under test (ADR-0021). Coordinates passed in are from the top-left corner of the page,
like `bbox` in the inventory; `y` of text is its baseline.
"""
from __future__ import annotations

import io
import re
import textwrap

from wgc.ingest.markdown import inline_text

FONTS = {"F1": "Courier", "F2": "Courier-Bold", "F3": "Helvetica-Bold"}
WIDTH, HEIGHT = 595, 842


def _escape(s: str) -> bytes:
    raw = s.encode("cp1252")
    return raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def _color(rgb, op: str) -> bytes:
    if isinstance(rgb, str):  # raw colour operator, e.g. "0 g" or "0 0 0 1 k"
        return rgb.encode() + b"\n"
    return b"%g %g %g %s\n" % (*rgb, op.encode())


class PdfWriter:
    def __init__(self):
        self.pages: list[bytearray] = []
        self.page()

    def page(self) -> None:
        self.pages.append(bytearray())

    def text(self, x: float, y: float, s: str, font: str = "F1", size: float = 10, color=(0, 0, 0)) -> None:
        self.pages[-1] += (b"BT " + _color(color, "rg") + b"/%s %g Tf %g %g Td (" % (font.encode(), size, x, HEIGHT - y)
                           + _escape(s) + b") Tj ET\n")

    def line(self, x0: float, x1: float, y: float, width: float = 0.8, color=(0, 0, 0)) -> None:
        self.pages[-1] += _color(color, "RG") + b"%g w %g %g m %g %g l S\n" % (width, x0, HEIGHT - y, x1, HEIGHT - y)

    def rect(self, x0: float, x1: float, y: float, height: float, color=(0, 0, 0)) -> None:
        """Filled rectangle whose vertical centre is at `y`."""
        self.pages[-1] += _color(color, "rg") + b"%g %g %g %g re f\n" % (x0, HEIGHT - y - height / 2, x1 - x0, height)

    def bytes(self) -> bytes:
        n = len(self.pages)
        fonts = b" ".join(b"/%s %d 0 R" % (k.encode(), 3 + 2 * n + i) for i, k in enumerate(FONTS))
        objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
                b"<< /Type /Pages /Kids [%s] /Count %d >>" % (b" ".join(b"%d 0 R" % (3 + i) for i in range(n)), n)]
        objs += [b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Resources << /Font << %s >> >> /Contents %d 0 R >>"
                 % (WIDTH, HEIGHT, fonts, 3 + n + i) for i in range(n)]
        objs += [b"<< /Length %d >>\nstream\n" % len(c) + bytes(c) + b"\nendstream" for c in self.pages]
        objs += [b"<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding /WinAnsiEncoding >>" % f.encode()
                 for f in FONTS.values()]
        out = io.BytesIO()
        out.write(b"%PDF-1.4\n")
        offsets = []
        for i, o in enumerate(objs, 1):
            offsets.append(out.tell())
            out.write(b"%d 0 obj\n" % i + o + b"\nendobj\n")
        xref = out.tell()
        out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1))
        out.writelines(b"%010d 00000 n \n" % o for o in offsets)
        out.write(b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref))
        return out.getvalue()


# --- Markdown → PDF (layout of a printed rulebook) ----------------------------------------------------------------

_MARKER = re.compile(r"^\*\*(\d+(?:\.\d+)*[A-Za-z]?)\.?\*\*[ \t]*", re.M)
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*)$")
HEADING_SIZES = {1: 18, 2: 13}
BODY = 9
CHAR = 0.6 * BODY  # Courier advance width
LEFT, RIGHT, TOP, BOTTOM = 50, 545, 60, 800
COLUMN = 220       # x step between table cells


def markdown_to_pdf(md: str, width_chars: int | None = None) -> bytes:
    """Lay out benchmark-style Markdown as a rulebook page: headings in Helvetica-Bold, rule numbers in Courier-Bold,
    body text in Courier rewrapped to the page width (no hyphenation), table cells in columns."""
    text = inline_text(_MARKER.sub(lambda m: f"\x00{m[1]}\x00 ", md))  # protect rule numbers from markup removal
    width = width_chars or int((RIGHT - LEFT) / CHAR)
    pdf = PdfWriter()
    y = TOP

    def advance(dy: float) -> float:
        nonlocal y
        if y + dy > BOTTOM:
            pdf.page()
            y = TOP
        y += dy
        return y

    paragraph: list[str] = []

    def flush():
        if not paragraph:
            return
        first = paragraph[0]
        label = None
        if first.startswith("\x00"):
            label, _, rest = first[1:].partition("\x00")
            paragraph[0] = rest.strip()
        for item in _items(paragraph):
            lines = textwrap.wrap(item, width - (len(label) + 1 if label else 0), break_long_words=False,
                                  break_on_hyphens=False) or [""]
            for ln in lines:
                yy = advance(BODY * 1.35)
                x = LEFT
                if label:
                    pdf.text(x, yy, label, "F2", BODY)
                    x += (len(label) + 1) * CHAR
                    label = None
                pdf.text(x, yy, ln, "F1", BODY)
        paragraph.clear()
        advance(BODY * 0.6)

    for raw in text.split("\n"):
        line = re.sub(r"^[ \t]*>[ \t]?", "", raw)
        h = _HEADING.match(line)
        if h:
            flush()
            size = HEADING_SIZES.get(len(h[1]), 11)
            pdf.text(LEFT, advance(size * 1.6), h[2].strip(), "F3", size)
            continue
        if not line.strip():
            flush()
            continue
        if line.lstrip().startswith("|"):
            if re.match(r"^[ \t|:-]+$", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            flush()
            yy = advance(BODY * 1.35)
            for i, c in enumerate(cells):
                pdf.text(LEFT + i * COLUMN, yy, c, "F1", BODY)
            continue
        paragraph.append(line.strip())
    flush()
    return pdf.bytes()


def _items(paragraph: list[str]) -> list[str]:
    """A paragraph as wrap units: numbered list items keep their own lines, other lines are joined."""
    items: list[str] = []
    for ln in paragraph:
        if re.match(r"^\d+\.\s", ln) or not items:
            items.append(ln)
        else:
            items[-1] += " " + ln
    return items
