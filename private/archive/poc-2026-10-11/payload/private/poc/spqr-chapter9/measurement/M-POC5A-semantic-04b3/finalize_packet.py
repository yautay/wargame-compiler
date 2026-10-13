"""Freeze new proposal packet; update additive state and aggregate docs."""
from pathlib import Path
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04b3';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
packet=load(OUT/'comparisons.json');summary=packet['summary'];old=load(R/'current-state-13.json')
save(OUT/'manifest.json',dict(id='M-POC5A.4b3-manifest-01',card='M-POC5A.4b3',evaluation=packet['evaluation'],responses=packet['responses'],source=packet['source'],
    artifacts=[ref(OUT/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],
    estimate=ref(M/'start.json'),manual_annotations=ref(M/'annotations.json'),status='partial_waiting_review',owner_decisions=[]))
state=copy.deepcopy(old)
state.update(id='M-POC5A-current-state-14',part='M-POC5A.4b3',previous_state=ref(R/'current-state-13.json'),proposal_overlay=ref(OUT/'manifest.json'),
    prior_part_summary=old['summary'],summary=summary,evaluator_compared_relationship_occurrences=257,remaining_uncompared_relationship_occurrences=0,
    owner_pending_relationship_occurrences=72,owner_pending_relationship_occurrences_4b3=72,new_owner_decisions=[],newly_decided_assigned_occurrences=0,
    inherited_issue_ids=old['unresolved_issue_ids'],new_issue_ids=['SEM-018','SEM-019'],unresolved_issue_ids=old['unresolved_issue_ids']+['SEM-018','SEM-019'],
    next_action='Owner decisions on .4b3 owner-focus:68 bounded positive proposals;2occurrences SEM-018 cost vs chart explicitness;2occurrences SEM-019 summary necessity/impact. D961stack kind already decided, not reasked.',
    next_part='M-POC5A.4c',parts_4b3_4c_4d_not_executed=False,parts_4c_4d_not_executed=True,part_4b3_evaluator_review_complete=True,part_4b3_owner_review_complete=False,
    all_4b_assigned_occurrences_evaluator_compared=True,
    owner_pending_relationship_occurrences_policy='72 newly compared .4b3 scoped proposals await owner; prior185 assigned scoped decisions and2extra frozen mention-kind components retained. Excluded fields/full records/frozen missing pairs are not accepted.',
    resume='Owner decision on .4b3 packet68+2+2 scopes; kindD961stack already resolved inSEM-015. Afterwards separate .4c with estimate and pre-review split if needed. Previous8expectations/SEM-001–013 and excluded fields remain open; no extraction/correction/new source.')
assert state['decision']==ref(R/'owner-decision-06.json') and state['overlay']==ref(R/'owner-review-overlay-06.json')
assert state['owner_accepted_relationship_occurrences']==185
save(R/'current-state-14.json',state)
aggregate='''Wykonano rzeczywisty przegląd wszystkich36 przypisanych ID /72 wystąpień,
osobno36 w każdej odpowiedzi. Prywatny part-04b3 zawiera źródła, dokładne
porównania, pola/pointers/hash/bajty i czytelny owner-focus. Propozycje:
68 ograniczonych pozytywnych ocen ról/wymagań oraz4 wystąpienia w dwóch
osobnych kwestiach klasyfikacji i zakresu konieczności/blokady.
Porównano72 /udostępniono72 /nowych decyzji właściciela0 /pending72.
Faktyczne otwarcie/odczyt plików unknown. Wcześniej przyjęty komponent
rodzaju w dwóch wystąpieniach tej partii zachowano, bez ponownego pytania.

Wszystkie36 krawędzi i przypisane im luki identyczne między odpowiedziami;
oba wyniki mają osobne ślady. Uwzględniono częściowo dostarczony ogólny
kontekst, bez zastępowania nim brakujących tabel lub pełnych procedur.
Brak pełnego celu blokuje zależne wykonanie lub realną kwalifikację,
nie automatycznie źródłowy lokalny operator przy zadanych faktach.
Nowe kwestieSEM-018/019 nie wykazują konkretnego błędnego wyniku gry
i nie nadają automatycznie FP. Pełne role/aliasy całych rekordów wyłączone.

current-state-14 prowadzi przegląd; owner-decision-06/overlay-06 zachowują
185 wcześniejszych przypisanych zakresów z decyzjami. Łącznie w trzech
partiach .4b porównano257 przypisanych wystąpień (126/131); pozostaje72
nowych zakresów do decyzji właściciela. To nie257 poprawnych całych
rekordów lub zakończony przegląd wszystkich pól i brakujących par.
SEM-001–013 w pozostałych zakresach i8 starych oczekiwań nadal otwarte;
scoped decyzjeSEM-014–017 zachowane. Po63 lokalne zakresy/3 wymagania
źródła na wynik i264 pary rubryka/EXP bez zmiany.105 candidates nie
staje się gold; pełneTP/FP/FN/precision/recall not_assessable.

Najbliższa czynność: decyzje według prywatnego owner-focus .4b3:68+2+2
dokładnych zakresów. Potem osobna .4c, oszacować i podzielić przed pracą
jeśli potrzeba. .4c/.4d i M-POC5B niewykonane; M-POC5A/.4/.4b partial,
M-POC5 jedyny next. Bez nowych źródeł/pass-02, ekstrakcji, korekt,
czatów, commit/push. Pomiar: measurement/M-POC5A-semantic-04b3/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4b','.4b3']]]
save(M/'public-documents-before.json',[ref(p) for p in files])
p=D/'STATUS.md';text=p.read_text(encoding='utf-8');lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):lines[i]='- **Wynik M-POC5A:** partial — .4b3 porównana36 ID/72 wystąpienia:68 ograniczonych propozycji i4 w dwóch osobnych kwestiach; nowe decyzje pending; poprzednie185 zakresów zachowane; po decyzjach następna osobna .4c'
text='\n'.join(lines)+'\n';marker='## M-POC5A — zatwierdzenie .4b2, 2026-10-11';assert marker in text
p.write_text(text.replace(marker,'## M-POC5A — rzeczywisty przegląd .4b3, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md';text=p.read_text(encoding='utf-8');needle='następna osobna .4b3, lokatory/reszta i M-POC5B osobno';assert needle in text
p.write_text(text.replace(needle,'.4b3 porównana36 ID/72 wystąpienia:68 ograniczonych propozycji i4 w dwóch osobnych kwestiach, nowe pending; łącznie257 przypisanych wystąpień porównano; po decyzjach osobna .4c, reszta i M-POC5B osobno',1),encoding='utf-8')
for p in files[3:]:p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Wykonanie .4b3 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
handoff=D/'handoff/2026-10-11-M-POC5A-semantic-04b3.md';assert not handoff.exists()
handoff.write_text('''# M-POC5A.4b3 — rzeczywisty przegląd trzeciej partii relacji

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca propozycji: Codex; znaczenie akceptuje właściciel. „Kontynuuj”
uruchomiło .4b3, nie nadało akceptacji nowych ocen. Hashe oryginalnych
odpowiedzi, eval-v1, źródła i przydziału prowadzi prywatny manifest.
Dawne pakiety, decyzje, raporty i pomiary pozostają niezmiennymi dowodami.

Szacunek70–85 minut zapisano przed semantycznym przeglądem; dalszy podział
nie był potrzebny. Faktyczny czas kalendarzowy i wyniki obowiązkowych
kontroli prowadzi measurement/M-POC5A-semantic-04b3/completion.json:
scripts/check.ps1 offline z lokalnymiTMP/TEMP i nowym basetemp,
git diff --check i końcowy audyt. Kontrole nie akceptują znaczenia.
Aktywne czasy, selektory, tokens/cena i zgodność pełnego budżetu unknown.

Limity bez zmian:1 dodatkowa strona/1 reguła/0 tabel,1 runda/0 korekt,
0 pełnych domknięć luk,4 częściowe aktualizacje i4 nowe deklaracje;
nie pozyskano trzeciego źródła, stop ekspansji na2. Listing/path discovery
poza allowlistą dawnego context-01 potwierdzone; odczyt treści oceny
niezaobserwowany. Exposure/czysty kontekst unknown, bez certyfikacji
izolacji, grafu, ratingów, setupu, sytuacji lub aktywnego budżetu.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n')
history=history.replace('[2026-10-11-M-POC5A-owner-review-06](handoff/2026-10-11-M-POC5A-owner-review-06.md)',
    '2026-10-11-M-POC5A-owner-review-06 (`handoff/2026-10-11-M-POC5A-owner-review-06.md`)',1)
p.write_text('''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04b3](handoff/2026-10-11-M-POC5A-semantic-04b3.md)
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'\n## Historia przed przeglądem .4b3\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,handoff]])
save(M/'packet-artifacts.json',dict(manifest=ref(OUT/'manifest.json'),current_state=ref(R/'current-state-14.json')))
print('New packet manifest/state14 and aggregate documentation saved; earlier owner decisions unchanged.')
