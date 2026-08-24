from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game/Utilities/General/NPC/NPCRelationshipLevels.rpy"


def test_relationship_levels_are_derived_without_a_cache_or_sync_layer():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert "default RelationshipLevels" not in source
    assert "sync_npc_relationship_level" not in source
    assert "sync_relationship_levels" not in source
    assert "def npc_relationship_level(npc_id=\"\")" in source
    assert "return build_npc_relationship_level(key)" in source
    assert "after_load_callbacks" not in source
