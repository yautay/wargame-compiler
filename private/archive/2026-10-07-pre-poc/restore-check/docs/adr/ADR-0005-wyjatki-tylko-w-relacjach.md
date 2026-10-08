# ADR-0005: Wyjątki i nadpisania wyłącznie w relacjach

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
W `wgu/kb@1` wyjątki zapisywano dwa razy: w polu tekstowym reguły (`exceptions: → R-9.0.8`) i w `relations.yaml`.
Takie zapisy mogą się rozjechać. Digitalizacja wymaga jawnego modelu pierwszeństwa, a nie kolejności ifów.

## Decyzja
Rekord `relation` (`REL-…`) to jedyne miejsce zapisu wyjątków, nadpisań i pierwszeństwa. Ma typ (`exception_to`,
`overrides`, `replaces`, `modifies`, `requires`, `precedes`…) i pole `priority_basis`. Reguła nie ma pola `exceptions`.
Widoki i Stage 1.5 (`priority`, `legality.unless`) wyprowadzają wyjątki z relacji.

## Konsekwencje
Walidator może sprawdzać kompletność. Marker wyjątku w tekście źródła („except”, „unless”, „exception”) bez
odpowiadającej relacji to ostrzeżenie i sygnał ryzyka.
