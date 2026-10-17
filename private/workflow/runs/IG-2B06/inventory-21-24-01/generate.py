"""Independent complete evidence invocation from the persisted pre-evidence inventory."""
import datetime
import sys
import time
from pathlib import Path
from author import ROOT, RUN, load, write, meta
from wgc.sources.inventory import file_pin, seal, validate
from wgc.sources.pdf import extract_evidence

name=sys.argv[1]
assert name in ('replay-a','replay-b','final-verified')
out=RUN/name
assert not out.exists(), 'Fresh output directory required'
started=datetime.datetime.now(datetime.timezone.utc).isoformat(); clock=time.monotonic()
inputs=[file_pin(ROOT,(RUN/p).as_posix()) for p in ('authored/inventory.json','authored/identity-registry.json','authored-regions.json')]
doc=load(RUN/'authored/inventory.json')
assert doc['registry']==load(RUN/'authored/identity-registry.json')
spec=load(RUN/'authored-regions.json')['regions']
validate(doc,ROOT)
out.mkdir()
generated=[]
for i,s in enumerate(spec):
    # The same immutable pre-evidence input is independently reopened by the
    # installed extraction implementation. No other replay is an input.
    generated.append(extract_evidence(doc,s['region_id'],ROOT,(out/f'region-{i:03d}').as_posix(),dpi=144))
    if (i+1)%10==0:print(f'{name}: {i+1}/{len(spec)} regions',flush=True)
doc['evidence']+=generated;doc=seal(doc)
validation=validate(doc,ROOT)
write(out/'inventory.json',doc);write(out/'identity-registry.json',doc['registry']);write(out/'coverage.json',validation)
assert inputs==[file_pin(ROOT,p['path']) for p in inputs]
write(out/'generation.json',dict(meta,summary='Complete independent fresh evidence generation using installed wgc.sources, including authorized context crops.',input_pins=inputs,output_pins=[file_pin(ROOT,(out/p).as_posix()) for p in ('inventory.json','identity-registry.json','coverage.json')],generated_count=len(generated),started_utc=started,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=round(time.monotonic()-clock,3),dpi=144,exit_code=0))
print(f'{name}: complete {len(generated)} regions',flush=True)
