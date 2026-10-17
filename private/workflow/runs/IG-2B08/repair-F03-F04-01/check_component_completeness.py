"""F03/F04 full original-component pixel regressions, independent of selections."""
from PIL import Image, ImageDraw
from build_inventory import ROOT, SPECS, load, write, pin, metadata

COMPONENTS = {
    'F03': {
        'key': 'ig2b08:p29:collapse-diagram-component-v-counter',
        'windows': {'Tribune_full_artwork_label_zero_frame': (183,333,214,366),
                    'underlying_V_counter': (174,339,206,369)},
        'old': [174,339,205,370],
        'negative': {'top_frame': [173,336,215,370],
                     'right_zero_and_frame': [173,333,209,370],
                     'bottom_frame': [173,333,215,363],
                     'left_frame': [187,333,215,370]},
    },
    'F04': {
        'key': 'ig2b08:p29:advance-diagram-component-c-hits',
        'windows': {'full_visible_three_and_frame': (457,392,489,425)},
        'old': [465,385,495,418],
        'negative': {'left_frame': [461,390,490,426],
                     'bottom_frame': [455,390,490,421],
                     'top_frame': [455,396,490,426],
                     'right_frame': [455,390,485,426]},
    },
}


def references():
    im = Image.open(ROOT/'originals/page-29.png').convert('RGB')
    assert im.size == (1224,1584)
    result = {}
    for finding, c in COMPONENTS.items():
        result[finding] = {}
        for name, box in c['windows'].items():
            x0,y0,x1,y1 = [int(v*2) for v in box]
            # Full colored artwork, lettering, digit, outlines and antialiasing;
            # only plain white background is excluded. No witness-only mask.
            pixels = [(x,y,im.getpixel((x,y)))
                      for y in range(y0,y1) for x in range(x0,x1)
                      if min(im.getpixel((x,y))) < 245]
            assert len(pixels) > 1000
            result[finding][name] = pixels
    return im,result


def require(box, masks):
    x0,y0,x1,y1 = box
    for name,pixels in masks.items():
        missing = [(x,y) for x,y,_ in pixels if not
                   (x0 <= x/2 and (x+1)/2 <= x1 and
                    y0 <= y/2 and (y+1)/2 <= y1)]
        assert not missing, (name,'incomplete source component',len(missing))


def check_evidence(region, ev, masks):
    assert region['denominator_role'] == 'context'
    box = [region['box'][0]*612/1e6, region['box'][1]*792/1e6,
           region['box'][2]*612/1e6, region['box'][3]*792/1e6]
    require(box,masks)
    for f in ('image','text','crop_pdf'):
        assert pin(ev[f]['path']) == ev[f]
    crop = Image.open(ev['image']['path']).convert('RGB')
    matches = {}
    for name,pixels in masks.items():
        matched = 0
        for x,y,rgb in pixels:
            px,py = round(x-box[0]*2),round(y-box[1]*2)
            # Independent renders can differ at a fractional-pixel origin.
            # Every original pixel needs matching RGB support within one pixel.
            if any(0 <= px+dx < crop.width and 0 <= py+dy < crop.height
                   and max(abs(a-b) for a,b in zip(rgb,crop.getpixel((px+dx,py+dy)))) <= 35
                   for dx in (-1,0,1) for dy in (-1,0,1)):
                matched += 1
        assert matched == len(pixels), (name,'missing intended image pixels',matched,len(pixels))
        matches[name] = matched
    return {'region_id':region['id'],'revision':region['revision'],
            'image':ev['image'],'all_source_pixels_supported':True,
            'matched_source_pixels':matches}


def check_all():
    im,reference = references()
    reports = {}
    for finding,c in COMPONENTS.items():
        masks = reference[finding]
        selected = next(s for s in SPECS if s['key']==c['key'])
        require(selected['points'],masks)
        negative = {}
        for label,box in {'original_clip':c['old'],**c['negative']}.items():
            try:
                require(box,masks)
            except AssertionError:
                negative[label] = 'correctly_rejected'
            else:
                raise AssertionError((finding,label,'truncation passed'))
        runs = []
        for name in ('final-verified','replay-1','replay-2'):
            doc = load(ROOT/name/'inventory.json')
            region = next(r for r in doc['regions'] if r['key']==c['key'])
            ev = next(e for e in doc['evidence'] if e['region_id']==region['id'])
            runs.append({'name':name,**check_evidence(region,ev,masks)})
        reports[finding] = {'key':c['key'],'reference_windows':c['windows'],
            'old_points':c['old'],'new_points':selected['points'],
            'old_crop_rejected':True,'negative_cases':negative,'runs':runs,
            'masks':{n:{'pixel_count':len(p),'bounds_half_open':
                [min(x for x,y,rgb in p),min(y for x,y,rgb in p),
                 max(x for x,y,rgb in p)+1,max(y for x,y,rgb in p)+1]}
                for n,p in masks.items()}}
    report = {**metadata(),'summary':'Complete Tribune artwork/label/0/frame and complete visible 3-marker/frame verified in each intended detail; old clips and all edge truncations rejected.',
        'physical_page':29,'original':pin(ROOT/'originals/page-29.png'),
        'source_sha256':load(ROOT/'final-verified/inventory.json')['source']['sha256'],
        'findings':reports,'semantic_acceptance_granted':False,
        'executable_readiness':False,'exit_code':0}
    write(ROOT/'F03-F04-completeness-report.json',report)
    return report


if __name__ == '__main__':
    check_all()
    print('F03/F04 complete source component regressions passed in all three sets.')
