"""Fresh assigned-page word-center and visible-ink gap probe, not coverage proof."""
import json
from PIL import Image,ImageDraw,ImageChops
from build_inventory import ROOT,SPECS,load,write,pin,metadata

def main():
    rows=[]
    for page in (29,30,31,32):
        primary=[s for s in SPECS if s['page']==page and s['role']=='inventory']
        words=load(ROOT/'originals'/f'page-{page}.words.json')
        missing=[]
        for w in words:
            x=(w['x0']+w['x1'])/2;y=(w['top']+w['bottom'])/2
            if not any(s['points'][0]<=x<s['points'][2] and s['points'][1]<=y<s['points'][3] for s in primary):
                missing.append({'center_points':[x,y],'text':w['text']})
        im=Image.open(ROOT/'originals'/f'page-{page}.png').convert('RGB')
        r,g,b=im.split();ink=ImageChops.darker(ImageChops.darker(r,g),b).point(lambda x:255 if x<180 else 0)
        represented=Image.new('L',im.size);draw=ImageDraw.Draw(represented)
        for s in primary:
            x0,y0,x1,y1=[int(round(v*2)) for v in s['points']]
            draw.rectangle((x0,y0,x1-1,y1-1),fill=255)
        gap=ImageChops.subtract(ink,represented)
        count=gap.histogram()[255]
        gap.save(ROOT/f'geometric-gap-page-{page}.png')
        rows.append({'physical_page':page,'word_count':len(words),'unassigned_word_centers':missing,
                     'unassigned_ink_pixels_at_144dpi':count,'gap_pixel_bounds':gap.getbbox(),
                     'gap_mask':pin(ROOT/f'geometric-gap-page-{page}.png'),
                     'original':pin(ROOT/'originals'/f'page-{page}.png')})
    report={**metadata(),'summary':'Fresh word-center and thresholded ink gap observations; geometric gaps never count as represented source content.',
            'parameters':{'dpi':144,'ink_predicate':'min(R,G,B)<180','primary_pixel_boxes':'half-open rounded PDF point bounds at 2 pixels/point'},
            'pages':rows,'total_unassigned_word_centers':sum(len(x['unassigned_word_centers']) for x in rows),
            'total_unassigned_ink_pixels':sum(x['unassigned_ink_pixels_at_144dpi'] for x in rows),
            'limitation':'A pixel threshold and word centers cannot prove semantic or transcription completeness; every detected gap remains a gap.'}
    write(ROOT/'geometric-content-probe.json',report)
    print(json.dumps({'geometric_probe':'complete','unassigned_word_centers':report['total_unassigned_word_centers'],'unassigned_ink_pixels':report['total_unassigned_ink_pixels']}))

if __name__=='__main__':main()
