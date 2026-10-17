"""Public reads, literal Git paths and refusal latching cannot expand a task packet."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    import task_access as a
    import orchestrate_ig2 as o
finally:
    sys.path.pop(0)


@pytest.fixture(autouse=True)
def isolate_live_guard(monkeypatch):
    monkeypatch.delenv('WGC_CONTEXT_GUARD', raising=False)
    monkeypatch.delenv('WGC_CONTEXT_GUARD_SHA256', raising=False)


def dump(p, body):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(body), encoding='utf-8')


@pytest.fixture
def access(tmp_path):
    for rel, text in [('scripts/allowed.py', 'ALLOWED\n' * 200),
                      ('scripts/outside.py', 'OUTSIDE_SENTINEL'),
                      ('private/workflow/runs/IG-2B04/current.txt', 'own'),
                      ('private/workflow/runs/IG-2B05/unrelated.txt', 'other')]:
        p = tmp_path / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')
    dump(tmp_path / 'docs/work/context-policy.json', {'allow': ['scripts/']})
    search = 'private/session/search-manifest.json'
    dump(tmp_path / search, {'format': a.search.FORMAT, 'task': 'IG-2B04', 'files': [
        {'path': 'scripts/allowed.py', 'sha256': a.w.digest(tmp_path / 'scripts/allowed.py')}]})
    rel = 'private/session/access-manifest.json'
    dump(tmp_path / rel, {'format': 'wgc-task-access-1', 'task': 'IG-2B04',
        'search_manifest': {'path': search, 'sha256': a.w.digest(tmp_path / search)},
        'git_paths': ['scripts/allowed.py', 'private/workflow/runs/IG-2B04/']})
    return tmp_path, rel, a.w.digest(tmp_path / rel)


def test_read_only_pinned_file_and_bounded_lines(access):
    root, rel, sha = access
    data = a.read_public(root, rel, sha, 'IG-2B04', 'scripts/allowed.py', start=2, lines=3)
    assert data['lines'] == ['ALLOWED'] * 3 and data['truncated']
    with pytest.raises(ValueError, match='not in'):
        a.read_public(root, rel, sha, 'IG-2B04', 'scripts/outside.py')


@pytest.mark.parametrize('file', ['docs/STATUS.md', 'docs/HANDOFF.md'])
def test_bootstrap_view_uses_frozen_snapshot_after_live_state_changes(access, file):
    root, rel, _ = access
    snapshot = 'private/session/bootstrap/' + Path(file).name
    p = root / snapshot; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('Dispatch navigation \u2192 task contract remains authoritative\n', encoding='utf-8')
    body = a.w.read_json(root / rel)
    body['bootstrap_reads'] = {file: {'path': snapshot, 'sha256': a.w.digest(p)}}
    dump(root / rel, body)
    live = root / file; live.parent.mkdir(parents=True, exist_ok=True)
    live.write_text('CHANGED_LIVE_VIEW_SENTINEL', encoding='utf-8')
    result = a.read_public(root, rel, a.w.digest(root / rel), 'IG-2B04', file)
    assert result['basis'] == 'dispatch_snapshot' and result['status_authority'] is False
    assert result['lines'] == ['Dispatch navigation \u2192 task contract remains authoritative']
    assert 'CHANGED_LIVE_VIEW_SENTINEL' not in json.dumps(result)
    assert not a.search.searchable(file)
    p.write_text('tampered', encoding='utf-8')
    with pytest.raises(ValueError, match='Bootstrap snapshot changed'):
        a.read_public(root, rel, a.w.digest(root / rel), 'IG-2B04', file)


@pytest.mark.parametrize('file,path', [('docs/STATUS.md', 'private/unrelated/source.txt'),
                                     ('scripts/outside.py', 'private/session/bootstrap/outside.py')])
def test_bootstrap_snapshot_cannot_expand_private_or_public_scope(access, file, path):
    root, rel, _ = access
    body = a.w.read_json(root / rel)
    body['bootstrap_reads'] = {file: {'path': path, 'sha256': '0' * 64}}
    dump(root / rel, body)
    with pytest.raises(ValueError, match='not an authorized session view'):
        a.read_public(root, rel, a.w.digest(root / rel), 'IG-2B04', file)


def test_public_read_budget_includes_unicode_json_escapes(access):
    root, rel, sha = access
    source = root / 'scripts/allowed.py'
    text = '\u2192\U0001f3b2' * 100
    source.write_text((text + '\n') * 100, encoding='utf-8')
    body = a.w.read_json(root / rel)
    search_rel = body['search_manifest']['path']
    search_body = a.w.read_json(root / search_rel)
    search_body['files'][0]['sha256'] = a.w.digest(source)
    dump(root / search_rel, search_body)
    body['search_manifest']['sha256'] = a.w.digest(root / search_rel)
    dump(root / rel, body)
    result = a.read_public(root, rel, a.w.digest(root / rel), 'IG-2B04', 'scripts/allowed.py')
    assert result['truncated'] and result['lines'][0] == text
    assert len(a.guard.json_text(result).encode('ascii')) + 1 <= 12000


def test_git_status_omits_unrelated_task_and_public_paths(access):
    root, rel, sha = access
    subprocess.run(['git', 'init', str(root)], check=True, capture_output=True)
    result = a.git_status(root, rel, sha, 'IG-2B04')
    assert {p['path'] for p in result['entries']} == {'scripts/allowed.py', 'private/workflow/runs/IG-2B04/current.txt'}
    assert 'unrelated' not in json.dumps(result) and 'outside.py' not in json.dumps(result)


def test_git_pathspec_is_literal_and_output_is_bounded(access):
    root, rel, _ = access
    subprocess.run(['git', 'init', str(root)], check=True, capture_output=True)
    for name in ['[literal].py', 'l.py']:
        (root / 'scripts' / name).write_text('synthetic', encoding='utf-8')
    body = a.w.read_json(root / rel); body['git_paths'] = ['scripts/[literal].py']
    dump(root / rel, body)
    result = a.git_status(root, rel, a.w.digest(root / rel), 'IG-2B04')
    assert [x['path'] for x in result['entries']] == ['scripts/[literal].py']
    body['git_paths'] = ['private/workflow/runs/IG-2B04/']; dump(root / rel, body)
    for n in range(6): (root / 'private/workflow/runs/IG-2B04' / f'{n}.txt').write_text('x')
    result = a.git_status(root, rel, a.w.digest(root / rel), 'IG-2B04', max_items=2)
    assert result['truncated'] and len(result['entries']) == 2


def test_empty_scope_and_unexpected_git_output_fail_closed(access, monkeypatch):
    root, rel, sha = access
    monkeypatch.setattr(a.subprocess, 'run', lambda *a, **kw: subprocess.CompletedProcess([], 0, b'?? private/other.txt\0', b''))
    with pytest.raises(ValueError, match='unlisted path'):
        a.git_status(root, rel, sha, 'IG-2B04')
    body = a.w.read_json(root / rel); body['git_paths'] = []; dump(root / rel, body)
    with pytest.raises(ValueError, match='never fall back'):
        a.git_status(root, rel, a.w.digest(root / rel), 'IG-2B04')


def validation_scope(access):
    root, rel, _ = access
    file = 'private/workflow/runs/IG-2B04/frozen/final-verified/inventory.json'
    p = root / file; p.parent.mkdir(parents=True); p.write_text('{}', encoding='utf-8')
    body = a.w.read_json(root / rel)
    body['source_validation'] = {'inputs': [{'path': file, 'sha256': a.w.digest(p)}],
        'log_root': 'private/workflow/runs/IG-2B04/review-validation-synthetic/'}
    dump(root / rel, body)
    return root, rel, a.w.digest(root / rel), file


@pytest.mark.parametrize('code', [0, 1])
def test_source_validation_never_releases_child_output_on_success_or_failure(access, monkeypatch, capsys, code):
    root, rel, sha, file = validation_scope(access)
    module = root / 'synthetic-module/wgc/sources'
    module.mkdir(parents=True)
    (module.parent / '__init__.py').write_text('', encoding='utf-8')
    (module / '__init__.py').write_text('', encoding='utf-8')
    stdout = 'UNASSIGNED_PAGE_METADATA_SENTINEL' * 300
    stderr = 'FAILURE_OUTPUT_SENTINEL' * 300
    (module / '__main__.py').write_text(
        f'import sys\nsys.stdout.write({stdout!r})\nsys.stderr.write({stderr!r})\nsys.exit({code})\n', encoding='utf-8')
    monkeypatch.setenv('PYTHONPATH', str(root / 'synthetic-module'))
    monkeypatch.setattr(a.w, 'ROOT', root)
    for key, value in [('WGC_TASK_ID', 'IG-2B04'), ('WGC_TASK_ACCESS_MANIFEST', rel),
                       ('WGC_TASK_ACCESS_SHA256', sha)]:
        monkeypatch.setenv(key, value)
    monkeypatch.setattr(sys, 'argv', ['task_access.py', 'validate-source', '--file', file])
    assert a.guard.cli(root, 'task_access', a.main) == code
    emitted = capsys.readouterr()
    summary = json.loads(emitted.out)
    assert summary['exit_code'] == code
    assert summary['command'] == [sys.executable, '-m', 'wgc.sources', 'validate', file]
    assert 'SENTINEL' not in emitted.out + emitted.err
    assert (root / summary['stdout']['path']).read_text() == stdout
    assert (root / summary['stderr']['path']).read_text() == stderr
    assert a.w.digest(root / summary['stdout']['path']) == summary['stdout']['sha256']
    assert a.w.digest(root / summary['stderr']['path']) == summary['stderr']['sha256']
    assert json.loads((root / summary['stdout']['path']).with_name('result.json').read_text()) == summary
    assert (root / file).read_text() == '{}'


@pytest.mark.parametrize('fault', ['unlisted', 'input_changed', 'manifest_changed', 'escape', 'wrong_task_root'])
def test_source_validation_refuses_unpinned_input_and_log_scope_before_launch(access, monkeypatch, fault):
    root, rel, sha, file = validation_scope(access)
    if fault == 'unlisted': file = 'private/other/inventory.json'
    if fault == 'input_changed': (root / file).write_text('tampered', encoding='utf-8')
    if fault == 'manifest_changed': sha = 'wrong'
    if fault in {'escape', 'wrong_task_root'}:
        body = a.w.read_json(root / rel)
        body['source_validation']['log_root'] = (
            'private/workflow/runs/IG-2B04/review-validation-test/../../escape/' if fault == 'escape'
            else 'private/workflow/runs/IG-2B05/review-validation-test/')
        dump(root / rel, body); sha = a.w.digest(root / rel)
    monkeypatch.setattr(a.subprocess, 'run', lambda *a, **kw: pytest.fail('Refusal must precede process launch'))
    with pytest.raises(ValueError):
        a.validate_source(root, rel, sha, 'IG-2B04', file)


def owned_validation(access):
    root, rel, _, file = validation_scope(access)
    attempt = file.partition('final-verified/')[0]
    session = (root / rel).parent
    dump(session / 'runtime-configuration.json', {'status': 'confirmed', 'model': 'gpt-6.1-sol',
          'reasoning': 'high', 'session_id': 'synthetic-executor'})
    claim = {'actor': 'ig2:session:executor', 'model': 'gpt-6.1-sol', 'reasoning': 'high',
          'configuration_evidence': (session / 'runtime-configuration.json').relative_to(root).as_posix(),
          'configuration_sha256': a.w.digest(session / 'runtime-configuration.json')}
    dump(root / attempt / 'claim.json', claim)
    dump(root / a.w.QUEUE, {'tasks': [{'id': 'IG-2B04', 'status': 'in_progress', 'write_scope': [attempt],
        'inventory_contract': {'attempt_root': attempt.rstrip('/')}, 'events': [{'to': 'in_progress',
        'evidence': attempt + 'claim.json', 'sha256': a.w.digest(root / attempt / 'claim.json')}]}]})
    body = a.w.read_json(root / rel)
    body['source_validation'].update(mode='owned_attempt', attempt=attempt,
        inputs=[{'path': attempt + name + '/inventory.json'} for name in ('final-verified', 'replay-1', 'replay-2')])
    dump(root / rel, body)
    return root, rel, a.w.digest(root / rel), file


def test_executor_validation_snapshots_generated_output_after_observed_claim(access, monkeypatch):
    root, rel, sha, file = owned_validation(access)
    # The output may be generated after dispatch; it is not a frozen reviewer pin.
    (root / file).write_text('{"freshly_generated":true}', encoding='utf-8')
    def validate(argv, **kw):
        kw['stdout'].write(b'UNASSIGNED_SENTINEL')
        return subprocess.CompletedProcess(argv, 0)
    monkeypatch.setattr(a.subprocess, 'run', validate)
    summary = a.validate_source(root, rel, sha, 'IG-2B04', file)
    assert summary['exit_code'] == 0
    assert summary['inventory']['sha256'] == a.w.digest(root / file)
    assert 'UNASSIGNED_SENTINEL' not in json.dumps(summary)
    assert (root / summary['stdout']['path']).read_bytes() == b'UNASSIGNED_SENTINEL'


@pytest.mark.parametrize('fault', ['stale_owner', 'other_runtime', 'unconfirmed', 'other_attempt', 'foreign_path'])
def test_executor_validation_cannot_reuse_another_claim_or_widen_output_scope(access, monkeypatch, fault):
    root, rel, sha, file = owned_validation(access)
    q = a.w.read_json(root / a.w.QUEUE)
    if fault == 'stale_owner': q['tasks'][0]['status'] = 'review'
    if fault == 'other_attempt': q['tasks'][0]['write_scope'] = ['private/workflow/runs/IG-2B04/other/']
    if fault in {'other_runtime', 'unconfirmed'}:
        runtime = (root / rel).with_name('runtime-configuration.json')
        data = a.w.read_json(runtime)
        if fault == 'other_runtime': data['session_id'] = 'another-session'
        else: data['status'] = 'pending'
        dump(runtime, data)
    if fault == 'foreign_path': file = 'private/workflow/runs/IG-2B04/prior/final-verified/inventory.json'
    dump(root / a.w.QUEUE, q)
    monkeypatch.setattr(a.subprocess, 'run', lambda *a, **kw: pytest.fail('Invalid ownership must precede validation'))
    with pytest.raises(ValueError):
        a.validate_source(root, rel, sha, 'IG-2B04', file)


@pytest.mark.parametrize('helper,fault', [
    ('read', None), ('search', None), ('dependency', None), ('status', None), ('validate', None),
    ('read', 'digest'), ('read', 'json'), ('read', 'type'), ('read', 'open'), ('read', 'replace'),
    ('read', 'all_writes'),
])
def test_supervisor_stops_denied_request_before_direct_read_fallback(access, monkeypatch, helper, fault):
    root, rel, sha = access
    session = root / 'private/session'
    guard = session / 'context-guard.json'
    dump(guard, {'format': 'wgc-context-guard-1', 'task': 'IG-2B04', 'denial': 'private/session/context-denied.json'})
    inner = f'''import sys
from pathlib import Path
sys.path.insert(0, {str(ROOT / 'scripts')!r})
import task_access as a
import dependency_context as d
import context_guard as g
root=Path({str(root)!r})
fault={fault!r}
if fault=='digest':
    g.os.environ['WGC_CONTEXT_GUARD_SHA256']='wrong'
if fault in ('json','type'):
    original_json=g.w.read_json
    def bad_json(p):
        if p.name=='context-guard.json':
            if fault=='type': return []
            raise ValueError('Malformed synthetic guard JSON')
        return original_json(p)
    g.w.read_json=bad_json
if fault in ('open','all_writes'):
    original_open=Path.open
    def bad_open(p,*args,**kwargs):
        if p.name.endswith('.pending'): raise PermissionError('Synthetic marker open failure')
        return original_open(p,*args,**kwargs)
    Path.open=bad_open
if fault=='replace':
    def bad_replace(*args): raise PermissionError('Synthetic marker replace failure')
    g.os.replace=bad_replace
if fault=='all_writes':
    def bad_os_open(*args): raise PermissionError('Synthetic fallback marker open failure')
    g.os.open=bad_os_open
kind={helper!r}
if kind=='read': a.read_public(root,{rel!r},{sha!r},'IG-2B04','scripts/outside.py')
elif kind=='search': a.search.search(root,'private/session/search-manifest.json',a.w.digest(root/'private/session/search-manifest.json'),'IG-2B04','SENTINEL',['scripts/outside.py'])
elif kind=='dependency': d.read_view(root,None,None,'IG-2B04','UNLISTED','summary')
elif kind=='validate': a.validate_source(root,{rel!r},{sha!r},'IG-2B04','private/unlisted/inventory.json')
else: a.git_status(root,{rel!r},'wrong','IG-2B04')
'''
    fake = root / 'fake_cli.py'
    fake.write_text(f'''import sys
from pathlib import Path
print('model: gpt-6.1-sol\\nreasoning effort: high\\nsession id: synthetic-denial\\nuser',file=sys.stderr,flush=True)
sys.stdin.read()
exec({inner!r})
Path({str(root / 'fallback.txt')!r}).write_text(Path({str(root / 'scripts/outside.py')!r}).read_text())
''', encoding='utf-8')
    monkeypatch.setattr(o, 'command', lambda *a: [sys.executable, str(fake)])
    env = dict(os.environ, WGC_TASK_ID='IG-2B04', WGC_CONTEXT_GUARD='private/session/context-guard.json',
               WGC_CONTEXT_GUARD_SHA256=a.w.digest(guard))
    with pytest.raises(ValueError, match='Context helper denied'):
        o.launch('unused', root, session, 'Synthetic request; no model is launched.', 8, env)
    assert (session / 'context-denied.json').is_file() is (fault != 'all_writes')
    assert not (root / 'fallback.txt').exists()
    result = a.w.read_json(session / 'process-result.json')
    assert result['exit_code'] != 0
