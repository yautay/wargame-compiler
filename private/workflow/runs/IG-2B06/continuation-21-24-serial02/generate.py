"""Serial complete task evidence derivation; no worker pools or inherited evidence."""
import argparse
import copy
import datetime
import json
from pathlib import Path
import time

from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import assemble, file_pin, seal, validate, page_basis_hash
from wgc.sources.pdf import extract_evidence

ROOT = Path.cwd()
RUN = Path('private/workflow/runs/IG-2B06/continuation-21-24-serial02')
parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True, choices=['replay-a','replay-b','final-verified'])
args = parser.parse_args()
start = time.perf_counter()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
meta = {k: json.loads((RUN/'claim.json').read_text())[k] for k in
        ('role','actor','model','reasoning','configuration_evidence','configuration_sha256','task')}
inventory_path = RUN/'authored/inventory.json'
registry_path = RUN/'authored/identity-registry.json'
doc = json.loads(inventory_path.read_text())
registry = json.loads(registry_path.read_text())
assert doc['registry'] == registry
input_pin = file_pin(ROOT, inventory_path.as_posix())
registry_pin = file_pin(ROOT, registry_path.as_posix())
validate(doc, ROOT)
out = RUN/args.output
out.mkdir(exist_ok=False)
new_evidence = []
chosen = [r for r in doc['regions'] if r['key'].startswith('ig2b06:')]
assert len(chosen) == 114
by_id = {r['id']:r for r in chosen}
chosen = [by_id[rid] for rid in doc['reading_order'] if rid in by_id]
for index, region in enumerate(chosen):
    # A bounded validation view carries the unchanged full 44-page source geometry,
    # full persisted registry and exact current region. This avoids reopening 622
    # unrelated immutable evidence triples for each crop. Full input and assembled
    # output validations still run unchanged with actual source/artifact checks.
    geometry_pages = copy.deepcopy(doc['pages'])
    for p in geometry_pages:
        p['label'] = {'status':'unknown','value':None,'reason':'Geometry-only extraction view makes no printed-label verification claim.','evidence':None}
    geometry_pages = [seal(p) for p in geometry_pages]
    assert [page_basis_hash(p) for p in geometry_pages] == [page_basis_hash(p) for p in doc['pages']]
    view = assemble(doc['source'], geometry_pages, [region], registry,
                    reading_order=[region['id']], links=[], evidence=[], toolchain=doc['toolchain'])
    assert view['regions'][0] == region and view['registry'] == registry
    ev = extract_evidence(view, region['id'], ROOT, f'{out.as_posix()}/region-{index:03d}', dpi=144)
    page = next(p for p in doc['pages'] if p['id'] == region['page_id'])
    assert ev['region_revision'] == region['revision'] and ev['box'] == region['box']
    assert ev['page_basis_hash'] == page_basis_hash(page)
    new_evidence.append(ev)
    if (index+1) % 10 == 0 or index+1 == len(chosen):
        print(json.dumps({'output':args.output,'completed':index+1,'total':len(chosen),'elapsed_seconds':round(time.perf_counter()-start,2)}), flush=True)
doc['evidence'].extend(new_evidence)
doc = seal(doc)
coverage = validate(doc, ROOT)
assert file_pin(ROOT, inventory_path.as_posix()) == input_pin
assert file_pin(ROOT, registry_path.as_posix()) == registry_pin
(out/'inventory.json').write_bytes(canonical_bytes(doc)+b'\n')
(out/'identity-registry.json').write_bytes(canonical_bytes(registry)+b'\n')
(out/'coverage.json').write_bytes(canonical_bytes(coverage)+b'\n')
report = {**meta,'summary':'Complete serial fresh evidence generation from the same pre-evidence full authored inventory and persisted registry.',
          'command':f'.venv/Scripts/python.exe {RUN.as_posix()}/generate.py --output {args.output}',
          'exit_code':0,'input_inventory':input_pin,'input_registry':registry_pin,
          'output_inventory':file_pin(ROOT,(out/'inventory.json').as_posix()),
          'output_registry':file_pin(ROOT,(out/'identity-registry.json').as_posix()),
          'assigned_region_count':112,'context_region_count':2,'complete_region_ids':[r['id'] for r in chosen],
          'full_input_validation':True,'full_output_validation':True,'bounded_extraction_views_preserve_full_page_registry_and_region_bases':True,
          'extraction_view_labels':'Unknown in temporary views only, because original label evidence is outside the one-region extraction view. Full input/output page records and label evidence are unchanged and validated.',
          'execution_mode':'Serial calls to installed extract_evidence in this Python process; ordinary Poppler CLI children only.',
          'started_utc':started,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.perf_counter()-start,3)}
(out/'generation-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':args.output,'exit_code':0,'elapsed_seconds':report['elapsed_seconds']}),flush=True)
