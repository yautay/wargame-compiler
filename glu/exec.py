"""Tier 0 executor: runs the deterministic implementation of planned jobs (ADR-0025).

Every state change goes through `glu.store` and the transition tables of `glu.states` (ADR-0023):
- job: `pending → ready → running → proposed → validating → accepted → done`; an exception in the implementation
  is `running → failed`, a rejected output (schema, domain, conflict) is `validating → failed`. During acceptance
  three outcomes are kept apart: rejected output (Attempt `rejected`), operational failure of `accept()` (`KBError`:
  busy lock, stale inventory, failed write; Attempt `error`) and a program error (any other exception; Attempt
  `error`, message `błąd programu: …`). Both errors also end in `validating → failed`, so no job stays `validating`;
- build: `planning → running → done`, or `running → failed` when any job failed. The executor sets the build state;
  it is never derived from job states by the store.
Each run is one Attempt (`tier: deterministic`). The output goes to `wgc.kb.accept`, which decides provenance and is
the only writer of `kb/`: the executor never writes KB YAML. No routing decision is recorded (router: M12).
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from glu.planner import Plan, PlannedJob
from glu.store import Store
from wgc import kb
from wgc.kb import Workspace


@dataclass
class JobResult:
    id: str
    task: str
    inputs: list[str]
    state: str
    records: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


@dataclass
class BuildResult:
    id: str
    project: str
    stage: str
    scope: str
    state: str
    jobs: list[JobResult]
    metrics: dict


# Transition reasons of operational `accept()` failures (all are Attempts with `outcome: error`, not `rejected`).
_KB_FAILURES = {kb.KBBusy: "kb/ zajęte przez innego pisarza", kb.KBStale: "inwentarz zmienił się w trakcie joba",
                kb.KBWriteError: "awaria zapisu kb/"}


def _where(e: BaseException) -> str:
    """` (file:line)` of the innermost frame, so a program error can be found without a traceback."""
    tb = e.__traceback__
    while tb is not None and tb.tb_next is not None:
        tb = tb.tb_next
    return f" ({Path(tb.tb_frame.f_code.co_filename).name}:{tb.tb_lineno})" if tb is not None else ""


def run_job(store: Store, ws: Workspace, job_id: str, planned: PlannedJob, counts: Counter) -> JobResult:
    spec, tier = planned.spec, planned.tier
    result = JobResult(job_id, spec.id, list(planned.inputs), "failed")
    store.transition_job(job_id, "ready")
    store.transition_job(job_id, "running")
    try:
        proposals = spec.deterministic_impl(ws, planned.inputs)
    except Exception as e:  # a bug or unreadable input of one task must not stop the build
        result.issues = [f"{type(e).__name__}: {e}"]
        store.add_attempt(job_id, tier, "error", error_class="runtime", validation_errors=result.issues)
        store.transition_job(job_id, "failed", reason="błąd implementacji deterministycznej")
        return result
    store.transition_job(job_id, "proposed")
    store.transition_job(job_id, "validating")
    try:
        accepted = kb.accept(ws.root, spec, planned.inputs, proposals, by={"tier": tier, "tool": spec.name},
                             job=job_id, ws=ws)
    except kb.KBError as e:  # operational: the output was not judged, so it is an error, not a rejection
        result.issues = [str(e)]
        store.add_attempt(job_id, tier, "error", error_class="runtime", validation_errors=result.issues)
        store.transition_job(job_id, "failed", reason=_KB_FAILURES.get(type(e), "błąd odczytu KB"))
        return result
    except Exception as e:  # a bug in WGC or in the task's `validate`: never reported as a bad output
        result.issues = [f"błąd programu: {type(e).__name__}: {e}{_where(e)}"]
        store.add_attempt(job_id, tier, "error", error_class="runtime", validation_errors=result.issues)
        store.transition_job(job_id, "failed", reason="błąd programu w akceptacji")
        return result
    fields = {"schema_valid": accepted.schema_valid, "domain_valid": accepted.domain_valid}
    if not accepted.ok:
        result.issues = accepted.issues
        store.add_attempt(job_id, tier, "rejected", validation_errors=accepted.issues, **fields)
        store.transition_job(job_id, "failed", reason="wynik odrzucony przez WGC")
        return result
    store.add_attempt(job_id, tier, "accepted", **fields)
    store.transition_job(job_id, "accepted", accepted_records=accepted.records)
    store.transition_job(job_id, "done")
    counts.update(created=len(accepted.created), updated=len(accepted.updated), unchanged=len(accepted.unchanged))
    result.state, result.records = "done", accepted.records
    return result


def run(store: Store, ws: Workspace, plan: Plan, project: str) -> BuildResult:
    """Create the build, run every job of the plan and set the final build state."""
    build_id = store.create_build(project, plan.stage, scope=plan.scope)
    store.transition_build(build_id, "running")
    job_ids = [store.create_job(build_id, p.spec.id, list(p.inputs), p.cache_key, tier=p.tier) for p in plan.jobs]
    counts: Counter = Counter()
    results = [run_job(store, ws, job_id, p, counts) for job_id, p in zip(job_ids, plan.jobs)]
    failed = sum(1 for r in results if r.state != "done")
    metrics = {"jobs_total": len(results), "jobs_deterministic": len(results), "jobs_done": len(results) - failed,
               "jobs_failed": failed, "records_created": counts["created"], "records_updated": counts["updated"],
               "records_unchanged": counts["unchanged"]}
    if failed:
        build = store.transition_build(build_id, "failed", reason=f"jobów nieudanych: {failed}", metrics=metrics)
    else:
        build = store.transition_build(build_id, "done", metrics=metrics)
    return BuildResult(build_id, project, plan.stage, plan.scope, build["state"], results, metrics)
