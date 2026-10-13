"""Bind authored comparisons to exact source child spans and original fields."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04d1'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=load(R/'checklist.json');A=load(M/'annotations.json');plan=load(M/'scope-plan.json');prior=load(R/'current-state-21.json');overlay=load(R/'owner-review-overlay-10.json');ids=plan['parts'][0]['inventory_ids']
assert [x[0] for x in A['rows']]==ids
prov={r:load(P/f'proposals/{r}/provenance.json') for r in C['responses']};unique={r:set() for r in C['responses']}
def trace(run,id):
    x=C['output_records'][run][id];ptr=x['pointer'];obj=x['original_record'];fields={}
    def walk(value,pointer):
        assert pointer in prov[run]['json_value_spans'],pointer
        fields[pointer]=dict(pointer=pointer,raw_span=prov[run]['json_value_spans'][pointer],original_value=value)
        if isinstance(value,dict):
            for k,v in value.items():walk(v,pointer+'/'+k.replace('~','~0').replace('/','~1'))
        elif isinstance(value,list):
            for i,v in enumerate(value):walk(v,pointer+'/'+str(i))
    walk(obj,ptr)
    return dict(response=C['responses'][run],pointer=ptr,raw_span=x['raw_span'],original_record=obj,fields=fields)
OUT.mkdir(exist_ok=False);rows=[]
for iid,assessment,note in A['rows']:
    n,item=next((i,x) for i,x in enumerate(C['inventory']) if x['id']==iid);f=item['frozen_item'];child=f.get('source_transcription');sources=[]
    for k,e in enumerate(f['evidence']):
        helperpath=P/e['helper_file'];helper=helperpath.read_text(encoding='utf-8-sig');literal=child if child is not None else e['transcription'];begin=helper.find(literal);assert begin>=0,(iid,e['helper_file'])
        sources.append(dict(evaluation_inventory=ref(P/'evaluation/eval-v1/inventory.json'),inventory_pointer=f'/items/{n}',original_evidence=e,
            literal_scope=literal,scope_policy='Exact child source_transcription takes precedence over containing parent' if child else 'Whole identified heading/note/example source passage; output may represent explicitly selected summary only',
            helper=ref(helperpath),helper_character_range=[begin,begin+len(literal)],literal_scope_sha256=hashlib.sha256(literal.encode()).hexdigest(),
            source_visual=ref(P/e['render']),visual_read_scope='Previously suppliedPDF31–36 only; no new source',parent_envelope_not_child_certificate=True))
    row=dict(id=iid,inventory_type=item['type'],evaluation_pointer=f'/items/{n}',frozen_inventory_item=f,source_scopes=sources,manual_assessment=assessment,manual_comparison=note,
        reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',whole_record_accepted=False,original_response_modified=False,
        prior_expectation_ids=item['expectation_ids'],overlapping_parent_child_not_additional_rule_points=True,exclusions=A['exclusions'],runs={})
    for run in C['responses']:
        mapped=item['runs'][run]['output_record_ids'];traces=[trace(run,id) for id in mapped];unique[run].update(mapped)
        evidenceids=list(dict.fromkeys(eid for t in traces for eid in t['original_record']['evidence_ids']));evidences=[trace(run,eid) for eid in evidenceids]
        gapids=[]
        for t in traces:
            node=t['original_record'];gapids+=node.get('gap_ids',[])
            if node['id']=='N932ex':gapids+=node['content']['value']['interpretation']['gap_ids']
        gaps=[trace(run,gid) for gid in dict.fromkeys(gapids)]
        oldscopes=[dict(artifact=ref(R/'owner-review-overlay-10.json'),pointer=f'/runs/{run}/scopes/{j}',prior_scoped_decision=z,policy='Retained only in its reviewed_scope; no duplicate rule/rubric point') for j,z in enumerate(overlay['runs'][run]['scopes']) if z['id'] in item['expectation_ids']]
        oldcontext=[dict(artifact=ref(R/'owner-review-overlay-10.json'),pointer=f'/runs/{run}/context_requirements/{j}',prior_scoped_decision=z) for j,z in enumerate(overlay['runs'][run]['context_requirements']) if z['id'] in item['expectation_ids']]
        notequote=[trace(run,'E917hist')] if iid=='N-05' else []
        row['runs'][run]=dict(response=C['responses'][run],status='waiting_review',evaluator_compared=True,reviewer=A['reviewer'],human_reviewer=None,owner_decision=None,
            literal_result='Source/evidence short quotation supported; main content does not state the historical proposition' if iid=='N-05' else 'Selected literal or structured/summary content supported in stated bounded scope',
            content_result=assessment,comparison=note,output_traces=traces,evidence_traces=evidences,gap_traces=gaps,central_statement_evidence=notequote,
            source_scopes=sources,original_mapping=item['runs'][run]['structural_mapping'],mapping_not_semantic_proof=True,
            prior_local_scopes=oldscopes,prior_context_requirements=oldcontext,whole_record_accepted=False,exclusions=A['exclusions'],uncertainties=['Actual full procedures and setup not acquired','Summary completeness and unreviewed aliases not certified','Old unresolved variants retained'])
    one=[t['original_record'] for t in row['runs']['first-001']['output_traces']];two=[t['original_record'] for t in row['runs']['context-01']['output_traces']]
    row['mapped_records_equal_between_runs']=one==two;row['between_run_difference']='Context N932ex documents supplied AS/LC evidence while retaining unknown execution/order' if iid=='X-04' else 'None in these mapped records'
    rows.append(row)
assert all(row['mapped_records_equal_between_runs'] for row in rows if row['id']!='X-04') and not next(row for row in rows if row['id']=='X-04')['mapped_records_equal_between_runs']
summary=dict(distinct_inventory_ids=39,assigned_inventory_occurrences=78,per_answer={'first-001':39,'context-01':39},evaluator_compared_occurrences=78,owner_available_occurrences=78,new_owner_reviewed_occurrences=0,owner_pending_occurrences=78,
    bounded_supported_inventory_occurrences=76,qualified_summary_omission_occurrences=2,structured_transcription_observations_occurrences=6,unique_mapped_records_per_answer={r:len(v) for r,v in unique.items()},
    remaining_assigned_inventory_ids=168,remaining_assigned_inventory_occurrences=336,all_inventory_ids=207,prior_owner_relation_scopes=257,prior_owner_locator_scopes=124,prior_category_units=264,
    previous_pending_expectation_ids=prior['pending_expectation_ids'],previous_unresolved_issue_ids=prior['unresolved_issue_ids'],new_issue_ids=['SEM-020'],TP_FP_FN_precision_recall='not_assessable',actual_owner_file_open_or_read='unknown',count_policy=A['scope_policy'])
c=dict(id='M-POC5A.4d1-comparisons-01',card='M-POC5A.4d1',status='partial_waiting_review',source=C['source'],evaluation=C['evaluation'],responses=C['responses'],previous_state=ref(R/'current-state-21.json'),owner_decision=ref(R/'owner-decision-10.json'),owner_overlay=ref(R/'owner-review-overlay-10.json'),
    scope_plan=ref(M/'scope-plan.json'),estimate=ref(M/'start.json'),manual_annotations=ref(M/'annotations.json'),method=A['method'],scope_policy=A['scope_policy'],summary=summary,inventory=rows,
    visual_source_pages_manually_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in range(31,37)],prior_issue_dispositions=prior['issue_dispositions'],prior_issues_retained=True,new_sources=0,new_extractions=0,new_corrections=0,new_owner_decisions=[],limits=C['limits'],limitations=C['limitations'],other_parts_executed=False)
save(OUT/'comparisons.json',c)
obs=dict(id='SEM-020',issue_class='content_summary_omission',criticality='noncritical_in_observed_historical_note_scope; no wrong game result demonstrated',inventory_id='N-05',source_scope=next(z for z in rows if z['id']=='N-05')['source_scopes'],
    source_says='Elephants did not fight in formations.',model_content='Historical statement; no additional formation procedure inferred.',
    difference='The content field has no central historical proposition. Exact evidence quote retains it in both responses; not total omission or a new game prohibition.',impact='Reading only node content loses note meaning. Following attached quote recovers source. No automaticsemanticFN/TP or response correction.',
    proposed_decision='Retain as limited content-summary defect while accepting faithful evidence quote; do not certify complete note content or infer formation rules.',runs={r:next(z for z in rows if z['id']=='N-05')['runs'][r] for r in C['responses']},status='waiting_review',human_reviewer=None)
# Use the exact N-05 source row, independently of ordinal layout.
obs['source_scope']=next(z for z in rows if z['id']=='N-05')['source_scopes']
save(OUT/'issues.json',dict(inherited_pending=prior['unresolved_issue_ids'],prior_dispositions_preserved=prior['issue_dispositions'],new_issues=[obs],structured_field_observation=dict(ids=['N-04','X-03','X-05'],occurrences=6,meaning='Values supported, fields named transcription contain structured data, not literal quotes',no_automatic_error_or_repair=True),
    older_pending_unchanged=True,no_automatic_semantic_FP_FN=True))
save(OUT/'presentation.json',dict(card='M-POC5A.4d1',summary=summary,decisions=[
    dict(number=1,ids=[id for id in ids if id!='N-05'],occurrences=76,proposal='Accept exact bounded title/selected note/example content observations with stated exclusions. Structured examples represent correct facts, not literal transcription. Prior scopes retained, no extra points.'),
    dict(number=2,ids=['N-05'],occurrences=2,proposal='Accept limited main-content omission SEM-020: evidence quote faithful but content generic. Not total missing note or demonstrated game error; no repair.'),
    dict(number=3,ids=['X-04','N-14','N-14-S2','N-14-S3','N-09','N-09-S2','X-06'],proposal='Retain older meaning variants and missing-source full-result blocks; literal existence of source statements is not their broader acceptance. No new meaning choice requested.')],
    count_policy='76 bounded+2 qualified =78 inventory occurrence judgments; third recommendation is an overlapping exclusion, not extra points.',excludes=A['exclusions'],actual_owner_file_open_or_read='unknown',proposal_only=True,next_after_owner_decision='Separate.4d2 68 inventory positions/136occurrences after refreshed estimate; other.4d3/4/5 andM-POC5B separate.'))
lines=['# M-POC5A.4d1 — rzeczywiste porównania39pozycji /78wystąpień','',A['method'],'',A['scope_policy'],'',
    '76 propozycji w dokładnym ograniczonym zakresie;2N-05 z ograniczonym pominięciem wtreści i poprawnym cytatem dowodowym. Wszystkie78 nowe decyzje waiting_review.','',
    *[f"{run}:hash`{x['sha256']}`,bajty{x['bytes']}." for run,x in C['responses'].items()],
    '', '[Pełne ślady](comparisons.json) · [Decyzje po ludzku](owner-focus.md).','']
for row in rows:
    lines += [f"## {row['id']} — {row['inventory_type']}",'',row['manual_comparison'],'',f"Nowa ocena:{row['manual_assessment']}; całego rekordu nie przyjęto.",'']
    for src in row['source_scopes']:
        lines += ['Dokładne źródło (child przed parent):','', '> '+src['literal_scope'].replace('\n','\n> '),'',
            f"PDF{src['original_evidence']['pdf_page']};helper`{src['helper']['path']}`,znaki{src['helper_character_range']},hash`{src['literal_scope_sha256']}`. Inwentarz`{src['inventory_pointer']}`. Parentbbox nie poświadczachild.",'']
    for run,x in row['runs'].items():
        lines += [f"**{run}:** oceniającyCodex; właścicielwaiting_review. {x['literal_result']}",'']
        for t in x['output_traces']:
            b=t['raw_span'];lines += [f"`{t['original_record']['id']}` `{t['pointer']}` bajty[{b['start_byte']},{b['end_byte_exclusive']}),hash`{b['sha256']}`.",'',json.dumps(t['original_record'],ensure_ascii=False),'']
        lines += ['Zachowane wcześniejsze zakresy:'+','.join(z['prior_scoped_decision']['id'] for z in x['prior_local_scopes']+x['prior_context_requirements'])+'. Bez dodatkowych punktów.','']
    lines += ['Zmiana między wynikami:'+row['between_run_difference']+'.','', 'Wyłączenia:'+ '; '.join(A['exclusions'])+'.','']
lines += ['## Pokrycie i wznowienie','',json.dumps(summary,ensure_ascii=False),'', 'Dalsze168pozycji mają rozłączny przydział68/59/41; osobna.4d5 rozliczy całość74oczekiwań/277rubryk/pending/szerszych pól. Nie wykonano innych kart. Gold/źródła/oryginały/dawne decyzje i metryki bez zmiany. Po obecnych decyzjach .4d2 po oszacowaniu.','']
(OUT/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'review.md').write_text('# M-POC5A.4d1 — przegląd wykonany\n\n'+A['method']+'\n\n'+A['scope_policy']+'\n\n[Porównania](comparisons.md) · [Ślady](comparisons.json) · [Decyzje](owner-focus.md)\n\n'+lines[-2]+'\n',encoding='utf-8')
save(M/'packet-summary.json',summary)
save(M/'estimate-arithmetic-note.json',dict(original_whole_estimate=ref(M/'scope-plan.json'),original_range=[300,420],part_range_sum=[sum(x['minutes_range'][0] for x in plan['parts']),sum(x['minutes_range'][1] for x in plan['parts'])],
    leading_sum_estimate_minutes_range=[330,430],reason='Whole range was a coarse planning estimate; summing the five explicitly recorded per-part ranges yields330–430. Both preserved; no active-time or budget compliance claim.',further_cards_estimate_before_execution=True))
print(json.dumps(summary,ensure_ascii=False))
