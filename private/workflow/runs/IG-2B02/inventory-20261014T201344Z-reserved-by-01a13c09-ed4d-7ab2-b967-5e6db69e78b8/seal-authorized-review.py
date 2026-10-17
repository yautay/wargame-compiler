"""Append-only final seal after the single explicitly authorized recovery retry."""
from ops import *
from datetime import datetime
conf=load(AR+'/configuration.json');manifest=load(AR+'/delivery-manifest.json');candidate=load(AR+'/delivery-transition-envelope.json')
assert not (A/'final-seal.json').exists()
assert pin(A/'delivery-transition-envelope.json')['sha256']=='c02077ee51ff4dc773385942de23fe0f1428ddf7cc038b45a8464e78056c5a19'
for p in manifest['new_reviewed_artifacts']+manifest['immutable_inputs_and_old_evidence']:assert pin(p['path'])==p,p['path']
for p in candidate['artifacts']:assert pin(p['path'])==p,p['path']
assert load(AR+'/operator-retry-authorization.json')['approved_envelope']==pin(A/'delivery-transition-envelope.json')
q=load('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-2B02');event=t['events'][-1]
assert t['status']=='review' and len(t['events'])==3 and event['from']=='in_progress' and event['to']=='review' and event['evidence']==AR+'/delivery-transition-envelope.json' and event['sha256']==pin(A/'delivery-transition-envelope.json')['sha256']
for name in ('review-transition-authorized','review-status-workflow-validate','review-status-diff-check'):assert load(AR+'/'+name+'.command.json')['exit_code']==0
# Verify the complete queue differs from the last pre-retry snapshot solely by
# the authorized recovery event/status, preserving every other queue field.
restored=load('docs/work/queue.json');rt=next(x for x in restored['tasks'] if x['id']=='IG-2B02');rt['events'].pop();rt['status']='in_progress'
raw=(json.dumps(restored,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');before=load(AR+'/authorized-review-preflight.json')['queue_before_retry'];assert hashlib.sha256(raw).hexdigest()==before['sha256'] and len(raw)==before['bytes']
checks=load(AR+'/required-checks.json');assert all(c['exit_code']==0 for c in checks)
supplement=f'''# IG-2B02 final review handoff after authorized envelope recovery

Authoritative queue status: review. Event UTC: {event['utc']}.
Event evidence: {event['evidence']}; SHA256 {event['sha256']}.
Executor: {conf['actor']}; session {conf['session_id']}; actual runtime configuration
gpt-6.1-sol/high, reobserved in authorized-review-preflight.json.

The operator explicitly approved this exact new envelope and one retry. That retry
exited zero and persisted the correct event. No further retry was made. The first
failed transition, diagnosis, correction proposal, pending-authorization checkpoint
and original frozen delivery remain immutable. This handoff supersedes only their
operational pending-status instructions. It does not change any product/report bytes.
The envelope's recorded pending authorization is resolved by the later append-only
operator-retry-authorization.json; the approved envelope itself was not overwritten.

The original frozen manifest remains the complete product/input/evidence catalogue:
{AR}/delivery-manifest.json
SHA256 {pin(A/'delivery-manifest.json')['sha256']}.
The successful event's approved envelope retains every admissible reviewed artifact
and adds recovery evidence. Five executable observations remain pinned in toolchain,
preflight and manifest metadata rather than direct workflow artifact paths.

Inventory: {AR}/final-verified/inventory.json
SHA256 {pin(A/'final-verified/inventory.json')['sha256']}.
Registry: {AR}/final-verified/identity-registry.json
SHA256 {pin(A/'final-verified/identity-registry.json')['sha256']}.
Ledger: {AR}/region-ledger-final.json
SHA256 {pin(A/'region-ledger-final.json')['sha256']}.

141 new regions on physical pages 5-8; full denominator 307; preserved context
denominator zero. Accepted old scope, registry, evidence, links/order, 36 placeholders
and original PDF bytes remain exact. No page-9 content access occurred. Detailed
source scope, context correspondence, grouping, raw anomalies and representation/
geometric gaps remain in the original delivery-handoff.md and frozen reports.

All implementation checks passed: 71 unchanged source tests, 102 full-suite tests,
root PDF/schema/canonical/identity/order/partition validation, all 141 locator audits,
423 exact evidence files, rational crop bounds, Unicode offsets, pixel dimensions,
identical render/text replays and persisted-registry authoring replays. After the
successful transition, workflow validation and git diff --check also passed.
Original publisher Xref warnings remain visible in immutable stderr logs.

Criteria 1-4 are implemented for independent review; criterion 5 remains pending.
A fresh separate reviewer session/identity must compare all assigned original pages
against the complete exact ledger, examine grouped components and uncertainty,
verify unchanged old scope, bounded context/correspondence, every approved artifact
and immutable input hash. Use the exact envelope pinned by this review event and
final-seal.json. Executor self-inspection and IG-2B01 review are insufficient.

No acceptance/done, human semantic acceptance, whole-record source-IG approval,
approved exclusion, gameplay legality or executable readiness is granted. No
downstream task, new session, agent, automation, commit or push was started.
The executor stops at review. The operator supplies the independent-review session.
'''
with (A/'review-handoff-final.md').open('x',encoding='utf-8',newline='\n') as f:f.write(supplement)
checkpoint=load(AR+'/preclaim-checkpoint.json');checkpoint.update(stage='final-review',updated_utc=now(),completed_criteria=['Criteria 1-4 implemented for independent review','All required implementation checks passed','Frozen artifacts and approved envelope reverified','Exactly one operator-authorized retry succeeded','Review status/event/hash and derived views verified'],unmet_criteria=[t['acceptance'][4]],blocker=None,next_operation='STOP executor work; operator supplies a fresh separate independent reviewer for exact frozen hashes',current_owned_hashes=[pin(p) for p in sorted(A.rglob('*')) if p.is_file()],commands=[load(p.relative_to(R).as_posix()) for p in sorted(A.glob('*.command.json'))],review_event=event,operator_retry_authorization=pin(A/'operator-retry-authorization.json'))
write('checkpoint-final-review.json',checkpoint)
ended=now();start=load(AR+'/preclaim-checkpoint.json')['started_utc'];elapsed=(datetime.fromisoformat(ended)-datetime.fromisoformat(start)).total_seconds()
# The original manifest and approved envelope stay byte-identical. Recovery and
# epilogue files are separately sealed, including the authorization and final handoff.
original_paths={p['path'] for p in manifest['new_reviewed_artifacts']}
postfreeze=[pin(p) for p in sorted(A.rglob('*')) if p.is_file() and pin(p)['path'] not in original_paths and p.name not in ('final-seal.json',)]
seal={'task':'IG-2B02','status':'review','actor':conf['actor'],'session_id':conf['session_id'],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':pin(A/'configuration.json'),'configuration_reobservation':pin(A/'authorized-review-preflight.json'),'operator_authorization':pin(A/'operator-retry-authorization.json'),'delivery_manifest':pin(A/'delivery-manifest.json'),'original_frozen_delivery':pin(A/'delivery.json'),'authoritative_transition_delivery':pin(A/'delivery-transition-envelope.json'),'original_handoff':pin(A/'delivery-handoff.md'),'final_review_handoff':pin(A/'review-handoff-final.md'),'criteria':pin(A/'criteria.json'),'inventory':pin(A/'final-verified/inventory.json'),'registry':pin(A/'final-verified/identity-registry.json'),'complete_region_ledger':pin(A/'region-ledger-final.json'),'checkpoint':pin(A/'checkpoint-final-review.json'),'all_original_frozen_artifacts_verified':True,'all_approved_envelope_artifacts_verified':True,'frozen_files_overwritten':False,'review_event':event,'queue_mutation_verification':'Exact pre-retry queue bytes reconstructed from current queue by reverting only this authorized review status/event; hash/byte count match.','queue_observation':pin('docs/work/queue.json'),'approved_retry_count':1,'successful_retry_exit_code':0,'approved_artifact_count':len(candidate['artifacts']),'postfreeze_recovery_and_epilogue_artifacts':postfreeze,'required_checks':checks,'post_transition_checks':[load(AR+'/'+name+'.command.json') for name in ('review-status-workflow-validate','review-status-diff-check')],'measurement':{'started_utc':start,'ended_utc':ended,'elapsed_wall_seconds':elapsed,'basis':'Preclaim preflight start to final seal construction. Elapsed wall time includes waiting for operator recovery authorization; active/operator time was not independently measured.','input_tokens':None,'output_tokens':None,'monetary_cost':None,'operator_seconds':None,'unknown_reason':'Not exposed/measured.'},'independent_reviewer':None,'independent_review':'Pending fresh separate session/identity comparing original assigned pages, complete ledger and all exact delivery hashes.','acceptance_granted':False,'semantic_acceptance_granted':False,'whole_record_source_IG_review':'not established','executable_readiness':'unverified','downstream_work_started':False,'self_exclusion_policy':'Final seal excludes itself. This invocation writes no subsequent mutable artifacts in the attempt. Exact final seal bytes/hash are returned to the operator.','stop':'Review reached; executor stops. No acceptance/done, downstream task or new session.'}
for p in postfreeze:assert pin(p['path'])==p
write('final-seal.json',seal)
print(json.dumps({'status':t['status'],'final_seal':pin(A/'final-seal.json'),'approved_envelope':pin(A/'delivery-transition-envelope.json'),'final_handoff':pin(A/'review-handoff-final.md'),'inventory':pin(A/'final-verified/inventory.json'),'registry':pin(A/'final-verified/identity-registry.json'),'manifest':pin(A/'delivery-manifest.json')},indent=2))
