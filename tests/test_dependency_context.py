"""Dependency projections preserve needed metadata without exposing history or other pages."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


@pytest.fixture(autouse=True)
def isolate_live_guard(monkeypatch):
    monkeypatch.delenv('WGC_CONTEXT_GUARD', raising=False)
    monkeypatch.delenv('WGC_CONTEXT_GUARD_SHA256', raising=False)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    spec = importlib.util.spec_from_file_location('dependency_projection', ROOT / 'scripts/dependency_context.py')
    d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
finally:
    sys.path.pop(0)


def dump(p, body):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(body), encoding='utf-8')


def test_dependency_ceiling_counts_unicode_json_escapes():
    value = {'observation': '\u2192\U0001f3b2' * 2000}
    assert len(json.dumps(value, ensure_ascii=False).encode('utf-8')) < d.MAX_BYTES
    with pytest.raises(ValueError, match='byte ceiling'):
        d.bounded(value)


@pytest.fixture
def context(tmp_path):
    def pin(rel, body):
        dump(tmp_path / rel, body)
        return {'path': rel, 'sha256': d.w.digest(tmp_path / rel),
                'raw_text': 'EXTRA_PIN_FIELD_SENTINEL', 'events': ['EXTRA_PIN_FIELD_SENTINEL']}
    base = 'private/workflow/runs/IG-2B03/frozen/'
    pdf = pin('private/source.pdf', {'opaque': 'SOURCE_TEXT_SENTINEL'})
    provenance = pin('private/provenance.json', {'opaque': 'SOURCE_TEXT_SENTINEL'})
    inv = pin(base + 'final-verified/inventory.json', {
        'format': 'wgc-inventory-1', 'source': {'id': 'synthetic', 'sha256': pdf['sha256'],
            'pdf': pdf, 'provenance': provenance, 'page_count': 44, 'raw_text': 'SOURCE_TEXT_SENTINEL'},
        'pages': [{'id': f'p{n}', 'key': f'physical-page:{n}', 'pdf_page': n, 'revision': 'synthetic',
                   'label': 'UNASSIGNED_TEXT_SENTINEL'} for n in range(1, 45)],
        'regions': [{'id': f'r{n}', 'key': f'physical-page:{n}:placeholder', 'page_id': f'p{n}',
                     'kind': 'unclassified', 'box': [0, 0, 1, 1],
                     'raw_text': 'UNASSIGNED_TEXT_SENTINEL'} for n in range(1, 45)],
        'evidence': [{'raw_text': 'UNASSIGNED_TEXT_SENTINEL'}], 'links': []})
    registry = pin(base + 'final-verified/identity-registry.json', {'opaque': 'UNASSIGNED_TEXT_SENTINEL'})
    artifacts = [inv, registry]
    outputs = []
    for name in ['region-ledger.json', 'continuations.json', 'coverage-report.json', 'source-pins.json', 'toolchain.json']:
        body = {'opaque': 'UNASSIGNED_TEXT_SENTINEL'}
        if name == 'continuations.json': body['assigned_range_exit'] = {'physical_page': 12, 'observation': 'Synthetic exit.'}
        if name == 'toolchain.json': body.update(process_pythonpath='synthetic runtime', libraries={'pytest': 'synthetic'})
        old = pin(base + name, body); artifacts.append(old)
        if name in ['region-ledger.json', 'continuations.json']:
            new = pin('private/workflow/runs/IG-2B03/r01/' + name, body)
            artifacts.append(new); outputs.append(new['path'])
    artifacts.append(pin('private/unrelated/source.txt', {'opaque': 'UNRELATED_MANIFEST_SENTINEL'}))
    artifacts.append(pin('private/workflow/runs/IG-2B02/ancestor/final-verified/inventory.json',
                         {'opaque': 'UNRELATED_MANIFEST_SENTINEL'}))
    artifacts.append(pin('private/workflow/runs/IG-2B03/preparation/toolchain.json',
                         {'process_pythonpath': 'WRONG_ANCESTOR_RUNTIME'}))
    accepted = pin(base + 'review.json', {'artifacts': artifacts, 'summary': 'EVENT_HISTORY_SENTINEL'})
    done = pin(base + 'done.json', {'artifacts': artifacts, 'summary': 'EVENT_HISTORY_SENTINEL'})
    dep = {'id': 'IG-2B03', 'status': 'done', 'outputs': outputs,
           'events': [{'to': 'old_state', 'evidence': 'EVENT_HISTORY_SENTINEL'},
                      {'to': 'accepted', 'evidence': accepted['path'], 'sha256': accepted['sha256']},
                      {'to': 'done', 'evidence': done['path'], 'sha256': done['sha256']}]}
    task = {'id': 'IG-2B04', 'title': 'Inventory SPQR PDF pages 13-16', 'depends': ['IG-2B03']}
    q = {'tasks': [dep, task]}; dump(tmp_path / d.w.QUEUE, q)
    return tmp_path, q, task


def test_only_required_fields_and_assigned_metadata_are_projected(context):
    root, q, task = context
    view = d.build(root, q, task); text = json.dumps(view)
    assert all(x not in text for x in ['EXTRA_PIN_FIELD_SENTINEL', 'SOURCE_TEXT_SENTINEL', 'UNASSIGNED_TEXT_SENTINEL',
                                      'EVENT_HISTORY_SENTINEL', 'UNRELATED_MANIFEST_SENTINEL'])
    dep = view['dependencies']['IG-2B03']; inv = dep['inventory']
    assert inv['assigned_physical_pages'] == [13, 14, 15, 16]
    assert [x['id'] for x in inv['assigned_region_metadata']] == ['r13', 'r14', 'r15', 'r16']
    assert inv['reports']['continuations.json']['path'].endswith('/r01/continuations.json')
    assert dep['boundary'] == {'physical_page': 12, 'observation': 'Synthetic exit.'}
    assert dep['toolchain']['process_pythonpath'] == 'synthetic runtime'
    assert 'WRONG_ANCESTOR_RUNTIME' not in text
    assert 'artifacts' not in dep and 'events' not in dep['summary']
    assert len(text.encode()) < d.MAX_BYTES


def test_pdf_page_exit_is_projected_without_reading_retained_boundary(context):
    root, q, task = context
    dep = q['tasks'][0]
    done_path = root / dep['events'][-1]['evidence']
    done = d.w.read_json(done_path)
    report = next(p for p in done['artifacts'] if p['path'].endswith('/r01/continuations.json'))
    dump(root / report['path'], {
        'assigned_range_exit': {'pdf_page': 12, 'observation': 'Synthetic exit.',
                                'last_substantive_key': 'UNASSIGNED_TEXT_SENTINEL'},
        'retained_dependency_report': {'assigned_range_exit': {
            'physical_page': 8, 'observation': 'UNASSIGNED_TEXT_SENTINEL'}}})
    report['sha256'] = d.w.digest(root / report['path'])
    dump(done_path, done)
    dep['events'][-1]['sha256'] = d.w.digest(done_path)
    view = d.build(root, q, task)
    assert view['dependencies'][dep['id']]['boundary'] == {
        'physical_page': 12, 'observation': 'Synthetic exit.'}
    assert 'UNASSIGNED_TEXT_SENTINEL' not in json.dumps(view)


def test_accepted_native_versions_and_executable_records_share_one_projection(context):
    root, q, task = context
    dep = q['tasks'][0]
    done_path = root / dep['events'][-1]['evidence']
    done = d.w.read_json(done_path)
    report = next(p for p in done['artifacts'] if p['path'].endswith('/frozen/toolchain.json'))
    tool = d.w.read_json(root / report['path'])
    tool['native'] = {
        'git': 'git version synthetic\n',
        'pdfinfo': 'pdfinfo version synthetic\nCopyright synthetic',
        'pdftoppm': {'version': 'synthetic', 'executable': {
            'path': 'synthetic/pdftoppm.exe', 'sha256': 'synthetic', 'bytes': 42,
            'raw_text': 'EXTRA_PIN_FIELD_SENTINEL'}, 'events': ['EVENT_HISTORY_SENTINEL']},
        'unlisted': 'UNRELATED_MANIFEST_SENTINEL',
    }
    dump(root / report['path'], tool)
    report['sha256'] = d.w.digest(root / report['path'])
    dump(done_path, done)
    dep['events'][-1]['sha256'] = d.w.digest(done_path)
    view = d.build(root, q, task)
    native = view['dependencies'][dep['id']]['toolchain']['native']
    assert native == {
        'git': {'version': 'git version synthetic\n'},
        'pdfinfo': {'version': 'pdfinfo version synthetic\nCopyright synthetic'},
        'pdftoppm': {'version': 'synthetic', 'executable': {
            'path': 'synthetic/pdftoppm.exe', 'sha256': 'synthetic', 'bytes': 42}},
    }
    assert all(s not in json.dumps(view) for s in (
        'EXTRA_PIN_FIELD_SENTINEL', 'EVENT_HISTORY_SENTINEL', 'UNRELATED_MANIFEST_SENTINEL'))


@pytest.mark.parametrize('native', [None, [], 'version', {'git': 7}, {'git': None},
    {'git': {'version': 7}}, {'git': {'executable': 'unverified.exe'}},
    {'git': {'executable': {'path': 'unverified.exe'}}}])
def test_malformed_native_toolchain_stops_with_a_controlled_diagnostic(native):
    with pytest.raises(ValueError, match='[Nn]ative toolchain'):
        d.native_toolchain(native)


@pytest.mark.parametrize('boundary', [
    {'pdf_page': 11}, {'physical_page': 11},
    {'physical_page': 12, 'pdf_page': 11}, {'physical_page': 11, 'pdf_page': 12},
    {'pdf_page': '12'}, {'pdf_page': True}, {'observation': 'Missing ordinal.'},
])
def test_exit_boundary_rejects_wrong_conflicting_or_missing_ordinals(boundary):
    with pytest.raises(ValueError, match='assigned range boundary'):
        d.exit_boundary({'assigned_range_exit': boundary}, 12)


def test_exit_boundary_accepts_matching_aliases_and_absent_exit():
    assert d.exit_boundary({'assigned_range_exit': {'physical_page': 12, 'pdf_page': 12}}, 12) == {
        'physical_page': 12}
    assert d.exit_boundary({}, 12) == {}


@pytest.mark.parametrize('section', d.SECTIONS)
def test_pinned_view_supports_only_one_needed_section(context, section):
    root, q, task = context
    view = d.build(root, q, task); rel = 'private/view.json'; dump(root / rel, view)
    result = d.read_view(root, rel, d.w.digest(root / rel), task['id'], 'IG-2B03', section)
    assert result['data'] == view['dependencies']['IG-2B03'][section]
    assert set(result) == {'task', 'dependency', 'section', 'data'}


@pytest.mark.parametrize('section', ['events', 'artifacts', 'history', 'all'])
def test_no_full_history_manifest_or_arbitrary_field_mode(context, section):
    root, _, task = context
    with pytest.raises(ValueError, match='supported section'):
        d.read_view(root, 'private/view.json', 'irrelevant', task['id'], 'IG-2B03', section)


def test_missing_binding_unlisted_dependency_wrong_task_and_changed_view_are_rejected(context):
    root, q, task = context
    rel = 'private/view.json'; dump(root / rel, d.build(root, q, task)); sha = d.w.digest(root / rel)
    for manifest, digest, tid, dep in [(None, None, None, 'IG-2B03'), (rel, sha, task['id'], 'IG-2B02'),
                                      (rel, sha, 'IG-2B05', 'IG-2B03'), (rel, 'wrong', task['id'], 'IG-2B03')]:
        with pytest.raises(ValueError): d.read_view(root, manifest, digest, tid, dep, 'summary')


def test_live_dependency_change_and_artifact_tamper_fail_closed(context):
    root, q, task = context
    rel = 'private/view.json'; dump(root / rel, d.build(root, q, task)); sha = d.w.digest(root / rel)
    q['tasks'][0]['status'] = 'planned'; dump(root / d.w.QUEUE, q)
    with pytest.raises(ValueError, match='authority changed'):
        d.read_view(root, rel, sha, task['id'], 'IG-2B03', 'summary')
    q['tasks'][0]['status'] = 'done'; dump(root / d.w.QUEUE, q)
    p = root / q['tasks'][0]['events'][-1]['evidence']; p.write_text('{}', encoding='utf-8')
    with pytest.raises(ValueError, match='changed or is forbidden'):
        d.build(root, q, task)


def test_ambiguous_baseline_and_conflicting_page_scope_cannot_be_guessed(context):
    root, q, task = context
    task['dependency_scope'] = {'physical_pages': [12, 13, 14, 15]}
    with pytest.raises(ValueError, match='conflicts'): d.build(root, q, task)
    pins = [{'path': 'one/inventory.json'}, {'path': 'two/inventory.json'}]
    with pytest.raises(ValueError, match='Ambiguous'): d.choose(pins, [], 'inventory.json')


def test_oversized_projection_is_rejected_without_truncation(context):
    with pytest.raises(ValueError, match='byte ceiling'):
        d.bounded({'unexpected': 'x' * d.MAX_BYTES})


def test_cli_cannot_override_session_binding(context):
    root, _, _ = context
    env = dict(d.os.environ, WGC_TASK_ID='IG-2B04', WGC_TASK_DEPENDENCY_VIEW='private/view.json',
               WGC_TASK_DEPENDENCY_SHA256='synthetic')
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/dependency_context.py'),
        '--task', 'IG-2B05', '--dependency', 'IG-2B03'], cwd=root, env=env, capture_output=True, text=True)
    assert result.returncode == 2 and 'session binding' in result.stderr and result.stdout == ''
