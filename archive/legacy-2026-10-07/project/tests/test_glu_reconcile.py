"""M-STAB2: final store entries in one transaction and reconcile of interrupted builds (glu.reconcile, ADR-0031).

F04 of the review: `kb/` written, then the store write fails (or the process dies) before the Attempt. Reconcile
brings each job of a dead build in line with `kb/`; a live build (its liveness lock held) is never touched.
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from glu import reconcile, states
from glu.__main__ import main
from glu.store import Store, StoreError, db_path
from test_glu_build import CONCEPTS, build, tree
from test_glu_store import Clock, Ids
from test_kb_safety import ROOT
from test_tables import game  # noqa: F401  (fixture)
from wgc import contracts, fsio, kb
from wgc.validate import validate

STUCK = ("validating", "running", "proposed", "ready", "pending")
KEY = {"task": "wgc.tables.parse", "task_version": "0", "output_schema": "wgc/logic@0#table",
       "input_hash": "sha256:" + "0" * 16, "context_hash": "sha256:" + "0" * 16}


def store_of(root: Path) -> Store:
    return Store(db_path(root), create=False)


def fail_store_after_first_accept(monkeypatch) -> None:
    """`Store.finish_job` fails for the first accepted job: kb/ already holds its result (F04, P8 of the review)."""
    real = Store.finish_job

    def failing(self, job_id, tier, outcome, steps, **fields):
        if outcome == "accepted":
            raise StoreError("baza stanu niedostępna (symulacja)")
        return real(self, job_id, tier, outcome, steps, **fields)

    monkeypatch.setattr(Store, "finish_job", failing)


def test_finish_job_is_one_transaction(game):
    with Store(db_path(game), clock=Clock(), new_id=Ids()) as store:
        b = store.create_build("p", "stage1")
        store.transition_build(b, "running")
        j = store.create_job(b, "wgc.tables.parse", ["SEG-dsk.4.3"], KEY)
        for s in ("ready", "running", "proposed", "validating"):
            store.transition_job(j, s)
        with pytest.raises(states.IllegalTransition):  # the second step is illegal: nothing of it is kept
            store.finish_job(j, "deterministic", "accepted", [("accepted", {"accepted_records": []}), ("pending", {})])
        assert store.attempts(j) == [] and store.job(j)["state"] == "validating"
        store.finish_job(j, "deterministic", "accepted", [("accepted", {"accepted_records": []}), ("done", {})])
        assert [a["outcome"] for a in store.attempts(j)] == ["accepted"] and store.job(j)["state"] == "done"


def test_accepted_attempt_carries_the_receipt(game):
    res = build(game)
    with store_of(game) as store:
        [attempt] = store.attempts(res.jobs[1].id)
        assert list(attempt["kb_receipt"]["records"]) == CONCEPTS
        assert kb.check_receipt(game, attempt["kb_receipt"]) == []
        assert contracts.errors(store.export()) == []
    assert kb.receipt_jobs(game) == []  # discarded once the Attempt holds it


def test_store_failure_after_kb_write_is_reconciled(game, monkeypatch):
    fail_store_after_first_accept(monkeypatch)
    with pytest.raises(StoreError):
        build(game)
    monkeypatch.undo()
    with store_of(game) as store:
        [b] = store.builds()
        jobs = store.jobs(b["id"])
        assert b["state"] == "running" and [j["state"] for j in jobs] == ["validating", "pending"]
        assert store.attempts(jobs[0]["id"]) == []  # no Attempt without its transitions
    assert kb.receipt_jobs(game) == [jobs[0]["id"]]

    snapshot = tree(game)
    plan = reconcile.reconcile(game, dry_run=True)
    assert plan.actions and tree(game) == snapshot

    res = reconcile.reconcile(game)
    assert any("validating → done" in a for a in res.actions)
    with store_of(game) as store:
        b = store.build(b["id"])
        tab, harvest = store.jobs(b["id"])
        assert (tab["state"], harvest["state"], b["state"]) == ("done", "cancelled", "failed")
        assert tab["accepted_records"] == ["TAB-4.3"]
        [attempt] = store.attempts(tab["id"])
        assert attempt["outcome"] == "accepted" and attempt["kb_receipt"]["records"].keys() == {"TAB-4.3"}
        assert store.history(tab["id"])[-2]["reason"].startswith("reconcile")
        assert contracts.errors(store.export()) == []
    assert kb.receipt_jobs(game) == []
    assert reconcile.reconcile(game).actions == []  # idempotent

    nxt = build(game)  # the next build finishes the work; kb/ stays valid
    assert nxt.state == "done" and nxt.reconciled == []
    assert validate([game / "source", game / "kb"]).ok


def _stuck_build(game: Path, state: str) -> tuple[str, str]:
    """A dead build with one job left in `state` (as after a crash)."""
    with Store(db_path(game)) as store:
        b = store.create_build("p", "stage1")
        store.transition_build(b, "running")
        j = store.create_job(b, "wgc.tables.parse", ["SEG-dsk.4.3"], KEY, tier="deterministic")
        path = ["ready", "running", "proposed", "validating"]
        for s in path[:path.index(state) + 1] if state != "pending" else []:
            store.transition_job(j, s)
    return b, j


@pytest.mark.parametrize("state, final", [("validating", "failed"), ("running", "failed"), ("proposed", "cancelled"),
                                          ("ready", "cancelled"), ("pending", "cancelled")])
def test_job_without_a_confirmed_result(game, state, final):
    b, j = _stuck_build(game, state)
    res = reconcile.reconcile(game)
    assert f"{j}: {state} → {final}" in "\n".join(res.actions)
    with store_of(game) as store:
        assert store.job(j)["state"] == final and store.build(b)["state"] == "failed"
        if final == "failed":
            [attempt] = store.attempts(j)
            assert attempt["outcome"] == "error" and attempt["error_class"] == "runtime"
    assert reconcile.reconcile(game).actions == []


def test_receipt_that_kb_does_not_confirm(game):
    """The receipt is written before kb/: a write that never happened (or was rolled back) is not accepted."""
    b, j = _stuck_build(game, "validating")
    kb._write_receipt(game, j, {"generation": "sha256:" + "1" * 16, "records": {"TAB-4.3": "sha256:" + "2" * 16}})
    res = reconcile.reconcile(game)
    assert any("kb/ nie zawiera wyniku z receiptu: TAB-4.3: brak w kb/" in a for a in res.actions)
    with store_of(game) as store:
        assert store.job(j)["state"] == "failed"
    assert kb.receipt_jobs(game) == []


def test_live_build_is_not_touched(game):
    b, j = _stuck_build(game, "validating")
    held, release = threading.Event(), threading.Event()

    def alive():
        with fsio.exclusive(reconcile.run_lock_path(game, b), 0):
            held.set()
            release.wait(10)

    t = threading.Thread(target=alive)
    t.start()
    assert held.wait(10)
    try:
        assert reconcile.reconcile(game).actions == []
        with store_of(game) as store:
            assert store.job(j)["state"] == "validating"
    finally:
        release.set()
        t.join(10)
    assert reconcile.reconcile(game).actions  # dead now


def test_build_start_reconciles_and_leaves_no_lock(game, monkeypatch):
    fail_store_after_first_accept(monkeypatch)
    with pytest.raises(StoreError):
        build(game)
    monkeypatch.undo()
    res = build(game)
    assert res.state == "done" and any("validating → done" in a for a in res.reconciled)
    assert list((game / reconcile.BUILDS_DIR).glob("*.lock")) == []
    with store_of(game) as store:
        assert all(j["state"] not in STUCK for b in store.builds() for j in store.jobs(b["id"]))


CHILD = """\
import os
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from glu import exec as executor, planner
from glu.store import Store
from wgc.kb import Workspace

root = Path(sys.argv[2])
real = Store.finish_job


def die_after_kb(self, job_id, tier, outcome, steps, **fields):
    if outcome == "accepted":
        os._exit(9)  # kb/ and the receipt are written, the Attempt is not
    return real(self, job_id, tier, outcome, steps, **fields)


Store.finish_job = die_after_kb
ws = Workspace(root)
with Store.at_root(root) as store:
    executor.run(store, ws, planner.plan(ws, "1"), "p")
"""


def test_killed_build_process_is_reconciled(game, tmp_path):
    script = tmp_path / "child.py"
    script.write_text(CHILD, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(script), str(ROOT), str(game)], capture_output=True, encoding="utf-8",
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=120)
    assert proc.returncode == 9, (proc.stdout, proc.stderr)
    res = reconcile.reconcile(game)  # the OS released the liveness lock of the dead process
    assert any("validating → done" in a for a in res.actions)
    with store_of(game) as store:
        [b] = store.builds()
        assert [j["state"] for j in store.jobs(b["id"])] == ["done", "cancelled"] and b["state"] != "running"


# --- CLI ---------------------------------------------------------------------------------------------------------

def test_cli_reconcile_on_a_clean_repo_writes_nothing(game, capsys):
    before = tree(game)
    assert main(["reconcile", "--root", str(game), "--dry-run"]) == 0
    assert main(["reconcile", "--root", str(game)]) == 0
    assert "Nic do uzgodnienia" in capsys.readouterr().out and tree(game) == before
    build(game)
    before = tree(game)
    assert main(["reconcile", "--root", str(game)]) == 0
    assert "Nic do uzgodnienia" in capsys.readouterr().out and tree(game) == before


def test_cli_reconcile_waits_for_a_starting_build(game, capsys, monkeypatch):
    """A build that is being created (start lock held, liveness lock not yet taken) is not taken for a dead one."""
    with Store(db_path(game)) as store:
        b = store.create_build("p", "stage1")  # `planning`, no liveness lock yet
    monkeypatch.setattr(reconcile, "START_TIMEOUT", 0.2)
    held, release = threading.Event(), threading.Event()

    def starting():
        with fsio.exclusive(game / reconcile.START_LOCK, 5):
            held.set()
            release.wait(10)

    t = threading.Thread(target=starting)
    t.start()
    assert held.wait(10)
    try:
        assert main(["reconcile", "--root", str(game)]) == 2
        assert "startuje" in capsys.readouterr().err
        with store_of(game) as store:
            assert store.build(b)["state"] == "planning"
    finally:
        release.set()
        t.join(10)


def test_cli_reconcile_dry_run_then_real(game, capsys, monkeypatch):
    fail_store_after_first_accept(monkeypatch)
    with pytest.raises(StoreError):
        build(game)
    monkeypatch.undo()
    before = tree(game)
    assert main(["reconcile", "--root", str(game), "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "Plan reconcile (bez zapisu)" in out and "validating → done" in out and "Niczego nie zapisano" in out
    assert tree(game) == before
    assert main(["reconcile", "--root", str(game)]) == 0
    assert "validating → done" in capsys.readouterr().out
    assert main(["status", "--root", str(game)]) == 0
    assert "validating" not in capsys.readouterr().out
