# M-POC5A.4a — porównania EXP-051–074

Oceniający: Codex. Każda nowa propozycja dla każdego hasha pozostaje pending/waiting_review; znaczenie akceptuje właściciel. Dawne 43 lokalne zakresy i 2 wymagania źródła na wynik zachowane.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`; PDF `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

first-001: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

[Pełny ślad JSON](comparisons.json) zawiera osobne oceny obu hashów, JSON pointers, zakresy rekordów i pól UTF-8 [start,end), SHA-256 fragmentów, źródła i zakresy decyzji. Cytaty literalne są oddzielone od podsumowań i interpretacji. Koperty źródeł nie rozszerzają reviewed_scope.

Propozycje: 20 lokalnych zgodności, 1 właściwa potrzeba/blokada źródła (EXP-064); 3 kwestie do osobnej decyzji (EXP-052/066/074). 31 powiązanych pozycji źródła, 95 diagnostycznych par rubryka/EXP. To nie zaakceptowane wyniki jakości.

## Dokładny pozytywny zestaw do decyzji

EXP-051, EXP-053, EXP-054, EXP-055, EXP-056, EXP-057, EXP-058, EXP-059, EXP-060, EXP-061, EXP-062, EXP-063, EXP-064, EXP-065, EXP-067, EXP-068, EXP-069, EXP-070, EXP-071, EXP-072, EXP-073. Tylko wskazane reviewed_scope w obu hashach; EXP-052/066/074 wyłączone.

### EXP-051

Zakres oceny: movementgate9.71cannotmovebutmayface untiloneofORtriggers:enemycombatnotELwithin3andLOSanyTriariilineunit ORTriarii>=6fromallRoman/Alainfantrylinesexcludingallied

Porównanie oceniającego: R971 zachowuje zakaz ruchu i możliwość facing przed zwolnieniem. Bramka 9.71 ma OR: enemy combat nie-EL w odległości do 3 heksów AND LOS dowolnej jednostki linii Triarii, albo odległość co najmniej 6 od wszystkich innych Roman/Ala infantry lines, z wyłączeniem allied. Nie zastąpiono any przez all, OR przez AND ani >=6 przez >6. To lokalna bramka, bez ogólnego zezwolenia na move+Shock i bez akceptacji relacji 9.72→9.71.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.71-01, PDF 35 right. Wybrany literalny zakres: 9.71 Triarii units cannot move, but may change facing, until and unless one of the following occurs:

Źródło: C-9.71-02, PDF 35 right. Wybrany literalny zakres: • There is an enemy combat unit, other than an Elephant unit, which is within 3 hexes and LOS of any unit in the Triarii line, or

Źródło: C-9.71-03, PDF 35 right. Wybrany literalny zakres: • The Triarii units are at least 6 hexes from all other Roman or Ala—but not allied–infantry lines, be they Hastati, Principes or whatever.

first-001 R971, `/rules/31`, bajty [330949,335849), SHA-256 `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.

context-01 R971, `/rules/31`, bajty [403209,408288), SHA-256 `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.

Niepewności i wyłączenia: Line, LOS, odległości i identyfikacja wojsk wymagają jawnych danych.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-052

Zakres oceny: move+ShockRP>=floor(AWL/2)doesnotbypass9.71;standingShockagainsttargetinownZOCper9.72withouthavingtomove

Porównanie oceniającego: R972 zachowuje RP >= floor(AWL/2), jednostkę Rout Points i wyjątek Shock bez ruchu przeciw enemy w własnej ZOC. R971 osobno zawiera drugą bramkę. R972.conditions/action_effect nie podaje jednak jawnie, że próg RP nie omija 9.71; brak osobnej pary DEP-NEW-001 odziedziczony. Właściciel rozstrzyga, czy dwa osobne ograniczenia wystarczają do całego reviewed_scope EXP-052, czy reprezentacja ich koniunkcji jest niepełna. Nie dopisano bramki do odpowiedzi, nie nadano FN ani ogólnego pozwolenia na atak.

Propozycja: `local_components_supported_combination_pending`. Obie decyzje właściciela pending.

Źródło: C-9.72-01, PDF 35 right. Wybrany literalny zakres: 9.72 Triarii units cannot move and Shock attack unless and until the Roman army has Rout Points equal to at least one-half of its Army Withdrawal Level (round down). They may always, however, Shock attack (without moving) against enemy units in their ZOC.

first-001 R972, `/rules/32`, bajty [335855,339867), SHA-256 `f304ccb85a653664ddb287c3e591dd67a2744b35cf4210ace71592b684436f5b`.

first-001 R971, `/rules/31`, bajty [330949,335849), SHA-256 `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.

context-01 R972, `/rules/32`, bajty [408295,412460), SHA-256 `efc3e461afcdf47ef5fafdc90f3c9223badabf8597ff20dc3ef7807de8842bde`.

context-01 R971, `/rules/31`, bajty [403209,408288), SHA-256 `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.

Niepewności i wyłączenia: 9.71 i9.72 czytane razem; full legal attack nadal wymaga innych warunków.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-053

Zakres oceny: ScorpioBoltB,builtincrew,TQ,LIonlymovement/defense;noShockattack,offensiveMissileFireonly

Porównanie oceniającego: R981 zachowuje Bolt B, built-in crews i obecność TQ; LI tylko dla movement oraz obrony w Shock/Missile. Zakaz Shock-capable i jedyna zdolność ofensywna Missile Fire nie są rozszerzone na brak możliwości obrony. Konkretna wartość TQ i pełny lookup Bolt MRRC wyłączone.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.81-01, PDF 36 left. Wybrany literalny zakres: 9.81 Scorpios are Bolt-firing (B) engines with built- in crews. The Scorpios have a TQ rating, and they are treated as Light Infantry (LI) for movement and when defending in Shock Combat or against Missile Fire. Scorpio units are not Shock-capable and their only offensive combat capability is to Missile Fire.

first-001 R981, `/rules/33`, bajty [339873,343919), SHA-256 `4e4891fc2c755ae9c07ed249141e368ed4377a415f874d747416eecb628eed39`.

context-01 R981, `/rules/33`, bajty [412467,416654), SHA-256 `76cecff485b506b160191a8885cea72dd7016bed6da4f3798c6d7d01dbc6b826`.

Niepewności i wyłączenia: Pełne LI defense/movement i bolt MRRC wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-054

Zakres oceny: modechangeIOanyfriendlyleader;Firecannotmove,Movecannotfire;switchtoMoveblocksMoveinthesamephase,switchtoFireblocksFireinthesamephase;moveIOrequired,firedoesnotrequireorder;awersFire,rewersMove

Porównanie oceniającego: R982: zmiana trybu przez IO od dowolnego friendly leader; Move nie strzela, Fire nie rusza. Switch to Move blokuje ruch w tej Orders Phase, switch to Fire blokuje fire w tej fazie. Ruch w Move wymaga IO, fire nie wymaga order. R982note zachowuje awers Fire/rewers Move. Brak nowej akcji po switch i brak certyfikacji ratingów żetonu.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.82-01, PDF 36 left. Wybrany literalny zakres: 9.82 A Scorpio is in either Fire or Move mode. It requires an Individual Order from any friendly leader to change its mode. Scorpios in Move mode cannot fire, and conversely, cannot move in Fire mode. A Scorpio that has had its mode changed to Move cannot move in that Orders Phase, nor can a Scorpio that has had its mode switched to Fire, fire in that Orders Phase. A Scorpio unit in Move mode requires an Individual Order from any friendly leader to move. Scorpio units do not need orders to fire (see 9.85 below).

Źródło: N-11, PDF 36 left. Wybrany literalny zakres: PLAY NOTE: The front side of the counter shows the unit in Fire mode; the reverse side in Move mode.

first-001 R982, `/rules/34`, bajty [343925,349222), SHA-256 `db2932e05afee950e1d27137b71fe09be42fd41a52f8e80905dc27726cf31a48`.

first-001 R982note, `/rules/35`, bajty [349228,352453), SHA-256 `88bf7f560fd28fa8d2955805d683d0f7eac1210dac638fc5f483232a758bd6c6`.

context-01 R982, `/rules/34`, bajty [416661,422148), SHA-256 `c322a28fb1c69bff5deac677b5a8ee02c5c27f63d0f17bce8a72a482a530f988`.

context-01 R982note, `/rules/35`, bajty [422155,425494), SHA-256 `9ac67925c35fae2788830f9c0809376ae5aace09ee195639c5f67b7240858bd0`.

Niepewności i wyłączenia: 9.85 uzupełnia harmonogram ognia; źródło nie ustanawia dodatkowej akcji po switch.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-055

Zakres oceny: atmostoneScorpioperhex,otherstackingrulesretained

Porównanie oceniającego: R983 zachowuje maksimum jeden Scorpio na heks i all other stacking rules. Nie przyznaje automatycznej legalności współzajęcia. G-D983stack blocking=true dotyczy pełnych ograniczeń, nie znanego lokalnego maksimum.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.83-01, PDF 36 left. Wybrany literalny zakres: 9.83 Only one Scorpio unit may occupy any one hex. All other stacking rules apply.

first-001 R983, `/rules/36`, bajty [352459,356106), SHA-256 `f7d2aafc87c8ed78040ffececeea0285fff874b6b06483f0065d8564c626e87f`.

context-01 R983, `/rules/36`, bajty [425501,429280), SHA-256 `7a009418ad0af36b8ee5ca3de17a068395e17db2e7da4760ace20689e5366e00`.

Niepewności i wyłączenia: Pełna legalność współzajęcia wymaga general stacking.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-056

Zakres oceny: nofacing;allhexesFront;range/LOS/terrainnotwaived

Porównanie oceniającego: R984: brak facing, ruch/fire w dowolnym kierunku niezależnie od orientacji counter, wszystkie heksy Front. Nie ma zniesienia mode, range/LOS lub terrain; nie oceniono zewnętrznych ograniczeń ani konkretnego strzału.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.84-01, PDF 36 left. Wybrany literalny zakres: 9.84 Scorpio units have no facing; they may move or fire in any direction, regardless of the direction the actual counter is pointed. All hexes are considered Front hexes.

first-001 R984, `/rules/37`, bajty [356112,359528), SHA-256 `de911fdc0696db757fc4653804f89e65ed4a57ec809e9dd48209d12f438a56a5`.

context-01 R984, `/rules/37`, bajty [429287,432825), SHA-256 `1c7feae738ab6c980bff3d77751acadc52dc149fb5e6ab07b6dbfcb090e4ec60`.

Niepewności i wyłączenia: Nie znosi range/LOS/terrain.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-057

Zakres oceny: ActiveFiremax2/GameTurnandmax1/friendlyOrdersPhaseinMovementMissilesegment;Once/Finished;afteractiveFire nootheractionthatphaseincludingRecovery

Porównanie oceniającego: R985 zachowuje max 2 active shots/Game Turn, max 1/friendly Orders Phase w Movement and Missile Fire Segment, bez order. Pierwszy Once, drugi Finished w R985 i N985markers; grafika pokazuje oba. Po fire brak innych działań tej Orders Phase, w tym Recovery. Nie myli Game Turn z Orders Phase i nie przyznaje fire w Move.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.85-01, PDF 36 left. Wybrany literalny zakres: 9.85 Active Fire: Scorpios may fire of- fensively twice per Game Turn (not Orders Phase) during any friendly Orders Phase. They do not need an order to fire and can fire at any time during the active player’s Movement and Missile Fire Segment, no more than one shot per Orders Phase. The first time a Scorpio unit fires, place an ACTIVE FIRE ONCE mark- er on it. The second time it fires, flip the marker to its ACTIVE FIRE FINISHED side. A Scorpio that fires cannot do anything else that Orders Phase (such as recover Hits).

Źródło: G-04, PDF 36 left. Grafika; ratingi wyłączone.

first-001 N985markers, `/nodes/34`, bajty [150642,151434), SHA-256 `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.

first-001 R985, `/rules/38`, bajty [359534,364613), SHA-256 `9083d4f2690f24d2424f617dbf3a0b4481149a19932798070e26fcfe4b74207e`.

context-01 N985markers, `/nodes/34`, bajty [199790,200614), SHA-256 `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.

context-01 R985, `/rules/38`, bajty [432832,438091), SHA-256 `15e7d8e13c9489316c465caf3fb6ec40f605189e3145e013051d7ec031e0dea3`.

Niepewności i wyłączenia: Warunki range/LOS/MRRC i mode9.82 nadal obowiązują.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-058

Zakres oceny: specialReactionFiremax2/enemyOrdersPhasein enemyMovementMissilesegment,includingduringenemyunitmovement;ordinary8.2ReactionFireforbidden;sourceanymovementdoesnotgrantScorpiofireinMovemode

Porównanie oceniającego: R986 zachowuje specjalne 2 shots/enemy Orders Phase podczas enemy Movement and Missile Segment, także w trakcie ruchu enemy, i zakaz ordinary Reaction Fire 8.2. Conditions jawnie Fire mode under9.82. Once/Finished opisane w prozie; N986marker uczciwie odróżnia pokazane Once od Finished z tekstu. Lokalna propozycja nie uchyla zakazu Reaction Fire any kind podczas Rampage w R914; brak pary DEP-NEW-003 pozostaje SEM-006, bez naprawy/TP/FN.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.86-01, PDF 36 left. Wybrany literalny zakres: 9.86 Reaction Fire: Scorpios may fire twice per enemy Orders Phase at any time during the enemy Movement and Missile Seg- ment—and we mean “any”; they may fire even during enemy movement! The first time the Scorpio unit fires, place a REACTION FIRE ONCE marker on it. The second time it fires, flip the marker to its REACTION FIRE FINISHED side. Scorpios, however, cannot use any type of ordinary Reaction Fire (8.2).

Źródło: G-05, PDF 36 left. Grafika; ratingi wyłączone.

first-001 N986marker, `/nodes/35`, bajty [151440,152165), SHA-256 `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.

first-001 R986, `/rules/39`, bajty [364619,369123), SHA-256 `64c29b4c0d2490544011c5ceb97b13ba7cd008eb4729f5055d1ca9665796cca7`.

first-001 R982, `/rules/34`, bajty [343925,349222), SHA-256 `db2932e05afee950e1d27137b71fe09be42fd41a52f8e80905dc27726cf31a48`.

first-001 R914, `/rules/4`, bajty [191201,210006), SHA-256 `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

context-01 N986marker, `/nodes/35`, bajty [200621,201375), SHA-256 `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.

context-01 R986, `/rules/39`, bajty [438098,442766), SHA-256 `4cf0366781c3358abc98fff09da31c4c44d05d4c9dae4f10f7cd6443e2c714da`.

context-01 R982, `/rules/34`, bajty [416661,422148), SHA-256 `c322a28fb1c69bff5deac677b5a8ee02c5c27f63d0f17bce8a72a482a530f988`.

context-01 R914, `/rules/4`, bajty [257723,277141), SHA-256 `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

Niepewności i wyłączenia: No Reaction Fire any kind w Rampage9.14 nadal wyłącza trigger; zewnętrzny ogień i segment wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-059

Zakres oceny: incur/recoverHitsasgeneralunits;Routimmediateelimination

Porównanie oceniającego: R987 zachowuje incurring/recovering Cohesion Hits jak inne jednostki i natychmiastową eliminację przy Rout. Nie zgaduje triggeru Rout ani liczby odzyskiwanych Hits. R985 osobno zachowuje zakaz Recovery w fazie active fire; brak pełnej procedury recovery nie blokuje podanego lokalnego skutku Rout.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.87-01, PDF 36 left. Wybrany literalny zakres: 9.87 Scorpios incur and recover Cohesion Hits as any other unit. A Scorpio that routs is immediately eliminated.

first-001 R987, `/rules/40`, bajty [369129,372461), SHA-256 `0bdf1d408d64bb25daf21ea3f60f30aeb4ff91ce89afa5fc8f59908eba99ca8a`.

first-001 R985, `/rules/38`, bajty [359534,364613), SHA-256 `9083d4f2690f24d2424f617dbf3a0b4481149a19932798070e26fcfe4b74207e`.

context-01 R987, `/rules/40`, bajty [442773,446233), SHA-256 `4319d42d58befea89683b3ce1da7b0ca03bb21ea982de7aaa504ab436290a229`.

context-01 R985, `/rules/38`, bajty [432832,438091), SHA-256 `15e7d8e13c9489316c465caf3fb6ec40f605189e3145e013051d7ec031e0dea3`.

Niepewności i wyłączenia: Trigger Rout i recovery amounts wymagają general rules.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-060

Zakres oceny: BI no terrainCohesionHits crossing/enteringpassableterrain or facingRough;MP/passabilitynotwaived;noColumn/PAW/OW

Porównanie oceniającego: R991 zachowuje 0 terrain Cohesion Hits tylko przy crossing/entering passable terrain oraz facing Rough. Kontynuacja w prawej kolumnie zakazuje Column6.7, PAW6.8 i OW6.5. Nie wyzerowano MP ani nie zezwolono na impassable terrain. Definicje zakazanych procedur nonblocking nie stanowią zgody na ich wykonanie.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.91-02, PDF 36 left. Wybrany literalny zakres: Barbarian Infantry (BI) units do not incur Cohesion Hits for crossing or entering any type of passable terrain, nor do they incur Cohesion Hits for changing facing in Rough terrain. BI units

Źródło: C-9.91-02, PDF 36 right. Wybrany literalny zakres: cannot use Column Movement (6.7), Pre-Arranged Withdrawal (6.8), or Orderly Withdrawal (6.5).

first-001 R991, `/rules/41`, bajty [372467,377217), SHA-256 `54dcf8cd5202e6beebb7d87fcb4104ee5d6b6b3b8737e8ad794d6665eb6c387b`.

context-01 R991, `/rules/41`, bajty [446240,451161), SHA-256 `5e41692ae51622c98f8ec0c02518e45efed39da42849c4d7693b20f9138a770c`.

Niepewności i wyłączenia: Passability/koszt MP wymagają Movement Cost Chart, zakazy nie wymagają wykonania zabronionych procedur.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-061

Zakres oceny: Recoveryorderonly1CH;depletedBIeliminatedinsteadofRout;do notautomaticallytreatthateliminationasRoutforFerocity;fulltriggerorderingnotresolved

Porównanie oceniającego: R993: tylko 1 Cohesion Hit/Recovery order; Depleted BI eliminated instead of Rout. Zestawione R994 ma trigger BI Routs, więc nie utożsamiono tego zastąpienia z jawnym Rout dla Ferocity. Pełne ordering i depletion/recovery eligibility pozostają poza zakresem; established_absent w exceptions nie jest ogólnym brakiem wyjątków.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.93-02, PDF 36 right. Wybrany literalny zakres: BI units can only remove 1 Cohesion Hit per Recovery order.

Źródło: C-9.93-03, PDF 36 right. Wybrany literalny zakres: Depleted BI units do not Rout but are instead eliminated.

first-001 R993, `/rules/42`, bajty [377223,381102), SHA-256 `ac9f1b844e212d7c1ed2c0b307f8f974da613cd2137afc21a716bd6ff2f5d820`.

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

context-01 R993, `/rules/42`, bajty [451168,455190), SHA-256 `fdf01acb9629e037cb6f43e05f89f53320c84ff76245e149f5dce967553aa1f3`.

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

Niepewności i wyłączenia: Depleted stan i inne warunki recovery wymagają kontekstu; konflikt z Ferocity po depleted elimination nie rozstrzygnięty.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-062

Zakres oceny: BI startFerocity;BI PreShock-1DRM and defenders+2DRM inshownscope,othermodifiers/procedureunknown

Porównanie oceniającego: R994.conditions zachowuje start game Ferocity dla all BI. Action/parameters: własny Pre-Shock TQ -1 DRM, defending units +2 DRM. To nie modyfikatory wszystkich TQ checks, nie +2 dla BI. Brak scenariusza i base Pre-Shock nie blokuje znanych lokalnych operatorów przy zadanych faktach.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.94-02, PDF 36 right. Wybrany literalny zakres: All BI units start the game with Ferocity. A BI unit with Ferocity earns a –1 DRM to its Pre-Shock TQ die roll while penalizing the defending unit(s) with a +2 DRM to their Pre-Shock TQ die roll(s).

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

Niepewności i wyłączenia: Inne DRM i Pre-Shock procedure nie są domknięte.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-063

Zakres oceny: EachordinaryBI RouttriggersFerocitycheckagainstscenarioassignedleaderInitiative;DR<=retains,>losespermanentlyforthatleaderBIcommand,othersunaffected

Porównanie oceniającego: R994 zachowuje check each time BI Routs wobec Initiative leader przypisanego w scenario setup; DR<=Initiative zatrzymuje, wyższy trwale odbiera Ferocity BI tego dowódcy, inne commands bez skutku. Depleted elimination z R993 nie jest automatycznie tym triggerem. Nie wybrano dowódcy ani ratingu.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.94-03, PDF 36 right. Wybrany literalny zakres: Ferocity continues until the BI’s leader (as given in the scenario setup) fails a Ferocity check, which the player conducts each time a BI unit Routs. The player rolls the die and compares it to the leader’s Initiative Rating. If the DR is the same or lower, BI units retain their Ferocity, otherwise Ferocity is permanently lost for BI under the command of that leader. The loss of Ferocity for the units under one leader has no effect on the Ferocity of units under the command of different leaders.

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

first-001 R993, `/rules/42`, bajty [377223,381102), SHA-256 `ac9f1b844e212d7c1ed2c0b307f8f974da613cd2137afc21a716bd6ff2f5d820`.

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

context-01 R993, `/rules/42`, bajty [451168,455190), SHA-256 `fdf01acb9629e037cb6f43e05f89f53320c84ff76245e149f5dce967553aa1f3`.

Niepewności i wyłączenia: Scenario commander mapping i Initiative muszą być dostępne; depleted elimination ≠ jawny Rout trigger.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-064

Zakres oceny: Actualleader/Initiative/membership requires scenariosetup;no nearest/favorable default

Porównanie oceniającego: R994/R995 odwołują się do scenario-assigned command, G-D994scenario i G-D995scenario jawnie blocking=true. Potrzebne actual leader, Initiative i BI membership nie zostały zastąpione najbliższym lub korzystnym leader. Propozycja przyjmuje poprawną potrzebę/blokadę źródła; brak danych wciąż blokuje pełne rzeczywiste zastosowanie, a zadane syntetyczne facts mają własny lokalny zakres.

Propozycja: `source_block_supported`. Obie decyzje właściciela pending.

Źródło: C-9.94-03, PDF 36 right. Wybrany literalny zakres: Ferocity continues until the BI’s leader (as given in the scenario setup) fails a Ferocity check, which the player conducts each time a BI unit Routs. The player rolls the die and compares it to the leader’s Initiative Rating. If the DR is the same or lower, BI units retain their Ferocity, otherwise Ferocity is permanently lost for BI under the command of that leader. The loss of Ferocity for the units under one leader has no effect on the Ferocity of units under the command of different leaders.

Źródło: C-9.95-02, PDF 36 right. Wybrany literalny zakres: At the start of a battle, the Gauls usually worked themselves into a fever pitch, which translated into an all-out charge. To reflect this, at the start of a game, all BI units have their MA increased by 1. Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls. Impetuosity lasts until at least two BI units of a leader’s command enter an enemy ZOC, at which point Impetuosity continues for the rest of the Game Turn, after which it is lost. Only the BI units in that command (per the sce- nario setup) are affected.

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

first-001 R995, `/rules/44`, bajty [386929,392597), SHA-256 `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

context-01 R995, `/rules/44`, bajty [461228,467103), SHA-256 `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.

Niepewności i wyłączenia: Actual leader, Initiative and BI command membership require scenario setup.; Jedno wskazane przypisanie scenario wraz z ratings, nie domyślny najbliższy leader.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-065

Zakres oceny: BI startMA+1 and commandingLeader-1allfirsttryMomentum;after>=2distinctBIofsamecommandenterenemyZOC,Impetuosity lastsrestofthatGameTurn thenlostforthatcommandonly

Porównanie oceniającego: R995: wszystkie BI startują MA+1, leaders commanding BI -1 do all first-try Momentum rolls. Trigger >=2 BI units tego samego command entering enemy ZOC, a nie dwie wizyty jednej jednostki. Efekt trwa resztę tego Game Turn i wygasa potem tylko dla tego command. Nie natychmiast po triggerze ani dla całej armii.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.95-02, PDF 36 right. Wybrany literalny zakres: At the start of a battle, the Gauls usually worked themselves into a fever pitch, which translated into an all-out charge. To reflect this, at the start of a game, all BI units have their MA increased by 1. Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls. Impetuosity lasts until at least two BI units of a leader’s command enter an enemy ZOC, at which point Impetuosity continues for the rest of the Game Turn, after which it is lost. Only the BI units in that command (per the sce- nario setup) are affected.

first-001 R995, `/rules/44`, bajty [386929,392597), SHA-256 `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.

context-01 R995, `/rules/44`, bajty [461228,467103), SHA-256 `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.

Niepewności i wyłączenia: Mapping command, ZOC i Momentum wymagają danych; lokalny czas wygaśnięcia jest jawny.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-066

Zakres oceny: GallictransportCHCombatTablesignoreinstruction retained;exacttables/entriesrequirecontext alreadyRQ05scope

Porównanie oceniającego: R996note zachowuje ignore Chariots reference on Combat Tables; N996design nie tworzy dodatkowego skutku. N-14-S2 to dokładna instrukcja, N-14-S3 appearances Sentinum/Telamon, bez listy eligibility wszystkich LI. G-D996tables deklaruje potrzebę actual tables/entries, ale blocking=false; D996tables blocks_full_result=false. Lokalny zakaz użycia wiersza znany, konkretne identyfikowanie suppressowanych entries niezamknięte. Właściciel rozstrzyga wystarczalność jawnej blokady zależnego pełnego pytania. Nie ma konkretnego niepoprawnego lookupu, nie jest to automatyczny błąd odczytu lub FP.

Propozycja: `partial_context_declaration_pending`. Obie decyzje właściciela pending.

Źródło: N-14-S2, PDF 36 right. Wybrany literalny zakres: Thus, ignore the reference to Chariots on the Combat Tables.

Źródło: N-14-S3, PDF 36 right. Wybrany literalny zakres: However, the tribes were quite adept at using them to whatever advantage they did of- fer. In this module, chariots make an appearance at Sentinum and Telamon.

first-001 N996design, `/nodes/30`, bajty [146679,147468), SHA-256 `c01e2df13e259d2b65d4ec89dee199481937bd990757f3a83e9f9dc5ce3784dd`.

first-001 R996note, `/rules/45`, bajty [392603,396286), SHA-256 `3dfdaccd8a573ddf99e083715c467fb8a36ec4ad52929c71b7259de8de628ab5`.

first-001 D996tables, `/dependencies/108`, bajty [512527,513635), SHA-256 `1f7003a3d4d4e84827c18ca49ade9e7bb6d3e7bf41627b4af176911bda5c0b8a`.

first-001 G-D996tables, `/gaps/68`, bajty [561690,562253), SHA-256 `4d25580273e2f47e9861742228dfda824e123a8c160529580af039237d78a715`.

context-01 N996design, `/nodes/30`, bajty [195676,196492), SHA-256 `7ad32edfe26a51d99e6ab415bbb1f85fc82f8061c5071dd33970b43437e5378f`.

context-01 R996note, `/rules/45`, bajty [467110,470918), SHA-256 `88c04eae1baf89929461610b1d701ea1201da58987d814350fdcfb5516d2ec76`.

context-01 D996tables, `/dependencies/108`, bajty [590968,592103), SHA-256 `f4555792332ddf87bf519ee6a9231583e2516e597f413bb1afa7a4b5ea93bccb`.

context-01 G-D996tables, `/gaps/68`, bajty [647668,648248), SHA-256 `709d00bec15889990cc4d425d9ee7b2f041b8814b8f0bf029e59286bcc067d4b`.

Niepewności i wyłączenia: Exact Combat Tables and relevant entries are required; no values are guessed.; Dokładne Combat Tables i ich chariot entries, decision owner o zakresie; nie traktować Sentinum/Telamon jako listy eligibility wszystkich LI.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-067

Zakres oceny: CHonlyMA,noSize/TQ;cannotmoveincludingOWwithouteligibleLI;enemycombatmovingadjacenttosolitaryCH eliminatesit;staticadjacency notthegivenmovementtrigger

Porównanie oceniającego: R996a: CH ma tylko MA, brak Size/TQ. Bez stacked eligible LI zakaz wszelkiego ruchu, także OW. Enemy combat unit any type moving adjacent do CH alone eliminuje go natychmiast. Static adjacency nie jest podanym triggerem. Szerszy time_limits mówi qualifying adjacency; operacyjny trigger pozostaje w action_effect. Nie nadaje się CH ratingów Roman top-unit.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.96-02, PDF 36 right. Wybrany literalny zakres: Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating. These units cannot move at all, and this includes Orderly Withdrawal, unless stacked with an eligible Light Infantry (LI) unit. If an enemy combat unit (of any type) moves adjacent to a CH unit alone in a hex, the CH unit is immediately eliminated.

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

Niepewności i wyłączenia: Eligibility LI scenariuszowa nieuzupełniona; samotny CH da się ocenić lokalnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-068

Zakres oceny: oneLIperCH,CHtopdenotesmounted,combinedsingleforstackingbutotherrestrictionsretained

Porównanie oceniającego: R996b zachowuje jeden LI na CH, CH na górze oznacza mounted, kombinacja single unit tylko dla stacking; all other restrictions dla CH+LI i CH alone nadal obowiązują. Continuation PDF36right→37left zawiera pełne zdanie. Nie stosuje Roman top/TQ do transport CH i nie przyznaje pełnej legalności stacking.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.96-03, PDF 36 right. Wybrany literalny zakres: Each CH unit may carry one Light Infantry (LI) unit. To denote that a LI unit is mounted on the CH unit, place the CH on top of the LI unit. The combined CH and LI unit is treated as a single

Źródło: C-9.96-03, PDF 37 left. Wybrany literalny zakres: unit for stacking purposes. All other stacking restrictions apply to both a CH+LI stack and a CH alone in the hex. There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH. However, a dismounting LI unit may continue to move only if the LI+CH combination moved less than the LI’s printed Movement Allowance. The number of MP allowed is equal to the difference. Conversely, an LI unit mounting a CH can continue to move (as a mounted CH) up to the MA of the CH unit less the number of MP already used by the LI prior to mounting the CH. While stacked with an LI, the CH expends MP to enter/cross terrain or is prohibited from entering/crossing terrain per the Movement Cost Chart. However, Cohesion Hits for movement are applied to the LI only; CH units do not suffer Hits for Movement/Terrain.

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

Niepewności i wyłączenia: Nie używać roman top/TQ jako zasad CH; brak TQ/Size CH zachować.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-069

Zakres oceny: mount/dismount0MP/CH;dismountcontinueonlyifcomboMPspent<LIprintedMA,remainingdifference;mountremainingCHMAminusLIalreadyusedMP

Porównanie oceniającego: R996b: mount/dismount 0 MP i 0 Cohesion Hits dla LI. Dismount dalszy ruch tylko gdy combo MPs used < LI printed MA, pozostałe MP równe różnicy. Mount pozwala kontynuować jako CH do CH MA minus MPs already used przez LI. Strict < i printed LI MA zachowane; nie odtworzono MP od zera, żadna trasa/eligibility/MA nie została zgadnięta.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.96-03, PDF 36 right. Wybrany literalny zakres: Each CH unit may carry one Light Infantry (LI) unit. To denote that a LI unit is mounted on the CH unit, place the CH on top of the LI unit. The combined CH and LI unit is treated as a single

Źródło: C-9.96-03, PDF 37 left. Wybrany literalny zakres: unit for stacking purposes. All other stacking restrictions apply to both a CH+LI stack and a CH alone in the hex. There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH. However, a dismounting LI unit may continue to move only if the LI+CH combination moved less than the LI’s printed Movement Allowance. The number of MP allowed is equal to the difference. Conversely, an LI unit mounting a CH can continue to move (as a mounted CH) up to the MA of the CH unit less the number of MP already used by the LI prior to mounting the CH. While stacked with an LI, the CH expends MP to enter/cross terrain or is prohibited from entering/crossing terrain per the Movement Cost Chart. However, Cohesion Hits for movement are applied to the LI only; CH units do not suffer Hits for Movement/Terrain.

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

Niepewności i wyłączenia: Ocenia się lokalny budżet przy supplied eligibility, MA i MP; trasa wymaga tabeli.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-070

Zakres oceny: MovementCostChart governsCHMP/prohibitions;movementCohesionHitsLIonly,notCH;no waiverofterrainprohibitions

Porównanie oceniającego: R996b zachowuje CH MP costs oraz zakazy entering/crossing według Movement Cost Chart przy LI. Movement/Terrain Cohesion Hits do LI only, CH ich nie otrzymuje. G-D996movement blocking=true dla konkretnej trasy. To nie zwolnienie z zakazu terenu ani zwolnienie LI z wszystkich Hits.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.96-03, PDF 36 right. Wybrany literalny zakres: Each CH unit may carry one Light Infantry (LI) unit. To denote that a LI unit is mounted on the CH unit, place the CH on top of the LI unit. The combined CH and LI unit is treated as a single

Źródło: C-9.96-03, PDF 37 left. Wybrany literalny zakres: unit for stacking purposes. All other stacking restrictions apply to both a CH+LI stack and a CH alone in the hex. There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH. However, a dismounting LI unit may continue to move only if the LI+CH combination moved less than the LI’s printed Movement Allowance. The number of MP allowed is equal to the difference. Conversely, an LI unit mounting a CH can continue to move (as a mounted CH) up to the MA of the CH unit less the number of MP already used by the LI prior to mounting the CH. While stacked with an LI, the CH expends MP to enter/cross terrain or is prohibited from entering/crossing terrain per the Movement Cost Chart. However, Cohesion Hits for movement are applied to the LI only; CH units do not suffer Hits for Movement/Terrain.

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

Niepewności i wyłączenia: Konkretna trasa bez Movement Cost Chart pozostaje zablokowana.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-071

Zakres oceny: repeat-movementHitexceptiononlyentireOrdersPhasemounted;partialphasemountinsufficient

Porównanie oceniającego: R996c: zwolnienie LI z second/third movement Hits w Game Turn tylko jeśli entire Orders Phase mounted. Wybrany literalny cytat urywa się przed if, lecz conditions i action_effect zachowują całe ograniczenie. Nie przyznano zwolnienia za częściowe mount lub dla terrain Hits.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.96-05, PDF 37 left. Wybrany literalny zakres: • LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn, if they spend the entire Orders Phase mounted on the CH unit.

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

Niepewności i wyłączenia: General repeat movement i pozostałe terrain Hits oddzielnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-072

Zakres oceny: mountedLInoShockattack,mustdismount;defendsasLI,notfullattackpermissionafterdismount

Porównanie oceniającego: R996c jawnie Mounted LI cannot Shock attack; must dismount; defends as LI. Dismount jest konieczny, nie stanowi pełnej zgody na późniejszy attack bez pozostałych warunków. Nie zamieniono defend as LI na attack jako cavalry.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.96-06, PDF 37 left. Wybrany literalny zakres: • LI cannot Shock attack; they must dismount to do so. When mounted, they defend as LI.

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

Niepewności i wyłączenia: Dismount nie dowodzi legalności późniejszego attack bez pozostałych warunków.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-073

Zakres oceny: Mounted LI uses Mounted Javelin MRRC, is exempt from Missile Supply 8.17 while mounted, removes LOW/NO on mounting, and uses H&D as cavalry. No post-dismount supply state or equivalence with the hypothesized 9.13 row is inferred.

Porównanie oceniającego: R996d zachowuje dokładnie nazwę Mounted Javelin MRRC, exemption Missile Supply8.17 while mounted, remove LOW/NO when mounts i H&D as cavalry. Nie zgaduje post-dismount supply, nie utożsamia tej row z hipotetycznym 9.13. G-D996MRRC/HD blocking=true; nonblocking supply dotyczy znanego lokalnego wyjątku/marker removal, bez rozstrzygania pełnej procedury.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło: C-9.96-07, PDF 37 left. Wybrany literalny zakres: • LI may use Missile Fire using the Mounted Javelin row on the MRRC. Missile Supply (8.17) does not apply while the LI unit is mounted. Remove any MiSSile low/No markers from the LI unit when the unit mounts a CH. They may use Harassment and Dispersal fire as if they were cavalry units.

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

Niepewności i wyłączenia: Nie zgadywać podaży po późniejszym dismount ani pełnego MRRC/H&D; display annotation06c zachowuje original helper.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-074

Zakres oceny: Confirm actualidentifiedunit TQ/MA before concreteuse; not alltinygraphicratings were individuallyverified inthisreview. SyntheticinputTQ6 doesnotestablishactualLeaderElephantTQ. Keeprequires_context foractualvalues.

Porównanie oceniającego: N911counter/N921counter/N981counter podają visible glyphs, lecz wyraźnie wykluczają game-wide values i rating-position inference. N966diagram mówi illustrative, not general Roman parameters; N985markers/N986marker to stany markerów. Brak twierdzenia o realnym Leader Elephant TQ6. Równocześnie nie ma osobnego gap ani jawnej conditional blocking deklaracji actual identified TQ/MA przed concrete use. Właściciel rozstrzyga, czy zapis illustrative wystarcza dla ograniczonego wymagania EXP-074. Same oględziny paneli/states nie certyfikują małych ratingów, tożsamości konkretnych jednostek ani 64 granic glifów. Criticality pozostaje conditional_on_concrete_parameter_use.

Propozycja: `illustration_boundary_supported_block_declaration_pending`. Obie decyzje właściciela pending.

Źródło: G-01, PDF 31 right. Grafika; ratingi wyłączone.

Źródło: G-02, PDF 33 right. Grafika; ratingi wyłączone.

Źródło: G-03, PDF 36 left. Grafika; ratingi wyłączone.

Źródło: D-02, PDF 35 left. Grafika; ratingi wyłączone.

Źródło: G-04, PDF 36 left. Grafika; ratingi wyłączone.

Źródło: G-05, PDF 36 left. Grafika; ratingi wyłączone.

first-001 N911counter, `/nodes/31`, bajty [147474,148541), SHA-256 `23d5455d6e3e846f2793ab9162a4d52e351dec50fdbb6c82f9bbdf60726cf009`.

first-001 N921counter, `/nodes/32`, bajty [148547,149599), SHA-256 `30e857892be2b6c8be03571a7cf4d4176065f50d0ebbc1464ce5742405a3dc86`.

first-001 N966diagram, `/nodes/7`, bajty [128977,130323), SHA-256 `f5c32b1dae24067c8069c9f6a259e1da4cd473f61255ce80b5b070a71cc69689`.

first-001 N981counter, `/nodes/33`, bajty [149605,150636), SHA-256 `5598ad644a67222e29a3ec1778f8d63074add8759087c77097a583b05c918b7b`.

first-001 N985markers, `/nodes/34`, bajty [150642,151434), SHA-256 `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.

first-001 N986marker, `/nodes/35`, bajty [151440,152165), SHA-256 `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.

context-01 N911counter, `/nodes/31`, bajty [196499,197607), SHA-256 `7b6b333e688ac23f557a2c1e1344876b6770501901c9407247d341dac0c97653`.

context-01 N921counter, `/nodes/32`, bajty [197614,198706), SHA-256 `0c1388f9709c55e4e5a45fc7686880da9f5078247249284e32ca56de85771f8b`.

context-01 N966diagram, `/nodes/7`, bajty [177283,178673), SHA-256 `36e8f4cd62347156e4d08983cd3b50a484a73b8478deddb5b4167d954c4d364d`.

context-01 N981counter, `/nodes/33`, bajty [198713,199783), SHA-256 `a40fc3ffd54bad133ba38846aeb3aab44303b5e8c073a04740d3cbc39f922451`.

context-01 N985markers, `/nodes/34`, bajty [199790,200614), SHA-256 `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.

context-01 N986marker, `/nodes/35`, bajty [200621,201375), SHA-256 `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.

Niepewności i wyłączenia: Actual identified counter TQ/MA and glyph values remain unconfirmed; criticality is conditional on changing outcome or legality.; Wybrany żeton/parametr z dokładnym źródłem i przeglądem, tylko jeśli sytuacja go potrzebuje.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

## Kwestie wymagające osobnej decyzji

SEM-011 / EXP-052: oba lokalne ograniczenia występują osobno. Czy ich zapis wystarcza dla koniunkcji reviewed_scope, czy brakuje jawnego powiązania? Brak pary DEP-NEW-001 zachowany; relację ocenia .4b.

SEM-012 / EXP-066: instrukcja ignore zachowana i potrzeba actual Combat Tables zadeklarowana, lecz blocking=false. Ocena dotyczy konkretnego identyfikowania wpisów; sam lokalny zakaz nie wymaga wykonania tabeli.

SEM-013 / EXP-074: illustrative/no general ratings zachowane; brak osobnego actual-value gap/conditional blocking. Nie zgadywać konkretnych TQ/MA ani przypisania ratingów do pól.

Wcześniejsze SEM-001–010 i EXP-010/017/019/040/050 pozostają pending. Brakujące krytyczne pary, E916, 64 granice glifów, pełny graf i reszta inwentarza nie zostały rozstrzygnięte. 175 przyjętych wcześniej par rubryka/EXP bez zmiany, nowe nie dają dodatkowych punktów.

1 dodatkowa strona/1 reguła/0 tabel, 1 runda kontekstu, 0 korekt, 0 pełnych domknięć, 4 częściowe uzupełnienia i 4 nowe deklaracje. Trzecie źródło niepozyskane, stop ekspansji na granicy 2. Pełne metryki i TP/FP/FN not_assessable; aktywny czas/budżet/config/tokeny/cena unknown. Listing/path discovery poza allowlistą potwierdzony; odczyt treści oceny niezaobserwowany, ekspozycja/czysty kontekst unknown.

Następna praca: decyzje właściciela dla tego pakietu i wcześniejszych pending; następnie osobna .4b, później .4c/.4d, z dalszym podziałem przed wykonaniem jeśli potrzebny. M-POC5A i .4 partial, M-POC5 jedyny next.
