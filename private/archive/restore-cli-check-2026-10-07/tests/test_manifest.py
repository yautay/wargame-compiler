"""M-STAB3b: invocation manifest, one definition of dependencies, freshness of the `kb/` context (ADR-0033).

Regressions of finding F05 of the review after M9a: a task's own projection, the full read of a harvest job and a
change of a source document's role. A task reading `kb/` records as context: a change of the context changes the job
key, a change between execution and acceptance blocks the write. The manifest lives in `kb/`, so the dependencies of
a record can be rebuilt after `.glu/` is gone.
"""
from __future__ import annotations

import dataclasses
import shutil
from pathlib import Path

import pytest

from glu import planner
from glu.store import Store, db_path
from test_glu_build import build
from test_struct_hash import LINES_AFTER, LINES_BEFORE, PHASES, TABLE, edit_rulebook, keys, record
from test_tables import game  # noqa: F401  (fixture)
from wgc import kb, manifest as manifests, source, tables, tasks, terms
from wgc.canonical import PROJECTION_VERSION, content_hash, projection
from wgc.kb import Workspace
from wgc.tasks import TaskSpec
from wgc.validate import validate

BY = {"tier": "deterministic", "tool": "test.context@0"}


def inventory_replace(root: Path, old: str, new: str) -> None:
    path = source.inventory_path(root)
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def kb_replace(root: Path, file: str, old: str, new: str) -> None:
    path = root / "kb" / "logic" / file
    text = path.read_text(encoding="utf-8")
    assert old in text, text
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def job_key(root: Path, task: str) -> dict:
    """Cache key of the last job of `task` in the store."""
    with Store(db_path(root), create=False) as store:
        jobs = [j for b in store.builds() for j in store.jobs(b["id"]) if j["task"] == task]
    return jobs[-1]["cache_key"]


# --- F05: one definition for the planner and provenance --------------------------------------------------------------

def test_own_projection_of_a_task_is_the_key_and_the_manifest(game, monkeypatch):
    """F05 P3: a task's own projection used to give `prov.inputs_hash` ≠ the job key."""
    own = dataclasses.replace(tables.PARSE, semantic_projection=lambda ws, sid: {"table_cells": [1, 2]})
    monkeypatch.setattr(tasks, "REGISTRY", {own.id: own})
    assert build(game).state == "done"
    rec = record(game, "tables.yaml", "TAB-4.3")
    m = manifests.Manifest(rec["prov"]["manifest"])
    assert m.body["inputs"] == [{"id": TABLE, "hash": content_hash({"table_cells": [1, 2]})}]
    key = job_key(game, own.id)
    assert key["input_hash"] == m.input_hash and key["context_hash"] == m.context_hash == planner.EMPTY_CONTEXT
    assert m.body == manifests.build(Workspace(game), own, (TABLE,)).body


def test_harvest_manifest_covers_every_input_of_the_job(game):
    """F05: a concept's evidence is its anchors, but the job reads every matching segment of the document."""
    assert build(game).state == "done"
    d6 = record(game, "concepts.yaml", "CON-d6")
    assert {a["seg"] for a in d6["prov"]["anchors"]} == {"SEG-dsk.4.2"}
    assert [e["id"] for e in d6["prov"]["manifest"]["inputs"]] == ["SEG-dsk.2.2", "SEG-dsk.4.2", "SEG-dsk.5.2",
                                                                    "SEG-dsk.7.0"]
    # every rules document is authority data of harvest (it picks the main rules among them)
    assert [e["id"] for e in d6["prov"]["manifest"]["authority"]] == ["SRC-dsk.rules"]

    edit_rulebook(game, LINES_BEFORE, LINES_AFTER)  # the phase list: an input of the job, no anchor of CON-d6
    source.extract(game)
    assert manifests.check(Workspace(game), d6["prov"]["manifest"]) == [f"wejście {PHASES}: zmieniony"]
    assert build(game).state == "done"
    d6b = record(game, "concepts.yaml", "CON-d6")
    assert d6b["prov"]["anchors"] == d6["prov"]["anchors"] and d6b["prov"]["inputs_hash"] == d6["prov"]["inputs_hash"]
    assert d6b["prov"]["manifest"] != d6["prov"]["manifest"]
    assert manifests.Manifest(d6b["prov"]["manifest"]).input_hash == job_key(game, terms.TASK_ID)["input_hash"]


def test_new_rules_document_changes_the_harvest_manifest_only(game):
    """The main rules are picked among all `rules` documents: one more of them is a dependency of harvest, not of
    the table parser (which reads only its input's document)."""
    before = keys(game)
    inventory_replace(game, "  - {kind: source_document, id: SRC-dsk.faq,",
                      "  - {kind: source_document, id: SRC-aaa.rules, role: rules, present: false}\n"
                      "  - {kind: source_document, id: SRC-dsk.faq,")
    after = keys(game)
    assert after["wgc.terms.harvest@0"]["input_hash"] != before["wgc.terms.harvest@0"]["input_hash"]
    assert after["wgc.tables.parse@0"] == before["wgc.tables.parse@0"]


def test_role_change_changes_job_keys_and_provenance(game):
    """F05 P11: `rules` → `errata` changes the table ID and `prov.kind`, so it must change the job key too."""
    before = keys(game)
    assert build(game).state == "done"
    tab0 = record(game, "tables.yaml", "TAB-4.3")
    inventory_replace(game, "id: SRC-dsk.rules, role: rules,", "id: SRC-dsk.rules, role: errata,")
    after = keys(game)
    for task in ("wgc.tables.parse@0", "wgc.terms.harvest@0"):
        assert after[task]["input_hash"] != before[task]["input_hash"], task
    assert build(game).state == "done"
    tab1 = record(game, "tables.yaml", "TAB-dsk:4.3")
    assert tab1["prov"]["kind"] == "errata" and tab0["prov"]["kind"] == "explicit_source"
    assert tab1["prov"]["manifest"]["inputs"] == tab0["prov"]["manifest"]["inputs"]
    assert tab1["prov"]["manifest"]["authority"] != tab0["prov"]["manifest"]["authority"]
    assert manifests.check(Workspace(game), tab0["prov"]["manifest"]) == ["dokument źródłowy SRC-dsk.rules: zmieniony"]


def test_evidence_outside_the_manifest_is_rejected(game):
    assert build(game).state == "done"
    ws = Workspace(game)
    props = tables.PARSE.deterministic_impl(ws, (TABLE,))
    props[0]["derived_from"] = ["CON-d6"]  # a kb/ record the table parser never read
    res = kb.accept(game, tables.PARSE, (TABLE,), props, by={"tier": "deterministic", "tool": "wgc.tables.parse@0"})
    assert not res.ok and any("spoza manifestu" in i for i in res.issues)


def test_manifest_has_nothing_volatile(game):
    """The scope of a build, the job and kb/ never enter the manifest: `chapter:5` after `all` leaves kb/ as it is."""
    assert build(game).state == "done"
    files = {p: p.read_bytes() for p in (game / "kb").rglob("*.yaml")}
    assert build(game, "chapter:5").state == "done"
    assert {p: p.read_bytes() for p in (game / "kb").rglob("*.yaml")} == files


# --- the manifest survives the loss of .glu/ -------------------------------------------------------------------------

def test_dependencies_are_rebuilt_from_kb_after_glu_is_gone(game):
    assert build(game).state == "done"
    shutil.rmtree(game / ".glu")
    ws = Workspace(game)
    recs = [record(game, "tables.yaml", "TAB-4.3"), record(game, "concepts.yaml", "CON-scn.the_ford")]
    for rec in recs:
        m = rec["prov"]["manifest"]
        assert m["projection"] == PROJECTION_VERSION and manifests.check(ws, m) == [], rec["id"]
    assert [e["id"] for e in recs[1]["prov"]["manifest"]["inputs"]] == ["SEG-dsk.2.2", "SEG-dsk.4.2", "SEG-dsk.5.2",
                                                                        "SEG-dsk.7.0"]
    # what changed since acceptance, still without .glu/ (checking writes nothing)
    inventory_replace(game, "id: SRC-dsk.rules, role: rules,", "id: SRC-dsk.rules, role: errata,")
    ws = Workspace(game)
    assert manifests.check(ws, recs[0]["prov"]["manifest"]) == ["dokument źródłowy SRC-dsk.rules: zmieniony"]
    assert not (game / ".glu").exists()


def test_check_reports_a_vanished_input(game):
    assert build(game).state == "done"
    m = record(game, "tables.yaml", "TAB-4.3")["prov"]["manifest"]
    path = source.inventory_path(game)
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines(keepends=True) if f"id: {TABLE}," not in ln]
    path.write_text("".join(lines), encoding="utf-8", newline="\n")
    assert manifests.check(Workspace(game), m) == [f"wejście {TABLE}: nie istnieje"]


# --- freshness of the kb/ context -----------------------------------------------------------------------------------

def _context_run(ws, inputs):
    """A table whose title comes from a kb/ record (stands for a model task reading context, M10/M14)."""
    props = tables.PARSE.deterministic_impl(ws, inputs)
    rec = props[0]["record"]
    rec.update(id="TAB-ctx", title=f"Kostka {ws.record('CON-d6')['name']}")
    props[0]["derived_from"] = ["CON-d6"]
    return props


CONTEXT_TASK = TaskSpec(id="test.context", version="0", stage="stage1", output_kind="table",
                        output_schema="wgc/logic@0#table", input_selector=tables.PARSE.input_selector,
                        validate=lambda ws, inputs, proposals: [], deterministic_impl=_context_run,
                        context_selector=lambda ws, inputs: ["CON-d6"])


@pytest.fixture
def built(game):
    """The game after one build: kb/ has `CON-d6` (harvest) and `TAB-4.3`."""
    assert build(game).state == "done"
    return game


def test_kb_context_enters_the_job_key(built):
    m0 = manifests.build(Workspace(built), CONTEXT_TASK, (TABLE,))
    assert [e["id"] for e in m0.body["context"]] == ["CON-d6"] and m0.generation == kb.generation(built)
    kb_replace(built, "concepts.yaml", "name: d6\n", "name: D6\n")
    m1 = manifests.build(Workspace(built), CONTEXT_TASK, (TABLE,))
    assert m1.context_hash != m0.context_hash and m1.input_hash == m0.input_hash
    assert planner.cache_key(CONTEXT_TASK, m1) != planner.cache_key(CONTEXT_TASK, m0)
    assert manifests.diff(m0.body, m1.body) == ["kontekst kb/ CON-d6: zmieniony"]


def _execute(root: Path):
    """What the executor does before `accept()`: one pinned snapshot for the manifest and the implementation."""
    jws = Workspace(root).pinned(kb.snapshot(root))
    m = manifests.build(jws, CONTEXT_TASK, (TABLE,))
    return jws, m, CONTEXT_TASK.deterministic_impl(jws, (TABLE,))


def test_context_change_before_accept_blocks_the_write(built):
    jws, m, props = _execute(built)
    assert props[0]["record"]["title"] == "Kostka d6"
    kb_replace(built, "concepts.yaml", "name: d6\n", "name: D6\n")  # another writer between execution and acceptance
    tables_before = (built / "kb" / "logic" / "tables.yaml").read_bytes()
    with pytest.raises(kb.KBContextStale, match="CON-d6: zmieniony"):
        kb.accept(built, CONTEXT_TASK, (TABLE,), props, by=BY, job="job_ctx", ws=jws, manifest=m)
    assert (built / "kb" / "logic" / "tables.yaml").read_bytes() == tables_before
    assert kb.read_receipt(built, "job_ctx") is None  # refused before the receipt


def test_unchanged_context_is_accepted_with_its_manifest(built):
    jws, m, props = _execute(built)
    res = kb.accept(built, CONTEXT_TASK, (TABLE,), props, by=BY, job="job_ctx", ws=jws, manifest=m)
    assert res.ok and res.created == ["TAB-ctx"]
    rec = record(built, "tables.yaml", "TAB-ctx")
    assert rec["prov"]["manifest"] == m.body and rec["prov"]["derived_from"] == ["CON-d6"]
    assert "generation" not in str(rec["prov"]["manifest"])
    assert validate([built / "source", built / "kb"]).ok


def test_unrelated_kb_change_does_not_block(built):
    """Another file of kb/ changed (e.g. a parallel build): new generation, same context → accepted."""
    jws, m, props = _execute(built)
    kb_replace(built, "tables.yaml", "title: Combat Results Table", "title: Combat Results Table (CRT)")
    assert kb.generation(built) != m.generation
    res = kb.accept(built, CONTEXT_TASK, (TABLE,), props, by=BY, job="job_ctx", ws=jws, manifest=m)
    assert res.ok and res.created == ["TAB-ctx"]


def test_context_changed_and_restored_is_accepted(built):
    """The generation is a content hash: the same bytes again are the same context (no ABA error)."""
    jws, m, props = _execute(built)
    kb_replace(built, "concepts.yaml", "name: d6\n", "name: D6\n")
    kb_replace(built, "concepts.yaml", "name: D6\n", "name: d6\n")
    res = kb.accept(built, CONTEXT_TASK, (TABLE,), props, by=BY, job="job_ctx", ws=jws, manifest=m)
    assert res.ok


def test_task_reading_kb_needs_the_manifest_of_its_execution(built):
    jws, _m, props = _execute(built)
    with pytest.raises(kb.KBError, match="wymaga manifestu"):
        kb.accept(built, CONTEXT_TASK, (TABLE,), props, by=BY, ws=jws)


def test_implementation_reads_the_snapshot_of_its_manifest(built):
    jws, m, _props = _execute(built)
    kb_replace(built, "concepts.yaml", "name: d6\n", "name: D6\n")
    assert jws.record("CON-d6")["name"] == "d6"  # pinned: not the file changed meanwhile
    assert Workspace(built).record("CON-d6")["name"] == "D6"


def test_executor_refuses_a_result_from_an_old_context(built, monkeypatch):
    """Through GLU: the context changes while the job runs → Attempt `error`, job failed, kb/ without the result."""
    def run_and_change(ws, inputs):
        props = _context_run(ws, inputs)
        kb_replace(built, "concepts.yaml", "name: d6\n", "name: D6\n")
        return props

    task = dataclasses.replace(CONTEXT_TASK, deterministic_impl=run_and_change)
    monkeypatch.setattr(tasks, "REGISTRY", {task.id: task})
    result = build(built)
    assert result.state == "failed"
    [job] = result.jobs
    assert job.state == "failed" and "CON-d6: zmieniony" in job.issues[0]
    with Store(db_path(built), create=False) as store:
        [attempt] = store.attempts(job.id)
        reasons = [t.get("reason") for t in store.history(job.id)]
    assert attempt["outcome"] == "error" and attempt["error_class"] == "runtime"
    assert "kontekst kb/ zmienił się między wykonaniem a akceptacją" in reasons
    assert "TAB-ctx" not in (built / "kb" / "logic" / "tables.yaml").read_text(encoding="utf-8")
    assert kb.read_receipt(built, job.id) is None


def test_executor_fails_a_job_whose_context_changed_since_planning(game, monkeypatch):
    """An earlier job of the same build writes the context (harvest creates CON-d6): the planned key is not the
    executed one, so the job fails before running; ordering jobs is M13."""
    task = dataclasses.replace(CONTEXT_TASK, context_selector=lambda ws, inputs: [
        r["id"] for _, d in ws.kb_documents() for r in (d.get("records") or []) if r.get("id") == "CON-d6"])
    monkeypatch.setattr(tasks, "REGISTRY", {terms.HARVEST.id: terms.HARVEST, task.id: task})
    result = build(game)
    by_task = {j.task: j for j in result.jobs}
    assert by_task["wgc.terms.harvest"].state == "done"
    assert by_task["test.context"].state == "failed"
    assert "wejścia joba zmieniły się od planu" in by_task["test.context"].issues[0]
    assert "kontekst kb/ CON-d6: nowy" in by_task["test.context"].issues[0]
    # the next build plans with the context present and succeeds
    assert build(game).state == "done"
    assert record(game, "tables.yaml", "TAB-ctx")["prov"]["manifest"]["context"][0]["id"] == "CON-d6"
