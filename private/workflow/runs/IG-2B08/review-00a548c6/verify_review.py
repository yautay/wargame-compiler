"""Independent frozen-byte and whole-set checks; no source text is emitted."""
import json, pathlib, hashlib, copy
from collections import Counter
from PIL import Image, ImageDraw

ROOT=pathlib.Path('private/workflow/runs/IG-2B08/review-00a548c6')
DEL=pathlib.Path('private/workflow/runs/IG-2B08/repair-F03-F04-01')
SESSION=pathlib.Path('private/workflow/orchestrator/20261017T151724Z-86fb83c5/002-IG-2B08-reviewer-00a548c6')
def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def pin(p):
    p=pathlib.Path(p); b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verify(row):
    p=pin(row['path']); assert p['sha256']==row['sha256']
    assert 'bytes' not in row or row['bytes']==p['bytes']
def save(name,d):
    runtime=SESSION/'runtime-configuration.json'
    meta=dict(role='reviewer',actor='ig2:002-IG-2B08-reviewer-00a548c6:reviewer',model='gpt-6.1-sol',reasoning='high',configuration_evidence=runtime.as_posix(),configuration_sha256=pin(runtime)['sha256'])
    (ROOT/name).write_text(json.dumps(dict(meta,**d),indent=2)+'\n',encoding='utf-8')
def pins(d):
    if isinstance(d,dict):
        if 'path' in d and 'sha256' in d: yield d
        for v in d.values(): yield from pins(v)
    elif isinstance(d,list):
        for v in d: yield from pins(v)
delivery=load(DEL/'delivery.json')
assert pin(DEL/'delivery.json')['sha256']=='00328bb99d2bb49708078181a007ba3dff40bba5af6e200325d2aba77d6be52f'
for a in delivery['artifacts']: verify(a)
frozen={a['path']:a for a in delivery['artifacts']}
assert len(frozen)==len(delivery['artifacts'])
pm=delivery['preservation_manifest'];verify(pm)
preserved=load(pm['path'])['artifacts']
for a in preserved: verify(a)
packet=load(SESSION/'packet.json'); access=load(SESSION/'access-manifest.json')
for a in packet['files']+packet['control_files']:
    if a['path'] in access['bootstrap_reads']: verify(access['bootstrap_reads'][a['path']])
    else: verify(a)
task=load(SESSION/'task.json'); retired=set(task['inventory_contract']['placeholder_target_ids'])
# Complete dependency objects are used only internally for preservation validation,
# as required by the batch contract. No dependency text or records are released.
basepath='private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/final-verified/inventory.json'
verify(dict(path=basepath,sha256='24d895f0e42c56e8d8fdb49afe2605da393bf3c9f5b153b2629fc50f5ef1415d'))
base=load(basepath)
docs=[load(DEL/n/'inventory.json') for n in ['final-verified','replay-1','replay-2']]
final=docs[0]; old={r['id']:r for r in base['regions']}; now={r['id']:r for r in final['regions']}
assert set(old)-set(now)==retired
assert all(now[k]==v for k,v in old.items() if k not in retired)
assert final['pages']==base['pages'] and final['source']==base['source']
assert final['links'][:len(base['links'])]==base['links']
assert final['evidence'][:len(base['evidence'])]==base['evidence']
oldorder=[x for x in base['reading_order'] if x not in retired]
assert [x for x in final['reading_order'] if x in set(oldorder)]==oldorder
assert all(e in final['registry']['entries'] for e in base['registry']['entries'])
obs=load(DEL/'region-ledger.json')['new_observations']; expected={x['region_id'] for x in obs}
assert len(expected)==269
index=load(DEL/'source-pins.json'); indexed={p['path']:p for p in pins(index)}
checks=[]
def norm(doc):
    result=copy.deepcopy(doc)
    result.pop('revision',None)
    for e in result['evidence']:
        if e['region_id'] in expected:
            for k in ['crop_pdf','image','text']:
                e[k]['path']=e[k]['path'].split('/evidence/',1)[1]
    return result
for n,doc in zip(['final-verified','replay-1','replay-2'],docs):
    assert norm(doc)==norm(final)
    assert doc['registry']==load(DEL/n/'identity-registry.json')
    selected=[r for r in doc['regions'] if r['key'].startswith('ig2b08:')]
    assert {r['id'] for r in selected}==expected and len(selected)==269
    assert len(doc['pages'])==44
    ev={e['region_id']:e for e in doc['evidence']}
    for r in selected:
        e=ev[r['id']]; assert e['region_revision']==r['revision']
        for k in ['crop_pdf','image','text']:
            verify(e[k]); assert indexed[e[k]['path']]==e[k]
            assert frozen[e[k]['path']]==e[k]
    checks.append(dict(name=n,regions=len(selected),evidence_files=3*len(selected),inventory=pin(DEL/n/'inventory.json')))
for p in pins(index):
    verify(p)
    if p['path'].startswith(DEL.as_posix()+'/'): assert frozen[p['path']]==p
for p in pins(load(DEL/'original-page-inspection.json')['original_artifacts']):
    assert p==indexed[p['path']]==frozen[p['path']]
components=load(DEL/'component-ledger.json')['components']
assert {o['region_id'] for o in components}=={o['region_id'] for o in obs if o['kind'] in {'example','legend','table','diagram'}}
roles=Counter(r['denominator_role'] for r in final['regions'])
assert roles['inventory']==1028
assert sum(o['denominator_contribution'] for o in obs)==183
assert sum(o['page']==33 for o in obs)==1
for o in obs:
    if o['page']==33:
        assert o['box']==[73529,63131,500000,101011] and o['denominator_contribution']==0
        assert pathlib.Path(o['evidence']['text']['path']).read_text(encoding='utf-8')==(ROOT/'originals/page-33.txt').read_text(encoding='utf-8')
save('independent-structural-check.json',dict(status='pass',delivery_artifacts=len(frozen),preserved_artifacts=len(preserved),packet_and_controls_verified=True,source_pages=44,retired_placeholders=4,preserved_regions=len(old)-4,preserved_evidence=len(base['evidence']),preserved_links=len(base['links']),preserved_registry_entries=len(base['registry']['entries']),retained_order=len(oldorder),runs=checks,full_denominator=1028,assigned_denominator=183,inherited_denominator=845,new_context=86,context_denominator=0,complete_components=len(components),source_index_references_verified=len(indexed)))

witnesses=[
 (150,[183,333,213,336],'gray','Tribune top frame'),
 (139,[146.5,342,149.5,349],'gray','A 2-marker exposed right frame'),
 (142,[147.5,424,150,431],'gray','B 2-marker exposed right frame'),
 (190,[452.5,318,456,325],'gray','Advanced B 2-marker exposed right frame'),
 (196,[476.5,381,479,391],'green','Celt C right counter vertex'),
 (228,[155.5,408,158,416],'red','Advance opaque Phalanx right vertex'),
 (239,[221,434.5,248,436.5],'red','Wheeled opaque Phalanx lower border'),
 (216,[232,259,237,261],'pink','Pivot origin lower counter vertex'),
 (240,[220,452,223.5,458],'pink','Wheel origin left counter vertex'),
 (241,[247,441,257,449],'black','Wheel forward black arrow tail'),
]
def predicate(c,kind):
    r,g,b=c
    if kind=='gray': return max(c)-min(c)<12 and 40<min(c)<225
    if kind=='green': return g>100 and g>r*1.2 and g>b*1.1
    if kind=='red': return r>140 and g<130 and b<140 and r-g>50
    if kind=='pink': return r>200 and 100<g<235 and 100<b<235 and r-g>15
    if kind=='black': return max(c)<80
results=[]
for i,box,kind,label in witnesses:
    o=obs[i]; image=Image.open(ROOT/'originals'/f"page-{o['page']}.png").convert('RGB')
    x0,y0,x1,y1=[round(v*2) for v in box]
    samples=[(x,y) for y in range(y0,y1) for x in range(x0,x1) if predicate(image.getpixel((x,y)),kind)]
    runs=[]
    for name,doc in zip(['final-verified','replay-1','replay-2'],docs):
        ev=next(e for e in doc['evidence'] if e['region_id']==o['region_id'])
        page=next(p for p in doc['pages'] if p['id']==ev['page_id'])
        # Source coordinates of the actual PNG, including outward-normalized origin
        # and any extra ceiling pixel. A one-pixel margin is intentionally allowed.
        left=ev['box'][0]*612*2/1e6; top=ev['box'][1]*792*2/1e6
        w,h=Image.open(ev['image']['path']).size
        missing=[(x,y) for x,y in samples if not (left-1<=x<left+w+1 and top-1<=y<top+h+1)]
        runs.append(dict(name=name,image=ev['image'],source_mask_pixels=len(samples),source_pixels_outside_actual_image_with_1px_margin=len(missing),actual_source_pixel_extent=[left,top,left+w,top+h]))
    patch=image.crop((x0,y0,x1,y1)); patch=patch.resize((patch.width*8,patch.height*8)); patch.save(ROOT/f'witness-{i}.png')
    results.append(dict(observation_index=i,key=o['key'],region_id=o['region_id'],region_revision=o['revision'],page=o['page'],points=o['points'],witness_points=box,label=label,predicate=kind,runs=runs,witness=pin(ROOT/f'witness-{i}.png')))
save('component-proof.json',dict(source=pin('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'),method='Source-colored pixels in independently inspected narrow witness windows outside actual delivered crop extent, even allowing one pixel. Witness masks establish omissions only; repairs must verify complete physical components.',results=results))
print(json.dumps({'structural':'pass','delivery_artifacts':len(frozen),'preservation_artifacts':len(preserved),'witnesses':[{'index':r['observation_index'],'source_pixels':r['runs'][0]['source_mask_pixels'],'outside':[v['source_pixels_outside_actual_image_with_1px_margin'] for v in r['runs']]} for r in results]}))
