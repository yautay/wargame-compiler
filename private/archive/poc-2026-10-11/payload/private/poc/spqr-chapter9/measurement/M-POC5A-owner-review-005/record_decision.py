"""Record six explicitly approved recommendations; never change response bytes."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
M = Path(__file__).resolve().parent
R = P / 'reviews/semantic-01'
PACK = R / 'part-04b1'

def load(path):
    return json.loads(path.read_bytes())

def ref(path):
    b = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def save(path, value):
    assert not path.exists(), path
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

now = datetime.now(timezone.utc).isoformat()
protected = [ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f != P/'measurement/sessions.jsonl']
save(M/'start.json', dict(recorded_at_utc=now, card='M-POC5A', part='M-POC5A.4b1-owner-review',
    estimate_minutes=[10,20], estimate_scope='Record six existing owner-approved recommendations and verify; no new semantic batch.',
    protected=protected, sessions_before=ref(P/'measurement/sessions.jsonl'), owner_reply_verbatim='zgodnie z rekomendacją'))
C = load(PACK/'comparisons.json')
old = load(R/'owner-review-overlay-04.json')
state = load(R/'current-state-10.json')
for a in [C['evaluation'], C['source'], *C['responses'].values()]:
    assert ref(ROOT/a['path']) == a
for a in load(PACK/'manifest.json')['artifacts']:
    assert ref(ROOT/a['path']) == a

recommendations = [
 dict(number=1, issue='SEM-014', edge='D9621013', accepted=['source/target identity', 'direction', 'explicit procedure use'],
      decision='Przyjąć poprawność odesłania do 10.13; deklarację blokady na tej relacji uznać za niewystarczającą.',
      rejected_original_facets={'impact_if_missing': 'false and empty gap list fail to convey the nested missing within-stack allocation rule'},
      expected_kind='procedure_use', expected_explicitness='explicit',
      limits='Block exists elsewhere in answer. Missing 6.68 #6 still blocks full within-stack allocation. No actually wrong allocation asserted. Other edges generic false remain outside this decision.'),
 dict(number=2, issue='SEM-004', edge='DCTX923-S4', accepted=['bounded source/target', 'direction', 'implicit operation correspondence', 'attacker Hits half/floor/cap1 when selected defender is SK'],
      decision='Przyjąć wąskie niejawne powiązanie potwierdzające operację; dodatkowy fragment nie jest niezbędny do lokalnego pół/floor/cap1.',
      rejected_original_facets={}, expected_kind='procedure_use', expected_explicitness='implicit',
      necessity='supporting correspondence, not necessary for the local operator already supplied in 9.23',
      limits='Requires selected defender SK. Mere SK presence in mixed defense is insufficient. Full combat, source lookup, participant selection and remaining SEM-004 stay open. procedure_use accepted only in this supporting correspondence scope, without blanket execution necessity.'),
 dict(number=3, issue='SEM-015', edge='D961stack', accepted=['referring direction', 'named Stacking Charts occurrence', 'explicitness'],
      decision='Wystąpienie see for a summary to wzmianka; table_use modelu ma błędny rodzaj w tym zakresie.',
      rejected_original_facets={'kind': 'table_use'}, expected_kind='mention', expected_explicitness='explicit',
      limits='Only frozen DEP-037 mention occurrence. No chart content, alias resolution, full stacking, impact-field acceptance, whole record, full .4b3 review or TP/FP count.'),
 dict(number=4, issue='SEM-016', edge='D9161011', accepted=['target identity', 'source/target scope', 'direction'],
      decision='Cel i kierunek poprawne; potrzebne jest użycie procedury testu TQ, nie tylko definicja.',
      rejected_original_facets={'kind': 'definition'}, expected_kind='procedure_use', expected_explicitness=None,
      limits='Local relation only; EXP-017 DR<=TQ branch and E916 locator remain open. No response correction.'),
 dict(number=5, issue='SEM-016', edge='D967966', accepted=['source/target scope', 'direction', 'MLE operation and preserved conditions'],
      decision='Odesłanie jest jawne przez nazwę operacji MLE; numer przepisu nie jest wymagany dla jawnego nazwanego odwołania.',
      rejected_original_facets={'explicitness': 'implicit'}, expected_kind=None, expected_explicitness='explicit',
      classification_convention='Named operation use may be explicit without a printed rule number. No automatic reclassification of other records.',
      limits='Exact named MLE use only; no acceptance of unrelated fields or complete reaction outcome.'),
 dict(number=6, issue='SEM-016', edge='D968column', accepted=['source/target scope', 'direction', 'local in-Column MLE prohibition'],
      decision='Zakaz MLE w Column jest warunkiem dopuszczalności; mention modelu ma błędny rodzaj.',
      rejected_original_facets={'kind': 'mention'}, expected_kind='condition', expected_explicitness=None,
      limits='Exact in-Column exclusion only; no reclassification of other maneuver prohibitions.')
]
save(M/'approval-evidence.json', dict(owner_reply_verbatim='zgodnie z rekomendacją',
    preceding_assistant_offer='Możesz odpowiedzieć np. „przyjmuję rekomendacje 1–6” albo wskazać numery i własne rozstrzygnięcia.',
    preceding_recommendations=copy.deepcopy(recommendations), interpretation='Direct assent to all six recommendations immediately presented in chat.',
    recorded_at_utc=now, message_sent_at_utc='unknown', actual_owner_file_open_or_read='unknown',
    source_packet=[ref(PACK/'owner-focus.md'), ref(PACK/'issues.json'), ref(PACK/'comparisons.json')]))

reviewer = 'owner in this chat; personal identity unknown'
judgments = []
for rec in recommendations:
    extra = rec['edge'] == 'D961stack'
    collection = 'frozen_tuple_comparisons' if extra else 'relationships'
    row_index, row = next((i, x) for i, x in enumerate(C[collection]) if x['id'] == ('DEP-037' if extra else rec['edge']))
    j = copy.deepcopy(rec)
    j.update(status='reviewed_in_decided_scope', reviewer=reviewer, recorded_at_utc=now,
        whole_record_accepted=False, full_dependent_result_accepted=False,
        comparison_artifact=ref(PACK/'comparisons.json'), comparison_pointer=f'/{collection}/{row_index}',
        extra_frozen_scope=extra, runs={})
    if extra:
        j['frozen_record'] = row['frozen_record']
        j['evaluation_pointer'] = row['evaluation_pointer']
    else:
        for k in ['source_scope','target_scope','source_evidence','target_evidence','necessity_and_missing_impact']:
            j[k] = row[k]
    for run, x in row['runs'].items():
        if not extra and not x['record_present']:
            continue
        trace = x['output_trace'][rec['edge']]
        j['runs'][run] = dict(response=C['responses'][run], trace=copy.deepcopy(trace),
            endpoint_traces={key:dict(response=t['response'],pointer=t['pointer'],raw_span=t['raw_span']) for key,t in x['output_trace'].items()},
            comparison_pointer=f'/{collection}/{row_index}/runs/{run}',
            original_kind=trace['original_record']['kind'], original_explicitness=trace['original_record']['explicitness'],
            original_impact=trace['original_record']['impact_if_missing'],
            result='correct_in_accepted_components_with_original_facets_rejected' if rec['rejected_original_facets'] else 'correct_in_bounded_supporting_scope',
            scope_limits=rec['limits'], whole_record_accepted=False, full_result_accepted=False)
    judgments.append(j)
counts = {run:sum(run in j['runs'] for j in judgments if not j['extra_frozen_scope']) for run in C['responses']}
assert counts == {'first-001':4,'context-01':5}
assert sum(len(j['runs']) for j in judgments) == 11
decision = dict(id='M-POC5A-owner-decision-05', card='M-POC5A', part='M-POC5A.4b1', date='2026-10-11', timezone='Europe/Warsaw',
    recorded_at_utc=now, reviewer=reviewer, owner_reply_verbatim='zgodnie z rekomendacją',
    decision='accepted_recommendations_1_to_6_in_exact_presented_scopes', approval_evidence=ref(M/'approval-evidence.json'),
    prior_decision=ref(R/'owner-decision-04.json'), prior_state=ref(R/'current-state-10.json'), evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
    judgments=judgments, newly_decided_assigned_occurrences=9, per_answer=counts, extra_frozen_mention_occurrences=2,
    prior_positive_scope_occurrences_unchanged=116, assigned_scoped_review_total=125,
    original_facet_issue_occurrences_assigned=8, original_kind_issue_occurrences_extra=2,
    issue_dispositions={'SEM-014':'resolved only for D9621013 identity/direction/use and insufficient edge block declaration; full allocation still blocked',
        'SEM-015':'resolved for DEP-037 occurrence classification only', 'SEM-016':'resolved for three exact classification scopes only',
        'SEM-004':'partially resolved for DCTX923-S4 supporting operator correspondence; remaining earlier scope pending'},
    unresolved_prior_issue_ids=[f'SEM-{n:03}' for n in range(1,14)], pending_expectation_ids=old['pending_expectation_ids'],
    excluded=['Whole original records', 'Unreviewed or previously excluded fields', 'Blanket impact=false on other necessary supplied targets',
        'Full dependent outcomes', 'External aliases, chart content, ratings/setup', 'Locators, E916 and glyph boundaries',
        'Missing-record repair or automatic semantic FN', 'Gold extension or final TP/FP/FN/precision/recall'],
    owner_file_open_or_read='unknown', no_response_changes=True, no_gold_change=True, metrics='not_assessable',
    new_extractions=0,new_sources=0,new_corrections=0, whole_card_closed=False)
save(R/'owner-decision-05.json', decision)
dr = ref(R/'owner-decision-05.json')
overlay = copy.deepcopy(old)
overlay.update(id='M-POC5A-owner-review-overlay-05', decision=dr, prior_overlay=ref(R/'owner-review-overlay-04.json'),
    relationship_owner_decision=dr, prior_relationship_owner_decision=old['relationship_owner_decision'],
    pending_prior_issue_ids=decision['unresolved_prior_issue_ids'], pending_relation_ids_4b1=[],
    accepted_relation_scoped_occurrences=125, previously_accepted_positive_occurrences=116,
    newly_decided_mixed_scope_occurrences=9, relation_facet_decisions=judgments, extra_frozen_mention_decided_occurrences=2,
    issue_dispositions=decision['issue_dispositions'],
    all_output_edges_review='Assigned .4b1 scopes decided:116 previous positive +9 mixed decisions; full records/excluded fields still unaccepted. Extra DEP-037 kind decided, not full .4b3.',
    relation_scope_policy={'previous_positive_scope':old['relation_scope_policy'],'additional_decision':dr,
        'count_policy':'125 occurrences have accepted components; only116 are previous positive scopes. Nine new decisions have mixed facet judgments; not125 wholly correct edges.'})
for run, v in overlay['runs'].items():
    for j in judgments:
        if j['extra_frozen_scope'] or run not in j['runs']:
            continue
        v['relationship_scopes'].append(dict(id=j['edge'], status='reviewed', reviewer=reviewer, decision=dr,
            accepted_components=j['accepted'], rejected_original_facets=j['rejected_original_facets'],
            expected_kind=j['expected_kind'], expected_explicitness=j['expected_explicitness'],
            source_scope=j['source_scope'], target_scope=j['target_scope'], source_evidence=j['source_evidence'],target_evidence=j['target_evidence'],
            excluded_components=[j['limits'], *decision['excluded']],trace=j['runs'][run],
            whole_record_accepted=False,full_dependent_result_accepted=False,result=j['runs'][run]['result']))
    v['accepted_relation_scoped_occurrences'] = len(v['relationship_scopes'])
    v['pending_relation_occurrences_4b1'] = 0
    v['remaining_without_owner_relation_scope'] = v['all_output_relation_occurrences'] - len(v['relationship_scopes'])
assert len(overlay['runs']['first-001']['relationship_scopes']) == 60
assert len(overlay['runs']['context-01']['relationship_scopes']) == 65
save(R/'owner-review-overlay-05.json', overlay)
state.update(id='M-POC5A-current-state-11', previous_state=ref(R/'current-state-10.json'),decision=dr,overlay=ref(R/'owner-review-overlay-05.json'),
    owner_accepted_relationship_occurrences=125, owner_pending_relationship_occurrences=132,owner_pending_relationship_occurrences_4b1=0,
    owner_accepted_relationship_occurrences_policy='125 assigned occurrences have accepted bounded components:116 prior positive,9 newly decided mixed facets. This does not count125 fully correct edges.',
    owner_pending_relationship_occurrences_policy='132 assigned occurrences of .4b2/3 await full scoped review; D961stack has only extra DEP-037 mention classification decided. Excluded fields in decided occurrences remain unaccepted.',
    owner_decided_assigned_relationship_occurrences=125,newly_decided_assigned_occurrences=9,extra_frozen_mention_decided_occurrences=2,
    unresolved_issue_ids=decision['unresolved_prior_issue_ids'],issue_dispositions=decision['issue_dispositions'],new_owner_decisions=[dr],
    resume='Next separate M-POC5A.4b2:30IDs/60occurrences; estimate before review. Six recommendations decided with mixed judgments; .4b1 scoped decisions125, extra DEP-037 kind only2. Preserve remaining SEM-004, prior SEM-001–013, all8expectations and excluded fields. No extraction/correction/new source.')
state['summary'].update(new_human_reviewed_occurrences=9,owner_decided_assigned_occurrences_total=125,
    owner_accepted_scoped_occurrences=125,previous_positive_scopes_unchanged=116,new_mixed_scoped_decisions=9,
    owner_pending_occurrences=0,extra_frozen_mention_decided_occurrences=2)
save(R/'current-state-11.json', state)
summary = '''# Decyzje właściciela 1–6 — 2026-10-11

Właściciel odpowiedział „zgodnie z rekomendacją” po sześciu konkretnych
rekomendacjach w czacie. Zapisano owner-decision-05.json, overlay-05 i stan11.

1. D9621013: poprawne odesłanie do 10.13; deklaracja blokady na relacji
   niewystarczająca. Brak 6.68 #6 nadal blokuje podział wewnątrz stosu.
   Nie stwierdzono konkretnego błędnego rozdziału strat.
2. DCTX923-S4: przyjęto niejawne powiązanie potwierdzające pół/floor/cap1
   dla Hits atakującego, gdy wybranym obrońcą jest SK. Dodatkowy fragment
   nie jest niezbędny do lokalnej operacji już zapisanej w 9.23. Samo SK
   w mieszanej obronie nie wystarcza. Reszta SEM-004 nadal otwarta.
3. D961stack / DEP-037: odesłanie do podsumowania jest wzmianką;
   table_use jest błędnym rodzajem w tym wystąpieniu. Nie oceniono całej .4b3.
4. D9161011: właściwy cel i kierunek; rodzaj procedure_use zamiast definition.
   EXP-017 oraz lokator E916 bez rozstrzygnięcia.
5. D967966: nazwana operacja MLE jest jawnym odwołaniem mimo braku numeru;
   implicit modelu nie jest poprawną klasyfikacją tego wystąpienia.
6. D968column: zakaz MLE w Column jest warunkiem dopuszczalności;
   mention modelu jest błędnym rodzajem w tym zakresie.

SEM-014/015/016 rozstrzygnięto tylko w opisanych zakresach; SEM-004 częściowo.
SEM-001–013 i osiem wcześniejszych oczekiwań pozostają otwarte w pozostałych
zakresach. Pozostałe wyłączone pola, w tym ogólne false na innych relacjach,
nie otrzymują akceptacji. Pełne wyniki i TP/FP/FN/precision/recall nieocenialne.

116 wcześniejszych pozytywnych zakresów bez zmiany. Nowa decyzja dotyczy
9 przypisanych wystąpień (4 first / 5 context) z ocenami mieszanymi oraz
2 dodatkowych wystąpień zamrożonej wzmianki. Łącznie 125 przypisanych
wystąpień .4b1 ma decyzje o dokładnych zakresach, a nie 125 poprawnych całych
relacji. Nowe decyzje odnotowują 8 wystąpień z błędem klasyfikacji lub
niewystarczającą deklaracją blokady w .4b1 oraz 2 z różnicą rodzaju wzmianki.
Nie są to automatyczne FP ani nowe punkty gold.

Następna osobna .4b2: 30 ID / 60 wystąpień po oszacowaniu. Pozostałe .4b2/3:
132 wystąpienia do pełnego scoped review, mimo wąskiej dodatkowej decyzji
o D961stack. M-POC5A/.4/.4b partial, M-POC5 jedyny next.
Oryginały, źródła, stare decyzje i pakiet porównań zachowano; bez nowych
źródeł, ekstrakcji, korekt, czatów, commit/push lub wykonania kolejnej partii.
'''
assert not (R/'owner-review-summary-05.md').exists()
(R/'owner-review-summary-05.md').write_text(summary,encoding='utf-8')
save(M/'decision-artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-05.json','owner-review-overlay-05.json','current-state-11.json','owner-review-summary-05.md']],counts=counts))
print(json.dumps(dict(recommendations=6,new_assigned_decisions=9,extra_mention=2,assigned_scoped_total=125,protected=len(protected))))
