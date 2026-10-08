"""Offline contract gold, corruption checks and separation of validation from review."""
from __future__ import annotations

import copy
import io
from pathlib import Path

import pdfplumber
import pytest

from wgc import contracts, desktop
from wgc.canonical import content_hash, sha256_hex

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "contracts/fixtures/valid"
EXAMPLE = ROOT / "bench/desktop-two-page"


@pytest.fixture
def bundle():
    return [contracts.load(VALID / f"desktop.{name}.yaml") for name in ("package", "response", "revision")]


def codes(bundle):
    return {d.code for d in desktop.check(*bundle)}


def refresh(bundle):
    p, r, v = bundle
    p["hash"] = desktop.envelope_hash(p)
    binding = {"id": p["id"], "hash": p["hash"]}
    r["package"] = copy.deepcopy(binding)
    r["document"]["package"] = copy.deepcopy(binding)
    v["package"] = copy.deepcopy(binding)
    v["response"]["hash"] = content_hash(r)
    v["document"]["hash"] = content_hash(r["document"])
    v["hash"] = desktop.envelope_hash(v)


def reviews_for(bundle):
    document = bundle[1]["document"]
    bundle[2]["reviews"] = [{"subject": item["ref"], "status": "pending"}
                            for field in ("blocks", "evidence", "relations", "coverage") for item in document[field]]


def approve(bundle, subjects=None):
    p, r, v = bundle
    for review in v["reviews"]:
        if subjects is None or review["subject"] in subjects:
            review.update(status="approved", reviewer="synthetic-test-reviewer",
                          basis={"document_hash": content_hash(r["document"]),
                                 "render_hashes": [page["render"]["hash"] for page in p["pages"]]})
    refresh(bundle)


def test_fixture_is_valid_but_not_approved(bundle):
    before = copy.deepcopy(bundle)
    assert desktop.check(*bundle) == []
    assert bundle == before  # Read-only: validation does not promote anything.
    assert bundle[2]["validation"] == "valid"
    assert bundle[2]["completeness"] == "partial"
    assert {r["status"] for r in bundle[2]["reviews"]} == {"pending"}
    assert contracts.load(VALID / "desktop.document.yaml") == bundle[1]["document"]


def test_all_manifest_bytes_and_source_layer_are_real(bundle):
    p = bundle[0]
    for asset in p["assets"]:
        assert sha256_hex((EXAMPLE / asset["path"]).read_bytes()) == asset["hash"]
    assert (EXAMPLE / "desktop.schema.json").read_bytes() == (contracts.SCHEMA_DIR / "desktop.schema.json").read_bytes()
    with pdfplumber.open(io.BytesIO((EXAMPLE / "source.pdf").read_bytes())) as pdf:
        assert len(pdf.pages) == 2
        assert len(pdf.pages[1].images) == 1
        text = "\n".join(page.extract_text() for page in pdf.pages)
        assert "NIGHT: LIMIT 1" not in text
        for page, snapshot in zip(pdf.pages, p["pages"]):
            assert sorted(c["text"] for c in page.chars) == sorted(c for f in snapshot["fragments"] for c in f["text"])
            assert [round(page.width), round(page.height)] == [snapshot["width"], snapshot["height"]]


def test_gold_columns_continuation_scope_and_image(bundle):
    p, r, _ = bundle
    d = r["document"]
    assert [page["printed_label"] for page in p["pages"]] == ["7", "8"]
    assert d["reading_order"][:7] == ["b.title", "b.setup", "b.flood", "b.flood-rule", "b.crossing", "b.crossing-start", "b.crossing-end"]
    e = {item["ref"]: item for item in d["evidence"]}
    start, areas1 = desktop.resolve_text(p, e["e.p1f5"])
    end, areas2 = desktop.resolve_text(p, e["e.p2f1"])
    assert start + " " + end == "A scout may cross the river only when the bridge is clear."
    assert [a["pdf_page"] for a in areas1 + areas2] == [1, 2]
    scope = next(x for x in d["relations"] if x["type"] == "scope")
    assert (scope["from"], scope["to"], scope["cue"]) == ("b.flood", "b.flood-rule", "frame")
    assert e["e.night"]["kind"] == "image_transcription" and e["e.night"]["text"] == "NIGHT: LIMIT 1"
    assert e["e.frame"]["kind"] == "visual_scope"


def test_split_raw_fragment_and_reordered_spans(bundle):
    p = bundle[0]
    fragment = p["pages"][0]["fragments"][4]
    split = 12
    evidence = {"kind": "text_layer", "spans": [{"fragment": fragment["ref"], "start": split, "end": len(fragment["text"])},
                                                 {"fragment": fragment["ref"], "start": 0, "end": split}]}
    text, areas = desktop.resolve_text(p, evidence)
    assert text == fragment["text"][split:] + "\n" + fragment["text"][:split]
    assert areas[0]["bbox"][0] > areas[1]["bbox"][0]
    assert areas[0]["bbox"][2] == fragment["bbox"][2]


@pytest.mark.parametrize("mutation, expected", [
    (lambda p, d: d["blocks"][0]["evidence"].clear(), "schema_error"),
    (lambda p, d: d["blocks"][0]["evidence"].append("e.missing"), "unresolved_ref"),
    (lambda p, d: d["evidence"][0]["spans"][0].update(fragment="p9f1"), "unknown_fragment"),
    (lambda p, d: d["evidence"][0]["spans"][0].update(end=10000), "text_span"),
    (lambda p, d: d["evidence"][0]["spans"].append(copy.deepcopy(d["evidence"][0]["spans"][0])), "text_overlap"),
    (lambda p, d: d["reading_order"].pop(), "reading_order"),
    (lambda p, d: d["blocks"][0].update(parent="b.setup"), "hierarchy_cycle"),
    (lambda p, d: d["relations"][0].update(to="b.crossing-start"), "continuation_order"),
    (lambda p, d: d["relations"][1].update(evidence=["e.p1f6"]), "scope_evidence"),
    (lambda p, d: d["evidence"][-2].update(bbox=[320, 140, 900, 185]), "area_bounds"),
    (lambda p, d: d["evidence"][-2]["image"].update(hash="sha256:" + "0" * 64), "asset_mismatch"),
    (lambda p, d: d["coverage"].pop(), "text_coverage"),
    (lambda p, d: d["coverage"][0]["evidence"].clear(), "schema_error"),
    (lambda p, d: d["blocks"][8]["table"]["cells"][0].update(column_span=2), "table_grid"),
    (lambda p, d: p["context_pages"].append(2), "page_scope"),
    (lambda p, d: p["pages"][0]["fragments"][0]["glyphs"][0].update(end=10000), "glyph_span"),
    (lambda p, d: p["pages"][0]["fragments"][0]["glyphs"][0].update(bbox=[1, 1, 2, 2]), "glyph_bounds"),
])
def test_corruptions_are_structural_errors(bundle, mutation, expected):
    mutation(bundle[0], bundle[1]["document"])
    refresh(bundle)
    assert "desktop_" + expected in codes(bundle)


def test_context_does_not_grant_output_ownership(bundle):
    p = bundle[0]
    p.update(target_pages=[1], context_pages=[2])
    refresh(bundle)
    assert "desktop_context_write" in codes(bundle)


def test_manifest_and_foreign_response(bundle):
    p, r, _ = bundle
    p["instructions"]["version"] = "changed"
    assert "desktop_manifest_hash" in codes(bundle)
    refresh(bundle)
    r = contracts.load(ROOT / "contracts/fixtures/desktop-invalid/foreign-package.yaml")
    assert contracts.errors(r) == []
    assert "desktop_package_mismatch" in {d.code for d in desktop.check(p, r)}


@pytest.mark.parametrize("unapproved", ["pending", "stale", "rejected"])
def test_complete_requires_review_of_all_evidence(bundle, unapproved):
    bundle[2]["completeness"] = "complete"
    refresh(bundle)
    assert "desktop_incomplete" in codes(bundle)
    approve(bundle)
    assert codes(bundle) == set()
    image = next(r for r in bundle[2]["reviews"] if r["subject"] == "e.night")
    image["status"] = unapproved
    refresh(bundle)
    assert {"desktop_incomplete", "desktop_review_dependency"} <= codes(bundle)


def test_review_is_bound_to_artifact_and_render(bundle):
    approve(bundle)
    bundle[2]["reviews"][0]["basis"]["render_hashes"] = ["sha256:" + "0" * 64]
    refresh(bundle)
    assert "desktop_review_basis" in codes(bundle)
    bundle[2]["validation"] = "unchecked"
    refresh(bundle)
    assert "desktop_review_validation" in codes(bundle)


def test_explicit_gap_preserves_independent_approved_fragment(bundle):
    d = bundle[1]["document"]
    d["coverage"].append({"ref": "c.uncertain", "pdf_page": 1, "bbox": [310, 115, 550, 140], "classification": "gap",
                          "evidence": [], "blocks": [], "reason": "Continuation needs visual review.", "affects": ["b.crossing-start"]})
    reviews_for(bundle)
    approve(bundle, {"b.title", "e.p1f1", "c.b.title"})
    assert codes(bundle) == set()
    approve(bundle, {"b.crossing-start"})
    assert "desktop_review_dependency" in codes(bundle)
    approve(bundle)
    assert "desktop_review_gap" in codes(bundle)


def test_declared_text_gap_is_structurally_accounted_for(bundle):
    d = bundle[1]["document"]
    footer = d["coverage"][-1]
    footer.update(classification="gap", reason="Printed label uncertain.", affects=[])
    refresh(bundle)
    assert codes(bundle) == set()


def test_semantically_wrong_but_well_formed_response_stays_pending(bundle):
    d = bundle[1]["document"]
    d["reading_order"][1], d["reading_order"][4] = d["reading_order"][4], d["reading_order"][1]
    next(e for e in d["evidence"] if e["ref"] == "e.night")["text"] = "NIGHT: LIMIT 9"
    refresh(bundle)
    assert codes(bundle) == set()  # Neither column meaning nor OCR truth is proved by schema.
    assert all(r["status"] == "pending" for r in bundle[2]["reviews"])


def test_revision_hash_and_pointers_are_checked(bundle):
    bundle[2]["document"]["hash"] = "sha256:" + "0" * 64
    assert {"desktop_revision_hash", "desktop_revision_mismatch"} <= codes(bundle)


def test_one_row_table_and_merged_cell_are_representable(bundle):
    table = bundle[1]["document"]["blocks"][8]["table"]
    table.update(rows=1, columns=4)
    for i, cell in enumerate(table["cells"]):
        cell.update(row=0, column=i)
    refresh(bundle)
    assert codes(bundle) == set()
    table["cells"] = [{"row": 0, "column": 0, "row_span": 1, "column_span": 4, "role": "data",
                       "evidence": [f"e.p2f{i}" for i in range(3, 7)]}]
    refresh(bundle)
    assert codes(bundle) == set()


def test_revision_parent_requires_explicit_change_map(bundle):
    v = bundle[2]
    v["parent"] = {"id": "rev.fixture.0", "hash": "sha256:" + "0" * 64}
    refresh(bundle)
    assert "desktop_schema_error" in codes(bundle)
    v["changes"] = [{"before": ["b.previous-sign"], "after": ["b.night-sign"], "reason": "Explicit split mapping."}]
    refresh(bundle)
    assert codes(bundle) == set()
    v["changes"][0]["after"] = ["b.missing"]
    refresh(bundle)
    assert "desktop_change_map" in codes(bundle)


@pytest.mark.parametrize("bad", [None, [], {"schema": "unknown"}, {"schema": "wgc/desktop@0", "kind": "response"}])
def test_bad_envelopes_produce_diagnostics(bundle, bad):
    assert "desktop_schema_error" in {d.code for d in desktop.check(bad, bundle[1])}
