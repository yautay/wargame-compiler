# ADR-0004: KB w git jako źródło prawdy, stan wykonania w `.glu/`

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
YAML w git sprawdził się w `wgu`: baza jednej gry ma setki KB, da się ją przeglądać, porównywać i deterministycznie
przeszukiwać (stare repo, `docs/ARCHITECTURE.md` §4). Nowy system wykonuje setki jobów lokalnych z próbami, cache
i metrykami. To stan operacyjny, a nie wiedza o grze.

## Decyzja
- **Wiedza domenowa** żyje jako YAML w repo gry (`kb/`, `source/inventory.yaml`): Stage 0–3, decyzje `HD-`, prośby
  o przegląd `RR-`. Kanoniczne są tylko rekordy `accepted`.
- **Stan wykonania** żyje w `.glu/` w repo gry (SQLite i bloby adresowane treścią), dodanym do `.gitignore`:
  Build, Job, Attempt, RoutingDecision, cache, wyjścia, metryki. Utrata `.glu/` kosztuje tylko ponowne obliczenia, nie wiedzę.
- Świeżość (staleness) da się wyliczyć z samego `kb/`: kotwice mają `seg_hash`, a provenance ma `inputs_hash`.
- GLU zapisuje do `kb/` wyłącznie przez walidatory WGC: propozycja → walidacja → akceptacja.

## Konsekwencje
GLU nie ma konkurencyjnej bazy wiedzy. Raporty buildów i metryki, które trzeba zachować, eksportuje się jawnie
do `reports/`.

## Odrzucone warianty
Baza dokumentowa lub wektorowa jako źródło prawdy: nie ma diffów, przeglądu w PR ani deterministycznego wyszukiwania.
