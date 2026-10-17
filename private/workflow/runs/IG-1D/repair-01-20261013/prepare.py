"""First bounded repair claim for exact independent IG1D-R01/R02/R03/R04 findings."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path.cwd();R=Path(__file__).parent
REVIEW=Path('private/workflow/runs/IG-1D/review-20261013T122807Z/review.json')
DELIVERY=Path('private/workflow/runs/IG-1D/preflight-20261013/delivery.json')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def art(p):return {'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)}
def write(n,d):
 with (R/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
review=read(REVIEW);delivery=read(DELIVERY)
assert sha(REVIEW)=='ef9955c57e22a85ecd76a54ea08fda9dcfedbba7419cfc85ff91497abf468b00'
assert review['technical_result']=='changes_requested' and len(review['findings'])==4
for a in review['artifacts']+delivery['artifacts']:assert sha(a['path'])==a['sha256']
q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-1D');assert t['status']=='changes_requested'
base=[]
for name in ['src/wgc/wgu_adapter/identity.py','src/wgc/wgu_adapter/references.py','src/wgc/export/source.py','tests/wgu_adapter/test_identity.py','tests/wgu_adapter/test_references.py','tests/export/test_source.py']:
 p=Path(name);copy=R/'baseline'/name;copy.parent.mkdir(parents=True,exist_ok=True)
 with copy.open('xb') as f:f.write(p.read_bytes())
 base.append({'original':art(p),'preserved_copy':art(copy)})
write('baseline-manifest.json',{'parent_delivery':art(DELIVERY),'files':base})
scope={'parent_review':art(REVIEW),'parent_delivery':art(DELIVERY),'finding_iterations':[{
    'finding_id':f['id'],'repair_iteration':1,'maximum':2,'required_change':f['required_change'],
    'required_verification':f['required_verification']} for f in review['findings']],
    'write_scope':t['write_scope'],'scope_expansion':False,'prior_packages_reports_preserved':True}
write('repair-scope.json',scope)
write('checkpoint.json',{'task':'IG-1D','actor':'ig1-stage-executor-20261013','started_utc':datetime.now(timezone.utc).isoformat(),
    'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Earlier direct current-conversation operator UI observation with same-session continuity: sol 6.1 high; no settings change requested/observed.',
    'base_files':base,'parent_review':art(REVIEW),'parent_delivery':art(DELIVERY),'repair_iterations':scope['finding_iterations'],
    'next_operation':'Repair contradictory evidence, overlapping decisions, direct active IDs and unique explicit merge-child replay; strict original probes and full private reproducibility; same independent reviewer re-review.',
    'tokens':None,'cost':None})
write('claim.json',{'role':'executor','actor':'ig1-stage-executor-20261013','summary':'Claim first bounded repair for independent IG1D-R01/R02/R03/R04; preserve all prior hashes/versions and original strict probes; no task scope expansion or source/semantic acceptance.',
    'criteria':t['acceptance'],'artifacts':[art(R/n) for n in ['checkpoint.json','repair-scope.json','baseline-manifest.json']],
    'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Same ongoing executor conversation direct earlier operator UI confirmation; unchanged settings.'})
print('First bounded repair prepared for four independent findings')
