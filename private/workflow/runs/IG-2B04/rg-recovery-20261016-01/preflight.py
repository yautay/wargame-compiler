"""Run the formerly failing helper inside the independent host before any model."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w
launch = Path(sys.argv[2])
report = {'model': None, 'reasoning': None, 'models_launched': 0, 'started_utc': o.utc()}
try:
    q = w.read_json(ROOT / w.QUEUE)
    before = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
    assert task['status'] == 'ready'
    assert not (ROOT / task['continuation_authorization']['attempt']).exists()
    session = launch / 'preflight'
    session.mkdir(exist_ok=False)
    o.prepare(ROOT, q, task, 'executor', session)
    env = o.launch_environment(ROOT, task, session, sys.argv[1])
    report['rg'] = w.read_json(session / 'tool-runtime.json')['ripgrep']
    report['ambient_rg'] = shutil.which('rg', path=env.get('PATH', ''))
    search_env = dict(env, PATH='', PYTHONIOENCODING='cp1252:strict', PYTHONUTF8='0')
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/search_task.py'), '--pattern',
        '^def |links|evidence', '--file', 'src/wgc/sources/inventory.py'],
        cwd=ROOT, env=search_env, capture_output=True, timeout=12)
    (session / 'search.stdout.json').write_bytes(result.stdout)
    (session / 'search.stderr.log').write_bytes(result.stderr)
    assert result.returncode == 0, result.stderr.decode('ascii', errors='replace')
    matches = json.loads(result.stdout.decode('ascii'))['matches']
    assert matches and not (session / 'context-denied.json').exists()
    report.update(search_exit=0, matches=len(matches), search_PATH='', unicode_pipe='cp1252:strict',
                  guard_active=True, no_denial=True)
    tools = subprocess.run([sys.executable, '-c',
        'import pypdf,pdfplumber,PIL,reportlab;import shutil,subprocess;'
        'assert shutil.which("pdfinfo") and shutil.which("pdftoppm");'
        'subprocess.run(["git","--version"],check=True);'
        'subprocess.run(["pdfinfo","-v"],check=True)'],
        cwd=ROOT, env=env, capture_output=True, timeout=10)
    (session / 'toolchain.stdout.log').write_bytes(tools.stdout)
    (session / 'toolchain.stderr.log').write_bytes(tools.stderr)
    assert tools.returncode == 0, tools.stderr.decode('utf-8', errors='replace')[-800:]
    assert w.digest(ROOT / w.QUEUE) == before
    report.update(result='passed', native_dependencies_exit=0, queue_unchanged=True)
except Exception as exc:
    report.update(result='failed', error=str(exc))
finally:
    report['ended_utc'] = o.utc()
    o.dump(launch / 'preflight-result.json', report)
print(json.dumps(report))
raise SystemExit(0 if report['result'] == 'passed' else 2)
