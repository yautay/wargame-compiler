"""Freeze coordinator validation and readiness evidence after unchanged checks pass."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

root=Path.cwd()
run='private/workflow/runs/IG-2B04/coordinator-f870c628-01'
session='private/workflow/orchestrator/20261015T200250Z-56a048a1/001-IG-2B04-coordinator-f870c628'
def load(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
def pin(p): return dict(path=p,sha256=sha(p),bytes=(root/p).stat().st_size)
validation_path=sys.argv[1]
assert validation_path.startswith(run+'/validation-') and validation_path.endswith('/validation.json')
validation=load(validation_path)
assert all(c['exit_code']==0 and not c['permission_denied'] for c in validation['checks'])
verification=load(run+'/input-verification.json')
for p in verification['verified']:
    assert sha(p['path'])==p['sha256'], p['path']
ready=load(run+'/ready.json')
for p in ready['artifacts']:
    assert sha(p['path'])==p['sha256'],p['path']
contract=load(run+'/execution-contract.json')
assert not (root/contract['output_attempt']).exists()
q=load('docs/work/queue.json')
t=next(t for t in q['tasks'] if t['id']=='IG-2B04')
assert t['status']=='ready' and len(t['events'])==1
assert t['events'][0]['evidence']==run+'/ready.json' and t['events'][0]['sha256']==sha(run+'/ready.json')
assert t['inventory_contract']==pin(run+'/execution-contract.json')
assert t['acceptance'][:len(contract['original_acceptance'])]==contract['original_acceptance']
assert t['tests'][:len(contract['original_tests'])]==contract['original_tests']
assert t['semantic_acceptance_required']==contract['semantic_acceptance_required']
assert all(next(x for x in q['tasks'] if x['id']==dep)['status']=='done' for dep in t['depends'])
logs=[c['log'] for c in validation['checks']]
text=(root/logs[0]['path']).read_text(encoding='utf-8-sig',errors='replace')
matches=re.findall(r'\b\d+ passed[^\r\n]*',text)
assert matches
log_root=re.search(r'LOG_ROOT=(.+)',text).group(1).strip()
check_root=Path(log_root)
if not check_root.is_absolute(): check_root=root/check_root
check_relative=check_root.relative_to(root).as_posix()
assert check_relative.startswith('private/workflow/checks/active-')
check_result=load(check_relative+'/result.json')
assert all(check_result[k]==0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
end=datetime.now(timezone.utc)
start=datetime.fromisoformat(load(run+'/checkpoint.json')['utc'])
report=dict(format='wgc-coordinator-readiness-1',role='coordinator',actor='ig2:001-IG-2B04-coordinator-f870c628:coordinator',
 task='IG-2B04',model='gpt-6.1-sol',reasoning='high',configuration_evidence=session+'/runtime-configuration.json',
 configuration_sha256=sha(session+'/runtime-configuration.json'),
 summary='IG-2B04 is ready for a fresh executor. Exact accepted inputs, complete-baseline preservation, fresh original inspection/evidence, two independent replays, denominators and independent review are bound by the frozen contract. Required unchanged coordinator checks passed.',
 criteria=t['acceptance'],criteria_scope='Refinement accounts for all criteria as future execution/review obligations; no product criterion completion is asserted.',
 readiness=dict(task_status='ready',dependencies_done=True,exact_context_available=True,refinement_complete=True,fresh_product_attempt_absent=True),
 artifacts=[pin(run+'/'+p) for p in ('ready.json','ready-packet-check.json','execution-contract.json','refinement.json','input-verification.json','baseline-validation.json','source-tests.json')]+[pin(validation_path)]+logs+[pin(check_relative+'/'+p) for p in ('result.json','plan.log','dry-run.log','pytest.log','diff-check.log')],
 checks=validation['checks']+[dict(command=ready['checks'][-1]['command'],exit_code=0,result='71 passed in 29.21s; unchanged approved source suite')],
 test_summary=matches[-1],input_pin_reverification_count=len(verification['verified']),
 original_acceptance_preserved=True,original_tests_preserved=True,source_pages_inspected=[],product_deliverables_created=False,
 independent_product_review='Required in a fresh reviewer session after frozen executor delivery; none claimed.',
 human_semantic_acceptance_granted=False,
 measurements=dict(start_utc=start.isoformat(),end_utc=end.isoformat(),elapsed_wall_seconds=(end-start).total_seconds(),tokens=None,operator_time_seconds=None),
 diagnostics=dict(restricted_validation=pin(run+'/validation-feecc95ef4b2/validation.json'),reason='Windows restricted-token pytest temporary-directory access denial; exact unchanged command rerun through approved execution. No assertions, ACLs, libraries or guards changed.'),
 next_operation='Only the supervisor may launch the next fresh executor process. Claim exact frozen scope with newly observed gpt-6.1-sol/high; inspect pages13-16 and implement the contract.')
path=run+'/readiness-final.json'
with (root/path).open('x',encoding='utf-8',newline='\n') as f:
    json.dump(report,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps(dict(task='IG-2B04',status='ready',evidence=pin(path),tests=report['test_summary'],reverified_pins=report['input_pin_reverification_count'])))
