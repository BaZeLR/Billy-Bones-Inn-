"""Live event gates, thread progression and save migration for the stove arc."""
import ast
from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest
from tools.runtime_logic_tests import extract_balanced_assignment

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


@pytest.fixture
def runtime():
    clock = SimpleNamespace(day=17, hour=21, minute=0, week=1, daysInGame=17)
    clock.clock_minutes = lambda: clock.hour * 60 + clock.minute
    clock.moon_phase_name_en = lambda: "Full Moon" if 17 <= clock.day <= 20 else "Waning Moon"
    a = SimpleNamespace(virgin=True, anger_with_player=0, asked_today=0, talked_today=0)
    m = SimpleNamespace(virgin=True, anger_with_player=0, asked_today=0, talked_today=0)
    a.sex_stat = lambda *args: a.virgin
    m.sex_stat = lambda *args: m.virgin
    m.intimacy_story_ready = lambda: True
    ns = {
        "calendar_v2": clock, "Amanda": a, "Melissa": m,
        "rooms": SimpleNamespace(get=lambda name: SimpleNamespace(is_hidden=False)),
        "event_runtime": SimpleNamespace(fired_day=-1, fired_keys_today=[]),
        "available_npcs": {"amanda", "melissa"},
        "relationship_anger": lambda name: 0,
        "player": SimpleNamespace(equipment=SimpleNamespace(hand=""), item_count=lambda name: 0),
        "_story_num_day": lambda: clock.daysInGame,
        "_story_to_int": lambda value, default=0: default if value is None else int(value),
        "_story_level_enabled": lambda *args: True,
        "_story_delay_ready": lambda delay, day: delay is None or clock.daysInGame >= day + delay,
        "_story_location_is_open": lambda name: True,
        "checkEventTime": lambda current, spec: spec is None or spec[0] <= current <= spec[-1],
        "makeConditions": lambda rows: rows or [],
    }
    ns["moon_stove_npc_available"] = lambda name: name in ns["available_npcs"]
    ns["_story_conditions_met"] = lambda rows: all(eval(row[1:], ns) for row in rows)
    event_body = source("game/Utilities/General/Events/events.rpy").split("init -25 python:\n", 1)[1].split("\ninit ", 1)[0]
    event_body = "\n".join(line[4:] if line.startswith("    ") else line for line in event_body.splitlines())
    nodes = ast.parse(event_body).body
    names = {"story_event_day_key", "story_event_reset_fired_today_if_needed", "story_event_fired_today", "story_event_mark_fired_today"}
    selected = [node for node in nodes if (isinstance(node, ast.ClassDef) and node.name == "Event") or (isinstance(node, ast.FunctionDef) and node.name in names)]
    exec(compile(ast.Module(body=selected, type_ignores=[]), "events.rpy", "exec"), ns)
    thread_body = textwrap.dedent(source("game/Utilities/General/Events/threads.rpy").split("init -25 python:\n", 1)[1])
    nodes = [node for node in ast.parse(thread_body).body if not isinstance(node, (ast.Import, ast.ImportFrom))]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "threads.rpy", "exec"), ns)
    content = source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    wanted = {"MoonStoveRitual", "MoonProtection", "StoveDebrief", "FullMoonBats"}
    ns["threads"] = {"melissaMoonNoise": SimpleNamespace(completed=True, num=0)}
    for assignment in ("melissaThreadList", "churchThreadList"):
        tree = ast.parse(extract_balanced_assignment(content, assignment), mode="eval")
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "LThreadData" and ast.literal_eval(node.args[2]) in wanted):
                continue
            data = eval(compile(ast.Expression(node), "registry", "eval"), ns)
            thread = ns["createThread"](data)
            data.initConditions()
            for stage in data.triggers:
                for event in stage:
                    event.initConditions()
            ns["threads"][data.name] = thread
    return ns


def targets(thread):
    return [event.target for event in thread.getAvailableEvents()]


def test_distinct_nights_and_next_cycle_catch_up(runtime):
    thread = runtime["threads"]["melissaMoonStoveRitual"]
    c = runtime["calendar_v2"]
    assert targets(thread) == ["story_melissa_moon_window_clue_0"]
    thread.advanceTo(2)
    thread.day = 17
    assert targets(thread) == []
    c.day = c.daysInGame = 18
    assert targets(thread) == ["story_melissa_moon_second_window_2"]
    thread.advanceTo(4)
    thread.day = 18
    c.hour = 23
    assert targets(thread) == []
    c.day = c.daysInGame = 19
    assert targets(thread) == ["story_melissa_moon_stove_wait_1"]
    c.minute = 46
    assert targets(thread) == []
    c.minute = 0
    c.day, c.daysInGame = 20, 48
    assert targets(thread) == ["story_melissa_moon_stove_wait_1"]


@pytest.mark.parametrize("owned,equipped", [(False, False), (True, False), (True, True)])
def test_glove_does_not_block_wait(runtime, owned, equipped):
    thread = runtime["threads"]["melissaMoonStoveRitual"]
    thread.advanceTo(4)
    thread.day = 18
    c = runtime["calendar_v2"]
    c.hour, c.day, c.daysInGame = 23, 19, 19
    runtime["player"].item_count = lambda name: int(owned)
    runtime["player"].equipment.hand = "fur_glove_001" if equipped else ""
    assert targets(thread) == ["story_melissa_moon_stove_wait_1"]


def test_absent_participant_postpones_and_no_listeners_closes(runtime):
    thread = runtime["threads"]["melissaMoonStoveRitual"]
    thread.advanceTo(4)
    thread.day = 18
    c = runtime["calendar_v2"]
    c.hour, c.day, c.daysInGame = 23, 19, 19
    runtime["available_npcs"].remove("melissa")
    assert targets(thread) == []
    runtime["available_npcs"].add("melissa")
    runtime["Amanda"].virgin = runtime["Melissa"].virgin = False
    assert targets(thread) == ["story_melissa_moon_stove_not_needed"]


def test_visits_have_separate_windows_and_cursors(runtime):
    ritual = runtime["threads"]["melissaMoonStoveRitual"]
    ritual.advanceTo(5, complete_at_end=True)
    ritual.day = 19
    ritual.ritual_result = {"route": "no_glove", "participants": ["amanda", "melissa"], "ritual_participants": ["amanda", "melissa"]}
    c = runtime["calendar_v2"]
    c.day = c.daysInGame = 19
    a = runtime["threads"]["amandaMoonProtection"]
    m = runtime["threads"]["melissaMoonProtection"]
    c.hour = 22
    assert targets(a) == ["story_amanda_moon_protection_0"]
    assert targets(m) == []
    c.hour = 23
    assert targets(a) == []
    assert targets(m) == ["story_melissa_moon_protection_0"]
    a.advance()
    assert not m.completed
    ritual.ritual_result["ritual_participants"] = ["amanda"]
    assert targets(m) == []


def test_church_alternatives_share_daily_consumption(runtime):
    thread = runtime["threads"]["churchFullMoonBats"]
    first = thread.getAvailableEvents()[0]
    runtime["story_event_mark_fired_today"](first)
    assert targets(thread) == []
    c = runtime["calendar_v2"]
    c.hour = 0
    assert targets(thread) == []
    c.daysInGame += 1
    assert targets(thread) == ["story_church_full_moon_bats_0"]
    c.day = 21
    assert targets(thread) == []


@pytest.mark.parametrize("stage,completed,proof,route", [(0, False, True, None), (1, False, True, None), (2, False, True, "glove"), (3, True, True, "glove"), (2, False, False, "legacy_unknown")])
def test_migration_keeps_content_without_replay_or_invented_route(runtime, stage, completed, proof, route):
    ns = runtime
    ritual = ns["threads"]["melissaMoonStoveRitual"]
    ritual.num, ritual.completed = stage, completed
    del ritual.ritual_result
    live_data = ritual.data
    ritual.data = SimpleNamespace(triggers=[[SimpleNamespace(target="story_melissa_moon_room_protection_2" if proof else "unknown")]])
    ns["initThreads"] = lambda: setattr(ritual, "data", live_data)
    migration = source("game/TractirSaveSync.rpy").split("    def updateSave_V109():", 1)[1].split("    # Saved objects must be upgraded", 1)[0]
    exec(textwrap.dedent("    def updateSave_V109():" + migration), ns)
    ns["updateSave_V109"]()
    assert ritual.num == (5 if completed or stage >= 2 else stage)
    assert (ritual.ritual_result or {}).get("route") == route
    snapshot = (ritual.num, ritual.completed, ritual.ritual_result)
    ns["updateSave_V109"]()
    assert (ritual.num, ritual.completed, ritual.ritual_result) == snapshot
    assert ns["threads"]["amandaMoonProtection"].completed is completed
