"""Exercise authored Clara gates with the real clock, event and state owners.

Ren'Py dialogue/navigation and theft encounter execution remain UI-test concerns.
Only unrelated engine ports are stubbed; no availability predicate is copied here.
"""

import ast
import builtins
from types import SimpleNamespace

import pytest

from tests.test_tavern_renovations_runtime import _exec_definitions, _python_nodes


@pytest.fixture
def runtime():
    namespace = {
        "_story_range_type": range,
        "renpy": SimpleNamespace(log=lambda *args: None),
        "procedural_shuffle": lambda sequence, **kwargs: None,
        "register_room_rule": lambda rule: rule,
        "room_rule_true": lambda rule: rule is None,
        "DressTopPart": {},
        "DressBottomPart": {},
    }
    for path, names in (
        ("script.rpy", {"CALENDAR_START_CYCLE", "MOON_PHASE_NAMES_EN", "_cal_int", "Calendar"}),
        ("Utilities/General/Player/Player.rpy", {"player_to_int", "PlayerHorse"}),
        ("Utilities/General/NPC/PeopleRuntime.rpy", {"people_to_int", "GirlWardrobeState"}),
        ("Utilities/General/Classes/RoomTemplate.rpy", {"RoomSchedule"}),
        ("Utilities/General/Common/CheckDailyEvent.rpy", {"_daily_int", "_daily_match_time", "DailyEventRuntime"}),
    ):
        _exec_definitions(path, names, namespace)
    for path in (
        "Utilities/General/Events/conditions.rpy",
        "Utilities/General/Events/events.rpy",
        "Utilities/General/Events/threads.rpy",
    ):
        names = {node.name for node in _python_nodes(path) if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        _exec_definitions(path, names, namespace)

    calendar = namespace["Calendar"](hour=19, day=20, week=6, daysInGame=19)
    horse = namespace["PlayerHorse"]()
    horse.theft_attempted = True
    wardrobe = namespace["GirlWardrobeState"]()
    wardrobe.add_owned("thiefdress")
    player = SimpleNamespace(horse=horse, stats=SimpleNamespace(exploration=100))
    clara = SimpleNamespace(wardrobe=wardrobe, market_evening_roll=True, market_evening_roll_day=19)
    namespace.update(
        calendar_v2=calendar,
        player=player,
        Clara=clara,
        daily_events=namespace["DailyEventRuntime"](),
        event_runtime=SimpleNamespace(fired_day=-1, fired_keys_today=[], active_thread=None),
        npc_relationship_level=lambda person: {"phase_index": 6},
        current_game_day=lambda: calendar.daysInGame,
        people=SimpleNamespace(get_info=lambda person: clara, location=lambda person: "WineStore"),
    )
    # Use the real market schedule expression, without constructing its UI/actions.
    room_node = next(
        node for node in _python_nodes("Town/Market/MarketPlace.rpy")
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "MarketPlaceRoomDefinition" for target in node.targets)
    )
    schedule_node = next(keyword.value for keyword in room_node.value.keywords if keyword.arg == "schedule")
    schedule = eval(compile(ast.Expression(schedule_node), "MarketPlace.rpy", "eval"), namespace)
    market = SimpleNamespace(is_open=schedule.is_open)
    namespace["rooms"] = SimpleNamespace(
        current_code="MarketPlace",
        get=lambda name: market if name == "MarketPlace" else SimpleNamespace(is_open=lambda: True),
    )
    # Other NPCs/services occur in the production scope but not these predicates.
    for name in namespace["_story_condition_scope"].__code__.co_names:
        if not hasattr(builtins, name):
            namespace.setdefault(name, None)
    _exec_definitions(
        "Utilities/General/Classes/StoryEventRuntime.rpy",
        {"claraMongolMarketConditions", "claraThreadList"}, namespace,
    )
    threads = {data.name: namespace["createThread"](data) for data in namespace["claraThreadList"]}
    namespace["threads"] = threads
    for thread in threads.values():
        thread.data.initConditions()
        for events in thread.data.triggers:
            for event in events:
                event.initConditions()
    threads["claraPaintingsPath"].advanceTo(1)
    threads["claraForestSofa"].advanceTo(3)
    return SimpleNamespace(
        namespace=namespace, calendar=calendar, player=player, clara=clara,
        market=market, threads=threads, daily_events=namespace["daily_events"],
        booklet=threads["claraBookletMarket"], forest=threads["claraForestSofa"],
        sabbath=threads["claraMoonSabbath"],
    )


@pytest.mark.parametrize("stage", [1, 2])
@pytest.mark.parametrize("missing", ["theft", "exploration", "paintings", "roll_day", "roll"])
def test_both_mongol_market_stages_require_every_authored_gate(runtime, stage, missing):
    event = runtime.booklet.getevent(stage)
    assert event.canTrigger()
    if missing == "theft":
        runtime.player.horse.theft_attempted = False
    elif missing == "exploration":
        runtime.player.stats.exploration = 99
    elif missing == "paintings":
        runtime.threads["claraPaintingsPath"].done[0] = False
    elif missing == "roll_day":
        runtime.clara.market_evening_roll_day -= 1
    else:
        runtime.clara.market_evening_roll = False
    assert not event.canTrigger()


@pytest.mark.parametrize("hour,minute,expected", [(18, 59, False), (19, 0, True), (22, 59, True), (23, 0, False)])
def test_mongol_market_entry_uses_actual_closed_market_clock(runtime, hour, minute, expected):
    runtime.calendar.hour, runtime.calendar.minute = hour, minute
    assert runtime.market.is_open() == (hour == 18)
    for stage in (1, 2):
        assert runtime.booklet.getevent(stage).canTrigger() is expected


def test_mongol_market_excludes_friday_and_sunday(runtime):
    calendar = runtime.namespace["Calendar"](hour=19)
    runtime.namespace["calendar_v2"] = calendar
    for weekday in range(1, 8):
        assert calendar.week == weekday
        runtime.clara.market_evening_roll_day = calendar.daysInGame
        for stage in (1, 2):
            assert runtime.booklet.getevent(stage).canTrigger() == (weekday not in (5, 7))
        calendar.advance_minutes(1440)


def test_pending_theft_event_does_not_unlock_mongol(runtime):
    horse = runtime.player.horse
    horse.theft_attempted = False
    horse.acquire("Test horse", 1000)
    runtime.daily_events.add("", "TavernStable", 7, "=", 1, 0, "StableHorseTheft", "TavernStableHorseTheftAttempt", "none")
    assert runtime.daily_events.exists("", "StableHorseTheft") == 1
    assert not runtime.booklet.getevent(1).canTrigger()
    assert not horse.theft_attempted


def test_recorded_theft_attempt_survives_horse_acquisition_and_removal(runtime):
    horse = runtime.namespace["PlayerHorse"]()
    assert not horse.theft_attempted
    horse.acquire("First horse", 1000)
    assert not horse.theft_attempted
    horse.theft_attempted = True  # The actual encounter writer is covered by Ren'Py tests.
    assert horse.remove() == "First horse"
    assert horse.theft_attempted
    assert horse.acquire("Replacement", 1200)
    assert horse.theft_attempted
    horse.mark_stolen()
    assert horse.theft_attempted
    assert horse.acquire("Third horse", 900)
    assert horse.theft_attempted


@pytest.mark.parametrize("elapsed,expected", [(0, False), (6, False), (7, True), (8, True)])
def test_arrest_rumor_waits_seven_days_after_wine_lie(runtime, elapsed, expected):
    runtime.booklet.advanceTo(4)
    runtime.booklet.setDay()
    runtime.calendar.advance_minutes(elapsed * 1440)
    event = runtime.booklet.getevent(4)
    assert event.target == "story_clara_market_booklet_5"
    assert event.canTrigger(runtime.booklet.day) is expected


def test_wine_lie_requires_clara_in_wine_store(runtime):
    event = runtime.booklet.getevent(3)
    assert event.target == "story_clara_market_booklet_4"
    assert event.canTrigger()
    runtime.namespace["people"].location = lambda person: "TavernMain"
    assert not event.canTrigger()


@pytest.mark.parametrize("booklet_stage,expected", [(2, False), (3, True), (4, True), (8, True)])
def test_ordinary_forest_follow_opens_after_deal_without_release_completion(runtime, booklet_stage, expected):
    runtime.booklet.advanceTo(booklet_stage)
    runtime.forest.advanceTo(0)
    runtime.calendar.hour = 15
    assert not runtime.booklet.completed
    events = runtime.forest.getAvailableEvents()
    assert bool(events) is expected
    if expected:
        assert events[0].target == "story_clara_forest_follow_0"


@pytest.mark.parametrize("missing", ["moon", "saturday", "closed_market", "exploration", "forest_request", "costume", "forest_not_aborted"])
def test_sabbath_requires_each_live_gate(runtime, missing):
    event = runtime.sabbath.getevent(0)
    assert event.canTrigger(runtime.sabbath.day)
    if missing == "moon":
        runtime.calendar.advance_minutes(7 * 1440)
    elif missing == "saturday":
        runtime.calendar.day = 19
        runtime.calendar.daysInGame = 18
        runtime.calendar.week = 5
    elif missing == "closed_market":
        runtime.market.is_open = lambda: True
    elif missing == "exploration":
        runtime.player.stats.exploration = 99
    elif missing == "forest_request":
        runtime.forest.advanceTo(2)
    elif missing == "costume":
        runtime.clara.wardrobe.owned_items.remove("thiefdress")
    else:
        runtime.forest.abort()
    assert not event.canTrigger(runtime.sabbath.day)


@pytest.mark.parametrize("hour,minute,expected", [(18, 59, False), (19, 0, True), (22, 59, True), (23, 0, False)])
def test_sabbath_clock_boundaries_preserve_market_closure(runtime, hour, minute, expected):
    runtime.calendar.hour, runtime.calendar.minute = hour, minute
    assert runtime.sabbath.getevent(0).canTrigger(runtime.sabbath.day) is expected


def test_sabbath_calendar_finds_only_full_moon_saturday_each_period(runtime):
    event = runtime.sabbath.getevent(0)
    calendar = runtime.namespace["Calendar"](hour=19)
    runtime.namespace["calendar_v2"] = calendar
    days = []
    for _ in range(56):
        if event.canTrigger(0):
            days.append((calendar.period, calendar.day, calendar.week))
        calendar.advance_minutes(1440)
    assert days == [(1, 20, 6), (2, 20, 6)]


def test_sabbath_delay_and_daily_consumption_allow_later_full_moon(runtime):
    event = runtime.sabbath.getevent(0)
    runtime.sabbath.setDay()
    assert not event.canTrigger(runtime.sabbath.day)
    runtime.sabbath.day -= 1
    assert event.canTrigger(runtime.sabbath.day)
    runtime.namespace["story_event_mark_fired_today"](event)
    assert not event.canTrigger(runtime.sabbath.day)
    assert not runtime.sabbath.completed
    runtime.calendar.advance_minutes(28 * 1440)
    assert (runtime.calendar.day, runtime.calendar.week) == (20, 6)
    assert event.canTrigger(runtime.sabbath.day)


def test_sabbath_conditions_do_not_latch_after_thread_activation(runtime):
    assert runtime.sabbath.getAvailableEvents()
    runtime.clara.wardrobe.owned_items.remove("thiefdress")
    assert not runtime.sabbath.getAvailableEvents()
    runtime.clara.wardrobe.add_owned("thiefdress")
    assert runtime.sabbath.getAvailableEvents()
