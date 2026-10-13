"""Read-only quote/glyph locator diagnostics; no rule extraction/correction."""
from pathlib import Path
import json,hashlib,re,math
from PIL import Image,ImageDraw,ImageFont
import pdfplumber
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
C=load(R/'checklist.json');ids=load(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json')['parts'][2]['evidence_ids'];V=M/'visual';V.mkdir(exist_ok=False)
assert ref(ROOT/C['source']['path'])==C['source']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
rows=[]
scope=load(P/'transfer/context-v1/context/pass-01/evidence/8.46-step-4-scope.json')
assert ref(ROOT/scope['full_render']['path'])==scope['full_render']
with Image.open(ROOT/scope['full_render']['path']) as metadata_only: full_dimensions=metadata_only.size
offset=scope['pixel_bbox_on_reviewer_render'][:2]
def pattern(q):
    parts=[]
    for ch in q:
        if ch.isspace():parts.append(r'\s+')
        elif ch.isalpha():parts.append(re.escape(ch)+r'(?:[-\u00ad]\s*)?')
        else:parts.append(re.escape(ch))
    return ''.join(parts)
with pdfplumber.open(ROOT/C['source']['path']) as pdf:
    for eid in ids:
        e=C['output_records']['context-01'][eid]['original_record'];runs=[r for r in C['responses'] if eid in C['output_records'][r]]
        if len(runs)==2:
            other=C['output_records']['first-001'][eid]['original_record'];assert e['quote']==other['quote'] and e['image']==other['image']
        page=pdf.pages[e['pdf_page']-1];assert e['pdf_page'] in [27,36,37]
        im=Image.open(P/e['image']['path']).convert('RGB');w,h=im.size;b=e['image']['bbox'];assert ref(P/e['image']['path'])['sha256']==e['image']['sha256']
        iscontext=e['pdf_page']==27
        if iscontext:
            assert runs==['context-01'] and (w,h)==(433,395)
            sx=page.width/full_dimensions[0];sy=page.height/full_dimensions[1];ox,oy=offset
            supplied=scope['pixel_bbox_on_reviewer_render'];clip=[supplied[0]*sx,supplied[1]*sy,supplied[2]*sx,supplied[3]*sy]
            searchpage=page.crop(tuple(clip)) # Read only the already supplied Step4 pixels' scope.
        else:
            sx=page.width/w;sy=page.height/h;ox=oy=0;clip=None
            searchpage=page.crop((0,0,page.width/2,page.height)) if b[0]<w/2 else page.crop((page.width/2,0,page.width,page.height))
        box=[(b[0]+ox)*sx,(b[1]+oy)*sy,(b[2]+ox)*sx,(b[3]+oy)*sy]
        q=e['quote']['value']
        hits=searchpage.search(pattern(q),regex=True,case=True,return_chars=True,x_tolerance=2,y_tolerance=3)
        assert len(hits)==1,(eid,len(hits))
        hit=hits[0];chars=hit['chars'];clipped=[]
        for index,c in enumerate(chars):
            if not (box[0]<=c['x0'] and c['x1']<=box[2] and box[1]<=c['top'] and c['bottom']<=box[3]):
                px=[c['x0']/sx-ox,c['top']/sy-oy,c['x1']/sx-ox,c['bottom']/sy-oy]
                ink=[];gray=im.convert('L')
                for y in range(max(0,math.floor(px[1])),min(h,math.ceil(px[3]))):
                    for x in range(max(0,math.floor(px[0])),min(w,math.ceil(px[2]))):
                        if not(b[0]<=x<b[2] and b[1]<=y<b[3]) and gray.getpixel((x,y))<100:ink.append([x,y])
                clipped.append(dict(index=index,text=c['text'],bbox_pdf_points=[c['x0'],c['top'],c['x1'],c['bottom']],bbox_pixels=px,
                    overflow_pdf_points=dict(left=max(0,box[0]-c['x0']),right=max(0,c['x1']-box[2]),top=max(0,box[1]-c['top']),bottom=max(0,c['bottom']-box[3])),
                    dark_pixels_outside_original_crop=len(ink),dark_pixels_sample=ink[:12],pixel_diagnostic_limitation='Threshold100 over glyph envelope, includes antialias/background effects; not a font-outline or semantic certificate.'))
        exact=im.crop(tuple(b));exactpath=V/f'{eid}-exact.png';exact.save(exactpath)
        qpx=[hit['x0']/sx-ox,hit['top']/sy-oy,hit['x1']/sx-ox,hit['bottom']/sy-oy]
        # Reference quote region is diagnostic comparison, never a repaired locator.
        rect=[max(0,math.floor(qpx[0])-10),max(0,math.floor(qpx[1])-8),min(w,math.ceil(qpx[2])+10),min(h,math.ceil(qpx[3])+8)]
        reference=im.crop(tuple(rect));dr=ImageDraw.Draw(reference)
        for x in [b[0],b[2]]:
            if rect[0]<=x<=rect[2]:dr.line((x-rect[0],0,x-rect[0],reference.height-1),fill='red',width=1)
        for y in [b[1],b[3]]:
            if rect[1]<=y<=rect[3]:dr.line((0,y-rect[1],reference.width-1,y-rect[1]),fill='red',width=1)
        canvas=Image.new('RGB',(max(740,reference.width+20),reference.height+34),'white');canvas.paste(reference,(10,30));ImageDraw.Draw(canvas).text((10,5),f'{eid} | page{e["pdf_page"]} | original bbox red; reference beyond bbox is NOT accepted crop',font=font,fill='black')
        compare=V/f'{eid}-quote-reference.png';canvas.save(compare)
        for j,c in enumerate(clipped):
            x0,y0,x1,y1=c['bbox_pixels'];small=[max(0,math.floor(x0)-8),max(0,math.floor(y0)-4),min(w,math.ceil(x1)+8),min(h,math.ceil(y1)+4)]
            patch=im.crop(tuple(small));d=ImageDraw.Draw(patch)
            for x in [b[0],b[2]]:
                if small[0]<=x<=small[2]:d.line((x-small[0],0,x-small[0],patch.height-1),fill='red',width=1)
            for y in [b[1],b[3]]:
                if small[1]<=y<=small[3]:d.line((0,y-small[1],patch.width-1,y-small[1]),fill='red',width=1)
            patch=patch.resize((patch.width*6,patch.height*6),Image.Resampling.NEAREST)
            path=V/f'{eid}-boundary-{j}.png';patch.save(path);c['magnified_boundary_patch']=ref(path)
        row=dict(evidence_id=eid,pdf_page=e['pdf_page'],source_image=ref(P/e['image']['path']),source=C['source'],quote=q,
            original_bbox_pixels=b,actual_dimensions=[w,h],bbox_pdf_points=box,page_dimensions_pdf_points=[page.width,page.height],
            source_quote_match=dict(text=hit['text'],bbox_pdf_points=[hit['x0'],hit['top'],hit['x1'],hit['bottom']],bbox_pixels=qpx,char_count=len(chars)),
            quote_glyphs_outside_box=clipped,quote_whole_glyph_envelopes_contained=(not clipped),exact_crop=ref(exactpath),quote_reference=ref(compare),quote_reference_area_pixels=rect,
            runs=runs,both_runs_original_quote_and_image_equal=True if len(runs)==2 else 'not_applicable_context_only',coordinate_mapping=dict(scale_pdf_points_per_pixel=[sx,sy],pixel_offset_on_render=[ox,oy],allowed_pdf_clip=clip,scope_artifact=ref(P/'transfer/context-v1/context/pass-01/evidence/8.46-step-4-scope.json') if iscontext else None),visual_review='pending_manual',geometry='Coordinates in bounds and image hash/dimensions verified; does not imply quote coverage.')
        rows.append(row)
        print(eid,'chars',len(chars),'outside envelopes',[(x['text'],round(max(x['overflow_pdf_points'].values()),4),x['dark_pixels_outside_original_crop']) for x in clipped])
data=dict(id='M-POC5A.4c3-locator-diagnostics-01',source=C['source'],responses=C['responses'],scope_plan=ref(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json'),
    tools=dict(pdfplumber=pdfplumber.__version__,pillow=Image.__version__),method='Search only22 original short quotes in suppliedPDF36–37 and suppliedStep4crop27; no text/image outside that crop on27. No new rule extraction; no original changes/tolerance expansion. Character envelopes are distinct from raster ink/readability.',rows=rows)
assert not (M/'locator-diagnostics.json').exists();(M/'locator-diagnostics.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
