"""Capture unchanged required reviewer validation commands."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys

OUT=Path('private/workflow/runs/IG-2B04/review-ce506337-01')
DELIVERY='private/workflow/runs/IG-2B04/continuation-13-16-rg04'
meta=json.loads((OUT/'checkpoint.json').read_text())
meta={k:v for k,v in meta.items() if k in ('role','actor','task','model','reasoning','configuration_evidence','configuration_sha256')}
checks=[]
commands=[
    ('validate-final',['.venv/Scripts/python.exe','-m','wgc.sources','validate',DELIVERY+'/final-verified/inventory.json']),
    ('validate-replay-a',['.venv/Scripts/python.exe','-m','wgc.sources','validate',DELIVERY+'/replay-a/inventory.json']),
    ('validate-replay-b',['.venv/Scripts/python.exe','-m','wgc.sources','validate',DELIVERY+'/replay-b/inventory.json']),
    ('sources',['.venv/Scripts/python.exe','-m','pytest','-q','tests/sources','--basetemp','private/workflow/checks/b04-review-ce506337-src','-p','no:cacheprovider','--tb=short']),
    ('repository',['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B04']),
    ('diff',['git','diff','--check']),
]
for name,command in commands:
    start=datetime.now(timezone.utc).isoformat()
    result=subprocess.run(command,capture_output=True)
    path=OUT/(name+'.log')
    data=result.stdout+result.stderr
    path.write_bytes(data)
    checks.append({'command':' '.join(command),'exit_code':result.returncode,'started_utc':start,'ended_utc':datetime.now(timezone.utc).isoformat(),'log':{'path':path.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}})
    (OUT/'checks.json').write_text(json.dumps({**meta,'checks':checks},indent=2)+'\n',encoding='utf-8')
    print(name,result.returncode,flush=True)
    if result.returncode:
        print(data.decode('utf-8',errors='replace')[-6000:],flush=True)
        sys.exit(result.returncode)
