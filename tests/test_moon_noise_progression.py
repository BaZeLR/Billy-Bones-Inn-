"""Exercise the real lunar event registry and its household listener predicate."""
import ast
from types import SimpleNamespace

import pytest

from tests.test_moon_stove_runtime import runtime, source, targets
from tests.test_tavern_renovations_runtime import _exec_definitions
from tools.runtime_logic_tests import extract_balanced_assignment


@pytest.fixture
def noise(runtime):
    ns = runtime
    extra = SimpleNamespace(virgin=True)
    extra.sex_stat = lambda *args: extra.virgin
    girls = {"amanda": ns["Amanda"], "melissa": ns["Melissa"], "liza": extra}
    ns["residents"] = {"amanda", "melissa", "sandra"}
    ns["breakfast_ids"] = {"amanda", "melissa", "sandra"}
    ns["locations"] = {key: "TavernKitchen" for key in girls}
    ns["household"] = SimpleNamespace(resident_ids=lambda: list(ns["residents"]))
    ns["people"] = SimpleNamespace(girl_items=lambda: list(girls.items()),
                                  location=lambda key: ns["locations"][key])
    ns["tavern_breakfast_present_ids"] = lambda: list(ns["breakfast_ids"])
    ns["tavern"] = SimpleNamespace(renovation_complete=lambda code: True)
    ns["threads"]["melissaBatProblem"] = SimpleNamespace(completed=True, day=18)
    _exec_definitions("NPC/Girls/Melissa/MelissaMoonNoise.rpy", {"moon_noise_listener_ids"}, ns)
    tree = ast.parse(extract_balanced_assignment(
        source("game/Utilities/General/Classes/StoryEventRuntime.rpy"), "melissaThreadList"), mode="eval")
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "LThreadData" and ast.literal_eval(node.args[2]) in {"MoonNoise", "MoonNoiseRepeat"}):
            continue
        data = eval(compile(ast.Expression(node), "noise_registry", "eval"), ns)
        data.initConditions()
        for stage in data.triggers:
            for event in stage:
                event.initConditions()
        ns["threads"][data.name] = ns["createThread"](data)
    ns["calendar_v2"].hour = 22
    ns["calendar_v2"].daysInGame = 44
    return ns


@pytest.mark.parametrize("amanda,melissa,expected", [
    (True, True, ["amanda", "melissa"]), (False, True, ["melissa"]),
    (True, False, ["amanda"]), (False, False, []),
])
def test_each_listener_uses_live_virginity(noise, amanda, melissa, expected):
    noise["Amanda"].virgin, noise["Melissa"].virgin = amanda, melissa
    assert noise["moon_noise_listener_ids"]() == expected
    assert noise["moon_noise_listener_ids"](True) == expected


def test_hired_virgin_only_if_resident_and_present(noise):
    assert "liza" not in noise["moon_noise_listener_ids"]()
    noise["residents"].add("liza")
    assert "liza" in noise["moon_noise_listener_ids"]()
    assert "liza" not in noise["moon_noise_listener_ids"](True)
    noise["breakfast_ids"].add("liza")
    assert "liza" in noise["moon_noise_listener_ids"](True)
    noise["locations"]["liza"] = "MarketPlace"
    assert "liza" not in noise["moon_noise_listener_ids"]()


@pytest.mark.parametrize("day,eligible", [(13, False), (14, True), (16, True), (17, True), (20, True), (21, True), (23, True), (24, False)])
def test_night_window(noise, day, eligible):
    noise["calendar_v2"].day = day
    noise["calendar_v2"].daysInGame = 28 + day - 1
    assert bool(targets(noise["threads"]["melissaMoonNoise"])) is eligible
    noise["threads"]["melissaMoonNoise"].advanceTo(4, complete_at_end=True)
    assert bool(targets(noise["threads"]["melissaMoonNoiseRepeat"])) is eligible


def test_first_investigation_preserves_order_and_day_delays(noise):
    thread = noise["threads"]["melissaMoonNoise"]
    clock = noise["calendar_v2"]
    assert targets(thread) == ["story_melissa_moon_noise_0"]
    thread.setDay()
    thread.advance()
    clock.hour = 8
    assert targets(thread) == []
    clock.daysInGame += 1
    assert targets(thread) == ["story_melissa_moon_breakfast_1"]
    thread.advance()
    assert targets(thread) == ["story_melissa_moon_roof_check_2"]
    thread.setDay()
    thread.advance()
    assert targets(thread) == []
    clock.daysInGame += 1
    assert targets(thread) == ["story_melissa_moon_sandra_story_3"]
    thread.advance()
    assert thread.completed


def test_corridor_reminder_finishes_without_breakfast_and_returns_next_full_moon(noise):
    first = noise["threads"]["melissaMoonNoise"]
    repeat = noise["threads"]["melissaMoonNoiseRepeat"]
    clock = noise["calendar_v2"]
    assert targets(repeat) == []
    first.advanceTo(4, complete_at_end=True)
    assert targets(repeat) == ["story_melissa_moon_noise_repeat"]
    assert not repeat.data.triggers[0][0].threaded and repeat.data.length == 1
    noise["story_event_mark_fired_today"](repeat.data.triggers[0][0])
    repeat.setDay()
    assert targets(repeat) == []
    clock.daysInGame += 1
    clock.day += 1
    clock.hour = 8
    assert targets(repeat) == []
    assert repeat.num == 0 and not repeat.completed and first.completed
    clock.hour = 22
    assert targets(repeat) == []
    clock.daysInGame += 27
    clock.day = 17
    assert targets(repeat) == ["story_melissa_moon_noise_repeat"]


def test_reminder_waits_for_both_women_without_making_nonvirgins_hear_noise(noise):
    first, repeat = (noise["threads"][key] for key in ("melissaMoonNoise", "melissaMoonNoiseRepeat"))
    first.advanceTo(4, complete_at_end=True)
    noise["available_npcs"].remove("amanda")
    assert targets(repeat) == []
    noise["available_npcs"].add("amanda")
    noise["Amanda"].virgin = False
    assert targets(repeat) == ["story_melissa_moon_noise_repeat"]
    noise["Amanda"].virgin = noise["Melissa"].virgin = False
    assert targets(repeat) == []


def test_older_unthreaded_repeat_retains_progress_when_registry_rebinds(noise):
    repeat = noise["threads"]["melissaMoonNoiseRepeat"]
    repeat.done = [False]
    repeat.adjustLen()
    assert repeat.done == [False] and repeat.num == 0 and not repeat.completed


def test_post_repair_noise_waits_for_the_next_month(noise):
    clock = noise["calendar_v2"]
    clock.daysInGame = 19
    clock.day = 20
    assert targets(noise["threads"]["melissaMoonNoise"]) == []
    clock.daysInGame, clock.day = 44, 17
    assert targets(noise["threads"]["melissaMoonNoise"]) == ["story_melissa_moon_noise_0"]


@pytest.mark.parametrize("day,eligible", [(13, False), (14, True), (23, True), (24, False)])
def test_original_bat_opening_uses_noise_window_without_gating_later_quest_stages(day, eligible):
    tree = ast.parse(extract_balanced_assignment(
        source("game/Utilities/General/Classes/StoryEventRuntime.rpy"), "melissaThreadList"), mode="eval")
    data = next(node for node in ast.walk(tree) if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name) and node.func.id == "LThreadData"
        and ast.literal_eval(node.args[2]) == "BatProblem")
    first = ast.literal_eval(data.args[4].elts[0])
    gate = "#14 <= int(calendar_v2.day or 0) <= 23"
    assert gate in first[6]
    assert eval(gate[1:], {"calendar_v2": SimpleNamespace(day=day)}) is eligible
    assert "calendar_v2.day" not in ast.unparse(data.args[4].elts[1])


def test_amanda_keeps_her_enjoyment_private_and_corridor_scene_ends_reminder():
    text = source("game/NPC/Girls/Melissa/MelissaMoonNoise.rpy")
    breakfast = text.split("label story_melissa_moon_breakfast_1:", 1)[1].split("\nlabel ", 1)[0]
    assert "Аманда молчит" in breakfast and "Аманда подтверждает" not in breakfast
    story = text.split("label story_melissa_moon_sandra_story_3:", 1)[1].split("\nlabel ", 1)[0]
    assert "просыпаюсь горячая и довольная" not in story
    corridor = text.split("label story_melissa_moon_noise_repeat:", 1)[1].split("\nlabel ", 1)[0]
    assert "Обе встревожены" in corridor and "волосы растрёпаны" in corridor and "сорочки надеты кое-как" in corridor
    assert "Amanda.wear_night_clothes(0)" in corridor and "Melissa.wear_night_clothes(0)" in corridor
    assert ".advance()" not in corridor and ".reset()" not in corridor
    assert "label story_melissa_moon_breakfast_repeat:" not in text


def test_night_date_is_stamped_before_crossing_midnight():
    text = source("game/NPC/Girls/Melissa/MelissaMoonNoise.rpy")
    for name in ("story_melissa_moon_noise_0", "story_melissa_moon_noise_repeat"):
        scene = text.split("label " + name + ":", 1)[1].split("\nlabel ", 1)[0]
        assert scene.index(".setDay()") < scene.index("calendar_v2.advance_minutes(")
