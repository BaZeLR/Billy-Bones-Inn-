# Action Binding Model

Purpose: describe how actions actually work in the current Ren'Py port.

This is the canonical model to use for refactoring and for new content.

---

## Core Point

Actions are **not** organized as one central catalog of generic methods.

They are primarily **bound to entities and containers**:

- rooms
- room exits
- room objects
- game items
- NPCs

Then a room-specific or generic builder assembles the current visible action list from those bindings.

This is much closer to how QSP locations expose context-sensitive `act` options than to a single service router.

---

## Current Runtime Model

## 1. Room is the main container

File:

- `game/Inn/RoomTemplate.rpy`

A `Room` already contains:

- descriptions
- exits
- `game_items`
- `npcs`
- `action_menus`
- schedule
- triggers
- custom properties

So the room is the top-level container that decides what can appear right now.

QSP perspective:

- this is the closest equivalent of a location context
- room contents determine what actions become available

---

## 2. Exits create movement actions

Example:

- `RoomExit(label="Вернуться в главный зал", target="TavernMain")`

Then build logic turns exits into menu actions, usually through:

- `Call("AdvanceMovementTime", exit.target)`

So movement actions are not looked up from a global movement registry.
They are created from the current room's visible exits.

---

## 3. Objects create object-specific action menus

Example file:

- `game/Inn/TavernMyRoom.rpy`

The room contains objects:

- `bed_001`
- `chest_001`
- `myroom_window_001`
- `myroom_attic_hatch_001`

The room action list is built from those objects:

- `"Кровать" -> Call("TavernMyRoomObjectMenu", "bed_001")`
- `"Ларь" -> Call("TavernMyRoomObjectMenu", "chest_001")`

Then the object menu reads that object's own visible actions and exposes them.

So:

- room gives access to object
- object gives access to actions

This is the correct current model.

---

## 4. NPC actions are bound through room NPC lists

File:

- `game/Inn/CharacterActionHub.rpy`

NPC actions come from the room's `npcs` list, not from a global NPC action dispatcher.

Each NPC entry typically provides:

- `npc_id`
- `name`
- `condition`
- `talk_label`
- optional inspect target

Then the current room decides which NPCs are visible.

The hub provides actions like:

- inspect
- talk

So NPC interactions are:

- room-bound
- entity-bound
- then passed through a generic interaction hub

This is a good architecture.

---

## 5. Generic action labels still exist, but they are support tools

File:

- `game/Inn/Actions.rpy`

These are reusable actions like:

- `Examine`
- `Take`
- `Drop`
- `Drink`
- `MakeFire`
- `Clean`
- `Chop`

They are useful, but they are **not** the true top-level organization model.

The real organization model is:

- current room
- visible object/item/NPC/exit
- bound actions for that entity

The generic labels are implementation helpers used when an entity action needs them.

---

## 6. MC-owned actions are also a real category

This project also already has actions that belong primarily to the player character, not to an external NPC or passive room object.

Examples:

- sleep
- eat
- drink
- wash
- chores
- time skip / wait
- flirt / gift / talk helper actions

Files:

- `game/Inn/Actions.rpy`
- `game/Inn/PlayerChoresSystem.rpy`
- `game/Inn/TimeChangeMenu.rpy`
- `game/Inn/TavernMyRoom.rpy`
- `game/Inn/Backyard.rpy`
- `game/Inn/TavernKitchen.rpy`

These actions directly affect player stats such as:

- `energy`
- `fun`
- `look`
- `exploration`
- `dayssincewash`
- `taverncleanliness`
- `hotwaterready`
- `upstairsroomsdirty`
- inventory / carried items
- friendship values in some social actions

So the full action model is not only:

- room -> object/NPC/exit -> action

It is also:

- room -> player-available self action -> stat change

QSP perspective:

- this is equivalent to location-specific self-actions like rest, wash, train, eat, wait, work
- these should remain labelized and explicit

### Recommended rule for MC actions

If the action is something the player does to himself / his own routine / his own condition, it should still be exposed as a clear label or helper endpoint.

Good pattern:

- room menu exposes self action
- self action label performs state change
- `call stat` refreshes UI
- room rebuild label restores current menu

Examples already in code:

- `TavernMyRoomSleepAction`
- `BackyardWashAtBarrel`
- `TavernKitchenEat`
- `TavernKitchenDrink`
- `TavernKitchenMakeFire`
- `TavernKitchenBoilWater`

---

## 7. Generic builder already exists

File:

- `game/Inn/my_layouts/build_room_action_items.rpy`

This confirms the runtime direction:

1. iterate visible room objects
2. add object menu actions
3. iterate visible exits
4. add movement actions

This is entity-driven assembly, not method-catalog dispatch.

---

## What To Prefer Going Forward

## Preferred pattern

For new work, prefer this hierarchy:

1. room defines which objects/NPCs/exits are present
2. object or NPC defines what actions are available
3. room may also expose MC-owned self actions
4. builder assembles current menu
5. action label performs the actual logic

That means:

- room = container
- object/NPC/item = action owner
- MC self-state = another valid action owner
- label = action executor

---

## Good examples

### Room-driven object actions

- `TavernMyRoom`
- `TavernStable`
- `StreetTavern`
- `Backyard`
- `Shed`

### Room-driven NPC actions

- `TavernMain`
- `TavernKitchen`
- `EllonaTemple`

### Generic support labels

- `Actions.rpy`
- `ShowImage.rpy`
- `CharacterActionHub.rpy`

---

## What To Avoid

Avoid designing future systems as:

- one giant central action catalog
- one generic dispatcher that knows every object and every NPC
- action availability determined far away from the room/entity that owns it

Why:

- harder to trace
- less QSP-like
- less maintainable
- breaks locality of logic

---

## Recommended Rule For Refactors

If an action belongs to:

- a bed
- a stove
- a chest
- a signboard
- a bar counter
- a specific NPC
- a specific room

then keep that action owned by that object/NPC/room, not by a universal catalog.

Only keep generic support in shared files when the action truly repeats across many places.

Examples of valid shared actions:

- take/drop/examine
- drink/eat
- image display
- card/report display
- movement-time application

Examples of actions that should stay local:

- bed-specific sleep/grope/rest actions
- stove/fireplace interactions
- chest wardrobe flow
- room-specific shop menus
- NPC-specific flirt/talk branches
- room-specific self-care/work actions

---

## Best Simplified Mental Model

Use this mental model for the port:

- QSP location -> Ren'Py room label
- QSP visible `act` set -> room-built current action list
- QSP object-specific acts -> object menu/actions
- QSP NPC-specific acts -> NPC hub + NPC talk labels
- QSP self-actions -> room-exposed player labels that mutate stats
- generic helper `gs` style logic -> reusable label/helper files

That matches the current codebase much better than pretending actions come from one central method map.

---

## Bottom Line

The current project already treats actions as:

- contextual
- entity-bound
- assembled from room contents

That is the correct model to continue.

So for future implementation:

- keep actions bound to rooms / objects / items / NPCs
- use builders to assemble visible actions
- use labels as execution endpoints
- do not refactor toward one abstract global action catalog
