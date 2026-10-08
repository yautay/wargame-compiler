# ADR-0032: Wersjonowany hash struktury segmentu (`struct_hash`) obok `text_hash`, ekstraktory `@1`

- **Status:** przyjęty (zastępuje ADR-0024; rozszerza listę pól generowanych segmentu i warunek usunięcia `verified_by_render` z ADR-0020); wersja projekcji podbita do `@2` przez ADR-0034, `prov.inputs_hash` przedefiniowany przez ADR-0033
- **Data:** 2026-10-06
- **Milestone:** M-STAB3a

## Kontekst
- `text_hash` liczy się z `normalize_text`, która zwija każdy ciąg białych znaków do spacji (DATA-CONTRACTS §5). Nie
  zależy więc ani od zawijania wierszy, ani od tabulatora między komórkami. ADR-0024 wprowadził tabulator jako
  separator komórek bez zmiany wersji ekstraktorów i bez zmiany hasha.
- Ustalenie F03 [przeglądu po M9a](../reviews/2026-10-05-przeglad-po-M9a.md): w cache segmentu `SEG-dsk.4.3` zmieniono
  `4 or less<TAB>No effect` na `4<TAB>or less No effect`. `text_hash`, klucz joba planera i `wgc source verify` zostały
  bez zmian, a `wgc.tables.parse` dało inny pierwszy wiersz (`[{min: null, max: 4}, "No effect"]` →
  `[4, "or less No effect"]`). Przyszły cache wyników (M11) zwróciłby pod tym samym kluczem inny wynik.
- Strukturę czytają oba zadania Tier 0:
  - `wgc.tables.parse` dzieli tekst na wiersze i komórki;
  - `wgc.terms.harvest` szuka pozycji listy numerowanej wiersz po wierszu (`wgc/terms.py`, `matches`).

  Problem dotyczy więc wierszy we wszystkich segmentach, nie tylko komórek tabel.
- Decyzja N03 przeglądu: wariant B, czyli dodatkowy wersjonowany hash struktury obok znormalizowanego hasha tekstu.

## Decyzja
- **`struct_hash`** (pole segmentu w `wgc/source@0`, opcjonalne w schemacie, zapisywane przez ekstraktory `@1`):
  - definicja: `content_hash({format: "wgc/struct@0", lines: structure(tekst)})`;
  - `structure` (`wgc.canonical`) daje listę wierszy, a każdy wiersz to lista komórek. Tekst w NFC, końce wierszy LF,
    podział po LF i po tabulatorze (`CELL_SEP`), w komórce zwinięte białe znaki. Pomijany jest pusty wiersz bez
    tabulatora; wiersz pustych komórek zostaje. Przeniesień się nie łączy;
  - wersja `wgc/struct@N` jest częścią hashowanej treści. Każda zmiana `structure` to nowa wersja i nowa wersja
    ekstraktorów.
- **Podział ról hashy:**
  - `text_hash` to hash tekstu niezależny od zawijania. Używają go kotwice (`seg_hash`), wykrywanie nieaktualnych
    kotwic (`anchor_hash_mismatch`) i parytet Markdown ↔ PDF;
  - `struct_hash` to hash wejścia zadań. Jest w projekcji `logic` segmentu (`wgc/projection@1`), więc wchodzi do
    `input_hash` klucza joba i do `prov.inputs_hash`. Sprawdza go też bramka tekstu `Workspace.text`.
- **Parsery** czytają tekst wyłącznie przez `structure`: `wgc.tables.parse` (wiersze z co najmniej dwiema komórkami)
  i `wgc.terms.harvest` (wiersze listy). Równy `struct_hash` daje więc równy wynik. Wersje zadań się nie zmieniają,
  bo dla tego samego tekstu wynik jest taki sam.
- **Bramka tekstu:** `Workspace.text` (planner, parsery, cytaty kotwic w `accept()`) odmawia (`KBError`, „uruchom
  `wgc source extract`”) w trzech przypadkach:
  - segment bez `struct_hash`;
  - tekst w `.glu/source/` z innym `text_hash`;
  - tekst w `.glu/source/` z innym `struct_hash`.

  `glu build` kończy się wtedy kodem 2, zanim powstanie build.
- **Verify:**
  - `segment_struct_mismatch`: ponowna ekstrakcja daje ten sam `text_hash` i inny `struct_hash`;
  - `cache_mismatch`: cache niezgodny z `text_hash` albo z `struct_hash`;
  - `struct_hash_missing`: segmenty dokumentu bez `struct_hash`.

  Wszystkie trzy to błędy.
- **Ekstraktory `wgc.ingest.markdown@1` i `wgc.ingest.pdf@1`.** Segmentacja i tekst są jak w `@0` po ADR-0024;
  nowością jest `struct_hash` w inwentarzu. Wraca reguła ADR-0021: zmiana pól inwentarza to nowa wersja ekstraktora.
  Wyjątek z ADR-0024 przestaje obowiązywać.
- **Jawna regeneracja.** Inwentarz z ekstraktora `@0` daje:
  - w `verify`: błąd `struct_hash_missing` i ostrzeżenie `extractor_changed`;
  - w każdym zadaniu: odmowę odczytu tekstu.

  Naprawą jest `wgc source extract`. Przepisuje cache, więc znika też cache sprzed ADR-0024 bez tabulatorów. Samo
  dopisanie `struct_hash` nie jest zmianą segmentu (`verified_by_render` zostaje). Zmiana `struct_hash` przy
  późniejszej ekstrakcji usuwa `verified_by_render`, tak jak zmiana `text_hash`.

## Konsekwencje
- Ten sam tekst w innych komórkach albo wierszach daje inny klucz joba, inny `prov.inputs_hash` i błąd `verify`.
  Rozstrzyga to F03 dla planera, parsera, provenance i verify (testy `tests/test_struct_hash.py`).
- Kotwice nie zmieniają się: `seg_hash` to nadal `text_hash`, więc przezawijanie nie unieważnia kotwic ani nie
  blokuje `accept()` (Q-12).
- Rekord już zaakceptowany nie staje się nieaktualny przez samą zmianę `struct_hash`, bo walidator nie przelicza
  `prov.inputs_hash`. Ponowny build zastępuje go wynikiem z nowym `inputs_hash`, bo klucz joba się zmienia.
  Wykrywanie nieaktualności przez `inputs_hash` to M13 (graf, invalidacja, Q-12).
- Pierwszy build po regeneracji zapisuje istniejące rekordy `TAB-` i `CON-` z nowym `prov.inputs_hash`
  (jednorazowo `zmienione`), bo projekcja segmentu ma nowe pole.
- **Przyjęty koszt:**
  - przezawijanie akapitu (nowe wydanie PDF z tym samym tekstem, inna szerokość kolumny) zmienia `struct_hash`, a więc
    klucze jobów wszystkich zadań czytających ten segment. Od M11 to missy cache także dla zadań modelowych;
  - `verify` zgłasza wtedy `segment_struct_mismatch`;
  - `struct_hash` segmentów PDF i Markdown z tym samym tekstem zwykle się różni.

  Bezpieczny kierunek: zadanie, które czyta wiersze lub komórki, nigdy nie dostaje starego klucza.
- Projekcja segmentu tylko z `text_hash`, dla zadań, które dowodnie czytają tylko `normalize_text`, to temat M-STAB3b
  (projekcje). Dziś takich zadań nie ma.
- `prov.inputs_hash` pojęcia z harvest obejmuje tylko segmenty jego kotwic, a `input_hash` joba obejmuje wszystkie
  wejścia. Rozdział dowodów rekordu od manifestu wywołania to M-STAB3b (F05).

## Odrzucone warianty
- **Hash tylko struktury tabel (tylko segmenty `table`):** harvest czyta wiersze każdego segmentu, więc zmiana wiersza
  w liście faz przeszłaby bez zmiany klucza.
- **Hash surowych bajtów artefaktu (`.glu/source/*.txt`):** zależy od białych znaków wewnątrz komórek i pustych
  wierszy, których żaden parser nie czyta. Dałby missy bez zmiany wyniku.
- **`struct_hash` w kotwicy (`anchors[].struct_hash`) i nowy kod walidatora:** każde przezawijanie unieważniłoby
  kotwice reguł modelowych i zablokowało `accept()` (Q-12). Zależność rekordu od struktury niesie `prov.inputs_hash`.
- **Flaga zadania „czytam strukturę”, domyślnie tylko `text_hash`:** zadanie, które zapomni flagi, a czyta wiersze lub
  komórki, powtórzyłoby F03 po cichu pod cache M11. Domyślnie bezpieczniej jest uwzględniać strukturę.
- **Bez nowej wersji ekstraktorów, tylko `struct_hash_missing`:** łamie regułę ADR-0021 i zostawia w inwentarzu
  `@0`, które nie mówi, że artefakt ma tabulatory i `struct_hash`.
