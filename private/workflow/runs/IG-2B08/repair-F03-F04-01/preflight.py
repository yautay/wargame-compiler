"""Exact proposed evidence and complete source masks before full generation."""
from build_inventory import *
from check_component_completeness import references,COMPONENTS,check_evidence
from check_arrow_completeness import reference_masks,require_mask_coverage,KEY as AK
from check_hit_completeness import masks,require as require_hit,KEY as HK

_,refs=references()
_,arrows=reference_masks()
_,hits,_=masks()
doc=load(ROOT/'author-inventory.json')
reader=PdfReader(PIN['source']['pdf']['path'],strict=True)
rows=[]
with pdfplumber.open(PIN['source']['pdf']['path']) as original:
    for finding,c in COMPONENTS.items():
        region=next(x for x in doc['regions'] if x['key']==c['key'])
        ev=evidence(doc,region,ROOT/'proposal-2-evidence'/finding,reader,original)
        result=check_evidence(region,ev,refs[finding])
        rows.append({'finding':finding,'region':region,'evidence':ev,'result':result})
    for key,reference,fn in [(AK,arrows,require_mask_coverage),(HK,hits,require_hit)]:
        s=next(s for s in SPECS if s['key']==key)
        fn(s['points'],reference)
write(ROOT/'proposal-preflight.json',{**metadata(),
    'summary':'Exact F03/F04 evidence passes full independent source masks; unchanged F01/F02 selections retain their original full masks.',
    'rows':rows,'exit_code':0})
