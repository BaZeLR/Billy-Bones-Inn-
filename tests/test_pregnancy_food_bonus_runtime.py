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


def conception_chance(worker, phase, kitchen_bonus):
    source = SOURCE.read_text(encoding="utf-8-sig")
    start = source.index("    def pregnancy_conception_chance")
    end = source.index("\n    def pregnancy_check", start)
    function_source = textwrap.dedent(source[start:end])
    info = GirlInfo(worker)
    namespace = {
        "people": SimpleNamespace(get_info=lambda _girl: info),
        "girl_decision_cycle_state": lambda _girl: {"phase": phase, "fertility": 0.45},
        "tavern_kitchen_fertility_bonus_active": lambda: kitchen_bonus,
    }
    exec(function_source, namespace)
    return namespace["pregnancy_conception_chance"]("testgirl")


def kitchen_fertility_bonus(honey, milk):
    source = (ROOT / "game/Inn/TavernKitchen.rpy").read_text(encoding="utf-8-sig")
    start = source.index("    def tavern_kitchen_fertility_bonus_active")
    end = source.index("\n    def tavern_kitchen_daily_product_savings", start)
    function_source = textwrap.dedent(source[start:end])
    namespace = {
        "tavern_kitchen_honey_bonus_active": lambda: honey,
        "tavern_kitchen_milk_bonus_active": lambda: milk,
    }
    exec(function_source, namespace)
    return namespace["tavern_kitchen_fertility_bonus_active"]()


@pytest.mark.parametrize(
    "worker,phase,kitchen_bonus,expected",
    (
        (True, "fertile", True, 25),
        (True, "fertile", False, 20),
        (True, "luteal", True, 20),
        (False, "fertile", True, 20),
    ),
)
def test_milk_and_honey_adds_exactly_25_percent_only_to_fertile_tavern_workers(
    worker, phase, kitchen_bonus, expected
):
    assert conception_chance(worker, phase, kitchen_bonus) == expected


@pytest.mark.parametrize(
    "honey,milk,expected",
    ((False, False, False), (True, False, False), (False, True, False), (True, True, True)),
)
def test_fertility_food_bonus_requires_both_milk_and_honey(honey, milk, expected):
    assert kitchen_fertility_bonus(honey, milk) is expected
