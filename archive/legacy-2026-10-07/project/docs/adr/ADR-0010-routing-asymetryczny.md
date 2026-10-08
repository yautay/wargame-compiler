# ADR-0010: Routing asymetryczny oparty na deterministycznym ryzyku

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Próba SPQR z 2026-10-04 (stare repo, `docs/proby/`):
- kontrola mechaniczna wykryła 5/6 wstrzykniętych błędów i **przeoczyła zawężenie „osiągnie lub przekroczy” →
  „przekroczy”** (≥ → >);
- ślepy weryfikator premium wykrył 6/6;
- pierwsza wersja heurystyk dała 8/8 fałszywych alarmów.

Samoocena modelu nie jest wiarygodna.

## Decyzja
- Routing opiera się na **deterministycznym modelu ryzyka** (`wgc/risk@N`): cechy tekstu źródła, grafu KB i procesu.
- **Twarde reguły eskalacji** działają niezależnie od wyniku punktowego. Przykłady:
  - operator graniczny w źródle,
  - niezgodność sygnałów źródła z IR,
  - rozbieżność dwóch niezależnych ekstrakcji lokalnych.
- Samoocena modelu to tylko jeden sygnał.
- Asymetria: w razie wątpliwości eskalujemy. Wynik fałszywie negatywny kosztuje więcej niż zbędna eskalacja.
- Losowy audyt premium próbki rekordów zaakceptowanych lokalnie mierzy odsetek wyników fałszywie negatywnych.
- Każda decyzja routingu jest zapisana (`routing_decision`) i da się ją odtworzyć z sygnałów i wersji polityki.

## Konsekwencje
Wagi ryzyka kalibruje benchmark mutacyjny (`docs/QUALITY.md`). Zmiana wag to nowa wersja modelu ryzyka.
