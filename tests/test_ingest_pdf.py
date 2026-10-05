"""PDF extractor `wgc.ingest.pdf@0`: parity with Markdown, layout fields, visual flags, render (ADR-0021).

Every PDF is generated in the test (`tests/pdfgen.py`) from self-authored text: no network, no publisher files.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from pdfgen import CHAR, LEFT, PdfWriter, markdown_to_pdf
from wgc import source
from wgc.__main__ import main
from wgc.canonical import text_hash
from wgc.ingest import IngestError, extractor_for, markdown, pdf

ROOT = Path(__file__).resolve().parent.parent
RULEBOOK = ROOT / "bench" / "minigame" / "rulebook.md"
BENCH_INVENTORY = ROOT / "bench" / "minigame" / "source" / "inventory.yaml"


@pytest.fixture(scope="module")
def rulebook_pdf() -> bytes:
    return markdown_to_pdf(RULEBOOK.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def bench(rulebook_pdf):
    return {s.key: s for s in pdf.extract(rulebook_pdf)}


def rule_line(w: PdfWriter, y: float, label: str | None, text: str, **kw) -> float:
    """A body line at baseline `y`: optional bold rule number, then regular text; returns the x where text starts."""
    x = LEFT
    if label:
        w.text(x, y, label, "F2", 9, **kw)
        x += (len(label) + 1) * CHAR
    w.text(x, y, text, "F1", 9, **kw)
    return x


# --- Markdown ↔ PDF parity ------------------------------------------------------------------------------------------

def test_registry_maps_pdf():
    assert extractor_for("private/Rules.PDF")[0] == pdf.NAME == "wgc.ingest.pdf@0"


def test_same_text_in_markdown_and_pdf_gives_same_rule_hashes(bench):
    md = {s.key: s for s in markdown.extract(RULEBOOK.read_bytes())}
    assert list(bench) == list(md)
    rules = [k for k, s in md.items() if s.segment_type == "rule"]
    assert len(rules) == 21
    for k in rules:
        assert text_hash(bench[k].text) == text_hash(md[k].text), k
    for k, s in md.items():  # headings, preamble and the table too, with the same structure
        b = bench[k]
        assert (b.label, b.segment_type, b.parent_key, b.order) == (s.label, s.segment_type, s.parent_key, s.order), k
        assert text_hash(b.text) == text_hash(s.text), k


def test_pdf_hashes_match_committed_markdown_inventory(bench):
    from wgc.validate import load_documents
    inv = {r["id"]: r for d in load_documents(BENCH_INVENTORY) for r in d["records"] if r["kind"] == "segment"}
    for k, s in bench.items():
        assert inv[f"SEG-dsk.{k}"]["text_hash"] == text_hash(s.text), k


def test_parity_does_not_depend_on_line_wrapping():
    text = RULEBOOK.read_text(encoding="utf-8")
    wide = {s.key: text_hash(s.text) for s in pdf.extract(markdown_to_pdf(text))}
    narrow = {s.key: text_hash(s.text) for s in pdf.extract(markdown_to_pdf(text, width_chars=47))}
    assert narrow == wide


def test_label_is_not_part_of_text_and_list_numbers_stay(bench):
    assert bench["3.4"].text == "A Routed unit may not enter a hex adjacent to an enemy unit."
    assert bench["3.4"].label == "3.4"
    assert "\n1. Rally Phase\n2. Movement Phase" in bench["2.2"].text
    assert "1" not in bench and "4" not in bench
    assert bench["4.3"].segment_type == "table" and "5–6\tRouted" in bench["4.3"].text
    assert "\t" not in bench["3.4"].text  # only table rows use the cell separator


def test_headings_levels_and_parents(bench):
    assert bench["u1"].segment_type == "heading" and bench["u1"].text == "Drill Skirmish: benchmark rulebook"
    assert bench["u2"].segment_type == "other" and bench["u2"].parent_key == "u1"
    assert bench["3.0"].segment_type == "heading" and bench["3.0"].text == "Movement"
    assert bench["3.0"].parent_key == "u1" and bench["3.4"].parent_key == "3.0"


def test_regular_weight_number_at_line_start_does_not_open_segment():
    w = PdfWriter()
    rule_line(w, 100, "3.5", "Light units are not required to stop under")
    rule_line(w, 112, None, "3.3. They remain subject to")
    rule_line(w, 124, None, "3.4. They may move.")
    rule_line(w, 140, "3.6", "A hex may never contain more than one unit.")
    segs = pdf.extract(w.bytes())
    assert [s.key for s in segs] == ["3.5", "3.6"]
    assert segs[0].text == ("Light units are not required to stop under\n3.3. They remain subject to\n"
                            "3.4. They may move.")


def test_hyphenated_line_break_is_joined_by_text_hash():
    w = PdfWriter()
    rule_line(w, 100, "3.1", "A unit may spend its MA during the move-")
    rule_line(w, 112, None, "ment phase.")
    (seg,) = pdf.extract(w.bytes())
    assert text_hash(seg.text) == text_hash("A unit may spend its MA during the movement phase.")


def test_duplicate_label_is_an_error():
    w = PdfWriter()
    rule_line(w, 100, "1.1", "First.")
    rule_line(w, 112, "1.1", "Again.")
    with pytest.raises(IngestError, match="1.1"):
        pdf.extract(w.bytes())


def test_damaged_file_is_an_ingest_error():
    with pytest.raises(IngestError, match="PDF"):
        pdf.extract(b"not a pdf at all")


def test_extract_is_deterministic(rulebook_pdf, bench):
    assert {s.key: s for s in pdf.extract(rulebook_pdf)} == bench


# --- layout fields ------------------------------------------------------------------------------------------------

def test_pages_and_bbox(bench):
    assert bench["1.1"].pages == "1" and bench["7.2"].pages == "2"
    x0, top, x1, bottom = bench["3.4"].bbox
    assert x0 == LEFT and top < bottom and x1 > x0
    assert all(v == round(v, 1) for v in bench["3.4"].bbox)
    assert bench["3.4"].bbox[1] > bench["3.3"].bbox[3]  # reading order top to bottom
    assert bench["3.4"].visual_flags == ()


def test_segment_spanning_pages_has_page_range_and_bbox_on_first_page():
    w = PdfWriter()
    rule_line(w, 780, "2.1", "A game lasts six Game Turns.")
    w.page()
    rule_line(w, 70, None, "Each Game Turn has two Player Turns.")
    rule_line(w, 90, "2.2", "Phases follow.")
    s21, s22 = pdf.extract(w.bytes())
    assert (s21.pages, s22.pages) == ("1-2", "2")
    assert s21.bbox[1] > 700 and s21.bbox[3] < 800
    assert s21.text == "A game lasts six Game Turns.\nEach Game Turn has two Player Turns."


# --- visual flags -------------------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def flagged():
    w = PdfWriter()
    rule_line(w, 100, "1.1", "Plain text in gray-space black.", color="0 g")
    rule_line(w, 115, "1.2", "Plain text in CMYK black.", color="0 0 0 1 k")
    x = rule_line(w, 130, "1.3", "A unit may move ")
    w.text(x + 16 * CHAR, 130, "two hexes.", "F1", 9, color=(0.8, 0, 0))
    x = rule_line(w, 145, "1.4", "This sentence is struck through.")
    w.line(x, x + 32 * CHAR, 145 - 2.7)
    x = rule_line(w, 160, "1.5", "This sentence is underlined.")
    w.line(x, x + 28 * CHAR, 160 + 1.5)
    x = rule_line(w, 175, "1.6", "Struck with a thin filled rectangle.")
    w.rect(x, x + 36 * CHAR, 175 - 2.7, 0.8)
    x = rule_line(w, 190, "1.7", "Deleted in red.", color=(1, 0, 0))
    w.line(x, x + 15 * CHAR, 190 - 2.7, color=(1, 0, 0))
    w.text(LEFT, 200, "1.8", "F2", 9, color=(0, 0, 0.7))  # a coloured rule number is not changed text
    w.text(LEFT + 4 * CHAR, 200, "Black text after a blue number.", "F1", 9)
    w.text(LEFT, 210, "1.9", "F2", 9)
    w.line(LEFT, LEFT + 3 * CHAR, 210 - 2.7)  # nor is a struck-out number
    w.text(LEFT + 4 * CHAR, 210, "Black text after a struck number.", "F1", 9)
    for i, y in enumerate(range(225, 285, 15)):  # body text sets the base colour (black)
        rule_line(w, y, f"2.{i + 1}", "Ordinary black text of the base colour.")
    return {s.key: s for s in pdf.extract(w.bytes())}


def test_visual_flags(flagged):
    assert flagged["1.1"].visual_flags == ()
    assert flagged["1.2"].visual_flags == ()  # Gray, RGB and CMYK black are one colour
    assert flagged["1.3"].visual_flags == ("changed_color",)
    assert flagged["1.4"].visual_flags == ("strikethrough",)
    assert flagged["1.5"].visual_flags == ()  # an underline is not a strike
    assert flagged["1.6"].visual_flags == ("strikethrough",)
    assert flagged["1.7"].visual_flags == ("strikethrough", "changed_color")
    assert flagged["1.8"].visual_flags == ()  # flags come from the text, not the label
    assert flagged["1.9"].visual_flags == ()
    assert flagged["2.1"].visual_flags == ()


def test_coloured_heading_is_not_changed_text():
    w = PdfWriter()
    w.text(LEFT, 80, "1.0 Units", "F3", 13, color=(0, 0, 0.7))
    for i, y in enumerate(range(100, 160, 15)):
        rule_line(w, y, f"1.{i + 1}", "Ordinary black text of the base colour.")
    segs = {s.key: s for s in pdf.extract(w.bytes())}
    assert segs["1.0"].segment_type == "heading" and segs["1.0"].visual_flags == ()
    assert segs["1.1"].parent_key == "1.0"


def test_struck_text_stays_in_segment_text(flagged):
    assert flagged["1.4"].text == "This sentence is struck through."
    assert flagged["1.3"].text == "A unit may move two hexes."


# --- inventory and render -----------------------------------------------------------------------------------------

def make_pdf_game(tmp_path: Path, data: bytes) -> Path:
    root = tmp_path / "game"
    (root / "private").mkdir(parents=True)
    (root / "private" / "rules.pdf").write_bytes(data)
    source.init(root, "tst", [("rules", "private/rules.pdf")])
    source.extract(root)
    return root


def test_extract_pdf_writes_layout_fields(tmp_path, rulebook_pdf):
    root = make_pdf_game(tmp_path, rulebook_pdf)
    inv = source.read_inventory(root)
    assert inv.documents[0]["extractor"] == pdf.NAME
    segs = {s["id"]: s for s in inv.segments}
    assert segs["SEG-tst.3.4"]["pages"] == "1" and len(segs["SEG-tst.3.4"]["bbox"]) == 4
    assert "visual_flags" not in segs["SEG-tst.3.4"]  # written only when non-empty
    assert source.verify(root).ok
    assert (root / ".glu" / "source" / "SRC-tst.rules" / "SEG-tst.3.4.txt").is_file()


def test_extract_pdf_writes_flags_and_keeps_verified_by_render(tmp_path):
    w = PdfWriter()
    rule_line(w, 100, "1.1", "Deleted rule.")
    w.line(LEFT + 4 * CHAR, LEFT + 17 * CHAR, 100 - 2.7)
    for i, y in enumerate(range(115, 175, 15)):
        rule_line(w, y, f"1.{i + 2}", "Ordinary text.")
    root = make_pdf_game(tmp_path, w.bytes())
    inv = source.read_inventory(root)
    seg = next(s for s in inv.segments if s["id"] == "SEG-tst.1.1")
    assert seg["visual_flags"] == ["strikethrough"]
    seg["verified_by_render"] = True
    source.write_inventory(root, inv)
    source.extract(root)
    seg = next(s for s in source.read_inventory(root).segments if s["id"] == "SEG-tst.1.1")
    assert seg["verified_by_render"] is True and seg["visual_flags"] == ["strikethrough"]


def test_render_segment_pages_and_whole_document(tmp_path, rulebook_pdf):
    root = make_pdf_game(tmp_path, rulebook_pdf)
    pages = root / ".glu" / "source" / "SRC-tst.rules" / "pages"
    msgs = source.render(root, segment="SEG-tst.7.2", scale=0.5)
    assert len(msgs) == 1 and (pages / "p002.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert not (pages / "p001.png").exists()
    source.render(root, doc_id="SRC-tst.rules", scale=0.5)
    assert sorted(p.name for p in pages.iterdir()) == ["p001.png", "p002.png"]
    source.extract(root)  # refreshing the text cache keeps the renders
    assert (pages / "p001.png").is_file()


def test_render_errors(tmp_path, rulebook_pdf):
    root = make_pdf_game(tmp_path, rulebook_pdf)
    with pytest.raises(source.SourceError, match="--doc"):
        source.render(root)
    with pytest.raises(source.SourceError, match="SEG-tst.9.9"):
        source.render(root, segment="SEG-tst.9.9")
    with pytest.raises(source.SourceError, match="zakres"):
        source.render(root, doc_id="SRC-tst.rules", pages="2-1")
    with pytest.raises(source.SourceError, match="Strona 5 jest poza dokumentem"):
        source.render(root, doc_id="SRC-tst.rules", pages="5", scale=0.5)
    md_root = tmp_path / "md"
    (md_root / "private").mkdir(parents=True)
    (md_root / "private" / "rules.md").write_text("**1.1** Text.\n", encoding="utf-8")
    source.init(md_root, "tst", [("rules", "private/rules.md")])
    with pytest.raises(source.SourceError, match="tylko PDF"):
        source.render(md_root, doc_id="SRC-tst.rules")


def test_parse_pages():
    assert source.parse_pages("3") == [3]
    assert source.parse_pages("1,3-4") == [1, 3, 4]
    with pytest.raises(source.SourceError):
        source.parse_pages("x")


def test_cli_render(tmp_path, rulebook_pdf, capsys):
    root = make_pdf_game(tmp_path, rulebook_pdf)
    assert main(["source", "render", "--root", str(root), "--segment", "SEG-tst.1.1", "--scale", "0.5"]) == 0
    assert "strona 1" in capsys.readouterr().out
    assert main(["source", "render", "--root", str(root), "--doc", "SRC-tst.nope"]) == 2
    assert "SRC-tst.nope" in capsys.readouterr().err
