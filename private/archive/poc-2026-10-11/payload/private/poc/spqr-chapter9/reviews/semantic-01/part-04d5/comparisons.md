# M-POC5A.4d5 — końcowe uzgodnienie zakresów

Uzgodniono207 pozycji/414 wcześniejszych ocen inwentarza,74 oczekiwania w obu odpowiedziach,277 par rubryki,257 zakresów relacji,124 lokatorów i13 starych kwestii. To oddzielne osie, nie sumowane punkty reguł. Każdy wcześniejszy zakres zachowuje swoją decyzję; nowa akceptacja dotyczy tylko raportu uzgodnienia.

Pełne źródła, oryginalne pola i bajty: [comparisons.json](comparisons.json).

## Wszystkie74 oczekiwania

### EXP-001 — confirmed_local_content_scope

In the reviewed supplied case, Pass-Thru is allowed with LI defending Front, EL marker, no co-attacker, no initial enemy ZOC, a free Rear and an early decision. Initial enemy ZOC excludes it despite later exit. With two defenders both must meet the earlier conditions.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Pełny Shock i definicje Front/Rear/ZOC są celami zewnętrznymi; nie wyliczać ich z tego akapitu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911.conditions: Front, marker, wolny Rear; exceptions: Flank/Rear, współatak i ZOC na początku Orders Phase. time_limits zachowuje decyzję przed DR i początkowy ZOC. Obie jednostki muszą spełniać warunki. Nie wyliczamy geometrii ZOC.

R911: `/rules/0`, bajty[171012,179988); SHA `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911.conditions: Front, marker, wolny Rear; exceptions: Flank/Rear, współatak i ZOC na początku Orders Phase. time_limits zachowuje decyzję przed DR i początkowy ZOC. Obie jednostki muszą spełniać warunki. Nie wyliczamy geometrii ZOC.

R911: `/rules/0`, bajty[236824,246111); SHA `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

### EXP-002 — confirmed_local_content_scope

For the reviewed supplied Pass-Thru result, defender Pre-Shock +1 DRM; infantry Hits 5 become 2 and EL Hits 3 become 2. Base-0 reduction floor and other modifier order remain unresolved.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Base EL Hits=0 reduction floor/order remains unresolved; do not infer a negative result or minimum.; Bazowy wynik Shock musi być dostarczony; kolejność innych modyfikatorów i dolna granica redukcji EL do przeglądu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911 action_effect/parameters zachowują Pre-Shock +1 DRM, pół/floor Hits obrońcy i -1 Hits EL. Są to operatory zgodne z zatwierdzonym zakresem 5→2 oraz 3→2; nie dopisano dolnej granicy dla bazowego 0 ani kolejności innych modyfikatorów. Nie oceniono SIT.

R911: `/rules/0`, bajty[171012,179988); SHA `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911 action_effect/parameters zachowują Pre-Shock +1 DRM, pół/floor Hits obrońcy i -1 Hits EL. Są to operatory zgodne z zatwierdzonym zakresem 5→2 oraz 3→2; nie dopisano dolnej granicy dla bazowego 0 ani kolejności innych modyfikatorów. Nie oceniono SIT.

R911: `/rules/0`, bajty[236824,246111); SHA `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

### EXP-003 — confirmed_local_content_scope

After supplied no-infantry-Rout and no-EL-Rampage outcomes, place EL in a free defender Rear hex chosen by the EL player, keeping facing. No complete Shock result inferred.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Stan Rout wymaga procedury ogólnej; Rampage ma wewnętrzny cel R-9.14.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911 action_effect krok 3: po Shock, tylko gdy piechota nie Rout i EL nie Rampage; wolny Rear wybiera gracz EL, facing zachowane. Nie zastępuje to pełnego wyniku Shock.

R911: `/rules/0`, bajty[171012,179988); SHA `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911 action_effect krok 3: po Shock, tylko gdy piechota nie Rout i EL nie Rampage; wolny Rear wybiera gracz EL, facing zachowane. Nie zastępuje to pełnego wyniku Shock.

R911: `/rules/0`, bajty[236824,246111); SHA `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

### EXP-004 — confirmed_local_content_scope

The final Pass-Thru TQ check is separate from Pre-Shock; SK are exempt from that final check. For non-SK, positive DR-TQ gives Hits; DR<=TQ gives no excess. No minimum imported from 9.16.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie rozszerzać wyjątku na wszystkie testy TQ.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911 rozdziela końcowy Pass-Thru TQ od Pre-Shock, wyłącza SK z kroku 4 i nalicza tylko positive excess DR-TQ. R924 powtarza wyłączenie SK. Parametr positive excess nie importuje minimum 1 z 9.16; brak konkretnej liczby nie jest pominięciem operatora.

R911: `/rules/0`, bajty[171012,179988); SHA `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.
R924: `/rules/14`, bajty[249766,255895); SHA `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R911 rozdziela końcowy Pass-Thru TQ od Pre-Shock, wyłącza SK z kroku 4 i nalicza tylko positive excess DR-TQ. R924 powtarza wyłączenie SK. Parametr positive excess nie importuje minimum 1 z 9.16; brak konkretnej liczby nie jest pominięciem operatora.

R911: `/rules/0`, bajty[236824,246111); SHA `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.
R924: `/rules/14`, bajty[318324,324673); SHA `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

### EXP-005 — confirmed_local_content_scope

Elephant Screen uses the explicitly named Elephant Screen MRRC row and fires only as Reaction Fire, has its own supply markers, and is absent on Leader Elephant. Actual lookup and supply procedure remain context requirements.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Pełny wynik ognia wymaga 8.2 i wiersza MRRC.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R912: Reaction Fire only, nazwany Elephant Screen MRRC row, własne supply markers i brak screen u Leader Elephant. Nie ma podstaw do wartości pełnego lookupu lub domknięcia supply.

R912: `/rules/1`, bajty[179994,184187); SHA `3f41d13d808d94b10acd6b9c50291e48c421110a1cbd8ade5b4005da89db6f2b`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R912: Reaction Fire only, nazwany Elephant Screen MRRC row, własne supply markers i brak screen u Leader Elephant. Nie ma podstaw do wartości pełnego lookupu lub domknięcia supply.

R912: `/rules/1`, bajty[246118,250457); SHA `7f308d008537d03c5e4e9cefca02e958fd41bf37b65dc395a998895b28c401f2`.

### EXP-006 — confirmed_local_content_scope

RidersasMountedJavelinists,separatejavelin/screenDR,N03-S2nochangefromhistoricaltowerabsence

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Tożsamość wiersza MRRC z samego Mounted Javelinists pozostaje hipotezą DC-031.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R913: Mounted Javelinists dla Missile Fire; javeliny/screen mają osobne DR. R913note: historyczny brak wież nie zmienia reguły. Nie utożsamiono niepotwierdzonych aliasów wiersza MRRC.

R913: `/rules/2`, bajty[184193,187922); SHA `6ae8731a79d93d63ac442f6c3ebbb060431519b68ea15f099061e09e89710ac9`.
R913note: `/rules/3`, bajty[187928,191195); SHA `daa665c7c08f5cc4d8bbd84d94483163762c15694e230b680f9e8355f85d3b61`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R913: Mounted Javelinists dla Missile Fire; javeliny/screen mają osobne DR. R913note: historyczny brak wież nie zmienia reguły. Nie utożsamiono niepotwierdzonych aliasów wiersza MRRC.

R913: `/rules/2`, bajty[250464,254326); SHA `cf0f58a2d98a672e77cf653d796bf33730b38d13e2613a8516a04a57e224b290`.
R913note: `/rules/3`, bajty[254333,257716); SHA `6fc580e76f219adc2a6ee990c85c9387c2ded93be6d55b5f79a548ec7c5782f5`.

### EXP-007 — confirmed_local_content_scope

Ordinary EL Rout triggers immediate Rampage procedure. Ordinary EL roll 0 heads toward nearest friendly unit with opponent choosing a tie; first 7-9 moves away from cause, subsequent 7-9 eliminates. Concrete map and cause are not invented.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Kierunku na rzeczywistej mapie nie ustala sam przykład D-01.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914 i N914table zachowują immediate Rout→Rampage; zwykły EL: 0 do najbliższej friendly, remis wybiera przeciwnik; pierwsze 7–9 od przyczyny, późniejsze 7–9 eliminacja. first/subsequent jest jawne w wierszu tabeli. Rzeczywisty kierunek nie został ustalony.

N914table: `/nodes/0`, bajty[120024,122102); SHA `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.
R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914 i N914table zachowują immediate Rout→Rampage; zwykły EL: 0 do najbliższej friendly, remis wybiera przeciwnik; pierwsze 7–9 od przyczyny, późniejsze 7–9 eliminacja. first/subsequent jest jawne w wierszu tabeli. Rzeczywisty kierunek nie został ustalony.

N914table: `/nodes/0`, bajty[167589,169718); SHA `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.
R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

### EXP-008 — confirmed_local_content_scope

Leader Elephant roll 0 eliminates it; subsequent 7-9 immediately rallies it with Hits=TQ-2 instead of elimination. This owns the subsequent-roll result; first Leader 7-9 is scored only in EXP-009.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Later7-9LeaderRally outcome andcriticality accepted; actualTQ and4.84counting notclosed. Firsttable7-9 addressedseparatelyEXP009.; Zakres Leader Elephant przy pierwszym 7–9 jest odrębnym nierozstrzygniętym oczekiwaniem.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

N914table: Leader 0 eliminuje; późniejsze 7–9 rally z Hits=TQ−2 zamiast eliminacji. R914.exceptions utrzymuje ten wyjątek wobec ogólnego zakazu rally. Pierwsze 7–9 nie daje drugiego punktu w EXP-008.

N914table: `/nodes/0`, bajty[120024,122102); SHA `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.
R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

N914table: Leader 0 eliminuje; późniejsze 7–9 rally z Hits=TQ−2 zamiast eliminacji. R914.exceptions utrzymuje ten wyjątek wobec ogólnego zakazu rally. Pierwsze 7–9 nie daje drugiego punktu w EXP-008.

N914table: `/nodes/0`, bajty[167589,169718); SHA `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.
R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

### EXP-009 — confirmed_local_content_scope

First Rampage-table 7-9 for Leader Elephant means movement away from the causing unit, without immediate special rally. Subsequent-roll result is referenced in EXP-008 and earns no second point here. Counting the 4.84 trigger die is unresolved.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; FirstLeader7-9interpretation andcriticality accepted;actualcause/map/route/TQ and4.84countingnotclosed.; Przegląd składni tabeli i uzasadniona decyzja właściciela.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

N914table rozdziela first Rampage DR od any subsequent: pierwsze Leader 7–9 prowadzi od przyczyny, nie do natychmiastowego rally. R914.exceptions ogranicza rally do subsequent. Nie określono zaliczania rzutu wyzwalającego 4.84.

N914table: `/nodes/0`, bajty[120024,122102); SHA `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.
R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

N914table rozdziela first Rampage DR od any subsequent: pierwsze Leader 7–9 prowadzi od przyczyny, nie do natychmiastowego rally. R914.exceptions ogranicza rally do subsequent. Nie określono zaliczania rzutu wyzwalającego 4.84.

N914table: `/nodes/0`, bajty[167589,169718); SHA `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.
R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

### EXP-010 — requires_context

1-6 uses actual battle map compass; missing compass blocks concrete direction/hexside.

Wiersz1–6 wymaga kompasu wybranej bitwy. Oba modele odróżniają diagram przykładowy od rzeczywistej mapy i deklarują blocking=true; brakujące realne źródło nadal pozostaje otwarte. Nie zamieniam przykładu roll1 w uniwersalny kierunek ani blokady realnej mapy w blokadę zadanej syntetycznej trasy.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; A real battle-map compass is required for a concrete direction/hexside.; Wskazana mapa bitwy z dowodem i kompasem, bez domknięcia całej instrukcji.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

N914diagram podaje illustrative example, użycie kompasu konkretnej bitwy i brak uniwersalnego kierunku geograficznego. D914compass/G-D914compass mają brak źródła i blocking=true. To blokada rzeczywistego kierunku, nie lokalnie podanej syntetycznej trasy.

N914diagram: `/nodes/1`, bajty[122108,123601); SHA `99553c9e8dd99e5d6630491e66a2f8303144f0c27ea52a45ac24b4b368166f4d`.
N914table: `/nodes/0`, bajty[120024,122102); SHA `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.
D914compass: `/dependencies/54`, bajty[459795,460817); SHA `2329eef178fde36656363601a0b0a8e0c12bd5ee1a33b15a6b1197b0e34d607e`.
G-D914compass: `/gaps/14`, bajty[535977,536514); SHA `4bda56919fefbc95954ea322fb5af5bea3f9a0e539c36dfc6e7ca2f8bec75c8d`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

N914diagram podaje illustrative example, użycie kompasu konkretnej bitwy i brak uniwersalnego kierunku geograficznego. D914compass/G-D914compass mają brak źródła i blocking=true. To blokada rzeczywistego kierunku, nie lokalnie podanej syntetycznej trasy.

N914diagram: `/nodes/1`, bajty[169725,171268); SHA `1365c92a4d04710676a2e125eb8e5f6adccbbcf43675f2725fb1db147361d934`.
N914table: `/nodes/0`, bajty[167589,169718); SHA `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.
D914compass: `/dependencies/54`, bajty[536513,537563); SHA `a6a4251c69eb2d2d05643f642fbb1e5ebf93486528dc7879d21a18040e6da46c`.
G-D914compass: `/gaps/14`, bajty[619959,620515); SHA `7f06c6d840f91c9e11ef9a94e541fc052df74c92e799572526b83b4978785600`.

### EXP-011 — confirmed_local_content_scope

Complete each Rampage immediately before any other mechanic except OW under 6.51; no concurrent Rampages. Rampaging EL has no ZOC, triggers no Reaction Fire of any kind, and normally cannot rally. The special later Leader result is a reference to EXP-008, not a second scored result.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; OW 6.51 wymaga zewnętrznej procedury; szczególny Leader Elephant zachować oddzielnie.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914: immediate i serial resolution, wyjątek OW; brak ZOC i Reaction Fire każdego rodzaju; no rally z osobnym wyjątkiem Leader w exceptions. C-9.14-11 przechodzi na PDF33 i kontynuacja źródła jest zachowana. Wyjątek jest referencją do EXP-008, bez drugiego punktu.

R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914: immediate i serial resolution, wyjątek OW; brak ZOC i Reaction Fire każdego rodzaju; no rally z osobnym wyjątkiem Leader w exceptions. C-9.14-11 przechodzi na PDF33 i kontynuacja źródła jest zachowana. Wyjątek jest referencją do EXP-008, bez drugiego punktu.

R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

### EXP-012 — confirmed_local_content_scope

Attempt 3 hexes per directional roll with supplied route/no early termination. At a would-be occupied hex stop adjacent; occupant gets 1 CH via Front, 2 via Flank/Rear, cavalry always 2. Both units of a stack get their Hits. A leader unable to withdraw under 4.72 dies without DR; actual inability requires context.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Możliwość withdrawal leadera wymaga 4.72; geometrię i typy przyjąć tylko jako jawne dane przypadku.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914 parametry/action: próba 3 hexów na directional DR; stop adjacent przed occupied hex; occupant 1 CH przez Front, 2 Flank/Rear, cavalry zawsze 2; oba elementy stacku Hits. Leader unable to withdraw według 4.72 ginie bez DR. Realnego warunku unable nie domknięto.

R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914 parametry/action: próba 3 hexów na directional DR; stop adjacent przed occupied hex; occupant 1 CH przez Front, 2 Flank/Rear, cavalry zawsze 2; oba elementy stacku Hits. Leader unable to withdraw według 4.72 ginie bez DR. Realnego warunku unable nie domknięto.

R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

### EXP-013 — confirmed_local_content_scope

Repeat until offmap, elimination(ordinaryEL7-9mahout), at least8hexes from nearest unit(any allegiance) causing elimination, or if none above eliminate after4th consecutive RampageDR.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie dorabiać pomiaru odległości na nieznanej mapie.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914: ponawianie do offmap/elimination, >=8 hexów od nearest unit i eliminacja po 4. consecutive DR, jeśli wcześniej nie zakończono. Wiersz tabeli i wyjątki nadal kwalifikują późniejsze 7–9 oraz Leader. Nie dodano realnego pomiaru mapy.

R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914: ponawianie do offmap/elimination, >=8 hexów od nearest unit i eliminacja po 4. consecutive DR, jeśli wcześniej nie zakończono. Wiersz tabeli i wyjątki nadal kwalifikują późniejsze 7–9 oraz Leader. Nie dodano realnego pomiaru mapy.

R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

### EXP-014 — confirmed_local_content_scope

Leader stackedwithRampagingEL travelswithit. At end leadercasualty4.73; survivor stayswhereELended. If ELoffmap bothELandleader eliminated, not survival inferred fromcasualtyDR.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Wynik casualty wymaga 4.73; nie wyliczać prawdopodobieństwa bez celu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914: leader podróżuje z EL; na końcu casualty 4.73, survivor zostaje na końcowym heksie. Offmap eliminuje obu, odrębnie od survival placement. Nie podano wyniku casualty DR z nieobecnego źródła.

R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R914: leader podróżuje z EL; na końcu casualty 4.73, survivor zostaje na końcowym heksie. Offmap eliminuje obu, odrębnie od survival placement. Nie podano wyniku casualty DR z nieobecnego źródła.

R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

### EXP-015 — confirmed_local_content_scope

Cavalry cannot voluntarily enterenemyELZOC; enteringeach enemyELFlank/Rearhex incurs2CH, samepenaltyforforcedentryELZOC; no cavalryattackenemyELFront; Flank/Rearattack doesnotgainusualAS. Nofullpositiveattackpermission.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Wyliczenie geometrii ZOC i bazowego Shock wymaga reguł ogólnych.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R915: zakaz voluntary enemy EL ZOC, 2 CH za każdy Flank/Rear hex i przy forced ZOC entry; Front attack zakazany, Flank/Rear nie daje zwykłego AS. Pozwolenie lokalne nie potwierdza pełnej legalności ataku bez bazowego kontekstu.

R915: `/rules/5`, bajty[210012,214748); SHA `e7a73035f7d9687d28f1dcb19e01d02be16cd4d325a249d7b7fc1b9a0dfaf226`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R915: zakaz voluntary enemy EL ZOC, 2 CH za każdy Flank/Rear hex i przy forced ZOC entry; Front attack zakazany, Flank/Rear nie daje zwykłego AS. Pozwolenie lokalne nie potwierdza pełnej legalności ataku bez bazowego kontekstu.

R915: `/rules/5`, bajty[277148,282047); SHA `cf617cf7b5c3ca2083c7fb23420fe52d8cc8d0f87cec79861f8fe21e3464ae8e`.

### EXP-016 — confirmed_local_content_scope

Ordinary EL moving from nonadjacent to adjacent enemy cavalry forces an OW attempt. If cavalry can withdraw, no Reaction Fire; otherwise immediate TQ check, and routed cavalry eliminates without DR in the supplied cannot-withdraw branch. Leader EL excluded. Arithmetic belongs to EXP-017.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; OW i ustalenie możliwości withdrawal wymagają kontekstu; zakres minimum dla DR≤TQ osobno.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R916: wejście z nonadjacent do adjacent, obligatory OW attempt; jeśli można odejść brak Reaction Fire, jeśli nie można immediate TQ, routed cavalry eliminuje bez DR. Leader EL wyłączony w exceptions. Zakres minimum należy do EXP-017. E916 urywa cytat wyjątku; semantyczne podparcie pochodzi z pełnego regionu PDF33, a lokator nadal błędny.

R916: `/rules/6`, bajty[214754,219957); SHA `7a3e47595d7018caed44c65c56be0fb9558e0a1a69c8c87522c6e82d1d719d49`.
E916: `/evidence/15`, bajty[28605,29597); SHA `9e4f30da57821c33dd930a08581e936b9990433103927de53462965fd0a0baf7`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R916: wejście z nonadjacent do adjacent, obligatory OW attempt; jeśli można odejść brak Reaction Fire, jeśli nie można immediate TQ, routed cavalry eliminuje bez DR. Leader EL wyłączony w exceptions. Zakres minimum należy do EXP-017. E916 urywa cytat wyjątku; semantyczne podparcie pochodzi z pełnego regionu PDF33, a lokator nadal błędny.

R916: `/rules/6`, bajty[282054,287456); SHA `24d2167ad17175100c6e004dadba05315767f139f2955cd85082f5ebf04f590a`.
E916: `/evidence/15`, bajty[64824,65845); SHA `b9ea1eb8048dde08eb59af663518460a7ac056c3419da5e46c58df1fdf78e4f8`.

### EXP-017 — confirmed_local_content_scope

W9.16 przy DR<=TQ kawaleria nie otrzymuje CH; przy DR>TQ otrzymuje DR-TQ CH, z minimum1. Minimum nie wyłącza warunku DR>TQ.

Warunek DR>TQ i minimum1 są zapisane, lecz interpretation unknown i G916 blocking pozostawiają gałąź DR<=TQ bez ustalonego wyniku. Przyjęty numer/wyjątek Leader Elephant/literalna klauzula ani decyzja o lokatorze nie rozstrzygają SEM-001. Wariant pozostaje do dawnej decyzji właściciela, bez nowego zawsze1CH.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; LocalDR<=TQ0CH/DR>TQdifference+min1 interpretation andcriticality accepted; nofullOW/cavalryprocedure or targetmetadata closure.; Właściciel rozstrzyga zakres minimum z tekstem lub wskazuje potrzebny dowód.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R916 zachowuje DR>TQ/difference/minimum 1, ale interpretation=unknown i G916.blocking pozostawiają DR<=TQ nierozstrzygnięte. Zatwierdzona lokalna gałąź 0 CH nie jest jednoznacznie reprezentowana jako ustalona. SEM-001 nadal czeka na decyzję właściciela; nie stwierdzono błędnej transkrypcji ani zawsze 1 CH.

R916: `/rules/6`, bajty[214754,219957); SHA `7a3e47595d7018caed44c65c56be0fb9558e0a1a69c8c87522c6e82d1d719d49`.
G916: `/gaps/0`, bajty[528984,529510); SHA `5ace56915486ab06bd226069e9c9402e84707a60d8700dfad4c22e4c0da8059c`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R916 zachowuje DR>TQ/difference/minimum 1, ale interpretation=unknown i G916.blocking pozostawiają DR<=TQ nierozstrzygnięte. Zatwierdzona lokalna gałąź 0 CH nie jest jednoznacznie reprezentowana jako ustalona. SEM-001 nadal czeka na decyzję właściciela; nie stwierdzono błędnej transkrypcji ani zawsze 1 CH.

R916: `/rules/6`, bajty[282054,287456); SHA `24d2167ad17175100c6e004dadba05315767f139f2955cd85082f5ebf04f590a`.
G916: `/gaps/0`, bajty[612466,613008); SHA `1149bf75c9e07c293ae890ad880b22c217a1da8ed02d6a180000371aa8fa8a56`.

### EXP-018 — confirmed_local_content_scope

ELvsEL neither side PositionSuperiority, including no positionalASfromFlank/Rear; notallpossibletypesofsuperiorityexcluded.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie rozszerzać zakazu na wszystkie rodzaje superiority.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R917 zawiera zakaz Position Superiority dla EL vs EL oraz pozycyjnego AS z Flank/Rear. Nie zawiera zakazu wszystkich rodzajów superiority. Pole o AS należy czytać wraz z zakresem Position Superiority; pełne ogólne procedury pozostają poza oceną.

R917: `/rules/7`, bajty[219963,223365); SHA `63af6f30b27679af5c8b57201640efcb4a3682e020bfdbe15a3d27e411c84ac6`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R917 zawiera zakaz Position Superiority dla EL vs EL oraz pozycyjnego AS z Flank/Rear. Nie zawiera zakazu wszystkich rodzajów superiority. Pole o AS należy czytać wraz z zakresem Position Superiority; pełne ogólne procedury pozostają poza oceną.

R917: `/rules/7`, bajty[287463,290991); SHA `cb0234059d792c80894b60db2acd72e1e243aba445d6746eeac66ddb3035eb0a`.

### EXP-019 — requires_context

Any leader maycommandEL unlessrules specificallyotherwise. Actual leaderauthorization requirescheckingexceptions; keeprequires_context, no inventedactualeligibility.

Dosłowny unless rules specifically otherwise zachowany; exceptions unknown. Streszczenie Any leader may command i false blocking wymagają osobnej oceny realnego użycia. Ograniczone przyjęcie lokalnego odsyłacza/wymagania nie certyfikuje uprawnienia konkretnego leadera ani nie domyka SEM-009.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Actual leader eligibility and rule-specific exceptions require external context.; Wskazany leader, scenariusz i źródło jego ograniczeń; lokalna reguła ogólna pozostaje znana.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R918.transcription zachowuje unless rules specifically otherwise, a exceptions=unknown wskazuje nieznane wyjątki. Jednak action_effect/interpretation brzmi Any leader may command i D918specific/G-D918specific mają blocks_full_result=false/blocking=false. Oznaczono brak źródła, lecz nie zadeklarowano blokady realnej autoryzacji. Kandydat SEM-009: właściwość deklaracji blokady w rzeczywistym użyciu wymaga decyzji; nie ma konkretnego niepoprawnie wybranego dowódcy.

R918: `/rules/8`, bajty[223371,226469); SHA `d2ef7d501f146bfd281fbaa1eae741db574916086ba549200fddadbe2e5c5cc1`.
D918specific: `/dependencies/58`, bajty[464010,465079); SHA `46bc37098ddd17b19bb35251ad26ded1fe92ed25c86c4c900e3c2438c05dff5b`.
G-D918specific: `/gaps/18`, bajty[538068,538573); SHA `c3847703ebaacf82f8fe34d6c7bcf04b9a8a1eb02391ac68d50382088fd5f932`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R918.transcription zachowuje unless rules specifically otherwise, a exceptions=unknown wskazuje nieznane wyjątki. Jednak action_effect/interpretation brzmi Any leader may command i D918specific/G-D918specific mają blocks_full_result=false/blocking=false. Oznaczono brak źródła, lecz nie zadeklarowano blokady realnej autoryzacji. Kandydat SEM-009: właściwość deklaracji blokady w rzeczywistym użyciu wymaga decyzji; nie ma konkretnego niepoprawnie wybranego dowódcy.

R918: `/rules/8`, bajty[290998,294212); SHA `d7a45288d96c2d73bc22a2bc1b20b8c03362c7d8c907b908c1b9dfae8df0ae67`.
D918specific: `/dependencies/58`, bajty[540841,541937); SHA `52edbbb6bd90058a52943715a9959a7d2fec9ad9eedc21249d17952bf12a0a27`.
G-D918specific: `/gaps/18`, bajty[622124,622646); SHA `2a3d8899a381c03d274291d16e984507b2e5d63d9fc7fa52cb05cb734fce6d9a`.

### EXP-020 — confirmed_local_content_scope

WhenIndianELfightAfricanEL:AfricanEL+1PreShockDRM, inadditiontoClashofSpearsandSwords andShockSuperiority notes; notIndian+1norallEL+1norwaiveroftablenotes.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Clash of Spears and Swords, Shock Superiority oraz 8.43 wymagają źródeł do pełnego Shock.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R919.conditions: Indian vs African; +1 Pre-Shock wyłącznie African, dodatkowo do not Clash/SS. Nie przeniesiono DRM na Indian lub wszystkie EL; nie pominięto not przez ogólne zwolnienie.

R919: `/rules/9`, bajty[226475,230470); SHA `d55d07a6e11f89c7a28adb050205027c3cf23a3a60661483c5da133df78666d3`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R919.conditions: Indian vs African; +1 Pre-Shock wyłącznie African, dodatkowo do not Clash/SS. Nie przeniesiono DRM na Indian lub wszystkie EL; nie pominięto not przez ogólne zwolnienie.

R919: `/rules/9`, bajty[294219,298360); SHA `0570133a32e2c860a0a2cd97438a1c41e489344facec89dbf3cac591a0f397ea`.

### EXP-021 — confirmed_local_content_scope

Velites are LI, not SK; SK exceptions do not transfer by similarity. SK OW incurs Hits only via Rear; Velites via Flank or Rear. OW distance/MA condition belongs to EXP-022.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Added maneuver nie definiuje wszystkich uprawnień; procedura OW pozostaje zewnętrzna.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R92note: Velites to LI, nie SK. R921: OW Hits dla SK tylko Rear, Velites Flank/Rear. Nie przeniesiono wszystkich wyjątków SK na Velites. Historyczna nota ma operatywny fragment N-07-S2; pozostała historia poza gold.

N92design: `/nodes/24`, bajty[142234,143048); SHA `06557a0571509b2b41162d16c634800e71f5138b049bdbbe5d769f43280da535`.
R921: `/rules/11`, bajty[234091,238938); SHA `cfe4efdae432e0047facb62fddc25627addc679b00fe30a91959f6a1c715ce32`.
R92note: `/rules/10`, bajty[230476,234085); SHA `77b7cd1fd5a784f68bdbc62ea18264365019ddc79b4a90cbc5326e7bfc953e23`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R92note: Velites to LI, nie SK. R921: OW Hits dla SK tylko Rear, Velites Flank/Rear. Nie przeniesiono wszystkich wyjątków SK na Velites. Historyczna nota ma operatywny fragment N-07-S2; pozostała historia poza gold.

N92design: `/nodes/24`, bajty[191063,191904); SHA `f714c9ad53d998b3e9866366d7a25d9c30c323a4ea051ff70b9acd807b945ea4`.
R921: `/rules/11`, bajty[302099,307124); SHA `7d4cae8640312910b3a82d27a32c19c34148a5723d11798a0df99ab1c459d0aa`.
R92note: `/rules/10`, bajty[298367,302092); SHA `a9052b99d997213c3c6f44fe1a85290abe7bcd5df64b1f8caa64ed751a81072a`.

### EXP-022 — confirmed_local_content_scope

SK may OW up to 2 hexes before an approaching unit with MA equal to or less than SK MA. OW angle costs belong to EXP-021; real routes remain context-dependent.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Pełna trasa OW wymaga procedury, mapy i danych.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R921.conditions i parameters zachowują approaching MA<=SK MA oraz maksimum 2 hexów. action_effect powtarza źródłowe regardless of MA differential; trzeba je czytać w tym warunku, nie jako zniesienie <=. Pełna trasa i kąt OW są osobne. Sama fraza regardless nie jest błędem odczytu.

R921: `/rules/11`, bajty[234091,238938); SHA `cfe4efdae432e0047facb62fddc25627addc679b00fe30a91959f6a1c715ce32`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R921.conditions i parameters zachowują approaching MA<=SK MA oraz maksimum 2 hexów. action_effect powtarza źródłowe regardless of MA differential; trzeba je czytać w tym warunku, nie jako zniesienie <=. Pełna trasa i kąt OW są osobne. Sama fraza regardless nie jest błędem odczytu.

R921: `/rules/11`, bajty[302099,307124); SHA `7d4cae8640312910b3a82d27a32c19c34148a5723d11798a0df99ab1c459d0aa`.

### EXP-023 — confirmed_local_content_scope

targetSKMissile+2DRM;SK/LIArchersA noH&D;LCanymissileclass noH&DvsSK

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Wynik ognia wymaga MRRC i H&D; brak zakazu nie dowodzi pełnej legalności.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R922: target SK +2 Missile DRM; SK/LI Archers Class A nie H&D; LC każdego missile class nie H&D przeciw SK. Te zakazy nie ustalają pełnego lookupu MRRC lub reszty procedury.

R922: `/rules/12`, bajty[238944,243461); SHA `a9598a0db96d75f2c086f3ef29f067d725296d84db5b293cc8eafd8a0cd1c7f2`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R922: target SK +2 Missile DRM; SK/LI Archers Class A nie H&D; LC każdego missile class nie H&D przeciw SK. Te zakazy nie ustalają pełnego lookupu MRRC lub reszty procedury.

R922: `/rules/12`, bajty[307131,311809); SHA `68bf0a61ddd806de4cb7850830a717026f0a98611306b6b6f7c3155fcaf2c767`.

### EXP-024 — confirmed_local_content_scope

SK cannot Shock attack; units attacking a defense consisting only of SK are exempt from Pre-Shock TQ even with the marker. With mixed defense use the other type and ignore SK Size. This owns the attacker exemption; EXP-004 owns the final Pass-Thru check.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie przypisywać SK immunitetu od innych testów ani obrońcy mieszanego.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R923: SK nie Shock attack; atakujący SK alone nie Pre-Shock nawet z markerem; mixed defense wybiera other type i pomija SK Size. Wyjątek końcowego Pass-Thru należy do EXP-004, nie do tego zwolnienia. Nowa DCTX923-S4 ma osobny pending.

R923: `/rules/13`, bajty[243467,249760); SHA `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R923: SK nie Shock attack; atakujący SK alone nie Pre-Shock nawet z markerem; mixed defense wybiera other type i pomija SK Size. Wyjątek końcowego Pass-Thru należy do EXP-004, nie do tego zwolnienia. Nowa DCTX923-S4 ma osobny pending.

R923: `/rules/13`, bajty[311816,318317); SHA `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

### EXP-025 — confirmed_local_content_scope

HitsinflictedbySKhalvefloor,cap1

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Bazowe Hits muszą być podane; kolejność innych modyfikatorów wymaga kontekstu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R923.action/parameters: Hits zadane przez SK pół, floor, maksimum 1 CH. W context-01 Step 4 dostarcza stronę atakującego przy obrońcy SK, lecz nie zmienia lokalnej treści R923. Nowa relacja i pełne applicability/base/CRT/order pozostają poza tą oceną.

R923: `/rules/13`, bajty[243467,249760); SHA `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R923.action/parameters: Hits zadane przez SK pół, floor, maksimum 1 CH. W context-01 Step 4 dostarcza stronę atakującego przy obrońcy SK, lecz nie zmienia lokalnej treści R923. Nowa relacja i pełne applicability/base/CRT/order pozostają poza tą oceną.

R923: `/rules/13`, bajty[311816,318317); SHA `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

### EXP-026 — confirmed_local_content_scope

PH/HI/LGdefendingFrontvsLI noPreShockevenwithattackermarker;LIstillcheck;reverseexemptionnotapplied

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie rozszerzać na Flank/Rear ani inne typy.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R923: PH/HI/LG broniące przez Front przed LI nie robią Pre-Shock nawet z markerem atakującego; LI nadal sprawdza. Reverse wyraźnie nie zachodzi. Nie rozszerzono na Flank/Rear lub inne typy.

R923: `/rules/13`, bajty[243467,249760); SHA `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R923: PH/HI/LG broniące przez Front przed LI nie robią Pre-Shock nawet z markerem atakującego; LI nadal sprawdza. Reverse wyraźnie nie zachodzi. Nie rozszerzono na Flank/Rear lub inne typy.

R923: `/rules/13`, bajty[311816,318317); SHA `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

### EXP-027 — confirmed_local_content_scope

SKRouteliminated,facing0MP,no repeat-moveCohesioncost;no blanketterrain/stackingimmunity

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Koszty terenu i pełny stacking nie są wyłączone.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R924: SK Rout oznacza eliminację, facing kosztuje 0 MP, ponowne ruchy w Game Turn bez Cohesion cost. Nie ma ogólnego zwolnienia z kosztów terenu i stacking.

R924: `/rules/14`, bajty[249766,255895); SHA `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R924: SK Rout oznacza eliminację, facing kosztuje 0 MP, ponowne ruchy w Game Turn bez Cohesion cost. Nie ma ogólnego zwolnienia z kosztów terenu i stacking.

R924: `/rules/14`, bajty[318324,324673); SHA `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

### EXP-028 — confirmed_local_content_scope

oneSK/Velitespergap,notoneglobal;two consecutiveunits do notqualify

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; To lokalny wyjątek; pozostałe warunki 4.32 wymagają kontekstu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R924 i N924ex pokazują pojedynczą przerwę na gap, z możliwością oddzielnych powtórzeń. Dwa kolejne Velites w przykładzie nie tworzą line. Literalne układy 2808/2809/2810/2811/2812 zachowane; nie przyznano pełnej legalności 4.32.

N924ex: `/nodes/3`, bajty[124483,126113); SHA `6a3ef8e03ddb0e28dba14bc0413f7a3ed8013ed67c512e6e022456029c02a8f7`.
R924: `/rules/14`, bajty[249766,255895); SHA `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R924 i N924ex pokazują pojedynczą przerwę na gap, z możliwością oddzielnych powtórzeń. Dwa kolejne Velites w przykładzie nie tworzą line. Literalne układy 2808/2809/2810/2811/2812 zachowane; nie przyznano pełnej legalności 4.32.

N924ex: `/nodes/3`, bajty[172182,173878); SHA `b672863aac81d4eb2fb84ba3e3ca1cae6b8d9c86491f7c4229e84afdeb4e726e`.
R924: `/rules/14`, bajty[318324,324673); SHA `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

### EXP-029 — confirmed_local_content_scope

LCMissileH&DstrictlowerMA,exceptSK;LCArchersfireOW via6.55;fullproceduresunknown

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Sama przewaga MA nie domyka H&D; konieczna procedura 8.3.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R931: missile-armed LC, target strictly lower MA (<, nie <=), wyjątek SK; LC Archers fire podczas OW według 6.55. G-D931HD/OW zatrzymują pełne procedury, nie znany warunek lokalny.

R931: `/rules/15`, bajty[255901,259855); SHA `c203ab22fc5188464f7dabe7f42906f436da91d6c786eab4e76045ad31a63322`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R931: missile-armed LC, target strictly lower MA (<, nie <=), wyjątek SK; LC Archers fire podczas OW według 6.55. G-D931HD/OW zatrzymują pełne procedury, nie znany warunek lokalny.

R931: `/rules/15`, bajty[324680,328792); SHA `9a16f1cac6ab3823e712cfd40b143d10ef7906f1848eeb7b1425e3affe652b04`.

### EXP-030 — confirmed_local_content_scope

attackingLCHitsvsPH/HI/MI/LG/BI halvefloor

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Zależność od AS w przykładzie X-04 wymaga osobnej interpretacji/kontekstu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

Lokalne R932.action_effect/parameters w obu wynikach zachowują pół/floor Hits zadanych przez atakujące LC PH/HI/MI/LG/BI. context-01 zmienia interpretation/exceptions, lecz nie literalną lokalną transkrypcję ani parametr. Ta propozycja nie akceptuje nowych operatorów/wyjątku Routed, całej R932, relacji ani kolejności AS/LC; SEM-003 nadal pending.

R932: `/rules/16`, bajty[259861,263502); SHA `cfce4763843cd4617670464caf65022de44c34273a2423cb87d74de3dd3c2624`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

Lokalne R932.action_effect/parameters w obu wynikach zachowują pół/floor Hits zadanych przez atakujące LC PH/HI/MI/LG/BI. context-01 zmienia interpretation/exceptions, lecz nie literalną lokalną transkrypcję ani parametr. Ta propozycja nie akceptuje nowych operatorów/wyjątku Routed, całej R932, relacji ani kolejności AS/LC; SEM-003 nadal pending.

R932: `/rules/16`, bajty[328799,333292); SHA `064aae5db27a9bda8dd053c7d30ce2d21255bc4236946d1083acd1e2d946dabe`.

### EXP-031 — requires_context

AS/halvingprintedresultconflict requirescontext;no newexceptioninvented

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; AS/LC printed result versus halving order and tables remain unresolved.; Ograniczony dowód bazowego AS/CRT; decyzja właściciela o kolejności.

**first-001: preserve_accepted_source_requirement_full_result_blocked**. Wcześniejszy owner status: reviewed.

first-001 zachowuje literalny printed-result przykład i unknown interpretację; G932/G-D932CRT blocking. context-01 dodaje źródłowe kwalifikacje AS/LC/Routed, ale N932ex nadal unknown i GCTX-order/CRT/applicability/845 blocking. Propozycja: właściwe zachowanie nierozstrzygnięcia pełnego przykładu i potrzeby kontekstu; źródłowa poprawność samych nowych operatorów pozostaje osobnym SEM-003, bez założenia automatycznego znoszenia 2x i pół.

N932ex: `/nodes/4`, bajty[126119,127170); SHA `267371a59674521bf587b0dc168aaec6f2a0370510a765edb525f92a91ad022d`.
R932: `/rules/16`, bajty[259861,263502); SHA `cfce4763843cd4617670464caf65022de44c34273a2423cb87d74de3dd3c2624`.
G932: `/gaps/1`, bajty[529516,530113); SHA `43cf016d3697d9674abe943581db6ce085b1bd34d93ebff98716ba95c28cb7db`.

**context-01: preserve_accepted_source_requirement_full_result_blocked**. Wcześniejszy owner status: reviewed.

first-001 zachowuje literalny printed-result przykład i unknown interpretację; G932/G-D932CRT blocking. context-01 dodaje źródłowe kwalifikacje AS/LC/Routed, ale N932ex nadal unknown i GCTX-order/CRT/applicability/845 blocking. Propozycja: właściwe zachowanie nierozstrzygnięcia pełnego przykładu i potrzeby kontekstu; źródłowa poprawność samych nowych operatorów pozostaje osobnym SEM-003, bez założenia automatycznego znoszenia 2x i pół.

N932ex: `/nodes/4`, bajty[173885,175403); SHA `0eb4d362032a4ff5fd28d28ce38de975b77453af7223949fec3d0d816223b27c`.
R932: `/rules/16`, bajty[328799,333292); SHA `064aae5db27a9bda8dd053c7d30ce2d21255bc4236946d1083acd1e2d946dabe`.
G932: `/gaps/1`, bajty[613015,613877); SHA `40ca31a42e0dc11f02dc67847683cb0ede5435964a848312c5b720bfbb8bc5d4`.

### EXP-032 — confirmed_local_content_scope

movingFrontPHDefense2Lperqualifyingflank,HI1Lperflank;excludestartadjacentstayed,FlankRear,anyPHattacker

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Lokalny shift, nie pełny wynik CRT bez tabeli.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R941.conditions: moves adjacent i Shock przez Front; po 2L na flank zajęty przez friendly PH lub w friendly PH ZOC, HI any Class 1L zamiast 2L. Wyłączenia: rozpoczęcie adjacent i pozostanie tam, Flank/Rear oraz jakikolwiek PH wśród atakujących. Brak CRT nie blokuje podanego lokalnego shiftu.

R941: `/rules/17`, bajty[263508,268383); SHA `112f98003ed54c0f8f09d2d00327263a8c7c577c036536d988707561e7dbac94`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R941.conditions: moves adjacent i Shock przez Front; po 2L na flank zajęty przez friendly PH lub w friendly PH ZOC, HI any Class 1L zamiast 2L. Wyłączenia: rozpoczęcie adjacent i pozostanie tam, Flank/Rear oraz jakikolwiek PH wśród atakujących. Brak CRT nie blokuje podanego lokalnego shiftu.

R941: `/rules/17`, bajty[333299,338353); SHA `554b4ecd3a2ad5a80f0fa28cafc3c8b8f0528efdd7418e7d1999840cae58b045`.

### EXP-033 — requires_context

scenarioDDeligibilitylistnecessary,missingblocksSIT11

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Scenario-specific Double-Depth eligibility list is required.; Wybrany scenariusz z listą uprawnionych jednostek.

**first-001: preserve_accepted_source_requirement_full_result_blocked**. Wcześniejszy owner status: reviewed.

R95note/N95design zachowują operatywny wymóg scenario-specific eligible units, R951 warunek eligible. G-D95scenario blocking=true, brak listy nie zastąpiony zgodą dla wszystkich PH. N953ex to jedynie odesłanie do przykładu; jego nonblocking nie zamyka krytycznej listy eligibility. Nie oceniono SIT-11.

N953ex: `/nodes/6`, bajty[128320,128971); SHA `32ad4997be80003431ce7d9782486b53cafcb6a9bd4a6ba63f26a0091bbff9b9`.
N95design: `/nodes/26`, bajty[143799,144517); SHA `befa3bbc8e95ad44cd60c24834e7ac7c76df7271a4c228979bb40b3ec394ab04`.
R951: `/rules/19`, bajty[271660,276889); SHA `6ed20d621c4094781ff1689567d941ab7d22e764fe9a78ef1686795326e5e7a7`.
R95note: `/rules/18`, bajty[268389,271654); SHA `119eed8150bbbc291da6700cfdd1cf837f904262b76165126e4b13fd265bbf7c`.
G-D95scenario: `/gaps/33`, bajty[545320,545797); SHA `ffc2b8f02e837a46b5e9af729d8cbb8bf17509c59767c860a00a3e04b0ee9259`.

**context-01: preserve_accepted_source_requirement_full_result_blocked**. Wcześniejszy owner status: reviewed.

R95note/N95design zachowują operatywny wymóg scenario-specific eligible units, R951 warunek eligible. G-D95scenario blocking=true, brak listy nie zastąpiony zgodą dla wszystkich PH. N953ex to jedynie odesłanie do przykładu; jego nonblocking nie zamyka krytycznej listy eligibility. Nie oceniono SIT-11.

N953ex: `/nodes/6`, bajty[176598,177276); SHA `32059fb98dda21cbaacbf3674087807d1696268d8d9a7236e4b6220eb6b7380f`.
N95design: `/nodes/26`, bajty[192684,193429); SHA `f17c97f5b1d2fb4d5811fb18481d7ff3dfbe32f09a24af8c9e2568f554fabe8c`.
R951: `/rules/19`, bajty[341748,347170); SHA `5a34602f7f460a66fe124c94424a27e1ac98d03e9da186e73f8c2763358bf313`.
R95note: `/rules/18`, bajty[338360,341741); SHA `45f74a06c6c69fbd84bd9aff1a0d58e7f58f502096e2ab3bd83ae51d84aedf49`.
G-D95scenario: `/gaps/33`, bajty[630196,630690); SHA `3e15292276ba3e8a68b020af426167df2b461ba730b0f23460eb69d28884545c`.

### EXP-034 — confirmed_local_content_scope

formingDDIOorLCdirectOC,backstartsbehindfront,terraincost+1MP,backunderfront,endbothmovementthisphase

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Eligibility, OC i koszt terenu jako osobne potrzebne fakty.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R951: IO albo LC bezpośrednio od OC, back PH startuje bezpośrednio za front, płaci terrain+1 MP, trafia pod front; kończy ruch obu w tej Orders Phase. Nie ustalono realnej eligibility, OC ani kosztu terenu.

R951: `/rules/19`, bajty[271660,276889); SHA `6ed20d621c4094781ff1689567d941ab7d22e764fe9a78ef1686795326e5e7a7`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R951: IO albo LC bezpośrednio od OC, back PH startuje bezpośrednio za front, płaci terrain+1 MP, trafia pod front; kończy ruch obu w tej Orders Phase. Nie ustalono realnej eligibility, OC ani kosztu terenu.

R951: `/rules/19`, bajty[341748,347170); SHA `5a34602f7f460a66fe124c94424a27e1ac98d03e9da186e73f8c2763358bf313`.

### EXP-035 — confirmed_local_content_scope

OCordersonly,2IOwhenIOmovement,PAWvia6.8,noWheel/Reverse/Column;unstacktopmoves,bottomstays,IOorLCasabove;fullLCprocedure notclosed

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Procedury zewnętrzne 6.8/6.44/6.45/6.7 i orders pozostają potrzebne dla pełnego wykonania.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R952: rozkazy tylko OC; 2 IO przy ruchu w trybie IO, PAW 6.8, no Wheel/Reverse/Column. Unstack IO lub LC as above, top rusza za normalny koszt, bottom zostaje. R951 i pierwszy warunek OC zachowują zakres as above; nie domknięto pełnej procedury LC lub PAW.

R952: `/rules/20`, bajty[276895,283151); SHA `d3c03f8437c1acf3a3540923b725ecef09aac6ba7a23ecba4b82837c59d2d011`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R952: rozkazy tylko OC; 2 IO przy ruchu w trybie IO, PAW 6.8, no Wheel/Reverse/Column. Unstack IO lub LC as above, top rusza za normalny koszt, bottom zostaje. R951 i pierwszy warunek OC zachowują zakres as above; nie domknięto pełnej procedury LC lub PAW.

R952: `/rules/20`, bajty[347177,353653); SHA `bbf568a4a71dbd5e7ae685da23f7c7d5c0527aab3e5650cf8fb3695982a880d3`.

### EXP-036 — confirmed_local_content_scope

readyDDMA4never5,movementHittoeach,nounitthroughorintoreadyDD;forming9.51separate

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Przypadek formowania DD z 9.51 wymaga rozróżnienia etapu od gotowej formacji.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R952 dla units in DD: zawsze MA4, nigdy MA5; movement CH do każdej, zakaz wejścia/przejścia jakiegokolwiek unit przez gotowy DD. R951 osobno reprezentuje etap formowania, zanim gotowy stack istnieje. Nie odczytano zakazu jako anulowania formowania.

R952: `/rules/20`, bajty[276895,283151); SHA `d3c03f8437c1acf3a3540923b725ecef09aac6ba7a23ecba4b82837c59d2d011`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R952 dla units in DD: zawsze MA4, nigdy MA5; movement CH do każdej, zakaz wejścia/przejścia jakiegokolwiek unit przez gotowy DD. R951 osobno reprezentuje etap formowania, zanim gotowy stack istnieje. Nie odczytano zakazu jako anulowania formowania.

R952: `/rules/20`, bajty[347177,353653); SHA `bbf568a4a71dbd5e7ae685da23f7c7d5c0527aab3e5650cf8fb3695982a880d3`.

### EXP-037 — confirmed_local_content_scope

combinedSize,topTQunlessRearthenbottom;otherchecksifselectedunitincursHits;actualTQvaluesunknown

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Ogólny test TQ i inne modyfikatory poza lokalną selekcją wymagają celu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R953: combine Sizes, TQ top, przy Rear bottom; jeśli wybrana do check jednostka dostaje jakiekolwiek Hits, druga również sprawdza. Unknown interpretacja końcowej eliminacji G953 nie uchyla jawnych wcześniejszych efektów; prawdziwe ratingi i pełny check nieustalone.

R953: `/rules/21`, bajty[283157,290596); SHA `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R953: combine Sizes, TQ top, przy Rear bottom; jeśli wybrana do check jednostka dostaje jakiekolwiek Hits, druga również sprawdza. Unknown interpretacja końcowej eliminacji G953 nie uchyla jawnych wcześniejszych efektów; prawdziwe ratingi i pełny check nieustalone.

R953: `/rules/21`, bajty[353660,361365); SHA `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

### EXP-038 — confirmed_local_content_scope

enemydefendingagainstDD+1PreShock,DDdefending-1;9.41conditionsstillapply

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; R-9.53→R-9.41 to użycie warunkowej modyfikacji, nie odwrotny kierunek.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R953: przeciwnik broniący się przed DD +1 Pre-Shock; DD jako defender -1. R941 w mapowanym zakresie zachowuje warunki i wyłączenia Phalanx Defense, więc nie przyznano shiftu bezwarunkowo. Nie nadaje to formalnego TP krawędzi R953→R941.

R941: `/rules/17`, bajty[263508,268383); SHA `112f98003ed54c0f8f09d2d00327263a8c7c577c036536d988707561e7dbac94`.
R953: `/rules/21`, bajty[283157,290596); SHA `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R953: przeciwnik broniący się przed DD +1 Pre-Shock; DD jako defender -1. R941 w mapowanym zakresie zachowuje warunki i wyłączenia Phalanx Defense, więc nie przyznano shiftu bezwarunkowo. Nie nadaje to formalnego TP krawędzi R953→R941.

R941: `/rules/17`, bajty[333299,338353); SHA `554b4ecd3a2ad5a80f0fa28cafc3c8b8f0528efdd7418e7d1999840cae58b045`.
R953: `/rules/21`, bajty[353660,361365); SHA `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

### EXP-039 — confirmed_local_content_scope

FlankReardefenderShockHits3xinstead2x,equalallocationoddtop;missileHits topunlessRearthenbottom

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Bazowy wynik i kolejność wobec innych mnożników muszą być dostarczone/zweryfikowane.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R953: Hits DD defender w Shock przez Flank/Rear 3x zamiast 2x; Shock rozdzielony równo, nieparzysty Hit do top. Missile do top z wyjątkiem Rear do bottom. Selekcja TQ przez Rear nie zmienia odd-Hit allocation Shock; baza i inne mnożniki pozostają poza zakresem.

R953: `/rules/21`, bajty[283157,290596); SHA `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R953: Hits DD defender w Shock przez Flank/Rear 3x zamiast 2x; Shock rozdzielony równo, nieparzysty Hit do top. Missile do top z wyjątkiem Rear do bottom. Selekcja TQ przez Rear nie zmienia odd-Hit allocation Shock; baza i inne mnożniki pozostają poza zakresem.

R953: `/rules/21`, bajty[353660,361365); SHA `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

### EXP-040 — confirmed_local_content_scope

When one PH of DD Routs, both Rout and retreat separately. Eliminate each PH individually if it cannot complete legal Rout movement; the other may perform its own legal Rout if possible. Actual geometry, 6.69/10.22, order/shared sole destination and later D1 result are unclosed. Local 10.24/25/23 context is supporting evidence, not an additional scoring unit.

Oba R953 zachowują both rout/separate hexes i literalne the unit, ale interpretation/G953 pozostawia liczbę eliminowanych jednostek otwartą. .4d3 przyjęła literalną treść, nie pełną gałąź per-unit eliminacji. Zachowuję SEM-002, w tym dostępność podparcia dla ekstraktora i realną geometrię/kolejność; nie pozyskuję nowej strony.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Per-unit elimination reading is confirmed; real geometry, 6.69/10.22, legal ordering and a shared sole destination remain unresolved.; Legalne heksy retreat i zakres końcowego the unit wymagają kontekstu przy konfliktach.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

Oba R953 zachowują both rout i separate hexes, ale końcowe the unit pozostaje literalne; interpretation unknown/G953 blocking. Eval-v1 ma per-unit eliminację z możliwością legalnego Rout drugiej PH. Propozycja niepełnej reprezentacji tej lokalnej gałęzi pozostaje SEM-002 pending; osobno dostępność podparcia 10.24/25/23 dla ekstraktora i rzeczywista geometria/kolejność.

R953: `/rules/21`, bajty[283157,290596); SHA `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.
G953: `/gaps/2`, bajty[530119,530709); SHA `e7acbacfb4fb7b0f9a12bc3d1bf41019f7507987177c49efc34ba8b596816a21`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

Oba R953 zachowują both rout i separate hexes, ale końcowe the unit pozostaje literalne; interpretation unknown/G953 blocking. Eval-v1 ma per-unit eliminację z możliwością legalnego Rout drugiej PH. Propozycja niepełnej reprezentacji tej lokalnej gałęzi pozostaje SEM-002 pending; osobno dostępność podparcia 10.24/25/23 dla ekstraktora i rzeczywista geometria/kolejność.

R953: `/rules/21`, bajty[353660,361365); SHA `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.
G953: `/gaps/2`, bajty[613884,614490); SHA `7924b01b3b0ac91dbac0c788b1ec6d730954bca49cca180b5737da725e4c05ba`.

### EXP-041 — confirmed_local_content_scope

ruleofthumb2Romaninfantry sameborderwithexceptions;notfulllegaleligibility;move2IO,1IOifstackedOCgivingorders,1LCifbotheligible

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Pełny stacking chart i eligibility nie są dowiedzione regułą thumb.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R961: rule of thumb dwóch Roman infantry tego samego border color, z wyjątkami jak Velites. Nie pełne eligibility. Joint move 2 IO; 1 IO tylko z OC w stack dającym rozkazy; 1 LC tylko jeśli obie eligible. Odesłania do charts/line nie zamykają pełnych procedur.

R961: `/rules/22`, bajty[290602,296910); SHA `6b8470e5e55b69e23271008267a8bbe41527657e5a35dcdbfead196e82bce062`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R961: rule of thumb dwóch Roman infantry tego samego border color, z wyjątkami jak Velites. Nie pełne eligibility. Joint move 2 IO; 1 IO tylko z OC w stack dającym rozkazy; 1 LC tylko jeśli obie eligible. Odesłania do charts/line nie zamykają pełnych procedur.

R961: `/rules/22`, bajty[361372,367903); SHA `bcb032de73b22e12958d3e579d0d9c7a13da82705652c8059b17135e5ec59a74`.

### EXP-042 — confirmed_local_content_scope

combineSize,otherratingsespeciallyTQtop,eachunitowntestusingtopTQ,onlytopfire,bothShock samehex;automaticHitsto each;Shockallocationdelegated8.46Step4/10.13

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Rozdział 9 nie domyka alokacji Shock Hits; 10.13 jest kontekstem, 6.68 nieprzejrzane.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R962: combine Size, inne ratingi w tym TQ top; własny check każdej z top TQ; tylko top Missile Fire, obie Shock tego samego hex; Automatic Hits do każdej. Shock alokacja delegated 8.46 Step4/10.13. R962 jest niezmieniona; context D962shock dostało endpoint, lecz G-D962shock nadal blocking, dalej brak 6.68 #6. Lokalna reprezentacja nie zamyka alokacji ani nie nadaje TP.

R962: `/rules/23`, bajty[296916,301592); SHA `ae11cd4ac05b78d7fd21fa35572b242282d9da3c6d8f9663a0bca89e32363e44`.
D962shock: `/dependencies/86`, bajty[491159,492109); SHA `3c908d4ef58625aa4246c0c74394c38d248d7395d859cbe232853e1f16fd6e84`.
G-D962shock: `/gaps/46`, bajty[551285,551743); SHA `feddccd1eae798c1109af40a1131d66402bdffbae6842f125ea7599830635945`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R962: combine Size, inne ratingi w tym TQ top; własny check każdej z top TQ; tylko top Missile Fire, obie Shock tego samego hex; Automatic Hits do każdej. Shock alokacja delegated 8.46 Step4/10.13. R962 jest niezmieniona; context D962shock dostało endpoint, lecz G-D962shock nadal blocking, dalej brak 6.68 #6. Lokalna reprezentacja nie zamyka alokacji ani nie nadaje TP.

R962: `/rules/23`, bajty[367910,372751); SHA `661e95a04df56028793a45c4b225c06f3a371ebc9314efc42611fd5c3c3a451d`.
D962shock: `/dependencies/86`, bajty[568940,569960); SHA `4b5a3bf62cbe0d3cc8ae154e79c9b1c2a395320a952179da661102ad74d23c25`.
G-D962shock: `/gaps/46`, bajty[636395,637341); SHA `509a59a82e0105d408795e67884d2c386317392861627fcc47a506f0fef47014`.

### EXP-043 — confirmed_local_content_scope

differentbordercolors ORsamecolordifferentclasses,+1DRMtoallTQchecks

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Typy i kolory muszą być znane z danych jednostek.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R963 zachowuje OR: różne border colors lub ten sam color i różne classes. +1 DRM do wszystkich TQ checks, bez zastąpienia OR przez AND. Faktyczne kolory i klasy wymagają danych.

R963: `/rules/24`, bajty[301598,305296); SHA `58a813b6aaba0b0d25a66c3b7a3fd2c3a6bcf811684e8bf617f574c0430f29f8`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R963 zachowuje OR: różne border colors lub ten sam color i różne classes. +1 DRM do wszystkich TQ checks, bez zastąpienia OR przez AND. Faktyczne kolory i klasy wymagają danych.

R963: `/rules/24`, bajty[372758,376599); SHA `4fbf3c5ea3e740875782caf600b70a3974f0e7f9ff7bda1b8dea4c9c2261a9ea`.

### EXP-044 — confirmed_local_content_scope

stackorderchangeIOonly,notmovement/LC;facingcanLC;onlytopmovesifmovingoneunitfromstack

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie zastosować zwykłego unstack do MLE bez sprawdzenia szczególnej reguły.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R964: zamiana kolejności stack tylko IO, nie część movement ani LC; facing może LC. Przy ruchu jednej jednostki z stacku rusza tylko top. Nie rozszerzono zwykłego unstack na szczególne MLE.

R964: `/rules/25`, bajty[305302,309224); SHA `0011f5a4a5cd234d3f5c62f4b8510d023a26e8b43bc154f1edd2acb291c5b9ea`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R964: zamiana kolejności stack tylko IO, nie część movement ani LC; facing może LC. Przy ruchu jednej jednostki z stacku rusza tylko top. Nie rozszerzono zwykłego unstack na szczególne MLE.

R964: `/rules/25`, bajty[376606,380671); SHA `e4530c490edde7d54d4ac9fd06686c4a0312813eb32d7107cf885172e47c8fe8`.

### EXP-045 — confirmed_local_content_scope

Romaninfantryfacing1MPanynumbervertices;notMLEfacingrule

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie rozszerzać tej wartości na MLE, które zachowuje facing.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R965: Roman infantry 1 MP za facing dowolnej liczby vertices, nie koszt za każdy vertex. Nie przeniesiono tej operacji na MLE, które zachowuje facing.

R965: `/rules/26`, bajty[309230,312838); SHA `e38853213823da0429d224631ca49efed539fcf423497ce1ab8828e28f8fc77a`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R965: Roman infantry 1 MP za facing dowolnej liczby vertices, nie koszt za każdy vertex. Nie przeniesiono tej operacji na MLE, które zachowuje facing.

R965: `/rules/26`, bajty[380678,384416); SHA `19ae59d6e959efb3e6c037af8605714eddab51c425881ad764356addf2f199d3`.

### EXP-046 — confirmed_local_content_scope

topunits instackssameLine sideways tovacantflankClearoutsideenemyZOC,facingunchanged;unstackonly,notstackingTogether;diagramOriginaltop/Afterbottomillustrative

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Same Line przez4.32, Clear i ZOC wymagają danych/procedur; grafika nie daje ogólnego prawa do dowolnej strony.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R966: top units w stackach tej samej Line, sideways do vacant flank; Clear i poza enemy ZOC, facing bez zmiany; wyłącznie unstack, nie stacking together. N966diagram zachowuje Original Deployment u góry, After MLE u dołu jako ilustrację. Nie akceptujemy małych ratingów, identyfikacji front/back konkretnych counterów ani ogólnego prawa do dowolnej strony z samej grafiki.

N966diagram: `/nodes/7`, bajty[128977,130323); SHA `f5c32b1dae24067c8069c9f6a259e1da4cd473f61255ce80b5b070a71cc69689`.
R966: `/rules/27`, bajty[312844,317525); SHA `2e7a501a9a282ca4841068af720073ea84aba9cb1de2d3ccd280e3a2103302a6`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R966: top units w stackach tej samej Line, sideways do vacant flank; Clear i poza enemy ZOC, facing bez zmiany; wyłącznie unstack, nie stacking together. N966diagram zachowuje Original Deployment u góry, After MLE u dołu jako ilustrację. Nie akceptujemy małych ratingów, identyfikacji front/back konkretnych counterów ani ogólnego prawa do dowolnej strony z samej grafiki.

N966diagram: `/nodes/7`, bajty[177283,178673); SHA `36e8f4cd62347156e4d08983cd3b50a484a73b8478deddb5b4167d954c4d364d`.
R966: `/rules/27`, bajty[384423,389278); SHA `2c3df78a88652b14a70895ae92c0bb0cf0a15d34596c536e9f59a05f1c63c10e`.

### EXP-047 — confirmed_local_content_scope

reactiontriggerenemycombatwithin2hexes,line;maydeclinefirstopportunitywithoutlosinglatertriggers;OW/MLEdifferentunitscanwithvalidtriggers,sameunitscannotboth

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; OW i legalność line muszą być ustalone oddzielnie.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R967: reakcja w instant approach enemy combat within 2 hexes of stacked Roman line; wolno odroczyć pierwszą okazję do następnego kwalifikowanego triggeru. OW/MLE razem tylko przez różne jednostki z właściwymi triggerami, nie te same. N967ex zachowuje przykład Velites OW i Hastati MLE.

N967ex: `/nodes/8`, bajty[130329,131266); SHA `e2e9a2dcba7c2946ba1d54d93b45bacb6ff8a8e47c5af7e1e088c2c856fcbb15`.
R967: `/rules/28`, bajty[317531,321925); SHA `8aba3115f33776d806a6a196be0cae710b2eea2eef13c04318a89102b3d53fcc`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R967: reakcja w instant approach enemy combat within 2 hexes of stacked Roman line; wolno odroczyć pierwszą okazję do następnego kwalifikowanego triggeru. OW/MLE razem tylko przez różne jednostki z właściwymi triggerami, nie te same. N967ex zachowuje przykład Velites OW i Hastati MLE.

N967ex: `/nodes/8`, bajty[178680,179647); SHA `6c9efe1728ad06ece3b7d45cd71e78dd02c715ae518ebbee8f2841bd7e8fdc26`.
R967: `/rules/28`, bajty[389285,393844); SHA `e9376d25c08d2ed7bc27163917fcc5b9fc9ec4de5df11c2c309c7a92e2ef5755`.

### EXP-048 — confirmed_local_content_scope

activeMLELC-only,bothunitsmaymoveafterwithMA-2,noCHforMLE;ColumnunitsnoMLE;noautomatictransferofLCpostmovepermissiontoreaction

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie przenosić automatycznie post-MLE ruchu na tryb reakcyjny.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R968 wyraźnie kwalifikuje post-MLE move przez When by LC: obie jednostki mogą ruszyć z MA-2. LC-only dla aktywnego MLE, 0 CH za samo MLE i zakaz Column. Nie przeniesiono uprawnienia dalszego ruchu na tryb reakcyjny R967.

R968: `/rules/29`, bajty[321931,326799); SHA `4b8130db1b3f0bfe4d6e9ea3c3c7f8bcbb8db3d078654f49c01ad8a85db297bb`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R968 wyraźnie kwalifikuje post-MLE move przez When by LC: obie jednostki mogą ruszyć z MA-2. LC-only dla aktywnego MLE, 0 CH za samo MLE i zakaz Column. Nie przeniesiono uprawnienia dalszego ruchu na tryb reakcyjny R967.

R968: `/rules/29`, bajty[393851,398910); SHA `8b4bf17469c5987e914879bec985cb90bb189d32fa5e9a15e1e560fcf66722a1`.

### EXP-049 — confirmed_local_content_scope

Romansprior200BCE,ScipioAfricanusnotOC;Cannaeexplicitusepergameinstruction,notnewhistoricalinference;C9.7S2explanatory

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; W realnym scenariuszu data i tożsamość OC wymagają dowodów.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R97intro: obowiązek dla Romans przed 200 BCE i bez Scipio Africanus jako OC; Cannae jawnie objęte instrukcją gry, nie historycznym wnioskowaniem. Parametr jest prior to 200, nie <=200. Explanatory C9.7-S2 nie stanowi dodatkowego obowiązku.

R97intro: `/rules/30`, bajty[326805,330943); SHA `640110048218e02f57f9aa8bdca2bd334ae950abe580344d8bfe03f9663b5001`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R97intro: obowiązek dla Romans przed 200 BCE i bez Scipio Africanus jako OC; Cannae jawnie objęte instrukcją gry, nie historycznym wnioskowaniem. Parametr jest prior to 200, nie <=200. Explanatory C9.7-S2 nie stanowi dodatkowego obowiązku.

R97intro: `/rules/30`, bajty[398917,403202); SHA `e89bbba15ff240518389e505e94aa7d9a023816ca59d362b60b3a7c6e8b29516`.

### EXP-050 — requires_context

realbattlewithoutdate/OC/AWL notresolved,requires_context

R97intro ma datę/OC jako predykat, nie fakty wybranej bitwy; osobnej date/OC gap brak, AWL/RP/LOS/ZOC mają blocking gaps. Przyjęta proza nie jest przyjęciem kompletnej deklaracji źródeł lub konkretnej kwalifikacji bitwy. SEM-010 pozostaje otwarte; pominięcie historycznej końcówki SEM-021 już rozstrzygnięte osobno.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Actual battle date, Overall Commander, AWL and scenario facts are required.; Konkretny scenariusz, OC, AWL/RP i stan mapy.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

Obie odpowiedzi podają predykaty daty/OC i warunki Triarii, nie rzeczywiste dane wybranej bitwy. AWL/RP/LOS/ZOC mają jawne blocking gaps; brak osobnych deklaracji źródła rzeczywistej daty i OC w R97intro.gap_ids (pusta lista). SEM-010: wystarczalność tego opisu needs-context wymaga właściciela. Nie jest to dowód fikcyjnego wybrania dowódcy/daty; known na conditions oznacza znany warunek, nie spełniony fakt. Nie oceniono SIT.

R971: `/rules/31`, bajty[330949,335849); SHA `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.
R972: `/rules/32`, bajty[335855,339867); SHA `f304ccb85a653664ddb287c3e591dd67a2744b35cf4210ace71592b684436f5b`.
R97intro: `/rules/30`, bajty[326805,330943); SHA `640110048218e02f57f9aa8bdca2bd334ae950abe580344d8bfe03f9663b5001`.
G-D972AWL: `/gaps/54`, bajty[555028,555502); SHA `7b2a49345eb5abfd06e09555c1a797ca2d0960cac20429a52f04434614135c9c`.
G-D972RP: `/gaps/55`, bajty[555508,555991); SHA `ecd85583d0a2f8ae358a010ae1bdbd73965717a64fd61fa126755e49e065078c`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

Obie odpowiedzi podają predykaty daty/OC i warunki Triarii, nie rzeczywiste dane wybranej bitwy. AWL/RP/LOS/ZOC mają jawne blocking gaps; brak osobnych deklaracji źródła rzeczywistej daty i OC w R97intro.gap_ids (pusta lista). SEM-010: wystarczalność tego opisu needs-context wymaga właściciela. Nie jest to dowód fikcyjnego wybrania dowódcy/daty; known na conditions oznacza znany warunek, nie spełniony fakt. Nie oceniono SIT.

R971: `/rules/31`, bajty[403209,408288); SHA `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.
R972: `/rules/32`, bajty[408295,412460); SHA `efc3e461afcdf47ef5fafdc90f3c9223badabf8597ff20dc3ef7807de8842bde`.
R97intro: `/rules/30`, bajty[398917,403202); SHA `e89bbba15ff240518389e505e94aa7d9a023816ca59d362b60b3a7c6e8b29516`.
G-D972AWL: `/gaps/54`, bajty[640754,641245); SHA `4501dab342ed343a618bfbff3bc2c2a58e0037d4bb0ec51b1ce768d66008b659`.
G-D972RP: `/gaps/55`, bajty[641252,641752); SHA `f55d0cda36ede2f89e9a06f65931deb0783be55f592e897fdf842846f390abca`.

### EXP-051 — confirmed_local_content_scope

movementgate9.71cannotmovebutmayface untiloneofORtriggers:enemycombatnotELwithin3andLOSanyTriariilineunit ORTriarii>=6fromallRoman/Alainfantrylinesexcludingallied

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Line, LOS, odległości i identyfikacja wojsk wymagają jawnych danych.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R971 zachowuje zakaz ruchu i możliwość facing przed zwolnieniem. Bramka 9.71 ma OR: enemy combat nie-EL w odległości do 3 heksów AND LOS dowolnej jednostki linii Triarii, albo odległość co najmniej 6 od wszystkich innych Roman/Ala infantry lines, z wyłączeniem allied. Nie zastąpiono any przez all, OR przez AND ani >=6 przez >6. To lokalna bramka, bez ogólnego zezwolenia na move+Shock i bez akceptacji relacji 9.72→9.71.

R971: `/rules/31`, bajty[330949,335849); SHA `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.
G-D971LOS: `/gaps/53`, bajty[554574,555022); SHA `0fbbec450f17ca03c3aabeaeee56e5ba736da2a160154409128713bb125171b7`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R971 zachowuje zakaz ruchu i możliwość facing przed zwolnieniem. Bramka 9.71 ma OR: enemy combat nie-EL w odległości do 3 heksów AND LOS dowolnej jednostki linii Triarii, albo odległość co najmniej 6 od wszystkich innych Roman/Ala infantry lines, z wyłączeniem allied. Nie zastąpiono any przez all, OR przez AND ani >=6 przez >6. To lokalna bramka, bez ogólnego zezwolenia na move+Shock i bez akceptacji relacji 9.72→9.71.

R971: `/rules/31`, bajty[403209,408288); SHA `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.
G-D971LOS: `/gaps/53`, bajty[640282,640747); SHA `30bef8bfaae34c6d93008a0e4a476c3a60dd69b4aaaad592022e14b733622c12`.

### EXP-052 — confirmed_local_content_scope

move+ShockRP>=floor(AWL/2)doesnotbypass9.71;standingShockagainsttargetinownZOCper9.72withouthavingtomove

R971 iR972 zachowują dwie bramki i stationary Shock exception, lecz nie podają jawnego połączenia we wskazanym reviewed_scope. .4d3 przyjęła dokładne klauzule osobno; nie wybrała koniunkcji za model. Brak DEP-NEW-001 zachowany strukturalnie; SEM-011/EXP-052 i sześć powiązanych rubryk pending.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; 9.71 i9.72 czytane razem; full legal attack nadal wymaga innych warunków.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R972 zachowuje RP >= floor(AWL/2), jednostkę Rout Points i wyjątek Shock bez ruchu przeciw enemy w własnej ZOC. R971 osobno zawiera drugą bramkę. R972.conditions/action_effect nie podaje jednak jawnie, że próg RP nie omija 9.71; brak osobnej pary DEP-NEW-001 odziedziczony. Właściciel rozstrzyga, czy dwa osobne ograniczenia wystarczają do całego reviewed_scope EXP-052, czy reprezentacja ich koniunkcji jest niepełna. Nie dopisano bramki do odpowiedzi, nie nadano FN ani ogólnego pozwolenia na atak.

R972: `/rules/32`, bajty[335855,339867); SHA `f304ccb85a653664ddb287c3e591dd67a2744b35cf4210ace71592b684436f5b`.
R971: `/rules/31`, bajty[330949,335849); SHA `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.
G-D972AWL: `/gaps/54`, bajty[555028,555502); SHA `7b2a49345eb5abfd06e09555c1a797ca2d0960cac20429a52f04434614135c9c`.
G-D972RP: `/gaps/55`, bajty[555508,555991); SHA `ecd85583d0a2f8ae358a010ae1bdbd73965717a64fd61fa126755e49e065078c`.
G-D-ZOC-R972: `/gaps/79`, bajty[567098,567558); SHA `a4d67be1b5ec9d51a406e372f6202fce147a18184e5a5f18a6425518640595a8`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R972 zachowuje RP >= floor(AWL/2), jednostkę Rout Points i wyjątek Shock bez ruchu przeciw enemy w własnej ZOC. R971 osobno zawiera drugą bramkę. R972.conditions/action_effect nie podaje jednak jawnie, że próg RP nie omija 9.71; brak osobnej pary DEP-NEW-001 odziedziczony. Właściciel rozstrzyga, czy dwa osobne ograniczenia wystarczają do całego reviewed_scope EXP-052, czy reprezentacja ich koniunkcji jest niepełna. Nie dopisano bramki do odpowiedzi, nie nadano FN ani ogólnego pozwolenia na atak.

R972: `/rules/32`, bajty[408295,412460); SHA `efc3e461afcdf47ef5fafdc90f3c9223badabf8597ff20dc3ef7807de8842bde`.
R971: `/rules/31`, bajty[403209,408288); SHA `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.
G-D972AWL: `/gaps/54`, bajty[640754,641245); SHA `4501dab342ed343a618bfbff3bc2c2a58e0037d4bb0ec51b1ce768d66008b659`.
G-D972RP: `/gaps/55`, bajty[641252,641752); SHA `f55d0cda36ede2f89e9a06f65931deb0783be55f592e897fdf842846f390abca`.
G-D-ZOC-R972: `/gaps/79`, bajty[653278,653755); SHA `f4316df191200527106f5fdd44db596d27ef4f4760e20d7f5d07f53eae494b36`.

### EXP-053 — confirmed_local_content_scope

ScorpioBoltB,builtincrew,TQ,LIonlymovement/defense;noShockattack,offensiveMissileFireonly

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Pełne LI defense/movement i bolt MRRC wymagają kontekstu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R981 zachowuje Bolt B, built-in crews i obecność TQ; LI tylko dla movement oraz obrony w Shock/Missile. Zakaz Shock-capable i jedyna zdolność ofensywna Missile Fire nie są rozszerzone na brak możliwości obrony. Konkretna wartość TQ i pełny lookup Bolt MRRC wyłączone.

R981: `/rules/33`, bajty[339873,343919); SHA `4e4891fc2c755ae9c07ed249141e368ed4377a415f874d747416eecb628eed39`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R981 zachowuje Bolt B, built-in crews i obecność TQ; LI tylko dla movement oraz obrony w Shock/Missile. Zakaz Shock-capable i jedyna zdolność ofensywna Missile Fire nie są rozszerzone na brak możliwości obrony. Konkretna wartość TQ i pełny lookup Bolt MRRC wyłączone.

R981: `/rules/33`, bajty[412467,416654); SHA `76cecff485b506b160191a8885cea72dd7016bed6da4f3798c6d7d01dbc6b826`.

### EXP-054 — confirmed_local_content_scope

modechangeIOanyfriendlyleader;Firecannotmove,Movecannotfire;switchtoMoveblocksMoveinthesamephase,switchtoFireblocksFireinthesamephase;moveIOrequired,firedoesnotrequireorder;awersFire,rewersMove

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; 9.85 uzupełnia harmonogram ognia; źródło nie ustanawia dodatkowej akcji po switch.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R982: zmiana trybu przez IO od dowolnego friendly leader; Move nie strzela, Fire nie rusza. Switch to Move blokuje ruch w tej Orders Phase, switch to Fire blokuje fire w tej fazie. Ruch w Move wymaga IO, fire nie wymaga order. R982note zachowuje awers Fire/rewers Move. Brak nowej akcji po switch i brak certyfikacji ratingów żetonu.

R982: `/rules/34`, bajty[343925,349222); SHA `db2932e05afee950e1d27137b71fe09be42fd41a52f8e80905dc27726cf31a48`.
R982note: `/rules/35`, bajty[349228,352453); SHA `88bf7f560fd28fa8d2955805d683d0f7eac1210dac638fc5f483232a758bd6c6`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R982: zmiana trybu przez IO od dowolnego friendly leader; Move nie strzela, Fire nie rusza. Switch to Move blokuje ruch w tej Orders Phase, switch to Fire blokuje fire w tej fazie. Ruch w Move wymaga IO, fire nie wymaga order. R982note zachowuje awers Fire/rewers Move. Brak nowej akcji po switch i brak certyfikacji ratingów żetonu.

R982: `/rules/34`, bajty[416661,422148); SHA `c322a28fb1c69bff5deac677b5a8ee02c5c27f63d0f17bce8a72a482a530f988`.
R982note: `/rules/35`, bajty[422155,425494); SHA `9ac67925c35fae2788830f9c0809376ae5aace09ee195639c5f67b7240858bd0`.

### EXP-055 — confirmed_local_content_scope

atmostoneScorpioperhex,otherstackingrulesretained

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Pełna legalność współzajęcia wymaga general stacking.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R983 zachowuje maksimum jeden Scorpio na heks i all other stacking rules. Nie przyznaje automatycznej legalności współzajęcia. G-D983stack blocking=true dotyczy pełnych ograniczeń, nie znanego lokalnego maksimum.

R983: `/rules/36`, bajty[352459,356106); SHA `f7d2aafc87c8ed78040ffececeea0285fff874b6b06483f0065d8564c626e87f`.
G-D983stack: `/gaps/56`, bajty[555997,556446); SHA `2601f6668acf6d9ad7da7796f0daec6d1ddeca0042706531540d45ba973b2edd`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R983 zachowuje maksimum jeden Scorpio na heks i all other stacking rules. Nie przyznaje automatycznej legalności współzajęcia. G-D983stack blocking=true dotyczy pełnych ograniczeń, nie znanego lokalnego maksimum.

R983: `/rules/36`, bajty[425501,429280); SHA `7a009418ad0af36b8ee5ca3de17a068395e17db2e7da4760ace20689e5366e00`.
G-D983stack: `/gaps/56`, bajty[641759,642225); SHA `ce88ae13d5292724dbb7bb023a8021b917b69a71f72ac40d3693dab72de74ace`.

### EXP-056 — confirmed_local_content_scope

nofacing;allhexesFront;range/LOS/terrainnotwaived

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie znosi range/LOS/terrain.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R984: brak facing, ruch/fire w dowolnym kierunku niezależnie od orientacji counter, wszystkie heksy Front. Nie ma zniesienia mode, range/LOS lub terrain; nie oceniono zewnętrznych ograniczeń ani konkretnego strzału.

R984: `/rules/37`, bajty[356112,359528); SHA `de911fdc0696db757fc4653804f89e65ed4a57ec809e9dd48209d12f438a56a5`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R984: brak facing, ruch/fire w dowolnym kierunku niezależnie od orientacji counter, wszystkie heksy Front. Nie ma zniesienia mode, range/LOS lub terrain; nie oceniono zewnętrznych ograniczeń ani konkretnego strzału.

R984: `/rules/37`, bajty[429287,432825); SHA `1c7feae738ab6c980bff3d77751acadc52dc149fb5e6ab07b6dbfcb090e4ec60`.

### EXP-057 — confirmed_local_content_scope

ActiveFiremax2/GameTurnandmax1/friendlyOrdersPhaseinMovementMissilesegment;Once/Finished;afteractiveFire nootheractionthatphaseincludingRecovery

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Warunki range/LOS/MRRC i mode9.82 nadal obowiązują.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R985 zachowuje max 2 active shots/Game Turn, max 1/friendly Orders Phase w Movement and Missile Fire Segment, bez order. Pierwszy Once, drugi Finished w R985 i N985markers; grafika pokazuje oba. Po fire brak innych działań tej Orders Phase, w tym Recovery. Nie myli Game Turn z Orders Phase i nie przyznaje fire w Move.

N985markers: `/nodes/34`, bajty[150642,151434); SHA `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.
R985: `/rules/38`, bajty[359534,364613); SHA `9083d4f2690f24d2424f617dbf3a0b4481149a19932798070e26fcfe4b74207e`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R985 zachowuje max 2 active shots/Game Turn, max 1/friendly Orders Phase w Movement and Missile Fire Segment, bez order. Pierwszy Once, drugi Finished w R985 i N985markers; grafika pokazuje oba. Po fire brak innych działań tej Orders Phase, w tym Recovery. Nie myli Game Turn z Orders Phase i nie przyznaje fire w Move.

N985markers: `/nodes/34`, bajty[199790,200614); SHA `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.
R985: `/rules/38`, bajty[432832,438091); SHA `15e7d8e13c9489316c465caf3fb6ec40f605189e3145e013051d7ec031e0dea3`.

### EXP-058 — confirmed_local_content_scope

specialReactionFiremax2/enemyOrdersPhasein enemyMovementMissilesegment,includingduringenemyunitmovement;ordinary8.2ReactionFireforbidden;sourceanymovementdoesnotgrantScorpiofireinMovemode

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; No Reaction Fire any kind w Rampage9.14 nadal wyłącza trigger; zewnętrzny ogień i segment wymagają kontekstu.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R986 zachowuje specjalne 2 shots/enemy Orders Phase podczas enemy Movement and Missile Segment, także w trakcie ruchu enemy, i zakaz ordinary Reaction Fire 8.2. Conditions jawnie Fire mode under9.82. Once/Finished opisane w prozie; N986marker uczciwie odróżnia pokazane Once od Finished z tekstu. Lokalna propozycja nie uchyla zakazu Reaction Fire any kind podczas Rampage w R914; brak pary DEP-NEW-003 pozostaje SEM-006, bez naprawy/TP/FN.

N986marker: `/nodes/35`, bajty[151440,152165); SHA `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.
R986: `/rules/39`, bajty[364619,369123); SHA `64c29b4c0d2490544011c5ceb97b13ba7cd008eb4729f5055d1ca9665796cca7`.
R982: `/rules/34`, bajty[343925,349222); SHA `db2932e05afee950e1d27137b71fe09be42fd41a52f8e80905dc27726cf31a48`.
R914: `/rules/4`, bajty[191201,210006); SHA `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.
G-D986react: `/gaps/57`, bajty[556452,556928); SHA `5c69aa8c8b0faba50fa29d8c9273e2b22b62a835695ea49e08a452e3058eb9c8`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R986 zachowuje specjalne 2 shots/enemy Orders Phase podczas enemy Movement and Missile Segment, także w trakcie ruchu enemy, i zakaz ordinary Reaction Fire 8.2. Conditions jawnie Fire mode under9.82. Once/Finished opisane w prozie; N986marker uczciwie odróżnia pokazane Once od Finished z tekstu. Lokalna propozycja nie uchyla zakazu Reaction Fire any kind podczas Rampage w R914; brak pary DEP-NEW-003 pozostaje SEM-006, bez naprawy/TP/FN.

N986marker: `/nodes/35`, bajty[200621,201375); SHA `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.
R986: `/rules/39`, bajty[438098,442766); SHA `4cf0366781c3358abc98fff09da31c4c44d05d4c9dae4f10f7cd6443e2c714da`.
R982: `/rules/34`, bajty[416661,422148); SHA `c322a28fb1c69bff5deac677b5a8ee02c5c27f63d0f17bce8a72a482a530f988`.
R914: `/rules/4`, bajty[257723,277141); SHA `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.
G-D986react: `/gaps/57`, bajty[642232,642725); SHA `45e1f6dd8be4e7d1cef1f01dad4a06508b05e1d1f6481cbfc5c1c91423b06949`.

### EXP-059 — confirmed_local_content_scope

incur/recoverHitsasgeneralunits;Routimmediateelimination

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Trigger Rout i recovery amounts wymagają general rules.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R987 zachowuje incurring/recovering Cohesion Hits jak inne jednostki i natychmiastową eliminację przy Rout. Nie zgaduje triggeru Rout ani liczby odzyskiwanych Hits. R985 osobno zachowuje zakaz Recovery w fazie active fire; brak pełnej procedury recovery nie blokuje podanego lokalnego skutku Rout.

R987: `/rules/40`, bajty[369129,372461); SHA `0bdf1d408d64bb25daf21ea3f60f30aeb4ff91ce89afa5fc8f59908eba99ca8a`.
R985: `/rules/38`, bajty[359534,364613); SHA `9083d4f2690f24d2424f617dbf3a0b4481149a19932798070e26fcfe4b74207e`.
G-D987recovery: `/gaps/58`, bajty[556934,557400); SHA `f05e5cf84dbdbec0e8bcd4f8e06ff594e8d2905045f6e8871d7f21675b6073bb`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R987 zachowuje incurring/recovering Cohesion Hits jak inne jednostki i natychmiastową eliminację przy Rout. Nie zgaduje triggeru Rout ani liczby odzyskiwanych Hits. R985 osobno zachowuje zakaz Recovery w fazie active fire; brak pełnej procedury recovery nie blokuje podanego lokalnego skutku Rout.

R987: `/rules/40`, bajty[442773,446233); SHA `4319d42d58befea89683b3ce1da7b0ca03bb21ea982de7aaa504ab436290a229`.
R985: `/rules/38`, bajty[432832,438091); SHA `15e7d8e13c9489316c465caf3fb6ec40f605189e3145e013051d7ec031e0dea3`.
G-D987recovery: `/gaps/58`, bajty[642732,643215); SHA `bb0c068ff4e763a593c93bb17c8317e14f6459174ef40d45e192c2ce816db360`.

### EXP-060 — confirmed_local_content_scope

BI no terrainCohesionHits crossing/enteringpassableterrain or facingRough;MP/passabilitynotwaived;noColumn/PAW/OW

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Passability/koszt MP wymagają Movement Cost Chart, zakazy nie wymagają wykonania zabronionych procedur.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R991 zachowuje 0 terrain Cohesion Hits tylko przy crossing/entering passable terrain oraz facing Rough. Kontynuacja w prawej kolumnie zakazuje Column6.7, PAW6.8 i OW6.5. Nie wyzerowano MP ani nie zezwolono na impassable terrain. Definicje zakazanych procedur nonblocking nie stanowią zgody na ich wykonanie.

R991: `/rules/41`, bajty[372467,377217); SHA `54dcf8cd5202e6beebb7d87fcb4104ee5d6b6b3b8737e8ad794d6665eb6c387b`.
G-D991column: `/gaps/59`, bajty[557406,557849); SHA `21c7908a31249062fd79298c49cfa5ffc171fb65ba371f1fb3e9d75d91c5ae93`.
G-D991PAW: `/gaps/60`, bajty[557855,558300); SHA `40455f6e8efd482cb56671bc8b25c967ddc33317159ffccbeff0a89d09900951`.
G-D991OW: `/gaps/61`, bajty[558306,558728); SHA `4faa4ac08561677b7abc26d31318f745f9632dd5ea870a19688ba0be5069a2fa`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R991 zachowuje 0 terrain Cohesion Hits tylko przy crossing/entering passable terrain oraz facing Rough. Kontynuacja w prawej kolumnie zakazuje Column6.7, PAW6.8 i OW6.5. Nie wyzerowano MP ani nie zezwolono na impassable terrain. Definicje zakazanych procedur nonblocking nie stanowią zgody na ich wykonanie.

R991: `/rules/41`, bajty[446240,451161); SHA `5e41692ae51622c98f8ec0c02518e45efed39da42849c4d7693b20f9138a770c`.
G-D991column: `/gaps/59`, bajty[643222,643682); SHA `e00f043865aa4198721e59d3236abd096a7a37262bb6e862aa77311703e62b92`.
G-D991PAW: `/gaps/60`, bajty[643689,644151); SHA `d7f08e71c1cc07c87e8e1533bbf883c8e2f08e3eb81313bb09067428e67f4010`.
G-D991OW: `/gaps/61`, bajty[644158,644597); SHA `0d27fe434550bc8f13cd6a227585090b06c3852a1d7a95d6c6f1e7e147f9841a`.

### EXP-061 — confirmed_local_content_scope

Recoveryorderonly1CH;depletedBIeliminatedinsteadofRout;do notautomaticallytreatthateliminationasRoutforFerocity;fulltriggerorderingnotresolved

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Depleted stan i inne warunki recovery wymagają kontekstu; konflikt z Ferocity po depleted elimination nie rozstrzygnięty.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R993: tylko 1 Cohesion Hit/Recovery order; Depleted BI eliminated instead of Rout. Zestawione R994 ma trigger BI Routs, więc nie utożsamiono tego zastąpienia z jawnym Rout dla Ferocity. Pełne ordering i depletion/recovery eligibility pozostają poza zakresem; established_absent w exceptions nie jest ogólnym brakiem wyjątków.

R993: `/rules/42`, bajty[377223,381102); SHA `ac9f1b844e212d7c1ed2c0b307f8f974da613cd2137afc21a716bd6ff2f5d820`.
R994: `/rules/43`, bajty[381108,386923); SHA `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.
G-D993recovery: `/gaps/62`, bajty[558734,559207); SHA `e97246cb8c85acdf2b718f201480216826a1d7309f7055376dc6be6bff64c43e`.
G-D993depleted: `/gaps/63`, bajty[559213,559690); SHA `eed856d3e7aef25bab157896c5fe33fd9f5c71ae62f878fe5598bafe8cb973a3`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R993: tylko 1 Cohesion Hit/Recovery order; Depleted BI eliminated instead of Rout. Zestawione R994 ma trigger BI Routs, więc nie utożsamiono tego zastąpienia z jawnym Rout dla Ferocity. Pełne ordering i depletion/recovery eligibility pozostają poza zakresem; established_absent w exceptions nie jest ogólnym brakiem wyjątków.

R993: `/rules/42`, bajty[451168,455190); SHA `fdf01acb9629e037cb6f43e05f89f53320c84ff76245e149f5dce967553aa1f3`.
R994: `/rules/43`, bajty[455197,461221); SHA `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.
G-D993recovery: `/gaps/62`, bajty[644604,645094); SHA `837c301fff02606dca51181a6dac5eb9de810deadc48840a33793f4a1dae2a9c`.
G-D993depleted: `/gaps/63`, bajty[645101,645595); SHA `f761def146a8386ceaeed18b8712253451c0275245b4e3e13d05ab12485f9be1`.

### EXP-062 — confirmed_local_content_scope

BI startFerocity;BI PreShock-1DRM and defenders+2DRM inshownscope,othermodifiers/procedureunknown

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Inne DRM i Pre-Shock procedure nie są domknięte.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R994.conditions zachowuje start game Ferocity dla all BI. Action/parameters: własny Pre-Shock TQ -1 DRM, defending units +2 DRM. To nie modyfikatory wszystkich TQ checks, nie +2 dla BI. Brak scenariusza i base Pre-Shock nie blokuje znanych lokalnych operatorów przy zadanych faktach.

R994: `/rules/43`, bajty[381108,386923); SHA `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.
G-D994scenario: `/gaps/64`, bajty[559696,560235); SHA `5d919573808660c9c61d0d2b42e5ecf28e405da46551b15f001669dfe748d17b`.
G-D994pre: `/gaps/65`, bajty[560241,560701); SHA `21dadb238612c398fba0ce48743e0ec9cacb2d701e63cfa3b618d33628bfe9b1`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R994.conditions zachowuje start game Ferocity dla all BI. Action/parameters: własny Pre-Shock TQ -1 DRM, defending units +2 DRM. To nie modyfikatory wszystkich TQ checks, nie +2 dla BI. Brak scenariusza i base Pre-Shock nie blokuje znanych lokalnych operatorów przy zadanych faktach.

R994: `/rules/43`, bajty[455197,461221); SHA `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.
G-D994scenario: `/gaps/64`, bajty[645602,646158); SHA `e99c36601e444c56865de2229bbbc9901fea5df5b1d04556fa4885f1ae9b13e3`.
G-D994pre: `/gaps/65`, bajty[646165,646642); SHA `f0664691c0576667258d6f0baf116aa7bcc5a7f8a043000596482572a7323116`.

### EXP-063 — confirmed_local_content_scope

EachordinaryBI RouttriggersFerocitycheckagainstscenarioassignedleaderInitiative;DR<=retains,>losespermanentlyforthatleaderBIcommand,othersunaffected

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Scenario commander mapping i Initiative muszą być dostępne; depleted elimination ≠ jawny Rout trigger.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R994 zachowuje check each time BI Routs wobec Initiative leader przypisanego w scenario setup; DR<=Initiative zatrzymuje, wyższy trwale odbiera Ferocity BI tego dowódcy, inne commands bez skutku. Depleted elimination z R993 nie jest automatycznie tym triggerem. Nie wybrano dowódcy ani ratingu.

R994: `/rules/43`, bajty[381108,386923); SHA `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.
R993: `/rules/42`, bajty[377223,381102); SHA `ac9f1b844e212d7c1ed2c0b307f8f974da613cd2137afc21a716bd6ff2f5d820`.
G-D994scenario: `/gaps/64`, bajty[559696,560235); SHA `5d919573808660c9c61d0d2b42e5ecf28e405da46551b15f001669dfe748d17b`.
G-D994pre: `/gaps/65`, bajty[560241,560701); SHA `21dadb238612c398fba0ce48743e0ec9cacb2d701e63cfa3b618d33628bfe9b1`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R994 zachowuje check each time BI Routs wobec Initiative leader przypisanego w scenario setup; DR<=Initiative zatrzymuje, wyższy trwale odbiera Ferocity BI tego dowódcy, inne commands bez skutku. Depleted elimination z R993 nie jest automatycznie tym triggerem. Nie wybrano dowódcy ani ratingu.

R994: `/rules/43`, bajty[455197,461221); SHA `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.
R993: `/rules/42`, bajty[451168,455190); SHA `fdf01acb9629e037cb6f43e05f89f53320c84ff76245e149f5dce967553aa1f3`.
G-D994scenario: `/gaps/64`, bajty[645602,646158); SHA `e99c36601e444c56865de2229bbbc9901fea5df5b1d04556fa4885f1ae9b13e3`.
G-D994pre: `/gaps/65`, bajty[646165,646642); SHA `f0664691c0576667258d6f0baf116aa7bcc5a7f8a043000596482572a7323116`.

### EXP-064 — requires_context

Actualleader/Initiative/membership requires scenariosetup;no nearest/favorable default

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Actual leader, Initiative and BI command membership require scenario setup.; Jedno wskazane przypisanie scenario wraz z ratings, nie domyślny najbliższy leader.

**first-001: preserve_accepted_source_requirement_full_result_blocked**. Wcześniejszy owner status: reviewed.

R994/R995 odwołują się do scenario-assigned command, G-D994scenario i G-D995scenario jawnie blocking=true. Potrzebne actual leader, Initiative i BI membership nie zostały zastąpione najbliższym lub korzystnym leader. Propozycja przyjmuje poprawną potrzebę/blokadę źródła; brak danych wciąż blokuje pełne rzeczywiste zastosowanie, a zadane syntetyczne facts mają własny lokalny zakres.

R994: `/rules/43`, bajty[381108,386923); SHA `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.
R995: `/rules/44`, bajty[386929,392597); SHA `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.
G-D994scenario: `/gaps/64`, bajty[559696,560235); SHA `5d919573808660c9c61d0d2b42e5ecf28e405da46551b15f001669dfe748d17b`.
G-D994pre: `/gaps/65`, bajty[560241,560701); SHA `21dadb238612c398fba0ce48743e0ec9cacb2d701e63cfa3b618d33628bfe9b1`.
G-D995momentum: `/gaps/66`, bajty[560707,561203); SHA `0b956ea1ee6e93dea84faa748e30ad5008539edbd9c7469466919ced64317394`.
G-D995scenario: `/gaps/67`, bajty[561209,561684); SHA `bc53604b790254e2d489ca478c98c24fcc36710fa8c84e6f25661986168ce51f`.
G-D-ZOC-R995: `/gaps/80`, bajty[567564,568024); SHA `d47024d75386d2415530f183f901e005786e4f49d319ad6c14f96e4e64a6ca82`.

**context-01: preserve_accepted_source_requirement_full_result_blocked**. Wcześniejszy owner status: reviewed.

R994/R995 odwołują się do scenario-assigned command, G-D994scenario i G-D995scenario jawnie blocking=true. Potrzebne actual leader, Initiative i BI membership nie zostały zastąpione najbliższym lub korzystnym leader. Propozycja przyjmuje poprawną potrzebę/blokadę źródła; brak danych wciąż blokuje pełne rzeczywiste zastosowanie, a zadane syntetyczne facts mają własny lokalny zakres.

R994: `/rules/43`, bajty[455197,461221); SHA `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.
R995: `/rules/44`, bajty[461228,467103); SHA `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.
G-D994scenario: `/gaps/64`, bajty[645602,646158); SHA `e99c36601e444c56865de2229bbbc9901fea5df5b1d04556fa4885f1ae9b13e3`.
G-D994pre: `/gaps/65`, bajty[646165,646642); SHA `f0664691c0576667258d6f0baf116aa7bcc5a7f8a043000596482572a7323116`.
G-D995momentum: `/gaps/66`, bajty[646649,647162); SHA `5d49adeccbcf512657b27df883cae3717612a4a46771c714b339e43d411033cc`.
G-D995scenario: `/gaps/67`, bajty[647169,647661); SHA `3042e55550aa4d0b3526b7091ee210120cd7c48bcb016610a6aa8e1105b39d5d`.
G-D-ZOC-R995: `/gaps/80`, bajty[653762,654239); SHA `60d830f90cce5dc09348508a78b8687b9d873c9573527169061b07c277d90069`.

### EXP-065 — confirmed_local_content_scope

BI startMA+1 and commandingLeader-1allfirsttryMomentum;after>=2distinctBIofsamecommandenterenemyZOC,Impetuosity lastsrestofthatGameTurn thenlostforthatcommandonly

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Mapping command, ZOC i Momentum wymagają danych; lokalny czas wygaśnięcia jest jawny.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R995: wszystkie BI startują MA+1, leaders commanding BI -1 do all first-try Momentum rolls. Trigger >=2 BI units tego samego command entering enemy ZOC, a nie dwie wizyty jednej jednostki. Efekt trwa resztę tego Game Turn i wygasa potem tylko dla tego command. Nie natychmiast po triggerze ani dla całej armii.

R995: `/rules/44`, bajty[386929,392597); SHA `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.
G-D995momentum: `/gaps/66`, bajty[560707,561203); SHA `0b956ea1ee6e93dea84faa748e30ad5008539edbd9c7469466919ced64317394`.
G-D995scenario: `/gaps/67`, bajty[561209,561684); SHA `bc53604b790254e2d489ca478c98c24fcc36710fa8c84e6f25661986168ce51f`.
G-D-ZOC-R995: `/gaps/80`, bajty[567564,568024); SHA `d47024d75386d2415530f183f901e005786e4f49d319ad6c14f96e4e64a6ca82`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R995: wszystkie BI startują MA+1, leaders commanding BI -1 do all first-try Momentum rolls. Trigger >=2 BI units tego samego command entering enemy ZOC, a nie dwie wizyty jednej jednostki. Efekt trwa resztę tego Game Turn i wygasa potem tylko dla tego command. Nie natychmiast po triggerze ani dla całej armii.

R995: `/rules/44`, bajty[461228,467103); SHA `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.
G-D995momentum: `/gaps/66`, bajty[646649,647162); SHA `5d49adeccbcf512657b27df883cae3717612a4a46771c714b339e43d411033cc`.
G-D995scenario: `/gaps/67`, bajty[647169,647661); SHA `3042e55550aa4d0b3526b7091ee210120cd7c48bcb016610a6aa8e1105b39d5d`.
G-D-ZOC-R995: `/gaps/80`, bajty[653762,654239); SHA `60d830f90cce5dc09348508a78b8687b9d873c9573527169061b07c277d90069`.

### EXP-066 — requires_context

GallictransportCHCombatTablesignoreinstruction retained;exacttables/entriesrequirecontext alreadyRQ05scope

Lokalne ignore Chariots reference on Combat Tables zachowane. Do identyfikacji rzeczywistych wyłączanych entries potrzeba tabel; flags false pozostają oryginalne. .4d1 przyjęła literalny nakaz, nie wystarczalność blokady pełnego lookupu. SEM-012 pending, bez zgadywania tabel, nowego źródła lub twierdzenia o dokonanym złym lookupie.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Exact Combat Tables and relevant entries are required; no values are guessed.; Dokładne Combat Tables i ich chariot entries, decision owner o zakresie; nie traktować Sentinum/Telamon jako listy eligibility wszystkich LI.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R996note zachowuje ignore Chariots reference on Combat Tables; N996design nie tworzy dodatkowego skutku. N-14-S2 to dokładna instrukcja, N-14-S3 appearances Sentinum/Telamon, bez listy eligibility wszystkich LI. G-D996tables deklaruje potrzebę actual tables/entries, ale blocking=false; D996tables blocks_full_result=false. Lokalny zakaz użycia wiersza znany, konkretne identyfikowanie suppressowanych entries niezamknięte. Właściciel rozstrzyga wystarczalność jawnej blokady zależnego pełnego pytania. Nie ma konkretnego niepoprawnego lookupu, nie jest to automatyczny błąd odczytu lub FP.

N996design: `/nodes/30`, bajty[146679,147468); SHA `c01e2df13e259d2b65d4ec89dee199481937bd990757f3a83e9f9dc5ce3784dd`.
R996note: `/rules/45`, bajty[392603,396286); SHA `3dfdaccd8a573ddf99e083715c467fb8a36ec4ad52929c71b7259de8de628ab5`.
D996tables: `/dependencies/108`, bajty[512527,513635); SHA `1f7003a3d4d4e84827c18ca49ade9e7bb6d3e7bf41627b4af176911bda5c0b8a`.
G-D996tables: `/gaps/68`, bajty[561690,562253); SHA `4d25580273e2f47e9861742228dfda824e123a8c160529580af039237d78a715`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

R996note zachowuje ignore Chariots reference on Combat Tables; N996design nie tworzy dodatkowego skutku. N-14-S2 to dokładna instrukcja, N-14-S3 appearances Sentinum/Telamon, bez listy eligibility wszystkich LI. G-D996tables deklaruje potrzebę actual tables/entries, ale blocking=false; D996tables blocks_full_result=false. Lokalny zakaz użycia wiersza znany, konkretne identyfikowanie suppressowanych entries niezamknięte. Właściciel rozstrzyga wystarczalność jawnej blokady zależnego pełnego pytania. Nie ma konkretnego niepoprawnego lookupu, nie jest to automatyczny błąd odczytu lub FP.

N996design: `/nodes/30`, bajty[195676,196492); SHA `7ad32edfe26a51d99e6ab415bbb1f85fc82f8061c5071dd33970b43437e5378f`.
R996note: `/rules/45`, bajty[467110,470918); SHA `88c04eae1baf89929461610b1d701ea1201da58987d814350fdcfb5516d2ec76`.
D996tables: `/dependencies/108`, bajty[590968,592103); SHA `f4555792332ddf87bf519ee6a9231583e2516e597f413bb1afa7a4b5ea93bccb`.
G-D996tables: `/gaps/68`, bajty[647668,648248); SHA `709d00bec15889990cc4d425d9ee7b2f041b8814b8f0bf029e59286bcc067d4b`.

### EXP-067 — confirmed_local_content_scope

CHonlyMA,noSize/TQ;cannotmoveincludingOWwithouteligibleLI;enemycombatmovingadjacenttosolitaryCH eliminatesit;staticadjacency notthegivenmovementtrigger

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Eligibility LI scenariuszowa nieuzupełniona; samotny CH da się ocenić lokalnie.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996a: CH ma tylko MA, brak Size/TQ. Bez stacked eligible LI zakaz wszelkiego ruchu, także OW. Enemy combat unit any type moving adjacent do CH alone eliminuje go natychmiast. Static adjacency nie jest podanym triggerem. Szerszy time_limits mówi qualifying adjacency; operacyjny trigger pozostaje w action_effect. Nie nadaje się CH ratingów Roman top-unit.

R996a: `/rules/46`, bajty[396292,400339); SHA `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.
R996b: `/rules/47`, bajty[400345,409010); SHA `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.
R996c: `/rules/48`, bajty[409016,413605); SHA `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.
R996d: `/rules/49`, bajty[413611,417619); SHA `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.
G-D996eligible: `/gaps/69`, bajty[562259,562746); SHA `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.
G-D996OW: `/gaps/70`, bajty[562752,563192); SHA `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.
G-D996stack: `/gaps/71`, bajty[563198,563649); SHA `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.
G-D996movement: `/gaps/72`, bajty[563655,564128); SHA `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.
G-D996MRRC: `/gaps/73`, bajty[564134,564595); SHA `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.
G-D996supply: `/gaps/74`, bajty[564601,565114); SHA `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.
G-D996HD: `/gaps/75`, bajty[565120,565603); SHA `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996a: CH ma tylko MA, brak Size/TQ. Bez stacked eligible LI zakaz wszelkiego ruchu, także OW. Enemy combat unit any type moving adjacent do CH alone eliminuje go natychmiast. Static adjacency nie jest podanym triggerem. Szerszy time_limits mówi qualifying adjacency; operacyjny trigger pozostaje w action_effect. Nie nadaje się CH ratingów Roman top-unit.

R996a: `/rules/46`, bajty[470925,475124); SHA `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.
R996b: `/rules/47`, bajty[475131,484102); SHA `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.
R996c: `/rules/48`, bajty[484109,488868); SHA `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.
R996d: `/rules/49`, bajty[488875,493035); SHA `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.
G-D996eligible: `/gaps/69`, bajty[648255,648759); SHA `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.
G-D996OW: `/gaps/70`, bajty[648766,649223); SHA `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.
G-D996stack: `/gaps/71`, bajty[649230,649698); SHA `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.
G-D996movement: `/gaps/72`, bajty[649705,650195); SHA `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.
G-D996MRRC: `/gaps/73`, bajty[650202,650680); SHA `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.
G-D996supply: `/gaps/74`, bajty[650687,651217); SHA `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.
G-D996HD: `/gaps/75`, bajty[651224,651724); SHA `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

### EXP-068 — confirmed_local_content_scope

oneLIperCH,CHtopdenotesmounted,combinedsingleforstackingbutotherrestrictionsretained

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie używać roman top/TQ jako zasad CH; brak TQ/Size CH zachować.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996b zachowuje jeden LI na CH, CH na górze oznacza mounted, kombinacja single unit tylko dla stacking; all other restrictions dla CH+LI i CH alone nadal obowiązują. Continuation PDF36right→37left zawiera pełne zdanie. Nie stosuje Roman top/TQ do transport CH i nie przyznaje pełnej legalności stacking.

R996a: `/rules/46`, bajty[396292,400339); SHA `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.
R996b: `/rules/47`, bajty[400345,409010); SHA `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.
R996c: `/rules/48`, bajty[409016,413605); SHA `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.
R996d: `/rules/49`, bajty[413611,417619); SHA `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.
G-D996eligible: `/gaps/69`, bajty[562259,562746); SHA `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.
G-D996OW: `/gaps/70`, bajty[562752,563192); SHA `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.
G-D996stack: `/gaps/71`, bajty[563198,563649); SHA `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.
G-D996movement: `/gaps/72`, bajty[563655,564128); SHA `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.
G-D996MRRC: `/gaps/73`, bajty[564134,564595); SHA `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.
G-D996supply: `/gaps/74`, bajty[564601,565114); SHA `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.
G-D996HD: `/gaps/75`, bajty[565120,565603); SHA `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996b zachowuje jeden LI na CH, CH na górze oznacza mounted, kombinacja single unit tylko dla stacking; all other restrictions dla CH+LI i CH alone nadal obowiązują. Continuation PDF36right→37left zawiera pełne zdanie. Nie stosuje Roman top/TQ do transport CH i nie przyznaje pełnej legalności stacking.

R996a: `/rules/46`, bajty[470925,475124); SHA `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.
R996b: `/rules/47`, bajty[475131,484102); SHA `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.
R996c: `/rules/48`, bajty[484109,488868); SHA `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.
R996d: `/rules/49`, bajty[488875,493035); SHA `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.
G-D996eligible: `/gaps/69`, bajty[648255,648759); SHA `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.
G-D996OW: `/gaps/70`, bajty[648766,649223); SHA `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.
G-D996stack: `/gaps/71`, bajty[649230,649698); SHA `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.
G-D996movement: `/gaps/72`, bajty[649705,650195); SHA `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.
G-D996MRRC: `/gaps/73`, bajty[650202,650680); SHA `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.
G-D996supply: `/gaps/74`, bajty[650687,651217); SHA `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.
G-D996HD: `/gaps/75`, bajty[651224,651724); SHA `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

### EXP-069 — confirmed_local_content_scope

mount/dismount0MP/CH;dismountcontinueonlyifcomboMPspent<LIprintedMA,remainingdifference;mountremainingCHMAminusLIalreadyusedMP

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Ocenia się lokalny budżet przy supplied eligibility, MA i MP; trasa wymaga tabeli.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996b: mount/dismount 0 MP i 0 Cohesion Hits dla LI. Dismount dalszy ruch tylko gdy combo MPs used < LI printed MA, pozostałe MP równe różnicy. Mount pozwala kontynuować jako CH do CH MA minus MPs already used przez LI. Strict < i printed LI MA zachowane; nie odtworzono MP od zera, żadna trasa/eligibility/MA nie została zgadnięta.

R996a: `/rules/46`, bajty[396292,400339); SHA `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.
R996b: `/rules/47`, bajty[400345,409010); SHA `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.
R996c: `/rules/48`, bajty[409016,413605); SHA `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.
R996d: `/rules/49`, bajty[413611,417619); SHA `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.
G-D996eligible: `/gaps/69`, bajty[562259,562746); SHA `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.
G-D996OW: `/gaps/70`, bajty[562752,563192); SHA `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.
G-D996stack: `/gaps/71`, bajty[563198,563649); SHA `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.
G-D996movement: `/gaps/72`, bajty[563655,564128); SHA `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.
G-D996MRRC: `/gaps/73`, bajty[564134,564595); SHA `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.
G-D996supply: `/gaps/74`, bajty[564601,565114); SHA `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.
G-D996HD: `/gaps/75`, bajty[565120,565603); SHA `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996b: mount/dismount 0 MP i 0 Cohesion Hits dla LI. Dismount dalszy ruch tylko gdy combo MPs used < LI printed MA, pozostałe MP równe różnicy. Mount pozwala kontynuować jako CH do CH MA minus MPs already used przez LI. Strict < i printed LI MA zachowane; nie odtworzono MP od zera, żadna trasa/eligibility/MA nie została zgadnięta.

R996a: `/rules/46`, bajty[470925,475124); SHA `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.
R996b: `/rules/47`, bajty[475131,484102); SHA `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.
R996c: `/rules/48`, bajty[484109,488868); SHA `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.
R996d: `/rules/49`, bajty[488875,493035); SHA `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.
G-D996eligible: `/gaps/69`, bajty[648255,648759); SHA `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.
G-D996OW: `/gaps/70`, bajty[648766,649223); SHA `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.
G-D996stack: `/gaps/71`, bajty[649230,649698); SHA `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.
G-D996movement: `/gaps/72`, bajty[649705,650195); SHA `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.
G-D996MRRC: `/gaps/73`, bajty[650202,650680); SHA `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.
G-D996supply: `/gaps/74`, bajty[650687,651217); SHA `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.
G-D996HD: `/gaps/75`, bajty[651224,651724); SHA `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

### EXP-070 — confirmed_local_content_scope

MovementCostChart governsCHMP/prohibitions;movementCohesionHitsLIonly,notCH;no waiverofterrainprohibitions

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Konkretna trasa bez Movement Cost Chart pozostaje zablokowana.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996b zachowuje CH MP costs oraz zakazy entering/crossing według Movement Cost Chart przy LI. Movement/Terrain Cohesion Hits do LI only, CH ich nie otrzymuje. G-D996movement blocking=true dla konkretnej trasy. To nie zwolnienie z zakazu terenu ani zwolnienie LI z wszystkich Hits.

R996a: `/rules/46`, bajty[396292,400339); SHA `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.
R996b: `/rules/47`, bajty[400345,409010); SHA `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.
R996c: `/rules/48`, bajty[409016,413605); SHA `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.
R996d: `/rules/49`, bajty[413611,417619); SHA `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.
G-D996eligible: `/gaps/69`, bajty[562259,562746); SHA `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.
G-D996OW: `/gaps/70`, bajty[562752,563192); SHA `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.
G-D996stack: `/gaps/71`, bajty[563198,563649); SHA `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.
G-D996movement: `/gaps/72`, bajty[563655,564128); SHA `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.
G-D996MRRC: `/gaps/73`, bajty[564134,564595); SHA `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.
G-D996supply: `/gaps/74`, bajty[564601,565114); SHA `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.
G-D996HD: `/gaps/75`, bajty[565120,565603); SHA `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996b zachowuje CH MP costs oraz zakazy entering/crossing według Movement Cost Chart przy LI. Movement/Terrain Cohesion Hits do LI only, CH ich nie otrzymuje. G-D996movement blocking=true dla konkretnej trasy. To nie zwolnienie z zakazu terenu ani zwolnienie LI z wszystkich Hits.

R996a: `/rules/46`, bajty[470925,475124); SHA `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.
R996b: `/rules/47`, bajty[475131,484102); SHA `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.
R996c: `/rules/48`, bajty[484109,488868); SHA `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.
R996d: `/rules/49`, bajty[488875,493035); SHA `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.
G-D996eligible: `/gaps/69`, bajty[648255,648759); SHA `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.
G-D996OW: `/gaps/70`, bajty[648766,649223); SHA `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.
G-D996stack: `/gaps/71`, bajty[649230,649698); SHA `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.
G-D996movement: `/gaps/72`, bajty[649705,650195); SHA `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.
G-D996MRRC: `/gaps/73`, bajty[650202,650680); SHA `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.
G-D996supply: `/gaps/74`, bajty[650687,651217); SHA `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.
G-D996HD: `/gaps/75`, bajty[651224,651724); SHA `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

### EXP-071 — confirmed_local_content_scope

repeat-movementHitexceptiononlyentireOrdersPhasemounted;partialphasemountinsufficient

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; General repeat movement i pozostałe terrain Hits oddzielnie.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996c: zwolnienie LI z second/third movement Hits w Game Turn tylko jeśli entire Orders Phase mounted. Wybrany literalny cytat urywa się przed if, lecz conditions i action_effect zachowują całe ograniczenie. Nie przyznano zwolnienia za częściowe mount lub dla terrain Hits.

R996a: `/rules/46`, bajty[396292,400339); SHA `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.
R996b: `/rules/47`, bajty[400345,409010); SHA `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.
R996c: `/rules/48`, bajty[409016,413605); SHA `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.
R996d: `/rules/49`, bajty[413611,417619); SHA `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.
G-D996eligible: `/gaps/69`, bajty[562259,562746); SHA `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.
G-D996OW: `/gaps/70`, bajty[562752,563192); SHA `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.
G-D996stack: `/gaps/71`, bajty[563198,563649); SHA `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.
G-D996movement: `/gaps/72`, bajty[563655,564128); SHA `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.
G-D996MRRC: `/gaps/73`, bajty[564134,564595); SHA `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.
G-D996supply: `/gaps/74`, bajty[564601,565114); SHA `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.
G-D996HD: `/gaps/75`, bajty[565120,565603); SHA `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996c: zwolnienie LI z second/third movement Hits w Game Turn tylko jeśli entire Orders Phase mounted. Wybrany literalny cytat urywa się przed if, lecz conditions i action_effect zachowują całe ograniczenie. Nie przyznano zwolnienia za częściowe mount lub dla terrain Hits.

R996a: `/rules/46`, bajty[470925,475124); SHA `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.
R996b: `/rules/47`, bajty[475131,484102); SHA `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.
R996c: `/rules/48`, bajty[484109,488868); SHA `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.
R996d: `/rules/49`, bajty[488875,493035); SHA `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.
G-D996eligible: `/gaps/69`, bajty[648255,648759); SHA `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.
G-D996OW: `/gaps/70`, bajty[648766,649223); SHA `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.
G-D996stack: `/gaps/71`, bajty[649230,649698); SHA `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.
G-D996movement: `/gaps/72`, bajty[649705,650195); SHA `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.
G-D996MRRC: `/gaps/73`, bajty[650202,650680); SHA `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.
G-D996supply: `/gaps/74`, bajty[650687,651217); SHA `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.
G-D996HD: `/gaps/75`, bajty[651224,651724); SHA `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

### EXP-072 — confirmed_local_content_scope

mountedLInoShockattack,mustdismount;defendsasLI,notfullattackpermissionafterdismount

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Dismount nie dowodzi legalności późniejszego attack bez pozostałych warunków.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996c jawnie Mounted LI cannot Shock attack; must dismount; defends as LI. Dismount jest konieczny, nie stanowi pełnej zgody na późniejszy attack bez pozostałych warunków. Nie zamieniono defend as LI na attack jako cavalry.

R996a: `/rules/46`, bajty[396292,400339); SHA `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.
R996b: `/rules/47`, bajty[400345,409010); SHA `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.
R996c: `/rules/48`, bajty[409016,413605); SHA `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.
R996d: `/rules/49`, bajty[413611,417619); SHA `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.
G-D996eligible: `/gaps/69`, bajty[562259,562746); SHA `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.
G-D996OW: `/gaps/70`, bajty[562752,563192); SHA `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.
G-D996stack: `/gaps/71`, bajty[563198,563649); SHA `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.
G-D996movement: `/gaps/72`, bajty[563655,564128); SHA `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.
G-D996MRRC: `/gaps/73`, bajty[564134,564595); SHA `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.
G-D996supply: `/gaps/74`, bajty[564601,565114); SHA `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.
G-D996HD: `/gaps/75`, bajty[565120,565603); SHA `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996c jawnie Mounted LI cannot Shock attack; must dismount; defends as LI. Dismount jest konieczny, nie stanowi pełnej zgody na późniejszy attack bez pozostałych warunków. Nie zamieniono defend as LI na attack jako cavalry.

R996a: `/rules/46`, bajty[470925,475124); SHA `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.
R996b: `/rules/47`, bajty[475131,484102); SHA `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.
R996c: `/rules/48`, bajty[484109,488868); SHA `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.
R996d: `/rules/49`, bajty[488875,493035); SHA `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.
G-D996eligible: `/gaps/69`, bajty[648255,648759); SHA `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.
G-D996OW: `/gaps/70`, bajty[648766,649223); SHA `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.
G-D996stack: `/gaps/71`, bajty[649230,649698); SHA `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.
G-D996movement: `/gaps/72`, bajty[649705,650195); SHA `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.
G-D996MRRC: `/gaps/73`, bajty[650202,650680); SHA `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.
G-D996supply: `/gaps/74`, bajty[650687,651217); SHA `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.
G-D996HD: `/gaps/75`, bajty[651224,651724); SHA `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

### EXP-073 — confirmed_local_content_scope

Mounted LI uses Mounted Javelin MRRC, is exempt from Missile Supply 8.17 while mounted, removes LOW/NO on mounting, and uses H&D as cavalry. No post-dismount supply state or equivalence with the hypothesized 9.13 row is inferred.

Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Nie zgadywać podaży po późniejszym dismount ani pełnego MRRC/H&D; display annotation06c zachowuje original helper.

**first-001: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996d zachowuje dokładnie nazwę Mounted Javelin MRRC, exemption Missile Supply8.17 while mounted, remove LOW/NO when mounts i H&D as cavalry. Nie zgaduje post-dismount supply, nie utożsamia tej row z hipotetycznym 9.13. G-D996MRRC/HD blocking=true; nonblocking supply dotyczy znanego lokalnego wyjątku/marker removal, bez rozstrzygania pełnej procedury.

R996a: `/rules/46`, bajty[396292,400339); SHA `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.
R996b: `/rules/47`, bajty[400345,409010); SHA `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.
R996c: `/rules/48`, bajty[409016,413605); SHA `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.
R996d: `/rules/49`, bajty[413611,417619); SHA `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.
G-D996eligible: `/gaps/69`, bajty[562259,562746); SHA `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.
G-D996OW: `/gaps/70`, bajty[562752,563192); SHA `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.
G-D996stack: `/gaps/71`, bajty[563198,563649); SHA `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.
G-D996movement: `/gaps/72`, bajty[563655,564128); SHA `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.
G-D996MRRC: `/gaps/73`, bajty[564134,564595); SHA `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.
G-D996supply: `/gaps/74`, bajty[564601,565114); SHA `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.
G-D996HD: `/gaps/75`, bajty[565120,565603); SHA `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

**context-01: preserve_accepted_local_scope**. Wcześniejszy owner status: reviewed.

R996d zachowuje dokładnie nazwę Mounted Javelin MRRC, exemption Missile Supply8.17 while mounted, remove LOW/NO when mounts i H&D as cavalry. Nie zgaduje post-dismount supply, nie utożsamia tej row z hipotetycznym 9.13. G-D996MRRC/HD blocking=true; nonblocking supply dotyczy znanego lokalnego wyjątku/marker removal, bez rozstrzygania pełnej procedury.

R996a: `/rules/46`, bajty[470925,475124); SHA `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.
R996b: `/rules/47`, bajty[475131,484102); SHA `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.
R996c: `/rules/48`, bajty[484109,488868); SHA `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.
R996d: `/rules/49`, bajty[488875,493035); SHA `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.
G-D996eligible: `/gaps/69`, bajty[648255,648759); SHA `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.
G-D996OW: `/gaps/70`, bajty[648766,649223); SHA `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.
G-D996stack: `/gaps/71`, bajty[649230,649698); SHA `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.
G-D996movement: `/gaps/72`, bajty[649705,650195); SHA `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.
G-D996MRRC: `/gaps/73`, bajty[650202,650680); SHA `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.
G-D996supply: `/gaps/74`, bajty[650687,651217); SHA `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.
G-D996HD: `/gaps/75`, bajty[651224,651724); SHA `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

### EXP-074 — requires_context

Confirm actualidentifiedunit TQ/MA before concreteuse; not alltinygraphicratings were individuallyverified inthisreview. SyntheticinputTQ6 doesnotestablishactualLeaderElephantTQ. Keeprequires_context foractualvalues.

Modele zachowują visible glyphs i jawnie wykluczają game-wide/rating-position meanings. .4d4 potwierdziła Scorpio/markery w tym zakresie. Nie dostarcza to zidentyfikowanego rzeczywistego TQ/MA ani osobnej conditional blocking deklaracji; SEM-013 nadal pending. Syntetyczne TQ6 nie staje się realnym ratingiem jednostki.

Wyłączenia: any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed; Actual identified counter TQ/MA and glyph values remain unconfirmed; criticality is conditional on changing outcome or legality.; Wybrany żeton/parametr z dokładnym źródłem i przeglądem, tylko jeśli sytuacja go potrzebuje.

**first-001: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

N911counter/N921counter/N981counter podają visible glyphs, lecz wyraźnie wykluczają game-wide values i rating-position inference. N966diagram mówi illustrative, not general Roman parameters; N985markers/N986marker to stany markerów. Brak twierdzenia o realnym Leader Elephant TQ6. Równocześnie nie ma osobnego gap ani jawnej conditional blocking deklaracji actual identified TQ/MA przed concrete use. Właściciel rozstrzyga, czy zapis illustrative wystarcza dla ograniczonego wymagania EXP-074. Same oględziny paneli/states nie certyfikują małych ratingów, tożsamości konkretnych jednostek ani 64 granic glifów. Criticality pozostaje conditional_on_concrete_parameter_use.

N911counter: `/nodes/31`, bajty[147474,148541); SHA `23d5455d6e3e846f2793ab9162a4d52e351dec50fdbb6c82f9bbdf60726cf009`.
N921counter: `/nodes/32`, bajty[148547,149599); SHA `30e857892be2b6c8be03571a7cf4d4176065f50d0ebbc1464ce5742405a3dc86`.
N966diagram: `/nodes/7`, bajty[128977,130323); SHA `f5c32b1dae24067c8069c9f6a259e1da4cd473f61255ce80b5b070a71cc69689`.
N981counter: `/nodes/33`, bajty[149605,150636); SHA `5598ad644a67222e29a3ec1778f8d63074add8759087c77097a583b05c918b7b`.
N985markers: `/nodes/34`, bajty[150642,151434); SHA `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.
N986marker: `/nodes/35`, bajty[151440,152165); SHA `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.

**context-01: preserve_old_pending_no_variant_chosen**. Wcześniejszy owner status: pending.

N911counter/N921counter/N981counter podają visible glyphs, lecz wyraźnie wykluczają game-wide values i rating-position inference. N966diagram mówi illustrative, not general Roman parameters; N985markers/N986marker to stany markerów. Brak twierdzenia o realnym Leader Elephant TQ6. Równocześnie nie ma osobnego gap ani jawnej conditional blocking deklaracji actual identified TQ/MA przed concrete use. Właściciel rozstrzyga, czy zapis illustrative wystarcza dla ograniczonego wymagania EXP-074. Same oględziny paneli/states nie certyfikują małych ratingów, tożsamości konkretnych jednostek ani 64 granic glifów. Criticality pozostaje conditional_on_concrete_parameter_use.

N911counter: `/nodes/31`, bajty[196499,197607); SHA `7b6b333e688ac23f557a2c1e1344876b6770501901c9407247d341dac0c97653`.
N921counter: `/nodes/32`, bajty[197614,198706); SHA `0c1388f9709c55e4e5a45fc7686880da9f5078247249284e32ca56de85771f8b`.
N966diagram: `/nodes/7`, bajty[177283,178673); SHA `36e8f4cd62347156e4d08983cd3b50a484a73b8478deddb5b4167d954c4d364d`.
N981counter: `/nodes/33`, bajty[198713,199783); SHA `a40fc3ffd54bad133ba38846aeb3aab44303b5e8c073a04740d3cbc39f922451`.
N985markers: `/nodes/34`, bajty[199790,200614); SHA `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.
N986marker: `/nodes/35`, bajty[200621,201375); SHA `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.

## Wszystkie207 pozycje inwentarza

| ID | First — dokładna wcześniejsza ocena | Context — dokładna wcześniejsza ocena |
|---|---|---|
| H-9.0 | bounded_supported | bounded_supported |
| H-9.1 | bounded_supported | bounded_supported |
| H-9.2 | bounded_supported | bounded_supported |
| H-9.3 | bounded_supported | bounded_supported |
| H-9.4 | bounded_supported | bounded_supported |
| H-9.5 | bounded_supported | bounded_supported |
| H-9.6 | bounded_supported | bounded_supported |
| H-9.7 | bounded_supported | bounded_supported |
| H-9.8 | bounded_supported | bounded_supported |
| H-9.9 | bounded_supported | bounded_supported |
| R-9.11 | bounded_label_supported | bounded_label_supported |
| C-9.11-01 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-03 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-04 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-05 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-06 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-07 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-08 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-09 | bounded_clause_supported | bounded_clause_supported |
| C-9.11-10 | bounded_clause_supported | bounded_clause_supported |
| R-9.12 | bounded_label_supported | bounded_label_supported |
| C-9.12-01 | bounded_clause_supported | bounded_clause_supported |
| C-9.12-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.12-03 | bounded_clause_supported | bounded_clause_supported |
| R-9.13 | bounded_label_supported | bounded_label_supported |
| C-9.13-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.14 | bounded_label_supported | bounded_label_supported |
| C-9.14-01 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-03 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-04 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-05 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-06 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-07 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-08 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-09 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-10 | bounded_clause_supported | bounded_clause_supported |
| C-9.14-11 | bounded_clause_supported | bounded_clause_supported |
| R-9.15 | bounded_label_supported | bounded_label_supported |
| C-9.15-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.16 | bounded_label_supported | bounded_label_supported |
| C-9.16-01 | bounded_literal_prior_pending | bounded_literal_prior_pending |
| R-9.17 | bounded_label_supported | bounded_label_supported |
| C-9.17-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.18 | bounded_label_supported | bounded_label_supported |
| C-9.18-01 | bounded_literal_prior_pending | bounded_literal_prior_pending |
| R-9.19 | bounded_label_supported | bounded_label_supported |
| C-9.19-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.21 | bounded_label_supported | bounded_label_supported |
| C-9.21-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.22 | bounded_label_supported | bounded_label_supported |
| C-9.22-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.23 | bounded_label_supported | bounded_label_supported |
| C-9.23-01 | bounded_clause_supported | bounded_clause_supported |
| C-9.23-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.23-03 | bounded_clause_supported | bounded_clause_supported |
| C-9.23-04 | bounded_clause_supported | bounded_clause_supported |
| C-9.23-05 | bounded_clause_supported | bounded_clause_supported |
| C-9.23-06 | bounded_clause_supported | bounded_clause_supported |
| R-9.24 | bounded_label_supported | bounded_label_supported |
| C-9.24-01 | bounded_clause_supported | bounded_clause_supported |
| C-9.24-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.24-03 | bounded_clause_supported | bounded_clause_supported |
| C-9.24-04 | bounded_clause_supported | bounded_clause_supported |
| C-9.24-05 | bounded_clause_supported | bounded_clause_supported |
| R-9.31 | bounded_label_supported | bounded_label_supported |
| C-9.31-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.32 | bounded_label_supported | bounded_label_supported |
| C-9.32-01 | bounded_local_and_supplied_context_supported | bounded_local_and_supplied_context_supported |
| R-9.41 | bounded_label_supported | bounded_label_supported |
| C-9.41-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.51 | bounded_label_supported | bounded_label_supported |
| C-9.51-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.52 | bounded_label_supported | bounded_label_supported |
| C-9.52-01 | bounded_clause_supported | bounded_clause_supported |
| C-9.52-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.52-03 | bounded_clause_supported | bounded_clause_supported |
| C-9.52-04 | bounded_clause_supported | bounded_clause_supported |
| C-9.52-05 | bounded_clause_supported | bounded_clause_supported |
| C-9.52-06 | bounded_clause_supported | bounded_clause_supported |
| R-9.53 | bounded_label_supported | bounded_label_supported |
| C-9.53-01 | bounded_clause_supported | bounded_clause_supported |
| C-9.53-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.53-03 | bounded_clause_supported | bounded_clause_supported |
| C-9.53-04 | bounded_clause_supported | bounded_clause_supported |
| C-9.53-05 | bounded_clause_supported | bounded_clause_supported |
| C-9.53-06 | bounded_clause_supported | bounded_clause_supported |
| C-9.53-07 | bounded_clause_supported | bounded_clause_supported |
| C-9.53-08 | bounded_literal_prior_pending | bounded_literal_prior_pending |
| R-9.61 | bounded_label_supported | bounded_label_supported |
| C-9.61-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.62 | bounded_label_supported | bounded_label_supported |
| C-9.62-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.63 | bounded_label_supported | bounded_label_supported |
| C-9.63-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.64 | bounded_label_supported | bounded_label_supported |
| C-9.64-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.65 | bounded_label_supported | bounded_label_supported |
| C-9.65-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.66 | bounded_label_supported | bounded_label_supported |
| C-9.66-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.67 | bounded_label_supported | bounded_label_supported |
| C-9.67-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.68 | bounded_label_supported | bounded_label_supported |
| C-9.68-01 | bounded_clause_supported | bounded_clause_supported |
| R-9.71 | bounded_label_supported | bounded_label_supported |
| C-9.71-01 | bounded_literal_prior_pending | bounded_literal_prior_pending |
| C-9.71-02 | bounded_clause_supported | bounded_clause_supported |
| C-9.71-03 | bounded_clause_supported | bounded_clause_supported |
| R-9.72 | bounded_label_supported | bounded_label_supported |
| C-9.72-01 | bounded_literal_prior_pending | bounded_literal_prior_pending |
| R-9.81 | bounded_label_supported | bounded_label_supported |
| C-9.81-01 | bounded_content_supported | bounded_content_supported |
| R-9.82 | bounded_label_supported | bounded_label_supported |
| C-9.82-01 | bounded_content_supported | bounded_content_supported |
| R-9.83 | bounded_label_supported | bounded_label_supported |
| C-9.83-01 | bounded_content_supported | bounded_content_supported |
| R-9.84 | bounded_label_supported | bounded_label_supported |
| C-9.84-01 | bounded_content_supported | bounded_content_supported |
| R-9.85 | bounded_label_supported | bounded_label_supported |
| C-9.85-01 | bounded_content_supported | bounded_content_supported |
| R-9.86 | bounded_label_supported | bounded_label_supported |
| C-9.86-01 | bounded_content_supported | bounded_content_supported |
| R-9.87 | bounded_label_supported | bounded_label_supported |
| C-9.87-01 | bounded_content_supported | bounded_content_supported |
| R-9.91 | bounded_label_supported | bounded_label_supported |
| C-9.91-01 | bounded_heading_role_supported | bounded_heading_role_supported |
| C-9.91-02 | bounded_content_supported | bounded_content_supported |
| R-9.93 | bounded_label_supported | bounded_label_supported |
| C-9.93-01 | bounded_heading_role_supported | bounded_heading_role_supported |
| C-9.93-02 | bounded_content_supported | bounded_content_supported |
| C-9.93-03 | bounded_content_supported | bounded_content_supported |
| R-9.94 | bounded_label_supported | bounded_label_supported |
| C-9.94-01 | bounded_heading_role_supported | bounded_heading_role_supported |
| C-9.94-02 | bounded_content_supported | bounded_content_supported |
| C-9.94-03 | bounded_content_supported | bounded_content_supported |
| R-9.95 | bounded_label_supported | bounded_label_supported |
| C-9.95-01 | bounded_heading_role_supported | bounded_heading_role_supported |
| C-9.95-02 | mixed_operative_supported_explanation_omitted | mixed_operative_supported_explanation_omitted |
| R-9.96 | bounded_label_supported | bounded_label_supported |
| C-9.96-01 | bounded_heading_role_supported | bounded_heading_role_supported |
| C-9.96-02 | bounded_content_supported | bounded_content_supported |
| C-9.96-03 | bounded_content_supported | bounded_content_supported |
| C-9.96-04 | bounded_heading_role_supported | bounded_heading_role_supported |
| C-9.96-05 | bounded_content_supported | bounded_content_supported |
| C-9.96-06 | bounded_content_supported | bounded_content_supported |
| C-9.96-07 | bounded_content_supported | bounded_content_supported |
| C-9.7-01 | mixed_operative_supported_rationale_omitted | mixed_operative_supported_rationale_omitted |
| N-01 | bounded_supported | bounded_supported |
| N-02 | bounded_supported | bounded_supported |
| N-03 | bounded_supported | bounded_supported |
| N-04 | bounded_structured_not_literal | bounded_structured_not_literal |
| N-05 | content_summary_omits_central_statement_evidence_retains_it | content_summary_omits_central_statement_evidence_retains_it |
| N-06 | bounded_supported | bounded_supported |
| N-07 | bounded_supported | bounded_supported |
| N-08 | bounded_supported | bounded_supported |
| N-09 | bounded_supported_context_missing | bounded_supported_context_missing |
| N-10 | bounded_supported | bounded_supported |
| N-11 | bounded_supported | bounded_supported |
| N-12 | bounded_supported | bounded_supported |
| N-13 | bounded_supported | bounded_supported |
| N-14 | bounded_supported_prior_meaning_pending | bounded_supported_prior_meaning_pending |
| X-01 | bounded_caption_prior_context_pending | bounded_caption_prior_context_pending |
| X-02 | bounded_supported | bounded_supported |
| X-03 | bounded_structured_not_literal | bounded_structured_not_literal |
| X-04 | bounded_literal_prior_interpretation_pending | bounded_literal_prior_interpretation_pending |
| X-05 | bounded_structured_not_literal | bounded_structured_not_literal |
| X-06 | bounded_supported_context_missing | bounded_supported_context_missing |
| X-07 | bounded_supported | bounded_supported |
| T-01 | bounded_structured_table_supported | bounded_structured_table_supported |
| TR-01 | bounded_table_row_supported | bounded_table_row_supported |
| TR-02 | bounded_table_row_prior_context_pending | bounded_table_row_prior_context_pending |
| TR-03 | bounded_table_row_supported | bounded_table_row_supported |
| D-01 | bounded_graphic_prior_context_pending | bounded_graphic_prior_context_pending |
| D-02 | bounded_graphic_layout_supported | bounded_graphic_layout_supported |
| CAP-01 | bounded_caption_supported | bounded_caption_supported |
| CAP-02 | bounded_caption_supported | bounded_caption_supported |
| G-01 | bounded_visible_glyphs_rating_meaning_pending | bounded_visible_glyphs_rating_meaning_pending |
| G-02 | bounded_visible_glyphs_rating_meaning_pending | bounded_visible_glyphs_rating_meaning_pending |
| G-03 | bounded_graphic_supported | bounded_graphic_supported |
| G-04 | bounded_graphic_supported | bounded_graphic_supported |
| G-05 | bounded_graphic_supported | bounded_graphic_supported |
| K-01 | bounded_physical_continuation_supported | bounded_physical_continuation_supported |
| K-02 | bounded_physical_continuation_supported | bounded_physical_continuation_supported |
| K-03 | bounded_physical_continuation_supported | bounded_physical_continuation_supported |
| K-04 | bounded_physical_continuation_supported | bounded_physical_continuation_supported |
| K-05 | bounded_physical_continuation_supported | bounded_physical_continuation_supported |
| K-06 | bounded_physical_continuation_supported | bounded_physical_continuation_supported |
| K-07 | bounded_physical_continuation_supported | bounded_physical_continuation_supported |
| N-14-S1 | bounded_supported | bounded_supported |
| N-14-S2 | bounded_literal_prior_interpretation_pending | bounded_literal_prior_interpretation_pending |
| N-14-S3 | bounded_literal_prior_interpretation_pending | bounded_literal_prior_interpretation_pending |
| N-03-S1 | bounded_supported | bounded_supported |
| N-03-S2 | bounded_supported | bounded_supported |
| N-07-S1 | bounded_supported | bounded_supported |
| N-07-S2 | bounded_supported | bounded_supported |
| N-09-S1 | bounded_supported | bounded_supported |
| N-09-S2 | bounded_supported_context_missing | bounded_supported_context_missing |
| C-9.66-01-S1 | bounded_child_supported | bounded_child_supported |
| C-9.66-01-S2 | bounded_child_supported | bounded_child_supported |
| C-9.66-01-S3 | bounded_child_supported | bounded_child_supported |
| C-9.66-01-S4 | bounded_child_supported | bounded_child_supported |
| C-9.66-01-S5 | bounded_child_supported | bounded_child_supported |
| C-9.66-01-S6 | bounded_child_supported | bounded_child_supported |
| C-9.7-01-S1 | bounded_child_supported | bounded_child_supported |
| C-9.7-01-S2 | explanatory_clause_omitted_image_retains_source | explanatory_clause_omitted_image_retains_source |

Wszystkie414 zakresów ma decyzje; nie całe poprawne rekordy. Pochodzenie, właściciel i dokładne wyłączenia prowadzą wskazane owner-overlay pointers w JSON.

## Wszystkie277 par rubryki

| Para | Wcześniejsza decyzja | Ograniczenie |
|---|---|---|
| numbers:EXP-002 | accepted_exact_scope — oba wyniki | Tylko EXP-002 reviewed_scope; bez nowego punktu |
| numbers:EXP-004 | accepted_exact_scope — oba wyniki | Tylko EXP-004 reviewed_scope; bez nowego punktu |
| numbers:EXP-007 | accepted_exact_scope — oba wyniki | Tylko EXP-007 reviewed_scope; bez nowego punktu |
| numbers:EXP-008 | accepted_exact_scope — oba wyniki | Tylko EXP-008 reviewed_scope; bez nowego punktu |
| numbers:EXP-009 | accepted_exact_scope — oba wyniki | Tylko EXP-009 reviewed_scope; bez nowego punktu |
| numbers:EXP-012 | accepted_exact_scope — oba wyniki | Tylko EXP-012 reviewed_scope; bez nowego punktu |
| numbers:EXP-013 | accepted_exact_scope — oba wyniki | Tylko EXP-013 reviewed_scope; bez nowego punktu |
| numbers:EXP-015 | accepted_exact_scope — oba wyniki | Tylko EXP-015 reviewed_scope; bez nowego punktu |
| numbers:EXP-017 | old_pending — oba wyniki | Tylko EXP-017 reviewed_scope; bez nowego punktu |
| numbers:EXP-020 | accepted_exact_scope — oba wyniki | Tylko EXP-020 reviewed_scope; bez nowego punktu |
| numbers:EXP-022 | accepted_exact_scope — oba wyniki | Tylko EXP-022 reviewed_scope; bez nowego punktu |
| numbers:EXP-023 | accepted_exact_scope — oba wyniki | Tylko EXP-023 reviewed_scope; bez nowego punktu |
| numbers:EXP-025 | accepted_exact_scope — oba wyniki | Tylko EXP-025 reviewed_scope; bez nowego punktu |
| numbers:EXP-027 | accepted_exact_scope — oba wyniki | Tylko EXP-027 reviewed_scope; bez nowego punktu |
| numbers:EXP-028 | accepted_exact_scope — oba wyniki | Tylko EXP-028 reviewed_scope; bez nowego punktu |
| numbers:EXP-030 | accepted_exact_scope — oba wyniki | Tylko EXP-030 reviewed_scope; bez nowego punktu |
| numbers:EXP-032 | accepted_exact_scope — oba wyniki | Tylko EXP-032 reviewed_scope; bez nowego punktu |
| numbers:EXP-034 | accepted_exact_scope — oba wyniki | Tylko EXP-034 reviewed_scope; bez nowego punktu |
| numbers:EXP-035 | accepted_exact_scope — oba wyniki | Tylko EXP-035 reviewed_scope; bez nowego punktu |
| numbers:EXP-036 | accepted_exact_scope — oba wyniki | Tylko EXP-036 reviewed_scope; bez nowego punktu |
| numbers:EXP-037 | accepted_exact_scope — oba wyniki | Tylko EXP-037 reviewed_scope; bez nowego punktu |
| numbers:EXP-038 | accepted_exact_scope — oba wyniki | Tylko EXP-038 reviewed_scope; bez nowego punktu |
| numbers:EXP-039 | accepted_exact_scope — oba wyniki | Tylko EXP-039 reviewed_scope; bez nowego punktu |
| numbers:EXP-041 | accepted_exact_scope — oba wyniki | Tylko EXP-041 reviewed_scope; bez nowego punktu |
| numbers:EXP-042 | accepted_exact_scope — oba wyniki | Tylko EXP-042 reviewed_scope; bez nowego punktu |
| numbers:EXP-043 | accepted_exact_scope — oba wyniki | Tylko EXP-043 reviewed_scope; bez nowego punktu |
| numbers:EXP-045 | accepted_exact_scope — oba wyniki | Tylko EXP-045 reviewed_scope; bez nowego punktu |
| numbers:EXP-047 | accepted_exact_scope — oba wyniki | Tylko EXP-047 reviewed_scope; bez nowego punktu |
| numbers:EXP-048 | accepted_exact_scope — oba wyniki | Tylko EXP-048 reviewed_scope; bez nowego punktu |
| numbers:EXP-049 | accepted_exact_scope — oba wyniki | Tylko EXP-049 reviewed_scope; bez nowego punktu |
| numbers:EXP-051 | accepted_exact_scope — oba wyniki | Tylko EXP-051 reviewed_scope; bez nowego punktu |
| numbers:EXP-052 | old_pending — oba wyniki | Tylko EXP-052 reviewed_scope; bez nowego punktu |
| numbers:EXP-055 | accepted_exact_scope — oba wyniki | Tylko EXP-055 reviewed_scope; bez nowego punktu |
| numbers:EXP-057 | accepted_exact_scope — oba wyniki | Tylko EXP-057 reviewed_scope; bez nowego punktu |
| numbers:EXP-058 | accepted_exact_scope — oba wyniki | Tylko EXP-058 reviewed_scope; bez nowego punktu |
| numbers:EXP-061 | accepted_exact_scope — oba wyniki | Tylko EXP-061 reviewed_scope; bez nowego punktu |
| numbers:EXP-062 | accepted_exact_scope — oba wyniki | Tylko EXP-062 reviewed_scope; bez nowego punktu |
| numbers:EXP-063 | accepted_exact_scope — oba wyniki | Tylko EXP-063 reviewed_scope; bez nowego punktu |
| numbers:EXP-065 | accepted_exact_scope — oba wyniki | Tylko EXP-065 reviewed_scope; bez nowego punktu |
| numbers:EXP-068 | accepted_exact_scope — oba wyniki | Tylko EXP-068 reviewed_scope; bez nowego punktu |
| numbers:EXP-069 | accepted_exact_scope — oba wyniki | Tylko EXP-069 reviewed_scope; bez nowego punktu |
| units:EXP-002 | accepted_exact_scope — oba wyniki | Tylko EXP-002 reviewed_scope; bez nowego punktu |
| units:EXP-004 | accepted_exact_scope — oba wyniki | Tylko EXP-004 reviewed_scope; bez nowego punktu |
| units:EXP-008 | accepted_exact_scope — oba wyniki | Tylko EXP-008 reviewed_scope; bez nowego punktu |
| units:EXP-012 | accepted_exact_scope — oba wyniki | Tylko EXP-012 reviewed_scope; bez nowego punktu |
| units:EXP-013 | accepted_exact_scope — oba wyniki | Tylko EXP-013 reviewed_scope; bez nowego punktu |
| units:EXP-015 | accepted_exact_scope — oba wyniki | Tylko EXP-015 reviewed_scope; bez nowego punktu |
| units:EXP-017 | old_pending — oba wyniki | Tylko EXP-017 reviewed_scope; bez nowego punktu |
| units:EXP-020 | accepted_exact_scope — oba wyniki | Tylko EXP-020 reviewed_scope; bez nowego punktu |
| units:EXP-022 | accepted_exact_scope — oba wyniki | Tylko EXP-022 reviewed_scope; bez nowego punktu |
| units:EXP-023 | accepted_exact_scope — oba wyniki | Tylko EXP-023 reviewed_scope; bez nowego punktu |
| units:EXP-025 | accepted_exact_scope — oba wyniki | Tylko EXP-025 reviewed_scope; bez nowego punktu |
| units:EXP-027 | accepted_exact_scope — oba wyniki | Tylko EXP-027 reviewed_scope; bez nowego punktu |
| units:EXP-028 | accepted_exact_scope — oba wyniki | Tylko EXP-028 reviewed_scope; bez nowego punktu |
| units:EXP-030 | accepted_exact_scope — oba wyniki | Tylko EXP-030 reviewed_scope; bez nowego punktu |
| units:EXP-032 | accepted_exact_scope — oba wyniki | Tylko EXP-032 reviewed_scope; bez nowego punktu |
| units:EXP-034 | accepted_exact_scope — oba wyniki | Tylko EXP-034 reviewed_scope; bez nowego punktu |
| units:EXP-035 | accepted_exact_scope — oba wyniki | Tylko EXP-035 reviewed_scope; bez nowego punktu |
| units:EXP-036 | accepted_exact_scope — oba wyniki | Tylko EXP-036 reviewed_scope; bez nowego punktu |
| units:EXP-037 | accepted_exact_scope — oba wyniki | Tylko EXP-037 reviewed_scope; bez nowego punktu |
| units:EXP-038 | accepted_exact_scope — oba wyniki | Tylko EXP-038 reviewed_scope; bez nowego punktu |
| units:EXP-039 | accepted_exact_scope — oba wyniki | Tylko EXP-039 reviewed_scope; bez nowego punktu |
| units:EXP-041 | accepted_exact_scope — oba wyniki | Tylko EXP-041 reviewed_scope; bez nowego punktu |
| units:EXP-042 | accepted_exact_scope — oba wyniki | Tylko EXP-042 reviewed_scope; bez nowego punktu |
| units:EXP-043 | accepted_exact_scope — oba wyniki | Tylko EXP-043 reviewed_scope; bez nowego punktu |
| units:EXP-045 | accepted_exact_scope — oba wyniki | Tylko EXP-045 reviewed_scope; bez nowego punktu |
| units:EXP-047 | accepted_exact_scope — oba wyniki | Tylko EXP-047 reviewed_scope; bez nowego punktu |
| units:EXP-048 | accepted_exact_scope — oba wyniki | Tylko EXP-048 reviewed_scope; bez nowego punktu |
| units:EXP-051 | accepted_exact_scope — oba wyniki | Tylko EXP-051 reviewed_scope; bez nowego punktu |
| units:EXP-052 | old_pending — oba wyniki | Tylko EXP-052 reviewed_scope; bez nowego punktu |
| units:EXP-055 | accepted_exact_scope — oba wyniki | Tylko EXP-055 reviewed_scope; bez nowego punktu |
| units:EXP-057 | accepted_exact_scope — oba wyniki | Tylko EXP-057 reviewed_scope; bez nowego punktu |
| units:EXP-058 | accepted_exact_scope — oba wyniki | Tylko EXP-058 reviewed_scope; bez nowego punktu |
| units:EXP-061 | accepted_exact_scope — oba wyniki | Tylko EXP-061 reviewed_scope; bez nowego punktu |
| units:EXP-062 | accepted_exact_scope — oba wyniki | Tylko EXP-062 reviewed_scope; bez nowego punktu |
| units:EXP-063 | accepted_exact_scope — oba wyniki | Tylko EXP-063 reviewed_scope; bez nowego punktu |
| units:EXP-065 | accepted_exact_scope — oba wyniki | Tylko EXP-065 reviewed_scope; bez nowego punktu |
| units:EXP-068 | accepted_exact_scope — oba wyniki | Tylko EXP-068 reviewed_scope; bez nowego punktu |
| units:EXP-069 | accepted_exact_scope — oba wyniki | Tylko EXP-069 reviewed_scope; bez nowego punktu |
| negations:EXP-001 | accepted_exact_scope — oba wyniki | Tylko EXP-001 reviewed_scope; bez nowego punktu |
| negations:EXP-003 | accepted_exact_scope — oba wyniki | Tylko EXP-003 reviewed_scope; bez nowego punktu |
| negations:EXP-004 | accepted_exact_scope — oba wyniki | Tylko EXP-004 reviewed_scope; bez nowego punktu |
| negations:EXP-005 | accepted_exact_scope — oba wyniki | Tylko EXP-005 reviewed_scope; bez nowego punktu |
| negations:EXP-006 | accepted_exact_scope — oba wyniki | Tylko EXP-006 reviewed_scope; bez nowego punktu |
| negations:EXP-009 | accepted_exact_scope — oba wyniki | Tylko EXP-009 reviewed_scope; bez nowego punktu |
| negations:EXP-011 | accepted_exact_scope — oba wyniki | Tylko EXP-011 reviewed_scope; bez nowego punktu |
| negations:EXP-014 | accepted_exact_scope — oba wyniki | Tylko EXP-014 reviewed_scope; bez nowego punktu |
| negations:EXP-015 | accepted_exact_scope — oba wyniki | Tylko EXP-015 reviewed_scope; bez nowego punktu |
| negations:EXP-018 | accepted_exact_scope — oba wyniki | Tylko EXP-018 reviewed_scope; bez nowego punktu |
| negations:EXP-021 | accepted_exact_scope — oba wyniki | Tylko EXP-021 reviewed_scope; bez nowego punktu |
| negations:EXP-023 | accepted_exact_scope — oba wyniki | Tylko EXP-023 reviewed_scope; bez nowego punktu |
| negations:EXP-024 | accepted_exact_scope — oba wyniki | Tylko EXP-024 reviewed_scope; bez nowego punktu |
| negations:EXP-026 | accepted_exact_scope — oba wyniki | Tylko EXP-026 reviewed_scope; bez nowego punktu |
| negations:EXP-027 | accepted_exact_scope — oba wyniki | Tylko EXP-027 reviewed_scope; bez nowego punktu |
| negations:EXP-028 | accepted_exact_scope — oba wyniki | Tylko EXP-028 reviewed_scope; bez nowego punktu |
| negations:EXP-029 | accepted_exact_scope — oba wyniki | Tylko EXP-029 reviewed_scope; bez nowego punktu |
| negations:EXP-032 | accepted_exact_scope — oba wyniki | Tylko EXP-032 reviewed_scope; bez nowego punktu |
| negations:EXP-035 | accepted_exact_scope — oba wyniki | Tylko EXP-035 reviewed_scope; bez nowego punktu |
| negations:EXP-036 | accepted_exact_scope — oba wyniki | Tylko EXP-036 reviewed_scope; bez nowego punktu |
| negations:EXP-040 | old_pending — oba wyniki | Tylko EXP-040 reviewed_scope; bez nowego punktu |
| negations:EXP-041 | accepted_exact_scope — oba wyniki | Tylko EXP-041 reviewed_scope; bez nowego punktu |
| negations:EXP-044 | accepted_exact_scope — oba wyniki | Tylko EXP-044 reviewed_scope; bez nowego punktu |
| negations:EXP-046 | accepted_exact_scope — oba wyniki | Tylko EXP-046 reviewed_scope; bez nowego punktu |
| negations:EXP-047 | accepted_exact_scope — oba wyniki | Tylko EXP-047 reviewed_scope; bez nowego punktu |
| negations:EXP-048 | accepted_exact_scope — oba wyniki | Tylko EXP-048 reviewed_scope; bez nowego punktu |
| negations:EXP-049 | accepted_exact_scope — oba wyniki | Tylko EXP-049 reviewed_scope; bez nowego punktu |
| negations:EXP-051 | accepted_exact_scope — oba wyniki | Tylko EXP-051 reviewed_scope; bez nowego punktu |
| negations:EXP-052 | old_pending — oba wyniki | Tylko EXP-052 reviewed_scope; bez nowego punktu |
| negations:EXP-053 | accepted_exact_scope — oba wyniki | Tylko EXP-053 reviewed_scope; bez nowego punktu |
| negations:EXP-054 | accepted_exact_scope — oba wyniki | Tylko EXP-054 reviewed_scope; bez nowego punktu |
| negations:EXP-055 | accepted_exact_scope — oba wyniki | Tylko EXP-055 reviewed_scope; bez nowego punktu |
| negations:EXP-056 | accepted_exact_scope — oba wyniki | Tylko EXP-056 reviewed_scope; bez nowego punktu |
| negations:EXP-057 | accepted_exact_scope — oba wyniki | Tylko EXP-057 reviewed_scope; bez nowego punktu |
| negations:EXP-058 | accepted_exact_scope — oba wyniki | Tylko EXP-058 reviewed_scope; bez nowego punktu |
| negations:EXP-059 | accepted_exact_scope — oba wyniki | Tylko EXP-059 reviewed_scope; bez nowego punktu |
| negations:EXP-060 | accepted_exact_scope — oba wyniki | Tylko EXP-060 reviewed_scope; bez nowego punktu |
| negations:EXP-061 | accepted_exact_scope — oba wyniki | Tylko EXP-061 reviewed_scope; bez nowego punktu |
| negations:EXP-067 | accepted_exact_scope — oba wyniki | Tylko EXP-067 reviewed_scope; bez nowego punktu |
| negations:EXP-070 | accepted_exact_scope — oba wyniki | Tylko EXP-070 reviewed_scope; bez nowego punktu |
| negations:EXP-071 | accepted_exact_scope — oba wyniki | Tylko EXP-071 reviewed_scope; bez nowego punktu |
| negations:EXP-072 | accepted_exact_scope — oba wyniki | Tylko EXP-072 reviewed_scope; bez nowego punktu |
| negations:EXP-073 | accepted_exact_scope — oba wyniki | Tylko EXP-073 reviewed_scope; bez nowego punktu |
| conditions:EXP-001 | accepted_exact_scope — oba wyniki | Tylko EXP-001 reviewed_scope; bez nowego punktu |
| conditions:EXP-002 | accepted_exact_scope — oba wyniki | Tylko EXP-002 reviewed_scope; bez nowego punktu |
| conditions:EXP-003 | accepted_exact_scope — oba wyniki | Tylko EXP-003 reviewed_scope; bez nowego punktu |
| conditions:EXP-004 | accepted_exact_scope — oba wyniki | Tylko EXP-004 reviewed_scope; bez nowego punktu |
| conditions:EXP-005 | accepted_exact_scope — oba wyniki | Tylko EXP-005 reviewed_scope; bez nowego punktu |
| conditions:EXP-006 | accepted_exact_scope — oba wyniki | Tylko EXP-006 reviewed_scope; bez nowego punktu |
| conditions:EXP-007 | accepted_exact_scope — oba wyniki | Tylko EXP-007 reviewed_scope; bez nowego punktu |
| conditions:EXP-008 | accepted_exact_scope — oba wyniki | Tylko EXP-008 reviewed_scope; bez nowego punktu |
| conditions:EXP-009 | accepted_exact_scope — oba wyniki | Tylko EXP-009 reviewed_scope; bez nowego punktu |
| conditions:EXP-011 | accepted_exact_scope — oba wyniki | Tylko EXP-011 reviewed_scope; bez nowego punktu |
| conditions:EXP-012 | accepted_exact_scope — oba wyniki | Tylko EXP-012 reviewed_scope; bez nowego punktu |
| conditions:EXP-013 | accepted_exact_scope — oba wyniki | Tylko EXP-013 reviewed_scope; bez nowego punktu |
| conditions:EXP-014 | accepted_exact_scope — oba wyniki | Tylko EXP-014 reviewed_scope; bez nowego punktu |
| conditions:EXP-015 | accepted_exact_scope — oba wyniki | Tylko EXP-015 reviewed_scope; bez nowego punktu |
| conditions:EXP-016 | accepted_exact_scope — oba wyniki | Tylko EXP-016 reviewed_scope; bez nowego punktu |
| conditions:EXP-017 | old_pending — oba wyniki | Tylko EXP-017 reviewed_scope; bez nowego punktu |
| conditions:EXP-018 | accepted_exact_scope — oba wyniki | Tylko EXP-018 reviewed_scope; bez nowego punktu |
| conditions:EXP-020 | accepted_exact_scope — oba wyniki | Tylko EXP-020 reviewed_scope; bez nowego punktu |
| conditions:EXP-021 | accepted_exact_scope — oba wyniki | Tylko EXP-021 reviewed_scope; bez nowego punktu |
| conditions:EXP-022 | accepted_exact_scope — oba wyniki | Tylko EXP-022 reviewed_scope; bez nowego punktu |
| conditions:EXP-023 | accepted_exact_scope — oba wyniki | Tylko EXP-023 reviewed_scope; bez nowego punktu |
| conditions:EXP-024 | accepted_exact_scope — oba wyniki | Tylko EXP-024 reviewed_scope; bez nowego punktu |
| conditions:EXP-025 | accepted_exact_scope — oba wyniki | Tylko EXP-025 reviewed_scope; bez nowego punktu |
| conditions:EXP-026 | accepted_exact_scope — oba wyniki | Tylko EXP-026 reviewed_scope; bez nowego punktu |
| conditions:EXP-027 | accepted_exact_scope — oba wyniki | Tylko EXP-027 reviewed_scope; bez nowego punktu |
| conditions:EXP-028 | accepted_exact_scope — oba wyniki | Tylko EXP-028 reviewed_scope; bez nowego punktu |
| conditions:EXP-029 | accepted_exact_scope — oba wyniki | Tylko EXP-029 reviewed_scope; bez nowego punktu |
| conditions:EXP-030 | accepted_exact_scope — oba wyniki | Tylko EXP-030 reviewed_scope; bez nowego punktu |
| conditions:EXP-032 | accepted_exact_scope — oba wyniki | Tylko EXP-032 reviewed_scope; bez nowego punktu |
| conditions:EXP-034 | accepted_exact_scope — oba wyniki | Tylko EXP-034 reviewed_scope; bez nowego punktu |
| conditions:EXP-035 | accepted_exact_scope — oba wyniki | Tylko EXP-035 reviewed_scope; bez nowego punktu |
| conditions:EXP-036 | accepted_exact_scope — oba wyniki | Tylko EXP-036 reviewed_scope; bez nowego punktu |
| conditions:EXP-037 | accepted_exact_scope — oba wyniki | Tylko EXP-037 reviewed_scope; bez nowego punktu |
| conditions:EXP-038 | accepted_exact_scope — oba wyniki | Tylko EXP-038 reviewed_scope; bez nowego punktu |
| conditions:EXP-039 | accepted_exact_scope — oba wyniki | Tylko EXP-039 reviewed_scope; bez nowego punktu |
| conditions:EXP-040 | old_pending — oba wyniki | Tylko EXP-040 reviewed_scope; bez nowego punktu |
| conditions:EXP-041 | accepted_exact_scope — oba wyniki | Tylko EXP-041 reviewed_scope; bez nowego punktu |
| conditions:EXP-042 | accepted_exact_scope — oba wyniki | Tylko EXP-042 reviewed_scope; bez nowego punktu |
| conditions:EXP-043 | accepted_exact_scope — oba wyniki | Tylko EXP-043 reviewed_scope; bez nowego punktu |
| conditions:EXP-044 | accepted_exact_scope — oba wyniki | Tylko EXP-044 reviewed_scope; bez nowego punktu |
| conditions:EXP-045 | accepted_exact_scope — oba wyniki | Tylko EXP-045 reviewed_scope; bez nowego punktu |
| conditions:EXP-046 | accepted_exact_scope — oba wyniki | Tylko EXP-046 reviewed_scope; bez nowego punktu |
| conditions:EXP-047 | accepted_exact_scope — oba wyniki | Tylko EXP-047 reviewed_scope; bez nowego punktu |
| conditions:EXP-048 | accepted_exact_scope — oba wyniki | Tylko EXP-048 reviewed_scope; bez nowego punktu |
| conditions:EXP-049 | accepted_exact_scope — oba wyniki | Tylko EXP-049 reviewed_scope; bez nowego punktu |
| conditions:EXP-051 | accepted_exact_scope — oba wyniki | Tylko EXP-051 reviewed_scope; bez nowego punktu |
| conditions:EXP-052 | old_pending — oba wyniki | Tylko EXP-052 reviewed_scope; bez nowego punktu |
| conditions:EXP-053 | accepted_exact_scope — oba wyniki | Tylko EXP-053 reviewed_scope; bez nowego punktu |
| conditions:EXP-054 | accepted_exact_scope — oba wyniki | Tylko EXP-054 reviewed_scope; bez nowego punktu |
| conditions:EXP-055 | accepted_exact_scope — oba wyniki | Tylko EXP-055 reviewed_scope; bez nowego punktu |
| conditions:EXP-056 | accepted_exact_scope — oba wyniki | Tylko EXP-056 reviewed_scope; bez nowego punktu |
| conditions:EXP-057 | accepted_exact_scope — oba wyniki | Tylko EXP-057 reviewed_scope; bez nowego punktu |
| conditions:EXP-058 | accepted_exact_scope — oba wyniki | Tylko EXP-058 reviewed_scope; bez nowego punktu |
| conditions:EXP-059 | accepted_exact_scope — oba wyniki | Tylko EXP-059 reviewed_scope; bez nowego punktu |
| conditions:EXP-060 | accepted_exact_scope — oba wyniki | Tylko EXP-060 reviewed_scope; bez nowego punktu |
| conditions:EXP-061 | accepted_exact_scope — oba wyniki | Tylko EXP-061 reviewed_scope; bez nowego punktu |
| conditions:EXP-062 | accepted_exact_scope — oba wyniki | Tylko EXP-062 reviewed_scope; bez nowego punktu |
| conditions:EXP-063 | accepted_exact_scope — oba wyniki | Tylko EXP-063 reviewed_scope; bez nowego punktu |
| conditions:EXP-065 | accepted_exact_scope — oba wyniki | Tylko EXP-065 reviewed_scope; bez nowego punktu |
| conditions:EXP-067 | accepted_exact_scope — oba wyniki | Tylko EXP-067 reviewed_scope; bez nowego punktu |
| conditions:EXP-068 | accepted_exact_scope — oba wyniki | Tylko EXP-068 reviewed_scope; bez nowego punktu |
| conditions:EXP-069 | accepted_exact_scope — oba wyniki | Tylko EXP-069 reviewed_scope; bez nowego punktu |
| conditions:EXP-070 | accepted_exact_scope — oba wyniki | Tylko EXP-070 reviewed_scope; bez nowego punktu |
| conditions:EXP-071 | accepted_exact_scope — oba wyniki | Tylko EXP-071 reviewed_scope; bez nowego punktu |
| conditions:EXP-072 | accepted_exact_scope — oba wyniki | Tylko EXP-072 reviewed_scope; bez nowego punktu |
| conditions:EXP-073 | accepted_exact_scope — oba wyniki | Tylko EXP-073 reviewed_scope; bez nowego punktu |
| exceptions:EXP-004 | accepted_exact_scope — oba wyniki | Tylko EXP-004 reviewed_scope; bez nowego punktu |
| exceptions:EXP-005 | accepted_exact_scope — oba wyniki | Tylko EXP-005 reviewed_scope; bez nowego punktu |
| exceptions:EXP-006 | accepted_exact_scope — oba wyniki | Tylko EXP-006 reviewed_scope; bez nowego punktu |
| exceptions:EXP-008 | accepted_exact_scope — oba wyniki | Tylko EXP-008 reviewed_scope; bez nowego punktu |
| exceptions:EXP-009 | accepted_exact_scope — oba wyniki | Tylko EXP-009 reviewed_scope; bez nowego punktu |
| exceptions:EXP-011 | accepted_exact_scope — oba wyniki | Tylko EXP-011 reviewed_scope; bez nowego punktu |
| exceptions:EXP-012 | accepted_exact_scope — oba wyniki | Tylko EXP-012 reviewed_scope; bez nowego punktu |
| exceptions:EXP-014 | accepted_exact_scope — oba wyniki | Tylko EXP-014 reviewed_scope; bez nowego punktu |
| exceptions:EXP-015 | accepted_exact_scope — oba wyniki | Tylko EXP-015 reviewed_scope; bez nowego punktu |
| exceptions:EXP-016 | accepted_exact_scope — oba wyniki | Tylko EXP-016 reviewed_scope; bez nowego punktu |
| exceptions:EXP-018 | accepted_exact_scope — oba wyniki | Tylko EXP-018 reviewed_scope; bez nowego punktu |
| exceptions:EXP-020 | accepted_exact_scope — oba wyniki | Tylko EXP-020 reviewed_scope; bez nowego punktu |
| exceptions:EXP-021 | accepted_exact_scope — oba wyniki | Tylko EXP-021 reviewed_scope; bez nowego punktu |
| exceptions:EXP-023 | accepted_exact_scope — oba wyniki | Tylko EXP-023 reviewed_scope; bez nowego punktu |
| exceptions:EXP-024 | accepted_exact_scope — oba wyniki | Tylko EXP-024 reviewed_scope; bez nowego punktu |
| exceptions:EXP-026 | accepted_exact_scope — oba wyniki | Tylko EXP-026 reviewed_scope; bez nowego punktu |
| exceptions:EXP-027 | accepted_exact_scope — oba wyniki | Tylko EXP-027 reviewed_scope; bez nowego punktu |
| exceptions:EXP-029 | accepted_exact_scope — oba wyniki | Tylko EXP-029 reviewed_scope; bez nowego punktu |
| exceptions:EXP-032 | accepted_exact_scope — oba wyniki | Tylko EXP-032 reviewed_scope; bez nowego punktu |
| exceptions:EXP-035 | accepted_exact_scope — oba wyniki | Tylko EXP-035 reviewed_scope; bez nowego punktu |
| exceptions:EXP-036 | accepted_exact_scope — oba wyniki | Tylko EXP-036 reviewed_scope; bez nowego punktu |
| exceptions:EXP-037 | accepted_exact_scope — oba wyniki | Tylko EXP-037 reviewed_scope; bez nowego punktu |
| exceptions:EXP-038 | accepted_exact_scope — oba wyniki | Tylko EXP-038 reviewed_scope; bez nowego punktu |
| exceptions:EXP-039 | accepted_exact_scope — oba wyniki | Tylko EXP-039 reviewed_scope; bez nowego punktu |
| exceptions:EXP-040 | old_pending — oba wyniki | Tylko EXP-040 reviewed_scope; bez nowego punktu |
| exceptions:EXP-041 | accepted_exact_scope — oba wyniki | Tylko EXP-041 reviewed_scope; bez nowego punktu |
| exceptions:EXP-042 | accepted_exact_scope — oba wyniki | Tylko EXP-042 reviewed_scope; bez nowego punktu |
| exceptions:EXP-044 | accepted_exact_scope — oba wyniki | Tylko EXP-044 reviewed_scope; bez nowego punktu |
| exceptions:EXP-046 | accepted_exact_scope — oba wyniki | Tylko EXP-046 reviewed_scope; bez nowego punktu |
| exceptions:EXP-047 | accepted_exact_scope — oba wyniki | Tylko EXP-047 reviewed_scope; bez nowego punktu |
| exceptions:EXP-048 | accepted_exact_scope — oba wyniki | Tylko EXP-048 reviewed_scope; bez nowego punktu |
| exceptions:EXP-049 | accepted_exact_scope — oba wyniki | Tylko EXP-049 reviewed_scope; bez nowego punktu |
| exceptions:EXP-051 | accepted_exact_scope — oba wyniki | Tylko EXP-051 reviewed_scope; bez nowego punktu |
| exceptions:EXP-052 | old_pending — oba wyniki | Tylko EXP-052 reviewed_scope; bez nowego punktu |
| exceptions:EXP-053 | accepted_exact_scope — oba wyniki | Tylko EXP-053 reviewed_scope; bez nowego punktu |
| exceptions:EXP-054 | accepted_exact_scope — oba wyniki | Tylko EXP-054 reviewed_scope; bez nowego punktu |
| exceptions:EXP-055 | accepted_exact_scope — oba wyniki | Tylko EXP-055 reviewed_scope; bez nowego punktu |
| exceptions:EXP-056 | accepted_exact_scope — oba wyniki | Tylko EXP-056 reviewed_scope; bez nowego punktu |
| exceptions:EXP-057 | accepted_exact_scope — oba wyniki | Tylko EXP-057 reviewed_scope; bez nowego punktu |
| exceptions:EXP-058 | accepted_exact_scope — oba wyniki | Tylko EXP-058 reviewed_scope; bez nowego punktu |
| exceptions:EXP-059 | accepted_exact_scope — oba wyniki | Tylko EXP-059 reviewed_scope; bez nowego punktu |
| exceptions:EXP-060 | accepted_exact_scope — oba wyniki | Tylko EXP-060 reviewed_scope; bez nowego punktu |
| exceptions:EXP-061 | accepted_exact_scope — oba wyniki | Tylko EXP-061 reviewed_scope; bez nowego punktu |
| exceptions:EXP-062 | accepted_exact_scope — oba wyniki | Tylko EXP-062 reviewed_scope; bez nowego punktu |
| exceptions:EXP-063 | accepted_exact_scope — oba wyniki | Tylko EXP-063 reviewed_scope; bez nowego punktu |
| exceptions:EXP-065 | accepted_exact_scope — oba wyniki | Tylko EXP-065 reviewed_scope; bez nowego punktu |
| exceptions:EXP-067 | accepted_exact_scope — oba wyniki | Tylko EXP-067 reviewed_scope; bez nowego punktu |
| exceptions:EXP-069 | accepted_exact_scope — oba wyniki | Tylko EXP-069 reviewed_scope; bez nowego punktu |
| exceptions:EXP-070 | accepted_exact_scope — oba wyniki | Tylko EXP-070 reviewed_scope; bez nowego punktu |
| exceptions:EXP-071 | accepted_exact_scope — oba wyniki | Tylko EXP-071 reviewed_scope; bez nowego punktu |
| exceptions:EXP-072 | accepted_exact_scope — oba wyniki | Tylko EXP-072 reviewed_scope; bez nowego punktu |
| exceptions:EXP-073 | accepted_exact_scope — oba wyniki | Tylko EXP-073 reviewed_scope; bez nowego punktu |
| time:EXP-001 | accepted_exact_scope — oba wyniki | Tylko EXP-001 reviewed_scope; bez nowego punktu |
| time:EXP-003 | accepted_exact_scope — oba wyniki | Tylko EXP-003 reviewed_scope; bez nowego punktu |
| time:EXP-009 | accepted_exact_scope — oba wyniki | Tylko EXP-009 reviewed_scope; bez nowego punktu |
| time:EXP-011 | accepted_exact_scope — oba wyniki | Tylko EXP-011 reviewed_scope; bez nowego punktu |
| time:EXP-013 | accepted_exact_scope — oba wyniki | Tylko EXP-013 reviewed_scope; bez nowego punktu |
| time:EXP-014 | accepted_exact_scope — oba wyniki | Tylko EXP-014 reviewed_scope; bez nowego punktu |
| time:EXP-016 | accepted_exact_scope — oba wyniki | Tylko EXP-016 reviewed_scope; bez nowego punktu |
| time:EXP-024 | accepted_exact_scope — oba wyniki | Tylko EXP-024 reviewed_scope; bez nowego punktu |
| time:EXP-034 | accepted_exact_scope — oba wyniki | Tylko EXP-034 reviewed_scope; bez nowego punktu |
| time:EXP-035 | accepted_exact_scope — oba wyniki | Tylko EXP-035 reviewed_scope; bez nowego punktu |
| time:EXP-040 | old_pending — oba wyniki | Tylko EXP-040 reviewed_scope; bez nowego punktu |
| time:EXP-044 | accepted_exact_scope — oba wyniki | Tylko EXP-044 reviewed_scope; bez nowego punktu |
| time:EXP-047 | accepted_exact_scope — oba wyniki | Tylko EXP-047 reviewed_scope; bez nowego punktu |
| time:EXP-048 | accepted_exact_scope — oba wyniki | Tylko EXP-048 reviewed_scope; bez nowego punktu |
| time:EXP-049 | accepted_exact_scope — oba wyniki | Tylko EXP-049 reviewed_scope; bez nowego punktu |
| time:EXP-051 | accepted_exact_scope — oba wyniki | Tylko EXP-051 reviewed_scope; bez nowego punktu |
| time:EXP-052 | old_pending — oba wyniki | Tylko EXP-052 reviewed_scope; bez nowego punktu |
| time:EXP-054 | accepted_exact_scope — oba wyniki | Tylko EXP-054 reviewed_scope; bez nowego punktu |
| time:EXP-057 | accepted_exact_scope — oba wyniki | Tylko EXP-057 reviewed_scope; bez nowego punktu |
| time:EXP-058 | accepted_exact_scope — oba wyniki | Tylko EXP-058 reviewed_scope; bez nowego punktu |
| time:EXP-059 | accepted_exact_scope — oba wyniki | Tylko EXP-059 reviewed_scope; bez nowego punktu |
| time:EXP-061 | accepted_exact_scope — oba wyniki | Tylko EXP-061 reviewed_scope; bez nowego punktu |
| time:EXP-062 | accepted_exact_scope — oba wyniki | Tylko EXP-062 reviewed_scope; bez nowego punktu |
| time:EXP-063 | accepted_exact_scope — oba wyniki | Tylko EXP-063 reviewed_scope; bez nowego punktu |
| time:EXP-065 | accepted_exact_scope — oba wyniki | Tylko EXP-065 reviewed_scope; bez nowego punktu |
| time:EXP-067 | accepted_exact_scope — oba wyniki | Tylko EXP-067 reviewed_scope; bez nowego punktu |
| time:EXP-069 | accepted_exact_scope — oba wyniki | Tylko EXP-069 reviewed_scope; bez nowego punktu |
| time:EXP-071 | accepted_exact_scope — oba wyniki | Tylko EXP-071 reviewed_scope; bez nowego punktu |
| time:EXP-073 | accepted_exact_scope — oba wyniki | Tylko EXP-073 reviewed_scope; bez nowego punktu |
| tables:EXP-005 | accepted_exact_scope — oba wyniki | Tylko EXP-005 reviewed_scope; bez nowego punktu |
| tables:EXP-007 | accepted_exact_scope — oba wyniki | Tylko EXP-007 reviewed_scope; bez nowego punktu |
| tables:EXP-008 | accepted_exact_scope — oba wyniki | Tylko EXP-008 reviewed_scope; bez nowego punktu |
| tables:EXP-009 | accepted_exact_scope — oba wyniki | Tylko EXP-009 reviewed_scope; bez nowego punktu |
| tables:EXP-020 | accepted_exact_scope — oba wyniki | Tylko EXP-020 reviewed_scope; bez nowego punktu |
| tables:EXP-070 | accepted_exact_scope — oba wyniki | Tylko EXP-070 reviewed_scope; bez nowego punktu |
| tables:EXP-073 | accepted_exact_scope — oba wyniki | Tylko EXP-073 reviewed_scope; bez nowego punktu |
| diagrams:EXP-046 | accepted_exact_scope — oba wyniki | Tylko EXP-046 reviewed_scope; bez nowego punktu |

264 wcześniejsze pary przyjęte;13 nadal pending dla EXP-017/040/052. To te same pary w każdej odpowiedzi, nie554 reguły.

## Stare kwestie i późniejsze decyzje

### SEM-001

Oba wyniki zachowują warunek DR>TQ i minimum 1, ale R916.interpretation=unknown/G916.blocking pozostawia DR<=TQ nierozstrzygnięte. Proponowane niepełne odtworzenie zatwierdzonej lokalnej gałęzi 0 CH i nieuzasadniona blokada tej gałęzi; nie jest to dowód błędnego odczytu ani twierdzenia o zawsze 1 CH.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-002

Oba wyniki podają both rout/separate hexes, lecz deklarują nierozstrzygnięty zakres eliminacji. Eval-v1 przyjmuje eliminację każdej PH osobno, z możliwością legalnego Rout drugiej. Proponowana niepełna lokalna interpretacja; sprawdzić osobno, czy podstawa wcześniejszej decyzji była dostępna ekstraktorowi.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-003

first-001 ma lokalne pół/floor i literalny przykład, bez rozstrzygnięcia AS. context-01 dodaje udokumentowane 2x wyniku obrońcy przy AS, warunkowe pół/floor dla LC, wyjątek Routed i kumulatywność. Proponowane poprawne częściowe podparcie operatorów; pełna kolejność, zaokrąglenie, applicability i wynik pozostają nierozstrzygnięte.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-004

9.23 mówi o Hits zadanych przez SK; Step 4 #3 mówi o Hits atakującego, gdy obrońcą jest SK. Nowa niejawna relacja R923->NCTX846S4 jest kandydatem uzasadnienia strony/faktora/floor/cap, wymaga osobnej decyzji o konieczności i rodzaju. Nie jest pewnym TP ani FP.

DCTX923-S4 operator correspondence already accepted; earlier mixed-defense/Size/CRT and broader semantics remain open. No new gold edge.

Późniejsza dyspozycja: partially resolved for DCTX923-S4 supporting operator correspondence; remaining earlier scope pending

### SEM-005

Dawny potwierdzony błąd: bbox E916 urywa wyjątek Leader Elephant. Pełny obraz obejmuje wyjątek, ale oryginalnego lokatora nie naprawiono.

E916 locator defect confirmed by owner; original unchanged. Do not reopen accepted defect, or infer semantic minimum resolution from it.

Późniejsza dyspozycja: Owner confirmed exact E916 locator defect in both answers; original rectangle not repaired, semantic variants not decided.

### SEM-006

Oba wyniki nadal nie mają 3 krytycznych osobnych par niejawnych DEP-NEW-001/002/003 i 4 osobnych wzmianek DEP-034/035/043/067-1. To obserwacje strukturalne; semantyczne FN i treść w prozie oceniane osobno.

Three frozen implicit execution pairs and four mentions remain absent as records; prosaic content separate. D961stack kind is already owner-decided mention; no stale pending of that accepted component and no automatic semantic FN.

Późniejsza dyspozycja: None

### SEM-007

58 dawnych i 6 nowych granic glifów wymagają dokładnego review. Oględziny trzech pełnych regionów w tej części nie potwierdzają wszystkich bbox.

All124 assigned locator facets decided; not64stillunreviewed bounds. Preserve122 measurable envelope failures and2numeric-precision unresolved;116readable/6clipped-readable/2missingline. Wider graphical meaning/full-record facets not certified.

Późniejsza dyspozycja: Owner accepted all124 assigned short-quote locator assessments in bounded facets:122 measurable envelope failures,2E962 numericprecision unresolved;116 readable without observed ink loss,6clipped but readable,2E916 missingline. Source/geometry124. Original defects retained; wider evidence/glyph/whole-content review not certified.

### SEM-008

Nowa połączona ścieżka kończy się na brakującym 6.68 bullet #6 po 3 krawędziach. Nie pozyskano źródła trzeciego kroku; pełne zależne wyniki blocked_source.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-009

R918.transcription zachowuje unless rules specifically otherwise, a exceptions=unknown wskazuje nieznane wyjątki. Jednak action_effect/interpretation brzmi Any leader may command i D918specific/G-D918specific mają blocks_full_result=false/blocking=false. Oznaczono brak źródła, lecz nie zadeklarowano blokady realnej autoryzacji. Kandydat SEM-009: właściwość deklaracji blokady w rzeczywistym użyciu wymaga decyzji; nie ma konkretnego niepoprawnie wybranego dowódcy.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-010

Obie odpowiedzi podają predykaty daty/OC i warunki Triarii, nie rzeczywiste dane wybranej bitwy. AWL/RP/LOS/ZOC mają jawne blocking gaps; brak osobnych deklaracji źródła rzeczywistej daty i OC w R97intro.gap_ids (pusta lista). SEM-010: wystarczalność tego opisu needs-context wymaga właściciela. Nie jest to dowód fikcyjnego wybrania dowódcy/daty; known na conditions oznacza znany warunek, nie spełniony fakt. Nie oceniono SIT.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-011

R972 zachowuje RP >= floor(AWL/2), jednostkę Rout Points i wyjątek Shock bez ruchu przeciw enemy w własnej ZOC. R971 osobno zawiera drugą bramkę. R972.conditions/action_effect nie podaje jednak jawnie, że próg RP nie omija 9.71; brak osobnej pary DEP-NEW-001 odziedziczony. Właściciel rozstrzyga, czy dwa osobne ograniczenia wystarczają do całego reviewed_scope EXP-052, czy reprezentacja ich koniunkcji jest niepełna. Nie dopisano bramki do odpowiedzi, nie nadano FN ani ogólnego pozwolenia na atak.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-012

R996note zachowuje ignore Chariots reference on Combat Tables; N996design nie tworzy dodatkowego skutku. N-14-S2 to dokładna instrukcja, N-14-S3 appearances Sentinum/Telamon, bez listy eligibility wszystkich LI. G-D996tables deklaruje potrzebę actual tables/entries, ale blocking=false; D996tables blocks_full_result=false. Lokalny zakaz użycia wiersza znany, konkretne identyfikowanie suppressowanych entries niezamknięte. Właściciel rozstrzyga wystarczalność jawnej blokady zależnego pełnego pytania. Nie ma konkretnego niepoprawnego lookupu, nie jest to automatyczny błąd odczytu lub FP.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

### SEM-013

N911counter/N921counter/N981counter podają visible glyphs, lecz wyraźnie wykluczają game-wide values i rating-position inference. N966diagram mówi illustrative, not general Roman parameters; N985markers/N986marker to stany markerów. Brak twierdzenia o realnym Leader Elephant TQ6. Równocześnie nie ma osobnego gap ani jawnej conditional blocking deklaracji actual identified TQ/MA przed concrete use. Właściciel rozstrzyga, czy zapis illustrative wystarcza dla ograniczonego wymagania EXP-074. Same oględziny paneli/states nie certyfikują małych ratingów, tożsamości konkretnych jednostek ani 64 granic glifów. Criticality pozostaje conditional_on_concrete_parameter_use.

Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.

Późniejsza dyspozycja: None

## Pozostałe granice

W JSON rozliczono wszystkie257 oryginalnych krawędzi z wcześniejszymi accepted/excluded components,124 lokatory i218 oryginalnych rekordów reguł/węzłów. Nie nadano im pełnej akceptacji z powodu pokrycia inwentarza. Brakujące3 pary wykonawcze/4wzmianki zachowane, bez autoFN;105 niepotwierdzonych kandydatów nie staje się gold.

Nowe punkty reguł/inwentarza:0. Nowe błędy:0 w raporcie uzgodnienia — nie jest to globalne zero błędów odpowiedzi. Uzgodnienie czeka na właściciela; po nim osobne M-POC5B20 sytuacji/40 ocen.
