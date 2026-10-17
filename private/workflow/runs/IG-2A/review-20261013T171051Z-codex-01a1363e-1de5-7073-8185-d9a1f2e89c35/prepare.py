import datetime, hashlib, importlib.util, json, os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
ATTEMPT = ROOT/'private/workflow/runs/IG-2A/attempt-20261013T155212Z'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, data): (OUT/name).write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8', newline='\n')
q = json.loads((ROOT/'docs/work/queue.json').read_text(encoding='utf-8-sig'))
task = next(t for t in q['tasks'] if t['id']=='IG-2A')
assert task['status']=='review'
expected = {'delivery.json':'31a175fb77f14a586f03327c3674a05a4b4ae9f7296932ef757669428d454290','delivery-manifest.json':'d283e0054a515995803a6c17fb8c31606cf23f206ad4454be68291a1459cfa1c','delivery-handoff.md':'d50e607d60ac23a1f5948d0f0edaa811dc344f6ce8bc1a7230fe2d7f80314135'}
pins = [{'path':str((ATTEMPT/n).relative_to(ROOT)).replace('\\','/'),'expected_sha256':h,'actual_sha256':sha(ATTEMPT/n)} for n,h in expected.items()]
delivery = json.loads((ATTEMPT/'delivery.json').read_text())
artifacts=[]
for a in delivery['artifacts']:
    p=ROOT/a['path']
    artifacts.append({**a,'actual_sha256':sha(p),'bytes':p.stat().st_size,'matches':sha(p)==a['sha256']})
save('reviewed-artifact-manifest.json', {'delivery_pins':pins,'artifacts':artifacts,'queue_sha256':sha(ROOT/'docs/work/queue.json'),'task':task})
assert len(artifacts)==87
assert all(a['matches'] for a in artifacts) and all(a['expected_sha256']==a['actual_sha256'] for a in pins)
spec=importlib.util.spec_from_file_location('wgc_workflow',ROOT/'scripts/workflow.py')
wf=importlib.util.module_from_spec(spec);spec.loader.exec_module(wf)
packet=wf.packet(q,ROOT,'IG-2A',output=False)
sections=[]
for f in packet['files']:
    p=wf.safe_path(ROOT,f['path'])
    assert wf.permitted(ROOT,f['path']) and sha(p)==f['sha256']
    if p.suffix.lower() in {'.md','.json','.py','.ps1','.toml'}:
        sections.append('\n--- FILE: '+f['path']+' ---\n'+p.read_text(encoding='utf-8-sig'))
(OUT/'context.txt').write_text('\n'.join(sections),encoding='utf-8',newline='\n')
packet['context_sha256']=sha(OUT/'context.txt')
save('packet-manifest.json',packet)
old=ROOT/'private/workflow/packets/IG-2A-8108c7c22a77477296f0af21fe898f92'
om=json.loads((old/'manifest.json').read_text()); oc=(old/'context.txt').read_text(encoding='utf-8')
assert sha(old/'context.txt')==om['context_sha256']
save('packet-verification.json',{'fresh_queue_matches':packet['queue_sha256']==sha(ROOT/'docs/work/queue.json'),'old_queue_sha256':om['queue_sha256'],'old_context_hash_verified':True,'old_context_sections':[s.split(' ---\n',1)[0] for s in oc.split('\n--- FILE: ')[1:]],'fresh_files_verified':len(packet['files']),'workflow_script_sha256':sha(ROOT/'scripts/workflow.py'),'output_false_reason':'Use unchanged workflow.packet allowlist/validation; caller serializes only inside reviewer directory.'})
status=subprocess.run(['git','status','--porcelain=v1','-z'],cwd=ROOT,capture_output=True)
(OUT/'git-status-before.bin').write_bytes(status.stdout)
save('checkpoint.json',{'role':'reviewer','actor':'codex-'+os.environ['CODEX_THREAD_ID'],'executor':delivery['actor'],'started_utc':'2026-10-13T17:06:40Z','configuration':{'model':None,'reasoning':None,'reason':'Awaiting current-session operator confirmation'},'queue_sha256':sha(ROOT/'docs/work/queue.json'),'frozen_artifacts':87,'git_status_exit':status.returncode,'setup_observations':['Root toolchain.json lookup failed; exact attempt/toolchain.json located and read.','Initial status output was verbose; subsequent status is captured as bytes only.']})
print(json.dumps({'out':str(OUT),'status':task['status'],'artifacts':len(artifacts),'mismatches':sum(not a['matches'] for a in artifacts),'fresh_packet_files':len(packet['files']),'reviewer':'codex-'+os.environ['CODEX_THREAD_ID']}))
