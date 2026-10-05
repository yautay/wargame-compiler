# GLU: wykonanie i orkiestracja

GLU kieruje pracę do wykonawców (kod deterministyczny, lokalny LLM, premium LLM, człowiek), pilnuje cache,
przyrostowości, budżetu i metryk. **Nie posiada wiedzy o grze.** Knowledge Base (repo gry) pozostaje źródłem prawdy
(ADR-0004). Kontrakt stanu wykonania: `contracts/schemas/glu.schema.json` (`glu/exec@0`).

## 1. Model nie jest pamięcią projektu
```text
INPUT (rekordy, segmenty, hashe) → EXECUTOR (tier) → PROPOSED OUTPUT (blob) → VALIDATOR (WGC) → ACCEPTED STATE (kb/)
                                                       ↘ retry (z opisem błędów) / escalate / requires_human_interpretation
```
Nic, co nie przeszło walidacji WGC, nie trafia do `kb/`. Historia czatu nie jest stanem.

## 2. Pojęcia
| Pojęcie | Znaczenie | Gdzie żyje |
|---|---|---|
| **Project** | repo gry z `project.yaml` | git |
| **Stage** | etap pipeline'u (0, 1, 1.5, 2, 3) ze statusem z bramki | wyliczany (`wgc gate`) |
| **Build** | jedno zlecenie kompilacji: etap + zakres + polityka (routing, budżet, limit pytań) | `.glu/state.db` |
| **Job** | jednostka pracy: `TaskSpec` + wejścia + klucz cache. Idempotentny | `.glu/state.db` |
| **Attempt** | jedno wykonanie joba przez wykonawcę (tier, profil, tokeny, koszt, czas, wynik walidacji) | `.glu/state.db` + blob |
| **RoutingDecision** | dlaczego job trafił do danego tieru (sygnały, polityka, powody) | `.glu/state.db` |
| **Review** | przegląd premium lub ludzki wyniku albo przypadku spornego, przez `review_package` | `.glu/`; wynik → `kb/` |
| **Escalation** | przejście joba do wyższego tieru (z powodem) | stan joba + RoutingDecision |
| **Decision** | rozstrzygnięcie człowieka `HD-` (domena!) | `kb/decisions.yaml` |
| **Artifact** | zaakceptowany rekord albo wygenerowany plik (widok, LaTeX, engine kit) | `kb/`, `publication/`, `reports/` |
| **Session** | okres pracy interaktywnej: człowiek albo premium w Claude Desktop/Code przerabia kolejkę przeglądów i pytań | efekty w `kb/` i `.glu/` |

## 3. Cykl życia joba
```text
pending → ready → running → proposed → validating ─┬→ accepted → done
   ↑                                                ├→ retry ──────────→ ready        (≤ N prób na tier)
   │                                                ├→ escalated → ready (wyższy tier)
   │                                                ├→ waiting_review → (pakiet premium/człowiek) → validating
   │                                                ├→ waiting_human  → (HD-) → validating
   │                                                └→ rejected / failed
   └──────── stale (zmiana wejścia) ← done / accepted
```
- **Cache hit** przy `ready` → od razu `accepted` (zero wywołań modelu).
- **Retry** dostaje listę błędów walidacji (schemat i domena) w prompcie. Po wyczerpaniu prób następuje eskalacja, a nie akceptacja.
- **Build** kończy się `done`, `waiting_review` (czeka kolejka premium), `waiting_human` (pytania) albo `failed`.

## 4. Pętla structured output
```text
MODEL → STRUCTURED OUTPUT (JSON Schema w żądaniu: guided decoding / response_format)
      → SCHEMA VALIDATION (wgc.contracts, schemat propozycji zadania)
      → DOMAIN VALIDATION (wgc.validate: referencje, kotwice, cytaty dosłowne, sygnały źródło↔IR, liczby)
      → ACCEPT / RETRY / ESCALATE
```
- Schemat propozycji jest okrojonym schematem rekordu: **bez `prov`, `risk` i `status`**. Te pola dopisują GLU i WGC (ADR-0014).
- Wiedza kanoniczna nigdy nie pochodzi z niezwalidowanego wolnego tekstu. Pola `{text}` i glosy są dozwolone,
  ale wliczają się do ryzyka.

## 5. Wykonanie lokalne a sesja premium
- **Lokalnie** GLU wykonuje setki jobów w falach według profilu (żeby ograniczyć przeładowania modelu w VRAM),
  z równoległością ustaloną dla profilu.
- **Premium jest bezstanowy.** Dostaje `review_package`: pytanie, minimalny fragment źródła, rekordy z otoczenia w grafie
  (sąsiedztwo k-hop po `refs` i relacjach, przycięte do budżetu tokenów), propozycje lokalne (także rozbieżne),
  uzasadnienie ryzyka i `answer_schema`. Pakiet jest samowystarczalny: recenzent nie potrzebuje historii ani
  dostępu do repo.
- Dwie drogi premium (ADR-0013): `anthropic` (API) i `desktop_pull` (Claude Desktop pobiera pakiet przez MCP).
  Odpowiedź przechodzi tę samą walidację.

## 6. Cache
Cache jest częścią architektury. **Niezmienione wejście = zero wywołań modelu.**

| Poziom | Klucz | Zawartość |
|---|---|---|
| L1: inferencja | sha256 z (provider, `profile_fingerprint`, wiadomości, schemat wyjścia, parametry próbkowania) | surowa odpowiedź modelu |
| L2: wynik joba | sha256 z `cache_key` (niżej) | zaakceptowana propozycja + wynik walidacji |

`cache_key` (schemat `glu.schema.json#/$defs/cache_key`):
`task`, `task_version`, `prompt_version`, `output_schema`, `profile` + `profile_fingerprint` (model, kwantyzacja,
parametry), `input_hash` (hashe segmentów lub rekordów wejściowych), `context_hash` (hash projekcji rekordów
kontekstu), `dependency_state` (hash projekcji zaakceptowanych rekordów nadrzędnych).

- Dekodowanie lokalne deterministyczne (temperatura 0 + seed, gdy serwer to wspiera), żeby cache L1 był sensowny i testowalny.
- Bloby adresowane treścią: `.glu/blobs/sha256/<2>/<hash>`, indeks w SQLite. `glu cache gc` usuwa wpisy bez odwołań.
- Provider `replay` odtwarza nagrane odpowiedzi L1. Na tym opierają się testy GLU bez GPU (ADR-0008).

<a id="przyrostowosc"></a>
## 7. Przyrostowość (dependency-aware invalidation)
- **Graf zależności** budowany z danych KB: `anchors` (SEG → rekord), `derived_from`, `refs`, `relation.from/to`,
  `realizes`, `covers`, `from_case`, `concepts_used` (przekład → CON).
- **Projekcje semantyczne** (dostarcza WGC dla każdego rodzaju rekordu i konsumenta): hash obejmuje tylko pola
  istotne dla konsumenta. Przykłady:
  - Stage 1.5 zależy od struktury reguły (`nature`, `modality`, `bind`, `conditions`, `effects`, `limits`, `timing`,
    `layer`, relacje), a nie od glosy ani notatek;
  - przekład zależy od projekcji znaczeniowej reguł segmentu (modalność, warunki, limity, liczby), od terminów
    użytych pojęć i od konwencji Stage 2. Nie zależy od `realizes` w Stage 1.5.
- **Algorytm:** zmiana → przelicz hashe → oznacz bezpośrednich konsumentów jako `stale` → przelicz (cache często
  trafia) → jeśli projekcja wyniku się nie zmieniła, **zatrzymaj propagację** (early cutoff) → w przeciwnym razie
  idź dalej.
- **Kierunek:** krawędzie biegną tylko w dół etapów. Zmiana layoutu Stage 3 nie ma krawędzi do Stage 1.
- Zmiana jednej reguły nie powoduje pełnej analizy gry. Przelicza się tylko jej domknięcie w grafie.
- Świeżość da się wyliczyć bez `.glu/`, bo `seg_hash` i `prov.inputs_hash` są w `kb/`.

## 8. Budżety i bezpieczniki
- `build.policy.budget_premium_usd` i limit tokenów premium. Po przekroczeniu joby czekają (`waiting_review`) i nigdy
  nie są akceptowane lokalnie zamiast przeglądu.
- `build.policy.max_human_questions`: pytania ponad limit są odkładane do następnej sesji.
- Limity prób na tier, limit czasu joba, limit równoległości na profil.

## 9. Metryki
Każdy Attempt zapisuje tokeny, koszt, czas GPU, czas ścienny i wynik walidacji, a każdy Build agregaty.
Definicje i raporty: [COST.md](COST.md#obserwowalnosc).
