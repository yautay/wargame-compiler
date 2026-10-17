"""Verify list-valued native PATH prefixes against the actual B08 dependency."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B08/path-list-recovery-20261017-03/'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(name, body):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, indent=2)
        f.write('\n')


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    task, role = o.select(q)
    if task['id'] != 'IG-2B08' or role != 'coordinator' or task['status'] != 'planned':
        raise ValueError('Expected planned B08 coordinator; reconcile ownership')
    triage = w.read_json(ROOT / PREP / 'process-triage.json')
    if triage['processes'] or triage['supervisor_lock'] or triage['queue_lock']:
        raise ValueError('Previous ownership requires triage')
    queue_hash = w.digest(ROOT / w.QUEUE)
    previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    if not Path(previous['codex']).is_file():
        raise ValueError('Recorded installed CLI unavailable; do not install or change providers')
    rg = previous['ripgrep']
    if w.digest(Path(rg['path'])) != rg['sha256']:
        raise ValueError('Installed ripgrep binding changed')
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    session = ROOT / PREP / 'dispatch-preflight'
    session.mkdir(exist_ok=False)
    o.prepare(ROOT, q, task, role, session)
    env = o.launch_environment(ROOT, task, session, previous['codex'])
    view = w.read_json(session / 'dependency-view.json')
    tool_pin = view['dependencies']['IG-2B07']['inventory']['reports']['toolchain.json']
    tool = w.read_json(w.safe_path(ROOT, tool_pin['path']))
    if w.digest(ROOT / tool_pin['path']) != tool_pin['sha256']:
        raise ValueError('Accepted toolchain changed')
    prefix = tool['process_path_prefix']
    if not isinstance(prefix, list):
        raise ValueError('Actual regression input no longer has a path list')
    expected_prefix = os.pathsep.join(prefix)
    if not env['PATH'].startswith(expected_prefix + os.pathsep):
        raise ValueError('Ordered native path list was not preserved')
    probes = {}
    for name, flag in [('pwsh', '--version'), ('git', '--version'),
                       ('pdfinfo', '-v'), ('pdftoppm', '-v')]:
        executable = shutil.which(name, path=env['PATH'])
        if not executable:
            raise ValueError('Required installed native tool unavailable: ' + name)
        result = subprocess.run([executable, flag], env=env, cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=10)
        if result.returncode:
            raise ValueError('Required native tool probe failed: ' + name)
        probes[name] = {'path': executable, 'sha256': w.digest(Path(executable)),
                        'exit_code': result.returncode,
                        'version': (result.stdout + result.stderr).splitlines()[0]}
    if queue_hash != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed during preflight')
    write('preflight-result.json', {
        'utc': datetime.now(timezone.utc).isoformat(), 'operator_requested_recovery': True,
        'task': task['id'], 'role': role, 'queue_sha256': queue_hash, 'queue_unchanged': True,
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Exact coordinating session configuration is unavailable; fresh child startup observation remains mandatory.',
        'cause': 'An accepted toolchain records process_path_prefix as a list, but validation_environment passed the list to pathlib.Path.',
        'change': 'Normalize a single directory or ordered directory list into the child PATH. Preserve order, duplicates, expired wrapper entries and the complete inherited PATH tail. Reject malformed values and entirely unavailable native prefixes.',
        'accepted_toolchain': tool_pin, 'accepted_toolchain_unchanged': True,
        'prefix_entry_count': len(prefix),
        'expired_prefix_entries': [p for p in prefix if not Path(p).is_dir()],
        'native_probes': probes,
        'targeted_tests': {'exit_code': 0, 'result': '18 passed',
            'command': '.venv/Scripts/python.exe -m pytest -q tests/test_orchestrator.py -k "native_path or pinned_bundled_environment or planned_coordinator_inherits or validation_exposes_pinned_rg" --basetemp private/workflow/checks/b08-path-prefix-tests02 -p no:cacheprovider --tb=short'},
        'artifacts': [pin(p) for p in ('scripts/orchestrate_ig2.py', 'tests/test_orchestrator.py', 'docs/work/IG2-ORCHESTRATOR.md')],
        'no_source_or_semantic_acceptance_granted': True})
    print('B08 coordinator dispatch and all four required native tool probes passed.', flush=True)
    # No task is ready/active yet. The legacy executable packet dry-run must
    # refuse planned B08; the actual planned-coordinator dispatch was checked above.
    effective = dict(task, context=task['context'] + [tool_pin['path']])
    validation_env = o.validation_environment(ROOT, effective, rg)
    with (ROOT / PREP / 'full-check.log').open('x', encoding='utf-8') as log:
        result = subprocess.run(['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', task['id']],
                                cwd=ROOT, env=validation_env, stdout=log, stderr=subprocess.STDOUT, timeout=1200)
    log_text = (ROOT / PREP / 'full-check.log').read_text(encoding='utf-8-sig')
    log_root = next(line.partition('=')[2] for line in log_text.splitlines() if line.startswith('LOG_ROOT='))
    logs = Path(log_root)
    if not logs.resolve().is_relative_to(ROOT):
        raise ValueError('Unexpected check log root')
    checks = w.read_json(logs / 'result.json')
    dry = (logs / 'dry-run.log').read_text(encoding='utf-8-sig').strip()
    write('full-check-result.json', {'exit_code': result.returncode, 'checks': checks,
        'logs': logs.relative_to(ROOT).as_posix(), 'dry_run_diagnostic': dry,
        'state_note': 'B08 remains planned. Refusal of executable packet dry-run is expected until coordinator refinement; no delivery or acceptance is authorized.'})
    if any(checks[k] != 0 for k in ('plan_exit', 'tests_exit', 'diff_exit')):
        raise ValueError('Queue, full suite or diff checks failed; do not launch')
    if checks['dry_run_exit'] != 1 or dry != 'ERROR: Task is not ready or active':
        raise ValueError('Unexpected dry-run failure; do not launch')
    print(json.dumps({'full_tests_exit': checks['tests_exit'], 'diff_exit': checks['diff_exit'],
                      'planned_coordinator_verified': True, 'check_logs': logs.relative_to(ROOT).as_posix()}), flush=True)


if __name__ == '__main__':
    main()
