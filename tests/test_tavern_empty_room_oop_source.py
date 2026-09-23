from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_empty_room_has_direct_actions_without_build_loop():
    source = (ROOT / "game/Inn/TavernEmptyRoom.rpy").read_text(encoding="utf-8-sig")

    assert "label TavernEmptyRoomBuildActions:" not in source
    assert "call TavernEmptyRoomBuildActions" not in source
    assert "while _empty_room_ui_return" not in source
    assert 'Call("UpstairsRoomSearch", "TavernEmptyRoom")' in source
    assert 'Call("TavernEmptyRoomObjectMenu"' not in source
    assert "game_items=[]" in source
    assert "rooms.get(\"TavernEmptyRoom\").visible_exits()" in source


def test_relocated_peephole_keeps_existing_client_event_flow():
    source = (ROOT / "game/Inn/TavernEmptyRoom.rpy").read_text(encoding="utf-8-sig")

    assert 'object_id="tavern_empty_room_peephole"' in source
    assert 'action_id="peek_client_room"' in source
    assert 'action_id="peek_empty_client_room"' in source
    assert 'call checkTriggers("TavernEmptyRoom", "tavern_client_room", 0)' in source
    assert "label TavernEmptyRoomPeekClient:" in source
    assert "label TavernEmptyRoomPeekEmpty:" in source
    bedroom = (ROOT / "game/Inn/TavernMyRoom.rpy").read_text(encoding="utf-8-sig")
    assert '"tavern_empty_room_peephole"' in bedroom
    assert '"myroom_guest_peephole"' not in bedroom
