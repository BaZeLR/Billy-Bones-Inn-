import ast
from pathlib import Path
import re
from types import SimpleNamespace
import textwrap

import pytest


GAME = Path(__file__).resolve().parents[1] / "game"
FIGHT = "Utilities/Fight/FightSystemRuntime.rpy"
HUNTER = "Town/HunterClub.rpy"
SKIN = "boar_skin_001"


def load_nodes(relative, names, namespace):
    source = (GAME / relative).read_text(encoding="utf-8-sig")
    block = re.split(r"\n(?=\S)", source.split("python:", 1)[1], maxsplit=1)[0]
    tree = ast.parse(textwrap.dedent(block))
    selected = []
    for node in tree.body:
        node_names = {getattr(node, "name", "")}
        if isinstance(node, ast.Assign):
            node_names.update(target.id for target in node.targets if isinstance(target, ast.Name))
        if node_names.intersection(names):
            selected.append(node)
    assert len(selected) == len(names), (relative, names)
    exec(compile(ast.Module(body=selected, type_ignores=[]), relative, "exec"), namespace)


@pytest.fixture
def runtime():
    ns = {}
    load_nodes("Utilities/General/Classes/GameObjectTemplate.rpy", {
        "game_object_registry", "room_rule_registry", "register_room_rule",
        "GameObject", "get_object_id", "get_game_item", "get_game_object",
    }, ns)
    load_nodes("Items/Core/GameItem.rpy", {"game_item_registry", "GameItem"}, ns)
    load_nodes("Items/Shops/HunterClubItems.rpy", {
        "BoarSkinItem", "BoarFangItem", "BoarMeatItem", "WolfSkinItem", "BrownBearFurItem",
    }, ns)
    load_nodes("Utilities/General/Player/Player.rpy", {
        "player_to_int", "player_normalize_item_id", "player_normalize_inventory",
        "PlayerInventory", "PlayerEconomy", "Player",
    }, ns)
    player = object.__new__(ns["Player"])
    player.inventory = ns["PlayerInventory"]()
    player.economy = ns["PlayerEconomy"]()
    player.appearance = SimpleNamespace(ensure_item_life=lambda _item_id: None)
    ns["player"] = player
    ns["rooms"] = {"HunterClub": SimpleNamespace(state={"trade_selection": {}})}
    ns["current_game_day"] = lambda: 3
    ns["procedural_randint"] = lambda minimum, maximum, _key: minimum
    ns["fight_rng_key"] = lambda value: value
    load_nodes(FIGHT, {
        "FightEnemyDefinition", "FightEnemyInstance", "FightInfo", "HuntInfo",
        "FIGHT_ENEMY_DEFINITIONS", "fight_collect_victory_loot",
        "fight_dead_enemy_exploration_reward", "fight_roll_loot_quantity",
        "forest_trap_can_check", "forest_trap_check",
    }, ns)
    ns["fight"] = ns["FightInfo"]()
    ns["hunt"] = ns["HuntInfo"]()
    load_nodes(HUNTER, {
        "HUNTER_CLUB_TRADE_MAX_QTY", "HUNTER_CLUB_SELL_ITEM_IDS",
        "hunter_club_sell_entries", "hunter_club_sell_max_quantity",
        "hunter_club_trade_entries", "hunter_club_trade_selected_qty",
        "hunter_club_apply_trade",
    }, ns)
    return ns


def test_boar_skin_is_one_registered_carryable_stackable_item(runtime):
    item = runtime["get_game_item"](SKIN)
    assert item is runtime["BoarSkinItem"]
    assert runtime["game_object_registry"][SKIN] is item
    assert item.name == "кабанья шкура"
    assert item.description
    assert item.carriable and item.stackable
    assert item.price == 35
    assert runtime["WolfSkinItem"].price < item.price < runtime["BrownBearFurItem"].price
    assert item.custom_properties == {
        "item_kind": "animal_loot", "animal_kind": "boar", "loot_kind": "skin",
    }


@pytest.mark.parametrize("count", (1, 2, 3))
@pytest.mark.parametrize("meat_per_boar", (1, 3))
def test_each_dead_boar_adds_one_hide_and_preserves_meat_range(runtime, count, meat_per_boar):
    definition = runtime["FIGHT_ENEMY_DEFINITIONS"]["boar"]
    assert definition.loot["boar_meat_001"] == (1, 3)
    runtime["procedural_randint"] = lambda minimum, maximum, _key: (
        maximum if meat_per_boar == 3 else minimum
    )
    runtime["player"].add_item(SKIN, 2)
    for index in range(count + 1):
        enemy = runtime["FightEnemyInstance"](definition, index)
        if index < count:
            enemy.health = 0
        runtime["fight"].enemy_party.append(enemy)

    loot = runtime["fight_collect_victory_loot"]()

    assert loot == {
        SKIN: count, "boar_fang_001": count, "boar_meat_001": count * meat_per_boar,
    }
    assert runtime["player"].item_count(SKIN) == 2 + count
    assert runtime["player"].item_count("boar_meat_001") == count * meat_per_boar


@pytest.mark.parametrize("roll", (35, 70, 71, 100))
def test_only_boar_trap_reward_gives_a_hide_and_cannot_repeat(runtime, roll):
    runtime["hunt"].trap_rooms["Forest"] = {"day": 2, "armed_count": 1}
    runtime["procedural_randint"] = lambda *_args: roll
    result = runtime["forest_trap_check"]("Forest")

    assert result["ok"] is True
    assert runtime["player"].item_count(SKIN) == (1 if roll > 70 else 0)
    if roll > 70:
        assert result["loot"] == {SKIN: 1, "boar_meat_001": 1, "boar_fang_001": 1}
        assert "шкуру" in result["text"]
    assert runtime["forest_trap_check"]("Forest")["ok"] is False


def test_louise_sells_selected_hides_using_catalog_price_and_real_inventory(runtime):
    player = runtime["player"]
    player.add_item(SKIN, 3)
    player.add_item("boar_meat_001", 2)
    money_before = player.economy.money
    rows = runtime["hunter_club_sell_entries"]()
    hide_row = next(row for row in rows if row["item_id"] == SKIN)
    assert hide_row["count"] == 3
    assert hide_row["price"] == runtime["BoarSkinItem"].price
    assert hide_row["total_price"] == 105

    selection = runtime["rooms"]["HunterClub"].state["trade_selection"]
    selection[SKIN] = 2
    result = runtime["hunter_club_apply_trade"]("sell")
    assert result["ok"] is True
    assert "кабанья шкура x2" in result["text"]
    assert player.item_count(SKIN) == 1
    assert player.item_count("boar_meat_001") == 2
    assert player.economy.money == money_before + 70

    # An old selection cannot sell more than the remaining inventory.
    assert runtime["hunter_club_apply_trade"]("sell")["ok"] is True
    assert player.item_count(SKIN) == 0
    assert player.economy.money == money_before + 105
    assert runtime["hunter_club_apply_trade"]("sell")["ok"] is False
    assert player.economy.money == money_before + 105
    assert SKIN not in {row["item_id"] for row in runtime["hunter_club_sell_entries"]()}
