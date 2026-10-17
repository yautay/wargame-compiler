"""Verify frozen R03 input bytes only; never repair, transition or create a run."""
import argparse, hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path
R=Path('C:/repo/wargame-compiler'); P=Path(__file__).resolve().parent
def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()
parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--report',required=True); args=parser.parse_args()
assert '\\' not in args.report and ':' not in args.report and '..' not in Path(args.report).parts
assert args.report.startswith('private/workflow/runs/IG-2B02/')
target=R/args.report; assert target.parent.is_dir() and not target.exists()
started=datetime.now(timezone.utc).isoformat(); clock=time.monotonic()
catalogue=json.loads((P/'frozen-base-pins.json').read_text(encoding='utf-8'))
for row in catalogue['frozen_pins']:
    path=Path(row['path']); path=path if path.is_absolute() else R/path
    assert path.is_file() and path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],row['path']
state=json.loads((P/'preparation.json').read_text(encoding='utf-8')); q=json.loads((R/'docs/work/queue.json').read_text(encoding='utf-8')); task=next(t for t in q['tasks'] if t['id']=='IG-2B02')
assert state['review_event'] in task['events']
assert all(next(t for t in q['tasks'] if t['id']==dep)['status']=='done' for dep in ('IG-2A','IG-2B01'))
report=dict(outcome='passed_frozen_bytes_only',frozen_refs_verified=len(catalogue['frozen_pins']),original_review_event_preserved=True,current_status=task['status'],current_queue_sha256=sha(R/'docs/work/queue.json'),queue_equals_preparation_snapshot=sha(R/'docs/work/queue.json')==state['queue_snapshot']['sha256'],started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.monotonic()-clock,repair_performed=False,meaning_review_performed=False,acceptance_granted=False,note='Mutable queue/projections are not frozen input. Caller must separately check only explicitly authorized coordinator/claim/event differences, actual scope and fresh packet. Success is not claim readiness or acceptance.')
with target.open('x',encoding='utf-8',newline='\n') as stream: json.dump(report,stream,indent=2); stream.write('\n')
print(json.dumps(report,indent=2))
