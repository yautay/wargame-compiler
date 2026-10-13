# M-POC7B: Decyzja właściciela i następny plan

- **ID:** M-POC7B
- **Milestone:** M-POC7
- **Rola:** Właściciel; przegląd wspólny
- **Zależności:** M-POC7A i dostępny właściciel do przeglądu.

## Cel i pytanie eksperymentalne

Zamknąć eksperyment rzeczywistą decyzją i zakresem dalszej pracy. Kontynuować, poprawić metodę czy odrzucić obecne podejście?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/decision/comparison-index.json`
- `P/decision/comparison.md`
- `P/decision/architecture-options.md`
- `docs/POC-PLAN.md`
- `docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md`
- `docs/ROADMAP.md`

## Wejścia i wersja oceny

Ta sama zamrożona ocena co raporty; podstawa decyzji wyliczona hashami w comparison-index.json.

## Wymagane działania

1. Przejrzyj krytyczne dowody i wynik progów; zapisz decyzję człowieka, zakres akceptacji oraz powody.
2. Dla kontynuacji zaproponuj minimalny następny kontrakt/magazyn/orkiestrację; dla poprawy nowy ograniczony eksperyment; dla odrzucenia zachowaj negatywny wynik.
3. Zapisz kolejny ADR (następny wolny numer od ADR-0040) i nowy plan tylko w zatwierdzonym zakresie. Uaktualnij STATUS/ROADMAP/HANDOFF i regułę next po zakończeniu eksperymentu.

## Artefakty wyjściowe i lokalizacje

- `P/decision/human-decision.md`
- `docs/adr/ADR-0040-<temat-decyzji>.md (lub następny wolny numer)`
- `docs/adr/README.md`
- `docs/ROADMAP.md, docs/STATUS.md, docs/HANDOFF.md i nowy handoff`

## Kryteria zakończenia i kontrole

Recenzent, data, dowody, decyzja i ograniczenia zapisane; publiczne dokumenty nie ujawniają SPQR. Bez człowieka etap pozostaje waiting_review.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Implementacja następnej architektury, pozorna akceptacja przez model, zmiana historii wyników.

## Przegląd człowieka

Obowiązkowa decyzja właściciela o kierunku i akceptacji znaczenia. Żaden inny wykonawca jej nie zastępuje.

## Wznowienie

Czytaj human-decision.md; jeśli brak decyzji, przedstaw istniejące porównanie, nie powtarzaj inferencji.

## Przekazanie

Następna sesja wykonuje dopiero zatwierdzony nowy plan; archiwum pozostaje zachowane.
