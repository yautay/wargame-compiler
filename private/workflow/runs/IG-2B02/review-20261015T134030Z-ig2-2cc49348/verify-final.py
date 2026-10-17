import json,hashlib,datetime
from pathlib import Path
R=Path.cwd(); O=R/'private/workflow/orchestrator/20261015T134030Z-67077de2/001-IG-2B02-reviewer-2cc49348'; B=R/'private/workflow/runs/IG-2B02/repair-r01-r02-20261015T091559Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c'; V=R/'private/workflow/runs/IG-2B02/review-20261015T134030Z-ig2-2cc49348'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def pins(o):
 if isinstance(o,dict):
  if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):yield o
  for x in o.values():yield from pins(x)
 elif isinstance(o,list):
  for x in o:yield from pins(x)
def verify(ps):
 rows=[]
 for p in ps:
  f=R/p['path']; row={'path':p['path'],'expected_sha256':p['sha256']}
  try:
   b=f.read_bytes();row.update(actual_sha256=hashlib.sha256(b).hexdigest(),actual_bytes=len(b));row['pass']=row['actual_sha256']==p['sha256'] and ('bytes' not in p or p['bytes']==len(b))
  except OSError as e:row.update(passed=False,error=str(e));row['pass']=False
  rows.append(row)
 return rows
packet=load(O/'packet.json'); refs=load(O/'references.json'); dr=load(O/'delivery-reference.json'); d=load(B/'delivery.json')
ps=list(pins(packet))+[dict(path=x['evidence'],sha256=x['sha256']) for x in refs.values() if 'evidence' in x]+[dict(path=x['evidence'],sha256=x['sha256']) for x in refs.get('dependencies',{}).values()]+[dict(path=dr['evidence'],sha256=dr['sha256'])]
for name in ['delivery.json','delivery-manifest.json','final-seal.json','rereview-input-pins.json','toolchain.json']:
 ps+=list(pins(load(B/name)))
unique={(p['path'],p['sha256'],p.get('bytes')):p for p in ps}; rows=verify(unique.values())
report={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unique_pins':len(rows),'failed':[r for r in rows if not r['pass']],'pins':rows,'ordered_delivery_artifacts':d['artifacts']}
(V/'frozen-verification-final.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pins':len(rows),'failures':report['failed'],'delivery_artifacts':len(d['artifacts'])},indent=2))
print('SCOPE KEYS',list(load(R/'private/workflow/runs/IG-2B02/repair-preparation-20261015T091559Z-01a13c20-b7bd-7962-a954-f5841c09831c/repair-scope.json')))
print('INVENTORY KEYS',list(load(B/'final-verified/inventory.json')))
