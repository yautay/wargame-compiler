"""Recheck every frozen artifact and input after independent review validation."""
import hashlib
import json
from pathlib import Path
R=Path(__file__).parent
A=Path('private/workflow/runs/IG-2B07/inventory-25-28-01')
delivery=json.loads((A/'delivery.json').read_text())
meta={k:v for k,v in json.loads((R/'checkpoint.json').read_text()).items() if k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256')}
results=[]
for item in delivery['artifacts']+delivery['input_pins']:
    path=Path(item['path'])
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    results.append(dict(item,actual_sha256=actual,passed=actual==item['sha256'] and path.stat().st_size==item['bytes']))
assert all(x['passed'] for x in results)
assert hashlib.sha256((A/'delivery.json').read_bytes()).hexdigest()=='cee94ecd856edb0da9439881a0e002f7515f45f334a1b4e02fcd16b3f20cab27'
assert hashlib.sha256(Path(meta['configuration_evidence']).read_bytes()).hexdigest()==meta['configuration_sha256']
report=dict(meta,all_passed=True,artifact_count=len(delivery['artifacts']),input_count=len(delivery['input_pins']),results=results)
path=R/'frozen-reverification.json'
with path.open('x',encoding='utf-8') as f: json.dump(report,f,indent=2);f.write('\n')
print('All 2956 frozen artifacts and 10 input pins remain unchanged; delivery and runtime pins also match.')
