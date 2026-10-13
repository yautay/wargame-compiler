# M-POC1C: Przegląd i zamrożenie eval-v1

- **ID:** M-POC1C
- **Milestone:** M-POC1
- **Rola:** Właściciel; Codex zapisuje decyzję i hashe
- **Zależności:** M-POC1B; rzeczywisty przegląd właściciela.

## Cel i pytanie eksperymentalne

Zamrozić sprawdzoną podstawę porównania przed ekstrakcją. Czy ocena i limity są wystarczająco wiarygodne, aby ocenić pierwszy wynik?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/source/source-v1.json`
- `P/evaluation/draft/inventory.json`
- `P/evaluation/draft/expectations.json`
- `P/evaluation/draft/dependencies.json`
- `P/evaluation/draft/situations.json`
- `P/evaluation/draft/review-questions.md`
- `docs/POC-PLAN.md`

## Wejścia i wersja oceny

Draft oceny; wyniki modelu jeszcze nie istnieją.

## Wymagane działania

1. Przejrzyj dowody, zakres oraz 15–20 sytuacji i zatwierdź tylko sprawdzone oczekiwania.
2. Utrwal progi i limity z planu albo zmień je jawnie przed próbą. Zapisz recenzenta, datę, zakres i nierozstrzygnięcia.
3. Zapisz nowy eval-v1 i pełne hashe plików; przygotuj freeze-public-v1.json zawierający tylko metadane, bez odpowiedzi.

## Artefakty wyjściowe i lokalizacje

- `P/evaluation/eval-v1/inventory.json`
- `P/evaluation/eval-v1/expectations.json`
- `P/evaluation/eval-v1/dependencies.json`
- `P/evaluation/eval-v1/situations.json`
- `P/evaluation/eval-v1/review.md`
- `P/evaluation/eval-v1/manifest.json`
- `P/evaluation/freeze-public-v1.json`

## Kryteria zakończenia i kontrole

Hashy zgodne, rzeczywisty przegląd zapisany, liczebności sprawdzone. Zamrożenie przed czasem pierwszej ekstrakcji; brak potwierdzenia oznacza waiting_review.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Ekstrakcja, ujawnienie odpowiedzi ekstraktorowi, zmiana historycznych plików.

## Przegląd człowieka

Obowiązkowe zatwierdzenie podstawy oceny i limitów przez właściciela. Codex nie podpisuje tej decyzji.

## Wznowienie

Sprawdź czy eval-v1 istnieje: jeśli tak, weryfikuj hashe; poprawki przez erratę i nową wersję, bez nadpisania.

## Przekazanie

M-POC2A dostaje źródło i metadane zamrożenia; M-POC2B wyłącznie odseparowany pakiet ekstrakcji.
