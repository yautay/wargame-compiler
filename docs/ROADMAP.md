# Roadmapa

Każdy milestone to **jedna ograniczona sesja**: skończony zakres, testy, kryteria akceptacji, dokumentacja, handoff
([SESSION-PLAYBOOK.md](SESSION-PLAYBOOK.md)). Jeśli milestone nie mieści się w sesji, dzieli się go na `Mna`, `Mnb` (bez kropki)
(z wpisem w tym pliku), zamiast przeciągać. Rola wykonawcy jest zaleceniem ([SESSION-PLAYBOOK.md](SESSION-PLAYBOOK.md#role-modeli)).

Legenda roli: **ARCH** model architektoniczny, **IMPL** model implementacyjny, **HUM** wymaga człowieka.
Status: `done`, `next`, `planned`, `optional`.

<a id="kolejnosc"></a>
## Kolejność wykonania
Sekcje niżej grupują milestone'y tematycznie. Kolejność wykonania (strzałka = kolejność; zależności podaje każdy milestone):

```text
tor domeny + GLU:  M1 → M2 → M8 → M9 → M10 ─────────┐
tor węzła (LAN):   M-GW1 → M-NODE (HUM) ─────────────┼─→ M-E2E (walking skeleton przez LAN) → M3 → M4 → M5 → M6 → M7
pomiar:            M-BASE (HUM, jak najwcześniej)    │       → M11 → M12 → M13 → M-GW2 → M-INF → M14 → M15 → M16 → …
                                                     │   (M-VLLM, M-GW3: optional, tylko gdy pomiar tego wymaga)
```
- Tor węzła nie zależy od domeny (węzeł nie zna WGC), więc M-GW1 i M-NODE mogą iść równolegle z M1–M10.
- **M-E2E** to wczesny pionowy przekrój: jedna reguła przechodzi source → Stage 1 → GLU → węzeł w LAN → walidacja →
  `kb/` → Stage 1.5 → test, z premium jako `fake`.
- Mapa tematów inferencji:

  | Temat | Milestone |
  |---|---|
  | Inference Provider Contract | M-INF0 (kontrakt `igw/api@0`), M10 (kod) |
  | Remote Self-Hosted Provider | M10 |
  | Inference Gateway | M-GW1 |
  | Node Runtime | M-GW1 (adapter), M-NODE (instalacja), M-GW2 (supervisor) |
  | LAN Security | M-GW1 (aplikacja), M-NODE (firewall, TLS, sekrety) |
  | Health / Capabilities | M-GW1 (endpointy), M10 (klient) |
  | Model Profiles | M-INF0 (projekt), M-GW1 (`node.yaml`), M10 (`profiles.yaml`), M-INF (wybór modeli) |
  | Queue / Scheduling | M-GW1 (kolejka), M-GW2 (scheduler, cykl życia) |
  | Diagnostics | M-E2E (`glu doctor`), M-GW2 (`igw doctor`) |
  | End-to-end LAN test | M-E2E |

## Faza 0: fundament
### M0: Architektura i system ciągłości (Session 0)
- **Status:** done · **Rola:** ARCH
- **Wynik:** dokumentacja `docs/`, ADR-0001…0014, kontrakty `@0` z fixture'ami, gra benchmarkowa, testy ciągłości.

### M-INF0: Korekta architektury: self-hosted inference na węźle w LAN
- **Status:** done · **Rola:** ARCH · **Zależy od:** M0
- **Wynik:**
  - „local” = self-hosted;
  - osobny węzeł RTX 3090 w LAN jako wymienialny worker;
  - Inference Gateway `igw` i protokół `igw/api@0` (`contracts/schemas/inference.schema.json` + fixture'y);
  - `glu/exec@0`: `fallback_policy`, `premium_reason`, `waiting_inference`, pola węzła w Attempt;
  - ADR-0015…0018 (zastępują ADR-0008 i ADR-0009);
  - `docs/inference/NODE.md`, `docs/inference/DEPLOYMENT.md`;
  - nowa kolejność roadmapy.

  Macierz DoD: [DOD-M-INF0.md](DOD-M-INF0.md).

### M1: Tożsamość, hashowanie i walidator referencji
- **Status:** next · **Rola:** IMPL · **Zależy od:** M0
- **Zakres:** `wgc/ids.py` (gramatyka, rejestr prefiksów, `kind` ↔ prefiks), `wgc/canonical.py` (kanoniczny JSON,
  sha256, projekcje semantyczne v0 dla `rule`, `concept`, `relation`, `segment`), `wgc/validate.py` (L0 + L1 + reguły
  provenance spoza schematu: istnienie segmentu kotwicy, zgodność `seg_hash`, `HD-` dla `human_decision` i accepted
  `INT-`), CLI `wgc validate`, domknięcie fixture'ów (zbiór bez wiszących referencji). Raport walidatora to lista
  **diagnostyk** `{code, severity, subject, message, affected}` (podstawa `wgc diagnose` i `wgc explain`).
- **Szczegóły:** [STATUS.md](STATUS.md#nastepny-milestone).

### M2: Stage 0: inwentarz i ingest źródeł
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M1
- **Zakres:** `wgc source init/scan/extract/verify`; ingest Markdown (gra benchmarkowa) i PDF (PyMuPDF): segmentacja
  po numerach reguł, typy segmentów, `text_hash`, flagi wizualne (kolor zmian, przekreślenie), render strony do
  weryfikacji; tekst w `.glu/source/`, inwentarz commitowany. Kontrakt `source_document`: role `living_rules`,
  `community_interpretation` i domyślne pierwszeństwo według roli ([LOGIC-MODEL](LOGIC-MODEL.md#pierwszenstwo-zrodel)).
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
- **Status:** planned · **Rola:** ARCH (kontrakt) + IMPL · **Zależy od:** M2, M8
- **Zakres:** interfejs `TaskSpec` (ARCHITECTURE §2, z `decoding_schema`), rejestr zadań WGC, wykonawca Tier 0,
  `glu build --stage --scope --dry-run`, pierwsze zadania deterministyczne (harvest terminów, parse tabel, relacje
  warstwy scenariusza). Sprawdzanie bramek przez planner dochodzi w M12 (po M7). Dzięki temu M9 nie czeka na M3–M7,
  a walking skeleton (M-E2E) powstaje wcześnie.
- **Akceptacja:** build Tier 0 na `bench/minigame` daje rekordy przechodzące walidację; `accept()` jedyną drogą zapisu do `kb/`.

### M10: Providerzy fake/replay/self_hosted + pętla structured output
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M9 (kontrakt `igw/api@0` z M-INF0)
- **Zakres:**
  - `glu.providers` z interfejsem INFERENCE-ROUTING §3: `generate`, `embed?`, `health`, `capabilities`, `models`
    i typowane błędy;
  - **`self_hosted`**: klient `igw/api@0` przez HTTPS z `ca_file` i tokenem ze zmiennej środowiskowej; nazwa hosta
    z konfiguracji, nigdy IP na sztywno; klient HTTP `httpx` (dopisany do `requirements.txt`, transport w pamięci w testach);
  - `glu/profiles@0` (`profiles.yaml`: endpointy, profile, `fallback`);
  - wykonawca self-hosted;
  - pętla schemat → domena → accept/retry/escalate z feedbackiem błędów;
  - błąd dostępności → `waiting_inference` bez zużycia prób, bez premium (ADR-0017);
  - provenance dopisywane deterministycznie (ADR-0014).
- **Akceptacja:**
  - testy na `fake` (poprawne, niepoprawne schematycznie, niepoprawne domenowo, wyczerpane próby);
  - `self_hosted` testowany na atrapie bramki w procesie (transport w pamięci, bez gniazd): sukces, `model_loading`
    z `Retry-After`, 401, timeout, `queue_full`;
  - niedostępność nie produkuje Attemptu premium;
  - zero testów wymagających GPU lub sieci.

### M11: Cache i ledger metryk
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M10
- **Zakres:** cache L1/L2 (GLU §6) z `profile_fingerprint` = hash(`model_fingerprint` z węzła, profil węzła, parametry
  próbkowania z `profiles.yaml`), `inference_snapshot` buildu,
  bloby, `glu cache gc`, metryki Attempt/Build (także `premium_by_reason`, `local_queue_seconds`), `glu stats`.
- **Akceptacja:** drugi identyczny build = 0 wywołań providera; zmiana `model_fingerprint` na węźle, parametrów
  próbkowania w `profiles.yaml` lub `prompt_version` = miss;
  zmiana endpointu lub węzła z tym samym fingerprintem = hit; build z cache L2 kończy się bez węzła.

### M12: Routing deterministyczny
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M6, M11
- **Zakres:** `routing@0` (tabela INFERENCE-ROUTING §2, reguły 1–13) jako dane, `routing_decision` z powodami
  i `premium_reason`, lokalny multi-pass (`local_deep` jako rozjemca i pass naprawczy), audyt próbkowy, budżety,
  polityka niedostępności, sprawdzanie bramek w plannerze, `glu explain <job|rekord>` (dlaczego self-hosted, dlaczego
  premium).
- **Akceptacja:** testy tabelaryczne dla każdej reguły; budżet wyczerpany → `waiting_review`, nigdy akceptacja lokalna;
  węzeł niedostępny + `allow_premium_fallback: false` → 0 jobów premium; przy `true` → `premium_reason:
  self_hosted_unavailable` w każdej decyzji; reguły `forced` idą do premium także po zgodzie `local_deep`.

### M13: Graf zależności i przyrostowość
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M12
- **Zakres:** `glu.graph` z krawędzi KB, invalidacja `stale`, early cutoff na projekcjach, `glu build --incremental`,
  `wgc explain <ID>` / `wgc diagnose` (diagnostyki z listą dotkniętych rekordów, np. „R-014 zależy od nieaktualnego
  SEG-031 → ACT-007, LEG-003, TST-009”), test właściwości: build przyrostowy = build od zera (QUALITY §3a).
- **Akceptacja:** zmiana jednego segmentu przelicza tylko jego domknięcie (test liczy joby); zmiana glosy nie
  unieważnia Stage 1.5; zmiana layoutu nie dotyka Stage 1.

## Faza 1b: self-hosted inference (węzeł w LAN)
Architektura: [inference/NODE.md](inference/NODE.md), wdrożenie: [inference/DEPLOYMENT.md](inference/DEPLOYMENT.md),
decyzje ADR-0015…0018. Pakiet `igw` nie importuje `wgc` ani `glu`.

### M-GW1: Inference Gateway MVP (API, auth, limity, kolejka, adapter runtime'u)
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M-INF0
- **Zakres:**
  - pakiet `igw` (FastAPI i uvicorn: extra `[node]` w `pyproject.toml`, wersje dopisane do `requirements.txt`, bo testy bramki działają też na dev machine);
  - `igw/node@0` (`node.yaml`) z walidacją;
  - endpointy `GET /healthz`, `/v1/health`, `/v1/capabilities`, `/v1/models`, `POST /v1/infer`, `GET /v1/metrics`
    zgodne z `igw/api@0`;
  - token Bearer (hashe w pliku, `igw token new|list|revoke`), allowlista IP klientów;
  - limity: body, `max_tokens`, kolejka;
  - kolejka FIFO na profil w pamięci, deduplikacja po `idempotency_key`;
  - adapter runtime'u `fake` (testy) i `openai_compat` (llama-server pod stałym adresem `127.0.0.1`, bez cyklu życia);
  - `model_fingerprint` z sha256 pliku, kwantyzacji, wersji runtime'u i parametrów;
  - TLS z plików certyfikatu;
  - logi bez treści promptów.
- **Akceptacja:**
  - testy `fastapi.testclient` bez sieci i GPU: każdy endpoint waliduje się schematem `igw/api@0`;
  - request z polem domenowym odrzucony (400);
  - brak lub zły token → 401;
  - IP spoza allowlisty → 403;
  - za duże body → 413;
  - pełna kolejka → 429;
  - fingerprint stabilny i niezależny od hosta;
  - `igw` nie importuje `wgc` ani `glu` (test importów).

### M-NODE: Wdrożenie węzła na Windows 11 Pro (RTX 3090)
- **Status:** planned · **Rola:** HUM + IMPL · **Zależy od:** M-GW1
- **Zakres:**
  - procedura z [DEPLOYMENT.md](inference/DEPLOYMENT.md) wykonana na sprzęcie: sterownik, llama.cpp CUDA (wersja
    przypięta), venv;
  - certyfikat z SAN `ai-node`, tokeny;
  - reguła Windows Firewall (TCP 8443, profil Private, `RemoteAddress` = dev machine);
  - nazwa hosta w DNS lub `hosts`;
  - autostart (Harmonogram zadań albo WinSW, decyzja z uzasadnieniem);
  - skrypty `deploy/node/*.ps1` (instalacja zadania, reguła firewall, generowanie certyfikatu);
  - jeden model `fast` ze stałym procesem runtime'u;
  - weryfikacja punktów oznaczonych „weryfikacja M-NODE”.
- **Akceptacja:**
  - po restarcie PC, bez logowania, `curl.exe --cacert … https://ai-node:8443/healthz` z dev machine zwraca `ok`;
  - z innego hosta LAN (spoza allowlisty) połączenie odrzucone;
  - runtime niedostępny spoza `127.0.0.1`;
  - DEPLOYMENT.md zaktualizowany do stanu faktycznego (bez „weryfikacji M-NODE”).

### M-E2E: Walking skeleton przez LAN + `glu doctor`
- **Status:** planned · **Rola:** IMPL + HUM (węzeł) · **Zależy od:** M2, M10, M-NODE
- **Zakres:**
  - **jedna reguła gry benchmarkowej** (zakaz 3.4) przechodzi całą drogę: `bench/minigame` → Stage 0 (M2) → TaskSpec
    `logic.rule.extract` (minimalny prompt, `decoding_schema`) → GLU → `self_hosted` → bramka na węźle przez LAN →
    walidacja L0/L1 → `accept()` do `kb/` w katalogu tymczasowym → Stage 1.5 (szablon Tier 0 `prohibition` → `LEG-`
    i jeden `TST-` illegal) → walidacja kontraktu;
  - premium jako `fake`;
  - **`glu doctor`** (kroki z [NODE.md §10](inference/NODE.md#diagnostyka));
  - nagranie odpowiedzi węzła do `replay`, żeby test CI przeszedł bez sieci;
  - provenance i `routing_decision` z pełnym śladem (endpoint i węzeł tylko w `.glu/`).
- **Akceptacja:**
  - test automatyczny na `replay` (CI, bez sieci) zielony;
  - ręczny przebieg przez LAN zapisany w handoffie (czasy, tokeny, fingerprint);
  - `glu doctor` wskazuje właściwy krok dla: złej nazwy hosta, wyłączonego węzła, złego tokenu, złego certyfikatu;
  - wyłączony węzeł → job `waiting_inference`, 0 wywołań premium;
  - `kb/` nie zawiera hosta.

### M-GW2: Scheduler, cykl życia modeli, telemetria GPU, `igw doctor`
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M-GW1, M-E2E
- **Zakres:**
  - supervisor procesów `llama-server` (start, health, restart, porty efemeryczne na `127.0.0.1`);
  - scheduler z [NODE.md §5](inference/NODE.md#scheduler): afinicja, `min_residency_s`, `max_wait_s`, LRU w
    `vram_budget_mb`, `pinned`, aliasy profili;
  - `503 model_loading` z `retry_after_s`;
  - priorytety `interactive` i `batch`;
  - ocena trybu routera llama.cpp jako wariantu adaptera;
  - telemetria GPU, VRAM i RAM (`nvidia-smi` ze stałymi argumentami albo NVML);
  - metryki ładowań i przełączeń;
  - `igw doctor`.
- **Akceptacja:**
  - testy na `fake` runtime z symulowanym czasem ładowania;
  - przeplatane requesty A/B/A nie powodują przełączenia na każdy request (limit przełączeń w teście);
  - brak zagłodzenia (`max_wait_s`);
  - budżet VRAM nigdy nie przekroczony;
  - testy właściwości schedulera (QUALITY §3a).

### M-INF: Wybór modeli i profili na węźle (benchmark przez bramkę)
- **Status:** planned · **Rola:** IMPL + HUM (węzeł RTX 3090) · **Zależy od:** M3, M-GW2
- **Zakres:**
  - 2–3 kandydatów na profile `fast`, `semantic` i `deep` (MoE z ekspertami w RAM);
  - pomiar przez `igw` na węźle:
    - jakość (scorer M3);
    - zgodność structured output z `decoding_schema`;
    - tok/s przy 1..N slotach;
    - VRAM i RAM;
    - czas ładowania z NVMe i z page cache;
    - koszt przełączeń w realnej mieszance jobów Stage 1;
  - decyzja: llama.cpp wystarcza albo M-VLLM;
  - przykładowe `node.yaml` i `profiles.yaml` w `docs/inference/`.
- **Akceptacja:** ADR z wyborem i liczbami (aktualizuje hipotezy ADR-0018 i NODE.md §4); progi QUALITY §5 dla
  profilu akceptującego `low`.

### M-VLLM: Runtime high-throughput (vLLM w WSL2)
- **Status:** optional · **Rola:** IMPL + HUM · **Zależy od:** M-INF (tylko jeśli pomiar wykaże wąskie gardło
  batchingu, równoległości lub przepustowości)
- **Zakres:**
  - WSL2 + CUDA + vLLM na węźle ([DEPLOYMENT §5](inference/DEPLOYMENT.md#wsl2));
  - adapter runtime'u w `igw`;
  - porównanie z llama.cpp na tej samej mieszance jobów.

  GLU się nie zmienia.

### M-GW3: Async jobs i SSE w bramce
- **Status:** optional · **Rola:** IMPL · **Zależy od:** M-GW2 (tylko jeśli joby `local_deep` przestają mieścić się
  w deadline synchronicznym)
- **Zakres:**
  - `POST /v1/jobs`, `GET /v1/jobs/{id}`, `DELETE /v1/jobs/{id}` (`job_status` z `igw/api@0`), stan w SQLite węzła
    (tylko stan operacyjny, bez wyników po odebraniu);
  - opcjonalnie SSE z postępem;
  - provider `self_hosted` korzysta z async dla profili `batch`.

## Faza 2: Stage 1 z modelami
### M14: Pakiet zadań Stage 1 (ekstrakcja reguł, pojęć, relacji, przypadków)
- **Status:** planned · **Rola:** ARCH (prompty) + IMPL · **Zależy od:** M13, M-INF
- **Zakres:** TaskSpec `logic.rule.extract`, `logic.concept.extract`, `logic.relations`, `logic.case.generate`,
  `logic.ambiguity.detect`; context buildery; zamrożenie `wgc/logic@1`.
- **Akceptacja:** build Stage 1 na `bench/minigame` przez węzeł self-hosted (albo `replay` nagrań) → scorer ≥ progów
  QUALITY §5; raport kosztu, routingu i `premium_delta`.

### M-BASE: Pomiar baseline kosztu obecnego workflow
- **Status:** planned · **Rola:** HUM + IMPL · **Zależy od:** M0 (korpus `bench/minigame` istnieje)
- **Kiedy:** jak najwcześniej, równolegle z M1–M10, a na pewno przed M14.
- **Zakres:** procedura z COST §1 na starym narzędziu: wywołania premium, tokeny premium, koszt premium, rozmiar
  kontekstu na wywołanie.
- **Akceptacja:** `B_logic`, `B_translate` w STATUS; metoda opisana tak, by dało się powtórzyć; od M12 każda zmiana
  routingu raportuje `premium_delta`.

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
- **Akceptacja:** gold digital (stan) dla gry benchmarkowej; snapshot round-trip (kanoniczny hash stabilny);
  testy właściwości (Hypothesis): generowane stany spełniają inwarianty (QUALITY §3a).

### M18: Akcje, legalność, zdarzenia
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M17
- **Zakres:** domknięcie `action`/`legality`/`event`, szablon Tier 0: `prohibition` → `LEG-`, walidacja `reason_code`;
  **werdykt legalności** `legal | illegal | blocked | unresolved` z `reasons` i `evidence` zamiast `then.accepted: bool`
  (DIGITALIZATION, Legality Model; zmiana `wgc/digital@0` + fixture'y).
- **Akceptacja:** gold akcji i legalności dla rozdziałów 3–5 gry benchmarkowej; brak wiedzy daje `unresolved`
  lub `blocked`, nigdy `illegal`; testy właściwości: akcja nielegalna nie zmienia stanu.

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
- **Akceptacja:** złote testy przechodzą na interpreterze; mutacje spec wykryte; build 1.5 na węźle self-hosted
  ≥ progów (multi-pass: ekstrakcja → weryfikator → analiza rozbieżności; premium tylko dla semantyki nierozstrzygniętej).

## Faza 4: interfejsy
### M22: MCP tylko do odczytu + konfiguracja bezpieczeństwa
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M16
- **Zakres:** serwer stdio, narzędzia odczytu z MCP.md, `mcp.yaml` (allowlisty, zakresy, redakcja logów).
- **Zakres (dodatkowo):** `inference_status` (widok GLU na endpointy; MCP nie zna tokenów węzła i nie łączy się z nim).
- **Akceptacja:** testy kontraktowe narzędzi bez Claude Desktop; próba wyjścia poza allowlistę odrzucona; test ręczny
  z Claude Desktop (stdio natywnie albo przez `wsl.exe`, zależnie od miejsca GLU).

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
- **Zakres:** `translate.segment` (profil `local_translate`, model wybrany pomiarem, może być inny niż dla logiki),
  kroki 1–5 weryfikacji (EDITORIAL-PUBLICATION), `ir_hash`/`glossary_hash`, punktowa aktualizacja po zmianie terminu,
  referencyjny przekład PL gry benchmarkowej.
- **Akceptacja:** mutacje przekładu wykryte (≥ progów); zmiana terminu unieważnia tylko segmenty z tym `CON-`.

### M27: Publikacja LaTeX
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M26
- **Zakres:** API makr semantycznych, generator stylu z `layout_spec`, `wgc publish build` (LuaLaTeX w WSL), słowniczek, pomoce do gry z `PROC-`.
- **Akceptacja:** PDF gry benchmarkowej; zmiana layoutu nie unieważnia przekładów ani Stage 1.

## Faza 6: pilotaż
### M28: Pilot na prawdziwej grze + porównanie z baseline
- **Status:** planned · **Rola:** HUM + IMPL · **Zależy od:** M21, M27, M-BASE
- **Zakres:** jedna gra (wybór właściciela), Stage 0–1.5 dla 1–2 rozdziałów, raport kosztu (premium według
  `premium_reason`, GPU węzła, czas) vs `B_*`.
- **Akceptacja:** premium ≤ 2× baseline; FN z audytu ≤ progu; decyzja o dalszym rozwoju w ADR.

### M-LEG: Importer `wgu/kb@1` (opcjonalny)
- **Status:** optional · **Rola:** IMPL · **Zależy od:** M3
- **Zakres:** jednokierunkowy import starej KB do `private/bench/` jako materiał porównawczy (np. GCACW-PL). Nie jest migracją gier.
