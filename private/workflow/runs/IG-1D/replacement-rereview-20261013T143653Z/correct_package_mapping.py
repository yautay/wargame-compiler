"""Retain second setup failure and bind the audit target by exact published bytes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
record = {'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/verify-corrected.py before',
    'exit_code': 1, 'started_utc': None, 'ended_utc': None, 'wall_seconds': None,
    'recorded_utc': datetime.now(timezone.utc).isoformat(), 'failure': 'StopIteration at line 63: new delivery lists its own packages/ copy, not the earlier official canonical path.',
    'scope': 'Review setup mapping; all earlier delivery/preservation assertions passed.',
    'resolution': 'Locate the exact package via delivery artifacts and verify all four hashes and exact bytes against the audit target. Keep all original accounting assertions and target unchanged.',
    'failed_verifier_sha256': hashlib.sha256((RUN / 'verify-corrected.py').read_bytes()).hexdigest()}
with (RUN / 'package-mapping-setup-failure.json').open('x', encoding='utf-8') as f:
    json.dump(record,f,indent=2);f.write('\n')
raw = (RUN / 'verify-corrected.py').read_text()
start = raw.index("# A fresh two-transform audit")
end = raw.index("report = ",start)
replacement = '''# Bind the unchanged audit target to the exact new delivery publication.
package = ROOT / 'private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc'
published = (ROOT / next(a['path'] for a in d['artifacts'] if '/packages/sha256-' in a['path'] and a['path'].endswith('/source-ig.json'))).parent
package_mapping = []
for name in ['source-ig.json', 'identity-registry.json', 'references.json', 'manifest.json']:
    a = next(a for a in d['artifacts'] if a['path'] == (published / name).relative_to(ROOT).as_posix())
    verify(a)
    assert (published / name).read_bytes() == (package / name).read_bytes()
    package_mapping.append({'delivery_path': a['path'], 'audit_target': (package / name).relative_to(ROOT).as_posix(), 'sha256': a['sha256'], 'exact_bytes_match': True})
'''
raw = raw[:start] + replacement + raw[end:]
raw = raw.replace("'canonical_target_bound_to_current_delivery':True}", "'canonical_target_bound_to_current_delivery':True, 'package_mapping':package_mapping}")
with (RUN / 'verify-final.py').open('x', encoding='utf-8', newline='\n') as f: f.write(raw)
print('Both failed setup variants retained; exact publication-to-audit byte mapping added.')
