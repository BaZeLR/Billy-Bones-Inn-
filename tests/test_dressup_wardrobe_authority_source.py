from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dressup_and_nightwear_write_girl_owned_state_without_layer_maps():
    dressup = (ROOT / "game/Utilities/General/Clothes/DressUp.rpy").read_text(
        encoding="utf-8-sig"
    )
    night = (ROOT / "game/Utilities/General/Clothes/DressForNight.rpy").read_text(
        encoding="utf-8-sig"
    )
    temporary = (ROOT / "game/Utilities/General/Clothes/ChangeDressTmp.rpy").read_text(
        encoding="utf-8-sig"
    )

    for legacy_map in ("dressdefault", "topdress", "bottomdress", "topraised", "bottomraised"):
        assert legacy_map not in dressup + night + temporary
    assert "_dress_wardrobe.set_day_dress(cur_default)" in dressup
    assert '_dress_wardrobe.set_day_underwear("bra", "")' in dressup
    assert "_dress_wardrobe.wear_day()" in dressup
    assert "_night_girl.wear_night_clothes(mode)" in night
    assert "girl.wear_temporary_dress(dress)" in temporary
    assert "reset_sex_clothing_state" not in dressup + night + temporary
    assert "dress_override" not in dressup + night + temporary
    assert "label DressForNight" not in night
    assert "label dress_up" not in dressup
