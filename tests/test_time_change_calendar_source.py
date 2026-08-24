from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_time_change_screen_defines_clock_targets_and_sets_clock_directly():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "TimeChangeMenu.rpy").read_text(encoding="utf-8-sig")

    assert "TIME_CHANGE_PERIOD_TARGETS" in source
    assert "calendar_v2.hud_data()" in source
    assert "def _time_minutes_to_hour(target_hour):" in source
    assert "current_minutes = (int(calendar_v2.hour or 0) % 24) * 60" in source
    assert "target_minutes = (int(target_hour or 0) % 24) * 60" in source
    assert 'Call("AdvanceTimeOnly", int(minutes_to_add or 0))' in source
    assert "label ApplyTimeSkip" not in source
    assert "jump expression return_loc" not in source
    assert "label ShowTimeChangeMenu" not in source
    assert "label HideTimeChangeMenu" not in source
    assert "calendar_v2.set_time_slot" not in source
    assert "screen time_change_panel():" in source
    assert "time_change_card_overlay" not in source
    assert "Hide(" not in source
    assert 'SetField(main_ui_runtime, "overlay", "")' in source

    assert "current_time = int(time or 0)" not in source
    assert "target_time" not in source
    assert "_time_label" not in source


def test_nextday_after_midnight_detection_uses_calendar_hour_not_old_slot():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay.rpy").read_text(encoding="utf-8-sig")
    body = source.split("def nextday_started_after_midnight():", 1)[1].split("label NextDay(", 1)[0]

    assert "int(calendar_v2.hour or 0) % 24" in body
    assert "return 0 <= current_hour < 6" in body
    assert "current_time = int(time or 0)" not in body
    assert "current_time == 4" not in body
