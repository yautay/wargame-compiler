# ADR-0014: Rodzaj provenance nadaje WGC, nie model

- **Status:** przyjęty; punkt „w przeciwnym razie `llm_inference`” zastąpiony przez ADR-0027
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
W `wgu/kb@1` wnioski oznaczał sam analityk: znacznikiem `[wniosek]` w notatce i flagą `inference`. Prompt (§4)
zabrania zapisywania inferencji jako treści instrukcji.

## Decyzja
- Model zwraca propozycję **bez** pola `prov`. GLU dopisuje wykonawcę: tier, profil, prompt, job.
- Rodzaj (`kind`) ustala WGC:
  - `explicit_source` tylko wtedy, gdy każda kotwica wskazuje istniejący segment o zgodnym hashu, a cytat (jeśli jest)
    występuje dosłownie w znormalizowanym tekście segmentu;
  - w przeciwnym razie `llm_inference` z `derived_from`;
  - `errata`, `faq` i `designer_clarification` wynikają z roli dokumentu źródłowego;
  - `human_decision` wymaga rekordu `HD-`.
- Schemat już teraz wymusza część tych reguł (fixture'y w `contracts/fixtures/invalid/`).

## Konsekwencje
Inferencja nie może udawać źródła, nawet gdy model twierdzi inaczej.
