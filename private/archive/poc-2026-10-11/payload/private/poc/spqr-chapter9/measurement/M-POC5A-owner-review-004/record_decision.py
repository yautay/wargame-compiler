"""Record the human's bounded .4b1 acceptance additively, without new review."""
from pathlib import Path
from datetime import datetime, timezone
import copy,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent;REV=P/'reviews/semantic-01';PACK=REV/'part-04b1'
sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();reply='zatwierdzam'
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(part='M-POC5A.4b1-owner-review',recorded_at_utc=now,protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),owner_reply=reply,owner_message_sent_at_utc='unknown'))
C=load(PACK/'comparisons.json');presentation=load(PACK/'presentation.json');previous=load(REV/'current-state-09.json')
for a in list(C['responses'].values())+[C['evaluation'],C['source']]:assert ref(ROOT/a['path'])==a
for a in load(PACK/'manifest.json')['artifacts']:assert ref(ROOT/a['path'])==a
save(M/'approval-evidence.json',dict(date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,owner_reply_verbatim=reply,
    preceding_offer_verbatim='Proponuję przyjąć 116 wystąpień w dokładnie opisanych zakresach.',
    prior_explanation_basis=[ref(PACK/'owner-focus.md'),ref(PACK/'comparisons.md'),ref(PACK/'presentation.json')],
    preceding_chat_summary='Positive116 bounded occurrences; allocation block, SK new relation, missing critical/mention records and kind classification kept separate. No old unresolved choice selected.',
    interpretation='Direct assent to the presented positive scope only, preserving explicit exclusions and separate unresolved decisions. Does not accept all125occurrences, complete records or full quality.',
    actual_owner_file_open_or_read='unknown',owner_message_sent_at_utc='unknown'))
positive=presentation['positive_scope'];ids=positive['ids'];assert len(ids)==60 and len(set(ids))==60
reviewer='owner in this chat; personal identity unknown';scopes=[]
for row_index,row in enumerate(C['relationships']):
    if row['id'] not in ids:continue
    scoped=dict(id=row['id'],source_scope=row['source_scope'],target_scope=row['target_scope'],source_evidence=row['source_evidence'],target_evidence=row['target_evidence'],
        necessity_or_occurrence_scope=row['necessity_and_missing_impact'],evaluator_comparison=row['proposal'],
        accepted_components=positive['includes'],excluded_components=positive['excludes'],whole_record_accepted=False,full_dependent_result_accepted=False,
        reviewer=reviewer,recorded_at_utc=now,status='reviewed',result='correct_in_owner_accepted_scope',runs={})
    for run,x in row['runs'].items():
        if not x['record_present']:continue
        t=x['output_trace'][row['id']]
        scoped['runs'][run]=dict(response=x['response'],reviewer=reviewer,status='reviewed',result='correct_in_owner_accepted_scope',
            comparison_artifact=ref(PACK/'comparisons.json'),comparison_pointer=f'/relationships/{row_index}/runs/{run}',
            source_scope=x['source_scope'],target_identity=x['target_identity'],target_scope=x['target_scope'],bounded_independent_source=x['bounded_independent_source'],
            direction=x['direction'],kind=x['kind'],explicitness=x['explicitness'],
            edge_pointer=t['pointer'],edge_raw_span=t['raw_span'],edge_field_trace=t['fields'],
            output_trace={q:dict(response=v['response'],pointer=v['pointer'],raw_span=v['raw_span']) for q,v in x['output_trace'].items()},
            exclusions=x['exclusions']+positive['excludes'],uncertainties=x['uncertainties'],
            missing_target_impact_acceptance='Only exact necessity/missing-scope discussed; generic impact=false for necessary source-present targets remains excluded.',
            whole_record_accepted=False,full_result_accepted=False)
    scopes.append(scoped)
counts={r:sum(r in s['runs'] for s in scopes) for r in C['responses']};assert counts=={'first-001':56,'context-01':60}
assert sum(counts.values())==116
decision=dict(id='M-POC5A-owner-decision-04',card='M-POC5A',part='M-POC5A.4b1',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,
    reviewer=reviewer,owner_reply=reply,owner_message_sent_at_utc='unknown',decision='accepted_exact_positive60IDs_116occurrences_in_supplied_bounded_scopes',
    interpretation_basis='Assent to immediately preceding116-positive offer and linked plain-language scope; all separately named issues and earlier pending stay open.',
    approval_evidence=ref(M/'approval-evidence.json'),evaluation=C['evaluation'],responses=C['responses'],source=C['source'],prior_decision=ref(REV/'owner-decision-03.json'),
    prior_state=ref(REV/'current-state-09.json'),comparison_manifest=ref(PACK/'manifest.json'),presentation=ref(PACK/'presentation.json'),focused_packet=ref(PACK/'owner-focus.md'),
    accepted_relation_ids=ids,accepted_scoped_occurrences=116,per_answer=counts,scopes=scopes,
    separate_issue_edge_ids=C['summary']['separate_issue_ids'],separate_issue_occurrences=9,unresolved_issue_ids=[f'SEM-{n:03}' for n in range(1,17)],
    excluded=positive['excludes']+['D961stack/DEP-037 separate kind decision','Missing tuples not automatically semanticFN','No implicit gold acceptance or missing-pair repair','No acquisition of missing target source or closure of blocking full outcome'],
    accepted_frozen_scopes_already_inside_116=dict(explicit_ids=presentation['proposed_frozen_scope']['explicit_ids'],mention_ids=presentation['proposed_frozen_scope']['mention_ids'],physical_continuation_ids=presentation['proposed_frozen_scope']['physical_continuation_ids'],extra_output_points=0),
    missing_record_observations_retained=presentation['proposed_frozen_scope']['missing_record_and_retained_prose_observations'],
    owner_file_open_or_read='unknown',new_extractions=0,new_corrections=0,new_sources=0,no_gold_change=True,metrics='not_assessable',
    M_POC5A_closed=False,M_POC5A_4_closed=False,M_POC5A_4b_closed=False)
save(REV/'owner-decision-04.json',decision);dr=ref(REV/'owner-decision-04.json')
old=load(REV/'owner-review-overlay-03.json');overlay=copy.deepcopy(old)
overlay.update(id='M-POC5A-owner-review-overlay-04',decision=dr,prior_overlay=ref(REV/'owner-review-overlay-03.json'),
    expectation_owner_decision=ref(REV/'owner-decision-03.json'),relationship_owner_decision=dr,
    all_output_edges_review='partially_owner_reviewed_in_exact_scopes; full records and unresolved fields remain unaccepted',
    pending_prior_issue_ids=[f'SEM-{n:03}' for n in range(1,17)],pending_relation_ids_4b1=C['summary']['separate_issue_ids'],
    relation_scope_policy=positive,accepted_relation_scoped_occurrences=116,whole_record_acceptance=False,full_relation_precision_recall='not_assessable')
for run,v in overlay['runs'].items():
    v['relationship_scopes']=[dict({k:val for k,val in s.items() if k!='runs'},response=C['responses'][run],decision=dr,trace=s['runs'][run]) for s in scopes if run in s['runs']]
    v['accepted_relation_scoped_occurrences']=counts[run]
    v['assigned_relation_occurrences_4b1']=C['summary']['assigned_occurrences_per_answer'][run]
    v['pending_relation_occurrences_4b1']=v['assigned_relation_occurrences_4b1']-counts[run]
    v['all_output_relation_occurrences']=126 if run=='first-001' else 131
    v['remaining_without_owner_relation_scope']=v['all_output_relation_occurrences']-counts[run]
assert len(overlay['category_units'])==264 and overlay['pending_expectation_ids']==old['pending_expectation_ids']
save(REV/'owner-review-overlay-04.json',overlay)
state=copy.deepcopy(previous)
state.update(id='M-POC5A-current-state-10',part='M-POC5A.4b1-owner-review',previous_state=ref(REV/'current-state-09.json'),decision=dr,overlay=ref(REV/'owner-review-overlay-04.json'),
    expectation_owner_decision=ref(REV/'owner-decision-03.json'),owner_accepted_relationship_occurrences=116,
    owner_accepted_relationship_occurrences_policy='Only exact scoped components; not whole records or full semantics. Excluded fields in accepted edges remain open.',
    owner_pending_relationship_occurrences=141,owner_pending_relationship_occurrences_policy='Occurrences without any accepted positive relation scope:9in4b1+132in4b2/3; excluded fields of116also remain pending separately.',
    owner_pending_relationship_occurrences_4b1=9,all_relations_and_locators_pending=False,full_relation_record_review_incomplete=True,all_locator_review_pending=True,new_owner_decisions=[dr],
    unresolved_issue_ids=[f'SEM-{n:03}' for n in range(1,17)],
    resume='Positive .4b1 scope accepted:56first/60context occurrences. SEM-001–016,5issue IDs/9occurrences, all8prior expectations remain open. Next separate .4b2 with30IDs/60occurrences from existing plan; estimate/split before review. .4b3/.4c/.4d later. No new extraction/answer corrections/source.')
state['summary'].update(new_human_reviewed_occurrences=116,owner_accepted_scoped_occurrences=116,owner_pending_occurrences=9,owner_actual_open_or_read='unknown')
save(REV/'current-state-10.json',state)
summary='''# Akceptacja pozytywnego zakresu .4b1 — 2026-10-11

Właściciel odpowiedział „zatwierdzam” po opisie wyników po ludzku i propozycji
przyjęcia 116 wystąpień w dokładnie opisanych zakresach. Zapisano nową
owner-decision-04.json; oryginalny pakiet part-04b1 i wcześniejsze decyzje
zachowano. Faktyczne otwarcie/odczyt plików pozostaje unknown.

Przyjęto 60 różnych ID: 56 zakresów first-001 i 60 context-01, razem 116.
Akceptacja obejmuje tylko wskazany source/target scope, kierunek, rodzaj,
jawność oraz konieczność lub rolę odniesienia. Cel unresolved oznacza jedynie
nazwane wymaganie/brak/blokadę, bez treści celu lub ustalenia aliasu.
Blankietowe impact=false dla koniecznych dostępnych celów, całe rekordy,
pełne wyniki i wydzielone nierozstrzygnięcia pozostają wyłączone.

5 ID / 9 wystąpień .4b1 nadal pending; osobna różnica rodzaju frozenmention
także otwarta. SEM-001–016 i osiem wcześniejszych oczekiwań zachowano.
Trzy brakujące krytyczne pary i cztery wzmianki nie zostały dopisane ani
automatycznie uznane za semantyczne FN. Pozytywne zamrożone zakresy 5 jawnych
par, 2 wzmianek i 7 kontynuacji już mieszczą się w 116 i nie dają nowych punktów.

Stan prowadzi current-state-10.json i owner-review-overlay-04.json.
Wcześniejsze po 63 lokalne zakresy i 3 wymagania źródła na wynik oraz
264 pary rubryka/EXP bez zmiany. Relacje bez przyjętego pozytywnego zakresu:
141 wystąpień = 9 w .4b1 + 132 w .4b2/.4b3. Wyłączone pola przyjętych relacji
także pozostają otwarte. Pełne TP/FP/FN/precision/recall not_assessable;
105 candidates nie staje się gold, brak zamknięcia całego grafu lub budżetu.

Następna osobna .4b2: 30 ID / 60 wystąpień według istniejącego scope-plan,
z oszacowaniem przed wykonaniem. .4b3/.4c/.4d i 20 sytuacji M-POC5B osobno.
M-POC5A/.4/.4b partial, M-POC5 jedyny next. Bez nowych źródeł, ekstrakcji,
korekt, czatów lub commit/push; zapis decyzji nie uruchamia następnej partii.
'''
f=REV/'owner-review-summary-04.md';assert not f.exists();f.write_text(summary,encoding='utf-8')
save(M/'decision-artifacts.json',dict(artifacts=[ref(REV/f) for f in ['owner-decision-04.json','owner-review-overlay-04.json','current-state-10.json','owner-review-summary-04.md']],scope_acceptance='actual_owner_exact_scope',counts=counts))
print(json.dumps(dict(accepted_scoped_occurrences=116,per_answer=counts,pending_4b1=9,pending_without_scope_all_relations=141,pending_expectations=8,protected_files=len(protected))))
