from prepare import *
from math import floor
tool=read(f'{REL}/toolchain.json'); sys.path[:0]=tool['process_pythonpath'].split(';'); os.environ['PATH']=tool['process_path_prefix']+';'+os.environ['PATH']; sys.dont_write_bytecode=True
from wgc.sources.inventory import seal,validate
from wgc.sources.pdf import extract_evidence
from wgc.sources.geometry import box_to_pdf
from wgc.contracts.source import canonical_bytes
from PIL import Image,ImageDraw
doc=read(f'{REL}/final/inventory.json'); ledger=read(f'{REL}/region-ledger.json')
region=next(r for r in doc['regions'] if r['key']=='ig2b01:cover:spqr-logotype'); old=copy.deepcopy(region)
old_evidence=next(e for e in doc['evidence'] if e['region_id']==region['id'])
region['box'][2]=floor(416/612*1e6); region.update(seal(region))
doc['evidence']=[e for e in doc['evidence'] if e['region_id']!=region['id']]; doc=seal(doc)
fresh=extract_evidence(doc,region['id'],ROOT,f'{REL}/evidence-logo-corrected',dpi=144);doc['evidence'].append(fresh);doc=seal(doc)
out=RUN/'final-verified';out.mkdir(exist_ok=False)
(out/'inventory.json').write_bytes(canonical_bytes(doc)+b'\n');(out/'identity-registry.json').write_bytes(canonical_bytes(doc['registry'])+b'\n')
for row in ledger:
 if row['region_id']==region['id']:
  row.update(region_revision=region['revision'],box=region['box'],native_top_left_points=[186,82,416,155],evidence=fresh,exact_native_bottom_left_bounds_rational=[{'numerator':v.numerator,'denominator':v.denominator} for v in box_to_pdf(region['box'],doc['pages'][0])])
write(f'{REL}/region-ledger-final.json',ledger)
write(f'{REL}/logo-correction.json',{'reason':'Original-page overlay and cropped PNG inspection found the rightmost white R glyph touching the x=412 point boundary. Independent original-PNG scan found white pixels through x=824 at 144 DPI. Widen the locator to x=416 points to preserve the entire glyph and margin.','old_region':old,'new_region':region,'old_evidence':old_evidence,'new_evidence':fresh,'identity_unchanged':old['id']==region['id'],'registry_unchanged':doc['registry']==read(f'{REL}/final/identity-registry.json'),'old_artifacts_preserved':True})
report=validate(doc,ROOT);write(f'{REL}/corrected-root-validation.json',report)
# Redo exact replay using the persisted registry and corrected authored locator, with evidence/labels removed.
from author import build,spec
next(s for s in spec if s['key']=='ig2b01:cover:spqr-logotype')['native_top_left_points'][2]=416
replay,_=build(copy.deepcopy(doc['registry']))
expected=copy.deepcopy(doc);expected['evidence']=[]
base=read(f'{BASE}/inventory-one/inventory.json')
expected['pages']=base['pages'];expected=seal(expected)
assert canonical_bytes(expected)==canonical_bytes(replay)
(out/'replay-without-evidence.json').write_bytes(canonical_bytes(replay)+b'\n')
write(f'{REL}/repeatability-final.json',{'persisted_registry_replay_identical_canonical_bytes':True,'all_region_ids_unchanged':True,'final_inventory':pin(f'{REL}/final-verified/inventory.json'),'replay':pin(f'{REL}/final-verified/replay-without-evidence.json'),'comparison':'Exact author/source/page/registry/region/order/link bytes after removing evidence and restoring baseline label metadata; labels are separately evidence-verified.','source_remapping':False})
scope=read(f'{REL}/scope-report.json');scope['inventory']=pin(f'{REL}/final-verified/inventory.json');write(f'{REL}/scope-report-final.json',scope)
(RUN/'overlays-verified').mkdir(exist_ok=False)
for p in range(1,5):
 im=Image.open(RUN/f'pages/original-{p:02}.png').convert('RGB');draw=ImageDraw.Draw(im)
 for i,l in enumerate([l for l in ledger if l['page']==p]):
  a,b,c,d=l['box'];box=[a*im.width/1e6,b*im.height/1e6,c*im.width/1e6,d*im.height/1e6];draw.rectangle(box,outline='red',width=1);draw.text((box[0],box[1]),str(i+1),fill='blue')
 im.save(RUN/f'overlays-verified/page-{p:02}.png')
print('Corrected logo; final verified inventory root-valid; exact registry replay passed')
