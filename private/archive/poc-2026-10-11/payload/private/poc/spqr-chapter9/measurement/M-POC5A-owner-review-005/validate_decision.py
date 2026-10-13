"""Check materialization against original byte spans, not mirrored semantic tests."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
d=load(R/'owner-decision-05.json');o=load(R/'owner-review-overlay-05.json');old=load(R/'owner-review-overlay-04.json');s=load(R/'current-state-11.json')
c=load(R/'part-04b1/comparisons.json');start=load(M/'start.json')
assert d['owner_reply_verbatim']=='zgodnie z rekomendacją'
assert [j['number'] for j in d['judgments']]==list(range(1,7))
assert {j['edge'] for j in d['judgments'] if not j['extra_frozen_scope']}==set(c['summary']['separate_issue_ids'])
fields=0;edges=0;assigned=0;extra=0
for j in d['judgments']:
    collection='frozen_tuple_comparisons' if j['extra_frozen_scope'] else 'relationships'
    row=next(x for x in c[collection] if x['id']==('DEP-037' if j['extra_frozen_scope'] else j['edge']))
    if not j['extra_frozen_scope']:
        for key in ['source_scope','target_scope','source_evidence','target_evidence','necessity_and_missing_impact']:
            assert j[key]==row[key]
    else:
        assert j['frozen_record']==row['frozen_record'] and j['evaluation_pointer']==row['evaluation_pointer']
    for run,x in j['runs'].items():
        a=x['response'];assert ref(ROOT/a['path'])==a
        raw=(ROOT/a['path']).read_bytes();parsed=json.loads(raw);t=x['trace']
        assert t==row['runs'][run]['output_trace'][j['edge']]
        def check(span,value,pointer):
            b=raw[span['start_byte']:span['end_byte_exclusive']]
            assert hashlib.sha256(b).hexdigest()==span['sha256'] and json.loads(b)==value
            found=parsed
            for key in pointer.strip('/').split('/'):
                key=key.replace('~1','/').replace('~0','~')
                found=found[int(key)] if isinstance(found,list) else found[key]
            assert found==value
        check(t['raw_span'],t['original_record'],t['pointer']);edges+=1
        for f in t['fields'].values():
            check(f['raw_span'],f['original_value'],f['pointer']);fields+=1
        for ep in x['endpoint_traces'].values():
            b=raw[ep['raw_span']['start_byte']:ep['raw_span']['end_byte_exclusive']]
            assert hashlib.sha256(b).hexdigest()==ep['raw_span']['sha256']
        assert not x['whole_record_accepted'] and not x['full_result_accepted']
        if j['extra_frozen_scope']:extra+=1
        else:assigned+=1
        for facet,bad in j['rejected_original_facets'].items():
            if facet=='impact_if_missing':
                assert x['original_impact']['blocks_full_result'] is False and not t['original_record']['gap_ids']
            else:assert t['original_record'][facet]==bad
assert (edges,assigned,extra)==(11,9,2)
for run,v in o['runs'].items():
    prior=old['runs'][run]
    for key in ['scopes','context_requirements','accepted_scoped_groups','reviewed_context_groups']:
        assert v[key]==prior[key]
    assert v['relationship_scopes'][:len(prior['relationship_scopes'])]==prior['relationship_scopes']
    assert len(v['relationship_scopes'])==(60 if run=='first-001' else 65)
    assert v['pending_relation_occurrences_4b1']==0
    assert v['remaining_without_owner_relation_scope']==66
for key in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_locator_review']:
    assert o[key]==old[key]
assert len(o['category_units'])==264 and len(o['pending_expectation_ids'])==8
assert s['remaining_uncompared_relationship_occurrences']==132 and s['owner_pending_relationship_occurrences']==132
assert s['owner_pending_relationship_occurrences_4b1']==0 and s['owner_accepted_relationship_occurrences']==125
assert s['unresolved_issue_ids']==[f'SEM-{n:03}' for n in range(1,14)]
assert s['issue_dispositions']['SEM-004'].startswith('partially resolved')
assert s['next_part']=='M-POC5A.4b2' and not s['M_POC5A_closed'] and not s['M_POC5A_4b_closed']
changed=[a['path'] for a in start['protected'] if not (ROOT/a['path']).exists() or ref(ROOT/a['path'])!=a]
assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
report=dict(status='passed',recommendations=6,assigned_occurrences_verified=assigned,extra_frozen_occurrences_verified=extra,
    original_edge_fields_verified=fields,original_pointer_and_byte_spans_verified=True,previous_116_scopes_and_264_units_unchanged=True,
    pending_expectations_unchanged=8,remaining_SEM_004_open=True,protected_files_preserved=len(start['protected']),
    semantics='Owner six decisions; verification checks faithful recording, no automatic whole-record correctness or final metrics.')
assert not (M/'validation.json').exists()
(M/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
