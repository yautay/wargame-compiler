"""Read-only hash/status gate. Writes only the explicitly supplied fresh report.
This verifies bytes/structure, not source meaning or independent review completion.
"""
import argparse,hashlib,json,os,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('C:/repo/wargame-compiler').resolve()
LAUNCH=Path(__file__).resolve().parent
DELIVERY='private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
PACKET='private/workflow/packets/IG-2B02-0851cf2e8efe4e0b818505d7727cb94f'
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def digest(path):
 with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def verify(pin):
 path=Path(pin['path']);path=path if path.is_absolute() else ROOT/path
 assert path.is_file() and not path.is_symlink() and path.stat().st_size==pin['bytes'] and digest(path)==pin['sha256'],pin['path']
 return path
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',required=True);args=parser.parse_args();started=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
 destination=Path(args.report);destination=destination if destination.is_absolute() else ROOT/destination
 assert not destination.exists(),'Output report must be new'
 prep=load(LAUNCH/'preparation.json');verify(prep['queue']);verify(prep['packet_manifest']);verify(prep['packet_context']);verify(prep['review_skill'])
 expected={'delivery-transition-envelope.json':'c02077ee51ff4dc773385942de23fe0f1428ddf7cc038b45a8464e78056c5a19','delivery-manifest.json':'593fbe0c8af8166b241382df47513e20e05851ae65ab30c03f9c46834732796b','final-seal.json':'4fad3c1c4284105d93763dca713313a008c80ea0a72a30e7ffb23cd386bdc878','review-handoff-final.md':'fc5b99afa1a5b50fcc89b3571295c4cd3e0679b1450442a729cf822e06465c92'}
 for name,sha in expected.items():assert digest(ROOT/DELIVERY/name)==sha,name
 queue=load(ROOT/'docs/work/queue.json');task=next(t for t in queue['tasks'] if t['id']=='IG-2B02');event=task['events'][-1]
 assert task['status']=='review' and len(task['events'])==3 and event['from']=='in_progress' and event['to']=='review' and event['evidence']==DELIVERY+'/delivery-transition-envelope.json' and event['sha256']==expected['delivery-transition-envelope.json']
 assert all(next(t for t in queue['tasks'] if t['id']==dep)['status']=='done' for dep in ('IG-2A','IG-2B01'))
 envelope=load(ROOT/DELIVERY/'delivery-transition-envelope.json');manifest=load(ROOT/DELIVERY/'delivery-manifest.json');seal=load(ROOT/DELIVERY/'final-seal.json');packet=load(ROOT/PACKET/'manifest.json')
 assert seal['review_event']==event and seal['authoritative_transition_delivery']['sha256']==event['sha256']
 assert seal['actor']==envelope['actor']=='codex-01a13c20-b7bd-7962-a954-f5841c09831c'
 assert envelope['criteria']==task['acceptance'] and all(c['exit_code']==0 for c in envelope['checks'])
 sections=[]
 for pin in packet['files']:
  path=verify(pin)
  if path.suffix.lower() in ('.md','.json','.py','.ps1','.toml'):sections.append('\n--- FILE: '+pin['path']+' ---\n'+path.read_text(encoding='utf-8-sig'))
 payload='\n'.join(sections);assert len(payload.encode('utf-8'))==packet['text_bytes'] and payload.replace('\n','\r\n').encode('utf-8')==(ROOT/PACKET/'context.txt').read_bytes()
 pins={}
 for group in (envelope['artifacts'],manifest['new_reviewed_artifacts'],manifest['immutable_inputs_and_old_evidence'],seal['postfreeze_recovery_and_epilogue_artifacts']):
  for pin in group:
   if pin['path'] in pins:assert pins[pin['path']]==pin,pin['path']
   pins[pin['path']]=pin
 for pin in pins.values():verify(pin)
 assert len(envelope['artifacts'])==2895 and len(manifest['new_reviewed_artifacts'])==1462 and len(manifest['immutable_inputs_and_old_evidence'])==1428 and len(seal['postfreeze_recovery_and_epilogue_artifacts'])==40
 result={'outcome':'passed_byte_status_gate_only','task':'IG-2B02','queue_status':task['status'],'review_event':event,'executor_actor':envelope['actor'],'unique_frozen_refs_verified':len(pins),'approved_ordered_artifact_count':len(envelope['artifacts']),'manifest_new_artifacts':1462,'manifest_immutable_inputs':1428,'final_seal_postfreeze_artifacts':40,'packet_payload_logical_bytes':packet['text_bytes'],'packet_context_physical_bytes':prep['packet_context']['bytes'],'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-clock,'helper_sha256':digest(Path(__file__)),'warning':'No source content inspected; these facts do not satisfy independent review or authenticity/semantic acceptance.'}
 destination.parent.mkdir(parents=True,exist_ok=True)
 with destination.open('x',encoding='utf-8',newline='\n') as stream:json.dump(result,stream,indent=2);stream.write('\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
