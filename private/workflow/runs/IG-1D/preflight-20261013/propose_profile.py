"""Prepare a reviewable timestamp/profile decision without changing frozen contracts."""
from pathlib import Path
from datetime import datetime,timezone
import copy,difflib,hashlib,json
R=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,data):
 with (R/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,indent=2);f.write('\n')
q=json.loads(Path('docs/work/queue.json').read_text());by={t['id']:t for t in q['tasks']}
assert by['IG-1C']['status']=='done' and by['IG-1D']['status']=='planned'
c_delivery=Path('private/workflow/runs/IG-1C/repair-01-20261013/delivery.json')
for a in json.loads(c_delivery.read_text())['artifacts']:assert sha(a['path'])==a['sha256']
base_path=Path('contracts/ig/source.schema.json');base=json.loads(base_path.read_text());profile=copy.deepcopy(base)
assert sha(base_path)=='8593fb5f3929f72a97657593272c9089a34faeac74ce10a2f7a925a00fddab13'
assert base['$defs']['run_data']['properties']['started_utc']=={'type':'string','minLength':1}
profile['$id']='urn:wgc:ig:source-export:1'
profile['title']='WGC deterministic source export profile 1'
changes=[]
def version(value,pointer=''):
 if isinstance(value,dict):
  for k,v in value.items():
   if k=='schema_version' and isinstance(v,dict) and v.get('const')=='wgc-source-1':
    v['const']='wgc-source-export-1';changes.append(pointer+'/'+k+'/const')
   else:version(v,pointer+'/'+k)
 elif isinstance(value,list):
  for i,v in enumerate(value):version(v,pointer+'/'+str(i))
version(profile)
for key in ['started_utc','ended_utc']:
 profile['$defs']['run_data']['properties'][key]={'type':'null'}
 changes.append('/$defs/run_data/properties/'+key)
for key in base['$defs']:
 if key not in ('run_data','record'):assert base['$defs'][key]==profile['$defs'][key]
write('source-export.schema.proposed.json',profile)
old=json.dumps(base,indent=2).splitlines(keepends=True);new=json.dumps(profile,indent=2).splitlines(keepends=True)
with (R/'profile-proposal.patch').open('x',encoding='utf-8',newline='\n') as f:f.write(''.join(difflib.unified_diff(old,new,fromfile='frozen source.schema.json (unchanged)',tofile='proposed src/wgc/export/source-export.schema.json')))
write('contract-decision.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'task':'IG-1D','dependency_IG_1C':'done','frozen_source_schema_sha256':sha(base_path),'source_contract_started_utc':'Required non-null string; README specifies UTC timestamps. Record hashes include every field other than revision_id/content_hash.','operator_IG_1D_requirement':'Repeated identical inputs yield identical canonical export; operational timestamps stay outside canonical hashes; unavailable values are null.','conflict':'A complete source-v1 bundle requires a stored run and non-null started_utc, so omitting/unmeasured timestamps violates the pinned shape; inserting current time into canonical records violates the operator timestamp requirement. A fabricated fixed date or unknown string is not actual UTC evidence.','proposed_resolution':'Add explicitly versioned wgc-source-export-1 profile within assigned src/wgc/export scope; require canonical run.started_utc/ended_utc null and keep real session/config/time/usage evidence in operational sidecar. Reuse frozen validator with explicit profile path and every existing hash/reference/mechanical/review invariant. Original frozen contracts/code/reports unchanged.','profile_change_paths':changes,'unchanged_definitions':[k for k in base['$defs'] if k not in ('run_data','record')],'original_contract_modified':False,'product_implementation_started':False,'alternative':'Operator explicitly permits immutable pinned provenance timestamps inside canonical source-v1 hashes and defines their exact provenance input; this changes the current timestamp exclusion requirement.','smallest_operator_action':'Select/authorize the concrete proposed export profile or the provenance-timestamp alternative before IG-1D readiness.'})
print('Timestamp contract conflict and exact profile proposal preserved; frozen source schema unchanged.')
