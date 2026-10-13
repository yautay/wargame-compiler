# wargame compiler i digitalizacja instrukcji gier

Aktywny kierunek to narzędzie do digitalizacji instrukcji historycznych gier
wojennych. Instruction Graph (IG) zachowuje treść, dowody, znaczenie,
zależności, braki i decyzje człowieka. Wspólny rdzeń uzupełniają osobne
profile SPQR, rodzin OSG i GCACW z MMP.

Pierwszy cel to pełna instrukcja SPQR połączona z istniejącą KB WGU.
IG ma umożliwić kompilację do szybkiego, deterministycznego mechanizmu
legalnych akcji i zmian stanu. Przyszły przeciwnik AI zużywa kontekst
na decyzje strategiczne; legalność oblicza mechanizm reguł bez LLM.
Obecna praca obejmuje wyłącznie architekturę i plan.

Projekt jest na etapie propozycji modelu i planu. Nie ma jeszcze nowego
importera, wykonawcy reguł ani zweryfikowanego pełnego grafu gry.

## Aktywne dokumenty

- [Stan projektu](docs/STATUS.md) i [przekazanie](docs/HANDOFF.md).
- [Plan IG](docs/IG-PLAN.md) i [roadmapa](docs/ROADMAP.md).
- [Architektura WGC: KB WGU i pełna instrukcja do IG](docs/IG-WGU-ARCHITECTURE.md).
- [IG dla deterministycznych legalnych akcji AI](docs/IG-LEGAL-ACTIONS.md).
- [Struktura danych IG](docs/IG-DATA-MODEL.md).
- [Mechaniki i profile](docs/IG-MECHANICS-PROFILES.md).
- [Decyzja o kierunku](docs/adr/ADR-0040-ig-i-archiwum-poc.md).
- [Prompt nowej sesji](docs/prompts/IG-0-critical-review.md).
- [Zasady pracy](CLAUDE.md).

Tekst wydawców, cytaty, obrazy, konkretne reguły, grafy i sytuacje
przechowujemy w private/. Publiczne dokumenty opisują metodę i model.
Akceptacja znaczenia wymaga jawnej decyzji człowieka o dokładnym zakresie.

## Archiwa

[POC SPQR z 2026-10-11](archive/poc-2026-10-11/README.md) zachowuje
cały dotychczasowy stan. Eksperyment pozostaje nieukończony; archiwizacja
nie zalicza POC6–POC7. Manifest pozwala odtworzyć dawne ścieżki i bajty.
[Projekt legacy](archive/legacy-2026-10-07/README.md) pozostaje osobnym archiwum.

## Kontrole

```powershell
pwsh -NoProfile -File scripts/check.ps1
```

Kontrole obejmują aktywne dokumenty, plan i integralność archiwum POC.
Nie potwierdzają działania mechanik gry. Środowisko .venv pozostaje
zasobem narzędziowym; konfiguracja nie instaluje runtime starego projektu.
