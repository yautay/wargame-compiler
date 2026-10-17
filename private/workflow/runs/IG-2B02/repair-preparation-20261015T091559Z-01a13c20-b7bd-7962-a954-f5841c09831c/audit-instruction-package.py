"""Audit prepared instructions and own configuration records; no content review."""
import hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path

R = Path('C:/repo/wargame-compiler')
P = Path(__file__).resolve().parent

def read(name):
    return json.loads((P/name).read_text(encoding='utf-8'))

def pin(path):
    raw = path.read_bytes()
    return dict(path=path.relative_to(R).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def check(row):
    path = Path(row['path'])
    if not path.is_absolute():
        path = R/path
    raw = path.read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']

def visit(obj):
    if isinstance(obj, dict):
        if all(key in obj for key in ('path', 'bytes', 'sha256')) and isinstance(obj['sha256'], str):
            check(obj)
        for value in obj.values():
            visit(value)
    elif isinstance(obj, list):
        for value in obj:
            visit(value)

for name in ('instruction-delivery.json', 'launch-gate-pins.json', 'repair-scope.json', 'preparation.json'):
    visit(read(name))
table_count = 0
for name in ('repair-launch.txt', 'coordinator-setup.txt', 'independent-rereview-template.txt'):
    raw = (P/name).read_bytes()
    assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw
    for line in raw.decode('utf-8').splitlines():
        match = re.fullmatch(r'([^|]+) \| ([0-9]+) \| ([0-9a-f]{64})', line)
        if match:
            check(dict(path=match[1], bytes=int(match[2]), sha256=match[3]))
            table_count += 1
for path in P.glob('*.py'):
    compile(path.read_text(encoding='utf-8'), str(path), 'exec')
state = read('preparation.json')
assert pin(R/'docs/work/queue.json') == state['queue_snapshot']
task = next(t for t in json.loads((R/'docs/work/queue.json').read_text(encoding='utf-8'))['tasks'] if t['id']=='IG-2B02')
assert task['status']=='review' and len(task['events'])==3
assert not (R/state['reserved_absent_repair_attempt']).exists()

# Explicit own-current-session configuration scope; do not inspect message records.
metadata = Path('C:/Users/yauta/.codex/sessions/2026/10/14/rollout-2026-10-14T22-35-39-01a13c20-b7bd-7962-a954-f5841c09831c.jsonl')
session_record = None
turn_record = None
with metadata.open('r', encoding='utf-8') as stream:
    for number, line in enumerate(stream, 1):
        if '"session_meta"' not in line[:160] and '"turn_context"' not in line[:160]:
            continue
        item = json.loads(line)
        payload = item.get('payload', {})
        if item.get('type') == 'session_meta':
            session_record = dict(line=number, raw_record_sha256=hashlib.sha256(line.encode('utf-8')).hexdigest(), **{key:payload.get(key) for key in ('id','cwd','source','model_provider')})
        elif item.get('type') == 'turn_context':
            turn_record = dict(line=number, raw_record_sha256=hashlib.sha256(line.encode('utf-8')).hexdigest(), **{key:payload.get(key) for key in ('model','effort','reasoning_effort','cwd')})
assert session_record and session_record['id']=='01a13c20-b7bd-7962-a954-f5841c09831c'
assert turn_record
report = dict(outcome='passed_instruction_package_byte_audit_only', observed_utc=datetime.now(timezone.utc).isoformat(), task='IG-2B02', instruction_table_pins_verified=table_count, nested_pin_objects_verified=True, scripts_syntax_valid=True, utf8_no_bom_lf_instructions=True, queue_unchanged=True, current_status='review', event_count=3, reserved_repair_attempt_absent=True, own_preparer_configuration=dict(source=str(metadata), scope='Own session_meta and latest turn_context identity/configuration fields only; no conversation content.', session_record=session_record, turn_record=turn_record), configuration_of_future_repair_session=None, future_configuration_reason='Future session has not been created. It must confirm its own actual model and reasoning before claim.', repair_executed=False, session_created=False, acceptance_granted=False)
with (P/'instruction-package-audit.json').open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps(report, indent=2))
