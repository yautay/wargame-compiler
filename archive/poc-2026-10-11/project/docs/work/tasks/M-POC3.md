# M-POC3: Raport pierwszego wyniku

- **ID:** M-POC3
- **Milestone:** M-POC3
- **Rola:** Codex; przegląd wspólny rozbieżności
- **Zależności:** M-POC2B; odpowiedź lub udokumentowany brak.

## Cel i pytanie eksperymentalne

Utrwalić uczciwy baseline przed poprawkami. Co jest poprawne strukturalnie, czego brakuje i co wymaga dalszej oceny?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/runs/first-001/response.raw.txt`
- `P/runs/first-001/run.json`
- `P/inputs/v1/manifest.json`
- `P/formats/proposal-format-v1.md`
- `P/evaluation/eval-v1/manifest.json`
- `P/evaluation/eval-v1/inventory.json`
- `P/evaluation/eval-v1/expectations.json`
- `P/evaluation/eval-v1/dependencies.json`

## Wejścia i wersja oceny

Oryginalna odpowiedź oraz zamrożony eval-v1; dokładną nazwę pobranego pliku ustala run.json.

## Wymagane działania

1. Sprawdź format, unikalność ID, referencje, wiązanie wejść, cytaty i obszary obrazów. Zapisz oddzielną reprezentację bez zmiany treści.
2. Porównaj z inwentarzem, rozdziel sześć klas błędów z planu. Podaj liczniki i sprawdzone mianowniki; nieocenialne pola oznacz not_assessable.
3. Zamknij raport przed korektą. Jeśli format blokuje ocenę, zapisz baseline i przejdź przez ograniczony tryb M-POC6A/B, potem wróć do tej karty.

## Artefakty wyjściowe i lokalizacje

- `P/proposals/first-001/proposal.json i provenance.json`
- `P/reports/first-001/format.json`
- `P/reports/first-001/inventory.json`
- `P/reports/first-001/report.md`
- `P/reports/first-001/metrics.json`

## Kryteria zakończenia i kontrole

Każdy element ma wynik lub jawną nieocenialność; surowy hash bez zmian; raport datowany przed korektą. Schemat nie oznacza akceptacji.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Domykanie wszystkich zależności, semantyczna akceptacja bez człowieka, zmiana eval-v1.

## Przegląd człowieka

Wspólne rozstrzygnięcie klasy błędu i kwestii źródłowych; nierozstrzygnięcia pozostają w raporcie.

## Wznowienie

Wznowienie z report.md i listy nieocenionych ID; po korekcie użyj nowego raportu i zachowaj pierwszy.

## Przekazanie

M-POC4A otrzymuje listę zależności blokujących; M-POC5 otrzyma jawny baseline.
