"""Synthetic supervisor checks: no model, source corpus or external service calls."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import time

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    spec = importlib.util.spec_from_file_location('ig2_supervisor', ROOT / 'scripts/orchestrate_ig2.py')
    o = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(o)
finally:
    sys.path.pop(0)


def task(id='IG-2C', status='ready', depends=None):
    return {'id': id, 'stage': 'IG-2', 'status': status, 'kind': 'implementation',
            'depends': depends or [], 'events': [], 'context': [], 'acceptance': ['Exact synthetic criterion'],
            'semantic_acceptance_required': False}


def queue(*tasks):
    return {'tasks': list(tasks)}


def complete_task():
    return task('IG-2D', 'done')


@pytest.mark.parametrize('winerror', [5, 32, 33])
def test_atomic_status_retries_same_complete_candidate_without_touching_old_file(tmp_path, monkeypatch, winerror):
    path = tmp_path / 'process.json'
    path.write_text('{"state": "old"}', encoding='utf-8')
    original_replace = o.os.replace
    candidates, pauses = [], []
    def replace(src, dst):
        candidates.append((src, Path(src).read_bytes()))
        assert json.loads(path.read_text()) == {'state': 'old'}
        if len(candidates) < 3:
            error = PermissionError('Synthetic Windows sharing denial')
            error.winerror = winerror
            raise error
        original_replace(src, dst)
    monkeypatch.setattr(o.os, 'replace', replace)
    monkeypatch.setattr(o.time, 'sleep', pauses.append)
    o.dump(path, {'state': 'new'})
    assert len(candidates) == 3 and candidates[0] == candidates[1] == candidates[2]
    assert pauses == [0.05, 0.1]
    assert json.loads(path.read_text()) == {'state': 'new'}
    assert not list(tmp_path.glob('*.pending'))


@pytest.mark.parametrize('winerror,calls', [(5, 3), (None, 1)])
def test_atomic_status_permanent_denial_is_bounded_and_preserves_old_bytes(tmp_path, monkeypatch, winerror, calls):
    path = tmp_path / 'process.json'
    old = b'{"state":"old"}\n'
    path.write_bytes(old)
    attempts = []
    def denied(src, dst):
        attempts.append(src)
        error = PermissionError('Synthetic permanent denial')
        if winerror is not None:
            error.winerror = winerror
        raise error
    monkeypatch.setattr(o.os, 'replace', denied)
    monkeypatch.setattr(o.time, 'sleep', lambda seconds: None)
    with pytest.raises(PermissionError, match='permanent denial'):
        o.dump(path, {'state': 'new'})
    assert len(attempts) == calls and path.read_bytes() == old
    pending = list(tmp_path.glob('*.pending'))
    assert len(pending) == 1 and json.loads(pending[0].read_text()) == {'state': 'new'}


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows destination sharing handle')
def test_atomic_status_recovers_after_real_windows_reader_releases_handle(tmp_path, monkeypatch):
    import ctypes
    from ctypes import wintypes
    path = tmp_path / 'process.json'
    path.write_text('{"state":"old"}', encoding='utf-8')
    api = ctypes.WinDLL('kernel32', use_last_error=True)
    api.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
        ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    api.CreateFileW.restype = wintypes.HANDLE
    api.CloseHandle.argtypes = [wintypes.HANDLE]
    api.CloseHandle.restype = wintypes.BOOL
    # Permit reads/writes but hold DELETE sharing, which blocks atomic replace.
    handle = api.CreateFileW(str(path), 0x80000000, 3, None, 3, 0x80, None)
    assert handle != ctypes.c_void_p(-1).value
    pauses = []
    def release(seconds):
        nonlocal handle
        assert json.loads(path.read_text()) == {'state': 'old'}
        pauses.append(seconds)
        assert api.CloseHandle(handle)
        handle = None
    monkeypatch.setattr(o.time, 'sleep', release)
    try:
        o.dump(path, {'state': 'new'})
        assert pauses == [0.05]
        assert json.loads(path.read_text()) == {'state': 'new'}
    finally:
        if handle is not None:
            api.CloseHandle(handle)


def test_select_prioritizes_pending_review_over_next_batch():
    t = task(status='review')
    picked, role = o.select(queue(t, complete_task(), task('IG-2D-A01')))
    assert picked is t and role == 'reviewer'


def continuation_inputs(root, preservation_name='blocked-state-manifest.json'):
    t = task('IG-2B03')
    t['tests'] = ['Synthetic required check']
    old = 'private/workflow/runs/IG-2B03/blocked/'
    prep = 'private/workflow/runs/IG-2B03/recovery/'
    new = 'private/workflow/runs/IG-2B03/fresh/'
    def pin(rel, body):
        o.dump(root / rel, body)
        return {'path': rel, 'sha256': o.w.digest(root / rel)}
    draft = pin(old + 'draft.json', {'unaccepted': True})
    manifest = pin(old + preservation_name, {'artifacts': [draft]})
    blocked = pin(old + 'blocked.json', {'artifacts': [manifest]})
    preserve = pin(prep + 'preserve.json', {'artifacts': [draft, manifest, blocked]})
    scope = pin(prep + 'scope.json', {'mode': 'draft_revalidation', 'blocked_attempt': old,
        'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256'],
        'attempt': new, 'acceptance': t['acceptance'], 'tests': t['tests'],
        'drafts': [draft], 'preserve_manifest': preserve})
    evidence = pin(prep + 'authorization.json', {'operator_requested_recovery': True})
    t.update(write_scope=[new], events=[{'to': 'blocked', 'evidence': blocked['path'],
                                     'sha256': blocked['sha256']}, {'to': 'planned'}, {'to': 'ready'}],
             continuation_authorization={'scope': scope, 'evidence': evidence, 'attempt': new,
                 'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256']})
    return t


def update_continuation_scope(root, t, change):
    pin = t['continuation_authorization']['scope']
    scope = o.w.read_json(root / pin['path'])
    change(scope)
    o.dump(root / pin['path'], scope)
    pin['sha256'] = o.w.digest(root / pin['path'])


@pytest.mark.parametrize('preservation_name', ['blocked-state-manifest.json', 'blocked-attempt-preservation.json'])
def test_continuation_requires_fresh_root_and_preserves_blocked_attempt(tmp_path, preservation_name):
    t = continuation_inputs(tmp_path, preservation_name)
    assert len(o.continuation_preservation(tmp_path, t, require_absent=True)) == 3
    (tmp_path / t['continuation_authorization']['attempt']).mkdir()
    with pytest.raises(ValueError, match='already exists'):
        o.continuation_preservation(tmp_path, t, require_absent=True)
    assert len(o.continuation_preservation(tmp_path, t)) == 3  # Review/restart still checks preservation.
    o.dump(tmp_path / 'private/workflow/runs/IG-2B03/blocked/draft.json', {'changed': True})
    with pytest.raises(ValueError, match='Frozen artifact'):
        o.continuation_preservation(tmp_path, t)


@pytest.mark.parametrize('kind', ['incident', 'old_attempt', 'draft', 'gates', 'reuse'])
def test_continuation_cannot_expand_or_replace_its_authority(tmp_path, kind):
    t = continuation_inputs(tmp_path)
    def change(scope):
        if kind == 'incident': scope['blocked_sha256'] = 'wrong'
        if kind == 'old_attempt': scope['blocked_attempt'] = 'private/workflow/runs/IG-2B03/other/'
        if kind == 'draft': scope['drafts'] = [{'path': 'private/outside.json', 'sha256': 'wrong'}]
        if kind == 'gates': scope['tests'] = []
        if kind == 'reuse':
            scope['attempt'] = scope['blocked_attempt']
            t['continuation_authorization']['attempt'] = scope['attempt']
            t['write_scope'] = [scope['attempt']]
    update_continuation_scope(tmp_path, t, change)
    with pytest.raises(ValueError):
        o.continuation_preservation(tmp_path, t, require_absent=True)


@pytest.mark.parametrize('tamper_hash', [False, True])
def test_continuation_event_reference_accepts_extra_metadata_but_requires_same_hash(tmp_path, tamper_hash):
    t = continuation_inputs(tmp_path)
    def change(scope):
        pin = scope['preserve_manifest']
        body = o.w.read_json(tmp_path / pin['path'])
        row = body['artifacts'][-1]
        row['bytes'] = (tmp_path / row['path']).stat().st_size
        if tamper_hash: row['sha256'] = 'wrong'
        o.dump(tmp_path / pin['path'], body)
        pin['sha256'] = o.w.digest(tmp_path / pin['path'])
    update_continuation_scope(tmp_path, t, change)
    if tamper_hash:
        with pytest.raises(ValueError): o.continuation_preservation(tmp_path, t)
    else:
        preserved = o.continuation_preservation(tmp_path, t)
        assert preserved[-1]['bytes'] > 0


def test_continuation_cannot_omit_original_even_with_rehashed_scope(tmp_path):
    t = continuation_inputs(tmp_path)
    def change(scope):
        pin = scope['preserve_manifest']
        body = o.w.read_json(tmp_path / pin['path'])
        body['artifacts'].pop(0)
        o.dump(tmp_path / pin['path'], body)
        pin['sha256'] = o.w.digest(tmp_path / pin['path'])
    update_continuation_scope(tmp_path, t, change)
    with pytest.raises(ValueError, match='omitted or changed original'):
        o.continuation_preservation(tmp_path, t)


def reviewed_continuation_inputs(root):
    t = continuation_inputs(root)
    old = t['continuation_authorization']['attempt']
    prep = 'private/workflow/runs/IG-2B03/r01-prep/'
    new = 'private/workflow/runs/IG-2B03/r01/'
    def pin(rel, body):
        o.dump(root / rel, body)
        return {'path': rel, 'sha256': o.w.digest(root / rel)}
    report = pin(old + 'report.json', {'frozen': True})
    delivery = pin(old + 'delivery.json', {'artifacts': [report]})
    finding = pin(prep + 'review.json', {'findings': [{'id': 'R01'}]})
    scope = pin(prep + 'scope.json', {'review_evidence': finding['path'],
        'review_sha256': finding['sha256'], 'attempt': new, 'finding_ids': ['R01'],
        'acceptance': t['acceptance'], 'tests': t['tests'], 'immutable_delivery': delivery,
        'mode': 'reference_index_repair'})
    authority = pin(prep + 'authorization.json', {'authorized': True})
    t['events'] += [{'to': 'review', 'evidence': delivery['path'], 'sha256': delivery['sha256']},
                    {'to': 'changes_requested', 'evidence': finding['path'], 'sha256': finding['sha256']}]
    t.update(status='changes_requested', write_scope=[new], repair_authorization={
        'review_evidence': finding['path'], 'review_sha256': finding['sha256'],
        'scope': scope, 'evidence': authority, 'attempt': new})
    return t, report, delivery


@pytest.mark.parametrize('phase', ['repair_ready', 'repair_review', 'new_finding'])
def test_frozen_continuation_survives_repair_handoff_review_and_restart(tmp_path, phase):
    t, report, delivery = reviewed_continuation_inputs(tmp_path)
    assert o.verify_repair_authorization(tmp_path, t)['finding_ids'] == ['R01']
    if phase != 'repair_ready':
        new = t['repair_authorization']['attempt']
        o.dump(tmp_path / (new + 'delivery.json'), {'artifacts': [report]})
        t['events'].append({'to': 'review', 'evidence': new + 'delivery.json',
                            'sha256': o.w.digest(tmp_path / (new + 'delivery.json'))})
        t['status'] = 'review'
        if phase == 'new_finding':
            o.dump(tmp_path / (new + 'finding.json'), {'findings': [{'id': 'R02'}]})
            t['events'].append({'to': 'changes_requested', 'evidence': new + 'finding.json',
                                'sha256': o.w.digest(tmp_path / (new + 'finding.json'))})
            t['status'] = 'changes_requested'
            assert not o.repair_authorized(t)  # Coordinator must refine the new finding.
    snapshot = o.continuation_preservation(tmp_path, t)
    assert report in snapshot and delivery in snapshot and len(snapshot) == 5
    # The existing run() post-role snapshot check must protect this frozen report too.
    o.dump(tmp_path / report['path'], {'tampered': True})
    with pytest.raises(ValueError, match='Frozen artifact'):
        o.verify_artifacts(tmp_path, {'artifacts': snapshot})
    with pytest.raises(ValueError, match='Frozen artifact'):
        o.continuation_preservation(tmp_path, t)


@pytest.mark.parametrize('defect', ['missing_authority', 'stale_review', 'no_delivery', 'changed_scope'])
def test_continuation_ownership_cannot_move_without_verified_review_repair(tmp_path, defect):
    t, _, _ = reviewed_continuation_inputs(tmp_path)
    if defect == 'missing_authority': t.pop('repair_authorization')
    if defect == 'stale_review': t['repair_authorization']['review_sha256'] = 'wrong'
    if defect == 'no_delivery': t['events'].pop(-2)
    if defect == 'changed_scope':
        p = tmp_path / t['repair_authorization']['scope']['path']
        o.dump(p, {'changed': True})
    with pytest.raises((ValueError, StopIteration)):
        o.continuation_preservation(tmp_path, t)


def test_repair_handoff_keeps_fresh_claim_and_initial_ownership_gates(tmp_path):
    t, _, _ = reviewed_continuation_inputs(tmp_path)
    with pytest.raises(ValueError, match='Initial continuation requires exact'):
        o.continuation_preservation(tmp_path, t, require_absent=True)
    (tmp_path / t['repair_authorization']['attempt']).mkdir()
    assert o.continuation_preservation(tmp_path, t)
    with pytest.raises(ValueError, match='already exists'):
        o.verify_repair_authorization(tmp_path, t)


def test_completion_includes_dynamic_children():
    c = task(status='done')
    d = complete_task()
    assert o.select(queue(c, d)) == (None, 'complete')
    child = task('IG-2D-A01')
    assert o.select(queue(c, d, child)) == (child, 'executor')


@pytest.mark.parametrize('state', ['in_progress', 'accepted'])
def test_abandoned_ownership_is_not_silently_taken(state):
    with pytest.raises(ValueError, match='triage'):
        o.select(queue(task(status=state), complete_task()))


def test_outside_stage_writer_blocks_even_when_ig2_has_ready_work():
    other = dict(task('IG-3A', 'review'), stage='IG-3')
    with pytest.raises(ValueError, match='Another stage'):
        o.select(queue(task(), complete_task(), other))


def test_blocker_is_not_automatically_retried_or_promoted():
    with pytest.raises(ValueError, match='No eligible'):
        o.select(queue(task(status='blocked'), task('IG-2D', 'planned', ['IG-2C'])))


def test_refinement_waits_for_all_dependencies():
    c = task(status='planned')
    c['kind'] = 'refine'
    d = task('IG-2D', 'planned', ['IG-2C'])
    assert o.select(queue(c, d)) == (c, 'coordinator')


def test_requested_or_model_echoed_settings_are_not_startup_evidence():
    assert o.parse_startup(['requested model: gpt-6.1-sol', 'user', 'model: gpt-6.1-sol',
                            'reasoning effort: high']) == {}
    assert o.parse_startup(['model: gpt-6.1-sol', 'reasoning effort: high', 'session id: unique',
                            'user', 'model: wrong']) == {
                                'model': o.MODEL, 'reasoning': 'high', 'session_id': 'unique'}


def test_frozen_delivery_tamper_and_path_escape_rejected(tmp_path):
    artifact = tmp_path / 'synthetic.txt'
    artifact.write_text('source-independent fixture', encoding='utf-8')
    evidence = {'artifacts': [{'path': 'synthetic.txt', 'sha256': o.w.digest(artifact)}]}
    o.verify_artifacts(tmp_path, evidence)
    artifact.write_text('tampered', encoding='utf-8')
    with pytest.raises(ValueError, match='Frozen artifact'):
        o.verify_artifacts(tmp_path, evidence)
    evidence['artifacts'][0]['path'] = '../escape'
    with pytest.raises(ValueError, match='Unsafe'):
        o.verify_artifacts(tmp_path, evidence)


def test_fresh_process_arguments_do_not_resume_or_bypass_sandbox(tmp_path):
    argv = o.command('codex', tmp_path, tmp_path / 'session')
    assert '--ephemeral' in argv and '--approve-for-me' in argv
    assert '-s' not in argv and '--sandbox' not in argv  # Mutually exclusive CLI switches.
    assert 'resume' not in argv and 'fork' not in argv
    assert not any('dangerously' in part or part == '--ignore-rules' for part in argv)
    assert argv[argv.index('-m') + 1] == o.MODEL


@pytest.mark.parametrize('model,reasoning,success', [
    ('gpt-6.1-sol', 'high', True), ('gpt-6.1-sol', 'low', False), ('unknown', 'high', False)])
def test_local_fake_cli_observed_config_gate(tmp_path, monkeypatch, model, reasoning, success):
    session = tmp_path / 'session'
    session.mkdir()
    fake = tmp_path / 'fake_cli.py'
    fake.write_text('''import json, sys
from pathlib import Path
print('model: ' + sys.argv[2], file=sys.stderr, flush=True)
print('reasoning effort: ' + sys.argv[3], file=sys.stderr, flush=True)
print('session id: synthetic-local-process', file=sys.stderr, flush=True)
print('user', file=sys.stderr, flush=True)
sys.stdin.read()
Path(sys.argv[1]).write_text(json.dumps({'outcome':'progress','evidence':None,'summary':'synthetic'}))
''', encoding='utf-8')
    monkeypatch.setattr(o, 'command', lambda cli, root, path: [sys.executable, str(fake),
                         str(path / 'response.json'), model, reasoning])
    if success:
        assert o.launch('unused', tmp_path, session, 'Synthetic prompt', 5)['outcome'] == 'progress'
    else:
        with pytest.raises(ValueError):
            o.launch('unused', tmp_path, session, 'Synthetic prompt', 5)
    config = o.w.read_json(session / 'runtime-configuration.json')
    assert (config['status'] == 'confirmed') == success
    assert config['basis'].startswith('Observed CLI')
    process = o.w.read_json(session / 'process.json')
    assert process['pid'] > 0 and process['supervisor_pid'] == o.os.getpid()
    assert process['state'] == 'exited' and process['ended_utc']


def review_inputs(tmp_path, outcome='pass'):
    for rel in ['README.md', 'docs/work/WORKFLOW.md',
                'scripts/workflow.py', 'scripts/check.ps1', 'scripts/search_task.py', 'scripts/dependency_context.py',
                'scripts/context_guard.py', 'scripts/task_access.py',
                'scripts/orchestrate_ig2.py', 'docs/skills/wgc-execute/SKILL.md',
                'docs/skills/wgc-review/SKILL.md', 'docs/skills/wgc-queue/SKILL.md']:
        path = tmp_path / rel; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Synthetic task control context\n', encoding='utf-8')
    o.dump(tmp_path / 'docs/work/context-policy.json', {
        'allow': ['README.md', 'docs/work/WORKFLOW.md', 'scripts/', 'docs/skills/']})
    t = task(status='review')
    t['events'] = [{'to': 'review', 'evidence': 'delivery.json'}]
    artifact = tmp_path / 'synthetic.txt'
    artifact.write_text('unchanged', encoding='utf-8')
    delivery = {'actor': 'executor', 'artifacts': [{'path': 'synthetic.txt', 'sha256': o.w.digest(artifact)}]}
    o.dump(tmp_path / 'delivery.json', delivery)
    t['events'][0]['sha256'] = o.w.digest(tmp_path / 'delivery.json')
    session = tmp_path / 'session'; session.mkdir()
    config = session / 'runtime-configuration.json'
    o.dump(config, {'status': 'confirmed', 'model': o.MODEL, 'reasoning': o.REASONING,
                    'session_id': 'synthetic'})
    review = {'role': 'reviewer', 'actor': 'ig2:session:reviewer', 'model': o.MODEL,
              'reasoning': o.REASONING, 'criteria': t['acceptance'], 'artifacts': delivery['artifacts'],
              'configuration_evidence': config.relative_to(tmp_path).as_posix(),
              'configuration_sha256': o.w.digest(config), 'summary': 'synthetic',
              'checks': [{'command': 'synthetic', 'exit_code': 0}]}
    rel = 'private/workflow/runs/IG-2C/review/review.json'
    o.dump(tmp_path / rel, review)
    return t, session, review, rel, {'outcome': outcome, 'evidence': rel, 'summary': 'synthetic'}


def test_human_gate_stops_before_any_transition(tmp_path, monkeypatch):
    t, session, _, _, result = review_inputs(tmp_path)
    t['semantic_acceptance_required'] = True
    monkeypatch.setattr(o, 'apply_transition', lambda *args: pytest.fail('No automatic human acceptance'))
    with pytest.raises(ValueError, match='Human semantic decision'):
        o.finish_review(tmp_path, t, result, session)


@pytest.mark.parametrize('role', ['executor', 'reviewer'])
def test_role_validation_scope_contains_only_current_final_and_complete_replays(tmp_path, monkeypatch, role):
    t, _, _, _, _ = review_inputs(tmp_path)
    root = 'private/workflow/runs/IG-2C/current'
    t['inventory_contract'] = {'attempt_root': root}
    t['write_scope'] = [root + '/']
    if role == 'executor': t['status'] = 'ready'
    delivery = o.w.read_json(tmp_path / 'delivery.json')
    paths = [root + '/' + name + '/inventory.json' for name in ('final-verified', 'replay-1', 'replay-2')]
    for path in paths + ['private/workflow/runs/IG-2C/prior/final-verified/inventory.json']:
        o.dump(tmp_path / path, {'synthetic': True})
        delivery['artifacts'].append({'path': path, 'sha256': o.w.digest(tmp_path / path)})
    o.dump(tmp_path / 'delivery.json', delivery)
    t['events'][0]['sha256'] = o.w.digest(tmp_path / 'delivery.json')
    monkeypatch.setattr(o.w, 'packet', lambda *a, **kw: {'files': []})
    monkeypatch.setattr(o.dep_context, 'build', lambda *a: {})
    session = tmp_path / 'fresh-review'; session.mkdir()
    o.prepare(tmp_path, queue(t), t, role, session)
    scope = o.w.read_json(session / 'access-manifest.json')['source_validation']
    assert [p['path'] for p in scope['inputs']] == paths
    assert scope['mode'] == ('frozen' if role == 'reviewer' else 'owned_attempt')
    assert all(('sha256' in p) == (role == 'reviewer') for p in scope['inputs'])
    assert scope['log_root'] == 'private/workflow/runs/IG-2C/review-validation-fresh-review/'
    text = o.prompt(tmp_path, t, role, session)
    assert 'task_access.py validate-source' in text and 'No generic last-N-character/line preview' in text


@pytest.mark.parametrize('fault,preparations,launches', [
    ('transient', 3, 1), ('persistent', 3, 0), ('queue_changed', 1, 0), ('other_error', 1, 0)])
def test_pre_model_io_recovery_is_bounded_fresh_and_preserves_ownership(tmp_path, monkeypatch, fault, preparations, launches):
    t = task(); q = queue(t, complete_task())
    o.dump(tmp_path / o.w.QUEUE, q)
    monkeypatch.setattr(o.w, 'validate', lambda *a: None)
    seen, started = [], []
    def prepare(root, q, task, role, session):
        seen.append(session)
        if fault == 'transient' and len(seen) == 3: return
        if fault == 'queue_changed':
            altered = copy.deepcopy(q); altered['tasks'][0]['goal'] = 'another writer'
            o.dump(tmp_path / o.w.QUEUE, altered)
        error = PermissionError('Synthetic pre-model file lock')
        if fault != 'other_error': error.winerror = 32
        raise error
    monkeypatch.setattr(o, 'prepare', prepare)
    monkeypatch.setattr(o, 'launch_environment', lambda *a: {})
    monkeypatch.setattr(o, 'prompt', lambda *a: 'synthetic')
    def launch(*args):
        started.append(True)
        return {'outcome': 'blocked', 'summary': 'Synthetic final role stop', 'evidence': None}
    monkeypatch.setattr(o, 'launch', launch)
    assert o.run(tmp_path, 'unused', tmp_path / 'run', 4, 5, 20) == 2
    assert len(seen) == preparations and len(set(seen)) == preparations
    assert len(started) == launches
    assert len(list((tmp_path / 'run').glob('*/preparation-retry.json'))) == (2 if preparations == 3 else 0)


def test_self_review_and_incomplete_manifest_cannot_be_accepted(tmp_path):
    t, session, review, rel, result = review_inputs(tmp_path)
    review['actor'] = 'executor'; o.dump(tmp_path / rel, review)
    with pytest.raises(ValueError, match='identity'):
        o.finish_review(tmp_path, t, result, session)
    review['actor'] = 'ig2:session:reviewer'; review['artifacts'] = []; o.dump(tmp_path / rel, review)
    with pytest.raises(ValueError, match='entire delivery'):
        o.finish_review(tmp_path, t, result, session)


def test_validation_recovery_reuses_independent_review_and_preserves_old_logs(tmp_path, monkeypatch):
    t, session, review, rel, result = review_inputs(tmp_path)
    o.dump(session / 'supervisor-checks.json', [{'exit_code': 1}])
    (session / 'project-check.log').write_text('Previous failed check\n', encoding='utf-8')
    before = {p.name: p.read_bytes() for p in session.iterdir() if p.is_file()}
    fresh = tmp_path / 'private/workflow/runs/IG-2C/validation-recovery'
    transitions = []
    def check(argv, root, log_path, deadline, env=None):
        assert log_path.parent == fresh
        log_path.write_text('Fresh unchanged check passed\n', encoding='utf-8')
        return 0
    monkeypatch.setattr(o, 'run_check', check)
    monkeypatch.setattr(o, 'apply_transition', lambda root, id, state, evidence, deadline: transitions.append(state))
    o.finish_review(tmp_path, t, result, session, validation_session=fresh)
    assert transitions == ['accepted', 'done']
    assert {p.name: p.read_bytes() for p in session.iterdir() if p.is_file()} == before
    done = o.w.read_json(fresh / 'done.json')
    assert done['artifacts'] == review['artifacts'] and done['criteria'] == review['criteria']
    assert all(c['exit_code'] == 0 for c in done['checks'])
    with pytest.raises(FileExistsError):
        o.finish_review(tmp_path, t, result, session, validation_session=fresh)


def test_repair_limit_survives_supervisor_restart(tmp_path, monkeypatch):
    t, session, review, rel, result = review_inputs(tmp_path, 'changes_requested')
    review['findings'] = [{'id': 'R01', 'consequence': 'synthetic missing condition'}]
    o.dump(tmp_path / rel, review)
    prior = []
    for number in range(2):
        path = f'private/workflow/runs/IG-2C/history-{number}/review.json'
        o.dump(tmp_path / path, {'findings': [{'id': 'R01'}]})
        prior.append({'to': 'changes_requested', 'evidence': path, 'sha256': o.w.digest(tmp_path / path)})
    t['events'] = prior + t['events']
    monkeypatch.setattr(o, 'apply_transition', lambda *args: pytest.fail('Repair limit must stop'))
    with pytest.raises(ValueError, match='Two repair cycles'):
        o.finish_review(tmp_path, t, result, session)


@pytest.mark.parametrize('current,blocked', [(['F03', 'F04'], False), (['F01', 'F03'], False),
                                           (['F01', 'F04'], False), (['F02', 'F04'], True)])
def test_finding_budgets_are_independent_for_new_and_grouped_repairs(tmp_path, monkeypatch, current, blocked):
    t, session, review, rel, result = review_inputs(tmp_path, 'changes_requested')
    events = []
    for number, ids in enumerate([['F01', 'F02'], ['F02']]):
        path = f'private/workflow/runs/IG-2C/history-{number}/review.json'
        o.dump(tmp_path / path, {'findings': [{'id': id} for id in ids]})
        events.append({'to': 'changes_requested', 'evidence': path, 'sha256': o.w.digest(tmp_path / path)})
    t['events'] = events + t['events']
    review['findings'] = [{'id': id} for id in current]; o.dump(tmp_path / rel, review)
    budget = o.finding_repair_budget(tmp_path, t, review)
    assert budget['prior_requests'] == {'F01': 1, 'F02': 2}
    calls = []
    monkeypatch.setattr(o, 'apply_transition', lambda *a: calls.append(a[2]))
    if blocked:
        with pytest.raises(ValueError, match='findings F02'): o.finish_review(tmp_path, t, result, session)
        assert calls == []
    else:
        o.finish_review(tmp_path, t, result, session)
        assert calls == ['changes_requested']


@pytest.mark.parametrize('ids', [[None], [''], ['F03', 'F03']])
def test_repair_budget_refuses_missing_or_duplicate_finding_ids(tmp_path, ids):
    with pytest.raises(ValueError, match='unique nonempty stable IDs'):
        o.finding_repair_budget(tmp_path, task(), {'findings': [{'id': id} for id in ids]})


def test_repair_budget_cannot_reset_by_tampering_with_prior_review(tmp_path):
    path = 'private/workflow/runs/IG-2C/history/review.json'
    o.dump(tmp_path / path, {'findings': [{'id': 'F03'}]})
    t = task(); t['events'] = [{'to': 'changes_requested', 'evidence': path, 'sha256': o.w.digest(tmp_path / path)}]
    o.dump(tmp_path / path, {'findings': [{'id': 'OTHER'}]})
    with pytest.raises(ValueError, match='Prior finding review changed'):
        o.finding_repair_budget(tmp_path, t, {'findings': [{'id': 'F03'}]})


def test_successful_review_runs_checks_then_uses_existing_transition_gate(tmp_path, monkeypatch):
    t, session, _, _, result = review_inputs(tmp_path)
    calls = []
    monkeypatch.setattr(o, 'run_check', lambda *a: 0)
    monkeypatch.setattr(o, 'apply_transition', lambda root, id, state, evidence, deadline: calls.append((state, evidence)))
    o.finish_review(tmp_path, t, result, session)
    assert [c[0] for c in calls] == ['accepted', 'done']
    done = o.w.read_json(tmp_path / calls[-1][1])
    assert done['role'] == 'coordinator' and done['model'] is None
    assert done['artifacts'] == o.w.read_json(tmp_path / result['evidence'])['artifacts']


def test_failed_supervisor_check_cannot_accept(tmp_path, monkeypatch):
    t, session, _, _, result = review_inputs(tmp_path)
    monkeypatch.setattr(o, 'run_check', lambda *a: 1)
    monkeypatch.setattr(o, 'apply_transition', lambda *args: pytest.fail('No acceptance with failing checks'))
    with pytest.raises(ValueError, match='validation failed'):
        o.finish_review(tmp_path, t, result, session)


def test_zero_remaining_launch_budget_starts_no_model(tmp_path, monkeypatch):
    q = queue(task(), complete_task())
    o.dump(tmp_path / o.w.QUEUE, q)
    monkeypatch.setattr(o.w, 'validate', lambda *a: None)
    monkeypatch.setattr(o, 'launch', lambda *a: pytest.fail('Budget must prevent launch'))
    run_dir = tmp_path / 'private/workflow/orchestrator/synthetic'
    assert o.run(tmp_path, 'unused', run_dir, 0, 1, 10) == 2
    status = o.w.read_json(run_dir / 'status.json')
    assert status['state'] == 'budget_stop' and status['sessions'] == 0
    assert not (tmp_path / 'private/workflow/ig2-orchestrator.lock').exists()


def test_supervisor_binds_search_to_generated_packet_and_environment(tmp_path, monkeypatch):
    t, _, _, _, _ = review_inputs(tmp_path)
    t.update(status='ready', events=[])
    q = queue(t, complete_task())
    o.dump(tmp_path / o.w.QUEUE, q)
    pins = []
    for rel in ['docs/packet.md', 'docs/STATUS.md', 'private/unrelated.json']:
        o.dump(tmp_path / rel, {'synthetic': True})
        pins.append({'path': rel, 'sha256': o.w.digest(tmp_path / rel)})
    monkeypatch.setattr(o.w, 'validate', lambda *a: None)
    monkeypatch.setattr(o.w, 'packet', lambda *a, **kw: {'task': t['id'], 'files': pins})
    def launch(cli, root, session, text, timeout, env):
        manifest = o.w.read_json(session / 'search-manifest.json')
        paths = {p['path'] for p in manifest['files']}
        assert 'docs/packet.md' in paths and 'scripts/search_task.py' in paths
        assert 'docs/STATUS.md' not in paths and 'private/unrelated.json' not in paths
        assert env['WGC_TASK_ID'] == t['id']
        assert env['WGC_TASK_SEARCH_MANIFEST'] == (session / 'search-manifest.json').relative_to(root).as_posix()
        assert env['WGC_TASK_SEARCH_SHA256'] == o.w.digest(session / 'search-manifest.json')
        assert env['WGC_TASK_SEARCH_SHA256'] in text
        assert env['WGC_TASK_DEPENDENCY_SHA256'] == o.w.digest(session / 'dependency-view.json')
        assert env['WGC_TASK_DEPENDENCY_VIEW'] == (session / 'dependency-view.json').relative_to(root).as_posix()
        assert env['WGC_TASK_DEPENDENCY_SHA256'] in text
        assert env['WGC_TASK_ACCESS_SHA256'] == o.w.digest(session / 'access-manifest.json')
        assert env['WGC_CONTEXT_GUARD_SHA256'] == o.w.digest(session / 'context-guard.json')
        access = o.w.read_json(session / 'access-manifest.json')
        snapshot = access['bootstrap_reads']['docs/STATUS.md']
        assert snapshot['path'] == (session / 'bootstrap/STATUS.md').relative_to(root).as_posix()
        assert snapshot['sha256'] == o.w.digest(root / snapshot['path'])
        assert snapshot['path'] not in paths
        runtime = o.w.read_json(session / 'tool-runtime.json')['ripgrep']
        assert env['WGC_RIPGREP_PATH'] == runtime['path']
        assert Path(runtime['path']).is_absolute()
        assert env['WGC_RIPGREP_SHA256'] == runtime['sha256'] == o.w.digest(Path(runtime['path']))
        assert runtime['version'].startswith('ripgrep ')
        assert manifest['packet']['sha256'] == o.w.digest(session / 'packet.json')
        return {'outcome': 'blocked', 'evidence': None, 'summary': 'Synthetic binding verified'}
    monkeypatch.setattr(o, 'launch', launch)
    run_dir = tmp_path / 'r'
    assert o.run(tmp_path, 'unused', run_dir, 1, 5, 10) == 2
    assert o.w.read_json(run_dir / 'status.json')['summary'] == 'Synthetic binding verified'


def test_missing_ripgrep_stops_dispatch_before_claim_or_model(tmp_path, monkeypatch):
    t, _, _, _, _ = review_inputs(tmp_path)
    t.update(status='ready', events=[])
    o.dump(tmp_path / o.w.QUEUE, queue(t, complete_task()))
    monkeypatch.setattr(o.w, 'validate', lambda *a: None)
    monkeypatch.setattr(o.w, 'packet', lambda *a, **k: {'task': t['id'], 'files': []})
    monkeypatch.setattr(o, 'launch', lambda *a, **k: pytest.fail('Missing native tool must stop before model'))
    monkeypatch.delenv('WGC_RIPGREP_PATH', raising=False)
    monkeypatch.delenv('WGC_RIPGREP_SHA256', raising=False)
    monkeypatch.setenv('PATH', '')
    run_dir = tmp_path / 'native-tool-preflight'
    assert o.run(tmp_path, 'unused', run_dir, 1, 5, 10) == 2
    state = o.w.read_json(run_dir / 'status.json')
    assert state['state'] == 'blocked' and state['sessions'] == 0
    assert 'Ripgrep unavailable' in state['summary']
    assert o.w.read_json(tmp_path / o.w.QUEUE)['tasks'][0]['status'] == 'ready'


def test_unexpected_preparation_error_records_blocked_status_and_keeps_traceback(tmp_path, monkeypatch):
    o.dump(tmp_path / o.w.QUEUE, queue(task(), complete_task()))
    monkeypatch.setattr(o.w, 'validate', lambda *a: None)
    def broken_prepare(*args):
        raise TypeError('Synthetic malformed runtime metadata')
    monkeypatch.setattr(o, 'prepare', broken_prepare)
    monkeypatch.setattr(o, 'launch', lambda *a: pytest.fail('No model after failed preparation'))
    run_dir = tmp_path / 'run'
    with pytest.raises(TypeError, match='Synthetic malformed'):
        o.run(tmp_path, 'unused', run_dir, 1, 5, 10)
    status = o.w.read_json(run_dir / 'status.json')
    assert status['state'] == 'blocked' and status['ended_utc']
    assert 'TypeError' in status['summary'] and status['sessions'] == 0
    assert not (tmp_path / 'private/workflow/ig2-orchestrator.lock').exists()


def test_existing_supervisor_lock_is_not_stolen(tmp_path):
    lock = tmp_path / 'private/workflow/ig2-orchestrator.lock'
    o.dump(lock, {'pid': 'another-owner'})
    with pytest.raises(FileExistsError):
        o.run(tmp_path, 'unused', tmp_path / 'new-run', 1, 1, 1)
    assert o.w.read_json(lock)['pid'] == 'another-owner'


def test_inventory_coordinator_packet_closes_documentation_and_git_scope(tmp_path):
    t, _, _, _, _ = review_inputs(tmp_path)
    t.update(id='IG-2B04', title='Inventory SPQR PDF pages 13-16', status='planned', events=[])
    policy = o.w.read_json(tmp_path / 'docs/work/context-policy.json')
    for rel in o.INVENTORY_TOOL_CONTEXT:
        p = tmp_path / rel; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('Pinned synthetic inventory documentation', encoding='utf-8')
        policy['allow'].append(rel)
    o.dump(tmp_path / 'docs/work/context-policy.json', policy)
    o.dump(tmp_path / o.w.QUEUE, queue(t, complete_task()))
    s = tmp_path / 'closed-packet'; s.mkdir()
    o.prepare(tmp_path, queue(t, complete_task()), t, 'coordinator', s)
    paths = {p['path'] for p in o.w.read_json(s / 'search-manifest.json')['files']}
    assert set(o.INVENTORY_TOOL_CONTEXT) <= paths
    # Planned cards may omit required bootstrap reads from their product context.
    assert t['context'] == []
    assert {'README.md', 'docs/work/WORKFLOW.md'} <= paths
    packet = o.w.read_json(s / 'packet.json')
    for rel in ('README.md', 'docs/work/WORKFLOW.md'):
        pin = next(p for p in packet['control_files'] if p['path'] == rel)
        assert pin['sha256'] == o.w.digest(tmp_path / rel)
    assert 'src/wgc/sources/README.md' in paths and 'docs/work/EVIDENCE.md' in paths
    access = o.w.read_json(s / 'access-manifest.json')
    assert 'private/workflow/runs/IG-2B04/' in access['git_paths']
    assert 'private/workflow/checks/' not in access['git_paths']
    assert 'private/workflow/packets/' not in access['git_paths']
    assert 'private/workflow/runs/IG-2B03/' not in access['git_paths']
    guard = o.w.read_json(s / 'context-guard.json')
    assert guard['task'] == 'IG-2B04' and guard['denial'].endswith('/context-denied.json')


@pytest.mark.parametrize('role', ['executor', 'coordinator'])
def test_other_same_stage_task_cannot_be_changed(role):
    c = dict(task(), tests=['Required check'])
    before = queue(c, complete_task())
    after = copy.deepcopy(before); after['tasks'][1]['acceptance'] = ['weakened']
    with pytest.raises(ValueError, match='Another task'):
        o.check_queue_delta(before, after, c, role)


@pytest.mark.parametrize('key,value', [('semantic_acceptance_required', False), ('acceptance', ['weakened'])])
def test_executor_cannot_change_its_contract(key, value):
    c = dict(task(), semantic_acceptance_required=True)
    before = queue(c, complete_task()); after = copy.deepcopy(before)
    after['tasks'][0][key] = value
    with pytest.raises(ValueError, match='immutable'):
        o.check_queue_delta(before, after, c, 'executor')


def test_coordinator_cannot_lower_criteria_or_human_gate():
    c = dict(task(status='planned'), tests=['Required check'], semantic_acceptance_required=True)
    before = queue(c, complete_task()); after = copy.deepcopy(before)
    after['tasks'][0]['semantic_acceptance_required'] = False
    with pytest.raises(ValueError, match='human acceptance'):
        o.check_queue_delta(before, after, c, 'coordinator')
    after = copy.deepcopy(before); after['tasks'][0]['tests'] = []
    with pytest.raises(ValueError, match='required tests'):
        o.check_queue_delta(before, after, c, 'coordinator')


@pytest.mark.parametrize('key,value', [('context_recovery_authorization', {}),
                                      ('dependency_scope', {'physical_pages': [12, 13, 14, 15]})])
def test_coordinator_cannot_replace_operator_context_recovery(key, value):
    t = dict(task(status='planned'), tests=['Required check'],
             context_recovery_authorization={'scope': 'immutable operator authority'},
             dependency_scope={'physical_pages': [13, 14, 15, 16]})
    before = queue(t, complete_task()); after = copy.deepcopy(before)
    after['tasks'][0][key] = value
    with pytest.raises(ValueError, match='operator context recovery'):
        o.check_queue_delta(before, after, t, 'coordinator')


def test_context_incident_is_rechecked_after_blocked_role(tmp_path, monkeypatch):
    t, _, _, _, _ = review_inputs(tmp_path)
    t.update(status='ready', events=[])
    pins = {}
    for name in ['incident', 'scope', 'assessment']:
        rel = f'private/workflow/runs/{t["id"]}/context-recovery/{name}.json'
        o.dump(tmp_path / rel, {'immutable': True})
        pins[name] = {'path': rel, 'sha256': o.w.digest(tmp_path / rel)}
    t['context_recovery_authorization'] = pins
    q = queue(t, complete_task()); o.dump(tmp_path / o.w.QUEUE, q)
    monkeypatch.setattr(o.w, 'validate', lambda *a: None)
    monkeypatch.setattr(o.w, 'packet', lambda *a, **kw: {'task': t['id'], 'files': []})
    def launch(*args):
        o.dump(tmp_path / pins['incident']['path'], {'tampered': True})
        return {'outcome': 'blocked', 'evidence': None, 'summary': 'Synthetic stop'}
    monkeypatch.setattr(o, 'launch', launch)
    run_dir = tmp_path / 'r'
    assert o.run(tmp_path, 'unused', run_dir, 1, 5, 10) == 2
    assert 'Frozen artifact changed' in o.w.read_json(run_dir / 'status.json')['summary']


@pytest.mark.parametrize('tampered', [False, True])
@pytest.mark.parametrize('list_prefix', [False, True])
def test_planned_coordinator_inherits_only_verified_dependency_runtime(tmp_path, tampered, list_prefix):
    t = task(status='planned')
    rel = 'private/workflow/runs/IG-2B03/frozen/toolchain.json'
    prefix = [str(tmp_path)] if list_prefix else str(tmp_path)
    o.dump(tmp_path / rel, {'process_pythonpath': str(tmp_path), 'process_path_prefix': prefix})
    pin = {'path': rel, 'sha256': o.w.digest(tmp_path / rel)}
    s = tmp_path / 'session'
    o.dump(s / 'dependency-view.json', {'dependencies': {'IG-2B03': {'inventory': {'reports': {'toolchain.json': pin}}}}})
    o.dump(s / 'search-manifest.json', {'synthetic': True})
    o.dump(s / 'access-manifest.json', {'synthetic': True})
    o.dump(s / 'context-guard.json', {'synthetic': True})
    if tampered:
        o.dump(tmp_path / rel, {'process_pythonpath': 'changed'})
        with pytest.raises(ValueError, match='artifact changed'):
            o.launch_environment(tmp_path, t, s)
    else:
        env = o.launch_environment(tmp_path, t, s)
        assert env['PYTHONPATH'] == str(tmp_path)
        assert env['PATH'].startswith(str(tmp_path))
        assert t['context'] == []  # The queued contract remains unchanged.


def test_reviewer_mutation_rejected_regardless_of_outcome():
    c = task(status='review'); before = queue(c, complete_task()); after = copy.deepcopy(before)
    after['tasks'][0]['status'] = 'blocked'
    with pytest.raises(ValueError, match='Reviewer modified'):
        o.check_queue_delta(before, after, c, 'reviewer')


def test_configuration_citation_must_match_observed_session(tmp_path):
    t, session, review, rel, result = review_inputs(tmp_path)
    review['configuration_evidence'] = 'invented.json'; o.dump(tmp_path / rel, review)
    with pytest.raises(ValueError, match='not bound'):
        o.finish_review(tmp_path, t, result, session)


def test_hanging_check_is_terminated_within_deadline(tmp_path):
    started = time.monotonic()
    with pytest.raises((o.subprocess.TimeoutExpired, ValueError)):
        o.run_check([sys.executable, '-c', 'import time; time.sleep(60)'], tmp_path,
                    tmp_path / 'check.log', time.monotonic() + 0.15)
    assert time.monotonic() - started < 12


def test_expired_deadline_never_starts_process(tmp_path, monkeypatch):
    monkeypatch.setattr(o.subprocess, 'Popen', lambda *a, **kw: pytest.fail('Expired deadline'))
    with pytest.raises(ValueError, match='budget exhausted'):
        o.run_check(['unused'], tmp_path, tmp_path / 'check.log', time.monotonic() - 1)


def test_failed_tree_termination_reports_owned_pid(monkeypatch):
    if o.os.name != 'nt':
        pytest.skip('Windows tree termination policy')
    class Process:
        pid = 123456
        def poll(self): return None
        def kill(self): pass
        def wait(self, timeout): return 1
    monkeypatch.setattr(o.subprocess, 'run', lambda *a, **kw: type('Result', (), {'returncode': 1})())
    with pytest.raises(ValueError, match='PID 123456'):
        o.stop_process(Process())


def test_background_launch_detaches_and_preserves_logs(tmp_path, monkeypatch):
    calls = []
    def spawn(argv, **kwargs):
        calls.append((argv, kwargs))
        assert kwargs['stdout'].name.endswith('stdout.log')
        assert kwargs['stderr'].name.endswith('stderr.log')
        return type('Process', (), {'pid': 123456})()
    monkeypatch.setattr(o.subprocess, 'Popen', spawn)
    result = o.start_background(tmp_path, 'codex', 48, 3600, 28800)
    argv, options = calls[0]
    assert argv[2] == 'run' and '--approve-for-me' not in argv
    assert options['stdin'] == o.subprocess.DEVNULL and options['close_fds']
    if o.os.name == 'nt':
        assert options['creationflags'] & o.subprocess.CREATE_BREAKAWAY_FROM_JOB
        assert options['creationflags'] & o.subprocess.DETACHED_PROCESS
        assert options['creationflags'] & o.subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        assert options['start_new_session']
    record = o.w.read_json(Path(result['launch_directory']) / 'launch.json')
    assert record['pid'] == 123456 and record['state'] == 'launched'
    assert record['builder_model'] is None


def test_background_launch_never_bypasses_lock_or_failed_detachment(tmp_path, monkeypatch):
    lock = tmp_path / 'private/workflow/ig2-orchestrator.lock'
    lock.parent.mkdir(parents=True)
    lock.write_text('preserved', encoding='utf-8')
    monkeypatch.setattr(o.subprocess, 'Popen', lambda *a, **k: pytest.fail('Existing lock'))
    with pytest.raises(ValueError, match='ownership triage'):
        o.start_background(tmp_path, 'codex', 48, 3600, 28800)
    assert lock.read_text(encoding='utf-8') == 'preserved'
    lock.unlink()
    def denied(*a, **k):
        raise PermissionError('Job breakaway denied')
    monkeypatch.setattr(o.subprocess, 'Popen', denied)
    with pytest.raises(PermissionError, match='breakaway denied'):
        o.start_background(tmp_path, 'codex', 48, 3600, 28800)
    records = list((tmp_path / 'private/workflow/launches').glob('*/launch.json'))
    assert len(records) == 1
    assert o.w.read_json(records[0])['state'] == 'launch_failed'


def test_detached_supervisor_survives_launcher_exit(tmp_path):
    scripts = tmp_path / 'scripts'
    scripts.mkdir()
    marker = tmp_path / 'survived.txt'
    (scripts / 'orchestrate_ig2.py').write_text(
        'import time, os, json\nfrom pathlib import Path\ntime.sleep(0.5)\n'
        + f'Path({str(marker)!r}).write_text(json.dumps({{"pid": os.getpid()}}))\n', encoding='utf-8')
    launcher = tmp_path / 'launcher.py'
    launcher.write_text(
        f'import sys\nsys.path.insert(0, {str(ROOT / "scripts")!r})\n'
        'from pathlib import Path\nimport orchestrate_ig2 as o\n'
        + f'o.start_background(Path({str(tmp_path)!r}), "unused", 1, 5, 10)\n', encoding='utf-8')
    result = o.subprocess.run([sys.executable, str(launcher)], capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr.decode(errors='replace')
    deadline = time.monotonic() + 10
    while not marker.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    actual_pid = json.loads(marker.read_text())['pid']
    launches = list((tmp_path / 'private/workflow/launches').glob('*/launch.json'))
    assert len(launches) == 1
    assert o.w.read_json(launches[0])['pid'] == actual_pid


def test_rereview_gets_only_current_finding_and_repair_references(tmp_path, monkeypatch):
    t, session, _, _, _ = review_inputs(tmp_path)
    base = copy.deepcopy(t['events'][0])
    t['events'] = [base, {'to': 'changes_requested', 'evidence': 'findings.json', 'sha256': 'pin'},
                   {'to': 'in_progress', 'evidence': 'claim.json', 'sha256': 'pin'}, base]
    monkeypatch.setattr(o.w, 'packet', lambda *a, **kw: {'files': [], 'task': t['id']})
    o.prepare(tmp_path, queue(t), t, 'reviewer', session)
    refs = o.w.read_json(session / 'references.json')
    assert refs['findings']['evidence'] == 'findings.json'
    assert refs['repair_claim']['evidence'] == 'claim.json'
    assert refs['prior_delivery'] == base
    assert 'events' not in o.w.read_json(session / 'task.json')


def test_partition_targets_cannot_overlap_or_disappear():
    c = task(status='done')
    d = dict(task('IG-2D', 'planned', ['IG-2C']), kind='refine', tests=['Partition equality'])
    before = queue(c, d); after = copy.deepcopy(before)
    after['tasks'][1].update(kind='closure', depends=['IG-2D-A01', 'IG-2D-A02'], target_ids=['a', 'b'])
    for id in ['IG-2D-A01', 'IG-2D-A02']:
        after['tasks'].append(dict(task(id, 'planned', ['IG-2C']), target_ids=['a']))
    with pytest.raises(ValueError, match='target set mismatch'):
        o.check_queue_delta(before, after, d, 'coordinator', ['a', 'b'])
    after['tasks'][-1]['target_ids'] = ['b']
    o.check_queue_delta(before, after, d, 'coordinator', ['a', 'b'])
    after['tasks'][1]['target_ids'] = ['a']
    after['tasks'][1]['depends'] = ['IG-2D-A01']
    after['tasks'].pop()
    with pytest.raises(ValueError, match='accepted dependency'):
        o.check_queue_delta(before, after, d, 'coordinator', ['a', 'b'])


def test_nonreading_cli_cannot_block_prompt_feed_forever(tmp_path, monkeypatch):
    session = tmp_path / 'session'; session.mkdir()
    script = tmp_path / 'no_read.py'
    script.write_text("import sys,time\nprint('model: gpt-6.1-sol\\nreasoning effort: high\\nsession id: synthetic\\nuser',file=sys.stderr,flush=True)\ntime.sleep(60)\n", encoding='utf-8')
    monkeypatch.setattr(o, 'command', lambda *a: [sys.executable, str(script)])
    started = time.monotonic()
    with pytest.raises(ValueError):
        o.launch('unused', tmp_path, session, 'x' * 200000, 2)
    assert time.monotonic() - started < 22  # Startup + bounded tree/pipe cleanup, never the 60s child sleep.
    assert o.w.read_json(session / 'runtime-configuration.json')['status'] == 'confirmed'


def test_partition_universe_is_pinned_to_accepted_manifest(tmp_path):
    inputs = []
    for name in ['inventory.json', 'import.json']:
        (tmp_path / name).write_text('{}', encoding='utf-8')
        inputs.append({'path': name, 'sha256': o.w.digest(tmp_path / name)})
    o.dump(tmp_path / 'reconciliation-universe.json', {'format': 'wgc-reconciliation-universe-1',
                                                      'target_ids': ['a', 'b'], 'inputs': inputs})
    reference = {'path': 'reconciliation-universe.json', 'sha256': o.w.digest(tmp_path / 'reconciliation-universe.json')}
    o.dump(tmp_path / 'accepted.json', {'artifacts': [reference]})
    c = task(status='done')
    c['events'] = [{'to': 'done', 'evidence': 'accepted.json', 'sha256': o.w.digest(tmp_path / 'accepted.json')}]
    d = task('IG-2D', 'planned', ['IG-2C'])
    assert o.accepted_universe(tmp_path, queue(c, d), d)[0] == ['a', 'b']
    o.dump(tmp_path / 'reconciliation-universe.json', {'target_ids': ['a']})
    with pytest.raises(ValueError, match='Frozen artifact'):
        o.accepted_universe(tmp_path, queue(c, d), d)


def test_partition_cannot_be_bypassed_by_direct_readiness():
    d = dict(task('IG-2D', 'planned', ['IG-2C']), kind='refine', tests=['Partition equality'])
    before = queue(task(status='done'), d)
    after = copy.deepcopy(before)
    after['tasks'][1].update(kind='implementation', status='ready')
    with pytest.raises(ValueError, match='must create'):
        o.check_queue_delta(before, after, d, 'coordinator', ['a', 'b'])


def repair_inputs(tmp_path):
    t, session, review, review_rel, _ = review_inputs(tmp_path, 'changes_requested')
    t.update(status='changes_requested', tests=['Required unchanged validation'])
    review['findings'] = [{'id': 'V01', 'category': 'required_validation_environment_failure'}]
    o.dump(tmp_path / review_rel, review)
    t['events'].append({'to': 'changes_requested', 'evidence': review_rel,
                        'sha256': o.w.digest(tmp_path / review_rel)})
    attempt = 'private/workflow/runs/IG-2C/repair-v01-fresh/'
    t['write_scope'] = [attempt]
    scope = {'review_evidence': review_rel, 'review_sha256': t['events'][-1]['sha256'],
             'finding_ids': ['V01'], 'attempt': attempt, 'acceptance': t['acceptance'],
             'tests': t['tests'], 'immutable_delivery': {'path': t['events'][0]['evidence'],
             'sha256': t['events'][0]['sha256']}, 'mode': 'validation_only'}
    scope_path = 'private/workflow/runs/IG-2C/preparation-v01/scope.json'
    evidence_path = 'private/workflow/runs/IG-2C/preparation-v01/authorization.json'
    o.dump(tmp_path / scope_path, scope)
    o.dump(tmp_path / evidence_path, {'summary': 'Synthetic authorization'})
    t['repair_authorization'] = {'review_evidence': review_rel,
        'review_sha256': t['events'][-1]['sha256'], 'attempt': attempt,
        'scope': {'path': scope_path, 'sha256': o.w.digest(tmp_path / scope_path)},
        'evidence': {'path': evidence_path, 'sha256': o.w.digest(tmp_path / evidence_path)}}
    return t, scope


def test_new_findings_route_to_coordinator_before_executor():
    t = task(status='changes_requested')
    t['events'] = [{'to': 'changes_requested', 'evidence': 'new-review.json', 'sha256': 'new'}]
    assert o.select(queue(t, complete_task())) == (t, 'coordinator')
    t['repair_authorization'] = {'review_evidence': 'old-review.json', 'review_sha256': 'old',
                                 'attempt': 'old/', 'scope': {'path': 'old'}, 'evidence': {'path': 'old'}}
    assert o.select(queue(t, complete_task())) == (t, 'coordinator')


def test_fresh_exact_authorization_unblocks_executor(tmp_path):
    t, scope = repair_inputs(tmp_path)
    assert o.select(queue(t, complete_task())) == (t, 'executor')
    assert o.verify_repair_authorization(tmp_path, t) == scope


def test_used_repair_directory_cannot_be_reused(tmp_path):
    t, _ = repair_inputs(tmp_path)
    (tmp_path / t['repair_authorization']['attempt']).mkdir()
    with pytest.raises(ValueError, match='already exists'):
        o.verify_repair_authorization(tmp_path, t)


@pytest.mark.parametrize('key,value', [('finding_ids', ['R01']), ('mode', 'product_repair'),
    ('immutable_delivery', {'path': 'other.json', 'sha256': 'wrong'})])
def test_current_scope_cannot_reauthorize_obsolete_repairs(tmp_path, key, value):
    t, scope = repair_inputs(tmp_path)
    scope[key] = value
    pin = t['repair_authorization']['scope']
    o.dump(tmp_path / pin['path'], scope); pin['sha256'] = o.w.digest(tmp_path / pin['path'])
    with pytest.raises(ValueError):
        o.verify_repair_authorization(tmp_path, t)


def test_repair_coordinator_must_not_claim_or_change_status(tmp_path):
    t, _ = repair_inputs(tmp_path)
    before = queue(copy.deepcopy(t), complete_task())
    after = copy.deepcopy(before); after['tasks'][0]['status'] = 'in_progress'
    with pytest.raises(ValueError, match='not transition'):
        o.check_queue_delta(before, after, t, 'coordinator')


def test_repair_coordinator_preserves_criteria_and_authorizes_exact_review(tmp_path):
    t, _ = repair_inputs(tmp_path)
    before_task = copy.deepcopy(t); before_task.pop('repair_authorization')
    before = queue(before_task, complete_task()); after = queue(t, complete_task())
    o.check_queue_delta(before, after, before_task, 'coordinator')
    after['tasks'][0]['acceptance'] = ['weakened']
    with pytest.raises(ValueError, match='required acceptance'):
        o.check_queue_delta(before, after, before_task, 'coordinator')


def test_unchanged_blocked_coordinator_preserves_its_blocker_summary():
    t = task(status='changes_requested')
    before = queue(t, complete_task())
    o.check_queue_delta(before, copy.deepcopy(before), t, 'coordinator', outcome='blocked')
    after = copy.deepcopy(before); after['tasks'][0]['acceptance'] = ['weakened']
    with pytest.raises(ValueError):
        o.check_queue_delta(before, after, t, 'coordinator', outcome='blocked')


def test_validation_repair_cannot_mutate_an_old_artifact(tmp_path):
    t, _, _, _, _ = review_inputs(tmp_path)
    original = o.w.read_json(tmp_path / t['events'][0]['evidence'])['artifacts']
    (tmp_path / 'synthetic.txt').write_text('changed by validation repair', encoding='utf-8')
    with pytest.raises(ValueError, match='Frozen artifact'):
        o.verify_preserved_delivery(tmp_path, original, {'artifacts': original})


def test_validation_repair_cannot_drop_an_old_manifest_entry(tmp_path):
    t, _, _, _, _ = review_inputs(tmp_path)
    original = o.w.read_json(tmp_path / t['events'][0]['evidence'])['artifacts']
    with pytest.raises(ValueError, match='omitted'):
        o.verify_preserved_delivery(tmp_path, original, {'artifacts': []})
    o.verify_preserved_delivery(tmp_path, original, {'artifacts': original + [{'path': 'new-report.json'}]})


def test_pinned_bundled_environment_is_inherited_without_global_mutation(tmp_path, monkeypatch):
    native = tmp_path / 'native'; native.mkdir()
    source = tmp_path / 'src'; source.mkdir()
    bundled = tmp_path / 'site-packages'; bundled.mkdir()
    pythonpath = o.os.pathsep.join([str(source), str(bundled)])
    o.dump(tmp_path / 'toolchain.json', {'process_pythonpath': pythonpath, 'process_path_prefix': str(native)})
    monkeypatch.setenv('PYTHONPATH', 'inherited-original')
    env = o.validation_environment(tmp_path, {'context': ['toolchain.json']})
    assert env['PYTHONPATH'] == pythonpath
    assert env['PATH'].startswith(str(native) + o.os.pathsep)
    assert o.os.environ['PYTHONPATH'] == 'inherited-original'
    assert env['PYTHONDONTWRITEBYTECODE'] == '1'


@pytest.mark.parametrize('bound_rg', [False, True])
def test_native_path_list_preserves_order_duplicates_expired_entries_and_inherited_tail(tmp_path, monkeypatch, bound_rg):
    binding = o.task_search.ripgrep_binding() if bound_rg else None
    first = tmp_path / 'native first'; first.mkdir()
    second = tmp_path / 'native second'; second.mkdir()
    expired = tmp_path / 'expired-session-wrapper'
    prefix = [str(first), str(expired), str(second), str(first)]
    o.dump(tmp_path / 'toolchain.json', {'process_path_prefix': prefix})
    monkeypatch.setenv('PATH', 'inherited-path')
    if binding:
        monkeypatch.setenv('WGC_RIPGREP_PATH', binding['path'])
        monkeypatch.setenv('WGC_RIPGREP_SHA256', binding['sha256'])
    else:
        monkeypatch.delenv('WGC_RIPGREP_PATH', raising=False)
        monkeypatch.delenv('WGC_RIPGREP_SHA256', raising=False)
    env = o.validation_environment(tmp_path, {'context': ['toolchain.json']})
    rg_prefix = [str(Path(binding['path']).parent)] if binding else []
    assert env['PATH'] == o.os.pathsep.join(prefix + rg_prefix + ['inherited-path'])
    assert o.os.environ['PATH'] == 'inherited-path'
    assert not expired.exists()
    assert o.w.read_json(tmp_path / 'toolchain.json')['process_path_prefix'] == prefix


@pytest.mark.parametrize('prefix', [42, False, {}, [['nested']], [''], ['native', 7],
    ['native\x00bad'], ['one' + o.os.pathsep + 'two']])
def test_invalid_native_path_prefix_has_a_controlled_error(prefix):
    with pytest.raises(ValueError, match='native path prefix'):
        o.native_path_prefix(prefix)


@pytest.mark.parametrize('list_prefix', [False, True])
def test_unavailable_native_path_prefix_is_not_replaced_by_inherited_path(tmp_path, list_prefix):
    missing = str(tmp_path / 'missing-native')
    prefix = [missing] if list_prefix else missing
    with pytest.raises(ValueError, match='dependency directory is unavailable'):
        o.native_path_prefix(prefix)


def test_validation_exposes_pinned_rg_to_raw_tests_without_losing_environment(tmp_path, monkeypatch):
    binding = o.task_search.ripgrep_binding()
    inherited = o.os.environ.get('PATH', '')
    monkeypatch.setenv('WGC_RIPGREP_PATH', binding['path'])
    monkeypatch.setenv('WGC_RIPGREP_SHA256', binding['sha256'])
    native = tmp_path / 'native'; native.mkdir()
    pythonpath = o.os.pathsep.join([str(tmp_path), str(native)])
    o.dump(tmp_path / 'toolchain.json', {'process_pythonpath': pythonpath, 'process_path_prefix': str(native)})
    env = o.validation_environment(tmp_path, {'context': ['toolchain.json']})
    assert env['PATH'].endswith(o.os.pathsep + inherited)
    assert env['PATH'].startswith(str(native) + o.os.pathsep)
    assert env['PYTHONPATH'] == pythonpath
    assert o.os.environ['PATH'] == inherited
    probe = o.subprocess.run([sys.executable, '-c',
        'import subprocess; subprocess.run(["rg","--version"],check=True)'], env=env,
        capture_output=True, timeout=10)
    assert probe.returncode == 0 and probe.stdout.startswith(b'ripgrep ')


def reduced_validation_delivery(tmp_path):
    t, _ = repair_inputs(tmp_path)
    unrelated = tmp_path / 'new-report.txt'; unrelated.write_text('new report', encoding='utf-8')
    reduced = {'actor': 'new-executor', 'artifacts': [{'path': unrelated.name, 'sha256': o.w.digest(unrelated)}]}
    rel = 'private/workflow/runs/IG-2C/repair-v01-fresh/delivery.json'
    o.dump(tmp_path / rel, reduced)
    t['events'].append({'to': 'review', 'evidence': rel, 'sha256': o.w.digest(tmp_path / rel)})
    t['status'] = 'review'
    return t


def test_restart_reviewer_cannot_bypass_validation_preservation(tmp_path, monkeypatch):
    t = reduced_validation_delivery(tmp_path)
    monkeypatch.setattr(o.w, 'packet', lambda *a, **kw: {'files': [], 'task': t['id']})
    with pytest.raises(ValueError, match='omitted'):
        o.prepare(tmp_path, queue(t), t, 'reviewer', tmp_path / 'fresh-review-session')


def test_blocked_executor_after_delivery_still_checks_manifest_preservation(tmp_path, monkeypatch):
    after_task = reduced_validation_delivery(tmp_path)
    before_task = copy.deepcopy(after_task)
    before_task['events'].pop(); before_task['status'] = 'changes_requested'
    q = queue(before_task, complete_task())
    o.dump(tmp_path / o.w.QUEUE, q)
    original = o.w.read_json(tmp_path / before_task['events'][0]['evidence'])['artifacts']
    monkeypatch.setattr(o.w, 'validate', lambda *a: None)
    monkeypatch.setattr(o, 'select', lambda q: (q['tasks'][0], 'executor'))
    def prepare(root, q, task, role, session):
        o.dump(session / 'preserved-artifacts.json', original)
        o.dump(session / 'search-manifest.json', {'format': 'synthetic'})
        o.dump(session / 'dependency-view.json', {'format': 'synthetic'})
        o.dump(session / 'access-manifest.json', {'format': 'synthetic'})
        o.dump(session / 'context-guard.json', {'format': 'synthetic'})
    def launch(*args):
        o.dump(tmp_path / o.w.QUEUE, queue(after_task, complete_task()))
        return {'outcome': 'blocked', 'summary': 'model stopped after delivery', 'evidence': None}
    monkeypatch.setattr(o, 'prepare', prepare)
    monkeypatch.setattr(o, 'launch', launch)
    monkeypatch.setattr(o, 'prompt', lambda *a: 'synthetic')
    run_dir = tmp_path / 'r'  # Leave room for atomic filenames below Windows' legacy path limit.
    assert o.run(tmp_path, 'unused', run_dir, 1, 5, 10) == 2
    status = o.w.read_json(run_dir / 'status.json')
    assert 'omitted' in status['summary']
