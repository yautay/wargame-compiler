"""Run unchanged validation commands with the authorized process-local environment."""
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

from audit import ROOT, OUT, base, load, pin, sha, write

mode = sys.argv[1]
scope = load(ROOT / 'prepare-v01-e742d89b-01/scope.json')
assert sha(scope['toolchain']['path']) == scope['toolchain']['sha256']
assert sha(scope['rg']['path']) == scope['rg']['sha256']
environment = os.environ.copy()
inherited_path = environment.get('PATH', '')
rg_dir = os.path.dirname(scope['rg']['path']).replace('/', '\\')
poppler_dir = scope['process_path_prefix']
environment['PATH'] = rg_dir + ';' + poppler_dir + ';' + inherited_path
environment['PYTHONPATH'] = scope['process_pythonpath']
environment['PYTHONDONTWRITEBYTECODE'] = '1'
assert len(environment['PYTHONPATH'].split(';')) == 2
assert environment['PATH'].endswith(';' + inherited_path)
resolved = shutil.which('rg', path=environment['PATH'])
assert resolved and sha(resolved) == scope['rg']['sha256']
if mode == 'repository':
    argv = ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B04']
    command = 'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B04'
elif mode == 'sources':
    basetemp = OUT / 'pytest-sources'
    assert not basetemp.exists(), 'Basetemp must be fresh'
    argv = ['.venv/Scripts/python.exe', '-m', 'pytest', '-q', 'tests/sources', '--basetemp', basetemp.as_posix(), '-p', 'no:cacheprovider', '--tb=short']
    command = ' '.join(argv)
elif mode == 'diff':
    argv = ['git', 'diff', '--check']
    command = 'git diff --check'
else:
    raise ValueError(mode)
log = OUT / (mode + '.log')
assert not log.exists()
started = datetime.now(timezone.utc).isoformat()
t0 = time.monotonic()
with log.open('wb') as output:
    result = subprocess.run(argv, env=environment, stdout=output, stderr=subprocess.STDOUT)
report = base('Independent unchanged validation command; actual exit and full log frozen.')
report.update(command=command, argv=argv, exit_code=result.returncode,
              started_utc=started, ended_utc=datetime.now(timezone.utc).isoformat(),
              wall_seconds=time.monotonic()-t0, log=pin(log),
              environment={'rg_resolved': resolved, 'rg_sha256': sha(resolved),
                           'inherited_path': inherited_path,
                           'complete_inherited_path_preserved_as_suffix': True,
                           'prepended_directories': [rg_dir, poppler_dir],
                           'process_pythonpath': environment['PYTHONPATH'],
                           'toolchain': scope['toolchain']},
              sandbox_permissions='require_escalated' if mode != 'diff' else 'use_default')
if mode == 'repository':
    text = log.read_text(encoding='utf-8-sig', errors='replace')
    roots = [line[len('LOG_ROOT='):].strip() for line in text.splitlines() if line.startswith('LOG_ROOT=')]
    assert len(roots) == 1, roots
    from pathlib import Path
    checkroot = Path(roots[0])
    report['subchecks'] = load(checkroot / 'result.json')
    report['check_artifacts'] = [pin(checkroot / name) for name in ['plan.log', 'dry-run.log', 'pytest.log', 'diff-check.log', 'result.json']]
    print((checkroot / 'pytest.log').read_text(encoding='utf-8-sig').strip())
elif mode == 'sources':
    print(log.read_text(encoding='utf-8-sig').strip())
write(mode + '.json', report)
print('exit_code=' + str(result.returncode))
sys.exit(result.returncode)
