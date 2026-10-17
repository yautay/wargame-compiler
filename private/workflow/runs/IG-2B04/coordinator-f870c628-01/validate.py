"""Run unchanged validations and retain all output without broad context emission."""
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import uuid
from pathlib import Path

root=Path.cwd()
run=Path('private/workflow/runs/IG-2B04/coordinator-f870c628-01')
attempt=run/('validation-'+uuid.uuid4().hex[:12])
attempt.mkdir(exist_ok=False)
pwsh='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE'
commands=[[pwsh,'-NoProfile','-File','scripts/check.ps1','-Task','IG-2B04'],['git','diff','--check']]
checks=[]
for n,command in enumerate(commands):
    log=attempt/f'command-{n+1}.log'
    with log.open('wb') as stream:
        result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT)
    data=log.read_bytes()
    checks.append(dict(command=subprocess.list2cmdline(command),exit_code=result.returncode,
      log=dict(path=log.as_posix(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)),
      permission_denied=(b'PermissionError' in data or b'Access is denied' in data or b'Permission denied' in data)))
session=Path('private/workflow/orchestrator/20261015T200250Z-56a048a1/001-IG-2B04-coordinator-f870c628')
report=dict(format='wgc-coordinator-validation-1',role='coordinator',actor='ig2:001-IG-2B04-coordinator-f870c628:coordinator',
 model='gpt-6.1-sol',reasoning='high',configuration_evidence=(session/'runtime-configuration.json').as_posix(),
 configuration_sha256=hashlib.sha256((session/'runtime-configuration.json').read_bytes()).hexdigest(),
 task='IG-2B04',utc=datetime.now(timezone.utc).isoformat(),summary='Unchanged required validation commands; full outputs retained privately.',checks=checks)
path=attempt/'validation.json'
path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(report=path.as_posix(),checks=[{k:v for k,v in c.items() if k!='log'} for c in checks])))
raise SystemExit(0 if all(c['exit_code']==0 and not c['permission_denied'] for c in checks) else 1)
