# Architektura

Dokument opisuje warstwy, granice i układ repozytoriów. Szczegóły: etapy w [PIPELINE.md](PIPELINE.md), wykonanie
w [GLU.md](GLU.md), kontrakty w [DATA-CONTRACTS.md](DATA-CONTRACTS.md).

## 1. Warstwy

```text
                 ┌──────────────── interfaces ────────────────┐
                 │  CLI (wgc, glu)   MCP server   (future API)  │   adaptery: parsują wejście, wołają usługi,
                 └──────────────────────┬──────────────────────┘   formatują wyjście; zero logiki domenowej
                                        │
                 ┌──────────────────── GLU core ───────────────────┐
                 │ build planner · job store · scheduler · router    │   wykonanie, nie wiedza
                 │ executors (deterministic | local | premium |      │
                 │ human) · providers · cache · dependency graph ·   │
                 │ metrics ledger                                    │
                 └──────────────────────┬──────────────────────────┘
                                        │ TaskSpec, validate(), accept()
                 ┌──────────────────── WGC (domain) ─────────────────┐
                 │ contracts (JSON Schema) · KB store · validators     │   wiedza i jej reguły
                 │ (schema, refs, provenance, cues) · risk model ·     │
                 │ gates · deterministic tools (ingest, tables, terms) │
                 │ · task specs (prompts, output schemas, context      │
                 │ builders) · views · exporters (engine kit, LaTeX)   │
                 └──────────────────────┬──────────────────────────┘
                                        │ read/write YAML
                 ┌──────────────── game project repo ────────────────┐
                 │ project.yaml · source/inventory.yaml · kb/ ·        │   źródło prawdy (git)
                 │ publication/ · reports/ · .glu/ (gitignored)        │
                 └─────────────────────────────────────────────────────┘
```

Kierunek zależności: `interfaces → glu → wgc → contracts`. Pakiet `wgc` nie importuje `glu`. GLU nie zna pojęć gry.
Wykonuje `TaskSpec` zarejestrowane przez WGC i zapisuje wyniki wyłącznie przez `wgc.accept()`.

## 2. Granica WGC ↔ GLU
| Pytanie | WGC (domena) | GLU (wykonanie) |
|---|---|---|
| Co jest regułą, relacją, akcją? | ✔ | ✘ |
| Jak wygląda poprawny wynik zadania? | ✔ schemat wyjścia + walidator domenowy | ✘ |
| Jaki kontekst dostaje model? | ✔ `context_builder` zadania (rekordy, sąsiedztwo w grafie) | pakuje i wysyła |
| Jakie jest ryzyko rekordu? | ✔ `wgc/risk@N` (deterministycznie) | czyta jako sygnał |
| Kto wykona job (tier, profil)? | ✘ | ✔ polityka routingu |
| Retry, eskalacja, budżet, kolejka? | ✘ | ✔ |
| Cache, klucze, przyrostowość? | dostarcza projekcje semantyczne i hashe | ✔ graf zależności, invalidacja |
| Zapis do KB | ✔ `accept()` z provenance | woła `accept()`, nigdy nie pisze YAML sam |
| Statusy etapów | ✔ `wgc gate` | czyta, planuje buildy |

**TaskSpec** (kontrakt WGC → GLU, kształtowany w M9): `id`, `version`, `stage`, `input_selector` (które rekordy lub
segmenty), `context_builder`, `prompt` (id@wersja), `output_schema`, `deterministic_impl?` (Tier 0), `validate(output)
→ issues`, `risk_features(output)`, `accept(output) → records`, `semantic_projection` (co z wejścia wpływa na wynik).

## 3. Komponenty
| Komponent | Pakiet | Opis | Milestone |
|---|---|---|---|
| Rejestr kontraktów | `wgc.contracts` | schematy `contracts/schemas/*.schema.json`, walidacja dokumentów | M0 (jest) |
| Tożsamość i hashowanie | `wgc.ids`, `wgc.canonical` | gramatyka ID, kanoniczny JSON, projekcje semantyczne | M1 |
| Walidator | `wgc.validate` | L0 schemat, L1 referencje, L2 provenance i sygnały | M1, M5 |
| Ingest źródeł | `wgc.source` | inwentarz, segmentacja, render, flagi wizualne | M2 |
| Model ryzyka | `wgc.risk` | cechy, wagi, klasy, twarde reguły | M6 |
| Bramki | `wgc.gate` | obliczane statusy etapów | M7 |
| Job store | `glu.store` | SQLite: build, job, attempt, routing_decision | M8 |
| Wykonawcy | `glu.exec` | deterministic, local, premium, human | M9–M16 |
| Providerzy | `glu.providers` | fake, replay, openai_compat, anthropic | M10, M15 |
| Cache | `glu.cache` | bloby adresowane treścią + indeks | M11 |
| Router | `glu.routing` | polityka `routing@N`, decyzje z uzasadnieniem | M12 |
| Graf zależności | `glu.graph` (z danymi od `wgc`) | stale, early cutoff | M13 |
| Eksport silnika | `wgc.export.engine` | engine kit + wyniki testów zwrotnie | M20 |
| MCP | `glu.interfaces.mcp` | adapter, najmniejsze uprawnienia | M22–M23 |
| Publikacja | `wgc.publish` | LaTeX z API makr, styl z pomiaru oprawy | M27 |

## 4. Repozytoria
**Repo narzędzia** (`wargame-compiler`): kod, kontrakty, benchmark z tekstów własnych, dokumentacja, ADR.
Nie zawiera niczego, co dotyczy jednej konkretnej gry komercyjnej.

**Repo gry** (jedno na grę i wydanie):
```text
<gra>/
├── project.yaml                 wgc/project@0: gra, języki, warstwy glosariusza, polityki bramek i routingu
├── source/inventory.yaml        SRC- i SEG- (bez tekstu), commitowane
├── private/                     PDF-y źródeł (gitignored, jeśli repo jest publiczne)
├── kb/
│   ├── logic/                   Stage 1: concepts/, rules/<rozdział>.yaml, relations, tables, procedures,
│   │                            ambiguities, interpretations, cases, changes
│   ├── decisions.yaml           HD- (tylko dopisywanie)
│   ├── reviews.yaml             RR- (prośby z etapów niższych)
│   ├── digital/                 Stage 1.5 (wgc/digital@0)
│   ├── editorial/               Stage 2
│   └── publication/<lang>/      Stage 3: glosariusz gry, polityka przekładu, przekłady segmentów
├── publication/<lang>/          wygenerowany LaTeX, styl, PDF (artefakty)
├── reports/                     generowane raporty bramek, pokrycia, śledzenia (z --check)
└── .glu/                        stan wykonania, cache, tekst segmentów (gitignored)
```
**Repo silnika** (opcjonalne, dowolna technologia) przypina wersję `engine kit` i odsyła wyniki testów (`engine-results.json`).

## 5. Interfejsy
- `wgc …`: polecenia domenowe, deterministyczne (validate, gate, view, export, ingest).
- `glu …`: build, status, queue, review, decide, stats, cache.
- MCP: te same usługi co CLI, z listą dozwolonych narzędzi ([MCP.md](MCP.md)).
- Skille Claude Code (opcjonalnie): cienkie nakładki wołające `glu`/`wgc`. Nie przechowują wiedzy.

## 6. Bezpieczeństwo (skrót)
Najmniejsze uprawnienia (allowlista katalogów projektów, zakresy odczytu i zapisu, allowlista podprocesów,
dozwolone endpointy lokalne), sekrety tylko ze zmiennych środowiska lub keyringu, redakcja logów, brak tekstu źródła
w commitach. Szczegóły: [MCP.md](MCP.md#bezpieczenstwo).

## 7. Granice przyszłego silnika
Opisane w [DIGITALIZATION.md](DIGITALIZATION.md#granice-silnika). Silnik nie jest częścią tego repo.
