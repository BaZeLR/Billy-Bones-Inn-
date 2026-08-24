from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOM = (ROOT / "game/Inn/TavernSandraRoom.rpy").read_text(encoding="utf-8")
EVENTS = (ROOT / "game/NPC/Girls/Sandra/SandraEvents.rpy").read_text(encoding="utf-8")


def test_sandra_room_uses_one_action_source_without_refresh_labels():
    assert "def tavern_sandra_room_action_items():" in ROOM
    assert "def tavern_sandra_room_text():" in ROOM
    assert "label TavernSandraRoomBuildActions:" not in ROOM
    assert "label TavernSandraRoomRestore:" not in ROOM
    assert "call TavernSandraRoomBuildActions" not in ROOM + EVENTS
    assert "while _sandra_room_ui_return is None:" not in ROOM
    object_text = ROOM.split('label TavernSandraRoomObjectText', 1)[1].split('label TavernSandraLedgerScene', 1)[0]
    assert "call TavernSandraRoomObjectMenu" not in object_text
    assert ROOM.count("tavern_sandra_room_text()") >= 3


def test_sandra_room_preserves_reputation_events_search_objects_and_exits():
    for token in (
        'household_room_issue_action_specs("sandra")',
        'Call("TavernSandraLedgerScene")',
        'story_event_action_items("TavernSandraRoom")',
        'Call("SandraSexEngine", "sandra", "TavernSandraRoom")',
        'Call("UpstairsRoomSearch", "TavernSandraRoom")',
        "rooms.get(\"TavernSandraRoom\").visible_game_items()",
        "rooms.get(\"TavernSandraRoom\").visible_exits()",
    ):
        assert token in ROOM
    assert EVENTS.count("tavern_sandra_room_action_items()") == 4
