import os
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from wgc import fsbatch, kb, tasks
from wgc.kb import Workspace

root, step = Path(sys.argv[2]), sys.argv[3]
INPUTS = ("SEG-dsk.4.3",)


def crash(name):
    if name == step:
        os._exit(9)  # no finally, no cleanup: like a killed process


fsbatch._step = crash
real_manifest = fsbatch._manifest


def manifest(journal, state, *args):
    if step == "staged" and state == "prepared":
        os._exit(9)  # new content and copies written, manifest not yet
    real_manifest(journal, state, *args)


fsbatch._manifest = manifest
spec = tasks.get("wgc.tables.parse")
ws = Workspace(root)
props = spec.deterministic_impl(ws, INPUTS) + spec.deterministic_impl(ws, INPUTS)
props[0]["record"]["title"] = "CRT"
props[1]["record"]["id"] = "TAB-new"
kb.accept(root, spec, INPUTS, props, by={"tier": "deterministic", "tool": spec.name}, job=sys.argv[4], ws=ws)
sys.exit(0)
