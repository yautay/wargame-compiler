# M-POC6A: Jedna ograniczona korekta w rozmowie

- **ID:** M-POC6A
- **Milestone:** M-POC6
- **Rola:** Codex w ręcznej rozmowie; właściciel przy kwestiach znaczenia
- **Zależności:** Raport z M-POC3, M-POC4B lub M-POC5; budżet korekt niewyczerpany.

## Cel i pytanie eksperymentalne

Uzyskać poprawkę z zachowaniem historii i mierzalnym kosztem. Czy konkretny raport błędów pozwala poprawić wynik bez nowych regresji?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `docs/POC-PLAN.md (pętla korekt i limity)`
- `P/runs/first-001/run.json`
- `P/reports/first-001/report.md`
- `P/measurement/sessions.jsonl`
- `P/formats/proposal-format-v1.md`

## Wejścia i wersja oceny

eval-v1 bez zmiany; konkretny raport i hash rodzica. Dla błędów późniejszych czytaj P/reports/context-01/report.md, P/reviews/semantic-01/issues.json i P/reviews/situations-01/issues.json, jeśli istnieją.

## Wymagane działania

1. Przed próbą wybierz ograniczony pakiet ID błędów, przyczyny, dowody i spodziewany zakres zmiany. Zapisz correction-01/parent.json z dokładnymi ścieżkami raportów i hashami.
2. Uzyskaj kompletną poprawioną odpowiedź ręcznie, zachowaj prompt i surowe bajty osobno. Bez lokalnego łatania.
3. Zapisz czas i numer próby. Tryb wczesny formatu: najwyżej jedna próba; wszystkie korekty łącznie do trzech. Każda kolejna to nowa sesja i correction-02/03.

## Artefakty wyjściowe i lokalizacje

- `P/corrections/correction-01/parent.json`
- `P/corrections/correction-01/prompt.txt`
- `P/corrections/correction-01/response.raw.txt`
- `P/corrections/correction-01/run.json`
- `P/measurement/sessions.jsonl`

## Kryteria zakończenia i kontrole

Rodzic i raport istnieją przed korektą; pierwszy wynik niezmieniony; limit czasu/iteracji sprawdzony; brak odpowiedzi jawny.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Nadpisanie odpowiedzi, fixture zamiast modelu, nieograniczone retry, zmiana gold.

## Przegląd człowieka

Rozstrzygnięcie niejednoznaczności źródła wymaga człowieka; odwracalny zapis pakietu nie wymaga dodatkowej zgody.

## Wznowienie

Sprawdź parent.json, odpowiedź i licznik prób. Nie licz istniejącej odpowiedzi jako nowej; po przerwaniu zapisz faktyczny koszt.

## Przekazanie

M-POC6B ponawia właściwe kontrole, następnie wraca do przerwanego M-POC3/4/5 lub kończy pętlę.
