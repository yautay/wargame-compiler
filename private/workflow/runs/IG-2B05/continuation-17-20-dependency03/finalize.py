"""Freeze exact known deliverable paths without recursive filesystem discovery."""
import datetime
import hashlib
import json
from pathlib import Path

from wgc.sources.inventory import file_pin

ROOT=Path.cwd()
BASE=Path(__file__).resolve().parent
REL=BASE.relative_to(ROOT).as_posix()
SESSION='private/workflow/orchestrator/20261016T154824Z-fae43db9/001-IG-2B05-executor-008601fd'

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def pin(path): return file_pin(ROOT,path)
def write(name,value):
    p=BASE/name
    assert not p.exists(),name+' must be fresh'
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

claim=load(REL+'/claim.json')
common={k:claim[k] for k in ('task','actor','role','model','reasoning','configuration_evidence','configuration_sha256')}
assert pin(common['configuration_evidence'])['sha256']==common['configuration_sha256']
runtime=load(common['configuration_evidence'])
assert (runtime['status'],runtime['model'],runtime['reasoning'])==('confirmed','gpt-6.1-sol','high')
task=load(SESSION+'/task.json')
# Queue is loaded only in this final edit/check process. No events are printed.
queue=load('docs/work/queue.json')
current=next(t for t in queue['tasks'] if t['id']=='IG-2B05')
assert current['status']=='in_progress'
for key,value in task.items():
    if key!='status': assert current[key]==value,'task contract changed: '+key
assert current['events'][-1]['evidence']==REL+'/claim.json'
assert current['events'][-1]['sha256']==pin(REL+'/claim.json')['sha256']
for rec in load(SESSION+'/packet.json')['control_files']:
    assert pin(rec['path'])['sha256']==rec['sha256'],'control file changed: '+rec['path']

final=load(REL+'/final-verified/inventory.json')
evidence=load(REL+'/set-validation-report.json')
assert evidence['assigned_region_evidence_ledger_sets_equal']
assert evidence['both_complete_replays_passed']
assert evidence['nonassigned_preservation_passed']
assert load(REL+'/crop-review.json')['all_reviewed_image_bytes_equal_final']
assert load(REL+'/checks/result.json')=={
    **load(REL+'/checks/result.json'),
    'plan_exit':0,'dry_run_exit':0,'tests_exit':0,'diff_exit':0}

checks=[
    {'command':load(REL+'/checks/sources-pytest.json')['command'],'exit_code':0,'report':pin(REL+'/checks/sources-pytest.json')},
    {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B05','exit_code':0,'report':pin(REL+'/checks/result.json')},
    {'command':'git diff --check','exit_code':0,'log':pin(REL+'/checks/final-diff-check.log')},
    {'command':'.venv/Scripts/python.exe '+REL+'/report.py','exit_code':0,'log':pin(REL+'/checks/report.log')},
]
for name in ('final-verified','replay-1','replay-2'):
    short='final' if name=='final-verified' else name
    checks.append({'command':'.venv/Scripts/python.exe -m wgc.sources validate '+REL+'/'+name+'/inventory.json',
                   'exit_code':0,'log':pin(REL+'/checks/validate-'+short+'.log')})
    checks.append({'command':'.venv/Scripts/python.exe '+REL+'/derive.py '+name,'exit_code':0,
                   'log':pin(REL+'/derive-'+short+'.log')})

envelope={k:evidence[k] for k in ('inventory','inventory_revision','registry','source','assigned_physical_pages','assigned_ids','assigned_evidence')}
for name in ('final-verified','replay-1','replay-2'):
    report_path=BASE/name/'derivation-validation.json'
    raw=json.loads(report_path.read_text(encoding='utf-8'))
    report_path.write_text(json.dumps({**common,**envelope,
        'checked_inventory':pin(REL+'/'+name+'/inventory.json'),
        'coverage_validation':raw,'semantic_acceptance':False,'gameplay_readiness':False},
        indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
validation={**common,**envelope,'checks':checks,'required_checks_passed':True,
    'current_report_reference_count':len(load(REL+'/source-reference-index.json')['reports'])+2,
    'all_current_report_reference_hashes_and_inventory_revisions_checked':True,
    'source_tests':71,'repository_tests':257,'all_source_regions_visually_inspected':102,
    'all_visible_components_accounted':138,'independent_review':'required; pending a different actor',
    'semantic_acceptance':False,'gameplay_readiness':False,
    'failure_history':[{'kind':'restricted_token_pytest_basetemp_denial','resolved_by':'Approved exact unchanged source-suite execution; no assertion, ACL or library changes.'},
                      {'kind':'initial_crop_input_verified_label_assertion','resolved_by':'Retain exact required label regions and evidence during crop derivation.'},
                      {'kind':'slow_derivation_superseded','resolved_by':'Owned process stopped with approval, all partial files preserved, fresh complete final derivation and two replays passed.'}],
    'control_files_unchanged':True,'selected_live_contract_unchanged':True,'ownership_confirmed':True}
write('validation-report.json',validation)

# Complete the current-report index after the last reports exist. Self-hashing is
# deliberately avoided; the delivery freezes the index itself.
index=load(REL+'/source-reference-index.json')
set_report=load(REL+'/set-validation-report.json')
set_report['checked_report_count']=len(index['reports'])+2
set_report['finalization_check']='All current indexed report hashes and inventory revisions checked again immediately before delivery freeze.'
(BASE/'set-validation-report.json').write_text(json.dumps(set_report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for name in ('set-validation-report.json','validation-report.json'):
    index['reports'].append({**pin(REL+'/'+name),'inventory_revision':final['revision']})
for item in index['reports']:
    assert pin(item['path'])['sha256']==item['sha256']
    assert load(item['path'])['inventory_revision']==final['revision']
(BASE/'source-reference-index.json').write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

start=load(REL+'/checkpoint.json')['started_utc']
end=datetime.datetime.now(datetime.timezone.utc)
measurement={'started_utc':start,'ended_utc':end.isoformat(),
    'wall_seconds':(end-datetime.datetime.fromisoformat(start)).total_seconds(),
    'operator_seconds':None,'input_tokens':None,'output_tokens':None,
    'unknown_reason':'Operator time and trusted token counts are not exposed in this session.',
    'reviewer_defect_counts':None,'reviewer_defect_note':'Independent review has not run.'}
checkpoint={**common,**envelope,'input_packet':pin(SESSION+'/packet.json'),
    'completed_criteria':task['acceptance'][:-1],
    'pending_criterion':'Fresh independent technical/source-page review by a different actor is required.',
    'checks':checks,'measurement':measurement,'blocker':None,
    'next_operation':'Transition this frozen delivery to review; supervisor launches the separate reviewer.'}
write('checkpoint-delivery.json',checkpoint)

handoff='''# IG-2B05 delivery for independent review

This fresh continuation inventories physical SPQR pages 17-20 as 102 regions with
138 visible component dispositions. The complete sidecar retains 44 pages, 646
regions, 622 evidence records and 126 structural links. Exactly four assigned
placeholder memberships were replaced; 24 unassigned placeholders remain explicit.

The original four pages and all 102 fresh region crops were visually inspected.
The ledger records headers, footers, clauses, bullets, examples, notes, markers,
diagrams and diagram labels. All assigned transcription, descriptive-semantic and
formal-semantic levels remain unprocessed. Blank geometry is an explicit gap;
there are no new exclusions or represented semantic claims.

The accepted page-16 exit observation is boundary context only. No adjacent page
was inspected. Internal sentence/example continuations are linked. Page-20 clause
7.24 exits at an introductory colon, and its uninspected target remains unresolved.

Final output and both independent replays were freshly derived from the same
authored partition, persisted registry and byte-pinned accepted baseline. The
complete logical sidecars, identities, evidence-ID sets, locators and all 306
assigned PDF/PNG/text files match, with only the documented derived path prefixes
normalized. Preservation and current report/index resolution checks passed.

71 source tests and 257 repository tests passed under approved unchanged commands
after the restricted token's pytest temporary-directory denial. Full source
validation passed for the final inventory and both replays; git diff --check passed.
Exact commands and frozen logs are recorded in validation-report.json.

An initial slow generation was superseded. Its 141 partial files and helper/log
snapshot are preserved as diagnostic material, with no completeness claim.
The delivered final generation and both replays are complete new derivations.

Next action: a different actor must audit every assigned original page, all
proposed boundaries/components and crop images, the entire region ledger,
nonassigned preservation, complete replay comparisons and report/reference index.
No independent technical acceptance, human semantic acceptance or gameplay
readiness is granted by this executor delivery. No downstream task was started.
'''
(BASE/'delivery-handoff.md').write_text(handoff,encoding='utf-8')

paths=[]
def add(path):
    if path not in paths: paths.append(path)
for name in ('checkpoint.json','claim.json','checkpoint-implementation.json','checkpoint-delivery.json',
             'authored-partition.json','persisted-registry.json','derive.py','derive-full-evidence.py','report.py',
             'crop_sheets.py','finalize.py','superseded-derivation.json','derive-partial-retained.log',
             'derive-final.log','derive-replay-1.log','derive-replay-2.log','region-ledger.json',
             'continuations.json','coverage-report.json','source-pins.json','toolchain.json',
             'original-page-inspection.json','preservation-report.json','replay-report.json','validation-report.json',
             'crop-review.json','source-reference-index.json','set-validation-report.json','delivery-handoff.md'):
    add(REL+'/'+name)
for n in (17,18,19,20): add(REL+f'/original-pages/page-{n}.png')
for sheet in load(REL+'/crop-review.json')['sheets']:
    add(sheet['sheet']['path']); add(sheet['source_metadata']['path'])
for name in ('plan.log','dry-run.log','pytest.log','diff-check.log','result.json','sources-pytest.json',
             'validate-final.log','validate-replay-1.log','validate-replay-2.log','report.log','final-diff-check.log'):
    add(REL+'/checks/'+name)
for name in ('final-verified','replay-1','replay-2'):
    doc=load(REL+'/'+name+'/inventory.json')
    for leaf in ('inventory.json','identity-registry.json','derivation-validation.json'): add(REL+'/'+name+'/'+leaf)
    for ev in doc['evidence']:
        for field in ('crop_pdf','image','text'): add(ev[field]['path'])
for item in load(REL+'/superseded-derivation.json')['partial_output_artifacts']: add(item['path'])
# The source and accepted inputs remain input pins rather than newly delivered
# source copies. Retained evidence is explicitly frozen above, with exact bytes.
artifacts=[pin(path) for path in paths]
delivery={**common,'format':'wgc-task-delivery-1','summary':'Fresh four-page inventory, complete evidence and two independent replays validated; frozen for separate full source-page and technical review.',
    'criteria':task['acceptance'],'artifacts':artifacts,'checks':checks,'measurement':measurement,
    'input_packet':pin(SESSION+'/packet.json'),'task_contract':pin(SESSION+'/task.json'),
    'inventory':pin(REL+'/final-verified/inventory.json'),'registry':pin(REL+'/final-verified/identity-registry.json'),
    'criteria_state':'Executor deliverables submitted; independent review criterion pending a different actor.',
    'independent_review':'required; not granted','human_semantic_acceptance':False,'gameplay_readiness':False,
    'unresolved':['Page-20 outgoing continuation target and other uninspected numeric references.',
                  '24 nonassigned page placeholders; all assigned semantic representation levels remain unprocessed.'],
    'next_operation':'Separate reviewer audits the exact frozen artifact list and all four assigned original pages.'}
write('delivery.json',delivery)
print(json.dumps({'delivery':REL+'/delivery.json','sha256':pin(REL+'/delivery.json')['sha256'],
                  'artifacts':len(artifacts),'full_regions':len(final['regions']),'assigned_regions':102}))
