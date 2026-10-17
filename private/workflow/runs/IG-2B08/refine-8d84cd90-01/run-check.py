"""Run the unchanged required check, retaining output without context-wide path dumps."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

root = Path.cwd()
own = root / 'private/workflow/runs/IG-2B08/refine-8d84cd90-01'
for attempt in (1, 2):
    log = own / f'full-check-{attempt:02}.log'
    if not log.exists():
        break
else:
    raise RuntimeError('Both unchanged validation attempts already exist')
start = time.monotonic()
started = datetime.now(timezone.utc).isoformat()
command = ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B08']
with log.open('xb') as stream:
    result = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT)
elapsed = time.monotonic() - start
selected = []
check_root = None
with log.open(encoding='utf-8-sig', errors='replace') as stream:
    for line in stream:
        if line.startswith('LOG_ROOT='):
            check_root = Path(line.strip().split('=', 1)[1])
        if line.startswith(('Validated ', 'Rendered ', 'IG-2B08')) or ' passed' in line or ' failed' in line or 'Checks failed: plan=' in line:
            selected.append(line.strip()[:500])
config_rel = 'private/workflow/orchestrator/20261017T064446Z-f1a71866/001-IG-2B08-coordinator-8d84cd90/runtime-configuration.json'
def pin(p):
    with p.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'path': p.relative_to(root).as_posix(), 'sha256': digest, 'bytes': p.stat().st_size}
report = {
    'format': 'wgc-coordinator-check-execution-1', 'task': 'IG-2B08',
    'role': 'coordinator', 'actor': 'ig2:001-IG-2B08-coordinator-8d84cd90:coordinator',
    'model': 'gpt-6.1-sol', 'reasoning': 'high',
    'configuration_evidence': config_rel,
    'configuration_sha256': pin(root / config_rel)['sha256'],
    'command': ' '.join(command), 'exit_code': result.returncode,
    'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
    'wall_seconds': elapsed, 'log': pin(log), 'selected_check_summaries': selected,
    'validation_assertions_changed': False}
if check_root is not None:
    assert check_root.resolve().is_relative_to((root / 'private/workflow/checks').resolve())
    result_file = check_root / 'result.json'
    if result_file.is_file():
        report['check_result'] = pin(result_file)
        # These four exit fields are operational results, not task/dependency content.
        values = json.loads(result_file.read_text(encoding='utf-8-sig'))
        report['check_exits'] = {k: values[k] for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit')}
with (own / f'full-check-{attempt:02}.json').open('x', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
    f.write('\n')
print(json.dumps({'report': f'private/workflow/runs/IG-2B08/refine-8d84cd90-01/full-check-{attempt:02}.json',
                  'exit_code': result.returncode, 'check_exits': report.get('check_exits'),
                  'summaries': selected}))
raise SystemExit(result.returncode)
