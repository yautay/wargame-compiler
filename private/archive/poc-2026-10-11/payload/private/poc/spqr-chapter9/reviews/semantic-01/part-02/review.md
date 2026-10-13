# M-POC5A.2 — EXP-001–025: konkretne porównania

Stan partial/waiting_review. Poniżej propozycje oceniającego Codex po porównaniu źródeł z polami obu odpowiedzi. Żadna nie została zaakceptowana za właściciela. „ok kontynuuj” autoryzuje dalszą pracę, nie rozstrzyga wcześniejszych SEM-001/002/003.

Pełne transkrypcje, pola i ślady bajtowe: [comparisons.json](comparisons.json). Nowa kwestia: [issues.json](issues.json). Pierwszy pakiet nadal [pending](../focus-01.md).

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`.

first-001: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

## Wynik porównania oceniającego

23 zakresy lokalne: 21 propozycji zgodności, 1 propozycja zgodności treści z osobnym błędem lokatora E916, 1 niepełna interpretacja (EXP-017). Dwa wymagania kontekstu: właściwa blokada mapy (EXP-010) i nierozstrzygnięta deklaracja blokowania dowodzenia (EXP-019). Te liczby opisują propozycje, nie metrykę poprawności ani akceptację.

Powiązano 42 różnych pozycji źródłowego inwentarza i 88 par rubryka/EXP. Nie nadano pełnej akceptacji pozycji o szerszym zakresie; tabele, nota operatywna i przykład kompasu są czytane tylko w zatwierdzonym zakresie.

## Nowa kwestia SEM-009 — 9.18

> Unless the rules specifically state otherwise, Elephant units may be commanded by any leader.

W obu wynikach literalny cytat zachowuje zastrzeżenie, a wyjątki mają unknown. Jednocześnie R918.action_effect mówi „Any leader may command Elephant units”, D918specific.blocks_full_result=false, G-D918specific.blocking=false. Brak wyjątków zgłoszono, lecz brak jawnej blokady realnej autoryzacji. To kandydat do oceny; nie wskazano rzeczywistego dowódcy i nie potwierdzono błędnego wyniku.

Proponowana decyzja: znana reguła lokalna pozostaje; rzeczywiste uprawnienie konkretnego leadera wymaga sprawdzenia wyjątków. Właściciel rozstrzyga, czy false w dwóch deklaracjach jest nieoznaczoną blokadą krytyczną. Nie ocenia to kierunku/rodzaju D918specific jako nowego gold.

## Zakresy do rzeczywistego review

### EXP-001

Dokładny zatwierdzony zakres: In the reviewed supplied case, Pass-Thru is allowed with LI defending Front, EL marker, no co-attacker, no initial enemy ZOC, a free Rear and an early decision. Initial enemy ZOC excludes it despite later exit. With two defenders both must meet the earlier conditions.

Porównanie: R911.conditions: Front, marker, wolny Rear; exceptions: Flank/Rear, współatak i ZOC na początku Orders Phase. time_limits zachowuje decyzję przed DR i początkowy ZOC. Obie jednostki muszą spełniać warunki. Nie wyliczamy geometrii ZOC.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 31 right, C-9.11-01, bbox [315.0, 481.4, 567.042, 563.4], PDF 31 right, C-9.11-02, bbox [315.0, 568.28, 530.611, 578.28], PDF 31 right, C-9.11-03, bbox [315.0, 581.72, 530.38, 591.72], PDF 31 right, C-9.11-04, bbox [315.0, 595.16, 567.07, 617.16], PDF 31 right, C-9.11-05, bbox [315.0, 624.38, 567.018, 658.38]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

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

**first-001** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [171012,179988), hash `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [236824,246111), hash `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Pełny Shock i definicje Front/Rear/ZOC są celami zewnętrznymi; nie wyliczać ich z tego akapitu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-002

Dokładny zatwierdzony zakres: For the reviewed supplied Pass-Thru result, defender Pre-Shock +1 DRM; infantry Hits 5 become 2 and EL Hits 3 become 2. Base-0 reduction floor and other modifier order remain unresolved.

Porównanie: R911 action_effect/parameters zachowują Pre-Shock +1 DRM, pół/floor Hits obrońcy i -1 Hits EL. Są to operatory zgodne z zatwierdzonym zakresem 5→2 oraz 3→2; nie dopisano dolnej granicy dla bazowego 0 ani kolejności innych modyfikatorów. Nie oceniono SIT.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 31 right, C-9.11-07, bbox [315.0, 680.66, 567.005, 702.66], PDF 31 right, C-9.11-08, bbox [315.0, 706.82, 567.12, 740.82]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 1. Apply a +1 DRM to the infantry unit’s Pre-Shock TQ Check
> DR.

> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

**first-001** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [171012,179988), hash `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [236824,246111), hash `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Base EL Hits=0 reduction floor/order remains unresolved; do not infer a negative result or minimum.; Bazowy wynik Shock musi być dostarczony; kolejność innych modyfikatorów i dolna granica redukcji EL do przeglądu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-003

Dokładny zatwierdzony zakres: After supplied no-infantry-Rout and no-EL-Rampage outcomes, place EL in a free defender Rear hex chosen by the EL player, keeping facing. No complete Shock result inferred.

Porównanie: R911 action_effect krok 3: po Shock, tylko gdy piechota nie Rout i EL nie Rampage; wolny Rear wybiera gracz EL, facing zachowane. Nie zastępuje to pełnego wyniku Shock.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 left, C-9.11-09, bbox [45.0, 54.004, 297.084, 100.004]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.

**first-001** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [171012,179988), hash `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [236824,246111), hash `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Stan Rout wymaga procedury ogólnej; Rampage ma wewnętrzny cel R-9.14.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-004

Dokładny zatwierdzony zakres: The final Pass-Thru TQ check is separate from Pre-Shock; SK are exempt from that final check. For non-SK, positive DR-TQ gives Hits; DR<=TQ gives no excess. No minimum imported from 9.16.

Porównanie: R911 rozdziela końcowy Pass-Thru TQ od Pre-Shock, wyłącza SK z kroku 4 i nalicza tylko positive excess DR-TQ. R924 powtarza wyłączenie SK. Parametr positive excess nie importuje minimum 1 z 9.16; brak konkretnej liczby nie jest pominięciem operatora.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 left, C-9.11-10, bbox [45.0, 104.164, 297.0, 150.164], PDF 33 right, C-9.24-03, bbox [314.995, 666.32, 566.897, 676.32]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 4. The defending unit, other than a Skirmisher unit, now un-
> dergoes a Pass-Thru TQ Check. Subtract the unit’s TQ from
> the DR, with any excess being the number of Cohesion Hits
> now applied (DR–TQ=Hits).

> • Skirmishers do not make an Elephant Pass-Thru Check (9.11).

**first-001** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [171012,179988), hash `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

R924, `/rules/14`, bajty [249766,255895), hash `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

transcription: {"state": "known", "value": ["Skirmishers do not make an Elephant Pass-Thru Check (9.11).", "the interruption is caused by only one such unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Line exception applies if interruption caused by only one such unit."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Single-unit interruption condition."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing cost", "value": 0, "unit": {"state": "known", "value": "MP", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}, {"name": "line interruption allowance", "value": 1, "unit": {"state": "known", "value": "Velites or Skirmisher unit per interruption", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Repeated movement within Game Turn."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R911, `/rules/0`, bajty [236824,246111), hash `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription: {"state": "known", "value": ["Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.", "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.", "At least one defender Rear hex unoccupied.", "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Optional Pass-Thru; refusal means normal Shock.", "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.", "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.", "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.", "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.", "Skirmishers excluded from Step 4.", "Step 3 conditional on neither infantry rout nor Elephant rampage."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defenders permitted", "value": 2, "unit": {"state": "known", "value": "infantry units", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "unoccupied Rear minimum", "value": 1, "unit": {"state": "known", "value": "hex", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "defender Hits multiplier", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Elephant Hits adjustment", "value": -1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}, {"name": "Pass-Thru Hits", "value": "positive excess DR–TQ", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E911a", "E911b"], "reason": null, "gap_ids": []}, "evidence_ids": ["E911a", "E911b"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Choice before Pre-Shock TQ Check die roll.", "Enemy ZOC assessed at start of Orders Phase.", "Steps 3–4 after Shock resolution."], "reason": null, "gap_ids": []}

R924, `/rules/14`, bajty [318324,324673), hash `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

transcription: {"state": "known", "value": ["Skirmishers do not make an Elephant Pass-Thru Check (9.11).", "the interruption is caused by only one such unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Line exception applies if interruption caused by only one such unit."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Single-unit interruption condition."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing cost", "value": 0, "unit": {"state": "known", "value": "MP", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}, {"name": "line interruption allowance", "value": 1, "unit": {"state": "known", "value": "Velites or Skirmisher unit per interruption", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Repeated movement within Game Turn."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Nie rozszerzać wyjątku na wszystkie testy TQ.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-005

Dokładny zatwierdzony zakres: Elephant Screen uses the explicitly named Elephant Screen MRRC row and fires only as Reaction Fire, has its own supply markers, and is absent on Leader Elephant. Actual lookup and supply procedure remain context requirements.

Porównanie: R912: Reaction Fire only, nazwany Elephant Screen MRRC row, własne supply markers i brak screen u Leader Elephant. Nie ma podstaw do wartości pełnego lookupu lub domknięcia supply.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 left, C-9.12-02, bbox [45.0, 303.127, 297.017, 325.127], PDF 32 left, C-9.12-03, bbox [45.0, 327.127, 297.023, 361.127]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> Elephant Screens can Missile Fire with Reaction Fire (8.2) only,
> using the Elephant Screen row on the MRRC. Elephant Screens

> have their own missile supply markers. Leader elephants do not
> have screens (they usually did, but they were too small to be a
> factor).

**first-001** — osobny wynik pending; porównane pola:

R912, `/rules/1`, bajty [179994,184187), hash `3f41d13d808d94b10acd6b9c50291e48c421110a1cbd8ade5b4005da89db6f2b`.

transcription: {"state": "known", "value": ["Elephant Screens can Missile Fire with Reaction Fire (8.2) only, using the Elephant Screen row on the MRRC."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.", "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.", "Leader elephants have no screens."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.", "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.", "Leader elephants have no screens."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Leader elephants lack screens."], "reason": null, "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R912, `/rules/1`, bajty [246118,250457), hash `7f308d008537d03c5e4e9cefca02e958fd41bf37b65dc395a998895b28c401f2`.

transcription: {"state": "known", "value": ["Elephant Screens can Missile Fire with Reaction Fire (8.2) only, using the Elephant Screen row on the MRRC."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.", "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.", "Leader elephants have no screens."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.", "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.", "Leader elephants have no screens."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Leader elephants lack screens."], "reason": null, "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Pełny wynik ognia wymaga 8.2 i wiersza MRRC.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-006

Dokładny zatwierdzony zakres: RidersasMountedJavelinists,separatejavelin/screenDR,N03-S2nochangefromhistoricaltowerabsence

Porównanie: R913: Mounted Javelinists dla Missile Fire; javeliny/screen mają osobne DR. R913note: historyczny brak wież nie zmienia reguły. Nie utożsamiono niepotwierdzonych aliasów wiersza MRRC.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 left, C-9.13-01, bbox [45.0, 368.527, 297.019, 414.527], PDF 32 left, N-03-S2, bbox [49.0, 423.03, 293.116, 457.03]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.13 Tower Riders: The riders atop elephants were armed with
> javelins and are treated as Mounted Javelinists for Missile Fire
> purposes. The Elephant unit may use Reaction Fire with both its
> javelins and its screen, with the player rolling separately for each.

> Makes no difference, the rule
> remains the same.

**first-001** — osobny wynik pending; porównane pola:

R913, `/rules/2`, bajty [184193,187922), hash `6ae8731a79d93d63ac442f6c3ebbb060431519b68ea15f099061e09e89710ac9`.

transcription: {"state": "known", "value": ["The Elephant unit may use Reaction Fire with both its javelins and its screen, with the player rolling separately for each."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Tower riders count as Mounted Javelinists for Missile Fire.", "Elephant may Reaction Fire with javelins and screen; roll separately for each."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Tower riders count as Mounted Javelinists for Missile Fire.", "Elephant may Reaction Fire with javelins and screen; roll separately for each."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

R913note, `/rules/3`, bajty [187928,191195), hash `daa665c7c08f5cc4d8bbd84d94483163762c15694e230b680f9e8355f85d3b61`.

transcription: {"state": "known", "value": ["Makes no difference, the rule remains the same."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "The Tower Riders rule remains the same despite that portrayal.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Historical portrayal of Hannibal’s elephants without towers."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "The Tower Riders rule remains the same despite that portrayal.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R913, `/rules/2`, bajty [250464,254326), hash `cf0f58a2d98a672e77cf653d796bf33730b38d13e2613a8516a04a57e224b290`.

transcription: {"state": "known", "value": ["The Elephant unit may use Reaction Fire with both its javelins and its screen, with the player rolling separately for each."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Tower riders count as Mounted Javelinists for Missile Fire.", "Elephant may Reaction Fire with javelins and screen; roll separately for each."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Tower riders count as Mounted Javelinists for Missile Fire.", "Elephant may Reaction Fire with javelins and screen; roll separately for each."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

R913note, `/rules/3`, bajty [254333,257716), hash `6fc580e76f219adc2a6ee990c85c9387c2ded93be6d55b5f79a548ec7c5782f5`.

transcription: {"state": "known", "value": ["Makes no difference, the rule remains the same."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "The Tower Riders rule remains the same despite that portrayal.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Historical portrayal of Hannibal’s elephants without towers."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "The Tower Riders rule remains the same despite that portrayal.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Tożsamość wiersza MRRC z samego Mounted Javelinists pozostaje hipotezą DC-031.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-007

Dokładny zatwierdzony zakres: Ordinary EL Rout triggers immediate Rampage procedure. Ordinary EL roll 0 heads toward nearest friendly unit with opponent choosing a tie; first 7-9 moves away from cause, subsequent 7-9 eliminates. Concrete map and cause are not invented.

Porównanie: R914 i N914table zachowują immediate Rout→Rampage; zwykły EL: 0 do najbliższej friendly, remis wybiera przeciwnik; pierwsze 7–9 od przyczyny, późniejsze 7–9 eliminacja. first/subsequent jest jawne w wierszu tabeli. Rzeczywisty kierunek nie został ustalony.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 left, C-9.14-01, bbox [45.0, 466.27, 297.01, 512.27], PDF 32 left, T-01, bbox [53.562, 523.318, 292.421, 647.178], PDF 32 right, T-01, bbox [333.145, 58.343, 562.471, 164.503], PDF 32 left, TR-01, bbox [68.142, 538.088, 292.421, 584.248], PDF 32 left, TR-02, bbox [63.142, 589.018, 292.388, 647.178], PDF 32 right, TR-03, bbox [333.145, 58.343, 562.471, 164.503]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.14 Elephant Rampage: When an Elephant unit routs, it Ram-
> pages. Leader Elephants also Rampage, but they have less of a
> chance of doing so. Each time an Elephant unit routs, its player
> rolls the die and does one of the following, depending on the DR:

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

**first-001** — osobny wynik pending; porównane pola:

N914table, `/nodes/0`, bajty [120024,122102), hash `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

R914, `/rules/4`, bajty [191201,210006), hash `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

N914table, `/nodes/0`, bajty [167589,169718), hash `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

R914, `/rules/4`, bajty [257723,277141), hash `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Kierunku na rzeczywistej mapie nie ustala sam przykład D-01.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-008

Dokładny zatwierdzony zakres: Leader Elephant roll 0 eliminates it; subsequent 7-9 immediately rallies it with Hits=TQ-2 instead of elimination. This owns the subsequent-roll result; first Leader 7-9 is scored only in EXP-009.

Porównanie: N914table: Leader 0 eliminuje; późniejsze 7–9 rally z Hits=TQ−2 zamiast eliminacji. R914.exceptions utrzymuje ten wyjątek wobec ogólnego zakazu rally. Pierwsze 7–9 nie daje drugiego punktu w EXP-008.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 left, TR-01, bbox [68.142, 538.088, 292.421, 584.248], PDF 32 right, TR-03, bbox [333.145, 58.343, 562.471, 164.503], PDF 32 right, C-9.14-11, bbox [315.0, 697.799, 567.008, 719.799], PDF 33 left, C-9.14-11, bbox [45.0, 54.004, 297.048, 76.004]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 0 The Elephant unit heads in the direction of the
> nearest friendly unit, opposing player’s choice
> if there is more than one nearest unit. A Leader
> Elephant is eliminated.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

**first-001** — osobny wynik pending; porównane pola:

N914table, `/nodes/0`, bajty [120024,122102), hash `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

R914, `/rules/4`, bajty [191201,210006), hash `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

N914table, `/nodes/0`, bajty [167589,169718), hash `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

R914, `/rules/4`, bajty [257723,277141), hash `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Later7-9LeaderRally outcome andcriticality accepted; actualTQ and4.84counting notclosed. Firsttable7-9 addressedseparatelyEXP009.; Zakres Leader Elephant przy pierwszym 7–9 jest odrębnym nierozstrzygniętym oczekiwaniem.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-009

Dokładny zatwierdzony zakres: First Rampage-table 7-9 for Leader Elephant means movement away from the causing unit, without immediate special rally. Subsequent-roll result is referenced in EXP-008 and earns no second point here. Counting the 4.84 trigger die is unresolved.

Porównanie: N914table rozdziela first Rampage DR od any subsequent: pierwsze Leader 7–9 prowadzi od przyczyny, nie do natychmiastowego rally. R914.exceptions ogranicza rally do subsequent. Nie określono zaliczania rzutu wyzwalającego 4.84.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 right, TR-03, bbox [333.145, 58.343, 562.471, 164.503], PDF 32 right, C-9.14-11, bbox [315.0, 697.799, 567.008, 719.799], PDF 33 left, C-9.14-11, bbox [45.0, 54.004, 297.048, 76.004]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

**first-001** — osobny wynik pending; porównane pola:

N914table, `/nodes/0`, bajty [120024,122102), hash `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

R914, `/rules/4`, bajty [191201,210006), hash `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

N914table, `/nodes/0`, bajty [167589,169718), hash `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

R914, `/rules/4`, bajty [257723,277141), hash `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: FirstLeader7-9interpretation andcriticality accepted;actualcause/map/route/TQ and4.84countingnotclosed.; Przegląd składni tabeli i uzasadniona decyzja właściciela.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-010

Dokładny zatwierdzony zakres: 1-6 uses actual battle map compass; missing compass blocks concrete direction/hexside.

Porównanie: N914diagram podaje illustrative example, użycie kompasu konkretnej bitwy i brak uniwersalnego kierunku geograficznego. D914compass/G-D914compass mają brak źródła i blocking=true. To blokada rzeczywistego kierunku, nie lokalnie podanej syntetycznej trasy.

Propozycja: `source_block_supported`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 left, TR-02, bbox [63.142, 589.018, 292.388, 647.178], PDF 32 right, D-01, bbox [350, 220, 535, 299], PDF 32 right, X-01, bbox [315.0, 303.779, 567.012, 337.779]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

> 

> EXAMPLE: The above diagram shows the elephant unit refaced
> after a Rampage die roll of 1. This is just an example; use the
> compass on the map for each battle.

**first-001** — osobny wynik pending; porównane pola:

N914diagram, `/nodes/1`, bajty [122108,123601), hash `99553c9e8dd99e5d6630491e66a2f8303144f0c27ea52a45ac24b4b368166f4d`.

content: {"state": "known", "value": {"transcription": {"caption": "The above diagram shows the elephant unit refaced after a Rampage die roll of 1.", "direction_labels": {"upper_left": "6", "upper_right": "1", "right": "2", "lower_right": "3", "lower_left": "4", "left": "5"}, "counter_labels": ["Africa", "8", "J", "a", "5", "EL", "5", "7"]}, "interpretation": "Left image shows original elephant facing; right image shows clockwise re-facing towards upper-right hexside for example roll 1. Numbers refer to the six directions by hexside. Actual battle map compass governs; no universal geographical direction inferred."}, "reason": null, "gap_ids": []}

N914table, `/nodes/0`, bajty [120024,122102), hash `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

D914compass, `/dependencies/54`, bajty [459795,460817), hash `2329eef178fde36656363601a0b0a8e0c12bd5ee1a33b15a6b1197b0e34d607e`.

impact_if_missing: {"affected_ids": ["N914table"], "blocks_full_result": true, "reason": "Battle-specific directions for 1–6 Rampage rolls is not fully supplied; no missing content reconstructed."}

G-D914compass, `/gaps/14`, bajty [535977,536514), hash `4bda56919fefbc95954ea322fb5af5bea3f9a0e539c36dfc6e7ca2f8bec75c8d`.

blocking: true

**context-01** — osobny wynik pending; porównane pola:

N914diagram, `/nodes/1`, bajty [169725,171268), hash `1365c92a4d04710676a2e125eb8e5f6adccbbcf43675f2725fb1db147361d934`.

content: {"state": "known", "value": {"transcription": {"caption": "The above diagram shows the elephant unit refaced after a Rampage die roll of 1.", "direction_labels": {"upper_left": "6", "upper_right": "1", "right": "2", "lower_right": "3", "lower_left": "4", "left": "5"}, "counter_labels": ["Africa", "8", "J", "a", "5", "EL", "5", "7"]}, "interpretation": "Left image shows original elephant facing; right image shows clockwise re-facing towards upper-right hexside for example roll 1. Numbers refer to the six directions by hexside. Actual battle map compass governs; no universal geographical direction inferred."}, "reason": null, "gap_ids": []}

N914table, `/nodes/0`, bajty [167589,169718), hash `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content: {"state": "known", "value": {"transcription": {"headers": ["Die Roll", "Result"], "rows": [{"die_roll": "0", "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."}, {"die_roll": "1–6", "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."}, {"die_roll": "7–9", "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."}]}, "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."}, "reason": null, "gap_ids": []}

D914compass, `/dependencies/54`, bajty [536513,537563), hash `a6a4251c69eb2d2d05643f642fbb1e5ebf93486528dc7879d21a18040e6da46c`.

impact_if_missing: {"affected_ids": ["N914table"], "blocks_full_result": true, "reason": "Battle-specific directions for 1–6 Rampage rolls is not fully supplied; no missing content reconstructed."}

G-D914compass, `/gaps/14`, bajty [619959,620515), hash `7f06c6d840f91c9e11ef9a94e541fc052df74c92e799572526b83b4978785600`.

blocking: true

Wyłączenia/niepewności: A real battle-map compass is required for a concrete direction/hexside.; Wskazana mapa bitwy z dowodem i kompasem, bez domknięcia całej instrukcji.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-011

Dokładny zatwierdzony zakres: Complete each Rampage immediately before any other mechanic except OW under 6.51; no concurrent Rampages. Rampaging EL has no ZOC, triggers no Reaction Fire of any kind, and normally cannot rally. The special later Leader result is a reference to EXP-008, not a second scored result.

Porównanie: R914: immediate i serial resolution, wyjątek OW; brak ZOC i Reaction Fire każdego rodzaju; no rally z osobnym wyjątkiem Leader w exceptions. C-9.14-11 przechodzi na PDF33 i kontynuacja źródła jest zachowana. Wyjątek jest referencją do EXP-008, bez drugiego punktu.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 right, C-9.14-02, bbox [315.005, 180.783, 567.114, 214.783], PDF 32 right, C-9.14-11, bbox [315.0, 697.799, 567.008, 719.799], PDF 33 left, C-9.14-11, bbox [45.0, 54.004, 297.048, 76.004]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> Each Elephant Rampage is always resolved immediately, before
> any other game mechanic is addressed, except for Orderly With-
> drawal in face of the rampaging elephant (6.51).

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

**first-001** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [191201,210006), hash `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [257723,277141), hash `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: OW 6.51 wymaga zewnętrznej procedury; szczególny Leader Elephant zachować oddzielnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-012

Dokładny zatwierdzony zakres: Attempt 3 hexes per directional roll with supplied route/no early termination. At a would-be occupied hex stop adjacent; occupant gets 1 CH via Front, 2 via Flank/Rear, cavalry always 2. Both units of a stack get their Hits. A leader unable to withdraw under 4.72 dies without DR; actual inability requires context.

Porównanie: R914 parametry/action: próba 3 hexów na directional DR; stop adjacent przed occupied hex; occupant 1 CH przez Front, 2 Flank/Rear, cavalry zawsze 2; oba elementy stacku Hits. Leader unable to withdraw według 4.72 ginie bez DR. Realnego warunku unable nie domknięto.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 right, C-9.14-03, bbox [315.0, 345.179, 567.03, 451.179], PDF 32 right, C-9.14-04, bbox [315.0, 458.579, 567.026, 516.579]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

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

**first-001** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [191201,210006), hash `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [257723,277141), hash `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Możliwość withdrawal leadera wymaga 4.72; geometrię i typy przyjąć tylko jako jawne dane przypadku.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-013

Dokładny zatwierdzony zakres: Repeat until offmap, elimination(ordinaryEL7-9mahout), at least8hexes from nearest unit(any allegiance) causing elimination, or if none above eliminate after4th consecutive RampageDR.

Porównanie: R914: ponawianie do offmap/elimination, >=8 hexów od nearest unit i eliminacja po 4. consecutive DR, jeśli wcześniej nie zakończono. Wiersz tabeli i wyjątki nadal kwalifikują późniejsze 7–9 oraz Leader. Nie dodano realnego pomiaru mapy.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 right, C-9.14-06, bbox [315.0, 538.859, 498.76, 548.859], PDF 32 right, C-9.14-07, bbox [315.0, 552.299, 534.79, 562.299], PDF 32 right, C-9.14-08, bbox [315.0, 565.739, 567.009, 587.739], PDF 32 right, C-9.14-09, bbox [315.0, 591.179, 567.008, 613.179]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> • The Elephant unit rampages off the map, or

> • The Elephant unit is eliminated (7-9 mahout DR), or

> • The Elephant unit is at least 8 hexes from the nearest unit, in
> which case it is eliminated, or

> • If none of the above, after the 4th consecutive Rampage DR,
> the Elephant unit is eliminated.

**first-001** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [191201,210006), hash `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [257723,277141), hash `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Nie dorabiać pomiaru odległości na nieznanej mapie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-014

Dokładny zatwierdzony zakres: Leader stackedwithRampagingEL travelswithit. At end leadercasualty4.73; survivor stayswhereELended. If ELoffmap bothELandleader eliminated, not survival inferred fromcasualtyDR.

Porównanie: R914: leader podróżuje z EL; na końcu casualty 4.73, survivor zostaje na końcowym heksie. Offmap eliminuje obu, odrębnie od survival placement. Nie podano wyniku casualty DR z nieobecnego źródła.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 32 right, C-9.14-10, bbox [315.0, 620.399, 567.008, 690.399]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> A leader stacked with a rampaging Elephant goes along with
> the Elephant on the Rampage. When the Rampage ends, the
> player rolls for a leader casualty (4.73). If the leader survives,
> he remains on the map where the Elephant ended the Rampage.
> If the Elephant Rampages off the map, both the Elephant and
> leader are eliminated.

**first-001** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [191201,210006), hash `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R914, `/rules/4`, bajty [257723,277141), hash `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription: {"state": "known", "value": ["Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:", "Die Roll Result", "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.", "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).", "This is just an example; use the compass on the map for each battle.", "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.", "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.", "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.", "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Each Elephant rout, including Leader Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.", "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.", "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.", "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.", "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.", "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.", "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.", "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Orderly Withdrawal interrupts priority.", "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.", "Cavalry occupant always takes 2 Hits.", "Off-map stacked leader eliminated without survival placement."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "directional roll movement", "value": 3, "unit": {"state": "known", "value": "hexes per directional die roll", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Front contact", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Flank/Rear contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per affected unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "cavalry contact", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "isolation termination", "value": ">=8", "unit": {"state": "known", "value": "hexes from nearest unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "maximum sequence", "value": 4, "unit": {"state": "known", "value": "consecutive Rampage DR", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "concurrent Rampages maximum", "value": 1, "unit": {"state": "known", "value": "Elephant unit", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "Leader rally Hits", "value": "TQ–2", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}, {"name": "table roll groups", "value": ["0", "1–6", "7–9"], "unit": {"state": "known", "value": "die-roll results", "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E914start", "E914tableL", "E914tableR", "E914priority", "E914diagram", "E914move", "E914end", "E914last", "E914cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Immediate, serial resolution until conclusion.", "First versus subsequent DR matters.", "Leader casualty at Rampage end."], "reason": null, "gap_ids": []}

Wyłączenia/niepewności: Wynik casualty wymaga 4.73; nie wyliczać prawdopodobieństwa bez celu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-015

Dokładny zatwierdzony zakres: Cavalry cannot voluntarily enterenemyELZOC; enteringeach enemyELFlank/Rearhex incurs2CH, samepenaltyforforcedentryELZOC; no cavalryattackenemyELFront; Flank/Rearattack doesnotgainusualAS. Nofullpositiveattackpermission.

Porównanie: R915: zakaz voluntary enemy EL ZOC, 2 CH za każdy Flank/Rear hex i przy forced ZOC entry; Front attack zakazany, Flank/Rear nie daje zwykłego AS. Pozwolenie lokalne nie potwierdza pełnej legalności ataku bez bazowego kontekstu.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 left, C-9.15-01, bbox [45.0, 139.747, 297.13, 245.747]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.15 Cavalry vs. Elephants: Cavalry units may never voluntarily
> move into the ZOC of an enemy Elephant unit. They may move
> into or through an enemy Elephant’s Flank or Rear hexes but
> at the cost of 2 Cohesion Hits for each such hex entered. This
> cohesion penalty also applies if the cavalry unit is forced to enter
> an Elephant ZOC. Cavalry may never attack an enemy Elephant
> through the latter’s Front hexes; they may attack through the
> Elephant unit’s Flank or Rear hexes, but they do not gain the
> usual Attack Superiority for such an attack.

**first-001** — osobny wynik pending; porównane pola:

R915, `/rules/5`, bajty [210012,214748), hash `e7a73035f7d9687d28f1dcb19e01d02be16cd4d325a249d7b7fc1b9a0dfaf226`.

transcription: {"state": "known", "value": ["Cavalry units may never voluntarily move into the ZOC of an enemy Elephant unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Cavalry may not voluntarily enter enemy Elephant ZOC.", "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.", "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Cavalry may not voluntarily enter enemy Elephant ZOC.", "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.", "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Forced ZOC entry uses the 2-Hit penalty.", "Flank/Rear attacks allowed but do not gain usual Attack Superiority."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "entry penalty", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per such hex entered", "evidence_ids": ["E915"], "reason": null, "gap_ids": []}, "evidence_ids": ["E915"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R915, `/rules/5`, bajty [277148,282047), hash `cf617cf7b5c3ca2083c7fb23420fe52d8cc8d0f87cec79861f8fe21e3464ae8e`.

transcription: {"state": "known", "value": ["Cavalry units may never voluntarily move into the ZOC of an enemy Elephant unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Cavalry may not voluntarily enter enemy Elephant ZOC.", "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.", "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Cavalry may not voluntarily enter enemy Elephant ZOC.", "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.", "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Forced ZOC entry uses the 2-Hit penalty.", "Flank/Rear attacks allowed but do not gain usual Attack Superiority."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "entry penalty", "value": 2, "unit": {"state": "known", "value": "Cohesion Hits per such hex entered", "evidence_ids": ["E915"], "reason": null, "gap_ids": []}, "evidence_ids": ["E915"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Wyliczenie geometrii ZOC i bazowego Shock wymaga reguł ogólnych.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-016

Dokładny zatwierdzony zakres: Ordinary EL moving from nonadjacent to adjacent enemy cavalry forces an OW attempt. If cavalry can withdraw, no Reaction Fire; otherwise immediate TQ check, and routed cavalry eliminates without DR in the supplied cannot-withdraw branch. Leader EL excluded. Arithmetic belongs to EXP-017.

Porównanie: R916: wejście z nonadjacent do adjacent, obligatory OW attempt; jeśli można odejść brak Reaction Fire, jeśli nie można immediate TQ, routed cavalry eliminuje bez DR. Leader EL wyłączony w exceptions. Zakres minimum należy do EXP-017. E916 urywa cytat wyjątku; semantyczne podparcie pochodzi z pełnego regionu PDF33, a lokator nadal błędny.

Propozycja: `supported_local_scope_with_locator_issue`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 left, C-9.16-01, bbox [45.0, 253.147, 297.021, 371.147]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

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

**first-001** — osobny wynik pending; porównane pola:

R916, `/rules/6`, bajty [214754,219957), hash `7a3e47595d7018caed44c65c56be0fb9558e0a1a69c8c87522c6e82d1d719d49`.

transcription: {"state": "known", "value": ["This rule does not apply to Leader Elephants."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.", "gap_ids": ["G916"]}

conditions: {"state": "known", "value": ["Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.", "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.", "Already routed cavalry automatically eliminated without DR."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Does not apply to Leader Elephants."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "TQ check comparison", "value": "DR > TQ", "unit": {"state": "known", "value": "die-roll comparison", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}, {"name": "Hits", "value": "DR–TQ; minimum result 1", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["On adjacency from non-adjacent hex; immediate check if cannot withdraw."], "reason": null, "gap_ids": []}

E916, `/evidence/15`, bajty [28605,29597), hash `9e4f30da57821c33dd930a08581e936b9990433103927de53462965fd0a0baf7`.

**context-01** — osobny wynik pending; porównane pola:

R916, `/rules/6`, bajty [282054,287456), hash `24d2167ad17175100c6e004dadba05315767f139f2955cd85082f5ebf04f590a`.

transcription: {"state": "known", "value": ["This rule does not apply to Leader Elephants."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.", "gap_ids": ["G916"]}

conditions: {"state": "known", "value": ["Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.", "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.", "Already routed cavalry automatically eliminated without DR."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Does not apply to Leader Elephants."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "TQ check comparison", "value": "DR > TQ", "unit": {"state": "known", "value": "die-roll comparison", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}, {"name": "Hits", "value": "DR–TQ; minimum result 1", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["On adjacency from non-adjacent hex; immediate check if cannot withdraw."], "reason": null, "gap_ids": []}

E916, `/evidence/15`, bajty [64824,65845), hash `b9ea1eb8048dde08eb59af663518460a7ac056c3419da5e46c58df1fdf78e4f8`.

Wyłączenia/niepewności: OW i ustalenie możliwości withdrawal wymagają kontekstu; zakres minimum dla DR≤TQ osobno.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-017

Dokładny zatwierdzony zakres: W9.16 przy DR<=TQ kawaleria nie otrzymuje CH; przy DR>TQ otrzymuje DR-TQ CH, z minimum1. Minimum nie wyłącza warunku DR>TQ.

Porównanie: R916 zachowuje DR>TQ/difference/minimum 1, ale interpretation=unknown i G916.blocking pozostawiają DR<=TQ nierozstrzygnięte. Zatwierdzona lokalna gałąź 0 CH nie jest jednoznacznie reprezentowana jako ustalona. SEM-001 nadal czeka na decyzję właściciela; nie stwierdzono błędnej transkrypcji ani zawsze 1 CH.

Propozycja: `incomplete_local_interpretation`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 left, C-9.16-01, bbox [45.0, 253.147, 297.021, 371.147]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

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

**first-001** — osobny wynik pending; porównane pola:

R916, `/rules/6`, bajty [214754,219957), hash `7a3e47595d7018caed44c65c56be0fb9558e0a1a69c8c87522c6e82d1d719d49`.

transcription: {"state": "known", "value": ["This rule does not apply to Leader Elephants."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.", "gap_ids": ["G916"]}

conditions: {"state": "known", "value": ["Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.", "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.", "Already routed cavalry automatically eliminated without DR."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Does not apply to Leader Elephants."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "TQ check comparison", "value": "DR > TQ", "unit": {"state": "known", "value": "die-roll comparison", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}, {"name": "Hits", "value": "DR–TQ; minimum result 1", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["On adjacency from non-adjacent hex; immediate check if cannot withdraw."], "reason": null, "gap_ids": []}

G916, `/gaps/0`, bajty [528984,529510), hash `5ace56915486ab06bd226069e9c9402e84707a60d8700dfad4c22e4c0da8059c`.

blocking: true

**context-01** — osobny wynik pending; porównane pola:

R916, `/rules/6`, bajty [282054,287456), hash `24d2167ad17175100c6e004dadba05315767f139f2955cd85082f5ebf04f590a`.

transcription: {"state": "known", "value": ["This rule does not apply to Leader Elephants."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.", "gap_ids": ["G916"]}

conditions: {"state": "known", "value": ["Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.", "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.", "Already routed cavalry automatically eliminated without DR."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Does not apply to Leader Elephants."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "TQ check comparison", "value": "DR > TQ", "unit": {"state": "known", "value": "die-roll comparison", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}, {"name": "Hits", "value": "DR–TQ; minimum result 1", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E916"], "reason": null, "gap_ids": []}, "evidence_ids": ["E916"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["On adjacency from non-adjacent hex; immediate check if cannot withdraw."], "reason": null, "gap_ids": []}

G916, `/gaps/0`, bajty [612466,613008), hash `1149bf75c9e07c293ae890ad880b22c217a1da8ed02d6a180000371aa8fa8a56`.

blocking: true

Wyłączenia/niepewności: LocalDR<=TQ0CH/DR>TQdifference+min1 interpretation andcriticality accepted; nofullOW/cavalryprocedure or targetmetadata closure.; Właściciel rozstrzyga zakres minimum z tekstem lub wskazuje potrzebny dowód.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-018

Dokładny zatwierdzony zakres: ELvsEL neither side PositionSuperiority, including no positionalASfromFlank/Rear; notallpossibletypesofsuperiorityexcluded.

Porównanie: R917 zawiera zakaz Position Superiority dla EL vs EL oraz pozycyjnego AS z Flank/Rear. Nie zawiera zakazu wszystkich rodzajów superiority. Pole o AS należy czytać wraz z zakresem Position Superiority; pełne ogólne procedury pozostają poza oceną.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 left, C-9.17-01, bbox [45.0, 378.547, 297.02, 424.547]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.17 In any instance where Elephant units attack other Elephant
> units, neither side may gain Position Superiority. Thus, one
> Elephant attacking another Elephant through the latter’s Flank/
> Rear does not gain Attack Superiority.

**first-001** — osobny wynik pending; porównane pola:

R917, `/rules/7`, bajty [219963,223365), hash `63af6f30b27679af5c8b57201640efcb4a3682e020bfdbe15a3d27e411c84ac6`.

transcription: {"state": "known", "value": ["neither side may gain Position Superiority."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Elephant attacks another Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R917, `/rules/7`, bajty [287463,290991), hash `cb0234059d792c80894b60db2acd72e1e243aba445d6746eeac66ddb3035eb0a`.

transcription: {"state": "known", "value": ["neither side may gain Position Superiority."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Elephant attacks another Elephant."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Nie rozszerzać zakazu na wszystkie rodzaje superiority.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-019

Dokładny zatwierdzony zakres: Any leader maycommandEL unlessrules specificallyotherwise. Actual leaderauthorization requirescheckingexceptions; keeprequires_context, no inventedactualeligibility.

Porównanie: R918.transcription zachowuje unless rules specifically otherwise, a exceptions=unknown wskazuje nieznane wyjątki. Jednak action_effect/interpretation brzmi Any leader may command i D918specific/G-D918specific mają blocks_full_result=false/blocking=false. Oznaczono brak źródła, lecz nie zadeklarowano blokady realnej autoryzacji. Kandydat SEM-009: właściwość deklaracji blokady w rzeczywistym użyciu wymaga decyzji; nie ma konkretnego niepoprawnie wybranego dowódcy.

Propozycja: `blocking_flag_conflict_pending`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 left, C-9.18-01, bbox [45.0, 455.45, 297.002, 477.45]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.18 Unless the rules specifically state otherwise, Elephant units
> may be commanded by any leader.

**first-001** — osobny wynik pending; porównane pola:

R918, `/rules/8`, bajty [223371,226469), hash `d2ef7d501f146bfd281fbaa1eae741db574916086ba549200fddadbe2e5c5cc1`.

transcription: {"state": "known", "value": ["Unless the rules specifically state otherwise, Elephant units may be commanded by any leader."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Any leader may command Elephant units.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Any leader may command Elephant units.", "reason": null, "gap_ids": []}

exceptions: {"state": "unknown", "value": null, "reason": "Specific exceptions are acknowledged but not enumerated in supplied clause.", "gap_ids": ["G-D918specific"]}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

D918specific, `/dependencies/58`, bajty [464010,465079), hash `46bc37098ddd17b19bb35251ad26ded1fe92ed25c86c4c900e3c2438c05dff5b`.

impact_if_missing: {"affected_ids": ["R918"], "blocks_full_result": false, "reason": "Unenumerated specific command exceptions is not fully supplied; no missing content reconstructed."}

G-D918specific, `/gaps/18`, bajty [538068,538573), hash `c3847703ebaacf82f8fe34d6c7bcf04b9a8a1eb02391ac68d50382088fd5f932`.

blocking: false

**context-01** — osobny wynik pending; porównane pola:

R918, `/rules/8`, bajty [290998,294212), hash `d7a45288d96c2d73bc22a2bc1b20b8c03362c7d8c907b908c1b9dfae8df0ae67`.

transcription: {"state": "known", "value": ["Unless the rules specifically state otherwise, Elephant units may be commanded by any leader."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Any leader may command Elephant units.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Any leader may command Elephant units.", "reason": null, "gap_ids": []}

exceptions: {"state": "unknown", "value": null, "reason": "Specific exceptions are acknowledged but not enumerated in supplied clause.", "gap_ids": ["G-D918specific"]}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

D918specific, `/dependencies/58`, bajty [540841,541937), hash `52edbbb6bd90058a52943715a9959a7d2fec9ad9eedc21249d17952bf12a0a27`.

impact_if_missing: {"affected_ids": ["R918"], "blocks_full_result": false, "reason": "Unenumerated specific command exceptions is not fully supplied; no missing content reconstructed."}

G-D918specific, `/gaps/18`, bajty [622124,622646), hash `2a3d8899a381c03d274291d16e984507b2e5d63d9fc7fa52cb05cb734fce6d9a`.

blocking: false

Wyłączenia/niepewności: Actual leader eligibility and rule-specific exceptions require external context.; Wskazany leader, scenariusz i źródło jego ograniczeń; lokalna reguła ogólna pozostaje znana.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-020

Dokładny zatwierdzony zakres: WhenIndianELfightAfricanEL:AfricanEL+1PreShockDRM, inadditiontoClashofSpearsandSwords andShockSuperiority notes; notIndian+1norallEL+1norwaiveroftablenotes.

Porównanie: R919.conditions: Indian vs African; +1 Pre-Shock wyłącznie African, dodatkowo do not Clash/SS. Nie przeniesiono DRM na Indian lub wszystkie EL; nie pominięto not przez ogólne zwolnienie.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 left, C-9.19-01, bbox [45.0, 484.85, 297.116, 542.85]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.19 Indians vs. Africans: In addition to the notes on the Clash of
> Spears and Swords and Shock Superiority Charts, the following
> rule is in effect when Indian Elephants fight African Elephants:
> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).

**first-001** — osobny wynik pending; porównane pola:

R919, `/rules/9`, bajty [226475,230470), hash `d55d07a6e11f89c7a28adb050205027c3cf23a3a60661483c5da133df78666d3`.

transcription: {"state": "known", "value": ["African Elephants incur a +1 DRM to their Pre-Shock die rolls (8.43)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Indian Elephants fight African Elephants."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "African Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E919"], "reason": null, "gap_ids": []}, "evidence_ids": ["E919"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R919, `/rules/9`, bajty [294219,298360), hash `0570133a32e2c860a0a2cd97438a1c41e489344facec89dbf3cac591a0f397ea`.

transcription: {"state": "known", "value": ["African Elephants incur a +1 DRM to their Pre-Shock die rolls (8.43)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Indian Elephants fight African Elephants."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "African Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E919"], "reason": null, "gap_ids": []}, "evidence_ids": ["E919"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Clash of Spears and Swords, Shock Superiority oraz 8.43 wymagają źródeł do pełnego Shock.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-021

Dokładny zatwierdzony zakres: Velites are LI, not SK; SK exceptions do not transfer by similarity. SK OW incurs Hits only via Rear; Velites via Flank or Rear. OW distance/MA condition belongs to EXP-022.

Porównanie: R92note: Velites to LI, nie SK. R921: OW Hits dla SK tylko Rear, Velites Flank/Rear. Nie przeniesiono wszystkich wyjątków SK na Velites. Historyczna nota ma operatywny fragment N-07-S2; pozostała historia poza gold.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 right, N-07-S2, bbox [319.0, 84.7, 563.059, 226.7], PDF 33 right, C-9.21-01, bbox [314.995, 235.94, 567.583, 317.94]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> Their forma-
> tion, however, was not so “open”, and they are not treated as
> skirmishers; they are Light Infantry, which also have some
> added maneuver capabilities.

> 9.21 Orderly Withdrawal: Skirmishers may Orderly
> Withdraw up to 2 hexes before any units whose MA
> is the same or less (i.e., all infantry units), regardless
> of the MA differential. The only time Skirmishers
> incur Cohesion Hits when using OW is after being approached
> from a Rear hex. The only time Velites incur Cohesion Hits from
> OW is after being approached from a Flank or Rear hex.

**first-001** — osobny wynik pending; porównane pola:

N92design, `/nodes/24`, bajty [142234,143048), hash `06557a0571509b2b41162d16c634800e71f5138b049bdbbe5d769f43280da535`.

content: {"state": "known", "value": "Historical context of Skirmisher weapons/open formation and harassment role, Velites first line of legionary deployment and less-open formation. Operative Velites classification owned by R92note.", "reason": null, "gap_ids": []}

R921, `/rules/11`, bajty [234091,238938), hash `cfe4efdae432e0047facb62fddc25627addc679b00fe30a91959f6a1c715ce32`.

transcription: {"state": "known", "value": ["Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "OW maximum", "value": 2, "unit": {"state": "known", "value": "hexes", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}, {"name": "approaching MA", "value": "<= withdrawing Skirmisher MA", "unit": {"state": "known", "value": "MA comparison", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

R92note, `/rules/10`, bajty [230476,234085), hash `77b7cd1fd5a784f68bdbc62ea18264365019ddc79b4a90cbc5326e7bfc953e23`.

transcription: {"state": "known", "value": ["they are not treated as skirmishers; they are Light Infantry, which also have some added maneuver capabilities."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

N92design, `/nodes/24`, bajty [191063,191904), hash `f714c9ad53d998b3e9866366d7a25d9c30c323a4ea051ff70b9acd807b945ea4`.

content: {"state": "known", "value": "Historical context of Skirmisher weapons/open formation and harassment role, Velites first line of legionary deployment and less-open formation. Operative Velites classification owned by R92note.", "reason": null, "gap_ids": []}

R921, `/rules/11`, bajty [302099,307124), hash `7d4cae8640312910b3a82d27a32c19c34148a5723d11798a0df99ab1c459d0aa`.

transcription: {"state": "known", "value": ["Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "OW maximum", "value": 2, "unit": {"state": "known", "value": "hexes", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}, {"name": "approaching MA", "value": "<= withdrawing Skirmisher MA", "unit": {"state": "known", "value": "MA comparison", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

R92note, `/rules/10`, bajty [298367,302092), hash `a9052b99d997213c3c6f44fe1a85290abe7bcd5df64b1f8caa64ed751a81072a`.

transcription: {"state": "known", "value": ["they are not treated as skirmishers; they are Light Infantry, which also have some added maneuver capabilities."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Added maneuver nie definiuje wszystkich uprawnień; procedura OW pozostaje zewnętrzna.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-022

Dokładny zatwierdzony zakres: SK may OW up to 2 hexes before an approaching unit with MA equal to or less than SK MA. OW angle costs belong to EXP-021; real routes remain context-dependent.

Porównanie: R921.conditions i parameters zachowują approaching MA<=SK MA oraz maksimum 2 hexów. action_effect powtarza źródłowe regardless of MA differential; trzeba je czytać w tym warunku, nie jako zniesienie <=. Pełna trasa i kąt OW są osobne. Sama fraza regardless nie jest błędem odczytu.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 right, C-9.21-01, bbox [314.995, 235.94, 567.583, 317.94]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.21 Orderly Withdrawal: Skirmishers may Orderly
> Withdraw up to 2 hexes before any units whose MA
> is the same or less (i.e., all infantry units), regardless
> of the MA differential. The only time Skirmishers
> incur Cohesion Hits when using OW is after being approached
> from a Rear hex. The only time Velites incur Cohesion Hits from
> OW is after being approached from a Flank or Rear hex.

**first-001** — osobny wynik pending; porównane pola:

R921, `/rules/11`, bajty [234091,238938), hash `cfe4efdae432e0047facb62fddc25627addc679b00fe30a91959f6a1c715ce32`.

transcription: {"state": "known", "value": ["Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "OW maximum", "value": 2, "unit": {"state": "known", "value": "hexes", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}, {"name": "approaching MA", "value": "<= withdrawing Skirmisher MA", "unit": {"state": "known", "value": "MA comparison", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R921, `/rules/11`, bajty [302099,307124), hash `7d4cae8640312910b3a82d27a32c19c34148a5723d11798a0df99ab1c459d0aa`.

transcription: {"state": "known", "value": ["Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmisher may OW up to 2 hexes regardless of MA differential.", "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "OW maximum", "value": 2, "unit": {"state": "known", "value": "hexes", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}, {"name": "approaching MA", "value": "<= withdrawing Skirmisher MA", "unit": {"state": "known", "value": "MA comparison", "evidence_ids": ["E921"], "reason": null, "gap_ids": []}, "evidence_ids": ["E921"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Pełna trasa OW wymaga procedury, mapy i danych.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-023

Dokładny zatwierdzony zakres: targetSKMissile+2DRM;SK/LIArchersA noH&D;LCanymissileclass noH&DvsSK

Porównanie: R922: target SK +2 Missile DRM; SK/LI Archers Class A nie H&D; LC każdego missile class nie H&D przeciw SK. Te zakazy nie ustalają pełnego lookupu MRRC lub reszty procedury.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 right, C-9.22-01, bbox [314.995, 325.34, 567.021, 371.34]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> 9.22 Missile Fire: There is a +2 DRM to the Missile Fire DR
> whenever a Skirmisher unit is the target. Skirmisher and Light
> Infantry Archers (Class A) cannot use H&D fire. Light Cavalry
> (all missile classes) cannot use H&D against Skirmishers..

**first-001** — osobny wynik pending; porównane pola:

R922, `/rules/12`, bajty [238944,243461), hash `a9598a0db96d75f2c086f3ef29f067d725296d84db5b293cc8eafd8a0cd1c7f2`.

transcription: {"state": "known", "value": ["There is a +2 DRM to the Missile Fire DR whenever a Skirmisher unit is the target."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["+2 Missile Fire DRM when Skirmisher is target.", "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.", "Light Cavalry of all missile classes cannot H&D against Skirmishers."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["+2 Missile Fire DRM when Skirmisher is target.", "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.", "Light Cavalry of all missile classes cannot H&D against Skirmishers."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher-target modifier", "value": 2, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E922"], "reason": null, "gap_ids": []}, "evidence_ids": ["E922"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R922, `/rules/12`, bajty [307131,311809), hash `68bf0a61ddd806de4cb7850830a717026f0a98611306b6b6f7c3155fcaf2c767`.

transcription: {"state": "known", "value": ["There is a +2 DRM to the Missile Fire DR whenever a Skirmisher unit is the target."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["+2 Missile Fire DRM when Skirmisher is target.", "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.", "Light Cavalry of all missile classes cannot H&D against Skirmishers."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["+2 Missile Fire DRM when Skirmisher is target.", "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.", "Light Cavalry of all missile classes cannot H&D against Skirmishers."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher-target modifier", "value": 2, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E922"], "reason": null, "gap_ids": []}, "evidence_ids": ["E922"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Wynik ognia wymaga MRRC i H&D; brak zakazu nie dowodzi pełnej legalności.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-024

Dokładny zatwierdzony zakres: SK cannot Shock attack; units attacking a defense consisting only of SK are exempt from Pre-Shock TQ even with the marker. With mixed defense use the other type and ignore SK Size. This owns the attacker exemption; EXP-004 owns the final Pass-Thru check.

Porównanie: R923: SK nie Shock attack; atakujący SK alone nie Pre-Shock nawet z markerem; mixed defense wybiera other type i pomija SK Size. Wyjątek końcowego Pass-Thru należy do EXP-004, nie do tego zwolnienia. Nowa DCTX923-S4 ma osobny pending.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 right, C-9.23-02, bbox [314.995, 405.62, 457.315, 415.62], PDF 33 right, C-9.23-03, bbox [314.995, 419.06, 567.159, 453.06], PDF 33 right, C-9.23-04, bbox [314.995, 456.5, 567.095, 490.5]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> • Skirmishers cannot Shock attack.

> • All units that Shock attack Skirmishers alone do not have
> to make a Pre-Shock TQ even if they have SHOCK MUST
> CHECK TQ markers.

> • If a Skirmisher unit is defending in coordination with any other
> unit type, the other Type must be chosen as the defender. The
> Size rating of the Skirmisher is ignored.

**first-001** — osobny wynik pending; porównane pola:

R923, `/rules/13`, bajty [243467,249760), hash `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

transcription: {"state": "known", "value": ["Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Shock Combat involving specified unit types."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmishers alone differs from mixed defense.", "Front LI attack exemption is not reciprocal."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}, {"name": "Skirmisher inflicted-Hits cap", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R923, `/rules/13`, bajty [311816,318317), hash `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

transcription: {"state": "known", "value": ["Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Shock Combat involving specified unit types."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmishers alone differs from mixed defense.", "Front LI attack exemption is not reciprocal."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}, {"name": "Skirmisher inflicted-Hits cap", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Nie przypisywać SK immunitetu od innych testów ani obrońcy mieszanego.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-025

Dokładny zatwierdzony zakres: HitsinflictedbySKhalvefloor,cap1

Porównanie: R923.action/parameters: Hits zadane przez SK pół, floor, maksimum 1 CH. W context-01 Step 4 dostarcza stronę atakującego przy obrońcy SK, lecz nie zmienia lokalnej treści R923. Nowa relacja i pełne applicability/base/CRT/order pozostają poza tą oceną.

Propozycja: `supported_local_scope`; właściciel **pending** dla obu hashów.

Źródło: PDF 33 right, C-9.23-05, bbox [314.995, 493.94, 567.01, 515.94]

Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):

> • Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.

**first-001** — osobny wynik pending; porównane pola:

R923, `/rules/13`, bajty [243467,249760), hash `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

transcription: {"state": "known", "value": ["Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Shock Combat involving specified unit types."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmishers alone differs from mixed defense.", "Front LI attack exemption is not reciprocal."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}, {"name": "Skirmisher inflicted-Hits cap", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

**context-01** — osobny wynik pending; porównane pola:

R923, `/rules/13`, bajty [311816,318317), hash `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

transcription: {"state": "known", "value": ["Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Shock Combat involving specified unit types."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmishers alone differs from mixed defense.", "Front LI attack exemption is not reciprocal."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}, {"name": "Skirmisher inflicted-Hits cap", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

Wyłączenia/niepewności: Bazowe Hits muszą być podane; kolejność innych modyfikatorów wymaga kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

## Granice tego pakietu

R921 „regardless of MA differential” jest frazą źródłową; warunek approaching MA<=SK MA nadal obowiązuje w conditions/parameters. Nie nazwano tego błędem odczytu. R917 dotyczy Position Superiority, nie wszystkich form superiority.

Znane operatory przy zadanych faktach nie wymagają automatycznie pełnego rzeczywistego setupu. Wszystkie gap.blocking do zakresów pełnego Shock/OW/CRT trzeba czytać oddzielnie od lokalnych operatorów. 20 sytuacji nie oceniono.

Potwierdzono równość wartości 18 mapowanych reguł/węzłów i wskazano osobne zakresy bajtów obu wyników; nie oznacza to identyczności leksykalnych bajtów ani poświadczenia znaczenia. Nowa DCTX923-S4, trzy dawne brakujące krytyczne pary i wszystkie pozostałe krawędzie nadal pending. 64 granice glifów i E916 nie zostały zamknięte.

Nie pozyskano źródeł ani pass-02, ekstrakcji lub korekt. Historyczne niewiadome izolacji/ekspozycji/selektorów/czasów/tokenów/ceny i aktywny budżet unknown. 49 dalszych oczekiwań w częściach .3/.4 pozostaje pending.
