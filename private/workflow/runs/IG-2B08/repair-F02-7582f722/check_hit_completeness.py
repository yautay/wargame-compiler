"""F02 source-bound digit and marker extent regression, using original pixels."""
from PIL import Image
from build_inventory import ROOT, SPECS, load, write, pin, metadata

KEY = 'ig2b08:p29:collapse-diagram-component-c-hits'
WINDOWS = {
    'complete_visible_digit': (122, 500, 138, 522),
    'reported_stem_witness': (130, 513, 138, 523),
    'left_marker_frame': (116, 497, 120, 525),
    'bottom_marker_frame': (117, 522, 147, 527),
}

def ink(rgb):
    r,g,b = rgb
    return r > 180 and g < 240 and b < 100

def reference_masks():
    im = Image.open(ROOT/'originals/page-29.png').convert('RGB')
    masks = {}
    for name,box in WINDOWS.items():
        x0,y0,x1,y1 = [int(v*2) for v in box]
        pred = ink if 'digit' in name or 'witness' in name else lambda c: max(c)-min(c)<12 and 80<min(c)<225
        masks[name] = [(x,y) for y in range(y0,y1) for x in range(x0,x1) if pred(im.getpixel((x,y)))]
        assert len(masks[name]) > 30, name
    return im,masks

def require(box,masks):
    x0,y0,x1,y1=box
    for name,pixels in masks.items():
        assert all(x0<=x/2 and (x+1)/2<=x1 and y0<=y/2 and (y+1)/2<=y1 for x,y in pixels),name

def check_document(doc,masks):
    region=next(r for r in doc['regions'] if r['key']==KEY)
    assert region['denominator_role']=='context'
    b=region['box'];box=[b[0]*612/1e6,b[1]*792/1e6,b[2]*612/1e6,b[3]*792/1e6]
    require(box,masks)
    ev=next(e for e in doc['evidence'] if e['region_id']==region['id'])
    for field in ('image','crop_pdf','text'): assert pin(ev[field]['path'])==ev[field]
    crop=Image.open(ev['image']['path']).convert('RGB')
    original=Image.open(ROOT/'originals/page-29.png').convert('RGB')
    for name,pixels in masks.items():
        for x,y in pixels:
            px,py=round(x-box[0]*2),round(y-box[1]*2)
            c=original.getpixel((x,y))
            assert any(0<=px+dx<crop.width and 0<=py+dy<crop.height and
                       max(abs(a-b) for a,b in zip(c,crop.getpixel((px+dx,py+dy))))<50
                       for dx in (-1,0,1) for dy in (-1,0,1)),(name,x,y)
    return {'region_id':region['id'],'revision':region['revision'],'image':ev['image'],'all_source_mask_pixels_present':True}

def main():
    im,masks=reference_masks()
    selected=next(s for s in SPECS if s['key']==KEY)
    require(selected['points'],masks)
    negatives={}
    for label,box in {'old_truncated_crop':[106,496,133,527],
                      'bottom_stem_cut':[106,496,148,518],
                      'left_digit_cut':[129,496,148,527],
                      'marker_right_frame_cut':[106,496,141,527]}.items():
        try:require(box,masks)
        except AssertionError:negatives[label]='correctly_rejected'
        else:raise AssertionError(label)
    witness=masks['reported_stem_witness']
    outside=[(x,y) for x,y in witness if x>=266]
    assert len(outside)>=51,'Reported missing stem witness must be covered in full'
    results=[{'name':n,**check_document(load(ROOT/n/'inventory.json'),masks)} for n in ('final-verified','replay-1','replay-2')]
    write(ROOT/'F02-completeness-report.json',{**metadata(),'summary':'Full visible digit, witness patch and marker frame fit and appear in intended final/replay detail; original crop rejected.',
        'source_sha256':load(ROOT/'final-verified/inventory.json')['source']['sha256'],
        'physical_page':29,'source_original':pin(ROOT/'originals/page-29.png'),'reference_windows':WINDOWS,
        'reference_masks':{n:{'pixel_count':len(p),'bounds':[min(x for x,y in p),min(y for x,y in p),max(x for x,y in p)+1,max(y for x,y in p)+1]} for n,p in masks.items()},
        'old_points':[106,496,133,527],'new_points':selected['points'],'old_crop_rejected':True,
        'witness_pixels_outside_old_right_edge':len(outside),'negative_cases':negatives,'runs':results,'exit_code':0})
    print({'F02':'passed','mask_pixels':{k:len(v) for k,v in masks.items()},'witness_outside_old':len(outside)})

if __name__=='__main__':main()
