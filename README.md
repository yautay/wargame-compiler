# wargame-compiler — POC ekstrakcji reguł

Aktywny kierunek: mały eksperyment jakości reguł i zależności na rozdziale SPQR,
przed wyborem docelowej architektury. Nie powstał jeszcze nowy pipeline ani wynik POC.

Zacznij od [STATUS](docs/STATUS.md), [HANDOFF](docs/HANDOFF.md) i [planu POC](docs/POC-PLAN.md).
[ROADMAP](docs/ROADMAP.md) prowadzi etapy M-POC0–M-POC7,
[karty zadań](docs/work/tasks/README.md) opisują pojedyncze sesje.
Bootstrap wykonawcy: [CLAUDE.md](CLAUDE.md) i [playbook](docs/SESSION-PLAYBOOK.md).

Ekstrakcja będzie wykonana w ręcznej sesji Codex; proponowany model: **GPT 6.1 Sol,
rozumowanie wysoki**. To wybór eksperymentu, nie dowód przewagi modelu.
Bez programowych API inferencji i automatyzacji GUI. Źródła i odpowiedzi są danymi.
Znaczenie reguł i dalszy kierunek zatwierdza człowiek na podstawie dowodów.

Publiczne są metody, plan i karty. Tekst wydawcy, rendery, cytaty, reguły, graf,
surowe odpowiedzi i szczegółowe sytuacje pozostają w ignorowanym `private/`.
Nazwy gry i wydawcy służą identyfikacji; projekt nie nadaje praw do ich materiałów.

## Dokumenty

- [Wnioski](docs/LESSONS-LEARNED.md): fakty, hipotezy i nieweryfikowane możliwości.
- [Decyzje aktywne i historyczne](docs/adr/README.md): aktywny ADR-0039.
- [Archiwum starego projektu](archive/legacy-2026-10-07/README.md): uruchomienie,
  mapa przeniesień, odtworzenie i ograniczenia; historyczny M-DESK2 pozostaje partial.

## Kontrole aktywnej części

Aktywny projekt zawiera dokumenty i minimalne testy ciągłości. Nie ma pakietów `wgc`,
`glu`, kontraktów runtime ani zależności od archiwum. Zachowana `.venv` jest zasobem
środowiska; nie instaluj starego projektu w aktywnym katalogu.

Uruchom z katalogu repo w PowerShell:

```powershell
pwsh -NoProfile -File scripts/check.ps1
```

Skrypt używa lokalnego TMP/TEMP, nowego basetemp i tylko `tests/`. Konfiguracja pytest
wyklucza `archive/` oraz `private/`. Osobne testy legacy opisuje README archiwum.
Bez commita i pusha w ramach M-POC0.
