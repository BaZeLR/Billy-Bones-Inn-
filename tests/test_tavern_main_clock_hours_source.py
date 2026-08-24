from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_tavern_main_closed_state_uses_clock_hours_not_day_slot():
    source = (PROJECT_ROOT / "game" / "Inn" / "TavernMain.rpy").read_text(encoding="utf-8-sig")

    assert "def tavern_main_late_closed()" in source
    assert "current_hour >= 23 or current_hour < 6" in source
    assert "def tavern_main_sunday_service_closed()" in source
    assert "return int(calendar_v2.week or 0) == 7" in source
    assert "return int(calendar_v2.week or 0) != 7 and not tavern_main_late_closed()" in source
    assert "def tavern_main_friday_dance_closed()" in source
    assert "18 <= int(calendar_v2.hour or 0) < 22" in source
    assert 'state["closed_text"]' not in source
    assert 'closed_text = tavern_main_closed_text()' in source
    assert "elif time > 3" not in source
    assert "time_slots=[0, 1, 2, 3, 4]" not in source
    assert 'start="06:00", end="22:59"' in source


def test_tavern_preopening_is_before_noon_by_clock():
    source = (PROJECT_ROOT / "game" / "Inn" / "TavernMain.rpy").read_text(encoding="utf-8-sig")

    preopening = source.split("def tavern_preopening_mode():", 1)[1].split("def tavern_main_late_closed():", 1)[0]
    assert "6 <= int(calendar_v2.hour or 0) < 12" in preopening
    assert "int(time or 0) < 4" not in preopening


def test_tavern_main_sets_day_night_room_picture_explicitly_for_main_ui():
    source = (PROJECT_ROOT / "game" / "Inn" / "TavernMain.rpy").read_text(encoding="utf-8-sig")

    assert 'bg_picture="images/tavern/mainhall/main_hall.png"' in source
    assert 'scene_runtime.picture = "images/tavern/mainhall/main_hall_night.png" if int(calendar_v2.hour or 0) >= 18 or int(calendar_v2.hour or 0) < 6 else "images/tavern/mainhall/main_hall.png"' in source
    assert 'show bg TavernMain' not in source
    assert "call TavernShowImage" not in source
    assert "def tavern_main_room_picture" not in source
