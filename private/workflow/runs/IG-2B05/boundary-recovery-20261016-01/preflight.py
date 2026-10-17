"""Verify the accepted B04 product and B05 dispatch without altering either task."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

launch = Path(sys.argv[2])
report = {'model': None, 'reasoning': None, 'models_launched': 0, 'started_utc': o.utc()}
try:
    q = w.read_json(ROOT / w.QUEUE)
    before = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B05')
    dep = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
    assert task['status'] == 'planned' and dep['status'] == 'done'
    done = dep['events'][-1]
    assert done['sha256'] == 'a6c41a92fcff58d4eeb1ccb31bcbda915575e8e5a39372cfe0861482ab00250e'
    assert w.digest(ROOT / done['evidence']) == done['sha256']
    frozen = w.read_json(ROOT / done['evidence'])
    o.verify_artifacts(ROOT, frozen)
    review = 'private/workflow/runs/IG-2B04/review-4fab98d5-01/review.json'
    assert w.digest(ROOT / review) == 'cd7bdda9e0040e0264b4cbf21cefacafaf16c630104aeb249ac7cd2344c9a2fc'
    original = ROOT / 'private/workflow/runs/IG-2B04/continuation-13-16-rg04/delivery-manifest.json'
    assert w.digest(original) == 'ba026675123a5e9f3b397ebc41b8840dcdc349d04391037a4d74ec5abd6463fc'
    baseline = w.read_json(original)
    assert frozen['artifacts'][:len(baseline['artifacts'])] == baseline['artifacts']
    report['b04_preservation'] = {'status': 'done', 'done': done,
        'accepted_artifacts_verified': len(frozen['artifacts']),
        'original_delivery_prefix_preserved': len(baseline['artifacts']), 'review_sha256': w.digest(ROOT / review)}
    session = launch / 'preflight'
    session.mkdir(exist_ok=False)
    o.prepare(ROOT, q, task, 'coordinator', session)
    env = o.launch_environment(ROOT, task, session, sys.argv[1])
    report['rg'] = w.read_json(session / 'tool-runtime.json')['ripgrep']
    assert Path(shutil.which('rg', path=env['PATH'])).resolve() == Path(report['rg']['path']).resolve()
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/dependency_context.py'),
        '--dependency', 'IG-2B04', '--section', 'boundary'], cwd=ROOT, env=env,
        capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr.decode('ascii', errors='replace')
    boundary = json.loads(result.stdout.decode('ascii'))['data']
    assert boundary['physical_page'] == 16 and boundary['observation']
    report['boundary'] = {'physical_page': boundary['physical_page'], 'observation_present': True}
    view = w.read_json(session / 'dependency-view.json')['dependencies']['IG-2B04']
    assert view['inventory']['assigned_physical_pages'] == [17, 18, 19, 20]
    report['assigned_physical_pages'] = [17, 18, 19, 20]
    report['bootstrap_reads'] = []
    for file in ('README.md', 'docs/work/WORKFLOW.md', 'docs/STATUS.md', 'docs/HANDOFF.md'):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/task_access.py'),
            'read', '--file', file, '--lines', '80'], cwd=ROOT, env=env, capture_output=True, timeout=12)
        assert result.returncode == 0, result.stderr.decode('ascii', errors='replace')
        value = json.loads(result.stdout.decode('ascii'))
        if file in ('docs/STATUS.md', 'docs/HANDOFF.md'):
            assert value['basis'] == 'dispatch_snapshot' and value['status_authority'] is False
        report['bootstrap_reads'].append({'path': file, 'basis': value.get('basis', 'pinned_stable_text')})
    assert not (session / 'context-denied.json').exists()
    assert w.digest(ROOT / w.QUEUE) == before
    report.update(result='passed', queue_unchanged=True)
except Exception as exc:
    report.update(result='failed', error=str(exc))
finally:
    report['ended_utc'] = o.utc()
    o.dump(launch / 'preflight-result.json', report)
print(json.dumps({k: v for k, v in report.items() if k != 'b04_preservation'}))
raise SystemExit(0 if report['result'] == 'passed' else 2)
