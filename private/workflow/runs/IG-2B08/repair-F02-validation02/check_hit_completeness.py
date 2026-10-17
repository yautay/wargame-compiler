"""Source-bound F02 digit/frame completeness, with full-mask negative cases."""
from PIL import Image, ImageDraw
from build_inventory import ROOT, SPECS, load, write, pin, metadata

KEY = 'ig2b08:p29:collapse-diagram-component-c-hits'
WINDOWS = {'visible_digit': (120, 499, 138, 523),
           'visible_marker_frame': (116, 496, 147, 527),
           'reported_stem_patch': (130, 513, 138, 523)}


def ink(rgb):
    r, g, b = rgb
    return r > 180 and b < 120


def frame(rgb):
    return max(rgb) - min(rgb) < 15 and 70 < sum(rgb)/3 < 200


def masks():
    im = Image.open(ROOT/'originals/page-29.png').convert('RGB')
    assert im.size == (1224, 1584)
    result = {}
    for name, box in WINDOWS.items():
        x0, y0, x1, y1 = [int(v*2) for v in box]
        predicate = frame if name == 'visible_marker_frame' else ink
        result[name] = [(x, y) for y in range(y0, y1) for x in range(x0, x1)
                        if predicate(im.getpixel((x, y)))]
        assert len(result[name]) > 50
    # Superset includes the exact 51-pixel reported core, plus antialias edges.
    outside = [(x,y) for x,y in result['reported_stem_patch'] if x >= 266]
    core = [(x,y) for x,y in outside if im.getpixel((x,y))[0] > 195
            and im.getpixel((x,y))[2] < 100]
    assert len(core) == 51
    assert len(outside) >= 51
    xs, ys = zip(*outside)
    assert [min(xs),min(ys),max(xs),max(ys)] == [266,1026,271,1039]
    return im, result, core


def require(box, reference):
    x0,y0,x1,y1 = box
    for name, pixels in reference.items():
        missing = [(x,y) for x,y in pixels if not
                   (x0 <= x/2 and (x+1)/2 <= x1 and y0 <= y/2 and (y+1)/2 <= y1)]
        assert not missing, (name, 'truncated source mask',len(missing))


def check_all():
    im, reference, core = masks()
    selected = next(s for s in SPECS if s['key'] == KEY)
    require(selected['points'], reference)
    negative = {}
    for label, box in {'original_crop': [106,496,133,527],
                       'digit_base_clipped': [106,496,148,518],
                       'frame_left_clipped': [123,496,148,527],
                       'frame_bottom_clipped': [106,496,148,524]}.items():
        try:
            require(box, reference)
        except AssertionError:
            negative[label] = 'correctly_rejected'
        else:
            raise AssertionError((label,'incomplete marker accepted'))
    runs = []
    for name in ('final-verified','replay-1','replay-2'):
        doc = load(ROOT/name/'inventory.json')
        region = next(r for r in doc['regions'] if r['key'] == KEY)
        assert region['denominator_role'] == 'context'
        box = [region['box'][0]*612/1e6,region['box'][1]*792/1e6,
               region['box'][2]*612/1e6,region['box'][3]*792/1e6]
        require(box, reference)
        ev = next(e for e in doc['evidence'] if e['region_id'] == region['id'])
        for field in ('image','text','crop_pdf'):
            assert pin(ev[field]['path']) == ev[field]
        crop = Image.open(ev['image']['path']).convert('RGB')
        matches = {}
        for mask_name, pixels in reference.items():
            predicate = frame if mask_name == 'visible_marker_frame' else ink
            count = 0
            for x,y in pixels:
                px,py = round(x-box[0]*2),round(y-box[1]*2)
                if any(0 <= px+dx < crop.width and 0 <= py+dy < crop.height
                       and predicate(crop.getpixel((px+dx,py+dy)))
                       for dx in (-1,0,1) for dy in (-1,0,1)):
                    count += 1
            assert count == len(pixels), (name,mask_name,count,len(pixels))
            matches[mask_name] = count
        runs.append({'name':name,'region_id':region['id'],'revision':region['revision'],
                     'intended_detail':ev['image'],'matched_source_pixels':matches,
                     'all_masks_in_intended_detail':True})
    mask_image = Image.new('RGB', im.size, 'white')
    draw = ImageDraw.Draw(mask_image)
    for pixels in reference.values():
        for xy in pixels: draw.point(xy, fill='red')
    mask_image.crop((200,980,310,1064)).resize((660,504)).save(ROOT/'F02-source-mask.png')
    report = {**metadata(),'summary':'Full visible digit and marker-frame source masks retained in the intended detail in all three complete sets; truncated crops rejected.',
              'source_sha256':load(ROOT/'final-verified/inventory.json')['source']['sha256'],
              'physical_page':29,'source_original':pin(ROOT/'originals/page-29.png'),
              'independent_reference_windows':WINDOWS,'reference_masks':{
                  n:{'pixel_count':len(p),'bounds_half_open':[min(x for x,y in p),min(y for x,y in p),max(x for x,y in p)+1,max(y for x,y in p)+1]}
                  for n,p in reference.items()},
              'reported_missing_stem_core_pixels':len(core),'old_points':[106,496,133,527],
              'new_points':selected['points'],'old_crop_rejected':True,'negative_cases':negative,
              'runs':runs,'inspection_image':pin(ROOT/'F02-original-detail.png'),
              'source_mask_image':pin(ROOT/'F02-source-mask.png'),
              'semantic_acceptance_granted':False,'executable_readiness':False,'exit_code':0}
    write(ROOT/'F02-completeness-report.json',report)
    return report


if __name__ == '__main__':
    check_all()
    print('F02 source-mask completeness passed in three complete sets.')
