# ADR-0008: Runtime WSL2, core wieloplatformowy, testy bez GPU

- **Status:** zastąpiony przez ADR-0015
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Maszyna docelowa to Windows 11, WSL2 Ubuntu i RTX 3090 (24 GB). Maszyna, na której powstała Session 0, nie ma GPU
(`nvidia-smi` niedostępne). Ma WSL2 Ubuntu-22.04 i Pythona 3.13 po stronie Windows. Stare narzędzie wpadało w
pułapki Windows: heredoc w PowerShell, backslashe, BOM, MiKTeX (stare repo, `templates/docs/pulapki.md`).

## Decyzja
- Główny runtime GLU, providerów lokalnych i LaTeX (TeX Live) to **WSL2 Ubuntu** z venv po stronie Linuksa.
- Kod `wgc` i `glu` jest wieloplatformowy (pathlib, UTF-8, LF). Testy przechodzą na Windows i na Linuksie.
- **Żaden test nie wymaga GPU, sieci ani modelu.** Służą do tego provider `fake` (deterministyczny) i `replay`
  (nagrane odpowiedzi).
- Claude Desktop (Windows) łączy się z serwerem MCP przez `wsl.exe` (stdio).
- Repo gier najlepiej trzymać w systemie plików WSL, bo `/mnt/c` działa wolno przy wielu małych plikach.

## Konsekwencje
Instrukcje środowiskowe trafiają do `docs/INFERENCE-ROUTING.md` (lokalna inferencja) i `docs/MCP.md`.
