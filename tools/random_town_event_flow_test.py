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
        action_match = re.search(r"\b(Call|Jump)\((?:\"([^\"]+)\"|([A-Za-z_]\w*))", line)
        if caption_match and action_match:
            rows.append(
                MenuRow(
                    caption=caption_match.group(1),
                    action=action_match.group(1),
                    target=action_match.group(2) or action_match.group(3) or "",
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
    namespace = {
        "renpy": RenpyStub(),
        "__builtins__": __builtins__,
    }
    exec(extract_init_python(SOURCE), namespace)
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


def set_store(namespace, **values) -> None:
    namespace.update(values)


def simulate_event_entry(namespace, location: str, patrol: bool = False, fight: bool = False) -> None:
    namespace["TownStreetEventsToday"] = int(namespace.get("TownStreetEventsToday", 0) or 0) + 1
    if patrol:
        namespace["TownStreetPatrolsToday"] = int(namespace.get("TownStreetPatrolsToday", 0) or 0) + 1
    if fight:
        namespace["TownStreetFightToday"] = int(namespace.get("TownStreetFightToday", 0) or 0) + 1
    namespace["town_street"].mark_seen(location)


def test_patrol_hide(namespace) -> None:
    set_store(
        namespace,
        CurLoc="StreetTavern",
        time=4,
        week=2,
        dayspassed=5,
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
    if not town.patrol_allowed("StreetTavern"):
        fail("patrol event is not ready for deterministic night StreetTavern setup")

    simulate_event_entry(namespace, "StreetTavern", patrol=True)
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
        time=1,
        week=3,
        dayspassed=0,
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
    if not town.help_allowed("MarketPlace"):
        fail("help event is not ready for deterministic MarketPlace setup")

    simulate_event_entry(namespace, "MarketPlace")
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
    namespace["notoriety"] += 1

    if len(namespace["TavernBlackworkerCandidates"]) != 1:
        fail("help recruit did not create a blackworker candidate")
    if namespace["tavernfame"] != 1 or namespace["exploration"] != 105:
        fail("help recruit did not apply fame/exploration rewards")


def test_thugs_shout(namespace) -> None:
    set_store(
        namespace,
        CurLoc="ArtisansQuarter",
        time=3,
        week=4,
        dayspassed=1,
        exploration=300,
        notoriety=0,
        TownStreetEventsToday=0,
        TownStreetPatrolsToday=0,
        TownStreetFightToday=0,
        TownCurfewCaughtToday=0,
        TownStreetStorySeenKeys=[],
    )
    town = namespace["town_street"]
    if not town.thug_allowed("ArtisansQuarter"):
        fail("thug event is not ready for deterministic ArtisansQuarter setup")

    simulate_event_entry(namespace, "ArtisansQuarter", fight=True)
    if not town.escape_success(85):
        fail("thug shout branch should succeed with 300 exploration")
    namespace["exploration"] += 6
    namespace["notoriety"] += 2

    if namespace["TownStreetEventsToday"] != 1 or namespace["TownStreetFightToday"] != 1:
        fail("thug entry did not consume event/fight counters")
    if namespace["exploration"] < 306 or namespace["notoriety"] < 2:
        fail("thug shout did not apply exploration/notoriety results")


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
            ("Пройти мимо", "Jump", "CurLoc"),
        ],
    )
    assert_menu(
        "TownStreetThugsEvent",
        [
            ("Вмешаться и драться", "Call", "TownStreetThugsFight"),
            ("Попробовать спугнуть их криком", "Call", "TownStreetThugsShout"),
            ("Пройти мимо", "Jump", "CurLoc"),
        ],
    )

    assert_contains("TownStreetPatrolHide", ["exploration += 8", "current_action_items = [MenuItem(\"Идти дальше\", Jump(CurLoc))]"])
    assert_contains("TownStreetHelpRecruit", ["TavernBlackworkerCandidates.append", "exploration += 5", "tavernfame += 1"])
    assert_contains("TownStreetThugsShout", ["exploration += 6", "notoriety += 2"])

    namespace = make_runtime_namespace()
    test_chronicle_content(namespace)
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
