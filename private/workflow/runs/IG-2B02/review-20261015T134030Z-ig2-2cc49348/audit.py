import json,hashlib,copy,collections,sys
from pathlib import Path
sys.path.insert(0,'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages')
from PIL import Image,ImageDraw,ImageFont
R=Path.cwd();V=R/'private/workflow/runs/IG-2B02/review-20261015T134030Z-ig2-2cc49348';B=R/'private/workflow/runs/IG-2B02/repair-r01-r02-20261015T091559Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c';D=R/'private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8';A=R/'private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
checks={}
for n in ['authored/inventory.json','authored/identity-registry.json','final-verified/inventory.json','final-verified/identity-registry.json','final-verified/coverage.json']:checks['snapshot_exact:'+n]=(B/n).read_bytes()==(D/n).read_bytes()
x=load(B/'final-verified/inventory.json');a=load(A/'final-verified/inventory.json');reg=load(B/'final-verified/identity-registry.json');areg=load(A/'final-verified/identity-registry.json');checks['accepted_registry_preserved']=all(e in reg['entries'] for e in areg['entries'])
pageids={p['id']:p['pdf_page'] for p in x['pages']}
checks['prior_pages_exact']=all(p in x['pages'] for p in a['pages'] if p['pdf_page'] not in range(5,9))
checks['prior_regions_exact']=all(r in x['regions'] for r in a['regions'] if pageids[r['page_id']] not in range(5,9) or r['denominator_role']=='context')
checks['prior_evidence_exact']=all(e in x['evidence'] for e in a['evidence']);checks['prior_links_exact']=all(e in x['links'] for e in a['links'])
l=load(B/'region-ledger-final.json');old=load(D/'region-ledger-final.json');spec=load(B/'author-specifications-final.json');ospec=load(D/'author-specifications-final.json');obs=load(B/'component-observations.json');oobs=load(D/'component-observations.json')
deltas=[]
for i,(r,o) in enumerate(zip(l['regions'],old['regions'])):
 rc=copy.deepcopy(r);oc=copy.deepcopy(o);rc.pop('components');oc.pop('components');checks['row_noncomponents_exact:'+str(i)]=rc==oc
 if r['components']!=o['components']:deltas.append({'index':i,'key':r['region']['key'],'before':o['components'],'after':r['components']})
 sm={s['key']:s for s in spec['specifications']};checks['effective_components:'+str(i)]=r['components']==obs['corrections_after_enlargement'].get(r['region']['key'],sm[r['region']['key']]['components'])
 checks['canonical_row:'+str(i)]=r['region'] in x['regions']
checks['three_component_deltas_only']=set(z['key'] for z in deltas)=={'ig2b02:p5:alae:counter','ig2b02:p5:light-infantry:counter','ig2b02:p5:javelinists:counter'}
specdiff=[i for i,(s,o) in enumerate(zip(spec['specifications'],ospec['specifications'])) if s!=o];checks['spec_deltas_match']=specdiff==[5,24,28]
for i in specdiff:
 s=copy.deepcopy(spec['specifications'][i]);o=copy.deepcopy(ospec['specifications'][i]);s.pop('components');o.pop('components');checks['spec_noncomponents:'+str(i)]=s==o
checks['prior_seven_overrides_exact']=all(obs['corrections_after_enlargement'][k]==v for k,v in oobs['corrections_after_enlargement'].items())
reports=['scope-report-final.json','context-authored-correspondence.json','continuations.json','uncertainty.json','gaps.json','geometric-gaps.json','locator-audit.json']
for n in reports:
 t=load(B/n);checks['report_baseline_exact:'+n]=t['baseline_payload']==load(D/n)
checks['task_counts']=collections.Counter(r['pdf_page'] for r in l['regions'])=={5:39,6:33,7:39,8:30}
checks['full_denominator']=sum(r['denominator_role']=='inventory' for r in x['regions'])==307
checks['context_count']=sum(r['denominator_role']=='context' for r in x['regions'])==1
checks['no_new_promotions']=all(c['gap'] and c['status'] in ['partial','unprocessed'] for r in l['regions'] for c in r['region']['coverage'].values())
checks['all_44_pages']=len(x['pages'])==44
checks['reading_order_complete']=set(x['reading_order'])=={r['id'] for r in x['regions']} and len(x['reading_order'])==308
report=dict(checks=checks,failures=[k for k,v in checks.items() if not v],component_deltas=deltas,prior_registry_entries=len(areg['entries']),accepted_evidence_count=len(a['evidence']))
(V/'independent-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
# Independent originals with every boundary, numbered by full ledger index.
for p in range(5,9):
 im=Image.open(V/f'original-{p:02}.png').convert('RGB');draw=ImageDraw.Draw(im)
 for i,r in enumerate(l['regions']):
  if r['pdf_page']!=p:continue
  box=tuple(round(v/1000000*(im.width if j%2==0 else im.height)) for j,v in enumerate(r['region']['box']))
  draw.rectangle(box,outline=(230,0,170),width=1);draw.text((box[0],box[1]),str(i),fill=(0,0,255),stroke_width=1,stroke_fill='white')
 im.save(V/f'boundaries-{p:02}.png')
# Every grouped diagram: independent original enlargement adjacent to submitted raw PNG.
diags=[(i,r) for i,r in enumerate(l['regions']) if r['region']['kind']=='diagram']
for part in range((len(diags)+5)//6):
 sheet=Image.new('RGB',(1050,6*250),'white');dr=ImageDraw.Draw(sheet)
 for row,(i,r) in enumerate(diags[part*6:part*6+6]):
  im=Image.open(V/f"original-{r['pdf_page']:02}.png");box=tuple(round(v/1000000*(im.width if j%2==0 else im.height)) for j,v in enumerate(r['region']['box']));crop=im.crop(box);crop.thumbnail((450,200));crop=crop.resize((crop.width*min(3,450//max(1,crop.width)),crop.height*min(3,450//max(1,crop.width))))
  raw=Image.open(R/r['evidence']['image']['path']);raw.thumbnail((450,200));factor=min(3,450//max(1,raw.width));raw=raw.resize((raw.width*factor,raw.height*factor))
  sheet.paste(crop,(0,row*250+35));sheet.paste(raw,(525,row*250+35));dr.text((0,row*250),f'{i} {r["region"]["key"]} ORIGINAL | SUBMITTED',fill='black')
 sheet.save(V/f'diagrams-{part+1}.png')
print('diagram_count',len(diags))

