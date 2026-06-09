from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_time_change_screen_defines_period_targets_and_sets_clock_directly():
    source = (PROJECT_ROOT / "game" / "Utilities" / "Time" / "TimeChangeMenu.rpy").read_text(encoding="utf-8-sig")

    assert "TIME_CHANGE_PERIOD_TARGETS" in source
    assert "calendar_v2.hud_data()" in source
    assert "calendar_v2.time_slot()" in source
    assert "label ApplyTimePeriodChange(target_time=0, target_hour=8):" in source
    assert "calendar_v2.hour = target_hour" in source
    assert "calendar_v2.minute = 0" in source
    assert "calendar_v2.set_time_slot" not in source

    assert "current_time = int(time or 0)" not in source
    assert "_time_label" not in source
