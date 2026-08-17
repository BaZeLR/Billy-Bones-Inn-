from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (PROJECT_ROOT / path).read_text(encoding="utf-8-sig")


def test_tavern_kitchen_uses_curloc_and_room_registry():
    source = read_rel("game/Inn/TavernKitchen.rpy")
    entry = source.split("label TavernKitchen:", 1)[1].split("label TavernKitchenBuildActions:", 1)[0]
    actions = source.split("label TavernKitchenBuildActions:", 1)[1].split("label TavernKitchenShareTeaWithSandraAndBecky:", 1)[0]

    assert '$ CurLoc = "TavernKitchen"' in entry
    assert "get_registered_room(CurLoc) or TavernKitchenRoom" in entry
    assert "get_registered_room(CurLoc) or TavernKitchenRoom" in actions
    assert "$ CurrentRoom =" not in source
    assert "$ location =" not in source


def test_tavern_kitchen_entry_restores_room_media_after_entry_event():
    source = read_rel("game/Inn/TavernKitchen.rpy")
    entry = source.split("label TavernKitchen:", 1)[1].split("label TavernKitchenBuildActions:", 1)[0]

    gate_index = entry.index("call RoomEnterEventGate(CurLoc, False)")
    picture_index = entry.index("tavern_kitchen_picture()")
    assert gate_index < picture_index
    assert 'tavern_work_pop_mandatory_code("WineForDance", CurLoc)' in entry
    assert "DisplayTavernEventShort(time" not in entry


def test_tavern_kitchen_clock_rules_do_not_use_display_time_slot():
    source = read_rel("game/Inn/TavernKitchen.rpy")

    assert "int(time" not in source
    assert "DisplayTavernEventShort(time" not in source
    assert "12 <= int(hour or 0) < 18" in source


def test_tavern_storage_uses_same_vertical_slice_and_room_exit_time():
    source = read_rel("game/Inn/TavernStorage.rpy")
    entry = source.split("label TavernStorage:", 1)[1]

    assert '$ CurLoc = "TavernStorage"' in entry
    assert "get_registered_room(CurLoc) or TavernStorageRoom" in entry
    assert "$ CurrentRoom =" not in source
    assert "$ location =" not in source
    assert "RoomExit(label=\"Вернуться на кухню\", target=\"TavernKitchen\", minutes_to_pass=10)" in source
    assert "_storage_room.build_menu_sections()" in entry
    assert "AdvanceMovementTime" not in entry

    gate_index = entry.index("call RoomEnterEventGate(CurLoc, False)")
    picture_index = entry.index("tavern_storage_picture()")
    assert gate_index < picture_index
