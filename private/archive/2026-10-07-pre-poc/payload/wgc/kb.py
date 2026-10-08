"""Knowledge Base of a game repo: reading the workspace and `accept()`, the only path that writes `kb/` (ADR-0025).

`Workspace` reads what tasks need: the Stage 0 inventory, segment text from `.glu/source/` (checked against
`text_hash` and `struct_hash`, ADR-0032) and the records already in `kb/`. `accept()` turns task proposals into KB records:

1. checks the `wgc/proposal@0` envelope, proposal shapes and each record against its stage contract without WGC-owned fields
   (pure checks, before any domain function: wrong data gives diagnostics, never a `TypeError`);
2. takes the KB writer lock of the project (`.glu/kb.lock`, ADR-0026) and checks that the inventory has not changed
   since the `Workspace` read it; steps 3–7 run under the lock on KB read afresh from disk (one snapshot). The job
   manifest (`wgc.manifest`, ADR-0033) is checked against that snapshot first: a task reading `kb/` whose context
   changed since its execution gets `KBContextStale`;
3. the task's own domain rules (`TaskSpec.validate`);
4. adds `status: accepted` and `prov`: the kind is decided here, never by the executor (ADR-0014); `by` comes from
   the caller (GLU: tier, tool or profile); `manifest` is what the job read; `inputs_hash` is the hash of the record's
   own evidence (the `logic` projections of its anchor segments and `derived_from` records, with the projection
   version), and that evidence must be among what the job read;
5. reconciles the complete output set of `task + logical input scope` with `kb/`: equal records stay untouched,
   missing outputs are retired, and records owned by another scope or edited outside the owner are protected;
6. validates the whole KB with the inventory in memory (`wgc.validate.validate_documents`);
7. writes only when there are no issues: first the receipt `.glu/kb-receipts/<job>.json` (when `job` is given),
   then the changed records and `wgc/outputs@0` owner manifest as one batch with an undo journal in
   `kb/.wgc-batch/` (`wgc.fsbatch`, ADR-0031).

Before step 3, under the lock, an interrupted batch is recovered (`recover`), so a result is never merged into a
partial `kb/`.

Outcomes: rejected data → `AcceptResult.issues` (nothing written); operational failure (unreadable input, busy lock,
stale workspace, failed write, undecidable interrupted batch) → `KBError` and its subclasses; any other exception is
a program error and propagates. A failed write normally leaves `kb/` as it was (`KBWriteError`: one file is replaced
atomically, a batch is rolled back at once). When the rollback of a batch does not complete, the result is not
decided yet: `KBUnresolved`, the journal and the receipt stay, and recovery plus reconcile decide (ADR-0031).

Layout: `kb/logic/<kind plural>.yaml` or `kb/digital/<kind plural>.yaml`, one stage document per file,
plus `kb/outputs/<owner hash>.yaml`. Records are sorted by ID (numbers in natural order), fields in contract order,
LF. A record found in another file of `kb/` stays in that file. Files are rewritten whole: comments are not kept.
"""
from __future__ import annotations

import contextlib
import copy
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import yaml

from wgc import contracts, fsbatch, fsio, manifest as manifests, ownership, source
from wgc.canonical import (PROJECTION_VERSION, ProjectionError, canonical_json, content_hash, normalize_text,
                           projection, sha256_hex, struct_hash, text_hash)
from wgc.ids import is_id
from wgc.manifest import Manifest
from wgc.tasks import Inputs, TaskSpec
from wgc.validate import ERROR, load_documents, validate_documents

KB_DIR = Path("kb")
# KB writer lock of a game repo; `.glu/` is local state (gitignored), so the lock never shows up in `kb/` or in git.
LOCK_FILE = Path(".glu") / "kb.lock"
LOCK_TIMEOUT = 60.0  # seconds `accept()` waits for the lock before `KBBusy`
# Undo journal of a multi-file acceptance (ADR-0031). Inside kb/, so losing .glu/ never hides a partial kb/.
BATCH_DIR = KB_DIR / ".wgc-batch"
# Receipts of acceptances, one per job, until GLU has recorded the Attempt (ADR-0031).
RECEIPTS_DIR = Path(".glu") / "kb-receipts"
LOGIC = "wgc/logic@0"
DIGITAL = "wgc/digital@0"
# Record kind → file under kb/logic/ (human decisions and review requests have their own files, outside accept()).
KIND_FILES = {"concept": "concepts.yaml", "rule": "rules.yaml", "relation": "relations.yaml", "table": "tables.yaml",
              "procedure": "procedures.yaml", "ambiguity": "ambiguities.yaml",
              "interpretation": "interpretations.yaml", "case": "cases.yaml", "change": "changes.yaml"}
DIGITAL_FILES = {kind: ("entities" if kind == "entity" else "priorities" if kind == "priority" else
                        "legalities" if kind == "legality" else f"{kind}s") + ".yaml"
                 for kind in ("entity", "derived", "action", "legality", "event", "trigger", "sequence",
                              "decision_point", "random_source", "modifier", "hidden_info", "invariant",
                              "priority", "blocker", "test")}
# Proposal fields set by WGC, never by the executor (ADR-0014).
RESERVED = ("prov", "status", "risk")
# `prov` fields that do not make two records different (who accepted it and when, not what it says).
VOLATILE_PROV = ("job", "at")
# Source role → provenance kind of an anchored record (ADR-0014).
ROLE_KINDS = {**{role: "explicit_source" for role in
                 ("rules", "living_rules", "scenario_book", "charts", "cards", "counters", "map", "module")},
              "errata": "errata", "faq": "faq", "designer_clarification": "designer_clarification"}

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


class KBContextStale(KBStale):
    """Records of `kb/` that the job read (its manifest) changed between execution and acceptance: the result was
    computed from an old context and is not written (ADR-0033)."""


class KBWriteError(KBError):
    """Writing `kb/` failed and `kb/` is as it was: one file is replaced atomically, a batch was rolled back and its
    journal removed. A batch whose rollback did not complete is `KBUnresolved` instead (ADR-0031)."""


class KBUnresolved(KBError):
    """A batch failed and its rollback did not complete: the outcome of the acceptance is not decided yet. The journal
    `kb/.wgc-batch/` and the receipt stay; `wgc kb recover` / `glu reconcile` decide it from `kb/` (ADR-0031)."""


class KBBatchConflict(KBError):
    """An interrupted batch cannot be finished or rolled back automatically (a file changed outside it, or a copy
    is missing); nothing was changed (ADR-0031)."""


# --- workspace ------------------------------------------------------------------------------------------------------

class Workspace:
    """Read-only view of a game repo for tasks: inventory, segment text and KB records.

    The inventory is read once (with its fingerprint `inventory_hash`); KB records are read from disk on every call,
    so a long-lived workspace never serves an old KB snapshot. A **pinned** workspace (`pinned`) reads `kb/` only from
    one snapshot instead: the manifest of a job and its implementation then see the same records, and the snapshot's
    generation tells `accept()` whether they are still current (ADR-0033)."""

    _kb: "KBSnapshot | None" = None

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
        """Extracted text of a segment from `.glu/source/`, checked against its `text_hash` and `struct_hash`: a task
        never reads lines or cells other than those its job key and `prov.inputs_hash` stand for (ADR-0032)."""
        if seg_id in self._text:
            return self._text[seg_id]
        seg = self._segments.get(seg_id)
        if seg is None:
            raise KBError(f"Segmentu `{seg_id}` nie ma w inwentarzu.")
        if "struct_hash" not in seg:
            raise KBError(f"Segment {seg_id} nie ma `struct_hash`: inwentarz i tekst z ekstraktora sprzed ADR-0032 "
                          "trzeba wygenerować ponownie: uruchom `wgc source extract`.")
        path = source.cache_dir(self.root, seg["doc"]) / f"{seg_id}.txt"
        if not path.is_file():
            raise KBError(f"Brak tekstu segmentu {seg_id} ({path.as_posix()}): uruchom `wgc source extract`.")
        text = path.read_text(encoding="utf-8")
        if text_hash(text) != seg.get("text_hash"):
            raise KBError(f"Tekst segmentu {seg_id} w {path.as_posix()} nie zgadza się z `text_hash` inwentarza: "
                          "uruchom `wgc source extract`.")
        if struct_hash(text) != seg["struct_hash"]:
            raise KBError(f"Tekst segmentu {seg_id} w {path.as_posix()} ma te same słowa, ale inne wiersze albo komórki "
                          "niż `struct_hash` inwentarza: uruchom `wgc source extract`.")
        self._text[seg_id] = text
        return text

    def kb_files(self) -> list[Path]:
        return kb_files(self.root)

    def kb_documents(self) -> list[tuple[Path, object]]:
        """(file, document) for every document of `kb/` (several per file allowed, ADR-0019); from the snapshot when
        pinned (do not modify the documents)."""
        return list(self._kb.documents) if self._kb is not None else kb_documents(self.root)

    @property
    def kb_generation(self) -> str | None:
        """Generation of the pinned `kb/` snapshot, None when not pinned."""
        return self._kb.generation if self._kb is not None else None

    def pinned(self, snapshot: "KBSnapshot") -> "Workspace":
        """The same workspace (inventory, text) reading `kb/` only from `snapshot`."""
        view = copy.copy(self)
        view._kb = snapshot
        return view

    def pinned_now(self) -> "Workspace":
        """Pinned to a snapshot of `kb/` read now (without the lock: a torn read never matches a later generation,
        so `accept()` recomputes and compares, ADR-0033)."""
        return self.pinned(read_snapshot(self.root))


@dataclass(frozen=True)
class KBSnapshot:
    """`kb/` read once: the bytes of every file, its documents and the generation of exactly these bytes."""
    files: dict[Path, bytes]
    documents: list[tuple[Path, object]]
    generation: str


def read_snapshot(root: str | Path) -> KBSnapshot:
    """Every KB file read once; documents and generation come from the same bytes (ADR-0033)."""
    root = Path(root)
    files: dict[Path, bytes] = {}
    docs: list[tuple[Path, object]] = []
    for path in kb_files(root):
        try:
            data = path.read_bytes()
            docs += [(path, d) for d in yaml.safe_load_all(data.decode("utf-8")) if d is not None]
        except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
            raise KBError(f"Nie można wczytać {path.as_posix()}: {e}") from None
        files[path] = data
    return KBSnapshot(files, docs, _generation(root, files))


def snapshot(root: str | Path, lock_timeout: float | None = None) -> KBSnapshot:
    """A snapshot read under the KB writer lock when its file exists (nothing is created): never a batch half-way."""
    with lock(root, lock_timeout, create=False):
        return read_snapshot(root)


def kb_files(root: str | Path) -> list[Path]:
    kb = Path(root) / KB_DIR
    return sorted(p for p in kb.rglob("*") if p.suffix in (".yaml", ".yml") and p.is_file()) if kb.is_dir() else []


def kb_documents(root: str | Path) -> list[tuple[Path, object]]:
    out = []
    for path in kb_files(root):
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
    retired: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)      # written files, relative to the root (POSIX)
    schema_valid: bool = True
    domain_valid: bool = True
    issues: list[str] = field(default_factory=list)     # Polish messages; non-empty → nothing written
    receipt: dict | None = None                         # {generation, records} of an accepted result (ADR-0031)

    @property
    def ok(self) -> bool:
        return not self.issues


def _fields(defn: str, contract: str = LOGIC) -> list[str]:
    """Property order of a `wgc/logic@0` definition, or of `provenance` from the common schema."""
    if defn == "provenance":
        common = contracts.registry().contents(contracts.BASE_URI + "common.schema.json")
        return list(common["$defs"]["provenance"]["properties"])
    return list(contracts.schema_for(contract)["$defs"][defn]["properties"])


def ordered(record: dict, contract: str = LOGIC) -> dict:
    """Record with fields in contract order (unknown fields last), `prov` too."""
    kind = record.get("kind")
    order = _fields(kind, contract) if kind in (KIND_FILES if contract == LOGIC else DIGITAL_FILES) else []
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


def _owned_by(record: dict, owner_id: dict, ws: Workspace, spec: TaskSpec) -> bool:
    """Explicit ownership is authoritative; a legacy record needs a manifest proving the same logical scope."""
    prov = record.get("prov") or {}
    if record.get("status") != "accepted" or record.get("kind") in ("human_decision", "interpretation") or \
            prov.get("kind") == "human_decision" or (prov.get("by") or {}).get("tier") == "human":
        return False
    recorded = prov.get("owner")
    if recorded is not None:
        return recorded == owner_id
    prior = prov.get("manifest") or {}
    prior_inputs = tuple(e["id"] for e in prior.get("inputs", []) if isinstance(e, dict) and "id" in e)
    try:
        return (_producer(record) == owner_id["task"] and
                prior.get("task", "").split("@", 1)[0] == owner_id["task"] and bool(prior_inputs) and
                ownership.owner(ws, spec, prior_inputs) == owner_id)
    except (KeyError, TypeError, ValueError):
        return False


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
        elif "quote" in a and not normalize_text(a["quote"]):
            out.append(f"kotwica {i}: `quote` nie może być pustym cytatem.")
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


def _output_contract(spec: TaskSpec) -> tuple[str, dict[str, str], str]:
    contract, sep, kind = spec.output_schema.partition("#")
    expected = {"stage1": LOGIC, "stage1.5": DIGITAL}.get(spec.stage)
    if not sep or contract != expected or kind != spec.output_kind:
        raise KBError(f"Zadanie {spec.name}: output_schema `{spec.output_schema}` nie pasuje do etapu `{spec.stage}` "
                      "i rodzaju outputu.")
    files = KIND_FILES if contract == LOGIC else DIGITAL_FILES
    if kind not in files:
        raise KBError(f"Zadanie {spec.name}: rodzaj `{kind}` nie ma polityki zapisu w {contract}.")
    return contract, files, "logic" if contract == LOGIC else "digital"


def _record_schema_issues(spec: TaskSpec, proposals: list[dict]) -> list[str]:
    """Each proposed record against its stage contract before provenance exists."""
    contract, _, _ = _output_contract(spec)
    validator = contracts.validator(contract)
    out = []
    for n, p in enumerate(proposals, 1):
        rec = p["record"]
        errs = sorted(validator.iter_errors({"schema": contract, "records": [rec]}), key=lambda e: list(e.absolute_path))
        for e in errs:
            if e.validator == "required" and e.message in _RESERVED_MISSING:
                continue
            loc = "/".join(map(str, list(e.absolute_path)[2:])) or "<rekord>"
            out.append(f"propozycja {n} ({rec['id']}): niezgodność ze schematem {spec.output_schema}: {loc}: "
                       f"{e.message[:300]}")
    return out


def _provenance(ws: Workspace, proposal: dict, by: dict, job: str | None,
                kb_records: dict[str, dict], manifest: Manifest, spec: TaskSpec,
                owner_id: dict, candidates: dict[str, dict]) -> tuple[dict | None, list[str]]:
    """`prov` of an accepted record (ADR-0014) or the reasons why it cannot be given. `kb_records` is the KB read
    under the writer lock: `derived_from` resolves against it, never against an older snapshot. The evidence of the
    record (anchors, `derived_from`) must be among what the job read (`manifest`, ADR-0033)."""
    rid = proposal["record"]["id"]
    issues = []
    anchors, kinds, inputs = [], set(), []
    read = manifest.ids()
    for a in proposal.get("anchors") or []:
        seg = ws.segment(a["seg"])
        if seg is None:
            issues.append(f"{rid}: kotwica wskazuje segment `{a['seg']}`, którego nie ma w inwentarzu.")
            continue
        if a["seg"] not in read:
            issues.append(f"{rid}: kotwica w {a['seg']}, którego job nie czytał (spoza manifestu wywołania).")
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
        if span is not None and quote is not None and normalize_text(quote) != text[span[0]:span[1]]:
            issues.append(f"{rid}: cytat {quote!r} nie odpowiada `span` {span} w segmencie {a['seg']}.")
            continue
        anchors.append({"seg": a["seg"], "seg_hash": seg["text_hash"],
                        **{k: a[k] for k in ("span", "quote") if k in a}})
        role = (ws.document(seg["doc"]) or {}).get("role")
        if role not in ROLE_KINDS:
            issues.append(f"{rid}: rola źródła `{role}` nie jest kanoniczna; automatyczna akceptacja wymaga roli "
                          "z listy ADR-0027 (materiał może być dowodem decyzji HD-).")
            continue
        kinds.add(ROLE_KINDS[role])
        inputs.append(projection(seg, "logic"))
    derived = list(proposal.get("derived_from") or [])
    for d in derived:
        rec = ws.segment(d) or candidates.get(d) or kb_records.get(d)
        if rec is None:
            issues.append(f"{rid}: brak rekordu `{d}` (derived_from) w inwentarzu ani w kb/.")
            continue
        if d not in read and d not in candidates:
            issues.append(f"{rid}: `derived_from` wskazuje {d}, którego job nie czytał (spoza manifestu wywołania).")
            continue
        try:
            inputs.append(projection(rec, "logic"))
        except ProjectionError as e:  # no fallback (ADR-0034)
            issues.append(f"{rid}: `derived_from` {d}: {e}.")
    if len(kinds) > 1:
        issues.append(f"{rid}: kotwice wskazują źródła o różnych rolach ({', '.join(sorted(kinds))}).")
    if issues:
        return None, issues
    if anchors:
        kind = kinds.pop()
    elif by.get("tier") == "deterministic":
        kind = "deterministic_derivation"
    elif by.get("tier") in ("local", "premium"):
        if not spec.allow_llm_inference:
            return None, [f"{rid}: zadanie {spec.name} nie deklaruje `allow_llm_inference`; propozycja bez kotwic "
                          "nie może być automatycznie przyjęta."]
        kind = "llm_inference"
    else:
        return None, [f"{rid}: wykonawca `{by.get('tier')}` bez kotwic nie daje provenance (wymaga HD-)."]
    prov = {"kind": kind, **({"anchors": anchors} if anchors else {}), **({"derived_from": derived} if derived else {}),
            "by": dict(by), **({"job": job} if job else {}), "inputs_hash": evidence_hash(inputs),
            "manifest": copy.deepcopy(manifest.body), "owner": copy.deepcopy(owner_id)}
    return prov, []


def evidence_hash(projections: list[dict]) -> str:
    """`prov.inputs_hash`: the evidence of one record (projections of its anchor segments and `derived_from` records),
    with the projection version (ADR-0033, ADR-0034). What the job read is `prov.manifest`."""
    return content_hash({"projection": PROJECTION_VERSION, "records": projections})


def _natural(record_id: str) -> list:
    return [(0, int(t), "") if t.isdigit() else (1, 0, t) for t in re.findall(r"\d+|\D+", record_id)]


@contextlib.contextmanager
def lock(root: str | Path, timeout: float | None = None, create: bool = True) -> Iterator[None]:
    """The KB writer lock of a game repo (`.glu/kb.lock`, ADR-0026), between processes and threads. Busy for longer
    than `timeout` seconds → `KBBusy`. `create=False` (read-only callers): without a lock file there has never been
    a writer, so nothing is locked and nothing is created."""
    path = Path(root) / LOCK_FILE
    timeout = LOCK_TIMEOUT if timeout is None else timeout
    if not create and not path.is_file():
        yield
        return
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


def accept(root: str | Path, spec: TaskSpec, inputs: Inputs, proposals: list | dict, *, by: dict,
           job: str | None = None, ws: Workspace | None = None, lock_timeout: float | None = None,
           manifest: Manifest | None = None) -> AcceptResult:
    """Accept the proposals of one job into `kb/` (the only writer of KB YAML). See the module docstring.
    `lock_timeout`: seconds to wait for the KB writer lock (default `LOCK_TIMEOUT`), then `KBBusy`.
    `manifest`: the manifest the proposals were computed with (`wgc.manifest.build` at execution); required for a
    task that reads `kb/`, else computed here. It is checked against `kb/` under the lock (ADR-0033)."""
    ws = ws or Workspace(root)
    root = ws.root
    if isinstance(proposals, dict):
        envelope = proposals
        proposals = envelope.get("proposals")
    else:
        envelope = {"schema": "wgc/proposal@0", "task": spec.name, "output_schema": spec.output_schema,
                    "proposals": proposals}
    envelope_issues = (contracts.errors(envelope) if envelope.get("schema") == "wgc/proposal@0" else
                       ["Envelope propozycji wymaga `schema: wgc/proposal@0`."])
    if envelope.get("task") != spec.name or envelope.get("output_schema") != spec.output_schema:
        envelope_issues.append(f"Envelope propozycji musi deklarować zadanie {spec.name} i kontrakt {spec.output_schema}.")
    res = AcceptResult(records=[p["record"]["id"] for p in proposals if isinstance(p, dict)
                                and isinstance(p.get("record"), dict) and isinstance(p["record"].get("id"), str)]
                       if isinstance(proposals, list) else [])
    # pure checks first: nothing below sees wrong types, and rejected data never waits for the lock
    issues = _shape_issues(spec, proposals)
    if not issues:
        issues = envelope_issues or _record_schema_issues(spec, proposals)
    if issues:
        res.schema_valid, res.issues = False, issues
        return res
    # one writer per project: read KB, merge, validate and write as one critical section (ADR-0026)
    with lock(root, LOCK_TIMEOUT if lock_timeout is None else lock_timeout):
        inventory = _inventory_under_lock(ws)
        return _accept_locked(ws, spec, inputs, proposals, by, job, inventory, res, manifest)


def _current_manifest(lws: Workspace, spec: TaskSpec, inputs: Inputs, given: Manifest | None) -> Manifest:
    """The manifest to record, checked against the inventory and `kb/` read under the lock (`lws`, ADR-0033):
    - a task reading `kb/` must bring the manifest of its execution; the same generation means the same bytes, else
      the manifest is rebuilt and any difference is `KBContextStale`;
    - a task not reading `kb/` is compared without the generation, so changes of other files never block it."""
    if given is None:
        if manifests.reads_kb(lws, spec, inputs):
            raise KBError(f"Zadanie {spec.name} czyta kb/: accept() wymaga manifestu z wykonania joba (ADR-0033).")
        return manifests.build(lws, spec, inputs)
    if given.generation is not None and given.generation == lws.kb_generation:
        return given
    current = manifests.build(lws, spec, inputs)
    changes = manifests.diff(given.body, current.body)
    if changes:
        cls = KBContextStale if given.generation is not None else KBStale
        raise cls(f"Wejścia joba zmieniły się między wykonaniem a akceptacją ({'; '.join(changes)}). Wynik obliczony "
                  "ze starego kontekstu nie został zapisany: ponów build.")
    return given


def _accept_locked(ws: Workspace, spec: TaskSpec, inputs: Inputs, proposals: list[dict], by: dict,
                   job: str | None, inventory: dict, res: AcceptResult, given: Manifest | None) -> AcceptResult:
    root = ws.root
    _recover_locked(root)  # never merge into a partial kb/ (ADR-0031)
    snap = read_snapshot(root)  # read now, under the lock
    lws = ws.pinned(snap)
    manifest = _current_manifest(lws, spec, inputs, given)  # before anything is judged or written (ADR-0033)
    contract, kind_files, stage_dir = _output_contract(spec)
    docs = list(snap.documents)
    kb_records = {r["id"]: r for _, doc in docs for r in _records(doc) if isinstance(r.get("id"), str)}
    domain = list(spec.validate(lws, inputs, proposals))
    owner_id = ownership.owner(lws, spec, inputs)
    owner_path = ownership.path(root, spec.id, tuple(owner_id["scope"]))
    old_output = next((d for p, d in docs if p == owner_path), None)
    if old_output is not None and (not isinstance(old_output, dict) or contracts.errors(old_output)
                                   or old_output.get("owner") != owner_id):
        raise KBError(f"Niepoprawny manifest outputów {owner_path.relative_to(root).as_posix()}.")
    # First acceptance after M-STAB3b: safely claim records whose old invocation maps to this exact logical scope.
    old_active = set(old_output["active"]) if old_output is not None else set()
    if old_output is None:
        for rid, rec in kb_records.items():
            if not _owned_by(rec, owner_id, lws, spec):
                continue
            old_active.add(rid)
    candidates = {p["record"]["id"]: p["record"] for p in proposals}
    def cyclic(rid: str, path: set[str], done: set[str]) -> bool:
        if rid in path:
            return True
        if rid in done:
            return False
        path.add(rid)
        for p in proposals:
            if p["record"]["id"] == rid:
                if any(cyclic(d, path, done) for d in p.get("derived_from", []) if d in candidates):
                    return True
                break
        path.remove(rid)
        done.add(rid)
        return False
    checked: set[str] = set()
    if any(cyclic(rid, set(), checked) for rid in candidates):
        domain.append("`derived_from` tworzy cykl w partii propozycji.")

    # records with provenance, each checked against the contract on its own
    new: list[dict] = []
    for p in proposals:
        prov, errs = _provenance(lws, p, by, job, kb_records, manifest, spec, owner_id, candidates)
        domain += errs
        if prov is None:
            continue
        rec = ordered({**p["record"], "status": "accepted", "prov": prov}, contract)
        schema_errs = contracts.errors({"schema": contract, "records": [rec]})
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
    if old_output is not None:
        for rid in old_active:
            current = kb_records.get(rid)
            if current is None or old_output["hashes"].get(rid) != content_hash(current):
                res.issues.append(f"{rid}: konflikt ownership: aktywny output zmienił treść poza ownerem albo zniknął; "
                                  "automatyczne uzgodnienie jest zablokowane.")
    if res.issues:
        res.domain_valid = False
        return res
    for rid in sorted(old_active - set(candidates)):
        if rid not in where:
            res.issues.append(f"{rid}: manifest outputów wskazuje brakujący rekord; nie można go wycofać bez "
                              "uzgodnienia ownership.")
            continue
        i, old = where[rid]
        if not _owned_by(old, owner_id, lws, spec):
            res.issues.append(f"{rid}: output zmienił właściciela albo status; zadanie {spec.name} go nie wycofuje.")
            continue
        docs[i][1]["records"].remove(old)
        changed.add(i)
        res.retired.append(rid)
    for rec in new:
        rid = rec["id"]
        if rid in where:
            i, old = where[rid]
            if not _owned_by(old, owner_id, lws, spec):
                res.issues.append(f"{rid}: konflikt z rekordem w {docs[i][0].relative_to(root).as_posix()} "
                                  f"(producent `{_producer(old)}`, status `{old.get('status')}`); zadanie {spec.name} "
                                  "nie nadpisuje cudzych rekordów.")
                continue
            if _comparable(old) == _comparable(rec):
                res.unchanged.append(rid)
                continue
            recs = docs[i][1]["records"]
            recs[recs.index(old)] = rec
            res.updated.append(rid)
        else:
            path = root / KB_DIR / stage_dir / kind_files[rec["kind"]]
            i = next((n for n, (p, d) in enumerate(docs) if p == path and isinstance(d, dict)
                      and d.get("schema") == contract), None)
            if i is None:
                docs.append((path, {"schema": contract, "records": []}))
                i = len(docs) - 1
            docs[i][1]["records"].append(rec)
            res.created.append(rid)
        changed.add(i)
    if res.issues:
        res.domain_valid = False
        return res

    active = {r["id"]: r for _, d in docs for r in _records(d) if r.get("id") in candidates}
    output = {"schema": ownership.SCHEMA, "owner": owner_id,
              "active": sorted(candidates), "hashes": {rid: content_hash(active[rid]) for rid in sorted(candidates)},
              "retired": sorted((set((old_output or {}).get("retired", [])) | set(res.retired)) - set(candidates))}
    if old_output != output:
        if old_output is None:
            docs.append((owner_path, output))
            changed.add(len(docs) - 1)
        else:
            i = next(i for i, (p, _) in enumerate(docs) if p == owner_path)
            docs[i] = (owner_path, output)
            changed.add(i)

    # the whole KB with the inventory checked under the lock must stay valid
    report = validate_documents([(source.inventory_path(root).relative_to(root).as_posix(), inventory)]
                                + [(p.relative_to(root).as_posix(), d) for p, d in docs])
    errors = [d for d in report.diagnostics if d.severity == ERROR]
    if errors:
        res.domain_valid = False
        res.issues += [f"{d.code} {d.subject}: {d.message}" for d in errors]
        return res

    # new content of the changed files, the receipt, then one atomic file or one batch (ADR-0031)
    files = sorted({docs[i][0] for i in changed})
    texts: dict[Path, str] = {}
    for path in files:
        file_docs = [d for p, d in docs if p == path]
        if path == owner_path:
            texts[path] = yaml.safe_dump(output, sort_keys=False, allow_unicode=True)
            continue
        for d in file_docs:
            if isinstance(d, dict) and d.get("schema") == contract:
                d["records"] = sorted((ordered(r, contract) for r in d["records"]),
                                      key=lambda r: _natural(r.get("id", "")))
        texts[path] = dump(file_docs)
    final = {r["id"]: r for _, d in docs for r in _records(d) if isinstance(r.get("id"), str)}
    contents = dict(snap.files) | {p: t.encode("utf-8") for p, t in texts.items()}
    res.receipt = {"generation": _generation(root, contents),
                   "records": {rid: content_hash(final[rid]) for rid in res.records},
                   "retired": res.retired}
    if job:
        _write_receipt(root, job, res.receipt)
    if len(files) == 1:
        [path] = files
        try:
            _write_file(path, texts[path])
        except OSError as e:
            raise KBWriteError(f"Nie można zapisać {path.relative_to(root).as_posix()}: {e}. Ten plik ma poprzednią "
                               "zawartość (zapis atomowy). Niczego nie zapisano.") from e
    elif files:
        _write_batch(root, [(p, texts[p].encode("utf-8")) for p in files], job)
    res.files = [p.relative_to(root).as_posix() for p in files]
    return res


def _write_batch(root: Path, changes: list[tuple[Path, bytes]], job: str | None) -> None:
    """Several files of `kb/` as one batch (ADR-0031). On failure: `KBWriteError` when the rollback completed,
    `KBUnresolved` when it did not (the journal stays for recovery), `KBWriteError` when preparing failed."""
    names = ", ".join(p.relative_to(root).as_posix() for p, _ in changes)
    try:
        fsbatch.commit(root, root / BATCH_DIR, changes, job)
    except fsbatch.BatchError as e:
        if e.rolled_back:
            raise KBWriteError(f"Nie można zapisać partii plików kb/ ({names}): {e}. Partia wycofana, kb/ bez zmian. "
                               "Niczego nie zapisano.") from e
        direction = ("wycofanie jest przesądzone (manifest `rolling_back`)" if e.rollback_decided
                     else "kierunek (dokończenie albo wycofanie) ustali recovery")
        raise KBUnresolved(f"Nie można zapisać partii plików kb/ ({names}): {e}. Wynik akceptacji nierozstrzygnięty: "
                           f"{direction}; dziennik {BATCH_DIR.as_posix()}/ i receipt zostają. Uruchom `glu reconcile` "
                           "(albo `wgc kb recover`), zanim cokolwiek przeczyta kb/.") from e
    except OSError as e:  # preparing the batch failed: no file of kb/ was touched
        raise KBWriteError(f"Nie można przygotować partii plików kb/ ({names}): {e}. Niczego nie zapisano.") from e


def _remove_orphan_temps(kb_dir: Path) -> None:
    """Temporary files of an interrupted earlier write (the writer lock is held, so no write is in progress)."""
    for tmp in fsio.temp_files(kb_dir):
        try:
            tmp.unlink()
        except OSError:
            pass


# --- recovery and receipts (ADR-0031) -------------------------------------------------------------------------------

@dataclass
class Recovery:
    state: str                      # clean | orphan | rollback | forward (wgc.fsbatch)
    actions: list[str] = field(default_factory=list)
    job: str | None = None          # job of the interrupted batch


def pending_batch(root: str | Path) -> bool:
    """`kb/.wgc-batch/` exists: a batch was interrupted (or is in progress in another process right now)."""
    return (Path(root) / BATCH_DIR).exists()


def _recover_locked(root: Path, dry_run: bool = False) -> Recovery:
    try:
        p = fsbatch.recover(root, root / BATCH_DIR, dry_run=dry_run)
    except fsbatch.BatchConflict as e:
        raise KBBatchConflict(f"Przerwana partia kb/ wymaga decyzji: {e}.") from None
    except OSError as e:
        raise KBWriteError(f"Recovery przerwanej partii kb/ nie powiodło się: {e}.") from None
    out = Recovery(p.state, list(p.actions), p.job)
    temps = fsio.temp_files(root / KB_DIR)
    if temps:
        out.actions += [f"usunięcie pliku tymczasowego {t.relative_to(root).as_posix()}" for t in temps]
        if not dry_run:
            _remove_orphan_temps(root / KB_DIR)
    return out


def recover(root: str | Path, dry_run: bool = False, lock_timeout: float | None = None) -> Recovery:
    """Finish or roll back an interrupted batch of `kb/` under the writer lock (ADR-0031): afterwards `kb/` is
    wholly old or wholly new. Idempotent; on a clean `kb/` it changes nothing. `dry_run`: only the plan, nothing
    written (not even the lock file)."""
    root = Path(root)
    if not pending_batch(root) and not fsio.temp_files(root / KB_DIR):
        return Recovery("clean")  # nothing to recover: not even the lock file is created
    with lock(root, lock_timeout, create=not dry_run):
        return _recover_locked(root, dry_run)


def _generation(root: Path, contents: dict[Path, bytes]) -> str:
    """Generation of `kb/`: hash of (path, `sha256:<hex>` of the bytes) of every KB file. Receipts written before
    this was fixed hashed `sha256:sha256:<hex>` components: their `generation` differs for the same `kb/`, which
    `check_receipt` does not compare (ADR-0031)."""
    return content_hash(sorted([p.relative_to(root).as_posix(), sha256_hex(b)] for p, b in contents.items()))


def generation(root: str | Path) -> str:
    root = Path(root)
    return _generation(root, {p: p.read_bytes() for p in kb_files(root)})


def _receipt_path(root: Path, job: str) -> Path:
    return Path(root) / RECEIPTS_DIR / f"{job}.json"


def _write_receipt(root: Path, job: str, receipt: dict) -> None:
    path = _receipt_path(root, job)
    try:
        fsio.atomic_write(path, json.dumps({"job": job, **receipt}, ensure_ascii=False, indent=1).encode("utf-8"))
    except OSError as e:
        raise KBWriteError(f"Nie można zapisać receiptu akceptacji {path.as_posix()}: {e}. Niczego nie zapisano "
                           "w kb/.") from e


def read_receipt(root: str | Path, job: str) -> dict | None:
    """Receipt `{generation, records}` of the acceptance of `job`, or None (never written, or already discarded)."""
    path = _receipt_path(Path(root), job)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
        return {"generation": doc["generation"], "records": dict(doc["records"]),
                "retired": list(doc.get("retired", []))}
    except FileNotFoundError:
        return None
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise KBError(f"Nieczytelny receipt {path.as_posix()}: {e}") from None


def receipt_jobs(root: str | Path) -> list[str]:
    """Jobs with a receipt still on disk."""
    d = Path(root) / RECEIPTS_DIR
    return sorted(p.stem for p in d.glob("*.json")) if d.is_dir() else []


def discard_receipt(root: str | Path, job: str) -> None:
    """Remove the receipt once the Attempt is recorded. A leftover receipt is harmless: reconcile removes it."""
    try:
        _receipt_path(Path(root), job).unlink()
    except OSError:
        pass


def check_receipt(root: str | Path, receipt: dict, *, dry_run: bool = False,
                  lock_timeout: float | None = None) -> list[str]:
    """Differences between a receipt and the current `kb/` (empty list: `kb/` holds that result). Under the writer
    lock and after recovery, so a batch in progress is never judged half-way. `dry_run`: no recovery, no lock file."""
    root = Path(root)
    with lock(root, lock_timeout, create=not dry_run):
        if pending_batch(root):
            if dry_run:
                return ["kb/ ma przerwaną partię (najpierw recovery)"]
            _recover_locked(root)
        current = {r["id"]: r for _, d in kb_documents(root) for r in _records(d) if isinstance(r.get("id"), str)}
    out = []
    for rid, h in receipt["records"].items():
        if rid not in current:
            out.append(f"{rid}: brak w kb/")
        elif content_hash(current[rid]) != h:
            out.append(f"{rid}: inna treść w kb/")
    for rid in receipt.get("retired", []):
        if rid in current:
            out.append(f"{rid}: wycofany output jest obecny w kb/")
    return out


@dataclass
class ReceiptComparison:
    """A receipt against the current `kb/`, read only (`glu receipt`, ADR-0033)."""
    status: str                                     # match | differs | pending_batch
    records: dict[str, dict] = field(default_factory=dict)  # id → {state: same|changed|missing, job: current prov.job}
    generation_equal: bool | None = None            # kb/ byte for byte as after the acceptance


def compare_receipt(root: str | Path, receipt: dict, lock_timeout: float | None = None) -> ReceiptComparison:
    """Compare a receipt with the current `kb/` and change nothing: no recovery, no lock file created (the writer lock
    is taken only when its file exists, which writes nothing). A pending batch is reported, not resolved. A
    difference may be a correct later change of `kb/` (another job, a human decision), not damage."""
    root = Path(root)
    with lock(root, lock_timeout, create=False):
        if pending_batch(root):
            return ReceiptComparison("pending_batch")
        snap = read_snapshot(root)
    current = {r["id"]: r for _, d in snap.documents for r in _records(d) if isinstance(r.get("id"), str)}
    out = ReceiptComparison("match", generation_equal=receipt.get("generation") == snap.generation)
    for rid, h in receipt["records"].items():
        rec = current.get(rid)
        state = "missing" if rec is None else "same" if content_hash(rec) == h else "changed"
        out.records[rid] = {"state": state, "job": ((rec or {}).get("prov") or {}).get("job")}
        if state != "same":
            out.status = "differs"
    for rid in receipt.get("retired", []):
        rec = current.get(rid)
        state = "missing" if rec is None else "changed"
        out.records[rid] = {"state": state, "job": ((rec or {}).get("prov") or {}).get("job"), "retired": True}
        if rec is not None:
            out.status = "differs"
    return out


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
    schema = documents[0].get("schema") if documents and isinstance(documents[0], dict) else LOGIC
    header = HEADER if schema == LOGIC else f"# {schema}: rekordy KB zapisuje wyłącznie `wgc.kb.accept()`.\n"
    return header + "---\n".join(parts)


def _write_file(path: Path, text: str) -> None:
    """Writes one file of `kb/` (tests replace it to prove that a single-file acceptance goes through here). Atomic
    replacement: a failure leaves the previous content (ADR-0026). Several files go through `_write_batch`; recovery
    only finishes or undoes such a batch from its journal (ADR-0031)."""
    fsio.atomic_write(path, text.encode("utf-8"))
