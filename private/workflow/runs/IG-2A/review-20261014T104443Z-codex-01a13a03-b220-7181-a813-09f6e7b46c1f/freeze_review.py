from support import *
from datetime import datetime

assert not (RUN/'review-manifest.json').exists()
assert not (RUN/'final-seal.json').exists()
assert read(RUN/'review.json')['outcome']=='PASS'
assert read(RUN/'findings.json')['actionable_findings']==[]
assert digest(ROOT/'docs/work/queue.json')=='18621ef45410770936da05949da3c434a9aedf262e50f18db3fc5d90ad809386'
# Check frozen external input pins once more immediately before the final seal.
verified=[]
for entry in read(REPAIR/'delivery.json')['artifacts']:
    assert digest(ROOT/entry['path'])==entry['sha256'],entry['path']
    verified.append(entry)
for entry in read(REPAIR/'final-seal.json')['post_freeze_operational_artifacts']+read(REPAIR/'final-seal.json')['governance_artifacts']:
    assert digest(ROOT/entry['path'])==entry['sha256'],entry['path']
assert len(verified)==273
files=[]
for path in sorted(RUN.rglob('*')):
    if path.is_symlink() or path.is_junction():raise ValueError('Linked reviewer output forbidden')
    if path.is_file():files.append(pin(path))
manifest={'format':'wgc-independent-review-manifest-1','task':'IG-2A','actor':read(RUN/'configuration.json')['actor'],'outcome':'PASS','artifacts':files,'artifact_count':len(files),'reviewed_delivery_manifest':pin(REPAIR/'delivery-manifest.json'),'reviewed_delivery_artifacts':verified,'exclusions':['review-manifest.json excludes itself; final-seal.json is written after this manifest and seals it. No operational scratch is excluded.'],'created_utc':utc()}
write('review-manifest.json',manifest)
for entry in files:
    assert digest(ROOT/entry['path'])==entry['sha256']
started=read(RUN/'configuration.json')['started_utc'];ended=utc()
seal={'task':'IG-2A','actor':read(RUN/'configuration.json')['actor'],'outcome':'PASS','manifest':pin(RUN/'review-manifest.json'),'review':pin(RUN/'review.json'),'handoff':pin(RUN/'coordinator-handoff.json'),'report':pin(RUN/'report.md'),'configuration':pin(RUN/'configuration.json'),'criteria':pin(RUN/'criteria.json'),'dispositions':pin(RUN/'dispositions.json'),'delivery':pin(REPAIR/'delivery.json'),'delivery_manifest':pin(REPAIR/'delivery-manifest.json'),'delivery_handoff':pin(REPAIR/'delivery-handoff.md'),'delivery_final_seal':pin(REPAIR/'final-seal.json'),'queue_sha256':digest(ROOT/'docs/work/queue.json'),'queue_status':'review','all_273_delivery_artifacts_unchanged':True,'all_manifest_artifacts_verified':len(files),'workflow_IG1A_source_old_reviews_preserved':True,'model':'gpt-6.1-sol','reasoning':'high','started_utc':started,'ended_utc':ended,'wall_seconds':(datetime.fromisoformat(ended)-datetime.fromisoformat(started.replace('Z','+00:00'))).total_seconds(),'input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,'semantic_acceptance_granted':False,'acceptance_transition_performed':False,'IG2B_executed':False,'exclusions':'Final seal cannot include its own hash. Review manifest contains every other reviewer file, including full operational scratch. Final seal hash is returned to the operator.'}
write('final-seal.json',seal)
print(json.dumps({'outcome':'PASS','manifest':pin(RUN/'review-manifest.json'),'final_seal':pin(RUN/'final-seal.json'),'review_files':len(files),'wall_seconds':seal['wall_seconds']},indent=2))
