import ast
from pathlib import Path
import re
import textwrap
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
PEOPLE = "game/Utilities/General/NPC/PeopleRuntime.rpy"
CLIENTS = "game/Utilities/General/Sex/WhoreNextDayClients.rpy"
ACTIONS = "game/Utilities/General/Common/Actions.rpy"


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def init_tree(path):
    body = source(path).split("python:\n", 1)[1]
    body = re.split(r"^(?:default |init |label )", body, maxsplit=1, flags=re.MULTILINE)[0]
    return ast.parse(textwrap.dedent(body))


def named_node(nodes, name):
    return next(node for node in nodes if getattr(node, "name", None) == name)


def execute_node(node, namespace):
    exec(compile(ast.Module(body=[node], type_ignores=[]), "<production code>", "exec"), namespace)


def compile_client_label(namespace):
    # This label contains only assignments, Python, branches and returns. Strip
    # Ren'Py syntax without copying its Sunday guard or generation algorithm.
    lines = source(CLIENTS).split("label WhoreNextDayClients", 1)[1].splitlines()
    translated = ["def WhoreNextDayClients" + lines[0]]
    in_python = False
    for line in lines[1:]:
        if line == "    python:":
            in_python = True
            continue
        if line.strip() and not line.startswith("        "):
            in_python = False
        if in_python:
            line = line[4:]
        translated.append(re.sub(r"^(\s*)\$ ", r"\1", line))
    exec("\n".join(translated), namespace)


@pytest.fixture
def runtime():
    namespace = {"player": SimpleNamespace(tavern_management=SimpleNamespace(visitors=60))}
    clothes = init_tree("game/Items/Clothes/InitDressDesc.rpy")
    for node in clothes.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id in ("DressLookValue", "DressTopPart", "DressBottomPart")
            for target in node.targets
        ):
            execute_node(node, namespace)
    people = init_tree(PEOPLE)
    execute_node(named_node(people.body, "people_to_int"), namespace)
    execute_node(named_node(people.body, "GirlWardrobeState"), namespace)
    methods = {}
    for owner, names in (
        ("PeopleInfo", ("sex_stat", "set_sex_stat", "job_value")),
        ("Girl", ("clothing_layer", "tavern_client_attraction", "tavern_glory_hole_client_limit")),
    ):
        owner_node = named_node(people.body, owner)
        for name in names:
            execute_node(named_node(owner_node.body, name), namespace)
            methods[name] = namespace[name]
    execute_node(named_node(init_tree(CLIENTS).body, "tavern_sex_work_day_allowed"), namespace)
    compile_client_label(namespace)
    return SimpleNamespace(namespace=namespace, girl_type=type("ClientTestGirl", (), methods))


def make_girl(runtime, beauty=44, dress="workdress", name="liza", glory=False):
    girl = runtime.girl_type()
    girl.name = name
    girl.stats = {"beauty": beauty}
    girl.jobs = {"jobgloryholeTommorow": int(glory)}
    girl.wardrobe = runtime.namespace["GirlWardrobeState"](owned_items=[dress], day_dress=dress)
    return girl


def generate(runtime, girl, capacity=3, week=1, rolls=(55,), glory_roll=5):
    events = []
    fill_rolls = []

    def randint(low, high, key):
        if key.startswith("port_clients_"):
            value = rolls[int(key.rsplit("_", 1)[1]) % len(rolls)]
            fill_rolls.append(value)
        elif key.startswith("glory_clients_"):
            value = glory_roll
        else:
            value = low
        assert low <= value <= high
        return value

    namespace = runtime.namespace
    namespace.update(
        people=SimpleNamespace(get_info=lambda name: girl if name == girl.name else None),
        calendar_v2=SimpleNamespace(week=week, time_slot=lambda: 3),
        current_game_day=lambda: 20,
        procedural_randint=randint,
        TodaySexEvents_Add=lambda *event: events.append(event),
        CheckIfEventAlreadyExist=lambda *_args: 0,
        renpy=SimpleNamespace(dynamic=lambda *_args: None),
        _args=[],
    )
    namespace["WhoreNextDayClients"](girl.name, capacity, girl.tavern_glory_hole_client_limit())
    count = girl.sex_stat("clients_day_total")
    assert count == len(events)
    return count, events, fill_rolls


def test_higher_beauty_fills_more_slots_under_identical_rolls(runtime):
    low = generate(runtime, make_girl(runtime, beauty=44), rolls=(51, 60, 70))
    high = generate(runtime, make_girl(runtime, beauty=64), rolls=(51, 60, 70))
    assert low[2] == high[2]
    assert low[0] == 1 < high[0] == 3


def test_only_actually_worn_better_outfit_raises_fill(runtime):
    girl = make_girl(runtime)
    before = generate(runtime, girl, rolls=(51, 54, 55))
    girl.wardrobe.add_owned("minidress")
    girl.wardrobe.set_day_dress("minidress", wear_now=False)
    assert girl.tavern_client_attraction() == 50
    assert generate(runtime, girl, rolls=(51, 54, 55)) == before
    girl.wardrobe.wear_day()
    after = generate(runtime, girl, rolls=(51, 54, 55))
    assert girl.tavern_client_attraction() == 56
    assert before[2] == after[2]
    assert before[0] == 1 < after[0] == 3


@pytest.mark.parametrize("removed", [("top",), ("bottom",), ("top", "bottom")])
def test_partial_or_full_stripping_removes_outfit_bonus(runtime, removed):
    girl = make_girl(runtime, dress="minidress")
    for layer in removed:
        girl.wardrobe.remove(layer)
    assert girl.wardrobe.day_dress == "minidress"
    assert girl.wardrobe.owns("minidress")
    assert girl.tavern_client_attraction() == girl.sex_stat("beauty")


@pytest.mark.parametrize("capacity", [0, 3, 4, 5])
@pytest.mark.parametrize("beauty", [0, 44, 100, 150])
def test_regular_clients_never_exceed_reference_capacity(runtime, capacity, beauty):
    girl = make_girl(runtime, beauty=beauty)
    count, _events, _rolls = generate(runtime, girl, capacity=capacity, rolls=(1,))
    assert 0 <= count <= capacity
    assert 0 <= girl.tavern_client_attraction() <= 100


@pytest.mark.parametrize("week,glory", [(5, False), (7, False), (7, True)])
def test_regular_friday_and_all_sunday_work_stay_zero(runtime, week, glory):
    girl = make_girl(runtime, beauty=100, glory=glory)
    count, events, _rolls = generate(runtime, girl, week=week, rolls=(1,))
    assert count == 0
    assert events == []


@pytest.mark.parametrize("visitors", [0, 5, 6, 35, 60, 120])
@pytest.mark.parametrize("week", [1, 5])
def test_glory_visitor_formula_is_unchanged_and_not_appearance_scaled(runtime, visitors, week):
    runtime.namespace["player"].tavern_management.visitors = visitors
    girl = make_girl(runtime, beauty=0, glory=True)
    assert girl.tavern_glory_hole_client_limit() == visitors // 6
    base = min(10, visitors // 6)
    if week == 5:
        base //= 2
    low = generate(runtime, girl, week=week, glory_roll=10)
    girl.set_sex_stat("beauty", 100)
    girl.wardrobe.set_day_dress("minidress", wear_now=True)
    high = generate(runtime, girl, week=week, glory_roll=10)
    assert low == high
    assert low[0] == base * 125 // 100
    assert all(event[3] == "Glory" for event in low[1])


@pytest.mark.parametrize("name", ["liza", "georgett"])
@pytest.mark.parametrize("family,bonus", [("soap", 20), ("luxury_soap", 25)])
def test_soap_gift_updates_owned_beauty_and_client_fill(runtime, name, family, bonus):
    girl = make_girl(runtime, beauty=40, name=name)
    girl.rel = 0
    girl.rebel_baseline = 0
    girl.change_social = lambda **_kwargs: None
    before = generate(runtime, girl, rolls=(60,))
    actions = init_tree(ACTIONS)
    rules_node = next(node for node in actions.body if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == "SOCIAL_ITEM_EFFECT_RULES"
                              for target in node.targets))
    rules = {ast.literal_eval(key): ast.literal_eval(value)
             for key, value in zip(rules_node.value.keys, rules_node.value.values)
             if isinstance(key, ast.Constant) and key.value in ("soap", "luxury_soap")}
    runtime.namespace.update(
        SOCIAL_ITEM_EFFECT_RULES=rules,
        get_game_item=lambda _item_id: SimpleNamespace(custom_properties={
            "social_effect_family": family, "crafted_kind": "soap",
        }),
        _social_item_effect_lines=lambda *_args: [],
    )
    for method in ("_social_item_rule", "player_apply_item_social_effects"):
        execute_node(named_node(actions.body, method), runtime.namespace)
    runtime.namespace["player_apply_item_social_effects"](name, family + "_001", from_gift=True)
    assert girl.stats["beauty"] == 40 + bonus
    after = generate(runtime, girl, rolls=(60,))
    assert before[2] == after[2]
    assert before[0] == 1 < after[0] == 3


@pytest.mark.parametrize("name", ["liza", "georgett"])
def test_barber_benefit_updates_same_owned_beauty_and_fill(runtime, name):
    girl = make_girl(runtime, beauty=40, name=name)
    before = generate(runtime, girl, rolls=(47,))
    barber = source("game/Town/Arts/BarberShop.rpy")
    statement = next(line.split("$ ", 1)[1] for line in barber.splitlines()
                     if '_barber_guest_info.set_sex_stat("beauty"' in line)
    exec(statement, {"_barber_guest_info": girl})
    assert girl.stats["beauty"] == 43
    after = generate(runtime, girl, rolls=(47,))
    assert before[2] == after[2]
    assert before[0] == 1 < after[0] == 3
