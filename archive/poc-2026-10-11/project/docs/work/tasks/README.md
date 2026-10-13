# Karty pojedynczych sesji

Status milestone'ów: [ROADMAP](../../ROADMAP.md). Bieżąca karta i blokady:
[STATUS](../../STATUS.md). Metoda i limity: [POC-PLAN](../../POC-PLAN.md).
Każda karta ma wejścia, wynik, sposób oceny i przekazanie. Nie jest automatyczną kolejką.

| Milestone | Karta | Rola |
|---|---|---|
| M-POC0 | [M-POC0 — Archiwum, wnioski i plan](M-POC0.md) | Codex |
| M-POC1 | [M-POC1A — Źródło i ręczny inwentarz](M-POC1A.md) | Codex; przegląd wspólny |
| M-POC1 | [M-POC1B — Oczekiwania i 15–20 sytuacji](M-POC1B.md) | Przegląd wspólny |
| M-POC1 | [M-POC1C — Przegląd i zamrożenie eval-v1](M-POC1C.md) | Właściciel; Codex zapisuje decyzję i hashe |
| M-POC2 | [M-POC2A — Pakiet wejściowy i minimalny format](M-POC2A.md) | Codex |
| M-POC2 | [M-POC2B — Pierwsza ręczna ekstrakcja](M-POC2B.md) | Codex w ręcznej sesji; właściciel obsługuje przekazanie |
| M-POC3 | [M-POC3 — Raport pierwszego wyniku](M-POC3.md) | Codex; przegląd wspólny rozbieżności |
| M-POC4 | [M-POC4A — Wybór ograniczonego kontekstu](M-POC4A.md) | Codex; przegląd wspólny źródeł |
| M-POC4 | [M-POC4B — Odpowiedź z kontekstem i jej kontrola](M-POC4B.md) | Codex w ręcznej sesji; przegląd wspólny |
| M-POC5 | [M-POC5A — Przegląd znaczenia reguł](M-POC5A.md) | Przegląd wspólny; akceptuje właściciel |
| M-POC5 | [M-POC5B — Ocena 15–20 sytuacji](M-POC5B.md) | Przegląd wspólny; akceptuje właściciel |
| M-POC6 | [M-POC6A — Jedna ograniczona korekta w rozmowie](M-POC6A.md) | Codex w ręcznej rozmowie; właściciel przy kwestiach znaczenia |
| M-POC6 | [M-POC6B — Ponowna ocena, regresje i koszt](M-POC6B.md) | Codex; przegląd wspólny |
| M-POC7 | [M-POC7A — Porównanie wyników i warianty dalszej pracy](M-POC7A.md) | Codex |
| M-POC7 | [M-POC7B — Decyzja właściciela i następny plan](M-POC7B.md) | Właściciel; przegląd wspólny |

M-POC6A/B można wywołać z M-POC3–M-POC5 jako ograniczoną korektę, następnie
wrócić do przerwanej karty. Nie zmienia to milestone'u next na późniejszy ani nie
oznacza wykonania M-POC6 z góry. Każda powtórzona runda to osobna sesja i nowe ID
artefaktów; maksymalnie trzy korekty oraz dwie rundy kontekstu.
Podział karty przed wykonaniem wymaga dopisania kart i aktualizacji indeksu,
ROADMAP oraz STATUS; nie uruchamiamy kilku dużych kart w jednej sesji.

## Podział M-POC5A przed oceną, 2026-10-10

- [M-POC5A.1 — Integralność, pełny rejestr i pierwsze rozbieżności](semantic/M-POC5A.1.md)
- [M-POC5A.2 — EXP-001–025](semantic/M-POC5A.2.md)
- [M-POC5A.3 — EXP-026–050](semantic/M-POC5A.3.md)
- [M-POC5A.4 — EXP-051–074 i rozliczenie całości](semantic/M-POC5A.4.md)

Podział części .4 przed wykonaniem, 2026-10-10:

- [M-POC5A.4a — EXP-051–074](semantic/M-POC5A.4a.md)
- [M-POC5A.4b — Relacje obu wyników](semantic/M-POC5A.4b.md)
- [M-POC5A.4c — Lokatory i granice glifów](semantic/M-POC5A.4c.md)
- [M-POC5A.4d — Inwentarz, pending i rozliczenie](semantic/M-POC5A.4d.md)

Podział .4b przed wykonaniem, 2026-10-11:

- [M-POC5A.4b1 — Cele z dostępnym źródłem, wzmianki, kontynuacje i nowe relacje](semantic/M-POC5A.4b1.md)
- [M-POC5A.4b2 — Pierwsza partia pozostałych brakujących celów](semantic/M-POC5A.4b2.md)
- [M-POC5A.4b3 — Wszystkie pozostałe cele](semantic/M-POC5A.4b3.md)

Rozłączne listy 65/30/36 ID rozliczają 126/131 wystąpień. Następna osobna
sesja .4b1; oszacowanie i dalszy podział przed wykonaniem, jeśli potrzebny.


## Podział przeglądu lokatorów przed wykonaniem — 2026-10-11

- [M-POC5A.4c1](semantic/M-POC5A.4c1.md): 22 ID /44 wystąpień.
- [M-POC5A.4c2](semantic/M-POC5A.4c2.md): 21 ID /42 wystąpień.
- [M-POC5A.4c3](semantic/M-POC5A.4c3.md): 22 ID /38 wystąpień.

Podział inwentarza M-POC5A.4d: [M-POC5A.4d1](semantic/M-POC5A.4d1.md), [M-POC5A.4d2](semantic/M-POC5A.4d2.md), [M-POC5A.4d3](semantic/M-POC5A.4d3.md), [M-POC5A.4d4](semantic/M-POC5A.4d4.md), [M-POC5A.4d5](semantic/M-POC5A.4d5.md). Dokładne przydziały przygotowane przed oceną, jedna część na sesję.


Stan po .4d4 (2026-10-11): rzeczywiście porównano cały przydział 41 pozycji/82 wystąpienia. Łącznie 207/207 pozycji i 414/414 porównań; 332 wcześniejsze zakresy z decyzjami, 82 nowe waiting_review. Po decyzjach obecnego pakietu osobna [M-POC5A.4d5](semantic/M-POC5A.4d5.md) i M-POC5B40 ocen sytuacji; nadrzędne karty partial, starsze nierozstrzygnięcia otwarte.


Stan po .4d5 (2026-10-11): .4d4 zatwierdzona82 ocen; całe uzgodnienie .4d5 wykonane i waiting_review.414 wcześniejszych zakresów inwentarza przyjęte, po63/66 lokalne zakresy i3/8 wymagania źródła zachowane. Po decyzji raportu pozostaje osobne M-POC5B20 sytuacji/40 ocen, z szacunkiem przed rozpoczęciem. Starsze8 oczekiwań/13 kwestii otwarte; nadrzędne karty partial.


Stan po M-POC5B (2026-10-11): zatwierdzono dokładne .4d5 uzgodnienie; wszystkie20 sytuacji w obu odpowiedziach porównano (40 ocen).35 pozytywnych propozycji i5 osobnych oczekuje właściciela, pełne3 wnioski zawieszone po porównaniu. Bieżąca kartaM-POC5B, M-POC5 jedyny next; szerszeM-POC5A i starsze8 oczekiwań/13 kwestii nadal partial/otwarte.
