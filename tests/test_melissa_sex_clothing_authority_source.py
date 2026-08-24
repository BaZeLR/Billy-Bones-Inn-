from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_melissa_sex_menu_uses_melissa_owned_clothing_state():
    source = (ROOT / "game/NPC/Girls/Melissa/IntMelissaSex.rpy").read_text(
        encoding="utf-8-sig"
    )

    for legacy_map in ("topdress", "bottomdress", "topraised", "bottomraised"):
        assert legacy_map not in source
    assert "Melissa.clothing_layer(" in source
    assert "Melissa.layer_raised(" in source
    assert "Melissa.set_layer_raised(" in source
    assert "Melissa.remove_clothing_layer(" in source
