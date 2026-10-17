"""Keep the current repair packet bounded; preserve scope/evidence byte pins."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd() / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

prep = Path('private/workflow/runs/IG-2B08/prepare-F02-7582f722')
queue_path = Path('docs/work/queue.json')
lock = Path('private/workflow/queue.lock')
fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    before_hash = w.digest(queue_path)
    before = w.read_json(queue_path)
    after = copy.deepcopy(before)
    task = next(t for t in after['tasks'] if t['id'] == 'IG-2B08')
    old = next(t for t in before['tasks'] if t['id'] == 'IG-2B08')
    task['context'] = [p for p in task['context'] if p not in {
        (prep / 'repair-scope.json').as_posix(), (prep / 'authorization.json').as_posix()}]
    task['inputs'] = [
        'Original baseline/source/provenance and historical input pins are retained in private/workflow/runs/IG-2B08/manifest-recovery-20261017-F01-01/input-pins.json. Current frozen F01 delivery reports and helpers are pinned ONLY by the CURRENT F02 repair-context.json.'
        if x.startswith('Exact current region ledger, continuations, coverage, source-pins and installed toolchain reports') else x
        for x in task['inputs']]
    assert task['events'] == old['events'] and task['acceptance'] == old['acceptance'] and task['tests'] == old['tests']
    o.check_queue_delta(before, after, old, 'coordinator', outcome='progress')
    assert w.digest(queue_path) == before_hash
    temp = queue_path.with_name('queue.F02-packet-refinement.pending.json')
    with temp.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(after, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    os.replace(temp, queue_path)
    w.validate(after, Path.cwd(), check_views=False)
    w.render(after, Path.cwd())
    w.validate(after, Path.cwd())
    o.verify_repair_authorization(Path.cwd(), task)
    # Construct bounded packet internally; never print dependency records or packet text.
    packet = w.packet(after, Path.cwd(), 'IG-2B08', output=False)
    result = {'task': 'IG-2B08', 'reason': 'Initial check: task dry-run exceeded 100 KB; narrowed text context to compact index. Scope/authorization remain exact immutable pins and readable on demand.',
              'scope_and_authorization_unchanged': True, 'events_unchanged':True,
              'packet_text_bytes':packet['text_bytes'], 'status':'changes_requested', 'queue_sha256':w.digest(queue_path)}
    with (prep/'packet-refinement.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'packet_text_bytes':packet['text_bytes'], 'validation_exit':0, 'authorization_unchanged':True}))
finally:
    os.close(fd)
    lock.unlink()
