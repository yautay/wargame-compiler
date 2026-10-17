import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
PACKET = ROOT / 'private/workflow/packets/IG-1C-1092608e68ff4dfeb1400b841a891d2d'
CURRENT = ROOT / 'private/workflow/runs/IG-1C/resume-20261013/delivery.json'
ORIGINAL = ROOT / 'private/workflow/runs/IG-1C/stage-20261013/delivery.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

phase = sys.argv[1]
queue = read(ROOT / 'docs/work/queue.json')
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1C')
assert task['status'] == 'review'
pin = next(e['sha256'] for e in reversed(task['events']) if e['evidence'] == CURRENT.relative_to(ROOT).as_posix())
assert sha(CURRENT) == pin
assert sha(ORIGINAL) == '8e3fc23cf3d64783b10c2f48287196b807272c2f5b356bcaabf35e695dbd9017'
current, original = read(CURRENT), read(ORIGINAL)
assert len(original['artifacts']) == 34
assert len({a['path'] for a in current['artifacts']}) == len(current['artifacts'])
assert all(a in current['artifacts'] for a in original['artifacts'])
results = []
for a in current['artifacts']:
    p = ROOT / a['path']
    assert p.resolve().is_relative_to(ROOT)
    actual = sha(p)
    results.append({**a, 'actual_sha256': actual, 'matches': actual == a['sha256']})
assert all(a['matches'] for a in results)
packet = read(PACKET / 'manifest.json')
assert sha(ROOT / 'docs/work/queue.json') == packet['queue_sha256']
assert sha(PACKET / 'context.txt') == packet['context_sha256']
packet_checks = []
for a in packet['files']:
    p = ROOT / a['path']
    assert sha(p) == a['sha256'] and p.stat().st_size == a['bytes']
    packet_checks.append(a)
foundation = read(ROOT / 'private/workflow/runs/IG-1C/stage-20261013/foundation-audit.json')
external = []
for a in foundation['external_scope']:
    p = Path(a['path'])
    assert sha(p) == a['sha256'] and p.stat().st_size == a['bytes']
    external.append(a)
dependency = read(ROOT / 'private/workflow/runs/IG-1C/stage-20261013/dependency.json')
metadata = ROOT / 'private/workflow/runs/IG-1C/stage-20261013/dependencies/pypi-6.0.3.json'
wheel = ROOT / 'private/workflow/runs/IG-1C/stage-20261013/dependencies/pyyaml-6.0.3-cp312-cp312-win_amd64.whl'
assert sha(metadata) == dependency['metadata_sha256']
assert sha(wheel) == dependency['wheel_sha256']
official = read(metadata)
assert official['info']['version'] == '6.0.3'
assert any(a['digests']['sha256'] == sha(wheel) and a['url'] == dependency['wheel_url'] for a in official['urls'])
wheel_checks = []
with zipfile.ZipFile(wheel) as z:
    for name in z.namelist():
        if name.endswith('/') or name.endswith('/RECORD'):
            continue
        installed = ROOT / '.venv/Lib/site-packages' / name
        expected = hashlib.sha256(z.read(name)).hexdigest()
        assert sha(installed) == expected
        wheel_checks.append({'path': str(installed), 'sha256': expected})
report = {
    'phase': phase, 'utc': datetime.now(timezone.utc).isoformat(),
    'task_state': task['status'], 'delivery': {'path': CURRENT.relative_to(ROOT).as_posix(), 'sha256': pin},
    'parent_delivery': {'path': ORIGINAL.relative_to(ROOT).as_posix(), 'sha256': sha(ORIGINAL)},
    'all_match': True, 'artifact_count': len(results), 'artifacts': results,
    'packet': {'path': (PACKET / 'manifest.json').relative_to(ROOT).as_posix(), 'sha256': sha(PACKET / 'manifest.json'), 'files': packet_checks},
    'external_support': external, 'installed_wheel_files': wheel_checks,
    'dependency_note': 'Official saved metadata pins wheel hash/url. Installed source, extension and metadata bytes equal wheel; pip-mutated RECORD excluded. No network or dependency changes.'
}
target = RUN / ('verification-' + phase + '.json')
with target.open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'phase': phase, 'current_delivery_sha256': pin, 'artifacts': len(results), 'installed_wheel_files': len(wheel_checks), 'all_match': True}))
