from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BARBER_SHOP = PROJECT_ROOT / "game" / "Town" / "Arts" / "BarberShop.rpy"
NPC_VISIBILITY = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "CheckVisibility.rpy"


def test_barber_shop_open_hours_use_calendar_clock_not_display_slot():
    source = BARBER_SHOP.read_text(encoding="utf-8-sig")
    body = source.split("def barber_shop_is_open():", 1)[1].split("\n    def ", 1)[0]

    assert "calendar_v2.sync_state()" in body
    assert "calendar_v2.week" in body
    assert "calendar_v2.hour" in body
    assert "calendar_v2.minute" in body
    assert "12 * 60" in body
    assert "17 * 60 + 59" in body
    assert "8 * 60" in body
    assert "11 * 60 + 59" in body
    assert "time_slot" not in body
    assert "int(time" not in body


def test_npc_appearance_engine_has_unique_profiles_for_core_adult_women():
    source = NPC_VISIBILITY.read_text(encoding="utf-8-sig")
    for npc_id in ("amanda", "melissa", "sandra", "becky", "georgett", "clara", "irma", "inga"):
        assert '"%s": {' % npc_id in source

    assert '"signature": "teasing_awakening"' in source
    assert '"signature": "warm_libertine"' in source
    assert '"signature": "fashion_precision"' in source
    assert '"signature": "professional_sensual"' in source


def test_npc_appearance_runtime_is_owned_by_body_profile_and_uses_real_clock():
    source = NPC_VISIBILITY.read_text(encoding="utf-8-sig")

    assert "def npc_appearance_state(" in source
    assert 'body_profile["appearance"] = state' in source
    assert "BodyInteractionProfiles[key] = body_profile" in source
    assert "calendar_v2.hour" in source
    assert "calendar_v2.minute" in source
    assert "time_slot" not in source


def test_grooming_and_body_products_mutate_shared_appearance_state():
    source = NPC_VISIBILITY.read_text(encoding="utf-8-sig")

    assert "def npc_apply_grooming(" in source
    assert "def npc_set_body_hair_state(" in source
    assert "def npc_apply_body_product(" in source
    assert '"soap_001"' in source
    assert '"luxury_soap_001"' in source
    assert '"fresh_shaved"' in source
    assert '"micro_stubble"' in source
    assert '"soft_regrowth"' in source


def test_intimate_description_is_visibility_and_adult_gated():
    source = NPC_VISIBILITY.read_text(encoding="utf-8-sig")

    assert '"PussyVisible"' in source
    assert "_girls_desc_age_value(key) >= 18" in source
    assert '"vulva"' in source
    assert '"intimate"' in source


def test_existing_girls_desc_builder_is_extended_not_replaced_by_another_ui():
    source = NPC_VISIBILITY.read_text(encoding="utf-8-sig")

    assert "_girls_desc_build_lines_core = _girls_desc_build_lines" in source
    assert "npc_appearance_description_lines(" in source
    assert "label GirlsDesc" not in source
