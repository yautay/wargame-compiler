"""One-off evidence consistency audit, not semantic tests or inference."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
M = Path(__file__).resolve().parent
C = json.loads((P / 'reviews/semantic-01/checklist.json').read_bytes())
I = json.loads((P / 'reviews/semantic-01/issues.json').read_bytes())
start = json.loads((M / 'start.json').read_bytes())

def load(path):
    return json.loads((P / path).read_bytes())

def digest(data):
    return hashlib.sha256(data).hexdigest()

def resolve(obj, pointer):
    for key in pointer.lstrip('/').split('/') if pointer else []:
        key = key.replace('~1', '/').replace('~0', '~')
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj

exp = load('evaluation/eval-v1/expectations.json')['expectations']
inv = load('evaluation/eval-v1/inventory.json')['items']
policy = load('evaluation/eval-v1/measurement-policy.json')
deps = load('evaluation/eval-v1/dependencies.json')
assert C['evaluation']['sha256'] == digest((P / 'evaluation/eval-v1/manifest.json').read_bytes())
assert {r['id'] for r in C['expectations']} == {r['id'] for r in exp}
assert {r['id'] for r in C['inventory']} == {r['id'] for r in inv}
assert len(C['expectations']) == 74 and len(C['inventory']) == 207
assert Counter(r['assigned_part'] for r in C['expectations']) == {'M-POC5A.2':25, 'M-POC5A.3':25, 'M-POC5A.4':24}
assert {r['id'] for r in C['category_units']} == {u['id'] for c in policy['categories'] for u in c['units']}
assert len(C['category_units']) == 277
assert len(C['frozen_relations']) == 127
assert sum(r['gold'] for r in C['frozen_relations']) == 8
assert sum(r['category'] == 'unconfirmed_execution_candidates' for r in C['frozen_relations']) == 105
assert C['human_decisions'] == [] and C['reviewer'] is None
assert C['semantic_acceptance'] == 'not_performed'

for row, frozen in zip(C['expectations'], exp):
    assert row['id'] == frozen['id']
    assert row['source_scope'] == frozen['reviewed_scope']
    assert row['source_evidence'] == frozen['evidence']
    assert row['criticality'] == frozen['criticality']
    assert row['exclusions'] == frozen['unreviewed_fields']
for row, frozen in zip(C['inventory'], inv):
    assert row['frozen_item'] == frozen

run_checks = []
for run, response in C['responses'].items():
    data = (ROOT / response['path']).read_bytes()
    assert digest(data) == response['sha256'] and len(data) == response['bytes']
    original = json.loads(data)
    for rid, r in C['output_records'][run].items():
        assert resolve(original, r['pointer']) == r['original_record']
        assert r['original_record']['id'] == rid
        span = r['raw_span']
        fragment = data[span['start_byte']:span['end_byte_exclusive']]
        assert digest(fragment) == span['sha256']
        assert json.loads(fragment) == r['original_record']
    for group in ['expectations','inventory','category_units']:
        for row in C[group]:
            result = row['runs'][run]
            assert result['status'] == 'pending' and result['result'] == 'not_assessable'
            assert result['reviewer'] is None and result['response'] == response
            assert set(result['output_record_ids']) <= C['output_records'][run].keys()
    assert {e['id'] for e in C['output_edges'][run]} == {e['id'] for e in original['dependencies']}
    assert len(C['output_edges'][run]) == len(original['dependencies'])
    assert all(e['status'] == 'pending' and e['reviewer'] is None for e in C['output_edges'][run])
    assert I['inherited_observations'][run] == load(f'reports/{run}/errors.json')['errors']
    statuses = Counter(r['inherited_locator_observation']['quote_in_area_status'] for r in C['locator_review'][run])
    assert statuses == {'boundary_clipping_pending_review': 58 if run == 'first-001' else 64, 'failed':1}
    run_checks.append(dict(run=run, records=len(C['output_records'][run]), edges=len(C['output_edges'][run]),
        locator_statuses=dict(statuses), accepted_groups=0, semantic_TP_FP_FN='not_assessable'))

for issue in I['issues']:
    assert all(k in issue for k in ['id','classes','criticality','proposal','impact','uncertainty','limits','status',
        'preparer','human_reviewer','response_refs','evaluation_manifest','output_trace'])
    assert issue['status'] == 'pending' and issue['human_reviewer'] is None
    for run, trace in issue['output_trace'].items():
        for rid, record in trace.items():
            assert record == C['output_records'][run][rid]

for f in start['protected']:
    data = (ROOT / f['path']).read_bytes()
    assert len(data) == f['bytes'] and digest(data) == f['sha256'], f['path']
before = start['sessions_before']
sessions = (P / 'measurement/sessions.jsonl').read_bytes()
assert digest(sessions[:before['bytes']]) == before['sha256']
result = dict(status='passed', protected_files=len(start['protected']), sessions_original_prefix_preserved=True,
    expectations=74, inventory=207, diagnostic_rubric_units=277, frozen_relation_records=127,
    runs=run_checks, owner_decisions=0, limitations='Consistency audit only; no meaning acceptance.')
assert not (M / 'docket-validation.json').exists()
(M / 'docket-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
