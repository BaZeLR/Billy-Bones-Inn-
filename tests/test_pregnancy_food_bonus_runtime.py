from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/NPC/Girls/Common/PregnancyCheck.rpy"


class GirlInfo:
    registry_group = "girl"
    mood = "neutral"

    def __init__(self, worker):
        self.worker = worker

    def sex_stat(self, key, default=0):
        return 20 if key == "ConceptionChance" else default

    def is_tavern_worker(self):
        return self.worker

    def arousal_value(self):
        return 0


def conception_chance(worker, phase, kitchen_bonus, friend_level=2, dad_name="you"):
    source = SOURCE.read_text(encoding="utf-8-sig")
    start = source.index("    def pregnancy_conception_chance")
    end = source.index("\n    def pregnancy_check", start)
    function_source = textwrap.dedent(source[start:end])
    info = GirlInfo(worker)
    namespace = {
        "people": SimpleNamespace(get_info=lambda _girl: info),
        "girl_decision_cycle_state": lambda _girl: {"phase": phase, "fertility": 1.0 if phase == "fertile" else 0.45},
        "tavern_kitchen_fertility_bonus_active": lambda: kitchen_bonus,
        "npc_friend_level": lambda _girl: friend_level,
    }
    exec(function_source, namespace)
    return namespace["pregnancy_conception_chance"]("testgirl", dad_name)


def kitchen_fertility_bonus(boar, honey, milk):
    source = (ROOT / "game/Inn/TavernKitchen.rpy").read_text(encoding="utf-8-sig")
    start = source.index("    def tavern_kitchen_fertility_bonus_active")
    end = source.index("\n    def tavern_kitchen_daily_product_savings", start)
    function_source = textwrap.dedent(source[start:end])
    namespace = {
        "tavern_kitchen_boar_bonus_active": lambda: boar,
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
def test_fertility_food_bonus_requires_boar_milk_and_honey(boar, honey, milk, expected):
    assert kitchen_fertility_bonus(boar, honey, milk) is expected
