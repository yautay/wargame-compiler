"""Revalidate the unchanged passing review, close B06 and restart bounded IG-2."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B06/status-write-recovery-20261016-01/'
OLD_SESSION = 'private/workflow/orchestrator/20261016T182116Z-202cea4c/002-IG-2B06-reviewer-089ffca5'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(name, body):
    p = ROOT / PREP / name
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, indent=2)
        f.write('\n')


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B06')
    if task['status'] != 'review':
        raise ValueError('Expected unchanged B06 review; reconcile current ownership')
    if (ROOT / 'private/workflow/ig2-orchestrator.lock').exists() or (ROOT / 'private/workflow/queue.lock').exists():
        raise ValueError('An existing owner requires triage')
    triage = w.read_json(ROOT / PREP / 'process-triage.json')
    when = datetime.fromisoformat(triage['observed_utc'].replace('Z', '+00:00'))
    if triage['processes'] or (datetime.now(timezone.utc) - when).total_seconds() > 600:
        raise ValueError('Refresh absence of prior supervisor/reviewer before recovery')
    session = ROOT / OLD_SESSION
    result = w.read_json(session / 'response.json')
    if result['outcome'] != 'pass':
        raise ValueError('Only the existing passing independent review may be reused')
    review = w.read_json(w.safe_path(ROOT, result['evidence']))
    o.configuration_binding(ROOT, session, review)
    event, delivery = o.latest_delivery(ROOT, task)
    if review['artifacts'] != delivery['artifacts'] or review['criteria'] != task['acceptance']:
        raise ValueError('Independent review no longer binds the complete delivery/criteria')
    if any(p['path'] in {'scripts/orchestrate_ig2.py', 'tests/test_orchestrator.py', 'docs/work/IG2-ORCHESTRATOR.md'} for p in delivery['artifacts']):
        raise ValueError('Tooling repair touches the frozen product; obtain new review')
    preserved = [pin(p.relative_to(ROOT).as_posix()) for p in sorted(session.rglob('*')) if p.is_file()]
    preserved += [pin(result['evidence']), pin(event['evidence'])]
    write('authorization.json', {
        'utc': datetime.now(timezone.utc).isoformat(),
        'operator_request_verbatim': 'napraw i uruchom',
        'task': task['id'], 'role': 'coordinator',
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Coordinating model/reasoning not exposed. Deterministic supervisor recovery reuses the verified observed independent-review configuration without impersonating that reviewer.',
        'cause': 'Windows access/sharing denial while atomically replacing the supervisor heartbeat file caused one synthetic guard test to fail. The independent frozen source review passed.',
        'change': 'At most two retries of the same complete pending file for Windows errors 5/32/33, preserving atomic replacement and persistent-error failure. Initial process metadata now includes its heartbeat, avoiding an immediate redundant rewrite.',
        'validation_recovery': 'Original passing review and source/product bytes remain frozen. Run unchanged supervisor checks in a new directory, then use existing accepted/done gates. No model rerun or source-semantic acceptance is inferred.',
        'targeted_tests': {'command': '.venv/Scripts/python.exe -m pytest -q tests/test_orchestrator.py -k "atomic_status or validation_recovery" --basetemp private/workflow/checks/b06-atomic-status-tests01 -p no:cacheprovider --tb=short', 'exit_code': 0, 'result': '7 passed, including real Windows sharing-handle recovery'},
        'preserved_artifacts': preserved,
        'tooling_artifacts': [pin(p) for p in ('scripts/orchestrate_ig2.py', 'tests/test_orchestrator.py', 'docs/work/IG2-ORCHESTRATOR.md')],
        'human_semantic_acceptance': False})
    previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    rg = previous['ripgrep']
    if w.digest(Path(rg['path'])) != rg['sha256'] or not Path(previous['codex']).is_file():
        raise ValueError('Installed runtime binding changed')
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    print('Running unchanged supervisor validation for the existing frozen passing review.', flush=True)
    validation = ROOT / PREP / 'validation-atomic-status01'
    o.finish_review(ROOT, task, result, session, deadline=time.monotonic() + 3600,
                    validation_session=validation)
    o.verify_artifacts(ROOT, {'artifacts': preserved})
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    current = next(t for t in q['tasks'] if t['id'] == 'IG-2B06')
    if current['status'] != 'done':
        raise ValueError('B06 closure did not complete')
    next_task, role = o.select(q)
    if next_task['id'] != 'IG-2B07' or role != 'coordinator':
        raise ValueError('Unexpected next owner; preserve closure and triage')
    preflight = ROOT / PREP / 'b07-preflight'
    preflight.mkdir(exist_ok=False)
    o.prepare(ROOT, q, next_task, role, preflight)
    o.launch_environment(ROOT, next_task, preflight, previous['codex'])
    write('closure-verification.json', {'task': 'IG-2B06', 'status': 'done',
        'next_task': next_task['id'], 'next_role': role, 'old_review_session_unchanged': True,
        'checks': w.read_json(validation / 'supervisor-checks.json'),
        'queue_sha256': w.digest(ROOT / w.QUEUE)})
    launch = o.start_background(ROOT, previous['codex'], 48, 3600, 28800)
    write('start-result.json', launch)
    print(json.dumps(launch, indent=2), flush=True)


if __name__ == '__main__':
    main()
