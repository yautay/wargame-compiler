"""Operator-scoped foundation audit and IG-1C readiness preparation."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
RUN = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'src'))
from wgc.inputs.snapshot import verify_snapshot

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(name, value):
    if (RUN / name).exists():
        assert load(RUN / name) == value, 'Preserve prior evidence: ' + name
        return
    with (RUN / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')

q = load('docs/work/queue.json')
tasks = {t['id']: t for t in q['tasks']}
assert {k: tasks[k]['status'] for k in ['IG-1A','IG-1B','IG-1C','IG-1D','IG-1E']} == dict(zip(['IG-1A','IG-1B','IG-1C','IG-1D','IG-1E'], ['done','done','planned','planned','planned']))
rows = []
for task in ['IG-1A', 'IG-1B']:
    for event in tasks[task]['events']:
        assert sha(event['evidence']) == event['sha256']
    accepted = load(next(e['evidence'] for e in reversed(tasks[task]['events']) if e['to']=='accepted'))
    for a in accepted['artifacts']:
        actual = sha(a['path'])
        assert actual == a['sha256'], a
        rows.append({**a, 'task': task, 'verified_path': a['path']})
    write(task + '-accepted-audit.json', {'artifact_count': len(accepted['artifacts']), 'all_match': True})
delivery = 'private/workflow/runs/IG-1B/attempt-review-repair-01-20261012T193641Z/delivery.json'
review = 'private/workflow/runs/IG-1B/review-rereview01-20261012T194946Z/review.json'
assert sha(delivery)=='cf1c928b34aa70ae5b7cf59928baa273c45b02fc26331f8f534f6d1d8056c236'
assert sha(review)=='a437521ea9feec705ac01039b28e133a0deceaa47b1cd49bead955af34989f10'
r = load(review)
assert r['technical_pass'] is True
for a in r['artifacts']:
    assert sha(a['path']) == a['sha256']
for pair in r['prior_preservation']['complete_baseline_mapping']:
    assert sha(pair['preserved_copy']['path']) == pair['original']['sha256']
a_review = load(load(next(e['evidence'] for e in reversed(tasks['IG-1A']['events']) if e['to']=='accepted'))['independent_review']['path'])
assert a_review['technical_result'] == 'pass'
input_path = 'private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df'
source_path = 'private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008'
im, sm = verify_snapshot(input_path), verify_snapshot(source_path)
assert sm['selection']['identity_to_wgu_original']=='unknown'
available = [f for m in [im,sm] for f in m['files'] if f['availability']=='available']
external = ['C:/repo/wargame-utils/wgu/schemas/kb.schema.json', 'C:/repo/wargame-utils/wgu/kb/store.py', 'C:/repo/wargame-utils/wgu/kb/export.py', 'C:/repo/wargame-utils/wgu/kb/lint.py']
write('configuration.json', {'model':'gpt-6.1-sol','reasoning':'high','source':'Direct operator observation of this current conversation UI','operator_statement':'sol 6.1 high','runtime_metadata':None,'recorded_utc':datetime.now(timezone.utc).isoformat()})
write('foundation-audit.json', {'artifacts':rows,'ig_1b_delivery_count':len(load(delivery)['artifacts']), 'ig_1b_independent_review_artifacts':len(r['artifacts']), 'preserved_baseline_count':len(r['prior_preservation']['complete_baseline_mapping']), 'input':{'path':input_path,'sha256':sha(Path(input_path)/'manifest.json')}, 'source':{'path':source_path,'sha256':sha(Path(source_path)/'manifest.json')}, 'available_game_files':sum(f['availability']=='available' for f in im['files']), 'available_registry_files':sum(f['availability']=='available' for f in sm['files']), 'available_bytes':sum(f['bytes'] for f in available), 'missing_sources':sum(f['availability']=='missing' for f in im['files']), 'identity_to_wgu_original':'unknown','external_scope':[{'path':p,'sha256':sha(p),'bytes':Path(p).stat().st_size} for p in external]})
write('queue-before.json',q)
t = tasks['IG-1C']
t['inputs'] = ['Complete frozen input: '+input_path+'/manifest.json SHA-256 '+sha(Path(input_path)/'manifest.json'), 'Selected source registry: '+source_path+'/manifest.json SHA-256 '+sha(Path(source_path)/'manifest.json')] + ['Read-only support: '+p+' SHA-256 '+sha(p) for p in external]
t['context'] += ['src/wgc/inputs/snapshot.py']
t['write_scope'] += ['.venv/']
t['inputs'] += ['Operator-authorized dependency exception: project-local pinned PyYAML safe parser only in .venv; obtain official PyPI metadata/wheel if no local wheel exists; record version/source/hash. No foundation edits.']
with Path('docs/work/queue.json').open('w',encoding='utf-8') as stream:
    json.dump(q,stream,ensure_ascii=False,indent=2);stream.write('\n')
write('scope-decision.json', {'role':'coordinator','actor':'ig1-stage-executor-20261013','summary':'Pin exact complete frozen input and four read-only WGU support files; add only operator-authorized project-local parser dependency scope. Product implementation scope remains parser.py/importer.py/tests/private import runs.','operator_authorization':'Current pasted OBJECTIVE and TASK IG-1C instructions','product_scope_unchanged':True,'dependency_scope':'.venv/','foundation_unchanged':True})
write('ready.json', {'role':'coordinator','actor':'ig1-stage-executor-20261013','summary':'Verified IG-1A/IG-1B done, exact accepted lists and independent PASS; sealed names/manifests/copy hashes verified; current executor Sol/high confirmed by operator; only IG-1C ownership assigned.','criteria':t['start_conditions'],'artifacts':[{'path':str((RUN/n).relative_to(ROOT)).replace('\\','/'),'sha256':sha(RUN/n)} for n in ['foundation-audit.json','configuration.json','scope-decision.json']], 'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'configuration.json: direct current-session operator UI observation','checks':[{'command':'workflow.py validate','exit_code':0},{'command':'workflow.py next','exit_code':0}]})
print(json.dumps({'available_files':len(available),'bytes':sum(f['bytes'] for f in available),'accepted_artifacts':len(rows),'ready_evidence':str(RUN/'ready.json')}))
