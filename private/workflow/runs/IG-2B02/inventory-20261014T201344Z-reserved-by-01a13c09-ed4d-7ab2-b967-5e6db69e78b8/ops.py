"""Owned executor operations, UTF-8 evidence, exact command recording."""
import json, hashlib, os, sys, subprocess, time
from pathlib import Path
from datetime import datetime, timezone
R=Path('C:/repo/wargame-compiler')
A=Path(__file__).resolve().parent
AR=A.relative_to(R).as_posix()
P='private/workflow/runs/IG-2B02/preparation-20261014T201344Z-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
PK='private/workflow/packets/IG-2B02-46811ecf99cf4834b010368daddf5f08'
PY=str(R/'.venv/Scripts/python.exe')
POP='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin'
PW='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE'
ENV=os.environ.copy()
ENV.update(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'src')+';C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages',PATH=POP+';'+ENV['PATH'])
def now():return datetime.now(timezone.utc).isoformat()
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def pin(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes()
 return {'path':p.relative_to(R).as_posix() if p.is_relative_to(R) else p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,o):
 p=Path(p);p=p if p.is_absolute() else A/p;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
def run(label,args):
 start=now();clock=time.monotonic();r=subprocess.run(args,cwd=R,env=ENV,capture_output=True)
 for stream,data in [('stdout',r.stdout),('stderr',r.stderr)]:
  with (A/(label+'.'+stream)).open('xb') as f:f.write(data)
 record={'command':args,'exit_code':r.returncode,'started_utc':start,'ended_utc':now(),'wall_seconds':time.monotonic()-clock,'stdout':pin(A/(label+'.stdout')),'stderr':pin(A/(label+'.stderr'))}
 write(label+'.command.json',record)
 print(label,r.returncode,flush=True)
 if r.stderr:print(r.stderr.decode('utf-8',errors='replace'),flush=True)
 return record
def checkpoint(stage,completed,next_operation,blocker=None):
 initial=load(AR+'/preclaim-checkpoint.json') if (A/'preclaim-checkpoint.json').exists() else {}
 records=[load(p.relative_to(R).as_posix()) for p in sorted(A.glob('*.command.json'))]
 current=[pin(p) for p in A.rglob('*') if p.is_file() and p.name not in ('checkpoint.json',)]
 initial.update(stage=stage,completed_criteria=completed,commands=records,current_owned_hashes=current,blocker=blocker,next_operation=next_operation,updated_utc=now())
 raw=json.dumps(initial,ensure_ascii=False,indent=2)+'\n'
 (A/'checkpoint.json').write_text(raw,encoding='utf-8',newline='\n')
 write('checkpoint-'+stage+'.json',initial)
if __name__=='__main__':
 label=sys.argv[1];record=run(label,sys.argv[2:]);sys.exit(record['exit_code'])
