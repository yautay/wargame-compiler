"""M9b: task `wgc.terms.harvest@0`: concepts only for patterns with a certain category (wgc.terms, ADR-0030)."""
from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from glu import planner
from glu.__main__ import main
from glu.store import db_path
from test_glu_build import CONCEPTS, HARVEST_INPUTS, build, tree
from test_tables import game  # noqa: F401  (fixture)
from wgc import kb, source, tasks, terms
from wgc.canonical import normalize_text
from wgc.kb import Workspace
from wgc.validate import load_documents, validate

BY = {"tier": "deterministic", "tool": "wgc.terms.harvest@0"}


def harvest(ws: Workspace, scope: str = "all") -> list[dict]:
    """Proposals of every harvest job planned for the scope."""
    return [p for inputs in terms.HARVEST.input_selector(ws, tasks.select(ws, scope))
            for p in terms.HARVEST.deterministic_impl(ws, inputs)]


def concepts(root: Path) -> list[dict]:
    path = root / "kb" / "logic" / "concepts.yaml"
    return load_documents(path)[0]["records"] if path.is_file() else []


def matches(text: str, segment_type: str = "rule") -> list[tuple]:
    return terms.matches({"segment_type": segment_type}, text)


def add_document(root: Path, doc_id: str, role: str, name: str, text: str) -> None:
    """A second document of the game (Markdown file + inventory entry), segmented by `wgc source extract`."""
    (root / name).write_text(text, encoding="utf-8", newline="\n")
    inv = source.read_inventory(root)
    inv.documents.append({"kind": "source_document", "id": doc_id, "role": role, "path": name, "present": True})
    source.write_inventory(root, inv)
    source.extract(root)


# --- the benchmark -------------------------------------------------------------------------------------------------

def test_bench_proposals(game):
    ws = Workspace(game)
    assert terms.HARVEST.input_selector(ws, tasks.select(ws, "all")) == [HARVEST_INPUTS]
    assert harvest(ws) == [
        {"record": {"kind": "concept", "id": "CON-rally_phase", "category": "phase", "name": "Rally Phase",
                    "source_terms": ["Rally Phase"]}, "anchors": [{"seg": "SEG-dsk.2.2", "quote": "Rally Phase"}]},
        {"record": {"kind": "concept", "id": "CON-movement_phase", "category": "phase", "name": "Movement Phase",
                    "source_terms": ["Movement Phase"]}, "anchors": [{"seg": "SEG-dsk.2.2", "quote": "Movement Phase"}]},
        {"record": {"kind": "concept", "id": "CON-combat_phase", "category": "phase", "name": "Combat Phase",
                    "source_terms": ["Combat Phase"]}, "anchors": [{"seg": "SEG-dsk.2.2", "quote": "Combat Phase"}]},
        {"record": {"kind": "concept", "id": "CON-end_phase", "category": "phase", "name": "End Phase",
                    "source_terms": ["End Phase"]}, "anchors": [{"seg": "SEG-dsk.2.2", "quote": "End Phase"}]},
        {"record": {"kind": "concept", "id": "CON-d6", "category": "die", "name": "d6", "source_terms": ["1d6"]},
         "anchors": [{"seg": "SEG-dsk.4.2", "quote": "1d6"}]},
        {"record": {"kind": "concept", "id": "CON-scn.the_ford", "category": "scenario", "name": "The Ford",
                    "source_terms": ["The Ford"]}, "anchors": [{"seg": "SEG-dsk.7.0", "quote": "Scenario: The Ford"}]},
    ]


def test_quotes_are_verbatim(game):
    ws = Workspace(game)
    for p in harvest(ws):
        for a in p["anchors"]:
            assert a["quote"] in ws.text(a["seg"]).replace("\n", " ")
            assert normalize_text(a["quote"]) in normalize_text(ws.text(a["seg"]))


def test_build_gives_valid_concepts_without_guessed_categories(game):
    res = build(game)
    assert res.state == "done" and res.jobs[1].records == CONCEPTS
    assert validate([game / "source", game / "kb"]).ok
    recs = concepts(game)
    assert sorted(r["id"] for r in recs) == sorted(CONCEPTS)
    assert {r["category"] for r in recs} <= set(terms.CATEGORIES)
    for r in recs:
        assert r["status"] == "accepted" and r["prov"]["kind"] == "explicit_source" and r["prov"]["by"] == BY
        assert all("quote" in a and a["seg_hash"].startswith("sha256:") for a in r["prov"]["anchors"])
    # terms without a certain category stay out of kb/ (M14): units, states, markers, other turns
    for absent in ("CON-unit", "CON-routed", "CON-game_turn", "CON-player_turn", "CON-reserve", "CON-hex"):
        assert absent not in {r["id"] for r in recs}


# --- patterns ------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("text, segment_type, found", [
    ("Roll 1d6.", "rule", [("die", "d6", "d6", "1d6", "1d6")]),
    ("Roll 2D6 and add 1d10.", "rule", [("die", "d6", "d6", "2D6", "2D6"), ("die", "d10", "d10", "1d10", "1d10")]),
    ("Add 1d6+1 to the result", "rule", [("die", "d6", "d6", "1d6", "1d6")]),
    ("Scenario: Night Attack", "heading", [("scenario", "scn.night_attack", "Night Attack", "Night Attack",
                                            "Scenario: Night Attack")]),
    ("Scenario:  The   Ford ", "heading", [("scenario", "scn.the_ford", "The Ford", "The Ford",
                                             "Scenario: The Ford")]),
    ("Phases:\n1. Rally Phase\n2) Air Superiority Phase.\n3. Movement", "rule",
     [("phase", "rally_phase", "Rally Phase", "Rally Phase", "Rally Phase"),
      ("phase", "air_superiority_phase", "Air Superiority Phase", "Air Superiority Phase", "Air Superiority Phase")]),
    ("1. Défense Phase\n2. End Phase", "rule",
     [("phase", "defense_phase", "Défense Phase", "Défense Phase", "Défense Phase"),
      ("phase", "end_phase", "End Phase", "End Phase", "End Phase")]),
])
def test_positive_patterns(text, segment_type, found):
    assert matches(text, segment_type) == found


@pytest.mark.parametrize("text, segment_type", [
    ("During his Movement Phase, the active player may move.", "rule"),       # phase in prose
    ("Each Player Turn consists of the following phases, in this order:", "rule"),
    ("1. Rally Phase", "rule"),                                               # one numbered line is not a list
    ("1. rally phase\n2. movement phase", "rule"),                            # not capitalized
    ("1. Rally Phase: rally one unit\n2. Movement Phase (3.0)", "rule"),      # more than the phase name
    ("Rally Phase\nMovement Phase", "rule"),                                  # bullet list (markers removed)
    ("1. Game Turn\n2. Player Turn", "rule"),                                 # turns have no certain pattern
    ("Scenario: The Ford", "rule"),                                           # not a heading
    ("In this scenario, a rally attempt succeeds.", "rule"),
    ("Scenario 2: The Ford", "heading"),                                      # numbered form not in the pattern
    ("Scenario: ★★", "heading"),                                              # nothing ASCII for the key
    ("Place the 3D map and the d6 counters in hex D6.", "rule"),              # no NdM with a count
    ("Roll x1d6 or 1d1 or 0d6 or 1d6x.", "rule"),
    ("A game lasts six Game Turns.", "rule"),
])
def test_negative_patterns(text, segment_type):
    assert matches(text, segment_type) == []


def test_term_without_certain_category_gives_no_record(game):
    ws = Workspace(game)
    ids = {p["record"]["id"] for p in harvest(ws)}
    # 1.2, 3.1, 4.1: Routed, Movement Phase in prose, Combat Phase in prose: nothing new from those segments
    for sid in ("SEG-dsk.1.2", "SEG-dsk.3.1", "SEG-dsk.4.1", "SEG-dsk.6.2", "SEG-dsk.7.1"):
        assert terms.matches(ws.segment(sid), ws.text(sid)) == []
    assert ids == set(CONCEPTS)


def test_validate_rejects_guessed_category_and_unquoted_anchor(game):
    ws = Workspace(game)
    [inputs] = terms.HARVEST.input_selector(ws, tasks.select(ws, "all"))
    proposals = harvest(ws)
    assert terms.HARVEST.validate(ws, inputs, proposals) == []
    guessed = {"record": {"kind": "concept", "id": "CON-unit", "category": "entity_type", "name": "unit"},
               "anchors": [{"seg": "SEG-dsk.1.1", "quote": "Each unit"}]}
    unquoted = {"record": {"kind": "concept", "id": "CON-d8", "category": "die", "name": "d8"},
                "anchors": [{"seg": "SEG-dsk.4.2"}]}
    wrong_key = {"record": {"kind": "concept", "id": "CON-ford", "category": "scenario", "name": "The Ford"},
                 "anchors": [{"seg": "SEG-dsk.7.0", "quote": "Scenario: The Ford"}]}
    # well-formed, with a verbatim quote from an input, but no pattern gives it: still rejected
    unmatched = {"record": {"kind": "concept", "id": "CON-d8", "category": "die", "name": "d8"},
                 "anchors": [{"seg": "SEG-dsk.2.2", "quote": "Rally Phase"}]}
    swapped = {"record": {"kind": "concept", "id": "CON-d6", "category": "die", "name": "d6"},
               "anchors": [{"seg": "SEG-dsk.4.2", "quote": "attack"}]}
    issues = terms.HARVEST.validate(ws, inputs, [guessed, unquoted, wrong_key, unmatched, swapped])
    assert issues == [
        "CON-unit: kategoria `entity_type` nie wynika z wzorca; wgc.terms.harvest daje tylko die, phase, scenario "
        "(pozostałe kategorie ustala M14).",
        "CON-d8: żaden wzorzec w wejściach joba nie daje tego ID z kategorią `die`.",
        "CON-d8: kotwica w SEG-dsk.4.2 bez cytatu dosłownego.",
        "CON-ford: klucz `ford` nie ma postaci wymaganej dla kategorii `scenario`.",
        "CON-ford: żaden wzorzec w wejściach joba nie daje tego ID z kategorią `scenario`.",
        "CON-ford: cytat 'Scenario: The Ford' w SEG-dsk.7.0 nie jest dopasowaniem wzorca tego pojęcia.",
        "CON-d8: żaden wzorzec w wejściach joba nie daje tego ID z kategorią `die`.",
        "CON-d8: cytat 'Rally Phase' w SEG-dsk.2.2 nie jest dopasowaniem wzorca tego pojęcia.",
        "CON-d6: cytat 'attack' w SEG-dsk.4.2 nie jest dopasowaniem wzorca tego pojęcia.",
    ]
    for wrong in (guessed, unmatched):
        res = kb.accept(game, terms.HARVEST, inputs, [wrong], by=BY, ws=ws)
        assert not res.ok and not res.domain_valid and not (game / "kb").exists()


def test_quote_not_in_segment_is_rejected(game):
    ws = Workspace(game)
    [inputs] = terms.HARVEST.input_selector(ws, tasks.select(ws, "all"))
    proposals = harvest(ws)
    proposals[4]["anchors"][0]["quote"] = "2d6"
    res = kb.accept(game, terms.HARVEST, inputs, proposals, by=BY, ws=ws)
    assert res.issues == ["CON-d6: cytat '2d6' w SEG-dsk.4.2 nie jest dopasowaniem wzorca tego pojęcia.",
                          "CON-d6: cytat '2d6' nie występuje dosłownie w segmencie SEG-dsk.4.2."]
    assert not (game / "kb").exists()


# --- IDs -----------------------------------------------------------------------------------------------------------

def test_slug():
    assert terms.slug("Rally Phase") == "rally_phase"
    assert terms.slug("Rally-Phase") == "rally_phase"
    assert terms.slug("The  Ford!") == "the_ford"
    assert terms.slug("Défense") == "defense"
    assert terms.slug("★★") == ""


def test_ids_are_deterministic_and_do_not_collide_between_documents(game):
    add_document(game, "SRC-dsk.scenario_book", "scenario_book", "scenarios.md",
                 "# Scenarios\n\n## 1.0 Scenario: The Ford\n\n**1.1** Roll 1d6 for the weather.\n")
    add_document(game, "SRC-dsk.rules.2", "rules", "advanced.md",
                 "# Advanced rules\n\n**1.1** Each Player Turn has these phases:\n1. Air Phase\n2. End Phase\n\n"
                 "**1.2** Roll 2d6.\n")
    ws = Workspace(game)
    assert terms.main_rules(ws) == "SRC-dsk.rules"
    first = harvest(ws)
    ids = [p["record"]["id"] for p in first]
    assert ids == CONCEPTS + ["CON-dsk.scenario_book:scn.the_ford", "CON-dsk.scenario_book:d6",
                              "CON-dsk.rules.2:air_phase", "CON-dsk.rules.2:end_phase", "CON-dsk.rules.2:d6"]
    assert len(set(ids)) == len(ids)
    assert harvest(Workspace(game)) == first  # same inventory → same IDs and proposals

    # the main rules do not depend on the order of documents in the inventory
    inv = source.read_inventory(game)
    inv.documents.reverse()
    source.write_inventory(game, inv)
    assert terms.main_rules(Workspace(game)) == "SRC-dsk.rules"
    by_id = lambda ps: sorted(ps, key=lambda p: p["record"]["id"])  # noqa: E731  (jobs follow document order)
    assert by_id(harvest(Workspace(game))) == by_id(first)

    res = build(game)
    assert res.state == "done" and [j.task for j in res.jobs].count("wgc.terms.harvest") == 3
    assert validate([game / "source", game / "kb"]).ok
    assert sorted(r["id"] for r in concepts(game)) == sorted(ids)
    assert sorted(p.name for p in (game / "kb" / "logic").iterdir()) == ["concepts.yaml", "tables.yaml"]


def test_concept_id():
    ws = type("WS", (), {"inventory": type("Inv", (), {"documents": [
        {"id": "SRC-g.rules.2", "role": "rules"}, {"id": "SRC-g.rules", "role": "rules"},
        {"id": "SRC-g.faq", "role": "faq"}]})()})()
    assert terms.concept_id(ws, "SRC-g.rules", "d6") == "CON-d6"
    assert terms.concept_id(ws, "SRC-g.rules.2", "d6") == "CON-g.rules.2:d6"
    assert terms.concept_id(ws, "SRC-g.faq", "scn.x") == "CON-g.faq:scn.x"


# --- idempotence, scope, dry-run -----------------------------------------------------------------------------------

def test_rebuild_and_other_scopes_keep_kb(game):
    build(game)
    before = tree(game / "kb")
    for scope in ("all", "chapter:5", "segment:SEG-dsk.7.0", "chapter:2"):
        res = build(game, scope)
        assert res.state == "done" and res.metrics["records_created"] == res.metrics["records_updated"] == 0
        assert tree(game / "kb") == before, scope
    plan = planner.plan(Workspace(game), "1", "chapter:3")
    assert len(plan.jobs) == 1  # owned document still reconciles when a scoped segment has no match


def test_harvest_records_do_not_depend_on_scope(game):
    ws = Workspace(game)
    assert harvest(ws, "chapter:5") == harvest(ws, "segment:SEG-dsk.7.0") == harvest(ws, "all")


def test_dry_run_writes_nothing(game, capsys):
    before = tree(game)
    assert main(["build", "--root", str(game), "--stage", "1", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "wgc.terms.harvest@0" in out and ", ".join(HARVEST_INPUTS) in out
    assert tree(game) == before and not db_path(game).exists() and not (game / "kb").exists()


def test_vanished_term_is_retired_by_owner(game):
    """The harvest owner retires the missing output and writes the replacement in one batch."""
    build(game)
    rulebook = game / "rulebook.md"
    rulebook.write_text(rulebook.read_text(encoding="utf-8").replace("4. End Phase", "4. Supply Phase"),
                        encoding="utf-8", newline="\n")
    source.extract(game)
    res = build(game)
    assert res.state == "failed" and [j.state for j in res.jobs] == ["failed", "done"]
    assert "CON-supply_phase" in res.jobs[1].records
    assert "CON-end_phase" not in {r["id"] for r in concepts(game)}
    res = build(game)
    assert res.state == "done" and res.metrics["records_created"] == 0
    assert "CON-end_phase" not in {r["id"] for r in concepts(game)}
    assert validate([game / "source", game / "kb"]).ok


def test_harvest_spec_fields():
    spec = tasks.get("wgc.terms.harvest")
    assert spec is terms.HARVEST and spec.name == "wgc.terms.harvest@0" and spec.stage == "stage1"
    assert spec.output_kind == "concept" and spec.output_schema == "wgc/logic@0#concept"
    assert spec.prompt is None and spec.decoding_schema is None and spec.deterministic_impl is not None
    assert dataclasses.replace(spec).name == spec.name
