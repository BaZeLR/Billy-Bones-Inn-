"""Spring-water catalog and real forest action-builder contracts."""

from pathlib import Path
import re
import textwrap
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def function_source(text, name, indent="    "):
    start = text.index(indent + "def " + name + "(")
    offset = len(indent) + 1
    following = re.search(r"(?m)^(?:" + indent + r"def |label |init )", text[start + offset:])
    end = start + offset + following.start() if following else len(text)
    return textwrap.dedent(text[start:end]).strip()


def test_spring_water_is_one_stackable_canonical_ingredient():
    catalog = source("game/Items/Crafting/SoapCraftAndAtticItems.rpy")
    definition = catalog.split("    SpringWaterItem = ", 1)[1].split("    CorkItem = ", 1)[0]
    item = eval(definition.strip(), {"GameItem": lambda **values: SimpleNamespace(**values)})
    assert item.object_id == "spring_water_001"
    assert item.carriable and item.stackable
    assert item.custom_properties == {"item_kind": "ingredient", "ingredient_kind": "spring_water"}
    assert catalog.count('object_id="spring_water_001"') == 1


@pytest.mark.parametrize("room_code", ["ForestSpring", "ForestLake", "ForestDeep"])
@pytest.mark.parametrize("hour,minute,daylight", [(8, 0, True), (19, 29, True), (19, 30, False), (22, 0, False)])
def test_actual_forest_builder_offers_refill_only_at_open_spring(room_code, hour, minute, daylight):
    forest = source("game/Forest/Forest.rpy")
    room = SimpleNamespace(code_name=room_code, visible_exits=lambda: [])
    namespace = {
        "rooms": SimpleNamespace(current=room),
        "calendar_v2": SimpleNamespace(hour=hour, minute=minute),
        "MenuItem": lambda caption, action: SimpleNamespace(caption=caption, action=action),
        "Call": lambda *args: args,
        "story_event_available": lambda *args: False,
        "werecat_can_set_bait": lambda *args: False,
        "werecat_can_check_bait": lambda *args: False,
        "fight_can_hunt_here": lambda *args: False,
        "player_can_train_shooting": lambda: False,
        "forest_trap_can_place": lambda *args: False,
        "forest_trap_can_check": lambda *args: False,
        "forest_has_horse": lambda: False,
        "forest_room_get_spawned_items": lambda room: [],
    }
    definition_namespace = {name: SimpleNamespace for name in ("Room", "RoomAction", "RoomDescription", "RoomExit", "RoomSchedule")}
    definition_namespace.update(ROOM_GROUP_FOREST="forest", forest_open_hours_visible=lambda: True)
    spring = source("game/Forest/ForestSpring.rpy").split("init 6 python:", 1)[1].split("label ForestSpring:", 1)[0]
    exec(textwrap.dedent(spring), definition_namespace)
    room.action_menus = definition_namespace["ForestSpringRoomDefinition"].action_menus if room_code == "ForestSpring" else []
    room.visible_actions = lambda: room.action_menus
    exec(function_source(source("game/Utilities/General/Screens/build_room_action_items.rpy"), "room_action_menu_item"), namespace)
    exec(function_source(source("game/Utilities/General/Classes/RoomTemplate.rpy"), "build_extra_action_items", "        "), namespace)
    room.build_extra_action_items = lambda: namespace["build_extra_action_items"](room)
    for name in ("forest_after_dusk", "forest_subroom_action_items"):
        exec(function_source(forest, name), namespace)
    items = namespace["forest_subroom_action_items"](room)
    refill = [item for item in items if item.action == ("ForestSpringFillBottle",)]
    assert len(refill) == int(room_code == "ForestSpring" and daylight)
    assert len({item.caption for item in items}) == len(items)
    if not daylight:
        assert [item.action for item in items] == [("ForestReturnToTavernAfterDusk",)]


def test_refill_menu_is_owned_only_by_spring_room_definition():
    forest = source("game/Forest/Forest.rpy")
    spring = source("game/Forest/ForestSpring.rpy")
    assert "items.extend(room_obj.build_extra_action_items())" in function_source(forest, "forest_subroom_action_items")
    assert "ForestSpringFillBottle" not in forest
    assert spring.count('target="ForestSpringFillBottle"') == 1


def test_refill_is_one_returnable_label_without_parallel_water_state_or_refresh():
    label = source("game/Forest/ForestSpring.rpy").split("label ForestSpringFillBottle:", 1)[1]
    assert 'if rooms.current_code != "ForestSpring" or forest_after_dusk():' in label
    assert 'if player.remove_item("empty_bottle_001", 1):' in label
    assert label.count('player.add_item("spring_water_001", 1)') == 1
    assert 'main_ui_begin_native_scene_state("Родниковая вода")' in label
    assert "main_ui_end_native_scene_state()" in label
    assert label.rstrip().endswith("return")
    assert all(token not in label for token in ("jump ", "call screen", "while ", "advance_minutes", "cork_001", "set_money", "action_items =", "state["))
