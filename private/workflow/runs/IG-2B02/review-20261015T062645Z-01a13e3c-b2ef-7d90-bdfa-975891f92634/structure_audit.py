from review_driver import *
from collections import Counter
from fractions import Fraction
from wgc.contracts.source import canonical_bytes,load_json
from wgc.sources.inventory import validate,page_basis_hash,seal
from pypdf import PdfReader
doc=load_json(D/'final-verified/inventory.json');base=load_json(B/'final-verified/inventory.json')
pages={p['id']:p for p in doc['pages']};regions={r['id']:r for r in doc['regions']}
new=[r for r in doc['regions'] if r['key'].startswith('ig2b02:')]
old={r['id']:r for r in base['regions']}
retired=[r for r in base['regions'] if r['key'] in [f'physical-page:{n}:unprocessed-placeholder' for n in range(5,9)]]
assert len(retired)==4 and len(new)==141
retired_ids={r['id'] for r in retired}
records=[]
for r in base['regions']:
    same=r['id'] in regions and regions[r['id']]==r
    assert same if r['id'] not in retired_ids else r['id'] not in regions
    records.append({'id':r['id'],'key':r['key'],'revision':r['revision'],'baseline_record_sha256':hashlib.sha256(canonical_bytes(r)).hexdigest(),'retired_membership_only':r['id'] in retired_ids,'exact_unchanged':same})
assert all(e in doc['registry']['entries'] for e in base['registry']['entries'])
assert len(doc['registry']['entries'])==len(base['registry']['entries'])+141
assert doc['registry']==load(D/'final-verified/identity-registry.json')==load(D/'authored/identity-registry.json')
assert len({r['key'] for r in new})==141
assert all(r['id']==next(e['id'] for e in doc['registry']['entries'] if e['kind']=='region' and e['key']==r['key']) for r in new)
old_evidence=[]
for ev in base['evidence']:
    assert ev in doc['evidence']
    pins=[ev[k] for k in ('text','image','crop_pdf')]
    for p in pins:assert pin(ROOT/p['path'])==p
    old_evidence.append({'id':ev['id'],'region_id':ev['region_id'],'exact_metadata':True,'pins':pins,'access':'Byte hashes only; no new source-content analysis.'})
assert doc['source']==base['source']
assert doc['links'][:len(base['links'])]==base['links']
assert [i for i in doc['reading_order'] if i in old and i not in retired_ids]==[i for i in base['reading_order'] if i not in retired_ids]
assert len(doc['reading_order'])==len(set(doc['reading_order']))==len(doc['regions']) and set(doc['reading_order'])==set(regions)
assert doc['revision']==seal(doc)['revision']
source=ROOT/doc['source']['pdf']['path'];before=pin(source)
reader=PdfReader(source,strict=True)
assert len(reader.pages)==44
geometry=[]
for n,raw in enumerate(reader.pages,1):
    p=next(p for p in doc['pages'] if p['pdf_page']==n);bp=next(p for p in base['pages'] if p['pdf_page']==n)
    media=[int(Fraction(str(v))*1000000) for v in raw.mediabox];crop=[int(Fraction(str(v))*1000000) for v in raw.cropbox]
    actual={'media_box':media,'crop_box':crop,'effective_crop_box':[max(media[0],crop[0]),max(media[1],crop[1]),min(media[2],crop[2]),min(media[3],crop[3])],'rotation':raw.rotation%360,'user_unit':{'numerator':Fraction(str(raw.get('/UserUnit',1))).numerator,'denominator':Fraction(str(raw.get('/UserUnit',1))).denominator}}
    assert all(p[k]==v==bp[k] for k,v in actual.items())
    assert all(p[k]==bp[k] for k in ('id','key','pdf_page','source_revision'))
    assert p['revision']==seal(p)['revision']
    if n not in range(5,9):assert p==bp
    else:assert p['label']['value']==str(n) and next(e for e in doc['evidence'] if e['id']==p['label']['evidence'])['pdf_page']==n
    geometry.append({'pdf_page':n,'id':p['id'],'key':p['key'],'actual':actual,'page_basis_hash':page_basis_hash(p),'baseline_unchanged':p==bp,'revision':p['revision']})
assert before==pin(source)
pop=run('08-independent-poppler-all-page-boxes',[POP/'pdfinfo.EXE','-f','1','-l','44','-box',source])
poptext=(ROOT/pop['stdout']['path']).read_text(encoding='utf-8')
import re
assert re.search(r'^Pages:\s+44\s*$',poptext,re.M)
for g in geometry:
    n=g['pdf_page']
    for key,pdfkey in [('media_box','MediaBox'),('crop_box','CropBox')]:
        match=re.search(r'^Page\s+'+str(n)+r'\s+'+pdfkey+r':\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)',poptext,re.M)
        assert match,(n,pdfkey)
        assert [int(Fraction(v)*1000000) for v in match.groups()]==g['actual'][key]
    match=re.search(r'^Page\s+'+str(n)+r'\s+rot:\s+(\d+)',poptext,re.M)
    assert match and int(match[1])==g['actual']['rotation']
write('preservation-audit.json',{'outcome':'passed','baseline':pin(B/'final-verified/inventory.json'),'registry_baseline':pin(B/'final-verified/identity-registry.json'),'all_old_regions':records,'old_evidence':old_evidence,'all_44_page_geometry':geometry,'old_links':base['links'],'old_links_exact':True,'old_relative_order_exact':True,'old_registry_entries':base['registry']['entries'],'old_registry_entries_exact':True,'retired_memberships':[r['id'] for r in retired],'retired_registry_entries_retained':True,'source_metadata_exact':True,'independent_poppler_check':pop,'source_before':before,'source_after':pin(source)})
counts=Counter(pages[r['page_id']]['pdf_page'] for r in new);assert counts=={5:39,6:33,7:39,8:30}
assert sum(r['denominator_role']=='inventory' for r in doc['regions'])==307
contexts=[r for r in doc['regions'] if r['denominator_role']=='context'];assert len(contexts)==1
assert contexts[0]==old['region:e8d77349-41ce-47d0-b678-eab1d0c8e8ed']
for r in new:
    assert r['revision']==seal(r)['revision'] and r['denominator_role']=='inventory'
    assert r['coverage']['transcription']['status']=='partial'
    for level,c in r['coverage'].items():
        assert c['gap'] and c['reason'] and c['boundary'] is None
        if level!='transcription':assert c['status']=='unprocessed'
complement=[];submitted=load(D/'geometric-gaps.json')['assigned_page_complement']
for n in range(5,9):
    boxes=[r['box'] for r in new if pages[r['page_id']]['pdf_page']==n]
    def area(b):return (b[2]-b[0])*(b[3]-b[1])
    def overlap(a,b):return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
    assert all(not overlap(a,b) for i,a in enumerate(boxes) for b in boxes[i+1:])
    xs=sorted({0,1000000,*[v for b in boxes for v in (b[0],b[2])]});gaps=[]
    for x0,x1 in zip(xs,xs[1:]):
        ys=sorted((b[1],b[3]) for b in boxes if b[0]<=x0 and b[2]>=x1);cursor=0
        for y0,y1 in ys:
            if cursor<y0:gaps.append([x0,cursor,x1,y0])
            cursor=max(cursor,y1)
        if cursor<1000000:gaps.append([x0,cursor,x1,1000000])
    claimed=next(c for c in submitted if c['pdf_page']==n)
    for b in claimed['rectangles']:
        assert 0<=b[0]<b[2]<=1000000 and 0<=b[1]<b[3]<=1000000
        assert not any(overlap(b,occupied) for occupied in boxes)
    assert all(not overlap(a,b) for i,a in enumerate(claimed['rectangles']) for b in claimed['rectangles'][i+1:])
    a=sum(map(area,gaps));assert a==sum(map(area,claimed['rectangles']))==claimed['unaccounted_area_trillionths']==10**12-sum(map(area,boxes))
    complement.append({'pdf_page':n,'method':'Independent x-axis slab decomposition; submitted y-axis complement checked disjoint/bounded/unoccupied with equal complete area.','rectangles':gaps,'unaccounted_area_trillionths':a,'inventory_area_trillionths':sum(map(area,boxes))})
write('denominator-audit.json',{'outcome':'passed','task_counts_by_physical_page':dict(counts),'task_denominator':141,'full_denominator':307,'preserved_authored':130,'unchanged_placeholders':36,'context_regions':1,'context_denominator':0,'new_coverage':{level:dict(Counter(r['coverage'][level]['status'] for r in new)) for level in new[0]['coverage']},'geometric_complement':complement,'source_completeness':'Assessed separately through full visual ledger review. Arithmetic and geometric complement do not prove content completeness.','representation':'All new transcription partial; descriptive/formal unprocessed; no approved exclusion, source-IG reconciliation, human acceptance or executable readiness.'})
checkpoint('structural_and_preservation',['Input/runtime gate','Original-first observations','Independent all-44-page geometry/counts','Every prior record/evidence/link/registry/order preserved','Denominators/coverage/geometric complement'], 'Reproduce every exact new locator; inspect every region and grouped component.')
print('STRUCTURAL/PRESERVATION/DENOMINATOR PASS',len(new),len(old_evidence))
