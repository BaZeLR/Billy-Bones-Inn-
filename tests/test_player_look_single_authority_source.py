from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_player_look_is_derived_from_appearance_without_saved_stat_mirror():
    player = (ROOT / "game/Utilities/General/Player/Player.rpy").read_text(encoding="utf-8-sig")
    stat = (ROOT / "game/Utilities/General/Screens/stat.rpy").read_text(encoding="utf-8-sig")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig") for path in (ROOT / "game").rglob("*.rpy")
    )

    stats_block = player.split("class PlayerStats(object):", 1)[1].split(
        "class PlayerEconomy(object):", 1
    )[0]
    assert "self.look" not in stats_block
    assert ".stats.look" not in game_sources
    assert "def player_look_breakdown():" in stat
    assert 'player_look_breakdown().get("look", 0)' in game_sources


def test_soap_appearance_bonus_has_one_player_owned_state():
    player = (ROOT / "game/Utilities/General/Player/Player.rpy").read_text(encoding="utf-8-sig")
    crafting = (ROOT / "game/Items/Crafting/SoapCraftAndAtticItems.rpy").read_text(encoding="utf-8-sig")
    backyard = (ROOT / "game/Inn/Backyard.rpy").read_text(encoding="utf-8-sig")
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert "self.soap_look_bonus = 0" in player
    assert "self.soap_look_bonus_until_day = -1" in player
    assert "def wash_with_soap(" in player
    assert "self.soap_look_bonus_until_day" not in crafting
    assert "crafting.soap_look_bonus_until_day" not in crafting
    assert "player.change_stat(\"look\"" not in backyard
    assert "player.appearance.wash_with_soap(" in backyard
    assert "def updateSave_V19():" in migration
    assert 'stats_state.pop("look", None)' in migration
