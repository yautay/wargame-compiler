# Przegląd właściciela — EXP-026–050

Tylko nowe, dokładne zakresy poniżej. Poprzednie 22 akceptacje nie przenoszą się na inne klauzule tych samych reguł. Pełna transkrypcja, pola i ślady bajtów: [review.md](review.md) i [comparisons.json](comparisons.json).

first-001 `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`; context-01 `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`; eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`.

## Propozycja akceptacji 21 zakresów lokalnych i 2 wymagań źródła

Lokalne: EXP-026–030, EXP-032, EXP-034–039, EXP-041–049. Wymagania/blokady źródła: EXP-031 i EXP-033. Wyłączone: EXP-040 i EXP-050 oraz rozstrzygnięcia SEM-002/003/009/010. Akceptacja nie obejmuje całych rekordów, aliasów, ratingów grafik, relacji, sytuacji ani finalnych wyników zależnych od brakującego źródła.

### EXP-026

Zatwierdzony zakres: PH/HI/LGdefendingFrontvsLI noPreShockevenwithattackermarker;LIstillcheck;reverseexemptionnotapplied

Oba wyniki / różnice: R923: PH/HI/LG broniące przez Front przed LI nie robią Pre-Shock nawet z markerem atakującego; LI nadal sprawdza. Reverse wyraźnie nie zachodzi. Nie rozszerzono na Flank/Rear lub inne typy.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 33 right, C-9.23-06.

Niepewności/wyłączenia: Nie rozszerzać na Flank/Rear ani inne typy.

### EXP-027

Zatwierdzony zakres: SKRouteliminated,facing0MP,no repeat-moveCohesioncost;no blanketterrain/stackingimmunity

Oba wyniki / różnice: R924: SK Rout oznacza eliminację, facing kosztuje 0 MP, ponowne ruchy w Game Turn bez Cohesion cost. Nie ma ogólnego zwolnienia z kosztów terenu i stacking.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 33 right, C-9.24-02, PDF 33 right, C-9.24-04.

Niepewności/wyłączenia: Koszty terenu i pełny stacking nie są wyłączone.

### EXP-028

Zatwierdzony zakres: oneSK/Velitespergap,notoneglobal;two consecutiveunits do notqualify

Oba wyniki / różnice: R924 i N924ex pokazują pojedynczą przerwę na gap, z możliwością oddzielnych powtórzeń. Dwa kolejne Velites w przykładzie nie tworzą line. Literalne układy 2808/2809/2810/2811/2812 zachowane; nie przyznano pełnej legalności 4.32.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 33 right, C-9.24-05, PDF 34 left, C-9.24-05, PDF 34 left, X-03.

Niepewności/wyłączenia: To lokalny wyjątek; pozostałe warunki 4.32 wymagają kontekstu.

### EXP-029

Zatwierdzony zakres: LCMissileH&DstrictlowerMA,exceptSK;LCArchersfireOW via6.55;fullproceduresunknown

Oba wyniki / różnice: R931: missile-armed LC, target strictly lower MA (<, nie <=), wyjątek SK; LC Archers fire podczas OW według 6.55. G-D931HD/OW zatrzymują pełne procedury, nie znany warunek lokalny.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 left, C-9.31-01.

Niepewności/wyłączenia: Sama przewaga MA nie domyka H&D; konieczna procedura 8.3.

### EXP-030

Zatwierdzony zakres: attackingLCHitsvsPH/HI/MI/LG/BI halvefloor

Oba wyniki / różnice: Lokalne R932.action_effect/parameters w obu wynikach zachowują pół/floor Hits zadanych przez atakujące LC PH/HI/MI/LG/BI. context-01 zmienia interpretation/exceptions, lecz nie literalną lokalną transkrypcję ani parametr. Ta propozycja nie akceptuje nowych operatorów/wyjątku Routed, całej R932, relacji ani kolejności AS/LC; SEM-003 nadal pending.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 left, C-9.32-01.

Niepewności/wyłączenia: Zależność od AS w przykładzie X-04 wymaga osobnej interpretacji/kontekstu.

### EXP-031

Zatwierdzony zakres: AS/halvingprintedresultconflict requirescontext;no newexceptioninvented

Oba wyniki / różnice: first-001 zachowuje literalny printed-result przykład i unknown interpretację; G932/G-D932CRT blocking. context-01 dodaje źródłowe kwalifikacje AS/LC/Routed, ale N932ex nadal unknown i GCTX-order/CRT/applicability/845 blocking. Propozycja: właściwe zachowanie nierozstrzygnięcia pełnego przykładu i potrzeby kontekstu; źródłowa poprawność samych nowych operatorów pozostaje osobnym SEM-003, bez założenia automatycznego znoszenia 2x i pół.

Propozycja: `source_block_supported`, właściciel pending.

Źródła: PDF 34 left, C-9.32-01, PDF 34 left, X-04.

Niepewności/wyłączenia: AS/LC printed result versus halving order and tables remain unresolved.; Ograniczony dowód bazowego AS/CRT; decyzja właściciela o kolejności.

### EXP-032

Zatwierdzony zakres: movingFrontPHDefense2Lperqualifyingflank,HI1Lperflank;excludestartadjacentstayed,FlankRear,anyPHattacker

Oba wyniki / różnice: R941.conditions: moves adjacent i Shock przez Front; po 2L na flank zajęty przez friendly PH lub w friendly PH ZOC, HI any Class 1L zamiast 2L. Wyłączenia: rozpoczęcie adjacent i pozostanie tam, Flank/Rear oraz jakikolwiek PH wśród atakujących. Brak CRT nie blokuje podanego lokalnego shiftu.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 left, C-9.41-01.

Niepewności/wyłączenia: Lokalny shift, nie pełny wynik CRT bez tabeli.

### EXP-033

Zatwierdzony zakres: scenarioDDeligibilitylistnecessary,missingblocksSIT11

Oba wyniki / różnice: R95note/N95design zachowują operatywny wymóg scenario-specific eligible units, R951 warunek eligible. G-D95scenario blocking=true, brak listy nie zastąpiony zgodą dla wszystkich PH. N953ex to jedynie odesłanie do przykładu; jego nonblocking nie zamyka krytycznej listy eligibility. Nie oceniono SIT-11.

Propozycja: `source_block_supported`, właściciel pending.

Źródła: PDF 34 right, N-09-S2, PDF 34 right, C-9.51-01, PDF 34 right, X-06.

Niepewności/wyłączenia: Scenario-specific Double-Depth eligibility list is required.; Wybrany scenariusz z listą uprawnionych jednostek.

### EXP-034

Zatwierdzony zakres: formingDDIOorLCdirectOC,backstartsbehindfront,terraincost+1MP,backunderfront,endbothmovementthisphase

Oba wyniki / różnice: R951: IO albo LC bezpośrednio od OC, back PH startuje bezpośrednio za front, płaci terrain+1 MP, trafia pod front; kończy ruch obu w tej Orders Phase. Nie ustalono realnej eligibility, OC ani kosztu terenu.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 right, C-9.51-01.

Niepewności/wyłączenia: Eligibility, OC i koszt terenu jako osobne potrzebne fakty.

### EXP-035

Zatwierdzony zakres: OCordersonly,2IOwhenIOmovement,PAWvia6.8,noWheel/Reverse/Column;unstacktopmoves,bottomstays,IOorLCasabove;fullLCprocedure notclosed

Oba wyniki / różnice: R952: rozkazy tylko OC; 2 IO przy ruchu w trybie IO, PAW 6.8, no Wheel/Reverse/Column. Unstack IO lub LC as above, top rusza za normalny koszt, bottom zostaje. R951 i pierwszy warunek OC zachowują zakres as above; nie domknięto pełnej procedury LC lub PAW.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 right, C-9.52-02, PDF 34 right, C-9.52-03, PDF 34 right, C-9.52-04.

Niepewności/wyłączenia: Procedury zewnętrzne 6.8/6.44/6.45/6.7 i orders pozostają potrzebne dla pełnego wykonania.

### EXP-036

Zatwierdzony zakres: readyDDMA4never5,movementHittoeach,nounitthroughorintoreadyDD;forming9.51separate

Oba wyniki / różnice: R952 dla units in DD: zawsze MA4, nigdy MA5; movement CH do każdej, zakaz wejścia/przejścia jakiegokolwiek unit przez gotowy DD. R951 osobno reprezentuje etap formowania, zanim gotowy stack istnieje. Nie odczytano zakazu jako anulowania formowania.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 right, C-9.52-05, PDF 34 right, C-9.52-06.

Niepewności/wyłączenia: Przypadek formowania DD z 9.51 wymaga rozróżnienia etapu od gotowej formacji.

### EXP-037

Zatwierdzony zakres: combinedSize,topTQunlessRearthenbottom;otherchecksifselectedunitincursHits;actualTQvaluesunknown

Oba wyniki / różnice: R953: combine Sizes, TQ top, przy Rear bottom; jeśli wybrana do check jednostka dostaje jakiekolwiek Hits, druga również sprawdza. Unknown interpretacja końcowej eliminacji G953 nie uchyla jawnych wcześniejszych efektów; prawdziwe ratingi i pełny check nieustalone.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 right, C-9.53-02, PDF 34 right, C-9.53-03.

Niepewności/wyłączenia: Ogólny test TQ i inne modyfikatory poza lokalną selekcją wymagają celu.

### EXP-038

Zatwierdzony zakres: enemydefendingagainstDD+1PreShock,DDdefending-1;9.41conditionsstillapply

Oba wyniki / różnice: R953: przeciwnik broniący się przed DD +1 Pre-Shock; DD jako defender -1. R941 w mapowanym zakresie zachowuje warunki i wyłączenia Phalanx Defense, więc nie przyznano shiftu bezwarunkowo. Nie nadaje to formalnego TP krawędzi R953→R941.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 right, C-9.53-04, PDF 34 right, C-9.53-05, PDF 34 left, C-9.41-01.

Niepewności/wyłączenia: R-9.53→R-9.41 to użycie warunkowej modyfikacji, nie odwrotny kierunek.

### EXP-039

Zatwierdzony zakres: FlankReardefenderShockHits3xinstead2x,equalallocationoddtop;missileHits topunlessRearthenbottom

Oba wyniki / różnice: R953: Hits DD defender w Shock przez Flank/Rear 3x zamiast 2x; Shock rozdzielony równo, nieparzysty Hit do top. Missile do top z wyjątkiem Rear do bottom. Selekcja TQ przez Rear nie zmienia odd-Hit allocation Shock; baza i inne mnożniki pozostają poza zakresem.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 34 right, C-9.53-06, PDF 34 right, C-9.53-07.

Niepewności/wyłączenia: Bazowy wynik i kolejność wobec innych mnożników muszą być dostarczone/zweryfikowane.

### EXP-040

Zatwierdzony zakres: When one PH of DD Routs, both Rout and retreat separately. Eliminate each PH individually if it cannot complete legal Rout movement; the other may perform its own legal Rout if possible. Actual geometry, 6.69/10.22, order/shared sole destination and later D1 result are unclosed. Local 10.24/25/23 context is supporting evidence, not an additional scoring unit.

Oba wyniki / różnice: Oba R953 zachowują both rout i separate hexes, ale końcowe the unit pozostaje literalne; interpretation unknown/G953 blocking. Eval-v1 ma per-unit eliminację z możliwością legalnego Rout drugiej PH. Propozycja niepełnej reprezentacji tej lokalnej gałęzi pozostaje SEM-002 pending; osobno dostępność podparcia 10.24/25/23 dla ekstraktora i rzeczywista geometria/kolejność.

Propozycja: `incomplete_local_interpretation_pending_source_availability`, właściciel pending.

Źródła: PDF 34 right, C-9.53-08.

Niepewności/wyłączenia: Per-unit elimination reading is confirmed; real geometry, 6.69/10.22, legal ordering and a shared sole destination remain unresolved.; Legalne heksy retreat i zakres końcowego the unit wymagają kontekstu przy konfliktach.

### EXP-041

Zatwierdzony zakres: ruleofthumb2Romaninfantry sameborderwithexceptions;notfulllegaleligibility;move2IO,1IOifstackedOCgivingorders,1LCifbotheligible

Oba wyniki / różnice: R961: rule of thumb dwóch Roman infantry tego samego border color, z wyjątkami jak Velites. Nie pełne eligibility. Joint move 2 IO; 1 IO tylko z OC w stack dającym rozkazy; 1 LC tylko jeśli obie eligible. Odesłania do charts/line nie zamykają pełnych procedur.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 left, C-9.61-01.

Niepewności/wyłączenia: Pełny stacking chart i eligibility nie są dowiedzione regułą thumb.

### EXP-042

Zatwierdzony zakres: combineSize,otherratingsespeciallyTQtop,eachunitowntestusingtopTQ,onlytopfire,bothShock samehex;automaticHitsto each;Shockallocationdelegated8.46Step4/10.13

Oba wyniki / różnice: R962: combine Size, inne ratingi w tym TQ top; własny check każdej z top TQ; tylko top Missile Fire, obie Shock tego samego hex; Automatic Hits do każdej. Shock alokacja delegated 8.46 Step4/10.13. R962 jest niezmieniona; context D962shock dostało endpoint, lecz G-D962shock nadal blocking, dalej brak 6.68 #6. Lokalna reprezentacja nie zamyka alokacji ani nie nadaje TP.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 left, C-9.62-01.

Niepewności/wyłączenia: Rozdział 9 nie domyka alokacji Shock Hits; 10.13 jest kontekstem, 6.68 nieprzejrzane.

### EXP-043

Zatwierdzony zakres: differentbordercolors ORsamecolordifferentclasses,+1DRMtoallTQchecks

Oba wyniki / różnice: R963 zachowuje OR: różne border colors lub ten sam color i różne classes. +1 DRM do wszystkich TQ checks, bez zastąpienia OR przez AND. Faktyczne kolory i klasy wymagają danych.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 left, C-9.63-01.

Niepewności/wyłączenia: Typy i kolory muszą być znane z danych jednostek.

### EXP-044

Zatwierdzony zakres: stackorderchangeIOonly,notmovement/LC;facingcanLC;onlytopmovesifmovingoneunitfromstack

Oba wyniki / różnice: R964: zamiana kolejności stack tylko IO, nie część movement ani LC; facing może LC. Przy ruchu jednej jednostki z stacku rusza tylko top. Nie rozszerzono zwykłego unstack na szczególne MLE.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 left, C-9.64-01.

Niepewności/wyłączenia: Nie zastosować zwykłego unstack do MLE bez sprawdzenia szczególnej reguły.

### EXP-045

Zatwierdzony zakres: Romaninfantryfacing1MPanynumbervertices;notMLEfacingrule

Oba wyniki / różnice: R965: Roman infantry 1 MP za facing dowolnej liczby vertices, nie koszt za każdy vertex. Nie przeniesiono tej operacji na MLE, które zachowuje facing.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 left, C-9.65-01.

Niepewności/wyłączenia: Nie rozszerzać tej wartości na MLE, które zachowuje facing.

### EXP-046

Zatwierdzony zakres: topunits instackssameLine sideways tovacantflankClearoutsideenemyZOC,facingunchanged;unstackonly,notstackingTogether;diagramOriginaltop/Afterbottomillustrative

Oba wyniki / różnice: R966: top units w stackach tej samej Line, sideways do vacant flank; Clear i poza enemy ZOC, facing bez zmiany; wyłącznie unstack, nie stacking together. N966diagram zachowuje Original Deployment u góry, After MLE u dołu jako ilustrację. Nie akceptujemy małych ratingów, identyfikacji front/back konkretnych counterów ani ogólnego prawa do dowolnej strony z samej grafiki.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 left, C-9.66-01-S1, PDF 35 right, C-9.66-01-S1, PDF 35 left, C-9.66-01-S2, PDF 35 right, C-9.66-01-S2, PDF 35 left, C-9.66-01-S3, PDF 35 right, C-9.66-01-S3, PDF 35 left, C-9.66-01-S4, PDF 35 right, C-9.66-01-S4, PDF 35 left, C-9.66-01-S5, PDF 35 right, C-9.66-01-S5, PDF 35 left, C-9.66-01-S6, PDF 35 right, C-9.66-01-S6, PDF 35 left, D-02, PDF 35 left, CAP-01, PDF 35 left, CAP-02.

Niepewności/wyłączenia: Same Line przez4.32, Clear i ZOC wymagają danych/procedur; grafika nie daje ogólnego prawa do dowolnej strony.

### EXP-047

Zatwierdzony zakres: reactiontriggerenemycombatwithin2hexes,line;maydeclinefirstopportunitywithoutlosinglatertriggers;OW/MLEdifferentunitscanwithvalidtriggers,sameunitscannotboth

Oba wyniki / różnice: R967: reakcja w instant approach enemy combat within 2 hexes of stacked Roman line; wolno odroczyć pierwszą okazję do następnego kwalifikowanego triggeru. OW/MLE razem tylko przez różne jednostki z właściwymi triggerami, nie te same. N967ex zachowuje przykład Velites OW i Hastati MLE.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 right, C-9.67-01, PDF 35 right, X-07.

Niepewności/wyłączenia: OW i legalność line muszą być ustalone oddzielnie.

### EXP-048

Zatwierdzony zakres: activeMLELC-only,bothunitsmaymoveafterwithMA-2,noCHforMLE;ColumnunitsnoMLE;noautomatictransferofLCpostmovepermissiontoreaction

Oba wyniki / różnice: R968 wyraźnie kwalifikuje post-MLE move przez When by LC: obie jednostki mogą ruszyć z MA-2. LC-only dla aktywnego MLE, 0 CH za samo MLE i zakaz Column. Nie przeniesiono uprawnienia dalszego ruchu na tryb reakcyjny R967.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 right, C-9.68-01.

Niepewności/wyłączenia: Nie przenosić automatycznie post-MLE ruchu na tryb reakcyjny.

### EXP-049

Zatwierdzony zakres: Romansprior200BCE,ScipioAfricanusnotOC;Cannaeexplicitusepergameinstruction,notnewhistoricalinference;C9.7S2explanatory

Oba wyniki / różnice: R97intro: obowiązek dla Romans przed 200 BCE i bez Scipio Africanus jako OC; Cannae jawnie objęte instrukcją gry, nie historycznym wnioskowaniem. Parametr jest prior to 200, nie <=200. Explanatory C9.7-S2 nie stanowi dodatkowego obowiązku.

Propozycja: `supported_local_scope`, właściciel pending.

Źródła: PDF 35 right, C-9.7-01-S1.

Niepewności/wyłączenia: W realnym scenariuszu data i tożsamość OC wymagają dowodów.

### EXP-050

Zatwierdzony zakres: realbattlewithoutdate/OC/AWL notresolved,requires_context

Oba wyniki / różnice: Obie odpowiedzi podają predykaty daty/OC i warunki Triarii, nie rzeczywiste dane wybranej bitwy. AWL/RP/LOS/ZOC mają jawne blocking gaps; brak osobnych deklaracji źródła rzeczywistej daty i OC w R97intro.gap_ids (pusta lista). SEM-010: wystarczalność tego opisu needs-context wymaga właściciela. Nie jest to dowód fikcyjnego wybrania dowódcy/daty; known na conditions oznacza znany warunek, nie spełniony fakt. Nie oceniono SIT.

Propozycja: `partial_context_declaration_pending`, właściciel pending.

Źródła: PDF 35 right, C-9.7-01-S1, PDF 35 right, C-9.71-01, PDF 35 right, C-9.72-01.

Niepewności/wyłączenia: Actual battle date, Overall Commander, AWL and scenario facts are required.; Konkretny scenariusz, OC, AWL/RP i stan mapy.

## SEM-010 — potrzeba rzeczywistej daty i OC

R97intro.conditions zachowuje znane predykaty daty/OC. R97intro.gap_ids jest puste; R972/AWL/RP i R971/LOS są jawnie blocking. Nie ma konkretnego przypadku z nieprawdziwą datą/dowódcą ani pełnym wynikiem. Właściciel rozstrzyga, czy jawność AWL/RP i warunków wystarcza, czy potrzeba osobnej deklaracji braku źródła rzeczywistej daty/OC. Nie traktować known-predicate jako spełnionego real-faktu.

## Obrazy źródła

- [PDF33 right](../../../inputs/v1/regions/pdf-33-core-right.png): klauzule SK/LI.
- [PDF34 left](../../../inputs/v1/regions/pdf-34-core-left.png): przykład Line, LC i Phalanx Defense.
- [PDF34 right](../../../inputs/v1/regions/pdf-34-core-right.png): Double Depth.
- [PDF35 left](../../../inputs/v1/regions/pdf-35-core-left.png): Roman stack i diagram.
- [PDF35 right](../../../inputs/v1/regions/pdf-35-core-right.png): MLE i Triarii.
- [Step 4](../../../context/pass-01/evidence/8.46-step-4-pdf-27.png): ograniczony kontekst AS/LC i odesłanie alokacji.

E916, 64 granice glifów, wszystkie krawędzie, rzeczywisty setup i 20 sytuacji pozostają wyłączone. Żadnych nowych źródeł lub korekt; następna część .4 ma EXP-051–074 i pozostały inwentarz/relacje/lokatory.
