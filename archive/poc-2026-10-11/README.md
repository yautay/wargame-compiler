# Archiwum POC SPQR z 2026-10-11

Właściciel polecił zachować cały dotychczasowy POC i oprzeć aktywny
projekt na planie IG. Archiwum zawiera stan roboczy, również
niezacommitowane i nieśledzone pliki, oryginalne odpowiedzi i pomiary.

**Eksperyment nie został ukończony.** Ostatni zapis POC5B przedstawia
40 porównań sytuacji oczekujących decyzji właściciela. Starsze kwestie
pozostają otwarte. POC6–POC7 nie wykonano. Archiwizacja nie stwierdza
sukcesu ani porażki modelu.

## Zawartość i dawne ścieżki

| Dawna lokalizacja od korzenia repo | Zachowana lokalizacja |
|---|---|
| README.md, CLAUDE.md, pyproject.toml, .gitignore, .gitattributes | `project/` z oryginalnymi bajtami |
| docs/, scripts/, tests/ | `project/` z zachowaną strukturą |
| private/poc/ | `private/archive/poc-2026-10-11/payload/private/poc/` od korzenia repo |
| private/source-artifacts/ | `private/archive/poc-2026-10-11/payload/private/source-artifacts/` od korzenia repo |

Snapshot obejmuje też kopię istniejących draftów IG. Ich rozwijane wersje
są w [aktywnych docs](../../docs/IG-DATA-MODEL.md).
`.git`, `.venv`, wcześniejsze archiwa i nowe `private/ig/` pozostały na miejscu.

Pełny manifest: `private/archive/poc-2026-10-11/manifest.json` od korzenia
repo. Wpis ma `original_path`, `archive_path`, wielkość i SHA-256.
[verification.json](verification.json) podaje liczbę plików, wynik
weryfikacji i hash manifestu. Prywatne listy plików pozostają prywatne.

## Weryfikacja i odtworzenie

Uruchom `scripts/check.ps1` z aktywnego korzenia repo. Kontrole sprawdzają
wszystkie pliki POC z manifestu. Historyczne testy są w `project/tests/`.

Dawne ścieżki w JSON i dokumentach zachowano bez zmian. Odczyt rozwiązuje
mapa manifestu. Odtworzenie do osobnego pustego katalogu polega na kopiowaniu
każdego `archive_path` do jego `original_path` i ponownym sprawdzeniu hashy.
Nie nadpisuj aktywnego repo. Niektóre linki i bootstrapy wskazują historyczny
korzeń lub starsze archiwum; pełne odtworzenie środowiska wymaga tych
zależności. Manifest potwierdza zachowanie danych, nie działanie runtime'u.

Nowy punkt wejścia: [README repo](../../README.md),
[plan IG](../../docs/IG-PLAN.md) i
[ADR-0040](../../docs/adr/ADR-0040-ig-i-archiwum-poc.md).
