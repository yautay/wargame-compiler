import json,subprocess,hashlib,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import pdfplumber
R=Path(__file__).parent; B=Path("private/workflow/runs/IG-2B08/repair-F02-validation02")
S=Path("private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf")
assert hashlib.sha256(S.read_bytes()).hexdigest()=="e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e"
O=R/"originals"; O.mkdir()
obs=json.loads((B/"region-ledger.json").read_text())["new_observations"]
font=ImageFont.truetype("C:/Windows/Fonts/consola.ttf",15)
for page in [29,30,31,32,33]:
 cmd=["pdftoppm","-f",str(page),"-l",str(page),"-r","144","-cropbox","-singlefile","-png"]
 if page==33: cmd += ["-x","90","-y","100","-W","522","-H","60"]
 cmd += [str(S),str(O/f"page-{page}")]
 c=subprocess.run(cmd,capture_output=True); (O/f"page-{page}-render.log").write_bytes(c.stdout+c.stderr); assert c.returncode==0
with pdfplumber.open(S) as pdf:
 for page in [29,30,31,32,33]:
  p=pdf.pages[page-1]
  if page==33:p=p.crop((45,50,306,80),strict=True)
  (O/f"page-{page}.txt").write_text(p.extract_text(x_tolerance=3,y_tolerance=3) or "",encoding="utf-8")
for page in [29,30,31,32]:
 rows=[(i,o) for i,o in enumerate(obs) if o["page"]==page]
 original=Image.open(O/f"page-{page}.png").convert("RGB")
 for role in ["inventory","context"]:
  im=original.copy(); draw=ImageDraw.Draw(im)
  for i,o in rows:
   if o["role"]!=role:continue
   box=[v*2 for v in o["points"]]; draw.rectangle(box,outline="red" if role=="inventory" else "blue",width=2); draw.text((box[0]+2,box[1]+1),str(i),font=font,fill="magenta",stroke_width=1,stroke_fill="white")
  im.save(O/f"page-{page}-{role}-overlay.png")
 details=[(i,o) for i,o in rows if o["role"]=="context"]
 for batch in range(math.ceil(len(details)/12)):
  group=details[batch*12:(batch+1)*12]; sheet=Image.new("RGB",(1200,math.ceil(len(group)/3)*260),"white"); d=ImageDraw.Draw(sheet)
  for j,(i,o) in enumerate(group):
   x=(j%3)*400;y=(j//3)*260; box=[v*2 for v in o["points"]]
   # Show independently rendered source beyond every intended boundary beside exact delivered crop.
   pad=8; src=original.crop((max(0,box[0]-pad),max(0,box[1]-pad),min(original.width,box[2]+pad),min(original.height,box[3]+pad)))
   sd=ImageDraw.Draw(src); sd.rectangle((pad,pad,pad+box[2]-box[0],pad+box[3]-box[1]),outline="red",width=1)
   out=Image.open(o["evidence"]["image"]["path"]).convert("RGB")
   src.thumbnail((190,215));out.thumbnail((190,215));sheet.paste(src,(x,y+40));sheet.paste(out,(x+200,y+40))
   label=str(i)+" "+o["key"].split(":")[-1]
   d.text((x+2,y+2),label[:42],font=font,fill="black");d.text((x+2,y+20),"original+boundary | delivered",font=font,fill="black")
  sheet.save(O/f"page-{page}-details-{batch+1}.png")
print(json.dumps({"original_pages":[29,30,31,32],"context33_pixels":[522,60],"boundary_observations":len(obs),"detail_count":sum(o["role"]=="context" and o["page"] in [29,30,31,32] for o in obs)}))
