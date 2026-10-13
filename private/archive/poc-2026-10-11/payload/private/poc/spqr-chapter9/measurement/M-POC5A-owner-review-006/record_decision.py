"""Record assent to both bounded .4b2 recommendations without changing evidence."""
from pathlib import Path
from datetime import datetime,timezone
import copy,json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
R=P/'reviews/semantic-01';PACK=R/'part-04b2';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();reply='zatwierdxam'
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(recorded_at_utc=now,card='M-POC5A',part='M-POC5A.4b2-owner-review',estimate_minutes=[10,20],
    estimate_scope='Record owner assent to two presented recommendations; no new batch/review/source.',protected=protected,
    sessions_before=ref(P/'measurement/sessions.jsonl'),owner_reply_verbatim=reply))
C=load(PACK/'comparisons.json');pres=load(PACK/'presentation.json');old=load(R/'owner-review-overlay-05.json');prior=load(R/'current-state-12.json')
for a in [C['evaluation'],C['source'],*C['responses'].values(),*load(PACK/'manifest.json')['artifacts']]:assert ref(ROOT/a['path'])==a
positive=pres['positive_scope'];special=pres['separate_issue']['ids']
assert len(positive['ids'])==26 and len(special)==4 and not set(positive['ids'])&set(special)
recommendations=[
 dict(number=1,decision='Przyjąć52 ograniczone zakresy relacji: role odesłań i wymagania źródła; bez treści brakujących celów lub pełnych wyników.',
      ids=positive['ids'],occurrences=52,includes=positive['includes'],excludes=positive['excludes']),
 dict(number=2,decision='Dla8 wystąpień przyjąć powiązania wyjątków; blokadę zawęzić do nieznanego dalszego wykonania/skutków. Szeroka deklaracja jest niewystarczająca do odróżnienia znanego lokalnego wyjątku.',
      ids=special,occurrences=8,issue='SEM-017',
      local_scope='OW exception to Rampage priority; no-AS cavalry Flank/Rear vsElephant; no Position/AS Elephant-vs-Elephant; bounded nonreciprocal Pre-Shock exemptions.',
      block_scope='Applicable full OW/general combat/remaining nonexempt checks can still require missing target source. Given participants/directions support local exception/no-AS/no-check answer.',
      excludes=positive['excludes'],actual_wrong_played_outcome='not_demonstrated')]
save(M/'approval-evidence.json',dict(owner_reply_verbatim=reply,interpretation='Unambiguous assent to both immediately presented recommendations; typo retained verbatim.',
    preceding_recommendations=copy.deepcopy(recommendations),basis=[ref(PACK/'owner-focus.md'),ref(PACK/'presentation.json'),ref(PACK/'issues.json')],
    recorded_at_utc=now,owner_message_sent_at_utc='unknown',actual_owner_file_open_or_read='unknown',
    limitations='Approval of presented bounded meaning and block-scope assessment; no full records, missing source acquisition, old pending selection or next batch execution.'))
reviewer='owner in this chat; personal identity unknown';scopes=[]
for idx,row in enumerate(C['relationships']):
    issue=row['id'] in special
    scoped=dict(id=row['id'],source_scope=row['source_scope'],target_scope=row['target_scope'],source_evidence=row['source_evidence'],
        bounded_independent_source=row['bounded_independent_source'],actual_target_source=None,target_source_policy=row['target_source_policy'],
        necessity_and_missing_impact=row['necessity_and_missing_impact'],evaluator_comparison=row['proposal'],
        owner_recommendation_number=2 if issue else 1,accepted_components=positive['includes'],excluded_components=positive['excludes'],
        reviewer=reviewer,recorded_at_utc=now,status='reviewed',
        result='correct_bounded_exception_with_block_scope_qualification' if issue else 'correct_in_bounded_named_requirement_scope',
        whole_record_accepted=False,full_dependent_result_accepted=False,runs={})
    if issue:
        scoped['SEM_017_assessment']=dict(issue_status='resolved_in_exact_presented_scope',
            accepted='Correct source-local exception reference, kind, direction and explicitness.',
            full_execution_block='Retained where missing applicable target is required for actual further execution or unknown effects.',
            local_query='Known exception/prohibition/no-check with supplied qualifying facts does not depend on reconstructing absent general procedure.',
            original_declaration_adequacy='Broad true/affected source record is insufficient to distinguish these scopes; original edge/gap flags remain unchanged.',
            actual_wrong_played_outcome='not_demonstrated',automatic_FP_award=False)
    for run,x in row['runs'].items():
        t=x['output_trace'][row['id']]
        scoped['runs'][run]=dict(response=C['responses'][run],reviewer=reviewer,status='reviewed',result=scoped['result'],
            comparison_artifact=ref(PACK/'comparisons.json'),comparison_pointer=f'/relationships/{idx}/runs/{run}',
            edge_trace=copy.deepcopy(t),endpoint_traces={rid:dict(response=q['response'],pointer=q['pointer'],raw_span=q['raw_span']) for rid,q in x['output_trace'].items()},
            target_identity=x['target_identity'],direction=x['direction'],kind=x['kind'],explicitness=x['explicitness'],
            supplemental_supplied_context=x['supplemental_supplied_context'],missing_target_impact=x['missing_target_impact'],
            exclusions=x['exclusions'],uncertainties=x['uncertainties'],whole_record_accepted=False,full_result_accepted=False)
    scopes.append(scoped)
assert len(scopes)==30 and sum(len(x['runs']) for x in scopes)==60
decision=dict(id='M-POC5A-owner-decision-06',card='M-POC5A',part='M-POC5A.4b2',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,
    reviewer=reviewer,owner_reply_verbatim=reply,decision='accepted_both_presented_recommendations_52_bounded_plus8_scoped_exception_block_assessments',
    approval_evidence=ref(M/'approval-evidence.json'),prior_decision=ref(R/'owner-decision-05.json'),prior_state=ref(R/'current-state-12.json'),
    comparison_manifest=ref(PACK/'manifest.json'),presentation=ref(PACK/'presentation.json'),focused_packet=ref(PACK/'owner-focus.md'),
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],recommendations=recommendations,scopes=scopes,
    newly_decided_assigned_occurrences=60,per_answer={'first-001':30,'context-01':30},positive_bounded_occurrences=52,block_scope_assessment_occurrences=8,
    prior_owner_decided_assigned_scopes_preserved=125,owner_decided_assigned_scopes_total=185,remaining_assigned_scopes_without_owner_decision=72,
    issue_disposition={'SEM-017':'Resolved only for four presented local exception relations and block-scope adequacy; applicable full execution remains blocked by missing source.'},
    unresolved_prior_issue_ids=prior['inherited_issue_ids'],pending_expectation_ids=prior['pending_expectation_ids'],
    excluded=positive['excludes'],owner_file_open_or_read='unknown',metrics='not_assessable',no_response_changes=True,no_gold_change=True,
    new_extractions=0,new_sources=0,new_context_rounds=0,new_corrections=0,whole_card_closed=False)
save(R/'owner-decision-06.json',decision);dr=ref(R/'owner-decision-06.json')
overlay=copy.deepcopy(old)
overlay.update(id='M-POC5A-owner-review-overlay-06',decision=dr,prior_overlay=ref(R/'owner-review-overlay-05.json'),relationship_owner_decision=dr,
    prior_relationship_owner_decision=old['relationship_owner_decision'],accepted_relation_scoped_occurrences=185,
    newly_decided_scoped_occurrences_4b2=60,positive_bounded_occurrences_4b2=52,qualified_block_occurrences_4b2=8,
    pending_prior_issue_ids=decision['unresolved_prior_issue_ids'],pending_relation_ids_4b2=[],
    all_output_edges_review='185 assigned occurrences have accepted bounded components. Prior125 plus .4b2 positive52 and qualified block8; not185 whole correct edges.72 assigned .4b3 await full scoped review.',
    relation_scope_policy={'previous_policy':old['relation_scope_policy'],'part_4b2_presentation':pres,'decision':dr,
        'count_policy':'185 scoped occurrences with mixed component judgments; no whole record quality or final metrics.'})
overlay['issue_dispositions']['SEM-017']=decision['issue_disposition']['SEM-017']
for j in scopes:
    if j['id'] in special:
        overlay['relation_facet_decisions'].append(dict(id='SEM-017',edge=j['id'],assessment=j['SEM_017_assessment'],decision=dr,
            source_scope=j['source_scope'],target_scope=j['target_scope'],runs=j['runs']))
for run,v in overlay['runs'].items():
    for j in scopes:
        v['relationship_scopes'].append(dict({k:x for k,x in j.items() if k!='runs'},response=C['responses'][run],decision=dr,trace=j['runs'][run]))
    v['accepted_relation_scoped_occurrences']=len(v['relationship_scopes'])
    v['assigned_relation_occurrences_4b2']=30;v['pending_relation_occurrences_4b2']=0
    v['remaining_without_owner_relation_scope']=v['all_output_relation_occurrences']-len(v['relationship_scopes'])
assert len(overlay['runs']['first-001']['relationship_scopes'])==90 and len(overlay['runs']['context-01']['relationship_scopes'])==95
assert all(v['remaining_without_owner_relation_scope']==36 for v in overlay['runs'].values())
save(R/'owner-review-overlay-06.json',overlay)
state=copy.deepcopy(prior)
state.update(id='M-POC5A-current-state-13',part='M-POC5A.4b2-owner-review',previous_state=ref(R/'current-state-12.json'),decision=dr,overlay=ref(R/'owner-review-overlay-06.json'),
    owner_accepted_relationship_occurrences=185,owner_decided_assigned_relationship_occurrences=185,owner_pending_relationship_occurrences=72,
    owner_pending_relationship_occurrences_4b2=0,new_owner_decisions=[dr],newly_decided_assigned_occurrences=60,part_4b2_owner_review_complete=True,
    unresolved_issue_ids=decision['unresolved_prior_issue_ids'],
    owner_accepted_relationship_occurrences_policy='185 assigned scoped decisions:125 prior +52 positive bounded requirements +8 qualified exception/block-scope judgments. Not whole records/fully correct edges.',
    owner_pending_relationship_occurrences_policy='72 assigned .4b3 occurrences await full scoped review. Previous extra DEP-037 kind decision does not complete .4b3. Excluded fields of185 remain unaccepted.',
    next_action='Separate M-POC5A.4b3:36IDs/72occurrences; estimate before execution; preserve all remaining pending and excluded fields.',
    resume='Both .4b2 recommendations owner accepted:52 bounded roles/requirements +8 scoped exception/block judgments. Next separate .4b3:36IDs/72occurrences after estimate. No new source/extraction/correction; old SEM-001–013,8expectations and excluded fields remain open.')
state['issue_dispositions']['SEM-017']=decision['issue_disposition']['SEM-017']
state['summary'].update(new_owner_reviewed_occurrences=60,owner_pending_occurrences=0,owner_accepted_scoped_occurrences=60,
    owner_decided_assigned_scopes_total=185,owner_positive_scope_accepted_occurrences=52,owner_qualified_block_assessment_occurrences=8)
save(R/'current-state-13.json',state)
summary='''# Zatwierdzenie obu decyzji .4b2 — 2026-10-11

Właściciel odpowiedział „zatwierdxam” po dwóch konkretnych propozycjach.
Literówkę zachowano dosłownie; odpowiedź stanowi zatwierdzenie obu zakresów.
Nowy zapis: owner-decision-06, owner-review-overlay-06 i current-state-13.

1. Przyjęto26 ID /52 wystąpienia jako dokładne role odesłań i wymagania
   brakującego źródła. Nie przyjęto treści celu, aliasu lub pełnego wyniku.
2. Dla4 ID /8 wystąpień przyjęto powiązania wyjątków i zawężenie blokady:
   D914OW, D915superiority, D917position, D923pre. Nieznane dalsze wykonanie
   lub skutki nadal wymagają brakujących zasad. Sam wyjątek OW od priorytetu
   Rampage, lokalny zakaz AS/Position Superiority albo no-check przy zadanych
   właściwych uczestnikach i kierunkach są znane. Szeroka deklaracja blokady
   jest niewystarczająca do rozróżnienia tych zakresów. SEM-017 rozstrzygnięto
   tylko w tym zakresie; nie wykazano konkretnego błędnego wyniku gry.

Nowa decyzja dotyczy60 wystąpień, osobno30 first-001 i30 context-01.
Wcześniejsze125 zakresów zachowano; razem185 przypisanych wystąpień ma
decyzje o komponentach, a nie185 poprawnych całych relacji. Decyzja nie
zmienia oryginalnych flag edge/gap i nie przyznaje automatycznych FP/TP.

Pozostałe SEM-001–013 (w tym reszta SEM-004), osiem oczekiwań
EXP-010/017/019/040/050/052/066/074 oraz wyłączone pola i pełne wyniki
pozostają otwarte. Wcześniejsze decyzje SEM-014–016, po63 lokalne zakresy
i3 wymagania źródła na wynik oraz264 pary rubryka/EXP bez zmiany.
Faktyczne otwarcie/odczyt plików unknown; decyzja po wyjaśnieniu w czacie
jest odnotowana. Pełne TP/FP/FN/precision/recall nadal not_assessable.

Następna osobna M-POC5A.4b3:36 ID /72 wystąpienia po oszacowaniu.
Wąska wcześniejsza decyzja o wzmiance D961stack nie wykonuje całej .4b3.
M-POC5A/.4/.4b partial, M-POC5 jedyny next. Oryginały, źródła, eval-v1,
pakiety, decyzje i pomiary zachowano; bez nowych źródeł, ekstrakcji,
korekt, czatów, commit/push lub uruchomienia kolejnej partii.
'''
assert not (R/'owner-review-summary-06.md').exists()
(R/'owner-review-summary-06.md').write_text(summary,encoding='utf-8')
save(M/'decision-artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-06.json','owner-review-overlay-06.json','current-state-13.json','owner-review-summary-06.md']],
    newly_decided=60,positive=52,qualified_blocks=8))

aggregate='''Właściciel zatwierdził obie propozycje .4b2 odpowiedzią „zatwierdxam”.
Nowa owner-decision-06, overlay-06 i current-state-13 pod prywatnym
reviews/semantic-01/ zapisują52 ograniczone zakresy relacji i8 powiązań
wyjątków z zawężeniem blokady, osobno30/30 wystąpień obu odpowiedzi.
SEM-017 rozstrzygnięto w przedstawionym zakresie; nieznane pełne wykonanie
pozostaje zablokowane. Brakującego celu nie zastąpiono jego nazwą.

Wcześniejsze125 zakresów zachowano; łącznie185 przypisanych wystąpień ma
decyzje o dokładnych komponentach, nie185 poprawnych całych relacji.
SEM-001–013 w pozostałych zakresach, osiem wcześniejszych oczekiwań,
wyłączone pola, pełne wyniki i lokatory pozostają otwarte. Wcześniejsze
decyzje SEM-014–016, po63 lokalne zakresy/3 wymagania źródła na wynik
i264 pary rubryka/EXP bez zmiany. Pełne metryki nieocenialne; bez auto-FP/TP.
Faktyczne otwarcie/odczyt plików unknown; zgodę w czacie odnotowano.

Następna osobna .4b3:36 ID /72 wystąpienia według istniejącego scope-plan,
z oszacowaniem przed wykonaniem. Dodatkowa wcześniejsza decyzja o wzmiance
nie wykonuje całej .4b3. .4c/.4d i M-POC5B osobno. M-POC5A/.4/.4b partial,
M-POC5 jedyny next. Oryginały i dawne artefakty zachowano; bez nowych
źródeł, ekstrakcji, korekt, czatów lub commit/push. Zapis decyzji nie
uruchamia następnej partii. Pomiar: measurement/M-POC5A-owner-review-006/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4b','.4b2']]]
save(M/'public-documents-before.json',[ref(p) for p in files])
p=D/'STATUS.md';text=p.read_text(encoding='utf-8');lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):
        lines[i]='- **Wynik M-POC5A:** partial — właściciel zatwierdził .4b2:52 ograniczone zakresy i8 wyjątków z zawężeniem blokady; łącznie185 przypisanych wystąpień ma decyzje o komponentach; wcześniejsze nierozstrzygnięcia zachowane; następna osobna .4b3'
text='\n'.join(lines)+'\n';marker='## M-POC5A — rzeczywisty przegląd .4b2, 2026-10-11';assert marker in text
p.write_text(text.replace(marker,'## M-POC5A — zatwierdzenie .4b2, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md';text=p.read_text(encoding='utf-8')
needle='.4b2 porównana30 ID/60 wystąpień:52 ograniczone propozycje i8 do decyzji o blokadzie, wszystkie nowe pending; po decyzjach następna osobna .4b3'
assert needle in text
p.write_text(text.replace(needle,'.4b2 porównana30 ID/60 wystąpień i zatwierdzona w zakresie52 ról/wymagań oraz8 wyjątków z zawężeniem blokady; łącznie185 przypisanych zakresów z decyzjami; następna osobna .4b3',1),encoding='utf-8')
for p in files[3:]:p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Zatwierdzenie .4b2 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
handoff=D/'handoff/2026-10-11-M-POC5A-owner-review-06.md';assert not handoff.exists()
handoff.write_text('''# M-POC5A — zatwierdzenie obu decyzji .4b2

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca zapisu: Codex; znaczenie zatwierdził właściciel w tym czacie.
Wejścia i hashe obu oryginałów, eval-v1, pakietu .4b2 i poprzedniej decyzji
prowadzi prywatny owner-decision-06. Pełny zakres i wyłączenia w
owner-review-summary-06.md. Poprzedni pakiet i decyzje nie są nadpisane.

Kontrole, końcowy audyt i append-only pomiar: prywatny katalog
measurement/M-POC5A-owner-review-006/, completion.json i logi.
Szacunek zapisu10–20 minut; czas kalendarzowy w completion.json,
czas aktywny/tokeny/cena i zgodność budżetu unknown. Kontrole nie
poszerzają zakresu semantycznej decyzji. Brak nowych źródeł lub korekt;
dotychczasowe limity kontekstu i niewiadome izolacji pozostają bez zmiany.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n')
history=history.replace('[2026-10-11-M-POC5A-semantic-04b2](handoff/2026-10-11-M-POC5A-semantic-04b2.md)',
    '2026-10-11-M-POC5A-semantic-04b2 (`handoff/2026-10-11-M-POC5A-semantic-04b2.md`)',1)
p.write_text('''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-owner-review-06](handoff/2026-10-11-M-POC5A-owner-review-06.md)
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'\n## Historia przed zatwierdzeniem .4b2\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,handoff]])
print(json.dumps(dict(newly_decided=60,positive=52,qualified_blocks=8,total_scoped=185,remaining=72,protected=len(protected))))
