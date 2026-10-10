"""Active POC continuity and isolation; no imports from the legacy project."""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
import re
import tomllib
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
TASKS = DOCS / 'work/tasks'
ACTIVE_MARKDOWN = sorted([ROOT / 'README.md', ROOT / 'CLAUDE.md', *DOCS.rglob('*.md')])
LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)\)')
FENCE = re.compile(r'^```.*?^```\s*$', re.M | re.S)
LEGACY = ROOT / 'archive/legacy-2026-10-07'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def field(body: str, key: str) -> str:
    match = re.search(r'^- \*\*' + re.escape(key) + r':\*\*\s*(\S+)', body, re.M)
    assert match, f'Missing field: {key}'
    return match.group(1)


def roadmap(body: str) -> dict[str, str]:
    rows = re.findall(r'^\| (M-POC\d+) \| (\w+) \|', body, re.M)
    assert rows, 'No milestone rows'
    assert len(rows) == len(dict(rows)), 'Duplicate milestone'
    assert all(status in {'done', 'next', 'planned'} for _, status in rows)
    return dict(rows)


def next_milestone(rows: dict[str, str]) -> str:
    pending = [key for key, value in rows.items() if value == 'next']
    assert len(pending) == 1, 'Exactly one next milestone required'
    return pending[0]


def check_poc1_card_progress(card: str, results: dict[str, str]) -> None:
    order = ['M-POC1A', 'M-POC1B', 'M-POC1C']
    assert card in order, 'Current card must belong to M-POC1'
    position = order.index(card)
    assert all(results.get(prior) == 'done' for prior in order[:position]), 'Previous cards must be done'
    assert results.get(card) != 'done', 'Completed card cannot remain current'


def check_completed_card_handoff(milestone: str, completed: str, current: str,
                                 results: dict[str, str]) -> None:
    orders = {
        'M-POC1': ['M-POC1A', 'M-POC1B', 'M-POC1C'],
        'M-POC2': ['M-POC2A', 'M-POC2B'],
        'M-POC4': ['M-POC4A', 'M-POC4B'],
    }
    assert milestone in orders, 'Unsupported within-milestone handoff'
    order = orders[milestone]
    assert completed in order and current in order, 'Cards must belong to milestone'
    assert order.index(current) == order.index(completed) + 1, 'Handoff must advance one card'
    assert all(results.get(card) == 'done' for card in order[:order.index(current)]), 'Previous cards must be done'
    assert results.get(current) != 'done', 'Completed card cannot remain current'


def anchors(body: str) -> set[str]:
    body = FENCE.sub('', body)
    result = set(re.findall(r'<a id="([^"]+)">', body))
    used: dict[str, int] = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*$', body, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = used.get(slug, 0)
        used[slug] = count + 1
        result.add(f'{slug}-{count}' if count else slug)
    return result


def link_errors(path: Path) -> list[str]:
    errors = []
    for href in LINK.findall(FENCE.sub('', read(path))):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', href):
            continue
        target, _, anchor = unquote(href).partition('#')
        dest = (path.parent / target).resolve() if target else path.resolve()
        if not dest.exists():
            errors.append(f'{href}: missing target')
        elif anchor and dest.suffix.lower() == '.md' and anchor not in anchors(read(dest)):
            errors.append(f'{href}: missing anchor')
    return errors


@pytest.mark.parametrize('path', ACTIVE_MARKDOWN, ids=lambda p: str(p.relative_to(ROOT)))
def test_active_markdown_links(path):
    assert not link_errors(path), '\n'.join(link_errors(path))


def test_roadmap_status_handoff_and_current_card_agree():
    rows = roadmap(read(DOCS / 'ROADMAP.md'))
    assert set(rows) == {f'M-POC{i}' for i in range(8)}
    current = next_milestone(rows)
    status = read(DOCS / 'STATUS.md')
    pointer = read(DOCS / 'HANDOFF.md')
    assert field(status, 'Bieżący milestone') == current
    assert field(pointer, 'Następny milestone') == current
    card = field(status, 'Bieżąca karta')
    assert field(pointer, 'Następna karta') == card
    assert field(read(TASKS / f'{card}.md'), 'Milestone') == current
    links = re.findall(r'\]\((handoff/[^)]+\.md)\)', pointer)
    assert len(links) == 1, 'Handoff pointer must identify one latest session'
    handoff = read(DOCS / links[0])
    outcome = field(handoff, 'Wynik')
    milestone = field(handoff, 'Milestone')
    assert outcome in {'done', 'partial', 'blocked'}
    assert field(pointer, 'Wynik') == outcome
    assert field(handoff, 'Następny milestone') == current
    assert field(handoff, 'Następna karta') == card
    if outcome == 'done':
        if rows[milestone] != 'done':
            # Completing one card does not complete its containing milestone.
            assert milestone == current
            completed = field(handoff, 'Karta')
            results = dict(re.findall(r'^- \*\*Wynik (M-POC\d+[A-C]):\*\*\s*(\w+)', status, re.M))
            check_completed_card_handoff(milestone, completed, card, results)
    else:
        assert milestone == current
    if current == 'M-POC1':
        assert rows['M-POC0'] == 'done'
        assert field(status, 'Wynik M-POC0') == 'done'
        results = dict(re.findall(r'^- \*\*Wynik (M-POC1[A-C]):\*\*\s*(\w+)', status, re.M))
        check_poc1_card_progress(card, results)


@pytest.mark.parametrize('path', sorted(TASKS.glob('M-POC*.md')), ids=lambda p: p.stem)
def test_cards_are_complete_and_indexed(path):
    body = read(path)
    assert field(body, 'ID') == path.stem
    assert field(body, 'Milestone') in roadmap(read(DOCS / 'ROADMAP.md'))
    assert field(body, 'Rola')
    assert field(body, 'Zależności')
    sections = ['Cel i pytanie eksperymentalne', 'Dokładne pliki do przeczytania',
                'Wejścia i wersja oceny', 'Wymagane działania',
                'Artefakty wyjściowe i lokalizacje', 'Kryteria zakończenia i kontrole',
                'Zakres wyłączony', 'Przegląd człowieka', 'Wznowienie', 'Przekazanie']
    for section in sections:
        match = re.search(r'^## ' + re.escape(section) + r'\n+(.*?)(?=^## |\Z)', body, re.M | re.S)
        assert match and len(match.group(1).strip()) > 20, f'Empty section: {section}'
    assert f']({path.name})' in read(TASKS / 'README.md')
    assert f'](work/tasks/{path.name})' in read(DOCS / 'ROADMAP.md')


def test_task_inventory_is_not_vacuous():
    expected = {'M-POC0', 'M-POC1A', 'M-POC1B', 'M-POC1C', 'M-POC2A', 'M-POC2B',
                'M-POC3', 'M-POC4A', 'M-POC4B', 'M-POC5A', 'M-POC5B',
                'M-POC6A', 'M-POC6B', 'M-POC7A', 'M-POC7B'}
    assert {p.stem for p in TASKS.glob('M-POC*.md')} == expected


def test_decision_index_separates_active_and_history():
    index = read(DOCS / 'adr/README.md')
    active, history = index.split('## Historyczne')
    assert '## Aktywne' in active
    assert 'ADR-0039' in active and 'archive/' not in active
    assert 'ADR-0001–ADR-0038' in history and 'archive/legacy-2026-10-07/project/docs/adr/README.md' in history
    assert {p.name for p in (DOCS / 'adr').glob('ADR-*.md')} == {'ADR-0039-archiwum-i-poc-przed-architektura.md'}
    for name in ('README.md', 'CLAUDE.md'):
        body = read(ROOT / name)
        assert 'docs/POC-PLAN.md' in body and 'archive/legacy-2026-10-07/README.md' in body


def test_active_configuration_has_no_legacy_runtime():
    config = tomllib.loads(read(ROOT / 'pyproject.toml'))
    assert set(config) == {'tool'}, 'No active distribution or legacy dependency metadata'
    options = config['tool']['pytest']['ini_options']
    assert options['testpaths'] == ['tests']
    assert {'archive', 'private'} <= set(options['norecursedirs'])
    assert '--import-mode=importlib' in options['addopts']
    for name in ('wgc', 'glu', 'contracts', 'bench', 'requirements.txt', 'wargame_compiler.egg-info', '.glu'):
        assert not (ROOT / name).exists(), f'Legacy entry still active: {name}'
    assert importlib.util.find_spec('wgc') is None, 'Legacy wgc exposed to active imports'
    assert importlib.util.find_spec('glu') is None, 'Legacy glu exposed to active imports'


def test_active_code_does_not_import_legacy():
    code_paths = [*ROOT.glob('*.py'), *(ROOT / 'tests').rglob('*.py'), *(ROOT / 'scripts').rglob('*.py')]
    assert code_paths
    for path in code_paths:
        tree = ast.parse(read(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(alias.name.split('.')[0] not in {'wgc', 'glu', 'archive'} for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert (node.module or '').split('.')[0] not in {'wgc', 'glu', 'archive'}
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert ast.unparse(node.func) not in {'sys.path.insert', 'sys.path.append'}


def test_collection_is_only_active_tests(request):
    paths = {Path(str(item.path)).resolve() for item in request.session.items}
    assert paths and all(path.is_relative_to(ROOT / 'tests') for path in paths)
    assert all(not path.is_relative_to(LEGACY) for path in paths)


def test_generated_files_are_ignored_and_private_is_versionable():
    lines = {line.strip() for line in read(ROOT / '.gitignore').splitlines()}
    assert {'.venv/', '__pycache__/', '.pytest_cache/', '.glu/'} <= lines
    assert '/private/' not in lines, 'Owner authorized versioning private artifacts'


def test_broken_link_and_anchor_are_detected(tmp_path):
    doc = tmp_path / 'test.md'
    target = tmp_path / 'target.md'
    target.write_text('# Valid\n', encoding='utf-8')
    doc.write_text('[missing](absent.md)\n[anchor](target.md#absent)\n', encoding='utf-8')
    assert len(link_errors(doc)) == 2
    doc.write_text('[valid](target.md#valid)\n', encoding='utf-8')
    assert link_errors(doc) == []


def test_duplicate_and_multiple_next_are_rejected():
    with pytest.raises(AssertionError, match='Duplicate'):
        roadmap('| M-POC0 | next | x |\n| M-POC0 | planned | x |')
    with pytest.raises(AssertionError, match='Exactly one'):
        next_milestone({'M-POC0': 'next', 'M-POC1': 'next'})
    with pytest.raises(AssertionError, match='Exactly one'):
        next_milestone({'M-POC0': 'done', 'M-POC1': 'planned'})


@pytest.mark.parametrize('card,results', [
    ('M-POC1A', {}),
    ('M-POC1B', {'M-POC1A': 'done'}),
    ('M-POC1C', {'M-POC1A': 'done', 'M-POC1B': 'done'}),
])
def test_poc1_card_progress_accepts_completed_prerequisites(card, results):
    check_poc1_card_progress(card, results)


@pytest.mark.parametrize('card,results', [
    ('M-POC1B', {}),
    ('M-POC1B', {'M-POC1A': 'partial'}),
    ('M-POC1C', {'M-POC1A': 'done'}),
    ('M-POC1A', {'M-POC1A': 'done'}),
    ('M-POC2A', {'M-POC1A': 'done'}),
])
def test_poc1_card_progress_rejects_skips_and_completed_current_card(card, results):
    with pytest.raises(AssertionError):
        check_poc1_card_progress(card, results)


def test_poc2_handoff_accepts_completed_preparation():
    check_completed_card_handoff('M-POC2', 'M-POC2A', 'M-POC2B', {'M-POC2A': 'done'})


@pytest.mark.parametrize('completed,current,results', [
    ('M-POC2A', 'M-POC2B', {}),
    ('M-POC2A', 'M-POC2A', {'M-POC2A': 'done'}),
    ('M-POC2A', 'M-POC2B', {'M-POC2A': 'done', 'M-POC2B': 'done'}),
    ('M-POC1C', 'M-POC2B', {'M-POC1C': 'done'}),
])
def test_poc2_handoff_rejects_incomplete_repeated_or_wrong_cards(completed, current, results):
    with pytest.raises(AssertionError):
        check_completed_card_handoff('M-POC2', completed, current, results)


def test_poc4_handoff_accepts_completed_context_selection():
    check_completed_card_handoff('M-POC4', 'M-POC4A', 'M-POC4B',
                                 {'M-POC4A': 'done', 'M-POC4B': 'planned'})


@pytest.mark.parametrize('completed,current,results', [
    ('M-POC4A', 'M-POC4B', {}),
    ('M-POC4A', 'M-POC4B', {'M-POC4A': 'partial'}),
    ('M-POC4A', 'M-POC4A', {'M-POC4A': 'done'}),
    ('M-POC4A', 'M-POC4B', {'M-POC4A': 'done', 'M-POC4B': 'done'}),
    ('M-POC4A', 'M-POC5A', {'M-POC4A': 'done'}),
    ('M-POC3', 'M-POC4B', {'M-POC3': 'done'}),
])
def test_poc4_handoff_rejects_unreviewed_repeated_completed_or_wrong_cards(completed, current, results):
    with pytest.raises(AssertionError):
        check_completed_card_handoff('M-POC4', completed, current, results)
