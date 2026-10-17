import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from datetime import datetime, timezone

root = Path.cwd()
run = 'private/workflow/runs/IG-2B04/coordinator-f870c628-01'
session = 'private/workflow/orchestrator/20261015T200250Z-56a048a1/001-IG-2B04-coordinator-f870c628'
def load(p): return json.loads((root / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((root / p).read_bytes()).hexdigest()
def pin(p): return dict(path=p, sha256=sha(p), bytes=(root/p).stat().st_size)
def create(p, v):
    with (root/p).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(v, f, indent=2, ensure_ascii=False); f.write('\n')
base = dict(role='coordinator', actor='ig2:001-IG-2B04-coordinator-f870c628:coordinator', task='IG-2B04',
 model='gpt-6.1-sol', reasoning='high', configuration_evidence=session+'/runtime-configuration.json',
 configuration_sha256=sha(session+'/runtime-configuration.json'), utc=datetime.now(timezone.utc).isoformat())
source_command = '.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp private/workflow/runs/IG-2B04/coordinator-f870c628-01/pytest-sources -p no:cacheprovider --tb=short'
create(run+'/source-tests.json', dict(base, summary='Exact unchanged source suite passed with approved permissions after restricted-token temporary-directory denial.',
 checks=[dict(command=source_command, exit_code=1, permissions='restricted', result='Windows WinError 5: pytest basetemp inaccessible'),
         dict(command=source_command, exit_code=0, permissions='approved', result='71 passed in 29.21s')],
 assertions_changed=False, libraries_or_acls_changed=False))
spec=importlib.util.spec_from_file_location('workflow',root/'scripts/workflow.py')
w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
q=load(w.QUEUE); queue_hash=sha(w.QUEUE)
t=next(t for t in q['tasks'] if t['id']=='IG-2B04')
assert t['status']=='planned' and not t['events']
contract=load(t['inventory_contract']['path'])
assert sha(t['inventory_contract']['path'])==t['inventory_contract']['sha256']
assert not (root/contract['output_attempt']).exists()
assert all(next(x for x in q['tasks'] if x['id']==dep)['status']=='done' for dep in t['depends'])
w.validate(q,root)
paths=list(dict.fromkeys(w.BASE_CONTEXT+['docs/work/tasks/IG-2B04.md']+t['context']))
for p in paths+t['tool_context']:
    assert w.permitted(root,p) and (root/p).is_file(),p
payload=''.join((root/p).read_text(encoding='utf-8-sig') for p in paths)
assert len(payload.encode('utf-8'))<100000
criteria=t['acceptance']
ready=dict(base, format='wgc-ready-evidence-1', summary='IG-2B04 fully refined and ready for a fresh executor claim; no product execution or semantic acceptance is claimed.',
 criteria=criteria, artifacts=[pin(run+'/execution-contract.json'),pin(run+'/input-verification.json'),pin(run+'/refinement.json'),pin(run+'/source-tests.json'),pin('docs/work/repair-context/IG-2B04-inventory-contract.md')],
 checks=[dict(command='workflow.validate(refined_queue, repository_root)',exit_code=0),dict(command='Exact executable packet/tool-context availability and size preflight',exit_code=0),dict(command=source_command,exit_code=0)],
 readiness=dict(dependencies_done=True,refinement_complete=True,exact_context_available=True,product_attempt_absent=True,source_inspection_inherited=False,semantic_acceptance_granted=False),
 next_operation='Supervisor may launch only a fresh IG-2B04 executor with observed gpt-6.1-sol/high; claim, inspect assigned originals and implement the frozen contract.',
 packet_files=[pin(p) for p in paths if p!='docs/work/tasks/IG-2B04.md'])
create(run+'/ready.json',ready)
w.transition(q,root,'IG-2B04','ready',run+'/ready.json')
assert sha(w.QUEUE)==queue_hash
(root/w.QUEUE).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for rel,body in w.views(q).items():
    p=root/rel
    if not p.exists() or p.read_text(encoding='utf-8')!=body: p.write_text(body,encoding='utf-8')
w.validate(q,root)
p=w.packet(q,root,'IG-2B04',output=False)
create(run+'/ready-packet-check.json',dict(base,summary='Actual ready packet validated without emitting or saving its context text.',
 format='wgc-ready-packet-check-1',task_status='ready',context_files=len(p['files']),context_bytes=p['text_bytes'],packet_files=p['files'],
 checks=[dict(command='workflow.packet(ready_queue, repository_root, IG-2B04, output=False)',exit_code=0)]))
print(json.dumps(dict(task='IG-2B04',status='ready',evidence=pin(run+'/ready.json'),packet_files=len(p['files']),packet_bytes=p['text_bytes'])))
