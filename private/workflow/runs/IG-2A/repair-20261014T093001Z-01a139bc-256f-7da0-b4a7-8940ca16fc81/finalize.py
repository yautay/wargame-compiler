"""Seal post-transition governance and command recovery without editing delivery."""
import importlib.util
import json
import sys
from datetime import datetime, timezone
from prepare import ROOT, RUN, OLD, REVIEW, sha, write, pin, command

delivery=json.loads((RUN/'delivery.json').read_text())
for artifact in delivery['artifacts']: assert sha(ROOT/artifact['path'])==artifact['sha256']
spec=importlib.util.spec_from_file_location('workflow',ROOT/'scripts/workflow.py')
w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
q=w.read_json(ROOT/w.QUEUE)
task=next(t for t in q['tasks'] if t['id']=='IG-2A')
assert task['status']=='review' and task['events'][-1]['sha256']==sha(RUN/'delivery.json')
# Restore LF serialization of generated governance without changing content.
(ROOT/w.QUEUE).write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
for path,body in w.views(q).items(): (ROOT/path).write_text(body,encoding='utf-8',newline='\n')
checks=[command('post-review-workflow',[sys.executable,'scripts/workflow.py','validate']),
        command('post-review-diff',['git','diff','--check'])]
assert all(c['exit_code']==0 for c in checks)
for artifact in delivery['artifacts']: assert sha(ROOT/artifact['path'])==artifact['sha256']
for artifact in json.loads((REVIEW/'review-manifest.json').read_text())['artifacts']:
    assert sha(ROOT/artifact['path'])==artifact['sha256']
write('freeze-01-clarification.json',{'artifact':pin(RUN/'freeze-01-failure.json'),
      'correction':'product_edits_after_passing_tests=false was imprecise: no semantic product edit occurred; schema CRLF serialization was restored after passing sources tests, with parsed equality verified in schema-byte-format.json. The handoff already records this distinction.',
      'frozen_artifact_unchanged':True})
base=json.loads((RUN/'queue-before.json').read_text(encoding='utf-8'))
assert [t for t in q['tasks'] if t['id']!='IG-2A']==[t for t in base['tasks'] if t['id']!='IG-2A']
governance=[pin(ROOT/path) for path in ['docs/work/queue.json','docs/work/context-policy.json','docs/work/tasks/IG-2A.md']]
write('governance-manifest.json',{'task':'IG-2A','queue_status':'review','artifacts':governance,
      'role':'coordinator','other_38_task_records_unchanged':True,'derived_views_validated':True,
      'note':'Queue/projection pins recorded after transition, outside immutable delivery to avoid queue-event hash cycles.'})
config=json.loads((RUN/'configuration.json').read_text()); end=datetime.now(timezone.utc)
start=datetime.fromisoformat(config['started_utc'])
write('final-measurement.json',{'actor':config['actor'],'started_utc':start.isoformat(),'ended_utc':end.isoformat(),
      'wall_seconds':(end-start).total_seconds(),'input_tokens':None,'output_tokens':None,'cost':None,
      'operator_seconds':None,'preliminary_reads_before_start_seconds':None,
      'unknown_reason':'No exposed task token/cost counters or operator-time report; earlier preliminary reads unmeasured.'})
write('checkpoint-sealed.json',{'task':'IG-2A','actor':config['actor'],'status':'review',
      'delivery':pin(RUN/'delivery.json'),'manifest':pin(RUN/'delivery-manifest.json'),
      'handoff':pin(RUN/'delivery-handoff.md'),'checks':checks,'blocker':None,
      'next_operation':'Separate independent review of this delivery and all five finding closure conditions; no executor self-approval or IG-2B.'})
included={a['path'] for a in delivery['artifacts']}
extras=[]
for path in sorted(RUN.rglob('*')):
    if not path.is_file() or path.name=='final-seal.json': continue
    rel=path.relative_to(RUN)
    if rel.parts[0] in {'t1','t2','t3'} or rel.parts[:2] in [('c','pytest'),('c','temp')]: continue
    if path.relative_to(ROOT).as_posix() not in included: extras.append(pin(path))
write('final-seal.json',{'task':'IG-2A','actor':config['actor'],'status':'review',
      'delivery':pin(RUN/'delivery.json'),'manifest':pin(RUN/'delivery-manifest.json'),
      'handoff':pin(RUN/'delivery-handoff.md'),'post_freeze_operational_artifacts':extras,
      'governance_artifacts':governance,'all_delivery_artifacts_verified':len(delivery['artifacts']),
      'checks':checks,'transition_recovery':pin(RUN/'transition-recovery.json'),
      'independent_review':'required_pending','semantic_acceptance_granted':False,
      'ended_utc':end.isoformat(),'tokens':None,'cost':None,'operator_seconds':None,
      'exclusions':'The final seal cannot include its own hash; operational scratch excluded as documented in delivery manifest.'})
print('Final status review;',len(delivery['artifacts']),'delivery artifacts and',len(extras),'post-freeze artifacts verified and sealed.')
print('Delivery SHA256:',sha(RUN/'delivery.json'))
print('Manifest SHA256:',sha(RUN/'delivery-manifest.json'))
print('Final seal SHA256:',sha(RUN/'final-seal.json'))
