# Definition of Done: M-INF0 (korekta architektury inferencji)

Każdy punkt wskazuje miejsce, które go spełnia. Linki sprawdza `tests/test_continuity.py`.

| # | Kryterium | Gdzie |
|---|---|---|
| 1 | self-hosted inference działa na osobnym PC w LAN | [ADR-0015](adr/ADR-0015-self-hosted-inference-wezel-lan.md), [NODE §2](inference/NODE.md#architektura) |
| 2 | węzeł RTX 3090 jest wymienialnym workerem obliczeniowym | [ADR-0015](adr/ADR-0015-self-hosted-inference-wezel-lan.md), [NODE §7](inference/NODE.md#zrodlo-prawdy) |
| 3 | GLU nie zakłada localhost | [INFERENCE-ROUTING §3](INFERENCE-ROUTING.md#3-abstrakcja-providera), [GLU §5](GLU.md#5-wykonanie-self-hosted-a-sesja-premium), [NODE §1](inference/NODE.md#definicja) |
| 4 | WGC nie zna infrastruktury inferencji | [ARCHITECTURE §1](ARCHITECTURE.md#1-warstwy), [NODE §2 (tabela warstw)](inference/NODE.md#architektura), [DATA-CONTRACTS §1](DATA-CONTRACTS.md#1-rejestr-kontraktów) |
| 5 | istnieje remote self-hosted provider | [INFERENCE-ROUTING §3](INFERENCE-ROUTING.md#3-abstrakcja-providera) (`self_hosted`), [ROADMAP M10](ROADMAP.md#m10-providerzy-fakereplayself_hosted--pętla-structured-output) |
| 6 | istnieje koncepcja Inference Gateway | [ADR-0016](adr/ADR-0016-inference-gateway-i-protokol.md), [NODE §3](inference/NODE.md#bramka), `contracts/schemas/inference.schema.json` |
| 7 | backend runtime jest wymienialny | [ADR-0016](adr/ADR-0016-inference-gateway-i-protokol.md) (OpenAI-compatible tylko bramka → runtime), [ADR-0018](adr/ADR-0018-runtime-mvp-llama-cpp-windows.md) |
| 8 | strategia Windows/WSL jest określona | [ADR-0018](adr/ADR-0018-runtime-mvp-llama-cpp-windows.md), [DEPLOYMENT §5](inference/DEPLOYMENT.md#wsl2) |
| 9 | networking jest częścią architektury | [DEPLOYMENT §3](inference/DEPLOYMENT.md#siec), [NODE §8](inference/NODE.md#awarie) |
| 10 | security jest częścią architektury | [NODE §7](inference/NODE.md#zrodlo-prawdy), [ARCHITECTURE §6](ARCHITECTURE.md#6-bezpieczeństwo-skrót) |
| 11 | node health i capabilities są dostępne | [NODE §3](inference/NODE.md#bramka), `contracts/fixtures/valid/igw.api.yaml` |
| 12 | model lifecycle jest zaprojektowany | [NODE §5](inference/NODE.md#scheduler) |
| 13 | jedna RTX 3090 ma kontrolowany scheduler i kolejkę | [NODE §5](inference/NODE.md#scheduler), [ROADMAP M-GW2](ROADMAP.md#m-gw2-scheduler-cykl-życia-modeli-telemetria-gpu-igw-doctor) |
| 14 | brak węzła nie powoduje automatycznego premium fallback | [ADR-0017](adr/ADR-0017-niedostepnosc-wezla-bez-premium-fallback.md), [INFERENCE-ROUTING §2 (reguła 12)](INFERENCE-ROUTING.md#2-polityka-routingu-routing0-do-implementacji-w-m12) |
| 15 | premium fallback wymaga jawnej polityki | `contracts/schemas/glu.schema.json` (`fallback_policy`, `premium_reason`), `contracts/fixtures/invalid/glu.premium_without_reason.yaml` |
| 16 | limit 2× dotyczy wyłącznie premium LLM | [COST §2](COST.md#2-ograniczenie) |
| 17 | self-hosted compute może być używany agresywnie | [COST §2](COST.md#2-ograniczenie), [INFERENCE-ROUTING §5](INFERENCE-ROUTING.md#self-hosted) |
| 18 | lokalny multi-pass jest dozwolony | [ADR-0017](adr/ADR-0017-niedostepnosc-wezla-bez-premium-fallback.md), [INFERENCE-ROUTING §2 (reguła 11)](INFERENCE-ROUTING.md#2-polityka-routingu-routing0-do-implementacji-w-m12) |
| 19 | profile providerów i modeli pozostają wymienialne | [INFERENCE-ROUTING §4](INFERENCE-ROUTING.md#4-profile-modeli), [NODE §4](inference/NODE.md#profile) |
| 20 | Stage 1/1.5/2/3 mogą korzystać z self-hosted compute | [DIGITALIZATION](DIGITALIZATION.md#self-hosted-stage-1-5), [EDITORIAL-PUBLICATION](EDITORIAL-PUBLICATION.md#self-hosted-stage-2-3), [INFERENCE-ROUTING §1](INFERENCE-ROUTING.md#1-tiery-wykonania) |
| 21 | source of truth nadal jest poza węzłem | [NODE §7](inference/NODE.md#zrodlo-prawdy), [ADR-0004](adr/ADR-0004-zrodlo-prawdy-i-stan-wykonania.md) |
| 22 | repo zawiera roadmapę wdrożenia | [ROADMAP: kolejność](ROADMAP.md#kolejnosc), [ROADMAP: Faza 1b](ROADMAP.md#faza-1b-self-hosted-inference-węzeł-w-lan) |
| 23 | kolejna sesja wie dokładnie, co implementować | [STATUS: następny milestone](STATUS.md#nastepny-milestone), [handoff M-INF0](handoff/2026-10-05-M-INF0.md) |
