# M-POC5A.4b1 — rzeczywiste porównania relacji

Recenzent propozycji: Codex. Znaczenie akceptuje właściciel; wszystkie nowe decyzje waiting_review.

65 ID /125 wystąpień: first60, context65. Dodatkowo22 zamrożone pary osobno dla obu odpowiedzi. 60 ID/116 wystąpień ma pozytywną propozycję w dokładnym ograniczonym zakresie;5 ID/9 wystąpień wydzielono do decyzji. To nie liczby poprawnych całych rekordów/TP.

first-001: SHA-256 `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: SHA-256 `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`; źródło PDF `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

[Pełne porównania JSON](comparisons.json): osobne oba hashe, source/targetscope, dosłowne źródła i zapisy modelu, pointers, bajty [start,end), SHA-256 rekordów/pól, gapy, dowody i wyłączenia.

## Każde przypisane ID

### D1011descriptor

Źródło: 10.11: chart summarizes timing/results of TQ checks

Cel: 8.75: purpose of Cohesion Hit and TQ Check Chart, not chart cells

Potrzeba/konsekwencja braku: Opis pojęcia; sam lokalny test ze znanym DR/TQ nie wymaga nowego odczytu chart. Bez chart brak pełnego wykazu wyników i momentów.

Porównanie/propozycja: N1011→N875 ma poprawny kierunek i jawne odwołanie 8.75. Definition można przyjąć wyłącznie jako identyfikację roli chart; dane tabeli i D1011chart pozostają poza zakresem.

**first-001:** `/dependencies/25`, bajty [436644,437389), fragment SHA-256 `8e72600dc9c92372356715c6177ed1b0b4ffc71b2e2d4849e5ad48ab0142c991`.

Zapis modelu: `N1011→N875`, `definition/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 8.75 supplied descriptor identifies the referenced chart’s purpose; actual chart use is separately unresolved.

**context-01:** `/dependencies/25`, bajty [512651,513418), fragment SHA-256 `b2cd77bbdbac5973150ea2584b475571532a98f2b5ab30ea29fc5fe83f066a8d`.

Zapis modelu: `N1011→N875`, `definition/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 8.75 supplied descriptor identifies the referenced chart’s purpose; actual chart use is separately unresolved.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/14/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.11 TQ Checks: The Cohesion Hit and TQ Check Chart gives
> the times during the game when a unit must undergo a TQ check.
> These instances have also been noted throughout the rules. A TQ
> check consists of rolling the die and comparing it to the unit’s
> printed TQ rating, and applying the result given on the chart—
> usually one or more Cohesion Hits if the DR exceeds the rating.
> Exception: Routed units use a TQ of 1 for all TQ checks instead
> of the printed TQ.
> 

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/1/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 8.75 The Cohesion Hit and TQ Check Chart: Use this as
> a summary of when Cohesion Hits are applied and when TQ
> checks take place.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D911914

Źródło: 9.11 step 3: post-Shock placement only if infantry did not rout and EL has not rampaged

Cel: 9.14: Rout initiates Rampage, including Leader EL

Potrzeba/konsekwencja braku: Warunek konieczny dla tego placement; bez stanu Rampage nie wolno wybrać Rear. Cel lokalny dostępny, pełna historia Rampage nie wynika z samej pary.

Porównanie/propozycja: R911→R914 condition/explicit odpowiada DEP-002. R911 zachowuje non-rout, wolny Rear, wybór gracza EL i facing. Przyjąć dokładnie sprawdzenie braku Rampage dla placement, bez wyniku całej procedury.

**first-001:** `/dependencies/34`, bajty [443469,444133), fragment SHA-256 `52cd2f6dd3b1b0bcb714e3aa767d8b0ae477b4c473171b6ee7912de58ea56298`.

Zapis modelu: `R911→R914`, `condition/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.11 Step 3 explicitly tests whether Elephant has rampaged under 9.14.

**context-01:** `/dependencies/34`, bajty [519683,520368), fragment SHA-256 `adaf97de357b4052a84e2de33e645e4b858b5229da349a4ca80b65246f15953a`.

Zapis modelu: `R911→R914`, `condition/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.11 Step 3 explicitly tests whether Elephant has rampaged under 9.14.

source_evidence: `C-9.11-09` / `/items/19`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.

target_evidence: `C-9.14-01` / `/items/28`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.14 Elephant Rampage: When an Elephant unit routs, it Ram-
> pages. Leader Elephants also Rampage, but they have less of a
> chance of doing so. Each time an Elephant unit routs, its player
> rolls the die and does one of the following, depending on the DR:

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D911rout

Źródło: 9.11 step 3: infantry did not rout

Cel: 10.14: ordinary Hits>=TQ Rout threshold

Potrzeba/konsekwencja braku: Niejawna definicyjna przesłanka ustalenia stanu Rout; przy zadanym stanie nie potrzeba lookupu. 10.2 i pełne wyjątki rozstrzygnięcia Rout nie są zamknięte.

Porównanie/propozycja: R911→N1014 condition/implicit poprawnie prowadzi od warunku placement do progu. Przyjąć tylko zwykły próg, nie równoważność wszystkich zdarzeń Rout z Hits>=TQ; dostarczone 10.15 może kwalifikować jednoczesny Rout obu stron.

**first-001:** `/dependencies/27`, bajty [438171,438922), fragment SHA-256 `80bdf532d2d054a256e7ffb3172204ede4af435f4e8f748d4144238ac90ecdee`.

Zapis modelu: `R911→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

**context-01:** `/dependencies/27`, bajty [514224,514997), fragment SHA-256 `7d5da688bff063363aaf8e8ec40e90d0c75c4b396adf25ad0e373467ca5326ac`.

Zapis modelu: `R911→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

source_evidence: `C-9.11-09` / `/items/19`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.14 When a unit has absorbed Cohesion Hits equal to or more
> than its TQ rating, it routs (10.2).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D912MRRCdef

Źródło: 9.12: Elephant Screen MRRC row for Reaction Fire only

Cel: 8.71: MRRC purpose (missile strength at range)

Potrzeba/konsekwencja braku: Ta krawędź identyfikuje opis chart; nie wykonuje row. Brak opisu nie blokuje lokalnego zakazu, brak row blokuje konkretny fire wynik.

Porównanie/propozycja: R912→N871 mention/explicit poparte nazwą MRRC i opisem 8.71. Przyjąć odwołanie do opisu, z wyłączeniem wykonawczego D912MRRC i realnych danych wiersza.

**first-001:** `/dependencies/37`, bajty [445611,446300), fragment SHA-256 `ac5874d5f9639b2848f65c01a9eed791ba552592beb66e84b9e7313685f27c5e`.

Zapis modelu: `R912→N871`, `mention/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Supplied 8.71 gives MRRC purpose, not Elephant Screen row results.

**context-01:** `/dependencies/37`, bajty [521893,522604), fragment SHA-256 `34033de084d7d3fdd5cb8419ca024001e05023b431b542fc931854293d1e0a8a`.

Zapis modelu: `R912→N871`, `mention/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Supplied 8.71 gives MRRC purpose, not Elephant Screen row results.

source_evidence: `C-9.12-02` / `/items/23`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Elephant Screens can Missile Fire with Reaction Fire (8.2) only,
> using the Elephant Screen row on the MRRC. Elephant Screens

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/1/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 8.71 The Missile Range and Results Chart: This table is used
> to determine the strength of a missile unit firing at a given range.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D913screen

Źródło: 9.13: Reaction Fire with javelins and screen, separate rolls

Cel: 9.12: screen fire and Leader EL has no screen

Potrzeba/konsekwencja braku: Niejawny warunek istnienia screen konieczny do drugiego rzutu; nie przyznaje screen Leader EL. Procedury 8.2/MRRC nadal niedostępne.

Porównanie/propozycja: R913→R912 condition/implicit sensownie zawęża oba środki ognia. R913 ma szerokie Elephant may w action, R912 przechowuje wyjątek Leader. Przyjąć tylko połączenie z tym wyjątkiem, bez pełnego wyniku fire.

**first-001:** `/dependencies/119`, bajty [522697,523432), fragment SHA-256 `4b442335e9ee1bffa9c3a8ff18e49f728e63977989a88d48d6b9ddbd7c59f0b4`.

Zapis modelu: `R913→R912`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Using Elephant screen in 9.13 requires screen existence; 9.12 excludes Leader elephants and identifies screen capabilities.

**context-01:** `/dependencies/119`, bajty [601431,602188), fragment SHA-256 `a4f95450815c2b3cc12dba057be77e89ea41cb3f020a7702fdec9642a20743fb`.

Zapis modelu: `R913→R912`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Using Elephant screen in 9.13 requires screen existence; 9.12 excludes Leader elephants and identifies screen capabilities.

source_evidence: `C-9.13-01` / `/items/26`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.13 Tower Riders: The riders atop elephants were armed with
> javelins and are treated as Mounted Javelinists for Missile Fire
> purposes. The Elephant unit may use Reaction Fire with both its
> javelins and its screen, with the player rolling separately for each.

target_evidence: `C-9.12-02` / `/items/23`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Elephant Screens can Missile Fire with Reaction Fire (8.2) only,
> using the Elephant Screen row on the MRRC. Elephant Screens

target_evidence: `C-9.12-03` / `/items/24`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> have their own missile supply markers. Leader elephants do not
> have screens (they usually did, but they were too small to be a
> factor).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D914diagram

Źródło: 9.14: direction roll and illustrated refacing

Cel: local Rampage diagram/caption on PDF32

Potrzeba/konsekwencja braku: Ilustracja nie jest obowiązkową procedurą. Bez niej nadal obowiązuje map compass; brak rzeczywistego compass blokuje kierunek na mapie.

Porównanie/propozycja: R914→N914diagram mention/explicit zgodne z caption just an example. N914diagram i R914 odsyłają do compass wybranej bitwy. Przyjąć rolę ilustracji, wyłączyć odczyt małych ratingów i uniwersalny kierunek geograficzny.

**first-001:** `/dependencies/1`, bajty [418383,419105), fragment SHA-256 `eaafb54511601b5bce478b1d2430fff236520dea99125b1e87da8781d5abb699`.

Zapis modelu: `R914→N914diagram`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Diagram illustrates one facing result; caption directs actual resolution to battle map compass, not this example.

**context-01:** `/dependencies/1`, bajty [493826,494569), fragment SHA-256 `c07b274e4beab653eece3be5038a280ff95c5c2bf21905274d7c85fbdfbb7077`.

Zapis modelu: `R914→N914diagram`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Diagram illustrates one facing result; caption directs actual resolution to battle map compass, not this example.

source_evidence: `C-9.14-01` / `/items/28`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.14 Elephant Rampage: When an Elephant unit routs, it Ram-
> pages. Leader Elephants also Rampage, but they have less of a
> chance of doing so. Each time an Elephant unit routs, its player
> rolls the die and does one of the following, depending on the DR:

target_evidence: `D-01` / `/items/174`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

target_evidence: `X-01` / `/items/163`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: The above diagram shows the elephant unit refaced
> after a Rampage die roll of 1. This is just an example; use the
> compass on the map for each battle.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D914rout

Źródło: 9.14: each EL Rout triggers Rampage

Cel: 10.14 ordinary Rout threshold

Potrzeba/konsekwencja braku: Próg potrzebny gdy Rout dopiero ustalamy; zadany Rout uruchamia lokalny trigger bez dodatkowego lookupu. Ogólna procedura/wyjątki Rout pozostają poza tą definicją.

Porównanie/propozycja: R914→N1014 condition/implicit poprawne dla zwykłego progu. Leader exception dotyczy późniejszych wyników Rampage, nie zniesienia triggeru. Przyjąć tylko tę lokalną relację, bez pełnego certyfikatu Rout/10.15.

**first-001:** `/dependencies/28`, bajty [438928,439683), fragment SHA-256 `7af07a12f887d7281dec1edb6b867f45018fcb1803e9d9748bca9b5cff1df541`.

Zapis modelu: `R914→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

**context-01:** `/dependencies/28`, bajty [515004,515781), fragment SHA-256 `517e82beebd32f45d9264395f7357684be0ffbdd176c749ea0dd654edfacb31f`.

Zapis modelu: `R914→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

source_evidence: `C-9.14-01` / `/items/28`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.14 Elephant Rampage: When an Elephant unit routs, it Ram-
> pages. Leader Elephants also Rampage, but they have less of a
> chance of doing so. Each time an Elephant unit routs, its player
> rolls the die and does one of the following, depending on the DR:

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.14 When a unit has absorbed Cohesion Hits equal to or more
> than its TQ rating, it routs (10.2).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D914table

Źródło: 9.14: roll and do stated result

Cel: local Die Roll/Result table, PDF32 left 0/1–6 then right 7–9

Potrzeba/konsekwencja braku: Wykonanie wymaga właściwego wiersza. Brak tabeli uniemożliwi wynik rzutu; tabela jest dostępna. Realne nearest/map compass i inne procedury nie są przez to dostarczone.

Porównanie/propozycja: R914→N914table table_use/explicit odpowiada DEP-041. N914table zachowuje 0 Leader elimination, first/subsequent 7–9 i subsequent Leader rally TQ−2. Przyjąć tożsamość/użycie lokalnej tabeli z tymi granicami, bez glyph certificate i bez liczenia 4.84 jako pierwszego directional roll.

**first-001:** `/dependencies/0`, bajty [417649,418377), fragment SHA-256 `67d120fecb7b3722b48d27278cd13c5dd81236759ee78319fdb366b444e72cf1`.

Zapis modelu: `R914→N914table`, `table_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rampage resolution uses the printed DR/result table; rule points to used table.

**context-01:** `/dependencies/0`, bajty [493068,493819), fragment SHA-256 `7479cb8668dfd550ee24e8ca37629a12da540f389396d64c5c9f432fc2a873ff`.

Zapis modelu: `R914→N914table`, `table_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rampage resolution uses the printed DR/result table; rule points to used table.

source_evidence: `C-9.14-01` / `/items/28`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.14 Elephant Rampage: When an Elephant unit routs, it Ram-
> pages. Leader Elephants also Rampage, but they have less of a
> chance of doing so. Each time an Elephant unit routs, its player
> rolls the die and does one of the following, depending on the DR:

target_evidence: `T-01` / `/items/170`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Die Roll Result
> 0 The Elephant unit heads in the direction of the
> nearest friendly unit, opposing player’s choice
> if there is more than one nearest unit. A Leader
> Elephant is eliminated.
> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

target_evidence: `TR-01` / `/items/171`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 0 The Elephant unit heads in the direction of the
> nearest friendly unit, opposing player’s choice
> if there is more than one nearest unit. A Leader
> Elephant is eliminated.

target_evidence: `TR-02` / `/items/172`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

target_evidence: `TR-03` / `/items/173`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D9161011

Źródło: 9.16: immediate TQ check if cavalry cannot withdraw; no Leader EL

Cel: 10.11: TQ-check concept/procedure, routed TQ=1

Potrzeba/konsekwencja braku: Cel wyjaśnia TQ check; jednak 9.16 samo podaje DR>TQ i Hits, więc chart nie zastępuje lokalnego operatora. Brak 10.11 nie uzasadnia blokady DR<=TQ przy zadanych faktach.

Porównanie/propozycja: R916→N1011 ma poprawny kierunek i niejawną więź. Rodzaj definition wobec celu procedure wymaga decyzji: przyjąć komponent definicji TQ, czy użycie procedury? Nie rozstrzygać SEM-001/EXP-017 ani naprawiać E916; brak pełnego TP dla rodzaju.

**first-001:** `/dependencies/26`, bajty [437395,438165), fragment SHA-256 `040798ce6af1cfca803ee6c5b668aee59f6f24def6d77f90583a0300056fea59`.

Zapis modelu: `R916→N1011`, `definition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.16 requires immediate TQ check; supplied 10.11 defines TQ check and routed-unit TQ exception. This necessity is procedural, not merely wording.

**context-01:** `/dependencies/26`, bajty [513425,514217), fragment SHA-256 `e5f679cbfe2243f7b16b3fd47df2ef28bb8810010a966d6a409ebe15f9508bc4`.

Zapis modelu: `R916→N1011`, `definition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.16 requires immediate TQ check; supplied 10.11 defines TQ check and routed-unit TQ exception. This necessity is procedural, not merely wording.

source_evidence: `C-9.16-01` / `/items/42`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.16 Elephants vs. Cavalry: If an Elephant unit moves adjacent
> to an enemy cavalry unit from a non-adjacent hex, the cavalry
> must attempt Orderly Withdrawal. The cavalry unit cannot use
> any form of Reaction Fire if it can withdraw. If the cavalry unit
> cannot withdraw, it must undergo an immediate TQ check. If
> the DR is higher than a unit’s TQ, it incurs Cohesion Hits equal
> to the difference between the DR result and its TQ, with a mini-
> mum result of 1 Cohesion Hit. If the cavalry unit is routed, it is
> automatically eliminated, no DR necessary. This rule does not
> apply to Leader Elephants.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/14/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.11 TQ Checks: The Cohesion Hit and TQ Check Chart gives
> the times during the game when a unit must undergo a TQ check.
> These instances have also been noted throughout the rules. A TQ
> check consists of rolling the die and comparing it to the unit’s
> printed TQ rating, and applying the result given on the chart—
> usually one or more Cohesion Hits if the DR exceeds the rating.
> Exception: Routed units use a TQ of 1 for all TQ checks instead
> of the printed TQ.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D918specific

Źródło: 9.18: Unless rules specifically state otherwise

Cel: unnamed specific Elephant command exceptions, no supplied target

Potrzeba/konsekwencja braku: Informacja o możliwych wyjątkach nie blokuje zdania lokalnego. Faktyczna legalność konkretnego dowódcy wymaga rozpoznania stosownych wyjątków; nonblocking nie certyfikuje jej.

Porównanie/propozycja: R918→null mention/explicit poprawnie rejestruje zastrzeżenie i unknown exceptions. Przyjąć tylko wystąpienie odniesienia; blocks_full_result=false/G nonblocking i Any leader summary pozostają SEM-009/EXP-019, bez wyboru wariantu.

**first-001:** `/dependencies/58`, bajty [464010,465079), fragment SHA-256 `46bc37098ddd17b19bb35251ad26ded1fe92ed25c86c4c900e3c2438c05dff5b`.

Zapis modelu: `R918→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to Unless the rules specifically state otherwise; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/58`, bajty [540841,541937), fragment SHA-256 `52edbbb6bd90058a52943715a9959a7d2fec9ad9eedc21249d17952bf12a0a27`.

Zapis modelu: `R918→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to Unless the rules specifically state otherwise; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.18-01` / `/items/46`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.18 Unless the rules specifically state otherwise, Elephant units
> may be commanded by any leader.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D919chartdef

Źródło: 9.19: in addition to Shock Superiority Chart notes

Cel: 8.72: chart purpose and attacker-column reading

Potrzeba/konsekwencja braku: Opis chart nie zawiera notes. Można ustalić lokalne +1 dla African EL, lecz realna przewaga/wynik zależy od niedostarczonych notes/cells.

Porównanie/propozycja: R919→N872 mention/explicit identyfikuje opis właściwego chart. Przyjąć rolę odwołania, bez uznania opisu za notes i bez akceptacji wykonawczego D919shock.

**first-001:** `/dependencies/35`, bajty [444139,444886), fragment SHA-256 `e2a563018d8e57c3a4a4bda78adb00767b9023b01ed78e4f63b10f27f894caaa`.

Zapis modelu: `R919→N872`, `mention/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Supplied 8.72 identifies Shock Superiority Chart purpose; its actual notes are a separate unavailable execution dependency.

**context-01:** `/dependencies/35`, bajty [520375,521144), fragment SHA-256 `419d1694acc3d8c6a8ddab7c14e8be998c2fb02dc0d8a28826e9557f779ca2bf`.

Zapis modelu: `R919→N872`, `mention/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Supplied 8.72 identifies Shock Superiority Chart purpose; its actual notes are a separate unavailable execution dependency.

source_evidence: `C-9.19-01` / `/items/48`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.19 Indians vs. Africans: In addition to the notes on the Clash of
> Spears and Swords and Shock Superiority Charts, the following
> rule is in effect when Indian Elephants fight African Elephants:
> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/1/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 8.72 The Shock Superiority Chart: This chart is used to
> compare the superiority (if any) of one type of unit compared
> to another, depending on which side is attacking or defending.
> Always read down the column—from the Attacker’s point of
> view. (Reading across, by row, gives a “false” result.) Superiority
> is used to augment Cohesion Hits.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D919clashdef

Źródło: 9.19: in addition to Clash of Spears and Swords notes

Cel: 8.73: chart selects Shock CRT column subject to adjustments

Potrzeba/konsekwencja braku: Cel opisowy nie daje notes/cells. Znane +1 nie wymaga ich przy zadanych faktach; pełny Shock lookup nadal zablokowany.

Porównanie/propozycja: R919→N873 mention/explicit poprawne jako identyfikacja opisu. Przyjąć ten zakres, nie pełną procedurę D919clash ani aliases innych chart.

**first-001:** `/dependencies/36`, bajty [444892,445605), fragment SHA-256 `f50d58f6e481b1f1c98c1521a007b8f8c64bb80ac911c1f5ce538ac9439ca5ff`.

Zapis modelu: `R919→N873`, `mention/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Supplied 8.73 identifies Clash Chart purpose; does not supply notes/cells needed by 9.19.

**context-01:** `/dependencies/36`, bajty [521151,521886), fragment SHA-256 `0d7cbce850f7cdfa124f62e0bd6679f2ba1d1c66da5d0b6f0970b70f3e013beb`.

Zapis modelu: `R919→N873`, `mention/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Supplied 8.73 identifies Clash Chart purpose; does not supply notes/cells needed by 9.19.

source_evidence: `C-9.19-01` / `/items/48`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.19 Indians vs. Africans: In addition to the notes on the Clash of
> Spears and Swords and Shock Superiority Charts, the following
> rule is in effect when Indian Elephants fight African Elephants:
> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/1/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 8.73 Clash of Spears and Swords Chart: This chart is used
> to determine which Column will be used on the Shock Combat
> Results Table (subject to adjustments).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D922HD

Źródło: 9.22: SK/LI Archers A no H&D; LC all missile classes no H&D vs SK

Cel: H&D concept, absent procedure

Potrzeba/konsekwencja braku: Zakaz jest znany i nie każe wykonywać H&D. Brak definicji może blokować identyfikację konkretnej akcji, nie lokalny zakaz z zadanym typem.

Porównanie/propozycja: R922→candidate mention/explicit uczciwie zostawia cel unresolved. Przyjąć tylko odniesienie/zakaz, bez pełnej procedury i bez automatycznego warunku table/procedure_use.

**first-001:** `/dependencies/64`, bajty [470145,471118), fragment SHA-256 `bc236c79c6247558117c7e7b3203070ba6577a409c1dfef29e11835c040090d5`.

Zapis modelu: `R922→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to H&D fire; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/64`, bajty [547144,548144), fragment SHA-256 `db66ebc64907ecb7d99e1cce0cd8c4d0838a1f5a08129286a7c01001c2931e4b`.

Zapis modelu: `R922→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to H&D fire; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.22-01` / `/items/52`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.22 Missile Fire: There is a +2 DRM to the Missile Fire DR
> whenever a Skirmisher unit is the target. Skirmisher and Light
> Infantry Archers (Class A) cannot use H&D fire. Light Cavalry
> (all missile classes) cannot use H&D against Skirmishers..

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D923ex

Źródło: 9.23: Hits inflicted by SK half/floor cap1

Cel: local 1(4)→0(4) example when LI attacks SK

Potrzeba/konsekwencja braku: Przykład ilustruje operator; nie jest konieczny do min(1,floor(H/2)) przy zadanych H. Bez rzeczywistego CRT nie ustalamy base Hits.

Porównanie/propozycja: R923→N923ex mention/explicit poprawne. N923ex zachowuje 1(4)→0(4); Step4 pozwala oddzielnie potwierdzić stronę attacker. Przyjąć rolę przykładu; nie zastępuje brakującego DEP-034 z example do Table.

**first-001:** `/dependencies/41`, bajty [448354,449025), fragment SHA-256 `fe373ce5c1dae9f9f10c01a814d0f01b880e0fba6ab22c21cca874c8ac604396`.

Zapis modelu: `R923→N923ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Numerical example illustrates defender-inflicted Hit scaling.

**context-01:** `/dependencies/41`, bajty [524728,525421), fragment SHA-256 `c3f4509425df9e1237a94b8c5de3351191f10907e1591ff8abed603b24dac07b`.

Zapis modelu: `R923→N923ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Numerical example illustrates defender-inflicted Hit scaling.

source_evidence: `C-9.23-05` / `/items/58`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.

target_evidence: `X-02` / `/items/164`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: Thus, if a Light Infantry attacking a Skirmisher
> would produce an unadjusted result on the Shock Results Table
> of 1(4), the actual result would be 0(4).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D924911

Źródło: 9.24: SK do not make Elephant Pass-Thru Check

Cel: 9.11 step4 final defender check only

Potrzeba/konsekwencja braku: Wyjątek konieczny, by nie zarządzić końcowego testu SK. Nie znosi wcześniejszych warunków i etapów Pass-Thru ani Pre-Shock innych jednostek.

Porównanie/propozycja: R924→R911 exception/explicit odpowiada DEP-008, mimo szerokich ID rodziców. R911 action/exception jawnie wyłącza SK ze Step4. Przyjąć dokładnie to zawężenie; nie całą 9.11 jako wyjątek.

**first-001:** `/dependencies/3`, bajty [419805,420533), fragment SHA-256 `98d8bc545e4afcec22f063e16bf1da0781d4ad22e424d0879b3a9cf60d4b6186`.

Zapis modelu: `R924→R911`, `exception/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.24 explicitly exempts Skirmishers from the Pass-Thru Check in 9.11; exception points to qualified general procedure.

**context-01:** `/dependencies/3`, bajty [495292,496042), fragment SHA-256 `159af844875c40c8fd1dfb64f903f9230b54b15cb94385a8a601e8c1f0e67802`.

Zapis modelu: `R924→R911`, `exception/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.24 explicitly exempts Skirmishers from the Pass-Thru Check in 9.11; exception points to qualified general procedure.

source_evidence: `C-9.24-03` / `/items/63`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • Skirmishers do not make an Elephant Pass-Thru Check (9.11).

target_evidence: `C-9.11-10` / `/items/20`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 4. The defending unit, other than a Skirmisher unit, now un-
> dergoes a Pass-Thru TQ Check. Subtract the unit’s TQ from
> the DR, with any excess being the number of Cohesion Hits
> now applied (DR–TQ=Hits).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D924ex

Źródło: 9.24: one SK/Velites per interruption does not disrupt line

Cel: three local line examples on PDF34 left

Potrzeba/konsekwencja braku: Przykłady objaśniają powtarzalne pojedyncze przerwy; nie zastępują warunków LC4.32. Brak przykładów nie unieważnia lokalnej reguły.

Porównanie/propozycja: R924→N924ex mention/explicit poprawne. N924ex rozróżnia jedną przerwę, dwie kolejne Velites i dwie rozdzielone przerwy; nie globalnie jednego SK. Przyjąć rolę ilustracji, bez całej legalności line.

**first-001:** `/dependencies/40`, bajty [447680,448348), fragment SHA-256 `db61f4012ae0296b4864959df5056e0fdf0b5abb4a7fce6f92f5598471fabf02`.

Zapis modelu: `R924→N924ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Printed line examples illustrate single interruptions.

**context-01:** `/dependencies/40`, bajty [524031,524721), fragment SHA-256 `fa7bc6ab4eacc77c2257dad52adf78df50b1cef30abd39935b388891d505f93b`.

Zapis modelu: `R924→N924ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Printed line examples illustrate single interruptions.

source_evidence: `C-9.24-05` / `/items/65`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • When determining lines for a Line Command (4.32), the pres-
> ence of a Velites or Skirmisher unit does not disrupt the line if

> the interruption is caused by only one such unit.

target_evidence: `X-03` / `/items/165`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: There are Hastati in 2808, Velites in 2809, and Has-
> tati in 2810. This would still be eligible to be a line. However,
> if there were Velites in 2809 and 2810 and the Hastati in 2808
> and 2811, the two Hastati would not form a line. If there were
> Hastati in 2808, 2810, and 2812, with Velites in 2809 and 2811,
> the Hastati could form a line.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D924rout

Źródło: 9.24: SK Rout replaced by elimination

Cel: 10.14 ordinary Rout threshold

Potrzeba/konsekwencja braku: Próg dostarcza warunek zastępowanego Rout; zastąpienie elimination nie przyznaje normalnego retreat/rally. Zadany trigger lokalnie wystarcza.

Porównanie/propozycja: R924→N1014 condition/implicit poprawne w zwykłym triggerze. Przyjąć próg i kierunek do definicji, wyłączyć pełny Rout i kwalifikacje 10.15.

**first-001:** `/dependencies/29`, bajty [439689,440439), fragment SHA-256 `286024105730d45fea4573dcc5181018af7e7a8199c61d57ca4849524054a981`.

Zapis modelu: `R924→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

**context-01:** `/dependencies/29`, bajty [515788,516560), fragment SHA-256 `b27810db64beb815022252b4f017f3e9639b664cd6f5af76975a28c113950427`.

Zapis modelu: `R924→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

source_evidence: `C-9.24-02` / `/items/62`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • Skirmishers that Rout are eliminated instead.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.14 When a unit has absorbed Cohesion Hits equal to or more
> than its TQ rating, it routs (10.2).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D931922

Źródło: 9.31: missile LC H&D lower-MA except SK

Cel: 9.22: LC any missile class cannot H&D against SK

Potrzeba/konsekwencja braku: Niejawny warunek celu zabezpiecza wyjątek; obie reguły mówią go wprost lokalnie. Realna H&D procedura/ratingi nie są dostarczone.

Porównanie/propozycja: R931→R922 condition/implicit poparte tym samym ograniczeniem celu, nie samą nazwą. Przyjąć tylko zakaz SK i zachowane lower MA, bez zezwolenia na dowolny fire.

**first-001:** `/dependencies/4`, bajty [420539,421333), fragment SHA-256 `ea31ad25ca07ae14e92a6f5d88ea964287d83543af23d0442eaf591dfee0eadf`.

Zapis modelu: `R931→R922`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Both supplied clauses explicitly exclude LC H&D against Skirmishers; 9.31 target permission is qualified by 9.22 prohibition. This is a target condition, not a word-similarity relation.

**context-01:** `/dependencies/4`, bajty [496049,496865), fragment SHA-256 `3ba738210b0e3dcc5e800e672dec3c4ebd576d70effd8557911fb79453dbf4f6`.

Zapis modelu: `R931→R922`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Both supplied clauses explicitly exclude LC H&D against Skirmishers; 9.31 target permission is qualified by 9.22 prohibition. This is a target condition, not a word-similarity relation.

source_evidence: `C-9.31-01` / `/items/67`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.31 Missile-armed Light Cavalry may use H&D fire (8.3) against
> all units with a lower MA, except Skirmishers. Light Cavalry
> Archers can fire when they use Orderly Withdrawal (6.55).

target_evidence: `C-9.22-01` / `/items/52`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.22 Missile Fire: There is a +2 DRM to the Missile Fire DR
> whenever a Skirmisher unit is the target. Skirmisher and Light
> Infantry Archers (Class A) cannot use H&D fire. Light Cavalry
> (all missile classes) cannot use H&D against Skirmishers..

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D932ex

Źródło: 9.32: attacking LC Hits half/floor for PH/HI/MI/LG/BI

Cel: local AS vs HI printed-CRT-result example

Potrzeba/konsekwencja braku: Przykład nie jest procedurą ani dowodem kolejności operatorów. Lokalny operator ze znanymi H działa; realny base i AS applicability wymagają źródeł.

Porównanie/propozycja: R932→N932ex mention/explicit poprawne jako rola przykładu w obu hashach. Po kontekście interpretacja nadal unknown, z wyjątkiem Routed i cumulative opisanymi osobno. Przyjąć tę rolę, bez zamknięcia SEM-003, nowego wyjątku ani AS/LC order.

**first-001:** `/dependencies/38`, bajty [446306,447001), fragment SHA-256 `cc9475d15261fdb557c7ca8ab2c060784e976233b90b37dac2e0fd7de938abe3`.

Zapis modelu: `R932→N932ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Printed example illustrates R932; unresolved interaction retained separately as G932.

**context-01:** `/dependencies/38`, bajty [522611,523328), fragment SHA-256 `7c03e42800abfb08a66dcfbbb19c67b523b78ac909257fd89d9f451da17bb976`.

Zapis modelu: `R932→N932ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Printed example illustrates R932; unresolved interaction retained separately as G932.

source_evidence: `C-9.32-01` / `/items/69`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).

target_evidence: `X-04` / `/items/166`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: A Light Cavalry unit with Attack Superiority (AS)
> against a Heavy Infantry unit would use the printed result on
> the Shock CRT.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D941ex

Źródło: 9.41: qualifying flank-supported frontal moving attack

Cel: 2LG vs PH; column5→1 by4L, no other adjustments

Potrzeba/konsekwencja braku: Ilustracja, nie niezbędny krok. Warunki Front/moving/flank/HI/any-PH-attacker muszą pozostać; realnego CRT brak.

Porównanie/propozycja: R941→N941ex mention/explicit poprawne. N941ex ma assumption no other adjustments i approximate Hits, nie gwarancję. Przyjąć rolę przykładu z wyłączeniem lookupu, ratingów i wszystkich sytuacji.

**first-001:** `/dependencies/39`, bajty [447007,447674), fragment SHA-256 `6ba6fda994dd5796926e41bbe18ac34523543fedbf043b65403eb564e8a835c0`.

Zapis modelu: `R941→N941ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Printed numerical example illustrates two Flank supports.

**context-01:** `/dependencies/39`, bajty [523335,524024), fragment SHA-256 `e15b99b6c60a8120f23af4f498cc4a2be0551a2f8f2f702dfaff145f5b9da587`.

Zapis modelu: `R941→N941ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Printed numerical example illustrates two Flank supports.

source_evidence: `C-9.41-01` / `/items/71`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.41 In any Shock Resolution in which a unit moves adjacent to
> and Shock attacks a Phalanx from the defender’s Front hex, the
> Phalanx earns a 2L shift on the Shock Combat CRT for each of
> its Flank hexes either occupied by another friendly Phalanx unit
> or in the ZOC of a friendly Phalanx unit. If the attacker is Heavy
> Infantry (any Class), the shift is 1L instead. This applies only to
> moving attacks, not to attacks in which the attacking unit started
> adjacent to the Phalanx unit and stayed in that hex to Shock. It
> also does not apply to Flank/Rear attacks, or if any attacker is
> also a Phalanx unit.

target_evidence: `X-05` / `/items/167`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: If 2 LGs attack a PH frontally that has other PH
> units in each Flank hex, the Shock attack is resolved, assuming
> no other adjustments, on the 1 column (they start in 5 and get
> shuffled 4L to 1). This means that, on average per Shock, the PH
> will take 1, maybe 2 Hits; but each LG will take 2 or 3.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D951elig

Źródło: 9.51: eligible PH may form DD

Cel: 9.5 note: scenario-specific rules list eligible units

Potrzeba/konsekwencja braku: Warunek konieczny dla wybrania realnych PH. Dostępna nota mówi gdzie szukać, a nie które PH; bez scenario lista pozostaje blocked. Przy zadanej eligibility lokalna formacja ocenialna.

Porównanie/propozycja: R951→R95note condition/implicit poprawnie zawęża DD. Przyjąć więź do wymagania źródła, bez przeniesienia internal/false na realną dostępność eligibility i bez wykonania D95scenario.

**first-001:** `/dependencies/117`, bajty [521284,521987), fragment SHA-256 `60700a4d5879715f9dcec36b24e496a95ed18db049d3c0ee47dd8d7fdce4d8f4`.

Zapis modelu: `R951→R95note`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.5 note explicitly assigns eligible units to scenarios, qualifying 9.51 DD permission.

**context-01:** `/dependencies/117`, bajty [599972,600697), fragment SHA-256 `bd23e317394e3de58ea4ee03b8daa3282d1e1198144afcdb4734d75df433953c`.

Zapis modelu: `R951→R95note`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.5 note explicitly assigns eligible units to scenarios, qualifying 9.51 DD permission.

source_evidence: `C-9.51-01` / `/items/73`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.51 Phalanxes may use Double-Depth (DD) formation, which al-
> lows them to stack two to a hex. Forming Double-Depth requires
> an Individual Order or Line Command, directly from the OC. To
> form Double-Depth, the stacking, “back” Phalanx must start its
> movement in the hex directly behind the “front” Phalanx. The
> “back” Phalanx then moves into the front Phalanx’s hex, paying
> normal terrain costs, and expends 1 MP in addition to the terrain
> cost to stack. The “back” Phalanx is then placed underneath the
> “front” Phalanx. This completes the movement for both units
> for that Orders Phase.

target_evidence: `N-09-S2` / `/items/198`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Eligible units are listed in the scenario-specific rules.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D952951

Źródło: 9.52: unstack with IO or LC as above

Cel: 9.51: IO/LC directly from OC

Potrzeba/konsekwencja braku: Konieczna jest reguła uprawnionego rozkazu; nie cała procedura forming DD. Brak celowej klauzuli uniemożliwiłby właściwe uprawnienie unstack.

Porównanie/propozycja: R952→R951 procedure_use/explicit poparte as above i osobnym orders-only-OC. Top rusza za normalny koszt, bottom zostaje. Przyjąć użycie wymogu IO/LC direct OC, nie nadawać unstack kosztu +1 z forming DD.

**first-001:** `/dependencies/116`, bajty [520582,521278), fragment SHA-256 `617cb684341d5c9fe8a9c3d874861655a83d6e01803de0caef4cd475b7a57242`.

Zapis modelu: `R952→R951`, `procedure_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.52 unstacking order is “as above”; 9.51 supplies direct-OC order requirement.

**context-01:** `/dependencies/116`, bajty [599247,599965), fragment SHA-256 `1190f25d869ff1f00fb20b9a40e348482b327ae7e5f9249f5519a5c5b81140b9`.

Zapis modelu: `R952→R951`, `procedure_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.52 unstacking order is “as above”; 9.51 supplies direct-OC order requirement.

source_evidence: `C-9.52-04` / `/items/78`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • The units may not Wheel (6.44), Reverse (6.45), or use Col-
> umn (6.7). Unstacking requires an Individual Order or Line
> Command as above, at which time the top unit moves off at
> normal costs. The bottom unit must remain in place.

target_evidence: `C-9.51-01` / `/items/73`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.51 Phalanxes may use Double-Depth (DD) formation, which al-
> lows them to stack two to a hex. Forming Double-Depth requires
> an Individual Order or Line Command, directly from the OC. To
> form Double-Depth, the stacking, “back” Phalanx must start its
> movement in the hex directly behind the “front” Phalanx. The
> “back” Phalanx then moves into the front Phalanx’s hex, paying
> normal terrain costs, and expends 1 MP in addition to the terrain
> cost to stack. The “back” Phalanx is then placed underneath the
> “front” Phalanx. This completes the movement for both units
> for that Orders Phase.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D952column

Źródło: 9.52: DD cannot use Column6.7

Cel: 6.7 Column procedure unavailable

Potrzeba/konsekwencja braku: Znany zakaz, brak potrzeby wykonania zabronionego manewru; identyfikacja szczegółowej akcji wymaga celu.

Porównanie/propozycja: R952→null mention/explicit poparte numerem i nazwą; przyjąć odniesienie zakazu, bez certyfikacji 6.7.

**first-001:** `/dependencies/79`, bajty [484600,485539), fragment SHA-256 `1eb65d06586190484be1c211389f90930759a58093b42967d578d423c7738378`.

Zapis modelu: `R952→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.7; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/79`, bajty [562185,563151), fragment SHA-256 `5d3a3e713878d659db229631ec721947849d75fb5cf83bd85b5606b25342eb26`.

Zapis modelu: `R952→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.7; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.52-04` / `/items/78`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • The units may not Wheel (6.44), Reverse (6.45), or use Col-
> umn (6.7). Unstacking requires an Individual Order or Line
> Command as above, at which time the top unit moves off at
> normal costs. The bottom unit must remain in place.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D952reverse

Źródło: 9.52: DD cannot Reverse6.45

Cel: 6.45 Reverse unavailable

Potrzeba/konsekwencja braku: Brak definicji nie blokuje lokalnego zakazu przy zadanym manewrze Reverse; brak szczegółowej procedury jawny.

Porównanie/propozycja: R952→null mention/explicit poprawne jako zakaz wskazanego manewru. Przyjąć to wystąpienie, bez wykonania Reverse.

**first-001:** `/dependencies/78`, bajty [483648,484594), fragment SHA-256 `db2cbcaccd82484eb7f2c98ba3711ca944c6124e30033d393fdddb7f67ae47de`.

Zapis modelu: `R952→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.45; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/78`, bajty [561205,562178), fragment SHA-256 `4f071999849333484d0048bacfc1ec5a88cdad6fb5591fc345cd4a294a045db8`.

Zapis modelu: `R952→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.45; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.52-04` / `/items/78`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • The units may not Wheel (6.44), Reverse (6.45), or use Col-
> umn (6.7). Unstacking requires an Individual Order or Line
> Command as above, at which time the top unit moves off at
> normal costs. The bottom unit must remain in place.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D952wheel

Źródło: 9.52: DD cannot Wheel6.44

Cel: 6.44 Wheel unavailable

Potrzeba/konsekwencja braku: Zakaz znany; brak celu dotyczy identyfikacji manewru, nie potrzeby wykonania zabronionego Wheel.

Porównanie/propozycja: R952→null mention/explicit poprawne dla tego odniesienia. Przyjąć lokalny zakaz, bez procedury Wheel.

**first-001:** `/dependencies/77`, bajty [482704,483642), fragment SHA-256 `914a0acd44d566f2c56e89fbe9e02bfccf0e4a71a98a6b81b485840d5183acff`.

Zapis modelu: `R952→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.44; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/77`, bajty [560233,561198), fragment SHA-256 `7570e723ace6ef651b28f77f534e780eaee39f83935d890955c8bae8001cf5d0`.

Zapis modelu: `R952→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.44; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.52-04` / `/items/78`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • The units may not Wheel (6.44), Reverse (6.45), or use Col-
> umn (6.7). Unstacking requires an Individual Order or Line
> Command as above, at which time the top unit moves off at
> normal costs. The bottom unit must remain in place.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D953941

Źródło: 9.53: defending DD gets−1 PreShock; Phalanx Defense also applies

Cel: 9.41: moving Front attack; flank support;2L or HI1L; stationary/FlankRear/anyPH attacker excluded

Potrzeba/konsekwencja braku: Użycie konieczne dla oceny shift. −1 PreShock to inny operator. Bez 9.41 nie można przyznać shift bezwarunkowo; sam dostępny cel nie daje realnego CRT/geometry.

Porównanie/propozycja: R953→R941 procedure_use/explicit odpowiada DEP-017. Oba rekordy zachowują osobne −1 oraz warunki i wszystkie wyłączenia 9.41. Przyjąć dokładnie warunkowe wywołanie, nie automatyczne4L.

**first-001:** `/dependencies/2`, bajty [419111,419799), fragment SHA-256 `0ba0d177b17d0de528b2e0c8bfcbd7f5911fe5950abbcad4998651afb7e9763f`.

Zapis modelu: `R953→R941`, `procedure_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.53 explicitly applies Phalanx Defense (9.41); DD combat rule points to used defense rule.

**context-01:** `/dependencies/2`, bajty [494576,495285), fragment SHA-256 `e934272eeb970661350bd1128064181f1fae666a8d3223b54d50b86c2f5f6c9d`.

Zapis modelu: `R953→R941`, `procedure_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.53 explicitly applies Phalanx Defense (9.41); DD combat rule points to used defense rule.

source_evidence: `C-9.53-05` / `/items/86`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • Defending units at Double Depth earn a –1 DRM to their Pre-
> Shock TQ check die rolls. Phalanx Defense (9.41) also applies.

target_evidence: `C-9.41-01` / `/items/71`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.41 In any Shock Resolution in which a unit moves adjacent to
> and Shock attacks a Phalanx from the defender’s Front hex, the
> Phalanx earns a 2L shift on the Shock Combat CRT for each of
> its Flank hexes either occupied by another friendly Phalanx unit
> or in the ZOC of a friendly Phalanx unit. If the attacker is Heavy
> Infantry (any Class), the shift is 1L instead. This applies only to
> moving attacks, not to attacks in which the attacking unit started
> adjacent to the Phalanx unit and stayed in that hex to Shock. It
> also does not apply to Flank/Rear attacks, or if any attacker is
> also a Phalanx unit.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D953elig

Źródło: 9.53: combat effects only for DD formation

Cel: 9.5 scenario eligibility note

Potrzeba/konsekwencja braku: Stos musi rzeczywiście być legalnym DD; nota jest dostępna, lista scenario nie. Zadany legalny DD pozwala na lokalne operatory.

Porównanie/propozycja: R953→R95note condition/implicit poparte zakresem DD i elig note. Przyjąć związek do wymagania eligibility, bez uznania konkretnych jednostek za uprawnione.

**first-001:** `/dependencies/118`, bajty [521993,522691), fragment SHA-256 `3a1b3ac3547de8ff724e3c3ee95e74155f7634b0d9fe3886a132b94a32e1609c`.

Zapis modelu: `R953→R95note`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Scenario eligibility is necessary for being a DD stack; no scenario list supplied.

**context-01:** `/dependencies/118`, bajty [600704,601424), fragment SHA-256 `fc0d702cf89770fc2bed35b3cad0035e451ca56b1f64f79d89c5d85150aad238`.

Zapis modelu: `R953→R95note`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Scenario eligibility is necessary for being a DD stack; no scenario list supplied.

source_evidence: `C-9.53-01` / `/items/82`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.53 Combat Effects: Double Depth formation has the follow-
> ing effects on combat:

target_evidence: `N-09-S2` / `/items/198`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Eligible units are listed in the scenario-specific rules.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D953rout

Źródło: 9.53: either DD PH Rout makes both Rout; separate hexes

Cel: 10.14 ordinary threshold

Potrzeba/konsekwencja braku: Próg może ustalić zdarzenie pierwszej PH; target nie rozstrzyga kto eliminated gdy nie ma osobnego hexu. SEM-002/EXP-040 pozostaje otwarte.

Porównanie/propozycja: R953→N1014 condition/implicit można przyjąć dla zwykłego triggeru, bez uogólnienia wszystkich Rout i bez decyzji o per-unit elimination.

**first-001:** `/dependencies/30`, bajty [440445,441195), fragment SHA-256 `b3ae794987fa0c9ad4c0c73be6389a068dce33d544ff9dfd73aefaff245e2d33`.

Zapis modelu: `R953→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

**context-01:** `/dependencies/30`, bajty [516567,517339), fragment SHA-256 `c9a39397dfa369938e037bc0ecb7684d671141b3809d4fba9a8b1b32099e2ca4`.

Zapis modelu: `R953→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

source_evidence: `C-9.53-08` / `/items/89`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • If either unit in the stack routs, they both rout. The units must
> retreat to separate hexes. If this is not possible, the unit is
> eliminated instead.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.14 When a unit has absorbed Cohesion Hits equal to or more
> than its TQ rating, it routs (10.2).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D953scenario

Źródło: 9.53 example: See scenario rules for Cynoscephalae

Cel: Cynoscephalae example absent, identity beyond supplied name unknown

Potrzeba/konsekwencja braku: Wzmianka informacyjna; brak przykładu nie blokuje znanych lokalnych DD operators. Nie dostarcza listy eligibility.

Porównanie/propozycja: N953ex→null mention/explicit odpowiada DEP-063 w zakresie wystąpienia i roli. Przyjąć tylko skierowanie do przykładu, bez treści scenario i alias/source identity.

**first-001:** `/dependencies/81`, bajty [486504,487494), fragment SHA-256 `cf35bd0512341efb62fe4761b31c3aabfc52616cb8180107a7bbcafa9c409f5f`.

Zapis modelu: `N953ex→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to scenario rules for Cynoscephalae; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/81`, bajty [564145,565162), fragment SHA-256 `44040550635c77c8dcec6e67c4ad87eff1c8dbe3ebb8c5b0c9dde6f7906f0c5d`.

Zapis modelu: `N953ex→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to scenario rules for Cynoscephalae; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `X-06` / `/items/168`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: See the scenario rules for Cynoscephalae.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D9621013

Źródło: 9.62 last sentence: Shock Step4 Hits allocated per10.13

Cel: 10.13 equal division across units/stacks; remainder priorities; two exceptions; within-stack6.68#6 absent

Potrzeba/konsekwencja braku: Użycie konieczne do allocation. Bez6.68#6 pełny wynik stosu zablokowany; nawet dostępne10.13 nie zamyka go. Zadana liczba Hits nie dostarcza reguły within-stack.

Porównanie/propozycja: R962→N1013 procedure_use/explicit ma poprawny cel i kierunek. Jednak blocks_full_result=false i gap_ids=[] nie pokazują zagnieżdżonej blokady; N1013 ją opisuje, G-D1013stack=true istnieje osobno. Proponuję przyjąć endpoint/use tylko, a deklarację blokady przekazać osobno do decyzji SEM-014; nie naprawiać odpowiedzi.

**first-001:** `/dependencies/22`, bajty [433906,434668), fragment SHA-256 `121a149de55cb0de8218605312898793a7aa5310f7886b1f2eec97d652d0ab09`.

Zapis modelu: `R962→N1013`, `procedure_use/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.62 allocates Shock Hits per 10.13; actual target supplied as boundary evidence, with unresolved stack distribution nested reference.

**context-01:** `/dependencies/22`, bajty [509833,510617), fragment SHA-256 `14b44927a2ea4036ef24d4919d0704d52aaea07f38538e9931af69a12b1161a8`.

Zapis modelu: `R962→N1013`, `procedure_use/explicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.62 allocates Shock Hits per 10.13; actual target supplied as boundary evidence, with unresolved stack distribution nested reference.

source_evidence: `C-9.62-01` / `/items/93`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.62 Stacked Roman units combine their Size when attacking or
> defending, but all other ratings, especially TQ, are those of the
> top unit. Stacked Romans must Shock attack the same hex; see
> 8.42. Only the top unit may fire. Each unit makes its own TQ
> check but uses the TQ of the top unit. Automatic Cohesion Hits
> (6.68) are applied to each unit in the stack. Cohesion Hits from
> Shock resolution 8.46 Step 4 are allocated per 10.13.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.13 If there are multiple units involved in a single combat
> resolution, Cohesion Hits must be divided as equally as possible
> amongst these units (treat a stack as a single unit for this purpose),
> with any extra Hits being given to the unit/stack:
> • used to gain Superiority (either type), otherwise
> • used to determine the Shock Column on the Clash of Spears
> and Swords Chart.
> Owning player’s choice if more than one unit/stack qualifies in
> either category. Hits allocated to a stack are distributed per 6.68
> bullet #6.
> Exceptions:
> • If a leader on a Leader Elephant is stacked with a combat unit,
> that player does not have to apportion any Hits to the Leader
> Elephant, unless the number of Hits exceeds the other combat
> unit’s TQ. In that case, all excess Hits apply to the Leader
> Elephant.
> • If a Phalanx unit is attacking two or more non-Phalanx units,
> the attacking player chooses how any Cohesion Hits will be
> distributed amongst the defenders. Such distribution may be
> uneven, if so desired. This does not apply when Phalanx units
> are defending.
> EXAMPLE: A Hastati stack and another Hastati unit receive 1
> Hit from their attack. The Hit cannot be divided equally so it is
> excess. There was no superiority and all units have the same Type
> which was used to determine the Shock column on the Clash of
> Spears and Swords chart. The attacking player gets to choose
> whether to give the Hit to the stack or the lone Hastati. If he
> chooses the stack, the top Hastati will incur the Hit.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D962shock

Źródło: 9.62: Shock resolution8.46 Step4 before allocation

Cel: first: absent Step4; context: only supplied Step4 crop PDF27

Potrzeba/konsekwencja braku: Procedure necessary for applying Shock Hits. First has absent source; context supplies operators/notation but no CRT/8.45/order/within-stack result. Both full results blocked.

Porównanie/propozycja: Jawne R962→candidate w first i R962→NCTX846S4 w context poprawnie odpowiadają źródłu; zmiana endpointu to częściowe podparcie, nie domknięcie allocation. Przyjąć oba dokładne stany/pozostałe blokady, bez nowego lookupu.

**first-001:** `/dependencies/86`, bajty [491159,492109), fragment SHA-256 `3c908d4ef58625aa4246c0c74394c38d248d7395d859cbe232853e1f16fd6e84`.

Zapis modelu: `R962→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Uzasadnienie modelu (osobno od oceny): Source refers to 8.46 Step 4; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

**context-01:** `/dependencies/86`, bajty [568940,569960), fragment SHA-256 `4b5a3bf62cbe0d3cc8ae154e79c9b1c2a395320a952179da661102ad74d23c25`.

Zapis modelu: `R962→NCTX846S4`, `procedure_use/explicit`, `external_with_source`, blocks_full_result=`True`.

Uzasadnienie modelu (osobno od oceny): 9.62 explicitly uses 8.46 Step 4. Direction R962 to supplied complete fragment. This confirms application text, not actual Shock CRT result.

source_evidence: `C-9.62-01` / `/items/93`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.62 Stacked Roman units combine their Size when attacking or
> defending, but all other ratings, especially TQ, are those of the
> top unit. Stacked Romans must Shock attack the same hex; see
> 8.42. Only the top unit may fire. Each unit makes its own TQ
> check but uses the TQ of the top unit. Automatic Cohesion Hits
> (6.68) are applied to each unit in the stack. Cohesion Hits from
> Shock resolution 8.46 Step 4 are allocated per 10.13.

Dostarczone źródło: `private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-helper.txt`, pointer `whole bounded helper`, hash `5bb9c43565dba73617ddf0234f46401d197ee3be8d12a8a1c3f18b33610a330a`.

> Step 4: Apply Results: Results on the Shock CRT are Cohesion
> Hits for both attacker and defender. The # in parentheses is for
> the defender. The resultant Hits are modified as follows:
> • If the attacker was superior (AS), then double (2x) the de-
> fender’s result.
> • If the defender was superior (DS), then triple (3x) the attacker’s
> result.
> • If the defender is a Skirmisher, halve (½x, round down) the
> attacker’s Hits with a maximum result of 1 Hit.
> • If the attacker used in the determination is Light Cavalry (8.45)
> and the defender is a Phalanx or a Heavy, Medium, Legion, or
> Barbarian Infantry unit, halve (½x, round down) the defender’s
> Hits. This reduction does not apply if the defender is Routed
> and is cumulative with bullet #1.
> If more than one unit of the same player was involved in that
> combat, Cohesion Hits are distributed as per 10.13.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D966diag

Źródło: 9.66 continuation: see diagram above for sideways unstack

Cel: local Original Deployment→After MLE diagram PDF35

Potrzeba/konsekwencja braku: Ilustracja kierunku i facing, nie kolejny algorytm. Brak grafiki nie blokuje znanej tekstowej operacji; realne4.32/ZOC/terrain pozostają źródłowo zależne.

Porównanie/propozycja: R966→N966diagram mention/explicit odpowiada DEP-044 occurrence. Obraz pokazuje top units w flank i zachowanie facing. Przyjąć rolę ilustracji, bez ratingów/glyphs i bez rozszerzenia na restacking.

**first-001:** `/dependencies/9`, bajty [424273,424996), fragment SHA-256 `0ec648dcfb0ced480050c19fd2ab9814f16763f1d18bdeaefc314c6ed8812e89`.

Zapis modelu: `R966→N966diagram`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.66 refers to diagram above; illustration supports destination/facing, not an additional procedure.

**context-01:** `/dependencies/9`, bajty [499900,500645), fragment SHA-256 `4d2091d83a80df1d2c77936d10d51debd3a3254794dffd607ddbac91731f707e`.

Zapis modelu: `R966→N966diagram`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.66 refers to diagram above; illustration supports destination/facing, not an additional procedure.

source_evidence: `C-9.66-01` / `/items/101`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

target_evidence: `D-02` / `/items/175`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

target_evidence: `CAP-01` / `/items/176`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Original Deployment

target_evidence: `CAP-02` / `/items/177`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> After Manipular Line Extension

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D967966

Źródło: 9.67: MLE reaction when enemy combat unit within2hexes, choice at later approaches; different units for OW+MLE

Cel: 9.66: all tops in line move sideways to vacant Clear flank outside enemyZOC, facing unchanged, unstack only

Potrzeba/konsekwencja braku: Operacja konieczna do wykorzystania reaction permission. Timing nie uchyla target geometry/line conditions. Brak operation uniemożliwi jej wykonanie, przy supplied state lokalna ocenialność.

Porównanie/propozycja: R967→R966 procedure_use i kierunek poparte tekstem. Explicitness=implicit wymaga decyzji: pełna nazwa MLE jest wprost użyta, a numer9.66 nie; typowanie named use jako implicit nie jest oczywiste. Proponuję zachować jako kandydat różnicy etykiety SEM-016, bez pewnego FP.

**first-001:** `/dependencies/7`, bajty [422797,423544), fragment SHA-256 `08bf36ff38833cf82c7bd7eadc11261d3f61bce013b7896f4204db78a86df772`.

Zapis modelu: `R967→R966`, `procedure_use/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.67 reaction timing uses the MLE operation defined in 9.66; operation is necessary to perform the timed permission.

**context-01:** `/dependencies/7`, bajty [498376,499146), fragment SHA-256 `8be3881894388d836aa88a4ef06b3b430afb8f5eedb87af271542402867dcb74`.

Zapis modelu: `R967→R966`, `procedure_use/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.67 reaction timing uses the MLE operation defined in 9.66; operation is necessary to perform the timed permission.

source_evidence: `C-9.67-01` / `/items/103`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.67 Manipular Line Extension may be undertaken as a reaction
> to enemy movement the instant an enemy combat unit comes
> within 2 hexes of a line of stacked Roman units. The Roman
> player may make his choice at any time any enemy unit so places
> itself (that is, he does not have to exercise his MLE rights the first
> time they become available). If enemy movement triggers both
> Orderly Withdrawal as well as MLE, both may be undertaken
> together but not by the same units.

target_evidence: `C-9.66-01` / `/items/101`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D967ex

Źródło: 9.67: OW and MLE together but not same units

Cel: Velites withdraw through gap then Hastati line MLE example

Potrzeba/konsekwencja braku: Przykład wyjaśnia rozdzielenie wykonawców i lokalną kolejność; nie zastępuje OW procedure. Brak example nie blokuje znanego zakazu same units.

Porównanie/propozycja: R967→N967ex mention/explicit poprawne; N967ex zachowuje różne jednostki. Przyjąć rolę przykładu, bez warunków pełnej OW trasy.

**first-001:** `/dependencies/42`, bajty [449031,449701), fragment SHA-256 `e83c1ce95717a119e50e62d570341a8872f9a9a4fecba46eb6a2f3533250a3d3`.

Zapis modelu: `R967→N967ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Example illustrates concurrent OW and MLE by distinct units.

**context-01:** `/dependencies/42`, bajty [525428,526120), fragment SHA-256 `ea71d1be99acc6953d463080c04f677cafbe49a030e96693789d4eedf8a1f19b`.

Zapis modelu: `R967→N967ex`, `mention/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Example illustrates concurrent OW and MLE by distinct units.

source_evidence: `C-9.67-01` / `/items/103`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.67 Manipular Line Extension may be undertaken as a reaction
> to enemy movement the instant an enemy combat unit comes
> within 2 hexes of a line of stacked Roman units. The Roman
> player may make his choice at any time any enemy unit so places
> itself (that is, he does not have to exercise his MLE rights the first
> time they become available). If enemy movement triggers both
> Orderly Withdrawal as well as MLE, both may be undertaken
> together but not by the same units.

target_evidence: `X-07` / `/items/169`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: A Velites unit sitting between two Hastati stacks may
> withdraw through the gaps in a Hastati line upon approach of,
> say, an enemy Phalanx and, as soon as that unit is through the
> gap, the Hastati line may undergo MLE.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D968966

Źródło: 9.68: LC-only variant, both may move afterward MA−2; no MLE Hits; no Column

Cel: 9.66 base MLE operation

Potrzeba/konsekwencja braku: Modyfikacja potrzebna przy LC variant; bazowe warunki Clear/flank/ZOC i unstack-only nadal obowiązują. Bez base nie da się wykonać MLE; −2 przy zadanym MA lokalnie znane.

Porównanie/propozycja: R968→R966 modification/implicit poparte kwalifikacją tej samej MLE operation; tekst nie odwołuje numerem. Przyjąć niejawną relację modyfikacji, bez podmiany reaction9.67 i bez ogólnego −2 przy każdym MLE.

**first-001:** `/dependencies/8`, bajty [423550,424267), fragment SHA-256 `06657a4bd26a66518e4f7c571ef773d79a28f0341e145efc12869227d09570f2`.

Zapis modelu: `R968→R966`, `modification/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.68 qualifies LC performance of MLE with post-extension MA reduction and restrictions.

**context-01:** `/dependencies/8`, bajty [499153,499893), fragment SHA-256 `1a7416c7db32c35c8093f2319df89a5d2233456239b7f057744bf64eada73e1e`.

Zapis modelu: `R968→R966`, `modification/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.68 qualifies LC performance of MLE with post-extension MA reduction and restrictions.

source_evidence: `C-9.68-01` / `/items/105`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.68 Manipular Line Extension may also be undertaken as part
> of a Line Command (only). If undertaken as an LC, both units
> may move after the MLE but with their MA reduced by 2. There
> are no Cohesion Hits applied for the MLE. Units in Column may
> not use MLE.

target_evidence: `C-9.66-01` / `/items/101`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D968column

Źródło: 9.68: Units in Column may not use MLE

Cel: Column status/formation definition absent

Potrzeba/konsekwencja braku: Stwierdzenie in Column jest warunkiem niedopuszczalności MLE, nie instrukcją wykonania Column. Brak definicji może blokować identyfikację statusu realnej jednostki; zadany status pozwala na lokalny zakaz.

Porównanie/propozycja: R968→candidate ma jawne odniesienie i poprawny kierunek, lecz mention vs condition wymaga decyzji SEM-016. Nie akceptować całej klasy zakazów automatycznie; propozycja dotyczy statusu in Column, nie cannot use Column z9.52.

**first-001:** `/dependencies/92`, bajty [496976,497900), fragment SHA-256 `9df97bd060d2c444d88bb601df07f217462c5ae40506ceac419c6c1d27f6bc3c`.

Zapis modelu: `R968→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to Column; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/92`, bajty [574969,575920), fragment SHA-256 `92f5d322e1be564f302b8c06636de1b95f10e1964792a9ef678ff277ccc925ce`.

Zapis modelu: `R968→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to Column; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.68-01` / `/items/105`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.68 Manipular Line Extension may also be undertaken as part
> of a Line Command (only). If undertaken as an LC, both units
> may move after the MLE but with their MA reduced by 2. There
> are no Cohesion Hits applied for the MLE. Units in Column may
> not use MLE.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D971app

Źródło: 9.71 movement gate with two OR alternatives

Cel: 9.7 mandatory before200BCE, Romans, Scipio not OC; Cannae deemed applicable

Potrzeba/konsekwencja braku: Warunek stosowalności potrzebny, by stosować doctrine. Known predicate nie oznacza znanej realnej daty/OC; EXP-050/SEM-010 source requirement pozostaje otwarte.

Porównanie/propozycja: R971→R97intro condition/implicit poprawnie wiąże lokalną bramkę z intro, zachowuje OR, enemy nonEL<=3 AND LOS any lub>=6 od all Roman/Ala not allied. Przyjąć tylko stosowalność według zadanych faktów, bez actual battle certificate.

**first-001:** `/dependencies/5`, bajty [421339,422083), fragment SHA-256 `3c6028ef639cdccc8b0e20a5eacb9b45131d24b4ba6e844870a054e5a15fba57`.

Zapis modelu: `R971→R97intro`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.7 introduction sets mandatory applicability of the following Triarii movement clause; rule points to applicability condition.

**context-01:** `/dependencies/5`, bajty [496872,497638), fragment SHA-256 `9cf10aa98261524d06e4d3097b4c0a28d054501199461fdb51cb526e5b6d3482`.

Zapis modelu: `R971→R97intro`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.7 introduction sets mandatory applicability of the following Triarii movement clause; rule points to applicability condition.

source_evidence: `C-9.71-01` / `/items/107`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.71 Triarii units cannot move, but may change facing, until and
> unless one of the following occurs:

source_evidence: `C-9.71-02` / `/items/108`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • There is an enemy combat unit, other than an Elephant unit,
> which is within 3 hexes and LOS of any unit in the Triarii line,
> or

source_evidence: `C-9.71-03` / `/items/109`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • The Triarii units are at least 6 hexes from all other Roman or
> Ala—but not allied–infantry lines, be they Hastati, Principes
> or whatever.

target_evidence: `C-9.7-01-S1` / `/items/205`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> This rule must be used with any battle involving Romans that took
> place prior to 200 BCE in which Scipio Africanus is not pres-
> ent as Overall Commander (and, yes, even though, historically,
> Scipio was at Cannae, for game purposes he wasn’t, so use it at
> Cannae).

target_evidence: `C-9.7-01-S2` / `/items/206`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> It represents the way Romans used their Triarii, and,
> for Rome, doctrine was the equivalent of unassailable dogma.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D972app

Źródło: 9.72 RP>=floor(AWL/2) for move+Shock; stationary Shock ownZOC exception

Cel: 9.7 applicability predicate and Cannae qualification

Potrzeba/konsekwencja braku: Potrzebna stosowalność; nie zastępuje bramki9.71 ani RP/AWL źródeł. Brak daty/OC nie blokuje predykatu z zadanymi faktami, ale blokuje realny dobór rule.

Porównanie/propozycja: R972→R97intro condition/implicit poparte układem doctrine. Przyjąć tylko applicability link i zachowany stationary exception; DEP-NEW-001/EXP-052/SEM-011 oraz SEM-010 pozostają otwarte.

**first-001:** `/dependencies/6`, bajty [422089,422791), fragment SHA-256 `7c728d2f62a80319a01f2921e3e3c9d98c27eb83a7bc26be062cfb1e8e5e68de`.

Zapis modelu: `R972→R97intro`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.7 introduction sets mandatory applicability of the following Triarii attack clause.

**context-01:** `/dependencies/6`, bajty [497645,498369), fragment SHA-256 `26791157a18ec82e4439e5607a1af2bc8c04df50d712c13404fcabe8cc55876f`.

Zapis modelu: `R972→R97intro`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.7 introduction sets mandatory applicability of the following Triarii attack clause.

source_evidence: `C-9.72-01` / `/items/111`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

target_evidence: `C-9.7-01-S1` / `/items/205`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> This rule must be used with any battle involving Romans that took
> place prior to 200 BCE in which Scipio Africanus is not pres-
> ent as Overall Commander (and, yes, even though, historically,
> Scipio was at Cannae, for game purposes he wasn’t, so use it at
> Cannae).

target_evidence: `C-9.7-01-S2` / `/items/206`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> It represents the way Romans used their Triarii, and,
> for Rome, doctrine was the equivalent of unassailable dogma.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D982985

Źródło: 9.82: no orders needed to fire, see9.85

Cel: 9.85 max2 active shots/GameTurn, max1/friendlyOrdersPhase, active segment, no other action phase

Potrzeba/konsekwencja braku: Wywołanie schedule konieczne; Fire mode i no-fire switch phase z9.82 obowiązują dalej. Brak9.85 uniemożliwi prawidłowy limit, realnego missile lookup nie dostarcza.

Porównanie/propozycja: R982→R985 procedure_use/explicit odpowiada DEP-024. R982 zachowuje tryb/switch, R985 warunki i dwa limity z różnymi jednostkami czasu. Przyjąć ten zakres, bez orderfree move/fire-in-switch-phase.

**first-001:** `/dependencies/10`, bajty [425002,425652), fragment SHA-256 `9e35a08cf2649c5a1cf1fa4be902e5fa43bb5f9ace3b866eaaabc58c0709a63d`.

Zapis modelu: `R982→R985`, `procedure_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.82 explicitly refers to 9.85 for order-free firing.

**context-01:** `/dependencies/10`, bajty [500652,501323), fragment SHA-256 `84b209de2e085e85075a240c5b17f7a6f16e52817cad197c310691b9eaba8b61`.

Zapis modelu: `R982→R985`, `procedure_use/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.82 explicitly refers to 9.85 for order-free firing.

source_evidence: `C-9.82-01` / `/items/115`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.82 A Scorpio is in either Fire or Move mode. It requires an
> Individual Order from any friendly leader to change its mode.
> Scorpios in Move mode cannot fire, and conversely, cannot
> move in Fire mode. A Scorpio that has had its mode changed to
> Move cannot move in that Orders Phase, nor can a Scorpio that
> has had its mode switched to Fire, fire in that Orders Phase. A
> Scorpio unit in Move mode requires an Individual Order from
> any friendly leader to move. Scorpio units do not need orders to
> fire (see 9.85 below).

target_evidence: `C-9.85-01` / `/items/121`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.85 Active Fire: Scorpios may fire of-
> fensively twice per Game Turn (not Orders
> Phase) during any friendly Orders Phase.
> They do not need an order to fire and can
> fire at any time during the active player’s Movement and Missile
> Fire Segment, no more than one shot per Orders Phase. The first
> time a Scorpio unit fires, place an ACTIVE FIRE ONCE mark-
> er on it. The second time it fires, flip the marker to its ACTIVE
> FIRE FINISHED side. A Scorpio that fires cannot do anything
> else that Orders Phase (such as recover Hits).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D985982

Źródło: 9.85 permission Active Fire

Cel: 9.82 Fire vs Move and no fire in phase switched to Fire

Potrzeba/konsekwencja braku: Niejawne warunki konieczne, by no-order fire nie zniosło mode/switch restriction. Cel dostępny; hipotetyczny brak uniemożliwiłby legalność trybu, nie rating fire.

Porównanie/propozycja: R985→R982 condition/implicit poprawnie kieruje od specjalnego fire do warunków ogólnych. Przyjąć warunki, bez dublowania punktu DEP-024 i bez pełnego rezultatu strzału.

**first-001:** `/dependencies/11`, bajty [425658,426387), fragment SHA-256 `3f9a719fa03738e50c4c97a59a7675d0e68a0778471c76a07efb56984c9a443d`.

Zapis modelu: `R985→R982`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.82 forbids firing in Move and immediately after switching to Fire; these are necessary mode conditions on Active Fire.

**context-01:** `/dependencies/11`, bajty [501330,502081), fragment SHA-256 `889055560bc2cbfe1d37813ea6376691673170255c940d7649a3160abbe87388`.

Zapis modelu: `R985→R982`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.82 forbids firing in Move and immediately after switching to Fire; these are necessary mode conditions on Active Fire.

source_evidence: `C-9.85-01` / `/items/121`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.85 Active Fire: Scorpios may fire of-
> fensively twice per Game Turn (not Orders
> Phase) during any friendly Orders Phase.
> They do not need an order to fire and can
> fire at any time during the active player’s Movement and Missile
> Fire Segment, no more than one shot per Orders Phase. The first
> time a Scorpio unit fires, place an ACTIVE FIRE ONCE mark-
> er on it. The second time it fires, flip the marker to its ACTIVE
> FIRE FINISHED side. A Scorpio that fires cannot do anything
> else that Orders Phase (such as recover Hits).

target_evidence: `C-9.82-01` / `/items/115`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.82 A Scorpio is in either Fire or Move mode. It requires an
> Individual Order from any friendly leader to change its mode.
> Scorpios in Move mode cannot fire, and conversely, cannot
> move in Fire mode. A Scorpio that has had its mode changed to
> Move cannot move in that Orders Phase, nor can a Scorpio that
> has had its mode switched to Fire, fire in that Orders Phase. A
> Scorpio unit in Move mode requires an Individual Order from
> any friendly leader to move. Scorpio units do not need orders to
> fire (see 9.85 below).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D985markers

Źródło: 9.85 first/second active shot marker progression

Cel: local Active Fire Once and Finished faces PDF36

Potrzeba/konsekwencja braku: Stany pomagają ewidencji dwóch shots, tekst sam je definiuje; brak artwork nie blokuje znanej progresji. Brak actual shot history blokuje realny remaining count.

Porównanie/propozycja: R985→N985markers definition/explicit poprawnie wiąże pokazane dwa stany z tekstem. Przyjąć tylko bookkeeping states, nie dodatkowy shot limit, grafikę ratingów ani cały marker system.

**first-001:** `/dependencies/43`, bajty [449707,450402), fragment SHA-256 `fb900a1f81f504ad2c420cde5b11784ac3de03ed75d91fb056019789a5b737cf`.

Zapis modelu: `R985→N985markers`, `definition/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rule uses pictured active-fire marker faces for status bookkeeping.

**context-01:** `/dependencies/43`, bajty [526127,526844), fragment SHA-256 `9f0a194d3e8d73430e15c8f8532d293d6ca70cc0ee4320928aeb88f2149fec52`.

Zapis modelu: `R985→N985markers`, `definition/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rule uses pictured active-fire marker faces for status bookkeeping.

source_evidence: `C-9.85-01` / `/items/121`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.85 Active Fire: Scorpios may fire of-
> fensively twice per Game Turn (not Orders
> Phase) during any friendly Orders Phase.
> They do not need an order to fire and can
> fire at any time during the active player’s Movement and Missile
> Fire Segment, no more than one shot per Orders Phase. The first
> time a Scorpio unit fires, place an ACTIVE FIRE ONCE mark-
> er on it. The second time it fires, flip the marker to its ACTIVE
> FIRE FINISHED side. A Scorpio that fires cannot do anything
> else that Orders Phase (such as recover Hits).

target_evidence: `G-04` / `/items/181`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D986982

Źródło: 9.86 special Scorpio Reaction Fire, twice/enemyOrdersPhase

Cel: 9.82 general Fire-mode and switch-phase restrictions

Potrzeba/konsekwencja braku: Ogólny warunek trybu potrzebny również dla special fire; brak mode state uniemożliwi realną autoryzację. Any movement nie uchyla Rampage no-Reaction-Fire.

Porównanie/propozycja: R986→R982 condition/implicit poprawna więź; R986.conditions podaje Fire under9.82. Przyjąć ten warunek, bez uznania że zastępuje brakujący DEP-NEW-003.

**first-001:** `/dependencies/12`, bajty [426393,427078), fragment SHA-256 `44c5e3c7ab4c7e866242786eb751e5fafa52a08745ae90ed59883644e695a515`.

Zapis modelu: `R986→R982`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.82 general Fire-mode requirement qualifies Scorpio firing, including 9.86.

**context-01:** `/dependencies/12`, bajty [502088,502795), fragment SHA-256 `ee659f095af3fba6c530b3b69e039ccd29363e417f452b74ebb77b119408dcb2`.

Zapis modelu: `R986→R982`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): 9.82 general Fire-mode requirement qualifies Scorpio firing, including 9.86.

source_evidence: `C-9.86-01` / `/items/123`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.86 Reaction Fire: Scorpios may fire twice per enemy Orders
> Phase at any time during the enemy Movement and Missile Seg-
> ment—and we mean “any”; they may fire even during enemy
> movement! The first time the Scorpio unit fires, place
> a REACTION FIRE ONCE marker on it. The second
> time it fires, flip the marker to its REACTION FIRE
> FINISHED side. Scorpios, however, cannot use any
> type of ordinary Reaction Fire (8.2).

target_evidence: `C-9.82-01` / `/items/115`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.82 A Scorpio is in either Fire or Move mode. It requires an
> Individual Order from any friendly leader to change its mode.
> Scorpios in Move mode cannot fire, and conversely, cannot
> move in Fire mode. A Scorpio that has had its mode changed to
> Move cannot move in that Orders Phase, nor can a Scorpio that
> has had its mode switched to Fire, fire in that Orders Phase. A
> Scorpio unit in Move mode requires an Individual Order from
> any friendly leader to move. Scorpio units do not need orders to
> fire (see 9.85 below).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D986marker

Źródło: 9.86 first shot Once, second flip Finished

Cel: local Reaction Fire Once artwork; Finished specified in prose only

Potrzeba/konsekwencja braku: Stan licznika potrzebny do limitu przy zadanej historii; sama grafika niewymagana. Brak artwork Finished nie znaczy brak tekstowego stanu.

Porównanie/propozycja: R986→N986marker definition/explicit poprawne w opisanym zakresie; node uczciwie odróżnia pictured Once i prose Finished. Przyjąć tę więź stanów, bez poświadczania niepokazanego artwork.

**first-001:** `/dependencies/44`, bajty [450408,451112), fragment SHA-256 `535037eb3d53321c9dfe800a22644bc7ac453ea6e3675159736908999698a61f`.

Zapis modelu: `R986→N986marker`, `definition/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rule uses pictured reaction-fire Once marker; Finished face described in prose.

**context-01:** `/dependencies/44`, bajty [526851,527577), fragment SHA-256 `09f656bda8e6e7133a82b950e209e1fcf2b8a381f8029465f6c7dc95d709a669`.

Zapis modelu: `R986→N986marker`, `definition/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rule uses pictured reaction-fire Once marker; Finished face described in prose.

source_evidence: `C-9.86-01` / `/items/123`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.86 Reaction Fire: Scorpios may fire twice per enemy Orders
> Phase at any time during the enemy Movement and Missile Seg-
> ment—and we mean “any”; they may fire even during enemy
> movement! The first time the Scorpio unit fires, place
> a REACTION FIRE ONCE marker on it. The second
> time it fires, flip the marker to its REACTION FIRE
> FINISHED side. Scorpios, however, cannot use any
> type of ordinary Reaction Fire (8.2).

target_evidence: `G-05` / `/items/182`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D986react

Źródło: 9.86 Scorpio cannot use ordinary Reaction Fire8.2

Cel: 8.2 ordinary types absent

Potrzeba/konsekwencja braku: Zakaz ordinary znany, special permission pozostaje. Brak celu nie blokuje lokalnego zakazu, może blokować rozpoznanie konkretnego typu fire.

Porównanie/propozycja: R986→candidate mention/explicit poprawnie zachowuje zakaz z numerem. Przyjąć role occurrence, bez general Reaction Fire procedure i bez uchylenia Rampage zakazu.

**first-001:** `/dependencies/97`, bajty [501776,502737), fragment SHA-256 `c5654f08ee0cca6a5dc37ab6962713027d53595236e9b4a7e8729f7098934250`.

Zapis modelu: `R986→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 8.2; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/97`, bajty [579909,580897), fragment SHA-256 `033f04fcf1e10ae03f70c943017789e0c2c5e79b1272e2a30c6fba80cd3adb55`.

Zapis modelu: `R986→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 8.2; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.86-01` / `/items/123`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.86 Reaction Fire: Scorpios may fire twice per enemy Orders
> Phase at any time during the enemy Movement and Missile Seg-
> ment—and we mean “any”; they may fire even during enemy
> movement! The first time the Scorpio unit fires, place
> a REACTION FIRE ONCE marker on it. The second
> time it fires, flip the marker to its REACTION FIRE
> FINISHED side. Scorpios, however, cannot use any
> type of ordinary Reaction Fire (8.2).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D987rout

Źródło: 9.87 Scorpio Rout immediately eliminates

Cel: 10.14 ordinary Hits>=TQ trigger

Potrzeba/konsekwencja braku: Próg potrzebny gdy Rout jeszcze ustalamy; lokalny skutek zadanej Rout nie wymaga całego10.2. Pełne exceptions/state nie zamknięte.

Porównanie/propozycja: R987→N1014 condition/implicit poparte potrzebą triggeru. Przyjąć tylko zwykły próg, bez auto-relacji do Recovery ani traktowania10.14 jako wszystkich przypadków Rout.

**first-001:** `/dependencies/31`, bajty [441201,441951), fragment SHA-256 `a2aadc1332c980815eb5e2a018f7cb783e4e89f10c81491aa87b15089dcab834`.

Zapis modelu: `R987→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

**context-01:** `/dependencies/31`, bajty [517346,518118), fragment SHA-256 `94956e37ae22e748413f26a3f16cb00f5f33ae16795195e0cf8393a84c13e7e0`.

Zapis modelu: `R987→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

source_evidence: `C-9.87-01` / `/items/125`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.87 Scorpios incur and recover Cohesion Hits as any other unit.
> A Scorpio that routs is immediately eliminated.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.14 When a unit has absorbed Cohesion Hits equal to or more
> than its TQ rating, it routs (10.2).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D991OW

Źródło: 9.91 continuation: BI cannot OW6.5

Cel: 6.5 OW absent

Potrzeba/konsekwencja braku: Zakaz bez wykonania OW; znane lokalne forbidden action nie blokowane samym brakiem procedury.

Porównanie/propozycja: R991→candidate mention/explicit poprawna referencja i kierunek. Przyjąć wyłącznie zakaz OW, bez przyznania alternatywnej trasy/ruchu.

**first-001:** `/dependencies/101`, bajty [505630,506511), fragment SHA-256 `86d3bd60448ef5e6663b5ef43d8e3ca6bf0b2889f8fb20acc2abccc3d8666994`.

Zapis modelu: `R991→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.5; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/101`, bajty [583875,584783), fragment SHA-256 `61f74891a1cb5d59639126772de6de1fc66ef61561eb31e2a1dedaf3f97e2d52`.

Zapis modelu: `R991→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.5; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.91-02` / `/items/128`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Barbarian Infantry (BI) units do not incur Cohesion Hits for
> crossing or entering any type of passable terrain, nor do they
> incur Cohesion Hits for changing facing in Rough terrain. BI units

> cannot use Column Movement (6.7), Pre-Arranged Withdrawal
> (6.8), or Orderly Withdrawal (6.5).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D991PAW

Źródło: 9.91 continuation: BI cannot PAW6.8

Cel: 6.8 PAW absent

Potrzeba/konsekwencja braku: Brak PAW definition może utrudnić klasyfikację akcji, lecz nie odczyt zakazu.

Porównanie/propozycja: R991→candidate mention/explicit poprawne jako prohibition reference. Przyjąć occurrence, bez PAW execution.

**first-001:** `/dependencies/100`, bajty [504699,505624), fragment SHA-256 `be3f4fc13c0c76728e805352a60876ab0fbe09275603625b55918d4fd25fe536`.

Zapis modelu: `R991→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.8; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/100`, bajty [582916,583868), fragment SHA-256 `54e34c06ccb9dcfea11ac6aa626f0463220b1552ff04522247f42b12f14d3054`.

Zapis modelu: `R991→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.8; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.91-02` / `/items/128`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Barbarian Infantry (BI) units do not incur Cohesion Hits for
> crossing or entering any type of passable terrain, nor do they
> incur Cohesion Hits for changing facing in Rough terrain. BI units

> cannot use Column Movement (6.7), Pre-Arranged Withdrawal
> (6.8), or Orderly Withdrawal (6.5).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D991column

Źródło: 9.91 continuation: BI cannot ColumnMovement6.7

Cel: 6.7 Column Movement absent

Potrzeba/konsekwencja braku: Brak procedury nie blokuje lokalnego zakazu przy zadanej nazwie manewru; nie określa szczegółowej formacji.

Porównanie/propozycja: R991→candidate mention/explicit poprawne dla zakazanego manewru. Przyjąć occurrence, bez rozszerzenia na wszystkie ruchy BI.

**first-001:** `/dependencies/99`, bajty [503778,504693), fragment SHA-256 `f4ee226a2f696464f91209cdaa16f77306a6ef4f3d2e15bad383d016695bb8e4`.

Zapis modelu: `R991→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.7; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

**context-01:** `/dependencies/99`, bajty [581967,582909), fragment SHA-256 `65c2d39418618fb471e697ff10d4a432f1ac75b39ce3182f2c7c06b0666e165a`.

Zapis modelu: `R991→candidate`, `mention/explicit`, `unresolved`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Source refers to 6.7; direction is referring clause to the unavailable target. This is a mention/prohibition reference, not an instruction to execute that procedure.

source_evidence: `C-9.91-02` / `/items/128`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Barbarian Infantry (BI) units do not incur Cohesion Hits for
> crossing or entering any type of passable terrain, nor do they
> incur Cohesion Hits for changing facing in Rough terrain. BI units

> cannot use Column Movement (6.7), Pre-Arranged Withdrawal
> (6.8), or Orderly Withdrawal (6.5).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D993rout

Źródło: 9.93: Depleted BI eliminated instead of Rout

Cel: 10.14 ordinary Rout threshold

Potrzeba/konsekwencja braku: Potrzebny trigger zastępowanego Rout; nie utożsamiać replacement elimination z wystąpieniem Rout dla Ferocity9.94. Depleted status nadal requires context.

Porównanie/propozycja: R993→N1014 condition/implicit poprawne w zwykłym progu. Przyjąć bounded link, bez dopisania Ferocity check po każdej elimination i bez pełnego10.2.

**first-001:** `/dependencies/32`, bajty [441957,442707), fragment SHA-256 `f429f6df134c112e9ed52e05ebbe37e0395d9af4109e0446e68aee7fc4f84b50`.

Zapis modelu: `R993→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

**context-01:** `/dependencies/32`, bajty [518125,518897), fragment SHA-256 `2185070671582e1c3c9e23e6f97e0cfb7efe805dff2c26869d22f652ff5c9926`.

Zapis modelu: `R993→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

source_evidence: `C-9.93-03` / `/items/132`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Depleted BI units do not Rout but are instead eliminated.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.14 When a unit has absorbed Cohesion Hits equal to or more
> than its TQ rating, it routs (10.2).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D994rout

Źródło: 9.94: Ferocity check each time BI Routs

Cel: 10.14 ordinary Rout threshold

Potrzeba/konsekwencja braku: Wyzwalacz potrzebny gdy nie zadano Rout. Brak realnego leader/Initiative nadal blokuje cały check; zwykły próg nie uchyla Depleted replacement9.93.

Porównanie/propozycja: R994→N1014 condition/implicit poprawne jako threshold link. Przyjąć tylko to, nie leader rating, wszystkie Rout exceptions ani połączenie elimination→Rout.

**first-001:** `/dependencies/33`, bajty [442713,443463), fragment SHA-256 `cf5bf40915502483ef5523cb7e13f4d020ee24b6432af797c9a07c9ffef180d4`.

Zapis modelu: `R994→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

**context-01:** `/dependencies/33`, bajty [518904,519676), fragment SHA-256 `5fd13c3828dcf1465f0c9c27fb9385831328573498f7ef708e54a6cd61d15ff3`.

Zapis modelu: `R994→N1014`, `condition/implicit`, `external_with_source`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Rout event in this clause requires the supplied Hits>=TQ definition; full rout procedure outside boundary remains unavailable.

source_evidence: `C-9.94-03` / `/items/136`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.14 When a unit has absorbed Cohesion Hits equal to or more
> than its TQ rating, it routs (10.2).
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D996def

Źródło: 9.96 mounted LI: wholeOrdersPhase repeated-move exemption; noShock attack; LI defense

Cel: CH atop one LI denotes mounted; combo single only for stacking

Potrzeba/konsekwencja braku: Mounted status jest warunkiem koniecznym. Cała faza dla repeated movement pozostaje dodatkowa; brak definicji mounted blokuje rozpoznanie stanu, zadany state pozwala lokalny wniosek.

Porównanie/propozycja: R996c→R996b condition/implicit poprawne; R996c ma entireOrdersPhase, must dismount forShock. Przyjąć więź stanu, bez przyznania no terrain Hits LI i bez Roman topTQ.

**first-001:** `/dependencies/14`, bajty [427836,428581), fragment SHA-256 `357f37a5617ce9e33d98ddfe5b3ddb63323218f18031e28b2b8b331e2f74723b`.

Zapis modelu: `R996c→R996b`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Counter arrangement/carrying definition supplies mounted status required for combat and repeated-movement clauses.

**context-01:** `/dependencies/14`, bajty [503577,504345), fragment SHA-256 `ea80ff8ada67b4b1917500e032f593c798a5702489fe5253db73caaa2f586fd6`.

Zapis modelu: `R996c→R996b`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Counter arrangement/carrying definition supplies mounted status required for combat and repeated-movement clauses.

source_evidence: `C-9.96-05` / `/items/145`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • LI do not suffer any Cohesion Hits for moving a second (and
> third) time in a Game Turn, if they spend the entire Orders
> Phase mounted on the CH unit.

source_evidence: `C-9.96-06` / `/items/146`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • LI cannot Shock attack; they must dismount to do so. When
> mounted, they defend as LI.

target_evidence: `C-9.96-03` / `/items/143`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

> unit for stacking purposes. All other stacking restrictions apply
> to both a CH+LI stack and a CH alone in the hex. There is no MP
> or Cohesion Hit cost to the LI unit to either mount or dismount
> from a CH. However, a dismounting LI unit may continue to
> move only if the LI+CH combination moved less than the LI’s
> printed Movement Allowance. The number of MP allowed is
> equal to the difference. Conversely, an LI unit mounting a CH
> can continue to move (as a mounted CH) up to the MA of the
> CH unit less the number of MP already used by the LI prior to
> mounting the CH. While stacked with an LI, the CH expends
> MP to enter/cross terrain or is prohibited from entering/crossing
> terrain per the Movement Cost Chart. However, Cohesion Hits
> for movement are applied to the LI only; CH units do not suffer
> Hits for Movement/Terrain.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D996fire

Źródło: 9.96 mounted LI missile row/supply exemption/H&D as cavalry

Cel: CH atop LI mounted-state definition

Potrzeba/konsekwencja braku: Stan konieczny dla permissions; brak MRRC/H&D rules blokuje konkretne fire wyniki, nie known removeLowNo instruction upon mounting.

Porównanie/propozycja: R996d→R996b condition/implicit poprawne. Mounted unit jest LI, nie CH with Size/TQ; przyjąć warunek mounted, bez wykonania MRRC/H&D i bez eligibility list.

**first-001:** `/dependencies/15`, bajty [428587,429307), fragment SHA-256 `10c9036df012795aaa27d4ca51f5da816c0da3c61995ea104b29979fb38f8f64`.

Zapis modelu: `R996d→R996b`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Mounted status defined by CH atop eligible LI is necessary for mounted fire permissions.

**context-01:** `/dependencies/15`, bajty [504352,505095), fragment SHA-256 `16be6d510ffcee54233e8f77437884a957ddafe86fc4f9c15c3804eeca5f7b1a`.

Zapis modelu: `R996d→R996b`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Mounted status defined by CH atop eligible LI is necessary for mounted fire permissions.

source_evidence: `C-9.96-07` / `/items/147`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • LI may use Missile Fire using the Mounted Javelin row on the
> MRRC. Missile Supply (8.17) does not apply while the LI unit
> is mounted. Remove any MiSSile low/No markers from the LI
> unit when the unit mounts a CH. They may use Harassment
> and Dispersal fire as if they were cavalry units.

target_evidence: `C-9.96-03` / `/items/143`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

> unit for stacking purposes. All other stacking restrictions apply
> to both a CH+LI stack and a CH alone in the hex. There is no MP
> or Cohesion Hit cost to the LI unit to either mount or dismount
> from a CH. However, a dismounting LI unit may continue to
> move only if the LI+CH combination moved less than the LI’s
> printed Movement Allowance. The number of MP allowed is
> equal to the difference. Conversely, an LI unit mounting a CH
> can continue to move (as a mounted CH) up to the MA of the
> CH unit less the number of MP already used by the LI prior to
> mounting the CH. While stacked with an LI, the CH expends
> MP to enter/cross terrain or is prohibited from entering/crossing
> terrain per the Movement Cost Chart. However, Cohesion Hits
> for movement are applied to the LI only; CH units do not suffer
> Hits for Movement/Terrain.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### D996ratings

Źródło: 9.96 transport/mount/dismount movement

Cel: CH onlyMA/noSize/noTQ; must carry eligibleLI to move, includingOW

Potrzeba/konsekwencja braku: Carry eligibleLI jest koniecznym warunkiem ruchu; sam target nie daje actualMA ani listy eligibleLI. Zadane ratingi mogą obsłużyć lokalny operator.

Porównanie/propozycja: R996b→R996a condition/implicit poparte warunkiem carrying, mimo mylącej nazwy ID ratings. Przyjąć dokładnie ten warunek i brak CH Size/TQ; EXP-074/SEM-013 i źródła ratingów niezamknięte.

**first-001:** `/dependencies/13`, bajty [427084,427830), fragment SHA-256 `e842cc2827f18d0d88492eeede7a594058a8a42bc7c348f06e392b16076a2a6b`.

Zapis modelu: `R996b→R996a`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Eligible LI carrying requirement in 9.96 is necessary to the mounted movement procedure; split clauses retain one printed label.

**context-01:** `/dependencies/13`, bajty [502802,503570), fragment SHA-256 `6bdac1dc915ccd67ed0b9f882a19dc7c4f5c826acd9fd953e391d3affec737a0`.

Zapis modelu: `R996b→R996a`, `condition/implicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Eligible LI carrying requirement in 9.96 is necessary to the mounted movement procedure; split clauses retain one printed label.

source_evidence: `C-9.96-03` / `/items/143`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

> unit for stacking purposes. All other stacking restrictions apply
> to both a CH+LI stack and a CH alone in the hex. There is no MP
> or Cohesion Hit cost to the LI unit to either mount or dismount
> from a CH. However, a dismounting LI unit may continue to
> move only if the LI+CH combination moved less than the LI’s
> printed Movement Allowance. The number of MP allowed is
> equal to the difference. Conversely, an LI unit mounting a CH
> can continue to move (as a mounted CH) up to the MA of the
> CH unit less the number of MP already used by the LI prior to
> mounting the CH. While stacked with an LI, the CH expends
> MP to enter/cross terrain or is prohibited from entering/crossing
> terrain per the Movement Cost Chart. However, Cohesion Hits
> for movement are applied to the LI only; CH units do not suffer
> Hits for Movement/Terrain.

target_evidence: `C-9.96-02` / `/items/142`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Gallic Chariot (CH) units have only a Movement Allowance;
> they have no Size and no TQ Rating. These units cannot move
> at all, and this includes Orderly Withdrawal, unless stacked with
> an eligible Light Infantry (LI) unit. If an enemy combat unit (of
> any type) moves adjacent to a CH unit alone in a hex, the CH
> unit is immediately eliminated.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### DCTX846S4-1013

Źródło: Step4 final sentence: multiple same-player units distribute per10.13

Cel: supplied10.13, not absent6.68#6 within-stack

Potrzeba/konsekwencja braku: Konieczne procedure_use; blocks_full_result=true właściwe dla pytania o podział wewnątrz stosu, nie dla każdego syntetycznego sumarycznego Hits operatora.

Porównanie/propozycja: Nowa context-only jawna NCTX846S4→N1013 poprawna. Target zachowuje equal division, priorities/owner choice, LeaderEL i attackingPH exceptions. Przyjąć bounded link plus tę blokadę; brak trzeciego źródła, nie TP z nowości.

**first-001:** brak nowej relacji przed context; nie automatyczneFN.

**context-01:** `/dependencies/128`, bajty [609604,610450), fragment SHA-256 `815bd9a822ccc3981c850a201f6b801a6a06e22684f61e01f94322191c68cd32`.

Zapis modelu: `NCTX846S4→N1013`, `procedure_use/explicit`, `external_with_source`, blocks_full_result=`True`.

Uzasadnienie modelu (osobno od oceny): Final sentence uses supplied 10.13 allocation; direction Step 4 to original boundary-context procedure. No chapter10 core expansion.

Dostarczone źródło: `private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-helper.txt`, pointer `whole bounded helper`, hash `5bb9c43565dba73617ddf0234f46401d197ee3be8d12a8a1c3f18b33610a330a`.

> Step 4: Apply Results: Results on the Shock CRT are Cohesion
> Hits for both attacker and defender. The # in parentheses is for
> the defender. The resultant Hits are modified as follows:
> • If the attacker was superior (AS), then double (2x) the de-
> fender’s result.
> • If the defender was superior (DS), then triple (3x) the attacker’s
> result.
> • If the defender is a Skirmisher, halve (½x, round down) the
> attacker’s Hits with a maximum result of 1 Hit.
> • If the attacker used in the determination is Light Cavalry (8.45)
> and the defender is a Phalanx or a Heavy, Medium, Legion, or
> Barbarian Infantry unit, halve (½x, round down) the defender’s
> Hits. This reduction does not apply if the defender is Routed
> and is cumulative with bullet #1.
> If more than one unit of the same player was involved in that
> combat, Cohesion Hits are distributed as per 10.13.
> 

Dostarczone źródło: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, pointer `/regions/15/text`, hash `0244829f403e4ed6da125404afaa6dc600bb48c037792c70f1fdc8bb6ffa1b34`.

> 10.13 If there are multiple units involved in a single combat
> resolution, Cohesion Hits must be divided as equally as possible
> amongst these units (treat a stack as a single unit for this purpose),
> with any extra Hits being given to the unit/stack:
> • used to gain Superiority (either type), otherwise
> • used to determine the Shock Column on the Clash of Spears
> and Swords Chart.
> Owning player’s choice if more than one unit/stack qualifies in
> either category. Hits allocated to a stack are distributed per 6.68
> bullet #6.
> Exceptions:
> • If a leader on a Leader Elephant is stacked with a combat unit,
> that player does not have to apportion any Hits to the Leader
> Elephant, unless the number of Hits exceeds the other combat
> unit’s TQ. In that case, all excess Hits apply to the Leader
> Elephant.
> • If a Phalanx unit is attacking two or more non-Phalanx units,
> the attacking player chooses how any Cohesion Hits will be
> distributed amongst the defenders. Such distribution may be
> uneven, if so desired. This does not apply when Phalanx units
> are defending.
> EXAMPLE: A Hastati stack and another Hastati unit receive 1
> Hit from their attack. The Hit cannot be divided equally so it is
> excess. There was no superiority and all units have the same Type
> which was used to determine the Shock column on the Clash of
> Spears and Swords chart. The attacking player gets to choose
> whether to give the Hit to the stack or the lone Hastati. If he
> chooses the stack, the top Hastati will incur the Hit.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### DCTX846S4-845

Źródło: Step4 bullet4: attacker used in determination isLC(8.45)

Cel: 8.45 selection procedure absent

Potrzeba/konsekwencja braku: Jawne wymaganie celu konieczne dla realnego selected attacker. Przy jawnie zadanym LC used-in-determination operator lokalny pozostaje ocenialny.

Porównanie/propozycja: Nowa context-only NCTX846S4→null procedure_use/explicit i blocking=true poprawnie zachowują brak8.45. Przyjąć wymaganie/blokadę konkretnego selection, bez rekonstrukcji8.45 i bez nowego źródła.

**first-001:** brak nowej relacji przed context; nie automatyczneFN.

**context-01:** `/dependencies/127`, bajty [608699,609597), fragment SHA-256 `98efb0dfcccd15963aabe8399c0c62c71ff31a45dc0251011a8ea1a6d6feef12`.

Zapis modelu: `NCTX846S4→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Uzasadnienie modelu (osobno od oceny): LC condition refers explicitly to 8.45; application fragment uses missing selection procedure.

Dostarczone źródło: `private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-helper.txt`, pointer `whole bounded helper`, hash `5bb9c43565dba73617ddf0234f46401d197ee3be8d12a8a1c3f18b33610a330a`.

> Step 4: Apply Results: Results on the Shock CRT are Cohesion
> Hits for both attacker and defender. The # in parentheses is for
> the defender. The resultant Hits are modified as follows:
> • If the attacker was superior (AS), then double (2x) the de-
> fender’s result.
> • If the defender was superior (DS), then triple (3x) the attacker’s
> result.
> • If the defender is a Skirmisher, halve (½x, round down) the
> attacker’s Hits with a maximum result of 1 Hit.
> • If the attacker used in the determination is Light Cavalry (8.45)
> and the defender is a Phalanx or a Heavy, Medium, Legion, or
> Barbarian Infantry unit, halve (½x, round down) the defender’s
> Hits. This reduction does not apply if the defender is Routed
> and is cumulative with bullet #1.
> If more than one unit of the same player was involved in that
> combat, Cohesion Hits are distributed as per 10.13.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### DCTX846S4-CRT

Źródło: Step4 header: ShockCRT results for both sides; parentheses defender

Cel: NCTX-ShockCRT is unresolved placeholder, no table source

Potrzeba/konsekwencja braku: Table_use konieczne do base lookup; brak tabeli blokuje liczby bazowe. Zadane H pozwalają oceniać lokalny faktor/rounding/cap bez lookupu.

Porównanie/propozycja: Nowa context-only NCTX846S4→NCTX-ShockCRT table_use/explicit poprawnie ma unresolved, content unknown i blocking=true. ID nie dowodzi dostępności Table. Przyjąć tylko potrzebę named target, bez rows/notes/alias closure.

**first-001:** brak nowej relacji przed context; nie automatyczneFN.

**context-01:** `/dependencies/126`, bajty [607890,608692), fragment SHA-256 `801163380f9f44885f1572dbd969d6e2b1a9d97598429dd4475438bd4cc74e9b`.

Zapis modelu: `NCTX846S4→NCTX-ShockCRT`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Uzasadnienie modelu (osobno od oceny): Step 4 uses Shock CRT results; direction is application fragment to exact named table candidate. Mention does not supply table.

Dostarczone źródło: `private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-helper.txt`, pointer `whole bounded helper`, hash `5bb9c43565dba73617ddf0234f46401d197ee3be8d12a8a1c3f18b33610a330a`.

> Step 4: Apply Results: Results on the Shock CRT are Cohesion
> Hits for both attacker and defender. The # in parentheses is for
> the defender. The resultant Hits are modified as follows:
> • If the attacker was superior (AS), then double (2x) the de-
> fender’s result.
> • If the defender was superior (DS), then triple (3x) the attacker’s
> result.
> • If the defender is a Skirmisher, halve (½x, round down) the
> attacker’s Hits with a maximum result of 1 Hit.
> • If the attacker used in the determination is Light Cavalry (8.45)
> and the defender is a Phalanx or a Heavy, Medium, Legion, or
> Barbarian Infantry unit, halve (½x, round down) the defender’s
> Hits. This reduction does not apply if the defender is Routed
> and is cumulative with bullet #1.
> If more than one unit of the same player was involved in that
> combat, Cohesion Hits are distributed as per 10.13.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### DCTX923-S4

Źródło: 9.23: SK cannot attack; Hits inflicted by SK half/floor cap1; mixed defender uses other type

Cel: Step4 bullet3: SK defender, halve attacker Hits floor cap1

Potrzeba/konsekwencja braku: Źródło wspiera stronę otrzymującą Hits: zadawane przez broniącegoSK trafiają do attacker. Przy zadanych Hits operator9.23 sam wystarcza; pełne selection/CRT nadal absent.

Porównanie/propozycja: Nowa context-only R923→NCTX846S4 ma poprawny kierunek i lokalny side/factor/cap. Procedure_use/implicit i konieczność całego Step4 wymagają decyzji SEM-004; nie rozciągać SKdefender bullet na mixed defense z innym wybranym Type. Proponuję bounded support tych komponentów, bez pełnego TP albo zamknięcia SEM-004.

**first-001:** brak nowej relacji przed context; nie automatyczneFN.

**context-01:** `/dependencies/130`, bajty [611494,612441), fragment SHA-256 `c5d2367e4a5562b2c9ffc9cef85fb2f1b68fdc7353e08cad7074bf61aca8c3c3`.

Zapis modelu: `R923→NCTX846S4`, `procedure_use/implicit`, `external_with_source`, blocks_full_result=`True`.

Uzasadnienie modelu (osobno od oceny): 9.23 halved capped Skirmisher-inflicted Hits require application to attacking side; Step 4 bullet #3 identifies that side. Core restriction uses bounded application fragment; general defender/Size selection not supplied.

source_evidence: `C-9.23-02` / `/items/55`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • Skirmishers cannot Shock attack.

source_evidence: `C-9.23-04` / `/items/57`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • If a Skirmisher unit is defending in coordination with any other
> unit type, the other Type must be chosen as the defender. The
> Size rating of the Skirmisher is ignored.

source_evidence: `C-9.23-05` / `/items/58`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.

Dostarczone źródło: `private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-helper.txt`, pointer `whole bounded helper`, hash `5bb9c43565dba73617ddf0234f46401d197ee3be8d12a8a1c3f18b33610a330a`.

> Step 4: Apply Results: Results on the Shock CRT are Cohesion
> Hits for both attacker and defender. The # in parentheses is for
> the defender. The resultant Hits are modified as follows:
> • If the attacker was superior (AS), then double (2x) the de-
> fender’s result.
> • If the defender was superior (DS), then triple (3x) the attacker’s
> result.
> • If the defender is a Skirmisher, halve (½x, round down) the
> attacker’s Hits with a maximum result of 1 Hit.
> • If the attacker used in the determination is Light Cavalry (8.45)
> and the defender is a Phalanx or a Heavy, Medium, Legion, or
> Barbarian Infantry unit, halve (½x, round down) the defender’s
> Hits. This reduction does not apply if the defender is Routed
> and is cumulative with bullet #1.
> If more than one unit of the same player was involved in that
> combat, Cohesion Hits are distributed as per 10.13.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### DCTX932-S4

Źródło: 9.32 LC attacking listed infantry halve/floor; ASexample

Cel: Step4 bullets1/4: AS2x defender; selectedLC half/floor; no reduction if Routed; cumulative

Potrzeba/konsekwencja braku: Niejawne procedure_use potrzebne do kwalifikacji stosowania redukcji przy pełnym Shock. Znane H/fakty pozwalają pojedynczy operator; brak8.45/CRT/combined order nadal blokuje pełny wynik.

Porównanie/propozycja: Nowa context-only R932→NCTX846S4 poprawnie wiąże te same LC/defender classes i wyjątek ze źródła. Przyjąć jedynie cel/direction/type tej więzi oraz jawnie zachowane niedomknięcie; nie akceptuje wyjątku jako całego polaR932, nie ustala AS/LC kolejności i nie zamyka SEM-003.

**first-001:** brak nowej relacji przed context; nie automatyczneFN.

**context-01:** `/dependencies/129`, bajty [610457,611487), fragment SHA-256 `49e4a64e8ebd72d004904f98ef714e9b347204cff67d6b75e07c8d6352861a1e`.

Zapis modelu: `R932→NCTX846S4`, `procedure_use/implicit`, `external_with_source`, blocks_full_result=`True`.

Uzasadnienie modelu (osobno od oceny): 9.32 LC halving for same listed defender classes uses Step 4 numerical qualification/cumulability with its AS example. Direction core clause to bounded application procedure; no chart alias inferred.

source_evidence: `C-9.32-01` / `/items/69`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).

source_evidence: `X-04` / `/items/166`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> EXAMPLE: A Light Cavalry unit with Attack Superiority (AS)
> against a Heavy Infantry unit would use the printed result on
> the Shock CRT.

Dostarczone źródło: `private/poc/spqr-chapter9/context/pass-01/evidence/8.46-step-4-helper.txt`, pointer `whole bounded helper`, hash `5bb9c43565dba73617ddf0234f46401d197ee3be8d12a8a1c3f18b33610a330a`.

> Step 4: Apply Results: Results on the Shock CRT are Cohesion
> Hits for both attacker and defender. The # in parentheses is for
> the defender. The resultant Hits are modified as follows:
> • If the attacker was superior (AS), then double (2x) the de-
> fender’s result.
> • If the defender was superior (DS), then triple (3x) the attacker’s
> result.
> • If the defender is a Skirmisher, halve (½x, round down) the
> attacker’s Hits with a maximum result of 1 Hit.
> • If the attacker used in the determination is Light Cavalry (8.45)
> and the defender is a Phalanx or a Heavy, Medium, Legion, or
> Barbarian Infantry unit, halve (½x, round down) the defender’s
> Hits. This reduction does not apply if the defender is Routed
> and is cumulative with bullet #1.
> If more than one unit of the same player was involved in that
> combat, Cohesion Hits are distributed as per 10.13.
> 

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### Dcont-R911

Źródło: PDF31right ends9.11 step2

Cel: PDF32left continuesstep3/4

Potrzeba/konsekwencja braku: Fizyczna kolejność; brak dalszego fragmentu ukryłby warunki placement i końcowy test. Nie osobna dependency execution.

Porównanie/propozycja: N911first→N911next continuation/explicit odpowiada DEP-090; oba locator nodes wskazują R911, który ma treść. Przyjąć tylko porządek fragmentów, bez dodatkowych punktów treści.

**first-001:** `/dependencies/16`, bajty [429313,430071), fragment SHA-256 `435030eea0dd47bbdcc6ad4b167b2e3296043cc4b311e796cd57c6b63bbcff96`.

Zapis modelu: `N911first→N911next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

**context-01:** `/dependencies/16`, bajty [505102,505882), fragment SHA-256 `cd2eb493443d82361d7f97daf6f4507c72b9513c4d905aac4c54fcf0813e13a3`.

Zapis modelu: `N911first→N911next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

source_evidence: `K-01` / `/items/183`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.

target_evidence: `K-01` / `/items/183`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### Dcont-R914

Źródło: PDF32right: Each Rampage is

Cel: PDF33left: undertaken until conclusion, oneRampage at time

Potrzeba/konsekwencja braku: Fizyczne dokończenie zdania, potrzebne dla pełnego zakresu tekstu; nie akcja wykonywana po innym mechanic.

Porównanie/propozycja: N914first→N914next continuation/explicit odpowiada DEP-092. R914 zachowuje conclusion/one at time. Przyjąć physical relation, bez executionTP.

**first-001:** `/dependencies/17`, bajty [430077,430841), fragment SHA-256 `cf1408d4f1bd3158bf11065ad95faabf5f44e1792a5884159e0d2f9297a8fd9d`.

Zapis modelu: `N914first→N914next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

**context-01:** `/dependencies/17`, bajty [505889,506675), fragment SHA-256 `edc4121a12e8aa11053841bb9dcac02d0464c253c23d441162cf1876810f3897`.

Zapis modelu: `N914first→N914next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

source_evidence: `K-03` / `/items/185`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

target_evidence: `K-03` / `/items/185`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### Dcont-R924

Źródło: PDF33right: line not disrupted if

Cel: PDF34left: interruption onlyone SK/Velites

Potrzeba/konsekwencja braku: Kontynuacja zachowuje warunek onepergap; brak urywa if i może zmienić legalność. Nie wykonawczy edge.

Porównanie/propozycja: N924first→N924next continuation/explicit odpowiada DEP-093, właściwy porządek. Przyjąć physical relation, bez całego4.32.

**first-001:** `/dependencies/18`, bajty [430847,431607), fragment SHA-256 `6cf932a5f193d3217e8ee3a113647989fcd545e1b8e1643babd2ca97fa4fa546`.

Zapis modelu: `N924first→N924next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

**context-01:** `/dependencies/18`, bajty [506682,507464), fragment SHA-256 `f02f67ddf5f96f8d3f69ac934948b1cc44efaa0c37ae96912f257fae42561e02`.

Zapis modelu: `N924first→N924next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

source_evidence: `K-04` / `/items/186`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • When determining lines for a Line Command (4.32), the pres-
> ence of a Velites or Skirmisher unit does not disrupt the line if

> the interruption is caused by only one such unit.

target_evidence: `K-04` / `/items/186`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> • When determining lines for a Line Command (4.32), the pres-
> ence of a Velites or Skirmisher unit does not disrupt the line if

> the interruption is caused by only one such unit.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### Dcont-R966

Źródło: PDF35left: all tops in sameLine(4.32)

Cel: PDF35right: sideways vacant flank/Clear/noenemyZOC/facing/unstackonly

Potrzeba/konsekwencja braku: Fizyczna kontynuacja między kolumnami; bez niej brak geometrii/wyjątków MLE. Nie procedura kolejności ruchu jednostek.

Porównanie/propozycja: N966first→N966next continuation/explicit odpowiada DEP-094. Przyjąć physical relation i wskazany zakres, bez Line/ZOC source closure.

**first-001:** `/dependencies/19`, bajty [431613,432371), fragment SHA-256 `387bdd8ef3f0d070450579538aa92840ac8f6da6d10309dfaf16e21a55379545`.

Zapis modelu: `N966first→N966next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

**context-01:** `/dependencies/19`, bajty [507471,508251), fragment SHA-256 `b1bc681c98b9a5749512f8db2e3e3235016a4b09c588595faecbad62cf0332eb`.

Zapis modelu: `N966first→N966next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

source_evidence: `K-05` / `/items/187`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

target_evidence: `K-05` / `/items/187`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### Dcont-R991

Źródło: PDF36left: BI units

Cel: PDF36right: cannotColumn/PAW/OW

Potrzeba/konsekwencja braku: Physical continuation niesie trzy zakazy; brak tekstu gubi je, ale to nie executiondependency.

Porównanie/propozycja: N991first→N991next continuation/explicit odpowiada DEP-095. R991 ma lokalną exemption passableterrain i trzy zakazy. Przyjąć tylko porządek, bez noMPcost lub impassablepermission.

**first-001:** `/dependencies/20`, bajty [432377,433135), fragment SHA-256 `f55d61a3b4eef45e79eb1fb0b95c2600e6f6707efac45cd1ef0dc998ceede90b`.

Zapis modelu: `N991first→N991next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

**context-01:** `/dependencies/20`, bajty [508258,509038), fragment SHA-256 `be04cac786bb84e7819bd92f5cf35d4f65f6b35b0916c4810f11d4c9c915fc13`.

Zapis modelu: `N991first→N991next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

source_evidence: `K-06` / `/items/188`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Barbarian Infantry (BI) units do not incur Cohesion Hits for
> crossing or entering any type of passable terrain, nor do they
> incur Cohesion Hits for changing facing in Rough terrain. BI units

> cannot use Column Movement (6.7), Pre-Arranged Withdrawal
> (6.8), or Orderly Withdrawal (6.5).

target_evidence: `K-06` / `/items/188`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Barbarian Infantry (BI) units do not incur Cohesion Hits for
> crossing or entering any type of passable terrain, nor do they
> incur Cohesion Hits for changing facing in Rough terrain. BI units

> cannot use Column Movement (6.7), Pre-Arranged Withdrawal
> (6.8), or Orderly Withdrawal (6.5).

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### Dcont-R996b

Źródło: PDF36right: CH+LI treated as single

Cel: PDF37left: unit for stacking purposes; other restrictions; mount/dismount/MP/terrain

Potrzeba/konsekwencja braku: Physical continuation zawęża single do stacking; bez niej grozi ogólnym singleunit. Nie przenosi Roman topTQ.

Porównanie/propozycja: N996first→N996next continuation/explicit odpowiada DEP-096. R996b zachowuje for stacking i pozostałe restrykcje. Przyjąć porządek fragmentów, bez nowego punktu execution.

**first-001:** `/dependencies/21`, bajty [433141,433900), fragment SHA-256 `5067dc80227b97faf4c6cdc9035c0bd5dd4455f1f857518d6732529e1603c7f7`.

Zapis modelu: `N996first→N996next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

**context-01:** `/dependencies/21`, bajty [509045,509826), fragment SHA-256 `177a4e37a472f4b855f9bb7a7a010899349a25677f2d98495603952dcacb5e2f`.

Zapis modelu: `N996first→N996next`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Earlier printed fragment points to its later physical continuation; fragment nodes do not create additional operative coverage.

source_evidence: `K-07` / `/items/189`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

> unit for stacking purposes. All other stacking restrictions apply
> to both a CH+LI stack and a CH alone in the hex. There is no MP
> or Cohesion Hit cost to the LI unit to either mount or dismount
> from a CH. However, a dismounting LI unit may continue to
> move only if the LI+CH combination moved less than the LI’s
> printed Movement Allowance. The number of MP allowed is
> equal to the difference. Conversely, an LI unit mounting a CH
> can continue to move (as a mounted CH) up to the MA of the
> CH unit less the number of MP already used by the LI prior to
> mounting the CH. While stacked with an LI, the CH expends
> MP to enter/cross terrain or is prohibited from entering/crossing
> terrain per the Movement Cost Chart. However, Cohesion Hits
> for movement are applied to the LI only; CH units do not suffer
> Hits for Movement/Terrain.

target_evidence: `K-07` / `/items/189`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

> unit for stacking purposes. All other stacking restrictions apply
> to both a CH+LI stack and a CH alone in the hex. There is no MP
> or Cohesion Hit cost to the LI unit to either mount or dismount
> from a CH. However, a dismounting LI unit may continue to
> move only if the LI+CH combination moved less than the LI’s
> printed Movement Allowance. The number of MP allowed is
> equal to the difference. Conversely, an LI unit mounting a CH
> can continue to move (as a mounted CH) up to the MA of the
> CH unit less the number of MP already used by the LI prior to
> mounting the CH. While stacked with an LI, the CH expends
> MP to enter/cross terrain or is prohibited from entering/crossing
> terrain per the Movement Cost Chart. However, Cohesion Hits
> for movement are applied to the LI only; CH units do not suffer
> Hits for Movement/Terrain.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

### Dcont-table914

Źródło: PDF32left table rows0/1–6

Cel: PDF32right table row7–9

Potrzeba/konsekwencja braku: Physical continuation jednej tabeli; brak końca gubi first/subsequent i Leader exception. Nie dodatkowa tabela ani executionTP.

Porównanie/propozycja: N914tablefirst→N914tablenext continuation/explicit odpowiada DEP-091; oba nodes należą N914table. Przyjąć wyłącznie physical relation, bez glyph/rating/rollsequencing certificate.

**first-001:** `/dependencies/125`, bajty [528179,528962), fragment SHA-256 `fc37581d9ad327c872614216f2893b35bf57d4836734cfe0c16a33812fb8ced0`.

Zapis modelu: `N914tablefirst→N914tablenext`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Table begins in left column and continues with row 7–9 at top of right column; earlier fragment points to later fragment.

**context-01:** `/dependencies/125`, bajty [607078,607883), fragment SHA-256 `5cb41e61cc9b261df87a2ababb22161139095d0891af90ad0443db64cd08b422`.

Zapis modelu: `N914tablefirst→N914tablenext`, `continuation/explicit`, `internal`, blocks_full_result=`False`.

Uzasadnienie modelu (osobno od oceny): Table begins in left column and continues with row 7–9 at top of right column; earlier fragment points to later fragment.

source_evidence: `K-02` / `/items/184`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

target_evidence: `K-02` / `/items/184`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.

##22 zamrożone pary — oddzielne porównania obu hashów

### DEP-NEW-001 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/0`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: missing_tuple. Osobnego R972→R971 condition/implicit brak w obu odpowiedziach. R971 ma obie alternatywy bramki ruchu, R972 ma RP>=floor(AWL/2) i stationaryShock własnaZOC, ale nie ma jawnej koniunkcji. Strukturalny missing_tuple zachować; treść oceniana osobno. SEM-011/EXP-052 i potencjalne semantyczne FN wymagają właściciela.

**context-01**: missing_tuple. Osobnego R972→R971 condition/implicit brak w obu odpowiedziach. R971 ma obie alternatywy bramki ruchu, R972 ma RP>=floor(AWL/2) i stationaryShock własnaZOC, ale nie ma jawnej koniunkcji. Strukturalny missing_tuple zachować; treść oceniana osobno. SEM-011/EXP-052 i potencjalne semantyczne FN wymagają właściciela.

### DEP-NEW-002 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/1`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: missing_tuple. Osobnego N914table/TR-03→R914/C-9.14-11 exception/implicit brak w obu. Treść wyjątku jest w N914table subsequent7–9 i R914.exceptions: Leader immediate rally TQ−2 overriding non-rally. Nie ma podstawy mówić, że sama proza gubi wyjątek. Przyjąć obserwację missing record + retained prose tylko, bez automatycznego FN i bez dopisania relacji.

**context-01**: missing_tuple. Osobnego N914table/TR-03→R914/C-9.14-11 exception/implicit brak w obu. Treść wyjątku jest w N914table subsequent7–9 i R914.exceptions: Leader immediate rally TQ−2 overriding non-rally. Nie ma podstawy mówić, że sama proza gubi wyjątek. Przyjąć obserwację missing record + retained prose tylko, bez automatycznego FN i bez dopisania relacji.

### DEP-NEW-003 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/2`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: missing_tuple. Osobnego R986→R914 condition/implicit brak w obu. R914 mówi noReactionFire of anykind; R986 ma any movement bez powiązania zakazu, a D986982 dotyczy innego warunku. Zgodny lokalny zakaz w osobnym rekordzie nie jest dowodem świadomego połączenia. Proponuję missing record, retained clauses, combined scope pending; any nie uchyla Rampage. Bez konkretnego błędnego shot outcome i bez automatycznego FN.

**context-01**: missing_tuple. Osobnego R986→R914 condition/implicit brak w obu. R914 mówi noReactionFire of anykind; R986 ma any movement bez powiązania zakazu, a D986982 dotyczy innego warunku. Zgodny lokalny zakaz w osobnym rekordzie nie jest dowodem świadomego połączenia. Proponuję missing record, retained clauses, combined scope pending; any nie uchyla Rampage. Bez konkretnego błędnego shot outcome i bez automatycznego FN.

### DEP-008 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/3`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_tuple_match. R924→R911 exception/explicit odpowiada DEP-008, mimo szerokich ID rodziców. R911 action/exception jawnie wyłącza SK ze Step4. Przyjąć dokładnie to zawężenie; nie całą 9.11 jako wyjątek. Wyjątek konieczny, by nie zarządzić końcowego testu SK. Nie znosi wcześniejszych warunków i etapów Pass-Thru ani Pre-Shock innych jednostek.

**context-01**: candidate_tuple_match. R924→R911 exception/explicit odpowiada DEP-008, mimo szerokich ID rodziców. R911 action/exception jawnie wyłącza SK ze Step4. Przyjąć dokładnie to zawężenie; nie całą 9.11 jako wyjątek. Wyjątek konieczny, by nie zarządzić końcowego testu SK. Nie znosi wcześniejszych warunków i etapów Pass-Thru ani Pre-Shock innych jednostek.

### DEP-002 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/4`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_tuple_match. R911→R914 condition/explicit odpowiada DEP-002. R911 zachowuje non-rout, wolny Rear, wybór gracza EL i facing. Przyjąć dokładnie sprawdzenie braku Rampage dla placement, bez wyniku całej procedury. Warunek konieczny dla tego placement; bez stanu Rampage nie wolno wybrać Rear. Cel lokalny dostępny, pełna historia Rampage nie wynika z samej pary.

**context-01**: candidate_tuple_match. R911→R914 condition/explicit odpowiada DEP-002. R911 zachowuje non-rout, wolny Rear, wybór gracza EL i facing. Przyjąć dokładnie sprawdzenie braku Rampage dla placement, bez wyniku całej procedury. Warunek konieczny dla tego placement; bez stanu Rampage nie wolno wybrać Rear. Cel lokalny dostępny, pełna historia Rampage nie wynika z samej pary.

### DEP-017 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/5`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_tuple_match. R953→R941 procedure_use/explicit odpowiada DEP-017. Oba rekordy zachowują osobne −1 oraz warunki i wszystkie wyłączenia 9.41. Przyjąć dokładnie warunkowe wywołanie, nie automatyczne4L. Użycie konieczne dla oceny shift. −1 PreShock to inny operator. Bez 9.41 nie można przyznać shift bezwarunkowo; sam dostępny cel nie daje realnego CRT/geometry.

**context-01**: candidate_tuple_match. R953→R941 procedure_use/explicit odpowiada DEP-017. Oba rekordy zachowują osobne −1 oraz warunki i wszystkie wyłączenia 9.41. Przyjąć dokładnie warunkowe wywołanie, nie automatyczne4L. Użycie konieczne dla oceny shift. −1 PreShock to inny operator. Bez 9.41 nie można przyznać shift bezwarunkowo; sam dostępny cel nie daje realnego CRT/geometry.

### DEP-024 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/6`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_tuple_match. R982→R985 procedure_use/explicit odpowiada DEP-024. R982 zachowuje tryb/switch, R985 warunki i dwa limity z różnymi jednostkami czasu. Przyjąć ten zakres, bez orderfree move/fire-in-switch-phase. Wywołanie schedule konieczne; Fire mode i no-fire switch phase z9.82 obowiązują dalej. Brak9.85 uniemożliwi prawidłowy limit, realnego missile lookup nie dostarcza.

**context-01**: candidate_tuple_match. R982→R985 procedure_use/explicit odpowiada DEP-024. R982 zachowuje tryb/switch, R985 warunki i dwa limity z różnymi jednostkami czasu. Przyjąć ten zakres, bez orderfree move/fire-in-switch-phase. Wywołanie schedule konieczne; Fire mode i no-fire switch phase z9.82 obowiązują dalej. Brak9.85 uniemożliwi prawidłowy limit, realnego missile lookup nie dostarcza.

### DEP-041 — confirmed_execution_relations

eval-v1 pointer `/confirmed_execution_relations/7`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_tuple_match. R914→N914table table_use/explicit odpowiada DEP-041. N914table zachowuje 0 Leader elimination, first/subsequent 7–9 i subsequent Leader rally TQ−2. Przyjąć tożsamość/użycie lokalnej tabeli z tymi granicami, bez glyph certificate i bez liczenia 4.84 jako pierwszego directional roll. Wykonanie wymaga właściwego wiersza. Brak tabeli uniemożliwi wynik rzutu; tabela jest dostępna. Realne nearest/map compass i inne procedury nie są przez to dostarczone.

**context-01**: candidate_tuple_match. R914→N914table table_use/explicit odpowiada DEP-041. N914table zachowuje 0 Leader elimination, first/subsequent 7–9 i subsequent Leader rally TQ−2. Przyjąć tożsamość/użycie lokalnej tabeli z tymi granicami, bez glyph certificate i bez liczenia 4.84 jako pierwszego directional roll. Wykonanie wymaga właściwego wiersza. Brak tabeli uniemożliwi wynik rzutu; tabela jest dostępna. Realne nearest/map compass i inne procedury nie są przez to dostarczone.

### DEP-034 — mentions

eval-v1 pointer `/mentions/0`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: missing_tuple. Brak osobnego N923ex→ShockResultsTable mention; literalne1(4)→0(4) i Table name są w N923ex.content. D923ex idzie od rule do example, więc nie zastępuje tej pary. Proponuję structural missing, prose occurrence retained; nie semantic FN ani alias table acceptance.

**context-01**: missing_tuple. Brak osobnego N923ex→ShockResultsTable mention; literalne1(4)→0(4) i Table name są w N923ex.content. D923ex idzie od rule do example, więc nie zastępuje tej pary. Proponuję structural missing, prose occurrence retained; nie semantic FN ani alias table acceptance.

### DEP-035 — mentions

eval-v1 pointer `/mentions/1`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: missing_tuple. Brak osobnego N932ex→ShockCRT mention. N932ex literalnie mówi printedresultonShockCRT w obu; po context interpretation wciąż unknown. D932ex rule→example nie zastępuje pary. Structural missing/prose retained, bez FN/SEM-003 closure/alias identity.

**context-01**: missing_tuple. Brak osobnego N932ex→ShockCRT mention. N932ex literalnie mówi printedresultonShockCRT w obu; po context interpretation wciąż unknown. D932ex rule→example nie zastępuje pary. Structural missing/prose retained, bez FN/SEM-003 closure/alias identity.

### DEP-037 — mentions

eval-v1 pointer `/mentions/2`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: different_kind_candidate. D961stack z R961 do StackingCharts ma table_use/explicit i blocking=true. Źródłowe See...for a summary jest zamrożoną wzmianką, nie poleceniem wykonania lookupu. R961action/transcription zachowują wystąpienie. Proponuję różnicę kind wobec DEP-037, z poprawnym referring direction i nazwą kandydata; potrzeba chart dla innych szczegółowych stacking pytań nie zmienia roli tego wystąpienia. Nie pełne TP; brak table nie jest automatycznym FP. To dodatkowy zakres frozenmention, bez wykonania reszty .4b3.

**context-01**: different_kind_candidate. D961stack z R961 do StackingCharts ma table_use/explicit i blocking=true. Źródłowe See...for a summary jest zamrożoną wzmianką, nie poleceniem wykonania lookupu. R961action/transcription zachowują wystąpienie. Proponuję różnicę kind wobec DEP-037, z poprawnym referring direction i nazwą kandydata; potrzeba chart dla innych szczegółowych stacking pytań nie zmienia roli tego wystąpienia. Nie pełne TP; brak table nie jest automatycznym FP. To dodatkowy zakres frozenmention, bez wykonania reszty .4b3.

### DEP-043 — mentions

eval-v1 pointer `/mentions/3`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: missing_tuple. Brak osobnego N914diagram/X-01→battle-map compass mention. Caption i interpretation node oraz R914transcription zachowują usecompassforeachbattle. D914compass z R914 to wykonawczy inny zakres; nie zastępuje mention z caption. Proponuję structuralmissing/proseretained, bez actualcompass/aliascertification.

**context-01**: missing_tuple. Brak osobnego N914diagram/X-01→battle-map compass mention. Caption i interpretation node oraz R914transcription zachowują usecompassforeachbattle. D914compass z R914 to wykonawczy inny zakres; nie zastępuje mention z caption. Proponuję structuralmissing/proseretained, bez actualcompass/aliascertification.

### DEP-044 — mentions

eval-v1 pointer `/mentions/4`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_occurrence_match. D966diag poprawnie odwzorowuje9.66 see diagram above jako mention do lokalnegoD-02. Oba końce dostępne i ilustracja odpowiada sideways-unstack/facing. Przyjąć occurrence/role, bez ratingów i bez całej geometry/legalności.

**context-01**: candidate_occurrence_match. D966diag poprawnie odwzorowuje9.66 see diagram above jako mention do lokalnegoD-02. Oba końce dostępne i ilustracja odpowiada sideways-unstack/facing. Przyjąć occurrence/role, bez ratingów i bez całej geometry/legalności.

### DEP-063 — mentions

eval-v1 pointer `/mentions/5`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_occurrence_match. D953scenario odwzorowuje X-06 do Cynoscephalaeexample jako mention/explicit. Treści scenario nie ma. Przyjąć occurrence/role i non-execution, bez treści ani zewnętrznej sourceidentity.

**context-01**: candidate_occurrence_match. D953scenario odwzorowuje X-06 do Cynoscephalaeexample jako mention/explicit. Treści scenario nie ma. Przyjąć occurrence/role i non-execution, bez treści ani zewnętrznej sourceidentity.

### DEP-067-1 — mentions

eval-v1 pointer `/mentions/6`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: missing_tuple. Brak osobnego R966→OWalternative mention. R966action zachowuje inplaceofOW oraz text9.66, a D967OW odnosi się do współwystępowania w9.67, inny zakres. Proponuję structuralmissing/proseretained dla frozenfacet, bez semanticFN i bez nowych Clear/ZOC/OWaliases.

**context-01**: missing_tuple. Brak osobnego R966→OWalternative mention. R966action zachowuje inplaceofOW oraz text9.66, a D967OW odnosi się do współwystępowania w9.67, inny zakres. Proponuję structuralmissing/proseretained dla frozenfacet, bez semanticFN i bez nowych Clear/ZOC/OWaliases.

### DEP-090 — continuations

eval-v1 pointer `/continuations/0`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_physical_order_match. N911first→N911next continuation/explicit odpowiada DEP-090; oba locator nodes wskazują R911, który ma treść. Przyjąć tylko porządek fragmentów, bez dodatkowych punktów treści. Fizyczna kolejność; brak dalszego fragmentu ukryłby warunki placement i końcowy test. Nie osobna dependency execution.

**context-01**: candidate_physical_order_match. N911first→N911next continuation/explicit odpowiada DEP-090; oba locator nodes wskazują R911, który ma treść. Przyjąć tylko porządek fragmentów, bez dodatkowych punktów treści. Fizyczna kolejność; brak dalszego fragmentu ukryłby warunki placement i końcowy test. Nie osobna dependency execution.

### DEP-091 — continuations

eval-v1 pointer `/continuations/1`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_physical_order_match. N914tablefirst→N914tablenext continuation/explicit odpowiada DEP-091; oba nodes należą N914table. Przyjąć wyłącznie physical relation, bez glyph/rating/rollsequencing certificate. Physical continuation jednej tabeli; brak końca gubi first/subsequent i Leader exception. Nie dodatkowa tabela ani executionTP.

**context-01**: candidate_physical_order_match. N914tablefirst→N914tablenext continuation/explicit odpowiada DEP-091; oba nodes należą N914table. Przyjąć wyłącznie physical relation, bez glyph/rating/rollsequencing certificate. Physical continuation jednej tabeli; brak końca gubi first/subsequent i Leader exception. Nie dodatkowa tabela ani executionTP.

### DEP-092 — continuations

eval-v1 pointer `/continuations/2`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_physical_order_match. N914first→N914next continuation/explicit odpowiada DEP-092. R914 zachowuje conclusion/one at time. Przyjąć physical relation, bez executionTP. Fizyczne dokończenie zdania, potrzebne dla pełnego zakresu tekstu; nie akcja wykonywana po innym mechanic.

**context-01**: candidate_physical_order_match. N914first→N914next continuation/explicit odpowiada DEP-092. R914 zachowuje conclusion/one at time. Przyjąć physical relation, bez executionTP. Fizyczne dokończenie zdania, potrzebne dla pełnego zakresu tekstu; nie akcja wykonywana po innym mechanic.

### DEP-093 — continuations

eval-v1 pointer `/continuations/3`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_physical_order_match. N924first→N924next continuation/explicit odpowiada DEP-093, właściwy porządek. Przyjąć physical relation, bez całego4.32. Kontynuacja zachowuje warunek onepergap; brak urywa if i może zmienić legalność. Nie wykonawczy edge.

**context-01**: candidate_physical_order_match. N924first→N924next continuation/explicit odpowiada DEP-093, właściwy porządek. Przyjąć physical relation, bez całego4.32. Kontynuacja zachowuje warunek onepergap; brak urywa if i może zmienić legalność. Nie wykonawczy edge.

### DEP-094 — continuations

eval-v1 pointer `/continuations/4`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_physical_order_match. N966first→N966next continuation/explicit odpowiada DEP-094. Przyjąć physical relation i wskazany zakres, bez Line/ZOC source closure. Fizyczna kontynuacja między kolumnami; bez niej brak geometrii/wyjątków MLE. Nie procedura kolejności ruchu jednostek.

**context-01**: candidate_physical_order_match. N966first→N966next continuation/explicit odpowiada DEP-094. Przyjąć physical relation i wskazany zakres, bez Line/ZOC source closure. Fizyczna kontynuacja między kolumnami; bez niej brak geometrii/wyjątków MLE. Nie procedura kolejności ruchu jednostek.

### DEP-095 — continuations

eval-v1 pointer `/continuations/5`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_physical_order_match. N991first→N991next continuation/explicit odpowiada DEP-095. R991 ma lokalną exemption passableterrain i trzy zakazy. Przyjąć tylko porządek, bez noMPcost lub impassablepermission. Physical continuation niesie trzy zakazy; brak tekstu gubi je, ale to nie executiondependency.

**context-01**: candidate_physical_order_match. N991first→N991next continuation/explicit odpowiada DEP-095. R991 ma lokalną exemption passableterrain i trzy zakazy. Przyjąć tylko porządek, bez noMPcost lub impassablepermission. Physical continuation niesie trzy zakazy; brak tekstu gubi je, ale to nie executiondependency.

### DEP-096 — continuations

eval-v1 pointer `/continuations/6`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.

**first-001**: candidate_physical_order_match. N996first→N996next continuation/explicit odpowiada DEP-096. R996b zachowuje for stacking i pozostałe restrykcje. Przyjąć porządek fragmentów, bez nowego punktu execution. Physical continuation zawęża single do stacking; bez niej grozi ogólnym singleunit. Nie przenosi Roman topTQ.

**context-01**: candidate_physical_order_match. N996first→N996next continuation/explicit odpowiada DEP-096. R996b zachowuje for stacking i pozostałe restrykcje. Przyjąć porządek fragmentów, bez nowego punktu execution. Physical continuation zawęża single do stacking; bez niej grozi ogólnym singleunit. Nie przenosi Roman topTQ.

##Granice wyniku

105 candidates nie staje się gold. Nowe edges osobno, bez punktów za nowość. PełneTP_gold/TP_output/FP/FN/precision/recall not_assessable. 132 wystąpienia .4b2/.4b3 czekają na osobne sesje.

Właścicielowi udostępniono pakiet125 wystąpień; faktyczny odczyt/otwarcie unknown, nowe humanreview0, pending125. Dodatkowe22pary/hash także waiting_review. Dawne63lokalne/3wymagania source na hash bez zmiany; EXP-010/017/019/040/050/052/066/074 i SEM-001–013 pozostają otwarte.

1 dodatkowa strona/1reguła/0tabel,1runda context/0korekt;0pełnych domknięć,4częściowe uzupełnienia i4nowe deklaracje. Trzeciego źródła nie pozyskano, stop rozszerzania na2. Czysty kontekst/ekspozycja unknown, listing/path discovery poza allowlistą potwierdzony, treści oceny nie zaobserwowano. Nie dowodzi skażenia ani izolacji. Aktywny czas/budżet/config/tokeny/cena unknown.

Następny krok: decyzje dla owner-focus i wcześniejszych pending; potem osobna .4b2, oszacowana przed wykonaniem; .4b3/.4c/.4d później. M-POC5A/.4/.4b partial; M-POC5 jedyny next.
