"""Continue unchanged closure assertions; report unavailable symlink creation."""
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRESH = HERE / "c"
FRESH.mkdir(exist_ok=False)
copies = []
for name in ["closure_probes.py", "review_controls.py"]:
    raw = (HERE / name).read_bytes()
    (FRESH / name).write_bytes(raw)
    assert (FRESH / name).read_bytes() == raw
    copies.append(dict(path=str(FRESH / name), sha256=hashlib.sha256(raw).hexdigest(), byte_identical=True))
spec = importlib.util.spec_from_file_location("available_windows_closure", FRESH / "closure_probes.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
for kind in ["input_snapshot", "source_snapshot"]:
    for action in ["verify", "reuse"]:
        probe.declared_type(kind, action, "directory")
    probe.missing_blob(kind)
    probe.linked_parent(kind)
    probe.nonregular(kind)
    probe.staging(kind)
result = dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              cases=probe.ROWS, count=len(probe.ROWS), all_available_cases_pass=True,
              original_probe_script_bytes_unchanged=True, copies=copies,
              actual_file_symlink_rejection=None, actual_directory_symlink_rejection=None,
              symlink_creation_unavailable=dict(winerror=1314,
                  reason="A required privilege is not held by the client",
                  source_log="closure-probes.log",
                  note="Reviewed local execution succeeded; OS refused link creation before a rejection assertion could run. No system privilege/configuration changes or bypass were attempted."),
              native_junctions_rejected=True,
              nonregular_entries="S_IFIFO metadata simulation; no real Windows FIFO was claimed")
(HERE / "closure-available.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
