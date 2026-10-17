"""Freeze actual coordinator validation evidence without changing the ready task."""
import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime, timezone

RUN = Path('private/workflow/runs/IG-2B05/coordinator-6daf4d13-01')
SESSION = Path('private/workflow/orchestrator/20261016T150146Z-33452c9a/001-IG-2B05-coordinator-6daf4d13')

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pin(p):
    p = Path(p)
    return {'path':p.as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}

def write(name,obj):
    with (RUN/name).open('x',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
        f.write('\n')

all_pins = []
results = {}
for mode, folder in [
    ('restricted','private/workflow/checks/active-b8f52bd603b74bb9b6ba69b1bb824597'),
    ('approved','private/workflow/checks/active-57814c07301e4f7aa1fead4ab8198a76')]:
    dst = RUN/f'checks-{mode}'
    dst.mkdir(exist_ok=False)
    for name in ['result.json','plan.log','dry-run.log','pytest.log','diff-check.log']:
        source = Path(folder)/name
        shutil.copyfile(source,dst/name)
        assert sha(source)==sha(dst/name)
        all_pins.append(pin(dst/name))
    results[mode] = load(dst/'result.json')
assert all(results['approved'][k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
assert results['restricted']['tests_exit']==1
log = (RUN/'checks-approved/pytest.log').read_text(encoding='utf-8-sig')
assert '256 passed in 32.95s' in log
dry = load(RUN/'checks-approved/dry-run.log')
assert dry['result']=='passed' and dry['context_bytes']==92610
ready = load(RUN/'ready.json')
for p in ready['artifacts']:
    assert sha(p['path'])==p['sha256']
contract = load(RUN/'refined-contract.json')
q = load('docs/work/queue.json')
t = next(t for t in q['tasks'] if t['id']=='IG-2B05')
assert t['status']=='ready'
assert all(t[k]==v for k,v in contract.items() if k!='status')
event = t['events'][-1]
assert event['to']=='ready' and event['evidence']==(RUN/'ready.json').as_posix()
assert event['sha256']==sha(RUN/'ready.json')
assert not Path(contract['inventory_batch']['owned_attempt']).exists()
original = load(SESSION/'task.json')
for k in ['acceptance','tests']:
    assert t[k][:len(original[k])]==original[k]
assert t['semantic_acceptance_required']==original['semantic_acceptance_required']
inputs = load(RUN/'dependency-inputs.json')['inventory']
for p in [inputs['baseline_inventory'],inputs['identity_registry'],inputs['source']['pdf'],
          inputs['source']['provenance'],*inputs['reports'].values()]:
    assert sha(p['path'])==p['sha256']
config = load(SESSION/'runtime-configuration.json')
assert (config['status'],config['model'],config['reasoning'])==('confirmed','gpt-6.1-sol','high')
binding = {'actor':'ig2:001-IG-2B05-coordinator-6daf4d13:coordinator',
    'model':config['model'],'reasoning':config['reasoning'],
    'configuration_evidence':(SESSION/'runtime-configuration.json').as_posix(),
    'configuration_sha256':sha(SESSION/'runtime-configuration.json')}
checks = [*ready['checks'],
    {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B05','exit_code':0,
     'execution':'approved exact unchanged command','result':'256 passed in 32.95s; plan, packet dry-run and diff checks passed',
     'report':pin(RUN/'checks-approved/result.json')},
    {'command':'git diff --check','exit_code':0,'execution':'also run by unchanged approved scripts/check.ps1',
     'report':pin(RUN/'checks-approved/diff-check.log')}]
write('checkpoint-final.json',{'task':'IG-2B05','attempt':RUN.name,'role':'coordinator',**binding,
    'utc':datetime.now(timezone.utc).isoformat(),'base':pin(RUN/'preflight.json'),
    'input_packet':pin(SESSION/'packet.json'),'refined_contract':pin(RUN/'refined-contract.json'),
    'changed_planning_hashes':[pin(p) for p in ['docs/work/queue.json','docs/work/context-policy.json',
        'docs/work/tasks/IG-2B05.md','docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md']],
    'completed':['Selected contract refinement','Exact accepted input pins and context available',
        'Original assigned-page coordinator navigation','Readiness transition','Unchanged approved validation'],
    'checks':checks,'blocker':None,'product_delivery':False,
    'next_operation':'Supervisor dispatches the ready IG-2B05 executor with fresh observed runtime metadata.'})
write('readiness-verification.json',{'format':'wgc-coordinator-readiness-verification-1',
    'task':'IG-2B05','role':'coordinator',**binding,'status':'ready',
    'summary':'Refined IG-2B05 pages 17-20 with exact accepted IG-2B04 inputs, full-sidecar preservation, fresh source evidence and two complete replay requirements, independent review and unchanged human gates. All required coordinator checks passed through exact approved commands.',
    'criteria':contract['acceptance'],
    'artifacts':[*ready['artifacts'],pin(RUN/'ready.json'),pin(RUN/'finalize.py'),
        pin(RUN/'checkpoint-final.json'),*all_pins],
    'checks':checks,'readiness_event_evidence':pin(RUN/'ready.json'),
    'packet_check':{'context_files':dry['context_files'],'context_bytes':dry['context_bytes'],
                    'queue_unchanged':dry['queue_unchanged'],'models_launched':0},
    'preservation':{'original_acceptance_and_tests_preserved_verbatim':True,
        'human_semantic_gate_unchanged':True,'other_task_records_unchanged':True,
        'accepted_input_pins_reverified':True,'executor_attempt_still_absent':True},
    'restricted_check':{'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B05',
        'exit_code':1,'report':pin(RUN/'checks-restricted/result.json'),
        'cause':'Windows restricted-token pytest temporary-directory Access Denied. Exact unchanged approved rerun passed; no test, assertion, ACL or library changes.'},
    'limitations':['No executor inventory deliverable created or accepted.',
        'Fresh executor inspection/evidence/replays and fresh independent review remain required.',
        'No human semantic acceptance or executable/gameplay readiness is asserted.'],
    'next_operation':'Supervisor launches the next authorized executor session; this coordinator stops after this role.',
    'measurement':{'input_tokens':None,'output_tokens':None,'operator_seconds':None,
        'unknown_reason':'Not exposed to this role.'}})
print(json.dumps({'task':'IG-2B05','status':'ready','evidence':(RUN/'readiness-verification.json').as_posix(),
    'sha256':sha(RUN/'readiness-verification.json'),'source_tests_passed':71,'repository_tests_passed':256,
    'context_bytes':dry['context_bytes']}))
