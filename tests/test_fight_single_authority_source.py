from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8-sig")


def test_fight_level_is_derived_from_player_exploration_without_a_mirror():
    runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    player = source("game/Utilities/General/Player/Player.rpy")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "def fight_player_level():" in runtime
    assert "effective_player_exploration()" in runtime
    assert "fight_sync_level_from_exploration" not in game_sources
    assert "combat.fight_level" not in game_sources
    assert "self.fight_level" not in player
    assert "hunt.unlocked" not in game_sources


def test_inventory_backed_fight_supplies_are_not_copied_into_combat_state():
    runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    player = source("game/Utilities/General/Player/Player.rpy")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "def fight_supply_count(" in runtime
    assert "def fight_consume_supply(" in runtime
    assert "def fight_sync_supply_from_inventory" not in game_sources
    assert "combat.supply" not in game_sources
    assert "self.supply" not in player
    assert 'self.special_supply = {"bees_bomb": 0}' in player
    assert 'legacy_name = "sup" + "ply"' not in runtime
    assert "def updateSave_V8():" in source("game/TractirSaveSync.rpy")


def test_combat_queries_do_not_repair_runtime_state():
    runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    stat = source("game/Utilities/General/Screens/stat.rpy")
    migration = source("game/TractirSaveSync.rpy")

    assert "def fight_ensure_runtime" not in runtime
    assert "fight_ensure_runtime()" not in runtime + stat
    assert "fight.enemy_state" not in runtime
    assert "fight.side_log" not in runtime
    assert "fight.outcome_text" not in runtime
    assert "def updateSave_V46():" in migration


def test_fight_result_hunt_state_and_fatal_ending_have_distinct_owners():
    runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    town = source("game/Town/RandomTownEvents.rpy")
    progress = source("game/Utilities/General/Common/AchievementsEndings.rpy")
    migration = source("game/TractirSaveSync.rpy")

    assert "self.last_result = {}" in runtime
    assert "hunt.last_result" not in runtime + town + progress
    assert "fight.last_result" in runtime + town
    assert 'self.boss_fatal_enemy = ""' in progress
    assert "fight.enemy_state" not in progress
    assert 'getattr(hunt, "last_result", {})' in migration
    assert 'fight_state.pop("enemy_state", None)' not in migration


def test_player_party_is_the_only_dog_combat_membership_authority():
    runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    dog = source("game/NPC/Secondary/DogCompanion.rpy")
    debug = source("game/Utilities/General/Common/DebugTools.rpy")
    migration = source("game/TractirSaveSync.rpy")

    assert "self.in_company" not in dog
    assert ".in_company" not in runtime + dog + debug
    assert '"dog" in player.combat.party' in runtime + dog + debug
    assert 'dog_state.pop("in_company", None)' in migration


def test_hunting_traps_use_one_room_map_and_migrate_old_summary_once():
    runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    migration = source("game/TractirSaveSync.rpy")

    assert "trap_state" not in runtime
    assert "self.trap_rooms = {}" in runtime
    assert "def updateSave_V20():" in migration
    assert 'delattr(hunt, "trap_state")' in migration


def test_enemy_instances_own_live_state_as_direct_fields_without_a_data_wrapper():
    runtime = source("game/Utilities/Fight/FightSystemRuntime.rpy")
    instance = runtime.split("class FightEnemyInstance(object):", 1)[1].split("class FightInfo(object):", 1)[0]

    for field_name in (
        "object_id", "name", "enemy_type", "index", "health", "health_max",
        "energy", "energy_max", "attack_min", "attack_max", "defence_min",
        "defence_max", "moves", "skills", "weapon", "tactics", "loot",
        "money_min", "money_max", "exploration_reward", "status",
    ):
        assert "self.{} =".format(field_name) in instance
    assert "self.data" not in instance
    assert "def get(" not in instance
    assert "def __getitem__" not in instance
    assert "def __setitem__" not in instance
    assert 'target["health"]' not in runtime
    assert 'enemy["status"]' not in runtime
    assert 'enemy.get("health"' not in runtime


def test_v68_migration_consumes_in_progress_enemy_data_maps_once():
    migration = source("game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V68():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 82" in migration
    assert "if loaded_version < 69:" in migration
    assert "updateSave_V68()" in migration
    assert 'legacy_data = getattr(old_enemy, "data", None)' in block
    assert "converted = FightEnemyInstance(fight_enemy_template(enemy_id)" in block
    assert "fight.enemy_party = converted_party" in block
