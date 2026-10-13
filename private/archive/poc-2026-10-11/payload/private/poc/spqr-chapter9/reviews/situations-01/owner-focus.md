# M-POC5B — wyniki sytuacji i proponowane decyzje

Zatwierdzenie uzgodnienia .4d5 zapisałem jako **owner-decision-15**. Zachowuje414 wcześniejszych decyzji inwentarza i starsze8 oczekiwań/13 kwestii; nie rozstrzyga ich wariantów.

Wykonałem całe M-POC5B: **20 zamrożonych sytuacji w obu oryginalnych odpowiedziach,40 porównań**. Przeczytałem właściwe źródła, wszystkie fakty i warianty pytań oraz odpowiednie oryginalne pola. Każdy przypadek ma osobne ślady do bajtów obu odpowiedzi.

Oryginały zawierają reguły. Poniższe obliczenia są **wyprowadzeniami oceniającego z tych zapisanych reguł przy zadanych faktach**. Nie są nowymi odpowiedziami modelu na sytuacje ani wynikiem uruchomienia silnika. Nie wykonałem ekstrakcji, korekty lub nowej inferencji.

| Proponowana ocena pełnej sytuacji | first-001 | context-01 |
|---|---:|---:|
| Zgodny lokalny wynik |15|14|
| Właściwa oczekiwana blokada |3|3|
| Kandydat nieuzasadnionej lokalnej blokady |1|1|
| Pełny wynik zawieszony po porównaniu |1|2|
| Pełny mianownik |20|20|

Wszystkie40 wystąpień porównałem; trzy zawieszone pełne wyniki mają przejrzane i opisane komponenty, a nie pominiętą pracę. Nie przyznaję części sukcesu za pojedynczy wariant. Oczekiwanych blokad nie zaliczam do meaningful local results dla progu80%. Liczniki są propozycjami do przeglądu właściciela.

## 1. Proponuję przyjąć35 ograniczonych pozytywnych ocen

To29 lokalnych wyników oraz6 ocen właściwych blokad. Dokładne ID/run prowadzi [presentation.json](presentation.json).

**Pass-Thru i testy:** przy wszystkich zadanych warunkach LI może wybrać opcję, +1DRM trafia do jej Pre-Shock, bazowe5Hits obrońcy dają2, a3Hits słonia dają2. Po zadanym braku Rout/Rampage końcowe placement pozostawia wybór wolnego Rear graczowi EL i zachowuje facing. ZOC na początku fazy nadal wyklucza opcję mimo późniejszego wyjścia. SK nie robi końcowego Pass-Thru check; to nie zwolnienie każdego testu Pre-Shock. Model rozdziela te kroki i adresatów.

**Rampage i wyjątek Leader Elephant:** dla zwykłego EL pierwszy8 oznacza ruch od zadanej przyczyny i próbę3heksów na podanej wolnej trasie; kolejny8 eliminuje. Leader Elephant przy drugim8 ma jawny wyjątek natychmiastowego rally. Zadane syntetyczne TQ6 daje4CH przez6−2. Ogólny zakaz rally nie uchyla tego szczególnego wyjątku. Brak osobnej krawędzi nie usuwa zachowanej treści wyjątku w polach i tabeli; nie nadaję przez to TP/FN grafu.

**Lokalne liczby:** SK z bazowymi Hits1,3,6 daje0,1,1 po pół/rounddown/cap1. DD przy zadanym legalnym stosie i Flank Shock przekształca3 przez3× do9, następnie dzieli na top5/bottom4. Dawna niepewność eliminacji DD dotyczy późniejszego Rout, który jest wyłączony z tego pytania; nie blokuje tego podziału. Phalanx Defense dla ruchomego HI i dwóch właściwych flanków daje2L; startując z sąsiedztwa i pozostając tam —0L. To shift, bez odczytu wyniku CRT.

**Stosy i MLE:** LC nie pozwala zamienić kolejności stosu, ale spełnia lokalny wymóg zmiany facing. Przy zadanym TQ górnej jednostki7 obie wykonują własne testy z7 oraz+1 za różne kolory. MLE dopuszcza tylko zadany wolny Clear bez enemy ZOC; inne trzy warianty celu są wykluczone. Górna jednostka idzie w bok, facing pozostaje, przy eligible LC obie mogą potem ruszyć z MA−2 i bez Hits za MLE. Odwrócenie diagramu nie daje prawa tworzenia stosów. Te same jednostki nie mogą jednocześnie wykonać OW i MLE; rezygnacja z pierwszej okazji MLE nie kasuje następnych właściwych okazji.

**Scorpio:** zmiana Move→Fire blokuje strzał w tej samej fazie. Przy jednym aktywnym strzale w turze i zerze w bieżącej fazie kolejny jest dostępny; po nim marker Finished i brak Recovery w tej fazie. Po dwóch aktywnych strzałach nie ma trzeciego. Nowa faza przeciwnika ma odrębny limit reakcyjny2, więc po jednym zostaje jeden. Oceniono zadany cel, który nie jest Rampaging EL; nie przyjęto przez to brakującej relacji do tego wyjątku. Zakazu innych działań po aktywnym strzale nie przeniosłem automatycznie na specjalny ogień reakcyjny.

**Impetuosity i transport:** przy zadanym dowództwie A druga BI uruchamia koniec stanu dopiero po końcu Game Turn2. Do tego czasu MA5+1=6 i−1first-try Momentum; B nie traci stanu przez trigger A. Przy zsiadaniu LI z MA5 po4MP zostaje1MP; po5MP nie ma dalszego ruchu. Wsiadanie po3MP daje CH z MA8 jeszcze5MP. Koszt wsiadania/zsiadania jest0MP/0Hits, Low/No znika przy wsiadaniu, mounted LI nie atakuje Shock, a partial-phase mount nie spełnia warunku całej fazy dla zwolnienia za powtórny ruch.

**Trzy właściwe blokady w każdej odpowiedzi:** bez mapowego kompasu nie można wybrać rzeczywistego kierunku Rampage; bez listy scenariusza nie można ustalić eligibility realnych PH do DD; bez przypisania dowództwa BI nie można wybrać Initiative ani zasięgu utraty Ferocity. Bliskość leadera lub korzystniejszy rating nie zastępują przypisania. To potrzebne źródła dla konkretnych pytań, a nie blokowanie lokalnych operatorów przy już zadanych faktach.

## 2. SIT-07 — źródło daje0CH, zapis pozostawia gałąź nieznaną

W sytuacji zadano DR5=TQ5, brak możliwości OW i brak Rout. Zamrożony expected oraz instrukcja wiążą Hits z DR>TQ, więc dla równości przewidują0CH; natychmiastowy test nadal jest wymagany.

Oba R916 zachowują warunek DR>TQ i minimum1, ale interpretation jest unknown, a G916 jawnie blokuje rozstrzygnięcie DR≤TQ do wyjaśnienia. W zapisanej reprezentacji ta konkretna gałąź nie ma ustalonego wyniku. Nie twierdzę, że model odpowiedział „1Hit” — takiej odpowiedzi na sytuację nie ma.

**Rekomendacja2:** potraktować dwa wystąpienia SIT-07 jako kandydat nieuzasadnionej lokalnej blokady/niepełnego określenia wyniku przy zadanych faktach. To zastosowanie dawnej SEM-001, bez jej automatycznego zamknięcia. Brak pełnego OW lub rzeczywistego ratingu nie jest tu uzasadnieniem, bo odpowiednie fakty są zadane. Oryginał pozostaje bez poprawki.

## 3. SIT-16 — liczby zgodne, pełne połączenie bramek pozostaje otwarte

Oba zapisy dają floor(11/2)=5:RP4 nie spełnia bramki9.72, RP5 ją spełnia. Wyjątek stationary Shock przeciw enemy w zadanej ZOC działa przy obu RP. Bramka ruchu9.71 została w faktach zadana jako spełniona.

Pytanie zawiera również wniosek, że sam RP nie uchyla9.71. To sięga dawnej EXP-052/SEM-011: model ma dwa osobne ograniczenia, ale nie ma ich jawnego połączenia ani osobnej pary DEP-NEW-001. Wcześniejsze decyzje zaakceptowały lokalne klauzule, pozostawiając ocenę wystarczalności tego połączenia otwartą.

**Rekomendacja3:** zachować zgodne komponenty, lecz zawiesić dwie pełne oceny SIT-16 do dawnej decyzji o połączeniu bramek. Nie liczyć części sukcesu i nie nadawać automatycznie FN za brak krawędzi. Nie wykazano tu błędnie wykonanego ruchu; nie rozstrzygnąłem starego wariantu za właściciela.

## 4. SIT-09 po kontekście — brak jawnego stanu obrońcy przy znanym wyjątku

Pierwszy zapis daje lokalne5→2 dla LC przeciw HI bez AS/innych modyfikatorów. Zakaz H&D przeciw SK jest zachowany w obu odpowiedziach mimo MA6<8.

Po kontekście R932 i dostarczony Step4 mówią dodatkowo, że redukcja nie działa, jeśli obrońca jest Routed; wskazują też LC użyte do determination. Zamrożone fakty SIT-09 nie wiążą jawnie tych warunków. Przy właściwym lokalnym atakującym LC i obrońcy non-Routed wynik jest2; przy Routed redukcja nie działa i pozostaje5 przy zadanym braku innych modyfikatorów. Nie wstawiłem domyślnie non-Routed.

Właściciel mógł zamierzać, że „no other modifiers” wyłącza również taki wyjątek, albo że test dotyczy wyłącznie operatora9.32. To możliwe odczytania zakresu, ale nie ustanawiam ich sam przez dopisanie brakującego faktu.

**Rekomendacja4:** zawiesić jedną pełną ocenę context/SIT-09 do decyzji o zakresie/faktach. Zachować zakaz H&D i lokalny operator; nie twierdzić, że kontekst pogorszył model lub że model podał złą liczbę. `eval-v1` pozostaje bez zmiany. Ewentualne doprecyzowanie powinno mieć osobny zapis właściciela i tę samą podstawę porównania obu odpowiedzi, bez ukrytej korekty gold. To pytanie SITREV-003, powiązane z nadal otwartą SEM-003.

## Co pozostaje do zamknięcia M-POC5

Wszystkie sytuacje są przejrzane. **Nowe40 ocen czeka na decyzję właściciela**:35 pozytywnych oraz2+2+1 opisane wyżej. Faktyczny odczyt plików przez właściciela unknown. Pełne wyniki trzech wystąpień są zawieszone mimo wykonanych porównań; nie zostały usunięte z mianownika.

Starsze8 oczekiwań i13 kwestii pozostają otwarte; wcześniejsze ograniczone dyspozycje SEM-014–022 i414 decyzji inwentarza zachowane. Akceptacja nowych wyników lokalnych nie akceptuje rzeczywistej mapy, scenariusza, tabel lub ratingów i nie domyka całych rekordów/grafu. Pełne TP/FP/FN/precision/recall i ocena jakości nadal nieocenialne. Czas aktywny, konfiguracja, tokeny, cena i zgodność budżetu unknown.

M-POC5 nie jest jeszcze formalnie zakończony. Pozostają decyzje o tym pakiecie i świadome rozliczenie starszych nierozstrzygnięć oraz ograniczeń. M-POC6/7 i korekt nie uruchomiono.

[Pełne porównania40 ocen](comparisons.md) · [Oryginalne pola, źródła i bajty](results.json) · [Zestawy decyzji](presentation.json).
