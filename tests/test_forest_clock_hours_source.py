from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_forest_dusk_uses_clock_minutes_not_time_slot():
    source = (PROJECT_ROOT / "game" / "Forest" / "Forest.rpy").read_text(encoding="utf-8-sig")

    dusk_block = source.split("def forest_after_dusk():", 1)[1].split("def forest_open_hours_visible():", 1)[0]
    assert "current_minutes = int(clock_minutes or 0) % 1440" in dusk_block
    assert "return current_minutes >= ((19 * 60) + 30)" in dusk_block
    assert "int(time or 0) >= 3" not in dusk_block
    assert "int(hour or 0) >= 18" not in dusk_block


def test_forest_rooms_use_clock_open_hours_not_slots():
    forest_files = [
        "Forest.rpy",
        "ForestWaterfall.rpy",
        "ForestDarkWoods.rpy",
        "ForestSpring.rpy",
        "ForestLake.rpy",
        "ForestClearing.rpy",
        "ForestHiddenPath.rpy",
        "ForestCave.rpy",
    ]

    for filename in forest_files:
        source = (PROJECT_ROOT / "game" / "Forest" / filename).read_text(encoding="utf-8-sig")
        assert "time_slots=[0, 1, 2, 3, 4]" not in source
        assert 'start="06:00", end="19:29"' in source
