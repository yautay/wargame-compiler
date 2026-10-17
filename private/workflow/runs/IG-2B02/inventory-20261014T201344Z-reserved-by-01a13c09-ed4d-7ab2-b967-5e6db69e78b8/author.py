from ops import *
import copy
from math import floor,ceil
from wgc.sources.inventory import make_region,seal,validate,assign
from wgc.contracts.source import canonical_bytes
from PIL import Image,ImageDraw,ImageFont
def build(registry):
 s=load(P+'/scope.json');base=load(s['baseline']['path']);assert pin(s['baseline']['path'])==s['baseline']
 spec=load(AR+'/author-specifications-final.json');reg=copy.deepcopy(registry);regions={};by_page={}
 for item in spec['specifications']:
  p=next(p for p in base['pages'] if p['pdf_page']==item['page']);x0,y0,x1,y1=item['observed_pixel_box'];box=[floor(x0*1000000/1224),floor(y0*1000000/1584),ceil(x1*1000000/1224),ceil(y1*1000000/1584)]
  r=make_region(reg,item['key'],p,box,kind=item['kind'],reason='Independently inventoried physical source; source-IG reconciliation and representation remain pending.')
  r['uncertainty']=item['uncertainty']
  r['coverage']['transcription']={'status':'partial','gap':True,'reason':'Raw literal machine extraction and visual source locator retained; complete independently verified transcription and source-IG binding remain pending.','boundary':None}
  r=seal(r);regions[item['key']]=r;by_page.setdefault(item['page'],[]).append(r)
 retired={r['id']:next(p['pdf_page'] for p in base['pages'] if p['id']==r['page_id']) for r in base['regions'] if r['key'] in [f'physical-page:{n}:unprocessed-placeholder' for n in (5,6,7,8)]}
 assert len(retired)==4
 additions={n:[regions[k] for k in spec['page_order_keys'][str(n)]] for n in (5,6,7,8)}
 final=copy.deepcopy(base);final['registry']=reg;final['regions']=[];final['reading_order']=[]
 for r in base['regions']:
  final['regions'].extend(additions[retired[r['id']]] if r['id'] in retired else [r])
 for identity in base['reading_order']:
  final['reading_order'].extend([r['id'] for r in additions[retired[identity]]] if identity in retired else [identity])
 allkeys={r['key']:r['id'] for r in final['regions']}
 for kind,a,b,reason in spec['links']:final['links'].append({'kind':kind,'from':allkeys[a],'to':allkeys[b],'reason':reason})
 final=seal(final);validate(final)
 return final,reg,regions,retired
if __name__=='__main__':
 dest=A/(sys.argv[1] if len(sys.argv)>1 else 'authored');registry=load(sys.argv[2]) if len(sys.argv)>2 else load(P+'/scope.json')['registry'];registry=load(registry['path']) if 'path' in registry else registry
 doc,reg,regions,retired=build(registry);dest.mkdir(exist_ok=False)
 for name,obj in [('inventory.json',doc),('identity-registry.json',reg)]:
  with (dest/name).open('xb') as f:f.write(canonical_bytes(obj)+b'\n')
 if dest.name=='authored':
  write('retired-placeholder-memberships.json',{'retired_ids':retired,'registry_entries_retained':True,'old_context_preserved':True,'no_identity_remap':True})
  font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
  index=[]
  for n in (5,6,7,8):
   with Image.open(A/f'inspection/original-{n:02}.png') as im:
    assert im.size==(1224,1584);overlay=im.convert('RGB');draw=ImageDraw.Draw(overlay)
    entries=[r for r in doc['regions'] if r['key'].startswith('ig2b02:') and next(p['pdf_page'] for p in doc['pages'] if p['id']==r['page_id'])==n]
    for i,r in enumerate(entries,1):
     x0,y0,x1,y1=r['box'];rect=(x0*1224/1000000,y0*1584/1000000,x1*1224/1000000,y1*1584/1000000);draw.rectangle(rect,outline='red',width=1);draw.text((rect[0]+1,rect[1]+1),str(i),font=font,fill='blue');index.append({'page':n,'overlay_number':i,'region_id':r['id'],'key':r['key'],'box':r['box']})
    overlay.save(A/f'inspection/overlay-{n:02}.png')
  write('overlay-index.json',index)
  checkpoint('authored',['Explicit original-page observation','Explicit manual selections (count verified from artifact)','Accepted full baseline/registry extended and canonical authored inventory validated internally'],'Inspect every overlay/component; derive evidence for exact new IDs only')
 print('AUTHORED',len(regions),'new regions; full',len(doc['regions']),'records')
