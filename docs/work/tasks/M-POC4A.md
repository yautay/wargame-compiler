# M-POC4A: Wybór ograniczonego kontekstu

- **ID:** M-POC4A
- **Milestone:** M-POC4
- **Rola:** Codex; przegląd wspólny źródeł
- **Zależności:** M-POC3; czytelny wynik i raport. Powtórzenie tylko jako pass-02 w limitach.

## Cel i pytanie eksperymentalne

Dostarczyć źródło potrzebnych zależności bez rozszerzenia na całą instrukcję. Ile dodatkowych stron/reguł/tabel potrzeba, aby usunąć istotne blokady?

## Dokładne pliki do przeczytania

[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, [ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), [ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

- `P/source/source-v1.json`
- `P/reports/first-001/report.md`
- `P/reports/first-001/metrics.json`
- `P/evaluation/eval-v1/dependencies.json`
- `P/proposals/first-001/proposal.json`
- `C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf`

## Wejścia i wersja oceny

eval-v1 i lista luk; przy drugim przejściu dodatkowo P/reports/context-01/report.md i P/context/pass-01/manifest.json.

## Wymagane działania

1. Dla każdej krytycznej zależności znajdź źródło albo zapisz brak; określ przyczynę i wpływ na sytuacje.
2. Policz unikalny przyrost stron, reguł, tabel, głębokość i czas przed rozszerzeniem: maks. 8/20/4/2 kroki i 2 rundy.
3. Zapisz nowy pakiet kontekstu, dowody, prompt i manifest. Nie osiągalny cel pozostaje blocked_source.

## Artefakty wyjściowe i lokalizacje

- `P/context/pass-01/targets.json`
- `P/context/pass-01/manifest.json`
- `P/context/pass-01/prompt.txt i pliki dowodów`
- `P/context/pass-01/review.md`

## Kryteria zakończenia i kontrole

Każdy dodany plik ma hash, powód i zakres; brak przekroczeń limitu; nazwane tabele i nienumerowane cele mają ID. Nierozstrzygnięcia nie znikają.

Kontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).

## Zakres wyłączony

Cała instrukcja, automatyczne obejście limitów, nadpisanie wejść pierwszej próby.

## Przegląd człowieka

Przegląd źródeł krytycznych i niejednoznaczności. Zwiększenie limitu wymaga nowej decyzji przed próbą.

## Wznowienie

Czytaj targets.json i dotychczasowe liczniki. Dokończ bieżącą rundę przed rozpoczęciem drugiej.

## Przekazanie

M-POC4B otrzymuje zamrożony kontekst; bez źródła przekazuje jawną blokadę dalej.
