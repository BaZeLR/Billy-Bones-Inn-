from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_becky_sex_menu_uses_becky_owned_clothing_state():
    source = (ROOT / "game/NPC/Girls/Becky/IntBeckySex.rpy").read_text(
        encoding="utf-8-sig"
    )

    for legacy_map in (
        "topdress",
        "bottomdress",
        "topraised",
        "bottomraised",
        "pantiesdef",
    ):
        assert legacy_map not in source
    assert "Becky.clothing_layer(" in source
    assert "Becky.clothing_slut(" in source
    assert "Becky.set_layer_raised(" in source
    assert "Becky.remove_clothing_layer(" in source


def test_becky_sex_uses_the_authored_pregnancy_procedure_label():
    source = (ROOT / "game/NPC/Girls/Becky/IntBeckySex.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "Becky.apply_pregnancy_check" not in source
    assert source.count('call PregnancyCheck("becky",') == 5
