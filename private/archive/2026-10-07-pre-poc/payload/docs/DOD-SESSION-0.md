# Definition of Done: Session 0 (§52 promptu)

Każdy punkt wskazuje miejsce, które go spełnia. Test `tests/test_continuity.py` sprawdza, że każdy link (plik
i kotwica) istnieje.

| # | Kryterium | Gdzie |
|---|---|---|
| 1 | istniejący projekt został rzeczywiście przeanalizowany | [ARCHAEOLOGY §1](ARCHAEOLOGY.md#1-co-istnieje-faza-a) |
| 2 | znane są mechanizmy, które można wykorzystać | [ARCHAEOLOGY §4](ARCHAEOLOGY.md#4-mechanizmy-do-ponownego-wykorzystania-idee-nie-kod), [analiza luk](ARCHAEOLOGY.md#3-analiza-luk-faza-b) |
| 3 | istnieje docelowa architektura | [ARCHITECTURE §1](ARCHITECTURE.md#1-warstwy), [VISION](VISION.md) |
| 4 | Stage 1 jest jasno zdefiniowany | [LOGIC-MODEL: Rule IR](LOGIC-MODEL.md#rule-ir), [kontrakt Source → Logic](PIPELINE.md#11-source--logic-stage-0--stage-1), `contracts/schemas/logic.schema.json` |
| 5 | Stage 1.5 jest jasno zdefiniowany | [DIGITALIZATION: zasady](DIGITALIZATION.md#zasady), `contracts/schemas/digital.schema.json` |
| 6 | Stage 2 jest oddzielony od logiki | [Stage 2](EDITORIAL-PUBLICATION.md#stage-2-model-redakcyjny), [kontrakt Logic → Editorial](PIPELINE.md#13-logic--editorial-stage-1--stage-2) |
| 7 | Stage 3 jest oddzielony od analizy | [Stage 3](EDITORIAL-PUBLICATION.md#stage-3-przekład-i-publikacja), [kontrakt → Publication](PIPELINE.md#14-logic--editorial--publication-stage-1--2--stage-3) |
| 8 | digitalizacja zależy wyłącznie od Stage 1 | [kontrakt Logic → Digitalization](PIPELINE.md#12-logic--digitalization-stage-1--stage-15), [bramki](PIPELINE.md#wymagania-wejściowe-bramki) |
| 9 | istnieje kierunek modelu state/action/legality/event | [State](DIGITALIZATION.md#state-model-schemat-stanu), [Action](DIGITALIZATION.md#action-model-katalog-akcji), [Legality](DIGITALIZATION.md#legality-model), [Event](DIGITALIZATION.md#event-model), [ADR-0007](adr/ADR-0007-referencyjny-ksztalt-silnika.md) |
| 10 | istnieje traceability source → engine test | [Rule Traceability](DIGITALIZATION.md#sledzenie-regul), [PIPELINE §3](PIPELINE.md#3-śledzenie-traceability) |
| 11 | znana jest granica WGU ↔ GLU | [ARCHITECTURE §2](ARCHITECTURE.md#2-granica-wgc--glu), [ADR-0002](adr/ADR-0002-nazwy-i-pakiety.md) |
| 12 | MCP jest adapterem, nie core | [MCP: rola](MCP.md#rola), [ADR-0013](adr/ADR-0013-mcp-adapter-premium-dwie-drogi.md) |
| 13 | istnieje local inference strategy | [INFERENCE-ROUTING §5](INFERENCE-ROUTING.md#self-hosted), [inference/NODE.md](inference/NODE.md), [ADR-0015](adr/ADR-0015-self-hosted-inference-wezel-lan.md) (zastąpiła [ADR-0008](adr/ADR-0008-srodowisko-wsl2.md) i [ADR-0009](adr/ADR-0009-providerzy-i-profile.md) w M-INF0) |
| 14 | istnieje routing strategy | [INFERENCE-ROUTING §2](INFERENCE-ROUTING.md#2-polityka-routingu-routing0-do-implementacji-w-m12), [ADR-0010](adr/ADR-0010-routing-asymetryczny.md) |
| 15 | istnieje cache strategy | [GLU §6](GLU.md#6-cache) |
| 16 | istnieje incremental strategy | [GLU §7](GLU.md#przyrostowosc), [PIPELINE §4](PIPELINE.md#4-przyrostowość-między-etapami) |
| 17 | istnieje provenance model | [LOGIC-MODEL: provenance](LOGIC-MODEL.md#provenance), [ADR-0014](adr/ADR-0014-provenance-nadawana-deterministycznie.md) |
| 18 | istnieje cost model | [COST](COST.md#3-model-szacunkowy), [baseline](COST.md#1-baseline-10-jak-go-zmierzyć) |
| 19 | istnieje quality model | [QUALITY §1–3](QUALITY.md#1-drabina-walidacji), [model ryzyka](LOGIC-MODEL.md#model-ryzyka) |
| 20 | istnieje logic benchmark | [QUALITY: Logic](QUALITY.md#logic), `bench/minigame/rulebook.md`, `bench/minigame/phenomena.yaml` |
| 21 | istnieje digitalization benchmark | [QUALITY: Digitalization](QUALITY.md#digitalization) |
| 22 | istnieje editorial/translation benchmark | [QUALITY: Editorial](QUALITY.md#editorial), [QUALITY: Translation](QUALITY.md#translation) |
| 23 | istnieje roadmap | [ROADMAP](ROADMAP.md) |
| 24 | roadmap jest rozbita na małe sesje | [ROADMAP: M1](ROADMAP.md#m1-tożsamość-hashowanie-i-walidator-referencji), [rozmiar sesji](SESSION-PLAYBOOK.md#rozmiar-sesji) |
| 25 | istnieje project continuity system | [SESSION-PLAYBOOK](SESSION-PLAYBOOK.md#procedura-sesji-8-kroków), [STATUS](STATUS.md), [HANDOFF](HANDOFF.md), [ADR](adr/README.md), `tests/test_continuity.py` |
| 26 | kolejna sesja może zacząć bez znajomości historii rozmowy | `CLAUDE.md` (bootstrap), [HANDOFF](HANDOFF.md), [handoff M0](handoff/2026-10-05-M0.md) |
| 27 | wiadomo dokładnie, co zrobić jako następny milestone | [STATUS: następny milestone](STATUS.md#nastepny-milestone) |
