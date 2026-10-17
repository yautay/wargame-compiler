import os,subprocess,json,time,datetime
from pathlib import Path
R=Path.cwd();V=R/'private/workflow/runs/IG-2B02/review-20261015T134030Z-ig2-2cc49348';B=R/'private/workflow/runs/IG-2B02/repair-r01-r02-20261015T091559Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c'
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONPATH']=str(R/'src')+';C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages';native='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native';env['PATH']=native+'/poppler/Library/bin;'+env['PATH'];py=str(R/'.venv/Scripts/python.exe')
commands=[('root-inventory',[py,'-B','-m','wgc.sources','validate',str(B/'final-verified/inventory.json')]),('sources-tests',[py,'-B','-m','pytest','-q','tests/sources','--basetemp',str(R/'private/workflow/checks/rb02-2cc49348'),'-p','no:cacheprovider','--tb=short']),('repository-check',[native+'/powershell/pwsh.exe','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02']),('workflow-validate',[py,'-B','scripts/workflow.py','validate']),('diff-check',['git','diff','--check']),('original-pages',[native+'/poppler/Library/bin/pdftoppm.exe','-f','5','-l','8','-r','144','-png','private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf',str(V/'original')])]
records=[]
for name,cmd in commands:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();r=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
 (V/(name+'.stdout')).write_bytes(r.stdout);(V/(name+'.stderr')).write_bytes(r.stderr)
 rec=dict(name=name,command=cmd,exit_code=r.returncode,started_utc=start,wall_seconds=time.monotonic()-t,stdout=(V/(name+'.stdout')).relative_to(R).as_posix(),stderr=(V/(name+'.stderr')).relative_to(R).as_posix());records.append(rec)
 with (V/'checks.json').open('w') as f:json.dump(records,f,indent=2)
 print(name,r.returncode,r.stdout.decode('utf-8',errors='replace')[-250:],flush=True)
