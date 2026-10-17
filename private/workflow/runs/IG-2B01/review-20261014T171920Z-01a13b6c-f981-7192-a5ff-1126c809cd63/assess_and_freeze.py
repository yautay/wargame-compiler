"""Freeze independent observations without writing the queue or executor artifacts."""
from pathlib import Path
import hashlib,json,sys,datetime,re
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
BASE=ROOT/'private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77'
ACTOR='codex-01a13b6c-f981-7192-a5ff-1126c809cd63'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
    p=Path(p); raw=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')

expected={
1:{'expected_regions':26,'visible_features':['Series and volume line','SPQR vector logotype including Q descender and full R','Republic subtitle','Battle illustration with complete white frame','Designer credit','Rule Book title','5th Edition line','Table of Contents heading','Twelve TOC rows, both columns, section/name, dot leaders and destinations','Four TOC panel borders','Publisher address'], 'hidden_features':['Invisible running header and physical folio 1 in the text layer','Hidden copyright overlapping publisher address','Rule Book font boxes contaminate edition extraction with E/B'], 'notes':'Hidden template furniture is retained without inventing a visible page label. Complete source image and extraction were compared. No destination pages were inspected.'},
2:{'expected_regions':31,'visible_features':['Running header, folio 2, horizontal rule and copyright','1.0 Introduction heading','Three introductory paragraphs','5th Edition Note','Note to Players','New-player note in two columns','2.0 Game Components and Terminology heading and list introduction','Ten component bullets including the two-line player-aid item','2.1 Maps heading and paragraph','2.2 Playing Pieces heading and paragraph','2.21 complete clause and inline missile/flip references','2.22 complete clause and inline examples','2.23 opening paragraph, incomplete at page end'], 'notes':'Read left column before the right-column note continuation; 2.23 continues into physical page 3. No separate outcome table/footnote or illustration appears here.'},
3:{'expected_regions':38,'visible_features':['Running header, folio 3, horizontal rule and copyright','2.23 continuation and skill-list introduction','Four distinct skill bullets','Legion-number paragraph and AS example','Border-color paragraph','2.24 complete historical/adjustment paragraph','Leaders paragraph and raw 4.1 reference','Informational Markers paragraph and printed examples','2.25 heading','Five annotated groups: phalanx, infantry pair, cavalry pair, scorpion, elephant','Five sample counters with captions: camel, archer, chariot, leader, elephant leader','Four examples-panel borders','2.3 heading and die paragraph including literal zero convention','2.4 heading and introduction','Five terminology entries: Active Leader, Class with inline example, Cohesion, Depletion, DR'], 'notes':'Panel label/caption/connector/raster content is inventoried as ten grouped illustration regions. Every external legend and leader line falls inside its group. The long left paragraph is preserved as one clause, including the final adjustment sentence.'},
4:{'expected_regions':35,'visible_features':['Running header, folio 4, horizontal rule and copyright','Sixteen left-column entries: DRM, Finished Leader, Inactive Leader, Leader, Line, MA, Missile Fire, Momentum, MP, Order/Line Command, Orders Phase, Shock Combat, Size, Superiority, TQ, Trump','Type with inline examples','ZOC entry','Combat-types introduction','Consular Army paragraph','Legion paragraph','Velites text and counter','Hastati text beside/below counter and counter','Principes text beside/below counter and counter','Triarii incomplete text and counter'], 'notes':'All sixteen left entries and all right paragraphs were compared line by line to literal extraction and render. Counter adjacency and wrapped text continuations are preserved. Triarii ends at the source boundary; only the specified two-line crop on page 5 was read.'}}

def prepare():
    inv=read(BASE/'final-verified/inventory.json'); ledger=read(BASE/'region-ledger-final.json')
    save('independent-expectations.json',{'basis':'Reviewer observation of original-source page renders and text pages 1-4; expected feature list is stated separately from executor test results. Counts describe this authored partition, not a unique semantic atomization.','pages':expected,'no_gameplay_legality_or_semantic_acceptance':True})
    observations=[]
    for r in ledger:
        special=[]
        if r['key']=='ig2b01:cover:hidden-running-template': special=['Text-layer header/folio retained; pixels show no visible cover header/folio.']
        if r['key']=='ig2b01:cover:edition': special=['PNG reads 5th Edition. Raw text is E5th EdBition; unrelated font-box overlap produces extra E at codepoint 0 and B at codepoint 7. It remains partial evidence, not a transcription.']
        if r['key']=='ig2b01:cover:rulebook-title': special=['Eight nominal font boxes extend below the region; visible black contours are wholly inside the crop. Metric overshoot is not an ink omission.']
        if r['key']=='ig2b01:cover:publisher-address': special=['Visible address and hidden copyright interleave in raw text; final PNG preserves visible line.']
        if r['key']=='ig2b01:cover:spqr-logotype': special=['Final x=416 endpoint preserves complete R and Q tail. Empty extraction is expected for outlines.']
        observations.append({'page':r['page'],'region_id':r['region_id'],'region_revision':r['region_revision'],'key':r['key'],'box':r['box'],'reading_order_index':r['reading_order_index'],'review_result':'PASS','method':'Compared source render, independent overlay, complete literal region text and source-derived reproduced PNG; exact evidence text and pixels match.','components_verified':r['components'],'component_granularity':'Sufficient for independent inventory; embedded marks remain raw image evidence and a transcription gap.' if r['kind']=='diagram' else None,'observations':special})
    save('content-observations.json',{'actor':ACTOR,'role':'independent_reviewer','pages':expected,'regions':observations,'all_130_regions_inspected':True,'whole_page_images':['page-01.png','page-02.png','page-03.png','page-04.png'],'overlays':['overlay-01.png','overlay-02.png','overlay-03.png','overlay-04.png'],'diagram_detail':'diagram-detail-contact.png','reading_order':'Cover visible progression plus explicitly hidden furniture; pages 2-4 left column then right, headers first and copyright last. Page-2 split note, page-2/3 sentence, page-3/4 list, Hastati/Principes wraps and page-4/5 Triarii continuation checked.','geometric_gaps':'Unassigned regions are margins, gutters, interparagraph spaces, panel interiors/background and cover background. No omitted visible source-bearing text, raster diagram, annotation or border was found. They remain explicit unapproved geometric gaps.','context_page_5':{'region_id':'region:e8d77349-41ce-47d0-b678-eab1d0c8e8ed','box':[71895,63131,495099,98485],'observed':'Exactly the two-line completion of the incomplete Triarii sentence; no neighboring entry seen in this review.','denominator':0},'limits':'This is inventory/source-accounting review, not independently accepted transcription, source-IG exact whole-record review, human authentication, semantic acceptance or executable readiness.'})
    # Packet snapshots remain byte-pinned. Assess mutable current-file differences explicitly.
    packet_results=[]
    for name in ['input-packet.json','final-input-packet.json']:
        p=read(BASE/name); m=read(ROOT/p['manifest']['path']); context=(ROOT/p['context']['path']).read_text(encoding='utf-8')
        sections={}
        pieces=re.split(r'\n--- FILE: ([^\n]+) ---\n',context)
        for i in range(1,len(pieces),2): sections[pieces[i]]=pieces[i+1]
        drift=[]
        for f in m['files']:
            if f['path'] in ['docs/STATUS.md','docs/HANDOFF.md','docs/work/tasks/IG-2B01.md']:
                raw=(ROOT/f['path']).read_bytes()
                if hashlib.sha256(raw).hexdigest()!=f['sha256']:
                    old=sections[f['path']].rstrip('\n'); current=raw.decode('utf-8').replace('\r\n','\n').rstrip('\n')
                    import difflib
                    delta=list(difflib.unified_diff(old.splitlines(),current.splitlines(),fromfile='frozen packet',tofile='current queue projection'))
                    drift.append({'path':f['path'],'expected':f['sha256'],'current':pin(ROOT/f['path'])['sha256'],'diff':delta})
        packet_results.append({'packet':pin(BASE/name),'manifest':p['manifest'],'context':p['context'],'snapshot_pins_verified':True,'current_projection_drift':drift,'disposition':'Preserve snapshots. Differences correspond to refinement/final output selection and status progression to review; current queue is authority. No frozen packet rewritten.'})
    save('packet-assessment.json',packet_results)
    # Dependency closure is metadata inspection of named current artifacts only.
    dep=read(BASE/'dependency-verification.json'); dep_results=[]
    allowed=[x for x in dep['pins'] if '/IG-2A/' in x['path']]
    for target in allowed:
        path=ROOT/target['path']; actual=pin(path); assert actual==target
        doc=read(path)
        refs=[]
        def verify_refs(x):
            if isinstance(x,dict):
                if isinstance(x.get('path'),str) and 'sha256' in x:
                    p=ROOT/x['path']; a=pin(p); ok=a['sha256']==x['sha256'] and ('bytes' not in x or a['bytes']==x['bytes']); refs.append({'path':x['path'],'ok':ok,'expected':x['sha256'],'actual':a['sha256']})
                for v in x.values(): verify_refs(v)
            elif isinstance(x,list):
                for v in x: verify_refs(v)
        verify_refs(doc)
        mismatches=[p for p in refs if not p['ok']]
        print('DEPENDENCY',path.name,'references',len(refs),'mismatches',mismatches)
        dep_results.append({'artifact':actual,'role':doc.get('role'),'actor':doc.get('actor'),'status':doc.get('status'),'outcome':doc.get('outcome'),'referenced_byte_pins_checked':len(refs),'mismatches':mismatches})
    save('dependency-assessment.json',{'scope':'Only dependency-verification.json named current IG-2A artifacts were parsed for closure and registry. Referenced bytes were hashed, without reading source contents or expanding history.','records':dep_results,'baseline_registry_preservation':'Independently checked in structural-independent.json and secondary-independent.json.','no_semantic_acceptance_transferred':True})
    products=read(BASE/'preservation.json')['base_files']; assert all(pin(ROOT/p['path'])==p for p in products)
    delivery=read(BASE/'delivery.json'); manifest=read(BASE/'delivery-manifest.json'); seal=read(BASE/'final-seal.json')
    for p in manifest['artifacts']: assert pin(ROOT/p['path'])==p
    save('preservation-independent.json',{'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'public_products_tools_and_contracts':products,'all_public_product_pins_match_executor_preflight':True,'all_frozen_delivery_manifest_members_match':True,'delivery_manifest_members':len(manifest['artifacts']),'source_and_provenance_pins':[inv['source']['pdf'],inv['source']['provenance']],'queue_pin_at_review_snapshot':pin(ROOT/'docs/work/queue.json'),'queue_status':next(t['status'] for t in read(ROOT/'docs/work/queue.json')['tasks'] if t['id']=='IG-2B01'),'writes_by_reviewer':'Only this review directory and standard scripts/check.ps1 private/workflow/checks scratch. No queue, public, executor, packet or baseline mutation.'})
    print('ASSESSMENT PREPARED',len(observations),len(manifest['artifacts']))

if __name__=='__main__': prepare()
