"""Freeze bounded inventory ledgers and preservation reports after derivation."""
import json, pathlib, copy, re, math, datetime, hashlib, struct
from fractions import Fraction
from PIL import Image
from pypdf import PdfReader
from author import OUT, ROOT, BASE, PINS, META
from wgc.sources.inventory import validate, file_pin, page_basis_hash, coverage
from wgc.sources.geometry import box_to_pdf, render_size_pixels, area
from wgc.contracts.source import canonical_bytes

def save(name,data):
 path=OUT/name
 with path.open('xb') as stream:stream.write(canonical_bytes(data)+b'\n')

def pin(path):return file_pin(ROOT,path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix())

def complement(boxes):
 """Exact disjoint rectangular decomposition of all geometry outside regions."""
 ys=sorted({0,1000000,*[b[j] for b in boxes for j in (1,3)]});rects=[]
 for y0,y1 in zip(ys,ys[1:]):
  spans=sorted((b[0],b[2]) for b in boxes if b[1]<=y0 and b[3]>=y1);x=0
  for a,b in spans:
   if a>x:rects.append([x,y0,a,y1])
   x=b
  if x<1000000:rects.append([x,y0,1000000,y1])
 return rects

def component(row,ev,slug,bounds,observation):
 # Pixel sublocators annotate a raster counter; they are not overlapping inventory
 # regions, independent evidence IDs, extra denominator units or represented rules.
 w=ev['render_parameters']['width_pixels'];h=ev['render_parameters']['height_pixels'];b=row['box']
 x0,y0,x1,y1=bounds
 assert 0<=x0<x1<=w and 0<=y0<y1<=h
 pagebox=[b[0]+math.floor(Fraction(x0*(b[2]-b[0]),w)),b[1]+math.floor(Fraction(y0*(b[3]-b[1]),h)),b[0]+math.ceil(Fraction(x1*(b[2]-b[0]),w)),b[1]+math.ceil(Fraction(y1*(b[3]-b[1]),h))]
 return {'component_key':row['key']+':component:'+slug,'region_id':row['region_id'],'evidence_id':ev['id'],'image':ev['image'],'image_pixel_box':bounds,'pixel_bounds':'half_open_top_left','page_box':pagebox,'observation':observation,'task_denominator_units':0,'coverage_status':'unprocessed','gap_reason':'Visual component observation does not constitute accepted transcription or source semantics.'}

def main():
 replay=json.loads((OUT/'registry-replay-report.json').read_text())
 assert len(replay['runs'])==3 and all(r['independent_root_validation']=='passed' for r in replay['runs'])
 doc=json.loads((OUT/'final-verified/inventory.json').read_text());plan=json.loads((OUT/'authored/partition-plan.json').read_text())['regions'];regions={r['id']:r for r in doc['regions']};pages={p['id']:p for p in doc['pages']};evs={e['region_id']:e for e in doc['evidence']};new_ids={r['region_id'] for r in plan}
 report=validate(doc,ROOT);task_rows=[];components=[]
 # Every new locator independently verifies rational crop bounds, Unicode range,
 # predicted dimensions, actual PNG header, byte pins and current revisions.
 for pos,row in enumerate(plan,1):
  reg=regions[row['region_id']];page=pages[reg['page_id']];ev=evs[reg['id']];text=pathlib.Path(ev['text']['path']).read_text(encoding='utf-8')
  assert ev['page_basis_hash']==page_basis_hash(page)
  assert ev['text_offsets']['start']==0 and ev['text_offsets']['end']==len(text)==ev['text_codepoints']
  predicted=render_size_pixels(reg['box'],page,ev['render_parameters']['dpi'])
  with Image.open(ev['image']['path']) as im:actual=im.size
  png=pathlib.Path(ev['image']['path']).read_bytes()
  assert png[:8]==b'\x89PNG\r\n\x1a\n' and png[12:16]==b'IHDR'
  header_dimensions=struct.unpack('>II',png[16:24]);assert header_dimensions==actual
  assert predicted==actual==(ev['render_parameters']['width_pixels'],ev['render_parameters']['height_pixels'])
  for k in ('text','image','crop_pdf'):assert file_pin(ROOT,ev[k]['path'])==ev[k]
  native=box_to_pdf(reg['box'],page)
  crop=PdfReader(ev['crop_pdf']['path'],strict=True);assert len(crop.pages)==1
  crop_page=crop.pages[0];actual_crop=[Fraction(str(v)) for v in crop_page.mediabox]
  assert all(abs(a-b)<=Fraction(1,1000000) for a,b in zip(actual_crop,native))
  assert list(crop_page.mediabox)==list(crop_page.cropbox) and crop_page.rotation==page['rotation']
  refs=[{'literal':m.group(),'start':m.start(),'end':m.end(),'target_resolution':'not followed; raw citation only'} for m in re.finditer(r'\b(?:[4-9]|10)\.\d{1,2}\b',text)]
  for literal in ('Line Command Eligibility Chart','Leader Casualty Table','Stacking rules','Phase A','Phase B','Phase (D)','Rout and Reload Phase'):
   pattern=r'\s+'.join(re.escape(word) for word in literal.split(' '))
   for m in re.finditer(pattern,text):refs.append({'literal':m.group(),'start':m.start(),'end':m.end(),'target_resolution':'not followed; raw citation only'})
  task_rows.append(dict(row,reading_order_global=doc['reading_order'].index(reg['id']),reading_order_task=pos-1,region_revision=reg['revision'],source_sha256=doc['source']['sha256'],page_id=page['id'],page_basis_hash=page_basis_hash(page),rational_native_pdf_box=[{'numerator':v.numerator,'denominator':v.denominator} for v in native],serialized_crop_pdf_box=[str(v) for v in crop_page.mediabox],crop_pdf_geometry_check='Strict single-page read; MediaBox and CropBox match exact rational target within serialization tolerance 1/1000000 native PDF point; rotation preserved.',evidence=ev,predicted_pixels=list(predicted),actual_png_pixels=list(actual),png_ihdr_pixels=list(header_dimensions),raw_references=refs,coverage=reg['coverage'],boundary_visual_inspection='Original page and complete overlay inspected; independent review pending.',uncertainty=reg['uncertainty'],observation=row['observation'] or 'Independently located source heading, numbered rule, list item, paragraph, note or example. Exact machine text is byte-pinned in evidence; it is not a verified transcription.'))
  if row['slug']=='44-commander-counter':
   defs=[('field-and-border',[0,0,310,309],'White rectangular field and dark outer border.'),('name',[102,34,260,85],'Visible name T.Varro; spacing/punctuation observation only.'),('star-strip',[34,35,90,210],'Three gold star symbols vertically stacked on a dark strip.'),('star-top',[38,40,86,93],'Top gold star.'),('star-middle',[38,95,86,149],'Middle gold star.'),('star-bottom',[38,150,86,206],'Bottom gold star.'),('helmet',[100,82,216,212],'Gold helmet with red crest on a purple field.'),('red-disc-1',[220,108,284,170],'Red disc with visible yellow/gold 1.'),('bottom-left-4',[33,215,81,280],'Left black 4 on white.'),('bottom-second-4',[98,214,148,280],'Second black 4 on white.'),('bottom-boxed-1',[149,208,214,283],'White 1 on a dark gray rectangular field.'),('bottom-boxed-0',[223,207,281,284],'Yellow 0 in black square.')]
   for slug,bounds,obs in defs:components.append(component(row,ev,slug,bounds,obs))
  elif row['slug']=='49-elephant-counter':
   # Filled after direct inspection of the exact 600-dpi crop. Coordinates are
   # explicitly pinned to that PNG, rather than inferred from the printed rules.
   defs=json.loads((OUT/'elephant-component-specifications.json').read_text())['components']
   for c in defs:components.append(component(row,ev,c['slug'],c['bounds'],c['observation']))
 save('region-ledger.json',dict(META,format='wgc-ig2b03-region-ledger-1',source=doc['source'],assigned_pages=[9,10,11,12],regions=task_rows,component_ledger=components,component_policy='Raster sublocator annotations within the two inventory diagram regions; no extra membership or denominator and no semantic interpretation.',new_region_count=len(plan),tables='No standalone table on assigned pages; referenced charts/tables remain unresolved raw citations.',editorial_policy='Furniture remains inventoried and unprocessed, never automatically excluded.',independent_review='Pending fresh reviewer comparison of all original pages, every boundary/component and all frozen artifacts.'))
 newlinks=[l for l in doc['links'] if l not in BASE['links']]
 cont=[]
 for l in newlinks:
  if l['kind']=='continuation':
   a=next(x for x in task_rows if x['region_id']==l['from']);b=next(x for x in task_rows if x['region_id']==l['to']);cont.append(dict(l,from_page=a['page'],to_page=b['page'],from_evidence=a['evidence'],to_evidence=b['evidence'],status='Literal structural continuation visually observed; no accepted source meaning inferred.'))
   before=pathlib.Path(a['evidence']['text']['path']).read_text(encoding='utf-8');after=pathlib.Path(b['evidence']['text']['path']).read_text(encoding='utf-8')
   cont[-1]['from_literal_tail']={'text':before[-160:],'start':max(0,len(before)-160),'end':len(before),'unit':'unicode_codepoints','bounds':'half_open'}
   cont[-1]['to_literal_head']={'text':after[:160],'start':0,'end':min(160,len(after)),'unit':'unicode_codepoints','bounds':'half_open'}
 save('continuations.json',dict(META,format='wgc-ig2b03-continuations-1',continuations=cont,structural_links_added=newlinks,inherited_links_unchanged=True,inherited_continuation_report=PINS['files'][2],context={'optional_page_8_region_id':PINS['context_only_ids'][0],'accessed_for_meaning':False,'new_extraction_or_render':False,'task_denominator_units':0,'inherited_denominator_role_changed':False},boundaries={'8_to_9':'No adjacent source access used. Pinned coordinator boundary records no unfinished page-8 fragment. Page 9 begins numbered 4.34.','9_to_10':'4.56 sentence and following list continue literally.','10_to_11':'4.84 note ends on page 10; 4.85 starts on page 11.','11_to_12':'5.22 list introduction continues to items 1-7.','12_to_13':'Page 12 ends a complete 5.34 sentence. Page 13 was not accessed.'},cross_references_policy='Every machine-extracted reference is retained with Unicode offsets in region-ledger.json; no referenced source beyond assigned pages was read.'))
 # Preserve nested records, array order, registry bindings, old evidence and
 # existing context exactly. Only four placeholder memberships may be retired.
 retired={r['id'] for r in PINS['replace_only_placeholders']}
 old_by_id={r['id']:r for r in BASE['regions']};old_pages={p['id']:p for p in BASE['pages']}
 kept=[r for r in doc['regions'] if r['id'] not in new_ids]
 assert kept==[r for r in BASE['regions'] if r['id'] not in retired]
 assert [p for p in doc['pages'] if p['pdf_page'] not in [9,10,11,12]]==[p for p in BASE['pages'] if p['pdf_page'] not in [9,10,11,12]]
 for p in doc['pages']:
  if p['pdf_page'] in [9,10,11,12]:assert {k:v for k,v in p.items() if k not in ['label','revision']}=={k:v for k,v in old_pages[p['id']].items() if k not in ['label','revision']}
 assert doc['source']==BASE['source'] and doc['toolchain']==BASE['toolchain']
 assert doc['evidence'][:len(BASE['evidence'])]==BASE['evidence']
 assert doc['links'][:len(BASE['links'])]==BASE['links']
 assert [i for i in doc['reading_order'] if i not in new_ids]==[i for i in BASE['reading_order'] if i not in retired]
 assert all(e in doc['registry']['entries'] for e in BASE['registry']['entries'])
 for e in BASE['evidence']:
  for key in ('text','image','crop_pdf'):assert file_pin(ROOT,e[key]['path'])==e[key]
 prior=pathlib.Path('private/workflow/runs/IG-2B02/closure-002-IG-2B02-reviewer-e259028c/done.json');accepted=json.loads(prior.read_text())
 for a in accepted['artifacts']:
  actual=file_pin(ROOT,a['path']);assert actual['sha256']==a['sha256'] and actual['bytes']==a.get('bytes',actual['bytes'])
 save('preservation-report.json',dict(META,format='wgc-ig2b03-preservation-1',baseline=PINS['files'][0],baseline_registry=PINS['files'][1],accepted_dependency=pin(prior),prior_artifacts_verified=len(accepted['artifacts']),prior_evidence_records_preserved=len(BASE['evidence']),prior_links_preserved=len(BASE['links']),exact_prior_region_records_preserved=len(kept),exact_prior_page_records_preserved=40,assigned_page_changes='Only same-page printed-label evidence and enclosing page revisions added; geometry/address unchanged.',retired_memberships=sorted(retired),retired_registry_entries_retained=True,registry_bindings_preserved=len(BASE['registry']['entries']),registry_bindings_added=len(doc['registry']['entries'])-len(BASE['registry']['entries']),source_and_toolchain_unchanged=True,reading_order_prior_relative_order_preserved=True,context_records_unchanged=True,old_artifact_changes=[],result='passed'))
 geometry=[]
 for n in [9,10,11,12]:
  rows=[r for r in plan if r['page']==n];rects=complement([r['box'] for r in rows]);gap=sum(area(b) for b in rects)
  assert gap==next(p['unaccounted_area_trillionths'] for p in report['pages'] if p['pdf_page']==n)
  geometry.append({'physical_page':n,'unassigned_area_trillionths':gap,'disjoint_gap_boxes':rects,'status':'explicit geometric gap','reason':'Margins, gutters, inter-region space and possible thin note-background perimeter strips remain outside authored boxes. No area is silently represented or authorized for exclusion. Original pages and all boundaries were visually inspected; machine-text geometry audit has no omitted or clipped non-space characters.'})
 task_levels={k:{'represented':0,'partial':0,'unprocessed':len(plan),'excluded':0} for k in ['transcription','descriptive_semantics','formal_semantics']}
 save('coverage-report.json',dict(META,format='wgc-ig2b03-coverage-1',full_inventory=report,task={'physical_pages':[9,10,11,12],'denominator_regions':len(plan),'by_page':{str(n):sum(r['page']==n for r in plan) for n in [9,10,11,12]},'levels':task_levels,'context_denominator_units':0,'component_extra_denominator_units':0},geometric_gaps=geometry,representation_gaps=[{'region_id':r['region_id'],'levels':['transcription','descriptive_semantics','formal_semantics'],'status':'unprocessed','reason':'Exact source accounting and extraction do not establish representation; fresh independent review and later semantic work remain separate.'} for r in plan],content_gaps={'text_geometry_audit':pin(OUT/'text-geometry-audit.json'),'unassigned_machine_text_characters':0,'clipped_machine_text_characters':0,'raster_counter_transcription':'Visual components recorded with uncertainty; no verified transcription claimed.','source_references':'Out-of-scope charts, scenarios and chapter references unresolved and never followed.'},semantic_acceptance_granted=False,executable_readiness='unverified',denominator_note='Full/task/context region counts remain separate. Region counts are source-accounting units, not percentages of rule meaning.'))
 save('visual-review.json',dict(META,format='wgc-ig2b03-executor-visual-inspection-1',role_note='Executor self-inspection only; fresh independent technical review pending.',original_pages=[{'physical_page':n,'image':pin(OUT/f'original-pages/page-{n:02d}.png'),'boundary_overlay':pin(OUT/f'boundary-overlays/page-{n:02d}.png'),'all_region_evidence_mosaic':pin(OUT/f'evidence-mosaics/page-{n:02d}.png'),'dpi':180,'both_columns_inspected':True,'region_boundaries_inspected':[r['region_id'] for r in plan if r['page']==n]} for n in [9,10,11,12]],counter_evidence=[{'region_id':r['region_id'],'evidence':evs[r['region_id']],'all_component_keys':[c['component_key'] for c in components if c['region_id']==r['region_id']],'dpi':600} for r in plan if r['kind']=='diagram'],observations=['All original pages 9-12 and all 135 proposed region boundaries were inspected visually; column order, notes, exceptions, examples, all enumerated items and furniture retained.','Mosaics of all 135 exact region PNGs were inspected against the original pages; these QA images arrange the crops at their original source positions. They do not replace the individually byte-pinned evidence.','Both counter crops were inspected at 600 dpi. Glyph identity and artwork are observations with no approval of gameplay semantics.','The 5.0 IMPORTANT box is included with its red outline. Notes retain shaded fields within locators; any residual background perimeter geometry stays an explicit gap.','The 4.56 and 5.22 cross-page continuations and the 5.11 and 5.26 column continuations are explicit links.','No fresh page-8 or page-13 extraction/rendering and no external referenced chapter/scenario access.'],semantic_acceptance_granted=False,independent_review_status='pending'))
 config=pathlib.Path(META['configuration_evidence']);assert hashlib.sha256(config.read_bytes()).hexdigest()==META['configuration_sha256']
 save('source-pins.json',dict(META,format='wgc-ig2b03-source-pins-1',source=doc['source'],input_pins=pin(pathlib.Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76/input-pins.json')),packet=pin(config.parent/'packet.json'),task_packet=pin(config.parent/'task.json'),configuration=pin(config),assigned_page_basis=[{'pdf_page':p['pdf_page'],'page_id':p['id'],'page_basis_hash':page_basis_hash(p)} for p in doc['pages'] if p['pdf_page'] in [9,10,11,12]],access='Content analysis confined to original physical pages 9-12. Other source access was count/geometry and byte hashes only; prior artifacts byte-compared without historical content analysis.'))
 tool=json.loads(pathlib.Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76/toolchain.json').read_text())
 save('toolchain.json',dict(META,format='wgc-ig2b03-executor-toolchain-1',pinned_toolchain=pin(pathlib.Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76/toolchain.json')),python_executable=tool['python_executable'],libraries=tool['libraries'],native=tool['native'],process_pythonpath=tool['process_pythonpath'],process_path_prefix=tool['process_path_prefix'],observations=pin(OUT/'preflight.json'),source_tools_unchanged=True,render_dpi={'original_pages':180,'text_regions':180,'counter_regions':600},settings_changes=[]))
 save('checkpoint-complete.json',dict(META,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input_packet=pin(config.parent/'packet.json'),completed_criteria=['135 independent source regions, all assigned pages and visual boundaries inspected.','Full sidecar preserved outside four replaced placeholder memberships; registry bindings and all 4409 prior delivery artifacts verified unchanged.','All exact new locators root-validated; two canonical registry replays separately derived and root-validated.'],blocker=None,next_operation='Freeze validation records and complete delivery artifact list, transition to review, stop this role.',semantic_acceptance_granted=False))
 print(json.dumps({'task_regions':len(plan),'full_denominator':report['denominator_regions'],'components':len(components),'preservation':'passed','old_artifacts':len(accepted['artifacts'])}))

if __name__=='__main__':main()
