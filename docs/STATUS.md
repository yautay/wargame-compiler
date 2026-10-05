# STATUS

- **Data aktualizacji:** 2026-10-05
- **Ostatni milestone:** M9a (TaskSpec, `accept()`, wykonawca Tier 0, `glu build`, parse tabel): done
- **Bieżący milestone:** M9b
- **Stan repo:** testy zielone (`python -m pytest`); gałąź `master`, remote `origin` = `git@github.com:yautay/wargame-compiler.git`

## Gdzie jesteśmy
Architektura, kontrakty `@0`, gra benchmarkowa i system ciągłości istnieją. Kod domenowy:
- **M1:**
  - rejestr kontraktów (`wgc/contracts.py`);
  - tożsamość (`wgc/ids.py`);
  - kanoniczny JSON, hashe i projekcje (`wgc/canonical.py`);
  - walidator L0/L1 z kontrolami provenance (`wgc/validate.py`) i CLI `python -m wgc validate`
    ([DATA-CONTRACTS §8](DATA-CONTRACTS.md#walidator)).
- **M2a:**
  - inwentarz źródeł i `python -m wgc source init|scan|extract|verify` (`wgc/source.py`);
  - ekstraktor Markdown `wgc.ingest.markdown@0` z rejestrem ekstraktorów (`wgc/ingest/`)
    ([DATA-CONTRACTS §9](DATA-CONTRACTS.md#stage0), ADR-0020);
  - commitowany inwentarz gry benchmarkowej `bench/minigame/source/inventory.yaml`;
  - fixture'y `contracts/fixtures/valid/` z prawdziwymi `text_hash`, `seg_hash` i `file_hash`, zgodne z inwentarzem
    (pilnuje tego test).
- **M2b:**
  - ekstraktor PDF `wgc.ingest.pdf@0` na bibliotekach o licencjach liberalnych (pdfplumber/pdfminer.six, pypdfium2,
    Pillow; Q-10 zamknięta przez ADR-0021);
  - pola `pages`, `bbox` i `visual_flags` (`changed_color`, `strikethrough`);
  - `python -m wgc source render` zapisuje strony PNG do `.glu/source/<SRC-id>/pages/`;
  - ten sam tekst w Markdown i PDF daje te same segmenty i `text_hash` (test na PDF-ie gry benchmarkowej
    wygenerowanym w teście).

- **M8 (pierwszy kod GLU):**
  - job store `glu.store` w `.glu/state.db` (SQLite z biblioteki standardowej): tabele build, job, attempt,
    routing_decision i dziennik `transition`; migracje schematu bazy przez `PRAGMA user_version`; walidacja każdego
    rekordu kontraktem `glu/exec@0` przed zapisem (ADR-0023);
  - maszyna stanów joba i buildu jako tabela `glu.states` (strażniki: premium fallback tylko przy
    `allow_premium_fallback`, eskalacja podnosi tier); dokładna tabela w [GLU §3](GLU.md#tabela-przejsc);
  - `glu status` i `glu export` (skrypt `glu` w `[project.scripts]`); eksport odtwarza fixture `glu.job.yaml`.
- **M9a (pierwszy kontrakt WGC → GLU, pierwsze rekordy KB z buildu):**
  - `TaskSpec` i rejestr zadań (`wgc/tasks.py`), zakresy `all|chapter:N|segment:SEG-…` (ADR-0025);
  - `wgc.kb.accept()` jako jedyny zapis do `kb/`: provenance nadawana przez WGC, walidacja całego `kb/` z inwentarzem
    w pamięci, idempotencja, konflikty producentów, układ `kb/logic/<rodzaj>.yaml`
    ([DATA-CONTRACTS §10](DATA-CONTRACTS.md#propozycje));
  - zadanie `wgc.tables.parse@0`; komórki tabel w cache tekstu rozdziela tabulator bez zmiany `text_hash` (ADR-0024);
  - planner (`glu/planner.py`), wykonawca Tier 0 (`glu/exec.py`) i `glu build --stage --scope --dry-run`;
    na `bench/minigame` build daje `TAB-4.3`.

Mapa dokumentów: [README.md](../README.md#dokumentacja).

**Inferencja (M-INF0):** „local” znaczy self-hosted. Modele działają na **osobnym PC w LAN** (Windows 11 Pro,
RTX 3090 24 GB, 128 GB RAM) za Inference Gateway `igw`, a nie na maszynie z Claude Desktop. Węzeł jest wymienialnym
workerem bez wiedzy domenowej i nie jest źródłem prawdy. GLU łączy się z nim providerem `self_hosted` przez HTTPS
(`igw/api@0`). Niedostępny węzeł nie eskaluje do premium bez jawnej polityki. Decyzje: ADR-0015…0018. Projekt:
[inference/NODE.md](inference/NODE.md), wdrożenie: [inference/DEPLOYMENT.md](inference/DEPLOYMENT.md). Kolejność prac:
[ROADMAP](ROADMAP.md#kolejnosc).

| Etap / podsystem | Kontrakt | Kod | Benchmark |
|---|---|---|---|
| Tożsamość, hashe, walidator | `wgc/common` (ID, hash) | `wgc.ids`, `wgc.canonical`, `wgc.validate` (M1) | fixture'y `valid/` + `invalid/semantic/` |
| Stage 0 | `wgc/source@0` (szkic; role, `seg_prefix`) | `wgc.source`, `wgc.ingest.markdown` (M2a), `wgc.ingest.pdf` (M2b) | `bench/minigame/source/inventory.yaml` |
| Stage 1 | `wgc/logic@0` (szkic) | `wgc.tasks`, `wgc.kb.accept`, `wgc.tables` (M9a) | `phenomena.yaml`, gold w M3 |
| Stage 1.5 | `wgc/digital@0` (szkic) | — | gold w M17–M21 |
| Stage 2 | planowany (M24) | — | — |
| Stage 3 | planowany (M25–M26) | — | — |
| Bramki | `wgc/gate@0` (szkic) | — | — |
| GLU | `glu/exec@0` (szkic, z polityką fallbacku i `premium_reason`) | `glu.store`, `glu.states`, `glu status`, `glu export` (M8); `glu.planner`, `glu.exec`, `glu build` (M9a) | build Tier 0 na `bench/minigame` w testach |
| Węzeł inferencji (`igw`) | `igw/api@0` (szkic) | — (M-GW1) | — (M-INF) |

<a id="nastepny-milestone"></a>
## Następny milestone: M9b Harvest terminów (Tier 0)
**Dlaczego teraz:** M9a dał `TaskSpec`, `accept()`, planner i wykonawcę Tier 0 z jednym zadaniem (parse tabel).
Według [ROADMAP](ROADMAP.md#kolejnosc) tor domeny idzie dalej przez M9b → M10 do walking skeletonu M-E2E. M10 zależy
tylko od M9a, więc można go zacząć przed M9b, jeśli właściciel tak zdecyduje.

**Środowisko:** GLU natywnie na Windows (ADR-0022). Kontrakt zadań i zapis do `kb/`: ADR-0025, DATA-CONTRACTS §10.

**Tor równoległy:** M-GW1 (Inference Gateway) i M-BASE (HUM) bez zmian.

**Zakres (ROADMAP M9b)**
1. Zadanie `wgc.terms.harvest@0` w rejestrze `wgc.tasks`: pojęcia `concept` tylko dla wzorców o pewnej kategorii
   (np. `NdM` → `die`, `Scenario: X` → `scenario`, pozycje listy sekwencji `… Phase` → `phase`), z kotwicą i cytatem.
2. Pozostałe terminy nie trafiają do `kb/` (kategorię ustala M14).

**Kryteria akceptacji**
- Build Tier 0 na `bench/minigame` daje pojęcia przechodzące `wgc validate` i nie zgaduje kategorii.
- `python -m pytest` zielone; test ciągłości zielony.

**Poza zakresem:** relacje warstwy scenariusza (M14), providerzy i pętla structured output (M10), cache (M11), router
i bramki (M12).

## Otwarte kwestie
Zamknięte w M2b: Q-10 (biblioteka PDF, ADR-0021), Q-03 (GLU natywnie na Windows, ADR-0022). M8 nie otworzył nowych
kwestii (ustalenia właściciela w ADR-0023). M9a otworzył Q-12 i Q-13 (ADR-0025).

| # | Kwestia | Kto | Kiedy |
|---|---|---|---|
| Q-02 | Wybór gry pilotażowej (M28) i rozdziału do M-BASE | właściciel | przed M-BASE |
| Q-06 | Nazwa hosta węzła (`ai-node`?), sposób rozwiązywania (DNS routera, rezerwacja DHCP albo `hosts`) i adres dev machine do allowlisty | właściciel | przed M-NODE |
| Q-07 | Autostart węzła: Harmonogram zadań czy usługa (WinSW) | właściciel + M-NODE | M-NODE |
| Q-08 | Czy dopuszczamy `allow_premium_fallback: true` w jakimkolwiek buildzie (np. pilot z terminem) | właściciel | przed M12 |
| Q-04 | Czy glosy KB mają mieć drugi język (np. PL) jako widok Stage 3, czy wystarczy EN | właściciel | przed M7 (widoki) |
| Q-05 | Licencja repo narzędzia | właściciel | przed publikacją |
| Q-09 | Zakres `unresolved_ref` poza listą M1: referencje w wyrażeniach (`pred`, `is`, `val`, `count`), `ref_to`, `timing`, `emits`, `fires_on`, `legality`, `chain`, `ambiguities`, kroki testów; kontrola rodzaju celu (np. `interpretation.ambiguity` → `AMB-`). Fixture'y `valid/` już dziś je rozwiązują | M5 (L2) albo M7 | przed M5 |
| Q-11 | Ekstraktor PDF obsługuje jedną kolumnę: przed pierwszym PDF-em prawdziwej gry potrzebne są kolumny (wykrycie `column_scrambled` albo kolejność czytania), usuwanie nagłówków i stopek stron oraz decyzja o stronach bez warstwy tekstu (`image_only`, OCR). Zakres do ustalenia na PDF-ie gry pilotażowej (ADR-0021) | właściciel + IMPL | przed M28 |
| Q-12 | `accept()` waliduje całe `kb/` i każdy błąd blokuje zapis. Rekord unieważniony zmianą źródła (np. stara kotwica `TAB-4.3` po przenumerowaniu tabeli) blokuje każdy kolejny `accept()`, aż ktoś poprawi KB ręcznie. Trzeba rozdzielić błędy blokujące od stanu `stale` (ADR-0004, ADR-0025) | M13 (graf, invalidacja) | przed M13 |
| Q-13 | `accept()` daje `explicit_source` dla kotwic w każdej roli dokumentu poza errata/FAQ/wyjaśnieniem autora, także `community_interpretation` i `prior_translation`, które same nie są kanoniczne (LOGIC-MODEL). Rozstrzygnąć: odrzucenie, inny rodzaj provenance albo status inny niż `accepted` | właściciel + ARCH | przed pierwszym takim źródłem (najpóźniej M14) |

## Ryzyka
| Ryzyko | Wpływ | Łagodzenie |
|---|---|---|
| Modele self-hosted nie osiągną progów jakości Stage 1 | wysoki udział premium, koszt > 2× | M-INF przed M14; routing asymetryczny; zadania drobne; lokalny multi-pass (`local_deep`) |
| Węzeł w LAN niedostępny (wyłączony, uśpiony, awaria sieci) | buildy stoją w `waiting_inference` | autostart (M-NODE), `glu doctor` (M-E2E), cache L2 offline; **bez** automatycznego premium (ADR-0017) |
| Constrained decoding llama.cpp nie obsługuje `if/then/else` i pomija nieobsługiwane cechy schematu po cichu | wynik zgodny z gramatyką, ale nie ze schematem | `decoding_schema` płaski (pole `TaskSpec` od M9a, schemat zadań modelowych w M10), pełna walidacja w GLU/WGC (M10), test zgodności w M-INF |
| Prompty z tekstem chronionym przechodzą przez LAN | wyciek przy podsłuchu lub logowaniu | HTTPS z przypiętym certyfikatem, token, firewall z allowlistą, węzeł nie zapisuje promptów (NODE §7) |
| Aktualizacja runtime'u lub modelu na węźle zmienia fingerprint | masowe missy cache | wersje przypięte w `node.yaml`; aktualizacja jako świadoma decyzja |
| Gramatyka IR za uboga dla gier z gęstymi wyjątkami | dużo `{text}`, niskie `formalization` | `formalization` jako metryka; predykaty-pojęcia; przegląd na M3 i pilocie |
| Kalibracja ryzyka na grze benchmarkowej nie przeniesie się na prawdziwe gry | FN na pilocie | audyt premium (reguła 9), prywatny benchmark M-LEG |
| Koszt baseline nieznany | brak oceny celu 2× | M-BASE |
| `wgc/contracts.py` szuka schematów w `../contracts/` (poza pakietem): instalacja nieedytowalna ich nie zabierze | skrypty `wgc` (M1) i `glu` (M8, store waliduje rekordy przez `wgc.contracts`) nie działają po `pip install .` (działają po `pip install -e .`) | M7: przenieść schematy do `wgc/` jako package data lub dodać je do dystrybucji |
| Skrypt `glu` dopisany do `[project.scripts]` w M8; istniejąca instalacja edytowalna go nie ma | `glu` nie działa jako polecenie, dopóki nie przeinstalujesz pakietu (`python -m glu` działa) | `pip install -e .` po M8 |
| Job store ma jednego pisarza naraz (domyślny journal, `timeout` 5 s, bez WAL) | MCP (M22) równolegle z CLI może dostać `database is locked` | decyzja o WAL w M22 (ADR-0023) |
| Store waliduje każdy rekord schematem przy zapisie | wolniejsze buildy z tysiącami jobów | pomiar w M11 (w M9a nie mierzono: build gry benchmarkowej ma 1 job); w razie potrzeby walidacja tylko przy eksporcie (ADR-0023) |
| Narzędzie czytające pliki KB przez `contracts.load` pominie dokumenty po `---` (ADR-0019) | ciche pominięcie rekordów | czytać przez `wgc.validate.load_documents` |
| `bench/minigame/source/inventory.yaml` i fixture'y `valid/` mają te same ID segmentów | `wgc validate bench/minigame/source contracts/fixtures/valid` w jednym przebiegu daje `duplicate_id` (a `wgc validate bench` dodatkowo `schema_error` dla `phenomena.yaml`, który nie jest dokumentem KB) | walidować osobno (DATA-CONTRACTS §9) |
| Klucze segmentów bez numeru (`u1`, `u2`…) zależą od pozycji | wstawienie wstępu przenumeruje je i unieważni kotwice do nich | nie kotwiczyć reguł do segmentów bez numeru (ADR-0020) |
| Nowa wersja `pdfminer.six` zmienia pozycje znaków albo dekodowanie | `segment_hash_mismatch` w `wgc source verify` bez zmiany pliku | minimalne wersje równe przetestowanym; dryf wykrywa `wgc source verify`; zmianę reguł ekstraktora wprowadza nowa wersja `wgc.ingest.pdf@N` (ADR-0021) |
| Cache tekstu `.glu/source/` zapisany przed ADR-0024 ma ten sam `text_hash`, ale komórki tabel rozdzielone spacją | `wgc source verify` tego nie wykrywa; `wgc.tables.parse` odrzuca tabelę (job `failed`) | ponowne `wgc source extract`; komunikat zadania to podpowiada (ADR-0024) |
| Fixture `logic.minigame.yaml` ma `TAB-crt` z `tool: wgc.tables.parse@0`, ale z ID i wartościami (`none`, `routed`), których deterministyczny parse nie daje (`TAB-4.3`, `No effect`) | mylący przykład dla kolejnych sesji | fixture to ilustracja kontraktu, nie gold; gold tabeli w M3 |
| `accept()` przy każdym jobie czyta i waliduje całe `kb/` | wolne buildy przy tysiącach rekordów | pomiar w M11/M14; w razie potrzeby walidacja przyrostowa (M13) |
| PDF gry nie pogrubia numerów reguł albo ma kilka kolumn | segmentacja PDF zlewa reguły albo daje fałszywe tabele | sprawdzić na PDF-ie gry pilotażowej (Q-11), render stron do porównania (`wgc source render`) |
