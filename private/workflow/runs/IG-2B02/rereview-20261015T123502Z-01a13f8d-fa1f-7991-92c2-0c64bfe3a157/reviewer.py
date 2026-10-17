"""Independent reviewer utilities; writes confined to this new review directory."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, time

ROOT = Path('C:/repo/wargame-compiler')
OUT = Path(__file__).resolve().parent
REPAIR = ROOT/'private/workflow/runs/IG-2B02/repair-r01-r02-20261015T091559Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c'
OLD = ROOT/'private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
PREVIOUS = ROOT/'private/workflow/runs/IG-2B02/review-20261015T062645Z-01a13e3c-b2ef-7d90-bdfa-975891f92634'
PACKET = ROOT/'private/workflow/packets/IG-2B02-191a1946c4954dd29452ae824907a264'
SID = '01a13f8d-fa1f-7991-92c2-0c64bfe3a157'
RUNTIME = Path('C:/Users/yauta/.codex/sessions/2026/10/15/rollout-2026-10-15T14-33-51-'+SID+'.jsonl')
def utc(): return datetime.now(timezone.utc).isoformat()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(name, obj):
    p = OUT/name
    assert p.resolve().is_relative_to(OUT)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def pins(x):
    if isinstance(x,dict):
        if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str): yield x
        for v in x.values(): yield from pins(v)
    elif isinstance(x,list):
        for v in x: yield from pins(v)
def check_pins(objects):
    seen={}; occurrences=0; errors=[]
    for obj in objects:
        for target in pins(obj):
            occurrences+=1; path=ROOT/target['path']
            if not path.resolve().is_relative_to(ROOT) and path.suffix.lower() not in ['.exe','.json']:
                errors.append(dict(target=target,error='unexpected external pin')); continue
            key=(target['path'],target['sha256'],target.get('bytes'))
            if key in seen: continue
            try:
                actual=pin(path)
                ok=actual['sha256']==target['sha256'] and ('bytes' not in target or actual['bytes']==target['bytes'])
                seen[key]=dict(expected=target,actual=actual,match=ok)
                if not ok: errors.append(seen[key])
            except OSError as e: errors.append(dict(target=target,error=str(e)))
    return dict(utc=utc(),occurrences=occurrences,unique_pin_count=len(seen),errors=errors,results=list(seen.values()))
def run(name,args,env=None):
    start=utc(); t=time.monotonic()
    result=subprocess.run(args,cwd=ROOT,env=env,capture_output=True)
    (OUT/(name+'.stdout')).write_bytes(result.stdout)
    (OUT/(name+'.stderr')).write_bytes(result.stderr)
    record=dict(command=subprocess.list2cmdline([str(a) for a in args]),argv=[str(a) for a in args],exit_code=result.returncode,started_utc=start,ended_utc=utc(),wall_seconds=time.monotonic()-t,stdout=pin(OUT/(name+'.stdout')),stderr=pin(OUT/(name+'.stderr')),retry=0)
    write(name+'.json',record); return record
def preflight():
    records=[]
    for line in RUNTIME.open(encoding='utf-8'):
        j=json.loads(line)
        if j['type']=='session_meta':
            records.append(dict(type=j['type'],timestamp=j['timestamp'],id=j['payload']['id'],model_provider=j['payload'].get('model_provider'),cli_version=j['payload'].get('cli_version')))
        elif j['type']=='turn_context':
            p=j['payload']; records.append(dict(type=j['type'],timestamp=j['timestamp'],model=p.get('model'),effort=p.get('effort'),settings=p.get('collaboration_mode',{}).get('settings',{})))
            records[-1]['settings'].pop('developer_instructions',None)
            break
    assert records[0]['id']==SID and records[-1]['model']=='gpt-6.1-sol' and records[-1]['effort']=='high'
    write('configuration.json',dict(session_id=SID,actor='codex-'+SID,model='gpt-6.1-sol',reasoning='high',observed_utc=utc(),evidence_source=str(RUNTIME),runtime_records=records,environment_identity={k:os.environ.get(k) for k in ['CODEX_SESSION_ID','CODEX_THREAD_ID','CODEX_VERSION']},requested_flags_are_not_proof=True,independent_of=['01a13c20-b7bd-7962-a954-f5841c09831c','01a13f2d-eb41-7760-9e94-99f0508d544a','01a13e3c-b2ef-7d90-bdfa-975891f92634'],usage=dict(input_tokens=None,output_tokens=None,reason='Reliable per-review token usage not exposed',operator_seconds=None)))
    direct=[(REPAIR/'independent-rereview-launch.txt',21882,'c1db1ef5dd01784287bd08c0a846fd3e1f8c0dc157b5a31fc041df2da8088f8c'),(REPAIR/'final-seal.json',33977,'e8a6dafff6de73761a7422d8a6fe6ad161320d8bcdbddc85ab4f5be67ac8b598'),(REPAIR/'rereview-input-pins.json',1216245,'af0d993dd12ab162394ee133da8f967e69204d8f2e2294c48dc29a3601e09485'),(PACKET/'manifest.json',6500,'9482c383b99e0434177b3754555216f9c54467fa64e8ef75c5252eb5c2ccdc23'),(PACKET/'context.txt',99349,'3b7080285bc98bdff2d7525acc56cb0a445e5925e15ab5b289d4fb3950b233f7')]
    objects=[[dict(path=p.relative_to(ROOT).as_posix(),bytes=n,sha256=h) for p,n,h in direct]]
    objects += [read(REPAIR/n) for n in ['rereview-input-pins.json','delivery.json','delivery-manifest.json','final-seal.json']]
    objects += [read(PACKET/'manifest.json')]
    audit=check_pins(objects); write('launch-byte-audit.json',audit)
    queue=read(ROOT/'docs/work/queue.json'); task=next(t for t in queue['tasks'] if t['id']=='IG-2B02')
    index=read(REPAIR/'rereview-input-pins.json'); delivery=read(REPAIR/'delivery.json')
    write('checkpoint.json',dict(task='IG-2B02',actor='codex-'+SID,started_utc='2026-10-15T12:33:55.587Z',recorded_utc=utc(),configuration=pin(OUT/'configuration.json'),queue=pin(ROOT/'docs/work/queue.json'),status=task['status'],delivery_artifact_count=len(delivery['artifacts']),ordered_list_matches=delivery['artifacts']==index['ordered_delivery_artifacts'],input_pins=audit['unique_pin_count'],pin_errors=len(audit['errors']),completed=['own configuration confirmed','immutable launch hashes checked'],next='Independent complete source and metadata review',history_scope='Only explicitly pinned current task delivery, earlier review/base, accepted baseline and own runtime configuration. No archive or Git history.',write_scope='New reviewer directory plus fresh permitted check outputs',acceptance_granted=False))
    print(json.dumps({k:v for k,v in read(OUT/'checkpoint.json').items() if k not in ['completed','history_scope','write_scope']}))
    print('pin errors:',json.dumps(audit['errors']))
if __name__=='__main__': preflight()
