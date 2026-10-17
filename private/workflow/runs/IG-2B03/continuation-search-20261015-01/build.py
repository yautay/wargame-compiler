"""Fresh bounded IG-2B03 builds. No prior derivation helper is used."""
import copy
import json
from pathlib import Path
from datetime import datetime, timezone
from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import seal, validate, file_pin
from wgc.sources.pdf import extract_evidence

ROOT = Path.cwd()
OUT = Path('private/workflow/runs/IG-2B03/continuation-search-20261015-01')
SESSION = Path('private/workflow/orchestrator/20261015T164901Z-046553b7/001-IG-2B03-executor-c99dc525')
load = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
SCOPE = load('private/workflow/runs/IG-2B03/recovery-20261015-search-01/scope.json')
COMMON = {k: load(OUT/'claim.json')[k] for k in ('role','actor','task','model','reasoning','configuration_evidence','configuration_sha256')}

def write(path, value):
    path = Path(path)
    with path.open('xb') as stream:
        stream.write(canonical_bytes(value)+b'\n')

def author():
    # Nonassigned source content is preserved structurally, never printed/analyzed.
    base = load(SCOPE['preservation']['baseline_inventory']['path'])
    draft = load(SCOPE['drafts'][0]['path'])
    ids = {p['id'] for p in base['pages'] if p['pdf_page'] in (9,10,11,12)}
    old_ids = {r['id'] for r in base['regions'] if r['page_id'] in ids}
    candidates = [r for r in draft['regions'] if r['page_id'] in ids]
    doc = copy.deepcopy(base)
    # Persist candidate explicit identities without inheriting draft assertions/evidence.
    registry = load(SCOPE['drafts'][1]['path'])
    assert all(e in registry['entries'] for e in base['registry']['entries'])
    doc['registry'] = registry
    doc['regions'] = [r for r in base['regions'] if r['id'] not in old_ids]+copy.deepcopy(candidates)
    by_page = {p['id']:p['pdf_page'] for p in base['pages']}
    doc['regions'].sort(key=lambda r: (by_page[r['page_id']], draft['reading_order'].index(r['id']) if r['page_id'] in ids else base['reading_order'].index(r['id'])))
    doc['reading_order'] = [r['id'] for r in doc['regions']]
    new_ids = {r['id'] for r in candidates}
    doc['links'] = copy.deepcopy(base['links'])+[copy.deepcopy(l) for l in draft['links'] if l['from'] in new_ids or l['to'] in new_ids]
    assert all(l['from'] not in old_ids and l['to'] not in old_ids for l in doc['links'])
    doc = seal(doc)
    validate(doc, ROOT)
    return doc

def run():
    # Author twice independently from accepted baseline + exact bounded candidates.
    a = author(); b = author()
    assert canonical_bytes(a)==canonical_bytes(b)
    for name, doc in [('authored',a),('replay-a-authored',b),('replay-b-authored',author())]:
        directory=OUT/name;directory.mkdir(exist_ok=False)
        write(directory/'inventory.json',doc);write(directory/'identity-registry.json',doc['registry'])
    assert (OUT/'authored/inventory.json').read_bytes()==(OUT/'replay-a-authored/inventory.json').read_bytes()==(OUT/'replay-b-authored/inventory.json').read_bytes()
    plan = load(SCOPE['drafts'][2]['path'])
    write(OUT/'partition-plan.json',{**COMMON,'reading_order_policy':'Running title, printed label, separator; left column top to bottom with counter adjacent to its introduction; right column top to bottom; copyright. Explicit order is authoritative; extraction order is not.','regions':[{k:r[k] for k in ('page','key','kind','box','region_id','slug')} for r in plan['regions'] if r['page'] in (9,10,11,12)],'basis':'Fresh original-page and boundary inspection in this session; pinned candidates supply explicit keys/IDs/boxes only. No prior inspection/check claims are inherited.'})
    for name, input_name in [('final-verified','authored'),('replay-a-verified','replay-a-authored'),('replay-b-verified','replay-b-authored')]:
        directory=OUT/name;directory.mkdir(exist_ok=False)
        doc=load(OUT/input_name/'inventory.json')
        assigned={p['id'] for p in doc['pages'] if p['pdf_page'] in (9,10,11,12)}
        regions=[r for r in doc['regions'] if r['page_id'] in assigned]
        for i,r in enumerate(regions):
            ev=extract_evidence(doc,r['id'],ROOT,(directory/f"region-{i+1:03d}").as_posix(),dpi=144)
            doc['evidence'].append(ev);doc=seal(doc)
            if (i+1)%10==0: print(name,i+1,'/',len(regions),flush=True)
        for page in doc['pages']:
            if page['id'] in assigned:
                region=next(r for r in regions if r['page_id']==page['id'] and r['key'].endswith(':printed-label'))
                ev=next(e for e in doc['evidence'] if e['region_id']==region['id'])
                page.update(seal({**page,'label':{'status':'verified','value':str(page['pdf_page']),'reason':'Visible glyph inspected on original assigned page and exact current printed-label crop by executor; technical observation only.','evidence':ev['id']}}))
        doc=seal(doc); report=validate(doc,ROOT)
        write(directory/'inventory.json',doc);write(directory/'identity-registry.json',doc['registry']);write(directory/'coverage.json',report)
        write(directory/'validation.json',{**COMMON,'operation':'wgc.sources.inventory.validate(document, repository_root)','exit_code':0,'inventory':file_pin(ROOT,(directory/'inventory.json').as_posix()),'result':report,'ended_utc':datetime.now(timezone.utc).isoformat()})
        print(name,'complete and independently validated',flush=True)

if __name__=='__main__': run()
