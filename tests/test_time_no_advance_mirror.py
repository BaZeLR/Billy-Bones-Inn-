from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_time_uses_calendar_without_last_advanced_minutes_mirror_or_restore_wrapper():
    source = "\n".join(path.read_text(encoding="utf-8-sig") for path in (ROOT / "game").rglob("*.rpy"))
    advance = (ROOT / "game/Utilities/Time/AdvanceTime.rpy").read_text(encoding="utf-8-sig")
    assert "LastAdvancedMinutes" not in source
    assert "AdvanceTimeAndRestore" not in source
    assert "label AdvanceTime(" not in advance
    assert "advanced_minutes = max(0, int(minutes_to_add or 60))" in advance
    assert "calendar_v2.advance_minutes(advanced_minutes)" in advance
