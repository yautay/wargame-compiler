"""Check instruction preparation only, without changing queue or frozen runs."""
import hashlib, json, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

R = Path('C:/repo/wargame-compiler')
P = Path(__file__).resolve().parent
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH='C:/repo/wargame-compiler/src;C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages', PATH='C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;' + env['PATH'])

def pin(path):
    raw = path.read_bytes()
    return dict(path=path.relative_to(R).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def now():
    return datetime.now(timezone.utc).isoformat()

commands = [
    ('repository-check', ['C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B02']),
    ('workflow-validate', [str(R / '.venv/Scripts/python.exe'), '-B', 'scripts/workflow.py', 'validate']),
    ('diff-check', ['git', 'diff', '--check']),
]
records = []
for label, args in commands:
    start = now()
    clock = time.monotonic()
    result = subprocess.run(args, cwd=R, env=env, capture_output=True)
    for name, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        with (P / (label + '.' + name)).open('xb') as stream:
            stream.write(data)
    record = dict(command=args, exit_code=result.returncode, started_utc=start, ended_utc=now(), wall_seconds=time.monotonic()-clock, stdout=pin(P/(label+'.stdout')), stderr=pin(P/(label+'.stderr')))
    records.append(record)
    with (P/(label+'.command.json')).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(label, result.returncode, flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
state = json.loads((P/'preparation.json').read_text(encoding='utf-8'))
assert pin(R/'docs/work/queue.json') == state['queue_snapshot']
assert not (R/state['reserved_absent_repair_attempt']).exists()
with (P/'checks.json').open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(dict(checks=records, queue_unchanged=True, reserved_repair_attempt_absent=True, purpose='Instruction preparation checks only; no repair, independent content review or acceptance.'), stream, indent=2)
    stream.write('\n')
print('PREPARATION CHECKS PASSED; queue unchanged; repair attempt absent', flush=True)
