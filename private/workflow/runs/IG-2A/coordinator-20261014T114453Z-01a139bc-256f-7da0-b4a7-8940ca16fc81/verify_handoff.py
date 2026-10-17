"""Verify independent PASS and prepare unapplied technical closure proposals."""
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path.cwd()
RUN=Path(__file__).resolve().parent
REVIEW=ROOT/'private/workflow/runs/IG-2A/review-20261014T104443Z-codex-01a13a03-b220-7181-a813-09f6e7b46c1f'
REPAIR=ROOT/'private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def write(name,value): (RUN/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def command(name,argv):
    start=datetime.now(timezone.utc); clock=time.monotonic()
    result=subprocess.run(argv,capture_output=True,text=True)
    (RUN/(name+'.stdout')).write_text(result.stdout,encoding='utf-8',newline='\n')
    (RUN/(name+'.stderr')).write_text(result.stderr,encoding='utf-8',newline='\n')
    row={'command':subprocess.list2cmdline(argv),'argv':argv,'exit_code':result.returncode,
         'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
         'wall_seconds':time.monotonic()-clock,'stdout':name+'.stdout','stderr':name+'.stderr'}
    write(name+'.json',row); return row

start=datetime.now(timezone.utc)
actor='codex-'+os.environ['CODEX_THREAD_ID']
config=read(REPAIR/'configuration.json'); assert config['actor']==actor
write('configuration.json',{'role':'coordinator','actor':actor,'session_id':os.environ['CODEX_THREAD_ID'],
      'model':config['model'],'reasoning':config['reasoning'],'configuration_evidence':pin(REPAIR/'configuration.json'),
      'evidence_note':'Same continuing session; current operator confirmation is preserved in repair configuration. Independent reviewer identity is separately attributed, never used as this coordinator identity.',
      'started_utc':start.isoformat()})
queue_path=ROOT/'docs/work/queue.json'; queue_sha=sha(queue_path)
q=read(queue_path); task=next(t for t in q['tasks'] if t['id']=='IG-2A'); assert task['status']=='review'
assert sha(REVIEW/'final-seal-corrected.json')=='af1af2473a58e47ab69396bdf1d7f9dd39a765881bacab630068b87c2411b295'
seal=read(REVIEW/'final-seal-corrected.json'); manifest=read(ROOT/seal['manifest']['path'])
review=read(ROOT/seal['review']['path']); handoff=read(ROOT/seal['handoff']['path']); delivery=read(REPAIR/'delivery.json')
checked=[]
def verify(entry):
    p=ROOT/entry['path']; actual=sha(p)
    assert actual==entry['sha256'] and ('bytes' not in entry or entry['bytes']==p.stat().st_size),entry['path']
    checked.append({'path':entry['path'],'expected_sha256':entry['sha256'],'actual_sha256':actual,'matches':True})
for container in [seal,handoff]:
    for entry in container.values():
        if isinstance(entry,dict) and 'path' in entry and 'sha256' in entry: verify(entry)
for entry in manifest['artifacts']+manifest['reviewed_delivery_artifacts']+review['artifacts']: verify(entry)
original=read(REVIEW/'review-manifest.json')
for entry in original['artifacts']: verify(entry)
repair_seal=read(REPAIR/'final-seal.json')
for entry in repair_seal['post_freeze_operational_artifacts']+repair_seal['governance_artifacts']: verify(entry)
assert len(manifest['artifacts'])==954 and manifest['reviewed_delivery_artifacts']==delivery['artifacts']
assert seal['queue_sha256']==queue_sha
assert review['actor']!=actor and review['outcome']==handoff['outcome']==seal['outcome']=='PASS'
assert task['events'][-1]['sha256']==sha(REPAIR/'delivery.json')
assert review['criteria']==handoff['criteria']==task['acceptance']
assert review['semantic_acceptance_granted'] is False and task['semantic_acceptance_required'] is False
dispositions=read(REVIEW/'dispositions.json'); criteria=read(REVIEW/'criteria.json'); findings=read(REVIEW/'findings.json')
assert {d['id'] for d in dispositions}=={f'IG2A-R0{i}' for i in range(1,6)}
assert all(d['disposition']=='CLOSED' for d in dispositions)
assert [c['criterion'] for c in criteria]==task['acceptance']
assert all(c['status']=='MET_FOR_IG2A_TECHNICAL_TOOLING_SCOPE' for c in criteria)
assert not findings['actionable_findings']
probe_summaries=[]
for name in ['probe-results.json','retained-reproduction-results.json','independent-pixel-oracles.json']:
    rows=read(REVIEW/name)['results']; assert all(row['expectation_met'] for row in rows)
    probe_summaries.append({'evidence':pin(REVIEW/name),'cases':len(rows),'all_expectations_met':True})
rows=read(REVIEW/'independent-integer-pixel-boundaries.json')['results']
assert len(rows)==8 and all(row['validator_error'] is None and row['actual_pixels']==row['exact_mathematical_pixels'] for row in rows)
probe_summaries.append({'evidence':pin(REVIEW/'independent-integer-pixel-boundaries.json'),'cases':len(rows),'all_expectations_met':True})
repeat=read(REVIEW/'repeatability.json')
for key in ['canonical_bytes_identical','serialized_bytes_identical','persisted_registry_identical','page_and_region_identity_identical','all_44_placeholders_unprocessed','source_geometry_matches_independent_pypdf']: assert repeat[key] is True
assert repeat['represented_all_levels']==0
required=read(REVIEW/'required-checks.json'); assert all(c['exit_code']==0 for c in required)
assert all(c['exit_code']==0 for c in review['checks'])
checks=[command('workflow-validate',[sys.executable,'scripts/workflow.py','validate']),command('diff-check',['git','diff','--check'])]
assert all(c['exit_code']==0 for c in checks)
write('integrity.json',{'checked':checked,'mismatches':0,'review_artifacts':954,'delivery_artifacts':273,
      'original_review_freeze_artifacts':len(original['artifacts']),'queue':pin(queue_path),
      'corrected_review_seal':pin(REVIEW/'final-seal-corrected.json')})
write('technical-assessment.json',{'role':'coordinator','actor':actor,'task':'IG-2A',
      'decision':'Technical PASS recommendation; no acceptance/done transition applied',
      'independent_reviewer':review['actor'],'review':pin(REVIEW/'review-final.json'),
      'criterion_assessments':criteria,'finding_dispositions':dispositions,'probes':probe_summaries,
      'required_checks':required,'coordinator_checks':checks,
      'handoff_correction':'Corrected seal and suffixed final review/report/handoff are consistent. Original frozen handoff deliberately preserves the documented stale review pin; old bytes remain immutable.',
      'product_test_reuse':'Reviewer ran 71 sources and 102 project tests against the exact unchanged delivery. Coordinator verifies their pinned logs and current product hashes; no implementation changed, so no duplicate full suite is justified.',
      'semantic_acceptance_granted':False,'IG2B_authorized':False})
# The decision actor comes from the immutable independent reviewer; preparation
# ownership and the coordinator's continuing session are explicit and separate.
acceptance=copy.deepcopy(review)
extras=[entry for entry in review['artifacts'] if entry not in delivery['artifacts']]
acceptance['artifacts']=copy.deepcopy(delivery['artifacts'])
acceptance['prepared_by']={'role':'coordinator','actor':actor,'configuration':pin(RUN/'configuration.json')}
acceptance['decision_provenance']=pin(REVIEW/'review-final.json')
acceptance['supporting_review_artifacts']=extras
acceptance['application_status']='PROPOSAL_NOT_APPLIED'
acceptance['preparation_note']='Mandatory artifacts are exactly the unchanged delivery list. Supporting reviewer reports remain separately pinned. Reviewer actor, outcome, criteria, checks, configuration and observations are copied unchanged from the frozen independent review; this coordinator is not the reviewer.'
write('accepted-proposal.json',acceptance)
done={'role':'coordinator','actor':actor,'summary':'Proposed technical closure of IG-2A after verified independent PASS and exact criteria/evidence; no semantic acceptance or IG-2B execution.',
      'criteria':task['acceptance'],'artifacts':copy.deepcopy(delivery['artifacts']),
      'model':config['model'],'reasoning':config['reasoning'],'configuration_evidence':pin(RUN/'configuration.json')['path'],
      'checks':checks,'independent_review':pin(REVIEW/'review-final.json'),
      'technical_assessment':pin(RUN/'technical-assessment.json'),'application_status':'PROPOSAL_NOT_APPLIED',
      'semantic_acceptance_granted':False}
write('done-proposal.json',done)
spec=importlib.util.spec_from_file_location('workflow',ROOT/'scripts/workflow.py'); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
simulated=copy.deepcopy(q)
w.transition(simulated,ROOT,'IG-2A','accepted',(RUN/'accepted-proposal.json').relative_to(ROOT).as_posix())
w.transition(simulated,ROOT,'IG-2A','done',(RUN/'done-proposal.json').relative_to(ROOT).as_posix())
assert sha(queue_path)==queue_sha and next(t for t in read(queue_path)['tasks'] if t['id']=='IG-2A')['status']=='review'
write('gate-simulation.json',{'result':'PASS','scope':'Deep copy of queue in memory only; no queue writes, events, rendering or real transitions',
      'simulated_gates':['review -> accepted','accepted -> done'],'real_queue_status':'review','real_queue_unchanged':True,
      'review_support_artifacts_separated':len(extras),'reviewer_artifact_bytes_unchanged':True,
      'acceptance_proposal':pin(RUN/'accepted-proposal.json'),'done_proposal':pin(RUN/'done-proposal.json')})
end=datetime.now(timezone.utc)
write('measurement.json',{'actor':actor,'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'wall_seconds':(end-start).total_seconds(),
      'tokens':None,'cost':None,'operator_seconds':None,'unknown_reason':'Task totals/cost/operator time unavailable.'})
report=f'''# IG-2A coordinator handoff verification

Technical recommendation: PASS and ready for an operator-authorized technical closure. Real queue status remains review. No acceptance/done transition, semantic decision, product edit or IG-2B work occurred.

Coordinator {actor} is the continuing executor session acting as coordinator. Independent reviewer {review['actor']} supplied the frozen PASS; reviewer identity/configuration/decision are separately attributed, not claimed as this coordinator's identity. Current coordinator configuration is preserved from this same session's direct operator confirmation.

All 954 corrected review manifest artifacts, 273 exact delivery artifacts, all first-review-freeze artifacts and current post-freeze/governance pins were verified without hash discrepancies. The corrected seal, final handoff, final report and final review point to the same exact bytes. The original stale handoff metadata remains preserved with the documented append-only correction; it is not the acceptance basis.

All three exact task criteria are met for the IG-2A tooling scope; all five prior findings are independently CLOSED. The verified review includes 55 fresh probes, 12 migrated retained cases, eight exact full-image pixel oracles and eight integer-pixel-boundary cases. All expectations passed. Two independently generated inventories preserve canonical bytes and UUID identity. All 44 placeholders remain unprocessed; none grant substantive source coverage. Independent review's 71 sources and 102 project tests passed on these exact unchanged product bytes; current workflow validation and diff checks also pass.

The final reviewer evidence includes {len(review['artifacts'])} entries: the exact 273 delivery entries and {len(extras)} supporting reports. The unchanged workflow acceptance gate requires the mandatory artifact list to equal delivery exactly. accepted-proposal.json therefore preserves the original reviewer decision fields and attribution, moves supporting reports to a separately pinned field, and explicitly records this coordinator as preparer. done-proposal.json uses the coordinator's own identity. Both gates pass on an in-memory copy only; the real queue remains untouched. No independent reviewer statement or human authority was invented.

The earlier operator instruction explicitly forbids acceptance/done and requires stopping at review. A generic continuation authorizes this handoff verification, but is not treated as a revocation of that explicit restriction. The prepared proposals await explicit authorization for technical review -> accepted -> done on IG-2A only. This is not human semantic acceptance. IG-2B remains outside scope.

Evidence: integrity.json, technical-assessment.json, gate-simulation.json, accepted-proposal.json, done-proposal.json. UTC {start.isoformat()} to {end.isoformat()}; elapsed {(end-start).total_seconds():.3f} seconds. Tokens/cost/operator time are null.
'''
(RUN/'report.md').write_text(report,encoding='utf-8',newline='\n')
files=[pin(p) for p in sorted(RUN.iterdir()) if p.is_file()]
write('manifest.json',{'task':'IG-2A','actor':actor,'purpose':'Coordinator verification and unapplied technical closure proposals',
      'artifacts':files,'queue_unchanged':True,'queue_sha256':queue_sha})
write('final-seal.json',{'task':'IG-2A','actor':actor,'status':'review','manifest':pin(RUN/'manifest.json'),'report':pin(RUN/'report.md'),
      'independent_review_seal':pin(REVIEW/'final-seal-corrected.json'),'accepted_proposal':pin(RUN/'accepted-proposal.json'),
      'done_proposal':pin(RUN/'done-proposal.json'),'technical_recommendation':'PASS','transitions_applied':False,
      'queue_sha256':queue_sha,'semantic_acceptance_granted':False,'ended_utc':end.isoformat()})
print('Coordinator verification PASS; 954 review and 273 delivery artifacts verified; both technical gates pass in memory only. Queue remains review.')
