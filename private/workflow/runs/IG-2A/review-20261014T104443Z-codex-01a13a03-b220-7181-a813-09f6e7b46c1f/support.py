import os, sys, json, hashlib, subprocess, time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(r'C:\repo\wargame-compiler')
RUN = Path(__file__).resolve().parent
REPAIR = ROOT / 'private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81'
PRIOR = ROOT / 'private/workflow/runs/IG-2A/review-20261013T171051Z-codex-01a1363e-1de5-7073-8185-d9a1f2e89c35'
PREP = ROOT / 'private/workflow/runs/IG-2A/review-preparation-20261014T101407Z-01a139bc-256f-7da0-b4a7-8940ca16fc81'
BUNDLE = Path(r'C:\Users\yauta\.cache\codex-runtimes\codex-primary-runtime\dependencies')
PYTHON = ROOT / '.venv/Scripts/python.exe'
POPPLER = BUNDLE / 'native/poppler/Library/bin'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONPATH'] = os.pathsep.join(map(str, [ROOT/'src', ROOT/'.venv/Lib/site-packages', BUNDLE/'python/Lib/site-packages']))
os.environ['PATH'] = str(POPPLER) + os.pathsep + os.environ['PATH']
sys.path[:0] = [str(ROOT/'src'), str(BUNDLE/'python/Lib/site-packages')]
sys.dont_write_bytecode = True

def utc(): return datetime.now(timezone.utc).isoformat()
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(name, value):
    path = RUN / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return path
def pin(path):
    path = Path(path)
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path), 'bytes': path.stat().st_size}
def command(name, args, env=None):
    start, t = utc(), time.monotonic()
    result = subprocess.run(list(map(str,args)), cwd=ROOT, env=env, capture_output=True)
    (RUN/(name+'.stdout')).write_bytes(result.stdout)
    (RUN/(name+'.stderr')).write_bytes(result.stderr)
    record = {'command':subprocess.list2cmdline(list(map(str,args))), 'argv':list(map(str,args)), 'exit_code':result.returncode, 'started_utc':start, 'ended_utc':utc(), 'wall_seconds':time.monotonic()-t, 'stdout':name+'.stdout', 'stderr':name+'.stderr'}
    write(name+'.json',record)
    print(name, result.returncode, result.stdout.decode(errors='replace')[-1000:], result.stderr.decode(errors='replace')[-500:])
    return record
