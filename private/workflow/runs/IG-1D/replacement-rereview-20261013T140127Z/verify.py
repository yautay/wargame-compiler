"""Exact current and preserved-version verification; no inherited configuration."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
BASE = ROOT / 'private/workflow/runs/IG-1D'
PACKET = ROOT / 'private/workflow/packets/IG-1D-b4e7e41d1a1740d49d34cc2793d9132f'

def read(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(a):
    p = ROOT / a.get('verified_path', a['path'])
    assert p.resolve().is_relative_to(ROOT)
    actual = sha(p)
    assert actual == a['sha256'], (a, actual)
    return {**a, 'verified_path': p.relative_to(ROOT).as_posix(), 'actual_sha256': actual}

phase = sys.argv[1]
queue_path = ROOT / 'docs/work/queue.json'
queue = read(queue_path)
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'review'
delivery_path = BASE / 'repair-01-20261013/delivery.json'
assert sha(delivery_path) == '3ebef08719717c41043cb4df8bb98874d214e38d0e8fdbf21de6e35a9adfaa73'
delivery = read(delivery_path)
assert len(delivery['artifacts']) == len({a['path'] for a in delivery['artifacts']}) == 50
current = [verify(a) for a in delivery['artifacts']]
checkpoint_manifest = BASE / 'operator-checkpoint-20261013T132827Z/verified-artifact-manifest.json'
preserved = [verify(a) for a in read(checkpoint_manifest)]
assert len(preserved) == 119
preservation = read(BASE / 'repair-01-20261013/preservation.json')
parent = [verify(a) for a in preservation['parent_artifact_versions']]
assert len(parent) == 69 and preservation['all_parent_69_versions_preserved']
foundation = [verify(a) for a in read(BASE / 'preflight-20261013/foundation-preservation.json')['artifacts']]
prior = BASE / 'review-20261013T122807Z/review.json'
assert sha(prior) == 'ef9955c57e22a85ecd76a54ea08fda9dcfedbba7419cfc85ff91497abf468b00'
assert len(read(prior)['findings']) == 4
prior_artifacts = [verify(a) for a in read(prior)['artifacts']]
prior_manifest = [verify(a) for a in read(prior.with_name('review-manifest.json'))['artifacts']]
old = [verify(a) for a in read(RUN / 'prior-rereview-baseline.json')['artifacts']]
assert not read(RUN / 'prior-rereview-baseline.json')['final_review_exists']
assert sha(BASE / 'rereview-20261013T131151Z/dispositions.json') == '0741368107d61f95d9658431322920ff15968c0c3dab2c6e54e225594c80bf60'
packet = read(PACKET / 'manifest.json')
assert packet['queue_sha256'] == sha(queue_path) == '07cb9707259e91d1f779360ba4eb8606a3d2ae51502aaba53c4961a7e264e1e3'
assert packet['context_sha256'] == sha(PACKET / 'context.txt')
packet_files = [verify(a) for a in packet['files']]
inputs = []
for entry in task['inputs']:
    match = re.fullmatch(r'(.+) SHA-256 ([0-9a-f]{64})', entry)
    if match: inputs.append(verify({'path': match[1], 'sha256': match[2]}))
assert len(inputs) == 9
report = {'phase': phase, 'utc': datetime.now(timezone.utc).isoformat(), 'all_match': True,
    'queue_sha256': sha(queue_path), 'queue_states': {t['id']: t['status'] for t in queue['tasks'] if t['id'].startswith('IG-1')},
    'reviewed_delivery': {'path': delivery_path.relative_to(ROOT).as_posix(), 'sha256': sha(delivery_path), 'artifacts': current},
    'checkpoint_manifest': {'path': checkpoint_manifest.relative_to(ROOT).as_posix(), 'sha256': sha(checkpoint_manifest), 'artifacts': preserved},
    'parent_versions': parent, 'foundation_artifacts': foundation, 'prior_review_artifacts': prior_artifacts,
    'prior_manifest_artifacts': prior_manifest, 'prior_rereview_artifacts': old,
    'input_pins': inputs, 'packet': {'path': (PACKET / 'manifest.json').relative_to(ROOT).as_posix(), 'sha256': sha(PACKET / 'manifest.json'), 'files': packet_files}}
with (RUN / ('verification-' + phase + '.json')).open('x', encoding='utf-8') as f:
    json.dump(report, f, indent=2); f.write('\n')
print(json.dumps({'phase': phase, 'current': len(current), 'checkpoint': len(preserved), 'parent': len(parent), 'foundation': len(foundation), 'prior': len(prior_artifacts), 'prior_manifest': len(prior_manifest), 'old_rereview': len(old), 'all_match': True}))
