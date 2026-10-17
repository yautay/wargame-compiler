"""Apply the operator-authorized, exact IG-2B02 R01/R02 coordinator scope patch."""
import copy, hashlib, importlib.util, json, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

R = Path('C:/repo/wargame-compiler')
C = Path(__file__).resolve().parent
P = R/'private/workflow/runs/IG-2B02/repair-preparation-20261015T091559Z-01a13c20-b7bd-7962-a954-f5841c09831c'
PY = str(R/'.venv/Scripts/python.exe')
PS = 'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE'
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(R/'src')+';C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages', PATH='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;'+env['PATH'])

def now(): return datetime.now(timezone.utc).isoformat()
def pin(path):
    raw = path.read_bytes()
    return dict(path=path.relative_to(R).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def write(name, value):
    with (C/name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False); stream.write('\n')
def run(label, args):
    start=now(); clock=time.monotonic()
    result=subprocess.run(args,cwd=R,env=env,capture_output=True)
    for suffix,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        with (C/(label+'.'+suffix)).open('xb') as stream: stream.write(data)
    record=dict(command=args,exit_code=result.returncode,started_utc=start,ended_utc=now(),wall_seconds=time.monotonic()-clock,stdout=pin(C/(label+'.stdout')),stderr=pin(C/(label+'.stderr')))
    write(label+'.command.json',record)
    print(label,result.returncode,flush=True)
    if result.returncode: raise SystemExit(result.returncode)
    return record

start=now(); clock=time.monotonic()
seal=read(P/'preparation-seal.json')
assert pin(P/'preparation-seal.json')['sha256']=='3240750023211874afd1e74ec6204b56be967c4e569c23696e8cd7c104a69412'
for row in seal['artifacts']: assert pin(R/row['path'])==row,row['path']
state=read(P/'preparation.json'); patch=read(P/'coordinator-queue-patch-v2.json')
assert pin(R/'docs/work/queue.json')==patch['expected_queue']
assert not (R/state['reserved_absent_repair_attempt']).exists()
assert pin(P/'repair-launch.txt')['sha256']=='8903ed388eb549d23c988a2d5270c2758077bb4c5917b608ffa1daef49408f40'
assert pin(P/'coordinator-queue-patch-v2.json')['sha256']=='43878efbbf1431ea50f671dcb497ca33049c225b20ff554f081c9dd1814a2913'
spec=importlib.util.spec_from_file_location('workflow',R/'scripts/workflow.py'); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
q=read(R/'docs/work/queue.json'); t=next(t for t in q['tasks'] if t['id']=='IG-2B02')
assert t['status']==patch['expected_task_status'] and t['events'][-1]==patch['expected_event']
assert [x['id'] for x in read(R/state['independent_review_directory']/'findings.json')['findings']]==['IG-2B02-R01','IG-2B02-R02']
metadata=Path('C:/Users/yauta/.codex/sessions/2026/10/14/rollout-2026-10-14T22-35-39-01a13c20-b7bd-7962-a954-f5841c09831c.jsonl')
session=None; turn=None
with metadata.open('r',encoding='utf-8') as stream:
    for number,line in enumerate(stream,1):
        if '"session_meta"' not in line[:160] and '"turn_context"' not in line[:160]: continue
        item=json.loads(line); payload=item.get('payload',{})
        row=dict(line=number,raw_record_sha256=hashlib.sha256(line.encode('utf-8')).hexdigest())
        if item.get('type')=='session_meta': session=dict(row,**{k:payload.get(k) for k in ('id','cwd','source','model_provider')})
        if item.get('type')=='turn_context': turn=dict(row,**{k:payload.get(k) for k in ('model','effort','reasoning_effort','cwd')})
assert session and session['id']=='01a13c20-b7bd-7962-a954-f5841c09831c'
assert turn and turn['model']=='gpt-6.1-sol' and turn['effort']=='high'
write('configuration.json',dict(role='coordinator',actor='codex-'+session['id'],observed_utc=now(),model=turn['model'],reasoning=turn['effort'],source=str(metadata),scope='Own session_meta and current turn_context identity/configuration fields only; no conversation history.',session_record=session,turn_record=turn))
write('authorization.json',dict(source='Current explicit human operator message in this session',recorded_utc=now(),authorized=['Execute coordinator-setup.txt for IG-2B02 R01/R02','Then create one new LOCAL repair session on gpt-6.1-sol/high and deliver repair-launch.txt plus actual coordinator handoff'],prohibited=['Acceptance or done','Any downstream task or additional reviewer session','Alter frozen delivery/review or prepared instructions'],instruction_scope='Queue setup plus requested repair-session launch only. No independent reviewer is started.'))
records=[]
records.append(run('initial-workflow-validate',[PY,'-B','scripts/workflow.py','validate']))
records.append(run('initial-next',[PY,'-B','scripts/workflow.py','next']))
records.append(run('pre-setup-frozen-bases',[PY,'-B',str(P/'verify-frozen-bases.py'),'--report',str(C/'pre-setup-frozen-bases.json')]))
before=(R/'docs/work/queue.json').read_bytes()
with (C/'queue-before.json').open('xb') as stream: stream.write(before)
before_views={}
for rel in w.views(q):
    path=R/rel; before_views[rel]=pin(path)
    snapshot=C/'views-before'/rel; snapshot.parent.mkdir(parents=True,exist_ok=True)
    with snapshot.open('xb') as stream: stream.write(path.read_bytes())
write('views-before-pins.json',before_views)
draft=copy.deepcopy(q); selected=next(t for t in draft['tasks'] if t['id']=='IG-2B02')
for key,value in patch['task_field_updates'].items(): selected[key]=copy.deepcopy(value)
for key in patch['preserve_fields']: assert selected[key]==t[key],key
assert set(k for k in t if t[k]!=selected[k])==set(patch['task_field_updates'])
assert [x for x in draft['tasks'] if x['id']!='IG-2B02']==[x for x in q['tasks'] if x['id']!='IG-2B02']
assert {k:v for k,v in draft.items() if k!='tasks'}=={k:v for k,v in q.items() if k!='tasks'}
w.validate(draft,R,check_views=False)
write('draft-validation.json',dict(outcome='passed',selected_patch=pin(P/'coordinator-queue-patch-v2.json'),changed_task_fields=list(patch['task_field_updates']),status_events_unchanged=True,other_tasks_and_queue_fields_unchanged=True,context_policy_unchanged=True))
lock=R/'private/workflow/queue.lock'; fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
try:
    assert pin(R/'docs/work/queue.json')==patch['expected_queue'],'Concurrent queue change'
    pending=R/'docs/work/queue.pending.json'
    with pending.open('x',encoding='utf-8') as stream: json.dump(draft,stream,ensure_ascii=False,indent=2); stream.write('\n')
    assert pin(R/'docs/work/queue.json')==patch['expected_queue'],'Concurrent queue change'
    os.replace(pending,R/'docs/work/queue.json')
finally:
    os.close(fd); lock.unlink()
with (C/'queue-scoped-review.json').open('xb') as stream: stream.write((R/'docs/work/queue.json').read_bytes())
records.append(run('scope-render',[PY,'-B','scripts/workflow.py','render']))
changed_views=[rel for rel,old in before_views.items() if pin(R/rel)!=old]
assert set(changed_views)<= {'docs/work/tasks/IG-2B02.md','docs/ROADMAP.md','docs/STATUS.md','docs/HANDOFF.md'}
write('scope-application.json',dict(outcome='applied_exact_selected_v2_fields',before_queue=pin(C/'queue-before.json'),scoped_queue=pin(C/'queue-scoped-review.json'),status='review',events_preserved=True,changed_views=changed_views,unchanged_other_views=True,repair_directory_absent=not (R/state['reserved_absent_repair_attempt']).exists(),no_acceptance=True))
records.append(run('scope-workflow-validate',[PY,'-B','scripts/workflow.py','validate']))
records.append(run('scope-dry-run',[PY,'-B','scripts/workflow.py','dry-run','--task','IG-2B02']))
records.append(run('scope-repository-check',[PS,'-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02']))
records.append(run('scope-diff-check',['git','diff','--check']))
assert pin(R/'docs/work/queue.json')['sha256']==pin(C/'queue-scoped-review.json')['sha256']
write('scope-checks.json',dict(checks=records,started_utc=start,ended_utc=now(),wall_seconds=time.monotonic()-clock,transition_not_yet_attempted=True,repair_session_not_yet_created=True))
print('EXACT SCOPE SETUP AND CHECKS PASSED; status still review; ready for one coordinator transition.',flush=True)
