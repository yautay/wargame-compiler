"""Validate coverage, pointers, hashes and source excerpts; no meaning approval."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
R=P/'reviews/semantic-01';OUT=R/'part-04b2'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def resolve(x,pointer):
    if pointer=='':return x
    for k in pointer.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
c=load(OUT/'comparisons.json');a=load(M/'annotations.json');manifest=load(OUT/'manifest.json');s=load(R/'current-state-12.json');old=load(R/'current-state-11.json')
plan=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json');pres=load(OUT/'presentation.json')
assert [x['id'] for x in c['relationships']]==plan['parts'][1]['output_edge_ids']
assert len(c['relationships'])==30 and c['summary']['assigned_occurrences']==60
for artifact in [c['source'],c['evaluation'],*c['responses'].values(),*manifest['artifacts']]:assert ref(ROOT/artifact['path'])==artifact
raws={run:(ROOT/x['path']).read_bytes() for run,x in c['responses'].items()};parsed={r:json.loads(b) for r,b in raws.items()}
helpers=load(P/'inputs/v1/helper-regions.json');inv=load(P/'evaluation/eval-v1/inventory.json')
edges=0;records=0;fields=0;source_blocks=0;inventory_items=0;supplemental=0
for row,note in zip(c['relationships'],a['rows']):
    assert row['source_scope']==note[3] and row['target_scope']==note[4] and row['proposal']==note[6]
    assert row['target_source_actual'] is None
    for b in row['bounded_independent_source']:
        assert ref(ROOT/b['artifact']['path'])==b['artifact'] and ref(ROOT/b['image']['path'])==b['image']
        text=resolve(helpers,b['pointer']);start,end=b['character_range']
        assert text[start:end]==b['literal_helper_text'] and sha(b['literal_helper_text'].encode('utf-8'))==b['utf8_excerpt_sha256'];source_blocks+=1
    for i in row['source_evidence']:
        assert ref(ROOT/i['artifact']['path'])==i['artifact']
        item=resolve(inv,i['pointer']);assert item['id']==i['inventory_id'] and item['evidence']==i['exact_child_evidence'];inventory_items+=1
    for run,x in row['runs'].items():
        assert x['evaluator_compared'] and x['status']=='waiting_review' and x['human_reviewer'] is None
        assert x['target_identity']['actual_target_content']=='not_supplied'
        for t in x['output_trace'].values():
            sp=t['raw_span'];b=raws[run][sp['start_byte']:sp['end_byte_exclusive']]
            assert sha(b)==sp['sha256'] and json.loads(b)==t['original_record'] and resolve(parsed[run],t['pointer'])==t['original_record'];records+=1
            for f in t['fields'].values():
                sp=f['raw_span'];b=raws[run][sp['start_byte']:sp['end_byte_exclusive']]
                assert sha(b)==sp['sha256'] and json.loads(b)==f['original_value'] and resolve(parsed[run],f['pointer'])==f['original_value'];fields+=1
        edge=x['output_trace'][row['id']]['original_record'];assert edge['to'] is None and edge['gap_ids'] and edge['impact_if_missing']['blocks_full_result'] is True;edges+=1
        assert x['kind']['observed']==edge['kind'] and x['explicitness']['observed']==edge['explicitness']
        assert x['missing_target_impact']['observed']==edge['impact_if_missing']
        for b in x['supplemental_supplied_context']:
            assert run=='context-01' and ref(ROOT/b['artifact']['path'])==b['artifact'] and ref(ROOT/b['image']['path'])==b['image']
            assert (ROOT/b['artifact']['path']).read_text(encoding='utf-8')==b['literal_helper_text'];supplemental+=1
    assert row['output_values_identical_between_runs']==(row['runs']['first-001']['output_trace'][row['id']]['original_record']==row['runs']['context-01']['output_trace'][row['id']]['original_record'])
assert edges==60 and supplemental==3
assert sum(x['output_values_identical_between_runs'] for x in c['relationships'])==29
positive=pres['positive_scope']['ids'];separate=pres['separate_issue']['ids']
assert len(positive)==26 and len(separate)==4 and not set(positive)&set(separate) and set(positive+separate)==set(plan['parts'][1]['output_edge_ids'])
assert pres['positive_scope']['occurrences']==52 and pres['separate_issue']['occurrences']==8
assert pres['new_owner_reviewed_occurrences']==0 and pres['owner_pending_occurrences']==60
for key in ['decision','overlay','expectation_owner_decision','owner_accepted_relationship_occurrences','owner_pending_relationship_occurrences',
            'pending_expectation_ids','owner_accepted_local_groups_per_answer','reviewed_context_requirements_per_answer','issue_dispositions']:
    assert s[key]==old[key]
assert s['evaluator_compared_relationship_occurrences']==185 and s['remaining_uncompared_relationship_occurrences']==72
assert s['new_owner_decisions']==[] and not s['M_POC5A_closed'] and not s['M_POC5A_4b_closed']
assert s['unresolved_issue_ids']==old['unresolved_issue_ids']+['SEM-017'] and s['next_part']=='M-POC5A.4b3'
start=load(M/'start.json');changed=[i['path'] for i in start['protected'] if not (ROOT/i['path']).exists() or ref(ROOT/i['path'])!=i]
assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',assigned_edges_verified=edges,output_records_verified=records,output_fields_verified=fields,
    independent_source_blocks_verified=source_blocks,inventory_crosswalk_items_verified=inventory_items,supplied_context_blocks_verified=supplemental,
    exact_original_pointers_raw_spans_and_values=True,all_30_ids_separately_compared_in_both_answers=True,disjoint_positive_52_separate_8=True,
    actual_target_content_not_supplied=True,no_automatic_gold_or_semantic_acceptance=True,previous_owner_scopes_pending_and_decisions_preserved=True,
    protected_files_preserved=len(start['protected']),previous_sessions_unchanged_before_append=True)
assert not (M/'validation.json').exists()
(M/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
