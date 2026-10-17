"""Run mandatory preparation checks with fresh logs; no queue edits or repair."""
import hashlib,json,os,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
R=Path('C:/repo/wargame-compiler');P=Path(__file__).resolve().parent
def pin(path):
    raw=path.read_bytes();return dict(path=path.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def now():return datetime.now(timezone.utc).isoformat()
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'src')+';C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages',PATH='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;'+env['PATH'])
commands=[('repository-check',['C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02']),('workflow-validate',[str(R/'.venv/Scripts/python.exe'),'-B','scripts/workflow.py','validate']),('diff-check',['git','diff','--check'])]
records=[]
for name,args in commands:
    start=now();clock=time.monotonic();result=subprocess.run(args,cwd=R,env=env,capture_output=True)
    for suffix,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        with (P/(name+'.'+suffix)).open('xb') as stream:stream.write(data)
    record=dict(command=args,exit_code=result.returncode,started_utc=start,ended_utc=now(),wall_seconds=time.monotonic()-clock,stdout=pin(P/(name+'.stdout')),stderr=pin(P/(name+'.stderr')));records.append(record)
    with (P/(name+'.command.json')).open('x',encoding='utf-8',newline='\n') as stream:json.dump(record,stream,indent=2);stream.write('\n')
    print(name,result.returncode,flush=True)
    if result.returncode:raise SystemExit(result.returncode)
state=json.loads((P/'preparation.json').read_text(encoding='utf-8'));assert pin(R/'docs/work/queue.json')==state['queue_snapshot'];assert not (R/state['reserved_absent_repair_attempt']).exists()
with (P/'checks.json').open('x',encoding='utf-8',newline='\n') as stream:json.dump(dict(checks=records,queue_unchanged=True,repair_attempt_absent=True,purpose='Preparation checks only; not repair, content review or acceptance.'),stream,indent=2);stream.write('\n')
print('PREPARATION CHECKS PASSED; queue unchanged; no repair session or directory.',flush=True)
