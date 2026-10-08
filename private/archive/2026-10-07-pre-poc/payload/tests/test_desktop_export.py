"""Offline export checks. Synthetic responses below are not desktop trials."""
from __future__ import annotations

import copy
import io
import json
from pathlib import Path
from types import SimpleNamespace

import pdfplumber
import pytest

from pdfgen import PdfWriter
from wgc import contracts, desktop, source
from wgc.__main__ import main
from wgc.canonical import sha256_hex
from wgc.desktop_export import ExportError, export_package, parse_pages, verify_files
from wgc.ingest import IngestError, pdf

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "bench/desktop-two-page/source.pdf"


def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def exported(tmp_path, **kwargs):
    return export_package(EXAMPLE, tmp_path / "packet", doc="SRC-desktop.rules", target_pages=[1, 2], **kwargs)


def excluded_response(package):
    """Account for synthetic target text without interpreting it; no review."""
    binding = {"id": package["id"], "hash": package["hash"]}
    evidence, coverage = [], []
    for page in package["pages"]:
        if page["pdf_page"] not in package["target_pages"]:
            continue
        for fragment in page["fragments"]:
            ref = "e." + fragment["ref"]
            evidence.append({"ref": ref, "kind": "text_layer", "spans": [
                {"fragment": fragment["ref"], "start": 0, "end": len(fragment["text"])}]})
            coverage.append({"ref": "c." + fragment["ref"], "pdf_page": page["pdf_page"], "bbox": fragment["bbox"],
                             "classification": "excluded", "evidence": [ref], "blocks": [], "reason": "Synthetic test only."})
    return {"schema": "wgc/desktop@0", "kind": "response", "package": binding,
            "producer": {"application": "unknown", "model": "unknown", "model_identity": "unknown"},
            "document": {"schema": "wgc/desktop@0", "kind": "document", "package": binding,
                         "source": package["source"], "blocks": [], "reading_order": [], "relations": [],
                         "evidence": evidence, "coverage": coverage}}


def test_repeat_export_has_identical_bytes_independent_of_path_and_page_order(tmp_path):
    first = exported(tmp_path)
    second = export_package(EXAMPLE, tmp_path / "other", doc="SRC-desktop.rules", target_pages=[2, 1, 2])
    assert first == second
    assert files(tmp_path / "packet") == files(tmp_path / "other")
    assert json.loads((tmp_path / "packet/manifest.txt").read_text("utf-8")) == first
    assert first["hash"] == desktop.envelope_hash(first)
    assert contracts.errors(first) == []
    assert first["source"]["file_hash"] == sha256_hex(EXAMPLE.read_bytes())
    assert all(page["printed_label"] is None for page in first["pages"])


def test_asset_hashes_schema_and_instructions_are_real(tmp_path):
    package = exported(tmp_path)
    root = tmp_path / "packet"
    verify_files(package, root)
    assert {a["path"] for a in package["assets"]} == set(files(root)) - {"manifest.txt"}
    assert (root / "desktop.schema.json").read_bytes() == (contracts.SCHEMA_DIR / "desktop.schema.json").read_bytes()
    assert package["instructions"]["version"] in (root / "instructions.txt").read_text("utf-8")
    assert contracts.errors(json.loads((root / "example.txt").read_text("utf-8"))) == []
    for asset in package["assets"]:
        assert sha256_hex((root / asset["path"]).read_bytes()) == asset["hash"]
    (root / "p001.png").write_bytes(b"corrupt")
    with pytest.raises(ExportError, match="hash pliku p001.png"):
        verify_files(package, root)
    package["target_pages"] = [1]
    with pytest.raises(ExportError, match="Hash manifestu"):
        verify_files(package, root)


def test_own_gold_response_still_binds_to_general_export(tmp_path):
    package = exported(tmp_path)
    response = contracts.load(ROOT / "contracts/fixtures/valid/desktop.response.yaml")
    binding = {"id": package["id"], "hash": package["hash"]}
    response["package"] = response["document"]["package"] = binding
    for evidence in response["document"]["evidence"]:
        if evidence["kind"] != "text_layer":
            evidence["image"] = package["pages"][evidence["pdf_page"] - 1]["render"]
    assert desktop.check(package, response) == []
    # No fixture layout knowledge: every decoded PDF character and its real box is retained.
    with pdfplumber.open(io.BytesIO(EXAMPLE.read_bytes())) as document:
        for page, snapshot in zip(document.pages, package["pages"]):
            assert "".join(c["text"] for c in page.chars) == "".join(f["text"] for f in snapshot["fragments"])
            assert [g["bbox"] for f in snapshot["fragments"] for g in f["glyphs"]] == [
                [round(c[k], 3) for k in ("x0", "top", "x1", "bottom")] for c in page.chars]
    assert "NIGHT: LIMIT 1" not in "".join(f["text"] for p in package["pages"] for f in p["fragments"])


def test_context_has_no_output_ownership(tmp_path):
    package = export_package(EXAMPLE, tmp_path / "packet", doc="SRC-desktop.rules", target_pages=[1])
    assert package["target_pages"] == [1] and package["context_pages"] == [2]
    response = excluded_response(package)
    assert desktop.check(package, response) == []
    fragment = package["pages"][1]["fragments"][0]
    response["document"]["evidence"].append({"ref": "e.context", "kind": "text_layer", "spans": [
        {"fragment": fragment["ref"], "start": 0, "end": len(fragment["text"])}]})
    response["document"]["blocks"].append({"ref": "b.context", "type": "paragraph", "evidence": ["e.context"]})
    response["document"]["reading_order"].append("b.context")
    response["document"]["coverage"].append({"ref": "c.context", "pdf_page": 2, "bbox": fragment["bbox"],
        "classification": "content", "blocks": ["b.context"], "evidence": ["e.context"]})
    assert "desktop_context_write" in {d.code for d in desktop.check(package, response)}


def test_only_selected_pages_are_rendered_and_original_pdf_is_not_sent(tmp_path, monkeypatch):
    writer = PdfWriter()
    for n in range(1, 6):
        if n > 1:
            writer.page()
        writer.text(40, 80, f"Page {n} content")
    original = tmp_path / "original.pdf"
    original.write_bytes(writer.bytes())
    import wgc.desktop_export as exporter
    calls, real_render = [], exporter.render_page
    def render(data, number, scale):
        calls.append(number)
        return real_render(data, number, scale)
    monkeypatch.setattr(exporter, "render_page", render)
    package = export_package(original, tmp_path / "packet", doc="SRC-test.rules", target_pages=[3])
    assert package["source"]["page_count"] == 5
    assert package["context_pages"] == [2, 4]
    assert calls == [2, 3, 4]
    assert {p["pdf_page"] for p in package["pages"]} == {2, 3, 4}
    assert all(a["role"] not in {"source", "page_pdf"} for a in package["assets"])
    assert not any(p.suffix == ".pdf" for p in (tmp_path / "packet").iterdir())
    assert "Page 1 content" not in (tmp_path / "packet/manifest.txt").read_text("utf-8")
    explicit = export_package(original, tmp_path / "explicit", doc="SRC-test.rules", target_pages=[3], context_pages=[])
    assert explicit["context_pages"] == [] and [p["pdf_page"] for p in explicit["pages"]] == [3]
    assert explicit["hash"] != package["hash"] and explicit["id"] != package["id"]


def test_raw_unicode_offsets_preserve_multicodepoint_glyph_without_normalization(monkeypatch):
    chars = [{"text": t, "x0": x, "x1": x + 10, "top": 10, "bottom": 20, "size": 10}
             for x, t in ((10, "e\u0301"), (20, "fi"), (30, " "), (40, "A"))]
    class Document:
        pages = [SimpleNamespace(width=100, height=100, chars=chars)]
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
    monkeypatch.setattr(pdf, "_open_pdf", lambda data: Document())
    count, pages = pdf.raw_pages(b"mock decoded PDF", [1])
    fragment = pages[0]["fragments"][0]
    assert count == 1 and fragment["text"] == "e\u0301fi A"
    assert [(g["start"], g["end"]) for g in fragment["glyphs"]] == [(0, 2), (2, 4), (4, 5), (5, 6)]
    text, areas = desktop.resolve_text({"pages": pages}, {"spans": [{"fragment": "p1f1", "start": 2, "end": 4}]})
    assert text == "fi" and areas == [{"pdf_page": 1, "bbox": [20, 10, 30, 20]}]
    chars[0]["x1"] = chars[0]["x0"]
    with pytest.raises(IngestError, match="geometrią"):
        pdf.raw_pages(b"mock decoded PDF", [1])


def test_empty_text_layer_is_allowed_without_inventing_text(tmp_path):
    original = tmp_path / "blank.pdf"
    original.write_bytes(PdfWriter().bytes())
    package = export_package(original, tmp_path / "packet", doc="SRC-blank.rules", target_pages=[1])
    assert package["pages"][0]["fragments"] == []
    assert (tmp_path / "packet/p001.png").read_bytes().startswith(b"\x89PNG")


@pytest.mark.parametrize("kwargs", [
    {"target_pages": []}, {"target_pages": [0]}, {"target_pages": [3]},
    {"context_pages": [1]}, {"context_pages": [3]}, {"doc": "bad"},
    {"scale": float("nan")}, {"scale": 0}, {"scale": 5},
])
def test_bad_selection_does_not_publish(tmp_path, kwargs):
    options = {"doc": "SRC-desktop.rules", "target_pages": [1]}
    options.update(kwargs)
    with pytest.raises(ExportError):
        export_package(EXAMPLE, tmp_path / "packet", **options)
    assert not (tmp_path / "packet").exists()


def test_failed_render_and_existing_destination_preserve_files(tmp_path, monkeypatch):
    existing = tmp_path / "existing"
    existing.mkdir()
    (existing / "response.json").write_bytes(b"user answer")
    before = files(existing)
    with pytest.raises(ExportError, match="już istnieje"):
        export_package(EXAMPLE, existing, doc="SRC-test.rules", target_pages=[1])
    assert files(existing) == before
    import wgc.desktop_export as exporter
    def fail(*args):
        raise IngestError("Render failure")
    monkeypatch.setattr(exporter, "render_page", fail)
    with pytest.raises(ExportError, match="Render failure"):
        exported(tmp_path)
    assert not (tmp_path / "packet").exists()


def test_missing_and_damaged_pdf_are_cli_errors(tmp_path, capsys):
    path = tmp_path / "bad.pdf"
    for data in (None, b"not a PDF"):
        if data is not None:
            path.write_bytes(data)
        assert main(["desktop", "export", "--pdf", str(path), "--doc", "SRC-test.rules", "--pages", "1",
                     "--output", str(tmp_path / "packet")]) == 2
        assert "BŁĄD" in capsys.readouterr().err
        assert not (tmp_path / "packet").exists()


def test_publish_failure_leaves_no_partial_package_and_preserves_source(tmp_path, monkeypatch):
    original, real_rename = EXAMPLE.read_bytes(), Path.rename
    def fail(path, target):
        if path.name == "package":
            raise PermissionError("Directory is held open")
        return real_rename(path, target)
    monkeypatch.setattr(Path, "rename", fail)
    with pytest.raises(ExportError, match="held open"):
        exported(tmp_path)
    assert not (tmp_path / "packet").exists()
    assert not list(tmp_path.glob(".desktop-export-*"))
    assert EXAMPLE.read_bytes() == original


def test_cli_export_requires_explicit_scope_and_supports_no_context(tmp_path, capsys):
    args = ["desktop", "export", "--pdf", str(EXAMPLE), "--doc", "SRC-desktop.rules", "--pages", "1",
            "--context", "none", "--output", str(tmp_path / "packet")]
    assert main(args) == 0
    assert "kontekst: []" in capsys.readouterr().out
    package = json.loads((tmp_path / "packet/manifest.txt").read_text("utf-8"))
    assert [p["pdf_page"] for p in package["pages"]] == [1]
    with pytest.raises(SystemExit):
        main(args[:6] + args[8:])  # No --pages; never exports all implicitly.


@pytest.mark.parametrize("selection", ["", "all", "0", "2-1", "1,,2", "-1", "1-100001"])
def test_invalid_page_syntax(selection):
    with pytest.raises(ExportError):
        parse_pages(selection)


def test_export_does_not_change_legacy_inventory_cache_or_extraction(tmp_path):
    game = tmp_path / "game"
    (game / "source").mkdir(parents=True)
    writer = PdfWriter()
    writer.text(40, 80, "1.1", "F2", 9)
    writer.text(65, 80, "Move one hex.", "F1", 9)
    original = game / "source/rules.pdf"
    original.write_bytes(writer.bytes())
    source.init(game, "test", [("rules", "source/rules.pdf")])
    source.extract(game)
    assert source.verify(game).ok
    before, segments = files(game), copy.deepcopy(pdf.extract(original.read_bytes()))
    export_package(original, tmp_path / "packet", doc="SRC-test.rules", target_pages=[1])
    assert files(game) == before
    assert pdf.extract(original.read_bytes()) == segments
    assert source.verify(game).ok
