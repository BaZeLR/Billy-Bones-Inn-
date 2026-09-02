from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_random_chronicle_owns_native_event_menu_without_dialogue_gate():
    source = (PROJECT_ROOT / "game" / "Town" / "RandomTownEvents.rpy").read_text(encoding="utf-8-sig")
    body = source.split("label TownRandomChronicleEvent:", 1)[1].split("label TownStreetHelpEvent:", 1)[0]

    assert 'main_ui_begin_native_scene_state("Случайное событие")' in body
    assert '"[scene_runtime.text]"' not in body
    assert '"Идти дальше":' in body
    assert "main_ui_end_native_scene_state()" in body
    assert "main_ui_runtime.action_items" not in body


def test_town_street_thugs_shout_renders_result_as_native_menu():
    source = (PROJECT_ROOT / "game" / "Town" / "RandomTownEvents.rpy").read_text(encoding="utf-8-sig")
    body = source.split("label TownStreetThugsShout:", 1)[1].split("label TownStreetPatrolEvent:", 1)[0]

    assert "Попробовать спугнуть их криком" not in body
    assert '"[scene_runtime.text]"' in body
    assert '"Вернуться":' in body
    assert "main_ui_runtime.action_items" not in body
    assert "call screen main_ui" not in body


def test_town_street_patrol_uses_its_dedicated_picture():
    source = (PROJECT_ROOT / "game" / "Town" / "RandomTownEvents.rpy").read_text(encoding="utf-8-sig")
    body = source.split("label TownStreetPatrolEvent:", 1)[1].split("label TownStreetPatrolPass:", 1)[0]

    assert 'scene_runtime.picture = "images/fight/patrol_guard.png"' in body
    assert 'scene_runtime.picture = "images/general/cityguard.jpg"' not in body


def test_street_tavern_objects_use_main_ui_without_recursive_overlay_menu():
    source = (PROJECT_ROOT / "game" / "Town" / "StreetTavern.rpy").read_text(encoding="utf-8-sig")

    assert "def street_tavern_action_items():" in source
    assert 'Call("StreetTavernObjectMenu", room_object.object_id)' in source
    assert 'label StreetTavernObjectMenu(object_id=""):' in source
    assert "room_action_menu_item(_street_action)" in source
    assert "label street_tavern_menu:" not in source
    assert "label street_tavern_object_menu" not in source
    assert "renpy.display_menu" not in source
    assert "jump street_tavern" not in source


def test_help_event_procedure_does_not_replace_room_actions():
    source = (PROJECT_ROOT / "game" / "Town" / "RandomTownEvents.rpy").read_text(encoding="utf-8-sig")
    body = source.split('label TownStreetHelpRecruit(help_name="бродяга"):', 1)[1].split("label TownStreetHelpMoney:", 1)[0]

    assert "main_ui_runtime.action_items" not in body
    assert body.rstrip().endswith("return")


def test_street_event_conditions_use_the_authoritative_runtime_object():
    source = (PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")

    for method in ("patrol_allowed", "thug_allowed", "help_allowed", "chronicle_allowed"):
        assert source.count(f'"#TownStreet.{method}(rooms.current_code)"') == 4
    for legacy_name in ("town_street", "TownStreetEventsToday", "TownStreetFightToday"):
        assert legacy_name not in source
