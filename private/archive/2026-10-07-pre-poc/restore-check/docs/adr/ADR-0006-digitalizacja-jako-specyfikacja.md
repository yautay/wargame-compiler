# ADR-0006: Stage 1.5 to specyfikacja i testy, nie wykonywalny DSL reguł

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Silnik `spqr` (ADR-0004 w tamtym repo) odrzucił DSL reguł w YAML/JSON, bo SPQR to „wyjątki na wyjątkach”.
Procedury i wyjątki są tam kodem, a tabele, parametry i opcje danymi. Śledzenie zapewniają adnotacje `@rule` i testy.
Prompt wymaga specyfikacji „architecture-ready”, niezależnej od silnika, z testami i traceability.

## Decyzja
Stage 1.5 produkuje **specyfikację**:
- schemat stanu,
- katalog akcji i predykaty legalności z `reason_code`,
- efekty i zdarzenia,
- model timingu, triggery, decyzje, losowość, informację ukrytą,
- inwarianty, pierwszeństwo, blokery,
- **testy Given/When/Then w kanonicznym formacie stanu**.

Predykaty używają małej gramatyki Rule IR i mogą zawierać jawne liście `{text}`. Specyfikacja nie musi być wykonywalna.
Silnik implementuje reguły w kodzie, a zgodność dowodzą testy specyfikacji. Dla gry benchmarkowej powstaje
referencyjny interpreter testów (`bench/`), który sprawdza spójność samej specyfikacji.

## Konsekwencje
- Nie budujemy języka reguł ani dowodzenia twierdzeń.
- Pakiet dla silnika (`engine kit`) to dane, tabele, testy i mapa śledzenia. Silnik odsyła wyniki testów, co daje
  śledzenie odwrotne.

## Odrzucone warianty
Pełny wykonywalny DSL: drogi i kruchy przy grach z gęstymi wyjątkami.
