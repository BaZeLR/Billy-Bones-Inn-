from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_clara_uses_normal_data_and_runtime_instances():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")

    assert "class ClaraData(PeopleData):" in source
    assert "class ClaraInfo(Girl):" in source
    assert "define ClaraStaticData = ClaraData()" in source
    assert "default Clara = ClaraInfo()" in source

    init_label = source.split("label InitClara:", 1)[1]
    assert "GirlName = Clara.code_name" in init_label
    assert "peopleData[GirlName] = ClaraStaticData" in init_label
    assert "Clara.var = ClaraVar" in init_label
    assert "Clara.initialize_new_game_state()" in init_label
    assert "peopleInfo[GirlName] = Clara" in init_label
    assert "if Clara not in girls:" in init_label
    assert "Clara.install_schedule()" in init_label


def test_clara_schedule_uses_json_interval_contract_not_duplicate_slot_schedule():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    schedule_model = _source(Path("game") / "Utilities" / "General" / "NPC" / "NPCScheduleModel.rpy")
    install_schedule = source.split("def install_schedule(self):", 1)[1].split("define ClaraStaticData", 1)[0]

    assert "npc_interval_schedule_load_file(name)" in install_schedule
    assert "npc_schedule_sync_currentloc(name)" in install_schedule
    assert "npc_daily_schedule_set(" not in install_schedule
    assert "npc_schedule_set(" not in install_schedule
    assert "NPCScheduleEntry(" not in install_schedule
    assert "def clara_wine_store_shift_active" not in source
    assert "def clara_extra_location_code" not in source
    assert "clara_extra_location" not in schedule_model


def test_clara_does_not_own_alber_portraits():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")

    assert "alber_random_portrait" not in source
    assert "images/Alber/" not in source


def test_clara_old_peopleinfo_bridge_is_removed():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")

    assert "Auto-attach .var for PeopleInfo consistency" not in source
    assert "if 'peopleInfo' not in dir()" not in source
    assert "class Clara(Girl):" not in source
    assert "peopleInfo['clara'] = Clara(" not in source
    assert "girls.append(peopleInfo['clara'])" not in source


def test_clara_social_and_gift_logic_belongs_to_clara_instance():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    talk_source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy")
    character_hub = _source(Path("game") / "Utilities" / "General" / "NPC" / "CharacterActionHub.rpy")
    social_topics = _source(Path("game") / "Utilities" / "General" / "NPC" / "SocialTalkTopics.rpy")

    clara_class = source.split("class ClaraInfo(Girl):", 1)[1].split("define ClaraStaticData", 1)[0]
    for method_name in [
        "can_start_social_events",
        "can_receive_gifts",
        "has_caught_cat_gift",
        "can_accept_horse_ride",
        "giftable_entries",
        "has_giftable_entries",
        "remove_gift_entry",
        "social_outcome",
        "apply_result_counters",
        "apply_social_result",
    ]:
        assert f"def {method_name}(self" in clara_class

    for old_name in [
        "def clara_can_start_social_events",
        "def clara_can_receive_gifts",
        "def clara_has_caught_cat_gift",
        "def clara_can_accept_horse_ride",
        "def clara_giftable_entries",
        "def clara_has_giftable_entries",
        "def clara_remove_gift_entry",
        "def clara_social_outcome",
        "def clara_apply_result_counters",
        "def clara_apply_social_result",
    ]:
        assert old_name not in source
        assert old_name not in talk_source

    assert "Clara.can_start_social_events()" in talk_source
    assert "Clara.giftable_entries()" in talk_source
    assert "Clara.remove_gift_entry(_selected)" in talk_source
    assert "Clara.apply_social_result(\"talk\")" in talk_source
    assert "Clara.apply_social_result(\"flirt\")" in talk_source
    assert "Clara.can_receive_gifts()" in character_hub
    assert "Clara.has_giftable_entries()" in character_hub
    assert "Clara.has_caught_cat_gift()" in social_topics


def test_clara_random_logic_uses_project_random_engine():
    source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "InitClara.rpy")
    talk_source = _source(Path("game") / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy")

    assert "procedural_randint(" in source
    assert "random.randint" not in source
    assert "renpy.random.randint" not in source
    assert "random.randint" not in talk_source
    assert "renpy.random.randint" not in talk_source
