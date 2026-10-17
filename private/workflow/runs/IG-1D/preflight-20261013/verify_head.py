"""Verify indexed current exporter reproduces the full audited canonical package."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,time
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'src'))
from wgc.export.source import build
from wgc.contracts.source import canonical_bytes,load_json
R=Path(__file__).parent
start=datetime.now(timezone.utc);clock=time.monotonic()
report=json.loads((R/'full-export-accounting.json').read_text(encoding='utf-8'))
package=Path(report['package']['package'])
registry=load_json(package/'identity-registry.json');bundle=load_json(package/'source-ig.json')
imported=load_json(Path('private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json'))
ip=Path('private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json')
sp=Path('private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json')
result=build(imported,registry,previous_bundle=bundle,namespace='wgu.spqr',source_manifest=load_json(sp),
    input_manifest_sha256=hashlib.sha256(ip.read_bytes()).hexdigest(),source_manifest_sha256=hashlib.sha256(sp.read_bytes()).hexdigest())
checks=[]
for key,name in [('bundle','source-ig.json'),('registry','identity-registry.json'),('references','references.json')]:
    raw=canonical_bytes(result[key])+b'\n';assert raw==(package/name).read_bytes(),name
    checks.append({'path':str(package/name),'sha256':hashlib.sha256(raw).hexdigest(),'current_indexed_export_byte_identical':True})
out={'result':'pass','started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
     'wall_seconds':time.monotonic()-clock,'canonical_files':checks,'source_graph_record_count':len(result['bundle']['records']),
     'semantic_acceptance_granted':False,'source_coverage_granted':False,'executable_readiness_granted':False,'tokens':None,'cost':None}
with (R/'current-head-reproducibility.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
