# M-POC5A.4b3 — decyzje właściciela po przeglądzie

Przejrzałem wszystkie przypisane 36 relacji w obu odpowiedziach: 72 wystąpienia.
Porównałem klauzule instrukcji, zapisane relacje, ich źródłowe rekordy i luki.
Obie odpowiedzi mają tutaj identyczne krawędzie i przypisane im luki, ale każda
ma osobny ślad do swoich oryginalnych bajtów. Nie powstała nowa ekstrakcja lub korekta.

Rekomenduję trzy decyzje poniżej. Są propozycjami; wcześniejsze zatwierdzenie
dotyczyło poprzedniego pakietu, a „kontynuuj” uruchomiło ten przegląd.
Wcześniejsze nierozstrzygnięcia pozostają otwarte.

## 1. Przyjąć 68 ograniczonych ocen relacji i wymagań źródła

To 34 relacje w każdej odpowiedzi. Instrukcja rzeczywiście korzysta z nazwanych
procedur, tabel, definicji lub danych scenariusza. Model zachowuje kierunek od
korzystającej klauzuli do potrzebnego celu. Brakujące cele nie zostały dostarczone
w całości; akceptacja obejmowałaby potrzebę celu i rolę relacji w opisanym zakresie,
nie treść tych celów lub poprawność całego rekordu.

Najważniejsze wyniki:

- **Falanga i rzymskie stosy.** Rozkazy bezpośrednio od OC, PAW, wspólny heks
  ataku i warunek jednej linii mają rzeczywiste oparcie w tekście. Pełna legalność
  ruchu wymaga brakujących zasad rozkazów, wyboru celu albo definicji linii.
  Lokalnie znamy już odbiorców modyfikatorów, wymóg tego samego heksu czy zastosowanie
  automatycznych Hits do każdej jednostki. Automatyczne Hits z6.68 to osobna
  zależność od podziału Shock Hits przez10.13; wcześniejsza otwarta alokacja nie znika.
- **Triarii.** LOS jest potrzebne do pierwszej alternatywy9.71; druga alternatywa
  odległościowa ma własne warunki. W9.72 potrzebujemy AWL i RP, aby ocenić rzeczywisty
  próg. Przy zadanych wartościach połowa z zaokrągleniem w dół jest znana. Wyjątek
  ataku bez ruchu na przeciwnika we własnym ZOC pozostaje czytelny. Ta decyzja nie
  rozstrzyga wcześniejszego pytania o połączenie obu bramek Triarii.
- **Scorpio i barbarzyńcy.** Limit jednego Scorpio, eliminacja routującego Scorpio,
  jeden odzyskany Hit na rozkaz BI i modyfikatory Ferocity/Momentum są podane
  lokalnie. Brak ogólnej procedury blokuje jej wykonanie, nie odczytanie tych
  ograniczeń. Dostarczone10.11 opisuje część ogólnego testu TQ; nadal nie mamy tabeli
  wszystkich momentów i wyników, ani pełnej procedury Recovery.
- **Galijskie rydwany.** Instrukcja wprost kieruje do Movement Cost Chart i wiersza
  Mounted Javelin w MRRC. Samotny CH nie może wykonać OW; przewożenie eligible LI
  jest warunkiem koniecznym, lecz nie daje samo w sobie prawa do każdego OW.
  Nie dopowiadam, które LI są eligible ani gdzie znajdują się ich kryteria.
- **Dwa lokalne wyłączenia są nieblokujące.** Mounted LI nie stosuje Missile Supply,
  a po wejściu na CH usuwa Low/No. Transportowe CH mają ignorować wpisy Chariot
  w Combat Tables. Model ma tutaj blocks=false i to pasuje do samych tych dyspozycji.
  Nie oznacza pełnej gotowości strzału, znajomości tabel lub stanu supply po zejściu.

**Proponowana decyzja:** przyjąć te68 ocen wyłącznie w zakresach opisanych osobno
w comparisons. Zapis `definition` dla AWL/RP oznacza potrzebę znaczenia i wartości
nazwanego parametru; nie poświadcza definicji lub realnych danych scenariusza.
Nie akceptować bezwarunkowej blokady lokalnych operatorów przy zadanych faktach.

Dokładne ID tego zestawu: D-ZOC-R966, D-ZOC-R972, D-ZOC-R995, D951OC, D952PAW,
D953pre, D95scenario, D961line, D962auto, D962target, D963TQ, D964order,
D966line, D967OW, D968LC, D971LOS, D972AWL, D972RP, D983stack, D987recovery,
D993depleted, D993recovery, D994pre, D994scenario, D995momentum, D995scenario,
D996HD, D996MRRC, D996OW, D996eligible, D996movement, D996stack, D996supply,
D996tables — osobno dla first-001 i context-01.

## 2. Koszt terenu jest jawny; wskazanie konkretnej tabeli jest wnioskowane

**Instrukcja:** przy formowaniu Double-Depth tylna PH płaci zwykły koszt terenu
i dodatkowo1 MP. W tym zdaniu nie ma nazwy Movement Cost Chart.

**Model:** D951terrain ma `table_use/explicit`. Jako dosłowne odniesienie zapisuje
„normal terrain costs”, a dopiero w opisie potrzebnego kontekstu wskazuje tabelę.

**Różnica i skutek:** potrzeba bazowego kosztu jest rzeczywista i jawna. Nie ma
jednak źródłowego dowodu jawnego odesłania w9.51 do tej konkretnej tabeli.
To odmienna sytuacja od9.96, gdzie Movement Cost Chart jest wymieniona wprost.
Zadany poprawny koszt pozwala dodać1, choć nie znamy rzeczywistych kosztów terenu.

**Proponowana decyzja SEM-018:** przyjąć wymaganie zwykłego kosztu i kierunek
relacji. Nie przyjmować `table_use/explicit` jako dosłownego odesłania do chart;
potrzebę tabeli traktować najwyżej jako wnioskowaną. Nie wskazujemy jej treści,
aliasu lub kosztu konkretnego heksu. Dwa wystąpienia, po jednym w każdej odpowiedzi.
To ocena istniejącego zapisu, bez poprawiania odpowiedzi lub dopisywania relacji.

## 3. Podsumowanie stosów nie jest obowiązkową procedurą wykonawczą

**Instrukcja:** odsyła do Stacking Charts po podsumowanie, następnie podaje zasadę
orientacyjną dla dwóch rzymskich jednostek i zaznacza wyjątki, np.Velites.

**Model:** D961stack i jego luka mają szerokie `blocks=true` dla niedostarczonego
podsumowania i wyjątków. Sam rodzaj relacji został już rozstrzygnięty przez
właściciela jako `mention` w SEM-015; ta decyzja pozostaje bez zmiany.

**Różnica i skutek:** z odesłania po podsumowanie nie wynika obowiązek konsultacji
chart przy każdym lokalnym odczycie9.61. Jednocześnie zasada orientacyjna z niewymienionymi
wyjątkami nie wystarcza do zatwierdzenia legalności każdego rzeczywistego stosu.

**Proponowana decyzja SEM-019:** nie uznać brakującego summary za obowiązkowy lookup
blokujący lokalne zdania. Zachować brak treści podsumowania oraz warunkową blokadę
pełnej legalności tam, gdzie potrzebne są nieznane wyjątki lub ogólne zasady.
To tylko decyzja o wcześniej wyłączonych necessity/impact, dwa wystąpienia.
Nie pytamy ponownie o `mention`, nie akceptujemy chart, aliasów ani dowolnego
stackingu Velites.

## Zakres akceptacji i dalszy krok

[Wszystkie porównania](comparisons.md) oraz [pełne ślady JSON](comparisons.json)
zawierają źródła, dokładne zakresy, recenzenta, pointers, hashe i surowe bajty.
Pakiet udostępnia72 nowe oceny; oceniający porównał72; nowych decyzji właściciela0;
pending72. Faktyczne otwarcie/odczyt plików przez właściciela pozostaje unknown.
Wcześniejsze dwa komponenty kindD961stack są już rozstrzygnięte i nie są nowe.

Łącznie porównano wszystkie257 przypisanych wystąpień trzech partii .4b.
185 wcześniejszych zakresów ma decyzje właściciela. Nie są to257 poprawne całe
rekordy lub TP. Nie rozszerzam gold, ocen dawnych komponentów ani zakresu zgody.
Osiem wcześniejszych oczekiwań iSEM-001–013 w pozostałych zakresach pozostaje otwarte;
ograniczone decyzjeSEM-014–017 zachowane. Pełne metryki, realne setupy, wartości
żetonów/tabel, lokatory i20 sytuacji bez akceptacji.

Po decyzji dla tego pakietu następna jest osobna .4c: lokatory i granice glifów,
z własnym oszacowaniem i ewentualnym podziałem przed pracą. M-POC5A/.4/.4b pozostają
partial; M-POC5 jedyny next. Bez nowych źródeł, ekstrakcji, korekt i publikacji Git.
