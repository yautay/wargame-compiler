# M-POC5A.4b2: Relacje — partia 2

- **ID:** M-POC5A.4b2
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** [M-POC5A.4b](M-POC5A.4b.md), stan current-state-07.json lub nowszy.

## Cel i pytanie eksperymentalne

Rzeczywisty przegląd przypisanych relacji obu odpowiedzi. Podział z
2026-10-11 PRZED wykonaniem: 30 różnych ID,
30 wystąpień first-001 i 30 context-01.
Typy/statusy ekstraktora służą wyłącznie przydzieleniu zakresu, nie ocenie.

## Dokładne pliki do przeczytania

Bootstrap, SESSION-PLAYBOOK, STATUS, HANDOFF i aktualny handoff, ROADMAP,
POC-PLAN, ADR-0039; karty M-POC5A/.4/.4b. Prywatnie stan, decyzje i overlay,
oba run/proposal/provenance/report, eval-v1 i źródła. Dokładny przydział:
private/poc/spqr-chapter9/measurement/M-POC5A-part04b-preparation-001/scope-plan.json.

## Wejścia i wersja oceny

Niezmienione first-001/context-01 i eval-v1; osobne hashe i bajty.
63 zakresy lokalne i 3 wymagania źródła przyjęte na wynik; żadna relacja
nie dziedziczy przez to akceptacji. 8 oczekiwań nadal pending.

## Wymagane działania

Sprawdzić dla każdego ID źródłowy zakres, tożsamość/zakres celu, kierunek,
rodzaj, jawność, konieczność i wpływ brakującego celu. Transkrypcję odróżnić
od interpretacji; brak źródła od pominięcia relacji. Dwa osobne wyniki na
eval-v1, z pointer/hash/bajtami, recenzentem, zakresem i niepewnościami.
Jedna część do 90 minut. Jeśli oszacowany zakres jest większy, podzielić
go z pełnymi listami ID PRZED przeglądem znaczenia i zaktualizować karty,
ROADMAP i STATUS. Nie zastępować realnego review samym rejestrem pending.

## Artefakty wyjściowe i lokalizacje

Nowy reviews/semantic-01/part-04b2/ (comparisons, review, issues,
owner-focus, presentation, manifest), additive current-state i nowy pomiar
M-POC5A-semantic-04b2/. Wpis sessions.jsonl append-only.

## Kryteria zakończenia i kontrole

Wszystkie przypisane ID rozliczone źródłowo, ocenione lub jawnie blokowane;
brak automatycznej akceptacji. scripts/check.ps1, git diff --check,
rzeczywiste logi i audyt niezmienności. Tylko decyzja człowieka akceptuje znaczenie.

## Zakres wyłączony

Inne partie, .4c/.4d, nowe źródła/pass-02, ekstrakcja i korekty,
API inferencji/automatyczne procesy modelowe, M-POC5B/20 sytuacji, M-POC6/7
i architektura. Nie rozszerzać eval-v1/gold ani wyborów właściciela.

## Przegląd człowieka

Pokazać decyzje po ludzku: co mówi źródło, co zapisał model, gdzie jest
różnica i co zmienia; potem proponowana decyzja i wyłączenia. Pełne ID,
hash/pointer/bajty zostają w prywatnym pakiecie. Brak decyzji waiting_review.

## Wznowienie

Od scope-plan i aktualnego current-state; wszystkie wcześniejsze pending
zachować. Nie utożsamiać poprawnego source requirement z zamkniętym wynikiem.

## Przekazanie

Następna osobna część z zachowaniem wszystkich pending. Nadrzędne .4b,
.4 i M-POC5A partial do pełnego rozliczenia i decyzji. M-POC5 jedyny next.

## Dokładne ID relacji tej partii

D-ZOC-R911, D-ZOC-R915, D1011chart, D1013stack, D911pre, D911shock, D912MRRC, D912react, D913mounted, D913react, D914OW, D914casualty, D914compass, D914leaderwithdraw, D915superiority, D916OW, D917position, D919clash, D919pre, D919shock, D921OW, D922missile, D923pre, D923shock, D924line, D924stack, D931HD, D931OW, D932CRT, D941CRT.

## Wykonanie .4b2 — 2026-10-11

Wykonano rzeczywisty przegląd wszystkich 30 przypisanych ID / 60 wystąpień,
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

## Zatwierdzenie .4b2 — 2026-10-11

Właściciel zatwierdził obie propozycje .4b2 odpowiedzią „zatwierdxam”.
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
