"""Bound coordinator preflight; never prints dependency records or source text."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path.cwd()
RUN = Path(__file__).parent
SESSION = Path('private/workflow/orchestrator/20261016T150146Z-33452c9a/001-IG-2B05-coordinator-6daf4d13')
ACTOR = 'ig2:001-IG-2B05-coordinator-6daf4d13:coordinator'

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(name, obj):
    with (RUN / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

def pin(p):
    p = Path(p)
    return {'path': p.as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}

def dep(section):
    cmd = [sys.executable, 'scripts/dependency_context.py', '--task', 'IG-2B05',
           '--manifest', (SESSION / 'dependency-view.json').as_posix(), '--sha256',
           '95f7c6edb5c7245a9dc59b56e220ff7ecdaea2d9d682bbef23f6835301882523',
           '--dependency', 'IG-2B04', '--section', section]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
    return json.loads(result.stdout)['data']

config = load(SESSION / 'runtime-configuration.json')
assert (config['status'], config['model'], config['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
packet = load(SESSION / 'packet.json')
verified = []
for item in packet['files'] + packet['control_files']:
    assert sha(item['path']) == item['sha256'], item['path']
    verified.append(pin(item['path']))
inventory = dep('inventory')
toolchain = dep('toolchain')
boundary = dep('boundary')
for item in [inventory['baseline_inventory'], inventory['identity_registry'],
             inventory['source']['pdf'], inventory['source']['provenance'],
             *inventory['reports'].values()]:
    assert sha(item['path']) == item['sha256'], item['path']
    verified.append(pin(item['path']))
assert sha(toolchain['python_executable']['path']) == toolchain['python_executable']['sha256']
write('dependency-inputs.json', {'format': 'wgc-inventory-batch-inputs-1', 'task': 'IG-2B05',
                              'dependency': 'IG-2B04', 'inventory': inventory,
                              'boundary': boundary, 'toolchain': toolchain})
write('preflight.json', {'task': 'IG-2B05', 'role': 'coordinator', 'actor': ACTOR,
                       'model': config['model'], 'reasoning': config['reasoning'],
                       'configuration_evidence': (SESSION / 'runtime-configuration.json').as_posix(),
                       'configuration_sha256': sha(SESSION / 'runtime-configuration.json'),
                       'packet': pin(SESSION / 'packet.json'), 'task_snapshot': pin(SESSION / 'task.json'),
                       'verified_pins': verified,
                       'preexisting_owned_paths': [pin(p) for p in ['docs/work/queue.json',
                           'docs/work/context-policy.json', 'docs/work/tasks/IG-2B05.md',
                           'docs/STATUS.md', 'docs/HANDOFF.md', 'docs/ROADMAP.md']],
                       'product_files_written': 0, 'dependency_records_printed': 0})
print(json.dumps({'verified_pin_count': len(verified), 'configuration_sha256': sha(SESSION / 'runtime-configuration.json'),
                  'dependency_inputs_sha256': sha(RUN / 'dependency-inputs.json')}))
