# Routing, providerzy i self-hosted inference

**Local = self-hosted.** Tier `local` i profile `local_*` oznaczają modele na naszej infrastrukturze za Inference
Gateway (docelowo osobny węzeł w LAN), a nie model na localhost ([ADR-0015](adr/ADR-0015-self-hosted-inference-wezel-lan.md),
[inference/NODE.md](inference/NODE.md#definicja)).

## 1. Tiery wykonania
| Tier | Wykonawca | Do czego | Przykłady zadań |
|---|---|---|---|
| **0 deterministyczny** | kod WGC | wszystko, co da się zrobić bez modelu | ingest, segmentacja, hashe, parsowanie tabel, harvest terminów, odsyłacze, relacje warstwy scenariusza, `LEG-` z zakazów, sygnały ryzyka, walidacja, gate, widoki, LaTeX |
| **1 self-hosted szybki** | `local_fast` | szkice i ekstrakcja przy dobrze określonym wyjściu | szkic reguł z segmentu, klasyfikacja segmentów, propozycje pojęć |
| **2 self-hosted semantyczny** | `local_semantic` | niezależna druga ekstrakcja, weryfikacja, wsteczna ekstrakcja IR z przekładu | weryfikacja szkicu, relacje, przypadki kontrolne, kontrola przekładu |
| **2+ self-hosted głęboki** | `local_deep` (tylko wsadowo) | rozjemca sporów, pass naprawczy, przygotowanie pakietu review | spór `medium`, wyczerpane próby walidacji przed premium |
| **3 premium** | `premium_semantic`, `premium_translate` | **starszy recenzent semantyczny**: tylko trudne przypadki, rozbieżności, audyt. Wyjątek: przekład Stage 3 (ADR-0029) | rekordy `high`/`critical`, spory lokalne, niejasności, próbka audytowa; przekład segmentów |
| **4 człowiek** | właściciel | to, czego system nie powinien zgadywać | interpretacje, terminy, polityki, przekroczony budżet |

Schemat nie jest sztywny. Polityka routingu jest daną (`routing@N`), a zadanie może deklarować własną drabinę tierów.
`local_deep` to profil tieru `local` (ten sam tier w kontrakcie), a nie osobny tier.

## 2. Polityka routingu `routing@0` (do implementacji w M12)
Wejście: klasa ryzyka i twarde reguły z `wgc/risk@N`, wynik walidacji, zgodność wykonań lokalnych, historia prób, budżet.

| # | Warunek | Decyzja |
|---|---|---|
| 1 | zadanie ma `deterministic_impl` | Tier 0. Model nie jest wołany |
| 2 | cache L2 trafia (ten sam `cache_key`) | akceptacja z cache |
| 3 | domyślnie | Tier 1 → walidacja |
| 4 | ryzyko `low`, walidacja OK | akceptacja lokalna (+ losowanie do audytu, reguła 9) |
| 5 | ryzyko `medium` | Tier 2 wykonuje niezależną ekstrakcję. Zgoda po normalizacji + walidacja OK → akceptacja, w przeciwnym razie Tier 3 |
| 6 | ryzyko `high`/`critical` albo jakakolwiek reguła `forced` | Tier 3, także gdy wykonania lokalne się zgadzają |
| 7 | walidacja nie przechodzi po N próbach na tierze | eskalacja o jeden tier |
| 8 | wynik `requires_human_interpretation` albo niejasność z `impact.semantic` bez źródła rozstrzygającego | Tier 4 (pytanie `HD-` w kolejce) |
| 9 | audyt: losowe p% (domyślnie 10%, potem z kalibracji) akceptacji lokalnych | kopia do Tier 3. Niezgodność zwiększa szacowany odsetek FN i wymusza rekalibrację |
| 10 | budżet premium wyczerpany | job czeka (`waiting_review`). **Nigdy** nie spada do akceptacji lokalnej |
| 11 | spór Tier 1 vs Tier 2 albo wyczerpane próby na Tier 2 | `local_deep` przygotowuje diff kandydatów, analizę rozbieżności albo pass naprawczy i pakiet review, potem Tier 3. `local_deep` **nie daje akceptacji**; wynik passu naprawczego przechodzi zwykłą walidację i reguły ryzyka, a spór (`local_disagreement`, `forced`) zawsze kończy się Tier 3 (ADR-0028) |
| 12 | provider self-hosted niedostępny (`error_class` dostępności) | job `waiting_inference` zgodnie z `fallback.self_hosted_unavailable` (domyślnie `queue`). Nie zużywa prób jakościowych. Premium **tylko** przy `allow_premium_fallback: true` (`premium_reason: self_hosted_unavailable`) |
| 13 | brak profilu lub capability na węźle | czekanie albo `failed` (`capability_missing`). Nigdy cicha podmiana profilu |

Każda decyzja wybierająca premium zapisuje `premium_reason` (`glu/exec@0`): `risk_class`, `forced_rule`,
`local_disagreement`, `validation_exhausted`, `audit_sample`, `capability_missing`, `self_hosted_unavailable` albo
`human_request`. Dzięki temu fallback dostępności nie miesza się z eskalacją semantyczną
([ADR-0017](adr/ADR-0017-niedostepnosc-wezla-bez-premium-fallback.md)).

W telemetrii i raportach rozróżniamy dwie klasy, wyprowadzane z `premium_reason` (bez nowego pola w kontrakcie):
- **`infrastructure_fallback`**: `self_hosted_unavailable`. Powstaje tylko po jawnym `allow_premium_fallback: true`.
  Nie mówi nic o trudności zadania i nie kalibruje ryzyka;
- **`semantic_escalation`**: pozostałe powody (`risk_class`, `forced_rule`, `local_disagreement`,
  `validation_exhausted`, `audit_sample`, `capability_missing`, `human_request`). Podlega kalibracji routingu i audytowi.

Asymetria (ADR-0010): niepotrzebna eskalacja kosztuje pieniądze, a fałszywie negatywny wynik kosztuje poprawność
całego łańcucha (logika → silnik → przekład). Każda decyzja zapisuje `routing_decision` z sygnałami i powodami.

## 3. Abstrakcja providera
```text
Provider.generate(GenerationRequest) -> GenerationResult
  request: profile (logiczny), messages, output (mode + decoding_schema), max_tokens, temperature, seed,
           deadline, priority (interactive|batch), idempotency_key (hash klucza L1), client_ref (id joba, nieprzezroczysty)
  result:  text/json, finish_reason, tokens_in/out, timing (queue, load, infer), model_fingerprint, node_id?,
           cost_usd? (premium), gpu_seconds? (self-hosted, raportowane przez węzeł)
Provider.embed(EmbedRequest) -> EmbedResult              (opcjonalnie)
Provider.health() -> ok | degraded | unavailable(reason)
Provider.capabilities() -> {structured_output, json_schema_subset, embeddings, vision, max_context, async_jobs}
Provider.models() -> [{profile, model_fingerprint, state, max_concurrency, max_context}]
errors:  ProviderUnavailable (network, tls, timeout, runtime, model_loading) · ProviderAuthError ·
         ProviderOverloaded · CapabilityMissing · BadOutput (→ pętla jakości, nie dostępność)
```
Implementacje:

| Provider | Do czego | Milestone |
|---|---|---|
| `fake` | reguły → odpowiedzi, deterministyczny (testy) | M10 |
| `replay` | nagrania L1 (testy bez GPU; nagrania z prawdziwego węzła z M-E2E) | M10 |
| `self_hosted` | klient protokołu `igw/api@0` (Inference Gateway) przez HTTPS z przypiętym certyfikatem i tokenem | M10 |
| `anthropic` | premium przez API | M15 |
| `desktop_pull` | premium przez kolejkę i Claude Desktop (ADR-0013) | M15 |

- **GLU nie rozmawia z runtime'em** (llama.cpp, Ollama, vLLM) i nie zna jego portu ani endpointu. Robi to bramka
  przez własny adapter runtime'u (dziś OpenAI-compatible, ale to szczegół bramki, a nie kontrakt GLU;
  [ADR-0016](adr/ADR-0016-inference-gateway-i-protokol.md)). Kontrakt GLU↔bramka to `igw/api@0`, kontrakt
  bramka→runtime jest wewnętrzny dla `igw`. Bramkę można uruchomić także na localhost lub drugim węźle, a GLU tego
  nie odróżnia (zmienia się tylko `url` w `profiles.yaml`).
- **Profile logiczne vs modele fizyczne:** GLU operuje na profilu (`local_fast` → `node_profile: fast`). Fizyczny model
  widzi tylko bramka. `/v1/models` zwraca profile węzła razem z `model_fingerprint`, więc GLU zna dostępne profile
  i zapisuje fingerprint w provenance i cache bez znajomości nazwy GGUF ani runtime'u.
- Core nie zależy od żadnego serwera ani modelu. Schemat dekodowania (`decoding_schema` z TaskSpec) mieści się w
  `capabilities.json_schema_subset` (np. bez `if/then/else`). Brak structured output oznacza JSON mode + walidację
  + retry.
- **Tożsamość modelu pochodzi z węzła** (`model_fingerprint` z `/v1/models` i z każdego wyniku). GLU nie zgaduje jej
  z własnej konfiguracji. Do klucza cache wchodzi `profile_fingerprint` = hash(`model_fingerprint` raportowany przez węzeł, `node_profile`, parametry próbkowania i wyjścia z `profiles.yaml`) ([inference/NODE.md §6](inference/NODE.md#cache)).

## 4. Profile modeli
Domena zna tylko nazwy profili logicznych. Mapowanie ma dwa poziomy:
- GLU: profil logiczny → endpoint i profil węzła, w `~/.config/glu/profiles.yaml` na dev machine, poza repo;
- węzeł: profil węzła → model, w `node.yaml`, poza repo.

Przykłady obu plików i klasy profili `fast`, `semantic`, `deep`, `embed`:
[inference/NODE.md §4](inference/NODE.md#profile). Skrót konfiguracji GLU:
```yaml
endpoints:
  ai-node: {provider: self_hosted, url: https://ai-node:8443, ca_file: ~/.config/glu/ai-node.pem, token_env: GLU_AI_NODE_TOKEN}
profiles:
  local_fast:       {endpoint: ai-node, node_profile: fast,     temperature: 0, seed: 0}
  local_semantic:   {endpoint: ai-node, node_profile: semantic, temperature: 0, seed: 0}
  local_deep:       {endpoint: ai-node, node_profile: deep,     temperature: 0, seed: 0, priority: batch}
  premium_semantic: {provider: anthropic, model: <najmocniejszy dostępny model Claude>, api_key_env: ANTHROPIC_API_KEY}
  premium_translate: {provider: anthropic, model: <najmocniejszy dostępny model Claude>, api_key_env: ANTHROPIC_API_KEY}
fallback: {self_hosted_unavailable: queue, allow_premium_fallback: false}
```
Profile pozostają wymienialne: zmiana modelu to zmiana `node.yaml` i nowy fingerprint, a zmiana węzła to zmiana `url`.
Stage 1, 1.5, 2 i 3 mogą mapować profile na różne modele (logika ≠ przekład ≠ redakcja).

<a id="self-hosted"></a>
## 5. Self-hosted inference: węzeł RTX 3090 w LAN
**Strategia:** self-hosted compute to **zasób obfity**, więc używamy go agresywnie: wiele passów, druga ekstrakcja,
weryfikatory, rozjemca `local_deep`. Warunek: benchmark potwierdza jakość, a każdy pass ma cel w polityce routingu.
Konkretne modele wybiera **M-INF** (benchmark przez bramkę na węźle).

- **Topologia:** dev machine (Claude Desktop, MCP, GLU, repo gier) → HTTPS → `ai-node` (Windows 11 Pro, RTX 3090
  24 GB, 128 GB RAM) z Inference Gateway (`igw`) i llama.cpp server natywnie na Windows
  ([ADR-0018](adr/ADR-0018-runtime-mvp-llama-cpp-windows.md)). vLLM w WSL2 tylko po benchmarku (M-VLLM).
- **VRAM:** wagi + KV cache + narzut. Orientacyjnie (do weryfikacji pomiarem):
  - model ~30B w 4 bitach zajmuje ok. 17–20 GB, co daje kontekst 8–16k przy małej równoległości;
  - model 7–14B mieści długi kontekst i wysoką równoległość;
  - **dwa duże profile zwykle nie zmieszczą się jednocześnie**.
- **RAM 128 GB:** page cache plików modeli (tańsze przeładowania), offload ekspertów MoE dla `deep`, profile CPU.
  Model częściowo w RAM jest wolny, więc służy tylko do trybu wsadowego.
- **Cykl życia modeli** należy do bramki: afinicja profilu, minimalny czas rezydencji, limit oczekiwania i LRU w budżecie
  VRAM ([inference/NODE.md §5](inference/NODE.md#scheduler)). GLU porządkuje joby według profilu (fale), ale to tylko
  wskazówka.
- **Kontekst:** zadania Stage 1 pracują na segmencie i jego sąsiedztwie (zwykle < 4k tokenów wejścia). Kontekst buduje
  `context_builder` z grafu, a nie z całej instrukcji.
- **Równoległość:** GLU wysyła równolegle najwyżej `max_concurrency` profilu z `/v1/models`. Przy 429 lub 503 robi
  backoff z jitterem.
- **Niedostępność węzła:** `waiting_inference`, bez automatycznego premium (reguła 12, ADR-0017). Cache L2 działa
  offline.
- **Sieć i bezpieczeństwo:** nazwa hosta, HTTPS, token, firewall, allowlista
  ([inference/NODE.md §7](inference/NODE.md#zrodlo-prawdy), [inference/DEPLOYMENT.md](inference/DEPLOYMENT.md#siec)).
- **Bez węzła** (laptop deweloperski, CI): `fake` i `replay`. Testy nigdy nie wołają prawdziwego modelu ani sieci.

## 6. Premium jako starszy recenzent
Premium nie wykonuje masowej ekstrakcji. Jedynym zadaniem masowym premium jest przekład Stage 3 (ADR-0029): premium
pisze przekład, a wierność sprawdzają kroki deterministyczne i self-hosted. W pozostałych etapach premium dostaje pakiety (`review_package`) dla rekordów, w których lokalna praca
jest ryzykowna lub sporna, oraz próbkę audytową. Odpowiada w `answer_schema`: werdykt (`accept`, `correct`,
`requires_human_interpretation`), poprawiony rekord (jeśli `correct`), uzasadnienie z kotwicami, nowe niejasności.
Wynik przechodzi tę samą walidację WGC co praca lokalna.
