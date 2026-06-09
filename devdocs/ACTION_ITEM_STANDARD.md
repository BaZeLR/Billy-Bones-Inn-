# Action And Item Standard

Family Life uses `actions.rpy` as a simple file of real Ren'Py action labels.
Those labels show/select pictures, write text, mutate stats/time/items/state,
and return. The owning room/location label then jumps or calls back to itself.

Tractir should follow that design while keeping its existing `main_ui` shell.
The active current file is `game/Utilities/General/Common/Actions.rpy`, but its
current shape is not the target architecture.

## Core Structures

- `GameItem`
  - Defined in `game/Inn/GameItem.rpy`.
  - Static item/object-like data: id, name, description, actions, contents, picture, price, flags, custom properties.

- `RoomAction` / `ObjectAction`
  - Defined in `game/Inn/GameObjectTemplate.rpy`.
  - Action blueprint for object/item menus.
  - Fields: `action_id`, `label`, `hook`, `target`, `args`, `condition`, `custom_properties`.

- `game_items`, `item_catalog`, `game_item_registry`
  - Built in `game/Inn/GameItems.rpy`.
  - `game_items` is the known item id list.
  - `item_catalog` and `game_item_registry` are lookup tables for UI/inventory.

- Room `game_items`
  - Stored on room objects.
  - Helper methods in `Actions.rpy` move items between room and player inventory.

## Desired Common Action Labels

The common actions file should contain clear basic action labels, not a central
dispatcher or UI refresh system.

Important labels:

- `Examine`
- `Take`
- `Drop`
- `Drink`
- `Eat`
- `UseDrinkItem`
- `UseFoodItem`
- `Wash`
- `DoChore`
- `Sleep`
- `Rest`
- `MakeFire`
- `Clean`
- `Chop`

The label is the executor. It may directly:

- set `MainTxt` / scene text
- select a picture or use `vscene` for an authored scene
- mutate player stats
- mutate inventory or room/object state
- advance time
- call `stat` or another tiny status update helper
- return

Screens are allowed as actual UI surfaces, but basic action labels should not
route through refresh/apply/renew labels just to redraw a menu.

Tiny Python helpers are acceptable only when they remove real duplication and
do not hide the action's meaning.

Possible tiny helpers:

- `action_restriction_message()`
- `action_restriction_result()`
- item count/add/remove helpers
- clamp/stat helpers

NPC-specific social gift/share effects do not belong in the common basic action
file. They belong with the NPC or item ownership layer.

## Action Definition Metadata

Action definitions may carry display metadata close to the owner:

- caption
- target label
- picture
- description/result text
- condition
- small custom properties when needed

This lets an object or room show the right text and picture without making the
common action file know every object in the game.

Example object definition:

```renpy
actions=[
    make_examine_action(
        "old_axe_001",
        "Shed",
        "Лезвие затупилось, древко потрескалось, но топор еще годится."
    ),
    make_take_action(
        "old_axe_001",
        "Shed",
        "Вы снимаете со стены старый топор и забираете его с собой."
    ),
]
```

Factories can exist if they build these simple action rows. They must not become
dispatchers that hide the real label.

Current factories in Tractir include:

- `make_standard_object_action(action_key, label="", args=None, condition=None, custom_properties=None, action_id="", target="", hook="")`
- `make_examine_action(object_id, where_id="", text_value="", label="", condition=None)`
- `make_take_action(object_id, where_id="", fallback_text="", label="", condition=None)`
- `make_consume_item_action(object_id, action_key="eat", where_id="", label="", fallback_text="", condition=None)`
- `make_meal_action(item_name, item_energy=0, where_id="", object_id="", label="", fallback_text="", condition=None)`
- `make_chore_action(chore_key, where_id="", label="", fallback_text="", object_id="", condition=None)`
- `make_sleep_action(return_location="TavernMain", days=1, label="", fallback_text="", where_id="", object_id="", condition=None)`
- `make_rest_action(return_location="", minutes_passed=120, energy_gain=15, label="", fallback_text="", where_id="", object_id="", condition=None)`
- `make_simple_target_action(action_key, object_id="", where_id="", label="", fallback_text="", condition=None)`

These are acceptable only if they produce direct calls to real labels.

## Standard Action Keys

These keys are registered in `STANDARD_ACTION_METHODS`:

- `examine`
- `take`
- `drop`
- `drink`
- `eat`
- `meal`
- `wash`
- `chore`
- `sleep`
- `rest`
- `make_fire`
- `clean`
- `chop`

## Rule For New Content

Do not add refresh/apply/renew/rebuild wrappers.

Preferred flow:

```text
room/object/NPC exposes action
-> button calls real label
-> label performs effect and returns
-> owning room/object/NPC flow is restored directly
```

Good room/location style:

```renpy
label TavernExample:
    $ CurrentRoom = TavernExampleRoom
    $ MainTxt = TavernExampleRoom.descriptions[0].text
    call screen main_ui
    return
```

Good action style:

```renpy
label TavernExampleClean:
    $ MainTxt = "Вы прибираете комнату."
    $ energy -= 5
    $ taverncleanliness += 1
    $ calendar_advance_minutes(20)
    call stat
    return
```

The caller should return to the owning room or object directly, not through a
generic refresh label.

## Present Tractir Code Comparison

Current `game/Utilities/General/Common/Actions.rpy` is bloated because it mixes:

- real basic action labels
- inventory storage helpers
- social gift/share rules
- NPC-specific item effects
- UI refresh routing
- result applier wrappers
- room-specific refresh maps

Classify current symbols this way:

- KEEP: `Examine`, `Take`, `Drop`, `Drink`, `Eat`, `Wash`, `DoChore`, `Sleep`,
  `Rest`, `MakeFire`, `Clean`, `Chop`, `BoilWater`, after simplifying them.
- KEEP CAREFULLY: small inventory/stat/restriction helpers.
- MOVE: social item rules and NPC-specific effects to item/NPC ownership.
- REMOVE/BYPASS: `ROOM_ACTION_REFRESH`, `RefreshCurrentActionMenu`,
  `ApplyActionResultToUI`, and generic apply/renew/rebuild labels.

The target is not "more dispatch tables." The target is fewer layers and clearer
labels.
