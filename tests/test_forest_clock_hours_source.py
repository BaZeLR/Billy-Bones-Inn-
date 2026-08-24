from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_forest_dusk_uses_calendar_hour_minute_not_time_slot():
    source = (PROJECT_ROOT / "game" / "Forest" / "Forest.rpy").read_text(encoding="utf-8-sig")

    dusk_block = source.split("def forest_after_dusk():", 1)[1].split("def forest_open_hours_visible():", 1)[0]
    assert "calendar_v2.sync_state()" not in dusk_block
    assert "current_hour = int(calendar_v2.hour or 0) % 24" in dusk_block
    assert "current_minute = int(calendar_v2.minute or 0) % 60" in dusk_block
    assert "return current_hour > 19 or (current_hour == 19 and current_minute >= 30)" in dusk_block
    assert "clock_minutes" not in dusk_block
    assert "int(time or 0) >= 3" not in dusk_block
    assert "int(hour or 0) >= 18" not in dusk_block


def test_forest_departure_uses_calendar_hour_not_display_slot():
    source = (PROJECT_ROOT / "game" / "Forest" / "Forest.rpy").read_text(encoding="utf-8-sig")
    departure_block = source.split("def forest_can_depart_now():", 1)[1].split("def forest_departure_block_text():", 1)[0]

    assert "calendar_v2.sync_state()" not in departure_block
    assert "int(calendar_v2.hour or 0) < 12" in departure_block
    assert "int(time or 0)" not in departure_block


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


def test_forest_cave_night_picture_uses_canonical_dusk_clock():
    source = (PROJECT_ROOT / "game" / "Forest" / "ForestCave.rpy").read_text(encoding="utf-8-sig")
    picture_block = source.split("def forest_cave_picture():", 1)[1].split("ForestCaveRoomDefinition = Room(", 1)[0]
    assert "forest_after_dusk()" in picture_block
    assert "calendar_v2.time_slot()" not in picture_block
