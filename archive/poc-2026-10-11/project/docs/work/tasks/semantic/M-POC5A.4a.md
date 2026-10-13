# M-POC5A.4a: EXP-051–074

- **ID:** M-POC5A.4a
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** M-POC4 ograniczone done; wcześniejsze pakiety M-POC5A i jawne pending zachowane.

## Cel i pytanie eksperymentalne

Porównać wszystkie 24 oczekiwania z obu odpowiedzi ze źródłem, wraz z przypisanymi zakresami inwentarza i rubryk. Nie rozstrzygać całego grafu, lokatorów lub reszty inwentarza w tej części.

## Dokładne pliki do przeczytania

[Karta nadrzędna .4](M-POC5A.4.md), [M-POC5A](../M-POC5A.md), bootstrap, STATUS, HANDOFF z aktualnym przekazaniem, ROADMAP, POC-PLAN i ADR-0039. Prywatne: najnowszy current-state i owner-decision/overlay, oryginalny checklist, oba run/proposal/provenance/report i niezmienione eval-v1.

## Wejścia i wersja oceny

Te same oryginalne first-001/context-01 i eval-v1, z pełnymi hashami oraz dokładnymi źródłowymi zakresami; właściciel przyjął 43 lokalne zakresy i 2 wymagania źródła w obu wynikach, z wyłączeniami.

## Wymagane działania

Porównać wszystkie 24 oczekiwania z obu odpowiedzi ze źródłem, wraz z przypisanymi zakresami inwentarza i rubryk. Nie rozstrzygać całego grafu, lokatorów lub reszty inwentarza w tej części. Zachować transkrypcję i interpretację osobno, krytyczny brak źródła jako blokadę zależnego pełnego wyniku, a lokalne zadane fakty oceniać we właściwym zakresie. Oceny modelu są propozycjami, nie akceptacją. Jedna część do 90 minut.

## Artefakty wyjściowe i lokalizacje

Osobne dodatki w reviews/semantic-01/ pod private/poc/spqr-chapter9/, z dokładnymi hashami i śladami do surowych bajtów; nowe decyzje człowieka, nowy katalog pomiaru oraz append-only sessions.jsonl. Nie przepisywać zamkniętych artefaktów.

## Kryteria zakończenia i kontrole

Jawne ID ocenionych i pending, recenzent, źródło, zakres i niepewności. scripts/check.ps1 i git diff --check z logami, nowym basetemp oraz końcową kontrolą niezmienności.

## Zakres wyłączony

Nowe źródła/pass-02, ekstrakcja i korekty, API inferencji, M-POC5B i 20 sytuacji, M-POC6/7 oraz architektura. Nie rozszerzać eval-v1 lub gold.

## Przegląd człowieka

Właściciel rzeczywiście ocenia pokazane zakresy; missing review pozostaje waiting_review. Akceptacja nie obejmuje innych pól, aliasów lub pełnych wyników zależnych od brakujących źródeł.

## Wznowienie

Od pierwszego pending przypisanego tej części. Zmiana hasha odpowiedzi unieważnia dotknięte oceny; bez modelowego wyboru wariantów nierozstrzygniętych przez właściciela.

## Przekazanie

Następna osobna część otrzymuje wszystkie pozostałe pending. M-POC5A pozostaje partial do rozliczenia całości; M-POC5B jest odrębną kartą.

## Wykonanie porównań, 2026-10-10

Przygotowano wszystkie 24 porównania, 31 powiązanych pozycji źródła i 95
diagnostycznych par rubryka/oczekiwanie w prywatnym part-04a/. Propozycje:
20 lokalnych zgodności, 1 właściwa potrzeba/blokada źródła i 3 kwestie
do osobnej decyzji. Nowe znaczenie waiting_review; wcześniejsze 43/2
przyjęte zakresy na wynik zachowane. Stan: current-state-06.json,
pomiar: measurement/M-POC5A-semantic-04a/. .4a partial, nadrzędne .4
i M-POC5A partial; .4b/.4c/.4d niewykonane. Decyzja właściciela jest
osobnym nowym artefaktem, nigdy zmianą zamkniętych porównań/odpowiedzi.

2026-10-11 właściciel zatwierdził pozytywny zakres po objaśnieniu po ludzku:
20 lokalnych zakresów oraz 1 wymaganie źródła w obu hashach. Trzy kwestie
tej części pozostają pending. Nowa owner-decision-03.json i current-state-07.json
prowadzą stan: łącznie 63 lokalne/3 wymagania źródła na wynik, 8 oczekiwań
pending. Pomiar M-POC5A-owner-review-003/. Nie zamknięto nadrzędnej .4
lub M-POC5A; następna osobna .4b, potem .4c/.4d.
