"""Persist separate native command/stdout/stderr logs for every crop render.
The unchanged extract_evidence library captures its internal native subprocess
buffers without exposing them. These direct fresh replays close that logging gap.
"""
from review_driver import *
from PIL import Image
ledger=load(D/'region-ledger-final.json')['regions'];destination=R/'native-render-replay';destination.mkdir()
rows=[]
for i,l in enumerate(ledger,1):
    r=l['region'];e=l['evidence'];assert r['key'].startswith('ig2b02:') and l['pdf_page'] in (5,6,7,8)
    crop=ROOT/e['crop_pdf']['path'];assert pin(crop)==e['crop_pdf']
    prefix=destination/r['id'].split(':')[1]
    command=run(f'19-native-render-{i:03}',[POP/'pdftoppm.EXE','-f','1','-l','1','-singlefile','-cropbox','-r','144','-png',crop,prefix])
    actual=pin(prefix.with_suffix('.png'));assert actual['sha256']==e['image']['sha256'] and actual['bytes']==e['image']['bytes']
    with Image.open(prefix.with_suffix('.png')) as image:dimensions=list(image.size)
    assert dimensions==[e['render_parameters']['width_pixels'],e['render_parameters']['height_pixels']]
    rows.append({'index':i,'region_id':r['id'],'revision':r['revision'],'key':r['key'],'pdf_page':l['pdf_page'],'box':r['box'],'source_crop':e['crop_pdf'],'actual_image':actual,'dimensions':dimensions,'exact_bytes':True,'command':command})
write('native-render-audit.json',{'outcome':'passed','regions':rows,'count':len(rows),'reason':'Separate native per-region command/stdout/stderr capture supplements unchanged library extraction, whose successful internal buffers are not exposed. No unassigned source access or changed validation.','library_replay':'Independent full crop/text/PNG regeneration remains in locator-audit.json.'})
print('ALL 141 NATIVE RENDERS EXACT WITH SEPARATE COMMAND LOGS')
