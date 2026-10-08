# ADR-0036: Jawny hybrydowy ingest PDF z dowodami stron

- **Status:** docelowy kierunek zastąpiony przez [ADR-0037](ADR-0037-ekstrakcja-desktop-bez-api.md); implementacja pozostaje legacy
- **Data:** 2026-10-06
- **Milestone:** Q-11

## Kontekst

Ekstraktor `wgc.ingest.pdf@1` z ADR-0021 zakłada jedną kolumnę. Próba na prywatnym podręczniku pokazała sklejanie kolumn, fałszywe tabele i duplikat etykiety `1`. Sam render jest dostępny, ale układ strony wymaga interpretacji. M10 nie dostarczył jeszcze wspólnej granicy providera.

## Decyzja

- Dotychczasowy PDF `@1` pozostaje domyślny. `wgc source hybrid --doc SRC-…` jawnie wybiera `wgc.ingest.pdf.hybrid@2` dla jednego dokumentu.
- Kod wydobywa słowa, ich ID i współrzędne z warstwy PDF oraz renderuje każdą stronę. `--prepare` eksportuje te pakiety do `.glu` dla asystenta w Codex lub Claude Desktop, a replay czyta jego pliki `pNNN.json`. `--codex` może uruchomić zalogowany Codex CLI bez klucza API. Wąski adapter programu przyjmuje JSON przez stdin i oddaje JSON przez stdout. Model wybiera kolejność, typy i granice segmentów, wyłączenia, nierozstrzygnięte obszary i widoczny tekst bez warstwy tekstowej. Nie nadaje ID ani hashy.
- Każda strona przechodzi kontrole kompletności słów, jednokrotnego użycia, zgodności tekstu, granic obszarów i komórek tabel. Po błędzie jest najwyżej jedno ponowienie z renderem w wyższej rozdzielczości i diagnostyką. Kolejny błąd, strona bez warstwy tekstowej, nierozstrzygnięty obszar lub tekst tylko na obrazie wymaga przeglądu. Nie tworzymy pustego segmentu OCR.
- Wynik zatwierdzony trafia do ignorowanego `.glu/source/<SRC-id>/hybrid/approved.json`; raport, także przy niepowodzeniu, do `report.json`, a ostatnie propozycje stron do `proposals/pNNN.json`. Inwentarz przechowuje wersję ekstraktora, hash artefaktu i obszary dla wszystkich stron segmentu. Tekst oraz wiersze i komórki tabel pozostają tylko w `.glu`. `source verify` odczytuje zapisany wynik, wiąże go z hashem PDF, sprawdza propozycje względem aktualnej warstwy tekstowej i porównuje hashe i obszary segmentów, bez wywołania providera.
- ID segmentu jest kodowym kluczem pozycyjnym `p<strona>s<kolejność>`. Etykiety wydrukowane są metadanymi i mogą się powtarzać. Kontynuacja segmentu przez stronę przenosi obszary obu stron.

## Konsekwencje

- Testy automatyczne używają syntetycznych PDF-ów i fake/replay, bez sieci, GPU i modelu.
- Propozycja musi jawnie oznaczać paginy i inne wyłączone słowa z powodem. Niepewnej strony nie ma w zatwierdzonym inwentarzu.
- Nie ma automatycznego OCR ani uniwersalnego systemu analizy dokumentów. Człowiek może poprawić propozycję w pliku replay i ponowić jawne polecenie.
- Jakość na prywatnym podręczniku wymaga pilota z dostępnym płatnym providerem i porównania renderów. Bez niego Q-11 pozostaje otwarta.
