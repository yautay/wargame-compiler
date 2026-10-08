# ADR-0018: Runtime MVP: llama.cpp server natywnie na Windows; vLLM w WSL2 tylko po benchmarku

- **Status:** przyjęty (MVP; liczby do potwierdzenia w M-INF)
- **Data:** 2026-10-05
- **Milestone:** M-INF0

## Kontekst
Węzeł: Windows 11 Pro, RTX 3090 24 GB (Ampere), 128 GB RAM. Fakty sprawdzone 2026-10-05 (źródła niżej):

**llama.cpp server:**
- natywne buildy CUDA na Windows, GGUF z pełną gamą kwantyzacji;
- `response_format` typu `json_schema` (konwersja do gramatyki: bez `if/then/else`, bez `not`, nieobsługiwane cechy
  pomijane po cichu);
- `--parallel` (sloty) z ciągłym batchowaniem;
- `--cpu-moe` i `--n-cpu-moe` (eksperty MoE w RAM);
- `/v1/embeddings`, `/health`, `/metrics` (`--metrics`), `--api-key`;
- tryb routera (`--models-dir`, `--models-max`) z dynamicznym ładowaniem modeli.

**vLLM:**
- brak oficjalnego wsparcia Windows, ścieżki to WSL2 albo Docker z backendem WSL2 (są buildy natywne społeczności);
- najlepsza przepustowość przy wielu równoległych requestach;
- wolniejszy start, prealokacja VRAM, praktycznie brak CPU offloadu.

Źródła:
- llama.cpp: README serwera (`ggml-org/llama.cpp`, `tools/server/README.md`) i README gramatyk (`grammars/README.md`);
- vLLM: źródła wtórne (przeglądy wsparcia Windows z 2026 r., blog Docker Model Runner o vLLM na Windows przez WSL2),
  do potwierdzenia w oficjalnej dokumentacji instalacji vLLM w M-INF/M-VLLM.

**Ollama:** natywna na Windows, ale ma własny scheduler ładowania i zwalniania modeli (konflikt z schedulerem bramki)
i mniejszą kontrolę nad parametrami i tożsamością modelu.

## Decyzja
- **MVP runtime: llama.cpp server natywnie na Windows**, nadzorowany przez `igw` (jeden proces na załadowany model,
  słuchający na `127.0.0.1`). Tryb routera llama.cpp to wariant adaptera do oceny w M-GW2. Bramka zachowuje własną
  politykę eviction, bo zna kolejkę.
- **Windows-native w MVP, bez WSL2.** Prostsza sieć (bez NAT, `portproxy` i reguł Hyper-V), start po restarcie,
  dostęp do całego RAM, modele na NTFS i jedna warstwa do utrzymania.
- **Autostart:** Harmonogram zadań („przy uruchomieniu”, konto usługi, restart po awarii) uruchamia tylko `igw`, a ten
  uruchamia procesy runtime'u. Wariant: usługa Windows przez wrapper (WinSW), oceniany w M-NODE.
- **Przyszła opcja high-throughput: vLLM (albo SGLang) w WSL2**, tylko gdy benchmark M-INF wykaże, że batching,
  równoległość lub przepustowość są wąskim gardłem dla jednego gorącego profilu (milestone opcjonalny M-VLLM, adapter
  runtime'u w `igw`). GLU się wtedy nie zmienia.
- Konkretne modele, kwantyzacje i liczby wybiera M-INF (benchmark przez bramkę). Ten ADR nie zaszywa nazw modeli.

## Konsekwencje
- Schematy dekodowania muszą mieścić się w dialekcie `llama.cpp-gbnf@1` (TaskSpec `decoding_schema`, M9). Pełna
  walidacja dalej odbywa się po stronie GLU i WGC.
- Model częściowo offloadowany do RAM (`deep`) jest wolny. Służy do trybu wsadowego, nie do każdego joba.
- Hipotezy do pomiaru w M-INF:
  - tok/s dla każdej klasy profilu;
  - czas ładowania z NVMe i z page cache;
  - zysk z `--parallel` przy Stage 1.

## Odrzucone warianty
- vLLM od początku: wymaga WSL2 lub Dockera, a przewaga ujawnia się dopiero przy dużej równoległości jednego modelu.
- Ollama jako MVP: podwójny scheduler i słabsza kontrola fingerprintu. Zostaje wariantem awaryjnym przez ten sam
  adapter OpenAI-compatible.
