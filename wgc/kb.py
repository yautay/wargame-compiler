"""Knowledge Base of a game repo: reading the workspace and `accept()`, the only path that writes `kb/` (ADR-0025).

`Workspace` reads what tasks need: the Stage 0 inventory, segment text from `.glu/source/` (checked against
`text_hash`) and the records already in `kb/`. `accept()` turns task proposals into KB records:

1. checks the proposal shape and the task's own domain rules (`TaskSpec.validate`);
2. adds `status: accepted` and `prov`: the kind is decided here, never by the executor (ADR-0014); `by` comes from
   the caller (GLU: tier, tool or profile), `inputs_hash` is the hash of the `logic` projections of the inputs;
3. merges with `kb/`: an equal record (ignoring `prov.job` and `prov.at`) is left untouched, a record of the same
   task is replaced, a record of another producer with the same ID is a conflict;
4. validates the whole KB with the inventory in memory (`wgc.validate.validate_documents`);
5. writes only when there are no issues and something changed.

Layout: `kb/logic/<kind plural>.yaml` (`tables.yaml`, `concepts.yaml`, …), one `wgc/logic@0` document per file,
records sorted by ID (numbers in natural order), fields in contract order, LF. A record found in another file of
`kb/` stays in that file. Files are rewritten whole: comments are not kept.
"""
from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from wgc import contracts, source
from wgc.canonical import canonical_json, content_hash, normalize_text, projection, text_hash
from wgc.tasks import Inputs, TaskSpec
from wgc.validate import ERROR, load_documents, validate_documents

KB_DIR = Path("kb")
LOGIC = "wgc/logic@0"
# Record kind → file under kb/logic/ (human decisions and review requests have their own files, outside accept()).
KIND_FILES = {"concept": "concepts.yaml", "rule": "rules.yaml", "relation": "relations.yaml", "table": "tables.yaml",
              "procedure": "procedures.yaml", "ambiguity": "ambiguities.yaml",
              "interpretation": "interpretations.yaml", "case": "cases.yaml", "change": "changes.yaml"}
# Proposal fields set by WGC, never by the executor (ADR-0014).
RESERVED = ("prov", "status", "risk")
# `prov` fields that do not make two records different (who accepted it and when, not what it says).
VOLATILE_PROV = ("job", "at")
# Source role → provenance kind of an anchored record (ADR-0014).
ROLE_KINDS = {"errata": "errata", "faq": "faq", "designer_clarification": "designer_clarification"}

HEADER = """\
# wgc/logic@0: rekordy KB zapisuje wyłącznie `wgc.kb.accept()` (ADR-0025). Komentarze nie są zachowywane.
"""


class KBError(Exception):
    """Operational error: missing inventory or segment text, unreadable KB (message in Polish)."""


# --- workspace ------------------------------------------------------------------------------------------------------

class Workspace:
    """Read-only view of a game repo for tasks: inventory, segment text and KB records."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        try:
            self.inventory = source.read_inventory(self.root)
        except source.SourceError as e:
            raise KBError(str(e)) from None
        self._documents = {d["id"]: d for d in self.inventory.documents}
        self._segments = {s["id"]: s for s in self.inventory.segments}
        self._text: dict[str, str] = {}

    def document(self, doc_id: str) -> dict | None:
        return self._documents.get(doc_id)

    def segment(self, seg_id: str) -> dict | None:
        return self._segments.get(seg_id)

    def record(self, record_id: str) -> dict:
        """A segment of the inventory or a record of `kb/`."""
        rec = self._segments.get(record_id)
        if rec is None:
            rec = next((r for _, doc in self.kb_documents() for r in _records(doc) if r.get("id") == record_id), None)
        if rec is None:
            raise KBError(f"Brak rekordu `{record_id}` w inwentarzu ani w kb/.")
        return rec

    def text(self, seg_id: str) -> str:
        """Extracted text of a segment from `.glu/source/`, checked against its `text_hash`."""
        if seg_id in self._text:
            return self._text[seg_id]
        seg = self._segments.get(seg_id)
        if seg is None:
            raise KBError(f"Segmentu `{seg_id}` nie ma w inwentarzu.")
        path = source.cache_dir(self.root, seg["doc"]) / f"{seg_id}.txt"
        if not path.is_file():
            raise KBError(f"Brak tekstu segmentu {seg_id} ({path.as_posix()}): uruchom `wgc source extract`.")
        text = path.read_text(encoding="utf-8")
        if text_hash(text) != seg.get("text_hash"):
            raise KBError(f"Tekst segmentu {seg_id} w {path.as_posix()} nie zgadza się z `text_hash` inwentarza: "
                          "uruchom `wgc source extract`.")
        self._text[seg_id] = text
        return text

    def kb_files(self) -> list[Path]:
        kb = self.root / KB_DIR
        return sorted(p for p in kb.rglob("*") if p.suffix in (".yaml", ".yml") and p.is_file()) if kb.is_dir() else []

    def kb_documents(self) -> list[tuple[Path, object]]:
        """(file, document) for every document of `kb/` (several per file allowed, ADR-0019)."""
        out = []
        for path in self.kb_files():
            try:
                docs = load_documents(path)
            except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
                raise KBError(f"Nie można wczytać {path.as_posix()}: {e}") from None
            out += [(path, d) for d in docs]
        return out


def _records(doc) -> list[dict]:
    if isinstance(doc, dict) and isinstance(doc.get("records"), list):
        return [r for r in doc["records"] if isinstance(r, dict)]
    return []


# --- accept ---------------------------------------------------------------------------------------------------------

@dataclass
class AcceptResult:
    records: list[str] = field(default_factory=list)    # ids of the proposed records, in proposal order
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)      # written files, relative to the root (POSIX)
    schema_valid: bool = True
    domain_valid: bool = True
    issues: list[str] = field(default_factory=list)     # Polish messages; non-empty → nothing written

    @property
    def ok(self) -> bool:
        return not self.issues


def _fields(defn: str) -> list[str]:
    """Property order of a `wgc/logic@0` definition, or of `provenance` from the common schema."""
    if defn == "provenance":
        common = contracts.registry().contents(contracts.BASE_URI + "common.schema.json")
        return list(common["$defs"]["provenance"]["properties"])
    return list(contracts.schema_for(LOGIC)["$defs"][defn]["properties"])


def ordered(record: dict) -> dict:
    """Record with fields in contract order (unknown fields last), `prov` too."""
    kind = record.get("kind")
    order = _fields(kind) if kind in KIND_FILES else []
    out = {f: record[f] for f in order if f in record}
    out.update({k: v for k, v in record.items() if k not in out})
    if isinstance(out.get("prov"), dict):
        prov = out["prov"]
        porder = _fields("provenance")
        out["prov"] = {**{f: prov[f] for f in porder if f in prov}, **{k: v for k, v in prov.items() if k not in porder}}
    return out


def _comparable(record: dict) -> bytes:
    rec = copy.deepcopy(record)
    if isinstance(rec.get("prov"), dict):
        for f in VOLATILE_PROV:
            rec["prov"].pop(f, None)
    return canonical_json(rec)


def _producer(record: dict) -> str | None:
    """Task or tool id (without version) that produced the record, from `prov.by.tool` or `prov.by.prompt`."""
    by = (record.get("prov") or {}).get("by") or {}
    name = by.get("tool") or by.get("prompt")
    return name.split("@", 1)[0] if isinstance(name, str) else None


def _shape_issues(spec: TaskSpec, proposals: list) -> list[str]:
    issues = []
    seen = set()
    for n, p in enumerate(proposals, 1):
        where = f"propozycja {n}"
        if not isinstance(p, dict) or not isinstance(p.get("record"), dict):
            issues.append(f"{where}: oczekiwano obiektu z polem `record`.")
            continue
        extra = sorted(set(p) - {"record", "anchors", "derived_from"})
        if extra:
            issues.append(f"{where}: nieznane pola propozycji: {', '.join(extra)}.")
        rec = p["record"]
        rid = rec.get("id")
        if rec.get("kind") != spec.output_kind:
            issues.append(f"{where} ({rid}): rodzaj `{rec.get('kind')}`, zadanie {spec.name} daje `{spec.output_kind}`.")
        reserved = [f for f in RESERVED if f in rec]
        if reserved:
            issues.append(f"{where} ({rid}): pola {', '.join(reserved)} nadaje WGC, nie wykonawca (ADR-0014).")
        if rid in seen:
            issues.append(f"{where}: ID `{rid}` powtarza się w wyniku zadania.")
        seen.add(rid)
        anchors, derived = p.get("anchors") or [], p.get("derived_from") or []
        if not isinstance(anchors, list) or not all(isinstance(a, dict) and isinstance(a.get("seg"), str) for a in anchors):
            issues.append(f"{where} ({rid}): `anchors` musi być listą obiektów z polem `seg`.")
        elif any(set(a) - {"seg", "quote", "span"} for a in anchors):
            issues.append(f"{where} ({rid}): kotwica propozycji ma tylko pola seg, quote, span (seg_hash dopisuje WGC).")
        if not isinstance(derived, list) or not all(isinstance(d, str) for d in derived):
            issues.append(f"{where} ({rid}): `derived_from` musi być listą ID.")
        if not anchors and not derived:
            issues.append(f"{where} ({rid}): brak kotwic i `derived_from`: nie da się ustalić provenance.")
    return issues


def _provenance(ws: Workspace, proposal: dict, by: dict, job: str | None) -> tuple[dict | None, list[str]]:
    """`prov` of an accepted record (ADR-0014) or the reasons why it cannot be given."""
    rid = proposal["record"].get("id")
    issues = []
    anchors, kinds, inputs = [], set(), []
    for a in proposal.get("anchors") or []:
        seg = ws.segment(a["seg"])
        if seg is None:
            issues.append(f"{rid}: kotwica wskazuje segment `{a['seg']}`, którego nie ma w inwentarzu.")
            continue
        quote = a.get("quote")
        if quote is not None and normalize_text(quote) not in normalize_text(ws.text(a["seg"])):
            issues.append(f"{rid}: cytat {quote!r} nie występuje dosłownie w segmencie {a['seg']}.")
            continue
        anchors.append({"seg": a["seg"], "seg_hash": seg["text_hash"],
                        **{k: a[k] for k in ("span", "quote") if k in a}})
        kinds.add(ROLE_KINDS.get((ws.document(seg["doc"]) or {}).get("role"), "explicit_source"))
        inputs.append(projection(seg, "logic"))
    derived = list(proposal.get("derived_from") or [])
    for d in derived:
        try:
            rec = ws.record(d)
        except KBError as e:
            issues.append(f"{rid}: {e}")
            continue
        try:
            inputs.append(projection(rec, "logic"))
        except KeyError:  # kinds without a semantic projection: the record without WGC-owned fields
            inputs.append({k: v for k, v in rec.items() if k not in (*RESERVED, "notes")})
    if len(kinds) > 1:
        issues.append(f"{rid}: kotwice wskazują źródła o różnych rolach ({', '.join(sorted(kinds))}).")
    if issues:
        return None, issues
    if anchors:
        kind = kinds.pop()
    elif by.get("tier") == "deterministic":
        kind = "deterministic_derivation"
    elif by.get("tier") in ("local", "premium"):
        kind = "llm_inference"
    else:
        return None, [f"{rid}: wykonawca `{by.get('tier')}` bez kotwic nie daje provenance (wymaga HD-)."]
    prov = {"kind": kind, **({"anchors": anchors} if anchors else {}), **({"derived_from": derived} if derived else {}),
            "by": dict(by), **({"job": job} if job else {}), "inputs_hash": content_hash(inputs)}
    return prov, []


def _natural(record_id: str) -> list:
    return [(0, int(t), "") if t.isdigit() else (1, 0, t) for t in re.findall(r"\d+|\D+", record_id)]


def accept(root: str | Path, spec: TaskSpec, inputs: Inputs, proposals: list, *, by: dict,
           job: str | None = None, ws: Workspace | None = None) -> AcceptResult:
    """Accept the proposals of one job into `kb/` (the only writer of KB YAML). See the module docstring."""
    ws = ws or Workspace(root)
    root = ws.root
    res = AcceptResult(records=[p["record"].get("id") for p in proposals
                                if isinstance(p, dict) and isinstance(p.get("record"), dict)])
    issues = _shape_issues(spec, proposals)
    if issues:
        res.schema_valid, res.issues = False, issues
        return res
    domain = list(spec.validate(ws, inputs, proposals))

    # records with provenance, each checked against the contract on its own
    new: list[dict] = []
    for p in proposals:
        prov, errs = _provenance(ws, p, by, job)
        domain += errs
        if prov is None:
            continue
        rec = ordered({**p["record"], "status": "accepted", "prov": prov})
        schema_errs = contracts.errors({"schema": LOGIC, "records": [rec]})
        if schema_errs:
            res.schema_valid = False
            res.issues += [f"{rec['id']}: niezgodność ze schematem {spec.output_schema}: {e}" for e in schema_errs]
        new.append(rec)
    if res.issues or domain:
        res.domain_valid = not domain
        res.issues += domain
        return res

    # merge into the documents of kb/
    docs = [(path, copy.deepcopy(doc)) for path, doc in ws.kb_documents()]
    where = {r["id"]: (i, r) for i, (_, doc) in enumerate(docs) for r in _records(doc) if isinstance(r.get("id"), str)}
    changed: set[int] = set()
    for rec in new:
        rid = rec["id"]
        if rid in where:
            i, old = where[rid]
            if _comparable(old) == _comparable(rec):
                res.unchanged.append(rid)
                continue
            if old.get("status") != "accepted" or _producer(old) != spec.id:
                res.issues.append(f"{rid}: konflikt z rekordem w {docs[i][0].relative_to(root).as_posix()} "
                                  f"(producent `{_producer(old)}`, status `{old.get('status')}`); zadanie {spec.name} "
                                  "nie nadpisuje cudzych rekordów.")
                continue
            recs = docs[i][1]["records"]
            recs[recs.index(old)] = rec
            res.updated.append(rid)
        else:
            path = root / KB_DIR / "logic" / KIND_FILES[rec["kind"]]
            i = next((n for n, (p, d) in enumerate(docs) if p == path and isinstance(d, dict)
                      and d.get("schema") == LOGIC), None)
            if i is None:
                docs.append((path, {"schema": LOGIC, "records": []}))
                i = len(docs) - 1
            docs[i][1]["records"].append(rec)
            res.created.append(rid)
        changed.add(i)
    if res.issues:
        res.domain_valid = False
        return res

    # the whole KB with the inventory must stay valid
    inventory = source.inventory_path(root)
    report = validate_documents([(inventory.relative_to(root).as_posix(), load_documents(inventory)[0])]
                                + [(p.relative_to(root).as_posix(), d) for p, d in docs])
    errors = [d for d in report.diagnostics if d.severity == ERROR]
    if errors:
        res.domain_valid = False
        res.issues += [f"{d.code} {d.subject}: {d.message}" for d in errors]
        return res

    # write the changed files
    files = sorted({docs[i][0] for i in changed})
    for path in files:
        file_docs = [d for p, d in docs if p == path]
        for d in file_docs:
            if isinstance(d, dict) and d.get("schema") == LOGIC:
                d["records"] = sorted((ordered(r) for r in d["records"]), key=lambda r: _natural(r.get("id", "")))
        _write_file(path, dump(file_docs))
        res.files.append(path.relative_to(root).as_posix())
    return res


# --- serialization --------------------------------------------------------------------------------------------------

FLOW_WIDTH = 120  # a record whose flow form fits in this many characters is written on one line


def _flow(value: dict) -> str:
    return yaml.safe_dump(value, default_flow_style=True, allow_unicode=True, sort_keys=False,
                          width=1_000_000).strip()


def _dump_record(rec: dict) -> list[str]:
    """`- {…}` on one line when short (as in the inventory), else one `key: <flow value>` line per field."""
    line = f"  - {_flow(rec)}"
    if len(line) <= FLOW_WIDTH:
        return [line]
    fields = [_flow({k: v})[1:-1] for k, v in rec.items()]
    return [f"  - {fields[0]}"] + [f"    {f}" for f in fields[1:]]


def dump(documents: list) -> str:
    """Deterministic YAML of KB documents (fields in the given order, LF); other documents in PyYAML block style."""
    parts = []
    for d in documents:
        if isinstance(d, dict) and set(d) == {"schema", "records"} and all(isinstance(r, dict) for r in d["records"]):
            lines = [f"schema: {d['schema']}", "records:" if d["records"] else "records: []"]
            parts.append("\n".join(lines + [x for r in d["records"] for x in _dump_record(r)]) + "\n")
        else:
            parts.append(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=120))
    return HEADER + "---\n".join(parts)


def _write_file(path: Path, text: str) -> None:
    """The only place that writes a file of `kb/` (tests replace it to prove that)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)
