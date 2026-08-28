from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_day_start_checkpoint_freezes_state_after_report_without_reinitializing():
    next_day = source("game/Utilities/Time/NextDay.rpy")
    body = next_day.split("label NextDay(retlocname, timepassed):", 1)[1].split("default next_day_runtime", 1)[0]

    report = body.index("call screen nextday_report_card_overlay")
    release = body.index("$ calendar_v2.time_advance_blocked = 0")
    save = body.index('$ renpy.save("day-1"')
    room_entry = body.index("jump expression _nextday_return_label")
    checkpoint_tail = body[report:]

    assert report < release < save < room_entry
    assert 'if _nextday_return_label == "TavernMyRoom":' in checkpoint_tail
    assert 'extra_info=_day_start_save_name' in checkpoint_tail
    assert "include_screenshot=False" in checkpoint_tail
    assert "InitGameNPCs" not in checkpoint_tail
    assert "NextDay_NewDayEvents" not in checkpoint_tail
    assert "CreateTavernEvents" not in checkpoint_tail


def test_day_start_checkpoint_loads_through_the_real_bedroom_entry():
    next_day = source("game/Utilities/Time/NextDay.rpy")
    bedroom = source("game/Inn/TavernMyRoom.rpy")
    screens = source("game/screens.rpy")

    checkpoint_tail = next_day.split('$ renpy.save("day-1"', 1)[1].split("default next_day_runtime", 1)[0]
    bedroom_entry = bedroom.split("label TavernMyRoom:", 1)[1].split("label TavernMyRoomObjectMenu", 1)[0]

    assert "jump expression _nextday_return_label" in checkpoint_tail
    assert '$ rooms.enter("TavernMyRoom")' in bedroom_entry
    assert "tavern_my_room_scene_state()" in bedroom_entry
    assert "tavern_my_room_action_items()" in bedroom_entry
    assert "renpy.save(" not in bedroom_entry
    assert 'textbutton "Утро" action FilePage("day")' in screens
