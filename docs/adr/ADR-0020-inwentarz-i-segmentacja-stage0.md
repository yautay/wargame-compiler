# ADR-0020: Inwentarz Stage 0, segmentacja Markdown, ID segmentów i domyślne pierwszeństwo źródeł

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M2a

## Kontekst
- Kontrakt `wgc/source@0` z M0 opisuje `source_document` i `segment`, ale nie mówi:
  - jak powstają segmenty i ich ID;
  - gdzie leży tekst;
  - co dzieje się z polami wpisanymi ręcznie, gdy inwentarz jest generowany ponownie.
- Fixture'y miały placeholderowe hashe oraz `order` wyprowadzony z cyfr etykiety (`3.4` → 34). Ten schemat psuje się
  przy `1.10` i `10.1`.
- Dokument `SRC-dsk.rules` ma segmenty `SEG-dsk.*`, a nie `SEG-dsk.rules.*`, więc prefiksu ID segmentu nie da się
  wyprowadzić z ID dokumentu.
- LOGIC-MODEL ([pierwszeństwo źródeł](../LOGIC-MODEL.md#pierwszenstwo-zrodel)) zapowiadał role `living_rules`
  i `community_interpretation` oraz domyślną kolejność według roli.

## Decyzja
- **Inwentarz:**
  - `source/inventory.yaml` to jeden dokument `wgc/source@0`, commitowany.
  - Zapisują go `wgc source init|scan|extract` deterministycznie: stała kolejność pól, jeden rekord w wierszu,
    segmenty w kolejności dokumentów i `order`.
  - Pola generowane są nadpisywane:
    - w dokumencie: `present`, `file_hash`, `extractor`;
    - w segmencie: `doc`, `label`, `segment_type`, `parent`, `order`, `pages`, `bbox`, `text_hash`, `visual_flags`.
  - Pola ręczne zostają. `verified_by_render` znika, gdy zmienia się `text_hash`.
  - Komentarze nie są zachowywane.
- **Tekst segmentów:**
  - leży w `.glu/source/<SRC-id>/<SEG-id>.txt` (ADR-0012);
  - `extract` odtwarza go deterministycznie i usuwa pliki segmentów, których już nie ma;
  - `verify` porównuje cache, ponowną ekstrakcję i `file_hash` z inwentarzem.
- **ID segmentu:**
  - ma postać `SEG-<seg_prefix>.<klucz>`;
  - nowe opcjonalne pole `source_document.seg_prefix` domyślnie jest kluczem ID `SRC-`;
  - `wgc source init` nadaje pierwszemu dokumentowi `rules` prefiks równy kodowi gry;
  - klucz to etykieta, jak wydrukowana (`3.4`, `1.0`), albo `u<n>` dla n-tego segmentu bez numeru;
  - powtórzona etykieta w dokumencie jest błędem ekstrakcji.
- **Segmentacja Markdown (`wgc.ingest.markdown@0`):**
  - Nagłówek to segment `heading`, a liczba na jego początku staje się etykietą.
  - `**N.N**` na początku wiersza otwiera segment, który biegnie do następnego znacznika albo nagłówka, razem z pustymi
    wierszami, listami i tabelami.
  - Segment z tabelą Markdown ma typ `table`, pozostałe numerowane mają typ `rule`.
  - Treść bez numeru (tytuł, wstęp) tworzy segmenty `heading` albo `other`.
  - Etykieta nie należy do tekstu.
  - Tekst jest „jak wydrukowany”:
    - znika markup inline, znaczniki cytatu i punktorów, pionowe kreski tabel i wiersz separatora;
    - numery list zostają.
  - `parent` to najbliższy wcześniejszy nagłówek, a dla nagłówka najbliższy wcześniejszy nagłówek wyższego rzędu.
  - `order` to pozycja w dokumencie liczona od 1.
- **Ekstraktory:**
  - ekstraktor to czysta funkcja: bajty dokumentu na wejściu, lista segmentów na wyjściu;
  - rejestr rozszerzeń jest w `wgc/ingest`;
  - M2b dopisze PDF.
- **Role i pierwszeństwo:**
  - Do `source_document.role` dochodzą `living_rules` i `community_interpretation`.
  - Domyślne pierwszeństwo jest danymi w kodzie (`wgc.source.DEFAULT_PRECEDENCE`):
    errata 60 > living_rules 50 > rules 40 > faq 30 > designer_clarification 20 > community_interpretation 10.
  - Drukowane komponenty (`scenario_book`, `charts`, `cards`, `counters`, `map`, `module`) mają pozycję `rules`, więc
    konflikt z regułami daje `AMB-`.
  - `prior_translation` i `other` nie mają wartości domyślnej.
  - Jawne `precedence` w inwentarzu nadpisuje wartość domyślną; politykę w `project.yaml` dodaje M7.
- **Walidator:** `segment.parent` jest referencją sprawdzaną przez `unresolved_ref`.

## Konsekwencje
- Kolejne przebiegi `extract` dają identyczny inwentarz co do bajtu. Zmiana tekstu reguły zmienia jej `text_hash`,
  a walidator zgłasza nieaktualne kotwice (`anchor_hash_mismatch`).
- Segmenty bez numeru mają klucze zależne od pozycji (`u1`, `u2`, …): wstawienie wstępu przenumeruje je. Nie należy
  kotwiczyć do nich reguł.
- Kotwice z cytatem z segmentu tabeli muszą cytować tekst bez pionowych kresek.
- Ręczne notatki w inwentarzu trzeba zapisywać w polu `notes`, nie w komentarzach.
- `bench/minigame/source/inventory.yaml` jest commitowany. Fixture `source.minigame.yaml` jest jego podzbiorem,
  a test pilnuje zgodności. Obu nie waliduje się w jednym przebiegu, bo dałoby to `duplicate_id`.

## Odrzucone warianty
- **ID segmentu z pełnego klucza `SRC-` (`SEG-dsk.rules.3.4`):** zmienia wszystkie kotwice i jest długie dla głównych
  reguł.
- **Segment do pustego wiersza:** 4.3 traci tabelę, a 2.2 listę.
- **`order` z cyfr etykiety:** niejednoznaczny przy `1.10` i `10.1`.
- **Zapisywanie domyślnego `precedence` w inwentarzu:** utrwala wartość obliczaną (ADR-0011) i miesza ją
  z jawnymi decyzjami właściciela.
- **Tekst segmentów w jednym pliku JSON na dokument:** pliki per segment łatwiej porównać i sprawdzić ręcznie, a
  ekstrakcja i tak jest deterministyczna.
