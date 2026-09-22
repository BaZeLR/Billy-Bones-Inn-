"""Exercise the authored breakfast thread with the actual event/condition owners."""

import ast
import builtins
from copy import deepcopy
from functools import lru_cache
from types import SimpleNamespace

import pytest

from tests.test_tavern_renovations_runtime import _exec_definitions, _python_nodes as _source_nodes


THREAD = "sandraAmandaReconciliation"
CONTENT = "Utilities/General/Classes/StoryEventRuntime.rpy"
_python_nodes = lru_cache(maxsize=None)(_source_nodes)


@pytest.fixture
def runtime():
    ns = {
        "_story_range_type": range,
        "renpy": SimpleNamespace(log=lambda *args: None),
        "procedural_shuffle": lambda sequence, **kwargs: None,
    }
    for path in (
        "Utilities/General/Events/conditions.rpy",
        "Utilities/General/Events/events.rpy",
        "Utilities/General/Events/threads.rpy",
    ):
        names = {node.name for node in _python_nodes(path)
                 if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        _exec_definitions(path, names, ns)
    calendar = SimpleNamespace(daysInGame=40, day=13, period=2, cycle=1080,
                               week=2, hour=8, minute=0,
                               time_slot=lambda: 1, clock_minutes=lambda: 480)
    breakfast = SimpleNamespace(event_active=True, present_ids=["sandra", "amanda", "melissa"])
    issues = {}
    ns.update(
        calendar_v2=calendar,
        current_game_day=lambda: calendar.daysInGame,
        player=SimpleNamespace(tavern_management=SimpleNamespace(breakfast=breakfast)),
        people=SimpleNamespace(ids_at=lambda room: []),
        household_breakfast_attendee_ids=lambda: ["sandra", "melissa", "amanda"],
        household_morning_issue_type=lambda key: issues.get(key, ""),
        rooms=SimpleNamespace(current_code="TavernKitchen",
                              get=lambda key: SimpleNamespace(is_open=lambda: True)),
        event_runtime=SimpleNamespace(fired_day=-1, fired_keys_today=[]),
        threads={"melissaBatProblem": SimpleNamespace(num=9, day=20, completed=False)},
    )
    _exec_definitions("Inn/TavernKitchenBreakfast.rpy", {"tavern_breakfast_present_ids"}, ns)
    # Keep the real whitelist/evaluator. Only unrelated dependencies are inert.
    for name in ns["_story_condition_scope"].__code__.co_names:
        if not hasattr(builtins, name):
            ns.setdefault(name, None)
    declarations = [node for root in _python_nodes(CONTENT) for node in ast.walk(root)
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "LThreadData" and len(node.args) > 2
                    and isinstance(node.args[1], ast.Constant) and node.args[1].value == "sandra"
                    and isinstance(node.args[2], ast.Constant) and node.args[2].value == "AmandaReconciliation"]
    assert len(declarations) == 1, "One authored reconciliation thread must own both stages"
    data = eval(compile(ast.Expression(declarations[0]), CONTENT, "eval"), ns)
    ns["threadData"] = {data.name: data}
    ns["initThreads"]()
    ns["initEvents"]()
    return SimpleNamespace(ns=ns, calendar=calendar, breakfast=breakfast, issues=issues,
                           thread=ns["threads"][THREAD], bat=ns["threads"]["melissaBatProblem"])


def test_two_stages_are_bound_to_actual_breakfast_not_room_entry(runtime):
    data = runtime.thread.data
    assert data.condStr is None
    assert data.length == 2
    for index, label in enumerate(("story_sandra_amanda_argument_0", "story_sandra_amanda_reconciliation_1")):
        event = runtime.thread.getevent(index)
        assert (event.target, event.location, event.action) == (label, "TavernKitchen", "breakfast")
        assert event.threaded and not event.repeatable
        assert event.day is None and event.hour is None
        assert event.prob == 1
    assert runtime.thread.getevent(1).evtDay == 2
    assert runtime.ns["_story_condition_scope"]()["tavern_breakfast_present_ids"] is runtime.ns["tavern_breakfast_present_ids"]


@pytest.mark.parametrize("bat_stage,expected", [(0, False), (8, False), (9, True), (12, True)])
def test_initial_scene_waits_until_original_booklet_argument_finished(runtime, bat_stage, expected):
    runtime.bat.num = bat_stage
    runtime.bat.completed = bat_stage == 12
    assert bool(runtime.thread.getAvailableEvents()) is expected


@pytest.mark.parametrize("stage", [0, 1])
@pytest.mark.parametrize("missing", ["breakfast", "amanda", "sandra", "sick_amanda", "sleepy_sandra"])
def test_each_stage_rechecks_actual_attendance_even_after_thread_activated(runtime, stage, missing):
    runtime.thread.advanceTo(stage)
    runtime.thread.day = 38
    assert runtime.thread.getAvailableEvents()
    assert runtime.thread.metconds
    if missing == "breakfast":
        runtime.breakfast.event_active = False
    elif missing in ("amanda", "sandra"):
        runtime.breakfast.present_ids.remove(missing)
    else:
        issue, girl = missing.split("_")
        runtime.issues[girl] = issue
    assert not runtime.thread.getAvailableEvents()


@pytest.mark.parametrize("hour", [0, 7, 12, 23])
def test_active_breakfast_owns_time_without_a_second_hour_window(runtime, hour):
    runtime.calendar.hour = hour
    assert runtime.thread.getAvailableEvents()


@pytest.mark.parametrize("start_day", [0, 40])
@pytest.mark.parametrize("elapsed,expected", [(0, False), (1, False), (2, True), (3, True), (40, True)])
def test_reconciliation_waits_at_least_two_absolute_days_from_its_own_argument(runtime, start_day, elapsed, expected):
    runtime.calendar.daysInGame = start_day
    runtime.thread.setDay()  # The actual preEvent operation before stage zero.
    runtime.thread.advance()
    runtime.calendar.daysInGame += elapsed
    runtime.bat.day = runtime.calendar.daysInGame + 100
    assert bool(runtime.thread.getAvailableEvents()) is expected


def test_first_event_fires_once_daily_and_final_advance_finishes_thread(runtime):
    first = runtime.thread.getAvailableEvents()[0]
    runtime.ns["story_event_mark_fired_today"](first)
    assert not runtime.thread.getAvailableEvents()
    runtime.thread.setDay()
    runtime.thread.advance()
    assert runtime.thread.num == 1 and not runtime.thread.completed
    runtime.calendar.daysInGame += 2
    assert runtime.thread.getAvailableEvents()[0].target == "story_sandra_amanda_reconciliation_1"
    runtime.thread.setDay()
    runtime.thread.advance()
    assert runtime.thread.num == 2 and runtime.thread.completed
    for elapsed in (0, 1, 28):
        runtime.calendar.daysInGame += elapsed
        assert not runtime.thread.getAvailableEvents()


@pytest.mark.parametrize("bat_stage", [9, 12])
def test_init_threads_adds_missing_thread_without_replaying_or_rewriting_old_progress(runtime, bat_stage):
    ns = runtime.ns
    ns["threads"].pop(THREAD)
    runtime.bat.num = bat_stage
    runtime.bat.completed = bat_stage == 12
    before = deepcopy(vars(runtime.bat))
    ns["initThreads"]()
    created = ns["threads"][THREAD]
    assert created.num == 0 and not created.completed
    assert ns["threads"]["melissaBatProblem"] is runtime.bat
    assert vars(runtime.bat) == before
    assert created.getAvailableEvents()
    created.setDay()
    created.advance()
    saved = (created.num, created.day, list(created.done), created.completed)
    ns["initThreads"]()
    assert ns["threads"][THREAD] is created
    assert (created.num, created.day, created.done, created.completed) == saved
    assert vars(runtime.bat) == before
