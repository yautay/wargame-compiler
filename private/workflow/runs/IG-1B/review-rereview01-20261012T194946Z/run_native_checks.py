"""Run exact independent reviewer scripts and explicit input tests locally."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path.cwd()
here = Path(__file__).resolve().parent
env = dict(os.environ, PYTHONPATH=str(root / "src"), PYTHONDONTWRITEBYTECODE="1")
records = []
commands = [("input-tests", [sys.executable, "-m", "pytest", "tests/inputs", "-q",
                              "-p", "no:cacheprovider", "--basetemp", str(here / "input-test-temp-01"),
                              "--tb=short"])]
commands += [(name, [sys.executable, str(here / (name + ".py"))])
             for name in ["review_controls", "native_handle_probe", "private_audit"]]
for name, argv in commands:
    started = datetime.datetime.now(datetime.timezone.utc)
    timer = time.monotonic()
    result = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True)
    ended = datetime.datetime.now(datetime.timezone.utc)
    log = here / (name + ".log")
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    records.append(dict(argv=argv, command=subprocess.list2cmdline(argv), exit_code=result.returncode,
                        started_utc=started.isoformat(), ended_utc=ended.isoformat(),
                        wall_seconds=time.monotonic() - timer,
                        log=log.relative_to(root).as_posix(),
                        log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
                        execution_context="Reviewed exact local require_escalated; native Windows handles/links"))
    (here / "native-checks.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(name, "exit", result.returncode)
    print(result.stdout)
    if result.returncode:
        print(result.stderr)
raise SystemExit(0 if all(x["exit_code"] == 0 for x in records) else 1)
