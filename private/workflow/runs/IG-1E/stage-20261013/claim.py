"""Verify the fresh IG-1E packet, pins and executor continuity before claiming."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
RUN=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def art(p):return {'path':str(p).replace('\\','/'),'sha256':sha(p)}
def write(n,d):
 with (RUN/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
packet_path='private/workflow/packets/IG-1E-18802d95b9564aaf9ee661c8770e4158/manifest.json'
packet=read(packet_path);assert packet['queue_sha256']==sha('docs/work/queue.json')
for a in packet['files']:assert sha(a['path'])==a['sha256'],a['path']
for a in read(RUN/'input-contract.json')['pinned_inputs']:assert sha(a['path'])==a['sha256'],a['path']
q=read('docs/work/queue.json');task=next(t for t in q['tasks'] if t['id']=='IG-1E')
assert task['status']=='ready' and next(t for t in q['tasks'] if t['id']=='IG-1D')['status']=='done'
configuration=art('private/workflow/runs/IG-1D/resume-audit-20261013T134548Z/configuration-confirmed.json')
common={'task':'IG-1E','actor':'ig1-continuation-executor-20261013','model':'gpt-6.1-sol','reasoning':'high',
 'configuration_evidence':configuration,'same_executor_chat_continuity':True}
write('checkpoint.json',{**common,'started_utc':datetime.now(timezone.utc).isoformat(),
 'input_packet':art(packet_path),'pinned_inputs_verified':True,'changed_file_hashes':[],
 'allowed_write_scope':task['write_scope'],'tokens':None,'cost':None,'operator_time_seconds':None,
 'next_operation':'Implement public synthetic integration controls, two full imports and independent complete accounting, then seal/repeat the structural snapshot with all gaps and uncertainty retained.'})
write('claim.json',{**common,'role':'executor','summary':'Claim IG-1E after IG-1D independent acceptance/done, exact readiness refinement and fresh allowlisted packet verification.',
 'criteria':task['acceptance'],'artifacts':[art('private/workflow/runs/IG-1E/stage-20261013/checkpoint.json'),art('private/workflow/runs/IG-1E/stage-20261013/input-contract.json')]})
print('Fresh IG-1E packet and all pinned bytes verified; same confirmed executor chat; claim ready.')
