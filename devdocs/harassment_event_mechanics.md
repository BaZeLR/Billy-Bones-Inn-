# Harassment Event Mechanics

Source of truth:
- `game/Inn/PartEventYourFirstReaction.rpy`
- `game/Inn/PartEventGirlHarrassmentReaction.rpy`
- `game/Inn/PartEventCustomerHarrassmentReaction.rpy`
- `game/Inn/PartEventAfterHarrassment.rpy`
- `game/Inn/IntHarrassmentDiscuss.rpy`

## Overview

This system is one of the game's best examples of layered social simulation.

One player choice can affect:
- trust / relationship
- sexual permissiveness
- work quality
- tavern public reputation
- later discipline and management conversations

The event is not resolved by one simple flag. It is computed from:
- player reaction
- girl sluttiness
- existing harassment policy for that girl
- whether she runs away
- whether she slaps the customer

## Flow

1. Event fires.
2. Player chooses a first reaction:
- ignore
- watch
- help
3. Girl-side reaction is computed.
4. Customer/public outcome is computed.
5. After-event conversation with the girl is computed.
6. Optional follow-up discussion updates longer-term relationship/discipline state.

## First Reaction Layer

Defined in:
- `PartEventYourFirstReaction`

Player choices:
- `Не обращать внимания`
- `Стоять и смотреть`
- `Вмешаться и помочь <girl>`

This first choice sets:
- `YourReaction1 = 1` ignore
- `YourReaction1 = 2` watch
- `YourReaction1 = 3` help

That value is then passed into the second-stage event logic.

## Core Inputs

Main inputs used by later branches:
- `sluttiness[girl]`
- `Friends[girl]`
- `HarassInstructions[girl]`
- `JobType`
- `GirlRunAway`
- `GirlSlapped`

### Meaning of the important inputs

`sluttiness[girl]`
- controls how threatening / offensive / acceptable the unwanted touching feels to the girl
- low values push toward shame, fear, anger, gratitude for protection
- high values push toward tolerance, passive acceptance, or even approval

`Friends[girl]`
- governs trust fallout and gratitude chance
- low friendship leaves more room for positive trust gain from helping
- positive friendship can also be damaged if the player behaves badly

`HarassInstructions[girl]`
- current management rule for how the girl is supposed to react
- important values:
  - empty string: no explicit instruction
  - starts with `allow`: player normalized or allowed this kind of treatment
  - `notallow`: player forbade it

This is what makes the system management-driven, not just emotional.

## Girl-Side Reaction

Defined in:
- `PartEventGirlHarrassmentReaction`

Main outputs:
- `GirlRunAway`
- `GirlSlapped`
- event text
- possible `Friends[girl]` changes

### Case A: Player helps (`YourReaction1 == 3`)

Outcome base:
- player defends the worker
- girl usually escapes the situation

Common result:
- `GirlRunAway = 1`

Low sluttiness (`<= 10`)
- girl slaps the offender
- `GirlSlapped = 1`
- if friendship is still low enough, she may thank the player
- possible trust gain:
  - `Friends[girl] += 1`

Mid sluttiness (`30+` but not very high)
- girl may not be upset enough to reward the help
- text suggests your intervention may have been unnecessary

Very high sluttiness (`>= 60`)
- girl may actively dislike the intervention
- she can side with the customer
- possible trust loss:
  - `Friends[girl] -= 1`
- `GirlRunAway = 2`

### Case B: Player watches (`YourReaction1 == 2`)

This is the most trust-sensitive branch.

If policy is strict and sluttiness is low:
- girl tries to break free
- often returns to work upset

If no strict policy and sluttiness is moderate:
- girl may hesitate, see the player watching, and decide to endure it

If policy explicitly allows it:
- low sluttiness can still lead to fear and flight
- high sluttiness can produce calm or positive acceptance

Main design meaning:
- watching is not automatically cruel or helpful
- it is interpreted through the girl's sexual tolerance and through prior player policy

### Case C: Player ignores (`YourReaction1 == 1`)

This overlaps with the policy/sluttiness checks from the watch path, but with a different emotional framing.

If girl is low-slut or under stricter instruction:
- she breaks free and may slap or flee

If policy allows it and sluttiness is high:
- she may accept it calmly

Design meaning:
- ignoring is often judged more harshly in the later trust phase than simple watching

## Customer / Public Outcome

Defined in:
- `PartEventCustomerHarrassmentReaction`

This is where work quality and tavern reputation are affected.

### If the girl does not run away

High sluttiness (`>= 50`)
- on `1/12` chance:
  - tavern fame rises by `1`
  - waitress skill may rise by `1` if below `70`

Lower sluttiness
- on `1/25` chance:
  - tavern fame rises by `1`
  - waitress skill may rise by `1`
- on `1/6` chance, if sluttiness is still under `7`:
  - sluttiness rises by `1`

Meaning:
- enduring harassment can train public-service tolerance
- and very rarely improve reputation among regulars
- but this can also sexually desensitize the girl

### If the girl runs away and slaps the customer

On `1/2` chance:
- angry customer leaves
- tavern fame drops by `1`
- waitress skill may drop by `1` if it was at least `20`

Also, on `1/2` chance if sluttiness > 0:
- sluttiness drops by `1`
- text frames this as pride / regained self-respect

Meaning:
- good for dignity
- bad for tavern reputation sometimes

### If the girl runs away without slapping

On `1/8` chance:
- customer still leaves angry
- tavern fame drops by `1`
- waitress skill may drop by `1`

On `1/10` chance if sluttiness > 0:
- sluttiness drops by `1`

Meaning:
- refusal still has a reputation risk
- but less explosive than a slap

## After-Event Trust Fallout

Defined in:
- `PartEventAfterHarrassment`

This is the most direct trust layer.

### If the player's standing policy was `allow...`

Low sluttiness (`< 18`)
- girl confronts the player:
  - "did I really have to endure this?"
- on `1/3` chance, if friendship > 0:
  - `Friends[girl] -= 1`

Meaning:
- even if the player set permissive policy, some girls resent being pushed too far

### If player watched and girl was upset

If:
- `YourReaction1 == 2`
- and `(sluttiness < 30 or GirlSlapped > 0)`

Then girl explicitly blames the player for standing there and watching.

On `1/2` chance, if friendship > 0:
- `Friends[girl] -= 1`

### If player ignored and girl was upset

If:
- `YourReaction1 == 1`
- and `(sluttiness < 30 or GirlSlapped > 0)`

Then girl complains that the player was absent and did not help.

On `1/5` chance, if friendship > 0:
- `Friends[girl] -= 1`

### If girl is already permissive

In higher-slut branches she may:
- walk by calmly
- tease the player
- avoid trust loss entirely

## Work Quality Impact

This system does not directly change all tavern service stats.

The main explicit skill effect is:
- `waitress[girl]`

Why waitress specifically:
- these harassment events are tied to floor service and customer contact
- so the system treats them as part of service professionalism

Net effect pattern:
- smooth endurance can improve waitress skill
- public disruption can reduce waitress skill

This is a realistic simulation loop:
- exposure can toughen a waitress
- but ugly incidents can also reduce service effectiveness

## Reputation Impact

The main public metric touched here is:
- `tavernfame`

Possible changes:
- `+1`
  - if customers are pleased with how the interaction is absorbed
- `-1`
  - if the interaction ends in public conflict and angry departure

So these incidents are not purely private. They can shape the tavern's public standing.

## Longer-Term Management Meaning

The system is not just:
- protect her
- ignore her

It also asks:
- what standard has the player set for this worker?
- can the worker psychologically endure that standard?
- does the standard help tavern profit, hurt tavern profit, or damage trust?

That makes `HarassInstructions[girl]` extremely important:
- it converts the event from one-off moral flavor
- into real workplace policy simulation

## Concrete Examples

### Example 1: Low-slut waitress, player helps

Inputs:
- `sluttiness = 5`
- `Friends = 3`
- `YourReaction1 = 3`

Likely result:
- girl runs away
- slaps customer
- may thank player
- friendship can rise by `1`
- tavern fame may later drop by `1` if customer storms out

Meaning:
- trust improves
- tavern reputation may suffer

### Example 2: High-slut waitress, player helps

Inputs:
- `sluttiness = 65`
- `YourReaction1 = 3`

Likely result:
- girl may dislike the intervention
- friendship can drop by `1`
- event text frames the player as overreacting

Meaning:
- protective behavior can backfire if the girl already accepts this conduct

### Example 3: Player watches, no strict instruction, medium sluttiness

Inputs:
- `HarassInstructions = ""`
- `sluttiness = 24`
- `YourReaction1 = 2`

Likely result:
- she notices the player watching
- decides to endure it instead of fleeing
- no immediate trust gain
- no strong trust loss if she is permissive enough

Meaning:
- player passivity is normalized by her tolerance level

### Example 4: Player allowed harassment, girl is still too shy

Inputs:
- `HarassInstructions = "allow..."`
- `sluttiness = 10`

Likely result:
- she still feels humiliated
- after-event confrontation
- possible `Friends -1`

Meaning:
- management policy can outrun the girl's real readiness

## Summary

This system computes 4 different consequences at once:

1. Emotional trust:
- `Friends`

2. Sexual tolerance:
- `sluttiness`

3. Work professionalism:
- `waitress`

4. Public tavern outcome:
- `tavernfame`

That is why it is one of the stronger mechanics in the project:
- one event
- one player reaction
- several interacting social and economic consequences
