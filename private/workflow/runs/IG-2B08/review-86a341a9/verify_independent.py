"""Independent internal verification; releases counts only, no source closure."""
import collections
import copy
import hashlib
import json
import pathlib
from PIL import Image

ROOT=pathlib.Path('private/workflow/runs/IG-2B08/review-86a341a9')
PRODUCT=pathlib.Path('private/workflow/runs/IG-2B08/repair-F01-manifest02')
SESSION=pathlib.Path('private/workflow/orchestrator/20261017T111422Z-80dfde30/001-IG-2B08-reviewer-86a341a9')
def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def pin(p):
    p=pathlib.Path(p);return dict(path=p.as_posix(),sha256=sha(p),bytes=p.stat().st_size)
def meta():return dict(role='reviewer',actor='ig2:001-IG-2B08-reviewer-86a341a9:reviewer',model='gpt-6.1-sol',reasoning='high',configuration_evidence=(SESSION/'runtime-configuration.json').as_posix(),configuration_sha256=sha(SESSION/'runtime-configuration.json'))
def checkpins(rows):
    for r in rows:
        p=pathlib.Path(r['path']);assert p.is_file()
        assert sha(p)==r['sha256']
        if 'bytes' in r:assert p.stat().st_size==r['bytes']
    return len(rows)

delivery=load(PRODUCT/'delivery.json')
preserve=load('private/workflow/runs/IG-2B08/validation-context-recovery-20261017-01/preserve-manifest.json')
counts={'delivery_artifacts':checkpins(delivery['artifacts']),'preserved_artifacts':checkpins(preserve['artifacts'])}
assert len({x['path'] for x in delivery['artifacts']})==len(delivery['artifacts'])
frozen={x['path']:x for x in delivery['artifacts']}
pr=load(PRODUCT/'preservation-report.json')
checkpins([pr['baseline'],pr['baseline_registry']])
# Dependency source objects are compared internally only; none are emitted.
before=load(pr['baseline']['path']);before_registry=load(pr['baseline_registry']['path'])
assert before['registry']==before_registry
doc=load(PRODUCT/'final-verified/inventory.json')
retired=set(load(SESSION/'task.json')['inventory_contract']['placeholder_target_ids'])
bm={r['id']:r for r in before['regions']};fm={r['id']:r for r in doc['regions']}
assert set(bm)-set(fm)==retired
assert all(fm[k]==r for k,r in bm.items() if k not in retired)
assert before['source']==doc['source'] and before['pages']==doc['pages']
assert len(doc['pages'])==44
assert doc['evidence'][:len(before['evidence'])]==before['evidence']
assert doc['links'][:len(before['links'])]==before['links']
retained=[x for x in before['reading_order'] if x not in retired]
assert [x for x in doc['reading_order'] if x in bm]==retained
assert all(x in doc['registry']['entries'] for x in before_registry['entries'])
assert doc['registry']==load(PRODUCT/'final-verified/identity-registry.json')
counts.update(preserved_regions=len(bm)-4,preserved_evidence=len(before['evidence']),preserved_links=len(before['links']),preserved_registry_entries=len(before_registry['entries']),retained_reading_order=len(retained))
assert digest(retained)==pr['retained_reading_order_hash']
rows=load(PRODUCT/'region-ledger.json')['new_observations']
components=load(PRODUCT/'component-ledger.json')['components']
newids={r['region_id'] for r in rows};assert newids==set(fm)-set(bm)
assert len(newids)==269
assert len({r['region_id'] for r in components})==189
assert all(r['region_id'] in newids for r in components)
for r in rows:
    region=fm[r['region_id']]
    assert region['box']==r['box'] and region['revision']==r['revision']
    assert region['denominator_role']==r['role']
    assert next(e for e in doc['evidence'] if e['region_id']==r['region_id'])==r['evidence']
for r in components:
    assert all(r[k]==next(v for v in rows if v['region_id']==r['region_id'])[k] for k in ['points','box','evidence','revision','key'])
primary=[r for r in rows if r['role']=='inventory']
assert len(primary)==183
for r in rows:
    assert r['points'][0]<r['points'][2] and r['points'][1]<r['points'][3]
for i,a in enumerate(primary):
    for b in primary[i+1:]:
        if a['page']==b['page']:
            x0,y0,x1,y1=a['box'];u0,v0,u1,v1=b['box']
            assert max(x0,u0)>=min(x1,u1) or max(y0,v0)>=min(y1,v1)
context=next(r for r in rows if r['page']==33)
assert context['points']==[45,50,306,80] and context['role']=='context'
assert context['box']==[73529,63131,500000,101011]
assert fm['region:720a5d03-c721-469b-8a5e-2b91cb653a02']==bm['region:720a5d03-c721-469b-8a5e-2b91cb653a02']
indexes=load(PRODUCT/'source-pins.json');indexed={a['path']:a for a in indexes['artifacts']}
checkpins(indexes['artifacts']);checkpins(indexes['current_reports'])
assert all(a==frozen[p] for p,a in indexed.items())
assert all(a==frozen[a['path']] for a in indexes['current_reports'])
def normal_evidence(document,name):
    result=[]
    for e in document['evidence']:
        if e['region_id'] not in newids:continue
        e=copy.deepcopy(e);e.pop('id')
        for k in ['crop_pdf','image','text']:
            a=e[k];assert a==frozen[a['path']] and a==indexed[a['path']]
            a['path']=a['path'].replace((PRODUCT/name).as_posix(),'RUN')
        result.append(e)
    return result
normalized=normal_evidence(doc,'final-verified');runs=[]
for name in ['final-verified','replay-1','replay-2']:
    d=load(PRODUCT/name/'inventory.json')
    assert d['regions']==doc['regions'] and d['reading_order']==doc['reading_order'] and d['links']==doc['links']
    assert d['registry']==doc['registry']==load(PRODUCT/name/'identity-registry.json')
    assert normal_evidence(d,name)==normalized
    indexset=next(x for x in indexes['region_evidence_sets'] if x['name']==name)
    assert set(indexset['region_ids'])==newids
    assert len([e for e in d['evidence'] if e['region_id'] in newids])==269
    runs.append({'name':name,'inventory':pin(PRODUCT/name/'inventory.json'),'new_region_count':269,'evidence_artifacts':807,'normalized_evidence_digest':digest(normalized)})
for p in [29,30,31,32]:
    assert sha(ROOT/f'originals/page-{p}.png')==sha(PRODUCT/f'originals/page-{p}.png')
    assert (PRODUCT/f'originals/page-{p}.png').as_posix() in indexed
cov=load(PRODUCT/'coverage-report.json')
assert cov['full_page_count']==44 and cov['denominator_regions']==1028
assert cov['assigned_four_page']['denominator_regions']==183
assert cov['inherited_nonassigned']['denominator_regions']==845
assert cov['context_only']['denominator_contribution']==0 and cov['context_regions']==178
assert cov['semantic_acceptance_granted'] is False and cov['executable_readiness']=='unverified'
counts.update(new_regions=269,primary_regions=183,new_context_regions=86,component_entries=189,source_index_artifacts=len(indexed),current_reports=len(indexes['current_reports']))

# Source-bound F02 probe. The red/yellow digit stem below the green counter
# is visible to the right of the declared right edge. Count its full patch.
im=Image.open(ROOT/'originals/page-29.png').convert('RGB')
window=[130,513,138,523]
mask=[]
for y in range(window[1]*2,window[3]*2):
    for x in range(window[0]*2,window[2]*2):
        red,green,blue=im.getpixel((x,y))
        if red>190 and blue<110 and green<240:mask.append((x,y))
assert mask
probe=[]
for name in ['final-verified','replay-1','replay-2']:
    d=load(PRODUCT/name/'inventory.json')
    r=next(r for r in d['regions'] if r['key']=='ig2b08:p29:collapse-diagram-component-c-hits')
    x0,y0,x1,y1=r['box'];points=[x0*612/1e6,y0*792/1e6,x1*612/1e6,y1*792/1e6]
    missing=[(x,y) for x,y in mask if not(points[0]<=x/2<points[2] and points[1]<=y/2<points[3])]
    assert missing
    ev=next(e for e in d['evidence'] if e['region_id']==r['id'])
    probe.append({'run':name,'region_id':r['id'],'revision':r['revision'],'box':r['box'],'intended_detail_image':ev['image'],'missing_visible_stem_pixels':len(missing),'missing_pixel_bounds':[min(x for x,y in missing),min(y for x,y in missing),max(x for x,y in missing)+1,max(y for x,y in missing)+1]})
arrow_original=Image.open(ROOT/'originals/page-30.png').convert('RGB')
def cyan(rgb):
    red,green,blue=rgb;t=(255-red)/213
    return t>.12 and abs(green-(255-58*t))<8 and abs(blue-(255-11*t))<8
arrow_masks={}
for label,box in {'left_curve_head':[92,365,111,400],'right_curve_head':[122,344,143,382],'black_forward':[109,425,131,463]}.items():
    predicate=cyan if 'curve' in label else lambda rgb:max(rgb)<80
    pixels=[(x,y) for y in range(box[1]*2,box[3]*2) for x in range(box[0]*2,box[2]*2) if predicate(arrow_original.getpixel((x,y)))]
    assert len(pixels)>50
    arrow_masks[label]=pixels
def contains(points,pixel):
    x,y=pixel;return points[0]<=x/2 and (x+1)/2<=points[2] and points[1]<=y/2 and (y+1)/2<=points[3]
assert any(not contains([104,345,141,476],xy) for pixels in arrow_masks.values() for xy in pixels)
arrow_runs=[]
for name in ['final-verified','replay-1','replay-2']:
    d=load(PRODUCT/name/'inventory.json');r=next(r for r in d['regions'] if r['key']=='ig2b08:p30:advance-component-arrows')
    points=[r['box'][0]*612/1e6,r['box'][1]*792/1e6,r['box'][2]*612/1e6,r['box'][3]*792/1e6]
    ev=next(e for e in d['evidence'] if e['region_id']==r['id']);crop=Image.open(ev['image']['path']).convert('RGB')
    assert r['denominator_role']=='context'
    for label,pixels in arrow_masks.items():
        assert all(contains(points,xy) for xy in pixels)
        predicate=cyan if 'curve' in label else lambda rgb:max(rgb)<100
        for x,y in pixels:
            xx,yy=round(x-points[0]*2),round(y-points[1]*2)
            assert any(0<=xx+dx<crop.width and 0<=yy+dy<crop.height and predicate(crop.getpixel((xx+dx,yy+dy))) for dx in [-1,0,1] for dy in [-1,0,1])
    arrow_runs.append({'name':name,'region_id':r['id'],'revision':r['revision'],'evidence_image':ev['image'],'all_source_arrow_masks_present':True})
report={**meta(),'summary':'Independent hashes, baseline preservation, complete replay sets, normalized evidence and current indexes verified. Source-bound F02 confirmed separately; structural equality is not component completeness.','counts':counts,'runs':runs,'preservation_hashes':{'regions':digest([r for r in before['regions'] if r['id'] not in retired]),'retained_reading_order':digest(retained)},'F01_verification':{'fresh_original':pin(ROOT/'originals/page-30.png'),'old_crop_rejected':True,'source_mask_pixel_counts':{k:len(v) for k,v in arrow_masks.items()},'runs':arrow_runs},'F02_probe':{'source':pin('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'),'fresh_original':pin(ROOT/'originals/page-29.png'),'window_points':window,'selected_digit_pixels':len(mask),'runs':probe},'semantic_acceptance_granted':False,'executable_readiness':False,'exit_code':0}
(ROOT/'independent-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'exit_code':0,'counts':counts,'F02_confirmed_in_runs':len(probe),'F02_missing_pixels_each':[r['missing_visible_stem_pixels'] for r in probe]}))
