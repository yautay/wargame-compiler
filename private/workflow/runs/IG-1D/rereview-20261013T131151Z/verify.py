from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
DELIVERY = ROOT / 'private/workflow/runs/IG-1D/repair-01-20261013/delivery.json'
PACKET = ROOT / 'private/workflow/packets/IG-1D-404435e2638b4a369400e9b6a283b961'
PARENT = ROOT / 'private/workflow/runs/IG-1D/preflight-20261013/delivery.json'
PRIOR = ROOT / 'private/workflow/runs/IG-1D/review-20261013T122807Z/review.json'
CONFIG = ROOT / 'private/workflow/runs/IG-1C/review-20261013T071955Z/configuration-confirmed.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def verify(artifact, path=None):
    path = Path(path or artifact.get('verified_path', artifact['path']))
    if not path.is_absolute():
        path = ROOT / path
    assert path.resolve().is_relative_to(ROOT)
    actual = sha(path)
    assert actual == artifact['sha256'], (artifact, path, actual)
    return {**artifact, 'verified_path': path.relative_to(ROOT).as_posix(), 'actual_sha256': actual}

phase = sys.argv[1]
queue = read(ROOT / 'docs/work/queue.json')
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'review'
pin = next(e['sha256'] for e in reversed(task['events']) if e['evidence'] == DELIVERY.relative_to(ROOT).as_posix())
assert pin == sha(DELIVERY) == '3ebef08719717c41043cb4df8bb98874d214e38d0e8fdbf21de6e35a9adfaa73'
current = read(DELIVERY)
assert len(current['artifacts']) == len({a['path'] for a in current['artifacts']}) == 50
artifacts = [verify(a) for a in current['artifacts']]
assert sha(PARENT) == 'f510ae8830d5a5cbf1311c8383a4a8e0581d3e5421e64283b4d4820cae8f4154'
assert sha(PRIOR) == 'ef9955c57e22a85ecd76a54ea08fda9dcfedbba7419cfc85ff91497abf468b00'
baseline = read(DELIVERY.parent / 'baseline-manifest.json')
mapping = {a['original']['path']: a['preserved_copy'] for a in baseline['files']}
assert len(mapping) == 6
parent_versions = []
for a in read(PARENT)['artifacts']:
    if a['path'] in mapping:
        assert mapping[a['path']]['sha256'] == a['sha256']
    parent_versions.append(verify(a, mapping.get(a['path'], a)['path']))
prior_artifacts = [verify(a) for a in read(PRIOR)['artifacts']]
prior_manifest = [verify(a) for a in read(PRIOR.with_name('review-manifest.json'))['artifacts']]
foundation = [verify(a) for a in read(PARENT.parent / 'foundation-preservation.json')['artifacts']]
assert len(parent_versions) == 69 and len(prior_artifacts) == 42 and len(prior_manifest) == 43 and len(foundation) == 182
packet = read(PACKET / 'manifest.json')
assert packet['queue_sha256'] == sha(ROOT / 'docs/work/queue.json')
assert packet['context_sha256'] == sha(PACKET / 'context.txt')
packet_files = [verify(a) for a in packet['files']]
assert all((ROOT / a['path']).stat().st_size == a['bytes'] for a in packet['files'])
old_context = ROOT / 'private/workflow/packets/IG-1D-e2dc4314bbd94e2f86db733486d95700/context.txt'
assert (PACKET / 'context.txt').read_bytes() == old_context.read_bytes()
inputs = []
for item in task['inputs']:
    match = re.fullmatch(r'(.+) SHA-256 ([0-9a-f]{64})', item)
    if match:
        inputs.append(verify({'path': match[1], 'sha256': match[2]}))
assert len(inputs) == 9
assert sha(ROOT / 'src/wgc/export/source-export.schema.json') == '2a1f619eb4773d1432470cf0a340ac55c2f74451661c92002a6c89a7864bd768'
approved_delta = read(PRIOR.parent / 'verification-before.json')['approved_profile_delta']
config = read(CONFIG)
assert config['model'] == 'gpt-6.1-sol' and config['reasoning'] == 'high'
report = {'phase': phase, 'utc': datetime.now(timezone.utc).isoformat(),
    'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'sha256': pin}, 'artifact_count': 50, 'artifacts': artifacts,
    'parent_delivery': {'path': PARENT.relative_to(ROOT).as_posix(), 'sha256': sha(PARENT)}, 'parent_review': {'path': PRIOR.relative_to(ROOT).as_posix(), 'sha256': sha(PRIOR)},
    'parent_versions': parent_versions, 'baseline_mapping': baseline['files'], 'prior_review_artifacts': prior_artifacts, 'prior_manifest_artifacts': prior_manifest, 'foundation_artifacts': foundation,
    'packet': {'path': (PACKET / 'manifest.json').relative_to(ROOT).as_posix(), 'sha256': sha(PACKET / 'manifest.json'), 'context_sha256': packet['context_sha256'], 'files': packet_files, 'context_identical_to_previously_read_packet': True},
    'input_pins': inputs, 'approved_profile_delta': approved_delta, 'all_match': True,
    'configuration': {'model': config['model'], 'reasoning': config['reasoning'], 'source': config['configuration_evidence'], 'same_chat_continuity': True, 'original_confirmation': {'path': CONFIG.relative_to(ROOT).as_posix(), 'sha256': sha(CONFIG)}}}
with (RUN / ('verification-' + phase + '.json')).open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'phase': phase, 'delivery_artifacts': 50, 'parent_versions': 69, 'prior_review_artifacts': 42, 'prior_manifest_artifacts': 43, 'foundation_artifacts': 182, 'all_match': True}))
