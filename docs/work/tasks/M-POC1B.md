# M-POC1B: Oczekiwania i 15–20 sytuacji

- **ID:** M-POC1B
- **Milestone:** M-POC1
- **Rola:** Przegląd wspólny
- **Zależności:** M-POC1A; granice źródła sprawdzone.

## Cel i pytanie eksperymentalne

Przygotować źródłowo uzasadnioną ocenę niezależną od odpowiedzi. Które fakty i zależności są krytyczne oraz jakie sytuacje ujawnią błąd lub brak kontekstu?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/source/source-v1.json`
- `P/evaluation/owner-review-001/review-summary.md`
- `P/evaluation/owner-review-001/review-manifest.json` i wymienione w nim
  uzupełnienia `inventory-supplement-05a/05b/05c/06c.json` oraz mapy zmian;
  oryginalny draft pozostaje niezmieniony, decyzje mają dokładnie opisany zakres.
- `P/evaluation/draft/inventory.json`
- `P/evaluation/draft/dependency-candidates.json`
- `P/evaluation/draft/inventory-review.md`
- `C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf (zakres i jawnie oznaczony kontekst)`

## Wejścia i wersja oceny

Ręczny inwentarz. Ocena: draft przed zamrożeniem, brak pierwszej odpowiedzi.

## Wymagane działania

1. Przypisz krytyczność warunków, skutków, wyjątków, liczb, negacji, czasu i grafiki.
2. Sprawdź ręcznie relacje jawne/niejawne, kierunek i rodzaj; oddziel wzmianki. Brak celu zapisuj jako wymagający kontekstu.
3. Przygotuj 15–20 sytuacji zwykłych, granicznych, wyjątków i konfliktów z oczekiwanym wynikiem lub uzasadnioną blokadą. Każdy oczekiwany wynik ma podstawę źródłową.

## Artefakty wyjściowe i lokalizacje

- `P/evaluation/draft/expectations.json`
- `P/evaluation/draft/dependencies.json`
- `P/evaluation/draft/situations.json`
- `P/evaluation/draft/review-questions.md`

## Kryteria zakończenia i kontrole

15–20 sytuacji; wszystkie oczekiwania mają dowód lub status wymagający kontekstu. Osobne mianowniki potwierdzone/niepotwierdzone, jawne/niejawne.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Ekstrakcja, dopasowanie gold do odpowiedzi, interpretacja bez źródła.

## Przegląd człowieka

Właściciel uzasadnia krytyczność i oczekiwane rozstrzygnięcia; sporne oczekiwanie pozostaje niepotwierdzone.

## Wznowienie

Kontynuuj od review-questions.md; sprawdź istniejące ID przed dopisaniem kolejnej sytuacji.

## Przekazanie

M-POC1C otrzymuje kompletny draft i pytania do zamrożenia.
