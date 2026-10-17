from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
PRIOR = ROOT / 'private/workflow/runs/IG-1D/review-20261013T122807Z'
PYTHON = str(ROOT / '.venv/Scripts/python.exe')
name = sys.argv[1]
commands = {
    'original': [PYTHON, '-m', 'pytest', str(PRIOR / 'probes.py'), str(PRIOR / 'lineage_probes.py'), '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/d2o', '--tb=short'],
    'risk': [PYTHON, '-m', 'pytest', str(RUN / 'risk_probes.py'), str(RUN / 'receipt_edge_probes.py'), '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/d2r', '--tb=short'],
    'explicit': [PYTHON, '-m', 'pytest', 'tests/wgu_adapter', 'tests/export', '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/d2a', '--tb=short'],
    'accounting': [PYTHON, '-B', str(RUN / 'accounting.py')],
    'project': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-1D'],
    'diff': ['git', 'diff', '--check'],
}
command = commands[name]
temp = ROOT / ('private/workflow/checks/d2t-' + name)
temp.mkdir(exist_ok=False)
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + os.pathsep + str(PRIOR), PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0', TEMP=str(temp), TMP=str(temp))
started = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / (name + '.log')).open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
record = {'command': subprocess.list2cmdline(command), 'argv': command, 'exit_code': result.returncode, 'start_utc': started.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / (name + '.log')), 'process_local_import_path': [str(ROOT / 'src'), str(PRIOR)]}
with (RUN / (name + '-check.json')).open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
print(json.dumps(record))
print((RUN / (name + '.log')).read_text(encoding='utf-8', errors='replace'))
raise SystemExit(result.returncode)
