from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
PRIOR = ROOT / 'private/workflow/runs/IG-1D/review-20261013T122807Z'
command = [str(ROOT / '.venv/Scripts/python.exe'), '-m', 'pytest', str(RUN / 'export_history_probes.py'), '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/d2h', '--tb=short']
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + os.pathsep + str(PRIOR), PYTHONDONTWRITEBYTECODE='1')
started = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / 'history.log').open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
record = {'command': subprocess.list2cmdline(command), 'argv': command, 'exit_code': result.returncode, 'start_utc': started.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / 'history.log')}
with (RUN / 'history-check.json').open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
print(json.dumps(record))
print((RUN / 'history.log').read_text(encoding='utf-8', errors='replace'))
raise SystemExit(result.returncode)
