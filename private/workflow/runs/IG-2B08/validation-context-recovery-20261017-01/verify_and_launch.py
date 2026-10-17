"""Check the private-output review binding and launch a fresh independent reviewer."""
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B08/validation-context-recovery-20261017-01/'


def write(name, body):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(body, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    task, role = o.select(q)
    prepared = w.read_json(ROOT / PREP / 'preparation-result.json')
    if (task['id'], task['status'], role) != ('IG-2B08', 'review', 'reviewer'):
        raise ValueError('Expected fresh independent review of F01 delivery')
    if prepared['queue_sha256'] != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed after review preparation')
    installed = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    rg = installed['ripgrep']
    if not Path(installed['codex']).is_file() or w.digest(Path(rg['path'])) != rg['sha256']:
        raise ValueError('Installed runtime binding changed')
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    preflight = ROOT / PREP / 'dispatch-preflight'
    preflight.mkdir(exist_ok=False)
    packet = o.prepare(ROOT, q, task, role, preflight)
    session_env = o.launch_environment(ROOT, task, preflight, installed['codex'])
    access = w.read_json(preflight / 'access-manifest.json')
    paths = [p['path'] for p in access['source_validation']['inputs']]
    expected = [task['inventory_contract']['attempt_root'] + '/' + name + '/inventory.json'
                for name in ('final-verified', 'replay-1', 'replay-2')]
    if paths != expected:
        raise ValueError('Validation scope is not exactly the current final and two replays')
    print('Fresh review packet and exact three-inventory validation scope verified.', flush=True)
    # Exercise the real unchanged full validator through the new capture boundary.
    # This coordinator check grants no independent review result or acceptance.
    smoke = ROOT / PREP / 'validation-helper-summary.log'
    code = o.run_check([sys.executable, 'scripts/task_access.py', 'validate-source', '--file', paths[0]],
                       ROOT, smoke, time.monotonic() + 300, session_env)
    summary = w.read_json(smoke)
    if code or summary['exit_code'] or set(summary) != {
            'task', 'inventory', 'command', 'exit_code', 'stdout', 'stderr', 'output_policy'}:
        raise ValueError('Validation helper integration did not pass with summary-only output')
    print('Real source validator passed; raw output remains in private logs.', flush=True)
    view = w.read_json(preflight / 'dependency-view.json')
    tool = view['dependencies']['IG-2B07']['inventory']['reports']['toolchain.json']
    env = o.validation_environment(ROOT, dict(task, context=task['context'] + [tool['path']]), rg)
    check_log = ROOT / PREP / 'full-check.log'
    code = o.run_check(['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', task['id']],
                       ROOT, check_log, time.monotonic() + 1200, env)
    lines = check_log.read_text(encoding='utf-8-sig').splitlines()
    log_root = Path(next(line.partition('=')[2] for line in lines if line.startswith('LOG_ROOT=')))
    if not log_root.resolve().is_relative_to(ROOT):
        raise ValueError('Unexpected check directory')
    checks = w.read_json(log_root / 'result.json')
    write('check-result.json', {'exit_code': code, 'checks': checks,
                               'logs': log_root.relative_to(ROOT).as_posix(),
                               'real_validation_helper_exit': summary['exit_code']})
    if code or any(checks[k] != 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit')):
        raise ValueError('Required checks failed; no reviewer launched')
    preserved = w.read_json(ROOT / PREP / 'preserve-manifest.json')
    o.verify_artifacts(ROOT, preserved)
    if prepared['queue_sha256'] != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed during checks')
    write('launch-authorization.json', {
        'utc': o.utc(), 'task': task['id'], 'role': role, 'operator_authorized': True,
        'queue_sha256': prepared['queue_sha256'], 'packet_text_bytes': packet['text_bytes'],
        'preserved_artifact_count': len(preserved['artifacts']), 'checks': checks,
        'logs': log_root.relative_to(ROOT).as_posix(), 'validation_inputs': paths,
        'validation_output_policy': 'Exit/command/log pins only; raw stdout/stderr private.',
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Coordinating metadata unavailable; new reviewer must confirm observed gpt-6.1-sol/high startup.',
        'semantic_acceptance_granted': False})
    launch = o.start_background(ROOT, installed['codex'], 48, 3600, 28800)
    write('start-result.json', launch)
    print(json.dumps(launch, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
