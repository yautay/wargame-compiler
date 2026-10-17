"""Coordinator verification of exact independent PASS and every IG-1D gate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time

ROOT = Path.cwd(); RUN = Path(__file__).resolve().parent
REVIEW = Path('private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z')
DELIVERY = Path('private/workflow/runs/IG-1D/repair-02-20261013/delivery.json')
started = datetime.now(timezone.utc); tick = time.perf_counter()
def read(p): return json.loads(Path(p).read_bytes())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def art(p): return {'path': Path(p).as_posix(), 'sha256': sha(p)}
def write(n, v):
    with (RUN/n).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(v, f, indent=2); f.write('\n')
assert sha(DELIVERY) == 'ea2d2cacf42939e516dfc8b65f6c0cffc2d2267478819233fb1f573fddd4275c'
assert sha(REVIEW/'review-manifest.json') == 'ada8130957d2b336225acfa386878b6f327a27be37a47556b58ce28cfed55a60'
assert sha(REVIEW/'acceptance-evidence.json') == '34488bbf3187ff7e34626c092d7fb33d1a712eca48a7f1b8e68f223dfcb20b00'
manifest = read(REVIEW/'review-manifest.json')
for a in manifest['artifacts']: assert sha(a['path']) == a['sha256'], a['path']
report = read(REVIEW/'review.json'); acceptance = read(REVIEW/'acceptance-evidence.json'); delivery = read(DELIVERY)
assert report['technical_result'] == 'pass' and report['technical_pass'] and report['independent_pass']
assert {d['finding_id']: d['disposition'] for d in report['dispositions']} == {f'IG1D-R0{i}': 'closed' for i in range(1,5)}
assert all(r['result'] == 'pass' for r in report['criteria_results'])
assert acceptance['artifacts'] == delivery['artifacts']
assert acceptance['actor'] != delivery['actor']
assert all(c['exit_code'] == 0 for c in acceptance['checks'])
for a in delivery['artifacts']: assert sha(a['path']) == a['sha256'], a['path']
preservation = read('private/workflow/runs/IG-1D/repair-02-20261013/preservation.json')
for key in ['parent_delivery_versions', 'checkpoint_versions', 'independent_review_versions', 'foundation_versions']:
    for a in preservation[key]: assert sha(a['verified_path']) == a['sha256'], a['path']
q = read('docs/work/queue.json'); task = next(t for t in q['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'review' and not task['semantic_acceptance_required']
assert acceptance['criteria'] == task['acceptance']
write('verification.json', {'task': 'IG-1D', 'technical_gates': 'passed',
    'delivery': art(DELIVERY), 'independent_review': art(REVIEW/'review.json'),
    'review_manifest': art(REVIEW/'review-manifest.json'), 'acceptance_evidence': art(REVIEW/'acceptance-evidence.json'),
    'all_51_delivery_hashes_verified': True, 'every_original_finding_closed': True,
    'every_acceptance_criterion_passed': True, 'all_prior_versions_verified': True,
    'started_utc': started.isoformat(), 'ended_utc': datetime.now(timezone.utc).isoformat(),
    'wall_seconds': time.perf_counter()-tick, 'tokens': None, 'cost': None, 'operator_time_seconds': None,
    'semantic_acceptance_granted': False, 'publisher_source_coverage_granted': False, 'executable_readiness_granted': False})
write('done.json', {'role': 'coordinator', 'actor': 'ig1-continuation-executor-20261013',
    'summary': 'All IG-1D technical gates independently passed and all four findings closed on the exact 51-artifact repair-2 delivery. Coordinator verifies every criterion/hash and retained foundations; no semantic, publisher-coverage or executable acceptance.',
    'criteria': task['acceptance'], 'artifacts': delivery['artifacts'], 'checks': acceptance['checks'],
    'model': 'gpt-6.1-sol', 'reasoning': 'high',
    'configuration_evidence': delivery['configuration_evidence'], 'independent_review': art(REVIEW/'review.json'),
    'independent_review_manifest': art(REVIEW/'review-manifest.json'),
    'coordinator_verification': art(Path('private/workflow/runs/IG-1D/completion-20261013/verification.json')),
    'semantic_acceptance_granted': False, 'publisher_source_coverage_granted': False, 'executable_readiness_granted': False})
print('Every technical criterion, finding, exact artifact and preserved foundation verified. Acceptance/done evidence ready.')
