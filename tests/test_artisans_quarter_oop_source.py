from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game" / "Town" / "Arts" / "ArtisansQuarter.rpy"


def test_artisans_quarter_builds_actions_inline_without_restore_loop():
    source = SOURCE.read_text(encoding="utf-8-sig")

    assert "label ArtisansQuarterBuildActions:" not in source
    assert "call ArtisansQuarterBuildActions" not in source
    assert "label ArtisansQuarterRestore:" not in source
    assert "while _artisans_" not in source
    assert "rooms.get(\"ArtisansQuarter\").visible_objects()" in source
    assert "rooms.get(\"ArtisansQuarter\").visible_exits()" in source
    assert "movement_actions(_artisans_exit.target, artisans_quarter_exit_minutes(_artisans_exit.target))" in source


def test_artisans_quarter_keeps_real_object_actions_and_destinations():
    source = SOURCE.read_text(encoding="utf-8-sig")

    for destination in ("StolyarWorkshop", "DressShop", "BarberShop", "StreetTavern"):
        assert 'target="%s"' % destination in source
    assert 'object_id="workshops"' in source
    assert 'object_id="farago_shop_sign"' in source
    assert "label ArtisansQuarterObjectMenu" in source
    assert "label ArtisansQuarterObjectText" in source
