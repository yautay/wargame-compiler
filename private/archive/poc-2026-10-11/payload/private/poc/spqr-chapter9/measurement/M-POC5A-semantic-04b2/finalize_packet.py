"""Freeze the new proposal packet and advance additive/public state."""
from pathlib import Path
import copy,json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
R=P/'reviews/semantic-01';OUT=R/'part-04b2';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
packet=load(OUT/'comparisons.json');summary=packet['summary'];old=load(R/'current-state-11.json')
save(OUT/'manifest.json',dict(id='M-POC5A.4b2-manifest-01',card='M-POC5A.4b2',evaluation=packet['evaluation'],responses=packet['responses'],source=packet['source'],
    artifacts=[ref(OUT/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],
    estimate=ref(M/'start.json'),manual_annotations=ref(M/'annotations.json'),status='partial_waiting_review',owner_decisions=[]))
state=copy.deepcopy(old)
state.update(id='M-POC5A-current-state-12',part='M-POC5A.4b2',previous_state=ref(R/'current-state-11.json'),proposal_overlay=ref(OUT/'manifest.json'),
    prior_part_summary=old['summary'],summary=summary,evaluator_compared_relationship_occurrences=185,remaining_uncompared_relationship_occurrences=72,
    owner_pending_relationship_occurrences=132,owner_pending_relationship_occurrences_4b2=60,new_owner_decisions=[],newly_decided_assigned_occurrences=0,
    inherited_issue_ids=old['unresolved_issue_ids'],new_issue_ids=['SEM-017'],unresolved_issue_ids=old['unresolved_issue_ids']+['SEM-017'],
    next_action='Owner decision on part-04b2/owner-focus.md:52 bounded positive +8 separate block-scope cases; no automatic acceptance.',next_part='M-POC5A.4b3',
    parts_4b2_4b3_4c_4d_not_executed=False,parts_4b3_4c_4d_not_executed=True,part_4b2_evaluator_review_complete=True,part_4b2_owner_review_complete=False,
    owner_pending_relationship_occurrences_policy='60 newly compared .4b2 scopes await owner +72 assigned .4b3 scopes await full review. Excluded fields of previous125 remain unaccepted.',
    resume='Owner decision on .4b2 packet:52 bounded proposals and8 scope casesSEM-017. Then separate .4b3:36IDs/72occurrences; estimate before review. Preserve previous owner-decision05/overlay05, remaining SEM-001–013, all8expectations, excluded fields, and scoped dispositions SEM-014–016. No extraction/correction/new source.')
assert state['decision']==ref(R/'owner-decision-05.json') and state['overlay']==ref(R/'owner-review-overlay-05.json')
assert state['owner_accepted_relationship_occurrences']==125
save(R/'current-state-12.json',state)
aggregate='''Wykonano rzeczywisty przegląd wszystkich 30 przypisanych ID / 60 wystąpień,
osobno 30 pierwszej odpowiedzi i 30 po kontekście. Prywatny part-04b2 zawiera
źródła, pełne porównania, surowe pola i ślady do bajtów oraz owner-focus.
52 wystąpienia mają pozytywne propozycje tylko w dokładnych zakresach ról
relacji i wymagań źródła; 8 ma osobną decyzję o zakresie blokady SEM-017.
Wszystkie nowe oceny właściciela pending: porównano60 / udostępniono60 /
nowych decyzji0. Faktyczne otwarcie/odczyt plików pozostaje unknown.

W 29 ID relacje obu wyników identyczne; jedno ID zmienione po kontekście,
osobno oceniono dwa doprecyzowane opisy luk. Brak nowych źródeł lub korekt.
Przegląd nie rekonstruuje brakujących celów z ich nazw. Pełne wykonanie
zależne od brakującego źródła odróżniono od lokalnego operatora lub wyjątku
przy zadanych faktach. Nowa kwestia dotyczy zakresu blokady, bez wykazanego
konkretnego błędnego wyniku gry i bez automatycznych FP.

current-state-12 prowadzi przegląd; owner-decision-05/overlay-05 zachowują
125 wcześniejszych zakresów. SEM-001–013 w pozostałych zakresach i osiem
wcześniejszych oczekiwań nadal otwarte; decyzje SEM-014–016 zachowane.
Po 63 lokalne zakresy / 3 wymagania źródła na wynik i 264 pary rubryka/EXP
bez zmiany. Wyłączone pola, pełne wyniki, lokatory i metryki bez akceptacji.
105 candidates nie staje się gold. Łącznie porównano185 przypisanych
wystąpień; .4b3 ma72 do pełnego review. Łącznie132 bez nowych decyzji:
60 oczekuje właściciela w .4b2,72 pełnego przeglądu w .4b3.

Najbliższa czynność: decyzje według prywatnego owner-focus .4b2; następnie
osobna .4b3:36 ID /72 wystąpienia według istniejącego scope-plan, oszacować
przed wykonaniem. .4c/.4d i M-POC5B osobno. M-POC5A/.4/.4b partial,
M-POC5 jedyny next. Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów
i commit/push. Pomiar i logi: measurement/M-POC5A-semantic-04b2/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',
    *[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4b','.4b2']]]
save(M/'public-documents-before.json',[ref(p) for p in files])
p=D/'STATUS.md';text=p.read_text(encoding='utf-8');lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):
        lines[i]='- **Wynik M-POC5A:** partial — .4b2 porównana: 30 ID /60 wystąpień, 52 ograniczone propozycje i8 osobnych zakresów blokady; nowe oceny właściciela pending; wcześniejsze125 zakresów zachowane; po decyzjach następna osobna .4b3'
text='\n'.join(lines)+'\n';marker='## M-POC5A — rozstrzygnięcie rekomendacji 1–6, 2026-10-11';assert marker in text
text=text.replace(marker,'## M-POC5A — rzeczywisty przegląd .4b2, 2026-10-11\n\n'+aggregate+'\n'+marker,1)
p.write_text(text,encoding='utf-8')
p=D/'ROADMAP.md';text=p.read_text(encoding='utf-8');needle='następna osobna .4b2, .4b3/lokatory/reszta i M-POC5B osobno';assert needle in text
text=text.replace(needle,'.4b2 porównana30 ID/60 wystąpień:52 ograniczone propozycje i8 do decyzji o blokadzie, wszystkie nowe pending; po decyzjach następna osobna .4b3, lokatory/reszta i M-POC5B osobno',1)
p.write_text(text,encoding='utf-8')
for p in files[3:]:
    p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Wykonanie .4b2 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
handoff=D/'handoff/2026-10-11-M-POC5A-semantic-04b2.md';assert not handoff.exists()
handoff.write_text('''# M-POC5A.4b2 — rzeczywisty przegląd drugiej partii relacji

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca propozycji: Codex. Znaczenie akceptuje właściciel; „kontynuuj”
uruchomiło przegląd, nie zaakceptowało nowych wyników. Wejścia i pełne hashe
obu odpowiedzi/eval-v1/źródła/przydziału prowadzi prywatny manifest part-04b2.
Poprzednie pakiety, decyzje, raporty i pomiary są niezmiennymi dowodami.

Szacunek 60–75 minut zapisano przed semantycznym review; dalszy podział
nie był potrzebny. Czas kalendarzowy, logi scripts/check.ps1 z lokalnymi
TMP/TEMP i nowym basetemp, git diff --check oraz końcowy audyt prowadzi
measurement/M-POC5A-semantic-04b2/completion.json. Aktywny czas, selektory,
tokeny/cena i zgodność całego budżetu unknown. Kontrole nie nadają
akceptacji znaczenia.

Limity kontekstu i korekt bez zmian:1 strona/1 reguła/0 tabel,
1 runda/0 korekt,0 pełnych domknięć,4 częściowe aktualizacje i4 nowe
deklaracje. Źródła trzeciego kroku nie pozyskano; stop ekspansji na2.
Naruszenie izolacji nazw/ścieżek dawnego context-01 potwierdzone;
odczyt treści oceny niezaobserwowany. Ekspozycja/czysty kontekst unknown,
bez certyfikacji pełnej izolacji, grafu lub aktywnego budżetu.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n')
history=history.replace('[2026-10-11-M-POC5A-owner-review-05](handoff/2026-10-11-M-POC5A-owner-review-05.md)',
    '2026-10-11-M-POC5A-owner-review-05 (`handoff/2026-10-11-M-POC5A-owner-review-05.md`)',1)
p.write_text('''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04b2](handoff/2026-10-11-M-POC5A-semantic-04b2.md)
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'\n## Historia przed przeglądem .4b2\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,handoff]])
save(M/'packet-artifacts.json',dict(manifest=ref(OUT/'manifest.json'),current_state=ref(R/'current-state-12.json')))
print('New packet manifest/state12 and aggregate documentation saved; owner-decision05/overlay05 unchanged.')
