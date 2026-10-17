from datetime import datetime, timezone
import hashlib,json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5];RUN=Path(__file__).resolve().parent
STAGE=ROOT/'private/workflow/runs/IG-1E/stage-20261013'
PACKET=ROOT/'private/workflow/packets/IG-1E-d18b6ad686714c4fa531ced10229d05b'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(a):
    p=ROOT/a.get('verified_path',a['path'])
    assert p.resolve().is_relative_to(ROOT)
    assert sha(p)==a['sha256'],(a,sha(p))
    return {**a,'actual_sha256':sha(p),'verified_path':p.relative_to(ROOT).as_posix()}
phase=sys.argv[1]
delivery=STAGE/'delivery.json'
assert sha(delivery)=='5a2d7595085ef19877f921da96ea79647493ed73a813b5ce29b36d80b4f60e54'
d=read(delivery);assert len(d['artifacts'])==len({a['path'] for a in d['artifacts']})==50
current=[verify(a) for a in d['artifacts']]
q=read(ROOT/'docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-1E')
assert t['status']=='review' and d['criteria']==t['acceptance']
assert all(next(t for t in q['tasks'] if t['id']==s)['status']=='done' for s in ['IG-1A','IG-1B','IG-1C','IG-1D'])
assert t['events'][-1]['evidence']==delivery.relative_to(ROOT).as_posix() and t['events'][-1]['sha256']==sha(delivery)
pres=read(STAGE/'preservation.json')
foundations=[verify(a) for a in pres['accepted_foundation_artifacts']]
inputs=[verify(a) for a in pres['pinned_inputs']]
assert len(foundations)==233 and len(inputs)==22
packet=read(PACKET/'manifest.json')
assert packet['queue_sha256']==sha(ROOT/'docs/work/queue.json')
assert packet['context_sha256']==sha(PACKET/'context.txt')
packet_files=[verify(a) for a in packet['files']]
pins=[]
for entry in t['inputs']:
    m=re.fullmatch(r'(.+) SHA-256 ([0-9a-f]{64})',entry)
    if m:pins.append(verify({'path':m[1],'sha256':m[2]}))
assert len(pins)==22
prior_manifest=ROOT/'private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/review-manifest.json'
prior_artifacts=[verify(a) for a in read(prior_manifest)['artifacts']]
seal=ROOT/'private/ig/projects/spqr/snapshots/sha256-4571340270f16519ee8207f0e474e6e71620ae11d74a1c787f273bb617a34fa7/manifest.json'
assert sha(seal)=='8c3da679b4cc3f5b08bf0f9ad4db633bf7ff037bceb96bb41be4f310577ba6b4'
report={'phase':phase,'utc':datetime.now(timezone.utc).isoformat(),'all_match':True,
    'delivery':{'path':delivery.relative_to(ROOT).as_posix(),'sha256':sha(delivery),'artifacts':current,'artifact_count':50},
    'queue_sha256':sha(ROOT/'docs/work/queue.json'),'queue_states':{t['id']:t['status'] for t in q['tasks'] if t['id'].startswith('IG-1')},
    'foundations':foundations,'inputs':inputs,'task_input_pins':pins,'prior_IG1D_review_artifacts':prior_artifacts,
    'packet':{'path':(PACKET/'manifest.json').relative_to(ROOT).as_posix(),'sha256':sha(PACKET/'manifest.json'),'files':packet_files},
    'configuration_continuity':read(RUN/'checkpoint.json')['configuration_evidence']}
with (RUN/('verification-'+phase+'.json')).open('x',encoding='utf-8') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps({'phase':phase,'delivery':50,'foundations':233,'inputs':22,'prior_review':len(prior_artifacts),'all_match':True,'queue_sha256':report['queue_sha256']}))
