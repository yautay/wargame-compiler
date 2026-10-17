"""Freeze coordinator readiness; no executor claim or product delivery."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from wgc.sources.inventory import validate

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

c = load(RUN/'refined-contract.json')
i = load(RUN/'dependency-inputs.json')['inventory']
for p in [i['baseline_inventory'],i['identity_registry'],i['source']['pdf'],i['source']['provenance'],*i['reports'].values()]:
    assert sha(p['path']) == p['sha256']
baseline = load(i['baseline_inventory']['path'])
assert len(baseline['pages']) == 44
assert baseline['registry'] == load(i['identity_registry']['path'])
for target in i['assigned_region_metadata']:
    record = next(r for r in baseline['regions'] if r['id']==target['id'])
    assert all(record[k]==v for k,v in target.items())
validate(baseline,Path.cwd())
write('input-validation.json',{'task':'IG-2B05','baseline':i['baseline_inventory'],
    'registry':i['identity_registry'],'structural_validation':'passed','page_count':44,
    'assigned_placeholder_count':4,'assigned_physical_pages':[17,18,19,20],
    'retained_record_contents_printed':False,'source_text_extracted':False})
assert not Path(c['inventory_batch']['owned_attempt']).exists()
for p in c['context']:
    assert Path(p).is_file(),p
config = load(SESSION/'runtime-configuration.json')
assert (config['status'],config['model'],config['reasoning']) == ('confirmed','gpt-6.1-sol','high')
write('ready.json',{'task':'IG-2B05','role':'coordinator',
    'actor':'ig2:001-IG-2B05-coordinator-6daf4d13:coordinator',
    'model':config['model'],'reasoning':config['reasoning'],
    'configuration_evidence':(SESSION/'runtime-configuration.json').as_posix(),
    'configuration_sha256':sha(SESSION/'runtime-configuration.json'),
    'utc':datetime.now(timezone.utc).isoformat(),
    'summary':'IG-2B05 is refined for fresh full-page inventory work on physical pages 17-20 using the exact accepted IG-2B04 44-page baseline, registry, reports, original source and installed toolchain. Readiness grants no delivery, source-meaning acceptance or gameplay readiness.',
    'criteria':c['acceptance'],
    'artifacts':[pin(RUN/n) for n in ['prepare.py','preflight.json','dependency-inputs.json',
        'page-navigation.json','refine.py','refined-contract.json','refinement-report.json',
        'ready.py','input-validation.json']],
    'checks':[
        {'command':'.venv/Scripts/python.exe scripts/workflow.py validate','exit_code':0},
        {'command':'.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp private/workflow/runs/IG-2B05/coordinator-6daf4d13-01/pytest-sources -p no:cacheprovider --tb=short',
         'exit_code':0,'execution':'approved exact unchanged command','result':'71 passed in 15.17s'},
        {'command':'.venv/Scripts/python.exe private/workflow/runs/IG-2B05/coordinator-6daf4d13-01/ready.py',
         'exit_code':0,'scope':'accepted baseline structural validation, byte pins, assigned IDs, exact context and fresh output absence'}],
    'gates':{'direct_dependency_done':'IG-2B04','complete_baseline_and_registry_verified':True,
        'original_criteria_and_tests_preserved':True,'other_task_records_unchanged':True,
        'executor_attempt_absent':True,'fresh_executor_inspection_required':True,
        'fresh_independent_review_required':True,'human_semantic_gate_unchanged':True},
    'restricted_validation':{'command':'.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp private/workflow/runs/IG-2B05/coordinator-6daf4d13-01/pytest-sources -p no:cacheprovider --tb=short',
        'exit_code':1,'reason':'Windows restricted-token Access Denied on pytest basetemp; exact approved rerun passed without test changes.'},
    'next_operation':'Supervisor prepares a new executor session and runtime evidence. Executor claims only the absent pinned attempt, reinspects assigned original pages and builds the new immutable batch. No process is launched by this coordinator.',
    'measurement':{'input_tokens':None,'output_tokens':None,'operator_seconds':None,
        'unknown_reason':'Not exposed to this role.'}})
print(json.dumps({'task':'IG-2B05','ready_evidence':(RUN/'ready.json').as_posix(),
                  'sha256':sha(RUN/'ready.json'),'structural_input_validation':'passed'}))
