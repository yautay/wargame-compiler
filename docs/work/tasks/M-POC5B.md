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
