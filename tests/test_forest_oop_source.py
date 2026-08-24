from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
FOREST = (GAME / "Forest/Forest.rpy").read_text(encoding="utf-8-sig")
FOREST_FILES = "\n".join(path.read_text(encoding="utf-8-sig") for path in (GAME / "Forest").glob("*.rpy"))
CONSUMERS = "\n".join(
    (GAME / relative).read_text(encoding="utf-8-sig")
    for relative in (
        "NPC/Secondary/MelissaWerecatQuest.rpy", "Utilities/Fight/FightSystemRuntime.rpy",
        "Items/Crafting/SoapCraftAndAtticItems.rpy",
    )
)


def test_forest_uses_per_room_display_state_without_shared_text_scalars():
    source = FOREST_FILES + CONSUMERS
    assert 'room_obj.state.get("display_text", "")' in FOREST
    assert 'room_obj.state["display_text"]' in FOREST
    assert "ForestSavedText" not in source
    assert "ForestSubroomSavedText" not in source


def test_forest_has_two_action_sources_without_build_restore_labels_or_loops():
    source = FOREST_FILES + CONSUMERS
    assert "def forest_action_items():" in FOREST
    assert "def forest_subroom_action_items(room=None):" in FOREST
    for legacy in ("ForestBuildActions", "ForestRestore", "ForestSubroomBuildActions", "ForestSubroomRestore"):
        assert legacy not in source
    assert "_forest_ui_return" not in source
    assert "_forest_lake_ui_return" not in source


def test_forest_preserves_hunting_traps_werecat_shooting_spawns_horse_and_exits():
    for token in (
        'Call("FightStartHuntCurrentRoom")', 'Call("ShootingPracticeMenu", "Forest")',
        'Call("ForestSetTrap")', 'Call("ForestCheckTrap")',
        'Call("WerecatSetTrap", "Forest")', 'Call("WerecatCheckTrap", "Forest")',
        'Call("ForestLakeBath")', 'Call("ForestLakeWashHorse")',
        "rooms.get(\"Forest\").get_spawned_items()", "forest_room_get_spawned_items(room_obj)",
        "rooms.get(\"Forest\").visible_exits()", "room_obj.visible_exits()",
    ):
        assert token in FOREST


def test_all_seven_subrooms_use_shared_derived_actions_and_room_owned_text():
    for name in ("ForestCave", "ForestClearing", "ForestDarkWoods", "ForestHiddenPath", "ForestLake", "ForestSpring", "ForestWaterfall"):
        source = (GAME / f"Forest/{name}.rpy").read_text(encoding="utf-8-sig")
        assert "forest_room_set_saved_text(scene_runtime.text, rooms.current)" in source
        assert "forest_subroom_action_items(rooms.current)" in source
        assert "call screen main_ui" in source
