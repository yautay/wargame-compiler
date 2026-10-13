# M-POC5A.4c2 — druga część lokatorów

Przejrzałem wszystkie21 przypisanych lokatorów ze stron34–35, osobno42
wystąpienia obu odpowiedzi. Sprawdziłem cytat, wskazany obraz, dokładną
ramkę, obwiednie znaków i czytelność rastra. Nie poprawiłem odpowiedzi,
cytatów lub ramki. To nowe propozycje do oceny właściciela.

Twoje „zatwierdzam i kontynuuj” zapisałem jako zgodę na pokazane44
oceny .4c1. Owner-decision-08/overlay-08 zachowują38 czytelnych krótkich
cytatów,4 przycięcia dolnych części liter i2 przypadki brakującej liniiE916.
To44 decyzje o komponentach, nie44 dobre lokatory lub poprawne całe reguły.
Potwierdzenie wadyE916 nie naprawia jej ani nie rozstrzyga innych pytań
o znaczenie9.16. Wcześniejsze nierozstrzygnięcia pozostają otwarte.

## 1. Wszystkie42 krótkie cytaty są czytelne na wskazanym rastrze

W obu odpowiedziach każde21ID ma taki sam cytat i obraz/ramkę.
Każde wystąpienie ma osobny ślad do swoich oryginalnych bajtów.
Zgadza się hash obrazu, jego rozmiar i układ współrzędnych; ramki
mieszczą się na właściwych stronach. Krótkie cytaty znajdują się w
dostarczonym źródle i helperze.

W odróżnieniu od przyciętych wycinków z poprzedniej części tutaj nie
zaobserwowałem utraty tuszu cytowanych liter. Na dokładnych wycinkach
widać m.in.4MA zamiast5MA, osobny test każdej jednostki zTQ górnej,
dowolną liczbę vertices przy zmianie facing oraz stationary Shock
Triarii. Drobne graniczne litery obejrzałem również w powiększeniu.

**Rekomendacja1:** przyjąć poprawne wskazanie źródła/geometrię oraz
czytelność42 krótkich cytatów, w dokładnych zakresach opisanych w
comparisons. Nie rozszerzać tego na całą regułę lub pozostałą zawartość
dużego cropu, tabelę, wartości żetonu czy geometrię rzeczywistej gry.
Przykład AS/LC wE932ex i wyjątek stationary Shock wE972 nie otrzymują
przez tę ocenę nowego rozstrzygnięcia dawnych pytań semantycznych.

Dokładne ID, po dwa wystąpienia: E924cont, E924ex, E931, E932ex,
E941, E941ex, E951, E952, E962, E963, E964, E965, E966a, E966b,
E967, E968, E97intro, E972, E95, E96, E97.

## 2. Dla40 wystąpień pełna obwiednia glifu wykracza poza ramkę

W20ID odnotowano różnicę granicy obwiedni większą niż sam ślad
reprezentacji zmiennoprzecinkowej. Raster pozostaje czytelny, ponieważ
obwiednia fontu zawiera także przestrzeń bez widocznego tuszu.

Przykładowo A w5MA wE952 ma obwiednię wychodzącą w prawo o0.551pt;
w powiększeniu tusz litery zostaje przed ramką. W nagłówkachE95/E96
dolna obwiednia wystaje2.811pt, ale litery nadal są całe i czytelne.
Dokończenie zdania wE924cont jest czytelne mimo dolnego marginesu
obwiedni1.0036pt. Żaden z tych faktów nie poświadcza całych obwiedni.

**Rekomendacja2:** zachować40 ścisłych naruszeń obwiedni jako osobne
ograniczenie dowodu. Nie zamieniać ich automatycznie w widoczne ucięcie
litery, błędny odczyt lub semantyczneFP/FN. Nie poszerzać prostokąta
i nie dodawać tolerancji, aby otrzymać wynik „pass”. Zestaw obejmuje
wszystkie ID powyżej z wyjątkiemE962.

## 3. E962: różnica liczbowa nie dowodzi fizycznego przycięcia

W obu wystąpieniachE962 cytat jest czytelny. Surowe porównanie pełnych
obwiedni zgłasza jako jedyny problem lewe „c” w„check”, z różnicą
**2.842170943040401×10⁻¹⁴ punktu PDF** względem granicy.
To poziom reprezentacji zmiennoprzecinkowej, o wiele mniejszy od piksela.
Nie zaobserwowałem ucięcia tego znaku w dokładnym cropie lub powiększeniu.

Nie przerobiłem wyniku skryptu: jego porównanie bez tolerancji nadal
zwraca false. Jednak ten wynik nie jest wystarczającym dowodem rzeczywistego
naruszenia geometrii. Dlatego rozdzielam obserwację liczbową od wniosku
o przyciętym glifie.

**Rekomendacja3:** przyjąć ograniczenie precyzji dla tych2 wystąpień,
bez stwierdzenia pewnego fizycznego clipping i bez automatycznego
ścisłego „pass”. Ścisłe rozstrzygnięcie pozostaje
`not_assessable_numeric_precision`; czytelność krótkiego rastra jest
oceniona pozytywnie. Dodatkowe różnice rzędu10⁻¹⁴ wE963/E964/E965
też oznaczono osobno, ale tam występują ponadto większe różnice obwiedni.

## Pokrycie, wyłączenia i następny krok

[Wszystkie porównania](comparisons.md) i [pełne śladyJSON](comparisons.json)
zawierają oryginalne pola, pointers/hash/bajty, źródłowe zakresy, geometrię,
obserwacje glifów, dokładne wycinki i notatkę dla każdegoID.

Porównano42, udostępniono42, nowych decyzji właściciela0, pending42.
Te trzy decyzje dotyczą różnych komponentów tych samych42 wystąpień;
nie sumujemy ich jako dodatkowych punktów. Faktyczny odczyt plików przez
właściciela pozostaje unknown. Łącznie porównano86 ze124 przypisanych
wystąpień lokatorów; poprzednie44 ma ocenę właściciela, następne38
jest przypisane do .4c3 i tutaj niewykonane.

SEM-007 pozostaje otwarty w reszcie zakresu. E916 i wcześniejsze wady
nie zostały naprawione. Osiem dawnych oczekiwań, szersze pola/aliasy,
pełne wyniki i inne nierozstrzygnięcia zachowano.257 komponentowych
decyzji relacji,264 pary rubryka/EXP, eval-v1/gold, limity kontekstu
i korekt bez zmiany. Nie wykonano sytuacjiM-POC5B.

Po decyzji dla .4c2 następna osobna .4c3:22ID/38 wystąpień, po własnym
oszacowaniu. Nadrzędne M-POC5A/.4/.4b/.4c nadalpartial; M-POC5 jedynynext.
