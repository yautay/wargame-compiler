# Architektura

Dokument opisuje warstwy, granice i układ repozytoriów. Szczegóły: etapy w [PIPELINE.md](PIPELINE.md), wykonanie
w [GLU.md](GLU.md), kontrakty w [DATA-CONTRACTS.md](DATA-CONTRACTS.md), self-hosted inference w
[inference/NODE.md](inference/NODE.md).

## 1. Warstwy

```text
 DEV MACHINE (Claude Desktop, GLU, repo gier)                         INFERENCE NODE (osobny PC w LAN)
 ┌──────────────── interfaces ────────────────┐
 │  CLI (wgc, glu)   MCP server   (future API)  │  adaptery: zero logiki domenowej
 └──────────────────────┬──────────────────────┘
                        │
 ┌──────────────────── GLU core ───────────────────┐
 │ build planner · job store (trwała kolejka) ·      │   wykonanie, nie wiedza
 │ router · fallback policy · executors              │
 │ (deterministic | local=self-hosted | premium |    │
 │ human) · cache · dependency graph · metrics       │
 ├──────────── provider abstraction ────────────────┤  HTTPS igw/api@0   ┌──────────────────────────────┐
 │ fake · replay · self_hosted ──────────────────────┼─────────────────► │ igw: Inference Gateway        │
 │ anthropic · desktop_pull ──► premium (API / MCP)  │   token + TLS     │  auth · kolejka · scheduler · │
 └──────────────────────┬──────────────────────────┘                    │  lifecycle · health · metrics │
                        │ TaskSpec, validate(), accept()                │      ↓ runtime adapter        │
 ┌──────────────────── WGC (domain) ─────────────────┐                  │ llama.cpp / vLLM (127.0.0.1)  │
 │ contracts (JSON Schema) · KB store · validators     │  wiedza i jej   │      ↓                        │
 │ (schema, refs, provenance, cues) · risk model ·     │  reguły; nie    │ RTX 3090 24 GB · 128 GB RAM   │
 │ gates · deterministic tools (ingest, tables, terms) │  zna sieci      └──────────────────────────────┘
 │ · task specs (prompts, output/decoding schemas,     │  ani GPU         wymienialny worker: bez wiedzy
 │ context builders) · views · exporters               │                  domenowej, bez stanu kanonicznego
 └──────────────────────┬──────────────────────────┘
                        │ read/write YAML
 ┌──────────────── game project repo ────────────────┐
 │ project.yaml · source/inventory.yaml · kb/ ·        │  źródło prawdy (git)
 │ publication/ · reports/ · .glu/ (gitignored)        │
 └─────────────────────────────────────────────────────┘
```

Kierunek zależności: `interfaces → glu → wgc → contracts`. Pakiet `wgc` nie importuje `glu`. GLU nie zna pojęć gry.
Wykonuje `TaskSpec` zarejestrowane przez WGC i zapisuje wyniki wyłącznie przez `wgc.accept()`.
Pakiet **`igw`** (Inference Gateway, działa na węźle) nie importuje `wgc` ani `glu`, a GLU rozmawia z nim tylko przez
HTTP i kontrakt `igw/api@0` (ADR-0016).

**Warstwy inferencji** (od domeny w dół; każda nie wie nic o warstwach niżej):
```text
WGC domain → GLU orchestration → provider abstraction → self_hosted provider → LAN (HTTPS) → Inference Gateway
→ runtime (llama.cpp; wymienialny) → GPU / CPU / RAM
```
- WGC nie wie nic o sieci ani GPU.
- GLU nie wie, czy model działa na localhost, w LAN, w WSL czy na Linuksie.
- Węzeł nie wie, czym jest reguła, gra, Stage ani przekład.

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

**TaskSpec** (kontrakt WGC → GLU, M9a, ADR-0025): zamrożona dataclass w `wgc/tasks.py`, rejestr `wgc.tasks.registry()`.
- Pola obowiązkowe: `id`, `version`, `stage`, `output_kind`, `output_schema` (np. `wgc/logic@0#table`),
  `input_selector` (które segmenty lub rekordy, jedno wejście na job), `validate(ws, wejścia, propozycje) → issues`.
- Pola opcjonalne:
  - `deterministic_impl?` (Tier 0);
  - `semantic_projection?` (co z wejścia wpływa na wynik; domyślnie projekcje `logic` wejść);
  - `risk_features` (do M6 pusta lista);
  - do M10: `context_builder`, `prompt` (id@wersja) i `decoding_schema?` (płaski podzbiór do constrained decoding na
    węźle; domyślnie `output_schema`, jeśli jest zgodny).
- Wynik zadania to lista propozycji (rekord bez `prov`, `status`, `risk` + kotwice albo `derived_from`,
  [DATA-CONTRACTS §10](DATA-CONTRACTS.md#propozycje)). Zamiast `accept` w każdym zadaniu jest jedna funkcja
  `wgc.kb.accept()`: nadaje provenance, waliduje całe `kb/` i jako jedyna zapisuje YAML KB (pod blokadą pisarza
  projektu, każdy plik atomowo; ADR-0026).

## 3. Komponenty
| Komponent | Pakiet | Opis | Milestone |
|---|---|---|---|
| Rejestr kontraktów | `wgc.contracts` | schematy `contracts/schemas/*.schema.json`, walidacja dokumentów | M0 (jest) |
| Tożsamość i hashowanie | `wgc.ids`, `wgc.canonical` | gramatyka ID, kanoniczny JSON, projekcje semantyczne | M1 |
| Walidator | `wgc.validate` | L0 schemat, L1 referencje, L2 provenance i sygnały | M1, M5 |
| Ingest źródeł | `wgc.source`, `wgc.ingest` | inwentarz, segmentacja (Markdown: M2a; PDF, render, flagi wizualne: M2b) | M2a, M2b |
| Model ryzyka | `wgc.risk` | cechy, wagi, klasy, twarde reguły | M6 |
| Bramki | `wgc.gate` | obliczane statusy etapów | M7 |
| Job store | `glu.store`, `glu.states` | SQLite `.glu/state.db`: build, job, attempt, routing_decision; tabela przejść (ADR-0023); `glu status`, `glu export` | M8 |
| Zadania i akceptacja | `wgc.tasks`, `wgc.kb`, `wgc.tables`, `wgc.terms` | `TaskSpec` i rejestr, zakres buildu, `Workspace`, `accept()` (jedyny zapis do `kb/`), zadania `wgc.tables.parse@0` i `wgc.terms.harvest@0` | M9a, M9b |
| Bezpieczny zapis KB | `wgc.fsio`, `wgc.kb` | atomowa podmiana pojedynczego pliku, blokada pisarza projektu `.glu/kb.lock` wokół całego `accept()` (ADR-0026) | M-STAB1 |
| Planner | `glu.planner` | etap + zakres → joby z kluczem cache; `glu build --dry-run` | M9a, M12 (bramki) |
| Wykonawcy | `glu.exec` | deterministic (Tier 0, M9a), local, premium, human; `glu build` | M9a–M16 |
| Providerzy | `glu.providers` | fake, replay, self_hosted (klient `igw/api@0`), anthropic, desktop_pull | M10, M15 |
| Inference Gateway | `igw` (węzeł) | API `igw/api@0`, auth, limity, kolejka, scheduler, cykl życia modeli, adapter runtime'u, telemetria | M-GW1, M-GW2 |
| Diagnostyka inferencji | `glu doctor`, `igw doctor` | DNS, TCP, TLS, auth, health, capabilities, modele, structured output | M-E2E, M-GW2 |
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
│   ├── logic/                   Stage 1: concepts.yaml, rules.yaml, relations.yaml, tables.yaml, procedures.yaml,
│   │                            ambiguities.yaml, interpretations.yaml, cases.yaml, changes.yaml (zapisuje accept())
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

**Hosty.** Dev machine (Claude Desktop, MCP, GLU, repo gier, `.glu/`) i **inference node** w LAN (`igw`, runtime,
pliki modeli, `node.yaml`) to różne komputery. Węzeł nie jest źródłem prawdy: jego wymiana kosztuje tylko ponowne
obliczenia ([inference/NODE.md §7](inference/NODE.md#zrodlo-prawdy)).

## 5. Interfejsy
- `wgc …`: polecenia domenowe, deterministyczne (validate, gate, view, export, ingest).
- `glu …`: build, status, queue, review, decide, stats, cache, doctor, explain.
- `igw …` (na węźle): serve, doctor, token.
- MCP: te same usługi co CLI, z listą dozwolonych narzędzi ([MCP.md](MCP.md)).
- Skille Claude Code (opcjonalnie): cienkie nakładki wołające `glu`/`wgc`. Nie przechowują wiedzy.

## 6. Bezpieczeństwo (skrót)
Najmniejsze uprawnienia (allowlista katalogów projektów, zakresy odczytu i zapisu, allowlista podprocesów,
endpointy inferencji wyłącznie z konfiguracji providerów GLU), sekrety tylko ze zmiennych środowiska lub keyringu,
redakcja logów, brak tekstu źródła w commitach. Szczegóły: [MCP.md](MCP.md#bezpieczenstwo).
Sieć do węzła inferencji: HTTPS z przypiętym certyfikatem, token per klient, firewall z allowlistą hostów, runtime tylko na
`127.0.0.1` węzła, limity requestów, brak wykonywania poleceń ([inference/NODE.md §7](inference/NODE.md#zrodlo-prawdy)).

## 7. Granice przyszłego silnika
Opisane w [DIGITALIZATION.md](DIGITALIZATION.md#granice-silnika). Silnik nie jest częścią tego repo.
