# Rejestr decyzji architektonicznych (ADR)

ADR zapisuje decyzję, jej kontekst i konsekwencje. Rejestr tylko się dopisuje: decyzję zmienia nowy ADR ze statusem
`zastępuje ADR-NNNN`, a stary dostaje status `zastąpiony`. Szablon: [TEMPLATE.md](TEMPLATE.md).
Decyzje domenowe konkretnej gry (interpretacje, terminologia) nie są ADR-ami. To rekordy `HD-…` w repo gry.

| ADR | Tytuł | Status |
|---|---|---|
| [ADR-0001](ADR-0001-czysty-start.md) | Czysty start: nowe repo, bez kompatybilności wstecznej | przyjęty |
| [ADR-0002](ADR-0002-nazwy-i-pakiety.md) | Nazwy: `wargame-compiler`, pakiety `wgc` i `glu` | przyjęty |
| [ADR-0003](ADR-0003-model-logiki-niezalezny-od-jezyka.md) | Model logiki niezależny od języka docelowego | przyjęty |
| [ADR-0004](ADR-0004-zrodlo-prawdy-i-stan-wykonania.md) | KB w git jako źródło prawdy, stan wykonania w `.glu/` | przyjęty |
| [ADR-0005](ADR-0005-wyjatki-tylko-w-relacjach.md) | Wyjątki i nadpisania wyłącznie w relacjach | przyjęty |
| [ADR-0006](ADR-0006-digitalizacja-jako-specyfikacja.md) | Stage 1.5 to specyfikacja i testy, nie wykonywalny DSL reguł | przyjęty |
| [ADR-0007](ADR-0007-referencyjny-ksztalt-silnika.md) | Referencyjny kształt silnika: decyzje → zdarzenia → reduktor | przyjęty |
| [ADR-0008](ADR-0008-srodowisko-wsl2.md) | Runtime WSL2, core wieloplatformowy, testy bez GPU | zastąpiony przez ADR-0015 |
| [ADR-0009](ADR-0009-providerzy-i-profile.md) | Jeden adapter lokalny (OpenAI-compatible) i profile modeli | zastąpiony przez ADR-0016 |
| [ADR-0010](ADR-0010-routing-asymetryczny.md) | Routing asymetryczny oparty na deterministycznym ryzyku | przyjęty |
| [ADR-0011](ADR-0011-statusy-obliczane.md) | Statusy i widoki są obliczane, nie edytowane | przyjęty |
| [ADR-0012](ADR-0012-tekst-zrodla-poza-repo.md) | Tekst źródła poza repozytoriami, kotwice z hashami | przyjęty |
| [ADR-0013](ADR-0013-mcp-adapter-premium-dwie-drogi.md) | MCP jako adapter; premium review przez API albo Claude Desktop | przyjęty |
| [ADR-0014](ADR-0014-provenance-nadawana-deterministycznie.md) | Rodzaj provenance nadaje WGC, nie model | przyjęty |
| [ADR-0015](ADR-0015-self-hosted-inference-wezel-lan.md) | Self-hosted inference na osobnym węźle w LAN (`local` = self-hosted) | przyjęty |
| [ADR-0016](ADR-0016-inference-gateway-i-protokol.md) | Inference Gateway (`igw`) i protokół `igw/api@0` | przyjęty |
| [ADR-0017](ADR-0017-niedostepnosc-wezla-bez-premium-fallback.md) | Niedostępność węzła nie eskaluje do premium; self-hosted jako zasób obfity | przyjęty |
| [ADR-0018](ADR-0018-runtime-mvp-llama-cpp-windows.md) | Runtime MVP: llama.cpp natywnie na Windows; vLLM w WSL2 po benchmarku | przyjęty |
