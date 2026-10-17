"""Capture strict final regression and diff results for bounded repair delivery."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,time,sys
R=Path(__file__).parent
commands=[('regressions',[sys.executable,'-m','pytest','tests/wgu_adapter','private/workflow/runs/IG-1C/review-20261013T092949Z/probes.py','-q','-p','no:cacheprovider','--basetemp','private/workflow/checks/cr4','--tb=short']),('diff',['git','diff','--check'])]
checks=[]
for name,argv in commands:
 start=datetime.now(timezone.utc);clock=time.monotonic();p=subprocess.run(argv,capture_output=True,text=True)
 with (R/(name+'-final.log')).open('x',encoding='utf-8',newline='\n') as f:f.write(p.stdout+p.stderr)
 checks.append({'command':subprocess.list2cmdline(argv),'argv':argv,'exit_code':p.returncode,'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-clock,'log':str(R/(name+'-final.log'))})
 print(name,'exit',p.returncode,p.stdout[-1000:])
with (R/'final-checks.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(checks,f,indent=2);f.write('\n')
raise SystemExit(any(c['exit_code'] for c in checks))
