"""Preserve failed operational-identity comparison, correct only its normalization."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
failed = {'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/verify.py before',
    'exit_code': 1, 'started_utc': None, 'ended_utc': None, 'wall_seconds': None,
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'failure': 'AssertionError at verify.py:59: executor oracle identity normalization missed review_actor -> executor_actor key rename.',
    'scope': 'Review-helper setup only; all earlier byte verification assertions passed. No product assertion changed.',
    'resolution': 'Diff inspection established only operational actor key/value changed. Corrected verifier normalizes both, preserving all byte/target/assertion checks.',
    'original_verifier_sha256': hashlib.sha256((RUN / 'verify.py').read_bytes()).hexdigest()}
with (RUN / 'verification-setup-failure.json').open('x', encoding='utf-8') as f:
    json.dump(failed,f,indent=2); f.write('\n')
raw = (RUN / 'verify.py').read_bytes()
old = b"raw.replace(b'ig1-continuation-executor-20261013', b'ig1d-replacement-reviewer-20261013T140127Z')"
new = old + b".replace(b'executor_actor', b'review_actor')"
assert raw.count(old) == 1
with (RUN / 'verify-corrected.py').open('xb') as f: f.write(raw.replace(old,new))
print('Original failed verifier retained; only operational identity-key normalization corrected.')
