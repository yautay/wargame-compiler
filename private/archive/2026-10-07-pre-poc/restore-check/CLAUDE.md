# wargame-compiler: bootstrap dla sesji AI

**Zanim cokolwiek zrobisz:** przeczytaj `docs/SESSION-PLAYBOOK.md`, potem `docs/STATUS.md` i plik wskazany
w `docs/HANDOFF.md`. Pracujesz nad **jednym** milestone'em z `docs/ROADMAP.md` (bieżący jest w STATUS). Nie kontynuuj
z pamięci rozmowy, bo stan projektu jest w plikach.

## Zasady repo
- To repo **narzędzia**. Dane gier żyją w repozytoriach gier (`project.yaml`, `source/`, `kb/`). Nie dodawaj tu
  niczego specyficznego dla jednej gry komercyjnej ani tekstów wydawców (ADR-0012). Benchmark = `bench/minigame` (tekst własny, CC0).
- Pakiety: `wgc` (domena, rola „WGU”), `glu` (wykonanie) i `igw` (Inference Gateway węzła, od M-GW1). `wgc` nie
  importuje `glu` (ADR-0002); `igw` nie importuje `wgc` ani `glu` (ADR-0016).
- Inference: „local” = **self-hosted**. Lokalny worker i sprzęt RTX 3090 są opcjonalne; nie ma automatycznej
  eskalacji do API przy ich niedostępności (ADR-0037, zastępuje obowiązkową topologię ADR-0015).
- **Kierunek od 2026-10-06 (ADR-0037, nadrzędny wobec starszych opisów inferencji):** premium wyłącznie przez
  ChatGPT lub Claude Desktop, wymiana pakietów plikowych, **bez API inferencji**. Lokalny LLM opcjonalny przez
  proces/pliki; gateway LAN nie jest zależnością. Przebudowujemy istniejący ingest, zachowując rdzeń WGC/GLU.
  Przed implementacją przeczytaj `docs/DESKTOP-IMPLEMENTATION-PLAN.md`; aktywna kolejność to M-DESK, nie dawny M10.
- Kontrakty: `contracts/schemas/*.schema.json`. Zmiana kontraktu w tej samej sesji aktualizuje fixture'y
  (`contracts/fixtures/`), testy i `docs/DATA-CONTRACTS.md`. Od `@1` pola usuwane lub przemianowane wymagają
  podbicia wersji, ADR i migracji.
- Kod: Python ≥ 3.10, zależności tylko z `requirements.txt`. Nazwy pól i kod po angielsku. Dokumentacja, komunikaty
  dla użytkownika i skille po polsku.
- Testy: `python -m pytest`. Żaden test nie może wymagać GPU, sieci ani modelu (ADR-0008). Test ciągłości
  (`tests/test_continuity.py`) musi być zielony na koniec sesji.
- Decyzje architektoniczne → nowy ADR (`docs/adr/`). Zapisuj fakty, decyzje i stan, nie tok rozumowania.
- Commit i push tylko na prośbę właściciela.
- Windows: długie skrypty i pliki z backslashami pisz narzędziem Write, nie heredokiem. W YAML nie używaj kluczy
  `on`/`yes`/`no` (`docs/DATA-CONTRACTS.md` §6).

## Koniec sesji
Testy zielone → ROADMAP (status milestone'u) → STATUS (nowy bieżący milestone) → handoff `docs/handoff/RRRR-MM-DD-Mn.md`
→ wskaźnik w `docs/HANDOFF.md`.
