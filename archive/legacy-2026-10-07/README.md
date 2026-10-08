# Archiwum legacy — 2026-10-07

`project/` zawiera starą publiczną strukturę w oryginalnych bajtach, także
niezacommitowane i nieśledzone zmiany Q-11, M-DESK1 i M-DESK2. **M-DESK2 pozostaje
partial.** Historyczne instrukcje i statusy wewnątrz projektu nie sterują nowym POC.
Aktywny punkt wejścia: [README repo](../../README.md) i [ADR-0039](../../docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md).

## Co przeniesiono

| Dawna ścieżka | Zachowana lokalizacja |
|---|---|
| `wgc/`, `glu/`, `tests/`, `contracts/`, `bench/`, `docs/` | `project/` z taką samą strukturą wewnętrzną |
| `README.md`, `CLAUDE.md`, `COPYRIGHT.md` | `project/` — oryginalna treść |
| `pyproject.toml`, `requirements.txt`, `.gitignore`, `.gitattributes` | `project/` — oryginalne konfiguracje |
| `.glu/` | `private/archive/legacy-2026-10-07-state/.glu/` od korzenia repo, również stare katalogi testowe |
| `.pytest_cache/`, `wargame_compiler.egg-info/` | `private/archive/legacy-2026-10-07-state/` — wygenerowane zasoby starego środowiska |

[Mapa publicznych plików](movement-map.json) zawiera 237 oryginalnych ścieżek,
lokalizacje docelowe, rozmiary i pełne SHA-256. Nie obejmuje odtwarzalnego bytecode/cache.
Pełna mapa 392 plików, także prywatnych, jest w
`private/archive/2026-10-07-pre-poc/movement-map.json`. Mapa przeniesień katalogów
jest obok jako `planned-root-moves.json`.

`private/source-artifacts/` pozostaje w pierwotnym miejscu bez zmiany treści;
snapshot zachowuje również jego kopię. `.git` i historia pozostały nietknięte,
bez commita/pusha. `.venv` pozostaje w korzeniu jako istniejące środowisko weryfikacji.
Zarządzanych konfiguracji agentów i logowania nie przenoszono ani nie kopiowano;
w inwentaryzowanym korzeniu nie znaleziono takich katalogów.

## Snapshot i odtwarzanie

Snapshot: `private/archive/2026-10-07-pre-poc/` od korzenia repo.

- `payload/`: 392 pliki, **81 319 086 bajtów**; kod, dokumenty, fixture’y,
  źródłowe pakiety, odpowiedzi, metadane, dowody i istotne wyniki `.glu/`.
- `manifest.json`, `manifest.sha256`: ścieżki, rozmiary, hashe, HEAD/gałąź/stan Git
  i jawne wyłączenia; dodatkowo stan Git i pomocnicze patche zmian staged/unstaged.
- `verification.json`, `restore-check/`: wszystkie 392 hashe sprawdzone przed
  reorganizacją i po odtworzeniu do nowego katalogu; zero różnic.
- `post-move-verification.json`: te same pliki po przeniesieniu, zero różnic.

Wyłączono `.git`, `.venv`, wygenerowane egg-info, pytest/bytecode oraz wielotysięczne
katalogi basetemp: `.glu/desktop-export-tests`, `.glu/desktop-plan-tests`,
`.glu/desktop-contract-tests/focused-1` i `full-1`. Oryginałów tych katalogów nie
usunięto — przeniesiono je z całym starym stanem. Zachowano logi, raporty, odpowiedzi
Q-11 i M-DESK oraz obrazy kontroli. Snapshot nie obejmuje swojego celu ani konfiguracji
logowania/sekretów. Nie kopiuje zewnętrznego PDF z repo `C:\dev\spqr`.

Aby odtworzyć bez nadpisania nowego projektu, uruchom w PowerShell z korzenia repo:

```powershell
$restoreTarget = Join-Path (Get-Location) ('private\archive\restore-' + [guid]::NewGuid().ToString('N'))
.\.venv\Scripts\python.exe archive/legacy-2026-10-07/restore.py --snapshot private/archive/2026-10-07-pre-poc --destination $restoreTarget
```

[Skrypt odtwarzania](restore.py) odrzuca istniejący cel, sprawdza manifest i wszystkie
bajty przed kopiowaniem, a potem hashe kopii. Nie przywraca `.git`, nie aplikuje patchy
i nie modyfikuje aktywnej struktury. Po awarii zachowuje częściową kopię do diagnozy;
ponowienie wymaga nowego celu. Przenieś/skopiuj kompletny katalog snapshotu na inny
nośnik, jeśli potrzebna jest ochrona przed awarią całego dysku; w tej sesji sprawdzono
odtwarzanie lokalne, bez zewnętrznego backupu. Historia Git pozostaje w pierwotnym `.git`.

Snapshot i mapa odnoszą się do oryginalnych bajtów plików roboczych. Zachowana
`project/.gitattributes` nadal zawiera historyczną politykę normalizacji końców linii;
przyszły staging/checkout może znormalizować CRLF. Nie wykonywano stagingu.
Do odtworzenia dokładnych oryginalnych bajtów używaj snapshotu i kontroli SHA-256,
nie samego przyszłego checkoutu.

Dodatkowa próba dostarczonego `restore.py` odtworzyła wszystkie 392 pliki do
`private/archive/restore-cli-check-2026-10-07/` z zerem różnic. Ponowienie do istniejącego
celu zostało odrzucone bez nadpisania. `.venv` i wersje jej bibliotek są zasobem
środowiska, nie częścią payload; zapis wersji znajduje się w prywatnym `environment.json`.

## Oddzielne uruchomienie legacy

Zachowana `.venv` dostarcza Python i już zainstalowane zależności. Uruchamiaj moduły
z **własnego katalogu projektu**, bez instalacji edytowalnej w aktywnym korzeniu:

```powershell
Set-Location C:\dev\wargame-compiler\archive\legacy-2026-10-07\project
$legacyPython = 'C:\dev\wargame-compiler\.venv\Scripts\python.exe'
& $legacyPython -c "import pathlib,wgc,glu; r=pathlib.Path.cwd().resolve(); print(wgc.__file__, glu.__file__); assert all(pathlib.Path(m.__file__).resolve().is_relative_to(r) for m in (wgc,glu))"
& $legacyPython -m wgc --help
& $legacyPython -m glu --help
```

Nie uruchamiaj historycznych providerów inferencji. CLI help oraz testy offline
wystarczają do sprawdzenia izolacji. Pełne testy z nowym lokalnym basetemp:

```powershell
$legacyCheck = 'C:\dev\wargame-compiler\private\archive\2026-10-07-pre-poc\checks\legacy-' + [guid]::NewGuid().ToString('N')
New-Item -ItemType Directory -Path $legacyCheck | Out-Null
$env:TMP = Join-Path $legacyCheck 'temp'
$env:TEMP = $env:TMP
New-Item -ItemType Directory -Path $env:TMP | Out-Null
$env:PYTHONDONTWRITEBYTECODE = '1'
$legacyBase = Join-Path $legacyCheck 'pytest'
if (Test-Path -LiteralPath $legacyBase) { throw 'Basetemp już istnieje' }
& $legacyPython -m pytest -q --basetemp $legacyBase -p no:cacheprovider --tb=short
```

Zmienne dotyczą tylko tej powłoki; nie zapisuj ich globalnie. Zakończ powłokę po
sprawdzeniu lub przywróć jej poprzednie wartości. Dla odtworzonej kopii zamiast
`project/` ustaw katalog `$restoreTarget`; zależności opisują zachowane
[requirements.txt](project/requirements.txt) i [pyproject.toml](project/pyproject.toml).
Nie instalowano dodatkowych zależności.

Weryfikacja M-POC0: oba importy wskazały `project/`, oba CLI help zakończyły się
kodem 0; pełne testy **807 passed, 1 skipped**, 156,27 s. Logi:
`private/archive/2026-10-07-pre-poc/checks/legacy-cd4230d3bc574269b20cafa15e87ef90/`.
Kontrole te nie potwierdzają jakości SPQR ani ukończenia M-DESK2.
