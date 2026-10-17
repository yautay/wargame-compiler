"""Verify current IG-2B06 dispatch without launching or changing queue state."""
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

prep = Path(__file__).resolve().parent
q = w.read_json(ROOT / w.QUEUE)
w.validate(q, ROOT)
task, role = o.select(q)
if task['id'] != 'IG-2B06' or role != 'coordinator' or task['status'] != 'planned':
    raise ValueError('Queue no longer selects IG-2B06 coordinator; reconcile ownership')
queue_hash = w.digest(ROOT / w.QUEUE)
previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
rg = previous['ripgrep']
if w.digest(Path(rg['path'])) != rg['sha256']:
    raise ValueError('Pinned installed ripgrep changed')
os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'])
session = prep / 'dispatch-preflight'
session.mkdir(exist_ok=False)
packet = o.prepare(ROOT, q, task, role, session)
env = o.launch_environment(ROOT, task, session, previous['codex'])
view = w.read_json(session / 'dependency-view.json')
tool = view['dependencies']['IG-2B05']['toolchain']
if queue_hash != w.digest(ROOT / w.QUEUE):
    raise ValueError('Queue changed during preflight')
result = {
    'format': 'wgc-toolchain-parser-recovery-1', 'utc': datetime.now(timezone.utc).isoformat(),
    'operator_request': 'Fix toolchain.json reading and resume the orchestrator from IG-2B06.',
    'task': task['id'], 'role': role, 'queue_unchanged': True, 'queue_sha256': queue_hash,
    'actual_model': None, 'actual_reasoning': None,
    'configuration_evidence': 'Current coordinating session exact model/reasoning is not exposed; child startup observation remains mandatory.',
    'cause': 'Accepted native tool versions were strings; the projection assumed each entry was an object.',
    'change': 'Normalize string versions to version objects, retain bounded structured executable pins, reject malformed supported records with ValueError.',
    'assigned_physical_pages': view['dependencies']['IG-2B05']['inventory']['assigned_physical_pages'],
    'native_tools': list(tool['native']),
    'runtime_directories_verified': True,
    'checks': [{'command': '.venv/Scripts/python.exe -m pytest -q tests/test_dependency_context.py --basetemp private/workflow/checks/b06-toolchain-fix-targeted01 -p no:cacheprovider --tb=short',
                'exit_code': 0, 'result': '34 passed in 2.83s'},
               {'command': 'orchestrate_ig2.prepare and launch_environment for current IG-2B06 coordinator', 'exit_code': 0}],
    'artifacts': [{'path': rel, 'sha256': w.digest(ROOT / rel)} for rel in (
        'scripts/dependency_context.py', 'tests/test_dependency_context.py',
        'private/workflow/runs/IG-2B05/continuation-17-20-dependency03/toolchain.json')],
    'source_or_semantic_acceptance_granted': False,
    'old_run_preserved': 'private/workflow/orchestrator/20261016T154824Z-fae43db9',
    'next_operation': 'Run unchanged full checks, confirm old process absent, then start a fresh bounded background supervisor from the authoritative queue.'}
with (prep / 'preflight-result.json').open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({k: result[k] for k in ('task', 'role', 'queue_unchanged', 'assigned_physical_pages', 'native_tools')}))
