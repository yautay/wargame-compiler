"""Revalidate immutable existing inventories without rebuilding evidence."""
import subprocess
import sys
from repair_indexes import META, OLD, ROOT, RUN, pin, write

checks = []
for name in ['final-verified', 'replay-a-verified', 'replay-b-verified',
             'components', 'components-replay-a', 'components-replay-b']:
    inventory = (OLD / name / 'inventory.json').relative_to(ROOT).as_posix()
    argv = ['.venv/Scripts/python.exe', '-B', '-m', 'wgc.sources', 'validate', inventory]
    result = subprocess.run(argv, cwd=ROOT, capture_output=True)
    log = RUN / ('root-' + name + '.log')
    with log.open('xb') as handle:
        handle.write(result.stdout)
        handle.write(result.stderr)
    checks.append({'command': ' '.join(argv), 'exit_code': result.returncode,
                   'log': pin(log)})
    print(name, 'exit', result.returncode, flush=True)
write('root-validations.json', {**META, 'checks': checks,
      'policy': 'Existing two complete independent replay pairs retained and independently root-validated. No rebuilding or evidence regeneration.'})
sys.exit(0 if all(check['exit_code'] == 0 for check in checks) else 1)
