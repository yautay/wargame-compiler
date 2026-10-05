# STATUS

- **Data aktualizacji:** 2026-10-05
- **Ostatni milestone:** M1 (tożsamość, hashowanie i walidator referencji): done
- **Bieżący milestone:** M2
- **Stan repo:** testy zielone (`python -m pytest`); gałąź `master`, remote `origin` = `git@github.com:yautay/wargame-compiler.git`

## Gdzie jesteśmy
Architektura, kontrakty `@0`, gra benchmarkowa i system ciągłości istnieją. Kod domenowy (M1): rejestr kontraktów
(`wgc/contracts.py`), tożsamość (`wgc/ids.py`), kanoniczny JSON, hashe i projekcje (`wgc/canonical.py`), walidator L0/L1
z kontrolami provenance (`wgc/validate.py`) i CLI `python -m wgc validate` ([DATA-CONTRACTS §8](DATA-CONTRACTS.md#walidator)).
Fixture'y `contracts/fixtures/valid/` tworzą zbiór zamknięty (hashe segmentów to wciąż placeholdery do M2).
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
| Stage 0 | `wgc/source@0` (szkic) | — | rulebook gry benchmarkowej |
| Stage 1 | `wgc/logic@0` (szkic) | — | `phenomena.yaml`, gold w M3 |
| Stage 1.5 | `wgc/digital@0` (szkic) | — | gold w M17–M21 |
| Stage 2 | planowany (M24) | — | — |
| Stage 3 | planowany (M25–M26) | — | — |
| Bramki | `wgc/gate@0` (szkic) | — | — |
| GLU | `glu/exec@0` (szkic, z polityką fallbacku i `premium_reason`) | — | — |
| Węzeł inferencji (`igw`) | `igw/api@0` (szkic) | — (M-GW1) | — (M-INF) |

<a id="nastepny-milestone"></a>
## Następny milestone: M2 Stage 0: inwentarz i ingest źródeł
**Dlaczego teraz:** M1 dał `text_hash` i walidację kotwic (`anchor_hash_mismatch`). Fixture'y mają placeholderowe hashe
segmentów i plików. M2 liczy prawdziwe, co odblokowuje M8 (joby GLU na segmentach) i M3 (gold z prawdziwymi kotwicami).

**Tor równoległy:** M-GW1 (Inference Gateway) i M-BASE (HUM) bez zmian ([ROADMAP](ROADMAP.md#kolejnosc)).

**Przed pracą:** zakres z ROADMAP (Markdown + PDF + render + flagi wizualne + role źródeł) jest na granicy jednej sesji.
Rekomendacja: podzielić w ROADMAP na **M2a** (inwentarz, `wgc source init/scan/extract/verify`, ingest Markdown, prawdziwe
hashe w fixture'ach, role `living_rules` i `community_interpretation` z domyślnym pierwszeństwem) i **M2b** (ingest PDF
przez PyMuPDF, flagi wizualne, render strony). PyMuPDF to nowa zależność: dopisać do `requirements.txt`
i `pyproject.toml` w sesji, która go użyje.

**Zakres (ROADMAP M2)**
1. `wgc source init/scan/extract/verify` (podpolecenia w `wgc/__main__.py`), inwentarz `source/inventory.yaml`
   commitowany, tekst segmentów w `.glu/source/` (nigdy w repo, ADR-0012).
2. Ingest Markdown (`bench/minigame/rulebook.md`): segmentacja po numerach reguł, typy segmentów, `text_hash` przez
   `wgc.canonical.text_hash`, `file_hash` przez `wgc.canonical.sha256_hex`.
3. Ingest PDF (PyMuPDF): segmentacja, flagi wizualne (kolor zmian, przekreślenie), render strony do weryfikacji.
4. Kontrakt `source_document`: role `living_rules`, `community_interpretation` i domyślne pierwszeństwo według roli
   ([LOGIC-MODEL](LOGIC-MODEL.md#pierwszenstwo-zrodel)); zmiana kontraktu aktualizuje fixture'y, testy i DATA-CONTRACTS.
5. Przeliczenie fixture'ów: `text_hash` segmentów w `source.minigame.yaml` **i** `seg_hash` wszystkich kotwic
   w `logic.minigame.yaml` jednocześnie; `python -m wgc validate contracts/fixtures/valid` musi zostać na 0 błędów.

**Kryteria akceptacji**
- `python -m pytest` zielone; test ciągłości zielony.
- `bench/minigame` → inwentarz z prawdziwymi hashami, fixture'y przeliczone, `wgc validate` bez błędów.
- Deterministyczność: dwa przebiegi dają identyczne hashe.
- Test na PDF wygenerowanym w teście z tekstu własnego (bez sieci, bez plików wydawców).

**Poza zakresem:** Stage 1 (M3), cytaty dosłowne i sygnały źródło↔IR (M5), cokolwiek w `glu/`.

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
