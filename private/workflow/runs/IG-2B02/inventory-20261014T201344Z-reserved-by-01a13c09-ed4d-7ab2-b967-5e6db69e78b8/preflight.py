from ops import *
import importlib.metadata
started=now();verified={}
def verify(x):
 actual=pin(x['path']);assert actual['sha256']==x['sha256'] and ('bytes' not in x or actual['bytes']==x['bytes']),x['path'];verified[x['path']]=actual
def walk(o):
 if isinstance(o,dict):
  if {'path','sha256','bytes'}<=o.keys():verify(o)
  else:
   for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
for p,h,n in [(PK+'/manifest.json','0b117e04bde8f79c6a13a154b74abeec2f2fc8fc5091e398d8bc728736ca7be9',5563),(PK+'/context.txt','5a627465fe1de210d6c28ea9725d5a2584ee99c38f13cce926c97447e8e2138e',96228),(P+'/ready.json','17c54cff1ec12461d62c984d05797edb753cd2f933a80b41608c580884f82496',7990),(P+'/scope.json','8628a45c233d1a23a8976eb7047088d062037869c59f456b63143139fbce9168',16787),(P+'/dependency-verification.json','cd304d1e38e7e0afe2862e031696018b1f6526ceb0f05516648acd0251f992d8',3505),(P+'/toolchain.json','10e4c034b488fe44c6c6865f945278f83f1dec338d5572fac5b8db278ad54b27',4021),('src/wgc/contracts/source.py','14aa5fd5129ed5f6ae65937a3f646407c3f1433483aa2145b53f942ed43509b1',25536),('contracts/ig/source.schema.json','8593fb5f3929f72a97657593272c9089a34faeac74ce10a2f7a925a00fddab13',103222),('contracts/ig/README.md','c2d05b9cb20da646de21dc8b3f715799fae2006f06f322c7be800f0cb7e8db57',20706)]:verify({'path':p,'sha256':h,'bytes':n})
m=load(PK+'/manifest.json');q=load('docs/work/queue.json');assert pin('docs/work/queue.json')['sha256']==m['queue_sha256']
t=next(t for t in q['tasks'] if t['id']=='IG-2B02');assert t['status']=='ready' and len(t['events'])==1 and t['events'][0]['evidence']==P+'/ready.json' and t['events'][0]['sha256']==pin(P+'/ready.json')['sha256']
assert not any(t['status'] in ('in_progress','review','changes_requested','accepted') for t in q['tasks'])
assert all(next(t for t in q['tasks'] if t['id']==i)['status']=='done' for i in ('IG-2A','IG-2B01'))
sections=[]
for f in m['files']:
 verify(f)
 if Path(f['path']).suffix.lower() in ('.md','.json','.py','.ps1','.toml'):sections.append('\n--- FILE: '+f['path']+' ---\n'+(R/f['path']).read_text(encoding='utf-8-sig'))
payload='\n'.join(sections);assert len(payload.encode())==m['text_bytes'];assert payload.replace('\n','\r\n').encode()==(R/PK/'context.txt').read_bytes()
for f in ('source-pins.json','toolchain.json','dependency-verification.json'):walk(load(P+'/'+f))
for p in load(P+'/dependency-hash-audit.json')['immutable_files']:verify(p)
for i in ('IG-2A','IG-2B01'):
 for e in next(t for t in q['tasks'] if t['id']==i)['events']:assert pin(e['evidence'])['sha256']==e['sha256']
for p in load(P+'/ready.json')['artifacts']:verify(p)
conf=load(AR+'/configuration.json');assert conf['session_id']==os.environ['CODEX_SESSION_ID'] and conf['model']=='gpt-6.1-sol' and conf['reasoning']=='high'
old=load(P+'/toolchain.json');actual={'python':sys.version,'libraries':{n:importlib.metadata.version(n) for n in old['libraries']},'bundle_version':'26.1013.11914','native':{},'python_executable':pin(old['python_executable']['path']),'observed_utc':now()}
assert actual['python']==old['python'] and actual['libraries']==old['libraries']
for n,v in old['native'].items():
 c=run('version-'+n,[v['executable']['path'],'--version' if n in ('git','pwsh') else '-v']);assert c['exit_code']==0
 version=((R/c['stderr']['path']).read_text()+(R/c['stdout']['path']).read_text()).strip();assert version==v['version']
 actual['native'][n]={'executable':pin(v['executable']['path']),'version':version,'check':c}
actual.update(frozen_contract_and_tool_pins=old['frozen_contract_and_tool_pins'],workflow_and_checks=old['workflow_and_checks'],drift=[])
write('toolchain.json',actual);write('preflight.json',{'outcome':'passed','verified_input_pins':list(verified.values()),'queue_pin':pin('docs/work/queue.json'),'logical_text_bytes':len(payload.encode()),'physical_text_bytes':96228,'ready_event':t['events'][0],'no_active_task':True,'exclusive_owner':conf['actor'],'started_utc':started,'ended_utc':now()})
checks=[]
for label,args in [('preclaim-validate',[PY,'-B','scripts/workflow.py','validate']),('preclaim-next',[PY,'-B','scripts/workflow.py','next']),('baseline-validate',[PY,'-B','-m','wgc.sources','validate',load(P+'/scope.json')['baseline']['path']]),('initial-status',['git','status','--porcelain=v1']),('initial-diff-names',['git','diff','--name-only'])]:
 c=run(label,args);checks.append(c);assert c['exit_code']==0
write('existing-changes.json',{'tracked_modified_files':[pin(p) for p in (A/'initial-diff-names.stdout').read_text().splitlines() if (R/p).is_file()],'status':pin(A/'initial-status.stdout'),'policy':'Preserve every unrelated current change; no history access.'})
cp={'task':'IG-2B02','actor':conf['actor'],'session_id':conf['session_id'],'attempt':AR,'model':conf['model'],'reasoning':conf['reasoning'],'configuration_evidence':pin(A/'configuration.json'),'input_packet':pin(PK+'/manifest.json'),'input_context':pin(PK+'/context.txt'),'input_hashes':list(verified.values()),'base_owned_hashes':[],'current_owned_hashes':[pin(p) for p in A.iterdir() if p.is_file()],'completed_criteria':['Configuration/readiness/toolchain/packet preflight'],'unmet_criteria':t['acceptance'],'commands':checks,'blocker':None,'next_operation':'Claim only IG-2B02','started_utc':started,'updated_utc':now(),'exclusive_ownership':conf['actor']}
write('checkpoint.json',cp);write('preclaim-checkpoint.json',cp)
write('claim.json',{'role':'executor','actor':conf['actor'],'summary':'Claim only IG-2B02, physical pages 5-8 from accepted full baseline; stop at review.','model':conf['model'],'reasoning':conf['reasoning'],'configuration_evidence':pin(A/'configuration.json'),'criteria':t['acceptance'],'artifacts':[pin(A/f) for f in ('preclaim-checkpoint.json','preflight.json','configuration.json','toolchain.json')],'write_scope':t['write_scope'],'checks':checks,'exclusive_owner':conf['actor']})
print('PRECLAIM PASSED',len(verified),'input pins')
