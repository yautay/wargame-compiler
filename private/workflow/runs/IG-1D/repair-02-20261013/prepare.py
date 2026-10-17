"""Verify and preserve the exact delivery before claiming bounded R04 repair two."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

ROOT = Path.cwd()
RUN = Path(__file__).parent
REVIEW = Path('private/workflow/runs/IG-1D/replacement-rereview-20261013T140127Z')
PARENT = Path('private/workflow/runs/IG-1D/repair-01-20261013/delivery.json')
PACKET = Path('private/workflow/packets/IG-1D-29a30dba3350428bb9ccdaf5e778e1a5/manifest.json')
CONFIG = Path('private/workflow/runs/IG-1D/resume-audit-20261013T134548Z/configuration-confirmed.json')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def art(p):
    p = Path(p)
    return {'path': (p.relative_to(ROOT) if p.is_absolute() else p).as_posix(), 'sha256': sha(p)}
def write(name, data):
    with (RUN/name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2); f.write('\n')

assert sha(REVIEW/'review.json') == 'bd053c6d858dfbb2656a5e10b9ea395d14aee6f2e04f56f4f1d0176746accfba'
assert sha(REVIEW/'review-manifest.json') == '1004a11d1faaab6ed4bce69a64bbbb33031d9eb1240608e659a1e059dc181448'
assert sha(PARENT) == '3ebef08719717c41043cb4df8bb98874d214e38d0e8fdbf21de6e35a9adfaa73'
review, parent = read(REVIEW/'review.json'), read(PARENT)
assert review['review_finalized'] and review['technical_result'] == 'changes_requested'
for a in read(REVIEW/'review-manifest.json')['artifacts'] + parent['artifacts']:
    assert sha(a['path']) == a['sha256'], a['path']
for a in read('private/workflow/runs/IG-1D/operator-checkpoint-20261013T132827Z/verified-artifact-manifest.json'):
    assert sha(a.get('verified_path', a['path'])) == a['sha256'], a['path']
packet = read(PACKET)
assert sha('docs/work/queue.json') == packet['queue_sha256']
for a in packet['files']: assert sha(a['path']) == a['sha256'], a['path']
assert read(CONFIG)['model'] == 'gpt-6.1-sol' and read(CONFIG)['reasoning'] == 'high'
q = read('docs/work/queue.json')
task = next(t for t in q['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'review'
baseline = RUN/'baseline'/'identity.py'
baseline.parent.mkdir()
with baseline.open('xb') as f: f.write(Path('src/wgc/wgu_adapter/identity.py').read_bytes())
write('baseline-manifest.json', {'files': [{'original': art('src/wgc/wgu_adapter/identity.py'), 'preserved_copy': art(baseline)}]})
write('repair-scope.json', {
    'task': 'IG-1D', 'finding': 'IG1D-R04', 'iteration': 2, 'maximum': 2,
    'parent_delivery': art(PARENT), 'independent_review': art(REVIEW/'review.json'),
    'independent_review_manifest': art(REVIEW/'review-manifest.json'),
    'closed_findings_not_reopened': ['IG1D-R01', 'IG1D-R02', 'IG1D-R03'],
    'hypothesis': 'Filtering prior receipt children by kind/scope before testing receipt existence hides an incompatible typed output and treats replay as initial allocation. Validate named output kind/scope/persistent child-key against all persisted receipt children before replacement allocation.',
    'owned_product_paths': ['src/wgc/wgu_adapter/identity.py', 'tests/wgu_adapter/test_lineage_contract_repairs.py'],
    'controls': review['findings'][0]['required_verification'],
    'no_semantic_or_executable_acceptance': True
})
write('checkpoint.json', {
    'task': 'IG-1D', 'attempt': 'repair-02-20261013', 'actor': 'ig1-continuation-executor-20261013',
    'started_utc': datetime.now(timezone.utc).isoformat(), 'model': 'gpt-6.1-sol', 'reasoning': 'high',
    'configuration_evidence': art(CONFIG), 'input_packet': art(PACKET),
    'base_file': art('src/wgc/wgu_adapter/identity.py'), 'queue_before': art('docs/work/queue.json'),
    'tokens': None, 'cost': None, 'operator_time_seconds': None,
    'next_operation': 'Record changes_requested and the bounded second claim, then implement only the R04 typed-child contract guard and new strict synthetic controls.'
})
common = {'actor': 'ig1-continuation-executor-20261013', 'criteria': task['acceptance'],
          'model': 'gpt-6.1-sol', 'reasoning': 'high', 'configuration_evidence': art(CONFIG)}
write('changes-requested.json', {**common, 'role': 'coordinator',
    'summary': 'Record finalized independent replacement review: R01-R03 closed; one bounded second repair remains for R04 typed-child receipt contract.',
    'artifacts': [art(REVIEW/'review.json'), art(REVIEW/'review-manifest.json')],
    'reviewer_checks': review['checks'], 'technical_result': 'changes_requested'})
write('claim.json', {**common, 'role': 'executor',
    'summary': 'Claim second and final bounded R04 repair under the changed filter-before-contract hypothesis; preserve repair-1 and every strict independent assertion.',
    'artifacts': [art(RUN/'checkpoint.json'), art(RUN/'baseline-manifest.json'), art(RUN/'repair-scope.json')]})
print('Verified independent report, all current/prior versions and packet; preserved identity.py; prepared bounded R04 claim.')
