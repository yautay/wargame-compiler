"""Read-only resume gate and append-only operator authorization observation."""
from ops import *
sys.path.insert(0,str(R/'scripts'))
import workflow
expected='c02077ee51ff4dc773385942de23fe0f1428ddf7cc038b45a8464e78056c5a19'
candidate_pin=pin(A/'delivery-transition-envelope.json');assert candidate_pin['sha256']==expected
assert not (A/'final-seal.json').exists() and not (A/'review-transition-authorized.command.json').exists()
q=load('docs/work/queue.json');workflow.validate(q,R)
t=next(t for t in q['tasks'] if t['id']=='IG-2B02');assert t['status']=='in_progress' and len(t['events'])==2 and t['events'][-1]['sha256']==pin(A/'claim.json')['sha256']
conf=load(AR+'/configuration.json');assert conf['session_id']==os.environ['CODEX_SESSION_ID']
metadata=Path(conf['metadata_path']);last=None
for raw in metadata.read_bytes().splitlines():
 record=json.loads(raw)
 if record['type']=='turn_context':last=(record,hashlib.sha256(raw).hexdigest())
record,record_hash=last;assert record['payload']['model']=='gpt-6.1-sol' and record['payload']['effort']=='high'
manifest=load(AR+'/delivery-manifest.json');candidate=load(AR+'/delivery-transition-envelope.json')
for p in manifest['new_reviewed_artifacts']+manifest['immutable_inputs_and_old_evidence']:assert pin(p['path'])==p,p['path']
for p in candidate['artifacts']:
 path=workflow.safe_path(R,p['path']);assert not workflow.denied(p['path']) and path.is_file() and workflow.digest(path)==p['sha256'],p['path']
write('operator-retry-authorization.json',{'role':'operator_authorization_observation','operator':'Current human operator in this conversation','recorded_by':conf['actor'],'observed_utc':now(),'authorization_basis':'Direct human answer to the pending question asking approval for delivery-transition-envelope.json and one retry of IG-2B02 -> review.','answer_english_rendering':'I approve the new envelope and one retry.','translation_note':'Faithful English rendering of the direct Polish operator answer received in this chat. This is operational authorization, not semantic acceptance.','approved_envelope':candidate_pin,'authorized_retry_count':1,'original_frozen_files_may_be_overwritten':False,'acceptance_or_done_authorized':False,'downstream_work_authorized':False})
write('authorized-review-preflight.json',{'outcome':'passed','task':'IG-2B02','actor':conf['actor'],'session_id':conf['session_id'],'current_configuration':{'model':record['payload']['model'],'reasoning':record['payload']['effort'],'evidence':'Own current session turn_context','timestamp':record['timestamp'],'record_sha256':record_hash,'metadata_path':metadata.as_posix()},'authorization':pin(A/'operator-retry-authorization.json'),'approved_envelope':candidate_pin,'current_status':t['status'],'current_event':t['events'][-1],'queue_before_retry':pin('docs/work/queue.json'),'original_frozen_artifacts_unchanged':True,'candidate_path_hash_rules_passed':True,'candidate_artifact_count':len(candidate['artifacts']),'next_operation':'Execute exactly one authorized retry; inspect actual state/event/hash regardless of exit before any further action.'})
print('AUTHORIZED RESUME PREFLIGHT PASSED',candidate_pin['sha256'])
