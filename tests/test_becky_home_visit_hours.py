"""Execute the live visit predicate against clock and NPC-presence boundaries."""
import ast
from pathlib import Path
from types import SimpleNamespace
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_function(path, name, namespace):
    source = (ROOT / path).read_text(encoding="utf-8-sig")
    lines = source.splitlines()
    start = next(i for i, line in enumerate(lines) if line.lstrip().startswith(f"def {name}("))
    indent = len(lines[start]) - len(lines[start].lstrip())
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) > indent):
        end += 1
    exec(compile(ast.parse(textwrap.dedent("\n".join(lines[start:end]))), str(path), "exec"), namespace)
    return namespace[name]


@pytest.mark.parametrize("minute,home,expected", [
    (13 * 60, True, False),
    (17 * 60 + 59, True, False),
    (18 * 60, True, True),
    (20 * 60, False, False),
    (22 * 60 + 59, True, True),
    (23 * 60, True, False),
])
def test_regular_visits_use_evening_clock_and_current_npc_schedule(minute, home, expected):
    calendar = SimpleNamespace(week=1, clock_minutes=lambda: minute)
    namespace = {"calendar_v2": calendar}
    predicate = load_function("game/NPC/Girls/Becky/InitBecky.rpy", "is_home_for_evening_visit", namespace)
    becky = SimpleNamespace(
        getLocation=lambda: "BeckyHome" if home else "TavernKitchen",
        schedule_state=lambda: {"awake": minute < 23 * 60},
    )
    assert predicate(becky) is expected


@pytest.mark.parametrize("stage,available,expected", [(1, True, False), (2, True, True), (3, True, True), (3, False, False)])
def test_market_keeps_story_permission_separate_from_npc_presence(stage, available, expected):
    namespace = {
        "calendar_v2": SimpleNamespace(week=1, clock_minutes=lambda: 19 * 60),
        "threads": {"beckyHome": SimpleNamespace(num=stage)},
        "Becky": SimpleNamespace(is_home_for_evening_visit=lambda: available),
    }
    predicate = load_function("game/Town/Market/MarketPlace.rpy", "marketplace_becky_home_visible", namespace)
    assert predicate() is expected


@pytest.mark.parametrize("invited,expected", [(True, True), (False, False)])
def test_friday_escorted_visit_uses_dance_invitation(invited, expected):
    namespace = {
        "calendar_v2": SimpleNamespace(week=5, clock_minutes=lambda: 23 * 60),
        "threads": {"beckyHome": SimpleNamespace(num=0)},
        "rooms": SimpleNamespace(get=lambda code: SimpleNamespace(dance_count=5, becky_home_invited=invited)),
    }
    predicate = load_function("game/Town/Market/MarketPlace.rpy", "marketplace_becky_home_visible", namespace)
    assert predicate() is expected
