"""Tier 0 executor: runs the deterministic implementation of planned jobs (ADR-0025).

Every state change goes through `glu.store` and the transition tables of `glu.states` (ADR-0023):
- job: `pending → ready → running → proposed → validating → accepted → done`; an exception in the implementation
  is `running → failed`, a rejected output (schema, domain, conflict) is `validating → failed`. During acceptance
  three outcomes are kept apart: rejected output (Attempt `rejected`), operational failure of `accept()` (`KBError`:
  busy lock, stale inventory, failed write; Attempt `error`) and a program error (any other exception; Attempt
  `error`, message `błąd programu: …`). Both errors also end in `validating → failed`. The one exception is
  `kb.KBUnresolved` (a batch whose rollback did not complete, ADR-0031): no Attempt is written, the receipt is kept,
  the job stays `validating` and the build is aborted (the exception propagates), so reconcile decides it from `kb/`;
- build: `planning → running → done`, or `running → failed` when any job failed. The executor sets the build state;
  it is never derived from job states by the store.
Each run is one Attempt (`tier: deterministic`). The output goes to `wgc.kb.accept`, which decides provenance and is
the only writer of `kb/`: the executor never writes KB YAML. No routing decision is recorded (router: M12).

Before the implementation runs, the job manifest is computed again (`wgc.manifest.build`, ADR-0033). For a task that
reads `kb/` it is computed on a workspace pinned to one `kb/` snapshot, and the implementation reads the same
snapshot; `accept()` gets that manifest and refuses it when the context changed meanwhile (`KBContextStale`). A
manifest different from the planned one (e.g. an earlier job of this build changed the context) fails the job before
anything runs, so the job key in the store and `prov.manifest` never disagree; ordering jobs is M13.

The final entries of a job (the Attempt, with `kb_receipt` when accepted, and its last transitions) go in one store
transaction (`Store.finish_job`). A build starts with reconcile of interrupted builds and `kb/` (`glu.reconcile`) and
holds its liveness lock until it ends (ADR-0031).
"""
from __future__ import annotations

import contextlib
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from glu import reconcile
from glu.planner import Plan, PlannedJob, cache_key
from glu.store import Store, StoreError
from wgc import fsio, kb, manifest as manifests
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
    reconciled: list[str] = field(default_factory=list)  # what reconcile changed at the start of the build


# Transition reasons of operational `accept()` failures (all are Attempts with `outcome: error`, not `rejected`).
_KB_FAILURES = {kb.KBBusy: "kb/ zajęte przez innego pisarza", kb.KBStale: "inwentarz zmienił się w trakcie joba",
                kb.KBContextStale: "kontekst kb/ zmienił się między wykonaniem a akceptacją",
                kb.KBWriteError: "awaria zapisu kb/", kb.KBBatchConflict: "przerwana partia kb/ wymaga decyzji"}


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

    def finish(outcome: str, steps: list, **fields) -> None:
        store.finish_job(job_id, tier, outcome, steps, **fields)
        kb.discard_receipt(ws.root, job_id)  # the Attempt holds it now; kept if the store write failed (reconcile)

    def error(reason: str) -> JobResult:
        finish("error", [("failed", {"reason": reason})], error_class="runtime", validation_errors=result.issues)
        return result

    try:  # what the job reads, again: kb/ reads from one snapshot that the implementation reads too (ADR-0033)
        jws = ws.pinned(kb.snapshot(ws.root)) if manifests.reads_kb(ws, spec, planned.inputs) else ws
        manifest = manifests.build(jws, spec, planned.inputs)
    except kb.KBError as e:
        result.issues = [str(e)]
        return error("nie można odczytać wejść joba")
    if cache_key(spec, manifest) != planned.cache_key:
        result.issues = ["wejścia joba zmieniły się od planu: " + "; ".join(manifests.diff(planned.manifest.body,
                                                                                         manifest.body))]
        return error("wejścia joba zmieniły się od planu")
    try:
        proposals = spec.deterministic_impl(jws, planned.inputs)
    except Exception as e:  # a bug or unreadable input of one task must not stop the build
        result.issues = [f"{type(e).__name__}: {e}"]
        return error("błąd implementacji deterministycznej")
    store.transition_job(job_id, "proposed")
    store.transition_job(job_id, "validating")
    try:
        accepted = kb.accept(ws.root, spec, planned.inputs, proposals, by={"tier": tier, "tool": spec.name},
                             job=job_id, ws=jws, manifest=manifest)
    except kb.KBUnresolved as e:  # the outcome is not decided: keep the evidence (receipt, journal) for reconcile
        raise kb.KBUnresolved(f"job {job_id}: {e} Build przerwany: job zostaje w `validating` do reconcile.") from e
    except kb.KBError as e:  # operational: the output was not judged, so it is an error, not a rejection
        result.issues = [str(e)]
        return error(_KB_FAILURES.get(type(e), "błąd odczytu KB"))
    except Exception as e:  # a bug in WGC or in the task's `validate`: never reported as a bad output
        result.issues = [f"błąd programu: {type(e).__name__}: {e}{_where(e)}"]
        return error("błąd programu w akceptacji")
    fields = {"schema_valid": accepted.schema_valid, "domain_valid": accepted.domain_valid}
    if not accepted.ok:
        result.issues = accepted.issues
        finish("rejected", [("failed", {"reason": "wynik odrzucony przez WGC"})], validation_errors=accepted.issues,
               **fields)
        return result
    finish("accepted", [("accepted", {"accepted_records": accepted.records}), ("done", {})],
           kb_receipt=accepted.receipt, **fields)
    counts.update(created=len(accepted.created), updated=len(accepted.updated), unchanged=len(accepted.unchanged))
    result.state, result.records = "done", accepted.records
    return result


def run(store: Store, ws: Workspace, plan: Plan, project: str) -> BuildResult:
    """Reconcile interrupted builds, create the build, run every job of the plan and set the final build state.
    The build holds its liveness lock (`glu.reconcile.run_lock_path`) until it returns or raises."""
    root = ws.root
    with contextlib.ExitStack() as alive:
        try:
            with fsio.exclusive(root / reconcile.START_LOCK, reconcile.START_TIMEOUT):
                notes = reconcile.reconcile(root, store).actions
                build_id = store.create_build(project, plan.stage, scope=plan.scope)
                lock = reconcile.run_lock_path(root, build_id)
                alive.callback(_remove, lock)  # registered first, so it runs after the lock is released
                alive.enter_context(fsio.exclusive(lock, 0))
        except fsio.LockBusy:
            raise StoreError(f"inny `glu build` tej gry startuje dłużej niż {reconcile.START_TIMEOUT:g} s "
                             f"({reconcile.START_LOCK.as_posix()}); ponów") from None
        store.transition_build(build_id, "running")
        job_ids = [store.create_job(build_id, p.spec.id, list(p.inputs), p.cache_key, tier=p.tier)
                   for p in plan.jobs]
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
    return BuildResult(build_id, project, plan.stage, plan.scope, build["state"], results, metrics, notes)


def _remove(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass
