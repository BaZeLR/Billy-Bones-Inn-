from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
TOPICS = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")
INIT = (ROOT / "game/NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


def test_becky_eddie_topics_are_one_ordered_thread():
    thread = RUNTIME.split('LThreadData(0, "becky", "EddieBackstory"', 1)[1]
    thread = thread.split('LThreadData(0, "becky", "GeorgettHomeVisit"', 1)[0]

    assert thread.count("story_becky_talk_eddie_0") == 1
    assert thread.count("story_becky_talk_eddie_georgett_0") == 1
    assert "EddieFirstTalk" not in RUNTIME
    assert "EddieGeorgettTalk" not in RUNTIME


def test_becky_eddie_labels_advance_same_thread_without_scalar_stage():
    labels = TOPICS.split("label story_becky_talk_eddie_0", 1)[1]
    labels = labels.split("label story_becky_home_invite_talk_0", 1)[0]

    assert labels.count("event_runtime.active_thread.advance()") == 2
    assert "event_runtime.active_thread.complete()" not in labels
    assert "eddietalk" not in labels
    assert '"eddietalk"' not in INIT


def test_invite_reads_completed_eddie_thread_and_old_stage_migrates_once():
    invite = TOPICS.split("label story_becky_home_invite_talk_0", 1)[1]
    invite = invite.split("label story_becky_talk_pregnancy_0", 1)[0]
    migration = MIGRATION.split("def updateSave_V25():", 1)[1]

    assert 'threads.get("beckyEddieBackstory", None)' in invite
    assert "int(_becky_eddie_thread.num or 0) >= 2" in invite
    assert 'becky_var.pop("eddietalk", 0)' in migration
    assert 'thread_rows.get("beckyEddieBackstory", None)' in migration
    assert '"beckyEddieFirstTalk", "beckyEddieGeorgettTalk"' in migration


def test_becky_eddie_reaction_comparison_is_label_local():
    reactions = TOPICS.split("label story_becky_talk_eddie_reaction_0", 1)[1]
    reactions = reactions.split("label story_becky_talk_eddie_after_sex_0", 1)[0]

    assert "change_mind=0" in reactions
    assert "ChangeMind" not in reactions
