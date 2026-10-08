import sys
import time
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from wgc import kb, tasks
from wgc.kb import Workspace

root, rid, marker, timeout = Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), float(sys.argv[5])
real_write = kb._write_batch


def slow_write(root, changes, job):  # a long write keeps the other process waiting on the lock
    time.sleep(0.3)
    real_write(root, changes, job)


kb._write_batch = slow_write
spec = tasks.get("wgc.tables.parse")
ws = Workspace(root)
props = spec.deterministic_impl(ws, ("SEG-dsk.4.3",))
props[0]["record"]["id"] = rid
marker.write_text("ready", encoding="utf-8")
try:
    res = kb.accept(root, spec, ("SEG-dsk.4.3",), props, ws=ws, lock_timeout=timeout,
                    by={"tier": "deterministic", "tool": "wgc.tables.parse@0"})
except kb.KBBusy as e:
    print(e)
    sys.exit(3)
print(res.issues)
sys.exit(0 if res.ok else 1)
