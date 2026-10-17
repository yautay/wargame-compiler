from datetime import datetime,timezone
import json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];RUN=Path(__file__).resolve().parent
name=sys.argv[1];py=str(ROOT/'.venv/Scripts/python.exe')
commands={'explicit':[py,'-m','pytest','tests/integration','tests/wgu_adapter','tests/export','-q','-p','no:cacheprovider','--basetemp','private/workflow/checks/e2-public','--tb=short'],
    'accounting':[py,'-B',str(RUN/'accounting.py')],
    'supplemental':[py,'-B',str(RUN/'supplemental_audit.py')],
    'seal':[py,'-B',str(RUN/'independent_seal.py')],
    'project':['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-1E'],
    'diff':['git','diff','--check']}
command=commands[name];temp=ROOT/('private/workflow/checks/e2t-'+name);temp.mkdir(exist_ok=False)
env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',TEMP=str(temp),TMP=str(temp))
start=datetime.now(timezone.utc);tick=time.perf_counter()
with (RUN/(name+'.log')).open('xb') as f:r=subprocess.run(command,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
record={'command':subprocess.list2cmdline(command),'argv':command,'exit_code':r.returncode,
    'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-tick,
    'log':(RUN/(name+'.log')).relative_to(ROOT).as_posix(),'process_local_import_path':[str(ROOT/'src')]}
with (RUN/(name+'-check.json')).open('x',encoding='utf-8') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record));print((RUN/(name+'.log')).read_text(encoding='utf-8',errors='replace'))
raise SystemExit(r.returncode)
