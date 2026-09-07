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


def test_forest_departure_uses_horse_authority_then_calendar_hour():
    source = (PROJECT_ROOT / "game" / "Forest" / "Forest.rpy").read_text(encoding="utf-8-sig")
    departure_block = source.split("def forest_can_depart_now():", 1)[1].split("def forest_departure_block_text():", 1)[0]

    assert "calendar_v2.sync_state()" not in departure_block
    assert "if forest_has_horse():" in departure_block
    assert "return True" in departure_block.split("if forest_has_horse():", 1)[1].split("try:", 1)[0]
    assert "int(calendar_v2.hour or 0) < 12" in departure_block
    assert "int(time or 0)" not in departure_block


def test_forest_horse_access_does_not_duplicate_clara_event_probability():
    forest = (PROJECT_ROOT / "game" / "Forest" / "Forest.rpy").read_text(encoding="utf-8-sig")
    runtime = (
        PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
    ).read_text(encoding="utf-8-sig")
    forest_thread = runtime.split('LThreadData(1, "clara", "ForestSofa"', 1)[1].split(
        'LThreadData(2, "clara", "TavernVisit"', 1
    )[0]
    first_event = forest_thread.split('"story_clara_forest_follow_0"', 1)[1].split(
        '"story_clara_forest_horse_prank_1"', 1
    )[0]

    departure_block = forest.split("def forest_can_depart_now():", 1)[1].split(
        "def forest_departure_block_text():", 1
    )[0]
    assert "player.horse.owns_horse()" not in departure_block
    assert "forest_has_horse()" in departure_block
    assert "[1, 2, 3, 4, 5, 6], (12, 19), None" in first_event
    assert "\n            1,\n" in first_event


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
