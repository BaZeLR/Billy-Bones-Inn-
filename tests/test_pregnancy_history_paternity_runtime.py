"""Execute conception, canonical history projection, and paternity queries together."""

from pathlib import Path
from types import SimpleNamespace
import ast
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_function(path, name, namespace):
    lines = (ROOT / path).read_text(encoding="utf-8-sig").splitlines()
    start = next(i for i, line in enumerate(lines) if line.lstrip().startswith(f"def {name}("))
    indent = len(lines[start]) - len(lines[start].lstrip())
    end = start + 1
    while end < len(lines) and (
        not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) > indent
    ):
        end += 1
    exec(textwrap.dedent("\n".join(lines[start:end])), namespace)
    return namespace[name]


@pytest.fixture
def runtime():
    clock = SimpleNamespace(day=100, roll=0.0)
    rolls = []
    player_cums = []
    namespace = {
        "current_game_day": lambda: clock.day,
        "girl_decision_cycle_state": lambda key: {"phase": "steady", "fertility": 0.45},
        "npc_friend_level": lambda key: 1,
        "tavern_kitchen_fertility_bonus_active": lambda: False,
        "procedural_randint": lambda low, high, **kwargs: high,
        "procedural_random": lambda key: rolls.append(key) or clock.roll,
        "player": SimpleNamespace(
            condition=SimpleNamespace(change=lambda *args: None),
            intimacy=SimpleNamespace(record_cum=lambda day: player_cums.append(day)),
        ),
    }
    people_path = "game/Utilities/General/NPC/PeopleRuntime.rpy"
    load_function(people_path, "people_to_int", namespace)
    methods = {
        name: load_function(people_path, name, namespace)
        for name in ("sex_stat", "set_sex_stat", "add_sex_stat", "pregnancy_days")
    }
    methods.update(
        temporary_conception_permille=lambda self, day: 0,
        is_tavern_worker=lambda self: False,
        arousal_value=lambda self: 0,
        mark_fucked=lambda self, amount: None,
        set_cum_state=lambda self, key, value: self.sex_state.__setitem__(key, value),
        ensure_sex_state=lambda self: self.sex_state,
    )
    npc_type = type("PaternityNPC", (), methods)
    people = {}
    for name in ("amanda", "sandra", "melissa", "clara", "becky", "liza", "georgett", "inga"):
        info = npc_type()
        info.name, info.registry_group, info.mood = name, "girl", "neutral"
        info.corruption = 100
        info.stats = {"pregnancy": 0, "pregfather": "", "ConceptionChance": 10}
        info.sex_state, info.detailed_sex_history = {}, []
        people[name] = info
    namespace["people"] = SimpleNamespace(get_info=people.get)
    names_path = "game/Utilities/General/NPC/NamesSet.rpy"
    names_source = (ROOT / names_path).read_text(encoding="utf-8-sig")
    names_tree = ast.parse(textwrap.dedent(names_source.split("init python:\n", 1)[1].split("\nlabel ", 1)[0]))
    for node in names_tree.body:
        if isinstance(node, ast.Assign):
            namespace[node.targets[0].id] = ast.literal_eval(node.value)
    namespace["calendar_v2"] = SimpleNamespace(day=1, period=1, week=1, time_slot=lambda: 1)
    for name in ("procedural_seed", "procedural_index", "procedural_choice"):
        load_function("game/script.rpy", name, namespace)
    load_function(names_path, "RandomNameCode", namespace)
    for name in ("pregnancy_conception_chance", "pregnancy_check"):
        load_function("game/NPC/Girls/Common/PregnancyCheck.rpy", name, namespace)
    for name in ("_sexevents_int", "sex_history_rows"):
        load_function("game/Utilities/General/Sex/SexEventsTableCode.rpy", name, namespace)
    for name in (
        "_zalet_to_int", "_zalet_text", "_zalet_truthy", "_zalet_history_rows",
        "zalet_suspects", "ZaletSuspectLinesCount", "ZaletSuspectGetValue",
        "ZaletClearSuspectList", "ZaletGetExactDay", "ZaletGetExactId", "ZaletGetSuspectList",
    ):
        load_function("game/NPC/Girls/Common/ZaletOpinionCalc.rpy", name, namespace)
    return SimpleNamespace(ns=namespace, people=people, clock=clock, rolls=rolls, player_cums=player_cums)


@pytest.mark.parametrize("girl", ["amanda", "sandra", "melissa", "clara", "becky", "liza", "georgett", "inga"])
def test_successful_player_conception_reaches_paternity_queries(runtime, girl):
    ns, info = runtime.ns, runtime.people[girl]
    ns["pregnancy_check"](girl, "inside", 1, "you")
    assert (info.pregnancy_days(), info.sex_stat("pregfather")) == (1, "Вы")
    assert ns["ZaletGetExactDay"](girl) == 101
    assert ns["ZaletGetExactId"](girl) == 1
    ns["ZaletGetSuspectList"](girl)
    suspects = ns["zalet_suspects"](girl)
    assert len(suspects) == 1
    assert suspects[0]["DudeName"] == "Вы"
    assert suspects[0]["GirlName"] == girl
    assert suspects[0]["Zalet"] == 1
    assert suspects[0]["Rank"] == (10 if girl == "amanda" else 8)


@pytest.mark.parametrize("father,is_random,father_type,expected_grade", [
    ("legare", 0, "NPC", 6),
    ("Unknown visitor", 1, "Unknown merchant", 1),
])
def test_other_and_random_father_keep_truth_and_distinct_suspect_weight(runtime, father, is_random, father_type, expected_grade):
    ns, info = runtime.ns, runtime.people["sandra"]
    ns["pregnancy_check"]("sandra", "inside", 1, father, is_random, father_type)
    assert info.sex_stat("pregfather") == father
    projected = ns["sex_history_rows"]("sandra")[0]
    assert projected["IsDudeRandom"] == is_random
    assert projected["Zalet"] == 1
    ns["ZaletGetSuspectList"]("sandra")
    assert ns["zalet_suspects"]("sandra")[0]["SuspectGrade"] == expected_grade
    assert not runtime.player_cums


@pytest.mark.parametrize("target", ["ass", "mouth", "tits", "mouthface", "face", "outside"])
def test_non_vaginal_ejaculation_never_rolls_conception(runtime, target):
    ns, info = runtime.ns, runtime.people["becky"]
    ns["pregnancy_check"]("becky", target, 1, "you")
    assert (info.pregnancy_days(), info.sex_stat("pregfather")) == (0, "")
    assert not runtime.rolls
    assert ns["ZaletGetExactDay"]("becky") == -1
    assert ns["ZaletGetExactId"]("becky") == 0
    assert ns["sex_history_rows"]("becky")[0]["Zalet"] == 0


def test_failed_inside_check_records_encounter_but_no_conception(runtime):
    runtime.clock.roll = 0.99
    ns, info = runtime.ns, runtime.people["becky"]
    ns["pregnancy_check"]("becky", "inside", 2, "you")
    assert len(runtime.rolls) == 2
    assert len(set(runtime.rolls)) == 2
    assert (info.pregnancy_days(), info.sex_stat("pregfather")) == (0, "")
    assert len(info.detailed_sex_history) == 2
    assert ns["ZaletGetExactDay"]("becky") == -1
    ns["ZaletGetSuspectList"]("becky")
    assert ns["ZaletSuspectLinesCount"]("becky") == 0


def test_later_partners_do_not_replace_actual_father_but_remain_possible_suspects(runtime):
    ns, info = runtime.ns, runtime.people["sandra"]
    ns["pregnancy_check"]("sandra", "inside", 1, "you")
    runtime.clock.day += 1
    ns["pregnancy_check"]("sandra", "inside", 2, "legare")
    ns["pregnancy_check"]("sandra", "inside", 1, "Unknown visitor", 1, "Unknown merchant")
    ns["pregnancy_check"]("sandra", "mouth", 1, "Oral-only visitor", 1, "Unknown merchant")
    runtime.clock.day += 20
    ns["pregnancy_check"]("sandra", "inside", 1, "Late visitor", 1, "Unknown merchant")
    assert len(runtime.rolls) == 1
    assert info.sex_stat("pregfather") == "Вы"
    assert [row["Zalet"] for row in info.detailed_sex_history] == [1, 0, 0, 0, 0, 0]
    assert ns["ZaletGetExactDay"]("sandra") == 101
    assert ns["ZaletGetExactId"]("sandra") == 1
    ns["ZaletGetSuspectList"]("sandra")
    suspects = ns["zalet_suspects"]("sandra")
    assert [(row["DudeName"], row["Rank"], row["Zalet"]) for row in suspects] == [
        ("Мессир Легаре", 12, 0), ("Вы", 8, 1), ("Unknown visitor", 1, 0),
    ]
    assert ns["ZaletSuspectGetValue"]("sandra", 1, "Times") == 2
    assert ns["ZaletSuspectLinesCount"]("becky") == 0


def test_legacy_personal_suspect_weights_still_apply(runtime):
    ns = runtime.ns
    ns["pregnancy_check"]("becky", "inside", 1, "you")
    ns["pregnancy_check"]("becky", "inside", 1, "eddie")
    ns["ZaletGetSuspectList"]("becky")
    assert [(row["DudeName"], row["Rank"]) for row in ns["zalet_suspects"]("becky")] == [
        ("Эдди", 11), ("Вы", 8),
    ]


def test_projection_preserves_markers_without_mutating_history_or_inventing_conception(runtime):
    info, ns = runtime.people["clara"], runtime.ns
    info.detailed_sex_history = [
        {"RowId": "7", "Day": "33", "GirlName": "clara", "DudeName": "Visitor", "DudeNameType": "NPC", "CumTarget": "inside", "IsDudeRandom": "1", "Zalet": "1"},
        {"day": 34, "partner": "You", "place": "room", "cum_target": "orgasm"},
    ]
    original = [dict(row) for row in info.detailed_sex_history]
    rows = ns["sex_history_rows"]("clara")
    assert (rows[0]["RowId"], rows[0]["Day"], rows[0]["IsDudeRandom"], rows[0]["Zalet"]) == (7, 33, 1, 1)
    assert (rows[1]["GirlName"], rows[1]["IsDudeRandom"], rows[1]["Zalet"]) == ("clara", 0, 0)
    assert ns["ZaletGetExactDay"]("clara") == 33
    assert ns["ZaletGetExactId"]("clara") == 7
    assert info.detailed_sex_history == original


def test_unnamed_partners_use_existing_name_generator_and_keep_first_father(runtime):
    ns, info = runtime.ns, runtime.people["sandra"]
    first_name = ns["RandomNameCode"]("Male", "", key="pregnancy_father_sandra_1")
    second_name = ns["RandomNameCode"]("Male", "", key="pregnancy_father_sandra_2")
    assert second_name != first_name
    actual_choice = ns["procedural_choice"]
    choice_keys = []

    def record_choice(values, key=""):
        choice_keys.append(key)
        return actual_choice(values, key)

    ns["procedural_choice"] = record_choice
    ns["pregnancy_check"]("sandra", "inside", 1, "", 0, "Неизвестный торговец")
    assert info.sex_stat("pregfather") == first_name
    assert info.detailed_sex_history[0]["IsDudeRandom"] == 1
    ns["pregnancy_check"]("sandra", "inside", 1, "", 0, "Неизвестный торговец")
    assert [row["DudeName"] for row in info.detailed_sex_history] == [first_name, second_name]
    assert info.sex_stat("pregfather") == first_name
    ns["ZaletGetSuspectList"]("sandra")
    suspects = ns["zalet_suspects"]("sandra")
    assert {row["DudeName"] for row in suspects} == {first_name, second_name}
    assert [row["Rank"] for row in suspects] == [1, 1]
    assert sum(row["Zalet"] for row in suspects) == 1
    assert choice_keys[0] == "pregnancy_father_sandra_1:nationality"
    assert choice_keys[1].startswith("pregnancy_father_sandra_1:name:")
    assert choice_keys[2] == "pregnancy_father_sandra_2:nationality"
    assert choice_keys[3].startswith("pregnancy_father_sandra_2:name:")


@pytest.mark.parametrize("father_type,nationality", [
    ("Неизвестный негр", "Negr"), ("Неизвестный грузчик", ""),
])
def test_unnamed_partner_passes_exact_legacy_name_arguments(runtime, father_type, nationality):
    ns, calls = runtime.ns, []
    ns["RandomNameCode"] = lambda *args, **kwargs: calls.append((args, kwargs)) or "Generated name"
    ns["pregnancy_check"]("becky", "inside", 2, "", 0, father_type)
    assert calls == [
        (("Male", nationality), {"key": "pregnancy_father_becky_1"}),
        (("Male", nationality), {"key": "pregnancy_father_becky_2"}),
    ]
    assert runtime.people["becky"].sex_stat("pregfather") == "Generated name"
    assert all(row["IsDudeRandom"] == 1 for row in runtime.people["becky"].detailed_sex_history)


@pytest.mark.parametrize("event_type,expected_father", [(3, "Мессир Легаре"), (4, "Отец Герхард")])
@pytest.mark.parametrize("prior_look", [0, 1, 2, 3, 4, 7])
def test_offscreen_father_comes_from_scheduled_actor_not_prior_peeking(runtime, event_type, expected_father, prior_look):
    ns = runtime.ns
    path = "game/Utilities/Time/NextDay_FinishDayEvents.rpy"
    source = (ROOT / path).read_text(encoding="utf-8-sig")
    tree = ast.parse(textwrap.dedent(source.split("init python:\n", 1)[1].split("\nlabel ", 1)[0]))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "next_day_finish_day_events")
    encounter_loop = next(node for node in function.body if isinstance(node, ast.While))
    events = [{"GirlName": "sandra", "Place": "Glory", "EventType": event_type}]
    ns.update(
        SexEvents=SimpleNamespace(today_events=events),
        TodaySexEvents_PopFirst=lambda: events.pop(0),
        week_val=1,
        glory_hole_look=prior_look,
        tavern_sex_work_day_allowed=lambda week: True,
        procedural_randint=lambda low, high, **kwargs: low,
    )
    load_function(path, "_ndf_int", ns)
    exec(compile(ast.Module(body=[encounter_loop], type_ignores=[]), path, "exec"), ns)
    info = runtime.people["sandra"]
    assert info.sex_stat("pregfather") == expected_father
    assert info.detailed_sex_history[0]["DudeName"] == expected_father
    assert info.detailed_sex_history[0]["IsDudeRandom"] == 0
    assert len(runtime.rolls) == 1
    ns["ZaletGetSuspectList"]("sandra")
    assert ns["zalet_suspects"]("sandra")[0]["DudeName"] == expected_father


def test_default_name_generator_keeps_existing_keys_and_stable_calendar_behavior(runtime):
    ns, keys = runtime.ns, []
    actual_choice = ns["procedural_choice"]

    def record_choice(values, key=""):
        keys.append(key)
        return actual_choice(values, key)

    ns["procedural_choice"] = record_choice
    first = ns["RandomNameCode"]("Male")
    second = ns["RandomNameCode"]("Male")
    assert first == second
    assert keys == [
        "procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:169:2",
        "procedural:Utilities/General/NPC/NamesSet.rpy:procedural_choice:187:4",
    ] * 2


def test_existing_special_nationality_pool_is_used_for_generated_father(runtime):
    ns = runtime.ns
    ns["pregnancy_check"]("becky", "inside", 1, "", 0, "Неизвестный негр")
    assert runtime.people["becky"].sex_stat("pregfather") in ns["NegrMaleName"]
    assert ns["sex_history_rows"]("becky")[0]["DudeName"] in ns["NegrMaleName"]
