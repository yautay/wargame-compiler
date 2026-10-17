"""Record preparation checks without touching any frozen executor output."""
import subprocess,os,json,hashlib,time
from pathlib import Path
from datetime import datetime,timezone
R=Path('C:/repo/wargame-compiler');A=Path(__file__).resolve().parent
env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='C:/repo/wargame-compiler/src;C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages',PATH='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;'+env['PATH'])
def pin(p):
 raw=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def now():return datetime.now(timezone.utc).isoformat()
commands=[('repository-check',['C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02']),('workflow-validate',['C:/repo/wargame-compiler/.venv/Scripts/python.exe','-B','scripts/workflow.py','validate']),('diff-check',['git','diff','--check'])]
records=[]
for label,args in commands:
 start=now();clock=time.monotonic();result=subprocess.run(args,cwd=R,env=env,capture_output=True)
 for name,data in [('stdout',result.stdout),('stderr',result.stderr)]:
  with (A/(label+'.'+name)).open('xb') as f:f.write(data)
 record={'command':args,'exit_code':result.returncode,'started_utc':start,'ended_utc':now(),'wall_seconds':time.monotonic()-clock,'stdout':pin(A/(label+'.stdout')),'stderr':pin(A/(label+'.stderr'))};records.append(record)
 with (A/(label+'.command.json')).open('x',encoding='utf-8',newline='\n') as f:json.dump(record,f,indent=2);f.write('\n')
 print(label,result.returncode,flush=True)
 if result.returncode!=0:print(result.stderr.decode('utf-8',errors='replace'));raise SystemExit(result.returncode)
prep=json.loads((A/'preparation.json').read_text(encoding='utf-8'));assert pin(R/'docs/work/queue.json')==prep['queue']
with (A/'checks.json').open('x',encoding='utf-8',newline='\n') as f:json.dump({'checks':records,'queue_unchanged':True,'purpose':'Instruction preparation checks, not independent content review.'},f,indent=2);f.write('\n')
print('PREPARATION CHECKS PASSED; queue unchanged',flush=True)
