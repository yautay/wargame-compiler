from review_driver import *
from PIL import Image,ImageDraw,ImageFont
from math import floor,ceil
ledger=load(D/'region-ledger-final.json')['regions']
out=R/'visual';out.mkdir()
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
index=[];sheets=[];components=[]
for page in (5,6,7,8):
    original=Image.open(R/f'originals/original-{page:02}.png').convert('RGB')
    overlay=original.copy();od=ImageDraw.Draw(overlay)
    entries=[(i,row) for i,row in enumerate(ledger,1) if row['pdf_page']==page]
    batch=[];height=40;sheet_number=0
    def save_sheet():
        global batch,height,sheet_number
        if not batch:return
        sheet_number+=1
        sheet=Image.new('RGB',(1240,height),'white');draw=ImageDraw.Draw(sheet)
        draw.text((10,4),f'Page {page}: original context + red boundary (left) / exact submitted crop (right)',font=font,fill='black')
        y=35
        for i,row,crop,evidence,rect,h in batch:
            draw.text((10,y),f"{i:03} {row['region']['key']} :: {row['label']}",font=small,fill='black')
            y+=23;sheet.paste(crop,(10,y));sheet.paste(evidence,(640,y));y+=h+8
            draw.line((0,y,1240,y),fill='#999999');y+=10
            index.append({'index':i,'region_id':row['region']['id'],'key':row['region']['key'],'pdf_page':page,'sheet':(out/f'p{page}-sheet-{sheet_number:02}.png').relative_to(ROOT).as_posix(),'original_context_pixel_rectangle':rect,'submitted_image':row['evidence']['image'],'source':'Fresh original render with exact integer-normalized boundary; submitted crop is byte-identical to independently regenerated evidence after locator audit.'})
        path=out/f'p{page}-sheet-{sheet_number:02}.png';sheet.save(path)
        sheets.append(pin(path));batch=[];height=40
    for i,row in entries:
        r=row['region'];b=r['box'];exact=(b[0]*1224/1e6,b[1]*1584/1e6,b[2]*1224/1e6,b[3]*1584/1e6)
        od.rectangle(exact,outline='red',width=1);od.text((exact[0]+1,exact[1]+1),str(i),font=small,fill='blue')
        rect=[max(0,floor(exact[0])-5),max(0,floor(exact[1])-5),min(1224,ceil(exact[2])+5),min(1584,ceil(exact[3])+5)]
        crop=original.crop(rect);cd=ImageDraw.Draw(crop)
        cd.rectangle((exact[0]-rect[0],exact[1]-rect[1],exact[2]-rect[0],exact[3]-rect[1]),outline='red',width=1)
        evidence=Image.open(ROOT/row['evidence']['image']['path']).convert('RGB')
        scale=min(1,610/max(crop.width,evidence.width))
        if scale<1:
            crop=crop.resize((round(crop.width*scale),round(crop.height*scale)))
            evidence=evidence.resize((round(evidence.width*scale),round(evidence.height*scale)))
        h=max(crop.height,evidence.height)
        if height+41+h>1900 and batch:save_sheet()
        batch.append((i,row,crop,evidence,rect,h));height+=41+h
        if r['kind']=='diagram':
            path=out/f'component-{i:03}.png'
            if evidence.width<200:evidence=evidence.resize((evidence.width*4,evidence.height*4),Image.Resampling.NEAREST)
            else:evidence=evidence.resize((evidence.width*3,evidence.height*3),Image.Resampling.NEAREST)
            evidence.save(path);components.append({'index':i,'key':r['key'],'image':pin(path),'components':row['components']})
    save_sheet();overlay.save(out/f'overlay-p{page}.png')
write('visual-index.json',{'regions':index,'sheets':sheets,'components':components,'generated_utc':utc(),'viewing_status':'Prepared only; actual reviewer viewing is recorded separately.'})
print('VISUAL SHEETS',len(sheets))
for p in sheets:print(p['path'])
