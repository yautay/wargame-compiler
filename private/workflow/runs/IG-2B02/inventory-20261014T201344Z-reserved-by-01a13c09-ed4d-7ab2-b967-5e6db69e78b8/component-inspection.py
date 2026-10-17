from ops import *
from PIL import Image,ImageDraw,ImageFont
spec=load(AR+'/author-specifications-final.json');items=[s for s in spec['specifications'] if s['kind']=='diagram']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for page in (5,6,7):
 selected=[s for s in items if s['page']==page];sheet=Image.new('RGB',(1000,((len(selected)+3)//4)*330),'white');d=ImageDraw.Draw(sheet)
 with Image.open(A/f'inspection/original-{page:02}.png') as original:
  for i,s in enumerate(selected):
   crop=original.crop(tuple(s['observed_pixel_box']));crop.thumbnail((230,240));crop=crop.resize((crop.width*2,crop.height*2)) if crop.width<115 else crop
   x=(i%4)*250;y=(i//4)*330;sheet.paste(crop,(x,y+35));d.text((x+3,y+3),s['key'].split(':')[2],fill='black',font=font)
  if page==7:
   sheet=original.crop(tuple(selected[0]['observed_pixel_box'])).resize((1071,459))
 sheet.save(A/f'inspection/components-{page:02}.png')
print('Component inspection sheets ready; QA derivatives only, not evidence substitutions.')
