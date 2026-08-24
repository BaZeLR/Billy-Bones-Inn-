from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOM = (ROOT / "game/Inn/TavernAtic.rpy").read_text(encoding="utf-8-sig")
CRAFT = (ROOT / "game/Items/Crafting/SoapCraftAndAtticItems.rpy").read_text(encoding="utf-8-sig")


def test_attic_uses_room_owned_search_state_without_legacy_scalars():
    source = ROOM + CRAFT
    assert 'rooms.get(\"TavernAtic\").state.get("loot_found", False)' in source
    assert 'rooms.get(\"TavernAtic\").state.get("supply_loot_found", False)' in source
    assert "AtticLootFound" not in source
    assert "AtticSupplyLootFound" not in source


def test_attic_has_one_action_source_without_builder_restore_or_loop():
    assert "def tavern_atic_action_items():" in ROOM
    assert "label TavernAticBuildActions:" not in ROOM
    assert "label TavernAticRestore:" not in ROOM
    assert "TavernAticBuildActions" not in ROOM + CRAFT
    assert "TavernAticRestore" not in ROOM + CRAFT
    assert "while _atic_ui_return is None:" not in ROOM


def test_attic_preserves_loot_melissa_objects_and_exit():
    for item_id in ("recipe_book_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001", "droplets_001", "gunpowder_001"):
        assert item_id in ROOM
    assert 'story_event_available("TavernAtic", "melissa_bats")' in ROOM
    assert 'Call("checkTriggers", "TavernAtic", "melissa_bats", 0)' in ROOM
    assert "tavern_atic_visible_items()" in ROOM
    assert "rooms.get(\"TavernAtic\").visible_exits()" in ROOM
    assert 'SetField(main_ui_runtime, "action_items", tavern_atic_action_items())' in ROOM
    assert 'Jump("TavernAtic")' not in ROOM
