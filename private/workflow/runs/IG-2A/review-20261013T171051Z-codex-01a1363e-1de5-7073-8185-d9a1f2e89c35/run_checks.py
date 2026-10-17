import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
ATTEMPT=ROOT/'private/workflow/runs/IG-2A/attempt-20261013T155212Z'
env=os.environ.copy()
tc=json.loads((ATTEMPT/'toolchain.json').read_text())
env['PYTHONPATH']=tc['process_pythonpath']; env['PYTHONDONTWRITEBYTECODE']='1';env['GIT_OPTIONAL_LOCKS']='0'
env['PATH']=str(Path(tc['executables']['pdfinfo']['path']).parent)+';'+env['PATH']
env['TEMP']=str(OUT/'tmp');env['TMP']=env['TEMP'];(OUT/'tmp').mkdir(exist_ok=True)
def save(n,d): (OUT/n).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def run(name,args):
    start=datetime.datetime.now(datetime.timezone.utc); t=time.monotonic()
    p=subprocess.run(args,cwd=ROOT,env=env,capture_output=True)
    (OUT/(name+'.stdout')).write_bytes(p.stdout);(OUT/(name+'.stderr')).write_bytes(p.stderr)
    rec={'command':subprocess.list2cmdline(args),'argv':args,'exit_code':p.returncode,'started_utc':start.isoformat(),'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'stdout':name+'.stdout','stderr':name+'.stderr'}
    save(name+'.json',rec);print(name,p.returncode,p.stdout.decode('utf-8',errors='replace')[-1500:],flush=True)
    return rec
if __name__=='__main__':
    save('configuration.json',{'role':'reviewer','actor':'codex-'+os.environ['CODEX_THREAD_ID'],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':{'kind':'current-session operator confirmation','question':'Confirm actual model/reasoning of this current session; required GPT-6.1 Sol / high','operator_reply':'potwierdzam','received_in_current_review_turn':True},'identity_evidence':{'CODEX_THREAD_ID':os.environ['CODEX_THREAD_ID']},'started_utc':'2026-10-13T17:10:51.7733569Z','measurement_correction':'checkpoint.json used an unverified earlier start literal; this record supersedes it. Measured review interval starts at first captured UTC timestamp; preflight duration is unavailable.','tokens':None,'cost':None,'operator_seconds':None})
    checks=[]
    checks.append(run('sources-tests',[sys.executable,'-m','pytest','tests/sources','-q','--basetemp',str(OUT/'t'),'-p','no:cacheprovider','--tb=short']))
    checks.append(run('workflow-validate',[sys.executable,'scripts/workflow.py','validate']))
    checks.append(run('diff-check',['git','diff','--check']))
    checks.append(run('project-check',['pwsh','-NoProfile','-File',str(OUT/'check_adapter.ps1')]))
    save('required-checks.json',checks)
