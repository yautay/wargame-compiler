# M-POC1B — konkretne pytania do przeglądu

2026-10-07, draft-001, **waiting_review**. Przygotowanie Codex zakończone;
przegląd znaczenia i krytyczności właściciela w tej sesji jeszcze się nie odbył.
To materiał do wspólnego przeglądu M-POC1B, nie wykonanie M-POC1C ani zgoda na freeze.

Czytaj [oczekiwania](expectations.json), [relacje](dependencies.json) i
[20 sytuacji](situations.json) razem z dowodami osadzonymi w rekordach.
Współrzędne są w punktach PDF, od lewego górnego rogu, x w prawo, y w dół.
Obwiednia zawiera tekst/kontekst; nie stanowi dokładnej segmentacji wszystkich glifów.
[Przegląd M-POC1A](../owner-review-001/review-summary.md) i jego manifest dotyczą
inwentarza/struktury/polityki, bez akceptacji poniższych propozycji.

## Co dokładnie jest gotowe

| Zbiór | Propozycje poparte lokalnym źródłem | Wymaga kontekstu | Nierozstrzygnięta interpretacja | Potwierdzone przez właściciela |
|---|---:|---:|---:|---:|
| 74 oczekiwania | 64 | 8 | 2 | 0 |
| 20 sytuacji | 16 wyników lokalnych | 3 blokady kontekstu | 1 blokada interpretacji | 0 |

Każde oczekiwanie ma dowód i odrębne uzasadnienie proponowanej krytyczności.
74 to liczba propozycji do oceny, nie liczba norm ani potwierdzony mianownik
atomowego pokrycia. Dowody obejmują wszystkie 41 oznaczeń reguł, ale nie
potwierdzają pełnego podziału każdej klauzuli. Wszystkie 74 oznaczono jako
krytyczne w podanym zakresie: pomyłka wpływa na legalność, skutek, liczbę,
wyjątek, czas lub możliwość rozstrzygnięcia; właściciel może zawęzić zakres
albo uzasadnić inną krytyczność. Opisowe wzmianki relacji są niekrytyczne.

`source_supported_proposal` oznacza weryfikację podstawy przez Codex w zakresie
lokalnego twierdzenia, **nie** semantyczną akceptację właściciela.
`requires_context` nie usuwa znanych lokalnych warunków. Nieznana mapa,
eligibility, dowódca czy bazowa tabela blokuje konkretny pełny wynik.
Liczby i typy zadane syntetycznie w sytuacjach nie są parametrami zaakceptowanego
realnego scenariusza. Wyniki lokalne nie oznaczają legalności całej akcji.

## Pytania w zalecanej kolejności

### RQ-01 — granica minimum w 9.16

Dowód: [PDF33](../../source/review-evidence/pdf-33.png), lewa kolumna,
C-9.16-01; EXP-016/017, SIT-07, DEP-050-1/2/3.
Zdanie wiąże Hits z `DR is higher` i dodaje minimum 1.
Czy przy DR=TQ albo niższym minimum obejmuje sam test, czy tylko dodatni
nadmiar? Propozycja robocza: **zachować blokadę liczby 0/1** do uzasadnionej
decyzji; sam natychmiastowy test przy braku OW pozostaje wymagany.
Potrzebna decyzja: dokładny zakres minimum, dowód i krytyczność, albo jawne
pozostawienie EXP-017/SIT-07 nierozstrzygniętych. Nie proszę o ponowną akceptację
granicy rozdziału ani struktury inwentarza.

### RQ-02 — Leader Elephant, wiersz 7–9 i zakaz rally

Dowód: [PDF32](../../source/review-evidence/pdf-32.png), TR-01/TR-03,
C-9.14-11 i dokończenie na [PDF33](../../source/review-evidence/pdf-33.png).
EXP-007/008/009/011, SIT-04/05; szczególna relacja DEP-NEW-002.
Czy akceptujesz lokalny wynik **późniejszego** 7–9 jako natychmiastowy rally
Leader Elephant z Hits=TQ−2 mimo zwykłego zakazu rally Rampage?
Osobno: czy końcowe `If it is a Leader Elephant` obejmuje także pierwszy 7–9?
Propozycja: SIT-05 używa wyłącznie późniejszego rzutu; pierwszy pozostaje
EXP-009 unresolved. Decyzja o późniejszym rzucie nie zatwierdza pierwszego.
Nie podstawiać TQ z drobnego żetonu; w SIT-05 TQ6 jest syntetycznym wejściem.

### RQ-03 — Pass-Thru: czas, adresaci i dwa testy

Dowód: [PDF31](../../source/review-evidence/pdf-31.png), prawa core,
[PDF32](../../source/review-evidence/pdf-32.png), lewa kroki 3–4;
EXP-001–004, SIT-01–03; DEP-001/002/008/045-1–3/046.
Czy zatwierdzasz wszystkie trzy lokalne rozstrzygnięcia: start-phase ZOC
wyklucza opcję mimo późniejszego wyjścia, 5 Hits→2 i3→2 przy podanych wynikach
bazowych, SK bez końcowego Pass-Thru Check, z rozróżnieniem Pre-Shock i jego
adresatów? Propozycja nie usuwa żadnego innego testu TQ i nie ustala dolnej
granicy redukcji EL, gdy bazowe Hits=0. Jeśli ta granica ma wejść do oceny,
potrzebny osobny dowód; obecne SIT-01 jej nie testuje.

### RQ-04 — które odsyłacze są tylko wzmiankami

Dowody: X-02, X-04, X-01, X-06, C-9.61-01, C-9.66-01 oraz dopisany
facet OW-alternative C-9.66-01. DEP-034/035/037/043/044/063/067-1,
candidate_audit DC-034/035/037/043/044/063/067.
Czy akceptujesz klasyfikację tych siedmiu propozycji jako `mention`,
oddzielnie od wykonawczego lookup/procedury? W szczególności `for a summary`
w 9.61 nie tworzy obowiązkowego wykonania Stacking Charts; pełna legalność
stacking nadal zależy od exceptions/eligibility DEP-064-1/2.
X-01 nie tworzy drugiego lookup obok TR-02→map compass, a X-06 nie zastępuje
N-09→scenario eligibility. Kierunek zawsze od źródła odsyłającego do celu.

### RQ-05 — hipoteza MRRC oraz zakres instrukcji w notach

Dowody: [PDF32](../../source/review-evidence/pdf-32.png), C-9.13-01/N-03-S2;
[PDF33](../../source/review-evidence/pdf-33.png), N-07-S2;
[PDF36](../../source/review-evidence/pdf-36.png), N-14-S2/S3;
[PDF37](../../source/review-evidence/pdf-37.png), C-9.96-07.
EXP-005/006/021/066/073, DEP-030/031/038/040.
Czy zachować DC-031→MRRC jako niepotwierdzoną **niejawną** hipotezę
table/row identity, mimo jawnej klasyfikacji riders jako Mounted Javelinists?
Czy akceptujesz jako propozycje znaczenia N-03-S2 (wieża nie wyłącza reguły)
i N-07-S2 (Velites LI, nie SK)? Podział tych not z M-POC1A nie był tą akceptacją.
Osobno N-14-S2: jaki dokładnie zakres Combat Tables i Chariot entries wolno
pominąć dla Gallic CH? Propozycja: EXP-066/DEP-038 **requires_context**,
bez rozszerzenia na wszystkie historyczne rydwany lub całą instrukcję.

### RQ-06 — liczby i wyjątki SK/LC, konflikt AS

Dowody: [PDF33](../../source/review-evidence/pdf-33.png), prawa9.21–9.24;
[PDF34](../../source/review-evidence/pdf-34.png), lewa9.31–9.32/X-04.
EXP-021–031; SIT-08/09; DEP-010/011/012/035/053/054-1/2/055/056.
Czy zatwierdzasz kierunek wyjątku PH/HI/LG broniących Front przeciw LI,
SK halving w dół z cap1 oraz LC H&D tylko przeciw niższemu MA, nigdy SK?
Czy pojedyncza jednostka w **każdej** przerwie line jest właściwym odczytem
X-03, bez globalnego limitu jednej SK/Velites w całej line?
Oddzielna luka: X-04 z AS daje printed result, podczas gdy9.32 daje połowę.
Propozycja EXP-031 wymaga ograniczonego kontekstu kolejności AS/halving;
SIT-09 celowo podaje brak superiority. Nie uznać tego testu za rozstrzygnięcie konfliktu.

### RQ-07 — Phalanx Defense i gotowe DD

Dowód: [PDF34](../../source/review-evidence/pdf-34.png), obie kolumny;
EXP-032–040, SIT-10/11/12, DEP-017/036/058/059-1–3/060-1/2/061/062.
Czy zatwierdzasz 1L **na flank** przy moving HI (dwa flanks→2L), brak shift
przy started-adjacent/stayed oraz DD Flank3×, 9 Hits→top5/bottom4?
Czy eligibility nadal blokuje formowanie rzeczywistych PH bez listy scenario,
mimo spełnienia geometrycznych/MP warunków9.51?
Propozycja rozróżnia formowanie DD od zakazu wchodzenia w **gotowy** DD;
retreat do osobnych heksów i zakres końcowego `the unit` nie zostały domknięte
w konflikcie z zajętymi heksami. Nie stosować9.41 bezwarunkowo przez9.53.

### RQ-08 — Roman stacks: orders, testy i niezamknięta alokacja

Dowody: [PDF35](../../source/review-evidence/pdf-35.png), lewa9.61–9.65;
10.13 w **kontekście** [PDF37](../../source/review-evidence/pdf-37.png), prawa.
EXP-041–045, SIT-13; DEP-018–022/037/064-1/2/065/066.
Czy akceptujesz IO-only dla zmiany stacking order, LC dla facing, własny test
każdej unit zTQ top oraz+1DRM dla warunków9.63? Propozycja nie uznaje
`rule of thumb` za pełne stacking eligibility.
Czy pozostawić pełną alokację multi-stack Shock Hits zablokowaną przez
8.46Step4/10.13→6.68 mimo widocznego10.13? Obejrzenie kontekstu nie daje
źródła6.68 ani zatwierdzonej procedury; SIT-13 nie pyta o taką alokację.

### RQ-09 — MLE: warunki, diagram i dwie reakcje

Dowody: [PDF35](../../source/review-evidence/pdf-35.png), D-02/CAP-01/02,
sześć fragmentów9.66,9.67–9.68; EXP-046–048; SIT-14/15;
DEP-023/044/067-1–3/068/069-1/2 oraz fizyczne DEP-094.
Czy zatwierdzasz wszystkie lokalne warunki destinations i unstack-only,
zachowanie facing oraz MA−2 obu units **po LC**, bez przeniesienia tego
post-move prawa na reakcję? Czy zakaz OW+MLE przez te same units jest
krytyczny także gdy oba triggers jednocześnie zachodzą?
Zatwierdzona wcześniej struktura paneli nie dawała akceptacji legalności ruchu.
Grafika nie jest źródłem nowych uprawnień do ponownego stacking.

### RQ-10 — Triarii: dwie bramki i parametry scenariusza

Dowód: [PDF35](../../source/review-evidence/pdf-35.png), prawa9.7–9.72;
EXP-049–052; SIT-16; DEP-070-1/2/071-1/2/072/073-1/2/NEW-001.
Czy akceptujesz niejawne9.72→9.71 jako potrzebę **zachowania obu bramek**,
a nie automatyczne uchylenie zakazu ruchu przez osiągnięcie RP?
Czy lokalnie AWL11→próg5 i standing Shock bez ruchu przyRP4 są prawidłowe
przy jawnie podanej stosowalności iZOC? Cannae jest wskazanym wyjątkiem źródła,
nie wnioskiem z historii. Inna realna bitwa bez daty/OC/AWL zostaje requires_context.

### RQ-11 — Scorpio: nadrzędność mode lock i liczniki

Dowód: [PDF36](../../source/review-evidence/pdf-36.png), lewa9.81–9.87,
N-11/G-04/G-05; EXP-053–059; SIT-17; DEP-024/025/074-1/2/075-1/2/076–079
(z facetami) oraz DEP-NEW-003.
Czy no-order fire nie usuwa zakazu strzału w phase switch-to-Fire,
a limity active2/Game Turn +1/friendly phase i reaction2/enemy phase
muszą pozostać osobne? Czy Rampage no Reaction Fire **of any kind**
wyłącza także tę szczególną reakcję Scorpio? Propozycja tak; zakres target
Rampaging EL nie jest testowany w liczbach SIT-17 i pozostaje osobną relacją.
Tylko Once/Finished i mapping Fire/Move są odczytane z grafiki; brak pełnej
transkrypcji drobnych ratings G-03 pozostaje ograniczeniem.

### RQ-12 — BI: command, trigger i koniec turn

Dowód: [PDF36](../../source/review-evidence/pdf-36.png),9.91–9.95;
EXP-060–065; SIT-18/19; DEP-026–028/080/081-1/2/082/083-1/2/084-1/2.
Czy brak terrain cohesion BI nie usuwa MP/passability, Recovery order tylko1,
a depleted elimination nie ma automatycznie statusu Rout dla Ferocity trigger?
Propozycja pozostawia konflikt tego triggera do przeglądu, nie dodaje nowego testu.
Czy brak mapping leadera jest krytyczną blokadą w SIT-18, a w SIT-19
Impetuosity trwa do końca turn drugiego wejścia BI **tej command**, bez
natychmiastowej lub globalnej utraty? Syntetyczne mapping nie akceptuje realnego setup.

### RQ-13 — Gallic CH: granica MA i while/entire phase

Dowody: [PDF36](../../source/review-evidence/pdf-36.png),9.96/N-14;
[PDF37](../../source/review-evidence/pdf-37.png), lewa core przed10.0;
EXP-066–073; SIT-20; DEP-029/038/039/040/085-1/2/086-1/2/087/088-1/2/089.
Czy akceptujesz strict-less-than przy dismount (MA5 i4MP→1,5MP→brak ruchu),
CH-MA minus już użyte LI MP przy mount, mounted zakaz Shock attack i wymóg
**całej Orders Phase** dla zwolnienia repeat-movement cohesion?
Czy zachować removal LOW/NO przy mount, bez zgadywania supply po dismount?
Eligibility LI i tabeli kosztów nie ustalono; SIT-20 podaje je syntetycznie
i pyta o budżet, nie legalność dowolnej trasy. No Hits CH nie znosi terrain prohibition.

### RQ-14 — mianowniki relacji, krytyczność i pokrycie sytuacji

Dowody i listy: wszystkie rekordy trzech JSON, `candidate_audit` dla96/96;
osobne liczniki explicit/implicit/mention/continuation w dependencies.json.
Czy akceptujesz jako użyteczny zakres **lokalne** wyniki 16 sytuacji oraz
cztery blokady, zamiast pełnych rozstrzygnięć bitewnych bez tabel/scenariusza?
Proponowane16/20 =80% jest tylko składem draftu, nie osiągnięciem progu jakości
przyszłej ekstrakcji. Przed freeze trzeba ocenić, czy taki zakres mierzy zamierzony POC;
nie dostosowywać zestawu do późniejszej odpowiedzi.

Czy akceptujesz proponowaną krytyczność każdego EXP/SIT i wykonawczej relacji,
czy któreś ID wymaga zawężenia/innego uzasadnienia? Krytyczność nie pochodzi
z decyzji M-POC1A. Kierunek, kind, target identity i necessity należy ocenić
oddzielnie; `requires_context` nie jest pewnym gold ani FP.
Trzy nowe relacje DEP-NEW-001/002/003 pokazano jawnie poza96; rozdzielenie
compound candidates i zmiana explicitness są w audycie. Nie traktować liczby
propozycji jako zweryfikowanego grafu; owner-confirmed execution pozostaje
0 jawnych i 0 niejawnych, a precision/recall=n/a przed oceną.

### RQ-15 — kompletność przeglądu przed przekazaniem

Czy po przeglądzie wszystkich ID pozostają oczekiwania bez wystarczającego dowodu,
niepoparte krawędzie albo pominięte krytyczne warunki? Sprawdź także oczekiwania
bez własnej sytuacji: to świadomy dobór20 testów, nie pełne pokrycie każdej reguły.
Nie zatwierdzać całych74/relacji przez odpowiedź na jeden przykład. Dla zakresów
zbiorczych wymień dokładnie ID, dowody oraz pozostawione nierozstrzygnięcia.
Pełny podział atomowy i wszystkie drobne napisy pozostają niesprawdzone.

## Sposób zapisu odpowiedzi i dokładne wznowienie

Zacząć od **RQ-01**, z pokazaniem pełnego fragmentu źródła i SIT-07.
Następnie RQ-02 i pozostałe w kolejności. Dla każdego zapisać: recenzent,
rzeczywista odpowiedź, data/czas dostępny, zakres ID, uzasadnienie krytyczności,
dowód/hashe, pozostawione braki. Decyzje zapisać osobno, nie nadpisywać
oryginalnych source/draft ani rejestru owner-review-001.
Odpowiedź na jeden RQ nie nadaje akceptacji innym ID.

Przegląd M-POC1B pozostaje do wykonania; karta **partial/waiting_review**,
przygotowanie techniczne kompletne. Nie wykonano M-POC1C, nie zamrożono eval-v1,
nie wykonano M-POC2B ani ekstrakcji. Po rzeczywistym przeglądzie i odnotowaniu
zakresu domknąć M-POC1B; dopiero osobna karta M-POC1C może dostać kompletny
draft i decyzje do przeglądu zamrożenia. M-POC1 pozostaje jedynym next.
