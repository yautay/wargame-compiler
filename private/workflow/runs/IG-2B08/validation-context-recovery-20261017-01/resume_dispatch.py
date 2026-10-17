"""Preserve an externally interrupted pre-model dispatch and resume authorized review."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B08/validation-context-recovery-20261017-01/'
OLD_RUN = 'private/workflow/orchestrator/20261017T094517Z-0153b027/'


def main():
    out = ROOT / PREP / 'dispatch-recovery-01'
    out.mkdir(exist_ok=False)
    def write(name, body):
        with (out / name).open('x', encoding='utf-8') as f:
            json.dump(body, f, indent=2); f.write('\n')
    lock = ROOT / 'private/workflow/ig2-orchestrator.lock'
    lock_hash = w.digest(lock)
    old_lock = w.read_json(lock)
    assert old_lock['pid'] == 7376
    assert Path(old_lock['run']).resolve() == (ROOT / OLD_RUN).resolve()
    assert not (ROOT / OLD_RUN / 'status.json').exists()
    old_session = ROOT / OLD_RUN / '001-IG-2B08-reviewer-7257a513'
    assert not (old_session / 'process.json').exists()
    assert not (old_session / 'runtime-configuration.json').exists()
    # Approved fresh PID inspection inside the recovery avoids trusting stale state.
    query = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        "@(Get-CimInstance Win32_Process -Filter 'ProcessId = 7376').Count"],
        capture_output=True, text=True, check=True)
    assert query.stdout.strip() == '0'
    q = w.read_json(ROOT / w.QUEUE)
    prepared = w.read_json(ROOT / PREP / 'preparation-result.json')
    assert w.digest(ROOT / w.QUEUE) == prepared['queue_sha256']
    w.validate(q, ROOT)
    task, role = o.select(q)
    assert (task['id'], task['status'], role) == ('IG-2B08', 'review', 'reviewer')
    preflight = ROOT / PREP / 'dispatch-preflight'
    packet = w.read_json(preflight / 'packet.json')
    o.verify_artifacts(ROOT, {'artifacts': packet['control_files']})
    checks = w.read_json(ROOT / PREP / 'check-result.json')
    assert checks['exit_code'] == 0 and checks['real_validation_helper_exit'] == 0
    assert all(checks['checks'][k] == 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'))
    preserved = w.read_json(ROOT / PREP / 'preserve-manifest.json')
    o.verify_artifacts(ROOT, preserved)
    interrupted_pins = []
    for path in sorted(old_session.rglob('*')):
        if path.is_file():
            rel = path.relative_to(ROOT).as_posix()
            w.safe_path(ROOT, rel)
            interrupted_pins.append({'path': rel, 'sha256': w.digest(path), 'bytes': path.stat().st_size})
    write('old-lock.json', old_lock)
    write('assessment.json', {'utc': o.utc(), 'task': task['id'],
        'summary': 'Supervisor vanished during preparation before a model process was launched. External interruption cause is unknown; no traceback or final status exists.',
        'old_supervisor_pid': 7376, 'observed_matching_processes': 0,
        'old_lock_sha256': lock_hash, 'interrupted_dispatch_files': interrupted_pins,
        'preserved_artifacts_verified': len(preserved['artifacts']),
        'queue_unchanged': True, 'full_checks_reused': checks,
        'changed_condition': 'Explicit recovery of proven dead pre-model dispatch; fresh source/context controls and prior passing checks remain byte-valid.',
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Coordinating configuration unavailable; new reviewer startup must be observed.',
        'semantic_acceptance': False})
    assert w.digest(lock) == lock_hash
    lock.unlink()
    installed = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    rg = installed['ripgrep']
    assert w.digest(Path(rg['path'])) == rg['sha256']
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    result = o.start_background(ROOT, installed['codex'], 48, 3600, 28800)
    write('start-result.json', result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
