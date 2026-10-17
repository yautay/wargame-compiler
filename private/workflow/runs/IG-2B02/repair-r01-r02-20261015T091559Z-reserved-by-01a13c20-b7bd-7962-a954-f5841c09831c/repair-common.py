"""Attempt-local constants and byte/pin helpers. No generation of source identities."""
import copy
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

R = Path('C:/repo/wargame-compiler')
A = Path(__file__).resolve().parent
D = R / 'private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
V = R / 'private/workflow/runs/IG-2B02/review-20261015T062645Z-01a13e3c-b2ef-7d90-bdfa-975891f92634'
P = R / 'private/workflow/runs/IG-2B02/repair-preparation-20261015T091559Z-01a13c20-b7bd-7962-a954-f5841c09831c'
C = R / 'private/workflow/runs/IG-2B02/coordinator-setup-20261015T104356Z-01a13c20-b7bd-7962-a954-f5841c09831c'

def now():
    return datetime.now(timezone.utc).isoformat()

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    with p.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def pin(p):
    p = p.resolve()
    return dict(path=p.relative_to(R).as_posix() if p.is_relative_to(R) else p.as_posix(),
                bytes=p.stat().st_size, sha256=sha(p))

def verify(x):
    p = Path(x['path'])
    p = p if p.is_absolute() else R / p
    assert p.is_file() and p.stat().st_size == x['bytes'] and sha(p) == x['sha256'], x

def pins_in(x):
    if isinstance(x, dict):
        if {'path', 'sha256', 'bytes'} <= x.keys():
            yield x
        for v in x.values():
            yield from pins_in(v)
    elif isinstance(x, list):
        for v in x:
            yield from pins_in(v)

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(encoded(value))

def checkpoint(stage, completed, next_operation):
    cp = load(A / 'checkpoint.json')
    cp.update(stage=stage, updated_utc=now(), blocker=None, next_operation=next_operation)
    cp['completed'].extend(completed)
    cp['owned_current_hashes'] = [pin(p) for p in sorted(A.rglob('*'))
                                 if p.is_file() and p.name != 'checkpoint.json']
    (A / 'checkpoint.json').write_bytes(encoded(cp))

SCOPE = load(P / 'repair-scope.json')
TARGETS = {t['region']['key']: t for t in SCOPE['targets']}
CFG = load(A / 'configuration.json')
RULE = 'For each specification key, use corrections_after_enlargement[key] when present, otherwise specification.components. Canonical inventory records never contain these component sidecars. Original generators and drafts are historical inputs only.'
