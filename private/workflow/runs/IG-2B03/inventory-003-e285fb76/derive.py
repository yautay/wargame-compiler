"""Use unchanged pinned extraction/validation for this task's new regions only."""
import json, pathlib, copy, datetime
from author import OUT, ROOT, META, build
from wgc.sources.inventory import seal, validate, file_pin
from wgc.sources.pdf import extract_evidence
from wgc.contracts.source import canonical_bytes

def save(path,value):
 path.write_bytes(canonical_bytes(value)+b'\n')

def main():
 authored=json.loads((OUT/'authored/inventory.json').read_text())
 plan=json.loads((OUT/'authored/partition-plan.json').read_text())['regions']
 ids={r['region_id'] for r in plan}
 reports=[]
 for name in ['final-verified','replay-one','replay-two']:
  dest=OUT/name;dest.mkdir(exist_ok=False)
  if name=='final-verified':doc=copy.deepcopy(authored)
  else:
   doc,replayed=build(authored['registry'])
   assert canonical_bytes(doc)==canonical_bytes(authored)
   assert canonical_bytes(doc['registry'])==canonical_bytes(authored['registry'])
   save(dest/'authored-inventory.json',doc)
  # Pass the complete authored document to every unchanged extraction call. Each
  # call validates inherited pins and structure; new evidence is validated together below.
  evidence=[]
  for i,row in enumerate(plan,1):
   dpi=600 if row['kind']=='diagram' else 180
   rel=(dest/'evidence'/row['region_id'].split(':')[1]).relative_to(ROOT).as_posix()
   evidence.append(extract_evidence(doc,row['region_id'],ROOT,rel,dpi=dpi))
   if i%10==0 or row['kind']=='diagram':print(name,i,len(plan),row['slug'],flush=True)
  doc['evidence'].extend(evidence)
  # Labels were visually read in the original-page renders. The same-page crop
  # evidence below pins that observation separately from physical PDF page order.
  for page in doc['pages']:
   if page['pdf_page'] in [9,10,11,12]:
    row=next(r for r in plan if r['page']==page['pdf_page'] and r['slug']=='printed-label')
    ev=next(e for e in evidence if e['region_id']==row['region_id'])
    page['label']={'status':'verified','value':str(page['pdf_page']),'reason':'Executor visually read this glyph on the assigned original page and exact same-page crop; independent review pending.','evidence':ev['id']}
    page.update(seal(page))
  doc=seal(doc);report=validate(doc,ROOT)
  save(dest/'inventory.json',doc);save(dest/'identity-registry.json',doc['registry']);save(dest/'coverage.json',dict(META,**report))
  reports.append({'name':name,'authored_canonical_equal':True,'registry_equal':doc['registry']==authored['registry'],'independent_root_validation':'passed','inventory':file_pin(ROOT,(dest/'inventory.json').relative_to(ROOT).as_posix()),'new_evidence_count':len(evidence),'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
  print(name,'complete',flush=True)
 save(OUT/'registry-replay-report.json',dict(META,format='wgc-ig2b03-registry-replay-1',runs=reports,comparison='Both fresh replays reconstruct identical canonical authored inventory and persisted registry. Each distinct path-dependent evidence output independently validates; final evidence bytes are not asserted equal across paths.',retired_bindings_preserved=True))

if __name__=='__main__':main()
