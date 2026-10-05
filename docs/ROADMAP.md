# Roadmapa

Każdy milestone to **jedna ograniczona sesja**: skończony zakres, testy, kryteria akceptacji, dokumentacja, handoff
([SESSION-PLAYBOOK.md](SESSION-PLAYBOOK.md)). Jeśli milestone nie mieści się w sesji, dzieli się go na `Mn.a`, `Mn.b`
(z wpisem w tym pliku), zamiast przeciągać. Rola wykonawcy jest zaleceniem ([SESSION-PLAYBOOK.md](SESSION-PLAYBOOK.md#role-modeli)).

Legenda roli: **ARCH** model architektoniczny, **IMPL** model implementacyjny, **HUM** wymaga człowieka.
Status: `done`, `next`, `planned`, `optional`.

## Faza 0: fundament
### M0: Architektura i system ciągłości (Session 0)
- **Status:** done · **Rola:** ARCH
- **Wynik:** dokumentacja `docs/`, ADR-0001…0014, kontrakty `@0` z fixture'ami, gra benchmarkowa, testy ciągłości.

### M1: Tożsamość, hashowanie i walidator referencji
- **Status:** next · **Rola:** IMPL · **Zależy od:** M0
- **Zakres:** `wgc/ids.py` (gramatyka, rejestr prefiksów, `kind` ↔ prefiks), `wgc/canonical.py` (kanoniczny JSON,
  sha256, projekcje semantyczne v0 dla `rule`, `concept`, `relation`, `segment`), `wgc/validate.py` (L0 + L1 + reguły
  provenance spoza schematu: istnienie segmentu kotwicy, zgodność `seg_hash`, `HD-` dla `human_decision` i accepted
  `INT-`), CLI `wgc validate`, domknięcie fixture'ów (zbiór bez wiszących referencji).
- **Szczegóły:** [STATUS.md](STATUS.md#nastepny-milestone).

### M2: Stage 0: inwentarz i ingest źródeł
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M1
- **Zakres:** `wgc source init/scan/extract/verify`; ingest Markdown (gra benchmarkowa) i PDF (PyMuPDF): segmentacja
  po numerach reguł, typy segmentów, `text_hash`, flagi wizualne (kolor zmian, przekreślenie), render strony do
  weryfikacji; tekst w `.glu/source/`, inwentarz commitowany.
- **Akceptacja:** `bench/minigame` → inwentarz z prawdziwymi hashami, fixture'y przeliczone; deterministyczność
  (dwa przebiegi = identyczne hashe); test na PDF wygenerowanym z tekstu własnego.

### M3: Złoty model logiki gry benchmarkowej + scorer
- **Status:** planned · **Rola:** ARCH + HUM (przegląd) · **Zależy od:** M2
- **Zakres:** `bench/minigame/gold/logic.yaml` (wszystkie reguły 1.1–7.2, pojęcia, relacje, tabela, procedura
  sekwencji, AMB-001, przypadki dla każdej polaryzacji); `wgc bench score logic` (metryki z QUALITY §2).
- **Akceptacja:** gold przechodzi `wgc validate` bez ostrzeżeń; scorer daje 100% dla gold i < 100% dla 3 ręcznych zniekształceń.

### M4: Benchmark mutacyjny
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M3
- **Zakres:** operatory z QUALITY §3 dla IR (`wgc bench mutate`), harness wykrycia (kto wykrył: L1, L2, ryzyko), raport.
- **Akceptacja:** każdy operator generuje mutację gold; raport tabelaryczny; test regresji harnessu.

### M5: Walidator L2 (provenance, cytaty, sygnały źródło↔IR)
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M2, M4
- **Zakres:** cytat dosłowny w segmencie, słownik sygnałów EN (wersjonowany, idea z `wgu check fidelity`), reguły:
  zakaz → `must_not`/negacja, operator graniczny → `cmp`, liczby źródła ⊆ liczby IR, marker wyjątku → relacja.
- **Akceptacja:** 0 fałszywych alarmów na gold; wykrycie mutacji krytycznych raportowane przez M4 (cel ≥ 80%; resztę łapie ryzyko).

### M6: Model ryzyka v0
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M5
- **Zakres:** `wgc.risk` (cechy z LOGIC-MODEL, wagi, progi, reguły `forced`), `wgc risk score`, zapis `risk` w rekordach.
- **Akceptacja:** 100% mutacji krytycznych z M4 ma klasę ≥ `high` lub błąd L2; rozkład klas na gold w raporcie.

### M7: Bramki, statusy obliczane, widoki z `--check`, `project.yaml`
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M6
- **Zakres:** `wgc/project@0`, `wgc gate stage0|stage1`, polityka `gate.stage1@0`, `wgc view` (Markdown) z `--check`,
  stany i ich pierwszeństwo z PIPELINE §2.
- **Akceptacja:** gold → `validated_with_open_issues` (AMB-001); zmiana hasha segmentu → `stale`; widok nieaktualny → `--check` = 1.

## Faza 1: rdzeń GLU
### M8: Job store i maszyna stanów joba
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M1
- **Zakres:** `glu.store` (SQLite: build, job, attempt, routing_decision; migracje schematu bazy), przejścia stanów
  z GLU §3 (nielegalne przejście = wyjątek), `glu status`.
- **Akceptacja:** testy przejść (legalne i nielegalne), trwałość po restarcie, eksport rekordów zgodny z `glu/exec@0`.

### M9: TaskSpec, wykonawca deterministyczny, planner buildu
- **Status:** planned · **Rola:** ARCH (kontrakt) + IMPL · **Zależy od:** M7, M8
- **Zakres:** interfejs `TaskSpec` (ARCHITECTURE §2), rejestr zadań WGC, wykonawca Tier 0, `glu build --stage --scope
  --dry-run`, pierwsze zadania deterministyczne (harvest terminów, parse tabel, relacje warstwy scenariusza).
- **Akceptacja:** build Tier 0 na `bench/minigame` daje rekordy przechodzące walidację; `accept()` jedyną drogą zapisu do `kb/`.

### M10: Providerzy fake/replay/openai_compat + pętla structured output
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M9
- **Zakres:** `glu.providers` (interfejs z INFERENCE-ROUTING §3), wykonawca lokalny, pętla schemat → domena →
  accept/retry/escalate z feedbackiem błędów, provenance dopisywane deterministycznie (ADR-0014).
- **Akceptacja:** testy na `fake` (poprawne, niepoprawne schematycznie, niepoprawne domenowo, wyczerpane próby);
  `openai_compat` testowany na atrapie HTTP; zero testów wymagających GPU.

### M11: Cache i ledger metryk
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M10
- **Zakres:** cache L1/L2 (GLU §6), bloby, `glu cache gc`, metryki Attempt/Build, `glu stats`.
- **Akceptacja:** drugi identyczny build = 0 wywołań providera; zmiana `profile_fingerprint` lub `prompt_version` = miss.

### M12: Routing deterministyczny
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M6, M11
- **Zakres:** `routing@0` (tabela INFERENCE-ROUTING §2) jako dane, `routing_decision` z powodami, audyt próbkowy, budżety.
- **Akceptacja:** testy tabelaryczne dla każdej reguły; budżet wyczerpany → `waiting_review`, nigdy akceptacja lokalna.

### M13: Graf zależności i przyrostowość
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M12
- **Zakres:** `glu.graph` z krawędzi KB, invalidacja `stale`, early cutoff na projekcjach, `glu build --incremental`.
- **Akceptacja:** zmiana jednego segmentu przelicza tylko jego domknięcie (test liczy joby); zmiana glosy nie
  unieważnia Stage 1.5; zmiana layoutu nie dotyka Stage 1.

### M-INF: Wybór serwera i modeli lokalnych (benchmark)
- **Status:** planned · **Rola:** IMPL + HUM (maszyna z RTX 3090) · **Zależy od:** M10, M3
- **Zakres:** instrukcja środowiska WSL2/CUDA, 2–3 kandydatów na `local_fast` i `local_semantic`, pomiar jakości
  (scorer M3), przepustowości, VRAM, czasu ładowania; wynik w ADR.
- **Akceptacja:** ADR z wyborem i liczbami; `profiles.yaml` przykładowy w `docs/`.

## Faza 2: Stage 1 z modelami
### M14: Pakiet zadań Stage 1 (ekstrakcja reguł, pojęć, relacji, przypadków)
- **Status:** planned · **Rola:** ARCH (prompty) + IMPL · **Zależy od:** M13, M-INF
- **Zakres:** TaskSpec `logic.rule.extract`, `logic.concept.extract`, `logic.relations`, `logic.case.generate`,
  `logic.ambiguity.detect`; context buildery; zamrożenie `wgc/logic@1`.
- **Akceptacja:** build Stage 1 na `bench/minigame` z lokalnym modelem (albo `replay` nagrań) → scorer ≥ progów
  QUALITY §5; raport kosztu i routingu.

### M-BASE: Pomiar baseline kosztu obecnego workflow
- **Status:** planned · **Rola:** HUM + IMPL · **Zależy od:** M3 (korpus)
- **Zakres:** procedura z COST §1 na starym narzędziu.
- **Akceptacja:** `B_logic`, `B_translate` w STATUS; metoda opisana tak, by dało się powtórzyć.

### M15: Premium: review package, `anthropic`, `desktop_pull`
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M14
- **Zakres:** budowa pakietu (k-hop, limit tokenów), `answer_schema`, provider `anthropic`, kolejka `desktop_pull`, `glu review`.
- **Akceptacja:** pakiety ≤ 4k tokenów dla gold; odpowiedź niezgodna ze schematem → retry/odrzucenie; testy na `fake`.

### M16: Decyzje człowieka i kolejka pytań
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M15
- **Zakres:** `glu decide` (pytania zamknięte z wariantami i rekomendacją), zapis `HD-`, przejście `INT-` → accepted,
  limit pytań na build.
- **Akceptacja:** AMB-001 przechodzi pełną ścieżkę do `HD-` i odblokowuje `BLK-001` w gold.

## Faza 3: Stage 1.5
### M17: Stan, wartości pochodne, inwarianty, `wgc/state@0`
- **Status:** planned · **Rola:** ARCH + IMPL · **Zależy od:** M7
- **Zakres:** domknięcie schematu `entity`/`derived`/`invariant`, format snapshotu stanu, walidacja fixture'ów stanu wobec `ENT-`.
- **Akceptacja:** gold digital (stan) dla gry benchmarkowej; snapshot round-trip (kanoniczny hash stabilny).

### M18: Akcje, legalność, zdarzenia
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M17
- **Zakres:** domknięcie `action`/`legality`/`event`, szablon Tier 0: `prohibition` → `LEG-`, walidacja `reason_code`.
- **Akceptacja:** gold akcji i legalności dla rozdziałów 3–5 gry benchmarkowej.

### M19: Timing, triggery, decyzje, losowość, informacja ukryta, pierwszeństwo
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M18
- **Zakres:** `sequence` z `PROC-` (Tier 0), `trigger`, `decision_point`, `random_source`/`modifier`, `hidden_info`, `priority` z `REL-`.
- **Akceptacja:** gold dla całej gry benchmarkowej; `BLK-001` generowany automatycznie z AMB-001.

### M20: Testy, śledzenie, pokrycie, blokery, engine kit
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M19
- **Zakres:** `wgc trace --up/--down`, metryki pokrycia (DIGITALIZATION), `wgc gate stage1_5`, `wgc export engine-kit`,
  import `engine-results.json`.
- **Akceptacja:** łańcuch SEG → TST i TST → SEG dla gold; raport pokrycia; niezgodny `ruleset_hash` odrzucony.

### M21: Pakiet zadań Stage 1.5 + referencyjny interpreter testów
- **Status:** planned · **Rola:** ARCH + IMPL · **Zależy od:** M20, M14
- **Zakres:** TaskSpec 1.5 (z kontekstem wyłącznie ze Stage 1), mały interpreter testów dla gry benchmarkowej
  (`bench/`), mutacje specyfikacji; zamrożenie `wgc/digital@1`.
- **Akceptacja:** złote testy przechodzą na interpreterze; mutacje spec wykryte; build 1.5 na lokalnym modelu ≥ progów.

## Faza 4: interfejsy
### M22: MCP tylko do odczytu + konfiguracja bezpieczeństwa
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M16
- **Zakres:** serwer stdio, narzędzia odczytu z MCP.md, `mcp.yaml` (allowlisty, zakresy, redakcja logów).
- **Akceptacja:** testy kontraktowe narzędzi bez Claude Desktop; próba wyjścia poza allowlistę odrzucona; test ręczny z Claude Desktop przez `wsl.exe`.

### M23: MCP zapis (review, decyzje, build) + Desktop Extension
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M22
- **Akceptacja:** `review_submit` przechodzi przez walidatory; `build_start` domyślnie `dry_run`; pakiet rozszerzenia instaluje się w Claude Desktop.

## Faza 5: Stage 2 i 3
### M24: Stage 2: model redakcyjny i pomiar oprawy
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M7
- **Zakres:** `wgc/editorial@0`, pomiar oprawy PDF (idea `wgu pdf layout`), zadania lokalne rejestru i konwencji, `wgc gate stage2`.
- **Akceptacja:** gold editorial gry benchmarkowej; scorer editorial.

### M25: Glosariusz pojęciowy i polityka przekładu
- **Status:** planned · **Rola:** ARCH + HUM · **Zależy od:** M24
- **Zakres:** `wgc/publication@0` (glosariusz z warstwami, dowodami, statusami), przeniesienie warstw common/era/series
  z `wgu` jako danych (decyzje D-01…D-10 właściciela), lint homonimów, bramka „terminy zatwierdzone”.
- **Akceptacja:** glosariusz PL dla gry benchmarkowej; lint wykrywa wspólny odpowiednik dwóch mechanik.

### M26: Przekład segmentów + wsteczna kontrola IR
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M25, M15
- **Zakres:** `translate.segment`, kroki 1–5 weryfikacji (EDITORIAL-PUBLICATION), `ir_hash`/`glossary_hash`, punktowa
  aktualizacja po zmianie terminu, referencyjny przekład PL gry benchmarkowej.
- **Akceptacja:** mutacje przekładu wykryte (≥ progów); zmiana terminu unieważnia tylko segmenty z tym `CON-`.

### M27: Publikacja LaTeX
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M26
- **Zakres:** API makr semantycznych, generator stylu z `layout_spec`, `wgc publish build` (LuaLaTeX w WSL), słowniczek, pomoce do gry z `PROC-`.
- **Akceptacja:** PDF gry benchmarkowej; zmiana layoutu nie unieważnia przekładów ani Stage 1.

## Faza 6: pilotaż
### M28: Pilot na prawdziwej grze + porównanie z baseline
- **Status:** planned · **Rola:** HUM + IMPL · **Zależy od:** M21, M27, M-BASE
- **Zakres:** jedna gra (wybór właściciela), Stage 0–1.5 dla 1–2 rozdziałów, raport kosztu (premium, GPU, czas) vs `B_*`.
- **Akceptacja:** premium ≤ 2× baseline; FN z audytu ≤ progu; decyzja o dalszym rozwoju w ADR.

### M-LEG: Importer `wgu/kb@1` (opcjonalny)
- **Status:** optional · **Rola:** IMPL · **Zależy od:** M3
- **Zakres:** jednokierunkowy import starej KB do `private/bench/` jako materiał porównawczy (np. GCACW-PL). Nie jest migracją gier.
