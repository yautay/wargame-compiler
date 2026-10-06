"""M-STAB3b: `glu receipt <job>`: the `kb_receipt` of one job against the current `kb/`, read only (ADR-0033).

Every case — match, differences (by hand and by a later job), no job, no receipt, an undecided acceptance, a pending
batch, no store — leaves the game repo byte for byte as it was, `.glu/` included: no recovery, no reconcile, no
migration, no lock or receipt file created or removed.
"""
from __future__ import annotations

import dataclasses
import json
import sqlite3

import pytest

from glu import receipt
from glu.__main__ import main
from glu.store import SCHEMA_VERSION, Store, StoreError, db_path
from test_glu_build import build, tree
from test_glu_reconcile import fail_store_after_first_accept
from test_manifest import kb_replace
from test_struct_hash import LINES_AFTER, LINES_BEFORE, edit_rulebook
from test_tables import game  # noqa: F401  (fixture)
from wgc import kb, source, tables, tasks


def jobs_of(root) -> dict[str, str]:
    """Task → id of its job in the last build."""
    with Store(db_path(root), create=False) as store:
        last = store.builds()[-1]
        return {j["task"]: j["id"] for j in store.jobs(last["id"])}


def run(root, job: str, capsys, *extra: str) -> tuple[int, str]:
    snapshot = tree(root)
    code = main(["receipt", job, "--root", str(root), *extra])
    assert tree(root) == snapshot  # read only, in every case
    return code, capsys.readouterr().out


def test_match(game, capsys):
    assert build(game).state == "done"
    job, last = jobs_of(game)["wgc.tables.parse"], jobs_of(game)["wgc.terms.harvest"]
    code, out = run(game, last, capsys)  # the last acceptance of the build: kb/ byte for byte as after it
    assert code == 0 and "CON-d6: zgodny" in out and "Wynik: zgodny" in out and "bajt w bajt" in out
    code, out = run(game, job, capsys, "--json")  # harvest wrote kb/ after it: other generation, same records
    rep = json.loads(out)
    assert code == 0 and rep["status"] == "match" and rep["receipt"] == "attempt" and rep["generation_equal"] is False
    assert rep["records"] == {"TAB-4.3": {"state": "same", "job": job}}


def test_match_after_unrelated_later_change(game, capsys):
    """Another record changed: generation differs, the job's records still match."""
    assert build(game).state == "done"
    kb_replace(game, "concepts.yaml", "name: d6\n", "name: D6\n")
    rep = receipt.report(game, jobs_of(game)["wgc.tables.parse"])
    assert rep["status"] == "match" and rep["generation_equal"] is False


def test_difference_made_by_hand(game, capsys):
    assert build(game).state == "done"
    job = jobs_of(game)["wgc.tables.parse"]
    kb_replace(game, "tables.yaml", "title: Combat Results Table", "title: CRT")
    code, out = run(game, job, capsys)
    assert code == 1 and "TAB-4.3: inna treść w kb/" in out and "zmiana poza accept()" in out
    assert "nie oznacza sama w sobie uszkodzenia" in out and "inna niż w receipcie" in out


def test_difference_made_by_a_later_job(game, capsys):
    """A later build correctly replaced the job's records: reported as such, not as damage."""
    assert build(game).state == "done"
    first = jobs_of(game)["wgc.terms.harvest"]
    edit_rulebook(game, LINES_BEFORE, LINES_AFTER)
    source.extract(game)
    assert build(game).state == "done"
    later = jobs_of(game)["wgc.terms.harvest"]
    code, out = run(game, first, capsys)
    assert code == 1
    assert f"CON-rally_phase: inna treść w kb/ (bieżący rekord pochodzi z {later}, późniejszy job)" in out
    assert "CON-combat_phase: brak w kb/" in out  # the owner retired this output (F11)
    rep = receipt.report(game, first)
    assert rep["records"]["CON-rally_phase"] == {"state": "changed", "job": later, "later": True}


def test_no_job(game, capsys):
    assert build(game).state == "done"
    code, out = run(game, "job_999999", capsys)
    assert code == 1 and "Brak joba job_999999" in out
    assert receipt.report(game, "job_999999") == {"job": "job_999999", "status": "no_job"}


def test_no_receipt(game, capsys, monkeypatch):
    def broken(ws, inputs):
        raise ValueError("awaria implementacji (symulacja)")

    spec = dataclasses.replace(tables.PARSE, deterministic_impl=broken)
    monkeypatch.setattr(tasks, "REGISTRY", {spec.id: spec})
    assert build(game).state == "failed"
    code, out = run(game, jobs_of(game)["wgc.tables.parse"], capsys)
    assert code == 1 and "brak receiptu" in out and "stan: failed" in out


def test_undecided_acceptance_uses_the_pending_receipt(game, capsys, monkeypatch):
    """The store failed after kb/ was written: the job waits in `validating` with its receipt (ADR-0031)."""
    fail_store_after_first_accept(monkeypatch)
    with pytest.raises(StoreError):
        build(game)
    monkeypatch.undo()
    job = kb.receipt_jobs(game)[0]
    code, out = run(game, job, capsys)
    assert code == 0 and "nierozstrzygniętej akceptacji" in out and "stan: validating" in out
    assert kb.receipt_jobs(game) == [job]  # not removed: deciding is reconcile's job


def test_pending_batch_is_reported_not_recovered(game, capsys):
    assert build(game).state == "done"
    batch = game / kb.BATCH_DIR
    batch.mkdir()
    (batch / "manifest.json").write_text("{}", encoding="utf-8")
    code, out = run(game, jobs_of(game)["wgc.tables.parse"], capsys)
    assert code == 1 and "przerwaną partię" in out and "wgc kb recover" in out
    assert (batch / "manifest.json").is_file()


def test_no_store_is_an_operational_error(game, capsys):
    snapshot = tree(game)
    assert main(["receipt", "job_000001", "--root", str(game)]) == 2
    assert "brak bazy stanu GLU" in capsys.readouterr().err
    assert tree(game) == snapshot and not db_path(game).exists()


def test_store_of_another_version_is_not_migrated(game, capsys):
    assert build(game).state == "done"
    conn = sqlite3.connect(db_path(game))
    conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION - 1}")
    conn.close()
    snapshot = tree(game)
    assert main(["receipt", jobs_of_raw(game), "--root", str(game)]) == 2
    assert "bez migracji" in capsys.readouterr().err and tree(game) == snapshot


def jobs_of_raw(root) -> str:
    """Any job id, read without the store (whose version the test has just changed)."""
    conn = sqlite3.connect(db_path(root))
    try:
        return conn.execute("SELECT id FROM job ORDER BY rowid LIMIT 1").fetchone()[0]
    finally:
        conn.close()
