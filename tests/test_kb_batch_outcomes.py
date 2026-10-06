"""M-STAB2 follow-up (ADR-0031): the three outcomes of a failed batch, crashes during rollback and recovery, journals
of format @0, hashes without a doubled prefix and a consistent read of `kb/` by the validator.

Setup as in test_kb_batch: TAB-4.3 lies in `kb/logic/combat.yaml`, the job changes it and adds TAB-new
(`tables.yaml`), so one acceptance writes two files: index 0 = combat.yaml, index 1 = tables.yaml.
"""
from __future__ import annotations

import dataclasses
import errno
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from glu import planner, reconcile
from glu import exec as executor
from glu.store import Store, db_path
from test_glu_store import Clock, Ids
from test_kb_batch import JOB, combat_file, is_new, is_old, kb_tree, tree, two_file_proposals
from test_kb_safety import ROOT, accept, proposals, tables_file
from test_tables import game  # noqa: F401  (fixture)
from wgc import fsbatch, fsio, kb, tables
from wgc import validate as validate_mod
from wgc.canonical import content_hash, sha256_hex
from wgc.kb import Workspace
from wgc.validate import validate

JOURNAL = Path("kb") / ".wgc-batch"


def manifest(root: Path) -> dict:
    return json.loads((root / JOURNAL / fsbatch.MANIFEST).read_text(encoding="utf-8"))


def fail_marker(monkeypatch, *, intent_fails: bool = False) -> None:
    """Writing the `committed` marker fails (both files are already replaced); optionally the intent too."""
    real = fsbatch._manifest

    def failing(journal, state, *args):
        if state == "committed" or (intent_fails and state == "rolling_back"):
            raise OSError(errno.ENOSPC, f"brak miejsca przy zapisie `{state}` (symulacja)")
        real(journal, state, *args)

    monkeypatch.setattr(fsbatch, "_manifest", failing)


def fail_first_restore(monkeypatch) -> None:
    """The first restore of an old copy fails (later attempts, e.g. a later recovery, work)."""
    real, failed = fsio._replace, []

    def replace(src, dst):
        if str(src).endswith(".old") and not failed:
            failed.append(src)
            raise OSError(errno.EIO, "błąd I/O przy wycofaniu (symulacja)")
        real(src, dst)

    monkeypatch.setattr(fsio, "_replace", replace)


# --- the three outcomes in wgc ----------------------------------------------------------------------------------

def test_marker_and_first_rollback_fail_then_recovery_rolls_back(game, monkeypatch):
    """The scenario of the review: both files replaced, `committed` fails, the first rollback fails. Recovery used to
    go forward (every target new, `prepared`); the recorded intent now makes it roll back."""
    props = two_file_proposals(game)
    before = kb_tree(game)
    fail_marker(monkeypatch)
    fail_first_restore(monkeypatch)
    with pytest.raises(kb.KBUnresolved, match="wycofanie jest przesądzone"):
        accept(game, props, job=JOB)
    monkeypatch.undo()
    assert manifest(game)["state"] == "rolling_back" and is_new(game)  # still the new files, rollback decided
    assert kb.read_receipt(game, JOB) is not None  # evidence kept
    rec = kb.recover(game)
    assert rec.state == "rollback" and kb_tree(game) == before and is_old(game)
    assert kb.recover(game).actions == []
    assert validate([game / "source", game / "kb"]).ok


def test_intent_cannot_be_written_either_so_recovery_decides(game, monkeypatch):
    props = two_file_proposals(game)
    fail_marker(monkeypatch, intent_fails=True)
    fail_first_restore(monkeypatch)
    with pytest.raises(kb.KBUnresolved, match="kierunek .* ustali recovery"):
        accept(game, props, job=JOB)
    monkeypatch.undo()
    assert manifest(game)["state"] == "prepared"
    assert kb.recover(game).state == "forward" and is_new(game)  # every target new: forward is consistent
    assert kb.check_receipt(game, kb.read_receipt(game, JOB)) == []
    assert validate([game / "source", game / "kb"]).ok


def test_completed_rollback_is_a_plain_write_error(game, monkeypatch):
    props = two_file_proposals(game)
    before = kb_tree(game)
    fail_marker(monkeypatch)
    with pytest.raises(kb.KBWriteError, match="Partia wycofana, kb/ bez zmian") as exc:
        accept(game, props, job=JOB)
    assert not isinstance(exc.value, kb.KBUnresolved)
    monkeypatch.undo()
    assert kb_tree(game) == before and not (game / JOURNAL).exists()


# --- the three outcomes in a build ------------------------------------------------------------------------------

def two_file_build(root: Path):
    """A build whose tables job writes two files (TAB-4.3 moved to combat.yaml, changed, plus TAB-new)."""
    assert accept(root, proposals(root)).ok
    tables_file(root).rename(combat_file(root))

    def impl(ws, inputs):
        props = tables.PARSE.deterministic_impl(ws, inputs) + tables.PARSE.deterministic_impl(ws, inputs)
        props[0]["record"]["title"] = "CRT"
        props[1]["record"]["id"] = "TAB-new"
        return props

    spec = dataclasses.replace(tables.PARSE, deterministic_impl=impl)
    ws = Workspace(root)
    plan = planner.plan(ws, "1")
    plan = dataclasses.replace(plan, jobs=[dataclasses.replace(plan.jobs[0], spec=spec)])
    with Store(db_path(root), clock=Clock(), new_id=Ids()) as store:
        return executor.run(store, ws, plan, "p")


def job_state(root: Path) -> tuple[str, str, list[dict]]:
    with Store(db_path(root), create=False) as store:
        [b] = store.builds()
        [j] = store.jobs(b["id"])
        return b["state"], j["state"], store.attempts(j["id"])


@pytest.mark.parametrize("intent_fails, final, kb_after", [(False, "failed", "old"), (True, "done", "new")])
def test_unresolved_acceptance_aborts_the_build_and_reconcile_decides(game, monkeypatch, intent_fails, final,
                                                                       kb_after):
    fail_marker(monkeypatch, intent_fails=intent_fails)
    fail_first_restore(monkeypatch)
    with pytest.raises(kb.KBUnresolved, match="job zostaje w `validating`"):
        two_file_build(game)
    monkeypatch.undo()
    build_state, state, attempts = job_state(game)
    assert (build_state, state, attempts) == ("running", "validating", [])  # nothing decided, nothing discarded
    assert len(kb.receipt_jobs(game)) == 1 and (game / JOURNAL).exists()

    snapshot = tree(game)
    plan = reconcile.reconcile(game, dry_run=True)
    assert any("validating → done albo failed (rozstrzygnie receipt po recovery kb/)" in a for a in plan.actions)
    assert tree(game) == snapshot
    res = reconcile.reconcile(game)
    assert any(a.startswith("kb/: ") for a in res.actions)
    build_state, state, [attempt] = job_state(game)
    assert (state, build_state) == (final, "done" if final == "done" else "failed")
    assert attempt["outcome"] == ("accepted" if final == "done" else "error")
    assert (is_new if kb_after == "new" else is_old)(game)
    assert kb.receipt_jobs(game) == [] and not (game / JOURNAL).exists()
    assert reconcile.reconcile(game).actions == []
    assert validate([game / "source", game / "kb"]).ok


def test_completed_rollback_fails_the_job_at_once(game, monkeypatch):
    fail_marker(monkeypatch)
    res = two_file_build(game)
    monkeypatch.undo()
    build_state, state, [attempt] = job_state(game)
    assert (res.state, state, attempt["outcome"]) == ("failed", "failed", "error")
    assert kb.receipt_jobs(game) == [] and is_old(game)


def test_unresolved_batch_blocks_the_next_build_until_recovery_works(game, monkeypatch):
    """Reconcile at the start of the next build cannot recover kb/ (I/O still failing): the build does not start."""
    fail_marker(monkeypatch)
    fail_first_restore(monkeypatch)
    with pytest.raises(kb.KBUnresolved):
        two_file_build(game)
    monkeypatch.setattr(fsio, "_replace", lambda src, dst: (_ for _ in ()).throw(OSError(errno.EIO, "nadal (symulacja)")))
    with pytest.raises(kb.KBError):
        reconcile.reconcile(game)
    monkeypatch.undo()
    assert job_state(game)[1] == "validating" and len(kb.receipt_jobs(game)) == 1


# --- crashes of a process during rollback and during recovery -----------------------------------------------------

CHILD = """\
import errno
import os
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from wgc import fsbatch, kb, tasks
from wgc.kb import Workspace

root, mode, step = Path(sys.argv[2]), sys.argv[3], sys.argv[4]
fsbatch._step = lambda name: os._exit(9) if name == step else None
if mode == "recover":
    kb.recover(root)
    sys.exit(0)
real = fsbatch._manifest


def manifest(journal, state, *args):
    if state == "committed":
        raise OSError(errno.ENOSPC, "brak miejsca (symulacja)")
    real(journal, state, *args)


fsbatch._manifest = manifest
spec = tasks.get("wgc.tables.parse")
ws = Workspace(root)
I = ("SEG-dsk.4.3",)
props = spec.deterministic_impl(ws, I) + spec.deterministic_impl(ws, I)
props[0]["record"]["title"] = "CRT"
props[1]["record"]["id"] = "TAB-new"
kb.accept(root, spec, I, props, by={"tier": "deterministic", "tool": spec.name}, job="job_000009", ws=ws)
"""


def child(tmp_path: Path, root: Path, mode: str, step: str) -> None:
    script = tmp_path / "child.py"
    script.write_text(CHILD, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(script), str(ROOT), str(root), mode, step], capture_output=True,
                          encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=120)
    assert proc.returncode == 9, (proc.stdout, proc.stderr)


@pytest.mark.parametrize("step", ["rolling_back", "recovered:0"])
def test_crash_during_the_rollback_of_the_writer(game, tmp_path, step):
    """`committed` fails, the writer records the intent and dies before or after restoring the first file."""
    before = (two_file_proposals(game), kb_tree(game))[1]
    child(tmp_path, game, "accept", step)
    assert manifest(game)["state"] == "rolling_back"
    if step == "recovered:0":  # half-way: combat.yaml restored (its copy consumed), tables.yaml still new
        assert tables_file(game).exists() and load_title(game) != "CRT"
    assert kb.recover(game).state == "rollback" and kb_tree(game) == before
    assert kb.recover(game).actions == []


def load_title(root: Path) -> str:
    return validate_mod.load_documents(combat_file(root))[0]["records"][0]["title"]


def test_crash_during_rollback_recovery_then_again(game, tmp_path):
    before = (two_file_proposals(game), kb_tree(game))[1]
    child(tmp_path, game, "accept", "rolling_back")  # journal `rolling_back`, both files new
    child(tmp_path, game, "recover", "recovered:0")  # recovery dies after restoring combat.yaml
    assert manifest(game)["state"] == "rolling_back" and tables_file(game).exists()
    assert kb.recover(game).state == "rollback" and kb_tree(game) == before
    assert kb.recover(game).actions == [] and validate([game / "source", game / "kb"]).ok


def test_crash_during_forward_recovery_then_again(game, tmp_path):
    """A `committed` journal with one file still old (a lost rename): recovery dies while finishing, and the next
    recovery finishes it."""
    two_file_proposals(game)
    crash = tmp_path / "crash.py"
    crash.write_text(CHILD.replace('if mode == "recover":', 'if mode == "recover" or mode == "x":')
                     .replace('if state == "committed":', 'if False:'), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(crash), str(ROOT), str(game), "accept", "replaced:0"],
                          capture_output=True, encoding="utf-8", timeout=120)
    assert proc.returncode == 9, proc.stderr
    doc = manifest(game)
    doc["state"] = "committed"  # as if the marker survived and the second rename was lost
    (game / JOURNAL / fsbatch.MANIFEST).write_text(json.dumps(doc), encoding="utf-8")
    child(tmp_path, game, "recover", "recovered:1")
    assert (game / JOURNAL).exists() and is_new(game)  # finished, journal not removed yet
    assert kb.recover(game).state == "forward" and not (game / JOURNAL).exists()
    assert kb.recover(game).actions == [] and validate([game / "source", game / "kb"]).ok


# --- journal format @0 and hashes ---------------------------------------------------------------------------------

def crashed_at_replaced_0(game: Path, tmp_path: Path) -> None:
    crash = tmp_path / "crash.py"
    crash.write_text(CHILD.replace('if state == "committed":', 'if False:'), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(crash), str(ROOT), str(game), "accept", "replaced:0"],
                          capture_output=True, encoding="utf-8", timeout=120)
    assert proc.returncode == 9, proc.stderr


def test_hashes_have_one_prefix(game, tmp_path):
    two_file_proposals(game)
    crashed_at_replaced_0(game, tmp_path)
    doc = manifest(game)
    assert doc["format"] == fsbatch.FORMAT
    hashes = [h for f in doc["files"] for h in (f["old"], f["new"]) if h]
    assert hashes and all(h.startswith("sha256:") and not h.startswith("sha256:sha256:") for h in hashes)
    kb.recover(game)
    res = accept(game, proposals(game, "TAB-x"), job="job_000010")
    files = {p: p.read_bytes() for p in kb.kb_files(game)}
    assert res.receipt["generation"] == content_hash(sorted([p.relative_to(game).as_posix(), sha256_hex(b)]
                                                            for p, b in files.items()))


@pytest.mark.parametrize("state, outcome", [("prepared", "old"), ("committed", "new")])
def test_journal_of_format_0_is_recovered(game, tmp_path, state, outcome):
    """A journal written before the fix: format @0, hashes `sha256:sha256:<hex>`, mid-batch."""
    two_file_proposals(game)
    crashed_at_replaced_0(game, tmp_path)
    doc = manifest(game)
    doc["format"], doc["state"] = fsbatch.LEGACY_FORMAT, state
    for f in doc["files"]:
        f["old"], f["new"] = [("sha256:" + h) if h else h for h in (f["old"], f["new"])]
    (game / JOURNAL / fsbatch.MANIFEST).write_text(json.dumps(doc), encoding="utf-8")
    assert kb.recover(game).state == {"old": "rollback", "new": "forward"}[outcome]
    assert (is_old if outcome == "old" else is_new)(game)
    assert kb.recover(game).actions == [] and validate([game / "source", game / "kb"]).ok


def test_state_rolling_back_is_not_valid_in_format_0(game, tmp_path):
    two_file_proposals(game)
    crashed_at_replaced_0(game, tmp_path)
    doc = manifest(game)
    doc["format"], doc["state"] = fsbatch.LEGACY_FORMAT, "rolling_back"
    (game / JOURNAL / fsbatch.MANIFEST).write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(kb.KBBatchConflict, match="nieznany format albo stan"):
        kb.recover(game)


# --- consistent read by the validator -----------------------------------------------------------------------------

class Crash(BaseException):
    """Ends a batch half-way inside this process, without the writer's own rollback (like a killed process)."""


def test_batch_during_validation_is_never_reported_as_ok(game, monkeypatch):
    """A whole two-file batch runs after the validator checked for a manifest and read the first file of kb/: the
    result must describe the new version (re-read), not the old file list."""
    props = two_file_proposals(game)
    (game / kb.LOCK_FILE).unlink()  # no lock file: the validator cannot rely on the writer lock
    reads = []

    def batch_now(path):
        reads.append(path.name)
        if reads.count("combat.yaml") == 1 and path.name == "combat.yaml":
            assert accept(game, props).ok
    monkeypatch.setattr(validate_mod, "_after_read", batch_now)
    report = validate([game / "source", game / "kb"])
    monkeypatch.setattr(validate_mod, "_after_read", lambda path: None)
    assert reads.count("combat.yaml") >= 2  # read again after the change
    assert report.ok and report.records == validate([game / "source", game / "kb"]).records and is_new(game)


def two_file_proposals_keeping(root: Path) -> list[dict]:
    """Like `two_file_proposals`, but `tables.yaml` (with TAB-other) stays: the batch changes two existing files."""
    assert accept(root, proposals(root)).ok
    docs = validate_mod.load_documents(tables_file(root))[0]["records"]
    tab = [r for r in docs if r["id"] == "TAB-4.3"]
    rest = [r for r in docs if r["id"] != "TAB-4.3"]
    combat_file(root).write_bytes(kb.dump([{"schema": kb.LOGIC, "records": tab}]).encode("utf-8"))
    tables_file(root).write_bytes(kb.dump([{"schema": kb.LOGIC, "records": rest}]).encode("utf-8"))
    props = proposals(root) + proposals(root, "TAB-new")
    props[0]["record"]["title"] = "CRT"
    return props


def report_ids(root: Path) -> list[str]:
    return [r["id"] for p in kb.kb_files(root) for r in validate_mod.load_documents(p)[0]["records"]]


@pytest.mark.parametrize("with_lock_file", [True, False])
@pytest.mark.parametrize("target", ["kb", "kb/logic", "kb/logic/combat.yaml"])
def test_batch_cut_during_validation_is_pending(game, monkeypatch, target, with_lock_file):
    """A batch starts (and dies half-way) after the validator read the first file of kb/. The validator either
    excludes it (reads one version) or sees it; it never reports OK for a mix. Afterwards the journal is reported as
    pending for `kb`, `kb/logic` and a single file, and the validator writes nothing."""
    import threading
    props = two_file_proposals(game)
    if not with_lock_file:
        (game / kb.LOCK_FILE).unlink()
    old = combat_file(game).read_bytes()

    def crash(name):
        if name == "replaced:0" and threading.current_thread().name == "writer":
            raise Crash()

    def half_batch():
        try:
            accept(game, props)
        except Crash:
            pass
    monkeypatch.setattr(fsbatch, "_step", crash)
    writer = threading.Thread(target=half_batch, name="writer")

    def start_writer(path):
        if path.parent == combat_file(game).parent and not writer.is_alive() and writer.ident is None:
            writer.start()
            writer.join(1.0)  # completes only if the validator does not hold the writer lock
    monkeypatch.setattr(validate_mod, "_after_read", start_writer)
    reads = []
    real_read = validate_mod._read

    def spy(paths):
        out = real_read(paths)
        reads.append({f.name: d for f, d in out[1]})
        return out
    monkeypatch.setattr(validate_mod, "_read", spy)
    report = validate([game / target])
    writer.join(30)
    if report.ok:  # only a consistent old snapshot may pass
        assert reads[-1].get("combat.yaml", old) == old and "tables.yaml" not in reads[-1]
    monkeypatch.setattr(validate_mod, "_after_read", lambda path: None)
    snapshot = tree(game)
    assert "kb_batch_pending" in [d.code for d in validate([game / target]).errors]
    assert tree(game) == snapshot  # the validator writes nothing, not even a lock file
    assert (game / kb.LOCK_FILE).exists()  # created by the writer, never by the validator


def test_kb_that_keeps_changing_is_unstable(game, monkeypatch):
    assert accept(game, proposals(game)).ok
    monkeypatch.setattr(validate_mod, "READ_RETRY_WAIT", 0)
    counter = []

    def touch(path):
        counter.append(path)
        path.write_bytes(path.read_bytes() + b"\n")
    monkeypatch.setattr(validate_mod, "_after_read", touch)
    report = validate([game / "source", game / "kb"])
    assert "kb_read_unstable" in [d.code for d in report.errors] and not report.ok
    assert len([p for p in counter if p.parent.name == "logic"]) == validate_mod.READ_ATTEMPTS


def test_cli_build_with_an_unresolved_acceptance_exits_2(game, monkeypatch, capsys):
    from glu.__main__ import main as glu_main
    assert accept(game, proposals(game)).ok
    tables_file(game).rename(combat_file(game))
    real_plan = planner.plan

    def impl(ws, inputs):
        props = tables.PARSE.deterministic_impl(ws, inputs) + tables.PARSE.deterministic_impl(ws, inputs)
        props[0]["record"]["title"] = "CRT"
        props[1]["record"]["id"] = "TAB-new"
        return props

    def plan(ws, stage, scope="all"):
        p = real_plan(ws, stage, scope)
        spec = dataclasses.replace(tables.PARSE, deterministic_impl=impl)
        return dataclasses.replace(p, jobs=[dataclasses.replace(p.jobs[0], spec=spec)])

    monkeypatch.setattr(planner, "plan", plan)
    fail_marker(monkeypatch)
    fail_first_restore(monkeypatch)
    assert glu_main(["build", "--root", str(game), "--stage", "1"]) == 2
    err = capsys.readouterr().err
    assert "nierozstrzygnięty" in err and "glu reconcile" in err and "validating" in err
    monkeypatch.undo()
    assert job_state(game)[1] == "validating" and len(kb.receipt_jobs(game)) == 1
    assert glu_main(["reconcile", "--root", str(game)]) == 0 and job_state(game)[1] == "failed" and is_old(game)


# --- ABA: batches new → old → new between the reads and the checks of the validator --------------------------------

ORIGINAL = "Combat Results Table"


def aba_setup(root: Path, with_lock_file: bool):
    """Two existing files: combat.yaml (TAB-4.3) and tables.yaml (TAB-other). `batch(version)` changes both titles."""
    assert accept(root, proposals(root, "TAB-other")).ok
    two_file_proposals_keeping(root)  # TAB-4.3 → combat.yaml, TAB-other stays in tables.yaml

    def batch(version: str) -> None:
        props = proposals(root) + proposals(root, "TAB-other")
        if version == "new":
            props[0]["record"]["title"], props[1]["record"]["title"] = "A-new", "B-new"
        res = accept(root, props)
        assert res.ok and len(res.files) == 2, res  # one batch of two files
    batch("new")
    batch("old")
    if not with_lock_file:
        (root / kb.LOCK_FILE).unlink()
    return batch


def title_of(data: bytes | None) -> str:
    doc = [d for d in __import__("yaml").safe_load_all(data.decode("utf-8")) if d][0]
    return doc["records"][0]["title"]


@pytest.mark.parametrize("with_lock_file", [True, False])
def test_aba_batches_between_reads_and_checks_never_give_a_mix(game, monkeypatch, with_lock_file):
    """read combat (old) → batch new → read tables (new) → batch old → check combat (old again, same bytes) → batch
    new → check tables (new): byte comparison alone accepts that mix. Batches run in another thread; each hook waits
    a moment for its batch, so a validator that excludes writers simply reads one version."""
    import queue
    import threading
    batch = aba_setup(game, with_lock_file)
    jobs: queue.Queue = queue.Queue()
    done = []

    def worker():
        while True:
            version = jobs.get()
            if version is None:
                return
            batch(version)
            done.append(version)

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    def run_batch(version):
        jobs.put(version)
        n = len(done) + jobs.qsize()
        deadline = __import__("time").monotonic() + 1.0
        while len(done) < n and __import__("time").monotonic() < deadline:
            __import__("time").sleep(0.01)

    script = {("read", "combat.yaml"): "new", ("read", "tables.yaml"): "old", ("check", "combat.yaml"): "new"}
    fired = set()

    def hook(kind):
        def on(path):
            key = (kind, path.name)
            if key in script and key not in fired:
                fired.add(key)
                run_batch(script[key])
        return on
    monkeypatch.setattr(validate_mod, "_after_read", hook("read"))
    monkeypatch.setattr(validate_mod, "_after_check", hook("check"), raising=False)
    reads = []
    real_read = validate_mod._read

    def spy(paths):
        out = real_read(paths)
        reads.append({f.name: d for f, d in out[1]})
        return out
    monkeypatch.setattr(validate_mod, "_read", spy)
    report = validate([game / "source", game / "kb"])
    jobs.put(None)
    t.join(30)
    used = reads[-1]
    pair = (title_of(used["combat.yaml"]), title_of(used["tables.yaml"]))
    assert pair in ((ORIGINAL, ORIGINAL), ("A-new", "B-new")), (pair, report.ok)
    assert report.ok
    assert done == ["new", "old", "new"] and fired == set(script)  # all three batches ran, after or around the read


def test_validation_of_a_repo_without_lock_file_writes_nothing(game):
    assert accept(game, proposals(game)).ok
    (game / kb.LOCK_FILE).unlink()
    snapshot = tree(game)
    assert validate([game / "source", game / "kb"]).ok and validate([game / "kb" / "logic" / "tables.yaml"]).files == 1
    assert tree(game) == snapshot and not (game / kb.LOCK_FILE).exists()
