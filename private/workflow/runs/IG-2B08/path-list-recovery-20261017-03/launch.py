"""Start the current B08 coordinator after validating native PATH-list support."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import dependency_context as d
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B08/path-list-recovery-20261017-03/'


def write(name, body):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, indent=2)
        f.write('\n')


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    task, role = o.select(q)
    if task['id'] != 'IG-2B08' or role != 'coordinator' or task['status'] != 'planned':
        raise ValueError('B08 coordinator is no longer the expected next role')
    preflight = w.read_json(ROOT / PREP / 'preflight-result.json')
    if preflight['queue_sha256'] != w.digest(ROOT / w.QUEUE):
        raise ValueError('Queue changed since verified coordinator preparation')
    o.verify_artifacts(ROOT, preflight)
    d.checked(ROOT, preflight['accepted_toolchain'])
    checks = w.read_json(ROOT / PREP / 'full-check-result.json')
    if any(checks['checks'][k] != 0 for k in ('plan_exit', 'tests_exit', 'diff_exit')):
        raise ValueError('Queue, full tests or diff check did not pass')
    if checks['checks']['dry_run_exit'] != 1 or checks['dry_run_diagnostic'] != 'ERROR: Task is not ready or active':
        raise ValueError('Unexpected executable packet failure; do not launch')
    if (ROOT / 'private/workflow/ig2-orchestrator.lock').exists() or (ROOT / 'private/workflow/queue.lock').exists():
        raise ValueError('An existing owner requires triage')
    previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    rg = previous['ripgrep']
    if w.digest(Path(rg['path'])) != rg['sha256'] or not Path(previous['codex']).is_file():
        raise ValueError('Installed runtime binding changed')
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    write('launch-authorization.json', {
        'utc': datetime.now(timezone.utc).isoformat(),
        'operator_request_verbatim': 'Dokończ naprawę obsługi process_path_prefix i wznów orkiestrator od IG-2B08.',
        'task': task['id'], 'role': role,
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Exact coordinating session metadata unavailable. The next CLI session must confirm observed gpt-6.1-sol/high before any claim.',
        'preflight': {'path': PREP + 'preflight-result.json', 'sha256': w.digest(ROOT / PREP / 'preflight-result.json')},
        'full_tests_and_diff': checks,
        'state_dependent_dry_run': 'The unchanged executable packet dry-run requires ready/active state. B08 remains planned. Its actual coordinator prepare/launch_environment and all required native tools passed separate preflight. This launch authorizes refinement only; product delivery still requires the full unchanged checks after readiness.',
        'accepted_toolchain_preserved': True,
        'no_source_semantic_acceptance_granted': True})
    launch = o.start_background(ROOT, previous['codex'], 48, 3600, 28800)
    write('start-result.json', launch)
    print(json.dumps(launch, indent=2), flush=True)


if __name__ == '__main__':
    main()
