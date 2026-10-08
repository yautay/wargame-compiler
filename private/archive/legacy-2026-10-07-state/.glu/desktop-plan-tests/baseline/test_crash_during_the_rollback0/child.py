import errno
import os
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from wgc import fsbatch, kb, tasks
from wgc.kb import Workspace

root, mode, step = Path(sys.argv[2]), sys.argv[3], sys.argv[4]
fsbatch._step = lambda name: os._exit(9) if name == step else None
if mode == "recover":
    kb.recover(root)
    sys.exit(0)
real = fsbatch._manifest


def manifest(journal, state, *args):
    if state == "committed":
        raise OSError(errno.ENOSPC, "brak miejsca (symulacja)")
    real(journal, state, *args)


fsbatch._manifest = manifest
spec = tasks.get("wgc.tables.parse")
ws = Workspace(root)
I = ("SEG-dsk.4.3",)
props = spec.deterministic_impl(ws, I) + spec.deterministic_impl(ws, I)
props[0]["record"]["title"] = "CRT"
props[1]["record"]["id"] = "TAB-new"
kb.accept(root, spec, I, props, by={"tier": "deterministic", "tool": spec.name}, job="job_000009", ws=ws)
