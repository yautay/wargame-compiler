# Architektura digitalizacji (Stage 1.5)

Stage 1.5 odpowiada na pytanie: **jak przełożyć poprawny Logic Model na architekturę przyszłego silnika bez zmiany
zasad gry?** Wynik to specyfikacja gotowa do implementacji, niezależna od Unity, Godota, Unreala, frameworka webowego
czy backendu (ADR-0006, ADR-0007). Kontrakt: `contracts/schemas/digital.schema.json` (`wgc/digital@0`). Przykład:
`contracts/fixtures/valid/digital.minigame.yaml`.

## Zasady
1. **Wejście to wyłącznie Stage 1**: zaakceptowane rekordy, niejasności, przypadki kontrolne, graf zależności.
   Źródło tylko jako dowód przez kotwice. Stage 1.5 nie interpretuje instrukcji od zera.
2. **Każdy element ma `realizes`** → rekordy Stage 1. Element bez śledzenia jest błędem schematu.
3. **Niejasność wpływająca na semantykę implementacji → `blocker` (`BLK-`)** z `cause` → `AMB-`. Stage 1.5 jej nie „naprawia”.
4. Błąd wykryty w Stage 1 → `review_request` (`RR-`, `from_stage: stage1_5`). Zapis w górę jest zabroniony.
5. Specyfikacja nie musi być wykonywalna. Wykonywalne są **testy**: wstrzykują decyzje i wyniki losowe i sprawdzają
   zdarzenia oraz stan.
6. Model jest proporcjonalny: nie budujemy event sourcingu, DSL ani dowodzenia, jeśli prostszy kształt wystarcza.

## State Model (schemat stanu)
- `entity` (`ENT-`): encje stanu (jednostki, dowódcy, formacje, heksy/obszary, znaczniki, zasoby, gra: tura, faza,
  podfaza, inicjatywa, kontrola, stan scenariusza). **Pola nie są zakładane z góry.** Wynikają z `CON-` kategorii
  `state`, `state_var`, `resource`, `marker`, `place` danej gry.
- Pole ma typ (`int`, `bool`, `enum`, `string`, `ref`, `set`, `list`, `map_location`), zakres lub wartości,
  `visibility` (`public`, `owner`, `hidden`) i `realizes`.
- **Przechowywane ≠ pochodne.** W stanie przechowywanym są tylko wartości, których nie da się wyliczyć ze stanu
  kanonicznego. Każde pole, które wygląda na pochodne, a jest przechowywane, ma `stored_reason` (np. `mp_spent` zależy
  od historii ścieżki).
- `derived` (`DRV-`): wartości liczone (pozostałe MP, status dowodzenia, siła w walce, wynik LOS, kontrola heksu)
  z wyrażeniem `compute` i modyfikatorami.

## Action Model (katalog akcji)
`action` (`ACT-`): `actor` (rola), `params` (z domeną), `timing` (stany `SEQ-`, w których akcja może być
zaproponowana), `legality` (lista `LEG-`), `decisions` (`DP-`), `random` (`RNG-`), `effects` (atomy Rule IR),
`emits` (`EVT-`), `realizes`. Typowe akcje (move, attack, issue_order, activate, rally, withdraw, fire, charge, pass,
end_phase) **nie są szablonem**. Katalog powstaje z `CON-` kategorii `action` i reguł z `action`.

## Legality Model
- `legality` (`LEG-`): jeden predykat `can_perform_action`, rodzaj `check` (`precondition`, `prohibition`, `limit`,
  `timing`, `cost`), **`reason_code`** zwracany przy odrzuceniu i sprawdzany w testach nielegalnych akcji,
  `unless` dla wyjątków (z `REL-… exception_to`).
- Akcja jest legalna, gdy wszystkie jej `LEG-` są spełnione (z uwzględnieniem `unless`). Legalność da się testować
  niezależnie od efektów: `can_perform(state, action) → verdict` nie zmienia stanu.
- **Werdykt legalności (kierunek dla M18):** wynik nie jest booleanem. Brak wiedzy nie jest `false`:
  ```yaml
  verdict: illegal            # legal | illegal | blocked | unresolved
  reasons: [WRONG_PHASE, INSUFFICIENT_MP]   # reason_code z LEG-
  evidence: [R-031, LEG-014]                # rekordy, z których wynika werdykt
  ```
  - `blocked` oznacza, że odpowiedź zależy od otwartego `BLK-` lub niejasności;
  - `unresolved` oznacza, że specyfikacja nie pozwala rozstrzygnąć.

  Kontrakt `wgc/digital@0` ma dziś w testach `then.accepted: boolean`. Zamiana na `then.verdict` z `reasons`
  i `evidence` następuje w M18, razem z fixture'ami.
- Reguły zakazu (`nature: prohibition`) przekładają się na `LEG-` deterministycznie (szablon, zadanie Tier 0).
- Silnik generuje listę legalnych opcji dla `DecisionRequest` z tych samych predykatów. AI adapter i UI dostają tę samą listę.

## Transition Model
```text
state_before + action (+ decisions + random outcomes)  →  events  →  apply(state, event)*  →  state_after
```
- `perform` produkuje zdarzenia. Reduktor `apply` jest jedynym miejscem zmiany stanu.
- Efekty (`effects`) akcji i triggerów są specyfikacją zdarzeń, które powstają.
- Test przejścia: `given` (stan) + `when` (kroki, wyniki losowe) → `then` (`accepted`/`reason_code`, lista zdarzeń
  w kolejności, ścieżki stanu).

## Event Model
- **Reguła ≠ zdarzenie.** Reguła definiuje zależność, zdarzenie zapisuje to, co się stało (`UnitMoved`,
  `AttackDeclared`, `DieRolled`, `CombatResolved`, `UnitRouted`, `LeaderActivated`).
- `event` (`EVT-`): `name` (PascalCase), `payload` (typowane pola), `visibility`, `realizes`.
- Zdarzenia wystarczają do replay, audytu, debugowania, undo/redo i testów deterministycznych.
- Wynik losowania jest w zdarzeniu (np. `DieRolled.result`). Replay nie losuje.

## Timing Model
- `sequence` (`SEQ-`): drzewo poziomów `game → game_turn → player_turn → phase → subphase → step` z `next`, `repeat`,
  `exit_when` i oknami (`start_of`, `end_of`, `during`, `reaction`, `interrupt`).
- Okna reguł (`rule.timing.window`: before, after, during, immediate, start_of, end_of) mapują się na okna sekwencji.
- Kolejność rozstrzygania jednoczesnych triggerów jest jawna (`trigger.order`). Gdy instrukcja jej nie podaje, to bloker albo `INT-`.

## Trigger Model
`trigger` (`TRG-`): `fires_on` (`EVT-` albo okno `SEQ-`), `condition`, `response` (efekty, akcja lub decyzja),
`mandatory`, `timing` (`immediate`, `interrupt`, `reaction`, `end_of_step`, `end_of_phase`, `start_of_phase`), `order`.
Klasy (`class`) to zbiór otwarty: `on_action`, `on_enter_location`, `on_leave_location`, `after_combat`,
`when_routed`, `when_eliminated`, `on_activation`, `on_phase_start`, `on_phase_end`…

## Decision Model
- `decision_point` (`DP-`): `who` ∈ `active_player`, `opponent`, `both_players`, `owner`, `scenario`, `system`,
  `random_process`; `when` (stany `SEQ-`); `options` (akcje, wybór, `pass_allowed`); `simultaneous`, `secret`, `default`.
- **Każde wejście uczestnika** to odpowiedź na DecisionRequest z wyliczonymi legalnymi opcjami (ADR-0007).
- Decyzje gracza są oddzielone od automatycznych efektów systemu: efekt bez wyboru to `effects`, a nie `DP-`.

## Randomness Model
- `random_source` (`RNG-`): `mechanism` ∈ `dice`, `deck`, `draw`, `shuffle`, `table_lookup`, `reroll`,
  `random_selection`; `spec` (np. `1d6`), `table`, `modifiers`, `order` (dla losowań jednoczesnych), `recorded_as` (`EVT-`).
- `modifier` (`MOD-`): `applies_to`, `value`, `condition`, `stacking` (`cumulative`, `max_only`, `non_cumulative`,
  `replace`), `order`, `cap`. Przykład: `MOD-ford_rally` modyfikuje próg `DRV-rally_threshold`, a nie rzut `RNG-rally`. Przy teście „rzut ≤ próg” +1 do rzutu dałoby skutek odwrotny do reguły 7.1.
- **Losowość jest wstrzykiwana**: logika biznesowa woła port RNG (`roll(source, purpose)`), nie generator
  bezpośrednio. Testy podają wyniki (`when.random`), replay czyta je ze zdarzeń, a ziarno (seed) służy tylko do
  generowania nowych rozgrywek.

## Hidden Information Model
- `hidden_info` (`HID-`): `subject` (ścieżka pola), `owner`, `visible_to`, `reveal_on` (`TRG-`/`EVT-`).
- Pola mają `visibility`. Silnik wystawia stan przez **widoki per obserwator** (`view(state, observer)`).
  Zdarzenia mają `visibility`, więc log też da się filtrować.
- Nie zakładamy, że cały stan jest dostępny wszystkim. Zapis pełny (wszechwiedzący) i eksport widoku gracza to różne artefakty.

## Invariants
`invariant` (`INV-`): `forall` (zmienne), `holds` (wyrażenie), `severity`. Przykłady: jeden oddział na heks,
siła w zakresie 1–4, wyeliminowana jednostka nie ma pozycji na mapie, wydany zasób nie spada poniżej zera, bieżąca
faza należy do sekwencji tury. Sprawdzane w testach (po każdym zdarzeniu) i w buildach debug silnika. To nie jest dowodzenie twierdzeń.

## Priority / Overrides
`priority` (`PRI-`): uporządkowane warstwy (od najniższej): `general_rule`, `specific_rule`, `exception`, `series`,
`game`, `scenario_override`, `errata`, `temporary_effect` oraz `resolutions` (relacja, zwycięzca, przegrany, warunek),
wyprowadzone z `REL-`. Silnik implementuje pierwszeństwo jawnie, z odwołaniem do `PRI-`/`REL-`, a nie przez
kolejność ifów. Każde nadpisanie ma test `override`.

## Persistence / Replay Model
- **Format stanu** `wgc/state@0` (schemat w M17): `{format, game, ruleset_hash (hash modelu cyfrowego), seq
  (indeks ostatniego zdarzenia), state, rng: {kind, seed?, position?}}`, serializowany kanonicznym JSON (posortowane
  klucze, UTF-8). Dzięki temu porównanie stanów to porównanie hashy, a diff jest czytelny.
- **Zapis** = snapshot + log zdarzeń + wersje (`format`, `ruleset_hash`). **Load** = snapshot + odtworzenie logu.
  **Replay** = odtworzenie od początku (zdarzenia zawierają wyniki losowe). **Undo** = odtworzenie do n−1 od
  ostatniego snapshotu. **Redo** = stos cofniętych zdarzeń, kasowany przy nowym wejściu.
- Wersjonowanie od początku: zmiana formatu podbija `format`, a migracje są funkcjami `vN → vN+1` z fixture'ami
  na każdą wersję.
- Proporcjonalność: event sourcing w wersji minimalnej (log + snapshoty), bez infrastruktury zdarzeń, kolejek i
  projekcji asynchronicznych.

<a id="granice-silnika"></a>
## Granice przyszłego silnika
| Warstwa silnika | Odpowiada za | Źródło w specyfikacji |
|---|---|---|
| domain state | czysty, serializowalny stan | `entity`, `wgc/state@0` |
| rules | czyste funkcje reguł (kod) | `rule` przez `realizes` |
| actions | katalog i parametry | `action` |
| legality | `can_perform`, generowanie opcji | `legality`, `decision_point` |
| events | typy zdarzeń, reduktor | `event` |
| timing | maszyna stanów tury, okna | `sequence`, `trigger` |
| randomness | port RNG, nagrywanie wyników | `random_source`, `modifier` |
| scenario | ładowanie scenariusza, nadpisania | `CON-scn.*`, `priority` |
| map | topologia, odległości, sąsiedztwo, LOS | predykaty `CON-` + `derived` |
| persistence | snapshot, log, migracje | Persistence Model |
| view | widoki per obserwator | `hidden_info` |
| UI adapter | prezentacja, wejście → odpowiedź na DecisionRequest | — (poza specyfikacją) |
| AI adapter | wybór spośród legalnych opcji | `decision_point` |
Adapter konkretnej technologii to późniejsza, osobna warstwa. Model kanoniczny pozostaje niezależny od silnika.

<a id="sledzenie-regul"></a>
## Rule Traceability
```text
source rule (SEG-) → logical rule (R-) → digital rule (LEG-/ACT-/TRG-/MOD-…) → engine concept (kod z adnotacją ID) → test (TST-)
failed engine test (TST-) → digital rule (covers) → logical rule (realizes) → source evidence (prov.anchors → SEG-)
```
- Powiązania: `realizes` (1.5 → 1), `covers` i `from_case` (test → 1.5 i 1), `prov.anchors` (1 → 0).
- Silnik oznacza kod ID z modelu cyfrowego lub logiki (np. adnotacją `@rule R-3.4` / `@digital LEG-move.routed_adjacent`)
  i odsyła `engine-results.json` (`{test, passed, reason?}`). `wgc trace --up TST-001` daje łańcuch do segmentu źródła.
- Przykład w fixture'ach: `SEG-dsk.3.4 → R-3.4 → LEG-move.routed_adjacent → ACT-move → TST-001` (`reason_code:
  move.routed_adjacent`).

## Testing Strategy
- Każda istotna reguła mechaniczna ma test. Kategorie: `legal`, `illegal`, `boundary`, `exception`, `override`,
  `random`, `trigger`, `hidden_info`, `invariant`, `replay`.
- Źródłem testów są przypadki kontrolne Stage 1 (`case` → `test.from_case`) i reguły z ryzykiem `high`/`critical`
  (dla nich minimum: test legalny, nielegalny i graniczny).
- **Given**: snapshot stanu (`given.state` lub fixture) + punkt sekwencji (`at`) + scenariusz. **When**: kroki
  (`by`, `decision`, `action`, `params`) + wyniki losowe (`random`). **Then**: `accepted` / `reason_code`, zdarzenia
  w kolejności, asercje ścieżek stanu.
- Fixture'y stanu są w formacie `wgc/state@0`, więc działają w każdym silniku z adapterem testów.
- Dla gry benchmarkowej referencyjny interpreter (`bench/`, M21) wykonuje testy na specyfikacji i sprawdza, czy są
  spójne. Dla prawdziwej gry testy wykonuje silnik.

<a id="pokrycie"></a>
## Pokrycie digitalizacji
Metryki liczone deterministycznie (`wgc gate stage1_5`), raportowane w `metrics` raportu bramki:

| Metryka | Definicja |
|---|---|
| `rules_total` | reguły Stage 1 w zakresie (`nature ≠ commentary`) |
| `rules_modeled_logically` | reguły z `formalization ∈ {full, partial}` |
| `rules_digitalizable` | reguły mechaniczne (nie: commentary, presentation) |
| `rules_with_state_impact` | reguły z efektami na zmiennych lub stanach (`realizes` w `entity`/`derived`) |
| `rules_with_legality` | reguły zrealizowane przez ≥ 1 `legality` |
| `rules_with_transitions` | reguły zrealizowane przez `action`/`trigger` z efektami i zdarzeniami |
| `rules_with_tests` | reguły w `realizes` ≥ 1 testu |
| `rules_blocked_by_ambiguity` | reguły w zasięgu otwartego `blocker` |
| `rules_requiring_human_interpretation` | reguły z niejasnością `requires_human_interpretation` |
| `cases_with_tests` | przypadki `case` z testem |
| `high_risk_rules_with_boundary_tests` | reguły `high`/`critical` z testem `boundary` |

## Blokery
`blocker` (`BLK-`): `cause` (AMB-, TAB- z `complete: false`, brakujące SRC-), `affects` (rekordy 1.5), `needed`
(co odblokuje: decyzja człowieka, FAQ, brakujący arkusz), `status`, `resolved_by`. Elementy zablokowane mają
`blocked_by`, a ich testy nie liczą się do pokrycia.

## Engine kit (eksport)
`wgc export engine-kit` (M20) tworzy pakiet: rekordy Stage 1.5, tabele Stage 1 w postaci danych, testy, fixture'y
stanu, mapę śledzenia i hash modelu (`ruleset_hash`). Repo silnika przypina wersję pakietu. Pakiet się regeneruje, nie edytuje.

<a id="self-hosted-stage-1-5"></a>
## Self-hosted compute w Stage 1.5
Stage 1.5 to dobry kandydat do intensywnej pracy self-hosted (ADR-0017). Węzeł nie zna domeny: dostaje generyczne
requesty z promptem i schematem dekodowania od TaskSpec WGC.

| Zadanie | Wykonawca (domyślnie) | Premium tylko gdy |
|---|---|---|
| ekstrakcja stanu (`ENT-`, `DER-`) | Tier 0 (szablony) → `local_semantic` | — |
| generowanie akcji i kandydatów legalności | Tier 0 dla zakazów → `local_semantic` (druga ekstrakcja `local_fast`) | spór nierozstrzygnięty przez `local_deep` |
| triggery i zdarzenia | `local_semantic` | ryzyko `high`/`critical` |
| scenariusze i generowanie testów | `local_semantic`, weryfikacja `local_fast` | — |
| kontrole krzyżowe (spec ↔ IR, pokrycie) | Tier 0 + `local_deep` wsadowo | rozbieżność semantyczna |
| niejednoznaczna semantyka, konflikt źródeł, interpretacja wysokiego ryzyka | — | **zawsze premium lub człowiek** |

