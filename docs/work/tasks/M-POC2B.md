# M-POC2B: Pierwsza ręczna ekstrakcja

- **ID:** M-POC2B
- **Milestone:** M-POC2
- **Rola:** Codex w ręcznej sesji; właściciel obsługuje przekazanie
- **Zależności:** M-POC2A; właściciel ręcznie otwiera czystą sesję bez historii oceny.

## Cel i pytanie eksperymentalne

Uzyskać pierwszy wynik bez znajomości oczekiwanych odpowiedzi. Jakiej jakości propozycję reguł i zależności daje pierwszy odczyt?

## Dokładne pliki do przeczytania

Wyjątek od bootstrapu: ekstraktor czyta **wyłącznie odseparowany pakiet**.
Nie otwiera STATUS, HANDOFF, planu z podsumowaniem ocen ani repo z evaluation/.
Przygotowanie i późniejszą ocenę prowadzi osobna sesja według
[playbooka](../../SESSION-PLAYBOOK.md); jego treści nie przekazujemy ekstraktorowi.
Ścieżki poniżej opisują kanoniczne artefakty; `P/` oznacza
`private/poc/spqr-chapter9/`. W odseparowanym katalogu przekazania są tylko
`inputs/`, `formats/` i `prompts/`; metadane freeze skopiowano bajtowo do inputs/v1/.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/inputs/v1/manifest.json`
- `P/inputs/v1/transfer-list.txt`
- `P/prompts/first-v1.txt`
- `P/formats/proposal-format-v1.md`
- `P/formats/synthetic-example-v1.json`
- `P/inputs/v1/freeze-public-v1.json`

## Wejścia i wersja oceny

Wyłącznie pliki z transfer-list; eval-v1 jako ID/hash bez treści. Nie czytać evaluation/eval-v1, raportów ani prywatnych handoffów oceny.

## Wymagane działania

1. Sprawdź hashe pakietu i brak oczekiwanych odpowiedzi w kontekście. Jeśli je widziano, oznacz contaminated i nie udawaj ślepej próby.
2. W ręcznej sesji wykonaj prompt; proponowana konfiguracja GPT 6.1 Sol / wysoki. Bez API, GUI i uruchamiania procesu inferencji.
3. Zachowaj całą odpowiedź w oryginalnych bajtach, metadane i dostępny czas. Brak odpowiedzi zapisz jako waiting_response, bez fixture’a.

## Artefakty wyjściowe i lokalizacje

- `P/runs/first-001/response.raw.txt (lub oryginalny pobrany plik)`
- `P/runs/first-001/run.json`
- `P/runs/first-001/session-evidence.txt`
- `P/measurement/sessions.jsonl`

## Kryteria zakończenia i kontrole

Jeden pierwszy wynik; prompt i wszystkie wejścia znane; rzeczywista aplikacja/model/rozumowanie lub unknown, hashe i odbiór zapisane. Nie poprawiać odpowiedzi na tym etapie.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Oglądanie klucza oceny, korekty, lokalne uzupełnianie wyniku, akceptacja znaczenia.

## Przegląd człowieka

Właściciel potwierdza fakty przekazania i widoczną konfigurację; to nie akceptacja reguł.

## Wznowienie

Najpierw sprawdź run.json i plik odpowiedzi. Nie nadpisuj first-001; jawne ponowienie ma nowe ID i liczy czas.

## Przekazanie

M-POC3 otrzymuje oryginał, metadane i hashe; dopiero oceniający otwiera eval-v1.
