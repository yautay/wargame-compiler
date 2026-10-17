import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
DELIVERY = ROOT / 'private/workflow/runs/IG-1C/stage-20261013/delivery.json'
PIN = '8e3fc23cf3d64783b10c2f48287196b807272c2f5b356bcaabf35e695dbd9017'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

delivery_hash = digest(DELIVERY)
assert delivery_hash == PIN, (delivery_hash, PIN)
delivery = json.loads(DELIVERY.read_text(encoding='utf-8'))
assert len(delivery['artifacts']) == 34
results = []
for artifact in delivery['artifacts']:
    path = ROOT / artifact['path']
    assert path.resolve().is_relative_to(ROOT)
    actual = digest(path)
    results.append({**artifact, 'actual_sha256': actual, 'matches': actual == artifact['sha256']})
report = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'sha256': delivery_hash},
    'artifact_count': len(results),
    'all_match': all(item['matches'] for item in results),
    'artifacts': results,
}
output = RUN / ('delivery-verification-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'report': str(output), 'artifact_count': len(results), 'all_match': report['all_match']}))
assert report['all_match'], 'Frozen artifact mismatch; stop review'
