"""Reconcile: interrupted builds and jobs brought in line with `kb/` (ADR-0031).

Order: first `kb/` (an interrupted batch finished or rolled back by `wgc.kb.recover`; GLU never touches KB files),
then the job store. Only builds that are not finished and whose liveness lock `.glu/builds/<build>.lock` can be taken
at once are reconciled: a running `glu build` holds that lock, and the OS releases it when the process dies. Every
change uses existing transitions of `glu.states`; the final entries of each job go in one transaction
(`Store.finish_job`):
- `validating` with a receipt that matches `kb/` → Attempt `accepted` with `kb_receipt`, `accepted → done`;
- `validating` without a receipt or with one that `kb/` does not match → Attempt `error`, `failed`;
- `running` → Attempt `error`, `failed`; `accepted` → `done`; any other active state → `cancelled`;
- then the build: `done` when every job is `done`, else `failed`.

Receipts left over for finished or unknown jobs are removed. `dry_run`: the same plan, nothing written (no `.glu/`,
no database, no lock file is created).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from glu import states
from glu.store import Store, StoreError, db_path
from wgc import fsio, kb

# Liveness lock of one build, held by `glu.exec.run` for the whole build.
BUILDS_DIR = Path(".glu") / "builds"
# Short lock around the start of a build (reconcile + creating the build and taking its liveness lock), so that a
# build being created is never taken for a dead one.
START_LOCK = Path(".glu") / "build.lock"
START_TIMEOUT = 60.0
REASON = "reconcile"
# Job states with nothing left to reconcile.
SETTLED = states.JOB_TERMINAL | {"done", "stale"}


def run_lock_path(root: str | Path, build_id: str) -> Path:
    return Path(root) / BUILDS_DIR / f"{build_id}.lock"


@dataclass
class Reconciliation:
    actions: list[str] = field(default_factory=list)   # Polish, one line per change (or planned change)

    @property
    def changed(self) -> bool:
        return bool(self.actions)


def _dead(root: Path, build_id: str, dry_run: bool) -> bool:
    """No process holds the liveness lock of the build (it crashed, or predates the lock)."""
    path = run_lock_path(root, build_id)
    if dry_run and not path.is_file():
        return True
    try:
        with fsio.exclusive(path, 0):
            pass
    except fsio.LockBusy:
        return False
    if not dry_run:
        try:
            path.unlink()
        except OSError:
            pass
    return True


def _job(root: Path, store: Store, job: dict, dry_run: bool) -> str | None:
    jid, state = job["id"], job["state"]
    tier = job.get("tier") or "deterministic"
    if state in SETTLED:
        return None
    if state in ("validating", "running"):
        receipt = kb.read_receipt(root, jid) if state == "validating" else None
        diff = kb.check_receipt(root, receipt, dry_run=dry_run) if receipt is not None else None
        if receipt is not None and not diff:
            records = list(receipt["records"])
            if not dry_run:
                store.finish_job(jid, tier, "accepted",
                                 [("accepted", {"accepted_records": records, "reason": f"{REASON}: kb/ ma wynik joba"}),
                                  ("done", {"reason": REASON})],
                                 schema_valid=True, domain_valid=True, kb_receipt=receipt)
            return f"{jid}: {state} → done (kb/ zawiera wynik joba: {', '.join(records) or 'bez rekordów'})"
        if dry_run and receipt is not None and kb.pending_batch(root):
            return f"{jid}: {state} → done albo failed (rozstrzygnie receipt po recovery kb/)"
        if state == "running":
            why = "proces zakończył się przed akceptacją wyniku"
        elif receipt is None:
            why = "akceptacja nie została zatwierdzona (brak receiptu)"
        else:
            why = "kb/ nie zawiera wyniku z receiptu: " + "; ".join(diff)
        if not dry_run:
            store.finish_job(jid, tier, "error", [("failed", {"reason": f"{REASON}: {why}"})],
                             error_class="runtime", validation_errors=[f"{REASON}: {why}"])
        return f"{jid}: {state} → failed ({why})"
    if state == "accepted":
        if not dry_run:
            store.transition_job(jid, "done", reason=REASON)
        return f"{jid}: accepted → done"
    if not dry_run:
        store.transition_job(jid, "cancelled", reason=f"{REASON}: build przerwany")
    return f"{jid}: {state} → cancelled (build przerwany)"


def _build(root: Path, store: Store, build: dict, dry_run: bool) -> list[str]:
    actions = []
    jobs = store.jobs(build["id"])
    for job in jobs:
        line = _job(root, store, job, dry_run)
        if line:
            actions.append(line)
            if not dry_run:
                kb.discard_receipt(root, job["id"])
    final = [store.job(j["id"])["state"] for j in jobs] if not dry_run else []
    done = sum(1 for s in final if s == "done")
    if dry_run:
        actions.append(f"{build['id']}: {build['state']} → done albo failed (build przerwany)")
        return actions
    metrics = {"jobs_total": len(jobs), "jobs_done": done, "jobs_failed": len(jobs) - done}
    if build["state"] == "running" and done == len(jobs):
        store.transition_build(build["id"], "done", reason=f"{REASON}: build przerwany", metrics=metrics)
        actions.append(f"{build['id']}: running → done")
    else:
        store.transition_build(build["id"], "failed", reason=f"{REASON}: build przerwany", metrics=metrics)
        actions.append(f"{build['id']}: {build['state']} → failed (jobów niezakończonych sukcesem: "
                       f"{len(jobs) - done})")
    return actions


def reconcile(root: str | Path, store: Store | None = None, dry_run: bool = False) -> Reconciliation:
    """Recover `kb/`, then reconcile dead builds of the store (see the module docstring). Idempotent: a second run
    changes nothing. `store`: an open store (the build start passes its own); else `.glu/state.db`, if it exists."""
    root = Path(root)
    out = Reconciliation()
    if kb.pending_batch(root) or fsio.temp_files(root / kb.KB_DIR):
        out.actions += [f"kb/: {a}" for a in kb.recover(root, dry_run=dry_run).actions]
    if store is None:
        if not db_path(root).is_file():
            return out
        with Store.at_root(root, create=False) as own:
            return _store(root, own, dry_run, out)
    return _store(root, store, dry_run, out)


def _store(root: Path, store: Store, dry_run: bool, out: Reconciliation) -> Reconciliation:
    for build in store.builds():
        if build["state"] not in states.BUILD_TERMINAL and _dead(root, build["id"], dry_run):
            out.actions += _build(root, store, build, dry_run)
    for jid in kb.receipt_jobs(root):
        try:
            state = store.job(jid)["state"]
        except StoreError:
            state = None
        if state is None or state in SETTLED:
            out.actions.append(f"usunięcie osieroconego receiptu {jid}")
            if not dry_run:
                kb.discard_receipt(root, jid)
    return out
