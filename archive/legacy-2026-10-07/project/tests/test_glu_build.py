"""M9a: planner, Tier 0 executor and `glu build` on bench/minigame (glu.planner, glu.exec, ADR-0025)."""
from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from glu import exec as executor, planner, states
from glu.__main__ import main
from glu.store import Store, db_path
from test_glu_store import Clock, Ids
from test_tables import game  # noqa: F401  (fixture)
from wgc import contracts, fsio, kb, manifest as manifests, source, tables, tasks, terms
from wgc.kb import Workspace
from wgc.validate import load_documents, validate

# wgc.terms.harvest@0 on bench/minigame: one job over the segments with a match, six concepts (M9b)
HARVEST_INPUTS = ("SEG-dsk.2.2", "SEG-dsk.4.2", "SEG-dsk.5.2", "SEG-dsk.7.0")
CONCEPTS = ["CON-rally_phase", "CON-movement_phase", "CON-combat_phase", "CON-end_phase", "CON-d6", "CON-scn.the_ford"]
TIER0_PATH = ["pending", "ready", "running", "proposed", "validating", "accepted", "done"]


_IDS: dict[Path, Ids] = {}  # one ID sequence per game root, shared by the builds of a test


def build(root: Path, scope: str = "all", plan: planner.Plan | None = None) -> executor.BuildResult:
    ws = Workspace(root)
    plan = plan or planner.plan(ws, "1", scope)
    with Store(db_path(root), clock=Clock(), new_id=_IDS.setdefault(root, Ids())) as store:
        return executor.run(store, ws, plan, "drill-skirmish")


def tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def path_of(history: list[dict]) -> list[str]:
    return [h["dst"] for h in history]


def test_plan(game):
    plan = planner.plan(Workspace(game), "1")
    assert plan.stage == "stage1" and plan.scope == "all" and plan.skipped == []
    job, harvest = plan.jobs
    assert job.spec is tables.PARSE and job.inputs == ("SEG-dsk.4.3",) and job.tier == "deterministic"
    assert harvest.spec is terms.HARVEST and harvest.inputs == HARVEST_INPUTS
    assert job.cache_key == {"task": "wgc.tables.parse", "task_version": "0", "output_schema": "wgc/logic@0#table",
                             "input_hash": manifests.build(Workspace(game), tables.PARSE, job.inputs).input_hash,
                             "context_hash": planner.EMPTY_CONTEXT}
    assert job.manifest == manifests.build(Workspace(game), tables.PARSE, job.inputs)
    assert planner.plan(Workspace(game), "stage1", "chapter:3").jobs == []


def test_plan_skips_tasks_without_tier0(game, monkeypatch):
    model_only = dataclasses.replace(tables.PARSE, id="logic.model.only", deterministic_impl=None)
    monkeypatch.setattr(tasks, "REGISTRY", {"wgc.tables.parse": tables.PARSE, "logic.model.only": model_only})
    plan = planner.plan(Workspace(game), "1")
    assert len(plan.jobs) == 1 and plan.skipped == ["logic.model.only@0"]


def test_tier0_build_gives_valid_records(game):
    res = build(game)
    assert res.state == "done" and [j.state for j in res.jobs] == ["done", "done"]
    assert res.jobs[0].records == ["TAB-4.3"] and res.jobs[1].records == CONCEPTS
    assert res.metrics == {"jobs_total": 2, "jobs_deterministic": 2, "jobs_done": 2, "jobs_failed": 0,
                           "records_created": 7, "records_updated": 0, "records_unchanged": 0}
    report = validate([game / "source", game / "kb"])
    assert report.ok and not report.warnings and report.records == 40  # 33 Stage 0 records + TAB-4.3 + 6 concepts
    [rec] = load_documents(game / "kb" / "logic" / "tables.yaml")[0]["records"]
    assert rec["prov"]["job"] == res.jobs[0].id and rec["prov"]["by"] == {"tier": "deterministic",
                                                                          "tool": "wgc.tables.parse@0"}


def test_rebuild_without_changes_keeps_kb(game):
    build(game)
    before = tree(game / "kb")
    res = build(game)
    assert res.state == "done" and res.metrics["records_unchanged"] == 7 and res.metrics["records_created"] == 0
    assert res.metrics["records_updated"] == 0 and tree(game / "kb") == before


def test_jobs_follow_legal_path_and_export_is_valid(game):
    res = build(game)
    with Store(db_path(game), create=False) as store:
        history = store.history(res.jobs[0].id)
        assert path_of(history) == TIER0_PATH
        for src, dst in zip(TIER0_PATH, TIER0_PATH[1:]):
            assert dst in states.allowed("job", src)
        assert path_of(store.history(res.id)) == ["planning", "running", "done"]
        [attempt] = store.attempts(res.jobs[0].id)
        assert (attempt["tier"], attempt["outcome"], attempt["schema_valid"], attempt["domain_valid"]) == \
            ("deterministic", "accepted", True, True)
        job = store.job(res.jobs[0].id)
        assert job["accepted_records"] == ["TAB-4.3"] and job["cache_hit"] is False and job["tier"] == "deterministic"
        doc = store.export(res.id)
    assert contracts.errors(doc) == []
    assert [r["kind"] for r in doc["records"]] == ["build", "job", "job", "attempt", "attempt"]
    assert doc["records"][0]["target"] == {"stage": "stage1", "scope": "all"}


def test_rejected_output_fails_job_and_build(game):
    build(game)
    path = game / "kb" / "logic" / "tables.yaml"
    path.write_text(path.read_text(encoding="utf-8").replace("Combat Results Table", "CRT")
                    .replace("tool: wgc.tables.parse@0", "tool: wgc.other@0"), encoding="utf-8", newline="\n")
    before = tree(game / "kb")
    res = build(game)
    assert res.state == "failed" and res.metrics["jobs_failed"] == 1 and "konflikt" in res.jobs[0].issues[0]
    assert tree(game / "kb") == before
    with Store(db_path(game), create=False) as store:
        assert path_of(store.history(res.jobs[0].id)) == TIER0_PATH[:5] + ["failed"]
        assert path_of(store.history(res.id)) == ["planning", "running", "failed"]
        [attempt] = store.attempts(res.jobs[0].id)
        assert attempt["outcome"] == "rejected" and attempt["domain_valid"] is False
        assert "konflikt" in attempt["validation_errors"][0]


def test_implementation_error_fails_job(game):
    def boom(ws, inputs):
        raise RuntimeError("parser crashed")

    plan = planner.plan(Workspace(game), "1")
    broken = dataclasses.replace(plan, jobs=[dataclasses.replace(plan.jobs[0],
                                                                 spec=dataclasses.replace(tables.PARSE, deterministic_impl=boom))])
    res = build(game, plan=broken)
    assert res.state == "failed" and res.jobs[0].issues == ["RuntimeError: parser crashed"]
    with Store(db_path(game), create=False) as store:
        assert path_of(store.history(res.jobs[0].id)) == ["pending", "ready", "running", "failed"]
        [attempt] = store.attempts(res.jobs[0].id)
        assert attempt["outcome"] == "error" and attempt["error_class"] == "runtime"
    assert not (game / "kb").exists()


def test_program_error_in_acceptance_is_an_error_not_a_rejection(game):
    """M-STAB1 (F08): a bug in the task's `validate` fails the job with Attempt `error`, never `rejected`, and no
    job stays `validating`."""
    def broken(ws, inputs, proposals):
        raise RuntimeError("bug in validate")

    plan = planner.plan(Workspace(game), "1")
    spec = dataclasses.replace(tables.PARSE, validate=broken)
    res = build(game, plan=dataclasses.replace(plan, jobs=[dataclasses.replace(plan.jobs[0], spec=spec)]))
    assert res.state == "failed" and res.jobs[0].issues[0].startswith("błąd programu: RuntimeError: bug in validate")
    with Store(db_path(game), create=False) as store:
        history = store.history(res.jobs[0].id)
        assert path_of(history) == TIER0_PATH[:5] + ["failed"] and history[-1]["reason"] == "błąd programu w akceptacji"
        [attempt] = store.attempts(res.jobs[0].id)
        assert attempt["outcome"] == "error" and attempt["error_class"] == "runtime"
    assert not (game / "kb").exists()


@pytest.mark.parametrize("fault, reason", [("write", "awaria zapisu kb/"), ("busy", "kb/ zajęte przez innego pisarza")])
def test_operational_acceptance_failure_is_an_error(game, monkeypatch, fault, reason):
    """M-STAB1 (F01, F02): a failed write or a busy KB lock is Attempt `error` with its own reason; kb/ is untouched."""
    if fault == "write":
        def boom(*args):
            raise OSError(28, "brak miejsca (symulacja)")
        monkeypatch.setattr(fsio.os, "replace", boom)
        res = build(game)
    else:
        monkeypatch.setattr(kb, "LOCK_TIMEOUT", 0.2)
        with kb.lock(game):
            res = build(game)
    monkeypatch.undo()
    assert res.state == "failed"
    with Store(db_path(game), create=False) as store:
        assert store.history(res.jobs[0].id)[-1]["reason"] == reason
        [attempt] = store.attempts(res.jobs[0].id)
        assert attempt["outcome"] == "error" and attempt["error_class"] == "runtime"
    assert not (game / "kb" / "logic" / "tables.yaml").exists() and fsio.temp_files(game) == []


def test_only_accept_writes_kb(game, monkeypatch):
    """GLU never writes KB YAML itself: with the WGC writer stubbed out, a build leaves no kb/ behind, and with a spy
    every file in kb/ is one the WGC writer wrote."""
    written: list[Path] = []
    monkeypatch.setattr(kb, "_write_batch", lambda root, changes, job: written.extend(p for p, _ in changes))
    res = build(game)
    assert res.state == "done" and {p.name for p in written} >= {"tables.yaml", "concepts.yaml"}
    assert not (game / "kb").exists()

    monkeypatch.undo()
    real = kb._write_batch
    spied: list[Path] = []

    def spy(root, changes, job):
        spied.extend(p for p, _ in changes)
        real(root, changes, job)

    monkeypatch.setattr(kb, "_write_batch", spy)
    build(game)
    assert sorted(p for p in (game / "kb").rglob("*") if p.is_file()) == sorted(spied)


# --- CLI ---------------------------------------------------------------------------------------------------------

def test_cli_dry_run_writes_nothing(game, capsys):
    before = tree(game)
    assert main(["build", "--root", str(game), "--stage", "1", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "wgc.tables.parse@0" in out and "SEG-dsk.4.3" in out and "Niczego nie zapisano" in out
    assert tree(game) == before and not db_path(game).exists() and not (game / "kb").exists()
    assert not (game / kb.LOCK_FILE).exists()  # the plan never takes the KB writer lock (M-STAB1)


def test_cli_build_then_status(game, capsys):
    assert main(["build", "--root", str(game), "--stage", "1", "--scope", "chapter:4"]) == 0
    out = capsys.readouterr().out
    assert "stan: done" in out and "TAB-4.3" in out and "nowe 7" in out and "projekt drill-skirmish" in out
    assert main(["status", "--root", str(game)]) == 0
    assert "stage1 chapter:4" in capsys.readouterr().out
    assert main(["build", "--root", str(game), "--stage", "1", "--project", "dsk"]) == 0
    assert "bez zmian 7" in capsys.readouterr().out


def test_cli_failed_build_exits_1(game, capsys):
    assert main(["build", "--root", str(game), "--stage", "1"]) == 0
    path = game / "kb" / "logic" / "tables.yaml"
    path.write_text(path.read_text(encoding="utf-8").replace("Combat Results Table", "CRT")
                    .replace("tool: wgc.tables.parse@0", "tool: wgc.other@0"), encoding="utf-8", newline="\n")
    assert main(["build", "--root", str(game), "--stage", "1"]) == 1
    assert "stan: failed" in capsys.readouterr().out


@pytest.mark.parametrize("args, message", [
    (["--stage", "9"], "Brak zadań dla etapu"),
    (["--stage", "1", "--scope", "chapter:9"], "brak nagłówka rozdziału"),
    (["--stage", "1", "--scope", "everything"], "Niepoprawny zakres"),
])
def test_cli_operational_errors_exit_2(game, capsys, args, message):
    assert main(["build", "--root", str(game), *args]) == 2
    assert message in capsys.readouterr().err
    assert not db_path(game).exists()


def test_cli_missing_inventory_or_text_exits_2(game, tmp_path, capsys):
    assert main(["build", "--root", str(tmp_path / "empty"), "--stage", "1"]) == 2
    assert "inwentarza" in capsys.readouterr().err
    (source.cache_dir(game, "SRC-dsk.rules") / "SEG-dsk.4.3.txt").unlink()
    assert main(["build", "--root", str(game), "--stage", "1"]) == 2
    assert "wgc source extract" in capsys.readouterr().err
    assert not db_path(game).exists()
