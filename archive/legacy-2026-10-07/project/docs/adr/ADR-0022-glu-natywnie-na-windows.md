# ADR-0022: GLU na dev machine działa natywnie na Windows

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M2b (decyzja właściciela przed M8)

## Kontekst
- ADR-0015 ustalił, że dev machine (Claude Desktop, MCP, GLU, repo gier, `.glu/`) nie wymaga GPU ani WSL2. Wybór
  między Windows natywnie a WSL2 zostawił jako decyzję wdrożeniową (STATUS Q-03, termin: przed M8).
- M8 tworzy job store w SQLite w `.glu/`, więc środowisko GLU decyduje o położeniu bazy i repo gier.
- WGC (M1, M2a, M2b) jest już rozwijane i testowane natywnie na Windows (Python 3.13).

## Decyzja
- GLU na dev machine działa **natywnie na Windows**, bez WSL2.
- Repo gier, `.glu/` i baza SQLite job store leżą w systemie plików Windows (NTFS).
- Claude Desktop uruchamia serwer MCP (`glu mcp serve`) bezpośrednio, bez `wsl.exe`.
- Core WGC i GLU pozostaje wieloplatformowy: kod nie zakłada Windows (`pathlib`, ścieżki POSIX w danych, zapis z `\n`),
  a testy działają na Windows i Linuksie (ADR-0015).

## Konsekwencje
- Q-03 jest zamknięta. Repo gier nie trzeba trzymać w systemie plików WSL.
- M8 może zakładać SQLite na NTFS: plik bazy otwierany i zamykany jawnie (blokady plików Windows), bez założeń
  o semantyce POSIX.
- Polecenia GLU (M8, `[project.scripts]`) i serwer MCP (M22) uruchamia się natywnie. Wariant z `wsl.exe` w MCP.md
  przestaje być ścieżką domyślną.
- Nie rozstrzyga środowiska LaTeX (TeX Live) dla publikacji (M29): ADR-0015 zostawia wybór WSL2 albo natywnie.
- Nie dotyczy węzła inferencji (ADR-0015, ADR-0018).

## Odrzucone warianty
- **GLU w WSL2:** wymagałby repo gier w systemie plików ext4 WSL (wydajność I/O), opakowania MCP w `wsl.exe` i dwóch
  środowisk Pythona na jednej maszynie, bez korzyści dla GLU, które nie potrzebuje GPU ani narzędzi linuksowych.
