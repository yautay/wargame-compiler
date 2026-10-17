"""Prepare replacement review without modifying frozen evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
OLD = ROOT / 'private/workflow/runs/IG-1D/rereview-20261013T131151Z'
ACTOR = 'ig1d-replacement-reviewer-20261013T140127Z'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(name, data):
    with (RUN / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        f.write('\n')

write('checkpoint.json', {'role': 'reviewer', 'actor': ACTOR, 'task': 'IG-1D',
    'started_utc': '2026-10-13T13:57:00+00:00', 'start_note': 'First local tool call; timestamp reconstructed from session sequence, precision approximately one minute. Exact measured check times recorded separately.',
    'evidence_run_started_utc': datetime.now(timezone.utc).isoformat(),
    'requested_model': 'gpt-6.1-sol', 'requested_reasoning': 'high', 'model': None, 'reasoning': None,
    'configuration_evidence': 'Fresh confirmation requested in this reviewer chat; runtime metadata unavailable.',
    'scope': 'Independent replacement technical review of repair iteration 1; no implementation or queue changes.',
    'tokens': None, 'cost': None, 'operator_seconds': None})
adaptations = []
for name in ['risk_probes.py', 'receipt_edge_probes.py', 'export_history_probes.py', 'accounting.py']:
    original = (OLD / name).read_bytes()
    adapted = original.replace(b'ig1c-reviewer-20261013T071955Z', ACTOR.encode()) if name == 'accounting.py' else original
    with (RUN / name).open('xb') as f:
        f.write(adapted)
    adaptations.append({'source': str((OLD / name).relative_to(ROOT)), 'source_sha256': sha(OLD / name),
        'copy': str((RUN / name).relative_to(ROOT)), 'copy_sha256': sha(RUN / name),
        'change': 'Operational reviewer identity only; RUN resolves to own directory; assertions and target unchanged.' if name == 'accounting.py' else 'Exact byte copy; all assertions unchanged.'})
write('helper-provenance.json', adaptations)
old_files = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)} for p in sorted(OLD.rglob('*')) if p.is_file()]
write('prior-rereview-baseline.json', {'artifacts': old_files, 'count': len(old_files), 'final_review_exists': (OLD / 'review.json').exists()})
print(json.dumps({'run': str(RUN), 'actor': ACTOR, 'old_files_preserved': len(old_files), 'copied_helpers': len(adaptations)}))
