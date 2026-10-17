"""Exact final-repair delivery and all preserved-version maps."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
BASE = ROOT / 'private/workflow/runs/IG-1D'
DELIVERY = BASE / 'repair-02-20261013/delivery.json'
PACKET = ROOT / 'private/workflow/packets/IG-1D-09669c33c89d4eaabbbe9de266ca3bad'
OLD = BASE / 'replacement-rereview-20261013T140127Z'
def read(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(a):
    p = ROOT / a.get('verified_path', a['path'])
    assert p.resolve().is_relative_to(ROOT)
    actual = sha(p)
    assert actual == a['sha256'], (a, actual)
    return {**a, 'actual_sha256': actual, 'verified_path': p.relative_to(ROOT).as_posix()}
phase = sys.argv[1]
assert sha(DELIVERY) == 'ea2d2cacf42939e516dfc8b65f6c0cffc2d2267478819233fb1f573fddd4275c'
d = read(DELIVERY)
assert len(d['artifacts']) == len({a['path'] for a in d['artifacts']}) == 51
current = [verify(a) for a in d['artifacts']]
qpath = ROOT / 'docs/work/queue.json'
q = read(qpath); task = next(t for t in q['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'review'
assert task['events'][-1]['evidence'] == DELIVERY.relative_to(ROOT).as_posix()
assert task['events'][-1]['sha256'] == sha(DELIVERY)
assert d['criteria'] == task['acceptance']
pres = read(DELIVERY.parent / 'preservation.json')
groups = {k: [verify(a) for a in v] for k, v in pres.items() if isinstance(v, list)}
assert {k:len(v) for k,v in groups.items()} == {'parent_delivery_versions':50,'checkpoint_versions':119,'independent_review_versions':54,'foundation_versions':182}
assert sha(OLD / 'review.json') == 'bd053c6d858dfbb2656a5e10b9ea395d14aee6f2e04f56f4f1d0176746accfba'
assert sha(OLD / 'review-manifest.json') == '1004a11d1faaab6ed4bce69a64bbbb33031d9eb1240608e659a1e059dc181448'
assert sha(OLD / 'final-seal.json') == '394a0ce45682ed1dac40f60b92a22a89ed1a66fe8a62f593c8829745db60247b'
old_manifest = [verify(a) for a in read(OLD / 'review-manifest.json')['artifacts']]
parent_original = [verify(a) for a in read(BASE / 'repair-01-20261013/preservation.json')['parent_artifact_versions']]
prior = BASE / 'review-20261013T122807Z/review.json'
assert sha(prior) == 'ef9955c57e22a85ecd76a54ea08fda9dcfedbba7419cfc85ff91497abf468b00'
prior_artifacts = [verify(a) for a in read(prior)['artifacts']]
prior_manifest = [verify(a) for a in read(prior.with_name('review-manifest.json'))['artifacts']]
old_unfinalized = [verify(a) for a in read(OLD / 'prior-rereview-baseline.json')['artifacts']]
packet = read(PACKET / 'manifest.json')
assert packet['queue_sha256'] == sha(qpath)
assert packet['context_sha256'] == sha(PACKET / 'context.txt')
packet_files = [verify(a) for a in packet['files']]
input_pins = []
for s in task['inputs']:
    m = re.fullmatch(r'(.+) SHA-256 ([0-9a-f]{64})', s)
    if m: input_pins.append(verify({'path': m[1], 'sha256': m[2]}))
assert len(input_pins) == 9
oracle_pres = read(DELIVERY.parent / 'oracle-preservation.json')
verify(oracle_pres['original_oracle']); verify(oracle_pres['current_oracle'])
raw = (ROOT / oracle_pres['current_oracle']['path']).read_bytes()
assert raw.replace(b'ig1-continuation-executor-20261013', b'ig1d-replacement-reviewer-20261013T140127Z').replace(b'executor_actor', b'review_actor') == (OLD / 'accounting.py').read_bytes()
# A fresh two-transform audit must target the exact package included in repair 2.
package = ROOT / 'private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc'
for name in ['source-ig.json', 'identity-registry.json', 'references.json', 'manifest.json']:
    a = next(a for a in d['artifacts'] if a['path'] == (package / name).relative_to(ROOT).as_posix())
    verify(a)
report = {'phase': phase, 'utc': datetime.now(timezone.utc).isoformat(), 'all_match': True,
    'reviewed_delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'sha256': sha(DELIVERY), 'artifact_count':51,'artifacts':current},
    'queue_sha256':sha(qpath),'queue_states':{t['id']:t['status'] for t in q['tasks'] if t['id'].startswith('IG-1')},
    'preservation':groups,'prior_final_review_manifest':old_manifest, 'prior_original_parent_versions':parent_original,
    'original_review_artifacts':prior_artifacts,'original_review_manifest':prior_manifest,'prior_unfinalized_rereview':old_unfinalized,
    'packet':{'path':(PACKET / 'manifest.json').relative_to(ROOT).as_posix(),'sha256':sha(PACKET / 'manifest.json'),'files':packet_files},
    'input_pins':input_pins, 'executor_oracle_assertions_unchanged':True,'canonical_target_bound_to_current_delivery':True}
with (RUN / ('verification-' + phase + '.json')).open('x',encoding='utf-8') as f:
    json.dump(report,f,indent=2);f.write('\n')
print(json.dumps({'phase':phase,'current':51,'groups':{k:len(v) for k,v in groups.items()},'all_match':True,'queue_sha256':sha(qpath)}))
