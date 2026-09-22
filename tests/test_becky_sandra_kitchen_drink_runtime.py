"""Execute the real kitchen drink effects against the NPC-owned arousal API."""

from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
KITCHEN = (ROOT / "game/Inn/TavernKitchen.rpy").read_text(encoding="utf-8-sig")
PEOPLE = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
BREAKFAST = (ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")


def load_function(source, name, namespace):
    lines = source.splitlines()
    start = next(index for index, line in enumerate(lines) if line.lstrip().startswith(f"def {name}("))
    indent = len(lines[start]) - len(lines[start].lstrip())
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) > indent):
        end += 1
    exec(textwrap.dedent("\n".join(lines[start:end])), namespace)
    return namespace[name]


def kitchen_fixture(arousal):
    namespace = {}
    for name in ("people_to_int", "people_clamp"):
        load_function(PEOPLE, name, namespace)
    methods = {
        name: load_function(PEOPLE, name, namespace)
        for name in ("ensure_sex_state", "arousal_value", "set_arousal", "add_arousal", "change_social")
    }
    npc_type = type("KitchenNPC", (), methods)
    people = {}
    for name in ("sandra", "becky", "melissa"):
        info = npc_type()
        info.rel, info.openness, info.corruption, info.fun = 9, 2, 20, 10
        info.sex_state = {"arousal": arousal}
        people[name] = info

    stock = {"libido_tincture_001": 1, "energy_tea_001": 1}
    consumed = []
    player_stats = {"fun": 10}

    def remove_item(item_id, count):
        assert stock[item_id] >= count
        stock[item_id] -= count
        consumed.append((item_id, count))
        return True

    def change_stat(stat, amount):
        player_stats[stat] += amount

    namespace.update(
        Sandra=people["sandra"], Becky=people["becky"],
        people=SimpleNamespace(get_info=people.get),
        player=SimpleNamespace(remove_item=remove_item, change_stat=change_stat),
        scene_runtime=SimpleNamespace(text=""),
    )
    load_function(BREAKFAST, "tavern_kitchen_spicy_tincture_apply", namespace)
    return namespace, people, stock, consumed, player_stats


def execute_effect_lines(branch, namespace):
    for line in branch.splitlines():
        stripped = line.strip()
        if stripped.startswith("$ "):
            exec(stripped[2:], namespace)


@pytest.mark.parametrize("arousal", [0, 40, 98, 100])
def test_hot_honey_drink_adds_five_arousal_to_both_without_changing_existing_social_effects(arousal):
    namespace, people, stock, consumed, player_stats = kitchen_fixture(arousal)
    branch = KITCHEN.split('"Подать горячую медовую настойку" if ', 1)[1].split(
        'vscene "images/tavern/kitchen/becky_visit_1.png"', 1
    )[0]
    execute_effect_lines(branch, namespace)

    for name in ("sandra", "becky"):
        assert people[name].arousal_value() == min(100, arousal + 5)
        assert (people[name].rel, people[name].openness) == (10, 3)
        assert people[name].fun == 10
    assert people["sandra"].corruption == 21
    assert people["becky"].corruption == 20
    assert people["melissa"].arousal_value() == arousal
    assert (people["melissa"].rel, people["melissa"].openness, people["melissa"].corruption) == (9, 2, 20)
    assert consumed == [("libido_tincture_001", 1)]
    assert stock == {"libido_tincture_001": 0, "energy_tea_001": 1}
    assert player_stats == {"fun": 12}


@pytest.mark.parametrize("arousal", [0, 40, 98, 100])
def test_ordinary_tea_keeps_arousal_corruption_and_openness_unchanged(arousal):
    namespace, people, stock, consumed, player_stats = kitchen_fixture(arousal)
    branch = KITCHEN.split('"Угостить Сандру и Бекки бодрящим чаем" if ', 1)[1].split(
        "$ scene_runtime.text =", 1
    )[0]
    execute_effect_lines(branch, namespace)

    for name in ("sandra", "becky"):
        assert people[name].arousal_value() == arousal
        assert (people[name].rel, people[name].openness, people[name].corruption, people[name].fun) == (10, 2, 20, 11)
    assert consumed == [("energy_tea_001", 1)]
    assert stock == {"libido_tincture_001": 1, "energy_tea_001": 0}
    assert player_stats == {"fun": 11}
