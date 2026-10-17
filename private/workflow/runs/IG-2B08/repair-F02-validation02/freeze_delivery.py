"""Freeze only this bounded F02 repair, retaining all immutable input pins."""
from datetime import datetime,timezone
import json
from build_inventory import ROOT,SESSION,TASK,CONTRACT,SPECS,load,write,pin,metadata,old_preservation

def main():
    meta=metadata();config=load(SESSION/'runtime-configuration.json')
    assert (config['status'],config['model'],config['reasoning'])==('confirmed','gpt-6.1-sol','high')
    assert meta['configuration_sha256']=='6e1c13e8310a1dc9469b4807a1d9fb139e5b898213713dbf5ded7fb98bc3c6ad'
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
    assert old_preservation()==12033
    source=load(ROOT/'source-suite-execution.json');full=load(ROOT/'full-check-execution.json')
    assert source['attempts'][-1]['exit_code']==full['attempts'][-1]['exit_code']==0
    cli=load(ROOT/'source-cli-validation.json');assert all(c['exit_code']==0 for c in cli['checks'])
    qa=load(ROOT/'visual-qa.json');assert qa['all_sheets_inspected'] and qa['exact_page33_context_inspected']
    batch=load(ROOT/'batch-verification.json');assert batch['exit_code']==0
    arrow=load(ROOT/'arrow-completeness-report.json');assert arrow['exit_code']==0 and arrow['old_crop_rejected']
    hit=load(ROOT/'F02-completeness-report.json');assert hit['exit_code']==0 and hit['old_crop_rejected']
    delta=load(ROOT/'repair-delta.json');assert delta['exit_code']==0 and delta['changed_region_count']==1
    diff=load(ROOT/'diff-check-execution.json');assert diff['exit_code']==0
    names=('final-verified','replay-1','replay-2')
    coverage=load(ROOT/'coverage-report.json');preservation=load(ROOT/'preservation-report.json')
    checks=[
        {'command':'Exact packet/control/repair-input/runtime pin verification, absent owned directory and selected contract/dependency checks before claim','exit_code':0},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/inspect_originals.py','exit_code':0},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/build_inventory.py prepare','exit_code':0},
        *[{'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/build_inventory.py {name}','exit_code':0} for name in names],
        *[{'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/reconcile_reading_order.py {name}','exit_code':0,'evidence':pin(ROOT/f'order-reconciliation-{name}.json')} for name in ('author',*names)],
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/probe_geometry.py','exit_code':0,'evidence':pin(ROOT/'geometric-content-probe.json')},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/check_arrow_completeness.py','exit_code':0,'evidence':pin(ROOT/'arrow-completeness-report.json')},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/check_hit_completeness.py','exit_code':0,'evidence':pin(ROOT/'F02-completeness-report.json')},
        {'command':source['command'],'exit_code':0,'execution':'Approved unchanged exact command after observed restricted-token WinError 5.','evidence':pin(ROOT/'source-suite-execution.json')},
        *cli['checks'],
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/verify_batch.py','exit_code':0,'evidence':pin(ROOT/'batch-verification.json')},
        {'command':full['command'],'exit_code':0,'execution':'Unchanged required check command; exact attempts and observed counts in execution evidence.','evidence':pin(ROOT/'full-check-execution.json')},
        {'command':'git diff --check','exit_code':0,'evidence':pin(ROOT/'diff-check-execution.json')},
        {'command':'Fresh assigned-original, all proposed boundary/component and exact page-33 visual inspection','exit_code':0,'evidence':pin(ROOT/'visual-qa.json')},
        {'command':'Final selected ownership/contract/runtime/control checks and all 12033 preserved input artifact hashes','exit_code':0},
    ]
    started=load(ROOT/'checkpoint.json')['started_utc'];ended=datetime.now(timezone.utc)
    measurement={'started_utc':started,'ended_utc':ended.isoformat(),'elapsed_wall_seconds':(ended-datetime.fromisoformat(started)).total_seconds(),
        'input_tokens':None,'output_tokens':None,'operator_seconds':None,'unknown_reason':'Token usage and operator time were not exposed.',
        'executor':meta['actor'],'reviewer':None,'observed_model':config['model'],'observed_reasoning':config['reasoning']}
    validation={**meta,'summary':'Bounded F02 repair passed unchanged required suites, three source-backed CLI validations, complete serial replay/preservation/index checks and source-bound F02 marker and preserved F01 arrow regressions.',
        'checks':checks,'restricted_token_failure':source['attempts'][0],
        'approved_execution':{'source_suite':pin(ROOT/'source-suite-execution.json'),'full_check':pin(ROOT/'full-check-execution.json')},
        'verifier_development':pin(ROOT/'verifier-development.json'),
        'superseded_first_pass':pin(ROOT/'superseded-generation-index.json'),
        'F02_initial_regression_failure':'The strict full-frame mask rejected six top-edge pixels; expanded only the F02 top edge 496 to 495 and bottom edge 527 to 528 in two successive corrections, regenerated complete sets after each, and retained all strict assertions. The final exact-crop preflight passed every mask pixel.',
        'preserved_input_artifacts_verified':12033,'repair_finding':'F02','repair_cycles_in_this_session':1,'strict_F02_mask_failures':2,'local_F02_geometry_corrections':2,
        'defects_by_severity':{'addressed':{'medium':1},'fresh_independent_review_pending':True},
        'assembly_notes':pin(ROOT/'assembly-notes.json'),
        'toolchain_observations':pin(ROOT/'toolchain-comparison.json'),
        'F02_final_exact_crop_preflight':pin(ROOT/'proposal-preflight.json'),
        'reading_order_reconciliation':[pin(ROOT/f'order-reconciliation-{name}.json') for name in ('author',*names)],
        'reading_order_failure_and_response':'The margin changed geometry-sort position; preserve reviewed reading order explicitly. Reconstructed author/final/replays separately from baseline and complete generated evidence; only order and root revision changed; strict comparison retained.',
        'unresolved_review_findings':'Fresh independent review pending; no acceptance granted.',
        'source_meaning':'Unaccepted; machine transcription and descriptive gaps remain.','semantic_acceptance_granted':False,'executable_readiness':False,'measurement':measurement}
    write(ROOT/'validation-report.json',validation)
    handoff=f'''# IG-2B08 F02 repair for independent review

The page-29 Celt C hit-marker detail now uses [106,495,148,528] PDF points.
Fresh source-bound checks retain the complete visible digit 4 and marker frame,
including the reported 51-pixel right-stem core, in the intended detail in all
three complete generated sets. The original [106,496,133,527] crop and separate
base/frame truncations are rejected. The resolved F01 full-arrow masks remain
unchanged and pass in all three sets.

Only this zero-denominator F02 detail selection/revision and its derivatives
changed from the reviewed F01 candidate. Primary tiles, unrelated selections,
identities, registry history, reading order, links and normalized non-target
evidence are unchanged. The complete accepted 44-page baseline is preserved
except for the four explicitly retired active placeholders. All 12,033 preserved
artifact pins were checked before writes and again at freeze.

Final and both independent replays regenerated all 269 regions serially from
the accepted baseline and persisted author registry. Assigned primary regions,
inherited regions and context/detail regions remain separate. Context contributes
zero denominator. Every assigned original and proposed boundary/component was
freshly inspected. Page 28 was reference-only through the prepared dependency
projection. Page 33 was clipped to [45,50,306,80] before text/pixels were released;
only the two authorized continuation lines were inspected.

The unchanged source suite, required repository check, three task-bound source
CLI validators, complete batch/preservation/index verifier, F02/F01 regressions,
and git diff --check passed. Exact commands, exits, private log pins and approved
execution evidence are in validation-report.json. Tests/assertions, guards, ACLs,
libraries and global configuration were not changed.

Geometric gaps remain explicit and never count as represented content. Machine
transcription and descriptive gaps remain, formal semantics are unprocessed, and
no human semantic acceptance or executable gameplay readiness is granted. Fresh
independent review of every original/appended criterion and the exhaustive frozen
artifact set is pending. Only the supervisor launches the next role.
'''
    (ROOT/'delivery-handoff.md').write_text(handoff,encoding='utf-8',newline='\n')
    pending=[c for c in TASK['acceptance'] if c.startswith('A fresh independent reviewer') or c.startswith('Independent review compares')]
    write(ROOT/'checkpoint-delivery.json',{**meta,'task':'IG-2B08','attempt':ROOT.name,'summary':'Bounded F02 repair ready for frozen independent review.',
        'input_packet':pin(SESSION/'packet.json'),'repair_scope':TASK['repair_authorization']['scope'],
        'changed_file_hashes':[pin(ROOT/n/'inventory.json') for n in names],
        'completed_criteria':[c for c in TASK['acceptance'] if c not in pending],'pending_criteria':pending,
        'commands':checks,'blocker':None,'measurement':measurement,'next_operation':'Transition frozen delivery to review; stop this executor role.'})
    index=load(ROOT/'source-pins.json');current={p['path']:p for p in index['current_reports']}
    for name in ('original-access.json','validation-report.json','delivery-handoff.md','checkpoint-delivery.json','visual-qa.json','F02-completeness-report.json','source-cli-validation.json','source-suite-execution.json','full-check-execution.json','diff-check-execution.json','verifier-development.json','assembly-notes.json','toolchain-comparison.json','superseded-validation-index.json','proposal-preflight.json'):
        p=pin(ROOT/name);current[p['path']]=p
    index['current_reports']=list(current.values())
    index['superseded_validation_audit']=load(ROOT/'superseded-validation-index.json')
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
    for o in (index,validation,preservation,qa,full,source,delta,arrow,hit,load(ROOT/'superseded-generation-index.json'),load(ROOT/'superseded-second-generation-index.json'),load(ROOT/'proposal-preflight.json'),load(ROOT/'superseded-validation-index.json')):collect(o)
    collect(TASK['repair_authorization']);collect(TASK['context_recovery_authorization'])
    collect(scope['preserve_manifest'])
    for name in ('runtime-configuration.json','task.json','packet.json','references.json','access-manifest.json','dependency-view.json','search-manifest.json'):
        p=pin(SESSION/name);artifacts[p['path']]=p
    for n in names:
        for file in ('inventory.json','identity-registry.json'):
            p=pin(ROOT/n/file);artifacts[p['path']]=p
    # Exact owned root only; no recursive private tree search or pytest scratch.
    for file in ROOT.iterdir():
        if file.is_file() and file.name not in ('delivery.json','freeze-execution.log'):
            p=pin(file);artifacts[p['path']]=p
    for path in TASK['outputs']:assert path in artifacts,path
    ordered=[artifacts[path] for path in sorted(artifacts)]
    for p in ordered:assert pin(p['path'])==p
    envelope={**meta,'task':'IG-2B08','summary':'F02 marker-component evidence repaired; F01 arrow correction preserved at fresh paths; complete final and two serial replays, baseline preservation, source-bound marker/arrow regressions and unchanged required checks passed. Independent review requested.',
        'criteria':TASK['acceptance'],'criteria_assessment':{'executor_deliverables':'Submitted for independent review.','independent_review':'Pending in fresh supervisor-launched role.','human_semantic_acceptance':'Not granted; not required for this physical inventory task.','executable_readiness':'Unverified.'},
        'artifacts':ordered,'checks':checks,'input_packet':pin(SESSION/'packet.json'),'repair_scope':TASK['repair_authorization']['scope'],'measurement':measurement,
        'denominators':{'full_source':coverage['denominator_regions'],'assigned_four_pages':coverage['assigned_four_page']['denominator_regions'],'inherited_nonassigned':coverage['inherited_nonassigned']['denominator_regions'],'new_context_regions':coverage['context_only']['new_regions'],'context_contribution':0},
        'semantic_acceptance_granted':False,'executable_readiness':False,'preserved_input_artifact_count':12033,'preservation_manifest':scope['preserve_manifest'],
        'excluded_scratch':['source-pytest/','__pycache__/','freeze-execution.log'],'next_operation':'Fresh independent reviewer checks all original/appended criteria against this exact exhaustive frozen artifact set.'}
    write(ROOT/'delivery.json',envelope)
    for p in envelope['artifacts']:assert pin(p['path'])==p
    assert old_preservation()==12033
    print(json.dumps({'delivery':pin(ROOT/'delivery.json'),'artifact_count':len(ordered),'preserved_input_artifacts':12033}))

if __name__=='__main__':main()
