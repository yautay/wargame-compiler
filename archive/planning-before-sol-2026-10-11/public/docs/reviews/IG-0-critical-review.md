# IG-0: krytyczna recenzja Instruction Graph

Data: 2026-10-11, Europe/Warsaw. Przedmiot: zastany ig-draft-0.2.
Wynik pracy recenzenta: wykonana recenzja projektu i korekta aktywnych
draftów. Status na moment recenzji: **partial, oczekuje decyzji właściciela o zakresie**.
To nie akceptacja semantyki reguł ani zaliczenie eksperymentu ekstrakcji.

**Późniejsze doprecyzowanie 2026-10-11:** właściciel wskazał pełną instrukcję
oraz wykorzystanie istniejącej KB WGU. [Nowy plan](../IG-PLAN.md) i
[architektura](../IG-WGU-ARCHITECTURE.md) zastępują rekomendację małego pilota
z D3. Poniższe ustalenia pozostają zapisem recenzji; D1–D5 nie są już
oddzielną, aktualną listą decyzji. Właściciel wskazał również szybkie,
deterministyczne [legalne akcje dla AI](../IG-LEGAL-ACTIONS.md) jako cel IG.
Digitalizacja i wyszukiwanie są etapem pośrednim. Ukończenie późniejszego
planu zamyka IG-0 jako pracę projektową, bez nadawania akceptacji semantyce.
Obecne ustalenia wejściowe opisuje architektura.

## Rozstrzygnięcie

IG jest uzasadniony jako model dokumentów, dowodów, interpretacji i review.
Nie ma podstaw do przyjęcia obecnego rozszerzenia mechanik jako wspólnego
języka wykonawczego tych gier. Rekomenduję **klauzule z adresowalnymi
aspektami i jawnymi zależnościami**, z opcjonalną formalizacją, jako minimum
IG-1. Wyszukanie reguły i pokazanie braków powinno działać również wtedy,
gdy model nie potrafi obliczyć wyniku sytuacji.

Najważniejszy problem nie polega na braku kolejnych nazw pól. Draft dobrze
nazywa większość trudnych mechanik, lecz nie określa dostatecznie więzi
między częściami znaczenia, podstawy przenoszenia review i granicy między
zapisem opisowym a wykonywalnym. Swobodny `payload` pomieści dowolny tekst;
nie stanowi to dowodu jednoznacznej reprezentacji ani jej walidowalności.

## Pochodzenie i granice odczytu

Wykonawca: lokalna sesja Codex w `C:\repo\wargame-compiler`.
Dostępny opis systemowy: Codex oparty na GPT-6. **Dokładny identyfikator
modelu: unknown; faktycznie wybrany poziom reasoning: unknown** — nie
udostępniono wiarygodnej telemetrii selektora tej sesji. Zalecenie
GPT-6 Astra/high z promptu nie jest potwierdzeniem użycia tej konfiguracji.
Nie zmieniano modelu, nie uruchamiano nowych sesji, agentów ani inferencji API.
Czas aktywny człowieka, tokeny i cena: unknown.

W całości przeczytano README, CLAUDE, STATUS, HANDOFF, IG-PLAN, ROADMAP,
kartę IG-0, IG-DATA-MODEL, IG-MECHANICS-PROFILES, ADR-0040 oraz oba wskazane
prywatne dokumenty badawcze. Manifest archiwum odczytano programowo;
historyczne PDF, metadane źródła, propozycję formatu i STATUS odnaleziono
przez jego `entries`. Historyczny STATUS czytano fragmentami, format
propozycji i metadane źródła w całości. Nie uznano dawnych poleceń wznowienia
za aktywne instrukcje.

**Żadnej instrukcji gry nie przeczytano w całości.** Odczytano wybrane
strony i paragrafy oraz obejrzano siedem stron dowodowych. Pełne pobranie
PDF i automatyczne wydobycie tekstu nie oznaczają pełnego odczytu.

| Rodzina | Źródła sprawdzone w tej sesji | Granica wniosku |
|---|---|---|
| SPQR | Lokalny oryginał 5E, hash z manifestu; oficjalna lista GMT | Wybrane mechaniki, bez kompletnego scenariusza i pomocy 5E |
| OSG TLNB | Series Rules 7.38, wybrane strony tabel | Brak audytu zgodności całego kompletu pomocy z 7.38 |
| OSG CNS/NAB | Opis CNS i Exclusive Rules 2020-b, pierwsze trzy strony | Brak odczytu Standard Rules CNS; nie można certyfikować pełnej kompozycji |
| OSG Days | Last Days, wybrane strony; Seven Days, fragment słownika | Dwa osobne tytuły; nie dowód pokrycia całej rodziny |
| GCACW | Basic 1.6, tabele 1.6, fragment RTG II | Wybrane procedury i zakresy modułowe; Advanced nieprzeczytane w całości |

Oficjalne katalogi potwierdzają rozdział materiałów, a nie ich automatyczną
wymienność: [GMT SPQR](https://www.gmtgames.com/p-1118-spqr-deluxe-5th-edition.aspx),
[OSG support](https://napoleongames.com/pages/game-support-files),
[OSG CNS](https://napoleongames.com/pages/campaigns-of-napoleon-series-1x),
[MMP downloads](https://mmpgamers.com/gcacw-downloads-ezp-8).

Dokładne lokalizacje, hashe, obrazy, korekty wcześniejszych odwołań i siedem
próbek reprezentacji są wyłącznie w
`private/ig/reviews/IG-0/evidence-and-examples.md` oraz `sources-manifest.json`.
Kopie wejściowych draftów zachowano tam w `draft-before/`. Rejestr rozdziela
odczyt bieżący, wcześniejsze notatki i hipotezy. Internetowy czytnik nie
otworzył części PDF; osiem plików pobrano bezpośrednio z oficjalnych URL,
zachowano i zahashowano. Oryginał SPQR pozostał w archiwum, tylko do odczytu.

## Ustalenia wymagające poprawy

P1 oznacza blokadę przyjęcia kontraktu w danym zakresie; P2 — istotny koszt
lub ograniczenie wymagające rozliczenia przed skalowaniem. Nie są to błędy
działającego programu, którego jeszcze nie ma.

| ID | Priorytet, dowód w draftach/prywatnym aneksie | Wpływ i proponowana zmiana |
|---|---|---|
| R1 | P1. DATA: „Twierdzenia i znaczenie reguł”; rozdzielenie condition/effect/timing bez obowiązkowego powiązania; przykłady S, G | Dwa warunki i dwa skutki pod tym samym subject nie wyznaczają par. Dzielić klauzulę albo dodać adresowalną grupę wiążącą konkretne aspekty. Recenzować również te więzi. |
| R2 | P1. DATA: „Przegląd człowieka”; dopuszcza ponowne użycie akceptacji, lecz nie podaje porównywalnego zestawu jej podstaw; przypadek X2 | Hash lokalnego tekstu nie wykryje zmiany definicji, profilu, legendy lub wiązania. Zapisać przypięte basis_refs, rodzaj oceny i kompletność podstawy. Niepełna podstawa daje unknown, nie aktualną akceptację semantyczną. |
| R3 | P1. DATA: snapshot wybiera jedną rewizję ID, review może wskazywać historyczną; X3 | Odróżnić archiwalne odwołania dowodowe od aktywnych zależności. Stare review pozostaje czytelne bez włączenia starej reguły do aktywnego zestawu. |
| R4 | P1. MECHANICS: cancel/replace i uporządkowane writes; przykład S2 | Brak semantyki unieważnienia części już wykonanej procedury. cancel nie mówi, co zrobić z kosztami, licznikami i zdarzeniami. Zapisać ograniczenie formalizacji; przyszły wykonawca wymaga granicy zatwierdzenia i polityki unieważnienia. Nie wdrażać globalnego rollbacku na podstawie jednej reguły. |
| R5 | P1. Profile i composition_decisions; N, T, G oraz korekty źródeł | Jedno źródło może łączyć reguły wspólne, modułowe i opcjonalne. Sam game_id źródła nie wystarczy. Kompozycja musi celować w region/klauzulę/aspekt, zachować niepewność i wykrywać nakładanie poprawek. |
| R6 | P1 dla wykonawcy, P2 dla digitalizacji. MECHANICS: randomizer/state; D | Pula, ręka i element zagrany potrzebują wielokrotności oraz tożsamości losowania. Typ set gubi identyczne elementy. Opisowe minimum wystarcza; rozszerzenie wymaga multizbioru lub instancji żetonów, jawnych transferów i momentów zwrotu. |
| R7 | P1. DATA: conflicting_claims i konflikty różnych ID; D2 | Sprzeczność może leżeć wewnątrz tej samej instrukcji, a nawet w aspektach jednego obiektu. Zakaz wybierania „bardziej szczegółowego” bez podstawy jest trafny; potrzebny jawny zakres konfliktu i blokada dotkniętego wniosku. |
| R8 | P2. DATA: osobne obiekty każdej komórki, twierdzenia i pliki | Koszt jest narzucony przed pomiarem. Dopuścić blok tabeli z trwałymi adresami komórek/aspektów, niezależnie od fizycznego podziału plików. Semantycznej dekoracji nie wolno usuwać. |
| R9 | P1 dla przyszłych odpowiedzi w perspektywie gracza. MECHANICS: viewer_role; D3, N | Sam filtr końcowego tekstu nie chroni ukrytych faktów ujawnionych przez dowód, lukę, liczbę kandydatów lub ślad. IG-1 zachowuje opis widoczności; wykonawca i UI wymagają odrębnej polityki dostępu do całego wyniku. |
| R10 | P2. DATA: represented/partial bez zadeklarowanego poziomu; wszystkie próbki | Pokrycie transkrypcji może wyglądać jak pokrycie procedury. Każde rozliczenie wskazuje poziom i zamknięty inwentarz mianownika. Opaque może być zachowane w pełni jako tekst i jednocześnie nie mieć formalnej interpretacji. |

R1–R3 są kontrprzykładami konstrukcyjnymi kontraktu. R4–R9 wynikają
z odczytanych wymagań lub ujawniają brak definicji operacyjnej. Nie twierdzę,
że wszystkie są niemożliwe do zapisania w draftowym JSON: część da się
opisać prozą. To właśnie różnica między przechowaniem informacji a wspólnym,
sprawdzalnym znaczeniem struktury.

## Przegląd wszystkich wymaganych obszarów

| Obszar | Ocena |
|---|---|
| Jednostka reguły i review | Klauzula jest dobrą jednostką czytania. Aspekt jest jednostką korekty; pełna implikacja i jej zakres są jednostką oceny znaczenia. Akceptacja pojedynczego parametru nie zatwierdza działania. R1–R3. |
| Wersje i zakresy źródeł | Kwalifikowane numery i zachowanie bajtów są trafne. Potrzebna osobna kompatybilność na poziomie fragmentu, bez domyślnego latest-wins. R5. |
| Procedury, reakcje, powroty | Kolejność źródłowa, pętle i rodzaje kontynuacji są przydatne. Brakuje instancji wywołania, lokalnych wiązań, granicy zatwierdzenia i zasad zagnieżdżania dla wykonawcy. R4. |
| Stany i przyczyny zdarzeń | Rozdzielenie definicji od sytuacji oraz cause_filter jest właściwe. Trzeba rozróżniać zdarzenie, próbę, skutek i odwołanie skutku; równość końcowego stanu nie oznacza równoważności. |
| Historia | history_requirement i checkpoint są potrzebne. Minimum określa, jakich faktów brakuje; nie wymaga pełnego dziennika partii. Wykonawca musi odróżniać unknown od false i zero oraz fakty od stanu pochodnego. |
| Wybory między krokami | binding_id/lifetime/rechoose oraz selected/participating to mocna część draftu. Wykonawca potrzebuje wiązania do konkretnego wywołania, by dwie równoległe procedury nie współdzieliły wyboru. |
| Geometria wieloheksowa | Jeden obiekt z wieloma zajętymi polami jest trafny. Orientacja i historia poniesionych kosztów muszą należeć do jednostki/procedury, nie do niezależnych kopii żetonu. Brak mapy blokuje wynik, nie digitalizację tekstu. |
| ZOC, LOS, ścieżki | Osobne, kierunkowe polityki to właściwy kierunek. Potrzebna semantyka kwantyfikatorów: istnieje ścieżka, każda ścieżka, najkrótsza ścieżka, wybór spośród równorzędnych. Sam zestaw dozwolonych krawędzi nie rozstrzyga priorytetów. |
| Losowanie z puli | Opis odróżnia losowanie od decyzji, lecz nie definiuje stanu i wielokrotności puli. R6. |
| Wynik naturalny/zmodyfikowany | Oba wyniki oraz ID rzutu są potrzebne i wystarczające opisowo w przeczytanych przypadkach. Brak kontrprzykładu tej konkretnej zasadzie; nie jest to ocena wszystkich testów losowych. |
| Zaokrąglenia i modyfikatory | Kolejność, jednostki i stacking_policy są trafne. Późniejszy język musi określić dziedzinę liczb, etap odcięcia/limitu i zależność od historii; nie wystarczy jedna lista bonusów. |
| Tabele i legendy | Osie i nota to część znaczenia. Wersja tabeli, grupa kolumn, rola wyniku i dekoracja muszą być adresowalne; zdjęcie nie dowodzi poprawności transkrypcji. R5, R8. |
| Informacja ukryta | Zapis reguły widoczności należy do IG; bezpieczne zapytanie o stan partii wykracza poza IG-1. R9. |
| Scenariusze | Są źródłami parametrów, procedur i zmian, nie tylko pozycji startowych. Źródło wymagane, lecz nieodczytane, pozostaje luką; brak kompletnego scenariusza w próbie ogranicza wnioski. |
| Dowodzenie | Rozdzielenie gracza, strony, formacji i podporządkowania jest właściwe. Zasięg, uprawnienie i utrwalony status to różne rzeczy. Wspólny termin nie uzasadnia wspólnej reguły między profilami. |
| Zwycięstwo | metric/checkpoint/koniec/remis są dobrym katalogiem wymagań. Brak całego toru, scenariusza i reguł zmian wyniku blokuje pełne obliczenie. Nie wykazano kompletności modelu zwycięstwa. |
| Regresje | Porównywać również podstawy, profile, konflikty i wiązania przy niezmienionym tekście. Niekompletny graf wpływu nie uzasadnia braku regresji. Oczekiwana blokada jest osobnym wynikiem testu. |

## Alternatywy

| Model | Korzyść | Koszt/ograniczenie | Decyzja rekomendowana |
|---|---|---|---|
| A. PDF + indeks fragmentów + adnotacje | Najmniej rekordów, szybkie wyszukiwanie i źródło | Trudno kontrolować zasięg zmian i wspólne zależności; ręczne rozstrzygnięcia | Zachować jako punkt odniesienia kosztu i użyteczności |
| B. Klauzule z adresowalnymi aspektami, dowodami i linkami | Czytelna całość, dokładne review, stopniowa formalizacja | Wymaga trwałych kluczy aspektów i jawnych grup warunek–skutek | Minimum IG-1 |
| C. Obecny graf atomowych twierdzeń | Precyzyjne zależności i niezależne rewizje | Więcej rekordów, referencji i składania znaczenia; łatwo stworzyć fałszywą kompletność | Opcjonalna projekcja B, porównać na identycznym pakiecie |
| D. Język procedur + stan + wykonawca | Automatyczne sytuacje i ślady obliczeń | Duży kontrakt operacyjny, konflikty źródłowe, mapy i historyczne wejścia | Osobny późniejszy zakres |

Nie ma potrzeby wybierania bazy grafowej. Dokumenty JSON z indeksami mogą
realizować logiczny graf; typ magazynu nie naprawi niejasności znaczenia.
Nie rekomenduję odrzucenia relacji. Rekomenduję przestać utożsamiać osobne
ID i pola review z obowiązkiem osobnego pliku i kliknięcia dla każdej wartości.

## Liczba rekordów i koszt review

Koszt obejmuje liczbę **celów decyzji, przełączeń kontekstu i ponownych
ocen**, nie tylko bajty. Dla C klauzul, F aspektów/klauzulę i D relacji/klauzulę,
przy jednym regionie, dowodzie, wpisie coverage i pakiecie review na klauzulę:

- model atomowy: `R = C × (5 + F + D) + K`;
- klauzula z osadzonymi aspektami: `R = C × (5 + D) + K`;
- K to wspólne źródła, profile, runs i manifesty, osobno luki i dodatkowe rewizje.

To jawny model rachunkowy, **nie pomiar pełnej instrukcji**. Przy C=1000,
F=5, D=2 otrzymujemy 12000+K wobec 7000+K rekordów, lecz nadal co najmniej
5000 aspektów i 2000 relacji do kontroli w obu wariantach. Zbiorcze review
zmniejsza liczbę czynności administracyjnych, nie ilość znaczenia do oceny.
Dla tabeli 20×10 model komórkowy potrzebuje 200 obiektów i 200 twierdzeń
wartości jeszcze przed osiami, notami, dowodami i decyzjami. Blok tabeli
redukuje liczbę rekordów, lecz zachowuje 200 adresowalnych wartości.

Ilustracyjna wrażliwość: 1000 klauzul × 2–5 minut podstawowego przeglądu
to 33–83 godziny; 20% korekt po 2–4 minuty dodaje 7–13 godzin. Pozyskanie
źródeł, powiązania między rozdziałami i rozstrzyganie sporów są dodatkowe.
Założenia nie są estymacją opartą na zmierzonym czasie operatora.
Prywatny skrypt `cost-model.py` odtwarza ten rachunek i zapisuje wynik.

Historia POC pokazuje rozdzielność liczby rekordów, zakresów oceny i pełnych
wyników, ale nie daje wiarygodnej stawki minut na rekord. Nie przenoszę
czasów planowanych ani ograniczonych zgód na koszty IG.

Przed skalowaniem proponuję porównać A/B/C na tym samym pakiecie 20 klauzul
(po 4 dla pięciu rodzin profili), w tym klauzuli wielostronicowej i tabeli
z notą. Osobno mierzyć przygotowanie, sprawdzenie źródła, interpretację,
decyzję, korektę, ponowne review i czas przerwy. Raportować medianę,
rozrzut, liczbę otwartych kwestii i błędy krytyczne. To pomiar formatów;
kolejne prezentacje tego samego materiału mają efekt uczenia, który trzeba
odnotować, a nie nazywać ich niezależną ślepą ekstrakcją.

## Minimum IG-1 i warunki odbioru

Do zatwierdzenia proponuję następujący, ograniczony kontrakt:

1. Niezmienne artefakty źródłowe z hashem, wersją odczytaną z treści,
   rolą, pochodzeniem i odrębną informacją o zgodności materiałów.
2. Regiony i klauzule z trwałymi adresami aspektów; transkrypcja osobno
   od interpretacji. Jawne grupy wiążące warunki, skutki, wyjątki i czas.
3. Dowody, kwalifikowane odwołania, luki i konflikty. Dopuszczalne opisy
   opaque, bez udawania formalnego wyniku.
4. Minimalny profil kompozycji źródeł i snapshot przypinający rewizje;
   historia starszych decyzji poza aktywną selekcją reguł.
5. Review z dokładnym celem, podstawą, rodzajem oceny, uprawnieniem
   człowieka i stanem aktualności. Akceptacja i walidacja struktury osobno.
6. Coverage z poziomem reprezentacji i niezmiennym inwentarzem zakresu;
   run zachowujący surową odpowiedź i mapę pochodzenia przekształceń.
7. Walidator integralności oraz małe, samowystarczalne próbki pozytywne
   i negatywne. Bez silnika, UI, API i automatycznego rozstrzygania gry.

Warunki odbioru: każde odwołanie jest przypięte lub jawnie nierozstrzygnięte;
zmiana znaczenia nie dziedziczy akceptacji; konflikt źródeł pozostaje
widoczny; ten sam region nie zwiększa pokrycia wielokrotnie. Zły hash,
nieprawidłowy zakres decyzji, zamiana gałęzi warunek–skutek i zmiana
zależności mają odpowiednie odrzucenie lub blokadę. Opaque ma przejść
kontrolę zapisu i pozostać niedostępne dla obliczenia wymagającego jego
interpretacji. Osobno sprawdzić split/merge, starą decyzję w nowym
snapshocie i konflikt wewnątrz pojedynczego źródła.

Prywatne próbki tej recenzji są szkicami reprezentacji, nie pełnymi
snapshotami kontraktu. 36 przypadków wejściowego katalogu pozostaje
`proposed_not_run`. Wybrane mechanizmy sprawdzono źródłowo i projektowo;
nie uruchomiono 36 testów ani nie ustanowiono expected. Błędne odwołania
w katalogu mają osobną erratę, którą trzeba zastosować przed zamrożeniem
przyszłej oceny. Stary gold pozostaje bez zmian.

## Późniejsze rozszerzenia

Po walidacji rdzenia: strukturalne tabele i ich noty, formalny słownik
wyrażeń, wiązania wywołań, modele puli oraz testy kompozycji profili.
Osobno: transakcje procedur, reakcje i unieważnienia, historie zdarzeń,
topologia map, wyznaczanie ścieżek, perspektywy graczy, pełne obliczenia
scenariuszy i zwycięstwa. Każde rozszerzenie potrzebuje własnych przypadków
oraz ograniczenia do sprawdzonego systemu i wersji.

## Konkretne decyzje właściciela

| Decyzja | Rekomendacja | Co oznacza zgoda |
|---|---|---|
| D1. Cel IG-1 | Digitalizacja, wyszukiwanie, dowody i review; bez rozstrzygania partii | Przyjęcie siedmiu punktów minimum i podanych warunków odbioru |
| D2. Jednostka zapisu | B: klauzula z adresowalnymi aspektami; atomizacja opcjonalna | Próba A/B/C przed zobowiązaniem do osobnego rekordu każdej wartości |
| D3. Zakres prób | Pięć osobnych rodzin profili, 20 klauzul łącznie; trudne mechanizmy z aneksu | Wybór dokładnych źródeł/scenariuszy i uzupełnienie braków przed ekstrakcją |
| D4. Review | Tylko właściciel nadaje akceptację semantyczną w pierwszej próbie | Model i walidator dostarczają propozycje/obserwacje; delegowanie ludziom wymaga jawnych uprawnień |
| D5. Budżet | Dwa bloki po 60 minut aktywnego review jako limit pilota, nie obietnica ukończenia | Zapisać koszt i otwarte kwestie po limicie; nie poszerzać automatycznie zakresu ani nie nadawać statusu done |

Proponowana bramka jakości: zero nierozliczonych błędów krytycznych
w zakresach przedstawianych jako zaakceptowane, pełna rozliczalność
inwentarza próby i jawne blokady dla pozostałych. Próg użyteczności/czasu
dla całej instrukcji wymaga wyniku pilota; teraz jest unknown.

Zgoda na kierunek IG, zlecenie tej recenzji i zgoda na lokalną edycję
nie są przyjęciem D1–D5. Zgodnie z kartą IG-0 etap pozostaje partial.
ROADMAP zachowuje IG-0 jako jedyny next, a IG-1 planned.

## Zmiany i weryfikacja

Uzupełniono oba aktywne drafty o ograniczenie minimum, adresowanie aspektów,
podstawy review, historyczne referencje i jawne luki wykonawcze. Uaktualniono
plan, status, przekazanie i kartę. Numer roboczego formatu `ig-draft-0.2`
pozostaje etykietą draftu; rewizja dokumentacyjna `IG-0-review-1` nie stanowi
nowego przyjętego schematu. Archiwum nie jest aktualizowane.

Kontrole: `pwsh -NoProfile -File scripts/check.ps1` — **20 passed**;
`git diff --check` — kod 0. Test integralności potwierdził hashe i rozmiary
wszystkich 3117 plików archiwum. Sprawdzono też odnośniki aktywnych dokumentów,
ciągłość kolejki i składnię zastanych przykładów JSON. Logi:
`private/ig/_checks/active-edafd0dac13843079035c1ed9ebf992b/`.
To nie testy reprezentacji mechanik ani akceptacja nowych pól kontraktu.
Nie zmieniano testów, archiwów, gold ani oryginalnych odpowiedzi.
Nie wykonano commit/push.
