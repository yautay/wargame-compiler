# Drill Skirmish: benchmark rulebook

> Self-authored benchmark text, released as CC0. It contains no publisher material and may live in the tool repo.
> Every rule exists to exercise a phenomenon that rulebook compilation must handle (see `phenomena.yaml`).
> The text is deliberately written in the terse style of real wargame rules, including **one intentional
> ambiguity** (6.2) and **one scenario override** (7.1). Do not "fix" them: they are test material.

## 1.0 Components

**1.1** Each unit has a Strength (1 to 4) and a Movement Allowance (MA). Infantry units have an MA of 4.
Light units have an MA of 6.

**1.2** A unit is either Formed or Routed. A Routed unit is marked with a Routed marker.

**1.3** Reserve markers are placed face-down. Only the owning player may look at a face-down Reserve marker.

## 2.0 Sequence of Play

**2.1** A game lasts six Game Turns. Each Game Turn consists of two Player Turns: first the First Player's, then the
Second Player's. The player whose Player Turn it is, is the active player.

**2.2** Each Player Turn consists of the following phases, in this order:
1. Rally Phase
2. Movement Phase
3. Combat Phase
4. Supply Phase

## 3.0 Movement

**3.1** During his Movement Phase, the active player may move any or all of his units, one at a time. A unit may spend
up to its MA in Movement Points (MP) per Movement Phase.

**3.2** Entering a clear hex costs 1 MP; entering a woods hex costs 2 MP. A unit may not enter a hex if it does not have
enough MP left to pay the cost. Exception: a unit that has not yet moved this phase may always move one hex.

**3.3** A unit must stop moving when it enters a hex adjacent to an enemy unit.

**3.4** A Routed unit may not enter a hex adjacent to an enemy unit.

**3.5** Light units are not required to stop under 3.3. They remain subject to 3.4.

**3.6** A hex may never contain more than one unit.

## 4.0 Combat

**4.1** During his Combat Phase, each of the active player's units that is adjacent to an enemy unit may attack one
adjacent enemy unit. A unit may attack only once per Combat Phase. Routed units may not attack.

**4.2** To resolve an attack, roll one die (1d6) and add the attacker's Strength. Subtract 1 if the defender is in a
woods hex.

**4.3** Apply the modified result on the Combat Results Table:

| Modified result | Effect on defender |
|---|---|
| 4 or less | No effect |
| 5–6 | Routed |
| 7 or more | Eliminated |

**4.4** A Routed unit that receives a Routed result is eliminated instead.

**4.5** Eliminated units are removed from the map.

## 5.0 Rally

**5.1** During his Rally Phase, the active player may attempt to rally one of his Routed units that is not adjacent to
an enemy unit. Only one rally attempt may be made per Rally Phase.

**5.2** Roll 1d6. If the result is equal to or less than the unit's Strength, the unit becomes Formed. Otherwise there
is no effect.

## 6.0 Reserves

**6.1** During setup, each player places up to two Reserve markers face-down in his deployment area. Each Reserve marker
represents one unit or is a dummy.

**6.2** A Reserve marker is revealed when an enemy unit moves adjacent to it, or when its owner chooses to reveal it at
the start of his Movement Phase. When revealed, the marker is replaced by the unit it represents, or removed if it is
a dummy.

## 7.0 Scenario: The Ford

**7.1** In this scenario, a rally attempt succeeds if the result is equal to or less than the unit's Strength plus one.

**7.2** The player who controls the ford hex at the end of Game Turn 6 wins. A player controls a hex if one of his
units occupies it, or if one of his units was the last to occupy it.
