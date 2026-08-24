import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"


def read_game_file(relative_path):
    return (GAME_ROOT / relative_path).read_text(encoding="utf-8-sig")


def has_default(source, name):
    return re.search(rf"(?m)^\s*default\s+{re.escape(name)}\s*=", source) is not None


def test_dance_sponsor_is_initialized_by_tavern_owner():
    player_source = read_game_file("Utilities/General/Player/Player.rpy")
    breakfast_source = read_game_file("Inn/TavernKitchenBreakfast.rpy")
    script = read_game_file("script.rpy")

    assert "self.dance_sponsor = 0" in player_source
    assert "self.dance_sponsor_announced_day = -1" in player_source
    assert "player.tavern_management.breakfast.dance_sponsor_announced_day" in breakfast_source
    assert "player.tavern_management.dance_sponsor_announced_day" not in breakfast_source
    assert not has_default(script, "DanceSponsor")
