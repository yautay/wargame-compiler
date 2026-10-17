"""Append-only transition envelope recovery proposal; no queue mutation/retry."""
from ops import *
import copy
q=load('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-2B02');assert t['status']=='in_progress' and len(t['events'])==2 and t['events'][-1]['sha256']==pin(A/'claim.json')['sha256']
diagnosis=load(AR+'/review-transition-diagnosis.json');bad={x['pin']['path'] for x in diagnosis['invalid_artifacts']};assert len(bad)==5
delivery=load(AR+'/delivery.json');manifest=load(AR+'/delivery-manifest.json')
for p in delivery['artifacts']:assert pin(p['path'])==p
write('transition-recovery-proposal.json',{'task':'IG-2B02','status':'operator_authorization_required_before_retry','cause':'Executor incorrectly copied five tool-executable observations into workflow transition artifacts. Frozen gate denies .venv and absolute non-repository paths. All bytes matched; the failure is envelope path policy, not source/inventory/audit/test correctness.','first_transition_exit':1,'queue_status_after_failure':'in_progress','no_review_event_persisted':True,'excluded_from_workflow_artifact_array':[x['pin'] for x in diagnosis['invalid_artifacts']],'toolchain_observations_preserved_in':[pin(A/'toolchain.json'),pin(A/'preflight.json'),pin(A/'delivery-manifest.json')],'all_product_and_new_review_files_retained':True,'frozen_files_overwritten':False,'correction_policy':'Append a new transition envelope retaining every admissible artifact and all original frozen delivery bytes. Executable observations remain exactly pinned as metadata in immutable toolchain/preflight/manifest files; they cannot be direct queue artifact paths. No validation weakening or tool/test/contract change.','instruction_gate':'Operator launch explicitly says never automatically repeat a transition and otherwise checkpoint/escalate if no correct event persisted. Await operator/coordinator decision before retry.','next_command':[PY,'-B','scripts/workflow.py','transition','--task','IG-2B02','--to','review','--evidence',AR+'/delivery-transition-envelope.json'],'independent_review':'Still pending; no acceptance/done or downstream work.'})
text='''# IG-2B02 transition-envelope recovery handoff

The original frozen delivery and manifest remain immutable. All implementation and
required validations passed (71 source tests, 102 full-suite tests). The attempted
in_progress -> review transition exited 1 with Invalid artifact hash/path. Inspection
confirmed queue still in_progress and no review event persisted.

The executor wrongly included five executable observations as direct workflow artifact
paths: .venv/Scripts/python.exe is denied, and four installed native executable paths
are absolute/outside the repository. All bytes matched. These pins remain preserved
inside toolchain.json, preflight.json and delivery-manifest.json. The append-only
delivery-transition-envelope.json removes only those five direct paths, retaining all
admissible frozen product/report/source/evidence references and adding recovery evidence.
No original frozen artifact, source, tool, test, contract or validation was changed.

This is a concrete recovery proposal, not a successful transition or authorization to
retry. The launch instruction requires checkpoint/escalation and forbids automatic
repeat after transition failure. The operator/coordinator must explicitly authorize
the proposed new envelope/retry. If authorized, execute exactly the recorded command,
inspect actual event/hash/status, seal original delivery plus this new envelope and
all recovery evidence without overwriting originals, and stop at review.

The independent reviewer must use the exact envelope selected by the eventual review
event. That envelope will include the original frozen manifest, all admissible original
review targets and this recovery record. Original assigned-page/ledger/old-scope/hash
verification requirements remain unchanged. The current task is not yet in review.
'''
with (A/'transition-recovery-handoff.md').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
cp=copy.deepcopy(load(AR+'/checkpoint.json'));cp.update(stage='review-transition-failed',updated_utc=now(),blocker={'type':'transition_artifact_path_policy','evidence':pin(A/'review-transition-diagnosis.json'),'queue_status':'in_progress','operator_decision_required':'Authorize append-only corrected envelope and one retry, or coordinator triage.'},next_operation='Await operator/coordinator escalation decision; do not repeat transition automatically',current_frozen_targets=[pin(A/f) for f in ('delivery.json','delivery-manifest.json','delivery-handoff.md','final-verified/inventory.json','final-verified/identity-registry.json','criteria.json')]);write('checkpoint-review-transition-failed.json',cp)
candidate=copy.deepcopy(delivery);candidate['summary']='Append-only corrected IG-2B02 transition envelope: original frozen inventory/reports unchanged; five forbidden direct executable observation paths retained only in pinned toolchain/manifest metadata; independent review pending.'
candidate['artifacts']=[p for p in delivery['artifacts'] if p['path'] not in bad]+[pin(A/f) for f in ('delivery.json','review-transition.command.json','review-transition.stdout','review-transition.stderr','review-transition-diagnosis.json','transition-recovery-proposal.json','transition-recovery-handoff.md','checkpoint-review-transition-failed.json','prepare-transition-recovery.py')]
candidate['original_frozen_delivery']=pin(A/'delivery.json');candidate['transition_correction']=pin(A/'transition-recovery-proposal.json');candidate['authorization_status']='Pending operator/coordinator decision before use';candidate['self_exclusion_policy']='New envelope excludes itself; eventual review event pins exact envelope bytes. Original delivery remains frozen and included as recovery evidence.'
write('delivery-transition-envelope.json',candidate)
# Read-only reproduction of each gate's path/hash rule. Do not call transition.
sys.path.insert(0,str(R/'scripts'));import workflow
for p in candidate['artifacts']:
 path=workflow.safe_path(R,p['path']);assert not workflow.denied(p['path']) and path.is_file() and workflow.digest(path)==p['sha256']
write('transition-recovery-preflight.json',{'outcome':'passed_path_hash_structure','candidate':pin(A/'delivery-transition-envelope.json'),'valid_artifact_count':len(candidate['artifacts']),'excluded_executable_observations':5,'queue_unchanged':pin('docs/work/queue.json'),'no_transition_called':True,'authorization':'pending'})
print('RECOVERY CANDIDATE READY',json.dumps(pin(A/'delivery-transition-envelope.json')))
