"""Preserve accepted region-array order in all unfrozen current-attempt builds."""
import copy
from build import ROOT, OUT, SCOPE, COMMON, load
from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import seal, validate, file_pin
from wgc.sources.geometry import box_to_pdf, render_size_pixels
from PIL import Image

base=load(SCOPE['preservation']['baseline_inventory']['path'])
assigned={p['id'] for p in base['pages'] if p['pdf_page'] in (9,10,11,12)}
old=[r for r in base['regions'] if r['page_id'] not in assigned]

def normalize(doc):
    by_id={r['id']:r for r in doc['regions']}
    # Preserve exact inherited records and their array order, not merely their set.
    assert all(by_id[r['id']]==r for r in old)
    inherited={r['id'] for r in old}
    doc['regions']=copy.deepcopy(old)+[r for r in doc['regions'] if r['id'] not in inherited]
    return seal(doc)

def put(path,obj):path.write_bytes(canonical_bytes(obj)+b'\n')

for name in ('authored','replay-a-authored','replay-b-authored'):
    path=OUT/name/'inventory.json';put(path,normalize(load(path)))
for name in ('final-verified','replay-a-verified','replay-b-verified','components','components-replay-a','components-replay-b'):
    directory=OUT/name
    if name.startswith('components'):
        path=directory/'authored-inventory.json';put(path,normalize(load(path)))
    path=directory/'inventory.json';before=load(path);doc=normalize(before)
    assert {r['id']:r for r in before['regions']}=={r['id']:r for r in doc['regions']}
    assert doc['evidence']==before['evidence'] and doc['reading_order']==before['reading_order']
    report=validate(doc,ROOT);put(path,doc)
    vp=directory/'validation.json';v=load(vp);v['inventory']=file_pin(ROOT,path.as_posix());v['result']=report
    v['postprocessing']='Accepted inherited region-array order restored before freeze; individual region/page/evidence records, exact evidence artifact bytes, explicit IDs and reading-order list are unchanged. Complete repository-root validation was rerun.'
    put(vp,v)
    if not name.startswith('components'):put(directory/'coverage.json',{**COMMON,**report})
    print(name,'accepted array order restored; complete current evidence validation passed',flush=True)
assert (OUT/'authored/inventory.json').read_bytes()==(OUT/'replay-a-authored/inventory.json').read_bytes()==(OUT/'replay-b-authored/inventory.json').read_bytes()
assert (OUT/'components/authored-inventory.json').read_bytes()==(OUT/'components-replay-a/authored-inventory.json').read_bytes()==(OUT/'components-replay-b/authored-inventory.json').read_bytes()
doc=load(OUT/'components/inventory.json');ledger=load(OUT/'component-ledger.json')
for c in ledger['components']:
    region=next(r for r in doc['regions'] if r['id']==c['region_id'])
    page=next(p for p in doc['pages'] if p['id']==region['page_id'])
    ev=next(e for e in doc['evidence'] if e['region_id']==c['region_id'])
    with Image.open(ev['image']['path']) as image:actual=list(image.size)
    expected=list(render_size_pixels(region['box'],page,ev['render_parameters']['dpi']))
    assert actual==expected
    c.update(region=region,evidence=ev,native_pdf_bounds_rational=[str(v) for v in box_to_pdf(region['box'],page)],predicted_pixels=expected,actual_png_pixels=actual)
put(OUT/'component-ledger.json',ledger)
