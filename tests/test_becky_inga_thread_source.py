from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
TALK = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalk.rpy").read_text(encoding="utf-8-sig")
FRONT = (ROOT / "game/Town/BeckyHomeFront.rpy").read_text(encoding="utf-8-sig")
INGA_MORNING = (ROOT / "game/NPC/Girls/Inga/IngaGroceryMorning.rpy").read_text(encoding="utf-8-sig")
TOPICS = (ROOT / "game/NPC/Girls/Becky/IntBeckyTalkTopics.rpy").read_text(encoding="utf-8-sig")
MIGRATION = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
EVENTS = (ROOT / "game/Utilities/General/Events/events.rpy").read_text(encoding="utf-8-sig")


def test_becky_inga_discovery_and_talks_are_one_ordered_thread():
    start = RUNTIME.index('LThreadData(0, "becky", "IngaLucasPath"')
    end = RUNTIME.index('LThreadData(0, "becky", "HusbandBackstory"', start)
    thread = RUNTIME[start:end]

    for target in (
        "becky_homefront_share_with_becky",
        "story_becky_talk_inga_0",
        "story_becky_talk_inga_1",
        "story_becky_talk_lucas_0",
    ):
        assert thread.count(target) == 1
    assert '"BeckyHomeFront", "inga_discovery"' in thread
    assert "story_inga_grocery_morning_0" not in thread
    for retired in ("IngaFirstTalk", "IngaSecondTalk", "LucasTalk", "HomeFrontIngaLucas"):
        assert retired not in RUNTIME


def test_inga_grocery_encounter_has_its_own_enabled_thread():
    start = RUNTIME.index('LThreadData(0, "inga", "GroceryMorning"')
    end = RUNTIME.index("define eddieThreadList", start)
    thread = RUNTIME[start:end]

    assert thread.count("story_inga_grocery_morning_0") == 1
    assert '"ingaGroceryMorningEnabled"' in thread
    assert "threaded=True" in thread
    assert "event_runtime.active_thread.advance()" in INGA_MORNING
    assert TOPICS.count('threads["ingaGroceryMorning"].enable()') == 3
    grown_line = '"\\\"А ты заметил, что Ингенборг, доча моя, совсем большая стала?\\\" ответила вам мать семейства."'
    assert TOPICS.count(grown_line) == 3
    assert TOPICS.count(grown_line + '\n            $ threads["ingaGroceryMorning"].enable()') == 2
    assert TOPICS.count(grown_line + '\n                $ threads["ingaGroceryMorning"].enable()') == 1


def test_reachable_home_front_label_owns_the_qsp_menu_without_duplicate_copy():
    assert 'label BeckyHomeFront(arrive_mode=""):' in FRONT
    assert 'call checkTriggers("BeckyHomeFront", "inga_discovery", 0)' in FRONT
    assert "label becky_homefront_share_with_becky:" in FRONT
    assert "_becky_inga_thread.advance()" in FRONT
    assert '$ GetSexEventFromTable("inga", 99, "Lucas")' in FRONT
    assert "$ Inga.mark_known()" in FRONT
    assert "inga_scene_stage" not in FRONT
    assert "inga_scene_stage" not in RUNTIME
    assert "while True:" not in FRONT
    assert not (ROOT / "game/NPC/Girls/Becky/BeckyHomeEvents.rpy").exists()


def test_inga_talk_labels_advance_the_same_thread_without_stage_mirror():
    inga_labels = TOPICS[TOPICS.index("label story_becky_talk_inga_0"):TOPICS.index("label story_becky_talk_husband_0")]

    assert inga_labels.count("event_runtime.active_thread.advance()") == 3
    assert "event_runtime.active_thread.complete()" not in inga_labels
    assert "SawIngaFuck" not in inga_labels


def test_saw_inga_stage_is_absent_from_live_gameplay_and_migrated_once():
    live = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )
    migration = MIGRATION[MIGRATION.index("def updateSave_V24():"):]

    assert "SawIngaFuck" not in live
    assert 'becky_var.pop("SawIngaFuck", 0)' in migration
    assert 'thread_rows.get("beckyIngaLucasPath", None)' in migration
    assert "inga_thread.advanceTo(" in migration


def test_v89_repairs_only_grocery_advanced_becky_discovery_saves():
    migration = MIGRATION.split("def updateSave_V89():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]

    assert 'thread_rows.get("beckyIngaLucasPath", None)' in migration
    assert 'getattr(becky_inga_thread, "num", 0)' in migration
    assert 'getattr(Inga, "acquaintance_stage", 0)' in migration
    assert 'getattr(Inga, "saw_lucas_sex", False)' in migration
    assert "becky_inga_thread.reset()" in migration
    assert 'thread_rows.get("ingaGroceryMorning", None)' in migration
    assert "inga_morning_thread.advanceTo(" in migration


def test_home_front_has_no_synthetic_duplicate_objects():
    objects = (ROOT / "game/Town/BeckyHomeObjects.rpy").read_text(encoding="utf-8-sig")

    assert "becky_home_back_door" not in FRONT
    assert "becky_home_dark_corner" not in FRONT
    assert "GameObject(" not in objects


def test_home_front_exterior_has_no_invented_opening_hours():
    room_definition = FRONT.split("BeckyHomeFrontRoomDefinition = Room(", 1)[1].split("def show_inga_front_fuck_image", 1)[0]

    assert "schedule=" not in room_definition


def test_direct_event_availability_query_rechecks_mutated_scene_state():
    function = EVENTS.split('def story_event_available(location_name="", action_name=""):', 1)[1]
    function = function.split("def story_thread_advance_current", 1)[0]

    assert "findAvailableEvents(True)" in function
    assert "findAvailableEvents(False)" not in function


def test_becky_home_invite_preserves_qsp_topic_gate_and_internal_points():
    invite = TOPICS.split("label story_becky_home_invite_talk_0", 1)[1]
    invite = invite.split("label story_becky_talk_pregnancy_0", 1)[0]

    home_thread = RUNTIME.split('LThreadData(0, "becky", "Home"', 1)[1].split(
        'LThreadData(0, "becky", "Dinner"', 1
    )[0]
    assert 'story_event_available("talk_becky", "becky_home_invite")' in TALK
    assert '"#Becky.rel > 12"' in home_thread
    assert '"#Becky.talk_count() < 2"' in home_thread
    assert 'LThreadData(0, "becky", "HomeInviteTalk"' not in RUNTIME
    assert "_becky_husband_thread.checkActive() or int(_becky_husband_thread.num or 0) > 0" in invite
    assert 'player.appearance.has_dress("citydress")' in invite
    assert "invite_points >= 4" in invite
    assert "InvitePoints" not in invite
