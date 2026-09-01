from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOM = (ROOT / "game/Inn/Backyard.rpy").read_text(encoding="utf-8-sig")
DOG = (ROOT / "game/NPC/Secondary/DogCompanion.rpy").read_text(encoding="utf-8-sig")
CRAFT = (ROOT / "game/Items/Crafting/SoapCraftAndAtticItems.rpy").read_text(encoding="utf-8-sig")
SHED = (ROOT / "game/Inn/Shed.rpy").read_text(encoding="utf-8-sig")
SHED_ACTIONS = "\n".join(
    (ROOT / path).read_text(encoding="utf-8-sig")
    for path in (
        "game/Utilities/General/Common/Actions.rpy",
        "game/Items/Resources/LumberItem.rpy",
        "game/Items/Resources/OldAxeItem.rpy",
    )
)


def test_backyard_has_one_action_source_without_builder_restore_or_mirrors():
    source = ROOM + DOG + CRAFT
    assert "def backyard_action_items():" in ROOM
    assert "label BackyardBuildActions:" not in ROOM
    assert "label BackyardRestore:" not in ROOM
    assert "BackyardBuildActions" not in source
    assert "BackyardRestore" not in source
    assert "BackyardSavedText" not in source
    assert "BackyardToiletBusy" not in source
    assert "while _backyard_ui_return is None:" not in ROOM


def test_backyard_object_results_use_explicit_text_not_boolean_protocol():
    assert 'label BackyardObjectMenu(object_id="", display_text=""):' in ROOM
    assert "refresh_only" not in ROOM
    assert 'BackyardToiletObject.state.get("busy", False)' in ROOM
    assert 'call BackyardObjectMenu("backyard_water_barrel", scene_runtime.text)' in ROOM


def test_backyard_preserves_objects_shooting_exits_dog_and_crafting():
    for object_id in ("backyard_toilet", "backyard_water_barrel", "backyard_firepit", "backyard_laundry", "backyard_ash_barrel", "backyard_dog_booth"):
        assert object_id in ROOM
    assert 'Call("ShootingPracticeMenu", "Backyard")' in ROOM
    assert "rooms.get(\"Backyard\").visible_exits()" in ROOM
    assert "call IntDogTalk(\"Backyard\")" in ROOM
    assert 'target="BackyardChooseSoapRecipe"' in ROOM
    assert "label BackyardChooseSoapRecipe:" in CRAFT
    assert 'call BackyardCookSoap("soap_recipe")' in CRAFT
    assert DOG.count("backyard_action_items()") == 3
    assert "stolyar_workshop_action_items()" not in DOG


def test_shed_has_no_refresh_label_or_recursive_room_loop():
    source = SHED + SHED_ACTIONS

    assert "label ShedRoomActions:" not in source
    assert "call ShedRoomActions" not in source
    assert "_shed_ui_return" not in source
    assert "jump Shed" not in SHED
    assert "build_shed_action_items()" in SHED
    assert "call screen main_ui" in SHED
