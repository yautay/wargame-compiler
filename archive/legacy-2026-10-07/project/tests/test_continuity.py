"""Project continuity: STATUS, ROADMAP, HANDOFF, ADR index and the Session 0 DoD matrix stay consistent,
and every relative Markdown link (file and #anchor) resolves. A red test here means an unfinished session."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MD_FILES = sorted([*ROOT.glob("*.md"), *DOCS.rglob("*.md"), *(ROOT / "bench").rglob("*.md")])

FENCE = re.compile(r"```.*?```", re.S)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
EXPLICIT_ANCHOR = re.compile(r'<a id="([^"]+)"></a>')


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slug(heading: str) -> str:
    """GitHub-style heading anchor: lowercase, drop punctuation (keep unicode letters), spaces → hyphens."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    body = FENCE.sub("", text(path))
    return {slug(h) for h in HEADING.findall(body)} | set(EXPLICIT_ANCHOR.findall(body))


def links(path: Path) -> list[str]:
    return [m for m in LINK.findall(FENCE.sub("", text(path))) if not re.match(r"^[a-z]+:", m)]


@pytest.mark.parametrize("md", MD_FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_relative_links_resolve(md):
    broken = []
    for href in links(md):
        target, _, anchor = href.partition("#")
        dest = (md.parent / target).resolve() if target else md
        if not dest.exists():
            broken.append(f"{href}: missing file")
        elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
            broken.append(f"{href}: missing anchor")
    assert not broken, "\n".join(broken)


def current_milestone() -> str:
    m = re.search(r"\*\*Bieżący milestone:\*\*\s*(M[\w-]+)", text(DOCS / "STATUS.md"))
    assert m, "STATUS.md must name the current milestone as '**Bieżący milestone:** Mx'"
    return m.group(1)


def roadmap_milestones() -> dict[str, str]:
    """milestone id → status, from '### Mx: …' headings followed by '- **Status:** …'."""
    out = {}
    for m in re.finditer(r"^### (M[\w-]+):.*?\n- \*\*Status:\*\*\s*(\w+)", text(DOCS / "ROADMAP.md"), re.M):
        out[m.group(1)] = m.group(2)
    return out


def test_roadmap_milestones_have_status():
    headings = re.findall(r"^### (M[\w-]+):", text(DOCS / "ROADMAP.md"), re.M)
    assert headings and set(headings) == set(roadmap_milestones()), "every milestone heading needs a Status line"
    assert set(roadmap_milestones().values()) <= {"done", "next", "planned", "optional"}


def test_current_milestone_is_next_in_roadmap():
    ms = roadmap_milestones()
    cur = current_milestone()
    assert cur in ms, f"{cur} from STATUS.md is not in ROADMAP.md"
    assert ms[cur] == "next", f"{cur} should have status 'next' in ROADMAP.md"
    assert list(ms.values()).count("next") == 1, "exactly one milestone is 'next'"


def test_handoff_points_to_existing_file_for_last_done_milestone():
    hrefs = [h for h in links(DOCS / "HANDOFF.md") if h.startswith("handoff/")]
    assert hrefs, "HANDOFF.md must link the latest handoff"
    latest = DOCS / hrefs[0]
    assert latest.exists()
    assert re.match(r"\d{4}-\d{2}-\d{2}-M[\w-]+\.md$", latest.name)
    milestone = latest.stem.split("-", 3)[3]
    assert roadmap_milestones().get(milestone) == "done", f"latest handoff is for {milestone}, which is not 'done'"


def test_adr_index_matches_files():
    adr_dir = DOCS / "adr"
    files = {p.name for p in adr_dir.glob("ADR-*.md")}
    listed = {Path(h).name for h in links(adr_dir / "README.md") if h.startswith("ADR-")}
    assert files == listed, f"unlisted: {files - listed}, missing: {listed - files}"
    numbers = sorted(int(n[4:8]) for n in files)
    assert numbers == list(range(1, len(numbers) + 1)), "ADR numbers must be consecutive"
    for f in files:
        assert "**Status:**" in text(adr_dir / f), f"{f} has no Status line"


def test_dod_matrix_covers_all_27_items():
    rows = re.findall(r"^\| (\d+) \|", text(DOCS / "DOD-SESSION-0.md"), re.M)
    assert [int(r) for r in rows] == list(range(1, 28))


def test_dod_mentioned_repo_paths_exist():
    for p in re.findall(r"`((?:contracts|bench|tests|wgc|glu)/[^`]+)`", text(DOCS / "DOD-SESSION-0.md")):
        assert (ROOT / p).exists(), p
