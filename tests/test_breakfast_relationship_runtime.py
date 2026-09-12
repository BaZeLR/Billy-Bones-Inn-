from pathlib import Path
from types import SimpleNamespace
import textwrap


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Inn/TavernKitchenBreakfast.rpy"


class GirlInfo:
    def __init__(self, relationship):
        self.rel = relationship

    def add_relation(self, amount=1, cap=20):
        self.rel = max(0, min(cap, self.rel + amount))
        return self.rel


def run_breakfast_gain(relationships, caps):
    source = SOURCE.read_text(encoding="utf-8-sig")
    start = source.index("    def tavern_breakfast_apply_social_bonus")
    end = source.index("\n    def tavern_sunday_dinner_dialogue_lines", start)
    function_source = textwrap.dedent(source[start:end])
    infos = {npc_id: GirlInfo(value) for npc_id, value in relationships.items()}
    namespace = {
        "tavern_breakfast_present_ids": lambda: list(relationships.keys()),
        "people": SimpleNamespace(get_info=lambda npc_id: infos.get(npc_id)),
        "relationship_requirement_value": lambda npc_id, _action, _field: caps[npc_id],
    }
    exec(function_source, namespace)
    changed = namespace["tavern_breakfast_apply_social_bonus"]()
    return infos, changed


def test_breakfast_builds_relationship_only_until_each_npcs_flirt_gate():
    infos, changed = run_breakfast_gain(
        {"below": 9, "at": 10, "above": 15},
        {"below": 10, "at": 10, "above": 10},
    )

    assert infos["below"].rel == 10
    assert infos["at"].rel == 10
    assert infos["above"].rel == 15
    assert changed == ["below"]
