"""Validate coverage, original-byte traces and immutable history, not meaning."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04b3'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def resolve(x,pointer):
    for k in pointer.lstrip('/').split('/') if pointer else []:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
c=load(OUT/'comparisons.json');a=load(M/'annotations.json');mf=load(OUT/'manifest.json');s=load(R/'current-state-14.json');old=load(R/'current-state-13.json')
plan=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json');pres=load(OUT/'presentation.json');issues=load(OUT/'issues.json')
assigned=plan['parts'][2]['output_edge_ids'];assert [x['id'] for x in c['relationships']]==assigned
assert len(c['relationships'])==36 and c['summary']['assigned_occurrences']==72
for artifact in [c['source'],c['evaluation'],*c['responses'].values(),*mf['artifacts'],mf['manual_annotations'],mf['estimate'],c['previous_state'],c['owner_decision'],c['owner_overlay']]:assert ref(ROOT/artifact['path'])==artifact
raws={r:(ROOT/x['path']).read_bytes() for r,x in c['responses'].items()};parsed={r:json.loads(b) for r,b in raws.items()}
helper=load(P/'inputs/v1/helper-regions.json');inv=load(P/'evaluation/eval-v1/inventory.json')
edges=records=fields=blocks=items=nonblocking=partial=0
for row,note in zip(c['relationships'],a['rows']):
    assert row['source_scope']==note[3] and row['target_scope']==note[4] and row['necessity_and_missing_impact']==note[5] and row['proposal']==note[6] and row['separate_issue']==note[7]
    assert row['target_source_actual'] is None and row['human_reviewer'] is None and row['human_status']=='waiting_review'
    for b in row['bounded_independent_source']:
        assert ref(ROOT/b['artifact']['path'])==b['artifact'] and ref(ROOT/b['image']['path'])==b['image']
        text=resolve(helper,b['pointer']);start,end=b['character_range'];assert text[start:end]==b['literal_helper_text'] and sha(text[start:end].encode())==b['utf8_excerpt_sha256'];blocks+=1
        assert b['pdf_page'] in [31,34,35,36,37]
    for i in row['source_evidence']:
        assert ref(ROOT/i['artifact']['path'])==i['artifact'];item=resolve(inv,i['pointer'])
        assert item['id']==i['inventory_id'] and item['evidence']==i['exact_child_evidence'];items+=1
    for run,x in row['runs'].items():
        assert x['evaluator_compared'] and x['status']=='waiting_review' and x['human_reviewer'] is None and x['meaning_result']=='not_assessable'
        for rid,t in x['output_trace'].items():
            assert t['response']==c['responses'][run];sp=t['raw_span'];b=raws[run][sp['start_byte']:sp['end_byte_exclusive']]
            assert sha(b)==sp['sha256'] and json.loads(b)==t['original_record'] and resolve(parsed[run],t['pointer'])==t['original_record'];records+=1
            for f in t['fields'].values():
                sp=f['raw_span'];b=raws[run][sp['start_byte']:sp['end_byte_exclusive']]
                assert sha(b)==sp['sha256'] and json.loads(b)==f['original_value'] and resolve(parsed[run],f['pointer'])==f['original_value'];fields+=1
        e=x['output_trace'][row['id']]['original_record'];assert e['to'] is None and e['gap_ids']
        assert x['kind']['observed']==e['kind'] and x['explicitness']['observed']==e['explicitness'] and x['missing_target_impact']['observed']==e['impact_if_missing'];edges+=1
        if e['impact_if_missing']['blocks_full_result'] is False:
            assert row['id'] in ['D996supply','D996tables'];nonblocking+=1
        if row['id']=='D961stack':
            assert x['historical_kind_decision_unchanged'] and 'already owner-decided' in x['kind']['assessment'] and row['historical_component_decision']==ref(R/'owner-decision-05.json')
        for b in x['supplemental_supplied_context']:
            assert ref(ROOT/b['artifact']['path'])==b['artifact'] and ref(ROOT/b['image']['path'])==b['image'];partial+=1
    f=row['runs']['first-001']['output_trace'][row['id']]['original_record'];g=row['runs']['context-01']['output_trace'][row['id']]['original_record']
    assert row['output_values_identical_between_runs'] and f==g
    assert row['assigned_gap_values_identical_between_runs']
    for gid in f['gap_ids']:assert row['runs']['first-001']['output_trace'][gid]['original_record']==row['runs']['context-01']['output_trace'][gid]['original_record']
assert edges==72 and nonblocking==4 and partial==8
positive=pres['positive_scope']['ids'];separate=[i for x in pres['separate_issues'] for i in x['ids']]
assert len(positive)==34 and separate==['D951terrain','D961stack'] and not set(positive)&set(separate) and set(positive+separate)==set(assigned)
assert pres['positive_scope']['occurrences']==68 and sum(x['occurrences'] for x in pres['separate_issues'])==4
assert pres['new_owner_reviewed_occurrences']==0 and pres['owner_pending_occurrences']==72
assert [x['id'] for x in issues['issues']]==['SEM-018','SEM-019'] and issues['inherited_pending']==old['unresolved_issue_ids']
for key in ['decision','overlay','expectation_owner_decision','owner_accepted_relationship_occurrences','owner_pending_relationship_occurrences',
            'pending_expectation_ids','pending_local_ids','pending_context_ids','owner_accepted_local_groups_per_answer','reviewed_context_requirements_per_answer','issue_dispositions','extra_frozen_mention_decided_occurrences']:
    assert s[key]==old[key],key
assert s['evaluator_compared_relationship_occurrences']==257 and s['remaining_uncompared_relationship_occurrences']==0 and s['owner_accepted_relationship_occurrences']==185
assert s['new_owner_decisions']==[] and not s['M_POC5A_closed'] and not s['M_POC5A_4b_closed'] and s['full_relation_record_review_incomplete']
assert s['unresolved_issue_ids']==old['unresolved_issue_ids']+['SEM-018','SEM-019'] and s['next_part']=='M-POC5A.4c' and not s['part_4b3_owner_review_complete']
start=load(M/'start.json');changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',assigned_occurrences_verified=edges,output_records_verified=records,output_fields_verified=fields,independent_source_blocks_verified=blocks,
    inventory_crosswalk_items_verified=items,partial_previously_supplied_framework_blocks_verified=partial,local_nonblocking_exclusion_occurrences=nonblocking,
    all36_ids_separately_traced_both_original_answers=True,disjoint_positive68_separate4=True,exact_original_pointers_raw_spans_values=True,
    previous_kind_decision_not_reasked=True,previous_owner_scopes_and_pending_preserved=True,no_automatic_gold_semantic_acceptance=True,
    protected_files_preserved=len(start['protected']),previous_sessions_unchanged_before_append=True)
assert not (M/'validation.json').exists();(M/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
