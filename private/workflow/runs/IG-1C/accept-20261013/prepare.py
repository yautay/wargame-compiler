"""Coordinator records exact independent technical PASS; no semantic decision."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path.cwd();R=Path(__file__).parent
REVIEW=Path('private/workflow/runs/IG-1C/rereview-20261013T100001Z/review.json')
DELIVERY=Path('private/workflow/runs/IG-1C/repair-01-20261013/delivery.json')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def art(p):return {'path':p.as_posix(),'sha256':sha(p)}
def write(n,d):
 with (R/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
review=read(REVIEW);delivery=read(DELIVERY);q=read('docs/work/queue.json')
t=next(t for t in q['tasks'] if t['id']=='IG-1C')
assert t['status']=='review' and not t['semantic_acceptance_required']
assert sha(REVIEW)=='c1ee79e0cdf23fe31e1fc7831aa23f4042d00ce6e1cbce938aecdb9eb61d0144'
assert sha(DELIVERY)=='5392446d5e9d2112b048d4b74030b6a8790fd1848d2de1df4812590decedd7ad'
assert review['technical_result']=='pass' and review['technical_pass'] and review['independent_pass']
assert review['actor']!=delivery['actor']
assert review['model']=='gpt-6.1-sol' and review['reasoning']=='high'
assert review['criteria']==t['acceptance']==delivery['criteria']
assert [a['criterion'] for a in review['criterion_assessments']]==t['acceptance']
assert all(a['status']=='pass' for a in review['criterion_assessments'])
assert review['findings']==[]
assert all(f['disposition']=='closed' and f['required_verification_complete'] and f['repair_iteration']==1 for f in review['finding_dispositions'])
assert review['reviewed_delivery']['artifacts']==delivery['artifacts']
assert review['reviewed_delivery']['sha256']==sha(DELIVERY)
for a in review['artifacts']+delivery['artifacts']:assert sha(a['path'])==a['sha256'],a['path']
assert all(c['exit_code']==0 for c in review['checks'])
assert review['semantic_acceptance_granted'] is False and review['executable_readiness_granted'] is False
checks=review['checks']
write('gate-audit.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'accepted_delivery':art(DELIVERY),'independent_pass':art(REVIEW),'exact_delivery_artifact_count':len(delivery['artifacts']),'review_evidence_artifact_count':len(review['artifacts']),'all_hashes_match':True,'criteria':review['criterion_assessments'],'finding_dispositions':review['finding_dispositions'],'independent_checks_all_pass':True,'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':review['configuration_evidence'],'semantic_acceptance_required':False,'semantic_acceptance_granted':False,'source_coverage_granted':False,'executable_readiness_granted':False,'next_operation':'Record accepted then done via workflow transitions; only afterward refine/readiness/claim IG-1D.'})
base={'task':'IG-1C','criteria':t['acceptance'],'artifacts':delivery['artifacts'],'checks':checks,'model':review['model'],'reasoning':review['reasoning'],'configuration_evidence':review['configuration_evidence'],'independent_review':art(REVIEW),'accepted_exact_delivery':art(DELIVERY),'coordinator_gate_audit':art(R/'gate-audit.json'),'semantic_acceptance_granted':False,'executable_readiness_granted':False,'source_coverage_granted':False}
write('acceptance.json',{**base,'role':'reviewer','actor':review['actor'],'recorded_by':'ig1-stage-executor-20261013 (coordinator)','summary':'Coordinator records the exact independent technical PASS by the separately identified reviewer; every criterion, 34 delivery hashes, 41 reviewer evidence hashes and closed R01/R02/R03 verified. Role/actor attributes identify the independent technical basis; this record was written by the coordinator, not a new reviewer or human semantic approver.'})
write('completion.json',{**base,'role':'coordinator','actor':'ig1-stage-executor-20261013','summary':'Complete IG-1C lasting technical delivery after verified independent PASS and first-cycle finding closure; no human semantic acceptance or gameplay readiness conferred; IG-1D readiness is the next separate dependency-gated operation.'})
print('Acceptance/completion evidence prepared for exact 34-artifact delivery')
