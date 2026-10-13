# M-POC5A.4d5 — uzgodnienie i przekazanie do sytuacji

Twoje „zatwierdzam i kontynuuj” zapisałem jako **owner-decision-14**:80 ograniczonych ocen wsparcia i2mieszane oceny .4d4, w tym ograniczone pominięcie SEM-022. Wszystkie **414 wcześniejszych ocen zakresów inwentarza** mają decyzje właściciela. Nie zmieniłem oryginalnych odpowiedzi ani wcześniejszych pakietów.

Wykonałem całe uzgodnienie .4d5. Sprawdziłem, czy207 pozycji ma rozłączny przydział i odpowiednią decyzję w obu wynikach; czy74 oczekiwania zachowują ten sam frozen reviewed_scope; czy277 par rubryki przypisano do właściwych przyjętych lub otwartych zakresów; oraz jak13 starszych kwestii ma się do późniejszych ograniczonych decyzji. Rozliczyłem też257 zakresów relacji,124 lokatory i granice pól218 oryginalnych rekordów reguł/węzłów. W przypadku ośmiu pending ponownie odczytałem właściwe źródła i oryginalne pola obu odpowiedzi, zachowując nierozstrzygnięte warianty.

## Co można przyjąć z tego uzgodnienia

**Rekomendacja:** przyjąć raport uzgodnienia jako spójną podstawę do osobnej oceny sytuacji M-POC5B, z zachowaniem starszych nierozstrzygnięć i braków źródeł. To decyzja o rozliczeniu dokładnych zakresów. Nie przyjmuje ponownie dawnych414 ocen, nie dodaje punktów reguł i nie poświadcza pełnej poprawności rekordów.

| Obszar | Co faktycznie ustalono | Co pozostaje |
|---|---|---|
| Inwentarz |207 pozycji,414 ocen obu odpowiedzi porównano i przyjęto w ograniczonych zakresach |Całe rekordy/pola, realne parametry i procedury poza tymi zakresami |
| Znaczenie lokalne |Po63 z66 dokładnych zakresów przyjęto |EXP-017,040,052 nadal otwarte |
| Wymagania źródła |Po3 z8 wymagań przyjęto |5 wymagań pending; nawet przyjęte wymaganie nie dostarcza brakującej mapy, setupu lub tabeli |
| Rubryki |264 z277 par ma wcześniejsze decyzje |13 par związanych z trzema lokalnymi pending; kategorii nie sumuje się jako dodatkowych reguł |
| Relacje |257 przypisanych wystąpień ma decyzje o komponentach |Pełne rekordy/graf, brakujące osobne pary i pełne precision/recall |
| Lokatory |124 przypisane zakresy oceniono i przyjęto ich ustalenia |Wady w oryginałach,2 przypadki precyzji i szersza treść/glify poza ocenionym zakresem |

## Dlaczego komplet inwentarza nie daje pełnej poprawności

**Minimum Hits — EXP-017/SEM-001.** Instrukcja wiąże Hits z wynikiem DR wyższym od TQ. Model zachowuje warunek, różnicę i minimum1, lecz pozostawia interpretację gałęzi DR≤TQ nieznaną i blokowaną. Dawne oczekiwanie przyjmuje w tej gałęzi zero Hits. Później zaakceptowano oznaczenie, literalny zakres i wadę lokatora; żadna z tych decyzji nie wybrała interpretacji tej gałęzi. Zachowuję dawną kwestię, bez twierdzenia, że model zawsze daje1Hit.

**Double Depth — EXP-040/SEM-002.** Instrukcja mówi o wspólnym Rout, osobnych heksach i końcowym „the unit”. Model zachowuje tę treść, ale nie rozstrzyga liczby eliminowanych jednostek. Dawne oczekiwanie ma interpretację eliminacji każdej jednostki osobno, przy możliwości legalnej ucieczki drugiej. Akceptacja literalnej klauzuli w .4d3 nie jest akceptacją tej pełnej interpretacji. Dostępność podparcia dla ekstraktora i rzeczywista geometria/kolejność pozostają osobnymi pytaniami.

**Triarii — EXP-052/SEM-011.** Model zachowuje obie bramki i wyjątek ataku bez ruchu. Nie zapisuje jednak jawnie ich połączenia w oczekiwanym zakresie. Późniejsze decyzje przyjęły klauzule osobno; nie dopisały ich koniunkcji do odpowiedzi. Zachowuję to pytanie, próg i wyjątek, bez nowego pozwolenia na ruch lub atak. Z tą kwestią wiąże się sześć z13 nadal otwartych par rubryki.

## Pięć wymagań kontekstu nadal pending

**EXP-010:** diagram słonia pokazuje przykład. Instrukcja wymaga kompasu mapy konkretnej bitwy. Model jawnie odróżnia przykład i blokuje rzeczywisty kierunek bez mapy. Nie zamieniam przykładu w uniwersalny kierunek ani braku mapy w blokadę sytuacji z już zadaną syntetyczną trasą.

**EXP-019:** lokalny cytat zachowuje możliwość szczególnych ograniczeń dowodzenia słoniami, lecz streszczenie mówi o dowolnym leaderze i flaga blokady jest false. Brakuje rozstrzygnięcia wystarczalności opisu przed użyciem konkretnego leadera. Nie wykazano przez to błędnie wybranego dowódcy w konkretnej sytuacji.

**EXP-050:** data i OC w doktrynie Triarii są zapisane jako warunki, nie rzeczywiste dane bitwy. Są luki AWL/RP/LOS/ZOC, ale nie osobne luki daty i OC. Pytanie o wystarczalność deklaracji braków pozostaje otwarte. Znany predykat nie dowodzi spełnienia go przez wybraną bitwę.

**EXP-066:** nakaz ignorowania odniesień do rydwanów na Combat Tables zachowano. Do wskazania konkretnych wyłączanych wpisów potrzeba jednak tabel. Późniejsza akceptacja literalnego nakazu nie zamyka oceny flagi false blocking dla pełnego lookupu. Nie odgaduję tabel ani nie twierdzę, że model już wykonał zły lookup.

**EXP-074:** czytelne glify i markery nie dają znaczenia ratingów lub tożsamości jednostki. Model sam wyklucza taką interpretację. Pozostaje pytanie o wystarczalność deklaracji źródła przed konkretnym użyciem TQ/MA. Zadane w sytuacji TQ6 nie staje się rzeczywistym ratingiem Leader Elephant.

## Starsze kwestie z późniejszymi ograniczonymi decyzjami

SEM-001–013 zachowano w pozostałych zakresach. Nie powtórzyłem jednak ich starych statusów tak, jakby późniejsze decyzje nie istniały: związek operatorów w SEM-004 jest częściowo przyjęty; wada E916 w SEM-005 potwierdzona; w SEM-007 wszystkie124 przypisane zakresy lokatorów już oceniono. Wynik lokatorów to122 mierzalne naruszenia obwiedni i2 przypadki nieocenialne z powodu precyzji;116 rastrów czytelnych,6 przyciętych lecz czytelnych i2 z brakującą linią.

W SEM-006 nadal brak trzech osobnych par wykonawczych i czterech wzmianek. Prozę ocenia się osobno; brak rekordu nie nadaje automatycznie semantycznego FN. D961stack ma już przyjęty rodzaj mention, więc tego komponentu nie otwieram ponownie. Ograniczone dyspozycje SEM-014–022 zachowano; pominięcia wyjaśnień pozostają w oryginałach. Brakujący cel trzeciego kroku nadal jest brakiem źródła; rozszerzanie zatrzymano na głębokości2.

## Ile zostało do końca M-POC5

**Po przyjęciu tego uzgodnienia pozostaje wykonawczo M-POC5B:20 zamrożonych sytuacji w obu odpowiedziach, czyli40 ocen.** Każda wymaga oceny wyniku albo źródłowo uzasadnionej blokady. Trzeba oszacować pełny zakres przed rozpoczęciem; jeśli przekracza90minut, podzielić go wcześniej. Nie wykonałem sytuacji w tej sesji i nie przedstawiam nieoszacowanego czasu jako pewnej daty zakończenia.

Do pełnego zamknięcia oceny pozostają także decyzje o pokazanym uzgodnieniu i starszych nierozstrzygnięciach. Braki mogą zostać uczciwie przekazane jako ograniczenia lub blokady — nie trzeba ich zgadywać. M-POC5A/.4/.4d nadal partial, pełne TP/FP/FN/precision/recall i jakość nieocenialne. Nie ma jeszcze podstaw do ogłoszenia końca całego etapu5.

[Każde uzgodnienie i stare pending](comparisons.md) · [Pełne źródła, decyzje, pola i bajty](comparisons.json).

Wcześniejszy inwentarz: porównano414 / udostępniono414 / przyjęto414 / pending0. Nowy pakiet uzgodnienia: porównano1 / udostępniono1 / nowych decyzji0 / pending1. Te liczniki nie cofają wcześniejszych akceptacji. Faktyczny odczyt plików przez właściciela unknown. Szacunek .4d5 65–85min zapisano przed pracą; aktywny czas, konfiguracja, tokeny, cena i łączny budżet unknown.
