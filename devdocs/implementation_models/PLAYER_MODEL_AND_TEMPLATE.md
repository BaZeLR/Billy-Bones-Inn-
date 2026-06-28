# Player Model And Basic Action Template

This document defines the intended Player model and the basic player-side action
model.

## Ownership Rule

The Player class instance is the source of truth for player state.

Player-owned state includes:

- identity
- condition: health, energy, fun, fight injury state
- money and player economy access
- inventory access, not item definitions
- appearance and cleanliness
- skills and exploration progress
- reputation and notoriety
- player combat resources
- player sex/intimacy state
- daily and weekly action history that belongs to the player
- player-side chore participation

Legacy scalar globals and dicts may exist only as temporary compatibility output
while old labels still read them. They are not the authority.

## Current Runtime Owners

Current runtime files:

- `game/Utilities/General/Player/Player.rpy`
- `game/Inn/PlayerChoresSystem.rpy`
- `game/Utilities/General/Common/Actions.rpy`

`Player.rpy` already has the intended direction:

- `PlayerCondition`
- `PlayerStats`
- `PlayerEconomy`
- `PlayerInventory`
- `PlayerEquipment`
- `PlayerAppearance`
- `PlayerChores`
- `PlayerTavernManagement`
- `PlayerCombat`
- `Player`
- `player_state()`

`PlayerChoresSystem.rpy` and `Actions.rpy` still contain compatibility globals
and mixed departments. These must be audited before runtime cleanup.

## Basic Player Actions

Basic player actions are direct actions the player performs on himself, his
routine, or simple work state.

Examples:

- wash
- drink
- eat
- rest
- wait
- clean
- carry wood
- chop wood
- make fire
- boil water
- clean ashes
- clean upstairs rooms

These actions are usually not computation-heavy. A basic action should:

1. check simple restrictions
2. mutate the authoritative owner directly
3. advance time when needed
4. show optional picture/text
5. return to the current room/object flow

The action label is the execution endpoint. It must not require a refresh label,
apply label, dispatcher, rebuild label, or one-action handler.

## What Is Not A Basic Player Action

Do not put these departments into the basic action model:

- NPC interaction: talk, flirt, gifts, questions, relationship changes
- purchasing and shop flow
- inventory/game item use behavior
- crafting or object creation
- hunting
- fighting
- sex engine state and sex acts
- story event choices and consequences

Those systems may call player methods or mutate player state through the Player
API, but they own their own flow.

## Action Restrictions

Basic actions may be blocked by:

- low energy
- late time of day
- low fun or bad mood
- poor health or injury after a bad fight
- missing required object or resource
- action already done today
- daily or weekly action limit
- story/event lock

Restriction checks must be local and readable. If the check is primitive, keep it
in the label. If the check is shared by many actions, use one small Player method
or one small domain method owned by the correct system.

Do not make a generic rule engine for a handful of simple actions.

## Primitive Label Template

Use this when the action is simple.

```renpy
label PlayerWashAtBarrel(return_label="Backyard"):
    $ p = player_state()

    if p.condition.energy < 5:
        "I am too tired to wash now."
        jump expression return_label

    if p.condition.health < 20:
        "I feel too battered to stand here washing."
        jump expression return_label

    $ p.appearance.wash()
    $ p.condition.energy = max(0, p.condition.energy - 5)
    $ calendar_v2.advance_minutes(10)
    call stat

    "I wash the dirt off and feel a little more human."
    jump expression return_label
```

Template rules:

- get the Player instance once
- check restrictions directly
- mutate Player-owned fields directly
- mutate other owners only when the action truly affects them
- advance time in one place
- return directly to the owning room/object label

## Python Result Template

Use Python only when the action has enough calculation to justify it.

The method should belong to the owner of the logic.

```renpy
# Method belongs on the existing Player class.
def try_heavy_cleaning(self):
    if self.condition.energy < 30:
        return {"ok": False, "text": "I am too tired for heavy work."}
    if self.condition.health < 25:
        return {"ok": False, "text": "My body will not take that today."}

    self.condition.energy = max(0, self.condition.energy - 30)
    self.condition.fun = max(0, self.condition.fun - 10)
    self.chores.mark_done_today("heavy_cleaning")
    return {"ok": True, "text": "I clean until my arms ache.", "minutes": 60}

label PlayerHeavyCleaning(return_label="TavernMain"):
    $ result = player_state().try_heavy_cleaning()
    "[result['text']]"

    if result.get("ok", False):
        $ calendar_v2.advance_minutes(int(result.get("minutes", 0) or 0))
        call stat

    jump expression return_label
```

Do not wrap this result in an additional apply/refresh dispatcher. The label has
the result and should display it directly.

## Chores

Chores are player actions, but the affected state may belong to multiple owners:

- player: energy, fun, daily/weekly action history
- tavern: tavern cleanliness, service readiness
- room/object: dirty room state, fire state, water state

The label or method must mutate each correct owner directly.

Current compatibility state such as `PlayerChoresWeek` should be treated as
temporary output until the Player/Tavern chore state is fully class-owned.

## Object-Started Player Actions

An action can be started from an object and still be a Player action.

Example:

- barrel object exposes "wash"
- label mutates `player_state().appearance`
- object/room only provides the physical target and return path

The object owns action availability tied to the object. The Player owns player
state mutation.

## Daily Flags

Daily action flags should live on the correct owner:

- player routine flags on Player
- NPC social flags on NPC/social system
- tavern work flags on Tavern/TavernTeam
- room dirt/search flags on Room or GameObject
- event locks on Event/Thread

Do not add new daily dicts as a second state store unless this is an explicit
migration bridge.

## Actions.rpy Target Shape

`Actions.rpy` should contain only:

- small shared action labels that are truly reused
- small shared restriction helpers that are truly reused
- compatibility labels while callers are migrated

It should not contain:

- NPC social logic
- shop/purchase flow
- inventory item behavior
- crafting flow
- fight/hunt flow
- sex flow
- refresh/rebuild/apply dispatcher layers
- recursive menu loops

When a current label is mixed, split by ownership before editing behavior.

## Save/Load Rule

At any checkpoint, Player state must be present on the Player class instance.
Loading a game should restore the Player instance directly, not reconstruct the
real player state from loose globals or dicts.
