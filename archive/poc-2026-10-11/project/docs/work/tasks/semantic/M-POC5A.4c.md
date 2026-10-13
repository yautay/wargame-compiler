# M-POC5A.4c: Lokatory i granice glifów

- **ID:** M-POC5A.4c
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** M-POC4 ograniczone done; wcześniejsze pakiety M-POC5A i jawne pending zachowane.

## Cel i pytanie eksperymentalne

Przejrzeć E916 oraz 58 dawnych i 6 nowych przypadków granic glifów, z osobnymi dowodami obu hashów. Oddzielić geometryczną poprawność, położenie/kompletność cytatu, czytelność oraz znaczenie. Nie poprawiać bbox lub odpowiedzi; większy zakres dzielić przed wykonaniem.

## Dokładne pliki do przeczytania

[Karta nadrzędna .4](M-POC5A.4.md), [M-POC5A](../M-POC5A.md), bootstrap, STATUS, HANDOFF z aktualnym przekazaniem, ROADMAP, POC-PLAN i ADR-0039. Prywatne: najnowszy current-state i owner-decision/overlay, oryginalny checklist, oba run/proposal/provenance/report i niezmienione eval-v1.

## Wejścia i wersja oceny

Te same oryginalne first-001/context-01 i eval-v1, z pełnymi hashami oraz dokładnymi źródłowymi zakresami; właściciel przyjął 43 lokalne zakresy i 2 wymagania źródła w obu wynikach, z wyłączeniami.

## Wymagane działania

Przejrzeć E916 oraz 58 dawnych i 6 nowych przypadków granic glifów, z osobnymi dowodami obu hashów. Oddzielić geometryczną poprawność, położenie/kompletność cytatu, czytelność oraz znaczenie. Nie poprawiać bbox lub odpowiedzi; większy zakres dzielić przed wykonaniem. Zachować transkrypcję i interpretację osobno, krytyczny brak źródła jako blokadę zależnego pełnego wyniku, a lokalne zadane fakty oceniać we właściwym zakresie. Oceny modelu są propozycjami, nie akceptacją. Jedna część do 90 minut.

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

## Wykonanie .4c1 — 2026-10-11

Właściciel zatwierdził trzy rekomendacje .4b3 odpowiedzią „ok kontynuuj”:
68 ograniczonych ocen i4 wystąpienia dwóch osobnych kwestii.
Owner-decision-07/overlay-07 zachowują185 poprzednich zakresów; łącznie257
przypisanych wystąpień relacji ma decyzje o komponentach, nie całych rekordach.
SEM-018/019 rozstrzygnięte tylko w przedstawionych zakresach. Osiem starych
oczekiwań, SEM-001–013 w pozostałych zakresach i wyłączone pola otwarte.

Przed oceną .4c podzielono124 wystąpienia (59/65) na części44/42/38.
Wykonano rzeczywisty przegląd .4c1:22ID/44 wystąpienia, osobno22/22.
Geometria/hash/wymiary i lokalizacja krótkiego cytatu na pełnym źródle
potwierdzone przez oceniającego44. Pełne obwiednie glifów:0/44 mieszczą się.
Raster:38 krótkich cytatów czytelnych bez zaobserwowanej utraty tuszu,
4 z przyciętymi dolnymi częściami liter,2 z brakującą linią cytatu.
Nie utożsamiono wad lokatora z błędami odczytu/znaczenia lub metrykami.

Prywatny part-04c1 zawiera porównania, źródła, dokładne nieposzerzone
wycinki, diagnostyczne widoki granic, ślady pól do bajtów i owner-focus.
Porównano44 /udostępniono44 /nowych decyzji właściciela0 /pending44.
Faktyczny odczyt plików unknown. SEM-005/007 otrzymały ograniczone
propozycje, bez automatycznego zamknięcia. current-state-16 prowadzi
przegląd. Kolejne80 wystąpień niewykonane, jawnie przypisane.

Najbliższa czynność: decyzje według owner-focus .4c1, potem osobna .4c2
21ID/42 wystąpienia, oszacować przed pracą. .4c3 ma22ID/38, .4d iM-POC5B
osobno. M-POC5A/.4/.4b/.4c partial, M-POC5 jedyny next. Bez nowych
źródeł, ekstrakcji, korekt, czatów, commit/push; gold i limity bez zmiany.
Pomiar/logi/audyt: measurement/M-POC5A-semantic-04c1/.

## Zatwierdzenie .4c1 i wykonanie .4c2 — 2026-10-11

Właściciel zatwierdził oceny .4c1 odpowiedzią „zatwierdzam i kontynuuj”.
Owner-decision-08/overlay-08 zapisują44 rozłączne oceny komponentów:
poprawną geometrię,38 czytelnych krótkich rastrów i6 niepełnych;
wszystkie44 ścisłe naruszenia obwiedni zachowane. To nie44 dobre lokatory
lub poprawne całe reguły. Wady oryginalnych lokatorów nie zostały naprawione.
SEM-005 potwierdzony tylko jako wada dowodu, SEM-007 częściowo oceniony;
inne wcześniejsze nierozstrzygnięcia i8 oczekiwań pozostają otwarte.

Wykonano rzeczywisty przegląd .4c2:21ID/42 wystąpienia, osobno21/21.
Każdy krótki cytat odnaleziono w źródle; hash/wymiary/geometria zgodne42.
Wszystkie42 krótkie rastry czytelne bez zaobserwowanej utraty tuszu.
Pełne obwiednie:40 mierzalnych naruszeń;2 wystąpienia mają wyłącznie
różnicę na poziomie reprezentacji zmiennoprzecinkowej i ścisła ocena
pozostaje nieocenialna z powodu precyzji. Raw porównania bez tolerancji
zachowano, bez poszerzania ramki lub automatycznego ścisłego pass.
Wady/niepewności lokatora nie są automatycznie błędami znaczenia.

Prywatny part-04c2 ma każde porównanie, źródła, obrazy granic i dokładne
nieposzerzone wycinki, pola/pointers/hash/bajty oraz owner-focus.
Porównano42 /udostępniono42 /nowych decyzji właściciela0 /pending42.
Faktyczne otwarcie/odczyt plików unknown. current-state-18 prowadzi
przegląd. Łącznie86/124 przypisanych wystąpień lokatorów porównano,
44 poprzednie ma decyzje właściciela.38 w .4c3 nadal niewykonane.

257 komponentowych decyzji relacji,264 pary rubryka/EXP, po63 lokalne
zakresy/3 wymagania źródła na wynik zachowane. Pełne wyniki/pola/aliasy,
ratingi, setup, sytuacje i metryki wyłączone. Gold i limity bez zmiany.
Najbliższy krok: decyzje według owner-focus .4c2, potem osobna .4c3:
22ID/38 wystąpień po oszacowaniu. .4d iM-POC5B osobno; nadrzędne karty
partial, M-POC5 jedyny next. Bez nowych źródeł/ekstrakcji/korekt/czatów/
commit/push. Pomiar: measurement/M-POC5A-semantic-04c2/.

## Zatwierdzenie .4c2 i wykonanie .4c3 — 2026-10-11

Właściciel zatwierdził oceny .4c2 i polecił kontynuację oraz wskazanie
pozostałego etapu 5. Owner-decision-09/overlay-09 zapisują 42 ograniczone
oceny: czytelne krótkie rastry/poprawne źródła i geometrie; 40 mierzalnych
ograniczeń pełnych obwiedni oraz 2 przypadki nieocenialne z powodu precyzji.
Łącznie 86 wcześniejszych wystąpień lokatorów ma decyzje właściciela.
To komponenty oceny, nie 86 dobrych lokatorów lub całych poprawnych reguł.

Wykonano ostatnią przypisaną partię .4c3: 22 ID / 38 wystąpień, osobno
16/22. Sześć rekordów tylko po kontekście oceniono w już dostarczonym
wycinku, bez odczytu pozostałej strony. Geometria/źródło zgodne 38;
pełne obwiednie 38 mierzalnych naruszeń. Raster: 36 krótkich cytatów
czytelnych bez zaobserwowanej utraty tuszu, 2 czytelne, ale z uciętymi
dolnymi częściami liter. Oryginalne ramki/odpowiedzi bez naprawy.

Porównano 38 /udostępniono 38 /nowych decyzji właściciela 0 /pending 38.
Faktyczny odczyt plików unknown. Wszystkie 124/124 przypisane wystąpienia
lokatorów rzeczywiście porównano. To nie pełna certyfikacja dowodów,
grafu, ratingów lub znaczenia całych rekordów. current-state-20 prowadzi
nowy prywatny part-04c3: porównania, nieposzerzone wycinki, diagnostyka
granic, dokładne pola/pointers/hash/bajty i owner-focus po ludzku.

257 decyzji komponentów relacji, 264 pary rubryka/EXP, po 63 lokalne
zakresy/3 wymagania źródła na wynik oraz 8 dawnych oczekiwań zachowane.
Starsze nierozstrzygnięcia pozostają otwarte; pełne metryki nieocenialne.
Gold i limity bez zmiany. Nadrzędne karty partial, M-POC5 jedyny next.

Po decyzjach .4c3 pozostają dwa bloki etapu 5: osobna .4d rozliczy
inwentarz/szersze komponenty/pending; potem M-POC5B oceni 20 zamrożonych
sytuacji w dwóch odpowiedziach (40 ocen). Liczba sesji i godzin unknown
do oszacowania zakresu i ewentualnego podziału przed pracą. Nie wykonano
.4d/B, nowych źródeł/ekstrakcji/korekt/czatów/commit/push w tej sesji.
Pomiar: measurement/M-POC5A-semantic-04c3/.

## Zatwierdzenie .4c3 i wykonanie .4d1 — 2026-10-11

Właściciel zatwierdził .4c3: 38 ograniczonych ocen komponentów.
Wszystkie 124 przypisane wystąpienia lokatorów mają teraz decyzje
właściciela; nie jest to akceptacja całych rekordów ani dobrych ramek.
Oryginalne wady zachowano. Owner-decision-10/overlay-10 prowadzą stan.

Przed review podzielono .4d na pięć osobnych kart, z rozłącznym przydziałem
39/68/59/41 pozycji i osobnym końcowym uzgodnieniem. Wykonano wyłącznie
.4d1: 39 pozycji / 78 wystąpień, osobno 39/39 w obu odpowiedziach.
Rzeczywiście porównano nagłówki, noty i przykłady w dostarczonych źródłach
z oryginalnymi rekordami. Prywatny pakiet part-04d1 zawiera dokładne
zakresy źródłowe, pola, hash/pointer/bajty, niepewności i owner-focus.

Proponowane 76 ocen ograniczonego wsparcia treści oraz 2 oceny częściowego
pominięcia w treści noty, z poprawnym cytatem dowodowym. Struktury danych
nie otrzymują certyfikatu dosłownej transkrypcji. Udostępniono 78,
porównano 78, nowych decyzji właściciela 0, pending 78. Faktyczny odczyt
plików przez właściciela unknown. Starsze nierozstrzygnięcia i wyłączone
pola pozostają otwarte. Pełne metryki not_assessable, gold bez zmiany.

257 wcześniejszych zakresów relacji, 124 zakresy lokatorów, 264 pary
rubryka/oczekiwanie, po 63 lokalne zakresy/3 wymagania źródła i 8 dawnych
oczekiwań pending zachowano. Nie dodaje się punktów za parent/child.
current-state-22 prowadzi nowy wynik. Nadrzędne karty partial;
M-POC5 pozostaje jedynym next.

Po decyzjach .4d1 pozostały cztery karty .4d: 168 pozycji w trzech
partiach 68/59/41, następnie końcowe uzgodnienie. Potem osobne M-POC5B:
20 zamrożonych sytuacji w dwóch odpowiedziach, czyli 40 ocen.
Pierwotny ogólny szacunek .4d 300–420 minut zachowano; suma zapisanych
przed review zakresów pięciu części wynosi 330–430 minut. Szacunek
obecnej części 70–85 minut. Przed kolejną częścią odświeżyć jej szacunek;
nie wykonano jej w tej sesji. Czas aktywny i zgodność budżetu unknown.
Nie wykonano nowych źródeł, ekstrakcji, korekt, czatów, commit/push.
Pomiar: measurement/M-POC5A-semantic-04d1/.
