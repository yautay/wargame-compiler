"""Fresh bounded IG-2B05 derivation. No prior derivation helper is used."""
import copy
import json
from pathlib import Path
import sys

from wgc.sources.inventory import assemble, make_region, validate, file_pin
from wgc.sources.pdf import extract_evidence

ROOT = Path.cwd()
BASE = Path(__file__).resolve().parent
REL = BASE.relative_to(ROOT).as_posix()
def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def write(path, value):
    (ROOT / path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def verified(path, sha):
    assert file_pin(ROOT, path)['sha256'] == sha, path
    return load(path)

def derive(name):
    out = REL + '/' + name
    (ROOT / out).mkdir(exist_ok=False)
    # Exact accepted input is read mechanically for preservation, never dumped as context.
    old = verified('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/inventory.json',
                   '5ac48725279f2a44d77bdbc6a14ca8bb6c828ee709b5f143b117700bb4c5f656')
    accepted_registry = verified('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/identity-registry.json',
                                 '50f254c8f3ceb8cc0feb688ea8b31f5a39b4bb6c76fbcd89fa2d45d87d245375')
    assert old['registry'] == accepted_registry
    part = load(REL + '/authored-partition.json')
    registry = load(REL + '/persisted-registry.json')
    assert all(e in registry['entries'] for e in accepted_registry['entries'])
    pages = {p['pdf_page']: p for p in old['pages']}
    assigned_pages = {pages[n]['id'] for n in (17,18,19,20)}
    retired = {r['id'] for r in old['regions'] if r['page_id'] in assigned_pages}
    task = load('private/workflow/orchestrator/20261016T154824Z-fae43db9/001-IG-2B05-executor-008601fd/task.json')
    assert retired == set(task['target_ids'])
    assert not any(l['from'] in retired or l['to'] in retired for l in old['links'])
    new = []
    for item in part['regions']:
        x1,y1,x2,y2 = item['pixel_box']
        box = [round(x1*1000000/1224),round(y1*1000000/1584),round(x2*1000000/1224),round(y2*1000000/1584)]
        new.append(make_region(registry,item['key'],pages[item['page']],box,kind=item['kind'],
                               reason='Structurally inventoried; verified transcription and source semantics remain unprocessed.'))
    # Every identity was already explicit in the candidate registry; assignment adds none.
    assert registry == load(REL + '/persisted-registry.json')
    def rid(page, suffix):
        return next(r['id'] for r in new if r['key']==f'physical-page:{page}:ig2b05:{suffix}')
    links = copy.deepcopy(old['links'])
    def link(kind,a,b,reason):
        links.append({'kind':kind,'from':rid(*a),'to':rid(*b),'reason':reason})
    for a,b,reason in [
        ((17,'voluntary-example-start'),(18,'voluntary-example-velites'),'Example 1 continues across physical pages 17-18.'),
        ((18,'voluntary-example-velites'),(18,'voluntary-example-hastati'),'Second paragraph of Example 1.'),
        ((18,'6-66-start'),(18,'6-66-end'),'Sentence continues from left-column exit to right-column entrance.'),
        ((18,'6-71-upper'),(18,'6-71-lower'),'Text wraps around the In Column marker.'),
        ((18,'6-73-start'),(19,'6-73-end'),'Sentence continues across physical pages 18-19.'),
        ((19,'pw-introduction-upper'),(19,'pw-introduction-lower'),'Introduction wraps around the two markers.'),
        ((20,'7-15'),(20,'7-15-exception'),'Exception continues the clause in the right column.'),
        ((20,'7-21-upper'),(20,'7-21-lower'),'Text wraps below the ZOC diagram.')]:
        link('continuation',a,b,reason)
    for a,b in [((17,'withdrawal-play-note'),(17,'withdrawal-example')),((17,'stacking-design-note'),(17,'stacking-introduction')),
                ((17,'stacking-play-note'),(17,'6-63')),((18,'roman-flexibility-note'),(18,'rout-retreat-example')),
                ((18,'column-design-note'),(18,'6-7-heading')),((19,'pw-play-note-1'),(19,'6-83')),
                ((19,'pw-play-note-2'),(19,'6-83')),((20,'7-15-play-note'),(20,'7-15')),
                ((20,'reverse-face-note'),(20,'7-16')),((20,'7-23-play-note'),(20,'7-23-exception'))]:
        link('note_for',a,b,'Visible note associated with this local passage; structural relation only.')
    for a,b in [((18,'in-column-marker'),(18,'6-71-upper')),((19,'column-diagram'),(19,'6-74')),
                ((19,'column-caption'),(19,'column-diagram')),((19,'prearranged-marker'),(19,'pw-introduction-upper')),
                ((19,'no-pw-marker'),(19,'pw-introduction-upper')),((20,'single-hex-facing'),(20,'7-11')),
                ((20,'phalanx-facing'),(20,'7-11')),((20,'zoc-diagram'),(20,'zoc-introduction'))]:
        link('illustrates',a,b,'Visible illustration/caption associated with local text; no semantic acceptance.')
    regions = []
    order = []
    for r in old['regions']:
        if r['id'] in retired:
            replacements = [n for n in new if n['page_id']==r['page_id']]
            regions.extend(replacements)
        else:
            regions.append(copy.deepcopy(r))
    for identity in old['reading_order']:
        if identity in retired:
            original = next(r for r in old['regions'] if r['id']==identity)
            order.extend(r['id'] for r in new if r['page_id']==original['page_id'])
        else:
            order.append(identity)
    # For crop extraction only, use all 44 source pages, authored regions, and
    # the exact retained label evidence/regions required by verified page labels.
    # This avoids repeatedly hashing unrelated inherited crops for each new crop.
    # Every retained record/evidence byte is still validated in the complete
    # final output below; no source component or delivered record is omitted.
    label_ids={p['label']['evidence'] for p in old['pages'] if p['label']['status']=='verified'}
    label_evidence=[e for e in old['evidence'] if e['id'] in label_ids]
    label_regions={e['region_id'] for e in label_evidence}
    crop_regions=[r for r in regions if r['id'] in label_regions or r['id'] in {n['id'] for n in new}]
    crop_input = assemble(old['source'],old['pages'],crop_regions,registry,
                          reading_order=[r['id'] for r in crop_regions],evidence=label_evidence,toolchain=old['toolchain'])
    fresh = []
    for i,r in enumerate(new,1):
        slug = r['key'].replace(':','-')
        fresh.append(extract_evidence(crop_input,r['id'],ROOT,out+'/evidence/'+slug,dpi=144))
        print(f'{name}: crop {i}/{len(new)}',flush=True)
    final = assemble(old['source'],old['pages'],regions,registry,reading_order=order,links=links,
                      evidence=copy.deepcopy(old['evidence'])+fresh,toolchain=old['toolchain'])
    report = validate(final,ROOT)
    write(out+'/inventory.json',final)
    write(out+'/identity-registry.json',registry)
    write(out+'/derivation-validation.json',report)
    print(json.dumps({'output':out,'regions':len(final['regions']),'fresh_evidence':len(fresh),
                      'inventory':file_pin(ROOT,out+'/inventory.json')}),flush=True)

if __name__ == '__main__':
    derive(sys.argv[1])
