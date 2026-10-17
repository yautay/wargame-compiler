"""New evidence run for final bounded R04 repair, same confirmed reviewer chat."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
OLD = ROOT / 'private/workflow/runs/IG-1D/replacement-rereview-20261013T140127Z'
ACTOR = 'ig1d-replacement-reviewer-20261013T140127Z'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n, d):
    with (RUN / n).open('x', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write('\n')
write('checkpoint.json', {'role': 'reviewer', 'actor': ACTOR, 'task': 'IG-1D',
    'started_utc': datetime.now(timezone.utc).isoformat(), 'measurement_scope': 'Fresh evidence run; earlier instruction reading unmeasured.',
    'repair_iteration': 2, 'maximum_repair_iterations': 2,
    'model': 'gpt-6.1-sol', 'reasoning': 'high', 'same_reviewer_chat_continuity': True,
    'configuration_evidence': {'path': (OLD / 'configuration-confirmed.json').relative_to(ROOT).as_posix(), 'sha256': sha(OLD / 'configuration-confirmed.json')},
    'tokens': None, 'cost': None, 'operator_seconds': None})
copies = []
for name in ['accounting.py', 'supplemental_audit.py', 'risk_probes.py', 'receipt_edge_probes.py', 'export_history_probes.py', 'run_checks.py']:
    raw = (OLD / name).read_bytes()
    new = raw.replace(b'r3-', b'r5-').replace(b'r3t-', b'r5t-') if name == 'run_checks.py' else raw
    with (RUN / name).open('xb') as f: f.write(new)
    copies.append({'source': (OLD / name).relative_to(ROOT).as_posix(), 'source_sha256': sha(OLD / name),
        'copy': (RUN / name).relative_to(ROOT).as_posix(), 'sha256': sha(RUN / name),
        'delta': 'Only fresh basetemp/TEMP namespace; RUN resolves to new directory.' if name == 'run_checks.py' else 'Exact byte copy; RUN resolves to new directory; same independent reviewer actor.'})
write('helper-provenance.json', {'artifacts': copies, 'all_assertions_unchanged': True,
    'canonical_target_note': 'The existing canonical package is still the exact repair-2 target. Before verification binds its four exact files through new delivery.artifacts; no pre-manifest package is selected.'})
print(json.dumps({'run': str(RUN), 'started_utc': json.loads((RUN / 'checkpoint.json').read_bytes())['started_utc'], 'copies': len(copies)}))
