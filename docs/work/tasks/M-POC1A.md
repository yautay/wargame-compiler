# M-POC1A: Źródło i ręczny inwentarz

- **ID:** M-POC1A
- **Milestone:** M-POC1
- **Rola:** Codex; przegląd wspólny
- **Zależności:** M-POC0 zakończony.

## Cel i pytanie eksperymentalne

Ustalić rzeczywistą zawartość rozdziału i granice oceny. Jakie oznaczenia, klauzule, tabele, diagramy, noty i kontynuacje rzeczywiście występują?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `docs/LESSONS-LEARNED.md`
- `docs/handoff/2026-10-07-M-POC0.md`
- `private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/poc-plan-proposal.txt`
- `private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json`
- `C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf (PDF 31–37)`

## Wejścia i wersja oceny

Oryginalny PDF i kandydaci zakresu. Ocena: draft, bez zamrożonej wersji.

## Wymagane działania

1. Sprawdź istnienie, pełny SHA-256 i wydanie PDF; porównaj z kandydatem. Rozbieżność wymaga wyjaśnienia przed odczytem.
2. Sprawdź wizualnie początek prawej kolumny PDF 31 od 9.0 i koniec lewej PDF 37 przed 10.0; oddziel kontekst.
3. Spisz oznaczenia i klauzule z dowodami, tabele/diagramy/noty i kontynuacje. Nie zakładaj ciągłości numeracji. Zbierz odwołania liczbowe, nazwane i niejawne jako kandydatów.

## Artefakty wyjściowe i lokalizacje

- `P/source/source-v1.json`
- `P/evaluation/draft/inventory.json`
- `P/evaluation/draft/dependency-candidates.json`
- `P/evaluation/draft/inventory-review.md`

## Kryteria zakończenia i kontrole

Każdy obszar rozdziału rozliczony ręcznie; element ma typ, lokalne ID, źródło/stronę i status. 19 kandydatów nie staje się automatycznie gold.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Ekstrakcja modelowa, oczekiwane wyniki sytuacji, domykanie całej instrukcji, kod pipeline’u.

## Przegląd człowieka

Właściciel sprawdza granice i niepewne elementy inwentarza, bez uznawania propozycji modelu za akceptację.

## Wznowienie

Odczytaj draft/inventory-review.md; wznowienie od pierwszego oznaczonego nieprzejrzanego obszaru, bez zmiany sprawdzonego źródła.

## Przekazanie

M-POC1B otrzymuje inwentarz i listę niepewności.
