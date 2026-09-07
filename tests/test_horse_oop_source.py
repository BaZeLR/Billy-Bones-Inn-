from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"


def all_rpy_source():
    return "\n".join(path.read_text(encoding="utf-8-sig") for path in GAME.rglob("*.rpy"))


def test_horse_has_one_player_owned_authority_without_legacy_scalars():
    player_source = (GAME / "Utilities/General/Player/Player.rpy").read_text(encoding="utf-8-sig")
    source = all_rpy_source()
    assert "class PlayerHorse(object):" in player_source
    assert "self.horse = PlayerHorse()" in player_source
    assert "self.stolen_purchase_price = 0" in player_source
    assert "def mark_stolen(self, days=14):" in player_source
    for legacy_name in ("MyStallion", "HorseSaddled", "HorsePurchasePrice"):
        assert legacy_name not in source


def test_stable_has_no_builder_restore_or_object_selection_mirror():
    source = (GAME / "Inn/TavernStable.rpy").read_text(encoding="utf-8-sig")
    assert "def tavern_stable_action_items():" in source
    assert "label TavernStableBuildActions:" not in source
    assert "label TavernStableRestore:" not in source
    assert "tavern_stable_object_menu_id" not in source
    assert "while _stable_ui_return is None:" not in source


def test_stable_theft_event_uses_real_night_clock_not_display_slot():
    source = (GAME / "Inn/TavernStable.rpy").read_text(encoding="utf-8-sig")
    assert source.count("calendar_v2.is_between_clock(23, 0, 5, 59)") == 2
    assert "calendar_v2.time_slot()" not in source


def test_horse_consumers_use_player_horse_owner():
    for relative in (
        "Inn/TavernStable.rpy", "Utilities/Fight/FightSystemRuntime.rpy",
        "Utilities/Time/TimeTurnSystem.rpy", "Utilities/Time/NextDay_TavernDaily.rpy",
        "Utilities/Time/NextDay_NewDayEvents.rpy", "NPC/Secondary/IntMongolTalk.rpy",
        "NPC/Secondary/SherwoodTravel.rpy", "NPC/Girls/Clara/InitClara.rpy",
        "NPC/Secondary/IntZimmerTalk.rpy",
        "Forest/Forest.rpy", "Utilities/General/Screens/stat.rpy",
    ):
        assert "player.horse" in (GAME / relative).read_text(encoding="utf-8-sig")


def test_horse_theft_preserves_the_paid_price_for_story_restitution():
    daily = (GAME / "Utilities/Time/NextDay_TavernDaily.rpy").read_text(encoding="utf-8-sig")
    clara_story = (GAME / "NPC/Girls/Clara/ClaraForestSofaThread.rpy").read_text(encoding="utf-8-sig")

    assert "player.horse.mark_stolen(14)" in daily
    assert "player.horse.remove()\n                player.horse.stolen_days = 14" not in daily
    assert "player.horse.stolen_purchase_price" in clara_story
    assert "// 2" in clara_story
