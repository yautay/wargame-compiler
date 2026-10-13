"""Close additive packet metadata, state and public handoff; no owner decisions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01';OUT=REV/'part-04b1'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
S=load(M/'packet-summary.json');C=load(OUT/'comparisons.json')
# Explicit positive acceptance objects name components rather than accepting whole edges.
save(OUT/'presentation.json',dict(id='M-POC5A.4b1-presentation-01',date='2026-10-11',timezone='Europe/Warsaw',reviewer='Codex; proposals only',
    packet='owner-focus.md',comparisons='comparisons.md',complete_traces='comparisons.json',
    delivery_method='Prepared local files; open_in_codex result separately recorded, plus final chat links. This does not attest actual owner opening/reading.',
    shown_packet_scope=dict(assigned_ids=65,assigned_occurrences=125,extra_frozen_tuples=22,answers=2),actual_owner_opened_or_read='unknown',new_human_reviewed=0,pending_occurrences=125,
    positive_scope=dict(ids=S['positive_bounded_ids'],occurrences=116,per_answer={'first-001':56,'context-01':60},
        includes='Only evaluator-authored source_scope, target_scope, direction, kind/explicitness and necessity/occurrence role in comparisons.json for each ID and available answer. For unresolved targets only named candidate/absence/block scope, not target contents/alias identity.',
        excludes=['Whole output record or full result','Blanket impact=false for necessary source-present targets','SEM-001–016 unresolved components','R932 new exception field/AS-LC order/full SEM-003','Actual ratings/setup/20 situations','Glyph/locator and full graph acceptance']),
    separate_decisions=[dict(id='SEM-004',edge_ids=['DCTX923-S4'],status='waiting_review'),dict(id='SEM-014',edge_ids=['D9621013'],status='waiting_review'),dict(id='SEM-015',frozen_id='DEP-037',edge_ids=['D961stack'],status='waiting_review'),dict(id='SEM-016',edge_ids=['D9161011','D967966','D968column'],status='waiting_review')],
    proposed_frozen_scope=dict(explicit_ids=['DEP-002','DEP-008','DEP-017','DEP-024','DEP-041'],mention_ids=['DEP-044','DEP-063'],physical_continuation_ids=[f'DEP-{n:03}' for n in range(90,97)],
        missing_record_and_retained_prose_observations=['DEP-NEW-001','DEP-NEW-002','DEP-NEW-003','DEP-034','DEP-035','DEP-043','DEP-067-1'],automatic_FN=False),
    prior_owner_state='63 local scopes /3 source requirements per answer;8 expectations pending; unchanged',instruction_is_acceptance=False,owner_decisions=[]))
save(OUT/'manifest.json',dict(id='M-POC5A.4b1-packet-manifest',date='2026-10-11',evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
    artifacts=[ref(OUT/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],
    authorship=ref(M/'annotations.json'),scope_plan=C['scope_plan'],previous_state=C['previous_state'],semantic_acceptance='not_performed_for_new_scopes',owner_decisions=[]))
old=load(REV/'current-state-08.json')
state=dict(id='M-POC5A-current-state-09',card='M-POC5A',part='M-POC5A.4b1',next_part='M-POC5A.4b2',status='partial_waiting_review',previous_state=ref(REV/'current-state-08.json'),
    decision=old['decision'],overlay=old['overlay'],evaluation=old['evaluation'],responses=old['responses'],proposal_overlay=ref(OUT/'manifest.json'),summary=S,
    owner_accepted_local_groups_per_answer=63,reviewed_context_requirements_per_answer=3,remaining_pending_expectations=8,pending_expectation_ids=old['pending_expectation_ids'],pending_local_ids=old['pending_local_ids'],pending_context_ids=old['pending_context_ids'],
    evaluator_compared_relationship_occurrences=125,owner_accepted_relationship_occurrences=0,owner_pending_relationship_occurrences=257,remaining_uncompared_relationship_occurrences=132,
    remaining_uncompared_expectations=0,new_owner_decisions=[],all_relations_and_locators_pending=True,context_requirements_still_block_full_results=True,
    inherited_issue_ids=[f'SEM-{n:03}' for n in range(1,14)],new_issue_ids=['SEM-014','SEM-015','SEM-016'],
    M_POC5A_closed=False,M_POC5A_4_closed=False,M_POC5A_4b_closed=False,parts_4b2_4b3_4c_4d_not_executed=True,
    resume='Owner exact-scope decisions for positive116occurrences and SEM-004/014/015/016, all earlier pending preserved. Then separate .4b2 with existing30IDs/60occurrences, estimate/split before execution. .4b3/.4c/.4d later. No answer edits, extraction, sources/pass02 or automatic FN.')
save(REV/'current-state-09.json',state)
# Public files carry only aggregate method/outcome, no publisher rules or detailed graph.
docs=['docs/STATUS.md','docs/ROADMAP.md','docs/HANDOFF.md','docs/work/tasks/M-POC5A.md','docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4b.md','docs/work/tasks/semantic/M-POC5A.4b1.md']
save(M/'public-docs-before.json',dict(files=[dict(**ref(ROOT/f),text=(ROOT/f).read_text(encoding='utf-8-sig')) for f in docs]))
status=ROOT/'docs/STATUS.md';text=status.read_text(encoding='utf-8-sig')
old_line='- **Wynik M-POC5A:** partial — 63 lokalne zakresy i 3 wymagania źródła w obu wynikach; 8 oczekiwań pending; .4b podzielona przed wykonaniem, następna osobna .4b1'
assert old_line in text
text=text.replace(old_line,'- **Wynik M-POC5A:** partial — .4b1 porównana: 65 ID / 125 wystąpień i 22 dodatkowe zamrożone pary na wynik; nowa akceptacja waiting_review; .4b2 następna osobno; wcześniejsze 63/3 i 8 pending bez zmiany',1)
marker='## M-POC5A — prompt do dużej partii .4b1, 2026-10-11'
assert marker in text
update='''## M-POC5A — rzeczywisty przegląd .4b1, 2026-10-11

Wykonano źródłowe porównania wszystkich 65 przypisanych ID, osobno dla
60/65 wystąpień odpowiedzi (125), oraz 22 zamrożonych par na wynik.
Prywatny pakiet part-04b1 zawiera comparisons.json/.md, review, issues,
owner-focus, presentation i manifest. Oceny mają źródła, dokładne zakresy
i ślady do bajtów obu oryginałów; szacunek 75–90 minut zapisano przed review.

60 ID / 116 wystąpień ma pozytywne propozycje w ograniczonych zakresach;
5 ID / 9 wystąpień wymaga osobnych decyzji. Dodatkowe zamrożone porównania
zachowują 3 krytyczne brakujące rekordy, 4 brakujące wzmianki i różnicę
rodzaju. Treść w prozie oceniono osobno, bez automatycznego semantycznego FN.
Nowe SEM-014–016 oraz wcześniejsze SEM-001–013 waiting_review. Pozytywne
zakresy nie obejmują całych rekordów ani blankietowych deklaracji blokady.

Udostępniony zakres pakietu: 125 wystąpień; oceniający porównał 125;
nowe oceny właściciela 0, pending 125. Faktyczny odczyt/otwarcie unknown.
Stan additive current-state-09.json; owner-decision-03/overlay-03 bez zmiany.
Nadal po 63 lokalne zakresy / 3 wymagania źródła przyjęte na wynik,
8 oczekiwań pending. Pełne TP/FP/FN/precision/recall i aktywny budżet
nieocenione. 105 kandydatur nie staje się gold. Nadrzędne karty partial.

Pozostałe .4b2/.4b3 mają 30/36 ID i 60/72 wystąpienia (132), nadal planned;
.4c/.4d i M-POC5B osobno. Dokładny następny krok: decyzje dla owner-focus
i wcześniejszych pending, potem osobna .4b2 z oszacowaniem przed wykonaniem.
M-POC5 jedyny next. Bez nowych źródeł, ekstrakcji, korekt, czatów i commit/push.
Pomiar/logi/audyt: measurement/M-POC5A-semantic-04b1/ pod prywatnym korzeniem.

'''
status.write_text(text.replace(marker,update+marker,1),encoding='utf-8')
road=ROOT/'docs/ROADMAP.md';text=road.read_text(encoding='utf-8-sig')
oldphrase='podział .4b przed wykonaniem na 65/30/36 ID, następna duża .4b1; lokatory/reszta i M-POC5B osobno'
assert oldphrase in text
road.write_text(text.replace(oldphrase,'.4b1 źródłowo porównana: 65 ID / 125 wystąpień, 116 pozytywnych ograniczonych propozycji i 9 wydzielonych do decyzji; nowe owner review pending; następna osobna .4b2, .4b3/lokatory/reszta i M-POC5B osobno',1),encoding='utf-8')
handoff=ROOT/'docs/HANDOFF.md';oldtext=handoff.read_text(encoding='utf-8-sig')
newtop='''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04b1](handoff/2026-10-11-M-POC5A-semantic-04b1.md)
- **Wynik:** partial / waiting_review
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A; osobna część M-POC5A.4b2 po pakiecie decyzji .4b1

Przejrzano źródłowo pełną .4b1: 65 ID, 125 wystąpień (60/65) i 22 zamrożone
pary na wynik. 116 wystąpień ma pozytywne ograniczone propozycje, 9 wydzielono
do decyzji; wszystkie nowe oceny właściciela pending. Prywatny owner-focus
wyjaśnia znaczenie i skutki, comparisons.md/.json pokazują każde ID i bajty.
Stan prowadzi current-state-09.json, bez zmian owner-decision-03/overlay-03:
po 63/3 przyjętych zakresów na wynik, 8 wcześniejszych oczekiwań pending.
SEM-001–013 zachowane; nowe SEM-014–016 oczekują decyzji. Brakujące rekordy
oceniono osobno od obecnej prozy; nie przyznano automatycznych TP/FP/FN.

Dokładny następny krok: decyzje dla part-04b1/owner-focus.md i wcześniejszych
pending, następnie .4b2 (30 ID / 60 wystąpień) według scope-plan, z oszacowaniem
przed wykonaniem. .4b3 (36/72), .4c/.4d i M-POC5B osobno. M-POC5A/.4/.4b
partial; M-POC5 jedyny next. Źródła, odpowiedzi, eval-v1 i dawne pakiety
zachowane; bez nowych ekstrakcji, korekt, kontekstu, czatów i commit/push.
Logi i końcowy audyt: measurement/M-POC5A-semantic-04b1/.

## Historia przekazania przed .4b1

'''
handoff.write_text(newtop+oldtext.removeprefix('# HANDOFF\n'),encoding='utf-8')
for f in docs[3:]:
    path=ROOT/f;text=path.read_text(encoding='utf-8-sig')
    text+='''
## Wykonanie .4b1 — 2026-10-11

Rzeczywiste porównanie 65 przypisanych ID / 125 wystąpień (60/65) oraz
22 zamrożonych par na wynik ukończone przez oceniającego; akceptacja
właściciela waiting_review. Prywatny part-04b1 ma pełne porównania,
źródła/hashe/bajty, owner-focus i propozycje: 116 wystąpień w ograniczonym
pozytywnym zakresie, 9 do osobnej decyzji. Pokazany pakiet 125, oceniający
przejrzał 125, właściciel nowe 0, pending 125; faktyczny odczyt unknown.
3 krytyczne brakujące rekordy i 4 brakujące wzmianki zachowane oddzielnie
od obecnej prozy, bez automatycznego semantycznego FN. Wcześniejsze
nierozstrzygnięcia bez zmiany; current-state-09.json prowadzi nowy dodatek.
Nadrzędne M-POC5A/.4/.4b partial, nie done. Następna osobna .4b2 po pakiecie
decyzji; .4b3/.4c/.4d nadal niewykonane. M-POC5 jedyny next.
'''
    path.write_text(text,encoding='utf-8')
public='''# M-POC5A.4b1 — rzeczywisty przegląd relacji

- **Data:** 2026-10-11, Europe/Warsaw
- **Wykonawca:** Codex, C:/repo/wargame-compiler, feature/tests
- **Wynik:** partial / waiting_review; pełny przydział porównany przez oceniającego
- **Następny milestone:** M-POC5
- **Następna osobna część:** M-POC5A.4b2 po pakiecie decyzji .4b1

Zweryfikowano oryginalne bajty/hash obu odpowiedzi, eval-v1 i PDF. Szacunek
75–90 minut dla pełnej .4b1 zapisano przed semantycznym review. Porównano
wszystkie 65 ID / 125 wystąpień (60/65), źródłowe zakresy obu końców,
kierunek, rodzaj, jawność, konieczność i wpływ braków. Osobno porównano
22 zamrożone pary na wynik. Nie wykonano pozostałych partii.

Nowy prywatny pakiet reviews/semantic-01/part-04b1/ zawiera czytelne
comparisons.md i pełne comparisons.json z dowodami/pointers/bajtami,
review, issues, owner-focus, presentation i manifest. 60 ID / 116 wystąpień
ma pozytywne propozycje tylko w opisanych zakresach; 5 ID / 9 wystąpień
wydzielono do decyzji. Treść w prozie rozdzielono od braków osobnych rekordów.
Zachowano 3 krytyczne brakujące pary, 4 wzmianki i różnicę rodzaju; nie nadano
automatycznych TP/FP/FN. Nowe SEM-014–016 są propozycjami, nie werdyktami.

Udostępniony pakiet 125 / porównane przez oceniającego 125 / nowe human review
0 / pending 125. Faktyczny odczyt właściciela unknown. Additive stan:
current-state-09.json. owner-decision-03 i overlay-03 bez zmian: po 63 lokalne
zakresy i 3 wymagania źródła na wynik, 8 oczekiwań pending. Wcześniejsze
SEM-001–013 i warianty zachowane. Pełne metryki i budżet not_assessable/unknown.
105 niepotwierdzonych kandydatur nie staje się gold ani mianownikiem recall.

Bez nowych źródeł/pass-02, ekstrakcji/korekt, API inferencji, procesów modelowych,
nowych czatów, M-POC5B/6/7, architektury i commit/push. Nadal 1 dodatkowa strona /
1 reguła / 0 tabel, 1 runda / 0 korekt, 0 pełnych domknięć, 4 częściowe aktualizacje
i 4 nowe deklaracje. Trzeciego źródła nie pozyskano, stop ekspansji na granicy 2.
Izolacja nazw/ścieżek naruszona w historycznym context-01; odczyt treści oceny
niezaobserwowany, ekspozycja/czysty kontekst unknown, bez dowodu skażenia lub
pełnej izolacji. Aktywne czasy, selektory, tokeny, cena i zgodność budżetu unknown.

Dokładne wznowienie: owner-focus części .4b1 oraz wcześniejsze pending,
nowy owner-decision dopiero po rzeczywistej decyzji; następnie osobna .4b2
z istniejącą listą 30 ID / 60 wystąpień i oszacowaniem przed wykonaniem.
.4b3 (36/72), .4c/.4d i M-POC5B osobno. Pozostałe 132 wystąpienia przypisane.
M-POC5A/.4/.4b pozostają partial; M-POC5 jedyny next.

Rzeczywiste logi kontroli, audyt i append-only pomiar:
measurement/M-POC5A-semantic-04b1/ pod prywatnym korzeniem. Wyniki końcowych
kontroli prowadzi completion.json; nie nadają semantycznej akceptacji.
'''
f=ROOT/'docs/handoff/2026-10-11-M-POC5A-semantic-04b1.md';assert not f.exists();f.write_text(public,encoding='utf-8')
print('Additive packet/state/public docs complete; owner review pending.')
