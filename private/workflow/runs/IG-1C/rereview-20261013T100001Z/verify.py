import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CURRENT = ROOT / 'private/workflow/runs/IG-1C/repair-01-20261013/delivery.json'
PARENT = ROOT / 'private/workflow/runs/IG-1C/resume-20261013/delivery.json'
PRIOR_REVIEW = ROOT / 'private/workflow/runs/IG-1C/review-20261013T092949Z/review.json'
PACKET = ROOT / 'private/workflow/packets/IG-1C-e53938d9f57544e8a8bd52c12430be50'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def check(a, actual_path=None):
    actual_path = actual_path or a['path']
    p = ROOT / actual_path
    assert p.resolve().is_relative_to(ROOT)
    actual = sha(p)
    assert actual == a['sha256'], (a, actual_path, actual)
    return {**a, 'verified_path': actual_path, 'actual_sha256': actual}

phase = sys.argv[1]
queue = read(ROOT / 'docs/work/queue.json')
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1C')
assert task['status'] == 'review'
pin = next(e['sha256'] for e in reversed(task['events']) if e['evidence'] == CURRENT.relative_to(ROOT).as_posix())
assert sha(CURRENT) == pin
current = read(CURRENT)
assert len({a['path'] for a in current['artifacts']}) == len(current['artifacts'])
artifacts = [check(a) for a in current['artifacts']]
assert sha(PARENT) == 'aefeac57292fcb742e8f7263d2ed30af56af01fd1da8282bc7e4baa3c78742b8'
assert sha(PRIOR_REVIEW) == '333ca0ae84342bffc103045c5ad1ea1ee2dbc8f104764d2ce4db2255a8c0f48e'
baseline = read(CURRENT.parent / 'baseline-manifest.json')
mapping = {a['original']['path']: a['preserved_copy'] for a in baseline['files']}
assert len(mapping) == 3
parent_preservation = []
for a in read(PARENT)['artifacts']:
    if a['path'] in mapping:
        copy = mapping[a['path']]
        assert copy['sha256'] == a['sha256']
        parent_preservation.append(check(a, copy['path']))
    else:
        parent_preservation.append(check(a))
assert len(parent_preservation) == 53
prior_artifacts = [check(a) for a in read(PRIOR_REVIEW)['artifacts']]
prior_manifest = ROOT / 'private/workflow/runs/IG-1C/review-20261013T092949Z/review-manifest.json'
prior_manifest_artifacts = [check(a) for a in read(prior_manifest)['artifacts']]
foundation = read(ROOT / 'private/workflow/runs/IG-1C/stage-20261013/foundation-audit.json')
foundation_checks = [check(a, a['verified_path']) for a in foundation['artifacts']]
packet = read(PACKET / 'manifest.json')
assert packet['queue_sha256'] == sha(ROOT / 'docs/work/queue.json')
assert packet['context_sha256'] == sha(PACKET / 'context.txt')
packet_files = [check(a) for a in packet['files']]
for a in packet['files']:
    assert (ROOT / a['path']).stat().st_size == a['bytes']
previous_context = ROOT / 'private/workflow/packets/IG-1C-1092608e68ff4dfeb1400b841a891d2d/context.txt'
assert (PACKET / 'context.txt').read_bytes() == previous_context.read_bytes()
external = []
for a in foundation['external_scope']:
    p = Path(a['path'])
    assert sha(p) == a['sha256'] and p.stat().st_size == a['bytes']
    external.append(a)
tree = ast.parse((ROOT / 'src/wgc/wgu_adapter/importer.py').read_text(encoding='utf-8'))
embedded = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'WGU_SCHEMA' for t in n.targets))
external_schema = read(Path('C:/repo/wargame-utils/wgu/schemas/kb.schema.json'))
assert embedded == external_schema == read(CURRENT.parent / 'pinned-wgu-schema.json')
installed = []
wheel = ROOT / 'private/workflow/runs/IG-1C/stage-20261013/dependencies/pyyaml-6.0.3-cp312-cp312-win_amd64.whl'
assert sha(wheel) == '5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b'
with zipfile.ZipFile(wheel) as z:
    for name in z.namelist():
        if name.endswith('/') or name.endswith('/RECORD'):
            continue
        p = ROOT / '.venv/Lib/site-packages' / name
        expected = hashlib.sha256(z.read(name)).hexdigest()
        assert sha(p) == expected
        installed.append({'path': str(p), 'sha256': expected})
report = {'phase': phase, 'utc': datetime.now(timezone.utc).isoformat(),
    'delivery': {'path': CURRENT.relative_to(ROOT).as_posix(), 'sha256': pin}, 'artifact_count': len(artifacts), 'artifacts': artifacts,
    'parent_delivery': {'path': PARENT.relative_to(ROOT).as_posix(), 'sha256': sha(PARENT)},
    'parent_review': {'path': PRIOR_REVIEW.relative_to(ROOT).as_posix(), 'sha256': sha(PRIOR_REVIEW)},
    'parent_preservation': parent_preservation, 'baseline_mapping': baseline['files'],
    'prior_review_artifacts': prior_artifacts, 'prior_review_manifest_artifacts': prior_manifest_artifacts,
    'foundation': foundation_checks, 'external_support': external, 'installed_wheel_files': installed,
    'embedded_schema_equals_exact_pin': True,
    'packet': {'path': (PACKET / 'manifest.json').relative_to(ROOT).as_posix(), 'sha256': sha(PACKET / 'manifest.json'), 'files': packet_files, 'context_sha256': packet['context_sha256'], 'full_context_byte_identical_to_previously_read_reviewer_packet': True},
    'all_match': True}
with (RUN / ('verification-' + phase + '.json')).open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'phase': phase, 'delivery_sha256': pin, 'artifacts': len(artifacts), 'parent_versions_preserved': len(parent_preservation), 'prior_review_artifacts_preserved': len(prior_artifacts), 'foundation_artifacts_preserved': len(foundation_checks), 'all_match': True}))
