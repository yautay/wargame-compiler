"""Markdown extractor `wgc.ingest.markdown@0`: segmentation, printed text, determinism (ADR-0020)."""
from __future__ import annotations

from pathlib import Path

import pytest

from wgc.canonical import normalize_text, text_hash
from wgc.ingest import IngestError, extractor_for, markdown

ROOT = Path(__file__).resolve().parent.parent
RULEBOOK = ROOT / "bench" / "minigame" / "rulebook.md"


@pytest.fixture(scope="module")
def bench():
    return {s.key: s for s in markdown.extract(RULEBOOK.read_bytes())}


def seg(text: str):
    return markdown.extract(text.encode("utf-8"))


def test_benchmark_segments_in_document_order(bench):
    keys = list(bench)
    assert keys[:4] == ["u1", "u2", "1.0", "1.1"]
    assert keys[-1] == "7.2"
    assert [s.order for s in bench.values()] == list(range(1, len(bench) + 1))
    numbered = [k for k, s in bench.items() if s.segment_type in ("rule", "table")]
    assert len(numbered) == 22  # every numbered paragraph 1.1–7.2 of the rulebook


def test_benchmark_types_and_parents(bench):
    assert bench["u1"].segment_type == "heading" and bench["u1"].label is None
    assert bench["u2"].segment_type == "other" and bench["u2"].parent_key == "u1"
    assert bench["3.0"].segment_type == "heading" and bench["3.0"].text == "Movement"
    assert bench["3.0"].parent_key == "u1"
    assert bench["3.4"].segment_type == "rule" and bench["3.4"].parent_key == "3.0"
    assert bench["4.3"].segment_type == "table"


def test_label_is_not_part_of_text(bench):
    assert bench["3.4"].text == "A Routed unit may not enter a hex adjacent to an enemy unit."
    assert bench["3.4"].label == "3.4"


def test_table_segment_keeps_intro_and_cells(bench):
    t = bench["4.3"].text
    assert t.startswith("Apply the modified result on the Combat Results Table:")
    assert "Modified result Effect on defender" in t and "7 or more Eliminated" in t
    assert "|" not in t and "---" not in t


def test_numbered_list_stays_in_segment(bench):
    t = bench["2.2"].text
    assert t.startswith("Each Player Turn consists of the following phases")
    assert "1. Rally Phase" in t and "4. End Phase" in t


def test_inline_markup_removed(bench):
    t = bench["u2"].text
    assert "**" not in t and "`" not in t and not t.startswith(">")
    assert "one intentional ambiguity" in normalize_text(t) and "phenomena.yaml" in t


def test_text_hash_ignores_line_wrapping_and_line_endings():
    a = seg("## 1.0 Units\n\n**1.1** A unit may move\nup to its MA.\n")
    b = seg("## 1.0 Units\r\n\r\n**1.1** A unit may move up to\r\nits MA.\r\n")
    assert [text_hash(s.text) for s in a] == [text_hash(s.text) for s in b]


def test_numbered_segment_runs_to_next_marker_or_heading():
    out = seg("## 2.0 Turn\n\n**2.1** First part.\n\nSecond paragraph of 2.1.\n\n**2.2** Next.\n\n## 3.0 Next\n")
    by = {s.key: s for s in out}
    assert "Second paragraph of 2.1." in by["2.1"].text
    assert by["2.2"].text == "Next."
    assert [s.key for s in out] == ["2.0", "2.1", "2.2", "3.0"]


def test_unlabeled_content_and_heading_levels():
    out = seg("# Title\n\nIntro text.\n\n## 1.0 Part\n\nUnnumbered note.\n\n**1.1** Rule.\n\n### Sub\n\n**1.2** Rule.\n")
    by = {s.key: s for s in out}
    assert [s.key for s in out] == ["u1", "u2", "1.0", "u3", "1.1", "u4", "1.2"]
    assert by["u3"].segment_type == "other" and by["u3"].parent_key == "1.0"
    assert by["u4"].segment_type == "heading" and by["u4"].parent_key == "1.0"
    assert by["1.2"].parent_key == "u4"
    assert by["1.0"].parent_key == "u1"


def test_bullets_fences_and_breaks():
    out = seg("**1.1** Options:\n- first\n* second\n\n---\n\n```\n**9.9** not a marker\n```\n")
    assert len(out) == 1
    t = out[0].text
    assert "first" in t and "second" in t and "- " not in t and "---" not in t and "```" not in t
    assert "9.9 not a marker" in t  # a fenced line is body text, never a marker


def test_duplicate_label_is_an_error():
    with pytest.raises(IngestError, match="dwukrotnie"):
        seg("**1.1** One.\n\n**1.1** Again.\n")


def test_invalid_utf8_is_an_error():
    with pytest.raises(IngestError, match="UTF-8"):
        markdown.extract(b"**1.1** \xff\xfe")


def test_deterministic(bench):
    again = {s.key: s for s in markdown.extract(RULEBOOK.read_bytes())}
    assert again == bench


def test_extractor_registry():
    name, fn = extractor_for("source/rules.MD")
    assert name == markdown.NAME == "wgc.ingest.markdown@0" and fn is markdown.extract
    assert extractor_for("private/rules.docx") is None
