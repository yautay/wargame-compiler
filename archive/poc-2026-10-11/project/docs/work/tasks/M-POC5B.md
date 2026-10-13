# M-POC5B: Ocena 15–20 sytuacji

- **ID:** M-POC5B
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** M-POC5A; podstawa semantyczna i jawne luki.

## Cel i pytanie eksperymentalne

Sprawdzić użyteczność reguł na konkretnych sytuacjach bez pełnego silnika. Czy zwykłe, graniczne i konfliktowe sytuacje mają poprawne rozstrzygnięcie lub właściwą blokadę?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/evaluation/eval-v1/manifest.json`
- `P/evaluation/eval-v1/situations.json`
- `P/evaluation/eval-v1/dependencies.json`
- `P/reviews/semantic-01/review.md`
- `P/reviews/semantic-01/issues.json`
- `P/proposals/context-01/proposal.json`
- `P/proposals/first-001/proposal.json`
- `P/inputs/v1/manifest.json`
- `P/context/pass-01/manifest.json`

## Wejścia i wersja oceny

Wszystkie 15–20 sytuacji eval-v1 i jawnie wybrany wynik; jeśli nie było kontekstu, first-001 z n/a.

## Wymagane działania

1. Dla każdej sytuacji zapisz osobne wnioski z pierwszego wyniku i wyniku po kontekście, użyte zależności oraz źródłowo uzasadniony expected z eval-v1. Zachowaj dwie kolumny i hashe; nieocenialny pierwszy wynik pozostaje not_assessable, naprawa formatu ma osobną kolumnę.
2. Porównaj wynik, granice, konflikt i timing; brak krytycznego źródła blokuje odpowiedź, nie daje domyślnego wyniku.
3. Zlicz poprawne, błędne, właściwie/niezasadnie blokowane i nieocenione. Zachowaj pełen mianownik także przy blokadach.

## Artefakty wyjściowe i lokalizacje

- `P/reviews/situations-01/results.json`
- `P/reviews/situations-01/review.md`
- `P/reviews/situations-01/issues.json`

## Kryteria zakończenia i kontrole

Każda z 15–20 sytuacji oceniona albo jawnie oczekuje; expected i wniosek mają osobne dowody; brak zgadywania.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Implementacja silnika, generowanie nowego gold po zobaczeniu wyniku, usuwanie trudnych sytuacji.

## Przegląd człowieka

Właściciel potwierdza rozstrzygnięcia i źródła, zwłaszcza konflikt/wyjątek/granicę. Deklaracja modelu nie zamyka review.

## Wznowienie

Wznowienie od nieocenionej sytuacji; errata gold pozostaje osobno i wymaga ponownej oceny wszystkich porównywanych wariantów.

## Przekazanie

M-POC6A otrzymuje ID błędów; M-POC7 dostanie komplet wyników, także zablokowanych.


## M-POC5B — wszystkie sytuacje porównane, 2026-10-11

Po zatwierdzeniu dokładnego uzgodnienia .4d5 wykonano całe M-POC5B:20 zamrożonych sytuacji w obu oryginalnych odpowiedziach,40 ocen. Każdy wariant i wymagany wniosek porównano ze źródłem, oryginalnymi polami i frozenexpected; prywatny situations-01 zawiera ślady do bajtów, użyte zależności, ręczne wyprowadzenia i opis decyzji po ludzku. To ocena wyprowadzalności z zapisu reguł przy zadanych faktach, bez nowych odpowiedzi modelu na sytuacje, nowej ekstrakcji, korekty lub silnika. Szacunek75–90min zapisano przed oceną; cały zakres mieści się w jednej zaplanowanej części.

Propozycjefirst:15 zgodnych lokalnych wyników,3 właściwe oczekiwane blokady,1kandydat nieuzasadnionej lokalnej blokady i1pełny wynik zawieszony po porównaniu. Context:14/3/1/2. Razem35 pozytywnych ocen oraz5 do osobnego rozstrzygnięcia. Pełny mianownik20 w każdej odpowiedzi zachowany; warianty nie dają dodatkowych punktów. Oczekiwane blokady nie są meaningful localresults dla progu80%.

Porównano40 / udostępniono40 / nowych decyzji właściciela0 / pending40. Wszystkie40 ocen wykonane przez oceniającego;3 pełne wnioski zawieszone mimo porównanych komponentów. Wydzielono konsekwencje dwóch starych nierozstrzygnięć i jedno pytanie o zakres zamrożonych faktów wobec dostarczonego warunku po kontekście. Nie rozstrzygnięto starych wariantów ani nie zmieniono eval-v1; nie wykazano przez samo to regresji modelu lub konkretnej złej liczby.

current-state32 prowadzi nowy wynik. Starsze8 oczekiwań/13 kwestii oraz wcześniejsze ograniczone decyzje zachowane.414 zakresów inwentarza,257 relacji,124 lokatory i264 pary rubryki bez ponownego punktowania. M-POC5B i milestone5 partial/waiting_review, M-POC5 jedyny next. M-POC5A w szerszym zakresie nadal partial; pełne jakość/TP/FP/FN/precision/recall not_assessable.

Najbliższa czynność: decyzje według prywatnego situations-01/owner-focus —35 pozytywnych ocen oraz2+2+1 osobne. Następnie świadomie rozliczyć starsze nierozstrzygnięcia i warunki formalnego zamknięcia etapu5. Nie rozpoczęto M-POC6/7 ani naprawy odpowiedzi. Faktyczny odczyt plików przez właściciela unknown; konfiguracja, aktywne czasy, tokeny, cena i łączny budżet unknown. Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów, commit/push lub architektury. Kontrole i audyt: measurement/M-POC5B-situations-01/.
