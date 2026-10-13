"""Verify faithful recording of the human's two decisions and preserved history."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def resolve(x,pointer):
    for key in pointer.lstrip('/').split('/'):
        key=key.replace('~1','/').replace('~0','~');x=x[int(key)] if isinstance(x,list) else x[key]
    return x
d=load(R/'owner-decision-06.json');o=load(R/'owner-review-overlay-06.json');old=load(R/'owner-review-overlay-05.json');s=load(R/'current-state-13.json');prior=load(R/'current-state-12.json')
c=load(R/'part-04b2/comparisons.json');pres=load(R/'part-04b2/presentation.json');byid={row['id']:row for row in c['relationships']}
assert d['owner_reply_verbatim']=='zatwierdxam'
assert len(d['recommendations'])==2 and [r['occurrences'] for r in d['recommendations']]==[52,8]
assert [row['id'] for row in d['scopes']]==[row['id'] for row in c['relationships']]
assert len(d['scopes'])==30 and d['newly_decided_assigned_occurrences']==60
assert len([row for row in d['scopes'] if row['owner_recommendation_number']==1])==26
special=pres['separate_issue']['ids'];count=0;fields=0;endpoints=0
for run,a in d['responses'].items():
    assert ref(ROOT/a['path'])==a
    raw=(ROOT/a['path']).read_bytes();parsed=json.loads(raw)
    for row in d['scopes']:
        base=byid[row['id']]
        for key in ['source_scope','target_scope','source_evidence','bounded_independent_source','necessity_and_missing_impact']:
            assert row[key]==base[key]
        assert row['whole_record_accepted'] is False and row['full_dependent_result_accepted'] is False
        assert (row['id'] in special)==('SEM_017_assessment' in row)
        if row['id'] in special:
            assert row['owner_recommendation_number']==2 and not row['SEM_017_assessment']['automatic_FP_award']
        x=row['runs'][run];t=x['edge_trace'];assert t==base['runs'][run]['output_trace'][row['id']]
        def check(span,value,pointer):
            b=raw[span['start_byte']:span['end_byte_exclusive']]
            assert hashlib.sha256(b).hexdigest()==span['sha256'] and json.loads(b)==value and resolve(parsed,pointer)==value
        check(t['raw_span'],t['original_record'],t['pointer']);count+=1
        for f in t['fields'].values():check(f['raw_span'],f['original_value'],f['pointer']);fields+=1
        for rid,q in x['endpoint_traces'].items():
            original=base['runs'][run]['output_trace'][rid]
            check(q['raw_span'],original['original_record'],q['pointer']);endpoints+=1
    previous=old['runs'][run];current=o['runs'][run]
    assert current['relationship_scopes'][:len(previous['relationship_scopes'])]==previous['relationship_scopes']
    assert len(current['relationship_scopes'])==(90 if run=='first-001' else 95)
    assert current['pending_relation_occurrences_4b2']==0 and current['remaining_without_owner_relation_scope']==36
    for key in ['scopes','context_requirements','accepted_scoped_groups','reviewed_context_groups']:
        assert current[key]==previous[key]
for key in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_locator_review']:
    assert o[key]==old[key]
assert o['relation_facet_decisions'][:len(old['relation_facet_decisions'])]==old['relation_facet_decisions']
assert len(o['category_units'])==264 and len(s['pending_expectation_ids'])==8
assert s['unresolved_issue_ids']==prior['inherited_issue_ids'] and 'SEM-017' not in s['unresolved_issue_ids']
for key in ['SEM-004','SEM-014','SEM-015','SEM-016']:assert s['issue_dispositions'][key]==prior['issue_dispositions'][key]
assert s['issue_dispositions']['SEM-017'].startswith('Resolved only')
assert s['owner_decided_assigned_relationship_occurrences']==185 and s['owner_pending_relationship_occurrences']==72
assert s['remaining_uncompared_relationship_occurrences']==72 and s['owner_pending_relationship_occurrences_4b2']==0
assert s['next_part']=='M-POC5A.4b3' and s['part_4b2_owner_review_complete'] and not s['M_POC5A_closed'] and not s['M_POC5A_4b_closed']
start=load(M/'start.json');changed=[a['path'] for a in start['protected'] if not (ROOT/a['path']).exists() or ref(ROOT/a['path'])!=a];assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',owner_reply_verbatim=d['owner_reply_verbatim'],recommendations=2,assigned_scopes_verified=count,edge_fields_verified=fields,
    related_record_spans_verified=endpoints,positive_scopes=52,qualified_exception_scopes=8,prior_125_scopes_unchanged=True,
    prior_264_category_units_and_8_expectations_unchanged=True,remaining_SEM_004_and_prior_pending_unchanged=True,
    SEM_017_resolved_only_in_presented_scope=True,no_whole_record_acceptance_or_metrics=True,protected_files_preserved=len(start['protected']))
assert not (M/'validation.json').exists()
(M/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
