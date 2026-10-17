from ops import *
import time
from wgc.sources.pdf import extract_evidence
from wgc.sources.inventory import validate
from wgc.contracts.source import canonical_bytes
doc=load(AR+'/authored/inventory.json');s=load(P+'/scope.json')
for p in (s['baseline'],s['registry']):assert pin(p['path'])==p
new=[r for r in doc['regions'] if r['key'].startswith('ig2b02:')]
assert len(new)==141
validate(doc,R)
(A/'evidence-records').mkdir(exist_ok=False)
out=[]
for n,r in enumerate(new,1):
 started=now();clock=time.monotonic();page=next(p['pdf_page'] for p in doc['pages'] if p['id']==r['page_id'])
 directory=AR+'/evidence/'+r['id'].split(':')[1]
 ev=extract_evidence(doc,r['id'],R,directory,dpi=144,pdftoppm=POP+'/pdftoppm.EXE')
 with (A/'evidence-records'/('region-'+r['id'].split(':')[1]+'.json')).open('xb') as f:f.write(canonical_bytes(ev)+b'\n')
 out.append(ev)
 write('evidence-increment-'+str(n).zfill(3)+'.json',{'region':r['id'],'revision':r['revision'],'key':r['key'],'pdf_page':page,'operation':'Unchanged wgc.sources.pdf.extract_evidence(doc, exact_new_id, repo_root, fresh_uuid_directory, dpi=144, pinned_pdftoppm)','script':pin(A/'derive-evidence.py'),'evidence':ev,'started_utc':started,'ended_utc':now(),'wall_seconds':time.monotonic()-clock})
 print('EXTRACTED',n,'/',len(new),'page',page,r['key'],flush=True)
 if n in (39,72,111,141):checkpoint('evidence-'+str(n),['Authoring and original/overlay inspection','Exact new evidence triples: '+str(n)],'Continue exact new-ID extraction or finalize/audit at 141')
write('new-evidence.json',out)
print('ALL NEW EVIDENCE READY',len(out),flush=True)
