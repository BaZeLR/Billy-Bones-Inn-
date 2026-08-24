import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WINESTORE_ROOM = PROJECT_ROOT / "game" / "Town" / "WineStore.rpy"
CLARA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Clara" / "InitClara.rpy"
CLARA_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "clara.json"
ALBER_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "alber.json"
SECONDARY_INIT = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "InitSecondaryNPC.rpy"
ALBER_INIT = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "InitAlber.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def _payload(path):
    return json.loads(_source(path))


def _minutes(text):
    hour, minute = str(text).split(":", 1)
    return int(hour) * 60 + int(minute)


def _entry_matches(entry, weekday, minute):
    if weekday not in entry.get("weekdays", []):
        return False
    start = _minutes(entry.get("start", "00:00"))
    end = _minutes(entry.get("end", "23:59"))
    if start <= end:
        return start <= minute <= end
    return minute >= start or minute <= end


def _location_value(entry):
    location = entry.get("location", "")
    if isinstance(location, list):
        return location
    return [location]


def _wine_matches(path, weekday, clock_text):
    minute = _minutes(clock_text)
    return [
        entry
        for entry in _payload(path)["entries"]
        if "WineStore" in _location_value(entry) and _entry_matches(entry, weekday, minute)
    ]


def test_winestore_room_open_hours_are_clock_based_0600_to_1700_with_friday_1500_close():
    source = _source(WINESTORE_ROOM)
    schedule_block = source.split("schedule=RoomSchedule(", 1)[1].split("custom_properties={", 1)[0]

    assert "def wine_store_open_now():" in source
    assert "if current_week == 5:" in source
    assert "return 6 * 60 <= current_minutes <= 15 * 60" in source
    assert "return 6 * 60 <= current_minutes <= 17 * 60" in source
    assert 'start="06:00"' in schedule_block
    assert 'end="17:00"' in schedule_block
    assert "condition=wine_store_open_now" in schedule_block
    assert "time_slots=" not in schedule_block
    assert "if not _wine_room.is_open():" in source
    assert "_wine_room.is_open(week, time)" not in source


def test_winestore_npc_presence_uses_hour_intervals_not_display_slots():
    clara = _source(CLARA_INIT)
    schedule_runtime = _source(PROJECT_ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy")

    assert "def clara_wine_store_shift_active" not in clara
    assert 'self.schedule_source = "schedules/clara.json"' in clara
    assert "$ npc_interval_schedule_load_all(True)" in schedule_runtime
    assert "npc_interval_schedule_load_file(name)" not in clara
    assert "return time_value in (0, 1)" not in clara

    assert _wine_matches(CLARA_SCHEDULE, 1, "06:00")
    assert _wine_matches(CLARA_SCHEDULE, 1, "08:00")
    assert not _wine_matches(ALBER_SCHEDULE, 1, "08:00")

    assert _wine_matches(CLARA_SCHEDULE, 1, "11:30")
    assert _wine_matches(ALBER_SCHEDULE, 1, "11:30")

    assert not _wine_matches(CLARA_SCHEDULE, 1, "12:00")
    assert _wine_matches(ALBER_SCHEDULE, 1, "12:00")

    assert _wine_matches(ALBER_SCHEDULE, 1, "17:00")
    assert not _wine_matches(ALBER_SCHEDULE, 1, "17:01")

    assert _wine_matches(ALBER_SCHEDULE, 5, "15:00")
    assert not _wine_matches(ALBER_SCHEDULE, 5, "15:01")


def test_alber_portrait_source_is_secondary_npc_not_clara_or_wine_store_duplicate():
    clara = _source(CLARA_INIT)
    wine_store = _source(WINESTORE_ROOM)
    alber = _source(ALBER_INIT)

    assert "def alber_random_portrait():" in alber
    assert "images/Alber/portrait1.png" in alber
    assert "alber_random_portrait()" not in clara
    assert "def alber_stable_portrait" not in wine_store
    assert "alber_random_portrait()" in wine_store
