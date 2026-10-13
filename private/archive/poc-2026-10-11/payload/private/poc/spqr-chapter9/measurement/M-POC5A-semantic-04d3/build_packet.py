"""Bind manual semantic judgments to original values, byte spans and precise sources."""
from pathlib import Path
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';O=R/'part-04d3'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=load(R/'checklist.json');A=load(M/'annotations.json');assign=load(M/'scope-assignment.json');prior=load(R/'current-state-25.json');overlay=load(R/'owner-review-overlay-12.json');ids=assign['assigned_ids'];assert [x[0] for x in A['rows']]==ids
prov={r:load(P/f'proposals/{r}/provenance.json') for r in C['responses']};unique={r:set() for r in C['responses']};crops={x['id']:x for x in load(M/'graphic-source-crops.json')}
def trace(run,rid):
    x=C['output_records'][run][rid];fields={}
    def walk(v,pointer):
        assert pointer in prov[run]['json_value_spans'],pointer
        fields[pointer]=dict(pointer=pointer,raw_span=prov[run]['json_value_spans'][pointer],original_value=v)
        if isinstance(v,dict):
            for k,z in v.items():walk(z,pointer+'/'+k.replace('~','~0').replace('/','~1'))
        elif isinstance(v,list):
            for i,z in enumerate(v):walk(z,pointer+'/'+str(i))
    walk(x['original_record'],x['pointer'])
    return dict(response=C['responses'][run],pointer=x['pointer'],raw_span=x['raw_span'],original_record=x['original_record'],fields=fields)
def nested_gaps(v):
    if isinstance(v,dict):return v.get('gap_ids',[])+[g for k,z in v.items() if k!='gap_ids' for g in nested_gaps(z)]
    if isinstance(v,list):return [g for z in v for g in nested_gaps(z)]
    return []
O.mkdir(exist_ok=False);rows=[]
for iid,assessment,note in A['rows']:
    n,item=next((i,x) for i,x in enumerate(C['inventory']) if x['id']==iid);f=item['frozen_item'];sources=[]; joined='\n'.join(e.get('transcription','') for e in f['evidence']); child=f.get('source_transcription'); child_start=joined.find(child) if child is not None else None; assert child is None or child_start>=0; fragment_start=0
    for e in f['evidence']:
        fragment_text=e.get('transcription',''); a=fragment_start; z=a+len(fragment_text); fragment_start=z+1
        if child is not None:
            lo=max(a,child_start);hi=min(z,child_start+len(child))
            if lo>=hi:continue
            selected_literal=joined[lo:hi]
        else:selected_literal=fragment_text
        src=dict(evaluation_inventory=ref(P/'evaluation/eval-v1/inventory.json'),inventory_pointer=f'/items/{n}',original_evidence=e,source_visual=ref(P/e['render']),parent_mapping_not_child_certificate=True)
        if 'transcription' in e:
            helperpath=P/e['helper_file'];helper=helperpath.read_text(encoding='utf-8-sig');literal=selected_literal;begin=helper.find(literal);assert begin>=0,(iid,e['helper_file'])
            src.update(literal_scope=literal,helper=ref(helperpath),helper_character_range=[begin,begin+len(literal)],literal_scope_sha256=hashlib.sha256(literal.encode()).hexdigest(),scope_policy='Exact source_transcription child takes precedence over containing parent; intersections of ordered fragments only. Otherwise this exact inventory evidence passage.',joined_parent_character_range=[lo,hi] if child is not None else [a,z])
        else:
            assert iid in crops
            src.update(graphic_scope=crops[iid],scope_policy='Visible glyphs/orientation in exact supplied graphic crop; rating meanings and global map directions excluded')
        sources.append(src)
    row=dict(id=iid,inventory_type=item['type'],evaluation_pointer=f'/items/{n}',frozen_inventory_item=f,source_transcription_exact=child,joined_parent_transcription=joined,source_scopes=sources,manual_assessment=assessment,manual_comparison=note,reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',whole_record_accepted=False,original_response_modified=False,
        prior_expectation_ids=item['expectation_ids'],overlapping_parent_child_not_additional_rule_points=True,exclusions=A['exclusions'],runs={})
    for run in C['responses']:
        mapped=item['runs'][run]['output_record_ids'];traces=[trace(run,rid) for rid in mapped];unique[run].update(mapped)
        evidenceids=list(dict.fromkeys(eid for t in traces for eid in t['original_record']['evidence_ids']));evidences=[trace(run,eid) for eid in evidenceids]
        gapids=list(dict.fromkeys(g for t in traces for g in nested_gaps(t['original_record'])));gaps=[trace(run,gid) for gid in gapids]
        oldscopes=[dict(artifact=ref(R/'owner-review-overlay-12.json'),pointer=f'/runs/{run}/scopes/{j}',prior_scoped_decision=z,policy='Retain exact prior reviewed_scope, no duplicate point') for j,z in enumerate(overlay['runs'][run]['scopes']) if z['id'] in item['expectation_ids']]
        oldcontext=[dict(artifact=ref(R/'owner-review-overlay-12.json'),pointer=f'/runs/{run}/context_requirements/{j}',prior_scoped_decision=z) for j,z in enumerate(overlay['runs'][run]['context_requirements']) if z['id'] in item['expectation_ids']]
        if item['type']=='rule_label':fields=['original_label']
        elif item['type'] in ['clause_group','clause_text_span']:fields=['transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','unit_types']
        else:fields=['original_label','content','source_locator']
        fieldrefs=[dict(pointer=t['pointer']+'/'+key,scope='Only feature of this exact inventory source described in manual comparison; not all values of containing field') for t in traces for key in fields if key in t['original_record']]
        row['runs'][run]=dict(response=C['responses'][run],status='waiting_review',evaluator_compared=True,reviewer=A['reviewer'],human_reviewer=None,owner_decision=None,bounded_result=assessment,comparison=note,output_traces=traces,evidence_traces=evidences,gap_traces=gaps,selected_output_fields=fieldrefs,source_scopes=sources,
            original_mapping=item['runs'][run]['structural_mapping'],mapping_not_semantic_proof=True,prior_local_scopes=oldscopes,prior_context_requirements=oldcontext,whole_record_accepted=False,exclusions=A['exclusions'],uncertainties=['Complete execution depends on unavailable base procedures/tables/setup','Prior unresolved meanings retained','Source glyphs do not establish rating-position meanings'])
    vals=[[t['original_record'] for t in row['runs'][run]['output_traces']] for run in C['responses']];row['mapped_records_equal_between_runs']=vals[0]==vals[1]
    row['between_run_difference']='R932 after context adds suppliedRouted exception and AS/LC scope, retains unknown order/full result; local half/floor unchanged.' if 'R932' in mapped else ('R962 local node identical; context gap now explicitly targets10.13 and remains missing/blocking.' if 'R962' in mapped else 'Mapped record content identical; prior acceptance not broadened.')
    rows.append(row)
assert all(x['mapped_records_equal_between_runs']==(x['id'] not in ['R-9.32','C-9.32-01']) for x in rows)
summary=dict(distinct_inventory_ids=59,assigned_inventory_occurrences=118,per_answer={'first-001':59,'context-01':59},evaluator_compared_occurrences=118,owner_available_occurrences=118,new_owner_reviewed_occurrences=0,owner_pending_occurrences=118,
    bounded_supported_inventory_occurrences=114,mixed_parent_occurrences=2,explanatory_child_omission_occurrences=2,underlying_omitted_explanatory_clauses_per_answer=1,facet_occurrences_by_inventory_type={k:v*2 for k,v in Counter(x['inventory_type'] for x in rows).items()},unique_mapped_records_per_answer={r:len(v) for r,v in unique.items()},
    prior_owner_inventory_scopes=214,total_inventory_evaluator_compared_assigned_occurrences=332,remaining_assigned_inventory_ids=41,remaining_assigned_inventory_occurrences=82,all_inventory_ids=207,
    prior_owner_relation_scopes=257,prior_owner_locator_scopes=124,prior_category_units=264,previous_pending_expectation_ids=prior['pending_expectation_ids'],previous_unresolved_issue_ids=prior['unresolved_issue_ids'],new_issue_ids=['SEM-021'],TP_FP_FN_precision_recall='not_assessable',actual_owner_file_open_or_read='unknown',count_policy=A['scope_policy'])
c=dict(id='M-POC5A.4d3-comparisons-01',card='M-POC5A.4d3',status='partial_waiting_review',source=C['source'],evaluation=C['evaluation'],responses=C['responses'],previous_state=ref(R/'current-state-25.json'),owner_decision=ref(R/'owner-decision-12.json'),owner_overlay=ref(R/'owner-review-overlay-12.json'),scope_plan=assign['original_before_review_plan'],scope_assignment=ref(M/'scope-assignment.json'),estimate=ref(M/'start.json'),manual_annotations=ref(M/'annotations.json'),method=A['method'],scope_policy=A['scope_policy'],summary=summary,inventory=rows,
    visual_source_pages_manually_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in range(34,36)],graphic_source_crops=ref(M/'graphic-source-crops.json'),graphic_views_manually_inspected=[z['readability_zoom'] for z in crops.values()],prior_issue_dispositions=prior['issue_dispositions'],prior_issues_retained=True,new_sources=0,new_extractions=0,new_corrections=0,new_owner_decisions=[],limits=C['limits'],limitations=C['limitations'],other_parts_executed=False)
save(O/'comparisons.json',c)
omission=next(x for x in rows if x['id']=='C-9.7-01-S2'); parent=next(x for x in rows if x['id']=='C-9.7-01')
issue=dict(id='SEM-021',issue_class='explanatory_clause_omission',criticality='noncritical_in_observed_historical_explanation; no wrong game result demonstrated',inventory_ids=['C-9.7-01','C-9.7-01-S2'],source_scopes=omission['source_scopes'],source_statement=omission['source_transcription_exact'],runs=omission['runs'],affected_parent_runs=parent['runs'],difference='Historical explanation of Roman use/doctrine as unassailable dogma absent from mapped textual record and short quote; attached original source image retains full paragraph. Operative applicability/Cannae retained.',proposal='Accept limited explanatory-text omission in two original responses; parent and child reflect same omission, no automatic FN or operational rule change.',status='waiting_review',human_reviewer=None)
save(O/'issues.json',dict(inherited_pending=prior['unresolved_issue_ids'],prior_dispositions_preserved=prior['issue_dispositions'],new_issues=[issue],older_pending_unchanged=True,no_automatic_semantic_FP_FN=True,
    bounded_observations=['Label not whole rule','Conditional meanings distributed across action/conditions/exceptions; standalone action string not complete rule','Literal counter glyphs supported; rating meanings unknown','Physical continuation nodes delegate content to original owning node','R932 added bounded context does not resolve AS/LC order;R962 allocation stillmissing' , 'Diagram exact tracking of top/bottom counter identities across panels not certified'],
    preserved_pending_components=[dict(id=iid,assessment=next(r['manual_comparison'] for r in rows if r['id']==iid)) for iid in ['C-9.32-01','C-9.53-08','C-9.71-01','C-9.72-01','D-02']]))
save(O/'presentation.json',dict(card='M-POC5A.4d3',summary=summary,decisions=[dict(number=1,ids=[i for i in ids if i not in ['C-9.7-01','C-9.7-01-S2']],occurrences=114,proposal='Accept114 exact bounded label/clause/child/graphic/caption/physical-continuation facets, with older unresolved and complete execution excluded.'),dict(number=2,ids=['C-9.7-01','C-9.7-01-S2'],occurrences=4,proposal='Accept mixedparent2 and omittedexplanatorychild2 as SEM-021: one underlying historical explanation omitted per answer, not four independent errors. Operative text retained; attached image retains source. No repair/FN/game rule.'),dict(number=3,ids=['C-9.32-01','C-9.53-08','C-9.71-01','C-9.72-01','D-02'],proposal='Overlapping exclusions preserve older AS/LC, DD elimination, Triarii gate-combination and actual rating-source uncertainties. No variant selected.')],count_policy='114+2mixedparent+2omittedchild=118 occurrence judgments; one explanatory omission per answer, parent/child not extra errors or points.',excludes=A['exclusions'],actual_owner_file_open_or_read='unknown',proposal_only=True,next_after_owner_decision='Separate.4d4 41 IDs82occurrences after refreshed estimate; then.4d5 reconciliation andseparateM-POC5B.'))
lines=['# M-POC5A.4d3 — 59 pozycji / 118 rzeczywistych porównań','',A['method'],'',A['scope_policy'],'','[Decyzje po ludzku](owner-focus.md) · [Pełne ślady](comparisons.json)','']
for row in rows:
    lines += [f"## {row['id']} — {row['inventory_type']}",'',row['manual_comparison'],'',f"Wynik: {row['manual_assessment']}; oba warianty ocenione, owner waiting_review, cały rekord nieprzyjęty.",'']
    for src in row['source_scopes']:
        if 'literal_scope' in src:
            lines += ['Dokładny fragment źródła:','', '> '+src['literal_scope'].replace('\n','\n> '),'',f"PDF{src['original_evidence']['pdf_page']}, `{src['helper']['path']}`, znaki{src['helper_character_range']}, hash`{src['literal_scope_sha256']}`.",'']
        else:lines += [f"Dokładny obraz: [{row['id']} source crop]({(ROOT/src['graphic_scope']['exact_crop']['path']).as_posix()}), bboxPDF{src['original_evidence']['bbox_pdf_points']}; pełne hashe i prawdziwa ścieżka wJSON.",'']
    for run,x in row['runs'].items():
        lines += [f"**{run}:** {x['bounded_result']}; {x['comparison']}",'']
        for t in x['output_traces']:
            b=t['raw_span'];lines += [f"`{t['original_record']['id']}` pointer`{t['pointer']}`, bytes[{b['start_byte']},{b['end_byte_exclusive']}), hash`{b['sha256']}`.",'',json.dumps(t['original_record'],ensure_ascii=False),'']
        lines += ['Dawne zakresy:'+','.join(z['prior_scoped_decision']['id'] for z in x['prior_local_scopes']+x['prior_context_requirements'])+'; nie dodają nowych punktów.','']
    lines += ['Wyłączenia: '+'; '.join(A['exclusions'])+'.','']
lines += ['## Pokrycie','',json.dumps(summary,ensure_ascii=False),'','Pozostałe41pozycji w.4d4; następnie osobna.4d5 rozliczenie i osobneM-POC5B20sytuacji. Oryginały/dawne decyzje/gold zachowane, metryki pełne nieocenialne.','']
(O/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(O/'review.md').write_text('# M-POC5A.4d3 — przegląd wykonany\n\n'+A['method']+'\n\n'+A['scope_policy']+'\n\n[Porównania](comparisons.md) · [Ślady](comparisons.json) · [Decyzje](owner-focus.md)\n\n'+lines[-2]+'\n',encoding='utf-8')
save(M/'packet-summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
