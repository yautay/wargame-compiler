"""Explicit, evidence-checked PDF page proposals (ADR-0036).

The provider sees a render and code-extracted words. It proposes reading order and
grouping only. Approved proposals live in the ignored .glu cache and are checked
again against the original PDF whenever source verify runs.
"""
from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from wgc.canonical import normalize_text, sha256_hex
from wgc.ingest import IngestError, Segment
from wgc.ingest import pdf

NAME = "wgc.ingest.pdf.hybrid@2"
FORMAT = "wgc/pdf-hybrid@1"
TYPES = {"rule", "heading", "table", "example", "designer_note", "historical_note",
         "play_note", "box", "list_item", "caption", "other"}


class Provider(Protocol):
    def propose(self, packet: dict, png: bytes, retry: int, issues: list[str]) -> dict: ...


class ReplayProvider:
    """Offline page proposals; p001.json and optional p001.retry.json."""

    def __init__(self, directory: Path):
        self.directory = Path(directory)

    def propose(self, packet: dict, png: bytes, retry: int, issues: list[str]) -> dict:
        stem = f"p{packet['page']:03d}" + (".retry" if retry else "")
        path = self.directory / f"{stem}.json"
        if retry and not path.exists():
            path = self.directory / f"p{packet['page']:03d}.json"
        return json.loads(path.read_text(encoding="utf-8"))


class CommandProvider:
    """Small process adapter; JSON request on stdin, JSON response on stdout.

    The command owns the model connection. No provider credentials or API protocol
    are added to WGC. Nonzero exit/invalid JSON leaves the page for review.
    """

    def __init__(self, executable: str):
        self.executable = executable

    def propose(self, packet: dict, png: bytes, retry: int, issues: list[str]) -> dict:
        import base64
        request = {"instruction": PROMPT, "page": packet, "png_base64": base64.b64encode(png).decode("ascii"),
                   "retry": retry, "issues": issues}
        proc = subprocess.run([self.executable], input=json.dumps(request, ensure_ascii=False),
                              text=True, capture_output=True, timeout=180, check=False)
        if proc.returncode:
            raise IngestError(f"Provider zakończył się kodem {proc.returncode}.")
        return json.loads(proc.stdout)


class CodexProvider:
    """Use the signed-in Codex CLI; no separate API key is required."""

    def propose(self, packet: dict, png: bytes, retry: int, issues: list[str]) -> dict:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="wgc-pdf-") as directory:
            image = Path(directory) / "page.png"
            output = Path(directory) / "proposal.json"
            image.write_bytes(png)
            prompt = (PROMPT + "\nReturn only a JSON object. Do not use tools or read other files.\n"
                      + json.dumps({"page": packet, "retry": retry, "issues": issues}, ensure_ascii=False))
            command = ["codex", "exec", "--ephemeral", "--ignore-rules", "--skip-git-repo-check",
                       "-s", "read-only", "--json", "-i", str(image), "-o", str(output), "-"]
            proc = subprocess.run(command, input=prompt, text=True, capture_output=True, timeout=600, check=False)
            if proc.returncode:
                detail = (proc.stderr.strip().splitlines() or [""])[-1][:200]
                raise IngestError(f"Codex CLI zakończył się kodem {proc.returncode}: {detail}")
            result = json.loads(output.read_text(encoding="utf-8"))
            usage = {"input_tokens": 0, "output_tokens": 0}
            for line in proc.stdout.splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if isinstance(event.get("usage"), dict):
                    usage["input_tokens"] += event["usage"].get("input_tokens", 0)
                    usage["output_tokens"] += event["usage"].get("output_tokens", 0)
            return {"proposal": result.get("proposal", result), "usage": usage}


PROMPT = """Propose reading order and segments for this PDF page using the supplied word IDs and page image.
Return JSON: {proposal:{segments:[{type,text,areas:[{page,bbox,word_ids}],
rows:[[ {text,areas} ]] for tables, label optional, continues_previous optional}],
exclusions:[{word_ids,reason}], unresolved:[{bbox,reason}],
image_only:[{bbox,description}]}, usage:{input_tokens,output_tokens,cost_usd} optional}.
Allowed segment types: rule, heading, table, example, designer_note, historical_note,
play_note, box, list_item, caption, other. Do not create a footer type: use exclusions
with reason pagination. For each area, use the tight union bbox of its word IDs.
Every text-layer word ID must occur exactly once in a segment or an explicit exclusion.
The segment text must equal its word texts joined with spaces in word_ids order;
table text must equal cells joined with tabs and rows joined with newlines.
Use exact printed text; do not invent OCR. Mark visible text absent from the text layer
in image_only and any uncertain region in unresolved. Exclude page numbers explicitly.
Do not assign IDs or hashes. For a continuation from the preceding page, set continues_previous.
If supplying a label, it must be a word present in that segment (punctuation may differ).
"""


def _bounds(bbox, width: float, height: float) -> bool:
    return (isinstance(bbox, list) and len(bbox) == 4 and all(isinstance(x, (int, float))
            and math.isfinite(x) for x in bbox) and 0 <= bbox[0] < bbox[2] <= width
            and 0 <= bbox[1] < bbox[3] <= height)


def pages(data: bytes) -> list[dict]:
    """Extract every text-layer word with stable, page-qualified IDs."""
    doc = pdf._open_pdf(data)
    try:
        result = []
        for number, page in enumerate(doc.pages, 1):
            raw = page.extract_words(x_tolerance=2, y_tolerance=3, keep_blank_chars=False)
            raw.sort(key=lambda w: (round(w["top"], 2), round(w["x0"], 2), w["text"]))
            words = [{"id": f"p{number}w{i}", "text": w["text"],
                      "bbox": [round(w[k], 2) for k in ("x0", "top", "x1", "bottom")]}
                     for i, w in enumerate(raw, 1)]
            unmapped = 0
            for char in page.chars:
                if not char["text"].strip():
                    continue
                cx, cy = (char["x0"] + char["x1"]) / 2, (char["top"] + char["bottom"]) / 2
                if not any(w["bbox"][0] - 1 <= cx <= w["bbox"][2] + 1 and
                           w["bbox"][1] - 1 <= cy <= w["bbox"][3] + 1 for w in words):
                    unmapped += 1
            result.append({"page": number, "width": float(page.width), "height": float(page.height),
                           "words": words, "unmapped_glyphs": unmapped})
        return result
    finally:
        doc.close()


def _area_words(areas, packet: dict, issues: list[str]) -> list[str]:
    if not isinstance(areas, list) or not areas:
        issues.append("missing_areas")
        return []
    known = {w["id"]: w for w in packet["words"]}
    found = []
    for area in areas:
        if not isinstance(area, dict) or area.get("page") != packet["page"]:
            issues.append("wrong_area_page")
            continue
        box = area.get("bbox")
        if not _bounds(box, packet["width"], packet["height"]):
            issues.append("area_out_of_bounds")
            continue
        ids = area.get("word_ids")
        if not isinstance(ids, list) or not ids:
            issues.append("empty_area")
            continue
        for wid in ids:
            word = known.get(wid)
            if word is None:
                issues.append(f"unknown_word:{wid}")
                continue
            wb = word["bbox"]
            if wb[0] < box[0] - .5 or wb[1] < box[1] - .5 or wb[2] > box[2] + .5 or wb[3] > box[3] + .5:
                issues.append(f"word_outside_area:{wid}")
            found.append(wid)
    return found


def _same_text(actual, ids: list[str], known: dict) -> bool:
    return isinstance(actual, str) and normalize_text(actual) == normalize_text(" ".join(known[i]["text"] for i in ids))


def check_page(packet: dict, proposal: dict) -> list[str]:
    """Reject gaps, duplicates, invented text, invalid boxes and broken table cells."""
    issues: list[str] = []
    if not isinstance(proposal, dict):
        return ["invalid_proposal"]
    known = {w["id"]: w for w in packet["words"]}
    if packet.get("unmapped_glyphs", 0):
        issues.append(f"unmapped_text_glyphs:{packet['unmapped_glyphs']}")
    if not known:
        issues.append("no_text_layer")
    segments = proposal.get("segments")
    if not isinstance(segments, list) or (known and not segments):
        return issues + ["no_segments"]
    used = []
    segment_used = []
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict) or segment.get("type") not in TYPES:
            issues.append(f"invalid_segment:{index}")
            continue
        if "id" in segment or "hash" in segment:
            issues.append(f"model_assigned_identity:{index}")
        ids = _area_words(segment.get("areas"), packet, issues)
        used.extend(ids)
        segment_used.extend(ids)
        valid_ids = [i for i in ids if i in known]
        if not _same_text(segment.get("text"), valid_ids, known):
            issues.append(f"text_mismatch:{index}")
        label = segment.get("label")
        if label is not None and (not isinstance(label, str) or not any(
                known[i]["text"].strip(".:") == label.strip(".:") for i in valid_ids)):
            issues.append(f"label_not_in_source:{index}")
        if segment["type"] == "table":
            rows = segment.get("rows")
            if not isinstance(rows, list) or not rows or any(not isinstance(r, list) or not r for r in rows):
                issues.append(f"invalid_table_rows:{index}")
                continue
            if len(rows) < 2 or any(len(row) < 2 for row in rows):
                issues.append(f"table_needs_review:{index}")
            if len({len(row) for row in rows}) != 1:
                issues.append(f"ragged_table:{index}")
            cell_ids = []
            rendered = []
            for row in rows:
                cells = []
                for cell in row:
                    if not isinstance(cell, dict):
                        issues.append(f"invalid_table_cell:{index}")
                        continue
                    ci = _area_words(cell.get("areas"), packet, issues)
                    cell_ids.extend(ci)
                    if not _same_text(cell.get("text"), [i for i in ci if i in known], known):
                        issues.append(f"cell_text_mismatch:{index}")
                    cells.append(cell.get("text", ""))
                rendered.append("\t".join(cells))
            if len(cell_ids) != len(set(cell_ids)) or sorted(cell_ids) != sorted(ids):
                issues.append(f"table_cell_coverage:{index}")
            if segment.get("text") != "\n".join(rendered):
                issues.append(f"table_structure_mismatch:{index}")
        elif "rows" in segment:
            issues.append(f"rows_on_non_table:{index}")
    exclusions = proposal.get("exclusions", [])
    if not isinstance(exclusions, list):
        issues.append("invalid_exclusions")
        exclusions = []
    for exclusion in exclusions:
        if not isinstance(exclusion, dict) or not isinstance(exclusion.get("reason"), str) or not exclusion["reason"].strip():
            issues.append("exclusion_without_reason")
            continue
        ids = exclusion.get("word_ids")
        if not isinstance(ids, list) or not ids:
            issues.append("exclusion_without_words")
            continue
        for wid in ids:
            word = known.get(wid)
            if (word and word["text"].strip() == str(packet["page"])
                    and word["bbox"][1] > .9 * packet["height"]
                    and "pagin" not in exclusion["reason"].lower()):
                issues.append(f"pagination_reason:{wid}")
        used.extend(ids)
    counts = {wid: used.count(wid) for wid in set(used)}
    issues += [f"duplicate_word:{wid}" for wid, count in counts.items() if count != 1]
    issues += [f"unknown_word:{wid}" for wid in used if wid not in known]
    issues += [f"uncovered_word:{wid}" for wid in known if wid not in counts]
    for wid in segment_used:
        word = known.get(wid)
        if word and word["text"].strip() == str(packet["page"]) and word["bbox"][1] > .9 * packet["height"]:
            issues.append(f"pagination_in_segment:{wid}")
    for field in ("unresolved", "image_only"):
        regions = proposal.get(field, [])
        if not isinstance(regions, list):
            issues.append(f"invalid_{field}")
            continue
        for region in regions:
            detail = "reason" if field == "unresolved" else "description"
            if (not isinstance(region, dict) or not _bounds(region.get("bbox"), packet["width"], packet["height"])
                    or not isinstance(region.get(detail), str) or not region[detail].strip()):
                issues.append(f"invalid_{field}_region")
            else:
                issues.append(f"{field}_requires_review")
    return sorted(set(issues))


def _segments(checked: list[tuple[dict, dict]]) -> list[Segment]:
    out: list[Segment] = []
    for packet, proposal in checked:
        for item in proposal["segments"]:
            areas = tuple(item["areas"])
            if item.get("continues_previous"):
                if not out or out[-1].areas[-1]["page"] != packet["page"] - 1 or out[-1].segment_type != item["type"]:
                    raise IngestError(f"Strona {packet['page']}: niepoprawna kontynuacja segmentu.")
                prev = out.pop()
                areas = prev.areas + areas
                text = prev.text + "\n" + item["text"]
                label = prev.label
                key = prev.key
                order = prev.order
            else:
                text, label = item["text"], item.get("label")
                key = f"p{packet['page']}s{len(out) + 1}"
                order = len(out) + 1
            boxes = [a["bbox"] for a in areas if a["page"] == areas[0]["page"]]
            bbox = tuple(round(v, 1) for v in (min(b[0] for b in boxes), min(b[1] for b in boxes),
                                                max(b[2] for b in boxes), max(b[3] for b in boxes)))
            first, last = areas[0]["page"], areas[-1]["page"]
            span = str(first) if first == last else f"{first}-{last}"
            out.append(Segment(key, label, item["type"], text, None, order, span, bbox, (), areas))
    return out


@dataclass
class Result:
    approved: dict | None
    report: dict
    segments: list[Segment]
    page_proposals: list[dict]


def run(data: bytes, provider: Provider) -> Result:
    checked = []
    page_proposals = []
    report = {"extractor": NAME, "pdf_hash": sha256_hex(data), "pages": [], "review_pages": [],
              "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
    for packet in pages(data):
        issues = ["no_text_layer"] if not packet["words"] else []
        proposal = None
        for retry in range(2 if packet["words"] else 0):
            try:
                response = provider.propose(packet, pdf.render_page(data, packet["page"], 2.0 + retry), retry, issues)
                proposal = response.get("proposal", response)
                usage = response.get("usage", {})
                for key in ("input_tokens", "output_tokens"):
                    report[key] += usage.get(key, 0) or 0
                if "cost_usd" in usage and report["cost_usd"] is not None:
                    report["cost_usd"] += usage["cost_usd"] or 0
                elif "cost_usd" not in usage:
                    report["cost_usd"] = None
                issues = check_page(packet, proposal)
            except (IngestError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as e:
                issues = [f"provider_error:{type(e).__name__}:{str(e)[:200]}"]
            if not issues:
                break
        status = "approved" if not issues else "review"
        report["pages"].append({"page": packet["page"], "status": status, "issues": issues,
                                "word_count": len(packet["words"]), "attempts": 0 if not packet["words"] else retry + 1})
        page_proposals.append({"page": packet["page"], "status": status, "issues": issues, "proposal": proposal})
        if issues:
            report["review_pages"].append(packet["page"])
        else:
            checked.append((packet, proposal))
    if report["review_pages"]:
        return Result(None, report, [], page_proposals)
    try:
        segments = _segments(checked)
    except IngestError as e:
        report["review_pages"] = [p["page"] for p, _ in checked]
        report["pages"].append({"status": "review", "issues": [str(e)]})
        return Result(None, report, [], page_proposals)
    approved = {"format": FORMAT, "extractor": NAME, "pdf_hash": sha256_hex(data),
                "pages": [{"page": p["page"], "proposal": proposal} for p, proposal in checked]}
    return Result(approved, report, segments, page_proposals)


def load_approved(data: bytes, artifact: dict) -> list[Segment]:
    if artifact.get("format") != FORMAT or artifact.get("extractor") != NAME or artifact.get("pdf_hash") != sha256_hex(data):
        raise IngestError("Zatwierdzony wynik hybrydowy nie pasuje do hasha PDF lub wersji ekstraktora.")
    packets = pages(data)
    entries = artifact.get("pages", [])
    if len(entries) != len(packets):
        raise IngestError("Zatwierdzony wynik hybrydowy nie obejmuje wszystkich stron PDF.")
    checked = []
    for packet, entry in zip(packets, entries):
        if entry.get("page") != packet["page"]:
            raise IngestError("Kolejność stron w zatwierdzonym wyniku jest niepoprawna.")
        issues = check_page(packet, entry.get("proposal"))
        if issues:
            raise IngestError(f"Strona {packet['page']}: zatwierdzony wynik jest niepoprawny: {', '.join(issues[:8])}.")
        checked.append((packet, entry["proposal"]))
    return _segments(checked)


def artifact_hash(artifact: dict) -> str:
    return sha256_hex(json.dumps(artifact, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
