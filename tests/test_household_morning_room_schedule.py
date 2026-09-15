import json
import textwrap
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
PRIVATE_ROOMS = {
    "amanda": "TavernAmandaRoom",
    "melissa": "TavernMelissaRoom",
    "sandra": "TavernSandraRoom",
}


def read(relative):
    return (GAME / relative).read_text(encoding="utf-8-sig")


def schedule(npc_id):
    return json.loads(read("NPC/Schedules/%s.json" % npc_id))["entries"]


def method_source(source, name):
    start = source.index("        def %s(" % name)
    tail = source[start + 1 :]
    stop = tail.find("\n        def ")
    end = len(source) if stop < 0 else start + 1 + stop
    return textwrap.dedent(source[start:end])


def _morning_namespace(day=42, weekday=7, hour=8, minute=0):
    source = read("Inn/menu_tavernstat.rpy")
    block = source.split("    def _household_morning_state_key", 1)[1].split(
        "    def household_needs_reconcile", 1
    )[0]
    code = textwrap.dedent("    def _household_morning_state_key" + block)
    calendar = SimpleNamespace(week=weekday, hour=hour, minute=minute)

    def clock_minutes(time_value=None):
        if time_value is None:
            return calendar.hour * 60 + calendar.minute
        value = int(time_value or 0)
        return value * 60 if 0 <= value <= 23 else value % 1440

    namespace = {
        "Amanda": SimpleNamespace(var={}),
        "calendar_v2": calendar,
        "current_game_day": lambda: day,
        "household": SimpleNamespace(morning_state={}),
        "npc_schedule_clock_minute": clock_minutes,
        "procedural_randint": lambda low, high, key="": high,
        "_tavern_int": lambda value, default=0: int(value),
        "_tavern_person_corruption": lambda person: 0,
        "_tavern_person_relation": lambda person: 0,
    }
    exec(code, namespace)
    return namespace


def _runtime_registry(morning_namespace):
    source = read("Utilities/General/NPC/PeopleRuntime.rpy")
    schedule_block = source.split("    def npc_schedule_clock_minute", 1)[1].split(
        "    def npc_daily_schedule_interval", 1
    )[0]

    def condition_true(condition):
        if condition is None:
            return True
        if condition.get("rule") != "household_morning_issue":
            return True
        return morning_namespace["household_morning_issue_matches"](
            condition.get("person", ""), condition.get("issue", "")
        )

    runtime = {
        "calendar_v2": morning_namespace["calendar_v2"],
        "room_rule_true": condition_true,
        "procedural_randint": lambda low, high, key="": low,
    }
    exec(textwrap.dedent("    def npc_schedule_clock_minute" + schedule_block), runtime)

    class ScheduledPerson:
        def __init__(self, name, entries):
            self.name = name
            self.entries = entries

        def schedule_entry(self, weekday_value=None, time_value=None):
            for entry in sorted(self.entries, key=lambda row: row.priority, reverse=True):
                if entry.matches(weekday_value, time_value):
                    return entry
            return None

        def getLocation(self, weekday_value=None, time_value=None):
            entry = self.schedule_entry(weekday_value, time_value)
            return "" if entry is None else entry.selected_location()

        def display_name(self):
            return self.name

    people = {}
    for person in PRIVATE_ROOMS:
        rows = {row["label"]: row for row in schedule(person)}
        entries = []
        for label in ("morning_sick", "morning_sleepy"):
            row = rows[label]
            entries.append(runtime["NPCHourScheduleEntry"](
                npc_id=person,
                location=row["location"],
                weekdays=row["weekdays"],
                start=row["start"],
                end=row["end"],
                awake=row["awake"],
                talkable=row["talkable"],
                condition=row["condition"],
                priority=row["priority"],
                label=row["label"],
            ))
        entries.append(runtime["NPCHourScheduleEntry"](
            npc_id=person,
            location="TavernKitchen",
            weekdays=[1, 2, 3, 4, 5, 6, 7],
            start="06:00",
            end="20:30",
            awake=True,
            talkable=True,
            working=True,
            priority=620,
            label="ordinary_job",
        ))
        people[person] = ScheduledPerson(person, entries)

    class Registry:
        def get_info(self, person):
            return people.get(person)

        def items(self):
            return sorted(people.items())

    for name in ("location", "ids_at", "schedule_entry", "is_awake", "can_talk"):
        method_namespace = {}
        exec(method_source(source, name), method_namespace)
        setattr(Registry, name, method_namespace[name])
    return Registry()


def test_unresolved_sick_or_sleepy_state_matches_exact_morning_hours_on_every_weekday():
    for weekday in range(1, 8):
        for person in PRIVATE_ROOMS:
            for issue in ("sick", "sleepy"):
                namespace = _morning_namespace(weekday=weekday)
                state = namespace["household"].morning_state
                state["%s:42" % person] = {"issue": issue, "resolved": 0, "indecent": 0}
                matches = namespace["household_morning_issue_matches"]

                assert matches(person, issue, 6)
                assert matches(person, issue, 11 * 60 + 59)
                assert not matches(person, issue, 12)


def test_clearing_a_morning_issue_immediately_releases_its_schedule_condition():
    namespace = _morning_namespace(hour=10)
    state = namespace["household"].morning_state
    state["melissa:42"] = {"issue": "sleepy", "resolved": 0, "indecent": 1}

    assert namespace["household_morning_issue_matches"]("melissa", "sleepy")
    assert namespace["household_clear_morning_issue"]("melissa") == 1
    assert not namespace["household_morning_issue_matches"]("melissa", "sleepy")


def test_people_registry_projects_issue_room_awake_state_and_release_at_runtime():
    namespace = _morning_namespace(weekday=6, hour=8)
    state = namespace["household"].morning_state
    state["amanda:42"] = {"issue": "sick", "resolved": 0, "indecent": 0}
    state["melissa:42"] = {"issue": "sleepy", "resolved": 0, "indecent": 0}
    registry = _runtime_registry(namespace)

    assert registry.location("amanda", 6, 8) == "TavernAmandaRoom"
    assert registry.location("melissa", 6, 11 * 60 + 59) == "TavernMelissaRoom"
    assert registry.ids_at("TavernAmandaRoom", 6, 8) == ["amanda"]
    assert registry.ids_at("TavernMelissaRoom", 6, 8) == ["melissa"]
    assert registry.is_awake("amanda", 6, 8) is True
    assert registry.is_awake("melissa", 6, 8) is False
    assert registry.can_talk("amanda", 6, 8) is False
    assert registry.can_talk("melissa", 6, 8) is False

    assert namespace["household_clear_morning_issue"]("melissa") == 1
    assert registry.location("melissa", 6, 10) == "TavernKitchen"
    assert registry.can_talk("melissa", 6, 10) is True
    assert registry.location("amanda", 6, 12) == "TavernKitchen"


def test_new_day_preparation_is_idempotent_and_save_patch_prepares_old_saves():
    namespace = _morning_namespace()
    state = namespace["household"].morning_state
    state["amanda:42"] = {"issue": "sick", "resolved": 0, "indecent": 0}
    namespace["prepare_household_morning_states"](42)

    assert state["amanda:42"]["issue"] == "sick"
    assert {"sandra:42", "melissa:42", "amanda:42"}.issubset(state)

    new_day = read("Utilities/Time/NextDay_NewDayEvents.rpy")
    assert new_day.index("prepare_household_morning_states(day_value)") < new_day.index(
        'people.location("georgett"'
    )

    save_patch = read("TractirSaveSync.rpy").split(
        "def tractir_save_patch_loaded_state():", 1
    )[1]
    assert save_patch.index("household.repair()") < save_patch.index(
        "prepare_household_morning_states(current_game_day())"
    )


def test_private_room_rows_override_jobs_church_and_barber_without_new_location_state():
    for person, private_room in PRIVATE_ROOMS.items():
        rows = {row["label"]: row for row in schedule(person)}
        sick = rows["morning_sick"]
        sleepy = rows["morning_sleepy"]

        for row, issue, awake in ((sick, "sick", True), (sleepy, "sleepy", False)):
            assert row["weekdays"] == [1, 2, 3, 4, 5, 6, 7]
            assert row["start"] == "06:00"
            assert row["end"] == "11:59"
            assert row["location"] == private_room
            assert row["awake"] is awake
            assert row["talkable"] is False
            assert row["priority"] == 950
            assert row["condition"] == {
                "rule": "household_morning_issue",
                "person": person,
                "issue": issue,
            }

        assert max(row.get("priority", 0) for label, row in rows.items() if not label.startswith("morning_")) < 950

    rules = read("Utilities/General/Classes/GameObjectTemplate.rpy")
    assert 'if rule_name == "household_morning_issue":' in rules
    assert "household_morning_issue_matches(person, issue)" in rules

    people = read("Utilities/General/NPC/PeopleRuntime.rpy")
    girl_location = people.split("class Girl(BaseNPC):", 1)[1].split(
        "def tavern_service_target", 1
    )[0]
    assert "not household_morning_issue_matches(self.name, time_value=hour)" in girl_location
    assert girl_location.index("household_morning_issue_matches") < girl_location.index(
        "barber_shop_is_open_at"
    )
    assert "priority=770 if target == \"gloryhole\" else 760" in people


def test_schedule_predicate_is_read_only_and_has_no_private_room_mirror():
    source = read("Inn/menu_tavernstat.rpy")
    predicate = source.split("def household_morning_issue_matches", 1)[1].split(
        "def household_morning_issue_type", 1
    )[0]

    assert "household.morning_state.get" in predicate
    assert "household.morning_state[" not in predicate
    assert "_ensure_household_morning_state" not in predicate
    assert "_tavern_private_room" not in source
