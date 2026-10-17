"""Capture current explicit suites, queue and diff controls with real measurements."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,sys,time
R=Path(__file__).parent
commands=[('explicit',[sys.executable,'-m','pytest','tests/wgu_adapter','tests/export','-q','-p','no:cacheprovider','--basetemp','private/workflow/checks/df','--tb=short']),
          ('queue',[sys.executable,'scripts/workflow.py','validate']),('diff',['git','diff','--check'])]
checks=[]
for name,argv in commands:
 start=datetime.now(timezone.utc);clock=time.monotonic();p=subprocess.run(argv,capture_output=True,text=True)
 with (R/(name+'-final3.log')).open('x',encoding='utf-8',newline='\n') as f:f.write(p.stdout+p.stderr)
 checks.append({'command':subprocess.list2cmdline(argv),'argv':argv,'exit_code':p.returncode,
                'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
                'wall_seconds':time.monotonic()-clock,'log':str(R/(name+'-final3.log'))})
 print(name,'exit',p.returncode,p.stdout[-500:])
with (R/'captured-checks-head.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(checks,f,indent=2);f.write('\n')
raise SystemExit(any(c['exit_code'] for c in checks))
