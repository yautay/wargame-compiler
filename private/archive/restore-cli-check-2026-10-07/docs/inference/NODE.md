# Self-hosted inference: węzeł, Inference Gateway, profile, scheduler

Decyzje: [ADR-0015](../adr/ADR-0015-self-hosted-inference-wezel-lan.md) (węzeł w LAN),
[ADR-0016](../adr/ADR-0016-inference-gateway-i-protokol.md) (bramka i protokół),
[ADR-0017](../adr/ADR-0017-niedostepnosc-wezla-bez-premium-fallback.md) (niedostępność i premium),
[ADR-0018](../adr/ADR-0018-runtime-mvp-llama-cpp-windows.md) (runtime). Wdrożenie: [DEPLOYMENT.md](DEPLOYMENT.md).
Kontrakt: `contracts/schemas/inference.schema.json` (`igw/api@0`), przykład: `contracts/fixtures/valid/igw.api.yaml`.

<a id="definicja"></a>
## 1. Definicja: „local” = self-hosted
**Local** w tym projekcie znaczy **self-hosted**: modele działają na naszej infrastrukturze i pod naszą kontrolą.
Nie znaczy „localhost”. Tier `local` i profile `local_*` obejmują każdy model za Inference Gateway. Bramka może
działać na węźle w LAN (docelowo), na localhost, w WSL albo na Linuksie. GLU tego nie odróżnia.

<a id="architektura"></a>
## 2. Architektura

```text
DEV MACHINE (Windows; bez GPU)                          AI NODE (Windows 11 Pro; RTX 3090 24 GB; 128 GB RAM)
┌─────────────────────────────────────────┐            ┌───────────────────────────────────────────────┐
│ Claude Desktop                           │            │ igw: Inference Gateway  (HTTPS :8443, IF LAN)  │
│   ↓ MCP (stdio; adapter, zero logiki)    │            │   auth · limity · walidacja requestu           │
│ GLU core                                 │            │   kolejki per profil · scheduler · lifecycle   │
│   job store (SQLite) = trwała kolejka     │  HTTPS     │   health · capabilities · metrics              │
│   routing · cache L1/L2 · fallback policy │  + token   │        ↓ runtime adapter (OpenAI-compatible)   │
│   ↓                                      │ ─────────► │ llama-server ×N (127.0.0.1, jeden na model)    │
│ Provider abstraction                     │ igw/api@0  │        ↓                                       │
│   fake · replay · self_hosted · anthropic│            │ VRAM: modele w GPU · RAM: page cache GGUF,     │
│   ↑ TaskSpec / validate / accept         │            │ offload ekspertów MoE · CPU                    │
│ WGC (domena; nie zna sieci ani GPU)      │            └───────────────────────────────────────────────┘
│ repo gry: kb/ (źródło prawdy), .glu/     │             węzeł = wymienialny worker; nie zna WGC, nie trzyma
└─────────────────────────────────────────┘             KB, cache wyników, promptów ani tekstu źródeł
```

| Warstwa | Wie o | Nie wie o |
|---|---|---|
| WGC | regułach, etapach, kontraktach, zadaniach (`TaskSpec`, `decoding_schema`) | sieci, GPU, providerach, węźle |
| GLU | jobach, profilach logicznych, routingu, cache, budżecie, polityce fallbacku | modelach na węźle (zna tylko fingerprinty), GPU, runtime'ach |
| Provider `self_hosted` | endpointach, TLS, tokenie, typowaniu błędów | domenie, modelach |
| `igw` (bramka) | profilach węzła, modelach, VRAM, kolejce, runtime'ach | domenie WGC (reguła, gra, Stage, przekład) |
| Runtime | modelu, tokenach | wszystkim powyżej |

Kierunek zależności w kodzie: `glu → wgc → contracts`. `igw` nie importuje `wgc` ani `glu`. Łączy je tylko HTTP
i kontrakt `igw/api@0`.

<a id="bramka"></a>
## 3. Inference Gateway (`igw`)
Cienki serwis HTTP (Python, FastAPI i uvicorn, zależność opcjonalna `[node]`).

| Endpoint | Autoryzacja | Rola |
|---|---|---|
| `GET /healthz` | nie | `{status}`: dla Harmonogramu zadań i prostych sond. Nic więcej nie ujawnia |
| `GET /v1/health` | tak | status (`ok`, `degraded`, `loading`, `down`), `node_id`, `queue_depth`, GPU (VRAM total/free, użycie), RAM, załadowane profile, stan runtime'u |
| `GET /v1/capabilities` | tak | `structured_output`, `json_schema_subset`, embeddings, vision, streaming, `async_jobs`, limity |
| `GET /v1/models` | tak | profile węzła: `model_fingerprint`, `state` (`loaded`, `cold`, `loading`, `unavailable`), `max_context`, `max_concurrency`, `est_load_seconds`, `placement`, tryby |
| `POST /v1/infer` | tak | synchroniczna inferencja (niżej) |
| `POST /v1/embed` | tak | opcjonalnie, jeśli węzeł ma profil `embed` |
| `GET /v1/metrics` | tak | JSON: requesty, tokeny, tok/s, kolejka, ładowania i ich czas, czas inferencji, błędy według kodu, deduplikacje, GPU, VRAM, RAM |
| `/v1/jobs…` | — | zarezerwowane (M-GW3, opcjonalnie): `POST` zwraca `job_id`, `GET` i `DELETE` po id; stany `pending`, `running`, `completed`, `failed`, `cancelled` |

**Odpowiedzialności:**
- przyjmuje requesty i waliduje je (schemat `igw/api@0`, limity);
- mapuje profil węzła na model;
- zarządza kolejką i schedulerem (§5);
- zwraca ustrukturyzowane wyniki z `model_fingerprint`, `node_id`, tokenami i czasami;
- raportuje health, capabilities i metryki.

**Czego nie robi:**
- nie ma logiki domenowej;
- nie ma cache wyników (to rola GLU);
- nie trzyma trwałego stanu jobów (job store GLU jest jedyną trwałą kolejką);
- nie wykonuje poleceń;
- nie przyjmuje ścieżek modeli ani plików w requeście.

**Kontrakt `POST /v1/infer`** (pełny schemat w `inference.schema.json`):
- **Request:** `request_id`, `idempotency_key` (hash klucza cache GLU), `client_ref` (nieprzezroczysty, np. id joba),
  `profile` (profil węzła), `messages`, `output.mode` (`json_schema`, `json_object`, `text`) z `output.schema`,
  `params` (`max_tokens`, `temperature`, `seed`…), `priority` (`interactive`, `batch`), `deadline_s`,
  `expected_fingerprint`.
- **Wynik:** `output.text`, `output.json`, `mode_used`, `json_valid`, `finish_reason`, `usage`,
  `timing` (`queue_ms`, `load_ms`, `infer_ms`, `tokens_per_s`, `gpu_seconds`), `model_fingerprint`, `node_id`.
- **Błąd:** `error.code`, `retryable`, `retry_after_s`. Kody i reakcja GLU w §8.

**Dlaczego synchronicznie:** joby Stage 1, 1.5 i 2/3 to zwykle < 4k tokenów wejścia i ≤ 1–2k wyjścia. Request czeka
w kolejce bramki do swojego `deadline_s`. GLU wysyła równolegle tyle requestów, ile wynosi `max_concurrency` profilu.
Restart GLU albo bramki oznacza ponowne wysłanie (joby są idempotentne, a deduplikacja działa po `idempotency_key`).
Async (`/v1/jobs`) i SSE dochodzą dopiero wtedy, gdy długie joby `local_deep` przestaną mieścić się w deadline.

**OpenAI-compatible** jest kontraktem **bramka → runtime** (adapter runtime'u). Daje wymienność runtime'u
(llama.cpp, Ollama, vLLM) i łatwe atrapy w testach, a GLU pozostaje niezwiązany ze schematem OpenAI.

<a id="profile"></a>
## 4. Profile (logiczne w GLU, fizyczne na węźle)
**GLU operuje profilami logicznymi**, nie nazwami modeli. Dwa poziomy mapowania:

```yaml
# ~/.config/glu/profiles.yaml (dev machine, poza repo; schemat glu/profiles@0 w M10)
endpoints:
  ai-node:
    provider: self_hosted
    url: https://ai-node:8443           # nazwa hosta, nigdy IP na sztywno
    ca_file: ~/.config/glu/ai-node.pem  # przypięty certyfikat węzła
    token_env: GLU_AI_NODE_TOKEN        # sekret ze zmiennej środowiskowej / keyringu
    connect_timeout_s: 3
    request_timeout_s: 900
profiles:
  local_fast:     {endpoint: ai-node, node_profile: fast,     temperature: 0, seed: 0, max_tokens: 2048}
  local_semantic: {endpoint: ai-node, node_profile: semantic, temperature: 0, seed: 0, max_tokens: 2048}
  local_deep:     {endpoint: ai-node, node_profile: deep,     temperature: 0, seed: 0, priority: batch}
  premium_semantic: {provider: anthropic, model: <najmocniejszy dostępny model Claude>, api_key_env: ANTHROPIC_API_KEY}
  premium_translate: {provider: anthropic, model: <najmocniejszy dostępny model Claude>, api_key_env: ANTHROPIC_API_KEY}  # przekład Stage 3 (ADR-0029)
fallback:
  self_hosted_unavailable: queue        # queue | block | fail
  allow_premium_fallback: false
  max_wait_seconds: 7200
```

```yaml
# %ProgramData%\igw\node.yaml (węzeł, poza repo; schemat igw/node@0 w M-GW1)
node_id: ai-node-01
listen: {host: <adres IP interfejsu LAN>, port: 8443, tls_cert: ..., tls_key: ...}
auth: {tokens_file: '%ProgramData%\igw\secrets\tokens.json', client_allowlist: [<dev machine>]}
limits: {max_request_bytes: 1048576, max_queue: 256, max_tokens: 4096}
vram_budget_mb: 23000
runtime: {kind: llama_cpp, binary: 'C:\igw\llama.cpp\llama-server.exe', version: <przypięta>}
models:
  m_fast:     {file: 'D:\models\<fast>.gguf', sha256: ..., ctx: 16384, n_gpu_layers: all, parallel: 6, vram_mb: 9000}
  m_semantic: {file: 'D:\models\<semantic>.gguf', sha256: ..., ctx: 16384, n_gpu_layers: all, parallel: 2, vram_mb: 20000}
  m_deep:     {file: 'D:\models\<deep>.gguf', sha256: ..., ctx: 8192, n_gpu_layers: all, n_cpu_moe: <N>, parallel: 1, vram_mb: 22000}
profiles:
  fast:      {model: m_fast,     modes: [interactive, batch], pinned: false}
  semantic:  {model: m_semantic, modes: [interactive, batch]}
  deep:      {model: m_deep,     modes: [batch]}
scheduler: {min_residency_s: 120, max_wait_s: 600, batch_window_ms: 200}
```

**Klasy profili.** Wartości są hipotezami do pomiaru w M-INF. Nazwy modeli wybiera benchmark. Węzeł nie pisze
przekładu Stage 3 (pisze go premium, ADR-0029), więc profil `translate` nie jest potrzebny.

| Profil węzła | Klasa i rozmieszczenie | Jakość / opóźnienie / VRAM / RAM | Zastosowanie |
|---|---|---|---|
| `fast` | 7–14B, Q5–Q8, cały w VRAM, kontekst 16k, 4–8 slotów | średnia / niskie / 6–12 GB / — | klasyfikacja, ekstrakcja, triage, szkice |
| `semantic` | ~24–32B dense albo ~30B MoE, Q4, cały w VRAM (~17–20 GB), 1–3 sloty | wysoka / średnie / prawie cała karta / — | druga ekstrakcja, weryfikacja, relacje, przypadki, wsteczna ekstrakcja IR z przekładu |
| `deep` | ~70B dense albo duże MoE z ekspertami w RAM (`--n-cpu-moe`), 1 slot, tylko `batch` | najwyższa lokalnie / wysokie (kilka–kilkanaście tok/s) / cała karta / 40–80 GB | rozjemca sporów, trudne analizy przed premium, pass naprawczy |
| `embed` | opcjonalny, mały (GPU lub CPU), `pinned` | — | tylko jeśli zadanie tego wymaga (KB jest przeszukiwana deterministycznie) |

**Jak wykorzystujemy 24 GB VRAM i 128 GB RAM:**
- RTX 3090 obsługuje główny inference.
- RAM służy do trzech rzeczy:
  - page cache plików GGUF, więc ponowne załadowanie modelu jest tańsze niż odczyt z NVMe;
  - offload ekspertów MoE i większe kwantyzowane modele dla `deep`;
  - profile CPU-only.
- **Nie zakładamy, że model częściowo w RAM jest wystarczająco szybki do każdego joba.** `deep` działa tylko wsadowo
  i tylko tam, gdzie zmniejsza liczbę eskalacji premium.

<a id="scheduler"></a>
## 5. Scheduler i cykl życia modeli (jedna RTX 3090)
Cel: nie dopuścić do ładowania A, potem B, potem znowu A przy każdym requeście, i nie zagłodzić żadnego profilu.

- **Kolejki per profil węzła**, FIFO z priorytetem `interactive` > `batch`. `max_queue` daje odpowiedź 429.
- **Afinicja:** najpierw obsługujemy profile, których model jest już załadowany, do liczby slotów (`parallel`).
- **Przełączenie modelu** następuje tylko wtedy, gdy profil z pracą nie jest załadowany i zachodzi jeden z warunków:
  - (a) załadowane profile nie mają pracy;
  - (b) najstarszy request zimnego profilu czeka ≥ `max_wait_s`, a bieżący model był załadowany ≥ `min_residency_s`.
- **Eviction:** LRU wśród modeli bez requestów w toku, aż suma `vram_mb` zmieści się w `vram_budget_mb`.
  Profile `pinned` nie są wyładowywane. Profile-aliasy tego samego modelu nie wymagają przełączenia.
- **Ładowanie:** bramka uruchamia `llama-server` dla modelu (port efemeryczny na `127.0.0.1`), czeka na jego health
  i mierzy `load_ms`, który wchodzi do metryk i do `timing` pierwszego requestu.
  - W trakcie ładowania requesty profilu czekają w kolejce do `deadline_s`, potem dostają `503 model_loading`
    z `retry_after_s`.
  - Po zmierzonym `vram_mb` bramka koryguje swój budżet.
- **Batching:** sloty `--parallel` i ciągłe batchowanie runtime'u. `batch_window_ms` zbiera requesty tego samego
  profilu przed startem.
- **Deduplikacja:** identyczny `idempotency_key` w toku podpina się pod ten sam wynik. Węzeł nie ma cache wyników.
- **Rola GLU:** GLU nadal porządkuje joby według profilu (fale), ale to tylko **wskazówka**. Właścicielem cyklu życia
  modelu jest bramka, bo widzi wszystkich klientów i stan VRAM.
- **Wariant M-GW2:** tryb routera llama.cpp (`--models-dir`, `--models-max`) jako adapter. Bramka zachowuje politykę
  eviction.

<a id="cache"></a>
## 6. Cache: dwa rodzaje, bez dublowania
| Cache | Gdzie | Klucz / zawartość | Właściciel |
|---|---|---|---|
| L1 inferencji, L2 wyniku joba | dev machine, `.glu/` | klucz z `profile_fingerprint` (= `model_fingerprint` z węzła + profil węzła + parametry próbkowania GLU), wiadomości, schemat / surowa odpowiedź; `cache_key` joba / zaakceptowana propozycja | GLU (GLU.md §6) |
| Pliki modeli, page cache GGUF, prompt/KV cache slotów | węzeł | pliki wag (hash w `node.yaml`), prefix cache runtime'u w obrębie slotu | `igw` i runtime |

- `model_fingerprint` = hash z: sha256 pliku modelu, kwantyzacji, nazwy i wersji runtime'u oraz parametrów, które
  wpływają na wynik (kontekst, rope, szablon czatu). **Bez hosta, IP i `node_id`.**
  - Podmiana modelu na węźle oznacza miss.
  - Nowy węzeł z tym samym modelem i runtime'em oznacza trafienia.
  - Aktualizacja runtime'u to świadoma invalidacja (wersję się przypina).
- GLU zapisuje w buildzie `inference_snapshot` (profil → `model_fingerprint` na starcie buildu). Bez węzła GLU korzysta z cache
  L2 i z ostatnich znanych fingerprintów. Wynik z cache jest prawdziwym wynikiem tego modelu.

<a id="zrodlo-prawdy"></a>
## 7. Źródło prawdy i bezpieczeństwo (projekt)
**Węzeł nie jest źródłem prawdy.** Kanoniczny stan żyje w repo gry (`kb/`, `source/inventory.yaml`) i w repo narzędzia.
Na węźle są tylko:
- binarki;
- pliki modeli;
- `node.yaml`;
- certyfikat;
- hashe tokenów.

Wszystko to da się odtworzyć według [DEPLOYMENT.md](DEPLOYMENT.md). `kb/` nie zawiera hosta ani `node_id`.

**Minimalne rozsądne bezpieczeństwo** (LAN nie jest z założenia zaufany):

| Warstwa | Środek |
|---|---|
| Sieć | `igw` słucha tylko na adresie interfejsu LAN. Runtime słucha **tylko na 127.0.0.1**. Reguła Windows Firewall wpuszcza TCP 8443 tylko z adresów dev machine i tylko w profilu Private |
| Transport | HTTPS w uvicornie, certyfikat z SAN = nazwa hosta (`ai-node`). Klient przypina certyfikat lub CA (`ca_file`). Reverse proxy niepotrzebne |
| Uwierzytelnienie | token Bearer, osobny dla każdego klienta. Na węźle tylko hashe (`tokens.json` w `%ProgramData%\igw\secrets\`, ACL konta usługi). U klienta zmienna środowiskowa lub keyring. Nic w repo |
| Autoryzacja | allowlista IP klientów także w bramce (obrona w głąb) |
| Wejście | limit rozmiaru body, `max_tokens`, kontekstu i długości kolejki. Tylko profile z `node.yaml`. Żadnych ścieżek, plików, poleceń ani `exec` |
| Dane | prompty mogą zawierać tekst chroniony (ADR-0012). Węzeł **nie zapisuje** promptów ani wyjść na dysk. Logi zawierają metadane (`request_id`, `client_ref`, profil, tokeny, czasy, kod błędu) |
| Poza zakresem | IAM, SSO, mTLS dla wielu organizacji, service mesh |

<a id="awarie"></a>
## 8. Awarie i reakcja GLU
| Sytuacja | Sygnał | `error_class` | Reakcja GLU |
|---|---|---|---|
| DNS nie rozwiązuje `ai-node` | wyjątek DNS | `network` | job `waiting_inference`, backoff z jitterem, circuit breaker na endpoint, build `waiting_inference` |
| LAN nie działa, węzeł wyłączony lub uśpiony | timeout połączenia lub odmowa | `network` / `timeout` | jak wyżej (domyślnie `queue`, ADR-0017) |
| zły certyfikat | błąd TLS | `tls` | build `failed` z diagnozą `glu doctor`. Bez retry i bez premium |
| zły lub brak tokenu | 401/403 | `auth` | jak wyżej |
| runtime padł | 503 `runtime_unavailable` | `runtime` | bramka restartuje proces, GLU czeka |
| model się ładuje | 503 `model_loading` + `retry_after_s` | `model_loading` | czekanie zgodnie z `retry_after_s` |
| kolejka pełna | 429 `queue_full` | `overloaded` | backoff, mniejsza równoległość |
| brak profilu lub capability, inny fingerprint niż oczekiwany | 404/409 `unknown_profile` / `capability_missing` | `capability_missing` | job czeka albo `failed`. **Nigdy** cicha podmiana profilu lub modelu |
| deadline minął | 504 `deadline_exceeded` | `timeout` | ponowne wysłanie (idempotentne) |
| zły JSON albo wynik niezgodny ze schematem | wynik 200 | `bad_output` | **pętla jakości**: retry z błędami, potem eskalacja. To nie jest błąd dostępności |

- Błędy dostępności (`network`, `tls`, `auth`, `timeout`, `overloaded`, `model_loading`, `runtime`) nie zużywają
  limitu prób jakościowych.
- Fallback do premium działa tylko przy `allow_premium_fallback: true`, z `premium_reason: self_hosted_unavailable`.

<a id="multi-node"></a>
**Przyszły multi-node** (bez implementacji w MVP):
- API ma `node_id`, listę profili i capability discovery;
- konfiguracja GLU ma listę endpointów;
- drugi węzeł to drugi endpoint z tymi samymi profilami, albo router o tym samym `igw/api@0` przed węzłami;
- GLU wybiera endpoint według health i capabilities, a fingerprint pozwala współdzielić cache.

<a id="monitoring"></a>
## 9. Telemetria węzła
- `GET /v1/metrics` (JSON) i logi strukturalne (JSON lines, rotacja) w `%ProgramData%\igw\logs\`.
- Metryki:
  - requesty;
  - tokeny in/out;
  - tok/s (średnie i dla każdego profilu);
  - `queue_depth`;
  - liczba i czas ładowań modeli;
  - czas inferencji;
  - użycie GPU, VRAM i RAM;
  - błędy według kodu;
  - deduplikacje.

  Retry liczy klient (GLU Attempt).
- GPU czytamy przez `nvidia-smi --query-gpu=... --format=csv` (stałe argumenty, bez powłoki) albo bibliotekę NVML.
- Bez Prometheusa i Grafany w MVP. `llama-server --metrics` można dołączyć później.
- GLU agreguje metryki z `infer_result` w Attempt (`gpu_seconds`, `queue_seconds`, `load_seconds`, `node_id`)
  i w `glu stats` ([COST.md](../COST.md#obserwowalnosc)).

<a id="diagnostyka"></a>
## 10. Diagnostyka
**`glu doctor [--endpoint ai-node] [--json]`** (dev machine, M-E2E). Kolejne kroki zatrzymują się na pierwszym błędzie
z poradą:
1. konfiguracja `profiles.yaml` (endpoint, `ca_file`, zmienna tokenu istnieje);
2. DNS lub nazwa hosta (rozwiązanie `ai-node`);
3. TCP na porcie (z czasem);
4. TLS (certyfikat, SAN, przypięcie);
5. `GET /healthz`;
6. autoryzacja (`GET /v1/health`);
7. `capabilities` (wersja API, structured output);
8. `models` (każdy profil logiczny ma profil węzła, fingerprinty);
9. GPU, runtime i kolejka (z `health`);
10. test structured output: mały schemat na profilu `fast`, wynik JSON zgodny ze schematem;
11. opcjonalnie `--profile semantic --load`, czyli pomiar czasu ładowania.

**`igw doctor`** (węzeł, M-GW2): sterownik i GPU (`nvidia-smi`), binarka runtime'u i jej wersja, pliki modeli
(sha256), wolny VRAM i RAM, nasłuch tylko na LAN, obecność reguły firewall, certyfikat i jego ważność, plik tokenów.
