"""Check the precise-context B08 packet and launch a fresh bounded CLI session."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import dependency_context as d
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B08/context-recovery-20261017-p33-01/'


def write(name, value):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    task, role = o.select(q)
    if task['id'] != 'IG-2B08' or task['status'] != 'ready' or role != 'executor':
        raise ValueError('Expected the fresh ready B08 executor')
    preparation = w.read_json(ROOT / PREP / 'preparation-result.json')
    if preparation['queue_sha256'] != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed after scope preparation')
    if (ROOT / preparation['fresh_attempt']).exists():
        raise ValueError('New attempt already exists; reconcile ownership')
    preserved = w.read_json(ROOT / PREP / 'preserve-manifest.json')
    o.verify_artifacts(ROOT, preserved)
    previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    rg = previous['ripgrep']
    if not Path(previous['codex']).is_file() or w.digest(Path(rg['path'])) != rg['sha256']:
        raise ValueError('Installed CLI/ripgrep binding changed')
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    session = ROOT / PREP / 'dispatch-preflight'
    session.mkdir(exist_ok=False)
    packet = o.prepare(ROOT, q, task, role, session)
    o.launch_environment(ROOT, task, session, previous['codex'])
    view = w.read_json(session / 'dependency-view.json')
    tool_pin = view['dependencies']['IG-2B07']['inventory']['reports']['toolchain.json']
    d.checked(ROOT, tool_pin)
    env = o.validation_environment(ROOT, dict(task, context=task['context'] + [tool_pin['path']]), rg)
    print('Precise context scope, frozen prior attempt and fresh executor packet verified.', flush=True)
    check_log = ROOT / PREP / 'full-check.log'
    code = o.run_check(['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', task['id']],
                       ROOT, check_log, time.monotonic() + 1200, env)
    log_text = check_log.read_text(encoding='utf-8-sig')
    log_root = Path(next(line.partition('=')[2] for line in log_text.splitlines() if line.startswith('LOG_ROOT=')))
    if not log_root.resolve().is_relative_to(ROOT):
        raise ValueError('Unexpected validation log root')
    checks = w.read_json(log_root / 'result.json')
    write('check-result.json', {'exit_code': code, 'checks': checks, 'logs': log_root.relative_to(ROOT).as_posix()})
    if code or any(checks[k] != 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit')):
        raise ValueError('Required checks failed; no model launched')
    o.verify_artifacts(ROOT, preserved)
    if preparation['queue_sha256'] != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed during validation')
    write('launch-authorization.json', {
        'utc': datetime.now(timezone.utc).isoformat(), 'operator_requested_recovery': True,
        'task': task['id'], 'role': role, 'fresh_attempt': preparation['fresh_attempt'],
        'queue_sha256': w.digest(ROOT / w.QUEUE), 'packet_text_bytes': packet['text_bytes'],
        'prior_attempt_artifacts_verified': len(preserved['artifacts']),
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Current coordinating configuration unavailable; the new child must confirm observed gpt-6.1-sol/high startup metadata.',
        'context_scope': {'physical_page': 33, 'box_points': [45, 50, 306, 80],
                          'box_normalized': [73529, 63131, 500000, 101011]},
        'checks': checks, 'logs': log_root.relative_to(ROOT).as_posix(),
        'no_prior_inspection_or_acceptance_inherited': True})
    launch = o.start_background(ROOT, previous['codex'], 48, 3600, 28800)
    write('start-result.json', launch)
    o.verify_artifacts(ROOT, preserved)
    print(json.dumps(launch, indent=2), flush=True)


if __name__ == '__main__':
    main()
