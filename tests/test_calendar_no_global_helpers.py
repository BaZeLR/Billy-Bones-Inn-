from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_script_has_calendar_class_without_global_calendar_helpers():
    source = (PROJECT_ROOT / "game" / "script.rpy").read_text(encoding="utf-8-sig")

    assert "class Calendar(object):" in source
    assert "default calendar_v2 = Calendar(" in source
    assert "daysInGame=0" in source
    assert "def calendar_" not in source
    assert "CalendarRuntime" not in source


def test_calendar_days_in_game_is_object_owned_and_incremented_by_day_rollover():
    source = (PROJECT_ROOT / "game" / "script.rpy").read_text(encoding="utf-8-sig")

    assert "self.daysInGame = _cal_int(daysInGame, 0)" in source
    assert "def _advance_one_day_fields(self):" not in source
    assert "self._advance_one_day_fields()" not in source
    assert "self.daysInGame += 1" in source
    assert "while self.minute >= 60:" in source
    assert "while self.hour >= 24:" in source
    advance_body = source.split("def advance_minutes(self, minutes):", 1)[1].split("def clock_minutes(self):", 1)[0]
    assert "sync_state" not in advance_body
    assert '"days_in_game": int(self.daysInGame)' in source


def test_calendar_does_not_keep_abstract_slot_or_variable_month_helpers():
    source = (PROJECT_ROOT / "game" / "script.rpy").read_text(encoding="utf-8-sig")

    forbidden = (
        "def advance_slots(",
        "def minutes_until_next_time_slot(",
        "def slot_start_hour(",
        "def total_minutes_runtime(",
        "def set_clock(",
        "def set_date(",
        "def set_time_slot(",
        "def set_from_day_number(",
        "def set_from_fields(",
        "def set_weekday_for_debug(",
        "def day_number_from_fields(",
        "def advance_day(",
        "def advance_days(",
        "def birth_record_from_ordinal(",
        "def make_birth_record(",
        "def birth_record(",
        "def birth_matches_today(",
        "renpy.store.age",
        "def periods_in_cycle(",
        "def days_in_month(",
        "def days_before_month(",
        "def days_in_cycle(",
        "def days_before_cycle(",
        "def is_long_cycle(",
    )
    for token in forbidden:
        assert token not in source


def test_runtime_uses_calendar_object_methods_not_global_calendar_helpers():
    forbidden = (
        "calendar_sync_state(",
        "calendar_set_time_slot(",
        "calendar_set_from_fields(",
        "calendar_advance_minutes(",
        "calendar_advance_slots(",
        "calendar_advance_days(",
        "calendar_format_date_ru(",
        "calendar_make_birth_record(",
        "calendar_birth_matches_today(",
        "calendar_v2.set_from_fields(",
        "calendar_v2.set_weekday_for_debug(",
        "calendar_v2.day_number_from_fields(",
        "CalendarRuntime",
    )
    for path in (PROJECT_ROOT / "game").rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        for token in forbidden:
            assert token not in source, "%s still contains %s" % (path.relative_to(PROJECT_ROOT), token)


def test_calendar_has_no_scalar_or_display_mirrors():
    script = (PROJECT_ROOT / "game" / "script.rpy").read_text(encoding="utf-8-sig")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (PROJECT_ROOT / "game").rglob("*.rpy")
    )

    for name in ("day", "month", "year", "week", "hour", "minute", "time", "dayspassed", "clock_minutes"):
        assert f"default {name} =" not in script
    for name in (
        "week_name", "month_name", "week_name_en", "month_name_en", "datestr",
        "calendar_weekday_name_ru", "calendar_month_name_ru",
        "calendar_weekday_name_en", "calendar_month_name_en",
        "calendar_cycle_name_ru", "calendar_cycle_name_en",
        "calendar_time_slot_name_ru", "calendar_time_slot_name_en",
    ):
        assert f"default {name} =" not in script
    assert "def sync_state(self):" not in script
    assert "calendar_v2.sync_state()" not in game_sources
    assert "calendar_v2.daysInGame" in game_sources
    assert "calendar_v2.time_slot()" in game_sources
