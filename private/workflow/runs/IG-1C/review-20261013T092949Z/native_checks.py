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
    'affected-native': [PYTHON, '-m', 'pytest', 'tests/inputs', '-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/r1cn', '--tb=short'],
    'accounting-native': [PYTHON, '-B', str(RUN / 'accounting.py')],
}
command = commands[name]
temp = ROOT / 'private/workflow/checks/r1ct'
temp.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0', TEMP=str(temp), TMP=str(temp))
start = datetime.now(timezone.utc)
clock = time.perf_counter()
with (RUN / (name + '.log')).open('xb') as log:
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
measurement = {'command': subprocess.list2cmdline(command), 'exit_code': result.returncode, 'start_utc': start.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock, 'log': str(RUN / (name + '.log')), 'changed_conditions': 'Normally reviewed narrow local native Windows handle escalation; fresh basetemp; project-local TEMP/TMP. No parser/product changes or bypass of no-follow verification.', 'previous_attempt': 'affected-check.json' if name.startswith('affected') else 'accounting-sandbox-check.json'}
with (RUN / (name + '-check.json')).open('x', encoding='utf-8') as stream:
    json.dump(measurement, stream, indent=2)
    stream.write('\n')
print(json.dumps(measurement))
print((RUN / (name + '.log')).read_text(encoding='utf-8', errors='replace'))
raise SystemExit(result.returncode)
