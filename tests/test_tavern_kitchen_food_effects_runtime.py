from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Inn/TavernKitchen.rpy"


class Worker:
    def __init__(self, worker=True):
        self.worker = worker
        self.arousal = 0
        self.mana = 0

    def is_tavern_worker(self):
        return self.worker

    def add_arousal(self, amount):
        self.arousal += amount

    def change_mana(self, amount, _reason):
        self.mana += amount


def apply_deposit(item_id, item_count):
    source = SOURCE.read_text(encoding="utf-8-sig")
    start = source.index("    def tavern_kitchen_apply_deposit_effect")
    end = source.index("\n    def tavern_kitchen_consume_stock_units", start)
    function_source = textwrap.dedent(source[start:end])
    worker = Worker(True)
    visitor = Worker(False)
    food_effects = {}
    inventory = {}
    boar = SimpleNamespace(
        custom_properties={
            "kitchen_deposit_team_arousal_bonus": 5,
            "kitchen_deposit_outputs": (("dog_bone_001", 3),),
        }
    )

    def add_food_effect(key, days):
        food_effects[key] = days

    def add_item(item_key, amount):
        inventory[item_key] = inventory.get(item_key, 0) + amount

    namespace = {
        "people": SimpleNamespace(girl_items=lambda: [("worker", worker), ("visitor", visitor)]),
        "player": SimpleNamespace(add_item=add_item),
        "get_game_item": lambda key: boar if key == "boar_meat_001" else None,
        "tavern_kitchen_add_food_effect": add_food_effect,
    }
    exec(function_source, namespace)
    result = namespace["tavern_kitchen_apply_deposit_effect"](item_id, item_count)
    return result, worker, visitor, food_effects, inventory


@pytest.mark.parametrize("units", (1, 2))
def test_boar_deposit_gives_only_worker_arousal_and_three_bones_per_unit(units):
    result, worker, visitor, food_effects, inventory = apply_deposit("boar_meat_001", units)

    assert result == "boar"
    assert worker.arousal == 5 * units
    assert visitor.arousal == 0
    assert worker.mana == 0
    assert visitor.mana == 0
    assert inventory == {"dog_bone_001": 3 * units}
    assert food_effects == {"boar_days": units}


def test_honey_deposit_uses_only_the_expiring_food_effect():
    result, worker, visitor, food_effects, inventory = apply_deposit("honey_comb_001", 1)

    assert result == "honey"
    assert worker.mana == 0
    assert visitor.mana == 0
    assert worker.arousal == 0
    assert inventory == {}
    assert food_effects == {"honey_days": 1}
