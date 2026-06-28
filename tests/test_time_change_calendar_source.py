from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_time_change_screen_defines_clock_targets_and_sets_clock_directly():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "TimeChangeMenu.rpy").read_text(encoding="utf-8-sig")

    assert "TIME_CHANGE_PERIOD_TARGETS" in source
    assert "calendar_v2.hud_data()" in source
    assert "calendar_v2.time_slot()" not in source
    assert "label ApplyTimePeriodChange(target_hour=8):" in source
    assert "def _time_current_hour():" in source
    assert "int(calendar_v2.hour or 0) < target_hour" in source
    assert "calendar_v2.hour = target_hour" in source
    assert "calendar_v2.minute = 0" in source
    assert "calendar_v2.set_time_slot" not in source

    assert "current_time = int(time or 0)" not in source
    assert "target_time" not in source
    assert "_time_label" not in source


def test_nextday_after_midnight_detection_uses_calendar_hour_not_old_slot():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay.rpy").read_text(encoding="utf-8-sig")
    body = source.split("def nextday_started_after_midnight():", 1)[1].split("def nextday_pick_post_sleep_event_label():", 1)[0]

    assert "int(calendar_v2.hour or 0) % 24" in body
    assert "return 0 <= current_hour < 6" in body
    assert "current_time = int(time or 0)" not in body
    assert "current_time == 4" not in body
