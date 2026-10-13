# M-POC5A.4b2 — co zostało sprawdzone i co proponuję przyjąć

Przejrzałem wszystkie **30 przypisanych ID w obu odpowiedziach: 60 wystąpień**.
Porównałem źródłowe klauzule, rzeczywiste zapisy relacji, reguł i luk oraz
obejrzałem dostarczone strony 31–34 i 37 oraz wyłącznie dostarczony wycinek
kroku 4. Nie pozyskałem treści brakujących celów. Poniższe oceny są
propozycjami; znaczenie akceptuje właściciel.

**Dwie decyzje do podjęcia:**

1. Przyjąć **26 ID / 52 wystąpienia** w dokładnych zakresach nazwanych
   odniesień i wymagań brakującego źródła, opisanych niżej. Przyjęcie obejmuje
   rolę relacji, kierunek, jawność i potrzebę celu do wskazanego pełnego
   wykonania. Nie obejmuje treści celu, jego aliasu, całych rekordów ani
   automatycznej blokady lokalnej operacji przy zadanych faktach.
2. Dla pozostałych **4 ID / 8 wystąpień** przyjąć poprawność lokalnych
   powiązań wyjątków, ale **ograniczyć blokadę do nieznanego dalszego
   wykonania lub skutków**. Sam wyjątek jest już podany w rozdziale.
   To proponowane rozstrzygnięcie nowego SEM-017, wyjaśnione poniżej.

[Porównanie każdego ID](comparisons.md) i [pełny ślad do bajtów](comparisons.json)
zawierają dwa osobne wyniki z hashami odpowiedzi, zakresem źródła, surowymi
rekordami i polami, pointers oraz zakresami bajtów. Faktyczne otwarcie lub
odczyt tych plików przez właściciela pozostaje unknown.

## Brakuje źródła do wykonania, ale lokalna reguła jest znana

**Pass-Thru słonia.** Instrukcja każe przeprowadzić Pre-Shock według 8.43
i bazowy Shock, po czym stosuje lokalne zmiany strat. Model wskazuje te
brakujące procedury oraz definicję ZOC potrzebną do sprawdzenia warunku
na początku Orders Phase. To poprawne wymagania źródła. Jeśli jednak
prawidłowy bazowy rzut lub straty są już zadane, można lokalnie zastosować
+1 DRM, połowę strat obrońcy z zaokrągleniem w dół i zmniejszenie strat
słonia o 1. Brak całej procedury nie usuwa tych operatorów. Po kontekście
znamy krok 4 ogólnego Shock, lecz nadal nie znamy wcześniejszych etapów
i tabeli. Przyjęcie tych odniesień nie zatwierdza całego Pass-Thru.

**Ekran i jeźdźcy na słoniu.** Model prawidłowo rozdziela potrzebę 8.2,
wiersza Elephant Screen w MRRC oraz właściwości Mounted Javelinists.
Instrukcja podaje, że ekran strzela tylko w Reaction Fire, a oszczepy
i ekran wymagają osobnych rzutów. Możemy przyjąć te role i ograniczenia;
bez procedury i rzeczywistej tabeli nie wyliczymy legalnego pełnego
strzału. Opis tabeli w 8.71 nie jest jej wierszem. Pozwolenie z 9.13
nie znosi zakazu jakiejkolwiek Reaction Fire podczas Rampage.

**TQ i rozdział wewnątrz stosu.** W 10.11 ogólny test odsyła do wyniku
z Cohesion Hit and TQ Check Chart. To użycie tabeli, a nie samo wskazanie
podsumowania: źródło wprost każe zastosować wynik z chart. Lokalny test,
którego skutek podano osobno, pozostaje innym zakresem. Z kolei 10.13
odsyła rozdział strat wewnątrz stosu do 6.68 bullet #6. Model zachowuje
tę lukę i blokadę. Przykład ze stratą top Hastati nie zastępuje pełnego
6.68. Wcześniejsza decyzja o niewystarczającej blokadzie na D9621013 nie
dostarcza brakującego przepisu i nie zamyka całej alokacji.

**Rampage, mapa i dowódcy.** Model prawidłowo rozdziela trzy potrzeby:
rzut 1–6 wymaga compass rzeczywiście wybranej mapy; dowódca w heksie
na drodze słonia wymaga oceny wycofania według 4.72; dowódca jadący
na szalejącym słoniu podlega po zakończeniu procedurze casualty z 4.73.
To różne sytuacje. Obraz compass jest przykładem, a nie orientacją każdej
bitwy. Brak mapy nie blokuje wszystkich wierszy tabeli: np. lokalny wynik
eliminacji Leader Elephant na 0 nie wymaga wyboru kierunku z compass.
Podobnie zadane „dowódca nie może się wycofać” pozwala zastosować
lokalną automatyczną śmierć, choć nie dostarcza zasad ustalania tej możliwości.

**SK, LC i obrona falangi.** Model poprawnie wskazuje ogólne OW, H&D,
Missile Fire i CRT jako potrzebne do pełnego wykonania. Zachowuje przy tym
lokalne ograniczenia: dwa heksy OW i właściwe kierunki kosztów SK/Velites,
+2 do rzutu gdy celem jest SK, H&D tylko dla uzbrojonej w pociski LC
przeciw niższemu MA z wyłączeniem SK oraz strzał podczas OW dla LC Archers.
Wyjątek pojedynczej SK/Velites przerywającej linię nie zastępuje całego 4.32;
przykłady pokazują, że pojedyncze rozdzielone przerwy mogą wystąpić wielokrotnie.
Odesłanie do 6.69 dotyczy właściwych specjalnych zasad stacking, a nie
podsumowania typu wcześniej rozstrzygniętego D961stack.

W 9.41 można wyznaczyć lokalny shift z zadanej kolumny i kwalifikujących
flank. Realne straty nadal wymagają CRT. Pozostają warunki ataku z ruchu
przez Front, ograniczenie dla HI oraz wyłączenia ataku bez ruchu, Flank/Rear
i dowolnej atakującej PH. Przykład 5→1 zakłada brak innych zmian.

## Co rzeczywiście zmienił kontekst

**29 z 30 relacji jest identycznych.** Zmieniła się D932CRT: przed kontekstem
model potrzebował CRT i operacji związanej z AS, a po kontekście oddziela
dostarczone warunkowe operacje AS/LC od nadal brakującej rzeczywistej tabeli.
W obu przypadkach pełny wynik pozostaje zablokowany.

Osobno zmieniły się opisy luk G-D923shock i G-D932CRT. Pierwsza uwzględnia
znany operator dla wybranego obrońcy SK, ale nadal potrzebuje zasad wyboru
Type/Size i bazowych wyników. Druga uwzględnia dostarczone AS/LC, lecz
nadal potrzebuje CRT i nierozstrzygniętego kontekstu kolejności.

**Proponuję przyjąć to jako poprawne, częściowe doprecyzowanie potrzeby.**
Nie oznacza akceptacji całej walki, nowego pola wyjątków R932 lub zamknięcia
SEM-003/pozostałego SEM-004. Nie uznajemy, że AS i połowa LC automatycznie
się „kasują”. Przy zadanych stratach lokalna połowa jest innym pytaniem
niż pełny odczyt CRT.

## SEM-017 — cztery wyjątki nie powinny znikać przez brak ogólnych zasad

Instrukcja podaje wprost poniższe wyjątki. Model zachowuje je w treści,
ale ich relacje i luki mają szeroką deklarację blokady przypisaną całemu
rekordowi. Nie wykazano konkretnego błędnego wyniku gry. Właściciel
rozstrzyga, czy taki zapis wystarczająco odróżnia znany wyjątek od
nieznanego pełnego wykonania.

| Relacja w obu odpowiedziach | Co wiemy ze źródła | Co pozostaje nieznane |
|---|---|---|
| D914OW | OW wobec szalejącego słonia jest wyjątkiem od natychmiastowego priorytetu Rampage. | Kto faktycznie może wykonać OW i jak wykonać je według 6.51. |
| D915superiority | Kawaleria atakująca słonia przez Flank/Rear nie otrzymuje zwykłej AS. | Pozostałe ogólne zasady i liczbowe skutki przewagi w pełnej walce. |
| D917position | W walce Elephant–Elephant żadna strona nie dostaje Position Superiority; atak Flank/Rear nie daje AS. | Pełne ogólne definicje/skutki; nazwy nie ustalają zewnętrznego aliasu. |
| D923pre | Atak na samych SK zwalnia z testu. PH/HI/LG broniące Front przed LI są zwolnione, ale atakujące LI nadal sprawdzają; odwrotna sytuacja nie daje zwolnienia. | Wykonanie testów jednostek niezwolnionych oraz realna kwalifikacja uczestników. |

**Rekomendacja:** przyjąć poprawne powiązania wyjątków oraz stwierdzić,
że brak celu blokuje tylko potrzebne, nieznane dalsze wykonanie/skutki.
Przy zadanych właściwych uczestnikach i kierunkach nie powinien blokować
odpowiedzi „nie dostaje AS” lub „nie wykonuje tego testu”. Nie zamykamy
przez to całej walki ani nie zmieniamy oryginalnej odpowiedzi.

## Dokładny pozytywny zestaw do decyzji 1

26 ID / 52 wystąpienia, osobno po 26 w first-001 i context-01:

`D-ZOC-R911, D-ZOC-R915, D1011chart, D1013stack, D911pre, D911shock,
D912MRRC, D912react, D913mounted, D913react, D914casualty, D914compass,
D914leaderwithdraw, D916OW, D919clash, D919pre, D919shock, D921OW,
D922missile, D923shock, D924line, D924stack, D931HD, D931OW,
D932CRT, D941CRT`.

Pozostałe 4 ID / 8 wystąpień mają osobną decyzję SEM-017. Zbiory są rozłączne
i obejmują wszystkie przypisane 60 wystąpień. Wszystkie nowe oceny właściciela
pozostają pending do odpowiedzi na ten pakiet: oceniający porównał 60,
udostępniono 60, nowych decyzji właściciela 0. Udostępnienie nie poświadcza
otwarcia plików.

## Co pozostaje otwarte

Poprzednie 125 zakresów relacji i decyzje 1–6 zachowano, podobnie jak po
63 lokalne zakresy i 3 wymagania źródła w obu odpowiedziach. SEM-001–013
w pozostałych zakresach, osiem oczekiwań EXP-010/017/019/040/050/052/066/074,
wyłączone pola, lokatory i pełne wyniki nadal otwarte. Żadnej starej decyzji
nie rozszerzam ani nie nadpisuję.

Łącznie porównano 185 przypisanych wystąpień relacji. **.4b3 ma jeszcze
36 ID / 72 wystąpienia** do pełnego przeglądu; wcześniejsza wąska decyzja
o dodatkowej wzmiance D961stack nie wykonuje tej partii. .4c/.4d i 20 sytuacji
M-POC5B są osobnymi częściami. M-POC5A/.4/.4b pozostają partial.

Nie przyznano nowych TP/FP/FN ani precision/recall; 105 candidates nie
staje się gold. Nie pozyskano nowych stron, reguł lub tabel, nie powtórzono
ekstrakcji ani nie poprawiono odpowiedzi. Limity i wcześniejsze niewiadome
izolacji, aktywnego czasu, konfiguracji i kosztu pozostają bez zmiany.
