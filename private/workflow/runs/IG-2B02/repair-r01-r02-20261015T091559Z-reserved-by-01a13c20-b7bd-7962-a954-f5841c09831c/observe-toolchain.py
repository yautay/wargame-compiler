"""Fresh local/bundled version and executable-byte observation; no installation."""
from importlib.machinery import SourceFileLoader
from pathlib import Path
import importlib.metadata
import subprocess
import sys

u = SourceFileLoader('repair_common', str(Path(__file__).with_name('repair-common.py'))).load_module()
baseline = u.load(u.D / 'toolchain.json')
runtime_path = Path('C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/runtime.json')
runtime = u.load(runtime_path)
assert runtime['bundleVersion'] == '26.1013.11914'
result = dict(actor=u.CFG['actor'], observed_utc=u.now(), baseline=u.pin(u.D / 'toolchain.json'),
              runtime_manifest=u.pin(runtime_path), bundle_version=runtime['bundleVersion'],
              python=sys.version, python_executable=u.pin(Path(sys.executable)),
              libraries={k: importlib.metadata.version(k) for k in ('pypdf','pdfplumber','Pillow','pytest')},
              native={}, frozen_contract_and_tool_pins=baseline['frozen_contract_and_tool_pins'],
              workflow_and_checks=baseline['workflow_and_checks'], drift=[])
assert result['python'] == baseline['python']
assert result['python_executable'] == baseline['python_executable']
assert result['libraries'] == baseline['libraries']
for name, old in baseline['native'].items():
    exe = Path(old['executable']['path'])
    u.verify(old['executable'])
    args = [str(exe), '-v' if name in ('pdfinfo','pdftoppm') else '--version']
    p = subprocess.run(args, capture_output=True)
    assert p.returncode == 0, (args, p.stderr)
    raw_version = (p.stdout + p.stderr).decode('utf-8')
    version = raw_version.replace('\r\n', '\n').strip()
    assert version == old['version'], (name, version, old['version'])
    result['native'][name] = dict(executable=u.pin(exe), version=version, raw_stdout=p.stdout.decode('utf-8'), raw_stderr=p.stderr.decode('utf-8'), version_comparison='Explicit CRLF to LF only for native version banner comparison with frozen text-mode record.',
                                command=args, exit_code=p.returncode)
for x in result['frozen_contract_and_tool_pins'] + result['workflow_and_checks']:
    u.verify(x)
u.write(u.A / 'toolchain.json', result)
print('Fresh runtime bundle, Python/libraries/native versions and pinned bytes match frozen toolchain.')
