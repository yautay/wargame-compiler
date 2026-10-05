"""Build planner: stage + scope → jobs (task, inputs, cache key), from the WGC task registry (ADR-0025).

Planning only reads: the inventory, segment text (checked against `text_hash`, so a stale `.glu/source/` fails
here, before a build exists) and `kb/`. It writes nothing, which is what `glu build --dry-run` shows. Gate checks
join the planner in M12, the cache in M11: until then every planned job runs.
"""
from __future__ import annotations

from dataclasses import dataclass

from wgc import tasks
from wgc.canonical import content_hash
from wgc.kb import Workspace
from wgc.tasks import Inputs, TaskSpec

DETERMINISTIC = "deterministic"
EMPTY_CONTEXT = content_hash([])  # Tier 0 tasks get no model context


@dataclass(frozen=True)
class PlannedJob:
    spec: TaskSpec
    inputs: Inputs
    cache_key: dict
    tier: str


@dataclass(frozen=True)
class Plan:
    stage: str              # `stage1`
    scope: str              # `all`, `chapter:N`, `segment:SEG-…`
    jobs: list[PlannedJob]
    skipped: list[str]      # tasks of the stage without a Tier 0 implementation (executors from M10)


def cache_key(spec: TaskSpec, ws: Workspace, inputs: Inputs) -> dict:
    """Components of the job's cache key (`glu/exec@0#cache_key`); no prompt or profile for Tier 0."""
    return {"task": spec.id, "task_version": spec.version, "output_schema": spec.output_schema,
            "input_hash": spec.input_hash(ws, inputs), "context_hash": EMPTY_CONTEXT}


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
            jobs.append(PlannedJob(spec, inputs, cache_key(spec, ws, inputs), DETERMINISTIC))
    return Plan(tasks.stage_name(stage), scope, jobs, skipped)
