from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MELISSA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "InitMelissa.rpy"
PEOPLE_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
GIRL_DECISION = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "GirlDecisionModel.rpy"


def test_melissa_uses_data_info_runtime_shape():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")

    assert "class MelissaData(PeopleData):" in source
    assert "class MelissaInfo(Girl):" in source
    assert "define MelissaStaticData = MelissaData()" in source
    assert "default Melissa = MelissaInfo()" in source
    assert "peopleData[GirlName] = MelissaStaticData" in source
    assert "peopleInfo[GirlName] = Melissa" in source
    assert "register_melissa_runtime" not in source


def test_melissa_data_keeps_identity_not_runtime_maps():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    data_block = source.split("class MelissaData(PeopleData):", 1)[1].split("class MelissaInfo(Girl):", 1)[0]

    assert "code_name = \"melissa\"" in data_block
    assert "fullname=\"Мелисса\"" in data_block
    assert "birth_date" in data_block
    assert "card_image" in data_block
    assert "schedule_source" in data_block
    assert "self.stats" not in data_block
    assert "self.jobs" not in data_block
    assert "self.wardrobe" not in data_block
    assert "self.var" not in data_block


def test_melissa_story_defaults_cover_live_melissavar_keys():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    required_keys = [
        "MomDressComplaint",
        "AskedAboutClaraDay",
        "StartDay",
        "StartCount",
        "StartTotal",
        "private_context_day",
        "private_context_origin",
        "private_context_place",
        "private_place_heat",
        "RoomProblemAskDay",
        "StorageThanksDay",
        "AtticFindingsDay",
        "bats_episode",
        "temp_room",
        "storage_rat_last_help_day",
        "room_pests_last_help_day",
        "AskedMCToSolveRoomProblem",
        "bat_attic_check_day",
        "drawings_ready_day",
        "drawings_found",
        "drawings_returned",
        "bat_recipe_clue_seen",
        "bat_recipe_unlocked",
        "bats_completed",
        "bats_completion_day",
        "room_returned",
        "sex_engine_unlocked",
        "roof_repair_order_day",
        "roof_repair_complete_day",
        "breakfast_tease_day",
    ]

    for key in required_keys:
        assert f'"{key}"' in source


def test_melissa_info_owns_runtime_defaults_without_legacy_sync():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    runtime = PEOPLE_RUNTIME.read_text(encoding="utf-8-sig")

    for token in [
        "self.rel = 5",
        "self.openness = 0",
        "self.corruption = 3",
        "self.energy = 100",
        "self.mana = 10",
        "self.talked_today = 0",
        "self.flirted_today = 0",
        "self.gifted_today = 0",
        "self.asked_today = 0",
        "self.fucked_today = 0",
        "self.drunk = 0",
        "\"beauty\": 55",
        "\"ConceptionChance\": 15",
        "\"PussyWetStart\": 10",
        "\"virginity\": True",
        "\"cooking\": 30",
        "\"cleaning\": 40",
        "\"waitress\": 30",
        "\"jobcleaning\": 1",
        "\"jobwaitress\": 1",
        "def install_schedule",
    ]:
        assert token in source

    for token in [
        "def sync_from_melissa_maps",
        "def sync_melissa_maps",
        "Melissa.var =",
        "MelissaVar",
    ]:
        assert token not in source

    for token in [
        "def reset_daily",
        "def mana_bad_probability",
        "def reward_need_fulfilled",
        "def punish_need_unfulfilled",
        "def decision_profile",
        "def decide",
        "def decision_good_probability",
        "def record_reaction",
        "def last_decision_reaction",
        "def apply_decision_reaction",
    ]:
        assert token in runtime

    melissa_info_block = source.split("class MelissaInfo(Girl):", 1)[1]
    for token in [
        "def decision_profile",
        "def decide",
        "def decision_good_probability",
        "def record_reaction",
        "def last_decision_reaction",
        "def apply_decision_reaction",
    ]:
        assert token not in melissa_info_block

    decision_source = GIRL_DECISION.read_text(encoding="utf-8-sig")
    for token in [
        'GIRL_DECISION_CORE_IDS = ("amanda", "melissa", "sandra")',
        "girl_info = getPersonInfo(girl)",
        "girl in GIRL_DECISION_CORE_IDS",
        '"mana_bad_probability": girl_info.mana_bad_probability()',
        "in GIRL_DECISION_CORE_IDS:",
    ]:
        assert token in decision_source


def test_melissa_has_five_valid_favorite_talk_topics():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")

    assert '"favorite_topics": ["job_routine", "family_life", "melissa_safety", "melissa_quiet", "stories"]' in source
    assert '"clothes"' not in source


def test_melissa_removed_hidden_conditional_class_registration():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")

    assert "class Melissa(Girl):" not in source
    assert "isinstance(peopleInfo.get('melissa'), Melissa)" not in source
    assert "peopleInfo['melissa'] = Melissa" not in source
    assert "dir()" not in source
    assert "globals()" not in source
    assert "renpy.store" not in source
    assert "calendar_make_birth_record" not in source
