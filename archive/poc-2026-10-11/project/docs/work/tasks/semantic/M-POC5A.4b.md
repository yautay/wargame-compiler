# M-POC5A.4b: Relacje obu wyników

- **ID:** M-POC5A.4b
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** M-POC4 ograniczone done; wcześniejsze pakiety M-POC5A i jawne pending zachowane.

## Cel i pytanie eksperymentalne

Rozliczyć wszystkie 126/131 proponowanych krawędzi obu wyników, 5/3 potwierdzone pary wykonawcze, 7 wzmianek i 7 kontynuacji; zachować 105 kandydatur poza gold. Sprawdzić source/target/kind/direction/necessity oraz nowe relacje i brakujące krytyczne pary. Przed wykonaniem dzielić na jawne partie ID, jeśli review przekroczy 90 minut.

## Dokładne pliki do przeczytania

[Karta nadrzędna .4](M-POC5A.4.md), [M-POC5A](../M-POC5A.md), bootstrap, STATUS, HANDOFF z aktualnym przekazaniem, ROADMAP, POC-PLAN i ADR-0039. Prywatne: najnowszy current-state i owner-decision/overlay, oryginalny checklist, oba run/proposal/provenance/report i niezmienione eval-v1.

## Wejścia i wersja oceny

Te same oryginalne first-001/context-01 i eval-v1, z pełnymi hashami oraz dokładnymi źródłowymi zakresami; właściciel przyjął 43 lokalne zakresy i 2 wymagania źródła w obu wynikach, z wyłączeniami.

## Wymagane działania

Podział 2026-10-11 PRZED review relacji: [M-POC5A.4b1](M-POC5A.4b1.md)
obejmuje 65 ID i 60/65 wystąpień (125), [M-POC5A.4b2](M-POC5A.4b2.md)
30 ID i 30/30 (60), [M-POC5A.4b3](M-POC5A.4b3.md) 36 ID i 36/36 (72).
Razem rozłączne 131 ID/257 wystąpień, bez pominięć. Listy i routing:
private/poc/spqr-chapter9/measurement/M-POC5A-part04b-preparation-001/scope-plan.json.
Następna sesja wykonuje tylko .4b1; ewentualny dalszy podział PRZED review.
Podział wykorzystuje metadane odpowiedzi, bez nadania poprawności lub TP/FP/FN.
Aktualny stan właściciela to 63 lokalne zakresy/3 wymagania źródła na wynik,
8 oczekiwań pending; wcześniejsza liczba w sekcji wejść jest historyczna.

Rozliczyć wszystkie 126/131 proponowanych krawędzi obu wyników, 5/3 potwierdzone pary wykonawcze, 7 wzmianek i 7 kontynuacji; zachować 105 kandydatur poza gold. Sprawdzić source/target/kind/direction/necessity oraz nowe relacje i brakujące krytyczne pary. Przed wykonaniem dzielić na jawne partie ID, jeśli review przekroczy 90 minut. Zachować transkrypcję i interpretację osobno, krytyczny brak źródła jako blokadę zależnego pełnego wyniku, a lokalne zadane fakty oceniać we właściwym zakresie. Oceny modelu są propozycjami, nie akceptacją. Jedna część do 90 minut.

## Artefakty wyjściowe i lokalizacje

Osobne dodatki w reviews/semantic-01/ pod private/poc/spqr-chapter9/, z dokładnymi hashami i śladami do surowych bajtów; nowe decyzje człowieka, nowy katalog pomiaru oraz append-only sessions.jsonl. Nie przepisywać zamkniętych artefaktów.

## Kryteria zakończenia i kontrole

Jawne ID ocenionych i pending, recenzent, źródło, zakres i niepewności. scripts/check.ps1 i git diff --check z logami, nowym basetemp oraz końcową kontrolą niezmienności.

## Zakres wyłączony

Nowe źródła/pass-02, ekstrakcja i korekty, API inferencji, M-POC5B i 20 sytuacji, M-POC6/7 oraz architektura. Nie rozszerzać eval-v1 lub gold.

## Przegląd człowieka

Właściciel rzeczywiście ocenia pokazane zakresy; missing review pozostaje waiting_review. Akceptacja nie obejmuje innych pól, aliasów lub pełnych wyników zależnych od brakujących źródeł.

## Wznowienie

Od pierwszego pending przypisanego tej części. Zmiana hasha odpowiedzi unieważnia dotknięte oceny; bez modelowego wyboru wariantów nierozstrzygniętych przez właściciela.

## Przekazanie

Następna osobna część otrzymuje wszystkie pozostałe pending. M-POC5A pozostaje partial do rozliczenia całości; M-POC5B jest odrębną kartą.

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

## Decyzja właściciela dla .4b1 — 2026-10-11

Po odpowiedzi „zatwierdzam” przyjęto dokładny pozytywny zakres 60 ID /
116 wystąpień (56 first / 60 context), bez całych rekordów lub wyłączonych pól.
Nowe owner-decision-04, overlay-04 i current-state-10 zachowują poprzednie
dowody i decyzje. 9 wydzielonych wystąpień, SEM-001–016 i wcześniejsze
8 oczekiwań pending. Pełne metryki nieocenialne; nadrzędne karty partial.
Następna osobna .4b2 (30 ID / 60 wystąpień), po oszacowaniu przed wykonaniem;
.4b3/.4c/.4d i M-POC5B osobno. M-POC5 jedyny next.

## Rozstrzygnięcie rekomendacji 1–6 — 2026-10-11

Właściciel przyjął sześć przedstawionych rekomendacji odpowiedzią
„zgodnie z rekomendacją”. Nowa owner-decision-05, overlay-05 i current-state-11
pod prywatnym reviews/semantic-01/ zapisują 9 wydzielonych wystąpień (4/5)
z ocenami mieszanymi oraz 2 dodatkowe wystąpienia zamrożonej wzmianki.
116 wcześniejszych pozytywnych zakresów zachowano. Wszystkie 125 przypisanych
wystąpień .4b1 ma decyzje o dokładnych zakresach; nie oznacza to 125 całych
poprawnych relacji. Rozstrzygnięcia odnotowują błędne klasyfikacje i
niewystarczającą deklarację blokady, bez poprawiania odpowiedzi.

SEM-014–016 rozstrzygnięto w przedstawionych zakresach, SEM-004 częściowo;
reszta SEM-001–013 i osiem wcześniejszych oczekiwań pozostają otwarte.
Po 63 lokalne zakresy / 3 wymagania źródła na wynik i 264 pary rubryka/EXP
bez zmiany. Wyłączone pola, pełne wyniki, lokatory i metryki nie otrzymują
akceptacji. Pozostałe .4b2/.4b3 mają 132 wystąpienia do pełnego przeglądu;
dodatkowa decyzja o wzmiance nie wykonuje całej następnej partii.

Następna osobna .4b2: 30 ID / 60 wystąpień według istniejącego scope-plan,
z oszacowaniem przed wykonaniem. .4b3/.4c/.4d i M-POC5B osobno.
M-POC5A/.4/.4b partial, M-POC5 jedyny next. Oryginały, źródła, eval-v1,
poprzednie decyzje i pomiary zachowano; bez nowych źródeł, ekstrakcji,
korekt, czatów i commit/push. Pomiar: measurement/M-POC5A-owner-review-005/.

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

## Wykonanie .4b3 — 2026-10-11

Wykonano rzeczywisty przegląd wszystkich36 przypisanych ID /72 wystąpień,
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

## Decyzja .4b3 i podział .4c przed wykonaniem — 2026-10-11

Właściciel zatwierdził trzy dokładne rekomendacje .4b3:68 ograniczonych
ocen i4 wystąpienia dwóch osobnych kwestii. Owner-decision-07/overlay-07
oraz current-state-15 zachowują poprzednie185 zakresów; razem257
przypisanych wystąpień ma decyzje o komponentach, nie całych rekordach.
SEM-018/019 rozstrzygnięte tylko w przedstawionych zakresach. Osiem
wcześniejszych oczekiwań, SEM-001–013 i wyłączone pola nadal otwarte.

Przed review .4c podzielono124 wystąpienia lokatorów (59/65) na trzy
rozłączne części: .4c1 22ID/44 wystąpienia, .4c2 21ID/42, .4c3 22ID/38.
Szacunek całości160–220 minut; pierwsza część70–85. W tej sesji wykonywana
wyłącznie .4c1. Pozostałe przypisane, bez oceny z samych metadanych.
M-POC5A/.4/.4b/.4c partial, M-POC5 jedyny next. Bez ekstrakcji/korekt,
nowych źródeł, czatów, commit/push. Prywatny pomiar i scope-plan:
measurement/M-POC5A-semantic-04c1/.
