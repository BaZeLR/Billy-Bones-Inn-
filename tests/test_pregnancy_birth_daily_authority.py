import ast
import copy
from pathlib import Path
import textwrap
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
NPCS = ("sandra", "melissa", "amanda", "becky", "inga", "georgett", "liza")


def daily_runtime(pregnancy=285):
    source = (ROOT / "game/Utilities/General/Common/CheckDailyEvent.rpy").read_text(encoding="utf-8-sig")
    init = source.split("init -25 python:\n", 1)[1].split("\ndefault ", 1)[0]
    tree = ast.parse(textwrap.dedent(init))
    tree.body = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    girls = {name: SimpleNamespace(days=pregnancy) for name in NPCS}
    for info in girls.values():
        info.pregnancy_days = lambda info=info: info.days
    births = []
    calls = []

    def create_kid(name):
        births.append(name)
        girls[name].days = 0

    def call_label(name, *args):
        calls.append((name, args))
        if name == "GiveBirth":
            create_kid(args[0])

    namespace = {
        "procedural_randint": lambda low, high, **kwargs: low,
        "people": SimpleNamespace(get_info=girls.get),
        "rooms": SimpleNamespace(current_code="BeckyHome"),
        "calendar_v2": SimpleNamespace(time_slot=lambda: 3),
        "renpy": SimpleNamespace(has_label=lambda name: name in ("GiveBirth", "GirlDressBuy")),
        "CreateKid": create_kid,
        "call_label": call_label,
    }
    exec(compile(tree, "CheckDailyEvent.rpy", "exec"), namespace)
    queue = namespace["DailyEventRuntime"]()
    namespace["daily_events"] = queue

    # Execute the existing procedure, replacing only Ren'Py syntax and calls.
    label = source.split("label check_daily_event", 1)[1]
    signature, body = label.split(":\n", 1)
    lines = ["def check_daily_event" + signature + ":"]
    python_block = False
    for line in body.splitlines():
        stripped = line.lstrip()
        if not stripped:
            continue
        indent = len(line) - len(stripped)
        if stripped.startswith("$ renpy.dynamic("):
            continue
        if stripped == "python:":
            python_block = True
            continue
        if python_block and indent <= 4:
            python_block = False
        if python_block:
            indent -= 4
        if stripped.startswith("$ "):
            stripped = stripped[2:]
        if stripped.startswith("call expression "):
            expr = stripped.removeprefix("call expression ")
            if " pass " in expr:
                target, args = expr.split(" pass ", 1)
                stripped = "call_label(" + target + ", *" + args + ")"
            else:
                stripped = "call_label(" + expr + ")"
        lines.append(" " * indent + stripped)
    exec("\n".join(lines), namespace)
    return queue, namespace["check_daily_event"], girls, births, calls


@pytest.mark.parametrize("girl", NPCS)
@pytest.mark.parametrize("callback,mode", (("GiveBirth", "girl"), ("CreateKid", "girl_location")))
def test_scheduled_birth_consumes_once_and_uses_existing_callback(girl, callback, mode):
    queue, consume, girls, births, calls = daily_runtime()
    queue.add(girl, "alllocs", -1, ">", 1, 9999, "GiveBirth", callback, mode)

    assert consume(girl, "GiveBirth") == 1
    assert queue.rows == []
    assert girls[girl].days == 0
    assert births == [girl]
    assert calls == ([("GiveBirth", (girl,))] if callback == "GiveBirth" else [])
    assert consume(girl, "GiveBirth") == 0
    assert births == [girl]


@pytest.mark.parametrize("girl", NPCS)
@pytest.mark.parametrize("callback,mode", (("GiveBirth", "girl"), ("CreateKid", "girl_location")))
def test_stale_birth_row_is_removed_without_creating_another_child(girl, callback, mode):
    queue, consume, girls, births, calls = daily_runtime(pregnancy=0)
    queue.add(girl, "alllocs", -1, ">", 1, 9999, "GiveBirth", callback, mode)

    assert consume(girl, "GiveBirth") == 0
    assert queue.rows == []
    assert births == []
    assert calls == []


def test_unrelated_daily_label_keeps_its_girl_location_contract():
    queue, consume, girls, births, calls = daily_runtime()
    queue.add("becky", "dressshop", 0, "=", 1, 1, "BuyDress", "GirlDressBuy", "girl_location")

    assert consume("becky", "BuyDress", "DressShop", 0) == 1
    assert calls == [("GirlDressBuy", ("becky", "dressshop"))]
    assert births == []


def test_all_existing_birth_entries_consume_the_scheduled_event():
    source = (ROOT / "game/Town/Temple/GiveBirthEvents.rpy").read_text(encoding="utf-8-sig")
    for girl in NPCS:
        if girl == "amanda":
            amanda = (ROOT / "game/NPC/Girls/Amanda/AmandaPregnancyEvents.rpy").read_text(encoding="utf-8-sig")
            block = amanda.split("label story_amanda_give_birth_0:", 1)[1].split("\nlabel ", 1)[0]
            assert "label story_give_birth_amanda:" not in source
        else:
            block = source.split("label story_give_birth_" + girl + ":", 1)[1].split("\nlabel ", 1)[0]
        assert 'call check_daily_event("' + girl + '", "GiveBirth")' in block
        assert "return _return" in block
        assert "call GiveBirth(" not in block


def test_birth_entry_tuples_project_only_scheduled_due_rows_and_current_pregnancy():
    source = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    literal = source.split("define birthThreadList = ", 1)[1].split("\ndefine threadListsByGirl", 1)[0]
    rows = eval(literal, {"UThreadData": lambda *args, **kwargs: args[4]})[0]
    assert {row[0].removeprefix("story_give_birth_") for row in rows} == set(NPCS) - {"amanda"}
    for row in rows:
        girl = row[0].removeprefix("story_give_birth_")
        conditions = row[6]
        assert len(conditions) == 2
        for due, pregnant, expected in ((False, 285, False), (True, 0, False), (True, 241, True)):
            namespace = {
                girl.capitalize(): SimpleNamespace(pregnancy_days=lambda: pregnant),
                "daily_events": SimpleNamespace(exists=lambda name, event: int(due)),
            }
            assert all(eval(condition.removeprefix("#"), namespace) for condition in conditions) is expected


@pytest.mark.parametrize("due,pregnant,expected", ((False, 285, False), (True, 0, False), (True, 241, True)))
def test_amanda_typed_birth_event_uses_the_same_daily_queue_authority(due, pregnant, expected):
    source = (ROOT / "game/NPC/Girls/Amanda/InitAmanda.rpy").read_text(encoding="utf-8-sig")
    method = "def birth_ready(self):" + source.split("def birth_ready(self):", 1)[1].split("        def apply_body_state", 1)[0]
    namespace = {"daily_events": SimpleNamespace(exists=lambda girl, event: int(due))}
    exec(method, namespace)
    info = SimpleNamespace(code_name="amanda", pregnancy_days=lambda: pregnant)
    info.birth_ready = lambda: namespace["birth_ready"](info)
    namespace["Amanda"] = info
    event_source = (ROOT / "game/NPC/Girls/Amanda/AmandaEventModel.rpy").read_text(encoding="utf-8-sig")
    event_class = event_source.split("class AmandaBirthEvent(AmandaEvent):", 1)[1].split("    class ", 1)[0]
    check = "def checkAmandaConditions(self):" + event_class.split("def checkAmandaConditions(self):", 1)[1]
    exec(check, namespace)
    assert namespace["checkAmandaConditions"](None) is expected


@pytest.mark.parametrize("mode", ("", "FromDinner", "FromDances", "SvalnyiGreh"))
@pytest.mark.parametrize("available", (False, True))
def test_becky_home_entry_checks_events_once_for_every_admitted_arrival(mode, available):
    source = (ROOT / "game/Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")
    entry = source.split('label BeckyHome(arrive_mode=""):', 1)[1].split("\nlabel ", 1)[0]
    common = entry.split('$ main_ui_begin_native_scene_state("Дом Бекки")', 1)[1].split(
        "$ _start_becky_sex = False", 1
    )[0]
    assert entry.count('story_event_available("BeckyHome", "enter")') == 1
    assert entry.count('call checkTriggers("BeckyHome", "enter", 0)') == 1
    assert '"_becky_home_enter_event"' in entry.splitlines()[1]
    assert "elif arrive_mode == 'FromDinner':\n        if not _becky_home_enter_event:" in entry
    calls = []

    def event_available(room, phase):
        calls.append(("query", room, phase))
        return available

    lines = []
    for line in textwrap.dedent(common).splitlines():
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith('"'):
            stripped = 'calls.append(("intro",))'
        elif stripped.startswith("$ "):
            stripped = stripped[2:]
        elif stripped.startswith("call "):
            stripped = stripped.removeprefix("call ")
        lines.append(indent + stripped)
    namespace = {
        "arrive_mode": mode,
        "calls": calls,
        "story_event_available": event_available,
        "checkTriggers": lambda *args: calls.append(("trigger",) + args),
    }
    exec("\n".join(lines), namespace)
    expected = [("intro",)] if mode == "FromDinner" else []
    expected.append(("query", "BeckyHome", "enter"))
    if available:
        expected.append(("trigger", "BeckyHome", "enter", 0))
    assert calls == expected
    assert namespace["_becky_home_enter_event"] is available


def test_completed_birth_next_day_cannot_restore_its_old_room():
    finish = (ROOT / "game/Town/Temple/GiveBirthFinish.rpy").read_text(encoding="utf-8-sig")
    next_day = (ROOT / "game/Utilities/Time/NextDay.rpy").read_text(encoding="utf-8-sig")
    assert 'call NextDay("TavernMain", 1)' in finish
    exit_path = next_day.split('call checkTriggers("TavernMyRoom", "morning", 0)', 1)[1]
    assert exit_path.index("renpy.set_return_stack([])") < exit_path.index("jump TavernMyRoom")


@pytest.mark.parametrize("girl", NPCS)
@pytest.mark.parametrize("pregnant", (0, 1, 240, 241, 285))
def test_save_upgrade_discards_only_impossible_registered_birth_rows(girl, pregnant):
    source = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    function = "    def updateSave_V97():" + source.split("    def updateSave_V97():", 1)[1].split("    # Saved objects", 1)[0]
    queue, consume, girls, births, calls = daily_runtime(pregnancy=pregnant)
    queue.add(girl, "alllocs", -1, ">", 1, 9999, "GiveBirth", "GiveBirth", "girl")
    queue.add("unknown", "alllocs", -1, ">", 1, 9999, "GiveBirth", "GiveBirth", "girl")
    queue.add(girl, "DressShop", 0, "=", 1, 1, "BuyDress", "GirlDressBuy", "girl_location")
    queue.add(girl, "TavernKitchen", 2, "<", 1, 8, "MorningSickness", "MorningSickness", "girl")
    before_rows = copy.deepcopy(queue.rows)
    girls[girl].sex_state = {"kids": 3, "pregnancy_suspects": [{"DudeName": "saved"}]}
    girls[girl].detailed_sex_history = [{"RowId": 1, "Zalet": 1}]
    before_info = copy.deepcopy(girls[girl].__dict__)
    namespace = {"daily_events": queue, "people": SimpleNamespace(get_info=girls.get)}
    exec(textwrap.dedent(function), namespace)
    namespace["updateSave_V97"]()
    assert queue.exists(girl, "GiveBirth") == int(pregnant > 240)
    assert queue.exists("unknown", "GiveBirth") == 1
    assert before_rows[1] in queue.rows
    assert before_rows[2] in queue.rows
    assert queue.rows[-1] == dict(before_rows[-1], Location="alllocs")
    assert girls[girl].__dict__ == before_info
    assert births == calls == []
