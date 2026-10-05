# wargame-compiler

Kontrolowany **kompilator instrukcji gier wojennych**: od PDF-u wydawcy przez kanoniczny model logiki gry do
specyfikacji silnika gry (z testami) oraz do wiernego wydania w innym języku w oprawie oryginału.

```text
SOURCE → Stage 1 LOGIC ──┬──→ Stage 1.5 DIGITALIZATION → engine spec + testy
                         └──→ Stage 2 EDITORIAL → Stage 3 TRANSLATION / PUBLICATION → LaTeX / PDF
```

- **WGC** (pakiet `wgc`): domena: kontrakty, Knowledge Base, walidatory, narzędzia deterministyczne.
- **GLU** (pakiet `glu`): wykonanie: joby, routing kod → lokalny LLM → premium LLM → człowiek, cache, przyrostowość, CLI i MCP.
- Knowledge Base w repo gry jest źródłem prawdy. Repozytorium narzędzia jest pamięcią projektu.

> **Status:** Session 0 zakończona: architektura, kontrakty `@0`, roadmapa, system ciągłości. Kod domenowy zaczyna się
> od M1. Zob. [docs/STATUS.md](docs/STATUS.md).

Następca narzędzia `wargame_utils` (`wgu`), budowany od zera (ADR-0001). Oba mogą działać obok siebie (ADR-0002).

## Szybki start (deweloper)
```bash
python -m pip install -r requirements.txt pytest
```
```bash
python -m pytest
```

## Dokumentacja
| Dokument | Po co |
|---|---|
| [CLAUDE.md](CLAUDE.md) | bootstrap dla sesji AI |
| [docs/STATUS.md](docs/STATUS.md) | stan, bieżący i następny milestone, otwarte kwestie |
| [docs/HANDOFF.md](docs/HANDOFF.md) | ostatnie przekazanie pracy |
| [docs/SESSION-PLAYBOOK.md](docs/SESSION-PLAYBOOK.md) | jak prowadzić sesję, role modeli, rozmiar sesji |
| [docs/ROADMAP.md](docs/ROADMAP.md) | milestone'y M0–M28 |
| [docs/VISION.md](docs/VISION.md) | wizja i zasady |
| [docs/ARCHAEOLOGY.md](docs/ARCHAEOLOGY.md) | co istniało, lekcje, analiza luk |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | warstwy, granica WGC ↔ GLU, repozytoria |
| [docs/PIPELINE.md](docs/PIPELINE.md) | etapy, kontrakty etapów, bramki i statusy, śledzenie |
| [docs/LOGIC-MODEL.md](docs/LOGIC-MODEL.md) | Stage 0/1, Rule IR, provenance, model ryzyka |
| [docs/DIGITALIZATION.md](docs/DIGITALIZATION.md) | Stage 1.5: stan, akcje, legalność, zdarzenia, timing, losowość, testy |
| [docs/EDITORIAL-PUBLICATION.md](docs/EDITORIAL-PUBLICATION.md) | Stage 2 i Stage 3 |
| [docs/GLU.md](docs/GLU.md) | orkiestracja, joby, cache, przyrostowość |
| [docs/INFERENCE-ROUTING.md](docs/INFERENCE-ROUTING.md) | tiery, routing, providerzy, lokalna inferencja |
| [docs/MCP.md](docs/MCP.md) | MCP, Claude Desktop, bezpieczeństwo |
| [docs/DATA-CONTRACTS.md](docs/DATA-CONTRACTS.md) | schematy, ID, hashe, wersjonowanie |
| [docs/QUALITY.md](docs/QUALITY.md) | model jakości, mutacje, benchmarki |
| [docs/COST.md](docs/COST.md) | model kosztu, baseline, obserwowalność |
| [docs/adr/](docs/adr/README.md) | decyzje architektoniczne |
| [docs/DOD-SESSION-0.md](docs/DOD-SESSION-0.md) | spełnienie Definition of Done Session 0 |

## Układ repo
```text
contracts/schemas/     JSON Schema kontraktów (wgc/*@0, glu/exec@0)
contracts/fixtures/    przykłady poprawne (valid/) i niepoprawne (invalid/)
wgc/                   domena (dziś: rejestr kontraktów)
glu/                   wykonanie (pusty do M8)
bench/minigame/        gra benchmarkowa Drill Skirmish (CC0)
docs/                  dokumentacja, ADR, handoffy
tests/                 testy kontraktów i ciągłości
```

Tłumaczenia i materiały tworzone narzędziem są nieoficjalne. Teksty wydawców nie trafiają do tego repozytorium.
