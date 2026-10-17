"""Capture unchanged V01 validation commands and real process results."""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

attempt = Path(__file__).parent
claim = json.loads((attempt / 'claim.json').read_bytes())
metadata = {k: claim[k] for k in ('role', 'actor', 'model', 'reasoning',
                                'configuration_evidence', 'configuration_sha256', 'task')}
commands = {
    'sources-tests': ['.venv/Scripts/python.exe', '-B', '-m', 'pytest', '-q',
                      'tests/sources', '--basetemp',
                      'private/workflow/checks/v01-91db01b5-s1',
                      '-p', 'no:cacheprovider', '--tb=short'],
    'repository-check': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1',
                         '-Task', 'IG-2B02'],
    'root-inventory': ['.venv/Scripts/python.exe', '-B', '-m', 'wgc.sources',
                       'validate', 'private/workflow/runs/IG-2B02/'
                       'repair-r01-r02-20261015T091559Z-reserved-by-'
                       '01a13c20-b7bd-7962-a954-f5841c09831c/'
                       'final-verified/inventory.json'],
    'workflow-validate': ['.venv/Scripts/python.exe', '-B', 'scripts/workflow.py',
                          'validate'],
    'diff-check': ['git', 'diff', '--check'],
}
name = sys.argv[1]
command = commands[name]
report = attempt / (name + '.json')
assert not report.exists(), 'Validation records are immutable.'
if name == 'sources-tests':
    assert not Path(command[7]).exists(), 'Use a fresh basetemp.'
started = datetime.now(timezone.utc).isoformat()
clock = time.monotonic()
with (attempt / (name + '.stdout')).open('xb') as out:
    with (attempt / (name + '.stderr')).open('xb') as err:
        result = subprocess.run(command, stdout=out, stderr=err, check=False)
record = {**metadata, 'name': name, 'command': command,
          'exit_code': result.returncode, 'started_utc': started,
          'ended_utc': datetime.now(timezone.utc).isoformat(),
          'wall_seconds': time.monotonic() - clock,
          'stdout': (attempt / (name + '.stdout')).as_posix(),
          'stderr': (attempt / (name + '.stderr')).as_posix()}
with report.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
print(json.dumps(record))
sys.exit(result.returncode)
