# Routing, providerzy i lokalna inferencja

## 1. Tiery wykonania
| Tier | Wykonawca | Do czego | Przykłady zadań |
|---|---|---|---|
| **0 deterministyczny** | kod WGC | wszystko, co da się zrobić bez modelu | ingest, segmentacja, hashe, parsowanie tabel, harvest terminów, odsyłacze, relacje warstwy scenariusza, `LEG-` z zakazów, sygnały ryzyka, walidacja, gate, widoki, LaTeX |
| **1 lokalny szybki** | `local_fast` | szkice i ekstrakcja przy dobrze określonym wyjściu | szkic reguł z segmentu, klasyfikacja segmentów, propozycje pojęć |
| **2 lokalny semantyczny** | `local_semantic` | niezależna druga ekstrakcja, weryfikacja, wsteczna ekstrakcja IR z przekładu | weryfikacja szkicu, relacje, przypadki kontrolne, przekład |
| **3 premium** | `premium_semantic` | **starszy recenzent semantyczny**: tylko trudne przypadki, rozbieżności, audyt | rekordy `high`/`critical`, spory lokalne, niejasności, próbka audytowa |
| **4 człowiek** | właściciel | to, czego system nie powinien zgadywać | interpretacje, terminy, polityki, przekroczony budżet |

Schemat nie jest sztywny. Polityka routingu jest daną (`routing@N`), a zadanie może deklarować własną drabinę tierów.

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

Asymetria (ADR-0010): niepotrzebna eskalacja kosztuje pieniądze, a fałszywie negatywny wynik kosztuje poprawność
całego łańcucha (logika → silnik → przekład). Każda decyzja zapisuje `routing_decision` z sygnałami i powodami.

## 3. Abstrakcja providera
```text
Provider.generate(GenerationRequest) -> GenerationResult
  request: profile, messages, output_schema (JSON Schema), max_tokens, temperature, seed, timeout, metadata(job)
  result:  text/json, parsed?, finish_reason, tokens_in/out, latency, model_id, cost_usd?, gpu_seconds?
Provider.capabilities -> {structured_output: json_schema|grammar|json_mode|none, max_context, batching, concurrency}
Provider.health() -> ok | reason
```
Implementacje: `fake` (reguły → odpowiedzi, deterministyczny), `replay` (nagrania L1), `openai_compat` (vLLM,
llama.cpp server, Ollama, LM Studio), `anthropic`. Brak natywnego structured output → JSON mode + walidacja + retry.
Core nie zależy od żadnego serwera ani modelu (ADR-0009).

## 4. Profile modeli
Domena zna tylko nazwy profili. Mapowanie żyje u użytkownika (`~/.config/glu/profiles.yaml`, poza repo):
```yaml
profiles:
  local_fast:
    provider: openai_compat
    base_url: http://127.0.0.1:8000/v1        # tylko adresy z allowlisty endpointów
    model: <model klasy 7–14B, instrukcyjny>
    quant: <np. Q5/AWQ>
    context: 16384
    concurrency: 8
    temperature: 0
  local_semantic:
    provider: openai_compat
    base_url: http://127.0.0.1:8001/v1
    model: <model klasy ~30B (gęsty albo MoE), instrukcyjny>
    quant: <np. Q4/AWQ>
    context: 16384
    concurrency: 2
    temperature: 0
  premium_semantic:
    provider: anthropic                       # albo desktop_pull
    model: <najmocniejszy dostępny model Claude>
    api_key_env: ANTHROPIC_API_KEY
```
`profile_fingerprint` = hash z (provider, model, plik i kwantyzacja wag, kontekst, parametry próbkowania) wchodzi do
klucza cache. Zmiana modelu nie może zwrócić starego wyniku.

## 5. Lokalna inferencja: RTX 3090 (24 GB), WSL2
**Strategia:** maksymalnie dużo pracy lokalnie, ale tylko tam, gdzie benchmark potwierdza jakość. Konkretne modele
i serwer wybiera milestone **M-INF** na podstawie benchmarku logiki z `bench/`. Ten dokument nie zaszywa nazw modeli.

- **Serwer:** jeden z vLLM (guided JSON, ciągłe batchowanie, AWQ/GPTQ), llama.cpp server (GGUF, `json_schema` /
  gramatyki, mały narzut) albo Ollama (najprostszy start, `format` ze schematem). Wszystkie przez `openai_compat`.
  Uruchamiane w WSL2 z CUDA (sterownik NVIDIA po stronie Windows, toolkit CUDA dla WSL po stronie Linuksa).
- **Budżet VRAM:** wagi + KV cache + narzut. Orientacyjnie (do weryfikacji pomiarem): model ~30B w 4 bitach zajmuje
  ok. 17–20 GB i zostawia kilka GB na KV cache, czyli kontekst rzędu 8–16k przy małej równoległości. Model 7–14B
  w 4–8 bitach mieści długi kontekst i wysoką równoległość. **Dwa profile zwykle nie zmieszczą się jednocześnie.**
- **Ładowanie modeli:** scheduler GLU grupuje joby w **fale według profilu** (najpierw wszystkie `local_fast`
  z poziomu, potem przełączenie na `local_semantic`) i mierzy koszt przełączenia (czas ładowania wliczany do `gpu_seconds`).
- **Kontekst:** zadania Stage 1 pracują na segmencie i jego sąsiedztwie (zwykle < 4k tokenów wejścia). Długi kontekst
  nie jest potrzebny, bo kontekst buduje `context_builder` z grafu, a nie z całej instrukcji.
- **Batching i równoległość:** limit `concurrency` na profil. Retry z backoffem przy przeciążeniu. Joby są niezależne
  (wejście = segment + kontekst), więc dobrze się batchują.
- **WSL2:** repo gier w systemie plików Linuksa (szybkie I/O). Serwer modelu nasłuchuje na `127.0.0.1`. Claude Desktop
  łączy się z GLU przez `wsl.exe` (MCP stdio). Pamięć WSL ustawiona w `.wslconfig` (RAM hosta jest duży).
- **Bez GPU** (laptop deweloperski, CI): `fake`/`replay`. Testy nigdy nie wołają prawdziwego modelu.

## 6. Premium jako starszy recenzent
Premium nie wykonuje masowej ekstrakcji. Dostaje pakiety (`review_package`) dla rekordów, w których lokalna praca
jest ryzykowna lub sporna, oraz próbkę audytową. Odpowiada w `answer_schema`: werdykt (`accept`, `correct`,
`requires_human_interpretation`), poprawiony rekord (jeśli `correct`), uzasadnienie z kotwicami, nowe niejasności.
Wynik przechodzi tę samą walidację WGC co praca lokalna.
