# M-POC5A.3 — EXP-026–050

Propozycje Codex po porównaniu source spans i pól obu wyników; wszystkie nowe decyzje właściciela pending. Wcześniejsze 22 zaakceptowane lokalne zakresy pozostają osobną decyzją i nie akceptują nowych części tych samych reguł.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`.

first-001: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

Pełne ślady: [comparisons.json](comparisons.json). Nowa kwestia: [issues.json](issues.json). Czytelny pakiet: [owner-focus.md](owner-focus.md).

21 propozycji zgodności lokalnej, 2 właściwe potrzeby/blokady źródła, 1 niepełna lokalna interpretacja (SEM-002) i 1 niepełna jawność potrzeb setupu (SEM-010) do decyzji. Nie jest to zaakceptowany wynik jakości.

Powiązano 44 różnych pozycji inwentarza i 94 par rubryka/EXP. 24 z 26 mapowanych reguł/węzłów ma identyczne wartości; R932/N932ex różnią się. Nie poświadczono identyczności leksykalnych bajtów ani całego grafu.

## Pełne porównania w dokładnym zakresie

### EXP-026

Dokładny zatwierdzony zakres: PH/HI/LGdefendingFrontvsLI noPreShockevenwithattackermarker;LIstillcheck;reverseexemptionnotapplied

Porównanie: R923: PH/HI/LG broniące przez Front przed LI nie robią Pre-Shock nawet z markerem atakującego; LI nadal sprawdza. Reverse wyraźnie nie zachodzi. Nie rozszerzono na Flank/Rear lub inne typy.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 33 right, C-9.23-06, bbox [314.995, 519.38, 567.027, 589.38].

> • Phalanx (PH), Heavy Infantry (HI), and Legion Infantry (LG)
> units that are attacked from a Front hex by Light Infantry (LI)
> do not undergo a Pre-Shock TQ check even if the attackers have
> SHOCK MUST CHECK TQ markers, though the attacking LI
> still do. The reverse is not true; PH, HI and LG do undergo a
> Pre-Shock TQ check when attacking LI.

**first-001** — osobna propozycja/pending:

R923, `/rules/13`, bajty [243467,249760), hash `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

transcription: {"state": "known", "value": ["Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Shock Combat involving specified unit types."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmishers alone differs from mixed defense.", "Front LI attack exemption is not reciprocal."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}, {"name": "Skirmisher inflicted-Hits cap", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D923pre", "G-D923shock"]

**context-01** — osobna propozycja/pending:

R923, `/rules/13`, bajty [311816,318317), hash `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

transcription: {"state": "known", "value": ["Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Shock Combat involving specified unit types."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers cannot Shock attack.", "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.", "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.", "Hits inflicted by Skirmishers halved, round down, maximum 1.", "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.", "Reverse not true: PH/HI/LG attacking LI do check."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmishers alone differs from mixed defense.", "Front LI attack exemption is not reciprocal."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Skirmisher inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}, {"name": "Skirmisher inflicted-Hits cap", "value": 1, "unit": {"state": "known", "value": "Cohesion Hit", "evidence_ids": ["E923"], "reason": null, "gap_ids": []}, "evidence_ids": ["E923"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D923pre", "G-D923shock"]

Wyłączenia i niepewności: Nie rozszerzać na Flank/Rear ani inne typy.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-027

Dokładny zatwierdzony zakres: SKRouteliminated,facing0MP,no repeat-moveCohesioncost;no blanketterrain/stackingimmunity

Porównanie: R924: SK Rout oznacza eliminację, facing kosztuje 0 MP, ponowne ruchy w Game Turn bez Cohesion cost. Nie ma ogólnego zwolnienia z kosztów terenu i stacking.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 33 right, C-9.24-02, bbox [314.995, 652.88, 503.985, 662.88].

> • Skirmishers that Rout are eliminated instead.

Źródło PDF 33 right, C-9.24-04, bbox [314.995, 679.76, 567.113, 713.76].

> • See 6.69 for special stacking rules for Skirmishers and Velites.
> Skirmishers can change facing at no MP cost and can move
> more than once per Game Turn without a Cohesion cost.

**first-001** — osobna propozycja/pending:

R924, `/rules/14`, bajty [249766,255895), hash `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

transcription: {"state": "known", "value": ["Skirmishers do not make an Elephant Pass-Thru Check (9.11).", "the interruption is caused by only one such unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Line exception applies if interruption caused by only one such unit."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Single-unit interruption condition."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing cost", "value": 0, "unit": {"state": "known", "value": "MP", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}, {"name": "line interruption allowance", "value": 1, "unit": {"state": "known", "value": "Velites or Skirmisher unit per interruption", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Repeated movement within Game Turn."], "reason": null, "gap_ids": []}

gap_ids: ["G-D924stack", "G-D924line"]

**context-01** — osobna propozycja/pending:

R924, `/rules/14`, bajty [318324,324673), hash `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

transcription: {"state": "known", "value": ["Skirmishers do not make an Elephant Pass-Thru Check (9.11).", "the interruption is caused by only one such unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Line exception applies if interruption caused by only one such unit."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Single-unit interruption condition."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing cost", "value": 0, "unit": {"state": "known", "value": "MP", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}, {"name": "line interruption allowance", "value": 1, "unit": {"state": "known", "value": "Velites or Skirmisher unit per interruption", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Repeated movement within Game Turn."], "reason": null, "gap_ids": []}

gap_ids: ["G-D924stack", "G-D924line"]

Wyłączenia i niepewności: Koszty terenu i pełny stacking nie są wyłączone.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-028

Dokładny zatwierdzony zakres: oneSK/Velitespergap,notoneglobal;two consecutiveunits do notqualify

Porównanie: R924 i N924ex pokazują pojedynczą przerwę na gap, z możliwością oddzielnych powtórzeń. Dwa kolejne Velites w przykładzie nie tworzą line. Literalne układy 2808/2809/2810/2811/2812 zachowane; nie przyznano pełnej legalności 4.32.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 33 right, C-9.24-05, bbox [314.995, 717.2, 567.002, 739.2].

> • When determining lines for a Line Command (4.32), the pres-
> ence of a Velites or Skirmisher unit does not disrupt the line if

Źródło PDF 34 left, C-9.24-05, bbox [54.0, 54.004, 245.93, 64.004].

> the interruption is caused by only one such unit.

Źródło PDF 34 left, X-03, bbox [45.0, 71.224, 297.015, 141.224].

> EXAMPLE: There are Hastati in 2808, Velites in 2809, and Has-
> tati in 2810. This would still be eligible to be a line. However,
> if there were Velites in 2809 and 2810 and the Hastati in 2808
> and 2811, the two Hastati would not form a line. If there were
> Hastati in 2808, 2810, and 2812, with Velites in 2809 and 2811,
> the Hastati could form a line.

**first-001** — osobna propozycja/pending:

N924ex, `/nodes/3`, bajty [124483,126113), hash `6a3ef8e03ddb0e28dba14bc0413f7a3ed8013ed67c512e6e022456029c02a8f7`.

content: {"state": "known", "value": {"transcription": {"cases": [{"Hastati": ["2808", "2810"], "Velites": ["2809"], "line": "eligible"}, {"Hastati": ["2808", "2811"], "Velites": ["2809", "2810"], "line": "not formed by the two Hastati"}, {"Hastati": ["2808", "2810", "2812"], "Velites": ["2809", "2811"], "line": "could form"}]}, "interpretation": "Separated single interruptions may recur; two consecutive intervening Velites fail the illustrated line condition."}, "reason": null, "gap_ids": []}

R924, `/rules/14`, bajty [249766,255895), hash `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

transcription: {"state": "known", "value": ["Skirmishers do not make an Elephant Pass-Thru Check (9.11).", "the interruption is caused by only one such unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Line exception applies if interruption caused by only one such unit."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Single-unit interruption condition."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing cost", "value": 0, "unit": {"state": "known", "value": "MP", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}, {"name": "line interruption allowance", "value": 1, "unit": {"state": "known", "value": "Velites or Skirmisher unit per interruption", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Repeated movement within Game Turn."], "reason": null, "gap_ids": []}

gap_ids: ["G-D924stack", "G-D924line"]

**context-01** — osobna propozycja/pending:

N924ex, `/nodes/3`, bajty [172182,173878), hash `b672863aac81d4eb2fb84ba3e3ca1cae6b8d9c86491f7c4229e84afdeb4e726e`.

content: {"state": "known", "value": {"transcription": {"cases": [{"Hastati": ["2808", "2810"], "Velites": ["2809"], "line": "eligible"}, {"Hastati": ["2808", "2811"], "Velites": ["2809", "2810"], "line": "not formed by the two Hastati"}, {"Hastati": ["2808", "2810", "2812"], "Velites": ["2809", "2811"], "line": "could form"}]}, "interpretation": "Separated single interruptions may recur; two consecutive intervening Velites fail the illustrated line condition."}, "reason": null, "gap_ids": []}

R924, `/rules/14`, bajty [318324,324673), hash `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

transcription: {"state": "known", "value": ["Skirmishers do not make an Elephant Pass-Thru Check (9.11).", "the interruption is caused by only one such unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Line exception applies if interruption caused by only one such unit."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Skirmishers that Rout are eliminated instead.", "No Elephant Pass-Thru Check for Skirmishers.", "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.", "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Single-unit interruption condition."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing cost", "value": 0, "unit": {"state": "known", "value": "MP", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}, {"name": "line interruption allowance", "value": 1, "unit": {"state": "known", "value": "Velites or Skirmisher unit per interruption", "evidence_ids": ["E924", "E924cont"], "reason": null, "gap_ids": []}, "evidence_ids": ["E924", "E924cont"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Repeated movement within Game Turn."], "reason": null, "gap_ids": []}

gap_ids: ["G-D924stack", "G-D924line"]

Wyłączenia i niepewności: To lokalny wyjątek; pozostałe warunki 4.32 wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-029

Dokładny zatwierdzony zakres: LCMissileH&DstrictlowerMA,exceptSK;LCArchersfireOW via6.55;fullproceduresunknown

Porównanie: R931: missile-armed LC, target strictly lower MA (<, nie <=), wyjątek SK; LC Archers fire podczas OW według 6.55. G-D931HD/OW zatrzymują pełne procedury, nie znany warunek lokalny.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 left, C-9.31-01, bbox [45.0, 167.184, 297.005, 201.184].

> 9.31 Missile-armed Light Cavalry may use H&D fire (8.3) against
> all units with a lower MA, except Skirmishers. Light Cavalry
> Archers can fire when they use Orderly Withdrawal (6.55).

**first-001** — osobna propozycja/pending:

R931, `/rules/15`, bajty [255901,259855), hash `c203ab22fc5188464f7dabe7f42906f436da91d6c786eab4e76045ad31a63322`.

transcription: {"state": "known", "value": ["Light Cavalry Archers can fire when they use Orderly Withdrawal (6.55)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.", "LC Archers may fire while using OW."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Missile-armed LC using H&D against lower-MA target."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.", "LC Archers may fire while using OW."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmisher targets excluded."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "target MA", "value": "< LC MA", "unit": {"state": "known", "value": "MA comparison", "evidence_ids": ["E931"], "reason": null, "gap_ids": []}, "evidence_ids": ["E931"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Archer fire when using OW."], "reason": null, "gap_ids": []}

gap_ids: ["G-D931HD", "G-D931OW"]

**context-01** — osobna propozycja/pending:

R931, `/rules/15`, bajty [324680,328792), hash `9a16f1cac6ab3823e712cfd40b143d10ef7906f1848eeb7b1425e3affe652b04`.

transcription: {"state": "known", "value": ["Light Cavalry Archers can fire when they use Orderly Withdrawal (6.55)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.", "LC Archers may fire while using OW."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Missile-armed LC using H&D against lower-MA target."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.", "LC Archers may fire while using OW."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Skirmisher targets excluded."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "target MA", "value": "< LC MA", "unit": {"state": "known", "value": "MA comparison", "evidence_ids": ["E931"], "reason": null, "gap_ids": []}, "evidence_ids": ["E931"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Archer fire when using OW."], "reason": null, "gap_ids": []}

gap_ids: ["G-D931HD", "G-D931OW"]

Wyłączenia i niepewności: Sama przewaga MA nie domyka H&D; konieczna procedura 8.3.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-030

Dokładny zatwierdzony zakres: attackingLCHitsvsPH/HI/MI/LG/BI halvefloor

Porównanie: Lokalne R932.action_effect/parameters w obu wynikach zachowują pół/floor Hits zadanych przez atakujące LC PH/HI/MI/LG/BI. context-01 zmienia interpretation/exceptions, lecz nie literalną lokalną transkrypcję ani parametr. Ta propozycja nie akceptuje nowych operatorów/wyjątku Routed, całej R932, relacji ani kolejności AS/LC; SEM-003 nadal pending.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 left, C-9.32-01, bbox [45.0, 208.584, 297.009, 242.584].

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).

**first-001** — osobna propozycja/pending:

R932, `/rules/16`, bajty [259861,263502), hash `cfce4763843cd4617670464caf65022de44c34273a2423cb87d74de3dd3c2624`.

transcription: {"state": "known", "value": ["are halved (round down)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Halve such inflicted Cohesion Hits, round down.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Attacking LC inflicts Hits against PH or HI/MI/LG/BI."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Halve such inflicted Cohesion Hits, round down.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E932"], "reason": null, "gap_ids": []}, "evidence_ids": ["E932"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G932", "G-D932CRT"]

**context-01** — osobna propozycja/pending:

R932, `/rules/16`, bajty [328799,333292), hash `064aae5db27a9bda8dd053c7d30ce2d21255bc4236946d1083acd1e2d946dabe`.

transcription: {"state": "known", "value": ["are halved (round down)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "9.32 locally halves such LC-inflicted Cohesion Hits, round down. Added Step 4 bullet #4 qualifies reduction: attacker used in determination is LC (8.45), no reduction against a Routed defender, cumulative with bullet #1, which doubles defender result when attacker superior (AS). No actual applicability, base result, combined operation/rounding order or final result established.", "reason": "Unreviewed bounded-context interpretation; original local literal transcription and parameters unchanged.", "gap_ids": ["G932", "G-D932CRT", "GCTX-order", "GCTX-845"]}

conditions: {"state": "known", "value": ["Attacking LC inflicts Hits against PH or HI/MI/LG/BI."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Halve such inflicted Cohesion Hits, round down.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Supplied 8.46 Step 4 bullet #4: LC reduction does not apply if defender is Routed."], "reason": "Qualification from added bounded context; not inserted into 9.32 literal transcription.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E932"], "reason": null, "gap_ids": []}, "evidence_ids": ["E932"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G932", "G-D932CRT", "GCTX-order", "GCTX-845"]

Wyłączenia i niepewności: Zależność od AS w przykładzie X-04 wymaga osobnej interpretacji/kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-031

Dokładny zatwierdzony zakres: AS/halvingprintedresultconflict requirescontext;no newexceptioninvented

Porównanie: first-001 zachowuje literalny printed-result przykład i unknown interpretację; G932/G-D932CRT blocking. context-01 dodaje źródłowe kwalifikacje AS/LC/Routed, ale N932ex nadal unknown i GCTX-order/CRT/applicability/845 blocking. Propozycja: właściwe zachowanie nierozstrzygnięcia pełnego przykładu i potrzeby kontekstu; źródłowa poprawność samych nowych operatorów pozostaje osobnym SEM-003, bez założenia automatycznego znoszenia 2x i pół.

Propozycja: `source_block_supported`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 left, C-9.32-01, bbox [45.0, 208.584, 297.009, 242.584].

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).

Źródło PDF 34 left, X-04, bbox [45.0, 249.084, 297.009, 283.084].

> EXAMPLE: A Light Cavalry unit with Attack Superiority (AS)
> against a Heavy Infantry unit would use the printed result on
> the Shock CRT.

**first-001** — osobna propozycja/pending:

N932ex, `/nodes/4`, bajty [126119,127170), hash `267371a59674521bf587b0dc168aaec6f2a0370510a765edb525f92a91ad022d`.

content: {"state": "known", "value": {"transcription": "A Light Cavalry unit with Attack Superiority (AS) against a Heavy Infantry unit would use the printed result on the Shock CRT.", "interpretation": {"state": "unknown", "value": null, "evidence_ids": [], "reason": "Example relation to halving cannot be resolved from supplied general AS/CRT descriptions.", "gap_ids": ["G932"]}}, "reason": null, "gap_ids": []}

R932, `/rules/16`, bajty [259861,263502), hash `cfce4763843cd4617670464caf65022de44c34273a2423cb87d74de3dd3c2624`.

transcription: {"state": "known", "value": ["are halved (round down)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Halve such inflicted Cohesion Hits, round down.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Attacking LC inflicts Hits against PH or HI/MI/LG/BI."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Halve such inflicted Cohesion Hits, round down.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E932"], "reason": null, "gap_ids": []}, "evidence_ids": ["E932"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G932", "G-D932CRT"]

G932, `/gaps/1`, bajty [529516,530113), hash `43cf016d3697d9674abe943581db6ce085b1bd34d93ebff98716ba95c28cb7db`.

blocking: true

**context-01** — osobna propozycja/pending:

N932ex, `/nodes/4`, bajty [173885,175403), hash `0eb4d362032a4ff5fd28d28ce38de975b77453af7223949fec3d0d816223b27c`.

content: {"state": "known", "value": {"transcription": "A Light Cavalry unit with Attack Superiority (AS) against a Heavy Infantry unit would use the printed result on the Shock CRT.", "interpretation": {"state": "unknown", "value": null, "evidence_ids": ["E932ex", "ECTX846S4-AS", "ECTX846S4-LC"], "reason": "Added source supplies AS 2x defender result and cumulative LC halving, with round down and Routed exception. Exact table, applicability and combined operation/rounding order unavailable; printed-result example retained without declaring executable equality.", "gap_ids": ["G932", "GCTX-order", "G-D932CRT"]}}, "reason": null, "gap_ids": []}

R932, `/rules/16`, bajty [328799,333292), hash `064aae5db27a9bda8dd053c7d30ce2d21255bc4236946d1083acd1e2d946dabe`.

transcription: {"state": "known", "value": ["are halved (round down)."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "9.32 locally halves such LC-inflicted Cohesion Hits, round down. Added Step 4 bullet #4 qualifies reduction: attacker used in determination is LC (8.45), no reduction against a Routed defender, cumulative with bullet #1, which doubles defender result when attacker superior (AS). No actual applicability, base result, combined operation/rounding order or final result established.", "reason": "Unreviewed bounded-context interpretation; original local literal transcription and parameters unchanged.", "gap_ids": ["G932", "G-D932CRT", "GCTX-order", "GCTX-845"]}

conditions: {"state": "known", "value": ["Attacking LC inflicts Hits against PH or HI/MI/LG/BI."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Halve such inflicted Cohesion Hits, round down.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Supplied 8.46 Step 4 bullet #4: LC reduction does not apply if defender is Routed."], "reason": "Qualification from added bounded context; not inserted into 9.32 literal transcription.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "inflicted-Hits scaling", "value": "1/2, round down", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E932"], "reason": null, "gap_ids": []}, "evidence_ids": ["E932"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G932", "G-D932CRT", "GCTX-order", "GCTX-845"]

G932, `/gaps/1`, bajty [613015,613877), hash `40ca31a42e0dc11f02dc67847683cb0ede5435964a848312c5b720bfbb8bc5d4`.

blocking: true

Wyłączenia i niepewności: AS/LC printed result versus halving order and tables remain unresolved.; Ograniczony dowód bazowego AS/CRT; decyzja właściciela o kolejności.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-032

Dokładny zatwierdzony zakres: movingFrontPHDefense2Lperqualifyingflank,HI1Lperflank;excludestartadjacentstayed,FlankRear,anyPHattacker

Porównanie: R941.conditions: moves adjacent i Shock przez Front; po 2L na flank zajęty przez friendly PH lub w friendly PH ZOC, HI any Class 1L zamiast 2L. Wyłączenia: rozpoczęcie adjacent i pozostanie tam, Flank/Rear oraz jakikolwiek PH wśród atakujących. Brak CRT nie blokuje podanego lokalnego shiftu.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 left, C-9.41-01, bbox [45.0, 309.044, 297.032, 427.044].

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

**first-001** — osobna propozycja/pending:

R941, `/rules/17`, bajty [263508,268383), hash `112f98003ed54c0f8f09d2d00327263a8c7c577c036536d988707561e7dbac94`.

transcription: {"state": "known", "value": ["If the attacker is Heavy Infantry (any Class), the shift is 1L instead."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Attacker moves adjacent then Shock attacks Phalanx from defender Front.", "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Only moving attacks; not attacker starting adjacent and staying.", "No Flank/Rear attacks.", "No application if any attacker is a Phalanx."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "ordinary shift", "value": "2L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}, {"name": "HI shift", "value": "1L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Moves adjacent then attacks; starting-adjacent stationary attacks excluded."], "reason": null, "gap_ids": []}

gap_ids: ["G-D941CRT"]

**context-01** — osobna propozycja/pending:

R941, `/rules/17`, bajty [333299,338353), hash `554b4ecd3a2ad5a80f0fa28cafc3c8b8f0528efdd7418e7d1999840cae58b045`.

transcription: {"state": "known", "value": ["If the attacker is Heavy Infantry (any Class), the shift is 1L instead."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Attacker moves adjacent then Shock attacks Phalanx from defender Front.", "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Only moving attacks; not attacker starting adjacent and staying.", "No Flank/Rear attacks.", "No application if any attacker is a Phalanx."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "ordinary shift", "value": "2L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}, {"name": "HI shift", "value": "1L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Moves adjacent then attacks; starting-adjacent stationary attacks excluded."], "reason": null, "gap_ids": []}

gap_ids: ["G-D941CRT"]

Wyłączenia i niepewności: Lokalny shift, nie pełny wynik CRT bez tabeli.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-033

Dokładny zatwierdzony zakres: scenarioDDeligibilitylistnecessary,missingblocksSIT11

Porównanie: R95note/N95design zachowują operatywny wymóg scenario-specific eligible units, R951 warunek eligible. G-D95scenario blocking=true, brak listy nie zastąpiony zgodą dla wszystkich PH. N953ex to jedynie odesłanie do przykładu; jego nonblocking nie zamyka krytycznej listy eligibility. Nie oceniono SIT-11.

Propozycja: `source_block_supported`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, N-09-S2, bbox [319.0, 70.3, 563.01, 116.3].

> Eligible units are listed in the scenario-specific rules.

Źródło PDF 34 right, C-9.51-01, bbox [315.0, 125.54, 567.115, 243.54].

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

Źródło PDF 34 right, X-06, bbox [315.0, 701.54, 533.58, 711.54].

> EXAMPLE: See the scenario rules for Cynoscephalae.

**first-001** — osobna propozycja/pending:

N953ex, `/nodes/6`, bajty [128320,128971), hash `32ad4997be80003431ce7d9782486b53cafcb6a9bd4a6ba63f26a0091bbff9b9`.

content: {"state": "known", "value": "See the scenario rules for Cynoscephalae; example content is not supplied.", "reason": null, "gap_ids": []}

N95design, `/nodes/26`, bajty [143799,144517), hash `befa3bbc8e95ad44cd60c24834e7ac7c76df7271a4c228979bb40b3ec394ab04`.

content: {"state": "known", "value": "Post-Alexandrian Macedonian formation rationale. Scenario eligibility requirement owned by R95note.", "reason": null, "gap_ids": []}

R951, `/rules/19`, bajty [271660,276889), hash `6ed20d621c4094781ff1689567d941ab7d22e764fe9a78ef1686795326e5e7a7`.

transcription: {"state": "known", "value": ["This completes the movement for both units for that Orders Phase."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Eligible Phalanxes; “back” PH begins directly behind “front” PH.", "Individual Order or Line Command directly from OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "DD stack size", "value": 2, "unit": {"state": "known", "value": "Phalanx units per hex", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}, {"name": "formation additional cost", "value": 1, "unit": {"state": "known", "value": "MP plus normal terrain cost", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Starting position at start of back PH movement.", "No further movement for either unit that Orders Phase."], "reason": null, "gap_ids": []}

gap_ids: ["G-D951OC", "G-D951terrain"]

R95note, `/rules/18`, bajty [268389,271654), hash `119eed8150bbbc291da6700cfdd1cf837f904262b76165126e4b13fd265bbf7c`.

transcription: {"state": "known", "value": ["Eligible units are listed in the scenario-specific rules."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Double-Depth eligible units are determined by scenario-specific rules.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Double-Depth eligible units are determined by scenario-specific rules.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D95scenario"]

G-D95scenario, `/gaps/33`, bajty [545320,545797), hash `ffc2b8f02e837a46b5e9af729d8cbb8bf17509c59767c860a00a3e04b0ee9259`.

blocking: true

**context-01** — osobna propozycja/pending:

N953ex, `/nodes/6`, bajty [176598,177276), hash `32059fb98dda21cbaacbf3674087807d1696268d8d9a7236e4b6220eb6b7380f`.

content: {"state": "known", "value": "See the scenario rules for Cynoscephalae; example content is not supplied.", "reason": null, "gap_ids": []}

N95design, `/nodes/26`, bajty [192684,193429), hash `f17c97f5b1d2fb4d5811fb18481d7ff3dfbe32f09a24af8c9e2568f554fabe8c`.

content: {"state": "known", "value": "Post-Alexandrian Macedonian formation rationale. Scenario eligibility requirement owned by R95note.", "reason": null, "gap_ids": []}

R951, `/rules/19`, bajty [341748,347170), hash `5a34602f7f460a66fe124c94424a27e1ac98d03e9da186e73f8c2763358bf313`.

transcription: {"state": "known", "value": ["This completes the movement for both units for that Orders Phase."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Eligible Phalanxes; “back” PH begins directly behind “front” PH.", "Individual Order or Line Command directly from OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "DD stack size", "value": 2, "unit": {"state": "known", "value": "Phalanx units per hex", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}, {"name": "formation additional cost", "value": 1, "unit": {"state": "known", "value": "MP plus normal terrain cost", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Starting position at start of back PH movement.", "No further movement for either unit that Orders Phase."], "reason": null, "gap_ids": []}

gap_ids: ["G-D951OC", "G-D951terrain"]

R95note, `/rules/18`, bajty [338360,341741), hash `45f74a06c6c69fbd84bd9aff1a0d58e7f58f502096e2ab3bd83ae51d84aedf49`.

transcription: {"state": "known", "value": ["Eligible units are listed in the scenario-specific rules."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Double-Depth eligible units are determined by scenario-specific rules.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Double-Depth eligible units are determined by scenario-specific rules.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D95scenario"]

G-D95scenario, `/gaps/33`, bajty [630196,630690), hash `3e15292276ba3e8a68b020af426167df2b461ba730b0f23460eb69d28884545c`.

blocking: true

Wyłączenia i niepewności: Scenario-specific Double-Depth eligibility list is required.; Wybrany scenariusz z listą uprawnionych jednostek.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-034

Dokładny zatwierdzony zakres: formingDDIOorLCdirectOC,backstartsbehindfront,terraincost+1MP,backunderfront,endbothmovementthisphase

Porównanie: R951: IO albo LC bezpośrednio od OC, back PH startuje bezpośrednio za front, płaci terrain+1 MP, trafia pod front; kończy ruch obu w tej Orders Phase. Nie ustalono realnej eligibility, OC ani kosztu terenu.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, C-9.51-01, bbox [315.0, 125.54, 567.115, 243.54].

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

**first-001** — osobna propozycja/pending:

R951, `/rules/19`, bajty [271660,276889), hash `6ed20d621c4094781ff1689567d941ab7d22e764fe9a78ef1686795326e5e7a7`.

transcription: {"state": "known", "value": ["This completes the movement for both units for that Orders Phase."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Eligible Phalanxes; “back” PH begins directly behind “front” PH.", "Individual Order or Line Command directly from OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "DD stack size", "value": 2, "unit": {"state": "known", "value": "Phalanx units per hex", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}, {"name": "formation additional cost", "value": 1, "unit": {"state": "known", "value": "MP plus normal terrain cost", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Starting position at start of back PH movement.", "No further movement for either unit that Orders Phase."], "reason": null, "gap_ids": []}

gap_ids: ["G-D951OC", "G-D951terrain"]

**context-01** — osobna propozycja/pending:

R951, `/rules/19`, bajty [341748,347170), hash `5a34602f7f460a66fe124c94424a27e1ac98d03e9da186e73f8c2763358bf313`.

transcription: {"state": "known", "value": ["This completes the movement for both units for that Orders Phase."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Eligible Phalanxes; “back” PH begins directly behind “front” PH.", "Individual Order or Line Command directly from OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Double-Depth permits two PH in one hex.", "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.", "Movement of both units complete for Orders Phase."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "DD stack size", "value": 2, "unit": {"state": "known", "value": "Phalanx units per hex", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}, {"name": "formation additional cost", "value": 1, "unit": {"state": "known", "value": "MP plus normal terrain cost", "evidence_ids": ["E951"], "reason": null, "gap_ids": []}, "evidence_ids": ["E951"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Starting position at start of back PH movement.", "No further movement for either unit that Orders Phase."], "reason": null, "gap_ids": []}

gap_ids: ["G-D951OC", "G-D951terrain"]

Wyłączenia i niepewności: Eligibility, OC i koszt terenu jako osobne potrzebne fakty.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-035

Dokładny zatwierdzony zakres: OCordersonly,2IOwhenIOmovement,PAWvia6.8,noWheel/Reverse/Column;unstacktopmoves,bottomstays,IOorLCasabove;fullLCprocedure notclosed

Porównanie: R952: rozkazy tylko OC; 2 IO przy ruchu w trybie IO, PAW 6.8, no Wheel/Reverse/Column. Unstack IO lub LC as above, top rusza za normalny koszt, bottom zostaje. R951 i pierwszy warunek OC zachowują zakres as above; nie domknięto pełnej procedury LC lub PAW.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, C-9.52-02, bbox [315.0, 277.82, 515.91, 287.82].

> • The units may receive orders only from the OC.

Źródło PDF 34 right, C-9.52-03, bbox [315.0, 291.26, 567.011, 325.26].

> • They may move as one unit, but it takes 2 Individual Orders
> (when using Individual Orders) to move both units together.
> They may use Pre-Arranged Withdrawal (6.8).

Źródło PDF 34 right, C-9.52-04, bbox [315.0, 328.7, 567.008, 374.7].

> • The units may not Wheel (6.44), Reverse (6.45), or use Col-
> umn (6.7). Unstacking requires an Individual Order or Line
> Command as above, at which time the top unit moves off at
> normal costs. The bottom unit must remain in place.

**first-001** — osobna propozycja/pending:

R952, `/rules/20`, bajty [276895,283151), hash `d3c03f8437c1acf3a3540923b725ecef09aac6ba7a23ecba4b82837c59d2d011`.

transcription: {"state": "known", "value": ["The units always use their 4 MA; they never use their 5 MA for anything."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Units in Double Depth."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "joint movement cost", "value": 2, "unit": {"state": "known", "value": "Individual Orders", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "usable MA", "value": 4, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "excluded MA", "value": 5, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D952PAW", "G-D952wheel", "G-D952reverse", "G-D952column"]

**context-01** — osobna propozycja/pending:

R952, `/rules/20`, bajty [347177,353653), hash `bbf568a4a71dbd5e7ae685da23f7c7d5c0527aab3e5650cf8fb3695982a880d3`.

transcription: {"state": "known", "value": ["The units always use their 4 MA; they never use their 5 MA for anything."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Units in Double Depth."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "joint movement cost", "value": 2, "unit": {"state": "known", "value": "Individual Orders", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "usable MA", "value": 4, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "excluded MA", "value": 5, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D952PAW", "G-D952wheel", "G-D952reverse", "G-D952column"]

Wyłączenia i niepewności: Procedury zewnętrzne 6.8/6.44/6.45/6.7 i orders pozostają potrzebne dla pełnego wykonania.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-036

Dokładny zatwierdzony zakres: readyDDMA4never5,movementHittoeach,nounitthroughorintoreadyDD;forming9.51separate

Porównanie: R952 dla units in DD: zawsze MA4, nigdy MA5; movement CH do każdej, zakaz wejścia/przejścia jakiegokolwiek unit przez gotowy DD. R951 osobno reprezentuje etap formowania, zanim gotowy stack istnieje. Nie odczytano zakazu jako anulowania formowania.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, C-9.52-05, bbox [315.0, 378.14, 567.551, 412.14].

> • The units always use their 4 MA; they never use their 5 MA
> for anything. For any movement that would incur a Cohesion
> Hit, both units incur the Hit.

Źródło PDF 34 right, C-9.52-06, bbox [315.0, 415.58, 567.02, 437.58].

> • No unit, of any type, may ever move through or into a Double
> Depth stack. Treat them as impassable terrain.

**first-001** — osobna propozycja/pending:

R952, `/rules/20`, bajty [276895,283151), hash `d3c03f8437c1acf3a3540923b725ecef09aac6ba7a23ecba4b82837c59d2d011`.

transcription: {"state": "known", "value": ["The units always use their 4 MA; they never use their 5 MA for anything."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Units in Double Depth."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "joint movement cost", "value": 2, "unit": {"state": "known", "value": "Individual Orders", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "usable MA", "value": 4, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "excluded MA", "value": 5, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D952PAW", "G-D952wheel", "G-D952reverse", "G-D952column"]

**context-01** — osobna propozycja/pending:

R952, `/rules/20`, bajty [347177,353653), hash `bbf568a4a71dbd5e7ae685da23f7c7d5c0527aab3e5650cf8fb3695982a880d3`.

transcription: {"state": "known", "value": ["The units always use their 4 MA; they never use their 5 MA for anything."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Units in Double Depth."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Orders only from OC.", "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.", "Cannot Wheel, Reverse or use Column.", "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.", "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.", "No unit of any type may enter or pass through DD stack; impassable terrain."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "joint movement cost", "value": 2, "unit": {"state": "known", "value": "Individual Orders", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "usable MA", "value": 4, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}, {"name": "excluded MA", "value": 5, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E952"], "reason": null, "gap_ids": []}, "evidence_ids": ["E952"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D952PAW", "G-D952wheel", "G-D952reverse", "G-D952column"]

Wyłączenia i niepewności: Przypadek formowania DD z 9.51 wymaga rozróżnienia etapu od gotowej formacji.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-037

Dokładny zatwierdzony zakres: combinedSize,topTQunlessRearthenbottom;otherchecksifselectedunitincursHits;actualTQvaluesunknown

Porównanie: R953: combine Sizes, TQ top, przy Rear bottom; jeśli wybrana do check jednostka dostaje jakiekolwiek Hits, druga również sprawdza. Unknown interpretacja końcowej eliminacji G953 nie uchyla jawnych wcześniejszych efektów; prawdziwe ratingi i pełny check nieustalone.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, C-9.53-02, bbox [315.0, 471.68, 475.37, 481.68].

> • The Sizes of both units are combined.

Źródło PDF 34 right, C-9.53-03, bbox [315.0, 485.12, 567.017, 519.12].

> • Only the top unit is used for TQ checks (unless attacked from
> the rear, in which case it’s the bottom unit). However, if that
> unit incurs any Cohesion Hits, then the other unit checks.

**first-001** — osobna propozycja/pending:

R953, `/rules/21`, bajty [283157,290596), hash `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

**context-01** — osobna propozycja/pending:

R953, `/rules/21`, bajty [353660,361365), hash `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

Wyłączenia i niepewności: Ogólny test TQ i inne modyfikatory poza lokalną selekcją wymagają celu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-038

Dokładny zatwierdzony zakres: enemydefendingagainstDD+1PreShock,DDdefending-1;9.41conditionsstillapply

Porównanie: R953: przeciwnik broniący się przed DD +1 Pre-Shock; DD jako defender -1. R941 w mapowanym zakresie zachowuje warunki i wyłączenia Phalanx Defense, więc nie przyznano shiftu bezwarunkowo. Nie nadaje to formalnego TP krawędzi R953→R941.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, C-9.53-04, bbox [315.0, 522.56, 567.002, 544.56].

> • Units defending against a Shock attack by units in Double
> Depth incur a +1 DRM to their Pre-Shock TQ check die rolls.

Źródło PDF 34 right, C-9.53-05, bbox [315.0, 548.0, 567.102, 570.0].

> • Defending units at Double Depth earn a –1 DRM to their Pre-
> Shock TQ check die rolls. Phalanx Defense (9.41) also applies.

Źródło PDF 34 left, C-9.41-01, bbox [45.0, 309.044, 297.032, 427.044].

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

**first-001** — osobna propozycja/pending:

R941, `/rules/17`, bajty [263508,268383), hash `112f98003ed54c0f8f09d2d00327263a8c7c577c036536d988707561e7dbac94`.

transcription: {"state": "known", "value": ["If the attacker is Heavy Infantry (any Class), the shift is 1L instead."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Attacker moves adjacent then Shock attacks Phalanx from defender Front.", "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Only moving attacks; not attacker starting adjacent and staying.", "No Flank/Rear attacks.", "No application if any attacker is a Phalanx."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "ordinary shift", "value": "2L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}, {"name": "HI shift", "value": "1L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Moves adjacent then attacks; starting-adjacent stationary attacks excluded."], "reason": null, "gap_ids": []}

gap_ids: ["G-D941CRT"]

R953, `/rules/21`, bajty [283157,290596), hash `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

**context-01** — osobna propozycja/pending:

R941, `/rules/17`, bajty [333299,338353), hash `554b4ecd3a2ad5a80f0fa28cafc3c8b8f0528efdd7418e7d1999840cae58b045`.

transcription: {"state": "known", "value": ["If the attacker is Heavy Infantry (any Class), the shift is 1L instead."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Attacker moves adjacent then Shock attacks Phalanx from defender Front.", "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Only moving attacks; not attacker starting adjacent and staying.", "No Flank/Rear attacks.", "No application if any attacker is a Phalanx."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "ordinary shift", "value": "2L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}, {"name": "HI shift", "value": "1L", "unit": {"state": "known", "value": "Shock CRT columns left per qualifying Flank hex", "evidence_ids": ["E941"], "reason": null, "gap_ids": []}, "evidence_ids": ["E941"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Moves adjacent then attacks; starting-adjacent stationary attacks excluded."], "reason": null, "gap_ids": []}

gap_ids: ["G-D941CRT"]

R953, `/rules/21`, bajty [353660,361365), hash `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

Wyłączenia i niepewności: R-9.53→R-9.41 to użycie warunkowej modyfikacji, nie odwrotny kierunek.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-039

Dokładny zatwierdzony zakres: FlankReardefenderShockHits3xinstead2x,equalallocationoddtop;missileHits topunlessRearthenbottom

Porównanie: R953: Hits DD defender w Shock przez Flank/Rear 3x zamiast 2x; Shock rozdzielony równo, nieparzysty Hit do top. Missile do top z wyjątkiem Rear do bottom. Selekcja TQ przez Rear nie zmienia odd-Hit allocation Shock; baza i inne mnożniki pozostają poza zakresem.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, C-9.53-06, bbox [315.0, 573.44, 567.011, 607.44].

> • If a Double Depth stack is Shock attacked from a Flank or
> Rear hex, the defender Cohesion Hits are tripled (3x) instead
> of doubled.

Źródło PDF 34 right, C-9.53-07, bbox [315.0, 610.88, 567.07, 656.88].

> • Cohesion Hits from Shock are distributed equally between the
> two units, with any odd Hits going to the top unit. Cohesion Hits
> from Missile Fire Hits apply only to the top unit unless fire is
> through a Rear hex, in which case Hits apply to the bottom unit.

**first-001** — osobna propozycja/pending:

R953, `/rules/21`, bajty [283157,290596), hash `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

**context-01** — osobna propozycja/pending:

R953, `/rules/21`, bajty [353660,361365), hash `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

Wyłączenia i niepewności: Bazowy wynik i kolejność wobec innych mnożników muszą być dostarczone/zweryfikowane.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-040

Dokładny zatwierdzony zakres: When one PH of DD Routs, both Rout and retreat separately. Eliminate each PH individually if it cannot complete legal Rout movement; the other may perform its own legal Rout if possible. Actual geometry, 6.69/10.22, order/shared sole destination and later D1 result are unclosed. Local 10.24/25/23 context is supporting evidence, not an additional scoring unit.

Porównanie: Oba R953 zachowują both rout i separate hexes, ale końcowe the unit pozostaje literalne; interpretation unknown/G953 blocking. Eval-v1 ma per-unit eliminację z możliwością legalnego Rout drugiej PH. Propozycja niepełnej reprezentacji tej lokalnej gałęzi pozostaje SEM-002 pending; osobno dostępność podparcia 10.24/25/23 dla ekstraktora i rzeczywista geometria/kolejność.

Propozycja: `incomplete_local_interpretation_pending_source_availability`; decyzja właściciela pending dla obu hashów.

Źródło PDF 34 right, C-9.53-08, bbox [315.0, 660.32, 567.03, 694.32].

> • If either unit in the stack routs, they both rout. The units must
> retreat to separate hexes. If this is not possible, the unit is
> eliminated instead.

**first-001** — osobna propozycja/pending:

R953, `/rules/21`, bajty [283157,290596), hash `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

G953, `/gaps/2`, bajty [530119,530709), hash `e7acbacfb4fb7b0f9a12bc3d1bf41019f7507987177c49efc34ba8b596816a21`.

blocking: true

**context-01** — osobna propozycja/pending:

R953, `/rules/21`, bajty [353660,361365), hash `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription: {"state": "known", "value": ["If either unit in the stack routs, they both rout."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "unknown", "value": null, "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.", "gap_ids": ["G953"]}

conditions: {"state": "known", "value": ["Double Depth combat."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combine Sizes.", "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.", "Defenders against DD Shock incur +1 Pre-Shock DRM.", "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.", "DD defender Hits from Flank/Rear Shock tripled, not doubled.", "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.", "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Rear attack uses bottom TQ/check and rear fire bottom Hits.", "Flank/Rear Shock uses 3x.", "Odd Shock Hit to top."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "defender versus DD Pre-Shock modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "DD defender Pre-Shock modifier", "value": -1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Flank/Rear Shock multiplier", "value": 3, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "replaced multiplier", "value": 2, "unit": {"state": "known", "value": "times defender Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}, {"name": "Shock allocation", "value": "equal, odd to top", "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E953"], "reason": null, "gap_ids": []}, "evidence_ids": ["E953"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G953", "G-D953pre"]

G953, `/gaps/2`, bajty [613884,614490), hash `7924b01b3b0ac91dbac0c788b1ec6d730954bca49cca180b5737da725e4c05ba`.

blocking: true

Wyłączenia i niepewności: Per-unit elimination reading is confirmed; real geometry, 6.69/10.22, legal ordering and a shared sole destination remain unresolved.; Legalne heksy retreat i zakres końcowego the unit wymagają kontekstu przy konfliktach.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-041

Dokładny zatwierdzony zakres: ruleofthumb2Romaninfantry sameborderwithexceptions;notfulllegaleligibility;move2IO,1IOifstackedOCgivingorders,1LCifbotheligible

Porównanie: R961: rule of thumb dwóch Roman infantry tego samego border color, z wyjątkami jak Velites. Nie pełne eligibility. Joint move 2 IO; 1 IO tylko z OC w stack dającym rozkazy; 1 LC tylko jeśli obie eligible. Odesłania do charts/line nie zamykają pełnych procedur.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 left, C-9.61-01, bbox [45.0, 176.7, 297.03, 282.7].

> 9.61 See the Stacking Charts for a summary of the legionary
> stacking advantages. For Romans, the rule of thumb is that two
> Roman infantry units of the same border color can stack without
> penalty. There are exceptions, such as Velites. A Roman stack
> may move together when necessary or desired. It takes two In-
> dividual Orders to move two stacked units (only one, if stacked
> with the OC, and he is giving the orders), but only one LC, if they
> are both eligible. Roman infantry units are also allowed spaces
> between them when determining lines; see 4.32.

**first-001** — osobna propozycja/pending:

R961, `/rules/22`, bajty [290602,296910), hash `6b8470e5e55b69e23271008267a8bbe41527657e5a35dcdbfead196e82bce062`.

transcription: {"state": "known", "value": ["There are exceptions, such as Velites."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Consult Stacking Charts for legionary advantages.", "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.", "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.", "Roman infantry may have spaces when determining lines under 4.32."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Consult Stacking Charts for legionary advantages.", "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.", "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.", "Roman infantry may have spaces when determining lines under 4.32."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Velites and other exceptions not enumerated here.", "1 Individual Order with ordering OC stacked; 1 LC if both eligible."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "usual stack", "value": 2, "unit": {"state": "known", "value": "Roman infantry units", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}, {"name": "joint movement", "value": 2, "unit": {"state": "known", "value": "Individual Orders", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}, {"name": "OC-stacked joint movement", "value": 1, "unit": {"state": "known", "value": "Individual Order", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}, {"name": "eligible joint movement", "value": 1, "unit": {"state": "known", "value": "Line Command", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D961stack", "G-D961line"]

**context-01** — osobna propozycja/pending:

R961, `/rules/22`, bajty [361372,367903), hash `bcb032de73b22e12958d3e579d0d9c7a13da82705652c8059b17135e5ec59a74`.

transcription: {"state": "known", "value": ["There are exceptions, such as Velites."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Consult Stacking Charts for legionary advantages.", "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.", "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.", "Roman infantry may have spaces when determining lines under 4.32."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Consult Stacking Charts for legionary advantages.", "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.", "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.", "Roman infantry may have spaces when determining lines under 4.32."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Velites and other exceptions not enumerated here.", "1 Individual Order with ordering OC stacked; 1 LC if both eligible."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "usual stack", "value": 2, "unit": {"state": "known", "value": "Roman infantry units", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}, {"name": "joint movement", "value": 2, "unit": {"state": "known", "value": "Individual Orders", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}, {"name": "OC-stacked joint movement", "value": 1, "unit": {"state": "known", "value": "Individual Order", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}, {"name": "eligible joint movement", "value": 1, "unit": {"state": "known", "value": "Line Command", "evidence_ids": ["E961"], "reason": null, "gap_ids": []}, "evidence_ids": ["E961"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D961stack", "G-D961line"]

Wyłączenia i niepewności: Pełny stacking chart i eligibility nie są dowiedzione regułą thumb.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-042

Dokładny zatwierdzony zakres: combineSize,otherratingsespeciallyTQtop,eachunitowntestusingtopTQ,onlytopfire,bothShock samehex;automaticHitsto each;Shockallocationdelegated8.46Step4/10.13

Porównanie: R962: combine Size, inne ratingi w tym TQ top; własny check każdej z top TQ; tylko top Missile Fire, obie Shock tego samego hex; Automatic Hits do każdej. Shock alokacja delegated 8.46 Step4/10.13. R962 jest niezmieniona; context D962shock dostało endpoint, lecz G-D962shock nadal blocking, dalej brak 6.68 #6. Lokalna reprezentacja nie zamyka alokacji ani nie nadaje TP.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 left, C-9.62-01, bbox [45.0, 290.1, 297.017, 372.1].

> 9.62 Stacked Roman units combine their Size when attacking or
> defending, but all other ratings, especially TQ, are those of the
> top unit. Stacked Romans must Shock attack the same hex; see
> 8.42. Only the top unit may fire. Each unit makes its own TQ
> check but uses the TQ of the top unit. Automatic Cohesion Hits
> (6.68) are applied to each unit in the stack. Cohesion Hits from
> Shock resolution 8.46 Step 4 are allocated per 10.13.

**first-001** — osobna propozycja/pending:

R962, `/rules/23`, bajty [296916,301592), hash `ae11cd4ac05b78d7fd21fa35572b242282d9da3c6d8f9663a0bca89e32363e44`.

transcription: {"state": "known", "value": ["Each unit makes its own TQ check but uses the TQ of the top unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Combined Size on attack/defense; other ratings including TQ from top.", "Stack must Shock attack same hex; only top fires.", "Each unit rolls its own TQ check using top TQ.", "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Stacked Roman units."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combined Size on attack/defense; other ratings including TQ from top.", "Stack must Shock attack same hex; only top fires.", "Each unit rolls its own TQ check using top TQ.", "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D962target", "G-D962auto", "G-D962shock"]

D962shock, `/dependencies/86`, bajty [491159,492109), hash `3c908d4ef58625aa4246c0c74394c38d248d7395d859cbe232853e1f16fd6e84`.

gap_ids: ["G-D962shock"]

impact_if_missing: {"affected_ids": ["R962"], "blocks_full_result": true, "reason": "Base Shock Hit calculation before allocation is not fully supplied; no missing content reconstructed."}

G-D962shock, `/gaps/46`, bajty [551285,551743), hash `feddccd1eae798c1109af40a1131d66402bdffbae6842f125ea7599830635945`.

blocking: true

**context-01** — osobna propozycja/pending:

R962, `/rules/23`, bajty [367910,372751), hash `661e95a04df56028793a45c4b225c06f3a371ebc9314efc42611fd5c3c3a451d`.

transcription: {"state": "known", "value": ["Each unit makes its own TQ check but uses the TQ of the top unit."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Combined Size on attack/defense; other ratings including TQ from top.", "Stack must Shock attack same hex; only top fires.", "Each unit rolls its own TQ check using top TQ.", "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Stacked Roman units."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Combined Size on attack/defense; other ratings including TQ from top.", "Stack must Shock attack same hex; only top fires.", "Each unit rolls its own TQ check using top TQ.", "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."], "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D962target", "G-D962auto", "G-D962shock"]

D962shock, `/dependencies/86`, bajty [568940,569960), hash `4b5a3bf62cbe0d3cc8ae154e79c9b1c2a395320a952179da661102ad74d23c25`.

gap_ids: ["G-D962shock", "GCTX-CRT", "GCTX-applicability"]

impact_if_missing: {"affected_ids": ["R962"], "blocks_full_result": true, "reason": "Fragment supplied, but exact table/selection/order and separate within-stack allocation still block full result."}

G-D962shock, `/gaps/46`, bajty [636395,637341), hash `509a59a82e0105d408795e67884d2c386317392861627fcc47a506f0fef47014`.

blocking: true

Wyłączenia i niepewności: Rozdział 9 nie domyka alokacji Shock Hits; 10.13 jest kontekstem, 6.68 nieprzejrzane.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-043

Dokładny zatwierdzony zakres: differentbordercolors ORsamecolordifferentclasses,+1DRMtoallTQchecks

Porównanie: R963 zachowuje OR: różne border colors lub ten sam color i różne classes. +1 DRM do wszystkich TQ checks, bez zastąpienia OR przez AND. Faktyczne kolory i klasy wymagają danych.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 left, C-9.63-01, bbox [45.0, 379.5, 297.011, 413.5].

> 9.63 For stacked Roman units with different border colors, or of
> the same border color and different classes, there is a +1 DRM
> to all TQ checks.

**first-001** — osobna propozycja/pending:

R963, `/rules/24`, bajty [301598,305296), hash `58a813b6aaba0b0d25a66c3b7a3fd2c3a6bcf811684e8bf617f574c0430f29f8`.

transcription: {"state": "known", "value": ["there is a +1 DRM to all TQ checks."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "+1 DRM to all TQ checks.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Stacked Romans with different border colors OR same border color but different classes."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "+1 DRM to all TQ checks.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "stack TQ modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E963"], "reason": null, "gap_ids": []}, "evidence_ids": ["E963"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D963TQ"]

**context-01** — osobna propozycja/pending:

R963, `/rules/24`, bajty [372758,376599), hash `4fbf3c5ea3e740875782caf600b70a3974f0e7f9ff7bda1b8dea4c9c2261a9ea`.

transcription: {"state": "known", "value": ["there is a +1 DRM to all TQ checks."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "+1 DRM to all TQ checks.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Stacked Romans with different border colors OR same border color but different classes."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "+1 DRM to all TQ checks.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "stack TQ modifier", "value": 1, "unit": {"state": "known", "value": "DRM", "evidence_ids": ["E963"], "reason": null, "gap_ids": []}, "evidence_ids": ["E963"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D963TQ"]

Wyłączenia i niepewności: Typy i kolory muszą być znane z danych jednostek.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-044

Dokładny zatwierdzony zakres: stackorderchangeIOonly,notmovement/LC;facingcanLC;onlytopmovesifmovingoneunitfromstack

Porównanie: R964: zamiana kolejności stack tylko IO, nie część movement ani LC; facing może LC. Przy ruchu jednej jednostki z stacku rusza tylko top. Nie rozszerzono zwykłego unstack na szczególne MLE.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 left, C-9.64-01, bbox [45.0, 420.9, 297.04, 478.9].

> 9.64 Roman Stacking order may be changed/switched only by
> an Individual Order; it may not be part of movement or a Line
> Command, although facing may be changed by LC. If the player
> desires to move only one unit from a stack, only the top unit
> may move.

**first-001** — osobna propozycja/pending:

R964, `/rules/25`, bajty [305302,309224), hash `0011f5a4a5cd234d3f5c62f4b8510d023a26e8b43bc154f1edd2acb291c5b9ea`.

transcription: {"state": "known", "value": ["If the player desires to move only one unit from a stack, only the top unit may move."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Stack order may be switched only by Individual Order, never as movement or LC.", "Facing may change by LC.", "If moving one unit out of stack, only top can move."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Stack order may be switched only by Individual Order, never as movement or LC.", "Facing may change by LC.", "If moving one unit out of stack, only top can move."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Facing may change by LC despite stacking-order LC prohibition."], "reason": null, "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D964order"]

**context-01** — osobna propozycja/pending:

R964, `/rules/25`, bajty [376606,380671), hash `e4530c490edde7d54d4ac9fd06686c4a0312813eb32d7107cf885172e47c8fe8`.

transcription: {"state": "known", "value": ["If the player desires to move only one unit from a stack, only the top unit may move."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Stack order may be switched only by Individual Order, never as movement or LC.", "Facing may change by LC.", "If moving one unit out of stack, only top can move."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["Stack order may be switched only by Individual Order, never as movement or LC.", "Facing may change by LC.", "If moving one unit out of stack, only top can move."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Facing may change by LC despite stacking-order LC prohibition."], "reason": null, "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: ["G-D964order"]

Wyłączenia i niepewności: Nie zastosować zwykłego unstack do MLE bez sprawdzenia szczególnej reguły.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-045

Dokładny zatwierdzony zakres: Romaninfantryfacing1MPanynumbervertices;notMLEfacingrule

Porównanie: R965: Roman infantry 1 MP za facing dowolnej liczby vertices, nie koszt za każdy vertex. Nie przeniesiono tej operacji na MLE, które zachowuje facing.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 left, C-9.65-01, bbox [45.0, 486.3, 297.1, 508.3].

> 9.65 Roman infantry pay 1 MP cost for changing facing, but,
> unlike most other units, they may change any number of vertices.

**first-001** — osobna propozycja/pending:

R965, `/rules/26`, bajty [309230,312838), hash `e38853213823da0429d224631ca49efed539fcf423497ce1ab8828e28f8fc77a`.

transcription: {"state": "known", "value": ["Roman infantry pay 1 MP cost for changing facing, but, unlike most other units, they may change any number of vertices."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Roman infantry change facing through any number of vertices for 1 MP.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Roman infantry change facing through any number of vertices for 1 MP.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing change", "value": 1, "unit": {"state": "known", "value": "MP for any number of vertices", "evidence_ids": ["E965"], "reason": null, "gap_ids": []}, "evidence_ids": ["E965"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: []

**context-01** — osobna propozycja/pending:

R965, `/rules/26`, bajty [380678,384416), hash `19ae59d6e959efb3e6c037af8605714eddab51c425881ad764356addf2f199d3`.

transcription: {"state": "known", "value": ["Roman infantry pay 1 MP cost for changing facing, but, unlike most other units, they may change any number of vertices."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Roman infantry change facing through any number of vertices for 1 MP.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": "Roman infantry change facing through any number of vertices for 1 MP.", "reason": null, "gap_ids": []}

exceptions: {"state": "established_absent", "value": [], "reason": "No exception stated within this identified clause; external rules may qualify it.", "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "facing change", "value": 1, "unit": {"state": "known", "value": "MP for any number of vertices", "evidence_ids": ["E965"], "reason": null, "gap_ids": []}, "evidence_ids": ["E965"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: []

Wyłączenia i niepewności: Nie rozszerzać tej wartości na MLE, które zachowuje facing.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-046

Dokładny zatwierdzony zakres: topunits instackssameLine sideways tovacantflankClearoutsideenemyZOC,facingunchanged;unstackonly,notstackingTogether;diagramOriginaltop/Afterbottomillustrative

Porównanie: R966: top units w stackach tej samej Line, sideways do vacant flank; Clear i poza enemy ZOC, facing bez zmiany; wyłącznie unstack, nie stacking together. N966diagram zachowuje Original Deployment u góry, After MLE u dołu jako ilustrację. Nie akceptujemy małych ratingów, identyfikacji front/back konkretnych counterów ani ogólnego prawa do dowolnej strony z samej grafiki.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 left, C-9.66-01-S1, bbox [44.997, 678.9, 297.009, 736.9].

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal.

Źródło PDF 35 right, C-9.66-01-S1, bbox [314.997, 54.01, 567.03, 124.01].

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal.

Źródło PDF 35 left, C-9.66-01-S2, bbox [44.997, 678.9, 297.009, 736.9].

> To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)
> may move sideways into the vacant flank hexes (see the diagram
> above).

Źródło PDF 35 right, C-9.66-01-S2, bbox [314.997, 54.01, 567.03, 124.01].

> To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)
> may move sideways into the vacant flank hexes (see the diagram
> above).

Źródło PDF 35 left, C-9.66-01-S3, bbox [44.997, 678.9, 297.009, 736.9].

> If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex.

Źródło PDF 35 right, C-9.66-01-S3, bbox [314.997, 54.01, 567.03, 124.01].

> If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex.

Źródło PDF 35 left, C-9.66-01-S4, bbox [44.997, 678.9, 297.009, 736.9].

> The hex entered by MLE must be Clear and
> not in an enemy ZOC.

Źródło PDF 35 right, C-9.66-01-S4, bbox [314.997, 54.01, 567.03, 124.01].

> The hex entered by MLE must be Clear and
> not in an enemy ZOC.

Źródło PDF 35 left, C-9.66-01-S5, bbox [44.997, 678.9, 297.009, 736.9].

> Facing remains the same.

Źródło PDF 35 right, C-9.66-01-S5, bbox [314.997, 54.01, 567.03, 124.01].

> Facing remains the same.

Źródło PDF 35 left, C-9.66-01-S6, bbox [44.997, 678.9, 297.009, 736.9].

> This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35 right, C-9.66-01-S6, bbox [314.997, 54.01, 567.03, 124.01].

> This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35 left, D-02, bbox [80, 516, 266, 674].

> [graphic evidence; no literal text field]

Źródło PDF 35 left, CAP-01, bbox [128.368, 579.9, 213.638, 589.9].

> Original Deployment

Źródło PDF 35 left, CAP-02, bbox [107.257, 661.5, 234.757, 671.5].

> After Manipular Line Extension

**first-001** — osobna propozycja/pending:

N966diagram, `/nodes/7`, bajty [128977,130323), hash `f5c32b1dae24067c8069c9f6a259e1da4cd473f61255ce80b5b070a71cc69689`.

content: {"state": "known", "value": {"transcription": {"captions": ["Original Deployment", "After Manipular Line Extension"], "top_panel": "Two separated stacks; curved arrows point sideways right into adjacent empty hexes.", "bottom_panel": "Four single counters in adjacent hexes, labeled I a, I b, I c, I d.", "counter_text": ["HA", "J", "3", "LG", "7", "5"]}, "interpretation": "Illustration shows unstacking each top unit into vacant side hex, preserving facing. Numeric counter ratings are illustrative and are not general Roman unit parameters."}, "reason": null, "gap_ids": []}

R966, `/rules/27`, bajty [312844,317525), hash `2e7a501a9a282ca4841068af720073ea84aba9cb1de2d3ccd280e3a2103302a6`.

transcription: {"state": "known", "value": ["all the top units in the stacks in the same Line (see 4.32)", "The hex entered by MLE must be Clear and not in an enemy ZOC."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.", "Facing unchanged.", "Applies only to unstacking; cannot stack units by MLE."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Stacked Romans in same Line; unoccupied Flank hexes.", "Entered hex Clear and outside enemy ZOC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.", "Facing unchanged.", "Applies only to unstacking; cannot stack units by MLE."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Occupied Flank hex cannot receive MLE.", "Does not apply to stacking together."], "reason": null, "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "known", "value": ["LC or reaction to enemy movement."], "reason": null, "gap_ids": []}

gap_ids: ["G-D966line", "G-D-ZOC-R966"]

**context-01** — osobna propozycja/pending:

N966diagram, `/nodes/7`, bajty [177283,178673), hash `36e8f4cd62347156e4d08983cd3b50a484a73b8478deddb5b4167d954c4d364d`.

content: {"state": "known", "value": {"transcription": {"captions": ["Original Deployment", "After Manipular Line Extension"], "top_panel": "Two separated stacks; curved arrows point sideways right into adjacent empty hexes.", "bottom_panel": "Four single counters in adjacent hexes, labeled I a, I b, I c, I d.", "counter_text": ["HA", "J", "3", "LG", "7", "5"]}, "interpretation": "Illustration shows unstacking each top unit into vacant side hex, preserving facing. Numeric counter ratings are illustrative and are not general Roman unit parameters."}, "reason": null, "gap_ids": []}

R966, `/rules/27`, bajty [384423,389278), hash `2c3df78a88652b14a70895ae92c0bb0cf0a15d34596c536e9f59a05f1c63c10e`.

transcription: {"state": "known", "value": ["all the top units in the stacks in the same Line (see 4.32)", "The hex entered by MLE must be Clear and not in an enemy ZOC."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.", "Facing unchanged.", "Applies only to unstacking; cannot stack units by MLE."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Stacked Romans in same Line; unoccupied Flank hexes.", "Entered hex Clear and outside enemy ZOC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.", "Facing unchanged.", "Applies only to unstacking; cannot stack units by MLE."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Occupied Flank hex cannot receive MLE.", "Does not apply to stacking together."], "reason": null, "gap_ids": []}

parameters: {"state": "established_absent", "value": [], "reason": "No numerical parameter stated within this identified clause.", "gap_ids": []}

time_limits: {"state": "known", "value": ["LC or reaction to enemy movement."], "reason": null, "gap_ids": []}

gap_ids: ["G-D966line", "G-D-ZOC-R966"]

Wyłączenia i niepewności: Same Line przez4.32, Clear i ZOC wymagają danych/procedur; grafika nie daje ogólnego prawa do dowolnej strony.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-047

Dokładny zatwierdzony zakres: reactiontriggerenemycombatwithin2hexes,line;maydeclinefirstopportunitywithoutlosinglatertriggers;OW/MLEdifferentunitscanwithvalidtriggers,sameunitscannotboth

Porównanie: R967: reakcja w instant approach enemy combat within 2 hexes of stacked Roman line; wolno odroczyć pierwszą okazję do następnego kwalifikowanego triggeru. OW/MLE razem tylko przez różne jednostki z właściwymi triggerami, nie te same. N967ex zachowuje przykład Velites OW i Hastati MLE.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 right, C-9.67-01, bbox [314.997, 131.41, 567.05, 225.41].

> 9.67 Manipular Line Extension may be undertaken as a reaction
> to enemy movement the instant an enemy combat unit comes
> within 2 hexes of a line of stacked Roman units. The Roman
> player may make his choice at any time any enemy unit so places
> itself (that is, he does not have to exercise his MLE rights the first
> time they become available). If enemy movement triggers both
> Orderly Withdrawal as well as MLE, both may be undertaken
> together but not by the same units.

Źródło PDF 35 right, X-07, bbox [314.997, 232.81, 567.013, 278.81].

> EXAMPLE: A Velites unit sitting between two Hastati stacks may
> withdraw through the gaps in a Hastati line upon approach of,
> say, an enemy Phalanx and, as soon as that unit is through the
> gap, the Hastati line may undergo MLE.

**first-001** — osobna propozycja/pending:

N967ex, `/nodes/8`, bajty [130329,131266), hash `e2e9a2dcba7c2946ba1d54d93b45bacb6ff8a8e47c5af7e1e088c2c856fcbb15`.

content: {"state": "known", "value": {"transcription": "A Velites unit sitting between two Hastati stacks may withdraw through the gaps in a Hastati line upon approach of, say, an enemy Phalanx and, as soon as that unit is through the gap, the Hastati line may undergo MLE.", "interpretation": "Different units withdraw and extend, illustrating permitted coexistence."}, "reason": null, "gap_ids": []}

R967, `/rules/28`, bajty [317531,321925), hash `8aba3115f33776d806a6a196be0cae710b2eea2eef13c04318a89102b3d53fcc`.

transcription: {"state": "known", "value": ["both may be undertaken together but not by the same units."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["May react with MLE instantly, at any qualifying approach; need not take first opportunity.", "If movement triggers both OW and MLE, both may occur together using different units."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Enemy combat unit comes within 2 hexes of stacked Roman line."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["May react with MLE instantly, at any qualifying approach; need not take first opportunity.", "If movement triggers both OW and MLE, both may occur together using different units."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Same units cannot perform both OW and MLE."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "MLE trigger distance", "value": "within 2", "unit": {"state": "known", "value": "hexes", "evidence_ids": ["E967"], "reason": null, "gap_ids": []}, "evidence_ids": ["E967"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Instant of qualifying enemy movement; choice may be deferred to later qualifying approach."], "reason": null, "gap_ids": []}

gap_ids: ["G-D967OW"]

**context-01** — osobna propozycja/pending:

N967ex, `/nodes/8`, bajty [178680,179647), hash `6c9efe1728ad06ece3b7d45cd71e78dd02c715ae518ebbee8f2841bd7e8fdc26`.

content: {"state": "known", "value": {"transcription": "A Velites unit sitting between two Hastati stacks may withdraw through the gaps in a Hastati line upon approach of, say, an enemy Phalanx and, as soon as that unit is through the gap, the Hastati line may undergo MLE.", "interpretation": "Different units withdraw and extend, illustrating permitted coexistence."}, "reason": null, "gap_ids": []}

R967, `/rules/28`, bajty [389285,393844), hash `e9376d25c08d2ed7bc27163917fcc5b9fc9ec4de5df11c2c309c7a92e2ef5755`.

transcription: {"state": "known", "value": ["both may be undertaken together but not by the same units."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["May react with MLE instantly, at any qualifying approach; need not take first opportunity.", "If movement triggers both OW and MLE, both may occur together using different units."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Enemy combat unit comes within 2 hexes of stacked Roman line."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["May react with MLE instantly, at any qualifying approach; need not take first opportunity.", "If movement triggers both OW and MLE, both may occur together using different units."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Same units cannot perform both OW and MLE."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "MLE trigger distance", "value": "within 2", "unit": {"state": "known", "value": "hexes", "evidence_ids": ["E967"], "reason": null, "gap_ids": []}, "evidence_ids": ["E967"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Instant of qualifying enemy movement; choice may be deferred to later qualifying approach."], "reason": null, "gap_ids": []}

gap_ids: ["G-D967OW"]

Wyłączenia i niepewności: OW i legalność line muszą być ustalone oddzielnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-048

Dokładny zatwierdzony zakres: activeMLELC-only,bothunitsmaymoveafterwithMA-2,noCHforMLE;ColumnunitsnoMLE;noautomatictransferofLCpostmovepermissiontoreaction

Porównanie: R968 wyraźnie kwalifikuje post-MLE move przez When by LC: obie jednostki mogą ruszyć z MA-2. LC-only dla aktywnego MLE, 0 CH za samo MLE i zakaz Column. Nie przeniesiono uprawnienia dalszego ruchu na tryb reakcyjny R967.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 right, C-9.68-01, bbox [314.997, 286.21, 567.012, 344.21].

> 9.68 Manipular Line Extension may also be undertaken as part
> of a Line Command (only). If undertaken as an LC, both units
> may move after the MLE but with their MA reduced by 2. There
> are no Cohesion Hits applied for the MLE. Units in Column may
> not use MLE.

**first-001** — osobna propozycja/pending:

R968, `/rules/29`, bajty [321931,326799), hash `4b8130db1b3f0bfe4d6e9ea3c3c7f8bcbb8db3d078654f49c01ad8a85db297bb`.

transcription: {"state": "known", "value": ["There are no Cohesion Hits applied for the MLE."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["MLE may also be part of LC only.", "When by LC, both units may then move at MA reduced by 2.", "No Hits for MLE; Column units cannot MLE."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["MLE may also be part of LC only.", "When by LC, both units may then move at MA reduced by 2.", "No Hits for MLE; Column units cannot MLE."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Units in Column excluded."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "post-LC-MLE MA adjustment", "value": -2, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E968"], "reason": null, "gap_ids": []}, "evidence_ids": ["E968"]}, {"name": "MLE Cohesion cost", "value": 0, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E968"], "reason": null, "gap_ids": []}, "evidence_ids": ["E968"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["After MLE in LC both units may move."], "reason": null, "gap_ids": []}

gap_ids: ["G-D968LC", "G-D968column"]

**context-01** — osobna propozycja/pending:

R968, `/rules/29`, bajty [393851,398910), hash `8b4bf17469c5987e914879bec985cb90bb189d32fa5e9a15e1e560fcf66722a1`.

transcription: {"state": "known", "value": ["There are no Cohesion Hits applied for the MLE."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["MLE may also be part of LC only.", "When by LC, both units may then move at MA reduced by 2.", "No Hits for MLE; Column units cannot MLE."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "established_absent", "value": [], "reason": "No additional prerequisite stated in this identified clause.", "gap_ids": []}

action_effect: {"state": "known", "value": ["MLE may also be part of LC only.", "When by LC, both units may then move at MA reduced by 2.", "No Hits for MLE; Column units cannot MLE."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Units in Column excluded."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "post-LC-MLE MA adjustment", "value": -2, "unit": {"state": "known", "value": "MA", "evidence_ids": ["E968"], "reason": null, "gap_ids": []}, "evidence_ids": ["E968"]}, {"name": "MLE Cohesion cost", "value": 0, "unit": {"state": "known", "value": "Cohesion Hits", "evidence_ids": ["E968"], "reason": null, "gap_ids": []}, "evidence_ids": ["E968"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["After MLE in LC both units may move."], "reason": null, "gap_ids": []}

gap_ids: ["G-D968LC", "G-D968column"]

Wyłączenia i niepewności: Nie przenosić automatycznie post-MLE ruchu na tryb reakcyjny.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-049

Dokładny zatwierdzony zakres: Romansprior200BCE,ScipioAfricanusnotOC;Cannaeexplicitusepergameinstruction,notnewhistoricalinference;C9.7S2explanatory

Porównanie: R97intro: obowiązek dla Romans przed 200 BCE i bez Scipio Africanus jako OC; Cannae jawnie objęte instrukcją gry, nie historycznym wnioskowaniem. Parametr jest prior to 200, nie <=200. Explanatory C9.7-S2 nie stanowi dodatkowego obowiązku.

Propozycja: `supported_local_scope`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 right, C-9.7-01-S1, bbox [315.0, 370.173, 567.015, 440.173].

> This rule must be used with any battle involving Romans that took
> place prior to 200 BCE in which Scipio Africanus is not pres-
> ent as Overall Commander (and, yes, even though, historically,
> Scipio was at Cannae, for game purposes he wasn’t, so use it at
> Cannae).

**first-001** — osobna propozycja/pending:

R97intro, `/rules/30`, bajty [326805,330943), hash `640110048218e02f57f9aa8bdca2bd334ae950abe580344d8bfe03f9663b5001`.

transcription: {"state": "known", "value": ["so use it at Cannae"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Scipio Africanus as OC excludes the stated mandatory applicability."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "date cutoff", "value": "prior to 200", "unit": {"state": "known", "value": "BCE", "evidence_ids": ["E97intro"], "reason": null, "gap_ids": []}, "evidence_ids": ["E97intro"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: []

**context-01** — osobna propozycja/pending:

R97intro, `/rules/30`, bajty [398917,403202), hash `e89bbba15ff240518389e505e94aa7d9a023816ca59d362b60b3a7c6e8b29516`.

transcription: {"state": "known", "value": ["so use it at Cannae"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Scipio Africanus as OC excludes the stated mandatory applicability."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "date cutoff", "value": "prior to 200", "unit": {"state": "known", "value": "BCE", "evidence_ids": ["E97intro"], "reason": null, "gap_ids": []}, "evidence_ids": ["E97intro"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: []

Wyłączenia i niepewności: W realnym scenariuszu data i tożsamość OC wymagają dowodów.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-050

Dokładny zatwierdzony zakres: realbattlewithoutdate/OC/AWL notresolved,requires_context

Porównanie: Obie odpowiedzi podają predykaty daty/OC i warunki Triarii, nie rzeczywiste dane wybranej bitwy. AWL/RP/LOS/ZOC mają jawne blocking gaps; brak osobnych deklaracji źródła rzeczywistej daty i OC w R97intro.gap_ids (pusta lista). SEM-010: wystarczalność tego opisu needs-context wymaga właściciela. Nie jest to dowód fikcyjnego wybrania dowódcy/daty; known na conditions oznacza znany warunek, nie spełniony fakt. Nie oceniono SIT.

Propozycja: `partial_context_declaration_pending`; decyzja właściciela pending dla obu hashów.

Źródło PDF 35 right, C-9.7-01-S1, bbox [315.0, 370.173, 567.015, 440.173].

> This rule must be used with any battle involving Romans that took
> place prior to 200 BCE in which Scipio Africanus is not pres-
> ent as Overall Commander (and, yes, even though, historically,
> Scipio was at Cannae, for game purposes he wasn’t, so use it at
> Cannae).

Źródło PDF 35 right, C-9.71-01, bbox [315.0, 447.573, 567.0, 469.573].

> 9.71 Triarii units cannot move, but may change facing, until and
> unless one of the following occurs:

Źródło PDF 35 right, C-9.72-01, bbox [315.0, 553.113, 567.008, 611.113].

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

**first-001** — osobna propozycja/pending:

R971, `/rules/31`, bajty [330949,335849), hash `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.

transcription: {"state": "known", "value": ["Triarii units cannot move, but may change facing, until and unless one of the following occurs:"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Elephants excluded from proximity trigger.", "Allied infantry excluded from separation test.", "Facing permitted before release."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "enemy proximity", "value": "within 3", "unit": {"state": "known", "value": "hexes AND LOS", "evidence_ids": ["E971"], "reason": null, "gap_ids": []}, "evidence_ids": ["E971"]}, {"name": "separation", "value": ">=6", "unit": {"state": "known", "value": "hexes from all other Roman/Ala infantry lines", "evidence_ids": ["E971"], "reason": null, "gap_ids": []}, "evidence_ids": ["E971"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Until and unless either trigger occurs."], "reason": null, "gap_ids": []}

gap_ids: ["G-D971LOS"]

R972, `/rules/32`, bajty [335855,339867), hash `f304ccb85a653664ddb287c3e591dd67a2744b35cf4210ace71592b684436f5b`.

transcription: {"state": "known", "value": ["They may always, however, Shock attack (without moving) against enemy units in their ZOC."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Triarii cannot move and Shock attack until Rout Point threshold reached.", "Always may stationary Shock enemy in their ZOC."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Triarii cannot move and Shock attack until Rout Point threshold reached.", "Always may stationary Shock enemy in their ZOC."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Stationary Shock against enemy in own ZOC always permitted."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Rout Point threshold", "value": ">= floor(Army Withdrawal Level / 2)", "unit": {"state": "known", "value": "Rout Points", "evidence_ids": ["E972"], "reason": null, "gap_ids": []}, "evidence_ids": ["E972"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Until Rout Point threshold; stationary Shock always allowed."], "reason": null, "gap_ids": []}

gap_ids: ["G-D972AWL", "G-D972RP", "G-D-ZOC-R972"]

R97intro, `/rules/30`, bajty [326805,330943), hash `640110048218e02f57f9aa8bdca2bd334ae950abe580344d8bfe03f9663b5001`.

transcription: {"state": "known", "value": ["so use it at Cannae"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Scipio Africanus as OC excludes the stated mandatory applicability."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "date cutoff", "value": "prior to 200", "unit": {"state": "known", "value": "BCE", "evidence_ids": ["E97intro"], "reason": null, "gap_ids": []}, "evidence_ids": ["E97intro"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: []

G-D972AWL, `/gaps/54`, bajty [555028,555502), hash `7b2a49345eb5abfd06e09555c1a797ca2d0960cac20429a52f04434614135c9c`.

blocking: true

G-D972RP, `/gaps/55`, bajty [555508,555991), hash `ecd85583d0a2f8ae358a010ae1bdbd73965717a64fd61fa126755e49e065078c`.

blocking: true

**context-01** — osobna propozycja/pending:

R971, `/rules/31`, bajty [403209,408288), hash `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.

transcription: {"state": "known", "value": ["Triarii units cannot move, but may change facing, until and unless one of the following occurs:"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Elephants excluded from proximity trigger.", "Allied infantry excluded from separation test.", "Facing permitted before release."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "enemy proximity", "value": "within 3", "unit": {"state": "known", "value": "hexes AND LOS", "evidence_ids": ["E971"], "reason": null, "gap_ids": []}, "evidence_ids": ["E971"]}, {"name": "separation", "value": ">=6", "unit": {"state": "known", "value": "hexes from all other Roman/Ala infantry lines", "evidence_ids": ["E971"], "reason": null, "gap_ids": []}, "evidence_ids": ["E971"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Until and unless either trigger occurs."], "reason": null, "gap_ids": []}

gap_ids: ["G-D971LOS"]

R972, `/rules/32`, bajty [408295,412460), hash `efc3e461afcdf47ef5fafdc90f3c9223badabf8597ff20dc3ef7807de8842bde`.

transcription: {"state": "known", "value": ["They may always, however, Shock attack (without moving) against enemy units in their ZOC."], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": ["Triarii cannot move and Shock attack until Rout Point threshold reached.", "Always may stationary Shock enemy in their ZOC."], "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": ["Triarii cannot move and Shock attack until Rout Point threshold reached.", "Always may stationary Shock enemy in their ZOC."], "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Stationary Shock against enemy in own ZOC always permitted."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "Rout Point threshold", "value": ">= floor(Army Withdrawal Level / 2)", "unit": {"state": "known", "value": "Rout Points", "evidence_ids": ["E972"], "reason": null, "gap_ids": []}, "evidence_ids": ["E972"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "known", "value": ["Until Rout Point threshold; stationary Shock always allowed."], "reason": null, "gap_ids": []}

gap_ids: ["G-D972AWL", "G-D972RP", "G-D-ZOC-R972"]

R97intro, `/rules/30`, bajty [398917,403202), hash `e89bbba15ff240518389e505e94aa7d9a023816ca59d362b60b3a7c6e8b29516`.

transcription: {"state": "known", "value": ["so use it at Cannae"], "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.", "gap_ids": []}

interpretation: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": "Interpretation confined to supplied source; no external procedures reconstructed.", "gap_ids": []}

conditions: {"state": "known", "value": ["Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."], "reason": null, "gap_ids": []}

action_effect: {"state": "known", "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.", "reason": null, "gap_ids": []}

exceptions: {"state": "known", "value": ["Scipio Africanus as OC excludes the stated mandatory applicability."], "reason": null, "gap_ids": []}

parameters: {"state": "known", "value": [{"name": "date cutoff", "value": "prior to 200", "unit": {"state": "known", "value": "BCE", "evidence_ids": ["E97intro"], "reason": null, "gap_ids": []}, "evidence_ids": ["E97intro"]}], "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.", "gap_ids": []}

time_limits: {"state": "not_applicable", "value": null, "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.", "gap_ids": []}

gap_ids: []

G-D972AWL, `/gaps/54`, bajty [640754,641245), hash `4501dab342ed343a618bfbff3bc2c2a58e0037d4bb0ec51b1ce768d66008b659`.

blocking: true

G-D972RP, `/gaps/55`, bajty [641252,641752), hash `f55d0cda36ede2f89e9a06f65931deb0783be55f592e897fdf842846f390abca`.

blocking: true

Wyłączenia i niepewności: Actual battle date, Overall Commander, AWL and scenario facts are required.; Konkretny scenariusz, OC, AWL/RP i stan mapy.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

## Zachowane granice

SEM-002 i SEM-003 nadal pending. Akceptacja lokalnego pół/floor w EXP-030 nie akceptuje całej R932, nowego Routed/AS wyjątku, kolejności lub relacji; akceptacja wymagania źródła w EXP-031 nie rozstrzyga operators/result.

R962 lokalna delegacja nie domyka pełnej alokacji. Nowa ścieżka trzech krawędzi kończy się na brakującym 6.68 #6; stop rozszerzania na granicy 2 zachowany, brak certyfikatu całego grafu.

Krytyczny brak źródła blokuje odpowiedni pełny wynik. Znane operatory/warunki z zadanymi faktami nie są automatycznie blokowane brakiem całego setupu. 20 sytuacji nie oceniono.

R966diagram: sprawdzono tekst warunków oraz orientację Original/After panels. Nie certyfikowano tiny ratings, tożsamości counterów w obu panelach lub wszystkich granic glifów. E916 i 64 granice nadal otwarte.

Źródła, odpowiedzi, eval-v1 i wcześniejsze pakiety/raporty zachowane. 0 nowych ekstrakcji, kontekstu i korekt. Historyczne izolacja/ekspozycja i selektory/czasy/tokeny/cena/aktywny budżet nadal unknown. M-POC5A partial.
