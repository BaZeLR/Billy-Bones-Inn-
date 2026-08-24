from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOM = (ROOT / "game/Inn/TavernMyRoom.rpy").read_text(encoding="utf-8-sig")
WINDOW = (ROOT / "game/Inn/TavernMyRoomWindow001.rpy").read_text(encoding="utf-8-sig")
ACTIONS = (ROOT / "game/Utilities/General/Common/Actions.rpy").read_text(encoding="utf-8-sig")


def test_my_room_has_one_action_source_without_builder_restore_or_loop():
    assert "def tavern_my_room_action_items():" in ROOM
    assert "label TavernMyRoomBuildActions:" not in ROOM
    assert "label TavernMyRoomRestore:" not in ROOM
    assert "TavernMyRoomBuildActions" not in ROOM + ACTIONS
    assert "TavernMyRoomRestore" not in ROOM + ACTIONS
    assert "while _my_room_ui_return is None:" not in ROOM


def test_my_room_has_no_hidden_action_text_mailbox():
    assert "action_override_text" not in ROOM + WINDOW + ACTIONS
    assert 'label TavernMyRoomObjectMenu(object_id="", display_text=""):' in ROOM
    assert 'call TavernMyRoomObjectMenu("myroom_window_001", _window_text)' in WINDOW
    assert "call TavernMyRoomObjectMenu(object_id, _room_text)" in ROOM


def test_my_room_preserves_objects_forest_floor_items_and_chest():
    for item_id in ("bed_001", "chest_001", "myroom_window_001", "myroom_attic_hatch_001", "rusty_hunter_rifle_001", "old_leather_cuirass_001"):
        assert item_id in ROOM
    assert 'travel_to_forest_actions("TavernMyRoom")' in ROOM
    assert "label TavernMyRoomOpenChest" in ROOM
    assert "label TavernMyRoomTakeFloorItem" in ROOM
    assert "player.appearance" in ROOM
