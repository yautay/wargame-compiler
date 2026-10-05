"""Knowledge Base of a game repo: reading the workspace and `accept()`, the only path that writes `kb/` (ADR-0025).

`Workspace` reads what tasks need: the Stage 0 inventory, segment text from `.glu/source/` (checked against
`text_hash`) and the records already in `kb/`. `accept()` turns task proposals into KB records:

1. checks types and shape of the proposals and each record against the contract without the WGC-owned fields
   (pure checks, before any domain function: wrong data gives diagnostics, never a `TypeError`);
2. takes the KB writer lock of the project (`.glu/kb.lock`, ADR-0026) and checks that the inventory has not changed
   since the `Workspace` read it; steps 3–7 run under the lock on KB read afresh from disk;
3. the task's own domain rules (`TaskSpec.validate`);
4. adds `status: accepted` and `prov`: the kind is decided here, never by the executor (ADR-0014); `by` comes from
   the caller (GLU: tier, tool or profile), `inputs_hash` is the hash of the `logic` projections of the inputs;
5. merges with `kb/`: an equal record (ignoring `prov.job` and `prov.at`) is left untouched, a record of the same
   task is replaced, a record of another producer with the same ID is a conflict;
6. validates the whole KB with the inventory in memory (`wgc.validate.validate_documents`);
7. writes only when there are no issues and something changed, each file by atomic replacement (`wgc.fsio`).

Outcomes: rejected data → `AcceptResult.issues` (nothing written); operational failure (unreadable input, busy lock,
stale workspace, failed write) → `KBError` and its subclasses; any other exception is a program error and propagates.
A failed write keeps the previous content of that file, but files replaced before it in the same acceptance stay
replaced: there is no multi-file commit yet (ADR-0026).

Layout: `kb/logic/<kind plural>.yaml` (`tables.yaml`, `concepts.yaml`, …), one `wgc/logic@0` document per file,
records sorted by ID (numbers in natural order), fields in contract order, LF. A record found in another file of
`kb/` stays in that file. Files are rewritten whole: comments are not kept.
"""
from __future__ import annotations

import contextlib
import copy
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import yaml

from wgc import contracts, fsio, source
from wgc.canonical import canonical_json, content_hash, normalize_text, projection, sha256_hex, text_hash
from wgc.ids import is_id
from wgc.tasks import Inputs, TaskSpec
from wgc.validate import ERROR, load_documents, validate_documents

KB_DIR = Path("kb")
# KB writer lock of a game repo; `.glu/` is local state (gitignored), so the lock never shows up in `kb/` or in git.
LOCK_FILE = Path(".glu") / "kb.lock"
LOCK_TIMEOUT = 60.0  # seconds `accept()` waits for the lock before `KBBusy`
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
    """Operational error: missing inventory or segment text, unreadable KB, busy lock, failed write (message in
    Polish). Never a rejection of the proposals: those are `AcceptResult.issues`."""


class KBBusy(KBError):
    """Another process or thread holds the KB writer lock for longer than the timeout."""


class KBStale(KBError):
    """The inventory changed after the `Workspace` read it: a result computed from the old state is not written."""


class KBWriteError(KBError):
    """Writing a file of `kb/` failed. That file keeps its previous content; the message names the files already
    replaced by the same acceptance."""


# --- workspace ------------------------------------------------------------------------------------------------------

class Workspace:
    """Read-only view of a game repo for tasks: inventory, segment text and KB records.

    The inventory is read once (with its fingerprint `inventory_hash`); KB records are read from disk on every call,
    so a long-lived workspace never serves an old KB snapshot."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        path = source.inventory_path(self.root)
        try:
            # fingerprint first: a change after this point makes `accept()` stop with KBStale
            self.inventory_hash = sha256_hex(path.read_bytes()) if path.is_file() else None
            self.inventory = source.read_inventory(self.root)
        except source.SourceError as e:
            raise KBError(str(e)) from None
        except OSError as e:
            raise KBError(f"Nie można wczytać {path.as_posix()}: {e}") from None
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


def _label(value) -> str:
    return value if isinstance(value, str) else repr(value)


def _is_span(span) -> bool:
    """`[start, end]`: two non-negative integers (not booleans), start ≤ end."""
    return (isinstance(span, list) and len(span) == 2 and all(type(n) is int and n >= 0 for n in span)
            and span[0] <= span[1])


def _anchor_issues(anchors) -> list[str]:
    if not isinstance(anchors, list) or not all(isinstance(a, dict) for a in anchors):
        return ["`anchors` musi być listą obiektów {seg, quote?, span?}."]
    out = []
    for i, a in enumerate(anchors, 1):
        if set(a) - {"seg", "quote", "span"}:
            out.append(f"kotwica {i}: propozycja ma tylko pola seg, quote, span (seg_hash dopisuje WGC).")
        if not is_id(a.get("seg")):
            out.append(f"kotwica {i}: `seg` musi być ID segmentu (napis), jest {a.get('seg')!r}.")
        if "quote" in a and not isinstance(a["quote"], str):
            out.append(f"kotwica {i}: `quote` musi być napisem, jest {a['quote']!r}.")
        if "span" in a and not _is_span(a["span"]):
            out.append(f"kotwica {i}: `span` musi być parą liczb całkowitych [początek, koniec] z 0 ≤ początek ≤ koniec, "
                       f"jest {a['span']!r}.")
    return out


def _shape_issues(spec: TaskSpec, proposals) -> list[str]:
    """Types and shape of the proposals, before anything uses their values (no domain function, no I/O)."""
    if not isinstance(proposals, list):
        return [f"wynik zadania musi być listą propozycji, jest {type(proposals).__name__}."]
    issues = []
    seen = set()
    for n, p in enumerate(proposals, 1):
        where = f"propozycja {n}"
        if not isinstance(p, dict) or not isinstance(p.get("record"), dict):
            issues.append(f"{where}: oczekiwano obiektu z polem `record` (obiekt).")
            continue
        extra = sorted(map(str, set(p) - {"record", "anchors", "derived_from"}))
        if extra:
            issues.append(f"{where}: nieznane pola propozycji: {', '.join(extra)}.")
        rec = p["record"]
        rid = rec.get("id")
        if is_id(rid):
            where = f"{where} ({rid})"
            if rid in seen:
                issues.append(f"{where}: ID powtarza się w wyniku zadania.")
            seen.add(rid)
        else:
            issues.append(f"{where}: `record.id` musi być ID w postaci PREFIKS-klucz (napis), jest {rid!r}.")
        if rec.get("kind") != spec.output_kind:
            issues.append(f"{where}: rodzaj `{_label(rec.get('kind'))}`, zadanie {spec.name} daje `{spec.output_kind}`.")
        reserved = [f for f in RESERVED if f in rec]
        if reserved:
            issues.append(f"{where}: pola {', '.join(reserved)} nadaje WGC, nie wykonawca (ADR-0014).")
        anchors, derived = p.get("anchors", []), p.get("derived_from", [])
        issues += [f"{where}: {m}" for m in _anchor_issues(anchors)]
        if not isinstance(derived, list) or not all(is_id(d) for d in derived):
            issues.append(f"{where}: `derived_from` musi być listą ID (napisów), jest {derived!r}.")
        if not anchors and not derived:
            issues.append(f"{where}: brak kotwic i `derived_from`: nie da się ustalić provenance.")
    return issues


# Schema errors that only say a WGC-owned field is missing: `accept()` adds those fields later.
_RESERVED_MISSING = {f"{f!r} is a required property" for f in RESERVED}


def _record_schema_issues(spec: TaskSpec, proposals: list[dict]) -> list[str]:
    """Each proposed record against `wgc/logic@0` before provenance exists, so domain functions get typed data."""
    validator = contracts.validator(LOGIC)
    out = []
    for n, p in enumerate(proposals, 1):
        rec = p["record"]
        errs = sorted(validator.iter_errors({"schema": LOGIC, "records": [rec]}), key=lambda e: list(e.absolute_path))
        for e in errs:
            if e.validator == "required" and e.message in _RESERVED_MISSING:
                continue
            loc = "/".join(map(str, list(e.absolute_path)[2:])) or "<rekord>"
            out.append(f"propozycja {n} ({rec['id']}): niezgodność ze schematem {spec.output_schema}: {loc}: "
                       f"{e.message[:300]}")
    return out


def _provenance(ws: Workspace, proposal: dict, by: dict, job: str | None,
                kb_records: dict[str, dict]) -> tuple[dict | None, list[str]]:
    """`prov` of an accepted record (ADR-0014) or the reasons why it cannot be given. `kb_records` is the KB read
    under the writer lock: `derived_from` resolves against it, never against an older snapshot."""
    rid = proposal["record"]["id"]
    issues = []
    anchors, kinds, inputs = [], set(), []
    for a in proposal.get("anchors") or []:
        seg = ws.segment(a["seg"])
        if seg is None:
            issues.append(f"{rid}: kotwica wskazuje segment `{a['seg']}`, którego nie ma w inwentarzu.")
            continue
        quote, span = a.get("quote"), a.get("span")
        text = normalize_text(ws.text(a["seg"])) if quote is not None or span is not None else ""
        if quote is not None and normalize_text(quote) not in text:
            issues.append(f"{rid}: cytat {quote!r} nie występuje dosłownie w segmencie {a['seg']}.")
            continue
        if span is not None and span[1] > len(text):
            issues.append(f"{rid}: `span` {span} wykracza poza znormalizowany tekst segmentu {a['seg']} "
                          f"(długość {len(text)}).")
            continue
        anchors.append({"seg": a["seg"], "seg_hash": seg["text_hash"],
                        **{k: a[k] for k in ("span", "quote") if k in a}})
        kinds.add(ROLE_KINDS.get((ws.document(seg["doc"]) or {}).get("role"), "explicit_source"))
        inputs.append(projection(seg, "logic"))
    derived = list(proposal.get("derived_from") or [])
    for d in derived:
        rec = ws.segment(d) or kb_records.get(d)
        if rec is None:
            issues.append(f"{rid}: brak rekordu `{d}` (derived_from) w inwentarzu ani w kb/.")
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


@contextlib.contextmanager
def lock(root: str | Path, timeout: float | None = None) -> Iterator[None]:
    """The KB writer lock of a game repo (`.glu/kb.lock`, ADR-0026), between processes and threads. Busy for longer
    than `timeout` seconds → `KBBusy`."""
    path = Path(root) / LOCK_FILE
    timeout = LOCK_TIMEOUT if timeout is None else timeout
    with contextlib.ExitStack() as stack:
        try:
            stack.enter_context(fsio.exclusive(path, timeout))
        except fsio.LockBusy:
            raise KBBusy(f"kb/ jest zajęte: inny proces albo wątek trzyma blokadę zapisu {path.as_posix()} dłużej niż "
                         f"{timeout:g} s. Poczekaj na koniec tamtego buildu i ponów.") from None
        except OSError as e:
            raise KBError(f"Nie można założyć blokady zapisu {path.as_posix()}: {e}") from None
        yield


def _inventory_under_lock(ws: Workspace) -> dict:
    """The inventory document on disk, if it is the one the workspace was built from (else KBStale)."""
    path = source.inventory_path(ws.root)
    try:
        data = path.read_bytes()
    except OSError as e:
        raise KBError(f"Nie można wczytać {path.as_posix()}: {e}") from None
    if sha256_hex(data) != ws.inventory_hash:
        raise KBStale(f"Inwentarz {path.relative_to(ws.root).as_posix()} zmienił się po odczycie przez to zadanie "
                      "(np. `wgc source extract` w trakcie buildu). Wynik obliczony ze starego stanu nie został "
                      "zapisany: ponów build.")
    return [d for d in yaml.safe_load_all(data.decode("utf-8")) if d is not None][0]


def accept(root: str | Path, spec: TaskSpec, inputs: Inputs, proposals: list, *, by: dict,
           job: str | None = None, ws: Workspace | None = None, lock_timeout: float | None = None) -> AcceptResult:
    """Accept the proposals of one job into `kb/` (the only writer of KB YAML). See the module docstring.
    `lock_timeout`: seconds to wait for the KB writer lock (default `LOCK_TIMEOUT`), then `KBBusy`."""
    ws = ws or Workspace(root)
    root = ws.root
    res = AcceptResult(records=[p["record"]["id"] for p in proposals if isinstance(p, dict)
                                and isinstance(p.get("record"), dict) and isinstance(p["record"].get("id"), str)]
                       if isinstance(proposals, list) else [])
    # pure checks first: nothing below sees wrong types, and rejected data never waits for the lock
    issues = _shape_issues(spec, proposals) or _record_schema_issues(spec, proposals)
    if issues:
        res.schema_valid, res.issues = False, issues
        return res
    # one writer per project: read KB, merge, validate and write as one critical section (ADR-0026)
    with lock(root, LOCK_TIMEOUT if lock_timeout is None else lock_timeout):
        inventory = _inventory_under_lock(ws)
        return _accept_locked(ws, spec, inputs, proposals, by, job, inventory, res)


def _accept_locked(ws: Workspace, spec: TaskSpec, inputs: Inputs, proposals: list[dict], by: dict,
                   job: str | None, inventory: dict, res: AcceptResult) -> AcceptResult:
    root = ws.root
    docs = ws.kb_documents()  # read now, under the lock
    kb_records = {r["id"]: r for _, doc in docs for r in _records(doc) if isinstance(r.get("id"), str)}
    domain = list(spec.validate(ws, inputs, proposals))

    # records with provenance, each checked against the contract on its own
    new: list[dict] = []
    for p in proposals:
        prov, errs = _provenance(ws, p, by, job, kb_records)
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

    # the whole KB with the inventory checked under the lock must stay valid
    report = validate_documents([(source.inventory_path(root).relative_to(root).as_posix(), inventory)]
                                + [(p.relative_to(root).as_posix(), d) for p, d in docs])
    errors = [d for d in report.diagnostics if d.severity == ERROR]
    if errors:
        res.domain_valid = False
        res.issues += [f"{d.code} {d.subject}: {d.message}" for d in errors]
        return res

    # write the changed files, each by atomic replacement
    files = sorted({docs[i][0] for i in changed})
    if files:
        _remove_orphan_temps(root / KB_DIR)
    for path in files:
        file_docs = [d for p, d in docs if p == path]
        for d in file_docs:
            if isinstance(d, dict) and d.get("schema") == LOGIC:
                d["records"] = sorted((ordered(r) for r in d["records"]), key=lambda r: _natural(r.get("id", "")))
        rel = path.relative_to(root).as_posix()
        try:
            _write_file(path, dump(file_docs))
        except OSError as e:
            done = (f" Pliki już podmienione w tej akceptacji: {', '.join(res.files)}. kb/ zawiera część wyniku: ponów "
                    "build; jeśli walidacja całego kb/ odrzuci ten stan częściowy, przywróć te pliki z git."
                    if res.files else " Niczego nie zapisano.")
            raise KBWriteError(f"Nie można zapisać {rel}: {e}. Ten plik ma poprzednią zawartość (zapis atomowy)."
                               + done) from e
        res.files.append(rel)
    return res


def _remove_orphan_temps(kb_dir: Path) -> None:
    """Temporary files of an interrupted earlier write (the writer lock is held, so no write is in progress)."""
    for tmp in fsio.temp_files(kb_dir):
        try:
            tmp.unlink()
        except OSError:
            pass


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
    """The only place that writes a file of `kb/` (tests replace it to prove that). Atomic replacement: a failure
    leaves the previous content (ADR-0026)."""
    fsio.atomic_write(path, text.encode("utf-8"))
