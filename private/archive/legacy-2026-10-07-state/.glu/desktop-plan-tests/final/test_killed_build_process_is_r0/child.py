import os
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from glu import exec as executor, planner
from glu.store import Store
from wgc.kb import Workspace

root = Path(sys.argv[2])
real = Store.finish_job


def die_after_kb(self, job_id, tier, outcome, steps, **fields):
    if outcome == "accepted":
        os._exit(9)  # kb/ and the receipt are written, the Attempt is not
    return real(self, job_id, tier, outcome, steps, **fields)


Store.finish_job = die_after_kb
ws = Workspace(root)
with Store.at_root(root) as store:
    executor.run(store, ws, planner.plan(ws, "1"), "p")
