"""IG documentation continuity and byte preservation of the archived experiment."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import tomllib
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
PUBLIC_ARCHIVE = ROOT / 'archive/poc-2026-10-11'
MANIFEST = ROOT / 'private/archive/poc-2026-10-11/manifest.json'
ACTIVE_MARKDOWN = sorted([ROOT / 'README.md', ROOT / 'CLAUDE.md', *DOCS.rglob('*.md'), PUBLIC_ARCHIVE / 'README.md'])
LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)\)')
FENCE = re.compile(r'^```.*?^```\s*$', re.M | re.S)


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8-sig')


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


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


@pytest.mark.parametrize('path', ACTIVE_MARKDOWN, ids=lambda p: str(p.relative_to(ROOT)))
def test_active_links_resolve(path: Path):
    for href in LINK.findall(FENCE.sub('', read(path))):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', href):
            continue
        target, _, anchor = unquote(href).partition('#')
        destination = (path.parent / target).resolve() if target else path.resolve()
        assert destination.exists(), f'{path}: missing {href}'
        if anchor and destination.suffix.lower() == '.md':
            assert anchor in anchors(read(destination)), f'{path}: missing anchor {href}'


def test_ig_is_the_only_active_queue():
    rows = re.findall(r'^\| (IG-\d+) \| (\w+) \|', read(DOCS / 'ROADMAP.md'), re.M)
    assert len(rows) == len(dict(rows)) == 6
    pending = [stage for stage, status in rows if status == 'next']
    assert len(pending) == 1
    current = pending[0]
    assert all(status in {'next', 'planned', 'done', 'partial'} for _, status in rows)
    assert f'**Bieżący etap:** {current}.' in read(DOCS / 'STATUS.md')
    assert f'**Następny etap:** {current}.' in read(DOCS / 'HANDOFF.md')
    assert not (DOCS / 'POC-PLAN.md').exists()
    assert not (DOCS / 'work/tasks/M-POC5A.md').exists()
    assert not (ROOT / 'private/poc').exists()
    assert not (ROOT / 'private/source-artifacts').exists()


def test_archived_experiment_is_byte_preserved():
    manifest = json.loads(read(MANIFEST))
    verification = json.loads(read(PUBLIC_ARCHIVE / 'verification.json'))
    assert verification['result'] == 'verified'
    assert sha256(MANIFEST) == verification['full_manifest_sha256']
    entries = manifest['entries']
    assert len(entries) == verification['files_checked'] == 3117
    assert len({item['original_path'] for item in entries}) == len(entries)
    assert len({item['archive_path'] for item in entries}) == len(entries)
    assert manifest['completion_state'] == 'incomplete_experiment_archived'
    for item in entries:
        path = (ROOT / item['archive_path']).resolve()
        assert path.is_relative_to(ROOT / 'archive/poc-2026-10-11') or path.is_relative_to(ROOT / 'private/archive/poc-2026-10-11')
        assert path.is_file(), f'Missing archived file: {item["original_path"]}'
        assert path.stat().st_size == item['bytes'], f'Length changed: {item["original_path"]}'
        assert sha256(path) == item['sha256'], f'Bytes changed: {item["original_path"]}'


def test_runtime_and_test_collection_exclude_archives(request):
    config = tomllib.loads(read(ROOT / 'pyproject.toml'))
    assert set(config) == {'tool'}
    options = config['tool']['pytest']['ini_options']
    assert options['testpaths'] == ['tests']
    assert {'archive', 'private'} <= set(options['norecursedirs'])
    assert all(Path(str(item.path)).resolve().is_relative_to(ROOT / 'tests') for item in request.session.items)
    assert not any((ROOT / name).exists() for name in ('wgc', 'glu', 'contracts', 'bench', '.glu'))


def test_embedded_json_examples_are_syntactically_valid():
    examples = re.findall(r'^```json\r?\n(.*?)^```', read(DOCS / 'IG-DATA-MODEL.md'), re.M | re.S)
    assert examples
    for example in examples:
        parsed = json.loads(example)
        assert parsed['schema_version'] == 'ig-draft-0.2'


def test_archive_git_attributes_preserve_original_bytes():
    attributes = read(ROOT / '.gitattributes')
    assert '/archive/poc-2026-10-11/project/** -text -eol -filter' in attributes
    assert '/private/** -text -eol -filter' in attributes
