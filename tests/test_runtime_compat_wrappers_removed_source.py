from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_retired_runtime_compatibility_wrapper_file_is_removed():
    assert not (ROOT / "game/Utilities/General/Common/RuntimeCompat.rpy").exists()


def test_next_day_calls_tavern_job_owners_directly():
    source = (ROOT / "game/Utilities/Time/NextDay_TavernDaily.rpy").read_text(encoding="utf-8-sig")

    assert "$ change_tomorrow_whore_job('georgett')" in source
    assert "$ change_tomorrow_whore_job('liza')" in source
    assert "$ apply_tomorrow_hall_job('sandra')" in source
    assert "call change_tomorrow_whore_job" not in source
    assert "call change_tomorrow_hall_job" not in source


def test_one_hop_compatibility_labels_have_no_live_definitions_or_calls():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    for label_name in (
        "GetGirlDrunk",
        "girls_desc",
        "amanda_legare_dance_sequence",
        "ChangeTommorowWhoreJob",
        "ChangeTommorowHallJob",
        "GetRandomGirlByJob",
        "UseAleItem",
        "UseBerriesItem",
        "UseMushroomItem",
        "UseEnergyTeaItem",
        "UseLibidoTinctureItem",
        "AtticInventoryReturn",
        "ShootingPracticeReturn",
        "art_level_text",
        "GloryHoleBusy",
        "day_to_text",
        "PartEventGirlReactionTalk",
    ):
        assert re.search(r"(?m)^label\s+%s\b" % re.escape(label_name), game_sources) is None
        assert re.search(r"(?m)^\s*call\s+%s\b" % re.escape(label_name), game_sources) is None


def test_room_search_and_submenu_navigation_use_direct_contracts():
    source = (ROOT / "game/Items/Crafting/SoapCraftAndAtticItems.rpy").read_text(encoding="utf-8-sig")

    assert 'label UpstairsRoomSearch(room_code=""):' in source
    assert "restore_label" not in source
    assert 'MenuItem("Назад", Call("TavernMyRoomOpenChest"))' in source
    assert 'SetField(main_ui_runtime, "action_items", tavern_atic_action_items())' in source
    assert 'SetField(main_ui_runtime, "action_items", _shoot_return_items)' in source
    assert 'MenuItem("Назад", Jump(' not in source
