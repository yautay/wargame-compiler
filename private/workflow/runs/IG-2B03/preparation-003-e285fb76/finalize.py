import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

base=Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76')
def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=Path(p)
    return dict(path=p.as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def save(name,data):
    with (base/name).open('x',encoding='utf-8') as stream:
        json.dump(data,stream,indent=2,ensure_ascii=False)
        stream.write('\n')
    return pin(base/name)

assert subprocess.run([sys.executable,'-B',str(base/'refinement-check.py')],check=True).returncode==0
scope=load(base/'scope.json')
meta={k:scope[k] for k in ['role','actor','task','model','reasoning','configuration_evidence','configuration_sha256']}
q=load('docs/work/queue.json')
task=next(t for t in q['tasks'] if t['id']=='IG-2B03')
assert task['status']=='ready' and task['events'][-1]['evidence']==(base/'ready.json').as_posix()
assert pin(base/'ready.json')['sha256']==task['events'][-1]['sha256']
ready=load(base/'ready.json')
for artifact in ready['artifacts']:
    assert pin(artifact['path'])['sha256']==artifact['sha256']
dep=load(base/'dependency-verification.json')
delivery=load(dep['delivery']['path'])
for artifact in delivery['artifacts']:
    assert pin(artifact['path'])['sha256']==artifact['sha256'],artifact['path']
check_names=['refinement-preflight','workflow-before-ready','accepted-root-validation','sources-tests-approved','repository-check','packet-build','final-refinement','diff-check']
checks=[]
artifacts=[]
for name in check_names:
    p=base/(name+'.json')
    report=load(p)
    assert report['exit_code']==0
    assert report['configuration_evidence']==meta['configuration_evidence'] and report['configuration_sha256']==meta['configuration_sha256']
    for artifact in report['artifacts']:
        assert pin(artifact['path'])['sha256']==artifact['sha256']
        artifacts.append(artifact)
    artifacts.append(pin(p))
    checks.append(dict(command=report['command'],exit_code=0,report=pin(p)))
packet_dir=Path((base/'packet-build.stdout').read_text(encoding='utf-8').strip())
packet=load(packet_dir/'manifest.json')
assert packet['queue_sha256']==pin('docs/work/queue.json')['sha256']
assert packet['task']=='IG-2B03' and packet['text_bytes']<100_000
for item in packet['files']:
    assert pin(item['path'])['sha256']==item['sha256'],item['path']
artifacts.append(pin(packet_dir/'manifest.json'))
log=(base/'repository-check.stdout').read_text(encoding='utf-8')
log_root=Path(log.splitlines()[0].removeprefix('LOG_ROOT='))
result=load(log_root/'result.json')
assert all(result[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
for name in ['result.json','plan.log','dry-run.log','pytest.log','diff-check.log']:
    artifacts.append(pin((log_root/name).relative_to(Path.cwd())))
artifacts += [pin(base/name) for name in ['ready.json','scope.json','input-pins.json','dependency-verification.json','toolchain.json','source-inspection.json','checkpoint.json','prepare.py','run-check.py','refinement-check.py','record-ready.py','finalize.py','sources-tests.json','sources-tests.stdout','sources-tests.stderr','queue-before.json','context-policy-before.json']]
artifacts += [pin(base/f'page-{n:02d}.png') for n in [9,10,11,12]]
snapshot=save('selected-task-after.json',task)
artifacts.append(snapshot)
ended=datetime.now(timezone.utc)
runtime=load(meta['configuration_evidence'])
started=datetime.fromisoformat(runtime['observed_utc'])
report=dict(**meta,format='wgc-coordinator-readiness-1',outcome='progress',summary='IG-2B03 refined and ready for one fresh executor. Exact accepted IG-2B02 inputs, assigned pages 9-12, preservation, disjoint output scope, independent review and unchanged validation requirements are pinned. No product authoring or acceptance performed.',criteria=ready['criteria'],artifacts=artifacts,checks=checks,readiness=dict(status='ready',event=task['events'][-1],dependencies_done=True,refinement_complete=True,context_available=True,context_files=len(packet['files']),context_bytes=packet['text_bytes'],packet_manifest=pin(packet_dir/'manifest.json'),source_physical_pages=[9,10,11,12],target_ids=task['target_ids'],context_only_ids=task['context_only_ids'],executor_output_root=scope['output_root'],executor_output_absent=not Path(scope['output_root']).exists()),preservation=dict(other_existing_tasks_unchanged=True,original_acceptance_and_tests_preserved_verbatim=True,accepted_dependency_artifacts_reverified=len(delivery['artifacts']),historical_and_product_artifacts_modified=False),validation=dict(source_suite='71 passed',repository_suite='151 passed',repository_subchecks=result,restricted_token_failure=pin(base/'sources-tests.json'),approved_unchanged_source_validation=pin(base/'sources-tests-approved.json'),approved_repository_validation=pin(base/'repository-check.json'),diff_check_exit=0),remaining_gates=['Fresh executor claim with its own confirmed runtime configuration and exclusive ownership.','Task product implementation, complete independent source/technical review and coordinator acceptance are still required.','Human semantic acceptance and executable readiness remain separate downstream gates.'],semantic_acceptance_granted=False,product_acceptance_granted=False,executable_readiness='unverified',queue_sha256_at_freeze=pin('docs/work/queue.json')['sha256'],context_policy_sha256_at_freeze=pin('docs/work/context-policy.json')['sha256'],measurement=dict(started_utc=started.isoformat(),ended_utc=ended.isoformat(),wall_seconds=(ended-started).total_seconds(),input_tokens=None,output_tokens=None,operator_seconds=None,monetary_cost=None,unknown_reason='Not exposed or reported.'),next_action='Supervisor may launch the selected ready IG-2B03 executor. Coordinator stops after this one role.',immutability='New append-only readiness report; all listed preparation and validation files are frozen and must not be overwritten. Queue and policy hashes describe the freeze point, not immutable future paths.')
target=save('readiness.json',report)
for artifact in report['artifacts']:
    assert pin(artifact['path'])['sha256']==artifact['sha256']
print(json.dumps(dict(evidence=target,task_status='ready',checks='all passed',executor_products_written=False)))
