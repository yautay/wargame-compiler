# ADR-0012: Tekst źródła poza repozytoriami, kotwice z hashami

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Instrukcje wydawców są chronione prawem autorskim. Stare projekty trzymały PDF-y i wyciągnięty tekst poza repo
(`.gitignore` w wg-spqr), a próba tłumaczenia trzymała fragmenty w scratchpadzie. Ekstrakcja bywa zawodna
(przekreślenia, pomieszane kolumny tabel w Ukraine43), więc musi być deterministyczna i sprawdzalna renderem strony.

## Decyzja
- Repo gry commituje **inwentarz źródeł i mapę segmentów** (`SRC-`, `SEG-` z `text_hash`), bez tekstu.
- Tekst segmentów jest deterministycznie odtwarzany do `.glu/source/` i sprawdzany z `text_hash`.
- Kotwica (`anchor`) wskazuje segment i jego hash. Może mieć krótki cytat (≤ ok. 25 słów) do kontroli deterministycznych.
- Repo narzędzia zawiera wyłącznie teksty własne (benchmark `bench/minigame`, CC0). Benchmarki na grach komercyjnych
  żyją w `private/` (gitignored) i odwołują się do lokalnych repo gier.

## Konsekwencje
Pakiety premium review zawierają minimalny fragment źródła tylko w pamięci albo w `.glu/`, nigdy w commitach.
