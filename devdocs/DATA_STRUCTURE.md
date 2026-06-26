# Data Structure

## Goal

Define the target project structure for the core data layers before moving files into a dedicated `Data/` folder.

This document is about ownership and registries:

- what each data file owns
- which lists/indexes must exist
- how game code resolves rooms, items, and people
- how actions should read data without fallback shims or runtime bootstrap


## Core Principle

Data is owned once.

Each major gameplay layer has:

- one owning file
- one main list
- one id/name registry

Code should resolve from those registries directly.

Do not use:

- `globals().setdefault(...)`
- runtime-created fallback registries
- compatibility aliases that duplicate ownership


## Planned Folder

Target folder:

- `game/Inn/Data/`

Planned files:

- `GameItems.rpy`
- `GameObjects.rpy`
- `Rooms.rpy`
- `People.rpy`
- optionally later:
  - `Player.rpy`
  - `Tavern.rpy`


## Layer Model

### 1. Game Items

Owned by:

- `Data/GameItems.rpy`

Meaning:

- all concrete items in the game world

Examples:

- ale
- wine barrel
- axe
- book
- key
- wallet
- knife
- mushroom
- condom
- costume
- lamber

Implementation model:

- every item is a `GameObject`
- item behavior comes from shared flags plus `custom_properties`

Shared features may include:

- `wearable`
- `container`
- `carriable`
- `locked`
- `readable`
- `usable`
- `stackable`
- `hidden`

Important registries:

- `GameItems`
- `GameItemIds`

Optional category lists:

- `DrinkItems`
- `FoodItems`
- `WearableItems`
- `ContainerItems`
- `ToolItems`

Lookup helpers:

- `get_game_item(item_id)`
- optional category helpers like `get_drink_item(item_id)`


### 2. Game Objects

Owned by:

- `Data/GameObjects.rpy`

Meaning:

- world objects used by rooms and scenes

Examples:

- bed
- fireplace
- bar
- room door
- chest
- signboard

Note:

- an object may also be an item
- the project currently uses `GameObject` for both portable items and scene objects
- this is acceptable as long as ownership is clear

Important registries:

- `gameObjects`
- `GameObjectIds`

Lookup helpers:

- `get_game_object(object_id)`


### 3. Rooms

Owned by:

- `Data/Rooms.rpy`

Meaning:

- all actual room/location definitions

Examples:

- `TavernMainRoom`
- `StreetTavernRoom`
- `MarketPlaceRoom`
- `WineStoreRoom`
- `GroceryStoreRoom`

Important registries:

- `Rooms`
- `RoomIds`

Lookup helpers:

- `get_room(room_id)`

Rooms should contain:

- exits by target label/id
- object ids or object refs
- NPC ids or names
- room picture
- room display name


### 4. People

Owned by:

- `Data/People.rpy`

Meaning:

- character registries and core character-name lists

Main groups:

- core women cast
- secondary NPCs
- player

Required registries:

- `AllGirlNames`
- `SecondaryNPCNames`

Optional later:

- `CharacterNames`

Rules:

- girls are keyed by name string
- NPCs are keyed by name string
- player is a single dedicated actor key, usually `"you"`


### 5. Player

Owned by:

- later `Data/Player.rpy` or current player-state files until migration

Meaning:

- scalar player state and player-owned collections

Examples:

- `money`
- `fun`
- `energy`
- `notoriety`
- `exploration`
- `charisma`
- `MyDresses`
- `MyCurDress`

Action methods do not own data.

They mutate player-owned variables that are already defined once.


### 6. Tavern

Owned by:

- later `Data/Tavern.rpy` or current tavern-state files until migration

Meaning:

- tavern-wide economy and business state

Examples:

- `tavernvisitors`
- `tavernfame`
- `productnum`
- `winenum`
- `TavernHole`
- `TavernGloryHole`
- tavern daily/weekly reports


## Action Resolution Model

Actions should not own data.

Actions should:

1. receive an id or actor name
2. resolve the owned data object
3. mutate existing variables
4. return result text or payload

Examples:

- `player_drink_item(item_id)`
- `player_eat_meal(item_name, item_energy)` for now
- later:
  - `player_use_item(item_id)`
  - `player_read_item(item_id)`
  - `player_give_item(item_id, char_name)`

Room/object UI then:

- calls the action
- updates `MainTxt` / `CurLocDesc`
- keeps or restores the correct room/object menu state


## Action Patterns

Basic actions should stay simple.

For common player/game actions, use direct mutation methods in `Actions.rpy`.

Examples:

- `take(item_id, room_obj)`
- `drop(item_id, room_obj)`
- `drink(item_id)`
- `eat(item_id, item_energy, item_fun, time_cost)`
- `talk(char_name)`
- `gift(char_name, item_id)`
- `flirt(char_name)`
- `wash()`
- later:
  - `sleep()`
  - `explore()`
  - `use(item_id, target_id)`
  - `peep(char_name)`

Rules:

- mutate existing owned variables directly
- return plain text if the caller needs text
- do not return large result dicts unless a subsystem truly needs structured data
- do not create fallback state inside the action method

Good:

- room calls action method
- action mutates variables
- caller places returned text into `MainTxt` / `CurLocDesc`

Bad:

- action owns room flow
- action creates missing globals
- action returns `{"ok": True, ...}` for simple local actions without a real need


## Label Patterns

Room/event flow should stay plain Ren'Py.

Use labels for:

- room entry
- local object menus
- repeatable local routines
- event branches

Pattern:

1. room label sets room state
2. room action builder prepares visible choices
3. local action label mutates state or calls a reusable method
4. label returns to the same room flow unless it is a real location change

Use:

- `jump RoomLabel` for actual location change
- `call SomeRoutine` only when the routine is reusable and should return
- returned value/text may be plugged into room text or picture choice

Do not use:

- compatibility alias labels
- nested fallback menu layers
- room reload loops as a substitute for direct state mutation


## Room / Item / NPC Flow

Room owns:

- room description
- room picture
- exits
- placed items/objects
- optional room-owned actions only when the room itself is acted on
- room-specific flags/checks if needed
- hidden/locked/open state booleans
- optional venue schedule

Room does not own NPCs. NPCs appear in the right-side visible NPC field by
`getNPCids(current_location)`, which checks each NPC's `getLocation()`.

Item owns:

- item id
- actions
- shared features and custom properties

NPC owns:

- stable profile data
- mutable runtime state
- optional schedule
- optional inventory

UI owns:

- show room picture
- show current text
- show current action list

That is enough for most gameplay flow.


## Character Data

Character data is split into two layers.

### Stable profile data

Mostly immutable:

- key/name
- display name
- birthday
- portrait base info
- identity/background tags

### Mutable runtime state

Changes during play:

- friendship / relationship values
- work/job stats
- current location
- costume state
- openness/arousal flags
- inventories / gifts / possessions
- event and story flags

This allows cards, reports, schedules, and events to read one coherent runtime state.


## Character Inventories

Characters may own inventories the same way the player does.

Use this for:

- gifts
- personal possessions
- quest items
- carried tools/items

Suggested pattern:

- `playerItems = []`
- later per-character collections such as:
  - `CharacterItems[name] = []`

Gifts should not be modeled only as one-off flags if an actual item can be stored.


## Scheduling

Schedules belong to character runtime data, not to the UI.

They may include:

- known slots
- unknown/hidden slots
- weekday patterns
- weekend patterns
- temporary overrides from events or jobs

Schedules are the bridge between:

- who is visible in a room
- where characters move
- when random encounters can fire
- when house/street/weekend events can be added

Use schedules to drive:

- NPC presence
- movement dynamics
- street events
- house events
- weekend-only content


## Inventory And Stack Rules

Items are identified by id.

Take / drop should follow the same basic rule everywhere:

- `take(item_id, room_obj)`
  - remove item id from room item list
  - add item id to inventory

- `drop(item_id, room_obj)`
  - remove item id from inventory
  - add item id to room item list

Stackables need distinct stack instances or stack entries.

Do not treat one generic resource id as an infinite shared pile.

Examples:

- base type:
  - `chopped_wood`

- stack instances:
  - `chopped_wood_001`
  - `chopped_wood_002`

The exact stack amount should belong to the stack entry/instance, not to vague ad hoc room text.


## Registry Rules

Every major data layer should expose:

- one main list
- one id/name list
- one lookup helper

Required pattern:

- items:
  - `GameItems`
  - `GameItemIds`
  - `get_game_item(...)`
- objects:
  - `gameObjects`
  - `GameObjectIds`
  - `get_game_object(...)`
- rooms:
  - `Rooms`
  - `RoomIds`
  - `get_room(...)`
- people:
  - `AllGirlNames`
  - `SecondaryNPCNames`


## Defaults And Initialization

Defaults must be defined once in the owning place.

Examples:

- shared dict state in `Intro.rpy` today
- later moved into dedicated data files if needed

Good:

- `default Friends = {}`
- `default FightLevel = {"you": 1}`
- `default GameObjects = []`

Bad:

- `globals().setdefault("FightLevel", {})`
- “if missing, create runtime dict”


## Migration Plan

### Phase 1

Document and stabilize current ownership.

- keep current behavior
- stop adding new fallback layers
- keep registries explicit


### Phase 2

Move registry definitions into `Data/`.

- `GameItems.rpy`
- `GameObjects.rpy`
- `Rooms.rpy`
- `People.rpy`


### Phase 3

Update callers to use the new owning registries only.

- item actions by item id
- room/object resolution by id
- character actions by name


### Phase 4

Remove old compatibility/bootstrap code.

- alias labels
- `globals()` bootstrap
- duplicate registries


## Current Decision

The project will move toward:

- `Actions.rpy` for direct player action methods
- `Data/GameItems.rpy` for item catalog and item ids
- `Data/GameObjects.rpy` for world object registry
- `Data/Rooms.rpy` for room registry
- `Data/People.rpy` for name-based character registries

This is the reference structure for future wiring work.
