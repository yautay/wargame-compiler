import json,hashlib,math,copy
from pathlib import Path
from PIL import Image
R=Path(__file__).parent; B=Path("private/workflow/runs/IG-2B08/repair-F02-validation02"); S=Path("private/workflow/orchestrator/20261017T125512Z-933976c1/002-IG-2B08-reviewer-18a665c9")
load=lambda p:json.loads(Path(p).read_text(encoding="utf-8-sig"))
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
canon=lambda o:hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
pin=lambda p:{"path":Path(p).as_posix(),"sha256":h(p),"bytes":Path(p).stat().st_size}
meta=load(R/"checkpoint.json");report={k:meta[k] for k in ["task","role","actor","model","reasoning","configuration_evidence","configuration_sha256"]}
t=load(S/"task.json");d=load(B/"delivery.json"); artifacts={a["path"]:a for a in d["artifacts"]};assert len(artifacts)==len(d["artifacts"])
for a in artifacts.values():assert h(a["path"])==a["sha256"] and Path(a["path"]).stat().st_size==a["bytes"]
# Full dependency records are read internally only for exact preservation comparison; no source text or unassigned records are emitted.
baseline=load("private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/final-verified/inventory.json")
assert h("private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/final-verified/inventory.json")=="24d895f0e42c56e8d8fdb49afe2605da393bf3c9f5b153b2629fc50f5ef1415d"
base_registry=load("private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/final-verified/identity-registry.json")
assert h("private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/final-verified/identity-registry.json")=="5ebe4795143bf1ac02e5775fc5e984b75dc606954b5b8758861c972b6d741701"
final=load(B/"final-verified/inventory.json");obs=load(B/"region-ledger.json")["new_observations"]; comps=load(B/"component-ledger.json")["components"]
retired=set(t["inventory_contract"]["placeholder_target_ids"]); old={r["id"]:r for r in baseline["regions"]}; new={r["id"]:r for r in final["regions"]}; ids={o["region_id"] for o in obs}
assert set(old)-set(new)==retired;assert set(new)-set(old)==ids;assert len(ids)==269
for rid in set(old)-retired:assert old[rid]==new[rid]
assert final["source"]==baseline["source"];assert final["pages"]==baseline["pages"] and len(final["pages"])==44
assert final["links"][:len(baseline["links"]) ]==baseline["links"]
assert final["evidence"][:len(baseline["evidence"]) ]==baseline["evidence"]
assert [x for x in final["reading_order"] if x in set(old)-retired]==[x for x in baseline["reading_order"] if x not in retired]
assert base_registry==baseline["registry"]
assert {canon(e) for e in base_registry["entries"]} <= {canon(e) for e in final["registry"]["entries"]}
assert final["registry"]==load(B/"final-verified/identity-registry.json")
ledger_rows=load(B/"region-ledger.json")["regions"];assert {r["id"] for r in ledger_rows}==set(new)
page_numbers={p["id"]:p["pdf_page"] for p in final["pages"]}
for row in ledger_rows:
 for k in ["id","key","revision","box","kind","denominator_role","coverage"]:assert row[k]==new[row["id"]][k]
 assert row["pdf_page"]==page_numbers[new[row["id"]]["page_id"]]
for o in obs:assert o["region_id"] in new and o["revision"]==new[o["region_id"]]["revision"] and o["box"]==new[o["region_id"]]["box"]
for c in comps:
 o=next(o for o in obs if o["region_id"]==c["region_id"])
 for k in o:assert c[k]==o[k]
# Primary source geometry is positive and disjoint per page. Context components carry no denominator.
for page in [29,30,31,32]:
 rows=[o for o in obs if o["page"]==page and o["role"]=="inventory"]
 for i,a in enumerate(rows):
  x0,y0,x1,y1=a["points"];assert x0<x1 and y0<y1
  for b in rows[i+1:]:
   u0,v0,u1,v1=b["points"];assert min(x1,u1)<=max(x0,u0) or min(y1,v1)<=max(y0,v0)
assert sum(o["role"]=="inventory" for o in obs)==183;assert sum(o["role"]=="context" for o in obs)==86
# All source-index pins must be current and included in the frozen artifact order.
pins=load(B/"source-pins.json");pin_count=0

def walk(x):
 global pin_count
 if isinstance(x,dict):
  if all(k in x for k in ["path","sha256","bytes"]):
   assert h(x["path"])==x["sha256"] and Path(x["path"]).stat().st_size==x["bytes"]
   assert x["path"] in artifacts and artifacts[x["path"]]["sha256"]==x["sha256"]
   pin_count+=1
  else:
   for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(pins)
# Independent replay comparison; no dependency on executor report assertions.
reference=None;runs=[]
for name in ["final-verified","replay-1","replay-2"]:
 inv=load(B/name/"inventory.json");reg=load(B/name/"identity-registry.json")
 for k in ["source","pages","regions","reading_order","links","registry"]:assert inv[k]==final[k]
 assert reg==final["registry"]
 assert {e["region_id"] for e in inv["evidence"] if e["region_id"] in ids}==ids
 ev=[]
 for e in inv["evidence"]:
  if e["region_id"] not in ids:continue
  x=copy.deepcopy(e)
  for typ in ["crop_pdf","text","image"]:
   p=x[typ];assert h(p["path"])==p["sha256"];assert p["path"] in artifacts
   assert p["path"].startswith((B/name).as_posix()+"/")
   p["path"]=p["path"].replace((B/name).as_posix(),"<run>")
  text=Path(e["text"]["path"]).read_text(encoding="utf-8");assert len(text)==e["text_codepoints"] and e["text_offsets"]["end"]==len(text)
  image=Image.open(e["image"]["path"]);assert list(image.size)==[e["render_parameters"]["width_pixels"],e["render_parameters"]["height_pixels"]]
  ev.append(x)
 if reference is None:reference=ev
 else:assert ev==reference
 runs.append({"name":name,"inventory":pin(B/name/"inventory.json"),"region_count":len(ids),"new_artifact_count":len(ev)*3,"normalized_evidence_hash":canon(ev)})
# All fresh reviewer originals have identical source pixels to delivered originals; page 33 is native clipped at the authorized box.
for page in [29,30,31,32,33]:
 a=Image.open(R/f"originals/page-{page}.png").convert("RGB");b=Image.open(B/f"originals/page-{page}.png").convert("RGB");assert a.size==b.size and a.tobytes()==b.tobytes()
 if page==33:assert a.size==(522,60)
report.update(summary="Independent structural, preservation, evidence-index, complete replay and original-raster checks passed. Visual component findings are recorded separately.",frozen_artifacts_verified=len(artifacts),source_index_pin_objects_verified=pin_count,pages=44,preserved_regions=len(old)-4,preserved_evidence_objects=len(baseline["evidence"]),preserved_links=len(baseline["links"]),preserved_registry_entries=len(base_registry["entries"]),retired_placeholders=4,assigned_denominator=183,new_context_denominator=0,new_context_count=86,full_denominator=sum(r["denominator_role"]=="inventory" for r in new.values()),runs=runs,independent_original_pixels_equal=True,semantic_acceptance_granted=False,executable_readiness=False)
(R/"independent-verification.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:report[k] for k in ["frozen_artifacts_verified","source_index_pin_objects_verified","preserved_regions","pages","assigned_denominator","full_denominator"]}))
