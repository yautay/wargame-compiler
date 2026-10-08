# M-POC0: Archiwum, wnioski i plan

- **ID:** M-POC0
- **Milestone:** M-POC0
- **Rola:** Codex
- **Zależności:** Instrukcja właściciela z 2026-10-07; nie wymaga ukończenia M-DESK2.

## Cel i pytanie eksperymentalne

Zachować poprzedni projekt i rozpocząć odseparowaną aktywną strukturę. Czy wszystkie istotne bajty można odtworzyć bez inferencji, a oba projekty uruchamiać niezależnie?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `archive/legacy-2026-10-07/project/CLAUDE.md`
- `archive/legacy-2026-10-07/project/docs/SESSION-PLAYBOOK.md`
- `archive/legacy-2026-10-07/project/docs/STATUS.md`
- `archive/legacy-2026-10-07/project/docs/HANDOFF.md`
- `archive/legacy-2026-10-07/project/docs/handoff/2026-10-07-M-DESK2.md`
- `archive/legacy-2026-10-07/project/docs/ROADMAP.md`
- `archive/legacy-2026-10-07/project/docs/DESKTOP-IMPLEMENTATION-PLAN.md`
- `archive/legacy-2026-10-07/project/docs/DESKTOP-EXCHANGE.md`
- `archive/legacy-2026-10-07/project/docs/adr/ADR-0037-ekstrakcja-desktop-bez-api.md`
- `archive/legacy-2026-10-07/project/docs/adr/ADR-0038-minimalne-kontrakty-desktop.md`
- `archive/legacy-2026-10-07/project/docs/DATA-CONTRACTS.md (sekcja 11)`
- `private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/poc-plan-proposal.txt`
- `private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json`
- `private/source-artifacts/SRC-spqr.rules/responses/spqr-p032-codex-review-20261007-1.json`

## Wejścia i wersja oceny

Zastane pliki publiczne, private/source-artifacts i istotne .glu. Zestaw oceny jeszcze nie istnieje. Przed migracją czytano ścieżki bez prefiksu archive/legacy-2026-10-07/project/.

## Wymagane działania

1. Zinwentaryzuj Git i pliki; snapshot do nowego katalogu, manifest SHA-256 i wyłączenia.
2. Zweryfikuj wszystkie kopie i odtworzenie przed przenoszeniem; przenieś strukturę bez edycji bajtów.
3. Zapisz mapę, instrukcje, ADR, wnioski, plan, karty i bootstrap. Sprawdź prywatność oraz testy legacy i aktywne.

## Artefakty wyjściowe i lokalizacje

- `private/archive/2026-10-07-pre-poc/manifest.json, payload/, restore-check/`
- `archive/legacy-2026-10-07/README.md, movement-map.json, project/`
- `private/archive/legacy-2026-10-07-state/`
- `README.md, CLAUDE.md, docs/POC-PLAN.md, docs/LESSONS-LEARNED.md, docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md`
- `docs/ROADMAP.md, docs/STATUS.md, docs/HANDOFF.md, docs/SESSION-PLAYBOOK.md, docs/work/tasks/, tests/`

## Kryteria zakończenia i kontrole

Pełna zgodność hashy i odtworzenia; importy legacy z własnego katalogu; osobne testy; poprawne linki i jeden next; git diff --check. Dopiero potem done i M-POC1 jako next.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

M-POC1–M-POC7, ekstrakcja, pipeline, API/GUI, commit/push, zmiana historii.

## Przegląd człowieka

Polecenie właściciela upoważnia do reorganizacji. Nie nadaje akceptacji reguł SPQR.

## Wznowienie

Czytaj verification.json i movement-map.json przed wznowieniem; nie nadpisuj snapshotu ani już przeniesionych katalogów.

## Przekazanie

M-POC1A: sprawdzenie źródła i granic, następnie ręczny inwentarz.
