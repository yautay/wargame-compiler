"""Bounded fresh source-inventory derivation; no gameplay interpretation.

Each build starts from the byte-pinned accepted baseline, authored partition and
persisted registry. Evidence extraction uses a separately validated carrier with
the same source, physical geometry and new region records. Its unknown labels and
empty evidence list prevent irrelevant inherited label/evidence dependencies in
the extraction carrier. Complete delivered inventories retain baseline labels,
records and evidence and are validated independently against all source bytes.
"""
from pathlib import Path
import copy
import hashlib
import json
import sys
from wgc.sources.inventory import assign, assemble, file_pin, make_region, seal, validate
from wgc.sources.pdf import extract_evidence

ROOT=Path.cwd()
RUN=Path(__file__).parent.relative_to(ROOT).as_posix()
SESSION='private/workflow/orchestrator/20261016T150146Z-33452c9a/002-IG-2B05-executor-d0013415'
INPUT='private/workflow/runs/IG-2B05/coordinator-6daf4d13-01/dependency-inputs.json'

def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))

def write(path, value):
    p=ROOT/path
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(value,indent=2,ensure_ascii=True)+'\n')

def pin(path): return file_pin(ROOT,path)

def identity():
    c=read(SESSION+'/runtime-configuration.json')
    assert (c['status'],c['model'],c['reasoning'])==('confirmed','gpt-6.1-sol','high')
    return dict(role='executor',actor='ig2:002-IG-2B05-executor-d0013415:executor',
                model=c['model'],reasoning=c['reasoning'],configuration_evidence=SESSION+'/runtime-configuration.json',
                configuration_sha256=pin(SESSION+'/runtime-configuration.json')['sha256'])

def inputs():
    contract=read(SESSION+'/task.json')
    refs=read(INPUT)['inventory']
    for item in [refs['baseline_inventory'],refs['identity_registry'],refs['source']['pdf'],refs['source']['provenance'],*refs['reports'].values()]:
        assert pin(item['path'])==item, item['path']
    base=read(refs['baseline_inventory']['path'])
    registry=read(refs['identity_registry']['path'])
    assert base['registry']==registry
    assert len(base['pages'])==44
    pages={p['id']:p for p in base['pages']}
    for expected in contract['inventory_batch']['assigned_pages']:
        assert all(pages[expected['id']][k]==v for k,v in expected.items())
    regions={r['id']:r for r in base['regions']}
    for expected in contract['inventory_batch']['replace_placeholders']:
        assert all(regions[expected['id']][k]==v for k,v in expected.items())
    return contract,refs,base,registry

def prepare():
    _,refs,base,registry=inputs()
    validate(base,ROOT)
    authored=read(RUN+'/authored-partition.json')
    for row in authored['regions']: assign(registry,'region',row['key'])
    write(RUN+'/persisted-registry.json',registry)
    write(RUN+'/input-verification.json',{
        **identity(),'format':'wgc-input-verification-1','task':'IG-2B05',
        'input_reference':pin(INPUT),'input_pins':[refs['baseline_inventory'],refs['identity_registry'],refs['source']['pdf'],refs['source']['provenance'],*refs['reports'].values()],
        'all_pins_verified':True,'baseline_full_validation':'passed',
        'original_registry_retained':True,'assigned_page_and_placeholder_contract':'exact',
        'new_registry':pin(RUN+'/persisted-registry.json'),
        'authored_partition':pin(RUN+'/authored-partition.json')})
    print('Input pins, accepted baseline, all retained evidence and assigned contract validated.',flush=True)

LINKS=[
 ('continuation',17,'voluntary-example-start',18,'voluntary-example-velites','Example 1 continues across physical pages 17-18.'),
 ('continuation',18,'voluntary-example-velites',18,'voluntary-example-hastati','Second paragraph of the same example.'),
 ('continuation',18,'6-66-start',18,'6-66-end','Sentence continues from left-column exit to right-column entrance.'),
 ('continuation',18,'6-71-upper',18,'6-71-lower','Text wraps around the In Column marker.'),
 ('continuation',18,'6-73-start',19,'6-73-end','Sentence continues across physical pages 18-19.'),
 ('continuation',19,'pw-introduction-upper',19,'pw-introduction-lower','Text wraps around the paired PW markers.'),
 ('continuation',20,'7-15',20,'7-15-exception','Exception follows the left-column rule at the right-column entrance.'),
 ('continuation',20,'7-21-upper',20,'7-21-lower','Text wraps around the ZOC diagram.'),
 ('note_for',17,'withdrawal-play-note',17,'withdrawal-example','Gray play note follows the withdrawal example.'),
 ('note_for',17,'stacking-design-note',17,'stacking-introduction','Blue design note follows the stacking introduction.'),
 ('note_for',17,'stacking-play-note',17,'6-63','Gray note calls attention to the stacking chart.'),
 ('note_for',18,'roman-flexibility-note',18,'rout-retreat-example','Blue design note follows the stacking examples.'),
 ('note_for',18,'column-design-note',18,'6-7-heading','Blue design note introduces Column Movement.'),
 ('illustrates',18,'in-column-marker',18,'6-71-upper','Marker appears beside the column-formation clause.'),
 ('illustrates',19,'column-diagram',19,'6-74','Diagram illustrates front-flank movement.'),
 ('note_for',19,'column-caption',19,'column-diagram','Caption immediately below the movement diagram.'),
 ('illustrates',19,'prearranged-marker',19,'pw-introduction-upper','PW marker beside the introduction.'),
 ('illustrates',19,'no-pw-marker',19,'pw-introduction-upper','NO PW marker beside the introduction.'),
 ('note_for',19,'pw-play-note-1',19,'6-83','Play Note 1 follows the PW event alternatives.'),
 ('note_for',19,'pw-play-note-2',19,'6-83','Play Note 2 follows the PW event alternatives.'),
 ('illustrates',20,'single-hex-facing',20,'7-11','One-hex facing illustration beneath the facing clause.'),
 ('illustrates',20,'phalanx-facing',20,'7-11','Phalanx facing illustration beneath the facing clause.'),
 ('note_for',20,'7-15-play-note',20,'7-15','Gray note follows the reaction-facing exception.'),
 ('note_for',20,'reverse-face-note',20,'7-16','Blue design note follows Reverse Face.'),
 ('illustrates',20,'zoc-diagram',20,'7-21-upper','ZOC diagram beside the definition and extent text.'),
 ('note_for',20,'7-23-play-note',20,'7-23-exception','Gray play note follows the non-Shock-capable exception.'),
]

def derive(name):
    contract,_,base,_=inputs()
    registry=read(RUN+'/persisted-registry.json')
    authored=read(RUN+'/authored-partition.json')
    pages={p['pdf_page']:p for p in base['pages']}
    rows=[r for n in (17,18,19,20) for r in authored['regions'] if r['page']==n]
    new=[]; keys={}
    for row in rows:
        x0,y0,x1,y1=row['pixel_box']
        # Shared boundaries use identical nearest-integer quantization (no overlap).
        box=[round(x0*1000000/1224),round(y0*1000000/1584),round(x1*1000000/1224),round(y1*1000000/1584)]
        r=make_region(registry,row['key'],pages[row['page']],box,kind=row['kind'],
                      reason='Structurally inventoried; verified transcription and source semantics remain unprocessed.')
        new.append(r); keys[(row['page'],row['key'].split(':')[-1])]=r['id']
    assert registry==read(RUN+'/persisted-registry.json'),'Derivation cannot allocate new identities'
    links=[dict(kind=k,**{'from':keys[(p,a)],'to':keys[(q,b)]},reason=why) for k,p,a,q,b,why in LINKS]
    retired=set(contract['target_ids'])
    regions=[]; order=[]
    for old in base['regions']:
        if old['id'] in retired:
            replacements=[r for r in new if r['page_id']==old['page_id']]
            regions.extend(replacements)
        else: regions.append(copy.deepcopy(old))
    for old_id in base['reading_order']:
        if old_id in retired:
            old=next(r for r in base['regions'] if r['id']==old_id)
            order.extend(r['id'] for r in new if r['page_id']==old['page_id'])
        else: order.append(old_id)
    # A standalone validated evidence carrier preserves source/physical bases and
    # exact new regions. It is not the delivered complete inventory.
    carrier_pages=[]
    for p in base['pages']:
        p=copy.deepcopy(p)
        p['label']={'status':'unknown','value':None,'reason':'Evidence carrier does not verify printed labels.','evidence':None}
        carrier_pages.append(seal(p))
    carrier=assemble(base['source'],carrier_pages,new,registry,links=links,toolchain=base['toolchain'])
    evidence=[]
    for index,r in enumerate(new,1):
        evidence.append(extract_evidence(carrier,r['id'],ROOT,f'{RUN}/{name}/evidence/{index:03d}',dpi=144))
        if index%10==0 or index==len(new):print(f'{name}: derived {index}/{len(new)} fresh crops',flush=True)
    result=assemble(copy.deepcopy(base['source']),copy.deepcopy(base['pages']),regions,registry,
                    reading_order=order,links=copy.deepcopy(base['links'])+links,
                    evidence=copy.deepcopy(base['evidence'])+evidence,toolchain=copy.deepcopy(base['toolchain']))
    validate(result,ROOT)
    write(f'{RUN}/{name}/inventory.json',result)
    write(f'{RUN}/{name}/identity-registry.json',registry)
    write(f'{RUN}/{name}/derivation.json',{
        **identity(),'format':'wgc-fresh-derivation-1','task':'IG-2B05',
        'authored_partition':pin(RUN+'/authored-partition.json'),
        'persisted_registry':pin(RUN+'/persisted-registry.json'),
        'inventory':pin(f'{RUN}/{name}/inventory.json'),
        'registry':pin(f'{RUN}/{name}/identity-registry.json'),
        'fresh_evidence_count':len(evidence),'full_validation':'passed',
        'evidence_carrier':'Same source, 44 physical geometry bases, exact assigned region revisions and persisted identities; labels unknown, no inherited evidence. Full complete output independently validated.'})
    print(f'{name}: complete independent derivation and full validation passed.',flush=True)

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1] in ('final-verified','replay-1','replay-2'):derive(sys.argv[1])
    else:raise ValueError('Unknown bounded operation')
