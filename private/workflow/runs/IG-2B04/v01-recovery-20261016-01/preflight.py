"""Verify bootstrap reads and the unchanged PATH-dependent test in the real host."""
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
    t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
    assert t['status'] == 'changes_requested'
    assert not (ROOT / t['repair_authorization']['attempt']).exists()
    session = launch / 'preflight'; session.mkdir(exist_ok=False)
    o.prepare(ROOT, q, t, 'executor', session)
    env = o.launch_environment(ROOT, t, session, sys.argv[1])
    report['rg'] = w.read_json(session / 'tool-runtime.json')['ripgrep']
    report['resolved_rg'] = shutil.which('rg', path=env['PATH'])
    assert Path(report['resolved_rg']).resolve() == Path(report['rg']['path']).resolve()
    report['bootstrap_reads'] = []
    for file in ('docs/STATUS.md', 'docs/HANDOFF.md'):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/task_access.py'),
            'read', '--file', file, '--lines', '80'], cwd=ROOT, env=env,
            capture_output=True, timeout=12)
        assert result.returncode == 0, result.stderr.decode('ascii', errors='replace')
        value = json.loads(result.stdout.decode('ascii'))
        assert value['basis'] == 'dispatch_snapshot' and value['status_authority'] is False
        report['bootstrap_reads'].append({'path': file, 'basis': value['basis'], 'exit_code': 0})
    assert not (session / 'context-denied.json').exists()
    command = [sys.executable, '-m', 'pytest', '-q',
        'tests/test_workflow.py::test_default_ripgrep_excludes_history',
        '--basetemp', str(launch / 'pytest'), '-p', 'no:cacheprovider', '--tb=short']
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=30)
    (session / 'unchanged-test.stdout.log').write_bytes(result.stdout)
    (session / 'unchanged-test.stderr.log').write_bytes(result.stderr)
    assert result.returncode == 0, result.stdout.decode('utf-8', errors='replace')[-1200:]
    assert w.digest(ROOT / w.QUEUE) == before
    report.update(result='passed', unchanged_raw_rg_test_exit=0, queue_unchanged=True,
                  inherited_path_preserved=True, both_pythonpath_entries=len(env['PYTHONPATH'].split(o.os.pathsep)) == 2)
except Exception as exc:
    report.update(result='failed', error=str(exc))
finally:
    report['ended_utc'] = o.utc()
    o.dump(launch / 'preflight-result.json', report)
print(json.dumps(report))
raise SystemExit(0 if report['result'] == 'passed' else 2)
