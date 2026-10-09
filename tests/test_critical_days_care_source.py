from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_girl_owns_daily_critical_care_state_and_penetration_rule():
    text = source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    assert 'self.critical_hygiene_request_day = -1' in text
    assert 'self.critical_hygiene_supplied_day = -1' in text
    assert 'self.critical_tea_day = -1' in text
    assert 'def critical_days_active(self):' in text
    assert 'def is_tavern_team_girl(self):' in text
    assert 'def can_accept_penetration_today(self):' in text
    assert 'if str(action_code or "").strip().lower() in ("vaginal", "anal"):' in text


def test_pad_item_and_recipe_use_existing_cloth_and_moss_authorities():
    text = source("game/Items/Crafting/SoapCraftAndAtticItems.rpy")
    assert 'object_id="moss_cloth_pad_001"' in text
    assert 'recipe_id="moss_cloth_pad_recipe"' in text
    assert 'item_result="moss_cloth_pad_001"' in text
    assert '"cloth_scrap_001": {"quantity": 1' in text
    assert '"dried_moss_001": {"quantity": 1' in text
    assert 'result_quantity=1' in text


def test_each_present_team_girl_can_make_a_daily_request():
    text = source("game/Inn/HouseholdRuntimeEvents.rpy")
    assert 'def household_critical_care_request_ready(girl_name=""):' in text
    assert 'girl_info.is_tavern_team_girl()' in text
    assert 'girl_info.critical_days_active()' in text
    assert 'girl_info.critical_hygiene_supplied_today()' in text
    assert 'for girl, girl_info in people.girl_items()' in text
    assert 'return ("critical_care", girl)' in text
    assert 'label HouseholdCriticalCareRequestEvent(girl_name=""):' in text
    assert 'player.remove_item("moss_cloth_pad_001", 1)' in text
    assert 'player.remove_item("energy_tea_001", 1)' in text


def test_room_entries_present_the_native_request_label():
    for relative_path in ("game/Inn/TavernMain.rpy", "game/Inn/TavernKitchen.rpy"):
        text = source(relative_path)
        assert '== "critical_care":' in text
        assert 'call HouseholdCriticalCareRequestEvent(' in text


def test_direct_and_automated_penetration_paths_use_the_shared_rule():
    direct_paths = (
        "game/NPC/Girls/Amanda/IntAmandaSex.rpy",
        "game/NPC/Girls/Amanda/AmandaAtHomeCode.rpy",
        "game/NPC/Girls/Amanda/AmandaAtGloryHole.rpy",
        "game/NPC/Girls/Amanda/AfterDanceSexLegare.rpy",
        "game/NPC/Girls/Amanda/AmandaLoverSex.rpy",
        "game/NPC/Girls/Liza/IntLizaSex.rpy",
        "game/NPC/Girls/Georgett/IntGeorgettSex.rpy",
        "game/NPC/Girls/Georgett/InitGeorgettChurch.rpy",
    )
    for relative_path in direct_paths:
        assert '.can_accept_penetration_today()' in source(relative_path)

    assert 'sex_event_type_for_cycle' in source("game/Utilities/General/Sex/WhoreNextDayClients.rpy")
    assert 'sex_event_type_for_cycle' in source("game/Inn/TavernProstClients.rpy")
    assert 'sex_event_type_for_cycle' in source("game/Utilities/General/Sex/StreetClients.rpy")
    assert 'sex_event_type_for_cycle' in source("game/Utilities/Time/NextDay_FinishDayEvents.rpy")
    assert 'self.can_accept_penetration_today()' in source("game/NPC/Girls/Liza/InitLiza.rpy")
    assert 'self.can_accept_penetration_today()' in source("game/NPC/Girls/Georgett/InitGeorgett.rpy")
