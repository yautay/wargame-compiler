import json, subprocess, sys, math, collections
from fractions import Fraction
from PIL import Image, ImageDraw
import pdfplumber
from verify import ROOT, OUT, BASE, META, load, save, sha

inventory=load(BASE/'final-verified/inventory.json')
ledger=load(BASE/'region-ledger.json')
components=load(BASE/'component-ledger.json')
replay=load(BASE/'registry-replay-report.json')
checks=[]
for build in replay['verified_builds']+replay['component_builds_and_two_replays']:
    path=build['inventory']['path']
    cmd=['.venv/Scripts/python.exe','-B','-m','wgc.sources','validate',path]
    p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
    name='root-'+build['name']
    (OUT/(name+'.log')).write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
    result=json.loads(p.stdout) if p.returncode==0 else None
    record=dict(command=' '.join(cmd),exit_code=p.returncode,source_structure_verification=result.get('source_structure_verification') if result else None,log=(OUT/(name+'.log')).relative_to(ROOT).as_posix())
    checks.append(record)
    print(name,p.returncode,record['source_structure_verification'],flush=True)

errors=[]
for x in ledger['regions']+components['components']:
    e=x['evidence']; region=x['region']
    text=(ROOT/e['text']['path']).read_text(encoding='utf-8')
    pixels=Image.open(ROOT/e['image']['path']).size
    if 'raw_extracted_text' in x and text!=x['raw_extracted_text']: errors.append([region['id'],'raw text mismatch'])
    if e['text_codepoints']!=len(text) or e['text_offsets']!=dict(bounds='half_open',end=len(text),start=0,unit='unicode_codepoints'): errors.append([region['id'],'codepoint offsets'])
    page=next(p for p in inventory['pages'] if p['id']==region['page_id'])
    if e['region_id']!=region['id'] or e['region_revision']!=region['revision'] or e['box']!=region['box'] or e['pdf_page']!=page['pdf_page']: errors.append([region['id'],'locator mismatch'])
    a=region['box']; dpi=e['render_parameters']['dpi']
    # All assigned original pages are unrotated 612 by 792 PDF points, UserUnit 1.
    expected=(math.ceil(float(Fraction((a[2]-a[0])*612*dpi,1000000*72))),math.ceil(float(Fraction((a[3]-a[1])*792*dpi,1000000*72))))
    if pixels!=expected or list(pixels)!=x['actual_png_pixels'] or list(expected)!=x['predicted_pixels']: errors.append([region['id'],'pixels mismatch'])
    bounds=[Fraction(a[0]*612,1000000),Fraction((1000000-a[3])*792,1000000),Fraction(a[2]*612,1000000),Fraction((1000000-a[1])*792,1000000)]
    if [str(b) for b in bounds]!=x['native_pdf_bounds_rational']: errors.append([region['id'],'rational crop mismatch'])
    if region['denominator_role'] != ('context' if 'parent_region_id' in x else 'inventory'): errors.append([region['id'],'denominator role'])
    if any(c['status']!='unprocessed' or c['gap'] is not True for c in region['coverage'].values()): errors.append([region['id'],'coverage promotion'])
save('locator-audit.json',dict(checked_regions=len(ledger['regions']),checked_components=len(components['components']),errors=errors,checks=checks,semantic_acceptance_granted=False))

report=load(BASE/'coverage-report.json')
page_reports=[]
with pdfplumber.open(ROOT/inventory['source']['pdf']['path']) as pdf:
    for number in [9,10,11,12]:
        page=pdf.pages[number-1]
        entries=[r for r in ledger['regions'] if r['pdf_page']==number]
        boxes=[r['region']['box'] for r in entries]
        chars=[c for c in page.chars if c['text'].strip()]
        outside=[]
        for c in chars:
            b=[c['x0']/page.width*1000000,c['top']/page.height*1000000,c['x1']/page.width*1000000,c['bottom']/page.height*1000000]
            if not any(a[0]<=b[0] and a[1]<=b[1] and a[2]>=b[2] and a[3]>=b[3] for a in boxes): outside.append(dict(text=c['text'],box=b))
        # Independent exact sweep decomposition of every geometric gap.
        xs=sorted({0,1000000,*[a[i] for a in boxes for i in [0,2]]})
        gaps=[]
        for left,right in zip(xs,xs[1:]):
            intervals=sorted((a[1],a[3]) for a in boxes if a[0]<=left and a[2]>=right)
            cursor=0
            for top,bottom in intervals:
                assert top>=cursor
                if cursor<top:gaps.append([left,cursor,right,top])
                cursor=bottom
            if cursor<1000000:gaps.append([left,cursor,right,1000000])
        area=sum((a[2]-a[0])*(a[3]-a[1]) for a in gaps)
        pinned=next(p for p in report['task']['geometric_gaps'] if p['pdf_page']==number)
        original_equal=sha(OUT.relative_to(ROOT)/'original-pages'/f'page-{number:02}.png')==sha(BASE/'original-pages'/f'page-{number:02}.png')
        page_reports.append(dict(pdf_page=number,regions=len(entries),nonspace_characters=len(chars),outside=outside,gap_area=area,gap_count=len(gaps),gap_partition_matches=set(map(tuple,gaps))==set(map(tuple,pinned['geometric_gap_rectangles'])),gap_area_matches=area==pinned['unaccounted_area_trillionths'],fresh_original_render_matches_delivery=original_equal))
save('geometry-audit.json',dict(pages=page_reports,semantic_acceptance_granted=False,access_scope='Content extraction and rendering restricted to original physical pages 9-12. Other pages only structural metadata/hash comparisons. Optional page-8 content not read. No cross-chapter reference followed.'))

for number,offset in [(9,(350,2360)),(11,(350,1048))]:
    image=Image.open(OUT/'original-pages'/f'counter-{number:02}.png').convert('RGB')
    draw=ImageDraw.Draw(image)
    for index,x in enumerate(components['components']):
        if x['page']!=number:continue
        a=x['box']; b=(a[0]*5100/1000000-offset[0],a[1]*6600/1000000-offset[1],a[2]*5100/1000000-offset[0],a[3]*6600/1000000-offset[1])
        draw.rectangle(b,outline='red',width=1); draw.text((b[0],b[1]),str(index),fill='blue')
    image.save(OUT/'original-pages'/f'component-boundaries-{number:02}.png')
print('locator errors',errors,flush=True)
print('geometry',json.dumps([{k:v for k,v in p.items() if k!='outside'} for p in page_reports]),flush=True)
assert not errors and all(p['gap_partition_matches'] and p['gap_area_matches'] and not p['outside'] and p['fresh_original_render_matches_delivery'] for p in page_reports)
assert all(c['exit_code']==0 for c in checks)
