# STATUS

- **Data aktualizacji:** 2026-10-06
- **Ostatni milestone:** M-STAB3b (stabilizacja po M9a, etap 3b: manifest wejść, projekcje, diagnostyka receiptu): done
- **Bieżący milestone:** M-STAB3c
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
  - zadanie `wgc.tables.parse@0`; komórki tabel w cache tekstu rozdziela tabulator bez zmiany `text_hash` (ADR-0024,
    zastąpiony przez ADR-0032);
  - planner (`glu/planner.py`), wykonawca Tier 0 (`glu/exec.py`) i `glu build --stage --scope --dry-run`;
    na `bench/minigame` build daje `TAB-4.3`.
- **M-STAB1 (etap naprawczy po przeglądzie [po M9a](reviews/2026-10-05-przeglad-po-M9a.md), ADR-0026):**
  - zapis pliku `kb/` przez atomową podmianę (`wgc/fsio.py`); awaria przed podmianą zachowuje poprzednie bajty (F01
    dla pojedynczego pliku);
  - blokada pisarza projektu `.glu/kb.lock` (procesy i wątki) wokół całego odczytu, merge'a, walidacji i zapisu
    w `accept()`. Zajęta dłużej niż 60 s daje `KBBusy`. `Workspace` z nieaktualnym inwentarzem daje `KBStale` (F02);
  - typy i schemat propozycji sprawdzane przed funkcjami domenowymi: diagnostyka zamiast `TypeError` (F08);
  - wykonawca Tier 0 rozróżnia odrzucenie (Attempt `rejected`), awarię operacyjną i błąd programu (Attempt `error`).

  Pozostałe ustalenia przeglądu (F03–F07, F09–F20) są otwarte; ich plan to M-STAB2, M-STAB3a–c i kwestie poniżej.
- **M9b (ADR-0030):**
  - zadanie `wgc.terms.harvest@0` (`wgc/terms.py`). Daje `concept` tylko dla wzorców o pewnej kategorii:
    - `NdM` → `die`;
    - nagłówek `Scenario: X` → `scenario`;
    - pozycja listy numerowanej `… Phase` → `phase`.

    Inne terminy nie trafiają do `kb/` (M14);
  - jeden job na dokument, niezależny od `--scope`; kotwica z cytatem dosłownym;
  - reguła ID pojęć: `CON-<klucz>` dla głównej instrukcji, `CON-<klucz SRC>:<klucz>` dla innych dokumentów
    ([DATA-CONTRACTS §10](DATA-CONTRACTS.md#id-pojec));
  - na `bench/minigame` build daje `TAB-4.3` i 6 pojęć.
- **M-STAB2 (ADR-0031, ustalenia F01 i F04 przeglądu):**
  - akceptacja zmieniająca dwa pliki `kb/` lub więcej idzie jedną partią z dziennikiem wycofania w `kb/.wgc-batch/`
    (`wgc/fsbatch.py`, format `wgc-kb-batch@1`, czyta też `@0`). Po przerwaniu `kb/` jest w całości stara albo
    w całości nowa;
  - nieudana partia ma trzy rozłączne wyniki: zatwierdzony, potwierdzone wycofanie (`KBWriteError`, job `failed`)
    i nierozstrzygnięty (`KBUnresolved`: intencja `rolling_back` albo jej brak, job zostaje w `validating`, receipt
    i dziennik zostają, build przerwany, rozstrzyga reconcile);
  - `wgc kb recover [--dry-run]`; `accept()` robi recovery pod blokadą przed odczytem `kb/`; `wgc validate` zgłasza
    `kb_batch_pending` (także dla `kb/logic` i pojedynczego pliku) i czyta `kb/` pod wspólną blokadą z pisarzem,
    bez tworzenia pliku blokady; pierwszy zapis w repo bez `.glu/kb.lock` wymusza ponowny odczyt
    (`kb_read_unstable` po 5 próbach);
  - receipt akceptacji (`generation`, `records`) w `.glu/kb-receipts/` i w Attempcie (`kb_receipt`, `glu/exec@0`);
  - `Store.finish_job`: Attempt i ostatnie przejścia joba w jednej transakcji;
  - `glu reconcile [--dry-run]` i krok startu `glu build`: joby martwych buildów uzgadniane z `kb/` (blokada
    żywotności `.glu/builds/<build>.lock`), bez nowych krawędzi tabeli przejść ([GLU §3](GLU.md#reconcile)).
- **M-STAB3a (ADR-0032, zastępuje ADR-0024; ustalenie F03 przeglądu):**
  - `struct_hash` segmentu: wersjonowany hash wierszy i komórek tekstu (`wgc/struct@0`, `wgc.canonical.structure`),
    obok `text_hash` ([DATA-CONTRACTS §5](DATA-CONTRACTS.md));
  - jest w projekcji `logic` segmentu (`wgc/projection@1`), więc ten sam tekst w innych komórkach lub wierszach daje
    inny klucz joba i `prov.inputs_hash`; `seg_hash` kotwic zostaje `text_hash`;
  - `Workspace.text` (planner, parsery, cytaty kotwic) sprawdza oba hashe; `wgc.tables.parse` i `wgc.terms.harvest`
    czytają tekst tylko przez `structure`;
  - `wgc source verify`: `segment_struct_mismatch`, `struct_hash_missing`, `cache_mismatch` także dla struktury;
  - ekstraktory `wgc.ingest.markdown@1` i `wgc.ingest.pdf@1`; inwentarz `@0` wymaga `wgc source extract` (jawna
    regeneracja: do tego czasu `glu build` kończy się kodem 2).
- **M-STAB3b (ADR-0033, ADR-0034; ustalenia F05 i F06 przeglądu):**
  - manifest wywołania `wgc/manifest@0` (`wgc/manifest.py`): zadanie, wersja projekcji, wejścia, dane autorytetu
    dokumentów źródłowych i kontekst `kb/` z hashami. Jedna definicja dla klucza joba i `prov.manifest`
    ([DATA-CONTRACTS §10](DATA-CONTRACTS.md#manifest)); zależności rekordu odtwarza `wgc.manifest.check` bez `.glu/`;
  - `prov.inputs_hash` to hash dowodów rekordu (kotwice, `derived_from`), a dowód spoza manifestu jest odrzucany;
  - `TaskSpec.authority_selector` (harvest: każdy dokument `rules`) i `context_selector`; `semantic_projection` dla
    jednego wejścia;
  - świeżość kontekstu `kb/`: migawka (`Workspace.pinned`), generacja jako token porównania w `accept()`,
    `KBContextStale`; manifest wykonania różny od planu kończy job przed implementacją;
  - projekcje `wgc/projection@2`: treść nieformalizowana reguł `none`/`partial`, definicje predykatów, rodzaje
    M10–M14 i E2E, bez zapasów ([DATA-CONTRACTS §5](DATA-CONTRACTS.md));
  - `glu receipt <job> [--json]`: porównanie `kb_receipt` z `kb/`, tylko do odczytu
    ([GLU §3](GLU.md#receipt)).

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
| Stage 0 | `wgc/source@0` (szkic; role, `seg_prefix`, `struct_hash`) | `wgc.source`, `wgc.ingest.markdown` (M2a), `wgc.ingest.pdf` (M2b); `struct_hash`, ekstraktory `@1` (M-STAB3a) | `bench/minigame/source/inventory.yaml` |
| Stage 1 | `wgc/logic@0` (szkic; `prov.manifest`) | `wgc.tasks`, `wgc.kb.accept`, `wgc.tables` (M9a); `wgc.fsio`, blokada i atomowy zapis `kb/` (M-STAB1); `wgc.terms` (M9b); `wgc.fsbatch`, `wgc kb recover` (M-STAB2); `wgc.manifest`, projekcje `@2` (M-STAB3b) | `phenomena.yaml`, gold w M3 |
| Stage 1.5 | `wgc/digital@0` (szkic) | — | gold w M17–M21 |
| Stage 2 | planowany (M24) | — | — |
| Stage 3 | planowany (M25–M26) | — | — |
| Bramki | `wgc/gate@0` (szkic) | — | — |
| GLU | `glu/exec@0` (szkic, z polityką fallbacku i `premium_reason`) | `glu.store`, `glu.states`, `glu status`, `glu export` (M8); `glu.planner`, `glu.exec`, `glu build` (M9a); `glu.reconcile`, `glu reconcile` (M-STAB2); `glu.receipt`, `glu receipt` (M-STAB3b) | build Tier 0 na `bench/minigame` w testach |
| Węzeł inferencji (`igw`) | `igw/api@0` (szkic) | — (M-GW1) | — (M-INF) |

<a id="nastepny-milestone"></a>
## Następny milestone: M-STAB3c Stabilizacja po M9a, etap 3c: kontrakt propozycji, ownership, wdrożenie ADR-0027
**Dlaczego teraz:** według [ROADMAP](ROADMAP.md#kolejnosc) tor domeny idzie przez M-STAB3c → M10. M-STAB3b dał jedną
definicję zależności joba (manifest, ADR-0033) i projekcje `@2` (ADR-0034). Przed pętlą structured output (M10)
potrzebne są: kontrakt propozycji dla modelu (F07, N07), własność wyników zadania (F11, N10) i jawna lista ról
kanonicznych z ADR-0027 (Q-13, Q-14). Dziś kotwica w dokumencie `community_interpretation` daje `explicit_source`.

**Środowisko:** GLU natywnie na Windows (ADR-0022). Zapis do `kb/`: ADR-0025, ADR-0026, ADR-0031, ADR-0033,
DATA-CONTRACTS §10.

**Tor równoległy:** M-GW1 (Inference Gateway) i M-BASE (HUM) bez zmian.

**Zakres:** [ROADMAP M-STAB3c](ROADMAP.md) (ustalenia F07 i F11, decyzje N07 i N10):
- kontrakt propozycji `wgc/proposal@0` (envelope), dispatch kontraktu etapu, lifecycle oddzielony od rozstrzygnięcia
  niejasności;
- ownership `zadanie + zakres wejść` z manifestem outputów (manifest wywołania z ADR-0033 opisuje wejścia, nie
  wyjścia);
- wdrożenie ADR-0027: lista ról kanonicznych, deklaracja inferencji zadania.

**Pierwsza czynność:** ADR kontraktu propozycji i ownership (F07, F11, N07, N10). Czytać:
- ADR-0025, ADR-0027, ADR-0030, ADR-0033;
- ustalenia F07, F09 i F11 [przeglądu](reviews/2026-10-05-przeglad-po-M9a.md);
- `wgc/kb.py` (`_shape_issues`, `_provenance`, `ROLE_KINDS`, `_accept_locked`), `wgc/manifest.py`, `wgc/tasks.py`.

**Kryteria akceptacji:** z ROADMAP: testy zmiany roli źródła (każda rola) i zniknięcia jednego outputu; kontrakt
propozycji z fixture'ami i DATA-CONTRACTS; `python -m pytest` zielone, test ciągłości zielony.

**Poza zakresem:** pełny graf zależności i przyrostowy rebuild (M13), cache (M11), trwałe ID (F10). Q-12, Q-16 i Q-17
pozostają otwarte (decyzja właściciela 2026-10-06), chyba że właściciel zdecyduje inaczej przed sesją.

## Otwarte kwestie
Zamknięte w M2b: Q-10 (biblioteka PDF, ADR-0021), Q-03 (GLU natywnie na Windows, ADR-0022). M8 nie otworzył nowych
kwestii (ustalenia właściciela w ADR-0023). M9a otworzył Q-12 i Q-13 (ADR-0025). Przegląd po M9a dodał Q-14 i Q-15.
Zamknięte po M-STAB1 decyzją właściciela (2026-10-05): Q-13 i Q-14 (ADR-0027, wdrożenie M-STAB3c/M10), Q-15 (ADR-0028,
wdrożenie M12). Kolejność potwierdzona: M9b przed M-STAB2. Grę pilotażową (Q-02) właściciel poda później. M9b otworzył
Q-16 i Q-17. M-STAB2 otworzył Q-18, zamkniętą przez właściciela 2026-10-06 (poniżej). M-STAB3a i M-STAB3b nie
otworzyły nowych kwestii.
Decyzje właściciela po M-STAB2 (2026-10-06, ADR-0031): dziennik partii zostaje w `kb/.wgc-batch/`; repo gry nie
ignoruje go w git (Q-18 zamknięta); automatyczny reconcile martwych buildów zostaje; przed M10 (w M-STAB3b)
dochodzi polecenie diagnostyczne porównujące receipt wskazanego joba z `kb/`, bez automatycznej naprawy (różnica
względem historycznego receiptu nie oznacza sama w sobie uszkodzenia); M-STAB3 podzielony na M-STAB3a/3b/3c;
Q-12, Q-16 i Q-17 pozostają otwarte.
Decyzja właściciela (2026-10-05, w trakcie M9b): przekład Stage 3 pisze premium dla jakości językowej, wierność
sprawdzają kroki deterministyczne i self-hosted (ADR-0029, wdrożenie M26; akceptacja M26 ze ślepym porównaniem stron).

| # | Kwestia | Kto | Kiedy |
|---|---|---|---|
| Q-02 | Wybór gry pilotażowej i reprezentatywnego rozdziału (wyjątek, limit liczbowy, tabela, errata/FAQ) plus kilka stron jako próbka kontrolna; rekomendacja: wybrać teraz, nie dopiero w M28 (przegląd F13/F15). Właściciel poda grę później | właściciel | przed M3 i M-BASE |
| Q-06 | Nazwa hosta węzła (`ai-node`?), sposób rozwiązywania (DNS routera, rezerwacja DHCP albo `hosts`) i adres dev machine do allowlisty | właściciel | przed M-NODE |
| Q-07 | Autostart węzła: Harmonogram zadań czy usługa (WinSW) | właściciel + M-NODE | M-NODE |
| Q-08 | Czy dopuszczamy `allow_premium_fallback: true` w jakimkolwiek buildzie (np. pilot z terminem) | właściciel | przed M12 |
| Q-04 | Czy glosy KB mają mieć drugi język (np. PL) jako widok Stage 3, czy wystarczy EN | właściciel | przed M7 (widoki) |
| Q-05 | Licencja repo narzędzia | właściciel | przed publikacją |
| Q-09 | Zakres `unresolved_ref` poza listą M1: referencje w wyrażeniach (`pred`, `is`, `val`, `count`), `ref_to`, `timing`, `emits`, `fires_on`, `legality`, `chain`, `ambiguities`, kroki testów; kontrola rodzaju celu (np. `interpretation.ambiguity` → `AMB-`). Fixture'y `valid/` już dziś je rozwiązują | M5 (L2) albo M7 | przed M5 |
| Q-11 | Ekstraktor PDF obsługuje jedną kolumnę: przed pierwszym PDF-em prawdziwej gry potrzebne są kolumny (wykrycie `column_scrambled` albo kolejność czytania), usuwanie nagłówków i stopek stron oraz decyzja o stronach bez warstwy tekstu (`image_only`, OCR). Zakres do ustalenia na PDF-ie gry pilotażowej (ADR-0021) | właściciel + IMPL | przed M28 |
| Q-12 | `accept()` waliduje całe `kb/` i każdy błąd blokuje zapis. Rekord unieważniony zmianą źródła (np. stara kotwica `TAB-4.3` po przenumerowaniu tabeli) blokuje każdy kolejny `accept()`, aż ktoś poprawi KB ręcznie. Trzeba rozdzielić błędy blokujące od stanu `stale` (ADR-0004, ADR-0025). Od M9b częściej: przemianowana faza zostawia stare pojęcie (`anchor_hash_mismatch`), a zmiana segmentu z kotwicami pojęć daje nieudany pierwszy build zadań wykonywanych przed harvest (ADR-0030, `tests/test_terms.py`) | M13 (graf, invalidacja) | przed M13 |
| Q-16 | Własność rekordów `CON-`: harvest nie usuwa pojęć, których już nie daje (F11), a model (M14) albo `HD-` z tym samym ID daje konflikt, po którym job harvest kończy się `failed`. Kto jest właścicielem pojęcia `die`/`phase`/`scenario`, gdy M14 je wzbogaci (definicja, `values`), i jak łączyć pojęcia między dokumentami (`CON-d6` i `CON-<klucz SRC>:d6`)? | ARCH + właściciel | M-STAB3c (ownership) albo przed M14 |
| Q-17 | Który dokument jest „główną instrukcją” (ID bez przedrostka) dla `TAB-` i `CON-`. `TAB-` ma regułę z M9a: bez przedrostka dla każdego dokumentu `rules`, więc dwa dokumenty `rules` z tabelą o tej samej etykiecie dają to samo ID. `CON-` bierze dokument `rules` o najmniejszym `SRC-` (ADR-0030), co zakłada nazewnictwo `wgc source init`: ręcznie dopisany `SRC-dsk.advanced` przejąłby tę rolę i zmienił ID. Propozycja: jawne pole w inwentarzu (np. `main: true` albo `seg_prefix` równy kodowi gry) jako jedno źródło dla obu prefiksów. To zmiana ID i kontraktu, więc potrzebuje decyzji | właściciel + ARCH | przed pierwszą grą z dwoma dokumentami `rules` |

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
| Job store ma jednego pisarza naraz (domyślny journal, `timeout` 5 s, bez WAL) | MCP (M22) równolegle z CLI może dostać `database is locked` | decyzja o WAL w M22 (ADR-0023); WAL nie chroni plików `kb/` (te chroni blokada ADR-0026) |
| Windows bez `fsync` katalogu: trwałość podmian partii i znacznika zatwierdzenia po odcięciu zasilania nie jest wymuszona (ADR-0031) | spójność `kb/` zależy od kolejności dziennika NTFS (nietestowane); Attempt `accepted` w SQLite może przetrwać utratę zmian `kb/` | awaria procesu jest pokryta testami (`os._exit`); rozbieżność po awarii zasilania pokazuje `glu receipt <job>` (porównanie `kb_receipt` z `kb/`, tylko odczyt, M-STAB3b), naprawia ją ponowny build |
| Reconcile kończy przerwany build `failed` (albo `done`), nie wznawia go | przerwana praca wymaga nowego buildu | świadomie (ADR-0023, ADR-0031); Tier 0 jest tani, cache M11 ograniczy koszt modeli |
| Receipt dowodzi zgodności treści z `kb/`, nie autorstwa | job martwego buildu uznany za `done`, gdy identyczny rekord dał inny job | wystarcza do uzgodnienia stanu (ADR-0031) |
| Blokada żywotności buildu i blokada startu (`.glu/builds/`, `.glu/build.lock`) to blokady systemowe jak `kb.lock` | na dysku sieciowym (SMB/NFS) mogą działać inaczej: reconcile mógłby uznać żywy build za martwy | repo gry na dysku lokalnym (jak w ADR-0026) |
| Pozostałość `kb/.wgc-batch/` po nieudanym usunięciu katalogu (np. antywirus na Windows) | `wgc validate` zgłasza `kb_batch_pending` mimo spójnego `kb/`; po wycofaniu w `accept()` wynik jest `KBUnresolved`, więc build się przerywa | `wgc kb recover` sprząta (idempotentne); `accept()` robi to samo pod blokadą; reconcile rozstrzyga job |
| Wynik nierozstrzygnięty (`KBUnresolved`) przy trwałej awarii I/O | każdy kolejny `glu build` kończy się kodem 2 na starcie (recovery zawodzi), dopóki I/O nie wróci | świadomie: nie budować na niepewnym `kb/`; `wgc kb recover` po usunięciu przyczyny, potem `glu reconcile` |
| Walidator czyta `kb/` pod blokadą pisarza `.glu/kb.lock` | `wgc validate` w trakcie buildu czeka na bieżący `accept()` (i odwrotnie); przy blokadzie zajętej ponad 60 s `kb_read_unstable` | akceptacje trwają ułamki sekundy; walidować po zakończeniu buildów |
| Zmiana `kb/` spoza blokady (edytor, `git checkout`) przywracająca identyczne bajty między kontrolami walidatora | mieszana wersja niewykryta (ABA) | blokada doradcza (ADR-0026); nie edytować `kb/` w trakcie walidacji ani buildu |
| `accept()` z `job` wywołany poza GLU zostawia receipt w `.glu/kb-receipts/` | pliki receiptów rosną | GLU usuwa receipt po zapisie Attemptu; `glu reconcile` usuwa osierocone |
| Blokada `.glu/kb.lock` jest doradcza | ręczna edycja, `git checkout` i czytelnicy bez blokady (`wgc validate`, planner) jej nie respektują; na Windows otwarty plik wymusza ponowienia `os.replace` (ok. 1,5 s), potem `KBWriteError` | nie edytować `kb/` w trakcie buildu; zamknąć edytor pliku `kb/` przed buildem |
| Zadanie czytające `kb/` jako kontekst w buildzie, w którym wcześniejszy job zmienia ten kontekst (np. harvest przed zadaniem czytającym pojęcia) | job kończy się błędem „wejścia joba zmieniły się od planu”, potrzebny drugi build | świadomie (ADR-0033): nigdy wynik ze starego kontekstu; kolejność i zależności jobów w M13. Dziś żadne zadanie nie czyta kontekstu `kb/` |
| Manifest wywołania jest powtarzany w `prov` każdego rekordu joba (harvest: w każdym pojęciu dokumentu) | pliki `kb/` rosną, linie `prov` są długie i mniej czytelne | przyjęty koszt (ADR-0033); przy dużych grach przeniesienie manifestów do osobnego pliku w nowym ADR |
| Pierwszy build po M-STAB3b w istniejącym repo gry | każdy rekord `TAB-`/`CON-` zapisany jako „zmieniony” (nowe `prov.manifest`, `prov.inputs_hash` z wersją projekcji `@2`) | jednorazowo, oczekiwane (ADR-0033, ADR-0034); rekord bez `prov.manifest` nie jest błędem walidacji |
| Testy awarii: wyjątki wstrzykiwane i (od M-STAB2) procesy potomne kończone `os._exit` w punktach protokołu | odcięcie zasilania, zabicie procesu wewnątrz `fsync`/`os.replace` i dyski sieciowe (SMB) niezbadane; na Windows trwałość podmiany nie jest wymuszona (brak `fsync` katalogu) | repo gry na dysku lokalnym; ewentualny test fizyczny przy M-NODE/pilocie |
| Gałąź POSIX `wgc.fsio` i `wgc.fsbatch` (`fcntl.flock`, `fsync` katalogu, tryb pliku) nie była uruchamiana; M-STAB1 i M-STAB2 nie były testowane na Pythonie 3.10 | błąd widoczny dopiero na Linux/WSL albo starszym Pythonie | uruchomić `python -m pytest` na Linux/WSL i 3.10 przy najbliższej okazji (np. M-NODE) |
| Store waliduje każdy rekord schematem przy zapisie | wolniejsze buildy z tysiącami jobów | pomiar w M11 (w M9a nie mierzono: build gry benchmarkowej ma 1 job); w razie potrzeby walidacja tylko przy eksporcie (ADR-0023) |
| Narzędzie czytające pliki KB przez `contracts.load` pominie dokumenty po `---` (ADR-0019) | ciche pominięcie rekordów | czytać przez `wgc.validate.load_documents` |
| `bench/minigame/source/inventory.yaml` i fixture'y `valid/` mają te same ID segmentów | `wgc validate bench/minigame/source contracts/fixtures/valid` w jednym przebiegu daje `duplicate_id` (a `wgc validate bench` dodatkowo `schema_error` dla `phenomena.yaml`, który nie jest dokumentem KB) | walidować osobno (DATA-CONTRACTS §9) |
| Klucze segmentów bez numeru (`u1`, `u2`…) zależą od pozycji | wstawienie wstępu przenumeruje je i unieważni kotwice do nich | nie kotwiczyć reguł do segmentów bez numeru (ADR-0020) |
| Nowa wersja `pdfminer.six` zmienia pozycje znaków albo dekodowanie | `segment_hash_mismatch` albo `segment_struct_mismatch` w `wgc source verify` bez zmiany pliku | minimalne wersje równe przetestowanym; dryf wykrywa `wgc source verify`; zmianę reguł ekstraktora wprowadza nowa wersja `wgc.ingest.pdf@N` (ADR-0021) |
| Repo gry z inwentarzem z ekstraktora `@0` (sprzed ADR-0032) | `glu build` kończy się kodem 2, `wgc source verify` zgłasza `struct_hash_missing` | `wgc source extract` (jawna regeneracja, ADR-0032); pierwszy build potem zapisuje rekordy z nowym `prov.inputs_hash` (jednorazowo `zmienione`) |
| Przezawijanie akapitów (nowe wydanie PDF z tym samym tekstem) zmienia `struct_hash` | `segment_struct_mismatch` w verify; inne klucze jobów wszystkich zadań czytających segment, od M11 missy cache także dla zadań modelowych | świadomie (ADR-0032: bezpieczny kierunek); projekcji tylko z `text_hash` nie dodano w M-STAB3b, bo żadne zadanie nie czyta wyłącznie `normalize_text` (ADR-0034) |
| Rekord zaakceptowany przed zmianą `struct_hash` segmentu nie jest oznaczany jako nieaktualny | walidator nie przelicza `prov.inputs_hash`; stary wynik zostaje w `kb/` do ponownego buildu | ponowny build zastępuje rekord (inny klucz joba); `wgc.manifest.check(ws, prov.manifest)` pokazuje zmienione wpisy bez `.glu/` (M-STAB3b); oznaczanie `stale` w M13 (Q-12) |
| Fixture `logic.minigame.yaml` ma `TAB-crt` z `tool: wgc.tables.parse@0`, ale z ID i wartościami (`none`, `routed`), których deterministyczny parse nie daje (`TAB-4.3`, `No effect`) | mylący przykład dla kolejnych sesji | fixture to ilustracja kontraktu, nie gold; gold tabeli w M3 |
| Fixture `logic.minigame.yaml` przypisuje `tool: wgc.terms.harvest@0` pojęcia o kategoriach, których harvest nie daje (`CON-rally` jako `action`, `CON-game`, `CON-enter_hex`), i klucz `CON-scn.ford` (harvest: `CON-scn.the_ford`) | mylący przykład: sugeruje, że Tier 0 zgaduje kategorie | ilustracja kontraktu, nie gold (ADR-0030); gold pojęć w M3 |
| Pojęcie zakotwiczone w dokumencie `community_interpretation` albo `prior_translation` dostaje dziś `explicit_source` i `accepted` (harvest czyta każdy obecny dokument) | niekanoniczny termin w KB | ADR-0027 wdraża M-STAB3c; job harvest obejmuje jeden dokument, więc odrzucenie nie zablokuje innych |
| Wzorce harvest są ścisłe (bez `Scenario 2: X`, `1. Movement Phase: …`, list punktowanych, `… Step`, gołego `d6`) | na prawdziwej grze mniej pojęć Tier 0, więcej pracy w M14 | świadomie; rozszerzenie to `wgc.terms.harvest@1` po próbce gry pilotażowej (Q-02) |
| `accept()` przy każdym jobie czyta i waliduje całe `kb/` | wolne buildy przy tysiącach rekordów | pomiar w M11/M14; w razie potrzeby walidacja przyrostowa (M13) |
| PDF gry nie pogrubia numerów reguł albo ma kilka kolumn | segmentacja PDF zlewa reguły albo daje fałszywe tabele | sprawdzić na PDF-ie gry pilotażowej (Q-11), render stron do porównania (`wgc source render`) |
