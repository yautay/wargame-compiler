import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

base=Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76')
def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p)
    return dict(path=p.as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
scope=load(base/'scope.json')
meta={k:scope[k] for k in ['role','actor','task','model','reasoning','configuration_evidence','configuration_sha256']}
assert pin(meta['configuration_evidence'])['sha256']==meta['configuration_sha256']
reports=[load(base/(name+'.json')) for name in ['refinement-preflight','sources-tests-approved','workflow-before-ready','accepted-root-validation']]
assert all(r['exit_code']==0 for r in reports)
tools=load(base/'toolchain.json')
for item in [tools['python_executable']]+[v['executable'] for v in tools['native'].values()]:
    assert pin(item['path'])['sha256']==item['sha256']
files=['prepare.py','run-check.py','refinement-check.py','record-ready.py','scope.json','input-pins.json','dependency-verification.json','toolchain.json','source-inspection.json','checkpoint.json','refinement-preflight.json','sources-tests.json','sources-tests-approved.json','workflow-before-ready.json','accepted-root-validation.json']
files += ['page-'+str(n).zfill(2)+'.png' for n in [9,10,11,12]]
report=dict(**meta,format='wgc-ready-evidence-1',recorded_utc=datetime.now(timezone.utc).isoformat(),summary='IG-2B03 refinement complete: accepted exact inputs, bounded physical pages 9-12, immutable prior scope, available context and disjoint absent executor outputs. Ready for a fresh executor; no inventory deliverable or semantic acceptance claimed.',criteria=['All direct dependencies are done and exact current accepted event/output hashes verified.','All original acceptance criteria and required tests preserved verbatim; detailed source/evidence/preservation/review requirements appended.','All exact context available below 100 KB; physical pages 9-12 visually inspected for contract scope; target/context IDs separate.','Executor output root absent; no other existing task changed.'],artifacts=[pin(base/name) for name in files],checks=[dict(command=r['command'],exit_code=r['exit_code'],report=pin(base/(name+'.json'))) for name,r in zip(['refinement-preflight','sources-tests-approved','workflow-before-ready','accepted-root-validation'],reports)],readiness=dict(dependencies_done=True,refinement_complete=True,context_available=True,target_physical_pages=[9,10,11,12],executor_output_root=scope['output_root'],executor_output_absent=not Path(scope['output_root']).exists()),permission_failure=dict(failed_report=pin(base/'sources-tests.json'),resolution_report=pin(base/'sources-tests-approved.json'),explanation='Windows restricted-token mode0700 basetemp failure; approved exact unchanged pytest validation passed. No ACL, test, library or assertion change.'),semantic_acceptance_granted=False,product_acceptance_granted=False,executable_readiness='unverified',next_action='Transition selected planned task to ready, render derived views, run required repository check and freeze final coordinator readiness evidence. Only supervisor launches next executor.')
with (base/'ready.json').open('x',encoding='utf-8') as stream:
    json.dump(report,stream,indent=2)
    stream.write('\n')
print((base/'ready.json').as_posix())
