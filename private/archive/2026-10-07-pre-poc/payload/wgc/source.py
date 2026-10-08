"""Stage 0: source inventory and the `wgc source init|scan|extract|verify|render` commands (DATA-CONTRACTS §9, ADR-0020, ADR-0021).

The inventory `source/inventory.yaml` (`wgc/source@0`) is committed in the game repo; segment text lives only in
`.glu/source/<SRC-id>/<SEG-id>.txt` (ADR-0012). `scan` and `extract` rewrite the inventory deterministically:
generated fields are replaced, hand-set fields are kept (see `GENERATED_SEGMENT_FIELDS`).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from wgc import contracts, ids
from wgc.canonical import sha256_hex, struct_hash, text_hash
from wgc.ingest import IngestError, Segment, extractor_for
from wgc.validate import ERROR, WARNING, Diagnostic, Report, load_documents, validate

CONTRACT = "wgc/source@0"
INVENTORY = Path("source") / "inventory.yaml"
CACHE = Path(".glu") / "source"

# Default precedence by role (higher wins on an explicit conflict, docs/LOGIC-MODEL.md#pierwszenstwo-zrodel).
# Printed game components rank with the printed rules (a conflict between them is an ambiguity for a human).
# `prior_translation` and `other` have no default: they need an explicit `precedence`. An explicit `precedence`
# in the inventory overrides the default; `project.yaml` policy comes in M7.
DEFAULT_PRECEDENCE: dict[str, int] = {
    "errata": 60,
    "living_rules": 50,
    "rules": 40, "scenario_book": 40, "charts": 40, "cards": 40, "counters": 40, "map": 40, "module": 40,
    "faq": 30,
    "designer_clarification": 20,
    "community_interpretation": 10,
}

# Field order in the written inventory (schema order).
DOCUMENT_FIELDS = ("kind", "id", "role", "title", "edition", "language", "path", "file_hash", "present", "complete",
                   "precedence", "edition_skew", "seg_prefix", "extractor", "hybrid_hash", "notes")
SEGMENT_FIELDS = ("kind", "id", "doc", "label", "segment_type", "parent", "order", "pages", "bbox", "areas", "text_hash",
                  "struct_hash", "visual_flags", "verified_by_render", "corrections")
# Segment fields owned by the extractor; `corrections` and `verified_by_render` are hand-set and kept
# (`verified_by_render` is dropped when the text or its structure changes: the render confirmed the old extraction).
GENERATED_SEGMENT_FIELDS = ("doc", "label", "segment_type", "parent", "order", "pages", "bbox", "areas", "text_hash",
                            "struct_hash", "visual_flags")

# Stage 0 diagnostic codes of `verify` (besides the validator's codes for the inventory itself).
CODES = ("source_missing", "file_hash_mismatch", "extractor_changed", "extract_error", "hybrid_area_mismatch", "segment_hash_mismatch",
         "segment_struct_mismatch", "segment_missing", "segment_unlisted", "struct_hash_missing", "cache_missing",
         "cache_mismatch")

HEADER = """\
# wgc/source@0: inwentarz źródeł (Stage 0), commitowany. Tekst segmentów jest tylko w .glu/source/ (ADR-0012).
# Plik zapisują `wgc source scan|extract`: pola generowane są nadpisywane, pola ręczne zostają (title, edition,
# language, complete, precedence, edition_skew, seg_prefix, notes, corrections, verified_by_render).
# Komentarze nie są zachowywane: notatki zapisuj w polu `notes`.
"""


class SourceError(Exception):
    """An operational error of a `wgc source` command (message in Polish)."""


@dataclass
class Inventory:
    documents: list[dict] = field(default_factory=list)
    segments: list[dict] = field(default_factory=list)

    def document(self, doc_id: str) -> dict | None:
        return next((d for d in self.documents if d["id"] == doc_id), None)

    def segments_of(self, doc_id: str) -> list[dict]:
        return [s for s in self.segments if s.get("doc") == doc_id]


def roles() -> list[str]:
    return contracts.schema_for(CONTRACT)["$defs"]["source_document"]["properties"]["role"]["enum"]


def effective_precedence(doc: dict) -> int | None:
    """Explicit `precedence`, else the default for the document's role (None: no default, must be explicit)."""
    if "precedence" in doc:
        return doc["precedence"]
    return DEFAULT_PRECEDENCE.get(doc.get("role"))


def seg_prefix(doc: dict) -> str:
    """Key prefix of the document's segment ids: `seg_prefix`, else the key of its `SRC-` id."""
    return doc.get("seg_prefix") or ids.parse_id(doc["id"]).key


def segment_id(doc: dict, key: str) -> str:
    sid = f"SEG-{seg_prefix(doc)}.{key}"
    if not ids.is_id(sid):
        raise IngestError(f"Klucz segmentu `{key}` daje niepoprawne ID `{sid}`.")
    return sid


def inventory_path(root: Path) -> Path:
    return Path(root) / INVENTORY


def cache_dir(root: Path, doc_id: str) -> Path:
    return Path(root) / CACHE / doc_id


# --- inventory I/O ---------------------------------------------------------------------------------------------

def read_inventory(root: Path) -> Inventory:
    path = inventory_path(root)
    if not path.is_file():
        raise SourceError(f"Brak inwentarza {path.as_posix()}: uruchom `wgc source init`.")
    try:
        docs = load_documents(path)
    except yaml.YAMLError as e:
        raise SourceError(f"Inwentarz {path.as_posix()} nie jest poprawnym YAML-em: {e}") from None
    if len(docs) != 1 or not isinstance(docs[0], dict) or docs[0].get("schema") != CONTRACT:
        raise SourceError(f"Inwentarz {path.as_posix()} musi być jednym dokumentem `{CONTRACT}`.")
    errs = contracts.errors(docs[0])
    if errs:
        raise SourceError(f"Inwentarz {path.as_posix()} jest niezgodny ze schematem `{CONTRACT}`: {errs[0]}")
    inv = Inventory()
    for rec in docs[0].get("records") or []:
        (inv.documents if rec["kind"] == "source_document" else inv.segments).append(rec)
    return inv


def _ordered(rec: dict, fields: tuple[str, ...]) -> dict:
    out = {f: rec[f] for f in fields if f in rec}
    out.update({k: v for k, v in rec.items() if k not in out})
    return out


def _flow(rec: dict) -> str:
    return yaml.safe_dump(rec, default_flow_style=True, allow_unicode=True, sort_keys=False,
                          width=1_000_000).strip()


def dump_inventory(inv: Inventory) -> str:
    doc_order = {d["id"]: i for i, d in enumerate(inv.documents)}
    segments = sorted(inv.segments, key=lambda s: (doc_order.get(s.get("doc"), len(doc_order)), s.get("order", 0)))
    lines = [HEADER.rstrip("\n"), f"schema: {CONTRACT}", "records:"]
    lines += [f"  - {_flow(_ordered(d, DOCUMENT_FIELDS))}" for d in inv.documents]
    lines += [f"  - {_flow(_ordered(s, SEGMENT_FIELDS))}" for s in segments]
    if not inv.documents and not segments:
        lines[-1] = "records: []"
    return "\n".join(lines) + "\n"


def write_inventory(root: Path, inv: Inventory) -> Path:
    text = dump_inventory(inv)
    doc = yaml.safe_load(text)
    errs = contracts.errors(doc)
    if errs:
        raise SourceError(f"Wygenerowany inwentarz jest niezgodny ze schematem `{CONTRACT}`: {errs[0]}")
    path = inventory_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


# --- commands ----------------------------------------------------------------------------------------------------

def _project_path(root: Path, path: str) -> str:
    """`path` (relative to `root`, or absolute inside it) as a project-relative POSIX path."""
    root = Path(root).resolve()
    p = Path(path)
    full = (p if p.is_absolute() else root / p).resolve()
    try:
        return full.relative_to(root).as_posix()
    except ValueError:
        raise SourceError(f"Ścieżka {path} leży poza katalogiem projektu {root.as_posix()}.") from None


def init(root: Path, game: str, docs: list[tuple[str, str]]) -> list[str]:
    """Create `source/inventory.yaml` with one `source_document` per (role, path) and scan the files."""
    root = Path(root)
    if inventory_path(root).exists():
        raise SourceError(f"Inwentarz {inventory_path(root).as_posix()} już istnieje.")
    if not ids.is_id(f"SRC-{game}"):
        raise SourceError(f"Kod gry `{game}` nie daje poprawnego ID (`SRC-{game}`).")
    known = roles()
    inv = Inventory()
    has_rules_prefix = False
    for role, path in docs:
        if role not in known:
            raise SourceError(f"Nieznana rola `{role}`. Dozwolone: {', '.join(known)}.")
        base = f"SRC-{game}.{role}"
        doc_id, n = base, 1
        while inv.document(doc_id):
            n += 1
            doc_id = f"{base}.{n}"
        doc = {"kind": "source_document", "id": doc_id, "role": role, "path": _project_path(root, path),
               "present": False}
        if role == "rules" and not has_rules_prefix:
            doc["seg_prefix"] = game  # segments of the main rules are SEG-<game>.<label>
            has_rules_prefix = True
        inv.documents.append(doc)
    messages = _scan(root, inv)
    path = write_inventory(root, inv)
    return messages + [f"Utworzono {path.as_posix()} (dokumenty: {len(inv.documents)})."]


def _scan(root: Path, inv: Inventory) -> list[str]:
    messages = []
    for doc in inv.documents:
        if "path" not in doc:
            messages.append(f"{doc['id']}: bez ścieżki (present: {str(doc['present']).lower()}).")
            continue
        p = Path(root) / doc["path"]
        if not p.is_file():
            doc["present"] = False
            messages.append(f"{doc['id']}: brak pliku {doc['path']}.")
            continue
        h = sha256_hex(p.read_bytes())
        state = "bez zmian" if doc.get("file_hash") == h else ("zmieniony" if "file_hash" in doc else "nowy")
        doc["present"], doc["file_hash"] = True, h
        ext = extractor_for(doc["path"])
        if ext and doc.get("extractor") == "wgc.ingest.pdf.hybrid@2" and ext[0].startswith("wgc.ingest.pdf@"):
            pass  # explicit hybrid choice survives scan; source verify checks its artifact
        elif ext:
            doc["extractor"] = ext[0]
        else:
            state += ", brak ekstraktora dla tego formatu"
        messages.append(f"{doc['id']}: {state} ({h}).")
    return messages


def scan(root: Path) -> list[str]:
    """Refresh `present`, `file_hash` and `extractor` of every document with a `path`."""
    inv = read_inventory(root)
    messages = _scan(root, inv)
    write_inventory(root, inv)
    return messages


def _extract_doc(root: Path, doc: dict) -> list[tuple[str, Segment]] | None:
    """(segment id, segment) of a present document, None when it has no file or no extractor."""
    if not doc.get("present") or "path" not in doc:
        return None
    p = Path(root) / doc["path"]
    ext = extractor_for(doc["path"])
    if not p.is_file() or ext is None:
        return None
    if doc.get("extractor") == "wgc.ingest.pdf.hybrid@2":
        from wgc.ingest import pdf_hybrid
        artifact_path = cache_dir(root, doc["id"]) / "hybrid" / "approved.json"
        try:
            artifact = __import__("json").loads(artifact_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise IngestError(f"Brak poprawnego zatwierdzonego wyniku hybrydowego: {e}") from None
        if doc.get("hybrid_hash") != pdf_hybrid.artifact_hash(artifact):
            raise IngestError("Hash zatwierdzonego wyniku hybrydowego nie zgadza się z inwentarzem.")
        return [(segment_id(doc, s.key), s) for s in pdf_hybrid.load_approved(p.read_bytes(), artifact)]
    return [(segment_id(doc, s.key), s) for s in ext[1](p.read_bytes())]


def _segment_record(doc: dict, sid: str, seg: Segment, old: dict | None) -> dict:
    rec = {"kind": "segment", "id": sid, "doc": doc["id"]}
    if seg.label is not None:
        rec["label"] = seg.label
    rec["segment_type"] = seg.segment_type
    if seg.parent_key is not None:
        rec["parent"] = segment_id(doc, seg.parent_key)
    rec["order"] = seg.order
    if seg.pages is not None:
        rec["pages"] = seg.pages
    if seg.bbox is not None:
        rec["bbox"] = list(seg.bbox)
    if seg.areas:
        rec["areas"] = list(seg.areas)
    rec["text_hash"] = text_hash(seg.text)
    rec["struct_hash"] = struct_hash(seg.text)
    if seg.visual_flags:
        rec["visual_flags"] = list(seg.visual_flags)
    if old:
        for k, v in old.items():
            if k not in GENERATED_SEGMENT_FIELDS and k not in rec:
                rec[k] = v
        if _changed(old, rec):
            rec.pop("verified_by_render", None)
    return rec


def _changed(old: dict, new: dict) -> bool:
    """The segment's text or its structure changed. A record without `struct_hash` (extractor @0, before ADR-0032)
    gets one at regeneration: that alone is not a change."""
    return old.get("text_hash") != new["text_hash"] or old.get("struct_hash", new["struct_hash"]) != new["struct_hash"]


def _write_cache(root: Path, doc_id: str, extracted: list[tuple[str, Segment]]) -> None:
    d = cache_dir(root, doc_id)
    d.mkdir(parents=True, exist_ok=True)
    for stale in d.glob("*.txt"):
        stale.unlink()
    for sid, seg in extracted:
        with (d / f"{sid}.txt").open("w", encoding="utf-8", newline="\n") as f:
            f.write(seg.text)


def extract(root: Path) -> list[str]:
    """Scan, then segment every present document: inventory segment records and text in `.glu/source/`."""
    root = Path(root)
    inv = read_inventory(root)
    messages = _scan(root, inv)
    for doc in inv.documents:
        try:
            extracted = _extract_doc(root, doc)
        except IngestError as e:
            raise SourceError(f"{doc['id']}: {e}") from None
        if extracted is None:
            continue
        old = {s["id"]: s for s in inv.segments_of(doc["id"])}
        new = [_segment_record(doc, sid, seg, old.get(sid)) for sid, seg in extracted]
        changed = sum(1 for r in new if r["id"] in old and _changed(old[r["id"]], r))
        added = sum(1 for r in new if r["id"] not in old)
        removed = len(set(old) - {r["id"] for r in new})
        inv.segments = [s for s in inv.segments if s.get("doc") != doc["id"]] + new
        _write_cache(root, doc["id"], extracted)
        messages.append(f"{doc['id']}: segmenty {len(new)} (nowe {added}, zmienione {changed}, usunięte {removed}).")
    write_inventory(root, inv)
    return messages


def hybrid(root: Path, doc_id: str, provider) -> list[str]:
    """Explicit PDF hybrid run. A review result never changes the inventory."""
    import json
    from wgc.ingest import pdf_hybrid

    root = Path(root)
    inv = read_inventory(root)
    doc = inv.document(doc_id)
    if doc is None or not doc.get("path", "").lower().endswith(".pdf"):
        raise SourceError(f"{doc_id}: wybierz dokument PDF z inwentarza.")
    path = root / doc["path"]
    if not path.is_file():
        raise SourceError(f"{doc_id}: brak pliku PDF.")
    try:
        result = pdf_hybrid.run(path.read_bytes(), provider)
    except IngestError as e:
        raise SourceError(f"{doc_id}: {e}") from None
    directory = cache_dir(root, doc_id) / "hybrid"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "report.json").write_text(json.dumps(result.report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    proposal_dir = directory / "proposals"
    proposal_dir.mkdir(exist_ok=True)
    for item in result.page_proposals:
        (proposal_dir / f"p{item['page']:03d}.json").write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n",
                                                              encoding="utf-8")
    if result.approved is None:
        if not inv.segments_of(doc_id) and "hybrid_hash" not in doc:
            doc["extractor"] = pdf_hybrid.NAME  # explicit selection, but no approved segments
            write_inventory(root, inv)
        raise SourceError(f"{doc_id}: strony do przeglądu: {result.report['review_pages']}; raport: {directory / 'report.json'}.")
    (directory / "approved.json").write_text(json.dumps(result.approved, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8")
    doc["extractor"] = pdf_hybrid.NAME
    doc["hybrid_hash"] = pdf_hybrid.artifact_hash(result.approved)
    doc["present"] = True
    doc["file_hash"] = sha256_hex(path.read_bytes())
    old = {s["id"]: s for s in inv.segments_of(doc_id)}
    new = [_segment_record(doc, segment_id(doc, s.key), s, old.get(segment_id(doc, s.key)))
           for s in result.segments]
    inv.segments = [s for s in inv.segments if s.get("doc") != doc_id] + new
    _write_cache(root, doc_id, [(segment_id(doc, s.key), s) for s in result.segments])
    write_inventory(root, inv)
    return [f"{doc_id}: zatwierdzono {len(result.report['pages'])} stron i {len(new)} segmentów; raport: "
            f"{directory / 'report.json'}." ]


def hybrid_prepare(root: Path, doc_id: str) -> list[str]:
    """Export word packets and renders for an assistant in Codex/Claude Desktop."""
    import json
    from wgc.ingest import pdf, pdf_hybrid

    root = Path(root)
    doc = read_inventory(root).document(doc_id)
    if doc is None or not doc.get("path", "").lower().endswith(".pdf"):
        raise SourceError(f"{doc_id}: wybierz dokument PDF z inwentarza.")
    path = root / doc["path"]
    if not path.is_file():
        raise SourceError(f"{doc_id}: brak pliku PDF.")
    data = path.read_bytes()
    directory = cache_dir(root, doc_id) / "hybrid" / "prepared"
    directory.mkdir(parents=True, exist_ok=True)
    try:
        packets = pdf_hybrid.pages(data)
    except IngestError as e:
        raise SourceError(f"{doc_id}: {e}") from None
    for packet in packets:
        stem = f"p{packet['page']:03d}"
        (directory / f"{stem}.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n",
                                                   encoding="utf-8")
        (directory / f"{stem}.png").write_bytes(pdf.render_page(data, packet["page"], 2.0))
    return [f"{doc_id}: przygotowano {len(packets)} stron w {directory}. Propozycje zapisz jako pNNN.json "
            "w osobnym katalogu i uruchom `wgc source hybrid --replay-dir`." ]


def parse_pages(spec: str) -> list[int]:
    """`"3"`, `"3-4"` or `"1,3-4"` → sorted 1-based page numbers."""
    out: set[int] = set()
    for part in spec.split(","):
        a, sep, b = part.strip().partition("-")
        try:
            lo, hi = int(a), int(b) if sep else int(a)
        except ValueError:
            raise SourceError(f"Niepoprawny zakres stron `{spec}` (oczekiwano np. 3, 3-4 albo 1,3-4).") from None
        if lo < 1 or hi < lo:
            raise SourceError(f"Niepoprawny zakres stron `{spec}`.")
        out.update(range(lo, hi + 1))
    return sorted(out)


def render(root: Path, doc_id: str | None = None, segment: str | None = None, pages: str | None = None,
           scale: float = 2.0) -> list[str]:
    """Render PDF pages to `.glu/source/<SRC-id>/pages/p<NNN>.png` for manual verification (`verified_by_render`).

    Pages: `pages`, else the pages of `segment`, else the whole document.
    """
    from wgc.ingest import pdf

    root = Path(root)
    inv = read_inventory(root)
    if segment is not None:
        seg = next((s for s in inv.segments if s["id"] == segment), None)
        if seg is None:
            raise SourceError(f"Segmentu {segment} nie ma w inwentarzu.")
        if doc_id is not None and doc_id != seg.get("doc"):
            raise SourceError(f"Segment {segment} należy do {seg.get('doc')}, nie do {doc_id}.")
        doc_id = seg.get("doc")
        if pages is None:
            if "pages" not in seg:
                raise SourceError(f"Segment {segment} nie ma pola `pages` (render obsługuje tylko PDF).")
            pages = seg["pages"]
    if doc_id is None:
        raise SourceError("Podaj dokument (--doc) albo segment (--segment).")
    doc = inv.document(doc_id)
    if doc is None:
        raise SourceError(f"Dokumentu {doc_id} nie ma w inwentarzu.")
    if not doc.get("present") or "path" not in doc or not (root / doc["path"]).is_file():
        raise SourceError(f"{doc_id}: brak pliku do renderu.")
    ext = extractor_for(doc["path"])
    if ext is None or ext[0] != pdf.NAME:
        raise SourceError(f"{doc_id}: render obsługuje tylko PDF.")
    data = (root / doc["path"]).read_bytes()
    numbers = parse_pages(pages) if pages is not None else list(range(1, pdf.page_count(data) + 1))
    out_dir = cache_dir(root, doc_id) / "pages"
    out_dir.mkdir(parents=True, exist_ok=True)
    messages = []
    for n in numbers:
        try:
            png = pdf.render_page(data, n, scale)
        except IngestError as e:
            raise SourceError(f"{doc_id}: {e}") from None
        target = out_dir / f"p{n:03d}.png"
        target.write_bytes(png)
        messages.append(f"{doc_id}: strona {n} → {target.as_posix()}")
    return messages


def verify(root: Path) -> Report:
    """Validate the inventory, then re-extract and compare file hashes, segment hashes and the text cache."""
    root = Path(root)
    path = inventory_path(root)
    inv = read_inventory(root)
    report = validate([path])
    loc = path.as_posix()
    diags = report.diagnostics

    def add(code, severity, subject, message, affected=()):
        diags.append(Diagnostic(code, severity, subject, message, list(affected), loc))

    for doc in inv.documents:
        did = doc["id"]
        listed = {s["id"]: s for s in inv.segments_of(did)}
        if doc.get("present") and "path" in doc:
            p = root / doc["path"]
            if not p.is_file():
                add("source_missing", ERROR, did, f"Brak pliku {doc['path']} oznaczonego jako obecny.")
                continue
            h = sha256_hex(p.read_bytes())
            if doc.get("file_hash") != h:
                add("file_hash_mismatch", ERROR, did,
                    f"Plik {doc['path']} ma hash {h}, inwentarz: {doc.get('file_hash')}. Uruchom `wgc source extract`.")
            ext = extractor_for(doc["path"])
            if ext and doc.get("extractor") != ext[0] and doc.get("extractor") != "wgc.ingest.pdf.hybrid@2":
                add("extractor_changed", WARNING, did,
                    f"Inwentarz zapisał ekstraktor {doc.get('extractor')}, bieżący to {ext[0]}: uruchom "
                    "`wgc source extract`.")
            try:
                extracted = _extract_doc(root, doc)
            except IngestError as e:
                add("extract_error", ERROR, did, str(e))
                extracted = None
            if extracted is not None:
                fresh = {sid: seg for sid, seg in extracted}
                for sid, seg in fresh.items():
                    h, sh = text_hash(seg.text), struct_hash(seg.text)
                    if sid not in listed:
                        add("segment_unlisted", ERROR, sid, f"Segment z {doc['path']} nie jest w inwentarzu.", [did])
                    elif listed[sid].get("text_hash") != h:
                        add("segment_hash_mismatch", ERROR, sid,
                            f"Tekst segmentu ma hash {h}, inwentarz: {listed[sid].get('text_hash')}.", [did])
                    elif listed[sid].get("struct_hash", sh) != sh:
                        add("segment_struct_mismatch", ERROR, sid,
                            f"Ten sam tekst, ale inne wiersze albo komórki: `struct_hash` {sh}, inwentarz: "
                            f"{listed[sid]['struct_hash']}. Uruchom `wgc source extract`.", [did])
                    elif doc.get("extractor") == "wgc.ingest.pdf.hybrid@2" and (
                            listed[sid].get("areas") != list(seg.areas) or listed[sid].get("pages") != seg.pages
                            or listed[sid].get("bbox") != list(seg.bbox)
                            or listed[sid].get("segment_type") != seg.segment_type
                            or listed[sid].get("label") != seg.label or listed[sid].get("order") != seg.order):
                        add("hybrid_area_mismatch", ERROR, sid,
                            "Obszary lub typ segmentu nie zgadzają się z zatwierdzonym wynikiem hybrydowym.", [did])
                for sid in listed.keys() - fresh.keys():
                    add("segment_missing", ERROR, sid, f"Segmentu z inwentarza nie ma już w {doc['path']}.", [did])
        unstructured = [sid for sid, seg in listed.items() if "struct_hash" not in seg]
        if unstructured:
            add("struct_hash_missing", ERROR, did,
                f"{len(unstructured)} segmentów bez `struct_hash`: inwentarz i tekst z ekstraktora sprzed ADR-0032. "
                "Uruchom `wgc source extract`.", unstructured)
        missing = []
        for sid, seg in listed.items():
            f = cache_dir(root, did) / f"{sid}.txt"
            if not f.is_file():
                missing.append(sid)
                continue
            cached = f.read_text(encoding="utf-8")
            if text_hash(cached) != seg.get("text_hash"):
                add("cache_mismatch", ERROR, sid, f"Tekst w {f.as_posix()} nie zgadza się z `text_hash`.", [did])
            elif seg.get("struct_hash", struct_hash(cached)) != struct_hash(cached):
                add("cache_mismatch", ERROR, sid, f"Tekst w {f.as_posix()} ma te same słowa, ale inne wiersze albo "
                    "komórki niż `struct_hash` inwentarza: uruchom `wgc source extract`.", [did])
        if missing:
            add("cache_missing", WARNING, did,
                f"Brak tekstu {len(missing)} segmentów w {cache_dir(root, did).as_posix()}: uruchom `wgc source extract`.",
                missing)
    return report
