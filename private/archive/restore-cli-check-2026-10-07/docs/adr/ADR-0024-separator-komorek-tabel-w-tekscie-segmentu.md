# ADR-0024: Komórki tabel w tekście segmentu rozdziela tabulator, bez zmiany wersji ekstraktorów

- **Status:** zastąpiony przez ADR-0032
- **Data:** 2026-10-05
- **Milestone:** M9a

## Kontekst
- Zadanie `wgc.tables.parse` (M9a) buduje rekord `table` z tekstu segmentu w `.glu/source/`. Do M9a oba ekstraktory
  łączyły komórki wiersza tabeli spacją (`wgc.ingest.markdown@0`, `wgc.ingest.pdf@0`, ADR-0021 „Tekst”). Tekst
  `SEG-dsk.4.3` miał wiersze `4 or less No effect` i `5–6 Routed`, których nie da się jednoznacznie podzielić na kolumny.
- ADR-0021 ustala, że zmianę reguł ekstraktora wprowadza nowa wersja `wgc.ingest.pdf@N`. Podbicie wersji daje
  `extractor_changed` w każdym inwentarzu i wymaga ponownej ekstrakcji, a fixture'y i inwentarz gry benchmarkowej
  zmieniają pole `extractor`.
- `text_hash` liczy się z tekstu po `normalize_text`, która zwija każdy ciąg białych znaków do jednej spacji
  (DATA-CONTRACTS §5). Tabulator i spacja dają ten sam hash.

## Decyzja
- W wierszu tabeli komórki rozdziela tabulator (`CELL_SEP = "\t"` w `wgc.ingest.markdown` i `wgc.ingest.pdf`):
  - Markdown: każdy wiersz tabeli, z pustymi komórkami (kolumny się nie przesuwają);
  - PDF: wiersze segmentu typu `table`; w pozostałych segmentach komórki nadal łączy spacja.
- Wersje ekstraktorów zostają `@0`. Zmienia się tylko zapis białych znaków w cache tekstu, nie segmentacja, typy,
  etykiety ani `text_hash`. To jedyny wyjątek od reguły ADR-0021 o wersjonowaniu; reguła obowiązuje dla każdej zmiany,
  która zmienia `text_hash`, segmenty albo pola inwentarza.
- Testy pilnują, że tekst z tabulatorem ma ten sam `text_hash` co tekst ze spacjami (Markdown i PDF), a inwentarz gry
  benchmarkowej i fixture'y są bez zmian.

## Konsekwencje
- `wgc.tables.parse` dzieli wiersze po tabulatorze, bez heurystyk.
- Cache tekstu zapisany przed tą zmianą ma ten sam `text_hash`, ale nie ma tabulatorów. `wgc source verify` tego nie
  wykryje. Zgłasza to dopiero zadanie tabel („uruchom `wgc source extract`”), a naprawą jest ponowne `wgc source extract`.
- Komórka PDF zawinięta w kilka wierszy nadal daje osobne wiersze (ADR-0021).

## Odrzucone warianty
- **`wgc.ingest.*@1`:** `extractor_changed` i zmiana pola `extractor` w każdym inwentarzu bez zmiany żadnego hasha.
- **Osobny plik ze strukturą tabeli w `.glu/source/`:** drugi format cache do utrzymania i weryfikacji.
- **Podział wierszy heurystyką na tekście ze spacjami:** komórki z kilku słów (`No effect`, `4 or less`) są
  nierozróżnialne od granic kolumn.
