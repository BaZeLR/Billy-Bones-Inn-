from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/NPC/Girls/Common/PregnancyCheck.rpy"


class GirlInfo:
    registry_group = "girl"
    mood = "neutral"

    def __init__(self, worker, temporary_chance=0, bathday_day=-1):
        self.worker = worker
        self.temporary_chance = temporary_chance
        self.bathday_day = bathday_day

    def sex_stat(self, key, default=0):
        return 20 if key == "ConceptionChance" else default

    def is_tavern_worker(self):
        return self.worker

    def arousal_value(self):
        return 0

    def temporary_conception_permille(self, _day):
        return self.temporary_chance


def conception_chance(worker, phase, kitchen_bonus, friend_level=2, dad_name="you", temporary_chance=0, bathday_day=-1):
    source = SOURCE.read_text(encoding="utf-8-sig")
    start = source.index("    def pregnancy_conception_chance")
    end = source.index("\n    def pregnancy_check", start)
    function_source = textwrap.dedent(source[start:end])
    info = GirlInfo(worker, temporary_chance, bathday_day)
    namespace = {
        "people": SimpleNamespace(get_info=lambda _girl: info),
        "girl_decision_cycle_state": lambda _girl: {"phase": phase, "fertility": 1.0 if phase == "fertile" else 0.45},
        "tavern_kitchen_fertility_bonus_active": lambda: kitchen_bonus,
        "npc_friend_level": lambda _girl: friend_level,
        "current_game_day": lambda: 10,
    }
    exec(function_source, namespace)
    return namespace["pregnancy_conception_chance"]("testgirl", dad_name)


def kitchen_fertility_bonus(meat, honey, milk):
    source = (ROOT / "game/Inn/TavernKitchen.rpy").read_text(encoding="utf-8-sig")
    start = source.index("    def tavern_kitchen_fertility_bonus_active")
    end = source.index("\n    def tavern_kitchen_daily_product_savings", start)
    function_source = textwrap.dedent(source[start:end])
    namespace = {
        "tavern_kitchen_meat_bonus_active": lambda: meat,
        "tavern_kitchen_honey_bonus_active": lambda: honey,
        "tavern_kitchen_milk_bonus_active": lambda: milk,
    }
    exec(function_source, namespace)
    return namespace["tavern_kitchen_fertility_bonus_active"]()


@pytest.mark.parametrize(
    "worker,phase,kitchen_bonus,friend_level,dad_name,expected",
    (
        (True, "fertile", True, 2, "you", 300),
        (True, "fertile", True, 1, "you", 93),
        (True, "fertile", False, 2, "you", 93),
        (True, "luteal", True, 2, "you", 60),
        (False, "fertile", True, 2, "you", 93),
        (True, "fertile", True, 2, "other", 31),
    ),
)
def test_full_food_bonus_sets_thirty_percent_only_for_friendly_fertile_tavern_worker_with_mc(
    worker, phase, kitchen_bonus, friend_level, dad_name, expected
):
    assert conception_chance(worker, phase, kitchen_bonus, friend_level, dad_name) == expected


@pytest.mark.parametrize(
    "boar,honey,milk,expected",
    (
        (False, False, False, False),
        (True, False, False, False),
        (True, True, False, False),
        (True, False, True, False),
        (False, True, True, False),
        (True, True, True, True),
    ),
)
def test_fertility_food_bonus_requires_meat_milk_and_honey(boar, honey, milk, expected):
    assert kitchen_fertility_bonus(boar, honey, milk) is expected


def test_shared_special_mushroom_overrides_mc_conception_chance_only():
    assert conception_chance(True, "luteal", False, dad_name="you", temporary_chance=550) == 550
    assert conception_chance(True, "luteal", False, dad_name="other", temporary_chance=550) == 20


def test_bathday_adds_five_percentage_points_only_on_bath_day():
    assert conception_chance(True, "luteal", False, bathday_day=10) == 110
    assert conception_chance(True, "luteal", False, bathday_day=9) == 60
    assert conception_chance(True, "fertile", True, bathday_day=10) == 350
    assert conception_chance(True, "luteal", False, temporary_chance=550, bathday_day=10) == 600


def test_conception_roll_is_unique_per_girl_and_inside_attempt():
    source = SOURCE.read_text(encoding="utf-8-sig")
    start = source.index("    def pregnancy_check")
    end = source.index("\n# Ren'Py label", start)
    function_source = textwrap.dedent(source[start:end])

    class RuntimeGirl:
        registry_group = "girl"
        corruption = 10

        def __init__(self):
            self.stats = {"cuminside": 0, "pregnancy": 0}
            self.detailed_sex_history = []

        def sex_stat(self, key, default=0):
            return self.stats.get(key, default)

        def add_sex_stat(self, key, amount=1):
            self.stats[key] = int(self.stats.get(key, 0) or 0) + int(amount or 0)

        def set_sex_stat(self, key, value):
            self.stats[key] = value

        def pregnancy_days(self):
            return int(self.stats.get("pregnancy", 0) or 0)

        def mark_fucked(self, _amount=1):
            return None

        def set_cum_state(self, _key, _value):
            return None

        def clear_cum(self, *_keys):
            return None

        def change_social(self, **_kwargs):
            return None

    girls = {"amanda": RuntimeGirl(), "becky": RuntimeGirl()}
    conception_keys = []
    namespace = {
        "people": SimpleNamespace(get_info=lambda key: girls.get(str(key).lower())),
        "player": SimpleNamespace(
            condition=SimpleNamespace(change=lambda *_args: None),
            intimacy=SimpleNamespace(record_cum=lambda *_args: None),
        ),
        "current_game_day": lambda: 10,
        "pregnancy_conception_chance": lambda *_args: 100,
        "procedural_randint": lambda *_args, **_kwargs: 999,
        "procedural_random": lambda key="": conception_keys.append(key) or 1.0,
    }
    exec(function_source, namespace)
    check = namespace["pregnancy_check"]

    check("amanda", "inside", 1, "you")
    check("amanda", "inside", 1, "you")
    check("becky", "inside", 1, "you")

    assert conception_keys == [
        "pregnancy_conception_amanda_1",
        "pregnancy_conception_amanda_2",
        "pregnancy_conception_becky_1",
    ]
