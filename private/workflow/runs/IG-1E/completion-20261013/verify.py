"""Verify independent IG-1E acceptance before coordinator status transitions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,time
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent;REVIEW=Path(sys.argv[1])
DELIVERY=Path('private/workflow/runs/IG-1E/stage-20261013/delivery.json')
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def art(p):return {'path':Path(p).as_posix(),'sha256':sha(p)}
def write(n,d):
 with (RUN/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
start=datetime.now(timezone.utc);tick=time.perf_counter()
assert sha(DELIVERY)=='5a2d7595085ef19877f921da96ea79647493ed73a813b5ce29b36d80b4f60e54'
assert sha(REVIEW/'review.json')=='46d0afa7c9b0c302934e535d4ab2c59c6a879b9ed0114baf30b26e6f22c069f4'
assert sha(REVIEW/'review-manifest.json')=='97a5e723ed7f6ac8aa09fd1ce2d33eac7bb89ec8210f7b12add3f4aaf845bc0c'
assert sha(REVIEW/'acceptance-evidence.json')=='57a82596add83677621e377d54e292d1c047c6b3dfc3427f59c752c87d5d0bca'
review=read(REVIEW/'review.json');acceptance=read(REVIEW/'acceptance-evidence.json');delivery=read(DELIVERY)
assert review['technical_result']=='pass' and review['technical_pass'] and review['independent_pass']
assert not review['findings'] and all(c['result']=='pass' for c in review['criteria_results'])
assert acceptance['role']=='reviewer' and acceptance['actor']!=delivery['actor']
assert acceptance['artifacts']==delivery['artifacts']
assert all(c['exit_code']==0 for c in acceptance['checks'])
for a in read(REVIEW/'review-manifest.json')['artifacts']:assert sha(a['path'])==a['sha256'],a['path']
for a in delivery['artifacts']:assert sha(a['path'])==a['sha256'],a['path']
preserved=read('private/workflow/runs/IG-1E/stage-20261013/preservation.json')
for a in preserved['accepted_foundation_artifacts']+preserved['pinned_inputs']:assert sha(a['path'])==a['sha256'],a['path']
q=read('docs/work/queue.json');task=next(t for t in q['tasks'] if t['id']=='IG-1E')
assert task['status']=='review' and not task['semantic_acceptance_required']
assert acceptance['criteria']==task['acceptance']
report=read('private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013/acceptance-report.json')
assert report['two_imports_and_two_transforms_and_two_seals_byte_identical']
assert report['independent_record_counts']=={'processed':1655,'raw':37,'error':0}
assert not report['semantic_acceptance_granted'] and not report['publisher_source_coverage_granted'] and not report['executable_readiness_granted']
write('verification.json',{'task':'IG-1E','technical_gates':'passed','delivery':art(DELIVERY),
 'independent_review':art(REVIEW/'review.json'),'review_manifest':art(REVIEW/'review-manifest.json'),
 'acceptance_evidence':art(REVIEW/'acceptance-evidence.json'),'all_delivery_hashes_verified':True,
 'all_prerequisites_preserved':True,'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
 'wall_seconds':time.perf_counter()-tick,'input_tokens':None,'output_tokens':None,'cost':None,'operator_time_seconds':None})
write('done.json',{'role':'coordinator','actor':'ig1-continuation-executor-20261013',
 'summary':'Every IG-1E technical gate independently passed on the exact full-input delivery and sealed structural snapshot; coordinator verifies exact bytes, entire accounting and preserved foundations. No semantic/source-coverage/executable acceptance.',
 'criteria':task['acceptance'],'artifacts':delivery['artifacts'],'checks':acceptance['checks'],
 'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':delivery['configuration_evidence'],
 'independent_review':art(REVIEW/'review.json'),'independent_review_manifest':art(REVIEW/'review-manifest.json'),
 'coordinator_verification':art(Path('private/workflow/runs/IG-1E/completion-20261013/verification.json')),
 'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False})
print(json.dumps({'review':art(REVIEW/'review.json'),'acceptance':art(REVIEW/'acceptance-evidence.json'),'verified_artifacts':len(delivery['artifacts'])}))
