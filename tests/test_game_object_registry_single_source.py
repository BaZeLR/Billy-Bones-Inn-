from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_game_objects_register_at_construction_without_manual_list():
    source = (ROOT / "game/Utilities/General/Classes/GameObjectTemplate.rpy").read_text(encoding="utf-8-sig")
    assert "game_object_registry = {}" in source
    assert "game_object_registry[self.object_id] = self" in source
    assert "dict(game_object_registry or {}).get(object_id" in source
    assert not (ROOT / "game/Utilities/General/Classes/GameObjects.rpy").exists()
