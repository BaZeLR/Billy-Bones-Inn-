from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_legacy_room_lists_are_removed_in_favor_of_registry_groups():
    assert not (ROOT / "game/Inn/TavernRooms.rpy").exists()
    assert not (ROOT / "game/Town/TownRooms.rpy").exists()
    room_template = (ROOT / "game/Utilities/General/Classes/RoomTemplate.rpy").read_text(encoding="utf-8-sig")
    assert "class RoomRegistry(object):" in room_template
    assert "default rooms = RoomRegistry()" in room_template
    assert "roomRegistry" not in room_template
    assert "roomDefinitions[self.code_name] = self" in room_template
    assert "def rooms_in_group" in room_template
    assert "def get_registered_room" not in room_template
