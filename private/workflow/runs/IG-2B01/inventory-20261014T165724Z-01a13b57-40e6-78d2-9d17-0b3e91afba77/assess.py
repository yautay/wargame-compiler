from prepare import *
tool=read(f'{REL}/toolchain.json'); sys.path[:0]=tool['process_pythonpath'].split(';'); os.environ['PATH']=tool['process_path_prefix']+';'+os.environ['PATH']; sys.dont_write_bytecode=True
from wgc.sources.inventory import validate
from wgc.sources.geometry import box_to_pdf,render_size_pixels
from PIL import Image
doc=read(f'{REL}/final-verified/inventory.json'); ledger=read(f'{REL}/region-ledger-final.json')
assert len(ledger)==130
report=validate(doc,ROOT); write(f'{REL}/final-root-validation.json',report)
check=[]
for e in doc['evidence']:
 r=next(r for r in doc['regions'] if r['id']==e['region_id']); p=next(p for p in doc['pages'] if p['id']==r['page_id'])
 with Image.open(ROOT/e['image']['path']) as im: size=im.size
 assert size==tuple(render_size_pixels(r['box'],p,e['render_parameters']['dpi']))
 text=(ROOT/e['text']['path']).read_text(encoding='utf-8')
 assert len(text)==e['text_codepoints']
 check.append({'evidence_id':e['id'],'region_id':r['id'],'region_revision':r['revision'],'page':p['pdf_page'],'box':r['box'],'actual_png_size':list(size),'utf8_codepoints':len(text),'pins_checked':[pin(e[k]['path']) for k in ['crop_pdf','text','image']],'result':'pass'})
write(f'{REL}/locator-audit.json',{'result':'pass','evidence_count':len(check),'records':check,'source_page_count':44,'source_bytes_unchanged':pin(f'{SOURCE}/rulebook.pdf')==doc['source']['pdf']})
uncertainty=[]
for e in doc['evidence']:
 text=(ROOT/e['text']['path']).read_text(encoding='utf-8')
 uncertainty.append({'evidence_id':e['id'],'region_id':e['region_id'],'text_pin':e['text'],'replacement_character_count':text.count('\ufffd'),'empty_extraction':not bool(text),'issues':['Machine extraction is literal evidence, not a verified transcription.','Line-wrap hyphens, ligatures, spaces, special glyph encodings and raster-embedded counter text require exact comparison with PNG.'],'normalization_performed':False,'known_replacement_offsets':[i for i,c in enumerate(text) if c=='\ufffd']})
write(f'{REL}/uncertainty.json',uncertainty)
# Exact rectangular complement of authored boxes, without approving blank-looking areas for exclusion.
geometry=[]
for p in range(1,5):
 page=doc['pages'][p-1]; boxes=[r['box'] for r in doc['regions'] if r['page_id']==page['id'] and r['denominator_role']=='inventory']
 ys=sorted({0,1000000,*[b[k] for b in boxes for k in [1,3]]}); rects=[]
 for y0,y1 in zip(ys,ys[1:]):
  intervals=sorted((b[0],b[2]) for b in boxes if b[1]<=y0 and b[3]>=y1); x=0
  for x0,x1 in intervals+[(1000000,1000000)]:
   if x<x0: rects.append([x,y0,x0,y1])
   x=max(x,x1)
 area=sum((b[2]-b[0])*(b[3]-b[1]) for b in rects)
 expected=next(x for x in report['pages'] if x['pdf_page']==p)['unaccounted_area_trillionths']; assert area==expected
 geometry.append({'pdf_page':p,'complement_rectangles':rects,'unaccounted_area_trillionths':area,'classification':'Unassigned geometric area, not an approved exclusion. Inspect page overlays for any substantive omission.'})
write(f'{REL}/geometric-gaps.json',geometry)
audit=read(f'{REL}/word-center-audit.json')
gaps=[]
for l in ledger:
 gaps.append({'id':'gap:'+l['key'],'region_id':l['region_id'],'region_revision':l['region_revision'],'levels':l['coverage'],'uncertainty':l['uncertainty'],'action':'Independent source comparison, exact transcription and later source-IG reconciliation; no semantic or exclusion approval inferred.'})
for a in audit:
 for w in a['unassigned_word_centers']: gaps.append({'id':f'gap:unassigned-word:p{a["page"]}:{len(gaps)}','page':a['page'],'source_word':w,'reason':'Extracted word center outside assigned region; inspect and refine without silently dropping source material.'})
write(f'{REL}/gaps.json',{'regions':gaps,'geometry_report':pin(f'{REL}/final-root-validation.json'),'geometric_gap_policy':'Every uncovered area remains an explicit geometric gap, including margins, gutters, interparagraph space, panel/cover background. No approved exclusion is inferred from blank-looking space. Word-center audit supports text accounting only; it cannot prove absence of raster/vector content.','unprocessed_outside_task_pages':list(range(5,45)),'raw_navigation':'TOC destinations and rule references outside assigned pages retained as source text; target content not inspected, resolved or inferred.','source_ig_review_freshness':'unknown','human_authority':'unverified','semantic_acceptance_granted':False})
before=read(f'{REL}/queue-before.json'); now=read('docs/work/queue.json')
assert [t for t in before['tasks'] if t['id']!='IG-2B01']==[t for t in now['tasks'] if t['id']!='IG-2B01']
for a in read(f'{REL}/base-products.json')['files']: assert pin(a['path'])==a,a['path']
for name,info in tool['native'].items(): assert hashlib.sha256(Path(info['path']).read_bytes()).hexdigest()==info['sha256']
write(f'{REL}/preservation.json',{'all_other_38_tasks_unchanged':True,'base_product_tool_schema_hashes_unchanged':True,'native_executable_hashes_unchanged':True,'source_and_provenance_unchanged':True,'modified_scope':'Only IG-2B01 queue refinement/events, exact allowlist additions, generated views and new private run/packet/check artifacts. Existing staged and unstaged work retained.','base_files':read(f'{REL}/base-products.json')['files']})
print('Locator audit passed',len(check),'evidence records; word gaps',sum(a['count'] for a in audit),flush=True)
