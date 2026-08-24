from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_game_item_reuses_canonical_game_object_behavior():
    source = (ROOT / "game/Items/Core/GameItem.rpy").read_text(encoding="utf-8-sig")
    assert "class GameItem(GameObject):" in source
    for duplicate_method in (
        "def is_visible(",
        "def is_locked(",
        "def visible_actions(",
        "def visible_contents(",
        "def has_contents(",
        "def __getstate__(",
        "def __setstate__(",
    ):
        assert duplicate_method not in source
    assert "def __reduce__(self):" in source
    assert "super(GameItem, self).__init__(*args, **kwargs)" in source
    assert "game_item_registry[self.object_id] = self" in source
