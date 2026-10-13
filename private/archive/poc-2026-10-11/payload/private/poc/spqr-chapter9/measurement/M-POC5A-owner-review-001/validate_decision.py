"""Validate scope, lineage and byte preservation of the owner decision."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01'
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def resolve(obj,pointer):
    for k in pointer.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    return obj

start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
C=load(REV/'checklist.json');D=load(REV/'part-02/comparisons.json')
decision=load(REV/'owner-decision-01.json');overlay=load(REV/'owner-review-overlay-01.json')
expected={f'EXP-{n:03}' for n in list(range(1,10))+list(range(11,17))+[18]+list(range(20,26))}
assert decision['owner_reply']=='akceptuję'
assert {r['id'] for r in decision['scopes']}==expected and len(decision['scopes'])==22
assert decision['M_POC5A_closed'] is False
assert decision['owner_opened_report_or_images']=='unknown'
assert decision['evaluation']==C['evaluation'] and decision['responses']==C['responses']
for r in list(decision['responses'].values())+[decision['evaluation'],decision['source']]:assert ref(ROOT/r['path'])==r
for scope in decision['scopes']:
    original=next(e for e in D['expectations'] if e['id']==scope['id'])
    assert scope['reviewed_scope']==original['source_scope']
    assert scope['source_evidence']==original['source_evidence']
    assert scope['limits']==original['limits'] and scope['unreviewed_fields']==original['unreviewed_fields']
    assert scope['reviewer']==decision['reviewer'] and scope['status']=='reviewed'
    assert scope['whole_record_accepted'] is False
    for run,trace in scope['output_trace'].items():
        raw=(ROOT/decision['responses'][run]['path']).read_bytes();obj=json.loads(raw)
        for rid,t in trace.items():
            assert t['pointer']==original['runs'][run]['output_trace'][rid]['pointer']
            span=t['raw_span'];piece=raw[span['start_byte']:span['end_byte_exclusive']]
            assert hashlib.sha256(piece).hexdigest()==span['sha256']
            assert json.loads(piece)==resolve(obj,t['pointer'])
for run,r in overlay['runs'].items():
    assert r['accepted_scoped_groups']==22 and r['pending_content_groups']==44
    assert r['pending_context_groups']==8 and r['reviewed_context_groups']==0
    assert r['complete_rule_quality']=='not_assessable' and r['semantic_TP_FP_FN']=='not_assessable'
    assert {s['id'] for s in r['scopes']}==expected
    assert all(s['response']==C['responses'][run] for s in r['scopes'])
assert len(overlay['pending_expectation_ids'])==52
assert set(overlay['pending_expectation_ids']).isdisjoint(expected)
assert all(f'EXP-{n:03}' in overlay['pending_expectation_ids'] for n in [10,17,19,26,74])
assert len(overlay['category_units'])==85
assert len({r['id'] for r in overlay['category_units']})==85
assert all(r['expectation_id'] in expected and r['decision']==ref(REV/'owner-decision-01.json') for r in overlay['category_units'])
assert Counter(r['category'] for r in overlay['category_units'])==overlay['category_accepted_scope_counts']
assert overlay['category_full_denominators']==C['counts']['categories']
assert overlay['all_output_edges_review']=='pending' and overlay['all_locator_review']=='unchanged'
assert 'SEM-009' in overlay['pending_prior_issue_ids']
assert next(r for r in decision['scopes'] if r['id']=='EXP-016')['locator_status']=='E916 confirmed failure preserved'
current=load(REV/'current-state-03.json')
assert current['decision']==ref(REV/'owner-decision-01.json')
assert current['overlay']==ref(REV/'owner-review-overlay-01.json')
assert current['M_POC5A_closed'] is False
for r in load(M/'decision-artifacts.json')['artifacts']:assert ref(ROOT/r['path'])==r
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(result='passed',owner_decisions=1,accepted_groups_per_answer=22,pending_expectations=52,
    scoped_category_units=85,protected_files=len(start['protected']),E916='unchanged_failure',
    SEM_009='pending_choice',responses_and_eval_unchanged=True,previous_sessions_unchanged=True,
    full_metrics='not_assessable',card='partial')
target=M/'validation.json';assert not target.exists();target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
