from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,sys,time,os
R=Path(__file__).parent
env=os.environ.copy();env['PYTHONPATH']=str(Path.cwd()/'src')+os.pathsep+str(Path.cwd()/'private/workflow/runs/IG-1D/review-20261013T122807Z')
commands=[('explicit',[sys.executable,'-m','pytest','tests/wgu_adapter','tests/export',
    'private/workflow/runs/IG-1D/review-20261013T122807Z/probes.py',
    'private/workflow/runs/IG-1D/review-20261013T122807Z/lineage_probes.py',
    '-q','-p','no:cacheprovider','--basetemp','private/workflow/checks/dr5','--tb=short']),
    ('queue',[sys.executable,'scripts/workflow.py','validate']),('diff',['git','diff','--check'])]
checks=[]
for name,argv in commands:
 start=datetime.now(timezone.utc);clock=time.monotonic();p=subprocess.run(argv,capture_output=True,text=True,env=env)
 with (R/(name+'.log')).open('x',encoding='utf-8',newline='\n') as f:f.write(p.stdout+p.stderr)
 checks.append({'command':subprocess.list2cmdline(argv),'argv':argv,'exit_code':p.returncode,
   'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
   'wall_seconds':time.monotonic()-clock,'log':str(R/(name+'.log'))})
 print(name,p.returncode,p.stdout[-500:])
with (R/'captured-checks.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(checks,f,indent=2);f.write('\n')
raise SystemExit(any(c['exit_code'] for c in checks))
