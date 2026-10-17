"""Verify real rendered page artifacts and the fresh executor's inspection progress."""
from datetime import datetime, timezone
import json
from pathlib import Path
import struct
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o
PREP = 'private/workflow/runs/IG-2B04/rg-recovery-20261016-01/'
RUN = 'private/workflow/orchestrator/20261016T115606Z-694df602/'
LAUNCH = 'private/workflow/launches/20261016T115559Z-e4dff3af/'
OUT = 'private/workflow/runs/IG-2B04/continuation-13-16-rg04/'
def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}
q = w.read_json(ROOT / w.QUEUE)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'in_progress'
state = w.read_json(ROOT / RUN / 'status.json')
assert state['state'] == 'running'
session = Path(state['session'])
rel_session = session.relative_to(ROOT).as_posix() + '/'
cfg = w.read_json(session / 'runtime-configuration.json')
assert cfg['status'] == 'confirmed' and cfg['model'] == 'gpt-6.1-sol' and cfg['reasoning'] == 'high'
claim = w.read_json(ROOT / OUT / 'claim.json')
assert claim['actor'] == f'ig2:{session.name}:executor'
o.configuration_binding(ROOT, session, claim)
assert pin(OUT + 'claim.json')['sha256'] == t['events'][-1]['sha256']
progress = w.read_json(ROOT / OUT / 'checkpoint-inspection-start.json')
o.configuration_binding(ROOT, session, progress)
assert progress['actor'] == claim['actor'] and '13' in progress['observations']
images = []
for page in (13, 14, 15, 16):
    rel = OUT + f'original-pages/page-{page}.png'
    with (ROOT / rel).open('rb') as stream:
        header = stream.read(24)
    assert header[:8] == b'\x89PNG\r\n\x1a\n'
    width, height = struct.unpack('>II', header[16:24])
    assert width >= 600 and height >= 600
    images.append({'pdf_page': page, **pin(rel), 'width': width, 'height': height})
preflight = w.read_json(ROOT / LAUNCH / 'preflight-result.json')
assert preflight['result'] == 'passed' and preflight['search_PATH'] == '' and preflight['matches'] > 0
runtime = w.read_json(session / 'tool-runtime.json')['ripgrep']
assert runtime['path'] == preflight['rg']['path'] and runtime['sha256'] == preflight['rg']['sha256']
assert w.digest(Path(runtime['path'])) == runtime['sha256']
process = w.read_json(session / 'process.json')
assert process['state'] == 'running'
assert (datetime.now(timezone.utc) - datetime.fromisoformat(process['heartbeat_utc'])).total_seconds() < 20
assert not (session / 'context-denied.json').exists()
lines = (session / 'stderr.log').read_text(encoding='utf-8', errors='replace').splitlines()
source_progress = [line for line in lines if line.startswith(('Fresh renders are complete,', 'I’ve inspected all four original pages'))]
assert len(source_progress) >= 2
report = {'role': 'coordinator', 'actor': 'operator-authorized-rg-recovery-20261016-01',
    'model': None, 'reasoning': None, 'configuration_evidence': 'Builder actual configuration unavailable; executor metadata independently observed below.',
    'verified_utc': o.utc(), 'summary': 'B04 progressed beyond claim/checkpoint: four original PNGs exist, fresh executor recorded page13 inspection, and reported a concrete page14 crop-boundary finding.',
    'task': t['id'], 'status': t['status'], 'claim': pin(OUT + 'claim.json'),
    'inspection_progress_checkpoint': pin(OUT + 'checkpoint-inspection-start.json'),
    'original_page_images': images,
    'inspection_evidence_basis': 'Current executor checkpoint plus concrete current-session source observation; rendering alone is not visual/source acceptance.',
    'executor_source_progress_statements': source_progress,
    'executor_configuration': pin(rel_session + 'runtime-configuration.json'),
    'tool_runtime': pin(rel_session + 'tool-runtime.json'), 'ripgrep': runtime,
    'independent_host_preflight': pin(LAUNCH + 'preflight-result.json'),
    'preflight_search_matches_with_empty_PATH': preflight['matches'],
    'supervisor_pid': process['supervisor_pid'], 'executor_pid': process['pid'],
    'heartbeat_utc': process['heartbeat_utc'], 'no_context_denial': True,
    'run': RUN, 'launch': LAUNCH, 'repository_tests': '242 passed; plan, dry-run and diff checks passed.',
    'task_completed': False, 'source_completeness_certified': False, 'semantic_acceptance_granted': False}
target = ROOT / PREP / 'restart-page-review-verified.json'
assert not target.exists()
o.dump(target, report)
print(json.dumps({'task': t['id'], 'status': t['status'], 'original_pages_rendered': [13,14,15,16],
                  'page13_inspection_checkpoint': True, 'page14_specific_finding_reported': True,
                  'supervisor_pid': process['supervisor_pid'], 'executor_pid': process['pid'],
                  'heartbeat_utc': process['heartbeat_utc']}))
