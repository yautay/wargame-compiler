import json, hashlib, pathlib, subprocess, math, textwrap
from PIL import Image, ImageDraw, ImageFont
import pdfplumber

ROOT = pathlib.Path('private/workflow/runs/IG-2B08/review-00a548c6')
DEL = pathlib.Path('private/workflow/runs/IG-2B08/repair-F03-F04-01')
SOURCE = pathlib.Path('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf')
def read(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def pin(p):
    p=pathlib.Path(p); b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(name,d): (ROOT/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
ROOT.mkdir(exist_ok=True)
(ROOT/'originals').mkdir(exist_ok=True)
assert pin(SOURCE)['sha256']=='e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
obs=read(DEL/'region-ledger.json')['new_observations']
for page in [29,30,31,32,33]:
    cmd=['pdftoppm','-f',str(page),'-l',str(page),'-r','144','-png','-singlefile']
    if page==33: cmd+=['-x','90','-y','100','-W','522','-H','60']
    cmd += [str(SOURCE),str(ROOT/'originals'/f'page-{page}')]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
with pdfplumber.open(SOURCE) as pdf:
    for page in [29,30,31,32,33]:
        p=pdf.pages[page-1]
        if page==33: p=p.crop((45,50,306,80),strict=True)
        (ROOT/'originals'/f'page-{page}.txt').write_text(p.extract_text() or '',encoding='utf-8')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
for page in [29,30,31,32]:
    primary=[(i,o) for i,o in enumerate(obs) if o['page']==page and o['role']=='inventory']
    im=Image.open(ROOT/'originals'/f'page-{page}.png').convert('RGB'); draw=ImageDraw.Draw(im)
    for i,o in primary:
        box=[v*2 for v in o['points']]; draw.rectangle(box,outline='red',width=1)
        draw.text((box[0]+2,box[1]+1),str(i),fill='blue',font=small)
    im.save(ROOT/f'boundaries-{page}.png')
    entries=[(i,o) for i,o in enumerate(obs) if o['page']==page]
    for start in range(0,len(entries),18):
        batch=entries[start:start+18]
        sheet=Image.new('RGB',(1500,6*260),'#eeeeee'); dr=ImageDraw.Draw(sheet)
        for n,(i,o) in enumerate(batch):
            x=(n%3)*500; y=(n//3)*260
            crop=Image.open(o['evidence']['image']['path']).convert('RGB')
            crop.thumbnail((480,180))
            sheet.paste(crop,(x+10,y+10))
            label=f"{i}: {o['key'].split(':',2)[2]} {o['points']}"
            lines=textwrap.wrap(label,65)+textwrap.wrap(o['observation'],70)
            dr.multiline_text((x+10,y+192),'\n'.join(lines[:4]),font=small,fill='black')
        sheet.save(ROOT/f'ledger-{page}-{start//18+1}.png')
write('inspection-index.json',{'originals':[pin(ROOT/'originals'/f'page-{p}.png') for p in [29,30,31,32,33]],'observations':len(obs),'sheets':{str(p):math.ceil(sum(o['page']==p for o in obs)/18) for p in [29,30,31,32]}})
print(json.dumps({'status':'pass','observations':len(obs),'sheets':{str(p):math.ceil(sum(o['page']==p for o in obs)/18) for p in [29,30,31,32]}}))
