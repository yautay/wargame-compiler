"""Claim first bounded product repair for independently identified IG1C-R01/R02/R03."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
ROOT=Path.cwd();RUN=Path(__file__).parent
REVIEW=Path('private/workflow/runs/IG-1C/review-20261013T092949Z/review.json')
DELIVERY=Path('private/workflow/runs/IG-1C/resume-20261013/delivery.json')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def art(p):return {'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)}
def write(n,d):
 with (RUN/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
review=read(REVIEW);delivery=read(DELIVERY)
assert sha(REVIEW)=='333ca0ae84342bffc103045c5ad1ea1ee2dbc8f104764d2ce4db2255a8c0f48e'
assert review['technical_result']=='changes_requested'
for a in review['artifacts']+delivery['artifacts']:assert sha(a['path'])==a['sha256'],a['path']
q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-1C');assert t['status']=='changes_requested'
base=[]
for name in ['src/wgc/wgu_adapter/parser.py','src/wgc/wgu_adapter/importer.py','tests/wgu_adapter/test_importer.py']:
 p=Path(name);copy=RUN/'baseline'/name;copy.parent.mkdir(parents=True,exist_ok=True)
 with copy.open('xb') as f:f.write(p.read_bytes())
 base.append({'original':art(p),'preserved_copy':art(copy)})
write('baseline-manifest.json',{'parent_delivery':art(DELIVERY),'files':base})
schema=Path('C:/repo/wargame-utils/wgu/schemas/kb.schema.json')
assert sha(schema)=='0a93858ed3e0d99382ea962350e3b2994fab90b872a8b86584519b5a9e33a551'
with (RUN/'pinned-wgu-schema.json').open('xb') as f:f.write(schema.read_bytes())
scope={'review':art(REVIEW),'parent_delivery':art(DELIVERY),'finding_iterations':[{'finding_id':f['id'],'repair_iteration':1,'maximum':2,'required_change':f['required_change'],'required_verification':f['required_verification']} for f in review['findings']],'product_write_scope':t['write_scope'],'scope_changes':False,'hypothesis':'Normalize only malformed built-in scalar-constructor exceptions with node locations; validate pinned known WGU schema types/enums/nested shapes while retaining unknown extensions and explicit integer step numbering extension; support unconstrained confusables item values.','old_output_preservation':'Do not overwrite prior private import output; repaired corpus output uses a new import run directory.'}
write('repair-scope.json',scope)
write('checkpoint.json',{'task':'IG-1C','actor':'ig1-stage-executor-20261013','started_utc':datetime.now(timezone.utc).isoformat(),'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct earlier operator UI confirmation in this same ongoing executor conversation: sol 6.1 high; no settings change requested/observed.','base_files':base,'parent_review':art(REVIEW),'parent_delivery':art(DELIVERY),'input_packet':read('private/workflow/runs/IG-1C/resume-20261013/checkpoint.json')['input_packet'],'repair_iterations':scope['finding_iterations'],'next_operation':'Implement bounded repairs; run strict original reviewer probes, new regressions, independent full accounting and current project checks; freeze new hashes and obtain same independent reviewer re-review.','tokens':None,'cost':None})
write('claim.json',{'role':'executor','actor':'ig1-stage-executor-20261013','summary':'Claim first bounded product repair cycle for independent findings IG1C-R01/R02/R03; preserve baseline/current deliveries and original strict reviewer probes; no task scope or dependency expansion.','criteria':t['acceptance'],'artifacts':[art(RUN/n) for n in ['checkpoint.json','repair-scope.json','baseline-manifest.json','pinned-wgu-schema.json']],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct earlier current-conversation operator UI confirmation with same-session continuity; no configuration change observed/requested.'})
print('First bounded repair claim prepared for 3 findings')
