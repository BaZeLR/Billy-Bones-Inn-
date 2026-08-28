from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_room_registry_owns_current_location_and_derives_room_object():
    room_template = read_rel("game/Utilities/General/Classes/RoomTemplate.rpy")
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert 'self.current_code = "TavernMain"' in room_template
    assert "def current(self):" in room_template
    assert "return self.get(self.current_code)" in room_template
    assert "def enter(self, room_code=\"\"):" in room_template
    assert "return self.current" in room_template
    assert re.search(r"\bCurLoc\b", live_sources) is None
    assert re.search(r"\bCurrentRoom\b", live_sources) is None
    assert "rooms.current =" not in live_sources


def test_room_entries_set_location_once_through_registry():
    gameplay_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name not in ("RoomTemplate.rpy", "TractirSaveSync.rpy")
    )

    assert gameplay_sources.count("rooms.enter(") >= 40
    assert re.search(r"rooms\.current_code\s*=(?!=)", gameplay_sources) is None


def test_old_location_names_are_one_way_save_migration_only():
    migration = read_rel("game/TractirSaveSync.rpy")

    assert "define currentVersion = 70" in migration
    assert "def updateSave_V35():" in migration
    assert 'globals().pop("CurLoc", "")' in migration
    assert 'globals().pop("CurrentRoom", None)' in migration
    assert "rooms.enter(legacy_code or \"TavernMain\")" in migration
