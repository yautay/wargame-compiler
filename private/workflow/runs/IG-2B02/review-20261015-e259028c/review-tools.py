"""Independent, append-only IG-2B02 reviewer evidence helpers."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path.cwd()
OUT = Path(__file__).parent
SESSION = Path('private/workflow/orchestrator/20261015T144301Z-98bff5f8/002-IG-2B02-reviewer-e259028c')
BASE = Path('private/workflow/runs/IG-2B02/repair-r01-r02-20261015T091559Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c')
V01 = Path('private/workflow/runs/IG-2B02/repair-v01-20261015T143929Z-d8aa5d')
PREP = Path('private/workflow/runs/IG-2B02/preparation-20261014T201344Z-01a13c09-ed4d-7ab2-b967-5e6db69e78b8')

def read(p):
    return json.loads(Path(p).read_bytes())

def pin(p):
    p = Path(p)
    data = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix() if p.is_absolute() and p.is_relative_to(ROOT) else p.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

CONFIG = SESSION / 'runtime-configuration.json'
observed = read(CONFIG)
assert observed['status'] == 'confirmed' and observed['model'] == 'gpt-6.1-sol' and observed['reasoning'] == 'high'
META = {'role': 'reviewer', 'actor': 'ig2:002-IG-2B02-reviewer-e259028c:reviewer', 'model': observed['model'], 'reasoning': observed['reasoning'], 'configuration_evidence': CONFIG.as_posix(), 'configuration_sha256': pin(CONFIG)['sha256'], 'task': 'IG-2B02'}

def write(name, data):
    target = OUT / name
    with target.open('x', encoding='utf-8', newline='\n') as f:
        json.dump({**META, **data}, f, indent=2, ensure_ascii=False)
        f.write('\n')
    return pin(target)

def check_pin(p):
    actual = pin(p['path'])
    return {'expected': p, 'actual': actual, 'matches': all(actual[k] == p[k] for k in ('sha256', 'bytes') if k in p)}

def verify(name):
    packet = read(SESSION/'packet.json')
    refs = read(SESSION/'references.json')
    ref = read(SESSION/'delivery-reference.json')
    delivery = read(ref['evidence'])
    old = read(BASE/'delivery.json')
    prior = read(refs['findings']['evidence'])
    pairs = [{'path': ref['evidence'], 'sha256': ref['sha256']}]
    pairs += packet['files']
    pairs += [{'path': v['evidence'], 'sha256': v['sha256']} for v in refs.values() if isinstance(v, dict) and 'evidence' in v]
    pairs += [{'path': v['evidence'], 'sha256': v['sha256']} for v in refs['dependencies'].values()]
    pairs += delivery['artifacts']
    pairs += prior['review_evidence']
    pairs += read(V01/'base-files.json')['files']
    tool = read(PREP/'toolchain.json')
    pairs += tool['frozen_contract_and_tool_pins'] + tool['workflow_and_checks'] + [tool['python_executable']]
    pairs += [v['executable'] for v in tool['native'].values()]
    pairs += [{'path': delivery['configuration_evidence'], 'sha256': delivery['configuration_sha256']}]
    results = [check_pin(p) for p in pairs]
    manifest = read(delivery['manifest']['path'])
    entries = manifest['artifacts']
    prefix = delivery['artifacts'][:len(old['artifacts'])] == old['artifacts']
    # The manifest excludes its own final artifact entry.
    manifest_agreement = delivery['artifacts'][:-1] == entries and delivery['artifacts'][-1] == delivery['manifest']
    ok = all(r['matches'] for r in results) and prefix and manifest_agreement
    report = write(name, {'created_utc': datetime.now(timezone.utc).isoformat(), 'delivery': pin(ref['evidence']), 'packet': pin(SESSION/'packet.json'), 'queue_matches_packet': pin('docs/work/queue.json')['sha256'] == packet['queue_sha256'], 'ordered_delivery_count': len(delivery['artifacts']), 'original_prefix_count': len(old['artifacts']), 'original_ordered_prefix_equal': prefix, 'manifest_agreement': manifest_agreement, 'verified_pin_count': len(results), 'mismatches': [r for r in results if not r['matches']], 'all_passed': ok, 'results': results})
    print(json.dumps({'report': report, 'passed': ok, 'delivery_count':len(delivery['artifacts']), 'pins':len(results), 'mismatches':[r for r in results if not r['matches']]}))
    return 0 if ok else 1

def run(name):
    commands = {
        'sources-tests': ['.venv/Scripts/python.exe','-B','-m','pytest','-q','tests/sources','--basetemp','private/workflow/checks/rb02-e259028c-s1','-p','no:cacheprovider','--tb=short'],
        'repository-check': ['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02'],
        'root-inventory': ['.venv/Scripts/python.exe','-B','-m','wgc.sources','validate',(BASE/'final-verified/inventory.json').as_posix()],
        'workflow-validate': ['.venv/Scripts/python.exe','-B','scripts/workflow.py','validate'],
        'diff-check': ['git','diff','--check'],
        'original-pages': ['pdftoppm','-f','5','-l','8','-r','144','-png','private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf',(OUT/'original').as_posix()],
    }
    command=commands[name]
    assert not (OUT/(name+'.json')).exists()
    if name == 'sources-tests':
        assert not Path(command[7]).exists(), 'Fresh basetemp required'
    started=datetime.now(timezone.utc).isoformat()
    clock=time.monotonic()
    with (OUT/(name+'.stdout')).open('xb') as stdout, (OUT/(name+'.stderr')).open('xb') as stderr:
        result=subprocess.run(command,stdout=stdout,stderr=stderr,check=False)
    record={'name':name,'command':command,'exit_code':result.returncode,'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-clock,'stdout':pin(OUT/(name+'.stdout')),'stderr':pin(OUT/(name+'.stderr'))}
    write(name+'.json',record)
    print(json.dumps(record))
    return result.returncode

def environment():
    t=read(PREP/'toolchain.json')
    libraries={n:importlib.metadata.version(n) for n in ['pypdf','pdfplumber','Pillow','pytest','reportlab']}
    assert os.environ.get('PYTHONPATH') == t['process_pythonpath']
    assert t['process_path_prefix'].lower() in os.environ['PATH'].lower()
    print(json.dumps(write('environment.json',{'python':sys.version,'python_executable':pin(sys.executable),'PYTHONPATH':os.environ.get('PYTHONPATH'),'process_path_prefix_present':True,'resolved_tools':{n:pin(shutil.which(n)) for n in ['pdfinfo','pdftoppm','pwsh','git']},'libraries':libraries,'toolchain':pin(PREP/'toolchain.json'),'environment_changes':[]})))

if __name__ == '__main__':
    if sys.argv[1]=='verify': sys.exit(verify(sys.argv[2]))
    if sys.argv[1]=='run': sys.exit(run(sys.argv[2]))
    if sys.argv[1]=='environment': environment()
