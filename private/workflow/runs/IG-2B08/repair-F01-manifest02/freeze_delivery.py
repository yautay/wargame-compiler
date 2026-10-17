"""Freeze only this bounded F01 repair, retaining all immutable input pins."""
from datetime import datetime,timezone
import json
from build_inventory import ROOT,SESSION,TASK,CONTRACT,SPECS,load,write,pin,metadata,old_preservation

def main():
    meta=metadata();config=load(SESSION/'runtime-configuration.json')
    assert (config['status'],config['model'],config['reasoning'])==('confirmed','gpt-6.1-sol','high')
    assert meta['configuration_sha256']=='8fe2d32465346ef58ac7c4308399eeb2123ef6d2c6be9039a9c9ee5df160375a'
    assert not (ROOT/'delivery.json').exists()
    # Internal selected-contract check only: no queue/event output.
    selected=next(t for t in load('docs/work/queue.json')['tasks'] if t['id']=='IG-2B08')
    assert selected['status']=='in_progress'
    for field,value in TASK.items():
        if field!='status':assert selected[field]==value,field
    for control in load(SESSION/'packet.json')['control_files']:
        assert pin(control['path'])['sha256']==control['sha256']
    scope=load(TASK['context_recovery_authorization']['scope']['path'])
    assert pin(scope['preserve_manifest']['path'])==scope['preserve_manifest']
    assert old_preservation()==7808
    source=load(ROOT/'source-suite-execution.json');full=load(ROOT/'full-check-execution.json')
    assert source['attempts'][-1]['exit_code']==full['attempts'][-1]['exit_code']==0
    cli=load(ROOT/'source-cli-validation.json');assert all(c['exit_code']==0 for c in cli['checks'])
    qa=load(ROOT/'visual-qa.json');assert qa['all_sheets_inspected'] and qa['exact_page33_context_inspected']
    batch=load(ROOT/'batch-verification.json');assert batch['exit_code']==0
    arrow=load(ROOT/'arrow-completeness-report.json');assert arrow['exit_code']==0 and arrow['old_crop_rejected']
    delta=load(ROOT/'repair-delta.json');assert delta['exit_code']==0 and delta['changed_region_count']==1
    diff=load(ROOT/'diff-check-execution.json');assert diff['exit_code']==0
    names=('final-verified','replay-1','replay-2')
    coverage=load(ROOT/'coverage-report.json');preservation=load(ROOT/'preservation-report.json')
    checks=[
        {'command':'Exact packet/control/repair-input/runtime pin verification, absent owned directory and selected contract/dependency checks before claim','exit_code':0},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/inspect_originals.py','exit_code':0},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/build_inventory.py prepare','exit_code':0},
        *[{'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/build_inventory.py {name}','exit_code':0} for name in names],
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/probe_geometry.py','exit_code':0,'evidence':pin(ROOT/'geometric-content-probe.json')},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/check_arrow_completeness.py','exit_code':0,'evidence':pin(ROOT/'arrow-completeness-report.json')},
        {'command':source['command'],'exit_code':0,'execution':'Approved unchanged exact command after observed restricted-token WinError 5.','evidence':pin(ROOT/'source-suite-execution.json')},
        *cli['checks'],
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/verify_batch.py','exit_code':0,'evidence':pin(ROOT/'batch-verification.json')},
        {'command':full['command'],'exit_code':0,'execution':'Approved unchanged command; 288 tests passed.','evidence':pin(ROOT/'full-check-execution.json')},
        {'command':'git diff --check','exit_code':0,'evidence':pin(ROOT/'diff-check-execution.json')},
        {'command':'Fresh assigned-original, all proposed boundary/component and exact page-33 visual inspection','exit_code':0,'evidence':pin(ROOT/'visual-qa.json')},
        {'command':'Final selected ownership/contract/runtime/control checks and all 7808 preserved input artifact hashes','exit_code':0},
    ]
    started=load(ROOT/'checkpoint.json')['started_utc'];ended=datetime.now(timezone.utc)
    measurement={'started_utc':started,'ended_utc':ended.isoformat(),'elapsed_wall_seconds':(ended-datetime.fromisoformat(started)).total_seconds(),
        'input_tokens':None,'output_tokens':None,'operator_seconds':None,'unknown_reason':'Token usage and operator time were not exposed.',
        'executor':meta['actor'],'reviewer':None,'observed_model':config['model'],'observed_reasoning':config['reasoning']}
    validation={**meta,'summary':'Bounded F01 repair passed unchanged required suites, three source-backed CLI validations, complete serial replay/preservation/index checks and source-bound arrow regression.',
        'checks':checks,'restricted_token_failure':source['attempts'][0],
        'approved_execution':{'source_suite':pin(ROOT/'source-suite-execution.json'),'full_check':pin(ROOT/'full-check-execution.json')},
        'verifier_development':pin(ROOT/'verifier-development.json'),
        'preserved_input_artifacts_verified':7808,'repair_finding':'F01','repair_cycles_in_this_session':1,
        'unresolved_review_findings':'Fresh independent review pending; no acceptance granted.',
        'source_meaning':'Unaccepted; machine transcription and descriptive gaps remain.','semantic_acceptance_granted':False,'executable_readiness':False,'measurement':measurement}
    write(ROOT/'validation-report.json',validation)
    handoff=f'''# IG-2B08 F01 repair for independent review

The page-30 Advance arrow detail now uses [90,344,143,476] PDF points.
Fresh original and final/replay detail inspection accounts for both complete cyan
curves and arrowheads and the black forward arrow, including source point [94,367].
The source-bound regression checks 199 left-cyan, 194 right-cyan and 458 black-arrow
reference pixels in the intended detail in all three sets. It rejects the old crop
and separate tail, head and shaft truncations that a single witness cannot catch.

Only this zero-denominator detail selection changed. All unrelated selections,
primary tiles, registry history, identities, reading order, links and normalized
non-target evidence match the frozen candidate. All accepted 44-page baseline
objects except the four retired active placeholders remain unchanged. All 7,808
current preservation-manifest artifacts were hash-verified before writes and freeze.

Final and both independent replays regenerated all 269 regions serially from the
accepted baseline and persisted registry. The 183 assigned primary regions and
86 new context/detail regions remain separate; context contributes zero denominator.
Fresh assigned originals, proposed boundaries/components and the exact page-33
[45,50,306,80] context were inspected. Page 28 was reference-only through the prepared
dependency projection. Page-33 access never expanded beyond the authorized crop.

Checks passed: 71 unchanged source tests, 288 full-suite tests, all three source-backed
CLI validations, complete batch/index/replay preservation checks, arrow regression
and git diff --check. Approved exact-command execution resolved the observed Windows
restricted-token pytest temporary-directory denial without changing tests, guards,
assertions, ACLs or libraries. See validation-report.json for commands and evidence.

The fresh gap probe reports zero unassigned word centers and 42 thresholded ink
pixels outside primary regions. These and other geometric spacing remain gaps;
machine transcription, counter glyphs and source meaning remain unaccepted, and
formal semantics remain unprocessed. No semantic acceptance or gameplay readiness
is granted. Fresh independent review of every original/appended criterion and this
exhaustive frozen artifact set is the next operation. Only the supervisor launches it.
'''
    (ROOT/'delivery-handoff.md').write_text(handoff,encoding='utf-8',newline='\n')
    pending=[c for c in TASK['acceptance'] if c.startswith('A fresh independent reviewer') or c.startswith('Independent review compares')]
    write(ROOT/'checkpoint-delivery.json',{**meta,'task':'IG-2B08','attempt':ROOT.name,'summary':'Bounded F01 repair ready for frozen independent review.',
        'input_packet':pin(SESSION/'packet.json'),'repair_scope':TASK['repair_authorization']['scope'],
        'changed_file_hashes':[pin(ROOT/n/'inventory.json') for n in names],
        'completed_criteria':[c for c in TASK['acceptance'] if c not in pending],'pending_criteria':pending,
        'commands':checks,'blocker':None,'measurement':measurement,'next_operation':'Transition frozen delivery to review; stop this executor role.'})
    index=load(ROOT/'source-pins.json');current={p['path']:p for p in index['current_reports']}
    for name in ('original-access.json','validation-report.json','delivery-handoff.md','checkpoint-delivery.json','visual-qa.json','source-cli-validation.json','source-suite-execution.json','full-check-execution.json','diff-check-execution.json','verifier-development.json'):
        p=pin(ROOT/name);current[p['path']]=p
    index['current_reports']=list(current.values())
    artifacts={p['path']:p for p in index['artifacts']}
    for p in qa['artifacts']:artifacts[p['path']]=p
    index['artifacts']=list(artifacts.values());write(ROOT/'source-pins.json',index)
    artifacts={}
    def collect(o):
        if isinstance(o,dict):
            if 'path' in o and 'sha256' in o:
                p=pin(o['path']);assert p['sha256']==o['sha256'],o['path']
                if 'bytes' in o:assert p['bytes']==o['bytes']
                artifacts[p['path']]=p
            for v in o.values():collect(v)
        elif isinstance(o,list):
            for v in o:collect(v)
    for o in (index,validation,preservation,qa,full,source,delta,arrow):collect(o)
    collect(TASK['repair_authorization']);collect(TASK['context_recovery_authorization'])
    collect(scope['preserve_manifest'])
    for name in ('runtime-configuration.json','task.json','packet.json','references.json','access-manifest.json','dependency-view.json','search-manifest.json'):
        p=pin(SESSION/name);artifacts[p['path']]=p
    for n in names:
        for file in ('inventory.json','identity-registry.json'):
            p=pin(ROOT/n/file);artifacts[p['path']]=p
    # Exact owned root only; no recursive private tree search or pytest scratch.
    for file in ROOT.iterdir():
        if file.is_file() and file.name!='delivery.json':
            p=pin(file);artifacts[p['path']]=p
    for path in TASK['outputs']:assert path in artifacts,path
    ordered=[artifacts[path] for path in sorted(artifacts)]
    for p in ordered:assert pin(p['path'])==p
    envelope={**meta,'task':'IG-2B08','summary':'F01 arrow-component evidence repaired at fresh paths; complete final and two serial replays, baseline preservation, source-bound regression and unchanged required checks passed. Independent review requested.',
        'criteria':TASK['acceptance'],'criteria_assessment':{'executor_deliverables':'Submitted for independent review.','independent_review':'Pending in fresh supervisor-launched role.','human_semantic_acceptance':'Not granted; not required for this physical inventory task.','executable_readiness':'Unverified.'},
        'artifacts':ordered,'checks':checks,'input_packet':pin(SESSION/'packet.json'),'repair_scope':TASK['repair_authorization']['scope'],'measurement':measurement,
        'denominators':{'full_source':coverage['denominator_regions'],'assigned_four_pages':coverage['assigned_four_page']['denominator_regions'],'inherited_nonassigned':coverage['inherited_nonassigned']['denominator_regions'],'new_context_regions':coverage['context_only']['new_regions'],'context_contribution':0},
        'semantic_acceptance_granted':False,'executable_readiness':False,'preserved_input_artifact_count':7808,'preservation_manifest':scope['preserve_manifest'],
        'excluded_scratch':['source-pytest/','__pycache__/'],'next_operation':'Fresh independent reviewer checks all original/appended criteria against this exact exhaustive frozen artifact set.'}
    write(ROOT/'delivery.json',envelope)
    for p in envelope['artifacts']:assert pin(p['path'])==p
    assert old_preservation()==7808
    print(json.dumps({'delivery':pin(ROOT/'delivery.json'),'artifact_count':len(ordered),'preserved_input_artifacts':7808}))

if __name__=='__main__':main()
