"""Close the separate context-response report; do not accept meaning for the owner."""
from pathlib import Path
import json,hashlib,datetime,collections,copy
ROOT=Path.cwd();P=ROOT/'private/poc/spqr-chapter9';M=P/'measurement/M-POC4B-context-01'
R=P/'reports/context-01';PR=P/'proposals/context-01';T=P/'transfer/context-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(x):
    b=x.read_bytes();return dict(path=x.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def load(x):return json.loads(x.read_bytes())
def save(x,obj):
    assert not x.exists(),x
    x.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not R.exists() and not PR.exists();R.mkdir();PR.mkdir()
A=load(M/'analysis.json');B=load(M/'new-evidence-analysis.json')
raw=(P/'runs/context-01/response.raw.txt').read_bytes();D=json.loads(raw)
old=load(P/'runs/first-001/first-001.json');run=load(P/'runs/context-01/run.json')
bm=load(P/'reports/first-001/metrics.json');bc=load(P/'reports/first-001/dependency-comparison.json')
E=load(P/'evaluation/eval-v1/expectations.json');G=load(P/'evaluation/eval-v1/dependencies.json')
POL=load(P/'evaluation/eval-v1/measurement-policy.json')
assert not A['issues'] and not A['duplicate_json_keys']
assert all(x['matches'] for x in A['input_integrity']+A['evaluation_integrity']+A['source_bindings'])
(PR/'proposal.json').write_bytes(raw)
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
save(PR/'provenance.json',dict(run_id='context-01',raw_response=desc(P/'runs/context-01/response.raw.txt'),
    representation=desc(PR/'proposal.json'),derivation='Entire raw UTF-8 JSON bytes copied unchanged; no content/format edits.',
    pointer_policy='RFC6901 JSON pointers; zero-based half-open UTF-8 lexical byte spans and fragment SHA-256.',
    json_value_spans=A['json_value_spans'],record_pointers=A['record_pointers'],
    parent_response=desc(P/'runs/first-001/first-001.json'),input_manifest=A['input_manifest'],
    evaluation_manifest=A['evaluation_manifest'],run=desc(P/'runs/context-01/run.json'),
    session_evidence=desc(P/'runs/context-01/session-evidence.txt'),
    scope_violation='Confirmed root entry/path metadata enumeration outside allowlist',
    clean_context_verified=False,assessment_exposure='unknown',semantic_acceptance='not_performed'))

delta={};old_ids={};new_ids={}
for group in ['rules','nodes','dependencies','evidence','gaps']:
    before={x['id']:x for x in old[group]};after={x['id']:x for x in D[group]}
    old_ids[group]=before;new_ids[group]=after
    changed=sorted(k for k in before.keys()&after.keys() if before[k]!=after[k])
    rows=[]
    for k in changed:
        diffs=[]
        def differ(a,b,path=''):
            if a==b:return
            if isinstance(a,dict) and isinstance(b,dict):
                for key in sorted(a.keys()|b.keys()):
                    if key not in a or key not in b:diffs.append(dict(path=path+'/'+key,before=a.get(key),after=b.get(key)))
                    else:differ(a[key],b[key],path+'/'+key)
            else:diffs.append(dict(path=path,before=a,after=b))
        differ(before[k],after[k])
        ptr=A['record_pointers'][k]
        rows.append(dict(id=k,pointer=ptr,raw_span=A['json_value_spans'][ptr],changes=diffs,
            attribution='Bounded-context change candidate; semantic correctness and scope require human review.'))
    delta[group]=dict(before=len(before),after=len(after),added=sorted(after.keys()-before.keys()),
        removed=sorted(before.keys()-after.keys()),changed=changed,unchanged=len(before.keys()&after.keys())-len(changed),changed_records=rows)
assert delta['rules']['changed']==['R932'] and delta['nodes']['changed']==['N932ex']
assert all(not x['removed'] for x in delta.values())
assert len(delta['dependencies']['added'])==5 and len(delta['evidence']['added'])==6

errors=[]
def error(cls,detail,pointer,status,criticality='unknown',impact=None):
    eid=f'ERR-context-01-{len(errors)+1:03}'
    errors.append(dict(id=eid,**{'class':cls},detail=detail,response_pointers=[pointer],
        raw_spans=[A['json_value_spans'][pointer]],status=status,criticality=criticality,
        impact=impact or 'Pending bounded review; not a confirmed semantic error.',
        response_sha256=sha(raw)))
    return eid
for inherited in load(P/'reports/first-001/errors.json')['errors']:
    if inherited['status']=='reported_claim_requires_review' or inherited['status']=='pending_locator_review':continue
    pointers=[]
    for ptr in inherited['response_pointers']:
        if ptr.startswith('/dependencies/'):
            oid=old['dependencies'][int(ptr.split('/')[2])]['id'];ptr=A['record_pointers'][oid]
        elif ptr.startswith('/evidence/'):
            parts=ptr.split('/');oid=old['evidence'][int(parts[2])]['id'];ptr=A['record_pointers'][oid]+('/'+'/'.join(parts[3:]) if len(parts)>3 else '')
        pointers.append(ptr)
    eid=error(inherited['class'],inherited['detail'],pointers[0],inherited['status'],inherited['criticality'],inherited['impact'])
    errors[-1]['inherited_baseline_error_id']=inherited['id'];errors[-1]['observation_unchanged']=True
for gap in D['gaps']:
    error('brak kontekstu' if gap['class']=='missing_context' else 'niejednoznaczność',
        'Extractor declaration '+gap['id']+': '+gap['reason'],A['record_pointers'][gap['id']],
        'reported_claim_requires_review',impact=dict(affected_ids=gap['affected_ids'],blocking_claim=gap['blocking'],
        needed_context=gap['needed_context'],semantic_confirmation='not_assessable'))

base_quotes={x['evidence_id']:x for x in load(P/'reports/first-001/quotes.json')['quotes']}
new_bbox={x['id']:x for x in B['results']};quotes=[];images=copy.deepcopy(A['images'])
for q in copy.deepcopy(A['quotes']):
    eid=q['evidence_id']
    if eid in base_quotes:
        assert old_ids['evidence'][eid]==new_ids['evidence'][eid]
        oq=base_quotes[eid];q.update({k:v for k,v in oq.items() if k not in {'pointer','raw_span','error_id'}})
        q['pointer']=A['record_pointers'][eid]+'/quote/value';q['raw_span']=A['json_value_spans'][q['pointer']]
        q['verification_method']='Current helper/hash/geometry checks plus inherited source/glyph/raster observation after exact evidence and source byte equality.'
        q['baseline_quote_artifact']=desc(P/'reports/first-001/quotes.json')
    else:
        b=new_bbox[eid];assert q['status']=='normalized_helper_match' and b['overlap_quote_match']
        q['area_status']='boundary_clipping_pending_review'
        q['new_source_match']=True;q['raster_area_visual_status']='short_quote_readable_by_Codex'
        q['visual_method']='Viewed exact asserted-area contact sheet of six crop-local areas; no semantic or glyph-envelope acceptance.'
        q['bbox_audit']=b
    if q['area_status']=='boundary_clipping_pending_review':
        q['error_id']=error('niejednoznaczność','Quote '+eid+' matches overlapping glyphs, not complete glyph envelopes; exact glyph-boundary review remains pending.',
            A['record_pointers'][eid]+'/image','pending_locator_review',impact='Do not count a strict whole-glyph-area pass. New raster areas are legible in the limited short-quote review.')
    quotes.append(q)
for im in images:
    q=next(x for x in quotes if x['evidence_id']==im['evidence_id'])
    im['quote_in_area_status']=q['area_status'];im['meaning']='not_assessable'

relations=copy.deepcopy(bc['execution_relations']);edges=new_ids['dependencies']
for row in relations:
    g=next(x for x in G['confirmed_execution_relations'] if x['id']==row['evaluation_id'])
    expected=tuple(row['mapped_output_endpoints'])+(g['kind'],g['explicitness'])
    matches=[x['id'] for x in D['dependencies'] if (x['from'],x['to'],x['kind'],x['explicitness'])==expected]
    assert matches==row['candidate_output_ids']
    row['output_pointers']=[A['record_pointers'][x] for x in matches]
    row['raw_spans']=[A['json_value_spans'][x] for x in row['output_pointers']]
    row['semantic_result']='not_assessable';row['comparison_to_parent']='unchanged tuple observation'
mentions=copy.deepcopy(bc['mentions']);continuations=copy.deepcopy(bc['continuations'])
for group in [mentions,continuations]:
    for row in group:
        for key in ['raw_span','raw_spans','output_pointers','error_id']:row.pop(key,None)
        row['parent_comparison_artifact']=desc(P/'reports/first-001/dependency-comparison.json')
        row['method']='Relevant original occurrence/continuation dependencies and endpoints are unchanged; parent observation retained with current input/source byte checks.'
for row in bc['all_output_edges']:
    if row['classification']=='frozen_tuple_candidate':assert old_ids['dependencies'][row['id']]==edges[row['id']]
baseline_edgeclass={x['id']:x['classification'] for x in bc['all_output_edges']}
output_edges=[dict(id=x['id'],kind=x['kind'],explicitness=x['explicitness'],target_status=x['target_status'],
    classification=baseline_edgeclass.get(x['id'],'new_context_edge_pending_review'),semantic_result='not_assessable',
    review_status='waiting_review',pointer=A['record_pointers'][x['id']],raw_span=A['json_value_spans'][A['record_pointers'][x['id']]]) for x in D['dependencies']]

expectations=[];mapped={x['inventory_id']:x for x in A['inventory_results']}
for exp in E['expectations']:
    out=sorted({x for ref in exp['inventory_refs'] if ref in mapped for x in mapped[ref]['output_ids']})
    gaps=sorted(g['id'] for g in D['gaps'] if set(g['affected_ids'])&set(out))
    expectations.append(dict(id=exp['id'],classification=exp['classification'],criticality=exp['criticality'],
        mapped_output_ids=out,candidate_gap_ids=gaps,result='not_assessable',
        reason='Human semantic review of frozen bounded expectations is not performed; source presence is not group correctness.'))
changed_gaps=[dict(id=k,before=old_ids['gaps'][k],after=new_ids['gaps'][k],
    full_gap_closed=False,partially_supplied_claim=True,necessity_and_sufficiency='pending_human_review') for k in delta['gaps']['changed']]
assert all(x['after']['blocking'] for x in changed_gaps)
paths=[dict(root=root,path=[root,'NCTX846S4','N1013','6.68 bullet #6'],depth=3,
    status='blocked_source_beyond_context_depth_boundary',
    method='New core-to-fragment edge plus new fragment-to-existing boundary node plus unchanged unresolved D1013stack.',
    disposition='No third-step source acquired; stop at allowed depth-2 boundary. Not a full graph-depth compliance certificate.') for root in ['R932','R923','R962']]
comparison=dict(run_id='context-01',parent_run_id='first-001',parent_response=desc(P/'runs/first-001/first-001.json'),
    response=desc(P/'runs/context-01/response.raw.txt'),record_deltas=delta,
    inherited_gap_ids_retained=81,old_gap_ids_removed=0,retained_changed_gap_ids=delta['gaps']['changed'],
    added_gap_ids=delta['gaps']['added'],full_declared_gap_closures=0,partial_source_updates=changed_gaps,
    source_procedure_endpoint_resolved=[dict(id='D962shock',before=old_ids['dependencies']['D962shock'],after=edges['D962shock'],
        status='source_target_fragment_now_supplied_only',full_result_closed=False,semantic_result='not_assessable')],
    confirmed_semantic_improvements='not_assessable',semantic_regressions='not_assessable',
    structural_regressions=dict(removed_parent_records=0,new_key_id_reference_enum_errors=0,inherited_locator_failure=1,
        new_strict_glyph_pending_areas=6,new_raster_areas_legible=6),
    scope_delta=dict(pages=1,rules=1,tables=0,source_depth_supplied=1,selection_depth_considered=2,
        newly_linked_unresolved_context_branch_depth=3,full_graph_depth_compliance='not_assessable',context_response_rounds=1,corrections=0),
    depth_blocked_paths=paths,active_time_budget='unknown',time_budget_compliance='unknown',
    first_reached_limit_applies=True,no_further_source_acquisition=True,
    corrections_result='not_assessable',semantic_acceptance='not_performed')

metrics=copy.deepcopy(bm);metrics.update(run_id='context-01',recorded_at_utc=stamp,response_sha256=sha(raw),
    method='Independent complete format/ID/reference/hash/inventory checks; inherited source observations only after equality verification; new six quotes checked against source/helper/PDF geometry and exact raster areas. No inference/correction or semantic acceptance.',
    counts=A['counts'],structural_checks={k:dict(passed=v,checked_denominator=v) for k,v in A['checks'].items()},
    input_files=dict(matched=41,checked_denominator=41),transfer_files=dict(verified=42,checked_denominator=42,historical_first_use='unknown'),
    source_bindings=dict(matched=43,checked_denominator=43),
    source_quotes=dict(checked_denominator=111,normalized_helper_matches=109,inherited_visual_matches=2,supported_short_quotes=111,
        new_quotes_source_supported=6,new_quote_semantic_acceptance='not_performed',transcription_error_count='not_assessable'),
    image_locators=dict(checked_denominator=111,hash_dimensions_valid_coordinates=111,strict_contained_quote_matches=41,
        inherited_graphic_label_visual_matches=5,quote_area_failure=1,boundary_clipping_pending_review=64,
        new_strict_contained_matches=0,new_overlapping_matches=6,new_raster_quotes_readable=6,fully_valid_content_areas='not_assessable'),
    cost=dict(new_extractions_in_evaluator=0,context_response_rounds_total=1,corrections_total=0,
        recorded_extractor_turn_calendar_seconds=run['timing']['turn_calendar_elapsed_seconds'],
        user_active_seconds='unknown',model_active_seconds='unknown',tokens='unknown',price='unknown',time_budget_compliance='unknown'),
    context_comparison=dict(full_declared_gap_closures=0,old_declared_gaps_retained=81,partial_gap_updates=4,new_declared_gaps=4,
        semantic_improvement='not_assessable',semantic_regressions='not_assessable'),scope_budget=comparison['scope_delta'],
    isolation=dict(scope_violation_confirmed=True,assessment_exposure='unknown',clean_context_verified=False,contamination_proven=False),
    context_result='not_assessable',corrected_result='not_assessable')
metrics['relations']['output_counts']=A['output_edge_counts']
for kind,total in [('explicit',75),('implicit',28)]:
    metrics['relations'][kind]['output_execution_denominator']=total;metrics['relations'][kind]['output_pending_review']=total
metrics['relations']['outside_confirmed_execution_set'].update(explicit_pending=70,implicit_pending=28)
classcounts=collections.Counter(x['class'] for x in errors)
confirmed=collections.Counter(x['class'] for x in errors if x['status'] in ['confirmed_locator_failure','confirmed_structural_omission'])
metrics['six_error_classes']=[dict(**{'class':c},confirmed_observations=confirmed[c] if c in ['format','pominięcie'] else 'not_assessable',
    logged_observations_or_claims=classcounts[c],scope='Structural/source-locator observations separate from declarations and semantic review.') for c in ['format','pominięcie','błędny odczyt','błędna interpretacja','brak kontekstu','niejednoznaczność']]

save(R/'format.json',dict(run_id='context-01',raw_response=desc(P/'runs/context-01/response.raw.txt'),json_parse='passed',
    duplicate_json_keys=A['duplicate_json_keys'],required_key_field_id_reference_enum_checks=A['checks'],issues=A['issues'],
    references=A['references'],input_integrity=A['input_integrity'],evaluation_integrity=A['evaluation_integrity'],source_bindings=A['source_bindings'],
    original_format=desc(P/'formats/proposal-format-v1.md'),context_addendum=desc(T/'formats/context-addendum-v1.md'),
    readable=True,semantic_acceptance='not_performed'))
save(R/'inventory.json',dict(run_id='context-01',summary=metrics['reference_inventory'],items=A['inventory_results'],
    expectations=expectations,categories=metrics['content_categories'],situation_denominator=20,situations_result='not_assessable',
    evaluation_manifest=A['evaluation_manifest'],mapping_is_semantic_score=False))
save(R/'dependency-comparison.json',dict(run_id='context-01',execution_relations=relations,mentions=mentions,
    continuations=continuations,all_output_edges=output_edges,depth_blocked_paths=paths,semantic_precision_recall='not_assessable'))
save(R/'quotes.json',dict(run_id='context-01',summary=metrics['source_quotes'],quotes=quotes,
    inherited_evidence_byte_equal=105,new_source_match=6,semantic_acceptance='not_performed'))
save(R/'image-areas.json',dict(run_id='context-01',summary=metrics['image_locators'],images=images,
    new_glyph_results=B,contact_sheet=desc(M/'new-evidence-areas.png'),
    current_visual_review='Codex viewed the six exact asserted raster areas; quotes legible, strict PDF glyph envelopes not fully contained. No complete content/semantic certification.'))
save(R/'errors.json',dict(run_id='context-01',response_sha256=sha(raw),six_classes=metrics['six_error_classes'],errors=errors,
    operational_limitations=run['session_evidence'],count_policy='Declared gaps and pending cases are not confirmed semantic errors.'))
save(R/'context-comparison.json',comparison)
save(R/'metrics.json',metrics)
report=f'''# context-01 - oddzielny raport M-POC4B

Data: 2026-10-10, Europe/Warsaw. Raport zamknięty; karta partial/waiting_review.
Odbiór istniejącej ręcznej odpowiedzi, bez powtórzenia inferencji/korekt.
Oryginał transfer/context-v1/context-01.json i runs/context-01/response.raw.txt
mają identyczne 712014 bajtów, SHA-256 {sha(raw)}.
Rodzic first-001, SHA-256 {comparison['parent_response']['sha256']}, pozostaje baseline.
Manifest nowego pakietu: {A['input_manifest']['sha256']}; eval-v1 niezmienione.

## Pierwszy wynik / po kontekście / po korektach

| Obserwacja | first-001 | context-01 | po korektach |
|---|---:|---:|---|
| Reguły / węzły / relacje / dowody / deklaracje luk | 50 / 58 / 126 / 105 / 81 | 50 / 60 / 131 / 111 / 85 | not_assessable |
| Pełne usunięte deklaracje luk | baseline | 0 | not_assessable |
| Częściowo zaktualizowane wcześniejsze luki | baseline | 4, nadal blocking | not_assessable |
| Zamrożone jawne pary-kandydaci | 5/5 | 5/5 | not_assessable |
| Zamrożone niejawne pary-kandydaci | 0/3 | 0/3 | not_assessable |
| Semantyczne TP/FP/FN i 20 sytuacji | not_assessable | not_assessable | not_assessable |

Nie utożsamiać liczby rekordów/źródłowych operatorów z poprawą znaczenia.
Zmieniły się R932, N932ex, dwa stare rekordy zależności i cztery stare luki.
Dodano dwa węzły, pięć relacji, sześć dowodów i cztery luki. Żaden stary rekord
nie został usunięty. Wszystkie 81 deklaracji luk pozostało; changed_gaps nadal
blocking. D962shock ma teraz cel w dostarczonym fragmencie, lecz jego pełny
wynik pozostaje zablokowany. Interpretacja wyjątku R932 oraz nowa niejawna
relacja ze R923 wymagają review; nie uznano ich za naprawę lub semantyczne TP.

## Kontrole struktury, źródeł i mianowników

480 ID rekordów i 154 ID klauzul unikalnych; 3660 referencji rozwiązanych.
10108 wymaganych kluczy, 832 Field objects, 759 wartości enum, bez błędów
tych kontroli. 41/41 artefaktów nowego manifestu i 42/42 pliki wejściowe,
43/43 wiązania sources, 7/7 artefakty zamrożonej oceny zgodne.
105 odziedziczonych dowodów jest identycznych z baseline; raportuje się
osobno odziedziczone oględziny i obecne helper/hash/geometry checks.

111 krótkich cytatów ma podparcie: 109 matches helper, 2 dawne ograniczone
oględziny potwierdzone śladem identyczności. Wszystkie 6 nowych cytatów pasuje
do pomocniczego tekstu i źródłowego wycinka. 111/111 geometrii/hashów/wymiarów
poprawnych. Dziedziczony błąd E916 nie naprawiony; 58 dawnych granic glifów
pending. Nowe 6 obszarów: 0 ścisłych matches całych glifów, 6 matches glifów
przecinających granice; w oględzinach rasteru wszystkie sześć cytatów czytelne.
Nie nadaje to ścisłego certyfikatu granic: 64 pending łącznie, 41 dawnych
ścisłych matches, 5 dawnych napisów graficznych, 1 błąd obszaru. Nie zmieniono
samego źródła ani bbox w odpowiedzi, nie sprawdzono wszystkich treści/liczb.

207 ID inwentarza rozliczone: 205 kandydatów, 2 lokatory nieocenione; 41/41
różnych oznaczeń. Mapowanie nie dowodzi kompletności każdej klauzuli.
66 grup treści, 8 wymagań kontekstu i rubryki 41/38/43/66/52/29/7/1
zachowują mianowniki i not_assessable. 20 sytuacji (17 lokalnych/3 blokady)
nie rozstrzygnięto na nowo; syntetyczne dane nie stały się rzeczywistym setupem.

Relacje wykonawcze: 75 jawnych, 28 niejawnych; poza nimi 21 wzmianek i 7
kontynuacji. Wszystkie 131 rozliczone. Brakujące trzy krytyczne pary niejawne
i cztery pary wzmianek nadal obecne jako pominięcia strukturalne; różnica
rodzaju jednej wzmianki pending. Wszystkie semantyczne precision/recall
not_assessable. Nowe propozycje spoza gold nie są pewnymi FP ani TP.

Sześć klas: format - 1 dziedziczony błąd lokatora; pominięcie - 7 brakujących
par; błędny odczyt - not_assessable; błędna interpretacja - kandydaci pending,
bez nowego werdyktu; brak kontekstu - 82 deklaracje; niejednoznaczność -
3 deklaracje oraz 64 granice glifów pending. Nie raportować zerowych błędów
znaczenia tylko dlatego, że nie wykonano review człowieka.

## Koszt, głębokość i izolacja

Faktycznie 1 ręczna odpowiedź po kontekście, 0 korekt, 0 nowych inferencji
w sesji oceniającej. Dodatkowe źródło: 1 strona / 1 reguła / 0 tabel.
Wybrana dostarczona ścieżka ma 1 krok, M-POC4A rozważało do 2. Nowy graf
łączy R932/R923/R962 -> NCTX846S4 -> istniejące N1013 -> brakujące 6.68
bullet #6: 3 krawędzie do nierozstrzygniętego celu. Nie pozyskano trzeciego
kroku źródła; na granicy 2 zatrzymano rozszerzanie. Nie deklarować zgodności
głębokości całego grafu. Brakujący cel i jego wpływ zachowano w raporcie;
pass-02 nie uruchomiono i nie wolno go traktować jako obejścia limitu.

Niezależny zapis aplikacji potwierdza start w korzeniu repo, próbę odczytu
nieistniejącej root transfer-list, listę nazw i wyszukiwanie ścieżek poza
allowlistą. Naruszona izolacja dostępu; nie jest to samo w sobie dowód
otwarcia klucza oceny. W dostępnym transkrypcie nie zaobserwowano odczytu
treści oceny; assessment exposure pozostaje unknown, bez certyfikatu czystego
kontekstu i bez dowodu skażenia. Samoopis not_exposed nie zastępuje dowodu.
Snapshot i konkretne komendy są w run.json i prywatnym pomiarze.

App turn: {run['timing']['turn_started_at_utc']} - {run['timing']['turn_completed_at_utc']},
{run['timing']['turn_calendar_elapsed_seconds']} s kalendarzowych. To nie czas
aktywny człowieka/modelu ani ścisły czas inferencji. Model/rozumowanie,
aktywne czasy, tokeny, cena i budżet czasu unknown; żadnej zgodności nie
zadeklarowano. Historyczne konfiguracja/przekazanie/czysty kontekst first-001
pozostają unknown. Odpowiedzi, wejść, źródeł, draftów, freeze, eval-v1 ani
zamkniętego raportu baseline nie zmieniono.

## Wznowienie i bramka człowieka

Karta partial/waiting_review: przygotowano odbiór, niezależne kontrole i
zamknięty raport; człowiek ma potwierdzić zakres efektu dostarczonego fragmentu.
Proponowane rozliczenie: częściowe podparcie procedury i celu źródłowego,
0 pełnych domknięć luk, nierozstrzygnięte znaczenie i reszta blokad jawna.
Nie jest to automatyczne zaliczenie jakości ani 20 sytuacji.
reviews/context-source-01/request.json prowadzi konkretny przegląd tej bramki.
Po jego zamknięciu przejść do M-POC5A/B, oceniając oba wyniki osobno na eval-v1.
Nie powtarzać ekstrakcji, nie edytować odpowiedzi, nie dokładać nowego kontekstu.
Kontrole repo i pomiary zamknięcia są w nowym completion.json; ten raport
pozostaje niezmieniony, a późniejsze decyzje/review są osobnymi artefaktami.
'''
(R/'report.md').write_text(report,encoding='utf-8')
save(R/'manifest.json',dict(run_id='context-01',card='M-POC4B',closed_report_before_corrections=True,
    response=desc(P/'runs/context-01/response.raw.txt'),parent_response=desc(P/'runs/first-001/first-001.json'),
    input_manifest=A['input_manifest'],evaluation_manifest=A['evaluation_manifest'],
    artifacts=[desc(x) for folder in [PR,R] for x in sorted(folder.iterdir()) if x.is_file()],
    self_hash_policy='Manifest hash in separate closure.json; never self-hash.',semantic_acceptance='not_performed'))
save(R/'closure.json',dict(id='M-POC4B-context-01-report-closure',closed_at_utc=stamp,
    report_manifest=desc(R/'manifest.json'),response=desc(P/'runs/context-01/response.raw.txt'),
    parent_baseline_closure=desc(P/'reports/first-001/closure.json'),report_closed=True,
    card_outcome='partial_waiting_review',new_inference_responses=0,new_corrections=0,
    semantic_acceptance='not_performed'))
Q=P/'reviews/context-source-01';assert not Q.exists();Q.mkdir(parents=True)
save(Q/'request.json',dict(id='M-POC4B-RQ-01-effect-scope',status='waiting_review',decision=None,
    question='Potwierdzić zakres efektu: dostarczony fragment podparł część procedury/cel źródłowy, lecz 0 pełnych luk zamknięto; pozostałe blokady, nowa ścieżka do trzeciego nierozstrzygniętego kroku i ograniczenie izolacji pozostają jawne?',
    report=desc(R/'report.md'),comparison=desc(R/'context-comparison.json'),source_image=desc(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),
    scope='M-POC4B source effect/remaining blocks only; no acceptance of rule meaning, new implicit relationships, AS/LC order, situation results or time budget.',
    detailed_changed_records=delta['rules']['changed_records']+delta['nodes']['changed_records'],
    semantic_acceptance='not_performed',human_reviewer='owner; identity unknown'))
print(json.dumps(dict(report=desc(R/'report.md'),closed=desc(R/'closure.json'),classes=metrics['six_error_classes'],
    raw_spans=len(A['json_value_spans']),full_gap_closures=0,new_gaps=4),ensure_ascii=False,indent=2))
