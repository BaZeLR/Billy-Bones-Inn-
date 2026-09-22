"""Exercise Clara residency through production predicates and schedule owners."""

from types import SimpleNamespace

import pytest

from tests.test_hordus_schedule_runtime import _clara_runtime, _exec_block, _set_day


@pytest.fixture
def runtime():
    clara, merchant, calendar, namespace = _clara_runtime()
    paintings = namespace["threads"]["claraPaintingsPath"]
    paintings.num, paintings.completed = 1, False
    case = SimpleNamespace(num=0, done=[False] * 4, completed=False, aborted=False)
    namespace["threads"]["claraMongolAccusation"] = case
    tavern = namespace["player"].tavern_management
    tavern.glory_hole = 0
    tavern.is_open_at = lambda weekday=None, hour=None: (
        (calendar.week if weekday is None else weekday) != 7
        and 12 * 60 <= namespace["npc_schedule_clock_minute"](hour) <= 20 * 60 + 30
    )
    _exec_block(
        "game/Utilities/General/NPC/HouseholdAI_ren.rpy",
        "    class HouseholdInfo(object):", "    HOUSEHOLD_NPC_DEFAULTS =", namespace,
    )
    hired = {name: SimpleNamespace(can_work_tavern=lambda: True) for name in ("georgett", "liza")}
    namespace["people"] = SimpleNamespace(get_info=lambda name: hired.get(name))
    namespace["kids_count_for_mothers"] = lambda *names: 0
    household = namespace["HouseholdInfo"]()
    namespace["household"] = household
    return SimpleNamespace(
        clara=clara, merchant=merchant, calendar=calendar, namespace=namespace,
        paintings=paintings, case=case, household=household,
    )


@pytest.mark.parametrize("num,completed,expected", [
    (0, False, False), (13, False, False), (14, False, True),
    (15, False, True), (16, True, True),
])
def test_existing_paintings_residency_threshold_is_preserved(runtime, num, completed, expected):
    runtime.paintings.num, runtime.paintings.completed = num, completed
    assert runtime.clara.tavern_resident() is expected


@pytest.mark.parametrize("num,completed", [(0, False), (1, False), (2, False), (3, False), (4, True)])
def test_accusation_route_residency_starts_only_after_arrival(runtime, num, completed):
    runtime.case.num, runtime.case.completed = num, completed
    runtime.case.done = [index < num for index in range(4)]
    assert runtime.clara.tavern_resident() is completed


def test_household_membership_is_derived_once_without_changing_existing_staff(runtime):
    previous = runtime.household.resident_ids()
    assert previous == ["you", "sandra", "melissa", "amanda", "georgett", "liza"]
    runtime.case.completed = True
    runtime.paintings.completed = True
    for _ in range(3):
        assert runtime.household.resident_ids() == previous + ["clara"]
        assert runtime.household.member_count() == len(previous) + 1
    assert runtime.clara.jobs == {}


def test_residency_rule_reads_the_same_owner_for_both_polarities(runtime):
    rule = runtime.namespace["room_rule_true"]
    positive = {"rule": "clara_tavern_resident"}
    negative = {"rule": "clara_tavern_resident", "resident": False}
    assert not rule(positive) and rule(negative)
    runtime.case.completed = True
    assert rule(positive) and not rule(negative)


def test_merchant_visit_is_preserved_for_nonresident_and_released_resident(runtime):
    _set_day(runtime.calendar, runtime.merchant.monthly_visit_days()[0])
    runtime.calendar.hour = 12
    assert runtime.clara.data.schedule_resolve() is runtime.merchant.schedule_resolve()
    runtime.case.completed = True
    assert runtime.clara.data.schedule_resolve() is runtime.merchant.schedule_resolve()
    assert runtime.clara.getLocation() == "MarketPlace"


@pytest.mark.parametrize("hour", [0, 6, 11, 16, 19, 22, 23])
def test_released_resident_does_not_return_to_wine_store(runtime, hour):
    runtime.case.completed = True
    for weekday in range(1, 8):
        runtime.calendar.week, runtime.calendar.hour = weekday, hour
        assert runtime.clara.getLocation() in ("TavernMelissaRoom", "TavernMain", "FridayDance", "MarketPlace")


@pytest.mark.parametrize("resident", [False, True])
@pytest.mark.parametrize("after_sixty_percent", [False, True])
def test_friday_dance_keeps_sixty_forty_split_with_correct_home(runtime, resident, after_sixty_percent):
    runtime.case.completed = resident
    runtime.calendar.week, runtime.calendar.hour = 5, 19
    runtime.namespace["procedural_randint"] = lambda low, high, key="": int(high * 0.6) + int(after_sixty_percent)
    entry = runtime.clara.data.schedule_resolve()
    assert entry.label == ("friday_dance_resident" if resident else "friday_dance")
    home = "TavernMelissaRoom" if resident else "WineStore"
    assert runtime.clara.getLocation() == (home if after_sixty_percent else "FridayDance")


def test_new_resident_uses_inherited_current_and_next_day_cleaning_assignment(runtime):
    runtime.case.completed = True
    ordinary_day = next(day for day in range(1, 29) if day not in runtime.merchant.monthly_visit_days() and day % 7 != 0)
    _set_day(runtime.calendar, ordinary_day)
    runtime.calendar.hour = 13
    runtime.clara.set_job_value("jobcleaning", 1)
    runtime.clara.set_job_value("jobcleaningtomorrow", 1)
    assert runtime.clara.is_tavern_worker()
    assert runtime.clara.schedule_entry().label == "tavern_cleaning_shift"
    assert runtime.clara.getLocation() == "TavernMain"
    runtime.clara.apply_tavern_job_plan()
    assert runtime.clara.job_value("jobcleaning") == 1
    assert runtime.clara.getLocation() == "TavernMain"


def test_custody_hides_clara_even_when_original_residency_was_reached(runtime):
    runtime.paintings.num = 14
    runtime.case.num = 1
    runtime.case.done[0] = True
    assert runtime.clara.tavern_resident()
    assert runtime.clara.getLocation() == ""
