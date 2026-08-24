from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy"


class CalendarStub:
    def __init__(self, hour=0, minute=0):
        self.hour = hour
        self.minute = minute
        self.daysInGame = 1

    def clock_minutes(self):
        return self.hour * 60 + self.minute


def _schedule_namespace(hour=0, minute=0):
    source = RUNTIME.read_text(encoding="utf-8-sig")
    block = source.split("    def npc_schedule_clock_minute", 1)[1].split(
        "    def npc_daily_schedule_interval", 1
    )[0]
    code = textwrap.dedent("    def npc_schedule_clock_minute" + block)
    namespace = {
        "calendar_v2": CalendarStub(hour, minute),
        "week": 1,
        "room_rule_true": lambda condition: True,
        "procedural_randint": lambda low, high, key="": low,
    }
    exec(code, namespace)
    return namespace


def test_overnight_clock_interval_matches_23_through_05_only():
    namespace = _schedule_namespace()
    entry = namespace["NPCScheduleEntry"](
        location="Room",
        weekdays=[1],
        start_hour=23,
        end_hour=6,
    )

    for hour in (23, 0, 1, 2, 3, 4, 5):
        assert entry.matches(1, hour)
    assert not entry.matches(1, 6)


def test_json_half_hour_boundaries_are_compared_at_minute_precision():
    namespace = _schedule_namespace(20, 30)
    entry = namespace["NPCHourScheduleEntry"](
        npc_id="amanda",
        location="TavernMain",
        weekdays=[1],
        start="12:00",
        end="20:30",
    )

    assert entry.matches(1, None)
    namespace["calendar_v2"].minute = 31
    assert not entry.matches(1, None)


def test_explicit_schedule_queries_accept_hours_and_minute_of_day():
    namespace = _schedule_namespace()
    entry = namespace["NPCScheduleEntry"](
        location="PortStreets",
        weekdays=[1],
        start_hour=19,
        end_hour=23,
    )

    assert entry.matches(1, 19)
    assert entry.matches(1, 19 * 60)
    assert not entry.matches(1, 12)
