import json
import pathlib
from PIL import Image, ImageDraw

ROOT=pathlib.Path(__file__).resolve().parent
PRODUCT=pathlib.Path('private/workflow/runs/IG-2B08/repair-F01-manifest02')
rows=json.loads((PRODUCT/'region-ledger.json').read_text())['new_observations']
components=json.loads((PRODUCT/'component-ledger.json').read_text())['components']
out=ROOT/'boundary-aids';out.mkdir(exist_ok=False)
for page in [29,30,31,32]:
    for role in ['inventory','context']:
        im=Image.open(ROOT/f'originals/page-{page}.png').convert('RGB');d=ImageDraw.Draw(im)
        for i,r in enumerate(rows):
            if r['page']!=page or r['role']!=role:continue
            box=[int(v*2) for v in r['points']]
            d.rectangle(box,outline='red',width=1)
            d.text((box[0]+1,box[1]+1),str(i),fill='red',stroke_width=1,stroke_fill='white')
        im.save(out/f'page-{page}-{role}.png')
for start in range(0,len(components),12):
    sheet=Image.new('RGB',(1200,1000),'#eeeeee');d=ImageDraw.Draw(sheet)
    for cell,r in enumerate(components[start:start+12]):
        im=Image.open(r['evidence']['image']['path']).convert('RGB');im.thumbnail((390,205))
        x=(cell%3)*400;y=(cell//3)*250
        d.text((x+5,y+3),f"{start+cell} p{r['page']} {r['key'].split(':')[-1]}",fill='black')
        sheet.paste(im,(x+5,y+35))
    sheet.save(out/f'components-{start//12+1:02d}.png')
# Independent candidate F02 comparison, wider original-only view and exact crop.
im=Image.open(ROOT/'originals/page-29.png').convert('RGB')
wide=im.crop((200,976,294,1064)).resize((564,528))
d=ImageDraw.Draw(wide);d.rectangle(((212-200)*6,(992-976)*6,(266-200)*6,(1054-976)*6),outline='red',width=3)
wide.save(out/'c-hit-original-boundary.png')
r=next(r for r in components if r['key']=='ig2b08:p29:collapse-diagram-component-c-hits')
Image.open(r['evidence']['image']['path']).resize((324,372)).save(out/'c-hit-delivered.png')
print(json.dumps({'component_count':len(components),'sheets':(len(components)+11)//12,'all_ledger_rows':len(rows),'detail_role':'context; zero denominator'}))
