from session import ROOT,P,R,S,M,read,ref as file_ref,save,md,pointer,now,locate_records,RECORD_IDS
from manual_assessments import CASES
import copy,json,hashlib,collections

S.mkdir(exist_ok=True)
cache={}
def ref(f):
    key=f.as_posix()
    if key not in cache:cache[key]=file_ref(f)
    return cache[key]

state=read(R/'current-state-31.json');evalref=ref(P/'evaluation/eval-v1/manifest.json')
sitref=ref(P/'evaluation/eval-v1/situations.json');situations=read(P/'evaluation/eval-v1/situations.json')['situations']
assert len(situations)==20 and set(CASES)=={x['id']for x in situations}
props={run:read(P/f'proposals/{run}/proposal.json')for run in ['first-001','context-01']}
raw={run:(ROOT/state['responses'][run]['path']).read_bytes()for run in props}
provs={run:read(P/f'proposals/{run}/provenance.json')for run in props}
deps=read(P/'evaluation/eval-v1/dependencies.json')
frozen_deps={x['id']:(family,idx,x) for family in ['confirmed_execution_relations','unconfirmed_execution_candidates','mentions','continuations'] for idx,x in enumerate(deps[family])}
dependency_reports={run:read(P/f'reports/{run}/dependency-comparison.json')for run in props}
prior=read(R/'part-04d5/comparisons.json')['expectations']
checked=[]
def trace(run,ptr):
    value=pointer(props[run],ptr);span=provs[run]['json_value_spans'][ptr]
    chunk=raw[run][span['start_byte']:span['end_byte_exclusive']]
    assert hashlib.sha256(chunk).hexdigest()==span['sha256'] and json.loads(chunk)==value,(run,ptr)
    checked.append((run,ptr))
    return dict(response=state['responses'][run],provenance=ref(P/f'proposals/{run}/provenance.json'),pointer=ptr,raw_span=span,original_value=value)

rows=[];counts={run:collections.Counter()for run in props};positive=[];separate=[]
for si,sit in enumerate(situations):
    source_scopes=[]
    for ei,e in enumerate(sit['evidence']):
        image=P/e['render'];assert ref(image)['sha256']==e['render_sha256']
        child=e.get('source_span',e.get('source_transcription',e.get('transcription')))
        scope=dict(frozen_situation=sitref,evidence_pointer=f'/situations/{si}/evidence/{ei}',original_evidence=e,source_visual=ref(image),
          selected_literal_child=child,selected_child_precedes_parent=True,whole_parent_not_certified=True)
        if isinstance(child,str):scope['selected_literal_sha256']=hashlib.sha256(child.encode()).hexdigest()
        if e.get('helper_file'):
            helper=P/e['helper_file'];text=helper.read_text(encoding='utf-8-sig');parent=e['transcription'];start=text.find(parent)
            assert start>=0,(sit['id'],e['helper_file'])
            scope.update(helper=ref(helper),original_parent_fragment=parent,parent_helper_character_range=[start,start+len(parent)],
              parent_range_is_child_certificate=False)
            child_at=text.find(child) if isinstance(child,str)else-1
            scope['exact_child_helper_character_range']=[child_at,child_at+len(child)] if child_at>=0 else None
            scope['child_locator_policy']='Exact child text assessed on supplied image and ordered parent fragments. Parent envelope does not establish child meaning; child may cross columns.'
        source_scopes.append(scope)
    row=dict(id=sit['id'],title=sit['title'],frozen_situation=sitref,situation_pointer=f'/situations/{si}',
      facts=sit['facts'],facts_policy=sit['facts_policy'],question=sit['question'],frozen_expected=sit['expected'],
      expected_is_new_model_answer=False,authorizing_expected_decision=sit['authorizing_decision'],
      criticality=sit['criticality'],criticality_basis=sit['criticality_basis'],source_scopes=source_scopes,
      expectation_ids=sit['expectation_ids'],frozen_dependency_ids=sit['dependency_ids'],
      frozen_dependency_refs=[],runs={},reviewer='Codex',human_reviewer=None,owner_status='waiting_review',
      one_situation_is_one_sample=True,no_partial_variant_points=True,no_expected_or_fact_changes=True)
    for did in sit['dependency_ids']:
        family,di,d=frozen_deps[did]
        row['frozen_dependency_refs'].append(dict(id=did,artifact=ref(P/'evaluation/eval-v1/dependencies.json'),pointer=f'/{family}/{di}',
           classification='confirmed_scoped_execution_tuple'if family=='confirmed_execution_relations'else family,
           scoring_eligible=family=='confirmed_execution_relations',original_record=d))
    for run,prop in props.items():
        annotation=copy.deepcopy(CASES[sit['id']]);override=annotation.pop('context_override',None)
        if run=='context-01' and override:annotation.update(override)
        selected=RECORD_IDS[sit['id']][:]
        if sit['id']=='SIT-09'and run=='context-01':selected+=['NCTX846S4','DCTX932-S4','GCTX-845','GCTX-order']
        original=locate_records(prop,selected);output_traces=[];field_traces=[]
        for ptr,record in original:
            output_traces.append(trace(run,ptr))
            for key in ['transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','content','reason','needed_context','blocking']:
                if key in record:
                    field_traces.append(dict(trace(run,ptr+'/'+key),assessed_scope='Only feature used in evaluator derivation steps; not the whole containing field.'))
        ids={v['id']for _,v in original}
        edges=[(i,d)for i,d in enumerate(prop['dependencies'])if d['from']in ids]
        edge_traces=[trace(run,f'/dependencies/{i}')for i,_ in edges]
        gaps=set(g for _,o in original for g in o.get('gap_ids',[]))
        for _,edge in edges:gaps.update(edge.get('gap_ids',[]))
        gap_traces=[trace(run,f'/gaps/{i}')for i,g in enumerate(prop['gaps'])if g['id']in gaps]
        frozen_matches=[]
        for family in ['execution_relations','mentions','continuations']:
            frozen_matches += [x for x in dependency_reports[run][family]if x.get('evaluation_id')in sit['dependency_ids']]
        evidence_ids={eid for _,record in original for eid in record.get('evidence_ids',[])}
        evidence_traces=[trace(run,f'/evidence/{i}')for i,e in enumerate(prop['evidence'])if e['id']in evidence_ids]
        exp_scopes=[]
        for eid in sit['expectation_ids']:
            e=next(x for x in prior if x['id']==eid)
            exp_scopes.append(dict(id=eid,prior_scope=e['reviewed_scope'],owner_status=e['runs'][run]['prior_scoped_owner_status'],
               prior_owner_decision=e['runs'][run]['prior_owner_decision'],new_acceptance_of_old_scope=False))
        contextual=[]
        if sit['id']=='SIT-09'and run=='context-01':
            contextual=[dict(helper=ref(P/'context/pass-01/evidence/8.46-step-4-helper.txt'),
              source_image=ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),scope=ref(P/'context/pass-01/evidence/8.46-step-4-scope.json'),
              supplied_only=True,whole_pdf27_read=False,relevant_source_clause='Step4#4 reduction doesnotapply if defenderRouted; all applicability qualifications retained.')]
        d=dict(response=state['responses'][run],evaluator_compared=True,evaluator_review_complete=True,reviewer='Codex',human_reviewer=None,
          owner_status='waiting_review',proposed_classification=annotation['proposed_classification'],
          manual_assessment=annotation,original_record_traces=output_traces,selected_field_traces=field_traces,
          original_dependency_traces=edge_traces,original_gap_traces=gap_traces,original_evidence_traces=evidence_traces,
          frozen_relation_mapping_observations=frozen_matches,frozen_mapping_is_semantic_proof=False,
          prior_expectation_scopes=exp_scopes,additional_supplied_source=contextual,
          actual_model_situation_response='not_present; this is evaluation of preserved rule representation',
          evaluator_derived_result_is_model_response=False,new_inference=0,whole_record_accepted=False,
          assessment_scope='Every supplied variant and required local conclusion; completeID counted once. Held full conclusions remain in denominator.')
        row['runs'][run]=d;counts[run][d['proposed_classification']]+=1
        occurrence=dict(situation_id=sit['id'],run=run,classification=d['proposed_classification'])
        if d['proposed_classification']in ['correct_local_result','justified_block']:positive.append(occurrence)
        else:separate.append(occurrence)
    rows.append(row)
assert len(rows)==20 and sum(sum(c.values())for c in counts.values())==40
assert counts['first-001']=={'correct_local_result':15,'justified_block':3,'unjustified_block':1,'unassessed':1}
assert counts['context-01']=={'correct_local_result':14,'justified_block':3,'unjustified_block':1,'unassessed':2}
summary=dict(situation_ids=20,assigned_answer_case_judgments=40,per_answer_denominator=20,
  frozen_expected_local_results=17,frozen_expected_blocks=3,evaluator_compared_occurrences=40,owner_available_occurrences=40,
  new_owner_decided_occurrences=0,owner_pending_occurrences=40,unreviewed_occurrences=0,
  full_result_unassessed_despite_comparison_occurrences=3,per_answer={r:dict(c)for r,c in counts.items()},
  positive_scoped_occurrences=35,separate_decision_occurrences=5,
  proposal_wrong_result_occurrences=0,global_zero_critical_errors_claimed=False,
  classification_policy='Provisional evaluator judgments about stored rule representations, not executed model situation answers. All20IDs remain denominator; no partialvariantinflation.',
  meaningful_local_results_per_full20={'first-001':15,'context-01':14},
  expected_blocks_count_as_meaningful_result=False,full_quality_and_TP_FP_FN_precision_recall='not_assessable',
  previous_inventory_decided_scopes=414,old_pending_expectation_ids=state['pending_expectation_ids'],old_unresolved_issue_ids=state['unresolved_issue_ids'])
report=dict(id='M-POC5B-situations-01-results-01',card='M-POC5B',status='partial_waiting_review',recorded_at_utc=now(),
  evaluation=evalref,frozen_situations=sitref,responses=state['responses'],semantic_parent=ref(R/'current-state-31.json'),
  reconciliation_owner_decision=ref(R/'owner-decision-15.json'),estimate=ref(M/'estimate.json'),
  method='Manual derivation from exact original rule fields with synthetic facts, compared with frozen source-backed expected; no new extraction/correction/model scenario responses or engine. Original model statements and evaluator calculations separated.',
  summary=summary,situations=rows,source_views_inspected=[ref(P/f'source/review-evidence/pdf-{n}.png')for n in range(31,38)],
  additional_supplied_crop_inspected=ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),
  source_policy='SuppliedPDF31–37 and only suppliedStep4crop fromPDF27. Chapter boundary preserved; no additional sources or table values.',
  raw_field_traces_verified=len(checked),unique_raw_field_traces_verified=len(set(checked)),
  new_sources=0,new_extractions=0,new_corrections=0,new_gold=0,new_owner_situation_decisions=0,
  limitations=['Allproposalswaitingowner; oldmeaningvariantsnotclosed. No actual model situation-response run exists in these originals.',
    'Stored full-result blocking flags are evaluated in their source scopes; do not blanket-block supplied local facts or invent missing applicability.',
    'Metadata path discovery outside extractor allowlist confirmed; assessment-content read not observed; exposure/cleancontextunknown.',
    'Selectedmodel/reasoning,activehuman/modeltime,tokens,price,overallbudgetunknown; calendar notactive time.'])
save(S/'results.json',report)
save(M/'manual-assessments.json',dict(reviewed_at_utc=now(),cases=CASES,method=report['method']))
save(M/'validation.json',dict(exact20_ids=True,separate20_per_answer=True,all_required_variants_compared=True,
  all40_have_original_traces_and_manual_reasoning=True,frozen_facts_expected_unchanged=True,
  raw_spans_verified=len(checked),unique_raw_spans_verified=len(set(checked)),summary=summary))
lines=['# M-POC5B — pełna ocena20 sytuacji w obu odpowiedziach','',
 'Wykonano40 porównań. To ręczna ocena użyteczności oryginalnego zapisu reguł przy zamrożonych faktach. Wyprowadzenia i obliczenia należą do oceniającego; nie są nowymi odpowiedziami modelu na sytuacje. Wszystkie nowe oceny waiting_review.',
 '', '| Kategoria propozycji | first-001 | context-01 |','|---|---:|---:|',
 '| Zgodny lokalny wynik |15|14|','| Właściwa oczekiwana blokada |3|3|','| Kandydat nieuzasadnionej blokady |1|1|','| Pełny wynik nieocenialny po porównaniu |1|2|',
 '', 'Mianownik20 w każdym wyniku; poprawne blokady nie są meaningful local results dla progu80%. Pełna jakość i metryki relacji nadal nieocenialne. Źródła,pola,hashe,bajty i użyte zależności: [results.json](results.json).','']
for row in rows:
    lines+=[f"## {row['id']} — {row['title']}",'','### Zamrożone fakty i pytanie','','```json',json.dumps(row['facts'],ensure_ascii=False,indent=2),'```','',row['question'],'',
      '**Expected z eval-v1:** '+row['frozen_expected']['result'],'','**Zakres:** '+row['frozen_expected']['scope'],'']
    for sc in row['source_scopes']:
        e=sc['original_evidence'];lines+=[f"Źródło PDF{e['pdf_page']}/{e['column']}, `{sc['evidence_pointer']}`, obraz SHA `{sc['source_visual']['sha256']}`.",'']
        if isinstance(sc['selected_literal_child'],str):lines+=['> '+sc['selected_literal_child'].replace('\n','\n> '),'']
    for run,d in row['runs'].items():
        a=d['manual_assessment'];lines+=[f"### {run} — {d['proposed_classification']} / waiting_review",'',
          'Oryginał SHA: `'+d['response']['sha256']+'`.','', '**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**','','```json',json.dumps(a['evaluator_derived_result'],ensure_ascii=False,indent=2),'```','']
        for n,step in enumerate(a['derivation_steps'],1):lines.append(f'{n}. {step}')
        lines+=['','**Porównanie:** '+a['comparison_with_frozen_expected'],'','**Zależności i blokada:** '+a['dependency_use_and_block_scope'],'',
          '**Wyłączenia:** '+'; '.join(a['exclusions']),'']
        for t in d['selected_field_traces']:
            sp=t['raw_span'];lines+=[f"`{t['pointer']}`, bajty[{sp['start_byte']},{sp['end_byte_exclusive']}); SHA `{sp['sha256']}`.",'','```json',json.dumps(t['original_value'],ensure_ascii=False,indent=2),'```','']
        if a.get('uncertainty'):lines+=['Niepewność: '+a['uncertainty'],'']
md(S/'comparisons.md','\n'.join(lines))

issue_defs=[
 dict(id='SITREV-001',linked_semantic_issue='SEM-001',case_ids=['SIT-07'],runs=['first-001','context-01'],classes=['błędna interpretacja','nieuzasadniona lokalna blokada'],
   proposal='Confirm candidate unjustified branch-specific uncertainty/block for suppliedDR5=TQ5; source-backed expected0CH. No claim that model returned1CH or any actual scenario response. OlderSEM-001 meaning decision remains open.',criticality='critical_in_frozen_local_scope'),
 dict(id='SITREV-002',linked_semantic_issue='SEM-011',case_ids=['SIT-16'],runs=['first-001','context-01'],classes=['niejednoznaczność','niepełne powiązanie lokalnych ograniczeń'],
   proposal='Accept compared numeric/standingShock components but hold complete required combination conclusion without choosing old9.71/9.72 representation sufficiency. MissingDEP-NEW-001 separate; no automaticFN or demonstratedwrongmove.',criticality='critical_if_complete_gate_result_changed; no concretewrongoutcome demonstrated'),
 dict(id='SITREV-003',linked_semantic_issue='SEM-003',case_ids=['SIT-09'],runs=['context-01'],classes=['niejednoznaczność zakresu zamrożonych faktów po dostarczeniu źródła'],
   proposal='Hold contextual fullLC result for scope/fact decision: suppliedStep4 Routed exception and8.45qualifier not explicitly bound in frozenfacts. H&D prohibition and localhalfoperator retained; no gold/facts amended, no modelregression asserted.',criticality='conditional_on_Routed/applicability; knownbranch2versus5 matters',
   proposed_owner_options=['Keep frozenexpected and explicitly interpret noothermodifiers/localoperator scope as excluding the exception for this test.',
      'Record a separate evaluation-scope erratum/clarification with provenance; eval-v1 remains unchanged and both answers must be compared under the same approved scope.'])]
for issue in issue_defs:
    issue.update(status='waiting_review',reviewer='Codex',human_reviewer=None,source_and_output_basis=[dict(case_id=row['id'],case_pointer=f"/situations/{idx}",artifact=ref(S/'results.json'))for idx,row in enumerate(rows)if row['id']in issue['case_ids']],
      no_original_response_changes=True,no_frozen_eval_changes=True,no_automatic_semantic_FN=True)
save(S/'issues.json',dict(id='M-POC5B-issues-01',status='waiting_review',issues=issue_defs,old_pending_expectations=state['pending_expectation_ids'],
  old_unresolved_issue_ids=state['unresolved_issue_ids'],prior_limited_issue_dispositions=state['issue_dispositions'],new_semantic_errors_confirmed_by_owner=0))
save(S/'presentation.json',dict(id='M-POC5B-presentation-01',status='waiting_review',summary=summary,
  positive_scoped_set=positive,separate_decision_set=separate,recommendations=[
   {'id':'REC-SIT-01','proposal':'Accept35boundedpositivejudgments:29localresults and6expectedsourceblocks, as manualderivability evaluations.'},
   {'id':'REC-SIT-02','proposal':'Review2candidateunjustifiedblocks forSIT07 while preserving oldSEM001; do not claim1Hitmodelanswer.'},
   {'id':'REC-SIT-03','proposal':'Keep2completeSIT16results held for oldTriariicombination decision; no fractionalsuccess.'},
   {'id':'REC-SIT-04','proposal':'Keep1contextSIT09result held for suppliedcondition/frozen-scope decision; no silentgoldchange.'}],
  owner_actual_file_open_or_read='unknown',files=[ref(S/'results.json'),ref(S/'comparisons.md')]))
md(S/'review.md','''# M-POC5B — rzeczywisty przegląd20 sytuacji wykonany

Porównano wszystkie20 sytuacji, osobno dla first-001 i context-01:40 ocen. Każdy wariant/pytanie ma źródło, fakty, oryginalne pola i ślad do bajtów, ręczne wyprowadzenie oceniającego, porównanie z frozenexpected, użyte zależności/blokady i wyłączenia. Nie powtórzono ekstrakcji ani nie uzyskano nowych odpowiedzi modelu na sytuacje; to ocena oryginalnego zapisu reguł, nie uruchomienie silnika.

Propozycjefirst:15 zgodnych lokalnych wyników,3 właściwe oczekiwane blokady,1kandydat nieuzasadnionej lokalnej blokady,1pełny wynik nieocenialny po porównaniu. Context:14/3/1/2. Razem35 pozytywnych propozycji i5 ocen do osobnego rozstrzygnięcia. Pełny mianownik20/20 zachowany, brak punktów za warianty; trzy oczekiwane blokady na wynik nie są meaningfulresults dla progu80%.

[Pełne porównania](comparisons.md) · [Źródła,pola,bajty](results.json) · [Wyniki po ludzku](owner-focus.md).

SIT07 wiąże się z dawnym minimum/SEM001; SIT16 z dawnym połączeniem bramek/SEM011. ContextSIT09 ma nowe pytanie o stan/aplikowalność jawnie dostarczonego wyjątku przy zachowanych frozenfacts. Nie wybrano starych wariantów, nie poprawiono odpowiedzi lub gold. Odczyt pełnegoPDF27 nie nastąpił, tylko dostarczonegoStep4crop. Oryginały i wcześniejsze decyzje zachowane.

Porównano40 / udostępniono40 / nowych decyzji właściciela0 / pending40. Faktyczny odczyt plików unknown. M-POC5B oraz milestone5 pozostają partial/waiting_review; wszystkie sytuacje przejrzano, ale pełne wnioski trzech wystąpień są zawieszone. Pełnequality/TP/FP/FN/precision/recall not_assessable, starsze8 oczekiwań/13 kwestii nadal otwarte. Szacunek75–90min zapisano przed oceną; aktywneczasy/konfiguracja/tokeny/cena/budżet unknown.
''')
print('Built all40case judgments: first15/3/1/1,context14/3/1/2;35positive,5separate. Verified',len(checked),'rawfield/recordspans.')
