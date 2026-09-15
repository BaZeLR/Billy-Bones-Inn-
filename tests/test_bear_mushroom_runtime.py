from pathlib import Path
from types import SimpleNamespace
import textwrap


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"


def read(relative):
    return (GAME / relative).read_text(encoding="utf-8-sig")


def function_source(source, name, indent="    "):
    start = source.index(f"{indent}def {name}(")
    following = source[start + 1 :]
    stops = []
    for marker in (f"\n{indent}def ", "\n    class ", "\ndefault ", "\nlabel ", "\n    # Saved objects"):
        position = following.find(marker)
        if position >= 0:
            stops.append(position + start + 1)
    end = min(stops) if stops else len(source)
    return textwrap.dedent(source[start:end])


def test_bears_drop_one_cumulative_meat_item_and_hunter_accepts_it():
    fight = read("Utilities/Fight/FightSystemRuntime.rpy")
    hunter = read("Town/HunterClub.rpy")
    brown = fight.split('"brown_bear": FightEnemyDefinition(', 1)[1].split('"giant_grizzly":', 1)[0]
    grizzly = fight.split('"giant_grizzly": FightEnemyDefinition(', 1)[1].split('"thug":', 1)[0]

    assert '"bear_meat_001": 1' in brown
    assert '"bear_meat_001": 1' in grizzly
    assert '"bear_meat_001",' in hunter.split("HUNTER_CLUB_SELL_ITEM_IDS", 1)[1]
    assert 'player.add_item(item_id, int(qty or 0))' in fight.split("def fight_collect_victory_loot():", 1)[1].split("\n    def ", 1)[0]


def test_bear_deposit_adds_exact_portions_without_creating_parallel_stock():
    kitchen = read("Inn/TavernKitchen.rpy")
    source = function_source(kitchen, "tavern_kitchen_deposit_food")
    inventory = {"bear_meat_001": 2}
    stock = {}
    applied = []
    item = SimpleNamespace(custom_properties={"kitchen_depositable": True, "kitchen_supply_units": 1000})

    class Player:
        tavern_management = SimpleNamespace(productnum=200)

        @staticmethod
        def item_count(item_id):
            return inventory.get(item_id, 0)

        @staticmethod
        def remove_item(item_id, quantity):
            if inventory.get(item_id, 0) < quantity:
                return False
            inventory[item_id] -= quantity
            return True

    namespace = {
        "player": Player(),
        "get_game_item": lambda item_id: item if item_id == "bear_meat_001" else None,
        "tavern_kitchen_depositable_food_ids": lambda: ("bear_meat_001",),
        "tavern_storage_supplies_stock": lambda: stock,
        "tavern_kitchen_apply_deposit_effect": lambda item_id, quantity: applied.append((item_id, quantity)),
    }
    exec(source, namespace)
    deposit = namespace["tavern_kitchen_deposit_food"]

    assert deposit("bear_meat_001", 1) == 1
    assert Player.tavern_management.productnum == 1200
    assert inventory == {"bear_meat_001": 1}
    assert stock == {}

    assert deposit("bear_meat_001", 0) == 1
    assert Player.tavern_management.productnum == 2200
    assert inventory == {"bear_meat_001": 0}
    assert stock == {}
    assert applied == [("bear_meat_001", 1), ("bear_meat_001", 1)]


def test_bear_effect_duration_and_meat_bonus_do_not_double():
    kitchen = read("Inn/TavernKitchen.rpy")
    apply_source = function_source(kitchen, "tavern_kitchen_apply_deposit_effect")
    worker = SimpleNamespace(is_tavern_worker=lambda: True, arousal=0)
    visitor = SimpleNamespace(is_tavern_worker=lambda: False, arousal=0)
    worker.add_arousal = lambda amount: setattr(worker, "arousal", worker.arousal + amount)
    visitor.add_arousal = lambda amount: setattr(visitor, "arousal", visitor.arousal + amount)
    effects = {}
    bear = SimpleNamespace(custom_properties={
        "kitchen_deposit_team_arousal_bonus": 5,
        "kitchen_meat_effect_days": 14,
    })

    def add_effect(key, days):
        effects[key] = effects.get(key, 0) + days

    namespace = {
        "people": SimpleNamespace(girl_items=lambda: [("worker", worker), ("visitor", visitor)]),
        "player": SimpleNamespace(add_item=lambda *_args: None),
        "get_game_item": lambda item_id: bear if item_id == "bear_meat_001" else None,
        "tavern_kitchen_add_food_effect": add_effect,
    }
    exec(apply_source, namespace)

    assert namespace["tavern_kitchen_apply_deposit_effect"]("bear_meat_001", 2) == "bear"
    assert effects == {"bear_days": 28}
    assert worker.arousal == 10
    assert visitor.arousal == 0

    meat_source = function_source(kitchen, "tavern_kitchen_meat_bonus_active")
    for boar, bear_active, expected in (
        (False, False, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ):
        meat_namespace = {
            "tavern_kitchen_boar_bonus_active": lambda value=boar: value,
            "tavern_kitchen_bear_bonus_active": lambda value=bear_active: value,
        }
        exec(meat_source, meat_namespace)
        assert meat_namespace["tavern_kitchen_meat_bonus_active"]() is expected


def player_intimacy_class():
    source = read("Utilities/General/Player/Player.rpy")
    start = source.index("    class PlayerIntimacy(object):")
    end = source.index("\n    class PlayerChores(object):", start)
    item = SimpleNamespace(custom_properties={"player_libido_days": 2, "player_daily_cum_limit": 4})
    namespace = {
        "player_to_int": lambda value, default=0: int(value if value is not None else default),
        "current_game_day": lambda: 10,
        "get_game_item": lambda item_id: item if item_id == "special_mushroom_001" else None,
    }
    exec(textwrap.dedent(source[start:end]), namespace)
    return namespace["PlayerIntimacy"]


def test_eaten_mushroom_limit_is_four_on_consumption_day_and_following_day():
    intimacy = player_intimacy_class()()

    assert intimacy.apply_consumed_item_effect("special_mushroom_001", 10) is True
    assert intimacy.temporary_libido == {"item_id": "special_mushroom_001", "until_day": 11}
    assert intimacy.daily_cum_limit(10) == 4
    assert intimacy.daily_cum_limit(11) == 4
    assert intimacy.daily_cum_limit(12) == 2

    intimacy.can_cum_daily = 5
    assert intimacy.daily_cum_limit(10) == 5
    intimacy.ellona_cursed = 1
    assert intimacy.daily_cum_limit(10) == 0
    assert intimacy.can_cum(10) is False


def test_mushroom_consumption_keeps_the_pre_midnight_start_day():
    actions = read("Utilities/General/Common/Actions.rpy")
    source = function_source(actions, "_player_apply_item_consume_profile")
    day = {"value": 10}
    activation_days = []
    item = SimpleNamespace(name="редкий гриб")

    class Intimacy:
        @staticmethod
        def apply_consumed_item_effect(_item_id, day_value):
            activation_days.append(day_value)

    class Player:
        intimacy = Intimacy()

        @staticmethod
        def item_count(_item_id):
            return 1

        @staticmethod
        def remove_item(_item_id, _quantity):
            return True

        @staticmethod
        def change_stat(_stat, _amount):
            return None

        @staticmethod
        def add_item(_item_id, _quantity):
            return None

    class Clock:
        @staticmethod
        def advance_minutes(_minutes):
            day["value"] = 11

    namespace = {
        "get_object_id": lambda item_id: item_id,
        "current_game_day": lambda: day["value"],
        "player": Player(),
        "calendar_v2": Clock(),
        "update_stat_state": lambda: None,
        "_player_item_consume_profile": lambda _item_id, _action: {
            "item_id": "special_mushroom_001",
            "item_obj": item,
            "action_key": "eat",
            "minutes": 10,
            "energy_gain": 2,
            "fun_gain": 5,
            "text": "effect",
            "outputs": [],
        },
    }
    exec(source, namespace)

    result = namespace["_player_apply_item_consume_profile"]("special_mushroom_001", "eat", True)
    assert result["ok"] is True
    assert day["value"] == 11
    assert activation_days == [10]


def girl_effect_class():
    source = read("Utilities/General/NPC/PeopleRuntime.rpy")
    namespace = {
        "people_to_int": lambda value, default=0: int(value if value is not None else default),
        "current_game_day": lambda: 20,
        "get_game_item": lambda item_id: SimpleNamespace(custom_properties={
            "shared_fertility_days": 2,
            "shared_conception_permille": 550,
        }) if item_id == "special_mushroom_001" else None,
    }

    class GirlEffect:
        pass

    for name in (
        "ensure_temporary_fertility_state",
        "apply_shared_item_effect",
        "temporary_fertility_active",
        "temporary_conception_permille",
    ):
        exec(function_source(source, name, "        "), namespace)
        setattr(GirlEffect, name, namespace[name])
    return GirlEffect


def test_shared_mushroom_fertility_is_owned_by_target_and_expires_after_two_days():
    girl = girl_effect_class()()
    girl.temporary_fertility = None

    assert girl.apply_shared_item_effect("special_mushroom_001", 20) is True
    assert girl.temporary_fertility == {"item_id": "special_mushroom_001", "until_day": 21}
    assert girl.temporary_conception_permille(20) == 550
    assert girl.temporary_conception_permille(21) == 550
    assert girl.temporary_conception_permille(22) == 0


def test_item_use_and_accepted_gift_are_the_only_timed_effect_entry_points():
    actions = read("Utilities/General/Common/Actions.rpy")
    consume = function_source(actions, "_player_apply_item_consume_profile")
    social = function_source(actions, "player_apply_item_social_effects")
    share = function_source(actions, "player_share_item_with")

    assert consume.index("player.remove_item(item_key, 1)") < consume.index("player.intimacy.apply_consumed_item_effect")
    assert "if consume_from_inventory:" in consume
    assert "if from_gift:" in social
    assert 'shared_effect_applied = info.apply_shared_item_effect(item_key, current_game_day())' in social
    assert share.index("removed = player.remove_item(item_key, 1)") < share.index("player_apply_item_social_effects(key, item_key, True)")


def test_mushroom_spawn_and_item_values_have_one_static_authority():
    items = read("Items/Shops/HunterClubItems.rpy")
    block = items.split('object_id="special_mushroom_001"', 1)[1].split("\n    SpecialHerbsItem", 1)[0]
    dark = read("Forest/ForestDarkWoods.rpy")
    cave = read("Forest/ForestCave.rpy")

    assert block.count('"player_libido_days": 2') == 1
    assert block.count('"player_daily_cum_limit": 4') == 1
    assert block.count('"shared_fertility_days": 2') == 1
    assert block.count('"shared_conception_permille": 550') == 1
    assert "spawn_zones" not in block
    assert "spawn_rarity" not in block
    assert dark.count('{"item_id": "special_mushroom_001", "frequency": 20, "units": 1}') == 1
    assert cave.count('{"item_id": "special_mushroom_001", "frequency": 20, "units": 1}') == 1


def test_v90_migration_merges_spawn_rule_once_without_rebuilding_saved_rooms():
    migration = read("TractirSaveSync.rpy")
    source = function_source(migration, "updateSave_V90")
    canonical = {"item_id": "special_mushroom_001", "frequency": 20, "units": 1}
    existing_spawn = [{"item_id": "moss_001", "units": 2}]

    class ActorEffect:
        def __init__(self):
            self.calls = 0

        def ensure_temporary_libido_state(self):
            self.calls += 1

        def ensure_temporary_fertility_state(self):
            self.calls += 1

    player_effect = ActorEffect()
    girl_effect = ActorEffect()
    saved_rooms = {
        "ForestDarkWoods": SimpleNamespace(custom_properties={
            "spawn_rules": [
                {"item_id": "mushroom_001", "frequency": 2, "units": 3},
                dict(canonical),
                dict(canonical),
            ],
            "spawned_items": list(existing_spawn),
        }),
        "ForestCave": SimpleNamespace(custom_properties={
            "spawn_rules": [{"item_id": "moss_001", "frequency": 2, "units": 2}],
            "spawned_items": list(existing_spawn),
        }),
    }
    definitions = {
        room_code: SimpleNamespace(custom_properties={"spawn_rules": [dict(canonical)]})
        for room_code in saved_rooms
    }
    namespace = {
        "player": SimpleNamespace(intimacy=player_effect),
        "people": SimpleNamespace(girl_values=lambda: [girl_effect]),
        "rooms": SimpleNamespace(get=lambda room_code: saved_rooms.get(room_code)),
        "roomDefinitions": definitions,
    }
    exec(source, namespace)
    migrate = namespace["updateSave_V90"]

    migrate()
    migrate()
    for room in saved_rooms.values():
        rules = room.custom_properties["spawn_rules"]
        assert sum(row.get("item_id") == "special_mushroom_001" for row in rules) == 1
        assert room.custom_properties["spawned_items"] == existing_spawn


def test_all_mc_cum_limit_readers_use_player_intimacy_owner():
    sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in GAME.rglob("*.rpy")
        if path.name not in ("Player.rpy", "TractirSaveSync.rpy", "TavernCursedSofa.rpy")
    )
    assert "player.intimacy.can_cum_daily" not in sources
    assert "state.intimacy.can_cum_daily" not in sources
    assert "_cock_intimacy.can_cum_daily" not in sources


def test_pregnancy_roll_remains_inside_only():
    pregnancy = read("NPC/Girls/Common/PregnancyCheck.rpy")
    roll = pregnancy.split("def pregnancy_check", 1)[1]
    conception = roll.rsplit("if cum_place == 'inside':", 1)[1]

    assert "if cum_place == 'inside':" in roll
    assert 'girl_info.add_sex_stat("cuminside", 1)' in conception
    assert 'girl_info.sex_stat("cuminside", 0)' in conception
    assert "procedural_random(conception_key)" in conception
