# Roadmapa

Każdy milestone to **jedna ograniczona sesja**: skończony zakres, testy, kryteria akceptacji, dokumentacja, handoff
([SESSION-PLAYBOOK.md](SESSION-PLAYBOOK.md)). Jeśli milestone nie mieści się w sesji, dzieli się go na `Mna`, `Mnb` (bez kropki)
(z wpisem w tym pliku), zamiast przeciągać. Rola wykonawcy jest zaleceniem ([SESSION-PLAYBOOK.md](SESSION-PLAYBOOK.md#role-modeli)).

Legenda roli: **ARCH** model architektoniczny, **IMPL** model implementacyjny, **HUM** wymaga człowieka.
Status: `done`, `next`, `planned`, `optional`.

<a id="kolejnosc"></a>
## Kolejność wykonania
Aktywną kolejność ustala ADR-0037 i [plan implementacji](DESKTOP-IMPLEMENTATION-PLAN.md).
Przebudowujemy istniejący kod. Premium działa przez ChatGPT lub Claude Desktop, bez API inferencji.

```text
M-DESK0 (done) -> M-DESK1 (done) -> M-DESK2 (next) -> M-DESK3 -> M-DESK4
 -> M-DESK5 (bramka jakości) -> M-DESK6a -> M-DESK6b -> M-DESK7 -> M-DESK9
                                                         -> M-DESK8 (optional)
```

**Milestone'y starszych faz o statusie `planned`/`optional` są odłożonym backlogiem, nie kolejką wykonania.**
Ich dawnych zakresów API, gatewaya, LAN i lokalnego routingu nie realizować. M-DESK9 przepisze przydatne
dalsze zadania według wyników pilota. Status `done` wcześniejszych etapów opisuje wykonane prace i pozostaje.
M-DESK8 nie blokuje M-DESK9. Q-11 jest otwarta i przechodzi do pilota M-DESK5, nie do ręcznego łatania 20 stron
legacy. M3 (gold) i M-BASE (pomiar) mają wczesny odpowiednik w M-DESK1/5; gateway nie jest zależnością gold.

## Aktywna przebudowa desktopowa

Szczegółowe zakresy, przypadki testowe i bramki: [plan](DESKTOP-IMPLEMENTATION-PLAN.md#7-etapy-i-kryteria-odbioru).
Każda sesja aktualizuje ten rejestr statusów; plan nie jest osobną kopią postępu.

### M-DESK0: Decyzja i plan przebudowy
- **Status:** done · **Rola:** ARCH · **Zależy od:** M-STAB3c
- **Wynik:** ADR-0037, plan implementacji, aktualizacja punktów wejścia i kolejności; kod bez zmian.

### M-DESK1: Minimalne kontrakty dokumentu i pakietu
- **Status:** done · **Rola:** ARCH + IMPL · **Zależy od:** M-DESK0
- **Zakres:** schematy pakietu, odpowiedzi, dowodów i rewizji; własny dwustronicowy przykład i fixture'y;
  DATA-CONTRACTS. Oddzielić zakres docelowy od kontekstu i poprawność strukturalną od zatwierdzenia.
- **Akceptacja:** kolumny, kontynuacja, ramka zakresu, transkrypcja obrazu mają reprezentację; negatywne
  fixture'y wykrywają brak dowodu i niespójny manifest; testy offline zielone.
- **Poza zakresem:** eksporter/importer, modele, GPU, migracja istniejącej gry.
- **Wynik:** `wgc/desktop@0` (package/response/document/revision, wspólne dowody), `wgc.desktop`
  (kontrola w pamięci i rekonstrukcja tekstu), własny [przykład CC0](../bench/desktop-two-page/README.md),
  fixture'y poprawne i negatywne, testy offline, DATA-CONTRACTS §11, ADR-0038.
  Walidacja nie nadaje zatwierdzenia; Q-11 i zmiany legacy pozostają. Handoff:
  [2026-10-06-M-DESK1](handoff/2026-10-06-M-DESK1.md).

### M-DESK2: Eksport pakietów do aplikacji desktopowej
- **Status:** next · **Rola:** IMPL + HUM · **Zależy od:** M-DESK1
- **Zakres:** deterministyczny pakiet z tekstem/renderami, kontekstem, schematem i instrukcją odpowiedzi.
- **Akceptacja:** zgodne hashe przy ponowieniu; ręczny round-trip pliku w co najmniej jednej aplikacji,
  możliwości drugiej opisane bez obietnic automatycznej integracji; bez API/sterowania GUI.
- **Wykonanie częściowe (2026-10-06):** ogólny eksporter `wgc.desktop_export`, jawne CLI `desktop export`,
  surowe glify/rendery i osobny kontekst, rzeczywiste hashe oraz kopia schematu, testy offline.
  [Pakiet i kroki ręcznej próby](DESKTOP-EXCHANGE.md) są gotowe. Schemat/hashe pakietu poprawne,
  ponowny eksport: siedem identycznych bajtowo plików (143563 bajty).
  Zapisany `mdesk2-chatgpt.json` (9770 bajtów) przeszedł JSON, schemat, wiązanie i `desktop.check`
  bez diagnostyk; oryginalne bajty zachowano. Metadane/dowód wskazują **Codex desktop** i bezpośredni
  zapis narzędziem plikowym; właściciel potwierdził **GPT 6.1 Sol, rozumowanie wysoki** w osobnych metadanych.
  Nie potwierdza to ręcznej wymiany w ChatGPT/Claude Desktop; oryginalna koperta nadal ma model `unknown`.
  M-DESK2 pozostaje `next`/partial, M-DESK3 nie rozpoczęto. Obie wymagane aplikacje nadal niesprawdzone;
  ograniczenia opisano na podstawie dokumentacji. Wynik strukturalny nie nadaje zatwierdzenia.
  Dodatkowo właściciel zatwierdził SPQR PDF 32 (edycja 5): pakiet z kontekstem 31/33 ma osiem plików,
  6806093 bajty; schemat/hashe i powtarzalność poprawne. Podgląd celu zachowany identycznie.
  Pakiet i instrukcja próby wyłącznie prywatne. Wynik SPQR sprawdzony 2026-10-07: JSON/schemat/wiązanie
  poprawne, `desktop.check` **23 błędy** (1 dowodów tabeli, 22 coverage). Odczyt tabeli/diagramu obiecujący,
  ale struktura wymaga ręcznej korekty. Dowód dotyczy Codex, model `gpt sol 6.1`, rozumowanie wysoki;
  ChatGPT/Claude Desktop nadal niesprawdzone. Oryginalne bajty i osiem assetów pakietu zachowane.
  Ostatni pełny zestaw dla tego kodu (2026-10-06): **806 passed, 1 skipped**, 291,11 s;
  bieżące testy kontraktów/eksportera/ciągłości: **160 passed**, 14,30 s
  (lokalny TMP/TEMP, nowy basetemp `spqr-response-review-20261007-1`;
  log `.glu/desktop-export-session/spqr-response-review-20261007-1/targeted.log`).
  Końcowa osobna ciągłość **95 passed**, 0,27 s; nowy basetemp `spqr-response-review-continuity-20261007-1`.
  [Bieżący handoff kontroli](handoff/2026-10-07-M-DESK2.md),
  [wcześniejszy eksport i przygotowanie](handoff/2026-10-06-M-DESK2.md).

### M-DESK3: Import i trwałe rewizje prywatnych artefaktów
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M-DESK2
- **Zakres:** import propozycji, diagnostyka, prywatny magazyn, eksport i odtworzenie.
- **Akceptacja:** stary/obcy pakiet odrzucony; powtórny import idempotentny; awaria zachowuje poprzedni wynik;
  utrata cache nie wymaga modelu. Brak zapisu do KB na tym etapie.

### M-DESK4: Podgląd, review i poprawki fragmentów
- **Status:** planned · **Rola:** IMPL + HUM · **Zależy od:** M-DESK3
- **Zakres:** porównanie renderu z blokami i tabelami, jawne zatwierdzanie i pakiet korekty obszaru.
- **Akceptacja:** poprawny fragment jest zachowany mimo innej luki; zależny zakres pozostaje zablokowany;
  tekst z obrazu może uzyskać zweryfikowany dowód bez udawania warstwy tekstowej.

### M-DESK5: Pilot jakości odczytu instrukcji
- **Status:** planned · **Rola:** HUM + ARCH · **Zależy od:** M-DESK4
- **Zakres:** 12–18 stron prywatnego korpusu, wcześniej ustalone oczekiwania i próbka kontrolna;
  raport pierwszego wyniku i korekt, czasu użytkownika i dostępnych metryk.
- **Akceptacja:** krytyczne elementy poprawne, brak cichych pominięć i dopowiedzeń, pokrycie rozliczone;
  decyzja kontynuować albo poprawić kontrakt. Nie zamykać Q-11 na podstawie samego JSON/schema validity.

### M-DESK6a: Ekstrakcja semantyczna z zatwierdzonego dokumentu
- **Status:** planned · **Rola:** ARCH + IMPL + HUM · **Zależy od:** M-DESK5
- **Zakres:** pakiet jednej sekcji z zależnościami, propozycje reguł/wyjątków/limitów i przypadków kontrolnych.
- **Akceptacja:** ślad reguły do dowodu tekstowego/wizualnego; przypadek pozytywny i negatywny sprawdzone
  względem źródła. Bez pełnej digitalizacji i bez bezpośredniego zapisu modelu do KB.

### M-DESK6b: Akceptacja KB i zmiana rewizji źródła
- **Status:** planned · **Rola:** ARCH + IMPL · **Zależy od:** M-DESK6a
- **Zakres:** integracja przez `accept()`, manifesty i ownership; dowody wizualne; Q-12/Q-16/Q-17 dla pilota.
- **Akceptacja:** odrzucenie starego pakietu i niepotwierdzonej kotwicy, kontrola zależnych rekordów po zmianie
  rewizji; konserwatywna blokada zakresu dopuszczalna przed pełnym grafem. Bez cichej migracji źródeł.

### M-DESK7: Kolejka pracy desktopowej w GLU
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M-DESK6b
- **Zakres:** powiązanie istniejącego job store z eksportem, oczekiwaniem, importem i review.
- **Akceptacja:** restart zachowuje pracę, duplikat odpowiedzi nie dubluje akceptacji; brak odpowiedzi pozostawia
  oczekiwanie bez wywołania API. Zmiany stanów/kontraktów wymagają fixture'ów i testów recovery.

### M-DESK8: Opcjonalny lokalny kontroler
- **Status:** optional · **Rola:** IMPL + HUM · **Zależy od:** M-DESK7
- **Zakres:** worker przez proces/pliki, niezależna ekstrakcja kontrolna, raport rozbieżności.
- **Akceptacja:** porównanie wykrytych błędów/fałszywych alarmów/czasu z wariantem bez workera;
  bez samodzielnej akceptacji; brak lokalnego modelu nie blokuje podstawowej pracy desktopowej.

### M-DESK9: Migracja i dalsza roadmapa
- **Status:** planned · **Rola:** ARCH + IMPL · **Zależy od:** M-DESK7
- **Zakres:** jawny diff i odwracalne przełączenie projektu; aktualizacja dalszych etapów M3–M28.
- **Akceptacja:** regresje legacy/Markdown, zachowane dowody i rewizje, udokumentowana migracja i rollback;
  decyzja o wycofaniu legacy oparta na pilocie, bez przywracania API.

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

### M-INF0a: Przegląd spójności dokumentacji i roadmapy po M-INF0
- **Status:** done · **Rola:** ARCH · **Zależy od:** M-INF0
- **Wynik:** audyt repo pod kątem założenia „local = localhost / WSL2”. Poprawki: brak `wsl.exe` w kryterium M22 i MCP.md,
  adapter runtime'u bramki nazwany `llama_server` (wewnętrzny dla `igw`, nie provider GLU), kryteria wyboru Windows
  natywnie vs WSL2 w M-INF, klasy `semantic_escalation` i `infrastructure_fallback` w telemetrii, rozdział profili
  logicznych od modeli fizycznych w INFERENCE-ROUTING. Brak zmian kontraktów i kodu.

### M1: Tożsamość, hashowanie i walidator referencji
- **Status:** done · **Rola:** IMPL · **Zależy od:** M0
- **Zakres:** `wgc/ids.py` (gramatyka, rejestr prefiksów, `kind` ↔ prefiks), `wgc/canonical.py` (kanoniczny JSON,
  sha256, projekcje semantyczne v0 dla `rule`, `concept`, `relation`, `segment`), `wgc/validate.py` (L0 + L1 + reguły
  provenance spoza schematu: istnienie segmentu kotwicy, zgodność `seg_hash`, `HD-` dla `human_decision` i accepted
  `INT-`), CLI `wgc validate`, domknięcie fixture'ów (zbiór bez wiszących referencji). Raport walidatora to lista
  **diagnostyk** `{code, severity, subject, message, affected}` (podstawa `wgc diagnose` i `wgc explain`).
- **Wynik:** moduły i CLI jak w zakresie (`python -m wgc validate`, skrypt `wgc`), fixture'y `valid/` zamknięte,
  `invalid/semantic/` z kodem w `# EXPECT:`, pliki YAML wielodokumentowe (ADR-0019), DATA-CONTRACTS §5 i §8.
  Handoff: [handoff/2026-10-05-M1.md](handoff/2026-10-05-M1.md).

Pierwotne M2 (Stage 0: inwentarz i ingest źródeł) podzielono przed pracą na M2a (inwentarz, Markdown, kontrakt)
i M2b (PDF), bo całość przekraczała rozmiar jednej sesji.

### M2a: Stage 0: inwentarz, polecenia `wgc source`, ingest Markdown
- **Status:** done · **Rola:** IMPL · **Zależy od:** M1
- **Zakres:** `wgc source init/scan/extract/verify`; ingest Markdown (gra benchmarkowa): segmentacja po numerach reguł,
  typy segmentów, `text_hash`, `file_hash`; tekst w `.glu/source/`, inwentarz commitowany (`bench/minigame/source/`).
  Kontrakt `source_document`: role `living_rules`, `community_interpretation` i domyślne pierwszeństwo według roli
  ([LOGIC-MODEL](LOGIC-MODEL.md#pierwszenstwo-zrodel)). Przeliczenie `text_hash` segmentów i `seg_hash` kotwic w fixture'ach.
- **Akceptacja:** `bench/minigame` → inwentarz z prawdziwymi hashami, fixture'y przeliczone i zgodne z ingestem,
  `wgc validate contracts/fixtures/valid` bez błędów; deterministyczność (dwa przebiegi = identyczne hashe i bajty
  inwentarza); `wgc source verify` wykrywa zmianę pliku i cache.
- **Wynik:** `wgc/source.py`, `wgc/ingest/` (rejestr ekstraktorów, `wgc.ingest.markdown@0`), `wgc source
  init/scan/extract/verify`, `bench/minigame/source/inventory.yaml` (31 segmentów), fixture'y z prawdziwymi hashami
  (16 segmentów, 34 kotwice), role i `seg_prefix` w `wgc/source@0`, `segment.parent` w `unresolved_ref`,
  DATA-CONTRACTS §9, ADR-0020. Handoff: [handoff/2026-10-05-M2a.md](handoff/2026-10-05-M2a.md).

### M2b: Stage 0: ingest PDF, flagi wizualne, render strony
- **Status:** done · **Rola:** IMPL · **Zależy od:** M2a
- **Zakres:** ekstraktor PDF (PyMuPDF albo biblioteka na licencji liberalnej, decyzja Q-10 w STATUS; nowa zależność
  w `requirements.txt` i `pyproject.toml`) podpięty do rejestru ekstraktorów z M2a: segmentacja po numerach reguł,
  `pages`, `bbox`, flagi wizualne (kolor zmian, przekreślenie), render strony do weryfikacji (`.glu/source/`).
- **Akceptacja:** test na PDF wygenerowanym w teście z tekstu własnego (bez sieci, bez plików wydawców); ten sam tekst
  w Markdown i PDF daje te same `text_hash` segmentów typu `rule`; flagi wizualne wykryte na przygotowanych stronach.
- **Wynik:**
  - ekstraktor `wgc.ingest.pdf@0` (`wgc/ingest/pdf.py`) na pdfplumber/pdfminer.six, z polami `pages`, `bbox`
    i `visual_flags` (`changed_color`, `strikethrough`);
  - `wgc source render` (pypdfium2) zapisuje strony do `.glu/source/<SRC-id>/pages/`;
  - writer PDF do testów `tests/pdfgen.py`;
  - zgodność z Markdown: PDF gry benchmarkowej daje te same segmenty i `text_hash` (także nagłówki i tabela);
  - DATA-CONTRACTS §9, ADR-0021 (Q-10).

  Handoff: [handoff/2026-10-05-M2b.md](handoff/2026-10-05-M2b.md).

### M3: Złoty model logiki gry benchmarkowej + scorer
- **Status:** planned · **Rola:** ARCH + HUM (przegląd) · **Zależy od:** M2a
- **Zakres:** `bench/minigame/gold/logic.yaml` (wszystkie reguły 1.1–7.2, pojęcia, relacje, tabela, procedura
  sekwencji, AMB-001, przypadki dla każdej polaryzacji); `wgc bench score logic` (metryki z QUALITY §2).
- **Akceptacja:** gold przechodzi `wgc validate` bez ostrzeżeń; scorer daje 100% dla gold i < 100% dla 3 ręcznych zniekształceń.

### M4: Benchmark mutacyjny
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M3
- **Zakres:** operatory z QUALITY §3 dla IR (`wgc bench mutate`), harness wykrycia (kto wykrył: L1, L2, ryzyko), raport.
- **Akceptacja:** każdy operator generuje mutację gold; raport tabelaryczny; test regresji harnessu.

### M5: Walidator L2 (provenance, cytaty, sygnały źródło↔IR)
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M2a, M4
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
- **Status:** done · **Rola:** IMPL · **Zależy od:** M1
- **Zakres:** `glu.store` (SQLite: build, job, attempt, routing_decision; migracje schematu bazy), przejścia stanów
  z GLU §3 (nielegalne przejście = wyjątek), `glu status`.
- **Akceptacja:** testy przejść (legalne i nielegalne), trwałość po restarcie, eksport rekordów zgodny z `glu/exec@0`.

Pierwotne M9 (TaskSpec, wykonawca deterministyczny, planner buildu) podzielono przed pracą na M9a i M9b, bo całość
przekraczała rozmiar jednej sesji. Relacje warstwy scenariusza przeniesiono do M14: wyprowadza się je z rekordów `R-`
(np. `REL-003` z `R-7.1` i `R-5.2`), a te powstają dopiero w M14.

### M9a: TaskSpec, `accept()`, wykonawca Tier 0, `glu build`, parse tabel
- **Status:** done · **Rola:** ARCH (kontrakt) + IMPL · **Zależy od:** M2a, M8
- **Zakres:** interfejs `TaskSpec` (ARCHITECTURE §2, z `decoding_schema`) i rejestr zadań WGC; format propozycji;
  `wgc.kb.accept()` (provenance nadawana deterministycznie, walidacja w pamięci przed zapisem, idempotencja, konflikty);
  wykonawca Tier 0; planner i `glu build --stage --scope --dry-run`; zadanie `wgc.tables.parse@0` (z separatorem
  komórek tabeli w cache tekstu Stage 0). Sprawdzanie bramek przez planner dochodzi w M12 (po M7). Dzięki temu M9a nie
  czeka na M3–M7, a walking skeleton (M-E2E) powstaje wcześnie.
- **Akceptacja:** build Tier 0 na `bench/minigame` daje rekordy przechodzące walidację; ponowny build bez zmian wejścia
  nie zmienia `kb/`; `accept()` jedyną drogą zapisu do `kb/`; dry-run niczego nie zapisuje.
- **Wynik:**
  - `wgc/tasks.py` (`TaskSpec`, rejestr, zakresy `all|chapter:N|segment:SEG-…`);
  - `wgc/kb.py` (`Workspace`, `accept()`, deterministyczny zapis `kb/logic/<rodzaj>.yaml`);
  - `wgc.validate.validate_documents`;
  - zadanie `wgc.tables.parse@0` (`wgc/tables.py`);
  - separator komórek `\t` w cache tekstu Stage 0 bez zmiany `text_hash` (ADR-0024);
  - `glu/planner.py`, `glu/exec.py` (wykonawca Tier 0) i `glu build --stage --scope --dry-run`;
  - DATA-CONTRACTS §10, ADR-0024, ADR-0025.

  Na `bench/minigame` build daje `TAB-4.3`. Handoff: [handoff/2026-10-05-M9a.md](handoff/2026-10-05-M9a.md).

Po M9a niezależny przegląd ([reviews/2026-10-05-przeglad-po-M9a.md](reviews/2026-10-05-przeglad-po-M9a.md)) wykazał
utratę danych przy zapisie KB i przy dwóch równoległych akceptacjach. Przed M9b wstawiono etap naprawczy M-STAB1,
a pozostałe naprawy granicy akceptacji zaplanowano jako M-STAB2 i M-STAB3 przed M10.

### M-STAB1: Stabilizacja po M9a, etap 1: bezpieczny zapis KB, jeden pisarz, typy propozycji
- **Status:** done · **Rola:** IMPL · **Zależy od:** M9a
- **Zakres:** ustalenia F01 (tylko pojedynczy plik), F02 i F08 przeglądu:
  - atomowa podmiana pliku KB (plik tymczasowy w tym samym katalogu, `fsync`, `os.replace`, sprzątanie, ponowienia
    na Windows) bez zapisu w miejscu;
  - blokada pisarza projektu między procesami i wątkami wokół całego odczytu, merge'a, walidacji i zapisu
    w `accept()`, z limitem czasu;
  - przekazany `Workspace` nie nadpisuje nowszego wyniku: świeży odczyt `kb/` pod blokadą i kontrola odcisku
    inwentarza;
  - typy i schemat propozycji przed funkcjami domenowymi;
  - rozdzielenie odrzucenia danych, awarii I/O i błędu programu w `accept()` i wykonawcy Tier 0.
- **Akceptacja:**
  - awaria przed podmianą zachowuje stare bajty;
  - dwie akceptacje (wątki i procesy) nie gubią rekordów;
  - `id=[]`, `quote=123` i błędny `span` dają diagnostykę bez zapisu;
  - rebuild idempotentny, dry-run bez zapisu;
  - `python -m pytest` zielone.
- **Poza zakresem:** commit partii plików i recovery (M-STAB2), hashe, manifest, projekcje i kontrakt propozycji
  (M-STAB3), decyzje Q-13, Q-14 i Q-15.
- **Wynik:**
  - `wgc/fsio.py` (`atomic_write`, `exclusive`);
  - `wgc/kb.py`: `lock()`, `KBBusy`, `KBStale`, `KBWriteError`, kontrole typów i schematu przed domeną;
  - `glu/exec.py`: Attempt `error` dla awarii i błędu programu;
  - `tests/test_kb_safety.py`;
  - ADR-0026 i DATA-CONTRACTS §10.

  Handoff: [handoff/2026-10-05-M-STAB1.md](handoff/2026-10-05-M-STAB1.md).

### M9b: Harvest terminów (Tier 0)
- **Status:** done · **Rola:** IMPL · **Zależy od:** M9a, M-STAB1
- **Zakres:** zadanie `wgc.terms.harvest@0`: pojęcia `concept` tylko dla wzorców o pewnej kategorii (np. `NdM` → `die`,
  `Scenario: X` → `scenario`, pozycje listy sekwencji `… Phase` → `phase`), z kotwicą i cytatem; pozostałe terminy nie
  trafiają do `kb/` (kategorię ustala M14).
- **Akceptacja:** build Tier 0 na `bench/minigame` daje pojęcia przechodzące walidację; brak zgadywanych kategorii.
- **Wynik:**
  - `wgc/terms.py` (`wgc.terms.harvest@0` w rejestrze `wgc.tasks`): wzorce `die`, `scenario`, `phase`, job na
    dokument niezależny od zakresu, `validate` odrzucający inne kategorie i kotwice bez cytatu;
  - reguła ID pojęć (`CON-<klucz>` dla głównej instrukcji, `CON-<klucz SRC>:<klucz>` dla innych dokumentów)
    w DATA-CONTRACTS §10 i ADR-0030;
  - `tests/test_terms.py`.

  Na `bench/minigame` build daje `TAB-4.3` i 6 pojęć: 4 fazy, `CON-d6`, `CON-scn.the_ford`. Handoff:
  [handoff/2026-10-05-M9b.md](handoff/2026-10-05-M9b.md).

### M-STAB2: Stabilizacja po M9a, etap 2: commit partii KB i recovery
- **Status:** done · **Rola:** ARCH (protokół) + IMPL · **Zależy od:** M-STAB1
- **Zakres:** ustalenia F01 (partia plików) i F04 przeglądu, decyzje N01 i N04:
  - commit całej partii plików `kb/` jednej akceptacji: manifest partii (np. w `.glu/`), podmiana plików i jawny
    znacznik zatwierdzenia; po przerwaniu albo dokończenie, albo wycofanie do poprzedniej wersji, nigdy częściowa
    `kb/` uznana za poprawną;
  - receipt akceptacji (generacja `kb/`) zapisywany razem z Attemptem; końcowe wpisy store (`add_attempt`
    i przejścia) w jednej transakcji;
  - reconcile/recovery: polecenie albo krok startu buildu, który znajduje joby w `validating`/`running`
    i uzgadnia je z `kb/` (KB pozostaje prawdą także po utracie `.glu/`, ADR-0004).
- **Akceptacja:** testy awarii między podmianami plików partii i po zapisie KB a przed zapisem Attemptu; recovery
  przywraca spójny stan bez ręcznej edycji; `kb/` nadal w YAML/git.
- **Poza zakresem:** rozproszona transakcja KB+SQLite, przeniesienie KB do bazy (ADR-0004).
- **Wynik (ADR-0031):**
  - `wgc/fsbatch.py`: partia ≥ 2 plików z dziennikiem wycofania w `kb/.wgc-batch/` (kopie, manifest `prepared`,
    podmiany, znacznik `committed`). Awaria w żywym procesie od razu wycofuje partię. Dziennik leży w `kb/`, więc
    utrata `.glu/` go nie ukrywa;
  - `wgc kb recover [--dry-run]`: dokończenie albo wycofanie z hashy plików, idempotentne. `accept()` robi recovery
    pod blokadą przed odczytem `kb/`. `wgc validate` zgłasza `kb_batch_pending`;
  - receipt akceptacji (`generation`, `records`) w `.glu/kb-receipts/<job>.json` przed zapisem plików i w Attempcie
    jako `kb_receipt` (zmiana addytywna `glu/exec@0`);
  - `Store.finish_job`: Attempt i ostatnie przejścia joba w jednej transakcji;
  - `glu reconcile [--dry-run]` i krok startu `glu build`: blokada żywotności buildu `.glu/builds/<build>.lock`,
    uzgodnienie jobów martwych buildów z `kb/` bez nowych krawędzi tabeli przejść;
  - testy `tests/test_kb_batch.py` i `tests/test_glu_reconcile.py`, w tym procesy potomne kończone `os._exit` między
    podmianami partii i po zapisie `kb/` przed Attemptem. Test luki partii w `tests/test_kb_safety.py` zamieniony na
    test gwarancji.

  Handoff: [handoff/2026-10-05-M-STAB2.md](handoff/2026-10-05-M-STAB2.md).

### Podział M-STAB3 (decyzja właściciela, 2026-10-06)
Zakres etapu 3 stabilizacji (ustalenia F03, F05, F06, F07 i F11 przeglądu, decyzje N03, N05, N06, N07 i N10) jest za
duży na jedną sesję, więc dzieli się na trzy milestone'y wykonywane po kolei przed M10.

### M-STAB3a: Stabilizacja po M9a, etap 3a: hashe strukturalne
- **Status:** done · **Rola:** ARCH + IMPL · **Zależy od:** M-STAB2
- **Zakres:** ustalenie F03 przeglądu, decyzja N03: obok znormalizowanego `text_hash` wersjonowany hash struktury
  tabeli albo artefaktu ekstrakcji, używany przez parser, planner, provenance i verify; zastąpienie ADR-0024; nowa
  wersja ekstraktora albo formatu i jawna regeneracja wcześniejszych artefaktów.
- **Akceptacja:** test zmiany granic komórek bez zmiany `text_hash` (wykryta przez verify, planner i provenance);
  `python -m pytest` zielone.
- **Poza zakresem:** manifest wejść i projekcje (M-STAB3b), kontrakt propozycji (M-STAB3c), trwałe ID (F10).
- **Wynik (ADR-0032, zastępuje ADR-0024):**
  - `struct_hash` segmentu: `content_hash({format: wgc/struct@0, lines: structure(tekst)})`, czyli wiersze i komórki
    tekstu (`wgc.canonical.structure`). Pole w `wgc/source@0` (addytywne);
  - projekcja `logic` segmentu ma `struct_hash` (`wgc/projection@1`): zmienia się klucz joba i `prov.inputs_hash`,
    a `seg_hash` kotwic (`text_hash`) zostaje;
  - `Workspace.text` sprawdza oba hashe i wymaga `struct_hash` (planner, parsery, cytaty kotwic);
  - `wgc.tables.parse` i `wgc.terms.harvest` czytają tekst tylko przez `structure`;
  - `verify`: `segment_struct_mismatch`, `struct_hash_missing`, `cache_mismatch` także dla struktury;
  - ekstraktory `wgc.ingest.markdown@1` i `wgc.ingest.pdf@1`. Inwentarz `@0` wymaga `wgc source extract` (jawna
    regeneracja); inwentarz gry benchmarkowej i fixture `source.minigame.yaml` wygenerowane ponownie;
  - testy `tests/test_struct_hash.py` (F03 w cache i w źródle, granica wiersza w liście faz, regeneracja `@0`).

### M-STAB3b: Stabilizacja po M9a, etap 3b: manifest wejść i projekcje
- **Status:** done · **Rola:** ARCH + IMPL · **Zależy od:** M-STAB3a
- **Zakres:** ustalenia F05 i F06, decyzje N05 i N06:
  - **manifest wejść wywołania:** task/version, projekcja/version, wejścia i kontekst z hashami, autorytet źródeł;
    osobno dowody rekordu (`prov`). Generacja `kb/` dla zadań czytających rekordy KB (liczona już przez
    `wgc.kb.generation`, ADR-0031);
  - **projekcje:** treść nieformalizowana przy `formalization: none|partial`, definicje predykatów, projekcje dla
    rodzajów używanych w M10–M14, podbicie wersji;
  - **diagnostyka receiptu (decyzja właściciela, 2026-10-06):** polecenie porównujące receipt (`kb_receipt`)
    wskazanego joba z bieżącym `kb/`, tylko raport, bez automatycznej naprawy. Różnica nie oznacza sama w sobie
    uszkodzenia, bo `kb/` mogło później zostać poprawnie zmienione. Ma być gotowe przed M10.
- **Akceptacja:** testy zmiany treści nieformalizowanej i zmiany kontekstu (generacja `kb/`); polecenie diagnostyczne
  z testem zgodnego receiptu, różnicy i braku joba; `python -m pytest` zielone.
- **Poza zakresem:** kontrakt propozycji (M-STAB3c), cache (M11), graf zależności (M13).
- **Wynik (ADR-0033, ADR-0034):**
  - manifest wywołania `wgc/manifest@0` (`wgc.manifest.build`): zadanie i wersja, wersja projekcji, wejścia, dane
    autorytetu dokumentów źródłowych i kontekst `kb/`, każde z hashem. Jedna definicja dla klucza joba (planner,
    ponownie wykonawca) i `prov.manifest` (w `kb/`, więc zależności przetrwają utratę `.glu/`; `wgc.manifest.check`);
  - `prov.inputs_hash` to hash dowodów rekordu (kotwice, `derived_from`); dowód spoza manifestu jest odrzucany;
  - `TaskSpec`: `semantic_projection` dla jednego wejścia, nowe `authority_selector` (harvest: każdy dokument
    `rules`) i `context_selector`; bez `projections` i `input_hash`;
  - świeżość kontekstu: migawka `kb/` (`wgc.kb.read_snapshot`, `Workspace.pinned`) dla manifestu i implementacji,
    generacja jako token porównania w `accept()`, `KBContextStale`; manifest wykonania różny od planu kończy job;
  - projekcje `wgc/projection@2`: treść nieformalizowana reguł `none`/`partial`, definicja i `defined_by` predykatu
    w `digital`, projekcje `source_document`, `table`, `procedure`, `ambiguity`, `interpretation`, `case`, `change`,
    `legality`, `test`; bez zapasów (`ProjectionError`);
  - `glu receipt <job> [--json]`: porównanie `kb_receipt` z `kb/` tylko do odczytu (`Store(read_only=True)`,
    `wgc.kb.compare_receipt`), statusy `match`, `differs`, `no_job`, `no_receipt`, `pending_batch`;
  - kontrakt: `$defs/manifest` i `provenance.manifest` w `common.schema.json` (addytywnie), fixture'y;
  - testy `tests/test_manifest.py`, `tests/test_projections.py`, `tests/test_glu_receipt.py`.

### M-STAB3c: Stabilizacja po M9a, etap 3c: kontrakt propozycji, ownership, wdrożenie ADR-0027
- **Status:** done · **Rola:** ARCH + IMPL · **Zależy od:** M-STAB3b
- **Zakres:** ustalenia F07 i F11, decyzje N07 i N10:
  - **kontrakt propozycji i statusów:** `wgc/proposal@0` (envelope), dispatch kontraktu etapu, lifecycle oddzielony
    od rozstrzygnięcia niejasności;
  - **ownership** `task + zakres wejść` z manifestem outputów;
  - **wdrożenie ADR-0027:** lista ról kanonicznych dla automatycznej akceptacji (`community_interpretation`,
    `prior_translation` i `other` odrzucane, Q-13); niepotwierdzona kotwica zawsze odrzuca, `llm_inference` tylko
    z deklaracją zadania (Q-14).
- **Akceptacja:** testy zmiany roli źródła (każda rola) i zniknięcia jednego outputu; kontrakt propozycji
  z fixture'ami i DATA-CONTRACTS; `python -m pytest` zielone.
- **Poza zakresem:** pełny graf zależności i przyrostowy rebuild (M13), cache (M11), trwałe ID i mapa przenumerowań
  (F10, osobna decyzja przed pierwszą regeneracją zmienionych źródeł). Q-12, Q-16 i Q-17 pozostają otwarte (decyzja
  właściciela, 2026-10-06).
- **Wynik (ADR-0035):**
  - `wgc/proposal@0` jako envelope wyniku zadania; GLU przekazuje go do `accept()`, które waliduje rekord względem
    kontraktu etapu (`logic` lub `digital`). Fixture'y poprawne i niepoprawne oraz testy dispatchu;
  - `AMB-`: `status` lifecycle i odrębne `resolution`; projekcja `wgc/projection@3` obejmuje `resolution`;
  - `prov.owner` = rodzina taska i logiczny zakres wejść; `wgc/outputs@0` w `kb/outputs/` ma aktywne ID, ich hashe
    i tombstones wycofanych ID. Rekordy i manifest są jedną partią, receipt zapisuje `retired`. Harvest uzgadnia
    także pusty output, jeśli dokument nadal istnieje;
  - ADR-0027: jawna lista ról kanonicznych; `community_interpretation`, `prior_translation`, `other` odrzucane;
    błędna kotwica zawsze odrzucana; `llm_inference` tylko z `TaskSpec.allow_llm_inference`;
  - testy każdej roli, zniknięcia jednego i ostatniego outputu, konfliktu ownerów, ręcznej zmiany, kontraktu,
    etapu i lifecycle.

### M10: Providerzy fake/replay/self_hosted + pętla structured output
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M9a, M-STAB3c (kontrakt `igw/api@0` z M-INF0)
- **Odłożone przez ADR-0037:** poniższy zakres jest historyczny; nie implementować API. Zastępuje go aktywny plan M-DESK.
- **Zakres:**
  - `glu.providers` z interfejsem INFERENCE-ROUTING §3: `generate`, `embed?`, `health`, `capabilities`, `models`
    i typowane błędy;
  - **`self_hosted`**: klient `igw/api@0` przez HTTPS z `ca_file` i tokenem ze zmiennej środowiskowej; nazwa hosta
    z konfiguracji, nigdy IP na sztywno; klient HTTP `httpx` (dopisany do `requirements.txt`, transport w pamięci w testach);
  - `glu/profiles@0` (`profiles.yaml`: endpointy, profile, `fallback`);
  - wykonawca self-hosted;
  - pętla schemat → domena → accept/retry/escalate z feedbackiem błędów; odrzucona kotwica wraca do modelu jako
    błąd do poprawy, bez obniżenia do `llm_inference` (ADR-0027);
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
  i `premium_reason`, lokalny multi-pass (`local_deep` jako pass naprawczy i przygotowanie diffu, bez prawa
  akceptacji, ADR-0028), audyt próbkowy, budżety,
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
  - adaptery runtime'u **wewnętrzne dla `igw`** (nie providery GLU): `fake` (testy) i `llama_server` (protokół
    OpenAI-compatible, stały adres `127.0.0.1`, bez cyklu życia). GLU nie zna ich portów;
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
- **Status:** planned · **Rola:** IMPL + HUM (węzeł) · **Zależy od:** M2a, M10, M-NODE
- **Zakres:**
  - **jedna reguła gry benchmarkowej** (zakaz 3.4) przechodzi całą drogę: `bench/minigame` → Stage 0 (M2a) → TaskSpec
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
  - **weryfikacja wyboru runtime'u** (ADR-0018 to hipoteza MVP, nie dogmat): Windows natywnie vs WSL2 według kryteriów:
    structured output, wydajność, stabilność, CUDA, ładowanie modeli, start usługi po restarcie, wdrożenie przez sieć,
    utrzymanie;
  - decyzja: llama.cpp natywnie wystarcza albo M-VLLM (WSL2);
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
  `logic.ambiguity.detect`; context buildery; deterministyczne relacje warstwy scenariusza
  (`wgc.relations.scenario_layer@0`, przeniesione z M9); zamrożenie `wgc/logic@1`.
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
- **Odłożone przez ADR-0037:** poniższy zakres jest historyczny; nie implementować API. Zastępuje go aktywny plan M-DESK.
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
  z Claude Desktop: `Claude Desktop → MCP (stdio) → GLU`. GLU działa natywnie na Windows (ADR-0022); środowisko nie jest
  częścią kontraktu, kryterium nie wymaga `wsl.exe`.

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
- **Zakres:** `translate.segment` pisany przez premium (profil `premium_translate`, ADR-0029), kroki 0–5 przekładu
  i weryfikacji (EDITORIAL-PUBLICATION), nowa wartość `premium_reason` dla zadania z premium jako tierem podstawowym
  (zmiana addytywna `glu/exec@0`), `ir_hash`/`glossary_hash`, punktowa aktualizacja po zmianie terminu, referencyjny
  przekład PL gry benchmarkowej.
- **Akceptacja:** mutacje przekładu wykryte (≥ progów); zmiana terminu unieważnia tylko segmenty z tym `CON-`;
  ślepe porównanie kilku stron przekładu nowego i obecnego workflow `wgu`, ocenione przez właściciela; koszt premium
  Stage 3 względem `B_translate`.

### M27: Publikacja LaTeX
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M26
- **Zakres:** API makr semantycznych, generator stylu z `layout_spec`, `wgc publish build` (LuaLaTeX w WSL), słowniczek, pomoce do gry z `PROC-`.
- **Akceptacja:** PDF gry benchmarkowej; zmiana layoutu nie unieważnia przekładów ani Stage 1.

## Faza 6: pilotaż
### M28: Pilot na prawdziwej grze + porównanie z baseline
- **Status:** planned · **Rola:** HUM + IMPL · **Zależy od:** M21, M27, M-BASE, M2b
- **Zakres:** jedna gra (wybór właściciela), Stage 0–1.5 dla 1–2 rozdziałów, raport kosztu (premium według
  `premium_reason`, GPU węzła, czas) vs `B_*`.
- **Akceptacja:** premium ≤ 2× baseline; FN z audytu ≤ progu; decyzja o dalszym rozwoju w ADR.

### M-LEG: Importer `wgu/kb@1` (opcjonalny)
- **Status:** optional · **Rola:** IMPL · **Zależy od:** M3
- **Zakres:** jednokierunkowy import starej KB do `private/bench/` jako materiał porównawczy (np. GCACW-PL). Nie jest migracją gier.
