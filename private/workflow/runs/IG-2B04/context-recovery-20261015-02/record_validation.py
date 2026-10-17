"""Record actual prelaunch checks without claiming an unrefined task is ready."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

HERE = Path(__file__).resolve().parent


def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


assert not (HERE / 'validation.json').exists()
check = 'private/workflow/checks/active-a56df8c417b34d12a0a59b03e8e93cb2/'
result = w.read_json(ROOT / check / 'result.json')
assert {k: result[k] for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit']} == {
    'plan_exit':0, 'dry_run_exit':1, 'tests_exit':0, 'diff_exit':0}
assert '227 passed' in (ROOT / check / 'pytest.log').read_text(encoding='utf-8-sig')
q = w.read_json(ROOT / w.QUEUE)
w.validate(q, ROOT)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'planned' and t['events'] == []
recovery = t['context_recovery_authorization']
for p in [*recovery.values(), *w.read_json(ROOT / recovery['scope']['path'])['preserved']]:
    assert w.digest(ROOT / p['path']) == p['sha256']
tested = ['scripts/context_guard.py', 'scripts/task_access.py', 'scripts/search_task.py',
          'scripts/dependency_context.py', 'scripts/orchestrate_ig2.py',
          'tests/test_task_access.py', 'tests/test_task_search.py',
          'tests/test_dependency_context.py', 'tests/test_orchestrator.py', 'pyproject.toml']
o.dump(HERE / 'validation.json', {
    'format':'wgc-context-recovery-validation-1', 'observed_utc':o.utc(), 'task':'IG-2B04',
    'actor':'operator-b04-context-access-recovery-20261015', 'model':None, 'reasoning':None,
    'configuration_evidence':'Builder configuration is not exposed. Test processes are deterministic; no Sol/high claim.',
    'checks':[{'command':'scripts/check.ps1 -Task IG-2B04 (pinned process environment; approved normal-user token)',
               'exit_code':1, 'results':result, 'tests_passed':227,
               'interpretation':'Queue, tests and diff checks pass. Execution dry-run correctly rejects planned/unrefined B04; no readiness is fabricated.'}],
    'check_artifacts':[pin(check + p) for p in ['result.json','plan.log','dry-run.log','pytest.log','diff-check.log']],
    'tested_tooling':[pin(p) for p in tested],
    'preflight':pin(str((HERE/'preflight-result.json').relative_to(ROOT)).replace('\\','/')),
    'independent_review':{'reviewer':'/root/review_orchestrator','outcome':'no_open_findings',
        'mode':'Inspection only; no acceptance or claimed source review.',
        'guard_sha256':'80d177bf7138e1089421b80c26d6646527734d69c8af26b4495f94d707e36898',
        'tests_sha256':'92df27cd4848fff0793ba273b2221e9e8ba0c66dd60c93ac9a69cb84068bee31'},
    'source_pages_inspected':[], 'readiness_granted':False, 'semantic_acceptance_granted':False,
    'next_operation':'Start one fresh coordinator through the existing sequential IG-2 supervisor; require observed Sol/high startup before claims.'})
assert w.digest(ROOT/'scripts/context_guard.py') == '80d177bf7138e1089421b80c26d6646527734d69c8af26b4495f94d707e36898'
assert w.digest(ROOT/'tests/test_task_access.py') == '92df27cd4848fff0793ba273b2221e9e8ba0c66dd60c93ac9a69cb84068bee31'
print('Recorded 227 passing tests, passing queue/diff checks, expected planned-task dry-run gate and final independent tooling review.')
