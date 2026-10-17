"""Independent review orchestration. All mutations confined to reviewer/check scope."""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path('C:/repo/wargame-compiler')
R=Path(__file__).resolve().parent
D=ROOT/'private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
P=ROOT/'private/workflow/runs/IG-2B02/review-launch-preparation-20261014T221144Z-01a13c20-b7bd-7962-a954-f5841c09831c'
B=ROOT/'private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77'
N=Path('C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native')
PY=ROOT/'.venv/Scripts/python.exe'
POP=N/'poppler/Library/bin'
env=os.environ.copy()
env['PYTHONDONTWRITEBYTECODE']='1'
env['PYTHONPATH']=str(ROOT/'src')+';C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages'
env['PATH']=str(POP)+';'+env['PATH']
env['GIT_OPTIONAL_LOCKS']='0'

def utc():return datetime.now(timezone.utc).isoformat()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def pin(p):
    p=Path(p);return {'path':p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
def write(name,data):
    path=R/name
    assert path.is_relative_to(R)
    with path.open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
def run(name,args):
    logs=R/'commands';logs.mkdir(exist_ok=True)
    assert not (logs/(name+'.json')).exists()
    start=utc();clock=time.monotonic()
    result=subprocess.run([str(x) for x in args],cwd=ROOT,env=env,capture_output=True)
    for suffix,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        with (logs/(name+'.'+suffix)).open('xb') as f:f.write(data)
    record={'command':[str(x) for x in args],'cwd':ROOT.as_posix(),'started_utc':start,'ended_utc':utc(),'wall_seconds':time.monotonic()-clock,'exit_code':result.returncode,'stdout':pin(logs/(name+'.stdout')),'stderr':pin(logs/(name+'.stderr')),'process_environment':{k:env[k] for k in ('PYTHONDONTWRITEBYTECODE','PYTHONPATH')}}
    write('commands/'+name+'.json',record)
    print(name, result.returncode, result.stdout.decode('utf-8',errors='replace')[-3500:], result.stderr.decode('utf-8',errors='replace')[-1800:],flush=True)
    if result.returncode:raise RuntimeError(f'{name} failed; dependent work stopped')
    return record

def checkpoint(stage,completed,next_operation,blocker=None):
    previous=load(R/'checkpoint.json')
    snapshots=R/'checkpoints';snapshots.mkdir(exist_ok=True)
    index=len(list(snapshots.glob('*.json')))
    (snapshots/f'{index:03}.json').write_bytes((R/'checkpoint.json').read_bytes())
    data={**previous,'utc':utc(),'stage':stage,'completed':completed,'next_operation':next_operation,'blocker':blocker,
          'unmet': ['Product criterion 1: IG-2B02-R01/R02 grouped-component defects; coordinator repair decision required.'] if stage=='review_ready_to_freeze' else previous['unmet'],
          'unreviewed_criteria': [] if stage=='review_ready_to_freeze' else None,
          'queue':pin(ROOT/'docs/work/queue.json'),'packet':pin(ROOT/'private/workflow/packets/IG-2B02-0851cf2e8efe4e0b818505d7727cb94f/context.txt'),
          'source_contract_tool_baseline_registry_pins':{'catalogue':pin(P/'frozen-pins.json'),'gate':pin(R/'input-hash-audit.json')},
          'commands':[load(p) for p in sorted((R/'commands').glob('*.json'))],
          'base_owned_hashes':[pin(snapshots/f'{index:03}.json')],
          'current_owned_hashes':[pin(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='checkpoint.json'],
          'wall_seconds':(datetime.now(timezone.utc)-datetime.fromisoformat(previous['start_utc'].replace('Z','+00:00'))).total_seconds()}
    (R/'checkpoint.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

def gate():
    expected={'preparation.json':(1238,'c06c404c514a10b09ba4fa38b5817ba64fea8dcecbe8ac9821d51980e190aba6'),'verify-frozen-review-inputs.py':(4868,'1d864d7017ea2548c60346798276ef822945a5bce9a2e9cb0f0816d62894a102'),'frozen-pins.json':(1623594,'d85b53b858304c2c5a7a052caa682c493abe79575b60d1d29c01e6468082ca97')}
    for name,(size,sha) in expected.items():assert (P/name).stat().st_size==size and digest(P/name)==sha,name
    run('01-frozen-input-gate',[PY,'-B',P/'verify-frozen-review-inputs.py','--report',(R/'input-hash-audit.json').relative_to(ROOT).as_posix()])
    cat=load(P/'frozen-pins.json')
    print('Catalogue sections:',[(k,len(v) if isinstance(v,list) else type(v).__name__) for k,v in cat.items()])
    run('02-workflow-validate',[PY,'-B','scripts/workflow.py','validate'])
    run('03-workflow-next',[PY,'-B','scripts/workflow.py','next'])
    run('04-working-tree-baseline',['git','status','--porcelain=v1','--untracked-files=normal'])
    run('05-root-inventory-validate',[PY,'-B','-m','wgc.sources','validate',(D/'final-verified/inventory.json').relative_to(ROOT).as_posix()])
    (R/'originals').mkdir()
    run('06-original-pages',[POP/'pdftoppm.EXE','-f','5','-l','8','-cropbox','-r','144','-png','private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf',R/'originals/original'])

if __name__=='__main__':
    {'gate':gate}[sys.argv[1]]()
