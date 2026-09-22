"""Exercise the real daily-row owner and tavern morning-sickness selector."""

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
    exec(textwrap.dedent(calendar_source[start:end]), {"_cal_int": lambda value, default: int(value)}, methods := {})
    calendar = SimpleNamespace(hour=8, minute=0)
    calendar.time_slot = lambda: methods["slot_from_hour"](calendar, calendar.hour)
    workers = {
        "nonworker": SimpleNamespace(is_tavern_worker=lambda: False),
        "new_worker": SimpleNamespace(is_tavern_worker=lambda: True),
        "second_worker": SimpleNamespace(is_tavern_worker=lambda: True),
    }
    tavern_rooms = {"TavernMain", "TavernKitchen", "TavernMyRoom", "TavernAtic", "TavernSandraRoom", "TavernGloryHole", "Backyard", "Shed", "ShedWashroom"}
    namespace.update(
        people=SimpleNamespace(girl_items=lambda: workers.items()),
        rooms=SimpleNamespace(current_code="TavernMain"),
        calendar_v2=calendar,
        player=SimpleNamespace(tavern_management=SimpleNamespace(breakfast=SimpleNamespace(today=False, event_active=False))),
        room_in_group=lambda room, group: room in tavern_rooms and group == "tavern",
        ROOM_GROUP_TAVERN="tavern",
        daily_events=namespace["DailyEventRuntime"](),
    )
    morning = source("game/NPC/Girls/Common/MorningSickness.rpy")
    exec(textwrap.dedent(morning.split("init python:", 1)[1].split("label MorningSickness", 1)[0]), namespace)
    for worker in workers:
        namespace["daily_events"].add(worker, "alllocs", 2, "<", 1, 8, "MorningSickness", "MorningSickness", "girl")
    return SimpleNamespace(**namespace)


@pytest.mark.parametrize("hour,minute,ready", [(0, 0, False), (5, 59, False), (6, 0, True), (7, 59, True), (8, 0, True), (10, 59, True), (11, 0, False), (23, 59, False)])
def test_clock_boundaries_use_actual_hours(runtime, hour, minute, ready):
    runtime.calendar_v2.hour, runtime.calendar_v2.minute = hour, minute
    assert runtime.tavern_morning_sickness_girl() == ("new_worker" if ready else "")


@pytest.mark.parametrize("room", ["TavernMain", "TavernKitchen", "TavernMyRoom", "TavernAtic", "TavernSandraRoom", "TavernGloryHole", "Backyard", "Shed", "ShedWashroom"])
def test_any_physical_tavern_room_uses_its_explicit_entry_code(runtime, room):
    runtime.rooms.current_code = "Church"
    assert runtime.tavern_morning_sickness_girl(room) == "new_worker"
    assert runtime.tavern_morning_sickness_girl() == ""


@pytest.mark.parametrize("room", ["Church", "StreetTavern", "Forest", "GroceryStore"])
def test_outside_tavern_does_not_consume_pending_row(runtime, room):
    assert runtime.tavern_morning_sickness_girl(room) == ""
    assert len(runtime.daily_events.rows) == 3


@pytest.mark.parametrize("field", ["today", "event_active"])
def test_breakfast_started_or_finished_blocks_sickness(runtime, field):
    setattr(runtime.player.tavern_management.breakfast, field, True)
    assert runtime.tavern_morning_sickness_girl() == ""
    assert len(runtime.daily_events.rows) == 3


def test_selector_consumes_no_rows_and_dispatch_consumes_each_worker_once(runtime):
    pending = runtime.daily_events
    assert runtime.tavern_morning_sickness_girl() == "new_worker"
    assert runtime.tavern_morning_sickness_girl() == "new_worker"
    assert len(pending.rows) == 3
    for expected in ("new_worker", "second_worker"):
        girl = runtime.tavern_morning_sickness_girl()
        assert girl == expected
        row = pending.pop_match(girl, "MorningSickness", "TavernMain", runtime.calendar_v2.time_slot())
        assert row["GirlName"] == expected
        assert row["CallMode"] == "girl"
    assert runtime.tavern_morning_sickness_girl() == ""
    assert [row["GirlName"] for row in pending.rows] == ["nonworker"]


def test_generic_daily_dispatch_cannot_bypass_the_entry_gate(runtime):
    assert runtime.daily_events.pop_match("new_worker", None, "TavernMain", 1) == {}
    assert len(runtime.daily_events.rows) == 3


def test_every_physical_tavern_entry_reaches_the_canonical_gate():
    for name in ("TavernMain", "TavernKitchen", "TavernMyRoom", "TavernAmandaRoom", "TavernMelissaRoom", "TavernSandraRoom", "TavernUpstairs", "TavernEmptyRoom", "TavernStorage", "TavernStable", "TavernGloryHole", "TavernAtic", "Backyard", "Shed", "ShedWashroom"):
        entry = source(f"game/Inn/{name}.rpy").split(f"label {name}:", 1)[1].split("\nlabel ", 1)[0]
        assert 'call RoomEnterEventGate(rooms.current_code, False)' in entry, name


def test_old_kitchen_rows_migrate_without_changing_other_daily_state(runtime):
    row = runtime.daily_events.rows[1]
    row.update(Location="TavernKitchen", KeepNextDay=3, ChanceToMeet=5)
    runtime.daily_events.add("new_worker", "TavernKitchen", 7, "=", 1, 99, "Unrelated", "Unrelated", "girl")
    before = [dict(item) for item in runtime.daily_events.rows]
    migration = source("game/TractirSaveSync.rpy").split("    def updateSave_V97():", 1)[1].split("    # Saved objects", 1)[0]
    namespace = {"daily_events": runtime.daily_events}
    exec("def migrate():\n" + textwrap.indent(textwrap.dedent(migration), "    "), namespace)
    namespace["migrate"]()
    namespace["migrate"]()
    before[1]["Location"] = "alllocs"
    assert runtime.daily_events.rows == before
    assert runtime.tavern_morning_sickness_girl() == "new_worker"
