"""One complete independent task regeneration from pinned accepted inputs."""
import copy
import json
import sys
import time
from pathlib import Path

from wgc.sources.inventory import assemble, file_pin, make_region, seal, validate, page_basis_hash
from wgc.sources.pdf import extract_evidence

ROOT = Path.cwd()
OUT = Path(__file__).parent
REL = OUT.relative_to(ROOT).as_posix()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def regenerate(mode):
    assert mode in ('replay-a', 'replay-b', 'final-verified')
    destination = OUT / mode
    destination.mkdir(exist_ok=False)
    claim = load(OUT/'claim.json')
    spec = load(OUT/'authored-regions.json')
    session = Path(claim['configuration_evidence']).parent
    task = load(session/'task.json')
    contract = load(task['inventory_contract']['path'])
    for pin in contract['inputs'].values():
        assert file_pin(ROOT,pin['path']) == pin, pin['path']
    # These exact inputs are read solely for preservation/transform, never printed.
    baseline = load(contract['inputs']['baseline_inventory']['path'])
    registry = load(OUT/'authored-registry.json')
    pages = {p['pdf_page']:p for p in baseline['pages']}
    authored=[]
    for rec in spec['regions']:
        region = make_region(registry, rec['key'], pages[rec['pdf_page']], rec['box'],
                             kind=rec['kind'], reason='Source unit inventoried visually; verified transcription remains pending.')
        assert region['id'] == rec['id']
        # Preserve the distinction between independent inventory, machine text,
        # verified transcription, and both semantic levels. No invented approval.
        region['uncertainty'] = []
        region['coverage']['transcription'] = {'status':'partial','gap':True,
            'reason':'Fresh exact graphical evidence and machine text; no verified verbatim transcription decision.', 'boundary':None}
        for level in ('descriptive_semantics','formal_semantics'):
            region['coverage'][level] = {'status':'unprocessed','gap':True,
                'reason':'Independent source inventory only; semantic representation and acceptance pending.', 'boundary':None}
        authored.append(seal(region))
    retired = set(task['target_ids'])
    assert retired == {r['id'] for r in baseline['regions'] if r['page_id'] in {pages[p]['id'] for p in (13,14,15,16)}}
    regions = [r for r in baseline['regions'] if r['id'] not in retired] + authored
    inserted=False
    order=[]
    for identity in baseline['reading_order']:
        if identity in retired:
            if not inserted:
                order.extend(r['id'] for r in authored)
                inserted=True
        else:
            order.append(identity)
    ids={r['key'].split(':',2)[-1]:r['id'] for r in authored}
    # Key lookup includes page explicitly where duplicate suffixes occur.
    ids={r['key']:r['id'] for r in authored}
    def identity(page,key):
        return ids[f'b04:p{page}:{key}']
    additions=[]
    def link(kind, p, a, q, b, reason):
        additions.append({'kind':kind,'from':identity(p,a),'to':identity(q,b),'reason':reason})
    link('continuation',13,'5.44-opening',13,'5.44-continuation','Same wrapped 5.44 paragraph below marker.')
    link('continuation',13,'example-5.53-start',14,'example-5.53-end','Visible sentence continues from definite to and one possible Momentum phase.')
    link('continuation',15,'6.32-opening',15,'6.32-phalanx','Second paragraph of 6.32.')
    link('continuation',15,'6.51-start',16,'6.51-continuation','Visible sentence continues from away to from the moving unit.')
    link('continuation',16,'6.51-continuation',16,'6.51-exception-1','First explicitly labeled exception to 6.51.')
    link('continuation',16,'6.51-exception-1',16,'6.51-exception-2','Second bulleted exception.')
    link('continuation',16,'6.51-exception-2',16,'6.51-missile','Following unnumbered paragraph before the play note.')
    link('continuation',16,'6.52-intro',16,'6.52-penalty-1','First numbered penalty following introduction.')
    link('continuation',16,'6.52-penalty-1',16,'6.52-penalty-2','Second numbered penalty.')
    link('continuation',16,'6.52-penalty-2',16,'6.52-penalty-3','Third numbered penalty.')
    link('continuation',16,'6.55-opening',16,'6.55-mounted-archers','Following unnumbered paragraph in 6.55.')
    link('illustrates',13,'marker-no-momentum',13,'5.44-opening','5.44 explicitly names the TRUMPED/NO MOMENTUM marker.')
    link('illustrates',14,'marker-moved',14,'play-note-moved','Moved marker beside play note.')
    link('illustrates',15,'diagram-front-to-flank',15,'6.43','Diagram and caption show the named front-to-flank maneuver; no legality inference.')
    link('illustrates',15,'caption-front-to-flank',15,'diagram-front-to-flank','Visible caption directly below diagram.')
    link('illustrates',16,'diagram-withdrawal',16,'example-6.51-3','Example3 explicitly refers to the above diagram.')
    link('illustrates',16,'diagram-withdrawal',16,'6.52-penalty-3','6.52 penalty3 explicitly refers to the diagram above Example3.')
    # Keep every old record and link; there are no links to the retired placeholders.
    assert not any(l['from'] in retired or l['to'] in retired for l in baseline['links'])
    document=assemble(baseline['source'],baseline['pages'],regions,registry,
                      reading_order=order,links=baseline['links']+additions,
                      evidence=baseline['evidence'],toolchain=baseline['toolchain'])
    validate(document,ROOT)
    start=time.monotonic()
    generated=[]
    evidence_base=REL+'/evidence' if mode=='final-verified' else REL+'/'+mode+'/evidence'
    # Transient extraction basis retains the full actual PDF structure and registry.
    # Labels do not enter page_basis_hash; the final document preserves every
    # accepted page byte-for-byte. Per-crop validation needs only its own region.
    extraction_pages=copy.deepcopy(document['pages'])
    for page in extraction_pages:
        page['label']={'status':'unknown','value':None,
            'reason':'Transient crop basis only; accepted labels retained in complete output.', 'evidence':None}
        page.update(seal(page))
    for index,region in enumerate(authored,1):
        basis=assemble(document['source'],extraction_pages,[region],registry,
                       toolchain=document['toolchain'])
        assert page_basis_hash(next(p for p in basis['pages'] if p['id']==region['page_id'])) == page_basis_hash(pages[next(rec['pdf_page'] for rec in spec['regions'] if rec['id']==region['id'])])
        generated.append(extract_evidence(basis,region['id'],ROOT,evidence_base+'/'+region['key'].replace(':','-'),dpi=144))
        if index%10==0:
            print(json.dumps({'mode':mode,'generated':index,'total':len(authored),'elapsed_seconds':round(time.monotonic()-start,1)}),flush=True)
    document=seal({**document,'evidence':baseline['evidence']+generated})
    validate(document,ROOT)
    write(destination/'inventory.json',document)
    write(destination/'identity-registry.json',registry)
    common={k:claim[k] for k in ('role','actor','task','model','reasoning','configuration_evidence','configuration_sha256')}
    write(destination/'regeneration.json',{**common,'mode':mode,'baseline':contract['inputs']['baseline_inventory'],
        'accepted_registry':contract['inputs']['identity_registry'],'authored_spec':file_pin(ROOT,REL+'/authored-regions.json'),
        'persisted_registry':file_pin(ROOT,REL+'/authored-registry.json'),'generated_evidence':len(generated),
        'inventory':file_pin(ROOT,REL+'/'+mode+'/inventory.json'),'validation':'passed against original PDF and artifact bytes',
        'seconds':time.monotonic()-start,'copied_output_evidence':False})
    print(json.dumps({'mode':mode,'complete':True,'generated_evidence':len(generated)}),flush=True)


if __name__=='__main__':
    regenerate(sys.argv[1])
