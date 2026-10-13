"""Bind manual semantic judgments to original values, byte spans and precise sources."""
from pathlib import Path
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';O=R/'part-04d2'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=load(R/'checklist.json');A=load(M/'annotations.json');assign=load(M/'scope-assignment.json');prior=load(R/'current-state-23.json');overlay=load(R/'owner-review-overlay-11.json');ids=assign['assigned_ids'];assert [x[0] for x in A['rows']]==ids
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
    n,item=next((i,x) for i,x in enumerate(C['inventory']) if x['id']==iid);f=item['frozen_item'];sources=[]
    for e in f['evidence']:
        src=dict(evaluation_inventory=ref(P/'evaluation/eval-v1/inventory.json'),inventory_pointer=f'/items/{n}',original_evidence=e,source_visual=ref(P/e['render']),parent_mapping_not_child_certificate=True)
        if 'transcription' in e:
            helperpath=P/e['helper_file'];helper=helperpath.read_text(encoding='utf-8-sig');literal=e['transcription'];begin=helper.find(literal);assert begin>=0,(iid,e['helper_file'])
            src.update(literal_scope=literal,helper=ref(helperpath),helper_character_range=[begin,begin+len(literal)],literal_scope_sha256=hashlib.sha256(literal.encode()).hexdigest(),scope_policy='Exact evidence passage belonging to this child/row or explicitly listed physical fragment; no parent-autoacceptance')
        else:
            assert iid in crops
            src.update(graphic_scope=crops[iid],scope_policy='Visible glyphs/orientation in exact supplied graphic crop; rating meanings and global map directions excluded')
        sources.append(src)
    row=dict(id=iid,inventory_type=item['type'],evaluation_pointer=f'/items/{n}',frozen_inventory_item=f,source_scopes=sources,manual_assessment=assessment,manual_comparison=note,reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',whole_record_accepted=False,original_response_modified=False,
        prior_expectation_ids=item['expectation_ids'],overlapping_parent_child_not_additional_rule_points=True,exclusions=A['exclusions'],runs={})
    for run in C['responses']:
        mapped=item['runs'][run]['output_record_ids'];traces=[trace(run,rid) for rid in mapped];unique[run].update(mapped)
        evidenceids=list(dict.fromkeys(eid for t in traces for eid in t['original_record']['evidence_ids']));evidences=[trace(run,eid) for eid in evidenceids]
        gapids=list(dict.fromkeys(g for t in traces for g in nested_gaps(t['original_record'])));gaps=[trace(run,gid) for gid in gapids]
        oldscopes=[dict(artifact=ref(R/'owner-review-overlay-11.json'),pointer=f'/runs/{run}/scopes/{j}',prior_scoped_decision=z,policy='Retain exact prior reviewed_scope, no duplicate point') for j,z in enumerate(overlay['runs'][run]['scopes']) if z['id'] in item['expectation_ids']]
        oldcontext=[dict(artifact=ref(R/'owner-review-overlay-11.json'),pointer=f'/runs/{run}/context_requirements/{j}',prior_scoped_decision=z) for j,z in enumerate(overlay['runs'][run]['context_requirements']) if z['id'] in item['expectation_ids']]
        if item['type']=='rule_label':fields=['original_label']
        elif item['type']=='clause_group':fields=['transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','unit_types']
        else:fields=['original_label','content','source_locator']
        fieldrefs=[dict(pointer=t['pointer']+'/'+key,scope='Only feature of this exact inventory source described in manual comparison; not all values of containing field') for t in traces for key in fields if key in t['original_record']]
        row['runs'][run]=dict(response=C['responses'][run],status='waiting_review',evaluator_compared=True,reviewer=A['reviewer'],human_reviewer=None,owner_decision=None,bounded_result=assessment,comparison=note,output_traces=traces,evidence_traces=evidences,gap_traces=gaps,selected_output_fields=fieldrefs,source_scopes=sources,
            original_mapping=item['runs'][run]['structural_mapping'],mapping_not_semantic_proof=True,prior_local_scopes=oldscopes,prior_context_requirements=oldcontext,whole_record_accepted=False,exclusions=A['exclusions'],uncertainties=['Complete execution depends on unavailable base procedures/tables/setup','Prior unresolved meanings retained','Source glyphs do not establish rating-position meanings'])
    vals=[[t['original_record'] for t in row['runs'][run]['output_traces']] for run in C['responses']];row['mapped_records_equal_between_runs']=vals[0]==vals[1]
    row['between_run_difference']='Mapped record content identical. Linked original gaps/evidence traced separately; context R923 base-Shock gap partially supplied, still blocking full result.' if 'R923' in mapped else 'Mapped record content identical; no transfer of broader prior acceptance.'
    rows.append(row)
assert all(x['mapped_records_equal_between_runs'] for x in rows)
summary=dict(distinct_inventory_ids=68,assigned_inventory_occurrences=136,per_answer={'first-001':68,'context-01':68},evaluator_compared_occurrences=136,owner_available_occurrences=136,new_owner_reviewed_occurrences=0,owner_pending_occurrences=136,
    bounded_supported_inventory_occurrences=136,facet_occurrences_by_inventory_type={k:v*2 for k,v in Counter(x['inventory_type'] for x in rows).items()},unique_mapped_records_per_answer={r:len(v) for r,v in unique.items()},
    prior_owner_inventory_scopes=78,total_inventory_evaluator_compared_assigned_occurrences=214,remaining_assigned_inventory_ids=100,remaining_assigned_inventory_occurrences=200,all_inventory_ids=207,
    prior_owner_relation_scopes=257,prior_owner_locator_scopes=124,prior_category_units=264,previous_pending_expectation_ids=prior['pending_expectation_ids'],previous_unresolved_issue_ids=prior['unresolved_issue_ids'],new_issue_ids=[],TP_FP_FN_precision_recall='not_assessable',actual_owner_file_open_or_read='unknown',count_policy=A['scope_policy'])
c=dict(id='M-POC5A.4d2-comparisons-01',card='M-POC5A.4d2',status='partial_waiting_review',source=C['source'],evaluation=C['evaluation'],responses=C['responses'],previous_state=ref(R/'current-state-23.json'),owner_decision=ref(R/'owner-decision-11.json'),owner_overlay=ref(R/'owner-review-overlay-11.json'),scope_plan=assign['original_before_review_plan'],scope_assignment=ref(M/'scope-assignment.json'),estimate=ref(M/'start.json'),manual_annotations=ref(M/'annotations.json'),method=A['method'],scope_policy=A['scope_policy'],summary=summary,inventory=rows,
    visual_source_pages_manually_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in range(31,35)],graphic_source_crops=ref(M/'graphic-source-crops.json'),graphic_views_manually_inspected=[z['readability_zoom'] for z in crops.values()],prior_issue_dispositions=prior['issue_dispositions'],prior_issues_retained=True,new_sources=0,new_extractions=0,new_corrections=0,new_owner_decisions=[],limits=C['limits'],limitations=C['limitations'],other_parts_executed=False)
save(O/'comparisons.json',c)
save(O/'issues.json',dict(inherited_pending=prior['unresolved_issue_ids'],prior_dispositions_preserved=prior['issue_dispositions'],new_issues=[],older_pending_unchanged=True,no_automatic_semantic_FP_FN=True,
    bounded_observations=['Label not whole rule','Conditional meanings distributed across action/conditions/exceptions; standalone action string not complete rule','Literal counter glyphs supported; rating meanings unknown','Physical continuation nodes delegate content to original owning node','Context R923 source gap retains partial status and full-result block'],
    preserved_pending_components=[dict(id=iid,assessment=next(r['manual_comparison'] for r in rows if r['id']==iid)) for iid in ['C-9.16-01','C-9.18-01','X-01','TR-02','D-01','G-01','G-02']]))
save(O/'presentation.json',dict(card='M-POC5A.4d2',summary=summary,decisions=[dict(number=1,ids=ids,occurrences=136,proposal='Accept stated bounded label, exact clause/row, glyph/orientation and physical-continuation assessments. Read guard/action/exception together; only explicit values, no whole records or extra rubric points.'),
    dict(number=2,ids=['C-9.16-01','C-9.18-01','X-01','TR-02','D-01','G-01','G-02'],proposal='Overlapping exclusions: older minimum1, specific leader exceptions, mapcompass and rating meanings remain unresolved. No old variant selected or missing source supplied.')],count_policy='136 bounded occurrence judgments; second recommendation is overlapping exclusions, not additional points or newly resolved meanings.',excludes=A['exclusions'],actual_owner_file_open_or_read='unknown',proposal_only=True,next_after_owner_decision='Separate.4d3 59 inventory IDs/118occurrences after refreshed estimate; .4d4/.4d5 andM-POC5B remain separate.'))
lines=['# M-POC5A.4d2 — 68 pozycji / 136 rzeczywistych porównań','',A['method'],'',A['scope_policy'],'','[Decyzje po ludzku](owner-focus.md) · [Pełne ślady](comparisons.json)','']
for row in rows:
    lines += [f"## {row['id']} — {row['inventory_type']}",'',row['manual_comparison'],'',f"Wynik: {row['manual_assessment']}; oba warianty ocenione, owner waiting_review, cały rekord nieprzyjęty.",'']
    for src in row['source_scopes']:
        if 'literal_scope' in src:
            lines += ['Dokładny fragment źródła:','', '> '+src['literal_scope'].replace('\n','\n> '),'',f"PDF{src['original_evidence']['pdf_page']}, `{src['helper']['path']}`, znaki{src['helper_character_range']}, hash`{src['literal_scope_sha256']}`.",'']
        else:lines += [f"Dokładny obraz: [{row['id']} source crop]({Path(src['graphic_scope']['exact_crop']['path']).name}), bboxPDF{src['original_evidence']['bbox_pdf_points']}; pełne hashe i prawdziwa ścieżka wJSON.",'']
    for run,x in row['runs'].items():
        lines += [f"**{run}:** {x['bounded_result']}; {x['comparison']}",'']
        for t in x['output_traces']:
            b=t['raw_span'];lines += [f"`{t['original_record']['id']}` pointer`{t['pointer']}`, bytes[{b['start_byte']},{b['end_byte_exclusive']}), hash`{b['sha256']}`.",'',json.dumps(t['original_record'],ensure_ascii=False),'']
        lines += ['Dawne zakresy:'+','.join(z['prior_scoped_decision']['id'] for z in x['prior_local_scopes']+x['prior_context_requirements'])+'; nie dodają nowych punktów.','']
    lines += ['Wyłączenia: '+'; '.join(A['exclusions'])+'.','']
lines += ['## Pokrycie','',json.dumps(summary,ensure_ascii=False),'','Pozostałe100pozycji:59w.4d3,41w.4d4; następnie osobna.4d5 rozliczenie i osobneM-POC5B20sytuacji. Oryginały/dawne decyzje/gold zachowane, metryki pełne nieocenialne.','']
(O/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(O/'review.md').write_text('# M-POC5A.4d2 — przegląd wykonany\n\n'+A['method']+'\n\n'+A['scope_policy']+'\n\n[Porównania](comparisons.md) · [Ślady](comparisons.json) · [Decyzje](owner-focus.md)\n\n'+lines[-2]+'\n',encoding='utf-8')
save(M/'packet-summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
