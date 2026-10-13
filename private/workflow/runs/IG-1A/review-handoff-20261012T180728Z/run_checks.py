"""Replay existing frozen checks into fresh evidence directories; no repairs."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).parent
REVIEW = ROOT / 'private/workflow/runs/IG-1A/review-repair02-20261012T174537Z-6b6e02fa'
ORIGINAL = ROOT / 'private/workflow/runs/IG-1A/review-independent-20261012T164949Z-163b3167'
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0', 'PYTHONPATH': str(ROOT / 'src')}
copies = []
for name in ['test_rereview.py', 'test_final_boundaries.py']:
    target = HERE / name
    assert not target.exists()
    target.write_bytes((REVIEW / name).read_bytes())
    copies.append({'source': str((REVIEW / name).relative_to(ROOT)).replace('\\', '/'),
                   'copy': str(target.relative_to(ROOT)).replace('\\', '/'),
                   'source_sha256': hashlib.sha256((REVIEW / name).read_bytes()).hexdigest(),
                   'copy_sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
(HERE / 'suite-copy-provenance.json').write_text(json.dumps(copies, indent=2) + '\n', encoding='utf-8')
checks = []


def run(args, log):
    started = datetime.now(timezone.utc).isoformat()
    before = time.perf_counter()
    result = subprocess.run(args, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    wall = time.perf_counter() - before
    (HERE / log).write_bytes(result.stdout)
    output = result.stdout.decode('utf-8', errors='replace')
    count = re.search(r'(\d+) passed(?:[^\n]*?) in ([\d.]+)s', output)
    root = re.search(r'LOG_ROOT=(.+)', output)
    entry = {'argv': args, 'command': subprocess.list2cmdline(args), 'exit_code': result.returncode,
             'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
             'wall_seconds': wall, 'log': str((HERE / log).relative_to(ROOT)).replace('\\', '/'),
             'tests_passed': int(count[1]) if count else None,
             'reported_pytest_seconds': float(count[2]) if count else None}
    if root:
        log_root = Path(root[1].strip())
        entry['log_root'] = str(log_root.relative_to(ROOT)).replace('\\', '/')
        entry['result'] = json.loads((log_root / 'result.json').read_text(encoding='utf-8-sig'))
    checks.append(entry)
    (HERE / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(entry), flush=True)
    return result.returncode


run(['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-1A'], 'project-check.log')
run([sys.executable, '-m', 'pytest', str(HERE / 'test_rereview.py'), str(ORIGINAL / 'test_review.py'),
     str(HERE / 'test_final_boundaries.py'), '-q', '-p', 'no:cacheprovider', '--basetemp',
     str(HERE / 'independent-temp'), '--tb=short'], 'independent-suites.log')
run(['git', 'diff', '--check'], 'diff-check.log')
run([sys.executable, str(HERE / 'verify_handoff.py')], 'hash-verification.log')
raise SystemExit(1 if any(c['exit_code'] for c in checks) else 0)
