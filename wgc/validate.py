"""Validator: L0 (schema), L1 (identity and references) and provenance checks outside the schema.

`validate(paths)` reads YAML files (a directory is searched recursively for *.yaml / *.yml; a file may hold several
documents separated by `---`, each naming its own contract) and returns a `Report`: a list of diagnostics
`{code, severity, subject, message, affected, location}`. Messages are Polish (user-facing).

L1 and provenance checks treat all records of the domain contracts (`wgc/source|logic|digital`) from all files as one
set. Documents of other contracts (`wgc/gate`, `glu/exec`, `igw/api`) get L0 only: their ids live outside the KB.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

from wgc import contracts, ids

DOMAIN_CONTRACTS = frozenset({"wgc/source@0", "wgc/logic@0", "wgc/digital@0"})

ERROR = "error"
WARNING = "warning"

# Diagnostic codes. L0: load_error, schema_error. L1: duplicate_id, kind_prefix_mismatch, unresolved_ref.
# Provenance: anchor_hash_mismatch, missing_decision.
CODES = ("load_error", "schema_error", "duplicate_id", "kind_prefix_mismatch", "unresolved_ref",
         "anchor_hash_mismatch", "missing_decision")

# Reference positions checked for `unresolved_ref`: (record kinds or None = any kind, field path).
# A value is one ID or a list of IDs; `*` steps into every item of a list. Anchors (`seg`) and `prov.decision` have dedicated checks below.
REF_FIELDS: tuple[tuple[frozenset[str] | None, tuple[str, ...]], ...] = (
    (None, ("refs",)),
    (None, ("prov", "derived_from")),
    (None, ("realizes",)),
    (frozenset({"entity"}), ("fields", "*", "realizes")),
    (None, ("covers",)),
    (None, ("applies_to",)),
    (None, ("from_case",)),
    (frozenset({"relation"}), ("from",)),
    (frozenset({"relation"}), ("to",)),
    (frozenset({"interpretation"}), ("ambiguity",)),
    (frozenset({"blocker"}), ("cause",)),
    (frozenset({"blocker"}), ("affects",)),
    (frozenset({"segment"}), ("doc",)),
    (frozenset({"segment"}), ("parent",)),
)


@dataclass
class Diagnostic:
    code: str
    severity: str
    subject: str
    message: str
    affected: list[str] = field(default_factory=list)
    location: str | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        if d["location"] is None:
            del d["location"]
        return d


@dataclass
class Report:
    diagnostics: list[Diagnostic] = field(default_factory=list)
    files: int = 0
    records: int = 0

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == ERROR]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == WARNING]

    @property
    def ok(self) -> bool:
        return not self.errors

    def codes(self, severity: str = ERROR) -> set[str]:
        return {d.code for d in self.diagnostics if d.severity == severity}

    def to_dict(self) -> dict:
        return {"ok": self.ok, "files": self.files, "records": self.records, "errors": len(self.errors),
                "warnings": len(self.warnings), "diagnostics": [d.to_dict() for d in self.diagnostics]}


@dataclass
class _Rec:
    data: dict
    location: str

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def kind(self):
        return self.data.get("kind")


def _files(paths, report: Report) -> list[Path]:
    out = []
    for p in map(Path, paths):
        if p.is_dir():
            out.extend(sorted(f for f in p.rglob("*") if f.suffix in (".yaml", ".yml") and f.is_file()))
        elif p.is_file():
            out.append(p)
        else:
            report.diagnostics.append(Diagnostic("load_error", ERROR, p.as_posix(), f"Ścieżka nie istnieje: {p.as_posix()}",
                                                 location=p.as_posix()))
    return out


def load_documents(path: Path) -> list:
    """All YAML documents of a file (empty documents skipped)."""
    return [d for d in yaml.safe_load_all(path.read_text(encoding="utf-8")) if d is not None]


_RECORD_LOC = re.compile(r"^records/(\d+)")


def _schema_diagnostics(doc, location: str) -> list[Diagnostic]:
    contract = doc.get("schema") if isinstance(doc, dict) else None
    try:
        errs = contracts.errors(doc)
    except KeyError:
        return [Diagnostic("schema_error", ERROR, location, f"Nieznany kontrakt `{contract}`.", location=location)]
    out = []
    for e in errs:
        subject = location
        m = _RECORD_LOC.match(e)
        if m:
            recs = doc.get("records") or []
            i = int(m.group(1))
            if i < len(recs) and isinstance(recs[i], dict) and isinstance(recs[i].get("id"), str):
                subject = recs[i]["id"]
        out.append(Diagnostic("schema_error", ERROR, subject, f"Niezgodność ze schematem `{contract}`: {e}",
                              location=location))
    return out


def _get(data: dict, path: tuple[str, ...]):
    for key in path:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data


def _ref_values(data, path: tuple[str, ...]) -> list[str]:
    """IDs at `path`; `*` fans out over a list."""
    if not path:
        return _as_ids(data)
    head, rest = path[0], path[1:]
    if head == "*":
        return [v for item in data for v in _ref_values(item, rest)] if isinstance(data, list) else []
    return _ref_values(data.get(head), rest) if isinstance(data, dict) else []


def _as_ids(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [v for v in value if isinstance(v, str)]
    return []


def _anchors(rec: _Rec) -> list[dict]:
    out = list(_get(rec.data, ("prov", "anchors")) or [])
    if rec.kind == "review_request":
        out += list(rec.data.get("evidence") or [])
    return [a for a in out if isinstance(a, dict)]


def _check_semantics(records: list[_Rec]) -> list[Diagnostic]:
    out: list[Diagnostic] = []

    # ---- index of defined ids (records + nested sequence nodes) ------------------------------
    defined: dict[str, list[tuple[str, str]]] = {}  # id → [(kind, location)]
    nested: list[tuple[str, str, str]] = []  # (id, kind, location) of nested definitions
    for r in records:
        defined.setdefault(r.id, []).append((r.kind, r.location))
        if r.kind == "sequence":
            for node in r.data.get("nodes") or []:
                if isinstance(node, dict) and isinstance(node.get("id"), str):
                    defined.setdefault(node["id"], []).append(("sequence", r.location))
                    nested.append((node["id"], "sequence", r.location))
    first: dict[str, _Rec] = {}
    for r in records:
        first.setdefault(r.id, r)

    # ---- duplicate_id ------------------------------------------------------------------------
    for i, entries in defined.items():
        if len(entries) > 1:
            locs = ", ".join(sorted({loc for _, loc in entries}))
            out.append(Diagnostic("duplicate_id", ERROR, i, f"ID `{i}` jest zdefiniowane {len(entries)} razy ({locs}).",
                                  location=entries[1][1]))

    # ---- kind_prefix_mismatch ----------------------------------------------------------------
    for i, kind, loc in [(r.id, r.kind, r.location) for r in records] + nested:
        prefix = ids.expected_prefix(kind) if isinstance(kind, str) else None
        if prefix and not ids.check_kind_prefix(kind, i):
            out.append(Diagnostic("kind_prefix_mismatch", ERROR, i,
                                  f"Rekord rodzaju `{kind}` ma ID `{i}`; oczekiwany prefiks `{prefix}-`.", location=loc))

    # ---- unresolved_ref, anchor_hash_mismatch, missing_decision ------------------------------
    for r in records:
        for kinds, path in REF_FIELDS:
            if kinds is not None and r.kind not in kinds:
                continue
            for target in _ref_values(r.data, path):
                if target not in defined:
                    out.append(Diagnostic("unresolved_ref", ERROR, r.id,
                                          f"Pole `{'.'.join(path).replace('.*.', '[].')}` wskazuje nieistniejący rekord `{target}`.",
                                          affected=[target], location=r.location))
        for a in _anchors(r):
            seg = a.get("seg")
            if not isinstance(seg, str):
                continue
            if seg not in defined:
                out.append(Diagnostic("unresolved_ref", ERROR, r.id, f"Kotwica wskazuje nieistniejący segment `{seg}`.",
                                      affected=[seg], location=r.location))
                continue
            target = first.get(seg)
            if target is None or target.kind != "segment":
                continue
            expected = target.data.get("text_hash")
            if expected is not None and a.get("seg_hash") != expected:
                out.append(Diagnostic("anchor_hash_mismatch", ERROR, r.id,
                                      f"Kotwica do `{seg}` ma `seg_hash` {a.get('seg_hash')}, a segment ma `text_hash` "
                                      f"{expected}: kotwica jest nieaktualna.", affected=[seg], location=r.location))
        prov = r.data.get("prov") if isinstance(r.data.get("prov"), dict) else {}
        needs_decision = prov.get("kind") == "human_decision" or (r.kind == "interpretation" and r.data.get("status") == "accepted")
        decision = prov.get("decision")
        if needs_decision or decision is not None:
            target = first.get(decision) if isinstance(decision, str) else None
            if target is None or target.kind != "human_decision":
                msg = (f"`prov.decision` wskazuje `{decision}`, które nie jest istniejącym rekordem `HD-`."
                       if decision is not None else "Rekord wymaga decyzji człowieka, ale nie ma `prov.decision` (`HD-`).")
                out.append(Diagnostic("missing_decision", ERROR, r.id, msg,
                                      affected=[decision] if isinstance(decision, str) else [], location=r.location))
    return out


def validate(paths) -> Report:
    report = Report()
    records: list[_Rec] = []
    for f in _files(paths, report):
        loc = f.as_posix()
        report.files += 1
        try:
            docs = load_documents(f)
        except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
            report.diagnostics.append(Diagnostic("load_error", ERROR, loc, f"Nie można wczytać pliku: {e}", location=loc))
            continue
        if not docs:
            report.diagnostics.append(Diagnostic("load_error", ERROR, loc, "Plik nie zawiera żadnego dokumentu YAML.",
                                                 location=loc))
        for n, doc in enumerate(docs, 1):
            dloc = loc if len(docs) == 1 else f"{loc}#{n}"
            report.diagnostics += _schema_diagnostics(doc, dloc)
            if isinstance(doc, dict) and doc.get("schema") in DOMAIN_CONTRACTS and isinstance(doc.get("records"), list):
                for rec in doc["records"]:
                    if isinstance(rec, dict) and isinstance(rec.get("id"), str):
                        records.append(_Rec(rec, dloc))
    report.records = len(records)
    report.diagnostics += _check_semantics(records)
    return report
