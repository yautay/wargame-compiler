import json,hashlib,copy
from pathlib import Path
R=Path(__file__).parent;B=Path("private/workflow/runs/IG-2B08/repair-F02-validation02");load=lambda p:json.loads(Path(p).read_text(encoding="utf-8-sig"))
meta=load(R/"checkpoint.json");report={k:meta[k] for k in ["task","role","actor","model","reasoning","configuration_evidence","configuration_sha256"]}
obs=load(B/"region-ledger.json")["new_observations"];expected={o["region_id"] for o in obs};sp=load(B/"source-pins.json");index={p["path"]:p for p in sp["artifacts"]};paths=set();runs=[]
for run in ["final-verified","replay-1","replay-2"]:
 inv=load(B/run/"inventory.json");ev=[e for e in inv["evidence"] if e["region_id"] in expected];assert {e["region_id"] for e in ev}==expected
 for e in ev:
  for typ in ["crop_pdf","text","image"]:
   p=e[typ];assert p["path"] in index and index[p["path"]]==p;paths.add(p["path"])
 assert next(s for s in sp["region_evidence_sets"] if s["name"]==run)["region_ids"]==[o["region_id"] for o in obs]
 runs.append({"name":run,"regions":len(ev),"evidence_artifacts":len(ev)*3})
originals=load(B/"original-page-inspection.json")["original_artifacts"]
for p in originals:assert p["path"] in index and index[p["path"]]==p
negative={}
def rejects(name,fn):
 try:fn()
 except AssertionError:negative[name]="correctly_rejected"
 else:raise AssertionError(name+" erroneously accepted")
def complete(ids):assert ids==expected
def index_complete(keys):assert paths<=keys
def valid_hash(p):assert hashlib.sha256(Path(p["path"]).read_bytes()).hexdigest()==p["sha256"]
rejects("missing_component",lambda:complete(expected-{obs[257]["region_id"]}))
rejects("incomplete_replay",lambda:complete(expected-{obs[198]["region_id"]}))
rejects("missing_index_path",lambda:index_complete(set(index)-{next(iter(paths))}))
changed=dict(index[next(iter(paths))]);changed["sha256"]="0"*64;rejects("stale_index_hash",lambda:valid_hash(changed))
report.update(summary="Independent exhaustive new evidence/index and negative omission/stale-pin checks passed.",new_region_count=len(expected),new_artifacts=len(paths),original_artifacts=len(originals),runs=runs,negative_cases=negative)
(R/"index-negative-verification.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"new_regions":len(expected),"indexed_new_artifacts":len(paths),"negative_cases":negative}))
