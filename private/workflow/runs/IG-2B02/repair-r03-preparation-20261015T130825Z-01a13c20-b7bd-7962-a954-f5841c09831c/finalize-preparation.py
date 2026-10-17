"""Audit and seal the R03 instruction package only; no queue/session/repair action."""
import copy,hashlib,importlib.util,json,re,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
R=Path('C:/repo/wargame-compiler');P=Path(__file__).resolve().parent
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def pin(path):return dict(path=path.relative_to(R).as_posix(),bytes=path.stat().st_size,sha256=sha(path))
def write(name,value):
    with (P/name).open('x',encoding='utf-8',newline='\n') as stream:json.dump(value,stream,indent=2,ensure_ascii=False);stream.write('\n')
started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();assert not (P/'preparation-seal.json').exists()
state=read(P/'preparation.json');assert pin(R/'docs/work/queue.json')==state['queue_snapshot'];assert not (R/state['reserved_absent_repair_attempt']).exists()
checks=read(P/'checks.json');assert all(row['exit_code']==0 for row in checks['checks'])
index=read(P/'instruction-index.json')
index['documents']=[pin(P/name) for name in ['repair-launch.txt','coordinator-setup.txt','independent-rereview-template.txt']]
# Refresh only the still-unsealed, preparer-owned document index after QA clarified
# that a future reviewer must direct helper output into its OWN run, never frozen A.
index['preseal_qa_note']='Clarified role-specific helper output ownership in all three documents before seal. No frozen input or scope changed.'
with (P/'instruction-index.json').open('w',encoding='utf-8',newline='\n') as stream:json.dump(index,stream,indent=2,ensure_ascii=False);stream.write('\n')
seen={}
def visit(value):
    if isinstance(value,dict):
        if all(k in value for k in ('path','bytes','sha256')) and isinstance(value['sha256'],str):
            row=(value['bytes'],value['sha256']);assert seen.setdefault(value['path'],row)==row,value['path']
        for nested in value.values():visit(nested)
    elif isinstance(value,list):
        for nested in value:visit(nested)
for name in ['instruction-index.json','launch-gate-pins.json','repair-scope.json','binding-expectations.json','coordinator-queue-patch.json','preparation.json']:visit(read(P/name))
for path,(size,digest) in seen.items():
    target=Path(path);target=target if target.is_absolute() else R/target
    assert target.is_file() and target.stat().st_size==size and sha(target)==digest,path
tables=0
for name in ['repair-launch.txt','coordinator-setup.txt','independent-rereview-template.txt']:
    raw=(P/name).read_bytes();assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw
    text=raw.decode('utf-8');assert 'A coordinator or reviewer must use its own new run report path' in text
    for line in text.splitlines():
        match=re.fullmatch(r'([^|]+) \| ([0-9]+) \| ([0-9a-f]{64})',line)
        if match:
            row=pin(R/match[1]);assert row['bytes']==int(match[2]) and row['sha256']==match[3];tables+=1
for path in P.glob('*.py'):compile(path.read_text(encoding='utf-8'),str(path),'exec')
q=read(R/'docs/work/queue.json');task=next(t for t in q['tasks'] if t['id']=='IG-2B02');assert task['status']=='review' and len(task['events'])==6
proposal=read(P/'coordinator-queue-patch.json');draft=copy.deepcopy(q);selected=next(t for t in draft['tasks'] if t['id']=='IG-2B02');selected.update(proposal['task_field_updates'])
assert all(selected[key]==task[key] for key in proposal['preserve_fields'])
assert [t for t in draft['tasks'] if t['id']!='IG-2B02']==[t for t in q['tasks'] if t['id']!='IG-2B02']
spec=importlib.util.spec_from_file_location('workflow',R/'scripts/workflow.py');w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w);w.validate(draft,R,check_views=False)
expect=read(P/'binding-expectations.json');assert len(expect['bindings'])==24 and sum(row['correction_required'] for row in expect['bindings'])==6
audit=dict(outcome='passed_preparation_package_audit_only',instruction_table_pins_verified=tables,nested_pin_objects_verified=len(seen),correct_scope_and_all_24_expectations=True,draft_queue_valid=True,queue_written=False,unchanged_criteria_and_other_task_fields=True,scripts_syntax_valid=True,instruction_utf8_no_bom_lf=True,current_status='review',event_count=6,repair_attempt_absent=True,session_created=False,repair_performed=False,acceptance_granted=False)
write('instruction-package-audit.json',audit)
report=(P/'frozen-base-verification-after.json').relative_to(R).as_posix()
result=subprocess.run([str(R/'.venv/Scripts/python.exe'),'-B',str(P/'verify-frozen-bases.py'),'--report',report],cwd=R,capture_output=True)
for suffix,data in [('stdout',result.stdout),('stderr',result.stderr)]:
    with (P/('frozen-postcheck.'+suffix)).open('xb') as stream:stream.write(data)
assert result.returncode==0
frozen=read(P/'frozen-base-verification-after.json');assert frozen['frozen_refs_verified']==5112 and frozen['queue_equals_preparation_snapshot']
output=(P/'repository-check.stdout').read_text(encoding='utf-8');log_root=Path(re.search(r'LOG_ROOT=(.+)',output)[1].strip());log_root.resolve().relative_to((R/'private/workflow/checks').resolve())
check_result=read(log_root/'result.json');assert all(check_result[k]==0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
assert '102 passed' in (log_root/'pytest.log').read_text(encoding='utf-8-sig')
assert pin(R/'docs/work/queue.json')==state['queue_snapshot'] and not (R/state['reserved_absent_repair_attempt']).exists()
files=sorted(path for path in P.iterdir() if path.is_file())+[R/state['context_index']['path']]+[log_root/name for name in ('plan.log','dry-run.log','pytest.log','diff-check.log','result.json')]
seal=dict(task='IG-2B02',finding='IG-2B02-R03',role='instruction_preparer',actor=state['actor'],sealed_utc=datetime.now(timezone.utc).isoformat(),started_utc=started,wall_seconds=time.monotonic()-clock,own_configuration=pin(P/'configuration.json'),instruction_index=pin(P/'instruction-index.json'),documents=index['documents'],selected_queue_patch=pin(P/'coordinator-queue-patch.json'),draft_packet_byte_estimates=read(P/'proposal-validation.json')['packet_logical_byte_estimates'],frozen_refs_verified_before_and_after=5112,source_metadata_reproduction='6 incorrect + 18 correct current bindings; no report edited',preparation_checks=dict(repository_check_exit=0,workflow_validate_exit=0,diff_check_exit=0,full_suite='102 passed',warnings='Retained in actual logs; no suppression.'),queue_snapshot=state['queue_snapshot'],queue_unchanged=True,status='review',event_count=6,reserved_repair_attempt_absent=True,artifacts=[pin(path) for path in files],self_exclusion_policy='This seal excludes itself; its real SHA256 is returned separately. Do not rewrite any sealed file. No repair/coordinator setup or session creation is performed.',repair_performed=False,session_created=False,queue_transition_performed=False,acceptance_granted=False,future_actual_packet_handoff_and_delivery=None,future_hash_reason='Unavailable until separately authorized real coordinator setup and repair; never fabricated.',input_tokens=None,output_tokens=None,cost=None,operator_time=None,unknown_measurement_reason='Exact usage/cost/operator measurements unavailable.',next_operation='Operator may separately authorize coordinator setup from prepared coordinator-setup.txt; then a new own-runtime-confirmed local executor uses repair-launch.txt plus actual coordinator handoff. Fresh independent review follows real new repair. No acceptance or downstream task.')
write('preparation-seal.json',seal)
print(json.dumps(dict(seal=pin(P/'preparation-seal.json'),documents=index['documents'],frozen_refs=5112,checks='102 passed; workflow validate and diff check exit 0',queue_unchanged=True,repair_attempt_absent=True),indent=2),flush=True)
