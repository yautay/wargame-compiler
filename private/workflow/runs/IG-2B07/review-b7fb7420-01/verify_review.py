import copy
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / 'private/workflow/runs/IG-2B07/review-b7fb7420-01'
CURRENT = ROOT / 'private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01'
PRIOR = ROOT / 'private/workflow/runs/IG-2B07/inventory-25-28-01'
META = {k: v for k, v in json.loads((OUT/'checkpoint.json').read_text()).items()
        if k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256')}

def load(p):
    return json.loads(p.read_text(encoding='utf-8'))

def pin(p):
    b = p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def save(name, **data):
    (OUT/name).write_text(json.dumps(dict(META, **data), indent=2)+'\n', encoding='utf-8')

def norm(obj, prefix):
    if isinstance(obj, dict):
        return {k:norm(v,prefix) for k,v in obj.items()}
    if isinstance(obj, list):
        return [norm(v,prefix) for v in obj]
    if isinstance(obj, str) and obj.startswith(prefix+'/'):
        return '$RUN/'+obj[len(prefix)+1:]
    return obj

def structure():
    inv=load(CURRENT/'final-verified/inventory.json')
    old=load(PRIOR/'final-verified/inventory.json')
    checks={}
    def check(name, value):
        checks[name]=bool(value)
        assert value,name
    regions={x['id']:x for x in inv['regions']}
    oldregions={x['id']:x for x in old['regions']}
    added=set(regions)-set(oldregions)
    check('single_new_region',added=={'region:09f8cd5c-437e-4b82-b72f-686431bb9c6c'})
    check('all_prior_region_records_exact',all(regions[k]==v for k,v in oldregions.items()))
    check('pages_exact',inv['pages']==old['pages'])
    check('links_exact',inv['links']==old['links'])
    check('reading_order_preserved',[x for x in inv['reading_order'] if x not in added]==old['reading_order'])
    curprefix=(CURRENT/'final-verified').relative_to(ROOT).as_posix()
    oldprefix=(PRIOR/'final-verified').relative_to(ROOT).as_posix()
    ev={x['id']:x for x in inv['evidence']}
    check('prior_evidence_exact_after_prefix_normalization',all(norm(ev[x['id']],curprefix)==norm(x,oldprefix) for x in old['evidence']))
    reg=load(CURRENT/'final-verified/identity-registry.json')
    oldreg=load(PRIOR/'final-verified/identity-registry.json')
    bindings={x['id']:x for x in reg['entries']}
    check('all_old_registry_bindings_exact',all(bindings[x['id']]==x for x in oldreg['entries']))
    ledger=load(CURRENT/'region-ledger.json')['regions']
    comps=load(CURRENT/'component-ledger.json')['components']
    ids={x['region']['id'] for x in ledger}
    compids={x['region']['id'] for x in comps}
    check('189_complete_targets',len(ids)==len(ledger)==189)
    check('87_components',len(compids)==len(comps)==87)
    check('complete_ledger_region_and_evidence_equality',all(regions[x['region']['id']]==x['region'] and ev[x['evidence']['id']]==x['evidence'] for x in ledger))
    check('components_match_full_ledger',all(x in ledger or any({k:v for k,v in y.items() if k!='reading_order_index'}==x for y in ledger) for x in comps))
    check('all_components_context',all(x['region']['denominator_role']=='context' for x in comps))
    check('all_component_parents_and_boxes_valid',all(x['parent_region_id'] in regions and all(x['box'][j]>=regions[x['parent_region_id']]['box'][j] for j in (0,1)) and all(x['box'][j]<=regions[x['parent_region_id']]['box'][j] for j in (2,3)) for x in comps))
    cov=load(CURRENT/'coverage-report.json')
    inventory={k for k,v in regions.items() if v['denominator_role']=='inventory'}
    context=set(regions)-inventory
    check('full_inventory_849',len(inventory)==849 and inventory==set(cov['full_inventory_ids']))
    check('full_context_92',len(context)==92 and context==set(cov['full_context_ids']))
    check('assigned_inventory_100',len(cov['assigned_inventory_ids'])==100 and set(cov['assigned_inventory_ids'])=={x['region']['id'] for x in ledger if x['role']=='inventory'})
    check('941_total_regions',len(regions)==941)
    check('coverage_complete_sets',set(cov['new_nested_component_ids'])==compids and set(cov['new_boundary_ids'])==ids-compids-set(cov['assigned_inventory_ids']))
    cont=load(CURRENT/'continuations.json')
    check('continuation_complete_endpoints',{x['id'] for x in cont['endpoints']}==ids)
    check('continuation_endpoint_evidence_exact',all(x['evidence_id']==next(y['evidence']['id'] for y in ledger if y['region']['id']==x['id']) for x in cont['endpoints']))
    check('context_zero_denominator',cov['context_denominator_contribution']==0)
    for directory in ['replay-1','replay-2']:
        replay=load(CURRENT/directory/'inventory.json')
        normalized=norm(replay,(CURRENT/directory).relative_to(ROOT).as_posix())
        final=norm(inv,curprefix)
        normalized.pop('revision'); final.pop('revision')
        check(directory+'_complete_normalized_inventory_equal',normalized==final)
        check(directory+'_registry_exact',load(CURRENT/directory/'identity-registry.json')==reg)
    priorreview=load(ROOT/'private/workflow/runs/IG-2B07/review-3f57d66e-01/review.json')
    check('prior_complete_target_review_retained',set(priorreview['review_scope']['all_delivered_region_ids'])==ids-added)
    check('prior_complete_component_review_retained',set(priorreview['review_scope']['all_delivered_component_ids'])==compids-added)
    save('structure-verification.json',checks=checks,all_passed=True,new_region_ids=sorted(added),target_ids=sorted(ids),component_ids=sorted(compids),prior_review_attribution='Prior complete coverage revalidated against unchanged records and payload pins; fresh inspection separately recorded.')
    print(json.dumps(dict(all_passed=True,checks=len(checks),targets=len(ids),components=len(compids))))

def replay(number):
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject
    import pdfplumber
    from wgc.sources.geometry import box_to_pdf
    from PIL import Image
    inv=load(CURRENT/'final-verified/inventory.json')
    ledger=load(CURRENT/'region-ledger.json')['regions']
    source=ROOT/inv['source']['pdf']['path']
    assert pin(source)==inv['source']['pdf']
    reader=PdfReader(source, strict=True)
    directory=OUT/f'independent-replay-{number}'
    directory.mkdir(exist_ok=False)
    pages={x['id']:x for x in inv['pages']}
    rows=[]
    for row in ledger:
        r=row['region']; p=pages[r['page_id']]; key=r['key'].replace(':','-')
        writer=PdfWriter(); page=writer.add_page(reader.pages[p['pdf_page']-1])
        native=box_to_pdf(r['box'],p)
        page.mediabox=RectangleObject([float(v) for v in native]); page.cropbox=RectangleObject([float(v) for v in native])
        crop=directory/(key+'.pdf'); text=directory/(key+'.txt'); png=directory/(key+'.png')
        with crop.open('xb') as f: writer.write(f)
        with pdfplumber.open(crop) as doc:
            clipped=doc.pages[0].crop(doc.pages[0].bbox)
            value=clipped.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
        text.write_text(value,encoding='utf-8',newline='\n')
        subprocess.run(['pdftoppm','-f','1','-l','1','-singlefile','-cropbox','-r','144','-png',str(crop),str(png.with_suffix(''))],capture_output=True,check=True)
        actual=[pin(x) for x in [crop,text,png]]
        expected=[row['evidence'][k] for k in ['crop_pdf','text','image']]
        assert all((a['sha256'],a['bytes'])==(b['sha256'],b['bytes']) for a,b in zip(actual,expected)),key
        rows.append(dict(region_id=r['id'],page=p['pdf_page'],box=r['box'],outputs=actual,payloads_exact=True))
    assert pin(source)==inv['source']['pdf']
    save(f'independent-replay-{number}.json',command=' '.join(sys.argv),serial=True,worker_pools=False,complete_targets=len(rows),complete_set_equal={x['region_id'] for x in rows}=={x['region']['id'] for x in ledger},payloads_compared=len(rows)*3,all_passed=True,rows=rows)
    print(json.dumps(dict(replay=number,targets=len(rows),payloads=len(rows)*3,all_passed=True)))

if __name__=='__main__':
    if sys.argv[1]=='structure': structure()
    else: replay(int(sys.argv[1]))
