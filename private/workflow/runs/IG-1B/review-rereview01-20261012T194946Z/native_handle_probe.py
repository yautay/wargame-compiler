"""Prove native redirection rejection occurs before yielding readable content."""
import datetime
import json
import os
from pathlib import Path
import subprocess
from unittest.mock import patch

from wgc.inputs import snapshot as s

here = Path(__file__).resolve().parent
base = here / "native-handle-probe-01"
base.mkdir(exist_ok=False)
outside = base / "outside"
outside.mkdir()
(outside / "secret").write_bytes(b"do not read redirected bytes")
link = base / "linked"
created = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True)
assert created.returncode == 0, created.stderr
yielded = False
with patch.object(s, "no_links", lambda path: None):
    try:
        with s.open_read(link / "secret"):
            yielded = True
    except s.SnapshotError as error:
        reason = str(error)
    else:
        raise AssertionError("A redirected handle must not yield a readable stream")
assert reason == "opened source escaped its exact enumerated path"
assert yielded is False
path = base / "regular"
path.write_bytes(b"stable")
write_denied = False
with s.open_read(path) as stream:
    try:
        path.write_bytes(b"changed")
    except OSError:
        write_denied = True
    assert stream.read() == b"stable"
assert write_denied
result = dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              platform=os.name, actual_junction_created=True,
              ancestry_precheck_disabled_only_for_race_simulation=True,
              yielded_readable_stream=yielded, native_rejection=reason,
              normal_read_handle_denies_write=True)
(here / "native-handle-probe.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result))
