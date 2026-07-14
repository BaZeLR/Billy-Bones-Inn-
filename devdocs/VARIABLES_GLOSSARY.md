# Owner State Glossary

Last updated: 2026-07-01

This glossary records the current ownership model. It is not a list of old QSP
dicts to preserve.

## Rule

Persistent gameplay state belongs to the object that owns the behavior.

- Player state belongs to the Player instance and player-owned systems.
- NPC state belongs to the NPC class instance.
- Room state belongs to the Room instance.
- Game item state belongs to the GameItem/inventory owner.
- Event and thread state belongs to Event/Thread runtime objects.
- Tavern business state remains in the tavern system until that system is fully ported.
- UI variables are display helpers only.

Old maps such as `AmandaVar`, `MelissaVar`, `SandraVar`, `GeorgettVar`,
`Friends[...]`, `Talked[...]`, `CurrentLoc[...]`, and `NPCSchedules` are not
current architecture authority. If an old reference doc uses those names, port
the meaning into the owning class or system instead of recreating the map.

## Current Location

| Name | Owner | Notes |
| --- | --- | --- |
| `CurLoc` | Player/location runtime | Current physical room/location code. |
| `CurrentRoom` | Room runtime | Current Room object used by the main UI. |
| NPC `getLocation()` | NPC instance | Authoritative visible-NPC source. The room does not own NPC presence. |

## Time

| Name | Owner | Notes |
| --- | --- | --- |
| `hour` / `minute` | Calendar runtime | Source for schedule and venue checks. |
| `week` / day counters | Calendar runtime | Source for weekday/day checks. |
| UI time slot text | Calendar/UI projection | Display only. Do not use it as schedule authority. |

## Events And Threads

| Name | Owner | Notes |
| --- | --- | --- |
| Event object | Event runtime | Owns availability checks. |
| Thread object | Thread runtime | Owns stage, completion, abort, and progression. |
| Event label | Script label | Owns text, `vscene`, menu, consequences, time cost, and return flow. |

## NPCs

NPC classes own:

- identity and display data;
- current/default schedule data;
- `getLocation()` behavior;
- relationship/trust/corruption/mana where applicable;
- daily counters such as talked/flirted/gifted/asked;
- story flags and counters under `npc.vars` or explicit fields;
- talk and event methods.

Shared NPC logic belongs in the upper NPC class only when it is real common
behavior. Do not create bridge maps or fallback dicts for normal flow.

## Player

The Player class owns player state such as health, energy, arousal, combat
skills, equipment, inventory-facing methods, notoriety/fame/exploration, and
other player progression. Systems such as fight or sex may mutate Player through
their own labels/methods, but should not keep a second player-state copy.

## Rooms

Rooms own physical-location data:

- name and code name;
- group;
- background/picture selection;
- first/situational descriptions;
- hidden/locked/open state;
- navigation exits;
- room objects;
- room-only actions.

Rooms do not own NPC story state, NPC schedules, item behavior, or event
consequences.

## UI

UI variables may hold currently selected card/menu/display state. They are
helpers, not gameplay truth. If a value changes story/gameplay, it belongs to
the appropriate Player/NPC/Room/Item/Event/Tavern owner instead.
