# M-POC5B — pełna ocena20 sytuacji w obu odpowiedziach

Wykonano40 porównań. To ręczna ocena użyteczności oryginalnego zapisu reguł przy zamrożonych faktach. Wyprowadzenia i obliczenia należą do oceniającego; nie są nowymi odpowiedziami modelu na sytuacje. Wszystkie nowe oceny waiting_review.

| Kategoria propozycji | first-001 | context-01 |
|---|---:|---:|
| Zgodny lokalny wynik |15|14|
| Właściwa oczekiwana blokada |3|3|
| Kandydat nieuzasadnionej blokady |1|1|
| Pełny wynik nieocenialny po porównaniu |1|2|

Mianownik20 w każdym wyniku; poprawne blokady nie są meaningful local results dla progu80%. Pełna jakość i metryki relacji nadal nieocenialne. Źródła,pola,hashe,bajty i użyte zależności: [results.json](results.json).

## SIT-01 — Pass-Thru: legalna opcja i lokalne liczby

### Zamrożone fakty i pytanie

```json
{
  "defender": "jedna LI, Front attack",
  "attacker": "jedna EL SHOCK MUST CHECK TQ bez współatakujących",
  "initial_enemy_ZOC": false,
  "free_rear": 1,
  "decision_before_PreShock_DR": true,
  "base_Shock_Hits": {
    "defender": 5,
    "elephant": 3
  },
  "infantry_routed": false,
  "elephant_rampaged": false
}
```

Czy można wybrać opcję? Podaj lokalny DRM, Hits i końcowe placement, bez obliczania całego Shock.

**Expected z eval-v1:** Opcja spełnia lokalne warunki; Pre-Shock piechoty +1 DRM, Hits5→2 i EL3→2. Po podanych stanach EL do wolnego Rear wybranego przez gracza EL, facing bez zmiany; końcowy test LI jest osobnym krokiem.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF31/right, `/situations/0/evidence/0`, obraz SHA `39f86ad053725088e9c571f43d1e8ecc4dbf21f5b191cc1e7d99cc854ddc34ba`.

> 9.11 Elephant Pass-Thru: An infantry unit being
> attacked through one of its Front hexes by an Ele-
> phant unit marked SHOCK MUST CHECK TQ, may
> attempt to allow the Elephant unit to pass through its
> hex. This decision must be made prior to the Pre-Shock TQ Check
> die roll (8.43) and may be elected only if at least one of the de-
> fender’s Rear hexes is unoccupied. Pass-Thru is not allowed if:

Źródło PDF31/right, `/situations/0/evidence/1`, obraz SHA `39f86ad053725088e9c571f43d1e8ecc4dbf21f5b191cc1e7d99cc854ddc34ba`.

> 1. Apply a +1 DRM to the infantry unit’s Pre-Shock TQ Check
> DR.

Źródło PDF31/right, `/situations/0/evidence/2`, obraz SHA `39f86ad053725088e9c571f43d1e8ecc4dbf21f5b191cc1e7d99cc854ddc34ba`.

> 2. Proceed with the Shock resolution procedure but halve (round
> down) Cohesion Hits to the defending unit and reduce the
> Cohesion Hits to the Elephant unit by 1.

Źródło PDF32/left, `/situations/0/evidence/3`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> 3. After the Shock Combat is resolved, if the infantry unit did
> not rout and the Elephant unit has not rampaged (9.14), place
> the Elephant unit in either one of the defender’s unoccupied
> Rear hexes (Elephant player’s choice), maintaining its facing.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "PassThru_local_gate": true,
  "defender_PreShock_DRM": 1,
  "defender_Hits": 2,
  "elephant_Hits": 2,
  "placement": "free defender Rear chosen by EL player; facing unchanged",
  "final_LI_check": "separate step"
}
```

1. R911 conditions+exceptions: LI/Front/EL marker/freeRear/beforeDR supplied, no co-attacker or initial ZOC → local option allowed.
2. R911 effect+parameters: floor(5/2)=2 defender Hits; 3−1=2 Elephant Hits; +1 DRM to defender Pre-Shock.
3. Given no infantryRout/noELRampage → R911 step3 placement at unoccupied Rear, EL player choice, facing unchanged; step4 remains separate.

**Porównanie:** All requested local gate,signs,numbers,choice and timing match frozen expected in both representations.

**Zależności i blokada:** Full8.43/Shock/CRT/ZOC procedures are not executed: baseHits/geometry/states are supplied. D911914 links the supplied noRampage gate; no real Rout inferred.

**Wyłączenia:** CompleteShock and actual die outcomes, realZOC/routes, finalLI check value and base0/other modifier ordering.

`/rules/0/transcription`, bajty[172872,173416); SHA `82b19294d61f9cb90e2a7b5778552dd59171a455c14013844cdac975c5eb59d1`.

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

`/rules/0/interpretation`, bajty[173442,174238); SHA `4e1f8e28e6c867f3bd0e68fbf4e49378dc1216b7dd5a30a0226835828519b48c`.

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

`/rules/0/conditions`, bajty[174260,174689); SHA `8a25a5117e361c1668de9deca1ff456e456ced4de02f1a4889a783d63b965018`.

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

`/rules/0/action_effect`, bajty[174714,175431); SHA `cfb83b4eedbb8c78972bf6546630ec9947d966a8c23987d6a3a3926d72bff3e9`.

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

`/rules/0/exceptions`, bajty[175453,175897); SHA `8108a96277b41b9c9d2b2450a045c2a1b6f009f44842b1b8aade961f691721bb`.

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

`/rules/0/parameters`, bajty[175919,178901); SHA `ed27a08a323d48862ad773fd7f48ae1cd85648d5f7c4f0bf7dec4124e7b13fc1`.

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

`/rules/0/time_limits`, bajty[179437,179784); SHA `7e782b393f9f03eb141023dc840ea969ed66c78ea41a4ce0498bcf11c30645c8`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "PassThru_local_gate": true,
  "defender_PreShock_DRM": 1,
  "defender_Hits": 2,
  "elephant_Hits": 2,
  "placement": "free defender Rear chosen by EL player; facing unchanged",
  "final_LI_check": "separate step"
}
```

1. R911 conditions+exceptions: LI/Front/EL marker/freeRear/beforeDR supplied, no co-attacker or initial ZOC → local option allowed.
2. R911 effect+parameters: floor(5/2)=2 defender Hits; 3−1=2 Elephant Hits; +1 DRM to defender Pre-Shock.
3. Given no infantryRout/noELRampage → R911 step3 placement at unoccupied Rear, EL player choice, facing unchanged; step4 remains separate.

**Porównanie:** All requested local gate,signs,numbers,choice and timing match frozen expected in both representations.

**Zależności i blokada:** Full8.43/Shock/CRT/ZOC procedures are not executed: baseHits/geometry/states are supplied. D911914 links the supplied noRampage gate; no real Rout inferred.

**Wyłączenia:** CompleteShock and actual die outcomes, realZOC/routes, finalLI check value and base0/other modifier ordering.

`/rules/0/transcription`, bajty[238753,239309); SHA `0bf73911af1ca24e7817082a3f3d81939ee823c22cb865fed8407838fc22ebe4`.

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

`/rules/0/interpretation`, bajty[239336,240147); SHA `7424da32e7fbcdd8e85f3026992274982684fda55e9bb6bbbbaf1b633be3e9b0`.

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

`/rules/0/conditions`, bajty[240170,240612); SHA `b0f2ca3fcbfd97a5e11e3433cbfc9831f94af2b3e9ec4e94b302862b390e83a0`.

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

`/rules/0/action_effect`, bajty[240638,241370); SHA `734e59d5073d6f749b088707235df4222786820442db349658397fb04518d169`.

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

`/rules/0/exceptions`, bajty[241393,241850); SHA `2e11fd44395901745544f3d39c05e70f6e03d80430d93036a0a318990ee2710a`.

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

`/rules/0/parameters`, bajty[241873,244973); SHA `f728d4884006752314b372740322be8b85051e15db358a9598ab280600541f59`.

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

`/rules/0/time_limits`, bajty[245536,245896); SHA `397436037b0b81b450fd1d6c8e911d840ef2e1f311859fbbfd2d04619616b98a`.

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

## SIT-02 — Pass-Thru: ZOC na początku phase

### Zamrożone fakty i pytanie

```json
{
  "other_PassThru_conditions": true,
  "in_enemy_ZOC_at_phase_start": true,
  "in_enemy_ZOC_now": false
}
```

Czy wyjście z ZOC w trakcie phase pozwala teraz wybrać Pass-Thru?

**Expected z eval-v1:** Nie. Pass-Thru wykluczony przez ZOC na początku Orders Phase; późniejszy stan nie usuwa zakazu.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF31/right, `/situations/1/evidence/0`, obraz SHA `39f86ad053725088e9c571f43d1e8ecc4dbf21f5b191cc1e7d99cc854ddc34ba`.

> 9.11 Elephant Pass-Thru: An infantry unit being
> attacked through one of its Front hexes by an Ele-
> phant unit marked SHOCK MUST CHECK TQ, may
> attempt to allow the Elephant unit to pass through its
> hex. This decision must be made prior to the Pre-Shock TQ Check
> die roll (8.43) and may be elected only if at least one of the de-
> fender’s Rear hexes is unoccupied. Pass-Thru is not allowed if:

Źródło PDF31/right, `/situations/1/evidence/1`, obraz SHA `39f86ad053725088e9c571f43d1e8ecc4dbf21f5b191cc1e7d99cc854ddc34ba`.

> • the infantry unit was in an enemy ZOC at the start of the Orders
> Phase.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "PassThru_local_gate": false,
  "reason": "initial enemy ZOC excludes option despite now outside ZOC"
}
```

1. R911 exceptions checks ZOC at OrdersPhase start. The supplied start flag is true.
2. Current ZOC=false cannot erase the start-condition prohibition; no Shock result computed.

**Porównanie:** Matches the frozen start-of-phase boundary, not a now-only test.

**Zależności i blokada:** The ZOC geometry is supplied; no general definition lookup is needed to apply the stated temporal predicate.

**Wyłączenia:** Actual mapZOC calculation and ordinaryShock after refusing the option.

`/rules/0/transcription`, bajty[172872,173416); SHA `82b19294d61f9cb90e2a7b5778552dd59171a455c14013844cdac975c5eb59d1`.

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

`/rules/0/interpretation`, bajty[173442,174238); SHA `4e1f8e28e6c867f3bd0e68fbf4e49378dc1216b7dd5a30a0226835828519b48c`.

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

`/rules/0/conditions`, bajty[174260,174689); SHA `8a25a5117e361c1668de9deca1ff456e456ced4de02f1a4889a783d63b965018`.

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

`/rules/0/action_effect`, bajty[174714,175431); SHA `cfb83b4eedbb8c78972bf6546630ec9947d966a8c23987d6a3a3926d72bff3e9`.

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

`/rules/0/exceptions`, bajty[175453,175897); SHA `8108a96277b41b9c9d2b2450a045c2a1b6f009f44842b1b8aade961f691721bb`.

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

`/rules/0/parameters`, bajty[175919,178901); SHA `ed27a08a323d48862ad773fd7f48ae1cd85648d5f7c4f0bf7dec4124e7b13fc1`.

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

`/rules/0/time_limits`, bajty[179437,179784); SHA `7e782b393f9f03eb141023dc840ea969ed66c78ea41a4ce0498bcf11c30645c8`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "PassThru_local_gate": false,
  "reason": "initial enemy ZOC excludes option despite now outside ZOC"
}
```

1. R911 exceptions checks ZOC at OrdersPhase start. The supplied start flag is true.
2. Current ZOC=false cannot erase the start-condition prohibition; no Shock result computed.

**Porównanie:** Matches the frozen start-of-phase boundary, not a now-only test.

**Zależności i blokada:** The ZOC geometry is supplied; no general definition lookup is needed to apply the stated temporal predicate.

**Wyłączenia:** Actual mapZOC calculation and ordinaryShock after refusing the option.

`/rules/0/transcription`, bajty[238753,239309); SHA `0bf73911af1ca24e7817082a3f3d81939ee823c22cb865fed8407838fc22ebe4`.

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

`/rules/0/interpretation`, bajty[239336,240147); SHA `7424da32e7fbcdd8e85f3026992274982684fda55e9bb6bbbbaf1b633be3e9b0`.

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

`/rules/0/conditions`, bajty[240170,240612); SHA `b0f2ca3fcbfd97a5e11e3433cbfc9831f94af2b3e9ec4e94b302862b390e83a0`.

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

`/rules/0/action_effect`, bajty[240638,241370); SHA `734e59d5073d6f749b088707235df4222786820442db349658397fb04518d169`.

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

`/rules/0/exceptions`, bajty[241393,241850); SHA `2e11fd44395901745544f3d39c05e70f6e03d80430d93036a0a318990ee2710a`.

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

`/rules/0/parameters`, bajty[241873,244973); SHA `f728d4884006752314b372740322be8b85051e15db358a9598ab280600541f59`.

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

`/rules/0/time_limits`, bajty[245536,245896); SHA `397436037b0b81b450fd1d6c8e911d840ef2e1f311859fbbfd2d04619616b98a`.

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

## SIT-03 — SK po Pass-Thru a Pre-Shock

### Zamrożone fakty i pytanie

```json
{
  "defender": "wyłącznie SK",
  "all_PassThru_conditions": true,
  "PassThru_elected": true
}
```

Czy końcowy Pass-Thru test jest wymagany i czy ten wyjątek usuwa każdy Pre-Shock test?

**Expected z eval-v1:** SK nie robi końcowego Pass-Thru TQ Check. Nie wolno z tego wywieść zwolnienia każdego testu:9.23 zwalnia attackerów atakujących SK alone,9.11 mówi o +1 do Pre-Shock obrońcy.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF31/right, `/situations/2/evidence/0`, obraz SHA `39f86ad053725088e9c571f43d1e8ecc4dbf21f5b191cc1e7d99cc854ddc34ba`.

> 1. Apply a +1 DRM to the infantry unit’s Pre-Shock TQ Check
> DR.

Źródło PDF32/left, `/situations/2/evidence/1`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> 4. The defending unit, other than a Skirmisher unit, now un-
> dergoes a Pass-Thru TQ Check. Subtract the unit’s TQ from
> the DR, with any excess being the number of Cohesion Hits
> now applied (DR–TQ=Hits).

Źródło PDF33/right, `/situations/2/evidence/2`, obraz SHA `3ba367da1aee5635f964b887ff518ec63ba48175278e3fefdb031a8e03a7d15d`.

> • Skirmishers do not make an Elephant Pass-Thru Check (9.11).

Źródło PDF33/right, `/situations/2/evidence/3`, obraz SHA `3ba367da1aee5635f964b887ff518ec63ba48175278e3fefdb031a8e03a7d15d`.

> • All units that Shock attack Skirmishers alone do not have
> to make a Pre-Shock TQ even if they have SHOCK MUST
> CHECK TQ markers.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "final_PassThru_TQ_for_SK": false,
  "blanket_PreShock_exemption": false,
  "attacker_of_SK_alone_PreShock": "exempt byR923",
  "defender_PreShock": "R911 local+1; outcome outside scope"
}
```

1. R911 step4 explicitly excludes Skirmisher; R923 exempts attackers of SK alone from their PreShock check.
2. R911 +1 is a defender PreShock modification, a different step/recipient. It cannot be erased by the final-check exception.
3. No complete defenderPreShock outcome is inferred without the base procedure.

**Porównanie:** All required distinctions match frozen expected; not every TQ check is waived.

**Zależności i blokada:** DEP-008 exception correspondence and PreShock reference distinguish finalcheck from basePreShock; no test-value execution required.

**Wyłączenia:** Base8.43 eligibility/results and real combat legality beyond supplied conditions.

`/rules/0/transcription`, bajty[172872,173416); SHA `82b19294d61f9cb90e2a7b5778552dd59171a455c14013844cdac975c5eb59d1`.

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

`/rules/0/interpretation`, bajty[173442,174238); SHA `4e1f8e28e6c867f3bd0e68fbf4e49378dc1216b7dd5a30a0226835828519b48c`.

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

`/rules/0/conditions`, bajty[174260,174689); SHA `8a25a5117e361c1668de9deca1ff456e456ced4de02f1a4889a783d63b965018`.

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

`/rules/0/action_effect`, bajty[174714,175431); SHA `cfb83b4eedbb8c78972bf6546630ec9947d966a8c23987d6a3a3926d72bff3e9`.

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

`/rules/0/exceptions`, bajty[175453,175897); SHA `8108a96277b41b9c9d2b2450a045c2a1b6f009f44842b1b8aade961f691721bb`.

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

`/rules/0/parameters`, bajty[175919,178901); SHA `ed27a08a323d48862ad773fd7f48ae1cd85648d5f7c4f0bf7dec4124e7b13fc1`.

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

`/rules/0/time_limits`, bajty[179437,179784); SHA `7e782b393f9f03eb141023dc840ea969ed66c78ea41a4ce0498bcf11c30645c8`.

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

`/rules/13/transcription`, bajty[245169,245582); SHA `c729fd1b6fb29a25fc050a801ec65a7db07e0ecea19ef684aedbda9b198ed270`.

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

`/rules/13/interpretation`, bajty[245608,246393); SHA `3d4d0e9bbc4b49db005d7d797ec431f2da0d09a03a020c2206b7b9131bc2e683`.

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

`/rules/13/conditions`, bajty[246415,246637); SHA `9860237474fe072827d805ccb1051bb6e9be1870ff8d7c18e47dc7b9c7cc3f17`.

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

`/rules/13/action_effect`, bajty[246662,247368); SHA `09863157927710eb00ef00e07ed72f8c5f3f373f4312b6c94fe570f3216b5f09`.

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

`/rules/13/exceptions`, bajty[247390,247671); SHA `eab97edd08efff26928013c89002a355b31aa825124e4b4440cbd8e0523a9077`.

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

`/rules/13/parameters`, bajty[247693,248781); SHA `4c304688d97300a7e65922d51a646e5a30ba77532052109c2ec159fa8af7a4e1`.

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

`/rules/13/time_limits`, bajty[249359,249598); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "final_PassThru_TQ_for_SK": false,
  "blanket_PreShock_exemption": false,
  "attacker_of_SK_alone_PreShock": "exempt byR923",
  "defender_PreShock": "R911 local+1; outcome outside scope"
}
```

1. R911 step4 explicitly excludes Skirmisher; R923 exempts attackers of SK alone from their PreShock check.
2. R911 +1 is a defender PreShock modification, a different step/recipient. It cannot be erased by the final-check exception.
3. No complete defenderPreShock outcome is inferred without the base procedure.

**Porównanie:** All required distinctions match frozen expected; not every TQ check is waived.

**Zależności i blokada:** DEP-008 exception correspondence and PreShock reference distinguish finalcheck from basePreShock; no test-value execution required.

**Wyłączenia:** Base8.43 eligibility/results and real combat legality beyond supplied conditions.

`/rules/0/transcription`, bajty[238753,239309); SHA `0bf73911af1ca24e7817082a3f3d81939ee823c22cb865fed8407838fc22ebe4`.

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

`/rules/0/interpretation`, bajty[239336,240147); SHA `7424da32e7fbcdd8e85f3026992274982684fda55e9bb6bbbbaf1b633be3e9b0`.

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

`/rules/0/conditions`, bajty[240170,240612); SHA `b0f2ca3fcbfd97a5e11e3433cbfc9831f94af2b3e9ec4e94b302862b390e83a0`.

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

`/rules/0/action_effect`, bajty[240638,241370); SHA `734e59d5073d6f749b088707235df4222786820442db349658397fb04518d169`.

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

`/rules/0/exceptions`, bajty[241393,241850); SHA `2e11fd44395901745544f3d39c05e70f6e03d80430d93036a0a318990ee2710a`.

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

`/rules/0/parameters`, bajty[241873,244973); SHA `f728d4884006752314b372740322be8b85051e15db358a9598ab280600541f59`.

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

`/rules/0/time_limits`, bajty[245536,245896); SHA `397436037b0b81b450fd1d6c8e911d840ef2e1f311859fbbfd2d04619616b98a`.

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

`/rules/13/transcription`, bajty[313577,314000); SHA `e5f1e9a5d2885bb7c6462a277c3fc5acef03fbd5aa05a369eceac75c9f6be3df`.

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

`/rules/13/interpretation`, bajty[314027,314827); SHA `2d8208efcc82ee9ca20f6321a7af8ba89d948ee6652f4ab0c77d958f38f0a754`.

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

`/rules/13/conditions`, bajty[314850,315082); SHA `4b0cf8384ed089ca6185d240b5d9d346c554cb798d65bb544931aec76c56cadc`.

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

`/rules/13/action_effect`, bajty[315108,315829); SHA `2ae1f4f582aba92c4a76cd3fa1b6124778a38380b517524b407b9aba5fb32cf5`.

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

`/rules/13/exceptions`, bajty[315852,316144); SHA `26c0e908fd486c9ee9bf3baee7acd2c2494f75823e50d106d52cb88208e8a283`.

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

`/rules/13/parameters`, bajty[316167,317296); SHA `0487b396d50818d2372a3ba39443718d456efa6f3039e1cd805528e8873a6872`.

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

`/rules/13/time_limits`, bajty[317901,318146); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

## SIT-04 — Zwykły EL: pierwszy i kolejny7–9

### Zamrożone fakty i pytanie

```json
{
  "unit": "ordinary EL",
  "DR": 8,
  "first_roll_geometry": "kierunek bezpośrednio od przyczyny jest jednoznaczny i wolny",
  "early_termination": false
}
```

Porównaj pierwszy8 z kolejnym8 przy podanych warunkach.

**Expected z eval-v1:** Ordinary EL: first DR8 moves away from cause and attempts 3 hexes under supplied route/no early termination; subsequent DR8 eliminates. First Leader 7-9 is outside this situation.

**Zakres:** Only the approved first/subsequent ordinary Elephant local distinction.

Źródło PDF32/right, `/situations/3/evidence/0`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

Źródło PDF32/right, `/situations/3/evidence/1`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> A rampaging Elephant and any stacked leader with it always
> attempt to move 3 hexes per directional die roll in the indicated
> direction until it either moves off the map or is otherwise elimi-
> nated. If a rampaging Elephant unit would enter a hex occupied
> by a unit, whether enemy or friendly, the Elephant unit stops in
> the adjacent hex and the unit incurs 1 Cohesion Hit if the Elephant
> would have entered through a Front hex or 2 Cohesion Hits if it
> would have entered through a Flank or Rear hex. A cavalry unit
> incurs 2 Cohesion Hits regardless of the angle.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "ordinary_first_DR8": "away from supplied cause; attempt3hexes",
  "ordinary_subsequent_DR8": "eliminated"
}
```

1. N914table row7–9 distinguishes first versus subsequent. Unit is ordinary EL; route/cause and no early termination are supplied.
2. R914 movement parameter=3 per directional roll; first8 attempts3 on given free route.
3. Subsequent8 takes ordinary elimination branch, not Leader rally.

**Porównanie:** Both ordinary branches match frozen expected; firstLeader case excluded.

**Zależności i blokada:** Missing separate DEP-NEW-002 remains structural. The requested ordinary distinction is present in table/body prose; no automatic case failure or semanticFN from absent record.

**Wyłączenia:** Leader first7–9/counting4.84trigger, actualmap/routes and additional Rampage sequence outcomes.

`/rules/4/transcription`, bajty[194129,195571); SHA `d2981c8bf1c1384abc5a59f3e62a9a9f8cdc1b27afadfbc464fa4c3934b259cd`.

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

`/rules/4/interpretation`, bajty[195597,197162); SHA `0799ec2f91c5f6d3365448e670c27bc1eca5f940181e68ac62cc6380f7e5031a`.

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

`/rules/4/conditions`, bajty[197184,197599); SHA `e30b43577cd81c3b2294aa5944cba5249db6e7f4c98cdafa8f0357b92a30ffee`.

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

`/rules/4/action_effect`, bajty[197624,199110); SHA `1ae2b20a1e94ce83f1df3575503a5c435df960957d2be2d8b645e28b0a678362`.

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

`/rules/4/exceptions`, bajty[199132,199829); SHA `0e5fb1f0776f8e9941958d97488e77f03dc853600b048dacd32610b9b3c69aea`.

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

`/rules/4/parameters`, bajty[199851,208182); SHA `65837d258e1021d757f276f08d4df7bd7522273f54207f6406ad1be1d3265dd9`.

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

`/rules/4/time_limits`, bajty[209126,209635); SHA `8c1ccb24242b4afd17251bd161d225a23d2097e50185f46274e363693460cc54`.

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

`/nodes/0/content`, bajty[120357,121983); SHA `7daa88309d039309d8273981fcfc3eb3f6166f2f15a4b99ca7070c9fabd43650`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "ordinary_first_DR8": "away from supplied cause; attempt3hexes",
  "ordinary_subsequent_DR8": "eliminated"
}
```

1. N914table row7–9 distinguishes first versus subsequent. Unit is ordinary EL; route/cause and no early termination are supplied.
2. R914 movement parameter=3 per directional roll; first8 attempts3 on given free route.
3. Subsequent8 takes ordinary elimination branch, not Leader rally.

**Porównanie:** Both ordinary branches match frozen expected; firstLeader case excluded.

**Zależności i blokada:** Missing separate DEP-NEW-002 remains structural. The requested ordinary distinction is present in table/body prose; no automatic case failure or semanticFN from absent record.

**Wyłączenia:** Leader first7–9/counting4.84trigger, actualmap/routes and additional Rampage sequence outcomes.

`/rules/4/transcription`, bajty[260754,262222); SHA `c8e9684ef68cac9c91cd8486f8ab98ea3af3779a683f2d75e81f135ef34fa198`.

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

`/rules/4/interpretation`, bajty[262249,263839); SHA `9b23c5ac4e5c25f8ca2125f7b62caadad64540c3e465f674941e8d7ec996d2cd`.

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

`/rules/4/conditions`, bajty[263862,264295); SHA `489614f9febaa05f510e7e79d36ae32f847ed85460b553d36d65ae054e235d53`.

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

`/rules/4/action_effect`, bajty[264321,265832); SHA `7dbba69656bab00b666311ba7a133c42c56d00be0bfde854d909cd320d61b314`.

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

`/rules/4/exceptions`, bajty[265855,266573); SHA `dad275d952bcf675639f6aaa6b3dd8e571d433e242bea6eb4ecd0db80ca39d1b`.

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

`/rules/4/parameters`, bajty[266596,275236); SHA `c2e78c7f6f892172a922bde0949cd6a272b8a36d4c906b694dc294dda4bd2aa3`.

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

`/rules/4/time_limits`, bajty[276223,276752); SHA `0a407790c2ae2542c0c055858fac2971c3cdf0dcb45bf579615cf1042d343bfe`.

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

`/nodes/0/content`, bajty[167936,169593); SHA `a4baee8cdd6d3ed083a560ad77e366c096f546bbd14c747adb67246c29477e9f`.

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

## SIT-05 — Leader Elephant: późniejsze7–9 wobec no rally

### Zamrożone fakty i pytanie

```json
{
  "unit": "Leader Elephant bez stacked leadera",
  "TQ": 6,
  "roll_number": 2,
  "DR": 8
}
```

Czy ogólny zakaz rally w Rampage wymusza eliminację?

**Expected z eval-v1:** immediate rally with4CH at syntheticTQ6 and secondRampageDR8; not elimination

**Zakres:** Only the approved local supplied facts; not a complete game-state resolution.

Źródło PDF32/right, `/situations/4/evidence/0`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> 7–9 On the first Rampage DR, the Elephant heads
> in the direction directly away from the unit that
> caused the rampage. A 7-9 on any subsequent
> die roll means the elephant’s mahout has been
> successful in stopping the rampage by driving a
> wedge into the beast’s brain; the Elephant unit is
> eliminated. If it is a Leader Elephant, the unit is,
> instead, immediately rallied with Cohesion Hits
> equal to its TQ minus 2.

Źródło PDF32/right, `/situations/4/evidence/1`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> Rampaging elephants have no ZOC, do not trigger Reaction
> Fire of any kind, and they may not be rallied. Each Rampage is

Źródło PDF33/left, `/situations/4/evidence/2`, obraz SHA `3ba367da1aee5635f964b887ff518ec63ba48175278e3fefdb031a8e03a7d15d`.

> undertaken until its conclusion, so there may never be more than
> one rampaging Elephant unit at any one time.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "subsequent_Leader_DR8": "immediate rally",
  "Cohesion_Hits": 4,
  "eliminated": false
}
```

1. Synthetic roll_number2 selects subsequent7–9 in N914table.
2. R914 exceptions explicitly says Leader subsequent7–9 rallies atTQ−2 and overrides general noRally.
3. SuppliedTQ6 → 6−2=4 CH; no stackedLeader casualty requested.

**Porównanie:** The explicit exception wins over general noRally; matches frozen local result in both.

**Zależności i blokada:** DEP-NEW-002 missing as separate record is preserved; R914 exceptions plus N914table provide the local exception in prose. TQ is supplied, not read from a real counter.

**Wyłączenia:** Actual LeaderElephantTQ/identity, firstLeaderDR and all casualty/generalRally procedures.

`/rules/4/transcription`, bajty[194129,195571); SHA `d2981c8bf1c1384abc5a59f3e62a9a9f8cdc1b27afadfbc464fa4c3934b259cd`.

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

`/rules/4/interpretation`, bajty[195597,197162); SHA `0799ec2f91c5f6d3365448e670c27bc1eca5f940181e68ac62cc6380f7e5031a`.

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

`/rules/4/conditions`, bajty[197184,197599); SHA `e30b43577cd81c3b2294aa5944cba5249db6e7f4c98cdafa8f0357b92a30ffee`.

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

`/rules/4/action_effect`, bajty[197624,199110); SHA `1ae2b20a1e94ce83f1df3575503a5c435df960957d2be2d8b645e28b0a678362`.

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

`/rules/4/exceptions`, bajty[199132,199829); SHA `0e5fb1f0776f8e9941958d97488e77f03dc853600b048dacd32610b9b3c69aea`.

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

`/rules/4/parameters`, bajty[199851,208182); SHA `65837d258e1021d757f276f08d4df7bd7522273f54207f6406ad1be1d3265dd9`.

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

`/rules/4/time_limits`, bajty[209126,209635); SHA `8c1ccb24242b4afd17251bd161d225a23d2097e50185f46274e363693460cc54`.

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

`/nodes/0/content`, bajty[120357,121983); SHA `7daa88309d039309d8273981fcfc3eb3f6166f2f15a4b99ca7070c9fabd43650`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "subsequent_Leader_DR8": "immediate rally",
  "Cohesion_Hits": 4,
  "eliminated": false
}
```

1. Synthetic roll_number2 selects subsequent7–9 in N914table.
2. R914 exceptions explicitly says Leader subsequent7–9 rallies atTQ−2 and overrides general noRally.
3. SuppliedTQ6 → 6−2=4 CH; no stackedLeader casualty requested.

**Porównanie:** The explicit exception wins over general noRally; matches frozen local result in both.

**Zależności i blokada:** DEP-NEW-002 missing as separate record is preserved; R914 exceptions plus N914table provide the local exception in prose. TQ is supplied, not read from a real counter.

**Wyłączenia:** Actual LeaderElephantTQ/identity, firstLeaderDR and all casualty/generalRally procedures.

`/rules/4/transcription`, bajty[260754,262222); SHA `c8e9684ef68cac9c91cd8486f8ab98ea3af3779a683f2d75e81f135ef34fa198`.

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

`/rules/4/interpretation`, bajty[262249,263839); SHA `9b23c5ac4e5c25f8ca2125f7b62caadad64540c3e465f674941e8d7ec996d2cd`.

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

`/rules/4/conditions`, bajty[263862,264295); SHA `489614f9febaa05f510e7e79d36ae32f847ed85460b553d36d65ae054e235d53`.

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

`/rules/4/action_effect`, bajty[264321,265832); SHA `7dbba69656bab00b666311ba7a133c42c56d00be0bfde854d909cd320d61b314`.

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

`/rules/4/exceptions`, bajty[265855,266573); SHA `dad275d952bcf675639f6aaa6b3dd8e571d433e242bea6eb4ecd0db80ca39d1b`.

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

`/rules/4/parameters`, bajty[266596,275236); SHA `c2e78c7f6f892172a922bde0949cd6a272b8a36d4c906b694dc294dda4bd2aa3`.

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

`/rules/4/time_limits`, bajty[276223,276752); SHA `0a407790c2ae2542c0c055858fac2971c3cdf0dcb45bf579615cf1042d343bfe`.

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

`/nodes/0/content`, bajty[167936,169593); SHA `a4baee8cdd6d3ed083a560ad77e366c096f546bbd14c747adb67246c29477e9f`.

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

## SIT-06 — Rampage: brak kompasu mapy

### Zamrożone fakty i pytanie

```json
{
  "unit": "EL",
  "DR": 1,
  "battle_map": "unknown",
  "available_diagram": "D-01 example"
}
```

Podaj konkretny hexside/kierunek na mapie.

**Expected z eval-v1:** Specificmapdirection/hexside cannotchosenwithoutactualcompass;examplenotuniversal orientation

**Zakres:** Concrete map direction remains blocked; the example is not a universal compass.

Źródło PDF32/left, `/situations/5/evidence/0`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> 1–6 The Elephant unit heads in the direction indicated
> on the Compass on the map, an example of which
> is given below. Note that geographical direction
> is represented at the vertex; the direction in which
> the Elephant is to Rampage is by hexside.

Źródło PDF32/right, `/situations/5/evidence/1`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

Źródło PDF32/right, `/situations/5/evidence/2`, obraz SHA `fe980a86fe41c88c191f49842d896385f9c855ee7534581d446f97ff3f3e9fa3`.

> EXAMPLE: The above diagram shows the elephant unit refaced
> after a Rampage die roll of 1. This is just an example; use the
> compass on the map for each battle.

### first-001 — justified_block / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "concrete_map_hexside": null,
  "block": "missing actual battle-map compass",
  "known_local_fact": "diagram is illustrative only"
}
```

1. N914table1–6 uses compass on map; N914diagram interpretation explicitly excludes universal geographical direction.
2. D914compass unresolved and G-D914compass blocking=true; actual battle_map missing in the case.
3. Example roll1 upper-right cannot establish a concrete battle-map hexside.

**Porównanie:** Matches the expected justified block; no invented compass.

**Zależności i blokada:** Actual map compass is essential here, unlike SIT-04 supplied route. Source diagram is not the missing real target.

**Wyłączenia:** Chosen geographic direction/hex, actualcounter rating and complete movement.

`/nodes/0/content`, bajty[120357,121983); SHA `7daa88309d039309d8273981fcfc3eb3f6166f2f15a4b99ca7070c9fabd43650`.

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

`/nodes/1/content`, bajty[122404,123453); SHA `6d4f6d24264c19f0074d51e715d44120a8036200046408cb5dbc92bbcd52e19c`.

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

`/gaps/14/reason`, bajty[536225,536308); SHA `286a5542f4ac379ccd55d2b0a8fd317afc8ff8198c7718d8a77a1b46f56cb2df`.

```json
"Battle-specific directions for 1–6 Rampage rolls is referenced but unavailable."
```

`/gaps/14/needed_context`, bajty[536334,536370); SHA `a37a1cb05ccaaed75273ff02a85c78abd59ba1597a62c694a0a8ae932cb45860`.

```json
"Actual selected battle map compass"
```

`/gaps/14/blocking`, bajty[536390,536394); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

### context-01 — justified_block / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "concrete_map_hexside": null,
  "block": "missing actual battle-map compass",
  "known_local_fact": "diagram is illustrative only"
}
```

1. N914table1–6 uses compass on map; N914diagram interpretation explicitly excludes universal geographical direction.
2. D914compass unresolved and G-D914compass blocking=true; actual battle_map missing in the case.
3. Example roll1 upper-right cannot establish a concrete battle-map hexside.

**Porównanie:** Matches the expected justified block; no invented compass.

**Zależności i blokada:** Actual map compass is essential here, unlike SIT-04 supplied route. Source diagram is not the missing real target.

**Wyłączenia:** Chosen geographic direction/hex, actualcounter rating and complete movement.

`/nodes/0/content`, bajty[167936,169593); SHA `a4baee8cdd6d3ed083a560ad77e366c096f546bbd14c747adb67246c29477e9f`.

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

`/nodes/1/content`, bajty[170034,171114); SHA `7c153965c8654edfba0068bc7b3c15c6cec3c26e8c03dc119754b76b83b376e1`.

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

`/gaps/14/reason`, bajty[620218,620301); SHA `286a5542f4ac379ccd55d2b0a8fd317afc8ff8198c7718d8a77a1b46f56cb2df`.

```json
"Battle-specific directions for 1–6 Rampage rolls is referenced but unavailable."
```

`/gaps/14/needed_context`, bajty[620328,620364); SHA `a37a1cb05ccaaed75273ff02a85c78abd59ba1597a62c694a0a8ae932cb45860`.

```json
"Actual selected battle map compass"
```

`/gaps/14/blocking`, bajty[620385,620389); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

## SIT-07 — Kawaleria bez OW: DR=TQ

### Zamrożone fakty i pytanie

```json
{
  "elephant": "ordinary, z nieprzyległego do sąsiedniego",
  "cavalry_can_withdraw": false,
  "cavalry_routed": false,
  "DR": 5,
  "TQ": 5
}
```

Czy natychmiastowy test daje0 czy1 Hit?

**Expected z eval-v1:** 0 CH przy DR5=TQ5; natychmiastowy test nadal wynika z9.16.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF33/left, `/situations/6/evidence/0`, obraz SHA `3ba367da1aee5635f964b887ff518ec63ba48175278e3fefdb031a8e03a7d15d`.

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

### first-001 — unjustified_block / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "immediate_TQ_check": true,
  "stored_representation_resolution": "blocked/unknown atDR<=TQ byG916",
  "source_expected_Cohesion_Hits": 0,
  "model_stated_1Hit": false
}
```

1. Source/frozen expected: DR5=TQ5 fails DR>TQ, hence local0CH while immediate test still required.
2. Original R916 action preserves DR>TQ/difference/min1 but interpretation.state=unknown; G916 explicitly requests clarification forDR<=TQ and blocking=true.
3. W faktach zadano brak możliwości OW, stan notRouted oraz DR5/TQ5. Brak pełnego OW lub rzeczywistego ratingu nie uzasadnia niepewności tej lokalnej gałęzi.
4. Evaluator does not insert0 into the preserved unknown interpretation or pretend an actual situation response said1.

**Porównanie:** Proposed unjustified local block/incomplete determination relative to frozen0CH; no claimed wrong numerical answer. Existing SEM-001/EXP-017 remain awaiting owner decision.

**Zależności i blokada:** G916 is the branch-specific block. General G-D916OW is out of requested scope because inability to withdraw is already supplied.

**Wyłączenia:** WholeOW, realTQ/rating, repair of original fields and automatic closure ofSEM-001.

`/rules/6/transcription`, bajty[216367,216709); SHA `faf33b1e91795adf3f8917104a33d773ed95f220987de9a880aeea404151ce6f`.

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

`/rules/6/interpretation`, bajty[216735,216976); SHA `aa9dc8b17a6de7173c63c5068c2160ec5962a35bb1d662804dbe5e0866ef5964`.

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

`/rules/6/conditions`, bajty[216998,217242); SHA `f47e84d4cb45fabc730175ed9ede2defe913d3bdeb8d5d13dca97ee3064f4978`.

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

`/rules/6/action_effect`, bajty[217267,217717); SHA `b4d40c43c2a7eda35edd8dae399439cd5cad3bb64b1ec2b2fe41f50e1a4ed9a1`.

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

`/rules/6/exceptions`, bajty[217739,217952); SHA `8b7699ae7c80269af8998037a3ebbc25e70e84f65f11beff1f6ab28233cb1522`.

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

`/rules/6/parameters`, bajty[217974,219048); SHA `5bfed31fbe3f66ae7884b8fb5ce5436cfa3ec1d99dd3e062a5bb27fdf58deea5`.

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

`/rules/6/time_limits`, bajty[219554,219803); SHA `74517483adeeaccda18aa44d23e2cbb964399fe27246d524946c3abd4c3838b9`.

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

`/gaps/0/reason`, bajty[529167,529310); SHA `f6cfd8f421cb08d667d73dbe253f6f2d5b316947ab2ecade667c196beb61ac4f`.

```json
"The minimum-1 phrase follows the DR>TQ condition; the text does not explicitly state the result for DR<=TQ. No unconditional minimum imposed."
```

`/gaps/0/needed_context`, bajty[529336,529395); SHA `f41ef0fdda2e7bbd6eec825af2b9072795e09307f9433f8fbcd98f93c75f600b`.

```json
"Clarification of whether minimum applies only when DR>TQ."
```

`/gaps/0/blocking`, bajty[529415,529419); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

### context-01 — unjustified_block / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "immediate_TQ_check": true,
  "stored_representation_resolution": "blocked/unknown atDR<=TQ byG916",
  "source_expected_Cohesion_Hits": 0,
  "model_stated_1Hit": false
}
```

1. Source/frozen expected: DR5=TQ5 fails DR>TQ, hence local0CH while immediate test still required.
2. Original R916 action preserves DR>TQ/difference/min1 but interpretation.state=unknown; G916 explicitly requests clarification forDR<=TQ and blocking=true.
3. W faktach zadano brak możliwości OW, stan notRouted oraz DR5/TQ5. Brak pełnego OW lub rzeczywistego ratingu nie uzasadnia niepewności tej lokalnej gałęzi.
4. Evaluator does not insert0 into the preserved unknown interpretation or pretend an actual situation response said1.

**Porównanie:** Proposed unjustified local block/incomplete determination relative to frozen0CH; no claimed wrong numerical answer. Existing SEM-001/EXP-017 remain awaiting owner decision.

**Zależności i blokada:** G916 is the branch-specific block. General G-D916OW is out of requested scope because inability to withdraw is already supplied.

**Wyłączenia:** WholeOW, realTQ/rating, repair of original fields and automatic closure ofSEM-001.

`/rules/6/transcription`, bajty[283726,284078); SHA `847c5d7215b12c62a7067b50880f680b5876b4f743b7d5caca53b2f791693b4f`.

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

`/rules/6/interpretation`, bajty[284105,284354); SHA `dc298ad7fa3d4ca2fb7184a3b637a430b119674df267969242a2f78dd5446a2d`.

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

`/rules/6/conditions`, bajty[284377,284631); SHA `f5ef97cca052405faf1d7e5f9f5b94084f28668f1926616bfe72f967d60d9e4a`.

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

`/rules/6/action_effect`, bajty[284657,285119); SHA `4a60a6e050c6f87a125d6b1e51e9c02e16927ab654cd9cbef7e4dfb560056c88`.

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

`/rules/6/exceptions`, bajty[285142,285365); SHA `f493d385ea94880ea721fcb08512f70a39cbbdb376e26670f5c93f9a9adcbdcd`.

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

`/rules/6/parameters`, bajty[285388,286503); SHA `9b436016e654b5ece64d9f615d14432fe87f0582bc956d7570375429361d107f`.

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

`/rules/6/time_limits`, bajty[287034,287293); SHA `1ec70752e940c8b5d6fd5be06ad30970b01af1166e4cb00ee6a9f81a7c35c41d`.

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

`/gaps/0/reason`, bajty[612658,612801); SHA `f6cfd8f421cb08d667d73dbe253f6f2d5b316947ab2ecade667c196beb61ac4f`.

```json
"The minimum-1 phrase follows the DR>TQ condition; the text does not explicitly state the result for DR<=TQ. No unconditional minimum imposed."
```

`/gaps/0/needed_context`, bajty[612828,612887); SHA `f41ef0fdda2e7bbd6eec825af2b9072795e09307f9433f8fbcd98f93c75f600b`.

```json
"Clarification of whether minimum applies only when DR>TQ."
```

`/gaps/0/blocking`, bajty[612908,612912); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

## SIT-08 — SK: halving i cap1

### Zamrożone fakty i pytanie

```json
{
  "context": "SK broni się w legalnie ustalonym Shock",
  "unadjusted_Hits_inflicted_by_SK": [
    1,
    3,
    6
  ],
  "other_modifiers": false
}
```

Podaj tylko transformację Hits zadanych przez SK.

**Expected z eval-v1:** Odpowiednio0,1,1 Hits: floor(1/2)=0, floor(3/2)=1, floor(6/2)=3 ograniczone do1.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF33/right, `/situations/7/evidence/0`, obraz SHA `3ba367da1aee5635f964b887ff518ec63ba48175278e3fefdb031a8e03a7d15d`.

> • Any Cohesion Hits inflicted by Skirmishers in Shock Combat
> are halved (round down) with a maximum of 1 Cohesion Hit.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "SK_inflicted_Hits_transformation": [
    0,
    1,
    1
  ]
}
```

1. R923 literal/effect says halve SK-inflicted Hits, rounddown,max1.
2. For supplied1: floor(1/2)=0, cap leaves0; for3:floor(3/2)=1; for6:floor(6/2)=3 then cap1.
3. N923ex retains numerical illustration; evaluator calculations use the stated operator, not unknown CRT lookup.

**Porównanie:** All three variants match; one situation sample, not three points.

**Zależności i blokada:** No baseCRT required because suppliedHits and legalShock context are given. Context operator correspondence does not accept mixed-defense/Size/wholeCRT.

**Wyłączenia:** BaseCRT, fullShock legality, mixeddefense and any other modifiers.

`/rules/13/transcription`, bajty[245169,245582); SHA `c729fd1b6fb29a25fc050a801ec65a7db07e0ecea19ef684aedbda9b198ed270`.

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

`/rules/13/interpretation`, bajty[245608,246393); SHA `3d4d0e9bbc4b49db005d7d797ec431f2da0d09a03a020c2206b7b9131bc2e683`.

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

`/rules/13/conditions`, bajty[246415,246637); SHA `9860237474fe072827d805ccb1051bb6e9be1870ff8d7c18e47dc7b9c7cc3f17`.

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

`/rules/13/action_effect`, bajty[246662,247368); SHA `09863157927710eb00ef00e07ed72f8c5f3f373f4312b6c94fe570f3216b5f09`.

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

`/rules/13/exceptions`, bajty[247390,247671); SHA `eab97edd08efff26928013c89002a355b31aa825124e4b4440cbd8e0523a9077`.

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

`/rules/13/parameters`, bajty[247693,248781); SHA `4c304688d97300a7e65922d51a646e5a30ba77532052109c2ec159fa8af7a4e1`.

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

`/rules/13/time_limits`, bajty[249359,249598); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/nodes/2/content`, bajty[123891,124342); SHA `d0b0d4ddd42b0c6c84106f212c9b847d2b613828097fe2f35875d8b88eb80b8c`.

```json
{
  "state": "known",
  "value": {
    "transcription": "Thus, if a Light Infantry attacking a Skirmisher would produce an unadjusted result on the Shock Results Table of 1(4), the actual result would be 0(4).",
    "interpretation": "Printed numerical example retained; no missing CRT semantics inferred."
  },
  "evidence_ids": [
    "E923ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "SK_inflicted_Hits_transformation": [
    0,
    1,
    1
  ]
}
```

1. R923 literal/effect says halve SK-inflicted Hits, rounddown,max1.
2. For supplied1: floor(1/2)=0, cap leaves0; for3:floor(3/2)=1; for6:floor(6/2)=3 then cap1.
3. N923ex retains numerical illustration; evaluator calculations use the stated operator, not unknown CRT lookup.

**Porównanie:** All three variants match; one situation sample, not three points.

**Zależności i blokada:** No baseCRT required because suppliedHits and legalShock context are given. Context operator correspondence does not accept mixed-defense/Size/wholeCRT.

**Wyłączenia:** BaseCRT, fullShock legality, mixeddefense and any other modifiers.

`/rules/13/transcription`, bajty[313577,314000); SHA `e5f1e9a5d2885bb7c6462a277c3fc5acef03fbd5aa05a369eceac75c9f6be3df`.

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

`/rules/13/interpretation`, bajty[314027,314827); SHA `2d8208efcc82ee9ca20f6321a7af8ba89d948ee6652f4ab0c77d958f38f0a754`.

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

`/rules/13/conditions`, bajty[314850,315082); SHA `4b0cf8384ed089ca6185d240b5d9d346c554cb798d65bb544931aec76c56cadc`.

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

`/rules/13/action_effect`, bajty[315108,315829); SHA `2ae1f4f582aba92c4a76cd3fa1b6124778a38380b517524b407b9aba5fb32cf5`.

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

`/rules/13/exceptions`, bajty[315852,316144); SHA `26c0e908fd486c9ee9bf3baee7acd2c2494f75823e50d106d52cb88208e8a283`.

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

`/rules/13/parameters`, bajty[316167,317296); SHA `0487b396d50818d2372a3ba39443718d456efa6f3039e1cd805528e8873a6872`.

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

`/rules/13/time_limits`, bajty[317901,318146); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/nodes/2/content`, bajty[171572,172034); SHA `8ab01da7049fde2b763e9527f0aa1c6b9a137d7fde2283c6d3ed4d6645535539`.

```json
{
  "state": "known",
  "value": {
    "transcription": "Thus, if a Light Infantry attacking a Skirmisher would produce an unadjusted result on the Shock Results Table of 1(4), the actual result would be 0(4).",
    "interpretation": "Printed numerical example retained; no missing CRT semantics inferred."
  },
  "evidence_ids": [
    "E923ex"
  ],
  "reason": null,
  "gap_ids": []
}
```

## SIT-09 — LC przeciw SK: wyjątek H&D i lokalna połowa

### Zamrożone fakty i pytanie

```json
{
  "missile_LC_MA": 8,
  "SK_MA": 6,
  "separate_Shock_test_target": "HI",
  "unadjusted_LC_Hits": 5,
  "superiority_and_other_modifiers": false
}
```

Czy niższe MA SK pozwala H&D? W osobnym ataku LC na HI przekształć podane5 Hits.

**Expected z eval-v1:** H&D przeciw SK zabronione mimo niższego MA. W odrębnym podanym Shock LC na HI lokalnie5→2 Hits.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF34/left, `/situations/8/evidence/0`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

> 9.31 Missile-armed Light Cavalry may use H&D fire (8.3) against
> all units with a lower MA, except Skirmishers. Light Cavalry
> Archers can fire when they use Orderly Withdrawal (6.55).

Źródło PDF33/right, `/situations/8/evidence/1`, obraz SHA `3ba367da1aee5635f964b887ff518ec63ba48175278e3fefdb031a8e03a7d15d`.

> 9.22 Missile Fire: There is a +2 DRM to the Missile Fire DR
> whenever a Skirmisher unit is the target. Skirmisher and Light
> Infantry Archers (Class A) cannot use H&D fire. Light Cavalry
> (all missile classes) cannot use H&D against Skirmishers..

Źródło PDF34/left, `/situations/8/evidence/2`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

> 9.32 Any Cohesion Hits inflicted by attacking Light Cavalry
> against a Phalanx or a Heavy, Medium, Legion, or Barbarian
> Infantry unit are halved (round down).

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "H_and_D_against_SK": false,
  "first_001_local_LC_vs_HI_Hits": 2
}
```

1. R931 permits lowerMA target exceptSK; R922 prohibits LC H&D againstSK of all missile classes.6<8 does not defeat the explicit exception.
2. In separate LCvsHI local arithmetic, originalfirstR932 states halve/floor; supplied5 and noAS/othermodifiers → floor(5/2)=2.
3. Do not combine the H&D targetSK and the different Shock targetHI or use Hits received rather than inflicted.

**Porównanie:** First representation matches the frozen requested two-part local result. Context-specific qualification is separately assessed below.

**Zależności i blokada:** Unknown AS/CRT procedure does not automatically block the supplied noAS arithmetic. AddedStep4 Routed qualification creates an additional scoped question after context.

**Wyłączenia:** FullH&D, AS/LC order, actualCRT, unstated defenderRouted status or8.45selection, and any revision of frozen facts.

`/rules/12/transcription`, bajty[240036,240415); SHA `feaed7656db285d2b6090a390284241e2c34440b842aa1284b6ea553ecc32763`.

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

`/rules/12/interpretation`, bajty[240441,240908); SHA `6dedb0ea1587bdd33bf62687a8af3ab9676d7ae37b6886550739cbe1b3d90384`.

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

`/rules/12/conditions`, bajty[240930,241157); SHA `212982f00efb4eb2c6537406ac6442981cba0aa20e3fbda9603eed1250676971`.

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

`/rules/12/action_effect`, bajty[241182,241570); SHA `3ca3cf71614646b859a61ea7cb7ecbf86161d03a09b500552ce6fa2ab0d3d760`.

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

`/rules/12/exceptions`, bajty[241592,241840); SHA `55d9e0079ac980ca21267f7c4b1f6b3348c63263ec077373e173d696d838a531`.

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

`/rules/12/parameters`, bajty[241862,242512); SHA `6979e735498f3877a164331dc936fa7ee3a07d721920841e3dd65f36d4ebbad9`.

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

`/rules/12/time_limits`, bajty[243059,243298); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/15/transcription`, bajty[256711,257079); SHA `fa5fb9f82d8ac93e9d1bcabf8d56f9364fc72a4e7cc3485bdb35cb7f2f9b3485`.

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

`/rules/15/interpretation`, bajty[257105,257486); SHA `30179e75bffb0d015141fe0a5f69b1bfde5bec03ab3c61b6060bcc44a70c80d1`.

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

`/rules/15/conditions`, bajty[257508,257737); SHA `1788d89aa96c764fdb50f09b70aa1f22bbbf2670a95d3b7817450e994cf97e99`.

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

`/rules/15/action_effect`, bajty[257762,258064); SHA `45a32003fd53ae15622cac099a481383da2d72b67942fc1f96ca01b8b548f35a`.

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

`/rules/15/exceptions`, bajty[258086,258292); SHA `584d9c9c488b166a828266d6132f5ef237a60be3a411be6502aeb31d7ed5d5b9`.

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

`/rules/15/parameters`, bajty[258314,258965); SHA `635c4166e34ea74e709200dcf5b80ac5a6d582fee72c8f503d51308a649522eb`.

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

`/rules/15/time_limits`, bajty[259493,259697); SHA `542972c55c7b938e282e661044b741040e3b38bf5bcebebfd8a1c15bdcd80f59`.

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

`/rules/16/transcription`, bajty[260440,260761); SHA `8a53d1f78d37ee6211d5aed412e66f87b0ce934973115bddf1fc262a51e12d61`.

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

`/rules/16/interpretation`, bajty[260787,261069); SHA `8cee10931c10751c18fe8a45901f6398eb999cb6210501811850f049d504fb2b`.

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

`/rules/16/conditions`, bajty[261091,261322); SHA `dbc9e73e8ddb502c76db8f62e79e514126f580f8804d513e46ddf970bbdd30de`.

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

`/rules/16/action_effect`, bajty[261347,261550); SHA `5036c1211b0fd4b3a033221f34c58dd83cdb5bba47ef36b2baa78f714cc9c904`.

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

`/rules/16/exceptions`, bajty[261572,261820); SHA `097e67ed95454f521c7b4db0d723b54a521dfd5cecdc67fd1f14e443e3c5b10c`.

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

`/rules/16/parameters`, bajty[261842,262514); SHA `fed8257ba56943c544cf61c6ec4d1755d75991ba16c4c872c71db021f0ed46de`.

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

`/rules/16/time_limits`, bajty[263108,263347); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/nodes/4/content`, bajty[126403,127035); SHA `4660d0a1496dab670767e40e4590977dcd343858b422e5f9ea7e647f7ee10602`.

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

### context-01 — unassessed / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "H_and_D_against_SK": false,
  "local_LC_Hits_if_defender_not_Routed": 2,
  "local_LC_Hits_if_defender_Routed": 5,
  "fixed_Hits_under_unqualified_frozen_facts": null
}
```

1. H&D targetSK prohibition unchanged.
2. Context R932 interpretation/exceptions and suppliedStep4#4 explicitly say reduction does not apply if defenderRouted.
3. Frozen facts nameHI and noAS/othermodifiers, but do not explicitly bind defenderRouted or LC-used-in-determination. No default false inserted.
4. Under the matching local LC condition: nonRouted branch floor(5/2)=2; Routed branch keeps5 with supplied noothermodifiers. Branches are diagnostic, not a silently changed expected.
5. Owner may confirm narrowpure9.32 operator scope or that supplied noothermodifiers excludes the Routed exception. Until that scope/fact reading is decided, the complete contextual case is held.

**Porównanie:** H&D matches; contextual full5→2 conclusion cannot be certified without a scope/fact decision. Not a demonstrated wrong model result or context regression.

**Zależności i blokada:** DCTX932-S4 reaches actual supplied conditional source; missing queried local applicability is distinct from missingCRT/base already supplied.

**Wyłączenia:** FullH&D, AS/LC order, actualCRT, unstated defenderRouted status or8.45selection, and any revision of frozen facts.

`/rules/12/transcription`, bajty[308264,308653); SHA `79aea0675a6df5da58362a2748b926bf3545d2affc30a3dac9bc6e6458c1adad`.

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

`/rules/12/interpretation`, bajty[308680,309159); SHA `d78646d6d1b8e79af11a0fbd5183b44d696f76eeff804c13ada890bd5aab3ef7`.

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

`/rules/12/conditions`, bajty[309182,309417); SHA `b22e8834a76a1f94c2864565f949b9ac0ab74fd4b50c7e235d46888964ed9919`.

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

`/rules/12/action_effect`, bajty[309443,309843); SHA `46aaa3cf385811a55eb8c8f75e6d4d808293593b73596c87f4b334d48d8ff3e1`.

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

`/rules/12/exceptions`, bajty[309866,310122); SHA `7e797ebf87a9d617e93cc1e1141b8273b24cc89becd45a884f8609db94d242dd`.

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

`/rules/12/parameters`, bajty[310145,310820); SHA `18a66551b2396ead4f8614a52c8b8f1494f992a52f4849803abf21928bf80f4d`.

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

`/rules/12/time_limits`, bajty[311392,311637); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/15/transcription`, bajty[325522,325900); SHA `f2fd90519283ac3df38166d0eb58003e0080771e5cbf98888032f86778d3aedc`.

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

`/rules/15/interpretation`, bajty[325927,326319); SHA `b31c2c701e00bd832468a18cccb4e5f91716795a36f0b76ad9daaac26e4ae9c1`.

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

`/rules/15/conditions`, bajty[326342,326581); SHA `8f43dc4b65eaf355d2764bede489c1a0884e5ab2850c57fcacc2211fceb5d08c`.

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

`/rules/15/action_effect`, bajty[326607,326920); SHA `be9a8dd988db4254de29319872ce268d65cc263dd1ae891fa198dea166ec33a5`.

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

`/rules/15/exceptions`, bajty[326943,327159); SHA `3341cf28e6cfdc90ae8ac9e22ccbeb982c95318cbbca3f321b04e20694d681b3`.

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

`/rules/15/parameters`, bajty[327182,327858); SHA `d8af76f77c67db9d533e035768b890db529f2298cbe7df450071803fb5cb913a`.

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

`/rules/15/time_limits`, bajty[328411,328625); SHA `a44ed4234d47f7e10b2312df55b8f2a2c3bce773a3d090ed2700e41187d9be69`.

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

`/rules/16/transcription`, bajty[329401,329732); SHA `a33aa4d1db4695a62905e1c72ddcc054552f28f62d8bb21bc3fa771641c0d1d9`.

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

`/rules/16/interpretation`, bajty[329759,330560); SHA `69967aa8bb252b4fbda7e252169ed13180bf9a932e0b3021bdce66e80bef9f60`.

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

`/rules/16/conditions`, bajty[330583,330824); SHA `edb26371f0d661ead19391daa09484c6dd689780503e3c012ca7036791198699`.

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

`/rules/16/action_effect`, bajty[330850,331061); SHA `8a04ff26ccf284ca7852440eb32218eb344ad3292bc6fb14ae1b6ee3903f692c`.

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

`/rules/16/exceptions`, bajty[331084,331447); SHA `723a5b248c7cc9f3c6ae8c902481d65bbd5958fa36698ca04711245827cde880`.

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

`/rules/16/parameters`, bajty[331470,332167); SHA `3af479066970ff224720e7855fa715c1728cd4e3fa08f23b47dfb016576e9f95`.

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

`/rules/16/time_limits`, bajty[332789,333034); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/nodes/4/content`, bajty[174182,175212); SHA `6389d28ed267dfc121abd485cc4a20a9e352f7fcd87fab5c3f565c340500f4d5`.

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

`/nodes/58/content`, bajty[221265,235786); SHA `f659c6735b345f778dd4f28f9ecf3d8796730a8f1ed7f331349fed76e1d16b04`.

```json
{
  "state": "known",
  "value": {
    "transcription": {
      "state": "known",
      "value": "Step 4: Apply Results: Results on the Shock CRT are Cohesion Hits for both attacker and defender. The # in parentheses is for the defender. The resultant Hits are modified as follows:\nIf the attacker was superior (AS), then double (2x) the defender’s result.\nIf the defender was superior (DS), then triple (3x) the attacker’s result.\nIf the defender is a Skirmisher, halve (½x, round down) the attacker’s Hits with a maximum result of 1 Hit.\nIf the attacker used in the determination is Light Cavalry (8.45) and the defender is a Phalanx or a Heavy, Medium, Legion, or Barbarian Infantry unit, halve (½x, round down) the defender’s Hits. This reduction does not apply if the defender is Routed and is cumulative with bullet #1.\nIf more than one unit of the same player was involved in that combat, Cohesion Hits are distributed as per 10.13.",
      "evidence_ids": [
        "ECTX846S4-header",
        "ECTX846S4-AS",
        "ECTX846S4-DS",
        "ECTX846S4-SK",
        "ECTX846S4-LC",
        "ECTX846S4-distribution"
      ],
      "reason": "Complete supplied Step 4 transcription; line wraps joined only. Rule number is metadata, not visible heading.",
      "gap_ids": []
    },
    "interpretation": {
      "state": "known",
      "value": [
        "Both Shock CRT results are Cohesion Hits; parenthesized number belongs to defender.",
        "AS doubles defender result; DS triples attacker result. These are conditional operators, not established applicability.",
        "Skirmisher defender: halve attacker Hits, round down, maximum 1 Hit.",
        "LC attacker used in determination (8.45) against listed infantry: halve defender Hits, round down; no reduction against Routed defender; cumulative with bullet #1.",
        "More than one unit of same player invokes 10.13 distribution.",
        "No base lookup, actual applicability, combined operation/rounding order or final result is reconstructed."
      ],
      "evidence_ids": [
        "ECTX846S4-header",
        "ECTX846S4-AS",
        "ECTX846S4-DS",
        "ECTX846S4-SK",
        "ECTX846S4-LC",
        "ECTX846S4-distribution"
      ],
      "reason": "Unreviewed interpretation confined to complete bounded fragment.",
      "gap_ids": []
    },
    "operators": [
      {
        "source_bullet": 1,
        "condition": {
          "state": "known",
          "value": "Attacker was superior (AS)",
          "evidence_ids": [
            "ECTX846S4-AS"
          ],
          "reason": null,
          "gap_ids": []
        },
        "action": {
          "state": "known",
          "value": "Double (2x) defender result",
          "evidence_ids": [
            "ECTX846S4-AS"
          ],
          "reason": null,
          "gap_ids": []
        },
        "parameters": [
          {
            "name": "AS defender-result factor",
            "value": 2,
            "unit": {
              "state": "known",
              "value": "multiplier",
              "evidence_ids": [
                "ECTX846S4-AS"
              ],
              "reason": null,
              "gap_ids": []
            },
            "evidence_ids": [
              "ECTX846S4-AS"
            ]
          }
        ]
      },
      {
        "source_bullet": 2,
        "condition": {
          "state": "known",
          "value": "Defender was superior (DS)",
          "evidence_ids": [
            "ECTX846S4-DS"
          ],
          "reason": null,
          "gap_ids": []
        },
        "action": {
          "state": "known",
          "value": "Triple (3x) attacker result",
          "evidence_ids": [
            "ECTX846S4-DS"
          ],
          "reason": null,
          "gap_ids": []
        },
        "parameters": [
          {
            "name": "DS attacker-result factor",
            "value": 3,
            "unit": {
              "state": "known",
              "value": "multiplier",
              "evidence_ids": [
                "ECTX846S4-DS"
              ],
              "reason": null,
              "gap_ids": []
            },
            "evidence_ids": [
              "ECTX846S4-DS"
            ]
          }
        ]
      },
      {
        "source_bullet": 3,
        "condition": {
          "state": "known",
          "value": "Defender is a Skirmisher",
          "evidence_ids": [
            "ECTX846S4-SK"
          ],
          "reason": null,
          "gap_ids": []
        },
        "action": {
          "state": "known",
          "value": "Halve attacker Hits, round down, maximum 1 Hit",
          "evidence_ids": [
            "ECTX846S4-SK"
          ],
          "reason": null,
          "gap_ids": []
        },
        "parameters": [
          {
            "name": "Skirmisher defender: attacker-Hits factor",
            "value": "1/2",
            "unit": {
              "state": "known",
              "value": "multiplier",
              "evidence_ids": [
                "ECTX846S4-SK"
              ],
              "reason": null,
              "gap_ids": []
            },
            "evidence_ids": [
              "ECTX846S4-SK"
            ]
          },
          {
            "name": "Skirmisher defender: attacker-Hits rounding",
            "value": "down",
            "unit": {
              "state": "known",
              "value": "rounding direction",
              "evidence_ids": [
                "ECTX846S4-SK"
              ],
              "reason": null,
              "gap_ids": []
            },
            "evidence_ids": [
              "ECTX846S4-SK"
            ]
          },
          {
            "name": "Skirmisher defender: attacker-Hits cap",
            "value": 1,
            "unit": {
              "state": "known",
              "value": "Cohesion Hit",
              "evidence_ids": [
                "ECTX846S4-SK"
              ],
              "reason": null,
              "gap_ids": []
            },
            "evidence_ids": [
              "ECTX846S4-SK"
            ]
          }
        ]
      },
      {
        "source_bullet": 4,
        "condition": {
          "state": "known",
          "value": "Attacker used in determination is Light Cavalry (8.45); defender is a Phalanx or Heavy, Medium, Legion, or Barbarian Infantry unit",
          "evidence_ids": [
            "ECTX846S4-LC"
          ],
          "reason": null,
          "gap_ids": []
        },
        "action": {
          "state": "known",
          "value": "Halve defender Hits, round down",
          "evidence_ids": [
            "ECTX846S4-LC"
          ],
          "reason": null,
          "gap_ids": []
        },
        "exception": {
          "state": "known",
          "value": "Reduction does not apply if defender is Routed",
          "evidence_ids": [
            "ECTX846S4-LC"
          ],
          "reason": null,
          "gap_ids": []
        },
        "combination": {
          "state": "known",
          "value": "Cumulative with bullet #1",
          "evidence_ids": [
            "ECTX846S4-LC"
          ],
          "reason": "No processing/rounding order inferred.",
          "gap_ids": []
        },
        "parameters": [
          {
            "name": "LC defender-Hits factor",
            "value": "1/2",
            "unit": {
              "state": "known",
              "value": "multiplier",
              "evidence_ids": [
                "ECTX846S4-LC"
              ],
              "reason": null,
              "gap_ids": []
            },
            "evidence_ids": [
              "ECTX846S4-LC"
            ]
          },
          {
            "name": "LC defender-Hits rounding",
            "value": "down",
            "unit": {
              "state": "known",
              "value": "rounding direction",
              "evidence_ids": [
                "ECTX846S4-LC"
              ],
              "reason": null,
              "gap_ids": []
            },
            "evidence_ids": [
              "ECTX846S4-LC"
            ]
          }
        ]
      }
    ],
    "result_notation": {
      "state": "known",
      "value": "Parenthesized number is for defender; both sides receive Cohesion Hits",
      "evidence_ids": [
        "ECTX846S4-header"
      ],
      "reason": null,
      "gap_ids": []
    },
    "distribution": {
      "state": "known",
      "value": "If more than one unit of same player involved, distribute as per 10.13",
      "evidence_ids": [
        "ECTX846S4-distribution"
      ],
      "reason": "N1013 is supplied original boundary context; 6.68 bullet #6 remains missing.",
      "gap_ids": [
        "G-D1013stack"
      ]
    },
    "applicability": {
      "state": "unknown",
      "value": null,
      "evidence_ids": [
        "ECTX846S4-header",
        "ECTX846S4-AS",
        "ECTX846S4-DS",
        "ECTX846S4-SK",
        "ECTX846S4-LC",
        "ECTX846S4-distribution"
      ],
      "reason": "AS/DS entitlement, attacker determination, exact tables and identified combat facts not established.",
      "gap_ids": [
        "GCTX-applicability",
        "GCTX-845"
      ]
    },
    "base_results": {
      "state": "unknown",
      "value": null,
      "evidence_ids": [
        "ECTX846S4-header"
      ],
      "reason": "Actual Shock CRT headers/rows/notes and numeric entries absent.",
      "gap_ids": [
        "GCTX-CRT"
      ]
    },
    "combined_operation_order": {
      "state": "unknown",
      "value": null,
      "evidence_ids": [
        "ECTX846S4-AS",
        "ECTX846S4-LC"
      ],
      "reason": "Cumulative explicit; combined processing/rounding order unresolved. No cancellation imposed.",
      "gap_ids": [
        "GCTX-order"
      ]
    },
    "final_results": {
      "state": "unknown",
      "value": null,
      "evidence_ids": [
        "ECTX846S4-header",
        "ECTX846S4-AS",
        "ECTX846S4-DS",
        "ECTX846S4-SK",
        "ECTX846S4-LC",
        "ECTX846S4-distribution"
      ],
      "reason": "No outcome calculated from absent tables or unresolved applicability/order/allocation.",
      "gap_ids": [
        "GCTX-CRT",
        "GCTX-applicability",
        "GCTX-order",
        "G-D1013stack"
      ]
    },
    "external_context_status": "external_with_source",
    "result_status": "blocked_source",
    "scope_status": {
      "region_id": "pdf-27-context-8.46-step-4",
      "pdf_page": 27,
      "column": "left",
      "pdf_bbox": [
        40,
        413,
        300,
        650
      ],
      "supplied_image": "context/pass-01/evidence/8.46-step-4-pdf-27.png",
      "supplied_image_sha256": "87ca4e8f337861b2116317ab8cecdebbc0ebdda10c3af8236c0689a5f9e2df1b",
      "crop_width": 433,
      "crop_height": 395,
      "fragment": "8.46 Step 4: Apply Results only; all four bullets and final 10.13 cross-reference",
      "source_selection_status": "owner_approved_exact_scope",
      "source_selection_evidence": "context/pass-01/freeze-public-v1.json",
      "historical_draft_human_review": "waiting_review",
      "selection_flag_resolution": "Superseded only for source selection by supplied freeze; no semantic approval conveyed.",
      "meaning_acceptance": "not_performed",
      "scope_role": "boundary_context",
      "excluded": "Step 1-3, actual Shock CRT, 8.45, 8.47 and full-page PDF27 render not supplied.",
      "heading_lineage_status": "8.46 attribution from supplied scope metadata; crop prints Step 4 only. Parent heading on PDF26 not viewed in this response."
    }
  },
  "evidence_ids": [
    "ECTX846S4-header",
    "ECTX846S4-AS",
    "ECTX846S4-DS",
    "ECTX846S4-SK",
    "ECTX846S4-LC",
    "ECTX846S4-distribution"
  ],
  "reason": "Complete supplied fragment; unresolved facets separately unknown. Not standalone chapter8 extraction.",
  "gap_ids": []
}
```

`/gaps/84/reason`, bajty[656689,656768); SHA `e74f3f13f4af089a3c9a9b1c05d74afd6be16f65be41e98f41ea9ae3c1a2f65f`.

```json
"Bullet #4 refers to 8.45 attacker determination; that procedure not included."
```

`/gaps/84/needed_context`, bajty[656795,656869); SHA `b1202b1765e8d23a53ec288b822df365ea32cbcf3a749028049a575465ba6001`.

```json
"Exact needed 8.45 selection procedure; no reconstruction from reference."
```

`/gaps/84/blocking`, bajty[656890,656894); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

`/gaps/83/reason`, bajty[655976,656143); SHA `c85996e558a1fa89ffa91532a5974882eef4f63b877652d57e2bf44230e68820`.

```json
"Cumulative with bullet #1 stated; combined operation/rounding order and execution of printed 9.32 example unresolved. No unconditional 2x/half cancellation asserted."
```

`/gaps/83/needed_context`, bajty[656170,656265); SHA `bcf237cef17bde0ef61d45bda56a85c4003dbf4e526a54e048763f17883d786d`.

```json
"Source-backed combined numeric/rounding procedure where needed and exact base-result context."
```

`/gaps/83/blocking`, bajty[656286,656290); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

Niepewność: The phrase noothermodifiers may be intended to suppress this exception; this evaluator does not choose that implicit reading or amend eval-v1.

## SIT-10 — Phalanx Defense: moving HI i stationary

### Zamrożone fakty i pytanie

```json
{
  "defender": "PH",
  "both_flanks_qualify": true,
  "attacker": "HI, żaden PH",
  "angle": "Front",
  "variants": [
    "moves adjacent then Shock",
    "starts adjacent and stays"
  ]
}
```

Podaj tylko shift wynikający z9.41, nie wynik CRT.

**Expected z eval-v1:** Moving HI:1L za każdy flank, razem2L. Started adjacent/stayed:0L z9.41. Dla moving non-HI/non-PH byłoby4L przy tych flankach.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF34/left, `/situations/9/evidence/0`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

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

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "moving_HI_shift": "2L",
  "started_adjacent_stayed_shift": "0L",
  "moving_nonHI_nonPH_counterfactual_shift": "4L"
}
```

1. R941 conditions require movesadjacent/Front/qualifyingflank and noPHattacker; supplied facts satisfy moving variant.
2. HI shift1L perqualifyingflank ×2=2L; started-adjacent/stayed is explicitly excluded →0L from9.41.
3. The specified nonHI/nonPH alternative uses2L perflank ×2=4L.

**Porównanie:** All requested shifts, signs and movement boundary match.

**Zależności i blokada:** D941CRT missing table is not needed for a requested column shift with qualifiers given. No actual CRT outcome claimed.

**Wyłączenia:** CRTbase/lookup and other combat modifiers or concretegeometry.

`/rules/17/transcription`, bajty[264603,264971); SHA `4151513228eee15659368949e0b30730453ae8508a0626819415989cbcf5efef`.

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

`/rules/17/interpretation`, bajty[264997,265343); SHA `cd15c8a42d56c6f141a539c7627089216e669b474b525a6429a93c0465854024`.

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

`/rules/17/conditions`, bajty[265365,265701); SHA `fbef9e61a1fa8cbabaa273cb6af8dbc1183c6122e0a74dc8d85306d392269084`.

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

`/rules/17/action_effect`, bajty[265726,265993); SHA `473fab550ae5127f0a3a89d531c253e197b93aa3fb454a35f1265fb6a0e67c07`.

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

`/rules/17/exceptions`, bajty[266015,266351); SHA `b1931298d3384d653c0768926318dff0ed1b002d67ceeec86e166cd3aff4315f`.

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

`/rules/17/parameters`, bajty[266373,267480); SHA `afa7b8426637d93c9054d85ae7747eee8a53b44bd2bf1f4213e02f07134712b9`.

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

`/rules/17/time_limits`, bajty[267991,268244); SHA `6ca5df95f6078220d9e6805651d52a99556aadc74c294bfba1c17ac8ba3db5d5`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "moving_HI_shift": "2L",
  "started_adjacent_stayed_shift": "0L",
  "moving_nonHI_nonPH_counterfactual_shift": "4L"
}
```

1. R941 conditions require movesadjacent/Front/qualifyingflank and noPHattacker; supplied facts satisfy moving variant.
2. HI shift1L perqualifyingflank ×2=2L; started-adjacent/stayed is explicitly excluded →0L from9.41.
3. The specified nonHI/nonPH alternative uses2L perflank ×2=4L.

**Porównanie:** All requested shifts, signs and movement boundary match.

**Zależności i blokada:** D941CRT missing table is not needed for a requested column shift with qualifiers given. No actual CRT outcome claimed.

**Wyłączenia:** CRTbase/lookup and other combat modifiers or concretegeometry.

`/rules/17/transcription`, bajty[334435,334813); SHA `83c108fc70c3c0101d4ff86e9982514a68f860154730b91a11b8675e527c8533`.

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

`/rules/17/interpretation`, bajty[334840,335194); SHA `3c624c466fc1d721d146b3aadb6809a2ca37e201727ba7e99080fef74d502fb2`.

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

`/rules/17/conditions`, bajty[335217,335564); SHA `552d7cac868fd2d23fa7cd70a6d70e6a3c495095ecfe5cc1877bcf93cbeb7a91`.

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

`/rules/17/action_effect`, bajty[335590,335865); SHA `d16fe240936ce66541286b2cbf5bd4c11b53e53384378d0ce1994a923695f666`.

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

`/rules/17/exceptions`, bajty[335888,336236); SHA `864e5c7ff178b1fc1dd67fefa457a57c2142076f8552b03817d1043e3eee9d02`.

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

`/rules/17/parameters`, bajty[336259,337407); SHA `7cdc38962c191482cebb839b40ed72afddcb40b962831e353ea422b26a7843a4`.

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

`/rules/17/time_limits`, bajty[337943,338206); SHA `2e1a745c571fd085a4976a26226b1fe68517dcf676dfa2612d64ca80d58caac7`.

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

## SIT-11 — DD: niewiadoma eligibility scenariusza

### Zamrożone fakty i pytanie

```json
{
  "units": "dwie PH",
  "OC_order": true,
  "rear_start_and_MPs": true,
  "scenario_eligible_list": "missing"
}
```

Czy można ogłosić formowanie DD dla tych rzeczywistych PH?

**Expected z eval-v1:** Blokada eligibility. Podane lokalne warunki9.51 nie zastępują listy scenario-specific.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF34/right, `/situations/10/evidence/0`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

> Eligible units are listed in the scenario-specific rules.

Źródło PDF34/right, `/situations/10/evidence/1`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

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

Źródło PDF34/right, `/situations/10/evidence/2`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

> EXAMPLE: See the scenario rules for Cynoscephalae.

### first-001 — justified_block / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "forming_actual_PH_DD": "blocked",
  "missing": "selected scenario eligible-unit list",
  "local_formation_conditions": "supplied but insufficient"
}
```

1. R95note says eligible units determined by scenario-specific rules; R951 conditions starts Eligible Phalanxes.
2. G-D95scenario blocking=true and case eligiblelist missing. OCorder/rearstart/MPs do not establish eligibility.
3. Cynoscephalae example reference is not a general eligible list.

**Porównanie:** Matches expected justified eligibility block in both representations.

**Zależności i blokada:** D95scenario actual target missing is critical for this realunit question. No new scenario acquired.

**Wyłączenia:** Eligibility invention, allPHdefault, exact terrain costs and actualformation legality beyond supplied predicates.

`/rules/18/transcription`, bajty[269020,269377); SHA `5ff333197c7db5690d7301bfdb9d3c04dad4fde1b51599f0c65d61872a3cd4bf`.

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

`/rules/18/interpretation`, bajty[269403,269711); SHA `5af8c602cf4f6e71ac41dda1814e4645faea21175a3adaf2f7a0b5c77df4c531`.

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

`/rules/18/conditions`, bajty[269733,269963); SHA `e5e7ba56126819de1009fb3fdc9c09e23042e9a27c39c503c87211f39a672f8a`.

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

`/rules/18/action_effect`, bajty[269988,270217); SHA `0994d504a3efa5cc677cbf971397953a896fb7be3a7ea49cb91b42d182316bb5`.

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

`/rules/18/exceptions`, bajty[270239,270490); SHA `7ef72c8f296bdeb240483c779e52827e85d491da68ea30eefec8be58aac6c6a4`.

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

`/rules/18/parameters`, bajty[270512,270742); SHA `886e5991b172fbc87ef5bf10d717d01535127674709f3c9eabfa5079a64639b5`.

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

`/rules/18/time_limits`, bajty[271224,271463); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/19/transcription`, bajty[273001,273363); SHA `3629aa77432ed912c36a5191d1e8b4943b01667b9bfb3d2735f6d202cbf5ae0d`.

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

`/rules/19/interpretation`, bajty[273389,273856); SHA `bc89ae70b273b4941d813ef43f9bee7a90e91234c66a72c57e2f9f56f04a0408`.

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

`/rules/19/conditions`, bajty[273878,274192); SHA `80a22b2c5e12e70d2c216f3f6a9d3ec02c7d5c3ee08806ddb23494739a6cbe85`.

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

`/rules/19/action_effect`, bajty[274217,274605); SHA `c5ae9a64ee1678bccdcfd80aa7c968512debc60c092b9dc63bde5ac36573a09a`.

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

`/rules/19/exceptions`, bajty[274627,274875); SHA `1fc0624068de45a38e86266ed06bc18546dfee5b7739e556ecc8b0bfbe9747f4`.

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

`/rules/19/parameters`, bajty[274897,275968); SHA `177b61bd3dfa68e19f68e3fbd87148c9c311a659e27f47cb878c6dcd12c8e153`.

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

`/rules/19/time_limits`, bajty[276433,276726); SHA `f3481943a11973d476decb5e49b39697bbfc317be73a4e7a80051732ab8fc6d6`.

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

`/gaps/33/reason`, bajty[545538,545602); SHA `ff87850991637d4d8630ea610daa4182f52045ee868a7dc295d6a6fefd9d711f`.

```json
"Eligible Double Depth Phalanxes is referenced but unavailable."
```

`/gaps/33/needed_context`, bajty[545628,545679); SHA `f6ad137cebebc5b0d3807dd4d2e30946d155b5aadc70e688b224750fc4f916e0`.

```json
"Selected scenario Double Depth eligible-unit list"
```

`/gaps/33/blocking`, bajty[545699,545703); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

### context-01 — justified_block / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "forming_actual_PH_DD": "blocked",
  "missing": "selected scenario eligible-unit list",
  "local_formation_conditions": "supplied but insufficient"
}
```

1. R95note says eligible units determined by scenario-specific rules; R951 conditions starts Eligible Phalanxes.
2. G-D95scenario blocking=true and case eligiblelist missing. OCorder/rearstart/MPs do not establish eligibility.
3. Cynoscephalae example reference is not a general eligible list.

**Porównanie:** Matches expected justified eligibility block in both representations.

**Zależności i blokada:** D95scenario actual target missing is critical for this realunit question. No new scenario acquired.

**Wyłączenia:** Eligibility invention, allPHdefault, exact terrain costs and actualformation legality beyond supplied predicates.

`/rules/18/transcription`, bajty[339014,339381); SHA `4a78b0e26487d9919be5ac6db27dc3be2056657bb752bf2f18f4d9f69486e166`.

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

`/rules/18/interpretation`, bajty[339408,339724); SHA `f046f3ad4ae191dae045a603be563e0f3d7f36c7eb2a111408f3802bd2a43b94`.

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

`/rules/18/conditions`, bajty[339747,339985); SHA `dff54594147e9a5f46fdddfc379c04e4d250819133eefff15ec3abbde782e3a6`.

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

`/rules/18/action_effect`, bajty[340011,340248); SHA `7405eedc561a8b312154b305fdc37b8db5758621366f86bcebe8adc36c4751f5`.

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

`/rules/18/exceptions`, bajty[340271,340530); SHA `c0addc7b41ee9f803b4ea92964a2d30313a326a64ebb760ea5558101c5013867`.

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

`/rules/18/parameters`, bajty[340553,340791); SHA `7b69901ac4d9a347dcf4c6a7117dfbfb20103183dfa66dc8cdd986755babb862`.

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

`/rules/18/time_limits`, bajty[341296,341541); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/19/transcription`, bajty[343139,343511); SHA `8ae8a86fedbba6b3ae488ca1a1b0fbf715543ffef04cca7077a25f872f286de8`.

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

`/rules/19/interpretation`, bajty[343538,344017); SHA `6955c979375bfcd10dd1ed99b816d76e89e9c7192d62e273f9a9388229871f79`.

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

`/rules/19/conditions`, bajty[344040,344365); SHA `248a7879a9b8e3efb61e3a8e17a648ae4f9dad534766671b7e99b25d2d22703c`.

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

`/rules/19/action_effect`, bajty[344391,344791); SHA `b899a18d22fc0ccf5e455a9f76cdf2d0c05924cbba2f07e0afb77567abbd81ca`.

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

`/rules/19/exceptions`, bajty[344814,345070); SHA `6d9d8dccbacf297fef5a990c1c55e41a92104787c878495afae813c76c725eff`.

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

`/rules/19/parameters`, bajty[345093,346205); SHA `2e3237468bbba7d8ab11ad5a0ef277f5417e4ab6fccd234fc959b4975d091b9c`.

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

`/rules/19/time_limits`, bajty[346694,346998); SHA `b02c642421215de55e05baece4aad621340fe850c51b3fd6355a7a435bbf8b29`.

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

`/gaps/33/reason`, bajty[630424,630488); SHA `ff87850991637d4d8630ea610daa4182f52045ee868a7dc295d6a6fefd9d711f`.

```json
"Eligible Double Depth Phalanxes is referenced but unavailable."
```

`/gaps/33/needed_context`, bajty[630515,630566); SHA `f6ad137cebebc5b0d3807dd4d2e30946d155b5aadc70e688b224750fc4f916e0`.

```json
"Selected scenario Double Depth eligible-unit list"
```

`/gaps/33/blocking`, bajty[630587,630591); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

## SIT-12 — DD: Flank3x i nieparzysty podział

### Zamrożone fakty i pytanie

```json
{
  "formation": "DD już legalnie ustalone",
  "attack": "Shock Flank",
  "base_defender_Hits_before_directional_multiplier": 3,
  "other_modifiers": false
}
```

Podaj lokalny mnożnik i podział Hits, bez testów Rout.

**Expected z eval-v1:** 3×3=9 Hits, top5 i bottom4. Użycie zwykłego2× lub odd Hit bottom byłoby błędne.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF34/right, `/situations/11/evidence/0`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

> • If a Double Depth stack is Shock attacked from a Flank or
> Rear hex, the defender Cohesion Hits are tripled (3x) instead
> of doubled.

Źródło PDF34/right, `/situations/11/evidence/1`, obraz SHA `96e693ff55aa1d5d9a9bcac77f70856696a4e4437c9d51f0bc9aead21feea5b4`.

> • Cohesion Hits from Shock are distributed equally between the
> two units, with any odd Hits going to the top unit. Cohesion Hits
> from Missile Fire Hits apply only to the top unit unless fire is
> through a Rear hex, in which case Hits apply to the bottom unit.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "multiplier": 3,
  "total_Hits": 9,
  "top_Hits": 5,
  "bottom_Hits": 4
}
```

1. R953 effect/parameters says Flank/Rear DD defender Hits tripled insteadofdoubled. Givenbase3 →3×3=9.
2. R953 equalShockallocation withoddHit top →4+4 plusone top =top5,bottom4.
3. R953 interpretation unknown/G953 blocking concerns later retreat/elimination cardinality. Rout is excluded from this requested transformation.

**Porównanie:** Both numerical steps match; unrelated oldSEM-002 does not blanket-block this local question.

**Zależności i blokada:** DD legality and baseHits supplied. No8.43/CRT/Rout procedure or missing eligibility list needed for the requested multiplier/split.

**Wyłączenia:** Any Rout/TQ/retreat outcome, realeligibility, and closure of oldelimination ambiguity.

`/rules/21/transcription`, bajty[285370,285717); SHA `45b6786bc3c1a91814ce5fd1c5de6b950c2aa5eaa771d19eddd79c3df5bd9b7c`.

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

`/rules/21/interpretation`, bajty[285743,286047); SHA `ca7886b71fdbd09be688460e75d739f02e2e0f84f973ddf1ee78f334f5380d52`.

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

`/rules/21/conditions`, bajty[286069,286267); SHA `1a3cf41cfaa6b103ff192bf058a6e610a4eeea507a0498e9b2dabd18d97f60be`.

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

`/rules/21/action_effect`, bajty[286292,287054); SHA `837e3578f5bce810fe97234129e5e97b37ec99cbea657ae2afba5bf6d5397c8d`.

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

`/rules/21/exceptions`, bajty[287076,287387); SHA `79b3d4464601eaf75f247f40155216e957d60a2da96cdbeef5ffa93dd38fe9eb`.

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

`/rules/21/parameters`, bajty[287409,289709); SHA `1e867c73f0caa58306ed010207556b4a711b15aabeea535534362d76692a5abd`.

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

`/rules/21/time_limits`, bajty[290202,290441); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/gaps/2/reason`, bajty[530303,530470); SHA `793a6f10361f2dab15c7e8a9c98ec66ff8ead63a9d165592916068045ec8285a`.

```json
"The shared-rout paragraph uses singular “the unit” when separate retreat hexes are impossible; it does not explicitly identify one or both units for elimination."
```

`/gaps/2/needed_context`, bajty[530496,530594); SHA `30112f794a63449d7b32cc5166cfc322e165f59a4da1dd5e9e4aefbed65bf6e9`.

```json
"Clarification of elimination scope when only part/all of stack cannot retreat to separate hexes."
```

`/gaps/2/blocking`, bajty[530614,530618); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "multiplier": 3,
  "total_Hits": 9,
  "top_Hits": 5,
  "bottom_Hits": 4
}
```

1. R953 effect/parameters says Flank/Rear DD defender Hits tripled insteadofdoubled. Givenbase3 →3×3=9.
2. R953 equalShockallocation withoddHit top →4+4 plusone top =top5,bottom4.
3. R953 interpretation unknown/G953 blocking concerns later retreat/elimination cardinality. Rout is excluded from this requested transformation.

**Porównanie:** Both numerical steps match; unrelated oldSEM-002 does not blanket-block this local question.

**Zależności i blokada:** DD legality and baseHits supplied. No8.43/CRT/Rout procedure or missing eligibility list needed for the requested multiplier/split.

**Wyłączenia:** Any Rout/TQ/retreat outcome, realeligibility, and closure of oldelimination ambiguity.

`/rules/21/transcription`, bajty[355950,356307); SHA `ccb8aeabc78fc74c2baebc72d73e41c7e55875e59c17cac93dc89d7d9fe29e49`.

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

`/rules/21/interpretation`, bajty[356334,356646); SHA `1317d664b029ec2465d8b01635ff7c85d228409a9f993b8c5dc367805995989b`.

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

`/rules/21/conditions`, bajty[356669,356877); SHA `5c5e64f2a2a12a819170d6e2e34722cbb2ca87a4b8da96349e2219b5abdd0674`.

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

`/rules/21/action_effect`, bajty[356903,357681); SHA `d7a07810d2e78897ad744ab4dcb6fed2f38e4c6b84ce87f5a8043c120fe974c4`.

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

`/rules/21/exceptions`, bajty[357704,358027); SHA `aae6360bf522c3faae1a011ff8bcb3fe45bdbab898c9e93675079dbd3f5c82d8`.

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

`/rules/21/parameters`, bajty[358050,360439); SHA `882b99334012551ad374b8f24d4121ad9eee252b7586656ec3e129c4336ed448`.

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

`/rules/21/time_limits`, bajty[360956,361201); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/gaps/2/reason`, bajty[614077,614244); SHA `793a6f10361f2dab15c7e8a9c98ec66ff8ead63a9d165592916068045ec8285a`.

```json
"The shared-rout paragraph uses singular “the unit” when separate retreat hexes are impossible; it does not explicitly identify one or both units for elimination."
```

`/gaps/2/needed_context`, bajty[614271,614369); SHA `30112f794a63449d7b32cc5166cfc322e165f59a4da1dd5e9e4aefbed65bf6e9`.

```json
"Clarification of elimination scope when only part/all of stack cannot retreat to separate hexes."
```

`/gaps/2/blocking`, bajty[614390,614394); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

## SIT-13 — Roman stack: order vs facing

### Zamrożone fakty i pytanie

```json
{
  "stack": "Roman units różne border colors",
  "top_TQ": 7,
  "bottom_TQ": 5,
  "order": "LC",
  "requested_actions": [
    "switch top/bottom",
    "change facing"
  ]
}
```

Która akcja spełnia lokalny wymóg order? Jakiego TQ/DRM używa każdy test stosu przed zmianą?

**Expected z eval-v1:** LC nie pozwala switch stacking order; facing może być przez LC. Każda unit własny test zTQ7 top i+1DRM za różne colors. Nie ustalono alokacji Shock Hits.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF35/left, `/situations/12/evidence/0`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.64 Roman Stacking order may be changed/switched only by
> an Individual Order; it may not be part of movement or a Line
> Command, although facing may be changed by LC. If the player
> desires to move only one unit from a stack, only the top unit
> may move.

Źródło PDF35/left, `/situations/12/evidence/1`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.62 Stacked Roman units combine their Size when attacking or
> defending, but all other ratings, especially TQ, are those of the
> top unit. Stacked Romans must Shock attack the same hex; see
> 8.42. Only the top unit may fire. Each unit makes its own TQ
> check but uses the TQ of the top unit. Automatic Cohesion Hits
> (6.68) are applied to each unit in the stack. Cohesion Hits from
> Shock resolution 8.46 Step 4 are allocated per 10.13.

Źródło PDF35/left, `/situations/12/evidence/2`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.63 For stacked Roman units with different border colors, or of
> the same border color and different classes, there is a +1 DRM
> to all TQ checks.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "stack_order_switch_by_LC": false,
  "facing_local_order_requirement_by_LC": true,
  "each_own_TQ_check_uses": 7,
  "DRM_each_check": 1
}
```

1. R964 switch onlyIO, neverLC; facing explicitLCexception → firstaction no, second satisfies localordertype.
2. R962 says each unit separatecheck using topTQ; suppliedtop7,bottom5 → each uses7.
3. R963 differentbordercolors →+1DRM to allTQchecks before requestedchange.

**Porównanie:** All requested localorder/TQ/modifier distinctions match; no allocation inferred.

**Zależności i blokada:** FullLC legality/source parameters or10.13allocation not asked. Values7/5 are synthetic facts, not artworkcertification.

**Wyłączenia:** FullLC eligibility, actualTQ/rating, ShockHitsallocation and actualroll result.

`/rules/23/transcription`, bajty[298538,298900); SHA `8afd0c93037cf4981a30682cc461140852ed3f63e0bfe1d71e393c09ea1e9fc4`.

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

`/rules/23/interpretation`, bajty[298926,299473); SHA `8525f82585463f769350d0976b7e7766bfbc137bebac5c4e66ec7eb47ed3cfce`.

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

`/rules/23/conditions`, bajty[299495,299693); SHA `174d2a08c167131c6c0b435e8259d6abee9c067f4de4cb439b034cbe4da32bcf`.

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

`/rules/23/action_effect`, bajty[299718,300186); SHA `ac1561370c9260de1d2000d67bf9c6208a347755a4b51978ad0ea333b4d49c2a`.

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

`/rules/23/exceptions`, bajty[300208,300456); SHA `44fa0dfbfea13533fdfcb580eb1c4ca9101a967c855bf67141aa53d168dda281`.

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

`/rules/23/parameters`, bajty[300478,300705); SHA `8c5bc554fd00008b23d1bb16aa331d5fafb122092de39dd41074ebdd59a067be`.

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

`/rules/23/time_limits`, bajty[301166,301405); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/24/transcription`, bajty[302416,302748); SHA `13d8541dddcc73ea8349079037ef68585043100a8b2170d88048dac0f220e10d`.

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

`/rules/24/interpretation`, bajty[302774,303033); SHA `7603bb08c7c4fa66d793c9bc81ea23f1ec56493a843b679deb4a7fb95ae5bf12`.

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

`/rules/24/conditions`, bajty[303055,303320); SHA `dd34b9d0f113c3110ede9cd2554c57e5bcdd74182e60fcef72c2480f04f22aaa`.

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

`/rules/24/action_effect`, bajty[303345,303525); SHA `72920e3c2433f52d080aca2158d2874b9e06821c721f74811cf484fbfa0c29d6`.

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

`/rules/24/exceptions`, bajty[303547,303795); SHA `d69fc68ceb3506b624857fb2a1eda0990bf04d93dede7ead03a9398746acc988`.

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

`/rules/24/parameters`, bajty[303817,304458); SHA `dc3291299671c64338f5803680c68878b53cc290a6b63ef1533710ff4b0ae00c`.

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

`/rules/24/time_limits`, bajty[304919,305158); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/25/transcription`, bajty[306393,306775); SHA `5e25642ffb1b0ea68f103443f5d537dd5dd7332cfa94b594c6ac14b8a5c4003e`.

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

`/rules/25/interpretation`, bajty[306801,307239); SHA `b0b9ed80d9b04a2c36a9b4a0ec8035436aee04588b8691fc28aecdda4b1940e5`.

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

`/rules/25/conditions`, bajty[307261,307488); SHA `30eca96d0053e18561360c192cea298a5067d89abf06b1f08b0f654482d829f8`.

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

`/rules/25/action_effect`, bajty[307513,307872); SHA `d13e119b2555c688cb3d2cfe0ceb96a08686ec5f1c08e4b0e9a0799db80ceffc`.

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

`/rules/25/exceptions`, bajty[307894,308134); SHA `6718bcd303f810e91c5da9377f03e9e3c5765fc7d9fecc72ba64e91fee621be9`.

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

`/rules/25/parameters`, bajty[308156,308383); SHA `9d312925f6f2e6a73b85c3167187bbaf16df97bddd254ded3e09c4d018c7f5bc`.

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

`/rules/25/time_limits`, bajty[308844,309083); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "stack_order_switch_by_LC": false,
  "facing_local_order_requirement_by_LC": true,
  "each_own_TQ_check_uses": 7,
  "DRM_each_check": 1
}
```

1. R964 switch onlyIO, neverLC; facing explicitLCexception → firstaction no, second satisfies localordertype.
2. R962 says each unit separatecheck using topTQ; suppliedtop7,bottom5 → each uses7.
3. R963 differentbordercolors →+1DRM to allTQchecks before requestedchange.

**Porównanie:** All requested localorder/TQ/modifier distinctions match; no allocation inferred.

**Zależności i blokada:** FullLC legality/source parameters or10.13allocation not asked. Values7/5 are synthetic facts, not artworkcertification.

**Wyłączenia:** FullLC eligibility, actualTQ/rating, ShockHitsallocation and actualroll result.

`/rules/23/transcription`, bajty[369591,369963); SHA `ec22b386e3b74894a8f51b78150e5a38df0bc7afd1586691643e38563d3f7759`.

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

`/rules/23/interpretation`, bajty[369990,370550); SHA `c3746d5bd4c8cb03fa208473e7df21637f3627f5cee89d0fdcc73f21e674209f`.

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

`/rules/23/conditions`, bajty[370573,370781); SHA `9cc6bc8ad287a11e3fca0e963c0358222f23425eaa2dcb91f1476a72a081f18e`.

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

`/rules/23/action_effect`, bajty[370807,371288); SHA `fb79ed540f2e6d645af5b7865d688639d9ac7851c4c5062687fec0c62ca24f6c`.

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

`/rules/23/exceptions`, bajty[371311,371567); SHA `d3cc4743b10bde442e63ebed8dc2fb6f8197dc66b6d7ba64213aea7e6e247dac`.

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

`/rules/23/parameters`, bajty[371590,371825); SHA `eb273e3893388f0ef6581f21cd8ac1a6af16a3d7cb08bce59ac4760de1212072`.

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

`/rules/23/time_limits`, bajty[372309,372554); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/24/transcription`, bajty[373608,373950); SHA `282584e2ad62f763c74abd538185073e9811cd377b4dfc4b9769d8de2a922833`.

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

`/rules/24/interpretation`, bajty[373977,374244); SHA `015b13694ff208709748fc12c6c35c92f4f929740660a8f3d902a522914d68b6`.

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

`/rules/24/conditions`, bajty[374267,374542); SHA `66559a4558cbff06aba8f986f6b4dc8c3ef9c4c4fe52c47d7b253b7ed5a12a12`.

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

`/rules/24/action_effect`, bajty[374568,374756); SHA `5e1276e9c90d0d24d3ec1b1a401280185ef11ba9f021601f5f63b6d2c22a6816`.

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

`/rules/24/exceptions`, bajty[374779,375035); SHA `9642e7c43dd87908e1378733ca99880f42eb948f085e101dc81850bb62933a98`.

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

`/rules/24/parameters`, bajty[375058,375724); SHA `feb843ecfa75510022e92a145782579a8d6c8799f63731c42d1bed4d93a811fe`.

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

`/rules/24/time_limits`, bajty[376208,376453); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/25/transcription`, bajty[377738,378130); SHA `523734912f5eb746aa7baad9ca41f15a04bd7128c084c8ea656388d5d1cf87b9`.

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

`/rules/25/interpretation`, bajty[378157,378607); SHA `696121fb75a87526e0e161911b0a8d4774d3dc3fa58ce7789b9c99bff0962ee7`.

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

`/rules/25/conditions`, bajty[378630,378865); SHA `01deb7f002968fdd4d0544150575e32f888cadc850118e3d4d7b63de017e8b32`.

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

`/rules/25/action_effect`, bajty[378891,379262); SHA `808f6df39988e3c0316a49b6d43ef56a23d7639eb38ab1c2d9b37c397dcc887c`.

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

`/rules/25/exceptions`, bajty[379285,379535); SHA `4f89f764ab2dadacbc0969721f8d66e7d3e525a68578809c9f762f48956cd2ba`.

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

`/rules/25/parameters`, bajty[379558,379793); SHA `93e20ee615211e9ea17f459efa7aa064f39d6d3b65274dfedda4116244221215`.

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

`/rules/25/time_limits`, bajty[380277,380522); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

## SIT-14 — MLE: wymagania heksu i orientacja

### Zamrożone fakty i pytanie

```json
{
  "line": "Roman stacks same Line established",
  "order": "eligible LC",
  "column": false,
  "destination_variants": [
    "vacant Clear outside enemy ZOC",
    "occupied Clear",
    "vacant non-Clear",
    "vacant Clear in enemy ZOC"
  ]
}
```

Porównaj lokalne warunki MLE i facing; czy można złożyć stos odwracając diagram?

**Expected z eval-v1:** Tylko pierwszy destination spełnia lokalne warunki; top sideways, facing zachowany, po LC obie units mogą move zMA−2, brak Hits za MLE. Pozostałe trzy destinations zabronione. Odwrócenie diagramu nie daje prawa stacking together.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF35/left, `/situations/13/evidence/0`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal.

Źródło PDF35/right, `/situations/13/evidence/1`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.66 Manipular Line Extension: Stacked Roman units with
> unoccupied flank hexes can extend their line as part of a Line
> Command or in reaction to enemy movement, instead of using
> Orderly Withdrawal.

Źródło PDF35/left, `/situations/13/evidence/2`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)
> may move sideways into the vacant flank hexes (see the diagram
> above).

Źródło PDF35/right, `/situations/13/evidence/3`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> To undertake Manipular Line Extension
> (MLE), all the top units in the stacks in the same Line (see 4.32)
> may move sideways into the vacant flank hexes (see the diagram
> above).

Źródło PDF35/left, `/situations/13/evidence/4`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex.

Źródło PDF35/right, `/situations/13/evidence/5`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> If a Flank hex is occupied, MLE cannot be used to place
> a unit in that hex.

Źródło PDF35/left, `/situations/13/evidence/6`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> The hex entered by MLE must be Clear and
> not in an enemy ZOC.

Źródło PDF35/right, `/situations/13/evidence/7`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> The hex entered by MLE must be Clear and
> not in an enemy ZOC.

Źródło PDF35/left, `/situations/13/evidence/8`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> Facing remains the same.

Źródło PDF35/right, `/situations/13/evidence/9`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> Facing remains the same.

Źródło PDF35/left, `/situations/13/evidence/10`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF35/right, `/situations/13/evidence/11`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> This rule only
> applies to unstacking the units; it does not apply to stacking
> them together.

Źródło PDF35/left, `/situations/13/evidence/12`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

Źródło PDF35/right, `/situations/13/evidence/13`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.68 Manipular Line Extension may also be undertaken as part
> of a Line Command (only). If undertaken as an LC, both units
> may move after the MLE but with their MA reduced by 2. There
> are no Cohesion Hits applied for the MLE. Units in Column may
> not use MLE.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "destination_local_validity": [
    true,
    false,
    false,
    false
  ],
  "moving_unit": "top sideways",
  "facing": "unchanged",
  "LC_post_MLE": "both maymove withMA−2",
  "MLE_Hits": 0,
  "reverse_diagram_stacking_permission": false
}
```

1. R966 requires vacantflank+Clear+notenemyZOC. Only firstdestination has all three; otherthree each violates a statedcondition.
2. R966 topunit moves sideways withfacingunchanged; onlyunstacking, no stacking together from reversing artwork.
3. EligibleLC/nonColumn supplied; R968 bothmaymoveafter withMA−2 and0CohesionHits forMLE.

**Porównanie:** All four destinations and remaininglocalconclusions match.

**Zależności i blokada:** SameLine/LC/ZOC supplied, so missingrealdefinitions do not block these predicates. Diagram supports direction/layout without providing realratings.

**Wyłączenia:** Actual MA/TQ fromdiagram, actualroutes/LC/fullZOC and stackingpermission beyondunstacking.

`/rules/27/transcription`, bajty[314251,314702); SHA `815b434bdf198b1872fc31b833239429274df555c8547636c8d7c3f3a2783ec5`.

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

`/rules/27/interpretation`, bajty[314728,315227); SHA `07e7a881d584e5c779ad1c7dd62211c88c0cd9dde0ae904361d3d3580e0fb559`.

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

`/rules/27/conditions`, bajty[315249,315553); SHA `46c642c862bf4b4a052e72243cdffe152a2200a9d354991e56ae63d28c8887c3`.

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

`/rules/27/action_effect`, bajty[315578,315998); SHA `a67aa59c5cb951426dc0d4c8487d202a36316d2bb4a75e72d08e5f185f7236b7`.

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

`/rules/27/exceptions`, bajty[316020,316306); SHA `f3ce14caa3b77062bf5fa83b10e70bdf1349965e6f136f00e21fc944549250d3`.

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

`/rules/27/parameters`, bajty[316328,316575); SHA `ab75a0f31cbf79a61e1e50a675e32054a7e9b8f098ae3aca33bca0767f7c8e05`.

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

`/rules/27/time_limits`, bajty[317112,317343); SHA `64d693cff5535f1962c8f496e7ce9ee599dac116483338e1cc155c0ed01da30a`.

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

`/rules/29/transcription`, bajty[323257,323601); SHA `b9ea5038c6a225c04b28f0a6c66ba7acde40655d85e59655671948e6fa9347ee`.

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

`/rules/29/interpretation`, bajty[323627,324041); SHA `4978c53d8691f7158bd8efb6d9c6fd36f4af2e44a76bda6af9f6f645f3a18bf7`.

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

`/rules/29/conditions`, bajty[324063,324290); SHA `41b3f6ae007fc3108cbeed0c02197789f74c868ef4e2d0c1807dbdfb6879072e`.

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

`/rules/29/action_effect`, bajty[324315,324650); SHA `cadd7f3fc1a9e4e146ec097dd6ca201a190a3526e8f5e2ccb73ab0eb5dda6076`.

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

`/rules/29/exceptions`, bajty[324672,324875); SHA `aee9a5b665f28362fb9af475926ed06369fbad6ff865c4e3c7fb53c07fc4e420`.

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

`/rules/29/parameters`, bajty[324897,325940); SHA `22161e7fe52c6654804d611d526167df99520cab5764161d552fca5c7c46c76a`.

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

`/rules/29/time_limits`, bajty[326423,326637); SHA `36820d74f828f1d587b54cc2c419b8523af449ea2fefdc1e7f5ce5f2581059ae`.

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

`/nodes/7/content`, bajty[129317,130225); SHA `e2d70f9ee7568729c4ba4a2f7ff87a2edc9b64bd0f95e1b53ab03132ec8be207`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "destination_local_validity": [
    true,
    false,
    false,
    false
  ],
  "moving_unit": "top sideways",
  "facing": "unchanged",
  "LC_post_MLE": "both maymove withMA−2",
  "MLE_Hits": 0,
  "reverse_diagram_stacking_permission": false
}
```

1. R966 requires vacantflank+Clear+notenemyZOC. Only firstdestination has all three; otherthree each violates a statedcondition.
2. R966 topunit moves sideways withfacingunchanged; onlyunstacking, no stacking together from reversing artwork.
3. EligibleLC/nonColumn supplied; R968 bothmaymoveafter withMA−2 and0CohesionHits forMLE.

**Porównanie:** All four destinations and remaininglocalconclusions match.

**Zależności i blokada:** SameLine/LC/ZOC supplied, so missingrealdefinitions do not block these predicates. Diagram supports direction/layout without providing realratings.

**Wyłączenia:** Actual MA/TQ fromdiagram, actualroutes/LC/fullZOC and stackingpermission beyondunstacking.

`/rules/27/transcription`, bajty[385881,386344); SHA `5db7fa5a257c9bfb0a107a04338ccba0329d5cd50d7c58c2df69fa4af6c9fb7b`.

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

`/rules/27/interpretation`, bajty[386371,386883); SHA `980e77c707fc284fda7d5c3d85faf1901a9e2394d5fa309f836245022bd1da86`.

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

`/rules/27/conditions`, bajty[386906,387222); SHA `63690cd0a5843202df0dfca2b59f2f0bf33f24348a2a58d963385ea6918199f8`.

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

`/rules/27/action_effect`, bajty[387248,387681); SHA `e09386fba9852efc3cec16fe08ab42be1324ffdc06c9c068141337ea35dce6ba`.

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

`/rules/27/exceptions`, bajty[387704,388002); SHA `88c2576f1a1154395c60d559a427b730b564c5d04cbf2c0397855cfb9c9aacfc`.

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

`/rules/27/parameters`, bajty[388025,388281); SHA `774278c4533f8565f40d4177052d5c48ca7f0ec87a6295878dd4627c755fccb7`.

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

`/rules/27/time_limits`, bajty[388844,389086); SHA `eeffeb974e0909fd90581224a76337abe1d148b5420530987d8ba478b1839e87`.

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

`/rules/29/transcription`, bajty[395227,395581); SHA `0c7240fad3d7dbb60f057de5db3209f3203f1b2ae4f875a20d0fd2912a74c577`.

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

`/rules/29/interpretation`, bajty[395608,396034); SHA `dc29372e1e91a0989422735fa25f162a6b0562c298e72ada628897142f332b95`.

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

`/rules/29/conditions`, bajty[396057,396292); SHA `9820b22f6997841feb202c1aeaf8e75ac344c0d27dbd6b394bbbcc85f1ce9813`.

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

`/rules/29/action_effect`, bajty[396318,396665); SHA `01ac6e56bb2fb44cde248456a5ef224225ea5e7f9a6e25df010272cdfe90d280`.

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

`/rules/29/exceptions`, bajty[396688,396901); SHA `640b0cf0b1ae359447e74493cc337d36e73a471411618075c10c52d7fd6400c4`.

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

`/rules/29/parameters`, bajty[396924,398008); SHA `a133c79454bf50df630ba6a2594381ec34f84dbf72044765d4f526f004e35576`.

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

`/rules/29/time_limits`, bajty[398515,398739); SHA `a755e652413b09e08b55402d5ae9bffa9cafb79c35a00a783d188e3c52156c05`.

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

`/nodes/7/content`, bajty[177636,178570); SHA `3076b275acddd17023726140d84abeef0bef017b3551be7bfae1f1679085a809`.

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

## SIT-15 — MLE i OW na jednym triggerze

### Zamrożone fakty i pytanie

```json
{
  "enemy_move": "combat unit wchodzi w2 heksy",
  "both_triggers_established": true,
  "MLE_and_OW_same_units": true
}
```

Czy te same units mogą wykonać obie reakcje? Czy zaniechanie pierwszej okazji kasuje następne?

**Expected z eval-v1:** Te same units nie mogą wykonać obu. Różne units mogą przy spełnionych warunkach; odmowa wcześniejszej okazji nie kasuje późniejszych MLE triggers.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF35/right, `/situations/14/evidence/0`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.67 Manipular Line Extension may be undertaken as a reaction
> to enemy movement the instant an enemy combat unit comes
> within 2 hexes of a line of stacked Roman units. The Roman
> player may make his choice at any time any enemy unit so places
> itself (that is, he does not have to exercise his MLE rights the first
> time they become available). If enemy movement triggers both
> Orderly Withdrawal as well as MLE, both may be undertaken
> together but not by the same units.

Źródło PDF35/right, `/situations/14/evidence/1`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> EXAMPLE: A Velites unit sitting between two Hastati stacks may
> withdraw through the gaps in a Hastati line upon approach of,
> say, an enemy Phalanx and, as soon as that unit is through the
> gap, the Hastati line may undergo MLE.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "same_units_MLE_and_OW": false,
  "different_units_both_if_triggers": true,
  "decline_first_MLE_loses_later_opportunities": false
}
```

1. R967 literal says bothtogether butnotsameunits; suppliedsameunits=true → cannotperformboth.
2. Withdifferentunits andbothtriggersestablished they maycoexist; N967ex illustrates that separation.
3. R967 timing says can defer to laterqualifyingapproach, not compulsoryfirstopportunity.

**Porównanie:** Matches recipient and timing distinctions.

**Zależności i blokada:** Bothtriggers are supplied. GeneralOW need not be executed to answer the localcoexistence prohibition.

**Wyłączenia:** FullOW paths, newtriggergeometries and anypermission without bothqualifyingtriggers.

`/rules/28/transcription`, bajty[318631,318986); SHA `db6d794c69487e6188a8253be54dbd9c1f16347126201e3d8a014da85bad6012`.

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

`/rules/28/interpretation`, bajty[319012,319457); SHA `95dd7f3ed8ed7c760af5db00c31d83162e6eca8fc68b54d4d7e5f2c9f1ea4a29`.

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

`/rules/28/conditions`, bajty[319479,319718); SHA `6d9c13162303c66d8bc8fbddff37314b811cd91353fffa006796cd1a701c4c15`.

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

`/rules/28/action_effect`, bajty[319743,320109); SHA `33a830a845fcbbc55f576a52c091ded15ede37e995a94e757ce834a7b9378d3e`.

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

`/rules/28/exceptions`, bajty[320131,320351); SHA `d8dd578ca03bc11d476e20584631bc80b215a00d212e37be0c2bbb0c259b6f52`.

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

`/rules/28/parameters`, bajty[320373,321028); SHA `b0400a5a0dd31e2b6ec2ff016a211b711c7e607d5210d7f76c9fe6951a0e98d0`.

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

`/rules/28/time_limits`, bajty[321519,321787); SHA `600230c83ca227270c74a1cae7636dfa258376ed21073423bf3249e6f352fdfc`.

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

`/nodes/8/content`, bajty[130613,131131); SHA `f18edcf65f1f59ec320d51f56cb875fd937a0c94e5a1e65e34e0300cb8a79c50`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "same_units_MLE_and_OW": false,
  "different_units_both_if_triggers": true,
  "decline_first_MLE_loses_later_opportunities": false
}
```

1. R967 literal says bothtogether butnotsameunits; suppliedsameunits=true → cannotperformboth.
2. Withdifferentunits andbothtriggersestablished they maycoexist; N967ex illustrates that separation.
3. R967 timing says can defer to laterqualifyingapproach, not compulsoryfirstopportunity.

**Porównanie:** Matches recipient and timing distinctions.

**Zależności i blokada:** Bothtriggers are supplied. GeneralOW need not be executed to answer the localcoexistence prohibition.

**Wyłączenia:** FullOW paths, newtriggergeometries and anypermission without bothqualifyingtriggers.

`/rules/28/transcription`, bajty[390426,390791); SHA `722b85d19abb1f00d39f83472c526249c5d1b0541635703840c5c2053424867d`.

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

`/rules/28/interpretation`, bajty[390818,391274); SHA `11e89b79cceb3c478b0433734fbab94a70c7037bc14836ccd8949df87fecd827`.

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

`/rules/28/conditions`, bajty[391297,391546); SHA `d75bdefffd7d6adf1502d334f33a4d6f3da568898b420e3a55f596a9d25ff7b2`.

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

`/rules/28/action_effect`, bajty[391572,391949); SHA `47ff5bb1b83c8dac4294f767a8c4daecaae2cd3e289a44f59b4f62495fb16017`.

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

`/rules/28/exceptions`, bajty[391972,392202); SHA `7e64a4ff354fb165ec0aa8592cd04f7b84defee21dd00ca7481a6067b348e5ee`.

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

`/rules/28/parameters`, bajty[392225,392905); SHA `ffb3e9e6d50c0aabc41bf3893fdab69034d476ebb2f8eacacd605bae273cdb77`.

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

`/rules/28/time_limits`, bajty[393420,393698); SHA `d64d6473fd9590b02d1584e6253ec451195168b52e473aab74c0493256b5cc4f`.

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

`/nodes/8/content`, bajty[178977,179506); SHA `ebcfba1c842534a71a78fa6a4b05ef25d5de482adf363ec3b271bca22d1b4150`.

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

## SIT-16 — Triarii: próg zaokrąglony i wyjątek bez ruchu

### Zamrożone fakty i pytanie

```json
{
  "doctrine_applicable": "synthetic:Romans218BCE, Scipio nie OC",
  "AWL": 11,
  "RP_variants": [
    4,
    5
  ],
  "movement_gate_9_71": true,
  "enemy_in_ZOC": true
}
```

Oceń tylko RP gate move+Shock oraz standing Shock; czy RP sam uchyla9.71?

**Expected z eval-v1:** Próg floor(11/2)=5:RP4 nie spełnia move+Shock gate,RP5 spełnia przy podanej bramce9.71. Standing Shock na enemy wZOC możliwy w zakresie9.72 przy obu RP. SamRP5 nie uchyla9.71.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF35/right, `/situations/15/evidence/0`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> This rule must be used with any battle involving Romans that took
> place prior to 200 BCE in which Scipio Africanus is not pres-
> ent as Overall Commander (and, yes, even though, historically,
> Scipio was at Cannae, for game purposes he wasn’t, so use it at
> Cannae).

Źródło PDF35/right, `/situations/15/evidence/1`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.71 Triarii units cannot move, but may change facing, until and
> unless one of the following occurs:

Źródło PDF35/right, `/situations/15/evidence/2`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> • There is an enemy combat unit, other than an Elephant unit,
> which is within 3 hexes and LOS of any unit in the Triarii line,
> or

Źródło PDF35/right, `/situations/15/evidence/3`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> • The Triarii units are at least 6 hexes from all other Roman or
> Ala—but not allied–infantry lines, be they Hastati, Principes
> or whatever.

Źródło PDF35/right, `/situations/15/evidence/4`, obraz SHA `96b9d6d8a64767881ee17ef33519b46fb73078bb1e06d859514f638b8b34d0e7`.

> 9.72 Triarii units cannot move and Shock attack unless and until
> the Roman army has Rout Points equal to at least one-half of
> its Army Withdrawal Level (round down). They may always,
> however, Shock attack (without moving) against enemy units
> in their ZOC.

### first-001 — unassessed / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "threshold_RoutPoints": 5,
  "RP4_meets_9_72_gate": false,
  "RP5_meets_9_72_gate": true,
  "stationary_Shock_with_given_enemy_ZOC_at_RP4_and_RP5": [
    true,
    true
  ],
  "whole_required_combination_conclusion": "held; no owner choice for omitted explicit9.71 linkage"
}
```

1. R972 parameter >=floor(AWL/2), givenAWL11 →floor5.5=5; RP4 fails,RP5 meets.
2. R972 exception permits stationaryShock againstenemy inownZOC; suppliedenemyZOCtrue → bothRPvariants permit that localexception.
3. R971 movementgate is suppliedtrue for concreteRP5variant; no realLOS/AWL/RP derived.
4. Required lastquestion RP-alone doesnotwaive9.71 reaches oldEXP-052/SEM-011: rules are separatelypresent but explicitcoupling/DEP-NEW-001 is absent. Do not choose wholecombination representation sufficiency for owner.
5. Allpartial numeric/exceptionconclusions retained; oneSIT remains unassessed for complete frozenquestion, not a wronglycomputed threshold or missingactualscenario source.

**Porównanie:** Localcomponents match but completequestion is held for oldcombination interpretation; no fractionalsuccess or forcedclosure.

**Zależności i blokada:** MissingseparateDEP-NEW-001 is structural; not automaticFN. Supplied9.71gate/11AWL/RP/ZOC avoid actualsetupblocks. The heldpart is representationalcombination.

**Wyłączenia:** OldTriarii variant decision, generalattacklegality, realScipio/date/AWL/RP/LOS/ZOC and newgoldedge.

`/rules/30/transcription`, bajty[327674,327994); SHA `b6e40cb57e29b43b6fb8510b876a8197c29904b934b89776bc867c1371b41aa6`.

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

`/rules/30/interpretation`, bajty[328020,328392); SHA `783920739f34e4ebdf927351507bbaf432ed52289b82747ff7f8c4cc065a72bf`.

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

`/rules/30/conditions`, bajty[328414,328669); SHA `831be476dc9bf3ce343310e3b56042cb2b047212f69aeb612897b07e9bc1818c`.

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

`/rules/30/action_effect`, bajty[328694,328987); SHA `63c43660902c1b91db40779c2a82fcad7b78ce11728f538ce6b3a484fc03909c`.

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

`/rules/30/exceptions`, bajty[329009,329258); SHA `7f05ef48ca2d4d4d7d441722269117d57f489f4c1d42ce8c27db6f86d80aaf1c`.

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

`/rules/30/parameters`, bajty[329280,329940); SHA `1d86a8f2ddb43d85e4ee968b76b00f06c655435788e79aff3119ba3e18b5097f`.

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

`/rules/30/time_limits`, bajty[330516,330755); SHA `24428a9d506d383b0f95237e731dfac1dc2c25a7e02d659f83b0861ab72fa78d`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/31/transcription`, bajty[332069,332461); SHA `56ef54fc1769f8972bb775a053d4723b883568a7654c339eca370bbf7a8fd73c`.

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

`/rules/31/interpretation`, bajty[332487,332801); SHA `cf9265dea9aa67cfd7058cfcb52f8f6a9282af2ddaa0a72055afa0b31d833e95`.

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

`/rules/31/conditions`, bajty[332823,333217); SHA `691344268dd16ab929850020a20c63a21fc0659b07680e82b2a0a14398b0adf9`.

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

`/rules/31/action_effect`, bajty[333242,333477); SHA `7f90da4e28cbc5185659dc4dde25d1d41e0f201f74e47d995232b46f8d063e00`.

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

`/rules/31/exceptions`, bajty[333499,333825); SHA `f371cd9bc9d3f532a744e5245be1daa65747acf115186910571cc8baa1be974a`.

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

`/rules/31/parameters`, bajty[333847,334928); SHA `b0366e0a499ef526da8030db8d33665e0e3f369abe4c0d1c1639364636e0edf6`.

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

`/rules/31/time_limits`, bajty[335493,335710); SHA `8091f196bcf5298968c522b05c51b94b5dba07221481f65be9a0fb2a4b5662db`.

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

`/rules/32/transcription`, bajty[336549,336935); SHA `923d480f3533ecbcb584440b111898aa22dd936e8b48b2c407d8860f4d7e7d0b`.

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

`/rules/32/interpretation`, bajty[336961,337351); SHA `35274a9c35b982ba6e075e5c507df2233827f815fa8430e896e4de4c42979a4f`.

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

`/rules/32/conditions`, bajty[337373,337643); SHA `8e2ab77be1fd9bcd32cb6acc5bbd4e38f33494b790c73f36dc1b0af35cc36751`.

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

`/rules/32/action_effect`, bajty[337668,337979); SHA `9bd173bf776c20d1a95e71ebe5971ac14866fd263db40c1f77a5480b3b7da6d6`.

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

`/rules/32/exceptions`, bajty[338001,338238); SHA `249d8137581b6915f5f784379ddb29673a9788196a3874b3a1e7c4210f8400d8`.

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

`/rules/32/parameters`, bajty[338260,338948); SHA `d630bf1b7e051b22f085966b22cb89a10eeaef0859f2bca75d54c7e17a089a99`.

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

`/rules/32/time_limits`, bajty[339446,339684); SHA `10dfd3071b3f3c7c8603541c4dc24335f42ea8f8d3567d2b33b4a6aa252fab70`.

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

### context-01 — unassessed / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "threshold_RoutPoints": 5,
  "RP4_meets_9_72_gate": false,
  "RP5_meets_9_72_gate": true,
  "stationary_Shock_with_given_enemy_ZOC_at_RP4_and_RP5": [
    true,
    true
  ],
  "whole_required_combination_conclusion": "held; no owner choice for omitted explicit9.71 linkage"
}
```

1. R972 parameter >=floor(AWL/2), givenAWL11 →floor5.5=5; RP4 fails,RP5 meets.
2. R972 exception permits stationaryShock againstenemy inownZOC; suppliedenemyZOCtrue → bothRPvariants permit that localexception.
3. R971 movementgate is suppliedtrue for concreteRP5variant; no realLOS/AWL/RP derived.
4. Required lastquestion RP-alone doesnotwaive9.71 reaches oldEXP-052/SEM-011: rules are separatelypresent but explicitcoupling/DEP-NEW-001 is absent. Do not choose wholecombination representation sufficiency for owner.
5. Allpartial numeric/exceptionconclusions retained; oneSIT remains unassessed for complete frozenquestion, not a wronglycomputed threshold or missingactualscenario source.

**Porównanie:** Localcomponents match but completequestion is held for oldcombination interpretation; no fractionalsuccess or forcedclosure.

**Zależności i blokada:** MissingseparateDEP-NEW-001 is structural; not automaticFN. Supplied9.71gate/11AWL/RP/ZOC avoid actualsetupblocks. The heldpart is representationalcombination.

**Wyłączenia:** OldTriarii variant decision, generalattacklegality, realScipio/date/AWL/RP/LOS/ZOC and newgoldedge.

`/rules/30/transcription`, bajty[399819,400149); SHA `cb5ff66f1c59277ec3df9b5844c25f652584b85e9f3b3b092e2d2bed179e03b7`.

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

`/rules/30/interpretation`, bajty[400176,400556); SHA `1c0b2367e6c53feb87977a5a84dba7df7dc80c9045e8d6a42e2a4ede35c71087`.

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

`/rules/30/conditions`, bajty[400579,400844); SHA `a60c6e5983498b52692cceb791ef1bfcfc870148c6a9d02acadb18bf53862f9c`.

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

`/rules/30/action_effect`, bajty[400870,401171); SHA `242ac1c8a0b218b3dc8d274bf3b98347cd6cb993b5826f22a780186129cf1245`.

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

`/rules/30/exceptions`, bajty[401194,401453); SHA `d3236e36d3cfa615a4f66c4799b0bcbe1c115122b6bbfcc3fcfe7f553e9a7be1`.

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

`/rules/30/parameters`, bajty[401476,402161); SHA `9cbeebf591c4fdc5e49f3aa2850639a9fd660dcc13fd46f54e4bdcd3a954b58a`.

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

`/rules/30/time_limits`, bajty[402762,403007); SHA `b0754e3ed43de4aed2d575fc759c5ceb96297bf6c2ed1859ac3b9ec6a53d6c4e`.

```json
{
  "state": "not_applicable",
  "value": null,
  "evidence_ids": [],
  "reason": "No separate time restriction stated; event timing, if any, is expressed in conditions/action_effect.",
  "gap_ids": []
}
```

`/rules/31/transcription`, bajty[404370,404772); SHA `0f84b0412fa43476fcbc4e8751322ca05ffe5f55432f2dc7d0b4c1a43e868efe`.

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

`/rules/31/interpretation`, bajty[404799,405121); SHA `ad9995174f49f08cca3960758d8b94a057046edd180fbafa0e8121138abe3648`.

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

`/rules/31/conditions`, bajty[405144,405548); SHA `2abb66d53319962445fe5054b05397d74ed2a816ba36c1913bf400c46c66ae8c`.

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

`/rules/31/action_effect`, bajty[405574,405817); SHA `b5ed4d8d7247c8b4648126f14a66b2ec1d43d8c2e5d5b5a83c37547b0b2c37e0`.

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

`/rules/31/exceptions`, bajty[405840,406178); SHA `86ee47d140a0c35312056089c9cf71bc47f0ff69f4a574d45a921a6869006cb4`.

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

`/rules/31/parameters`, bajty[406201,407323); SHA `17a93eb002e3c0ff26cf52639198b6f0f715f5d3a71808419d302f0e16f55c7c`.

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

`/rules/31/time_limits`, bajty[407914,408141); SHA `9388066ed7834bae8b796d8bf07afbebe688929a90e5b7efb745f7a930c64066`.

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

`/rules/32/transcription`, bajty[409015,409411); SHA `36d46ef4e0c3bbf26ccfc728a38748255b45b83da62f88c9a35929f7d6ba7fef`.

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

`/rules/32/interpretation`, bajty[409438,409839); SHA `0fbced2b400ed37d71af8c33e89843a55cadc7662ee814127db95cf8602d8cea`.

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

`/rules/32/conditions`, bajty[409862,410142); SHA `194e3b45478bb22bb070cf15377967012e4dcfd81ffca0a6a24c2ee3f68940c2`.

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

`/rules/32/action_effect`, bajty[410168,410490); SHA `dd827feffdd61f2e899a010850544f4ae26fd8792958b26a04bb4b243fc92dc3`.

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

`/rules/32/exceptions`, bajty[410513,410760); SHA `94781379ea7b07e44df63eec2e85efeab8deb8d57d506641febdcb82fe370755`.

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

`/rules/32/parameters`, bajty[410783,411496); SHA `ec6be990608b9d4a1c364e4a5d16f60f135e4d061ebb2475176bb0b0bbae7adf`.

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

`/rules/32/time_limits`, bajty[412019,412267); SHA `9b90f8b9e12ad998c4d1e5c2e46997a6f5a49786430fbb067d8e7241011aadf8`.

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

## SIT-17 — Scorpio: mode lock i dwa różne limity ognia

### Zamrożone fakty i pytanie

```json
{
  "variants": [
    {
      "mode_switch": "Move→Fire wtej phase",
      "active_shots_this_turn": 0
    },
    {
      "mode": "Fire bez switch",
      "active_shots_this_turn": 1,
      "active_shots_this_phase": 0
    },
    {
      "mode": "Fire bez switch",
      "active_shots_this_turn": 2
    },
    {
      "mode": "Fire",
      "enemy_phase": "nowa",
      "reaction_shots_this_phase": 1
    }
  ],
  "other_shot_conditions": "supplied legal range/LOS/target; target nie Rampaging EL"
}
```

Oceń lokalne prawo do następnego strzału i recovery po nim.

**Expected z eval-v1:** Po switch doFire brak strzału wtej phase mimo no orders. W drugiej wersji jeden active shot dostępny, marker Finished i brak recovery wphase. Przy2 active wturn brak następnego active. Nowa enemy phase ma odrębny cap2reaction, po1 dostępny jeszcze1, bez ordinary RF8.2.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF36/left, `/situations/16/evidence/0`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.82 A Scorpio is in either Fire or Move mode. It requires an
> Individual Order from any friendly leader to change its mode.
> Scorpios in Move mode cannot fire, and conversely, cannot
> move in Fire mode. A Scorpio that has had its mode changed to
> Move cannot move in that Orders Phase, nor can a Scorpio that
> has had its mode switched to Fire, fire in that Orders Phase. A
> Scorpio unit in Move mode requires an Individual Order from
> any friendly leader to move. Scorpio units do not need orders to
> fire (see 9.85 below).

Źródło PDF36/left, `/situations/16/evidence/1`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

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

Źródło PDF36/left, `/situations/16/evidence/2`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> 9.86 Reaction Fire: Scorpios may fire twice per enemy Orders
> Phase at any time during the enemy Movement and Missile Seg-
> ment—and we mean “any”; they may fire even during enemy
> movement! The first time the Scorpio unit fires, place
> a REACTION FIRE ONCE marker on it. The second
> time it fires, flip the marker to its REACTION FIRE
> FINISHED side. Scorpios, however, cannot use any
> type of ordinary Reaction Fire (8.2).

Źródło PDF36/left, `/situations/16/evidence/3`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

Źródło PDF36/left, `/situations/16/evidence/4`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "next_shot_local_permission": [
    false,
    true,
    false,
    true
  ],
  "second_active_marker": "Finished",
  "recovery_after_that_active_shot": false,
  "second_reaction_marker": "Finished",
  "ordinary_RF_8_2": false
}
```

1. R982 samphase switchtoFire blocksfiring despite noordersrequirement →variant1false.
2. R985 caps2/GameTurn and1/friendlyOrdersPhase;1previousactive/0thisphase →oneallowed, secondactive Finished and nootheraction/recovery thisphase.
3. 2active already thisturn →noadditionalactive.
4. R986 newenemyphase owncap2;1reaction already →oneadditionalreaction, flipFinished; noordinaryReactionFire8.2.
5. NoactivefireRecoveryprohibition is silently transferred to specialreaction; no independentright to Recovery duringenemyphase inferred beyond expectedscope.

**Porównanie:** All requiredfourvariant permissions,activeRecovery andmarker distinctions match.

**Zależności i blokada:** Range/LOS/target supplied; target expressly notRampagingEL, so missingDEP-NEW-003 is not exercised here. The originalstructural omission remains.

**Wyłączenia:** Realhitlookup, ordinaryRFprocedure, Recoveryrules outsideactivephaseban, and Rampageinteraction for excludedtarget.

`/rules/34/transcription`, bajty[345296,345651); SHA `a33422d92d6b503af6010daff3255fe01fe05210014dab1ba9a48db0777ad2e6`.

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

`/rules/34/interpretation`, bajty[345677,346292); SHA `8fdf6862151614f419f7a8295c53c7e22e1737a596e73c9266715f9d0c284cc6`.

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

`/rules/34/conditions`, bajty[346314,346541); SHA `894c24cc9cabfeac3d350722c7f067980a83a819e2c45049cfb0562faab6bdc4`.

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

`/rules/34/action_effect`, bajty[346566,347102); SHA `3471bd807913e91115a671617608912125cb753434b3e22f786113c4bee88a49`.

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

`/rules/34/exceptions`, bajty[347124,347326); SHA `2ba601d60b884a3f88d7002c7e0c0251d55b21998907f0ed9f59f0aff873b4d7`.

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

`/rules/34/parameters`, bajty[347348,348390); SHA `9db4fa2d859dc38f6c382f83ecf588fb7b81f3aaa6afc9c73056b20fee0d2c5d`.

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

`/rules/34/time_limits`, bajty[348872,349110); SHA `da37ba0e548bd429c02621f42caa46037488a158ef3fa11df8affe4223cad279`.

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

`/rules/38/transcription`, bajty[360632,360968); SHA `217e908673bf9e3b3a73eb7ac1d327c335ef7d7a657dbe72594e08591d908f69`.

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

`/rules/38/interpretation`, bajty[360994,361546); SHA `80d54dbcf28bf0ab19c6ee9564a08d8da82afd74bb496610952754753da02905`.

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

`/rules/38/conditions`, bajty[361568,361839); SHA `eb15169e078a3484c47b37efbb4d903ab4729d284e9204b12b580aeb1cd42219`.

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

`/rules/38/action_effect`, bajty[361864,362337); SHA `fde8bab7ff827f510123b26ca91143ecfc2a44a0bf93900c8e54f4d5103307ee`.

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

`/rules/38/exceptions`, bajty[362359,362607); SHA `fc16d2de5ca7db5f3d69122d6057730135f62812268b02b3c17a5f0a86aec720`.

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

`/rules/38/parameters`, bajty[362629,363685); SHA `29900cabc9f67bafca31dbfd918ae945cd5eb86eb0ab577943b3acd403a4914b`.

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

`/rules/38/time_limits`, bajty[364134,364501); SHA `5685d3eeacb4ed76b154c961e369821a7632fd45607a4111b45bf8fda78ffb0b`.

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

`/rules/39/transcription`, bajty[365715,366083); SHA `f340263de56e53936fb05f198154b7099c68f6601770cc84cf4f74cc44cfa0cd`.

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

`/rules/39/interpretation`, bajty[366109,366603); SHA `70c02b78a4a5d40573357d1e77404985359457e6642307bc4d4029af7f84b0aa`.

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

`/rules/39/conditions`, bajty[366625,366884); SHA `fbb30aa6cb47b42b6b0a715df606bdbab0bbc1f993b0c5316a5d76fd7b2864f9`.

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

`/rules/39/action_effect`, bajty[366909,367324); SHA `6b4779b43a06edaed06ae53a43208bd3c6aa539d56ee8977fb85d3efe10896c7`.

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

`/rules/39/exceptions`, bajty[367346,367594); SHA `a6ae04e894f910071142138472464062c0b1480f9b2c549768fbf0fae6136ea2`.

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

`/rules/39/parameters`, bajty[367616,368282); SHA `e3585bf37e853b97f92910414aa0c5b3dba14305e93eef0f9f3214dcde115a6e`.

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

`/rules/39/time_limits`, bajty[368731,368982); SHA `57fd7fcaf42e5fa67e3901dedc6cee8fec1332cacfbe3d0a7b69b8febbb2d522`.

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

`/nodes/34/content`, bajty[150949,151336); SHA `7a033fc7880c2cf6072fcb99cd9b9afa944bcb309e1df0c50b241deece2ff221`.

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

`/nodes/35/content`, bajty[151746,152068); SHA `b787048f35c79258814ee4b32c56168f76e3eb24113b0f84198df4399f46e151`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "next_shot_local_permission": [
    false,
    true,
    false,
    true
  ],
  "second_active_marker": "Finished",
  "recovery_after_that_active_shot": false,
  "second_reaction_marker": "Finished",
  "ordinary_RF_8_2": false
}
```

1. R982 samphase switchtoFire blocksfiring despite noordersrequirement →variant1false.
2. R985 caps2/GameTurn and1/friendlyOrdersPhase;1previousactive/0thisphase →oneallowed, secondactive Finished and nootheraction/recovery thisphase.
3. 2active already thisturn →noadditionalactive.
4. R986 newenemyphase owncap2;1reaction already →oneadditionalreaction, flipFinished; noordinaryReactionFire8.2.
5. NoactivefireRecoveryprohibition is silently transferred to specialreaction; no independentright to Recovery duringenemyphase inferred beyond expectedscope.

**Porównanie:** All requiredfourvariant permissions,activeRecovery andmarker distinctions match.

**Zależności i blokada:** Range/LOS/target supplied; target expressly notRampagingEL, so missingDEP-NEW-003 is not exercised here. The originalstructural omission remains.

**Wyłączenia:** Realhitlookup, ordinaryRFprocedure, Recoveryrules outsideactivephaseban, and Rampageinteraction for excludedtarget.

`/rules/34/transcription`, bajty[418082,418447); SHA `bb2fb7a340fa96084fb920e82bcc8f11437a8dec382e614a099efd13420790b1`.

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

`/rules/34/interpretation`, bajty[418474,419102); SHA `2bda8a6301ec97e69039c28e9f67f85d4f7d8fec49da1454d77dac65bba2a6ec`.

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

`/rules/34/conditions`, bajty[419125,419360); SHA `68973486651af2b291d4dc22af0877125951379266cb23a195add13f360483bc`.

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

`/rules/34/action_effect`, bajty[419386,419935); SHA `c53c773a292847db5c346b9fa60b86ed3d2c4e55175d7cd4cb3b39cbc21cc842`.

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

`/rules/34/exceptions`, bajty[419958,420170); SHA `5378035ced77dccae1adb5e9ffa07e6238cf6afd1d38b3f080b119b108e683c1`.

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

`/rules/34/parameters`, bajty[420193,421276); SHA `e6c833dfe6214399f34d274f429903dcd355fc266c68d07ba8ee5e353f9dd7cd`.

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

`/rules/34/time_limits`, bajty[421782,422030); SHA `324d1b980d652104fc07e2867f4163ad2efb26ccab044e5c091f648c34194197`.

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

`/rules/38/transcription`, bajty[433971,434317); SHA `07e54b41e30a904fdd048268c88c5912e56b83411b0d531743476db4b98bf0fe`.

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

`/rules/38/interpretation`, bajty[434344,434908); SHA `990defefcc40bfb6d19cf44d53222a9433408c7b9881440c717ca6465d05b0a6`.

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

`/rules/38/conditions`, bajty[434931,435212); SHA `bbd8daca33d310b17dafc396fa6f1ecced6e8165e039cb2113d8be02bcb52deb`.

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

`/rules/38/action_effect`, bajty[435238,435723); SHA `9c18d4c5534a490e99907441e57aa9dc7c4598528ec3606a11b0e7a86b761313`.

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

`/rules/38/exceptions`, bajty[435746,436002); SHA `51fcc9e7a61371944fae34de36b80457df890572a07f7b972146027596185f95`.

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

`/rules/38/parameters`, bajty[436025,437122); SHA `a60b39b3ae8687f03cb5eaa71394cc8c42017ace31bb00acbfce4892456a50a7`.

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

`/rules/38/time_limits`, bajty[437594,437973); SHA `107b129cd0ddae31d05893fcc42838870a0b5e5e731af8a75c59381eb80b659b`.

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

`/rules/39/transcription`, bajty[439235,439613); SHA `4b97dc78ff2ca202d66bf1c589e1f5f31d59d050f78bdba6366a1f007cff8159`.

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

`/rules/39/interpretation`, bajty[439640,440146); SHA `3de53d253c6681da51ca69bc33730280130054bfa2dec97ea72b841ef7aa103e`.

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

`/rules/39/conditions`, bajty[440169,440438); SHA `cefc65674ed6147c8d6d26130462e707addab3689342c13ab54061a732e00a9a`.

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

`/rules/39/action_effect`, bajty[440464,440891); SHA `61053779a781f90653d12cf83d671d43cee957bd8407f34fbd7a65e450332add`.

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

`/rules/39/exceptions`, bajty[440914,441170); SHA `407991a6f540aa3077e63df280e79336115d2576784ebf4a35cf695bbbe75df4`.

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

`/rules/39/parameters`, bajty[441193,441884); SHA `9a74118e92f4c6da932f597446b8e1143b667122537dfec502ad7e8487b7c528`.

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

`/rules/39/time_limits`, bajty[442356,442617); SHA `339ed6b46549e64e8c60919845468caaecb692fb79e255afbae857b535d0f6df`.

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

`/nodes/34/content`, bajty[200110,200511); SHA `ca1f9d19f8773d76ab2f05c4229586705c6531ec02312395b91e340c23fa17c8`.

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

`/nodes/35/content`, bajty[200940,201273); SHA `5760b38f03df3fb18a708db70be9b96e3da0d2fe7c6388ae1f56ab37b6af7d2a`.

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

## SIT-18 — Ferocity: brak przypisania leadera

### Zamrożone fakty i pytanie

```json
{
  "event": "jedna BI Routs",
  "nearby_leaders": [
    "A",
    "B"
  ],
  "Initiative": [
    5,
    7
  ],
  "DR": 6,
  "scenario_command_mapping": "missing"
}
```

Czy Ferocity utracona i które BI nią objąć?

**Expected z eval-v1:** Blokada wyboru leader Initiative i zakresu utraty. Wiadomo, że należy wykonać Ferocity check poRout, ale nie wybierać najbliższego ani korzystniejszego leadera.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF36/right, `/situations/17/evidence/0`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Ferocity continues until the BI’s leader (as given in the scenario
> setup) fails a Ferocity check, which the player conducts each
> time a BI unit Routs. The player rolls the die and compares it to
> the leader’s Initiative Rating. If the DR is the same or lower, BI
> units retain their Ferocity, otherwise Ferocity is permanently lost
> for BI under the command of that leader. The loss of Ferocity for
> the units under one leader has no effect on the Ferocity of units
> under the command of different leaders.

Źródło PDF36/right, `/situations/17/evidence/1`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.

### first-001 — justified_block / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "Ferocity_loss_and_command": "blocked",
  "known_trigger": "BI Rout requirescheck",
  "diagnostic_with_A5_DR6": "loss ifAisassigned",
  "diagnostic_with_B7_DR6": "retain ifBisassigned"
}
```

1. R994 conditions binds leader toscenario; G-D994scenario blocking=true and syntheticcase lackscommandmapping.
2. IfAwithInitiative5 assigned:6>5 →loss forAcommand; ifB7 assigned:6<=7 →retain. This demonstrates materialneed, not choice ofleader.
3. Do not selectnearest orfavorableleader and do not guess affectedBI membership.

**Porównanie:** Matches expectedjustifiedblock; localtrigger/operator known without actualcommanddetermination.

**Zależności i blokada:** D994scenario criticalmissingtarget supplies identity/Initiative/membership; nearbylabels andnumbers do not supply ownership.

**Wyłączenia:** Actualleaderchoice, commandmembership and completeRout/PreShock.

`/rules/43/transcription`, bajty[382491,382850); SHA `7a8d4e216cc75c55ccc4914ec64fb6826e98915024bc5bd738d1314fab1961eb`.

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

`/rules/43/interpretation`, bajty[382876,383415); SHA `df217c0a2974b1b1c93744cb9bc1cb1a1cc0a8fce1f445421411b41f401e4d02`.

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

`/rules/43/conditions`, bajty[383437,383737); SHA `d376b849a612d980496512780c161b4f6173374905638d9fbe11747ba034827f`.

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

`/rules/43/action_effect`, bajty[383762,384222); SHA `455c400aa81030e852f66652715946c33d1358f14b5568608e9ea1ee3d459c02`.

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

`/rules/43/exceptions`, bajty[384244,384492); SHA `c4c5a47c1819e2deb5f2f9419316ab2433f32f38600c9637ec50b8b94b940811`.

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

`/rules/43/parameters`, bajty[384514,385977); SHA `da37bd06c692dc7824ee3f42379a2a39980b34fd9f53fe571891278ed5d1f395`.

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

`/rules/43/time_limits`, bajty[386495,386758); SHA `d8907a2afd4c6db3cd0d7f9a028015e9adfbd9f4e6ae07b38d63d2bbb9dcfaaf`.

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

`/gaps/64/reason`, bajty[559913,560022); SHA `109dc1faf3036560f84b15f4cba2ab629e85fbb01b4e63b1571e6e3e95583346`.

```json
"Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable."
```

`/gaps/64/needed_context`, bajty[560048,560120); SHA `cf8e60275312cbbc9510da3e644086e88929224314165b6101f95ea75ae5df91`.

```json
"Selected scenario BI command assignments and leader Initiative Ratings"
```

`/gaps/64/blocking`, bajty[560140,560144); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

### context-01 — justified_block / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "Ferocity_loss_and_command": "blocked",
  "known_trigger": "BI Rout requirescheck",
  "diagnostic_with_A5_DR6": "loss ifAisassigned",
  "diagnostic_with_B7_DR6": "retain ifBisassigned"
}
```

1. R994 conditions binds leader toscenario; G-D994scenario blocking=true and syntheticcase lackscommandmapping.
2. IfAwithInitiative5 assigned:6>5 →loss forAcommand; ifB7 assigned:6<=7 →retain. This demonstrates materialneed, not choice ofleader.
3. Do not selectnearest orfavorableleader and do not guess affectedBI membership.

**Porównanie:** Matches expectedjustifiedblock; localtrigger/operator known without actualcommanddetermination.

**Zależności i blokada:** D994scenario criticalmissingtarget supplies identity/Initiative/membership; nearbylabels andnumbers do not supply ownership.

**Wyłączenia:** Actualleaderchoice, commandmembership and completeRout/PreShock.

`/rules/43/transcription`, bajty[456630,456999); SHA `723a100a7837d82f9165026f28ba0c919443b4eb2b4d7a268244c69aea95db62`.

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

`/rules/43/interpretation`, bajty[457026,457577); SHA `5ef70a4e65be0024cef522ff06f718be9490ceccf2cc1e6e18980e417039b9d3`.

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

`/rules/43/conditions`, bajty[457600,457911); SHA `94c5542c7bb9fe0c8716a1fe107b86aa43ce4c7960dc3c2d68f5536ea3bd0953`.

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

`/rules/43/action_effect`, bajty[457937,458409); SHA `422652c04189e8158ebeab441aac0b24e9c0dda9ce17d3df6d5fe39620fc0549`.

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

`/rules/43/exceptions`, bajty[458432,458688); SHA `cc513bf934d89de7d82f78a745c965244686eb6f7953c92f2983cf4e182d05cc`.

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

`/rules/43/parameters`, bajty[458711,460231); SHA `d2609df8d78e24aeacbc64489cfb4a2165a3cd0a05552b2a6e95fb61cf0b9a51`.

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

`/rules/43/time_limits`, bajty[460774,461047); SHA `02d47874e27eac052f117efb45f97fb61f66cddf6ef9bf7b2d9f45df6f828b3e`.

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

`/gaps/64/reason`, bajty[645829,645938); SHA `109dc1faf3036560f84b15f4cba2ab629e85fbb01b4e63b1571e6e3e95583346`.

```json
"Leader assignment and Initiative needed for command-specific Ferocity checks is referenced but unavailable."
```

`/gaps/64/needed_context`, bajty[645965,646037); SHA `cf8e60275312cbbc9510da3e644086e88929224314165b6101f95ea75ae5df91`.

```json
"Selected scenario BI command assignments and leader Initiative Ratings"
```

`/gaps/64/blocking`, bajty[646058,646062); SHA `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.

```json
true
```

## SIT-19 — Impetuosity: koniec turn, nie natychmiast

### Zamrożone fakty i pytanie

```json
{
  "command_mapping": "synthetic A=[BI1,BI2,BI3], B=[BI4]",
  "event": "druga BI zA wchodzi enemy ZOC wGame Turn2",
  "base_MA": 5,
  "Momentum_roll_kind": "first-try"
}
```

Kiedy wygasa bonus i jaki zakres obejmuje?

**Expected z eval-v1:** DlaA przez resztęGame Turn2 nadal MA6 i−1DRM first-try Momentum leadera; po końcu turn Impetuosity A wygasa. Nie traci jej automatycznie B, jeśli własny trigger nie zaszedł.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF36/right, `/situations/18/evidence/0`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> At the start of a battle, the Gauls usually worked themselves into
> a fever pitch, which translated into an all-out charge. To reflect
> this, at the start of a game, all BI units have their MA increased
> by 1. Leaders that command BI units receive a –1 DRM to all
> first-try Momentum die rolls. Impetuosity lasts until at least two
> BI units of a leader’s command enter an enemy ZOC, at which
> point Impetuosity continues for the rest of the Game Turn, after
> which it is lost. Only the BI units in that command (per the sce-
> nario setup) are affected.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "A_MA_remainder_GameTurn2": 6,
  "A_leader_first_try_Momentum_DRM": -1,
  "A_Impetuosity_end": "afterGameTurn2",
  "B_loss_from_A_trigger": false
}
```

1. R995 +1initialMA; suppliedbase5 →6 whileImpetuosityactive. R995 −1toallfirsttryMomentum ofBIleader.
2. Second distinctBIofAenteringZOC satisfies>=2trigger; R995 retainsstate forrest ofthatGameTurn2 andlosesafterturn.
3. Commandmapping suppliedA/B; lossAonly, noautomaticB loss absent itsowntrigger. HistoricalomissionSEM-022 does not alterthese operativefields.

**Porównanie:** Matches timing,bonus andcommandboundary without making ascenariodata claim.

**Zależności i blokada:** Syntheticcommandmapping/event/baseMA are supplied. Realsetup/Momentumprocedure notneeded for requestedadjustment/duration.

**Wyłączenia:** Realsetup/sourceMA andMomentumroll resolution, Bstate after anunspecifiedowntrigger.

`/rules/44/transcription`, bajty[388292,388674); SHA `8629c4fb8d9debf0c1bca8020a1c78a575e510459d30304ccd352ef736e77d5d`.

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

`/rules/44/interpretation`, bajty[388700,389170); SHA `03ad1c9e4fecfd7169d5bc364f87a72c132077907bd8db3b7db02b277fa612bd`.

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

`/rules/44/conditions`, bajty[389192,389477); SHA `aa58b012555cd6d29978b40ecdf3cd41ad49547ca24ea36083a7fd5122e9733d`.

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

`/rules/44/action_effect`, bajty[389502,389893); SHA `367e569d921f2b97e5472b1cea3319de4146c9197f6a0d0159402a46b5b08f75`.

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

`/rules/44/exceptions`, bajty[389915,390163); SHA `17e8b5f544a1dcf4836668ad50b7daf46ef44afdb129d3e46e9f66d8418db0ee`.

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

`/rules/44/parameters`, bajty[390185,391661); SHA `9b1bb7cc2e618d62b6d5b1e09e02fee8594acfde090e3f32c73a41a222667836`.

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

`/rules/44/time_limits`, bajty[392140,392403); SHA `6140a6e096a08371cab009fd8dad0a7cff437dd4ff4d228f4a137dca0966f450`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "A_MA_remainder_GameTurn2": 6,
  "A_leader_first_try_Momentum_DRM": -1,
  "A_Impetuosity_end": "afterGameTurn2",
  "B_loss_from_A_trigger": false
}
```

1. R995 +1initialMA; suppliedbase5 →6 whileImpetuosityactive. R995 −1toallfirsttryMomentum ofBIleader.
2. Second distinctBIofAenteringZOC satisfies>=2trigger; R995 retainsstate forrest ofthatGameTurn2 andlosesafterturn.
3. Commandmapping suppliedA/B; lossAonly, noautomaticB loss absent itsowntrigger. HistoricalomissionSEM-022 does not alterthese operativefields.

**Porównanie:** Matches timing,bonus andcommandboundary without making ascenariodata claim.

**Zależności i blokada:** Syntheticcommandmapping/event/baseMA are supplied. Realsetup/Momentumprocedure notneeded for requestedadjustment/duration.

**Wyłączenia:** Realsetup/sourceMA andMomentumroll resolution, Bstate after anunspecifiedowntrigger.

`/rules/44/transcription`, bajty[462641,463033); SHA `bedab52270618f2a4e4f4012382f5e4566d7e5afdeab1d0fd10b2dfc94ffafb1`.

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

`/rules/44/interpretation`, bajty[463060,463541); SHA `a5477240eb6fe75fccacb8487afbbb070bc5403df3a5c3e6276da198b24756af`.

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

`/rules/44/conditions`, bajty[463564,463860); SHA `a662e0efbd8aee0a50dd12b223d909d3b6eb717cea549c63890f7215a4704f6a`.

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

`/rules/44/action_effect`, bajty[463886,464288); SHA `75107d4be18b8f2184ffbb5318fc1cea43ef729083ea6432b782475cefcd1e42`.

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

`/rules/44/exceptions`, bajty[464311,464567); SHA `1204ed669a531c4ca4de90469f6543cea81892a88fa5a0ad55971319b2788b0f`.

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

`/rules/44/parameters`, bajty[464590,466123); SHA `872583ec1d926915fcea735785a062046230da1dc8ccf3957ec02678f930c100`.

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

`/rules/44/time_limits`, bajty[466626,466899); SHA `f7bf9287e7b7eee70d8a9cd1ffbecc9fb1bd8eeb8508e7c612189bba2e969764`.

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

## SIT-20 — CH+LI: dismount na granicy MA i mounted zakazy

### Zamrożone fakty i pytanie

```json
{
  "eligibility": "supplied eligible LI",
  "LI_printed_MA": 5,
  "CH_MA": 8,
  "distance_in_MPs_before_dismount_variants": [
    4,
    5
  ],
  "LI_MPs_before_mount": 3,
  "Missile_LOW_NO_marker_before_mount": true,
  "other_costs": false
}
```

Podaj lokalny budżet po dismount/mount; czy wolno mounted Shock i czy partial-phase mount daje repeat-movement wyjątek?

**Expected z eval-v1:** Dismount po4MP daje1MP, po5 brak dalszego ruchu; mount po3MP LI daje do5MP mounted CH (8−3). Mount/dismount koszt0MP/0Hits, marker LOW/NO usuwa się przy mount. Mounted LI nie Shock attack; partial-phase mount nie spełnia entire-phase zwolnienia repeat-movement Hits.

**Zakres:** Only requested local gate/transformation; never a complete combat/movement resolution.

Źródło PDF36/right, `/situations/19/evidence/0`, obraz SHA `19a8d294da3d5fda2896526b7aaa4c9ea239233ec6203c3b36d723c71fef4374`.

> Each CH unit may carry one Light Infantry (LI) unit. To denote
> that a LI unit is mounted on the CH unit, place the CH on top of
> the LI unit. The combined CH and LI unit is treated as a single

Źródło PDF37/left, `/situations/19/evidence/1`, obraz SHA `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

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

Źródło PDF37/left, `/situations/19/evidence/2`, obraz SHA `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

> • LI do not suffer any Cohesion Hits for moving a second (and
> third) time in a Game Turn, if they spend the entire Orders
> Phase mounted on the CH unit.

Źródło PDF37/left, `/situations/19/evidence/3`, obraz SHA `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

> • LI cannot Shock attack; they must dismount to do so. When
> mounted, they defend as LI.

Źródło PDF37/left, `/situations/19/evidence/4`, obraz SHA `eac35841555b17696a6dda014e9b482b91c2a15e2366c7effd30c8576f1c5d9b`.

> • LI may use Missile Fire using the Mounted Javelin row on the
> MRRC. Missile Supply (8.17) does not apply while the LI unit
> is mounted. Remove any MiSSile low/No markers from the LI
> unit when the unit mounts a CH. They may use Harassment
> and Dispersal fire as if they were cavalry units.

### first-001 — correct_local_result / waiting_review

Oryginał SHA: `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "dismount_remaining_MPs_after4": 1,
  "dismount_remaining_MPs_after5": 0,
  "mount_remaining_MPs_after_LI3": 5,
  "mount_dismount_MP_cost": 0,
  "mount_dismount_CH_cost": 0,
  "remove_LOW_NO_on_mount": true,
  "mounted_Shock_attack": false,
  "partial_phase_repeat_move_exemption": false
}
```

1. R996b strictused<LIprintedMA5:4<5 →remaining5−4=1;5<5false →no furthermovement.
2. MountremainingCHMA8−LIused3=5; R996b zeroMP/CHmount+dismountcost.
3. R996d removesLOW/NOonmount; R996c mountedLIcannotShock andmustdismount.
4. R996c exemptionrequiresentireOrdersPhase mounted; partialphase fails. No numerical repeatmovementHitcost invented.

**Porównanie:** Bothboundaryvariants and allotherrequestedlocalconclusions match.

**Zależności i blokada:** Eligibility/MA/usedMP/othercosts supplied; noactualMovementCostChart route/table,Supplyafterdismount orrealcounter needed.

**Wyłączenia:** Terrain/routes, postdismountSupplystate, exactrepeatmovementHitamount and actualeligibility/rating.

`/rules/47/transcription`, bajty[402305,402777); SHA `444c6951acb1ccccdcd854399bda44bbf1266c995d791c50b4add5bb5aa5df01`.

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

`/rules/47/interpretation`, bajty[402803,403610); SHA `6e4fadde95fc9ea0bab22f9be11bfcaeeaa1480116728527b9a11a450bfcfb5e`.

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

`/rules/47/conditions`, bajty[403632,403918); SHA `976f91c0d5e53b5dcc77d139661c1467291c102cb9fa6e62f9b69f10b30e0971`.

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

`/rules/47/action_effect`, bajty[403943,404671); SHA `d0d6699727a21b941d91afceb2a7408a024c330a422752c317e0880ce37bc4d8`.

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

`/rules/47/exceptions`, bajty[404693,405005); SHA `abfb4a380be6a5d2d04162973a266b610d9b7a9da92b91282188f00b61fd22b8`.

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

`/rules/47/parameters`, bajty[405027,408049); SHA `bbfa5e4499e301a8001e98b5bcd17a10da5112ad08fd50c692bb6ef1d30b82ed`.

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

`/rules/47/time_limits`, bajty[408592,408825); SHA `f4929655acc3c2c2053e589ba6e47091d22c46a1440c3ad038bf032082fd33cc`.

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

`/rules/48/transcription`, bajty[409900,410284); SHA `c376cb824211afa58ac39d92b7451e2639baa8c106dc03874aab23d73706155b`.

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

`/rules/48/interpretation`, bajty[410310,410717); SHA `419df34feae00c52bc039de51c5615f88ce6db46555992fd789d8dd18167d186`.

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

`/rules/48/conditions`, bajty[410739,410994); SHA `9d4ddbd05402da2b8bc6bc379bd3a4e9a6454a77e60776bf411229801b352474`.

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

`/rules/48/action_effect`, bajty[411019,411347); SHA `776cfa71e16ae6706714bb3240c22f8cf9d24a8273bc3fdce4a52fa6f22b3f69`.

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

`/rules/48/exceptions`, bajty[411369,411618); SHA `02c42ea71545a700d355667da2db7c9834d53e49b1e1880e5e90a914a197e85a`.

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

`/rules/48/parameters`, bajty[411640,412785); SHA `b48dc3140318e403e2a597809bc346b1caa3fcd29517c5e3ddff65815f7e1bfa`.

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

`/rules/48/time_limits`, bajty[413245,413492); SHA `8adf5f41d66ec8ad3efa9ef208ca190d89eb1ed31e8e919ef587d4a497cbc399`.

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

`/rules/49/transcription`, bajty[414726,415090); SHA `756f8222dd89663cb62b64389bf1d92ea009d6ebaf66c43a40e95dafe65e6b9b`.

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

`/rules/49/interpretation`, bajty[415116,415585); SHA `18381ea08d407f94b65c49195e0fdcffceb48ceecad725e23df3576eeb891c91`.

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

`/rules/49/conditions`, bajty[415607,415803); SHA `d48d5cd3ca0fd886b3d02ebe93ad0efb845176fe38b49c5e09a27e0a49e3dbf4`.

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

`/rules/49/action_effect`, bajty[415828,416218); SHA `04ba8a40a1a1016e113ee482ac06567ec3a8ddbd9e6152ee0a30c711336a9d11`.

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

`/rules/49/exceptions`, bajty[416240,416457); SHA `e544ed12ecb99cc9616dd7d530325c60e88f8d62958e389b4788d94a748638dd`.

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

`/rules/49/parameters`, bajty[416479,416707); SHA `b1f4eb30b4f4cd91e039e73fbe5f64736db0485e2dbe0b922afd7f097bb1a005`.

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

`/rules/49/time_limits`, bajty[417206,417434); SHA `7c5be4e014e97cb758facd71bd760823313897b1b4cf99eaf538a3e3340d3f16`.

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

### context-01 — correct_local_result / waiting_review

Oryginał SHA: `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`.

**Wyprowadzenie oceniającego, nie nowa odpowiedź modelu:**

```json
{
  "dismount_remaining_MPs_after4": 1,
  "dismount_remaining_MPs_after5": 0,
  "mount_remaining_MPs_after_LI3": 5,
  "mount_dismount_MP_cost": 0,
  "mount_dismount_CH_cost": 0,
  "remove_LOW_NO_on_mount": true,
  "mounted_Shock_attack": false,
  "partial_phase_repeat_move_exemption": false
}
```

1. R996b strictused<LIprintedMA5:4<5 →remaining5−4=1;5<5false →no furthermovement.
2. MountremainingCHMA8−LIused3=5; R996b zeroMP/CHmount+dismountcost.
3. R996d removesLOW/NOonmount; R996c mountedLIcannotShock andmustdismount.
4. R996c exemptionrequiresentireOrdersPhase mounted; partialphase fails. No numerical repeatmovementHitcost invented.

**Porównanie:** Bothboundaryvariants and allotherrequestedlocalconclusions match.

**Zależności i blokada:** Eligibility/MA/usedMP/othercosts supplied; noactualMovementCostChart route/table,Supplyafterdismount orrealcounter needed.

**Wyłączenia:** Terrain/routes, postdismountSupplystate, exactrepeatmovementHitamount and actualeligibility/rating.

`/rules/47/transcription`, bajty[477160,477644); SHA `3519fe394c1db085cc3316ccbf641e8215b0c404c4e8ca9a2159148a4e7bfe41`.

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

`/rules/47/interpretation`, bajty[477671,478494); SHA `5b65bd2dbc996c5d1bc1b32eba166516f39bf82b32842d70e9bb7108d46a2be1`.

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

`/rules/47/conditions`, bajty[478517,478814); SHA `cdcd6c72c750ac3063eab751e08d1d2189997f9a87383ee91a10c5a1692831bf`.

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

`/rules/47/action_effect`, bajty[478840,479584); SHA `e7efb29868aa443de5db7c745ebd541e731fca63e03286a331c319de6643a858`.

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

`/rules/47/exceptions`, bajty[479607,479931); SHA `c72820f3bd4f85641ecd0e30f44d20e046f63eddab8b6703a9cc68bab4d85d7c`.

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

`/rules/47/parameters`, bajty[479954,483094); SHA `3f818e810c91a52275007c3f7eb1a7faf61f45cc5b7bd2b72d1a63b6f6fd1fa9`.

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

`/rules/47/time_limits`, bajty[483663,483907); SHA `f6f059c6246ed337927282774d5236c8e2ebdf6956450bd47d308a744c3a74e1`.

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

`/rules/48/transcription`, bajty[485025,485419); SHA `864fb1b98dd462eb3997ca14ef42cb888cb9d1fbe90e468ea7c18f4c9e6d9098`.

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

`/rules/48/interpretation`, bajty[485446,485864); SHA `db2ba80230879271ef405a49da2f85cb1a57c24392469fa8ce1bb046f4582939`.

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

`/rules/48/conditions`, bajty[485887,486152); SHA `03f2092323224eeafef0c6822f83a23f5dea68d25b3664c0297c106aa371a9ba`.

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

`/rules/48/action_effect`, bajty[486178,486517); SHA `791bf978f761d134c06b4df760f31e5ea44bb91270eb15c93a49854aeb612eef`.

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

`/rules/48/exceptions`, bajty[486540,486797); SHA `89382c5af799d9779d7433af75abec693be530cf4d2bb8688e5a1355c62e3fe8`.

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

`/rules/48/parameters`, bajty[486820,488009); SHA `cf03606e5039fb400aa33c80de0fe401ba03cfd6fbfaedff87fa19638b8bc8ec`.

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

`/rules/48/time_limits`, bajty[488492,488749); SHA `c36a612bdf971faccd2fc7330191bbbc1bcf2e60774624aa1797ad6e0e3302cc`.

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

`/rules/49/transcription`, bajty[490031,490405); SHA `7f59208c3eca8bf8043f98cdc505032224609dcbf17e8273a9e6de74546a2514`.

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

`/rules/49/interpretation`, bajty[490432,490913); SHA `ae7d89b15b25c07a91bf2dea56febdbf73a7f09b0a24061f25a6b84cc8ae96ab`.

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

`/rules/49/conditions`, bajty[490936,491142); SHA `fa65aa1e6ff40c23bb80e5ac486a3d467e7fb8b93bbaacc758e81d0b78be106a`.

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

`/rules/49/action_effect`, bajty[491168,491570); SHA `2800a2c22bf12e58afba4306a07a2ec0eb6fd36554eab3f6d0ceb4a166c26c75`.

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

`/rules/49/exceptions`, bajty[491593,491820); SHA `eb0498e0f3b2978f40d83d8470976cab7d2e9e440a8d48b6a067b07cf58217c2`.

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

`/rules/49/parameters`, bajty[491843,492079); SHA `879f1d243c153e1345c51fcec0ab956d392547b7e2fee0086fad2392800e20f5`.

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

`/rules/49/time_limits`, bajty[492602,492840); SHA `4f3f4568175e0fba93a015086492c514375b40263e457ee5409f869e66222c93`.

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
