# M-POC7A: Porównanie wyników i warianty dalszej pracy

- **ID:** M-POC7A
- **Milestone:** M-POC7
- **Rola:** Codex
- **Zależności:** M-POC3–M-POC6 zakończone raportami, także przy limitach i blokadach.

## Cel i pytanie eksperymentalne

Przedstawić podstawę decyzji bez deklarowania sukcesu z góry. Czy jakość i koszt uzasadniają dalszą architekturę, zmianę metody lub odrzucenie?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/reports/first-001/report.md`
- `P/reports/first-001/metrics.json`
- `P/reports/context-01/report.md`
- `P/reviews/semantic-01/review.md`
- `P/reviews/situations-01/review.md`
- `P/reports/correction-01/report.md`
- `P/measurement/sessions.jsonl`
- `P/evaluation/eval-v1/manifest.json`
- `docs/LESSONS-LEARNED.md`

## Wejścia i wersja oceny

eval-v1; wszystkie istniejące rundy są wyliczone ścieżką i hashem w nowym comparison-index.json. Nieistniejący etap ma udokumentowane n/a/blocked, nie wymyślony wynik.

## Wymagane działania

1. Zbierz index raportów; porównaj pierwszy wynik, każdy kontekst i korekty na tych samych mianownikach. Oddziel naprawę formatu i skażenie oceną.
2. Sprawdź progi decyzji i budżet, podaj ograniczenia oraz brak danych. Przygotuj rekomendację z uzasadnieniem.
3. Rozważ kontrakt, magazyn i orkiestrację tylko jako propozycje wynikające z pomiaru; dla ewentualnego użycia legacy wskaż potrzebę, ograniczenie i alternatywę pozostawienia w archiwum.

## Artefakty wyjściowe i lokalizacje

- `P/decision/comparison-index.json`
- `P/decision/comparison.md`
- `P/decision/architecture-options.md`

## Kryteria zakończenia i kontrole

Metryki mają sprawdzone mianowniki; koszty obejmują nieudane próby; krytyczne luki jawne. Rekomendacja nie jest decyzją człowieka.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Implementacja architektury, import legacy, stwierdzenie przewagi modelu bez porównania.

## Przegląd człowieka

Właściciel otrzymuje raport i dowody do M-POC7B; nie zatwierdza automatycznie rekomendacji.

## Wznowienie

Od brakującego raportu w comparison-index.json; najpierw jawnie wyjaśnij brak danych.

## Przekazanie

M-POC7B otrzymuje porównanie, opcje i konkretne pytanie o dalszy kierunek.
