# M-POC5A.4b3 — wszystkie36ID porównane w obu wynikach

Ręczny przegląd wszystkich 36 ID w obu oryginalnych odpowiedziach, source rules/nodes i przypisanych gapów. Porównano literalne klauzule dostarczonych helperów z istniejącymi obrazami PDF34–37; pomocniczo PDF31 i10.11/8.75, które były już w pakiecie. Nie odczytano brakujących celów ani nowych stron. Skrypt zapisuje ręczne oceny i wiąże je z surowymi bajtami; nie wykonuje ekstrakcji lub inferencji. To propozycje, nie automatyczna akceptacja.

72 wystąpienia:36/36;68 pozytywnych ograniczonych propozycji i4 wystąpienia z dwiema osobnymi kwestiami. Wszystkie nowe oceny waiting_review. Rodzaj D961stack pozostaje już rozstrzygnięty jako mention.

first-001: SHA-256 `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: SHA-256 `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`; PDF `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

[Pełny ślad pól, źródeł i bajtów](comparisons.json). Kandydat modelu nie jest treścią źródła celu.

## D-ZOC-R966

Źródło / dokładny zakres: 9.66: entered MLE hex must be Clear and outside enemy ZOC

Cel / dostępność: General ZOC geometry/exceptions absent; word ZOC supplied, definition dependency inferred

Konieczność / wpływ: Do realnej kwalifikacji heksu potrzeba definicji ZOC. Przy zadanym enemy-ZOC lokalny zakaz wejścia jest znany; inne warunki MLE nadal obowiązują.

Porównanie / propozycja: Obie odpowiedzi R966→ZOC definition/implicit: kierunek i potrzeba definicji poparte użyciem terminu. Niejawność dotyczy zależności definicyjnej, nie samego jawnego warunku. Nie rekonstruuje Front/geometrii ani legalności całego MLE.

**first-001:** `/dependencies/122`; bajty [525338,526291), SHA-256 `7725bbe6b7efc3ce0b34dbdbabb517ae1dc9522afa93456dba8635592d90711c`.

Zapis modelu: `R966→candidate`, `definition/implicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Wpływ zapisany przez model: {"affected_ids": ["R966"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D-ZOC-R966", "class": "missing_context", "affected_ids": ["R966", "D-ZOC-R966"], "source_regions": ["pdf-35-core-left", "pdf-35-core-right"], "reason": "General ZOC test in rule condition is referenced but unavailable.", "needed_context": "General ZOC definition and exceptions", "blocking": true, "evidence_ids": ["E966a", "E966b"], "review_status": "unreviewed"}

**context-01:** `/dependencies/122`; bajty [604152,605133), SHA-256 `adab3db8b6ccdf4a10db97f3852f83ffdeecbca9a8e1b9cb2acf1c93ea3f45d5`.

Zapis modelu: `R966→candidate`, `definition/implicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Wpływ zapisany przez model: {"affected_ids": ["R966"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D-ZOC-R966", "class": "missing_context", "affected_ids": ["R966", "D-ZOC-R966"], "source_regions": ["pdf-35-core-left", "pdf-35-core-right"], "reason": "General ZOC test in rule condition is referenced but unavailable.", "needed_context": "General ZOC definition and exceptions", "blocking": true, "evidence_ids": ["E966a", "E966b"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [2061,2363), hash wycinka `78f078da6fa2fe33ab8e624792fedfa3a278aab91723954cab2e31c9131f6459`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [0,327), hash wycinka `1a05ddc906da07e49fe98fead9ee567340ebd447c7976027f2aa2673a971b318`. Oceniana klauzula to source_scope, nie cała koperta.

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D-ZOC-R972

Źródło / dokładny zakres: 9.72: stationary Shock exception against enemy in own ZOC

Cel / dostępność: General ZOC geometry/exceptions absent

Konieczność / wpływ: Na planszy trzeba rozpoznać własny ZOC; przy zadanym ZOC zezwolenie na Shock bez ruchu jest lokalnie znane, niezależnie od brakującej wartości AWL/RP. Nie rozstrzyga połączenia dwóch bramek Triarii.

Porównanie / propozycja: R972→ZOC definition/implicit zgodne w obu. Potrzeba definicji nie unieważnia stationary exception. Przyjąć wymaganie geometryczne w dokładnym zakresie; EXP-052/SEM-011 i cała legalność Shock pozostają poza decyzją.

**first-001:** `/dependencies/123`; bajty [526297,527232), SHA-256 `760b9efa18bb205fcded64ee4a102461667fbc08a6f268aa178ac64bbf65bf96`.

Zapis modelu: `R972→candidate`, `definition/implicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Wpływ zapisany przez model: {"affected_ids": ["R972"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D-ZOC-R972", "class": "missing_context", "affected_ids": ["R972", "D-ZOC-R972"], "source_regions": ["pdf-35-core-right"], "reason": "General ZOC test in rule condition is referenced but unavailable.", "needed_context": "General ZOC definition and exceptions", "blocking": true, "evidence_ids": ["E972"], "review_status": "unreviewed"}

**context-01:** `/dependencies/123`; bajty [605140,606102), SHA-256 `5080b89cfe80f26f67717fb7a13d1269a8db76bf1942e572c56428cab8ee027b`.

Zapis modelu: `R972→candidate`, `definition/implicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Wpływ zapisany przez model: {"affected_ids": ["R972"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D-ZOC-R972", "class": "missing_context", "affected_ids": ["R972", "D-ZOC-R972"], "source_regions": ["pdf-35-core-right"], "reason": "General ZOC test in rule condition is referenced but unavailable.", "needed_context": "General ZOC definition and exceptions", "blocking": true, "evidence_ids": ["E972"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [2066,2321), hash wycinka `9015a600ac9342bae6f5a305e4e7b9e62aa6e578398381968f2dffe52e4db010`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D-ZOC-R995

Źródło / dokładny zakres: 9.95: at least two BI of leader command enter enemy ZOC; Impetuosity lasts rest of Game Turn then lost

Cel / dostępność: General ZOC definition absent; selected command membership also not supplied

Konieczność / wpływ: Realne wejścia wymagają ZOC. Gdy dwa kwalifikujące wejścia i command są zadane, koniec bonusu po reszcie Game Turn jest znany, bez nowej definicji ZOC.

Porównanie / propozycja: R995→ZOC definition/implicit ma poprawny kierunek i rolę. Nie utożsamia pierwszego wejścia z natychmiastową utratą ani całej armii z jedną komendą. Przyjąć wymaganie i warunkową blokadę realnej kwalifikacji.

**first-001:** `/dependencies/124`; bajty [527238,528173), SHA-256 `c601359ff3ef69054b29881bfbd14cea8a4a3a8eb2240250ea3d0e7157890be8`.

Zapis modelu: `R995→candidate`, `definition/implicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Wpływ zapisany przez model: {"affected_ids": ["R995"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D-ZOC-R995", "class": "missing_context", "affected_ids": ["R995", "D-ZOC-R995"], "source_regions": ["pdf-36-core-right"], "reason": "General ZOC test in rule condition is referenced but unavailable.", "needed_context": "General ZOC definition and exceptions", "blocking": true, "evidence_ids": ["E995"], "review_status": "unreviewed"}

**context-01:** `/dependencies/124`; bajty [606109,607071), SHA-256 `dd820339af9e2d0f2c9e4a20b281a09e38d3138cfadc267593b99425ec84b026`.

Zapis modelu: `R995→candidate`, `definition/implicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "ZOC", "description": "General ZOC test in rule condition", "needed_context": "General ZOC definition and exceptions"}

Uzasadnienie modelu: The source directly tests presence/entry of ZOC; the missing geometric definition is necessary to evaluate that condition, not merely inferred from similar wording.

Wpływ zapisany przez model: {"affected_ids": ["R995"], "blocks_full_result": true, "reason": "General ZOC test in rule condition is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D-ZOC-R995", "class": "missing_context", "affected_ids": ["R995", "D-ZOC-R995"], "source_regions": ["pdf-36-core-right"], "reason": "General ZOC test in rule condition is referenced but unavailable.", "needed_context": "General ZOC definition and exceptions", "blocking": true, "evidence_ids": ["E995"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [1322,1895), hash wycinka `317a456b470533b735fa5d68027f5385d568b359bde804b811a58fb0891ed047`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.95 Barbarian Impetuosity
> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D951OC

Źródło / dokładny zakres: 9.51: DD formation needs Individual Order or LC directly from OC

Cel / dostępność: Individual Order/LC/OC eligibility, range and procedure absent

Konieczność / wpływ: Pełna legalność rozkazu potrzebuje procedury. Lokalnie wiadomo, że rozkaz ma pochodzić bezpośrednio od OC, a ruch obu jednostek kończy się w tej fazie.

Porównanie / propozycja: R951→named command procedure procedure_use/explicit poparte literalnym requires w obu wynikach. Przyjąć użycie i blokadę pełnej kwalifikacji; nie zatwierdza konkretnego zasięgu OC, listy jednostek ani całego formation record.

**first-001:** `/dependencies/74`; bajty [479788,480836), SHA-256 `a4d2fb0a39a0c6d88ca454fca25432f2a1199545c05ad351bf284a287dc88f37`.

Zapis modelu: `R951→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Individual Order or Line Command, directly from the OC", "description": "OC command eligibility/range and order procedure", "needed_context": "Individual Order/Line Command/OC rules"}

Uzasadnienie modelu: Source refers to Individual Order or Line Command, directly from the OC; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R951"], "blocks_full_result": true, "reason": "OC command eligibility/range and order procedure is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D951OC", "class": "missing_context", "affected_ids": ["R951", "D951OC"], "source_regions": ["pdf-34-core-right"], "reason": "OC command eligibility/range and order procedure is referenced but unavailable.", "needed_context": "Individual Order/Line Command/OC rules", "blocking": true, "evidence_ids": ["E951"], "review_status": "unreviewed"}

**context-01:** `/dependencies/74`; bajty [557233,558308), SHA-256 `e5a53c45fb136cbb044bcbf3fb23d0702840131afe1354f87857ac4b16017cd6`.

Zapis modelu: `R951→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Individual Order or Line Command, directly from the OC", "description": "OC command eligibility/range and order procedure", "needed_context": "Individual Order/Line Command/OC rules"}

Uzasadnienie modelu: Source refers to Individual Order or Line Command, directly from the OC; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R951"], "blocks_full_result": true, "reason": "OC command eligibility/range and order procedure is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D951OC", "class": "missing_context", "affected_ids": ["R951", "D951OC"], "source_regions": ["pdf-34-core-right"], "reason": "OC command eligibility/range and order procedure is referenced but unavailable.", "needed_context": "Individual Order/Line Command/OC rules", "blocking": true, "evidence_ids": ["E951"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/8/text`, znaki [265,852), hash wycinka `8e5bb49227e03f313217ad70156bbfe461bb2631e45567664b41f9935d008f63`. Oceniana klauzula to source_scope, nie cała koperta.

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
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D951terrain

Źródło / dokładny zakres: 9.51: back PH enters front PH hex paying normal terrain costs plus1 MP

Cel / dostępność: Normal terrain cost is expressly required; Movement Cost Chart identity/location is not expressly named in9.51 and actual costs absent

Konieczność / wpływ: Bez bazowego kosztu nie wyliczymy realnego wydatku MP. Przy zadanym prawidłowym koszcie dodanie1 jest znane. Samo zdanie nie dowodzi jawnego odesłania do konkretnej tabeli.

Porównanie / propozycja: Oba modele table_use/explicit; literalne original_reference mówi normal terrain costs, a dopiero needed_context wskazuje chart. SEM-018: przyjąć jawną potrzebę zwykłego kosztu i kierunek, nie przyjmować explicit table_use jako dosłownego odesłania do chart. Zależność od tabeli można uznać wyłącznie za wnioskowaną; brak treści/aliasu tabeli pozostaje.

**first-001:** `/dependencies/75`; bajty [480842,481785), SHA-256 `f03a2672b549a48d99475cdf13727ab139c4f881b606dd478b06470138664b58`.

Zapis modelu: `R951→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "normal terrain costs", "description": "Cost of entering front PH hex", "needed_context": "Movement Cost Chart terrain costs"}

Uzasadnienie modelu: Source refers to normal terrain costs; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R951"], "blocks_full_result": true, "reason": "Cost of entering front PH hex is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: explicit cost requirement supported; specific table-use target inferred, separate owner decision

Ocena jawności: normal cost explicit; specific chart reference not explicit in9.51; SEM-018

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D951terrain", "class": "missing_context", "affected_ids": ["R951", "D951terrain"], "source_regions": ["pdf-34-core-right"], "reason": "Cost of entering front PH hex is referenced but unavailable.", "needed_context": "Movement Cost Chart terrain costs", "blocking": true, "evidence_ids": ["E951"], "review_status": "unreviewed"}

**context-01:** `/dependencies/75`; bajty [558315,559285), SHA-256 `cee55538bd58af135ae1773d2fff4ba2dcff130b8d528575d569f349ae524043`.

Zapis modelu: `R951→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "normal terrain costs", "description": "Cost of entering front PH hex", "needed_context": "Movement Cost Chart terrain costs"}

Uzasadnienie modelu: Source refers to normal terrain costs; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R951"], "blocks_full_result": true, "reason": "Cost of entering front PH hex is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: explicit cost requirement supported; specific table-use target inferred, separate owner decision

Ocena jawności: normal cost explicit; specific chart reference not explicit in9.51; SEM-018

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D951terrain", "class": "missing_context", "affected_ids": ["R951", "D951terrain"], "source_regions": ["pdf-34-core-right"], "reason": "Cost of entering front PH hex is referenced but unavailable.", "needed_context": "Movement Cost Chart terrain costs", "blocking": true, "evidence_ids": ["E951"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/8/text`, znaki [265,852), hash wycinka `8e5bb49227e03f313217ad70156bbfe461bb2631e45567664b41f9935d008f63`. Oceniana klauzula to source_scope, nie cała koperta.

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
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D952PAW

Źródło / dokładny zakres: 9.52: DD units may use Pre-Arranged Withdrawal6.8

Cel / dostępność: 6.8 PAW qualifications and execution absent

Konieczność / wpływ: Brak6.8 blokuje wykonanie PAW, nie sam fakt lokalnego dopuszczenia tego trybu. Ograniczenia OC/4MA i zakazy Wheel/Reverse/Column nie znikają.

Porównanie / propozycja: R952→6.8 procedure_use/explicit zgodne: named permission plus numerowana procedura, nie definicja lub zwykła wzmianka. Przyjąć tę rolę; nie dopisać tras/warunków PAW lub wyników ruchu.

**first-001:** `/dependencies/76`; bajty [481791,482698), SHA-256 `e685a537846a4c65a9baa744caac807dbca558aa290c90dc38df0083bc6ccf36`.

Zapis modelu: `R952→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "6.8", "description": "Permitted Pre-Arranged Withdrawal of DD stack", "needed_context": "6.8"}

Uzasadnienie modelu: Source refers to 6.8; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R952"], "blocks_full_result": true, "reason": "Permitted Pre-Arranged Withdrawal of DD stack is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D952PAW", "class": "missing_context", "affected_ids": ["R952", "D952PAW"], "source_regions": ["pdf-34-core-right"], "reason": "Permitted Pre-Arranged Withdrawal of DD stack is referenced but unavailable.", "needed_context": "6.8", "blocking": true, "evidence_ids": ["E952"], "review_status": "unreviewed"}

**context-01:** `/dependencies/76`; bajty [559292,560226), SHA-256 `e7760e630ecebb3659dcf231c11f030bb59de4f6723b84363a00ebc5db1d5511`.

Zapis modelu: `R952→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "6.8", "description": "Permitted Pre-Arranged Withdrawal of DD stack", "needed_context": "6.8"}

Uzasadnienie modelu: Source refers to 6.8; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R952"], "blocks_full_result": true, "reason": "Permitted Pre-Arranged Withdrawal of DD stack is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D952PAW", "class": "missing_context", "affected_ids": ["R952", "D952PAW"], "source_regions": ["pdf-34-core-right"], "reason": "Permitted Pre-Arranged Withdrawal of DD stack is referenced but unavailable.", "needed_context": "6.8", "blocking": true, "evidence_ids": ["E952"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/8/text`, znaki [852,1637), hash wycinka `0d2d8fea5bed15df5d3cd99183ec7880fb2ffd3afdb4e48611e93945460cde58`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.52 Movement Restrictions: Double Depth formation has the
> following effects:
> • The units may receive orders only from the OC.
> • They may move as one unit, but it takes 2 Individual Orders
> (when using Individual Orders) to move both units together.
> They may use Pre-Arranged Withdrawal (6.8).
> • The units may not Wheel (6.44), Reverse (6.45), or use Col-
> umn (6.7). Unstacking requires an Individual Order or Line
> Command as above, at which time the top unit moves off at
> normal costs. The bottom unit must remain in place.
> • The units always use their 4 MA; they never use their 5 MA
> for anything. For any movement that would incur a Cohesion
> Hit, both units incur the Hit.
> • No unit, of any type, may ever move through or into a Double
> Depth stack. Treat them as impassable terrain.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D953pre

Źródło / dokładny zakres: 9.53: DD attack gives defenders+1 Pre-Shock; DD defenders receive−1; upper check except rear/bottom and other checks after Hits

Cel / dostępność: General Pre-Shock process absent; local modifiers/check selection supplied

Konieczność / wpływ: Pełny Pre-Shock potrzebuje procedury. Przy prawidłowo zadanym rzucie znany jest znak i odbiorca modyfikatora. Nie obejmuje niejasności retreat/elimination.

Porównanie / propozycja: R953→Pre-Shock modification/explicit poparte w obu. Zachować oddzielnie+1 przeciw DD i−1 dla broniących DD; rear nie otrzymuje domyślnie top check. Przyjąć ograniczoną rolę, SEM-010/EXP-040 bez zmiany.

**first-001:** `/dependencies/80`; bajty [485545,486498), SHA-256 `a66e9fdfc373fd815a07309efad0ada203198249997a9ee88eac4a3a3d57e64b`.

Zapis modelu: `R953→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Pre-Shock TQ check", "description": "Base Pre-Shock check to receive DD modifiers", "needed_context": "Pre-Shock TQ procedure"}

Uzasadnienie modelu: Source refers to Pre-Shock TQ check; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R953"], "blocks_full_result": true, "reason": "Base Pre-Shock check to receive DD modifiers is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D953pre", "class": "missing_context", "affected_ids": ["R953", "D953pre"], "source_regions": ["pdf-34-core-right"], "reason": "Base Pre-Shock check to receive DD modifiers is referenced but unavailable.", "needed_context": "Pre-Shock TQ procedure", "blocking": true, "evidence_ids": ["E953"], "review_status": "unreviewed"}

**context-01:** `/dependencies/80`; bajty [563158,564138), SHA-256 `b3b068c7eaf1b39378a1715e609b4b583bcdcb33d69d261018b3ed59b8f2e077`.

Zapis modelu: `R953→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Pre-Shock TQ check", "description": "Base Pre-Shock check to receive DD modifiers", "needed_context": "Pre-Shock TQ procedure"}

Uzasadnienie modelu: Source refers to Pre-Shock TQ check; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R953"], "blocks_full_result": true, "reason": "Base Pre-Shock check to receive DD modifiers is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D953pre", "class": "missing_context", "affected_ids": ["R953", "D953pre"], "source_regions": ["pdf-34-core-right"], "reason": "Base Pre-Shock check to receive DD modifiers is referenced but unavailable.", "needed_context": "Pre-Shock TQ procedure", "blocking": true, "evidence_ids": ["E953"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/8/text`, znaki [1637,2737), hash wycinka `2022c160528b1c987a00dd209023322f68d0f303e969c69255de5788d42c579b`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.53 Combat Effects: Double Depth formation has the follow-
> ing effects on combat:
> • The Sizes of both units are combined.
> • Only the top unit is used for TQ checks (unless attacked from
> the rear, in which case it’s the bottom unit). However, if that
> unit incurs any Cohesion Hits, then the other unit checks.
> • Units defending against a Shock attack by units in Double
> Depth incur a +1 DRM to their Pre-Shock TQ check die rolls.
> • Defending units at Double Depth earn a –1 DRM to their Pre-
> Shock TQ check die rolls. Phalanx Defense (9.41) also applies.
> • If a Double Depth stack is Shock attacked from a Flank or
> Rear hex, the defender Cohesion Hits are tripled (3x) instead
> of doubled.
> • Cohesion Hits from Shock are distributed equally between the
> two units, with any odd Hits going to the top unit. Cohesion Hits
> from Missile Fire Hits apply only to the top unit unless fire is
> through a Rear hex, in which case Hits apply to the bottom unit.
> • If either unit in the stack routs, they both rout. The units must
> retreat to separate hexes. If this is not possible, the unit is
> eliminated instead.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D95scenario

Źródło / dokładny zakres: 9.5 Design Note operational sentence: eligible units listed in scenario-specific rules

Cel / dostępność: Selected scenario eligible DD units absent

Konieczność / wpływ: Bez listy nie ustalimy, czy konkretna PH kwalifikuje się. Zasady tworzenia dla zadanej eligible PH mogą być lokalnie rozpatrywane.

Porównanie / propozycja: R95note→scenario condition/explicit poparte operacyjnym zdaniem wewnątrz Design Note. Nie odrzucać zależności przez sam nagłówek note. Przyjąć potrzebę listy, nie listę, setup lub inne historyczne zdania.

**first-001:** `/dependencies/73`; bajty [478804,479782), SHA-256 `85fedc25fa72e70325645416f45fe0e6b01796887985e6949c8dcd54e3d58d9c`.

Zapis modelu: `R95note→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "scenario-specific rules", "description": "Eligible Double Depth Phalanxes", "needed_context": "Selected scenario Double Depth eligible-unit list"}

Uzasadnienie modelu: Source refers to scenario-specific rules; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R95note"], "blocks_full_result": true, "reason": "Eligible Double Depth Phalanxes is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D95scenario", "class": "missing_context", "affected_ids": ["R95note", "D95scenario"], "source_regions": ["pdf-34-core-right"], "reason": "Eligible Double Depth Phalanxes is referenced but unavailable.", "needed_context": "Selected scenario Double Depth eligible-unit list", "blocking": true, "evidence_ids": ["E95note"], "review_status": "unreviewed"}

**context-01:** `/dependencies/73`; bajty [556221,557226), SHA-256 `dcba3775ef0fc3a3f0e955b2501f2ebbb79d50fed655798204b0277a521b50a3`.

Zapis modelu: `R95note→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "scenario-specific rules", "description": "Eligible Double Depth Phalanxes", "needed_context": "Selected scenario Double Depth eligible-unit list"}

Uzasadnienie modelu: Source refers to scenario-specific rules; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R95note"], "blocks_full_result": true, "reason": "Eligible Double Depth Phalanxes is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D95scenario", "class": "missing_context", "affected_ids": ["R95note", "D95scenario"], "source_regions": ["pdf-34-core-right"], "reason": "Eligible Double Depth Phalanxes is referenced but unavailable.", "needed_context": "Selected scenario Double Depth eligible-unit list", "blocking": true, "evidence_ids": ["E95note"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/8/text`, znaki [27,265), hash wycinka `cf92e795b59e7099b060aec08adcd7f9cd27b063d07ce92dce003ab1fc7e91b4`. Oceniana klauzula to source_scope, nie cała koperta.

> DESIGN NOTE: To increase the crushing pressure of the Pha-
> lanxes, post-Alexandrian commanders using the Macedonian
> system often implemented a formation which doubled their
> depth. Eligible units are listed in the scenario-specific rules.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D961line

Źródło / dokładny zakres: 9.61: Roman infantry may have spaces when determining lines; see4.32

Cel / dostępność: Full4.32 Line/LC eligibility absent

Konieczność / wpływ: Pełna kwalifikacja linii wymaga4.32. Lokalna możliwość przerw jest podana; nie znaczy dowolnej liczby/dystansu przerw.

Porównanie / propozycja: R961→4.32 procedure_use/explicit ma numerowany target i kierunek; rola użycia ustalania linii poparta. Przyjąć tę wąską rolę, nie całą definicję linii lub automatyczną legalność LC.

**first-001:** `/dependencies/83`; bajty [488475,489373), SHA-256 `4f8e2d0136fac22322de0d248076482a9fe95c7d35c6bbcaa38ba9b3ecee937b`.

Zapis modelu: `R961→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "4.32", "description": "Line gaps and Line Command eligibility", "needed_context": "4.32"}

Uzasadnienie modelu: Source refers to 4.32; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R961"], "blocks_full_result": true, "reason": "Line gaps and Line Command eligibility is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D961line", "class": "missing_context", "affected_ids": ["R961", "D961line"], "source_regions": ["pdf-35-core-left"], "reason": "Line gaps and Line Command eligibility is referenced but unavailable.", "needed_context": "4.32", "blocking": true, "evidence_ids": ["E961"], "review_status": "unreviewed"}

**context-01:** `/dependencies/83`; bajty [566172,567097), SHA-256 `dceca245e6312d304f7ec6fd03250d8efcfccdec00e6ed496ee56c103ad41dc0`.

Zapis modelu: `R961→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "4.32", "description": "Line gaps and Line Command eligibility", "needed_context": "4.32"}

Uzasadnienie modelu: Source refers to 4.32; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R961"], "blocks_full_result": true, "reason": "Line gaps and Line Command eligibility is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D961line", "class": "missing_context", "affected_ids": ["R961", "D961line"], "source_regions": ["pdf-35-core-left"], "reason": "Line gaps and Line Command eligibility is referenced but unavailable.", "needed_context": "4.32", "blocking": true, "evidence_ids": ["E961"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [500,1054), hash wycinka `8b410269ffd54c2aa44c496f060a05320b60caab16f8eef3c3383a83f677a565`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.61 See the Stacking Charts for a summary of the legionary
> stacking advantages. For Romans, the rule of thumb is that two
> Roman infantry units of the same border color can stack without
> penalty. There are exceptions, such as Velites. A Roman stack
> may move together when necessary or desired. It takes two In-
> dividual Orders to move two stacked units (only one, if stacked
> with the OC, and he is giving the orders), but only one LC, if they
> are both eligible. Roman infantry units are also allowed spaces
> between them when determining lines; see 4.32.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D961stack

Źródło / dokładny zakres: 9.61 first sentence: Stacking Charts summary; subsequent rule of thumb and exceptions such as Velites

Cel / dostępność: Actual summary/exception content absent; source does not make consulting summary an execution prerequisite

Konieczność / wpływ: Brak podsumowania nie blokuje odczytania lokalnej zasady orientacyjnej, liczby rozkazów lub samej wzmianki. Pełna legalność konkretnego stosu może wymagać niepodanych wyjątków/zasad; rule of thumb nie wystarcza do każdej sytuacji.

Porównanie / propozycja: Rodzaj mention już zaakceptowany owner-decision05/SEM-015 dla obu wystąpień; nie poddawać ponownie ani wracać do table_use. SEM-019 dotyczy tylko wcześniej wyłączonej konieczności/blocks=true i G-D961stack. Rekomendacja: nie uznać summary za obowiązkowy lookup; zachować missing summary i warunkową blokadę pełnej legalności przez nieznane wyjątki. Nie rekonstruować chart ani bezwarunkowo dopuszczać Velites.

**first-001:** `/dependencies/82`; bajty [487500,488469), SHA-256 `6a302f1a60d0ed6085bd1caff398a75a6fa04cc2533632d1ecd4c684c8aaff8b`.

Zapis modelu: `R961→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Stacking Charts", "description": "Roman stacking summary and exceptions", "needed_context": "Actual Stacking Charts including Roman/Velites exceptions"}

Uzasadnienie modelu: Source refers to Stacking Charts; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R961"], "blocks_full_result": true, "reason": "Roman stacking summary and exceptions is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: mention already owner-decided inSEM-015, rawtable_use retained as immutable observation; no repeated kind decision

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Actual stack legality with unsupplied exceptions remains blocked; summary lookup itself is not an execution prerequisite.

Dosłowny gap: {"id": "G-D961stack", "class": "missing_context", "affected_ids": ["R961", "D961stack"], "source_regions": ["pdf-35-core-left"], "reason": "Roman stacking summary and exceptions is referenced but unavailable.", "needed_context": "Actual Stacking Charts including Roman/Velites exceptions", "blocking": true, "evidence_ids": ["E961"], "review_status": "unreviewed"}

**context-01:** `/dependencies/82`; bajty [565169,566165), SHA-256 `5a64c6a711196f8edc448674e353defd2d3b14e7940528e15e8d0cc130f421b9`.

Zapis modelu: `R961→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Stacking Charts", "description": "Roman stacking summary and exceptions", "needed_context": "Actual Stacking Charts including Roman/Velites exceptions"}

Uzasadnienie modelu: Source refers to Stacking Charts; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R961"], "blocks_full_result": true, "reason": "Roman stacking summary and exceptions is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: mention already owner-decided inSEM-015, rawtable_use retained as immutable observation; no repeated kind decision

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Actual stack legality with unsupplied exceptions remains blocked; summary lookup itself is not an execution prerequisite.

Dosłowny gap: {"id": "G-D961stack", "class": "missing_context", "affected_ids": ["R961", "D961stack"], "source_regions": ["pdf-35-core-left"], "reason": "Roman stacking summary and exceptions is referenced but unavailable.", "needed_context": "Actual Stacking Charts including Roman/Velites exceptions", "blocking": true, "evidence_ids": ["E961"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [500,1054), hash wycinka `8b410269ffd54c2aa44c496f060a05320b60caab16f8eef3c3383a83f677a565`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.61 See the Stacking Charts for a summary of the legionary
> stacking advantages. For Romans, the rule of thumb is that two
> Roman infantry units of the same border color can stack without
> penalty. There are exceptions, such as Velites. A Roman stack
> may move together when necessary or desired. It takes two In-
> dividual Orders to move two stacked units (only one, if stacked
> with the OC, and he is giving the orders), but only one LC, if they
> are both eligible. Roman infantry units are also allowed spaces
> between them when determining lines; see 4.32.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D962auto

Źródło / dokładny zakres: 9.62: automatic Cohesion Hits6.68 apply to each unit in stack

Cel / dostępność: 6.68 automatic-hit triggers/amounts absent;10.13/Step4 concern Shock allocation, not replacement for this target

Konieczność / wpływ: Do rzeczywistego wyzwolenia i liczby automatic Hits potrzeba6.68. Dla zadanych należnych automatic Hits wiadomo, że każda jednostka je otrzymuje.

Porównanie / propozycja: R962→6.68 procedure_use/explicit zgodne w obu. Oddzielić automatic Hits od dzielenia Shock Hits i6.68#6 na dalszej ścieżce. Przyjąć wymaganie, nie domknięcie alokacji ani pełnyR962.

**first-001:** `/dependencies/85`; bajty [490273,491153), SHA-256 `054da6a651c90eab00d6b52e670877eff7c0eccf5caf802f2314fb41d6b5dad6`.

Zapis modelu: `R962→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "6.68", "description": "Automatic stack Cohesion Hits", "needed_context": "6.68"}

Uzasadnienie modelu: Source refers to 6.68; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R962"], "blocks_full_result": true, "reason": "Automatic stack Cohesion Hits is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D962auto", "class": "missing_context", "affected_ids": ["R962", "D962auto"], "source_regions": ["pdf-35-core-left"], "reason": "Automatic stack Cohesion Hits is referenced but unavailable.", "needed_context": "6.68", "blocking": true, "evidence_ids": ["E962"], "review_status": "unreviewed"}

**context-01:** `/dependencies/85`; bajty [568026,568933), SHA-256 `dcf0b2dfba1c795ed3b624de002c7a10790cf4e943e201507ed3af1f65a0372b`.

Zapis modelu: `R962→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "6.68", "description": "Automatic stack Cohesion Hits", "needed_context": "6.68"}

Uzasadnienie modelu: Source refers to 6.68; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R962"], "blocks_full_result": true, "reason": "Automatic stack Cohesion Hits is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D962auto", "class": "missing_context", "affected_ids": ["R962", "D962auto"], "source_regions": ["pdf-35-core-left"], "reason": "Automatic stack Cohesion Hits is referenced but unavailable.", "needed_context": "6.68", "blocking": true, "evidence_ids": ["E962"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [1054,1486), hash wycinka `91a35accdf3555fd2ccb476e47424d42652b37759580247fdde89ab75c367332`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.62 Stacked Roman units combine their Size when attacking or
> defending, but all other ratings, especially TQ, are those of the
> top unit. Stacked Romans must Shock attack the same hex; see
> 8.42. Only the top unit may fire. Each unit makes its own TQ
> check but uses the TQ of the top unit. Automatic Cohesion Hits
> (6.68) are applied to each unit in the stack. Cohesion Hits from
> Shock resolution 8.46 Step 4 are allocated per 10.13.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D962target

Źródło / dokładny zakres: 9.62: stacked Romans must Shock attack same hex; see8.42

Cel / dostępność: 8.42 target eligibility/attack selection absent

Konieczność / wpływ: Pełny legalny wybór celu wymaga8.42. Gdy poprawne cele są zadane, zakaz rozdzielania ataków stosu na różne heksy jest znany.

Porównanie / propozycja: R962→8.42 procedure_use/explicit poparte numerowanym odesłaniem. Gap nie dowodzi, że nieznany jest wymóg same hex. Przyjąć źródłową rolę i zależną pełną kwalifikację, bez treści8.42.

**first-001:** `/dependencies/84`; bajty [489379,490267), SHA-256 `e42ca7da39f4e144b19f3f3c2ffbf0e594f6fa96907649c0ab777738998c6194`.

Zapis modelu: `R962→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "8.42", "description": "Same-hex Shock attack targeting", "needed_context": "8.42"}

Uzasadnienie modelu: Source refers to 8.42; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R962"], "blocks_full_result": true, "reason": "Same-hex Shock attack targeting is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D962target", "class": "missing_context", "affected_ids": ["R962", "D962target"], "source_regions": ["pdf-35-core-left"], "reason": "Same-hex Shock attack targeting is referenced but unavailable.", "needed_context": "8.42", "blocking": true, "evidence_ids": ["E962"], "review_status": "unreviewed"}

**context-01:** `/dependencies/84`; bajty [567104,568019), SHA-256 `4eb07298d503ed6bb1f78ece41fdb0f49a2166074ffc3b5036180980ffaca714`.

Zapis modelu: `R962→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "8.42", "description": "Same-hex Shock attack targeting", "needed_context": "8.42"}

Uzasadnienie modelu: Source refers to 8.42; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R962"], "blocks_full_result": true, "reason": "Same-hex Shock attack targeting is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D962target", "class": "missing_context", "affected_ids": ["R962", "D962target"], "source_regions": ["pdf-35-core-left"], "reason": "Same-hex Shock attack targeting is referenced but unavailable.", "needed_context": "8.42", "blocking": true, "evidence_ids": ["E962"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [1054,1486), hash wycinka `91a35accdf3555fd2ccb476e47424d42652b37759580247fdde89ab75c367332`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.62 Stacked Roman units combine their Size when attacking or
> defending, but all other ratings, especially TQ, are those of the
> top unit. Stacked Romans must Shock attack the same hex; see
> 8.42. Only the top unit may fire. Each unit makes its own TQ
> check but uses the TQ of the top unit. Automatic Cohesion Hits
> (6.68) are applied to each unit in the stack. Cohesion Hits from
> Shock resolution 8.46 Step 4 are allocated per 10.13.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D963TQ

Źródło / dokładny zakres: 9.63: mixed Roman borders or same border/different classes+1 to all TQ checks

Cel / dostępność: General TQ context partially supplied by10.11/8.75; actual timing/result chart and applicable other modifiers absent

Konieczność / wpływ: Nie wolno mówić, że cały TQ processing jest niepozyskany:10.11 podaje die vs TQ i chart result. Brak actual chart/kwalifikacji blokuje pełny ogólny test; lokalny+1 jest znany.

Porównanie / propozycja: R963→all TQ checks modification/explicit zgodne w obu. Przyjąć modyfikację i potrzebę pozostałego kontekstu, uwzględniając już dostarczone10.11. Nie certyfikuje all possible checks/modifier order ani chart cells; źródło nie daje+1 do wszystkich rzutów poza TQ.

**first-001:** `/dependencies/87`; bajty [492115,493097), SHA-256 `9cc9a7f6cd42567f87a7db6d17f660804e7f132ea1eb3063f894a975ea51d899`.

Zapis modelu: `R963→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "all TQ checks", "description": "General TQ check processing to receive stacked-Roman modifier", "needed_context": "TQ check timing and modifiers"}

Uzasadnienie modelu: Source refers to all TQ checks; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R963"], "blocks_full_result": true, "reason": "General TQ check processing to receive stacked-Roman modifier is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D963TQ", "class": "missing_context", "affected_ids": ["R963", "D963TQ"], "source_regions": ["pdf-35-core-left"], "reason": "General TQ check processing to receive stacked-Roman modifier is referenced but unavailable.", "needed_context": "TQ check timing and modifiers", "blocking": true, "evidence_ids": ["E963"], "review_status": "unreviewed"}

**context-01:** `/dependencies/87`; bajty [569967,570976), SHA-256 `772bd319e624d2766a4589cc791b1dc3edb962ee578943e92c07a5103c49ae40`.

Zapis modelu: `R963→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "all TQ checks", "description": "General TQ check processing to receive stacked-Roman modifier", "needed_context": "TQ check timing and modifiers"}

Uzasadnienie modelu: Source refers to all TQ checks; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R963"], "blocks_full_result": true, "reason": "General TQ check processing to receive stacked-Roman modifier is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D963TQ", "class": "missing_context", "affected_ids": ["R963", "D963TQ"], "source_regions": ["pdf-35-core-left"], "reason": "General TQ check processing to receive stacked-Roman modifier is referenced but unavailable.", "needed_context": "TQ check timing and modifiers", "blocking": true, "evidence_ids": ["E963"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [1486,1632), hash wycinka `107e03e7ca5d8effff881e360ef301fcc8991da029e242f4b1cda77044d0b9a6`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.63 For stacked Roman units with different border colors, or of
> the same border color and different classes, there is a +1 DRM
> to all TQ checks.
> 

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/14/text`, znaki [639,1100), hash wycinka `ad14eb29acf309d322fe14c90cacfe825c8c36d6db647ae11521d5768e4d13be`. Oceniana klauzula to source_scope, nie cała koperta.

> 10.11 TQ Checks: The Cohesion Hit and TQ Check Chart gives
> the times during the game when a unit must undergo a TQ check.
> These instances have also been noted throughout the rules. A TQ
> check consists of rolling the die and comparing it to the unit’s
> printed TQ rating, and applying the result given on the chart—
> usually one or more Cohesion Hits if the DR exceeds the rating.
> Exception: Routed units use a TQ of 1 for all TQ checks instead
> of the printed TQ.
> 

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [803,931), hash wycinka `173e80b82aa7d5bcc82f7e015a3d3d6ca314323b85f9cc034b46b12ae41edf2d`. Oceniana klauzula to source_scope, nie cała koperta.

> 8.75 The Cohesion Hit and TQ Check Chart: Use this as
> a summary of when Cohesion Hits are applied and when TQ
> checks take place.

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D964order

Źródło / dokładny zakres: 9.64: changing Roman stack order only by Individual Order, not movement or LC; facing LC permitted

Cel / dostępność: Individual Order eligibility/range/execution absent

Konieczność / wpływ: Realny legalny rozkaz potrzebuje celu. Zakaz zamiany kolejności w LC/ruchu i wyjątek dla facing są znane; facing i stack order to osobne operacje.

Porównanie / propozycja: R964→Individual Order procedure_use/explicit poparte only, oba wyniki zachowują wyjątek facing i top-only single-unit movement. Przyjąć rolę, nie rozszerzyć LC facing do zamiany pozycji jednostek.

**first-001:** `/dependencies/88`; bajty [493103,494081), SHA-256 `5d4d7b6efa10aedb7a067cf23541153558cf3e153dea1aad2b748130bd48756b`.

Zapis modelu: `R964→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Individual Order", "description": "Individual Order for Roman stack-order change", "needed_context": "Individual Order eligibility/range/procedure"}

Uzasadnienie modelu: Source refers to Individual Order; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R964"], "blocks_full_result": true, "reason": "Individual Order for Roman stack-order change is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D964order", "class": "missing_context", "affected_ids": ["R964", "D964order"], "source_regions": ["pdf-35-core-left"], "reason": "Individual Order for Roman stack-order change is referenced but unavailable.", "needed_context": "Individual Order eligibility/range/procedure", "blocking": true, "evidence_ids": ["E964"], "review_status": "unreviewed"}

**context-01:** `/dependencies/88`; bajty [570983,571988), SHA-256 `7a86d1d85ada79ab14327ea6ceaa99c79860aa8e5956151d56534958cfdaecf6`.

Zapis modelu: `R964→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Individual Order", "description": "Individual Order for Roman stack-order change", "needed_context": "Individual Order eligibility/range/procedure"}

Uzasadnienie modelu: Source refers to Individual Order; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R964"], "blocks_full_result": true, "reason": "Individual Order for Roman stack-order change is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D964order", "class": "missing_context", "affected_ids": ["R964", "D964order"], "source_regions": ["pdf-35-core-left"], "reason": "Individual Order for Roman stack-order change is referenced but unavailable.", "needed_context": "Individual Order eligibility/range/procedure", "blocking": true, "evidence_ids": ["E964"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [1632,1885), hash wycinka `52ca8247a97862d6344590886d0029e09739314192a79a720f39b0d9b3b3beae`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.64 Roman Stacking order may be changed/switched only by
> an Individual Order; it may not be part of movement or a Line
> Command, although facing may be changed by LC. If the player
> desires to move only one unit from a stack, only the top unit
> may move.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D966line

Źródło / dokładny zakres: 9.66: all top units in stacks of same Line see4.32 may extend sideways to vacant Flank hexes

Cel / dostępność: 4.32 same-Line definition/eligibility absent

Konieczność / wpływ: Na rzeczywistej planszy należy ustalić same Line. Przy zadanej kwalifikującej linii i heksach lokalny ruch sideways/unchanged facing/unstack only jest znany.

Porównanie / propozycja: R966→4.32 condition/explicit zgodne w obu. Przeczytano dokończenie w prawej kolumnie, nie tylko urwany początek. Przyjąć warunek, nie dowolne MLE dowolnych top units lub stacking together.

**first-001:** `/dependencies/89`; bajty [494087,494996), SHA-256 `1d759a2be5d89e80fde69d0f74bf238ce22a0f13d391cf533cbea664d2097e08`.

Zapis modelu: `R966→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "4.32", "description": "Same-Line eligibility for MLE", "needed_context": "4.32 Line definition and eligibility"}

Uzasadnienie modelu: Source refers to 4.32; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R966"], "blocks_full_result": true, "reason": "Same-Line eligibility for MLE is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D966line", "class": "missing_context", "affected_ids": ["R966", "D966line"], "source_regions": ["pdf-35-core-left"], "reason": "Same-Line eligibility for MLE is referenced but unavailable.", "needed_context": "4.32 Line definition and eligibility", "blocking": true, "evidence_ids": ["E966a"], "review_status": "unreviewed"}

**context-01:** `/dependencies/89`; bajty [571995,572931), SHA-256 `11299e41d6a01c7fc7007847731f49d5465cab64312bb8905c616062cccbb202`.

Zapis modelu: `R966→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "4.32", "description": "Same-Line eligibility for MLE", "needed_context": "4.32 Line definition and eligibility"}

Uzasadnienie modelu: Source refers to 4.32; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R966"], "blocks_full_result": true, "reason": "Same-Line eligibility for MLE is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D966line", "class": "missing_context", "affected_ids": ["R966", "D966line"], "source_regions": ["pdf-35-core-left"], "reason": "Same-Line eligibility for MLE is referenced but unavailable.", "needed_context": "4.32 Line definition and eligibility", "blocking": true, "evidence_ids": ["E966a"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/9/text`, znaki [2061,2363), hash wycinka `78f078da6fa2fe33ab8e624792fedfa3a278aab91723954cab2e31c9131f6459`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [0,327), hash wycinka `1a05ddc906da07e49fe98fead9ee567340ebd447c7976027f2aa2673a971b318`. Oceniana klauzula to source_scope, nie cała koperta.

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D967OW

Źródło / dokładny zakres: 9.67: if enemy movement triggers both OW and MLE they may occur together but by different units

Cel / dostępność: OW trigger, path and execution absent; MLE local reaction rules present

Konieczność / wpływ: Pełne OW wymaga celu. Sama możliwość obu reakcji na ten ruch i zakaz obu dla tych samych jednostek są znane. Przykład Velites/Hastati nie zastępuje ogólnej procedury OW.

Porównanie / propozycja: R967→OW procedure_use/explicit poparte nazwanym działaniem, kierunek zachowany. Przyjąć współużycie warunkowe, nie obowiązkowo pierwszą okazję, nie automatyczną legalność obu ani nowe pozwolenie na OW w dowolnym momencie.

**first-001:** `/dependencies/90`; bajty [495002,496020), SHA-256 `9cbe3a7124fb5b40779c6c31e86a5f000182d5d0cdd9871f85233f00c131a1da`.

Zapis modelu: `R967→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Orderly Withdrawal", "description": "OW potentially concurrent with MLE by different units", "needed_context": "OW procedure, including trigger and withdrawal paths"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R967"], "blocks_full_result": true, "reason": "OW potentially concurrent with MLE by different units is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D967OW", "class": "missing_context", "affected_ids": ["R967", "D967OW"], "source_regions": ["pdf-35-core-right"], "reason": "OW potentially concurrent with MLE by different units is referenced but unavailable.", "needed_context": "OW procedure, including trigger and withdrawal paths", "blocking": true, "evidence_ids": ["E967", "E967ex"], "review_status": "unreviewed"}

**context-01:** `/dependencies/90`; bajty [572938,573984), SHA-256 `df57b67df142af7eb4032064641cb61aa5b4d208c35cc35d24dc492a46e9460a`.

Zapis modelu: `R967→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Orderly Withdrawal", "description": "OW potentially concurrent with MLE by different units", "needed_context": "OW procedure, including trigger and withdrawal paths"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R967"], "blocks_full_result": true, "reason": "OW potentially concurrent with MLE by different units is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D967OW", "class": "missing_context", "affected_ids": ["R967", "D967OW"], "source_regions": ["pdf-35-core-right"], "reason": "OW potentially concurrent with MLE by different units is referenced but unavailable.", "needed_context": "OW procedure, including trigger and withdrawal paths", "blocking": true, "evidence_ids": ["E967", "E967ex"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [327,1022), hash wycinka `663c903a0dd91faa9b986905ab4499c9d429033f39553a28ede49f09513e8940`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.67 Manipular Line Extension may be undertaken as a reaction
> to enemy movement the instant an enemy combat unit comes
> within 2 hexes of a line of stacked Roman units. The Roman
> player may make his choice at any time any enemy unit so places
> itself (that is, he does not have to exercise his MLE rights the first
> time they become available). If enemy movement triggers both
> Orderly Withdrawal as well as MLE, both may be undertaken
> together but not by the same units.
> EXAMPLE: A Velites unit sitting between two Hastati stacks may
> withdraw through the gaps in a Hastati line upon approach of,
> say, an enemy Phalanx and, as soon as that unit is through the
> gap, the Hastati line may undergo MLE.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D968LC

Źródło / dokładny zakres: 9.68: active MLE as Line Command only; both units may move afterwards at MA−2; no MLE Hits

Cel / dostępność: LC eligibility/procedure absent; reaction alternative9.67 independently supplied

Konieczność / wpływ: Pełne active LC potrzebuje celu. LC-only nie znosi odrębnego reaction MLE9.67; local−2MA/no Hits oraz zakaz Column są podane.

Porównanie / propozycja: R968→LC procedure_use/explicit poparte w obu w dokładnym trybie active MLE. Przyjęcie nie obejmuje LC dla reaction ani nowej akceptacji D968column już rozstrzygniętej w innym zakresie.

**first-001:** `/dependencies/91`; bajty [496026,496970), SHA-256 `010f18148fa2853a17c417012e6747ad9482f27bbe88ac9a48aa201cc65bb750`.

Zapis modelu: `R968→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Line Command (only)", "description": "Line Command eligibility for active MLE", "needed_context": "Line Command procedure"}

Uzasadnienie modelu: Source refers to Line Command (only); direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R968"], "blocks_full_result": true, "reason": "Line Command eligibility for active MLE is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D968LC", "class": "missing_context", "affected_ids": ["R968", "D968LC"], "source_regions": ["pdf-35-core-right"], "reason": "Line Command eligibility for active MLE is referenced but unavailable.", "needed_context": "Line Command procedure", "blocking": true, "evidence_ids": ["E968"], "review_status": "unreviewed"}

**context-01:** `/dependencies/91`; bajty [573991,574962), SHA-256 `7aef9ec1708e3537365f3e533254fb417189bd29f7bd4aa8e0da33cfc9b54a7e`.

Zapis modelu: `R968→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Line Command (only)", "description": "Line Command eligibility for active MLE", "needed_context": "Line Command procedure"}

Uzasadnienie modelu: Source refers to Line Command (only); direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R968"], "blocks_full_result": true, "reason": "Line Command eligibility for active MLE is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D968LC", "class": "missing_context", "affected_ids": ["R968", "D968LC"], "source_regions": ["pdf-35-core-right"], "reason": "Line Command eligibility for active MLE is referenced but unavailable.", "needed_context": "Line Command procedure", "blocking": true, "evidence_ids": ["E968"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [1022,1280), hash wycinka `a4e97d4eadd1fc9941198f90c1c9d3c7588f68ab691dd6acae03098517b2fc7d`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.68 Manipular Line Extension may also be undertaken as part
> of a Line Command (only). If undertaken as an LC, both units
> may move after the MLE but with their MA reduced by 2. There
> are no Cohesion Hits applied for the MLE. Units in Column may
> not use MLE.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D971LOS

Źródło / dokładny zakres: 9.71 first alternative: non-Elephant enemy combat unit within3 hexes AND LOS of any Triarii line unit

Cel / dostępność: General LOS geometric definition/test absent

Konieczność / wpływ: Realne LOS wymaga definicji; przy zadanym LOS i kwalifikującym enemy znana pierwsza alternatywa. Druga alternatywa≥6hexes ma osobny zakres i nie wymaga LOS; facing dozwolone przed release.

Porównanie / propozycja: R971→LOS definition/explicit poparte jawnym nazwaniem LOS jako testowanego warunku, bez numeru. Nie potwierdza geometrii/zasłon. Przyjąć wymaganie tylko pierwszej alternatywy; nie scalać9.71 i9.72 ani zamykaćSEM-011/EXP-052.

**first-001:** `/dependencies/93`; bajty [497906,498828), SHA-256 `31cfc93016392d406779554ef335816ca3844664873b455596251a866060cd26`.

Zapis modelu: `R971→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "LOS", "description": "LOS test necessary for enemy proximity release", "needed_context": "Line of Sight rules"}

Uzasadnienie modelu: Source refers to LOS; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R971"], "blocks_full_result": true, "reason": "LOS test necessary for enemy proximity release is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D971LOS", "class": "missing_context", "affected_ids": ["R971", "D971LOS"], "source_regions": ["pdf-35-core-right"], "reason": "LOS test necessary for enemy proximity release is referenced but unavailable.", "needed_context": "Line of Sight rules", "blocking": true, "evidence_ids": ["E971"], "review_status": "unreviewed"}

**context-01:** `/dependencies/93`; bajty [575927,576876), SHA-256 `20b2270687f29a58f8f7cb78482dd6b11ecc3d1ec61b2a3e291776ed9fb062a6`.

Zapis modelu: `R971→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "LOS", "description": "LOS test necessary for enemy proximity release", "needed_context": "Line of Sight rules"}

Uzasadnienie modelu: Source refers to LOS; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R971"], "blocks_full_result": true, "reason": "LOS test necessary for enemy proximity release is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D971LOS", "class": "missing_context", "affected_ids": ["R971", "D971LOS"], "source_regions": ["pdf-35-core-right"], "reason": "LOS test necessary for enemy proximity release is referenced but unavailable.", "needed_context": "Line of Sight rules", "blocking": true, "evidence_ids": ["E971"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [1695,2066), hash wycinka `a19914ca0603e239cd7d49a13a491ffcf3c3d23f44d1e1783cb7ec7c05438e21`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.71 Triarii units cannot move, but may change facing, until and
> unless one of the following occurs:
> • There is an enemy combat unit, other than an Elephant unit,
> which is within 3 hexes and LOS of any unit in the Triarii line,
> or
> • The Triarii units are at least 6 hexes from all other Roman or
> Ala—but not allied–infantry lines, be they Hastati, Principes
> or whatever.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D972AWL

Źródło / dokładny zakres: 9.72: RP≥floor(AWL/2) for move-and-Shock gate

Cel / dostępność: Named AWL parameter definition/value for selected scenario absent

Konieczność / wpływ: Realnego progu nie obliczymy bez AWL. Przy zadanym AWL połowa/floor i porównanie są znane. Stationary Shock exception nie czeka na AWL.

Porównanie / propozycja: R972→AWL definition/explicit przyjąć wyłącznie jako potrzebę znaczenia/wartości nazwanego parametru, nie jako dostarczoną definicję ani jej lokalizację w konkretnym scenario. Actualvalue, army withdrawal execution i łączność bramek wyłączone.

**first-001:** `/dependencies/94`; bajty [498834,499824), SHA-256 `4a21ff6572b64f4de714510485713fa79f1ce767c3c9c9aac8a19764461efee9`.

Zapis modelu: `R972→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Army Withdrawal Level", "description": "Scenario value for Triarii half-withdrawal threshold", "needed_context": "Selected scenario Army Withdrawal Level"}

Uzasadnienie modelu: Source refers to Army Withdrawal Level; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R972"], "blocks_full_result": true, "reason": "Scenario value for Triarii half-withdrawal threshold is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D972AWL", "class": "missing_context", "affected_ids": ["R972", "D972AWL"], "source_regions": ["pdf-35-core-right"], "reason": "Scenario value for Triarii half-withdrawal threshold is referenced but unavailable.", "needed_context": "Selected scenario Army Withdrawal Level", "blocking": true, "evidence_ids": ["E972"], "review_status": "unreviewed"}

**context-01:** `/dependencies/94`; bajty [576883,577900), SHA-256 `8ae6913c175efdfe39893ce883e6d9cf1f6782cd2006f1dadfb6e6cdeb0c996e`.

Zapis modelu: `R972→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Army Withdrawal Level", "description": "Scenario value for Triarii half-withdrawal threshold", "needed_context": "Selected scenario Army Withdrawal Level"}

Uzasadnienie modelu: Source refers to Army Withdrawal Level; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R972"], "blocks_full_result": true, "reason": "Scenario value for Triarii half-withdrawal threshold is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D972AWL", "class": "missing_context", "affected_ids": ["R972", "D972AWL"], "source_regions": ["pdf-35-core-right"], "reason": "Scenario value for Triarii half-withdrawal threshold is referenced but unavailable.", "needed_context": "Selected scenario Army Withdrawal Level", "blocking": true, "evidence_ids": ["E972"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [2066,2321), hash wycinka `9015a600ac9342bae6f5a305e4e7b9e62aa6e578398381968f2dffe52e4db010`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D972RP

Źródło / dokładny zakres: 9.72: Roman army Rout Points compared with rounded-down half AWL

Cel / dostępność: RP definition/accounting/current army value absent

Konieczność / wpływ: Realny stan RP wymaga zasad/liczenia. Dla zadanych RP/AWL porównanie jest znane, stationary exception nie wymaga wyliczenia progu.

Porównanie / propozycja: R972→RP definition/explicit poparte nazwanym parametrem. Przyjąć rolę wymaganej definicji/liczenia, nie treść całych army withdrawal rules ani zgodność konkretnego stanu. Obie bramki iSEM-011 nadal otwarte.

**first-001:** `/dependencies/95`; bajty [499830,500811), SHA-256 `90e0205d9990fe39f8bf0fdae54155743fbc23224c3c38aec98a1b877bc6890f`.

Zapis modelu: `R972→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Rout Points", "description": "Roman Rout Point accounting needed for Triarii release", "needed_context": "Rout Point calculation and army withdrawal rules"}

Uzasadnienie modelu: Source refers to Rout Points; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R972"], "blocks_full_result": true, "reason": "Roman Rout Point accounting needed for Triarii release is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D972RP", "class": "missing_context", "affected_ids": ["R972", "D972RP"], "source_regions": ["pdf-35-core-right"], "reason": "Roman Rout Point accounting needed for Triarii release is referenced but unavailable.", "needed_context": "Rout Point calculation and army withdrawal rules", "blocking": true, "evidence_ids": ["E972"], "review_status": "unreviewed"}

**context-01:** `/dependencies/95`; bajty [577907,578915), SHA-256 `ee6d3b8bd27706ed788fc546809a027b66867b195960a22b4fd15b4d135ee1d4`.

Zapis modelu: `R972→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Rout Points", "description": "Roman Rout Point accounting needed for Triarii release", "needed_context": "Rout Point calculation and army withdrawal rules"}

Uzasadnienie modelu: Source refers to Rout Points; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R972"], "blocks_full_result": true, "reason": "Roman Rout Point accounting needed for Triarii release is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D972RP", "class": "missing_context", "affected_ids": ["R972", "D972RP"], "source_regions": ["pdf-35-core-right"], "reason": "Roman Rout Point accounting needed for Triarii release is referenced but unavailable.", "needed_context": "Rout Point calculation and army withdrawal rules", "blocking": true, "evidence_ids": ["E972"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/10/text`, znaki [2066,2321), hash wycinka `9015a600ac9342bae6f5a305e4e7b9e62aa6e578398381968f2dffe52e4db010`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D983stack

Źródło / dokładny zakres: 9.83: maximum one Scorpio per hex; all other stacking rules apply

Cel / dostępność: Other stacking restrictions absent

Konieczność / wpływ: Limit jednego Scorpio jest znany. Czy może dzielić heks z inną klasą, zależy od brakujących ograniczeń; maximum1 nie oznacza całkowitego zakazu innych units.

Porównanie / propozycja: R983→other stacking condition/explicit właściwe w obu. To klauzula zachowująca obowiązywanie, nie summary mention. Przyjąć potrzebę pozostałych ograniczeń, nie ich zawartość ani pełną legalność stosu.

**first-001:** `/dependencies/96`; bajty [500817,501770), SHA-256 `6b4a95b49a6c08a4e6483ad868d737cb785fcef19e1e38f712aafc9e08bbf4be`.

Zapis modelu: `R983→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "All other stacking rules", "description": "Other Scorpio stacking constraints", "needed_context": "General stacking restrictions"}

Uzasadnienie modelu: Source refers to All other stacking rules; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R983"], "blocks_full_result": true, "reason": "Other Scorpio stacking constraints is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D983stack", "class": "missing_context", "affected_ids": ["R983", "D983stack"], "source_regions": ["pdf-36-core-left"], "reason": "Other Scorpio stacking constraints is referenced but unavailable.", "needed_context": "General stacking restrictions", "blocking": true, "evidence_ids": ["E983"], "review_status": "unreviewed"}

**context-01:** `/dependencies/96`; bajty [578922,579902), SHA-256 `c95fb9d12833a59f9d20c9508fe6757a71d63500ecd924c9a8eef0153b1a4632`.

Zapis modelu: `R983→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "All other stacking rules", "description": "Other Scorpio stacking constraints", "needed_context": "General stacking restrictions"}

Uzasadnienie modelu: Source refers to All other stacking rules; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R983"], "blocks_full_result": true, "reason": "Other Scorpio stacking constraints is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D983stack", "class": "missing_context", "affected_ids": ["R983", "D983stack"], "source_regions": ["pdf-36-core-left"], "reason": "Other Scorpio stacking constraints is referenced but unavailable.", "needed_context": "General stacking restrictions", "blocking": true, "evidence_ids": ["E983"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/11/text`, znaki [944,1027), hash wycinka `55c3a6de318b07cfc9c419776ac88cc426ade50518accc59987d6eaaefaf7bda`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.83 Only one Scorpio unit may occupy any one hex. All other
> stacking rules apply.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D987recovery

Źródło / dokładny zakres: 9.87: Scorpio incurs/recovers Hits as ordinary units; routing immediately eliminates it

Cel / dostępność: Normal Hit/recovery eligibility/execution absent or partial;10.11 gives general TQ framework, not recovery orders

Konieczność / wpływ: Faktyczne recovering wymaga procedury. Przy zadanym rout natychmiastowa eliminacja jest znana; odzyskiwanie Hits nie daje rally po rout.

Porównanie / propozycja: R987→normal Hits/recovery procedure_use/explicit zgodne. Nie twierdzić, że brak całego framework Hits, bo fragment10.11 jest dostarczony. Przyjąć wymaganie pozostałej procedury, nie zwykłe rally dlaScorpio ani całego ogólnegoHits.

**first-001:** `/dependencies/98`; bajty [502743,503772), SHA-256 `747ee76868b936260cd81aabf8f2f2cd620b037983be6b0363d9af3f4f95ef32`.

Zapis modelu: `R987→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "incur and recover Cohesion Hits as any other unit", "description": "Normal Scorpio Hits/recovery processing", "needed_context": "Cohesion Hit and Recovery procedure"}

Uzasadnienie modelu: Source refers to incur and recover Cohesion Hits as any other unit; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R987"], "blocks_full_result": true, "reason": "Normal Scorpio Hits/recovery processing is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D987recovery", "class": "missing_context", "affected_ids": ["R987", "D987recovery"], "source_regions": ["pdf-36-core-left"], "reason": "Normal Scorpio Hits/recovery processing is referenced but unavailable.", "needed_context": "Cohesion Hit and Recovery procedure", "blocking": true, "evidence_ids": ["E987"], "review_status": "unreviewed"}

**context-01:** `/dependencies/98`; bajty [580904,581960), SHA-256 `18ea840392e9c6c097980783d0d6e36af24ef8efd50cdf8b8b1e6f0a495cb963`.

Zapis modelu: `R987→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "incur and recover Cohesion Hits as any other unit", "description": "Normal Scorpio Hits/recovery processing", "needed_context": "Cohesion Hit and Recovery procedure"}

Uzasadnienie modelu: Source refers to incur and recover Cohesion Hits as any other unit; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R987"], "blocks_full_result": true, "reason": "Normal Scorpio Hits/recovery processing is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D987recovery", "class": "missing_context", "affected_ids": ["R987", "D987recovery"], "source_regions": ["pdf-36-core-left"], "reason": "Normal Scorpio Hits/recovery processing is referenced but unavailable.", "needed_context": "Cohesion Hit and Recovery procedure", "blocking": true, "evidence_ids": ["E987"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/11/text`, znaki [2143,2256), hash wycinka `f277d375409bd3831f947cdf3dee103a2afb9ee525259e0f860816a4c5272eee`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.87 Scorpios incur and recover Cohesion Hits as any other unit.
> A Scorpio that routs is immediately eliminated.
> 

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/14/text`, znaki [639,1100), hash wycinka `ad14eb29acf309d322fe14c90cacfe825c8c36d6db647ae11521d5768e4d13be`. Oceniana klauzula to source_scope, nie cała koperta.

> 10.11 TQ Checks: The Cohesion Hit and TQ Check Chart gives
> the times during the game when a unit must undergo a TQ check.
> These instances have also been noted throughout the rules. A TQ
> check consists of rolling the die and comparing it to the unit’s
> printed TQ rating, and applying the result given on the chart—
> usually one or more Cohesion Hits if the DR exceeds the rating.
> Exception: Routed units use a TQ of 1 for all TQ checks instead
> of the printed TQ.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D993depleted

Źródło / dokładny zakres: 9.93: Depleted BI eliminated instead of routing

Cel / dostępność: Depleted definition/determination absent

Konieczność / wpływ: Czy realny BI ma Depleted wymaga celu. Dla zadanej Depleted BI i zdarzenia rout zastąpienie eliminacją jest znane.

Porównanie / propozycja: R993→Depleted definition/explicit poparte nazwaniem statusu. Przyjąć potrzebę jego określenia, nie utożsamić Depleted z każdym BI lub liczbąHits; zwykłeBI mogą mieć inną gałąź.

**first-001:** `/dependencies/103`; bajty [507488,508455), SHA-256 `dbbddecac8ebaa216b3a11f4cf0dd15f363c6caf3638fa5874ca4aa60c2e0a8e`.

Zapis modelu: `R993→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Depleted BI", "description": "Depleted status necessary for rout replacement", "needed_context": "Depletion definition and determination"}

Uzasadnienie modelu: Source refers to Depleted BI; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R993"], "blocks_full_result": true, "reason": "Depleted status necessary for rout replacement is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D993depleted", "class": "missing_context", "affected_ids": ["R993", "D993depleted"], "source_regions": ["pdf-36-core-right"], "reason": "Depleted status necessary for rout replacement is referenced but unavailable.", "needed_context": "Depletion definition and determination", "blocking": true, "evidence_ids": ["E993"], "review_status": "unreviewed"}

**context-01:** `/dependencies/103`; bajty [585789,586783), SHA-256 `70da84c50e6510aa2ed451bf7e6b2d39f7e5b32fc10d7202e81a6c9c45ad7587`.

Zapis modelu: `R993→candidate`, `definition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Depleted BI", "description": "Depleted status necessary for rout replacement", "needed_context": "Depletion definition and determination"}

Uzasadnienie modelu: Source refers to Depleted BI; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R993"], "blocks_full_result": true, "reason": "Depleted status necessary for rout replacement is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D993depleted", "class": "missing_context", "affected_ids": ["R993", "D993depleted"], "source_regions": ["pdf-36-core-right"], "reason": "Depleted status necessary for rout replacement is referenced but unavailable.", "needed_context": "Depletion definition and determination", "blocking": true, "evidence_ids": ["E993"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [94,235), hash wycinka `453b6598ced1c78aa0eab7e5bf505372b9e998929b7152198488d3354151414d`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.93 Rout and Recovery
> BI units can only remove 1 Cohesion Hit per Recovery order.
> Depleted BI units do not Rout but are instead eliminated.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D993recovery

Źródło / dokładny zakres: 9.93: BI removes only1 Hit per Recovery order

Cel / dostępność: Recovery eligibility/order execution absent

Konieczność / wpływ: Legalny Recovery wymaga celu; dla zadanej poprawnej operacji limit1Hit jest lokalnie znany. Brak procedury nie pozwala zakładać nieograniczonych rozkazów.

Porównanie / propozycja: R993→Recovery modification/explicit zgodne. Przyjąć zmianę wielkości recovery i blokadę rzeczywistej kwalifikacji; nie 1Hit perGameTurn lub perPhase, lecz perorder.

**first-001:** `/dependencies/102`; bajty [506517,507482), SHA-256 `9942daeb76589b47734b6a5bb4ed6a16d0b4634210cdb5074dad0e29f57f6ea7`.

Zapis modelu: `R993→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Recovery order", "description": "Normal Recovery modified to 1 Hit for BI", "needed_context": "Recovery order eligibility and procedure"}

Uzasadnienie modelu: Source refers to Recovery order; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R993"], "blocks_full_result": true, "reason": "Normal Recovery modified to 1 Hit for BI is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D993recovery", "class": "missing_context", "affected_ids": ["R993", "D993recovery"], "source_regions": ["pdf-36-core-right"], "reason": "Normal Recovery modified to 1 Hit for BI is referenced but unavailable.", "needed_context": "Recovery order eligibility and procedure", "blocking": true, "evidence_ids": ["E993"], "review_status": "unreviewed"}

**context-01:** `/dependencies/102`; bajty [584790,585782), SHA-256 `3be111208203601e25dd9b39ddb69623bd4b9badaba05fbf969fd13083064144`.

Zapis modelu: `R993→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Recovery order", "description": "Normal Recovery modified to 1 Hit for BI", "needed_context": "Recovery order eligibility and procedure"}

Uzasadnienie modelu: Source refers to Recovery order; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R993"], "blocks_full_result": true, "reason": "Normal Recovery modified to 1 Hit for BI is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D993recovery", "class": "missing_context", "affected_ids": ["R993", "D993recovery"], "source_regions": ["pdf-36-core-right"], "reason": "Normal Recovery modified to 1 Hit for BI is referenced but unavailable.", "needed_context": "Recovery order eligibility and procedure", "blocking": true, "evidence_ids": ["E993"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [94,235), hash wycinka `453b6598ced1c78aa0eab7e5bf505372b9e998929b7152198488d3354151414d`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.93 Rout and Recovery
> BI units can only remove 1 Cohesion Hit per Recovery order.
> Depleted BI units do not Rout but are instead eliminated.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D994pre

Źródło / dokładny zakres: 9.94: Ferocious BI−1 Pre-Shock TQ; defending units+2

Cel / dostępność: Base Pre-Shock check absent; Ferocity local state/check supplied subject to leader data

Konieczność / wpływ: Pełny test potrzebuje celu. Przy zadanych prawidłowych rzutach i Ferocity oba modyfikatory znane; Ferocity check vs Initiative to inny rzut.

Porównanie / propozycja: R994→Pre-Shock modification/explicit zgodne. Nie przenosi−1/+2 do Ferocity check lub Momentum. Przyjąć rolę, strony i potrzebę base, nie cały Ferocity record lub leader rating.

**first-001:** `/dependencies/105`; bajty [509531,510509), SHA-256 `28970ea22c2c2cfb5a9f9809dfb669ebc75478fd288c9c5e141607d0df6853ba`.

Zapis modelu: `R994→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Pre-Shock TQ die roll", "description": "Base Pre-Shock process to receive Ferocity modifiers", "needed_context": "Pre-Shock check procedure"}

Uzasadnienie modelu: Source refers to Pre-Shock TQ die roll; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R994"], "blocks_full_result": true, "reason": "Base Pre-Shock process to receive Ferocity modifiers is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D994pre", "class": "missing_context", "affected_ids": ["R994", "D994pre"], "source_regions": ["pdf-36-core-right"], "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.", "needed_context": "Pre-Shock check procedure", "blocking": true, "evidence_ids": ["E994"], "review_status": "unreviewed"}

**context-01:** `/dependencies/105`; bajty [587888,588893), SHA-256 `9a2f923b95b4c6d106afe20ccba60a6d1bd6a57372d9969767c776e31ce44d6f`.

Zapis modelu: `R994→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Pre-Shock TQ die roll", "description": "Base Pre-Shock process to receive Ferocity modifiers", "needed_context": "Pre-Shock check procedure"}

Uzasadnienie modelu: Source refers to Pre-Shock TQ die roll; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R994"], "blocks_full_result": true, "reason": "Base Pre-Shock process to receive Ferocity modifiers is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D994pre", "class": "missing_context", "affected_ids": ["R994", "D994pre"], "source_regions": ["pdf-36-core-right"], "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.", "needed_context": "Pre-Shock check procedure", "blocking": true, "evidence_ids": ["E994"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [621,1322), hash wycinka `656d7ad7b18622813c76dce19fa8b3ca15e986d97b3cba50261648a32bdbdf11`. Oceniana klauzula to source_scope, nie cała koperta.

> All BI units start the game with Ferocity. A BI unit with Ferocity
> earns a –1 DRM to its Pre-Shock TQ die roll while penalizing
> the defending unit(s) with a +2 DRM to their Pre-Shock TQ die
> roll(s).
> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D994scenario

Źródło / dokładny zakres: 9.94: leader as given in scenario setup; test versus Initiative; loss only that command

Cel / dostępność: Actual leader assignment/Initiative absent; source of numeric Initiative not proven by scenario wording alone

Konieczność / wpływ: Dla rzeczywistego testu potrzeba przypisania i wartości Initiative; zadane dane wystarczą doDR≤Initiative. Setup wyznacza leader, nie dowodzi że tabela Initiative jest w setup.

Porównanie / propozycja: R994→scenario condition/explicit poparte assignment. Kandydat łączy to z potrzebą ratingu: przyjąć zapotrzebowanie na oba dane, bez tożsamości ich locatora. Nie rozszerzać utraty naBIinnychleaders lub wszystkie armies.

**first-001:** `/dependencies/104`; bajty [508461,509525), SHA-256 `41294f6f2e6a5a90e4479605f0d0c4fe1c0b4becf753f74623ec8e12c81651db`.

Zapis modelu: `R994→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "scenario setup", "description": "Leader assignment and Initiative needed for command-specific Ferocity checks", "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings"}

Uzasadnienie modelu: Source refers to scenario setup; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R994"], "blocks_full_result": true, "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D994scenario", "class": "missing_context", "affected_ids": ["R994", "D994scenario"], "source_regions": ["pdf-36-core-right"], "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.", "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings", "blocking": true, "evidence_ids": ["E994"], "review_status": "unreviewed"}

**context-01:** `/dependencies/104`; bajty [586790,587881), SHA-256 `ebc246146d446188ee89b3468c94cfe3888ee9fbc7cd9018538db5be63e34c84`.

Zapis modelu: `R994→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "scenario setup", "description": "Leader assignment and Initiative needed for command-specific Ferocity checks", "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings"}

Uzasadnienie modelu: Source refers to scenario setup; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R994"], "blocks_full_result": true, "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D994scenario", "class": "missing_context", "affected_ids": ["R994", "D994scenario"], "source_regions": ["pdf-36-core-right"], "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.", "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings", "blocking": true, "evidence_ids": ["E994"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [621,1322), hash wycinka `656d7ad7b18622813c76dce19fa8b3ca15e986d97b3cba50261648a32bdbdf11`. Oceniana klauzula to source_scope, nie cała koperta.

> All BI units start the game with Ferocity. A BI unit with Ferocity
> earns a –1 DRM to its Pre-Shock TQ die roll while penalizing
> the defending unit(s) with a +2 DRM to their Pre-Shock TQ die
> roll(s).
> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D995momentum

Źródło / dokładny zakres: 9.95: BI-commanding leader−1 to all first-try Momentum rolls

Cel / dostępność: Momentum qualifications/first-try procedure absent

Konieczność / wpływ: Pełne Momentum wymaga celu. Przy zadanym prawidłowym first-try roll−1 znane; nie dotyczy automatycznie każdej kolejnej próby.

Porównanie / propozycja: R995→first-try Momentum modification/explicit właściwe w obu. Przyjąć modyfikację i potrzebę first-try definition, bez domyślnego rozszerzenia na wszystkie rzuty leadera lub dowolneMomentum.

**first-001:** `/dependencies/106`; bajty [510515,511549), SHA-256 `202d8df482e6837e00aca86137c2850a8f7f6c192a5a9f13116c33834167b098`.

Zapis modelu: `R995→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "first-try Momentum die rolls", "description": "First-try Momentum process to receive Impetuosity modifier", "needed_context": "Momentum rules including first-try definition"}

Uzasadnienie modelu: Source refers to first-try Momentum die rolls; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R995"], "blocks_full_result": true, "reason": "First-try Momentum process to receive Impetuosity modifier is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D995momentum", "class": "missing_context", "affected_ids": ["R995", "D995momentum"], "source_regions": ["pdf-36-core-right"], "reason": "First-try Momentum process to receive Impetuosity modifier is referenced but unavailable.", "needed_context": "Momentum rules including first-try definition", "blocking": true, "evidence_ids": ["E995"], "review_status": "unreviewed"}

**context-01:** `/dependencies/106`; bajty [588900,589961), SHA-256 `0ef9e404c7972017d2f131985fec0ff77046887361159035efade27926bafc1d`.

Zapis modelu: `R995→candidate`, `modification/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "first-try Momentum die rolls", "description": "First-try Momentum process to receive Impetuosity modifier", "needed_context": "Momentum rules including first-try definition"}

Uzasadnienie modelu: Source refers to first-try Momentum die rolls; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R995"], "blocks_full_result": true, "reason": "First-try Momentum process to receive Impetuosity modifier is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D995momentum", "class": "missing_context", "affected_ids": ["R995", "D995momentum"], "source_regions": ["pdf-36-core-right"], "reason": "First-try Momentum process to receive Impetuosity modifier is referenced but unavailable.", "needed_context": "Momentum rules including first-try definition", "blocking": true, "evidence_ids": ["E995"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [1322,1895), hash wycinka `317a456b470533b735fa5d68027f5385d568b359bde804b811a58fb0891ed047`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.95 Barbarian Impetuosity
> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D995scenario

Źródło / dokładny zakres: 9.95: Impetuosity loss only BI of triggering leader command per scenario setup

Cel / dostępność: Selected BI command membership absent

Konieczność / wpływ: Realne przypisanieBIpotrzebuje setup. Przy zadanej komendzie i triggerze lokalny zakres i koniec poreszcieGameTurn są znane.

Porównanie / propozycja: R995→scenario condition/explicit poparte literalnym per scenario setup. Przyjąć dane command i warunkową blokadę realnego przypisania, nie nową listęunits lub utratębonusów całej armii.

**first-001:** `/dependencies/107`; bajty [511555,512521), SHA-256 `4aba09db3b479f7ac90ea468848dffcfa0ead16dcf5d42d2f5802480e9513276`.

Zapis modelu: `R995→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "scenario setup", "description": "BI command assignment for Impetuosity loss", "needed_context": "Selected scenario BI command assignments"}

Uzasadnienie modelu: Source refers to scenario setup; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R995"], "blocks_full_result": true, "reason": "BI command assignment for Impetuosity loss is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D995scenario", "class": "missing_context", "affected_ids": ["R995", "D995scenario"], "source_regions": ["pdf-36-core-right"], "reason": "BI command assignment for Impetuosity loss is referenced but unavailable.", "needed_context": "Selected scenario BI command assignments", "blocking": true, "evidence_ids": ["E995"], "review_status": "unreviewed"}

**context-01:** `/dependencies/107`; bajty [589968,590961), SHA-256 `4564aa19917a189c1fe269f83a5358b4032ceacf0d07f2f2a529cbba96ad427d`.

Zapis modelu: `R995→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "scenario setup", "description": "BI command assignment for Impetuosity loss", "needed_context": "Selected scenario BI command assignments"}

Uzasadnienie modelu: Source refers to scenario setup; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R995"], "blocks_full_result": true, "reason": "BI command assignment for Impetuosity loss is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D995scenario", "class": "missing_context", "affected_ids": ["R995", "D995scenario"], "source_regions": ["pdf-36-core-right"], "reason": "BI command assignment for Impetuosity loss is referenced but unavailable.", "needed_context": "Selected scenario BI command assignments", "blocking": true, "evidence_ids": ["E995"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [1322,1895), hash wycinka `317a456b470533b735fa5d68027f5385d568b359bde804b811a58fb0891ed047`. Oceniana klauzula to source_scope, nie cała koperta.

> 9.95 Barbarian Impetuosity
> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996HD

Źródło / dokładny zakres: 9.96: LI mounted on CH may H&D as cavalry

Cel / dostępność: Cavalry-style H&D qualification/execution absent;9.31 supplies only separate LC rule, not full8.3

Konieczność / wpływ: Wystrzelenie/rozstrzygnięcieH&D wymaga procedury. Lokalna możliwość korzystania jak cavalry znana; nie nadaje wszystkich innych cech cavalry mountedLI.

Porównanie / propozycja: R996d→H&D procedure_use/explicit zgodne nazwane użycie. Przyjąć potrzebę procedury w tym trybie, nie mapę/ścieżkę/odległość lub przeniesienie wszelkich cavalry bonuses.

**first-001:** `/dependencies/115`; bajty [519510,520576), SHA-256 `63d35f1e5a6195a9b190d5f3e070197e638df80a1a89516cac95be7d0f3dfcd2`.

Zapis modelu: `R996d→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Harassment and Dispersal fire as if they were cavalry units", "description": "Mounted LI cavalry-style H&D procedure", "needed_context": "Harassment and Dispersal procedure including cavalry conditions"}

Uzasadnienie modelu: Source refers to Harassment and Dispersal fire as if they were cavalry units; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996d"], "blocks_full_result": true, "reason": "Mounted LI cavalry-style H&D procedure is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996HD", "class": "missing_context", "affected_ids": ["R996d", "D996HD"], "source_regions": ["pdf-37-core-left"], "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.", "needed_context": "Harassment and Dispersal procedure including cavalry conditions", "blocking": true, "evidence_ids": ["E996e"], "review_status": "unreviewed"}

**context-01:** `/dependencies/115`; bajty [598147,599240), SHA-256 `1879264ea54a4a4698db24c440219ae8bbfa78eb129ae55b5152fdc63a1ca062`.

Zapis modelu: `R996d→candidate`, `procedure_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Harassment and Dispersal fire as if they were cavalry units", "description": "Mounted LI cavalry-style H&D procedure", "needed_context": "Harassment and Dispersal procedure including cavalry conditions"}

Uzasadnienie modelu: Source refers to Harassment and Dispersal fire as if they were cavalry units; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996d"], "blocks_full_result": true, "reason": "Mounted LI cavalry-style H&D procedure is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996HD", "class": "missing_context", "affected_ids": ["R996d", "D996HD"], "source_regions": ["pdf-37-core-left"], "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.", "needed_context": "Harassment and Dispersal procedure including cavalry conditions", "blocking": true, "evidence_ids": ["E996e"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/13/text`, znaki [826,1427), hash wycinka `784b85e429dd0ad8fb2fac5f1ac3aec58712801cb7787d31eea12fd0e27b17a8`. Oceniana klauzula to source_scope, nie cała koperta.

> LI mounted on CH units have the following special abilities/
> liabilities:
> • LI do not suffer any Cohesion Hits for moving a second (and
> third) time in a Game Turn, if they spend the entire Orders
> Phase mounted on the CH unit.
> • LI cannot Shock attack; they must dismount to do so. When
> mounted, they defend as LI.
> • LI may use Missile Fire using the Mounted Javelin row on the
> MRRC. Missile Supply (8.17) does not apply while the LI unit
> is mounted. Remove any MiSSile low/No markers from the LI
> unit when the unit mounts a CH. They may use Harassment
> and Dispersal fire as if they were cavalry units.

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996MRRC

Źródło / dokładny zakres: 9.96: mounted LI Missile Fire uses Mounted Javelin row of MRRC

Cel / dostępność: Actual Mounted Javelin row/headers/notes absent;8.71 describes only chart purpose

Konieczność / wpływ: Wynik/range wymagająrow; nazwa wiersza znana. Opis8.71 i możliwośćfire nie zastępują wartości tabeli.

Porównanie / propozycja: R996d→MRRC row table_use/explicit poprawnie wskazuje row w obu. Przyjąć źródłowy lookup i brak actual cells, bez utożsamiania ze wszystkimi strzelcami lub Elephant Screen.

**first-001:** `/dependencies/113`; bajty [517538,518516), SHA-256 `14d464152bcf580228f1e7095cbef23920006955a9703a60d6fc5f7c157f52d9`.

Zapis modelu: `R996d→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Mounted Javelin row on the MRRC", "description": "Mounted LI missile range/results", "needed_context": "MRRC Mounted Javelin row, headers and notes"}

Uzasadnienie modelu: Source refers to Mounted Javelin row on the MRRC; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996d"], "blocks_full_result": true, "reason": "Mounted LI missile range/results is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996MRRC", "class": "missing_context", "affected_ids": ["R996d", "D996MRRC"], "source_regions": ["pdf-37-core-left"], "reason": "Mounted LI missile range/results is referenced but unavailable.", "needed_context": "MRRC Mounted Javelin row, headers and notes", "blocking": true, "evidence_ids": ["E996e"], "review_status": "unreviewed"}

**context-01:** `/dependencies/113`; bajty [596119,597124), SHA-256 `db3c062462f2666883ef2fc1da244d55292d990ea71d8213b9e9f2147d03e45e`.

Zapis modelu: `R996d→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Mounted Javelin row on the MRRC", "description": "Mounted LI missile range/results", "needed_context": "MRRC Mounted Javelin row, headers and notes"}

Uzasadnienie modelu: Source refers to Mounted Javelin row on the MRRC; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996d"], "blocks_full_result": true, "reason": "Mounted LI missile range/results is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996MRRC", "class": "missing_context", "affected_ids": ["R996d", "D996MRRC"], "source_regions": ["pdf-37-core-left"], "reason": "Mounted LI missile range/results is referenced but unavailable.", "needed_context": "MRRC Mounted Javelin row, headers and notes", "blocking": true, "evidence_ids": ["E996e"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/13/text`, znaki [826,1427), hash wycinka `784b85e429dd0ad8fb2fac5f1ac3aec58712801cb7787d31eea12fd0e27b17a8`. Oceniana klauzula to source_scope, nie cała koperta.

> LI mounted on CH units have the following special abilities/
> liabilities:
> • LI do not suffer any Cohesion Hits for moving a second (and
> third) time in a Game Turn, if they spend the entire Orders
> Phase mounted on the CH unit.
> • LI cannot Shock attack; they must dismount to do so. When
> mounted, they defend as LI.
> • LI may use Missile Fire using the Mounted Javelin row on the
> MRRC. Missile Supply (8.17) does not apply while the LI unit
> is mounted. Remove any MiSSile low/No markers from the LI
> unit when the unit mounts a CH. They may use Harassment
> and Dispersal fire as if they were cavalry units.

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/1/text`, znaki [22,152), hash wycinka `6d536a1df692b011b2266ea6a564038d9b9444918a402e57a151b593e89eb00e`. Oceniana klauzula to source_scope, nie cała koperta.

> 8.71 The Missile Range and Results Chart: This table is used
> to determine the strength of a missile unit firing at a given range.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996OW

Źródło / dokładny zakres: 9.96: CH cannot move including OW unless carrying eligible LI

Cel / dostępność: OW eligibility/path/execution absent; source supplies necessary carrier condition, not sufficient permission

Konieczność / wpływ: Samotny CH ma lokalny zakaz OW. CH+eligibleLI nie dostaje przez samo unless bezwarunkowego prawa OW; dalsze warunki ogólne niepozyskane.

Porównanie / propozycja: R996a→OW condition/explicit zachowuje konieczny warunek. ModeldescriptionOW eligibility ifmounted przyjąć tylko jako konieczność, nie pełną kwalifikację. Kierunek i source exception poparte, actualOWunresolved.

**first-001:** `/dependencies/110`; bajty [514655,515584), SHA-256 `d5d4bc0775d54b59bae7ca3e2b3bf301124158fac2cf2cb7cb56c7c25612afb9`.

Zapis modelu: `R996a→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Orderly Withdrawal", "description": "CH+LI OW eligibility if mounted", "needed_context": "OW rules for mounted LI/CH"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996a"], "blocks_full_result": true, "reason": "CH+LI OW eligibility if mounted is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996OW", "class": "missing_context", "affected_ids": ["R996a", "D996OW"], "source_regions": ["pdf-36-core-right"], "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.", "needed_context": "OW rules for mounted LI/CH", "blocking": true, "evidence_ids": ["E996a"], "review_status": "unreviewed"}

**context-01:** `/dependencies/110`; bajty [593152,594108), SHA-256 `cdcf024a11ceb33029a8492f7689b163b9f5a4437cf4298d38332cdc8648e7ce`.

Zapis modelu: `R996a→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Orderly Withdrawal", "description": "CH+LI OW eligibility if mounted", "needed_context": "OW rules for mounted LI/CH"}

Uzasadnienie modelu: Source refers to Orderly Withdrawal; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996a"], "blocks_full_result": true, "reason": "CH+LI OW eligibility if mounted is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996OW", "class": "missing_context", "affected_ids": ["R996a", "D996OW"], "source_regions": ["pdf-36-core-right"], "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.", "needed_context": "OW rules for mounted LI/CH", "blocking": true, "evidence_ids": ["E996a"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [1900,2693), hash wycinka `a50a6d10184bf092649d6bc56d164f3c54613f57c8d73dc8ebf6612c499d4f20`. Oceniana klauzula to source_scope, nie cała koperta.

> Gallic Chariots
> DESIGN NOTE: The chariots used by the Gallic tribes were
> not, in any way, weapons systems. They were used only for
> transport. Their only resemblance to the war chariots of “days
> gone by” was that they had wheels. Thus, ignore the reference
> to Chariots on the Combat Tables. However, the tribes were
> quite adept at using them to whatever advantage they did of-
> fer. In this module, chariots make an appearance at Sentinum
> and Telamon.
> Gallic Chariot (CH) units have only a Movement Allowance;
> they have no Size and no TQ Rating. These units cannot move
> at all, and this includes Orderly Withdrawal, unless stacked with
> an eligible Light Infantry (LI) unit. If an enemy combat unit (of
> any type) moves adjacent to a CH unit alone in a hex, the CH
> unit is immediately eliminated.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996eligible

Źródło / dokładny zakres: 9.96: CH requires eligible LI to move

Cel / dostępność: Meaning/criteria of eligible LI absent; source does not identify a numbered eligibility rule or scenario restriction

Konieczność / wpływ: Nie można stwierdzić, że każdyLIeligible, ani wskazać realnejlisty. Dla zadanejeligibleLI carrierconditionznany. Nie ma dowodu, gdzie dokładnie znajduje się kryterium.

Porównanie / propozycja: R996a→eligibleLI condition/explicit poparte dosłownym eligible. Kandydatdef/scenario restrictions to prośba, nie odczytane źródło. Przyjąć samo wymaganie kwalifikacji, nie udowodnione istnienie konkretnej listy/scenario clause lub konieczny selector.

**first-001:** `/dependencies/109`; bajty [513641,514649), SHA-256 `f1374439128dfafa072c15172dcc9546910c88ccd735d529c287a2054667b5ad`.

Zapis modelu: `R996a→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "eligible Light Infantry (LI) unit", "description": "Which LI may ride Gallic chariots", "needed_context": "Eligibility definition/scenario restrictions for mounted LI"}

Uzasadnienie modelu: Source refers to eligible Light Infantry (LI) unit; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996a"], "blocks_full_result": true, "reason": "Which LI may ride Gallic chariots is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996eligible", "class": "missing_context", "affected_ids": ["R996a", "D996eligible"], "source_regions": ["pdf-36-core-right"], "reason": "Which LI may ride Gallic chariots is referenced but unavailable.", "needed_context": "Eligibility definition/scenario restrictions for mounted LI", "blocking": true, "evidence_ids": ["E996a"], "review_status": "unreviewed"}

**context-01:** `/dependencies/109`; bajty [592110,593145), SHA-256 `2e248c2642702b2334f335d0c54a78e4576b459c6e0d8e75bbf003a42d7672d6`.

Zapis modelu: `R996a→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "eligible Light Infantry (LI) unit", "description": "Which LI may ride Gallic chariots", "needed_context": "Eligibility definition/scenario restrictions for mounted LI"}

Uzasadnienie modelu: Source refers to eligible Light Infantry (LI) unit; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996a"], "blocks_full_result": true, "reason": "Which LI may ride Gallic chariots is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996eligible", "class": "missing_context", "affected_ids": ["R996a", "D996eligible"], "source_regions": ["pdf-36-core-right"], "reason": "Which LI may ride Gallic chariots is referenced but unavailable.", "needed_context": "Eligibility definition/scenario restrictions for mounted LI", "blocking": true, "evidence_ids": ["E996a"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [1900,2693), hash wycinka `a50a6d10184bf092649d6bc56d164f3c54613f57c8d73dc8ebf6612c499d4f20`. Oceniana klauzula to source_scope, nie cała koperta.

> Gallic Chariots
> DESIGN NOTE: The chariots used by the Gallic tribes were
> not, in any way, weapons systems. They were used only for
> transport. Their only resemblance to the war chariots of “days
> gone by” was that they had wheels. Thus, ignore the reference
> to Chariots on the Combat Tables. However, the tribes were
> quite adept at using them to whatever advantage they did of-
> fer. In this module, chariots make an appearance at Sentinum
> and Telamon.
> Gallic Chariot (CH) units have only a Movement Allowance;
> they have no Size and no TQ Rating. These units cannot move
> at all, and this includes Orderly Withdrawal, unless stacked with
> an eligible Light Infantry (LI) unit. If an enemy combat unit (of
> any type) moves adjacent to a CH unit alone in a hex, the CH
> unit is immediately eliminated.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996movement

Źródło / dokładny zakres: 9.96: mounted CH pays/obeys terrain costs/prohibitions per Movement Cost Chart; Hits onlyLI

Cel / dostępność: Actual Movement Cost Chart CH values/prohibitions absent

Konieczność / wpływ: Realny koszt/zakaz potrzebujechart. ZadaneMP/MApozwalają lokalnie rozliczyć montowanie/demontowanie; HitsprzypadająLI,nieCH.

Porównanie / propozycja: R996b→MovementCostChart table_use/explicit poparte nazwą wprost, inaczej niżD951terrain. Przeczytano fizyczną kontynuacjęPDF36→37. Przyjąć lookup i blokadę nieznanych terrainvalues,nie brak localformulas.

**first-001:** `/dependencies/112`; bajty [516566,517532), SHA-256 `c34587c10bb4689a8f90b552edaf73f23d174f6a8d49b9b674904286b9032299`.

Zapis modelu: `R996b→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Movement Cost Chart", "description": "CH terrain MP costs/prohibitions", "needed_context": "Actual Movement Cost Chart with CH restrictions"}

Uzasadnienie modelu: Source refers to Movement Cost Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996b"], "blocks_full_result": true, "reason": "CH terrain MP costs/prohibitions is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996movement", "class": "missing_context", "affected_ids": ["R996b", "D996movement"], "source_regions": ["pdf-37-core-left"], "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.", "needed_context": "Actual Movement Cost Chart with CH restrictions", "blocking": true, "evidence_ids": ["E996c"], "review_status": "unreviewed"}

**context-01:** `/dependencies/112`; bajty [595119,596112), SHA-256 `68ee62b05c25a954689b2b9d6a1c72b36b21468c050f6a331008f3a79996219f`.

Zapis modelu: `R996b→candidate`, `table_use/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "Movement Cost Chart", "description": "CH terrain MP costs/prohibitions", "needed_context": "Actual Movement Cost Chart with CH restrictions"}

Uzasadnienie modelu: Source refers to Movement Cost Chart; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996b"], "blocks_full_result": true, "reason": "CH terrain MP costs/prohibitions is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996movement", "class": "missing_context", "affected_ids": ["R996b", "D996movement"], "source_regions": ["pdf-37-core-left"], "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.", "needed_context": "Actual Movement Cost Chart with CH restrictions", "blocking": true, "evidence_ids": ["E996c"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [2693,2884), hash wycinka `7cc050f4347449647541a56d7685e0a39e690ad22b8da4568f9fed91d5ed11f6`. Oceniana klauzula to source_scope, nie cała koperta.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/13/text`, znaki [0,826), hash wycinka `635fbaf7e22aec57f19bc0913cf8d86b4f45256b3c13cf6984d8b48064c8bdf2`. Oceniana klauzula to source_scope, nie cała koperta.

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
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996stack

Źródło / dokładny zakres: 9.96: CH+LI counts as one unit for stacking; all other restrictions apply CH+LI and CHalone

Cel / dostępność: Other stacking restrictions absent

Konieczność / wpływ: Znane jest liczeniepary jako1. Legalność konkretnego heksu z innymi jednostkami wymaga ograniczeń; 1 nie usuwa tych ograniczeń i nie utożsamia CHalone z CH+LI.

Porównanie / propozycja: R996b→other stacking condition/explicit zgodne; klauzula wykonawcza nadal apply, nie summary. Przyjąć warunek i potrzebę pełnejlegalności,nie dowolny stacking lub zmianęCHnoTQ.

**first-001:** `/dependencies/111`; bajty [515590,516560), SHA-256 `9c9d6ae570ccdf8cd358baa88a3e720a3c73ae2dda769bb7514877c4046d5a14`.

Zapis modelu: `R996b→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "All other stacking restrictions", "description": "Other limits on CH+LI and CH alone", "needed_context": "General stacking restrictions"}

Uzasadnienie modelu: Source refers to All other stacking restrictions; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996b"], "blocks_full_result": true, "reason": "Other limits on CH+LI and CH alone is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996stack", "class": "missing_context", "affected_ids": ["R996b", "D996stack"], "source_regions": ["pdf-37-core-left"], "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.", "needed_context": "General stacking restrictions", "blocking": true, "evidence_ids": ["E996c"], "review_status": "unreviewed"}

**context-01:** `/dependencies/111`; bajty [594115,595112), SHA-256 `422ebf0b10bfc605a0329ff4bfcbad1f7d5fae0b2a38bc5c4defc23d902749b9`.

Zapis modelu: `R996b→candidate`, `condition/explicit`, unresolved, blocks_full_result=`True`.

Dosłowny kandydat modelu: {"original_reference": "All other stacking restrictions", "description": "Other limits on CH+LI and CH alone", "needed_context": "General stacking restrictions"}

Uzasadnienie modelu: Source refers to All other stacking restrictions; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996b"], "blocks_full_result": true, "reason": "Other limits on CH+LI and CH alone is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.

Dosłowny gap: {"id": "G-D996stack", "class": "missing_context", "affected_ids": ["R996b", "D996stack"], "source_regions": ["pdf-37-core-left"], "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.", "needed_context": "General stacking restrictions", "blocking": true, "evidence_ids": ["E996c"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [2693,2884), hash wycinka `7cc050f4347449647541a56d7685e0a39e690ad22b8da4568f9fed91d5ed11f6`. Oceniana klauzula to source_scope, nie cała koperta.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/13/text`, znaki [0,826), hash wycinka `635fbaf7e22aec57f19bc0913cf8d86b4f45256b3c13cf6984d8b48064c8bdf2`. Oceniana klauzula to source_scope, nie cała koperta.

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
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996supply

Źródło / dokładny zakres: 9.96: Missile Supply8.17 not applicable whileLI mounted; removeLow/No on mounting

Cel / dostępność: 8.17 ordinary supply content absent; exemption and marker removal expressly supplied

Konieczność / wpływ: blocks=false jest wystarczające dla samego lokalnego wyłączenia/removal, nie dla całego strzału, supply after dismount lub zwykłego supply. MRRC/H&D remainmissing.

Porównanie / propozycja: R996d→8.17 exception/explicit poprawne w obu. Przyjąć lokalny nonblocking zakres; reasonexceptionnot supplied jest nieprecyzyjne: niedostarczonyjest normalnycel, samwyjątekpodany. Nie nadać całemuR996d full_result lub dowolnego reload/dismountstate.

**first-001:** `/dependencies/114`; bajty [518522,519504), SHA-256 `fcda4987da387113f835575815542c6a3136b6825e9eeda7240e6a8ca0154157`.

Zapis modelu: `R996d→candidate`, `exception/explicit`, unresolved, blocks_full_result=`False`.

Dosłowny kandydat modelu: {"original_reference": "8.17", "description": "Missile Supply exception while mounted", "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit"}

Uzasadnienie modelu: Source refers to 8.17; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996d"], "blocks_full_result": false, "reason": "Missile Supply exception while mounted is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Local exclusion/ignore nonblocking; ordinary supply/table identification and complete fire/combat execution not certified.

Dosłowny gap: {"id": "G-D996supply", "class": "missing_context", "affected_ids": ["R996d", "D996supply"], "source_regions": ["pdf-37-core-left"], "reason": "Missile Supply exception while mounted is referenced but unavailable.", "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit", "blocking": false, "evidence_ids": ["E996e"], "review_status": "unreviewed"}

**context-01:** `/dependencies/114`; bajty [597131,598140), SHA-256 `b5510b3a5124d981b71935c5a72fa079919455f03830a18ce33472d45da16fe8`.

Zapis modelu: `R996d→candidate`, `exception/explicit`, unresolved, blocks_full_result=`False`.

Dosłowny kandydat modelu: {"original_reference": "8.17", "description": "Missile Supply exception while mounted", "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit"}

Uzasadnienie modelu: Source refers to 8.17; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996d"], "blocks_full_result": false, "reason": "Missile Supply exception while mounted is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Local exclusion/ignore nonblocking; ordinary supply/table identification and complete fire/combat execution not certified.

Dosłowny gap: {"id": "G-D996supply", "class": "missing_context", "affected_ids": ["R996d", "D996supply"], "source_regions": ["pdf-37-core-left"], "reason": "Missile Supply exception while mounted is referenced but unavailable.", "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit", "blocking": false, "evidence_ids": ["E996e"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/13/text`, znaki [826,1427), hash wycinka `784b85e429dd0ad8fb2fac5f1ac3aec58712801cb7787d31eea12fd0e27b17a8`. Oceniana klauzula to source_scope, nie cała koperta.

> LI mounted on CH units have the following special abilities/
> liabilities:
> • LI do not suffer any Cohesion Hits for moving a second (and
> third) time in a Game Turn, if they spend the entire Orders
> Phase mounted on the CH unit.
> • LI cannot Shock attack; they must dismount to do so. When
> mounted, they defend as LI.
> • LI may use Missile Fire using the Mounted Javelin row on the
> MRRC. Missile Supply (8.17) does not apply while the LI unit
> is mounted. Remove any MiSSile low/No markers from the LI
> unit when the unit mounts a CH. They may use Harassment
> and Dispersal fire as if they were cavalry units.

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## D996tables

Źródło / dokładny zakres: 9.96 Design Note operational sentence: ignore Chariot references on Combat Tables for transportCH

Cel / dostępność: Actual Combat Table Chariot entries absent; does not authorize lookup/execution as war chariots

Konieczność / wpływ: blocks=falsepoparte dla dyspozycji ignore. Do identyfikacji konkretnych wpisów potrzebaactualtables; normalny wynik walki innych jednostek nadal zależny odniepodanych danych.

Porównanie / propozycja: R996note→CombatTables exception/explicit właściwe. To operacyjny ignorewewnątrzDesignNote,nie sama historyczna wzmianka. Przyjąć lokalne pominięcie i nieblokowanie tejdyspozycji,nie zawartośćtables lub ichaliasy,żadnegoCHoffensivecombat.

**first-001:** `/dependencies/108`; bajty [512527,513635), SHA-256 `1f7003a3d4d4e84827c18ca49ade9e7bb6d3e7bf41627b4af176911bda5c0b8a`.

Zapis modelu: `R996note→candidate`, `exception/explicit`, unresolved, blocks_full_result=`False`.

Dosłowny kandydat modelu: {"original_reference": "Chariots on the Combat Tables", "description": "Combat Table Chariot references ignored for transport chariots", "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause"}

Uzasadnienie modelu: Source refers to Chariots on the Combat Tables; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996note"], "blocks_full_result": false, "reason": "Combat Table Chariot references ignored for transport chariots is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Local exclusion/ignore nonblocking; ordinary supply/table identification and complete fire/combat execution not certified.

Dosłowny gap: {"id": "G-D996tables", "class": "missing_context", "affected_ids": ["R996note", "D996tables"], "source_regions": ["pdf-36-core-right"], "reason": "Combat Table Chariot references ignored for transport chariots is referenced but unavailable.", "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause", "blocking": false, "evidence_ids": ["E996note"], "review_status": "unreviewed"}

**context-01:** `/dependencies/108`; bajty [590968,592103), SHA-256 `f4555792332ddf87bf519ee6a9231583e2516e597f413bb1afa7a4b5ea93bccb`.

Zapis modelu: `R996note→candidate`, `exception/explicit`, unresolved, blocks_full_result=`False`.

Dosłowny kandydat modelu: {"original_reference": "Chariots on the Combat Tables", "description": "Combat Table Chariot references ignored for transport chariots", "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause"}

Uzasadnienie modelu: Source refers to Chariots on the Combat Tables; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.

Wpływ zapisany przez model: {"affected_ids": ["R996note"], "blocks_full_result": false, "reason": "Combat Table Chariot references ignored for transport chariots is not fully supplied; no missing content reconstructed."}

Ocena rodzaju: supported_as_bounded_required_role_not_actual_target_content

Ocena jawności: supported_explicit_named_requirement_or_implicit_definition_dependency

Ocena brakującego celu: Local exclusion/ignore nonblocking; ordinary supply/table identification and complete fire/combat execution not certified.

Dosłowny gap: {"id": "G-D996tables", "class": "missing_context", "affected_ids": ["R996note", "D996tables"], "source_regions": ["pdf-36-core-right"], "reason": "Combat Table Chariot references ignored for transport chariots is referenced but unavailable.", "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause", "blocking": false, "evidence_ids": ["E996note"], "review_status": "unreviewed"}

Niezależny dostarczony helper `private/poc/spqr-chapter9/inputs/v1/helper-regions.json`, `/regions/12/text`, znaki [1916,2350), hash wycinka `ea39023296059f16c4d5342570c688e17e5dea5240c5bd4492071b9918f26765`. Oceniana klauzula to source_scope, nie cała koperta.

> DESIGN NOTE: The chariots used by the Gallic tribes were
> not, in any way, weapons systems. They were used only for
> transport. Their only resemblance to the war chariots of “days
> gone by” was that they had wheels. Thus, ignore the reference
> to Chariots on the Combat Tables. However, the tribes were
> quite adept at using them to whatever advantage they did of-
> fer. In this module, chariots make an appearance at Sentinum
> and Telamon.
> 

Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.

## Granice wyniku

36 przypisanych krawędzi i ich gapy identyczne między odpowiedziami; oba wyniki mają osobne pełne ślady. Wcześniej dostarczone10.11/8.75 opisują fragment framework TQ, nie actual chart; uwzględniono częściową dostępność.
Udostępniono72, porównano72, nowych decyzji właściciela0, pending72. Faktyczny odczyt/otwarcieunknown. Poprzednie185 dokładnych zakresów mają decyzje; dodatkowa wcześniejsza decyzja kindD961stack nie jest ponownie pytana ani liczonajako nowe rozstrzygnięcie.
Łącznie w przydziale .4b porównano257 wystąpień (126/131). To nie certyfikat wszystkich pól, całego grafu, brakujących frozen pairs lub gold. Osiem starych oczekiwań iSEM-001–013 w pozostałych zakresach otwarte; scopedSEM-014–017 zachowane. NoweSEM-018/019waiting_review.
105 candidates nie staje sięgold; TP/FP/FN/precision/recall not_assessable. Nie zmieniono źródeł, odpowiedzi, eval-v1, dawnych artefaktów ani limitów. Brak nowych ekstrakcji/korekt i sytuacji.
Kontekst1strona/1reguła/0tabel,1runda/0korekt;0pełnych domknięć,4częściowe aktualizacje/4nowe deklaracje, stop ekspansji na2. Izolacja dawnego context-01: listing/path pozaallowlistą potwierdzony, odczyt treści oceny niezaobserwowany, exposure/cleancontextunknown. Aktywne czasy/selektory/tokens/cena/budżetunknown.
Po decyzjach .4b3 kolejna osobna .4c z własnym oszacowaniem i ewentualnym podziałem przed pracą. .4c/.4d nie wykonano; M-POC5A/.4/.4b partial, M-POC5 jedyny next.
