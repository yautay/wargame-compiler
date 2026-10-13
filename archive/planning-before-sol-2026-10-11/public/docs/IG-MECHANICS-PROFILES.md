# Rozszerzenie IG dla mechanik SPQR OSG i GCACW

- **Data:** 2026-10-11.
- **Status:** propozycja ig-draft-0.2, wymagająca recenzji i prób reprezentacji.
- **Cel po doprecyzowaniu właściciela:** semantyka umożliwiająca szybkie,
  deterministyczne [legalne akcje](IG-LEGAL-ACTIONS.md) i zmiany stanu dla AI.
  Nie wszystkie rozszerzenia są potrzebne od razu, ale zakres wpływający
  na legalność i wykonanie wybranego profilu nie może pozostać opaque.
- **Rewizja dokumentacyjna:** IG-0-review-1, po [recenzji](reviews/IG-0-critical-review.md); kontrakt nadal nieprzyjęty.
- **Cel:** wspólny format wiedzy o instrukcji z osobnymi profilami systemów.

Przegląd materiałów wydawców uzasadnia wspólny model danych, pod warunkiem
rozdzielenia reguł od sytuacji partii oraz rozbudowania opisu mechanik.
Rdzeń [IG](IG-DATA-MODEL.md) zachowuje źródła, obiekty, twierdzenia,
zależności, luki i review. Profile definiują słownik i semantykę konkretnego
systemu. Wspólna nazwa parametru nie oznacza wspólnego sposobu jego użycia.

Model opisuje instrukcję do digitalizacji i kontroli wiedzy. Poniższe
struktury pozwalają przygotować późniejszego wykonawcę reguł, ale jego
poprawność musi zostać sprawdzona oddzielnie.

Minimum IG-1 zachowuje opis tych mechanik, źródła, zależności i luki.
Nie wymaga implementacji wszystkich poniższych typów i operacji.
Wymagania wykonawcze są listą do późniejszej specyfikacji, nie gotowym
kontraktem operacyjnym. Występowanie nazwy pola nie dowodzi obsługi mechaniki.

## Zakres źródeł i pewność wniosków

Przeczytano wybrane fragmenty oficjalnych instrukcji, tabel i uzupełnień,
istotne dla projektu danych. Sprawdzono również zachowaną w repo instrukcję
SPQR 5th Edition: hash zgodny z manifestem POC, istotne strony przejrzane
tekstowo i obrazowo. Nie przeprowadzono pełnej ekstrakcji tych systemów.

| System | Podstawa przeglądu | Zakres weryfikacji |
|---|---|---|
| SPQR | Lokalna instrukcja 5th Edition i oficjalne materiały GMT | Aktywacje, wybory w walce, geometria jednostek, kolejność skutków i zakres scenariusza |
| OSG TLNB | Series Rules 7.38, tabele, noty i lista zmian | Dowodzenie, ukryte informacje, procedury, obliczenia, czas i zaopatrzenie |
| OSG Campaigns of Napoleon | Opis wydawcy i Napoleon at Bay Exclusive Rules 2020-b | Hierarchia sił, organizacja poza mapą, zasoby i łączność; standardowe reguły serii nieocenione w całości |
| OSG Days | Seven Days of 1809 i Last Days of the Grande Armée 2nd Edition | Wybrane fragmenty dowodzenia, losowania, rozkazów i organizacji |
| MMP GCACW | Standard Basic Rules 1.6, Charts & Tables 1.6 i RTG II | Cykle działań, stany, kalkulacje, wyniki i kompozycja Basic/Advanced |

Źródła internetowe i konkretne obserwacje zestawiono w prywatnym
`private/ig/research/2026-10-11/mechanics-evidence.md`.
Poniżej podano oficjalne odnośniki. Dowody szczegółowych reguł i przyszłe
sytuacje oceny pozostają prywatne.

**Wniosek projektowy:** wspólny rdzeń jest obiecujący dla tych rodzin,
ale zgodność jest hipotezą do sprawdzenia na przypadkach. Nie deklarujemy
pełnego pokrycia wszystkich gier OSG, GBoH ani GCACW.

## Profile i zgodność materiałów

OSG rozróżnia TLNB, Campaigns of Napoleon i Days. Traktujemy je jako
osobne rodziny profili. [OSG Game Series](https://napoleongames.com/pages/3-different-game-series)

Profil ma `publisher_id`, `series_id`, `game_id`, `ruleset_id`,
`ruleset_version`, `rules_mode`, `source_requirements`, `capabilities`
i `vocabulary`. Konkretna konfiguracja dodaje scenariusz, opcje, mapy,
żetony i decyzje kompozycji źródeł. Identyfikatory pojęć są kwalifikowane
systemem: `spqr:troop_quality` i `tlnb:initiative` pozostają różnymi
definicjami, choć oba mogą być odczytywane w testach.

`source_requirements` zapisują rolę, wersję, stan dostępności, sprawdzoną
zgodność i dowód. Lista pobrań na stronie wydawcy nie dowodzi wzajemnej
zgodności wszystkich umieszczonych tam plików. Starsze tabele wymagają
sprawdzenia wobec wybranego wydania instrukcji.

`composition_decisions` zawierają jawne operacje `include`, `replace`,
`amend`, `exclude` albo `map_equivalent`, dokładne cele, warunek zakresu
i review. Reguła scenariusza nie otrzymuje automatycznie pierwszeństwa
przed każdą regułą serii. Profil musi pokazać konkretną podstawę modyfikacji.

Cele kompozycji przypinają rewizje regionów, klauzul lub aspektów;
jedna decyzja dla całego PDF nie wystarcza, gdy zawiera on różne zakresy.
Nakładające się zmiany wymagają jawnego porządku albo konfliktu.
Sprawdzamy także podwójne zastosowanie poprawki już włączonej do wydania.

Profile początkowe to SPQR 5E, OSG TLNB 7.38, OSG CNS/NAB 2020-b,
osobne profile tytułów OSG Days oraz GCACW Basic 1.6 z modułem i trybem.
Simple GBoH otrzymuje osobny `ruleset_id`; nie jest zwykłym przełącznikiem
kilku wyjątków SPQR. GMT udostępnia osobne materiały i zapowiada setupy
dla Simple GBoH. [SPQR 5th Edition](https://www.gmtgames.com/p-1118-spqr-deluxe-5th-edition.aspx)

W obrębie jednego PDF numer reguły kwalifikujemy przez `document_part_id`,
`rules_mode` i scenariusz, gdy jest to potrzebne. Odczyt koloru, kursywy
i symboli zachowuje `semantic_annotations` z dowodem obrazowym;
ekstrakcja samego tekstu nie może usuwać istotnych wyróżnień.

## Definicje obiektów oraz stan partii

IG przechowuje definicje `unit_type`, `leader_role`, `formation_type`,
`state_variable`, `resource`, `action`, `event_type`, `timing_window`,
`selector`, `spatial_policy`, `randomizer`, `calculation` i `outcome`.
Ich znaczenie opisują twierdzenia z dowodami. Wpis parametru podaje domenę,
jednostkę, zakres wartości i sposób odczytu; nie nadaje wartości bieżącej partii.

Kontekst sytuacji, przechowywany poza grafem instrukcji, ma następujące części:

| Część | Treść |
|---|---|
| `rules_snapshot_ref` | Niezmienny zestaw reguł, źródeł i review |
| `profile_configuration` | Gra, tryb, opcje i scenariusz |
| `instances` | Konkretne jednostki, dowódcy, formacje i fizyczne żetony |
| `position` | Mapa, zajmowane heksy, orientacja, stosy i pozycje poza mapą |
| `state` | Niezależne stany i zasoby obiektów |
| `clock` | Instancje tury, fazy, aktywacji, kroku i okien reakcji |
| `history` | Fakty wcześniejszych działań potrzebne regułom |
| `pending_choices` | Wybory, które gracz musi lub może wykonać |
| `random_inputs` | Znane rzuty/losowania lub jawne niewiadome |
| `knowledge_view` | Perspektywa gracza i dostępne mu informacje |

Definicja jednostki, historyczna jednostka, jej instancja w scenariuszu
i fizyczny żeton mają osobne ID oraz mapowania. Odwrócenie żetonu może
zmieniać reprezentowany stan, ale nie zawsze oznacza zastąpienie jednostki.
Rozwinięcie, podział, połączenie lub substytucja wymagają jawnego mapowania
i zasad zachowania liczników, strat oraz historii.

Przynależność narodowa, strona konfliktu, właściciel, gracz kontrolujący
i podporządkowanie dowódcze są oddzielnymi relacjami. Współpraca dwóch
armii lub dowodzenie zespołowe nie są zwykłą równością kolorów żetonów.

## Stany historia i przyczyna zdarzenia

`state_variable` zawiera typ `boolean`, `enum`, `integer`, `rational`,
`set` lub `reference`, jednostkę, właściciela, granice i zasady resetu.
Stany takie jak organizacja, zdolność aktywacji, zmęczenie, straty,
zużycie amunicji i status dowodzenia mogą współistnieć. Nie sprowadzamy
ich do jednego uniwersalnego statusu `normal/disordered/routed`.

Opis przejścia w twierdzeniu `transition` podaje `event_type_id`,
`cause_filter`, `read_moment`, `before_refs`, `writes`, `limits`,
`reset_window_id` i dowody. `writes` są uporządkowanymi operacjami
`set`, `increment`, `decrement`, `flip`, `move`, `remove`, `schedule`
lub `invoke`, z wyraźnymi celami i granicami.

Takie same wartości po zdarzeniu nie dowodzą tej samej historii ani
tych samych skutków ubocznych. Zmiana wywołana kosztem działania może
mieć inne następstwa niż zmiana wywołana wynikiem walki. Reguła uruchamiająca
procedurę musi więc wskazywać przyczynę, a nie jedynie próg liczbowy.

`history_requirement` opisuje potrzebne fakty: licznik działań w instancji
tury, wcześniejsze położenie, pierwsze wystąpienie, użytego uczestnika,
próbę nieudaną lub już rozliczony koszt. Brak historii jest luką wejściową.
Nie zakładamy zera poprzednich działań tylko dlatego, że obecny znacznik
ich nie pokazuje.

Późniejszy kontrakt musi odróżniać próbę, zatwierdzone zdarzenie, jego
przyczynę i ewentualne unieważnienie. Sam końcowy stan ani samo `writes`
nie dowodzą, czy zdarzenie liczy się w historii. Niepełna historia
blokuje zależny wniosek, lecz nie zapis i wyszukanie instrukcji.

Rozróżniamy `permission`, `obligation` i `prohibition`, a także koszt
podjęcia próby i koszt sukcesu. Rezygnacja po rozpoczęciu procedury,
nieudany test i brak legalnego celu mogą mieć różne następstwa.

## Czas reakcje i przepływ procedur

Definicja czasu to hierarchia instancji: tura → faza → segment → aktywacja
→ krok → zdarzenie. Profil wybiera potrzebne poziomy; nazwa fazy nie jest
instancją jej konkretnego wystąpienia. Ograniczenie „raz” ma `counter_scope`:
obiekt, strona, aktywacja, tura lub cała partia.

Krok procedury opisuje `actor_role`, `guard`, `inputs`, `outputs`,
`next_steps`, `reaction_windows`, `completion_condition` i `failure_path`.
Przejścia mogą mieć warunki, pętle, wcześniejsze zakończenie i powrót do
procedury nadrzędnej. Samo `precedes` nie wystarcza do opisania przerwania.

`timing_window` określa wyzwalacz, uprawnionego gracza, warunek otwarcia,
moment zamknięcia, licznik prób i kontynuację: `resume`, `replace`,
`cancel` lub `restart`. Bez źródła nie zakładamy, że po reakcji poprzednia
aktywacja zawsze wraca.

`cancel` nie definiuje cofania skutków już wykonanych. Jeżeli źródło
unieważnia czynność, zachowujemy jego dokładny opis i lukę formalizacji.
Wykonawca wymaga osobnej polityki zatwierdzenia/unieważnienia: które skutki,
koszty, liczniki i zdarzenia pozostają. Nie zakładamy globalnego rollbacku.
Przerwanie/powrót musi wiązać się z instancją wywołania i jej środowiskiem
lokalnym; statyczny link do definicji kroku tego nie zastępuje.

Skutek czasowy ma `starts_at`, `expires_at`, `checkpoint`, `snapshot_reads`
i `refresh_policy`. Odróżniamy stan sprawdzony w wyznaczonym momencie od
warunku liczonego nieprzerwanie. Naprawiona infrastruktura może mieć
różne momenty dostępności dla różnych czynności; graf zachowuje te
osobne reguły zamiast jednego `usable: true`.

Nie wprowadzamy wspólnej kolejki reakcji ani globalnego priorytetu.
Źródło określa kolejność, równoczesność i stronę rozstrzygającą remis.
Nieznane porządkowanie pozostaje luką, również dla kilku efektów na tym
samym obiekcie.

## Wybory uczestnicy i agregacja

`choice` ma `decision_owner`, `candidate_selector_id`, `cardinality`,
`constraints`, `binding_id`, `binding_lifetime`, `rechoose_policy`
i powiązane twierdzenia. Wybór gracza, automatyczne wskazanie przez regułę
i losowanie to trzy różne operacje.

Wybór używany w dalszych krokach jest utrzymywany przez nazwane wiązanie.
Nie wolno osobno wybierać najlepszego uczestnika do każdego korzystnego
parametru, jeżeli procedura wymaga użycia tej samej jednostki.
`selected`, `eligible`, `committed`, `participating` i `affected` to
osobne zbiory; mogą być różne po nieudanym teście lub reakcji.

`binding_id` jest nazwą definicji wiązania; wartość uczestnika należy do
konkretnej instancji procedury. Osobne wywołania nie współdzielą wartości.
W digitalizacji wystarczy opis tej zależności i dowód; reguły czasu życia
oraz ponownego wyboru muszą być formalnie sprawdzone przed wykonaniem.

`aggregation` określa zbiór, filtr, miarę, operację (`sum`, `max`,
`min`, `count`, `all`, `any`) i kolejność modyfikacji. Sumowanie wielkości
siły, siły bojowej i wartości artylerii korzysta z osobnych definicji.
Rozdział strat zapisuje wybierającego gracza, dopuszczalne cele,
proporcje, nadwyżki i moment eliminacji.

## Przestrzeń i pomiary

`spatial_policy` definiuje pomiar i jego cel. Polityki ruchu,
dowodzenia, zaopatrzenia, odwrotu i widoczności pozostają osobne,
nawet jeśli wszystkie odwołują się do tej samej mapy heksowej.

| Element | Pola wymagane do jednoznacznego odczytu |
|---|---|
| Lokalizacja | `map_id`, `sheet_id`, `hex_label`, topologia i połączenia arkuszy |
| Geometria jednostki | `occupied_hexes`, `anchor`, `orientation`, strefy względne i sposób pivotu |
| Teren | Właściwości heksu i krawędzi, wysokość, infrastruktura oraz stan |
| Dystans | `metric`, jednostka, liczenie początku/końca, limity i zaokrąglenia |
| Ścieżka | Dopuszczalne węzły i krawędzie, koszt, zakazy, wymagane punkty oraz wyjątki |
| ZOC | Polityka projekcji, warunki terenu, kontekst działania i wpływ jednostek |
| LOS | Kierunek obserwacji, wysokość, przesłony, granice i przypadki niesymetryczne |
| Stos | Kolejność i zgodność składu, limit oraz moment sprawdzenia |
| Pozycja poza mapą | Nazwana strefa, tor, pojemność, przynależność i warunki przejścia |

Heksy o takim samym numerze na dwóch arkuszach nie są jednym miejscem.
Odległość w heksach, kosztach ruchu i jednostkach historycznych nie jest
wymienna bez jawnego mapowania. Jedna fizyczna jednostka może zajmować
więcej niż jeden heks; policzenie jej dwa razy w sile lub stratach jest błędem.

Pełny model nie wymaga od razu wektoryzacji wszystkich map. Może wskazywać
obrazy i politykę, oznaczając nierozpoznaną topologię jako lukę.

Opis ścieżki rozróżnia istnienie legalnej trasy, wymóg wszystkich tras,
optymalność oraz wybór między równorzędnymi trasami. Nie utożsamiamy
osiągalności, najkrótszej drogi i priorytetów ruchu/odwrotu.

## Losowość obliczenia i tabele

`randomizer` określa fizyczne symbole, znaczenie symboli, liczbę losowań,
operator łączenia, niezależność oraz zasady zwrotu do puli. Kość, worek
żetonów, ręka gracza i talia są różnymi modelami. Profil nie przekształca
automatycznie każdego dziesięciościennego rzutu do zakresu 1–10.

Pula wymaga wielokrotności: multizbioru symboli lub zbioru fizycznych
instancji elementów. `set` wartości nie wystarcza, gdy powtarzają się symbole.
Skład początkowy, właściciel, transfery między pulą/ręką/zagranymi elementami
i moment zwrotu są osobnymi danymi. Nieznany skład nie daje znanego rozkładu.
Te struktury stanu należą do przyszłego wykonawcy; IG-1 zachowuje ich opis.

Przechowujemy `raw_result`, `modified_result`, etapy modyfikacji i ID
losowania. Reguła sprawdzająca wynik naturalny nie korzysta z wartości
po modyfikatorach. Test powtórzony albo wspólny dla kilku celów ma jawny
zakres i sposób ponownego użycia wyniku.

`calculation` jest uporządkowaną listą kroków z wejściami i dowodami.
Operacje obejmują `add`, `subtract`, `multiply`, `divide`, `compare`,
`round`, `clamp`, `column_shift`, `lookup`, `decode` i `invoke`.
Rozróżniamy zmianę wejściowej siły, zmianę rzutu, przesunięcie kolumny
i zmianę wyniku po odczycie tabeli. Każde ma osobny cel i moment.

Zaokrąglenie zapisuje etap, metodę, stronę uprzywilejowaną i warunek.
Ułamki przechowujemy jako liczby wymierne, gdy tego wymaga reguła.
`stacking_policy` modyfikatorów określa sumowanie, wykluczenie, zastąpienie,
limit albo wybór jednego. Nie domyślamy się sumowania wszystkich bonusów.

Tabela ma uporządkowane osie z przedziałami, włączeniem granic,
polityką wartości poza zakresem, brakujących pól i legendą.
`lookup` wskazuje rewizję tabeli, mapowanie wejść, wybranych uczestników,
zakres not i dekoracje o znaczeniu semantycznym.

`outcome` zawiera pierwotny symbol i listę warunkowych skutków, ich cele,
porządek, czas i opcjonalne wywołanie następnej procedury.
Jeden wynik może dotyczyć kilku stron i wielu liczników. Symbol bez
odczytanej legendy jest niekompletnym wynikiem, a nie gotową komendą.

## Informacja ukryta i zwycięstwo

`visibility` opisuje odbiorców informacji i warunki ujawnienia.
Wiedza narzędzia o pełnym stanie nie oznacza, że gracz może użyć tej
informacji do decyzji. Zapytanie przyjmuje `viewer_role` i zwraca
dozwoloną perspektywę lub blokadę; nie zmyśla składu ukrytej siły.

Jest to wymaganie przyszłego produktu, nie działająca gwarancja IG-1.
Polityka musi obejmować cały wynik: także dowody, ścieżki, luki, powody
odrzucenia i metadane, które mogą ujawnić ukryty fakt. Sam filtr pola stanu
lub końcowej odpowiedzi nie wystarcza. Digitalizacja publicznej instrukcji
nie wymaga przechowywania tajnego stanu konkretnej partii.

Warunki zwycięstwa mają `metric_id`, zbiór liczonych obiektów,
`checkpoint`, sposób porównania, moment końca partii i rozstrzygnięcie
remisu. Należy rozróżnić próg zależny od scenariusza, natychmiastowy
koniec i ocenę na końcu tury. Kontrola terytorium też wymaga własnej
definicji i pamięci, jeśli znaczenie zależy od wcześniejszego zajęcia.

## Kierunki nowych relacji

| Relacja | Kierunek |
|---|---|
| `reads` | Twierdzenie lub krok → definicja odczytywanego stanu/zasobu |
| `writes` | Twierdzenie lub krok → definicja zmienianego stanu/zasobu |
| `triggers` | Typ zdarzenia → uruchamiany krok/procedura; filtr przyczyny obowiązkowy, jeśli istotny |
| `schedules` | Twierdzenie lub krok → okno późniejszego zastosowania skutku |
| `resumes` | Procedura reakcji → punkt kontynuacji procedury nadrzędnej |
| `constrains` | Twierdzenie ograniczenia → wybór, działanie, ścieżka albo wynik |
| `uses_binding` | Krok lub twierdzenie → wybór dostarczający utrzymywanego uczestnika/wartość |

Dowody i zakres review są wymagane tak samo jak dla relacji pierwotnego
draftu. Analiza wpływu korekty przechodzi po odczytach, zapisach,
wyzwalaczach, wiązaniach, tabelach i profilach. Jeżeli relacje nie są
kompletne, nie wolno certyfikować braku regresji na podstawie samego grafu.

## Reprezentacja minimalna i wymagająca formalizacji

Minimalny IG może zachować tekst, dowody, wymagania wejściowe, wybory
i strukturę procedury bez obliczania wyniku. Dla dowolnego zapytania
zapisuje `representation_complete`, `semantic_review_complete`
oraz `resolvable_for_query` jako trzy osobne oceny z uzasadnieniem.

Wartość `opaque` pozwala przechować nieformalny fragment. Blokuje
rozstrzygnięcia wymagające jego wykonania, ale nie blokuje cytowania
ani wyszukania reguły. Brak stanu partii, nieznany rzut i nieodczytana
tabela to różne przyczyny blokady.

Obsługę wykazuje się przez reprezentację przypadków i kontrolę
źródłowych wniosków, a nie przez samo istnienie pola `payload`.
Zestaw proponowanych przypadków jest zapisany prywatnie. Wszystkie
pozostają `proposed_not_run`, nie rozszerzają starego eval-v1.

Recenzja IG-0 zawiera źródłowe sprawdzenie wybranych mechanizmów i szkice
z każdej rodziny, ale nie wykonuje tego zestawu jako testów. Nowe ustalenia,
korekty lokalizatorów wejściowego katalogu i odczyty obrazowe zapisano w
`private/ig/reviews/IG-0/evidence-and-examples.md`. Mają pierwszeństwo
informacyjne wobec błędnych lokalizatorów wcześniejszych notatek;
nie są zaakceptowanymi expected. Hashe pobranych PDF są w sąsiednim manifeście.

## Plan sprawdzenia i praca operatora

Aktualny [plan](IG-PLAN.md) prowadzi od adaptera całej KB WGU do pełnego
IG instrukcji SPQR. Przykłady służą testom kontraktu, nie stanowią osobnej
bramki pilota. Profile OSG i GCACW będą wymagały własnej weryfikacji przy
rozszerzaniu produktu; jakość SPQR nie dowodzi ich poprawności.

Operator powinien otrzymywać pakiet dokładnych zmian: źródło, wcześniejszą
i nową wersję twierdzenia, zmienione zależności, wynik kontrolowanych
sytuacji i proponowany zakres decyzji. Czas mierzymy osobno dla pozyskania
źródła, przekazania ekstrakcji, oceny i korekty. Koszt całej instrukcji
szacujemy i aktualizujemy na podstawie pomiarów pakietów w pełnym przebiegu.

Ryzyko projektu to nadmierna liczba drobnych rekordów i koszt ich review.
Należy porównać przechowywanie atomowych twierdzeń z wygodną prezentacją
całych klauzul. Grupowa decyzja może obejmować wiele jawnie wyliczonych
celów, bez dziedziczenia akceptacji przez nieprzejrzane pola.

## Oficjalne źródła

Przegląd: 2026-10-11. Wersje podano według odczytanego materiału;
nie są deklaracją, że dany plik jest najnowszy dla wszystkich tytułów.

- [GMT SPQR 5th Edition i lista materiałów](https://www.gmtgames.com/p-1118-spqr-deluxe-5th-edition.aspx).
- [SPQR 4th Edition Living Rules Oct 2022](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/gbsp/SPQR_4thEdition_Living_Rules_Draft_Oct2022.pdf).
- [SPQR 4th Edition Errata Oct 2022](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/gbsp/SPQR_4th_Ed_Errata_and_Clarifications_Oct2022.pdf).
- [SPQR Scenario Book 2018](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/gbsp/SPQR-Scenario-Book-2018-5.pdf).
- [OSG Game Support Files](https://napoleongames.com/pages/game-support-files).
- [OSG TLNB Series Rules 7.38](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/TLNB_SeriesRules-7.38-2.pdf?v=1741466415).
- [OSG TLNB Combat Tables](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/COMBAT_TABLES.pdf?v=1603420083).
- [OSG TLNB Notes to Combat Tables](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/NOTES_TO_COMBAT_TABLES.pdf?v=1603420077).
- [OSG Changes to TLNB 7.36](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/Changes_to_TLNB_Series_Rules_7.36-3.pdf?v=1706111836).
- [OSG Campaigns of Napoleon](https://napoleongames.com/pages/campaigns-of-napoleon-series-1x).
- [OSG Napoleon at Bay Exclusive Rules 2020-b](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/nab_exclusive_rules_update_kit__24k.pdf?v=1601499015).
- [OSG Seven Days of 1809](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/7D09-Rules_3.27.pdf?v=1603456254).
- [OSG Last Days of the Grande Armée 2nd Edition](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/ldga_1.12paged.pdf?v=1603458711).
- [MMP GCACW Downloads](https://mmpgamers.com/gcacw-downloads-ezp-8).
- [MMP GCACW Standard Basic Rules 1.6](https://mmpgamers.com/support/gcacw/GCACW_Series_Rules_1.6.pdf).
- [MMP GCACW Charts and Tables 1.6](https://mmpgamers.com/support/gcacw/GCACW_Charts_Tables_1.6.pdf).
- [MMP Roads to Gettysburg II rulebooks](https://mmpgamers.com/support/gcacw/RTG2_Rules.pdf).

Internetowy PDF 5E nie został odczytany przez narzędzie przeglądania.
Weryfikację 5E oparto na zachowanym pliku z repo, a nie na przeniesieniu
ustaleń z 4E. PDF źródłowy i hashe wskazuje prywatny rejestr badań.
