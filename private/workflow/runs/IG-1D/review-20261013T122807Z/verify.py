import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
DELIVERY = ROOT / 'private/workflow/runs/IG-1D/preflight-20261013/delivery.json'
PACKET = ROOT / 'private/workflow/packets/IG-1D-e2dc4314bbd94e2f86db733486d95700'
CONFIG = ROOT / 'private/workflow/runs/IG-1C/review-20261013T071955Z/configuration-confirmed.json'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def verify(a):
    p = Path(a.get('verified_path', a['path']))
    if not p.is_absolute():
        p = ROOT / p
    assert p.resolve().is_relative_to(ROOT)
    actual = sha(p)
    assert actual == a['sha256'], (a, actual)
    return {**a, 'verified_path': p.relative_to(ROOT).as_posix(), 'actual_sha256': actual}

phase = sys.argv[1]
assert sha(DELIVERY) == 'f510ae8830d5a5cbf1311c8383a4a8e0581d3e5421e64283b4d4820cae8f4154'
delivery = read(DELIVERY)
assert len(delivery['artifacts']) == len({a['path'] for a in delivery['artifacts']}) == 69
artifacts = [verify(a) for a in delivery['artifacts']]
queue = read(ROOT / 'docs/work/queue.json')
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'review'
assert next(t for t in queue['tasks'] if t['id'] == 'IG-1E')['status'] == 'planned'
packet = read(PACKET / 'manifest.json')
assert packet['queue_sha256'] == sha(ROOT / 'docs/work/queue.json')
assert packet['context_sha256'] == sha(PACKET / 'context.txt')
packet_files = [verify(a) for a in packet['files']]
assert all((ROOT / a['path']).stat().st_size == a['bytes'] for a in packet['files'])
input_pins = []
for item in task['inputs']:
    m = re.fullmatch(r'(.+) SHA-256 ([0-9a-f]{64})', item)
    if m:
        input_pins.append(verify({'path': m[1], 'sha256': m[2]}))
assert len(input_pins) == 9
base = read(ROOT / 'contracts/ig/source.schema.json')
profile = read(ROOT / 'src/wgc/export/source-export.schema.json')
expected = copy.deepcopy(base)
expected['$id'] = 'urn:wgc:ig:source-export:1'
expected['title'] = 'WGC deterministic source export profile 1'
changes = []
def transform(value, path=''):
    if isinstance(value, dict):
        for key, child in list(value.items()):
            pointer = path + '/' + key
            if key == 'schema_version' and child == {'const': 'wgc-source-1'}:
                value[key] = {'const': 'wgc-source-export-1'}
                changes.append(pointer)
            elif key in {'started_utc', 'ended_utc'}:
                value[key] = {'type': 'null'}
                changes.append(pointer)
            else:
                transform(child, pointer)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            transform(child, path + '/' + str(i))
transform(expected)
assert expected == profile
assert len([p for p in changes if p.endswith('/schema_version')]) == 14
assert len([p for p in changes if p.endswith('/started_utc') or p.endswith('/ended_utc')]) == 2
approval = read(DELIVERY.parent / 'operator-profile-approval.json')
assert approval['human_semantic_acceptance_granted'] is False
assert sha(Path(approval['approved_proposal']['path'])) == approval['approved_proposal']['sha256'] == sha(ROOT / 'src/wgc/export/source-export.schema.json')
assert sha(Path(approval['approved_patch']['path'])) == approval['approved_patch']['sha256']
foundation = read(DELIVERY.parent / 'foundation-preservation.json')
preserved = [verify(a) for a in foundation['artifacts']]
assert len(preserved) == 182
config = read(CONFIG)
assert config['model'] == 'gpt-6.1-sol' and config['reasoning'] == 'high'
report = {'phase': phase, 'utc': datetime.now(timezone.utc).isoformat(), 'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'sha256': sha(DELIVERY)}, 'artifact_count': 69, 'artifacts': artifacts,
    'packet': {'path': (PACKET / 'manifest.json').relative_to(ROOT).as_posix(), 'sha256': sha(PACKET / 'manifest.json'), 'context_sha256': packet['context_sha256'], 'files': packet_files},
    'input_pins': input_pins, 'approved_profile_delta': {'exact_expected_delta': True, 'root_id_title_changes': 2, 'schema_version_changes': 14, 'canonical_clock_changes': 2, 'changed_paths': changes, 'all_other_contract_bytes_semantically_unchanged': True},
    'operator_profile_approval': {'path': (DELIVERY.parent / 'operator-profile-approval.json').relative_to(ROOT).as_posix(), 'sha256': sha(DELIVERY.parent / 'operator-profile-approval.json')},
    'foundation_artifacts': preserved, 'all_match': True,
    'reviewer_configuration': {'model': config['model'], 'reasoning': config['reasoning'], 'source': config['configuration_evidence'], 'original_confirmation': {'path': CONFIG.relative_to(ROOT).as_posix(), 'sha256': sha(CONFIG)}, 'same_chat_continuity': True}}
with (RUN / ('verification-' + phase + '.json')).open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
if phase == 'before':
    with (RUN / 'checkpoint-initial.json').open('x', encoding='utf-8') as stream:
        json.dump({'task': 'IG-1D', 'role': 'reviewer', 'actor': 'ig1c-reviewer-20261013T071955Z', 'started_utc': '2026-10-13T12:28:07Z', 'model': config['model'], 'reasoning': config['reasoning'], 'configuration_evidence': report['reviewer_configuration'], 'input_packet': report['packet'], 'frozen_delivery': report['delivery'], 'completed': ['queue/configuration/69 delivery hashes/182 foundation hashes/profile exact delta verified'], 'next_operation': 'Read complete named source contracts and delivered identity/reference/export code, then independently probe and inventory.'}, stream, indent=2)
        stream.write('\n')
print(json.dumps({'phase': phase, 'delivery_artifacts': 69, 'foundation_artifacts': 182, 'approved_profile_delta_exact': True, 'all_match': True}))
