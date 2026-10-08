"""Offline hybrid PDF proposal checks using only PDFs generated in this test suite."""
from __future__ import annotations

import copy
import json

import pytest

from pdfgen import PdfWriter
from wgc import source
from wgc.ingest import IngestError, pdf_hybrid


def synthetic_pdf():
    writer = PdfWriter()
    writer.text(40, 60, "1. Setup", "F2", 12)
    writer.text(40, 95, "1. Place units", "F1", 10)
    writer.text(40, 112, "2. Draw cards", "F1", 10)
    writer.text(320, 95, "2. Movement", "F2", 12)
    writer.text(320, 112, "Move one hex.", "F1", 10)
    writer.text(40, 800, "1", "F1", 9)
    writer.page()
    writer.text(40, 65, "Continued instructions.", "F1", 10)
    writer.text(40, 100, "Terrain", "F1", 10)
    writer.text(260, 100, "Cost", "F1", 10)
    writer.text(40, 118, "Forest", "F1", 10)
    writer.text(260, 118, "2", "F1", 10)
    writer.text(40, 800, "2", "F1", 9)
    return writer.bytes()


def area(packet, words):
    boxes = [w["bbox"] for w in words]
    return {"page": packet["page"], "bbox": [min(b[0] for b in boxes), min(b[1] for b in boxes),
                                                   max(b[2] for b in boxes), max(b[3] for b in boxes)],
            "word_ids": [w["id"] for w in words]}


def segment(packet, words, kind="other", **extra):
    return {"type": kind, "text": " ".join(w["text"] for w in words), "areas": [area(packet, words)], **extra}


def proposals(data):
    first, second = pdf_hybrid.pages(data)
    def selected(p, x0, y0, y1):
        return [w for w in p["words"] if w["bbox"][0] >= x0 and y0 <= w["bbox"][1] < y1]
    left = [w for w in selected(first, 0, 70, 130) if w["bbox"][0] < 200]
    right = selected(first, 300, 70, 130)
    title = selected(first, 0, 0, 70)
    footer1 = selected(first, 0, 780, 840)
    cont = selected(second, 0, 0, 80)
    footer2 = selected(second, 0, 780, 840)
    table_words = selected(second, 0, 85, 140)
    rows = []
    for y0, y1 in ((85, 105), (105, 140)):
        cells = []
        for x0, x1 in ((0, 200), (200, 500)):
            words = [w for w in table_words if y0 <= w["bbox"][1] < y1 and x0 <= w["bbox"][0] < x1]
            cells.append({"text": " ".join(w["text"] for w in words), "areas": [area(second, words)]})
        rows.append(cells)
    table_text = "\n".join("\t".join(c["text"] for c in row) for row in rows)
    p1 = {"segments": [segment(first, title, "heading", label="1"),
                       segment(first, left, "list_item"), segment(first, right, "rule", label="2")],
          "exclusions": [{"word_ids": [w["id"] for w in footer1], "reason": "pagination"}],
          "unresolved": [], "image_only": []}
    p2 = {"segments": [segment(second, cont, "rule", continues_previous=True),
                       {"type": "table", "text": table_text, "areas": [area(second, table_words)], "rows": rows}],
          "exclusions": [{"word_ids": [w["id"] for w in footer2], "reason": "pagination"}],
          "unresolved": [], "image_only": []}
    return first, second, p1, p2


class Fake:
    def __init__(self, proposals):
        self.proposals = proposals
        self.calls = []

    def propose(self, packet, png, retry, issues):
        assert png.startswith(b"\x89PNG")
        self.calls.append((packet["page"], retry, issues))
        return {"proposal": copy.deepcopy(self.proposals[packet["page"] - 1]),
                "usage": {"input_tokens": 10, "output_tokens": 5, "cost_usd": .001}}


def test_hybrid_columns_lists_table_continuation_and_paginas():
    data = synthetic_pdf()
    p1_packet, p2_packet, p1, p2 = proposals(data)
    assert pdf_hybrid.check_page(p1_packet, p1) == []
    assert pdf_hybrid.check_page(p2_packet, p2) == []
    result = pdf_hybrid.run(data, Fake([p1, p2]))
    assert result.report["review_pages"] == []
    assert result.report["input_tokens"] == 20 and result.report["cost_usd"] == .002
    assert [s.segment_type for s in result.segments] == ["heading", "list_item", "rule", "table"]
    assert result.segments[1].text.startswith("1.") and "2." in result.segments[1].text
    assert result.segments[2].pages == "1-2" and {a["page"] for a in result.segments[2].areas} == {1, 2}
    assert "\t" in result.segments[3].text
    assert all("800" not in s.text for s in result.segments)
    assert pdf_hybrid.load_approved(data, result.approved) == result.segments


def test_repeated_printed_label_does_not_collide():
    writer = PdfWriter()
    writer.text(40, 80, "1. First item", "F1", 10)
    writer.page()
    writer.text(40, 80, "1. Second item", "F1", 10)
    data = writer.bytes()
    first, second = pdf_hybrid.pages(data)
    p1 = {"segments": [segment(first, first["words"], "list_item", label="1")],
          "exclusions": [], "unresolved": [], "image_only": []}
    p2 = {"segments": [segment(second, second["words"], "list_item", label="1")],
          "exclusions": [], "unresolved": [], "image_only": []}
    result = pdf_hybrid.run(data, Fake([p1, p2]))
    assert result.report["review_pages"] == []
    assert len({s.key for s in result.segments}) == 2
    assert [s.label for s in result.segments] == ["1", "1"]


@pytest.mark.parametrize("mutation,expected", [
    (lambda p: p["segments"][0]["areas"][0]["word_ids"].append(p["segments"][0]["areas"][0]["word_ids"][0]), "duplicate_word"),
    (lambda p: p["segments"][0]["areas"][0]["word_ids"].pop(), "uncovered_word"),
    (lambda p: p["segments"][0].update(text="Invented text"), "text_mismatch"),
    (lambda p: p["segments"][0]["areas"][0].update(bbox=[-1, 0, 5, 5]), "area_out_of_bounds"),
    (lambda p: p["exclusions"][0].update(reason=""), "exclusion_without_reason"),
    (lambda p: p["image_only"].append({"bbox": [0, 0, 20, 20], "description": "word in image"}), "image_only_requires_review"),
])
def test_rejects_uncertain_or_inconsistent_page(mutation, expected):
    packet, _, p1, _ = proposals(synthetic_pdf())
    mutation(p1)
    assert any(i.startswith(expected) for i in pdf_hybrid.check_page(packet, p1))


def test_table_cells_must_cover_segment_words():
    _, packet, _, p2 = proposals(synthetic_pdf())
    p2["segments"][1]["rows"][0][0]["areas"][0]["word_ids"].pop()
    assert "table_cell_coverage:1" in pdf_hybrid.check_page(packet, p2)


def test_single_row_catalog_is_not_accepted_as_table():
    _, packet, _, p2 = proposals(synthetic_pdf())
    p2["segments"][1]["rows"] = p2["segments"][1]["rows"][:1]
    assert "table_needs_review:1" in pdf_hybrid.check_page(packet, p2)


def test_ragged_table_requires_review():
    _, packet, _, p2 = proposals(synthetic_pdf())
    p2["segments"][1]["rows"][1].pop()
    assert "ragged_table:1" in pdf_hybrid.check_page(packet, p2)


def test_pagination_must_be_excluded_and_regions_need_details():
    packet, _, proposal, _ = proposals(synthetic_pdf())
    footer_id = proposal["exclusions"].pop()["word_ids"][0]
    footer = next(w for w in packet["words"] if w["id"] == footer_id)
    proposal["segments"].append(segment(packet, [footer]))
    assert any(i.startswith("pagination_in_segment") for i in pdf_hybrid.check_page(packet, proposal))
    proposal["segments"].pop()
    proposal["exclusions"].append({"word_ids": [footer_id], "reason": "pagination"})
    proposal["exclusions"][0]["reason"] = "decoration"
    assert any(i.startswith("pagination_reason") for i in pdf_hybrid.check_page(packet, proposal))
    proposal["exclusions"][0]["reason"] = "pagination"
    proposal["unresolved"] = [{"bbox": [0, 0, 10, 10], "reason": ""}]
    assert "invalid_unresolved_region" in pdf_hybrid.check_page(packet, proposal)
    proposal["unresolved"] = []
    packet["unmapped_glyphs"] = 1
    assert "unmapped_text_glyphs:1" in pdf_hybrid.check_page(packet, proposal)


def test_one_retry_then_review_and_no_text_layer():
    data = synthetic_pdf()
    _, _, p1, p2 = proposals(data)
    p1["segments"][0]["text"] = "wrong"
    fake = Fake([p1, p2])
    result = pdf_hybrid.run(data, fake)
    assert result.approved is None and result.report["review_pages"] == [1]
    assert [c[:2] for c in fake.calls] == [(1, 0), (1, 1), (2, 0)]
    writer = PdfWriter()
    blank = pdf_hybrid.run(writer.bytes(), fake)
    assert blank.report["pages"][0]["issues"] == ["no_text_layer"]


def test_review_keeps_explicit_hybrid_mode_without_approved_segments(tmp_path):
    data = synthetic_pdf()
    _, _, p1, p2 = proposals(data)
    p1["segments"][0]["text"] = "wrong"
    root = tmp_path / "game"
    (root / "private").mkdir(parents=True)
    (root / "private" / "rules.pdf").write_bytes(data)
    source.init(root, "tst", [("rules", "private/rules.pdf")])
    with pytest.raises(source.SourceError, match="przeglądu"):
        source.hybrid(root, "SRC-tst.rules", Fake([p1, p2]))
    inv = source.read_inventory(root)
    assert inv.documents[0]["extractor"] == pdf_hybrid.NAME and inv.segments == []
    report = source.verify(root)
    assert {d.code for d in report.errors} == {"extract_error"}


def test_replay_inventory_verify_is_offline_and_bound_to_pdf(tmp_path):
    data = synthetic_pdf()
    _, _, p1, p2 = proposals(data)
    root = tmp_path / "game"
    (root / "private").mkdir(parents=True)
    (root / "private" / "rules.pdf").write_bytes(data)
    source.init(root, "tst", [("rules", "private/rules.pdf")])
    source.hybrid_prepare(root, "SRC-tst.rules")
    prepared = root / ".glu/source/SRC-tst.rules/hybrid/prepared"
    assert (prepared / "p001.png").is_file() and (prepared / "p002.json").is_file()
    replay = root / ".glu" / "replay"
    replay.mkdir(parents=True)
    for number, proposal in enumerate((p1, p2), 1):
        (replay / f"p{number:03d}.json").write_text(json.dumps({"proposal": proposal}), encoding="utf-8")
    source.hybrid(root, "SRC-tst.rules", pdf_hybrid.ReplayProvider(replay))
    inv = source.read_inventory(root)
    assert inv.documents[0]["extractor"] == pdf_hybrid.NAME
    assert len(inv.segments[2]["areas"]) == 2
    assert source.verify(root).ok
    source.scan(root)
    source.extract(root)  # saved approved evidence; no provider call
    assert source.read_inventory(root).documents[0]["extractor"] == pdf_hybrid.NAME
    assert source.verify(root).ok
    artifact = root / ".glu/source/SRC-tst.rules/hybrid/approved.json"
    saved = json.loads(artifact.read_text(encoding="utf-8"))
    saved["pages"][0]["proposal"]["segments"][0]["text"] = "tampered"
    artifact.write_text(json.dumps(saved), encoding="utf-8")
    assert "extract_error" in {d.code for d in source.verify(root).errors}
    with pytest.raises(IngestError):
        pdf_hybrid.load_approved(data + b"changed", saved)
