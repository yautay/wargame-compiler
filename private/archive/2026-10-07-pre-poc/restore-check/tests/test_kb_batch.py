"""M-STAB2: commit of a multi-file acceptance, recovery and receipts (wgc.fsbatch, wgc.kb, ADR-0031).

A multi-file acceptance: TAB-4.3 already lies in `kb/logic/combat.yaml` (not the default `tables.yaml`), the job
changes it and adds TAB-new, which goes to `tables.yaml`. Crashes are real: a child process ends with `os._exit` at a
checkpoint of the protocol (no `finally`, no cleanup), then this process runs recovery.
"""
from __future__ import annotations

import errno
import os
import subprocess
import sys
from pathlib import Path

import pytest

from test_kb_safety import ROOT, accept, proposals, tables_file
from test_tables import game  # noqa: F401  (fixture)
from wgc import fsbatch, fsio, kb
from wgc.__main__ import main as wgc_main
from wgc.validate import load_documents, validate

JOB = "job_000009"


def combat_file(root: Path) -> Path:
    return root / "kb" / "logic" / "combat.yaml"


def two_file_proposals(root: Path) -> list[dict]:
    """KB with TAB-4.3 in combat.yaml; proposals that change it and add TAB-new (two files of kb/)."""
    assert accept(root, proposals(root)).ok
    tables_file(root).rename(combat_file(root))
    props = proposals(root) + proposals(root, "TAB-new")
    props[0]["record"]["title"] = "CRT"
    return props


def kb_tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted((root / "kb").rglob("*")) if p.is_file()}


def tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def is_old(root: Path) -> bool:
    return (load_documents(combat_file(root))[0]["records"][0]["title"] != "CRT"
            and not tables_file(root).exists())


def is_new(root: Path) -> bool:
    return (load_documents(combat_file(root))[0]["records"][0]["title"] == "CRT"
            and [r["id"] for r in load_documents(tables_file(root))[0]["records"]] == ["TAB-new"])


def codes(root: Path) -> list[str]:
    return [d.code for d in validate([root / "source", root / "kb"]).errors]


# --- commit ----------------------------------------------------------------------------------------------------

def test_two_files_are_committed_together_with_a_receipt(game):
    props = two_file_proposals(game)
    res = accept(game, props, job=JOB)
    assert res.ok and set(res.files) >= {"kb/logic/combat.yaml", "kb/logic/tables.yaml"} and is_new(game)
    assert not (game / kb.BATCH_DIR).exists() and fsio.temp_files(game / "kb") == []
    assert validate([game / "source", game / "kb"]).ok
    assert res.receipt["generation"] == kb.generation(game)
    assert list(res.receipt["records"]) == ["TAB-4.3", "TAB-new"]
    assert kb.read_receipt(game, JOB) == res.receipt and kb.check_receipt(game, res.receipt) == []


def test_receipt_of_an_unchanged_result_and_a_changed_kb(game):
    first = accept(game, proposals(game), job="job_000001")
    again = accept(game, proposals(game), job="job_000002")
    assert again.unchanged == ["TAB-4.3"] and again.files == [] and again.receipt == first.receipt
    text = tables_file(game).read_text(encoding="utf-8").replace("Combat Results Table", "Combat Table")
    tables_file(game).write_text(text, encoding="utf-8", newline="\n")
    assert kb.check_receipt(game, again.receipt) == ["TAB-4.3: inna treść w kb/"]
    kb.discard_receipt(game, "job_000002")
    assert kb.read_receipt(game, "job_000002") is None and kb.receipt_jobs(game) == ["job_000001"]


def test_rejected_output_writes_no_receipt(game):
    props = proposals(game)
    props[0]["record"]["columns"] = 5
    assert not accept(game, props, job=JOB).ok and kb.read_receipt(game, JOB) is None


def test_rollback_that_fails_too_is_left_for_recovery(game, monkeypatch):
    """The second file fails, and so does restoring the first: the outcome is unresolved, the journal stays with the
    recorded intent to roll back, and recovery rolls back."""
    props = two_file_proposals(game)
    before = kb_tree(game)
    real, done = os.replace, []

    def fail_after_first(src, dst):
        if Path(dst).parent == combat_file(game).parent:
            if done:
                raise OSError(errno.EIO, "błąd I/O (symulacja)")
            done.append(dst)
        real(src, dst)

    monkeypatch.setattr(fsio.os, "replace", fail_after_first)
    with pytest.raises(kb.KBUnresolved) as exc:
        accept(game, props)
    monkeypatch.undo()
    assert "wgc kb recover" in str(exc.value) and "wycofanie jest przesądzone" in str(exc.value)
    assert '"state": "rolling_back"' in (game / kb.BATCH_DIR / fsbatch.MANIFEST).read_text(encoding="utf-8")
    assert "kb_batch_pending" in codes(game)
    assert kb.recover(game).state == "rollback"
    assert kb_tree(game) == before and validate([game / "source", game / "kb"]).ok


# --- crash of a child process at each checkpoint -----------------------------------------------------------------

CHILD = """\
import os
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from wgc import fsbatch, kb, tasks
from wgc.kb import Workspace

root, step = Path(sys.argv[2]), sys.argv[3]
INPUTS = ("SEG-dsk.4.3",)


def crash(name):
    if name == step:
        os._exit(9)  # no finally, no cleanup: like a killed process


fsbatch._step = crash
real_manifest = fsbatch._manifest


def manifest(journal, state, *args):
    if step == "staged" and state == "prepared":
        os._exit(9)  # new content and copies written, manifest not yet
    real_manifest(journal, state, *args)


fsbatch._manifest = manifest
spec = tasks.get("wgc.tables.parse")
ws = Workspace(root)
props = spec.deterministic_impl(ws, INPUTS) + spec.deterministic_impl(ws, INPUTS)
props[0]["record"]["title"] = "CRT"
props[1]["record"]["id"] = "TAB-new"
kb.accept(root, spec, INPUTS, props, by={"tier": "deterministic", "tool": spec.name}, job=sys.argv[4], ws=ws)
sys.exit(0)
"""


def crash_child(tmp_path: Path, root: Path, step: str) -> None:
    script = tmp_path / "crash.py"
    script.write_text(CHILD, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(script), str(ROOT), str(root), step, JOB], capture_output=True,
                          encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=120)
    assert proc.returncode == 9, (proc.stdout, proc.stderr)


@pytest.mark.parametrize("step, outcome", [
    ("staged", "old"),        # preparing: kb/ untouched, journal without manifest
    ("prepared", "old"),      # manifest written, no file replaced
    ("replaced:0", "old"),    # between the two replacements: kb/ half old, half new
    ("replaced:1", "old"),    # ownership manifest is still old
    ("replaced:2", "new"),    # every file replaced, commit marker not written
    ("committed", "new"),     # marker written, journal not removed
])
def test_crash_of_a_process_then_recovery(game, tmp_path, step, outcome):
    two_file_proposals(game)
    crash_child(tmp_path, game, step)
    assert (game / kb.BATCH_DIR).exists()
    if step == "replaced:0":  # really half-way: the first file new, the second not written yet
        assert load_documents(combat_file(game))[0]["records"][0]["title"] == "CRT" and not tables_file(game).exists()
    if step != "staged":
        assert "kb_batch_pending" in codes(game)  # a partial kb/ never passes as valid

    snapshot = tree(game)
    plan = kb.recover(game, dry_run=True)
    assert plan.actions and tree(game) == snapshot  # dry run: nothing written

    rec = kb.recover(game)
    assert rec.state == {"staged": "orphan", "old": "rollback", "new": "forward"}[step if step == "staged" else outcome]
    assert (is_old if outcome == "old" else is_new)(game)
    assert not (game / kb.BATCH_DIR).exists() and fsio.temp_files(game / "kb") == []
    assert validate([game / "source", game / "kb"]).ok
    assert kb.recover(game).actions == []  # idempotent

    # the receipt was written before the files: kb/ confirms it only when the batch survived
    receipt = kb.read_receipt(game, JOB)
    assert (kb.check_receipt(game, receipt) == []) == (outcome == "new")


def test_accept_recovers_an_interrupted_batch_first(game, tmp_path):
    two_file_proposals(game)
    crash_child(tmp_path, game, "replaced:0")
    res = accept(game, proposals(game, "TAB-other"))
    assert res.ok and not (game / kb.BATCH_DIR).exists()
    assert [r["id"] for r in load_documents(tables_file(game))[0]["records"]] == ["TAB-other"]
    assert load_documents(combat_file(game))[0]["records"] == []  # rollback, then TAB-4.3 retired by this owner
    assert validate([game / "source", game / "kb"]).ok


def test_file_changed_by_hand_stops_recovery(game, tmp_path):
    two_file_proposals(game)
    crash_child(tmp_path, game, "replaced:0")
    combat_file(game).write_text(combat_file(game).read_text(encoding="utf-8") + "# ręczna zmiana\n",
                                 encoding="utf-8", newline="\n")
    before = kb_tree(game)
    with pytest.raises(kb.KBBatchConflict) as exc:
        kb.recover(game)
    assert "kb/logic/combat.yaml" in str(exc.value) and kb_tree(game) == before
    with pytest.raises(kb.KBBatchConflict):
        accept(game, proposals(game))  # never merged into a partial kb/


def test_recovery_of_a_clean_kb_changes_nothing(game):
    assert accept(game, proposals(game)).ok
    (game / kb.LOCK_FILE).unlink()  # a repo whose writer lock file was never created
    snapshot = tree(game)
    assert kb.recover(game, dry_run=True).actions == [] and tree(game) == snapshot
    assert not (game / kb.LOCK_FILE).exists()
    assert kb.recover(game).state == "clean" and tree(game) == snapshot
    assert not (game / kb.LOCK_FILE).exists()  # a clean repo gets no new file, not even the lock


def test_unreadable_manifest_is_a_conflict(game):
    journal = game / kb.BATCH_DIR
    journal.mkdir(parents=True)
    (journal / fsbatch.MANIFEST).write_text("{", encoding="utf-8")
    with pytest.raises(kb.KBBatchConflict, match="nieczytelny manifest"):
        kb.recover(game)
    assert journal.exists()


# --- CLI ---------------------------------------------------------------------------------------------------------

def test_cli_kb_recover(game, tmp_path, capsys):
    assert wgc_main(["kb", "recover", "--root", str(game)]) == 0
    assert "nic do zrobienia" in capsys.readouterr().out
    two_file_proposals(game)
    crash_child(tmp_path, game, "replaced:0")
    snapshot = tree(game)
    assert wgc_main(["kb", "recover", "--root", str(game), "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "wycofanie: kb/logic/combat.yaml" in out and "Niczego nie zapisano" in out and tree(game) == snapshot
    assert wgc_main(["validate", str(game / "source"), str(game / "kb")]) == 1
    assert "kb_batch_pending" in capsys.readouterr().out
    assert wgc_main(["kb", "recover", "--root", str(game)]) == 0
    assert "w całości stara albo w całości nowa" in capsys.readouterr().out and is_old(game)
    assert wgc_main(["validate", str(game / "source"), str(game / "kb")]) == 0


def test_cli_kb_recover_conflict_exits_2(game, tmp_path, capsys):
    two_file_proposals(game)
    crash_child(tmp_path, game, "replaced:0")
    tables_file(game).write_text("schema: wgc/logic@0\nrecords: []\n", encoding="utf-8")
    assert wgc_main(["kb", "recover", "--root", str(game)]) == 2
    assert "zmienił się poza partią" in capsys.readouterr().err
