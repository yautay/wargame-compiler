# M-POC5A: Przegląd znaczenia reguł

- **ID:** M-POC5A
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** M-POC4 z domknięciem lub jawnymi blokadami.

## Cel i pytanie eksperymentalne

Ocenić semantykę wobec źródła. Czy warunki, skutki, wyjątki, liczby, negacje i ograniczenia czasowe zachowano?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/evaluation/eval-v1/manifest.json`
- `P/evaluation/eval-v1/expectations.json`
- `P/evaluation/eval-v1/inventory.json`
- `P/evaluation/eval-v1/dependencies.json`
- `P/reports/first-001/report.md`
- `P/reports/context-01/report.md`
- `P/proposals/context-01/proposal.json`
- `P/proposals/first-001/proposal.json`
- `P/inputs/v1/manifest.json`
- `P/context/pass-01/manifest.json`

## Wejścia i wersja oceny

eval-v1, źródła wskazane manifestami, wybrany hash odpowiedzi. Przy braku rundy kontekstu użyć first-001 i zapisanego n/a.

## Wymagane działania

1. Porównaj każde oczekiwanie krytyczne i resztę inwentarza ze źródłem, w tym tabele, diagramy, noty i zakres wyjątku. Oceniaj osobno pierwszy wynik i wynik po kontekście na tym samym eval-v1; zapisz dwa zestawy ocen z hashami odpowiedzi. Nieocenialny pierwszy wynik pozostaje not_assessable, naprawa formatu ma osobną kolumnę. Nie zmieniaj raportu M-POC3.
2. Zapisz odrębnie błąd odczytu, interpretacji, brak kontekstu i niejednoznaczność. Nie poprawiaj oryginalnej odpowiedzi.
3. Nadaj stany reviewed/pending/blocked tylko z recenzentem i dowodem. Krytyczny brak blokuje zależne rozstrzygnięcia.

## Artefakty wyjściowe i lokalizacje

- `P/reviews/semantic-01/checklist.json`
- `P/reviews/semantic-01/review.md`
- `P/reviews/semantic-01/issues.json`

## Kryteria zakończenia i kontrole

Pełny spis ocenionych i nieocenionych oczekiwań, brak modelowej autoakceptacji; wszystkie liczby/negacje/wyjątki krytyczne sprawdzone.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Silnik gry, przyjęcie docelowego kontraktu, semantyczna akceptacja wyłącznie testem.

## Przegląd człowieka

Właściciel rzeczywiście porównuje reguły z dowodami i zapisuje zakres akceptacji; brak udziału = waiting_review.

## Wznowienie

Od pierwszego pending w checklist.json; zmiana hasha wyniku unieważnia podstawę wcześniejszej oceny dotkniętych elementów.

## Przekazanie

M-POC5B otrzymuje wynik przeglądu i listę blokowanych reguł; błędy do M-POC6A.
