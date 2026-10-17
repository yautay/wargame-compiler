"""Read-only exhaustive frozen-envelope/index/configuration integrity check."""
import json
from build_inventory import ROOT,SESSION,TASK,load,pin,old_preservation,metadata

delivery=load(ROOT/'delivery.json');meta=metadata()
for k,v in meta.items():assert delivery[k]==v
paths=[p['path'] for p in delivery['artifacts']]
assert paths==sorted(set(paths))
for p in delivery['artifacts']:assert pin(p['path'])==p
assert set(TASK['outputs'])<=set(paths)
index=load(ROOT/'source-pins.json')
indexed={p['path']:p for p in index['artifacts']+index['current_reports']}
frozen={p['path']:p for p in delivery['artifacts']}
assert all(frozen.get(path)==p for path,p in indexed.items())
for name in ('final-verified','replay-1','replay-2'):
    doc=load(ROOT/name/'inventory.json')
    assert doc['registry']==load(ROOT/name/'identity-registry.json')
    for e in doc['evidence']:
        for field in ('crop_pdf','text','image'):
            p=e[field];assert indexed.get(p['path'])==p
assert old_preservation()==7808
print(json.dumps({'frozen_delivery_integrity':'pass','artifact_count':len(paths),'source_index_count':len(indexed),'preserved_input_artifacts':7808,'delivery':pin(ROOT/'delivery.json')}))
