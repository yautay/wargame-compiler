"""Correct unsubmitted claim path spelling; no frozen/event evidence is edited."""
import json, hashlib
from pathlib import Path
root = Path.cwd()
run = Path(__file__).parent
def normalize(value):
    if isinstance(value, list): return [normalize(v) for v in value]
    if isinstance(value, dict):
        value = {k: normalize(v) for k,v in value.items()}
        if 'path' in value and Path(value['path']).is_absolute():
            value['path'] = Path(value['path']).relative_to(root).as_posix()
        if 'path' in value and 'sha256' in value:
            value['sha256'] = hashlib.sha256((root/value['path']).read_bytes()).hexdigest()
    return value
for name in ['baseline-manifest.json', 'repair-scope.json', 'checkpoint.json', 'claim.json']:
    path = run/name
    data = normalize(json.loads(path.read_text(encoding='utf-8')))
    path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8', newline='\n')
with (run/'claim-path-correction.json').open('x', encoding='utf-8') as f:
    json.dump({'reason': 'First in_progress claim rejected absolute artifact paths before queue mutation. Normalize only unsubmitted preparation files and recalculate dependency hashes.', 'frozen_transition_evidence_edited': False, 'product_edited': False}, f, indent=2)
