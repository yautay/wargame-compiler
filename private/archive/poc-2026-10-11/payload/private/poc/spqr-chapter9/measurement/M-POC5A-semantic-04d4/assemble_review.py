from review_tools import ROOT, P, M, R, read, ref, pointer, write
from manual_annotations import ANNOTATIONS
import json, hashlib, datetime, collections, copy

OUT=R/'part-04d4'
OUT.mkdir(exist_ok=False)
def save(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def md(path,text):path.write_text(text.rstrip()+'\n',encoding='utf-8')

now=datetime.datetime.now(datetime.timezone.utc).isoformat()
estimate=read(M/'estimate.json');ids=estimate['inventory_ids']
assert len(ids)==41 and len(set(ids))==41 and set(ids)==set(ANNOTATIONS)
save(M/'annotations.json',dict(recorded_at_utc=now,reviewer='Codex',judgments=ANNOTATIONS,
    method='Written after actual text/field/image comparison; owner decisions not granted.'))
scope=read(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json')['parts'][3]
save(M/'scope-assignment.json',dict(scope_plan=ref(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json'),pointer='/parts/3',assignment=scope))
state=read(R/'current-state-27.json')
source=ref(P/'source/original-pdf-20261008-01.pdf')
evalref=ref(P/'evaluation/eval-v1/manifest.json')
inventoryref=ref(P/'evaluation/eval-v1/inventory.json')
inventory=read(P/'evaluation/eval-v1/inventory.json')['items']
checklist=read(R/'checklist.json')
props={run:read(P/f'proposals/{run}/proposal.json') for run in ['first-001','context-01']}
provs={run:read(P/f'proposals/{run}/provenance.json') for run in props}
mappings={run:read(P/f'reports/{run}/inventory.json')['items'] for run in props}
rawpaths={'first-001':P/'runs/first-001/first-001.json','context-01':P/'runs/context-01/response.raw.txt'}
raw={run:path.read_bytes() for run,path in rawpaths.items()}
responses={run:ref(path) for run,path in rawpaths.items()}
common_exclusions=[
    'Akceptacja całego rekordu/pola/parent poza wymienioną cechą; niewymienione aliasy i globalna kompletność established_absent.',
    'Starsze EXP-010/017/019/040/050/052/066/074 oraz SEM-001–013 w pozostałych zakresach; warianty minimum, DD, AS/LC, Triarii i kompasu bez decyzji.',
    'Rzeczywisty setup/mapa/ZOC/LOS/ratingi i wartości Movement Cost Chart/MRRC/CRT oraz pełne bazowe procedury, bez zgadywania.',
    'Nowe punkty rubryki/gold, pełne TP/FP/FN/precision/recall, .4d5 i sytuacje M-POC5B.',
    'Całość ilustracji, glifów/lokatorów i dosłownej transkrypcji poza wybranymi zakresami; wcześniej przyjęte wady pozostają w oryginałach.']

def trace(run,ptr):
    val=pointer(props[run],ptr);span=provs[run]['json_value_spans'][ptr]
    chunk=raw[run][span['start_byte']:span['end_byte_exclusive']]
    assert hashlib.sha256(chunk).hexdigest()==span['sha256'],(run,ptr)
    assert json.loads(chunk)==val,(run,ptr)
    return dict(response=responses[run],provenance=ref(P/f'proposals/{run}/provenance.json'),pointer=ptr,raw_span=span,original_value=val)

items=[];verified_traces=0;record_ptrs={run:set() for run in props}
visuals=read(M/'visuals.json')['crops']
for id in ids:
    idx,item=next((i,item) for i,item in enumerate(inventory) if item['id']==id)
    annotation=ANNOTATIONS[id];sources=[]
    for ei,e in enumerate(item['evidence']):
        render=P/e['render'];assert ref(render)['sha256']==e['render_sha256']
        src=dict(evaluation_inventory=inventoryref,inventory_pointer=f'/items/{idx}',evidence_pointer=f'/items/{idx}/evidence/{ei}',
            original_evidence=e,source_visual=ref(render),literal_scope=e.get('transcription'),
            child_source_precedes_parent=True,mapped_parent_not_child_certificate=True)
        if 'transcription' in e:
            helper=P/e['helper_file'];txt=helper.read_text(encoding='utf-8-sig');literal=e['transcription']
            start=txt.find(literal);assert start>=0,(id,e['helper_file'])
            src.update(helper=ref(helper),helper_character_range=[start,start+len(literal)],literal_scope_sha256=hashlib.sha256(literal.encode()).hexdigest())
            if id=='C-9.95-02':
                end=literal.index(' To reflect')
                src['omitted_explanation_child']=dict(literal=literal[:end],character_range_in_literal=[0,end],helper_character_range=[start,start+end],
                     sha256=hashlib.sha256(literal[:end].encode()).hexdigest(),status='proposed_textual_omission; source image retained')
        sources.append(src)
    entry=dict(id=id,evaluation_pointer=f'/items/{idx}',type=item['type'],parent_id=item['parent_id'],
       source_scopes=sources,manual_comparison=annotation,runs={})
    original_maps={}
    for run in props:
        mapping=next(i for i in mappings[run] if i['inventory_id']==id);original_maps[run]=mapping
        record_ptrs[run].update(mapping['output_pointers'])
        selected=[dict(trace(run,ptr),assessed_scope='Only the feature described by manual_comparison; not all content of containing field.') for ptr in annotation['selected_fields']]
        verified_traces+=len(selected)
        evidence_traces=[]
        for eid in mapping['evidence_ids']:
            ei,ev=next((i,e) for i,e in enumerate(props[run]['evidence']) if e['id']==eid)
            evidence_traces.append(trace(run,f'/evidence/{ei}'))
        verified_traces+=len(evidence_traces)
        prior=next(x for x in checklist['inventory'] if x['id']==id)
        linked_expectations=prior.get('expectation_ids',[])
        result=annotation['bounded_result']
        entry['runs'][run]=dict(response=responses[run],status='waiting_review',evaluator_compared=True,reviewer='Codex',human_reviewer=None,
            source_scope_refs=[s['evidence_pointer'] for s in sources],original_mapping=mapping,mapping_is_semantic_proof=False,
            output_traces=selected,evidence_traces=evidence_traces,
            comparison=annotation,whole_record_accepted=False,proposed_decision=annotation['proposed_decision'],bounded_result=result,
            issue_ids=['SEM-022'] if id=='C-9.95-02' else [],
            prior_local_scope_expectation_ids=linked_expectations,prior_decision_refs=[state['expectation_owner_decision'],state['relationship_owner_decision'],state['locator_owner_decision']],
            previous_owner_judgments_retained=True,no_rescoring=True,
            uncertainties=['Właściciel nie podjął nowej decyzji; pełne wyniki zależą od nieocenionych zakresów/brakujących źródeł.',
                           'Meaning of visible counter ratings and real scenario qualifications remain unknown.'],
            exclusions=annotation['local_exclusions']+common_exclusions,
            visual_comparison=[v for v in visuals if v['run']==run and v['evidence_id'] in mapping['evidence_ids']])
    # Identity is lineage evidence only; source judgments above were made manually.
    all_ptrs=original_maps['first-001']['output_pointers']
    entry['same_mapped_values_between_answers']=all(pointer(props['first-001'],p)==pointer(props['context-01'],p) for p in all_ptrs)
    assert entry['same_mapped_values_between_answers'],id
    items.append(entry)

positive=[id for id in ids if id!='C-9.95-02']
summary=dict(distinct_inventory_ids=41,assigned_inventory_occurrences=82,per_answer={'first-001':41,'context-01':41},
    evaluator_compared_occurrences=82,owner_available_occurrences=82,new_owner_reviewed_occurrences=0,owner_pending_occurrences=82,
    bounded_supported_inventory_occurrences=80,mixed_clause_occurrences=2,underlying_omitted_explanatory_clauses_per_answer=1,
    facet_occurrences_by_inventory_type=dict(collections.Counter(i['type'] for i in items)),
    unique_mapped_records_per_answer={r:len(v) for r,v in record_ptrs.items()},prior_owner_inventory_scopes=332,
    total_inventory_evaluator_compared_assigned_occurrences=414,total_inventory_distinct_ids_compared=207,
    remaining_assigned_inventory_ids=0,remaining_assigned_inventory_occurrences=0,all_inventory_ids=207,
    prior_owner_relation_scopes=257,prior_owner_locator_scopes=124,prior_category_units=264,
    previous_pending_expectation_ids=state['pending_expectation_ids'],previous_unresolved_issue_ids=state['unresolved_issue_ids'],
    new_issue_ids=['SEM-022'],TP_FP_FN_precision_recall='not_assessable',actual_owner_file_open_or_read='unknown',
    count_policy='82 exact inventory scopes, not 82 full correct records/rules/TP. 80 supported and 2 mixed; one omitted explanation per answer. Prior scopes not scored again.')
summary['facet_occurrences_by_inventory_type']={k:v*2 for k,v in summary['facet_occurrences_by_inventory_type'].items()}
comparisons=dict(id='M-POC5A.4d4-comparisons-01',card='M-POC5A.4d4',status='partial_waiting_review',recorded_at_utc=now,
    source=source,evaluation=evalref,responses=responses,previous_state=ref(R/'current-state-27.json'),owner_decision=ref(R/'owner-decision-13.json'),
    owner_overlay=ref(R/'owner-review-overlay-13.json'),scope_plan=state['inventory_scope_plan'],scope_assignment=ref(M/'scope-assignment.json'),
    estimate=ref(M/'estimate.json'),manual_annotations=ref(M/'annotations.json'),summary=summary,inventory=items,
    method='Source passages and exact clause first, original selected fields next; independently scoped judgments for each answer. All 41 assigned IDs compared, including graphics and physical continuations. Hash/schema/mapping are lineage evidence only.',
    visual_source_pages_manually_inspected=[ref(P/f'source/review-evidence/pdf-{p}.png') for p in [36,37]],
    graphic_views_manually_inspected=read(M/'visuals.json'),prior_issue_dispositions=state['issue_dispositions'],prior_issues_retained=state['unresolved_issue_ids'],
    source_boundary='Chapter 9 stops before 10.0 on supplied PDF37. Full supplied page and helper displayed neighboring chapter10 material; no new source acquired, no chapter10 inventory added or old allocation decision reopened.',
    new_sources=0,new_extractions=0,new_corrections=0,new_owner_decisions=0,other_parts_executed=[],
    limits={'additional_pages':1,'additional_rules':1,'additional_tables':0,'context_rounds':1,'corrections':0,'full_gap_closures':0,'partial_updates':4,'new_declarations':4,'source_expansion_stop_depth':2},
    limitations=['No full metrics or whole-record certification. History of metadata listing outside extractor allowlist confirmed, evaluation-content read not observed; assessment exposure/clean context unknown.',
                'Selected model/reasoning, active human/model time, tokens/price/overall budget unknown; calendar duration is not active time.'])
save(OUT/'comparisons.json',comparisons)

lines=['# M-POC5A.4d4 — pełne porównania przypisanego zakresu','',
    '41 pozycji × 2 oryginalne odpowiedzi = 82 rzeczywiste porównania. Wszystkie propozycje waiting_review. Oceniający: Codex; właściciel nowych decyzji nie podjął.',
    '', 'Każda poniższa klauzula/rola ma własny zakres źródła i pól. Label nie przyjmuje treści całej reguły. Dosłowne krótkie cytaty, streszczenia i interpretacje są rozdzielone. Pełne bajty/pointers/hashe, oryginalne wartości i wyłączenia: [comparisons.json](comparisons.json).',
    '', '80 ograniczonych propozycji wsparcia i 2 oceny mieszane C-9.95-02/SEM-022. Jedno pominięte wyjaśnienie na odpowiedź; operatywna treść i obraz zachowane. 332 wcześniejsze decyzje pozostają bez zmiany.','']
for entry in items:
    a=entry['manual_comparison'];lines += [f"## {entry['id']} — {entry['type']}",'',f"**Instrukcja:** {a['source_says']}",'',f"**Model:** {a['model_says']}",'',f"**Różnica:** {a['difference']}",'',f"**Wpływ:** {a['impact']}",'',f"**Propozycja:** {a['proposed_decision']} / {a['bounded_result']}; waiting_review.",'']
    for si,s in enumerate(entry['source_scopes']):
        e=s['original_evidence'];lines += [f"Źródło {si+1}: PDF {e['pdf_page']}, {e['column']}, `{s['evidence_pointer']}`; bbox {e['bbox_pdf_points']}; hash obrazu `{s['source_visual']['sha256']}`.",'']
        if s['literal_scope']:
            lines += ['> '+s['literal_scope'].replace('\n','\n> '),'']
            lines += [f"Helper {s['helper']['path']}, znaki [{s['helper_character_range'][0]}, {s['helper_character_range'][1]}); SHA fragmentu `{s['literal_scope_sha256']}`.",'']
    for run,r in entry['runs'].items():
        lines += [f"### {run} — porównano, waiting_review",'',f"Oryginał: `{r['response']['sha256']}`; propozycja dotyczy tylko opisanej cechy poniższych pól.",'']
        for tr in r['output_traces']:
            sp=tr['raw_span'];lines += [f"`{tr['pointer']}`, bajty [{sp['start_byte']}, {sp['end_byte_exclusive']}); SHA `{sp['sha256']}`.",'','```json',json.dumps(tr['original_value'],ensure_ascii=False,indent=2),'```','']
        lines += ['Wyłączenia: '+' '.join(r['exclusions']),'', 'Niepewności: '+' '.join(r['uncertainties']),'']
md(OUT/'comparisons.md','\n'.join(lines))

mixed=next(i for i in items if i['id']=='C-9.95-02')
issue=dict(id='SEM-022',classes=['pominięcie'],status='waiting_review',reviewer='Codex',human_reviewer=None,
    inventory_ids=['C-9.95-02'],output_ids=['R995'],new_assigned_occurrences=2,underlying_omissions_per_answer=1,
    criticality='nonoperative_explanatory_content_in_presented_scope; no demonstrated wrong game result',
    proposal=ANNOTATIONS['C-9.95-02'],source_scopes=mixed['source_scopes'],output_traces={run:r['output_traces'] for run,r in mixed['runs'].items()},
    evidence_traces={run:r['evidence_traces'] for run,r in mixed['runs'].items()},
    source_image_retained=True,no_automatic_FN=True,no_new_rule=True,no_repair=True,
    impact='Textual explanation omitted in mapped content; operative MA/Momentum/ZOC/timing retained. Image retains the explanation. No demonstrated legal/game-outcome change.',
    exclusions=common_exclusions,structural_observations_separate=['Six heading/list-introduction roles are assessed without certifying a separate verbatim title; inherited two unassessed heading locators retained.'])
save(OUT/'issues.json',dict(id='M-POC5A.4d4-issues-01',status='waiting_review',responses=responses,evaluation=evalref,
    inherited_state=ref(R/'current-state-27.json'),inherited_open_issue_ids=state['unresolved_issue_ids'],prior_issue_dispositions=state['issue_dispositions'],
    new_issues=[issue],new_semantic_errors_confirmed_by_owner=0,
    observation_classes={'pominięcie':['SEM-022'],'błędny odczyt':[],'błędna interpretacja':[],'brak kontekstu':'inherited source requirements retained; full dependent results blocked',
      'niejednoznaczność':'inherited unresolved scopes unchanged','format':'inherited locators and structural missing pairs unchanged'},
    global_zero_errors_claimed=False))

save(OUT/'presentation.json',dict(id='M-POC5A.4d4-presentation-01',card='M-POC5A.4d4',status='waiting_review',
    evaluator_compared_occurrences=82,owner_available_occurrences=82,owner_newly_accepted_occurrences=0,owner_pending_occurrences=82,actual_owner_file_open_or_read='unknown',
    positive_set={'inventory_ids':positive,'per_answer':40,'occurrences':80,'scope':'Exact manual_comparison and selected fields only, including six bounded heading/list roles; not whole records.'},
    separate_decisions=[dict(id='SEM-022',inventory_ids=['C-9.95-02'],per_answer=1,occurrences=2,proposal='Confirm one limited omission of historical explanation per answer; operative content and source image retained.')],
    inherited_decisions_retained=332,inherited_open_expectations=state['pending_expectation_ids'],inherited_open_issues=state['unresolved_issue_ids'],
    files=[ref(OUT/'comparisons.json'),ref(OUT/'comparisons.md')],owner_decision_required=True,no_claim_owner_read=True))

md(OUT/'review.md','''# M-POC5A.4d4 — przegląd wykonany

Rzeczywiście porównano wszystkie 41 przypisanych pozycji inwentarza, osobno w obu oryginalnych odpowiedziach: 82 wystąpienia. Przeczytano dokładne źródłowe klauzule i wskazane oryginalne pola, obejrzano dostarczone strony PDF36–37 i osiem dokładnych wycinków obu odpowiedzi. Kolejność lewa→prawa kolumna 9.91 i PDF36→37 dla 9.96 zachowana; granica rozdziału przed 10.0.

Propozycje: 80 ograniczonych ocen wsparcia i 2 mieszane oceny C-9.95-02/SEM-022. Operatywna treść tej klauzuli zachowana; pominięto jedno historyczne wyjaśnienie na odpowiedź w textual content, źródłowy obraz nadal je zawiera. Bez automatycznego FN, naprawy lub nowej reguły. Sześć nagłówków/wprowadzeń oceniono jako role, bez przyjęcia ich pełnej literalnej transkrypcji lub dwóch dawnych nieocenionych lokatorów.

[Każde porównanie](comparisons.md) · [Dokładne źródła i pola/bajty](comparisons.json) · [Opis decyzji](owner-focus.md).

Porównano82 / udostępniono82 / nowych decyzji0 / pending82. Właściciel nie otrzymuje modelowej autoakceptacji. Faktyczny odczyt plików unknown. 332 wcześniejsze decyzje inwentarza, 257 relacji, 124 lokatorów, 264 pary rubryki i po63 lokalne zakresy/3 wymagania źródła zachowane bez ponownego punktowania. Starsze8 oczekiwań/13 kwestii pozostają otwarte.

Łączne pokrycie:207/207 pozycji i414/414 wystąpień porównano; nie jest to414 całych poprawnych rekordów. .4d5 uzgodnienie i M-POC5B40 ocen sytuacji niewykonane. Nadrzędne karty partial, M-POC5 jedyny next. Pełne metryki not_assessable, gold bez zmiany. Szacunek75–90min zapisano przed review; aktywny budżet/konfiguracja/tokeny/cena unknown.
''')

manifest=dict(id='M-POC5A.4d4-manifest-01',card='M-POC5A.4d4',status='partial_waiting_review',source=source,evaluation=evalref,responses=responses,
    artifacts=[ref(OUT/name) for name in ['comparisons.json','comparisons.md','review.md','issues.json','presentation.json']],
    scope_plan=state['inventory_scope_plan'],scope_assignment=ref(M/'scope-assignment.json'),estimate=ref(M/'estimate.json'),manual_annotations=ref(M/'annotations.json'),
    source_views=ref(M/'visuals.json'),owner_decisions=[])
# owner-focus is authored separately; manifest is finalized afterward.
save(M/'assembly-summary.json',dict(summary=summary,verified_raw_field_and_evidence_spans=verified_traces,
    all82_have_manual_judgments=True,assigned_ids_exhaustive=True,mapped_value_equality_is_not_semantic_proof=True,
    manifest_draft=manifest))
print('Built 41 separately scoped items / 82 judgments, 80 supported + 2 mixed; verified',verified_traces,'original field/evidence spans.')
