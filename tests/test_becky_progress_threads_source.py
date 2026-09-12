from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
RUNTIME = (GAME / "Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
HOME_FRONT = (GAME / "Town/BeckyHomeFront.rpy").read_text(encoding="utf-8-sig")
HOME = (GAME / "Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")
SEX = (GAME / "NPC/Girls/Becky/IntBeckySex.rpy").read_text(encoding="utf-8-sig")
DINNER = (GAME / "NPC/Girls/Becky/IntBeckyGuest.rpy").read_text(encoding="utf-8-sig")
TOPICS = (GAME / "NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")
EDDIE_SCENE = (GAME / "NPC/Girls/Becky/BeckyEddieJoinFirst.rpy").read_text(encoding="utf-8-sig")
CHURCH = (GAME / "NPC/Girls/Becky/IntBeckyAfterCermon.rpy").read_text(encoding="utf-8-sig")
INVITE = (GAME / "NPC/Girls/Becky/BeckyInviteHome.rpy").read_text(encoding="utf-8-sig")
EDDIE_TALK = (GAME / "NPC/Secondary/IntEddieTalk.rpy").read_text(encoding="utf-8-sig")
SHERWOOD = (GAME / "NPC/Secondary/SherwoodTravel.rpy").read_text(encoding="utf-8-sig")
NEXT_DAY = (GAME / "Utilities/Time/NextDay_NewDayEvents.rpy").read_text(encoding="utf-8-sig")
KITCHEN = (GAME / "Inn/TavernKitchen.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (GAME / "TractirSaveSync.rpy").read_text(encoding="utf-8-sig")


def test_becky_progress_has_one_thread_owner_per_story_sequence():
    for subname in ("SandraKitchenVisit", "Home", "Dinner", "Sex", "GerhardAdvice", "EddieSex"):
        assert RUNTIME.count(f'LThreadData(0, "becky", "{subname}"') == 1

    assert RUNTIME.count('LThreadData(0, "becky", "SherwoodTrade"') == 1

    assert 'LThreadData(0, "becky", "GeorgettHomeVisit"' not in RUNTIME
    assert "default becky_home" not in RUNTIME.lower()
    assert "default becky_dinner" not in RUNTIME.lower()
    assert "default becky_sex" not in RUNTIME.lower()
    assert "default becky_eddie_sex" not in RUNTIME.lower()


def test_becky_labels_advance_their_authoritative_story_threads():
    assert 'event_runtime.active_thread.advance()' in HOME_FRONT.split(
        "label story_becky_home_arrival_0:", 1
    )[1].split('label BeckyHomeFront(', 1)[0]
    assert 'threads["beckyHome"].advanceTo(2, force_active=True)' in HOME + SEX
    invite = TOPICS.split("label story_becky_home_invite_talk_0", 1)[1].split(
        "label story_becky_talk_pregnancy_0", 1
    )[0]
    assert 'event_runtime.active_thread.advance()' in invite

    assert 'threads["beckyDinner"].advanceTo(1, force_active=True)' in DINNER
    assert 'threads["beckyDinner"].advanceTo(2, force_active=True)' in DINNER
    assert 'event_runtime.active_thread.advanceTo(4, force_active=True)' in EDDIE_SCENE
    assert 'event_runtime.active_thread.complete()' in CHURCH
    assert 'threads["beckySherwoodTrade"].complete()' in SHERWOOD


def test_becky_eddie_abort_and_sherwood_handoff_use_thread_lifecycle():
    advice_thread = RUNTIME.split('LThreadData(0, "becky", "GerhardAdvice"', 1)[1].split(
        'LThreadData(0, "becky", "EddieSex"', 1
    )[0]
    eddie_thread = RUNTIME.split('LThreadData(0, "becky", "EddieSex"', 1)[1].split(
        'LThreadData(0, "becky", "IngaLucasPath"', 1
    )[0]
    sherwood_thread = RUNTIME.split('LThreadData(0, "becky", "SherwoodTrade"', 1)[1].split(
        "define tavernThreadList", 1
    )[0]

    assert '"beckySandraKitchenVisitDone"' in advice_thread
    assert '"beckyGerhardAdviceEnabled"' in advice_thread
    assert '"beckySandraKitchenVisitDone"' in eddie_thread
    assert '"beckyGerhardAdviceDone"' in eddie_thread
    assert '"beckyEddieSexDone"' in sherwood_thread
    assert EDDIE_TALK.count("event_runtime.active_thread.abort()") == 2
    assert 'threads["beckySherwoodTrade"].checkActive()' in NEXT_DAY
    assert 'threads["beckySherwoodTrade"].enable()' in NEXT_DAY


def test_kitchen_event_solely_owns_advice_transition_and_tea_availability():
    assert 'threads["beckyGerhardAdvice"].enable()' not in TOPICS
    assert KITCHEN.count('threads["beckyGerhardAdvice"].enable()') == 1
    assert "def tavern_kitchen_can_share_tea_with_sandra_and_becky" not in KITCHEN
    assert '"Угостить Сандру и Бекки бодрящим чаем":' in KITCHEN


def test_v87_rechecks_new_thread_conditions_for_untouched_old_save_stages():
    migration = MIGRATION.split("def updateSave_V87():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]
    assert "kitchen_thread.metconds = False" in migration
    assert "eddie_thread.metconds = False" in migration


def test_retired_becky_stage_fields_are_load_migration_only():
    live = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in GAME.rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    for retired_stage in (
        "home_visit_stage",
        "home_sex_unlocked",
        "open_oral_stage",
        "eddie_join_stage",
        "sandra_kitchen_friendship_progress",
        "priest_advice_stage",
        "trade_offer_stage",
    ):
        assert retired_stage not in live


def test_becky_repeat_invitation_and_husband_story_use_player_progress():
    husband = RUNTIME.split('LThreadData(0, "becky", "HusbandBackstory"', 1)[1].split(
        'LThreadData(0, "becky", "EddieBackstory"', 1
    )[0]

    assert "#int(Becky.stats.get('orgasms_given', 0) or 0) > 0" in husband
    assert "#int(threads['beckyHome'].num or 0) >= 2" in husband
    assert "sexacts" not in husband

    assert 'int(threads["beckyHome"].num or 0) >= 2' in INVITE
    assert 'Becky.stats.get("sexacts"' not in INVITE
