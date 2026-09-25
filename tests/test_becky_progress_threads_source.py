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
FINISH_DAY = (GAME / "Utilities/Time/NextDay_FinishDayEvents.rpy").read_text(encoding="utf-8-sig")
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

    assert '"beckySandraKitchenVisitDone"' not in advice_thread
    assert '"beckyGerhardAdviceEnabled"' in advice_thread
    eddie_base_conditions, eddie_events = eddie_thread.split("], [", 1)
    first_join_event = eddie_events.split('"BeckyEddieJoinFirst"', 1)[1].split(
        '"IntEddieTalkMomHelper"', 1
    )[0]
    assert '"beckySandraKitchenVisitDone"' in eddie_base_conditions
    assert '"beckyGerhardAdviceDone"' not in eddie_base_conditions
    assert '"beckyGerhardAdviceDone"' in first_join_event
    assert '"beckyEddieSexDone"' in sherwood_thread
    retry = EDDIE_TALK.split('if int(Eddie.rel or 0) < 10:', 1)[1].split(
        'elif Becky.eddie_join_failures > 2:', 1
    )[0]
    terminal_refusal = EDDIE_TALK.split('elif Becky.eddie_join_failures > 2:', 1)[1].split(
        'else:', 1
    )[0]
    assert "event_runtime.active_thread.abort()" not in retry
    assert "event_runtime.active_thread.abort()" in terminal_refusal
    assert EDDIE_TALK.count("event_runtime.active_thread.abort()") == 1
    assert 'threads["beckySherwoodTrade"].checkActive()' in NEXT_DAY
    assert 'threads["beckySherwoodTrade"].enable()' in NEXT_DAY


def test_finish_day_does_not_advance_unseen_becky_story_events():
    priest = FINISH_DAY.split('elif place == "Priest":', 1)[1].split(
        'elif girl == "becky":', 1
    )[0]

    assert 'pregnancy_check(girl, "inside", 1, "Отец Герхард")' in priest
    assert 'threads["beckyGerhardAdvice"]' not in priest
    assert 'threads["beckyEddieSex"]' not in priest
    assert "becky_advice_thread" not in priest
    assert "becky_eddie_thread" not in priest


def test_kitchen_event_distinguishes_tea_from_the_story_advancing_tincture():
    visit_thread = RUNTIME.split('LThreadData(0, "becky", "SandraKitchenVisit"', 1)[1].split(
        'LThreadData(0, "becky", "Home"', 1
    )[0]
    tea_branch = KITCHEN.split(
        '"Угостить Сандру и Бекки бодрящим чаем" if int(player.item_count("energy_tea_001") or 0) > 0:',
        1,
    )[1].split('"Подать горячую медовую настойку"', 1)[0]
    tincture_branch = KITCHEN.split(
        '"Подать горячую медовую настойку" if int(player.item_count("libido_tincture_001") or 0) > 0:',
        2,
    )[2].split('"Не мешать разговору":', 1)[0]

    assert 'threads["beckyGerhardAdvice"].enable()' not in TOPICS
    assert KITCHEN.count('threads["beckyGerhardAdvice"].enable()') == 1
    assert "def tavern_kitchen_can_share_tea_with_sandra_and_becky" not in KITCHEN
    assert "energy_tea_001" not in visit_thread
    assert "libido_tincture_001" not in visit_thread

    assert 'player.remove_item("energy_tea_001", 1)' in tea_branch
    assert 'vscene "images/tavern/kitchen/becky_visit_1.png"' not in tea_branch
    assert 'threads["beckyGerhardAdvice"].enable()' not in tea_branch
    assert "_becky_sandra_visit_thread.complete()" not in tea_branch

    assert 'tavern_kitchen_spicy_tincture_apply(("sandra", "becky"))' in tincture_branch
    assert 'call BeckySandraTipsyKitchenTalk' in tincture_branch
    assert 'vscene "images/tavern/kitchen/becky_visit_1.png"' in KITCHEN.split('label BeckySandraTipsyKitchenTalk:', 1)[1]
    assert "Эдди давно" in tincture_branch
    assert "здоровом доме" in tincture_branch
    assert "для хозяйства, и для торговли" in tincture_branch
    assert 'threads["beckyGerhardAdvice"].enable()' in tincture_branch
    assert "_becky_sandra_visit_thread.complete()" in tincture_branch


def test_dinner_bedroom_acceptance_uses_the_requested_fifty_percent_decision():
    dinner_decision = DINNER.split(
        'elif not threads["beckyEddieSex"].completed:',
        1,
    )[1].split('"Идти в спальню вместе с Бекки и Эдди"', 1)[0]

    assert 'int(threads["beckyDinner"].num or 0) >= 2' in dinner_decision
    assert 'procedural_randint(1, 2, "becky_dinner_bed_decision_%s" % int(current_game_day() or 0)) == 1' in dinner_decision
    assert "Becky.corruption + procedural_randint" not in dinner_decision
    assert 'call BeckyHome("FromDinner")' in dinner_decision


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
