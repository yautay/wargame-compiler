"""Run one bounded local command, retaining separate byte-exact logs and checkpoint."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

R = Path('C:/repo/wargame-compiler')
A = Path(__file__).resolve().parent

def now():
    return datetime.now(timezone.utc).isoformat()

def pin(p):
    return {'path': p.relative_to(R).as_posix(), 'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def write(p, value, exclusive=True):
    with p.open('x' if exclusive else 'w', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')

if __name__ == '__main__':
    label = sys.argv[1]
    command = sys.argv[2:]
    assert command and not (A / (label + '.command.json')).exists()
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(R / 'src') + ';C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages'
    env['PATH'] = 'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;' + env['PATH']
    start = now()
    clock = time.monotonic()
    out = A / (label + '.stdout')
    err = A / (label + '.stderr')
    with out.open('xb') as stdout, err.open('xb') as stderr:
        p = subprocess.run(command, cwd=R, env=env, stdout=stdout, stderr=stderr)
    record = dict(command=command, exit_code=p.returncode, started_utc=start,
                  ended_utc=now(), wall_seconds=time.monotonic() - clock,
                  process_environment_overrides={k: env[k] for k in ('PYTHONDONTWRITEBYTECODE', 'PYTHONPATH')},
                  path_prefix=env['PATH'].split(';')[0], stdout=pin(out), stderr=pin(err))
    write(A / (label + '.command.json'), record)
    cp = json.loads((A / 'checkpoint.json').read_text(encoding='utf-8'))
    cp['updated_utc'] = now()
    cp['commands'].append(pin(A / (label + '.command.json')))
    cp['last_command'] = record
    cp['next_operation'] = 'Inspect recorded result before any dependent operation.'
    if p.returncode:
        cp['blocker'] = 'Command failed; inspect exact retained stderr/state before another attempt.'
    write(A / 'checkpoint.json', cp, exclusive=False)
    print(json.dumps(record, indent=2))
    print('STDOUT TAIL:', out.read_text(encoding='utf-8', errors='replace')[-2000:])
    print('STDERR TAIL:', err.read_text(encoding='utf-8', errors='replace')[-2000:])
    sys.exit(p.returncode)
