# STATUS

- **Data aktualizacji:** 2026-10-05
- **Ostatni milestone:** M-INF0a (przegląd spójności po M-INF0; poprzednio M-INF0: self-hosted inference w LAN): done
- **Bieżący milestone:** M1
- **Stan repo:** testy zielone (`python -m pytest`); gałąź `master`, remote `origin` = `git@github.com:yautay/wargame-compiler.git`

## Gdzie jesteśmy
Architektura, kontrakty `@0`, gra benchmarkowa i system ciągłości istnieją. Nie ma jeszcze kodu domenowego poza
rejestrem kontraktów (`wgc/contracts.py`). GLU to pusty pakiet. Mapa dokumentów: [README.md](../README.md#dokumentacja).

**Inferencja (M-INF0):** „local” znaczy self-hosted. Modele działają na **osobnym PC w LAN** (Windows 11 Pro,
RTX 3090 24 GB, 128 GB RAM) za Inference Gateway `igw`, a nie na maszynie z Claude Desktop. Węzeł jest wymienialnym
workerem bez wiedzy domenowej i nie jest źródłem prawdy. GLU łączy się z nim providerem `self_hosted` przez HTTPS
(`igw/api@0`). Niedostępny węzeł nie eskaluje do premium bez jawnej polityki. Decyzje: ADR-0015…0018. Projekt:
[inference/NODE.md](inference/NODE.md), wdrożenie: [inference/DEPLOYMENT.md](inference/DEPLOYMENT.md). Kolejność prac:
[ROADMAP](ROADMAP.md#kolejnosc).

| Etap / podsystem | Kontrakt | Kod | Benchmark |
|---|---|---|---|
| Stage 0 | `wgc/source@0` (szkic) | — | rulebook gry benchmarkowej |
| Stage 1 | `wgc/logic@0` (szkic) | — | `phenomena.yaml`, gold w M3 |
| Stage 1.5 | `wgc/digital@0` (szkic) | — | gold w M17–M21 |
| Stage 2 | planowany (M24) | — | — |
| Stage 3 | planowany (M25–M26) | — | — |
| Bramki | `wgc/gate@0` (szkic) | — | — |
| GLU | `glu/exec@0` (szkic, z polityką fallbacku i `premium_reason`) | — | — |
| Węzeł inferencji (`igw`) | `igw/api@0` (szkic) | — (M-GW1) | — (M-INF) |

<a id="nastepny-milestone"></a>
## Następny milestone: M1 Tożsamość, hashowanie i walidator referencji
**Dlaczego M1 jest pierwszy:** wszystko dalej zależy od tożsamości i hashy. Kotwice (`seg_hash`) w M2, klucze cache
i joby w M8–M11, przyrostowość w M13 i bramki w M7 potrzebują stabilnych ID, kanonicznej serializacji i walidacji
referencji. Model jobów GLU bez tożsamości artefaktów musiałby ją zgadywać. M-INF0 nie zmienia zakresu M1 poza
kształtem raportu (diagnostyki, punkt 3).

**Tor równoległy:** M-GW1 (Inference Gateway) nie zależy od domeny i może iść w osobnej sesji równolegle z M1–M10.
M-BASE (HUM) warto wykonać jak najwcześniej ([ROADMAP](ROADMAP.md#kolejnosc)).

**Zakres**
1. `wgc/ids.py`: gramatyka ID z [DATA-CONTRACTS.md](DATA-CONTRACTS.md#identyfikatory), rejestr prefiksów → dozwolone
   `kind`, funkcje `parse_id`, `check_kind_prefix`.
2. `wgc/canonical.py`: `canonical_json(obj) -> bytes` (sortowane klucze, NFC, bez `null`, separatory bez spacji),
   `content_hash(obj) -> "sha256:…"`, `text_hash(str)` (normalizacja z DATA-CONTRACTS §5),
   `projection(record, consumer)` v0 dla `rule`, `concept`, `relation`, `segment` (lista pól jako dane).
3. `wgc/validate.py`: `validate(paths) -> Report`. Report to lista diagnostyk
   `{code, severity: error|warning, subject: ID, message (PL), affected: [ID…]}` (podstawa późniejszego `wgc diagnose`
   i `wgc explain`, M13). Kody błędów:
   - L0: `contracts.errors`;
   - L1: `duplicate_id`, `kind_prefix_mismatch`, `unresolved_ref` (dla `refs`, `derived_from`, `realizes`, `covers`,
     `applies_to`, `from_case`, `relation.from/to`, `interpretation.ambiguity`, `blocker.cause/affects`,
     `anchors.seg`, `segment.doc`);
   - provenance: `anchor_hash_mismatch` (kotwica vs `segment.text_hash`), `missing_decision` (`human_decision` lub
     accepted `INT-` bez istniejącego `HD-`).
4. CLI: `python -m wgc validate <ścieżki…> [--json]` (argparse), kod wyjścia 1 przy błędach. Komunikaty po polsku.
5. Domknięcie fixture'ów: brakujące rekordy (np. `R-3.1`, `CON-ma`, `ACT-rally`, `CON-mp_spent`…) dopisane, tak aby
   `contracts/fixtures/valid/` był zbiorem zamkniętym. Przy okazji: `ENT-game.concept` wskazuje dziś `CON-scn.ford`
   (scenariusz), a powinien wskazywać pojęcie gry (np. `CON-game`). Nowe fixture'y niepoprawne dla każdego kodu L1/provenance
   w `contracts/fixtures/invalid/semantic/`.

**Pliki:** `wgc/ids.py`, `wgc/canonical.py`, `wgc/validate.py`, `wgc/__main__.py`, `tests/test_ids.py`,
`tests/test_canonical.py`, `tests/test_validate.py`, `contracts/fixtures/valid/*.yaml`,
`contracts/fixtures/invalid/semantic/*.yaml`, `docs/DATA-CONTRACTS.md` (doprecyzowania), STATUS, ROADMAP, handoff.

**Kryteria akceptacji**
- `python -m pytest` zielone.
- `python -m wgc validate contracts/fixtures/valid` → 0 błędów, kod 0.
- Każdy plik w `contracts/fixtures/invalid/semantic/` daje dokładnie oczekiwany kod błędu (zapisany w komentarzu
  pliku i sprawdzany w teście).
- `content_hash` ma test złoty (stała wartość dla stałego wejścia) i test niezależności od kolejności kluczy;
  `text_hash` jest niezmienniczy wobec zawijania wierszy i przeniesień.
- `kind` ↔ prefiks egzekwowane (np. `kind: rule` z `id: CON-x` → `kind_prefix_mismatch`).

**Testy:** jednostkowe dla ids, canonical i validate; parametryzowane po fixture'ach.

**Poza zakresem:** ingest PDF i prawdziwe hashe segmentów (M2), cytaty dosłowne i sygnały źródło↔IR (M5), ryzyko (M6),
bramki (M7), cokolwiek w `glu/`, zamrożenie `@1`.

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
| `wgc/contracts.py` szuka schematów w `../contracts/` (poza pakietem): instalacja nieedytowalna ich nie zabierze | CLI nie działa po `pip install .` | M1 albo M7: przenieść schematy do `wgc/` jako package data lub dodać je do dystrybucji |
| ADR-0002 obiecuje CLI `wgc` i `glu`, `pyproject` nie definiuje jeszcze `[project.scripts]` | brak poleceń po instalacji | M1 (`wgc`), M8 (`glu`) |
