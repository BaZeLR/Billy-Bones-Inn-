import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_story_condition_scope_is_explicit_and_has_no_global_dump():
    source = (ROOT / "game/Utilities/General/Events/conditions.rpy").read_text(encoding="utf-8-sig")
    scope = source.split("def _story_condition_scope():", 1)[1].split("def _story_relationship_level", 1)[0]
    assert "globals()" not in scope
    assert "dict(globals())" not in source
    for required in (
        '"player": player',
        '"calendar_v2": calendar_v2',
        '"event_runtime": event_runtime',
        '"threads": threads',
        '"current_game_day": current_game_day',
        '"effective_player_exploration": effective_player_exploration',
        '"people": people',
        '"werecat_state": werecat_state',
    ):
        assert required in scope
    assert "church_after_cermon_event_roll" not in scope
    assert "amanda_tavern_seduction_ready" not in scope
    assert "tavern_amanda_bed_action_available" not in scope
    assert "Unknown story condition name" in source


def test_thread_conditions_use_event_runtime_owner():
    source = (ROOT / "game/Utilities/General/Events/conditions.rpy").read_text(encoding="utf-8-sig")
    assert "self.event_runtime" not in source
    assert "event_runtime.active_thread" in source


def test_every_story_condition_name_exists_in_the_explicit_scope():
    conditions = (ROOT / "game/Utilities/General/Events/conditions.rpy").read_text(encoding="utf-8-sig")
    runtime = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    scope_block = conditions.split("def _story_condition_scope():", 1)[1].split("def _story_relationship_level", 1)[0]
    scope_names = set(re.findall(r'^\s+"([A-Za-z_]\w*)"\s*:', scope_block, re.MULTILINE))

    unknown = []
    for line_number, line in enumerate(runtime.splitlines(), 1):
        for raw in re.findall(r'"(#(?:\\.|[^"\\])*)"', line):
            expression = json.loads('"' + raw + '"')[1:].strip()
            tree = ast.parse(expression, mode="eval")
            names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
            missing = sorted(names - scope_names)
            if missing:
                unknown.append((line_number, missing, expression))

    assert unknown == []
