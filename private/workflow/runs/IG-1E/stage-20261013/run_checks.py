"""Capture IG-1E validation in new temp paths and immutable evidence files."""
from pathlib import Path
from datetime import datetime, timezone
import json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[5];RUN=Path(__file__).resolve().parent
name=sys.argv[1]
tail=['-q','-p','no:cacheprovider','--basetemp','private/workflow/checks/e1-'+name,'--tb=short']
commands={'explicit':[sys.executable,'-m','pytest','tests/integration','tests/wgu_adapter','tests/export']+tail,
 'accounting':[sys.executable,'-B',str(RUN/'accounting.py')],
 'seal':[sys.executable,'-B',str(RUN/'seal_snapshot.py')],
 'project':['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-1E'],
 'diff':['git','diff','--check']}
temp=ROOT/('private/workflow/checks/e1t-'+name);temp.mkdir(exist_ok=False)
env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',TEMP=str(temp),TMP=str(temp))
start=datetime.now(timezone.utc);tick=time.perf_counter()
with (RUN/(name+'.log')).open('xb') as f:p=subprocess.run(commands[name],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
record={'command':subprocess.list2cmdline(commands[name]),'argv':commands[name],'exit_code':p.returncode,
 'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-tick,
 'log':(RUN/(name+'.log')).relative_to(ROOT).as_posix()}
with (RUN/(name+'-check.json')).open('x',encoding='utf-8',newline='\n') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record),flush=True)
print((RUN/(name+'.log')).read_text(encoding='utf-8',errors='replace')[-2200:],flush=True)
raise SystemExit(p.returncode)
