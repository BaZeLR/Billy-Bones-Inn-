import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_ROOT = PROJECT_ROOT / "game"


def read_game_file(relative_path):
    return (GAME_ROOT / relative_path).read_text(encoding="utf-8-sig")


def has_default(source, name):
    return re.search(rf"(?m)^\s*default\s+{re.escape(name)}\s*=", source) is not None


def test_dance_sponsor_has_early_script_default():
    script = read_game_file("script.rpy")

    assert has_default(script, "DanceSponsor")
