from pathlib import Path
import textwrap


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_PATH = PROJECT_ROOT / "devdocs" / "CalendarV2Blueprint.rpy"


def load_calendar_namespace():
    source = BLUEPRINT_PATH.read_text(encoding="utf-8-sig")
    marker = "init python:\n"
    assert marker in source
    body = source.split(marker, 1)[1]
    namespace = {}
    exec(textwrap.dedent(body), namespace)
    return namespace


def new_calendar(**kwargs):
    namespace = load_calendar_namespace()
    return namespace["Calendar"](**kwargs)


def test_calendar_initial_state_is_single_calendar_source():
    calendar = new_calendar()
    state = calendar.data()

    assert state["hour"] == 8
    assert state["minute"] == 0
    assert state["day"] == 1
    assert state["week"] == 1
    assert state["period"] == 1
    assert state["cycle"] == 1100
    assert state["daysInGame"] == 0
    assert state["time_code_name"] == "morning"
    assert state["moon_phase"] == "new_moon"


def test_calendar_time_slot_is_derived_from_hour_and_minute():
    cases = (
        (5, 59, "night"),
        (6, 0, "early_morning"),
        (7, 59, "early_morning"),
        (8, 0, "morning"),
        (10, 59, "morning"),
        (11, 0, "noon"),
        (12, 59, "noon"),
        (13, 0, "afternoon"),
        (15, 59, "afternoon"),
        (16, 0, "day"),
        (17, 59, "day"),
        (18, 0, "evening"),
        (20, 59, "evening"),
        (21, 0, "late_evening"),
        (22, 59, "late_evening"),
        (23, 0, "night"),
    )

    calendar = new_calendar()
    for hour, minute, expected_slot in cases:
        calendar.set_clock(hour, minute)
        assert calendar.data()["time_code_name"] == expected_slot


def test_calendar_exact_clock_interval_handles_overnight_windows():
    calendar = new_calendar()

    calendar.set_clock(8, 0)
    assert not calendar.is_between_clock(21, 30, 5, 30)

    calendar.set_clock(22, 0)
    assert calendar.is_between_clock(21, 30, 5, 30)

    calendar.set_clock(5, 30)
    assert calendar.is_between_clock(21, 30, 5, 30)

    calendar.set_clock(6, 0)
    assert not calendar.is_between_clock(21, 30, 5, 30)


def test_calendar_day_rollover_advances_calendar_date():
    calendar = new_calendar(hour=23, minute=30, day=1, week=1)
    calendar.advance_minutes(60)
    state = calendar.data()

    assert state["hour"] == 0
    assert state["minute"] == 30
    assert state["day"] == 2
    assert state["week"] == 2
    assert state["daysInGame"] == 1

def test_calendar_week_rollover_keeps_weekday_in_one_to_seven():
    calendar = new_calendar(hour=23, minute=30, day=7, week=7)
    calendar.advance_minutes(60)
    state = calendar.data()

    assert state["week"] == 1


def test_calendar_period_rollover_after_day_twenty_eight():
    calendar = new_calendar(hour=23, minute=30, day=28, week=7, period=1)
    calendar.advance_minutes(60)
    state = calendar.data()

    assert state["day"] == 1
    assert state["period"] == 2
    assert state["cycle"] == 1100


def test_calendar_cycle_rollover_after_period_thirteen():
    calendar = new_calendar(hour=23, minute=30, day=28, week=7, period=13, cycle=1100)
    calendar.advance_minutes(60)
    state = calendar.data()

    assert state["day"] == 1
    assert state["period"] == 1
    assert state["cycle"] == 1101


def test_calendar_hidden_moon_phase_and_girl_offset_are_computed():
    calendar = new_calendar(day=15)

    assert calendar.data()["moon_phase"] == "full_moon"
    assert calendar.moon_phase()["code_name"] == "full_moon"

    class GirlInfo:
        lunar_fertility = {"offset": 14}

    assert calendar.girl_lunar_state(GirlInfo())["code_name"] == "new_moon"


def test_calendar_sabbat_window_is_hidden_story_hook():
    calendar = new_calendar(day=7, week=4, period=1, hour=23, minute=0)
    window = calendar.data()["sabbat_window"]

    assert window is not None
    assert window["sabbat"] == "Yule"
    assert "ForestCave" in window["places"]

    calendar.set_clock(22, 59)
    assert calendar.data()["sabbat_window"] is None


def test_calendar_sleep_to_morning_advances_date_and_sets_clock():
    calendar = new_calendar(hour=23, minute=30, day=7, week=7)
    calendar.sleep_to_morning(8, 0)
    state = calendar.data()

    assert state["hour"] == 8
    assert state["minute"] == 0
    assert state["day"] == 8
    assert state["week"] == 1
    assert state["daysInGame"] == 1
