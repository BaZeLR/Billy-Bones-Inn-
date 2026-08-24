from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
TALK = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalk.rpy").read_text(encoding="utf-8-sig")
LABELS = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalkSherwood.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
QUEST = (ROOT / "game/NPC/Girls/Becky/BeckyQuestInit.rpy").read_text(encoding="utf-8-sig")
BECKY_INIT = (ROOT / "game/NPC/Girls/Becky/InitBecky.rpy").read_text(encoding="utf-8-sig")
ROBIN_INIT = (ROOT / "game/NPC/Secondary/InitRobin.rpy").read_text(encoding="utf-8-sig")
ZIMMER_INIT = (ROOT / "game/NPC/Secondary/InitZimmer.rpy").read_text(encoding="utf-8-sig")
NEXT_DAY = (ROOT / "game/Utilities/Time/NextDay_NewDayEvents.rpy").read_text(encoding="utf-8-sig")


TOPICS = (
    ("SherwoodOfferTalk", "story_becky_sherwood_offer_0"),
    ("SherwoodElvesTalk", "story_becky_sherwood_elves_0"),
    ("SherwoodFingalTalk", "story_becky_sherwood_fingal_0"),
    ("SherwoodWarnTalk", "story_becky_sherwood_warn_0"),
    ("SherwoodRoadTalk", "story_becky_sherwood_road_0"),
    ("SherwoodLiedTalk", "story_becky_sherwood_lied_0"),
    ("SherwoodRobbedTalk", "story_becky_sherwood_robbed_0"),
    ("SherwoodHowToTalk", "story_becky_sherwood_howto_0"),
    ("SherwoodWarnedTalk", "story_becky_sherwood_warned_0"),
)


def test_sherwood_followups_are_direct_native_topics_not_false_threads():
    for thread_name, target in TOPICS:
        assert 'LThreadData(0, "becky", "' + thread_name + '"' not in RUNTIME
        assert "call " + target + "(_becky_name)" in TALK


def test_sherwood_labels_change_only_branch_facts_not_thread_state():
    assert "event_runtime.active_thread" not in LABELS
    assert "thread.advance()" not in LABELS
    assert "thread.complete()" not in LABELS
    for fact in (
        'Becky.trade_offer_stage = 1',
        'Becky.asked_about_elf_trade = True',
        'Becky.fingal_connection_clarified = True',
        'Becky.sherwood_warning_stage = 2',
        'Becky.admitted_sherwood_stage = 1',
        'Becky.robbery_consolation_count',
        'Becky.robin_robbery_stage',
    ):
        assert fact in LABELS


def test_sherwood_topic_conditions_preserve_qsp_branch_gates():
    assert 'Becky.trade_offer_stage == 2' in TALK
    assert 'not Becky.asked_about_elf_trade' in TALK
    assert "Eddie.fingal_talk_stage > 0" in TALK
    assert 'Becky.sherwood_warning_stage == 1' in TALK
    assert 'Becky.knows_blackwood' in TALK
    assert 'Becky.robin_robbery_stage == 1' in TALK
    assert 'Becky.robin_robbery_stage >= 2' in TALK


def test_old_sherwood_topic_thread_records_are_removed_on_load():
    migration = MIGRATION.split("def updateSave_V27():", 1)[1]

    for thread_name, _target in TOPICS:
        assert '"becky' + thread_name + '"' in migration


def test_blackwood_quest_has_one_live_offer_label_and_one_static_text_source():
    assert not (ROOT / "game/NPC/Girls/Becky/BeckyEvents.rpy").exists()
    assert QUEST.count("define BECKY_TRADE_OFFER_TEXT =") == 1
    assert '"[BECKY_TRADE_OFFER_TEXT]"' in QUEST
    assert 'scene_runtime.text += "\\n\\n" + BECKY_TRADE_OFFER_TEXT' in LABELS
    assert "TradeOfferText" not in BECKY_INIT


def test_blackwood_trigger_uses_robbery_day_as_its_single_one_time_state():
    trigger = NEXT_DAY.split("# Бекки предлагает подзаработать", 1)[1]
    trigger = trigger.split("# Francheska", 1)[0]

    assert "Becky.eddie_robbed_day == 0" in trigger
    assert "Becky.eddie_robbed_day = day_value" in trigger
    assert "EddieRobbed'" not in trigger
    assert '"EddieRobbed"' not in BECKY_INIT
    assert '"SherwoodQuestScheduled"' not in BECKY_INIT


def test_unreachable_future_blackwood_outcome_flags_are_not_live_defaults():
    assert '"PlayerDestroyedCamp"' not in ROBIN_INIT
    assert '"ZimmerPeaceful"' not in ROBIN_INIT
    assert '"MissionUpdatedByPlayer"' not in ZIMMER_INIT
    assert '"PlayerHandledRobin"' not in ZIMMER_INIT
