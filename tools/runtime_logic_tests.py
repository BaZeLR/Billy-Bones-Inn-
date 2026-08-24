#!/usr/bin/env python3
"""Static runtime-logic checks kept outside the Ren'Py game tree.

This script is intentionally pure Python. It does not import Ren'Py and it does
not add labels, screens, or developer UI to the shipped game.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CORE_PEOPLE = ("amanda", "melissa", "sandra", "clara")
THREAD_LIST_NAMES = (
    "amandaThreadList",
    "melissaThreadList",
    "sandraThreadList",
    "claraThreadList",
    "beckyThreadList",
    "eddieThreadList",
    "irmaThreadList",
    "lizaThreadList",
    "georgettThreadList",
    "churchThreadList",
    "mongolThreadList",
    "cityGuardThreadList",
    "sherwoodThreadList",
    "cityThreadList",
)
KNOWN_NON_ITEM_RECIPE_KEYS = {
    "ash_barrel_ready",
    "flavor_mix",
    "flower_mix",
    "soap_container",
}
THREAD_RUNTIME_STATE_ASSIGN_RE = re.compile(
    r"\b(?:thread|tinfo|_clara_booklet_thread|_melissa_bat_thread|threads\[[^\]]+\])"
    r"\.(?:done|num|completed|aborted|metconds|blocks|blocked)\s*=(?!=)"
)
CALL_HYPERLINK_RE = re.compile(r"\{a=call:([^}]+)\}")


@dataclass
class CheckRow:
    status: str
    area: str
    detail: str


@dataclass
class StoryEvent:
    list_name: str
    thread: str
    constructor: str
    target: str
    day: object
    hour: object
    evt_day: object
    probability: object
    reqs: object
    cond: object
    location: str
    action: str
    item: str
    priority: int
    raw_len: int


@dataclass
class StoryThread:
    list_name: str
    constructor: str
    level: object
    person: str
    subname: str
    name: str
    cond: object
    events: list[StoryEvent]


class RuntimeLogicReport:
    def __init__(self) -> None:
        self.rows: list[CheckRow] = []

    def add(self, status: str, area: str, detail: str) -> None:
        self.rows.append(CheckRow(status, area, detail))

    def pass_(self, area: str, detail: str) -> None:
        self.add("pass", area, detail)

    def warn(self, area: str, detail: str) -> None:
        self.add("warn", area, detail)

    def fail(self, area: str, detail: str) -> None:
        self.add("fail", area, detail)

    @property
    def failures(self) -> list[CheckRow]:
        return [row for row in self.rows if row.status == "fail"]

    @property
    def warnings(self) -> list[CheckRow]:
        return [row for row in self.rows if row.status == "warn"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def iter_rpy_files(game_dir: Path) -> list[Path]:
    return sorted(path for path in game_dir.rglob("*.rpy") if path.is_file())


def collect_labels(game_dir: Path) -> set[str]:
    label_re = re.compile(r"^\s*label\s+([A-Za-z_]\w*)\b", re.MULTILINE)
    labels: set[str] = set()
    for path in iter_rpy_files(game_dir):
        labels.update(label_re.findall(read_text(path)))
    return labels


def extract_balanced_assignment(source: str, name: str) -> str:
    marker = re.search(r"(?m)^\s*define\s+%s\s*=\s*" % re.escape(name), source)
    if not marker:
        return ""
    start = marker.end()
    while start < len(source) and source[start].isspace():
        start += 1
    if start >= len(source):
        return ""

    opening = source[start]
    pairs = {"[": "]", "{": "}", "(": ")"}
    if opening not in pairs:
        end = source.find("\n", start)
        return source[start:] if end < 0 else source[start:end]

    closing = pairs[opening]
    depth = 0
    quote: str | None = None
    escape = False
    for index in range(start, len(source)):
        ch = source[index]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            continue
        if ch == opening:
            depth += 1
        elif ch == closing:
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    return ""


def ast_const(node: ast.AST, default=None):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        value = ast_const(node.operand, default)
        if isinstance(value, (int, float)):
            return -value
    return default


def ast_literal(node: ast.AST, default=None):
    try:
        return ast.literal_eval(node)
    except Exception:
        return ast_const(node, default)


def ast_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return ""


def is_event_tuple(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Tuple)
        and len(node.elts) >= 11
        and isinstance(ast_const(node.elts[0]), str)
    )


def event_from_tuple(node: ast.Tuple, list_name: str, thread_name: str, constructor: str) -> StoryEvent:
    target = str(ast_const(node.elts[0], "") or "")
    day = ast_literal(node.elts[1], None)
    hour = ast_literal(node.elts[2], None)
    evt_day = ast_literal(node.elts[3], None)
    probability = ast_literal(node.elts[4], None)
    reqs = ast_literal(node.elts[5], None)
    cond = ast_literal(node.elts[6], None)
    item = ast_const(node.elts[7], "")
    location = ast_const(node.elts[8], "")
    action = ast_const(node.elts[9], "")
    priority = ast_const(node.elts[10], 0)
    return StoryEvent(
        list_name=list_name,
        thread=thread_name,
        constructor=constructor,
        target=target,
        day=day,
        hour=hour,
        evt_day=evt_day,
        probability=probability,
        reqs=reqs,
        cond=cond,
        location=str(location or ""),
        action=str(action or ""),
        item=str(item or ""),
        priority=int(priority or 0),
        raw_len=len(node.elts),
    )


def collect_event_tuples(node: ast.AST, list_name: str, thread_name: str, constructor: str) -> list[StoryEvent]:
    events: list[StoryEvent] = []
    if is_event_tuple(node):
        events.append(event_from_tuple(node, list_name, thread_name, constructor))
        return events
    for child in ast.iter_child_nodes(node):
        events.extend(collect_event_tuples(child, list_name, thread_name, constructor))
    return events


def parse_story_threads(
    source: str,
    report: RuntimeLogicReport,
    named_event_objects: set[str] | None = None,
) -> list[StoryThread]:
    threads: list[StoryThread] = []
    named_event_objects = named_event_objects or set()
    for list_name in THREAD_LIST_NAMES:
        expr = extract_balanced_assignment(source, list_name)
        if not expr:
            report.warn("threads", f"{list_name} was not found")
            continue
        try:
            parsed = ast.parse(f"_value = {expr}", mode="exec")
        except SyntaxError as exc:
            report.fail("threads", f"{list_name} cannot be parsed: {exc}")
            continue

        list_events = 0
        for call in [node for node in ast.walk(parsed) if isinstance(node, ast.Call)]:
            func_name = ast_name(call.func)
            if func_name not in ("LThreadData", "RThreadData", "UThreadData"):
                continue
            if len(call.args) < 5:
                report.fail("threads", f"{list_name} contains malformed {func_name}")
                continue
            level = ast_literal(call.args[0], None)
            person = str(ast_const(call.args[1], "") or "")
            subname = str(ast_const(call.args[2], "") or "")
            cond = ast_literal(call.args[3], None)
            thread_name = person + subname
            thread_events = collect_event_tuples(call.args[4], list_name, thread_name, func_name)
            named_events = {
                node.id
                for node in ast.walk(call.args[4])
                if isinstance(node, ast.Name) and node.id in named_event_objects
            }
            if not thread_events:
                generated_events = [
                    node for node in ast.walk(call.args[4])
                    if isinstance(node, ast.Call) and ast_name(node.func).endswith("_event")
                ]
                if not generated_events and not named_events:
                    report.fail("threads", f"{thread_name} has no event definitions")
            list_events += len(thread_events) + len(named_events)
            threads.append(
                StoryThread(
                    list_name=list_name,
                    constructor=func_name,
                    level=level,
                    person=person,
                    subname=subname,
                    name=thread_name,
                    cond=cond,
                    events=thread_events,
                )
            )
        report.pass_("threads", f"{list_name}: {list_events} event definitions")
    return threads


def event_type_name(event: StoryEvent) -> str:
    return f"{event.thread}->{event.target}"


def validate_thread_blueprints(threads: list[StoryThread], report: RuntimeLogicReport) -> None:
    seen_names: dict[str, str] = {}
    levels_by_person: dict[str, set[int]] = {}
    for story_thread in threads:
        if not isinstance(story_thread.level, int):
            report.fail("thread_schema", f"{story_thread.name}: level must be an int")
        else:
            levels_by_person.setdefault(story_thread.person, set()).add(story_thread.level)
        if not story_thread.person:
            report.fail("thread_schema", f"{story_thread.name}: person is empty")
        if not story_thread.subname:
            report.fail("thread_schema", f"{story_thread.name}: subname is empty")
        expected_name = story_thread.person + story_thread.subname
        if story_thread.name != expected_name:
            report.fail("thread_schema", f"{story_thread.name}: name does not match person + subname")
        if story_thread.name in seen_names:
            report.fail(
                "thread_schema",
                f"{story_thread.name}: duplicate thread name in {seen_names[story_thread.name]} and {story_thread.list_name}",
            )
        seen_names[story_thread.name] = story_thread.list_name
        if story_thread.constructor not in ("LThreadData", "RThreadData", "UThreadData"):
            report.fail("thread_schema", f"{story_thread.name}: unknown thread constructor {story_thread.constructor}")

    for person in CORE_PEOPLE:
        if person not in levels_by_person:
            report.warn("thread_schema", f"{person} has no parsed story thread blueprint")
            continue
        if 0 not in levels_by_person[person]:
            report.warn("thread_schema", f"{person} has no level 0 entry thread")
    report.pass_("thread_schema", f"validated {len(threads)} thread blueprints")


def valid_time_spec(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, int):
        return True
    if isinstance(value, (tuple, list, set)):
        return all(isinstance(item, int) for item in value)
    return False


def valid_probability(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, (int, float)):
        return 0 <= float(value) <= 1
    return False


def valid_reqs(value: object) -> bool:
    if value is None:
        return True
    if not isinstance(value, dict):
        return False
    return all(isinstance(key, str) and isinstance(limit, int) for key, limit in value.items())


def validate_event_schema(events: list[StoryEvent], report: RuntimeLogicReport) -> None:
    for event in events:
        name = event_type_name(event)
        if event.raw_len != 11:
            report.fail("event_schema", f"{name}: event tuple has {event.raw_len} fields, expected exactly 11")
        if not event.target:
            report.fail("event_schema", f"{name}: empty target label")
        if not valid_time_spec(event.day):
            report.fail("event_schema", f"{name}: day spec is not int/list/tuple/set/None")
        if not valid_time_spec(event.hour):
            report.fail("event_schema", f"{name}: hour spec is not int/list/tuple/set/None")
        if not (event.evt_day is None or isinstance(event.evt_day, (int, str, tuple, list))):
            report.fail("event_schema", f"{name}: evtDay spec is not supported")
        if not valid_probability(event.probability):
            report.fail("event_schema", f"{name}: probability must be numeric 0..1 or None")
        if not valid_reqs(event.reqs):
            report.fail("event_schema", f"{name}: reqs must be a dict of stat names to integer limits or None")
        if event.item and not isinstance(event.item, str):
            report.fail("event_schema", f"{name}: item id must be a string")
        if not isinstance(event.location, str):
            report.fail("event_schema", f"{name}: location must be a string")
        if not isinstance(event.action, str):
            report.fail("event_schema", f"{name}: action must be a string")
        if not isinstance(event.priority, int):
            report.fail("event_schema", f"{name}: priority must be an int")
    report.pass_("event_schema", f"validated {len(events)} event tuple field sets")


def check_event_audit_methods(project_root: Path, report: RuntimeLogicReport) -> None:
    events_path = project_root / "game" / "Utilities" / "General" / "Events" / "events.rpy"
    threads_path = project_root / "game" / "Utilities" / "General" / "Events" / "threads.rpy"
    board_path = project_root / "game" / "Utilities" / "General" / "Screens" / "StoryThreadBoard.rpy"
    story_source = ""
    for path in (events_path, threads_path):
        if path.exists():
            story_source += "\n" + read_text(path)
    board_source = read_text(board_path) if board_path.exists() else ""
    required_runtime_tokens = (
        "def auditChecks",
        "def canTrigger",
        "def checkBlocks",
        '"target"',
        '"binding"',
        '"day"',
        '"hour"',
        '"delay"',
        '"requirements"',
        '"conditions"',
        '"item"',
        '"location_open"',
        '"probability"',
    )
    for token in required_runtime_tokens:
        if token not in story_source:
            report.fail("event_audit", f"split story runtime missing audit token: {token}")
    required_board_tokens = (
        "def story_board_condition_lines",
        "rows.append(str(cond.show()).replace(\"[\", \"[[\"))",
        "for _cond_line in story_board_condition_lines(tinfo.data.conds):",
        "for _cond_line in story_board_condition_lines(evt.conds):",
        'text "Conditions:"',
    )
    for token in required_board_tokens:
        if token not in board_source:
            report.fail("event_audit", f"StoryThreadBoard missing audit token: {token}")
    forbidden_board_tokens = (
        "def story_board_show_event_checks",
        "story_board_show_event_checks(evt, tinfo)",
        'text "Checks: "',
    )
    for token in forbidden_board_tokens:
        if token in board_source:
            report.fail("event_audit", f"StoryThreadBoard keeps old confusing audit display token: {token}")
    report.pass_("event_audit", "event audit methods remain runtime-only; board uses FamilyLife condition rows")


def extract_python_assignment(source: str, name: str) -> str:
    marker = re.search(r"(?m)^\s*%s\s*=\s*" % re.escape(name), source)
    if not marker:
        return ""
    start = marker.end()
    while start < len(source) and source[start].isspace():
        start += 1
    return extract_balanced_literal_from(source, start)


def extract_balanced_literal_from(source: str, start: int) -> str:
    if start >= len(source):
        return ""
    opening = source[start]
    pairs = {"[": "]", "{": "}", "(": ")"}
    if opening not in pairs:
        return ""
    closing = pairs[opening]
    depth = 0
    quote: str | None = None
    escape = False
    for index in range(start, len(source)):
        ch = source[index]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            continue
        if ch == opening:
            depth += 1
        elif ch == closing:
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    return ""


def check_thread_events(project_root: Path, report: RuntimeLogicReport) -> None:
    story_path = project_root / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
    if not story_path.exists():
        report.fail("threads", "StoryEventRuntime.rpy is missing")
        return
    source = read_text(story_path)
    game_dir = project_root / "game"
    labels = collect_labels(game_dir)
    named_event_re = re.compile(
        r"(?m)^\s*([A-Za-z_]\w*)\s*=\s*[A-Za-z_]\w*Event\s*\("
    )
    named_event_objects: set[str] = set()
    for path in iter_rpy_files(game_dir):
        named_event_objects.update(named_event_re.findall(read_text(path)))
    threads = parse_story_threads(source, report, named_event_objects)
    validate_thread_blueprints(threads, report)
    events = [event for story_thread in threads for event in story_thread.events]
    if not events:
        report.fail("events", "no story events parsed")
        return
    validate_event_schema(events, report)
    check_event_audit_methods(project_root, report)

    missing_labels = [event for event in events if event.target not in labels]
    for event in missing_labels:
        report.fail("events", f"{event.thread}: missing label {event.target}")

    unbound = [event for event in events if not event.location or not event.action]
    for event in unbound:
        report.warn("events", f"{event.thread}/{event.target}: empty location/action binding")

    priority_slots: dict[tuple[str, str, int], list[str]] = {}
    for event in events:
        if event.location and event.action:
            priority_slots.setdefault((event.location, event.action, event.priority), []).append(
                f"{event.thread}->{event.target}"
            )
    for (location, action, priority), rows in sorted(priority_slots.items()):
        if len(rows) > 1:
            report.warn(
                "priority",
                f"{location}/{action} priority {priority} has {len(rows)} competing events: {', '.join(rows[:4])}",
            )

    report.pass_("events", f"checked {len(events)} story event definitions")


def check_social_topics(project_root: Path, report: RuntimeLogicReport) -> None:
    path = project_root / "game" / "Utilities" / "General" / "NPC" / "SocialTalkTopics.rpy"
    if not path.exists():
        report.fail("social", "SocialTalkTopics.rpy is missing")
        return
    source = read_text(path)
    expr = extract_python_assignment(source, "SOCIAL_TALK_PROFILES")
    if not expr:
        report.fail("social", "SOCIAL_TALK_PROFILES assignment was not found")
        return
    try:
        profiles = ast.literal_eval(expr)
    except Exception as exc:
        report.fail("social", f"SOCIAL_TALK_PROFILES cannot be parsed: {exc}")
        return
    for person in CORE_PEOPLE:
        if person not in profiles:
            report.fail("social", f"{person} has no talk profile")
            continue
        row = profiles.get(person, {})
        for mode in ("talk", "flirt"):
            mode_scores = row.get(mode, {})
            if not isinstance(mode_scores, dict) or not mode_scores:
                report.fail("social", f"{person} has no {mode} scores")
                continue
            for topic, value in mode_scores.items():
                if not isinstance(value, int):
                    report.fail("social", f"{person}/{mode}/{topic} score is not int")
                elif value < -5 or value > 5:
                    report.fail("social", f"{person}/{mode}/{topic} score {value} outside -5..+5")
    report.pass_("social", "core talk/flirt topic scores are present and bounded")


def collect_game_item_ids(project_root: Path) -> set[str]:
    item_ids: set[str] = set()
    for path in iter_rpy_files(project_root / "game"):
        source = read_text(path)
        item_ids.update(re.findall(r"object_id\s*=\s*['\"]([^'\"]+)['\"]", source))
    return item_ids


def collect_recipe_item_refs(project_root: Path) -> tuple[set[str], set[str]]:
    recipe_sources = []
    for path in (
        project_root / "game" / "Items" / "Core" / "CraftingRecipes.rpy",
        project_root / "game" / "Items" / "Crafting" / "SoapCraftAndAtticItems.rpy",
    ):
        if path.exists():
            recipe_sources.append(read_text(path))
    source = "\n".join(recipe_sources)
    result_ids = set(re.findall(r"item_result\s*=\s*['\"]([^'\"]+)['\"]", source))
    quoted_item_ids = set(re.findall(r"['\"]([a-zA-Z0-9_]+_001)['\"]", source))
    return result_ids, quoted_item_ids


def check_recipe_items(project_root: Path, report: RuntimeLogicReport) -> None:
    crafting_path = project_root / "game" / "Items" / "Core" / "CraftingRecipes.rpy"
    table_path = project_root / "game" / "Inn" / "TavernMyRoom.rpy"
    if not crafting_path.exists():
        report.fail("recipes", "CraftingRecipes.rpy is missing")
        return
    crafting_source = read_text(crafting_path)
    table_source = read_text(table_path) if table_path.exists() else ""

    for token in (
        "find_unmarked_numbers",
        "recipe_book_bat_thread_started",
        "recipe_missing_requirement_indexes",
        "recipe_missing_requirement_rows",
        "craftable_recipe_pages",
        "RecipeBookCraftMenu",
        "apply_recipe_craft",
        "player.add_item",
    ):
        if token not in crafting_source:
            report.fail("recipes", f"{token} is missing from CraftingRecipes.rpy")

    if "for _recipe_id in list(craftable_recipe_pages() or [])" not in table_source:
        report.fail("recipes", "TavernMyRoomTableCraftMenu does not use craftable_recipe_pages()")
    if "Посмотреть: " in table_source:
        report.fail("recipes", "TavernMyRoomTableCraftMenu still lists unavailable recipes as view rows")

    item_ids = collect_game_item_ids(project_root)
    result_ids, referenced_item_ids = collect_recipe_item_refs(project_root)
    for item_id in sorted(result_ids):
        if item_id not in item_ids:
            report.fail("recipes", f"recipe result {item_id} is not registered as a GameItem")
    for item_id in sorted(referenced_item_ids):
        if item_id in KNOWN_NON_ITEM_RECIPE_KEYS:
            continue
        if item_id not in item_ids:
            report.fail("recipes", f"recipe references unregistered item id {item_id}")

    report.pass_("recipes", f"checked {len(result_ids)} recipe outputs against {len(item_ids)} game item ids")


def check_required_hooks(project_root: Path, report: RuntimeLogicReport) -> None:
    checks = {
        "projection": (
            project_root / "game" / "Utilities" / "General" / "Events" / "events.rpy",
            ("event_runtime.projection_rows", "event_runtime.route_hints", "story_event_projection_rows", "story_event_path_targets"),
        ),
        "player_condition": (
            project_root / "game" / "Utilities" / "General" / "Screens" / "stat.rpy",
            ("player_social_condition_modifier", "player_social_adjusted_delta", "player_social_condition_notify"),
        ),
        "narrator": (
            project_root / "game" / "Utilities" / "General" / "Common" / "NarratorRuntime.rpy",
            ("image side tractir_narrator", "define n", "tractir_narrate"),
        ),
        "board": (
            project_root / "game" / "Utilities" / "General" / "Screens" / "StoryThreadBoard.rpy",
            (
                "STORY_BOARD_COLORS",
                "story_board_event_status",
                "screen story_thread_screen",
                "screen story_event_screen",
                "story_board_show_target(evt.target)",
                "story_board_show_location(tinfo.data.person, evt.location, evt.action)",
                "story_board_show_item(evt.item)",
                "story_board_show_min_date(evt.evtDay, tinfo.day)",
                "story_board_show_day(evt.day)",
                "story_board_show_hour(evt.hour)",
                "story_board_show_stats(evt.reqs)",
                "story_board_condition_lines(evt.conds)",
                "done",
                "available",
                "waiting",
                "future",
                "blocked",
                "aborted",
            ),
        ),
        "progress": (
            project_root / "game" / "Utilities" / "General" / "Common" / "AchievementsEndings.rpy",
            (
                "class TractirProgressRuntimeState",
                "tractir_progress.activated_achievements",
                "tractir_progress.achieved",
                "tractir_progress.endings",
                "tractir_achievement_order",
                "tractir_achievements",
                "tractir_ending_desc",
                "tractir_check_achievements_apply",
                "tractir_first_active_ending",
                "tractir_mark_maid_revenge_ready",
                "tractir_mark_boss_fatal_loss",
                "tractir_apply_sandra_secured_future",
                "label TractirCheckAchievements",
                "label TractirShowPendingAchievements",
                "label TractirShowEnding",
                "label TractirCheckEndings",
                "screen tractir_progress_panel",
            ),
        ),
        "town_random": (
            project_root / "game" / "Town" / "RandomTownEvents.rpy",
            (
                "class TownStreetRuntime",
                "TownStreet.events_today",
                "TownStreetPatrolEvent",
                "TownStreetThugsEvent",
                "TownStreetHelpEvent",
                "TownRandomChronicleEvent",
                "patrol_allowed",
                "TownStreetPatrolHide",
                "TownStreetPatrolBribe",
            ),
        ),
    }
    for area, (path, tokens) in checks.items():
        if not path.exists():
            report.fail(area, f"{path.relative_to(project_root)} is missing")
            continue
        source = read_text(path)
        for token in tokens:
            if token not in source:
                report.fail(area, f"{token} is missing from {path.relative_to(project_root)}")
        report.pass_(area, f"{path.relative_to(project_root)} hook file checked")

    narrator_image = project_root / "game" / "images" / "general" / "narrator.png"
    if narrator_image.exists():
        report.pass_("narrator", "images/general/narrator.png exists")
    else:
        report.fail("narrator", "images/general/narrator.png is missing")


def check_thread_runtime_api_usage(project_root: Path, report: RuntimeLogicReport) -> None:
    bypasses = []
    for path in iter_rpy_files(project_root / "game"):
        source = read_text(path)
        for match in THREAD_RUNTIME_STATE_ASSIGN_RE.finditer(source):
            line_no = source.count("\n", 0, match.start()) + 1
            bypasses.append(f"{path.relative_to(project_root)}:{line_no}")
    for row in bypasses:
        report.fail("thread_api", f"direct ThreadInfo state assignment: {row}")
    if not bypasses:
        report.pass_("thread_api", "gameplay code uses ThreadInfo methods for runtime state changes")


def check_call_hyperlinks(project_root: Path, report: RuntimeLogicReport) -> None:
    labels = collect_labels(project_root / "game")
    checked = 0
    for path in iter_rpy_files(project_root / "game"):
        source = read_text(path)
        for match in CALL_HYPERLINK_RE.finditer(source):
            checked += 1
            target = match.group(1).strip()
            line_no = source.count("\n", 0, match.start()) + 1
            location = f"{path.relative_to(project_root)}:{line_no}"
            if not re.match(r"^[A-Za-z_]\w*$", target):
                report.fail("hyperlink", f"call hyperlink target is not a plain label at {location}: {target}")
                continue
            if target not in labels:
                report.fail("hyperlink", f"call hyperlink target label is missing at {location}: {target}")
    report.pass_("hyperlink", f"checked {checked} call hyperlinks")


def check_room_enter_gates(project_root: Path, report: RuntimeLogicReport) -> None:
    checks = {
        "TavernMelissaRoom": project_root / "game" / "Inn" / "TavernMelissaRoom.rpy",
    }
    for label, path in checks.items():
        if not path.exists():
            report.fail("room_enter", f"{path.relative_to(project_root)} is missing")
            continue
        source = read_text(path)
        if f"label {label}:" not in source:
            report.fail("room_enter", f"{label} label is missing")
        if "call RoomEnterEventGate(rooms.current_code, False)" not in source:
            report.fail("room_enter", f"{label} does not call RoomEnterEventGate")
    report.pass_("room_enter", f"checked {len(checks)} room enter gates")


def check_random_helpers(project_root: Path, report: RuntimeLogicReport) -> None:
    path = project_root / "game" / "script.rpy"
    if not path.exists():
        report.fail("random_helpers", "script.rpy is missing")
        return
    source = read_text(path)
    for token in (
        "def procedural_seed(",
        "def procedural_index(",
        "def procedural_choice(",
        "def procedural_randint(",
    ):
        if token not in source:
            report.fail("random_helpers", f"{token} is missing from script.rpy")
    if "renpy.random.choices" in source:
        report.fail("random_helpers", "script.rpy uses renpy.random.choices instead of local helper selection")
    direct_random_re = re.compile(r"renpy\.random\.(?:randint|choice|uniform|random)\(")
    direct_random_rows: list[str] = []
    for other_path in iter_rpy_files(project_root / "game"):
        if other_path == path:
            continue
        other_source = read_text(other_path)
        for match in direct_random_re.finditer(other_source):
            line_no = other_source.count("\n", 0, match.start()) + 1
            direct_random_rows.append(f"{other_path.relative_to(project_root)}:{line_no}")
    if direct_random_rows:
        report.warn(
            "random_helpers",
            f"{len(direct_random_rows)} direct renpy.random calls remain outside script helpers; first: {direct_random_rows[0]}",
        )
    report.pass_("random_helpers", "script.rpy procedural random helper API is present")


def run_checks(project_root: Path) -> RuntimeLogicReport:
    report = RuntimeLogicReport()
    check_thread_events(project_root, report)
    check_social_topics(project_root, report)
    check_recipe_items(project_root, report)
    check_required_hooks(project_root, report)
    check_thread_runtime_api_usage(project_root, report)
    check_call_hyperlinks(project_root, report)
    check_room_enter_gates(project_root, report)
    check_random_helpers(project_root, report)
    return report


def print_report(report: RuntimeLogicReport) -> None:
    for row in report.rows:
        print(f"{row.status.upper():5} {row.area:16} {row.detail}")
    print()
    print(f"Summary: {len(report.failures)} failures, {len(report.warnings)} warnings, {len(report.rows)} checks")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".", help="Path to Tractir project root")
    args = parser.parse_args(argv)
    project_root = Path(args.project_root).resolve()
    report = run_checks(project_root)
    print_report(report)
    return 1 if report.failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
