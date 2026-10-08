# ADR-0009: Jeden adapter lokalny (OpenAI-compatible) i profile modeli

- **Status:** zastąpiony przez ADR-0016
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
vLLM, llama.cpp server, Ollama i LM Studio wystawiają API zgodne z OpenAI. Różnią się wsparciem structured output
(guided JSON, gramatyki, `response_format`). Nazwy modeli szybko się dezaktualizują.

## Decyzja
- Interfejs `Provider` w `glu.providers`: `generate(request) → result` (schemat wyjścia, limity, metadane kosztu).
- Implementacje na start: `fake`, `replay`, `openai_compat` (serwery lokalne) i `anthropic` (premium).
- Domena i polityki routingu używają wyłącznie **profili** (`local_fast`, `local_semantic`, `premium_semantic`…).
  Mapowanie profilu na providera, model, kwantyzację i parametry żyje w konfiguracji użytkownika
  (`~/.config/glu/profiles.yaml`). Jego odcisk (`profile_fingerprint`) wchodzi do klucza cache.
- Serwer i modele wybiera benchmark (milestone M-INF), nie ten ADR.

## Konsekwencje
Zmiana modelu to zmiana konfiguracji i nowy fingerprint, bez zmian w kodzie domeny. Cache nie pomyli wyników
różnych modeli.
