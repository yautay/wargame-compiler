# Kontrakty danych

## 1. Rejestr kontraktów
| Kontrakt | Plik | Zawartość | Stan |
|---|---|---|---|
| `wgc/common` | `contracts/schemas/common.schema.json` | ID, hash, glosa, kotwica, wykonawca, provenance (z manifestem wywołania `wgc/manifest@0`, ADR-0033), ryzyko, cykl życia, `HD-`, `RR-` | @0 szkic |
| `wgc/source@0` | `source.schema.json` | Stage 0: `source_document` (role, `seg_prefix`, pierwszeństwo), `segment`; inwentarz `source/inventory.yaml` ([§9](#stage0)) | @0 szkic |
| `wgc/logic@0` | `logic.schema.json` | Stage 1: Rule IR i rekordy pokrewne, gramatyka wyrażeń i efektów | @0 szkic |
| `wgc/digital@0` | `digital.schema.json` | Stage 1.5 | @0 szkic |
| `wgc/gate@0` | `gate.schema.json` | raport bramki (obliczany) | @0 szkic |
| `glu/exec@0` | `glu.schema.json` | Build, Job, Attempt, RoutingDecision, ReviewPackage, CacheKey; polityka fallbacku, `premium_reason`, stan `waiting_inference`, pola węzła i `kb_receipt` w Attempt | @0 szkic |
| `igw/api@0` | `inference.schema.json` | protokół Inference Gateway: `infer_request`/`infer_result`, `error`, `health`, `capabilities`, `models`, `metrics`, `embed_*`, `job_status` (zarezerwowany) | @0 szkic |
| `glu/profiles@0` | (M10) | `~/.config/glu/profiles.yaml`: endpointy, profile logiczne, `fallback` | planowany |
| `igw/node@0` | (M-GW1) | `node.yaml` węzła: nasłuch, auth, limity, runtime, modele, profile węzła, scheduler | planowany |
| `wgc/project@0` | (M7) | `project.yaml` repo gry | planowany |
| `wgc/editorial@0` | (M24) | Stage 2 | planowany |
| `wgc/publication@0` | (M25–M26) | glosariusz, przekłady segmentów | planowany |
| `wgc/state@0` | (M17) | kanoniczny snapshot stanu gry | planowany |
| `wgc/engine-kit@0` | (M20) | pakiet dla silnika + format wyników testów | planowany |

Fixture'y:
- `contracts/fixtures/valid/*`: przechodzą schemat i `wgc validate` bez diagnostyk; razem tworzą **zbiór zamknięty**
  (każda referencja sprawdzana przez walidator rozwiązuje się w obrębie katalogu);
- `contracts/fixtures/invalid/*`: odpadają na schemacie (L0);
- `contracts/fixtures/invalid/semantic/*`: przechodzą schemat, a `wgc validate` daje **dokładnie** jeden kod błędu,
  zapisany w linii `# EXPECT: <kod>` (co najmniej jeden plik na każdy kod L1 i provenance, [§8](#walidator)).

Testy: `tests/test_contracts.py` (schematy), `tests/test_validate.py` (walidator). Ładowanie: `wgc/contracts.py`
(rejestr `referencing`, bez sieci).

**Przestrzenie nazw:**
- `wgc/*` to domena;
- `glu/*` to stan wykonania i konfiguracja GLU;
- `igw/*` to protokół i konfiguracja węzła inferencji, **bez pojęć domenowych**.

`wgc/contracts.py` rejestruje `igw/api@0` wyłącznie jako loader schematów dla testów kontraktów. WGC nie zna
infrastruktury inferencji, a `igw` czyta ten sam plik schematu bez importu `wgc` (ADR-0016).

**Inwarianty `igw/api@0` i `glu/exec@0`:**
- request inferencji nie ma pól domenowych (`additionalProperties: false`, tylko nieprzezroczysty `client_ref`);
- wynik zawsze niesie `model_fingerprint`, który nie zawiera hosta;
- decyzja routingu wybierająca premium zawsze ma `premium_reason`;
- `kb/` (`prov.by`) nigdy nie zawiera hosta ani `node_id`, bo te pola żyją tylko w Attempt w `.glu/`.

**Stan wykonania `glu/exec@0` w praktyce (M8, ADR-0023):**
- Job store (`glu/store.py`, `.glu/state.db`) waliduje każdy rekord kontraktem przed zapisem.
- `glu export [--build ID] [--out plik]` wydaje jeden dokument `glu/exec@0` z rekordami `build`, `job`, `attempt`
  i `routing_decision`. `review_package` dojdzie w M12/M13.
- `job.attempts` jest wyliczane z zapisanych Attemptów.
- Test `tests/test_glu_store.py` odtwarza przez store fixture `contracts/fixtures/valid/glu.job.yaml` rekord w rekord.
- Job Tier 0 (M9a) ma `tier: deterministic`, a `cache_key` bez `prompt_version`, `profile` i `dependency_state`.
  `input_hash` i `context_hash` pochodzą z manifestu wywołania joba ([§10](#manifest), ADR-0033). Dla zadania, które
  nie czyta rekordów `kb/`, `context_hash` to hash pustej listy.
- Attempt `accepted` niesie `kb_receipt` (M-STAB2, ADR-0031): `generation` (hash generacji `kb/` po akceptacji) i
  `records` (ID → `content_hash` rekordu w `kb/`). Pole jest opcjonalne i addytywne w `@0`. Końcowe wpisy joba
  (Attempt i ostatnie przejścia) zapisuje jedna transakcja (`Store.finish_job`). `glu receipt <job>` porównuje ten
  receipt z bieżącym `kb/` tylko do odczytu ([§10](#diagnostyka-receiptu), ADR-0033).

## 2. Wersjonowanie i zgodność
- `@0` to szkic: może się zmieniać bez migracji, ale każda zmiana aktualizuje fixture'y i testy w tej samej sesji.
- **Zamrożenie `@1`** następuje, gdy kontrakt ma pierwszego konsumenta poza testami. Dla `logic` to M14
  (pierwszy pakiet zadań Stage 1), dla `digital` M21.
- Od `@1` obowiązuje polityka: pola opcjonalne można dodawać. Usunięcie, zmiana nazwy lub semantyki = `@2`
  + ADR + migracja `wgc migrate` + fixture'y obu wersji.
- Dokument nazywa swój kontrakt w polu `schema` na najwyższym poziomie. Pliki bez `schema` są błędem.

## 3. Koperta dokumentu
```yaml
schema: wgc/logic@0
records:
  - {kind: rule, id: R-3.4, ...}
```
Rekordy różnych rodzajów mogą być w jednym pliku. Plik YAML może zawierać **kilka dokumentów** oddzielonych `---`,
każdy z własnym polem `schema` (np. segment `wgc/source@0` i kotwiczący go rekord `wgc/logic@0`), ADR-0019.
Walidator traktuje rekordy domenowe ze wszystkich dokumentów i plików jako jeden zbiór. Układ plików w repo gry ([ARCHITECTURE.md](ARCHITECTURE.md#4-repozytoria))
służy czytelności, a nie semantyce.

<a id="identyfikatory"></a>
## 4. Identyfikatory
Gramatyka: `<PREFIKS>-<klucz>`, gdzie prefiks to 1–4 wielkie litery, a klucz `[A-Za-z0-9][A-Za-z0-9._:-]*`.
ID są **stabilne**: nigdy nie są przenumerowywane ani używane ponownie. Usunięty rekord dostaje `status: deprecated`.

| Prefiks | Rodzaj | Etap | Klucz |
|---|---|---|---|
| `SRC-` | dokument źródłowy | 0 | `<gra>.<rola>` |
| `SEG-` | segment | 0 | `<gra>.<etykieta>`; dla innych dokumentów `<gra>.<dok>:<etykieta>` |
| `SEC-` | sekcja (mapowanie sekcja ↔ reguły atomowe) | 1 | numer sekcji |
| `CON-` | pojęcie | 1 | `snake_case`; scenariusz `scn.<nazwa>`; spoza głównej instrukcji `<klucz SRC>:<klucz>` ([§10](#id-pojec)) |
| `R-` | reguła | 1 | `[<dok>:]<etykieta>[.<n>]`, gdzie `<dok>` pomija się dla głównej instrukcji (np. `R-3.4`, `R-3.4.2`, `R-SB:2.1`, `R-ERR:12`) |
| `REL-` | relacja | 1 | numer kolejny |
| `TAB-` | tabela | 1 | `snake_case` lub numer z instrukcji |
| `PROC-` | procedura | 1 | `snake_case` |
| `AMB-` | niejasność | 1 | numer kolejny |
| `INT-` | interpretacja | 1 | numer niejasności lub kolejny |
| `CASE-` | przypadek kontrolny | 1 | numer kolejny |
| `CHG-` | zmiana (errata, FAQ, wydanie) | 1 | numer kolejny |
| `HD-` | decyzja człowieka | wszystkie | numer kolejny |
| `RR-` | prośba o przegląd | wszystkie | numer kolejny |
| `ENT-`, `DRV-`, `ACT-`, `LEG-`, `EVT-`, `TRG-`, `SEQ-`, `DP-`, `RNG-`, `MOD-`, `HID-`, `INV-`, `PRI-`, `BLK-`, `TST-` | elementy Stage 1.5 | 1.5 | `snake_case` / kropki; `EVT-` = nazwa zdarzenia |
| `build_`, `job_`, `att_`, `rd_`, `pkg_` | stan wykonania GLU | — | ULID / losowy, poza KB |

Prefiks jednoznacznie określa rodzaj rekordu, więc walidator (M1) sprawdza zgodność `kind` ↔ prefiks
(`kind_prefix_mismatch`). Rejestr prefiks → rodzaje jest danymi w `wgc/ids.py` (`PREFIX_KINDS`). `SEC-` jest znanym
prefiksem bez własnego rodzaju rekordu. Węzły `sequence.nodes[].id` (`SEQ-`) są zdefiniowanymi ID: można je wskazywać
i podlegają kontroli duplikatów.
`DP-` (punkt decyzji gracza) i `HD-` (decyzja człowieka) są rozdzielone celowo.

## 5. Kanoniczna serializacja i hashe
Implementacja: `wgc/canonical.py`.
- **Kanoniczny JSON (`canonical_json`):** UTF-8 bez escapowania, NFC dla napisów **i kluczy**, klucze posortowane
  według punktów kodowych Unicode, separatory bez spacji. Liczba zmiennoprzecinkowa o wartości całkowitej jest
  zapisywana jako całkowita (`1.0` → `1`), pozostałe w najkrótszej postaci odtwarzającej wartość (`repr` Pythona),
  wartości logiczne bez zmian. Pola słownika o wartości `null` są opuszczane, ale `null` **w liście** zostaje (komórki
  tabel). `NaN`, `Infinity`, klucze niebędące napisami i typy spoza JSON (np. daty YAML bez cudzysłowu) są błędem.
- **`content_hash`:** `sha256:` + hex kanonicznego JSON-a.
- **Hash segmentu (`text_hash`):** sha256 znormalizowanego tekstu (`normalize_text`): NFC, CRLF → LF, usunięte miękkie
  łączniki (U+00AD) razem z następującym białym znakiem, przeniesienia (łącznik na końcu wiersza między dwoma
  niebiałymi znakami): między literą a małą literą łącznik i złamanie znikają (`move-⏎ment` → `movement`), w pozostałych
  przypadkach znika tylko złamanie (`First-⏎Player` → `First-Player`, `3-⏎step` → `3-step`), zwinięte białe znaki,
  obcięte końce. Nie zależy od zawijania wierszy ani od separatora komórek. Używają go kotwice (`seg_hash`), wykrywanie
  nieaktualnych kotwic i parytet Markdown ↔ PDF.
- **Hash struktury segmentu (`struct_hash`, ADR-0032):** `content_hash({format: "wgc/struct@0", lines: structure(tekst)})`.
  `structure` (`wgc.canonical`) to wiersze tekstu segmentu jako listy komórek:
  - NFC, CRLF i CR → LF;
  - podział na wiersze po LF, na komórki po tabulatorze (`CELL_SEP`);
  - w komórce zwinięte białe znaki;
  - pomijany jest pusty wiersz bez tabulatora (wiersz pustych komórek zostaje, bo to wiersz tabeli);
  - bez łączenia przeniesień.

  Te same słowa w innych wierszach albo komórkach dają ten sam `text_hash` i inny `struct_hash`. Parsery tekstu
  (`wgc.tables.parse`, `wgc.terms.harvest`) czytają tekst wyłącznie przez `structure`, więc równy `struct_hash` daje
  równy wynik. Zmiana definicji `structure` to nowa wersja `wgc/struct@N` i nowa wersja ekstraktorów.
- **Projekcja semantyczna (`projection(record, consumer)`):** dla każdej pary (rodzaj rekordu, konsument) WGC definiuje
  listę pól wchodzących do hasha. Projekcja zawiera zawsze `kind` i `id` oraz te pola z listy, które rekord ma.
  `notes`, `refs`, `risk`, `status` i `prov` nigdy do niej nie wchodzą. Glosa reguły (`statement`) wchodzi tylko jako
  pole warunkowe (niżej). Listy są danymi (`PROJECTIONS`, `CONDITIONAL`), wersja `wgc/projection@2` (`@1`:
  `struct_hash` w projekcji `logic` segmentu, ADR-0032; `@2`: treść nieformalizowana, definicje predykatów, rodzaje
  M10–M14 i E2E, bez zapasów, ADR-0034). Konsumenci: `logic` (joby Stage 1 czytające rekord jako wejście lub
  kontekst), `digital` (Stage 1.5), `publication` (przekład segmentu, Stage 3).

  | Rodzaj | `logic` | `digital` | `publication` |
  |---|---|---|---|
  | `segment` | `doc`, `label`, `segment_type`, `text_hash`, `struct_hash` | — | `segment_type`, `text_hash` |
  | `source_document` | `role`, `seg_prefix`, `precedence` | — | — |
  | `rule` | `label`, `section`, `layer`, `applies_in`, `nature`, `modality`, `bind`, `actor`, `action`, `target`, `timing`, `conditions`, `effects`, `limits`, `triggers`, `formalization`, `ambiguities` | `nature`, `modality`, `bind`, `actor`, `action`, `target`, `timing`, `conditions`, `effects`, `limits`, `triggers`, `layer`, `applies_in`, `formalization` | `nature`, `modality`, `bind`, `actor`, `action`, `target`, `timing`, `conditions`, `effects`, `limits`, `triggers` |
  | `concept` | `category`, `name`, `source_terms`, `definition`, `of`, `params`, `parent`, `value_type`, `range`, `values`, `defined_by` | `category`, `name`, `of`, `params`, `value_type`, `range`, `values`, `parent` | `category`, `name`, `source_terms`, `definition` |
  | `relation` | `type`, `from`, `to`, `when`, `priority_basis` | `type`, `from`, `to`, `when`, `priority_basis` | `type`, `from`, `to` |
  | `table` | `title`, `columns`, `rows`, `complete` | jak `logic` | `title`, `columns`, `rows` |
  | `procedure` | `title`, `category`, `repeat`, `steps` | jak `logic` | `title`, `steps` |
  | `ambiguity` | `scope`, `question`, `readings`, `recommendation`, `impact`, `resolved_by` | — | — |
  | `interpretation` | `ambiguity`, `reading`, `statement` (treść odczytu, nie glosa) | jak `logic` | — |
  | `case` | `polarity`, `question`, `expected`, `verdict`, `chain` | jak `logic` | — |
  | `change` | `change_kind`, `affects`, `summary`, `from_edition`, `to_edition` | — | — |
  | `legality` | — | `applies_to`, `check`, `predicate`, `reason_code`, `unless`, `realizes` | — |
  | `test` | — | `category`, `from_case`, `covers`, `given`, `when`, `then`, `realizes` | — |

  **Pola warunkowe** (`CONDITIONAL`):
  - reguła z `formalization` `none` albo `partial` (brak pola = `full`): `statement` i `unformalized` we wszystkich
    trzech konsumentach. Przy pełnym IR glosa nie wchodzi do projekcji;
  - pojęcie `category: predicate`: `definition` i `defined_by` także w `digital`.

  Rodzaj bez projekcji dla danego konsumenta to błąd z nazwą wersji projekcji (`ProjectionError`), nigdy zapas
  z całego rekordu. Każdy rodzaj `kb/logic` ma projekcję `logic` (pilnuje tego test). Znaczenie reguł definiujących
  predykat (przechodnio) dochodzi przez graf (M13), nie przez projekcję.
- **Hashe rekordu w `prov`** (ADR-0033):
  - `prov.inputs_hash` = hash **dowodów rekordu**: `content_hash({projection: <wersja>, records: [projekcje logic
    segmentów kotwic i rekordów derived_from]})`;
  - `prov.manifest` = manifest wywołania joba, czyli wszystko, co job przeczytał ([§10](#manifest)). Klucz joba
    (`input_hash`, `context_hash`) liczy się z tego samego manifestu.

  Projekcja `logic` segmentu ma `struct_hash`, więc klucz joba i oba hashe zmieniają się przy innych granicach
  komórek lub wierszy, a `seg_hash` kotwicy (`text_hash`) nie (ADR-0032).

## 6. Konwencje YAML
- UTF-8 bez BOM, LF (`.gitattributes`).
- **Nie używać kluczy `on`, `off`, `yes`, `no`, `y`, `n`:** YAML 1.1 (PyYAML) czyta je jako wartości logiczne
  (wykryte w Session 0). Stąd pola `event`, `fires_on`.
- Operatory porównania w cudzysłowie (`"<="`), bo `>` i `<` bywają mylące w flow style.
- Zmienne zaczynają się od `$` (`$unit`).
- Teksty źródła tylko jako krótkie cytaty w kotwicach (ADR-0012).

## 7. Pakiet dla silnika i wyniki zwrotne (M20)
`engine-kit.json`: `{format: wgc/engine-kit@0, game, ruleset_hash, generated, source_rev, records (Stage 1.5),
tables (Stage 1), tests, fixtures, trace}`. Wyniki: `engine-results.json`: `{format, ruleset_hash, engine, results:
[{test, passed, reason_code?, events?}]}`. Niezgodność `ruleset_hash` jest błędem.

<a id="walidator"></a>
## 8. Walidator i diagnostyki (M1)
`python -m wgc validate <ścieżki…> [--json]` (po instalacji: `wgc validate`), implementacja `wgc/validate.py`.
Katalog jest przeszukiwany rekurencyjnie (`*.yaml`, `*.yml`). Kod wyjścia 1, gdy jest choć jeden błąd.

**Diagnostyka:** `{code, severity: error|warning, subject, message, affected: [ID…], location}`. `subject` to ID
rekordu, a dla błędów na poziomie pliku ścieżka. `message` jest po polsku. `location` to plik (z `#n` dla n-tego
dokumentu pliku wielodokumentowego). Raport JSON: `{ok, files, records, errors, warnings, diagnostics}`.
To podstawa późniejszych `wgc diagnose` i `wgc explain` (M13).

**Zakres:** L0 dotyczy każdego dokumentu. L1 i provenance dotyczą tylko rekordów kontraktów domenowych
(`wgc/source`, `wgc/logic`, `wgc/digital`), bo dokumenty `wgc/gate`, `glu/exec` i `igw/api` mają ID spoza KB.

| Kod | Poziom | Znaczenie |
|---|---|---|
| `load_error` | L0 | plik nie istnieje, nie jest poprawnym YAML-em albo nie ma dokumentu |
| `schema_error` | L0 | `contracts.errors` (brak `schema`, nieznany kontrakt, niezgodność ze schematem) |
| `duplicate_id` | L1 | to samo ID zdefiniowane więcej niż raz (w całym zbiorze, także w węzłach `sequence`) |
| `kind_prefix_mismatch` | L1 | prefiks ID nie odpowiada `kind` (§4) |
| `unresolved_ref` | L1 | referencja wskazuje nieistniejący rekord |
| `anchor_hash_mismatch` | provenance | `anchors[].seg_hash` ≠ `text_hash` wskazanego segmentu (kotwica nieaktualna) |
| `kb_batch_pending` | L0 | w odpowiednim `kb/` (podany katalog, nadrzędny katalog `kb` przy walidacji `kb/logic` albo pojedynczego pliku, katalog `kb` poniżej podanego) leży `.wgc-batch/manifest.json`: przerwana partia zapisu, pliki mogą być częściowo stare (ADR-0031; naprawa: `wgc kb recover`) |
| `kb_read_unstable` | L0 | nie udało się przeczytać spójnej wersji `kb/` w 5 próbach (pojawił się plik blokady pierwszego pisarza, manifest partii albo zmiana plików spoza blokady) albo blokada pisarza była zajęta dłużej niż 60 s (ADR-0031) |
| `missing_decision` | provenance | `prov.kind: human_decision` albo zaakceptowana interpretacja bez `prov.decision` wskazującego istniejący rekord `HD-` |

**Pozycje referencji sprawdzane przez `unresolved_ref`** (tabela `REF_FIELDS`): `refs`, `prov.derived_from`,
`realizes` (także `entity.fields[].realizes`), `covers`, `applies_to`, `from_case`, `relation.from`/`to`,
`interpretation.ambiguity`, `blocker.cause`/`affects`, `segment.doc`, `segment.parent` oraz `anchors[].seg` (w `prov.anchors`
i `review_request.evidence`). Referencje w wyrażeniach, `ref_to`, `timing`, `emits`, `fires_on`, `legality`, `chain`,
`ambiguities` i krokach testów nie są jeszcze sprawdzane. Walidator nie sprawdza też rodzaju celu referencji (np. czy
`interpretation.ambiguity` wskazuje `AMB-`).

<a id="stage0"></a>
## 9. Stage 0: inwentarz źródeł i `wgc source` (M2a, M2b)
Implementacja: `wgc/source.py` (inwentarz, polecenia) i `wgc/ingest/` (ekstraktory). Decyzje: ADR-0020 (inwentarz,
Markdown), ADR-0021 (PDF), ADR-0032 (`struct_hash`, ekstraktory `@1`).

**Pliki w repo gry:**
- `source/inventory.yaml`: jeden dokument `wgc/source@0`, commitowany, bez tekstu;
- `.glu/source/<SRC-id>/<SEG-id>.txt`: tekst segmentów, gitignored (ADR-0012). `text_hash` i `struct_hash` liczą się
  z tego tekstu (`wgc.canonical.text_hash`, `wgc.canonical.struct_hash`, §5), a `file_hash` to
  `wgc.canonical.sha256_hex` surowych bajtów pliku.

**Bramka tekstu dla zadań:** `Workspace.text` (planner, parsery, cytaty kotwic) podaje tekst segmentu tylko wtedy, gdy
segment ma `struct_hash`, a tekst w `.glu/source/` zgadza się z `text_hash` i `struct_hash`. W przeciwnym razie
`KBError` z poleceniem `wgc source extract`, a `glu build` kończy się kodem 2 przed utworzeniem buildu.

**Regeneracja artefaktów sprzed ADR-0032:** ekstraktory `@0` nie zapisywały `struct_hash`, a cache tekstu sprzed
ADR-0024 nie ma tabulatorów między komórkami. Inwentarz z `wgc.ingest.markdown@0` albo `wgc.ingest.pdf@0` daje w
`verify` błąd `struct_hash_missing` i ostrzeżenie `extractor_changed`, a każde zadanie odmawia odczytu tekstu. Naprawą
jest `wgc source extract`: dopisuje `struct_hash`, przepisuje cache i ustawia ekstraktor `@1`. Samo dopisanie
`struct_hash` nie jest zmianą segmentu (`verified_by_render` zostaje). Pierwszy build po regeneracji zapisuje rekordy
z nowym `prov.inputs_hash` (wynik `zmienione`), bo projekcja segmentu ma nowe pole; kotwice nie stają się nieaktualne.

**Polecenia** (`python -m wgc source <podpolecenie> [--root <repo gry>]`, domyślnie katalog bieżący):

| Podpolecenie | Działanie |
|---|---|
| `init --game <kod> [--doc rola:ścieżka …]` | tworzy inwentarz z dokumentem `SRC-<kod>.<rola>` dla każdego `--doc` (ścieżka względem `--root`; powtórzona rola dostaje `.2`, `.3`…) i od razu robi `scan`. Pierwszy dokument `rules` dostaje `seg_prefix: <kod>`. Istniejący inwentarz jest błędem |
| `scan` | dla dokumentów z `path`: `present`, `file_hash`, `extractor` (z rejestru rozszerzeń) |
| `extract` | `scan`, potem segmentacja obecnych dokumentów: rekordy `SEG-` w inwentarzu i tekst w `.glu/source/` |
| `verify [--json]` | walidacja inwentarza (§8) i kontrole Stage 0 niżej; kod 1 przy błędach |
| `render (--doc SRC-… \| --segment SEG-…) [--pages 1,3-4] [--scale 2.0]` | renderuje strony PDF do `.glu/source/<SRC-id>/pages/p<NNN>.png` do ręcznej weryfikacji (`verified_by_render`). Domyślnie renderuje strony segmentu (`pages`) albo cały dokument. Skala 1.0 = 72 dpi |

Kod wyjścia 2 oznacza błąd operacyjny: brak inwentarza, istniejący inwentarz przy `init`, nieznana rola, ścieżka
poza projektem, błąd ekstrakcji w `extract`, nieznany dokument lub segment, dokument inny niż PDF albo zły zakres stron
w `render`.

**Zapis inwentarza:**
- deterministyczny: stała kolejność pól (schemat), jeden rekord w wierszu, dokumenty w kolejności wpisów, segmenty
  według dokumentu i `order`;
- pola generowane są nadpisywane:
  - w dokumencie: `present`, `file_hash`, `extractor`;
  - w segmencie: `doc`, `label`, `segment_type`, `parent`, `order`, `pages`, `bbox`, `text_hash`, `struct_hash`,
    `visual_flags`;
- pola ręczne zostają (`title`, `edition`, `language`, `complete`, `precedence`, `edition_skew`, `seg_prefix`, `notes`,
  `corrections`, `verified_by_render`). `verified_by_render` znika, gdy zmienia się `text_hash` albo `struct_hash`
  segmentu (render potwierdzał poprzednią ekstrakcję);
- komentarze nie są zachowywane.

**ID segmentu:**
- postać `SEG-<seg_prefix>.<klucz>`;
- `seg_prefix` domyślnie jest kluczem ID `SRC-`;
- klucz to etykieta jak wydrukowana albo `u<n>` dla n-tego segmentu bez numeru;
- `order` to pozycja w dokumencie liczona od 1, a `parent` to najbliższy wcześniejszy nagłówek.

**Segmentacja Markdown (`wgc.ingest.markdown@1`; `@1` od ADR-0032: segmentacja i tekst jak w `@0` po ADR-0024, plus
`struct_hash`):**
- nagłówek ATX → `heading` (liczba na początku → etykieta);
- `**N.N**` na początku wiersza → segment do następnego znacznika lub nagłówka: `table`, gdy zawiera tabelę Markdown,
  inaczej `rule`;
- inna treść poza numerowanym segmentem → `other`;
- tekst bez etykiety i bez markupu inline, cytatów, punktorów, pionowych kresek i separatora tabel; numery list zostają;
- komórki wiersza tabeli rozdziela tabulator (puste komórki zostają, więc kolumny się nie przesuwają); granice komórek
  i wierszy pokrywa `struct_hash` (ADR-0032);
- blok kodu nie otwiera segmentu.

**Segmentacja PDF (`wgc.ingest.pdf@1`, ADR-0021, `@1` od ADR-0032 jak w Markdown):** te same zasady co Markdown, rozpoznawane z układu strony.
- **Wiersze i tekst:**
  - znaki składa się w wiersze według dolnej krawędzi i czyta od góry do dołu (jedna kolumna);
  - spacja to znak spacji albo przerwa > 0,2 rozmiaru fontu;
  - przerwa > 2 rozmiary fontu dzieli wiersz na komórki; w segmencie `table` komórki łączy się w tekście
    tabulatorem, w pozostałych spacją (ten sam `text_hash`, `struct_hash` rozróżnia, ADR-0032).
- **Nagłówek:** wiersz z fontem > 1,1 × najczęstszy rozmiar w dokumencie. Kolejne wiersze tego rozmiaru bez numeru na
  początku łączą się w jeden nagłówek, a poziom to ranga rozmiaru.
- **Numer reguły:** pogrubione pierwsze słowo wiersza w postaci `N.N`. Otwiera segment do następnego numeru lub
  nagłówka. Numer w zwykłym kroju (odsyłacz) i pozycje list zostają w tekście.
- **Typ segmentu:** `table`, gdy co najmniej dwa wiersze segmentu mają kilka komórek, inaczej `rule`. Treść bez numeru
  to `other`.
- **Pola generowane dla PDF:**

  | Pole | Postać |
  |---|---|
  | `pages` | `"3"` albo `"3-4"`: pierwsza i ostatnia strona segmentu, numeracja od 1 |
  | `bbox` | `[x0, top, x1, bottom]` w punktach od lewego górnego rogu pierwszej strony segmentu (suma wierszy na tej stronie), zaokrąglone do 0,1 |
  | `visual_flags` | ze znaków tekstu, bez etykiety. `changed_color`: kolor wypełnienia znaku ≠ najczęstszy kolor znaków w dokumencie (Gray/RGB/CMYK sprowadzone do RGB); nagłówki tej flagi nie dostają. `strikethrough`: pozioma linia albo prostokąt ≤ 2 pt w środkowym pasie znaku (30–70% wysokości od góry; podkreślenie się nie liczy). Puste flagi nie są zapisywane |

- **Ograniczenia:**
  - jedna kolumna;
  - nagłówki i stopki stron wchodzą do tekstu;
  - strony bez warstwy tekstu nie dają segmentów (`image_only`, `column_scrambled` i OCR nie są obsługiwane);
  - komórka tabeli zawinięta w kilka wierszy daje inny tekst niż w Markdown;
  - zawijanie akapitów w PDF różni się od Markdown, więc `struct_hash` segmentów PDF i Markdown z tym samym tekstem
    zwykle się różni (`text_hash` jest równy).

**Domyślne pierwszeństwo według roli** (`wgc.source.DEFAULT_PRECEDENCE`, wyższe wygrywa przy jawnym konflikcie,
[LOGIC-MODEL](LOGIC-MODEL.md#pierwszenstwo-zrodel)):

| Rola | Domyślne `precedence` |
|---|---|
| `errata` | 60 |
| `living_rules` | 50 |
| `rules`, `scenario_book`, `charts`, `cards`, `counters`, `map`, `module` | 40 |
| `faq` | 30 |
| `designer_clarification` | 20 |
| `community_interpretation` | 10 |
| `prior_translation`, `other` | brak (wymagane jawne `precedence`) |

Jawne `precedence` w inwentarzu nadpisuje wartość domyślną (`wgc.source.effective_precedence`); domyślna nie jest
zapisywana. Politykę projektu (`project.yaml`) dodaje M7.

**Diagnostyki `verify`** (format jak w §8):

| Kod | Poziom | Znaczenie |
|---|---|---|
| `source_missing` | error | dokument `present: true` bez pliku |
| `file_hash_mismatch` | error | hash pliku ≠ `file_hash` w inwentarzu |
| `extractor_changed` | warning | inwentarz zapisał inny ekstraktor niż bieżący dla tego formatu (regeneracja: `extract`) |
| `extract_error` | error | ponowna ekstrakcja się nie udała (np. powtórzona etykieta) |
| `segment_hash_mismatch` | error | tekst segmentu po ponownej ekstrakcji ma inny `text_hash` niż w inwentarzu |
| `segment_struct_mismatch` | error | ten sam `text_hash`, ale inny `struct_hash` niż w inwentarzu (inne granice komórek lub wierszy) |
| `segment_missing` | error | segmentu z inwentarza nie ma już w dokumencie |
| `segment_unlisted` | error | dokument ma segment nieobecny w inwentarzu |
| `struct_hash_missing` | error | segmenty dokumentu bez `struct_hash` (inwentarz z ekstraktora `@0`, sprzed ADR-0032); jedna diagnostyka na dokument, segmenty w `affected` |
| `cache_missing` | warning | brak tekstu segmentów w `.glu/source/` (odtwarza go `extract`) |
| `cache_mismatch` | error | tekst w `.glu/source/` nie zgadza się z `text_hash` albo z `struct_hash` |

Zmiana zawijania wierszy daje `file_hash_mismatch` i `segment_struct_mismatch` (wiersze to struktura), ale nie
`segment_hash_mismatch`, bo `text_hash` jest na nią niewrażliwy (§5).

**Gra benchmarkowa:** `bench/minigame/source/inventory.yaml` jest commitowany i odświeżany poleceniem
`python -m wgc source extract --root bench/minigame`. Fixture `contracts/fixtures/valid/source.minigame.yaml` jest jego
podzbiorem (te same projekcje `logic`, z `struct_hash`, i `order`), a `seg_hash` kotwic w `logic.minigame.yaml` to prawdziwe `text_hash`.
Pilnuje tego `tests/test_source.py`. Inwentarza i fixture'ów nie waliduje się w jednym przebiegu, bo dałoby to
`duplicate_id`.

<a id="propozycje"></a>
## 10. Propozycje zadań, `accept()` i układ `kb/` (M9a, M9b, M-STAB2, M-STAB3b)
Implementacja: `wgc/tasks.py` (`TaskSpec`, rejestr, zakres), `wgc/kb.py` (`Workspace`, `accept`), ADR-0025.

**Propozycja** to wynik zadania, zanim WGC go przyjmie. Wykonawca (kod Tier 0, a od M10 model) zwraca listę:
```yaml
- record: {kind: table, id: TAB-4.3, title: Combat Results Table, columns: [...], rows: [...], complete: true}
  anchors: [{seg: SEG-dsk.4.3, quote: "Combat Results Table"}]   # quote i span opcjonalne
  derived_from: [R-7.1]                                          # opcjonalne; kotwice albo derived_from wymagane
```
- `record` to rekord bez pól `prov`, `status` i `risk` (nadaje je WGC, ADR-0014); rodzaj musi być `output_kind` zadania.
- Kotwica propozycji ma tylko `seg`, `quote` i `span`. `seg_hash` dopisuje WGC z inwentarza.
- Schematu `wgc/proposal@0` jeszcze nie ma: kształt sprawdza `accept()`. Schemat dla modelu (z `decoding_schema`)
  dochodzi w M10.

**`accept(root, spec, inputs, proposals, *, by, job, ws, lock_timeout, manifest)`** to jedyna droga zapisu do `kb/`.
Recovery (`wgc kb recover`, ADR-0031) nie jest nowym źródłem treści: tylko kończy albo wycofuje partię, którą zaczął
`accept()`, bajtami z dziennika zapisanego przez `accept()`. Kroki `accept()`:
1. typy i kształt propozycji, a potem każdy `record` sprawdzony schematem `wgc/logic@0` z pominięciem tylko braku
   pól nadawanych przez WGC (`prov`, `status`, `risk`). To czyste kontrole przed jakąkolwiek funkcją domenową:
   - wynik zadania jest listą;
   - `record.id` to ID (napis zgodny z gramatyką §4);
   - `anchors` to lista obiektów `{seg, quote?, span?}`, gdzie `seg` to ID, `quote` to napis, a `span` to
     `[początek, koniec]` z liczb całkowitych (bez wartości logicznych) i `0 ≤ początek ≤ koniec`;
   - `derived_from` to lista ID.

   Błąd daje diagnostykę w `issues` (`schema_valid: false`), nigdy `TypeError`, i nie zakłada blokady (M-STAB1);
2. blokada pisarza projektu (`.glu/kb.lock`, ADR-0026) i kontrola, że inwentarz na dysku jest tym, z którego
   `Workspace` liczył wynik (odcisk bajtów). Pod blokadą najpierw recovery przerwanej partii (`kb/.wgc-batch/`,
   ADR-0031), więc wynik nigdy nie jest scalany z częściową `kb/`. Kroki 3–8 wykonują się pod blokadą, na `kb/`
   czytanym na nowo z dysku (jedna migawka: każdy plik czytany raz, z tych bajtów dokumenty i generacja).
   Najpierw manifest wywołania jest sprawdzany względem tej migawki ([niżej](#manifest)): zadanie czytające `kb/`,
   którego kontekst zmienił się od wykonania, dostaje `KBContextStale`, zanim cokolwiek zostanie ocenione lub
   zapisane;
3. reguły domenowe zadania (`TaskSpec.validate`);
4. `prov`:
   - `kind`: `explicit_source`, gdy każda kotwica wskazuje segment z inwentarza, a cytat (jeśli jest) występuje
     dosłownie w znormalizowanym tekście segmentu; `errata`, `faq` albo `designer_clarification`, gdy kotwice
     wskazują dokument o tej roli; bez kotwic: `deterministic_derivation` (tier `deterministic`) albo
     `llm_inference` (tier `local`/`premium`);
   - kotwica, której nie da się potwierdzić, odrzuca propozycję w każdym tierze (ADR-0025, ADR-0027: bez
     automatycznego obniżenia do `llm_inference`). Dotyczy to też `span`, którego koniec wykracza poza znormalizowany
     tekst segmentu (M-STAB1);
   - **zdecydowane, do wdrożenia w M-STAB3c (ADR-0027):** kotwica w dokumencie o roli `community_interpretation`,
     `prior_translation` albo `other` odrzuca propozycję (jawna lista ról kanonicznych), a `llm_inference` bez kotwic
     wymaga deklaracji zadania. Do wdrożenia obowiązuje opis powyżej;
   - `by` podaje wywołujący (GLU: tier i `tool` albo `profile`/`prompt`), `job` to ID joba;
   - `inputs_hash` = hash dowodów rekordu: `content_hash({projection: <wersja>, records: [projekcje logic segmentów
     kotwic (z `text_hash` i `struct_hash`, ADR-0032) i rekordów derived_from]})`. `derived_from` rozwiązuje się
     w inwentarzu i w `kb/` odczytanym pod blokadą. Rodzaj bez projekcji odrzuca propozycję (ADR-0034);
   - `manifest` = manifest wywołania joba (ADR-0033). Dla harvest obejmuje wszystkie wejścia joba, a nie tylko
     segmenty kotwic pojęcia;
   - każdy dowód (segment kotwicy, rekord `derived_from`) musi należeć do odczytu joba (`inputs` albo `context`
     manifestu). Inaczej propozycja jest odrzucana („spoza manifestu wywołania”);
   - `status: accepted`;
5. każdy rekord z `prov` sprawdzony schematem `wgc/logic@0`;
6. scalenie z `kb/`:
   - rekord równy istniejącemu z pominięciem `prov.job` i `prov.at` zostaje bez zmian (idempotencja; `prov.job`
     wskazuje job, który pierwszy dał bieżącą treść);
   - rekord tego samego zadania (`prov.by.tool` albo `prov.by.prompt` bez wersji) o innej treści jest zastępowany;
   - rekord o tym samym ID od innego producenta albo ze statusem innym niż `accepted` to konflikt;
7. walidacja całego `kb/` razem z inwentarzem sprawdzonym w kroku 2 (`wgc.validate.validate_documents`);
8. zapis tylko wtedy, gdy nie ma żadnego błędu (M-STAB2, ADR-0031):
   - najpierw receipt `.glu/kb-receipts/<job>.json` (gdy podano `job`; także gdy nic się nie zmieniło):
     `generation` (hash par ścieżka pliku `kb/` → `sha256` bajtów po akceptacji) i `records` (ID każdego
     zaproponowanego rekordu → `content_hash` rekordu w `kb/` po akceptacji);
   - **jeden zmieniony plik:** atomowa podmiana: plik tymczasowy `.<nazwa>.<losowe>.wgc-tmp` w tym samym katalogu,
     `flush` i `fsync`, potem `os.replace` (`wgc.fsio`, ADR-0026);
   - **dwa pliki lub więcej:** partia z dziennikiem wycofania w `kb/.wgc-batch/` (`wgc.fsbatch`): kopie starej
     i nowej treści, manifest `prepared`, podmiany, znacznik `committed`, usunięcie katalogu. Awaria podmiany albo
     znacznika w żywym procesie zapisuje intencję `rolling_back` i od razu wycofuje partię.

   Pozostałości po przerwanym procesie usuwa recovery pod blokadą.

Wynik (`AcceptResult`): `records`, `created`, `updated`, `unchanged`, `files`, `schema_valid`, `domain_valid`,
`issues`, `receipt` (`{generation, records}` przyjętego wyniku, inaczej `null`). GLU przepisuje `schema_valid`,
`domain_valid` i `issues` do Attemptu, a `receipt` do `kb_receipt` Attemptu `accepted`.

**Rodzaje niepowodzenia** (M-STAB1, ADR-0026):

| Sytuacja | `accept()` | Attempt w GLU |
|---|---|---|
| Dane odrzucone (typy, schemat, domena, kotwice, konflikt, walidacja całego `kb/`) | `AcceptResult.issues`, nic nie zapisane | `outcome: rejected` |
| Awaria operacyjna: brak lub nieczytelny inwentarz, tekst albo plik `kb/` | `KBError` | `outcome: error`, `error_class: runtime` |
| Blokada zajęta dłużej niż `lock_timeout` (domyślnie `kb.LOCK_TIMEOUT` = 60 s) | `KBBusy` | jak wyżej, powód „kb/ zajęte przez innego pisarza” |
| Inwentarz zmienił się po odczycie przez `Workspace` | `KBStale`, nic nie zapisane | jak wyżej, powód „inwentarz zmienił się w trakcie joba” |
| Rekordy `kb/` z manifestu zadania czytającego `kb/` zmieniły się między wykonaniem a akceptacją (ADR-0033) | `KBContextStale` (podklasa `KBStale`) z listą zmienionych wpisów, nic nie zapisane, bez receiptu | jak wyżej, powód „kontekst kb/ zmienił się między wykonaniem a akceptacją” |
| Zadanie czytające `kb/` wywołane bez manifestu z wykonania | `KBError` | jak wyżej |
| Nieudany zapis pliku albo partii, wycofanie potwierdzone | `KBWriteError`: `kb/` bez zmian (plik: atomowa podmiana; partia: przywrócona i dziennik usunięty) | jak wyżej, powód „awaria zapisu kb/”; receipt usuwany |
| Nieudana partia, której wycofanie się nie dokończyło (z zapisaną intencją `rolling_back` albo bez niej) | `KBUnresolved`: wynik nierozstrzygnięty, `kb/.wgc-batch/` i receipt zostają | **bez Attemptu**: job zostaje w `validating`, build przerwany (kod 2); rozstrzyga `glu reconcile` albo start następnego buildu, z `kb/` po recovery |
| Przerwana partia, której recovery nie rozstrzyga (plik zmieniony poza partią, brak kopii) | `KBBatchConflict`, nic nie zmienione | jak wyżej, powód „przerwana partia kb/ wymaga decyzji” |
| Błąd programu (wyjątek w WGC albo w `validate` zadania) | wyjątek przechodzi dalej, blokada zwolniona | `outcome: error`, komunikat `błąd programu: …` |

W CLI `KBError` przed buildem (np. brak inwentarza) daje kod 2. W trakcie buildu każdy z tych przypadków poza
`KBUnresolved` kończy job `failed`, a build kodem 1. `KBUnresolved` przerywa build kodem 2, a job zostaje w
`validating` do reconcile.

<a id="manifest"></a>
**Manifest wywołania (`wgc/manifest@0`, M-STAB3b, ADR-0033).** Jedyna definicja tego, co job czyta:
`wgc.manifest.build(ws, spec, wejścia)`. Planner liczy z niej klucz joba, wykonawca liczy ją ponownie przed
implementacją, a `accept()` zapisuje ją w `prov.manifest` (w `kb/`, więc zależności rekordu przetrwają utratę
`.glu/`). Schemat: `common.schema.json#/$defs/manifest`.

```yaml
manifest:
  format: wgc/manifest@0
  task: wgc.terms.harvest@0                  # id@wersja
  projection: wgc/projection@2
  inputs: [{id: SEG-dsk.2.2, hash: …}, …]    # w kolejności wejść; własna projekcja zadania albo projekcja logic
  authority: [{id: SRC-dsk.rules, hash: …}]  # projekcja logic dokumentu (role, seg_prefix, precedence), po ID
  context: [{id: CON-d6, hash: …}]           # rekordy kb/ czytane jako kontekst, po ID; brak pola, gdy ich nie ma
```

- `authority` zawsze obejmuje dokumenty segmentów wejściowych (rola wybiera rodzaj provenance). Zadanie dopisuje inne
  przez `TaskSpec.authority_selector`; `wgc.terms.harvest` dopisuje każdy dokument `rules`, bo wybiera spośród nich
  główną instrukcję (ADR-0030, Q-17 bez zmian).
- `context` wypełnia `TaskSpec.context_selector`. Dziś żadne zadanie nie czyta kontekstu `kb/` (M10/M14).
- W manifeście nie ma niczego zmiennego (job, build, zakres, czas, generacja `kb/`).
- Klucz joba: `input_hash` = `content_hash` manifestu bez `context`, `context_hash` = `content_hash` listy `context`
  (hash pustej listy, gdy jej nie ma).
- `TaskSpec.semantic_projection(ws, id) → dict` zastępuje projekcję jednego wejścia (ARCHITECTURE §2).
- **Świeżość kontekstu.** Zadanie czyta `kb/`, gdy ma `context_selector` albo wejście, które nie jest segmentem.
  Wykonawca czyta wtedy migawkę `kb/` (`wgc.kb.snapshot`, pod blokadą pisarza bez tworzenia pliku), liczy z niej
  manifest, a implementacja czyta tę samą migawkę (`Workspace.pinned`). Manifest wykonania różny od planu kończy job
  błędem („wejścia joba zmieniły się od planu”) przed implementacją. `accept()` porównuje generację migawki
  z wykonania z generacją `kb/` pod blokadą: równa generacja to te same bajty; inna oznacza ponowne policzenie
  manifestu, a różnica daje `KBContextStale`. Zadanie bez kontekstu porównuje manifest bez generacji, więc zmiany
  innych plików `kb/` (równoległy build) go nie blokują. Generacja nigdy nie trafia do manifestu, `prov` ani klucza.
- **Odtworzenie zależności bez `.glu/`:** `wgc.manifest.check(ws, prov.manifest)` porównuje każdy wpis z bieżącym
  inwentarzem i `kb/` i zwraca listę zmian (pusta lista: zależności bez zmian). Walidator sprawdza `prov.manifest`
  tylko schematem: brakujący wpis nie blokuje `accept()` (Q-12). Oznaczanie rekordów `stale` to M13.

<a id="diagnostyka-receiptu"></a>
**Diagnostyka receiptu: `glu receipt <job> [--root] [--json]` (M-STAB3b, ADR-0033, decyzja właściciela
2026-10-06).** Porównuje receipt akceptacji joba z bieżącym `kb/` i **niczego nie zmienia**: baza `.glu/state.db`
otwierana tylko do odczytu (`mode=ro`, bez migracji), `kb/` pod blokadą pisarza tylko wtedy, gdy plik blokady
istnieje, bez recovery, reconcile, usuwania receiptów i blokady startu buildów. Receipt to `kb_receipt` Attemptu
`accepted`, a dla joba w `validating` receipt nierozstrzygniętej akceptacji z `.glu/kb-receipts/`.

| Status | Znaczenie | Kod |
|---|---|---|
| `match` | każdy rekord receiptu ma w `kb/` tę samą treść | 0 |
| `differs` | rekord ma inną treść albo go brak; raport podaje bieżące `prov.job` i czy to późniejszy job | 1 |
| `no_job` | joba nie ma w bazie | 1 |
| `no_receipt` | job bez receiptu (np. `failed`) | 1 |
| `pending_batch` | `kb/` ma przerwaną partię; porównanie po `wgc kb recover` | 1 |
| błąd operacyjny | brak bazy, baza w innej wersji schematu, nieczytelny `kb/`, blokada zajęta > 60 s | 2 |

Raport mówi też, czy generacja `kb/` jest równa generacji z receiptu (`kb/` bajt w bajt jak po akceptacji). Różnica
względem historycznego receiptu nie oznacza sama w sobie uszkodzenia: późniejszy poprawny `accept()` (inny job,
decyzja człowieka) też zmienia rekord. Rozbieżność bez późniejszej zmiany (np. utrata zmian `kb/` po awarii zasilania
na Windows, ADR-0031) naprawia ponowny build.

<a id="recovery"></a>
**Recovery partii (`wgc kb recover [--dry-run]`, ADR-0031).** Decyzja ze stanu manifestu i hashy plików
(`sha256:<hex>`; dzienniki `wgc-kb-batch@0` z podwójnym przedrostkiem `sha256:sha256:` są normalizowane przy
odczycie):

| Stan `kb/.wgc-batch/` | Wynik |
|---|---|
| brak | bez zmian (usuwane są tylko osierocone `*.wgc-tmp`) |
| bez manifestu (przerwane przygotowanie) | katalog usunięty, `kb/` w całości stara |
| `committed` albo `prepared` z nową treścią każdego pliku | dokończenie, `kb/` w całości nowa |
| `rolling_back` (intencja wycofania) albo `prepared` w pozostałych przypadkach | wycofanie z kopii (nowe pliki usuwane), `kb/` w całości stara |
| plik ani ze starą, ani z nową treścią, brak kopii, nieczytelny manifest | `KBBatchConflict`, nic nie zmienione |

Recovery jest idempotentne: przerwane recovery albo wycofanie dokańcza się, uruchamiając je ponownie. Na czystym
`kb/` niczego nie zmienia (nie tworzy nawet `.glu/kb.lock`). `--dry-run` tylko wypisuje plan (bez zapisu, także bez
`.glu/kb.lock`). `wgc validate` zgłasza `kb_batch_pending`, dopóki manifest leży w `kb/`.

**Spójny odczyt w `wgc validate` (ADR-0031):**
- na czas odczytu walidator trzyma blokadę pisarza `.glu/kb.lock` każdego odpowiedniego `kb/` (podany katalog,
  nadrzędny `kb`, katalogi `kb` poniżej), jeśli jej plik istnieje. Pliku blokady nie tworzy i niczego nie zapisuje;
- jeśli plik blokady pojawi się w trakcie odczytu (pierwszy zapis w repo bez `.glu/kb.lock`), odczyt jest powtarzany
  pod tą blokadą;
- dodatkowo sprawdza, że nie pojawił się manifest, zbiór plików jest ten sam, a bajty się nie zmieniły;
- przy niepowodzeniu ponawia odczyt, a po 5 próbach albo po 60 s zajętej blokady zgłasza `kb_read_unstable`.

Partie zmieniające `kb/` w trakcie walidacji, także nowa → stara → nowa z przywróceniem identycznych bajtów, nie dają
OK dla mieszanej wersji. Nie dotyczy to zmian spoza blokady (edytor, git), które przywracają identyczne bajty.

**Granice gwarancji (ADR-0026, ADR-0031):**
- przerwanie procesu w dowolnym punkcie akceptacji, wycofania albo recovery kończy się po (ponownym) recovery `kb/`
  w całości starą albo w całości nową;
- zatwierdzenie, potwierdzone wycofanie i wynik nierozstrzygnięty mają różne skutki w GLU (tabela wyżej); dowód
  (receipt, dziennik) nie jest usuwany przed rozstrzygnięciem;
- Windows nie robi `fsync` katalogu: podmiany plików i znacznika są atomowe, ale ich trwałość po odcięciu
  zasilania nie jest wymuszona. Spójność zależy wtedy od kolejności dziennika NTFS (nietestowane). Attempt
  `accepted` w SQLite może przetrwać utratę zmian `kb/`; rozbieżność pokazuje porównanie `kb_receipt` z `kb/`;
- spójność `kb/` z `.glu/state.db` przywraca `glu reconcile` ([GLU §3](GLU.md#reconcile)). Receipt dowodzi
  zgodności treści, nie autorstwa;
- `kb/.wgc-batch/` nie jest ignorowany w git (decyzja właściciela, Q-18): po awarii widać go w `git status`,
  a `git clean -fdX` go nie usunie;
- blokada jest doradcza: chroni przed innymi wywołaniami `accept()`, nie przed edytorem, `git checkout` ani
  czytelnikami bez blokady (planner, edytor). Ręczna zmiana pliku przerwanej partii daje `KBBatchConflict`.

**Układ `kb/`:**
- `kb/logic/<rodzaj w liczbie mnogiej>.yaml`: `tables.yaml`, `concepts.yaml`, `rules.yaml`, `relations.yaml`,
  `procedures.yaml`, `ambiguities.yaml`, `interpretations.yaml`, `cases.yaml`, `changes.yaml`;
- jeden dokument `wgc/logic@0` na plik, rekordy posortowane po ID (liczby w porządku naturalnym), pola w kolejności
  kontraktu, LF;
- rekord krótszy niż 120 znaków w zapisie flow ma jedną linię (`- {…}`, jak inwentarz); dłuższy ma po jednej linii
  na pole z wartością w zapisie flow;
- rekord, który już leży w innym pliku `kb/`, zostaje w tym pliku;
- pliki zapisuje w całości `wgc.kb` (pojedynczy plik: `_write_file`, partia: `wgc.fsbatch`), więc komentarze nie
  są zachowywane;
- `kb/.wgc-batch/` istnieje tylko w trakcie partii albo po jej przerwaniu; nazwy w nim nie kończą się na `.yaml`;
- blokada `.glu/kb.lock` leży poza `kb/`, bo `.glu/` jest ignorowane przez git. Pliku blokady się nie usuwa; blokadę
  zwalnia system przy końcu procesu, więc nie ma „wiszących” blokad po awarii.

**Zadania Tier 0 (M9a, M9b):**

| Zadanie | Wejście (jeden job) | Wynik |
|---|---|---|
| `wgc.tables.parse@0` | segment `table` | `TAB-<etykieta>` (dokument `rules`) albo `TAB-<seg_prefix>:<etykieta>`; tytuł z frazy „… Table”; kolumny z nagłówka; zakresy `{min, max}`, liczby, napisy jak w druku; `complete: false`, gdy kolumna klucza miesza zakresy z napisami |
| `wgc.terms.harvest@0` | wszystkie segmenty jednego dokumentu z dopasowaniem wzorca; job powstaje, gdy zakres zawiera choć jeden z nich | `concept` tylko w kategoriach `die`, `phase`, `scenario` (wzorce niżej); jedna propozycja na ID; `source_terms` w kolejności pierwszego wystąpienia; jedna kotwica `{seg, quote}` na termin, cytat dosłowny, bez `span`; rekordy w `kb/logic/concepts.yaml` |

Oba zadania czytają wiersze i komórki tekstu wyłącznie przez `wgc.canonical.structure`, czyli treść `struct_hash`
(§5, ADR-0032). Wersje zadań się nie zmieniły: dla tego samego tekstu wynik jest taki sam jak przed ADR-0032.

<a id="id-pojec"></a>
**Pojęcia z `wgc.terms.harvest@0` (M9b, ADR-0030).** Rekord powstaje tylko dla wzorca o pewnej kategorii. Każdy inny
termin nie trafia do `kb/`: kategorię ustala M14.

| Kategoria | Wzorzec | Klucz | `name` |
|---|---|---|---|
| `die` | `NdM` jako całe słowo z liczbą kostek (`1d6`, `2D6`; N ≥ 1, M ≥ 2) | `d<M>` (`1d6` i `2d6` → `d6`) | `d<M>` |
| `scenario` | segment `heading`, którego cały tekst to `Scenario: X` | `scn.<slug(X)>` | `X` |
| `phase` | wiersz listy numerowanej (`N.`/`N)`, co najmniej dwa w segmencie), którego cała pozycja to słowa z wielkiej litery zakończone `Phase` | `<slug(name)>` (końcówka `_phase`) | jak w druku |

**Reguła ID pojęć** (deterministyczna, bez kolizji między dokumentami):
- `slug(x)`: NFKD, tylko ASCII, małe litery, ciągi `[a-z0-9]` łączone `_`, bez usuwania słów (`The Ford` → `the_ford`).
  Klucz spoza gramatyki §4 (np. pusty) nie daje rekordu;
- **główna instrukcja** to dokument `rules` o najmniejszym ID `SRC-` (`SRC-<gra>.rules`; `wgc source init` nadaje
  kolejnym `.2`, `.3`), niezależnie od kolejności w inwentarzu. Jej pojęcia mają ID `CON-<klucz>`. Warunek: nazwy
  `SRC-` według `wgc source init`. Ręcznie dopisany dokument `rules` sortujący się przed `SRC-<gra>.rules` zmieniłby
  główną instrukcję i ID pojęć (Q-17 w STATUS);
- pojęcia **każdego innego dokumentu** mają ID `CON-<klucz SRC>:<klucz>`, np. `CON-dsk.scenario_book:scn.the_ford`,
  `CON-dsk.rules.2:d6`. Klucz `SRC-` jest unikalny w inwentarzu, więc dwa dokumenty nie proponują tego samego ID;
- postaci kluczy kategorii są rozłączne (`d<M>`, `…_phase`, `scn.…`);
- `validate` zadania uruchamia wzorce ponownie na wejściach joba: ID, kategoria i każdy cytat muszą pochodzić
  z dopasowania. Propozycja spoza wzorców jest odrzucana, nawet z cytatem dosłownym;
- rekord nie zależy od `--scope`: wejścia joba to cały dokument, więc `chapter:5` po `all` nie zmienia `kb/`;
- łączenie pojęć między dokumentami (`CON-d6` i `CON-dsk.scenario_book:d6`) należy do M14. `TAB-` zachowuje regułę
  z M9a.

**Zakres buildu (`--scope`):** `all`, `chapter:<N>` (segmenty pod nagłówkiem z etykietą `N` albo `N.0`, po polu
`parent`), `segment:<SEG-id>`; tylko obecne dokumenty.
