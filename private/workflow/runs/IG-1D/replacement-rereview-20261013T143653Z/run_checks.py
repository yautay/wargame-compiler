"""Capture exact commands, failures and local elapsed time in a fresh review run."""
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
key = sys.argv[2] if len(sys.argv) > 2 else name
pytest_base = [PYTHON, '-m', 'pytest']
tail = ['-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/r5-' + key, '--tb=short']
commands = {
    'original': pytest_base + [str(PRIOR / 'probes.py'), str(PRIOR / 'lineage_probes.py')] + tail,
    'risk': pytest_base + [str(RUN / 'risk_probes.py'), str(RUN / 'receipt_edge_probes.py')] + tail,
    'explicit': pytest_base + ['tests/wgu_adapter', 'tests/export'] + tail,
    'history': pytest_base + [str(RUN / 'export_history_probes.py')] + tail,
    'accounting': [PYTHON, '-B', str(RUN / 'accounting.py')],
    'project': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-1D'],
    'diff': ['git', 'diff', '--check'],
}
command = commands[name]
temp = ROOT / ('private/workflow/checks/r5t-' + key)
temp.mkdir(exist_ok=False)
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + os.pathsep + str(PRIOR),
    PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0', TEMP=str(temp), TMP=str(temp))
started = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / (key + '.log')).open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
record = {'command': subprocess.list2cmdline(command), 'argv': command, 'exit_code': result.returncode,
    'start_utc': started.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(),
    'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / (key + '.log')),
    'process_local_import_path': [str(ROOT / 'src'), str(PRIOR)]}
with (RUN / (key + '-check.json')).open('x', encoding='utf-8') as f:
    json.dump(record, f, indent=2); f.write('\n')
print(json.dumps(record), flush=True)
print((RUN / (key + '.log')).read_text(encoding='utf-8', errors='replace'), flush=True)
raise SystemExit(result.returncode)
