# Kontrakty danych

## 1. Rejestr kontraktów
| Kontrakt | Plik | Zawartość | Stan |
|---|---|---|---|
| `wgc/common` | `contracts/schemas/common.schema.json` | ID, hash, glosa, kotwica, wykonawca, provenance, ryzyko, cykl życia, `HD-`, `RR-` | @0 szkic |
| `wgc/source@0` | `source.schema.json` | Stage 0: `source_document`, `segment` | @0 szkic |
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

Fixture'y: `contracts/fixtures/valid/*` (muszą przechodzić) i `contracts/fixtures/invalid/*` (muszą odpadać).
Test: `tests/test_contracts.py`. Ładowanie: `wgc/contracts.py` (rejestr `referencing`, bez sieci).

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
Rekordy różnych rodzajów mogą być w jednym pliku. Układ plików w repo gry ([ARCHITECTURE.md](ARCHITECTURE.md#4-repozytoria))
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

Prefiks jednoznacznie określa rodzaj rekordu, więc walidator (M1) sprawdza zgodność `kind` ↔ prefiks.
`DP-` (punkt decyzji gracza) i `HD-` (decyzja człowieka) są rozdzielone celowo.

## 5. Kanoniczna serializacja i hashe
- **Kanoniczny JSON:** UTF-8, NFC dla napisów, klucze posortowane, bez zbędnych spacji, liczby całkowite bez `.0`,
  bez pól o wartości `null` (opuszczane). `sha256:` + hex.
- **Hash segmentu (`text_hash`):** sha256 znormalizowanego tekstu (NFC, zwinięte białe znaki, złączone przeniesienia wyrazów).
- **Projekcja semantyczna:** dla każdej pary (rodzaj rekordu, konsument) WGC definiuje listę pól wchodzących do hasha
  (np. reguła dla Stage 1.5: `nature`, `modality`, `bind`, `actor`, `action`, `target`, `timing`, `conditions`,
  `effects`, `limits`, `triggers`, `layer`, `applies_in`, `formalization`. Bez `statement`, `notes`, `risk`).
  Projekcje są wersjonowane razem z kontraktem.
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
