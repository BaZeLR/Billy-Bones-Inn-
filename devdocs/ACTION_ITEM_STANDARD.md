# Action And Item Standard

FamilyLife uses `actions.rpy` as the common action method file. Tractir now follows the same idea through `game/Inn/Actions.rpy`, while preserving its existing `main_ui` right panel.

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

## Common Action Methods

`game/Inn/Actions.rpy` is the standard place for common actions.

Important labels:

- `Examine`
- `Take`
- `Drop`
- `ApplyItemAction`
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

Important Python helpers:

- `action_restriction_message()`
- `action_restriction_result()`
- `player_pick_up_item()`
- `player_drop_item()`
- `player_apply_item_action()`
- `player_share_item_with()`
- `player_gift_to()`
- `apply_social_interaction_base()`

## Standard ObjectAction Factories

New object/item definitions should use these factories when possible:

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

Available factories:

- `make_standard_object_action(action_key, label="", args=None, condition=None, custom_properties=None, action_id="", target="", hook="")`
- `make_examine_action(object_id, where_id="", text_value="", label="", condition=None)`
- `make_take_action(object_id, where_id="", fallback_text="", label="", condition=None)`
- `make_consume_item_action(object_id, action_key="eat", where_id="", label="", fallback_text="", condition=None)`
- `make_meal_action(item_name, item_energy=0, where_id="", object_id="", label="", fallback_text="", condition=None)`
- `make_chore_action(chore_key, where_id="", label="", fallback_text="", object_id="", condition=None)`
- `make_sleep_action(return_location="TavernMain", days=1, label="", fallback_text="", where_id="", object_id="", condition=None)`
- `make_rest_action(return_location="", minutes_passed=120, energy_gain=15, label="", fallback_text="", where_id="", object_id="", condition=None)`
- `make_simple_target_action(action_key, object_id="", where_id="", label="", fallback_text="", condition=None)`

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

Do not put repeated basic logic inside room labels.

Good room label structure:

```renpy
label TavernExampleBuildActions:
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Прибрать", Call("DoChore", "clean_upstairs_rooms", "TavernExample", "", "")))
    $ current_action_items.append(MenuItem("Назад", Call("TavernExampleRestore")))
    show screen main_ui
    return
```

Better item/object definition:

```renpy
ExampleItem = GameItem(
    object_id="example_item_001",
    name="предмет",
    description="Описание предмета.",
    actions=[
        make_examine_action("example_item_001", "TavernExample", "Вы осматриваете предмет."),
        make_take_action("example_item_001", "TavernExample", "Вы берете предмет."),
    ],
    carriable=True,
)
```

The label should display content and route choices. Common state mutation belongs in `Actions.rpy`.
