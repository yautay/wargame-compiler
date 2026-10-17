"""Capture final actual-state checks and the preserved projection recovery."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
records=[]
commands=[('repository',['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-1E']),
          ('queue',[str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','validate']),
          ('diff',['git','diff','--check'])]
for name,argv in commands:
 start=datetime.now(timezone.utc);tick=time.perf_counter()
 with (RUN/('final-'+name+'.log')).open('xb') as f:
  p=subprocess.run(argv,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'),stdout=f,stderr=subprocess.STDOUT)
 records.append({'command':subprocess.list2cmdline(argv),'exit_code':p.returncode,
  'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
  'wall_seconds':time.perf_counter()-tick,'log':(RUN/('final-'+name+'.log')).relative_to(ROOT).as_posix()})
 print(name,p.returncode,flush=True)
q=json.loads((ROOT/'docs/work/queue.json').read_bytes())
states={t['id']:t['status'] for t in q['tasks'] if t['id'] in ['IG-1A','IG-1B','IG-1C','IG-1D','IG-1E']}
assert all(s=='done' for s in states.values())
assert not [t for t in q['tasks'] if t['id'].startswith('IG-2') and t['status']=='in_progress']
for name in ['final-stage-handoff.json','final-stage-handoff.md']:
 assert (RUN/name).is_file()
with (RUN/'final-checks.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump({'checks':records,'states':states,'queue_sha256':hashlib.sha256((ROOT/'docs/work/queue.json').read_bytes()).hexdigest(),
  'projection_recovery':{'observed_command':'scripts/workflow.py transition --task IG-1E --to done',
    'observed_output':"ERROR: [Errno 22] Invalid argument: 'C:\\repo\\wargame-compiler\\docs\\ROADMAP.md'",
    'individual_transition_exit_code':None,'reason_individual_exit_unknown':'The shell sequence did not capture this individual exit; later commands completed. Queue was inspected before any retry.',
    'queue_status_written_before_render_error':'done','transition_not_retried':True,
    'recovery_command':'python -B private/workflow/runs/IG-1C/resume-20261013/render_atomic.py',
    'recovery_and_following_validate_diff_handoff_sequence_completed':True},
  'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False,
  'tokens':None,'cost':None,'operator_time_seconds':None},f,indent=2);f.write('\n')
raise SystemExit(any(c['exit_code'] for c in records))
