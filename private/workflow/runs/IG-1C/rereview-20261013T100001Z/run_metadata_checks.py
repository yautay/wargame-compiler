import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
command = [str(ROOT / '.venv/Scripts/python.exe'), '-m', 'pytest', str(RUN / 'metadata_edge_probes.py'), '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/r2cm', '--tb=short']
temp = ROOT / 'private/workflow/checks/r2tm'
temp.mkdir(exist_ok=False)
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), PYTHONDONTWRITEBYTECODE='1', TEMP=str(temp), TMP=str(temp))
start = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / 'metadata-edges.log').open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
measurement = {'command': subprocess.list2cmdline(command), 'argv': command, 'exit_code': result.returncode, 'start_utc': start.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / 'metadata-edges.log')}
with (RUN / 'metadata-edges-check.json').open('x', encoding='utf-8') as stream:
    json.dump(measurement, stream, indent=2)
    stream.write('\n')
print(json.dumps(measurement))
print((RUN / 'metadata-edges.log').read_text(encoding='utf-8'))
raise SystemExit(result.returncode)
