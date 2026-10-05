# ADR-0025: TaskSpec jako interfejs Pythona, `accept()` jako jedyny zapis do `kb/`, wykonawca Tier 0 i planner

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M9a

## Kontekst
- ARCHITECTURE §2 opisuje `TaskSpec` jako kontrakt WGC → GLU, kształtowany w M9: `id`, `version`, `stage`,
  `input_selector`, `context_builder`, `prompt`, `output_schema`, `decoding_schema?`, `deterministic_impl?`,
  `validate`, `risk_features`, `accept`, `semantic_projection`.
- ADR-0002: `glu` importuje `wgc`, `wgc` nigdy nie importuje `glu`. ADR-0004: GLU zapisuje do `kb/` wyłącznie przez WGC.
  ADR-0014: rodzaj provenance nadaje WGC. ADR-0023: stan joba zmienia się tylko przez tabelę przejść, a stan buildu
  ustawia wykonawca.
- Providerzy i pętla structured output to M10, cache M11, router M12, `project.yaml` M7, model ryzyka M6.
- Relacje warstwy scenariusza (`REL-003`: 7.1 nadpisuje 5.2) wyprowadza się z rekordów `R-`, które powstaną w M14.

## Decyzja
- **TaskSpec** to zamrożona dataclass w `wgc/tasks.py`, bez osobnego JSON Schema:
  - obowiązkowe: `id`, `version`, `stage` (`stage1`), `output_kind`, `output_schema` (`wgc/logic@0#table`),
    `input_selector(ws, segmenty) → [wejścia joba]`, `validate(ws, wejścia, propozycje) → komunikaty`;
  - opcjonalne: `deterministic_impl(ws, wejścia) → propozycje` (Tier 0), `semantic_projection` (domyślnie projekcje
    `logic` wejść), `risk_features` (do M6 zwraca pustą listę), `context_builder`, `prompt` i `decoding_schema` (M10);
  - nazwa narzędzia to `id@version` (`prov.by.tool`, klucz cache).
- **`accept` nie jest polem TaskSpec.** Wszystkie zadania przechodzą przez jedną funkcję `wgc.kb.accept()`, żeby zapis
  do `kb/` miał jedną ścieżkę i jedne reguły provenance. Zadanie wpływa na akceptację przez `validate`.
- **Rejestr** to słownik w `wgc.tasks` (`registry()`, `get`, `for_stage`). GLU go importuje; nie ma entry pointów.
- **Propozycja** ma postać `{record, anchors, derived_from}`; `record` bez `prov`, `status` i `risk`
  (DATA-CONTRACTS §10). Schemat `wgc/proposal@0` dochodzi w M10.
- **`wgc.kb.accept(root, spec, inputs, proposals, *, by, job)`**:
  - nadaje `prov` (rodzaj według ADR-0014, `seg_hash` z inwentarza, `inputs_hash`, `by` od wywołującego, `job`)
    i `status: accepted`;
  - kotwica, której nie da się potwierdzić (brak segmentu, cytat niedosłowny), odrzuca propozycję w każdym tierze.
    ADR-0014 przewiduje dla modelu obniżenie do `llm_inference`; ta ścieżka dochodzi w M10 razem z pętlą
    structured output. Dla Tier 0 obniżenie jest niemożliwe, bo `llm_inference` wymaga tieru `local` albo `premium`;
  - idempotencja: rekord równy istniejącemu z pominięciem `prov.job` i `prov.at` nie jest zapisywany;
  - to samo zadanie (producent z `prov.by.tool`/`prompt` bez wersji) zastępuje swój rekord; inny producent albo
    status inny niż `accepted` to konflikt, a nie nadpisanie;
  - przed zapisem waliduje całe `kb/` razem z inwentarzem (`wgc.validate.validate_documents`, nowa funkcja
    wydzielona z `validate`); każdy błąd blokuje zapis;
  - pisze `kb/logic/<rodzaj>.yaml` deterministycznie (DATA-CONTRACTS §10) jedną funkcją `wgc.kb._write_file`.
- **Planner** (`glu.planner`): etap i zakres (`all`, `chapter:N`, `segment:SEG-…`) → joby z kluczem cache
  `{task, task_version, output_schema, input_hash, context_hash}`; `context_hash` Tier 0 to hash pustej listy.
  Planner sprawdza tekst segmentów wejściowych (`text_hash`), zanim powstanie build, i niczego nie zapisuje.
  Zadania bez `deterministic_impl` pomija i wymienia.
- **Wykonawca Tier 0** (`glu.exec`):
  - job: `pending → ready → running → proposed → validating → accepted → done`; wyjątek implementacji to
    `running → failed`, odrzucenie przez `accept()` to `validating → failed`;
  - jeden Attempt na job (`tier: deterministic`, `outcome` `accepted`, `rejected` albo `error` z
    `error_class: runtime`, `schema_valid`, `domain_valid`, `validation_errors`), bez `output_blob` (bloby: M11);
  - bez RoutingDecision (router: M12);
  - build: `planning → running → done`, a przy jakimkolwiek nieudanym jobie `running → failed`; metryki
    `jobs_*` i `records_created|updated|unchanged`.
- **CLI:** `glu build --stage <etap> [--scope] [--dry-run] [--project] [--root]`. Projekt to nazwa katalogu `--root`,
  dopóki nie ma `project.yaml` (M7). Kod 2: błąd operacyjny (brak inwentarza lub tekstu, zły etap lub zakres, baza).
  Kod 1: build zakończony `failed`.
- **Zakres zadań:** M9a ma `wgc.tables.parse@0`. Harvest terminów to M9b. Relacje warstwy scenariusza przechodzą
  do M14.

## Konsekwencje
- GLU nie zna formatu `kb/` i nie zapisuje YAML-a KB. Test podmienia `wgc.kb._write_file` i sprawdza, że bez niego
  build nie zostawia `kb/`.
- Ponowny build bez zmian wejścia nie zmienia `kb/` (bez cache, bo cache to M11).
- Ścisła walidacja całego `kb/` przed zapisem ma koszt. Gdy zmiana źródła unieważni istniejący rekord (np. tabela
  przenumerowana z 4.3 na 4.4, a stary `TAB-4.3` ma nieaktualną kotwicę), każdy kolejny `accept()` się nie powiedzie,
  dopóki ktoś nie poprawi KB ręcznie. Nieaktualność ma być stanem (ADR-0004), więc rozdzielenie błędów blokujących od
  `stale` wymaga decyzji przy grafie zależności (M13).
- Rekord zakotwiczony w dokumencie o roli innej niż errata, FAQ albo wyjaśnienie autora dostaje `explicit_source`,
  także dla `community_interpretation` i `prior_translation`, które same nie są kanoniczne (LOGIC-MODEL). Gra
  benchmarkowa tego nie sprawdza. To kwestia do rozstrzygnięcia przed pierwszym takim źródłem.
- `TaskSpec` zmienia się w kodzie, a zmianę zapisuje się w ARCHITECTURE §2 i w ADR. Gdy pojawi się konsument spoza
  repo (np. MCP), może być potrzebny kontrakt JSON.

## Odrzucone warianty
- **`Protocol` albo klasa bazowa:** zadania to dane z funkcjami, dataclass daje niezmienność i `dataclasses.replace`
  w testach.
- **Rejestr przez entry pointy:** potrzebny dopiero przy zadaniach spoza pakietu `wgc`.
- **Własne `accept` w każdym TaskSpec:** wiele ścieżek zapisu do `kb/` i ryzyko rozjechania reguł provenance.
- **`prov.job` i `prov.at` w porównaniu:** każdy rebuild zmieniałby `kb/`.
- **Nadpisywanie rekordu innego producenta:** cichy konflikt między narzędziem, modelem i człowiekiem.
- **`validating → rejected` przy odrzuceniu Tier 0:** wybrano `failed`, bo kod deterministyczny nie ma kolejnej
  próby ani eskalacji w M9a; `rejected` zostaje dla pętli structured output (M10).
