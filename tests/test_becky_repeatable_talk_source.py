from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
TALK = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalk.rpy").read_text(encoding="utf-8-sig")
TOPICS = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")


def test_repeatable_becky_talk_random_choices_are_label_local():
    assert "tmpRnd" not in TOPICS
    assert "RandVar" not in TOPICS
    assert "tmp_rnd=0" in TOPICS
    assert "rand_var=0" in TOPICS


def test_becky_talk_repeats_the_same_native_menu_until_explicit_exit():
    assert 'while str(main_ui_runtime.mode or "") == "talk":' in TALK
    lifecycle = TALK.split('while str(main_ui_runtime.mode or "") == "talk":', 1)[1]

    assert lifecycle.index("$ initStoryEventRuntime(True)") < lifecycle.index("menu:")
    assert TALK.count("$ main_ui_end_talk_state()") == 1
    assert "IntBeckyTalkRefresh" not in TALK
    assert "IntBeckyTalkApply" not in TALK
    assert "jump IntBeckyTalk" not in TALK
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

    for target in (
        "story_becky_home_invite_talk_0",
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
    assert TALK.count('Becky.georgett_mentioned and Becky.home_visit_stage < 7 and Becky.talk_count() < 2') == 2
    assert 'call story_becky_talk_eddie_reaction_0(_becky_name)' in TALK
    assert 'call story_becky_talk_eddie_reaction_1(_becky_name)' in TALK


def test_repeatable_topic_labels_do_not_mutate_active_thread():
    repeatable = TOPICS.split("label story_becky_home_invite_talk_0", 1)[1]

    assert "event_runtime.active_thread" not in repeatable
    assert "thread.advance()" not in repeatable
    assert "thread.complete()" not in repeatable


def test_old_false_thread_records_are_removed_on_load():
    migration = MIGRATION.split("def updateSave_V26():", 1)[1]

    for name in RETIRED_THREADS:
        assert '"becky' + name + '"' in migration
