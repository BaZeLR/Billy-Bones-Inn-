from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLARA_PRIVATE = ROOT / "game" / "NPC" / "Girls" / "Clara" / "ClaraPrivateGamesThread.rpy"
CLARA_TALK = ROOT / "game" / "NPC" / "Girls" / "Clara" / "IntClaraTalk.rpy"
RUNTIME = ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
SHARED_ENGINE = ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaSex.rpy"
CLARA_INIT = ROOT / "game" / "NPC" / "Girls" / "Clara" / "InitClara.rpy"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def label(source, name):
    return source.split("label %s:" % name, 1)[1].split("\n\n# Event:", 1)[0]


def test_private_games_are_entered_only_from_clara_talk():
    talk = read(CLARA_TALK)
    branch = talk.split('"Спросить, почему вас не пускали в комнату"', 1)[1].split(
        '"Спросить Клариссу о семье"', 1
    )[0]

    assert 'story_event_available("talk_clara", "private_games")' in branch
    assert 'call checkTriggers("talk_clara", "private_games", 0)' in branch
    assert 'threads["claraPrivateGames"]' not in branch
    assert 'player.item_count("special_cream_001")' not in branch
    assert "jump TavernMelissaRoom" not in branch
    assert "call RoomEnterEventGate" not in branch


def test_private_game_label_owns_consent_and_delegates_intimacy_without_loops():
    source = read(CLARA_PRIVATE)
    first = label(source, "story_clara_private_games_0")
    assert "main_ui_begin_native_scene_state(" in first
    assert "show screen main_ui" in first
    assert 'vscene ClaraStaticData.image_path("portrait", "default")' in first
    assert "menu:" in first
    assert "main_ui_end_native_scene_state()" in first
    assert "while " not in first
    assert "jump " not in first
    assert 'call HouseholdSexEngine("clara", "TavernMelissaRoom", "blowjob")' in first
    assert "bodymodel_apply_action(" not in first
    assert "pregnancy_check(" not in first
    assert ".set_cock_position(" not in first
    assert ".set_arousal(" not in first
    assert first.count("event_runtime.active_thread.advance()") == 1


def test_private_thread_has_one_event_and_shared_engine_owns_anal():
    runtime = read(RUNTIME)
    engine = read(SHARED_ENGINE)
    clara = read(CLARA_INIT)
    clara_class = clara.split("class ClaraInfo(Girl):", 1)[1].split(
        "define ClaraStaticData", 1
    )[0]

    clara_list = runtime.split("define claraThreadList = [", 1)[1].split(
        "define beckyThreadList = [", 1
    )[0]
    block = clara_list.split('LThreadData(0, "clara", "PrivateGames"', 1)[1].split(
        "]\n]", 1
    )[0]
    georgett_list = runtime.split("define georgettThreadList = [", 1)[1].split(
        "define franThreadList = [", 1
    )[0]
    assert block.count('"story_clara_private_games_0"') == 1
    assert 'threads[\'claraPaintingsPath\'].completed' in block
    assert "threads['claraTavernVisit'].num" in block
    assert "Clara.relationship_allows('private_talk')" in block
    assert 'LThreadData(0, "clara", "PrivateGames"' not in georgett_list
    assert "story_clara_private_games_1" not in runtime
    assert 'def intimacy_action_allowed(self, action_code=""):' in clara_class
    assert 'if action_key == "anal":' in clara_class
    assert 'return self.relationship_allows("sex")' in clara_class
    assert 'if action_key == "vaginal":' in clara_class
    assert 'return not bool(self.sex_stat("virginity", True))' in clara_class
    assert '_hse_info.intimacy_action_allowed("anal")' in engine
    assert '_hse_info.intimacy_action_allowed("vaginal")' in engine
    assert '_hse_info.intimacy_scene_text("anal", _hse_full_engine)' in engine
    assert 'girl == "clara"' not in engine
    assert 'threads["claraPrivateGames"]' not in engine
    assert "def household_sex_anal_unlocked" not in engine
    assert 'player.remove_item("special_cream_001", 1)' not in read(CLARA_PRIVATE)


def test_private_games_do_not_duplicate_sofa_or_merchant_authority():
    source = read(CLARA_PRIVATE)

    assert "Clara.merchant_contact_unlocked =" not in source
    assert "claraForestSofa" not in source
    assert "cursed_sofa_001" not in source
    assert "main_ui_runtime.action_items" not in source
    assert "default " not in source


def test_clara_owns_shared_intimacy_availability_without_fake_visual_mappings():
    source = read(CLARA_INIT)
    engine = read(SHARED_ENGINE)
    clara_class = source.split("class ClaraInfo(Girl):", 1)[1].split(
        "define ClaraStaticData", 1
    )[0]

    assert 'def relationship_allows(self, action_code="talk"):' in clara_class
    assert 'private_thread = threads.get("claraPrivateGames")' in clara_class
    assert 'paintings_thread = threads.get("claraPaintingsPath")' in clara_class
    assert 'relationship_social_action_allowed(self.code_name, "private_talk")' in clara_class
    assert "and not self.sex_busy()" in clara_class
    assert "and self.can_have_sex_today()" in clara_class
    assert 'def intimacy_available(self, action_code="intimacy"):' in clara_class
    assert 'return self.relationship_allows(action_code)' in clara_class
    assert 'relationship_social_action_allowed("clara", "private_talk")' not in engine
    assert 'return bool(info.intimacy_available(action_code))' in engine
    initial_blowjob = engine.split('elif _hse_initial_action == "blowjob":', 1)[1].split(
        "label household_sex_menu:", 1
    )[0]
    assert '_hse_picture = _hse_data.cycle_image("sexy_times", "blowjob"' in initial_blowjob
    assert 'if str(_hse_picture or "").strip():' in initial_blowjob
    assert 'scene_runtime.picture = _hse_picture' in initial_blowjob

    data_class = source.split("class ClaraData(PeopleData):", 1)[1].split(
        "class ClaraInfo(Girl):", 1
    )[0]
    assert 'portrait="images/clara/portrait.png"' in data_class
    assert '"portrait": {"default": [self.portrait]}' in data_class
    for fake_context in ('"grope"', '"outfit_reward"', '"sexy_times"'):
        assert fake_context not in data_class
