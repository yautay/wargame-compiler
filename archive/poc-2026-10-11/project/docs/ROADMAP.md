# Roadmapa aktywnego POC

Statusy: `done`, `next`, `planned`. Dokładnie jeden milestone ma `next`.
[STATUS](STATUS.md) wskazuje bieżącą kartę, [HANDOFF](HANDOFF.md) ostatnią sesję.
Metoda i bramki: [POC-PLAN](POC-PLAN.md); szczegóły: [indeks kart](work/tasks/README.md).

| Milestone | Status | Wynik / bramka | Karty w kolejności |
|---|---|---|---|
| M-POC0 | done | Zweryfikowane archiwum, wnioski, plan, ADR i bootstrap | [M-POC0](work/tasks/M-POC0.md) |
| M-POC1 | done | M-POC1A/B/C zakończone w zatwierdzonych zakresach; decyzje 06/07 i zamrożony eval-v1; 66 grup/8 wymagań kontekstu, 20 sytuacji (17/3), 5 relacji jawnych/3 niejawne; progi i limity bez zmian | [M-POC1A](work/tasks/M-POC1A.md), [M-POC1B](work/tasks/M-POC1B.md), [M-POC1C](work/tasks/M-POC1C.md) |
| M-POC2 | done | M-POC2A/B done w zakresie przygotowania oraz odbioru już wykonanej first-001: 33 pliki pakietu zweryfikowane, oryginalne bajty i metadane zachowane; konfiguracja/czasy i niezależność próby niepotwierdzone, unknown; bez pomiaru jakości | [M-POC2A](work/tasks/M-POC2A.md), [M-POC2B](work/tasks/M-POC2B.md) |
| M-POC3 | done | Zamknięty baseline first-001 przed korektami: integralność zgodna, format czytelny; 207 rekordów rozliczonych, 1 błąd obszaru, 7 brakujących par, sześć klas oraz pending/not_assessable; bez semantycznej akceptacji, konfiguracja/czas/niezależność unknown | [M-POC3](work/tasks/M-POC3.md) |
| M-POC4 | done | M-POC4A/B done w zakresie wyboru źródła, raportu i przyjętego przez człowieka ograniczonego efektu: 0 pełnych domknięć/4 częściowe uzupełnienia/4 nowe luki; 1 strona/1 reguła/0 tabel, 1 runda/0 korekt; trzecia nierozstrzygnięta krawędź bez pozyskania źródła i naruszenie izolacji odnotowane; bez akceptacji znaczenia/budżetu | [M-POC4A](work/tasks/M-POC4A.md), [M-POC4B](work/tasks/M-POC4B.md) |
| M-POC5 | next | M-POC5A szerszy zakres partial, .4d5 dokładne uzgodnienie zatwierdzone;414 wcześniejszych decyzji inwentarza/257relacji/124lokatorów/264parrubryki zachowane, starsze8 oczekiwań/13 kwestii otwarte. M-POC5B całe20 sytuacji/40 ocen porównane, waiting_review:35 pozytywnych propozycji i5 osobnych (first15/3/1/1,context14/3/1/2), pełne3 wyniki zawieszone po porównaniu; mianownik20 na odpowiedź, bez nowych odpowiedzi modelu na sytuacje lub silnika; najpierw decyzje i rozliczenie ograniczeń, pełne metryki nieocenialne | [M-POC5A](work/tasks/M-POC5A.md), [M-POC5A.1](work/tasks/semantic/M-POC5A.1.md), [M-POC5A.2](work/tasks/semantic/M-POC5A.2.md), [M-POC5A.3](work/tasks/semantic/M-POC5A.3.md), [M-POC5A.4](work/tasks/semantic/M-POC5A.4.md), [M-POC5A.4a](work/tasks/semantic/M-POC5A.4a.md), [M-POC5A.4b](work/tasks/semantic/M-POC5A.4b.md), [M-POC5A.4b1](work/tasks/semantic/M-POC5A.4b1.md), [M-POC5A.4b2](work/tasks/semantic/M-POC5A.4b2.md), [M-POC5A.4b3](work/tasks/semantic/M-POC5A.4b3.md), [M-POC5A.4c](work/tasks/semantic/M-POC5A.4c.md), [M-POC5A.4d](work/tasks/semantic/M-POC5A.4d.md), [M-POC5B](work/tasks/M-POC5B.md) |
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

## Plan .4d przed przeglądem — 2026-10-11

Pięć osobnych części: [M-POC5A.4d1](work/tasks/semantic/M-POC5A.4d1.md) 39pozycji, [M-POC5A.4d2](work/tasks/semantic/M-POC5A.4d2.md) 68pozycji, [M-POC5A.4d3](work/tasks/semantic/M-POC5A.4d3.md) 59pozycji, [M-POC5A.4d4](work/tasks/semantic/M-POC5A.4d4.md) 41pozycji, [M-POC5A.4d5](work/tasks/semantic/M-POC5A.4d5.md) 0pozycji. Całość300–420minut; pierwsza39pozycji/78wystąpień70–85minut. ExactIDs prywatnie, dalszy podział przed wykonaniem jeśli potrzebny; nadrzędne karty partial, M-POC5 jedyny next.


## Wykonanie .4d4 — 2026-10-11

Wykonano cały rzeczywisty przegląd 41 przypisanych pozycji inwentarza, osobno w obu oryginalnych odpowiedziach: 82 porównania. Prywatny part-04d4 zawiera dokładne źródła, oryginalne pola i ślady do bajtów, oceny, wyłączenia oraz opis proponowanych decyzji po ludzku. Szacunek 75–90 minut zapisano przed oceną.

Proponowane 80 ograniczonych ocen wsparcia i 2 mieszane oceny jednej klauzuli, po jednej na odpowiedź. Operatywna treść zachowana; ograniczone pominięcie wyjaśnienia tekstowego przy zachowanym obrazie źródła zapisano osobno, bez automatycznego FN lub wykazanego błędnego wyniku gry. Role nagłówków nie certyfikują ich pełnej transkrypcji lub dawnych wad lokatorów.

Porównano 82 / udostępniono 82 / nowych decyzji właściciela 0 / pending 82; faktyczny odczyt plików unknown. Owner-decision-13 zachowuje zatwierdzenie .4d3 bez duplikatu. Łącznie 207/207 pozycji i 414/414 wystąpień porównano; 332 wcześniejsze zakresy przyjęte, 82 nowe oczekują decyzji. To nie 414 całych poprawnych rekordów.

Starsze 8 oczekiwań i 13 kwestii pozostają otwarte; ograniczone wcześniejsze dyspozycje zachowano. 257 zakresów relacji, 124 lokatorów, 264 pary rubryki i po 63 lokalne zakresy/3 wymagania źródła zachowano bez ponownego punktowania. Gold i limity bez zmiany; pełne metryki not_assessable.

current-state-28 prowadzi wynik. Najbliższa czynność: decyzje według prywatnego owner-focus .4d4; potem osobna .4d5 końcowe uzgodnienie i M-POC5B 20 sytuacji w obu wynikach (40 ocen). Tych kart tu nie wykonano. M-POC5A/.4/.4d pozostają partial; M-POC5 jedyny next. Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów, commit/push lub architektury. Konfiguracja, aktywne czasy, tokeny, cena i budżet unknown. Kontrole, logi i audyt niezmienności: measurement/M-POC5A-semantic-04d4/.


## Zatwierdzenie .4d4 i uzgodnienie .4d5 — 2026-10-11

Właściciel „zatwierdzam i kontynuuj” przyjął82 oceny .4d4:80 ograniczonych ocen wsparcia i2mieszane oceny klauzuli z ograniczonym pominięciem wyjaśnienia. Owner-decision14/overlay14 i current-state29 zapisują zgodę;414 wcześniejszych zakresów inwentarza ma decyzje,207 na odpowiedź. To nie414 całych poprawnych rekordów. Starsze8 oczekiwań/13 kwestii pozostają otwarte.

Wykonano całe .4d5: uzgodniono207 pozycji/414 wcześniejszych ocen,74 oczekiwania w obu oryginalnych hashach,277 par rubryki i13 starszych kwestii; rozliczono257 zakresów relacji,124 lokatory i granice218 oryginalnych rekordów reguł/węzłów. Odczytano właściwe źródła/pola ośmiu pending; nowsze ograniczone decyzje odróżniono od otwartych reszt. Prywatny part-04d5 zawiera konkretny wynik każdego uzgodnienia, podstawy, wyłączenia i opis po ludzku. Szacunek65–85min zapisano przed pracą.

Po63/66 lokalne zakresy i3/8 wymagania źródła na wynik przyjęte;3 lokalne i5 kontekstowych oczekiwań nadal pending.264/277 par rubryki przyjęte,13 pozostaje przy3lokalnych nierozstrzygnięciach. Nie dopisano wariantów, reguł lub gold i nie nadano nowych punktów. Pełne wyniki i metryki nadal not_assessable; wymaganie źródła nie dostarcza realnej mapy, setupu lub tabeli.

Wcześniejszy inwentarz: porównano414 / udostępniono414 / przyjęto414 / pending0. Nowy pakiet uzgodnienia: porównano1 / udostępniono1 / nowych decyzji0 / pending1. Wcześniejszych decyzji nie cofnięto; faktyczny odczyt plików przez właściciela unknown. current-state30 prowadzi wynik, M-POC5A/.4/.4d partial, M-POC5 jedyny next.

Najbliższa czynność: decyzja według owner-focus .4d5 o dokładnym uzgodnieniu i przekazaniu z ograniczeniami. Potem pozostaje wykonawczo osobne M-POC5B:20 zamrożonych sytuacji w obu odpowiedziach,40 ocen. Przed rozpoczęciem oszacować cały zakres i podzielić wcześniej, jeśli przekracza90min. Sytuacji nie wykonano tutaj. Do pełnego zamknięcia pozostaje także przegląd właściciela i rozliczenie otwartych kwestii, bez zgadywania braków.

Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów, commit/push lub architektury. Konfiguracja, aktywne czasy, tokeny, cena i łączny budżet unknown. Oryginały i wcześniejsze pakiety zachowane; logi, kontrole i audyt prowadzi measurement/M-POC5A-semantic-04d5/.


## M-POC5B — wszystkie sytuacje porównane, 2026-10-11

Po zatwierdzeniu dokładnego uzgodnienia .4d5 wykonano całe M-POC5B:20 zamrożonych sytuacji w obu oryginalnych odpowiedziach,40 ocen. Każdy wariant i wymagany wniosek porównano ze źródłem, oryginalnymi polami i frozenexpected; prywatny situations-01 zawiera ślady do bajtów, użyte zależności, ręczne wyprowadzenia i opis decyzji po ludzku. To ocena wyprowadzalności z zapisu reguł przy zadanych faktach, bez nowych odpowiedzi modelu na sytuacje, nowej ekstrakcji, korekty lub silnika. Szacunek75–90min zapisano przed oceną; cały zakres mieści się w jednej zaplanowanej części.

Propozycjefirst:15 zgodnych lokalnych wyników,3 właściwe oczekiwane blokady,1kandydat nieuzasadnionej lokalnej blokady i1pełny wynik zawieszony po porównaniu. Context:14/3/1/2. Razem35 pozytywnych ocen oraz5 do osobnego rozstrzygnięcia. Pełny mianownik20 w każdej odpowiedzi zachowany; warianty nie dają dodatkowych punktów. Oczekiwane blokady nie są meaningful localresults dla progu80%.

Porównano40 / udostępniono40 / nowych decyzji właściciela0 / pending40. Wszystkie40 ocen wykonane przez oceniającego;3 pełne wnioski zawieszone mimo porównanych komponentów. Wydzielono konsekwencje dwóch starych nierozstrzygnięć i jedno pytanie o zakres zamrożonych faktów wobec dostarczonego warunku po kontekście. Nie rozstrzygnięto starych wariantów ani nie zmieniono eval-v1; nie wykazano przez samo to regresji modelu lub konkretnej złej liczby.

current-state32 prowadzi nowy wynik. Starsze8 oczekiwań/13 kwestii oraz wcześniejsze ograniczone decyzje zachowane.414 zakresów inwentarza,257 relacji,124 lokatory i264 pary rubryki bez ponownego punktowania. M-POC5B i milestone5 partial/waiting_review, M-POC5 jedyny next. M-POC5A w szerszym zakresie nadal partial; pełne jakość/TP/FP/FN/precision/recall not_assessable.

Najbliższa czynność: decyzje według prywatnego situations-01/owner-focus —35 pozytywnych ocen oraz2+2+1 osobne. Następnie świadomie rozliczyć starsze nierozstrzygnięcia i warunki formalnego zamknięcia etapu5. Nie rozpoczęto M-POC6/7 ani naprawy odpowiedzi. Faktyczny odczyt plików przez właściciela unknown; konfiguracja, aktywne czasy, tokeny, cena i łączny budżet unknown. Bez nowych źródeł/pass-02, ekstrakcji, korekt, czatów, commit/push lub architektury. Kontrole i audyt: measurement/M-POC5B-situations-01/.
