# ADR-0002: Nazwy: `wargame-compiler`, pakiety `wgc` i `glu`

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Prompt rozróżnia WGU (narzędzia domenowe) i GLU (wykonanie). Stare narzędzie zajmuje nazwy `wgu` (pakiet Python,
skrypt CLI) i `wgu@wargame-utils` (plugin Claude Code). Druga instalacja o tych samych nazwach przesłoniłaby stare CLI.

## Decyzja
- Dystrybucja `wargame-compiler`, repo `C:/dev/wargame-compiler`.
- Pakiet **`wgc`** pełni rolę „WGU” z promptu: kontrakty, KB, walidatory, narzędzia deterministyczne, specyfikacje zadań.
- Pakiet **`glu`** odpowiada za wykonanie i orkiestrację. To osobny pakiet, nie podprzestrzeń `wgc`.
- CLI: `wgc` (domena) i `glu` (wykonanie). Plugin Claude Code, jeśli powstanie, nazywa się `wgc@wargame-compiler`.
- Zależności biegną w jedną stronę: `glu` importuje `wgc` (przez interfejs specyfikacji zadań), `wgc` nigdy nie importuje `glu`.

## Konsekwencje
Oba narzędzia mogą działać obok siebie. W dokumentacji „WGU” z promptu oznacza pakiet `wgc`.

## Odrzucone warianty
- `wgu2`: nazwa robocza bez znaczenia.
- `wgu` w osobnym venv: kolizja przy pierwszym `pip install -e` w złym środowisku.
