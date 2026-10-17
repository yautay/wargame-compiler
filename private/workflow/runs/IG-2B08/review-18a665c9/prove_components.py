import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).parent;B=Path("private/workflow/runs/IG-2B08/repair-F02-validation02")
load=lambda p:json.loads(Path(p).read_text(encoding="utf-8-sig"));h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();pin=lambda p:{"path":Path(p).as_posix(),"sha256":h(p),"bytes":Path(p).stat().st_size}
meta=load(R/"checkpoint.json");report={k:meta[k] for k in ["task","role","actor","model","reasoning","configuration_evidence","configuration_sha256"]}
obs=load(B/"region-ledger.json")["new_observations"];images={p:Image.open(R/f"originals/page-{p}.png").convert("RGB") for p in [29,30]}

def getmask(page,box,predicate):
 im=images[page];return [(x,y) for y in range(box[1]*2,box[3]*2) for x in range(box[0]*2,box[2]*2) if predicate(*im.getpixel((x,y)))]
def bounds(p):return [min(x for x,y in p),min(y for x,y in p),max(x for x,y in p)+1,max(y for x,y in p)+1] if p else None
cyan=lambda r,g,b:r<100 and g>140 and b>180
black=lambda r,g,b:max(r,g,b)<80
redyellow=lambda r,g,b:r>150 and b<100 and r>b*1.5
yellow=lambda r,g,b:r>150 and g>100 and b<100
gray=lambda r,g,b:max(r,g,b)-min(r,g,b)<10 and 50<r<220
cases=[("F01-left-cyan",229,30,[92,365,111,400],cyan,True),("F01-right-cyan",229,30,[122,344,143,382],cyan,True),("F01-black-arrow",229,30,[109,425,131,463],black,True),("F02-full-visible-4",145,29,[120,499,138,523],redyellow,True),("F02-reported-stem",145,29,[130,513,138,523],redyellow,True),("F03-Tribune-yellow-zero",257,29,[205,352,212,366],yellow,False),("F04-C3-lower-frame",198,29,[460,420,489,424],gray,False)]
results=[]
for name,idx,page,box,pred,expected in cases:
 o=obs[idx];pixels=getmask(page,box,pred);assert pixels
 row={"name":name,"observation_index":idx,"key":o["key"],"region_id":o["region_id"],"region_revision":o["revision"],"physical_page":page,"source_original":pin(R/f"originals/page-{page}.png"),"points":o["points"],"witness_box_points":box,"mask_pixels":len(pixels),"mask_pixel_bounds_half_open":bounds(pixels),"runs":[]}
 for run in ["final-verified","replay-1","replay-2"]:
  inv=load(B/run/"inventory.json");r=next(r for r in inv["regions"] if r["id"]==o["region_id"]);e=next(e for e in inv["evidence"] if e["region_id"]==o["region_id"]);assert r["revision"]==o["revision"] and r["box"]==o["box"]
  crop=Image.open(e["image"]["path"]).convert("RGB");x0,y0,x1,y1=o["points"];ox=int(x0*2);oy=int(y0*2)
  missing=[(x,y) for x,y in pixels if not(0<=x-ox<crop.width and 0<=y-oy<crop.height)]
  support=(lambda r,g,b:max(r,g,b)<100) if name=="F01-black-arrow" else pred
  matched=sum(any(0<=x-ox+dx<crop.width and 0<=y-oy+dy<crop.height and support(*crop.getpixel((x-ox+dx,y-oy+dy))) for dx in [-1,0,1] for dy in [-1,0,1]) for x,y in pixels)
  print("WITNESS "+json.dumps({"name":name,"run":run,"pixels":len(pixels),"missing":len(missing),"matched":matched}))
  if expected:assert not missing and matched==len(pixels)
  else:assert len(missing)==len(pixels)
  row["runs"].append({"name":run,"intended_evidence":pin(e["image"]["path"]),"source_pixels_outside_intended_image":len(missing),"outside_bounds_half_open":bounds(missing),"source_pixels_with_same_color_support_within_1px":matched,"source_pixels_complete":not missing})
 results.append(row)
# Explicit expanded witness comparisons for the two new findings, with original pixels and proposed boundary.
for idx in [257,198]:
 o=obs[idx];page=o["page"];p=o["points"]; pad=12;crop=images[page].crop((int((p[0]-pad)*2),int((p[1]-pad)*2),int((p[2]+pad)*2),int((p[3]+pad)*2)));draw=ImageDraw.Draw(crop);draw.rectangle((24,24,24+(p[2]-p[0])*2,24+(p[3]-p[1])*2),outline="red",width=1);crop.resize((crop.width*4,crop.height*4)).save(R/f"witness-{idx}.png")
report.update(raster_comparison="Source pixel centers mapped to crop with one-pixel local color support for fractional crop rerender antialiasing; geometric containment is checked separately. Replay and original-page byte/pixel equality are independent checks.",summary="F01 arrow masks and F02 repaired 4 pass independent source-pixel comparison. New F03 yellow-0 and F04 lower marker-frame witnesses are absent from their intended details in all three sets.",source_sha256="e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e",results=results,resolved_findings=["F01","F02"],new_findings=["F03","F04"],semantic_acceptance_granted=False,executable_readiness=False)
(R/"component-proof.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"resolved":["F01","F02"],"new_findings":[{"id":"F03","missing_yellow_pixels":results[-2]["mask_pixels"]},{"id":"F04","missing_frame_pixels":results[-1]["mask_pixels"]}]}))
