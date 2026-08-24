from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
TOPICS = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")
TALK = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalk.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


def test_becky_husband_history_is_one_ordered_thread():
    start = RUNTIME.index('LThreadData(0, "becky", "HusbandBackstory"')
    end = RUNTIME.index('LThreadData(0, "becky", "EddieBackstory"', start)
    husband = RUNTIME[start:end]

    assert husband.count("story_becky_talk_husband_") == 4
    for action in (
        "becky_talk_husband1",
        "becky_talk_husband2",
        "becky_talk_husband3",
        "becky_talk_husband4",
    ):
        assert action in husband
    for retired in (
        "HusbandFirstTalk",
        "HusbandSecondTalk",
        "HusbandThirdTalk",
        "HusbandFourthTalk",
    ):
        assert retired not in RUNTIME


def test_becky_husband_labels_advance_thread_without_parallel_stage():
    husband_labels = TOPICS[TOPICS.index("label story_becky_talk_husband_0"):TOPICS.index("label story_becky_talk_eddie_0")]

    assert husband_labels.count("event_runtime.active_thread.advance()") == 4
    assert "event_runtime.active_thread.complete()" not in husband_labels
    assert "husbandtalk" not in husband_labels


def test_becky_talk_returns_to_npc_context_after_one_selected_action():
    assert "while True:" not in TALK
    assert "menu:" in TALK
    assert TALK.count("main_ui_end_talk_state()") >= 2


def test_retired_husband_stage_is_absent_from_live_gameplay_sources():
    live = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert "husbandtalk" not in live


def test_old_becky_husband_stage_is_promoted_once_then_deleted():
    start = MIGRATION.index("def updateSave_V23():")
    migration = MIGRATION[start:]

    assert 'becky_var.pop("husbandtalk", 0)' in migration
    assert 'thread_rows.get("beckyHusbandBackstory", None)' in migration
    assert "target = max(0, legacy_stage - 1)" in migration
    assert "husband_thread.advanceTo(" in migration
    for retired in (
        "beckyHusbandFirstTalk",
        "beckyHusbandSecondTalk",
        "beckyHusbandThirdTalk",
        "beckyHusbandFourthTalk",
    ):
        assert 'thread_rows.pop("%s", None)' % retired not in migration
        assert '"%s"' % retired in migration
