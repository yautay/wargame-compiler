"""Validate the bounded current repair and start its fresh ephemeral executor."""
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B08/manifest-recovery-20261017-F01-01/'


def write(name, value):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    task, role = o.select(q)
    prepared = w.read_json(ROOT / PREP / 'preparation-result.json')
    if (task['id'], task['status'], role) != ('IG-2B08', 'changes_requested', 'executor'):
        raise ValueError('Expected the current authorized F01 repair executor')
    if prepared['queue_sha256'] != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed after preparation')
    if (ROOT / prepared['fresh_attempt']).exists():
        raise ValueError('Fresh repair root already exists; reconcile ownership')
    installed = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    rg = installed['ripgrep']
    if not Path(installed['codex']).is_file() or w.digest(Path(rg['path'])) != rg['sha256']:
        raise ValueError('Installed runtime binding changed')
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    preflight = ROOT / PREP / 'dispatch-preflight'
    preflight.mkdir(exist_ok=False)
    packet = o.prepare(ROOT, q, task, role, preflight)
    o.launch_environment(ROOT, task, preflight, installed['codex'])
    view = w.read_json(preflight / 'dependency-view.json')
    toolchain = view['dependencies']['IG-2B07']['inventory']['reports']['toolchain.json']
    effective = dict(task, context=task['context'] + [toolchain['path']])
    env = o.validation_environment(ROOT, effective, rg)
    print('Fresh repair packet, current F01 binding, source scope and runtime verified.', flush=True)
    check_log = ROOT / PREP / 'full-check.log'
    code = o.run_check(['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B08'],
                       ROOT, check_log, time.monotonic() + 1200, env)
    text = check_log.read_text(encoding='utf-8-sig')
    log_root = Path(next(line.partition('=')[2] for line in text.splitlines() if line.startswith('LOG_ROOT=')))
    if not log_root.resolve().is_relative_to(ROOT):
        raise ValueError('Unexpected check root')
    checks = w.read_json(log_root / 'result.json')
    write('check-result.json', {'exit_code': code, 'checks': checks,
                               'logs': log_root.relative_to(ROOT).as_posix()})
    if code or any(checks[k] != 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit')):
        raise ValueError('Required checks failed; no model launched')
    if prepared['queue_sha256'] != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed during checks')
    preserved = w.read_json(ROOT / PREP / 'preserve-manifest.json')
    o.verify_artifacts(ROOT, preserved)
    write('launch-authorization.json', {
        'utc': o.utc(), 'task': task['id'], 'role': role, 'operator_authorized': True,
        'fresh_attempt': prepared['fresh_attempt'], 'queue_sha256': prepared['queue_sha256'],
        'packet_text_bytes': packet['text_bytes'], 'preserved_artifact_count': len(preserved['artifacts']),
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Coordinating metadata unavailable; fresh child must confirm observed gpt-6.1-sol/high.',
        'checks': checks, 'logs': log_root.relative_to(ROOT).as_posix(),
        'semantic_acceptance_granted': False})
    launch = o.start_background(ROOT, installed['codex'], 48, 3600, 28800)
    write('start-result.json', launch)
    print(json.dumps(launch, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
