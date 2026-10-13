# M-POC5A.4b2 — rzeczywiste porównania wszystkich 30 ID

60 wystąpień: 30 first-001 i 30 context-01. Recenzent propozycji: Codex; właściciel akceptuje znaczenie. Wszystkie nowe decyzje waiting_review.

52 wystąpienia mają propozycję przyjęcia ograniczonej roli relacji/wymagania źródła. Dla 8 wydzielono osobną decyzję o zakresie blokady SEM-017. To nie liczba poprawnych całych rekordów lub TP.

first-001: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`; PDF `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

[Pełne ślady obu wyników](comparisons.json) zawierają surowe rekordy i pola, źródła, pointers, zakresy bajtów [start,end) i hashe. Brakującego celu nie odczytano; nie jest zastąpiony nazwą/opisem modelu.

## D-ZOC-R911

Źródło i dokładny zakres: 9.11: enemy ZOC at start of Orders Phase excludes Pass-Thru

Cel i granica dostępności: General ZOC definition/geometric applicability and exceptions; actual target absent

Konieczność / zakres blokady: Definicja potrzebna do ustalenia rzeczywistego in-ZOC na planszy. Jeśli obecność ZOC na początku fazy jest zadana, lokalny zakaz Pass-Thru jest znany.

Porównanie i propozycja: Obie odpowiedzi mają R911→kandydat ZOC definition/implicit. Źródło używa terminu w warunku, a zależność od jego ogólnej definicji jest wnioskowana, nie numerowana. Poparte jako wymaganie definicji; nie rozstrzyga geometrii, aliasu ani całego Pass-Thru.

**first-001:** `/dependencies/120`; bajty [523438,524391), SHA-256 `1676fe4b675a0d7702c66cf902de18bd65f7421d1babef6caa59860c914b1792`.

Zapis modelu: `R911→candidate`, `definition/implicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Deklaracja wpływu modelu: {"affected_ids": ["R911"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Definicja potrzebna do ustalenia rzeczywistego in-ZOC na planszy. Jeśli obecność ZOC na początku fazy jest zadana, lokalny zakaz Pass-Thru jest znany.

Zapis gapu modelu: G-D-ZOC-R911 — General ZOC test in rule condition is referenced but unavailable. Potrzebny kontekst: General ZOC definition and exceptions

**context-01:** `/dependencies/120`; bajty [602195,603176), SHA-256 `34a605d413ce8fb6b7bac98d3dcd37cb389b783e7eb82888380efe8ce2ab5c02`.

Zapis modelu: `R911→candidate`, `definition/implicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Deklaracja wpływu modelu: {"affected_ids": ["R911"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Definicja potrzebna do ustalenia rzeczywistego in-ZOC na planszy. Jeśli obecność ZOC na początku fazy jest zadana, lokalny zakaz Pass-Thru jest znany.

Zapis gapu modelu: G-D-ZOC-R911 — General ZOC test in rule condition is referenced but unavailable. Potrzebny kontekst: General ZOC definition and exceptions

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/2/text`, znaki [595,1627), SHA-256 wycinka `d005729e091c5829f0e6ae05229178059dc08510c1d19e10f85606a480723249`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.11 Elephant Pass-Thru: An infantry unit being
> attacked through one of its Front hexes by an Ele-
> phant unit marked SHOCK MUST CHECK TQ, may
> attempt to allow the Elephant unit to pass through its
> hex. This decision must be made prior to the Pre-Shock TQ Check
> die roll (8.43) and may be elected only if at least one of the de-
> fender’s Rear hexes is unoccupied. Pass-Thru is not allowed if:
> • an infantry unit is attacked through a Flank or Rear.
> • an Elephant unit is attacking along with other units.
> • the infantry unit was in an enemy ZOC at the start of the Orders
> Phase.
> Pass-Thru may be used by two defending infantry units if both
> units meet the preceding conditions. If the player decides against
> Pass-Thru, Shock proceeds normally.
> If the player decides to allow the Pass-Thru, do the following:
> 1. Apply a +1 DRM to the infantry unit’s Pre-Shock TQ Check
> DR.
> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/3/text`, znaki [0,453), SHA-256 wycinka `74d076d61a1ce443a13447a025057d28f9b0163c73c7cf2978ae6950fc5f3fe9`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.
> 4. The defending unit, other than a Skirmisher unit, now un-
> dergoes a Pass-Thru TQ Check. Subtract the unit’s TQ from
> the DR, with any excess being the number of Cohesion Hits
> now applied (DR–TQ=Hits).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D-ZOC-R915

Źródło i dokładny zakres: 9.15: voluntary entry to enemy Elephant ZOC forbidden; forced entry has penalty

Cel i granica dostępności: General ZOC geometric definition/exceptions, absent

Konieczność / zakres blokady: Definicja konieczna do rozpoznania rzeczywistego ZOC. Przy zadanym ZOC znany jest zakaz dobrowolnego wejścia; wymuszone wejście i 2 Hits pozostają lokalnie określone.

Porównanie i propozycja: R915→ZOC definition/implicit poparte warunkiem źródła w obu wynikach. Nie przenosi definicji Front na wszystkie sąsiadujące heksy ani nie blokuje automatycznie znanej kary przy zadanym wejściu.

**first-001:** `/dependencies/121`; bajty [524397,525332), SHA-256 `fc7b6f104c24b359bae521f2a84eab52f89dd9ddec2e342ee61201e548e9604f`.

Zapis modelu: `R915→candidate`, `definition/implicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Deklaracja wpływu modelu: {"affected_ids": ["R915"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Definicja konieczna do rozpoznania rzeczywistego ZOC. Przy zadanym ZOC znany jest zakaz dobrowolnego wejścia; wymuszone wejście i 2 Hits pozostają lokalnie określone.

Zapis gapu modelu: G-D-ZOC-R915 — General ZOC test in rule condition is referenced but unavailable. Potrzebny kontekst: General ZOC definition and exceptions

**context-01:** `/dependencies/121`; bajty [603183,604145), SHA-256 `eed1fc785bc87edd49761140f119e7afe2d62133d0ffe88cd0491c001718ce76`.

Zapis modelu: `R915→candidate`, `definition/implicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Deklaracja wpływu modelu: {"affected_ids": ["R915"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Definicja konieczna do rozpoznania rzeczywistego ZOC. Przy zadanym ZOC znany jest zakaz dobrowolnego wejścia; wymuszone wejście i 2 Hits pozostają lokalnie określone.

Zapis gapu modelu: G-D-ZOC-R915 — General ZOC test in rule condition is referenced but unavailable. Potrzebny kontekst: General ZOC definition and exceptions

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/5/text`, znaki [331,875), SHA-256 wycinka `3b3bd2be445ca417fd2cafc7d52fb80d85c004920f90b8b4c2046fb18b6a58bc`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.15 Cavalry vs. Elephants: Cavalry units may never voluntarily
> move into the ZOC of an enemy Elephant unit. They may move
> into or through an enemy Elephant’s Flank or Rear hexes but
> at the cost of 2 Cohesion Hits for each such hex entered. This
> cohesion penalty also applies if the cavalry unit is forced to enter
> an Elephant ZOC. Cavalry may never attack an enemy Elephant
> through the latter’s Front hexes; they may attack through the
> Elephant unit’s Flank or Rear hexes, but they do not gain the
> usual Attack Superiority for such an attack.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D1011chart

Źródło i dokładny zakres: 10.11: chart gives timing and result of general TQ check; routed TQ=1

Cel i granica dostępności: Actual Cohesion Hit and TQ Check Chart cells/timing, absent; 8.75 supplies only chart purpose

Konieczność / zakres blokady: Pełny ogólny test stosuje wynik chart. Lokalny przepis podający wynik wprost i zadane DR/TQ nie zawsze wymaga tabeli.

Porównanie i propozycja: N1011→chart table_use/explicit poparte słowami apply result given on chart, nie samym słowem summary w 8.75. Dostępny N875 opisuje rolę, nie komórki. Odróżnić od wcześniejszej wzmianki summary D961stack; przyjąć potrzebę pełnego chart, nie jego treść.

**first-001:** `/dependencies/24`; bajty [435642,436638), SHA-256 `02c77bad09babfc13be614fa43fa689ec6f740abd03edcdf519cef5c7d811183`.

Zapis modelu: `N1011→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Cohesion Hit and TQ Check Chart", "description": "TQ check chart timing and results", "needed_context": "Actual Cohesion Hit and TQ Check Chart."}

Uzasadnienie modelu: Source refers to Cohesion Hit and TQ Check Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["N1011"], "blocks_full_result": true, "reason": "TQ check chart timing and results is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny ogólny test stosuje wynik chart. Lokalny przepis podający wynik wprost i zadane DR/TQ nie zawsze wymaga tabeli.

Zapis gapu modelu: G-D1011chart — TQ check chart timing and results is referenced but unavailable. Potrzebny kontekst: Actual Cohesion Hit and TQ Check Chart.

**context-01:** `/dependencies/24`; bajty [511620,512644), SHA-256 `19f3dee6a0aabb15765280862fcad60ac8ea13f54330c10f068040f14c17b9e2`.

Zapis modelu: `N1011→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Cohesion Hit and TQ Check Chart", "description": "TQ check chart timing and results", "needed_context": "Actual Cohesion Hit and TQ Check Chart."}

Uzasadnienie modelu: Source refers to Cohesion Hit and TQ Check Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["N1011"], "blocks_full_result": true, "reason": "TQ check chart timing and results is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny ogólny test stosuje wynik chart. Lokalny przepis podający wynik wprost i zadane DR/TQ nie zawsze wymaga tabeli.

Zapis gapu modelu: G-D1011chart — TQ check chart timing and results is referenced but unavailable. Potrzebny kontekst: Actual Cohesion Hit and TQ Check Chart.

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/14/text`, znaki [639,1100), SHA-256 wycinka `ad14eb29acf309d322fe14c90cacfe825c8c36d6db647ae11521d5768e4d13be`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 10.11 TQ Checks: The Cohesion Hit and TQ Check Chart gives
> the times during the game when a unit must undergo a TQ check.
> These instances have also been noted throughout the rules. A TQ
> check consists of rolling the die and comparing it to the unit’s
> printed TQ rating, and applying the result given on the chart—
> usually one or more Cohesion Hits if the DR exceeds the rating.
> Exception: Routed units use a TQ of 1 for all TQ checks instead
> of the printed TQ.
> 

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [803,931), SHA-256 wycinka `173e80b82aa7d5bcc82f7e015a3d3d6ca314323b85f9cc034b46b12ae41edf2d`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 8.75 The Cohesion Hit and TQ Check Chart: Use this as
> a summary of when Cohesion Hits are applied and when TQ
> checks take place.

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D1013stack

Źródło i dokładny zakres: 10.13: Hits already allocated to stack are distributed per 6.68 bullet #6

Cel i granica dostępności: Exact 6.68 bullet #6 and qualifications, absent

Konieczność / zakres blokady: Konieczne do rozdziału wewnątrz stosu, nie do każdego podziału między jednostkami. Przykład top Hastati jest pojedynczym przykładem, nie pełną zastępczą procedurą.

Porównanie i propozycja: N1013→6.68#6 procedure_use/explicit i G-D1013stack blocking=true zgodne w obu wynikach. To rzeczywisty niepozyskany koniec ścieżki R962→Step4→10.13→6.68, nie jej domknięcie. Decyzja SEM-014 o wadliwej blokadzie D9621013 pozostaje w swoim zakresie.

**first-001:** `/dependencies/23`; bajty [434674,435636), SHA-256 `a210457dc5059864350df6e33f5430059791bf46150555b9d9a7c979cbb4f6d2`.

Zapis modelu: `N1013→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.68 bullet #6", "description": "Within-stack Cohesion Hit distribution", "needed_context": "6.68 bullet #6, including qualifications."}

Uzasadnienie modelu: Source refers to 6.68 bullet #6; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["N1013"], "blocks_full_result": true, "reason": "Within-stack Cohesion Hit distribution is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Konieczne do rozdziału wewnątrz stosu, nie do każdego podziału między jednostkami. Przykład top Hastati jest pojedynczym przykładem, nie pełną zastępczą procedurą.

Zapis gapu modelu: G-D1013stack — Within-stack Cohesion Hit distribution is referenced but unavailable. Potrzebny kontekst: 6.68 bullet #6, including qualifications.

**context-01:** `/dependencies/23`; bajty [510624,511613), SHA-256 `35c82ea3060bbe4c653e8f95a25bd55ff7fd070b60a40e9dd000eb39513ff9f1`.

Zapis modelu: `N1013→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.68 bullet #6", "description": "Within-stack Cohesion Hit distribution", "needed_context": "6.68 bullet #6, including qualifications."}

Uzasadnienie modelu: Source refers to 6.68 bullet #6; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["N1013"], "blocks_full_result": true, "reason": "Within-stack Cohesion Hit distribution is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Konieczne do rozdziału wewnątrz stosu, nie do każdego podziału między jednostkami. Przykład top Hastati jest pojedynczym przykładem, nie pełną zastępczą procedurą.

Zapis gapu modelu: G-D1013stack — Within-stack Cohesion Hit distribution is referenced but unavailable. Potrzebny kontekst: 6.68 bullet #6, including qualifications.

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/15/text`, znaki [111,1598), SHA-256 wycinka `818411bcd8f7926828082c16fbc686af4fed75ccb9e7c32e6b829a0534245e11`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

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

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D911pre

Źródło i dokładny zakres: 9.11: decision before Pre-Shock TQ roll (8.43), +1 DRM in step1

Cel i granica dostępności: 8.43 Pre-Shock TQ check timing/marker/check procedure, absent

Konieczność / zakres blokady: Brak 8.43 blokuje pełne przeprowadzenie Pre-Shock. Zadany prawidłowy rzut można lokalnie zmodyfikować o +1; końcowy Pass-Thru check nie jest tym samym etapem.

Porównanie i propozycja: R911→8.43 procedure_use/explicit ma właściwy cel wskazany numerem i kierunek. Brak full procedure uczciwie zachowany. Obie odpowiedzi rozróżniają etap1 i końcowy etap4; wyjątek SK z 9.24 nie znosi etapu1 dla wszystkich.

**first-001:** `/dependencies/45`; bajty [451118,452028), SHA-256 `389bc985d2d58b34835c75e8f0c6a28f117bafd8d6b0c6e4b057abf701c443e7`.

Zapis modelu: `R911→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.43", "description": "Pre-Shock TQ Check procedure", "needed_context": "8.43 including marker/check/DRM rules"}

Uzasadnienie modelu: Source refers to 8.43; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R911"], "blocks_full_result": true, "reason": "Pre-Shock TQ Check procedure is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Brak 8.43 blokuje pełne przeprowadzenie Pre-Shock. Zadany prawidłowy rzut można lokalnie zmodyfikować o +1; końcowy Pass-Thru check nie jest tym samym etapem.

Zapis gapu modelu: G-D911pre — Pre-Shock TQ Check procedure is referenced but unavailable. Potrzebny kontekst: 8.43 including marker/check/DRM rules

**context-01:** `/dependencies/45`; bajty [527584,528521), SHA-256 `9f5acc9e5ad21db35ac24c2abc1c2b081e1c2086f457084450777a90379087d2`.

Zapis modelu: `R911→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.43", "description": "Pre-Shock TQ Check procedure", "needed_context": "8.43 including marker/check/DRM rules"}

Uzasadnienie modelu: Source refers to 8.43; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R911"], "blocks_full_result": true, "reason": "Pre-Shock TQ Check procedure is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Brak 8.43 blokuje pełne przeprowadzenie Pre-Shock. Zadany prawidłowy rzut można lokalnie zmodyfikować o +1; końcowy Pass-Thru check nie jest tym samym etapem.

Zapis gapu modelu: G-D911pre — Pre-Shock TQ Check procedure is referenced but unavailable. Potrzebny kontekst: 8.43 including marker/check/DRM rules

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/2/text`, znaki [595,1627), SHA-256 wycinka `d005729e091c5829f0e6ae05229178059dc08510c1d19e10f85606a480723249`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.11 Elephant Pass-Thru: An infantry unit being
> attacked through one of its Front hexes by an Ele-
> phant unit marked SHOCK MUST CHECK TQ, may
> attempt to allow the Elephant unit to pass through its
> hex. This decision must be made prior to the Pre-Shock TQ Check
> die roll (8.43) and may be elected only if at least one of the de-
> fender’s Rear hexes is unoccupied. Pass-Thru is not allowed if:
> • an infantry unit is attacked through a Flank or Rear.
> • an Elephant unit is attacking along with other units.
> • the infantry unit was in an enemy ZOC at the start of the Orders
> Phase.
> Pass-Thru may be used by two defending infantry units if both
> units meet the preceding conditions. If the player decides against
> Pass-Thru, Shock proceeds normally.
> If the player decides to allow the Pass-Thru, do the following:
> 1. Apply a +1 DRM to the infantry unit’s Pre-Shock TQ Check
> DR.
> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D911shock

Źródło i dokładny zakres: 9.11 step2: proceed with Shock resolution, then halve defender Hits and reduce Elephant Hits by1

Cel i granica dostępności: Base Shock resolution and tables; only Step4 operators supplied after context, earlier steps/table absent

Konieczność / zakres blokady: Pełny bazowy Shock wymaga brakujących procedur/tabel. Przy zadanych base Hits lokalne pół/floor i minus1 są znane. Step4 nie dostarcza lookupu całej walki.

Porównanie i propozycja: Krawędź procedure_use/explicit identyczna, target pozostaje unresolved; po kontekście nie należy twierdzić, że cała procedura jest całkowicie niedostarczona, bo Step4 jest dostępny częściowo. Przyjąć potrzebę brakujących kroków/base, bez blankietowego blokowania lokalnych operatorów lub domknięcia alokacji.

**first-001:** `/dependencies/46`; bajty [452034,453068), SHA-256 `863d5df0b7b68933f7c5ab1346e9b227ee7c9b0f694140f2868018ea9d1c95c6`.

Zapis modelu: `R911→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock resolution procedure", "description": "Base Shock resolution needed before Pass-Thru hit adjustments", "needed_context": "Full Shock resolution procedure and used tables"}

Uzasadnienie modelu: Source refers to Shock resolution procedure; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R911"], "blocks_full_result": true, "reason": "Base Shock resolution needed before Pass-Thru hit adjustments is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny bazowy Shock wymaga brakujących procedur/tabel. Przy zadanych base Hits lokalne pół/floor i minus1 są znane. Step4 nie dostarcza lookupu całej walki.

Zapis gapu modelu: G-D911shock — Base Shock resolution needed before Pass-Thru hit adjustments is referenced but unavailable. Potrzebny kontekst: Full Shock resolution procedure and used tables

**context-01:** `/dependencies/46`; bajty [528528,529589), SHA-256 `a4e7d279f73999284dcca2ad386deab3102d81fd3ee3f4db7444283298b1f5ba`.

Zapis modelu: `R911→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock resolution procedure", "description": "Base Shock resolution needed before Pass-Thru hit adjustments", "needed_context": "Full Shock resolution procedure and used tables"}

Uzasadnienie modelu: Source refers to Shock resolution procedure; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R911"], "blocks_full_result": true, "reason": "Base Shock resolution needed before Pass-Thru hit adjustments is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny bazowy Shock wymaga brakujących procedur/tabel. Przy zadanych base Hits lokalne pół/floor i minus1 są znane. Step4 nie dostarcza lookupu całej walki.

Zapis gapu modelu: G-D911shock — Base Shock resolution needed before Pass-Thru hit adjustments is referenced but unavailable. Potrzebny kontekst: Full Shock resolution procedure and used tables

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/2/text`, znaki [595,1627), SHA-256 wycinka `d005729e091c5829f0e6ae05229178059dc08510c1d19e10f85606a480723249`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.11 Elephant Pass-Thru: An infantry unit being
> attacked through one of its Front hexes by an Ele-
> phant unit marked SHOCK MUST CHECK TQ, may
> attempt to allow the Elephant unit to pass through its
> hex. This decision must be made prior to the Pre-Shock TQ Check
> die roll (8.43) and may be elected only if at least one of the de-
> fender’s Rear hexes is unoccupied. Pass-Thru is not allowed if:
> • an infantry unit is attacked through a Flank or Rear.
> • an Elephant unit is attacking along with other units.
> • the infantry unit was in an enemy ZOC at the start of the Orders
> Phase.
> Pass-Thru may be used by two defending infantry units if both
> units meet the preceding conditions. If the player decides against
> Pass-Thru, Shock proceeds normally.
> If the player decides to allow the Pass-Thru, do the following:
> 1. Apply a +1 DRM to the infantry unit’s Pre-Shock TQ Check
> DR.
> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/3/text`, znaki [0,453), SHA-256 wycinka `74d076d61a1ce443a13447a025057d28f9b0163c73c7cf2978ae6950fc5f3fe9`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.
> 4. The defending unit, other than a Skirmisher unit, now un-
> dergoes a Pass-Thru TQ Check. Subtract the unit’s TQ from
> the DR, with any excess being the number of Cohesion Hits
> now applied (DR–TQ=Hits).
> 

Dodatkowy wcześniej dostarczony kontekst tylko dla context-01: Step4. Nie dostarcza wcześniejszych etapów lub rzeczywistej CRT.

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

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D912MRRC

Źródło i dokładny zakres: 9.12: Reaction Fire only using Elephant Screen row of MRRC

Cel i granica dostępności: Actual Elephant Screen row, headers/modifiers/notes of MRRC, absent; 8.71 only descriptive

Konieczność / zakres blokady: Wynik strzału wymaga tabeli; sam zakaz innego trybu strzału oraz brak screen u Leader Elephant są znane.

Porównanie i propozycja: R912→Elephant Screen row table_use/explicit zgodne. Description N871 nie jest row. Screen i tower rider nie mogą dostać jednego domyślnego wyniku; oba rzuty pozostają osobne według9.13. Przyjąć nazwane wymaganie, nie tabelę/żeton/supply procedure.

**first-001:** `/dependencies/48`; bajty [453997,454981), SHA-256 `def8a8ec219272cbefe09da69f79d803b121824d126b810983b49e75c01b82a0`.

Zapis modelu: `R912→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Elephant Screen row on the MRRC", "description": "Elephant Screen missile results", "needed_context": "MRRC Elephant Screen row, headers, modifiers and notes"}

Uzasadnienie modelu: Source refers to Elephant Screen row on the MRRC; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R912"], "blocks_full_result": true, "reason": "Elephant Screen missile results is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Wynik strzału wymaga tabeli; sam zakaz innego trybu strzału oraz brak screen u Leader Elephant są znane.

Zapis gapu modelu: G-D912MRRC — Elephant Screen missile results is referenced but unavailable. Potrzebny kontekst: MRRC Elephant Screen row, headers, modifiers and notes

**context-01:** `/dependencies/48`; bajty [530547,531558), SHA-256 `2787bd01cee735a890045987e1c08580b96836ed67ad81df69207f069331a604`.

Zapis modelu: `R912→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Elephant Screen row on the MRRC", "description": "Elephant Screen missile results", "needed_context": "MRRC Elephant Screen row, headers, modifiers and notes"}

Uzasadnienie modelu: Source refers to Elephant Screen row on the MRRC; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R912"], "blocks_full_result": true, "reason": "Elephant Screen missile results is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Wynik strzału wymaga tabeli; sam zakaz innego trybu strzału oraz brak screen u Leader Elephant są znane.

Zapis gapu modelu: G-D912MRRC — Elephant Screen missile results is referenced but unavailable. Potrzebny kontekst: MRRC Elephant Screen row, headers, modifiers and notes

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/3/text`, znaki [706,1320), SHA-256 wycinka `28cc98241b9178448cf90ad26f2bb63f07c4bde2cfa3575c1cc9635c16e2bed7`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.12 Elephant Screens: Elephants were quite vulnerable to
> missile attacks, and, to protect against this, armies surrounded
> each Elephant with its own light screen of skirmishers, usually
> archers represented by the small “a” on the counter. The firepower
> is much less than normal archer units, to account for the size of
> the screen and its tactical use.
> Elephant Screens can Missile Fire with Reaction Fire (8.2) only,
> using the Elephant Screen row on the MRRC. Elephant Screens
> have their own missile supply markers. Leader elephants do not
> have screens (they usually did, but they were too small to be a
> factor).
> 

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [22,152), SHA-256 wycinka `6d536a1df692b011b2266ea6a564038d9b9444918a402e57a151b593e89eb00e`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 8.71 The Missile Range and Results Chart: This table is used
> to determine the strength of a missile unit firing at a given range.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D912react

Źródło i dokładny zakres: 9.12: screen can fire with Reaction Fire (8.2) only

Cel i granica dostępności: 8.2 general Reaction Fire timing/eligibility, absent

Konieczność / zakres blokady: 8.2 potrzebne do legalnego momentu i wykonania reakcji, nie do odczytania lokalnego only.

Porównanie i propozycja: R912→8.2 procedure_use/explicit jest bezpośrednie i zachowuje ograniczenie only. Blokada pełnego legalnego strzału jest poparta; nie uznać braku źródła za nieznany lokalny zakaz albo dowód, że ekran rzeczywiście może strzelić w dowolnym momencie.

**first-001:** `/dependencies/47`; bajty [453074,453991), SHA-256 `33232c5c5f3b1135fb3d671916a22e97476d5130e5049cdc1d6b784e045f523c`.

Zapis modelu: `R912→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.2", "description": "Ordinary Reaction Fire timing/eligibility", "needed_context": "8.2 Reaction Fire"}

Uzasadnienie modelu: Source refers to 8.2; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R912"], "blocks_full_result": true, "reason": "Ordinary Reaction Fire timing/eligibility is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. 8.2 potrzebne do legalnego momentu i wykonania reakcji, nie do odczytania lokalnego only.

Zapis gapu modelu: G-D912react — Ordinary Reaction Fire timing/eligibility is referenced but unavailable. Potrzebny kontekst: 8.2 Reaction Fire

**context-01:** `/dependencies/47`; bajty [529596,530540), SHA-256 `50ca262743187bc65b629c44011b525e42040329914e56f64464b64fbee8630e`.

Zapis modelu: `R912→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.2", "description": "Ordinary Reaction Fire timing/eligibility", "needed_context": "8.2 Reaction Fire"}

Uzasadnienie modelu: Source refers to 8.2; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R912"], "blocks_full_result": true, "reason": "Ordinary Reaction Fire timing/eligibility is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. 8.2 potrzebne do legalnego momentu i wykonania reakcji, nie do odczytania lokalnego only.

Zapis gapu modelu: G-D912react — Ordinary Reaction Fire timing/eligibility is referenced but unavailable. Potrzebny kontekst: 8.2 Reaction Fire

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/3/text`, znaki [706,1320), SHA-256 wycinka `28cc98241b9178448cf90ad26f2bb63f07c4bde2cfa3575c1cc9635c16e2bed7`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.12 Elephant Screens: Elephants were quite vulnerable to
> missile attacks, and, to protect against this, armies surrounded
> each Elephant with its own light screen of skirmishers, usually
> archers represented by the small “a” on the counter. The firepower
> is much less than normal archer units, to account for the size of
> the screen and its tactical use.
> Elephant Screens can Missile Fire with Reaction Fire (8.2) only,
> using the Elephant Screen row on the MRRC. Elephant Screens
> have their own missile supply markers. Leader elephants do not
> have screens (they usually did, but they were too small to be a
> factor).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D913mounted

Źródło i dokładny zakres: 9.13: tower riders treated as Mounted Javelinists for Missile Fire purposes

Cel i granica dostępności: Mounted Javelinist characteristics/definition for Missile Fire, absent; actual resolution needs its table

Konieczność / zakres blokady: Przypisanie klasy jest znane; jej niepodane właściwości i wynik missile wymagają celu. Definition nie zatwierdza w jednej krawędzi całego lookupu tabeli.

Porównanie i propozycja: R913→Mounted Javelinists definition/explicit poparte ograniczoną klasyfikacją for Missile Fire purposes. Target request łączy definicję z tabelą; przyjąć rolę definicji i potrzebę wyniku osobno od nieodczytanej treści, bez nadawania wszystkich cech Mounted Javelinists słoniowi.

**first-001:** `/dependencies/50`; bajty [455966,456959), SHA-256 `4c12dad7714b21b5243f8562d0ea337e9db1ca288e1be76fd0d9f7d56833edf8`.

Zapis modelu: `R913→candidate`, `definition/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Mounted Javelinists", "description": "Mounted Javelinist missile characteristics", "needed_context": "Mounted Javelinist definition and missile resolution table"}

Uzasadnienie modelu: Source refers to Mounted Javelinists; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R913"], "blocks_full_result": true, "reason": "Mounted Javelinist missile characteristics is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Przypisanie klasy jest znane; jej niepodane właściwości i wynik missile wymagają celu. Definition nie zatwierdza w jednej krawędzi całego lookupu tabeli.

Zapis gapu modelu: G-D913mounted — Mounted Javelinist missile characteristics is referenced but unavailable. Potrzebny kontekst: Mounted Javelinist definition and missile resolution table

**context-01:** `/dependencies/50`; bajty [532572,533592), SHA-256 `213c2cdc238d7e26ba3258172530d074a974c3c28d596f11e45efab410f48599`.

Zapis modelu: `R913→candidate`, `definition/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Mounted Javelinists", "description": "Mounted Javelinist missile characteristics", "needed_context": "Mounted Javelinist definition and missile resolution table"}

Uzasadnienie modelu: Source refers to Mounted Javelinists; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R913"], "blocks_full_result": true, "reason": "Mounted Javelinist missile characteristics is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Przypisanie klasy jest znane; jej niepodane właściwości i wynik missile wymagają celu. Definition nie zatwierdza w jednej krawędzi całego lookupu tabeli.

Zapis gapu modelu: G-D913mounted — Mounted Javelinist missile characteristics is referenced but unavailable. Potrzebny kontekst: Mounted Javelinist definition and missile resolution table

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/3/text`, znaki [1320,1580), SHA-256 wycinka `090c25c1ed0964d2bcafd7b3117a51b92d84fd0a3f62476e2db6a9deea8d2982`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.13 Tower Riders: The riders atop elephants were armed with
> javelins and are treated as Mounted Javelinists for Missile Fire
> purposes. The Elephant unit may use Reaction Fire with both its
> javelins and its screen, with the player rolling separately for each.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D913react

Źródło i dokładny zakres: 9.13: may Reaction Fire with both javelins and screen, rolling separately for each

Cel i granica dostępności: Reaction Fire timing/eligibility procedure, absent

Konieczność / zakres blokady: Pełne wykonanie reakcji wymaga procedury; dwa odrębne rzuty są znane z9.13.

Porównanie i propozycja: R913→Reaction Fire procedure_use/explicit jest nazwanym użyciem operacji, zgodnie z decyzją o named use MLE, bez automatycznej zmiany innych etykiet. Oba wyniki zachowują both i separately. Nie usuwa zakazu jakiejkolwiek Reaction Fire podczas Rampage9.14.

**first-001:** `/dependencies/49`; bajty [454987,455960), SHA-256 `41ad1f246de30962eeb1a2180eabeb8201d42472751932f096eddccc5b25fa8a`.

Zapis modelu: `R913→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Reaction Fire", "description": "Reaction Fire eligibility/timing for javelins and screen", "needed_context": "Reaction Fire procedure"}

Uzasadnienie modelu: Source refers to Reaction Fire; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R913"], "blocks_full_result": true, "reason": "Reaction Fire eligibility/timing for javelins and screen is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełne wykonanie reakcji wymaga procedury; dwa odrębne rzuty są znane z9.13.

Zapis gapu modelu: G-D913react — Reaction Fire eligibility/timing for javelins and screen is referenced but unavailable. Potrzebny kontekst: Reaction Fire procedure

**context-01:** `/dependencies/49`; bajty [531565,532565), SHA-256 `9c11618b7a1f13c872f91c3ddf84d5cd8a4b679a8fb736dd89f00f8ee348e318`.

Zapis modelu: `R913→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Reaction Fire", "description": "Reaction Fire eligibility/timing for javelins and screen", "needed_context": "Reaction Fire procedure"}

Uzasadnienie modelu: Source refers to Reaction Fire; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R913"], "blocks_full_result": true, "reason": "Reaction Fire eligibility/timing for javelins and screen is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełne wykonanie reakcji wymaga procedury; dwa odrębne rzuty są znane z9.13.

Zapis gapu modelu: G-D913react — Reaction Fire eligibility/timing for javelins and screen is referenced but unavailable. Potrzebny kontekst: Reaction Fire procedure

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/3/text`, znaki [1320,1580), SHA-256 wycinka `090c25c1ed0964d2bcafd7b3117a51b92d84fd0a3f62476e2db6a9deea8d2982`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.13 Tower Riders: The riders atop elephants were armed with
> javelins and are treated as Mounted Javelinists for Missile Fire
> purposes. The Elephant unit may use Reaction Fire with both its
> javelins and its screen, with the player rolling separately for each.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D914OW

Źródło i dokładny zakres: 9.14: immediate Rampage priority except OW in face of rampaging Elephant (6.51)

Cel i granica dostępności: 6.51 OW eligibility/resolution, absent; local priority exception explicitly supplied

Konieczność / zakres blokady: Faktyczne wykonanie OW potrzebuje6.51. Sama możliwość przerwania priorytetu przez OW jest podana lokalnie i nie wymaga rekonstrukcji6.51.

Porównanie i propozycja: R914→6.51 exception/explicit i kierunek są poparte. Model/G-D914OW mają szerokie blocking=true, reason mówi o niedostarczonym wyjątku. Nie brakuje samego wyjątku priorytetu, brakuje zasad wykonania OW. Wydzielić SEM-017: przyjąć relację, ograniczyć blokadę do wykonania/kwalifikacji, nie lokalnej hierarchii.

**first-001:** `/dependencies/51`; bajty [456965,457910), SHA-256 `2783511113076fc854f3a522797b8f352d9f7bf2389e19c59db98dfe47b5e2f9`.

Zapis modelu: `R914→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.51", "description": "Orderly Withdrawal exception during Rampage", "needed_context": "6.51 including eligibility and resolution"}

Uzasadnienie modelu: Source refers to 6.51; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R914"], "blocks_full_result": true, "reason": "Orderly Withdrawal exception during Rampage is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Faktyczne wykonanie OW potrzebuje6.51. Sama możliwość przerwania priorytetu przez OW jest podana lokalnie i nie wymaga rekonstrukcji6.51.

Zapis gapu modelu: G-D914OW — Orderly Withdrawal exception during Rampage is referenced but unavailable. Potrzebny kontekst: 6.51 including eligibility and resolution

**context-01:** `/dependencies/51`; bajty [533599,534571), SHA-256 `0a94d267c9d5fbfaffd9b8cbe9d11e113a2c95afef2fbd5ae8c9e1bccec2ca8a`.

Zapis modelu: `R914→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.51", "description": "Orderly Withdrawal exception during Rampage", "needed_context": "6.51 including eligibility and resolution"}

Uzasadnienie modelu: Source refers to 6.51; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R914"], "blocks_full_result": true, "reason": "Orderly Withdrawal exception during Rampage is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Faktyczne wykonanie OW potrzebuje6.51. Sama możliwość przerwania priorytetu przez OW jest podana lokalnie i nie wymaga rekonstrukcji6.51.

Zapis gapu modelu: G-D914OW — Orderly Withdrawal exception during Rampage is referenced but unavailable. Potrzebny kontekst: 6.51 including eligibility and resolution

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/4/text`, znaki [413,586), SHA-256 wycinka `e61f74796ab21ad3af358ec1af911789c6dae86d14ff4af0ca6dbf5d22d3abef`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> Each Elephant Rampage is always resolved immediately, before
> any other game mechanic is addressed, except for Orderly With-
> drawal in face of the rampaging elephant (6.51).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D914casualty

Źródło i dokładny zakres: 9.14: casualty roll4.73 after Rampage for leader stacked with rampaging Elephant; off-map both eliminated

Cel i granica dostępności: 4.73 leader casualty procedure, absent

Konieczność / zakres blokady: Ustalenie przeżycia na mapie wymaga4.73. Off-map elimination i pozostanie ocalałego na końcowym heksie są określone lokalnie.

Porównanie i propozycja: R914→4.73 procedure_use/explicit poparte, oba wyniki wiążą rzut z leader jadącym na słoniu po zakończeniu Rampage. To inna sytuacja niż leader w heksie uderzonym przez słonia4.72. Przyjąć tę separację i potrzebę rzutu, nie wynik casualty.

**first-001:** `/dependencies/53`; bajty [458872,459789), SHA-256 `05463617bc0536387e3b5b142c3c97b2e76c43738b49c76004e6cd539939daa7`.

Zapis modelu: `R914→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "4.73", "description": "Stacked leader casualty roll after Rampage", "needed_context": "4.73"}

Uzasadnienie modelu: Source refers to 4.73; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R914"], "blocks_full_result": true, "reason": "Stacked leader casualty roll after Rampage is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Ustalenie przeżycia na mapie wymaga4.73. Off-map elimination i pozostanie ocalałego na końcowym heksie są określone lokalnie.

Zapis gapu modelu: G-D914casualty — Stacked leader casualty roll after Rampage is referenced but unavailable. Potrzebny kontekst: 4.73

**context-01:** `/dependencies/53`; bajty [535562,536506), SHA-256 `b17c49949d4403e8f666691b625e432e9854305e446cecc805cd6a9a12a65462`.

Zapis modelu: `R914→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "4.73", "description": "Stacked leader casualty roll after Rampage", "needed_context": "4.73"}

Uzasadnienie modelu: Source refers to 4.73; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R914"], "blocks_full_result": true, "reason": "Stacked leader casualty roll after Rampage is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Ustalenie przeżycia na mapie wymaga4.73. Off-map elimination i pozostanie ocalałego na końcowym heksie są określone lokalnie.

Zapis gapu modelu: G-D914casualty — Stacked leader casualty roll after Rampage is referenced but unavailable. Potrzebny kontekst: 4.73

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/4/text`, znaki [1984,2309), SHA-256 wycinka `3336ebb278b746b7d37ab67a94f2de6a65c999e3026df0aabbdbcf3ace40b1b6`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> A leader stacked with a rampaging Elephant goes along with
> the Elephant on the Rampage. When the Rampage ends, the
> player rolls for a leader casualty (4.73). If the leader survives,
> he remains on the map where the Elephant ended the Rampage.
> If the Elephant Rampages off the map, both the Elephant and
> leader are eliminated.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D914compass

Źródło i dokładny zakres: 9.14 table1–6: map compass supplies Rampage direction by hexside; caption only example

Cel i granica dostępności: Actual selected battle map compass mapping, absent

Konieczność / zakres blokady: Kierunek na konkretnej mapie dla1–6 potrzebuje compass. Inne wiersze tabeli mają własne warunki kierunku/końca, a obraz nie jest mapą każdej bitwy.

Porównanie i propozycja: N914table→map compass definition/explicit poparte jako mapa orientacji liczb/kierunków, bez treści wybranego celu. Zachowano vertex versus hexside. Blokadę ograniczyć do gałęzi1–6 i realnej mapy; nie blokuje eliminacji na0 Leader lub późniejszym7–9. Definicyjna rola mapping nie zatwierdza aliasu/mapy.

**first-001:** `/dependencies/54`; bajty [459795,460817), SHA-256 `2329eef178fde36656363601a0b0a8e0c12bd5ee1a33b15a6b1197b0e34d607e`.

Zapis modelu: `N914table→candidate`, `definition/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Compass on the map", "description": "Battle-specific directions for 1–6 Rampage rolls", "needed_context": "Actual selected battle map compass"}

Uzasadnienie modelu: Source refers to Compass on the map; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["N914table"], "blocks_full_result": true, "reason": "Battle-specific directions for 1–6 Rampage rolls is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Kierunek na konkretnej mapie dla1–6 potrzebuje compass. Inne wiersze tabeli mają własne warunki kierunku/końca, a obraz nie jest mapą każdej bitwy.

Zapis gapu modelu: G-D914compass — Battle-specific directions for 1–6 Rampage rolls is referenced but unavailable. Potrzebny kontekst: Actual selected battle map compass

**context-01:** `/dependencies/54`; bajty [536513,537563), SHA-256 `a6a4251c69eb2d2d05643f642fbb1e5ebf93486528dc7879d21a18040e6da46c`.

Zapis modelu: `N914table→candidate`, `definition/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Compass on the map", "description": "Battle-specific directions for 1–6 Rampage rolls", "needed_context": "Actual selected battle map compass"}

Uzasadnienie modelu: Source refers to Compass on the map; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["N914table"], "blocks_full_result": true, "reason": "Battle-specific directions for 1–6 Rampage rolls is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Kierunek na konkretnej mapie dla1–6 potrzebuje compass. Inne wiersze tabeli mają własne warunki kierunku/końca, a obraz nie jest mapą każdej bitwy.

Zapis gapu modelu: G-D914compass — Battle-specific directions for 1–6 Rampage rolls is referenced but unavailable. Potrzebny kontekst: Actual selected battle map compass

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/3/text`, znaki [2147,2392), SHA-256 wycinka `e53ede7c21557cb91896dab56201b72d89c28afa57f08e0ccc56ba90e5921e2b`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/4/text`, znaki [586,745), SHA-256 wycinka `ae6cb090c9f2302e5152be41079fb2629aaf2788f6266b914d8f4e34651e1f08`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> EXAMPLE: The above diagram shows the elephant unit refaced
> after a Rampage die roll of 1. This is just an example; use the
> compass on the map for each battle.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D914leaderwithdraw

Źródło i dokładny zakres: 9.14: leader in intended impacted hex dies without die roll if cannot withdraw4.72

Cel i granica dostępności: 4.72 withdrawal eligibility/execution, absent

Konieczność / zakres blokady: Ocena can withdraw wymaga4.72; zadane cannot withdraw pozwala zastosować lokalną automatyczną śmierć bez rzutu.

Porównanie i propozycja: R914→4.72 procedure_use/explicit poprawnie oznacza procedurę warunkującą gałąź. Dotyczy leader w zajętym heksie na drodze słonia, nie leader stacked with rampaging Elephant ocenianego4.73. Poparte w obu wynikach bez nadawania zasad4.72.

**first-001:** `/dependencies/52`; bajty [457916,458866), SHA-256 `eecaac90550a327244c90f476f2aaa94654edff3ebed80f79ca55d09f942ebd0`.

Zapis modelu: `R914→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "4.72", "description": "Leader withdrawal eligibility before automatic death", "needed_context": "4.72"}

Uzasadnienie modelu: Source refers to 4.72; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R914"], "blocks_full_result": true, "reason": "Leader withdrawal eligibility before automatic death is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Ocena can withdraw wymaga4.72; zadane cannot withdraw pozwala zastosować lokalną automatyczną śmierć bez rzutu.

Zapis gapu modelu: G-D914leaderwithdraw — Leader withdrawal eligibility before automatic death is referenced but unavailable. Potrzebny kontekst: 4.72

**context-01:** `/dependencies/52`; bajty [534578,535555), SHA-256 `8b12d47069daa517f78d4b3cc5d49b72005429aa62462ad1d7cf6a6257e75431`.

Zapis modelu: `R914→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "4.72", "description": "Leader withdrawal eligibility before automatic death", "needed_context": "4.72"}

Uzasadnienie modelu: Source refers to 4.72; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R914"], "blocks_full_result": true, "reason": "Leader withdrawal eligibility before automatic death is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Ocena can withdraw wymaga4.72; zadane cannot withdraw pozwala zastosować lokalną automatyczną śmierć bez rzutu.

Zapis gapu modelu: G-D914leaderwithdraw — Leader withdrawal eligibility before automatic death is referenced but unavailable. Potrzebny kontekst: 4.72

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/4/text`, znaki [745,1625), SHA-256 wycinka `26f3e8360adc4db77c8069b65ad8df6dc1aee64b6d297aa665ba92cfd0e11c11`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> A rampaging Elephant and any stacked leader with it always
> attempt to move 3 hexes per directional die roll in the indicated
> direction until it either moves off the map or is otherwise elimi-
> nated. If a rampaging Elephant unit would enter a hex occupied
> by a unit, whether enemy or friendly, the Elephant unit stops in
> the adjacent hex and the unit incurs 1 Cohesion Hit if the Elephant
> would have entered through a Front hex or 2 Cohesion Hits if it
> would have entered through a Flank or Rear hex. A cavalry unit
> incurs 2 Cohesion Hits regardless of the angle.
> If the affected units are a stack, both units receive the Cohesion
> Hits. If there is a leader in the hex (alone or stacked with a unit),
> and he cannot withdraw (see 4.72), he is tragically impaled on
> the elephant’s tusks, tossed high in the air, and then crushed to
> death under its feet. All that without a die roll!
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D915superiority

Źródło i dokładny zakres: 9.15: cavalry may attack Elephant Flank/Rear but gains no usual Attack Superiority

Cel i granica dostępności: General Attack Superiority effects, absent;8.72 chart purpose available only descriptively

Konieczność / zakres blokady: Brak numeric effects blokuje inne obliczenia general combat. Zakaz przyznania AS tej konkretnej kawalerii jest znany bez tabeli wartości.

Porównanie i propozycja: R915→usual AS exception/explicit poparte lokalnym do not gain. Blocking=true/G opisują brak całej ogólnej reguły, lecz nie dowodzą blokady zakazu AS. SEM-017: przyjąć wyjątek; blokadę stosować do nieznanych dalszych skutków, nie do odpowiedzi czy ta kawaleria dostaje AS.

**first-001:** `/dependencies/55`; bajty [460823,461910), SHA-256 `2c97e5aaa751de5025942f3aab2bb569d66d50579d6903b70ef27edd4815b8a8`.

Zapis modelu: `R915→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "usual Attack Superiority", "description": "General Attack Superiority rule qualified by cavalry/Elephant attack restriction", "needed_context": "Position/Attack Superiority definitions and numeric effects"}

Uzasadnienie modelu: Source refers to usual Attack Superiority; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R915"], "blocks_full_result": true, "reason": "General Attack Superiority rule qualified by cavalry/Elephant attack restriction is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Brak numeric effects blokuje inne obliczenia general combat. Zakaz przyznania AS tej konkretnej kawalerii jest znany bez tabeli wartości.

Zapis gapu modelu: G-D915superiority — General Attack Superiority rule qualified by cavalry/Elephant attack restriction is referenced but unavailable. Potrzebny kontekst: Position/Attack Superiority definitions and numeric effects

**context-01:** `/dependencies/55`; bajty [537570,538684), SHA-256 `0934f70d7e8f73f2bceef32f48e7b3192e5224c3022d65b3973e103e1538e923`.

Zapis modelu: `R915→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "usual Attack Superiority", "description": "General Attack Superiority rule qualified by cavalry/Elephant attack restriction", "needed_context": "Position/Attack Superiority definitions and numeric effects"}

Uzasadnienie modelu: Source refers to usual Attack Superiority; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R915"], "blocks_full_result": true, "reason": "General Attack Superiority rule qualified by cavalry/Elephant attack restriction is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Brak numeric effects blokuje inne obliczenia general combat. Zakaz przyznania AS tej konkretnej kawalerii jest znany bez tabeli wartości.

Zapis gapu modelu: G-D915superiority — General Attack Superiority rule qualified by cavalry/Elephant attack restriction is referenced but unavailable. Potrzebny kontekst: Position/Attack Superiority definitions and numeric effects

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/5/text`, znaki [331,875), SHA-256 wycinka `3b3bd2be445ca417fd2cafc7d52fb80d85c004920f90b8b4c2046fb18b6a58bc`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.15 Cavalry vs. Elephants: Cavalry units may never voluntarily
> move into the ZOC of an enemy Elephant unit. They may move
> into or through an enemy Elephant’s Flank or Rear hexes but
> at the cost of 2 Cohesion Hits for each such hex entered. This
> cohesion penalty also applies if the cavalry unit is forced to enter
> an Elephant ZOC. Cavalry may never attack an enemy Elephant
> through the latter’s Front hexes; they may attack through the
> Elephant unit’s Flank or Rear hexes, but they do not gain the
> usual Attack Superiority for such an attack.
> 

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [152,492), SHA-256 wycinka `0503283ab344c8f09740c58b52f5fae5c2845f8c7e62a433804062f9f7402647`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 8.72 The Shock Superiority Chart: This chart is used to
> compare the superiority (if any) of one type of unit compared
> to another, depending on which side is attacking or defending.
> Always read down the column—from the Attacker’s point of
> view. (Reading across, by row, gives a “false” result.) Superiority
> is used to augment Cohesion Hits.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D916OW

Źródło i dokładny zakres: 9.16: Elephant moves non-adjacent→adjacent to cavalry, mandatory attempt OW; excludes Leader Elephant

Cel i granica dostępności: OW eligibility/paths/costs, absent

Konieczność / zakres blokady: Brak OW uniemożliwia ustalenie rzeczywistej możliwości i wykonania wycofania. Jeśli cannot withdraw jest zadane, lokalna gałąź testu jest oceniana osobno.

Porównanie i propozycja: R916→OW procedure_use/explicit zgodne z must attempt. Oba wyniki zachowują no Reaction Fire if can withdraw oraz wyjątek Leader Elephant. Nie zamyka wcześniejszego minimum1/DR<=TQ aniEXP-017, nie naprawiaE916.

**first-001:** `/dependencies/56`; bajty [461916,462881), SHA-256 `7561986e666489d58bee19ec254573774cb3d4897e050b2b24ef7d26208ea4aa`.

Zapis modelu: `R916→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Orderly Withdrawal", "description": "Mandatory cavalry withdrawal procedure", "needed_context": "Orderly Withdrawal eligibility, paths and costs"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R916"], "blocks_full_result": true, "reason": "Mandatory cavalry withdrawal procedure is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Brak OW uniemożliwia ustalenie rzeczywistej możliwości i wykonania wycofania. Jeśli cannot withdraw jest zadane, lokalna gałąź testu jest oceniana osobno.

Zapis gapu modelu: G-D916OW — Mandatory cavalry withdrawal procedure is referenced but unavailable. Potrzebny kontekst: Orderly Withdrawal eligibility, paths and costs

**context-01:** `/dependencies/56`; bajty [538691,539683), SHA-256 `407dc853953054823ba0e36015fe2867e0c0b7eda27023f0de835bb0b7e5c397`.

Zapis modelu: `R916→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Orderly Withdrawal", "description": "Mandatory cavalry withdrawal procedure", "needed_context": "Orderly Withdrawal eligibility, paths and costs"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R916"], "blocks_full_result": true, "reason": "Mandatory cavalry withdrawal procedure is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Brak OW uniemożliwia ustalenie rzeczywistej możliwości i wykonania wycofania. Jeśli cannot withdraw jest zadane, lokalna gałąź testu jest oceniana osobno.

Zapis gapu modelu: G-D916OW — Mandatory cavalry withdrawal procedure is referenced but unavailable. Potrzebny kontekst: Orderly Withdrawal eligibility, paths and costs

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/5/text`, znaki [875,1472), SHA-256 wycinka `b94907d25d668fc6844756b3e1739e2e2f204dc9d332372e23baccec265e8795`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

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
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D917position

Źródło i dokładny zakres: 9.17: Elephant vs Elephant neither side Position Superiority; no AS for Flank/Rear attack

Cel i granica dostępności: Position/Attack Superiority general definitions/effects, absent

Konieczność / zakres blokady: Podany zakaz obu stron i konkretnej AS nie wymaga liczbowych efektów przy zadanym Elephant-vs-Elephant. Pozostały wynik walki może wymagać tabeli.

Porównanie i propozycja: R917→candidate Position/Attack exception/explicit odpowiada obu lokalnym sformułowaniom; nie potwierdza ich zewnętrznej tożsamości/aliasu. SEM-017: szerokie blocking=true nie powinno blokować znanego zakazu. Przyjąć wyjątek w tym zakresie bez pełnej general Superiority.

**first-001:** `/dependencies/57`; bajty [462887,464004), SHA-256 `0ce96bd3c947272c658299593bd1b2ac360c551af10d7c580ba4bc51f43c7de0`.

Zapis modelu: `R917→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Position Superiority / Attack Superiority", "description": "General Position/Attack Superiority qualified by Elephant-versus-Elephant prohibition", "needed_context": "Position/Attack Superiority definitions and effects"}

Uzasadnienie modelu: Source refers to Position Superiority / Attack Superiority; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R917"], "blocks_full_result": true, "reason": "General Position/Attack Superiority qualified by Elephant-versus-Elephant prohibition is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Podany zakaz obu stron i konkretnej AS nie wymaga liczbowych efektów przy zadanym Elephant-vs-Elephant. Pozostały wynik walki może wymagać tabeli.

Zapis gapu modelu: G-D917position — General Position/Attack Superiority qualified by Elephant-versus-Elephant prohibition is referenced but unavailable. Potrzebny kontekst: Position/Attack Superiority definitions and effects

**context-01:** `/dependencies/57`; bajty [539690,540834), SHA-256 `32e2ec477d46b6be8d39a353d286d76b867dad76059a1963608f2dd2603582ae`.

Zapis modelu: `R917→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Position Superiority / Attack Superiority", "description": "General Position/Attack Superiority qualified by Elephant-versus-Elephant prohibition", "needed_context": "Position/Attack Superiority definitions and effects"}

Uzasadnienie modelu: Source refers to Position Superiority / Attack Superiority; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R917"], "blocks_full_result": true, "reason": "General Position/Attack Superiority qualified by Elephant-versus-Elephant prohibition is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Podany zakaz obu stron i konkretnej AS nie wymaga liczbowych efektów przy zadanym Elephant-vs-Elephant. Pozostały wynik walki może wymagać tabeli.

Zapis gapu modelu: G-D917position — General Position/Attack Superiority qualified by Elephant-versus-Elephant prohibition is referenced but unavailable. Potrzebny kontekst: Position/Attack Superiority definitions and effects

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/5/text`, znaki [1472,1700), SHA-256 wycinka `013297c76e7875ab7a739a0e4aeebd7d90baac4c0300a82a6010900d32a8627a`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.17 In any instance where Elephant units attack other Elephant
> units, neither side may gain Position Superiority. Thus, one
> Elephant attacking another Elephant through the latter’s Flank/
> Rear does not gain Attack Superiority.
> 

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [152,492), SHA-256 wycinka `0503283ab344c8f09740c58b52f5fae5c2845f8c7e62a433804062f9f7402647`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 8.72 The Shock Superiority Chart: This chart is used to
> compare the superiority (if any) of one type of unit compared
> to another, depending on which side is attacking or defending.
> Always read down the column—from the Attacker’s point of
> view. (Reading across, by row, gives a “false” result.) Superiority
> is used to augment Cohesion Hits.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D919clash

Źródło i dokładny zakres: 9.19: Indian vs African rule in addition to Clash chart notes

Cel i granica dostępności: Actual Clash of Spears and Swords notes/cells including Elephant distinctions, absent

Konieczność / zakres blokady: Pełne rozstrzygnięcie może wymagać notes/column. Lokalny+1 do African Pre-Shock pozostaje znany; opis8.73 nie zawiera notes.

Porównanie i propozycja: R919→Clash notes table_use/explicit poparte addytywną rolą notes w rozstrzygnięciu, nie tylko wzmianką o nazwie. N873 opisuje wybór kolumny, nie daje wymaganych notes. Przyjąć wymaganie chart w pełnym wyniku, nie zawartość/aliasy lub konieczność lookupu do samego+1.

**first-001:** `/dependencies/60`; bajty [466015,467053), SHA-256 `1fa54f24d5fd43511577e8727fce95980d0bbab7e99f491866a732ee373f78fe`.

Zapis modelu: `R919→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "notes on the Clash of Spears and Swords Chart", "description": "Indian/African Elephant chart notes", "needed_context": "Clash of Spears and Swords Chart including Elephant distinctions/notes"}

Uzasadnienie modelu: Source refers to notes on the Clash of Spears and Swords Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R919"], "blocks_full_result": true, "reason": "Indian/African Elephant chart notes is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełne rozstrzygnięcie może wymagać notes/column. Lokalny+1 do African Pre-Shock pozostaje znany; opis8.73 nie zawiera notes.

Zapis gapu modelu: G-D919clash — Indian/African Elephant chart notes is referenced but unavailable. Potrzebny kontekst: Clash of Spears and Swords Chart including Elephant distinctions/notes

**context-01:** `/dependencies/60`; bajty [542902,543967), SHA-256 `2fde0071d554d130555be7f352f1530f513aa69b4ce63279573c08105d2c53f9`.

Zapis modelu: `R919→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "notes on the Clash of Spears and Swords Chart", "description": "Indian/African Elephant chart notes", "needed_context": "Clash of Spears and Swords Chart including Elephant distinctions/notes"}

Uzasadnienie modelu: Source refers to notes on the Clash of Spears and Swords Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R919"], "blocks_full_result": true, "reason": "Indian/African Elephant chart notes is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełne rozstrzygnięcie może wymagać notes/column. Lokalny+1 do African Pre-Shock pozostaje znany; opis8.73 nie zawiera notes.

Zapis gapu modelu: G-D919clash — Indian/African Elephant chart notes is referenced but unavailable. Potrzebny kontekst: Clash of Spears and Swords Chart including Elephant distinctions/notes

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/5/text`, znaki [1855,2120), SHA-256 wycinka `53f25ae70e3ce1cc0a11f8af97f3f5703707fc657fb9b0b13d02100313fb9d09`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.19 Indians vs. Africans: In addition to the notes on the Clash of
> Spears and Swords and Shock Superiority Charts, the following
> rule is in effect when Indian Elephants fight African Elephants:
> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).
> 

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [492,649), SHA-256 wycinka `dc0bfef48bbb85325925b9a024bac62bb800387081f1df96ca11f41b95f8e9f0`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 8.73 Clash of Spears and Swords Chart: This chart is used
> to determine which Column will be used on the Shock Combat
> Results Table (subject to adjustments).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D919pre

Źródło i dokładny zakres: 9.19: African Elephants+1 DRM to Pre-Shock die rolls8.43 when fighting Indian Elephants

Cel i granica dostępności: 8.43 Pre-Shock procedure, absent

Konieczność / zakres blokady: Procedura potrzebna do pełnego testu; przy zadanym właściwym rzucie kierunek+1 i stronaAfrican są znane.

Porównanie i propozycja: R919→8.43 procedure_use/explicit poparte numerem i rolą. Nie przekształca+1 w ogólny modifier do całego Shock lub dla obu stron. Przyjąć wymaganie i lokalne zawężenie; zakres całego source record poza relacją.

**first-001:** `/dependencies/59`; bajty [465085,466009), SHA-256 `b0f67748e7541b061f298d687b5970a754a5dac62ed2f2fd42c9ca15b36ebd17`.

Zapis modelu: `R919→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.43", "description": "Pre-Shock roll procedure to receive African modifier", "needed_context": "8.43"}

Uzasadnienie modelu: Source refers to 8.43; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R919"], "blocks_full_result": true, "reason": "Pre-Shock roll procedure to receive African modifier is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Procedura potrzebna do pełnego testu; przy zadanym właściwym rzucie kierunek+1 i stronaAfrican są znane.

Zapis gapu modelu: G-D919pre — Pre-Shock roll procedure to receive African modifier is referenced but unavailable. Potrzebny kontekst: 8.43

**context-01:** `/dependencies/59`; bajty [541944,542895), SHA-256 `e5c8345ad838ee31af82a2165f56c957c0e25c1daa4634d036577089c5ff1a5e`.

Zapis modelu: `R919→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.43", "description": "Pre-Shock roll procedure to receive African modifier", "needed_context": "8.43"}

Uzasadnienie modelu: Source refers to 8.43; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R919"], "blocks_full_result": true, "reason": "Pre-Shock roll procedure to receive African modifier is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Procedura potrzebna do pełnego testu; przy zadanym właściwym rzucie kierunek+1 i stronaAfrican są znane.

Zapis gapu modelu: G-D919pre — Pre-Shock roll procedure to receive African modifier is referenced but unavailable. Potrzebny kontekst: 8.43

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/5/text`, znaki [1855,2120), SHA-256 wycinka `53f25ae70e3ce1cc0a11f8af97f3f5703707fc657fb9b0b13d02100313fb9d09`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.19 Indians vs. Africans: In addition to the notes on the Clash of
> Spears and Swords and Shock Superiority Charts, the following
> rule is in effect when Indian Elephants fight African Elephants:
> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D919shock

Źródło i dokładny zakres: 9.19: Indian vs African addition to Shock Superiority chart notes

Cel i granica dostępności: Actual Shock Superiority chart notes/cells, absent

Konieczność / zakres blokady: Pełna przewaga potrzebuje chart notes;8.72 podaje tylko rolę i czytanie attacker column. Lokalny+1 nie czeka na tabelę.

Porównanie i propozycja: R919→Shock Superiority notes table_use/explicit zgodne z potrzebą chart w pełnej walce. Zachować odrębność Clash chart/CRT/Superiority. Przyjąć nazwane wymaganie, nie wartości lub pełny wynik; już przyjęte opisowe D919chartdef nie dostarcza notes.

**first-001:** `/dependencies/61`; bajty [467059,468094), SHA-256 `b1e04abfcffe4bc13d21e5862f058a17cedd9cf8c2ef8a421d29c35c6d171601`.

Zapis modelu: `R919→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "notes on the Shock Superiority Chart", "description": "Indian/African Elephant superiority chart notes", "needed_context": "Shock Superiority Chart including Elephant distinctions/notes"}

Uzasadnienie modelu: Source refers to notes on the Shock Superiority Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R919"], "blocks_full_result": true, "reason": "Indian/African Elephant superiority chart notes is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełna przewaga potrzebuje chart notes;8.72 podaje tylko rolę i czytanie attacker column. Lokalny+1 nie czeka na tabelę.

Zapis gapu modelu: G-D919shock — Indian/African Elephant superiority chart notes is referenced but unavailable. Potrzebny kontekst: Shock Superiority Chart including Elephant distinctions/notes

**context-01:** `/dependencies/61`; bajty [543974,545036), SHA-256 `90769189ca5048ffb541220509179de80ec1c4eb98c302fd096ada4318cdb7af`.

Zapis modelu: `R919→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "notes on the Shock Superiority Chart", "description": "Indian/African Elephant superiority chart notes", "needed_context": "Shock Superiority Chart including Elephant distinctions/notes"}

Uzasadnienie modelu: Source refers to notes on the Shock Superiority Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R919"], "blocks_full_result": true, "reason": "Indian/African Elephant superiority chart notes is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełna przewaga potrzebuje chart notes;8.72 podaje tylko rolę i czytanie attacker column. Lokalny+1 nie czeka na tabelę.

Zapis gapu modelu: G-D919shock — Indian/African Elephant superiority chart notes is referenced but unavailable. Potrzebny kontekst: Shock Superiority Chart including Elephant distinctions/notes

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/5/text`, znaki [1855,2120), SHA-256 wycinka `53f25ae70e3ce1cc0a11f8af97f3f5703707fc657fb9b0b13d02100313fb9d09`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.19 Indians vs. Africans: In addition to the notes on the Clash of
> Spears and Swords and Shock Superiority Charts, the following
> rule is in effect when Indian Elephants fight African Elephants:
> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).
> 

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [152,492), SHA-256 wycinka `0503283ab344c8f09740c58b52f5fae5c2845f8c7e62a433804062f9f7402647`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 8.72 The Shock Superiority Chart: This chart is used to
> compare the superiority (if any) of one type of unit compared
> to another, depending on which side is attacking or defending.
> Always read down the column—from the Attacker’s point of
> view. (Reading across, by row, gives a “false” result.) Superiority
> is used to augment Cohesion Hits.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D921OW

Źródło i dokładny zakres: 9.21: SK OW up to2 hexes before same/lower MA; SK Rear Hits, Velites Flank/Rear Hits

Cel i granica dostępności: General OW procedure and normal costs, absent

Konieczność / zakres blokady: Pełne wycofanie wymaga normalnej procedury. Lokalny dystans2, porównanieMA i warunki kierunku są znane; konkretne normalne Hits/costs nie są podane.

Porównanie i propozycja: R921→OW modification/explicit poparte modyfikacją odległości/MA i kosztów kierunkowych. Nie daje dowolnej legalnej ścieżki lub darmowego OW Velites z Rear. Przyjąć modyfikację oraz ograniczoną blokadę pełnego wykonania, nie blokadę znanych warunków.

**first-001:** `/dependencies/62`; bajty [468100,469141), SHA-256 `80ab1224bf1b51e8765d74dddb5ebca7692d3948bc57604dd898864400a971a0`.

Zapis modelu: `R921→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Orderly Withdrawal", "description": "General OW modified by Skirmisher distance/MA and directional penalties", "needed_context": "Orderly Withdrawal procedure and normal Cohesion Hit costs"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R921"], "blocks_full_result": true, "reason": "General OW modified by Skirmisher distance/MA and directional penalties is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełne wycofanie wymaga normalnej procedury. Lokalny dystans2, porównanieMA i warunki kierunku są znane; konkretne normalne Hits/costs nie są podane.

Zapis gapu modelu: G-D921OW — General OW modified by Skirmisher distance/MA and directional penalties is referenced but unavailable. Potrzebny kontekst: Orderly Withdrawal procedure and normal Cohesion Hit costs

**context-01:** `/dependencies/62`; bajty [545043,546111), SHA-256 `19190e3289a1f4f7f43fd82edf6375d367de8c1290cbd64a43ec24a30d691272`.

Zapis modelu: `R921→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Orderly Withdrawal", "description": "General OW modified by Skirmisher distance/MA and directional penalties", "needed_context": "Orderly Withdrawal procedure and normal Cohesion Hit costs"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R921"], "blocks_full_result": true, "reason": "General OW modified by Skirmisher distance/MA and directional penalties is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełne wycofanie wymaga normalnej procedury. Lokalny dystans2, porównanieMA i warunki kierunku są znane; konkretne normalne Hits/costs nie są podane.

Zapis gapu modelu: G-D921OW — General OW modified by Skirmisher distance/MA and directional penalties is referenced but unavailable. Potrzebny kontekst: Orderly Withdrawal procedure and normal Cohesion Hit costs

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/6/text`, znaki [748,1134), SHA-256 wycinka `6b9ff33c6cee81efe4a258b33df70d1de2677019352fffbbc3808246e994440c`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.21 Orderly Withdrawal: Skirmishers may Orderly
> Withdraw up to 2 hexes before any units whose MA
> is the same or less (i.e., all infantry units), regardless
> of the MA differential. The only time Skirmishers
> incur Cohesion Hits when using OW is after being approached
> from a Rear hex. The only time Velites incur Cohesion Hits from
> OW is after being approached from a Flank or Rear hex.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D922missile

Źródło i dokładny zakres: 9.22: +2 Missile Fire DR whenever SK is target

Cel i granica dostępności: Base Missile Fire procedure/results chart, absent

Konieczność / zakres blokady: Wynik strzału wymaga base/table. Przy zadanym DR lokalne dodanie2 nie wymaga odczytu nieznanej tabeli.

Porównanie i propozycja: R922→Missile Fire DR modification/explicit zgodne z nazwanym modyfikowanym rzutem. To+2 gdy celemSK, nie bonus dla strzelającegoSK, nie modyfikacja samychHits. Przyjąć rolę i potrzebę pełnego strzału; H&D zakazy osobno.

**first-001:** `/dependencies/63`; bajty [469147,470139), SHA-256 `591716eb6af883fa29d76a75b7b7f05dc34362571c706fd81a2ec0c1dcdf7c41`.

Zapis modelu: `R922→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Missile Fire DR", "description": "Base missile resolution to receive Skirmisher modifier", "needed_context": "Missile Fire procedure and result chart"}

Uzasadnienie modelu: Source refers to Missile Fire DR; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R922"], "blocks_full_result": true, "reason": "Base missile resolution to receive Skirmisher modifier is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Wynik strzału wymaga base/table. Przy zadanym DR lokalne dodanie2 nie wymaga odczytu nieznanej tabeli.

Zapis gapu modelu: G-D922missile — Base missile resolution to receive Skirmisher modifier is referenced but unavailable. Potrzebny kontekst: Missile Fire procedure and result chart

**context-01:** `/dependencies/63`; bajty [546118,547137), SHA-256 `22e597444d430d342443deaa6db2cec9e7245dd51c986878742619d0eb631e6f`.

Zapis modelu: `R922→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Missile Fire DR", "description": "Base missile resolution to receive Skirmisher modifier", "needed_context": "Missile Fire procedure and result chart"}

Uzasadnienie modelu: Source refers to Missile Fire DR; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R922"], "blocks_full_result": true, "reason": "Base missile resolution to receive Skirmisher modifier is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Wynik strzału wymaga base/table. Przy zadanym DR lokalne dodanie2 nie wymaga odczytu nieznanej tabeli.

Zapis gapu modelu: G-D922missile — Base missile resolution to receive Skirmisher modifier is referenced but unavailable. Potrzebny kontekst: Missile Fire procedure and result chart

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/6/text`, znaki [1134,1378), SHA-256 wycinka `09ec8487704f5a767f9741566027c864613d277a08c82fcc36e1839d66645c3c`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.22 Missile Fire: There is a +2 DRM to the Missile Fire DR
> whenever a Skirmisher unit is the target. Skirmisher and Light
> Infantry Archers (Class A) cannot use H&D fire. Light Cavalry
> (all missile classes) cannot use H&D against Skirmishers..
> 

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [22,152), SHA-256 wycinka `6d536a1df692b011b2266ea6a564038d9b9444918a402e57a151b593e89eb00e`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 8.71 The Missile Range and Results Chart: This table is used
> to determine the strength of a missile unit firing at a given range.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D923pre

Źródło i dokładny zakres: 9.23: attacker vs SK alone no check; PH/HI/LG defending Front LI no check, attacking LI still checks; reverse not exempt

Cel i granica dostępności: General Pre-Shock TQ/marker procedure, absent

Konieczność / zakres blokady: Same lokalne zwolnienia przy zadanych klasach/kierunku są rozstrzygalne bez procedury. Rzut dla niezwolnionych jednostek i realna kwalifikacja wymagają ogólnego kontekstu.

Porównanie i propozycja: R923→Pre-Shock exception/explicit zachowuje SKalone, nonreciprocalFrontLI i attackingLI still check. G-D923pre/blocks=true szeroko przypisaneR923 nie są dowodem, że zwolnienie jest nieznane. SEM-017: przyjąć wyjątki; blokada dotyczy dalszego wykonania niezwolnionych testów, nie samego no-check.

**first-001:** `/dependencies/65`; bajty [471124,472135), SHA-256 `4cf94cf694f0e376a2a50f56dfe9ae4f961249b2e6100de7a4a7434eb3b23de0`.

Zapis modelu: `R923→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Pre-Shock TQ", "description": "General Pre-Shock checks qualified by SK and LI front-attack exemptions", "needed_context": "Pre-Shock TQ procedure/marker definitions"}

Uzasadnienie modelu: Source refers to Pre-Shock TQ; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R923"], "blocks_full_result": true, "reason": "General Pre-Shock checks qualified by SK and LI front-attack exemptions is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Same lokalne zwolnienia przy zadanych klasach/kierunku są rozstrzygalne bez procedury. Rzut dla niezwolnionych jednostek i realna kwalifikacja wymagają ogólnego kontekstu.

Zapis gapu modelu: G-D923pre — General Pre-Shock checks qualified by SK and LI front-attack exemptions is referenced but unavailable. Potrzebny kontekst: Pre-Shock TQ procedure/marker definitions

**context-01:** `/dependencies/65`; bajty [548151,549189), SHA-256 `633d4a747e7b738d167ae1c43bb288f2d7fa4fc05cceaa407ec1f91931383cef`.

Zapis modelu: `R923→candidate`, `exception/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Pre-Shock TQ", "description": "General Pre-Shock checks qualified by SK and LI front-attack exemptions", "needed_context": "Pre-Shock TQ procedure/marker definitions"}

Uzasadnienie modelu: Source refers to Pre-Shock TQ; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R923"], "blocks_full_result": true, "reason": "General Pre-Shock checks qualified by SK and LI front-attack exemptions is not fully supplied; no missing content reconstructed."}

Ocena: separate_block_scope_decision. Same lokalne zwolnienia przy zadanych klasach/kierunku są rozstrzygalne bez procedury. Rzut dla niezwolnionych jednostek i realna kwalifikacja wymagają ogólnego kontekstu.

Zapis gapu modelu: G-D923pre — General Pre-Shock checks qualified by SK and LI front-attack exemptions is referenced but unavailable. Potrzebny kontekst: Pre-Shock TQ procedure/marker definitions

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/6/text`, znaki [1378,2431), SHA-256 wycinka `7a41ae70411a97363939e936161395afdacc50ef731d83ff5fc83badfabd23b5`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.23 Shock Combat: Skirmishers have the following restrictions
> when involved in Shock Combat:
> • Skirmishers cannot Shock attack.
> • All units that Shock attack Skirmishers alone do not have
> to make a Pre-Shock TQ even if they have SHOCK MUST
> CHECK TQ markers.
> • If a Skirmisher unit is defending in coordination with any other
> unit type, the other Type must be chosen as the defender. The
> Size rating of the Skirmisher is ignored.
> • Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.
> • Phalanx (PH), Heavy Infantry (HI), and Legion Infantry (LG)
> units that are attacked from a Front hex by Light Infantry (LI)
> do not undergo a Pre-Shock TQ check even if the attackers have
> SHOCK MUST CHECK TQ markers, though the attacking LI
> still do. The reverse is not true; PH, HI and LG do undergo a
> Pre-Shock TQ check when attacking LI.
> EXAMPLE: Thus, if a Light Infantry attacking a Skirmisher
> would produce an unadjusted result on the Shock Results Table
> of 1(4), the actual result would be 0(4).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D923shock

Źródło i dokładny zakres: 9.23: SK cannot Shock attack, other type selected in mixed defense/ignoreSKSize, inflicted Hits half/floor/cap1

Cel i granica dostępności: General Shock/type/Size/base resolution, absent; supplied Step4 after context confirms SK-defender attacker-Hits operator only

Konieczność / zakres blokady: Pełny Shock/base/selection wymaga brakującego kontekstu. Podane zakazy/wybórType/pół/floor/cap1 mają lokalny zakres; context nie dopuszcza cap1 od samej obecnościSKw mixed defense.

Porównanie i propozycja: Krawędź modification/explicit identyczna; G-D923shock po kontekście uczciwie zawęża remaining need do selection/CRT i podaje operator. Przyjąć rolę modyfikacji i częściową dostępność, bez domknięciaSEM-004. Decyzja05 o wspierającym powiązaniuSK nie nadaje konieczności dodatkowego lookupu dla zadanychHits.

**first-001:** `/dependencies/66`; bajty [472141,473131), SHA-256 `14cd5e30b3f348dfff39355a06e9ee8c3ff606190246537d7d86323c052d15ef`.

Zapis modelu: `R923→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock Combat", "description": "Base Shock defender/type/Size/hit rules modified here", "needed_context": "Shock resolution and base defender/Size selection"}

Uzasadnienie modelu: Source refers to Shock Combat; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R923"], "blocks_full_result": true, "reason": "Base Shock defender/type/Size/hit rules modified here is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny Shock/base/selection wymaga brakującego kontekstu. Podane zakazy/wybórType/pół/floor/cap1 mają lokalny zakres; context nie dopuszcza cap1 od samej obecnościSKw mixed defense.

Zapis gapu modelu: G-D923shock — Base Shock defender/type/Size/hit rules modified here is referenced but unavailable. Potrzebny kontekst: Shock resolution and base defender/Size selection

**context-01:** `/dependencies/66`; bajty [549196,550213), SHA-256 `8ad3579f3449e817954505d8ebe06b6a8b553a34458f051e53dce228bcc54e4e`.

Zapis modelu: `R923→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock Combat", "description": "Base Shock defender/type/Size/hit rules modified here", "needed_context": "Shock resolution and base defender/Size selection"}

Uzasadnienie modelu: Source refers to Shock Combat; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R923"], "blocks_full_result": true, "reason": "Base Shock defender/type/Size/hit rules modified here is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny Shock/base/selection wymaga brakującego kontekstu. Podane zakazy/wybórType/pół/floor/cap1 mają lokalny zakres; context nie dopuszcza cap1 od samej obecnościSKw mixed defense.

Zapis gapu modelu: G-D923shock — Step 4 bullet #3 now explicitly supplies attacker-Hits half, round down, cap 1 when defender Skirmisher; general defender/type/Size selection and exact base results absent. Potrzebny kontekst: Earlier general Shock defender/type/Size selection and exact Shock CRT.

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/6/text`, znaki [1378,2431), SHA-256 wycinka `7a41ae70411a97363939e936161395afdacc50ef731d83ff5fc83badfabd23b5`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.23 Shock Combat: Skirmishers have the following restrictions
> when involved in Shock Combat:
> • Skirmishers cannot Shock attack.
> • All units that Shock attack Skirmishers alone do not have
> to make a Pre-Shock TQ even if they have SHOCK MUST
> CHECK TQ markers.
> • If a Skirmisher unit is defending in coordination with any other
> unit type, the other Type must be chosen as the defender. The
> Size rating of the Skirmisher is ignored.
> • Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.
> • Phalanx (PH), Heavy Infantry (HI), and Legion Infantry (LG)
> units that are attacked from a Front hex by Light Infantry (LI)
> do not undergo a Pre-Shock TQ check even if the attackers have
> SHOCK MUST CHECK TQ markers, though the attacking LI
> still do. The reverse is not true; PH, HI and LG do undergo a
> Pre-Shock TQ check when attacking LI.
> EXAMPLE: Thus, if a Light Infantry attacking a Skirmisher
> would produce an unadjusted result on the Shock Results Table
> of 1(4), the actual result would be 0(4).
> 

Dodatkowy wcześniej dostarczony kontekst tylko dla context-01: Step4. Nie dostarcza wcześniejszych etapów lub rzeczywistej CRT.

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

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D924line

Źródło i dokładny zakres: 9.24: one SK/Velites per interruption does not disrupt LC line4.32; examples allow separated single interruptions

Cel i granica dostępności: 4.32 full Line Command eligibility, absent

Konieczność / zakres blokady: Kompletna kwalifikacjaLC wymaga4.32. Pojedyncza lokalna przerwa jest dopuszczona i nie oznacza globalnie tylkojednegoSKna całejlinii.

Porównanie i propozycja: R924→4.32 modification/explicit zachowuje warunek z dokończeniaPDF34. Oba wyniki nie gubią granicy onlyone i osobnych przerw. Przyjąć modyfikację; przykłady nie zastępują wszystkich innych kryteriówLC i brak4.32 nie unieważnia tego fragmentu.

**first-001:** `/dependencies/68`; bajty [474037,475039), SHA-256 `20fb6dd43e031f4e04849a4a72fb2792971973f4fe5f734fd578f8fbc0007bd5`.

Zapis modelu: `R924→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "4.32", "description": "Line Command line eligibility qualified by one intervening unit", "needed_context": "4.32 including Line Command definitions"}

Uzasadnienie modelu: Source refers to 4.32; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R924"], "blocks_full_result": true, "reason": "Line Command line eligibility qualified by one intervening unit is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Kompletna kwalifikacjaLC wymaga4.32. Pojedyncza lokalna przerwa jest dopuszczona i nie oznacza globalnie tylkojednegoSKna całejlinii.

Zapis gapu modelu: G-D924line — Line Command line eligibility qualified by one intervening unit is referenced but unavailable. Potrzebny kontekst: 4.32 including Line Command definitions

**context-01:** `/dependencies/68`; bajty [551148,552178), SHA-256 `06392b5b7f4df3e8798a54840d081d1e7668a7f6f2e1698bfff247d6da49575d`.

Zapis modelu: `R924→candidate`, `modification/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "4.32", "description": "Line Command line eligibility qualified by one intervening unit", "needed_context": "4.32 including Line Command definitions"}

Uzasadnienie modelu: Source refers to 4.32; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R924"], "blocks_full_result": true, "reason": "Line Command line eligibility qualified by one intervening unit is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Kompletna kwalifikacjaLC wymaga4.32. Pojedyncza lokalna przerwa jest dopuszczona i nie oznacza globalnie tylkojednegoSKna całejlinii.

Zapis gapu modelu: G-D924line — Line Command line eligibility qualified by one intervening unit is referenced but unavailable. Potrzebny kontekst: 4.32 including Line Command definitions

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/6/text`, znaki [2742,2869), SHA-256 wycinka `505de7478f7d20a4033c71691e64a8344dcef3f29c4f0b6bbf993020d119f9e1`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> • When determining lines for a Line Command (4.32), the pres-
> ence of a Velites or Skirmisher unit does not disrupt the line if

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/7/text`, znaki [0,399), SHA-256 wycinka `21e589c0b1549bb1f8eec7aa74a6b192da3e98ec0b174bfa3e09b1745e1f5157`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> the interruption is caused by only one such unit.
> EXAMPLE: There are Hastati in 2808, Velites in 2809, and Has-
> tati in 2810. This would still be eligible to be a line. However,
> if there were Velites in 2809 and 2810 and the Hastati in 2808
> and 2811, the two Hastati would not form a line. If there were
> Hastati in 2808, 2810, and 2812, with Velites in 2809 and 2811,
> the Hastati could form a line.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D924stack

Źródło i dokładny zakres: 9.24: see6.69 for special stacking rules for SK and Velites

Cel i granica dostępności: 6.69 substantive special stacking rules, absent

Konieczność / zakres blokady: Specjalnej legalności stosu nie wyznacza samo odesłanie. Lokalny brak kosztu zmianyfacing/ruchu nie dostarcza6.69.

Porównanie i propozycja: R924→6.69 procedure_use/explicit poparte odesłaniem do właściwych specjalnych zasad, nie do summaryjakD961stack. Nie potwierdzono wnętrza6.69, ale źródło jednoznacznie wskazuje potrzebę tychzasad. Przyjąć rolę użycia i ograniczoną blokadęlegalności stacking, nie reszty9.24.

**first-001:** `/dependencies/67`; bajty [473137,474031), SHA-256 `2f356812069d163bd331d87755522b166c5647e1630c172bc0d198e9b0161ac3`.

Zapis modelu: `R924→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.69", "description": "Special Skirmisher/Velites stacking", "needed_context": "6.69"}

Uzasadnienie modelu: Source refers to 6.69; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R924"], "blocks_full_result": true, "reason": "Special Skirmisher/Velites stacking is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Specjalnej legalności stosu nie wyznacza samo odesłanie. Lokalny brak kosztu zmianyfacing/ruchu nie dostarcza6.69.

Zapis gapu modelu: G-D924stack — Special Skirmisher/Velites stacking is referenced but unavailable. Potrzebny kontekst: 6.69

**context-01:** `/dependencies/67`; bajty [550220,551141), SHA-256 `144ff60367ee8a6b7a442bc28e2514d4747e16bbe27f7f610c1bdcb8b787958e`.

Zapis modelu: `R924→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.69", "description": "Special Skirmisher/Velites stacking", "needed_context": "6.69"}

Uzasadnienie modelu: Source refers to 6.69; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R924"], "blocks_full_result": true, "reason": "Special Skirmisher/Velites stacking is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Specjalnej legalności stosu nie wyznacza samo odesłanie. Lokalny brak kosztu zmianyfacing/ruchu nie dostarcza6.69.

Zapis gapu modelu: G-D924stack — Special Skirmisher/Velites stacking is referenced but unavailable. Potrzebny kontekst: 6.69

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/6/text`, znaki [2564,2742), SHA-256 wycinka `9eaa455cb4ddf577d3293e2638371865079bf05ff1c15980702edf96940fd132`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> • See 6.69 for special stacking rules for Skirmishers and Velites.
> Skirmishers can change facing at no MP cost and can move
> more than once per Game Turn without a Cohesion cost.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D931HD

Źródło i dokładny zakres: 9.31: missile-armedLC may H&D8.3 vs lowerMA exceptSK

Cel i granica dostępności: 8.3 H&D execution procedure, absent

Konieczność / zakres blokady: Wystrzelenie i rezultatH&D wymagają8.3; eligibilitylowerMA i wykluczenieSK są znane lokalnie.

Porównanie i propozycja: R931→8.3 procedure_use/explicit zachowuje Missile-armed, lowerMA i exceptSK. Brak źródła nie znosi zakazuSK, a jawne zezwolenie nie dostarcza drogi/limitu/CRT. Przyjąć potrzebę wykonaniaH&D, bez rozszerzenia na każdąLC lub każdą sytuacjęfire.

**first-001:** `/dependencies/69`; bajty [475045,475924), SHA-256 `e4e90e9f0899363da17174c4d177df333a9f7470d9f9aadca8da05df2952943a`.

Zapis modelu: `R931→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.3", "description": "Light Cavalry H&D fire procedure", "needed_context": "8.3"}

Uzasadnienie modelu: Source refers to 8.3; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R931"], "blocks_full_result": true, "reason": "Light Cavalry H&D fire procedure is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Wystrzelenie i rezultatH&D wymagają8.3; eligibilitylowerMA i wykluczenieSK są znane lokalnie.

Zapis gapu modelu: G-D931HD — Light Cavalry H&D fire procedure is referenced but unavailable. Potrzebny kontekst: 8.3

**context-01:** `/dependencies/69`; bajty [552185,553091), SHA-256 `4a10c22182c0f52d00c644f0d51ce71f007cbf9387560ba069e3f53353a68029`.

Zapis modelu: `R931→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "8.3", "description": "Light Cavalry H&D fire procedure", "needed_context": "8.3"}

Uzasadnienie modelu: Source refers to 8.3; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R931"], "blocks_full_result": true, "reason": "Light Cavalry H&D fire procedure is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Wystrzelenie i rezultatH&D wymagają8.3; eligibilitylowerMA i wykluczenieSK są znane lokalnie.

Zapis gapu modelu: G-D931HD — Light Cavalry H&D fire procedure is referenced but unavailable. Potrzebny kontekst: 8.3

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/7/text`, znaki [417,600), SHA-256 wycinka `b51847914c35625422d58600ed957739b59956413ba4e1d5fc3e295adf7cf909`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.31 Missile-armed Light Cavalry may use H&D fire (8.3) against
> all units with a lower MA, except Skirmishers. Light Cavalry
> Archers can fire when they use Orderly Withdrawal (6.55).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D931OW

Źródło i dokładny zakres: 9.31: LC Archers may fire while using OW6.55

Cel i granica dostępności: 6.55 OW-associated fire procedure/qualifications, absent

Konieczność / zakres blokady: Lokalne zezwolenie dotyczyLCArchers; realny moment i wykonanie strzału podczasOW wymagają6.55.

Porównanie i propozycja: R931→6.55 procedure_use/explicit jest numerowanym odesłaniem do wykonania firingduringOW. Nie rozszerza pozwolenia na wszystkie klasyLC lub wszystkie ReactionFire. Przyjąć rolę i ograniczoną blokadę wykonania; wnętrza6.55 nie odczytano.

**first-001:** `/dependencies/70`; bajty [475930,476818), SHA-256 `27f35934512788a7e31916539f5bbe3c0db4ea55b9869b641ab47bfb76873803`.

Zapis modelu: `R931→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.55", "description": "Light Cavalry Archer fire during OW", "needed_context": "6.55"}

Uzasadnienie modelu: Source refers to 6.55; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R931"], "blocks_full_result": true, "reason": "Light Cavalry Archer fire during OW is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Lokalne zezwolenie dotyczyLCArchers; realny moment i wykonanie strzału podczasOW wymagają6.55.

Zapis gapu modelu: G-D931OW — Light Cavalry Archer fire during OW is referenced but unavailable. Potrzebny kontekst: 6.55

**context-01:** `/dependencies/70`; bajty [553098,554013), SHA-256 `437d5d8f1315b6a266de5cb420af682784c47a66d7c3b6d68af0e30d712485e3`.

Zapis modelu: `R931→candidate`, `procedure_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "6.55", "description": "Light Cavalry Archer fire during OW", "needed_context": "6.55"}

Uzasadnienie modelu: Source refers to 6.55; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R931"], "blocks_full_result": true, "reason": "Light Cavalry Archer fire during OW is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Lokalne zezwolenie dotyczyLCArchers; realny moment i wykonanie strzału podczasOW wymagają6.55.

Zapis gapu modelu: G-D931OW — Light Cavalry Archer fire during OW is referenced but unavailable. Potrzebny kontekst: 6.55

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/7/text`, znaki [417,600), SHA-256 wycinka `b51847914c35625422d58600ed957739b59956413ba4e1d5fc3e295adf7cf909`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.31 Missile-armed Light Cavalry may use H&D fire (8.3) against
> all units with a lower MA, except Skirmishers. Light Cavalry
> Archers can fire when they use Orderly Withdrawal (6.55).
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D932CRT

Źródło i dokładny zakres: 9.32: attackingLC inflicted Hits vs specifiedinfantry half/floor; exampleAS usesprintedCRT

Cel i granica dostępności: Actual ShockCRT values/headers/notes, absent; AS/LC operators partly supplied aftercontext

Konieczność / zakres blokady: Tabela potrzebna do baseHits. Lokalny pół/floor przy zadanychHits nie wymaga nowegoCRT. Kontekstpodaje conditionalAS2x/LCpół/floor/Routedexception/cumulative, nie combinedorder ani lookup.

Porównanie i propozycja: Jedyna zmieniona krawędźpartii: contextcandidate/impact/evidence jawnieoddziela missingCRT od suppliedoperators. G-D932CRT też doprecyzowane. Poparte jako częściowe zawężenie wymagania, bez domknięciaSEM-003, akceptacji nowegocałegoR932exceptions lub algebraicznego skasowaniaAS/LC.

**first-001:** `/dependencies/71`; bajty [476824,477811), SHA-256 `86005b6142d8684bd97d9ec22d9360aca5337060adf2fd40e51e012b08614537`.

Zapis modelu: `R932→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock CRT", "description": "Shock CRT values and AS interaction for LC halving", "needed_context": "Shock CRT and Attack Superiority hit adjustment"}

Uzasadnienie modelu: Source refers to Shock CRT; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R932"], "blocks_full_result": true, "reason": "Shock CRT values and AS interaction for LC halving is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Tabela potrzebna do baseHits. Lokalny pół/floor przy zadanychHits nie wymaga nowegoCRT. Kontekstpodaje conditionalAS2x/LCpół/floor/Routedexception/cumulative, nie combinedorder ani lookup.

Zapis gapu modelu: G-D932CRT — Shock CRT values and AS interaction for LC halving is referenced but unavailable. Potrzebny kontekst: Shock CRT and Attack Superiority hit adjustment

**context-01:** `/dependencies/71`; bajty [554020,555198), SHA-256 `de499c5a9ae07c348e58daaf392163835bc102a1d8bcfd4d7110105e01080db4`.

Zapis modelu: `R932→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock CRT", "description": "Actual Shock CRT values used by 9.32; conditional AS/LC operators separately supplied by NCTX846S4", "needed_context": "Exact Shock CRT headers/rows/notes and base lookup; applicability and unresolved combined order"}

Uzasadnienie modelu: Source refers to Shock CRT; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R932"], "blocks_full_result": true, "reason": "Conditional operators supplied; exact table and base results absent. Target remains unresolved."}

Ocena: supported_named_requirement_and_relation_role. Tabela potrzebna do baseHits. Lokalny pół/floor przy zadanychHits nie wymaga nowegoCRT. Kontekstpodaje conditionalAS2x/LCpół/floor/Routedexception/cumulative, nie combinedorder ani lookup.

Zapis gapu modelu: G-D932CRT — Conditional AS/LC operators now supplied; actual Shock CRT headers/rows/notes, base numeric results and combined order unresolved. Potrzebny kontekst: Exact Shock CRT and needed lookup/applicability/order context; no chart alias equivalence inferred.

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/7/text`, znaki [600,894), SHA-256 wycinka `65183a5874c2b395a0054b9182edc6e5be10b68ec900a0f188243992d3421666`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).
> EXAMPLE: A Light Cavalry unit with Attack Superiority (AS)
> against a Heavy Infantry unit would use the printed result on
> the Shock CRT.
> 

Dodatkowy wcześniej dostarczony kontekst tylko dla context-01: Step4. Nie dostarcza wcześniejszych etapów lub rzeczywistej CRT.

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

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## D941CRT

Źródło i dokładny zakres: 9.41: qualifyingmovingFrontattack onflank-supportedPH shiftsCRT2Lperflank,HI1Linstead; notstationary/FlankRear/anyPHattacker

Cel i granica dostępności: ShockCombatCRT basecolumn/results and selection, absent

Konieczność / zakres blokady: Pełny odczyt wyniku wymagaCRT/basecolumn. Zadana bazowakolumna i kwalifikująceflanki pozwalają lokalnie obliczyćshift bez odczytuHits.

Porównanie i propozycja: R941→CRT table_use/explicit poparte rzeczywistym przesunięciemkolumny. Oba wyniki zachowują ograniczenia; przykład5→1zakłada nootheradjustments i nie zatwierdza całejtabeli. Przyjąć wymaganie i właściwy localshift scope, bez ratingów i pełnegowyniku.

**first-001:** `/dependencies/72`; bajty [477817,478798), SHA-256 `d8c5ecf02ca39bf7b762be84356bbd6303ee2cb130197835cf7a1c997b73c90d`.

Zapis modelu: `R941→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock Combat CRT", "description": "Base Shock columns/results to shift left", "needed_context": "Shock Combat CRT and column-selection procedure"}

Uzasadnienie modelu: Source refers to Shock Combat CRT; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R941"], "blocks_full_result": true, "reason": "Base Shock columns/results to shift left is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny odczyt wyniku wymagaCRT/basecolumn. Zadana bazowakolumna i kwalifikująceflanki pozwalają lokalnie obliczyćshift bez odczytuHits.

Zapis gapu modelu: G-D941CRT — Base Shock columns/results to shift left is referenced but unavailable. Potrzebny kontekst: Shock Combat CRT and column-selection procedure

**context-01:** `/dependencies/72`; bajty [555205,556214), SHA-256 `1cf483ac1c30f18cd4d0c9fc32b25012d646ef2b6f56903054324c053c79d69c`.

Zapis modelu: `R941→candidate`, `table_use/explicit`, `unresolved`, blocks_full_result=`True`.

Dosłowny kandydat modelu (nie dostarczone źródło celu): {"original_reference": "Shock Combat CRT", "description": "Base Shock columns/results to shift left", "needed_context": "Shock Combat CRT and column-selection procedure"}

Uzasadnienie modelu: Source refers to Shock Combat CRT; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Deklaracja wpływu modelu: {"affected_ids": ["R941"], "blocks_full_result": true, "reason": "Base Shock columns/results to shift left is not fully supplied; no missing content reconstructed."}

Ocena: supported_named_requirement_and_relation_role. Pełny odczyt wyniku wymagaCRT/basecolumn. Zadana bazowakolumna i kwalifikująceflanki pozwalają lokalnie obliczyćshift bez odczytuHits.

Zapis gapu modelu: G-D941CRT — Base Shock columns/results to shift left is referenced but unavailable. Potrzebny kontekst: Shock Combat CRT and column-selection procedure

Dostarczona niezależna transkrypcja: `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/7/text`, znaki [914,1826), SHA-256 wycinka `4f3d4b3d5617f1a6c2c3185e3018151fcb835adab07f60f19235c02125300fec`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.

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
> EXAMPLE: If 2 LGs attack a PH frontally that has other PH
> units in each Flank hex, the Shock attack is resolved, assuming
> no other adjustments, on the 1 column (they start in 5 and get
> shuffled 4L to 1). This means that, on average per Shock, the PH
> will take 1, maybe 2 Hits; but each LG will take 2 or 3.
> 

Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.

## Granice wyniku

29 krawędzi identycznych, D932CRT zmieniona; dodatkowo G-D923shock i G-D932CRT zawężono po kontekście. Brak nowych źródeł lub korekt. 
Właścicielowi udostępniono60; oceniający porównał60; nowych decyzji właściciela0; pending60. Faktyczny odczyt/otwarcieunknown.
Poprzednie125 zakresów mają własne decyzje; razem185 przypisanych wystąpień porównano. .4b3 ma72 niewykonane jako pełna partia, z wcześniej rozstrzygniętym tylko dodatkowym wystąpieniem D961stack.
SEM-001–013 zachowane w nierozstrzygniętych zakresach, w tym resztaSEM-004. DecyzjeSEM-014–016 zachowane, nie rozszerzone. Osiem oczekiwań nadalpending. 105 candidates nie staje sięgold. PełneTP/FP/FN/precision/recall not_assessable.
1 dodatkowa strona/1reguła/0tabel,1runda/0korekt;0pełnych domknięć,4częściowe aktualizacje i4nowe deklaracje. Trzeciego źródła nie pozyskano. Izolacja ścieżek naruszona w dawnym context-01, odczyt oceny niezaobserwowany; ekspozycja/czysty kontekst/aktywny budżet unknown.
Następny krok: decyzje dla owner-focus, potem osobna .4b3 po oszacowaniu. M-POC5A/.4/.4b partial; M-POC5 jedyny next.
