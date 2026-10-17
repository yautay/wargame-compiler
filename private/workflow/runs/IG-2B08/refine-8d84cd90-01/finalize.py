"""Freeze one coordinator handoff after required unchanged checks complete."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

root = Path.cwd()
own = 'private/workflow/runs/IG-2B08/refine-8d84cd90-01'
session = 'private/workflow/orchestrator/20261017T064446Z-f1a71866/001-IG-2B08-coordinator-8d84cd90'
sys.path.insert(0, str(root / 'scripts'))
import workflow as w


def load(rel):
    return w.read_json(root / rel)


def pin(rel):
    return {'path': rel, 'sha256': w.digest(root / rel), 'bytes': (root / rel).stat().st_size}


def main():
    config_rel = session + '/runtime-configuration.json'
    config = load(config_rel)
    assert (config['status'], config['model'], config['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
    assert w.digest(root / config_rel) == '6c19c296fa6ae7aeb13455fa4baf8e3c500b018d22bd793b17c53706c776e168'
    validation = load(own + '/full-check-02.json')
    assert validation['exit_code'] == 0 and all(v == 0 for v in validation['check_exits'].values())
    assert validation['command'] == 'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08'
    for key in ('log', 'check_result'):
        p = validation[key]
        assert w.digest(root / p['path']) == p['sha256']
    q = load(w.QUEUE)  # Check-only use; no event/history output.
    w.validate(q, root)
    t = next(t for t in q['tasks'] if t['id'] == 'IG-2B08')
    frozen = load(own + '/refined-contract.json')
    assert t['status'] == 'ready'
    assert {k: v for k, v in t.items() if k not in {'events', 'status'}} == {k: v for k, v in frozen.items() if k != 'status'}
    assert t['events'][-1]['evidence'] == own + '/ready.json'
    assert t['events'][-1]['sha256'] == w.digest(root / own / 'ready.json')
    assert all(next(x for x in q['tasks'] if x['id'] == d)['status'] == 'done' for d in t['depends'])
    assert not (root / t['inventory_contract']['attempt_root']).exists()
    # Recheck the full original control/input pin set without emitting any records.
    packet = load(session + '/packet.json')
    for p in packet['files'] + packet['control_files']:
        if p.get('sha256'):
            assert w.digest(root / p['path']) == p['sha256'], p['path']
    inputs = load(own + '/input-pins.json')
    input_pins = [inputs['baseline_inventory'], inputs['identity_registry']]
    input_pins += list(inputs['reports'].values())
    input_pins += [inputs['source']['pdf'], inputs['source']['provenance']]
    for p in input_pins:
        assert w.digest(root / p['path']) == p['sha256']
    ready = load(own + '/ready.json')
    for p in ready['artifacts']:
        assert w.digest(root / p['path']) == p['sha256']
    initial = load(own + '/checkpoint-initial.json')
    ended = datetime.now(timezone.utc)
    started = datetime.fromisoformat(initial['started_utc'])
    artifacts = [pin(own + '/' + n) for n in (
        'checkpoint-initial.json', 'input-pins.json', 'refined-contract.json',
        'refinement-check.json', 'prechecks.json', 'ready.json',
        'refine.py', 'make-ready.py', 'run-check.py', 'finalize.py',
        'full-check-01.log', 'full-check-01.json', 'full-check-02.log', 'full-check-02.json')]
    artifacts.append(validation['check_result'])
    report = {
        'format': 'wgc-inventory-coordination-1', 'task': 'IG-2B08', 'outcome': 'progress',
        'role': 'coordinator', 'actor': 'ig2:001-IG-2B08-coordinator-8d84cd90:coordinator',
        'model': 'gpt-6.1-sol', 'reasoning': 'high', 'configuration_evidence': config_rel,
        'configuration_sha256': w.digest(root / config_rel),
        'summary': 'Refined only IG-2B08 and transitioned planned to ready with immutable input/contract/readiness evidence. All original criteria/tests are preserved. The full unchanged required check passed after approved exact-command execution.',
        'readiness_evidence': pin(own + '/ready.json'), 'criteria': ready['criteria'],
        'artifacts': artifacts,
        'checks': [
            {'command': '.venv/Scripts/python.exe ' + own + '/refine.py', 'exit_code': 0,
             'result': '9 current input pins verified; other tasks unchanged; original criteria/tests retained; bounded context under 100 KB.'},
            {'command': '.venv/Scripts/python.exe -m pytest tests/sources -q --basetemp ' + own + '/source-pytest -p no:cacheprovider --tb=short',
             'exit_code': 0, 'sandbox_permissions': 'require_escalated', 'result': '71 passed in 22.52s'},
            {'command': validation['command'], 'exit_code': 0, 'sandbox_permissions': 'require_escalated',
             'execution_wrapper': '.venv/Scripts/python.exe ' + own + '/run-check.py',
             'result': validation['check_exits'], 'summaries': validation['selected_check_summaries']},
            {'command': 'git diff --check', 'exit_code': validation['check_exits']['diff_exit'],
             'basis': 'Executed unchanged by the passing full check.'},
            {'command': '.venv/Scripts/python.exe scripts/workflow.py next', 'exit_code': 0, 'result': 'IG-2B08'},
            {'command': '.venv/Scripts/python.exe ' + own + '/finalize.py', 'exit_code': 0,
             'result': 'Final selected contract, ready evidence, all input/control hashes, absent executor attempt, queue gates and passing validation pins verified.'}],
        'restricted_token_failures': [
            {'validation': 'sources suite', 'exit_code': 1, 'cause': 'WinError 5 at pytest basetemp',
             'unchanged_approved_retry': True},
            {'validation': validation['command'], 'exit_code': 1,
             'report': pin(own + '/full-check-01.json'), 'cause': 'Windows restricted-token pytest temporary-directory access',
             'unchanged_approved_retry': True}],
        'readiness': {'status': 'ready', 'assigned_physical_pages': [29, 30, 31, 32],
                      'context_only_physical_pages': [28, 33], 'full_source_pages': 44,
                      'fresh_executor_attempt': t['inventory_contract']['attempt_root'],
                      'executor_attempt_absent': True, 'independent_review_required': True},
        'product_writes': 0, 'source_inspection_claims': 0,
        'semantic_acceptance': 'Not granted; separate human/source-meaning gates remain binding.',
        'gameplay_readiness': 'Not evaluated or granted.', 'unresolved_refinement': [],
        'measurement': {'started_utc': initial['started_utc'], 'ended_utc': ended.isoformat(),
                        'wall_seconds_since_checkpoint': (ended - started).total_seconds(),
                        'input_tokens': None, 'output_tokens': None, 'operator_seconds': None,
                        'unknown_reason': 'Token counters and operator time were not exposed.'},
        'next_operation': 'Supervisor may launch one fresh sequential executor for IG-2B08. Reconfirm observed runtime and claim the frozen contract before product writes; inspect all assigned original pages and components, generate fresh serial evidence and two complete independent replays, then obtain fresh independent review.'}
    with (root / own / 'coordination.json').open('x', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(json.dumps({'outcome': 'progress', 'evidence': own + '/coordination.json',
                      'summary': 'IG-2B08 refined and ready; 71 source tests and the full required check passed. No product or semantic acceptance claimed.'}))


if __name__ == '__main__':
    main()
