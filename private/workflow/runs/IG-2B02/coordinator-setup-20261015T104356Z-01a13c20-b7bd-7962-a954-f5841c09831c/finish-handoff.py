"""Record one authorized changes_requested transition, issue actual packet, seal handoff."""
import copy, hashlib, importlib.util, json, os, re, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

R=Path('C:/repo/wargame-compiler'); C=Path(__file__).resolve().parent
P=R/'private/workflow/runs/IG-2B02/repair-preparation-20261015T091559Z-01a13c20-b7bd-7962-a954-f5841c09831c'
PY=str(R/'.venv/Scripts/python.exe')
env=os.environ.copy(); env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'src')+';C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages',PATH='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;'+env['PATH'])
def now(): return datetime.now(timezone.utc).isoformat()
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def pin(path):
    raw=path.read_bytes(); return dict(path=path.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(name,value):
    with (C/name).open('x',encoding='utf-8',newline='\n') as stream: json.dump(value,stream,indent=2,ensure_ascii=False); stream.write('\n')
def run(label,args,allow_failure=False):
    start=now(); clock=time.monotonic(); result=subprocess.run(args,cwd=R,env=env,capture_output=True)
    for suffix,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        with (C/(label+'.'+suffix)).open('xb') as stream: stream.write(data)
    record=dict(command=args,exit_code=result.returncode,started_utc=start,ended_utc=now(),wall_seconds=time.monotonic()-clock,stdout=pin(C/(label+'.stdout')),stderr=pin(C/(label+'.stderr')))
    write(label+'.command.json',record); print(label,result.returncode,flush=True)
    if result.returncode and not allow_failure: raise SystemExit(result.returncode)
    return record

started=now(); clock=time.monotonic(); state=read(P/'preparation.json'); config=read(C/'configuration.json')
checks=read(C/'scope-checks.json'); assert all(row['exit_code']==0 for row in checks['checks'])
q=read(R/'docs/work/queue.json'); scoped=read(C/'queue-scoped-review.json'); assert q==scoped
assert pin(R/'docs/work/queue.json')['sha256']==pin(C/'queue-scoped-review.json')['sha256']
task=next(t for t in q['tasks'] if t['id']=='IG-2B02'); assert task['status']=='review' and len(task['events'])==3
assert not (R/state['reserved_absent_repair_attempt']).exists()
spec=importlib.util.spec_from_file_location('workflow',R/'scripts/workflow.py'); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
w.validate(q,R)

# Verify all frozen native/bundle/executable/library metadata pins without making them
# inadmissible direct workflow artifacts. Old logs remain original attribution.
toolchain=read(R/state['original_delivery_directory']/'toolchain.json'); tool_rows=[]
def visit(value):
    if isinstance(value,dict):
        if all(k in value for k in ('path','bytes','sha256')):
            path=Path(value['path']); path=path if path.is_absolute() else R/path
            raw=path.read_bytes(); assert len(raw)==value['bytes'] and hashlib.sha256(raw).hexdigest()==value['sha256'],value['path']
            tool_rows.append(value)
        for nested in value.values(): visit(nested)
    elif isinstance(value,list):
        for nested in value: visit(nested)
visit(toolchain)
write('tool-source-pin-verification.json',dict(outcome='passed_exact_pins',observed_utc=now(),toolchain_input=pin(R/state['original_delivery_directory']/'toolchain.json'),toolchain_nested_pins_verified=tool_rows,source_and_contract_pins=[row for row in read(P/'launch-gate-pins.json')['pins'] if row['path'].startswith(('src/','contracts/','scripts/','private/ig/sources/'))],meaning_review_performed=False,note='Pin checks only. Original version observations remain attributed to their original actor; repair executor must independently confirm own runtime.'))
for row in read(C/'tool-source-pin-verification.json')['source_and_contract_pins']: assert pin(R/row['path'])==row
repository_stdout=(C/'scope-repository-check.stdout').read_text(encoding='utf-8'); log_root=Path(re.search(r'LOG_ROOT=(.+)',repository_stdout)[1].strip()); log_root.resolve().relative_to((R/'private/workflow/checks').resolve())
result=read(log_root/'result.json'); assert all(result[k]==0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
assert '102 passed' in (log_root/'pytest.log').read_text(encoding='utf-8-sig')
write('required-check-log-pins.json',dict(check_log_root=str(log_root),artifacts=[pin(log_root/name) for name in ('plan.log','dry-run.log','pytest.log','diff-check.log','result.json')],result=result,full_suite='102 passed',warnings_preserved=True))
run('pre-transition-frozen-bases',[PY,'-B',str(P/'verify-frozen-bases.py'),'--report',str(C/'pre-transition-frozen-bases.json')])
write('pre-transition-checkpoint.json',dict(role='coordinator',actor=config['actor'],recorded_utc=now(),task='IG-2B02',status='review',scope_applied=True,configuration=pin(C/'configuration.json'),operator_authorization=pin(C/'authorization.json'),queue_snapshot=pin(C/'queue-scoped-review.json'),frozen_refs_verified=4246,repair_directory_absent=True,checks_passed=True,next_operation='One review -> changes_requested transition using immutable coordinator-decision.json; inspect persisted state after any exit. No retry without diagnosis.',acceptance_granted=False))
decision_artifacts=[pin(path) for path in C.rglob('*') if path.is_file()]
decision_artifacts += [pin(P/name) for name in ('coordinator-setup.txt','repair-launch.txt','repair-scope.json','coordinator-queue-patch-v2.json','preparation-seal.json','frozen-base-pins.json')]
decision_artifacts += [state[key] for key in ('original_delivery','original_delivery_manifest','original_delivery_seal','review','review_manifest','review_seal','findings')]
decision_artifacts += read(C/'required-check-log-pins.json')['artifacts']
decision_artifacts += [pin(R/'docs/work/repair-context/IG-2B02-R01-R02-20261015T091559Z.json')]
seen=set(); decision_artifacts=[a for a in decision_artifacts if not (a['path'] in seen or seen.add(a['path']))]
for row in decision_artifacts:
    path=w.safe_path(R,row['path']); assert not w.denied(row['path']) and path.is_file() and pin(path)==row
decision=dict(role='coordinator',actor=config['actor'],summary='Request bounded metadata repair for independent P2 findings IG-2B02-R01 and IG-2B02-R02 in three exact page-5 counters. Adopt the independent review for changes_requested only; no acceptance, dismissal or semantic decision. Apply only prepared v2 task scope fields; original delivery and review stay immutable.',task='IG-2B02',model=config['model'],reasoning=config['reasoning'],configuration_evidence=(C/'configuration.json').relative_to(R).as_posix(),criteria=task['acceptance'],artifacts=decision_artifacts,checks=checks['checks'],recorded_utc=now(),authorization=(C/'authorization.json').relative_to(R).as_posix(),finding_ids=['IG-2B02-R01','IG-2B02-R02'],affected_regions=3,repair_directory=state['reserved_absent_repair_attempt'],acceptance_granted=False,measurement=dict(started_utc=checks['started_utc'],ended_utc=now(),wall_seconds=None,unknown_reason='Per-command wall times recorded; aggregate operator, token and monetary measures unavailable.',operator_seconds=None,input_tokens=None,output_tokens=None,cost=None))
write('coordinator-decision.json',decision)
# This is a read-only path/hash/criteria preflight. Never call transition on a clone:
# even clone preflight would create an unobserved timestamp rather than inspect bytes.
assert decision['role']=='coordinator' and decision['criteria']==task['acceptance']
assert all(row['exit_code']==0 for row in decision['checks'])
assert pin(R/'docs/work/queue.json')['sha256']==pin(C/'queue-scoped-review.json')['sha256']
record=run('changes-requested-transition',[PY,'-B','scripts/workflow.py','transition','--task','IG-2B02','--to','changes_requested','--evidence',(C/'coordinator-decision.json').relative_to(R).as_posix()],allow_failure=True)
actual=read(R/'docs/work/queue.json'); current=next(t for t in actual['tasks'] if t['id']=='IG-2B02'); event=current['events'][-1]
persisted=(current['status']=='changes_requested' and len(current['events'])==4 and event['from']=='review' and event['to']=='changes_requested' and event['evidence']==(C/'coordinator-decision.json').relative_to(R).as_posix() and event['sha256']==pin(C/'coordinator-decision.json')['sha256'])
write('transition-inspection.json',dict(exit_code=record['exit_code'],persisted_exact_expected_event=persisted,observed_status=current['status'],event_count=len(current['events']),latest_event=event,observed_queue_pin=pin(R/'docs/work/queue.json'),automatic_retry=False))
assert persisted,'Transition did not persist expected event: stop; no retry.'
assert record['exit_code']==0,'Event persisted but command failed: diagnose projection-only recovery; no retry.'
expected=copy.deepcopy(q); expected_task=next(t for t in expected['tasks'] if t['id']=='IG-2B02'); expected_task['status']='changes_requested'; expected_task['events'].append(event); assert actual==expected
with (C/'queue-changes-requested.json').open('xb') as stream: stream.write((R/'docs/work/queue.json').read_bytes())
post=[]
post.append(run('post-transition-workflow-validate',[PY,'-B','scripts/workflow.py','validate']))
post.append(run('post-transition-dry-run',[PY,'-B','scripts/workflow.py','dry-run','--task','IG-2B02']))
post.append(run('post-transition-diff-check',['git','diff','--check']))
run('repair-packet',[PY,'-B','scripts/workflow.py','packet','--task','IG-2B02'])
packet_rel=(C/'repair-packet.stdout').read_text(encoding='utf-8').strip(); packet_dir=w.safe_path(R,packet_rel); manifest=read(packet_dir/'manifest.json')
assert manifest['queue_sha256']==pin(R/'docs/work/queue.json')['sha256']
sections=[]
for row in manifest['files']:
    assert w.permitted(R,row['path']) and pin(R/row['path'])==row
    path=R/row['path']
    if path.suffix.lower() in {'.md','.json','.py','.ps1','.toml'}: sections.append('\n--- FILE: '+row['path']+' ---\n'+path.read_text(encoding='utf-8-sig'))
payload='\n'.join(sections); logical=len(payload.encode('utf-8'))
assert payload==(packet_dir/'context.txt').read_text(encoding='utf-8') and logical==manifest['text_bytes'] and logical<100000
assert manifest['context_sha256']==pin(packet_dir/'context.txt')['sha256']
assert read(R/'docs/work/queue.json')==actual
run('post-setup-frozen-bases',[PY,'-B',str(P/'verify-frozen-bases.py'),'--report',str(C/'post-setup-frozen-bases.json')])
assert not (R/state['reserved_absent_repair_attempt']).exists()
handoff=dict(task='IG-2B02',role='coordinator',actor=config['actor'],issued_utc=now(),status='changes_requested',operator_authorization=pin(C/'authorization.json'),configuration=pin(C/'configuration.json'),coordinator_decision=pin(C/'coordinator-decision.json'),review_to_changes_requested_event=event,current_queue=pin(R/'docs/work/queue.json'),immutable_queue_snapshot=pin(C/'queue-changes-requested.json'),scope=pin(P/'repair-scope.json'),selected_patch=pin(P/'coordinator-queue-patch-v2.json'),metadata_context_index=pin(R/'docs/work/repair-context/IG-2B02-R01-R02-20261015T091559Z.json'),repair_instruction=pin(P/'repair-launch.txt'),packet=dict(directory=packet_rel,manifest=pin(packet_dir/'manifest.json'),context=pin(packet_dir/'context.txt'),logical_utf8_bytes=logical,physical_context_bytes=(packet_dir/'context.txt').stat().st_size,limit=100000,complete_exact_reconstruction=True),allowed_write_scope=current['write_scope'],reserved_repair_attempt=state['reserved_absent_repair_attempt'],reserved_attempt_absent=True,ownership_policy='Only the NEW actual-config-confirmed executor may create reserved repair directory and claim changes_requested -> in_progress. Existing directory or writer drift requires checkpoint/escalation, never overwrite.',frozen_base_catalogue=pin(P/'frozen-base-pins.json'),frozen_verification_before=pin(C/'pre-setup-frozen-bases.json'),frozen_verification_after=pin(C/'post-setup-frozen-bases.json'),tool_source_pin_verification=pin(C/'tool-source-pin-verification.json'),setup_checks=pin(C/'scope-checks.json'),post_transition_checks=post,criteria_unchanged=current['acceptance'],original_events_preserved=True,other_tasks_and_queue_fields_unchanged=True,prepared_instructions_unchanged=True,executor_configuration=None,executor_configuration_reason='Future new session not created yet; its creation flags do not prove actual model/reasoning. It must confirm own runtime identity and gpt-6.1-sol/high before claim.',acceptance_granted=False,no_downstream_work=True,next_operation='Create exactly one operator-requested new local repair session on gpt-6.1-sol/high, supply full prepared repair-launch.txt plus this actual handoff. Executor repairs bounded findings, returns review with fresh rereview handoff, and stops without launching reviewer or granting acceptance.')
write('coordinator-handoff.json',handoff)
prompt='''The human operator has now explicitly authorized the coordinator setup and creation of this one NEW LOCAL repair session for IG-2B02-R01/R02, requested gpt-6.1-sol with reasoning high. Execute the prepared bounded repair instruction below after confirming YOUR OWN actual session model/reasoning and identity. Communicate in Polish; write repository/reports in English. This authorizes only this repair, its checks and return to review; no acceptance, reviewer-session creation or downstream task.

Coordinator setup is completed, not pending: review -> changes_requested is recorded. Do not execute the coordinator plan or alter queue structure. The historical prepared instruction/patch use preparation-time labels; verify their unchanged original pins, then reconcile ONLY the exact authorized coordinator field/event changes and actual new packet using this immutable handoff and saved before/after snapshots. Do not require the old review-state queue hash to remain current. The fresh packet below is the actual repair claim input; the old preparation packet remains evidence only.

Repository: C:/repo/wargame-compiler
'''
prompt+='Actual coordinator handoff: '+str(C/'coordinator-handoff.json')+'\nSHA256 '+pin(C/'coordinator-handoff.json')['sha256']+'; bytes '+str(pin(C/'coordinator-handoff.json')['bytes'])+'\n'
prompt+='Actual repair packet: '+str(packet_dir)+'\nManifest SHA256 '+pin(packet_dir/'manifest.json')['sha256']+'\nContext SHA256 '+pin(packet_dir/'context.txt')['sha256']+'\n'
prompt+='Prepared repair-launch.txt: '+str(P/'repair-launch.txt')+'\nSHA256 '+pin(P/'repair-launch.txt')['sha256']+'; bytes '+str(pin(P/'repair-launch.txt')['bytes'])+'\n\nThe complete immutable prepared instruction follows verbatim:\n\n'+(P/'repair-launch.txt').read_text(encoding='utf-8')
with (C/'new-repair-session-prompt.txt').open('x',encoding='utf-8',newline='\n') as stream: stream.write(prompt)
write('setup-manifest.json',dict(task='IG-2B02',role='coordinator',frozen_utc=now(),artifacts=[pin(path) for path in sorted(C.rglob('*')) if path.is_file()],external_artifacts=[pin(packet_dir/'manifest.json'),pin(packet_dir/'context.txt')]+read(C/'required-check-log-pins.json')['artifacts'],self_exclusion='This manifest excludes itself and later coordinator-seal.json. New session creation receipt is post-seal operational evidence, separately pinned and does not rewrite setup artifacts.',acceptance_granted=False))
write('coordinator-seal.json',dict(task='IG-2B02',role='coordinator',actor=config['actor'],sealed_utc=now(),status_at_handoff='changes_requested',setup_manifest=pin(C/'setup-manifest.json'),handoff=pin(C/'coordinator-handoff.json'),session_prompt=pin(C/'new-repair-session-prompt.txt'),coordinator_decision=pin(C/'coordinator-decision.json'),packet_manifest=pin(packet_dir/'manifest.json'),packet_context=pin(packet_dir/'context.txt'),frozen_refs_preserved=4246,full_suite='102 passed',workflow_validate_exit=0,dry_run_exit=0,diff_check_exit=0,started_utc=started,wall_seconds=time.monotonic()-clock,acceptance_granted=False,session_not_yet_created=True,token_usage=None,cost=None,operator_time=None,unknown_measurement_reason='Unavailable; not invented.',self_exclusion='Seal excludes itself; actual hash returned separately. Later session launch receipt is separate post-seal operational evidence.'))
print(json.dumps(dict(handoff=pin(C/'coordinator-handoff.json'),seal=pin(C/'coordinator-seal.json'),prompt=pin(C/'new-repair-session-prompt.txt'),packet=handoff['packet'],status='changes_requested',full_suite='102 passed'),indent=2),flush=True)
