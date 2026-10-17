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
    'explicit': [PYTHON, '-m', 'pytest', 'tests/wgu_adapter', 'tests/export', '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/dra', '--tb=short'],
    'probes': [PYTHON, '-m', 'pytest', str(RUN / 'probes.py'), '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/drp', '--tb=short'],
    'accounting': [PYTHON, '-B', str(RUN / 'accounting.py')],
    'project': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-1D'],
    'diff': ['git', 'diff', '--check'],
}
command = commands[name]
temp = ROOT / ('private/workflow/checks/drt-' + name)
temp.mkdir(exist_ok=False)
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0', TEMP=str(temp), TMP=str(temp))
started = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / (name + '.log')).open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
report = {'command': subprocess.list2cmdline(command), 'argv': command, 'exit_code': result.returncode, 'start_utc': started.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / (name + '.log'))}
with (RUN / (name + '-check.json')).open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps(report))
print((RUN / (name + '.log')).read_text(encoding='utf-8', errors='replace'))
raise SystemExit(result.returncode)
