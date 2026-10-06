# GLU: wykonanie i orkiestracja

GLU kieruje pracę do wykonawców (kod deterministyczny, self-hosted LLM, premium LLM, człowiek), pilnuje cache,
przyrostowości, budżetu i metryk. **Nie posiada wiedzy o grze.** Knowledge Base (repo gry) pozostaje źródłem prawdy
(ADR-0004). Kontrakt stanu wykonania: `contracts/schemas/glu.schema.json` (`glu/exec@0`).
Self-hosted inference wykonuje osobny węzeł w LAN za Inference Gateway ([inference/NODE.md](inference/NODE.md)).
GLU widzi go wyłącznie przez providera `self_hosted` i nie zakłada localhost (ADR-0015, ADR-0016).

## 1. Model nie jest pamięcią projektu
```text
INPUT (rekordy, segmenty, hashe) → EXECUTOR (tier) → PROPOSED OUTPUT (blob) → VALIDATOR (WGC) → ACCEPTED STATE (kb/)
                                                       ↘ retry (z opisem błędów) / escalate / requires_human_interpretation
```
Nic, co nie przeszło walidacji WGC, nie trafia do `kb/`. Historia czatu nie jest stanem.

## 2. Pojęcia
| Pojęcie | Znaczenie | Gdzie żyje |
|---|---|---|
| **Project** | repo gry z `project.yaml` | git |
| **Stage** | etap pipeline'u (0, 1, 1.5, 2, 3) ze statusem z bramki | wyliczany (`wgc gate`) |
| **Build** | jedno zlecenie kompilacji: etap + zakres + polityka (routing, budżet, limit pytań) | `.glu/state.db` |
| **Job** | jednostka pracy: `TaskSpec` + wejścia + klucz cache. Idempotentny | `.glu/state.db` |
| **Attempt** | jedno wykonanie joba przez wykonawcę (tier, profil, tokeny, koszt, czas, wynik walidacji) | `.glu/state.db` + blob |
| **RoutingDecision** | dlaczego job trafił do danego tieru (sygnały, polityka, powody) | `.glu/state.db` |
| **Review** | przegląd premium lub ludzki wyniku albo przypadku spornego, przez `review_package` | `.glu/`; wynik → `kb/` |
| **Escalation** | przejście joba do wyższego tieru (z powodem) | stan joba + RoutingDecision |
| **Decision** | rozstrzygnięcie człowieka `HD-` (domena!) | `kb/decisions.yaml` |
| **Artifact** | zaakceptowany rekord albo wygenerowany plik (widok, LaTeX, engine kit) | `kb/`, `publication/`, `reports/` |
| **Endpoint** | logiczna nazwa bramki inferencji z konfiguracji GLU (np. `ai-node`), nie IP | `~/.config/glu/profiles.yaml`; w Attempt |
| **Session** | okres pracy interaktywnej: człowiek albo premium w Claude Desktop/Code przerabia kolejkę przeglądów i pytań | efekty w `kb/` i `.glu/` |

## 3. Cykl życia joba
```text
pending → ready → running ⇄ waiting_inference (węzeł niedostępny; bez zużycia prób)
                     ↓
                  proposed → validating ─┬→ accepted → done
   ↑                                     ├→ retry ──────────→ ready        (≤ N prób na tier)
   │                                     ├→ escalated → ready (wyższy tier)
   │                                     ├→ waiting_review → (pakiet premium/człowiek) → validating
   │                                     ├→ waiting_human  → (HD-) → validating
   │                                     └→ rejected / failed
   └──────── stale (zmiana wejścia) ← done / accepted
```
- **Cache hit** przy `ready` → od razu `accepted` (zero wywołań modelu).
- **Retry** dostaje listę błędów walidacji (schemat i domena) w prompcie. Po wyczerpaniu prób następuje eskalacja, a nie akceptacja.
- **Błąd dostępności providera** (sieć, TLS, timeout, ładowanie modelu, runtime) przenosi job do `waiting_inference`
  zgodnie z `build.policy.fallback` (domyślnie `queue`). Nie zużywa limitu prób jakościowych i **nie eskaluje** do premium,
  chyba że `allow_premium_fallback: true` (ADR-0017). Błąd auth lub TLS kończy build `failed` z diagnozą `glu doctor`.
- **Build** kończy się `done`, `waiting_inference` (czeka na węzeł), `waiting_review` (czeka kolejka premium),
  `waiting_human` (pytania) albo `failed`.
- Job store GLU (SQLite) jest **jedyną trwałą kolejką**. Bramka węzła trzyma kolejkę w pamięci, a restart po którejkolwiek
  stronie oznacza ponowne wysłanie idempotentnego requestu.

<a id="tabela-przejsc"></a>
**Tabela przejść (M8, ADR-0023).** Wiążąca jest tabela w kodzie: `glu/states.py` (`JOB_RULES`, `BUILD_RULES`).
Przejście spoza niej to wyjątek `IllegalTransition`, a stan rekordu się nie zmienia.

| Job: ze stanu | do stanu | Strażnik, efekt, parametry |
|---|---|---|
| `pending` | `ready` | |
| `ready` | `running` | efekt: `cache_hit: false` |
| `ready` | `accepted` | cache hit; efekt: `cache_hit: true`; parametr `accepted_records` |
| `running` | `waiting_inference`, `proposed`, `failed` | |
| `waiting_inference` | `running`, `failed` | |
| `waiting_inference` | `escalated` | strażnik: `policy.fallback.allow_premium_fallback: true` (ADR-0017) |
| `proposed` | `validating` | |
| `validating` | `accepted` | parametr `accepted_records` |
| `validating` | `retry`, `escalated`, `waiting_review`, `waiting_human`, `rejected`, `failed` | |
| `retry` | `ready` | |
| `escalated` | `ready` | strażnik i parametr `tier`: wyższy niż bieżący (`deterministic < local < premium < human`) |
| `waiting_review`, `waiting_human` | `validating` | |
| `accepted` | `done`, `stale` | |
| `done` | `stale` | |
| `stale` | `pending` | |
| każdy aktywny (`pending` … `waiting_human`, bez `accepted`, `done`, `stale`) | `cancelled` | |

Stany końcowe joba: `rejected`, `failed` i `cancelled`. Limit N prób na tier egzekwuje pętla structured output (M10).
Store udostępnia liczbę prób jakościowych, czyli Attemptów z `outcome ≠ unavailable` (`Store.quality_attempts`).

| Build: ze stanu | do stanu | Efekt, parametry |
|---|---|---|
| `planning` | `running` | |
| `running` | `waiting_inference`, `waiting_review`, `waiting_human` | |
| `waiting_inference`, `waiting_review`, `waiting_human` | `running` | |
| `running` | `done` | efekt: `finished_at`; parametr `metrics` |
| `planning`, `running`, `waiting_*` | `failed`, `cancelled` | efekt: `finished_at`; parametr `metrics` |

Stany końcowe buildu: `done`, `failed` i `cancelled`. Wznowienie po `failed` to nowy build. Stanu buildu nie wylicza
się ze stanów jobów, tylko ustawia go wykonawca (M9a, M10).

**Tier 0 (M9a, ADR-0025).** Wykonawca deterministyczny (`glu.exec`) prowadzi job ścieżką `pending → ready → running →
proposed → validating → accepted → done` i zapisuje jeden Attempt `tier: deterministic`. Wyjątek implementacji to
`running → failed` (Attempt `outcome: error`), a odrzucenie wyniku przez `wgc.kb.accept()` to `validating → failed`
(Attempt `outcome: rejected`). Awaria operacyjna akceptacji (zajęta blokada `kb/`, inwentarz zmieniony w trakcie
joba, nieudany zapis) i błąd programu (wyjątek w WGC albo w `validate` zadania) też kończą job `validating → failed`,
ale z Attemptem `outcome: error` (`error_class: runtime`) i osobnym powodem przejścia; nigdy jako `rejected`
(M-STAB1, ADR-0026). Build idzie `planning → running → done`, a gdy któryś job się nie udał,
`running → failed`. Planner i `glu build --stage --scope --dry-run`: [DATA-CONTRACTS §10](DATA-CONTRACTS.md#propozycje).
Końcowe wpisy joba (Attempt, przy `accepted` z `kb_receipt`, i ostatnie przejścia) zapisuje jedna transakcja
(`Store.finish_job`, M-STAB2). Wyjątek: `KBUnresolved` (partia, której wycofanie się nie dokończyło, ADR-0031)
nie zapisuje Attemptu ani przejścia. Job zostaje w `validating`, receipt zostaje, a build jest przerywany. Rozstrzyga
reconcile.

<a id="reconcile"></a>
**Reconcile (M-STAB2, ADR-0031).** `glu reconcile [--dry-run]` i krok startu `glu build` (nie `--dry-run`):
1. recovery przerwanej partii `kb/` (`wgc kb recover`, [DATA-CONTRACTS §10](DATA-CONTRACTS.md#recovery));
2. buildy niezakończone, których blokady żywotności `.glu/builds/<build>.lock` nikt nie trzyma (proces buildu
   zginął). Żywy build trzyma ją przez cały czas działania i reconcile go nie dotyka. Start buildu (reconcile,
   utworzenie buildu i jego blokady) idzie pod krótką blokadą `.glu/build.lock`; `glu reconcile` bierze tę samą
   blokadę.

| Job martwego buildu | Wynik |
|---|---|
| `validating`, receipt `.glu/kb-receipts/<job>.json` zgodny z `kb/` | Attempt `accepted` z `kb_receipt`, `validating → accepted → done` |
| `validating` bez receiptu albo z niezgodnym | Attempt `error` (`runtime`), `validating → failed`, powód `reconcile: …` |
| `running` | Attempt `error` (`runtime`), `running → failed` |
| `accepted` | `accepted → done` |
| `pending`, `ready`, `proposed` i inne aktywne | `cancelled` |

Potem build: `running → done`, gdy każdy job jest `done`, inaczej `→ failed`. Wszystkie przejścia są w tabeli wyżej:
reconcile nie dodaje krawędzi. Receipty zakończonych i nieznanych jobów są usuwane. Reconcile jest idempotentne,
a `--dry-run` niczego nie tworzy (ani `.glu/`, ani bazy, ani plików blokad). Wznowienie przerwanej pracy to nadal
nowy build.

<a id="receipt"></a>
**Diagnostyka receiptu (M-STAB3b, ADR-0033).** `glu receipt <job> [--json]` porównuje `kb_receipt` joba (albo
receipt nierozstrzygniętej akceptacji joba w `validating`) z bieżącym `kb/` i tylko raportuje: `match` (kod 0),
`differs`, `no_job`, `no_receipt`, `pending_batch` (kod 1), błąd operacyjny (kod 2). Bazę otwiera tylko do odczytu
(bez migracji), nie robi recovery ani reconcile, nie usuwa receiptów i nie tworzy plików blokad. Przy różnicy podaje
bieżące `prov.job` rekordu i czy to późniejszy job: różnica względem historycznego receiptu może wynikać z poprawnej
późniejszej zmiany `kb/` ([DATA-CONTRACTS §10](DATA-CONTRACTS.md#diagnostyka-receiptu)).

**Manifest joba i świeżość kontekstu (M-STAB3b, ADR-0033).** Planner bierze klucz joba z manifestu wywołania
(`wgc.manifest.build`). Wykonawca liczy manifest ponownie przed implementacją (dla zadań czytających `kb/` na jednej
migawce `kb/`, którą czyta też implementacja). Inny niż w planie kończy job `running → failed` (Attempt `error`,
powód „wejścia joba zmieniły się od planu”), zanim implementacja ruszy. `accept()` dostaje ten manifest
i odmawia zapisu, gdy kontekst zmienił się przed akceptacją (`KBContextStale`: Attempt `error`, `validating → failed`,
powód „kontekst kb/ zmienił się między wykonaniem a akceptacją”).

## 4. Pętla structured output
```text
MODEL → STRUCTURED OUTPUT (JSON Schema w żądaniu: guided decoding / response_format)
      → SCHEMA VALIDATION (wgc.contracts, schemat propozycji zadania)
      → DOMAIN VALIDATION (wgc.validate: referencje, kotwice, cytaty dosłowne, sygnały źródło↔IR, liczby)
      → ACCEPT / RETRY / ESCALATE
```
- Schemat propozycji jest okrojonym schematem rekordu: **bez `prov`, `risk` i `status`**. Te pola dopisują GLU i WGC (ADR-0014).
- Do modelu idzie `decoding_schema` zadania: płaski podzbiór JSON Schema zgodny z `capabilities.json_schema_subset`
  węzła (np. llama.cpp nie obsługuje `if/then/else` i pomija nieobsługiwane cechy po cichu). Pełny schemat i walidacja
  domenowa zawsze działają po stronie GLU i WGC.
- Wiedza kanoniczna nigdy nie pochodzi z niezwalidowanego wolnego tekstu. Pola `{text}` i glosy są dozwolone,
  ale wliczają się do ryzyka.

## 5. Wykonanie self-hosted a sesja premium
- **Self-hosted** GLU wykonuje setki jobów na węźle w LAN. Wysyła je uporządkowane według profilu (fale jako
  **wskazówka**), z równoległością nie większą niż `max_concurrency` z `/v1/models`. **Cyklem życia modeli w VRAM
  (ładowanie, rezydencja, LRU) zarządza bramka węzła**, bo widzi wszystkich klientów
  ([inference/NODE.md §5](inference/NODE.md#scheduler)).
- Self-hosted compute nie ma limitu finansowego, więc dozwolone są dodatkowe passy z jasnym celem (druga ekstrakcja,
  weryfikator, analiza rozbieżności, `local_deep`), jeśli zmniejszają eskalację premium (ADR-0017).
- **Premium jest bezstanowy.** Dostaje `review_package`: pytanie, minimalny fragment źródła, rekordy z otoczenia w grafie
  (sąsiedztwo k-hop po `refs` i relacjach, przycięte do budżetu tokenów), propozycje lokalne (także rozbieżne),
  uzasadnienie ryzyka i `answer_schema`. Pakiet jest samowystarczalny: recenzent nie potrzebuje historii ani
  dostępu do repo.
- Dwie drogi premium (ADR-0013): `anthropic` (API) i `desktop_pull` (Claude Desktop pobiera pakiet przez MCP).
  Odpowiedź przechodzi tę samą walidację.

## 6. Cache
Cache jest częścią architektury. **Niezmienione wejście = zero wywołań modelu.**

| Poziom | Klucz | Zawartość |
|---|---|---|
| L1: inferencja | sha256 z (rodzaj providera, `profile_fingerprint`, wiadomości, schemat dekodowania, parametry próbkowania) | surowa odpowiedź modelu |
| L2: wynik joba | sha256 z `cache_key` (niżej) | zaakceptowana propozycja + wynik walidacji |

`cache_key` (schemat `glu.schema.json#/$defs/cache_key`):
`task`, `task_version`, `prompt_version`, `output_schema`, `profile` + `profile_fingerprint`, `input_hash` (hash
manifestu wywołania bez kontekstu: projekcje wejść i dane autorytetu dokumentów źródłowych; projekcja segmentu ma
`text_hash` i `struct_hash`, więc inne granice komórek lub wierszy dają inny klucz, ADR-0032, ADR-0033),
`context_hash` (hash listy `context` manifestu: projekcje rekordów `kb/` czytanych jako kontekst), `dependency_state`
(hash projekcji zaakceptowanych rekordów nadrzędnych). Generacja `kb/` nie wchodzi do klucza (ADR-0033).

- **Tożsamość modelu raportuje węzeł**: `model_fingerprint` (`igw/api@0`: `/v1/models` i każdy `infer_result`) to
  hash pliku modelu, kwantyzacji, runtime'u i parametrów uruchomienia. GLU łączy go z tym, co sam wysyła:
  `profile_fingerprint` = hash(`model_fingerprint` raportowany przez węzeł, `node_profile`, parametry próbkowania i wyjścia z `profiles.yaml`). Żaden z nich **nie** obejmuje hosta, IP ani `node_id`:
  - podmiana modelu na węźle daje miss;
  - zmiana `temperature`, `seed`, `max_tokens` lub mapowania profilu w `profiles.yaml` daje miss;
  - wymiana węzła na inny z tym samym modelem zachowuje trafienia.

  Build zapisuje `inference_snapshot` (profil → `model_fingerprint` na starcie). Bez węzła trafienia L2 nadal działają.
- Węzeł **nie** ma cache wyników. Jego cache to pliki modeli, page cache i prefix cache runtime'u
  ([inference/NODE.md §6](inference/NODE.md#cache)). Odpowiedzialności się nie dublują.

- Dekodowanie lokalne deterministyczne (temperatura 0 + seed, gdy serwer to wspiera), żeby cache L1 był sensowny i testowalny.
- Bloby adresowane treścią: `.glu/blobs/sha256/<2>/<hash>`, indeks w SQLite. `glu cache gc` usuwa wpisy bez odwołań.
- Provider `replay` odtwarza nagrane odpowiedzi L1. Na tym opierają się testy GLU bez GPU (ADR-0008).

<a id="przyrostowosc"></a>
## 7. Przyrostowość (dependency-aware invalidation)
- **Graf zależności** budowany z danych KB: `anchors` (SEG → rekord), `derived_from`, `refs`, `relation.from/to`,
  `realizes`, `covers`, `from_case`, `concepts_used` (przekład → CON).
- **Projekcje semantyczne** (dostarcza WGC dla każdego rodzaju rekordu i konsumenta): hash obejmuje tylko pola
  istotne dla konsumenta. Przykłady:
  - Stage 1.5 zależy od struktury reguły (`nature`, `modality`, `bind`, `conditions`, `effects`, `limits`, `timing`,
    `layer`, relacje), a nie od glosy ani notatek;
  - przekład zależy od projekcji znaczeniowej reguł segmentu (modalność, warunki, limity, liczby), od terminów
    użytych pojęć i od konwencji Stage 2. Nie zależy od `realizes` w Stage 1.5.
- **Algorytm:** zmiana → przelicz hashe → oznacz bezpośrednich konsumentów jako `stale` → przelicz (cache często
  trafia) → jeśli projekcja wyniku się nie zmieniła, **zatrzymaj propagację** (early cutoff) → w przeciwnym razie
  idź dalej.
- **Kierunek:** krawędzie biegną tylko w dół etapów. Zmiana layoutu Stage 3 nie ma krawędzi do Stage 1.
- Zmiana jednej reguły nie powoduje pełnej analizy gry. Przelicza się tylko jej domknięcie w grafie.
- Świeżość da się wyliczyć bez `.glu/`, bo `seg_hash`, `prov.inputs_hash` i `prov.manifest` są w `kb/`
  (`wgc.manifest.check`, ADR-0033).

## 8. Budżety i bezpieczniki
- `build.policy.budget_premium_usd` i limit tokenów premium. Po przekroczeniu joby czekają (`waiting_review`) i nigdy
  nie są akceptowane lokalnie zamiast przeglądu.
- `build.policy.max_human_questions`: pytania ponad limit są odkładane do następnej sesji.
- Limity prób na tier, limit czasu joba, równoległość na profil (≤ `max_concurrency` węzła).
- **Polityka niedostępności** `build.policy.fallback`: `self_hosted_unavailable: queue | block | fail`,
  `allow_premium_fallback` (domyślnie `false`), `max_wait_seconds`. Budżet premium (≤ 2× baseline) dotyczy wyłącznie
  premium. Self-hosted compute ma tylko limity czasu i pojemności.

## 9. Metryki
Każdy Attempt zapisuje tokeny, koszt, czas GPU (raportowany przez węzeł), czas w kolejce i ładowania modelu,
endpoint, `node_id`, `model_fingerprint`, czas ścienny, wynik walidacji i klasę błędu. Każdy Build zapisuje agregaty.
Węzeł i endpoint żyją tylko w `.glu/`, nigdy w `kb/`.
Definicje i raporty: [COST.md](COST.md#obserwowalnosc).
