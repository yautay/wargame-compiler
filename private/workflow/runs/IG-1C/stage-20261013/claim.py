import hashlib, json
from pathlib import Path
from datetime import datetime, timezone
R=Path('private/workflow/runs/IG-1C/stage-20261013')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,d):
 with (R/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
wheel=R/'dependencies/pyyaml-6.0.3-cp312-cp312-win_amd64.whl'
metadata=json.loads((R/'dependencies/pypi-6.0.3.json').read_text())
entry=next(e for e in metadata['urls'] if e['filename']==wheel.name)
assert sha(wheel)==entry['digests']['sha256']
import yaml
assert yaml.__version__=='6.0.3'
try:yaml.safe_load('!!python/object/apply:os.system [echo unsafe]')
except yaml.constructor.ConstructorError:pass
else:raise AssertionError('unsafe tag loaded')
write('dependency.json',{'name':'PyYAML','version':yaml.__version__,'official_metadata':'https://pypi.org/pypi/PyYAML/6.0.3/json','wheel_url':entry['url'],'wheel_sha256':sha(wheel),'metadata_sha256':sha(R/'dependencies/pypi-6.0.3.json'),'runtime_path':yaml.__file__,'safe_tag_rejected':True,'duplicate_key_policy':'Project SafeLoader subclass must enforce duplicate-key rejection; vanilla safe_load does not. Validate in product tests.','pip_bootstrap':'Bundled ensurepip 25.0.1 installed project-locally; TEMP moved to private/workflow/checks/dep1 after sandbox temp access denial.','network':'Sandbox DNS denied; explicitly authorized dependency-only escalation succeeded; no external service calls besides official registry.'})
P=Path('private/workflow/packets/IG-1C-998356d0bdea45f4b63552d4e26b5515')
m=json.loads((P/'manifest.json').read_text())
for a in m['files']:assert sha(a['path'])==a['sha256']
assert sha(P/'context.txt')==m['context_sha256']
q=json.loads(Path('docs/work/queue.json').read_text());t=next(t for t in q['tasks'] if t['id']=='IG-1C');assert t['status']=='ready'
write('checkpoint.json',{'task':'IG-1C','actor':'ig1-stage-executor-20261013','model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct current-session operator UI confirmation: sol 6.1 high','started_utc':datetime.now(timezone.utc).isoformat(),'input_packet':{'path':str(P/'manifest.json'),'sha256':sha(P/'manifest.json')},'owned_product_paths':t['write_scope'],'base_files':[],'completed_criteria':[],'next_operation':'Implement safe parser and lossless complete directory importer; run explicit adversarial and full private accounting tests','input_tokens':None,'output_tokens':None,'cost':None})
write('claim.json',{'role':'executor','actor':'ig1-stage-executor-20261013','summary':'Claim only ready IG-1C; complete frozen inputs/support hashes and packet verified; safe parser dependency wheel independently matches official registry hash.','criteria':t['start_conditions'],'artifacts':[{'path':str(R/n).replace('\\','/'),'sha256':sha(R/n)} for n in ['checkpoint.json','configuration.json','dependency.json']],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct operator current-session UI observation retained in configuration.json'})
print('IG-1C claim prepared; official wheel hash matches')
