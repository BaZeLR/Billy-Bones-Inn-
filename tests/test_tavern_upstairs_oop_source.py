from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_upstairs_uses_pure_action_list_without_build_label_or_room_loop():
    source = (ROOT / "game/Inn/TavernUpstairs.rpy").read_text(encoding="utf-8-sig")

    assert "def tavern_upstairs_action_items" in source
    assert "label TavernUpstairsBuildActions:" not in source
    assert "call TavernUpstairsBuildActions" not in source
    assert "while _upstairs_ui_return" not in source
    assert "rooms.get(\"TavernUpstairs\").visible_exits()" in source
    assert 'Call("TavernAmandaRoomDoor")' in source
    assert "movement_actions(target)" in source


def test_upstairs_callers_do_not_restore_through_build_wrapper():
    sandra = (ROOT / "game/Inn/TavernSandraRoom.rpy").read_text(encoding="utf-8-sig")
    amanda = (ROOT / "game/Inn/TavernAmandaRoom.rpy").read_text(encoding="utf-8-sig")

    assert "TavernUpstairsBuildActions" not in sandra + amanda
    assert "tavern_upstairs_action_items()" in sandra
    assert "label TavernAmandaRoomDoorLeave:" not in amanda
