"""The grocery pregnancy encounter follows the grocer's shift, not tavern mornings."""

from pathlib import Path
import textwrap
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


@pytest.fixture
def runtime():
    namespace = {"procedural_randint": lambda *args, **kwargs: 1}
    daily = source("game/Utilities/General/Common/CheckDailyEvent.rpy")
    daily = daily.split("init -25 python:", 1)[1].split("default daily_events", 1)[0]
    exec(textwrap.dedent(daily).replace("import renpy.exports as renpy", ""), namespace)

    calendar_source = source("game/script.rpy")
    start = calendar_source.index("        def slot_from_hour(self, hour_value):")
    end = calendar_source.index("\n        def ", start + 10)
    methods = {}
    exec(textwrap.dedent(calendar_source[start:end]), {"_cal_int": lambda value, default: int(value)}, methods)
    calendar = SimpleNamespace(hour=14)
    calendar.time_slot = lambda: methods["slot_from_hour"](calendar, calendar.hour)

    people_info = {
        "becky": SimpleNamespace(pregnancy_days=lambda: 30),
        "inga": SimpleNamespace(pregnancy_days=lambda: 20),
    }
    positions = {"becky": "GroceryStore", "inga": "MarketPlace"}
    store = SimpleNamespace(is_open=lambda: True)
    namespace.update(
        people=SimpleNamespace(get_info=people_info.get, location=positions.get),
        rooms=SimpleNamespace(current_code="GroceryStore", get=lambda code: store),
        calendar_v2=calendar,
        daily_events=namespace["DailyEventRuntime"](),
    )
    event_source = source("game/NPC/Girls/Common/GroceryPregnancySickness.rpy")
    exec(textwrap.dedent(event_source.split("init python:", 1)[1].split("label GroceryPregnancySickness", 1)[0]), namespace)
    return SimpleNamespace(**namespace, positions=positions, people_info=people_info)


def test_becky_afternoon_arrival_consumes_only_her_grocery_event(runtime):
    runtime.daily_events.add("becky", "GroceryStore", 5, "<", 1, -1, "GroceryPregnancySickness", "GroceryPregnancySickness", "girl")
    assert runtime.grocery_pregnancy_sickness_girl() == "becky"
    row = runtime.daily_events.pop_match("becky", "GroceryPregnancySickness", "GroceryStore", runtime.calendar_v2.time_slot())
    assert row["EventCode"] == "GroceryPregnancySickness"
    assert row["CallMode"] == "girl"
    assert runtime.grocery_pregnancy_sickness_girl() == ""


def test_inga_early_shift_and_room_boundary(runtime):
    runtime.positions.update(becky="MarketPlace", inga="GroceryStore")
    runtime.calendar_v2.hour = 7
    runtime.daily_events.add("inga", "GroceryStore", 5, "<", 1, -1, "GroceryPregnancySickness", "GroceryPregnancySickness", "girl")
    assert runtime.grocery_pregnancy_sickness_girl() == "inga"
    assert runtime.grocery_pregnancy_sickness_girl("TavernKitchen") == ""
    runtime.people_info["inga"] = SimpleNamespace(pregnancy_days=lambda: 0)
    assert runtime.grocery_pregnancy_sickness_girl() == ""
    assert len(runtime.daily_events.rows) == 1


def test_event_is_gated_by_open_shop_and_ends_at_closing(runtime):
    runtime.daily_events.add("becky", "GroceryStore", 5, "<", 1, -1, "GroceryPregnancySickness", "GroceryPregnancySickness", "girl")
    runtime.calendar_v2.hour = 18
    assert runtime.grocery_pregnancy_sickness_girl() == ""
    runtime.calendar_v2.hour = 14
    runtime.rooms.get("GroceryStore").is_open = lambda: False
    assert runtime.grocery_pregnancy_sickness_girl() == ""


def test_entry_dispatch_and_event_keep_tavern_wardrobe_unchanged():
    generator = source("game/Utilities/General/NPC/DailySetstatdefault.rpy")
    gate = source("game/Utilities/General/Common/RoomEnterPipeline.rpy")
    grocery = source("game/Town/GroceryStore.rpy")
    event = source("game/NPC/Girls/Common/GroceryPregnancySickness.rpy")
    assert 'daily_events.add(girl_name, "GroceryStore", 5, "<", 1, -1, "GroceryPregnancySickness"' in generator
    assert 'call check_daily_event(_room_enter_sick_girl, "GroceryPregnancySickness"' in gate
    assert 'call RoomEnterEventGate(rooms.current_code, False)' in grocery
    assert 'label GroceryPregnancySickness(girl_name):' in event
    assert 'wear_night_clothes' not in event
    assert 'wear_day_clothes' not in event
