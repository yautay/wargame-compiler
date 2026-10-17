"""Resume exact frozen IG-1C bytes after operator-confirmed reviewer configuration."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys

ROOT=Path.cwd()
RUN=Path(__file__).parent
ACTOR='ig1-stage-executor-20261013'
OLD=Path('private/workflow/runs/IG-1C/stage-20261013')
REVIEW=Path('private/workflow/runs/IG-1C/review-20261013T071955Z')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(name,data):
 with (RUN/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,indent=2);f.write('\n')
def art(p):return {'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)}
q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-1C')
delivery=read(OLD/'delivery.json')
assert sha(OLD/'delivery.json')=='8e3fc23cf3d64783b10c2f48287196b807272c2f5b356bcaabf35e695dbd9017'
for a in delivery['artifacts']:assert sha(a['path'])==a['sha256'],a['path']
cfg=read(REVIEW/'configuration-confirmed.json')
assert cfg['model']=='gpt-6.1-sol' and cfg['reasoning']=='high'
assert cfg['configuration_blocker_resolved'] is True
assert cfg['actor']!=ACTOR
if len(sys.argv)==1:
 assert t['status']=='blocked'
 write('queue-before.json',q)
 with (RUN/'reviewer-configuration-confirmed.json').open('xb') as f:f.write((REVIEW/'configuration-confirmed.json').read_bytes())
 write('resume-audit.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'frozen_delivery':art(OLD/'delivery.json'),'all_34_hashes_match':True,'configuration_blocker_resolved':True,'reviewer_configuration':art(REVIEW/'configuration-confirmed.json'),'dependent_statuses':{x['id']:x['status'] for x in q['tasks'] if x['stage']=='IG-1'},'product_edits':False,'executor_configuration_source':'Earlier direct operator UI observation in this same ongoing executor conversation: sol 6.1 high; no model/reasoning change requested or observed. Reviewer confirmation is independent.'})
 base={'role':'coordinator','actor':ACTOR,'criteria':t['start_conditions'],'artifacts':[art(RUN/'resume-audit.json'),art(RUN/'reviewer-configuration-confirmed.json'),art(OLD/'delivery.json')],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Same ongoing executor conversation direct operator UI confirmation; independent reviewer own UI confirmation copied into this run.'}
 write('replan.json',{**base,'summary':'Reviewer own Sol/high confirmed by direct operator UI observation; resolve exact configuration blocker and re-evaluate readiness; no product changes or new reviewer.'})
 write('ready.json',{**base,'summary':'IG-1B remains done, all frozen delivery/input hashes and existing ownership unchanged; current reviewer configuration blocker resolved. Ready only IG-1C to resume exact frozen delivery.'})
 print('Replan/readiness evidence prepared')
else:
 assert sys.argv[1]=='claim' and t['status']=='ready'
 packet=Path(sys.argv[2]);m=read(packet/'manifest.json')
 for a in m['files']:assert sha(a['path'])==a['sha256']
 assert sha(packet/'context.txt')==m['context_sha256']
 write('checkpoint.json',{'task':'IG-1C','actor':ACTOR,'attempt':'resume-20261013','started_utc':datetime.now(timezone.utc).isoformat(),'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct earlier operator UI observation in this same ongoing executor conversation: sol 6.1 high; same-session continuity, no settings change observed/requested.','input_packet':art(packet/'manifest.json'),'base_product_artifacts':delivery['artifacts'],'frozen_delivery':art(OLD/'delivery.json'),'product_changes':[],'next_operation':'Re-enter independent review of exact unchanged frozen delivery; existing independent reviewer creates its own fresh packet and completes review.','tokens':None,'cost':None})
 write('claim.json',{'role':'executor','actor':ACTOR,'summary':'Resume only ready IG-1C with new current packet/checkpoint and exact unchanged frozen product delivery; independent reviewer configuration now confirmed.','criteria':t['start_conditions'],'artifacts':[art(RUN/'checkpoint.json'),art(RUN/'reviewer-configuration-confirmed.json'),art(OLD/'configuration.json')],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct current-conversation operator UI confirmation retained with same-session continuity; no requested settings used as actual proof.'})
 print('Resume claim prepared')
