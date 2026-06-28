from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_town_street_thugs_shout_renders_result_screen():
    source = (PROJECT_ROOT / "game" / "Town" / "RandomTownEvents.rpy").read_text(encoding="utf-8-sig")
    body = source.split("label TownStreetThugsShout:", 1)[1].split("label TownStreetPatrolEvent:", 1)[0]

    assert "Попробовать спугнуть их криком" not in body
    assert "current_action_items = [MenuItem(\"Идти дальше\", Function(renpy.return_statement, True))]" in body
    assert "call screen main_ui" in body
