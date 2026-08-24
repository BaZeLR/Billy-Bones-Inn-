from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_called_church_events_return_without_reentering_the_room():
    event_files = [
        Path("game") / "NPC" / "Girls" / "Georgett" / "IntGeorgettAfterCermon.rpy",
        Path("game") / "NPC" / "Girls" / "Liza" / "IntLizettAfterCermon.rpy",
        Path("game") / "NPC" / "Girls" / "Becky" / "IntBeckyAfterCermon.rpy",
        Path("game") / "NPC" / "Girls" / "Georgett" / "InitGeorgettChurch.rpy",
    ]

    combined = "\n".join(_source(path) for path in event_files)

    assert "jump Church" not in combined
    assert 'show screen main_ui' in combined
    assert 'menu:' in combined
    assert '$ calendar_v2.advance_minutes(60)' in combined
