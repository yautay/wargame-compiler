# Model logiki (Stage 0 i Stage 1)

Stage 1 odpowiada wyłącznie na pytanie: **jak działa gra?** Buduje kanoniczną reprezentację instrukcji niezależną
od języka docelowego (ADR-0003), od wyglądu publikacji i od przyszłego silnika. Kontrakty:
`contracts/schemas/source.schema.json`, `logic.schema.json`, `common.schema.json`. Przykład:
`contracts/fixtures/valid/logic.minigame.yaml`.

## Stage 0: źródła
- **Inwentarz** (`source_document`, `SRC-`): wszystkie oczekiwane dokumenty z rolą (`rules`, `scenario_book`,
  `charts`, `errata`, `faq`, `designer_clarification`, `cards`, `counters`, `map`, `module`, `prior_translation`),
  wydaniem, `file_hash`, `present`, `complete`, `precedence` i `edition_skew`. **Brakujący dokument też jest rekordem**
  (`present: false`), więc luka jest widoczna, zanim ruszy analiza (lekcja 7 z ARCHAEOLOGY).
- **Segmenty** (`segment`, `SEG-`): najmniejsze adresowalne jednostki tekstu (akapit z numerem reguły, tabela, ramka,
  przykład, nota). Mają `text_hash` znormalizowanego tekstu (NFC, zwinięte białe znaki, złączone przeniesienia),
  `visual_flags` (przekreślenie, kolor zmian, pomieszane kolumny, OCR) i `verified_by_render`.
- Ekstrakcja jest deterministyczna i wersjonowana (`extractor`). Ręczne poprawki są jawne (`corrections`).
- Tekst segmentów nie trafia do repo (ADR-0012).

## Rekordy Stage 1
| Rodzaj | Prefiks | Rola |
|---|---|---|
| `concept` | `CON-` | typowane pojęcie: `entity_type`, `state`, `state_var`, `resource`, `action`, `event`, `phase`, `step`, `role`, `place`, `terrain`, `marker`, `predicate`, `die`, `deck`, `scenario` |
| `rule` | `R-` | atomowa reguła w Rule IR |
| `relation` | `REL-` | wyjątek, nadpisanie, wymaganie, kolejność. **Jedyne** miejsce zapisu pierwszeństwa (ADR-0005) |
| `table` | `TAB-` | tabela mechaniczna w postaci danych (przedziały `{min, max}`) z `complete` |
| `procedure` | `PROC-` | kroki (sekwencja tury, procedura walki) ze znacznikami `decision`, `reaction`, `roll`, `loop`, `hidden` |
| `ambiguity` | `AMB-` | to, czego źródła nie rozstrzygają: odczytania, rekomendacja z siłą, `impact` |
| `interpretation` | `INT-` | wybrane odczytanie; `accepted` tylko z decyzją `HD-` |
| `case` | `CASE-` | przypadek kontrolny (sytuacja → werdykt + łańcuch reguł), z polaryzacją |
| `change` | `CHG-` | errata, FAQ, wyjaśnienie autora, różnica wydań |
| `human_decision` | `HD-` | decyzja człowieka (tylko dopisywanie) |
| `review_request` | `RR-` | zgłoszenie z etapu niższego |

## Rule IR
Reguła ma strukturę i glosę. Struktura jest kontraktem, glosa służy ludziom.

| Pole | Znaczenie | Przykład (`R-3.4`) |
|---|---|---|
| `nature` | definition, permission, obligation, prohibition, automatic_effect, constraint, procedure_step, modifier, table_application, setup, victory, sequence, commentary | `prohibition` |
| `modality` | `may`, `must`, `must_not`, `need_not`, `is` (skutek automatyczny), `none` | `must_not` |
| `bind` | typowane zmienne | `{$unit: CON-unit, $hex: CON-hex}` |
| `actor`, `action`, `target` | kto, co, na czym | `$unit`, `CON-move`, `$hex` |
| `timing` | okno (`during`, `start_of`, `end_of`, `before`, `after`, `immediate`, `any_time`, `setup`) i jego obiekt | — |
| `conditions` | wyrażenie logiczne (warunki wstępne) | `all: [is $unit routed, adjacent_to_enemy $hex]` |
| `effects` | atomy efektów: `set`, `inc`, `dec`, `enter_state`, `leave_state`, `place`, `remove`, `move`, `random`, `lookup`, `choose`, `reveal`, `hide`, `invoke`, `end_activity`, `text` | — |
| `limits` | `{quantity, op, value, per}`, gdzie `per` ∈ action, activation, unit, attack, step, phase, player_turn, game_turn, game, hex, stack, player | „up to MA per Movement Phase” |
| `triggers` | `{event: CON-…, when}` | 3.3: wejście na heks obok wroga |
| `layer`, `applies_in` | core, advanced, optional, series, game, scenario, errata; scenariusze | 7.1: `scenario`, `CON-scn.ford` |
| `formalization` | `full` / `partial` / `none`; przy `partial` wymagane `unformalized` | `full` |
| `statement` | glosa w języku KB | — |
| `ambiguities`, `refs`, `prov`, `risk`, `status` | — | — |

### Gramatyka wyrażeń (celowo mała)
- Logiczne: `all`, `any`, `not`, `cmp: [a, op, b]` (op: `< <= = != >= >`), `is: [podmiot, CON-stan]`,
  `pred: CON-predykat, args`, `val: CON-zmienna` (zmienna logiczna), `{text}` (jawny, niesformalizowany liść).
- Wartości: liczby, `$zmienne`, ID pojęć, `val: CON-zmienna, of`, `count: CON-typ, where`, `add`, `sub`, `{text}`.
- Wszystko, co specyficzne dla gry (sąsiedztwo, LOS, kontrola, linia zaopatrzenia), jest **predykatem-pojęciem**
  (`CON-…`, `category: predicate`) z definicją i regułami definiującymi. Gramatyka się nie rozrasta.
- Liść `{text}` jest dozwolony, ale obniża `formalization` i podnosi ryzyko. Rośnie stopniowo, bez przepisywania.

Model zawiera wszystkie kategorie z promptu (§3): ENTITY i STATE (`concept`), ACTION (`concept` + `rule.action`),
TARGET, TRIGGER, PRECONDITION (`conditions`), EFFECT, EVENT (`concept: event`), RESOURCE, LIMIT, DECISION
(`effect: choose`, `procedure.markers`), RANDOM_SOURCE (`effect: random`, `concept: die/deck`), INVARIANT
(`nature: constraint`), OVERRIDE, EXCEPTION, DEPENDENCY (`relation`).

### Czego Stage 1 nie robi
Nie tłumaczy, nie projektuje silnika (pól stanu, zdarzeń, kodów błędów: to Stage 1.5), nie rozstrzyga niejasności,
nie poprawia autora. Błąd oryginału to `ambiguity` albo `change`, nigdy cicha korekta.

## Provenance
Rekord ma `prov.kind` (`common.schema.json#/$defs/provenance`):

| Rodzaj | Kiedy | Wymaga |
|---|---|---|
| `explicit_source` | treść wprost w segmencie źródła | `anchors` (≥ 1), zgodny `seg_hash`, cytat dosłowny w tekście segmentu (M5) |
| `deterministic_derivation` | wynik reguły kodu (np. relacja ze scenariusza nadpisującego) | `derived_from`, `by.tier: deterministic` |
| `llm_inference` | wniosek modelu | `derived_from`, `by.tier: local/premium` |
| `interpretation` | wybór odczytania niejasności | `derived_from` (AMB) |
| `errata`, `faq`, `designer_clarification` | treść z dokumentu o tej roli | `anchors` do segmentu takiego dokumentu |
| `human_decision` | ustalenie człowieka | `decision: HD-…`, `by.tier: human` |

Rodzaj nadaje WGC, nie model (ADR-0014). `inputs_hash` zapamiętuje stan wejść w chwili akceptacji (wykrywanie `stale`).

<a id="model-ryzyka"></a>
## Model ryzyka semantycznego (`wgc/risk@0`)
Cel: wskazać rekordy, w których pomyłka jest prawdopodobna albo kosztowna, **bez polegania na samoocenie modelu**.
Wynik jest audytowalny: każda cecha ma wartość, wagę i dowód (`risk.features[]`).

### Cechy
| Grupa | Cecha | Źródło |
|---|---|---|
| Tekst źródła (słownik sygnałów EN, wersjonowany) | `negation`, `prohibition`, `modal_strength`, `exception_marker`, `boundary_operator` („or more”, „equal to”, „at least”, „exceeds”…), `numeric_constraint` (liczba liczb), `scope_marker` („only”, „once”, „per”, „each”), `nested_conditions` (zagnieżdżone if/when/unless/only if i spójniki), `cross_refs` (odwołania do numerów reguł), `sentence_complexity` | segment |
| Graf KB | `inbound_exceptions`, `inbound_overrides`, `dependency_degree` (refs in/out), `open_ambiguity`, `layer_scenario_or_errata`, `referenced_by_exception_text` | KB |
| Wpływ | `digital_state_impact` (dotyka zmiennej stanu lub legalności), `downstream_count` (liczba zależnych) | KB |
| Proces | `formalization_gap` (`partial`/`none`), `local_disagreement` (dwie niezależne ekstrakcje różnią się po normalizacji), `cue_mismatch` (np. źródło ma zakaz, a IR nie ma `must_not` ani negacji), `validation_retries`, `self_confidence` (sygnał, nie werdykt) | job |

### Wynik i klasy
`score = Σ wᵢ·xᵢ` (cechy znormalizowane do [0, 1]). Klasy: `low < 0.25 ≤ medium < 0.5 ≤ high < 0.75 ≤ critical`
(progi wersjonowane razem z wagami). **Twarde reguły** (`risk.forced`) podnoszą klasę niezależnie od wyniku:
| Reguła | Klasa minimalna | Uzasadnienie |
|---|---|---|
| `boundary_operator` | high | ≥ → > przeoczone przez heurystykę w próbie SPQR |
| `cue_mismatch` | critical | strukturalna sprzeczność źródła i IR |
| `local_disagreement` | high | brak zgody dwóch niezależnych wykonań |
| `negation_with_exception_target` | high | negacja w regule z wyjątkami lub wskazywanej przez wyjątek |
| `open_ambiguity` z `impact.semantic` | high | wymaga przeglądu lub człowieka |
| `layer: scenario/errata` z `overrides` | medium | nadpisania są źródłem błędów pierwszeństwa |

### Kalibracja
Wagi i progi stroi benchmark mutacyjny ([QUALITY.md](QUALITY.md)). Wymagania: **zero wyników fałszywie negatywnych na
mutacjach krytycznych** (zmiana modalności, granicy, usunięcie wyjątku lub limitu), a przy tym możliwie mało eskalacji.
Zmiana wag = nowa wersja `wgc/risk@N`. Rekordy z ryzykiem policzonym starszą wersją są przeliczane deterministycznie,
bez wywołań modelu.

## Niejasności i człowiek w pętli
- Model może zaproponować odczytania i rekomendację z siłą (`certain`, `probable`, `speculative`). **Nie rozstrzyga.**
- Gdy wpływ jest semantyczny, a źródła (errata, FAQ) milczą, stan końcowy automatu to `requires_human_interpretation`,
  a przypadek kontrolny ma werdykt `requires_human_interpretation`.
- Człowiek odpowiada decyzją `HD-` (pytanie zamknięte z wariantami, rekomendacją i skutkami). Interpretacja `INT-`
  staje się `accepted` z `prov.decision`.
- Budżet pytań na build (`build.policy.max_human_questions`) chroni właściciela przed zalewem pytań (lekcja 14).
