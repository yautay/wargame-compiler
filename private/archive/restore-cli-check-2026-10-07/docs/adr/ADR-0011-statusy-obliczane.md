# ADR-0011: Statusy i widoki są obliczane, nie edytowane

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Ręcznie prowadzone statusy i widoki się rozjeżdżały. `wg-spqr/docs/niejasnosci_tabela.md` pokazywał jako otwarty
bloker, który KB już częściowo rozwiązała. Karty zadań `spqr` wymagały kilkunastu poprawek „stale”. `spqr`
rozwiązał to generowanymi STATUS i TRACEABILITY z bramką `--check`.

## Decyzja
- Status etapu (`wgc/gate@0`) jest **wyliczany** z artefaktów, walidacji, otwartych spraw i hashy świeżości.
  Pole `complete: true` w YAML nie istnieje.
- Widoki dla ludzi (Markdown, tabele śledzenia, pokrycie) są generowane. `--check` kończy się błędem, gdy widok
  jest nieaktualny.
- Wyjątek: `docs/STATUS.md` **tego repo** (rozwój narzędzia) prowadzi sesja AI według playbooka. Jego spójność
  z ROADMAP i ADR pilnuje test `tests/test_continuity.py`.
