from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_completed_church_events_jump_to_the_real_room_without_wrappers():
    event_files = [
        Path("game") / "NPC" / "Girls" / "Georgett" / "IntGeorgettAfterCermon.rpy",
        Path("game") / "NPC" / "Girls" / "Liza" / "IntLizettAfterCermon.rpy",
        Path("game") / "NPC" / "Girls" / "Becky" / "IntBeckyAfterCermon.rpy",
        Path("game") / "NPC" / "Girls" / "Georgett" / "InitGeorgettChurch.rpy",
    ]

    combined = "\n".join(_source(path) for path in event_files)

    assert "\n    call Church\n" not in combined
    assert "ChurchRestore" not in combined
    assert "AdvanceTimeAndRestore" not in combined
    assert "jump Church" in _source(Path("game") / "NPC" / "Girls" / "Georgett" / "IntGeorgettAfterCermon.rpy")
    assert "jump Church" in _source(Path("game") / "NPC" / "Girls" / "Georgett" / "InitGeorgettChurch.rpy")
    assert 'show screen main_ui' in combined
    assert 'menu:' in combined
    assert '$ calendar_v2.advance_minutes(60)' in combined


def test_church_room_entry_restores_scene_mode_after_events():
    church = _source(Path("game") / "Town" / "Church" / "Church.rpy")
    room_entry = church.split("label Church:", 1)[1].split("label ChurchServiceMenu", 1)[0]

    assert '$ rooms.enter("Church")' in room_entry
    assert '$ main_ui_runtime.mode = "scene"' in room_entry
