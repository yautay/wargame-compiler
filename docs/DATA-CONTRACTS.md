# Kontrakty danych

## 1. Rejestr kontraktów
| Kontrakt | Plik | Zawartość | Stan |
|---|---|---|---|
| `wgc/common` | `contracts/schemas/common.schema.json` | ID, hash, glosa, kotwica, wykonawca, provenance, ryzyko, cykl życia, `HD-`, `RR-` | @0 szkic |
| `wgc/source@0` | `source.schema.json` | Stage 0: `source_document` (role, `seg_prefix`, pierwszeństwo), `segment`; inwentarz `source/inventory.yaml` ([§9](#stage0)) | @0 szkic |
| `wgc/logic@0` | `logic.schema.json` | Stage 1: Rule IR i rekordy pokrewne, gramatyka wyrażeń i efektów | @0 szkic |
| `wgc/digital@0` | `digital.schema.json` | Stage 1.5 | @0 szkic |
| `wgc/gate@0` | `gate.schema.json` | raport bramki (obliczany) | @0 szkic |
| `glu/exec@0` | `glu.schema.json` | Build, Job, Attempt, RoutingDecision, ReviewPackage, CacheKey; polityka fallbacku, `premium_reason`, stan `waiting_inference`, pola węzła w Attempt | @0 szkic |
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
| `CON-` | pojęcie | 1 | `snake_case`; scenariusz `scn.<nazwa>` |
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
  obcięte końce.
- **Projekcja semantyczna (`projection(record, consumer)`):** dla każdej pary (rodzaj rekordu, konsument) WGC definiuje
  listę pól wchodzących do hasha. Projekcja zawiera zawsze `kind` i `id` oraz te pola z listy, które rekord ma.
  `statement`, `notes`, `risk`, `status` i `prov` nigdy do niej nie wchodzą. Listy są danymi (`PROJECTIONS`),
  wersja `wgc/projection@0`, zmieniana razem z kontraktem. Konsumenci: `logic` (joby Stage 1 czytające rekord jako
  wejście lub kontekst), `digital` (Stage 1.5), `publication` (przekład segmentu, Stage 3).

  | Rodzaj | `logic` | `digital` | `publication` |
  |---|---|---|---|
  | `segment` | `doc`, `label`, `segment_type`, `text_hash` | — | `segment_type`, `text_hash` |
  | `rule` | `label`, `section`, `layer`, `applies_in`, `nature`, `modality`, `bind`, `actor`, `action`, `target`, `timing`, `conditions`, `effects`, `limits`, `triggers`, `formalization`, `ambiguities` | `nature`, `modality`, `bind`, `actor`, `action`, `target`, `timing`, `conditions`, `effects`, `limits`, `triggers`, `layer`, `applies_in`, `formalization` | `nature`, `modality`, `bind`, `actor`, `action`, `target`, `timing`, `conditions`, `effects`, `limits`, `triggers` |
  | `concept` | `category`, `name`, `source_terms`, `definition`, `of`, `params`, `parent`, `value_type`, `range`, `values`, `defined_by` | `category`, `name`, `of`, `params`, `value_type`, `range`, `values`, `parent` | `category`, `name`, `source_terms`, `definition` |
  | `relation` | `type`, `from`, `to`, `when`, `priority_basis` | `type`, `from`, `to`, `when`, `priority_basis` | `type`, `from`, `to` |
- `prov.inputs_hash` = hash projekcji wejść (kotwic i `derived_from`) w chwili akceptacji.

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
Markdown), ADR-0021 (PDF).

**Pliki w repo gry:**
- `source/inventory.yaml`: jeden dokument `wgc/source@0`, commitowany, bez tekstu;
- `.glu/source/<SRC-id>/<SEG-id>.txt`: tekst segmentów, gitignored (ADR-0012). `text_hash` liczy się z tego tekstu
  przez `wgc.canonical.text_hash`, a `file_hash` to `wgc.canonical.sha256_hex` surowych bajtów pliku.

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
  - w segmencie: `doc`, `label`, `segment_type`, `parent`, `order`, `pages`, `bbox`, `text_hash`, `visual_flags`;
- pola ręczne zostają (`title`, `edition`, `language`, `complete`, `precedence`, `edition_skew`, `seg_prefix`, `notes`,
  `corrections`, `verified_by_render`). `verified_by_render` znika, gdy zmienia się `text_hash` segmentu;
- komentarze nie są zachowywane.

**ID segmentu:**
- postać `SEG-<seg_prefix>.<klucz>`;
- `seg_prefix` domyślnie jest kluczem ID `SRC-`;
- klucz to etykieta jak wydrukowana albo `u<n>` dla n-tego segmentu bez numeru;
- `order` to pozycja w dokumencie liczona od 1, a `parent` to najbliższy wcześniejszy nagłówek.

**Segmentacja Markdown (`wgc.ingest.markdown@0`):**
- nagłówek ATX → `heading` (liczba na początku → etykieta);
- `**N.N**` na początku wiersza → segment do następnego znacznika lub nagłówka: `table`, gdy zawiera tabelę Markdown,
  inaczej `rule`;
- inna treść poza numerowanym segmentem → `other`;
- tekst bez etykiety i bez markupu inline, cytatów, punktorów, pionowych kresek i separatora tabel; numery list zostają;
- blok kodu nie otwiera segmentu.

**Segmentacja PDF (`wgc.ingest.pdf@0`, ADR-0021):** te same zasady co Markdown, rozpoznawane z układu strony.
- **Wiersze i tekst:**
  - znaki składa się w wiersze według dolnej krawędzi i czyta od góry do dołu (jedna kolumna);
  - spacja to znak spacji albo przerwa > 0,2 rozmiaru fontu;
  - przerwa > 2 rozmiary fontu dzieli wiersz na komórki, a komórki łączy się w tekście spacją.
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
  - komórka tabeli zawinięta w kilka wierszy daje inny tekst niż w Markdown.

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
| `extractor_changed` | warning | inwentarz zapisał inny ekstraktor niż bieżący dla tego formatu |
| `extract_error` | error | ponowna ekstrakcja się nie udała (np. powtórzona etykieta) |
| `segment_hash_mismatch` | error | tekst segmentu po ponownej ekstrakcji ma inny `text_hash` niż w inwentarzu |
| `segment_missing` | error | segmentu z inwentarza nie ma już w dokumencie |
| `segment_unlisted` | error | dokument ma segment nieobecny w inwentarzu |
| `cache_missing` | warning | brak tekstu segmentów w `.glu/source/` (odtwarza go `extract`) |
| `cache_mismatch` | error | tekst w `.glu/source/` nie zgadza się z `text_hash` |

Zmiana zawijania wierszy lub przeniesień daje tylko `file_hash_mismatch`, bo `text_hash` jest na nie niewrażliwy (§5).

**Gra benchmarkowa:** `bench/minigame/source/inventory.yaml` jest commitowany i odświeżany poleceniem
`python -m wgc source extract --root bench/minigame`. Fixture `contracts/fixtures/valid/source.minigame.yaml` jest jego
podzbiorem (te same projekcje `logic` i `order`), a `seg_hash` kotwic w `logic.minigame.yaml` to prawdziwe `text_hash`.
Pilnuje tego `tests/test_source.py`. Inwentarza i fixture'ów nie waliduje się w jednym przebiegu, bo dałoby to
`duplicate_id`.
