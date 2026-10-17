import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

base = Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76')
runtime_path = Path('private/workflow/orchestrator/20261015T144301Z-98bff5f8/003-IG-2B03-coordinator-e285fb76/runtime-configuration.json')
runtime = json.loads(runtime_path.read_text())
assert (runtime['status'], runtime['model'], runtime['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
tools = json.loads((base/'toolchain.json').read_text())
env = os.environ.copy()
env['PYTHONPATH'] = tools['process_pythonpath']
env['PATH'] = tools['process_path_prefix'] + os.pathsep + env.get('PATH', '')
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['GIT_OPTIONAL_LOCKS'] = '0'
name, *command = sys.argv[1:]
assert command and not (base/(name+'.json')).exists()
start = datetime.now(timezone.utc).isoformat()
tick = time.monotonic()
result = subprocess.run(command, env=env, capture_output=True)
artifacts = []
for suffix, value in [('stdout', result.stdout), ('stderr', result.stderr)]:
    path = base/(name+'.'+suffix)
    with path.open('xb') as stream:
        stream.write(value)
    artifacts.append(dict(path=path.as_posix(), bytes=len(value), sha256=hashlib.sha256(value).hexdigest()))
report = dict(role='coordinator', actor='ig2:003-IG-2B03-coordinator-e285fb76:coordinator', task='IG-2B03', model=runtime['model'], reasoning=runtime['reasoning'], configuration_evidence=runtime_path.as_posix(), configuration_sha256=hashlib.sha256(runtime_path.read_bytes()).hexdigest(), command=command, exit_code=result.returncode, started_utc=start, ended_utc=datetime.now(timezone.utc).isoformat(), wall_seconds=time.monotonic()-tick, artifacts=artifacts, process_environment_pin=dict(path=(base/'toolchain.json').as_posix(), sha256=hashlib.sha256((base/'toolchain.json').read_bytes()).hexdigest()))
with (base/(name+'.json')).open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps(dict(name=name, exit_code=result.returncode, report=(base/(name+'.json')).as_posix(), stdout_tail=result.stdout.decode('utf-8', errors='replace')[-1200:], stderr_tail=result.stderr.decode('utf-8', errors='replace')[-1200:])))
sys.exit(result.returncode)
