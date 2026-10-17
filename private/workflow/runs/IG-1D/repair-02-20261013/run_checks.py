"""Capture bounded repair checks with exclusive logs and short fresh temp paths."""
from datetime import datetime, timezone
from pathlib import Path
import json, os, subprocess, sys, time

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
PRIOR = ROOT/'private/workflow/runs/IG-1D/review-20261013T122807Z'
RISK = ROOT/'private/workflow/runs/IG-1D/replacement-rereview-20261013T140127Z'
name = sys.argv[1]
tail = ['-q', '-p', 'no:cacheprovider', '--basetemp', 'private/workflow/checks/r4-'+name, '--tb=short']
commands = {
    'explicit': [sys.executable, '-m', 'pytest', 'tests/wgu_adapter', 'tests/export',
                 str(PRIOR/'probes.py'), str(PRIOR/'lineage_probes.py'),
                 str(RISK/'risk_probes.py'), str(RISK/'receipt_edge_probes.py'),
                 str(RISK/'export_history_probes.py')] + tail,
    'accounting': [sys.executable, '-B', str(RUN/'accounting.py')],
    'project': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-1D'],
    'diff': ['git', 'diff', '--check'],
}
temp = ROOT/('private/workflow/checks/r4t-'+name)
temp.mkdir(exist_ok=False)
env = dict(os.environ, PYTHONPATH=str(ROOT/'src')+os.pathsep+str(PRIOR),
           PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0', TEMP=str(temp), TMP=str(temp))
start = datetime.now(timezone.utc); tick = time.perf_counter()
with (RUN/(name+'.log')).open('xb') as log:
    result = subprocess.run(commands[name], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
record = {'command': subprocess.list2cmdline(commands[name]), 'argv': commands[name],
          'exit_code': result.returncode, 'started_utc': start.isoformat(),
          'ended_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter()-tick,
          'log': (RUN/(name+'.log')).relative_to(ROOT).as_posix()}
with (RUN/(name+'-check.json')).open('x', encoding='utf-8', newline='\n') as f:
    json.dump(record, f, indent=2); f.write('\n')
print(json.dumps(record), flush=True)
print((RUN/(name+'.log')).read_text(encoding='utf-8', errors='replace')[-2400:], flush=True)
raise SystemExit(result.returncode)
