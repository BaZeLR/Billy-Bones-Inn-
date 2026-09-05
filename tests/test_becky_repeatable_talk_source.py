from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
PEOPLE = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(encoding="utf-8-sig")
BECKY = (ROOT / "game/NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")
TALK = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalk.rpy").read_text(encoding="utf-8-sig")
TOPICS = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")
MAIN_LAYOUT = (ROOT / "game/Utilities/General/Screens/main_layout.rpy").read_text(encoding="utf-8-sig")


def test_repeatable_becky_talk_random_choices_are_label_local():
    assert "tmpRnd" not in TOPICS
    assert "RandVar" not in TOPICS
    assert "tmp_rnd=0" in TOPICS
    assert "rand_var=0" in TOPICS


def test_becky_store_smalltalk_remains_the_authored_friendship_path():
    repeatable = TOPICS.split("label _int_becky_talk_smalltalk", 1)[1].split(
        "label story_becky_talk_inga_0", 1
    )[0]

    interrupt_work = PEOPLE.split("def interrupt_work(self):", 1)[1].split(
        "def can_work_tavern", 1
    )[0]

    assert 'work_socializing_locations = ("GroceryStore",)' in BECKY
    assert "self.work_socializing_locations" in interrupt_work
    assert repeatable.count("Becky.interrupt_work()") == 2
    assert "Becky.add_relation(1, 3)" in repeatable
    assert "Becky.add_relation(1, 6)" in repeatable
    assert repeatable.count("procedural_randint(1, 2") == 2
    assert '"%s_becky_smalltalk_%s" % (Becky.talk_count(), current_game_day())' in repeatable
    assert '"%s_becky_personal_%s" % (Becky.talk_count(), current_game_day())' in repeatable
    assert "renpy.random" not in repeatable
    assert repeatable.count("Becky.finish_talk()") == 2


def test_becky_talk_repeats_the_same_native_menu_until_explicit_exit():
    assert "while True:" in TALK
    assert 'while str(main_ui_runtime.mode or "") == "talk":' not in TALK
    assert "_becky_repeat_menu" not in TALK
    lifecycle = TALK.split("while True:", 1)[1]

    assert lifecycle.index("$ initStoryEventRuntime(True)") < lifecycle.index("menu:")
    assert TALK.count("$ main_ui_end_talk_state()") == 1
    assert "IntBeckyTalkRefresh" not in TALK
    assert "IntBeckyTalkApply" not in TALK
    assert "jump IntBeckyTalk" not in TALK


def test_talk_text_viewport_starts_at_the_first_line():
    talk_panel = MAIN_LAYOUT.split('screen main_ui_talk_panel(girl_name="", room_name="", desc=""):', 1)[1].split(
        "screen main_ui_player_card_panel", 1
    )[0]

    assert "viewport:" in talk_panel
    assert 'id ("main_ui_talk_text_%s" % hash(_text))' in talk_panel
    assert "yinitial 0.0" in talk_panel
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


RETIRED_THREADS = (
    "HomeInviteTalk",
    "HomeLastVisitTalk",
    "EddieBehaviorTalk",
    "EddieGeorgMentionTalk",
    "EddieReactionTalk",
    "EddieAfterSexTalk",
    "PregnancyFatherTalk",
)


def test_repeatable_becky_topics_are_native_menu_choices_not_threads():
    for name in RETIRED_THREADS:
        assert 'LThreadData(0, "becky", "' + name + '"' not in RUNTIME

    assert 'call checkTriggers("talk_becky", "becky_home_invite", 0)' in TALK
    for target in (
        "story_becky_home_last_visit_talk_0",
        "story_becky_talk_eddie_behavior_0",
        "story_becky_talk_eddie_georgett_1",
        "story_becky_talk_eddie_reaction_0",
        "story_becky_talk_eddie_reaction_1",
        "story_becky_talk_eddie_after_sex_0",
        "story_becky_talk_pregnancy_0",
    ):
        assert "call " + target + "(_becky_name)" in TALK


def test_both_eddie_opinion_choices_use_the_same_qsp_gate():
    assert TALK.count('Becky.georgett_mentioned and not threads["beckyEddieSex"].completed and Becky.talk_count() < 2') == 2
    assert 'call story_becky_talk_eddie_reaction_0(_becky_name)' in TALK
    assert 'call story_becky_talk_eddie_reaction_1(_becky_name)' in TALK


def test_eddie_advice_returns_to_the_active_talk_instead_of_navigating_rooms():
    advice = TOPICS.split("label story_becky_talk_eddie_reaction_1", 1)[1].split(
        "label story_becky_talk_eddie_after_sex_0", 1
    )[0]

    assert "$ Becky.finish_talk()" in advice
    assert "jump MarketPlace" not in advice
    assert advice.count("return") >= 1


def test_repeatable_topic_labels_do_not_mutate_active_thread():
    repeatable = TOPICS.split("label story_becky_talk_pregnancy_0", 1)[1]

    assert "event_runtime.active_thread" not in repeatable
    assert "thread.advance()" not in repeatable
    assert "thread.complete()" not in repeatable


def test_old_false_thread_records_are_removed_on_load():
    migration = MIGRATION.split("def updateSave_V26():", 1)[1]

    for name in RETIRED_THREADS:
        assert '"becky' + name + '"' in migration
