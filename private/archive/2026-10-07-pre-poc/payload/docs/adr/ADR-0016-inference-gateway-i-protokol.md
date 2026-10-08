# ADR-0016: Inference Gateway (`igw`) i protokół `igw/api@0`

- **Status:** przyjęty (zastępuje ADR-0009)
- **Data:** 2026-10-05
- **Milestone:** M-INF0

## Kontekst
- ADR-0009 przewidywał w GLU jeden adapter `openai_compat` łączący się wprost z vLLM, llama.cpp lub Ollamą. Przy
  węźle w LAN (ADR-0015) zabrakło warstwy, która:
  - zarządza kolejką, VRAM i ładowaniem modeli dla wszystkich klientów;
  - autoryzuje i ogranicza requesty;
  - raportuje health, capabilities i metryki;
  - podaje tożsamość modelu (`model_fingerprint`) potrzebną dla cache.
- Runtime'y różnią się wsparciem structured output. llama.cpp zamienia JSON Schema na gramatykę bez `if/then/else`
  i bez `not`, a nieobsługiwane cechy pomija po cichu.

## Decyzja
- **Inference Gateway** to cienki serwis HTTP na węźle, trzeci pakiet repo: **`igw`** (Python, FastAPI i uvicorn jako
  zależność opcjonalna `[node]`, dodawana w M-GW1).
  - `igw` nie importuje `wgc` ani `glu`, a `glu` nie importuje `igw`. Łączy je tylko HTTP i kontrakt `igw/api@0`
    (`contracts/schemas/inference.schema.json`). Rejestr `wgc.contracts` ładuje ten schemat wyłącznie na potrzeby
    testów kontraktów.
  - Zadania: przyjmowanie i walidacja requestów, mapowanie profilu węzła na model, kolejka, scheduler i cykl życia
    modeli, structured output, health, capabilities i metryki, autoryzacja i limity.
  - Nie robi: logiki domenowej, cache wyników, trwałego stanu jobów, wykonywania poleceń.
- **Protokół** HTTP(S) i JSON, wersjonowany w ścieżce `/v1`:

  | Endpoint | Rola |
  |---|---|
  | `GET /healthz` | bez autoryzacji, tylko status |
  | `GET /v1/health` | stan węzła |
  | `GET /v1/capabilities` | możliwości węzła |
  | `GET /v1/models` | profile węzła i ich `model_fingerprint` |
  | `POST /v1/infer` | synchroniczny |
  | `POST /v1/embed` | opcjonalny |
  | `GET /v1/metrics` | JSON |

  `/v1/jobs` (async) i SSE są zarezerwowane na M-GW3 i powstaną tylko wtedy, gdy wymagają tego długie joby `local_deep`.
  WebSocket jest poza zakresem.
- Request jest **generyczny**: profil węzła, wiadomości, tryb wyjścia (`json_schema`, `json_object`, `text`)
  i schemat dekodowania, parametry, `deadline_s`, `idempotency_key`, nieprzezroczysty `client_ref`. Pola domenowe są
  zabronione (`additionalProperties: false`).
- **Trwałą kolejką jest job store GLU** (SQLite, M8). Kolejka bramki żyje w pamięci i deduplikuje requesty w toku
  po `idempotency_key`. Restart bramki = ponowne wysłanie przez GLU (joby są idempotentne).
- **OpenAI-compatible jest kontraktem między bramką a runtime'em** (adapter runtime'u), nie między GLU a bramką.
  Runtime da się wymienić bez zmian w GLU.
- **Providerzy GLU:** `fake`, `replay`, `self_hosted` (klient `igw/api@0`) i `anthropic`. `openai_compat` w GLU odpada.
  Zostają profile (`local_fast`, `local_semantic`, `local_deep`, `premium_semantic`…):
  - GLU mapuje profil logiczny na endpoint i profil węzła w `~/.config/glu/profiles.yaml`;
  - węzeł mapuje profil węzła na model w swoim `node.yaml`.
- **Tożsamość modelu (`model_fingerprint`) pochodzi z węzła** (`/v1/models` i każdy `infer_result`). Obejmuje hash
  pliku modelu, kwantyzację, runtime i parametry uruchomienia wpływające na wynik, ale **nie** host, IP ani `node_id`.
  Klucz cache GLU używa `profile_fingerprint` = hash(`model_fingerprint` raportowany przez węzeł, `node_profile`, parametry próbkowania i wyjścia z `profiles.yaml`).
- Zadanie WGC może podać `decoding_schema` (płaski podzbiór JSON Schema zgodny z `capabilities.json_schema_subset`).
  Pełna walidacja schematem i domeną zostaje po stronie GLU i WGC.

## Konsekwencje
- Zmiana modelu na węźle zmienia fingerprint, więc cache nie zwróci starego wyniku. Wymiana węzła na inny z tym samym
  modelem zachowuje trafienia.
- Aktualizacja runtime'u zmienia fingerprint (wynik może się zmienić). Wersję runtime'u przypina się na węźle.
- Testy bramki (`fastapi.testclient`) i providera (transport w pamięci) działają bez sieci i GPU.

## Odrzucone warianty
- GLU → runtime bezpośrednio: patrz Kontekst.
- Pełny schemat OpenAI jako kontrakt GLU: szeroki, zmienny i nie przenosi fingerprintu, kolejki ani błędów dostępności.
- Kolejka RabbitMQ, Redis lub Kafka: przy 1 węźle i kilku klientach wystarczy SQLite GLU i kolejka w pamięci bramki.
