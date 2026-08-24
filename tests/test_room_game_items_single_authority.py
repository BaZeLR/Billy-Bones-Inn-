from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOM_TEMPLATE = ROOT / "game" / "Utilities" / "General" / "Classes" / "RoomTemplate.rpy"
ACTIONS = ROOT / "game" / "Utilities" / "General" / "Common" / "Actions.rpy"
SAVE_SYNC = ROOT / "game" / "TractirSaveSync.rpy"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def test_room_game_items_is_the_only_live_room_item_collection():
    room = read(ROOM_TEMPLATE)
    actions = read(ACTIONS)

    assert "objects=None" not in room
    assert "self.objects" not in room
    assert "restored.objects" not in room
    assert 'state["objects"] =' not in room
    assert "room_obj.objects" not in actions


def test_old_objects_collection_is_consumed_only_during_load_migration():
    room = read(ROOM_TEMPLATE)
    save_sync = read(SAVE_SYNC)

    assert 'legacy_objects = payload.pop("objects", None)' in room
    assert 'legacy_objects = restored.pop("objects", None)' in room
    assert 'room_obj.__dict__.pop("objects", None)' in save_sync
    assert "room_obj.objects =" not in save_sync
