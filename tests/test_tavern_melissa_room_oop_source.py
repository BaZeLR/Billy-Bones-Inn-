from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOM = (ROOT / "game/Inn/TavernMelissaRoom.rpy").read_text(encoding="utf-8")
EVENTS = (ROOT / "game/NPC/Girls/Melissa/MelissaEvents.rpy").read_text(encoding="utf-8")


def test_melissa_room_has_one_action_source_without_refresh_labels():
    assert "def tavern_melissa_room_action_items():" in ROOM
    assert "label TavernMelissaRoomBuildActions:" not in ROOM
    assert "label TavernMelissaRoomRestore:" not in ROOM
    assert "call TavernMelissaRoomBuildActions" not in ROOM + EVENTS
    assert "while _melissa_room_ui_return is None:" not in ROOM


def test_melissa_room_preserves_actions_events_objects_and_exits():
    assert 'household_room_issue_action_specs("melissa")' in ROOM
    assert 'Call("DoChore", "clean_upstairs_rooms", "TavernMelissaRoom", "", "")' in ROOM
    assert 'Call("UpstairsRoomSearch", "TavernMelissaRoom")' in ROOM
    assert "Прислушаться к Клариссе и Мелиссе" not in ROOM
    assert "Выслушать Клариссу и Мелиссу" not in ROOM
    assert "rooms.get(\"TavernMelissaRoom\").visible_game_items()" in ROOM
    assert "rooms.get(\"TavernMelissaRoom\").visible_exits()" in ROOM
    assert EVENTS.count("tavern_melissa_room_action_items()") == 3
