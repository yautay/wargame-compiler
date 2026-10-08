# ADR-0001: Czysty start: nowe repo, bez kompatybilności wstecznej

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0 (Session 0)

## Kontekst
Prompt architektoniczny zakłada pracę w istniejącym `wargame_utils` (§0, §44, §51: zmiany addytywne, kompatybilność).
Właściciel zdecydował inaczej: nowe narzędzie powstaje w osobnym katalogu, **bez obowiązku kompatybilności wstecznej**
i bez wzorowania się na implementacjach SPQR, GCACW itd. Doświadczenia z tamtych projektów mają zostać wykorzystane.
Analiza (`docs/ARCHAEOLOGY.md`) pokazała, że:
- kontrakt `wgu/kb@1` opiera się na wolnym Markdownie (`when`, `effect`, `exceptions`),
- baza wiedzy jest pisana po polsku,
- etap digitalizacji nie był nigdy uruchomiony na żadnej grze.

## Decyzja
`C:/dev/wargame-compiler` to nowe repozytorium z nowymi kontraktami (`wgc/*@0`). Nie importuje kodu `wgu` i nie
utrzymuje formatu `wgu/kb@1`. Dotychczasowa praca przechodzi do nowego repo na trzy sposoby:
1. jako wnioski w `docs/ARCHAEOLOGY.md`;
2. jako świadomie przeniesione, sprawdzone idee: glosariusz pojęciowy z dowodami, pomiar oprawy PDF, API makr LaTeX,
   trzy przebiegi weryfikacji, testy weryfikatorów na wstrzykniętych błędach;
3. jako opcjonalny importer `kb@1` w roadmapie (M-LEG), wyłącznie źródło danych do prywatnego benchmarku
   (np. GCACW-PL, 238 reguł).

## Konsekwencje
- Rule IR, ID i provenance można zaprojektować swobodnie.
- Stare repozytoria gier zostają przy `wgu`. Przeniesienie konkretnej gry to osobna decyzja właściciela.
- Ekstrakcję PDF i pipeline LaTeX trzeba zbudować od nowa. Stary kod służy do czytania, nie do kopiowania.

## Odrzucone warianty
- Addytywne rozszerzanie `wargame_utils`: utrwala polskojęzyczną KB i wolny tekst jako kontrakt.
- Fork `wargame_utils`: dziedziczy nazwy, CLI i plugin, które kolidowałyby ze starym narzędziem.
