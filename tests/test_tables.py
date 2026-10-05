"""M9a: task `wgc.tables.parse@0`, build scopes and the task registry (wgc.tables, wgc.tasks)."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from wgc import source, tables, tasks
from wgc.canonical import text_hash
from wgc.kb import KBError, Workspace

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench" / "minigame"


@pytest.fixture
def game(tmp_path) -> Path:
    """bench/minigame copied to tmp_path, with segment text in .glu/source/ (`wgc source extract`)."""
    root = tmp_path / "drill-skirmish"
    shutil.copytree(BENCH, root)
    source.extract(root)
    return root


@pytest.mark.parametrize("printed, value", [
    ("4 or less", {"min": None, "max": 4}),
    ("2 or fewer", {"min": None, "max": 2}),
    ("≤ 3", {"min": None, "max": 3}),
    ("5–6", {"min": 5, "max": 6}),
    ("5-6", {"min": 5, "max": 6}),
    ("10 to 12", {"min": 10, "max": 12}),
    ("7 or more", {"min": 7, "max": None}),
    ("9+", {"min": 9, "max": None}),
    ("3", 3),
    ("-1", -1),
    ("1.5", 1.5),
    ("No effect", "No effect"),
    ("  Routed  ", "Routed"),
    ("", None),
])
def test_cell(printed, value):
    assert tables.cell(printed) == value


def test_parse_uses_tab_rows_only():
    text = "Apply the result on the Combat Results Table:\n\nRoll\tEffect\n1–2\tNone\n3 or more\tHit"
    assert tables.parse(text) == (["Roll", "Effect"], [[{"min": 1, "max": 2}, "None"], [{"min": 3, "max": None}, "Hit"]])
    assert tables.parse("A table without cell separators\n1 2") == ([], [])


def test_table_id_by_role():
    seg = {"id": "SEG-dsk.4.3", "label": "4.3"}
    assert tables.table_id({"id": "SRC-dsk.rules", "role": "rules", "seg_prefix": "dsk"}, seg) == "TAB-4.3"
    assert tables.table_id({"id": "SRC-dsk.charts", "role": "charts"}, {"id": "SEG-dsk.charts.u2"}) == "TAB-dsk.charts:u2"


def test_parse_minigame_crt(game):
    ws = Workspace(game)
    spec = tasks.get("wgc.tables.parse")
    jobs = spec.input_selector(ws, tasks.select(ws, "all"))
    assert jobs == [("SEG-dsk.4.3",)]
    [proposal] = spec.deterministic_impl(ws, jobs[0])
    assert proposal["anchors"] == [{"seg": "SEG-dsk.4.3"}]
    assert proposal["record"] == {
        "kind": "table", "id": "TAB-4.3", "title": "Combat Results Table",
        "columns": [{"name": "Modified result", "role": "key"}, {"name": "Effect on defender", "role": "value"}],
        "rows": [[{"min": None, "max": 4}, "No effect"], [{"min": 5, "max": 6}, "Routed"],
                 [{"min": 7, "max": None}, "Eliminated"]],
        "complete": True}
    assert spec.validate(ws, jobs[0], [proposal]) == []


def test_unparsed_key_cell_makes_table_incomplete(game):
    seg = Workspace(game).segment("SEG-dsk.4.3")
    path = source.cache_dir(game, seg["doc"]) / "SEG-dsk.4.3.txt"
    path.write_text(path.read_text(encoding="utf-8").replace("5–6\t", "5 through 6\t"), encoding="utf-8", newline="\n")
    inv = source.inventory_path(game)
    text = inv.read_text(encoding="utf-8").replace(seg["text_hash"], text_hash(path.read_text(encoding="utf-8")))
    inv.write_text(text, encoding="utf-8", newline="\n")
    ws = Workspace(game)
    [proposal] = tasks.get("wgc.tables.parse").deterministic_impl(ws, ("SEG-dsk.4.3",))
    assert proposal["record"]["rows"][1][0] == "5 through 6"
    assert proposal["record"]["complete"] is False


def test_cache_without_cell_separator_is_reported(game):
    """A cache written before ADR-0024 has the same text_hash but no tabs: the task says what to do."""
    seg = Workspace(game).segment("SEG-dsk.4.3")
    path = source.cache_dir(game, seg["doc"]) / "SEG-dsk.4.3.txt"
    path.write_text(path.read_text(encoding="utf-8").replace("\t", " "), encoding="utf-8", newline="\n")
    ws = Workspace(game)
    spec = tasks.get("wgc.tables.parse")
    proposals = spec.deterministic_impl(ws, ("SEG-dsk.4.3",))
    [issue] = spec.validate(ws, ("SEG-dsk.4.3",), proposals)
    assert "tabulatorem" in issue and "wgc source extract" in issue


def test_validate_reports_ragged_rows(game):
    ws = Workspace(game)
    spec = tasks.get("wgc.tables.parse")
    [p] = spec.deterministic_impl(ws, ("SEG-dsk.4.3",))
    p["record"]["rows"][0].append("extra")
    assert spec.validate(ws, ("SEG-dsk.4.3",), [p]) == ["TAB-4.3: wiersz 1 ma 3 komórek, a tabela ma 2 kolumn."]


# --- registry and scopes -------------------------------------------------------------------------------------------

def test_registry_and_stage():
    spec = tasks.get("wgc.tables.parse")
    assert spec.name == "wgc.tables.parse@0" and spec.output_schema == "wgc/logic@0#table"
    assert tasks.for_stage("1") == tasks.for_stage("stage1") == [spec, tasks.get("wgc.terms.harvest")]
    with pytest.raises(tasks.TaskError, match="Brak zadań dla etapu"):
        tasks.for_stage("9")
    with pytest.raises(tasks.TaskError, match="Nieznane zadanie"):
        tasks.get("wgc.nothing")


def test_task_spec_optional_model_fields():
    spec = tasks.get("wgc.tables.parse")
    assert spec.prompt is None and spec.decoding_schema is None and spec.context_builder is None
    assert spec.risk_features({}) == []


def test_scopes(game):
    ws = Workspace(game)
    everything = tasks.select(ws, "all")
    assert len(everything) == 31 and everything == tasks.select(ws, None)
    assert tasks.select(ws, "chapter:4") == ["SEG-dsk.4.0", "SEG-dsk.4.1", "SEG-dsk.4.2", "SEG-dsk.4.3",
                                             "SEG-dsk.4.4", "SEG-dsk.4.5"]
    assert tasks.select(ws, "chapter:4.0") == tasks.select(ws, "chapter:4")
    assert tasks.select(ws, "segment:SEG-dsk.4.3") == ["SEG-dsk.4.3"]
    for bad in ("chapter:9", "segment:SEG-dsk.9.9", "section:4", "chapter:", "everything"):
        with pytest.raises(tasks.TaskError):
            tasks.select(ws, bad)


def test_workspace_text_checks_cache(game):
    ws = Workspace(game)
    assert ws.text("SEG-dsk.3.4") == "A Routed unit may not enter a hex adjacent to an enemy unit."
    path = source.cache_dir(game, "SRC-dsk.rules") / "SEG-dsk.3.4.txt"
    path.write_text("Changed text.", encoding="utf-8", newline="\n")
    with pytest.raises(KBError, match="text_hash"):
        Workspace(game).text("SEG-dsk.3.4")
    path.unlink()
    with pytest.raises(KBError, match="wgc source extract"):
        Workspace(game).text("SEG-dsk.3.4")
    with pytest.raises(KBError, match="inwentarz"):
        Workspace(game.parent / "missing")
