from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
status=ROOT/'docs/STATUS.md';text=status.read_text(encoding='utf-8-sig')
old='nowa akceptacja waiting_review; .4b2 następna osobno; wcześniejsze 63/3 i 8 pending bez zmiany'
assert old in text
text=text.replace(old,'właściciel przyjął 116 dokładnych zakresów relacji (56/60), 9 wydzielonych wystąpień pending; .4b2 następna osobno; wcześniejsze 63/3 i 8 pending bez zmiany',1)
marker='## M-POC5A — rzeczywisty przegląd .4b1, 2026-10-11'
update='''## M-POC5A — akceptacja pozytywnego zakresu .4b1, 2026-10-11

Właściciel odpowiedział „zatwierdzam” po objaśnieniu wyników i propozycji
przyjęcia 116 wystąpień w dokładnie opisanych zakresach. Nowe prywatne
owner-decision-04.json, owner-review-overlay-04.json, current-state-10.json
i owner-review-summary-04.md prowadzą przyjęcie 60 ID: 56 first / 60 context.
Nie obejmuje całych rekordów, wyłączonych deklaracji blokady lub pełnych wyników.
Faktyczne otwarcie/odczyt plików pozostaje unknown.

Pokazany pakiet 125 / porównane przez oceniającego 125 / zakresy przyjęte przez
właściciela 116 / pending 9. Pozostałe .4b2/.4b3 to 132 wystąpienia bez review;
łącznie 141 wystąpień bez przyjętego pozytywnego zakresu. Wyłączone pola
w przyjętych relacjach także pozostają otwarte. SEM-001–016 oraz wcześniejsze
8 oczekiwań bez rozstrzygnięcia; po 63 lokalne / 3 wymagania źródła na wynik
i 264 pary rubryka/EXP bez zmiany. Brakujące rekordy zachowane, bez auto-FN.
105 candidates nie staje się gold; pełne TP/FP/FN/precision/recall nieocenialne.

Dokładny następny krok: osobna .4b2 według 30 ID / 60 wystąpień w scope-plan,
z oszacowaniem i ewentualnym podziałem przed wykonaniem. Wcześniejsze pending
zachować. .4b3/.4c/.4d i M-POC5B osobno. M-POC5A/.4/.4b pozostają partial,
M-POC5 jedyny next. Ta sesja zapisuje decyzję, nie wykonuje kolejnej partii.
Oryginały i poprzednie pakiety/decyzje/pomiary zachowane; bez ekstrakcji,
korekt, nowych źródeł, czatów i commit/push. Pomiar i kontrole:
measurement/M-POC5A-owner-review-004/ pod prywatnym korzeniem.

'''
assert marker in text;status.write_text(text.replace(marker,update+marker,1),encoding='utf-8')
road=ROOT/'docs/ROADMAP.md';text=road.read_text(encoding='utf-8-sig')
old='116 pozytywnych ograniczonych propozycji i 9 wydzielonych do decyzji; nowe owner review pending'
assert old in text;road.write_text(text.replace(old,'właściciel przyjął 116 dokładnych zakresów relacji (56/60), 9 wydzielonych wystąpień pending',1),encoding='utf-8')
handoff=ROOT/'docs/HANDOFF.md';text=handoff.read_text(encoding='utf-8-sig')
# Keep older prose as history, but only one live handoff link.
text=text.replace('[2026-10-11-M-POC5A-semantic-04b1](handoff/2026-10-11-M-POC5A-semantic-04b1.md)','2026-10-11-M-POC5A-semantic-04b1 (`handoff/2026-10-11-M-POC5A-semantic-04b1.md`)',1)
new='''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-owner-review-04](handoff/2026-10-11-M-POC5A-owner-review-04.md)
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Właściciel zatwierdził pozytywny zakres .4b1: 60 ID / 116 wystąpień,
osobno 56 first-001 i 60 context-01, z dokładnymi wyłączeniami. Nowy stan
current-state-10.json, owner-decision-04 i owner-review-overlay-04 pod
reviews/semantic-01/. Dotychczasowe pliki pozostają niezmienione.
9 wydzielonych wystąpień .4b1 oraz SEM-001–016 nadal pending; wcześniejsze
8 oczekiwań i po 63/3 przyjętych zakresów na wynik bez zmiany. Pełne metryki
nieocenialne; brak domknięcia zależnych wyników, grafu lub aktywnego budżetu.

Dokładny następny krok: osobna M-POC5A.4b2 według existing scope-plan:
30 ID / 60 wystąpień, oszacować i w razie potrzeby podzielić przed wykonaniem.
.4b3 (36/72), .4c/.4d i M-POC5B osobno. Wcześniejsze pending zachować;
M-POC5A/.4/.4b partial, M-POC5 jedyny next. Bez nowych źródeł, ekstrakcji,
korekt, czatów i commit/push. Pomiar i logi: measurement/M-POC5A-owner-review-004/.

## Historia przekazania przed decyzją .4b1

'''
handoff.write_text(new+text.removeprefix('# HANDOFF\n'),encoding='utf-8')
for name in ['docs/work/tasks/M-POC5A.md','docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4b.md','docs/work/tasks/semantic/M-POC5A.4b1.md']:
    f=ROOT/name;text=f.read_text(encoding='utf-8-sig')
    text+='''
## Decyzja właściciela dla .4b1 — 2026-10-11

Po odpowiedzi „zatwierdzam” przyjęto dokładny pozytywny zakres 60 ID /
116 wystąpień (56 first / 60 context), bez całych rekordów lub wyłączonych pól.
Nowe owner-decision-04, overlay-04 i current-state-10 zachowują poprzednie
dowody i decyzje. 9 wydzielonych wystąpień, SEM-001–016 i wcześniejsze
8 oczekiwań pending. Pełne metryki nieocenialne; nadrzędne karty partial.
Następna osobna .4b2 (30 ID / 60 wystąpień), po oszacowaniu przed wykonaniem;
.4b3/.4c/.4d i M-POC5B osobno. M-POC5 jedyny next.
'''
    f.write_text(text,encoding='utf-8')
f=ROOT/'docs/handoff/2026-10-11-M-POC5A-owner-review-04.md';assert not f.exists()
f.write_text('''# M-POC5A — akceptacja pozytywnego zakresu .4b1

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Właściciel odpowiedział „zatwierdzam” po objaśnieniu po ludzku i propozycji
przyjęcia 116 dokładnych zakresów relacji. Nowa decyzja owner-decision-04,
overlay-04, current-state-10 i owner-review-summary-04 pod prywatnym
reviews/semantic-01/ wiążą zakres z oboma oryginalnymi hashami oraz eval-v1.
60 różnych ID: 56 zakresów pierwszej odpowiedzi, 60 po kontekście.
Nie oznacza akceptacji całych rekordów, wyłączonych deklaracji blokady,
realnych ratingów/setupu, lokatorów, sytuacji lub pełnych wyników.
Faktyczne otwarcie/odczyt plików unknown; decyzja w czacie jest odnotowana.

Pakiet 125 wystąpień udostępniony i porównany przez oceniającego; 116 przyjętych
przez właściciela w dokładnych zakresach, 9 pending. Pozostałe .4b2/.4b3 mają
132 nieprzejrzane wystąpienia. Łącznie 141 bez przyjętego zakresu; wyłączone
pola zaakceptowanych relacji też otwarte. SEM-001–016 i 8 wcześniejszych
oczekiwań pozostają pending. Po 63 lokalne / 3 wymagania źródła na wynik,
264 pary rubryka/EXP bez zmian. Mianowniki, brakujące pary i 105 candidates
zachowane; pełne TP/FP/FN/precision/recall not_assessable.

Oryginały, źródła, eval-v1, poprzednie pakiety/decyzje/pomiary zachowano.
Ta sesja nie wykonuje .4b2, ekstrakcji/korekt, nowych źródeł/pass-02,
inferencji, czatów, M-POC5B/6/7, architektury i commit/push. Nadal 1 dodatkowa
strona / 1 reguła / 0 tabel, 1 runda / 0 korekt; 0 pełnych domknięć,
4 częściowe uzupełnienia i 4 nowe deklaracje. Trzeciego źródła nie pozyskano,
stop ekspansji na granicy 2. Ekspozycja/czysty kontekst i aktywny budżet unknown
w dotychczasowych zakresach; decyzja nie poświadcza pełnej izolacji/grafu.

Dokładne wznowienie: current-state-10 i owner-decision-04/overlay-04, potem
osobna .4b2: 30 ID / 60 wystąpień według istniejącego scope-plan. Oszacować
pełny zakres przed wykonaniem i podzielić dalej w razie potrzeby; zachować
wcześniejsze pending. .4b3/.4c/.4d i M-POC5B osobno.
M-POC5A/.4/.4b partial; M-POC5 jedyny next.

Pomiar append-only, logi kontroli i końcowy audyt:
measurement/M-POC5A-owner-review-004/ pod prywatnym korzeniem.
Kontrole nie rozszerzają zakresu zatwierdzenia.
''',encoding='utf-8')
print('Updated aggregate docs and next-part handoff, without executing .4b2.')
