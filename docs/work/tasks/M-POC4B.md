# M-POC4B: Odpowiedź z kontekstem i jej kontrola

- **ID:** M-POC4B
- **Milestone:** M-POC4
- **Rola:** Codex w ręcznej sesji; przegląd wspólny
- **Zależności:** M-POC4A; runda w budżecie. Jeżeli kontekst niepotrzebny, udokumentowane n/a bez wywołania.

## Cel i pytanie eksperymentalne

Oddzielić poprawę wynikającą z kontekstu od późniejszych korekt. Które luki zamyka dostarczenie źródła i jakie nowe zależności ujawnia?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/context/pass-01/manifest.json`
- `P/context/pass-01/targets.json`
- `P/context/pass-01/prompt.txt`
- `P/runs/first-001/run.json`
- `P/formats/proposal-format-v1.md`
- `P/reports/first-001/report.md`

## Wejścia i wersja oceny

eval-v1 dla oceniającego; ekstraktor dostaje kontekst, poprzednią propozycję i prompt, bez pełnego klucza oceny.

## Wymagane działania

1. Uzyskaj odpowiedź ręcznie i zachowaj jej bajty, konfigurację, czas i rodzica; nie mieszaj z niezależną korektą znaczenia.
2. Po odbiorze oceniający czyta P/evaluation/eval-v1/manifest.json, expectations.json, dependencies.json, inventory.json; ponawia kontrolę M-POC3.
3. Zmierz zamknięte/nowe luki i przyrost kontekstu. Drugi krok wymaga osobnej sesji M-POC4A/B i nowych pass-02/context-02.

## Artefakty wyjściowe i lokalizacje

- `P/runs/context-01/response.raw.txt i run.json`
- `P/proposals/context-01/proposal.json`
- `P/reports/context-01/report.md i metrics.json`
- `P/measurement/sessions.jsonl`

## Kryteria zakończenia i kontrole

Osobna kolumna po kontekście; wszystkie krytyczne zależności poparte albo blokujące; limit nieprzekroczony, regresje zapisane.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Zastępowanie baseline, niejawne korekty, rozstrzygnięcie bez źródła.

## Przegląd człowieka

Potwierdzenie, czy dostarczony fragment rzeczywiście uzasadnia domknięcie, nie tylko zgoda modelu.

## Wznowienie

Czytaj run.json i report.md; brak odpowiedzi pozostaje waiting_response. Nie wysyłaj ponownie bez odnotowania próby.

## Przekazanie

M-POC5A otrzymuje jawnie wskazany hash wyniku po kontekście lub raport n/a.
