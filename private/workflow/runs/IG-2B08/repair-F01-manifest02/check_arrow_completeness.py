"""Source-bound F01 regression: complete visible curves, heads and forward arrow.

The reference masks come from fresh original-page pixels, independently of the
authored crop. The three windows isolate the visibly inspected arrow paths. All
matching source pixels, including antialiasing, must fit the intended detail.
Neither primary field tiles nor adjacent detail crops can satisfy this check.
"""
from PIL import Image, ImageDraw
from build_inventory import ROOT, SPECS, load, write, pin, metadata

KEY = 'ig2b08:p30:advance-component-arrows'
# Independently inspected windows enclosing the complete visible arrow paths.
WINDOWS = {
    'left_cyan_curve_and_head': (92, 365, 111, 400),
    'right_cyan_curve_and_head': (122, 344, 143, 382),
    'black_forward_arrow': (109, 425, 131, 463),
}


def cyan(rgb):
    r, g, b = rgb
    # Cyan ink [42,197,244], including its white-background antialias blend.
    t = (255-r)/213
    return t > .12 and abs(g-(255-58*t)) < 8 and abs(b-(255-11*t)) < 8


def reference_masks():
    im = Image.open(ROOT/'originals/page-30.png').convert('RGB')
    assert im.size == (1224, 1584)
    masks = {}
    for name, box in WINDOWS.items():
        x0, y0, x1, y1 = [int(v*2) for v in box]
        masks[name] = [(x,y) for y in range(y0,y1) for x in range(x0,x1)
                       if (cyan(im.getpixel((x,y))) if 'cyan' in name
                           else max(im.getpixel((x,y))) < 80)]
        assert len(masks[name]) > 50, (name, 'missing source arrow pixels')
        xs, ys = zip(*masks[name])
        # Nontrivial two-dimensional coverage; a single witness is insufficient.
        assert max(xs)-min(xs) > 15 and max(ys)-min(ys) > 35
    assert cyan(im.getpixel((188,734))), 'Independent F01 witness changed'
    return im, masks


def require_mask_coverage(box, masks):
    x0,y0,x1,y1 = box
    for name, pixels in masks.items():
        missing = [(x,y) for x,y in pixels
                   if not (x0 <= x/2 and (x+1)/2 <= x1
                           and y0 <= y/2 and (y+1)/2 <= y1)]
        assert not missing, (name, 'clipped source pixels', len(missing))


def check_document(doc, masks):
    region = next(r for r in doc['regions'] if r['key']==KEY)
    assert region['denominator_role']=='context'
    box = [region['box'][0]*612/1e6, region['box'][1]*792/1e6,
           region['box'][2]*612/1e6, region['box'][3]*792/1e6]
    require_mask_coverage(box,masks)
    ev = next(e for e in doc['evidence'] if e['region_id']==region['id'])
    for field in ('image','text','crop_pdf'):
        assert pin(ev[field]['path']) == ev[field]
    # The actual intended detail PNG must contain every independently observed
    # source arrow's color, extent and pixel mass; no other crop is consulted.
    crop = Image.open(ev['image']['path']).convert('RGB')
    ox,oy = box[:2]
    for name,pixels in masks.items():
        matched=0
        for x,y in pixels:
            px,py=round(x-ox*2),round(y-oy*2)
            predicate=cyan if 'cyan' in name else lambda rgb:max(rgb)<100
            if any(0<=px+dx<crop.width and 0<=py+dy<crop.height
                   and predicate(crop.getpixel((px+dx,py+dy)))
                   for dx in (-1,0,1) for dy in (-1,0,1)):
                matched+=1
        assert matched==len(pixels),(name,'missing intended-crop arrow pixels',matched,len(pixels))
    return {'region_id':region['id'],'revision':region['revision'],
            'box':region['box'],'evidence_image':ev['image'],
            'all_reference_pixels_in_intended_detail':True}


def run():
    im,masks=reference_masks()
    selected=next(s for s in SPECS if s['key']==KEY)
    require_mask_coverage(selected['points'],masks)
    negative_cases={}
    for label,box in {
        'original_truncated_crop':[104,345,141,476],
        'left_tail_clipped_but_witness_retained':[90,344,143,390],
        'right_head_clipped_but_left_witness_retained':[90,355,143,476],
        'black_shaft_clipped_but_cyan_paths_retained':[90,344,143,450],
    }.items():
        try:
            require_mask_coverage(box,masks)
        except AssertionError:
            negative_cases[label]='correctly_rejected'
        else:
            raise AssertionError((label,'truncated crop wrongly passed'))
    rejected=negative_cases['original_truncated_crop']=='correctly_rejected'
    results=[]
    for name in ('final-verified','replay-1','replay-2'):
        doc=load(ROOT/name/'inventory.json')
        results.append({'name':name,**check_document(doc,masks)})
    overlay=im.crop((180,680,288,954)).resize((432,1096))
    overlay.save(ROOT/'arrow-original-detail.png')
    report={**metadata(),'summary':'All visible source-arrow masks fit and appear in the intended detail in final and both complete replays; old truncated crop rejected.',
            'source_original':pin(ROOT/'originals/page-30.png'),
            'source_sha256':load(ROOT/'final-verified/inventory.json')['source']['sha256'],
            'physical_page':30,'reference_windows':WINDOWS,
            'reference_masks':{n:{'pixel_count':len(p),'source_pixel_bounds':[min(x for x,y in p),min(y for x,y in p),max(x for x,y in p)+1,max(y for x,y in p)+1]} for n,p in masks.items()},
            'old_points':[104,345,141,476],'new_points':selected['points'],
            'old_crop_rejected':rejected,'negative_cases':negative_cases,'runs':results,
            'inspection_image':pin(ROOT/'arrow-original-detail.png'),
            'limitation':'Physical visible-component coverage only; no source-meaning or gameplay assertion.', 'exit_code':0}
    write(ROOT/'arrow-completeness-report.json',report)
    print(__import__('json').dumps({'arrow_completeness':'pass','old_crop_rejected':rejected,'reference_pixel_counts':{n:len(p) for n,p in masks.items()},'complete_runs_checked':3}))


if __name__=='__main__':
    run()
