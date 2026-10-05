# Pipeline: etapy, kontrakty, bramki

```text
Stage 0  SOURCE         inwentarz źródeł, segmenty, hashe            (deterministycznie + człowiek przy OCR)
   ↓
Stage 1  LOGIC / DATA   Rule IR, pojęcia, relacje, tabele, procedury,  „Jak działa gra?”
   │                    niejasności, przypadki kontrolne
   ├──────────────→ Stage 1.5  DIGITALIZATION   stan, akcje, legalność, zdarzenia, timing,
   │                                             decyzje, losowość, testy        „Jak to zaimplementować bez zmiany zasad?”
   ↓
Stage 2  EDITORIAL      rejestr, terminologia źródła, struktura, oprawa  „Jak oryginał komunikuje treść?”
   ↓
Stage 3  TRANSLATION /  przekład segmentów, glosariusz docelowy,         „Jak to powiedzieć i wydać w języku X?”
         PUBLICATION    LaTeX, pomoce do gry, PDF
```

Stage 1.5 to gałąź wychodząca ze Stage 1. Nie zależy od Stage 2 ani 3. Stage 2 i 1.5 mogą działać równolegle.

## 1. Kontrakty etapów (faza D)

### 1.1 Source → Logic (Stage 0 → Stage 1)
| | |
|---|---|
| **Wejście** | `source/inventory.yaml` (`SRC-`, `SEG-` z `text_hash`), tekst segmentów w `.glu/source/` (odtwarzany), rendery stron |
| **Wyjście** | `kb/logic/*` (`wgc/logic@0`): `concept`, `rule`, `relation`, `table`, `procedure`, `ambiguity`, `interpretation`, `case`, `change` |
| **Gwarancje wyjścia** | każdy rekord ma `prov`; `explicit_source` ma kotwice ze zgodnym `seg_hash`; każdy segment typu `rule`/`table` ma ≥ 1 rekord albo jawne wykluczenie (`commentary`); wyjątki tylko w `relation` |
| **Zakazy** | brak tekstu źródła w KB poza krótkimi cytatami w kotwicach; brak decyzji interpretacyjnych bez `HD-`; brak terminów docelowych |
| **Zmiana w górę** | nowe lub zmienione źródło (errata, karty, Vassal) = nowe `SRC-`/`SEG-` → invalidacja zależnych rekordów |

### 1.2 Logic → Digitalization (Stage 1 → Stage 1.5)
| | |
|---|---|
| **Wejście** | wyłącznie zaakceptowane rekordy Stage 1 (z niejasnościami i przypadkami). Źródło tylko jako dowód (przez kotwice) |
| **Wyjście** | `kb/digital/*` (`wgc/digital@0`): `entity`, `derived`, `action`, `legality`, `event`, `trigger`, `sequence`, `decision_point`, `random_source`, `modifier`, `hidden_info`, `invariant`, `priority`, `blocker`, `test` |
| **Gwarancje** | każdy rekord ma `realizes` → Stage 1; każda niejasność z `impact.digital ∈ {affects, blocks}` ma `blocker` albo zaakceptowaną interpretację (`INT-` z `HD-`); każdy `case` mechaniczny ma `test` albo powód braku |
| **Zakazy** | Stage 1.5 **nie zmienia** Stage 1 i nie rozstrzyga niejasności. Wykryty błąd logiki zgłasza jako `review_request` (`RR-`, `from_stage: stage1_5`) |

### 1.3 Logic → Editorial (Stage 1 → Stage 2)
| | |
|---|---|
| **Wejście** | Stage 1 (pojęcia z `source_terms`, struktura reguł), segmenty źródła, rendery i pomiar oprawy |
| **Wyjście** | `kb/editorial/*` (`wgc/editorial@0`, M24): profil rejestru, konwencje modalności, inwentarz terminologii źródła (wielkie litery, definicje), mapa struktury (hierarchia, numeracja, ramki, przykłady, noty), specyfikacja oprawy (`layout`) |
| **Gwarancje** | każdy rekord redakcyjny ma kotwice; każdy `CON-` z `source_terms` ma konwencję zapisu |
| **Zakazy** | Stage 2 **nie zmienia** Stage 1. Podejrzenie błędu logiki → `RR-` (`from_stage: stage2`) |

### 1.4 Logic + Editorial → Publication (Stage 1 + 2 → Stage 3)
| | |
|---|---|
| **Wejście** | segment źródła, Logic Model (projekcja semantyczna reguł segmentu), Editorial Model, glosariusz (warstwy), polityka przekładu, preferencje właściciela (`HD-`) |
| **Wyjście** | `kb/publication/<lang>/`: przekłady segmentów z hashami wejść, glosariusz gry; `publication/<lang>/`: LaTeX, styl, PDF, pomoce do gry |
| **Gwarancje** | każdy przekład segmentu ma `ir_hash` (projekcja Stage 1), `editorial_hash`, `glossary_hash`; terminy tylko zatwierdzone; kontrola wsteczna IR bez rozbieżności albo z rozstrzygnięciem |
| **Zakazy** | Stage 3 **nie analizuje mechaniki od zera**. Znaczenie bierze z IR, rozbieżność przekład↔IR to błąd przekładu albo `RR-` |

## 2. Model statusów i bramek
Status jest wyliczany przez `wgc gate <stage> --scope <game|chapter|record_set>` i zapisywany jako raport
`wgc/gate@0` (ADR-0011). Stany:

| Stan | Znaczenie |
|---|---|
| `not_started` | brak rekordów etapu w zakresie |
| `in_progress` | są rekordy, ale nie wszystkie wymagane kryteria są spełnione |
| `awaiting_review` | kryteria mechaniczne spełnione, czekają przeglądy premium lub ludzkie (rekordy `high`/`critical`) |
| `blocked` | otwarty bloker albo brak wymaganego etapu wejściowego |
| `stale` | wejście się zmieniło (hash kotwicy, `inputs_hash`) i rekordy nie zostały przeliczone |
| `validated_with_open_issues` | wszystkie wymagane kryteria spełnione; są otwarte sprawy nieblokujące (np. niejasność bez wpływu cyfrowego) |
| `validated` | wszystkie kryteria spełnione, brak otwartych spraw w zakresie |
| `complete` | `validated` + widoki i raporty świeże + pokrycie docelowe (dla 1.5: metryki z [DIGITALIZATION.md](DIGITALIZATION.md#pokrycie)) |

Pierwszeństwo przy wielu stanach: `blocked > stale > awaiting_review > in_progress`.

### Wymagania wejściowe (bramki)
| Etap | Wymaga (dla tego samego zakresu) |
|---|---|
| Stage 1 | Stage 0 ≥ `validated_with_open_issues` (inwentarz kompletny albo braki jawne) |
| Stage 1.5 | Stage 1 ≥ `validated_with_open_issues`, a otwarte sprawy nie mają `impact.digital: blocks` bez rekordu `blocker` |
| Stage 2 | Stage 1 ≥ `validated_with_open_issues` |
| Stage 3 | Stage 1 ≥ `validated`, Stage 2 ≥ `validated_with_open_issues`, glosariusz: wszystkie `CON-` użyte w zakresie mają termin `approved` |

Stage 1.5 i Stage 2 mają **niezależne** statusy. Zakres może być rozdziałem: digitalizacja walki może ruszyć, zanim
Stage 1 całej gry jest gotowy, jeśli zakres i jego zależności (domknięcie po `refs` i relacjach) są zwalidowane.

### Kryteria Stage 1 (polityka `gate.stage1@0`, progi w `project.yaml`)
`schema_valid`, `refs_resolve`, `segment_coverage = 1.0`, `anchors_fresh`, `provenance_consistent`,
`high_risk_reviewed = 1.0`, `cases_answerable` (każdy `case` ma łańcuch istniejących rekordów),
`exception_markers_have_relations` (ostrzeżenie → wymagane od M5), opcjonalnie `open_semantic_ambiguities = 0`.

## 3. Śledzenie (traceability)
```text
SEG-dsk.3.4 ──anchor──▶ R-3.4 ──realizes──▶ LEG-move.routed_adjacent ──applies_to──▶ ACT-move ──covers──▶ TST-001
     ▲                                                                                                        │
     └──────────── failed engine test → TST-001.realizes → R-3.4.prov.anchors → SEG-dsk.3.4 ◀──────────────────┘
```
Śledzenie w obie strony to zapytania po polach `anchors`, `derived_from`, `realizes`, `covers`, `applies_to`, `from_case`.
`wgc trace <ID> --down|--up` (M20) i narzędzie MCP `trace` je wykonują. Przykład w fixture'ach:
`contracts/fixtures/valid/digital.minigame.yaml`.

## 4. Przyrostowość między etapami
Krawędzie zależności biegną wyłącznie w dół (Stage 0 → 1 → {1.5, 2} → 3). Każdy rekord pochodny pamięta `inputs_hash`
projekcji semantycznych swoich wejść. Skutki:
- zmiana segmentu źródła unieważnia rekordy z kotwicą do niego, potem (przez graf) zależną logikę, fragmenty 1.5, 2, 3 i testy;
- **early cutoff**: jeśli przeliczony rekord ma tę samą projekcję semantyczną, propagacja się zatrzymuje;
- zmiana układu strony (Stage 3) nie ma krawędzi do Stage 1, więc go nie unieważnia;
- zmiana terminu w glosariuszu unieważnia tylko przekłady segmentów, które używają tego `CON-`.
Szczegóły: [GLU.md](GLU.md#przyrostowosc).

## 5. Kanał zwrotny
Etap niższy nigdy nie pisze w górę. Zgłasza `review_request` (`RR-`): `from_stage`, `target`, `issue`, `evidence`.
Właściciel lub zadanie Stage 1 rozpatruje go i ewentualnie zmienia rekord (z provenance i nowym `inputs_hash`), co
uruchamia invalidację w dół. Testy silnika, które nie przechodzą, a których przyczyną okazuje się logika, też wracają
jako `RR-` (`from_stage: engine`).
