"""Own CC0 two-page contract example; regenerate with the repo's Python environment.

This builds only test artifacts, not a desktop exporter. No models or network.
"""
from __future__ import annotations

import copy
import io
import json
from pathlib import Path
import sys
import zlib

from PIL import Image, ImageDraw, ImageFont
import pdfplumber
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from wgc.canonical import content_hash, sha256_hex
from wgc.desktop import envelope_hash
from wgc.ingest.pdf import render_page

HERE = Path(__file__).resolve().parent
VALID = ROOT / "contracts/fixtures/valid"
WIDTH, HEIGHT = 595, 842
LINES = [
    [(40, 60, "1. River watch"), (40, 95, "1. Place one scout."), (40, 112, "2. Draw one signal."),
     (320, 95, "2. Crossing"), (320, 130, "A scout may cross the river"),
     (40, 200, "Flood conditions only"), (40, 235, "3. Spend two signals."), (40, 252, "Wait until the next turn."),
     (40, 795, "7")],
    [(40, 65, "only when the bridge is clear."), (40, 130, "4. Signal chart"),
     (40, 165, "Signal"), (190, 165, "Limit"), (40, 187, "Blue"), (190, 187, "1"),
     (320, 65, "5. Night watch"), (320, 100, "Keep one scout on the bank."), (40, 795, "8")]
]


def example_pdf() -> tuple[bytes, bytes]:
    image = Image.new("RGB", (440, 90), "#e4eef6")
    draw = ImageDraw.Draw(image)
    draw.text((12, 28), "NIGHT: LIMIT 1", font=ImageFont.load_default(size=28), fill="#12283c")
    png = io.BytesIO()
    image.save(png, format="PNG")
    streams = []
    for number, lines in enumerate(LINES, 1):
        stream = bytearray()
        if number == 1:
            stream += b"0.9 0.95 1 rg 30 562 255 100 re f 0.1 0.3 0.5 RG 1 w 30 562 255 100 re S\n"
        for x, y, text in lines:
            size = 9 if y != 60 else 14
            escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            stream += f"BT 0 0 0 rg /F1 {size} Tf {x} {HEIGHT-y} Td ({escaped}) Tj ET\n".encode("ascii")
        if number == 2:
            stream += b"q 220 0 0 45 320 657 cm /Im1 Do Q\n"
        streams.append(bytes(stream))
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>"]
    for number in (1, 2):
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {WIDTH} {HEIGHT}] /Resources << /Font << /F1 7 0 R >> /XObject << /Im1 8 0 R >> >> /Contents {4+number} 0 R >>".encode())
    objects.extend(b"<< /Length %d >>\nstream\n" % len(s) + s + b"endstream" for s in streams)
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")
    compressed = zlib.compress(image.tobytes())
    objects.append(b"<< /Type /XObject /Subtype /Image /Width 440 /Height 90 /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode /Length %d >>\nstream\n" % len(compressed) + compressed + b"\nendstream")
    out = io.BytesIO()
    out.write(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, 1):
        offsets.append(out.tell())
        out.write(b"%d 0 obj\n" % i + obj + b"\nendobj\n")
    xref = out.tell()
    out.write(b"xref\n0 9\n0000000000 65535 f \n")
    out.writelines(b"%010d 00000 n \n" % offset for offset in offsets)
    out.write(b"trailer\n<< /Size 9 /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % xref)
    return out.getvalue(), png.getvalue()


def generate() -> None:
    data, crop = example_pdf()
    (HERE / "source.pdf").write_bytes(data)
    (HERE / "night.png").write_bytes(crop)
    package = {"schema": "wgc/desktop@0", "kind": "package", "id": "river.p1-2", "task": "document.read@0",
               "source": {"doc": "SRC-desktop.rules", "file_hash": sha256_hex(data), "page_count": 2},
               "target_pages": [1, 2], "context_pages": [],
               "instructions": {"version": "document.read@0", "artifact": {"path": "instructions.txt", "hash": sha256_hex((HERE / "instructions.txt").read_bytes())}},
               "response_schema": "wgc/desktop@0#response", "assets": [], "pages": []}
    asset_files = [("source.pdf", "source"), ("instructions.txt", "instructions"),
                   ("legend.txt", "legend"), ("example.txt", "example"), ("desktop.schema.json", "schema")]
    (HERE / "desktop.schema.json").write_bytes((ROOT / "contracts/schemas/desktop.schema.json").read_bytes())
    for path, role in asset_files:
        package["assets"].append({"path": path, "hash": sha256_hex((HERE / path).read_bytes()), "role": role})
    package["assets"].append({"path": "night.png", "hash": sha256_hex(crop), "role": "crop", "pdf_page": 2})
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            path = f"p{number:03}.png"
            png = render_page(data, number, 1.0)
            (HERE / path).write_bytes(png)
            render = {"path": path, "hash": sha256_hex(png)}
            package["assets"].append({**render, "role": "render", "pdf_page": number})
            fragments = []
            for i, (_, baseline, text) in enumerate(LINES[number-1], 1):
                chars = sorted([c for c in page.chars if abs(HEIGHT - c["matrix"][5] - baseline) < .01], key=lambda c: c["x0"])
                # At a shared baseline select only the characters of this printed line.
                x = LINES[number-1][i-1][0]
                size = 14 if baseline == 60 else 9
                chars = [c for c in chars if x <= c["x0"] < x + len(text) * .6 * size - .01]
                assert "".join(c["text"] for c in chars) == text, (number, text, chars)
                boxes = [[round(c[k], 3) for k in ("x0", "top", "x1", "bottom")] for c in chars]
                fragments.append({"ref": f"p{number}f{i}", "text": text,
                                  "bbox": [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)],
                                  "glyphs": [{"start": j, "end": j+1, "bbox": b} for j, b in enumerate(boxes)]})
            package["pages"].append({"pdf_page": number, "printed_label": str(6+number), "width": WIDTH,
                                     "height": HEIGHT, "render": render, "fragments": fragments})
    package["hash"] = envelope_hash(package)
    binding = {"id": package["id"], "hash": package["hash"]}
    document = {"schema": "wgc/desktop@0", "kind": "document", "source": copy.deepcopy(package["source"]),
                "package": binding, "blocks": [], "reading_order": [], "relations": [], "evidence": [], "coverage": []}
    for page in package["pages"]:
        for f in page["fragments"]:
            e = "e." + f["ref"]
            document["evidence"].append({"ref": e, "kind": "text_layer", "spans": [{"fragment": f["ref"], "start": 0, "end": len(f["text"])}]})
    def block(ref, kind, page, indices, parent=None, label=None):
        ev = [f"e.p{page}f{i}" for i in indices]
        b = {"ref": ref, "type": kind, "evidence": ev}
        if parent:
            b["parent"] = parent
        if label:
            b["printed_label"] = label
        document["blocks"].append(b)
        document["reading_order"].append(ref)
        boxes = [package["pages"][page-1]["fragments"][i-1]["bbox"] for i in indices]
        document["coverage"].append({"ref": "c." + ref, "pdf_page": page, "bbox": [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)],
                                     "classification": "content", "evidence": ev, "blocks": [ref]})
        return b
    block("b.title", "heading", 1, [1], label="1")
    block("b.setup", "list", 1, [2, 3], "b.title")
    block("b.flood", "box", 1, [6], "b.title")
    block("b.flood-rule", "paragraph", 1, [7, 8], "b.flood", "3")
    block("b.crossing", "heading", 1, [4], label="2")
    block("b.crossing-start", "paragraph", 1, [5], "b.crossing")
    block("b.crossing-end", "paragraph", 2, [1], "b.crossing")
    block("b.chart-title", "heading", 2, [2], label="4")
    table = block("b.chart", "table", 2, [3, 4, 5, 6], "b.chart-title")
    table["table"] = {"rows": 2, "columns": 2, "notes": [], "cells": [
        {"row": i//2, "column": i%2, "row_span": 1, "column_span": 1, "role": "header" if i < 2 else "data", "evidence": [f"e.p2f{i+3}"]} for i in range(4)]}
    block("b.night-title", "heading", 2, [7], label="5")
    block("b.night-rule", "paragraph", 2, [8], "b.night-title")
    image = {"ref": "e.night", "kind": "image_transcription", "pdf_page": 2, "bbox": [320, 140, 540, 185],
             "image": {"path": "night.png", "hash": sha256_hex(crop)}, "text": "NIGHT: LIMIT 1",
             "discrepancy": "No corresponding text-layer fragment."}
    frame = {"ref": "e.frame", "kind": "visual_scope", "pdf_page": 1, "bbox": [30, 180, 285, 280],
             "image": package["pages"][0]["render"], "text": "Blue frame restricts rule 3 to flood conditions."}
    document["evidence"] += [image, frame]
    document["blocks"].append({"ref": "b.night-sign", "type": "note", "parent": "b.night-title", "evidence": ["e.night"]})
    document["reading_order"].append("b.night-sign")
    document["coverage"].append({"ref": "c.night-sign", "pdf_page": 2, "bbox": image["bbox"], "classification": "content", "evidence": ["e.night"], "blocks": ["b.night-sign"]})
    document["coverage"].append({"ref": "c.frame", "pdf_page": 1, "bbox": frame["bbox"], "classification": "excluded", "reason": "Frame geometry is preserved as relation evidence; text is covered separately.", "evidence": ["e.frame"], "blocks": []})
    document["relations"] = [
        {"ref": "r.crossing", "type": "continuation", "from": "b.crossing-start", "to": "b.crossing-end", "evidence": ["e.p1f5", "e.p2f1"]},
        {"ref": "r.flood", "type": "scope", "from": "b.flood", "to": "b.flood-rule", "cue": "frame", "evidence": ["e.frame", "e.p1f6"]}]
    for page in package["pages"]:
        f = page["fragments"][-1]
        document["coverage"].append({"ref": f"c.footer{page['pdf_page']}", "pdf_page": page["pdf_page"], "bbox": f["bbox"], "classification": "excluded", "reason": "Printed pagination.", "evidence": ["e." + f["ref"]], "blocks": []})
    response = {"schema": "wgc/desktop@0", "kind": "response", "package": binding,
                "producer": {"application": "unknown", "model": "unknown", "model_identity": "unknown"}, "document": document}
    reviews = [{"subject": item["ref"], "status": "pending"} for collection in ("blocks", "evidence", "relations", "coverage") for item in document[collection]]
    revision = {"schema": "wgc/desktop@0", "kind": "revision", "id": "rev.fixture.1", "package": binding,
                "response": {"path": "responses/fixture.yaml", "hash": content_hash(response)},
                "document": {"path": "documents/fixture.yaml", "hash": content_hash(document)},
                "validation": "valid", "reviews": reviews, "completeness": "partial"}
    revision["hash"] = envelope_hash(revision)
    for name, value in (("package", package), ("response", response), ("document", document), ("revision", revision)):
        (VALID / f"desktop.{name}.yaml").write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True, default_flow_style=None, width=120), encoding="utf-8")
    invalid = ROOT / "contracts/fixtures/desktop-invalid"
    invalid.mkdir(exist_ok=True)
    foreign = copy.deepcopy(response)
    foreign["package"]["hash"] = "sha256:" + "0" * 64
    (invalid / "foreign-package.yaml").write_text("# EXPECT: desktop_package_mismatch\n" + yaml.safe_dump(foreign, sort_keys=False), encoding="utf-8")
    print("Generated own PDF, renders and desktop contract fixtures.")


if __name__ == "__main__":
    generate()
