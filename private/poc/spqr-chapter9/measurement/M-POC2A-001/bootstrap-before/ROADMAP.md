# Roadmapa aktywnego POC

Statusy: `done`, `next`, `planned`. Dokładnie jeden milestone ma `next`.
[STATUS](STATUS.md) wskazuje bieżącą kartę, [HANDOFF](HANDOFF.md) ostatnią sesję.
Metoda i bramki: [POC-PLAN](POC-PLAN.md); szczegóły: [indeks kart](work/tasks/README.md).

| Milestone | Status | Wynik / bramka | Karty w kolejności |
|---|---|---|---|
| M-POC0 | done | Zweryfikowane archiwum, wnioski, plan, ADR i bootstrap | [M-POC0](work/tasks/M-POC0.md) |
| M-POC1 | done | M-POC1A/B/C zakończone w zatwierdzonych zakresach; decyzje 06/07 i zamrożony eval-v1; 66 grup/8 wymagań kontekstu, 20 sytuacji (17/3), 5 relacji jawnych/3 niejawne; progi i limity bez zmian | [M-POC1A](work/tasks/M-POC1A.md), [M-POC1B](work/tasks/M-POC1B.md), [M-POC1C](work/tasks/M-POC1C.md) |
| M-POC2 | next | Niezmienne wejścia, format i pierwsza ręczna ekstrakcja | [M-POC2A](work/tasks/M-POC2A.md), [M-POC2B](work/tasks/M-POC2B.md) |
| M-POC3 | planned | Raport pierwszego wyniku przed korektą | [M-POC3](work/tasks/M-POC3.md) |
| M-POC4 | planned | Ograniczone domknięcie zależności i wynik po kontekście | [M-POC4A](work/tasks/M-POC4A.md), [M-POC4B](work/tasks/M-POC4B.md) |
| M-POC5 | planned | Ocena znaczenia i wszystkich sytuacji przez człowieka | [M-POC5A](work/tasks/M-POC5A.md), [M-POC5B](work/tasks/M-POC5B.md) |
| M-POC6 | planned | Ograniczone korekty, regresje i koszt | [M-POC6A](work/tasks/M-POC6A.md), [M-POC6B](work/tasks/M-POC6B.md) |
| M-POC7 | planned | Porównanie i decyzja właściciela; dopiero potem architektura | [M-POC7A](work/tasks/M-POC7A.md), [M-POC7B](work/tasks/M-POC7B.md) |

M-POC6A/B można wykonać wcześniej dla błędu z M-POC3–M-POC5, zachowując bieżący
milestone i wracając do niego po korekcie. Wczesna korekta formatu liczy się do
limitu trzech; domknięcie kontekstu ma osobny limit dwóch rund.

Większą kartę dzielimy przed wykonaniem, nie rozszerzamy niejawnie sesji.
M-POC0 kończy się tylko po wszystkich kontrolach; M-POC1–M-POC7 nie są wykonywane
w sesji reorganizacji. Wynik POC i przyszła architektura pozostają nieznane.

## Historia poza aktywną kolejką

M-DESK2 pozostaje **partial**. M-DESK3 oraz dawny backlog nie są zależnością POC.
[Archiwum](../archive/legacy-2026-10-07/README.md) zawiera starą roadmapę i wszystkie
ADR pod niezmienionymi numerami. Ich historyczne statusy nie są drugim aktywnym `next`.
Zakres zmiany określa [ADR-0039](adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
