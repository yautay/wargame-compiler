"""Build planner: stage + scope → jobs (task, inputs, manifest, cache key), from the WGC task registry (ADR-0025).

Planning only reads: the inventory, segment text (checked against `text_hash` and `struct_hash`, so a stale
`.glu/source/` or an inventory from an extractor before ADR-0032 fails here, before a build exists) and `kb/`. The
job key comes from the job manifest (`wgc.manifest.build`, ADR-0033), the same definition `wgc.kb.accept()` records
in `prov.manifest`: `input_hash` covers the inputs (a segment's `logic` projection has `struct_hash`, ADR-0032) and
the authority data of source documents, `context_hash` the `kb/` records read as context. It writes nothing, which
is what `glu build --dry-run` shows. Gate checks join the planner in M12, the cache in M11: until then every planned
job runs.
"""
from __future__ import annotations

from dataclasses import dataclass

from wgc import manifest as manifests, tasks
from wgc.canonical import content_hash
from wgc.kb import Workspace
from wgc.manifest import Manifest
from wgc.tasks import Inputs, TaskSpec

DETERMINISTIC = "deterministic"
EMPTY_CONTEXT = content_hash([])  # context hash of a task that reads no kb/ records


@dataclass(frozen=True)
class PlannedJob:
    spec: TaskSpec
    inputs: Inputs
    manifest: Manifest      # what the job reads (ADR-0033); the executor checks it again before running
    cache_key: dict
    tier: str


@dataclass(frozen=True)
class Plan:
    stage: str              # `stage1`
    scope: str              # `all`, `chapter:N`, `segment:SEG-…`
    jobs: list[PlannedJob]
    skipped: list[str]      # tasks of the stage without a Tier 0 implementation (executors from M10)


def cache_key(spec: TaskSpec, manifest: Manifest) -> dict:
    """Components of the job's cache key (`glu/exec@0#cache_key`) from its manifest; no prompt or profile for Tier 0."""
    return {"task": spec.id, "task_version": spec.version, "output_schema": spec.output_schema,
            "input_hash": manifest.input_hash, "context_hash": manifest.context_hash}


def plan(ws: Workspace, stage: str, scope: str | None = None) -> Plan:
    """Jobs of a build. Raises `wgc.tasks.TaskError` (stage, scope) or `wgc.kb.KBError` (inventory, text)."""
    specs = tasks.for_stage(stage)
    scope = scope or "all"
    segments = tasks.select(ws, scope)
    jobs, skipped = [], []
    for spec in specs:
        if spec.deterministic_impl is None:
            skipped.append(spec.name)
            continue
        for inputs in spec.input_selector(ws, segments):
            for sid in inputs:
                if ws.segment(sid) is not None:
                    ws.text(sid)
            m = manifests.build(ws, spec, inputs)
            jobs.append(PlannedJob(spec, inputs, m, cache_key(spec, m), DETERMINISTIC))
    return Plan(tasks.stage_name(stage), scope, jobs, skipped)
