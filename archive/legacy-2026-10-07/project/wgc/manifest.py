"""Invocation manifest of a job (`wgc/manifest@0`, ADR-0033): the one definition of what a task reads.

`build(ws, spec, inputs)` gives the manifest the planner keys the job with and `wgc.kb.accept()` records in
`prov.manifest` (in `kb/`, so the dependencies of a record survive the loss of `.glu/`):
- `format`, `task` (`id@version`), `projection` (`wgc.canonical.PROJECTION_VERSION`);
- `inputs`: `{id, hash}` of every job input in order: the task's own `semantic_projection(ws, id)`, else the `logic`
  projection of the record;
- `authority`: `{id, hash}` of the `logic` projection (`role`, `seg_prefix`, `precedence`) of every source document
  the task takes authority data from: the documents of its input segments (`accept()` derives the provenance kind from
  their role) and those of `TaskSpec.authority_selector`; sorted by id;
- `context`: `{id, hash}` of the `logic` projection of the `kb/` records of `TaskSpec.context_selector`, sorted by
  id; absent when there are none.

Nothing volatile (job, build, scope, time, `kb/` generation) enters the manifest. The job key takes `input_hash` (the
manifest without `context`) and `context_hash` (the `context` list) from it.

A task **reads `kb/`** when it has a `context_selector` or an input that is not a segment. Its manifest is computed
on a workspace pinned to one `kb/` snapshot (`wgc.kb.Workspace.pinned`), whose generation travels with the manifest
(`Manifest.generation`, never in the body) so that `accept()` can tell whether the context is still current.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from wgc.canonical import PROJECTION_VERSION, ProjectionError, content_hash, projection

if TYPE_CHECKING:
    from wgc.kb import Workspace
    from wgc.tasks import Inputs, TaskSpec

FORMAT = "wgc/manifest@0"
SECTIONS = ("inputs", "authority", "context")
SECTION_PL = {"inputs": "wejście", "authority": "dokument źródłowy", "context": "kontekst kb/"}


@dataclass(frozen=True)
class Manifest:
    body: dict                      # what `prov.manifest` records
    generation: str | None = None   # `kb/` generation of the snapshot read (tasks reading kb/ only); never persisted

    @property
    def input_hash(self) -> str:
        return content_hash({k: v for k, v in self.body.items() if k != "context"})

    @property
    def context_hash(self) -> str:
        return content_hash(self.body.get("context", []))

    def ids(self) -> set[str]:
        """Ids of the records the job read (inputs and context): the evidence of a record must be among them."""
        return {e["id"] for s in ("inputs", "context") for e in self.body.get(s, [])}


def _error(message: str) -> Exception:
    from wgc.kb import KBError  # wgc.kb imports this module
    return KBError(message)


def _logic(record: dict, where: str) -> dict:
    try:
        return projection(record, "logic")
    except ProjectionError as e:
        raise _error(f"{where} {record.get('id')}: {e}") from None


def _entry(record_id: str, proj: dict) -> dict:
    return {"id": record_id, "hash": content_hash(proj)}


def reads_kb(ws: "Workspace", spec: "TaskSpec", inputs: "Inputs") -> bool:
    return spec.context_selector is not None or any(ws.segment(i) is None for i in inputs)


def authority_ids(ws: "Workspace", spec: "TaskSpec", inputs: "Inputs") -> list[str]:
    docs = {ws.segment(i)["doc"] for i in inputs if ws.segment(i) is not None}
    if spec.authority_selector is not None:
        docs |= set(spec.authority_selector(ws, inputs))
    return sorted(docs)


def build(ws: "Workspace", spec: "TaskSpec", inputs: "Inputs") -> Manifest:
    """The manifest of one job. `wgc.kb.KBError` when an input, context record or document is missing or its kind
    has no projection (ADR-0034)."""
    kb_task = reads_kb(ws, spec, inputs)
    if kb_task and ws.kb_generation is None:
        ws = ws.pinned_now()  # every kb/ read of the manifest from one snapshot
    entries = []
    for i in inputs:
        rec = ws.record(i)
        proj = spec.semantic_projection(ws, i) if spec.semantic_projection is not None else _logic(rec, "wejście")
        entries.append(_entry(i, proj))
    authority = []
    for d in authority_ids(ws, spec, inputs):
        doc = ws.document(d)
        if doc is None:
            raise _error(f"Brak dokumentu `{d}` w inwentarzu (dane autorytetu zadania {spec.name}).")
        authority.append(_entry(d, _logic(doc, "dokument")))
    body = {"format": FORMAT, "task": spec.name, "projection": PROJECTION_VERSION, "inputs": entries,
            "authority": authority}
    if spec.context_selector is not None:
        context = [_entry(c, _logic(ws.record(c), "kontekst")) for c in sorted(set(spec.context_selector(ws, inputs)))]
        if context:
            body["context"] = context
    return Manifest(body, ws.kb_generation if kb_task else None)


def diff(old: dict, new: dict) -> list[str]:
    """Differences between two manifest bodies, in Polish (empty: equal)."""
    out = [f"{k}: {old.get(k)} → {new.get(k)}" for k in ("format", "task", "projection") if old.get(k) != new.get(k)]
    for section in SECTIONS:
        a = {e["id"]: e["hash"] for e in old.get(section, [])}
        b = {e["id"]: e["hash"] for e in new.get(section, [])}
        what = SECTION_PL[section]
        out += [f"{what} {i}: zmieniony" for i in a if i in b and a[i] != b[i]]
        out += [f"{what} {i}: nie jest już czytany albo nie istnieje" for i in a if i not in b]
        out += [f"{what} {i}: nowy" for i in b if i not in a]
        if section == "inputs" and not out and list(a) != list(b):
            out.append("wejścia: inna kolejność")
    return out


def check(ws: "Workspace", body: dict) -> list[str]:
    """What changed since a recorded manifest (e.g. `prov.manifest` of a record), from the inventory and `kb/` alone,
    without `.glu/` (ADR-0033). With the task of the same version in the registry the manifest is rebuilt (own
    projection, authority and context selectors included); otherwise each entry is compared with the default
    projection. Empty list: the record's dependencies are as they were."""
    from wgc import tasks
    from wgc.kb import KBError
    task_id, _, version = str(body.get("task", "")).rpartition("@")
    spec = tasks.registry().get(task_id)
    inputs = tuple(e["id"] for e in body.get("inputs", []))
    if spec is not None and spec.version == version:
        try:
            return diff(body, build(ws, spec, inputs).body)
        except KBError:  # an input or document vanished: reported entry by entry below
            pass
    out = []
    if body.get("projection") != PROJECTION_VERSION:
        out.append(f"projection: {body.get('projection')} → {PROJECTION_VERSION}")
    for section in SECTIONS:
        for e in body.get(section, []):
            what = SECTION_PL[section]
            if section == "authority":
                rec = ws.document(e["id"])
            else:
                rec = ws.segment(e["id"])
                if rec is None:
                    rec = next((r for _, d in ws.kb_documents() if isinstance(d, dict)
                                for r in (d.get("records") or []) if isinstance(r, dict) and r.get("id") == e["id"]),
                               None)
            if rec is None:
                out.append(f"{what} {e['id']}: nie istnieje")
                continue
            try:
                current = content_hash(projection(rec, "logic"))
            except ProjectionError as err:
                out.append(f"{what} {e['id']}: {err}")
                continue
            if current != e["hash"]:
                out.append(f"{what} {e['id']}: zmieniony")
    return out
