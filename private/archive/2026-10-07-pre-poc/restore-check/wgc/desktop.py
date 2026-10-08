"""Read-only checks for desktop contract fixtures, without import, storage or inference.

`check` verifies shape, hashes, references and review consistency. It cannot verify
meaning or visual completeness, and never changes a review status (ADR-0037).
"""
from __future__ import annotations

from collections import Counter
import math

from wgc import contracts
from wgc.canonical import content_hash
from wgc.validate import Diagnostic, ERROR


def envelope_hash(envelope: dict) -> str:
    """Canonical WGC hash of all fields except the envelope's own `hash`."""
    return content_hash({k: v for k, v in envelope.items() if k != "hash"})


def _fragments(package: dict) -> dict:
    return {f["ref"]: (p, f) for p in package["pages"] for f in p["fragments"]}


def resolve_text(package: dict, evidence: dict) -> tuple[str, list[dict]]:
    """Reconstruct exact slices and glyph union boxes in the declared order.

    Call only after `check` has accepted the references and spans. No normalized
    text offsets and no model-supplied copy of PDF text are used.
    """
    fragments = _fragments(package)
    texts, areas = [], []
    for span in evidence["spans"]:
        page, fragment = fragments[span["fragment"]]
        texts.append(fragment["text"][span["start"]:span["end"]])
        boxes = [g["bbox"] for g in fragment["glyphs"]
                 if span["start"] <= g["start"] and g["end"] <= span["end"]]
        areas.append({"pdf_page": page["pdf_page"], "bbox": [min(b[0] for b in boxes), min(b[1] for b in boxes),
                       max(b[2] for b in boxes), max(b[3] for b in boxes)]})
    return "\n".join(texts), areas


def check(package: dict, response: dict, revision: dict | None = None) -> list[Diagnostic]:
    """Check a supplied bundle in memory; an empty result gives no semantic approval."""
    issues: list[Diagnostic] = []

    def add(code, subject, message):
        issues.append(Diagnostic("desktop_" + code, ERROR, subject, message, []))

    for expected, envelope in (("package", package), ("response", response), ("revision", revision)):
        if envelope is None and expected == "revision":
            continue
        if (not isinstance(envelope, dict) or envelope.get("schema") != "wgc/desktop@0"
                or contracts.errors(envelope) or envelope.get("kind") != expected):
            add("schema_error", expected, "Dane nie odpowiadają kontraktowi i rodzajowi koperty.")
    if issues:
        return issues

    binding = {"id": package["id"], "hash": package["hash"]}
    document = response["document"]
    if package["hash"] != envelope_hash(package):
        add("manifest_hash", package["id"], "Hash manifestu pakietu nie odpowiada jego treści.")
    if response["package"] != binding or document["package"] != binding or document["source"] != package["source"]:
        add("package_mismatch", "response", "Odpowiedź wskazuje inny pakiet lub źródło.")

    def index(items, field, subject):
        counts = Counter(i[field] for i in items)
        if any(n != 1 for n in counts.values()):
            add("duplicate_ref", subject, "Identyfikatory w zbiorze nie są unikalne.")
        return {i[field]: i for i in items}

    pages = index(package["pages"], "pdf_page", "pages")
    target, context = set(package["target_pages"]), set(package["context_pages"])
    if target & context or set(pages) != target | context or any(p > package["source"]["page_count"] for p in pages):
        add("page_scope", "pages", "Zakres docelowy i kontekst muszą być rozłączne oraz odpowiadać stronom pakietu.")
    assets = index(package["assets"], "path", "assets")

    def artifact(ref, roles, number=None):
        asset = assets.get(ref["path"])
        return (asset is not None and asset["hash"] == ref["hash"] and asset["role"] in roles
                and (number is None or asset.get("pdf_page") == number))

    if not artifact(package["instructions"]["artifact"], {"instructions"}):
        add("asset_mismatch", "instructions", "Instrukcja nie odpowiada manifestowi plików.")
    if any(a["role"] == "source" and a["hash"] != package["source"]["file_hash"] for a in assets.values()):
        add("asset_mismatch", "source", "Oryginał w pakiecie nie odpowiada hashowi źródła.")
    for role in ("schema", "legend", "example"):
        if not any(a["role"] == role for a in assets.values()):
            add("asset_mismatch", role, "Brak wymaganego pliku pomocniczego w manifeście.")

    def bounds(number, box, subject):
        page = pages.get(number)
        valid = (page is not None and all(math.isfinite(x) for x in box)
                 and 0 <= box[0] < box[2] <= page["width"] and 0 <= box[1] < box[3] <= page["height"])
        if not valid:
            add("area_bounds", subject, "Obszar leży poza stroną albo ma pustą obwiednię.")
        return valid

    fragments = _fragments(package)
    index([f for p in pages.values() for f in p["fragments"]], "ref", "fragments")
    for number, page in pages.items():
        if not artifact(page["render"], {"render"}, number):
            add("asset_mismatch", str(number), "Render strony nie odpowiada manifestowi plików.")
        for fragment in page["fragments"]:
            bounds(number, fragment["bbox"], fragment["ref"])
            covered = Counter()
            for glyph in fragment["glyphs"]:
                if not 0 <= glyph["start"] < glyph["end"] <= len(fragment["text"]):
                    add("glyph_span", fragment["ref"], "Zakres glifu nie odpowiada surowemu tekstowi.")
                    continue
                bounds(number, glyph["bbox"], fragment["ref"])
                b, outer = glyph["bbox"], fragment["bbox"]
                if not (outer[0] <= b[0] < b[2] <= outer[2] and outer[1] <= b[1] < b[3] <= outer[3]):
                    add("glyph_bounds", fragment["ref"], "Glif leży poza obwiednią surowego fragmentu.")
                covered.update(range(glyph["start"], glyph["end"]))
            if any(covered[i] != 1 for i, char in enumerate(fragment["text"]) if not char.isspace()):
                add("glyph_span", fragment["ref"], "Glify nie pokrywają dokładnie widocznych znaków tekstu.")

    blocks = index(document["blocks"], "ref", "blocks")
    evidence = index(document["evidence"], "ref", "evidence")
    relations = index(document["relations"], "ref", "relations")
    coverage = index(document["coverage"], "ref", "coverage")
    subjects = {**blocks, **evidence, **relations, **coverage}
    if len(subjects) != len(blocks) + len(evidence) + len(relations) + len(coverage):
        add("duplicate_ref", "document", "Referencje różnych rodzajów muszą być rozłączne.")
    if set(document["reading_order"]) != set(blocks):
        add("reading_order", "document", "Kolejność czytania musi zawierać każdy blok dokładnie raz.")
    evidence_pages, evidence_chars = {}, {}
    for ref, item in evidence.items():
        numbers, chars = set(), set()
        if item["kind"] == "text_layer":
            span_chars = Counter()
            for span in item["spans"]:
                found = fragments.get(span["fragment"])
                if found is None:
                    add("unknown_fragment", ref, "Dowód wskazuje nieznany fragment tekstu.")
                    continue
                page, fragment = found
                numbers.add(page["pdf_page"])
                start, end = span["start"], span["end"]
                glyphs = fragment["glyphs"]
                if (not 0 <= start < end <= len(fragment["text"]) or not any(start <= g["start"] < g["end"] <= end for g in glyphs)
                        or any(g["start"] < end and start < g["end"] and not start <= g["start"] < g["end"] <= end for g in glyphs)):
                    add("text_span", ref, "Zakres tekstu jest pusty, nieprawidłowy albo przecina glif.")
                    continue
                selected = {(span["fragment"], i) for i in range(start, end) if not fragment["text"][i].isspace()}
                span_chars.update(selected)
                chars.update(selected)
            if any(n != 1 for n in span_chars.values()):
                add("text_overlap", ref, "Zakresy jednego dowodu powtarzają te same znaki.")
        else:
            numbers.add(item["pdf_page"])
            bounds(item["pdf_page"], item["bbox"], ref)
            if not artifact(item["image"], {"render", "crop"}, item["pdf_page"]):
                add("asset_mismatch", ref, "Dowód obrazowy nie wskazuje obrazu z manifestu.")
        evidence_pages[ref], evidence_chars[ref] = numbers, chars

    dependencies = {ref: set() for ref in subjects}

    def refs(owner, values, known):
        for value in values:
            if value not in known:
                add("unresolved_ref", owner, f"Brak celu referencji {value}.")
            else:
                dependencies[owner].add(value)

    for ref, block in blocks.items():
        refs(ref, block["evidence"], evidence)
        if any(not evidence_pages.get(e, set()) <= target for e in block["evidence"]):
            add("context_write", ref, "Blok zapisuje kontekst zamiast wyłącznie zakresu docelowego.")
        if "parent" in block:
            refs(ref, [block["parent"]], blocks)
        visited, current = {ref}, block.get("parent")
        while current in blocks:
            if current in visited:
                add("hierarchy_cycle", ref, "Hierarchia bloków zawiera cykl.")
                break
            visited.add(current)
            current = blocks[current].get("parent")
        if "table" in block:
            table, occupied = block["table"], Counter()
            refs(ref, table["notes"], blocks)
            for cell in table["cells"]:
                refs(ref, cell["evidence"], evidence)
                if not set(cell["evidence"]) <= set(block["evidence"]):
                    add("table_evidence", ref, "Dowód komórki musi należeć do dowodów tabeli.")
                occupied.update((r, c) for r in range(cell["row"], cell["row"] + cell["row_span"])
                                for c in range(cell["column"], cell["column"] + cell["column_span"]))
            if set(block["evidence"]) != {e for cell in table["cells"] for e in cell["evidence"]}:
                add("table_evidence", ref, "Komórki nie przypisują wszystkich dowodów tabeli.")
            expected = {(r, c) for r in range(table["rows"]) for c in range(table["columns"])}
            if set(occupied) != expected or any(n != 1 for n in occupied.values()):
                add("table_grid", ref, "Komórki i scalenia nie pokrywają dokładnie siatki tabeli.")
    order = {ref: i for i, ref in enumerate(document["reading_order"])}
    for ref, relation in relations.items():
        refs(ref, [relation["from"], relation["to"]], blocks)
        refs(ref, relation["evidence"], evidence)
        if relation["type"] in {"scope", "continuation"}:
            for b in (relation["from"], relation["to"]):
                if b in blocks:
                    dependencies[b].add(ref)
        if relation["type"] == "continuation" and order.get(relation["from"], -1) >= order.get(relation["to"], -1):
            add("continuation_order", ref, "Kontynuacja musi prowadzić do późniejszego bloku.")
        if relation["type"] == "scope" and not any(evidence.get(e, {}).get("kind") == "visual_scope" for e in relation["evidence"]):
            add("scope_evidence", ref, "Zakres ramki/koloru wymaga dowodu wizualnego.")

    counts, content_blocks = Counter(), set()
    for ref, region in coverage.items():
        bounds(region["pdf_page"], region["bbox"], ref)
        refs(ref, region["evidence"], evidence)
        refs(ref, region["blocks"], blocks)
        if region["classification"] == "gap":
            refs(ref, region["affects"], subjects)
            for affected in region["affects"]:
                if affected in subjects:
                    dependencies[affected].add(ref)
        if region["pdf_page"] not in target:
            add("context_write", ref, "Rozliczanie obszarów dotyczy wyłącznie zakresu docelowego.")
        if any(evidence_pages.get(e, set()) != {region["pdf_page"]} for e in region["evidence"]):
            add("coverage_page", ref, "Dowód rozliczenia musi należeć do wskazanej strony.")
        counts.update(ch for e in region["evidence"] for ch in evidence_chars.get(e, set()))
        if region["classification"] == "content":
            content_blocks.update(region["blocks"])
            for b in region["blocks"]:
                if b in blocks:
                    dependencies[b].add(ref)
                    if not set(blocks[b]["evidence"]) <= set(region["evidence"]):
                        add("coverage_evidence", ref, "Rozliczenie treści nie obejmuje dowodów wskazanego bloku.")
    expected = {(ref, i) for ref, (p, f) in fragments.items() if p["pdf_page"] in target
                for i, char in enumerate(f["text"]) if not char.isspace()}
    if set(counts) != expected or any(n != 1 for n in counts.values()):
        add("text_coverage", "document", "Tekst docelowy nie jest rozliczony dokładnie raz jako treść, wyłączenie lub luka.")
    if content_blocks != set(blocks):
        add("block_coverage", "document", "Każdy blok musi mieć jawne rozliczenie obszaru treści.")
    referenced = {value for values in dependencies.values() for value in values}
    if set(evidence) - referenced:
        add("unused_evidence", "document", "Dowód nie ma jawnego zastosowania w dokumencie.")

    if revision is not None:
        if revision.get("parent", {}).get("id") == revision["id"]:
            add("revision_parent", revision["id"], "Rewizja nie może być własnym rodzicem.")
        for change in revision.get("changes", []):
            if not set(change["after"]) <= set(subjects):
                add("change_map", revision["id"], "Nowe cele mapy zmian nie występują w dokumencie.")
        if revision["hash"] != envelope_hash(revision):
            add("revision_hash", revision["id"], "Hash rewizji nie odpowiada jej treści.")
        if (revision["package"] != binding or revision["response"]["hash"] != content_hash(response)
                or revision["document"]["hash"] != content_hash(document)):
            add("revision_mismatch", revision["id"], "Rewizja wskazuje inne wejścia lub artefakty.")
        reviews = index(revision["reviews"], "subject", "reviews")
        if set(reviews) != set(subjects):
            add("review_set", revision["id"], "Przegląd musi jawnie określać stan każdego elementu dokumentu.")
        approved = {r for r, review in reviews.items() if review["status"] == "approved"}
        render_hashes = {p["render"]["hash"] for p in pages.values()}
        if approved and revision["validation"] != "valid":
            add("review_validation", revision["id"], "Zatwierdzenie wymaga poprawnej walidacji strukturalnej.")
        for ref in approved:
            review = reviews[ref]
            reachable, pending = set(), [ref]
            while pending:
                current = pending.pop()
                if current in reachable:
                    continue
                reachable.add(current)
                pending.extend(dependencies.get(current, set()))
            numbers = {coverage[r]["pdf_page"] for r in reachable if r in coverage}
            numbers.update(n for r in reachable for n in evidence_pages.get(r, set()))
            required_renders = {pages[n]["render"]["hash"] for n in numbers if n in pages}
            basis_renders = set(review["basis"]["render_hashes"])
            if (review["basis"]["document_hash"] != content_hash(document) or not basis_renders <= render_hashes
                    or not required_renders <= basis_renders):
                add("review_basis", ref, "Przegląd nie dotyczy bieżącego dokumentu i renderów.")
            if not dependencies.get(ref, set()) <= approved:
                add("review_dependency", ref, "Zatwierdzony element ma niezatwierdzone zależności.")
            if ref in coverage and coverage[ref]["classification"] == "gap":
                add("review_gap", ref, "Otwarta luka nie może być zatwierdzonym dowodem.")
        if revision["completeness"] == "complete" and (revision["validation"] != "valid" or approved != set(subjects)
                or target != set(range(1, package["source"]["page_count"] + 1))
                or any(r["classification"] == "gap" for r in coverage.values())):
            add("incomplete", revision["id"], "Pełna kompletność wymaga wszystkich stron i zatwierdzonych elementów bez luk.")
    return issues
