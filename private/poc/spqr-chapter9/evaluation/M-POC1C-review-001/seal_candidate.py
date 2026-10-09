"""Validate and seal the incomplete candidate, without authorizing eval freeze."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
P = ROOT / 'private/poc/spqr-chapter9'
C = P / 'evaluation/eval-v1-candidate-20261008-02'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ref(path):
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha, 'bytes': path.stat().st_size}


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


e = load(C / 'expectations.json')
d = load(C / 'dependencies.json')
s = load(C / 'situations.json')
i = load(C / 'inventory.json')
old = load(P / 'evaluation/eval-v1-candidate-20261008-01/manifest.json')
assert len(i['items']) == 207
assert len({row['id'] for row in i['items']}) == 207
assert {row['id'] for row in e['expectations']} == {f'EXP-{n:03}' for n in range(1,75)}
assert Counter(row['classification'] for row in e['expectations']) == {'confirmed_local_content_scope':66,'requires_context':8}
assert len({row['scoring_unit'] for row in e['expectations'] if row['scoring_unit']}) == 66
assert len({row['context_requirement_unit'] for row in e['expectations'] if row['context_requirement_unit']}) == 8
assert len(d['confirmed_execution_relations']) == 3
assert all(row['explicitness'] == 'implicit' for row in d['confirmed_execution_relations'])
assert len({(row['from'],row['to'],row['kind'],row['explicitness']) for row in d['confirmed_execution_relations']}) == 3
assert all(row['from'] in {it['id'] for it in i['items']} and row['to'] in {it['id'] for it in i['items']} for row in d['confirmed_execution_relations'])
assert len(d['mentions']) == 7 and all(not row['executable'] for row in d['mentions'])
assert len(d['continuations']) == 7 and all(not row['execution_gold'] for row in d['continuations'])
assert len(d['unconfirmed_execution_candidates']) == 110
assert len({row['id'] for row in [*d['confirmed_execution_relations'],*d['unconfirmed_execution_candidates'],*d['mentions'],*d['continuations']]}) == 127
assert Counter(row['explicitness_proposal'] for row in d['unconfirmed_execution_candidates']) == {'explicit':99,'implicit':11}
assert {row['id'] for row in s['situations']} == {f'SIT-{n:02}' for n in range(1,21)}
assert Counter(row['expected']['kind'] for row in s['situations']) == {'local_result':17,'justified_block':3}
assert all(row['authorizing_decision'] and row['overlay_provenance'] and row['evidence'] for row in s['situations'])
assert all(not row['whole_parent_record_accepted'] for row in e['expectations'])
assert all(not it['candidate_review']['scoring_eligible'] for it in i['items'])
assert not (P / 'evaluation/eval-v1').exists()
assert not (P / 'evaluation/freeze-public-v1.json').exists()

for item in [*old['artifacts'],*old['parents']]:
    assert ref(ROOT / item['path']) == item, item

baseline = load(HERE / 'baseline.json')
allowed = set(baseline['allowed_public_updates'])
protected = []
intentional = []
for item in baseline['files']:
    actual = ref(ROOT / item['path'])
    if actual != item:
        assert item['path'] in allowed, (item, actual)
        intentional.append({'before':item,'after':actual})
    else:
        protected.append(actual)

now = datetime.now(timezone.utc).isoformat()
save(HERE / 'validation.json', {
    'recorded_at_utc':now, 'card':'M-POC1C', 'result':'passed technical checks; incomplete semantic review',
    'validated_counts':{'inventory':207,'expectation_ids':74,'content_groups_proposed':66,'context_groups':8,
                        'situations':20,'local_results':17,'blocks':3,'implicit_relations':3,'explicit_relations':0,
                        'mentions':7,'physical_continuations':7,'unconfirmed_execution':110},
    'prior_candidate_preserved':True, 'baseline_files_checked':len(baseline['files']),
    'unchanged_files':len(protected), 'intentional_public_updates':intentional,
    'preserved_sha256_records':protected, 'semantic_acceptance_inferred_from_checks':False,
    'freeze_ready':False, 'new_owner_decisions':[],
})
save(C / 'manifest.json', {
    'id':C.name, 'card':'M-POC1C', 'status':'incomplete_waiting_review',
    'recorded_at_utc':now, 'frozen':False, 'gold':False, 'freeze_authorized':False,
    'owner_freeze_response':None, 'new_owner_semantic_decisions':[],
    'branch':'feature/tests', 'current_head_at_preparation':load(HERE / 'audit.json')['head'],
    'source':ref(P / 'source/original-pdf-20261008-01.pdf'),
    'artifacts':[ref(C / name) for name in ('inventory.json','expectations.json','dependencies.json','situations.json','change-map.json','review.md')],
    'provenance':[
        ref(P / 'evaluation/eval-v1-candidate-20261008-01/manifest.json'),
        ref(P / 'evaluation/owner-review-002/review-manifest-final-20261008.json'),
        ref(P / 'evaluation/owner-review-002/closure-seal-24.json'),
        ref(P / 'evaluation/owner-review-001/review-manifest.json'),
        ref(ROOT / 'docs/POC-PLAN.md'), ref(HERE / 'audit.json'), ref(HERE / 'pending-question.json'),
    ],
    'counts':{'reference_inventory':207,'local_content_scope_groups_proposed':66,'context_requirement_groups':8,
              'situations':20,'local_results':17,'blocks':3,'confirmed_explicit_execution':0,
              'confirmed_implicit_execution':3,'mentions_separate':7,'continuations_separate':7},
    'open_gates':['explicit execution relation tuple review','grouping and category rubrics','actual owner freeze decision'],
    'plan_thresholds_unchanged':True, 'plan_limits_unchanged':True,
    'quality_results':'n/a: no freeze and no extraction response',
    'forbidden_work_performed':[],
})
print(json.dumps({'manifest':ref(C / 'manifest.json'), 'baseline_checked':len(baseline['files']),
                  'unchanged_files':len(protected),'intentional_updates':[r['before']['path'] for r in intentional]},indent=2))
