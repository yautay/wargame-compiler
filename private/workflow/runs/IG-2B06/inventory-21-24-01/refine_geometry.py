"""Preserve draft bytes and widen one visually audited italic overhang."""
from author import ROOT,RUN,load,write,report
from wgc.sources.inventory import seal,validate,file_pin

doc=load(RUN/'authored/inventory.json');s=load(RUN/'authored-regions.json')
target=next(x for x in s['regions'] if x['page']==24 and x['key']=='8.34-example-d')
old=list(target['box']);target['box'][0]=625*1000000//1224
target['components'][0]['box']=list(target['box'])
r=next(x for x in doc['regions'] if x['id']==target['region_id'])
r['box']=list(target['box']);r.update(seal(r));doc=seal(doc)
validate(doc,ROOT)
write(RUN/'authored-corrected/inventory.json',doc)
write(RUN/'authored-corrected/identity-registry.json',doc['registry'])
write(RUN/'authored-corrected/regions.json',s)
report('geometry-refinement.json',summary='Widened page-24 example-D left edge from pixel 629 to 625 to include five italic overhang pixels identified in the fresh full-page raster. All initial authored and generation draft bytes retained; corrected replay outputs will be new directories.',target_id=r['id'],old_box=old,new_box=r['box'],input_pins=[file_pin(ROOT,(RUN/p).as_posix()) for p in ('authored/inventory.json','authored/identity-registry.json','authored-regions.json')],output_pins=[file_pin(ROOT,(RUN/p).as_posix()) for p in ('authored-corrected/inventory.json','authored-corrected/identity-registry.json','authored-corrected/regions.json')])
print('Corrected pre-evidence author basis persisted without overwriting draft.')
