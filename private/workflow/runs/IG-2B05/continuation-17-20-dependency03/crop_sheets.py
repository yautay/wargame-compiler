"""Lossless-scale review sheets from every exact fresh assigned crop PNG."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parent
partition=json.loads((BASE/'authored-partition.json').read_text())
output=BASE/'crop-review-sheets'
output.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
created=[]
for page in (17,18,19,20):
    rows=[r for r in partition['regions'] if r['page']==page]
    for start in range(0,len(rows),6):
        group=rows[start:start+6]
        dest=output/f'p{page}-{start+1:02}-{start+len(group):02}.png'
        paths=[BASE/'final-verified/evidence'/r['key'].replace(':','-')/'image.png' for r in group]
        if not all(p.exists() for p in paths):
            paths=[BASE/'replay-1/evidence'/r['key'].replace(':','-')/'image.png' for r in group]
        if not all(p.exists() for p in paths): continue
        meta=dest.with_suffix('.json')
        if not meta.exists():
            meta.write_text(json.dumps({'physical_page':page,'region_keys':[r['key'] for r in group],
                'source_images':[p.relative_to(Path.cwd()).as_posix() for p in paths],
                'scale':'1:1; padding and labels only; no crop image is rescaled'},indent=2)+'\n',encoding='utf-8')
        if dest.exists(): continue
        images=[Image.open(p).convert('RGB') for p in paths]
        width=max(520,max(im.width for im in images))+20
        heights=[max(im.height for im in images[i:i+2])+52 for i in range(0,len(images),2)]
        sheet=Image.new('RGB',(width*2+20,sum(heights)+20),'#d9e0e6')
        draw=ImageDraw.Draw(sheet)
        y=10
        for i in range(0,len(images),2):
            for j in range(2):
                if i+j>=len(images): break
                x=10+j*width
                label=group[i+j]['key'].split(':ig2b05:')[1]
                draw.text((x,y),f'p{page} / {start+i+j+1:02} / {label}',fill='black',font=font)
                sheet.paste(images[i+j],(x,y+32))
            y+=heights[i//2]
        sheet.save(dest)
        created.append(dest.name)
        for im in images: im.close()
print(json.dumps({'created':created}))
