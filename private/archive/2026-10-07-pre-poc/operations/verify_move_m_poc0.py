import hashlib
import json
from pathlib import Path
ROOT = Path(r'C:\dev\wargame-compiler')
SNAP = ROOT / 'private/archive/2026-10-07-pre-poc'
manifest = json.loads((SNAP / 'manifest.json').read_text(encoding='utf-8'))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
mapped = []
for row in manifest['files']:
    original = row['path']
    if original.startswith('private/'):
        target = original
    elif original.startswith('.glu/'):
        target = 'private/archive/legacy-2026-10-07-state/' + original
    else:
        target = 'archive/legacy-2026-10-07/project/' + original
    p = ROOT / target
    assert p.stat().st_size == row['size'] and sha(p) == row['sha256'], original
    mapped.append(dict(row, destination=target))
assert sha(ROOT / '.git/index') == manifest['git']['index_sha256']
public = [row for row in mapped if row['class'] == 'public']
for filename, data in [(SNAP / 'movement-map.json', mapped),
    (ROOT / 'archive/legacy-2026-10-07/movement-map.json', public),
    (SNAP / 'post-move-verification.json', {'checked': len(mapped), 'public': len(public),
     'private': len(mapped)-len(public), 'mismatches': [], 'git_index_unchanged': True})]:
    with filename.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
print({'checked': len(mapped), 'public': len(public), 'private': len(mapped)-len(public), 'mismatches': 0})
