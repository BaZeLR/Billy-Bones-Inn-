from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGHT = ROOT / "game" / "Utilities" / "Fight" / "FightSystemRuntime.rpy"
FIGHT_SCREEN = ROOT / "game" / "Utilities" / "Fight" / "FightScreen.rpy"
LAYOUT = ROOT / "game" / "Utilities" / "General" / "Screens" / "main_layout.rpy"
DEBUG_TOOLS = ROOT / "game" / "Utilities" / "General" / "Common" / "DebugTools.rpy"
PLAYER = ROOT / "game" / "Utilities" / "General" / "Player" / "Player.rpy"
AXE = ROOT / "game" / "Items" / "Resources" / "OldAxeItem.rpy"
ATTIC_ITEMS = ROOT / "game" / "Items" / "Crafting" / "SoapCraftAndAtticItems.rpy"
CLICK_RUNNER = ROOT / "tools" / "external_click_play_test.py"


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def test_fight_has_attack_defence_speed_mana_and_party_totals():
    source = _source(FIGHT)
    player = _source(PLAYER)

    assert "class FightInfo(object):" in source
    assert "class HuntInfo(object):" in source
    assert "class FightEnemyInstance(object):" in source
    assert "default Fight = None" in source
    assert "default Hunt = None" in source
    assert "default PlayerFightMana = 50" not in source
    assert "def fight_player_mana_modifier():" in source
    assert "def fight_player_speed_points():" in source
    assert "def fight_enemy_speed_points(enemy=None):" in source
    assert "def fight_party_totals(side=\"player\"):" in source
    assert "FIGHT_COMPANION_BONUSES = {" in source
    assert "aggressiveness" in source
    assert "self.mana = 50" in player
    assert 'g["PlayerFightMana"]' not in player


def test_fight_uses_hunt_images_and_varied_loot_tables():
    source = _source(FIGHT)

    for image_path in (
        "images/hunt/lonely_wolf_attack.png",
        "images/hunt/boars.png",
        "images/hunt/bear.png",
        "images/hunt/bear_2.png",
        "images/fight/thug.png",
        "images/fight/thief.png",
        "images/fight/patrol_guard.png",
        "images/fight/default_enemy.png",
    ):
        assert image_path in source
        assert (ROOT / "game" / image_path).is_file()

    assert '"wolf_skin_001": (1, 1)' in source
    assert '"boar_meat_001": (1, 3)' in source
    assert '"bear_claw_001": (1, 2)' in source
    assert "def fight_roll_loot_quantity(raw_qty):" in source


def test_fight_outcome_popup_and_ui_show_combat_stats():
    source = _source(FIGHT)
    screen = _source(FIGHT_SCREEN)
    layout = _source(LAYOUT)

    assert 'default FightOutcomePopup = {"active": 0' not in source
    assert "def fight_set_outcome_popup" in source
    assert 'fight_set_outcome_popup("victory", "Победа"' in source
    assert 'fight_set_outcome_popup("defeat", "Поражение"' in source
    assert "screen fight_outcome_popup():" in screen
    assert "use fight_outcome_popup()" in screen
    assert 'id "fight_outcome_continue"' in screen
    assert "fight_selected_enemy_image()" in screen
    assert "screen fight_outcome_popup():" not in layout
    assert "screen main_ui_fight_panel():" not in layout
    assert "use main_ui_fight_panel()" in layout
    assert "return str(scene_image or _layout_last_picture or \"\")" not in source
    assert "$ _fight_text = str(MainTxt or fight_preview_text() or \"\")" in screen
    assert "Атака:" in screen
    assert "Скорость:" in screen
    assert "Оружие:" in screen
    assert "Тактика:" in screen
    assert "Навыки:" in screen
    assert "scrollbars \"vertical\"" in screen


def test_fight_flow_has_no_refresh_preview_or_store_bloat():
    source = _source(FIGHT)

    assert "fight_refresh_ui_actions" not in source
    assert "show_fight_preview_main_ui" not in source
    assert "renpy.store" not in source
    assert "globals()" not in source
    for removed_name in (
        "FightLoadedAmmo",
        "FightTargetIndex",
        "FightVictoryLoot",
        "FightLevel",
        "company_list",
        "PlayerFightSupply",
        "FightWeaponLoaded",
        "FightRetreatUsed",
        "FightEnemyState",
        "HuntUnlocked",
        "HuntLastResult",
        "FightSideLog",
        "FightEnemyParty",
        "FightEnemyId",
        "FightReturnRoomCode",
        "FightReturnPicture",
        "FightStatusState",
        "PlayerFightMana",
        "FightOutcomePopup",
        "ForestTrapState",
        "ForestTrapRooms",
        "fight_publish_state",
    ):
        assert removed_name not in source
    assert "$ current_action_items = fight_action_items()" in source


def test_fight_click_runner_uses_current_fight_object_state():
    runner = _source(CLICK_RUNNER)

    assert "FightEnemyParty" not in runner
    assert "FightEnemyId" not in runner
    assert "FightWeaponLoaded" not in runner
    assert "FightLoadedAmmo" not in runner
    assert "PlayerFightSupply" not in runner
    assert "fight_info().enemy_party" in runner
    assert "fight_info().enemy_id" in runner


def test_fight_has_explicit_flow_labels_and_escape_actions():
    source = _source(FIGHT)
    screen = _source(FIGHT_SCREEN)

    assert "label FightStart(" in source
    assert "$ Fight.begin(" not in source
    assert "$ fight_info().begin(enemy_id, enemy_count, CurLoc, \"images/forest/forest_1.png\")" in source
    assert "label FightStartHuntCurrentRoom:" in source
    assert "label FightDoAction(action_code=\"\"):" in source
    assert "label FightEnd:" in source
    assert "Call(\"FightEnd\")" in source
    assert "Call(\"FightEnd\")" in screen
    assert "Скрыться" in source
    assert "Попытаться сбежать" in source
    assert "fight_enemy_move_resolution(enemy, defence_mode)" in source
    assert "fight_apply_enemy_phase(\"normal\")" in source


def test_debug_builder_can_launch_real_fight_cases():
    source = _source(DEBUG_TOOLS)

    assert 'MenuItem("Fight test room", Jump("DebugBuilderFightTests"))' in source
    assert "label DebugBuilderFightTests:" in source
    assert "label DebugFightStreetCrooks:" in source
    assert "label DebugFightRandomForestHunt:" in source
    assert 'MenuItem("Street crooks", Jump("DebugFightStreetCrooks"))' in source
    assert 'MenuItem("Patrol guards", Jump("DebugFightPatrolGuards"))' in source
    assert 'Jump("DebugBuilderStartFight"' not in source
    assert 'fight_begin("street_crook", 2, "DebugBuilderFightTests"' in source
    assert 'fight_begin("patrol_guard", 2, "DebugBuilderFightTests"' in source
    assert 'fight_begin(_debug_hunt_enemy_id, _debug_hunt_enemy_count, "DebugBuilderFightTests"' in source
    assert "call screen main_ui" in source
    for enemy_id in (
        "wolf",
        "white_wolf",
        "boar",
        "brown_bear",
        "giant_grizzly",
        "street_crook",
        "street_thief",
        "patrol_guard",
    ):
        assert enemy_id in source


def test_equipment_has_attack_defence_speed_modifiers():
    axe = _source(AXE)
    attic = _source(ATTIC_ITEMS)

    assert '"attack_points": 10' in axe
    assert '"speed_penalty": 1' in axe
    assert '"attack_points": 14' in attic
    assert '"speed_penalty": 2' in attic
    assert '"defence_points": 8' in attic
    assert '"speed_penalty": 3' in attic
    assert '"fight_speed_boost": 4' in attic
