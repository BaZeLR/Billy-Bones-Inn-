from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_household_sex_menu_uses_selected_npc_owned_clothing_state():
    source = (ROOT / "game/NPC/Girls/Melissa/IntMelissaSex.rpy").read_text(
        encoding="utf-8-sig"
    )

    for legacy_map in ("topdress", "bottomdress", "topraised", "bottomraised"):
        assert legacy_map not in source
    assert "_hse_info.clothing_layer(" in source
    assert "_hse_info.layer_raised(" in source
    assert "_hse_info.set_layer_raised(" in source
    assert "_hse_info.remove_clothing_layer(" in source
    assert 'people.get_info(_hse_girl)' in source
