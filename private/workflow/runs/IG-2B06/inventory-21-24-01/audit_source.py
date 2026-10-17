"""Bounded original-source area, text-center and raster accounting."""
import math
from PIL import Image,ImageDraw
import pdfplumber
from author import ROOT,RUN,load,report
from wgc.sources.inventory import file_pin

spec=load(RUN/'authored-corrected/regions.json')['regions']
pages=[]
pdf=load(RUN/'authored-corrected/inventory.json')['source']['pdf']
with pdfplumber.open(ROOT/pdf['path']) as source:
    for p in (21,22,23,24):
        ss=[s for s in spec if s['page']==p];boxes=[s['box'] for s in ss]
        ys=sorted({0,1000000,*[b[i] for b in boxes for i in (1,3)]})
        gaps=[]
        for y0,y1 in zip(ys,ys[1:]):
            intervals=sorted((b[0],b[2]) for b in boxes if b[1]<=y0 and b[3]>=y1)
            x=0
            for a,b in intervals:
                assert a>=x
                if a>x:gaps.append([x,y0,a,y1])
                x=b
            if x<1000000:gaps.append([x,y0,1000000,y1])
        region_area=sum((b[2]-b[0])*(b[3]-b[1]) for b in boxes)
        gap_area=sum((b[2]-b[0])*(b[3]-b[1]) for b in gaps)
        assert region_area+gap_area==10**12
        chars=[c for c in source.pages[p-1].chars if c['text'].strip()]
        missing=[]
        for c in chars:
            x=(c['x0']+c['x1'])/2/612*1e6;y=(c['top']+c['bottom'])/2/792*1e6
            if not any(b[0]<=x<b[2] and b[1]<=y<b[3] for b in boxes):missing.append(dict(text=c['text'],x=x,y=y))
        assert not missing
        image=Image.open(RUN/f'inspection/page-{p}.png').convert('RGB');w,h=image.size
        mask=Image.new('1',(w,h));draw=ImageDraw.Draw(mask)
        overlay=image.copy();od=ImageDraw.Draw(overlay)
        for n,s in enumerate(ss):
            b=s['box'];rect=(math.floor(b[0]*w/1e6),math.floor(b[1]*h/1e6),math.ceil(b[2]*w/1e6)-1,math.ceil(b[3]*h/1e6)-1)
            draw.rectangle(rect,fill=1);od.rectangle(rect,outline=(225,0,190),width=1)
        overlay.save(RUN/f'inspection/overlay-{p}.png')
        pix=image.load();m=mask.load();counts={190:0,240:0,254:0}
        for y in range(h):
            for x in range(w):
                if not m[x,y]:
                    v=min(pix[x,y])
                    for t in counts:
                        if v<t:counts[t]+=1
        assert counts[190]==0
        pages.append(dict(pdf_page=p,region_count=len(ss),component_count=sum(len(s['components']) for s in ss),region_area_trillionths=region_area,gap_area_trillionths=gap_area,gaps=gaps,gap_assessment='Geometric unrepresented margins, whitespace and inter-region spacing; none counts as represented source content. Original visual inspection, character-center and raster audit support this classification; pixel tests are bounded by threshold and raster resolution.',nonwhitespace_character_centers=len(chars),unassigned_character_centers=missing,outside_raster_pixels_by_exclusive_threshold={str(k):v for k,v in counts.items()},render=file_pin(ROOT,(RUN/f'inspection/page-{p}.png').as_posix()),overlay=file_pin(ROOT,(RUN/f'inspection/overlay-{p}.png').as_posix())))
report('source-area-audit.json',summary='Exact disjoint authored area plus explicit geometric gaps exhaust each assigned original page; all text centers and all raster pixels darker than 190 are inside authored regions.',source=pdf,author_basis=[file_pin(ROOT,(RUN/p).as_posix()) for p in ('authored-corrected/inventory.json','authored-corrected/identity-registry.json','authored-corrected/regions.json')],pages=pages,limitations=['Character font metrics can overhang ink; center containment is a support check rather than verified transcription.','Raster mask rounds boxes outward to pixels; exact normalized area is checked independently.','No semantic coverage or human acceptance is inferred.'])
print('All four original pages: no missing character centers or dark raster pixels; exact area accounting passed.')
