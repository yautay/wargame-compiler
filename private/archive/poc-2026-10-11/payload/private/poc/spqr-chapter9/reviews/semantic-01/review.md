# M-POC5A.1 — porównanie znaczenia obu wyników

Stan: partial / waiting_review. Oceniający przygotował rejestr; właściciel nie nadał jeszcze akceptacji żadnemu zakresowi obu odpowiedzi.

eval-v1: `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`.

first-001: 617941 bajtów, SHA-256 `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.
context-01: 712014 bajtów, SHA-256 `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

Podział przed oceną: .1 integralność/rejestr/pierwsze rozbieżności; .2 EXP-001–025; .3 EXP-026–050; .4 EXP-051–074, pozostały inwentarz, wszystkie relacje i lokatory. Wszystkie części do 90 minut; bez pominięć pending.

Pełne zakresy źródłowe, pola obu wyników, JSON pointers i dokładne bajty znajdują się w [checklist.json](checklist.json). Rejestr zawiera 74 porównania, 207 pozycji, wszystkie rubryki i wszystkie krawędzie; to przygotowanie dowodów, nie 74/207 wykonanych ocen.

## Pierwszy zakres pokazany do przeglądu

### SEM-001

Oba wyniki zachowują warunek DR>TQ i minimum 1, ale R916.interpretation=unknown/G916.blocking pozostawia DR<=TQ nierozstrzygnięte. Proponowane niepełne odtworzenie zatwierdzonej lokalnej gałęzi 0 CH i nieuzasadniona blokada tej gałęzi; nie jest to dowód błędnego odczytu ani twierdzenia o zawsze 1 CH.

Granice: Nie obejmuje pełnego OW, rzeczywistego TQ ani całej EXP-016. E916 ma osobny błąd lokatora.

Propozycja oceniającego Codex; decyzja właściciela pending.

### SEM-002

Oba wyniki podają both rout/separate hexes, lecz deklarują nierozstrzygnięty zakres eliminacji. Eval-v1 przyjmuje eliminację każdej PH osobno, z możliwością legalnego Rout drugiej. Proponowana niepełna lokalna interpretacja; sprawdzić osobno, czy podstawa wcześniejszej decyzji była dostępna ekstraktorowi.

Granice: Nie oceniać rzeczywistej geometrii, kolejności, wspólnego jedynego celu, 6.69/10.22 ani D1. Nie przenosić braków setupu na syntetyczne dane.

Propozycja oceniającego Codex; decyzja właściciela pending.

### SEM-003

first-001 ma lokalne pół/floor i literalny przykład, bez rozstrzygnięcia AS. context-01 dodaje udokumentowane 2x wyniku obrońcy przy AS, warunkowe pół/floor dla LC, wyjątek Routed i kumulatywność. Proponowane poprawne częściowe podparcie operatorów; pełna kolejność, zaokrąglenie, applicability i wynik pozostają nierozstrzygnięte.

Granice: Zakres LC użytego w determination (8.45), tylko wymienione klasy obrońcy; nie dopisywać automatycznego znoszenia 2x i pół ani nowego gold dla EXP-031.

Propozycja oceniającego Codex; decyzja właściciela pending.

### SEM-004

9.23 mówi o Hits zadanych przez SK; Step 4 #3 mówi o Hits atakującego, gdy obrońcą jest SK. Nowa niejawna relacja R923->NCTX846S4 jest kandydatem uzasadnienia strony/faktora/floor/cap, wymaga osobnej decyzji o konieczności i rodzaju. Nie jest pewnym TP ani FP.

Granice: Nie domyka doboru mieszanego obrońcy/Size/CRT i nie zwiększa gold 3 relacji niejawnych.

Propozycja oceniającego Codex; decyzja właściciela pending.

### SEM-005

Dawny potwierdzony błąd: bbox E916 urywa wyjątek Leader Elephant. Pełny obraz obejmuje wyjątek, ale oryginalnego lokatora nie naprawiono.

Granice: Błąd dowodu nie jest automatycznie błędną transkrypcją lub interpretacją.

Propozycja oceniającego Codex; decyzja właściciela pending.

### SEM-006

Oba wyniki nadal nie mają 3 krytycznych osobnych par niejawnych DEP-NEW-001/002/003 i 4 osobnych wzmianek DEP-034/035/043/067-1. To obserwacje strukturalne; semantyczne FN i treść w prozie oceniane osobno.

Granice: DEP-NEW-001: R972->R971 condition; 002: N914table->R914 exception; 003: R986->R914 condition, wszystkie implicit. D961stack/DEP-037 różnica rodzaju pending.

Propozycja oceniającego Codex; decyzja właściciela pending.

### SEM-007

58 dawnych i 6 nowych granic glifów wymagają dokładnego review. Oględziny trzech pełnych regionów w tej części nie potwierdzają wszystkich bbox.

Granice: 111 cytatów i valid geometry nie certyfikują pełnych transkrypcji ani małych wartości.

Propozycja oceniającego Codex; decyzja właściciela pending.

### SEM-008

Nowa połączona ścieżka kończy się na brakującym 6.68 bullet #6 po 3 krawędziach. Nie pozyskano źródła trzeciego kroku; pełne zależne wyniki blocked_source.

Granice: Stop rozszerzania na granicy 2; nie deklarować zgodności całego grafu ani aktywnego czasu.

Propozycja oceniającego Codex; decyzja właściciela pending.

## Oczekiwania — pełny zakres do review

### EXP-001 — M-POC5A.2

Dokładny zatwierdzony zakres: In the reviewed supplied case, Pass-Thru is allowed with LI defending Front, EL marker, no co-attacker, no initial enemy ZOC, a free Rear and an early decision. Initial enemy ZOC excludes it despite later exit. With two defenders both must meet the earlier conditions.

Wyłączenia/niepewności: Pełny Shock i definicje Front/Rear/ZOC są celami zewnętrznymi; nie wyliczać ich z tego akapitu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 31, right, C-9.11-01, bbox [315.0, 481.4, 567.042, 563.4]; dokładny source_span: null.

> 9.11 Elephant Pass-Thru: An infantry unit being
> attacked through one of its Front hexes by an Ele-
> phant unit marked SHOCK MUST CHECK TQ, may
> attempt to allow the Elephant unit to pass through its
> hex. This decision must be made prior to the Pre-Shock TQ Check
> die roll (8.43) and may be elected only if at least one of the de-
> fender’s Rear hexes is unoccupied. Pass-Thru is not allowed if:

Źródło PDF 31, right, C-9.11-02, bbox [315.0, 568.28, 530.611, 578.28]; dokładny source_span: null.

> • an infantry unit is attacked through a Flank or Rear.

Źródło PDF 31, right, C-9.11-03, bbox [315.0, 581.72, 530.38, 591.72]; dokładny source_span: null.

> • an Elephant unit is attacking along with other units.

Źródło PDF 31, right, C-9.11-04, bbox [315.0, 595.16, 567.07, 617.16]; dokładny source_span: null.

> • the infantry unit was in an enemy ZOC at the start of the Orders
> Phase.

Źródło PDF 31, right, C-9.11-05, bbox [315.0, 624.38, 567.018, 658.38]; dokładny source_span: null.

> Pass-Thru may be used by two defending infantry units if both
> units meet the preceding conditions. If the player decides against
> Pass-Thru, Shock proceeds normally.

**first-001 — pending / not_assessable**. Kandydaci: R911; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [171012, 179988); hash zakresu `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D-ZOC-R911

**context-01 — pending / not_assessable**. Kandydaci: R911; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [236824, 246111); hash zakresu `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D-ZOC-R911

### EXP-002 — M-POC5A.2

Dokładny zatwierdzony zakres: For the reviewed supplied Pass-Thru result, defender Pre-Shock +1 DRM; infantry Hits 5 become 2 and EL Hits 3 become 2. Base-0 reduction floor and other modifier order remain unresolved.

Wyłączenia/niepewności: Base EL Hits=0 reduction floor/order remains unresolved; do not infer a negative result or minimum.; Bazowy wynik Shock musi być dostarczony; kolejność innych modyfikatorów i dolna granica redukcji EL do przeglądu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 31, right, C-9.11-07, bbox [315.0, 680.66, 567.005, 702.66]; dokładny source_span: null.

> 1. Apply a +1 DRM to the infantry unit’s Pre-Shock TQ Check
> DR.

Źródło PDF 31, right, C-9.11-08, bbox [315.0, 706.82, 567.12, 740.82]; dokładny source_span: null.

> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

**first-001 — pending / not_assessable**. Kandydaci: R911; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [171012, 179988); hash zakresu `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D-ZOC-R911

**context-01 — pending / not_assessable**. Kandydaci: R911; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [236824, 246111); hash zakresu `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D-ZOC-R911

### EXP-003 — M-POC5A.2

Dokładny zatwierdzony zakres: After supplied no-infantry-Rout and no-EL-Rampage outcomes, place EL in a free defender Rear hex chosen by the EL player, keeping facing. No complete Shock result inferred.

Wyłączenia/niepewności: Stan Rout wymaga procedury ogólnej; Rampage ma wewnętrzny cel R-9.14.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, left, C-9.11-09, bbox [45.0, 54.004, 297.084, 100.004]; dokładny source_span: null.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.

**first-001 — pending / not_assessable**. Kandydaci: R911; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [171012, 179988); hash zakresu `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D-ZOC-R911

**context-01 — pending / not_assessable**. Kandydaci: R911; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [236824, 246111); hash zakresu `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D-ZOC-R911

### EXP-004 — M-POC5A.2

Dokładny zatwierdzony zakres: The final Pass-Thru TQ check is separate from Pre-Shock; SK are exempt from that final check. For non-SK, positive DR-TQ gives Hits; DR<=TQ gives no excess. No minimum imported from 9.16.

Wyłączenia/niepewności: Nie rozszerzać wyjątku na wszystkie testy TQ.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, left, C-9.11-10, bbox [45.0, 104.164, 297.0, 150.164]; dokładny source_span: null.

> 4. The defending unit, other than a Skirmisher unit, now un-
> dergoes a Pass-Thru TQ Check. Subtract the unit’s TQ from
> the DR, with any excess being the number of Cohesion Hits
> now applied (DR–TQ=Hits).

Źródło PDF 33, right, C-9.24-03, bbox [314.995, 666.32, 566.897, 676.32]; dokładny source_span: null.

> • Skirmishers do not make an Elephant Pass-Thru Check (9.11).

**first-001 — pending / not_assessable**. Kandydaci: R911, R924; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [171012, 179988); hash zakresu `c45773ef61d2bf1dafaaf60ef44d52dfb19cb59693fa9e476529801f8cfe8463`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

R924, pointer `/rules/14`, bajty [249766, 255895); hash zakresu `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers do not make an Elephant Pass-Thru Check (9.11).",
    "the interruption is caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Line exception applies if interruption caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Single-unit interruption condition."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    },
    {
      "name": "line interruption allowance",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Velites or Skirmisher unit per interruption",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    }
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Repeated movement within Game Turn."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D924stack, G-D924line, G-D-ZOC-R911

**context-01 — pending / not_assessable**. Kandydaci: R911, R924; osobny hash powyżej.

R911, pointer `/rules/0`, bajty [236824, 246111); hash zakresu `d170837160a983848560c5db766ac82833ce19c22c7cec5bc094a0982b395432`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Pass-Thru may be used by two defending infantry units if both units meet the preceding conditions.",
    "Subtract the unit’s TQ from the DR, with any excess being the number of Cohesion Hits now applied (DR–TQ=Hits)."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Infantry attacked through a Front hex by an Elephant marked SHOCK MUST CHECK TQ.",
    "At least one defender Rear hex unoccupied.",
    "Decision before Pre-Shock TQ Check DR; both defenders must qualify if two use it."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Optional Pass-Thru; refusal means normal Shock.",
    "Step 1: +1 DRM to infantry Pre-Shock TQ Check DR.",
    "Step 2: resolve Shock; halve defender Cohesion Hits, round down; reduce Elephant Hits by 1.",
    "Step 3: after Shock, if infantry did not rout and Elephant has not rampaged, Elephant player places Elephant in either unoccupied defender Rear hex, maintaining facing.",
    "Step 4: defender other than Skirmisher makes Pass-Thru TQ Check; positive excess DR–TQ is additional Hits."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Not allowed for Flank/Rear attacks, Elephant attacking with other units, or infantry in enemy ZOC at Orders Phase start.",
    "Skirmishers excluded from Step 4.",
    "Step 3 conditional on neither infantry rout nor Elephant rampage."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defenders permitted",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "infantry units",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "unoccupied Rear minimum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "hex",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "defender Hits multiplier",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Elephant Hits adjustment",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    },
    {
      "name": "Pass-Thru Hits",
      "value": "positive excess DR–TQ",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E911a",
          "E911b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E911a",
        "E911b"
      ]
    }
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Choice before Pre-Shock TQ Check die roll.",
    "Enemy ZOC assessed at start of Orders Phase.",
    "Steps 3–4 after Shock resolution."
  ],
  "evidence_ids": [
    "E911a",
    "E911b"
  ],
  "reason": null,
  "gap_ids": []
}
```

R924, pointer `/rules/14`, bajty [318324, 324673); hash zakresu `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers do not make an Elephant Pass-Thru Check (9.11).",
    "the interruption is caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Line exception applies if interruption caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Single-unit interruption condition."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    },
    {
      "name": "line interruption allowance",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Velites or Skirmisher unit per interruption",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    }
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Repeated movement within Game Turn."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D911pre, G-D911shock, G-D924stack, G-D924line, G-D-ZOC-R911

### EXP-005 — M-POC5A.2

Dokładny zatwierdzony zakres: Elephant Screen uses the explicitly named Elephant Screen MRRC row and fires only as Reaction Fire, has its own supply markers, and is absent on Leader Elephant. Actual lookup and supply procedure remain context requirements.

Wyłączenia/niepewności: Pełny wynik ognia wymaga 8.2 i wiersza MRRC.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, left, C-9.12-02, bbox [45.0, 303.127, 297.017, 325.127]; dokładny source_span: null.

> Elephant Screens can Missile Fire with Reaction Fire (8.2) only,
> using the Elephant Screen row on the MRRC. Elephant Screens

Źródło PDF 32, left, C-9.12-03, bbox [45.0, 327.127, 297.023, 361.127]; dokładny source_span: null.

> have their own missile supply markers. Leader elephants do not
> have screens (they usually did, but they were too small to be a
> factor).

**first-001 — pending / not_assessable**. Kandydaci: R912; osobny hash powyżej.

R912, pointer `/rules/1`, bajty [179994, 184187); hash zakresu `3f41d13d808d94b10acd6b9c50291e48c421110a1cbd8ade5b4005da89db6f2b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Elephant Screens can Missile Fire with Reaction Fire (8.2) only, using the Elephant Screen row on the MRRC."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.",
    "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.",
    "Leader elephants have no screens."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E912"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.",
    "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.",
    "Leader elephants have no screens."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Leader elephants lack screens."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E912"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D912react, G-D912MRRC

**context-01 — pending / not_assessable**. Kandydaci: R912; osobny hash powyżej.

R912, pointer `/rules/1`, bajty [246118, 250457); hash zakresu `7f308d008537d03c5e4e9cefca02e958fd41bf37b65dc395a998895b28c401f2`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Elephant Screens can Missile Fire with Reaction Fire (8.2) only, using the Elephant Screen row on the MRRC."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.",
    "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.",
    "Leader elephants have no screens."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E912"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Light skirmisher screen, usually archers, shown by small “a” on counter; firepower lower than normal archers.",
    "Missile Fire only by Reaction Fire, using Elephant Screen MRRC row; separate missile supply markers.",
    "Leader elephants have no screens."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Leader elephants lack screens."
  ],
  "evidence_ids": [
    "E912"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E912"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D912react, G-D912MRRC

### EXP-006 — M-POC5A.2

Dokładny zatwierdzony zakres: RidersasMountedJavelinists,separatejavelin/screenDR,N03-S2nochangefromhistoricaltowerabsence

Wyłączenia/niepewności: Tożsamość wiersza MRRC z samego Mounted Javelinists pozostaje hipotezą DC-031.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, left, C-9.13-01, bbox [45.0, 368.527, 297.019, 414.527]; dokładny source_span: null.

> 9.13 Tower Riders: The riders atop elephants were armed with
> javelins and are treated as Mounted Javelinists for Missile Fire
> purposes. The Elephant unit may use Reaction Fire with both its
> javelins and its screen, with the player rolling separately for each.

Źródło PDF 32, left, N-03-S2, bbox [49.0, 423.03, 293.116, 457.03]; dokładny source_span: "Makes no difference, the rule\nremains the same.".

> DESIGN NOTE: Several historians portray Hannibal’s
> elephants without “towers.” Makes no difference, the rule
> remains the same.

**first-001 — pending / not_assessable**. Kandydaci: R913, R913note; osobny hash powyżej.

R913, pointer `/rules/2`, bajty [184193, 187922); hash zakresu `6ae8731a79d93d63ac442f6c3ebbb060431519b68ea15f099061e09e89710ac9`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The Elephant unit may use Reaction Fire with both its javelins and its screen, with the player rolling separately for each."
  ],
  "evidence_ids": [
    "E913"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Tower riders count as Mounted Javelinists for Missile Fire.",
    "Elephant may Reaction Fire with javelins and screen; roll separately for each."
  ],
  "evidence_ids": [
    "E913"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Tower riders count as Mounted Javelinists for Missile Fire.",
    "Elephant may Reaction Fire with javelins and screen; roll separately for each."
  ],
  "evidence_ids": [
    "E913"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

R913note, pointer `/rules/3`, bajty [187928, 191195); hash zakresu `daa665c7c08f5cc4d8bbd84d94483163762c15694e230b680f9e8355f85d3b61`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Makes no difference, the rule remains the same."
  ],
  "evidence_ids": [
    "E913note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "The Tower Riders rule remains the same despite that portrayal.",
  "evidence_ids": [
    "E913note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Historical portrayal of Hannibal’s elephants without towers."
  ],
  "evidence_ids": [
    "E913note"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "The Tower Riders rule remains the same despite that portrayal.",
  "evidence_ids": [
    "E913note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D913react, G-D913mounted

**context-01 — pending / not_assessable**. Kandydaci: R913, R913note; osobny hash powyżej.

R913, pointer `/rules/2`, bajty [250464, 254326); hash zakresu `cf0f58a2d98a672e77cf653d796bf33730b38d13e2613a8516a04a57e224b290`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The Elephant unit may use Reaction Fire with both its javelins and its screen, with the player rolling separately for each."
  ],
  "evidence_ids": [
    "E913"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Tower riders count as Mounted Javelinists for Missile Fire.",
    "Elephant may Reaction Fire with javelins and screen; roll separately for each."
  ],
  "evidence_ids": [
    "E913"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Tower riders count as Mounted Javelinists for Missile Fire.",
    "Elephant may Reaction Fire with javelins and screen; roll separately for each."
  ],
  "evidence_ids": [
    "E913"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

R913note, pointer `/rules/3`, bajty [254333, 257716); hash zakresu `6fc580e76f219adc2a6ee990c85c9387c2ded93be6d55b5f79a548ec7c5782f5`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Makes no difference, the rule remains the same."
  ],
  "evidence_ids": [
    "E913note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "The Tower Riders rule remains the same despite that portrayal.",
  "evidence_ids": [
    "E913note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Historical portrayal of Hannibal’s elephants without towers."
  ],
  "evidence_ids": [
    "E913note"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "The Tower Riders rule remains the same despite that portrayal.",
  "evidence_ids": [
    "E913note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E913note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D913react, G-D913mounted

### EXP-007 — M-POC5A.2

Dokładny zatwierdzony zakres: Ordinary EL Rout triggers immediate Rampage procedure. Ordinary EL roll 0 heads toward nearest friendly unit with opponent choosing a tie; first 7-9 moves away from cause, subsequent 7-9 eliminates. Concrete map and cause are not invented.

Wyłączenia/niepewności: Kierunku na rzeczywistej mapie nie ustala sam przykład D-01.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, left, C-9.14-01, bbox [45.0, 466.27, 297.01, 512.27]; dokładny source_span: null.

> 9.14 Elephant Rampage: When an Elephant unit routs, it Ram-
> pages. Leader Elephants also Rampage, but they have less of a
> chance of doing so. Each time an Elephant unit routs, its player
> rolls the die and does one of the following, depending on the DR:

Źródło PDF 32, left, T-01, bbox [53.562, 523.318, 292.421, 647.178]; dokładny source_span: null.

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

Źródło PDF 32, right, T-01, bbox [333.145, 58.343, 562.471, 164.503]; dokładny source_span: null.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

Źródło PDF 32, left, TR-01, bbox [68.142, 538.088, 292.421, 584.248]; dokładny source_span: null.

> 0 The Elephant unit heads in the direction of the
> nearest friendly unit, opposing player’s choice
> if there is more than one nearest unit. A Leader
> Elephant is eliminated.

Źródło PDF 32, left, TR-02, bbox [63.142, 589.018, 292.388, 647.178]; dokładny source_span: null.

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

Źródło PDF 32, right, TR-03, bbox [333.145, 58.343, 562.471, 164.503]; dokładny source_span: null.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

**first-001 — pending / not_assessable**. Kandydaci: N914table, R914; osobny hash powyżej.

N914table, pointer `/nodes/0`, bajty [120024, 122102); hash zakresu `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

R914, pointer `/rules/4`, bajty [191201, 210006); hash zakresu `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty, G-D914compass

**context-01 — pending / not_assessable**. Kandydaci: N914table, R914; osobny hash powyżej.

N914table, pointer `/nodes/0`, bajty [167589, 169718); hash zakresu `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

R914, pointer `/rules/4`, bajty [257723, 277141); hash zakresu `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty, G-D914compass

### EXP-008 — M-POC5A.2

Dokładny zatwierdzony zakres: Leader Elephant roll 0 eliminates it; subsequent 7-9 immediately rallies it with Hits=TQ-2 instead of elimination. This owns the subsequent-roll result; first Leader 7-9 is scored only in EXP-009.

Wyłączenia/niepewności: Later7-9LeaderRally outcome andcriticality accepted; actualTQ and4.84counting notclosed. Firsttable7-9 addressedseparatelyEXP009.; Zakres Leader Elephant przy pierwszym 7–9 jest odrębnym nierozstrzygniętym oczekiwaniem.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, left, TR-01, bbox [68.142, 538.088, 292.421, 584.248]; dokładny source_span: null.

> 0 The Elephant unit heads in the direction of the
> nearest friendly unit, opposing player’s choice
> if there is more than one nearest unit. A Leader
> Elephant is eliminated.

Źródło PDF 32, right, TR-03, bbox [333.145, 58.343, 562.471, 164.503]; dokładny source_span: null.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

Źródło PDF 32, right, C-9.14-11, bbox [315.0, 697.799, 567.008, 719.799]; dokładny source_span: null.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

Źródło PDF 33, left, C-9.14-11, bbox [45.0, 54.004, 297.048, 76.004]; dokładny source_span: null.

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

**first-001 — pending / not_assessable**. Kandydaci: N914table, R914; osobny hash powyżej.

N914table, pointer `/nodes/0`, bajty [120024, 122102); hash zakresu `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

R914, pointer `/rules/4`, bajty [191201, 210006); hash zakresu `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty, G-D914compass

**context-01 — pending / not_assessable**. Kandydaci: N914table, R914; osobny hash powyżej.

N914table, pointer `/nodes/0`, bajty [167589, 169718); hash zakresu `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

R914, pointer `/rules/4`, bajty [257723, 277141); hash zakresu `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty, G-D914compass

### EXP-009 — M-POC5A.2

Dokładny zatwierdzony zakres: First Rampage-table 7-9 for Leader Elephant means movement away from the causing unit, without immediate special rally. Subsequent-roll result is referenced in EXP-008 and earns no second point here. Counting the 4.84 trigger die is unresolved.

Wyłączenia/niepewności: FirstLeader7-9interpretation andcriticality accepted;actualcause/map/route/TQ and4.84countingnotclosed.; Przegląd składni tabeli i uzasadniona decyzja właściciela.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, right, TR-03, bbox [333.145, 58.343, 562.471, 164.503]; dokładny source_span: null.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

Źródło PDF 32, right, C-9.14-11, bbox [315.0, 697.799, 567.008, 719.799]; dokładny source_span: null.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

Źródło PDF 33, left, C-9.14-11, bbox [45.0, 54.004, 297.048, 76.004]; dokładny source_span: null.

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

**first-001 — pending / not_assessable**. Kandydaci: N914table, R914; osobny hash powyżej.

N914table, pointer `/nodes/0`, bajty [120024, 122102); hash zakresu `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

R914, pointer `/rules/4`, bajty [191201, 210006); hash zakresu `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty, G-D914compass

**context-01 — pending / not_assessable**. Kandydaci: N914table, R914; osobny hash powyżej.

N914table, pointer `/nodes/0`, bajty [167589, 169718); hash zakresu `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

R914, pointer `/rules/4`, bajty [257723, 277141); hash zakresu `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty, G-D914compass

### EXP-010 — M-POC5A.2

Dokładny zatwierdzony zakres: 1-6 uses actual battle map compass; missing compass blocks concrete direction/hexside.

Wyłączenia/niepewności: A real battle-map compass is required for a concrete direction/hexside.; Wskazana mapa bitwy z dowodem i kompasem, bez domknięcia całej instrukcji.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, left, TR-02, bbox [63.142, 589.018, 292.388, 647.178]; dokładny source_span: null.

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

Źródło PDF 32, right, D-01, bbox [350, 220, 535, 299]; dokładny source_span: null.

> 

Źródło PDF 32, right, X-01, bbox [315.0, 303.779, 567.012, 337.779]; dokładny source_span: null.

> EXAMPLE: The above diagram shows the elephant unit refaced
> after a Rampage die roll of 1. This is just an example; use the
> compass on the map for each battle.

**first-001 — pending / not_assessable**. Kandydaci: N914diagram, N914table; osobny hash powyżej.

N914diagram, pointer `/nodes/1`, bajty [122108, 123601); hash zakresu `99553c9e8dd99e5d6630491e66a2f8303144f0c27ea52a45ac24b4b368166f4d`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "caption": "The above diagram shows the elephant unit refaced after a Rampage die roll of 1.",
      "direction_labels": {
        "upper_left": "6",
        "upper_right": "1",
        "right": "2",
        "lower_right": "3",
        "lower_left": "4",
        "left": "5"
      },
      "counter_labels": [
        "Africa",
        "8",
        "J",
        "a",
        "5",
        "EL",
        "5",
        "7"
      ]
    },
    "interpretation": "Left image shows original elephant facing; right image shows clockwise re-facing towards upper-right hexside for example roll 1. Numbers refer to the six directions by hexside. Actual battle map compass governs; no universal geographical direction inferred."
  },
  "evidence_ids": [
    "E914diagram"
  ],
  "reason": null,
  "gap_ids": []
}
```

N914table, pointer `/nodes/0`, bajty [120024, 122102); hash zakresu `3579442988229f6c3d906f53ba791ed7ce73c7a68283c8e6170dcc3b639a91eb`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914compass

**context-01 — pending / not_assessable**. Kandydaci: N914diagram, N914table; osobny hash powyżej.

N914diagram, pointer `/nodes/1`, bajty [169725, 171268); hash zakresu `1365c92a4d04710676a2e125eb8e5f6adccbbcf43675f2725fb1db147361d934`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "caption": "The above diagram shows the elephant unit refaced after a Rampage die roll of 1.",
      "direction_labels": {
        "upper_left": "6",
        "upper_right": "1",
        "right": "2",
        "lower_right": "3",
        "lower_left": "4",
        "left": "5"
      },
      "counter_labels": [
        "Africa",
        "8",
        "J",
        "a",
        "5",
        "EL",
        "5",
        "7"
      ]
    },
    "interpretation": "Left image shows original elephant facing; right image shows clockwise re-facing towards upper-right hexside for example roll 1. Numbers refer to the six directions by hexside. Actual battle map compass governs; no universal geographical direction inferred."
  },
  "evidence_ids": [
    "E914diagram"
  ],
  "reason": null,
  "gap_ids": []
}
```

N914table, pointer `/nodes/0`, bajty [167589, 169718); hash zakresu `cdd196904bca1815616a2a63170f61ede0637d7135e9cd66e7995f6205bba943`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "headers": [
        "Die Roll",
        "Result"
      ],
      "rows": [
        {
          "die_roll": "0",
          "result": "The Elephant unit heads in the direction of the nearest friendly unit, opposing player’s choice if there is more than one nearest unit. A Leader Elephant is eliminated."
        },
        {
          "die_roll": "1–6",
          "result": "The Elephant unit heads in the direction indicated on the Compass on the map, an example of which is given below. Note that geographical direction is represented at the vertex; the direction in which the Elephant is to Rampage is by hexside."
        },
        {
          "die_roll": "7–9",
          "result": "On the first Rampage DR, the Elephant heads in the direction directly away from the unit that caused the rampage. A 7-9 on any subsequent die roll means the elephant’s mahout has been successful in stopping the rampage by driving a wedge into the beast’s brain; the Elephant unit is eliminated. If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2."
        }
      ]
    },
    "interpretation": "Roll table spans left and right columns; Leader Elephant outcomes are distinct, including an explicit rally exception."
  },
  "evidence_ids": [
    "E914tableL",
    "E914tableR"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914compass

### EXP-011 — M-POC5A.2

Dokładny zatwierdzony zakres: Complete each Rampage immediately before any other mechanic except OW under 6.51; no concurrent Rampages. Rampaging EL has no ZOC, triggers no Reaction Fire of any kind, and normally cannot rally. The special later Leader result is a reference to EXP-008, not a second scored result.

Wyłączenia/niepewności: OW 6.51 wymaga zewnętrznej procedury; szczególny Leader Elephant zachować oddzielnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, right, C-9.14-02, bbox [315.005, 180.783, 567.114, 214.783]; dokładny source_span: null.

> Each Elephant Rampage is always resolved immediately, before
> any other game mechanic is addressed, except for Orderly With-
> drawal in face of the rampaging elephant (6.51).

Źródło PDF 32, right, C-9.14-11, bbox [315.0, 697.799, 567.008, 719.799]; dokładny source_span: null.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

Źródło PDF 33, left, C-9.14-11, bbox [45.0, 54.004, 297.048, 76.004]; dokładny source_span: null.

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

**first-001 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [191201, 210006); hash zakresu `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

**context-01 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [257723, 277141); hash zakresu `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

### EXP-012 — M-POC5A.2

Dokładny zatwierdzony zakres: Attempt 3 hexes per directional roll with supplied route/no early termination. At a would-be occupied hex stop adjacent; occupant gets 1 CH via Front, 2 via Flank/Rear, cavalry always 2. Both units of a stack get their Hits. A leader unable to withdraw under 4.72 dies without DR; actual inability requires context.

Wyłączenia/niepewności: Możliwość withdrawal leadera wymaga 4.72; geometrię i typy przyjąć tylko jako jawne dane przypadku.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, right, C-9.14-03, bbox [315.0, 345.179, 567.03, 451.179]; dokładny source_span: null.

> A rampaging Elephant and any stacked leader with it always
> attempt to move 3 hexes per directional die roll in the indicated
> direction until it either moves off the map or is otherwise elimi-
> nated. If a rampaging Elephant unit would enter a hex occupied
> by a unit, whether enemy or friendly, the Elephant unit stops in
> the adjacent hex and the unit incurs 1 Cohesion Hit if the Elephant
> would have entered through a Front hex or 2 Cohesion Hits if it
> would have entered through a Flank or Rear hex. A cavalry unit
> incurs 2 Cohesion Hits regardless of the angle.

Źródło PDF 32, right, C-9.14-04, bbox [315.0, 458.579, 567.026, 516.579]; dokładny source_span: null.

> If the affected units are a stack, both units receive the Cohesion
> Hits. If there is a leader in the hex (alone or stacked with a unit),
> and he cannot withdraw (see 4.72), he is tragically impaled on
> the elephant’s tusks, tossed high in the air, and then crushed to
> death under its feet. All that without a die roll!

**first-001 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [191201, 210006); hash zakresu `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

**context-01 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [257723, 277141); hash zakresu `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

### EXP-013 — M-POC5A.2

Dokładny zatwierdzony zakres: Repeat until offmap, elimination(ordinaryEL7-9mahout), at least8hexes from nearest unit(any allegiance) causing elimination, or if none above eliminate after4th consecutive RampageDR.

Wyłączenia/niepewności: Nie dorabiać pomiaru odległości na nieznanej mapie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, right, C-9.14-06, bbox [315.0, 538.859, 498.76, 548.859]; dokładny source_span: null.

> • The Elephant unit rampages off the map, or

Źródło PDF 32, right, C-9.14-07, bbox [315.0, 552.299, 534.79, 562.299]; dokładny source_span: null.

> • The Elephant unit is eliminated (7-9 mahout DR), or

Źródło PDF 32, right, C-9.14-08, bbox [315.0, 565.739, 567.009, 587.739]; dokładny source_span: null.

> • The Elephant unit is at least 8 hexes from the nearest unit, in
> which case it is eliminated, or

Źródło PDF 32, right, C-9.14-09, bbox [315.0, 591.179, 567.008, 613.179]; dokładny source_span: null.

> • If none of the above, after the 4th consecutive Rampage DR,
> the Elephant unit is eliminated.

**first-001 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [191201, 210006); hash zakresu `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

**context-01 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [257723, 277141); hash zakresu `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

### EXP-014 — M-POC5A.2

Dokładny zatwierdzony zakres: Leader stackedwithRampagingEL travelswithit. At end leadercasualty4.73; survivor stayswhereELended. If ELoffmap bothELandleader eliminated, not survival inferred fromcasualtyDR.

Wyłączenia/niepewności: Wynik casualty wymaga 4.73; nie wyliczać prawdopodobieństwa bez celu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 32, right, C-9.14-10, bbox [315.0, 620.399, 567.008, 690.399]; dokładny source_span: null.

> A leader stacked with a rampaging Elephant goes along with
> the Elephant on the Rampage. When the Rampage ends, the
> player rolls for a leader casualty (4.73). If the leader survives,
> he remains on the map where the Elephant ended the Rampage.
> If the Elephant Rampages off the map, both the Elephant and
> leader are eliminated.

**first-001 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [191201, 210006); hash zakresu `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

**context-01 — pending / not_assessable**. Kandydaci: R914; osobny hash powyżej.

R914, pointer `/rules/4`, bajty [257723, 277141); hash zakresu `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:",
    "Die Roll Result",
    "If it is a Leader Elephant, the unit is, instead, immediately rallied with Cohesion Hits equal to its TQ minus 2.",
    "Each Elephant Rampage is always resolved immediately, before any other game mechanic is addressed, except for Orderly Withdrawal in face of the rampaging elephant (6.51).",
    "This is just an example; use the compass on the map for each battle.",
    "A cavalry unit incurs 2 Cohesion Hits regardless of the angle.",
    "If none of the above, after the 4th consecutive Rampage DR, the Elephant unit is eliminated.",
    "Rampaging elephants have no ZOC, do not trigger Reaction Fire of any kind, and they may not be rallied.",
    "undertaken until its conclusion, so there may never be more than one rampaging Elephant unit at any one time."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Each Elephant rout, including Leader Elephant."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Roll and use N914table; lower chance of rampaging is stated for Leader Elephants.",
    "Resolve each Rampage immediately and to conclusion before any other mechanic, except OW in face of rampaging Elephant.",
    "Elephant and stacked leader attempt 3 hexes per directional DR until off-map or otherwise eliminated.",
    "If a friendly/enemy unit occupies the intended entered hex, Elephant stops adjacent; occupant takes 1 Hit for Front entry, 2 for Flank/Rear; cavalry always 2. Both units in an affected stack take Hits.",
    "Leader in impacted hex dies without a roll if unable to withdraw under 4.72.",
    "Roll again: terminate on off-map, 7-9 mahout elimination, being at least 8 hexes from nearest unit (eliminate), or after 4th consecutive Rampage DR (eliminate) if no earlier condition.",
    "Stacked leader travels with Elephant; at end roll leader casualty under 4.73; survivor remains where Rampage ended. If off-map, both eliminated.",
    "Rampaging Elephant has no ZOC, triggers no Reaction Fire and cannot be rallied; finish one Rampage before another."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Orderly Withdrawal interrupts priority.",
    "Leader Elephant table: 0 eliminates; subsequent 7–9 immediately rallies at TQ–2 Hits, overriding general non-rally text for this explicit result.",
    "Cavalry occupant always takes 2 Hits.",
    "Off-map stacked leader eliminated without survival placement."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "directional roll movement",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "hexes per directional die roll",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Front contact",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Flank/Rear contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per affected unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "cavalry contact",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "isolation termination",
      "value": ">=8",
      "unit": {
        "state": "known",
        "value": "hexes from nearest unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "maximum sequence",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "consecutive Rampage DR",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "concurrent Rampages maximum",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Elephant unit",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "Leader rally Hits",
      "value": "TQ–2",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    },
    {
      "name": "table roll groups",
      "value": [
        "0",
        "1–6",
        "7–9"
      ],
      "unit": {
        "state": "known",
        "value": "die-roll results",
        "evidence_ids": [
          "E914start",
          "E914tableL",
          "E914tableR",
          "E914priority",
          "E914diagram",
          "E914move",
          "E914end",
          "E914last",
          "E914cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E914start",
        "E914tableL",
        "E914tableR",
        "E914priority",
        "E914diagram",
        "E914move",
        "E914end",
        "E914last",
        "E914cont"
      ]
    }
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate, serial resolution until conclusion.",
    "First versus subsequent DR matters.",
    "Leader casualty at Rampage end."
  ],
  "evidence_ids": [
    "E914start",
    "E914tableL",
    "E914tableR",
    "E914priority",
    "E914diagram",
    "E914move",
    "E914end",
    "E914last",
    "E914cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D914OW, G-D914leaderwithdraw, G-D914casualty

### EXP-015 — M-POC5A.2

Dokładny zatwierdzony zakres: Cavalry cannot voluntarily enterenemyELZOC; enteringeach enemyELFlank/Rearhex incurs2CH, samepenaltyforforcedentryELZOC; no cavalryattackenemyELFront; Flank/Rearattack doesnotgainusualAS. Nofullpositiveattackpermission.

Wyłączenia/niepewności: Wyliczenie geometrii ZOC i bazowego Shock wymaga reguł ogólnych.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, left, C-9.15-01, bbox [45.0, 139.747, 297.13, 245.747]; dokładny source_span: null.

> 9.15 Cavalry vs. Elephants: Cavalry units may never voluntarily
> move into the ZOC of an enemy Elephant unit. They may move
> into or through an enemy Elephant’s Flank or Rear hexes but
> at the cost of 2 Cohesion Hits for each such hex entered. This
> cohesion penalty also applies if the cavalry unit is forced to enter
> an Elephant ZOC. Cavalry may never attack an enemy Elephant
> through the latter’s Front hexes; they may attack through the
> Elephant unit’s Flank or Rear hexes, but they do not gain the
> usual Attack Superiority for such an attack.

**first-001 — pending / not_assessable**. Kandydaci: R915; osobny hash powyżej.

R915, pointer `/rules/5`, bajty [210012, 214748); hash zakresu `e7a73035f7d9687d28f1dcb19e01d02be16cd4d325a249d7b7fc1b9a0dfaf226`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Cavalry units may never voluntarily move into the ZOC of an enemy Elephant unit."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Cavalry may not voluntarily enter enemy Elephant ZOC.",
    "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.",
    "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E915"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Cavalry may not voluntarily enter enemy Elephant ZOC.",
    "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.",
    "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Forced ZOC entry uses the 2-Hit penalty.",
    "Flank/Rear attacks allowed but do not gain usual Attack Superiority."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "entry penalty",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per such hex entered",
        "evidence_ids": [
          "E915"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E915"
      ]
    }
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D915superiority, G-D-ZOC-R915

**context-01 — pending / not_assessable**. Kandydaci: R915; osobny hash powyżej.

R915, pointer `/rules/5`, bajty [277148, 282047); hash zakresu `cf617cf7b5c3ca2083c7fb23420fe52d8cc8d0f87cec79861f8fe21e3464ae8e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Cavalry units may never voluntarily move into the ZOC of an enemy Elephant unit."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Cavalry may not voluntarily enter enemy Elephant ZOC.",
    "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.",
    "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E915"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Cavalry may not voluntarily enter enemy Elephant ZOC.",
    "May enter/pass enemy Elephant Flank/Rear hexes for 2 Hits per entered hex; same penalty on forced Elephant ZOC entry.",
    "Cannot attack enemy Elephant through its Front; may attack Flank/Rear without normal Attack Superiority."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Forced ZOC entry uses the 2-Hit penalty.",
    "Flank/Rear attacks allowed but do not gain usual Attack Superiority."
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "entry penalty",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits per such hex entered",
        "evidence_ids": [
          "E915"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E915"
      ]
    }
  ],
  "evidence_ids": [
    "E915"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D915superiority, G-D-ZOC-R915

### EXP-016 — M-POC5A.2

Dokładny zatwierdzony zakres: Ordinary EL moving from nonadjacent to adjacent enemy cavalry forces an OW attempt. If cavalry can withdraw, no Reaction Fire; otherwise immediate TQ check, and routed cavalry eliminates without DR in the supplied cannot-withdraw branch. Leader EL excluded. Arithmetic belongs to EXP-017.

Wyłączenia/niepewności: OW i ustalenie możliwości withdrawal wymagają kontekstu; zakres minimum dla DR≤TQ osobno.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, left, C-9.16-01, bbox [45.0, 253.147, 297.021, 371.147]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R916; osobny hash powyżej.

R916, pointer `/rules/6`, bajty [214754, 219957); hash zakresu `7a3e47595d7018caed44c65c56be0fb9558e0a1a69c8c87522c6e82d1d719d49`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This rule does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.",
  "gap_ids": [
    "G916"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.",
    "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.",
    "Already routed cavalry automatically eliminated without DR."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "TQ check comparison",
      "value": "DR > TQ",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    },
    {
      "name": "Hits",
      "value": "DR–TQ; minimum result 1",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    }
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "On adjacency from non-adjacent hex; immediate check if cannot withdraw."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G916, G-D916OW

**context-01 — pending / not_assessable**. Kandydaci: R916; osobny hash powyżej.

R916, pointer `/rules/6`, bajty [282054, 287456); hash zakresu `24d2167ad17175100c6e004dadba05315767f139f2955cd85082f5ebf04f590a`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This rule does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.",
  "gap_ids": [
    "G916"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.",
    "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.",
    "Already routed cavalry automatically eliminated without DR."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "TQ check comparison",
      "value": "DR > TQ",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    },
    {
      "name": "Hits",
      "value": "DR–TQ; minimum result 1",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    }
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "On adjacency from non-adjacent hex; immediate check if cannot withdraw."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G916, G-D916OW

### EXP-017 — M-POC5A.2

Dokładny zatwierdzony zakres: W9.16 przy DR<=TQ kawaleria nie otrzymuje CH; przy DR>TQ otrzymuje DR-TQ CH, z minimum1. Minimum nie wyłącza warunku DR>TQ.

Wyłączenia/niepewności: LocalDR<=TQ0CH/DR>TQdifference+min1 interpretation andcriticality accepted; nofullOW/cavalryprocedure or targetmetadata closure.; Właściciel rozstrzyga zakres minimum z tekstem lub wskazuje potrzebny dowód.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, left, C-9.16-01, bbox [45.0, 253.147, 297.021, 371.147]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R916; osobny hash powyżej.

R916, pointer `/rules/6`, bajty [214754, 219957); hash zakresu `7a3e47595d7018caed44c65c56be0fb9558e0a1a69c8c87522c6e82d1d719d49`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This rule does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.",
  "gap_ids": [
    "G916"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.",
    "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.",
    "Already routed cavalry automatically eliminated without DR."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "TQ check comparison",
      "value": "DR > TQ",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    },
    {
      "name": "Hits",
      "value": "DR–TQ; minimum result 1",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    }
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "On adjacency from non-adjacent hex; immediate check if cannot withdraw."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G916, G-D916OW

**context-01 — pending / not_assessable**. Kandydaci: R916; osobny hash powyżej.

R916, pointer `/rules/6`, bajty [282054, 287456); hash zakresu `24d2167ad17175100c6e004dadba05315767f139f2955cd85082f5ebf04f590a`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This rule does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "The minimum-1 scope for DR<=TQ is not explicit; no complete check outcome inferred.",
  "gap_ids": [
    "G916"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy Elephant moves from non-adjacent hex to adjacent to cavalry."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Cavalry must attempt OW; no form of Reaction Fire if it can withdraw.",
    "If unable to withdraw, immediate TQ check; source says if DR>TQ incur difference in Hits, with minimum result 1 Hit.",
    "Already routed cavalry automatically eliminated without DR."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Does not apply to Leader Elephants."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "TQ check comparison",
      "value": "DR > TQ",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    },
    {
      "name": "Hits",
      "value": "DR–TQ; minimum result 1",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E916"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E916"
      ]
    }
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "On adjacency from non-adjacent hex; immediate check if cannot withdraw."
  ],
  "evidence_ids": [
    "E916"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G916, G-D916OW

### EXP-018 — M-POC5A.2

Dokładny zatwierdzony zakres: ELvsEL neither side PositionSuperiority, including no positionalASfromFlank/Rear; notallpossibletypesofsuperiorityexcluded.

Wyłączenia/niepewności: Nie rozszerzać zakazu na wszystkie rodzaje superiority.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, left, C-9.17-01, bbox [45.0, 378.547, 297.02, 424.547]; dokładny source_span: null.

> 9.17 In any instance where Elephant units attack other Elephant
> units, neither side may gain Position Superiority. Thus, one
> Elephant attacking another Elephant through the latter’s Flank/
> Rear does not gain Attack Superiority.

**first-001 — pending / not_assessable**. Kandydaci: R917; osobny hash powyżej.

R917, pointer `/rules/7`, bajty [219963, 223365); hash zakresu `63af6f30b27679af5c8b57201640efcb4a3682e020bfdbe15a3d27e411c84ac6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "neither side may gain Position Superiority."
  ],
  "evidence_ids": [
    "E917"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.",
  "evidence_ids": [
    "E917"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Elephant attacks another Elephant."
  ],
  "evidence_ids": [
    "E917"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.",
  "evidence_ids": [
    "E917"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E917"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E917"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D917position

**context-01 — pending / not_assessable**. Kandydaci: R917; osobny hash powyżej.

R917, pointer `/rules/7`, bajty [287463, 290991); hash zakresu `cb0234059d792c80894b60db2acd72e1e243aba445d6746eeac66ddb3035eb0a`.

transcription:
```json
{
  "state": "known",
  "value": [
    "neither side may gain Position Superiority."
  ],
  "evidence_ids": [
    "E917"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.",
  "evidence_ids": [
    "E917"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Elephant attacks another Elephant."
  ],
  "evidence_ids": [
    "E917"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Neither side may gain Position Superiority; Elephant Flank/Rear attack gains no Attack Superiority.",
  "evidence_ids": [
    "E917"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E917"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E917"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D917position

### EXP-019 — M-POC5A.2

Dokładny zatwierdzony zakres: Any leader maycommandEL unlessrules specificallyotherwise. Actual leaderauthorization requirescheckingexceptions; keeprequires_context, no inventedactualeligibility.

Wyłączenia/niepewności: Actual leader eligibility and rule-specific exceptions require external context.; Wskazany leader, scenariusz i źródło jego ograniczeń; lokalna reguła ogólna pozostaje znana.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, left, C-9.18-01, bbox [45.0, 455.45, 297.002, 477.45]; dokładny source_span: null.

> 9.18 Unless the rules specifically state otherwise, Elephant units
> may be commanded by any leader.

**first-001 — pending / not_assessable**. Kandydaci: R918; osobny hash powyżej.

R918, pointer `/rules/8`, bajty [223371, 226469); hash zakresu `d2ef7d501f146bfd281fbaa1eae741db574916086ba549200fddadbe2e5c5cc1`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Unless the rules specifically state otherwise, Elephant units may be commanded by any leader."
  ],
  "evidence_ids": [
    "E918"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Any leader may command Elephant units.",
  "evidence_ids": [
    "E918"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E918"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Any leader may command Elephant units.",
  "evidence_ids": [
    "E918"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Specific exceptions are acknowledged but not enumerated in supplied clause.",
  "gap_ids": [
    "G-D918specific"
  ]
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E918"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D918specific

**context-01 — pending / not_assessable**. Kandydaci: R918; osobny hash powyżej.

R918, pointer `/rules/8`, bajty [290998, 294212); hash zakresu `d7a45288d96c2d73bc22a2bc1b20b8c03362c7d8c907b908c1b9dfae8df0ae67`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Unless the rules specifically state otherwise, Elephant units may be commanded by any leader."
  ],
  "evidence_ids": [
    "E918"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Any leader may command Elephant units.",
  "evidence_ids": [
    "E918"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E918"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Any leader may command Elephant units.",
  "evidence_ids": [
    "E918"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Specific exceptions are acknowledged but not enumerated in supplied clause.",
  "gap_ids": [
    "G-D918specific"
  ]
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E918"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D918specific

### EXP-020 — M-POC5A.2

Dokładny zatwierdzony zakres: WhenIndianELfightAfricanEL:AfricanEL+1PreShockDRM, inadditiontoClashofSpearsandSwords andShockSuperiority notes; notIndian+1norallEL+1norwaiveroftablenotes.

Wyłączenia/niepewności: Clash of Spears and Swords, Shock Superiority oraz 8.43 wymagają źródeł do pełnego Shock.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, left, C-9.19-01, bbox [45.0, 484.85, 297.116, 542.85]; dokładny source_span: null.

> 9.19 Indians vs. Africans: In addition to the notes on the Clash of
> Spears and Swords and Shock Superiority Charts, the following
> rule is in effect when Indian Elephants fight African Elephants:
> African Elephants incur a +1 DRM to their Pre-Shock die rolls
> (8.43).

**first-001 — pending / not_assessable**. Kandydaci: R919; osobny hash powyżej.

R919, pointer `/rules/9`, bajty [226475, 230470); hash zakresu `d55d07a6e11f89c7a28adb050205027c3cf23a3a60661483c5da133df78666d3`.

transcription:
```json
{
  "state": "known",
  "value": [
    "African Elephants incur a +1 DRM to their Pre-Shock die rolls (8.43)."
  ],
  "evidence_ids": [
    "E919"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.",
  "evidence_ids": [
    "E919"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Indian Elephants fight African Elephants."
  ],
  "evidence_ids": [
    "E919"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.",
  "evidence_ids": [
    "E919"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E919"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "African Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E919"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E919"
      ]
    }
  ],
  "evidence_ids": [
    "E919"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D919pre, G-D919clash, G-D919shock

**context-01 — pending / not_assessable**. Kandydaci: R919; osobny hash powyżej.

R919, pointer `/rules/9`, bajty [294219, 298360); hash zakresu `0570133a32e2c860a0a2cd97438a1c41e489344facec89dbf3cac591a0f397ea`.

transcription:
```json
{
  "state": "known",
  "value": [
    "African Elephants incur a +1 DRM to their Pre-Shock die rolls (8.43)."
  ],
  "evidence_ids": [
    "E919"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.",
  "evidence_ids": [
    "E919"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Indian Elephants fight African Elephants."
  ],
  "evidence_ids": [
    "E919"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "In addition to notes on Clash of Spears and Swords and Shock Superiority Charts, African Elephants take +1 DRM to Pre-Shock die rolls.",
  "evidence_ids": [
    "E919"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E919"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "African Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E919"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E919"
      ]
    }
  ],
  "evidence_ids": [
    "E919"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D919pre, G-D919clash, G-D919shock

### EXP-021 — M-POC5A.2

Dokładny zatwierdzony zakres: Velites are LI, not SK; SK exceptions do not transfer by similarity. SK OW incurs Hits only via Rear; Velites via Flank or Rear. OW distance/MA condition belongs to EXP-022.

Wyłączenia/niepewności: Added maneuver nie definiuje wszystkich uprawnień; procedura OW pozostaje zewnętrzna.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, N-07-S2, bbox [319.0, 84.7, 563.059, 226.7]; dokładny source_span: "Their forma-\ntion, however, was not so “open”, and they are not treated as\nskirmishers; they are Light Infantry, which also have some\nadded maneuver capabilities.".

> DESIGN NOTE: Skirmisher units were truly ill-suited for
> Shock Combat; they were, in fact, trained to avoid it. Skirmish-
> ers rarely had any armor protection, and the only weapons
> they carried were their bows, slings, or javelins. They fought
> dispersed in “open” formation, and their intent was to delay,
> harass and screen (although they were quite effective against
> elephants and chariots). Velites were the first line of a legionary
> deployment. Although more heavily armed than skirmishers,
> their function and training were much the same. Their forma-
> tion, however, was not so “open”, and they are not treated as
> skirmishers; they are Light Infantry, which also have some
> added maneuver capabilities.

Źródło PDF 33, right, C-9.21-01, bbox [314.995, 235.94, 567.583, 317.94]; dokładny source_span: null.

> 9.21 Orderly Withdrawal: Skirmishers may Orderly
> Withdraw up to 2 hexes before any units whose MA
> is the same or less (i.e., all infantry units), regardless
> of the MA differential. The only time Skirmishers
> incur Cohesion Hits when using OW is after being approached
> from a Rear hex. The only time Velites incur Cohesion Hits from
> OW is after being approached from a Flank or Rear hex.

**first-001 — pending / not_assessable**. Kandydaci: N92design, R921, R92note; osobny hash powyżej.

N92design, pointer `/nodes/24`, bajty [142234, 143048); hash zakresu `06557a0571509b2b41162d16c634800e71f5138b049bdbbe5d769f43280da535`.

content:
```json
{
  "state": "known",
  "value": "Historical context of Skirmisher weapons/open formation and harassment role, Velites first line of legionary deployment and less-open formation. Operative Velites classification owned by R92note.",
  "evidence_ids": [
    "E92design"
  ],
  "reason": null,
  "gap_ids": []
}
```

R921, pointer `/rules/11`, bajty [234091, 238938); hash zakresu `cfe4efdae432e0047facb62fddc25627addc679b00fe30a91959f6a1c715ce32`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "OW maximum",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "hexes",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    },
    {
      "name": "approaching MA",
      "value": "<= withdrawing Skirmisher MA",
      "unit": {
        "state": "known",
        "value": "MA comparison",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    }
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

R92note, pointer `/rules/10`, bajty [230476, 234085); hash zakresu `77b7cd1fd5a784f68bdbc62ea18264365019ddc79b4a90cbc5326e7bfc953e23`.

transcription:
```json
{
  "state": "known",
  "value": [
    "they are not treated as skirmishers; they are Light Infantry, which also have some added maneuver capabilities."
  ],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.",
  "evidence_ids": [
    "E92note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.",
  "evidence_ids": [
    "E92note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D921OW

**context-01 — pending / not_assessable**. Kandydaci: N92design, R921, R92note; osobny hash powyżej.

N92design, pointer `/nodes/24`, bajty [191063, 191904); hash zakresu `f714c9ad53d998b3e9866366d7a25d9c30c323a4ea051ff70b9acd807b945ea4`.

content:
```json
{
  "state": "known",
  "value": "Historical context of Skirmisher weapons/open formation and harassment role, Velites first line of legionary deployment and less-open formation. Operative Velites classification owned by R92note.",
  "evidence_ids": [
    "E92design"
  ],
  "reason": null,
  "gap_ids": []
}
```

R921, pointer `/rules/11`, bajty [302099, 307124); hash zakresu `7d4cae8640312910b3a82d27a32c19c34148a5723d11798a0df99ab1c459d0aa`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "OW maximum",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "hexes",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    },
    {
      "name": "approaching MA",
      "value": "<= withdrawing Skirmisher MA",
      "unit": {
        "state": "known",
        "value": "MA comparison",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    }
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

R92note, pointer `/rules/10`, bajty [298367, 302092); hash zakresu `a9052b99d997213c3c6f44fe1a85290abe7bcd5df64b1f8caa64ed751a81072a`.

transcription:
```json
{
  "state": "known",
  "value": [
    "they are not treated as skirmishers; they are Light Infantry, which also have some added maneuver capabilities."
  ],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.",
  "evidence_ids": [
    "E92note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Velites are Light Infantry with added maneuver capabilities and are not treated as Skirmishers; historical description distinguishes their less-open formation.",
  "evidence_ids": [
    "E92note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E92note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D921OW

### EXP-022 — M-POC5A.2

Dokładny zatwierdzony zakres: SK may OW up to 2 hexes before an approaching unit with MA equal to or less than SK MA. OW angle costs belong to EXP-021; real routes remain context-dependent.

Wyłączenia/niepewności: Pełna trasa OW wymaga procedury, mapy i danych.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, C-9.21-01, bbox [314.995, 235.94, 567.583, 317.94]; dokładny source_span: null.

> 9.21 Orderly Withdrawal: Skirmishers may Orderly
> Withdraw up to 2 hexes before any units whose MA
> is the same or less (i.e., all infantry units), regardless
> of the MA differential. The only time Skirmishers
> incur Cohesion Hits when using OW is after being approached
> from a Rear hex. The only time Velites incur Cohesion Hits from
> OW is after being approached from a Flank or Rear hex.

**first-001 — pending / not_assessable**. Kandydaci: R921; osobny hash powyżej.

R921, pointer `/rules/11`, bajty [234091, 238938); hash zakresu `cfe4efdae432e0047facb62fddc25627addc679b00fe30a91959f6a1c715ce32`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "OW maximum",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "hexes",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    },
    {
      "name": "approaching MA",
      "value": "<= withdrawing Skirmisher MA",
      "unit": {
        "state": "known",
        "value": "MA comparison",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    }
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D921OW

**context-01 — pending / not_assessable**. Kandydaci: R921; osobny hash powyżej.

R921, pointer `/rules/11`, bajty [302099, 307124); hash zakresu `7d4cae8640312910b3a82d27a32c19c34148a5723d11798a0df99ab1c459d0aa`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers may Orderly Withdraw up to 2 hexes before any units whose MA is the same or less"
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Skirmisher faces approaching unit with same or lower MA (source parenthesis: all infantry units)."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmisher may OW up to 2 hexes regardless of MA differential.",
    "Skirmisher incurs OW Hits only when approached from Rear; Velites only when approached from Flank/Rear."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear approach for Skirmishers; Flank/Rear for Velites incur Hits."
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "OW maximum",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "hexes",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    },
    {
      "name": "approaching MA",
      "value": "<= withdrawing Skirmisher MA",
      "unit": {
        "state": "known",
        "value": "MA comparison",
        "evidence_ids": [
          "E921"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E921"
      ]
    }
  ],
  "evidence_ids": [
    "E921"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D921OW

### EXP-023 — M-POC5A.2

Dokładny zatwierdzony zakres: targetSKMissile+2DRM;SK/LIArchersA noH&D;LCanymissileclass noH&DvsSK

Wyłączenia/niepewności: Wynik ognia wymaga MRRC i H&D; brak zakazu nie dowodzi pełnej legalności.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, C-9.22-01, bbox [314.995, 325.34, 567.021, 371.34]; dokładny source_span: null.

> 9.22 Missile Fire: There is a +2 DRM to the Missile Fire DR
> whenever a Skirmisher unit is the target. Skirmisher and Light
> Infantry Archers (Class A) cannot use H&D fire. Light Cavalry
> (all missile classes) cannot use H&D against Skirmishers..

**first-001 — pending / not_assessable**. Kandydaci: R922; osobny hash powyżej.

R922, pointer `/rules/12`, bajty [238944, 243461); hash zakresu `a9598a0db96d75f2c086f3ef29f067d725296d84db5b293cc8eafd8a0cd1c7f2`.

transcription:
```json
{
  "state": "known",
  "value": [
    "There is a +2 DRM to the Missile Fire DR whenever a Skirmisher unit is the target."
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "+2 Missile Fire DRM when Skirmisher is target.",
    "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.",
    "Light Cavalry of all missile classes cannot H&D against Skirmishers."
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E922"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "+2 Missile Fire DRM when Skirmisher is target.",
    "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.",
    "Light Cavalry of all missile classes cannot H&D against Skirmishers."
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E922"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher-target modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E922"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E922"
      ]
    }
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D922missile, G-D922HD

**context-01 — pending / not_assessable**. Kandydaci: R922; osobny hash powyżej.

R922, pointer `/rules/12`, bajty [307131, 311809); hash zakresu `68bf0a61ddd806de4cb7850830a717026f0a98611306b6b6f7c3155fcaf2c767`.

transcription:
```json
{
  "state": "known",
  "value": [
    "There is a +2 DRM to the Missile Fire DR whenever a Skirmisher unit is the target."
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "+2 Missile Fire DRM when Skirmisher is target.",
    "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.",
    "Light Cavalry of all missile classes cannot H&D against Skirmishers."
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E922"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "+2 Missile Fire DRM when Skirmisher is target.",
    "Skirmisher and Light Infantry Archers (Class A) cannot use H&D fire.",
    "Light Cavalry of all missile classes cannot H&D against Skirmishers."
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E922"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher-target modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E922"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E922"
      ]
    }
  ],
  "evidence_ids": [
    "E922"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D922missile, G-D922HD

### EXP-024 — M-POC5A.2

Dokładny zatwierdzony zakres: SK cannot Shock attack; units attacking a defense consisting only of SK are exempt from Pre-Shock TQ even with the marker. With mixed defense use the other type and ignore SK Size. This owns the attacker exemption; EXP-004 owns the final Pass-Thru check.

Wyłączenia/niepewności: Nie przypisywać SK immunitetu od innych testów ani obrońcy mieszanego.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, C-9.23-02, bbox [314.995, 405.62, 457.315, 415.62]; dokładny source_span: null.

> • Skirmishers cannot Shock attack.

Źródło PDF 33, right, C-9.23-03, bbox [314.995, 419.06, 567.159, 453.06]; dokładny source_span: null.

> • All units that Shock attack Skirmishers alone do not have
> to make a Pre-Shock TQ even if they have SHOCK MUST
> CHECK TQ markers.

Źródło PDF 33, right, C-9.23-04, bbox [314.995, 456.5, 567.095, 490.5]; dokładny source_span: null.

> • If a Skirmisher unit is defending in coordination with any other
> unit type, the other Type must be chosen as the defender. The
> Size rating of the Skirmisher is ignored.

**first-001 — pending / not_assessable**. Kandydaci: R923; osobny hash powyżej.

R923, pointer `/rules/13`, bajty [243467, 249760); hash zakresu `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Shock Combat involving specified unit types."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmishers alone differs from mixed defense.",
    "Front LI attack exemption is not reciprocal."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    },
    {
      "name": "Skirmisher inflicted-Hits cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    }
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D923pre, G-D923shock

**context-01 — pending / not_assessable**. Kandydaci: R923; osobny hash powyżej.

R923, pointer `/rules/13`, bajty [311816, 318317); hash zakresu `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Shock Combat involving specified unit types."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmishers alone differs from mixed defense.",
    "Front LI attack exemption is not reciprocal."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    },
    {
      "name": "Skirmisher inflicted-Hits cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    }
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D923pre, G-D923shock, GCTX-CRT, GCTX-applicability

### EXP-025 — M-POC5A.2

Dokładny zatwierdzony zakres: HitsinflictedbySKhalvefloor,cap1

Wyłączenia/niepewności: Bazowe Hits muszą być podane; kolejność innych modyfikatorów wymaga kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, C-9.23-05, bbox [314.995, 493.94, 567.01, 515.94]; dokładny source_span: null.

> • Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.

**first-001 — pending / not_assessable**. Kandydaci: R923; osobny hash powyżej.

R923, pointer `/rules/13`, bajty [243467, 249760); hash zakresu `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Shock Combat involving specified unit types."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmishers alone differs from mixed defense.",
    "Front LI attack exemption is not reciprocal."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    },
    {
      "name": "Skirmisher inflicted-Hits cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    }
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D923pre, G-D923shock

**context-01 — pending / not_assessable**. Kandydaci: R923; osobny hash powyżej.

R923, pointer `/rules/13`, bajty [311816, 318317); hash zakresu `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Shock Combat involving specified unit types."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmishers alone differs from mixed defense.",
    "Front LI attack exemption is not reciprocal."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    },
    {
      "name": "Skirmisher inflicted-Hits cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    }
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D923pre, G-D923shock, GCTX-CRT, GCTX-applicability

### EXP-026 — M-POC5A.3

Dokładny zatwierdzony zakres: PH/HI/LGdefendingFrontvsLI noPreShockevenwithattackermarker;LIstillcheck;reverseexemptionnotapplied

Wyłączenia/niepewności: Nie rozszerzać na Flank/Rear ani inne typy.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, C-9.23-06, bbox [314.995, 519.38, 567.027, 589.38]; dokładny source_span: null.

> • Phalanx (PH), Heavy Infantry (HI), and Legion Infantry (LG)
> units that are attacked from a Front hex by Light Infantry (LI)
> do not undergo a Pre-Shock TQ check even if the attackers have
> SHOCK MUST CHECK TQ markers, though the attacking LI
> still do. The reverse is not true; PH, HI and LG do undergo a
> Pre-Shock TQ check when attacking LI.

**first-001 — pending / not_assessable**. Kandydaci: R923; osobny hash powyżej.

R923, pointer `/rules/13`, bajty [243467, 249760); hash zakresu `c017a74d0ffe7ef54ba4686b7fd4fc52ecffc9bf406143cc8ec56c55eab2a704`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Shock Combat involving specified unit types."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmishers alone differs from mixed defense.",
    "Front LI attack exemption is not reciprocal."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    },
    {
      "name": "Skirmisher inflicted-Hits cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    }
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D923pre, G-D923shock

**context-01 — pending / not_assessable**. Kandydaci: R923; osobny hash powyżej.

R923, pointer `/rules/13`, bajty [311816, 318317); hash zakresu `066ba920859c29d1df823aba213262bcbd5be17764050c3c9cdeaeef6468cdf6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Any Cohesion Hits inflicted by Skirmishers in Shock Combat are halved (round down) with a maximum of 1 Cohesion Hit."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Shock Combat involving specified unit types."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers cannot Shock attack.",
    "Units attacking Skirmishers alone skip Pre-Shock TQ even with SHOCK MUST CHECK TQ markers.",
    "If Skirmisher defends with any other type, choose other type as defender and ignore Skirmisher Size.",
    "Hits inflicted by Skirmishers halved, round down, maximum 1.",
    "PH/HI/LG attacked from Front by LI skip Pre-Shock TQ, even with attacker SHOCK MUST CHECK TQ markers; attacking LI still check.",
    "Reverse not true: PH/HI/LG attacking LI do check."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmishers alone differs from mixed defense.",
    "Front LI attack exemption is not reciprocal."
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Skirmisher inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    },
    {
      "name": "Skirmisher inflicted-Hits cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit",
        "evidence_ids": [
          "E923"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E923"
      ]
    }
  ],
  "evidence_ids": [
    "E923"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D923pre, G-D923shock, GCTX-CRT, GCTX-applicability

### EXP-027 — M-POC5A.3

Dokładny zatwierdzony zakres: SKRouteliminated,facing0MP,no repeat-moveCohesioncost;no blanketterrain/stackingimmunity

Wyłączenia/niepewności: Koszty terenu i pełny stacking nie są wyłączone.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, C-9.24-02, bbox [314.995, 652.88, 503.985, 662.88]; dokładny source_span: null.

> • Skirmishers that Rout are eliminated instead.

Źródło PDF 33, right, C-9.24-04, bbox [314.995, 679.76, 567.113, 713.76]; dokładny source_span: null.

> • See 6.69 for special stacking rules for Skirmishers and Velites.
> Skirmishers can change facing at no MP cost and can move
> more than once per Game Turn without a Cohesion cost.

**first-001 — pending / not_assessable**. Kandydaci: R924; osobny hash powyżej.

R924, pointer `/rules/14`, bajty [249766, 255895); hash zakresu `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers do not make an Elephant Pass-Thru Check (9.11).",
    "the interruption is caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Line exception applies if interruption caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Single-unit interruption condition."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    },
    {
      "name": "line interruption allowance",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Velites or Skirmisher unit per interruption",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    }
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Repeated movement within Game Turn."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D924stack, G-D924line

**context-01 — pending / not_assessable**. Kandydaci: R924; osobny hash powyżej.

R924, pointer `/rules/14`, bajty [318324, 324673); hash zakresu `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers do not make an Elephant Pass-Thru Check (9.11).",
    "the interruption is caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Line exception applies if interruption caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Single-unit interruption condition."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    },
    {
      "name": "line interruption allowance",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Velites or Skirmisher unit per interruption",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    }
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Repeated movement within Game Turn."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D924stack, G-D924line

### EXP-028 — M-POC5A.3

Dokładny zatwierdzony zakres: oneSK/Velitespergap,notoneglobal;two consecutiveunits do notqualify

Wyłączenia/niepewności: To lokalny wyjątek; pozostałe warunki 4.32 wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 33, right, C-9.24-05, bbox [314.995, 717.2, 567.002, 739.2]; dokładny source_span: null.

> • When determining lines for a Line Command (4.32), the pres-
> ence of a Velites or Skirmisher unit does not disrupt the line if

Źródło PDF 34, left, C-9.24-05, bbox [54.0, 54.004, 245.93, 64.004]; dokładny source_span: null.

> the interruption is caused by only one such unit.

Źródło PDF 34, left, X-03, bbox [45.0, 71.224, 297.015, 141.224]; dokładny source_span: null.

> EXAMPLE: There are Hastati in 2808, Velites in 2809, and Has-
> tati in 2810. This would still be eligible to be a line. However,
> if there were Velites in 2809 and 2810 and the Hastati in 2808
> and 2811, the two Hastati would not form a line. If there were
> Hastati in 2808, 2810, and 2812, with Velites in 2809 and 2811,
> the Hastati could form a line.

**first-001 — pending / not_assessable**. Kandydaci: N924ex, R924; osobny hash powyżej.

N924ex, pointer `/nodes/3`, bajty [124483, 126113); hash zakresu `6a3ef8e03ddb0e28dba14bc0413f7a3ed8013ed67c512e6e022456029c02a8f7`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "cases": [
        {
          "Hastati": [
            "2808",
            "2810"
          ],
          "Velites": [
            "2809"
          ],
          "line": "eligible"
        },
        {
          "Hastati": [
            "2808",
            "2811"
          ],
          "Velites": [
            "2809",
            "2810"
          ],
          "line": "not formed by the two Hastati"
        },
        {
          "Hastati": [
            "2808",
            "2810",
            "2812"
          ],
          "Velites": [
            "2809",
            "2811"
          ],
          "line": "could form"
        }
      ]
    },
    "interpretation": "Separated single interruptions may recur; two consecutive intervening Velites fail the illustrated line condition."
  },
  "evidence_ids": [
    "E924ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

R924, pointer `/rules/14`, bajty [249766, 255895); hash zakresu `63cd8fcd0da402f21b02c5c6f6c0aae2edb1f5984e19bc5da61c2a39dc5165db`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers do not make an Elephant Pass-Thru Check (9.11).",
    "the interruption is caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Line exception applies if interruption caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Single-unit interruption condition."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    },
    {
      "name": "line interruption allowance",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Velites or Skirmisher unit per interruption",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    }
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Repeated movement within Game Turn."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D924stack, G-D924line

**context-01 — pending / not_assessable**. Kandydaci: N924ex, R924; osobny hash powyżej.

N924ex, pointer `/nodes/3`, bajty [172182, 173878); hash zakresu `b672863aac81d4eb2fb84ba3e3ca1cae6b8d9c86491f7c4229e84afdeb4e726e`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "cases": [
        {
          "Hastati": [
            "2808",
            "2810"
          ],
          "Velites": [
            "2809"
          ],
          "line": "eligible"
        },
        {
          "Hastati": [
            "2808",
            "2811"
          ],
          "Velites": [
            "2809",
            "2810"
          ],
          "line": "not formed by the two Hastati"
        },
        {
          "Hastati": [
            "2808",
            "2810",
            "2812"
          ],
          "Velites": [
            "2809",
            "2811"
          ],
          "line": "could form"
        }
      ]
    },
    "interpretation": "Separated single interruptions may recur; two consecutive intervening Velites fail the illustrated line condition."
  },
  "evidence_ids": [
    "E924ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

R924, pointer `/rules/14`, bajty [318324, 324673); hash zakresu `6b943eca4f83d51e2ce27c2afa95422cdc3c5d956d16a256aa5c0955f6a71f9d`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Skirmishers do not make an Elephant Pass-Thru Check (9.11).",
    "the interruption is caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Line exception applies if interruption caused by only one such unit."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Skirmishers that Rout are eliminated instead.",
    "No Elephant Pass-Thru Check for Skirmishers.",
    "Special SK/Velites stacking referred to 6.69; Skirmishers may change facing for no MP and move more than once per Game Turn without Cohesion cost.",
    "A single Velites or Skirmisher interrupting a Line Command line does not disrupt it."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Single-unit interruption condition."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    },
    {
      "name": "line interruption allowance",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Velites or Skirmisher unit per interruption",
        "evidence_ids": [
          "E924",
          "E924cont"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E924",
        "E924cont"
      ]
    }
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Repeated movement within Game Turn."
  ],
  "evidence_ids": [
    "E924",
    "E924cont"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D924stack, G-D924line

### EXP-029 — M-POC5A.3

Dokładny zatwierdzony zakres: LCMissileH&DstrictlowerMA,exceptSK;LCArchersfireOW via6.55;fullproceduresunknown

Wyłączenia/niepewności: Sama przewaga MA nie domyka H&D; konieczna procedura 8.3.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, left, C-9.31-01, bbox [45.0, 167.184, 297.005, 201.184]; dokładny source_span: null.

> 9.31 Missile-armed Light Cavalry may use H&D fire (8.3) against
> all units with a lower MA, except Skirmishers. Light Cavalry
> Archers can fire when they use Orderly Withdrawal (6.55).

**first-001 — pending / not_assessable**. Kandydaci: R931; osobny hash powyżej.

R931, pointer `/rules/15`, bajty [255901, 259855); hash zakresu `c203ab22fc5188464f7dabe7f42906f436da91d6c786eab4e76045ad31a63322`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Light Cavalry Archers can fire when they use Orderly Withdrawal (6.55)."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.",
    "LC Archers may fire while using OW."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Missile-armed LC using H&D against lower-MA target."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.",
    "LC Archers may fire while using OW."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmisher targets excluded."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "target MA",
      "value": "< LC MA",
      "unit": {
        "state": "known",
        "value": "MA comparison",
        "evidence_ids": [
          "E931"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E931"
      ]
    }
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Archer fire when using OW."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D931HD, G-D931OW

**context-01 — pending / not_assessable**. Kandydaci: R931; osobny hash powyżej.

R931, pointer `/rules/15`, bajty [324680, 328792); hash zakresu `9a16f1cac6ab3823e712cfd40b143d10ef7906f1848eeb7b1425e3affe652b04`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Light Cavalry Archers can fire when they use Orderly Withdrawal (6.55)."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.",
    "LC Archers may fire while using OW."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Missile-armed LC using H&D against lower-MA target."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Missile-armed LC may H&D fire against any lower-MA unit except Skirmishers.",
    "LC Archers may fire while using OW."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Skirmisher targets excluded."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "target MA",
      "value": "< LC MA",
      "unit": {
        "state": "known",
        "value": "MA comparison",
        "evidence_ids": [
          "E931"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E931"
      ]
    }
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Archer fire when using OW."
  ],
  "evidence_ids": [
    "E931"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D931HD, G-D931OW

### EXP-030 — M-POC5A.3

Dokładny zatwierdzony zakres: attackingLCHitsvsPH/HI/MI/LG/BI halvefloor

Wyłączenia/niepewności: Zależność od AS w przykładzie X-04 wymaga osobnej interpretacji/kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, left, C-9.32-01, bbox [45.0, 208.584, 297.009, 242.584]; dokładny source_span: null.

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).

**first-001 — pending / not_assessable**. Kandydaci: R932; osobny hash powyżej.

R932, pointer `/rules/16`, bajty [259861, 263502); hash zakresu `cfce4763843cd4617670464caf65022de44c34273a2423cb87d74de3dd3c2624`.

transcription:
```json
{
  "state": "known",
  "value": [
    "are halved (round down)."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Halve such inflicted Cohesion Hits, round down.",
  "evidence_ids": [
    "E932"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacking LC inflicts Hits against PH or HI/MI/LG/BI."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Halve such inflicted Cohesion Hits, round down.",
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E932"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E932"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E932"
      ]
    }
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G932, G-D932CRT

**context-01 — pending / not_assessable**. Kandydaci: R932; osobny hash powyżej.

R932, pointer `/rules/16`, bajty [328799, 333292); hash zakresu `064aae5db27a9bda8dd053c7d30ce2d21255bc4236946d1083acd1e2d946dabe`.

transcription:
```json
{
  "state": "known",
  "value": [
    "are halved (round down)."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "9.32 locally halves such LC-inflicted Cohesion Hits, round down. Added Step 4 bullet #4 qualifies reduction: attacker used in determination is LC (8.45), no reduction against a Routed defender, cumulative with bullet #1, which doubles defender result when attacker superior (AS). No actual applicability, base result, combined operation/rounding order or final result established.",
  "evidence_ids": [
    "E932",
    "ECTX846S4-AS",
    "ECTX846S4-LC"
  ],
  "reason": "Unreviewed bounded-context interpretation; original local literal transcription and parameters unchanged.",
  "gap_ids": [
    "G932",
    "G-D932CRT",
    "GCTX-order",
    "GCTX-845"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacking LC inflicts Hits against PH or HI/MI/LG/BI."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Halve such inflicted Cohesion Hits, round down.",
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Supplied 8.46 Step 4 bullet #4: LC reduction does not apply if defender is Routed."
  ],
  "evidence_ids": [
    "ECTX846S4-LC"
  ],
  "reason": "Qualification from added bounded context; not inserted into 9.32 literal transcription.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E932"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E932"
      ]
    }
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G932, G-D932CRT, GCTX-CRT, GCTX-applicability, GCTX-order, GCTX-845

### EXP-031 — M-POC5A.3

Dokładny zatwierdzony zakres: AS/halvingprintedresultconflict requirescontext;no newexceptioninvented

Wyłączenia/niepewności: AS/LC printed result versus halving order and tables remain unresolved.; Ograniczony dowód bazowego AS/CRT; decyzja właściciela o kolejności.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, left, C-9.32-01, bbox [45.0, 208.584, 297.009, 242.584]; dokładny source_span: null.

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).

Źródło PDF 34, left, X-04, bbox [45.0, 249.084, 297.009, 283.084]; dokładny source_span: null.

> EXAMPLE: A Light Cavalry unit with Attack Superiority (AS)
> against a Heavy Infantry unit would use the printed result on
> the Shock CRT.

**first-001 — pending / not_assessable**. Kandydaci: N932ex, R932; osobny hash powyżej.

N932ex, pointer `/nodes/4`, bajty [126119, 127170); hash zakresu `267371a59674521bf587b0dc168aaec6f2a0370510a765edb525f92a91ad022d`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "A Light Cavalry unit with Attack Superiority (AS) against a Heavy Infantry unit would use the printed result on the Shock CRT.",
    "interpretation": {
      "state": "unknown",
      "value": null,
      "evidence_ids": [],
      "reason": "Example relation to halving cannot be resolved from supplied general AS/CRT descriptions.",
      "gap_ids": [
        "G932"
      ]
    }
  },
  "evidence_ids": [
    "E932ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

R932, pointer `/rules/16`, bajty [259861, 263502); hash zakresu `cfce4763843cd4617670464caf65022de44c34273a2423cb87d74de3dd3c2624`.

transcription:
```json
{
  "state": "known",
  "value": [
    "are halved (round down)."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Halve such inflicted Cohesion Hits, round down.",
  "evidence_ids": [
    "E932"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacking LC inflicts Hits against PH or HI/MI/LG/BI."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Halve such inflicted Cohesion Hits, round down.",
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E932"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E932"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E932"
      ]
    }
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G932, G-D932CRT

**context-01 — pending / not_assessable**. Kandydaci: N932ex, R932; osobny hash powyżej.

N932ex, pointer `/nodes/4`, bajty [173885, 175403); hash zakresu `0eb4d362032a4ff5fd28d28ce38de975b77453af7223949fec3d0d816223b27c`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "A Light Cavalry unit with Attack Superiority (AS) against a Heavy Infantry unit would use the printed result on the Shock CRT.",
    "interpretation": {
      "state": "unknown",
      "value": null,
      "evidence_ids": [
        "E932ex",
        "ECTX846S4-AS",
        "ECTX846S4-LC"
      ],
      "reason": "Added source supplies AS 2x defender result and cumulative LC halving, with round down and Routed exception. Exact table, applicability and combined operation/rounding order unavailable; printed-result example retained without declaring executable equality.",
      "gap_ids": [
        "G932",
        "GCTX-order",
        "G-D932CRT"
      ]
    }
  },
  "evidence_ids": [
    "E932ex",
    "ECTX846S4-AS",
    "ECTX846S4-LC"
  ],
  "reason": null,
  "gap_ids": []
}
```

R932, pointer `/rules/16`, bajty [328799, 333292); hash zakresu `064aae5db27a9bda8dd053c7d30ce2d21255bc4236946d1083acd1e2d946dabe`.

transcription:
```json
{
  "state": "known",
  "value": [
    "are halved (round down)."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "9.32 locally halves such LC-inflicted Cohesion Hits, round down. Added Step 4 bullet #4 qualifies reduction: attacker used in determination is LC (8.45), no reduction against a Routed defender, cumulative with bullet #1, which doubles defender result when attacker superior (AS). No actual applicability, base result, combined operation/rounding order or final result established.",
  "evidence_ids": [
    "E932",
    "ECTX846S4-AS",
    "ECTX846S4-LC"
  ],
  "reason": "Unreviewed bounded-context interpretation; original local literal transcription and parameters unchanged.",
  "gap_ids": [
    "G932",
    "G-D932CRT",
    "GCTX-order",
    "GCTX-845"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacking LC inflicts Hits against PH or HI/MI/LG/BI."
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Halve such inflicted Cohesion Hits, round down.",
  "evidence_ids": [
    "E932"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Supplied 8.46 Step 4 bullet #4: LC reduction does not apply if defender is Routed."
  ],
  "evidence_ids": [
    "ECTX846S4-LC"
  ],
  "reason": "Qualification from added bounded context; not inserted into 9.32 literal transcription.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "inflicted-Hits scaling",
      "value": "1/2, round down",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E932"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E932"
      ]
    }
  ],
  "evidence_ids": [
    "E932"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G932, G-D932CRT, GCTX-CRT, GCTX-applicability, GCTX-order, GCTX-845

### EXP-032 — M-POC5A.3

Dokładny zatwierdzony zakres: movingFrontPHDefense2Lperqualifyingflank,HI1Lperflank;excludestartadjacentstayed,FlankRear,anyPHattacker

Wyłączenia/niepewności: Lokalny shift, nie pełny wynik CRT bez tabeli.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, left, C-9.41-01, bbox [45.0, 309.044, 297.032, 427.044]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R941; osobny hash powyżej.

R941, pointer `/rules/17`, bajty [263508, 268383); hash zakresu `112f98003ed54c0f8f09d2d00327263a8c7c577c036536d988707561e7dbac94`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the attacker is Heavy Infantry (any Class), the shift is 1L instead."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacker moves adjacent then Shock attacks Phalanx from defender Front.",
    "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Only moving attacks; not attacker starting adjacent and staying.",
    "No Flank/Rear attacks.",
    "No application if any attacker is a Phalanx."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "ordinary shift",
      "value": "2L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    },
    {
      "name": "HI shift",
      "value": "1L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    }
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Moves adjacent then attacks; starting-adjacent stationary attacks excluded."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D941CRT

**context-01 — pending / not_assessable**. Kandydaci: R941; osobny hash powyżej.

R941, pointer `/rules/17`, bajty [333299, 338353); hash zakresu `554b4ecd3a2ad5a80f0fa28cafc3c8b8f0528efdd7418e7d1999840cae58b045`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the attacker is Heavy Infantry (any Class), the shift is 1L instead."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacker moves adjacent then Shock attacks Phalanx from defender Front.",
    "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Only moving attacks; not attacker starting adjacent and staying.",
    "No Flank/Rear attacks.",
    "No application if any attacker is a Phalanx."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "ordinary shift",
      "value": "2L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    },
    {
      "name": "HI shift",
      "value": "1L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    }
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Moves adjacent then attacks; starting-adjacent stationary attacks excluded."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D941CRT

### EXP-033 — M-POC5A.3

Dokładny zatwierdzony zakres: scenarioDDeligibilitylistnecessary,missingblocksSIT11

Wyłączenia/niepewności: Scenario-specific Double-Depth eligibility list is required.; Wybrany scenariusz z listą uprawnionych jednostek.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, N-09-S2, bbox [319.0, 70.3, 563.01, 116.3]; dokładny source_span: "Eligible units are listed in the scenario-specific rules.".

> DESIGN NOTE: To increase the crushing pressure of the Pha-
> lanxes, post-Alexandrian commanders using the Macedonian
> system often implemented a formation which doubled their
> depth. Eligible units are listed in the scenario-specific rules.

Źródło PDF 34, right, C-9.51-01, bbox [315.0, 125.54, 567.115, 243.54]; dokładny source_span: null.

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

Źródło PDF 34, right, X-06, bbox [315.0, 701.54, 533.58, 711.54]; dokładny source_span: null.

> EXAMPLE: See the scenario rules for Cynoscephalae.

**first-001 — pending / not_assessable**. Kandydaci: N953ex, N95design, R951, R95note; osobny hash powyżej.

N953ex, pointer `/nodes/6`, bajty [128320, 128971); hash zakresu `32ad4997be80003431ce7d9782486b53cafcb6a9bd4a6ba63f26a0091bbff9b9`.

content:
```json
{
  "state": "known",
  "value": "See the scenario rules for Cynoscephalae; example content is not supplied.",
  "evidence_ids": [
    "E953ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

N95design, pointer `/nodes/26`, bajty [143799, 144517); hash zakresu `befa3bbc8e95ad44cd60c24834e7ac7c76df7271a4c228979bb40b3ec394ab04`.

content:
```json
{
  "state": "known",
  "value": "Post-Alexandrian Macedonian formation rationale. Scenario eligibility requirement owned by R95note.",
  "evidence_ids": [
    "E95design"
  ],
  "reason": null,
  "gap_ids": []
}
```

R951, pointer `/rules/19`, bajty [271660, 276889); hash zakresu `6ed20d621c4094781ff1689567d941ab7d22e764fe9a78ef1686795326e5e7a7`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This completes the movement for both units for that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible Phalanxes; “back” PH begins directly behind “front” PH.",
    "Individual Order or Line Command directly from OC."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E951"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "DD stack size",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Phalanx units per hex",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    },
    {
      "name": "formation additional cost",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MP plus normal terrain cost",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    }
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starting position at start of back PH movement.",
    "No further movement for either unit that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

R95note, pointer `/rules/18`, bajty [268389, 271654); hash zakresu `119eed8150bbbc291da6700cfdd1cf837f904262b76165126e4b13fd265bbf7c`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Eligible units are listed in the scenario-specific rules."
  ],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Double-Depth eligible units are determined by scenario-specific rules.",
  "evidence_ids": [
    "E95note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Double-Depth eligible units are determined by scenario-specific rules.",
  "evidence_ids": [
    "E95note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D95scenario, G-D951OC, G-D951terrain, G-D953scenario

**context-01 — pending / not_assessable**. Kandydaci: N953ex, N95design, R951, R95note; osobny hash powyżej.

N953ex, pointer `/nodes/6`, bajty [176598, 177276); hash zakresu `32059fb98dda21cbaacbf3674087807d1696268d8d9a7236e4b6220eb6b7380f`.

content:
```json
{
  "state": "known",
  "value": "See the scenario rules for Cynoscephalae; example content is not supplied.",
  "evidence_ids": [
    "E953ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

N95design, pointer `/nodes/26`, bajty [192684, 193429); hash zakresu `f17c97f5b1d2fb4d5811fb18481d7ff3dfbe32f09a24af8c9e2568f554fabe8c`.

content:
```json
{
  "state": "known",
  "value": "Post-Alexandrian Macedonian formation rationale. Scenario eligibility requirement owned by R95note.",
  "evidence_ids": [
    "E95design"
  ],
  "reason": null,
  "gap_ids": []
}
```

R951, pointer `/rules/19`, bajty [341748, 347170); hash zakresu `5a34602f7f460a66fe124c94424a27e1ac98d03e9da186e73f8c2763358bf313`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This completes the movement for both units for that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible Phalanxes; “back” PH begins directly behind “front” PH.",
    "Individual Order or Line Command directly from OC."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E951"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "DD stack size",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Phalanx units per hex",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    },
    {
      "name": "formation additional cost",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MP plus normal terrain cost",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    }
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starting position at start of back PH movement.",
    "No further movement for either unit that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

R95note, pointer `/rules/18`, bajty [338360, 341741); hash zakresu `45f74a06c6c69fbd84bd9aff1a0d58e7f58f502096e2ab3bd83ae51d84aedf49`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Eligible units are listed in the scenario-specific rules."
  ],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Double-Depth eligible units are determined by scenario-specific rules.",
  "evidence_ids": [
    "E95note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Double-Depth eligible units are determined by scenario-specific rules.",
  "evidence_ids": [
    "E95note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E95note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D95scenario, G-D951OC, G-D951terrain, G-D953scenario

### EXP-034 — M-POC5A.3

Dokładny zatwierdzony zakres: formingDDIOorLCdirectOC,backstartsbehindfront,terraincost+1MP,backunderfront,endbothmovementthisphase

Wyłączenia/niepewności: Eligibility, OC i koszt terenu jako osobne potrzebne fakty.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, C-9.51-01, bbox [315.0, 125.54, 567.115, 243.54]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R951; osobny hash powyżej.

R951, pointer `/rules/19`, bajty [271660, 276889); hash zakresu `6ed20d621c4094781ff1689567d941ab7d22e764fe9a78ef1686795326e5e7a7`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This completes the movement for both units for that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible Phalanxes; “back” PH begins directly behind “front” PH.",
    "Individual Order or Line Command directly from OC."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E951"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "DD stack size",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Phalanx units per hex",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    },
    {
      "name": "formation additional cost",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MP plus normal terrain cost",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    }
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starting position at start of back PH movement.",
    "No further movement for either unit that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D951OC, G-D951terrain

**context-01 — pending / not_assessable**. Kandydaci: R951; osobny hash powyżej.

R951, pointer `/rules/19`, bajty [341748, 347170); hash zakresu `5a34602f7f460a66fe124c94424a27e1ac98d03e9da186e73f8c2763358bf313`.

transcription:
```json
{
  "state": "known",
  "value": [
    "This completes the movement for both units for that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible Phalanxes; “back” PH begins directly behind “front” PH.",
    "Individual Order or Line Command directly from OC."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Double-Depth permits two PH in one hex.",
    "Back PH moves into front PH hex for normal terrain cost plus 1 MP, placed underneath front PH.",
    "Movement of both units complete for Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E951"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "DD stack size",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Phalanx units per hex",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    },
    {
      "name": "formation additional cost",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MP plus normal terrain cost",
        "evidence_ids": [
          "E951"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E951"
      ]
    }
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starting position at start of back PH movement.",
    "No further movement for either unit that Orders Phase."
  ],
  "evidence_ids": [
    "E951"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D951OC, G-D951terrain

### EXP-035 — M-POC5A.3

Dokładny zatwierdzony zakres: OCordersonly,2IOwhenIOmovement,PAWvia6.8,noWheel/Reverse/Column;unstacktopmoves,bottomstays,IOorLCasabove;fullLCprocedure notclosed

Wyłączenia/niepewności: Procedury zewnętrzne 6.8/6.44/6.45/6.7 i orders pozostają potrzebne dla pełnego wykonania.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, C-9.52-02, bbox [315.0, 277.82, 515.91, 287.82]; dokładny source_span: null.

> • The units may receive orders only from the OC.

Źródło PDF 34, right, C-9.52-03, bbox [315.0, 291.26, 567.011, 325.26]; dokładny source_span: null.

> • They may move as one unit, but it takes 2 Individual Orders
> (when using Individual Orders) to move both units together.
> They may use Pre-Arranged Withdrawal (6.8).

Źródło PDF 34, right, C-9.52-04, bbox [315.0, 328.7, 567.008, 374.7]; dokładny source_span: null.

> • The units may not Wheel (6.44), Reverse (6.45), or use Col-
> umn (6.7). Unstacking requires an Individual Order or Line
> Command as above, at which time the top unit moves off at
> normal costs. The bottom unit must remain in place.

**first-001 — pending / not_assessable**. Kandydaci: R952; osobny hash powyżej.

R952, pointer `/rules/20`, bajty [276895, 283151); hash zakresu `d3c03f8437c1acf3a3540923b725ecef09aac6ba7a23ecba4b82837c59d2d011`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The units always use their 4 MA; they never use their 5 MA for anything."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Units in Double Depth."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E952"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "joint movement cost",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Individual Orders",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "usable MA",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "excluded MA",
      "value": 5,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    }
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D952PAW, G-D952wheel, G-D952reverse, G-D952column

**context-01 — pending / not_assessable**. Kandydaci: R952; osobny hash powyżej.

R952, pointer `/rules/20`, bajty [347177, 353653); hash zakresu `bbf568a4a71dbd5e7ae685da23f7c7d5c0527aab3e5650cf8fb3695982a880d3`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The units always use their 4 MA; they never use their 5 MA for anything."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Units in Double Depth."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E952"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "joint movement cost",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Individual Orders",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "usable MA",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "excluded MA",
      "value": 5,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    }
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D952PAW, G-D952wheel, G-D952reverse, G-D952column

### EXP-036 — M-POC5A.3

Dokładny zatwierdzony zakres: readyDDMA4never5,movementHittoeach,nounitthroughorintoreadyDD;forming9.51separate

Wyłączenia/niepewności: Przypadek formowania DD z 9.51 wymaga rozróżnienia etapu od gotowej formacji.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, C-9.52-05, bbox [315.0, 378.14, 567.551, 412.14]; dokładny source_span: null.

> • The units always use their 4 MA; they never use their 5 MA
> for anything. For any movement that would incur a Cohesion
> Hit, both units incur the Hit.

Źródło PDF 34, right, C-9.52-06, bbox [315.0, 415.58, 567.02, 437.58]; dokładny source_span: null.

> • No unit, of any type, may ever move through or into a Double
> Depth stack. Treat them as impassable terrain.

**first-001 — pending / not_assessable**. Kandydaci: R952; osobny hash powyżej.

R952, pointer `/rules/20`, bajty [276895, 283151); hash zakresu `d3c03f8437c1acf3a3540923b725ecef09aac6ba7a23ecba4b82837c59d2d011`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The units always use their 4 MA; they never use their 5 MA for anything."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Units in Double Depth."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E952"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "joint movement cost",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Individual Orders",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "usable MA",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "excluded MA",
      "value": 5,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    }
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D952PAW, G-D952wheel, G-D952reverse, G-D952column

**context-01 — pending / not_assessable**. Kandydaci: R952; osobny hash powyżej.

R952, pointer `/rules/20`, bajty [347177, 353653); hash zakresu `bbf568a4a71dbd5e7ae685da23f7c7d5c0527aab3e5650cf8fb3695982a880d3`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The units always use their 4 MA; they never use their 5 MA for anything."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Units in Double Depth."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Orders only from OC.",
    "Move as one; 2 Individual Orders if using Individual Orders; may Pre-Arranged Withdraw.",
    "Cannot Wheel, Reverse or use Column.",
    "Unstack with Individual Order or LC as above; top moves for normal costs, bottom stays.",
    "Always use 4 MA, never 5 MA; both suffer any movement Cohesion Hit.",
    "No unit of any type may enter or pass through DD stack; impassable terrain."
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E952"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "joint movement cost",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Individual Orders",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "usable MA",
      "value": 4,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    },
    {
      "name": "excluded MA",
      "value": 5,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E952"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E952"
      ]
    }
  ],
  "evidence_ids": [
    "E952"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D952PAW, G-D952wheel, G-D952reverse, G-D952column

### EXP-037 — M-POC5A.3

Dokładny zatwierdzony zakres: combinedSize,topTQunlessRearthenbottom;otherchecksifselectedunitincursHits;actualTQvaluesunknown

Wyłączenia/niepewności: Ogólny test TQ i inne modyfikatory poza lokalną selekcją wymagają celu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, C-9.53-02, bbox [315.0, 471.68, 475.37, 481.68]; dokładny source_span: null.

> • The Sizes of both units are combined.

Źródło PDF 34, right, C-9.53-03, bbox [315.0, 485.12, 567.017, 519.12]; dokładny source_span: null.

> • Only the top unit is used for TQ checks (unless attacked from
> the rear, in which case it’s the bottom unit). However, if that
> unit incurs any Cohesion Hits, then the other unit checks.

**first-001 — pending / not_assessable**. Kandydaci: R953; osobny hash powyżej.

R953, pointer `/rules/21`, bajty [283157, 290596); hash zakresu `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D953pre

**context-01 — pending / not_assessable**. Kandydaci: R953; osobny hash powyżej.

R953, pointer `/rules/21`, bajty [353660, 361365); hash zakresu `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D953pre

### EXP-038 — M-POC5A.3

Dokładny zatwierdzony zakres: enemydefendingagainstDD+1PreShock,DDdefending-1;9.41conditionsstillapply

Wyłączenia/niepewności: R-9.53→R-9.41 to użycie warunkowej modyfikacji, nie odwrotny kierunek.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, C-9.53-04, bbox [315.0, 522.56, 567.002, 544.56]; dokładny source_span: null.

> • Units defending against a Shock attack by units in Double
> Depth incur a +1 DRM to their Pre-Shock TQ check die rolls.

Źródło PDF 34, right, C-9.53-05, bbox [315.0, 548.0, 567.102, 570.0]; dokładny source_span: null.

> • Defending units at Double Depth earn a –1 DRM to their Pre-
> Shock TQ check die rolls. Phalanx Defense (9.41) also applies.

Źródło PDF 34, left, C-9.41-01, bbox [45.0, 309.044, 297.032, 427.044]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R941, R953; osobny hash powyżej.

R941, pointer `/rules/17`, bajty [263508, 268383); hash zakresu `112f98003ed54c0f8f09d2d00327263a8c7c577c036536d988707561e7dbac94`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the attacker is Heavy Infantry (any Class), the shift is 1L instead."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacker moves adjacent then Shock attacks Phalanx from defender Front.",
    "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Only moving attacks; not attacker starting adjacent and staying.",
    "No Flank/Rear attacks.",
    "No application if any attacker is a Phalanx."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "ordinary shift",
      "value": "2L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    },
    {
      "name": "HI shift",
      "value": "1L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    }
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Moves adjacent then attacks; starting-adjacent stationary attacks excluded."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

R953, pointer `/rules/21`, bajty [283157, 290596); hash zakresu `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D941CRT, G-D953pre

**context-01 — pending / not_assessable**. Kandydaci: R941, R953; osobny hash powyżej.

R941, pointer `/rules/17`, bajty [333299, 338353); hash zakresu `554b4ecd3a2ad5a80f0fa28cafc3c8b8f0528efdd7418e7d1999840cae58b045`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the attacker is Heavy Infantry (any Class), the shift is 1L instead."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Attacker moves adjacent then Shock attacks Phalanx from defender Front.",
    "Defender Flank hex occupied by another friendly PH or in friendly PH ZOC."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Defender earns 2L CRT shift per qualifying Flank hex; Heavy Infantry attacker of any class reduces shift to 1L.",
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Only moving attacks; not attacker starting adjacent and staying.",
    "No Flank/Rear attacks.",
    "No application if any attacker is a Phalanx."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "ordinary shift",
      "value": "2L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    },
    {
      "name": "HI shift",
      "value": "1L",
      "unit": {
        "state": "known",
        "value": "Shock CRT columns left per qualifying Flank hex",
        "evidence_ids": [
          "E941"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E941"
      ]
    }
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Moves adjacent then attacks; starting-adjacent stationary attacks excluded."
  ],
  "evidence_ids": [
    "E941"
  ],
  "reason": null,
  "gap_ids": []
}
```

R953, pointer `/rules/21`, bajty [353660, 361365); hash zakresu `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D941CRT, G-D953pre

### EXP-039 — M-POC5A.3

Dokładny zatwierdzony zakres: FlankReardefenderShockHits3xinstead2x,equalallocationoddtop;missileHits topunlessRearthenbottom

Wyłączenia/niepewności: Bazowy wynik i kolejność wobec innych mnożników muszą być dostarczone/zweryfikowane.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, C-9.53-06, bbox [315.0, 573.44, 567.011, 607.44]; dokładny source_span: null.

> • If a Double Depth stack is Shock attacked from a Flank or
> Rear hex, the defender Cohesion Hits are tripled (3x) instead
> of doubled.

Źródło PDF 34, right, C-9.53-07, bbox [315.0, 610.88, 567.07, 656.88]; dokładny source_span: null.

> • Cohesion Hits from Shock are distributed equally between the
> two units, with any odd Hits going to the top unit. Cohesion Hits
> from Missile Fire Hits apply only to the top unit unless fire is
> through a Rear hex, in which case Hits apply to the bottom unit.

**first-001 — pending / not_assessable**. Kandydaci: R953; osobny hash powyżej.

R953, pointer `/rules/21`, bajty [283157, 290596); hash zakresu `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D953pre

**context-01 — pending / not_assessable**. Kandydaci: R953; osobny hash powyżej.

R953, pointer `/rules/21`, bajty [353660, 361365); hash zakresu `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D953pre

### EXP-040 — M-POC5A.3

Dokładny zatwierdzony zakres: When one PH of DD Routs, both Rout and retreat separately. Eliminate each PH individually if it cannot complete legal Rout movement; the other may perform its own legal Rout if possible. Actual geometry, 6.69/10.22, order/shared sole destination and later D1 result are unclosed. Local 10.24/25/23 context is supporting evidence, not an additional scoring unit.

Wyłączenia/niepewności: Per-unit elimination reading is confirmed; real geometry, 6.69/10.22, legal ordering and a shared sole destination remain unresolved.; Legalne heksy retreat i zakres końcowego the unit wymagają kontekstu przy konfliktach.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 34, right, C-9.53-08, bbox [315.0, 660.32, 567.03, 694.32]; dokładny source_span: null.

> • If either unit in the stack routs, they both rout. The units must
> retreat to separate hexes. If this is not possible, the unit is
> eliminated instead.

**first-001 — pending / not_assessable**. Kandydaci: R953; osobny hash powyżej.

R953, pointer `/rules/21`, bajty [283157, 290596); hash zakresu `ab814cde16108d9e0cd10c4835e3c1f1c9330a7745a665a1ecd0407e9459f477`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D953pre

**context-01 — pending / not_assessable**. Kandydaci: R953; osobny hash powyżej.

R953, pointer `/rules/21`, bajty [353660, 361365); hash zakresu `8ad51a03751b5b4e793d603193a0a5f934f6a36e6181f10f5ab8e5e7ac724a29`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If either unit in the stack routs, they both rout."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "unknown",
  "value": null,
  "evidence_ids": [],
  "reason": "Combat effects except final elimination scope are represented in action_effect; singular “the unit” leaves elimination cardinality unresolved.",
  "gap_ids": [
    "G953"
  ]
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Double Depth combat."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combine Sizes.",
    "Use top for TQ checks, bottom if rear-attacked; if checked unit takes any Hits, other unit checks.",
    "Defenders against DD Shock incur +1 Pre-Shock DRM.",
    "DD defenders get –1 Pre-Shock DRM; Phalanx Defense also applies.",
    "DD defender Hits from Flank/Rear Shock tripled, not doubled.",
    "Shock Hits divided equally; odd Hits to top. Missile Hits top except Rear fire hits bottom.",
    "Either rout means both rout; retreat to separate hexes; if not possible source says “the unit is eliminated instead”."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Rear attack uses bottom TQ/check and rear fire bottom Hits.",
    "Flank/Rear Shock uses 3x.",
    "Odd Shock Hit to top."
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "defender versus DD Pre-Shock modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "DD defender Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Flank/Rear Shock multiplier",
      "value": 3,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "replaced multiplier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "times defender Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    },
    {
      "name": "Shock allocation",
      "value": "equal, odd to top",
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E953"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E953"
      ]
    }
  ],
  "evidence_ids": [
    "E953"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G953, G-D953pre

### EXP-041 — M-POC5A.3

Dokładny zatwierdzony zakres: ruleofthumb2Romaninfantry sameborderwithexceptions;notfulllegaleligibility;move2IO,1IOifstackedOCgivingorders,1LCifbotheligible

Wyłączenia/niepewności: Pełny stacking chart i eligibility nie są dowiedzione regułą thumb.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, left, C-9.61-01, bbox [45.0, 176.7, 297.03, 282.7]; dokładny source_span: null.

> 9.61 See the Stacking Charts for a summary of the legionary
> stacking advantages. For Romans, the rule of thumb is that two
> Roman infantry units of the same border color can stack without
> penalty. There are exceptions, such as Velites. A Roman stack
> may move together when necessary or desired. It takes two In-
> dividual Orders to move two stacked units (only one, if stacked
> with the OC, and he is giving the orders), but only one LC, if they
> are both eligible. Roman infantry units are also allowed spaces
> between them when determining lines; see 4.32.

**first-001 — pending / not_assessable**. Kandydaci: R961; osobny hash powyżej.

R961, pointer `/rules/22`, bajty [290602, 296910); hash zakresu `6b8470e5e55b69e23271008267a8bbe41527657e5a35dcdbfead196e82bce062`.

transcription:
```json
{
  "state": "known",
  "value": [
    "There are exceptions, such as Velites."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Consult Stacking Charts for legionary advantages.",
    "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.",
    "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.",
    "Roman infantry may have spaces when determining lines under 4.32."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E961"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Consult Stacking Charts for legionary advantages.",
    "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.",
    "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.",
    "Roman infantry may have spaces when determining lines under 4.32."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Velites and other exceptions not enumerated here.",
    "1 Individual Order with ordering OC stacked; 1 LC if both eligible."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "usual stack",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Roman infantry units",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    },
    {
      "name": "joint movement",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Individual Orders",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    },
    {
      "name": "OC-stacked joint movement",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Individual Order",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    },
    {
      "name": "eligible joint movement",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Line Command",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    }
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D961stack, G-D961line

**context-01 — pending / not_assessable**. Kandydaci: R961; osobny hash powyżej.

R961, pointer `/rules/22`, bajty [361372, 367903); hash zakresu `bcb032de73b22e12958d3e579d0d9c7a13da82705652c8059b17135e5ec59a74`.

transcription:
```json
{
  "state": "known",
  "value": [
    "There are exceptions, such as Velites."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Consult Stacking Charts for legionary advantages.",
    "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.",
    "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.",
    "Roman infantry may have spaces when determining lines under 4.32."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E961"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Consult Stacking Charts for legionary advantages.",
    "Rule of thumb: two Roman infantry with same border color stack without penalty, with exceptions such as Velites.",
    "Roman stack may move together; takes 2 Individual Orders, or 1 if stacked with OC giving orders; 1 LC if both eligible.",
    "Roman infantry may have spaces when determining lines under 4.32."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Velites and other exceptions not enumerated here.",
    "1 Individual Order with ordering OC stacked; 1 LC if both eligible."
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "usual stack",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Roman infantry units",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    },
    {
      "name": "joint movement",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "Individual Orders",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    },
    {
      "name": "OC-stacked joint movement",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Individual Order",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    },
    {
      "name": "eligible joint movement",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Line Command",
        "evidence_ids": [
          "E961"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E961"
      ]
    }
  ],
  "evidence_ids": [
    "E961"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D961stack, G-D961line

### EXP-042 — M-POC5A.3

Dokładny zatwierdzony zakres: combineSize,otherratingsespeciallyTQtop,eachunitowntestusingtopTQ,onlytopfire,bothShock samehex;automaticHitsto each;Shockallocationdelegated8.46Step4/10.13

Wyłączenia/niepewności: Rozdział 9 nie domyka alokacji Shock Hits; 10.13 jest kontekstem, 6.68 nieprzejrzane.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, left, C-9.62-01, bbox [45.0, 290.1, 297.017, 372.1]; dokładny source_span: null.

> 9.62 Stacked Roman units combine their Size when attacking or
> defending, but all other ratings, especially TQ, are those of the
> top unit. Stacked Romans must Shock attack the same hex; see
> 8.42. Only the top unit may fire. Each unit makes its own TQ
> check but uses the TQ of the top unit. Automatic Cohesion Hits
> (6.68) are applied to each unit in the stack. Cohesion Hits from
> Shock resolution 8.46 Step 4 are allocated per 10.13.

**first-001 — pending / not_assessable**. Kandydaci: R962; osobny hash powyżej.

R962, pointer `/rules/23`, bajty [296916, 301592); hash zakresu `ae11cd4ac05b78d7fd21fa35572b242282d9da3c6d8f9663a0bca89e32363e44`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each unit makes its own TQ check but uses the TQ of the top unit."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Combined Size on attack/defense; other ratings including TQ from top.",
    "Stack must Shock attack same hex; only top fires.",
    "Each unit rolls its own TQ check using top TQ.",
    "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Stacked Roman units."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combined Size on attack/defense; other ratings including TQ from top.",
    "Stack must Shock attack same hex; only top fires.",
    "Each unit rolls its own TQ check using top TQ.",
    "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E962"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E962"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D962target, G-D962auto, G-D962shock

**context-01 — pending / not_assessable**. Kandydaci: R962; osobny hash powyżej.

R962, pointer `/rules/23`, bajty [367910, 372751); hash zakresu `661e95a04df56028793a45c4b225c06f3a371ebc9314efc42611fd5c3c3a451d`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each unit makes its own TQ check but uses the TQ of the top unit."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Combined Size on attack/defense; other ratings including TQ from top.",
    "Stack must Shock attack same hex; only top fires.",
    "Each unit rolls its own TQ check using top TQ.",
    "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Stacked Roman units."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Combined Size on attack/defense; other ratings including TQ from top.",
    "Stack must Shock attack same hex; only top fires.",
    "Each unit rolls its own TQ check using top TQ.",
    "Automatic Hits under 6.68 apply to each; Shock 8.46 Step 4 Hits allocated per 10.13."
  ],
  "evidence_ids": [
    "E962"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E962"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E962"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D962target, G-D962auto, G-D962shock, GCTX-CRT, GCTX-applicability

### EXP-043 — M-POC5A.3

Dokładny zatwierdzony zakres: differentbordercolors ORsamecolordifferentclasses,+1DRMtoallTQchecks

Wyłączenia/niepewności: Typy i kolory muszą być znane z danych jednostek.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, left, C-9.63-01, bbox [45.0, 379.5, 297.011, 413.5]; dokładny source_span: null.

> 9.63 For stacked Roman units with different border colors, or of
> the same border color and different classes, there is a +1 DRM
> to all TQ checks.

**first-001 — pending / not_assessable**. Kandydaci: R963; osobny hash powyżej.

R963, pointer `/rules/24`, bajty [301598, 305296); hash zakresu `58a813b6aaba0b0d25a66c3b7a3fd2c3a6bcf811684e8bf617f574c0430f29f8`.

transcription:
```json
{
  "state": "known",
  "value": [
    "there is a +1 DRM to all TQ checks."
  ],
  "evidence_ids": [
    "E963"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "+1 DRM to all TQ checks.",
  "evidence_ids": [
    "E963"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Stacked Romans with different border colors OR same border color but different classes."
  ],
  "evidence_ids": [
    "E963"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "+1 DRM to all TQ checks.",
  "evidence_ids": [
    "E963"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E963"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "stack TQ modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E963"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E963"
      ]
    }
  ],
  "evidence_ids": [
    "E963"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D963TQ

**context-01 — pending / not_assessable**. Kandydaci: R963; osobny hash powyżej.

R963, pointer `/rules/24`, bajty [372758, 376599); hash zakresu `4fbf3c5ea3e740875782caf600b70a3974f0e7f9ff7bda1b8dea4c9c2261a9ea`.

transcription:
```json
{
  "state": "known",
  "value": [
    "there is a +1 DRM to all TQ checks."
  ],
  "evidence_ids": [
    "E963"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "+1 DRM to all TQ checks.",
  "evidence_ids": [
    "E963"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Stacked Romans with different border colors OR same border color but different classes."
  ],
  "evidence_ids": [
    "E963"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "+1 DRM to all TQ checks.",
  "evidence_ids": [
    "E963"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E963"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "stack TQ modifier",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E963"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E963"
      ]
    }
  ],
  "evidence_ids": [
    "E963"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D963TQ

### EXP-044 — M-POC5A.3

Dokładny zatwierdzony zakres: stackorderchangeIOonly,notmovement/LC;facingcanLC;onlytopmovesifmovingoneunitfromstack

Wyłączenia/niepewności: Nie zastosować zwykłego unstack do MLE bez sprawdzenia szczególnej reguły.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, left, C-9.64-01, bbox [45.0, 420.9, 297.04, 478.9]; dokładny source_span: null.

> 9.64 Roman Stacking order may be changed/switched only by
> an Individual Order; it may not be part of movement or a Line
> Command, although facing may be changed by LC. If the player
> desires to move only one unit from a stack, only the top unit
> may move.

**first-001 — pending / not_assessable**. Kandydaci: R964; osobny hash powyżej.

R964, pointer `/rules/25`, bajty [305302, 309224); hash zakresu `0011f5a4a5cd234d3f5c62f4b8510d023a26e8b43bc154f1edd2acb291c5b9ea`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the player desires to move only one unit from a stack, only the top unit may move."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Stack order may be switched only by Individual Order, never as movement or LC.",
    "Facing may change by LC.",
    "If moving one unit out of stack, only top can move."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E964"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Stack order may be switched only by Individual Order, never as movement or LC.",
    "Facing may change by LC.",
    "If moving one unit out of stack, only top can move."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Facing may change by LC despite stacking-order LC prohibition."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E964"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D964order

**context-01 — pending / not_assessable**. Kandydaci: R964; osobny hash powyżej.

R964, pointer `/rules/25`, bajty [376606, 380671); hash zakresu `e4530c490edde7d54d4ac9fd06686c4a0312813eb32d7107cf885172e47c8fe8`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the player desires to move only one unit from a stack, only the top unit may move."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Stack order may be switched only by Individual Order, never as movement or LC.",
    "Facing may change by LC.",
    "If moving one unit out of stack, only top can move."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E964"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Stack order may be switched only by Individual Order, never as movement or LC.",
    "Facing may change by LC.",
    "If moving one unit out of stack, only top can move."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Facing may change by LC despite stacking-order LC prohibition."
  ],
  "evidence_ids": [
    "E964"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E964"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D964order

### EXP-045 — M-POC5A.3

Dokładny zatwierdzony zakres: Romaninfantryfacing1MPanynumbervertices;notMLEfacingrule

Wyłączenia/niepewności: Nie rozszerzać tej wartości na MLE, które zachowuje facing.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, left, C-9.65-01, bbox [45.0, 486.3, 297.1, 508.3]; dokładny source_span: null.

> 9.65 Roman infantry pay 1 MP cost for changing facing, but,
> unlike most other units, they may change any number of vertices.

**first-001 — pending / not_assessable**. Kandydaci: R965; osobny hash powyżej.

R965, pointer `/rules/26`, bajty [309230, 312838); hash zakresu `e38853213823da0429d224631ca49efed539fcf423497ce1ab8828e28f8fc77a`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Roman infantry pay 1 MP cost for changing facing, but, unlike most other units, they may change any number of vertices."
  ],
  "evidence_ids": [
    "E965"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Roman infantry change facing through any number of vertices for 1 MP.",
  "evidence_ids": [
    "E965"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E965"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Roman infantry change facing through any number of vertices for 1 MP.",
  "evidence_ids": [
    "E965"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E965"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing change",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MP for any number of vertices",
        "evidence_ids": [
          "E965"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E965"
      ]
    }
  ],
  "evidence_ids": [
    "E965"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

**context-01 — pending / not_assessable**. Kandydaci: R965; osobny hash powyżej.

R965, pointer `/rules/26`, bajty [380678, 384416); hash zakresu `19ae59d6e959efb3e6c037af8605714eddab51c425881ad764356addf2f199d3`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Roman infantry pay 1 MP cost for changing facing, but, unlike most other units, they may change any number of vertices."
  ],
  "evidence_ids": [
    "E965"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Roman infantry change facing through any number of vertices for 1 MP.",
  "evidence_ids": [
    "E965"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E965"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Roman infantry change facing through any number of vertices for 1 MP.",
  "evidence_ids": [
    "E965"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E965"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "facing change",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MP for any number of vertices",
        "evidence_ids": [
          "E965"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E965"
      ]
    }
  ],
  "evidence_ids": [
    "E965"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

### EXP-046 — M-POC5A.3

Dokładny zatwierdzony zakres: topunits instackssameLine sideways tovacantflankClearoutsideenemyZOC,facingunchanged;unstackonly,notstackingTogether;diagramOriginaltop/Afterbottomillustrative

Wyłączenia/niepewności: Same Line przez4.32, Clear i ZOC wymagają danych/procedur; grafika nie daje ogólnego prawa do dowolnej strony.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, left, C-9.66-01-S1, bbox [44.997, 678.9, 297.009, 736.9]; dokładny source_span: "9.66 Manipular Line Extension: Stacked Roman units with\nunoccupied flank hexes can extend their line as part of a Line\nCommand or in reaction to enemy movement, instead of using\nOrderly Withdrawal.".

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Źródło PDF 35, right, C-9.66-01-S1, bbox [314.997, 54.01, 567.03, 124.01]; dokładny source_span: "9.66 Manipular Line Extension: Stacked Roman units with\nunoccupied flank hexes can extend their line as part of a Line\nCommand or in reaction to enemy movement, instead of using\nOrderly Withdrawal.".

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35, left, C-9.66-01-S2, bbox [44.997, 678.9, 297.009, 736.9]; dokładny source_span: "To undertake Manipular Line Extension\n(MLE), all the top units in the stacks in the same Line (see 4.32)\nmay move sideways into the vacant flank hexes (see the diagram\nabove).".

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Źródło PDF 35, right, C-9.66-01-S2, bbox [314.997, 54.01, 567.03, 124.01]; dokładny source_span: "To undertake Manipular Line Extension\n(MLE), all the top units in the stacks in the same Line (see 4.32)\nmay move sideways into the vacant flank hexes (see the diagram\nabove).".

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35, left, C-9.66-01-S3, bbox [44.997, 678.9, 297.009, 736.9]; dokładny source_span: "If a Flank hex is occupied, MLE cannot be used to place\na unit in that hex.".

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Źródło PDF 35, right, C-9.66-01-S3, bbox [314.997, 54.01, 567.03, 124.01]; dokładny source_span: "If a Flank hex is occupied, MLE cannot be used to place\na unit in that hex.".

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35, left, C-9.66-01-S4, bbox [44.997, 678.9, 297.009, 736.9]; dokładny source_span: "The hex entered by MLE must be Clear and\nnot in an enemy ZOC.".

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Źródło PDF 35, right, C-9.66-01-S4, bbox [314.997, 54.01, 567.03, 124.01]; dokładny source_span: "The hex entered by MLE must be Clear and\nnot in an enemy ZOC.".

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35, left, C-9.66-01-S5, bbox [44.997, 678.9, 297.009, 736.9]; dokładny source_span: "Facing remains the same.".

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Źródło PDF 35, right, C-9.66-01-S5, bbox [314.997, 54.01, 567.03, 124.01]; dokładny source_span: "Facing remains the same.".

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35, left, C-9.66-01-S6, bbox [44.997, 678.9, 297.009, 736.9]; dokładny source_span: "This rule only\napplies to unstacking the units; it does not apply to stacking\nthem together.".

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal. To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)

Źródło PDF 35, right, C-9.66-01-S6, bbox [314.997, 54.01, 567.03, 124.01]; dokładny source_span: "This rule only\napplies to unstacking the units; it does not apply to stacking\nthem together.".

> may move sideways into the vacant flank hexes (see the diagram
> above). If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex. The hex entered by MLE must be Clear and
> not in an enemy ZOC. Facing remains the same. This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF 35, left, D-02, bbox [80, 516, 266, 674]; dokładny source_span: null.

> 

Źródło PDF 35, left, CAP-01, bbox [128.368, 579.9, 213.638, 589.9]; dokładny source_span: null.

> Original Deployment

Źródło PDF 35, left, CAP-02, bbox [107.257, 661.5, 234.757, 671.5]; dokładny source_span: null.

> After Manipular Line Extension

**first-001 — pending / not_assessable**. Kandydaci: N966diagram, R966; osobny hash powyżej.

N966diagram, pointer `/nodes/7`, bajty [128977, 130323); hash zakresu `f5c32b1dae24067c8069c9f6a259e1da4cd473f61255ce80b5b070a71cc69689`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "captions": [
        "Original Deployment",
        "After Manipular Line Extension"
      ],
      "top_panel": "Two separated stacks; curved arrows point sideways right into adjacent empty hexes.",
      "bottom_panel": "Four single counters in adjacent hexes, labeled I a, I b, I c, I d.",
      "counter_text": [
        "HA",
        "J",
        "3",
        "LG",
        "7",
        "5"
      ]
    },
    "interpretation": "Illustration shows unstacking each top unit into vacant side hex, preserving facing. Numeric counter ratings are illustrative and are not general Roman unit parameters."
  },
  "evidence_ids": [
    "E966diagram"
  ],
  "reason": null,
  "gap_ids": []
}
```

R966, pointer `/rules/27`, bajty [312844, 317525); hash zakresu `2e7a501a9a282ca4841068af720073ea84aba9cb1de2d3ccd280e3a2103302a6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "all the top units in the stacks in the same Line (see 4.32)",
    "The hex entered by MLE must be Clear and not in an enemy ZOC."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.",
    "Facing unchanged.",
    "Applies only to unstacking; cannot stack units by MLE."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Stacked Romans in same Line; unoccupied Flank hexes.",
    "Entered hex Clear and outside enemy ZOC."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.",
    "Facing unchanged.",
    "Applies only to unstacking; cannot stack units by MLE."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Occupied Flank hex cannot receive MLE.",
    "Does not apply to stacking together."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "LC or reaction to enemy movement."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D966line, G-D-ZOC-R966

**context-01 — pending / not_assessable**. Kandydaci: N966diagram, R966; osobny hash powyżej.

N966diagram, pointer `/nodes/7`, bajty [177283, 178673); hash zakresu `36e8f4cd62347156e4d08983cd3b50a484a73b8478deddb5b4167d954c4d364d`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "captions": [
        "Original Deployment",
        "After Manipular Line Extension"
      ],
      "top_panel": "Two separated stacks; curved arrows point sideways right into adjacent empty hexes.",
      "bottom_panel": "Four single counters in adjacent hexes, labeled I a, I b, I c, I d.",
      "counter_text": [
        "HA",
        "J",
        "3",
        "LG",
        "7",
        "5"
      ]
    },
    "interpretation": "Illustration shows unstacking each top unit into vacant side hex, preserving facing. Numeric counter ratings are illustrative and are not general Roman unit parameters."
  },
  "evidence_ids": [
    "E966diagram"
  ],
  "reason": null,
  "gap_ids": []
}
```

R966, pointer `/rules/27`, bajty [384423, 389278); hash zakresu `2c3df78a88652b14a70895ae92c0bb0cf0a15d34596c536e9f59a05f1c63c10e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "all the top units in the stacks in the same Line (see 4.32)",
    "The hex entered by MLE must be Clear and not in an enemy ZOC."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.",
    "Facing unchanged.",
    "Applies only to unstacking; cannot stack units by MLE."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Stacked Romans in same Line; unoccupied Flank hexes.",
    "Entered hex Clear and outside enemy ZOC."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Extend by moving all top units sideways into vacant Flank hexes as part of LC or reaction to enemy movement in place of OW.",
    "Facing unchanged.",
    "Applies only to unstacking; cannot stack units by MLE."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Occupied Flank hex cannot receive MLE.",
    "Does not apply to stacking together."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "LC or reaction to enemy movement."
  ],
  "evidence_ids": [
    "E966a",
    "E966b"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D966line, G-D-ZOC-R966

### EXP-047 — M-POC5A.3

Dokładny zatwierdzony zakres: reactiontriggerenemycombatwithin2hexes,line;maydeclinefirstopportunitywithoutlosinglatertriggers;OW/MLEdifferentunitscanwithvalidtriggers,sameunitscannotboth

Wyłączenia/niepewności: OW i legalność line muszą być ustalone oddzielnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, right, C-9.67-01, bbox [314.997, 131.41, 567.05, 225.41]; dokładny source_span: null.

> 9.67 Manipular Line Extension may be undertaken as a reaction
> to enemy movement the instant an enemy combat unit comes
> within 2 hexes of a line of stacked Roman units. The Roman
> player may make his choice at any time any enemy unit so places
> itself (that is, he does not have to exercise his MLE rights the first
> time they become available). If enemy movement triggers both
> Orderly Withdrawal as well as MLE, both may be undertaken
> together but not by the same units.

Źródło PDF 35, right, X-07, bbox [314.997, 232.81, 567.013, 278.81]; dokładny source_span: null.

> EXAMPLE: A Velites unit sitting between two Hastati stacks may
> withdraw through the gaps in a Hastati line upon approach of,
> say, an enemy Phalanx and, as soon as that unit is through the
> gap, the Hastati line may undergo MLE.

**first-001 — pending / not_assessable**. Kandydaci: N967ex, R967; osobny hash powyżej.

N967ex, pointer `/nodes/8`, bajty [130329, 131266); hash zakresu `e2e9a2dcba7c2946ba1d54d93b45bacb6ff8a8e47c5af7e1e088c2c856fcbb15`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "A Velites unit sitting between two Hastati stacks may withdraw through the gaps in a Hastati line upon approach of, say, an enemy Phalanx and, as soon as that unit is through the gap, the Hastati line may undergo MLE.",
    "interpretation": "Different units withdraw and extend, illustrating permitted coexistence."
  },
  "evidence_ids": [
    "E967ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

R967, pointer `/rules/28`, bajty [317531, 321925); hash zakresu `8aba3115f33776d806a6a196be0cae710b2eea2eef13c04318a89102b3d53fcc`.

transcription:
```json
{
  "state": "known",
  "value": [
    "both may be undertaken together but not by the same units."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May react with MLE instantly, at any qualifying approach; need not take first opportunity.",
    "If movement triggers both OW and MLE, both may occur together using different units."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy combat unit comes within 2 hexes of stacked Roman line."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May react with MLE instantly, at any qualifying approach; need not take first opportunity.",
    "If movement triggers both OW and MLE, both may occur together using different units."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Same units cannot perform both OW and MLE."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "MLE trigger distance",
      "value": "within 2",
      "unit": {
        "state": "known",
        "value": "hexes",
        "evidence_ids": [
          "E967"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E967"
      ]
    }
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Instant of qualifying enemy movement; choice may be deferred to later qualifying approach."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D967OW

**context-01 — pending / not_assessable**. Kandydaci: N967ex, R967; osobny hash powyżej.

N967ex, pointer `/nodes/8`, bajty [178680, 179647); hash zakresu `6c9efe1728ad06ece3b7d45cd71e78dd02c715ae518ebbee8f2841bd7e8fdc26`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "A Velites unit sitting between two Hastati stacks may withdraw through the gaps in a Hastati line upon approach of, say, an enemy Phalanx and, as soon as that unit is through the gap, the Hastati line may undergo MLE.",
    "interpretation": "Different units withdraw and extend, illustrating permitted coexistence."
  },
  "evidence_ids": [
    "E967ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

R967, pointer `/rules/28`, bajty [389285, 393844); hash zakresu `e9376d25c08d2ed7bc27163917fcc5b9fc9ec4de5df11c2c309c7a92e2ef5755`.

transcription:
```json
{
  "state": "known",
  "value": [
    "both may be undertaken together but not by the same units."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May react with MLE instantly, at any qualifying approach; need not take first opportunity.",
    "If movement triggers both OW and MLE, both may occur together using different units."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy combat unit comes within 2 hexes of stacked Roman line."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May react with MLE instantly, at any qualifying approach; need not take first opportunity.",
    "If movement triggers both OW and MLE, both may occur together using different units."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Same units cannot perform both OW and MLE."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "MLE trigger distance",
      "value": "within 2",
      "unit": {
        "state": "known",
        "value": "hexes",
        "evidence_ids": [
          "E967"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E967"
      ]
    }
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Instant of qualifying enemy movement; choice may be deferred to later qualifying approach."
  ],
  "evidence_ids": [
    "E967"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D967OW

### EXP-048 — M-POC5A.3

Dokładny zatwierdzony zakres: activeMLELC-only,bothunitsmaymoveafterwithMA-2,noCHforMLE;ColumnunitsnoMLE;noautomatictransferofLCpostmovepermissiontoreaction

Wyłączenia/niepewności: Nie przenosić automatycznie post-MLE ruchu na tryb reakcyjny.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, right, C-9.68-01, bbox [314.997, 286.21, 567.012, 344.21]; dokładny source_span: null.

> 9.68 Manipular Line Extension may also be undertaken as part
> of a Line Command (only). If undertaken as an LC, both units
> may move after the MLE but with their MA reduced by 2. There
> are no Cohesion Hits applied for the MLE. Units in Column may
> not use MLE.

**first-001 — pending / not_assessable**. Kandydaci: R968; osobny hash powyżej.

R968, pointer `/rules/29`, bajty [321931, 326799); hash zakresu `4b8130db1b3f0bfe4d6e9ea3c3c7f8bcbb8db3d078654f49c01ad8a85db297bb`.

transcription:
```json
{
  "state": "known",
  "value": [
    "There are no Cohesion Hits applied for the MLE."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "MLE may also be part of LC only.",
    "When by LC, both units may then move at MA reduced by 2.",
    "No Hits for MLE; Column units cannot MLE."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E968"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "MLE may also be part of LC only.",
    "When by LC, both units may then move at MA reduced by 2.",
    "No Hits for MLE; Column units cannot MLE."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Units in Column excluded."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "post-LC-MLE MA adjustment",
      "value": -2,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E968"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E968"
      ]
    },
    {
      "name": "MLE Cohesion cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E968"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E968"
      ]
    }
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "After MLE in LC both units may move."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D968LC, G-D968column

**context-01 — pending / not_assessable**. Kandydaci: R968; osobny hash powyżej.

R968, pointer `/rules/29`, bajty [393851, 398910); hash zakresu `8b4bf17469c5987e914879bec985cb90bb189d32fa5e9a15e1e560fcf66722a1`.

transcription:
```json
{
  "state": "known",
  "value": [
    "There are no Cohesion Hits applied for the MLE."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "MLE may also be part of LC only.",
    "When by LC, both units may then move at MA reduced by 2.",
    "No Hits for MLE; Column units cannot MLE."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E968"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "MLE may also be part of LC only.",
    "When by LC, both units may then move at MA reduced by 2.",
    "No Hits for MLE; Column units cannot MLE."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Units in Column excluded."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "post-LC-MLE MA adjustment",
      "value": -2,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E968"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E968"
      ]
    },
    {
      "name": "MLE Cohesion cost",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E968"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E968"
      ]
    }
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "After MLE in LC both units may move."
  ],
  "evidence_ids": [
    "E968"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D968LC, G-D968column

### EXP-049 — M-POC5A.3

Dokładny zatwierdzony zakres: Romansprior200BCE,ScipioAfricanusnotOC;Cannaeexplicitusepergameinstruction,notnewhistoricalinference;C9.7S2explanatory

Wyłączenia/niepewności: W realnym scenariuszu data i tożsamość OC wymagają dowodów.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, right, C-9.7-01-S1, bbox [315.0, 370.173, 567.015, 440.173]; dokładny source_span: "This rule must be used with any battle involving Romans that took\nplace prior to 200 BCE in which Scipio Africanus is not pres-\nent as Overall Commander (and, yes, even though, historically,\nScipio was at Cannae, for game purposes he wasn’t, so use it at\nCannae).".

> This rule must be used with any battle involving Romans that took
> place prior to 200 BCE in which Scipio Africanus is not pres-
> ent as Overall Commander (and, yes, even though, historically,
> Scipio was at Cannae, for game purposes he wasn’t, so use it at
> Cannae). It represents the way Romans used their Triarii, and,
> for Rome, doctrine was the equivalent of unassailable dogma.

**first-001 — pending / not_assessable**. Kandydaci: R97intro; osobny hash powyżej.

R97intro, pointer `/rules/30`, bajty [326805, 330943); hash zakresu `640110048218e02f57f9aa8bdca2bd334ae950abe580344d8bfe03f9663b5001`.

transcription:
```json
{
  "state": "known",
  "value": [
    "so use it at Cannae"
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Scipio Africanus as OC excludes the stated mandatory applicability."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "date cutoff",
      "value": "prior to 200",
      "unit": {
        "state": "known",
        "value": "BCE",
        "evidence_ids": [
          "E97intro"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E97intro"
      ]
    }
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

**context-01 — pending / not_assessable**. Kandydaci: R97intro; osobny hash powyżej.

R97intro, pointer `/rules/30`, bajty [398917, 403202); hash zakresu `e89bbba15ff240518389e505e94aa7d9a023816ca59d362b60b3a7c6e8b29516`.

transcription:
```json
{
  "state": "known",
  "value": [
    "so use it at Cannae"
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Scipio Africanus as OC excludes the stated mandatory applicability."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "date cutoff",
      "value": "prior to 200",
      "unit": {
        "state": "known",
        "value": "BCE",
        "evidence_ids": [
          "E97intro"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E97intro"
      ]
    }
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

### EXP-050 — M-POC5A.3

Dokładny zatwierdzony zakres: realbattlewithoutdate/OC/AWL notresolved,requires_context

Wyłączenia/niepewności: Actual battle date, Overall Commander, AWL and scenario facts are required.; Konkretny scenariusz, OC, AWL/RP i stan mapy.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, right, C-9.7-01-S1, bbox [315.0, 370.173, 567.015, 440.173]; dokładny source_span: "This rule must be used with any battle involving Romans that took\nplace prior to 200 BCE in which Scipio Africanus is not pres-\nent as Overall Commander (and, yes, even though, historically,\nScipio was at Cannae, for game purposes he wasn’t, so use it at\nCannae).".

> This rule must be used with any battle involving Romans that took
> place prior to 200 BCE in which Scipio Africanus is not pres-
> ent as Overall Commander (and, yes, even though, historically,
> Scipio was at Cannae, for game purposes he wasn’t, so use it at
> Cannae). It represents the way Romans used their Triarii, and,
> for Rome, doctrine was the equivalent of unassailable dogma.

Źródło PDF 35, right, C-9.71-01, bbox [315.0, 447.573, 567.0, 469.573]; dokładny source_span: null.

> 9.71 Triarii units cannot move, but may change facing, until and
> unless one of the following occurs:

Źródło PDF 35, right, C-9.72-01, bbox [315.0, 553.113, 567.008, 611.113]; dokładny source_span: null.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

**first-001 — pending / not_assessable**. Kandydaci: R971, R972, R97intro; osobny hash powyżej.

R971, pointer `/rules/31`, bajty [330949, 335849); hash zakresu `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Elephants excluded from proximity trigger.",
    "Allied infantry excluded from separation test.",
    "Facing permitted before release."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "enemy proximity",
      "value": "within 3",
      "unit": {
        "state": "known",
        "value": "hexes AND LOS",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    },
    {
      "name": "separation",
      "value": ">=6",
      "unit": {
        "state": "known",
        "value": "hexes from all other Roman/Ala infantry lines",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    }
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until and unless either trigger occurs."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

R972, pointer `/rules/32`, bajty [335855, 339867); hash zakresu `f304ccb85a653664ddb287c3e591dd67a2744b35cf4210ace71592b684436f5b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "They may always, however, Shock attack (without moving) against enemy units in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Stationary Shock against enemy in own ZOC always permitted."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Rout Point threshold",
      "value": ">= floor(Army Withdrawal Level / 2)",
      "unit": {
        "state": "known",
        "value": "Rout Points",
        "evidence_ids": [
          "E972"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E972"
      ]
    }
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until Rout Point threshold; stationary Shock always allowed."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

R97intro, pointer `/rules/30`, bajty [326805, 330943); hash zakresu `640110048218e02f57f9aa8bdca2bd334ae950abe580344d8bfe03f9663b5001`.

transcription:
```json
{
  "state": "known",
  "value": [
    "so use it at Cannae"
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Scipio Africanus as OC excludes the stated mandatory applicability."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "date cutoff",
      "value": "prior to 200",
      "unit": {
        "state": "known",
        "value": "BCE",
        "evidence_ids": [
          "E97intro"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E97intro"
      ]
    }
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D971LOS, G-D972AWL, G-D972RP, G-D-ZOC-R972

**context-01 — pending / not_assessable**. Kandydaci: R971, R972, R97intro; osobny hash powyżej.

R971, pointer `/rules/31`, bajty [403209, 408288); hash zakresu `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Elephants excluded from proximity trigger.",
    "Allied infantry excluded from separation test.",
    "Facing permitted before release."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "enemy proximity",
      "value": "within 3",
      "unit": {
        "state": "known",
        "value": "hexes AND LOS",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    },
    {
      "name": "separation",
      "value": ">=6",
      "unit": {
        "state": "known",
        "value": "hexes from all other Roman/Ala infantry lines",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    }
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until and unless either trigger occurs."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

R972, pointer `/rules/32`, bajty [408295, 412460); hash zakresu `efc3e461afcdf47ef5fafdc90f3c9223badabf8597ff20dc3ef7807de8842bde`.

transcription:
```json
{
  "state": "known",
  "value": [
    "They may always, however, Shock attack (without moving) against enemy units in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Stationary Shock against enemy in own ZOC always permitted."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Rout Point threshold",
      "value": ">= floor(Army Withdrawal Level / 2)",
      "unit": {
        "state": "known",
        "value": "Rout Points",
        "evidence_ids": [
          "E972"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E972"
      ]
    }
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until Rout Point threshold; stationary Shock always allowed."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

R97intro, pointer `/rules/30`, bajty [398917, 403202); hash zakresu `e89bbba15ff240518389e505e94aa7d9a023816ca59d362b60b3a7c6e8b29516`.

transcription:
```json
{
  "state": "known",
  "value": [
    "so use it at Cannae"
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Battle involving Romans before 200 BCE and Scipio Africanus absent as OC."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii doctrine must be used for qualifying battles; explicitly applies at Cannae because Scipio is deemed absent for game purposes.",
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Scipio Africanus as OC excludes the stated mandatory applicability."
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "date cutoff",
      "value": "prior to 200",
      "unit": {
        "state": "known",
        "value": "BCE",
        "evidence_ids": [
          "E97intro"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E97intro"
      ]
    }
  ],
  "evidence_ids": [
    "E97intro"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D971LOS, G-D972AWL, G-D972RP, G-D-ZOC-R972

### EXP-051 — M-POC5A.4

Dokładny zatwierdzony zakres: movementgate9.71cannotmovebutmayface untiloneofORtriggers:enemycombatnotELwithin3andLOSanyTriariilineunit ORTriarii>=6fromallRoman/Alainfantrylinesexcludingallied

Wyłączenia/niepewności: Line, LOS, odległości i identyfikacja wojsk wymagają jawnych danych.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, right, C-9.71-01, bbox [315.0, 447.573, 567.0, 469.573]; dokładny source_span: null.

> 9.71 Triarii units cannot move, but may change facing, until and
> unless one of the following occurs:

Źródło PDF 35, right, C-9.71-02, bbox [315.0, 474.453, 567.03, 508.453]; dokładny source_span: null.

> • There is an enemy combat unit, other than an Elephant unit,
> which is within 3 hexes and LOS of any unit in the Triarii line,
> or

Źródło PDF 35, right, C-9.71-03, bbox [315.0, 511.893, 567.022, 545.893]; dokładny source_span: null.

> • The Triarii units are at least 6 hexes from all other Roman or
> Ala—but not allied–infantry lines, be they Hastati, Principes
> or whatever.

**first-001 — pending / not_assessable**. Kandydaci: R971; osobny hash powyżej.

R971, pointer `/rules/31`, bajty [330949, 335849); hash zakresu `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Elephants excluded from proximity trigger.",
    "Allied infantry excluded from separation test.",
    "Facing permitted before release."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "enemy proximity",
      "value": "within 3",
      "unit": {
        "state": "known",
        "value": "hexes AND LOS",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    },
    {
      "name": "separation",
      "value": ">=6",
      "unit": {
        "state": "known",
        "value": "hexes from all other Roman/Ala infantry lines",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    }
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until and unless either trigger occurs."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D971LOS

**context-01 — pending / not_assessable**. Kandydaci: R971; osobny hash powyżej.

R971, pointer `/rules/31`, bajty [403209, 408288); hash zakresu `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Elephants excluded from proximity trigger.",
    "Allied infantry excluded from separation test.",
    "Facing permitted before release."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "enemy proximity",
      "value": "within 3",
      "unit": {
        "state": "known",
        "value": "hexes AND LOS",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    },
    {
      "name": "separation",
      "value": ">=6",
      "unit": {
        "state": "known",
        "value": "hexes from all other Roman/Ala infantry lines",
        "evidence_ids": [
          "E971"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E971"
      ]
    }
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until and unless either trigger occurs."
  ],
  "evidence_ids": [
    "E971"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D971LOS

### EXP-052 — M-POC5A.4

Dokładny zatwierdzony zakres: move+ShockRP>=floor(AWL/2)doesnotbypass9.71;standingShockagainsttargetinownZOCper9.72withouthavingtomove

Wyłączenia/niepewności: 9.71 i9.72 czytane razem; full legal attack nadal wymaga innych warunków.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 35, right, C-9.72-01, bbox [315.0, 553.113, 567.008, 611.113]; dokładny source_span: null.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

**first-001 — pending / not_assessable**. Kandydaci: R972; osobny hash powyżej.

R972, pointer `/rules/32`, bajty [335855, 339867); hash zakresu `f304ccb85a653664ddb287c3e591dd67a2744b35cf4210ace71592b684436f5b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "They may always, however, Shock attack (without moving) against enemy units in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Stationary Shock against enemy in own ZOC always permitted."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Rout Point threshold",
      "value": ">= floor(Army Withdrawal Level / 2)",
      "unit": {
        "state": "known",
        "value": "Rout Points",
        "evidence_ids": [
          "E972"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E972"
      ]
    }
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until Rout Point threshold; stationary Shock always allowed."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D972AWL, G-D972RP, G-D-ZOC-R972

**context-01 — pending / not_assessable**. Kandydaci: R972; osobny hash powyżej.

R972, pointer `/rules/32`, bajty [408295, 412460); hash zakresu `efc3e461afcdf47ef5fafdc90f3c9223badabf8597ff20dc3ef7807de8842bde`.

transcription:
```json
{
  "state": "known",
  "value": [
    "They may always, however, Shock attack (without moving) against enemy units in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Triarii cannot move and Shock attack until Rout Point threshold reached.",
    "Always may stationary Shock enemy in their ZOC."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Stationary Shock against enemy in own ZOC always permitted."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Rout Point threshold",
      "value": ">= floor(Army Withdrawal Level / 2)",
      "unit": {
        "state": "known",
        "value": "Rout Points",
        "evidence_ids": [
          "E972"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E972"
      ]
    }
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Until Rout Point threshold; stationary Shock always allowed."
  ],
  "evidence_ids": [
    "E972"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D972AWL, G-D972RP, G-D-ZOC-R972

### EXP-053 — M-POC5A.4

Dokładny zatwierdzony zakres: ScorpioBoltB,builtincrew,TQ,LIonlymovement/defense;noShockattack,offensiveMissileFireonly

Wyłączenia/niepewności: Pełne LI defense/movement i bolt MRRC wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.81-01, bbox [45.0, 69.197, 297.101, 139.197]; dokładny source_span: null.

> 9.81 Scorpios are Bolt-firing (B) engines with built-
> in crews. The Scorpios have a TQ rating, and they
> are treated as Light Infantry (LI) for movement and
> when defending in Shock Combat or against Missile
> Fire. Scorpio units are not Shock-capable and their only offensive
> combat capability is to Missile Fire.

**first-001 — pending / not_assessable**. Kandydaci: R981; osobny hash powyżej.

R981, pointer `/rules/33`, bajty [339873, 343919); hash zakresu `4e4891fc2c755ae9c07ed249141e368ed4377a415f874d747416eecb628eed39`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Scorpio units are not Shock-capable and their only offensive combat capability is to Missile Fire."
  ],
  "evidence_ids": [
    "E981"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Scorpios are Bolt-firing (B) engines with built-in crews and TQ.",
    "Treat as LI for movement and defense in Shock or against Missile Fire.",
    "No Shock capability; offensive capability only Missile Fire."
  ],
  "evidence_ids": [
    "E981"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E981"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Scorpios are Bolt-firing (B) engines with built-in crews and TQ.",
    "Treat as LI for movement and defense in Shock or against Missile Fire.",
    "No Shock capability; offensive capability only Missile Fire."
  ],
  "evidence_ids": [
    "E981"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E981"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E981"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

**context-01 — pending / not_assessable**. Kandydaci: R981; osobny hash powyżej.

R981, pointer `/rules/33`, bajty [412467, 416654); hash zakresu `76cecff485b506b160191a8885cea72dd7016bed6da4f3798c6d7d01dbc6b826`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Scorpio units are not Shock-capable and their only offensive combat capability is to Missile Fire."
  ],
  "evidence_ids": [
    "E981"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Scorpios are Bolt-firing (B) engines with built-in crews and TQ.",
    "Treat as LI for movement and defense in Shock or against Missile Fire.",
    "No Shock capability; offensive capability only Missile Fire."
  ],
  "evidence_ids": [
    "E981"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E981"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Scorpios are Bolt-firing (B) engines with built-in crews and TQ.",
    "Treat as LI for movement and defense in Shock or against Missile Fire.",
    "No Shock capability; offensive capability only Missile Fire."
  ],
  "evidence_ids": [
    "E981"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E981"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E981"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

### EXP-054 — M-POC5A.4

Dokładny zatwierdzony zakres: modechangeIOanyfriendlyleader;Firecannotmove,Movecannotfire;switchtoMoveblocksMoveinthesamephase,switchtoFireblocksFireinthesamephase;moveIOrequired,firedoesnotrequireorder;awersFire,rewersMove

Wyłączenia/niepewności: 9.85 uzupełnia harmonogram ognia; źródło nie ustanawia dodatkowej akcji po switch.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.82-01, bbox [45.0, 146.597, 297.55, 252.597]; dokładny source_span: null.

> 9.82 A Scorpio is in either Fire or Move mode. It requires an
> Individual Order from any friendly leader to change its mode.
> Scorpios in Move mode cannot fire, and conversely, cannot
> move in Fire mode. A Scorpio that has had its mode changed to
> Move cannot move in that Orders Phase, nor can a Scorpio that
> has had its mode switched to Fire, fire in that Orders Phase. A
> Scorpio unit in Move mode requires an Individual Order from
> any friendly leader to move. Scorpio units do not need orders to
> fire (see 9.85 below).

Źródło PDF 36, left, N-11, bbox [49.0, 261.1, 292.996, 283.1]; dokładny source_span: null.

> PLAY NOTE: The front side of the counter shows the unit in
> Fire mode; the reverse side in Move mode.

**first-001 — pending / not_assessable**. Kandydaci: R982, R982note; osobny hash powyżej.

R982, pointer `/rules/34`, bajty [343925, 349222); hash zakresu `db2932e05afee950e1d27137b71fe09be42fd41a52f8e80905dc27726cf31a48`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Scorpio units do not need orders to fire (see 9.85 below)."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Either Fire or Move mode; switch with Individual Order from any friendly leader.",
    "Cannot fire in Move or move in Fire.",
    "After switching to Move, cannot move that Orders Phase; after switching to Fire cannot fire that Orders Phase.",
    "Moving in Move requires Individual Order from any friendly leader; firing needs no orders."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Either Fire or Move mode; switch with Individual Order from any friendly leader.",
    "Cannot fire in Move or move in Fire.",
    "After switching to Move, cannot move that Orders Phase; after switching to Fire cannot fire that Orders Phase.",
    "Moving in Move requires Individual Order from any friendly leader; firing needs no orders."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "No order needed to fire."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "mode change",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Individual Order",
        "evidence_ids": [
          "E982"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E982"
      ]
    },
    {
      "name": "movement order",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Individual Order",
        "evidence_ids": [
          "E982"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E982"
      ]
    }
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Switching blocks corresponding action for that Orders Phase."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": null,
  "gap_ids": []
}
```

R982note, pointer `/rules/35`, bajty [349228, 352453); hash zakresu `88bf7f560fd28fa8d2955805d683d0f7eac1210dac638fc5f483232a758bd6c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The front side of the counter shows the unit in Fire mode; the reverse side in Move mode."
  ],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
  "evidence_ids": [
    "E982note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
  "evidence_ids": [
    "E982note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

**context-01 — pending / not_assessable**. Kandydaci: R982, R982note; osobny hash powyżej.

R982, pointer `/rules/34`, bajty [416661, 422148); hash zakresu `c322a28fb1c69bff5deac677b5a8ee02c5c27f63d0f17bce8a72a482a530f988`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Scorpio units do not need orders to fire (see 9.85 below)."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Either Fire or Move mode; switch with Individual Order from any friendly leader.",
    "Cannot fire in Move or move in Fire.",
    "After switching to Move, cannot move that Orders Phase; after switching to Fire cannot fire that Orders Phase.",
    "Moving in Move requires Individual Order from any friendly leader; firing needs no orders."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Either Fire or Move mode; switch with Individual Order from any friendly leader.",
    "Cannot fire in Move or move in Fire.",
    "After switching to Move, cannot move that Orders Phase; after switching to Fire cannot fire that Orders Phase.",
    "Moving in Move requires Individual Order from any friendly leader; firing needs no orders."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "No order needed to fire."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "mode change",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Individual Order",
        "evidence_ids": [
          "E982"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E982"
      ]
    },
    {
      "name": "movement order",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Individual Order",
        "evidence_ids": [
          "E982"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E982"
      ]
    }
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Switching blocks corresponding action for that Orders Phase."
  ],
  "evidence_ids": [
    "E982"
  ],
  "reason": null,
  "gap_ids": []
}
```

R982note, pointer `/rules/35`, bajty [422155, 425494); hash zakresu `9ac67925c35fae2788830f9c0809376ae5aace09ee195639c5f67b7240858bd0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "The front side of the counter shows the unit in Fire mode; the reverse side in Move mode."
  ],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
  "evidence_ids": [
    "E982note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
  "evidence_ids": [
    "E982note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E982note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

### EXP-055 — M-POC5A.4

Dokładny zatwierdzony zakres: atmostoneScorpioperhex,otherstackingrulesretained

Wyłączenia/niepewności: Pełna legalność współzajęcia wymaga general stacking.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.83-01, bbox [45.0, 292.34, 297.017, 314.34]; dokładny source_span: null.

> 9.83 Only one Scorpio unit may occupy any one hex. All other
> stacking rules apply.

**first-001 — pending / not_assessable**. Kandydaci: R983; osobny hash powyżej.

R983, pointer `/rules/36`, bajty [352459, 356106); hash zakresu `f7d2aafc87c8ed78040ffececeea0285fff874b6b06483f0065d8564c626e87f`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Only one Scorpio unit may occupy any one hex. All other stacking rules apply."
  ],
  "evidence_ids": [
    "E983"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
  "evidence_ids": [
    "E983"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E983"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
  "evidence_ids": [
    "E983"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E983"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Scorpio hex limit",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Scorpio unit per hex",
        "evidence_ids": [
          "E983"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E983"
      ]
    }
  ],
  "evidence_ids": [
    "E983"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D983stack

**context-01 — pending / not_assessable**. Kandydaci: R983; osobny hash powyżej.

R983, pointer `/rules/36`, bajty [425501, 429280); hash zakresu `7a009418ad0af36b8ee5ca3de17a068395e17db2e7da4760ace20689e5366e00`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Only one Scorpio unit may occupy any one hex. All other stacking rules apply."
  ],
  "evidence_ids": [
    "E983"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
  "evidence_ids": [
    "E983"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E983"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
  "evidence_ids": [
    "E983"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E983"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Scorpio hex limit",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Scorpio unit per hex",
        "evidence_ids": [
          "E983"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E983"
      ]
    }
  ],
  "evidence_ids": [
    "E983"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D983stack

### EXP-056 — M-POC5A.4

Dokładny zatwierdzony zakres: nofacing;allhexesFront;range/LOS/terrainnotwaived

Wyłączenia/niepewności: Nie znosi range/LOS/terrain.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.84-01, bbox [45.0, 321.74, 297.063, 355.74]; dokładny source_span: null.

> 9.84 Scorpio units have no facing; they may move or fire in any
> direction, regardless of the direction the actual counter is pointed.
> All hexes are considered Front hexes.

**first-001 — pending / not_assessable**. Kandydaci: R984; osobny hash powyżej.

R984, pointer `/rules/37`, bajty [356112, 359528); hash zakresu `de911fdc0696db757fc4653804f89e65ed4a57ec809e9dd48209d12f438a56a5`.

transcription:
```json
{
  "state": "known",
  "value": [
    "All hexes are considered Front hexes."
  ],
  "evidence_ids": [
    "E984"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
  "evidence_ids": [
    "E984"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E984"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
  "evidence_ids": [
    "E984"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E984"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E984"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

**context-01 — pending / not_assessable**. Kandydaci: R984; osobny hash powyżej.

R984, pointer `/rules/37`, bajty [429287, 432825); hash zakresu `1c7feae738ab6c980bff3d77751acadc52dc149fb5e6ab07b6dbfcb090e4ec60`.

transcription:
```json
{
  "state": "known",
  "value": [
    "All hexes are considered Front hexes."
  ],
  "evidence_ids": [
    "E984"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
  "evidence_ids": [
    "E984"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E984"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
  "evidence_ids": [
    "E984"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E984"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E984"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

### EXP-057 — M-POC5A.4

Dokładny zatwierdzony zakres: ActiveFiremax2/GameTurnandmax1/friendlyOrdersPhaseinMovementMissilesegment;Once/Finished;afteractiveFire nootheractionthatphaseincludingRecovery

Wyłączenia/niepewności: Warunki range/LOS/MRRC i mode9.82 nadal obowiązują.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.85-01, bbox [44.997, 363.14, 297.024, 481.14]; dokładny source_span: null.

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

Źródło PDF 36, left, G-04, bbox [45, 365, 120, 404]; dokładny source_span: null.

> 

**first-001 — pending / not_assessable**. Kandydaci: N985markers, R985; osobny hash powyżej.

N985markers, pointer `/nodes/34`, bajty [150642, 151434); hash zakresu `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": [
      "Active Fire Once",
      "Active Fire Finished"
    ],
    "interpretation": "Once and Finished marker faces illustrate the two-stage Active Fire status."
  },
  "evidence_ids": [
    "E985markers"
  ],
  "reason": null,
  "gap_ids": []
}
```

R985, pointer `/rules/38`, bajty [359534, 364613); hash zakresu `9083d4f2690f24d2424f617dbf3a0b4481149a19932798070e26fcfe4b74207e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "no more than one shot per Orders Phase."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Offensive fire up to twice per Game Turn, at most one shot per Orders Phase, at any time within segment, without order.",
    "First shot place ACTIVE FIRE ONCE; second flip to ACTIVE FIRE FINISHED.",
    "Firing Scorpio can do nothing else that Orders Phase, including recover Hits."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Friendly Orders Phase, active player Movement and Missile Fire Segment, Scorpio in Fire mode."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Offensive fire up to twice per Game Turn, at most one shot per Orders Phase, at any time within segment, without order.",
    "First shot place ACTIVE FIRE ONCE; second flip to ACTIVE FIRE FINISHED.",
    "Firing Scorpio can do nothing else that Orders Phase, including recover Hits."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E985"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "active fire cap",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "shots per Game Turn",
        "evidence_ids": [
          "E985"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E985"
      ]
    },
    {
      "name": "active phase cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "shot per Orders Phase",
        "evidence_ids": [
          "E985"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E985"
      ]
    }
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Twice per Game Turn, not per Orders Phase.",
    "During any friendly Orders Phase Movement and Missile Fire Segment.",
    "Other actions prohibited entire firing Orders Phase."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

**context-01 — pending / not_assessable**. Kandydaci: N985markers, R985; osobny hash powyżej.

N985markers, pointer `/nodes/34`, bajty [199790, 200614); hash zakresu `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": [
      "Active Fire Once",
      "Active Fire Finished"
    ],
    "interpretation": "Once and Finished marker faces illustrate the two-stage Active Fire status."
  },
  "evidence_ids": [
    "E985markers"
  ],
  "reason": null,
  "gap_ids": []
}
```

R985, pointer `/rules/38`, bajty [432832, 438091); hash zakresu `15e7d8e13c9489316c465caf3fb6ec40f605189e3145e013051d7ec031e0dea3`.

transcription:
```json
{
  "state": "known",
  "value": [
    "no more than one shot per Orders Phase."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Offensive fire up to twice per Game Turn, at most one shot per Orders Phase, at any time within segment, without order.",
    "First shot place ACTIVE FIRE ONCE; second flip to ACTIVE FIRE FINISHED.",
    "Firing Scorpio can do nothing else that Orders Phase, including recover Hits."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Friendly Orders Phase, active player Movement and Missile Fire Segment, Scorpio in Fire mode."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Offensive fire up to twice per Game Turn, at most one shot per Orders Phase, at any time within segment, without order.",
    "First shot place ACTIVE FIRE ONCE; second flip to ACTIVE FIRE FINISHED.",
    "Firing Scorpio can do nothing else that Orders Phase, including recover Hits."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E985"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "active fire cap",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "shots per Game Turn",
        "evidence_ids": [
          "E985"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E985"
      ]
    },
    {
      "name": "active phase cap",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "shot per Orders Phase",
        "evidence_ids": [
          "E985"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E985"
      ]
    }
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Twice per Game Turn, not per Orders Phase.",
    "During any friendly Orders Phase Movement and Missile Fire Segment.",
    "Other actions prohibited entire firing Orders Phase."
  ],
  "evidence_ids": [
    "E985"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

### EXP-058 — M-POC5A.4

Dokładny zatwierdzony zakres: specialReactionFiremax2/enemyOrdersPhasein enemyMovementMissilesegment,includingduringenemyunitmovement;ordinary8.2ReactionFireforbidden;sourceanymovementdoesnotgrantScorpiofireinMovemode

Wyłączenia/niepewności: No Reaction Fire any kind w Rampage9.14 nadal wyłącza trigger; zewnętrzny ogień i segment wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.86-01, bbox [45.0, 489.54, 297.053, 583.54]; dokładny source_span: null.

> 9.86 Reaction Fire: Scorpios may fire twice per enemy Orders
> Phase at any time during the enemy Movement and Missile Seg-
> ment—and we mean “any”; they may fire even during enemy
> movement! The first time the Scorpio unit fires, place
> a REACTION FIRE ONCE marker on it. The second
> time it fires, flip the marker to its REACTION FIRE
> FINISHED side. Scorpios, however, cannot use any
> type of ordinary Reaction Fire (8.2).

Źródło PDF 36, left, G-05, bbox [260, 528, 297, 566]; dokładny source_span: null.

> 

**first-001 — pending / not_assessable**. Kandydaci: N986marker, R986; osobny hash powyżej.

N986marker, pointer `/nodes/35`, bajty [151440, 152165); hash zakresu `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "Reaction Fire Once",
    "interpretation": "Only Once face pictured here; Finished face is specified in prose R986."
  },
  "evidence_ids": [
    "E986marker"
  ],
  "reason": null,
  "gap_ids": []
}
```

R986, pointer `/rules/39`, bajty [364619, 369123); hash zakresu `64c29b4c0d2490544011c5ceb97b13ba7cd008eb4729f5055d1ca9665796cca7`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Scorpios, however, cannot use any type of ordinary Reaction Fire (8.2)."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May fire twice per enemy Orders Phase at any time in segment, including during enemy movement.",
    "First place REACTION FIRE ONCE; second flip REACTION FIRE FINISHED.",
    "Cannot use any ordinary Reaction Fire under 8.2."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy Orders Phase Movement and Missile Segment; Scorpio in Fire mode under 9.82."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May fire twice per enemy Orders Phase at any time in segment, including during enemy movement.",
    "First place REACTION FIRE ONCE; second flip REACTION FIRE FINISHED.",
    "Cannot use any ordinary Reaction Fire under 8.2."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E986"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "reaction fire cap",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "shots per enemy Orders Phase",
        "evidence_ids": [
          "E986"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E986"
      ]
    }
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Any time in enemy Movement and Missile Segment, including enemy movement."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D986react

**context-01 — pending / not_assessable**. Kandydaci: N986marker, R986; osobny hash powyżej.

N986marker, pointer `/nodes/35`, bajty [200621, 201375); hash zakresu `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "Reaction Fire Once",
    "interpretation": "Only Once face pictured here; Finished face is specified in prose R986."
  },
  "evidence_ids": [
    "E986marker"
  ],
  "reason": null,
  "gap_ids": []
}
```

R986, pointer `/rules/39`, bajty [438098, 442766); hash zakresu `4cf0366781c3358abc98fff09da31c4c44d05d4c9dae4f10f7cd6443e2c714da`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Scorpios, however, cannot use any type of ordinary Reaction Fire (8.2)."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May fire twice per enemy Orders Phase at any time in segment, including during enemy movement.",
    "First place REACTION FIRE ONCE; second flip REACTION FIRE FINISHED.",
    "Cannot use any ordinary Reaction Fire under 8.2."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Enemy Orders Phase Movement and Missile Segment; Scorpio in Fire mode under 9.82."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May fire twice per enemy Orders Phase at any time in segment, including during enemy movement.",
    "First place REACTION FIRE ONCE; second flip REACTION FIRE FINISHED.",
    "Cannot use any ordinary Reaction Fire under 8.2."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E986"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "reaction fire cap",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "shots per enemy Orders Phase",
        "evidence_ids": [
          "E986"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E986"
      ]
    }
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Any time in enemy Movement and Missile Segment, including enemy movement."
  ],
  "evidence_ids": [
    "E986"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D986react

### EXP-059 — M-POC5A.4

Dokładny zatwierdzony zakres: incur/recoverHitsasgeneralunits;Routimmediateelimination

Wyłączenia/niepewności: Trigger Rout i recovery amounts wymagają general rules.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.87-01, bbox [45.0, 590.94, 297.043, 612.94]; dokładny source_span: null.

> 9.87 Scorpios incur and recover Cohesion Hits as any other unit.
> A Scorpio that routs is immediately eliminated.

**first-001 — pending / not_assessable**. Kandydaci: R987; osobny hash powyżej.

R987, pointer `/rules/40`, bajty [369129, 372461); hash zakresu `0bdf1d408d64bb25daf21ea3f60f30aeb4ff91ce89afa5fc8f59908eba99ca8a`.

transcription:
```json
{
  "state": "known",
  "value": [
    "A Scorpio that routs is immediately eliminated."
  ],
  "evidence_ids": [
    "E987"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
  "evidence_ids": [
    "E987"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E987"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
  "evidence_ids": [
    "E987"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E987"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E987"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on rout."
  ],
  "evidence_ids": [
    "E987"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D987recovery

**context-01 — pending / not_assessable**. Kandydaci: R987; osobny hash powyżej.

R987, pointer `/rules/40`, bajty [442773, 446233); hash zakresu `4319d42d58befea89683b3ce1da7b0ca03bb21ea982de7aaa504ab436290a229`.

transcription:
```json
{
  "state": "known",
  "value": [
    "A Scorpio that routs is immediately eliminated."
  ],
  "evidence_ids": [
    "E987"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
  "evidence_ids": [
    "E987"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E987"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
  "evidence_ids": [
    "E987"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E987"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E987"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on rout."
  ],
  "evidence_ids": [
    "E987"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D987recovery

### EXP-060 — M-POC5A.4

Dokładny zatwierdzony zakres: BI no terrainCohesionHits crossing/enteringpassableterrain or facingRough;MP/passabilitynotwaived;noColumn/PAW/OW

Wyłączenia/niepewności: Passability/koszt MP wymagają Movement Cost Chart, zakazy nie wymagają wykonania zabronionych procedur.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, left, C-9.91-02, bbox [45.0, 698.844, 297.12, 732.844]; dokładny source_span: null.

> Barbarian Infantry (BI) units do not incur Cohesion Hits for
> crossing or entering any type of passable terrain, nor do they
> incur Cohesion Hits for changing facing in Rough terrain. BI units

Źródło PDF 36, right, C-9.91-02, bbox [315.0, 54.004, 567.0, 76.004]; dokładny source_span: null.

> cannot use Column Movement (6.7), Pre-Arranged Withdrawal
> (6.8), or Orderly Withdrawal (6.5).

**first-001 — pending / not_assessable**. Kandydaci: R991; osobny hash powyżej.

R991, pointer `/rules/41`, bajty [372467, 377217); hash zakresu `54dcf8cd5202e6beebb7d87fcb4104ee5d6b6b3b8737e8ad794d6665eb6c387b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "nor do they incur Cohesion Hits for changing facing in Rough terrain.",
    "cannot use Column Movement (6.7), Pre-Arranged Withdrawal (6.8), or Orderly Withdrawal (6.5)."
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "BI incur no Cohesion Hits for entering/crossing passable terrain or changing facing in Rough.",
    "Cannot use Column Movement, Pre-Arranged Withdrawal or OW."
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "BI incur no Cohesion Hits for entering/crossing passable terrain or changing facing in Rough.",
    "Cannot use Column Movement, Pre-Arranged Withdrawal or OW."
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "passable terrain/facing-Rough penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E991a",
          "E991b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E991a",
        "E991b"
      ]
    }
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D991column, G-D991PAW, G-D991OW

**context-01 — pending / not_assessable**. Kandydaci: R991; osobny hash powyżej.

R991, pointer `/rules/41`, bajty [446240, 451161); hash zakresu `5e41692ae51622c98f8ec0c02518e45efed39da42849c4d7693b20f9138a770c`.

transcription:
```json
{
  "state": "known",
  "value": [
    "nor do they incur Cohesion Hits for changing facing in Rough terrain.",
    "cannot use Column Movement (6.7), Pre-Arranged Withdrawal (6.8), or Orderly Withdrawal (6.5)."
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "BI incur no Cohesion Hits for entering/crossing passable terrain or changing facing in Rough.",
    "Cannot use Column Movement, Pre-Arranged Withdrawal or OW."
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "BI incur no Cohesion Hits for entering/crossing passable terrain or changing facing in Rough.",
    "Cannot use Column Movement, Pre-Arranged Withdrawal or OW."
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "passable terrain/facing-Rough penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E991a",
          "E991b"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E991a",
        "E991b"
      ]
    }
  ],
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D991column, G-D991PAW, G-D991OW

### EXP-061 — M-POC5A.4

Dokładny zatwierdzony zakres: Recoveryorderonly1CH;depletedBIeliminatedinsteadofRout;do notautomaticallytreatthateliminationasRoutforFerocity;fulltriggerorderingnotresolved

Wyłączenia/niepewności: Depleted stan i inne warunki recovery wymagają kontekstu; konflikt z Ferocity po depleted elimination nie rozstrzygnięty.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.93-02, bbox [315.0, 99.004, 566.997, 109.004]; dokładny source_span: null.

> BI units can only remove 1 Cohesion Hit per Recovery order.

Źródło PDF 36, right, C-9.93-03, bbox [315.0, 111.004, 543.32, 121.004]; dokładny source_span: null.

> Depleted BI units do not Rout but are instead eliminated.

**first-001 — pending / not_assessable**. Kandydaci: R993; osobny hash powyżej.

R993, pointer `/rules/42`, bajty [377223, 381102); hash zakresu `ac9f1b844e212d7c1ed2c0b307f8f974da613cd2137afc21a716bd6ff2f5d820`.

transcription:
```json
{
  "state": "known",
  "value": [
    "BI units can only remove 1 Cohesion Hit per Recovery order."
  ],
  "evidence_ids": [
    "E993"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
  "evidence_ids": [
    "E993"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E993"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
  "evidence_ids": [
    "E993"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E993"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Recovery amount",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per Recovery order",
        "evidence_ids": [
          "E993"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E993"
      ]
    }
  ],
  "evidence_ids": [
    "E993"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D993recovery, G-D993depleted

**context-01 — pending / not_assessable**. Kandydaci: R993; osobny hash powyżej.

R993, pointer `/rules/42`, bajty [451168, 455190); hash zakresu `fdf01acb9629e037cb6f43e05f89f53320c84ff76245e149f5dce967553aa1f3`.

transcription:
```json
{
  "state": "known",
  "value": [
    "BI units can only remove 1 Cohesion Hit per Recovery order."
  ],
  "evidence_ids": [
    "E993"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
  "evidence_ids": [
    "E993"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E993"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
  "evidence_ids": [
    "E993"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E993"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "Recovery amount",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Cohesion Hit per Recovery order",
        "evidence_ids": [
          "E993"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E993"
      ]
    }
  ],
  "evidence_ids": [
    "E993"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D993recovery, G-D993depleted

### EXP-062 — M-POC5A.4

Dokładny zatwierdzony zakres: BI startFerocity;BI PreShock-1DRM and defenders+2DRM inshownscope,othermodifiers/procedureunknown

Wyłączenia/niepewności: Inne DRM i Pre-Shock procedure nie są domknięte.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.94-02, bbox [315.0, 224.347, 567.029, 270.347]; dokładny source_span: null.

> All BI units start the game with Ferocity. A BI unit with Ferocity
> earns a –1 DRM to its Pre-Shock TQ die roll while penalizing
> the defending unit(s) with a +2 DRM to their Pre-Shock TQ die
> roll(s).

**first-001 — pending / not_assessable**. Kandydaci: R994; osobny hash powyżej.

R994, pointer `/rules/43`, bajty [381108, 386923); hash zakresu `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the DR is the same or lower, BI units retain their Ferocity"
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "All BI start game with Ferocity.",
    "Ferocity check each time a BI unit Routs; leader as given by scenario setup."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E994"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "BI Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "defender Pre-Shock modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "retention",
      "value": "DR <= leader Initiative Rating",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    }
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starts game; check each BI Rout; failed check causes permanent loss for that command."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D994scenario, G-D994pre

**context-01 — pending / not_assessable**. Kandydaci: R994; osobny hash powyżej.

R994, pointer `/rules/43`, bajty [455197, 461221); hash zakresu `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the DR is the same or lower, BI units retain their Ferocity"
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "All BI start game with Ferocity.",
    "Ferocity check each time a BI unit Routs; leader as given by scenario setup."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E994"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "BI Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "defender Pre-Shock modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "retention",
      "value": "DR <= leader Initiative Rating",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    }
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starts game; check each BI Rout; failed check causes permanent loss for that command."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D994scenario, G-D994pre

### EXP-063 — M-POC5A.4

Dokładny zatwierdzony zakres: EachordinaryBI RouttriggersFerocitycheckagainstscenarioassignedleaderInitiative;DR<=retains,>losespermanentlyforthatleaderBIcommand,othersunaffected

Wyłączenia/niepewności: Scenario commander mapping i Initiative muszą być dostępne; depleted elimination ≠ jawny Rout trigger.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.94-03, bbox [315.0, 277.747, 567.066, 371.747]; dokładny source_span: null.

> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.

**first-001 — pending / not_assessable**. Kandydaci: R994; osobny hash powyżej.

R994, pointer `/rules/43`, bajty [381108, 386923); hash zakresu `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the DR is the same or lower, BI units retain their Ferocity"
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "All BI start game with Ferocity.",
    "Ferocity check each time a BI unit Routs; leader as given by scenario setup."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E994"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "BI Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "defender Pre-Shock modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "retention",
      "value": "DR <= leader Initiative Rating",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    }
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starts game; check each BI Rout; failed check causes permanent loss for that command."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D994scenario, G-D994pre

**context-01 — pending / not_assessable**. Kandydaci: R994; osobny hash powyżej.

R994, pointer `/rules/43`, bajty [455197, 461221); hash zakresu `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the DR is the same or lower, BI units retain their Ferocity"
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "All BI start game with Ferocity.",
    "Ferocity check each time a BI unit Routs; leader as given by scenario setup."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E994"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "BI Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "defender Pre-Shock modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "retention",
      "value": "DR <= leader Initiative Rating",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    }
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starts game; check each BI Rout; failed check causes permanent loss for that command."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D994scenario, G-D994pre

### EXP-064 — M-POC5A.4

Dokładny zatwierdzony zakres: Actualleader/Initiative/membership requires scenariosetup;no nearest/favorable default

Wyłączenia/niepewności: Actual leader, Initiative and BI command membership require scenario setup.; Jedno wskazane przypisanie scenario wraz z ratings, nie domyślny najbliższy leader.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.94-03, bbox [315.0, 277.747, 567.066, 371.747]; dokładny source_span: null.

> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.

Źródło PDF 36, right, C-9.95-02, bbox [315.0, 394.747, 567.026, 500.747]; dokładny source_span: null.

> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.

**first-001 — pending / not_assessable**. Kandydaci: R994, R995; osobny hash powyżej.

R994, pointer `/rules/43`, bajty [381108, 386923); hash zakresu `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the DR is the same or lower, BI units retain their Ferocity"
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "All BI start game with Ferocity.",
    "Ferocity check each time a BI unit Routs; leader as given by scenario setup."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E994"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "BI Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "defender Pre-Shock modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "retention",
      "value": "DR <= leader Initiative Rating",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    }
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starts game; check each BI Rout; failed check causes permanent loss for that command."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

R995, pointer `/rules/44`, bajty [386929, 392597); hash zakresu `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Start of game: all BI have Impetuosity.",
    "At least two BI in leader’s command enter enemy ZOC."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E995"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "initial BI MA adjustment",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "leader first-try Momentum modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "end-state trigger",
      "value": ">=2",
      "unit": {
        "state": "known",
        "value": "BI units of one command entering enemy ZOC",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    }
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Start of game; after trigger retained through remainder of that Game Turn, then lost."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D994scenario, G-D994pre, G-D995momentum, G-D995scenario, G-D-ZOC-R995

**context-01 — pending / not_assessable**. Kandydaci: R994, R995; osobny hash powyżej.

R994, pointer `/rules/43`, bajty [455197, 461221); hash zakresu `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "If the DR is the same or lower, BI units retain their Ferocity"
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "All BI start game with Ferocity.",
    "Ferocity check each time a BI unit Routs; leader as given by scenario setup."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Ferocious BI earns –1 Pre-Shock TQ DRM; defender(s) +2 Pre-Shock TQ DRM.",
    "Roll versus leader Initiative: DR<=Initiative retains Ferocity; higher loses permanently for BI under that leader.",
    "Loss under one leader has no effect on BI under different leaders."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E994"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "BI Pre-Shock modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "defender Pre-Shock modifier",
      "value": 2,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    },
    {
      "name": "retention",
      "value": "DR <= leader Initiative Rating",
      "unit": {
        "state": "known",
        "value": "die-roll comparison",
        "evidence_ids": [
          "E994"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E994"
      ]
    }
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Starts game; check each BI Rout; failed check causes permanent loss for that command."
  ],
  "evidence_ids": [
    "E994"
  ],
  "reason": null,
  "gap_ids": []
}
```

R995, pointer `/rules/44`, bajty [461228, 467103); hash zakresu `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Start of game: all BI have Impetuosity.",
    "At least two BI in leader’s command enter enemy ZOC."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E995"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "initial BI MA adjustment",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "leader first-try Momentum modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "end-state trigger",
      "value": ">=2",
      "unit": {
        "state": "known",
        "value": "BI units of one command entering enemy ZOC",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    }
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Start of game; after trigger retained through remainder of that Game Turn, then lost."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D994scenario, G-D994pre, G-D995momentum, G-D995scenario, G-D-ZOC-R995

### EXP-065 — M-POC5A.4

Dokładny zatwierdzony zakres: BI startMA+1 and commandingLeader-1allfirsttryMomentum;after>=2distinctBIofsamecommandenterenemyZOC,Impetuosity lastsrestofthatGameTurn thenlostforthatcommandonly

Wyłączenia/niepewności: Mapping command, ZOC i Momentum wymagają danych; lokalny czas wygaśnięcia jest jawny.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.95-02, bbox [315.0, 394.747, 567.026, 500.747]; dokładny source_span: null.

> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.

**first-001 — pending / not_assessable**. Kandydaci: R995; osobny hash powyżej.

R995, pointer `/rules/44`, bajty [386929, 392597); hash zakresu `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Start of game: all BI have Impetuosity.",
    "At least two BI in leader’s command enter enemy ZOC."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E995"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "initial BI MA adjustment",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "leader first-try Momentum modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "end-state trigger",
      "value": ">=2",
      "unit": {
        "state": "known",
        "value": "BI units of one command entering enemy ZOC",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    }
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Start of game; after trigger retained through remainder of that Game Turn, then lost."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D995momentum, G-D995scenario, G-D-ZOC-R995

**context-01 — pending / not_assessable**. Kandydaci: R995; osobny hash powyżej.

R995, pointer `/rules/44`, bajty [461228, 467103); hash zakresu `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Start of game: all BI have Impetuosity.",
    "At least two BI in leader’s command enter enemy ZOC."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "All BI MA +1 initially; BI-commanding leaders –1 to all first-try Momentum rolls.",
    "On two-unit enemy-ZOC trigger, lasts rest of Game Turn then lost; affects only that leader’s command per scenario."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E995"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "initial BI MA adjustment",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "MA",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "leader first-try Momentum modifier",
      "value": -1,
      "unit": {
        "state": "known",
        "value": "DRM",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    },
    {
      "name": "end-state trigger",
      "value": ">=2",
      "unit": {
        "state": "known",
        "value": "BI units of one command entering enemy ZOC",
        "evidence_ids": [
          "E995"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E995"
      ]
    }
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Start of game; after trigger retained through remainder of that Game Turn, then lost."
  ],
  "evidence_ids": [
    "E995"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D995momentum, G-D995scenario, G-D-ZOC-R995

### EXP-066 — M-POC5A.4

Dokładny zatwierdzony zakres: GallictransportCHCombatTablesignoreinstruction retained;exacttables/entriesrequirecontext alreadyRQ05scope

Wyłączenia/niepewności: Exact Combat Tables and relevant entries are required; no values are guessed.; Dokładne Combat Tables i ich chariot entries, decision owner o zakresie; nie traktować Sentinum/Telamon jako listy eligibility wszystkich LI.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, N-14-S2, bbox [319.0, 524.85, 563.026, 618.85]; dokładny source_span: "Thus, ignore the reference\nto Chariots on the Combat Tables.".

> DESIGN NOTE: The chariots used by the Gallic tribes were
> not, in any way, weapons systems. They were used only for
> transport. Their only resemblance to the war chariots of “days
> gone by” was that they had wheels. Thus, ignore the reference
> to Chariots on the Combat Tables. However, the tribes were
> quite adept at using them to whatever advantage they did of-
> fer. In this module, chariots make an appearance at Sentinum
> and Telamon.

Źródło PDF 36, right, N-14-S3, bbox [319.0, 524.85, 563.026, 618.85]; dokładny source_span: "However, the tribes were\nquite adept at using them to whatever advantage they did of-\nfer. In this module, chariots make an appearance at Sentinum\nand Telamon.".

> DESIGN NOTE: The chariots used by the Gallic tribes were
> not, in any way, weapons systems. They were used only for
> transport. Their only resemblance to the war chariots of “days
> gone by” was that they had wheels. Thus, ignore the reference
> to Chariots on the Combat Tables. However, the tribes were
> quite adept at using them to whatever advantage they did of-
> fer. In this module, chariots make an appearance at Sentinum
> and Telamon.

**first-001 — pending / not_assessable**. Kandydaci: N996design, R996note; osobny hash powyżej.

N996design, pointer `/nodes/30`, bajty [146679, 147468); hash zakresu `c01e2df13e259d2b65d4ec89dee199481937bd990757f3a83e9f9dc5ce3784dd`.

content:
```json
{
  "state": "known",
  "value": "Gallic chariots historically transport rather than weapons. Operative instruction to ignore Combat Table Chariot references and module appearances owned by R996note.",
  "evidence_ids": [
    "E996design"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996note, pointer `/rules/45`, bajty [392603, 396286); hash zakresu `3dfdaccd8a573ddf99e083715c467fb8a36ec4ad52929c71b7259de8de628ab5`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Thus, ignore the reference to Chariots on the Combat Tables."
  ],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
  "evidence_ids": [
    "E996note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
  "evidence_ids": [
    "E996note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996tables

**context-01 — pending / not_assessable**. Kandydaci: N996design, R996note; osobny hash powyżej.

N996design, pointer `/nodes/30`, bajty [195676, 196492); hash zakresu `7ad32edfe26a51d99e6ab415bbb1f85fc82f8061c5071dd33970b43437e5378f`.

content:
```json
{
  "state": "known",
  "value": "Gallic chariots historically transport rather than weapons. Operative instruction to ignore Combat Table Chariot references and module appearances owned by R996note.",
  "evidence_ids": [
    "E996design"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996note, pointer `/rules/45`, bajty [467110, 470918); hash zakresu `88c04eae1baf89929461610b1d701ea1201da58987d814350fdcfb5516d2ec76`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Thus, ignore the reference to Chariots on the Combat Tables."
  ],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
  "evidence_ids": [
    "E996note"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "No additional prerequisite stated in this identified clause.",
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
  "evidence_ids": [
    "E996note"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996note"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996tables

### EXP-067 — M-POC5A.4

Dokładny zatwierdzony zakres: CHonlyMA,noSize/TQ;cannotmoveincludingOWwithouteligibleLI;enemycombatmovingadjacenttosolitaryCH eliminatesit;staticadjacency notthegivenmovementtrigger

Wyłączenia/niepewności: Eligibility LI scenariuszowa nieuzupełniona; samotny CH da się ocenić lokalnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.96-02, bbox [315.0, 628.09, 567.019, 698.09]; dokładny source_span: null.

> Gallic Chariot (CH) units have only a Movement Allowance;
> they have no Size and no TQ Rating. These units cannot move
> at all, and this includes Orderly Withdrawal, unless stacked with
> an eligible Light Infantry (LI) unit. If an enemy combat unit (of
> any type) moves adjacent to a CH unit alone in a hex, the CH
> unit is immediately eliminated.

**first-001 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [396292, 400339); hash zakresu `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [400345, 409010); hash zakresu `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [409016, 413605); hash zakresu `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [413611, 417619); hash zakresu `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

**context-01 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [470925, 475124); hash zakresu `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [475131, 484102); hash zakresu `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [484109, 488868); hash zakresu `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [488875, 493035); hash zakresu `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

### EXP-068 — M-POC5A.4

Dokładny zatwierdzony zakres: oneLIperCH,CHtopdenotesmounted,combinedsingleforstackingbutotherrestrictionsretained

Wyłączenia/niepewności: Nie używać roman top/TQ jako zasad CH; brak TQ/Size CH zachować.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.96-03, bbox [315.0, 705.49, 567.026, 739.49]; dokładny source_span: null.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Źródło PDF 37, left, C-9.96-03, bbox [45.0, 54.004, 297.469, 220.004]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [396292, 400339); hash zakresu `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [400345, 409010); hash zakresu `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [409016, 413605); hash zakresu `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [413611, 417619); hash zakresu `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

**context-01 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [470925, 475124); hash zakresu `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [475131, 484102); hash zakresu `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [484109, 488868); hash zakresu `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [488875, 493035); hash zakresu `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

### EXP-069 — M-POC5A.4

Dokładny zatwierdzony zakres: mount/dismount0MP/CH;dismountcontinueonlyifcomboMPspent<LIprintedMA,remainingdifference;mountremainingCHMAminusLIalreadyusedMP

Wyłączenia/niepewności: Ocenia się lokalny budżet przy supplied eligibility, MA i MP; trasa wymaga tabeli.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.96-03, bbox [315.0, 705.49, 567.026, 739.49]; dokładny source_span: null.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Źródło PDF 37, left, C-9.96-03, bbox [45.0, 54.004, 297.469, 220.004]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [396292, 400339); hash zakresu `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [400345, 409010); hash zakresu `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [409016, 413605); hash zakresu `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [413611, 417619); hash zakresu `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

**context-01 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [470925, 475124); hash zakresu `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [475131, 484102); hash zakresu `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [484109, 488868); hash zakresu `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [488875, 493035); hash zakresu `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

### EXP-070 — M-POC5A.4

Dokładny zatwierdzony zakres: MovementCostChart governsCHMP/prohibitions;movementCohesionHitsLIonly,notCH;no waiverofterrainprohibitions

Wyłączenia/niepewności: Konkretna trasa bez Movement Cost Chart pozostaje zablokowana.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 36, right, C-9.96-03, bbox [315.0, 705.49, 567.026, 739.49]; dokładny source_span: null.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Źródło PDF 37, left, C-9.96-03, bbox [45.0, 54.004, 297.469, 220.004]; dokładny source_span: null.

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

**first-001 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [396292, 400339); hash zakresu `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [400345, 409010); hash zakresu `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [409016, 413605); hash zakresu `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [413611, 417619); hash zakresu `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

**context-01 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [470925, 475124); hash zakresu `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [475131, 484102); hash zakresu `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [484109, 488868); hash zakresu `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [488875, 493035); hash zakresu `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

### EXP-071 — M-POC5A.4

Dokładny zatwierdzony zakres: repeat-movementHitexceptiononlyentireOrdersPhasemounted;partialphasemountinsufficient

Wyłączenia/niepewności: General repeat movement i pozostałe terrain Hits oddzielnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 37, left, C-9.96-05, bbox [45.0, 254.284, 297.001, 288.284]; dokładny source_span: null.

> • LI do not suffer any Cohesion Hits for moving a second (and
> third) time in a Game Turn, if they spend the entire Orders
> Phase mounted on the CH unit.

**first-001 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [396292, 400339); hash zakresu `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [400345, 409010); hash zakresu `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [409016, 413605); hash zakresu `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [413611, 417619); hash zakresu `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

**context-01 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [470925, 475124); hash zakresu `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [475131, 484102); hash zakresu `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [484109, 488868); hash zakresu `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [488875, 493035); hash zakresu `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

### EXP-072 — M-POC5A.4

Dokładny zatwierdzony zakres: mountedLInoShockattack,mustdismount;defendsasLI,notfullattackpermissionafterdismount

Wyłączenia/niepewności: Dismount nie dowodzi legalności późniejszego attack bez pozostałych warunków.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 37, left, C-9.96-06, bbox [45.0, 291.724, 297.003, 313.724]; dokładny source_span: null.

> • LI cannot Shock attack; they must dismount to do so. When
> mounted, they defend as LI.

**first-001 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [396292, 400339); hash zakresu `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [400345, 409010); hash zakresu `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [409016, 413605); hash zakresu `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [413611, 417619); hash zakresu `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

**context-01 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [470925, 475124); hash zakresu `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [475131, 484102); hash zakresu `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [484109, 488868); hash zakresu `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [488875, 493035); hash zakresu `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

### EXP-073 — M-POC5A.4

Dokładny zatwierdzony zakres: Mounted LI uses Mounted Javelin MRRC, is exempt from Missile Supply 8.17 while mounted, removes LOW/NO on mounting, and uses H&D as cavalry. No post-dismount supply state or equivalence with the hypothesized 9.13 row is inferred.

Wyłączenia/niepewności: Nie zgadywać podaży po późniejszym dismount ani pełnego MRRC/H&D; display annotation06c zachowuje original helper.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 37, left, C-9.96-07, bbox [45.0, 317.164, 297.05, 375.164]; dokładny source_span: null.

> • LI may use Missile Fire using the Mounted Javelin row on the
> MRRC. Missile Supply (8.17) does not apply while the LI unit
> is mounted. Remove any MiSSile low/No markers from the LI
> unit when the unit mounts a CH. They may use Harassment
> and Dispersal fire as if they were cavalry units.

**first-001 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [396292, 400339); hash zakresu `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [400345, 409010); hash zakresu `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [409016, 413605); hash zakresu `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [413611, 417619); hash zakresu `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

**context-01 — pending / not_assessable**. Kandydaci: R996a, R996b, R996c, R996d; osobny hash powyżej.

R996a, pointer `/rules/46`, bajty [470925, 475124); hash zakresu `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "CH must be stacked with eligible LI to move, including OW."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "CH only has MA, no Size/TQ.",
    "Cannot move at all unless carrying eligible LI.",
    "Enemy combat unit of any type moving adjacent to CH alone immediately eliminates it."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Movement allowed when stacked with eligible LI."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996a"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Immediate elimination on qualifying enemy adjacency."
  ],
  "evidence_ids": [
    "E996a"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996b, pointer `/rules/47`, bajty [475131, 484102); hash zakresu `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Each CH unit may carry one Light Infantry (LI) unit.",
    "There is no MP or Cohesion Hit cost to the LI unit to either mount or dismount from a CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "Eligible LI mounted/dismounting CH; post-dismount continuation only below printed LI MA."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "Carry one LI; place CH above LI to denote mounted status; combined stack is one unit for stacking.",
    "Other restrictions apply both to CH+LI and CH alone.",
    "Mount/dismount costs LI no MP or Hits.",
    "Dismounting LI may continue only if combined movement < printed LI MA; MP remaining is difference.",
    "Mounting LI may continue as CH up to CH MA minus MPs already used by LI.",
    "Mounted CH pays/obeys Movement Cost Chart terrain costs/prohibitions; movement Hits only LI, never CH."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "CH suffers no Movement/Terrain Hits; LI takes movement Hits.",
    "Other stacking restrictions still apply."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "CH capacity",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "Light Infantry unit",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "stack count",
      "value": 1,
      "unit": {
        "state": "known",
        "value": "unit for stacking purposes",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount MP",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "mount/dismount Hits",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-dismount remaining",
      "value": "LI printed MA – combined MPs used, only if used < LI printed MA",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    },
    {
      "name": "post-mount remaining",
      "value": "CH MA – LI MPs already used",
      "unit": {
        "state": "known",
        "value": "MP",
        "evidence_ids": [
          "E996b",
          "E996c"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996b",
        "E996c"
      ]
    }
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "During mount/dismount continuation."
  ],
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996c, pointer `/rules/48`, bajty [484109, 488868); hash zakresu `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

transcription:
```json
{
  "state": "known",
  "value": [
    "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "No second/third movement Hits in Game Turn if mounted entire Orders Phase.",
    "Mounted LI cannot Shock attack; must dismount; defends as LI."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "No exception stated within this identified clause; external rules may qualify it.",
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "known",
  "value": [
    {
      "name": "repeated mounted movement",
      "value": [
        "second",
        "third"
      ],
      "unit": {
        "state": "known",
        "value": "movement occurrence in Game Turn",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    },
    {
      "name": "repeated-movement penalty",
      "value": 0,
      "unit": {
        "state": "known",
        "value": "Cohesion Hits",
        "evidence_ids": [
          "E996d"
        ],
        "reason": null,
        "gap_ids": []
      },
      "evidence_ids": [
        "E996d"
      ]
    }
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": "Locally stated numerical parameters; unavailable referenced procedure/table values remain gaps.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "Entire Orders Phase mounted; second and third movement in Game Turn."
  ],
  "evidence_ids": [
    "E996d"
  ],
  "reason": null,
  "gap_ids": []
}
```

R996d, pointer `/rules/49`, bajty [488875, 493035); hash zakresu `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

transcription:
```json
{
  "state": "known",
  "value": [
    "Missile Supply (8.17) does not apply while the LI unit is mounted."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
  "gap_ids": []
}
```

interpretation:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
  "gap_ids": []
}
```

conditions:
```json
{
  "state": "known",
  "value": [
    "LI mounted on CH."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

action_effect:
```json
{
  "state": "known",
  "value": [
    "May Missile Fire using Mounted Javelin MRRC row.",
    "Missile Supply does not apply while mounted; remove Missile Low/No markers when LI mounts.",
    "May Harassment and Dispersal fire as cavalry."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

exceptions:
```json
{
  "state": "known",
  "value": [
    "Mounted LI exempt from Missile Supply."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

parameters:
```json
{
  "state": "established_absent",
  "value": [],
  "evidence_ids": [
    "E996e"
  ],
  "reason": "No numerical parameter stated within this identified clause.",
  "gap_ids": []
}
```

time_limits:
```json
{
  "state": "known",
  "value": [
    "While mounted; remove supply markers on mounting."
  ],
  "evidence_ids": [
    "E996e"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): G-D996eligible, G-D996OW, G-D996stack, G-D996movement, G-D996MRRC, G-D996supply, G-D996HD

### EXP-074 — M-POC5A.4

Dokładny zatwierdzony zakres: Confirm actualidentifiedunit TQ/MA before concreteuse; not alltinygraphicratings were individuallyverified inthisreview. SyntheticinputTQ6 doesnotestablishactualLeaderElephantTQ. Keeprequires_context foractualvalues.

Wyłączenia/niepewności: Actual identified counter TQ/MA and glyph values remain unconfirmed; criticality is conditional on changing outcome or legality.; Wybrany żeton/parametr z dokładnym źródłem i przeglądem, tylko jeśli sytuacja go potrzebuje.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

Źródło PDF 31, right, G-01, bbox [315, 482, 352, 521]; dokładny source_span: null.

> 

Źródło PDF 33, right, G-02, bbox [315, 239, 352, 276]; dokładny source_span: null.

> 

Źródło PDF 36, left, G-03, bbox [45, 71, 82, 109]; dokładny source_span: null.

> 

Źródło PDF 35, left, D-02, bbox [80, 516, 266, 674]; dokładny source_span: null.

> 

Źródło PDF 36, left, G-04, bbox [45, 365, 120, 404]; dokładny source_span: null.

> 

Źródło PDF 36, left, G-05, bbox [260, 528, 297, 566]; dokładny source_span: null.

> 

**first-001 — pending / not_assessable**. Kandydaci: N911counter, N921counter, N966diagram, N981counter, N985markers, N986marker; osobny hash powyżej.

N911counter, pointer `/nodes/31`, bajty [147474, 148541); hash zakresu `23d5455d6e3e846f2793ab9162a4d52e351dec50fdbb6c82f9bbdf60726cf009`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "visible_text": [
        "Africa",
        "15",
        "J",
        "a",
        "5",
        "EL",
        "5",
        "7"
      ]
    },
    "interpretation": "Illustrative counter. Numerical glyphs retained as displayed; no game-wide values or rating-position meanings inferred. Weapon/icon geometry remains in cited image."
  },
  "evidence_ids": [
    "E911counter"
  ],
  "reason": null,
  "gap_ids": []
}
```

N921counter, pointer `/nodes/32`, bajty [148547, 149599); hash zakresu `30e857892be2b6c8be03571a7cf4d4176065f50d0ebbc1464ce5742405a3dc86`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "visible_text": [
        "Bal'ric",
        "6",
        "S",
        "1",
        "SK",
        "3",
        "6"
      ]
    },
    "interpretation": "Illustrative counter. Numerical glyphs retained as displayed; no game-wide values or rating-position meanings inferred. Weapon/icon geometry remains in cited image."
  },
  "evidence_ids": [
    "E921counter"
  ],
  "reason": null,
  "gap_ids": []
}
```

N966diagram, pointer `/nodes/7`, bajty [128977, 130323); hash zakresu `f5c32b1dae24067c8069c9f6a259e1da4cd473f61255ce80b5b070a71cc69689`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "captions": [
        "Original Deployment",
        "After Manipular Line Extension"
      ],
      "top_panel": "Two separated stacks; curved arrows point sideways right into adjacent empty hexes.",
      "bottom_panel": "Four single counters in adjacent hexes, labeled I a, I b, I c, I d.",
      "counter_text": [
        "HA",
        "J",
        "3",
        "LG",
        "7",
        "5"
      ]
    },
    "interpretation": "Illustration shows unstacking each top unit into vacant side hex, preserving facing. Numeric counter ratings are illustrative and are not general Roman unit parameters."
  },
  "evidence_ids": [
    "E966diagram"
  ],
  "reason": null,
  "gap_ids": []
}
```

N981counter, pointer `/nodes/33`, bajty [149605, 150636); hash zakresu `5598ad644a67222e29a3ec1778f8d63074add8759087c77097a583b05c918b7b`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "visible_text": [
        "Scorpio",
        "1",
        "LI",
        "1",
        "2",
        "3"
      ]
    },
    "interpretation": "Illustrative counter. Numerical glyphs retained as displayed; no game-wide values or rating-position meanings inferred. Weapon/icon geometry remains in cited image."
  },
  "evidence_ids": [
    "E981counter"
  ],
  "reason": null,
  "gap_ids": []
}
```

N985markers, pointer `/nodes/34`, bajty [150642, 151434); hash zakresu `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": [
      "Active Fire Once",
      "Active Fire Finished"
    ],
    "interpretation": "Once and Finished marker faces illustrate the two-stage Active Fire status."
  },
  "evidence_ids": [
    "E985markers"
  ],
  "reason": null,
  "gap_ids": []
}
```

N986marker, pointer `/nodes/35`, bajty [151440, 152165); hash zakresu `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "Reaction Fire Once",
    "interpretation": "Only Once face pictured here; Finished face is specified in prose R986."
  },
  "evidence_ids": [
    "E986marker"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

**context-01 — pending / not_assessable**. Kandydaci: N911counter, N921counter, N966diagram, N981counter, N985markers, N986marker; osobny hash powyżej.

N911counter, pointer `/nodes/31`, bajty [196499, 197607); hash zakresu `7b6b333e688ac23f557a2c1e1344876b6770501901c9407247d341dac0c97653`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "visible_text": [
        "Africa",
        "15",
        "J",
        "a",
        "5",
        "EL",
        "5",
        "7"
      ]
    },
    "interpretation": "Illustrative counter. Numerical glyphs retained as displayed; no game-wide values or rating-position meanings inferred. Weapon/icon geometry remains in cited image."
  },
  "evidence_ids": [
    "E911counter"
  ],
  "reason": null,
  "gap_ids": []
}
```

N921counter, pointer `/nodes/32`, bajty [197614, 198706); hash zakresu `0c1388f9709c55e4e5a45fc7686880da9f5078247249284e32ca56de85771f8b`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "visible_text": [
        "Bal'ric",
        "6",
        "S",
        "1",
        "SK",
        "3",
        "6"
      ]
    },
    "interpretation": "Illustrative counter. Numerical glyphs retained as displayed; no game-wide values or rating-position meanings inferred. Weapon/icon geometry remains in cited image."
  },
  "evidence_ids": [
    "E921counter"
  ],
  "reason": null,
  "gap_ids": []
}
```

N966diagram, pointer `/nodes/7`, bajty [177283, 178673); hash zakresu `36e8f4cd62347156e4d08983cd3b50a484a73b8478deddb5b4167d954c4d364d`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "captions": [
        "Original Deployment",
        "After Manipular Line Extension"
      ],
      "top_panel": "Two separated stacks; curved arrows point sideways right into adjacent empty hexes.",
      "bottom_panel": "Four single counters in adjacent hexes, labeled I a, I b, I c, I d.",
      "counter_text": [
        "HA",
        "J",
        "3",
        "LG",
        "7",
        "5"
      ]
    },
    "interpretation": "Illustration shows unstacking each top unit into vacant side hex, preserving facing. Numeric counter ratings are illustrative and are not general Roman unit parameters."
  },
  "evidence_ids": [
    "E966diagram"
  ],
  "reason": null,
  "gap_ids": []
}
```

N981counter, pointer `/nodes/33`, bajty [198713, 199783); hash zakresu `a40fc3ffd54bad133ba38846aeb3aab44303b5e8c073a04740d3cbc39f922451`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": {
      "visible_text": [
        "Scorpio",
        "1",
        "LI",
        "1",
        "2",
        "3"
      ]
    },
    "interpretation": "Illustrative counter. Numerical glyphs retained as displayed; no game-wide values or rating-position meanings inferred. Weapon/icon geometry remains in cited image."
  },
  "evidence_ids": [
    "E981counter"
  ],
  "reason": null,
  "gap_ids": []
}
```

N985markers, pointer `/nodes/34`, bajty [199790, 200614); hash zakresu `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": [
      "Active Fire Once",
      "Active Fire Finished"
    ],
    "interpretation": "Once and Finished marker faces illustrate the two-stage Active Fire status."
  },
  "evidence_ids": [
    "E985markers"
  ],
  "reason": null,
  "gap_ids": []
}
```

N986marker, pointer `/nodes/35`, bajty [200621, 201375); hash zakresu `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.

content:
```json
{
  "state": "known",
  "value": {
    "transcription": "Reaction Fire Once",
    "interpretation": "Only Once face pictured here; Finished face is specified in prose R986."
  },
  "evidence_ids": [
    "E986marker"
  ],
  "reason": null,
  "gap_ids": []
}
```

Deklaracje blokad (do oceny w dokładnym zakresie, nie automatyczna blokada lokalnych faktów): 

## Inwentarz — wszystkie 207 pozycji

Dokładny frozen_item z transkrypcją, source_span, obrazem/hashem/bbox oraz osobnymi mapami obu odpowiedzi jest w checklist.inventory. Poniższy indeks nie nadaje akceptacji znaczenia.

| ID | Typ | first-001 kandydaci | context-01 kandydaci | Zakres review |
|---|---|---|---|---|
| H-9.0 | chapter_heading | N90 | N90 | M-POC5A.4; pending |
| H-9.1 | section_heading | N91 | N91 | M-POC5A.4; pending |
| H-9.2 | section_heading | N92 | N92 | M-POC5A.4; pending |
| H-9.3 | section_heading | N93 | N93 | M-POC5A.4; pending |
| H-9.4 | section_heading | N94 | N94 | M-POC5A.4; pending |
| H-9.5 | section_heading | N95 | N95 | M-POC5A.4; pending |
| H-9.6 | section_heading | N96 | N96 | M-POC5A.4; pending |
| H-9.7 | section_heading | N97 | N97 | M-POC5A.4; pending |
| H-9.8 | section_heading | N98 | N98 | M-POC5A.4; pending |
| H-9.9 | section_heading | N99 | N99 | M-POC5A.4; pending |
| R-9.11 | rule_label | R911 | R911 | M-POC5A.4; pending |
| C-9.11-01 | clause_group | R911 | R911 | EXP-001 |
| C-9.11-02 | clause_group | R911 | R911 | EXP-001 |
| C-9.11-03 | clause_group | R911 | R911 | EXP-001 |
| C-9.11-04 | clause_group | R911 | R911 | EXP-001 |
| C-9.11-05 | clause_group | R911 | R911 | EXP-001 |
| C-9.11-06 | clause_group | R911 | R911 | M-POC5A.4; pending |
| C-9.11-07 | clause_group | R911 | R911 | EXP-002 |
| C-9.11-08 | clause_group | R911 | R911 | EXP-002 |
| C-9.11-09 | clause_group | R911 | R911 | EXP-003 |
| C-9.11-10 | clause_group | R911 | R911 | EXP-004 |
| R-9.12 | rule_label | R912 | R912 | M-POC5A.4; pending |
| C-9.12-01 | clause_group | R912 | R912 | M-POC5A.4; pending |
| C-9.12-02 | clause_group | R912 | R912 | EXP-005 |
| C-9.12-03 | clause_group | R912 | R912 | EXP-005 |
| R-9.13 | rule_label | R913 | R913 | M-POC5A.4; pending |
| C-9.13-01 | clause_group | R913 | R913 | EXP-006 |
| R-9.14 | rule_label | R914 | R914 | M-POC5A.4; pending |
| C-9.14-01 | clause_group | R914 | R914 | EXP-007 |
| C-9.14-02 | clause_group | R914 | R914 | EXP-011 |
| C-9.14-03 | clause_group | R914 | R914 | EXP-012 |
| C-9.14-04 | clause_group | R914 | R914 | EXP-012 |
| C-9.14-05 | clause_group | R914 | R914 | M-POC5A.4; pending |
| C-9.14-06 | clause_group | R914 | R914 | EXP-013 |
| C-9.14-07 | clause_group | R914 | R914 | EXP-013 |
| C-9.14-08 | clause_group | R914 | R914 | EXP-013 |
| C-9.14-09 | clause_group | R914 | R914 | EXP-013 |
| C-9.14-10 | clause_group | R914 | R914 | EXP-014 |
| C-9.14-11 | clause_group | R914 | R914 | EXP-008,EXP-009,EXP-011 |
| R-9.15 | rule_label | R915 | R915 | M-POC5A.4; pending |
| C-9.15-01 | clause_group | R915 | R915 | EXP-015 |
| R-9.16 | rule_label | R916 | R916 | M-POC5A.4; pending |
| C-9.16-01 | clause_group | R916 | R916 | EXP-016,EXP-017 |
| R-9.17 | rule_label | R917 | R917 | M-POC5A.4; pending |
| C-9.17-01 | clause_group | R917 | R917 | EXP-018 |
| R-9.18 | rule_label | R918 | R918 | M-POC5A.4; pending |
| C-9.18-01 | clause_group | R918 | R918 | EXP-019 |
| R-9.19 | rule_label | R919 | R919 | M-POC5A.4; pending |
| C-9.19-01 | clause_group | R919 | R919 | EXP-020 |
| R-9.21 | rule_label | R921 | R921 | M-POC5A.4; pending |
| C-9.21-01 | clause_group | R921 | R921 | EXP-021,EXP-022 |
| R-9.22 | rule_label | R922 | R922 | M-POC5A.4; pending |
| C-9.22-01 | clause_group | R922 | R922 | EXP-023 |
| R-9.23 | rule_label | R923 | R923 | M-POC5A.4; pending |
| C-9.23-01 | clause_group | R923 | R923 | M-POC5A.4; pending |
| C-9.23-02 | clause_group | R923 | R923 | EXP-024 |
| C-9.23-03 | clause_group | R923 | R923 | EXP-024 |
| C-9.23-04 | clause_group | R923 | R923 | EXP-024 |
| C-9.23-05 | clause_group | R923 | R923 | EXP-025 |
| C-9.23-06 | clause_group | R923 | R923 | EXP-026 |
| R-9.24 | rule_label | R924 | R924 | M-POC5A.4; pending |
| C-9.24-01 | clause_group | R924 | R924 | M-POC5A.4; pending |
| C-9.24-02 | clause_group | R924 | R924 | EXP-027 |
| C-9.24-03 | clause_group | R924 | R924 | EXP-004 |
| C-9.24-04 | clause_group | R924 | R924 | EXP-027 |
| C-9.24-05 | clause_group | R924 | R924 | EXP-028 |
| R-9.31 | rule_label | R931 | R931 | M-POC5A.4; pending |
| C-9.31-01 | clause_group | R931 | R931 | EXP-029 |
| R-9.32 | rule_label | R932 | R932 | M-POC5A.4; pending |
| C-9.32-01 | clause_group | R932 | R932 | EXP-030,EXP-031 |
| R-9.41 | rule_label | R941 | R941 | M-POC5A.4; pending |
| C-9.41-01 | clause_group | R941 | R941 | EXP-032,EXP-038 |
| R-9.51 | rule_label | R951 | R951 | M-POC5A.4; pending |
| C-9.51-01 | clause_group | R951 | R951 | EXP-033,EXP-034 |
| R-9.52 | rule_label | R952 | R952 | M-POC5A.4; pending |
| C-9.52-01 | clause_group | R952 | R952 | M-POC5A.4; pending |
| C-9.52-02 | clause_group | R952 | R952 | EXP-035 |
| C-9.52-03 | clause_group | R952 | R952 | EXP-035 |
| C-9.52-04 | clause_group | R952 | R952 | EXP-035 |
| C-9.52-05 | clause_group | R952 | R952 | EXP-036 |
| C-9.52-06 | clause_group | R952 | R952 | EXP-036 |
| R-9.53 | rule_label | R953 | R953 | M-POC5A.4; pending |
| C-9.53-01 | clause_group | R953 | R953 | M-POC5A.4; pending |
| C-9.53-02 | clause_group | R953 | R953 | EXP-037 |
| C-9.53-03 | clause_group | R953 | R953 | EXP-037 |
| C-9.53-04 | clause_group | R953 | R953 | EXP-038 |
| C-9.53-05 | clause_group | R953 | R953 | EXP-038 |
| C-9.53-06 | clause_group | R953 | R953 | EXP-039 |
| C-9.53-07 | clause_group | R953 | R953 | EXP-039 |
| C-9.53-08 | clause_group | R953 | R953 | EXP-040 |
| R-9.61 | rule_label | R961 | R961 | M-POC5A.4; pending |
| C-9.61-01 | clause_group | R961 | R961 | EXP-041 |
| R-9.62 | rule_label | R962 | R962 | M-POC5A.4; pending |
| C-9.62-01 | clause_group | R962 | R962 | EXP-042 |
| R-9.63 | rule_label | R963 | R963 | M-POC5A.4; pending |
| C-9.63-01 | clause_group | R963 | R963 | EXP-043 |
| R-9.64 | rule_label | R964 | R964 | M-POC5A.4; pending |
| C-9.64-01 | clause_group | R964 | R964 | EXP-044 |
| R-9.65 | rule_label | R965 | R965 | M-POC5A.4; pending |
| C-9.65-01 | clause_group | R965 | R965 | EXP-045 |
| R-9.66 | rule_label | R966 | R966 | M-POC5A.4; pending |
| C-9.66-01 | clause_group | R966 | R966 | M-POC5A.4; pending |
| R-9.67 | rule_label | R967 | R967 | M-POC5A.4; pending |
| C-9.67-01 | clause_group | R967 | R967 | EXP-047 |
| R-9.68 | rule_label | R968 | R968 | M-POC5A.4; pending |
| C-9.68-01 | clause_group | R968 | R968 | EXP-048 |
| R-9.71 | rule_label | R971 | R971 | M-POC5A.4; pending |
| C-9.71-01 | clause_group | R971 | R971 | EXP-050,EXP-051 |
| C-9.71-02 | clause_group | R971 | R971 | EXP-051 |
| C-9.71-03 | clause_group | R971 | R971 | EXP-051 |
| R-9.72 | rule_label | R972 | R972 | M-POC5A.4; pending |
| C-9.72-01 | clause_group | R972 | R972 | EXP-050,EXP-052 |
| R-9.81 | rule_label | R981 | R981 | M-POC5A.4; pending |
| C-9.81-01 | clause_group | R981 | R981 | EXP-053 |
| R-9.82 | rule_label | R982 | R982 | M-POC5A.4; pending |
| C-9.82-01 | clause_group | R982 | R982 | EXP-054 |
| R-9.83 | rule_label | R983 | R983 | M-POC5A.4; pending |
| C-9.83-01 | clause_group | R983 | R983 | EXP-055 |
| R-9.84 | rule_label | R984 | R984 | M-POC5A.4; pending |
| C-9.84-01 | clause_group | R984 | R984 | EXP-056 |
| R-9.85 | rule_label | R985 | R985 | M-POC5A.4; pending |
| C-9.85-01 | clause_group | R985 | R985 | EXP-057 |
| R-9.86 | rule_label | R986 | R986 | M-POC5A.4; pending |
| C-9.86-01 | clause_group | R986 | R986 | EXP-058 |
| R-9.87 | rule_label | R987 | R987 | M-POC5A.4; pending |
| C-9.87-01 | clause_group | R987 | R987 | EXP-059 |
| R-9.91 | rule_label | R991 | R991 | M-POC5A.4; pending |
| C-9.91-01 | clause_group | R991 | R991 | M-POC5A.4; pending |
| C-9.91-02 | clause_group | R991 | R991 | EXP-060 |
| R-9.93 | rule_label | R993 | R993 | M-POC5A.4; pending |
| C-9.93-01 | clause_group | R993 | R993 | M-POC5A.4; pending |
| C-9.93-02 | clause_group | R993 | R993 | EXP-061 |
| C-9.93-03 | clause_group | R993 | R993 | EXP-061 |
| R-9.94 | rule_label | R994 | R994 | M-POC5A.4; pending |
| C-9.94-01 | clause_group | R994 | R994 | M-POC5A.4; pending |
| C-9.94-02 | clause_group | R994 | R994 | EXP-062 |
| C-9.94-03 | clause_group | R994 | R994 | EXP-063,EXP-064 |
| R-9.95 | rule_label | R995 | R995 | M-POC5A.4; pending |
| C-9.95-01 | clause_group | R995 | R995 | M-POC5A.4; pending |
| C-9.95-02 | clause_group | R995 | R995 | EXP-064,EXP-065 |
| R-9.96 | rule_label | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | M-POC5A.4; pending |
| C-9.96-01 | clause_group | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | M-POC5A.4; pending |
| C-9.96-02 | clause_group | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | EXP-067 |
| C-9.96-03 | clause_group | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | EXP-068,EXP-069,EXP-070 |
| C-9.96-04 | clause_group | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | M-POC5A.4; pending |
| C-9.96-05 | clause_group | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | EXP-071 |
| C-9.96-06 | clause_group | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | EXP-072 |
| C-9.96-07 | clause_group | R996a,R996b,R996c,R996d | R996a,R996b,R996c,R996d | EXP-073 |
| C-9.7-01 | clause_group | R97intro | R97intro | M-POC5A.4; pending |
| N-01 | note | N91hist | N91hist | M-POC5A.4; pending |
| N-02 | note | N911design | N911design | M-POC5A.4; pending |
| N-03 | note | R913note | R913note | M-POC5A.4; pending |
| N-04 | note | N914design | N914design | M-POC5A.4; pending |
| N-05 | note | N917hist | N917hist | M-POC5A.4; pending |
| N-06 | note | N919hist | N919hist | M-POC5A.4; pending |
| N-07 | note | R92note,N92design | R92note,N92design | M-POC5A.4; pending |
| N-08 | note | N941design | N941design | M-POC5A.4; pending |
| N-09 | note | R95note,N95design | R95note,N95design | M-POC5A.4; pending |
| N-10 | note | N96hist | N96hist | M-POC5A.4; pending |
| N-11 | note | R982note | R982note | EXP-054 |
| N-12 | note | N99design | N99design | M-POC5A.4; pending |
| N-13 | note | N994design | N994design | M-POC5A.4; pending |
| N-14 | note | R996note,N996design | R996note,N996design | M-POC5A.4; pending |
| X-01 | caption | N914diagram | N914diagram | EXP-010 |
| X-02 | example | N923ex | N923ex | M-POC5A.4; pending |
| X-03 | example | N924ex | N924ex | EXP-028 |
| X-04 | example | N932ex | N932ex | EXP-031 |
| X-05 | example | N941ex | N941ex | M-POC5A.4; pending |
| X-06 | example | N953ex | N953ex | EXP-033 |
| X-07 | example | N967ex | N967ex | EXP-047 |
| T-01 | table | N914table | N914table | EXP-007 |
| TR-01 | table_row | N914table | N914table | EXP-007,EXP-008 |
| TR-02 | table_row | N914table | N914table | EXP-007,EXP-010 |
| TR-03 | table_row | N914table | N914table | EXP-007,EXP-008,EXP-009 |
| D-01 | diagram | N914diagram | N914diagram | EXP-010 |
| D-02 | diagram | N966diagram | N966diagram | EXP-046,EXP-074 |
| CAP-01 | caption | N966diagram | N966diagram | EXP-046 |
| CAP-02 | caption | N966diagram | N966diagram | EXP-046 |
| G-01 | counter_illustration | N911counter | N911counter | EXP-074 |
| G-02 | counter_illustration | N921counter | N921counter | EXP-074 |
| G-03 | counter_illustration | N981counter | N981counter | EXP-074 |
| G-04 | marker_illustration | N985markers | N985markers | EXP-057,EXP-074 |
| G-05 | marker_illustration | N986marker | N986marker | EXP-058,EXP-074 |
| K-01 | continuation | N911first,N911next | N911first,N911next | M-POC5A.4; pending |
| K-02 | continuation | N914tablefirst,N914tablenext | N914tablefirst,N914tablenext | M-POC5A.4; pending |
| K-03 | continuation | N914first,N914next | N914first,N914next | M-POC5A.4; pending |
| K-04 | continuation | N924first,N924next | N924first,N924next | M-POC5A.4; pending |
| K-05 | continuation | N966first,N966next | N966first,N966next | M-POC5A.4; pending |
| K-06 | continuation | N991first,N991next | N991first,N991next | M-POC5A.4; pending |
| K-07 | continuation | N996first,N996next | N996first,N996next | M-POC5A.4; pending |
| N-14-S1 | note_text_span | R996note,N996design | R996note,N996design | M-POC5A.4; pending |
| N-14-S2 | note_text_span | R996note,N996design | R996note,N996design | EXP-066 |
| N-14-S3 | note_text_span | R996note,N996design | R996note,N996design | EXP-066 |
| N-03-S1 | note_text_span | R913note | R913note | M-POC5A.4; pending |
| N-03-S2 | note_text_span | R913note | R913note | EXP-006 |
| N-07-S1 | note_text_span | R92note,N92design | R92note,N92design | M-POC5A.4; pending |
| N-07-S2 | note_text_span | R92note,N92design | R92note,N92design | EXP-021 |
| N-09-S1 | note_text_span | R95note,N95design | R95note,N95design | M-POC5A.4; pending |
| N-09-S2 | note_text_span | R95note,N95design | R95note,N95design | EXP-033 |
| C-9.66-01-S1 | clause_text_span | R966 | R966 | EXP-046 |
| C-9.66-01-S2 | clause_text_span | R966 | R966 | EXP-046 |
| C-9.66-01-S3 | clause_text_span | R966 | R966 | EXP-046 |
| C-9.66-01-S4 | clause_text_span | R966 | R966 | EXP-046 |
| C-9.66-01-S5 | clause_text_span | R966 | R966 | EXP-046 |
| C-9.66-01-S6 | clause_text_span | R966 | R966 | EXP-046 |
| C-9.7-01-S1 | clause_text_span | R97intro | R97intro | EXP-049,EXP-050 |
| C-9.7-01-S2 | clause_text_span | R97intro | R97intro | M-POC5A.4; pending |

## Relacje, lokatory i metryki

5 jawnych i 3 niejawne pary wykonawcze, 7 wzmianek i 7 kontynuacji zachowują mianowniki. 105 kandydatur pozostaje poza gold. Wszystkie 126/131 proponowanych krawędzi mają osobne pending; TP_gold, TP_output, FP, FN i precision/recall pozostają not_assessable.

64 granice glifów i dziedziczony E916 wymagają osobnego zakresu review; 111 krótkich cytatów i valid geometry nie certyfikują całej treści. Rubryki: 41/38/43/66/52/29/7/1 oraz dwa osobne stany ilustracji.

Krytyczny brak źródła blokuje pełny zależny wynik; nie blokuje automatycznie lokalnego wyniku z zadanymi faktami. Bez nowych źródeł, pass-02, ekstrakcji, korekt i oceny 20 sytuacji.

Ścieżka 3 krawędzi kończy się brakującym celem; stop pozyskiwania na 2 zachowany, bez certyfikatu całego grafu. 1 strona/1 reguła/0 tabel, 1 runda kontekstu, 0 korekt.

Niezależnie potwierdzono listing/path discovery poza allowlistą w context-01. Odczyt treści oceny niezaobserwowany; ekspozycja i czysty kontekst unknown, bez dowodu skażenia lub pełnej izolacji. Historyczne first-001, selektory, aktywny czas/budżet, tokeny/cena unknown. Kalendarz nie mierzy aktywnego budżetu.

Kontrole i końcowe zachowanie bajtów prowadzi nowy measurement/M-POC5A-semantic-01/completion.json; zamkniętych raportów nie aktualizowano.

Wznowienie: decyzje właściciela SEM-001/002/003, następnie pierwsze pending części .2–.4. Nie przenosić akceptacji M-POC4B na znaczenie.
