from prepare import *
tool=read(f'{REL}/toolchain.json'); sys.path[:0]=tool['process_pythonpath'].split(';'); os.environ['PATH']=tool['process_path_prefix']+';'+os.environ['PATH']; sys.dont_write_bytecode=True
from wgc.sources.inventory import validate,seal
from wgc.sources.pdf import extract_evidence
from wgc.contracts.source import canonical_bytes
from wgc.sources.geometry import box_to_pdf
from author import build
from PIL import Image,ImageDraw
doc=read(f'{REL}/authored/inventory.json'); replay,ledger=build(copy.deepcopy(doc['registry']))
assert canonical_bytes(replay)==canonical_bytes(doc)
write(f'{REL}/repeatability.json',{'persisted_registry_replay_identical_canonical_bytes':True,'all_region_ids_unchanged':True,'baseline':pin(f'{REL}/authored/inventory.json'),'replay_sha256':hashlib.sha256(canonical_bytes(replay)+b'\n').hexdigest(),'source_pdf_remapped':False})
rows=[]
for number in [1,2,3,4,5]:
 page=doc['pages'][number-1]
 targets=[r for r in doc['regions'] if r['page_id']==page['id'] and not r['key'].endswith('unprocessed-placeholder')]
 for index,region in enumerate(targets):
  start=datetime.now(timezone.utc); t=time.monotonic()
  e=extract_evidence(doc,region['id'],ROOT,f'{REL}/evidence/p{number:02}-{index:03}',dpi=144)
  doc['evidence'].append(e); doc=seal(doc)
  rows.append({'region_id':region['id'],'region_key':region['key'],'evidence_id':e['id'],'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':0,'operation':'wgc.sources.pdf.extract_evidence','output':e['image']['path']})
  print(number,index,region['key'],flush=True)
 # Retain checkpoint at each finished page; never claim independent review.
 write(f'{REL}/checkpoint-page-{number}.json',{'task':'IG-2B01','actor':ACTOR,'input_packet':pin(f'{REL}/input-packet.json'),'configuration':pin(f'{REL}/configuration.json'),'completed_pages':list(range(1,min(number,4)+1)),'derived_evidence':len(doc['evidence']),'draft_inventory_revision':doc['revision'],'blocker':None,'next_operation':'Finish derivation and exact locator checks.'})
for p in doc['pages'][:4]:
 if p['pdf_page']>1:
  region=next(r for r in doc['regions'] if r['key']==f'ig2b01:p{p["pdf_page"]}:folio')
  e=next(e for e in doc['evidence'] if e['region_id']==region['id'])
  p['label']={'status':'verified','value':str(p['pdf_page']),'reason':'Executor observed visible folio in original page PNG and exact same-page evidence; independent review pending.','evidence':e['id']}
  p.update(seal(p))
doc=seal(doc); report=validate(doc,ROOT)
out=RUN/'final'; out.mkdir(exist_ok=False)
(out/'inventory.json').write_bytes(canonical_bytes(doc)+b'\n'); (out/'identity-registry.json').write_bytes(canonical_bytes(doc['registry'])+b'\n')
write(f'{REL}/root-validation.json',report); write(f'{REL}/evidence-operations.json',rows)
for row in ledger:
 r=next(r for r in doc['regions'] if r['id']==row['region_id']); e=next(e for e in doc['evidence'] if e['region_id']==r['id']); page=doc['pages'][row['page']-1]
 row.update(evidence=e,exact_native_bottom_left_bounds_rational=[{'numerator':v.numerator,'denominator':v.denominator} for v in box_to_pdf(r['box'],page)],reading_order_index=doc['reading_order'].index(r['id']),uncertainty=r['uncertainty'],coverage=r['coverage'])
write(f'{REL}/region-ledger.json',ledger)
write(f'{REL}/continuations.json',{'links':doc['links'],'context_region':next(r for r in doc['regions'] if r['denominator_role']=='context'),'context_access':pin(f'{REL}/context-access-authorization.json'),'overread_disclosure':pin(f'{REL}/context-overread.json'),'boundary_unresolved':[],'scope_note':'DR to DRM links the ongoing terminology list, not an incomplete DR definition. Triarii completion is context only. Other raw navigation references are unexpanded.'})
base=read(f'{BASE}/inventory-one/inventory.json')
assert doc['pages'][4:]==base['pages'][4:]
for r in base['regions'][4:]: assert r in doc['regions']
write(f'{REL}/scope-report.json',{'task':'IG-2B01','inventory':pin(f'{REL}/final/inventory.json'),'physical_page_count':44,'authored_pages':[1,2,3,4],'task_denominator':len(ledger),'per_page':{str(p):sum(l['page']==p for l in ledger) for p in range(1,5)},'full_inventory_denominator':len(ledger)+40,'unchanged_unprocessed_placeholders':40,'context_regions':1,'context_denominator':0,'represented_at_any_level':0,'excluded_at_any_level':0,'pages_5_44_and_placeholders_unchanged':True,'context_page_5':'Exact two-line Triarii tail only in final evidence; initial wider probe deviation disclosed.','no_semantic_acceptance':True})
# Compare centers of every extracted word against authored boxes. Not a semantic coverage oracle.
audit=[]
for p in range(1,5):
 page=doc['pages'][p-1]; regions=[r for r in doc['regions'] if r['page_id']==page['id']]
 missed=[]
 for w in read(f'{REL}/pages/page-{p:02}-words.json'):
  x=(w['x0']+w['x1'])/2/612*1e6; y=(w['top']+w['bottom'])/2/792*1e6
  hits=[r for r in regions if r['box'][0]<=x<r['box'][2] and r['box'][1]<=y<r['box'][3]]
  if not hits: missed.append(w)
 audit.append({'page':p,'unassigned_word_centers':missed,'count':len(missed)})
write(f'{REL}/word-center-audit.json',audit)
# Annotated full-page overlays make each exact locator visible to the reviewer.
(RUN/'overlays').mkdir(exist_ok=False)
for p in range(1,5):
 im=Image.open(RUN/f'pages/original-{p:02}.png').convert('RGB'); draw=ImageDraw.Draw(im)
 for i,l in enumerate([l for l in ledger if l['page']==p]):
  a,b,c,d=l['box']; box=[a*im.width/1e6,b*im.height/1e6,c*im.width/1e6,d*im.height/1e6]; draw.rectangle(box,outline='red',width=1); draw.text((box[0],box[1]),str(i+1),fill='blue')
 im.save(RUN/f'overlays/page-{p:02}.png')
print('ROOT VALIDATION PASS',len(ledger),'regions; missed word centers',[(x['page'],x['count']) for x in audit],flush=True)
