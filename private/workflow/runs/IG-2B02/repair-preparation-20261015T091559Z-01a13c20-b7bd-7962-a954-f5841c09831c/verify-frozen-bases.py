"""Verify named frozen delivery/review bytes only; never repair or transition."""
import argparse,hashlib,json,time
from pathlib import Path
from datetime import datetime,timezone
R=Path('C:/repo/wargame-compiler');P=Path(__file__).resolve().parent
def sha(path):
 with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True);args=parser.parse_args();start=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
 state=json.loads((P/'preparation.json').read_text(encoding='utf-8'));catalogue=json.loads((P/'frozen-base-pins.json').read_text(encoding='utf-8'));target=Path(args.report);target=target if target.is_absolute() else R/target;assert not target.exists()
 for pin in catalogue['frozen_pins']:
  path=Path(pin['path']);path=path if path.is_absolute() else R/path;assert path.is_file() and path.stat().st_size==pin['bytes'] and sha(path)==pin['sha256'],pin['path']
 queue=json.loads((R/'docs/work/queue.json').read_text(encoding='utf-8'));task=next(t for t in queue['tasks'] if t['id']=='IG-2B02');assert state['review_event'] in task['events'],'Original event chain changed'
 assert all(next(t for t in queue['tasks'] if t['id']==d)['status']=='done' for d in ('IG-2A','IG-2B01'))
 result={'outcome':'passed_frozen_bytes_only','task':'IG-2B02','frozen_unique_refs_verified':len(catalogue['frozen_pins']),'original_review_event_preserved':True,'current_status_observation':task['status'],'current_queue_sha256':sha(R/'docs/work/queue.json'),'queue_equals_preparation_snapshot':sha(R/'docs/work/queue.json')==state['queue_snapshot']['sha256'],'started_utc':start,'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-clock,'meaning_review_performed':False,'repair_performed':False,'acceptance_granted':False,'note':'Current queue after later authorized coordinator/claim transitions is NOT frozen input; caller must separately validate exact authorized field/event changes, current scope and actual packet. A successful byte check is not claim readiness or source/semantic acceptance.'}
 target.parent.mkdir(parents=True,exist_ok=True)
 with target.open('x',encoding='utf-8',newline='\n') as stream:json.dump(result,stream,indent=2);stream.write('\n')
 print(json.dumps(result,indent=2))
