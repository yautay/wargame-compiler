"""Replay unchanged saved reviewer probes into fresh executor evidence."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = Path(__file__).parent
PROBES = Path('private/workflow/runs/IG-1B/repair01-probes-20261012T193641Z')
env = {**os.environ, 'PYTHONPATH': str(Path.cwd() / 'src'), 'PYTHONDONTWRITEBYTECODE': '1'}
records = []
for script in ['review_controls.py', 'native_handle_probe.py', 'private_audit.py']:
    argv = [sys.executable, str(PROBES / script)]
    started = datetime.now(timezone.utc).isoformat()
    mark = time.perf_counter()
    result = subprocess.run(argv, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = HERE / (script.removesuffix('.py') + '.log')
    log.write_bytes(result.stdout)
    record = {'command': subprocess.list2cmdline(argv), 'argv': argv, 'exit_code': result.returncode,
              'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
              'wall_seconds': time.perf_counter() - mark,
              'log': log.absolute().relative_to(Path.cwd()).as_posix(),
              'execution_context': 'Reviewed local require_escalated; explicit native Windows handle/link checks'}
    records.append(record)
    (HERE / 'replayed-checks.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record), flush=True)
raise SystemExit(1 if any(r['exit_code'] for r in records) else 0)
