"""Freeze second bounded R04 delivery with all reviewed previous bytes retained."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re

ROOT = Path.cwd(); RUN = Path(__file__).resolve().parent
def read(p): return json.loads(Path(p).read_bytes())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def art(p):
    p = Path(p)
    return {'path': (p.relative_to(ROOT) if p.is_absolute() else p).as_posix(), 'sha256': sha(p)}
def write(name, data):
    with (RUN/name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2); f.write('\n')

scope = read(RUN/'repair-scope.json')
parent = read(scope['parent_delivery']['path'])
review = read(scope['independent_review']['path'])
versions = read('private/workflow/runs/IG-1D/operator-checkpoint-20261013T132827Z/verified-artifact-manifest.json')
baseline = read(RUN/'baseline-manifest.json')['files']
copies = {(a['path'], a['sha256']): a.get('verified_path', a['path']) for a in versions}
copies.update({(b['original']['path'], b['original']['sha256']): b['preserved_copy']['path'] for b in baseline})
def preserved(a):
    candidate = Path(a['path'])
    path = candidate if sha(candidate) == a['sha256'] else Path(copies[(a['path'], a['sha256'])])
    assert sha(path) == a['sha256'], a['path']
    return {**a, 'verified_path': art(path)['path']}
rows = [preserved(a) for a in parent['artifacts']]
prior = [preserved(a) for a in versions]
review_manifest = read(scope['independent_review_manifest']['path'])
review_rows = [preserved(a) for a in review_manifest['artifacts']]
q = read('docs/work/queue.json')
foundations = []
for task in q['tasks']:
    if task['id'] in ['IG-1A', 'IG-1B', 'IG-1C']:
        assert task['status'] == 'done'
        accepted = read(next(e['evidence'] for e in reversed(task['events']) if e['to'] == 'accepted'))
        foundations.extend(preserved(a) for a in accepted['artifacts'])
write('preservation.json', {'parent_delivery_versions': rows, 'checkpoint_versions': prior,
                          'independent_review_versions': review_rows, 'foundation_versions': foundations,
                          'all_previous_versions_retained': True})
checks = [read(RUN/(name+'-check.json')) for name in ['explicit', 'accounting', 'project', 'diff']]
assert all(c['exit_code'] == 0 for c in checks)
account = read(RUN/'independent-accounting.json')
assert account['result'] == 'pass' and account['two_complete_outputs_and_packages_byte_identical']
original_audit = Path('private/workflow/runs/IG-1D/replacement-rereview-20261013T140127Z/accounting.py').read_text(encoding='utf-8')
assert (RUN/'accounting.py').read_text(encoding='utf-8') == original_audit.replace("'review_actor': 'ig1d-replacement-reviewer-20261013T140127Z'", "'executor_actor': 'ig1-continuation-executor-20261013'")
write('oracle-preservation.json', {'source': scope['independent_review'], 'assertions_unchanged': True,
                                 'only_script_delta': 'Operational publication actor; RUN naturally resolves to this new directory.',
                                 'original_oracle': art('private/workflow/runs/IG-1D/replacement-rereview-20261013T140127Z/accounting.py'),
                                 'current_oracle': art(RUN/'accounting.py')})
project_log = (RUN/'project.log').read_text(encoding='utf-8-sig')
checkroot = Path(re.search(r'LOG_ROOT=(.+)', project_log).group(1).strip())
project_result = read(checkroot/'result.json')
assert all(project_result[k] == 0 for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])
end = datetime.now(timezone.utc)
start = datetime.fromisoformat(read(RUN/'checkpoint.json')['started_utc'])
write('measurement.json', {'started_utc': start.isoformat(), 'ended_utc': end.isoformat(),
                          'wall_seconds': (end-start).total_seconds(), 'input_tokens': None,
                          'output_tokens': None, 'cost': None, 'operator_time_seconds': None})
report = '''# IG-1D bounded second R04 repair

The named lineage replay now examines all persisted receipt children before the
kind/scope filter. A reused decision with incompatible logical child kind, resolved
parent scope or persistent child key raises ValueError on a private registry copy.
The caller registry is unchanged, and no replacement allocation is returned. A new
decision identifier permits a deliberately different output contract.

New synthetic controls cover term-to-rule reuse, child-key addition/removal/change,
logical procedure scope changes, deliberately new typed decisions, keyed splits,
parent reordering and file movement with corrected content. Unique merge corrections,
rename, stable IDs/origin keys and historical origins remain covered. No original
reviewer assertion or existing test was changed. R01-R03 remain closed by the
independent repair-1 report; only R04 used its second and final repair cycle.

The full public adapter/export suite and all original, risk, receipt-edge and export
history probes passed. The required project and diff checks passed. The independent
full-input oracle was copied without assertion changes; only its operational actor
was adapted. It checks every frozen file, record, YAML field/container location,
binding, raw byte/hash and selected/historical revision closure, and performs two
canonical transformations/publications. Its fresh output matches the frozen draft.

All current parent, prior checkpoint, independent reviewer and accepted foundation
versions are preserved by exact SHA256 mappings in preservation.json. The previous
identity.py bytes have an explicit baseline copy. Original source schema/validator,
approved export profile, input snapshots and accepted imports are unchanged.

The product remains structural-draft. Missing sources, unresolved references,
mixed-edition uncertainty and blocking opaque aspects remain. Technical delivery
does not grant source coverage, human semantic acceptance or executable readiness.
Independent re-review of these exact new bytes and coordinator acceptance/done are
pending. IG-1E is planned and cannot begin before those gates pass.
'''
with (RUN/'report.md').open('x', encoding='utf-8', newline='\n') as f: f.write(report)
products = {a['path'] for a in parent['artifacts'] if a['path'].startswith(('src/', 'tests/'))}
products.add('tests/wgu_adapter/test_lineage_contract_repairs.py')
paths = {Path(p) for p in products}
paths.update(p for p in RUN.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths.update(p for p in checkroot.glob('*') if p.is_file())
task = next(t for t in q['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'in_progress'
write('delivery.json', {'role': 'executor', 'actor': 'ig1-continuation-executor-20261013', 'task': 'IG-1D',
                       'summary': 'Second and final bounded R04 repair rejects incompatible named typed-child contracts before replacement allocation; all strict controls and full-input accounting/reproducibility pass. Independent re-review pending.',
                       'criteria': task['acceptance'], 'artifacts': [art(p) for p in sorted(paths)],
                       'checks': checks, 'model': 'gpt-6.1-sol', 'reasoning': 'high',
                       'configuration_evidence': read(RUN/'checkpoint.json')['configuration_evidence'],
                       'input_packet': read(RUN/'checkpoint.json')['input_packet'],
                       'parent_delivery': scope['parent_delivery'], 'independent_parent_review': scope['independent_review'],
                       'repair_cycles': {'IG1D-R01': 1, 'IG1D-R02': 1, 'IG1D-R03': 1, 'IG1D-R04': 2},
                       'semantic_acceptance_granted': False, 'publisher_source_coverage_granted': False,
                       'executable_readiness_granted': False})
print(json.dumps({'delivery': art(RUN/'delivery.json'), 'artifacts': len(paths),
                  'preserved_parent_versions': len(rows), 'preserved_foundations': len(foundations)}))
