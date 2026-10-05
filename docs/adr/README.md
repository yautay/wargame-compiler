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
| [ADR-0014](ADR-0014-provenance-nadawana-deterministycznie.md) | Rodzaj provenance nadaje WGC, nie model | przyjęty (obniżenie niepotwierdzonej kotwicy do `llm_inference` zastąpione przez ADR-0027) |
| [ADR-0015](ADR-0015-self-hosted-inference-wezel-lan.md) | Self-hosted inference na osobnym węźle w LAN (`local` = self-hosted) | przyjęty |
| [ADR-0016](ADR-0016-inference-gateway-i-protokol.md) | Inference Gateway (`igw`) i protokół `igw/api@0` | przyjęty |
| [ADR-0017](ADR-0017-niedostepnosc-wezla-bez-premium-fallback.md) | Niedostępność węzła nie eskaluje do premium; self-hosted jako zasób obfity | przyjęty (rola `local_deep` doprecyzowana przez ADR-0028) |
| [ADR-0018](ADR-0018-runtime-mvp-llama-cpp-windows.md) | Runtime MVP: llama.cpp natywnie na Windows; vLLM w WSL2 po benchmarku | przyjęty |
| [ADR-0019](ADR-0019-wiele-dokumentow-w-pliku-yaml.md) | Plik YAML może zawierać wiele dokumentów, każdy z własnym kontraktem | przyjęty |
| [ADR-0020](ADR-0020-inwentarz-i-segmentacja-stage0.md) | Inwentarz Stage 0, segmentacja Markdown, ID segmentów i domyślne pierwszeństwo źródeł | przyjęty |
| [ADR-0021](ADR-0021-ingest-pdf-biblioteka-i-segmentacja.md) | Ingest PDF na bibliotekach o licencjach liberalnych (pdfplumber, pypdfium2), segmentacja PDF i flagi wizualne | przyjęty |
| [ADR-0022](ADR-0022-glu-natywnie-na-windows.md) | GLU na dev machine działa natywnie na Windows (Q-03) | przyjęty |
| [ADR-0023](ADR-0023-job-store-sqlite-i-maszyna-stanow.md) | Job store GLU w SQLite (`.glu/state.db`, migracje przez `user_version`) i maszyna stanów joba i buildu jako tabela | przyjęty |
| [ADR-0024](ADR-0024-separator-komorek-tabel-w-tekscie-segmentu.md) | Komórki tabel w tekście segmentu rozdziela tabulator, bez zmiany wersji ekstraktorów | przyjęty |
| [ADR-0025](ADR-0025-taskspec-accept-i-wykonawca-tier0.md) | TaskSpec jako interfejs Pythona, `accept()` jako jedyny zapis do `kb/`, wykonawca Tier 0 i planner | przyjęty |
| [ADR-0026](ADR-0026-atomowy-zapis-i-blokada-pisarza-kb.md) | Atomowy zapis pliku KB i blokada pisarza projektu wokół całego `accept()` | przyjęty |
| [ADR-0027](ADR-0027-autorytet-rol-zrodel-i-niepotwierdzone-kotwice.md) | Automatyczna akceptacja tylko z ról kanonicznych; niepotwierdzona kotwica to odrzucenie, nie inferencja | przyjęty |
| [ADR-0028](ADR-0028-local-deep-bez-prawa-akceptacji.md) | `local_deep` bez prawa akceptacji w `routing@0`; spór i reguły `forced` zawsze idą do premium | przyjęty |
| [ADR-0029](ADR-0029-przeklad-premium-weryfikacja-lokalna.md) | Przekład Stage 3 pisze premium; wierność sprawdzają wykonawcy niezależni od tłumacza | przyjęty |
