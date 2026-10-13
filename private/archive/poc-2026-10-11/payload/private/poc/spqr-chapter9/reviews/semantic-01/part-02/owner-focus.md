# Przegląd właściciela — EXP-001–025

Każdy wiersz porównuje dokładny zatwierdzony zakres ze źródłem i obiema odpowiedziami. To propozycje Codex; wszystkie decyzje właściciela nadal pending. Pełne literalne pola, źródła i bajty są w [review.md](review.md) oraz [comparisons.json](comparisons.json).

first-001: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

context-01: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

eval-v1: `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`.

## Zakresy proponowane jako zgodnie reprezentowane

Lista 22 lokalnych zakresów: EXP-001–009, EXP-011–016, EXP-018, EXP-020–025. Każdy dotyczy wyłącznie swojego frozen reviewed_scope w obu hashach. EXP-016 ma osobny, zachowany błąd E916; zgodność treści nie akceptuje tego lokatora. Nie są objęte nieprzejrzane pola, aliasy, pełne procedury, małe wartości grafik, relacje ani sytuacje.

### EXP-001

Źródło i zatwierdzony zakres: In the reviewed supplied case, Pass-Thru is allowed with LI defending Front, EL marker, no co-attacker, no initial enemy ZOC, a free Rear and an early decision. Initial enemy ZOC excludes it despite later exit. With two defenders both must meet the earlier conditions.

Oba wyniki: R911.conditions: Front, marker, wolny Rear; exceptions: Flank/Rear, współatak i ZOC na początku Orders Phase. time_limits zachowuje decyzję przed DR i początkowy ZOC. Obie jednostki muszą spełniać warunki. Nie wyliczamy geometrii ZOC.

Dowody: PDF 31 right, C-9.11-01, PDF 31 right, C-9.11-02, PDF 31 right, C-9.11-03, PDF 31 right, C-9.11-04, PDF 31 right, C-9.11-05.

Niepewności/wyłączenia: Pełny Shock i definicje Front/Rear/ZOC są celami zewnętrznymi; nie wyliczać ich z tego akapitu.

### EXP-002

Źródło i zatwierdzony zakres: For the reviewed supplied Pass-Thru result, defender Pre-Shock +1 DRM; infantry Hits 5 become 2 and EL Hits 3 become 2. Base-0 reduction floor and other modifier order remain unresolved.

Oba wyniki: R911 action_effect/parameters zachowują Pre-Shock +1 DRM, pół/floor Hits obrońcy i -1 Hits EL. Są to operatory zgodne z zatwierdzonym zakresem 5→2 oraz 3→2; nie dopisano dolnej granicy dla bazowego 0 ani kolejności innych modyfikatorów. Nie oceniono SIT.

Dowody: PDF 31 right, C-9.11-07, PDF 31 right, C-9.11-08.

Niepewności/wyłączenia: Base EL Hits=0 reduction floor/order remains unresolved; do not infer a negative result or minimum.; Bazowy wynik Shock musi być dostarczony; kolejność innych modyfikatorów i dolna granica redukcji EL do przeglądu.

### EXP-003

Źródło i zatwierdzony zakres: After supplied no-infantry-Rout and no-EL-Rampage outcomes, place EL in a free defender Rear hex chosen by the EL player, keeping facing. No complete Shock result inferred.

Oba wyniki: R911 action_effect krok 3: po Shock, tylko gdy piechota nie Rout i EL nie Rampage; wolny Rear wybiera gracz EL, facing zachowane. Nie zastępuje to pełnego wyniku Shock.

Dowody: PDF 32 left, C-9.11-09.

Niepewności/wyłączenia: Stan Rout wymaga procedury ogólnej; Rampage ma wewnętrzny cel R-9.14.

### EXP-004

Źródło i zatwierdzony zakres: The final Pass-Thru TQ check is separate from Pre-Shock; SK are exempt from that final check. For non-SK, positive DR-TQ gives Hits; DR<=TQ gives no excess. No minimum imported from 9.16.

Oba wyniki: R911 rozdziela końcowy Pass-Thru TQ od Pre-Shock, wyłącza SK z kroku 4 i nalicza tylko positive excess DR-TQ. R924 powtarza wyłączenie SK. Parametr positive excess nie importuje minimum 1 z 9.16; brak konkretnej liczby nie jest pominięciem operatora.

Dowody: PDF 32 left, C-9.11-10, PDF 33 right, C-9.24-03.

Niepewności/wyłączenia: Nie rozszerzać wyjątku na wszystkie testy TQ.

### EXP-005

Źródło i zatwierdzony zakres: Elephant Screen uses the explicitly named Elephant Screen MRRC row and fires only as Reaction Fire, has its own supply markers, and is absent on Leader Elephant. Actual lookup and supply procedure remain context requirements.

Oba wyniki: R912: Reaction Fire only, nazwany Elephant Screen MRRC row, własne supply markers i brak screen u Leader Elephant. Nie ma podstaw do wartości pełnego lookupu lub domknięcia supply.

Dowody: PDF 32 left, C-9.12-02, PDF 32 left, C-9.12-03.

Niepewności/wyłączenia: Pełny wynik ognia wymaga 8.2 i wiersza MRRC.

### EXP-006

Źródło i zatwierdzony zakres: RidersasMountedJavelinists,separatejavelin/screenDR,N03-S2nochangefromhistoricaltowerabsence

Oba wyniki: R913: Mounted Javelinists dla Missile Fire; javeliny/screen mają osobne DR. R913note: historyczny brak wież nie zmienia reguły. Nie utożsamiono niepotwierdzonych aliasów wiersza MRRC.

Dowody: PDF 32 left, C-9.13-01, PDF 32 left, N-03-S2.

Niepewności/wyłączenia: Tożsamość wiersza MRRC z samego Mounted Javelinists pozostaje hipotezą DC-031.

### EXP-007

Źródło i zatwierdzony zakres: Ordinary EL Rout triggers immediate Rampage procedure. Ordinary EL roll 0 heads toward nearest friendly unit with opponent choosing a tie; first 7-9 moves away from cause, subsequent 7-9 eliminates. Concrete map and cause are not invented.

Oba wyniki: R914 i N914table zachowują immediate Rout→Rampage; zwykły EL: 0 do najbliższej friendly, remis wybiera przeciwnik; pierwsze 7–9 od przyczyny, późniejsze 7–9 eliminacja. first/subsequent jest jawne w wierszu tabeli. Rzeczywisty kierunek nie został ustalony.

Dowody: PDF 32 left, C-9.14-01, PDF 32 left, T-01, PDF 32 right, T-01, PDF 32 left, TR-01, PDF 32 left, TR-02, PDF 32 right, TR-03.

Niepewności/wyłączenia: Kierunku na rzeczywistej mapie nie ustala sam przykład D-01.

### EXP-008

Źródło i zatwierdzony zakres: Leader Elephant roll 0 eliminates it; subsequent 7-9 immediately rallies it with Hits=TQ-2 instead of elimination. This owns the subsequent-roll result; first Leader 7-9 is scored only in EXP-009.

Oba wyniki: N914table: Leader 0 eliminuje; późniejsze 7–9 rally z Hits=TQ−2 zamiast eliminacji. R914.exceptions utrzymuje ten wyjątek wobec ogólnego zakazu rally. Pierwsze 7–9 nie daje drugiego punktu w EXP-008.

Dowody: PDF 32 left, TR-01, PDF 32 right, TR-03, PDF 32 right, C-9.14-11, PDF 33 left, C-9.14-11.

Niepewności/wyłączenia: Later7-9LeaderRally outcome andcriticality accepted; actualTQ and4.84counting notclosed. Firsttable7-9 addressedseparatelyEXP009.; Zakres Leader Elephant przy pierwszym 7–9 jest odrębnym nierozstrzygniętym oczekiwaniem.

### EXP-009

Źródło i zatwierdzony zakres: First Rampage-table 7-9 for Leader Elephant means movement away from the causing unit, without immediate special rally. Subsequent-roll result is referenced in EXP-008 and earns no second point here. Counting the 4.84 trigger die is unresolved.

Oba wyniki: N914table rozdziela first Rampage DR od any subsequent: pierwsze Leader 7–9 prowadzi od przyczyny, nie do natychmiastowego rally. R914.exceptions ogranicza rally do subsequent. Nie określono zaliczania rzutu wyzwalającego 4.84.

Dowody: PDF 32 right, TR-03, PDF 32 right, C-9.14-11, PDF 33 left, C-9.14-11.

Niepewności/wyłączenia: FirstLeader7-9interpretation andcriticality accepted;actualcause/map/route/TQ and4.84countingnotclosed.; Przegląd składni tabeli i uzasadniona decyzja właściciela.

### EXP-011

Źródło i zatwierdzony zakres: Complete each Rampage immediately before any other mechanic except OW under 6.51; no concurrent Rampages. Rampaging EL has no ZOC, triggers no Reaction Fire of any kind, and normally cannot rally. The special later Leader result is a reference to EXP-008, not a second scored result.

Oba wyniki: R914: immediate i serial resolution, wyjątek OW; brak ZOC i Reaction Fire każdego rodzaju; no rally z osobnym wyjątkiem Leader w exceptions. C-9.14-11 przechodzi na PDF33 i kontynuacja źródła jest zachowana. Wyjątek jest referencją do EXP-008, bez drugiego punktu.

Dowody: PDF 32 right, C-9.14-02, PDF 32 right, C-9.14-11, PDF 33 left, C-9.14-11.

Niepewności/wyłączenia: OW 6.51 wymaga zewnętrznej procedury; szczególny Leader Elephant zachować oddzielnie.

### EXP-012

Źródło i zatwierdzony zakres: Attempt 3 hexes per directional roll with supplied route/no early termination. At a would-be occupied hex stop adjacent; occupant gets 1 CH via Front, 2 via Flank/Rear, cavalry always 2. Both units of a stack get their Hits. A leader unable to withdraw under 4.72 dies without DR; actual inability requires context.

Oba wyniki: R914 parametry/action: próba 3 hexów na directional DR; stop adjacent przed occupied hex; occupant 1 CH przez Front, 2 Flank/Rear, cavalry zawsze 2; oba elementy stacku Hits. Leader unable to withdraw według 4.72 ginie bez DR. Realnego warunku unable nie domknięto.

Dowody: PDF 32 right, C-9.14-03, PDF 32 right, C-9.14-04.

Niepewności/wyłączenia: Możliwość withdrawal leadera wymaga 4.72; geometrię i typy przyjąć tylko jako jawne dane przypadku.

### EXP-013

Źródło i zatwierdzony zakres: Repeat until offmap, elimination(ordinaryEL7-9mahout), at least8hexes from nearest unit(any allegiance) causing elimination, or if none above eliminate after4th consecutive RampageDR.

Oba wyniki: R914: ponawianie do offmap/elimination, >=8 hexów od nearest unit i eliminacja po 4. consecutive DR, jeśli wcześniej nie zakończono. Wiersz tabeli i wyjątki nadal kwalifikują późniejsze 7–9 oraz Leader. Nie dodano realnego pomiaru mapy.

Dowody: PDF 32 right, C-9.14-06, PDF 32 right, C-9.14-07, PDF 32 right, C-9.14-08, PDF 32 right, C-9.14-09.

Niepewności/wyłączenia: Nie dorabiać pomiaru odległości na nieznanej mapie.

### EXP-014

Źródło i zatwierdzony zakres: Leader stackedwithRampagingEL travelswithit. At end leadercasualty4.73; survivor stayswhereELended. If ELoffmap bothELandleader eliminated, not survival inferred fromcasualtyDR.

Oba wyniki: R914: leader podróżuje z EL; na końcu casualty 4.73, survivor zostaje na końcowym heksie. Offmap eliminuje obu, odrębnie od survival placement. Nie podano wyniku casualty DR z nieobecnego źródła.

Dowody: PDF 32 right, C-9.14-10.

Niepewności/wyłączenia: Wynik casualty wymaga 4.73; nie wyliczać prawdopodobieństwa bez celu.

### EXP-015

Źródło i zatwierdzony zakres: Cavalry cannot voluntarily enterenemyELZOC; enteringeach enemyELFlank/Rearhex incurs2CH, samepenaltyforforcedentryELZOC; no cavalryattackenemyELFront; Flank/Rearattack doesnotgainusualAS. Nofullpositiveattackpermission.

Oba wyniki: R915: zakaz voluntary enemy EL ZOC, 2 CH za każdy Flank/Rear hex i przy forced ZOC entry; Front attack zakazany, Flank/Rear nie daje zwykłego AS. Pozwolenie lokalne nie potwierdza pełnej legalności ataku bez bazowego kontekstu.

Dowody: PDF 33 left, C-9.15-01.

Niepewności/wyłączenia: Wyliczenie geometrii ZOC i bazowego Shock wymaga reguł ogólnych.

### EXP-016

Źródło i zatwierdzony zakres: Ordinary EL moving from nonadjacent to adjacent enemy cavalry forces an OW attempt. If cavalry can withdraw, no Reaction Fire; otherwise immediate TQ check, and routed cavalry eliminates without DR in the supplied cannot-withdraw branch. Leader EL excluded. Arithmetic belongs to EXP-017.

Oba wyniki: R916: wejście z nonadjacent do adjacent, obligatory OW attempt; jeśli można odejść brak Reaction Fire, jeśli nie można immediate TQ, routed cavalry eliminuje bez DR. Leader EL wyłączony w exceptions. Zakres minimum należy do EXP-017. E916 urywa cytat wyjątku; semantyczne podparcie pochodzi z pełnego regionu PDF33, a lokator nadal błędny.

Dowody: PDF 33 left, C-9.16-01.

Niepewności/wyłączenia: OW i ustalenie możliwości withdrawal wymagają kontekstu; zakres minimum dla DR≤TQ osobno.

### EXP-018

Źródło i zatwierdzony zakres: ELvsEL neither side PositionSuperiority, including no positionalASfromFlank/Rear; notallpossibletypesofsuperiorityexcluded.

Oba wyniki: R917 zawiera zakaz Position Superiority dla EL vs EL oraz pozycyjnego AS z Flank/Rear. Nie zawiera zakazu wszystkich rodzajów superiority. Pole o AS należy czytać wraz z zakresem Position Superiority; pełne ogólne procedury pozostają poza oceną.

Dowody: PDF 33 left, C-9.17-01.

Niepewności/wyłączenia: Nie rozszerzać zakazu na wszystkie rodzaje superiority.

### EXP-020

Źródło i zatwierdzony zakres: WhenIndianELfightAfricanEL:AfricanEL+1PreShockDRM, inadditiontoClashofSpearsandSwords andShockSuperiority notes; notIndian+1norallEL+1norwaiveroftablenotes.

Oba wyniki: R919.conditions: Indian vs African; +1 Pre-Shock wyłącznie African, dodatkowo do not Clash/SS. Nie przeniesiono DRM na Indian lub wszystkie EL; nie pominięto not przez ogólne zwolnienie.

Dowody: PDF 33 left, C-9.19-01.

Niepewności/wyłączenia: Clash of Spears and Swords, Shock Superiority oraz 8.43 wymagają źródeł do pełnego Shock.

### EXP-021

Źródło i zatwierdzony zakres: Velites are LI, not SK; SK exceptions do not transfer by similarity. SK OW incurs Hits only via Rear; Velites via Flank or Rear. OW distance/MA condition belongs to EXP-022.

Oba wyniki: R92note: Velites to LI, nie SK. R921: OW Hits dla SK tylko Rear, Velites Flank/Rear. Nie przeniesiono wszystkich wyjątków SK na Velites. Historyczna nota ma operatywny fragment N-07-S2; pozostała historia poza gold.

Dowody: PDF 33 right, N-07-S2, PDF 33 right, C-9.21-01.

Niepewności/wyłączenia: Added maneuver nie definiuje wszystkich uprawnień; procedura OW pozostaje zewnętrzna.

### EXP-022

Źródło i zatwierdzony zakres: SK may OW up to 2 hexes before an approaching unit with MA equal to or less than SK MA. OW angle costs belong to EXP-021; real routes remain context-dependent.

Oba wyniki: R921.conditions i parameters zachowują approaching MA<=SK MA oraz maksimum 2 hexów. action_effect powtarza źródłowe regardless of MA differential; trzeba je czytać w tym warunku, nie jako zniesienie <=. Pełna trasa i kąt OW są osobne. Sama fraza regardless nie jest błędem odczytu.

Dowody: PDF 33 right, C-9.21-01.

Niepewności/wyłączenia: Pełna trasa OW wymaga procedury, mapy i danych.

### EXP-023

Źródło i zatwierdzony zakres: targetSKMissile+2DRM;SK/LIArchersA noH&D;LCanymissileclass noH&DvsSK

Oba wyniki: R922: target SK +2 Missile DRM; SK/LI Archers Class A nie H&D; LC każdego missile class nie H&D przeciw SK. Te zakazy nie ustalają pełnego lookupu MRRC lub reszty procedury.

Dowody: PDF 33 right, C-9.22-01.

Niepewności/wyłączenia: Wynik ognia wymaga MRRC i H&D; brak zakazu nie dowodzi pełnej legalności.

### EXP-024

Źródło i zatwierdzony zakres: SK cannot Shock attack; units attacking a defense consisting only of SK are exempt from Pre-Shock TQ even with the marker. With mixed defense use the other type and ignore SK Size. This owns the attacker exemption; EXP-004 owns the final Pass-Thru check.

Oba wyniki: R923: SK nie Shock attack; atakujący SK alone nie Pre-Shock nawet z markerem; mixed defense wybiera other type i pomija SK Size. Wyjątek końcowego Pass-Thru należy do EXP-004, nie do tego zwolnienia. Nowa DCTX923-S4 ma osobny pending.

Dowody: PDF 33 right, C-9.23-02, PDF 33 right, C-9.23-03, PDF 33 right, C-9.23-04.

Niepewności/wyłączenia: Nie przypisywać SK immunitetu od innych testów ani obrońcy mieszanego.

### EXP-025

Źródło i zatwierdzony zakres: HitsinflictedbySKhalvefloor,cap1

Oba wyniki: R923.action/parameters: Hits zadane przez SK pół, floor, maksimum 1 CH. W context-01 Step 4 dostarcza stronę atakującego przy obrońcy SK, lecz nie zmienia lokalnej treści R923. Nowa relacja i pełne applicability/base/CRT/order pozostają poza tą oceną.

Dowody: PDF 33 right, C-9.23-05.

Niepewności/wyłączenia: Bazowe Hits muszą być podane; kolejność innych modyfikatorów wymaga kontekstu.

## Pozostałe trzy zakresy — osobne decyzje

**EXP-010:** rzeczywisty kierunek dla 1–6 wymaga kompasu mapy. N914diagram nie ustala kierunku dla każdej bitwy, D914compass/G-D914compass blocking=true. Propozycja: poprawnie zaznaczony brak źródła rzeczywistego kierunku; nie jest blokadą syntetycznej podanej trasy. Nie przyjmujemy pełnych liczb z żetonu.

**EXP-017 / SEM-001:** oba wyniki nadal nie rozstrzygają DR<=TQ mimo przyjętego w eval-v1 0 CH. Wcześniejszy [pakiet](../focus-01.md) i pytanie pozostają pending. Nie włączono do listy 22 zakresów.

**EXP-019 / SEM-009:** źródło 9.18: „Unless the rules specifically state otherwise, Elephant units may be commanded by any leader.” R918 zachowuje literalny cytat i exceptions=unknown, ale interpretation/action_effect mówi Any leader may command; D918specific.blocks_full_result=false oraz G-D918specific.blocking=false w obu wynikach.

Propozycja Codex: znana reguła ogólna zachowana, ale brak jawnej blokady rzeczywistego użycia przy nieznanych wyjątkach. Czy jest to brak wymaganej blokady, czy unknown exceptions wystarcza — rozstrzyga właściciel. Nie wskazano konkretnego dowódcy ani wyniku sytuacji, nie oceniono rodzaju relacji jako TP/FP.

## Źródła do sprawdzenia

- [PDF31 core right](../../../inputs/v1/regions/pdf-31-core-right.png): Pass-Thru eligibility, +1 i hit adjustments.
- [PDF32 core left](../../../inputs/v1/regions/pdf-32-core-left.png): Pass-Thru 3/4, Screen, Riders, pierwsza część tabeli.
- [PDF32 core right](../../../inputs/v1/regions/pdf-32-core-right.png): 7–9 i Leader exception, Rampage, przykład kompasu.
- [PDF33 core left](../../../inputs/v1/regions/pdf-33-core-left.png): dokończenie Rampage, 9.15–9.19.
- [PDF33 core right](../../../inputs/v1/regions/pdf-33-core-right.png): Velites, 9.21–9.23, wyjątek Pass-Thru.

21 propozycji zgodności + jedna z błędem lokatora nie są jeszcze 22 zaakceptowanymi grupami. 42 pozycje inwentarza i 88 par rubryka/EXP otrzymały dokładne powiązania; nie zamknięto ich pełnych zakresów. Pozostałe 49 oczekiwań, granice glifów i wszystkie relacje pozostają pending.
