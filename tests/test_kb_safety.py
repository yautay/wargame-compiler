"""M-STAB1: safe KB writes (F01), one writer per project (F02) and typed diagnostics for wrong proposals (F08).

Review: docs/reviews/2026-10-05-przeglad-po-M9a.md. Decision: ADR-0026. The faults are injected (exceptions in
`os.replace`/`os.fsync`); a power cut or a killed process during `fsync` is not simulated here.
"""
from __future__ import annotations

import dataclasses
import errno
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from test_tables import game  # noqa: F401  (fixture)
from wgc import fsio, kb, source, tasks
from wgc.kb import Workspace
from wgc.validate import load_documents, validate

ROOT = Path(__file__).resolve().parent.parent
SEG = "SEG-dsk.4.3"
INPUTS = (SEG,)
BY = {"tier": "deterministic", "tool": "wgc.tables.parse@0"}
SPEC = tasks.get("wgc.tables.parse")


def proposals(root: Path, rid: str | None = None, ws: Workspace | None = None) -> list[dict]:
    props = SPEC.deterministic_impl(ws or Workspace(root), INPUTS)
    if rid:
        props[0]["record"]["id"] = rid
    return props


def accept(root: Path, props, **kw) -> kb.AcceptResult:
    return kb.accept(root, SPEC, INPUTS, props, by=BY, **kw)


def tables_file(root: Path) -> Path:
    return root / "kb" / "logic" / "tables.yaml"


def table_ids(root: Path) -> list[str]:
    return [r["id"] for r in load_documents(tables_file(root))[0]["records"]]


def lock_file(root: Path) -> Path:
    return root / kb.LOCK_FILE


def fail_with(err: OSError):
    def boom(*args, **kwargs):
        raise err
    return boom


# --- F01: atomic replacement of one file ------------------------------------------------------------------------

def test_atomic_write_creates_and_replaces_without_temp_files(tmp_path):
    target = tmp_path / "d" / "f.yaml"
    fsio.atomic_write(target, b"one\n")
    fsio.atomic_write(target, "dwa\nłódź\n".encode("utf-8"))
    assert target.read_bytes() == "dwa\nłódź\n".encode("utf-8")
    assert fsio.temp_files(tmp_path) == []


@pytest.mark.skipif(os.name == "nt", reason="POSIX file modes")
def test_atomic_write_keeps_the_file_mode(tmp_path):
    target = tmp_path / "f.yaml"
    fsio.atomic_write(target, b"one\n")
    assert target.stat().st_mode & 0o777 == fsio._NEW_FILE_MODE  # not the 0600 of mkstemp
    target.chmod(0o640)
    fsio.atomic_write(target, b"two\n")
    assert target.stat().st_mode & 0o777 == 0o640


@pytest.mark.parametrize("patched", ["replace", "fsync"])
def test_failure_before_replace_keeps_old_bytes(game, monkeypatch, patched):
    assert accept(game, proposals(game)).ok
    before = tables_file(game).read_bytes()
    monkeypatch.setattr(fsio.os, patched, fail_with(OSError(errno.ENOSPC, "brak miejsca (symulacja)")))
    props = proposals(game)
    props[0]["record"]["title"] = "CRT"
    with pytest.raises(kb.KBWriteError) as exc:
        accept(game, props)
    assert "poprzednią zawartość" in str(exc.value) and "Niczego nie zapisano" in str(exc.value)
    monkeypatch.undo()
    assert tables_file(game).read_bytes() == before
    assert fsio.temp_files(game / "kb") == []


def test_failure_of_a_new_file_leaves_no_file(game, monkeypatch):
    monkeypatch.setattr(fsio.os, "replace", fail_with(OSError(errno.EIO, "błąd I/O (symulacja)")))
    with pytest.raises(kb.KBWriteError):
        accept(game, proposals(game))
    monkeypatch.undo()
    assert not tables_file(game).exists() and fsio.temp_files(game / "kb") == []


def test_failure_on_second_file_rolls_back_the_whole_batch(game, monkeypatch):
    """M-STAB2 guarantee (ADR-0031; in M-STAB1 this test documented the gap): the second file of a batch fails after
    the first was replaced, and `kb/` is back to the old content in full, with no journal left behind."""
    assert accept(game, proposals(game)).ok
    moved = game / "kb" / "logic" / "combat.yaml"
    tables_file(game).rename(moved)
    before = moved.read_bytes()
    props = proposals(game) + proposals(game, "TAB-new")  # TAB-4.3 stays in combat.yaml, TAB-new → tables.yaml
    props[0]["record"]["title"] = "CRT"
    real, targets = os.replace, []

    def second_target_fails(src, dst):
        if Path(dst).parent == moved.parent:  # files of kb/logic, not the journal manifest
            targets.append(dst)
            if len(targets) == 2:
                raise OSError(errno.EIO, "błąd I/O (symulacja)")
        real(src, dst)

    monkeypatch.setattr(fsio.os, "replace", second_target_fails)
    with pytest.raises(kb.KBWriteError) as exc:
        accept(game, props)
    monkeypatch.undo()
    assert "Partia wycofana, kb/ bez zmian" in str(exc.value) and len(targets) >= 2
    assert moved.read_bytes() == before and not tables_file(game).exists()
    assert not (game / kb.BATCH_DIR).exists() and fsio.temp_files(game / "kb") == []
    assert validate([game / "source", game / "kb"]).ok


@pytest.mark.skipif(os.name != "nt", reason="retries on PermissionError only on Windows")
def test_replace_retries_while_target_is_held(game, monkeypatch):
    assert accept(game, proposals(game)).ok
    monkeypatch.setattr(fsio, "REPLACE_RETRIES", (0, 0, 0))
    real, calls = os.replace, []

    def held_twice(src, dst):
        calls.append(dst)
        if len(calls) <= 2:
            raise PermissionError(errno.EACCES, "plik otwarty przez inny proces (symulacja)")
        real(src, dst)

    monkeypatch.setattr(fsio.os, "replace", held_twice)
    props = proposals(game)
    props[0]["record"]["title"] = "CRT"
    assert accept(game, props).ok and len(calls) == 3
    monkeypatch.undo()
    assert load_documents(tables_file(game))[0]["records"][0]["title"] == "CRT"

    before = tables_file(game).read_bytes()
    monkeypatch.setattr(fsio, "REPLACE_RETRIES", (0, 0))
    monkeypatch.setattr(fsio.os, "replace", fail_with(PermissionError(errno.EACCES, "zajęty (symulacja)")))
    props[0]["record"]["title"] = "CRT 2"
    with pytest.raises(kb.KBWriteError):
        accept(game, props)
    monkeypatch.undo()
    assert tables_file(game).read_bytes() == before and fsio.temp_files(game / "kb") == []


def test_orphan_temp_file_is_removed_by_the_next_write(game):
    orphan = game / "kb" / "logic" / f".tables.yaml.x1{fsio.TMP_SUFFIX}"
    orphan.parent.mkdir(parents=True)
    orphan.write_bytes(b"schema: wgc/logic@0\nrecords: [")  # half-written file of a killed process
    assert accept(game, proposals(game)).ok  # not read as KB: the suffix is not .yaml
    assert not orphan.exists() and table_ids(game) == ["TAB-4.3"]


def test_rebuild_is_idempotent_and_writes_nothing(game, monkeypatch):
    assert accept(game, proposals(game), job="job_000001").ok
    before = tables_file(game).read_bytes()
    written: list[Path] = []
    monkeypatch.setattr(kb, "_write_file", lambda path, text: written.append(path))
    res = accept(game, proposals(game), job="job_000002")
    assert res.ok and res.unchanged == ["TAB-4.3"] and res.files == [] and written == []
    assert tables_file(game).read_bytes() == before


# --- F02: one writer per project --------------------------------------------------------------------------------

def test_lock_is_exclusive_between_threads_and_times_out(game):
    held, release = threading.Event(), threading.Event()

    def holder():
        with kb.lock(game):
            held.set()
            release.wait(10)

    t = threading.Thread(target=holder)
    t.start()
    assert held.wait(10)
    start = time.monotonic()
    with pytest.raises(kb.KBBusy) as exc:
        with kb.lock(game, timeout=0.2):
            pass
    assert time.monotonic() - start < 5 and ".glu/kb.lock" in str(exc.value)
    release.set()
    t.join(10)
    with kb.lock(game, timeout=0):  # free again
        pass
    assert lock_file(game).exists()  # the lock file stays; the OS lock is what counts


def test_two_threads_do_not_lose_records(game, monkeypatch):
    """P15 of the review: both accepts start from the same empty KB; the writes are slow."""
    real = kb._write_file

    def slow(path, text):
        time.sleep(0.2)
        real(path, text)

    monkeypatch.setattr(kb, "_write_file", slow)
    barrier = threading.Barrier(2)
    results: dict[str, kb.AcceptResult] = {}

    def run(rid):
        ws = Workspace(game)
        props = proposals(game, rid, ws)
        barrier.wait(10)
        results[rid] = accept(game, props, ws=ws)

    threads = [threading.Thread(target=run, args=(rid,)) for rid in ("TAB-a", "TAB-b")]
    for t in threads:
        t.start()
    for t in threads:
        t.join(30)
    assert all(r.ok for r in results.values()) and len(results) == 2
    assert table_ids(game) == ["TAB-a", "TAB-b"]
    assert validate([game / "source", game / "kb"]).ok


CHILD = """\
import sys
import time
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from wgc import kb, tasks
from wgc.kb import Workspace

root, rid, marker, timeout = Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), float(sys.argv[5])
real_write = kb._write_file


def slow_write(path, text):  # a long write keeps the other process waiting on the lock
    time.sleep(0.3)
    real_write(path, text)


kb._write_file = slow_write
spec = tasks.get("wgc.tables.parse")
ws = Workspace(root)
props = spec.deterministic_impl(ws, ("SEG-dsk.4.3",))
props[0]["record"]["id"] = rid
marker.write_text("ready", encoding="utf-8")
try:
    res = kb.accept(root, spec, ("SEG-dsk.4.3",), props, ws=ws, lock_timeout=timeout,
                    by={"tier": "deterministic", "tool": "wgc.tables.parse@0"})
except kb.KBBusy as e:
    print(e)
    sys.exit(3)
print(res.issues)
sys.exit(0 if res.ok else 1)
"""


def spawn(tmp_path: Path, game: Path, rid: str, timeout: float) -> tuple[subprocess.Popen, Path]:
    script = tmp_path / "child.py"
    script.write_text(CHILD, encoding="utf-8")
    marker = tmp_path / f"ready-{rid}"
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.Popen([sys.executable, str(script), str(ROOT), str(game), rid, str(marker), str(timeout)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, encoding="utf-8")
    return proc, marker


def wait_for(paths: list[Path], procs: list[subprocess.Popen], limit: float = 60) -> None:
    deadline = time.monotonic() + limit
    while not all(p.exists() for p in paths):
        assert all(p.poll() is None for p in procs), [p.communicate() for p in procs]
        assert time.monotonic() < deadline, "child processes did not start"
        time.sleep(0.05)


def test_two_processes_do_not_lose_records(game, tmp_path):
    """Two processes compute proposals from the same empty KB while this process holds the lock, then race for it."""
    with kb.lock(game):
        spawned = [spawn(tmp_path, game, rid, 60) for rid in ("TAB-a", "TAB-b")]
        procs = [p for p, _ in spawned]
        wait_for([m for _, m in spawned], procs)
        assert all(p.poll() is None for p in procs)  # both wait for the lock
    outs = [p.communicate(timeout=60) for p in procs]
    assert [p.returncode for p in procs] == [0, 0], outs
    assert table_ids(game) == ["TAB-a", "TAB-b"]
    assert validate([game / "source", game / "kb"]).ok


def test_busy_lock_in_another_process_gives_kbbusy(game, tmp_path):
    with kb.lock(game):
        proc, marker = spawn(tmp_path, game, "TAB-a", 0.5)
        out, err = proc.communicate(timeout=60)
    assert proc.returncode == 3, (out, err)
    assert "kb/ jest zajęte" in out and not (game / "kb").exists()


def test_old_workspace_reads_current_kb(game):
    """A workspace built before another accept must not hide (and then overwrite) the newer KB."""
    old = Workspace(game)
    assert accept(game, proposals(game, "TAB-a")).ok
    assert accept(game, proposals(game, "TAB-b", old), ws=old).ok
    assert table_ids(game) == ["TAB-a", "TAB-b"]


def test_result_from_a_changed_inventory_is_not_written(game):
    """The same producer replaces its records, so a job computed before `wgc source extract` must not overwrite the
    result computed after it."""
    old = Workspace(game)
    old_props = proposals(game, ws=old)
    rulebook = game / "rulebook.md"
    rulebook.write_text(rulebook.read_text(encoding="utf-8").replace("| 4 or less | No effect |",
                                                                     "| 4 or less | No result |"),
                        encoding="utf-8", newline="\n")
    source.extract(game)
    assert accept(game, proposals(game)).ok
    after = tables_file(game).read_bytes()
    assert b"No result" in after
    with pytest.raises(kb.KBStale) as exc:
        accept(game, old_props, ws=old)
    assert "ponów build" in str(exc.value)
    assert tables_file(game).read_bytes() == after


# --- F08: wrong types give diagnostics ----------------------------------------------------------------------------

def _set_record(field, value):
    return lambda p: p["record"].__setitem__(field, value)


def _set(field, value):
    return lambda p: p.__setitem__(field, value)


WRONG = {
    "id=[]": _set_record("id", []),
    "id=7": _set_record("id", 7),
    "kind=[]": _set_record("kind", []),
    "quote=123": _set("anchors", [{"seg": SEG, "quote": 123}]),
    "seg=5": _set("anchors", [{"seg": 5}]),
    "span='x'": _set("anchors", [{"seg": SEG, "span": "x"}]),
    "span=[1]": _set("anchors", [{"seg": SEG, "span": [1]}]),
    "span=[5,2]": _set("anchors", [{"seg": SEG, "span": [5, 2]}]),
    "span=[-1,3]": _set("anchors", [{"seg": SEG, "span": [-1, 3]}]),
    "span=[true,2]": _set("anchors", [{"seg": SEG, "span": [True, 2]}]),
    "span=[0,1.5]": _set("anchors", [{"seg": SEG, "span": [0, 1.5]}]),
    "anchors={}": _set("anchors", {}),
    "anchors=None": _set("anchors", None),
    "derived_from='R-1'": _set("derived_from", "R-1"),
    "derived_from=[1]": _set("derived_from", [1]),
    "columns=5": _set_record("columns", 5),  # crashed the task's own `validate` before (len(int))
    "rows=[1]": _set_record("rows", [1]),
}


@pytest.mark.parametrize("case", list(WRONG))
def test_wrong_types_give_diagnostics_and_write_nothing(game, case):
    props = proposals(game)
    WRONG[case](props[0])
    res = accept(game, props)
    assert not res.ok and not res.schema_valid and res.issues, res
    assert all(isinstance(r, str) for r in res.records)
    assert not (game / "kb").exists()
    assert not lock_file(game).exists()  # rejected before the lock: never waits for another writer


def test_wrong_ids_are_not_reported_as_records(game):
    props = proposals(game)
    props[0]["record"]["id"] = []
    res = accept(game, props)
    assert res.records == [] and "record.id" in res.issues[0] and "[]" in res.issues[0]


def test_output_that_is_not_a_list(game):
    res = accept(game, {"record": {}})
    assert not res.ok and not res.schema_valid and "listą propozycji" in res.issues[0]


def test_span_beyond_the_segment_is_a_domain_issue(game):
    props = proposals(game)
    props[0]["anchors"] = [{"seg": SEG, "span": [0, 100_000]}]
    res = accept(game, props)
    assert not res.ok and res.schema_valid and not res.domain_valid and "wykracza" in res.issues[0]
    assert not (game / "kb").exists()


def test_valid_span_and_quote_are_kept(game):
    props = proposals(game)
    props[0]["anchors"] = [{"seg": SEG, "span": [0, 5], "quote": "Combat Results Table"}]
    assert accept(game, props).ok
    [anchor] = load_documents(tables_file(game))[0]["records"][0]["prov"]["anchors"]
    assert anchor["span"] == [0, 5] and anchor["quote"] == "Combat Results Table"


def test_program_error_in_task_validate_propagates(game):
    """A bug is not a rejected output: `accept()` raises it, writes nothing and releases the lock."""
    def broken(ws, inputs, props):
        raise RuntimeError("bug in validate")

    spec = dataclasses.replace(SPEC, validate=broken)
    with pytest.raises(RuntimeError, match="bug in validate"):
        kb.accept(game, spec, INPUTS, proposals(game), by=BY)
    assert not (game / "kb").exists()
    with kb.lock(game, timeout=0):
        pass
