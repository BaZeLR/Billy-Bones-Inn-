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


def test_upstairs_bedroom_sounds_are_derived_from_npc_location_and_arousal():
    source = (ROOT / "game/Inn/TavernUpstairs.rpy").read_text(encoding="utf-8-sig")
    sound_projection = source.split("def tavern_upstairs_bedroom_sound_lines():", 1)[1].split("\n    def ", 1)[0]

    assert 'for npc_id in ("sandra", "melissa", "amanda")' in sound_projection
    assert 'room_code = "Tavern%sRoom" % npc_id.capitalize()' in sound_projection
    assert 'people.location(npc_id)' in sound_projection
    assert 'info.arousal_value()' in sound_projection
    assert 'int(info.arousal_value() or 0) < 65' in sound_projection
    assert "скрип кровати" in sound_projection
    assert "tavern_upstairs_description()" in source
