# M-POC6B: Ponowna ocena, regresje i koszt

- **ID:** M-POC6B
- **Milestone:** M-POC6
- **Rola:** Codex; przegląd wspólny
- **Zależności:** M-POC6A; odpowiedź albo zapis braku.

## Cel i pytanie eksperymentalne

Zmierzyć rezultat jednej korekty i zdecydować o końcu pętli. Które błędy poprawiono, co zepsuto i ile kosztowała zmiana?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/corrections/correction-01/parent.json`
- `P/corrections/correction-01/response.raw.txt`
- `P/corrections/correction-01/run.json`
- `P/evaluation/eval-v1/manifest.json`
- `P/evaluation/eval-v1/inventory.json`
- `P/evaluation/eval-v1/expectations.json`
- `P/evaluation/eval-v1/dependencies.json`
- `P/evaluation/eval-v1/situations.json`
- `P/measurement/sessions.jsonl`

## Wejścia i wersja oceny

Ta sama wersja oceny co rodzic, jego raporty wymienione dokładnie w parent.json; iteracje 02/03 analogicznie.

## Wymagane działania

1. Ponów format/ID/referencje/dowody oraz kontrole dotkniętych i wszystkich krytycznych elementów. Przejrzyj również wcześniej poprawne sytuacje.
2. Zapisz poprawione błędy, nowe regresje, resztę luk i osobne metryki bez zastępowania baseline lub wyniku kontekstu.
3. Podsumuj iteracje i czas. Po kryteriach lub limicie zakończ pętlę; w trybie wczesnym wróć do wskazanego etapu.

## Artefakty wyjściowe i lokalizacje

- `P/reports/correction-01/report.md`
- `P/reports/correction-01/metrics.json`
- `P/reports/correction-01/regressions.json`
- `P/reports/correction-01/human-review.md`

## Kryteria zakończenia i kontrole

Porównanie tych samych mianowników; zero ukrytych regresji; człowiek ponownie ocenia zmienione znaczenie. Koniec budżetu zapisany, nie obchodzony.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Kolejna inferencja w tej karcie, ukrywanie błędów przez zmianę testów/oczekiwań.

## Przegląd człowieka

Właściciel akceptuje znaczenie poprawek lub utrzymuje pending/blocked; sam format nie wystarcza.

## Wznowienie

Czytaj report.md i listę pending; każde ponowne review wskazuje konkretny hash odpowiedzi.

## Przekazanie

M-POC7A dostaje końcowy wynik i koszt; ewentualna kolejna M-POC6A wymaga pozostałego budżetu.
