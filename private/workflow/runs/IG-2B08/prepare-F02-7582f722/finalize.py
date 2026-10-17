"""Freeze coordinator checks and bind the final authorization without transitioning."""
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path.cwd() / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

prep = Path('private/workflow/runs/IG-2B08/prepare-F02-7582f722')
session = Path('private/workflow/orchestrator/20261017T111422Z-80dfde30/002-IG-2B08-coordinator-7582f722')

def pin(path):
    path = Path(path)
    return {'path': path.as_posix(), 'sha256': w.digest(path), 'bytes': path.stat().st_size}

def write(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')

prior = w.read_json(prep/'authorization.json')
identity = {k:prior[k] for k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256')}
o.configuration_binding(Path.cwd(), Path.cwd()/session, prior)
check_command = 'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08'
check_records = []
for suffix, code in [('full-check.log',1),('full-check-approved.log',0)]:
    path = prep/suffix
    text = path.read_text(encoding='utf-8-sig')
    log_root = Path(re.search(r'LOG_ROOT=([^\r\n]+)', text).group(1).strip())
    result_path = log_root/'result.json'
    result = w.read_json(result_path)
    if code == 0:
        assert all(result[k] == 0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
    else:
        assert result['plan_exit'] == 0 and result['diff_exit'] == 0
        assert 'PermissionError' in text and 'WinError 5' in text
    check_records.append({'command':check_command,'exit_code':code,'execution':'approved exact unchanged command' if code == 0 else 'restricted-token initial attempt',
                          'log':pin(path),'result':pin(result_path.relative_to(Path.cwd())),
                          'selected_exits':{k:result[k] for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit')},
                          'reason':None if code == 0 else 'Packet dry-run exceeded 100 KB; compact index refinement resolved it. Pytest restricted-token PermissionError/WinError 5 resolved by approved exact-command execution.'})
diff_log = prep/'diff-check.log'
check_records.append({'command':'git diff --check','exit_code':0,'log':pin(diff_log)})
scope = w.read_json(prep/'repair-scope.json')
delivery_pin = scope['immutable_delivery']
assert w.digest(delivery_pin['path']) == delivery_pin['sha256']
delivery = w.read_json(delivery_pin['path'])
preserve_pin = scope['preserve_manifest']
assert w.digest(preserve_pin['path']) == preserve_pin['sha256']
preserved = w.read_json(preserve_pin['path'])['artifacts']
for item in delivery['artifacts'] + preserved:
    assert w.digest(item['path']) == item['sha256'], 'Frozen artifact changed'
assert not Path(scope['attempt']).exists()
check_records.append({'command':'Reverify complete immutable delivery and preservation-manifest hashes; verify fresh attempt absent',
                      'exit_code':0,'delivery_artifacts':len(delivery['artifacts']),'preserved_artifacts':len(preserved),'attempt_absent':True})
checks_path = prep/'coordinator-checks.json'
write(checks_path, dict(identity, task='IG-2B08', utc=datetime.now(timezone.utc).isoformat(), checks=check_records,
                        packet_refinement=pin(prep/'packet-refinement.json'),
                        coordinator_validation_attempts=[{'command':'Initial coordinator evidence finalizer','exit_code':1,
                            'reason':'Coordinator wrapper passed a relative session path to the absolute-path configuration binding API. Corrected wrapper argument before any evidence or queue write; repository tests unchanged.',
                            'log':pin(prep/'finalize.log')}],
                        semantic_acceptance_granted=False, executable_readiness=False))
final = copy.deepcopy(prior)
final['utc'] = datetime.now(timezone.utc).isoformat()
final['summary'] = 'Current F02 bounded repair authorized at an absent owned attempt. Exact acceptance/tests, status and events are preserved; compact packet, approved unchanged repository check, diff check and frozen-input hashes verified. No task execution, acceptance or downstream readiness is granted.'
final['checks'] = prior['checks'] + [c for c in check_records if c['exit_code'] == 0]
final['artifacts'] = prior['artifacts'] + [pin(prep/'authorization.json'),pin(checks_path)]
final_path = prep/'authorization-verified.json'
write(final_path, final)
o.configuration_binding(Path.cwd(), Path.cwd()/session, final)
lock = Path('private/workflow/queue.lock')
fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    queue_path = Path('docs/work/queue.json')
    before_hash = w.digest(queue_path)
    before = w.read_json(queue_path)
    after = copy.deepcopy(before)
    task = next(t for t in after['tasks'] if t['id']=='IG-2B08')
    old = next(t for t in before['tasks'] if t['id']=='IG-2B08')
    task['repair_authorization']['evidence'] = pin(final_path)
    o.check_queue_delta(before, after, old, 'coordinator', outcome='progress')
    assert task['events'] == old['events'] and task['status'] == 'changes_requested'
    assert task['acceptance'] == scope['acceptance'] and task['tests'] == scope['tests']
    policy_path = Path('docs/work/context-policy.json')
    policy = w.read_json(policy_path)
    assert final_path.as_posix() not in policy['allow']
    policy['allow'].append(final_path.as_posix())
    policy_temp = policy_path.with_name('context-policy.F02-final.pending.json')
    queue_temp = queue_path.with_name('queue.F02-final.pending.json')
    write(policy_temp,policy)
    write(queue_temp,after)
    assert w.digest(queue_path) == before_hash
    os.replace(policy_temp,policy_path)
    os.replace(queue_temp,queue_path)
    w.validate(after, Path.cwd(), check_views=False)
    w.render(after,Path.cwd())
    w.validate(after,Path.cwd())
    o.verify_repair_authorization(Path.cwd(),task)
    write(prep/'final-verification.json',dict(identity, task='IG-2B08', status='changes_requested', events_unchanged=True,
          acceptance_unchanged=True, tests_unchanged=True, attempt_absent=True, authorization=pin(final_path),
          checks=[{'command':'Final coordinator queue delta, rendered-view and repair-authorization validation','exit_code':0}]))
    print(json.dumps({'outcome':'progress','evidence':final_path.as_posix(),'status':'changes_requested','attempt_absent':True,
                      'check_exit':0,'diff_check_exit':0,'delivery_hash_count':len(delivery['artifacts']),'preserved_hash_count':len(preserved)}))
finally:
    os.close(fd)
    lock.unlink()
