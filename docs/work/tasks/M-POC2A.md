# M-POC2A: Pakiet wejściowy i minimalny format

- **ID:** M-POC2A
- **Milestone:** M-POC2
- **Rola:** Codex
- **Zależności:** M-POC1C, zamrożony eval-v1.

## Cel i pytanie eksperymentalne

Przygotować powtarzalne wejścia bez klucza oceny. Czy pełna reguła/rozdział, obrazy i prosty format wystarczą do pierwszego odczytu?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/source/source-v1.json`
- `P/evaluation/freeze-public-v1.json`
- `docs/POC-PLAN.md`
- `C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf`

## Wejścia i wersja oceny

Zweryfikowany PDF; wersja oceny eval-v1 znana tylko jako ID/hash.

## Wymagane działania

1. Przygotuj czytelne rendery PDF 31–37 i tekst pomocniczy, z rozdzielonym celem i kontekstem granicznych kolumn. Nie używaj legacy jako domyślnego importu.
2. Zapisz manifest pełnych hashy i wersji narzędzi. Minimalny format obejmuje reguły, osobne relacje, dowody i luki według planu; przykład wyłącznie syntetyczny.
3. Zapisz dokładny prompt i listę plików do ręcznej sesji. Sprawdź brak treści evaluation/ i oczekiwanych odpowiedzi w pakiecie.

## Artefakty wyjściowe i lokalizacje

- `P/inputs/v1/manifest.json i pliki wymienione w manifeście`
- `P/formats/proposal-format-v1.md`
- `P/prompts/first-v1.txt`
- `P/inputs/v1/transfer-list.txt`

## Kryteria zakończenia i kontrole

Rendery czytelne; granice prawidłowe; wszystkie hashe sprawdzone; prompt wymaga jawnych luk i nie nadaje akceptacji. Pliki po wysłaniu są niezmienne.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Inferencja, pełny język reguł, importer, magazyn, pełne coverage glifów.

## Przegląd człowieka

Oględziny czytelności i granic; techniczne zapisy nie wymagają osobnych potwierdzeń.

## Wznowienie

Jeśli inputs/v1 już wysłano, nie zmieniaj go; porównaj hashe i zapisz nową wersję przy koniecznej zmianie.

## Przekazanie

M-POC2B otrzymuje wyłącznie transfer-list, manifest, prompt, format i pliki wejść.
