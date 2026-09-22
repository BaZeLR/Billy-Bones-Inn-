# Harassment, Apology, And Personal Favors

## Authority And Scope

The September 17, 2026 user request sets the negative-reaction and apology
numbers below. These are requested gameplay rules, not claims of original QSP
parity. Live `.rpy` implements the rules; `textLocRef` is historical reference.

- `game/Utilities/General/NPC/PeopleRuntime.rpy`: each NPC owns `rel`,
  its relationship cap, anger, and daily interaction counters. Shared
  `PeopleInfo` mechanics apply to NPC instances; `Girl` owns female favor
  eligibility.
- `game/Utilities/General/NPC/RelationshipDynamics.rpy`: existing social
  readiness and relationship mood.
- `game/NPC/Girls/Common/OldPointTalkSystem.rpy`: shared returnable interaction
  labels. NPC talk labels own the visible apology choice.
- `game/Inn/HouseholdRuntimeEvents.rpy`: existing outfit and barber request
  scenes and consequences.
- `daily_events`: pending tailor visits. `household`: existing outfit requests,
  barber appointments, and request/visit cooldowns.

Do not add relationship maps, pending-apology mirrors, NPC-specific copies of
the shared rule, refresh/rebuild labels, dispatchers, or Python scene handlers.
Labels own authored text, media, native `menu:`, consequences, and return flow.
The right-side HUD remains persistent; screens only display UI.

## Negative Reaction

`PeopleInfo.record_negative_reaction(reason)` applies the universal consequence
when an authored interaction establishes a negative reaction:

- Friendship falls by 5 through the existing `change_social` owner, clamped at 0.
- Existing `change_anger(1, reason)` records the anger and its authored cause.
- A neutral response, unavailable action, or accepted interaction is not a
  negative reaction merely because no reward occurs.

This covers rejection of unwanted MC touching and a negative response to the
MC's handling of a harassment incident. Preserve the existing reaction
thresholds, positive outcomes, and consent boundaries; this rule does not make
an NPC accept intimacy.

## Apology

`PeopleInfo.can_apologize()` reads the NPC's existing anger, existing relationship
mood, and legacy low-friendship reconciliation eligibility (`rel < 5`).
Availability remains limited to fewer than 3 talks that day.

`PeopleInfo.attempt_apology()` is the shared numeric rule:

- Acceptance chance: exactly 50%.
- If accepted: restore a random integer from 1 through 5 friendship points,
  respecting the NPC's own relationship cap, and clear the existing anger
  states.
- If refused: no friendship reward or extra penalty; anger is not cleared.
- An attempt still uses the existing interaction/time bookkeeping.

The two rolls use `renpy.random.randint`, documented in the bundled Ren'Py
8.5.2 SDK (`doc/other.html`, `renpy.random`). This advances between attempts
and cooperates with rollback. Do not use the calendar-keyed `procedural_randint`
here: it repeats a fixed outcome at the same calendar position.

There is no new persistent apology state. NPC menus call the same rule, so an
incident's anger and a later apology do not depend on separate NPC-specific
implementations.

## Harassment Flow And Owners

1. `game/Utilities/General/NPC/PartEventYourFirstReaction.rpy`: MC chooses
   ignore (1), watch (2), or help (3).
2. `game/NPC/Girls/Common/PartEventGirlHarrassmentReaction.rpy`: NPC reaction,
   escape/slap result, and direct relationship consequences.
3. `game/Utilities/General/NPC/PartEventCustomerHarrassmentReaction.rpy`:
   customer outcome, NPC waitress skill, and player-owned tavern fame.
4. `game/Utilities/General/NPC/PartEventAfterHarrassment.rpy`: after-event
   complaint and relationship consequence.
5. `game/NPC/Girls/Common/IntHarrassmentDiscuss.rpy`: authored follow-up
   conversation and policy choice.

`EventWaitressHarrass` / `EventWaitressHarrassPart2` and
`EventCleaningHarrass` / `EventCleaningHarrassPart2`, under
`game/NPC/Girls/Common/`, share these returnable event procedures.

Reaction inputs come from the NPC instance: `corruption`, `rel`, and
`harass_instruction()`. Escape/slap results and the MC reaction are direct
procedure arguments, not parallel persistent NPC state.

Existing negative-reaction conditions include low tolerance for permissive
policy (`corruption < 18`), an upset NPC when the MC watches or ignores
(`corruption < 30 or GirlSlapped > 0`), and an NPC disliking an intervention at
`corruption >= 60`. Positive help outcomes and their existing thresholds remain
separate from the fixed negative-reaction penalty.

Public/customer effects remain owned by the existing customer-result label.
NPC skills use `NPC.skills["waitress"]`; tavern fame changes through
`player.change_tavern_fame()`. Do not reinterpret these as apology rewards.

## Tailor And Barber Favors

`Girl.can_request_favor()` is shared eligibility for female NPC instances,
including current and potential tavern staff; it is not restricted to the
three household women.

The rule reads existing NPC anger and existing appointment, request, and
cooldown state. It does not require employment or the MC's gift-offer
friendship threshold. Request scenes keep their authored choices.
Accepting a tailor request uses the existing `BuyDressTom` / `BuyDress` daily
event flow and outfit request state. Accepting a barber request uses the
existing `household.barber_appointments` and request/visit dates.

Do not create a second favor queue, duplicate schedule, or another pending
request flag. Existing shop rules, prices, and actual visit outcomes remain
with their current owners.

## Historical Numeric Reference

These old values explain the migration delta; they are not the current
September 17 rule:

| Reference | Original numeric behavior |
| --- | --- |
| `textLocRef/PartEventAfterHarrassment.txt:14-16` | Permissive policy, `corruption < 18`: -1 friendship on 1/3 chance, only when friendship > 0. |
| Same file, lines 22-26 | Upset NPC, MC watches: -1 on 1/2 chance, only when friendship > 0. |
| Same file, lines 30-34 | Upset NPC, MC ignores: -1 on 1/5 chance, only when friendship > 0. |
| `textLocRef/PartEventGirlHarrassmentReaction.txt:26-28` | Disliked intervention: -1 on 1/3 chance, only when friendship > 0. |
| `textLocRef/IntAmandaTalk.txt:16-25` and `IntMelissaTalk.txt:16-25` | Reconciliation: 1/3 acceptance, fixed +1 through `SlutFriendsIncrease(..., 6, 1, 1, ...)`; fewer than 3 talks and friendship < 5. |
| `textLocRef/IntSandraTalk.txt:16-25` | Same reconciliation gate/reward, but 1/2 acceptance. |

Before this change, `OldPointTalkSystem` instead calmed relationship-mood anger
by 2 deterministically and awarded a fixed +1 only when that anger reached 0.
Harassment used `anger_with_player`, while this apology's availability read
relationship-mood anger. The shared NPC rule must read the existing causes
consistently without adding a mirror.

`dialogue.tab` is a dialogue export with source-label/file locations, not an
authority for probabilities or numeric consequences. Preserve its text and
the original TXT files; numeric changes belong in live mechanics.
