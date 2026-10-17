"""Freeze only explicit owned F01 repair outputs and validation evidence."""
import datetime
import json
from pathlib import Path
from wgc.sources.inventory import file_pin
ROOT=Path.cwd()
A=Path(__file__).parent.relative_to(ROOT)
S=Path('private/workflow/orchestrator/20261016T195516Z-332903f5/005-IG-2B07-executor-32eedee6')
OLD=Path('private/workflow/runs/IG-2B07/inventory-25-28-01')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):return file_pin(ROOT,Path(p).as_posix())
def write(p,v):
    assert not Path(p).exists(),str(p)
    Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
task=load(S/'task.json');scope=task['source_scope'];claim=load(A/'claim.json')
meta={k:claim[k] for k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256')}
assert pin(meta['configuration_evidence'])['sha256']==meta['configuration_sha256']
assert (load(meta['configuration_evidence'])['status'],meta['model'],meta['reasoning'])==('confirmed','gpt-6.1-sol','high')
assert pin(OLD/'delivery.json')['sha256']=='cee94ecd856edb0da9439881a0e002f7515f45f334a1b4e02fcd16b3f20cab27'
for x in load(OLD/'delivery.json')['artifacts']:assert pin(x['path'])==x,x['path']
inputs=[scope[k] for k in ('baseline_inventory','identity_registry','source_pdf','source_provenance')]+list(scope['current_reports'].values())+[task['refinement_evidence'],task['repair_authorization']['scope'],task['repair_authorization']['evidence']]
for x in inputs:assert pin(x['path'])==x,x['path']
obs=load(A/'validation-command-observations.json')
assert all(c['exit_code']==0 for c in obs['checks'])
assert obs['repository_result']=={'plan_exit':0,'dry_run_exit':0,'tests_exit':0,'diff_exit':0}
replay=load(A/'replay-report.json');cov=load(A/'coverage-report.json');pres=load(A/'repair-preservation-report.json')
assert replay['all_passed'] and len(replay['runs'])==3
assert all(r['output_count']==571 for r in replay['runs'])
assert (cov['full_inventory_count'],cov['assigned_inventory_count'],cov['full_context_count'])==(849,100,92)
assert cov['context_denominator_contribution']==0 and len(replay['target_ids'])==189 and len(replay['component_ids'])==87
checks=list(obs['checks'])
for name in ('final-verified','replay-1','replay-2'):
    checks.append({'command':'.venv/Scripts/python.exe '+(A/'run_inventory.py').as_posix()+' --output '+(A/name).as_posix(),'exit_code':0,'report':pin(A/name/'derivation-report.json'),'log':pin(A/('final-generation.log' if name=='final-verified' else name+'.log'))})
checks.append({'command':'.venv/Scripts/python.exe '+(A/'report_inventory.py').as_posix(),'exit_code':0,'report':pin(A/'replay-report.json')})
validation={**meta,'format':'wgc-f01-repair-validation-1','checks':checks,'environment_failures_and_approved_execution':pin(A/'validation-command-observations.json'),'input_pins_reverified':inputs,'immutable_prior_delivery':pin(OLD/'delivery.json'),'prior_artifacts_verified_before_and_after':len(load(OLD/'delivery.json')['artifacts']),'packet':pin(S/'packet.json'),'full_inventory_count':849,'task_inventory_count':100,'full_context_count':92,'total_region_records':941,'new_nested_components':87,'new_total_targets':189,'context_denominator_contribution':0,'preservation':pin(A/'preservation-report.json'),'repair_preservation':pin(A/'repair-preservation-report.json'),'complete_replays':pin(A/'replay-report.json'),'source_inspection':pin(A/'original-page-inspection.json'),'unresolved_limits':['Fresh independent technical/source-accounting rereview is pending.','Prior complete four-page and boundary inspection retains its original actor attribution. Only the affected original second diagram and all its components were freshly visually inspected by this repair role.','Full transcription and tiny raster glyph readings remain unverified.','Descriptive/formal semantics and executable readiness remain unprocessed.','Unassigned pages 29-44 retain their inherited placeholders.'],'semantic_acceptance_granted':False,'executable_readiness':'unverified'}
write(A/'validation-report.json',validation)
handoff="""# IG-2B07 F01 repair handoff

Added the complete visible upper black arrow beside B in the second page-28 diagram
as one stable nested context component. The new component describes visual position
only and has no assigned legal target or gameplay semantics. All prior IDs, region
records, registry entries, links, observations and evidence payload byte pins remain
unchanged. The old delivery and all 2,956 artifacts verify unchanged.

The repaired set contains 189 targets, including 87 nested components. The full
inventory remains 849 units, the assigned inventory remains 100, and context now has
92 regions. Total region records: 941. Context contributes zero inventory denominator.

The affected original diagram and every one of its 43 nested components were freshly
inspected. The complete arrow is visible in its fresh original and derived crops.
Previous full four-page and permitted boundary inspection records remain immutable
and attributed to the prior executor; their target IDs and payload bytes revalidate.
Two separate complete serial replays regenerated all 189 targets. IDs, registry,
author fields, geometry, reading order, links, coverage and all PDF/text/image bytes
compare exactly after explicit output-path-prefix normalization.

The unchanged source suite and repository check passed through approved execution
after Windows restricted-token temporary-directory failures. Exact commands, exits,
failure logs, approved results and reports are frozen. Source validation and
git diff --check passed. No tests, assertions, dependencies, ACLs or global settings
were changed.

Next: independent technical/source-accounting rereview of the entire new delivery,
original assigned source scope and the F01 component. No human semantic acceptance,
gameplay legality or executable readiness is granted. The supervisor alone launches
any next role; this executor stops after transitioning to review.
"""
assert not (A/'delivery-handoff.md').exists()
(A/'delivery-handoff.md').write_text(handoff,encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc);initial=load(A/'checkpoint-initial.json')
write(A/'checkpoint-final.json',{**meta,'task':task['id'],'attempt':A.as_posix(),'input_packet':pin(S/'packet.json'),'base_files':inputs,'changed_files':[pin(p) for p in task['outputs']],'completed_criteria':[v for i,v in enumerate(task['acceptance']) if i not in (2,len(task['acceptance'])-1)],'pending_criteria':[task['acceptance'][2],task['acceptance'][-1]],'checks':checks,'blocker':None,'next_operation':'Freeze complete F01 delivery, transition to independent review and stop.','started_utc':initial['started_utc'],'checkpoint_utc':now.isoformat()})
paths=[Path(p) for p in task['outputs']]
paths += [A/n for n in ('run_inventory.py','report_inventory.py','affected_sheets.py','freeze_delivery.py','claim.json','checkpoint-initial.json','checkpoint-inspected.json','checkpoint-final.json','author-input.json','author-registry.json','author-pins.json','repair-preservation-report.json','visual-observations.json','validation-command-observations.json','final-generation.log','replay-1.log','replay-2.log','source-validation.log','pytest-sources-restricted-failure.log','pytest-sources-restricted.log','repository-check-restricted-failure.log','repository-check.log','diff-check.log','originals/pins.json','inspection-sheets/index.json','affected-inspection-sheets/index.json')]
paths += [Path(x['path']) for name in ('originals/pins.json','inspection-sheets/index.json','affected-inspection-sheets/index.json') for x in load(A/name)]
paths += [Path(x['path']) for run in replay['runs'] for x in run['output_pins']]
paths += [Path(x['path']) for x in obs['repository_check_reports']]
paths=list(dict.fromkeys(paths))
assert all(p.resolve().is_relative_to((ROOT/A).resolve()) for p in paths)
for run in replay['runs']:
    for x in run['output_pins']:assert pin(x['path'])==x
for x in obs['repository_check_reports']:assert pin(x['path'])==x
artifacts=[pin(p) for p in paths]
started=datetime.datetime.fromisoformat(initial['started_utc'])
delivery={**meta,'summary':'F01 repaired with one complete upper-B-arrow component, exact prior preservation, 189-target complete serial evidence and two independent full replays; passing unchanged validation; ready for independent rereview.','criteria':task['acceptance'],'criterion_status':[{'criterion':v,'status':'pending_independent_review' if i in (2,len(task['acceptance'])-1) else 'executor_evidence_complete_pending_independent_review'} for i,v in enumerate(task['acceptance'])],'artifacts':artifacts,'checks':checks,'input_packet':pin(S/'packet.json'),'input_pins':inputs,'immutable_prior_delivery':pin(OLD/'delivery.json'),'repair_finding_ids':['F01'],'measurement':{'started_utc':initial['started_utc'],'ended_utc':now.isoformat(),'wall_seconds':(now-started).total_seconds(),'operator_seconds':None,'input_tokens':None,'output_tokens':None,'unknown_reason':'Operator time and token counts are not exposed.'},'defects':{'F01_executor_repair':'implemented_pending_independent_rereview','new_open_executor_findings':0},'semantic_acceptance_granted':False,'executable_readiness':'unverified','next_operation':'Independent technical/source-accounting rereview against original scope and full frozen artifact list. Supervisor owns next process launch.'}
write(A/'delivery.json',delivery)
print(json.dumps({'delivery':(A/'delivery.json').as_posix(),'sha256':pin(A/'delivery.json')['sha256'],'artifacts':len(artifacts)}))
