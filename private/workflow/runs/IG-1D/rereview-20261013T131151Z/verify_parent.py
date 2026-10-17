import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
PARENT = ROOT / 'private/workflow/runs/IG-1D/preflight-20261013/delivery.json'
BASELINE = ROOT / 'private/workflow/runs/IG-1D/repair-01-20261013/baseline-manifest.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

assert sha(PARENT) == 'f510ae8830d5a5cbf1311c8383a4a8e0581d3e5421e64283b4d4820cae8f4154'
assert sha(BASELINE) == '2cf8160e578aca5e94f540d942c6254c604fa27980634ced39b9759252bede13'
mapping = {a['original']['path']: a['preserved_copy'] for a in read(BASELINE)['files']}
assert len(mapping) == 6
rows = []
for artifact in read(PARENT)['artifacts']:
    path = mapping.get(artifact['path'], artifact)['path']
    expected = mapping.get(artifact['path'], artifact)['sha256']
    assert expected == artifact['sha256']
    assert sha(ROOT / path) == expected
    rows.append({**artifact, 'verified_path': path, 'actual_sha256': expected})
assert len(rows) == 69
foundation = read(ROOT / 'private/workflow/runs/IG-1D/preflight-20261013/foundation-preservation.json')
protected = []
for a in foundation['artifacts']:
    path = Path(a.get('verified_path', a['path']))
    if not path.is_absolute():
        path = ROOT / path
    assert sha(path) == a['sha256']
    protected.append({**a, 'verified_path': path.relative_to(ROOT).as_posix()})
report = {'utc': datetime.now(timezone.utc).isoformat(), 'parent_artifact_versions': rows,
          'parent_count': len(rows), 'baseline_mapping': read(BASELINE)['files'],
          'protected_foundation_count': len(protected), 'protected_foundation': protected,
          'all_match': True, 'scope': 'Only frozen parent/baseline/foundation versions checked while repaired live product remains unpublished; no substantive repair review.'}
with (RUN / 'parent-preservation-pending.json').open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps({'parent_versions_verified': len(rows), 'protected_foundation_verified': len(protected), 'all_match': True}))
