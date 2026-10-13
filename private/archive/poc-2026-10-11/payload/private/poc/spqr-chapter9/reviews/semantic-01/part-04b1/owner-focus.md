# M-POC5A.4b1 — pakiet decyzji właściciela

Przejrzałem wszystkie 65 przypisanych ID: 60 relacji pierwszej odpowiedzi i 65 odpowiedzi po kontekście. Osobno porównałem w obu odpowiedziach 5 jawnych i 3 niejawne pary wykonawcze, 7 wzmianek i 7 kontynuacji z zamrożonej oceny. To rzeczywiste porównania tekstu obu końców i zapisów modelu, z oględzinami dostarczonych stron 31–37 oraz wyłącznie dostarczonego wycinka Step 4. Wszystkie poniższe oceny są propozycjami Codex; nie zapisuję akceptacji w imieniu właściciela.

[Czytelne porównania każdego ID](comparisons.md) i [pełne ślady JSON](comparisons.json) zawierają osobne wyniki dla obu hashów, źródła, dokładne zakresy, rekordy i pola surowej odpowiedzi, pointers oraz bajty [start,end). Nie zakładam, że właściciel już otworzył lub przeczytał pliki.

## Pozytywny zakres do przyjęcia

Proponuję przyjąć **60 ID / 116 wystąpień**, wyłącznie w opisanych dla nich zakresach relacji lub roli odniesienia: 56 w first-001 i 60 w context-01. Nie oznacza to 60 poprawnych całych rekordów. Akceptacja nie obejmuje blankietowego `impact_if_missing=false` dla koniecznych dostępnych celów, pełnych wyników, nieprzejrzanych pól lub wcześniejszych nierozstrzygnięć. Pięć pozostałych ID / 9 wystąpień wydzielam poniżej do osobnej decyzji.

Najważniejsze zgodne powiązania mają praktyczne znaczenie:

- **Pass-Thru słonia:** instrukcja pozwala na umieszczenie słonia za obrońcą po Shock tylko wtedy, gdy piechota nie uciekła, a słoń nie rozpoczął Rampage. Model łączy sprawdzenie Rampage z 9.14 i zachowuje wolny Rear, wybór gracza oraz facing. Osobny wyjątek dla SK dotyczy wyłącznie końcowego testu Pass-Thru w kroku 4; model zachowuje to zawężenie. Proponuję przyjąć oba powiązania, bez rozszerzenia wyjątku SK na całą procedurę.
- **Double Depth i obrona falangi:** 9.53 odsyła do 9.41. Model zachowuje warunki celu: atak musi nastąpić z ruchu przez Front, potrzebne jest wsparcie flank, HI zmniejsza shift, a atak bez ruchu, przez Flank/Rear lub z jakąkolwiek atakującą PH jest wyłączony. Proponuję przyjąć warunkowe korzystanie z obrony falangi. To nie automatyczny shift 4L i nie pełny odczyt CRT.
- **Scorpio strzela bez rozkazu:** model właściwie odsyła do limitu dwóch strzałów w Game Turn i jednego w przyjaznej Orders Phase. Jednocześnie zachowuje Fire mode oraz zakaz strzału w fazie przełączenia do Fire. Proponuję przyjąć te powiązania i rolę stanów Once/Finished, bez akceptacji całego strzału lub ratingów żetonu. Dla Reaction Fire obraz pokazuje Once; Finished jest określone w prozie.
- **Korzystanie z przykładów i diagramów:** model zazwyczaj poprawnie odróżnia ilustrację od instrukcji wykonania. Przykład Rampage nie zastępuje compass na mapie wybranej bitwy, a diagram MLE pokazuje rozstawienie i facing, nie uniwersalne ratingi Roman units. Proponuję przyjąć te role odniesień, bez małych wartości grafik.
- **Kontynuacje:** wszystkie siedem par zachowuje fizyczny porządek tekstu. Szczególnie ważne są dokończenia warunku pojedynczej przerwy w linii, warunków MLE oraz zdania, że CH+LI jest pojedynczą jednostką *dla stacking*. Proponuję przyjąć porządek fragmentów; to nie siedem dodatkowych zależności wykonawczych ani punktów reguł.

Dokładna pozytywna lista:

`D1011descriptor, D911914, D911rout, D912MRRCdef, D913screen, D914diagram, D914rout, D914table, D918specific, D919chartdef, D919clashdef, D922HD, D923ex, D924911, D924ex, D924rout, D931922, D932ex, D941ex, D951elig, D952951, D952column, D952reverse, D952wheel, D953941, D953elig, D953rout, D953scenario, D962shock, D966diag, D967ex, D968966, D971app, D972app, D982985, D985982, D985markers, D986982, D986marker, D986react, D987rout, D991OW, D991PAW, D991column, D993rout, D994rout, D996def, D996fire, D996ratings, DCTX846S4-1013, DCTX846S4-845, DCTX846S4-CRT, DCTX932-S4, Dcont-R911, Dcont-R914, Dcont-R924, Dcont-R966, Dcont-R991, Dcont-R996b, Dcont-table914`.

Pięć `DCTX...` powstało dopiero po kontekście; w pierwszym wyniku nie oceniam ich nieobecności jako FN. Z czterech pozytywnych nowych ID trzy opisują potrzebę celu i zachowaną blokadę, a jedno wąskie powiązanie kwalifikacji LC. Nowość nie nadaje TP.

## Alokacja Hits: dostępny cel nie oznacza końca blokady

**Co mówi instrukcja:** 9.62 każe rozdzielić Shock Hits według 10.13. Ta reguła dzieli Hits pomiędzy jednostki/stosy, ustala pierwszeństwo nadwyżki i dwa wyjątki. Dopiero potem odsyła rozdział wewnątrz stosu do 6.68 bullet #6. Tego ostatniego źródła nie dostarczono.

**Co zapisał model:** oba wyniki mają poprawne `R962→N1013`, ale relacja `D9621013` ma `blocks_full_result=false` i pustą listę gapów. W samym N1013 model opisuje brak dalszego rozdziału; osobny G-D1013stack ma blokadę. Po kontekście nowa relacja Step 4→10.13 ma już `blocks_full_result=true`.

**Różnica i skutek:** połączenie z właściwym tekstem jest poprawne, ale deklaracje blokady są rozłożone nierówno. Konsument czytający wyłącznie `D9621013` może uznać alokację za zamkniętą. Nie wykazano konkretnego błędnego rozdziału Hits; wykazano rozbieżność między deklaracją relacji a brakującą częścią celu.

**Propozycja SEM-014:** przyjąć poprawną tożsamość, kierunek i użycie 10.13, a wystarczalność deklaracji blokady pozostawić do osobnej decyzji. Ogólne uzasadnienie „cel jest dostarczony” opisuje dostępność; nie odpowiada na pytanie, co zablokowałby brak koniecznego celu. Dlatego analogicznego blankietowego `false` nie włączam do pozytywnej akceptacji pozostałych dostępnych relacji wykonawczych.

Znana ścieżka R962→Step 4→10.13→brakujące 6.68 #6 ma trzy krawędzie. Nie pozyskano trzeciego źródła; rozszerzanie zatrzymano na granicy dwóch. Przyjęcie poprawnego endpointu po kontekście nie zamyka alokacji. Zadane sumaryczne Hits mogą wystarczać do lokalnego operatora, lecz nie zastępują nieznanej reguły podziału wewnątrz stosu.

## SK: komu zmniejszamy Hits

**Co mówi instrukcja:** 9.23 mówi o Hits zadanych przez SK: połowa, w dół, najwyżej 1. SK nie może Shock attack. Dostarczony Step 4 mówi natomiast: gdy obrońcą jest SK, zmniejszamy Hits atakującego tą samą operacją.

**Co zapisał model:** po kontekście dodano `R923→NCTX846S4` jako niejawne `procedure_use`. Model wskazuje stronę atakującą oraz zachowuje faktor, zaokrąglenie i limit. Nadal blokuje pełny wynik przez brak tabeli i ustalenia uczestników.

**Różnica i skutek:** lokalne sformułowania są zgodne, kiedy wybranym obrońcą jest SK. Nie wolno z samej obecności SK zastosować bullet #3 do obrony mieszanej, w której 9.23 każe wybrać inny Type i pominąć Size SK. Przy zadanych Hits i właściwym zakresie lokalna operacja nie potrzebuje nowego lookupu całej walki.

**Propozycja dla wcześniejszego SEM-004:** uznać, że dostarczony fragment wspiera stronę, połowę, zaokrąglenie i cap. Pozostawić właścicielowi rodzaj i konieczność nowej relacji jako całej propozycji. To dodatkowy dowód; nie zamykam wcześniejszego pending, nie nadaję TP/FP i nie akceptuję całej walki.

## LC: przykład nie ustala kolejności AS i połowy

9.32 lokalnie podaje połowę Hits zadanych przez atakującą LC wskazanym klasom piechoty. Przykład mówi o użyciu drukowanego wyniku przy AS. Po kontekście źródło dostarcza 2× wyniku obrońcy przy AS, warunkowe pół/floor dla wybranego atakującego LC, wyjątek Routed oraz kumulatywność.

Model zachowuje te składniki i nadal oznacza kolejność połączonych operacji jako unknown. Proponuję przyjąć wąskie powiązanie do tego fragmentu (`DCTX932-S4`) i rolę przykładu (`D932ex`), bez decyzji o całym nowym polu exceptions R932, bez algebraicznego „skasowania” faktorów i bez domknięcia SEM-003. Wcześniejsza akceptacja lokalnego pół/floor nie przenosi się na nowy wyjątek lub pełny wynik.

## Brakujące połączenia krytyczne: rekord a treść

- **Triarii — DEP-NEW-001:** instrukcja zachowuje dwie bramki dla ruchu z Shock. 9.71 ma alternatywy związane z odległością/LOS, 9.72 próg RP ≥ floor(AWL/2). Zawsze pozostaje stationary Shock przeciw przeciwnikowi we własnej ZOC. Model przechowuje obie bramki osobno, lecz nie zapisuje R972→R971 ani jawnej koniunkcji. Proponuję zachować brak rekordu i pozostawić ocenę kompletności połączenia w EXP-052/SEM-011 otwartą. Niczego nie dopisuję za ekstraktora.
- **Leader Elephant — DEP-NEW-002:** osobnego wyjątku z wiersza subsequent 7–9 do zakazu rally brak. Jednak wyjątek jest w tabeli i w `R914.exceptions`: natychmiastowy rally przy Hits = TQ−2. Proponuję przyjąć obserwację „brak osobnego rekordu, wyjątek zachowany w prozie”; brak rekordu nie dowodzi utraty znaczenia. Pierwszy 7–9 pozostaje innym zakresem.
- **Scorpio i Rampage — DEP-NEW-003:** osobnego R986→R914 brak. R914 zachowuje zakaz Reaction Fire dowolnego rodzaju, a R986 szerokie pozwolenie na special fire podczas ruchu. Tekst „any” nie uchyla zakazu dla Rampage. Proponuję zachować brak rekordu oraz osobno obecne klauzule, bez automatycznego FN i bez twierdzenia o faktycznie wykonanym błędnym strzale. Akceptacja trybu Scorpio nie zamyka tego połączenia.

## Wzmianki: nazwa w prozie a osobna krawędź

Cztery osobne wzmianki nadal są pominięte: z przykładów SK i LC do Table/CRT, z caption Rampage do compass wybranej bitwy oraz z 9.66 do alternatywy OW (`DEP-034/035/043/067-1`). Model zachowuje te odniesienia w treści odpowiednich rekordów. Relacja od reguły do przykładu nie zastępuje relacji od przykładu do tabeli; odwołanie OW w 9.67 nie zastępuje wystąpienia w 9.66. Proponuję zachować cztery braki strukturalne oraz obecność treści w prozie, bez semantycznego FN i bez rozstrzygania zewnętrznych aliasów.

**SEM-015 / D961stack:** źródło mówi „See the Stacking Charts for a summary”. Zamrożony zakres uznaje to wystąpienie za wzmiankę. Model zapisał `table_use` i blokadę pełnego wyniku. Proponuję uznać różnicę rodzaju względem DEP-037; sama potrzeba chart dla innych pytań o stacking nie zmienia roli tego zdania. Kierunek i nazwa kandydata są zachowane. Nie przyznawać pełnego TP za tę zamrożoną wzmiankę. To wymagane dodatkowe porównanie; pozostała partia .4b3 nie została wykonana.

## Trzy granice typowania do decyzji

**SEM-016:**

- `D9161011`: 9.16 potrzebuje pojęcia/testu TQ; cel 10.11 opisuje również procedurę. Model użył `definition`. Proponuję osobno przyjąć trafny cel i rozstrzygnąć, czy wystarczy rodzaj definicji, czy potrzebne jest `procedure_use`. Nie zamyka to lokalnej gałęzi DR≤TQ w EXP-017 ani błędu lokatora E916.
- `D967966`: model właściwie kieruje reakcję MLE do operacji MLE i zachowuje jej warunki, ale oznacza relację jako niejawną. Nazwa operacji jest podana wprost, choć numer 9.66 nie występuje. Proponuję rozstrzygnąć klasyfikację named use, bez uznania etykiety za poprawną z samej obecności celu.
- `D968column`: „jednostki w Column nie mogą MLE” opisuje niedopuszczalny stan jednostki. Model ma `mention`; możliwy jest `condition`. Proponuję decyzję o rodzaju w tym dokładnym zakresie, bez zmiany znanego lokalnego zakazu lub automatycznego przeniesienia tego problemu na wszystkie zakazy manewrów.

## Czego ten pakiet nie zamyka

Brak nowych decyzji właściciela: **125 wystąpień porównanych przez Codex, 125 udostępnionych w pakiecie, 0 nowych ocenionych przez właściciela, 125 pending**. Faktyczne otwarcie/odczyt jest unknown. Dodatkowe 22 pary na wynik mają osobne ślady; nakładają się na przypisane relacje i nie zwiększają liczby unikalnych propozycji.

Wcześniejsze po 63 lokalne zakresy i 3 wymagania źródła na wynik pozostają przyjęte tylko w dawnych zakresach. Osiem oczekiwań EXP-010/017/019/040/050/052/066/074 i SEM-001–013 pozostaje otwartych. W tym pakiecie dodano propozycje SEM-014–016. Dodatkowe poprawne propozycje spoza gold nie zwiększają mianownika recall; 105 candidates nie staje się gold. Pełne TP_gold/TP_output/FP/FN/precision/recall nadal `not_assessable`.

Pozostałe 132 wystąpienia relacji mają jawne przypisanie: .4b2 60, .4b3 72. Lokatory, E916 i 64 granice glifów, reszta inwentarza, ratingi/setup i 20 sytuacji wymagają osobnych części. M-POC5A/.4/.4b pozostają partial; M-POC5 jest jedynym next.

Bez nowego źródła, ekstrakcji lub korekty: nadal 1 dodatkowa strona / 1 reguła / 0 tabel, 1 runda kontekstu / 0 korekt, 0 pełnych domknięć luk, 4 częściowe uzupełnienia i 4 nowe deklaracje. Trzeciego źródła nie pozyskano. Listing/path discovery poza allowlistą w context-01 potwierdzono niezależnie; nie zaobserwowano odczytu treści oceny. Ekspozycja/czysty kontekst, aktywny czas, selektory, tokeny, cena i zgodność budżetu pozostają unknown. Czas kalendarzowy tej sesji nie dowodzi aktywnego budżetu.

Dokładny następny krok: decyzja właściciela o pozytywnym zakresie tego pakietu, osobno o SEM-004/014/015/016 i wszystkich wcześniejszych pending. Ewentualne akceptacje zapisać jako nowy owner-decision. Następnie osobna .4b2 według istniejącej listy, z oszacowaniem zakresu przed wykonaniem.
