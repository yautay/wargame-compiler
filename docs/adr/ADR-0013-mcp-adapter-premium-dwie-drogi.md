# ADR-0013: MCP jako adapter; premium review przez API albo Claude Desktop

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Według promptu Claude Desktop jest interfejsem człowieka, klientem MCP i interfejsem premium review. GLU ma dać się
testować bez Claude Desktop. Koszt premium nie powinien przekroczyć ok. 2× bazowego workflow.

## Decyzja
- Rdzeń GLU nie zależy od MCP. CLI, MCP i późniejsze API to cienkie adaptery nad tymi samymi usługami.
- Premium review ma dwóch wykonawców o tym samym kontrakcie (`review_package` → odpowiedź zgodna z `answer_schema`):
  - `anthropic`: API, koszt w USD;
  - `desktop_pull`: kolejka; człowiek w Claude Desktop pobiera pakiet narzędziem MCP i odsyła odpowiedź w ramach
    subskrypcji.

  Odpowiedzi obu przechodzą tę samą walidację.
- Serwer MCP działa według zasady najmniejszych uprawnień (`docs/MCP.md`).

## Konsekwencje
Koszt premium liczymy w tokenach niezależnie od drogi, więc obie drogi da się porównać z baseline.
