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


def test_tavern_kitchen_entry_keeps_room_and_event_media_separate():
    source = read_rel("game/Inn/TavernKitchen.rpy")
    entry = source.split("label TavernKitchen:", 1)[1].split("label TavernKitchenBuildActions:", 1)[0]

    picture_index = entry.index("tavern_kitchen_picture()")
    gate_index = entry.index("call RoomEnterEventGate(CurLoc, False)")
    assert picture_index < gate_index
    assert 'tavern_work_pop_mandatory_code("WineForDance", CurLoc)' in entry
    assert "DisplayTavernEventShort(time" not in entry


def test_tavern_kitchen_clock_rules_do_not_use_display_time_slot():
    source = read_rel("game/Inn/TavernKitchen.rpy")

    assert "int(time" not in source
    assert "DisplayTavernEventShort(time" not in source
    assert "12 <= int(hour or 0) < 18" in source
