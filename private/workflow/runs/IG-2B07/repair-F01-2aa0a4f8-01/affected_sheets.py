"""Make explicit affected-diagram component inspection sheets from indexed fresh evidence."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from wgc.sources.inventory import file_pin
A=Path(__file__).parent.relative_to(Path.cwd())
rows=json.loads((A/'final-verified/region-accounting.json').read_text())
rows=[r for r in rows if r.get('parent_key')=='ig2b07:p28-diagram-after']
D=A/'affected-inspection-sheets';D.mkdir(exist_ok=False)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
pins=[]
for start in range(0,len(rows),8):
    batch=rows[start:start+8]
    im=Image.new('RGB',(1440,1440),'#eeeeee');draw=ImageDraw.Draw(im)
    for i,row in enumerate(batch):
        x=i%2*720;y=i//2*360
        draw.text((x+8,y+5),row['key'].removeprefix('ig2b07:p28-diagram-'),font=font,fill='black')
        draw.text((x+8,y+30),str(row['box']),font=small,fill='black')
        with Image.open(row['evidence']['image']['path']) as source:
            source=source.convert('RGB')
            factor=min(4,690/source.width,290/source.height)
            source=source.resize((max(1,int(source.width*factor)),max(1,int(source.height*factor))))
            im.paste(source,(x+8,y+60))
    out=D/f'components-{start//8+1:02}.png';im.save(out)
    pins.append({**file_pin(Path.cwd(),out.as_posix()),'region_ids':[r['region']['id'] for r in batch]})
(D/'index.json').write_text(json.dumps(pins,indent=2)+'\n')
print(json.dumps({'affected_components':len(rows),'sheets':[p['path'] for p in pins]}))
