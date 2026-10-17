import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
command = [str(ROOT / '.venv/Scripts/python.exe'), '-m', 'pytest', str(RUN / 'lineage_probes.py'), '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/drl', '--tb=short']
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src') + os.pathsep + str(RUN), PYTHONDONTWRITEBYTECODE='1')
started = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / 'lineage-probes.log').open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
record = {'command': subprocess.list2cmdline(command), 'argv': command, 'exit_code': result.returncode, 'start_utc': started.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / 'lineage-probes.log')}
with (RUN / 'lineage-probes-check.json').open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
print(json.dumps(record))
print((RUN / 'lineage-probes.log').read_text(encoding='utf-8', errors='replace'))
raise SystemExit(result.returncode)
