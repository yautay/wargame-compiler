"""Supplement checkpoint verification with each protected artifact's actual bytes."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

out = Path(__file__).resolve().parent
root = Path(__file__).resolve().parents[5]
groups = [
    ('foundation', 'private/workflow/runs/IG-1D/preflight-20261013/foundation-preservation.json'),
    ('original_review', 'private/workflow/runs/IG-1D/review-20261013T122807Z/review.json'),
]
verified = []
counts = {}
for group, path in groups:
    document = json.loads((root / path).read_text(encoding='utf-8-sig'))
    entries = document['artifacts']
    for entry in entries:
        actual = hashlib.sha256((root / entry['path']).read_bytes()).hexdigest()
        assert actual == entry['sha256'], entry['path']
        verified.append(dict(entry, group=group))
    counts[group] = len(entries)
assert counts == {'foundation': 182, 'original_review': 42}, counts
with (out / 'protected-artifacts-verification.json').open('x', encoding='utf-8', newline='\n') as stream:
    json.dump({'verified_utc': datetime.now(timezone.utc).isoformat(), 'result': 'pass',
               'counts': counts, 'artifacts': verified,
               'note': 'Supplement to checkpoint.json: capture.py verified the 69 parent versions and 50 current artifacts; this independently rehashes each of the 224 protected foundation/review artifacts.'}, stream, indent=2)
    stream.write('\n')
print(json.dumps({'result': 'pass', 'counts': counts}))
