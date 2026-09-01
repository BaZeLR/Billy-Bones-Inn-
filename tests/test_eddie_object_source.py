from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_eddie_has_own_data_info_and_explicit_state():
    source = read_rel("game/NPC/Secondary/InitEddie.rpy")
    people_runtime = read_rel("game/Utilities/General/NPC/PeopleRuntime.rpy")

    assert "class EddieData(PeopleData):" in source
    assert "class EddieInfo(BaseNPC):" in source
    assert "define EddieStaticData = EddieData()" in source
    assert "default Eddie = EddieInfo()" in source
    assert "self.var =" not in source
    assert "STORY_DEFAULTS" not in source
    assert "ensure_story_defaults" not in source
    assert "def eddie_story_defaults(" not in source
    assert "whore_visit_frequency = 6" in source
    for field_name in (
        "told_about_tavern_whores", "seen_with_georgett",
        "talked_about_georgett", "saw_mother_sex", "fingal_talk_stage",
        "asked_fingal_destination", "asked_fingal_guard_complaint",
        "ridiculed_follow_attempt", "others_saw_with_mother",
    ):
        assert "self.%s =" % field_name in source
    assert "label InitEddie:" not in source
    assert "label register_eddie_secondary:" in source


def test_eddie_uses_class_state_not_old_var_bridge():
    combined = "\n".join(
        [
            read_rel("game/NPC/Secondary/InitEddie.rpy"),
            read_rel("game/NPC/Secondary/IntEddieTalk.rpy"),
            read_rel("game/Utilities/Time/NextDay_NewDayEvents.rpy"),
            read_rel("game/NPC/Girls/Becky/IntBeckyGuest.rpy"),
            read_rel("game/NPC/Girls/Georgett/IntGeorgettTalk.rpy"),
            read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy"),
            read_rel("game/Inn/TavernProstClients.rpy"),
        ]
    )

    assert "EddieVar" not in combined
    assert "Eddie.var =" not in combined
    assert 'getattr(renpy.store, "Eddie.var"' not in combined
    assert "getattr(renpy.store, 'Eddie.var'" not in combined
    assert '_ensure_dict("Eddie.var")' not in combined
    assert '"var": Eddie.var' not in combined
    assert "Eddie(var=" not in combined
    assert "EddieInfo(var=" not in combined
    assert "Eddie.var.setdefault" not in combined
    assert "Eddie.var" not in combined
    assert "Eddie.var_int" not in combined
    assert "Eddie.set_var_int" not in combined


def test_tavern_client_event_uses_native_menu_and_returns_to_caller():
    source = read_rel("game/Inn/TavernProstClients.rpy")

    assert "menu:" in source
    assert "call screen main_ui" not in source
    assert "main_ui_runtime.action_items" not in source
    assert "jump expression" not in source


def test_eddie_threads_and_dialog_use_class_state():
    talk_source = read_rel("game/NPC/Secondary/IntEddieTalk.rpy")
    becky_talk_source = read_rel("game/NPC/Girls/Becky/IntBeckyTalk.rpy")
    threads_source = read_rel("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    people_source = read_rel("game/Utilities/General/NPC/PeopleRuntime.rpy")

    assert "Eddie.ensure_story_defaults()" not in talk_source
    assert "Eddie.talked_about_georgett" in threads_source
    assert "Eddie.saw_mother_sex" in threads_source
    assert "Eddie.fingal_talk_stage > 0" in becky_talk_source
    assert "call register_eddie_secondary" in people_source


def test_eddie_v60_migration_consumes_old_map_once():
    migration = read_rel("game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V60():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 77" in migration
    assert "if loaded_version < 61:" in migration
    assert "updateSave_V60()" in migration
    for old_key, field_name in (
        ("TalkedAboutWhores", "told_about_tavern_whores"),
        ("SawWithGeorgett", "seen_with_georgett"),
        ("TalkedAboutGeorgett", "talked_about_georgett"),
        ("SawMomSex", "saw_mother_sex"),
        ("FingalTalk", "fingal_talk_stage"),
        ("FingalTalkDestination", "asked_fingal_destination"),
        ("FingalTalkComplain", "asked_fingal_guard_complaint"),
        ("RidiculeFollow", "ridiculed_follow_attempt"),
        ("OthersSawWithMom", "others_saw_with_mother"),
    ):
        assert 'eddie_var.pop("%s"' % old_key in block
        assert "Eddie.%s =" % field_name in block
    assert 'eddie_var.pop("WhoreVisitFreq", None)' in block
    assert 'globals().pop("EddieVar", None)' in block
