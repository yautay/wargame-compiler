"""Audit exact current ledger, locators and preserved scope without content outside scope."""
from collections import Counter
from fractions import Fraction
from math import ceil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
from wgc.contracts.source import canonical_bytes
import hashlib
import json
import importlib.util

spec = importlib.util.spec_from_file_location('review_tools',Path(__file__).with_name('review-tools.py'))
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)
read, pin, write = rt.read, rt.pin, rt.write
BASE, OUT = rt.BASE, rt.OUT
inventory = read(BASE/'final-verified/inventory.json')
ledger = read(BASE/'region-ledger-final.json')
accepted_path=Path('private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77/final-verified/inventory.json')
assert pin(accepted_path)['sha256']=='42adf9a1598bd682917eb087e295fe899212e59dd81aed5c293e2187b9c587bb'
accepted=read(accepted_path)
accepted_registry_path=accepted_path.with_name('identity-registry.json')
assert pin(accepted_registry_path)['sha256']=='94ac81cac947342b7de757419d9b858f45cdae2f2eae521ce94404e0e7831657'
assert read(accepted_registry_path)==accepted['registry']
pages={p['id']:p for p in inventory['pages']}
regions={r['id']:r for r in inventory['regions']}
evidence={e['id']:e for e in inventory['evidence']}
checks=[]

def require(name,condition,details=None):
    checks.append({'name':name,'passed':bool(condition),'details':details})
    assert condition,name

def digest(v):
    return hashlib.sha256(canonical_bytes(v)).hexdigest()

def geometry(box,p,dpi):
    x0,y0,x1,y1=[Fraction(x,1000000) for x in p['effective_crop_box']]
    width,height=x1-x0,y1-y0
    native=[x0+width*box[0]/1000000,y1-height*box[3]/1000000,x0+width*box[2]/1000000,y1-height*box[1]/1000000]
    unit=Fraction(p['user_unit']['numerator'],p['user_unit']['denominator'])
    w,h=(native[2]-native[0])*unit,(native[3]-native[1])*unit
    if p['rotation'] in (90,270):w,h=h,w
    return native,(ceil(float(w)*dpi/72),ceil(float(h)*dpi/72))

require('44 physical pages retained',len(pages)==44 and {p['pdf_page'] for p in pages.values()}==set(range(1,45)))
unchanged_pages=[p for p in accepted['pages'] if p['pdf_page'] not in (5,6,7,8)]
require('accepted pages 1-4 and placeholders 9-44 exactly preserved',all(pages[p['id']]==p for p in unchanged_pages),{'pages':len(unchanged_pages)})
old_regions=[r for r in accepted['regions'] if pages[r['page_id']]['pdf_page'] not in (5,6,7,8) or r['denominator_role']=='context']
require('all accepted nonretired regions exactly preserved',all(regions[r['id']]==r for r in old_regions),{'regions':len(old_regions)})
retired=[r for r in accepted['regions'] if r not in old_regions]
require('only original 5-8 placeholder memberships retired',len(retired)==4 and all(r['id'] not in regions for r in retired))
require('all prior evidence and links exact',all(evidence[e['id']]==e for e in accepted['evidence']) and all(link in inventory['links'] for link in accepted['links']),{'evidence':len(accepted['evidence']),'links':len(accepted['links'])})
require('registry extends without remap',all(e in inventory['registry']['entries'] for e in accepted['registry']['entries']),{'prior_entries':len(accepted['registry']['entries']),'current_entries':len(inventory['registry']['entries'])})
require('current registry sidecar equals nested registry',read(BASE/'final-verified/identity-registry.json')==inventory['registry'])
require('full ledger exact region set',len(ledger['regions'])==141 and {r['region']['id'] for r in ledger['regions']}=={r['id'] for r in regions.values() if r['key'].startswith('ig2b02:')} )
author=read(BASE/'author-specifications-final.json')
specs={s['key']:s for s in author['specifications']}
components=read(BASE/'component-observations.json')['corrections_after_enlargement']
locators=[]
for i,row in enumerate(ledger['regions']):
    r=row['region']; e=row['evidence']; p=pages[r['page_id']]; s=specs[r['key']]
    require('ledger-current-exact:'+r['key'],regions[r['id']]==r and evidence[e['id']]==e and row['pdf_page']==p['pdf_page'] and inventory['reading_order'][row['reading_order_index']]==r['id'])
    require('component-authority:'+r['key'],row['components']==components.get(r['key'],s['components']) and row['label']==s['label'])
    basis={k:p[k] for k in ('id','key','source_revision','pdf_page','media_box','crop_box','effective_crop_box','rotation','user_unit')}
    native,pixels=geometry(r['box'],p,e['render_parameters']['dpi'])
    require('rational-bounds:'+r['key'],native==[Fraction(v['numerator'],v['denominator']) for v in row['native_crop_bounds']])
    require('page-basis:'+r['key'],e['page_basis_hash']==digest(basis))
    png=Image.open(e['image']['path'])
    require('png-size:'+r['key'],pixels==png.size==(e['render_parameters']['width_pixels'],e['render_parameters']['height_pixels']))
    text=Path(e['text']['path']).read_bytes().decode('utf-8')
    require('unicode-offsets:'+r['key'],len(text)==e['text_codepoints']==row['raw_text_codepoints'] and e['text_offsets']=={'unit':'unicode_codepoints','bounds':'half_open','start':0,'end':len(text)})
    require('evidence-byte-pins:'+r['key'],all(pin(e[k]['path'])==e[k] for k in ('text','image','crop_pdf')))
    crop=PdfReader(e['crop_pdf']['path'],strict=True).pages[0]
    require('crop-pdf-geometry:'+r['key'],all(abs(float(a)-float(b))<0.000001 for a,b in zip(crop.cropbox,native)) and int(crop.get('/Rotate',0))==p['rotation'])
    require('coverage-gaps:'+r['key'],all(c['gap'] and c['reason'] and c['boundary'] is None for c in r['coverage'].values()) and r['coverage']['transcription']['status']=='partial' and all(r['coverage'][level]['status']=='unprocessed' for level in ('descriptive_semantics','formal_semantics')))
    require('ledger-links:'+r['key'],all(link in inventory['links'] for link in row['links']))
    locators.append({'index':i,'key':r['key'],'region':{'id':r['id'],'revision':r['revision']},'pdf_page':p['pdf_page'],'box':r['box'],'components':row['components'],'uncertainty':r['uncertainty'],'evidence':e['id'],'text_pin':e['text'],'native_crop_bounds':row['native_crop_bounds'],'png_pixels':pixels,'passed':True})

task_counts=Counter(row['pdf_page'] for row in ledger['regions'])
require('task counts',dict(task_counts)=={5:39,6:33,7:39,8:30})
full=[r for r in inventory['regions'] if r['denominator_role']=='inventory']
context=[r for r in inventory['regions'] if r['denominator_role']=='context']
require('denominators task/full/context',len(full)==307 and len(context)==1)
counts={level:dict(Counter(r['coverage'][level]['status'] for r in full)) for level in ('transcription','descriptive_semantics','formal_semantics')}
require('no source representation or exclusion promotions',counts=={'transcription':{'partial':271,'unprocessed':36},'descriptive_semantics':{'unprocessed':307},'formal_semantics':{'unprocessed':307}})
corr=read(BASE/'context-authored-correspondence.json')['baseline_payload']
require('exact context correspondence',regions[corr['context']['id']]==corr['context'] and regions[corr['authored']['id']]==corr['authored'] and corr['context']['id']!=corr['authored']['id'] and corr['context_denominator']==0 and corr['authored_denominator']==1 and all(link in inventory['links'] for link in corr['preserved_prior_links']+corr['new_source_observed_link']))
continuation=read(BASE/'continuations.json')['baseline_payload']
require('no page-9 content access recorded',continuation['page_9']['accessed'] is False and author['page_9_access'].startswith('Not'))

replay=read(BASE/'replay-report.json')
replay_pairs=[]
for run in replay['runs']:
    for row in run['files']:
        current=pin(row['current']['path']); replayed=pin(row['replayed']['path'])
        require('frozen replay:'+row['replayed']['path'],current==row['current'] and replayed==row['replayed'] and current['sha256']==replayed['sha256'])
        replay_pairs.append({'current':current,'replayed':replayed,'byte_identical':True})

for page_no in (5,6,7,8):
    im=Image.open(OUT/f'original-{page_no:02}.png').convert('RGB')
    draw=ImageDraw.Draw(im)
    font=ImageFont.load_default(size=14)
    for i,row in enumerate(ledger['regions']):
        if row['pdf_page']!=page_no:continue
        x0,y0,x1,y1=row['region']['box']
        box=(x0*im.width/1e6,y0*im.height/1e6,x1*im.width/1e6,y1*im.height/1e6)
        draw.rectangle(box,outline='#de4500',width=1)
        draw.text((box[0]-23,box[1]),str(i),fill='#c52b00',font=font,stroke_width=1,stroke_fill='white')
    im.save(OUT/f'boundaries-{page_no:02}.png')

diagrams=[(i,row) for i,row in enumerate(ledger['regions']) if row['region']['kind']=='diagram']
sheet=Image.new('RGB',(1000,ceil(len(diagrams)/4)*280),'white')
draw=ImageDraw.Draw(sheet)
for n,(i,row) in enumerate(diagrams):
    crop=Image.open(row['evidence']['image']['path']).convert('RGB')
    crop.thumbnail((230,230))
    if crop.height<130:
        crop=crop.resize((int(crop.width*2.5),int(crop.height*2.5)))
        crop.thumbnail((230,230))
    x=(n%4)*250; y=(n//4)*280
    sheet.paste(crop,(x,y))
    draw.text((x,y+235),f"{i}: {row['region']['key'][8:]}",fill='black')
sheet.save(OUT/'diagram-components.png')
report=write('independent-audit.json',{'basis':'Independent current record/byte/geometry comparisons; all source content reads restricted to 5-8 and exact named continuation crop. Preserved earlier scope compared as data only. Replay files verified from the immutable delivery, not regenerated by this reviewer.','accepted_baseline':pin(accepted_path),'snapshot':pin(BASE/'final-verified/inventory.json'),'ledger':pin(BASE/'region-ledger-final.json'),'checks':checks,'all_passed':True,'counts':{'task':141,'full':307,'context':0,'preserved_authored':130,'placeholders':36,'task_by_page':dict(task_counts)},'coverage':counts,'locators':locators,'preserved_replay_pairs':replay_pairs,'new_original_renders':[pin(OUT/f'original-{n:02}.png') for n in (5,6,7,8)],'new_boundaries':[pin(OUT/f'boundaries-{n:02}.png') for n in (5,6,7,8)],'diagram_sheet':pin(OUT/'diagram-components.png')})
print(json.dumps({'report':report,'checks':len(checks),'all_passed':True}))
