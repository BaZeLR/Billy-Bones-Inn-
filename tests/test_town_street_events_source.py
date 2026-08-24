from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_town_street_thugs_shout_renders_result_screen():
    source = (PROJECT_ROOT / "game" / "Town" / "RandomTownEvents.rpy").read_text(encoding="utf-8-sig")
    body = source.split("label TownStreetThugsShout:", 1)[1].split("label TownStreetPatrolEvent:", 1)[0]

    assert "Попробовать спугнуть их криком" not in body
    assert "current_action_items = [MenuItem(\"Идти дальше\", Function(renpy.return_statement, True))]" in body
    assert "call screen main_ui" in body


def test_street_tavern_objects_use_main_ui_without_recursive_overlay_menu():
    source = (PROJECT_ROOT / "game" / "Town" / "StreetTavern.rpy").read_text(encoding="utf-8-sig")

    assert "def street_tavern_action_items():" in source
    assert 'Call("StreetTavernObjectMenu", room_object.object_id)' in source
    assert "label StreetTavernObjectMenu(object_id=\"\'):") in source
    assert "room_action_menu_item(_street_action)" in source
    assert "label street_tavern_menu:" not in source
    assert "label street_tavern_object_menu" not in source
    assert "renpy.display_menu" not in source
    assert "jump street_tavern" not in source
