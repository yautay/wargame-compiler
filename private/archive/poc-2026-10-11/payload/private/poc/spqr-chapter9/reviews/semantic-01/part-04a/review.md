# M-POC5A.4a — porównania EXP-051–074

Oceniający: Codex. Każda nowa propozycja dla każdego hasha pozostaje pending/waiting_review; znaczenie akceptuje właściciel. Dawne 43 lokalne zakresy i 2 wymagania źródła na wynik zachowane.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`; PDF `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

first-001: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

[Pełny ślad JSON](comparisons.json) zawiera osobne oceny obu hashów, JSON pointers, zakresy rekordów i pól UTF-8 [start,end), SHA-256 fragmentów, źródła i zakresy decyzji. Cytaty literalne są oddzielone od podsumowań i interpretacji. Koperty źródeł nie rozszerzają reviewed_scope.

Propozycje: 20 lokalnych zgodności, 1 właściwa potrzeba/blokada źródła (EXP-064); 3 kwestie do osobnej decyzji (EXP-052/066/074). 31 powiązanych pozycji źródła, 95 diagnostycznych par rubryka/EXP. To nie zaakceptowane wyniki jakości.

## Porównania i dowody

### EXP-051

Zakres oceny: movementgate9.71cannotmovebutmayface untiloneofORtriggers:enemycombatnotELwithin3andLOSanyTriariilineunit ORTriarii>=6fromallRoman/Alainfantrylinesexcludingallied

Porównanie oceniającego: R971 zachowuje zakaz ruchu i możliwość facing przed zwolnieniem. Bramka 9.71 ma OR: enemy combat nie-EL w odległości do 3 heksów AND LOS dowolnej jednostki linii Triarii, albo odległość co najmniej 6 od wszystkich innych Roman/Ala infantry lines, z wyłączeniem allied. Nie zastąpiono any przez all, OR przez AND ani >=6 przez >6. To lokalna bramka, bez ogólnego zezwolenia na move+Shock i bez akceptacji relacji 9.72→9.71.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.71-01, PDF 35 right, bbox [315.0, 447.573, 567.0, 469.573], render SHA-256 `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.71 Triarii units cannot move, but may change facing, until and
> unless one of the following occurs:

Źródło C-9.71-02, PDF 35 right, bbox [315.0, 474.453, 567.03, 508.453], render SHA-256 `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> • There is an enemy combat unit, other than an Elephant unit,
> which is within 3 hexes and LOS of any unit in the Triarii line,
> or

Źródło C-9.71-03, PDF 35 right, bbox [315.0, 511.893, 567.022, 545.893], render SHA-256 `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> • The Triarii units are at least 6 hexes from all other Roman or
> Ala—but not allied–infantry lines, be they Hastati, Principes
> or whatever.

**first-001 — osobna propozycja i ślady**

first-001 R971, `/rules/31`, bajty [330949,335849), SHA-256 `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.

```json
{
  "id": "R971",
  "original_label": {
    "state": "known",
    "value": "9.71",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R971-C1",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "Movement prohibition/facing permission"
    },
    {
      "local_clause_id": "R971-C2",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 1 — proximity and LOS"
    },
    {
      "local_clause_id": "R971-C3",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 2 — separation"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "known",
    "value": [
      "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Triarii",
      "enemy combat units except Elephants",
      "Roman/Ala infantry lines",
      "allied infantry"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.71"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Until and unless either trigger occurs."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E971"
  ],
  "gap_ids": [
    "G-D971LOS"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D971LOS, `/gaps/53`, bajty [554574,555022), SHA-256 `0fbbec450f17ca03c3aabeaeee56e5ba736da2a160154409128713bb125171b7`.

```json
{
  "id": "G-D971LOS",
  "class": "missing_context",
  "affected_ids": [
    "R971",
    "D971LOS"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "LOS test necessary for enemy proximity release is referenced but unavailable.",
  "needed_context": "Line of Sight rules",
  "blocking": true,
  "evidence_ids": [
    "E971"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R971, `/rules/31`, bajty [403209,408288), SHA-256 `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.

```json
{
  "id": "R971",
  "original_label": {
    "state": "known",
    "value": "9.71",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R971-C1",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "Movement prohibition/facing permission"
    },
    {
      "local_clause_id": "R971-C2",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 1 — proximity and LOS"
    },
    {
      "local_clause_id": "R971-C3",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 2 — separation"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "known",
    "value": [
      "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Triarii",
      "enemy combat units except Elephants",
      "Roman/Ala infantry lines",
      "allied infantry"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.71"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Until and unless either trigger occurs."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E971"
  ],
  "gap_ids": [
    "G-D971LOS"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D971LOS, `/gaps/53`, bajty [640282,640747), SHA-256 `30bef8bfaae34c6d93008a0e4a476c3a60dd69b4aaaad592022e14b733622c12`.

```json
{
  "id": "G-D971LOS",
  "class": "missing_context",
  "affected_ids": [
    "R971",
    "D971LOS"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "LOS test necessary for enemy proximity release is referenced but unavailable.",
  "needed_context": "Line of Sight rules",
  "blocking": true,
  "evidence_ids": [
    "E971"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Line, LOS, odległości i identyfikacja wojsk wymagają jawnych danych.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-052

Zakres oceny: move+ShockRP>=floor(AWL/2)doesnotbypass9.71;standingShockagainsttargetinownZOCper9.72withouthavingtomove

Porównanie oceniającego: R972 zachowuje RP >= floor(AWL/2), jednostkę Rout Points i wyjątek Shock bez ruchu przeciw enemy w własnej ZOC. R971 osobno zawiera drugą bramkę. R972.conditions/action_effect nie podaje jednak jawnie, że próg RP nie omija 9.71; brak osobnej pary DEP-NEW-001 odziedziczony. Właściciel rozstrzyga, czy dwa osobne ograniczenia wystarczają do całego reviewed_scope EXP-052, czy reprezentacja ich koniunkcji jest niepełna. Nie dopisano bramki do odpowiedzi, nie nadano FN ani ogólnego pozwolenia na atak.

Propozycja: `local_components_supported_combination_pending`. Obie decyzje właściciela pending.

Źródło C-9.72-01, PDF 35 right, bbox [315.0, 553.113, 567.008, 611.113], render SHA-256 `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

**first-001 — osobna propozycja i ślady**

first-001 R972, `/rules/32`, bajty [335855,339867), SHA-256 `f304ccb85a653664ddb287c3e591dd67a2744b35cf4210ace71592b684436f5b`.

```json
{
  "id": "R972",
  "original_label": {
    "state": "known",
    "value": "9.72",
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R972-C1",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E972"
      ],
      "original_label_text": "9.72",
      "source_clause_locator": [
        "Triarii cannot move and Shock attack until Rout Point threshold reached.",
        "Always may stationary Shock enemy in their ZOC."
      ]
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "They may always, however, Shock attack (without moving) against enemy units in their ZOC."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Stationary Shock against enemy in own ZOC always permitted."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Triarii",
      "Roman army",
      "enemy units"
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.72"
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Until Rout Point threshold; stationary Shock always allowed."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E972"
  ],
  "gap_ids": [
    "G-D972AWL",
    "G-D972RP",
    "G-D-ZOC-R972"
  ],
  "review_status": "unreviewed"
}
```

first-001 R971, `/rules/31`, bajty [330949,335849), SHA-256 `8045dea61d7a9ffced7822b0dc2fc0c47620776dc6d0afa4bf6ede4ca2211ea0`.

```json
{
  "id": "R971",
  "original_label": {
    "state": "known",
    "value": "9.71",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R971-C1",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "Movement prohibition/facing permission"
    },
    {
      "local_clause_id": "R971-C2",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 1 — proximity and LOS"
    },
    {
      "local_clause_id": "R971-C3",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 2 — separation"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "known",
    "value": [
      "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Triarii",
      "enemy combat units except Elephants",
      "Roman/Ala infantry lines",
      "allied infantry"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.71"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Until and unless either trigger occurs."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E971"
  ],
  "gap_ids": [
    "G-D971LOS"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D972AWL, `/gaps/54`, bajty [555028,555502), SHA-256 `7b2a49345eb5abfd06e09555c1a797ca2d0960cac20429a52f04434614135c9c`.

```json
{
  "id": "G-D972AWL",
  "class": "missing_context",
  "affected_ids": [
    "R972",
    "D972AWL"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "Scenario value for Triarii half-withdrawal threshold is referenced but unavailable.",
  "needed_context": "Selected scenario Army Withdrawal Level",
  "blocking": true,
  "evidence_ids": [
    "E972"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D972RP, `/gaps/55`, bajty [555508,555991), SHA-256 `ecd85583d0a2f8ae358a010ae1bdbd73965717a64fd61fa126755e49e065078c`.

```json
{
  "id": "G-D972RP",
  "class": "missing_context",
  "affected_ids": [
    "R972",
    "D972RP"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "Roman Rout Point accounting needed for Triarii release is referenced but unavailable.",
  "needed_context": "Rout Point calculation and army withdrawal rules",
  "blocking": true,
  "evidence_ids": [
    "E972"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D-ZOC-R972, `/gaps/79`, bajty [567098,567558), SHA-256 `a4d67be1b5ec9d51a406e372f6202fce147a18184e5a5f18a6425518640595a8`.

```json
{
  "id": "G-D-ZOC-R972",
  "class": "missing_context",
  "affected_ids": [
    "R972",
    "D-ZOC-R972"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "General ZOC test in rule condition is referenced but unavailable.",
  "needed_context": "General ZOC definition and exceptions",
  "blocking": true,
  "evidence_ids": [
    "E972"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R972, `/rules/32`, bajty [408295,412460), SHA-256 `efc3e461afcdf47ef5fafdc90f3c9223badabf8597ff20dc3ef7807de8842bde`.

```json
{
  "id": "R972",
  "original_label": {
    "state": "known",
    "value": "9.72",
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R972-C1",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E972"
      ],
      "original_label_text": "9.72",
      "source_clause_locator": [
        "Triarii cannot move and Shock attack until Rout Point threshold reached.",
        "Always may stationary Shock enemy in their ZOC."
      ]
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "They may always, however, Shock attack (without moving) against enemy units in their ZOC."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "For combined movement and Shock: Roman Rout Points >= floor(one-half Army Withdrawal Level)."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Stationary Shock against enemy in own ZOC always permitted."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Triarii",
      "Roman army",
      "enemy units"
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.72"
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Until Rout Point threshold; stationary Shock always allowed."
    ],
    "evidence_ids": [
      "E972"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E972"
  ],
  "gap_ids": [
    "G-D972AWL",
    "G-D972RP",
    "G-D-ZOC-R972"
  ],
  "review_status": "unreviewed"
}
```

context-01 R971, `/rules/31`, bajty [403209,408288), SHA-256 `6e94e151066b13d8cb84cbab7fe71d386ca967fe2925ed13f138ab1e272e4a25`.

```json
{
  "id": "R971",
  "original_label": {
    "state": "known",
    "value": "9.71",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R971-C1",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "Movement prohibition/facing permission"
    },
    {
      "local_clause_id": "R971-C2",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 1 — proximity and LOS"
    },
    {
      "local_clause_id": "R971-C3",
      "region_id": "pdf-35-core-right",
      "evidence_ids": [
        "E971"
      ],
      "original_label_text": "9.71",
      "source_clause_locator": "OR trigger 2 — separation"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Triarii units cannot move, but may change facing, until and unless one of the following occurs:"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "known",
    "value": [
      "Enemy combat unit other than Elephant within 3 hexes AND LOS of any unit in Triarii line; OR Triarii at least 6 hexes from all other Roman/Ala infantry lines, excluding allied infantry (Hastati, Principes or others)."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Triarii cannot move, but can change facing, until either stated trigger occurs.",
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Triarii",
      "enemy combat units except Elephants",
      "Roman/Ala infantry lines",
      "allied infantry"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.71"
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Until and unless either trigger occurs."
    ],
    "evidence_ids": [
      "E971"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E971"
  ],
  "gap_ids": [
    "G-D971LOS"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D972AWL, `/gaps/54`, bajty [640754,641245), SHA-256 `4501dab342ed343a618bfbff3bc2c2a58e0037d4bb0ec51b1ce768d66008b659`.

```json
{
  "id": "G-D972AWL",
  "class": "missing_context",
  "affected_ids": [
    "R972",
    "D972AWL"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "Scenario value for Triarii half-withdrawal threshold is referenced but unavailable.",
  "needed_context": "Selected scenario Army Withdrawal Level",
  "blocking": true,
  "evidence_ids": [
    "E972"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D972RP, `/gaps/55`, bajty [641252,641752), SHA-256 `f55d0cda36ede2f89e9a06f65931deb0783be55f592e897fdf842846f390abca`.

```json
{
  "id": "G-D972RP",
  "class": "missing_context",
  "affected_ids": [
    "R972",
    "D972RP"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "Roman Rout Point accounting needed for Triarii release is referenced but unavailable.",
  "needed_context": "Rout Point calculation and army withdrawal rules",
  "blocking": true,
  "evidence_ids": [
    "E972"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D-ZOC-R972, `/gaps/79`, bajty [653278,653755), SHA-256 `f4316df191200527106f5fdd44db596d27ef4f4760e20d7f5d07f53eae494b36`.

```json
{
  "id": "G-D-ZOC-R972",
  "class": "missing_context",
  "affected_ids": [
    "R972",
    "D-ZOC-R972"
  ],
  "source_regions": [
    "pdf-35-core-right"
  ],
  "reason": "General ZOC test in rule condition is referenced but unavailable.",
  "needed_context": "General ZOC definition and exceptions",
  "blocking": true,
  "evidence_ids": [
    "E972"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: 9.71 i9.72 czytane razem; full legal attack nadal wymaga innych warunków.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-053

Zakres oceny: ScorpioBoltB,builtincrew,TQ,LIonlymovement/defense;noShockattack,offensiveMissileFireonly

Porównanie oceniającego: R981 zachowuje Bolt B, built-in crews i obecność TQ; LI tylko dla movement oraz obrony w Shock/Missile. Zakaz Shock-capable i jedyna zdolność ofensywna Missile Fire nie są rozszerzone na brak możliwości obrony. Konkretna wartość TQ i pełny lookup Bolt MRRC wyłączone.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.81-01, PDF 36 left, bbox [45.0, 69.197, 297.101, 139.197], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.81 Scorpios are Bolt-firing (B) engines with built-
> in crews. The Scorpios have a TQ rating, and they
> are treated as Light Infantry (LI) for movement and
> when defending in Shock Combat or against Missile
> Fire. Scorpio units are not Shock-capable and their only offensive
> combat capability is to Missile Fire.

**first-001 — osobna propozycja i ślady**

first-001 R981, `/rules/33`, bajty [339873,343919), SHA-256 `4e4891fc2c755ae9c07ed249141e368ed4377a415f874d747416eecb628eed39`.

```json
{
  "id": "R981",
  "original_label": {
    "state": "known",
    "value": "9.81",
    "evidence_ids": [
      "E981"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R981-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E981"
      ],
      "original_label_text": "9.81",
      "source_clause_locator": "Engine/crew/TQ classification"
    },
    {
      "local_clause_id": "R981-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E981"
      ],
      "original_label_text": "9.81",
      "source_clause_locator": "LI movement and defense"
    },
    {
      "local_clause_id": "R981-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E981"
      ],
      "original_label_text": "9.81",
      "source_clause_locator": "Offensive restriction"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpio units are not Shock-capable and their only offensive combat capability is to Missile Fire."
    ],
    "evidence_ids": [
      "E981"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E981"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E981"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E981"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio",
      "Light Infantry (LI)",
      "Bolt-firing (B)"
    ],
    "evidence_ids": [
      "E981"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.81"
    ],
    "evidence_ids": [
      "E981"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E981"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R981, `/rules/33`, bajty [412467,416654), SHA-256 `76cecff485b506b160191a8885cea72dd7016bed6da4f3798c6d7d01dbc6b826`.

```json
{
  "id": "R981",
  "original_label": {
    "state": "known",
    "value": "9.81",
    "evidence_ids": [
      "E981"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R981-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E981"
      ],
      "original_label_text": "9.81",
      "source_clause_locator": "Engine/crew/TQ classification"
    },
    {
      "local_clause_id": "R981-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E981"
      ],
      "original_label_text": "9.81",
      "source_clause_locator": "LI movement and defense"
    },
    {
      "local_clause_id": "R981-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E981"
      ],
      "original_label_text": "9.81",
      "source_clause_locator": "Offensive restriction"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpio units are not Shock-capable and their only offensive combat capability is to Missile Fire."
    ],
    "evidence_ids": [
      "E981"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E981"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E981"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E981"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio",
      "Light Infantry (LI)",
      "Bolt-firing (B)"
    ],
    "evidence_ids": [
      "E981"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.81"
    ],
    "evidence_ids": [
      "E981"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E981"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Pełne LI defense/movement i bolt MRRC wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-054

Zakres oceny: modechangeIOanyfriendlyleader;Firecannotmove,Movecannotfire;switchtoMoveblocksMoveinthesamephase,switchtoFireblocksFireinthesamephase;moveIOrequired,firedoesnotrequireorder;awersFire,rewersMove

Porównanie oceniającego: R982: zmiana trybu przez IO od dowolnego friendly leader; Move nie strzela, Fire nie rusza. Switch to Move blokuje ruch w tej Orders Phase, switch to Fire blokuje fire w tej fazie. Ruch w Move wymaga IO, fire nie wymaga order. R982note zachowuje awers Fire/rewers Move. Brak nowej akcji po switch i brak certyfikacji ratingów żetonu.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.82-01, PDF 36 left, bbox [45.0, 146.597, 297.55, 252.597], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.82 A Scorpio is in either Fire or Move mode. It requires an
> Individual Order from any friendly leader to change its mode.
> Scorpios in Move mode cannot fire, and conversely, cannot
> move in Fire mode. A Scorpio that has had its mode changed to
> Move cannot move in that Orders Phase, nor can a Scorpio that
> has had its mode switched to Fire, fire in that Orders Phase. A
> Scorpio unit in Move mode requires an Individual Order from
> any friendly leader to move. Scorpio units do not need orders to
> fire (see 9.85 below).

Źródło N-11, PDF 36 left, bbox [49.0, 261.1, 292.996, 283.1], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> PLAY NOTE: The front side of the counter shows the unit in
> Fire mode; the reverse side in Move mode.

**first-001 — osobna propozycja i ślady**

first-001 R982, `/rules/34`, bajty [343925,349222), SHA-256 `db2932e05afee950e1d27137b71fe09be42fd41a52f8e80905dc27726cf31a48`.

```json
{
  "id": "R982",
  "original_label": {
    "state": "known",
    "value": "9.82",
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R982-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Two modes/order to switch"
    },
    {
      "local_clause_id": "R982-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Mode-specific prohibitions"
    },
    {
      "local_clause_id": "R982-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Same-phase transition restrictions"
    },
    {
      "local_clause_id": "R982-C4",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Move order/fire exemption"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpio units do not need orders to fire (see 9.85 below)."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "No order needed to fire."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio",
      "any friendly leader"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.82"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Switching blocks corresponding action for that Orders Phase."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E982"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R982note, `/rules/35`, bajty [349228,352453), SHA-256 `88bf7f560fd28fa8d2955805d683d0f7eac1210dac638fc5f483232a758bd6c6`.

```json
{
  "id": "R982note",
  "original_label": {
    "state": "known",
    "value": "PLAY NOTE:",
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R982note-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982note"
      ],
      "original_label_text": "PLAY NOTE:",
      "source_clause_locator": "Counter front denotes Fire mode; reverse denotes Move mode."
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "The front side of the counter shows the unit in Fire mode; the reverse side in Move mode."
    ],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
    "evidence_ids": [
      "E982note"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Physical mode representation."
    ],
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E982note"
  ],
  "gap_ids": [],
  "review_status": "unreviewed",
  "source_locator": "PLAY NOTE (9.82)"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R982, `/rules/34`, bajty [416661,422148), SHA-256 `c322a28fb1c69bff5deac677b5a8ee02c5c27f63d0f17bce8a72a482a530f988`.

```json
{
  "id": "R982",
  "original_label": {
    "state": "known",
    "value": "9.82",
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R982-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Two modes/order to switch"
    },
    {
      "local_clause_id": "R982-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Mode-specific prohibitions"
    },
    {
      "local_clause_id": "R982-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Same-phase transition restrictions"
    },
    {
      "local_clause_id": "R982-C4",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Move order/fire exemption"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpio units do not need orders to fire (see 9.85 below)."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "No order needed to fire."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio",
      "any friendly leader"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.82"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Switching blocks corresponding action for that Orders Phase."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E982"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R982note, `/rules/35`, bajty [422155,425494), SHA-256 `9ac67925c35fae2788830f9c0809376ae5aace09ee195639c5f67b7240858bd0`.

```json
{
  "id": "R982note",
  "original_label": {
    "state": "known",
    "value": "PLAY NOTE:",
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R982note-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982note"
      ],
      "original_label_text": "PLAY NOTE:",
      "source_clause_locator": "Counter front denotes Fire mode; reverse denotes Move mode."
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "The front side of the counter shows the unit in Fire mode; the reverse side in Move mode."
    ],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
    "evidence_ids": [
      "E982note"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Counter front denotes Fire mode; reverse denotes Move mode.",
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982note"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Physical mode representation."
    ],
    "evidence_ids": [
      "E982note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E982note"
  ],
  "gap_ids": [],
  "review_status": "unreviewed",
  "source_locator": "PLAY NOTE (9.82)"
}
```

Niepewności i wyłączenia: 9.85 uzupełnia harmonogram ognia; źródło nie ustanawia dodatkowej akcji po switch.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-055

Zakres oceny: atmostoneScorpioperhex,otherstackingrulesretained

Porównanie oceniającego: R983 zachowuje maksimum jeden Scorpio na heks i all other stacking rules. Nie przyznaje automatycznej legalności współzajęcia. G-D983stack blocking=true dotyczy pełnych ograniczeń, nie znanego lokalnego maksimum.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.83-01, PDF 36 left, bbox [45.0, 292.34, 297.017, 314.34], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.83 Only one Scorpio unit may occupy any one hex. All other
> stacking rules apply.

**first-001 — osobna propozycja i ślady**

first-001 R983, `/rules/36`, bajty [352459,356106), SHA-256 `f7d2aafc87c8ed78040ffececeea0285fff874b6b06483f0065d8564c626e87f`.

```json
{
  "id": "R983",
  "original_label": {
    "state": "known",
    "value": "9.83",
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R983-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E983"
      ],
      "original_label_text": "9.83",
      "source_clause_locator": "Maximum one Scorpio in any hex; all other stacking rules still apply."
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Only one Scorpio unit may occupy any one hex. All other stacking rules apply."
    ],
    "evidence_ids": [
      "E983"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
    "evidence_ids": [
      "E983"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E983"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E983"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "One-Scorpio restriction does not itself establish all other stacking permissions."
    ],
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E983"
  ],
  "gap_ids": [
    "G-D983stack"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D983stack, `/gaps/56`, bajty [555997,556446), SHA-256 `2601f6668acf6d9ad7da7796f0daec6d1ddeca0042706531540d45ba973b2edd`.

```json
{
  "id": "G-D983stack",
  "class": "missing_context",
  "affected_ids": [
    "R983",
    "D983stack"
  ],
  "source_regions": [
    "pdf-36-core-left"
  ],
  "reason": "Other Scorpio stacking constraints is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E983"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R983, `/rules/36`, bajty [425501,429280), SHA-256 `7a009418ad0af36b8ee5ca3de17a068395e17db2e7da4760ace20689e5366e00`.

```json
{
  "id": "R983",
  "original_label": {
    "state": "known",
    "value": "9.83",
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R983-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E983"
      ],
      "original_label_text": "9.83",
      "source_clause_locator": "Maximum one Scorpio in any hex; all other stacking rules still apply."
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Only one Scorpio unit may occupy any one hex. All other stacking rules apply."
    ],
    "evidence_ids": [
      "E983"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
    "evidence_ids": [
      "E983"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E983"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Maximum one Scorpio in any hex; all other stacking rules still apply.",
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E983"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "One-Scorpio restriction does not itself establish all other stacking permissions."
    ],
    "evidence_ids": [
      "E983"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E983"
  ],
  "gap_ids": [
    "G-D983stack"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D983stack, `/gaps/56`, bajty [641759,642225), SHA-256 `ce88ae13d5292724dbb7bb023a8021b917b69a71f72ac40d3693dab72de74ace`.

```json
{
  "id": "G-D983stack",
  "class": "missing_context",
  "affected_ids": [
    "R983",
    "D983stack"
  ],
  "source_regions": [
    "pdf-36-core-left"
  ],
  "reason": "Other Scorpio stacking constraints is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E983"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Pełna legalność współzajęcia wymaga general stacking.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-056

Zakres oceny: nofacing;allhexesFront;range/LOS/terrainnotwaived

Porównanie oceniającego: R984: brak facing, ruch/fire w dowolnym kierunku niezależnie od orientacji counter, wszystkie heksy Front. Nie ma zniesienia mode, range/LOS lub terrain; nie oceniono zewnętrznych ograniczeń ani konkretnego strzału.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.84-01, PDF 36 left, bbox [45.0, 321.74, 297.063, 355.74], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.84 Scorpio units have no facing; they may move or fire in any
> direction, regardless of the direction the actual counter is pointed.
> All hexes are considered Front hexes.

**first-001 — osobna propozycja i ślady**

first-001 R984, `/rules/37`, bajty [356112,359528), SHA-256 `de911fdc0696db757fc4653804f89e65ed4a57ec809e9dd48209d12f438a56a5`.

```json
{
  "id": "R984",
  "original_label": {
    "state": "known",
    "value": "9.84",
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R984-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E984"
      ],
      "original_label_text": "9.84",
      "source_clause_locator": "No facing/directional freedom"
    },
    {
      "local_clause_id": "R984-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E984"
      ],
      "original_label_text": "9.84",
      "source_clause_locator": "All Front classification"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "All hexes are considered Front hexes."
    ],
    "evidence_ids": [
      "E984"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
    "evidence_ids": [
      "E984"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E984"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E984"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E984"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.84"
    ],
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E984"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R984, `/rules/37`, bajty [429287,432825), SHA-256 `1c7feae738ab6c980bff3d77751acadc52dc149fb5e6ab07b6dbfcb090e4ec60`.

```json
{
  "id": "R984",
  "original_label": {
    "state": "known",
    "value": "9.84",
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R984-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E984"
      ],
      "original_label_text": "9.84",
      "source_clause_locator": "No facing/directional freedom"
    },
    {
      "local_clause_id": "R984-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E984"
      ],
      "original_label_text": "9.84",
      "source_clause_locator": "All Front classification"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "All hexes are considered Front hexes."
    ],
    "evidence_ids": [
      "E984"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
    "evidence_ids": [
      "E984"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E984"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Scorpios have no facing, move/fire in any direction regardless of counter orientation, and treat all hexes as Front hexes.",
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E984"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E984"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.84"
    ],
    "evidence_ids": [
      "E984"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E984"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Nie znosi range/LOS/terrain.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-057

Zakres oceny: ActiveFiremax2/GameTurnandmax1/friendlyOrdersPhaseinMovementMissilesegment;Once/Finished;afteractiveFire nootheractionthatphaseincludingRecovery

Porównanie oceniającego: R985 zachowuje max 2 active shots/Game Turn, max 1/friendly Orders Phase w Movement and Missile Fire Segment, bez order. Pierwszy Once, drugi Finished w R985 i N985markers; grafika pokazuje oba. Po fire brak innych działań tej Orders Phase, w tym Recovery. Nie myli Game Turn z Orders Phase i nie przyznaje fire w Move.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.85-01, PDF 36 left, bbox [44.997, 363.14, 297.024, 481.14], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

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

Źródło G-04, PDF 36 left, bbox [45, 365, 120, 404], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

**first-001 — osobna propozycja i ślady**

first-001 N985markers, `/nodes/34`, bajty [150642,151434), SHA-256 `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.

```json
{
  "id": "N985markers",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Active Fire markers",
    "evidence_ids": [
      "E985markers"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E985markers"
  ],
  "review_status": "unreviewed"
}
```

first-001 R985, `/rules/38`, bajty [359534,364613), SHA-256 `9083d4f2690f24d2424f617dbf3a0b4481149a19932798070e26fcfe4b74207e`.

```json
{
  "id": "R985",
  "original_label": {
    "state": "known",
    "value": "9.85",
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R985-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Firing permission and limits"
    },
    {
      "local_clause_id": "R985-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "First/second marker sequence"
    },
    {
      "local_clause_id": "R985-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Other-action prohibition"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "no more than one shot per Orders Phase."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "Friendly Orders Phase, active player Movement and Missile Fire Segment, Scorpio in Fire mode."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E985"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.85"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E985"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 N985markers, `/nodes/34`, bajty [199790,200614), SHA-256 `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.

```json
{
  "id": "N985markers",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Active Fire markers",
    "evidence_ids": [
      "E985markers"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E985markers"
  ],
  "review_status": "unreviewed"
}
```

context-01 R985, `/rules/38`, bajty [432832,438091), SHA-256 `15e7d8e13c9489316c465caf3fb6ec40f605189e3145e013051d7ec031e0dea3`.

```json
{
  "id": "R985",
  "original_label": {
    "state": "known",
    "value": "9.85",
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R985-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Firing permission and limits"
    },
    {
      "local_clause_id": "R985-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "First/second marker sequence"
    },
    {
      "local_clause_id": "R985-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Other-action prohibition"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "no more than one shot per Orders Phase."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "Friendly Orders Phase, active player Movement and Missile Fire Segment, Scorpio in Fire mode."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E985"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.85"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E985"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Warunki range/LOS/MRRC i mode9.82 nadal obowiązują.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-058

Zakres oceny: specialReactionFiremax2/enemyOrdersPhasein enemyMovementMissilesegment,includingduringenemyunitmovement;ordinary8.2ReactionFireforbidden;sourceanymovementdoesnotgrantScorpiofireinMovemode

Porównanie oceniającego: R986 zachowuje specjalne 2 shots/enemy Orders Phase podczas enemy Movement and Missile Segment, także w trakcie ruchu enemy, i zakaz ordinary Reaction Fire 8.2. Conditions jawnie Fire mode under9.82. Once/Finished opisane w prozie; N986marker uczciwie odróżnia pokazane Once od Finished z tekstu. Lokalna propozycja nie uchyla zakazu Reaction Fire any kind podczas Rampage w R914; brak pary DEP-NEW-003 pozostaje SEM-006, bez naprawy/TP/FN.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.86-01, PDF 36 left, bbox [45.0, 489.54, 297.053, 583.54], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.86 Reaction Fire: Scorpios may fire twice per enemy Orders
> Phase at any time during the enemy Movement and Missile Seg-
> ment—and we mean “any”; they may fire even during enemy
> movement! The first time the Scorpio unit fires, place
> a REACTION FIRE ONCE marker on it. The second
> time it fires, flip the marker to its REACTION FIRE
> FINISHED side. Scorpios, however, cannot use any
> type of ordinary Reaction Fire (8.2).

Źródło G-05, PDF 36 left, bbox [260, 528, 297, 566], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

**first-001 — osobna propozycja i ślady**

first-001 N986marker, `/nodes/35`, bajty [151440,152165), SHA-256 `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.

```json
{
  "id": "N986marker",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Reaction Fire marker",
    "evidence_ids": [
      "E986marker"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E986marker"
  ],
  "review_status": "unreviewed"
}
```

first-001 R986, `/rules/39`, bajty [364619,369123), SHA-256 `64c29b4c0d2490544011c5ceb97b13ba7cd008eb4729f5055d1ca9665796cca7`.

```json
{
  "id": "R986",
  "original_label": {
    "state": "known",
    "value": "9.86",
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R986-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E986"
      ],
      "original_label_text": "9.86",
      "source_clause_locator": "Special reaction timing/count"
    },
    {
      "local_clause_id": "R986-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E986"
      ],
      "original_label_text": "9.86",
      "source_clause_locator": "Marker sequence"
    },
    {
      "local_clause_id": "R986-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E986"
      ],
      "original_label_text": "9.86",
      "source_clause_locator": "Ordinary Reaction Fire prohibition"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpios, however, cannot use any type of ordinary Reaction Fire (8.2)."
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "Enemy Orders Phase Movement and Missile Segment; Scorpio in Fire mode under 9.82."
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E986"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.86"
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Any time in enemy Movement and Missile Segment, including enemy movement."
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E986"
  ],
  "gap_ids": [
    "G-D986react"
  ],
  "review_status": "unreviewed"
}
```

first-001 R982, `/rules/34`, bajty [343925,349222), SHA-256 `db2932e05afee950e1d27137b71fe09be42fd41a52f8e80905dc27726cf31a48`.

```json
{
  "id": "R982",
  "original_label": {
    "state": "known",
    "value": "9.82",
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R982-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Two modes/order to switch"
    },
    {
      "local_clause_id": "R982-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Mode-specific prohibitions"
    },
    {
      "local_clause_id": "R982-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Same-phase transition restrictions"
    },
    {
      "local_clause_id": "R982-C4",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Move order/fire exemption"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpio units do not need orders to fire (see 9.85 below)."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "No order needed to fire."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio",
      "any friendly leader"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.82"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Switching blocks corresponding action for that Orders Phase."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E982"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R914, `/rules/4`, bajty [191201,210006), SHA-256 `338c61649787bee795a30009efa232ca58c6e0edc28d5a1a2f699b86ab371a35`.

```json
{
  "id": "R914",
  "original_label": {
    "state": "known",
    "value": "9.14",
    "evidence_ids": [
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
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R914-C1",
      "region_id": "pdf-32-core-left",
      "evidence_ids": [
        "E914start"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Rout trigger"
    },
    {
      "local_clause_id": "R914-C2",
      "region_id": "pdf-32-core-left",
      "evidence_ids": [
        "E914tableL"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Table 0 and 1–6"
    },
    {
      "local_clause_id": "R914-C3",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914tableR"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Table 7–9 continuation"
    },
    {
      "local_clause_id": "R914-C4",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914priority"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Immediate priority"
    },
    {
      "local_clause_id": "R914-C5",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914diagram"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Diagram/caption"
    },
    {
      "local_clause_id": "R914-C6",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914move"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Movement/contact/stack/leader impact"
    },
    {
      "local_clause_id": "R914-C7",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914end"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Termination and accompanying leader"
    },
    {
      "local_clause_id": "R914-C8",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914last"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "No ZOC/Reaction/rally"
    },
    {
      "local_clause_id": "R914-C9",
      "region_id": "pdf-33-core-left",
      "evidence_ids": [
        "E914cont"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Serial completion continuation"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Elephant",
      "Leader Elephant",
      "cavalry",
      "friendly/enemy units",
      "stacked leader"
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
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.14"
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
  },
  "time_limits": {
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
  ],
  "gap_ids": [
    "G-D914OW",
    "G-D914leaderwithdraw",
    "G-D914casualty"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D986react, `/gaps/57`, bajty [556452,556928), SHA-256 `5c69aa8c8b0faba50fa29d8c9273e2b22b62a835695ea49e08a452e3058eb9c8`.

```json
{
  "id": "G-D986react",
  "class": "missing_context",
  "affected_ids": [
    "R986",
    "D986react"
  ],
  "source_regions": [
    "pdf-36-core-left"
  ],
  "reason": "Ordinary Reaction Fire prohibited for Scorpio is referenced but unavailable.",
  "needed_context": "8.2 to distinguish prohibited ordinary modes",
  "blocking": false,
  "evidence_ids": [
    "E986"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 N986marker, `/nodes/35`, bajty [200621,201375), SHA-256 `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.

```json
{
  "id": "N986marker",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Reaction Fire marker",
    "evidence_ids": [
      "E986marker"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E986marker"
  ],
  "review_status": "unreviewed"
}
```

context-01 R986, `/rules/39`, bajty [438098,442766), SHA-256 `4cf0366781c3358abc98fff09da31c4c44d05d4c9dae4f10f7cd6443e2c714da`.

```json
{
  "id": "R986",
  "original_label": {
    "state": "known",
    "value": "9.86",
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R986-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E986"
      ],
      "original_label_text": "9.86",
      "source_clause_locator": "Special reaction timing/count"
    },
    {
      "local_clause_id": "R986-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E986"
      ],
      "original_label_text": "9.86",
      "source_clause_locator": "Marker sequence"
    },
    {
      "local_clause_id": "R986-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E986"
      ],
      "original_label_text": "9.86",
      "source_clause_locator": "Ordinary Reaction Fire prohibition"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpios, however, cannot use any type of ordinary Reaction Fire (8.2)."
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "Enemy Orders Phase Movement and Missile Segment; Scorpio in Fire mode under 9.82."
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E986"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.86"
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Any time in enemy Movement and Missile Segment, including enemy movement."
    ],
    "evidence_ids": [
      "E986"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E986"
  ],
  "gap_ids": [
    "G-D986react"
  ],
  "review_status": "unreviewed"
}
```

context-01 R982, `/rules/34`, bajty [416661,422148), SHA-256 `c322a28fb1c69bff5deac677b5a8ee02c5c27f63d0f17bce8a72a482a530f988`.

```json
{
  "id": "R982",
  "original_label": {
    "state": "known",
    "value": "9.82",
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R982-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Two modes/order to switch"
    },
    {
      "local_clause_id": "R982-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Mode-specific prohibitions"
    },
    {
      "local_clause_id": "R982-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Same-phase transition restrictions"
    },
    {
      "local_clause_id": "R982-C4",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E982"
      ],
      "original_label_text": "9.82",
      "source_clause_locator": "Move order/fire exemption"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Scorpio units do not need orders to fire (see 9.85 below)."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E982"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "No order needed to fire."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio",
      "any friendly leader"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.82"
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Switching blocks corresponding action for that Orders Phase."
    ],
    "evidence_ids": [
      "E982"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E982"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R914, `/rules/4`, bajty [257723,277141), SHA-256 `450ebcd334fed58a89e2ebca5cd90f6405817af599e651277f5da0d7eff3fc88`.

```json
{
  "id": "R914",
  "original_label": {
    "state": "known",
    "value": "9.14",
    "evidence_ids": [
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
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R914-C1",
      "region_id": "pdf-32-core-left",
      "evidence_ids": [
        "E914start"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Rout trigger"
    },
    {
      "local_clause_id": "R914-C2",
      "region_id": "pdf-32-core-left",
      "evidence_ids": [
        "E914tableL"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Table 0 and 1–6"
    },
    {
      "local_clause_id": "R914-C3",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914tableR"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Table 7–9 continuation"
    },
    {
      "local_clause_id": "R914-C4",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914priority"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Immediate priority"
    },
    {
      "local_clause_id": "R914-C5",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914diagram"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Diagram/caption"
    },
    {
      "local_clause_id": "R914-C6",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914move"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Movement/contact/stack/leader impact"
    },
    {
      "local_clause_id": "R914-C7",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914end"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Termination and accompanying leader"
    },
    {
      "local_clause_id": "R914-C8",
      "region_id": "pdf-32-core-right",
      "evidence_ids": [
        "E914last"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "No ZOC/Reaction/rally"
    },
    {
      "local_clause_id": "R914-C9",
      "region_id": "pdf-33-core-left",
      "evidence_ids": [
        "E914cont"
      ],
      "original_label_text": "9.14",
      "source_clause_locator": "Serial completion continuation"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Elephant",
      "Leader Elephant",
      "cavalry",
      "friendly/enemy units",
      "stacked leader"
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
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.14"
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
  },
  "time_limits": {
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
  ],
  "gap_ids": [
    "G-D914OW",
    "G-D914leaderwithdraw",
    "G-D914casualty"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D986react, `/gaps/57`, bajty [642232,642725), SHA-256 `45e1f6dd8be4e7d1cef1f01dad4a06508b05e1d1f6481cbfc5c1c91423b06949`.

```json
{
  "id": "G-D986react",
  "class": "missing_context",
  "affected_ids": [
    "R986",
    "D986react"
  ],
  "source_regions": [
    "pdf-36-core-left"
  ],
  "reason": "Ordinary Reaction Fire prohibited for Scorpio is referenced but unavailable.",
  "needed_context": "8.2 to distinguish prohibited ordinary modes",
  "blocking": false,
  "evidence_ids": [
    "E986"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: No Reaction Fire any kind w Rampage9.14 nadal wyłącza trigger; zewnętrzny ogień i segment wymagają kontekstu.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-059

Zakres oceny: incur/recoverHitsasgeneralunits;Routimmediateelimination

Porównanie oceniającego: R987 zachowuje incurring/recovering Cohesion Hits jak inne jednostki i natychmiastową eliminację przy Rout. Nie zgaduje triggeru Rout ani liczby odzyskiwanych Hits. R985 osobno zachowuje zakaz Recovery w fazie active fire; brak pełnej procedury recovery nie blokuje podanego lokalnego skutku Rout.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.87-01, PDF 36 left, bbox [45.0, 590.94, 297.043, 612.94], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.87 Scorpios incur and recover Cohesion Hits as any other unit.
> A Scorpio that routs is immediately eliminated.

**first-001 — osobna propozycja i ślady**

first-001 R987, `/rules/40`, bajty [369129,372461), SHA-256 `0bdf1d408d64bb25daf21ea3f60f30aeb4ff91ce89afa5fc8f59908eba99ca8a`.

```json
{
  "id": "R987",
  "original_label": {
    "state": "known",
    "value": "9.87",
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R987-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E987"
      ],
      "original_label_text": "9.87",
      "source_clause_locator": "Ordinary Hits/recovery"
    },
    {
      "local_clause_id": "R987-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E987"
      ],
      "original_label_text": "9.87",
      "source_clause_locator": "Rout replacement"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "A Scorpio that routs is immediately eliminated."
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
    "evidence_ids": [
      "E987"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E987"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E987"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E987"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.87"
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on rout."
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E987"
  ],
  "gap_ids": [
    "G-D987recovery"
  ],
  "review_status": "unreviewed"
}
```

first-001 R985, `/rules/38`, bajty [359534,364613), SHA-256 `9083d4f2690f24d2424f617dbf3a0b4481149a19932798070e26fcfe4b74207e`.

```json
{
  "id": "R985",
  "original_label": {
    "state": "known",
    "value": "9.85",
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R985-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Firing permission and limits"
    },
    {
      "local_clause_id": "R985-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "First/second marker sequence"
    },
    {
      "local_clause_id": "R985-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Other-action prohibition"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "no more than one shot per Orders Phase."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "Friendly Orders Phase, active player Movement and Missile Fire Segment, Scorpio in Fire mode."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E985"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.85"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E985"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 G-D987recovery, `/gaps/58`, bajty [556934,557400), SHA-256 `f05e5cf84dbdbec0e8bcd4f8e06ff594e8d2905045f6e8871d7f21675b6073bb`.

```json
{
  "id": "G-D987recovery",
  "class": "missing_context",
  "affected_ids": [
    "R987",
    "D987recovery"
  ],
  "source_regions": [
    "pdf-36-core-left"
  ],
  "reason": "Normal Scorpio Hits/recovery processing is referenced but unavailable.",
  "needed_context": "Cohesion Hit and Recovery procedure",
  "blocking": true,
  "evidence_ids": [
    "E987"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R987, `/rules/40`, bajty [442773,446233), SHA-256 `4319d42d58befea89683b3ce1da7b0ca03bb21ea982de7aaa504ab436290a229`.

```json
{
  "id": "R987",
  "original_label": {
    "state": "known",
    "value": "9.87",
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R987-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E987"
      ],
      "original_label_text": "9.87",
      "source_clause_locator": "Ordinary Hits/recovery"
    },
    {
      "local_clause_id": "R987-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E987"
      ],
      "original_label_text": "9.87",
      "source_clause_locator": "Rout replacement"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "A Scorpio that routs is immediately eliminated."
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
    "evidence_ids": [
      "E987"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E987"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Scorpio incurs and recovers Hits like other units; rout immediately eliminates it.",
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E987"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E987"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.87"
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on rout."
    ],
    "evidence_ids": [
      "E987"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E987"
  ],
  "gap_ids": [
    "G-D987recovery"
  ],
  "review_status": "unreviewed"
}
```

context-01 R985, `/rules/38`, bajty [432832,438091), SHA-256 `15e7d8e13c9489316c465caf3fb6ec40f605189e3145e013051d7ec031e0dea3`.

```json
{
  "id": "R985",
  "original_label": {
    "state": "known",
    "value": "9.85",
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R985-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Firing permission and limits"
    },
    {
      "local_clause_id": "R985-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "First/second marker sequence"
    },
    {
      "local_clause_id": "R985-C3",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E985"
      ],
      "original_label_text": "9.85",
      "source_clause_locator": "Other-action prohibition"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "no more than one shot per Orders Phase."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "Friendly Orders Phase, active player Movement and Missile Fire Segment, Scorpio in Fire mode."
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E985"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Scorpio"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.85"
    ],
    "evidence_ids": [
      "E985"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E985"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 G-D987recovery, `/gaps/58`, bajty [642732,643215), SHA-256 `bb0c068ff4e763a593c93bb17c8317e14f6459174ef40d45e192c2ce816db360`.

```json
{
  "id": "G-D987recovery",
  "class": "missing_context",
  "affected_ids": [
    "R987",
    "D987recovery"
  ],
  "source_regions": [
    "pdf-36-core-left"
  ],
  "reason": "Normal Scorpio Hits/recovery processing is referenced but unavailable.",
  "needed_context": "Cohesion Hit and Recovery procedure",
  "blocking": true,
  "evidence_ids": [
    "E987"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Trigger Rout i recovery amounts wymagają general rules.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-060

Zakres oceny: BI no terrainCohesionHits crossing/enteringpassableterrain or facingRough;MP/passabilitynotwaived;noColumn/PAW/OW

Porównanie oceniającego: R991 zachowuje 0 terrain Cohesion Hits tylko przy crossing/entering passable terrain oraz facing Rough. Kontynuacja w prawej kolumnie zakazuje Column6.7, PAW6.8 i OW6.5. Nie wyzerowano MP ani nie zezwolono na impassable terrain. Definicje zakazanych procedur nonblocking nie stanowią zgody na ich wykonanie.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.91-02, PDF 36 left, bbox [45.0, 698.844, 297.12, 732.844], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Barbarian Infantry (BI) units do not incur Cohesion Hits for
> crossing or entering any type of passable terrain, nor do they
> incur Cohesion Hits for changing facing in Rough terrain. BI units

Źródło C-9.91-02, PDF 36 right, bbox [315.0, 54.004, 567.0, 76.004], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> cannot use Column Movement (6.7), Pre-Arranged Withdrawal
> (6.8), or Orderly Withdrawal (6.5).

**first-001 — osobna propozycja i ślady**

first-001 R991, `/rules/41`, bajty [372467,377217), SHA-256 `54dcf8cd5202e6beebb7d87fcb4104ee5d6b6b3b8737e8ad794d6665eb6c387b`.

```json
{
  "id": "R991",
  "original_label": {
    "state": "known",
    "value": "9.91",
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R991-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E991a"
      ],
      "original_label_text": "9.91",
      "source_clause_locator": "Passable terrain exception"
    },
    {
      "local_clause_id": "R991-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E991a"
      ],
      "original_label_text": "9.91",
      "source_clause_locator": "Rough-facing exception"
    },
    {
      "local_clause_id": "R991-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E991b"
      ],
      "original_label_text": "9.91",
      "source_clause_locator": "Continuation — three prohibited procedures"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Barbarian Infantry (BI)"
    ],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.91"
    ],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "gap_ids": [
    "G-D991column",
    "G-D991PAW",
    "G-D991OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D991column, `/gaps/59`, bajty [557406,557849), SHA-256 `21c7908a31249062fd79298c49cfa5ffc171fb65ba371f1fb3e9d75d91c5ae93`.

```json
{
  "id": "G-D991column",
  "class": "missing_context",
  "affected_ids": [
    "R991",
    "D991column"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Column Movement prohibited for BI is referenced but unavailable.",
  "needed_context": "6.7 definition only",
  "blocking": false,
  "evidence_ids": [
    "E991b"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D991PAW, `/gaps/60`, bajty [557855,558300), SHA-256 `40455f6e8efd482cb56671bc8b25c967ddc33317159ffccbeff0a89d09900951`.

```json
{
  "id": "G-D991PAW",
  "class": "missing_context",
  "affected_ids": [
    "R991",
    "D991PAW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Pre-Arranged Withdrawal prohibited for BI is referenced but unavailable.",
  "needed_context": "6.8 definition only",
  "blocking": false,
  "evidence_ids": [
    "E991b"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D991OW, `/gaps/61`, bajty [558306,558728), SHA-256 `4faa4ac08561677b7abc26d31318f745f9632dd5ea870a19688ba0be5069a2fa`.

```json
{
  "id": "G-D991OW",
  "class": "missing_context",
  "affected_ids": [
    "R991",
    "D991OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "OW prohibited for BI is referenced but unavailable.",
  "needed_context": "6.5 definition only",
  "blocking": false,
  "evidence_ids": [
    "E991b"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R991, `/rules/41`, bajty [446240,451161), SHA-256 `5e41692ae51622c98f8ec0c02518e45efed39da42849c4d7693b20f9138a770c`.

```json
{
  "id": "R991",
  "original_label": {
    "state": "known",
    "value": "9.91",
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R991-C1",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E991a"
      ],
      "original_label_text": "9.91",
      "source_clause_locator": "Passable terrain exception"
    },
    {
      "local_clause_id": "R991-C2",
      "region_id": "pdf-36-core-left",
      "evidence_ids": [
        "E991a"
      ],
      "original_label_text": "9.91",
      "source_clause_locator": "Rough-facing exception"
    },
    {
      "local_clause_id": "R991-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E991b"
      ],
      "original_label_text": "9.91",
      "source_clause_locator": "Continuation — three prohibited procedures"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Barbarian Infantry (BI)"
    ],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.91"
    ],
    "evidence_ids": [
      "E991a",
      "E991b"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E991a",
    "E991b"
  ],
  "gap_ids": [
    "G-D991column",
    "G-D991PAW",
    "G-D991OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D991column, `/gaps/59`, bajty [643222,643682), SHA-256 `e00f043865aa4198721e59d3236abd096a7a37262bb6e862aa77311703e62b92`.

```json
{
  "id": "G-D991column",
  "class": "missing_context",
  "affected_ids": [
    "R991",
    "D991column"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Column Movement prohibited for BI is referenced but unavailable.",
  "needed_context": "6.7 definition only",
  "blocking": false,
  "evidence_ids": [
    "E991b"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D991PAW, `/gaps/60`, bajty [643689,644151), SHA-256 `d7f08e71c1cc07c87e8e1533bbf883c8e2f08e3eb81313bb09067428e67f4010`.

```json
{
  "id": "G-D991PAW",
  "class": "missing_context",
  "affected_ids": [
    "R991",
    "D991PAW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Pre-Arranged Withdrawal prohibited for BI is referenced but unavailable.",
  "needed_context": "6.8 definition only",
  "blocking": false,
  "evidence_ids": [
    "E991b"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D991OW, `/gaps/61`, bajty [644158,644597), SHA-256 `0d27fe434550bc8f13cd6a227585090b06c3852a1d7a95d6c6f1e7e147f9841a`.

```json
{
  "id": "G-D991OW",
  "class": "missing_context",
  "affected_ids": [
    "R991",
    "D991OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "OW prohibited for BI is referenced but unavailable.",
  "needed_context": "6.5 definition only",
  "blocking": false,
  "evidence_ids": [
    "E991b"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Passability/koszt MP wymagają Movement Cost Chart, zakazy nie wymagają wykonania zabronionych procedur.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-061

Zakres oceny: Recoveryorderonly1CH;depletedBIeliminatedinsteadofRout;do notautomaticallytreatthateliminationasRoutforFerocity;fulltriggerorderingnotresolved

Porównanie oceniającego: R993: tylko 1 Cohesion Hit/Recovery order; Depleted BI eliminated instead of Rout. Zestawione R994 ma trigger BI Routs, więc nie utożsamiono tego zastąpienia z jawnym Rout dla Ferocity. Pełne ordering i depletion/recovery eligibility pozostają poza zakresem; established_absent w exceptions nie jest ogólnym brakiem wyjątków.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.93-02, PDF 36 right, bbox [315.0, 99.004, 566.997, 109.004], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> BI units can only remove 1 Cohesion Hit per Recovery order.

Źródło C-9.93-03, PDF 36 right, bbox [315.0, 111.004, 543.32, 121.004], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Depleted BI units do not Rout but are instead eliminated.

**first-001 — osobna propozycja i ślady**

first-001 R993, `/rules/42`, bajty [377223,381102), SHA-256 `ac9f1b844e212d7c1ed2c0b307f8f974da613cd2137afc21a716bd6ff2f5d820`.

```json
{
  "id": "R993",
  "original_label": {
    "state": "known",
    "value": "9.93",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R993-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Recovery cap"
    },
    {
      "local_clause_id": "R993-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Depleted rout replacement"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "BI units can only remove 1 Cohesion Hit per Recovery order."
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Barbarian Infantry (BI)",
      "Depleted BI"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.93"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E993"
  ],
  "gap_ids": [
    "G-D993recovery",
    "G-D993depleted"
  ],
  "review_status": "unreviewed"
}
```

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D993recovery, `/gaps/62`, bajty [558734,559207), SHA-256 `e97246cb8c85acdf2b718f201480216826a1d7309f7055376dc6be6bff64c43e`.

```json
{
  "id": "G-D993recovery",
  "class": "missing_context",
  "affected_ids": [
    "R993",
    "D993recovery"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Normal Recovery modified to 1 Hit for BI is referenced but unavailable.",
  "needed_context": "Recovery order eligibility and procedure",
  "blocking": true,
  "evidence_ids": [
    "E993"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D993depleted, `/gaps/63`, bajty [559213,559690), SHA-256 `eed856d3e7aef25bab157896c5fe33fd9f5c71ae62f878fe5598bafe8cb973a3`.

```json
{
  "id": "G-D993depleted",
  "class": "missing_context",
  "affected_ids": [
    "R993",
    "D993depleted"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Depleted status necessary for rout replacement is referenced but unavailable.",
  "needed_context": "Depletion definition and determination",
  "blocking": true,
  "evidence_ids": [
    "E993"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R993, `/rules/42`, bajty [451168,455190), SHA-256 `fdf01acb9629e037cb6f43e05f89f53320c84ff76245e149f5dce967553aa1f3`.

```json
{
  "id": "R993",
  "original_label": {
    "state": "known",
    "value": "9.93",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R993-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Recovery cap"
    },
    {
      "local_clause_id": "R993-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Depleted rout replacement"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "BI units can only remove 1 Cohesion Hit per Recovery order."
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Barbarian Infantry (BI)",
      "Depleted BI"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.93"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E993"
  ],
  "gap_ids": [
    "G-D993recovery",
    "G-D993depleted"
  ],
  "review_status": "unreviewed"
}
```

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D993recovery, `/gaps/62`, bajty [644604,645094), SHA-256 `837c301fff02606dca51181a6dac5eb9de810deadc48840a33793f4a1dae2a9c`.

```json
{
  "id": "G-D993recovery",
  "class": "missing_context",
  "affected_ids": [
    "R993",
    "D993recovery"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Normal Recovery modified to 1 Hit for BI is referenced but unavailable.",
  "needed_context": "Recovery order eligibility and procedure",
  "blocking": true,
  "evidence_ids": [
    "E993"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D993depleted, `/gaps/63`, bajty [645101,645595), SHA-256 `f761def146a8386ceaeed18b8712253451c0275245b4e3e13d05ab12485f9be1`.

```json
{
  "id": "G-D993depleted",
  "class": "missing_context",
  "affected_ids": [
    "R993",
    "D993depleted"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Depleted status necessary for rout replacement is referenced but unavailable.",
  "needed_context": "Depletion definition and determination",
  "blocking": true,
  "evidence_ids": [
    "E993"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Depleted stan i inne warunki recovery wymagają kontekstu; konflikt z Ferocity po depleted elimination nie rozstrzygnięty.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-062

Zakres oceny: BI startFerocity;BI PreShock-1DRM and defenders+2DRM inshownscope,othermodifiers/procedureunknown

Porównanie oceniającego: R994.conditions zachowuje start game Ferocity dla all BI. Action/parameters: własny Pre-Shock TQ -1 DRM, defending units +2 DRM. To nie modyfikatory wszystkich TQ checks, nie +2 dla BI. Brak scenariusza i base Pre-Shock nie blokuje znanych lokalnych operatorów przy zadanych faktach.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.94-02, PDF 36 right, bbox [315.0, 224.347, 567.029, 270.347], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> All BI units start the game with Ferocity. A BI unit with Ferocity
> earns a –1 DRM to its Pre-Shock TQ die roll while penalizing
> the defending unit(s) with a +2 DRM to their Pre-Shock TQ die
> roll(s).

**first-001 — osobna propozycja i ślady**

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D994scenario, `/gaps/64`, bajty [559696,560235), SHA-256 `5d919573808660c9c61d0d2b42e5ecf28e405da46551b15f001669dfe748d17b`.

```json
{
  "id": "G-D994scenario",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D994pre, `/gaps/65`, bajty [560241,560701), SHA-256 `21dadb238612c398fba0ce48743e0ec9cacb2d701e63cfa3b618d33628bfe9b1`.

```json
{
  "id": "G-D994pre",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994pre"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.",
  "needed_context": "Pre-Shock check procedure",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D994scenario, `/gaps/64`, bajty [645602,646158), SHA-256 `e99c36601e444c56865de2229bbbc9901fea5df5b1d04556fa4885f1ae9b13e3`.

```json
{
  "id": "G-D994scenario",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D994pre, `/gaps/65`, bajty [646165,646642), SHA-256 `f0664691c0576667258d6f0baf116aa7bcc5a7f8a043000596482572a7323116`.

```json
{
  "id": "G-D994pre",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994pre"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.",
  "needed_context": "Pre-Shock check procedure",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Inne DRM i Pre-Shock procedure nie są domknięte.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-063

Zakres oceny: EachordinaryBI RouttriggersFerocitycheckagainstscenarioassignedleaderInitiative;DR<=retains,>losespermanentlyforthatleaderBIcommand,othersunaffected

Porównanie oceniającego: R994 zachowuje check each time BI Routs wobec Initiative leader przypisanego w scenario setup; DR<=Initiative zatrzymuje, wyższy trwale odbiera Ferocity BI tego dowódcy, inne commands bez skutku. Depleted elimination z R993 nie jest automatycznie tym triggerem. Nie wybrano dowódcy ani ratingu.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.94-03, PDF 36 right, bbox [315.0, 277.747, 567.066, 371.747], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.

**first-001 — osobna propozycja i ślady**

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

first-001 R993, `/rules/42`, bajty [377223,381102), SHA-256 `ac9f1b844e212d7c1ed2c0b307f8f974da613cd2137afc21a716bd6ff2f5d820`.

```json
{
  "id": "R993",
  "original_label": {
    "state": "known",
    "value": "9.93",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R993-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Recovery cap"
    },
    {
      "local_clause_id": "R993-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Depleted rout replacement"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "BI units can only remove 1 Cohesion Hit per Recovery order."
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Barbarian Infantry (BI)",
      "Depleted BI"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.93"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E993"
  ],
  "gap_ids": [
    "G-D993recovery",
    "G-D993depleted"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D994scenario, `/gaps/64`, bajty [559696,560235), SHA-256 `5d919573808660c9c61d0d2b42e5ecf28e405da46551b15f001669dfe748d17b`.

```json
{
  "id": "G-D994scenario",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D994pre, `/gaps/65`, bajty [560241,560701), SHA-256 `21dadb238612c398fba0ce48743e0ec9cacb2d701e63cfa3b618d33628bfe9b1`.

```json
{
  "id": "G-D994pre",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994pre"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.",
  "needed_context": "Pre-Shock check procedure",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

context-01 R993, `/rules/42`, bajty [451168,455190), SHA-256 `fdf01acb9629e037cb6f43e05f89f53320c84ff76245e149f5dce967553aa1f3`.

```json
{
  "id": "R993",
  "original_label": {
    "state": "known",
    "value": "9.93",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R993-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Recovery cap"
    },
    {
      "local_clause_id": "R993-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E993"
      ],
      "original_label_text": "9.93",
      "source_clause_locator": "Depleted rout replacement"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "BI units can only remove 1 Cohesion Hit per Recovery order."
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "BI remove only 1 Hit per Recovery order; Depleted BI eliminated instead of Rout.",
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E993"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Barbarian Infantry (BI)",
      "Depleted BI"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.93"
    ],
    "evidence_ids": [
      "E993"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E993"
  ],
  "gap_ids": [
    "G-D993recovery",
    "G-D993depleted"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D994scenario, `/gaps/64`, bajty [645602,646158), SHA-256 `e99c36601e444c56865de2229bbbc9901fea5df5b1d04556fa4885f1ae9b13e3`.

```json
{
  "id": "G-D994scenario",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D994pre, `/gaps/65`, bajty [646165,646642), SHA-256 `f0664691c0576667258d6f0baf116aa7bcc5a7f8a043000596482572a7323116`.

```json
{
  "id": "G-D994pre",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994pre"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.",
  "needed_context": "Pre-Shock check procedure",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Scenario commander mapping i Initiative muszą być dostępne; depleted elimination ≠ jawny Rout trigger.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-064

Zakres oceny: Actualleader/Initiative/membership requires scenariosetup;no nearest/favorable default

Porównanie oceniającego: R994/R995 odwołują się do scenario-assigned command, G-D994scenario i G-D995scenario jawnie blocking=true. Potrzebne actual leader, Initiative i BI membership nie zostały zastąpione najbliższym lub korzystnym leader. Propozycja przyjmuje poprawną potrzebę/blokadę źródła; brak danych wciąż blokuje pełne rzeczywiste zastosowanie, a zadane syntetyczne facts mają własny lokalny zakres.

Propozycja: `source_block_supported`. Obie decyzje właściciela pending.

Źródło C-9.94-03, PDF 36 right, bbox [315.0, 277.747, 567.066, 371.747], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.

Źródło C-9.95-02, PDF 36 right, bbox [315.0, 394.747, 567.026, 500.747], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.

**first-001 — osobna propozycja i ślady**

first-001 R994, `/rules/43`, bajty [381108,386923), SHA-256 `cc7e17ddd619c3317c0da628e589bed64202b03d8d2c7801f4bff68360bd0ddd`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

first-001 R995, `/rules/44`, bajty [386929,392597), SHA-256 `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.

```json
{
  "id": "R995",
  "original_label": {
    "state": "known",
    "value": "9.95",
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R995-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Initial MA bonus"
    },
    {
      "local_clause_id": "R995-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "First-try Momentum modifier"
    },
    {
      "local_clause_id": "R995-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Two-unit trigger/end-of-turn loss"
    },
    {
      "local_clause_id": "R995-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Command-specific scope"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E995"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "BI-commanding leaders"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.95"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Start of game; after trigger retained through remainder of that Game Turn, then lost."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E995"
  ],
  "gap_ids": [
    "G-D995momentum",
    "G-D995scenario",
    "G-D-ZOC-R995"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D994scenario, `/gaps/64`, bajty [559696,560235), SHA-256 `5d919573808660c9c61d0d2b42e5ecf28e405da46551b15f001669dfe748d17b`.

```json
{
  "id": "G-D994scenario",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D994pre, `/gaps/65`, bajty [560241,560701), SHA-256 `21dadb238612c398fba0ce48743e0ec9cacb2d701e63cfa3b618d33628bfe9b1`.

```json
{
  "id": "G-D994pre",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994pre"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.",
  "needed_context": "Pre-Shock check procedure",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D995momentum, `/gaps/66`, bajty [560707,561203), SHA-256 `0b956ea1ee6e93dea84faa748e30ad5008539edbd9c7469466919ced64317394`.

```json
{
  "id": "G-D995momentum",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995momentum"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "First-try Momentum process to receive Impetuosity modifier is referenced but unavailable.",
  "needed_context": "Momentum rules including first-try definition",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D995scenario, `/gaps/67`, bajty [561209,561684), SHA-256 `bc53604b790254e2d489ca478c98c24fcc36710fa8c84e6f25661986168ce51f`.

```json
{
  "id": "G-D995scenario",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "BI command assignment for Impetuosity loss is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D-ZOC-R995, `/gaps/80`, bajty [567564,568024), SHA-256 `d47024d75386d2415530f183f901e005786e4f49d319ad6c14f96e4e64a6ca82`.

```json
{
  "id": "G-D-ZOC-R995",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D-ZOC-R995"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "General ZOC test in rule condition is referenced but unavailable.",
  "needed_context": "General ZOC definition and exceptions",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R994, `/rules/43`, bajty [455197,461221), SHA-256 `09e002a3df1cc15c1fd53543b7f693cbf5b5997287ac95a8d8e0af3a1a0206b0`.

```json
{
  "id": "R994",
  "original_label": {
    "state": "known",
    "value": "9.94",
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R994-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Initial state and two modifiers"
    },
    {
      "local_clause_id": "R994-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Rout trigger/leader assignment"
    },
    {
      "local_clause_id": "R994-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Check comparison/retention/loss"
    },
    {
      "local_clause_id": "R994-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E994"
      ],
      "original_label_text": "9.94",
      "source_clause_locator": "Other-command independence"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "If the DR is the same or lower, BI units retain their Ferocity"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E994"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "defending units",
      "BI’s scenario-assigned leader"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.94"
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Starts game; check each BI Rout; failed check causes permanent loss for that command."
    ],
    "evidence_ids": [
      "E994"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E994"
  ],
  "gap_ids": [
    "G-D994scenario",
    "G-D994pre"
  ],
  "review_status": "unreviewed"
}
```

context-01 R995, `/rules/44`, bajty [461228,467103), SHA-256 `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.

```json
{
  "id": "R995",
  "original_label": {
    "state": "known",
    "value": "9.95",
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R995-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Initial MA bonus"
    },
    {
      "local_clause_id": "R995-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "First-try Momentum modifier"
    },
    {
      "local_clause_id": "R995-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Two-unit trigger/end-of-turn loss"
    },
    {
      "local_clause_id": "R995-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Command-specific scope"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E995"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "BI-commanding leaders"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.95"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Start of game; after trigger retained through remainder of that Game Turn, then lost."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E995"
  ],
  "gap_ids": [
    "G-D995momentum",
    "G-D995scenario",
    "G-D-ZOC-R995"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D994scenario, `/gaps/64`, bajty [645602,646158), SHA-256 `e99c36601e444c56865de2229bbbc9901fea5df5b1d04556fa4885f1ae9b13e3`.

```json
{
  "id": "G-D994scenario",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments and leader Initiative Ratings",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D994pre, `/gaps/65`, bajty [646165,646642), SHA-256 `f0664691c0576667258d6f0baf116aa7bcc5a7f8a043000596482572a7323116`.

```json
{
  "id": "G-D994pre",
  "class": "missing_context",
  "affected_ids": [
    "R994",
    "D994pre"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Base Pre-Shock process to receive Ferocity modifiers is referenced but unavailable.",
  "needed_context": "Pre-Shock check procedure",
  "blocking": true,
  "evidence_ids": [
    "E994"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D995momentum, `/gaps/66`, bajty [646649,647162), SHA-256 `5d49adeccbcf512657b27df883cae3717612a4a46771c714b339e43d411033cc`.

```json
{
  "id": "G-D995momentum",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995momentum"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "First-try Momentum process to receive Impetuosity modifier is referenced but unavailable.",
  "needed_context": "Momentum rules including first-try definition",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D995scenario, `/gaps/67`, bajty [647169,647661), SHA-256 `3042e55550aa4d0b3526b7091ee210120cd7c48bcb016610a6aa8e1105b39d5d`.

```json
{
  "id": "G-D995scenario",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "BI command assignment for Impetuosity loss is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D-ZOC-R995, `/gaps/80`, bajty [653762,654239), SHA-256 `60d830f90cce5dc09348508a78b8687b9d873c9573527169061b07c277d90069`.

```json
{
  "id": "G-D-ZOC-R995",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D-ZOC-R995"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "General ZOC test in rule condition is referenced but unavailable.",
  "needed_context": "General ZOC definition and exceptions",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Actual leader, Initiative and BI command membership require scenario setup.; Jedno wskazane przypisanie scenario wraz z ratings, nie domyślny najbliższy leader.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-065

Zakres oceny: BI startMA+1 and commandingLeader-1allfirsttryMomentum;after>=2distinctBIofsamecommandenterenemyZOC,Impetuosity lastsrestofthatGameTurn thenlostforthatcommandonly

Porównanie oceniającego: R995: wszystkie BI startują MA+1, leaders commanding BI -1 do all first-try Momentum rolls. Trigger >=2 BI units tego samego command entering enemy ZOC, a nie dwie wizyty jednej jednostki. Efekt trwa resztę tego Game Turn i wygasa potem tylko dla tego command. Nie natychmiast po triggerze ani dla całej armii.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.95-02, PDF 36 right, bbox [315.0, 394.747, 567.026, 500.747], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.

**first-001 — osobna propozycja i ślady**

first-001 R995, `/rules/44`, bajty [386929,392597), SHA-256 `d913a1dbefeac66d990266a3fcc8d42616b05ceb1e70c3febeffd81c9643d321`.

```json
{
  "id": "R995",
  "original_label": {
    "state": "known",
    "value": "9.95",
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R995-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Initial MA bonus"
    },
    {
      "local_clause_id": "R995-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "First-try Momentum modifier"
    },
    {
      "local_clause_id": "R995-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Two-unit trigger/end-of-turn loss"
    },
    {
      "local_clause_id": "R995-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Command-specific scope"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E995"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "BI-commanding leaders"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.95"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Start of game; after trigger retained through remainder of that Game Turn, then lost."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E995"
  ],
  "gap_ids": [
    "G-D995momentum",
    "G-D995scenario",
    "G-D-ZOC-R995"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D995momentum, `/gaps/66`, bajty [560707,561203), SHA-256 `0b956ea1ee6e93dea84faa748e30ad5008539edbd9c7469466919ced64317394`.

```json
{
  "id": "G-D995momentum",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995momentum"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "First-try Momentum process to receive Impetuosity modifier is referenced but unavailable.",
  "needed_context": "Momentum rules including first-try definition",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D995scenario, `/gaps/67`, bajty [561209,561684), SHA-256 `bc53604b790254e2d489ca478c98c24fcc36710fa8c84e6f25661986168ce51f`.

```json
{
  "id": "G-D995scenario",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "BI command assignment for Impetuosity loss is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D-ZOC-R995, `/gaps/80`, bajty [567564,568024), SHA-256 `d47024d75386d2415530f183f901e005786e4f49d319ad6c14f96e4e64a6ca82`.

```json
{
  "id": "G-D-ZOC-R995",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D-ZOC-R995"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "General ZOC test in rule condition is referenced but unavailable.",
  "needed_context": "General ZOC definition and exceptions",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R995, `/rules/44`, bajty [461228,467103), SHA-256 `19a5406c171761a9fb3220c189faa76665e113910db1b3ab04d86432f26ce2a8`.

```json
{
  "id": "R995",
  "original_label": {
    "state": "known",
    "value": "9.95",
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R995-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Initial MA bonus"
    },
    {
      "local_clause_id": "R995-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "First-try Momentum modifier"
    },
    {
      "local_clause_id": "R995-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Two-unit trigger/end-of-turn loss"
    },
    {
      "local_clause_id": "R995-C4",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E995"
      ],
      "original_label_text": "9.95",
      "source_clause_locator": "Command-specific scope"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Leaders that command BI units receive a –1 DRM to all first-try Momentum die rolls."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E995"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "BI",
      "BI-commanding leaders"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.95"
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Start of game; after trigger retained through remainder of that Game Turn, then lost."
    ],
    "evidence_ids": [
      "E995"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E995"
  ],
  "gap_ids": [
    "G-D995momentum",
    "G-D995scenario",
    "G-D-ZOC-R995"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D995momentum, `/gaps/66`, bajty [646649,647162), SHA-256 `5d49adeccbcf512657b27df883cae3717612a4a46771c714b339e43d411033cc`.

```json
{
  "id": "G-D995momentum",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995momentum"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "First-try Momentum process to receive Impetuosity modifier is referenced but unavailable.",
  "needed_context": "Momentum rules including first-try definition",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D995scenario, `/gaps/67`, bajty [647169,647661), SHA-256 `3042e55550aa4d0b3526b7091ee210120cd7c48bcb016610a6aa8e1105b39d5d`.

```json
{
  "id": "G-D995scenario",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D995scenario"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "BI command assignment for Impetuosity loss is referenced but unavailable.",
  "needed_context": "Selected scenario BI command assignments",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D-ZOC-R995, `/gaps/80`, bajty [653762,654239), SHA-256 `60d830f90cce5dc09348508a78b8687b9d873c9573527169061b07c277d90069`.

```json
{
  "id": "G-D-ZOC-R995",
  "class": "missing_context",
  "affected_ids": [
    "R995",
    "D-ZOC-R995"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "General ZOC test in rule condition is referenced but unavailable.",
  "needed_context": "General ZOC definition and exceptions",
  "blocking": true,
  "evidence_ids": [
    "E995"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Mapping command, ZOC i Momentum wymagają danych; lokalny czas wygaśnięcia jest jawny.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-066

Zakres oceny: GallictransportCHCombatTablesignoreinstruction retained;exacttables/entriesrequirecontext alreadyRQ05scope

Porównanie oceniającego: R996note zachowuje ignore Chariots reference on Combat Tables; N996design nie tworzy dodatkowego skutku. N-14-S2 to dokładna instrukcja, N-14-S3 appearances Sentinum/Telamon, bez listy eligibility wszystkich LI. G-D996tables deklaruje potrzebę actual tables/entries, ale blocking=false; D996tables blocks_full_result=false. Lokalny zakaz użycia wiersza znany, konkretne identyfikowanie suppressowanych entries niezamknięte. Właściciel rozstrzyga wystarczalność jawnej blokady zależnego pełnego pytania. Nie ma konkretnego niepoprawnego lookupu, nie jest to automatyczny błąd odczytu lub FP.

Propozycja: `partial_context_declaration_pending`. Obie decyzje właściciela pending.

Źródło N-14-S2, PDF 36 right, bbox [319.0, 524.85, 563.026, 618.85], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Thus, ignore the reference
> to Chariots on the Combat Tables.

Źródło N-14-S3, PDF 36 right, bbox [319.0, 524.85, 563.026, 618.85], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> However, the tribes were
> quite adept at using them to whatever advantage they did of-
> fer. In this module, chariots make an appearance at Sentinum
> and Telamon.

**first-001 — osobna propozycja i ślady**

first-001 N996design, `/nodes/30`, bajty [146679,147468), SHA-256 `c01e2df13e259d2b65d4ec89dee199481937bd990757f3a83e9f9dc5ce3784dd`.

```json
{
  "id": "N996design",
  "kind": "other",
  "original_label": {
    "state": "known",
    "value": "DESIGN NOTE:",
    "evidence_ids": [
      "E996design"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
    "state": "known",
    "value": "Gallic chariots historically transport rather than weapons. Operative instruction to ignore Combat Table Chariot references and module appearances owned by R996note.",
    "evidence_ids": [
      "E996design"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996design"
  ],
  "review_status": "unreviewed",
  "source_locator": "DESIGN NOTE (9.96) — historical portion"
}
```

first-001 R996note, `/rules/45`, bajty [392603,396286), SHA-256 `3dfdaccd8a573ddf99e083715c467fb8a36ec4ad52929c71b7259de8de628ab5`.

```json
{
  "id": "R996note",
  "original_label": {
    "state": "known",
    "value": "DESIGN NOTE:",
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996note-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996note"
      ],
      "original_label_text": "DESIGN NOTE:",
      "source_clause_locator": "Ignore Combat Table Chariot reference"
    },
    {
      "local_clause_id": "R996note-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996note"
      ],
      "original_label_text": "DESIGN NOTE:",
      "source_clause_locator": "Module appearances"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Thus, ignore the reference to Chariots on the Combat Tables."
    ],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
    "evidence_ids": [
      "E996note"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot"
    ],
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Transport role and table-reference suppression; module appearances Sentinum/Telamon."
    ],
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E996note"
  ],
  "gap_ids": [
    "G-D996tables"
  ],
  "review_status": "unreviewed",
  "source_locator": "DESIGN NOTE (9.96)"
}
```

first-001 D996tables, `/dependencies/108`, bajty [512527,513635), SHA-256 `1f7003a3d4d4e84827c18ca49ade9e7bb6d3e7bf41627b4af176911bda5c0b8a`.

```json
{
  "id": "D996tables",
  "from": "R996note",
  "to": null,
  "target_candidate": {
    "original_reference": "Chariots on the Combat Tables",
    "description": "Combat Table Chariot references ignored for transport chariots",
    "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause"
  },
  "kind": "exception",
  "explicitness": "explicit",
  "rationale": "Source refers to Chariots on the Combat Tables; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.",
  "evidence_ids": [
    "E996note"
  ],
  "target_status": "unresolved",
  "impact_if_missing": {
    "affected_ids": [
      "R996note"
    ],
    "blocks_full_result": false,
    "reason": "Combat Table Chariot references ignored for transport chariots is not fully supplied; no missing content reconstructed."
  },
  "gap_ids": [
    "G-D996tables"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996tables, `/gaps/68`, bajty [561690,562253), SHA-256 `4d25580273e2f47e9861742228dfda824e123a8c160529580af039237d78a715`.

```json
{
  "id": "G-D996tables",
  "class": "missing_context",
  "affected_ids": [
    "R996note",
    "D996tables"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Combat Table Chariot references ignored for transport chariots is referenced but unavailable.",
  "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause",
  "blocking": false,
  "evidence_ids": [
    "E996note"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 N996design, `/nodes/30`, bajty [195676,196492), SHA-256 `7ad32edfe26a51d99e6ab415bbb1f85fc82f8061c5071dd33970b43437e5378f`.

```json
{
  "id": "N996design",
  "kind": "other",
  "original_label": {
    "state": "known",
    "value": "DESIGN NOTE:",
    "evidence_ids": [
      "E996design"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
    "state": "known",
    "value": "Gallic chariots historically transport rather than weapons. Operative instruction to ignore Combat Table Chariot references and module appearances owned by R996note.",
    "evidence_ids": [
      "E996design"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996design"
  ],
  "review_status": "unreviewed",
  "source_locator": "DESIGN NOTE (9.96) — historical portion"
}
```

context-01 R996note, `/rules/45`, bajty [467110,470918), SHA-256 `88c04eae1baf89929461610b1d701ea1201da58987d814350fdcfb5516d2ec76`.

```json
{
  "id": "R996note",
  "original_label": {
    "state": "known",
    "value": "DESIGN NOTE:",
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996note-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996note"
      ],
      "original_label_text": "DESIGN NOTE:",
      "source_clause_locator": "Ignore Combat Table Chariot reference"
    },
    {
      "local_clause_id": "R996note-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996note"
      ],
      "original_label_text": "DESIGN NOTE:",
      "source_clause_locator": "Module appearances"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Thus, ignore the reference to Chariots on the Combat Tables."
    ],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
    "state": "known",
    "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
    "evidence_ids": [
      "E996note"
    ],
    "reason": "Interpretation confined to supplied source; no external procedures reconstructed.",
    "gap_ids": []
  },
  "conditions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "No additional prerequisite stated in this identified clause.",
    "gap_ids": []
  },
  "action_effect": {
    "state": "known",
    "value": "Gallic chariots are transport; ignore Chariot reference on Combat Tables. In this module they appear at Sentinum and Telamon.",
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996note"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot"
    ],
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Transport role and table-reference suppression; module appearances Sentinum/Telamon."
    ],
    "evidence_ids": [
      "E996note"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "not_applicable",
    "value": null,
    "evidence_ids": [],
    "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
    "gap_ids": []
  },
  "evidence_ids": [
    "E996note"
  ],
  "gap_ids": [
    "G-D996tables"
  ],
  "review_status": "unreviewed",
  "source_locator": "DESIGN NOTE (9.96)"
}
```

context-01 D996tables, `/dependencies/108`, bajty [590968,592103), SHA-256 `f4555792332ddf87bf519ee6a9231583e2516e597f413bb1afa7a4b5ea93bccb`.

```json
{
  "id": "D996tables",
  "from": "R996note",
  "to": null,
  "target_candidate": {
    "original_reference": "Chariots on the Combat Tables",
    "description": "Combat Table Chariot references ignored for transport chariots",
    "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause"
  },
  "kind": "exception",
  "explicitness": "explicit",
  "rationale": "Source refers to Chariots on the Combat Tables; direction is referring clause to the unavailable target. Its contents are needed to fully execute or determine the stated result.",
  "evidence_ids": [
    "E996note"
  ],
  "target_status": "unresolved",
  "impact_if_missing": {
    "affected_ids": [
      "R996note"
    ],
    "blocks_full_result": false,
    "reason": "Combat Table Chariot references ignored for transport chariots is not fully supplied; no missing content reconstructed."
  },
  "gap_ids": [
    "G-D996tables"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996tables, `/gaps/68`, bajty [647668,648248), SHA-256 `709d00bec15889990cc4d425d9ee7b2f041b8814b8f0bf029e59286bcc067d4b`.

```json
{
  "id": "G-D996tables",
  "class": "missing_context",
  "affected_ids": [
    "R996note",
    "D996tables"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Combat Table Chariot references ignored for transport chariots is referenced but unavailable.",
  "needed_context": "Actual combat tables only to identify suppressed Chariot entries; no execution permitted by this clause",
  "blocking": false,
  "evidence_ids": [
    "E996note"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Exact Combat Tables and relevant entries are required; no values are guessed.; Dokładne Combat Tables i ich chariot entries, decision owner o zakresie; nie traktować Sentinum/Telamon jako listy eligibility wszystkich LI.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-067

Zakres oceny: CHonlyMA,noSize/TQ;cannotmoveincludingOWwithouteligibleLI;enemycombatmovingadjacenttosolitaryCH eliminatesit;staticadjacency notthegivenmovementtrigger

Porównanie oceniającego: R996a: CH ma tylko MA, brak Size/TQ. Bez stacked eligible LI zakaz wszelkiego ruchu, także OW. Enemy combat unit any type moving adjacent do CH alone eliminuje go natychmiast. Static adjacency nie jest podanym triggerem. Szerszy time_limits mówi qualifying adjacency; operacyjny trigger pozostaje w action_effect. Nie nadaje się CH ratingów Roman top-unit.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.96-02, PDF 36 right, bbox [315.0, 628.09, 567.019, 698.09], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Gallic Chariot (CH) units have only a Movement Allowance;
> they have no Size and no TQ Rating. These units cannot move
> at all, and this includes Orderly Withdrawal, unless stacked with
> an eligible Light Infantry (LI) unit. If an enemy combat unit (of
> any type) moves adjacent to a CH unit alone in a hex, the CH
> unit is immediately eliminated.

**first-001 — osobna propozycja i ślady**

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996eligible, `/gaps/69`, bajty [562259,562746), SHA-256 `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996OW, `/gaps/70`, bajty [562752,563192), SHA-256 `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996stack, `/gaps/71`, bajty [563198,563649), SHA-256 `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996movement, `/gaps/72`, bajty [563655,564128), SHA-256 `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996MRRC, `/gaps/73`, bajty [564134,564595), SHA-256 `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996supply, `/gaps/74`, bajty [564601,565114), SHA-256 `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996HD, `/gaps/75`, bajty [565120,565603), SHA-256 `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996eligible, `/gaps/69`, bajty [648255,648759), SHA-256 `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996OW, `/gaps/70`, bajty [648766,649223), SHA-256 `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996stack, `/gaps/71`, bajty [649230,649698), SHA-256 `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996movement, `/gaps/72`, bajty [649705,650195), SHA-256 `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996MRRC, `/gaps/73`, bajty [650202,650680), SHA-256 `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996supply, `/gaps/74`, bajty [650687,651217), SHA-256 `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996HD, `/gaps/75`, bajty [651224,651724), SHA-256 `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Eligibility LI scenariuszowa nieuzupełniona; samotny CH da się ocenić lokalnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-068

Zakres oceny: oneLIperCH,CHtopdenotesmounted,combinedsingleforstackingbutotherrestrictionsretained

Porównanie oceniającego: R996b zachowuje jeden LI na CH, CH na górze oznacza mounted, kombinacja single unit tylko dla stacking; all other restrictions dla CH+LI i CH alone nadal obowiązują. Continuation PDF36right→37left zawiera pełne zdanie. Nie stosuje Roman top/TQ do transport CH i nie przyznaje pełnej legalności stacking.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.96-03, PDF 36 right, bbox [315.0, 705.49, 567.026, 739.49], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Źródło C-9.96-03, PDF 37 left, bbox [45.0, 54.004, 297.469, 220.004], render SHA-256 `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

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

**first-001 — osobna propozycja i ślady**

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996eligible, `/gaps/69`, bajty [562259,562746), SHA-256 `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996OW, `/gaps/70`, bajty [562752,563192), SHA-256 `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996stack, `/gaps/71`, bajty [563198,563649), SHA-256 `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996movement, `/gaps/72`, bajty [563655,564128), SHA-256 `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996MRRC, `/gaps/73`, bajty [564134,564595), SHA-256 `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996supply, `/gaps/74`, bajty [564601,565114), SHA-256 `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996HD, `/gaps/75`, bajty [565120,565603), SHA-256 `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996eligible, `/gaps/69`, bajty [648255,648759), SHA-256 `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996OW, `/gaps/70`, bajty [648766,649223), SHA-256 `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996stack, `/gaps/71`, bajty [649230,649698), SHA-256 `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996movement, `/gaps/72`, bajty [649705,650195), SHA-256 `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996MRRC, `/gaps/73`, bajty [650202,650680), SHA-256 `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996supply, `/gaps/74`, bajty [650687,651217), SHA-256 `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996HD, `/gaps/75`, bajty [651224,651724), SHA-256 `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Nie używać roman top/TQ jako zasad CH; brak TQ/Size CH zachować.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-069

Zakres oceny: mount/dismount0MP/CH;dismountcontinueonlyifcomboMPspent<LIprintedMA,remainingdifference;mountremainingCHMAminusLIalreadyusedMP

Porównanie oceniającego: R996b: mount/dismount 0 MP i 0 Cohesion Hits dla LI. Dismount dalszy ruch tylko gdy combo MPs used < LI printed MA, pozostałe MP równe różnicy. Mount pozwala kontynuować jako CH do CH MA minus MPs already used przez LI. Strict < i printed LI MA zachowane; nie odtworzono MP od zera, żadna trasa/eligibility/MA nie została zgadnięta.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.96-03, PDF 36 right, bbox [315.0, 705.49, 567.026, 739.49], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Źródło C-9.96-03, PDF 37 left, bbox [45.0, 54.004, 297.469, 220.004], render SHA-256 `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

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

**first-001 — osobna propozycja i ślady**

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996eligible, `/gaps/69`, bajty [562259,562746), SHA-256 `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996OW, `/gaps/70`, bajty [562752,563192), SHA-256 `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996stack, `/gaps/71`, bajty [563198,563649), SHA-256 `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996movement, `/gaps/72`, bajty [563655,564128), SHA-256 `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996MRRC, `/gaps/73`, bajty [564134,564595), SHA-256 `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996supply, `/gaps/74`, bajty [564601,565114), SHA-256 `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996HD, `/gaps/75`, bajty [565120,565603), SHA-256 `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996eligible, `/gaps/69`, bajty [648255,648759), SHA-256 `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996OW, `/gaps/70`, bajty [648766,649223), SHA-256 `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996stack, `/gaps/71`, bajty [649230,649698), SHA-256 `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996movement, `/gaps/72`, bajty [649705,650195), SHA-256 `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996MRRC, `/gaps/73`, bajty [650202,650680), SHA-256 `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996supply, `/gaps/74`, bajty [650687,651217), SHA-256 `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996HD, `/gaps/75`, bajty [651224,651724), SHA-256 `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Ocenia się lokalny budżet przy supplied eligibility, MA i MP; trasa wymaga tabeli.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-070

Zakres oceny: MovementCostChart governsCHMP/prohibitions;movementCohesionHitsLIonly,notCH;no waiverofterrainprohibitions

Porównanie oceniającego: R996b zachowuje CH MP costs oraz zakazy entering/crossing według Movement Cost Chart przy LI. Movement/Terrain Cohesion Hits do LI only, CH ich nie otrzymuje. G-D996movement blocking=true dla konkretnej trasy. To nie zwolnienie z zakazu terenu ani zwolnienie LI z wszystkich Hits.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.96-03, PDF 36 right, bbox [315.0, 705.49, 567.026, 739.49], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Źródło C-9.96-03, PDF 37 left, bbox [45.0, 54.004, 297.469, 220.004], render SHA-256 `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

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

**first-001 — osobna propozycja i ślady**

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996eligible, `/gaps/69`, bajty [562259,562746), SHA-256 `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996OW, `/gaps/70`, bajty [562752,563192), SHA-256 `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996stack, `/gaps/71`, bajty [563198,563649), SHA-256 `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996movement, `/gaps/72`, bajty [563655,564128), SHA-256 `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996MRRC, `/gaps/73`, bajty [564134,564595), SHA-256 `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996supply, `/gaps/74`, bajty [564601,565114), SHA-256 `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996HD, `/gaps/75`, bajty [565120,565603), SHA-256 `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996eligible, `/gaps/69`, bajty [648255,648759), SHA-256 `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996OW, `/gaps/70`, bajty [648766,649223), SHA-256 `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996stack, `/gaps/71`, bajty [649230,649698), SHA-256 `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996movement, `/gaps/72`, bajty [649705,650195), SHA-256 `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996MRRC, `/gaps/73`, bajty [650202,650680), SHA-256 `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996supply, `/gaps/74`, bajty [650687,651217), SHA-256 `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996HD, `/gaps/75`, bajty [651224,651724), SHA-256 `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Konkretna trasa bez Movement Cost Chart pozostaje zablokowana.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-071

Zakres oceny: repeat-movementHitexceptiononlyentireOrdersPhasemounted;partialphasemountinsufficient

Porównanie oceniającego: R996c: zwolnienie LI z second/third movement Hits w Game Turn tylko jeśli entire Orders Phase mounted. Wybrany literalny cytat urywa się przed if, lecz conditions i action_effect zachowują całe ograniczenie. Nie przyznano zwolnienia za częściowe mount lub dla terrain Hits.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.96-05, PDF 37 left, bbox [45.0, 254.284, 297.001, 288.284], render SHA-256 `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

> • LI do not suffer any Cohesion Hits for moving a second (and
> third) time in a Game Turn, if they spend the entire Orders
> Phase mounted on the CH unit.

**first-001 — osobna propozycja i ślady**

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996eligible, `/gaps/69`, bajty [562259,562746), SHA-256 `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996OW, `/gaps/70`, bajty [562752,563192), SHA-256 `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996stack, `/gaps/71`, bajty [563198,563649), SHA-256 `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996movement, `/gaps/72`, bajty [563655,564128), SHA-256 `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996MRRC, `/gaps/73`, bajty [564134,564595), SHA-256 `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996supply, `/gaps/74`, bajty [564601,565114), SHA-256 `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996HD, `/gaps/75`, bajty [565120,565603), SHA-256 `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996eligible, `/gaps/69`, bajty [648255,648759), SHA-256 `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996OW, `/gaps/70`, bajty [648766,649223), SHA-256 `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996stack, `/gaps/71`, bajty [649230,649698), SHA-256 `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996movement, `/gaps/72`, bajty [649705,650195), SHA-256 `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996MRRC, `/gaps/73`, bajty [650202,650680), SHA-256 `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996supply, `/gaps/74`, bajty [650687,651217), SHA-256 `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996HD, `/gaps/75`, bajty [651224,651724), SHA-256 `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: General repeat movement i pozostałe terrain Hits oddzielnie.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-072

Zakres oceny: mountedLInoShockattack,mustdismount;defendsasLI,notfullattackpermissionafterdismount

Porównanie oceniającego: R996c jawnie Mounted LI cannot Shock attack; must dismount; defends as LI. Dismount jest konieczny, nie stanowi pełnej zgody na późniejszy attack bez pozostałych warunków. Nie zamieniono defend as LI na attack jako cavalry.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.96-06, PDF 37 left, bbox [45.0, 291.724, 297.003, 313.724], render SHA-256 `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

> • LI cannot Shock attack; they must dismount to do so. When
> mounted, they defend as LI.

**first-001 — osobna propozycja i ślady**

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996eligible, `/gaps/69`, bajty [562259,562746), SHA-256 `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996OW, `/gaps/70`, bajty [562752,563192), SHA-256 `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996stack, `/gaps/71`, bajty [563198,563649), SHA-256 `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996movement, `/gaps/72`, bajty [563655,564128), SHA-256 `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996MRRC, `/gaps/73`, bajty [564134,564595), SHA-256 `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996supply, `/gaps/74`, bajty [564601,565114), SHA-256 `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996HD, `/gaps/75`, bajty [565120,565603), SHA-256 `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996eligible, `/gaps/69`, bajty [648255,648759), SHA-256 `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996OW, `/gaps/70`, bajty [648766,649223), SHA-256 `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996stack, `/gaps/71`, bajty [649230,649698), SHA-256 `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996movement, `/gaps/72`, bajty [649705,650195), SHA-256 `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996MRRC, `/gaps/73`, bajty [650202,650680), SHA-256 `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996supply, `/gaps/74`, bajty [650687,651217), SHA-256 `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996HD, `/gaps/75`, bajty [651224,651724), SHA-256 `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Dismount nie dowodzi legalności późniejszego attack bez pozostałych warunków.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-073

Zakres oceny: Mounted LI uses Mounted Javelin MRRC, is exempt from Missile Supply 8.17 while mounted, removes LOW/NO on mounting, and uses H&D as cavalry. No post-dismount supply state or equivalence with the hypothesized 9.13 row is inferred.

Porównanie oceniającego: R996d zachowuje dokładnie nazwę Mounted Javelin MRRC, exemption Missile Supply8.17 while mounted, remove LOW/NO when mounts i H&D as cavalry. Nie zgaduje post-dismount supply, nie utożsamia tej row z hipotetycznym 9.13. G-D996MRRC/HD blocking=true; nonblocking supply dotyczy znanego lokalnego wyjątku/marker removal, bez rozstrzygania pełnej procedury.

Propozycja: `supported_local_scope`. Obie decyzje właściciela pending.

Źródło C-9.96-07, PDF 37 left, bbox [45.0, 317.164, 297.05, 375.164], render SHA-256 `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

> • LI may use Missile Fire using the Mounted Javelin row on the
> MRRC. Missile Supply (8.17) does not apply while the LI unit
> is mounted. Remove any MiSSile low/No markers from the LI
> unit when the unit mounts a CH. They may use Harassment
> and Dispersal fire as if they were cavalry units.

**first-001 — osobna propozycja i ślady**

first-001 R996a, `/rules/46`, bajty [396292,400339), SHA-256 `c952d38a534c36e42f9f29bf06d338b6e8c36dd2f52e26d5ebd1925c7b017ec0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996b, `/rules/47`, bajty [400345,409010), SHA-256 `3a76e8b78b318352b58c33ae9c20c6a3c13e9af7610add15f8a3edaac931f3b4`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

first-001 R996c, `/rules/48`, bajty [409016,413605), SHA-256 `bfbcd6b3ebcdf10d3da63ed0beb0819722403b336f45044dcf3ac5439b3f7947`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

first-001 R996d, `/rules/49`, bajty [413611,417619), SHA-256 `0ccbb98746b0fd7c045de79206716708f6fcb11578bb3a52e0751bbbe8cea95b`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996eligible, `/gaps/69`, bajty [562259,562746), SHA-256 `df15b414492d3ff7584de296e2e75cdb7e512d2f27a6aa4f5071d82a9a858612`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996OW, `/gaps/70`, bajty [562752,563192), SHA-256 `944770eed560ae9641d3051e9ff3259ade7097efe43a0e7dc5d5339f1fc9a707`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996stack, `/gaps/71`, bajty [563198,563649), SHA-256 `bf41413a42bd0e7d25d3d7f180563c0a6c429035e320f39ff69d3edf2ad56257`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996movement, `/gaps/72`, bajty [563655,564128), SHA-256 `4267159f9288b55b5002b10abe01544cafb49a8d74ce044503319c1e06467024`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996MRRC, `/gaps/73`, bajty [564134,564595), SHA-256 `934d66d30d35a94c45856227f8e3616a3fae4a79ab4fae504d1c5e8bd3817df4`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996supply, `/gaps/74`, bajty [564601,565114), SHA-256 `3b31e94db3242b9d49df2af266767a52fdec31456cdc1bb2993614c8b347a2e8`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

first-001 G-D996HD, `/gaps/75`, bajty [565120,565603), SHA-256 `e9cd457881123a9018b83c9e54ba89d7cd19db348e4d85e9a0bde6dda08ca994`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 R996a, `/rules/46`, bajty [470925,475124), SHA-256 `31cc8191b10247405968e870ba80d461dd280f7ab350aa964f281289001431f0`.

```json
{
  "id": "R996a",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996a-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Ratings absence"
    },
    {
      "local_clause_id": "R996a-C2",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "LI-dependent movement/OW"
    },
    {
      "local_clause_id": "R996a-C3",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996a"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Alone adjacency elimination"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH) units have only a Movement Allowance; they have no Size and no TQ Rating."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "CH must be stacked with eligible LI to move, including OW."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Movement allowed when stacked with eligible LI."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996a"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)",
      "enemy combat unit of any type"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Immediate elimination on qualifying enemy adjacency."
    ],
    "evidence_ids": [
      "E996a"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996a"
  ],
  "gap_ids": [
    "G-D996eligible",
    "G-D996OW"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996b, `/rules/47`, bajty [475131,484102), SHA-256 `d2bb159fb975e91f07a858964e588474dfa7b7aee724282a5906412dfd46341e`.

```json
{
  "id": "R996b",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996b-C1",
      "region_id": "pdf-36-core-right",
      "evidence_ids": [
        "E996b"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Capacity and counter order"
    },
    {
      "local_clause_id": "R996b-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "One stacking unit continuation/other restrictions"
    },
    {
      "local_clause_id": "R996b-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Zero mount/dismount cost"
    },
    {
      "local_clause_id": "R996b-C4",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Dismounting continuation"
    },
    {
      "local_clause_id": "R996b-C5",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounting continuation"
    },
    {
      "local_clause_id": "R996b-C6",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996c"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Terrain costs/prohibitions and Hits"
    }
  ],
  "transcription": {
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
  },
  "interpretation": {
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
  },
  "conditions": {
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
  },
  "action_effect": {
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
  },
  "exceptions": {
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
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "Gallic Chariot (CH)",
      "eligible Light Infantry (LI)"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996b",
      "E996c"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
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
  },
  "evidence_ids": [
    "E996b",
    "E996c"
  ],
  "gap_ids": [
    "G-D996stack",
    "G-D996movement"
  ],
  "review_status": "unreviewed"
}
```

context-01 R996c, `/rules/48`, bajty [484109,488868), SHA-256 `1f3e2dbbb4efb9a63335cf1463774f03732fe2e21db53e9b1580a1d0c538a1bf`.

```json
{
  "id": "R996c",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996c-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 1 — repeated-movement exemption"
    },
    {
      "local_clause_id": "R996c-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996d"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "bullet 2 — Shock attack prohibition and LI defense"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "LI do not suffer any Cohesion Hits for moving a second (and third) time in a Game Turn"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI spends entire Orders Phase mounted on CH for repeated-movement exemption."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996d"
    ],
    "reason": "No exception stated within this identified clause; external rules may qualify it.",
    "gap_ids": []
  },
  "parameters": {
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
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "Entire Orders Phase mounted; second and third movement in Game Turn."
    ],
    "evidence_ids": [
      "E996d"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996d"
  ],
  "gap_ids": [],
  "review_status": "unreviewed"
}
```

context-01 R996d, `/rules/49`, bajty [488875,493035), SHA-256 `a17a2137ba84dc2e998c5849537c2b675955358a793cf6afbd1ac6a7855fe2c6`.

```json
{
  "id": "R996d",
  "original_label": {
    "state": "known",
    "value": "9.96",
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "clause_map": [
    {
      "local_clause_id": "R996d-C1",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Mounted LI bullet 3 — MRRC row"
    },
    {
      "local_clause_id": "R996d-C2",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Supply exception and marker removal"
    },
    {
      "local_clause_id": "R996d-C3",
      "region_id": "pdf-37-core-left",
      "evidence_ids": [
        "E996e"
      ],
      "original_label_text": "9.96",
      "source_clause_locator": "Cavalry H&D permission"
    }
  ],
  "transcription": {
    "state": "known",
    "value": [
      "Missile Supply (8.17) does not apply while the LI unit is mounted."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "Selected literal excerpts; complete operative content is separately summarized in action_effect and linked source images.",
    "gap_ids": []
  },
  "interpretation": {
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
  },
  "conditions": {
    "state": "known",
    "value": [
      "LI mounted on CH."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "action_effect": {
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
  },
  "exceptions": {
    "state": "known",
    "value": [
      "Mounted LI exempt from Missile Supply."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "parameters": {
    "state": "established_absent",
    "value": [],
    "evidence_ids": [
      "E996e"
    ],
    "reason": "No numerical parameter stated within this identified clause.",
    "gap_ids": []
  },
  "unit_types": {
    "state": "known",
    "value": [
      "LI mounted on CH",
      "cavalry for H&D treatment"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_limits": {
    "state": "known",
    "value": [
      "Chapter 9.0; 9.96"
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "time_limits": {
    "state": "known",
    "value": [
      "While mounted; remove supply markers on mounting."
    ],
    "evidence_ids": [
      "E996e"
    ],
    "reason": null,
    "gap_ids": []
  },
  "evidence_ids": [
    "E996e"
  ],
  "gap_ids": [
    "G-D996MRRC",
    "G-D996supply",
    "G-D996HD"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996eligible, `/gaps/69`, bajty [648255,648759), SHA-256 `8629e6ef134412ea98deedeed877f24fc9870a1f9443622bb33ca561d74fc6eb`.

```json
{
  "id": "G-D996eligible",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996eligible"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "Which LI may ride Gallic chariots is referenced but unavailable.",
  "needed_context": "Eligibility definition/scenario restrictions for mounted LI",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996OW, `/gaps/70`, bajty [648766,649223), SHA-256 `5c985cf30073bd5ccb7177de97f9abd0690725aa886d12f9f902de6a99810a46`.

```json
{
  "id": "G-D996OW",
  "class": "missing_context",
  "affected_ids": [
    "R996a",
    "D996OW"
  ],
  "source_regions": [
    "pdf-36-core-right"
  ],
  "reason": "CH+LI OW eligibility if mounted is referenced but unavailable.",
  "needed_context": "OW rules for mounted LI/CH",
  "blocking": true,
  "evidence_ids": [
    "E996a"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996stack, `/gaps/71`, bajty [649230,649698), SHA-256 `fb8324b1213f928731abeedab089ab055e0cd3f9c30c7d3c9a993461c5dcdac3`.

```json
{
  "id": "G-D996stack",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996stack"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Other limits on CH+LI and CH alone is referenced but unavailable.",
  "needed_context": "General stacking restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996movement, `/gaps/72`, bajty [649705,650195), SHA-256 `cb9781836ad589de1610924b04d5a6648d48dd66ff3f9c1033a5953339116bbf`.

```json
{
  "id": "G-D996movement",
  "class": "missing_context",
  "affected_ids": [
    "R996b",
    "D996movement"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "CH terrain MP costs/prohibitions is referenced but unavailable.",
  "needed_context": "Actual Movement Cost Chart with CH restrictions",
  "blocking": true,
  "evidence_ids": [
    "E996c"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996MRRC, `/gaps/73`, bajty [650202,650680), SHA-256 `d4cd93bfb3b34d1c4d42807d7e86bd230b7fd04870f9e60c9bc25a9c9f2f7e67`.

```json
{
  "id": "G-D996MRRC",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996MRRC"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI missile range/results is referenced but unavailable.",
  "needed_context": "MRRC Mounted Javelin row, headers and notes",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996supply, `/gaps/74`, bajty [650687,651217), SHA-256 `e2167a6c172ffdd5821cad595bfd289e50d03c8b1aaa1ce1e5a3cf6a5a21e43b`.

```json
{
  "id": "G-D996supply",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996supply"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Missile Supply exception while mounted is referenced but unavailable.",
  "needed_context": "8.17 including normal supply state rules; mounting marker removal itself is explicit",
  "blocking": false,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

context-01 G-D996HD, `/gaps/75`, bajty [651224,651724), SHA-256 `58c5259ac1031c46f4a3d39de79bf3e18c74adff512368a5d0004c9083f2ea4f`.

```json
{
  "id": "G-D996HD",
  "class": "missing_context",
  "affected_ids": [
    "R996d",
    "D996HD"
  ],
  "source_regions": [
    "pdf-37-core-left"
  ],
  "reason": "Mounted LI cavalry-style H&D procedure is referenced but unavailable.",
  "needed_context": "Harassment and Dispersal procedure including cavalry conditions",
  "blocking": true,
  "evidence_ids": [
    "E996e"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Nie zgadywać podaży po późniejszym dismount ani pełnego MRRC/H&D; display annotation06c zachowuje original helper.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

### EXP-074

Zakres oceny: Confirm actualidentifiedunit TQ/MA before concreteuse; not alltinygraphicratings were individuallyverified inthisreview. SyntheticinputTQ6 doesnotestablishactualLeaderElephantTQ. Keeprequires_context foractualvalues.

Porównanie oceniającego: N911counter/N921counter/N981counter podają visible glyphs, lecz wyraźnie wykluczają game-wide values i rating-position inference. N966diagram mówi illustrative, not general Roman parameters; N985markers/N986marker to stany markerów. Brak twierdzenia o realnym Leader Elephant TQ6. Równocześnie nie ma osobnego gap ani jawnej conditional blocking deklaracji actual identified TQ/MA przed concrete use. Właściciel rozstrzyga, czy zapis illustrative wystarcza dla ograniczonego wymagania EXP-074. Same oględziny paneli/states nie certyfikują małych ratingów, tożsamości konkretnych jednostek ani 64 granic glifów. Criticality pozostaje conditional_on_concrete_parameter_use.

Propozycja: `illustration_boundary_supported_block_declaration_pending`. Obie decyzje właściciela pending.

Źródło G-01, PDF 31 right, bbox [315, 482, 352, 521], render SHA-256 `39f86ad053725088e9c571f43d1e8ecc4dbf21f5b191cc1e7d99cc854ddc34ba`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

Źródło G-02, PDF 33 right, bbox [315, 239, 352, 276], render SHA-256 `3ba367da1aee5635f964b887ff518ec63ba48175278e3fefdb031a8e03a7d15d`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

Źródło G-03, PDF 36 left, bbox [45, 71, 82, 109], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

Źródło D-02, PDF 35 left, bbox [80, 516, 266, 674], render SHA-256 `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

Źródło G-04, PDF 36 left, bbox [45, 365, 120, 404], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

Źródło G-05, PDF 36 left, bbox [260, 528, 297, 566], render SHA-256 `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

Dowód graficzny; brak literalnego pola tekstowego. Oględziny ograniczone do roli ilustracji/stanów, bez certyfikatu ratingów.

**first-001 — osobna propozycja i ślady**

first-001 N911counter, `/nodes/31`, bajty [147474,148541), SHA-256 `23d5455d6e3e846f2793ab9162a4d52e351dec50fdbb6c82f9bbdf60726cf009`.

```json
{
  "id": "N911counter",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Africa",
    "evidence_ids": [
      "E911counter"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E911counter"
  ],
  "review_status": "unreviewed",
  "source_locator": "Illustrative counter — Africa / EL"
}
```

first-001 N921counter, `/nodes/32`, bajty [148547,149599), SHA-256 `30e857892be2b6c8be03571a7cf4d4176065f50d0ebbc1464ce5742405a3dc86`.

```json
{
  "id": "N921counter",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Bal'ric",
    "evidence_ids": [
      "E921counter"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E921counter"
  ],
  "review_status": "unreviewed",
  "source_locator": "Illustrative counter — Bal’ric / SK"
}
```

first-001 N966diagram, `/nodes/7`, bajty [128977,130323), SHA-256 `f5c32b1dae24067c8069c9f6a259e1da4cd473f61255ce80b5b070a71cc69689`.

```json
{
  "id": "N966diagram",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Original Deployment / After Manipular Line Extension",
    "evidence_ids": [
      "E966diagram"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E966diagram"
  ],
  "review_status": "unreviewed"
}
```

first-001 N981counter, `/nodes/33`, bajty [149605,150636), SHA-256 `5598ad644a67222e29a3ec1778f8d63074add8759087c77097a583b05c918b7b`.

```json
{
  "id": "N981counter",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Scorpio",
    "evidence_ids": [
      "E981counter"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E981counter"
  ],
  "review_status": "unreviewed",
  "source_locator": "Illustrative counter — Scorpio / LI"
}
```

first-001 N985markers, `/nodes/34`, bajty [150642,151434), SHA-256 `7e5c2a786b20ef970bd132c76fad600d3c7f7fdf1ceda5d1f40250a08c6be599`.

```json
{
  "id": "N985markers",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Active Fire markers",
    "evidence_ids": [
      "E985markers"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E985markers"
  ],
  "review_status": "unreviewed"
}
```

first-001 N986marker, `/nodes/35`, bajty [151440,152165), SHA-256 `eec53b192a3f070793c45819fcd3e0ec3552a94155fabb4b3538dde4688285f7`.

```json
{
  "id": "N986marker",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Reaction Fire marker",
    "evidence_ids": [
      "E986marker"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E986marker"
  ],
  "review_status": "unreviewed"
}
```

**context-01 — osobna propozycja i ślady**

context-01 N911counter, `/nodes/31`, bajty [196499,197607), SHA-256 `7b6b333e688ac23f557a2c1e1344876b6770501901c9407247d341dac0c97653`.

```json
{
  "id": "N911counter",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Africa",
    "evidence_ids": [
      "E911counter"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E911counter"
  ],
  "review_status": "unreviewed",
  "source_locator": "Illustrative counter — Africa / EL"
}
```

context-01 N921counter, `/nodes/32`, bajty [197614,198706), SHA-256 `0c1388f9709c55e4e5a45fc7686880da9f5078247249284e32ca56de85771f8b`.

```json
{
  "id": "N921counter",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Bal'ric",
    "evidence_ids": [
      "E921counter"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E921counter"
  ],
  "review_status": "unreviewed",
  "source_locator": "Illustrative counter — Bal’ric / SK"
}
```

context-01 N966diagram, `/nodes/7`, bajty [177283,178673), SHA-256 `36e8f4cd62347156e4d08983cd3b50a484a73b8478deddb5b4167d954c4d364d`.

```json
{
  "id": "N966diagram",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Original Deployment / After Manipular Line Extension",
    "evidence_ids": [
      "E966diagram"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E966diagram"
  ],
  "review_status": "unreviewed"
}
```

context-01 N981counter, `/nodes/33`, bajty [198713,199783), SHA-256 `a40fc3ffd54bad133ba38846aeb3aab44303b5e8c073a04740d3cbc39f922451`.

```json
{
  "id": "N981counter",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Scorpio",
    "evidence_ids": [
      "E981counter"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E981counter"
  ],
  "review_status": "unreviewed",
  "source_locator": "Illustrative counter — Scorpio / LI"
}
```

context-01 N985markers, `/nodes/34`, bajty [199790,200614), SHA-256 `dbe361bd9cf8804ab74f36fb87df19676d1bb274181a69cbb81096f69bd1c781`.

```json
{
  "id": "N985markers",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Active Fire markers",
    "evidence_ids": [
      "E985markers"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E985markers"
  ],
  "review_status": "unreviewed"
}
```

context-01 N986marker, `/nodes/35`, bajty [200621,201375), SHA-256 `78dde9f9c9f3eb96ff736ce3906574f912063c631e83bc02f67c83e028508c80`.

```json
{
  "id": "N986marker",
  "kind": "diagram",
  "original_label": {
    "state": "known",
    "value": "Reaction Fire marker",
    "evidence_ids": [
      "E986marker"
    ],
    "reason": null,
    "gap_ids": []
  },
  "scope_role": "core",
  "content": {
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
  },
  "evidence_ids": [
    "E986marker"
  ],
  "review_status": "unreviewed"
}
```

Niepewności i wyłączenia: Actual identified counter TQ/MA and glyph values remain unconfirmed; criticality is conditional on changing outcome or legality.; Wybrany żeton/parametr z dokładnym źródłem i przeglądem, tylko jeśli sytuacja go potrzebuje.; any parent proposition clause not reproduced in reviewed_assertions; unshown relation metadata, aliases and external target identities; full external procedures and real-state parameters unless explicitly listed

## Kwestie wymagające osobnej decyzji

SEM-011 / EXP-052: oba lokalne ograniczenia występują osobno. Czy ich zapis wystarcza dla koniunkcji reviewed_scope, czy brakuje jawnego powiązania? Brak pary DEP-NEW-001 zachowany; relację ocenia .4b.

SEM-012 / EXP-066: instrukcja ignore zachowana i potrzeba actual Combat Tables zadeklarowana, lecz blocking=false. Ocena dotyczy konkretnego identyfikowania wpisów; sam lokalny zakaz nie wymaga wykonania tabeli.

SEM-013 / EXP-074: illustrative/no general ratings zachowane; brak osobnego actual-value gap/conditional blocking. Nie zgadywać konkretnych TQ/MA ani przypisania ratingów do pól.

Wcześniejsze SEM-001–010 i EXP-010/017/019/040/050 pozostają pending. Brakujące krytyczne pary, E916, 64 granice glifów, pełny graf i reszta inwentarza nie zostały rozstrzygnięte. 175 przyjętych wcześniej par rubryka/EXP bez zmiany, nowe nie dają dodatkowych punktów.

1 dodatkowa strona/1 reguła/0 tabel, 1 runda kontekstu, 0 korekt, 0 pełnych domknięć, 4 częściowe uzupełnienia i 4 nowe deklaracje. Trzecie źródło niepozyskane, stop ekspansji na granicy 2. Pełne metryki i TP/FP/FN not_assessable; aktywny czas/budżet/config/tokeny/cena unknown. Listing/path discovery poza allowlistą potwierdzony; odczyt treści oceny niezaobserwowany, ekspozycja/czysty kontekst unknown.

Następna praca: decyzje właściciela dla tego pakietu i wcześniejszych pending; następnie osobna .4b, później .4c/.4d, z dalszym podziałem przed wykonaniem jeśli potrzebny. M-POC5A i .4 partial, M-POC5 jedyny next.
