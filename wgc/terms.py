"""Task `wgc.terms.harvest@0` (Tier 0): terms whose category the printed form alone makes certain → `concept`
records (`CON-`), ADR-0030.

Patterns (nothing else gives a record; the category of every other term is decided in M14):
- **die:** dice notation `NdM` with a count (`1d6`, `2D6`; a whole word, N ≥ 1, M ≥ 2) → key `d<M>`, name `d<M>`. The
  concept is the die, so `1d6` and `2d6` are one concept `CON-d6`;
- **scenario:** a heading segment whose whole text is `Scenario: X` → key `scn.<slug(X)>`, name `X`;
- **phase:** a line of a numbered list (at least two lines `N.` or `N)` in the segment) whose whole item is
  capitalized words ending in `Phase` (`1. Rally Phase`) → key `<slug(name)>` (always ends in `_phase`), name as
  printed. Mentions in prose (`During his Movement Phase`) give nothing.

`slug`: NFKD, ASCII only, lower case, runs of `[a-z0-9]` joined by `_`. A key outside the ID grammar gives no record.

ID (DATA-CONTRACTS §10): `CON-<key>` for the main rules (the `rules` document with the smallest `SRC-` id, i.e.
`SRC-<game>.rules`), `CON-<SRC key>:<key>` for every other document. The SRC key is unique in the inventory, so two
documents never propose the same ID; joining concepts across documents is M14's job.

Jobs: one per document. The job is planned when the scope contains a segment with a match, and its inputs are all
segments of that document with a match, whatever the scope: a record never depends on `--scope`. One proposal per ID;
`source_terms` lists the printed terms in order of first occurrence, and each printed term has one anchor at its
first occurrence with a verbatim `quote` (the term; for a scenario the whole `Scenario: X`), no `span`.
"""
from __future__ import annotations

import re
import unicodedata

from wgc import ids
from wgc.tasks import Inputs, TaskSpec

TASK_ID = "wgc.terms.harvest"
VERSION = "0"
CATEGORIES = ("die", "phase", "scenario")  # the only categories this task may give

_DIE = re.compile(r"\b(\d+)[dD](\d+)\b")
_SCENARIO = re.compile(r"^Scenario\s*:\s*(\S.*?)\s*$")
_LIST_ITEM = re.compile(r"^\s*\d+[.)]\s+\S")
_PHASE_ITEM = re.compile(r"^\s*\d+[.)]\s+((?:[A-Z][\w'’-]*\s+)+Phase)\s*\.?\s*$")
_KEY_SHAPES = {"die": re.compile(r"^d[1-9]\d*$"), "phase": re.compile(r"^[a-z0-9_]+_phase$"),
               "scenario": re.compile(r"^scn\.[a-z0-9_]+$")}


def _squash(text: str) -> str:
    return " ".join(text.split())


def slug(text: str) -> str:
    """`Rally Phase` → `rally_phase`, `The Ford` → `the_ford`; empty when nothing ASCII is left."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return "_".join(re.findall(r"[a-z0-9]+", ascii_text.lower()))


def matches(seg: dict, text: str) -> list[tuple[str, str, str, str, str]]:
    """(category, key, name, printed term, verbatim quote) of each pattern match in a segment."""
    out = []
    if seg.get("segment_type") == "heading":
        m = _SCENARIO.match(_squash(text))
        if m and slug(m[1]):
            out.append(("scenario", f"scn.{slug(m[1])}", m[1], m[1], m[0]))
    lines = text.split("\n")
    if sum(1 for line in lines if _LIST_ITEM.match(line)) >= 2:
        for line in lines:
            m = _PHASE_ITEM.match(line)
            if m:
                name = _squash(m[1])
                out.append(("phase", slug(name), name, name, name))
    for m in _DIE.finditer(_squash(text)):
        sides = int(m[2])
        if int(m[1]) >= 1 and sides >= 2:
            out.append(("die", f"d{sides}", f"d{sides}", m[0], m[0]))
    return out


def main_rules(ws) -> str | None:
    """`SRC-` id of the main rules: the `rules` document with the smallest id (`wgc source init` names the next
    ones `.2`, `.3`)."""
    rules = [d["id"] for d in ws.inventory.documents if d.get("role") == "rules"]
    return min(rules) if rules else None


def concept_id(ws, doc_id: str, key: str) -> str:
    return f"CON-{key}" if doc_id == main_rules(ws) else f"CON-{ids.parse_id(doc_id).key}:{key}"


def _has_match(ws, sid: str) -> bool:
    return bool(matches(ws.segment(sid), ws.text(sid)))


def _select(ws, segments: list[str]) -> list[Inputs]:
    """One job per document with a match inside the scope; inputs: every segment of that document with a match."""
    docs: list[str] = []
    for sid in segments:
        doc = ws.segment(sid)["doc"]
        if doc not in docs and _has_match(ws, sid):
            docs.append(doc)
    return [tuple(s["id"] for s in ws.inventory.segments if s["doc"] == doc and _has_match(ws, s["id"]))
            for doc in docs]


def _run(ws, inputs: Inputs) -> list[dict]:
    found: dict[str, dict] = {}
    for sid in inputs:
        seg = ws.segment(sid)
        for category, key, name, term, quote in matches(seg, ws.text(sid)):
            cid = concept_id(ws, seg["doc"], key)
            if not ids.is_id(cid):
                continue
            p = found.setdefault(cid, {"record": {"kind": "concept", "id": cid, "category": category, "name": name,
                                                  "source_terms": []}, "anchors": []})
            if term not in p["record"]["source_terms"]:
                p["record"]["source_terms"].append(term)
                p["anchors"].append({"seg": sid, "quote": quote})
    return list(found.values())


def _matched(ws, inputs: Inputs) -> dict[str, tuple[str, set[tuple[str, str]]]]:
    """ID → (category, every (segment, quote) of a pattern match) over the job inputs."""
    out: dict[str, tuple[str, set[tuple[str, str]]]] = {}
    for sid in inputs:
        seg = ws.segment(sid)
        for category, key, _name, _term, quote in matches(seg, ws.text(sid)):
            out.setdefault(concept_id(ws, seg["doc"], key), (category, set()))[1].add((sid, quote))
    return out


def _validate(ws, inputs: Inputs, proposals: list[dict]) -> list[str]:
    """No guessed category: every ID, category and quote must come from a pattern match in the job inputs."""
    issues = []
    matched = _matched(ws, inputs)
    for p in proposals:
        rec = p["record"]
        rid, category = rec["id"], rec.get("category")
        if category not in CATEGORIES:
            issues.append(f"{rid}: kategoria `{category}` nie wynika z wzorca; {TASK_ID} daje tylko "
                          f"{', '.join(CATEGORIES)} (pozostałe kategorie ustala M14).")
            continue
        key = ids.parse_id(rid).key.rsplit(":", 1)[-1]
        if not _KEY_SHAPES[category].match(key):
            issues.append(f"{rid}: klucz `{key}` nie ma postaci wymaganej dla kategorii `{category}`.")
        if matched.get(rid, (None,))[0] != category:
            issues.append(f"{rid}: żaden wzorzec w wejściach joba nie daje tego ID z kategorią `{category}`.")
        for a in p.get("anchors") or []:
            if "quote" not in a:
                issues.append(f"{rid}: kotwica w {a['seg']} bez cytatu dosłownego.")
            elif a["seg"] not in inputs:
                issues.append(f"{rid}: kotwica w {a['seg']} spoza wejść joba.")
            elif (a["seg"], a["quote"]) not in matched.get(rid, (None, set()))[1]:
                issues.append(f"{rid}: cytat {a['quote']!r} w {a['seg']} nie jest dopasowaniem wzorca tego pojęcia.")
        if not p.get("anchors"):
            issues.append(f"{rid}: pojęcie bez kotwicy.")
    return issues


HARVEST = TaskSpec(id=TASK_ID, version=VERSION, stage="stage1", output_kind="concept",
                   output_schema="wgc/logic@0#concept", input_selector=_select, validate=_validate,
                   deterministic_impl=_run)
