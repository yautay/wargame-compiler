# STATUS

- **Data aktualizacji:** 2026-10-05
- **Ostatni milestone:** M2a (Stage 0: inwentarz, polecenia `wgc source`, ingest Markdown): done
- **Bieżący milestone:** M2b
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

GLU to pusty pakiet. Mapa dokumentów: [README.md](../README.md#dokumentacja).

**Inferencja (M-INF0):** „local” znaczy self-hosted. Modele działają na **osobnym PC w LAN** (Windows 11 Pro,
RTX 3090 24 GB, 128 GB RAM) za Inference Gateway `igw`, a nie na maszynie z Claude Desktop. Węzeł jest wymienialnym
workerem bez wiedzy domenowej i nie jest źródłem prawdy. GLU łączy się z nim providerem `self_hosted` przez HTTPS
(`igw/api@0`). Niedostępny węzeł nie eskaluje do premium bez jawnej polityki. Decyzje: ADR-0015…0018. Projekt:
[inference/NODE.md](inference/NODE.md), wdrożenie: [inference/DEPLOYMENT.md](inference/DEPLOYMENT.md). Kolejność prac:
[ROADMAP](ROADMAP.md#kolejnosc).

| Etap / podsystem | Kontrakt | Kod | Benchmark |
|---|---|---|---|
| Tożsamość, hashe, walidator | `wgc/common` (ID, hash) | `wgc.ids`, `wgc.canonical`, `wgc.validate` (M1) | fixture'y `valid/` + `invalid/semantic/` |
| Stage 0 | `wgc/source@0` (szkic; role, `seg_prefix`) | `wgc.source`, `wgc.ingest.markdown` (M2a); PDF: M2b | `bench/minigame/source/inventory.yaml` |
| Stage 1 | `wgc/logic@0` (szkic) | — | `phenomena.yaml`, gold w M3 |
| Stage 1.5 | `wgc/digital@0` (szkic) | — | gold w M17–M21 |
| Stage 2 | planowany (M24) | — | — |
| Stage 3 | planowany (M25–M26) | — | — |
| Bramki | `wgc/gate@0` (szkic) | — | — |
| GLU | `glu/exec@0` (szkic, z polityką fallbacku i `premium_reason`) | — | — |
| Węzeł inferencji (`igw`) | `igw/api@0` (szkic) | — (M-GW1) | — (M-INF) |

<a id="nastepny-milestone"></a>
## Następny milestone: M2b Stage 0: ingest PDF, flagi wizualne, render strony
**Dlaczego teraz:** M2a dał inwentarz, polecenia `wgc source` i rejestr ekstraktorów. Prawdziwe gry mają PDF-y, więc bez
M2b Stage 0 działa tylko na grze benchmarkowej. M2b domyka pierwotne M2.

**Kolejność do decyzji:** według [ROADMAP](ROADMAP.md#kolejnosc) M2b może iść w dowolnym momencie po M2a, najpóźniej
przed M28. Właściciel może zamiast niego wybrać M8 (tor domeny i GLU): wtedy M8 dostaje `next`, a M2b `planned`.
**Najpierw** trzeba rozstrzygnąć Q-10 (biblioteka PDF a licencja).

**Tor równoległy:** M-GW1 (Inference Gateway) i M-BASE (HUM) bez zmian.

**Zakres (ROADMAP M2b)**
1. Ekstraktor PDF w `wgc/ingest/pdf.py`:
   - czysta funkcja: bajty na wejściu, `Segment` na wyjściu;
   - podpięty pod rejestr `wgc.ingest.extractor_for` (`.pdf`);
   - segmentacja po numerach reguł (te same zasady co Markdown, ADR-0020);
   - `pages` i `bbox` w segmencie (pola generowane już obsługuje `wgc.source`).
2. Flagi wizualne `visual_flags`: `changed_color` (kolor tekstu inny niż podstawowy), `strikethrough` (linia przez
   tekst); ewentualnie `image_only` dla stron bez warstwy tekstu.
3. Render strony do `.glu/source/` (PNG) do ręcznej weryfikacji; `verified_by_render` pozostaje polem ręcznym.
4. Nowa zależność w `requirements.txt` i `pyproject.toml`.
5. DATA-CONTRACTS §9 (ekstraktor PDF), ewentualny ADR (wybór biblioteki).

**Kryteria akceptacji**
- `python -m pytest` zielone; test ciągłości zielony.
- Test na PDF wygenerowanym **w teście** z tekstu własnego (bez sieci, bez plików wydawców).
- Ten sam tekst w Markdown i PDF daje te same `text_hash` segmentów typu `rule`.
- Flagi wizualne wykryte na przygotowanych w teście stronach (kolor, przekreślenie).

**Poza zakresem:** OCR, kolumny pomieszane (`column_scrambled`) poza wykryciem, Stage 1 (M3), cokolwiek w `glu/`.

## Otwarte kwestie
| # | Kwestia | Kto | Kiedy |
|---|---|---|---|
| Q-02 | Wybór gry pilotażowej (M28) i rozdziału do M-BASE | właściciel | przed M-BASE |
| Q-03 | Czy GLU na dev machine działa natywnie na Windows, czy w WSL2 (od tego zależy, czy repo gier trzymać w systemie plików WSL). Węzła to nie dotyczy (ADR-0015) | właściciel | przed M8 |
| Q-06 | Nazwa hosta węzła (`ai-node`?), sposób rozwiązywania (DNS routera, rezerwacja DHCP albo `hosts`) i adres dev machine do allowlisty | właściciel | przed M-NODE |
| Q-07 | Autostart węzła: Harmonogram zadań czy usługa (WinSW) | właściciel + M-NODE | M-NODE |
| Q-08 | Czy dopuszczamy `allow_premium_fallback: true` w jakimkolwiek buildzie (np. pilot z terminem) | właściciel | przed M12 |
| Q-04 | Czy glosy KB mają mieć drugi język (np. PL) jako widok Stage 3, czy wystarczy EN | właściciel | przed M7 (widoki) |
| Q-05 | Licencja repo narzędzia | właściciel | przed publikacją |
| Q-09 | Zakres `unresolved_ref` poza listą M1: referencje w wyrażeniach (`pred`, `is`, `val`, `count`), `ref_to`, `timing`, `emits`, `fires_on`, `legality`, `chain`, `ambiguities`, kroki testów; kontrola rodzaju celu (np. `interpretation.ambiguity` → `AMB-`). Fixture'y `valid/` już dziś je rozwiązują | M5 (L2) albo M7 | przed M5 |
| Q-10 | Biblioteka PDF dla M2b: PyMuPDF jest na licencji AGPL-3.0 (albo komercyjnej), co wiąże się z Q-05. Alternatywy na licencjach liberalnych: `pdfplumber`/`pdfminer.six` (MIT; znaki z kolorem, linie), `pypdfium2` (Apache/BSD; render); PDF do testów z `reportlab` (BSD) albo z samej biblioteki | właściciel | przed M2b |

## Ryzyka
| Ryzyko | Wpływ | Łagodzenie |
|---|---|---|
| Modele self-hosted nie osiągną progów jakości Stage 1 | wysoki udział premium, koszt > 2× | M-INF przed M14; routing asymetryczny; zadania drobne; lokalny multi-pass (`local_deep`) |
| Węzeł w LAN niedostępny (wyłączony, uśpiony, awaria sieci) | buildy stoją w `waiting_inference` | autostart (M-NODE), `glu doctor` (M-E2E), cache L2 offline; **bez** automatycznego premium (ADR-0017) |
| Constrained decoding llama.cpp nie obsługuje `if/then/else` i pomija nieobsługiwane cechy schematu po cichu | wynik zgodny z gramatyką, ale nie ze schematem | `decoding_schema` płaski (M9), pełna walidacja w GLU/WGC (M10), test zgodności w M-INF |
| Prompty z tekstem chronionym przechodzą przez LAN | wyciek przy podsłuchu lub logowaniu | HTTPS z przypiętym certyfikatem, token, firewall z allowlistą, węzeł nie zapisuje promptów (NODE §7) |
| Aktualizacja runtime'u lub modelu na węźle zmienia fingerprint | masowe missy cache | wersje przypięte w `node.yaml`; aktualizacja jako świadoma decyzja |
| Gramatyka IR za uboga dla gier z gęstymi wyjątkami | dużo `{text}`, niskie `formalization` | `formalization` jako metryka; predykaty-pojęcia; przegląd na M3 i pilocie |
| Kalibracja ryzyka na grze benchmarkowej nie przeniesie się na prawdziwe gry | FN na pilocie | audyt premium (reguła 9), prywatny benchmark M-LEG |
| Koszt baseline nieznany | brak oceny celu 2× | M-BASE |
| `wgc/contracts.py` szuka schematów w `../contracts/` (poza pakietem): instalacja nieedytowalna ich nie zabierze | skrypt `wgc` (M1) nie działa po `pip install .` (działa po `pip install -e .`) | M7: przenieść schematy do `wgc/` jako package data lub dodać je do dystrybucji |
| ADR-0002 obiecuje CLI `glu`, `pyproject` ma tylko `wgc` w `[project.scripts]` | brak polecenia `glu` po instalacji | M8 |
| Narzędzie czytające pliki KB przez `contracts.load` pominie dokumenty po `---` (ADR-0019) | ciche pominięcie rekordów | czytać przez `wgc.validate.load_documents` |
| `bench/minigame/source/inventory.yaml` i fixture'y `valid/` mają te same ID segmentów | `wgc validate bench/minigame/source contracts/fixtures/valid` w jednym przebiegu daje `duplicate_id` (a `wgc validate bench` dodatkowo `schema_error` dla `phenomena.yaml`, który nie jest dokumentem KB) | walidować osobno (DATA-CONTRACTS §9) |
| Klucze segmentów bez numeru (`u1`, `u2`…) zależą od pozycji | wstawienie wstępu przenumeruje je i unieważni kotwice do nich | nie kotwiczyć reguł do segmentów bez numeru (ADR-0020) |
