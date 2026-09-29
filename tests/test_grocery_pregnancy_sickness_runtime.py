"""Grocery pregnancy sickness uses the existing room-entry Event objects."""

from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def registered_event(person):
    registry = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    start = registry.index(f'RThreadData(0, "{person}", "GroceryPregnancySickness"')
    end = registry.index("], highlight=False, threaded=True),", start) + len("], highlight=False, threaded=True)")
    registration = eval(registry[start:end], {"RThreadData": lambda *args, **kwargs: (args, kwargs)})
    args, options = registration
    assert options == {"highlight": False, "threaded": True}
    assert args[1:3] == (person, "GroceryPregnancySickness")
    return args[4][1][0]


@pytest.fixture
def runtime():
    code = source("game/Utilities/General/Events/events.rpy")
    event_class = code.split("    class Event(object):", 1)[1].split("    def story_event_location_keys", 1)[0]
    calendar = SimpleNamespace(week=2, hour=14)
    positions = {"becky": "GroceryStore", "inga": "MarketPlace"}
    pregnancy = {"becky": 30, "inga": 20}
    namespace = {
        "calendar_v2": calendar,
        "people": SimpleNamespace(location=positions.get),
        "Becky": SimpleNamespace(pregnancy_days=lambda: pregnancy["becky"]),
        "Inga": SimpleNamespace(pregnancy_days=lambda: pregnancy["inga"]),
        "story_event_fired_today": lambda event: False,
        "checkEventTime": lambda value, spec: spec is None or spec[0] <= value <= spec[1],
        "_story_delay_ready": lambda *args: True,
        "_story_conditions_met": lambda conditions: all(condition() for condition in conditions),
        "_story_location_is_open": lambda location: True,
        "procedural_random": lambda key: 0.1,
        "story_event_location_keys": lambda event: [event.location],
    }
    namespace["makeConditions"] = lambda conditions: [
        lambda expression=expression: eval(expression[1:], namespace)
        for expression in conditions
    ]
    exec("class Event(object):" + event_class, namespace)
    return SimpleNamespace(**namespace, positions=positions, pregnancy=pregnancy)


@pytest.mark.parametrize("person,hour", [("becky", 14), ("inga", 7)])
def test_each_pregnant_grocer_has_an_entry_event(runtime, person, hour):
    runtime.calendar_v2.hour = hour
    runtime.positions[person] = "GroceryStore"
    event = runtime.Event(registered_event(person), person + "GroceryPregnancySickness", True)
    event.initConditions()
    assert event.location == "GroceryStore"
    assert event.action == "enter"
    assert event.target == "GroceryPregnancySickness"
    assert event.daily_key == person + ":grocery_pregnancy_sickness"
    assert event.canTrigger()
    runtime.pregnancy[person] = 0
    assert not event.canTrigger()


def test_event_respects_shift_weekday_and_probability(runtime):
    event = runtime.Event(registered_event("becky"), "beckyGroceryPregnancySickness", True)
    event.initConditions()
    assert event.canTrigger()
    runtime.positions["becky"] = "MarketPlace"
    assert not event.canTrigger()
    runtime.positions["becky"] = "GroceryStore"
    runtime.calendar_v2.week = 7
    assert not event.canTrigger()
    runtime.calendar_v2.week = 2
    runtime.calendar_v2.hour = 18
    assert not event.canTrigger()
    assert event.prob == pytest.approx(1.0 / 7.0)


def test_same_scene_has_distinct_daily_keys_for_becky_and_inga(runtime):
    becky = runtime.Event(registered_event("becky"), "beckyGroceryPregnancySickness", True)
    inga = runtime.Event(registered_event("inga"), "ingaGroceryPregnancySickness", True)
    assert becky.target == inga.target
    assert becky.daily_key != inga.daily_key


def test_scene_is_label_owned_and_no_extra_daily_or_room_gate_exists():
    event = source("game/NPC/Girls/Common/GroceryPregnancySickness.rpy")
    generator = source("game/Utilities/General/NPC/DailySetstatdefault.rpy")
    gate = source("game/Utilities/General/Common/RoomEnterPipeline.rpy")
    grocery = source("game/Town/GroceryStore.rpy")
    assert 'label GroceryPregnancySickness(girl_name=""):' in event
    assert "event_runtime.active_thread.data.person" in event
    assert "grocery_store_grocer_picture(girl_name)" in event
    assert "wear_night_clothes" not in event
    assert "GroceryPregnancySickness" not in generator
    assert "GroceryPregnancySickness" not in gate
    assert 'call RoomEnterEventGate(rooms.current_code, False)' in grocery
