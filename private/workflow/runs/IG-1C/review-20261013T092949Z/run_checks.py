"""Run only requested local checks, with independent logs and real exits."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
PYTHON = str(ROOT / '.venv/Scripts/python.exe')
name = sys.argv[1]
commands = {
    'adapter': [PYTHON, '-m', 'pytest', 'tests/wgu_adapter', '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/r1ca', '--tb=short'],
    'probes': [PYTHON, '-m', 'pytest', str(RUN / 'probes.py'), '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/r1cp', '--tb=short'],
    'affected': [PYTHON, '-m', 'pytest', 'tests/inputs', '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/r1ci', '--tb=short'],
    'project': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-1C'],
    'diff': ['git', 'diff', '--check'],
}
command = commands[name]
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
start = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / (name + '.log')).open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
end = datetime.now(timezone.utc)
measurement = {'command': subprocess.list2cmdline(command), 'exit_code': result.returncode, 'start_utc': start.isoformat(), 'end_utc': end.isoformat(), 'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / (name + '.log'))}
with (RUN / (name + '-check.json')).open('x', encoding='utf-8') as stream:
    json.dump(measurement, stream, indent=2)
    stream.write('\n')
print(json.dumps(measurement))
print((RUN / (name + '.log')).read_text(encoding='utf-8', errors='replace'))
raise SystemExit(result.returncode)
