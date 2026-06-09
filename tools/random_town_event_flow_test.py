#!/usr/bin/env python3
"""Pure Python flow checks for random town events.

This test stays outside the Ren'Py game tree. It reads the real event script,
executes only the init-python runtime class with a small Ren'Py stub, and checks
that the event menu content still points to the intended branches.
"""

from __future__ import annotations

import random
import re
import sys
import textwrap
import types
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_FILE = ROOT / "game" / "Town" / "RandomTownEvents.rpy"


class RandomStub:
    def __init__(self) -> None:
        self.rng = random.Random(7)

    def choice(self, seq):
        return self.rng.choice(list(seq))

    def random(self) -> float:
        return self.rng.random()

    def randint(self, start: int, stop: int) -> int:
        return self.rng.randint(start, stop)


class RenpyStub:
    random = RandomStub()


class StoreModule(types.ModuleType):
    def __init__(self, name: str, namespace: dict):
        super().__init__(name)
        object.__setattr__(self, "_namespace", namespace)

    def __getattr__(self, name: str):
        namespace = object.__getattribute__(self, "_namespace")
        if name in namespace:
            return namespace[name]
        raise AttributeError(name)

    def __setattr__(self, name: str, value):
        if name == "_namespace":
            object.__setattr__(self, name, value)
            return
        namespace = object.__getattribute__(self, "_namespace")
        namespace[name] = value


@dataclass
class MenuRow:
    caption: str
    action: str
    target: str


def fail(message: str) -> None:
    raise AssertionError(message)


def read_source() -> str:
    return EVENT_FILE.read_text(encoding="utf-8-sig")


def extract_init_python(source: str) -> str:
    marker = re.search(r"(?m)^init\s+-20\s+python:\s*$", source)
    if not marker:
        fail("RandomTownEvents.rpy has no init -20 python block")

    tail = source[marker.end() :]
    end = re.search(r"(?m)^label\s+", tail)
    if not end:
        fail("RandomTownEvents.rpy init-python block is not followed by labels")

    block = tail[: end.start()]
    return textwrap.dedent(block)


def extract_label(source: str, label_name: str) -> str:
    marker = re.search(r"(?m)^label\s+%s\b.*:\s*$" % re.escape(label_name), source)
    if not marker:
        fail("Missing label %s" % label_name)

    tail = source[marker.end() :]
    end = re.search(r"(?m)^label\s+", tail)
    return tail if not end else tail[: end.start()]


def menu_rows(label_block: str) -> list[MenuRow]:
    rows: list[MenuRow] = []
    for line in label_block.splitlines():
        if "MenuItem(" not in line:
            continue
        caption_match = re.search(r'MenuItem\("((?:\\"|[^"])*)"', line)
        action_match = re.search(r"\b(Call|Jump|Return)\((?:\"([^\"]+)\"|([A-Za-z_]\w*)|(True|False))", line)
        function_return = re.search(r"\bFunction\(renpy\.return_statement,\s*(True|False)", line)
        if caption_match and function_return:
            rows.append(
                MenuRow(
                    caption=caption_match.group(1),
                    action="Function",
                    target="renpy.return_statement:%s" % function_return.group(1),
                )
            )
        elif caption_match and action_match:
            rows.append(
                MenuRow(
                    caption=caption_match.group(1),
                    action=action_match.group(1),
                    target=action_match.group(2) or action_match.group(3) or action_match.group(4) or "",
                )
            )
    return rows


def assert_menu(label_name: str, expected: list[tuple[str, str, str]]) -> None:
    rows = menu_rows(extract_label(SOURCE, label_name))
    got = [(row.caption, row.action, row.target) for row in rows]
    if got != expected:
        fail("%s menu mismatch\nexpected: %r\nactual:   %r" % (label_name, expected, got))


def assert_contains(label_name: str, fragments: list[str]) -> None:
    block = extract_label(SOURCE, label_name)
    for fragment in fragments:
        if fragment not in block:
            fail("%s does not contain required logic fragment: %s" % (label_name, fragment))


def make_runtime_namespace():
    namespace = {"__builtins__": __builtins__}
    renpy_module = types.ModuleType("renpy")
    renpy_module.random = RandomStub()
    store_module = StoreModule("renpy.store", namespace)
    renpy_module.store = store_module
    namespace["renpy"] = renpy_module

    def procedural_seed(key=""):
        key_text = str(key or "")
        key_total = 0
        for index, char_value in enumerate(key_text):
            key_total += (index + 1) * ord(char_value)
        return (
            int(namespace.get("dayspassed", 0) or 0) * 1009
            + int(namespace.get("day", 0) or 0) * 97
            + int(namespace.get("month", 0) or 0) * 53
            + int(namespace.get("week", 0) or 0) * 31
            + int(namespace.get("time", 0) or 0) * 17
            + key_total
        )

    def procedural_index(count=0, key=""):
        count_value = int(count or 0)
        if count_value <= 0:
            return 0
        return abs(int(procedural_seed(key))) % count_value

    def procedural_randint(a, b=None, key=""):
        if b is None:
            low_value = 0
            high_value = int(a or 0)
        else:
            low_value = int(a or 0)
            high_value = int(b or 0)
        if high_value < low_value:
            low_value, high_value = high_value, low_value
        return low_value + procedural_index(high_value - low_value + 1, key)

    namespace["procedural_randint"] = procedural_randint

    old_renpy = sys.modules.get("renpy")
    old_store = sys.modules.get("renpy.store")
    sys.modules["renpy"] = renpy_module
    sys.modules["renpy.store"] = store_module
    try:
        exec(extract_init_python(SOURCE), namespace)
    finally:
        if old_renpy is None:
            sys.modules.pop("renpy", None)
        else:
            sys.modules["renpy"] = old_renpy
        if old_store is None:
            sys.modules.pop("renpy.store", None)
        else:
            sys.modules["renpy.store"] = old_store
    return namespace


def test_chronicle_content(namespace) -> None:
    town = namespace["town_street"]
    for slot in ("morning", "noon", "weekends", "evening", "night"):
        entries = town.TIME_EVENTS.get(slot)
        if not entries or len(entries) < 6:
            fail("%s chronicle slot must keep the six-row snippet structure" % slot)
        for entry in entries:
            if not isinstance(entry, dict):
                fail("%s chronicle row must be structured dict data" % slot)
            if not entry.get("text") or not entry.get("hooks"):
                fail("%s chronicle row must expose text and hooks" % slot)

    all_text = "\n".join(entry["text"] for entries in town.TIME_EVENTS.values() for entry in entries)
    all_text_lower = all_text.lower()
    for fragment in (
        "награда 100 золотых",
        "налог на грех",
        "Комендантский час после заката",
        "капитана Циммера",
        "черный пес",
    ):
        if fragment.lower() not in all_text_lower and fragment.lower() not in SOURCE.lower():
            fail("snippet content fragment is missing: %s" % fragment)


def test_gender_bound_chronicles(namespace) -> None:
    town = namespace["town_street"]
    female_markers = ("голая по пояс [имя]", "Молодая [имя]")
    male_markers = (
        "наткнулся",
        "орет он",
        "толстый [имя]",
        "перед женой",
        "закидывают его",
        "шепчет он",
        "крутит партнершу",
        "Хозяин [имя]",
        "смеется он",
        "штаны спущены",
    )
    for slot, entries in town.TIME_EVENTS.items():
        for entry in entries:
            text = str(entry.get("text", ""))
            gender = str(entry.get("gender", ""))
            if any(marker in text for marker in female_markers) and gender != "female":
                fail("%s chronicle row with female grammar lacks female gender lock: %s" % (slot, text))
            if any(marker in text for marker in male_markers) and gender != "male":
                fail("%s chronicle row with male grammar lacks male gender lock: %s" % (slot, text))

    male_jobs = set(town.OCCUPATIONS["male"])
    female_jobs = set(town.OCCUPATIONS["female"])
    if male_jobs.intersection(female_jobs):
        fail("town occupation pools must not mix male/female forms")
    if town._call_occupation("male") not in male_jobs:
        fail("male occupation call returned a non-male form")
    if town._call_occupation("female") not in female_jobs:
        fail("female occupation call returned a non-female form")


def set_store(namespace, **values) -> None:
    namespace.update(values)


def find_allowed_clock(namespace, method_name: str, location: str, start_minute: int = 0, end_minute: int = 1439) -> int:
    town = namespace["town_street"]
    for minute_value in range(start_minute, end_minute + 1):
        namespace["clock_minutes"] = minute_value
        namespace["hour"] = minute_value // 60
        namespace["minute"] = minute_value % 60
        namespace["TownStreetStorySeenKeys"] = []
        namespace["TownStreetFiredLabelsToday"] = []
        namespace["TownStreetFiredLocationsToday"] = []
        if getattr(town, method_name)(location):
            return minute_value
    fail("%s did not allow %s in requested minute range" % (method_name, location))


def simulate_event_entry(namespace, location: str, label: str = "", patrol: bool = False, fight: bool = False) -> None:
    namespace["TownStreetEventsToday"] = int(namespace.get("TownStreetEventsToday", 0) or 0) + 1
    if patrol:
        namespace["TownStreetPatrolsToday"] = int(namespace.get("TownStreetPatrolsToday", 0) or 0) + 1
    if fight:
        namespace["TownStreetFightToday"] = int(namespace.get("TownStreetFightToday", 0) or 0) + 1
    namespace["town_street"].mark_seen(location, label)


def test_probability_contract(namespace) -> None:
    set_store(namespace, dayspassed=2, day=3, month=1, week=2, time=4, clock_minutes=22 * 60, notoriety=60)
    town = namespace["town_street"]
    plan = town.ensure_daily_plan()
    expected = {
        "beggar": 10,
        "thugs": 10,
        "patrol": 55,
        "patrol_base": 25,
        "patrol_notoriety_bonus": 30,
        "chronicle": 25,
        "chronicle_cooldown_days": 3,
    }
    if plan != expected:
        fail("town probability contract mismatch\nexpected: %r\nactual:   %r" % (expected, plan))
    if not town.curfew_active():
        fail("22:00 must be curfew")
    namespace["clock_minutes"] = 21 * 60 + 29
    if town.curfew_active():
        fail("21:29 must not be curfew")
    namespace["clock_minutes"] = 21 * 60 + 30
    if not town.curfew_active():
        fail("21:30 must be curfew")
    namespace["clock_minutes"] = 5 * 60 + 30
    if not town.curfew_active():
        fail("05:30 must still be curfew")
    namespace["clock_minutes"] = 5 * 60 + 31
    if town.curfew_active():
        fail("05:31 must not be curfew")
    set_store(namespace, hour=8, minute=0, clock_minutes=22 * 60, CurLoc="StreetTavern", TownStreetEventsToday=0, TownStreetStorySeenKeys=[], TownStreetFiredLabelsToday=[], TownStreetFiredLocationsToday=[], GuardCaptainVar={})
    if town.curfew_active():
        fail("visible 08:00 must not be curfew even if clock_minutes is stale")
    if town.patrol_allowed("StreetTavern"):
        fail("patrol must not be allowed at visible 08:00")


def test_patrol_hide(namespace) -> None:
    set_store(
        namespace,
        CurLoc="StreetTavern",
        time=4,
        clock_minutes=22 * 60,
        week=2,
        dayspassed=5,
        day=6,
        month=1,
        exploration=300,
        notoriety=60,
        money=500,
        tavernfame=10,
        TownStreetEventsToday=0,
        TownStreetPatrolsToday=0,
        TownStreetFightToday=0,
        TownCurfewCaughtToday=0,
        TownStreetStorySeenKeys=[],
        GuardCaptainVar={},
    )
    town = namespace["town_street"]
    find_allowed_clock(namespace, "patrol_allowed", "StreetTavern", 21 * 60 + 30, 23 * 60)
    if not town.patrol_allowed("StreetTavern"):
        fail("patrol event is not ready for deterministic night StreetTavern setup")

    simulate_event_entry(namespace, "StreetTavern", "TownStreetPatrolEvent", patrol=True)
    if not town.escape_success(115):
        fail("patrol hide branch should succeed with 300 exploration")
    namespace["exploration"] += 8

    if namespace["TownStreetEventsToday"] != 1:
        fail("patrol entry did not consume one daily town event")
    if namespace["TownStreetPatrolsToday"] != 1:
        fail("patrol entry did not count one patrol")
    if namespace["exploration"] < 308:
        fail("patrol hide did not award exploration")
    if not town.random_seen_this_slot("StreetTavern"):
        fail("patrol entry did not mark the current location/time as seen")


def test_help_recruit(namespace) -> None:
    set_store(
        namespace,
        CurLoc="MarketPlace",
        time=0,
        clock_minutes=8 * 60,
        week=3,
        dayspassed=0,
        day=1,
        month=1,
        exploration=100,
        notoriety=0,
        tavernfame=0,
        TownStreetEventsToday=0,
        TownStreetPatrolsToday=0,
        TownStreetFightToday=0,
        TownCurfewCaughtToday=0,
        TownStreetStorySeenKeys=[],
        TavernBlackworkerCandidates=[],
        TavernBlackworkers=[],
        TownStreetContext={},
    )
    town = namespace["town_street"]
    find_allowed_clock(namespace, "help_allowed", "MarketPlace", 6 * 60, 23 * 60)
    if not town.help_allowed("MarketPlace"):
        fail("help event is not ready for deterministic MarketPlace setup")

    simulate_event_entry(namespace, "MarketPlace", "TownStreetHelpEvent")
    town.make_help_context()
    namespace["TavernBlackworkerCandidates"].append(
        {
            "id": "bw_001",
            "name": namespace["TownStreetContext"].get("help_name", "бродяга"),
            "origin": "street_help",
            "day": int(namespace["dayspassed"] or 0),
            "sleep_place": "TavernStable",
            "trust": 0,
        }
    )
    namespace["exploration"] += 5
    namespace["tavernfame"] += 1

    if len(namespace["TavernBlackworkerCandidates"]) != 1:
        fail("help recruit did not create a blackworker candidate")
    if namespace["tavernfame"] != 1 or namespace["exploration"] != 105:
        fail("help recruit did not apply fame/exploration rewards")


def test_thugs_shout(namespace) -> None:
    set_store(
        namespace,
        CurLoc="ArtisansQuarter",
        time=3,
        clock_minutes=18 * 60,
        week=4,
        dayspassed=1,
        day=2,
        month=1,
        exploration=300,
        notoriety=0,
        TownStreetEventsToday=0,
        TownStreetPatrolsToday=0,
        TownStreetFightToday=0,
        TownCurfewCaughtToday=0,
        TownStreetStorySeenKeys=[],
    )
    town = namespace["town_street"]
    find_allowed_clock(namespace, "thug_allowed", "ArtisansQuarter", 6 * 60, 23 * 60)
    if not town.thug_allowed("ArtisansQuarter"):
        fail("thug event is not ready for deterministic ArtisansQuarter setup")

    simulate_event_entry(namespace, "ArtisansQuarter", "TownStreetThugsEvent", fight=True)
    if not town.escape_success(85):
        fail("thug shout branch should succeed with 300 exploration")
    namespace["exploration"] += 6

    if namespace["TownStreetEventsToday"] != 1 or namespace["TownStreetFightToday"] != 1:
        fail("thug entry did not consume event/fight counters")
    if namespace["exploration"] < 306 or namespace["notoriety"] != 0:
        fail("thug shout did not keep notoriety limited to fights/lewd events")


def main() -> int:
    assert_menu(
        "TownStreetPatrolEvent",
        [
            ("Показать пропуск", "Call", "TownStreetPatrolPass"),
            ("Заплатить штраф %d мараведи", "Call", "TownStreetPatrolBribe"),
            ("Спрятаться и уйти дворами", "Call", "TownStreetPatrolHide"),
            ("Бежать", "Call", "TownStreetPatrolRun"),
            ("Драться со стражей", "Call", "TownStreetPatrolFight"),
        ],
    )
    assert_menu(
        "TownStreetHelpEvent",
        [
            ("Дать еды и предложить грязную работу при трактире", "Call", "TownStreetHelpRecruit"),
            ("Дать пару мараведи", "Call", "TownStreetHelpMoney"),
            ("Пройти мимо", "Function", "renpy.return_statement:True"),
        ],
    )
    assert_menu(
        "TownStreetThugsEvent",
        [
            ("Вмешаться и драться", "Call", "TownStreetThugsFight"),
            ("Попробовать спугнуть их криком", "Call", "TownStreetThugsShout"),
            ("Пройти мимо", "Function", "renpy.return_statement:True"),
        ],
    )

    assert_contains("TownStreetPatrolHide", ["exploration += 8", "current_action_items = [MenuItem(\"Идти дальше\", Function(renpy.return_statement, True))]"])
    assert_contains("TownStreetHelpRecruit", ["TavernBlackworkerCandidates.append", "exploration += 5", "tavernfame += 1"])
    assert_contains("TownStreetThugsShout", ["exploration += 6", "current_action_items = [MenuItem(\"Идти дальше\", Function(renpy.return_statement, True))]"])

    namespace = make_runtime_namespace()
    test_chronicle_content(namespace)
    test_gender_bound_chronicles(namespace)
    test_probability_contract(namespace)
    test_patrol_hide(namespace)
    test_help_recruit(namespace)
    test_thugs_shout(namespace)

    print("random town event flow: chronicle content, 3 menus, and 3 action-result branches passed")
    return 0


if __name__ == "__main__":
    SOURCE = read_source()
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print("random town event flow failed: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
