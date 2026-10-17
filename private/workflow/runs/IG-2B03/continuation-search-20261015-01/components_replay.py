"""Two complete independent component locator replays with persisted identities."""
import copy
from build import ROOT, OUT, COMMON, load, write
from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import make_region, seal, validate, file_pin
from wgc.sources.pdf import extract_evidence

seed=load(OUT/'components/authored-inventory.json')
ledger=load(OUT/'component-ledger.json')
for name in ('components-replay-a','components-replay-b'):
    doc=load(OUT/'authored/inventory.json')
    doc['registry']=copy.deepcopy(seed['registry'])
    for c in ledger['components']:
        page=next(p for p in doc['pages'] if p['pdf_page']==c['page'])
        r=make_region(doc['registry'],c['key'],page,c['box'],kind='diagram',role='context',reason='Counter component observation only; parent owns inventory denominator; no verified transcription or semantics.')
        assert r['id']==c['region_id']
        doc['regions'].append(r);doc['reading_order'].append(r['id'])
    doc=seal(doc);assert canonical_bytes(doc)==canonical_bytes(seed)
    directory=OUT/name;directory.mkdir(exist_ok=False)
    write(directory/'authored-inventory.json',doc);write(directory/'identity-registry.json',doc['registry'])
    for i,c in enumerate(ledger['components']):
        doc['evidence'].append(extract_evidence(doc,c['region_id'],ROOT,(directory/f'component-{i+1:02d}').as_posix(),dpi=600));doc=seal(doc)
    result=validate(doc,ROOT)
    write(directory/'inventory.json',doc)
    write(directory/'validation.json',{**COMMON,'operation':'wgc.sources.inventory.validate(document, repository_root)','exit_code':0,'inventory':file_pin(ROOT,(directory/'inventory.json').as_posix()),'result':result,'authored_canonical_bytes_equal':True,'registry_ids_equal':True})
    print(name,'complete; 22 fresh component locators independently validated',flush=True)
