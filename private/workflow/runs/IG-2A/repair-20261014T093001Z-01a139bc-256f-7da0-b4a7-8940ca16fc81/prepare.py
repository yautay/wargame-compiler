"""Current coordinator verification; immutable prior runs are read only."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
RUN = Path(__file__).resolve().parent
OLD = ROOT / 'private/workflow/runs/IG-2A/attempt-20261013T155212Z'
REVIEW = ROOT / 'private/workflow/runs/IG-2A/review-20261013T171051Z-codex-01a1363e-1de5-7073-8185-d9a1f2e89c35'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, value):
    (RUN / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

def pin(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path), 'bytes': path.stat().st_size}

def command(name, argv):
    start = datetime.now(timezone.utc); clock = time.monotonic()
    result = subprocess.run(argv, capture_output=True, text=True)
    (RUN / (name + '.stdout')).write_text(result.stdout, encoding='utf-8', newline='\n')
    (RUN / (name + '.stderr')).write_text(result.stderr, encoding='utf-8', newline='\n')
    record = {'command': subprocess.list2cmdline(argv), 'argv': argv, 'exit_code': result.returncode,
              'started_utc': start.isoformat(), 'ended_utc': datetime.now(timezone.utc).isoformat(),
              'wall_seconds': time.monotonic()-clock, 'stdout': name+'.stdout', 'stderr': name+'.stderr'}
    write(name+'.json', record)
    return record

def prepare():
    expected = {REVIEW/'final-seal.json': 'd45b128f0e3be2cb0f3a97c4e7b91c955fe2760474ca78e6dbeca379089d864a',
                REVIEW/'review-manifest.json': '5bef17ff2526b5f423704625d8eb31c5e49229b3f4c010140be9833f48d02c73',
                REVIEW/'report.md': 'c25fdb5881afe2ace484148141c48ab6c56f47e58a390367d7aaaf54189b21ed',
                OLD/'delivery.json': '31a175fb77f14a586f03327c3674a05a4b4ae9f7296932ef757669428d454290'}
    checked = []
    def verify(path, expected_hash, expected_bytes=None):
        actual = pin(path); actual['expected_sha256'] = expected_hash
        actual['matches'] = actual['sha256']==expected_hash and (expected_bytes is None or actual['bytes']==expected_bytes)
        checked.append(actual)
        if not actual['matches']: raise ValueError('Frozen mismatch: '+str(path))
    for p, h in expected.items(): verify(p,h)
    for p in [OLD/'final-seal.json', REVIEW/'final-seal.json', REVIEW/'coordinator-handoff.json']:
        for v in json.loads(p.read_text()).values():
            if isinstance(v,dict) and 'path' in v and 'sha256' in v: verify(ROOT/v['path'],v['sha256'])
    totals = {}
    for p in [OLD/'delivery.json', OLD/'delivery-manifest.json', REVIEW/'review-manifest.json']:
        entries = json.loads(p.read_text())['artifacts']; totals[str(p.relative_to(ROOT))]=len(entries)
        for e in entries: verify(ROOT/e['path'],e['sha256'],e.get('bytes'))
    q = json.loads((ROOT/'docs/work/queue.json').read_text())
    task = next(t for t in q['tasks'] if t['id']=='IG-2A')
    assert task['status']=='review' and task['events'][-1]['sha256']==expected[OLD/'delivery.json']
    assert sha(ROOT/'docs/work/queue.json')==json.loads((REVIEW/'final-seal.json').read_text())['queue_sha256']
    write('integrity.json', {'checked':checked,'totals':totals,'mismatches':0,'queue':pin(ROOT/'docs/work/queue.json')})
    shutil.copyfile(ROOT/'docs/work/queue.json', RUN/'queue-before.json')
    shutil.copyfile(ROOT/'docs/work/context-policy.json', RUN/'context-policy-before.json')
    products = [p for base in ('src/wgc/sources','tests/sources') for p in (ROOT/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    products += [ROOT/'contracts/ig/regions.schema.json']
    old_entries = json.loads((OLD/'delivery.json').read_text())['artifacts']
    for e in old_entries + [pin(OLD/'delivery.json'),pin(OLD/'final-seal.json')]:
        src = ROOT/e['path']; dest=RUN/'original-delivery'/e['path']; dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest); assert sha(dest)==e['sha256']
    for p in products:
        dest=RUN/'product-before'/p.relative_to(ROOT); dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,dest); assert sha(dest)==sha(p)
    write('base-products.json', [pin(p) for p in products])
    write('frozen-tools.json', [pin(ROOT/p) for p in ('scripts/workflow.py','scripts/check.ps1','scripts/search.ps1','src/wgc/contracts/source.py','contracts/ig/source.schema.json','contracts/ig/README.md')])
    command('initial-status',['git','status','--short'])
    from wgc.sources.inventory import validate
    probes = []
    names = ['baseline','exact_exclusion_claim','stale_page_rotation','stale_page_userunit','stale_page_crop','false_render_dpi',
             'wrong_page_printed_label','exclusion_after_region_revision','exclusion_after_registry_change',
             'exclusion_after_page_remap','false_consistent_page_count','physical_page_remapping']
    for name in names:
        path=REVIEW/'p2'/(name+'.input.json'); doc=json.loads(path.read_text()); start=time.monotonic()
        try: report=validate(doc,ROOT); error=None
        except Exception as exc: report=None; error=f'{type(exc).__name__}: {exc}'
        probes.append({'name':name,'input':pin(path),'actual':'accept' if error is None else 'reject','error':error,'report':report,'wall_seconds':time.monotonic()-start})
    assert all(p['actual']=='accept' for p in probes)
    write('coordinator-reproductions.json',probes)
    findings=json.loads((REVIEW/'findings.json').read_text())['findings']
    mapping={'IG2A-R01':names[2:5],'IG2A-R02':[names[5]],'IG2A-R03':[names[6]],'IG2A-R04':names[7:10],'IG2A-R05':names[10:]}
    dispositions=[{'id':f['id'],'severity':f['severity'],'disposition':'confirmed','evidence':mapping[f['id']],
                   'consequence':f['consequence'],'closure_condition':f['repair_verification'],'repair_cycles':0} for f in findings]
    write('dispositions-before.json',dispositions)
    scope={'task':'IG-2A','findings':[f['id'] for f in findings],'product_write_scope':['src/wgc/sources/','tests/sources/','contracts/ig/regions.schema.json'],
           'evidence_write_scope':RUN.relative_to(ROOT).as_posix()+'/', 'source_read_pages':[1,2,3,4],
           'all_page_access':'Structure/count/geometry only','source_pdf':pin(ROOT/'private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'),
           'excluded':'IG-2B, frozen workflow tools and prior runs, source PDF, IG-1A contract, acceptance/done, external APIs, agents, Git history',
           'repair_plan':'Pin evidence page basis; verify actual source count/geometry; bind physical-page author keys; cross-check DPI with Poppler ceiling dimensions; bind label to same page; hash coverage-independent exact author/registry/page/partition scope.'}
    write('scope.json',scope)
    config=json.loads((RUN/'configuration.json').read_text())
    check=command('coordinator-workflow',[sys.executable,'scripts/workflow.py','validate']); assert check['exit_code']==0
    evidence={'role':'coordinator','actor':config['actor'],'summary':'Confirmed five independently reproduced findings; bounded IG-2A repair requested by current operator.',
              'criteria':task['acceptance'],'artifacts':[pin(RUN/p) for p in ('configuration.json','integrity.json','scope.json','dispositions-before.json','coordinator-reproductions.json')],
              'model':config['model'],'reasoning':config['reasoning'],'configuration_evidence':(RUN/'configuration.json').relative_to(ROOT).as_posix(),
              'checks':[check],'review_seal':pin(REVIEW/'final-seal.json'),'semantic_acceptance_granted':False}
    write('coordinator-decision.json',evidence)
    write('checkpoint-preclaim.json',{'task':'IG-2A','actor':config['actor'],'configuration':pin(RUN/'configuration.json'),
          'base_products':json.loads((RUN/'base-products.json').read_text()),'scope':pin(RUN/'scope.json'),
          'completed':['Frozen integrity verified','All five findings reproduced','Verified original delivery copies retained'],
          'next_operation':'Coordinator transition to changes_requested, fresh allowlisted packet, executor claim','blocker':None})
    print('Verified, preserved and reproduced all five findings.')

if __name__=='__main__': prepare()
