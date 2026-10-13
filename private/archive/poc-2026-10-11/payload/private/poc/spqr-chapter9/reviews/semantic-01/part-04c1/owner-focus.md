# M-POC5A.4c1 — lokatory: co działa, co jest przycięte

Wykonałem pierwszą część przeglądu:22 lokatory ze stron31–33, osobno44
wystąpienia obu odpowiedzi. Nie poprawiłem prostokątów, cytatów lub odpowiedzi.
Przed pracą podzieliłem całą .4c na44/42/38 wystąpień; pozostałe80 zachowuje
dokładny przydział i nie jest jeszcze przejrzane.

Twoje „ok kontynuuj” po trzech rekomendacjach .4b3 zapisałem jako ich
zatwierdzenie:68 ograniczonych ocen i2+2 ocen szczególnych. Nowe
owner-decision-07/overlay-07 zachowują poprzednie decyzje; łącznie257
przypisanych wystąpień relacji ma decyzje o przedstawionych komponentach.
Wcześniejsze nierozstrzygnięcia pozostają otwarte. Zgoda nie obejmuje
nowych wyników lokatorów opisanych tutaj.

## Prawidłowe współrzędne nie wystarczają do pełnego cytatu

W każdym z22ID zgadza się hash i rozmiar obrazu, prostokąt mieści się
na stronie i wskazuje właściwą część źródła. Cytat znajduje się na pełnej
dostarczonej stronie oraz w niezależnym helperze. Dla obu odpowiedzi
cytat i pole image są identyczne, choć ślady do surowych bajtów są osobne.

Wszystkie22ID przekraczają jednak co najmniej jedną granicę pełnej
obwiedni znaku. Obwiednia PDF obejmuje również miejsce, w którym znak
nie ma widocznego tuszu. Dlatego samo jej przekroczenie nie zawsze
oznacza uciętą, nieczytelną literę. Nie powiększyłem ramki ani nie dodałem
tolerancji, aby uzyskać zaliczenie tego ścisłego kryterium.

**Rekomendacja1:** przyjąć poprawność wskazania źródła i geometrii jako
osobne komponenty44 ocen. Jednocześnie zachować wynik **0/44** dla
ścisłego zawarcia całych obwiedni glifów. Nie uznawać tego za44 błędy
odczytu reguł lub44 poprawne całe rekordy.

## 38 wystąpień: krótki cytat czytelny, obwiednia naruszona

W19ID obraz zawiera czytelny krótki cytat bez zaobserwowanego ucięcia
jego tuszu. Najczęściej prawa granica przecina jedynie skraj obwiedni
końcowego znaku. Przykładowo w E911a końcowe „h” wychodzi obwiednią
o0.018 punktu PDF; na powiększeniu tusz pozostaje wewnątrz ramki.
W E914diagram dolna obwiednia podpisu wykracza o1.1786 punktu,
ale cytowane litery nadal są widoczne.

**Rekomendacja2:** przyjąć wyłącznie czytelność tych38 krótkich cytatów
na dostarczonym rastrze, z zachowaniem ograniczenia obwiedni.
To nie akceptacja całego obszaru, całej klauzuli, diagramu, wartości
żetonu lub znaczenia całej reguły. Niektóre cytaty są od początku
fragmentami zdań; nie dopisujemy im brakujących końcówek.

Dokładne ID, po dwa wystąpienia: E911a, E912, E913, E914start,
E914priority, E914diagram, E914move, E914end, E915, E918, E919,
E921, E922, E923, E923ex, E92, E871, E874, E875.

## 6 wystąpień: obraz dowodu rzeczywiście niepełny

**E914cont i E873, razem4 wystąpienia:** dolna krawędź ucina wystające
części liter, np.„p”, „g”, „j”. Potwierdzają to dokładne nieposzerzone
wycinki i powiększenia krawędzi. Tekst pozostaje czytelny, a pełna strona
potwierdza jego treść, ale taki crop nie zawiera całych cytowanych znaków.
Obwiednie wystają odpowiednio2.2036 i2.997 punktu PDF.

**E916, razem2 wystąpienia:** wada jest większa. Cytat brzmi
„This rule does not apply to Leader Elephants.”. Wskazana ramka kończy
się na „This rule does not”; linia „apply to Leader Elephants.” pozostaje
poza nią. Dolna granica ramki ma360 punktów, koniec obwiedni cytatu
371.147 punktu — różnica około31 pikseli w dostarczonym obrazie.
Nie można zaliczyć tej ramki jako pełnego obrazowego dowodu wyjątku.

Model zapisał ten wyjątek w cytacie i rekordzie reguły, a pełna strona
go zawiera. Zatem potwierdzenie wady E916 nie oznacza automatycznie,
że model pominął wyjątek lub błędnie go odczytał. Pytanie o wynik testu
przyDR≤TQ w SEM-001/EXP-017 pozostaje osobną, wcześniejszą sprawą.

**Rekomendacja3:** przyjąć ustalenie niepełnego obrazu dowodu dla tych6
wystąpień:4 z uciętymi dolnymi częściami liter i2 z brakującą linią
wyjątku. Zachować oryginalne lokatory i wcześniejsze raporty. Nie
nadawać przez to automatycznych semantycznychFP/FN lub błędu odczytu.

[Porównanie E916: dokładny crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/E916-exact.png)
oraz [referencja pokazująca tekst poza ramką](../../../measurement/M-POC5A-semantic-04c1/visual-02/E916-quote-reference.png).
Referencja służy oględzinom; nie zastępuje oryginalnego dowodu.

## Zakres decyzji i dalszy krok

[Każdy lokator osobno](comparisons.md) oraz [pełne śladyJSON](comparisons.json)
zawierają źródłowe zakresy, geometrię, naruszone glify, oryginalne pola,
pointers, hashe i bajty obu odpowiedzi. Oceniający przejrzał44 wystąpienia;
udostępniono44; nowych decyzji właściciela0; pending44. Faktyczne
otwarcie/odczyt plików przez właściciela pozostaje unknown.

SEM-005 ma propozycję potwierdzenia konkretnej wadyE916. SEM-007 ma
ocenę tylko tej części granic glifów; pozostałe80 wystąpień nadal
niewykonane. Wcześniejsze8 oczekiwań, inne zakresySEM-001–013,
wyłączone pola i brakujące źródła pozostają otwarte. Brak zmian w gold,
metrykach i limitach kontekstu/korekt. Nie wykonano sytuacjiM-POC5B.

Po decyzji obecnego pakietu następna osobna .4c2:21ID/42 wystąpienia
ze stron34–35, po własnym oszacowaniu. M-POC5A/.4/.4b/.4c nadalpartial;
M-POC5 jedynynext.
