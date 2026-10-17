import copy, hashlib, importlib.metadata, json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path.cwd()
RUN=Path(__file__).parent
REL=RUN.relative_to(ROOT).as_posix()
ACTOR='codex-01a13b57-40e6-78d2-9d17-0b3e91afba77'
BASE='private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81'
CLOSE='private/workflow/runs/IG-2A/closure-20261014T115019Z-01a139bc-256f-7da0-b4a7-8940ca16fc81'
REVIEW='private/workflow/runs/IG-2A/review-20261014T104443Z-codex-01a13a03-b220-7181-a813-09f6e7b46c1f'
SOURCE='private/ig/sources/spqr-5e-official/revision-20261013T155212Z'
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def write(p,d):
 p=ROOT/p; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p); p=p if p.is_absolute() else ROOT/p
 b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def run(name,args):
 start=datetime.now(timezone.utc); t=time.monotonic()
 r=subprocess.run(args,capture_output=True,encoding='utf-8',errors='replace')
 (RUN/(name+'.stdout')).write_text(r.stdout,encoding='utf-8'); (RUN/(name+'.stderr')).write_text(r.stderr,encoding='utf-8')
 d={'command':subprocess.list2cmdline(args),'argv':args,'exit_code':r.returncode,'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t}
 write(f'{REL}/{name}.json',d); print(name,r.returncode,r.stdout[:350],r.stderr[:200]); return r

if __name__=='__main__':
 write(f'{REL}/configuration.json',{'actor':ACTOR,'session_id':os.environ.get('CODEX_THREAD_ID'),'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':{'kind':'direct_current_session_operator_confirmation','question':'Does this current chat run GPT-6.1 Sol / high?','answer':'Potwierdzam: GPT-6.1 Sol / high','basis':'Operator reply in this session before claim; not prior-session or requested configuration.'},'started_utc':'2026-10-14T16:51:00+00:00','start_basis':'Conservative approximate beginning of preliminary reads; exact timed operations recorded separately. Attempt directory created 2026-10-14T16:57:24Z.','tokens':None,'cost':None,'operator_seconds':None})
 q=read('docs/work/queue.json'); write(f'{REL}/queue-before.json',q); write(f'{REL}/context-policy-before.json',read('docs/work/context-policy.json'))
 expected={f'{CLOSE}/final-seal.json':'325477d5c86abbfa161dd26620aa947a7ec649fd7a7df1c47d640ed767079ba7',f'{REVIEW}/final-seal-corrected.json':'af1af2473a58e47ab69396bdf1d7f9dd39a765881bacab630068b87c2411b295',f'{BASE}/delivery.json':'c69df3b2867f440c6b330159a2d335dff6bf959192ebb9d3ac5d0ea59977195e',f'{SOURCE}/rulebook.pdf':'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'}
 checks=[]
 for p,h in expected.items():
  x=pin(p); assert x['sha256']==h,p; checks.append(x)
 # Read complete JSON records without dumping their large artifact arrays.
 for p in [f'{CLOSE}/accepted.json',f'{CLOSE}/done.json',f'{BASE}/delivery-manifest.json',f'{BASE}/inventory-one/inventory.json',f'{BASE}/inventory-one/identity-registry.json',f'{BASE}/verified-inventory.json',f'{REVIEW}/coordinator-handoff-final.json']:
  d=read(p); checks.append(pin(p))
  print(p,'read',len(d.get('artifacts',[])))
  for a in d.get('artifacts',[]):
   assert pin(a['path'])['sha256']==a['sha256'],a['path']
 # Verify seals' direct pinned references (historical queue pins are observations, not live assertions).
 for seal in [f'{CLOSE}/final-seal.json',f'{REVIEW}/final-seal-corrected.json']:
  for k,v in read(seal).items():
   if k!='queue' and isinstance(v,dict) and 'path' in v and 'sha256' in v: assert pin(v['path'])['sha256']==v['sha256'],v
 t=next(x for x in q['tasks'] if x['id']=='IG-2A'); assert t['status']=='done'
 for e in t['events'][-2:]: assert pin(e['evidence'])['sha256']==e['sha256']
 baseline=read(f'{BASE}/inventory-one/inventory.json'); assert baseline['registry']==read(f'{BASE}/inventory-one/identity-registry.json')
 write(f'{REL}/dependency-verification.json',{'dependency':'IG-2A','status':'done','pins':checks,'delivery_members_verified':len(read(f'{BASE}/delivery-manifest.json')['artifacts']),'review':'PASS; R01-R05 closed in corrected final handoff','baseline_inventory':pin(f'{BASE}/inventory-one/inventory.json'),'persisted_registry':pin(f'{BASE}/inventory-one/identity-registry.json'),'verified_inventory':pin(f'{BASE}/verified-inventory.json'),'source_ig_semantic_acceptance':False})
 files=['scripts/workflow.py','scripts/check.ps1','scripts/search.ps1','contracts/ig/README.md','contracts/ig/regions.schema.json','contracts/ig/source.schema.json','src/wgc/contracts/source.py']
 files += [p.as_posix() for p in Path('src/wgc/sources').glob('*.py')]
 write(f'{REL}/base-products.json',{'files':[pin(p) for p in files]})
 runtime=Path('C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies')
 native=runtime/'native/poppler/Library/bin'; libs=runtime/'python/Lib/site-packages'
 os.environ['PYTHONPATH']=str(ROOT/'src')+';'+str(ROOT/'.venv/Lib/site-packages')+';'+str(libs)
 os.environ['PATH']=str(native)+';'+os.environ['PATH']; os.environ['PYTHONDONTWRITEBYTECODE']='1'; os.environ['PYTHONIOENCODING']='utf-8'
 sys.path[:0]=[str(ROOT/'src'),str(libs)]
 tools={}
 for n in ['pdfinfo','pdftoppm']:
  p=native/(n+'.exe'); b=p.read_bytes(); r=subprocess.run([str(p),'-v'],capture_output=True,text=True); tools[n]={'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'version':r.stdout+r.stderr,'exit_code':r.returncode}
 write(f'{REL}/toolchain.json',{'python':sys.version,'python_executable':sys.executable,'python_sha256':hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),'libraries':{n:importlib.metadata.version(n) for n in ['pypdf','pdfplumber','Pillow','pytest']},'native':tools,'process_pythonpath':os.environ['PYTHONPATH'],'process_path_prefix':str(native),'installs':0})
 task=next(x for x in q['tasks'] if x['id']=='IG-2B01')
 task['title']='Inventory SPQR PDF pages 01-04'
 task['outputs']=[f'{REL}/authored/inventory.json (full 44-page wgc-inventory-1; only physical pages 1-4 authored)',f'{REL}/authored/identity-registry.json',f'{REL}/evidence/ (separate region text, PNG, crop PDF)',f'{REL}/region-ledger.json, scope-report.json, continuations.json, gaps.json',f'{REL}/delivery-manifest.json, delivery.json, delivery-handoff.md']
 task['write_scope']=[REL+'/', 'private/workflow/packets/IG-2B01-/', 'private/workflow/checks/']
 task['inputs']=[f'{SOURCE}/rulebook.pdf SHA256 {expected[f"{SOURCE}/rulebook.pdf"]}; 44 physical pages; substantive analysis pages 1-4 only',f'{SOURCE}/provenance.json SHA256 '+pin(f'{SOURCE}/provenance.json')['sha256'],f'Accepted wgc-inventory-1 tooling and persisted baseline/registry: {BASE}/inventory-one/; exact hashes verified in dependency-verification.json','Retain unchanged pages and full-page placeholders 5-44. Retire page 1-4 placeholder membership but preserve registry entries; new explicit authored keys do not remap old identities.','Physical page 5 permitted only for minimal specifically documented continuation context; never included in task denominator. No content analysis pages 6-44.']
 task['context']=['docs/work/EVIDENCE.md','src/wgc/sources/README.md','contracts/ig/README.md','contracts/ig/regions.schema.json',f'{SOURCE}/provenance.json',f'{SOURCE}/rulebook.pdf',f'{REL}/configuration.json',f'{REL}/dependency-verification.json',f'{REL}/scope.json']
 task['tests']=['Root validate exact source, locators, evidence freshness, geometry and PNG dimensions; inspect full pages 1-4 visually.','Complete page-region ledger and explicit geometric/content gaps; separate task denominator from unchanged 40 placeholders and any context-only regions.','Cross-boundary continuation/context scope check; persisted-registry replay and canonical/identity repeatability.','scripts/check.ps1 -Task IG-2B01 while active; scripts/workflow.py validate; git diff --check.']
 write(f'{REL}/scope.json',{'task':'IG-2B01','actor':ACTOR,'content_pages':[1,2,3,4],'structural_pages':list(range(1,45)),'conditional_context':{'page':5,'constraint':'Only exact continuation from page 4; record access bbox/reason before extraction.'},'representation':'Unmodified wgc-inventory-1 full 44-page accounting; scoped sidecar counts authored inventory regions on pages 1-4 only. Pages/placeholder records 5-44 byte-equivalent as JSON records.','coverage_policy':'Evidence existence does not grant representation. Keep all semantic levels unprocessed; transcription partial until exact text/image reconciliation. Editorial classification never grants exclusion. No human approval fabricated.','registry':'Extend accepted persisted registry; retain retired placeholders. Explicit split lineage in sidecar; no automatic identity transfer or source remapping.','outputs':task['outputs'],'write_scope':task['write_scope'],'stop_at':'review; separate independent review required'})
 write('docs/work/queue.json',q)
 policy=read('docs/work/context-policy.json')
 needed=[f'{REL}/configuration.json',f'{REL}/dependency-verification.json',f'{REL}/scope.json',f'{BASE}/inventory-one/inventory.json',f'{BASE}/inventory-one/identity-registry.json',f'{BASE}/verified-inventory.json']
 for p in needed:
  if p not in policy['allow']: policy['allow'].append(p)
 write('docs/work/context-policy.json',policy)
 r=run('coordinator-render',[sys.executable,'scripts/workflow.py','render']); assert r.returncode==0
 r=run('coordinator-validate',[sys.executable,'scripts/workflow.py','validate']); assert r.returncode==0
 evidence={'role':'coordinator','actor':ACTOR,'summary':'Refined only IG-2B01; exact accepted dependency verified; full-source representation and bounded content scope pinned.','model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct operator confirmation in current session, recorded configuration.json.','criteria':task['acceptance'],'artifacts':[pin(f'{REL}/scope.json'),pin(f'{REL}/dependency-verification.json'),pin(f'{REL}/configuration.json')]}
 write(f'{REL}/ready.json',evidence)
 r=run('ready-transition',[sys.executable,'scripts/workflow.py','transition','--task','IG-2B01','--to','ready','--evidence',f'{REL}/ready.json'])
 if r.returncode: raise RuntimeError('Inspect committed queue event before recovery or retry')
 r=run('packet-command',[sys.executable,'scripts/workflow.py','packet','--task','IG-2B01']); assert r.returncode==0
 packet=r.stdout.strip(); manifest=read(packet+'/manifest.json')
 for a in manifest['files']: assert pin(a['path'])['sha256']==a['sha256']
 assert pin(packet+'/context.txt')['sha256']==manifest['context_sha256']
 write(f'{REL}/input-packet.json',{'manifest':pin(packet+'/manifest.json'),'context':pin(packet+'/context.txt'),'queue_sha256':manifest['queue_sha256'],'all_files_verified':True})
 checkpoint={'task':'IG-2B01','attempt':REL,'actor':ACTOR,'model':'gpt-6.1-sol','reasoning':'high','configuration':pin(f'{REL}/configuration.json'),'base_files':read(f'{REL}/base-products.json')['files'],'input_packet':pin(f'{REL}/input-packet.json'),'completed_criteria':[],'commands':['coordinator-validate.json','ready-transition.json','packet-command.json'],'blocker':None,'next_operation':'Claim then inspect original physical pages 1-4; author complete bounded region ledger.'}
 write(f'{REL}/checkpoint-preclaim.json',checkpoint); write(f'{REL}/checkpoint.json',checkpoint)
 evidence.update(role='executor',summary='Claim exact IG-2B01 content scope with current-session operator-confirmed Sol/high and verified packet.',artifacts=[pin(f'{REL}/checkpoint-preclaim.json'),pin(f'{REL}/input-packet.json'),pin(f'{REL}/configuration.json')])
 write(f'{REL}/claim.json',evidence)
 r=run('claim-transition',[sys.executable,'scripts/workflow.py','transition','--task','IG-2B01','--to','in_progress','--evidence',f'{REL}/claim.json'])
 if r.returncode: raise RuntimeError('Inspect committed event before recovery or retry')
