# ADR-0007: Referencyjny kształt silnika: decyzje → zdarzenia → reduktor

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Prompt wymaga undo/redo, replay, save/load, deterministycznych testów i wstrzykiwanej losowości. Silnik `spqr`
z powodzeniem używa:
- czystego stanu,
- `step(state, input) → {state, events, trace, pending}`,
- żądań decyzji z wyliczonymi opcjami,
- zapisu `{seed, inputs, snapshot, hash}`.

## Decyzja
Specyfikacja Stage 1.5 zakłada (ale nie implementuje) silnik o kształcie:
1. Każde wejście uczestnika to odpowiedź na **DecisionRequest** z listą legalnych opcji (`decision_point`).
2. `can_perform(state, action) → ok | reason_code` to czysta funkcja, oddzielona od `perform`.
3. `perform(state, action, random_outcomes, decisions) → events`, a reduktor `apply(state, event) → state`.
4. Wynik losowania jest częścią zdarzenia (`DieRolled`). Replay nie losuje ponownie.
5. Zapis to snapshot (`wgc/state@0`), log zdarzeń i wersje (formatu i modelu cyfrowego). Undo odtwarza stan n−1
   od ostatniego snapshotu.

Pełny event sourcing nie jest obowiązkowy. Wystarczy, że z logu zdarzeń da się odtworzyć stan.

## Konsekwencje
Testy specyfikacji są przenośne między silnikami. Test wstrzykuje wyniki losowe, odpowiada na decyzje, a potem
sprawdza zdarzenia i stan.
