"""Complete independent replay; four local workers use unchanged installed extraction."""
import datetime
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from author import ROOT,RUN,load,write,meta
from wgc.sources.inventory import file_pin,seal,validate
from wgc.sources.pdf import extract_evidence

def one(args):
    index,region_id,out=args
    doc=load(RUN/'authored-corrected/inventory.json')
    return extract_evidence(doc,region_id,ROOT,f'{out}/region-{index:03d}',dpi=144)

def main():
    name=sys.argv[1]
    assert name in ('corrected/replay-a','corrected/replay-b','final-verified')
    out=RUN/name;assert not out.exists()
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
    inputs=[file_pin(ROOT,(RUN/p).as_posix()) for p in ('authored-corrected/inventory.json','authored-corrected/identity-registry.json','authored-corrected/regions.json')]
    doc=load(RUN/'authored-corrected/inventory.json')
    assert doc['registry']==load(RUN/'authored-corrected/identity-registry.json')
    spec=load(RUN/'authored-corrected/regions.json')['regions']
    validate(doc,ROOT);out.mkdir(parents=True)
    with ProcessPoolExecutor(max_workers=4) as pool:
        generated=[]
        for i,e in enumerate(pool.map(one,[(i,s['region_id'],out.as_posix()) for i,s in enumerate(spec)])):
            generated.append(e)
            if (i+1)%10==0: print(f'{name}: {i+1}/{len(spec)}',flush=True)
    doc['evidence']+=generated;doc=seal(doc);validation=validate(doc,ROOT)
    write(out/'inventory.json',doc);write(out/'identity-registry.json',doc['registry']);write(out/'coverage.json',validation)
    assert inputs==[file_pin(ROOT,p['path']) for p in inputs]
    write(out/'generation.json',dict(meta,summary='Complete independent fresh generation from the same corrected pre-evidence full inventory and persisted registry; no other replay is an input.',input_pins=inputs,output_pins=[file_pin(ROOT,(out/p).as_posix()) for p in ('inventory.json','identity-registry.json','coverage.json')],generated_count=len(generated),local_workers=4,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=round(time.monotonic()-clock,3),dpi=144,exit_code=0))
    print(f'{name}: complete {len(generated)} regions',flush=True)

if __name__=='__main__':main()
