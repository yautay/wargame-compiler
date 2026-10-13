"""Manual semantic judgments after reading source passages, both answers and images.
No inferred semantic decision from hashes, schema validity or record equality.
"""

ANNOTATIONS = {}

def add(id, source, output, difference, impact, fields, result='bounded_content_supported', exclusions=None):
    ANNOTATIONS[id] = dict(source_says=source, model_says=output, difference=difference,
         impact=impact, selected_fields=fields, bounded_result=result,
         proposed_decision='accept_presented_bounded_judgment' if result!='mixed_operative_supported_explanation_omitted' else 'confirm_limited_textual_omission_and_retained_operative_content',
         local_exclusions=exclusions or [], reviewer='Codex in this evaluating session', human_reviewer=None,
         semantic_review_method='Manual source/field comparison, separately for both original answers; identical values allow same explanation with distinct original byte traces.')

# Each printed label was compared to its source location and both label fields.
for label,ptrs,topic in [
    ('9.81',['/rules/33'],'klasyfikacja Scorpio'),
    ('9.82',['/rules/34'],'tryby Fire/Move i rozkazy'),
    ('9.83',['/rules/36'],'limit Scorpio w heksie'),
    ('9.84',['/rules/37'],'brak facing'),
    ('9.85',['/rules/38'],'Active Fire'),
    ('9.86',['/rules/39'],'Reaction Fire'),
    ('9.87',['/rules/40'],'Hits i eliminacja Scorpio'),
    ('9.91',['/rules/41'],'Movement Effects BI, lewa→prawa kolumna'),
    ('9.93',['/rules/42'],'Rout and Recovery BI'),
    ('9.94',['/rules/43'],'Barbarian Ferocity'),
    ('9.95',['/rules/44'],'Barbarian Impetuosity'),
    ('9.96',['/rules/46','/rules/47','/rules/48','/rules/49'],'Gallic Chariots, kontynuacja do PDF37 przed 10.0')]:
    add('R-'+label, f'Wydrukowane oznaczenie {label} prowadzi temat: {topic}.',
        f'Oba wyniki mają original_label.value={label} we wskazanych rekordach.',
        'Numer zgodny; podział 9.96 na cztery rekordy nie tworzy czterech numerów reguł.',
        'Odnalezienie i tożsamość oznaczenia; bez przyjęcia treści całej reguły.',
        [p+'/original_label' for p in ptrs], 'bounded_label_supported',
        ['Cała treść mapped-parent, pełna procedura i literalna transkrypcja nagłówka poza numerem.'])

add('C-9.81-01',
    'Scorpio to silnik Bolt-firing (B) z wbudowaną załogą i TQ; jako LI przy ruchu i obronie w Shock/Missile Fire. Nie jest Shock-capable; ofensywnie tylko Missile Fire.',
    'R981 action_effect/interpretation zachowuje trzy aspekty; transcription cytuje dosłownie końcowy zakaz ofensywy Shock.',
    'Wybrany cytat nie jest całą transkrypcją; pozostałe cechy są w streszczeniu. Nie wykazano różnicy w wybranych znaczeniach.',
    'Zachowano granicę ofensywy/obrony i lokalną klasyfikację; wartości i pozycje ratingów nie wynikają z tej oceny.',
    ['/rules/33/transcription','/rules/33/action_effect','/rules/33/interpretation','/rules/33/unit_types'])
add('C-9.82-01',
    'Fire/Move są wzajemnie wyłączne. Zmiana wymaga Individual Order od dowolnego przyjaznego leadera. Po zmianie nie wolno wykonywać odpowiadającej czynności w tej Orders Phase; ruch w Move wymaga rozkazu, ogień nie.',
    'R982 podaje oba tryby, oba zakazy i obie blokady tej samej fazy; parameters zapisuje po jednym Individual Order, wyjątek dla ognia i time_limits.',
    'Nie pomylono zmiany trybu z prawem do natychmiastowego działania; conditions puste nie zastępuje warunków wpisanych w action_effect.',
    'Zachowano lokalne uprawnienia i terminy, bez wykonania całej procedury rozkazów lub oceny osobnej PLAY NOTE.',
    ['/rules/34/transcription','/rules/34/action_effect','/rules/34/interpretation','/rules/34/exceptions','/rules/34/parameters','/rules/34/time_limits'],
    exclusions=['Globalna poprawność established_absent w conditions; PLAY NOTE i fizyczne strony żetonu nie są tą klauzulą.'])
add('C-9.83-01',
    'Najwyżej jeden Scorpio w jednym heksie; wszystkie inne reguły stosów nadal obowiązują.',
    'R983 cytuje oba zdania i zapisuje limit 1 Scorpio/heks, pozostawiając lukę G-D983stack.',
    'Lokalny limit nie stał się zezwoleniem na dowolny stos; treść zgodna.',
    'Przyjęcie limitu i zastrzeżenia nie domyka pełnej legalności stosu.',
    ['/rules/36/transcription','/rules/36/action_effect','/rules/36/parameters','/rules/36/scope_limits'])
add('C-9.84-01',
    'Scorpio nie ma facing; ruch i ogień dowolnie kierunkowe bez zależności od obrotu żetonu. Wszystkie heksy traktowane jako Front.',
    'R984 zachowuje te trzy stwierdzenia; transcription dosłownie podaje wszystkie Front hexes.',
    'Bez różnicy w lokalnym braku facing i kwalifikacji Front.',
    'Nie wprowadzono kierunku broni z obrazka jako ograniczenia ognia; pełne zasięgi/LOS nie są ocenione.',
    ['/rules/37/transcription','/rules/37/action_effect','/rules/37/interpretation'])
add('C-9.85-01',
    'Do dwóch strzałów ofensywnych na Game Turn, najwyżej jeden na Orders Phase, w przyjaznym Movement and Missile Fire Segment bez rozkazu. Po pierwszym Once, po drugim Finished. Strzał blokuje inne czynności w tej fazie, w tym recovery.',
    'R985 zachowuje 2 shots/Game Turn, 1 shot/Orders Phase, właściwy segment, sekwencję markerów i zakaz innych działań. Fire mode w conditions ma podstawę w lokalnym 9.82.',
    'Nie pomylono tury z fazą; wybrany literalny cytat obejmuje tylko limit fazy, reszta to streszczenie z powiązanymi warunkami.',
    'Zachowano liczby, jednostki czasu i wyłączenie recovery. Ocena nie potwierdza całej procedury Missile Fire.',
    ['/rules/38/transcription','/rules/38/conditions','/rules/38/action_effect','/rules/38/parameters','/rules/38/time_limits'])
add('C-9.86-01',
    'Do dwóch strzałów na enemy Orders Phase, w enemy Movement and Missile Segment, również w trakcie ruchu. Once→Finished; zakaz każdego typu zwykłego Reaction Fire 8.2.',
    'R986 zapisuje ten limit/segment, ruch, markery i zakaz 8.2; Fire mode pochodzi z 9.82. G-D986react pozostaje luką.',
    'Szczególny ogień reakcyjny nie został utożsamiony ze zwykłym. Any movement w streszczeniu nie ustanawia wyjątku Rampage.',
    'Lokalny limit i zakaz zgodne; starsza brakująca osobna relacja do Rampage i pełne procedury pozostają otwarte.',
    ['/rules/39/transcription','/rules/39/conditions','/rules/39/action_effect','/rules/39/parameters','/rules/39/time_limits'],
    exclusions=['Brakująca osobna para DEP-NEW-003/SEM-006; pełna wykonalność i wyjątek Rampage nie otrzymują nowej decyzji.'])
add('C-9.87-01',
    'Scorpio otrzymuje/usuwa Cohesion Hits jak inne jednostki; jeśli routs, natychmiast eliminacja.',
    'R987 ma zwykłe Hits/recovery i natychmiastowe wyeliminowanie po Rout; cytat końcowego zdania zgodny.',
    'Nie zastąpiono eliminacji zwykłą ucieczką; bez nowej różnicy w klauzuli.',
    'Lokalny skutek zachowany; G-D987recovery nie daje pełnej procedury Recovery.',
    ['/rules/40/transcription','/rules/40/action_effect','/rules/40/time_limits'])

add('C-9.91-01','Nagłówek 9.91 Movement Effects wprowadza ruch BI.',
    'Numer 9.91 i temat ruchu BI są w R991; dosłowny tytuł nie jest osobnym polem.',
    'Zgodna rola nagłówka, nie literalna transkrypcja pełnego tytułu.',
    'Przyjęcie wyłącznie tożsamości/roli organizacyjnej.',
    ['/rules/41/original_label','/rules/41/action_effect','/rules/41/unit_types'],'bounded_heading_role_supported',
    ['Literalne odtworzenie tytułu i całe dalsze klauzule.'])
add('C-9.91-02',
    'BI nie ponosi Cohesion Hits za wejście/przekroczenie passable terrain ani zmianę facing w Rough. Następna kolumna kończy zdanie zakazem Column Movement 6.7, Pre-Arranged Withdrawal 6.8 i OW 6.5.',
    'R991 łączy oba fragmenty; transcription zachowuje Rough-facing i trzy zakazy, action_effect zachowuje oba zwolnienia; parameter 0 Cohesion Hits.',
    'Prawidłowa kolejność lewa→prawa kolumna. Zwolnienie Hits nie jest zwolnieniem MP ani prawem wejścia w impassable terrain.',
    'Lokalne negacje i zakres terenu zachowane; pełnych zewnętrznych procedur nie odtworzono.',
    ['/rules/41/transcription','/rules/41/action_effect','/rules/41/parameters'])
add('C-9.93-01','Nagłówek 9.93 Rout and Recovery wprowadza dwa skutki BI.',
    'R993 łączy numer 9.93 z Recovery i zastąpieniem Rout eliminacją.',
    'Rola obu tematów zachowana; pełny dosłowny tytuł nie jest osobnym polem.',
    'Tylko tożsamość/rola nagłówka, nie cała reguła.',
    ['/rules/42/original_label','/rules/42/action_effect'],'bounded_heading_role_supported',
    ['Literalna transkrypcja tytułu; dalsze klauzule mają własne oceny.'])
add('C-9.93-02','BI może usunąć tylko 1 Cohesion Hit na Recovery order.',
    'R993 transcription dokładnie cytuje to zdanie; parameter=1 Cohesion Hit per Recovery order.',
    'Limit i jednostka zgodne; nie przeniesiono limitu na turę.',
    'Znana lokalna ilość; G-D993recovery pozostawia procedurę/warunki Recovery poza oceną.',
    ['/rules/42/transcription','/rules/42/action_effect','/rules/42/parameters'],exclusions=['Druga klauzula Depleted BI w tym samym action_effect jest oceniona osobno.'])
add('C-9.93-03','Depleted BI nie wykonuje Rout, lecz jest eliminowana.',
    'W R993 action_effect/interpretation końcówka podaje Depleted BI eliminated instead of Rout; unit_types odróżnia Depleted.',
    'Lokalne zastąpienie Rout zachowane; transcription wybrało inną klauzulę, więc nie jest literalnym cytatem tego child.',
    'Nie przypisano eliminacji wszystkim BI; definicja rzeczywistego stanu Depleted nadal wymaga źródła.',
    ['/rules/42/action_effect','/rules/42/interpretation','/rules/42/unit_types'],exclusions=['Pierwsza klauzula limitu Recovery i pełna kwalifikacja Depleted.'])
add('C-9.94-01','Nagłówek 9.94 Barbarian Ferocity wprowadza stan Ferocity BI.',
    'R994 numer i pola używają Ferocity; literalnego tytułu nie zapisano osobno.',
    'Rola i nazwa stanu zachowane. Dawne mapowanie nie miało przecięcia dowodu z samym nagłówkiem; nie uznaję go przez parent za poprawny lokator.',
    'Tylko tożsamość/rola, bez nowej akceptacji lokatora lub dosłownego tytułu.',
    ['/rules/43/original_label','/rules/43/conditions'],'bounded_heading_role_supported',
    ['Oryginalny unassessed_locator i literalna transkrypcja nagłówka; DESIGN NOTE jest inną pozycją.'])
add('C-9.94-02',
    'Wszystkie BI zaczynają z Ferocity; jednostka BI z tym stanem ma -1 DRM Pre-Shock TQ, jej obrońcy +2 DRM do swoich Pre-Shock TQ rolls.',
    'R994 conditions start z Ferocity; action_effect/value/0 i parameters/value/0,1 mają -1 dla BI i +2 dla defender(s).',
    'Znak, strona i rodzaj testu zgodne; nie są to modyfikatory Hits lub Momentum.',
    'Lokalne modyfikatory zachowane; rzeczywista pełna kwalifikacja/test Pre-Shock wyłączone.',
    ['/rules/43/conditions/value/0','/rules/43/action_effect/value/0','/rules/43/interpretation/value/0','/rules/43/parameters/value/0','/rules/43/parameters/value/1'])
add('C-9.94-03',
    'Test po każdym Rout BI z leaderem ze scenariusza. DR<=Initiative zachowuje Ferocity, większy usuwa trwale tylko dla BI tego leadera, bez skutku dla innych leaderów.',
    'R994 conditions/value/1, cytat, action_effect/value/1,2 i parametr retention zapisują dokładnie operator <=, trwałość i niezależność dowództw.',
    'Równość jest po stronie zachowania, nie utraty. Nie pomylono trwałej utraty ze zdarzeniem Impetuosity do końca tury.',
    'Lokalny test zachowany; leader, jego rating i rzeczywiste przypisanie nadal wymagają setupu (EXP-064 wcześniej ocenione tylko jako wymaganie źródła).',
    ['/rules/43/transcription','/rules/43/conditions/value/1','/rules/43/action_effect/value/1','/rules/43/action_effect/value/2','/rules/43/parameters/value/2','/rules/43/time_limits'])
add('C-9.95-01','Nagłówek 9.95 Barbarian Impetuosity wprowadza stan początkowy BI.',
    'R995 original_label=9.95 i conditions/time_limits odnoszą się do Impetuosity.',
    'Rola zachowana, brak osobnego dosłownego tytułu nie jest tu certyfikowany jako pełna transkrypcja.',
    'Wyłącznie tożsamość/rola nagłówka.',
    ['/rules/44/original_label','/rules/44/conditions','/rules/44/time_limits'],'bounded_heading_role_supported',
    ['Literalny tytuł i cała klauzula C-9.95-02.'])
add('C-9.95-02',
    'Na początku bitwy Galowie rozbudzali się do gwałtownej szarży. Aby to oddać, BI startuje z MA+1, leaderzy BI z -1 DRM wszystkich first-try Momentum. Po wejściu co najmniej dwóch BI jednego dowództwa do enemy ZOC stan trwa do końca Game Turn, potem zanika tylko w tym dowództwie.',
    'R995 zachowuje MA+1, -1 first-try Momentum, >=2 BI, enemy ZOC, resztę tury i zakres dowództwa. Nie odwzorowuje początkowego zdania historycznego w textual content; krótki cytat dotyczy Momentum. Oryginalny obraz E995 zawiera całe wyjaśnienie.',
    'Część operatywna zgodna; początkowe wyjaśnienie historyczne pominięte w R995 w obu odpowiedziach. Ogólna nota N994design o wcześniejszej Ferocity nie odtwarza konkretnego zdania 9.95.',
    'SEM-022: ograniczone pominięcie tekstowe jednej klauzuli na odpowiedź. Nie wykazano zmiany liczby, legalności ani wyniku gry; źródłowy obraz zachowany. Bez automatycznego FN lub nowej reguły.',
    ['/rules/44/transcription','/rules/44/interpretation','/rules/44/conditions','/rules/44/action_effect','/rules/44/parameters','/rules/44/time_limits'],
    'mixed_operative_supported_explanation_omitted',
    ['Rzeczywisty setup/ZOC/Momentum i całość historycznej prozy; wcześniejsze źródłowe wymagania nie zostają zamknięte.'])
add('C-9.96-01','Nagłówek 9.96 Gallic Chariots wprowadza reguły CH.',
    'R996a–d mają ten sam original_label i odnoszą się do Gallic Chariot/LI mounted on CH.',
    'Tożsamość/rola jednego nagłówka zachowane przy rozdzieleniu rekordów; dawne mapowanie dowodów nie przecinało samego nagłówka.',
    'Jedno oznaczenie, bez mnożenia punktów. Nie jest to pozytywna ocena nagłówkowego lokatora.',
    ['/rules/46/original_label','/rules/46/unit_types','/rules/47/original_label','/rules/48/original_label','/rules/49/original_label'],'bounded_heading_role_supported',
    ['Literalna transkrypcja tytułu, unassessed_locator i cała DESIGN NOTE.'])
add('C-9.96-02',
    'CH ma tylko MA, bez Size/TQ; nie porusza się nawet przez OW bez eligible LI. Każda enemy combat unit podchodząca obok CH samotnego w heksie natychmiast go eliminuje.',
    'R996a ma literalny cytat MA/Size/TQ, warunek eligible LI w conditions, OW tam wskazane i w action_effect eliminację za kwalifikujące podejście.',
    'Zachowano warunek samotnego CH, typ każdej enemy combat unit i czas natychmiastowy; nie jest to dowolna już istniejąca adjacency.',
    'Lokalny zakaz/wyjątek/skutek zgodne; eligible LI i pełne OW nie są odtworzone.',
    ['/rules/46/transcription','/rules/46/conditions','/rules/46/action_effect','/rules/46/exceptions','/rules/46/time_limits'])
add('C-9.96-03',
    'CH przewozi jedną LI, leży nad LI, para liczy się jako jedna jednostka dla stosów przy innych ograniczeniach. Wsiadanie/zsiadanie LI kosztuje 0 MP/0 Hits. Zsiadająca może kontynuować tylko przy used<printed LI MA, pozostaje różnica; wsiadająca używa CH MA minus wcześniej użyte LI MP. CH obeys Movement Cost Chart, Hits ruchu tylko LI.',
    'R996b zapisuje 1 LI, CH na górze, stack count=1, 0 MP/0 Hits, ścisłe < i dwie różne formuły odejmowania; inne ograniczenia i Movement/Terrain Hits rozdzielone.',
    'Źródło sklejono od dołu PDF36 prawej do góry PDF37 lewej. Użyto właściwego MA po zsiadaniu i wsiadaniu; brak nowej różnicy w operatorach.',
    'Lokalne formuły i granice zachowane; nie odczytano z nich rzeczywistych MA lub kosztów/prohibicji tabeli.',
    ['/rules/47/transcription','/rules/47/conditions','/rules/47/action_effect','/rules/47/exceptions','/rules/47/parameters','/rules/47/time_limits'])
add('C-9.96-04','Wprowadzenie listy ogranicza następujące abilities/liabilities do LI mounted on CH.',
    'R996c/d ma unit_types i conditions dla zamontowanych LI; podaje powiązane uprawnienia/zakazy.',
    'Zachowano podmiot listy i stan mounted, nie przypisano całej listy CH samotnemu. Nie jest to dosłowna transkrypcja wprowadzenia.',
    'Wyłącznie rola i zakres listy; trzy punkty ocenione przez ich własne źródła.',
    ['/rules/48/unit_types','/rules/48/conditions','/rules/49/unit_types','/rules/49/conditions'],'bounded_heading_role_supported',
    ['Dosłowny tekst wprowadzenia i przyjęcie wszystkich pól trzech punktów przez sam parent.'])
add('C-9.96-05',
    'Brak Cohesion Hits za drugi/trzeci ruch w Game Turn tylko jeżeli LI spędza całą Orders Phase na CH.',
    'R996c transcription cytuje część przed warunkiem; conditions i time_limits uzupełniają entire Orders Phase mounted, action_effect/value/0 łączy warunek ze skutkiem; parametry second/third i 0 Hits.',
    'Warunek nieobecny w wybranym krótkim cytacie jest obecny w innych oryginalnych polach; nie jest to jego całkowite pominięcie ani zwolnienie za częściowy czas mounted.',
    'Zachowano zakres zwolnienia i jednostki czasu; ocena jest łączna dla wymienionych pól.',
    ['/rules/48/transcription','/rules/48/conditions','/rules/48/action_effect/value/0','/rules/48/parameters','/rules/48/time_limits'],exclusions=['Drugi punkt Shock w tym samym rekordzie nie otrzymuje tej oceny.'])
add('C-9.96-06',
    'Mounted LI nie atakuje Shock, musi zsiąść do ataku; gdy mounted, broni się jako LI.',
    'R996c action_effect/interpretation/value/1 podaje zakaz ataku, konieczność zsiadania i obronę jako LI.',
    'Atak i obrona rozdzielone; warunek całej Orders Phase z pierwszego punktu nie jest przenoszony na tę klauzulę.',
    'Lokalne zdanie zgodne; bazowe Shock/defense/tabele poza oceną.',
    ['/rules/48/action_effect/value/1','/rules/48/interpretation/value/1','/rules/48/unit_types'],exclusions=['Zwolnienie za drugi/trzeci ruch i jego warunek całej fazy ocenione osobno.'])
add('C-9.96-07',
    'Mounted LI używa Mounted Javelin row MRRC; Missile Supply 8.17 nie obowiązuje while mounted; przy mounting usuwa Low/No; może H&D jak cavalry.',
    'R996d zachowuje row, while mounted, moment usunięcia markerów i H&D as cavalry; transcription dosłownie cytuje wyjątek Supply, reszta w action_effect/exceptions/time_limits.',
    'Zachowano warunek i moment; nazwy Low/No zgodne z wcześniejszym display overlay. Nie zgadnięto wartości MRRC ani bazowego H&D.',
    'Lokalne wyjątki i uprawnienia zgodne; pełny wynik pozostaje zależny od brakujących tabel/procedur.',
    ['/rules/49/transcription','/rules/49/conditions','/rules/49/action_effect','/rules/49/exceptions','/rules/49/time_limits'])
add('G-03',
    'Obraz Scorpio: nazwa u góry; pod nią 1 i LI; środkowy czerwony 1; dolny szary 2 i czarny 3; silnik broni w ilustracji.',
    'N981counter transcription.visible_text zawiera Scorpio,1,LI,1,2,3, a interpretation jawnie nie nadaje rating-position meanings; geometria pozostaje w dołączonym obrazie.',
    'W obu dokładnych wycinkach napis i glify zgodne. Lista tekstowa nie koduje pełnego rozmieszczenia, które zachowuje źródłowy obraz.',
    'Ograniczone podparcie widocznych glifów i zachowanej ilustracji, bez znaczenia ratingów/tożsamości setupu.',
    ['/nodes/33/original_label','/nodes/33/content'],'bounded_graphic_supported',
    ['Znaczenie ratingów, rzeczywiste wartości gry, identyfikacja konkretnej jednostki i pełna certyfikacja każdego piksela.'])
add('G-04',
    'Dwie ilustracje obok siebie: Active Fire Once po lewej, Active Fire Finished po prawej; w obu biały trójkąt przy Fire.',
    'N985markers zapisuje obie nazwy i rolę dwóch stanów; oryginalny obraz zachowuje ich kolejność, glify i rozmieszczenie.',
    'Oba podpisy/nazwy zgodne, Once nie pomylono z Finished; tekstowe content nie jest opisem każdego graficznego elementu.',
    'Widoczne nazwy i lokalna ilustracja sekwencji R985 podparte; bez nowych reguł markera poza tekstem.',
    ['/nodes/34/content'],'bounded_graphic_supported',exclusions=['Pełne glify/kolory jako osobna transkrypcja i niezależne zasady resetu markerów.'])
add('G-05',
    'Jedna ilustracja Reaction Fire Once; Finished nie jest tu narysowane, jest wymienione w prozie 9.86. Biały trójkąt przy Fire na niebieskim tle.',
    'N986marker transcription=Reaction Fire Once, interpretation jawnie rozdziela obraz Once od tekstowego Finished w R986.',
    'Nie dopisano drugiej narysowanej strony; dokładny zakres ilustracji zgodny w obu odpowiedziach.',
    'Podparcie widocznego markera i rozróżnienia prozy od obrazu; bez pełnej certyfikacji grafiki.',
    ['/nodes/35/content'],'bounded_graphic_supported',exclusions=['Nieistniejący w tym miejscu obraz Finished i całe dodatkowe reguły ognia.'])
add('K-06',
    'Koniec lewej kolumny PDF36: BI units; początek prawej: cannot use Column Movement... To jedno kontynuowane zdanie.',
    'N991first→N991next wskazuje wcześniejszy/późniejszy fragment i owner_rule_id=R991; Dcont-R991 ma kind continuation.',
    'Kolejność i połączenie fizyczne zgodne. Węzły są lokatorami, nie osobnymi klauzulami wykonawczymi.',
    'Połączenie nie tworzy nowej reguły lub wykonawczej zależności i nie daje kolejnych punktów za C-9.91-02.',
    ['/nodes/44/content','/nodes/44/source_locator','/nodes/45/content','/nodes/45/source_locator','/dependencies/20/from','/dependencies/20/to','/dependencies/20/kind'],'bounded_physical_continuation_supported')
add('K-07',
    'Koniec PDF36 prawej: treated as a single; początek PDF37 lewej: unit for stacking purposes. Ten sam akapit kontynuuje transport przed listą i granicą 10.0.',
    'N996first→N996next ma owner_rule_id=R996b i earlier/later; Dcont-R996b continuation zachowuje kierunek.',
    'Nie urwano single unit przy zmianie strony; nie włączono treści 10.0 do 9.96.',
    'Ograniczona fizyczna kontynuacja, bez punktowania całego transportu ponownie.',
    ['/nodes/46/content','/nodes/46/source_locator','/nodes/47/content','/nodes/47/source_locator','/dependencies/21/from','/dependencies/21/to','/dependencies/21/kind'],'bounded_physical_continuation_supported')
