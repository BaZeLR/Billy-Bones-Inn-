from pathlib import Path
from types import SimpleNamespace
import io
import json
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _exec_block(path, start, end, namespace):
    source = (ROOT / path).read_text(encoding="utf-8-sig")
    block = start + source.split(start, 1)[1].split(end, 1)[0]
    exec(textwrap.dedent(block), namespace)


def _runtime(first_weekday=1, cycle=1080, period=1):
    calendar = SimpleNamespace(
        cycle=cycle, period=period, day=1, week=first_weekday,
        hour=12, minute=0, daysInGame=0,
    )
    calendar.clock_minutes = lambda: calendar.hour * 60 + calendar.minute
    namespace = {
        "calendar_v2": calendar,
        "room_rule_true": lambda condition: condition is None or bool(condition),
        "register_room_rule": lambda condition: condition,
        "people_normalize_id": lambda name: str(name).strip().lower(),
        "BaseNPC": type("BaseNPC", (), {}),
    }
    _exec_block(
        "game/Utilities/General/Classes/RoomTemplate.rpy",
        "    class RoomSchedule(object):", "    class Room(object):", namespace,
    )
    market_source = (ROOT / "game/Town/Market/MarketPlace.rpy").read_text(encoding="utf-8-sig")
    market_schedule = market_source.split("        schedule=", 1)[1].split(
        "        custom_properties=", 1
    )[0].strip().rstrip(",")
    market = eval(market_schedule, namespace)
    namespace["rooms"] = {"MarketPlace": market}
    _exec_block(
        "game/Utilities/General/NPC/PeopleRuntime.rpy",
        "    def npc_schedule_clock_minute", "    class NPCHourScheduleEntry", namespace,
    )
    _exec_block(
        "game/Utilities/General/NPC/PeopleRuntime.rpy",
        "    class PeopleData(object):", "    def npc_interval_schedule_load_all", namespace,
    )
    source = (ROOT / "game/NPC/Secondary/InitHordus.rpy").read_text(encoding="utf-8-sig")
    exec(textwrap.dedent(source.split("init python:\n", 1)[1].split("\ndefine ", 1)[0]), namespace)
    return namespace["HordusData"](), calendar, market


def _set_day(calendar, day, first_weekday=1):
    calendar.day = day
    calendar.week = (first_weekday + day - 2) % 7 + 1
    calendar.daysInGame = day - 1


@pytest.mark.parametrize("first_weekday", range(1, 8))
def test_exactly_two_distinct_open_dates_stable_through_the_month(first_weekday):
    for period in range(1, 13):
        data, calendar, market = _runtime(first_weekday, period=period)
        state_before = dict(data.__dict__)
        dates = data.monthly_visit_days()
        assert len(dates) == len(set(dates)) == 2
        assert dates == tuple(sorted(dates))
        for day in dates:
            weekday = (first_weekday + day - 2) % 7 + 1
            assert 1 <= day <= 28
            assert weekday != 7
            assert market.is_open(weekday, 12)
        for day in range(1, 29):
            _set_day(calendar, day, first_weekday)
            assert data.monthly_visit_days() == dates
        assert data.__dict__ == state_before


def test_recreated_data_and_calendar_restore_the_same_dates_without_saved_plan():
    data, calendar, _ = _runtime(first_weekday=4, cycle=1082, period=9)
    expected = data.monthly_visit_days()
    restored, restored_calendar, _ = _runtime(first_weekday=4, cycle=1082, period=9)
    _set_day(restored_calendar, 22, first_weekday=4)
    assert restored.monthly_visit_days() == expected
    assert "monthly_visit_days" not in data.__dict__
    assert "monthly_visit_days" not in restored.__dict__


def test_monthly_ranking_changes_with_month_and_cycle():
    data, calendar, _ = _runtime()
    visits = set()
    for cycle in (1080, 1081):
        calendar.cycle = cycle
        for period in range(1, 13):
            calendar.period = period
            visits.add(data.monthly_visit_days())
    assert len(visits) > 12


@pytest.mark.parametrize("hour,minute,present", [(11, 59, False), (12, 0, True), (17, 59, True), (18, 0, False)])
def test_visit_clock_boundaries_and_nonvisit_dates(hour, minute, present):
    data, calendar, _ = _runtime()
    dates = data.monthly_visit_days()
    _set_day(calendar, dates[0])
    calendar.hour, calendar.minute = hour, minute
    assert data.getLocation() == ("MarketPlace" if present else "")
    assert (data.schedule_resolve() is not None) is present
    _set_day(calendar, next(day for day in range(1, 29) if day not in dates))
    assert data.getLocation() == ""


def test_explicit_clock_queries_use_the_shared_interval():
    data, calendar, _ = _runtime()
    _set_day(calendar, data.monthly_visit_days()[0])
    for value, expected in ((11, ""), (12, "MarketPlace"), (719, ""), (720, "MarketPlace"), (1079, "MarketPlace"), (1080, "")):
        assert data.getLocation(calendar.week, value) == expected
    assert data.getLocation(7, 12) == ""


def test_friday_visit_ends_before_dance():
    data, calendar, _ = _runtime()
    for period in range(1, 13):
        calendar.period = period
        for day in data.monthly_visit_days():
            if (day - 1) % 7 + 1 == 5:
                _set_day(calendar, day)
                assert data.getLocation(5, 1079) == "MarketPlace"
                assert data.getLocation(5, 1080) == ""
                return
    pytest.fail("No Friday visit found in twelve deterministic months")


def test_market_schedule_owns_eligible_weekdays_and_closure():
    data, calendar, market = _runtime()
    market.weekdays = [2, 4]
    dates = data.monthly_visit_days()
    assert len(dates) == 2
    assert all((day - 1) % 7 + 1 in (2, 4) for day in dates)
    _set_day(calendar, dates[0])
    assert data.getLocation() == "MarketPlace"
    market.condition = False
    assert data.monthly_visit_days() == ()
    assert data.getLocation() == ""


def test_catalog_has_one_price_per_existing_product():
    data, _, _ = _runtime()
    assert data.catalog == {
        "cursed_sofa_001": 600,
        "luxury_soap_001": 45,
        "libido_tincture_001": 60,
        "special_mushroom_001": 35,
    }


def _clara_runtime():
    hordus_data, calendar, market = _runtime()
    namespace = hordus_data.monthly_visit_days.__globals__
    namespace.update({
        "json": json,
        "renpy": SimpleNamespace(
            loadable=lambda path: (ROOT / "game" / path).is_file(),
            file=lambda path: io.BytesIO((ROOT / "game" / path).read_bytes()),
        ),
        "HordusStaticData": hordus_data,
        "room_rule_registry": {},
        "people_to_int": lambda value, default=0: int(value) if value is not None else default,
        "procedural_randint": lambda low, high, key="": low,
        "current_game_day": lambda: calendar.daysInGame,
        "household_morning_issue_matches": lambda *args, **kwargs: False,
        "household": SimpleNamespace(barber_appointments={}),
        "tavern": SimpleNamespace(renovation_complete=lambda code: False),
        "player": SimpleNamespace(tavern_management=SimpleNamespace(
            breakfast=SimpleNamespace(event_active=False, present_ids=[]),
            is_open_at=lambda weekday=None, hour=None: (
                (calendar.week if weekday is None else weekday) != 7
                and 720 <= namespace["npc_schedule_clock_minute"](hour) <= 1230
            ),
        )),
        "threads": {
            "claraMongolAccusation": SimpleNamespace(done=[False] * 4, completed=False),
            "claraPaintingsPath": SimpleNamespace(num=15, completed=True),
            "claraTavernVisit": SimpleNamespace(num=7, completed=True),
        },
    })
    _exec_block(
        "game/Utilities/General/Classes/GameObjectTemplate.rpy",
        "    def register_room_rule", "    def restore_game_object_runtime", namespace,
    )
    _exec_block(
        "game/Utilities/General/NPC/PeopleRuntime.rpy",
        "    class NPCHourScheduleEntry", "    def npc_schedule_entry_state", namespace,
    )
    _exec_block(
        "game/Utilities/General/NPC/PeopleRuntime.rpy",
        "    class PeopleInfo(object):", "\ndefault people", namespace,
    )
    _exec_block(
        "game/NPC/Girls/Clara/InitClara.rpy",
        "    class ClaraData(PeopleData):", "define ClaraStaticData", namespace,
    )
    clara = namespace["ClaraInfo"].__new__(namespace["ClaraInfo"])
    clara.name = clara.code_name = "clara"
    clara.data = namespace["ClaraData"]()
    clara.jobs = {}
    clara.day_location_override_day = -1
    clara.day_location_override_code = ""
    namespace["Clara"] = clara
    namespace["rooms"]["TavernMain"] = SimpleNamespace(state={})
    return clara, hordus_data, calendar, namespace


@pytest.mark.parametrize("competing_label,tavern_stage", [
    ("melissa_tavern_visit", 6),
    ("melissa_room_visit", 3),
    ("tavern_resident_day", 7),
])
def test_late_game_routine_visits_do_not_hide_clara_on_merchant_dates(competing_label, tavern_stage):
    clara, hordus_data, calendar, namespace = _clara_runtime()
    namespace["threads"]["claraTavernVisit"].num = tavern_stage
    if competing_label != "tavern_resident_day":
        namespace["threads"]["claraPaintingsPath"].num = 0
        namespace["threads"]["claraPaintingsPath"].completed = False
    calendar.hour = 16
    for period in range(1, 13):
        calendar.period = period
        for day in hordus_data.monthly_visit_days():
            _set_day(calendar, day)
            rows = clara.data.schedule_entries_for_today()
            competing = next(row for row in rows if row.label == competing_label)
            if competing.matches():
                assert clara.data.schedule_resolve() is hordus_data.schedule_resolve()
                assert clara.getLocation() == hordus_data.getLocation() == "MarketPlace"
                return
    pytest.fail("No overlapping ordinary visit found in twelve merchant months")


@pytest.mark.parametrize("detained_stage", [8, 9, 10, 11])
def test_merchant_schedule_does_not_override_clara_detention(detained_stage):
    clara, hordus_data, calendar, namespace = _clara_runtime()
    _set_day(calendar, hordus_data.monthly_visit_days()[0])
    paintings = namespace["threads"]["claraPaintingsPath"]
    paintings.num, paintings.completed = detained_stage, False
    assert hordus_data.getLocation() == "MarketPlace"
    assert clara.getLocation() == ""
    clara.set_day_location_override("TavernMelissaRoom")
    assert clara.getLocation() == ""


def test_merchant_schedule_preserves_clara_forced_room_until_override_expires():
    clara, hordus_data, calendar, _ = _clara_runtime()
    _set_day(calendar, hordus_data.monthly_visit_days()[0])
    assert clara.getLocation() == "MarketPlace"
    clara.set_day_location_override("TavernMelissaRoom")
    assert clara.getLocation() == "TavernMelissaRoom"
    assert hordus_data.getLocation() == "MarketPlace"
    clara.day_location_override_day -= 1
    assert clara.getLocation() == "MarketPlace"


def _set_merchant_friday(hordus_data, calendar):
    for period in range(1, 13):
        calendar.period = period
        for day in hordus_data.monthly_visit_days():
            if (day - 1) % 7 + 1 == 5:
                _set_day(calendar, day)
                return
    pytest.fail("No Friday merchant visit found")


@pytest.mark.parametrize("current_hour", [12, 18])
def test_clara_explicit_visit_queries_forward_query_clock_not_current_clock(current_hour):
    clara, hordus_data, calendar, _ = _clara_runtime()
    _set_merchant_friday(hordus_data, calendar)
    calendar.hour = current_hour
    assert clara.data.schedule_resolve(5, 12) is hordus_data.schedule_resolve(5, 12)
    assert clara.getLocation(5, 12) == hordus_data.getLocation(5, 12) == "MarketPlace"
    assert hordus_data.getLocation(5, 18) == ""
    assert clara.getLocation(5, 18) != "MarketPlace"
    assert clara.data.schedule_resolve(5, 18).label != "monthly_market_visit"


def test_amanda_friday_claim_checks_clara_at_nineteen_even_during_merchant_visit():
    clara, hordus_data, calendar, namespace = _clara_runtime()
    _set_merchant_friday(hordus_data, calendar)
    calendar.hour = 12
    queried = []

    def location(person, weekday_value, time_value):
        queried.append((person, weekday_value, time_value))
        return "FridayDance" if person == "alber" else clara.getLocation(weekday_value, time_value)

    namespace["people"] = SimpleNamespace(location=location)
    _exec_block(
        "game/NPC/Girls/Amanda/InitAmanda.rpy",
        "        def legare_claims_first_friday_dance", "        def dress_change_other_saw_text", namespace,
    )
    assert clara.getLocation() == hordus_data.getLocation() == "MarketPlace"
    assert clara.getLocation(5, 19 * 60) == "FridayDance"
    assert namespace["legare_claims_first_friday_dance"](None) is False
    assert queried == [("alber", 5, 19 * 60), ("clara", 5, 19 * 60)]


@pytest.mark.parametrize("job", ["jobkitchen", "jobcleaning", "jobwaitress", "jobwhore", "jobgloryhole"])
def test_registered_resident_keeps_assigned_shift_on_merchant_day(job):
    clara, hordus_data, calendar, namespace = _clara_runtime()
    _set_day(calendar, hordus_data.monthly_visit_days()[0])
    calendar.hour = 16
    clara.jobs[job] = 1
    namespace["player"].tavern_management.is_open_at = lambda weekday_value, time_value: True
    namespace["GirlWardrobeState"] = SimpleNamespace(from_saved=lambda saved, sex_state, base: saved)
    namespace["ClaraStaticData"] = clara.data
    _exec_block(
        "game/Utilities/General/NPC/PeopleRuntime.rpy",
        "    class PeopleRegistry(object):", "    def npc_schedule_clock_minute", namespace,
    )
    registry = namespace["PeopleRegistry"]()
    namespace["people"] = registry
    registry.register(clara.data, clara)
    competing = clara.tavern_service_schedule_entry() if job in ("jobwhore", "jobgloryhole") else clara.tavern_regular_job_schedule_entry()
    merchant_visit = hordus_data.schedule_resolve()
    assert competing is not None and competing.matches()
    assert competing.priority < merchant_visit.priority
    assert registry.get_info("clara") is clara
    assert registry.schedule_entry("clara").label == competing.label
    assert registry.location("clara") == competing.selected_location()
    assert hordus_data.getLocation() == "MarketPlace"
    clara.jobs.clear()
    assert registry.schedule_entry("clara") is merchant_visit
    assert registry.location("clara") == "MarketPlace"
