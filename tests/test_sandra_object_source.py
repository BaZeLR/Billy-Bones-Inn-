import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SANDRA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "InitSandra.rpy"
SANDRA_ROOM = PROJECT_ROOT / "game" / "Inn" / "TavernSandraRoom.rpy"
SANDRA_TALK = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "IntSandraTalk.rpy"
SANDRA_DRESS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "IntSandraDressChange.rpy"
SANDRA_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Sandra" / "SandraEvents.rpy"
HOUSEHOLD_SEX = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaSex.rpy"
SANDRA_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "sandra.json"
SAVE_SYNC = PROJECT_ROOT / "game" / "TractirSaveSync.rpy"
PLAYER_CHORES = PROJECT_ROOT / "game" / "Inn" / "PlayerChoresSystem.rpy"
PLAYER_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Player" / "Player.rpy"
STORY_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
THREAD_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Events" / "threads.rpy"
NEXT_DAY = PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay.rpy"
SOCIAL_TOPICS = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "SocialTalkTopics.rpy"
PEOPLE_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
HARASS_REACTION = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Common" / "PartEventGirlHarrassmentReaction.rpy"
HARASS_DISCUSS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Common" / "IntHarrassmentDiscuss.rpy"
HARASS_AFTER = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PartEventAfterHarrassment.rpy"
HARASS_CUSTOMER = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PartEventCustomerHarrassmentReaction.rpy"


def test_sandra_uses_data_info_runtime_shape():
    source = SANDRA_INIT.read_text(encoding="utf-8-sig")

    assert "class SandraData(PeopleData):" in source
    assert "class SandraInfo(Girl):" in source
    assert "define SandraStaticData = SandraData()" in source
    assert "default Sandra = SandraInfo()" in source
    assert "people.register(SandraStaticData, Sandra)" in source
    assert "register_sandra_runtime" not in source


def test_sandra_data_keeps_only_immutable_identity_references():
    source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    data_block = source.split("class SandraData(PeopleData):", 1)[1].split("class SandraInfo(Girl):", 1)[0]

    assert "code_name" in data_block
    assert "fullname=\"Сандра\"" in data_block
    assert "birth_date" in data_block
    assert "card_image" in data_block
    assert "schedule_source" in data_block
    assert "self.stats" not in data_block
    assert "self.clothing" not in data_block
    assert "self.jobs" not in data_block
    assert "self.story_defaults" not in data_block
    assert "starting_age" not in data_block
    assert 'gift_preferences=[' in data_block
    assert '"soap_001"' in data_block
    assert "self.gift_preferences" not in source


def test_sandra_custom_state_has_typed_owners_instead_of_story_map_keys():
    source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    info_block = source.split("class SandraInfo(Girl):", 1)[1]
    assert "self.knows_molodost = False" in info_block
    assert 'self.revealing_dress_code = ""' in info_block
    assert "STORY_DEFAULTS = {" not in info_block
    assert "self.uses_own_var_state" not in info_block
    assert "self.ensure_story_defaults()" not in info_block
    assert "def ensure_story_defaults(" not in info_block

    for retired_key in (
        "knowmolodost", "revealing_dress_ordered", "revealing_dress_initiative_seen",
        "MaidRevengeEnding", "MaidRevengeReason", "SecuredFuture", "SecuredFutureDay",
        "harass_instruction", "kitchen_regular_breakfast_requests", "kitchen_client_manners_requests",
        "WeeklyChoreCheckScore", "WeeklyChoreCheckCounter", "Week5WakePending",
        "WeeklyChoreCheckEval", "RoomUnlocked", "MCVisitFirstReady",
        "MCVisitFirstPending", "MCVisitFirstDone", "FinalRewardDone",
        "NightThanksReady", "NightThanksLastDay", "SandraSex",
    ):
        assert f'"{retired_key}"' not in source
    assert "def save_story_state" not in source


def test_sandra_is_instantiated_from_init_label_not_eager_init_block():
    source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    init_block = source.split("init python:", 1)[1]

    assert "people.register(SandraStaticData, Sandra)" in source
    assert "default Sandra = SandraInfo()" in source
    assert "SandraNPC" not in source
    assert "current =" not in init_block
    assert "current = Sandra(" not in init_block
    assert "peopleInfo['sandra'] = Sandra" not in init_block


def test_people_runtime_registers_class_data_without_sandra_specific_overwrite():
    runtime = (PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy").read_text(encoding="utf-8-sig")

    assert "class PeopleRegistry(object):" in runtime
    assert "runtime_object.data = static_data" in runtime
    assert '"SandraStaticData" in globals()' not in runtime
    assert 'people.register(SandraStaticData, Sandra)' not in runtime


def test_sandra_runtime_has_hidden_reaction_state_and_methods():
    source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    runtime = PEOPLE_RUNTIME.read_text(encoding="utf-8-sig")

    for token in [
        "self.energy = 100",
        "self.rebellion = 0",
        "self.anger_with_player = 0",
        "self.trust = 0",
        "self.fear = 0",
        "self.mana = 10",
        "self.mana_corrupted = False",
        "self.reaction_log = []",
        "def daily_mana_update",
        "def reaction_score",
    ]:
        assert token in source

    for retired in (
        "weekly_chore_score", "weekly_chore_counter", "weekly_chore_eval",
        "weekly_wake_pending", "room_unlocked_flag", "final_reward_flag",
        "night_thanks_ready_flag", "night_thanks_last_day",
        "weekly_thanks_event_ready", "weekly_thanks_target_label",
        "def sex_available",
    ):
        assert retired not in source

    for token in [
        "def reset_daily",
        "def mark_talked",
        "def mark_asked",
        "def mark_fucked",
        "def change_social",
        "def change_rebellion",
        "def change_anger",
        "def change_fear",
        "def change_mana",
        "def mana_bad_probability",
        "def reward_need_fulfilled",
        "def punish_need_unfulfilled",
        "def decision_profile",
        "def decide",
        "def decision_good_probability",
        "def record_reaction",
        "def last_decision_reaction",
        "def apply_decision_reaction",
        "def harass_instruction",
        "def set_harass_instruction",
    ]:
        assert token in runtime

    sandra_info_block = source.split("class SandraInfo(Girl):", 1)[1]
    for token in [
        "def reset_daily",
        "def mark_talked",
        "def mark_asked",
        "def mark_fucked",
        "def change_social",
        "def change_mana",
        "def mana_bad_probability",
        "def reward_need_fulfilled",
        "def punish_need_unfulfilled",
        "def decision_profile",
        "def decide",
        "def decision_good_probability",
        "def record_reaction",
        "def last_decision_reaction",
        "def apply_decision_reaction",
        "def change_fear",
    ]:
        assert token not in sandra_info_block


def test_sandra_story_thread_is_the_only_sex_unlock_authority():
    source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    room = SANDRA_ROOM.read_text(encoding="utf-8-sig")
    events = SANDRA_EVENTS.read_text(encoding="utf-8-sig")
    talk = SANDRA_TALK.read_text(encoding="utf-8-sig")
    sex_engine = HOUSEHOLD_SEX.read_text(encoding="utf-8-sig")

    assert "self.sandraSex" not in source
    assert "mc_visit_first_" not in source
    assert "self.weekly_wake_num" not in source
    assert "final_reward_flag" not in source
    assert 'threads["sandraWeeklyEvaluation"]' in source
    assert 'Sandra.relationship_allows("intimacy")' in room
    assert 'Sandra.relationship_allows("intimacy")' in talk
    assert 'threads["sandraWeeklyEvaluation"].completed' not in room + sex_engine + talk


def test_sandra_schedule_is_unique_and_hour_based():
    schedule = json.loads(SANDRA_SCHEDULE.read_text(encoding="utf-8-sig"))
    entries = list(schedule["entries"])
    labels = [entry["label"] for entry in entries]

    assert len(labels) == len(set(labels))
    assert all("start" in entry and "end" in entry for entry in entries)
    assert all("time_slots" not in entry for entry in entries)


def test_sandra_harassment_uses_girl_class_state_not_old_maps():
    sources = {
        "reaction": HARASS_REACTION.read_text(encoding="utf-8-sig"),
        "discuss": HARASS_DISCUSS.read_text(encoding="utf-8-sig"),
        "after": HARASS_AFTER.read_text(encoding="utf-8-sig"),
        "customer": HARASS_CUSTOMER.read_text(encoding="utf-8-sig"),
    }
    combined = "\n".join(sources.values())

    assert "people.get_info(" in combined
    assert "getPersonInfo(" not in combined
    assert ".harass_instruction()" in combined
    assert ".set_harass_instruction(" in combined
    runtime = PEOPLE_RUNTIME.read_text(encoding="utf-8-sig")
    assert 'self.harass_instruction_state = ""' in runtime
    assert 'return str(self.harass_instruction_state or "")' in runtime
    assert 'self.var["harass_instruction"]' not in runtime
    assert ".change_social(" in combined
    assert ".change_mana(" in combined
    assert ".change_rebellion(" in combined
    assert ".change_anger(" in combined
    assert ".skills[\"waitress\"]" in combined

    for forbidden in [
        "HarassInstructions",
        "sluttiness.get",
        "sluttiness[",
        "Friends.get",
        "Friends[",
        "waitress[",
    ]:
        assert forbidden not in combined


def test_sandra_dress_event_and_progress_have_single_typed_authorities():
    household = (PROJECT_ROOT / "game/Inn/HouseholdRuntimeEvents.rpy").read_text(encoding="utf-8-sig")
    kitchen = (PROJECT_ROOT / "game/Inn/TavernKitchen.rpy").read_text(encoding="utf-8-sig")
    breakfast = (PROJECT_ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
    threads_source = STORY_RUNTIME.read_text(encoding="utf-8-sig")
    progress_source = (PROJECT_ROOT / "game/Utilities/General/Common/AchievementsEndings.rpy").read_text(encoding="utf-8-sig")
    migration = SAVE_SYNC.read_text(encoding="utf-8-sig")
    live_sources = "\n".join((household, kitchen, breakfast, progress_source))

    assert 'LThreadData(0, "sandra", "RevealingDressInitiative"' in threads_source
    assert '"SandraDressInitiativeEvent"' in threads_source
    assert '"TavernKitchen"' in threads_source
    assert '"sandra_dress_initiative"' in threads_source
    conditions_source = (PROJECT_ROOT / "game/Utilities/General/Events/conditions.rpy").read_text(encoding="utf-8-sig")
    assert '"daily_events": daily_events' in conditions_source
    assert 'story_event_available("TavernKitchen", "sandra_dress_initiative")' in kitchen
    assert 'story_event_available("TavernKitchen", "sandra_dress_initiative")' in breakfast
    assert '$ threads["sandraRevealingDressInitiative"].complete()' in household
    assert 'Sandra.revealing_dress_code = dress_name' in household
    assert "sandra_revealing_dress_initiative_ready" not in live_sources
    assert "Sandra.var" not in live_sources
    assert "kitchen_regular_breakfast_requests" not in kitchen
    assert "kitchen_client_manners_requests" not in kitchen

    assert "tractir_progress.maid_revenge_ready = True" in progress_source
    assert "tractir_progress.maid_revenge_reason = str(reason or \"\")" in progress_source
    assert "tractir_progress.sandra_secured_future_day" in progress_source
    assert "Sandra.var" not in progress_source

    migration_block = migration.split("def updateSave_V49():", 1)[1].split("label before_load:", 1)[0]
    for retired_key in (
        "knowmolodost", "revealing_dress_ordered", "revealing_dress_code",
        "revealing_dress_initiative_seen", "harass_instruction", "SecuredFuture",
        "SecuredFutureDay", "MaidRevengeEnding", "MaidRevengeReason",
        "kitchen_regular_breakfast_requests", "kitchen_client_manners_requests",
    ):
        assert f'"{retired_key}"' in migration_block
    assert "initThreads()" in migration_block


def test_sandra_night_thanks_uses_current_late_night_time_contract():
    room_source = SANDRA_ROOM.read_text(encoding="utf-8-sig")
    event_source = SANDRA_EVENTS.read_text(encoding="utf-8-sig")
    story_source = STORY_RUNTIME.read_text(encoding="utf-8-sig")

    assert "int(time or 0) == 3" not in room_source
    assert '"TavernSandraRoom", "sandra_night_thanks"' in story_source
    assert "(22, 23)" in story_source
    assert "int(calendar_v2.hour or 0) < 22" in event_source
    assert "int(calendar_v2.hour or 0) > 23" in event_source


def test_sandra_sex_engine_uses_native_choices_and_pregnancy_authority_once():
    init_source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    event_source = SANDRA_EVENTS.read_text(encoding="utf-8-sig")
    engine = HOUSEHOLD_SEX.read_text(encoding="utf-8-sig")
    night_thanks = event_source.split("label TavernSandraNightThanksScene:", 1)[1]

    assert '"breakfast": {' in init_source
    assert '"flirt": ["images/sandra/thanks/sandra_thanks.webm"]' in init_source
    assert 'call HouseholdSexEngine("sandra", "TavernSandraRoom")' in night_thanks
    assert '$ calendar_v2.advance_minutes(30)' not in night_thanks
    assert 'call PregnancyCheck("sandra", "inside", 1, "Вы")' not in night_thanks
    assert 'label HouseholdSexEngine(girl_name="melissa", source_room="", initial_action="sex"):' in engine
    assert 'main_ui_begin_native_scene_state(_hse_display)' in engine
    assert '_hse_data.image_path("portrait", "default")' in engine
    assert '"Попросить помочь рукой" if _hse_full_engine' in engine
    assert '"Попросить сделать минет" if _hse_full_engine' in engine
    assert '"Кончить..." if _hse_can_cum' in engine
    assert '"Кончить в киску" if _hse_info.cock_in("pussy")' in engine
    assert '"Кончить в попку" if _hse_info.cock_in("ass")' in engine
    assert '$ pregnancy_check(_hse_girl, "tits", 1, "Вы")' in engine
    assert '$ pregnancy_check(_hse_girl, "face", 1, "Вы")' in engine
    assert '$ pregnancy_check(_hse_girl, "inside", 1, "Вы")' in engine
    assert '$ pregnancy_check(_hse_girl, "ass", 1, "Вы")' in engine
    assert '$ Sandra.mark_fucked()' not in engine
    assert '"Остановиться":' in engine
    assert '"Закончить близость":' in engine
    assert "$ main_ui_end_native_scene_state()" in engine


def test_sandra_post_sex_breakfast_talk_uses_story_thread_not_mirror_flag():
    breakfast = (PROJECT_ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
    talk_result = breakfast.split("def tavern_breakfast_talk_result():", 1)[1].split(
        "def tavern_breakfast_amanda_alt_cure_possible():", 1
    )[0]

    assert 'threads["sandraWeeklyEvaluation"].completed' in talk_result
    assert 'and "sandra" in present_ids' in talk_result
    assert 'and "amanda" in present_ids' in talk_result
    assert 'and "melissa" in present_ids' in talk_result
    assert 'talk_npc = "sandra"' in talk_result
    assert "Жить свободно и ложиться с тем, кого сами хотите, не позор" in talk_result
    assert "sandra_free_love" not in breakfast


def test_sandra_weekly_visit_uses_canonical_portraits_and_native_event_beats():
    init_source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    source = SANDRA_EVENTS.read_text(encoding="utf-8-sig")
    scene = source.split("label SandraWeeklyEvaluationScene", 1)[1].split(
        "label sandraWeeklyEvaluation_0", 1
    )[0]
    night_thanks = source.split("label TavernSandraNightThanksScene:", 1)[1]

    assert '"standing": ["images/sandra/player_room_sandra_0.jpg"]' in init_source
    assert '"leaning": ["images/sandra/thanks/player_room_1.jpg"]' in init_source
    assert '"thanks": ["images/sandra/thanks/sandra_thanks.webm"]' in init_source
    assert 'SandraStaticData.image_path("weekly_evaluation", _sandra_media_key)' in scene
    assert '("standing", "leaning", "leaning", "thanks")' in scene
    assert "main_ui_begin_native_scene_state(\"Визит Сандры\")" in scene
    assert "vscene _sandra_picture" in scene
    assert "tractir_apply_sandra_secured_future()" in scene
    assert "call TractirShowPendingAchievements" in scene
    assert "tractir_apply_sandra_secured_future()" not in night_thanks
    assert scene.count('"Продолжить":') >= 4
    assert "call ShowImage" not in scene


def test_sandra_topics_use_existing_general_topic_ids_only():
    init_source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    social_source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")

    assert '"favorite_topics": ["job_routine", "food", "money", "family_life", "fashion"]' in init_source
    assert "sandra_household" not in init_source
    assert "sandra_tavern_plan" not in init_source
    assert "sandra_burden" not in init_source
    assert "sandra_household" not in social_source
    assert "sandra_tavern_plan" not in social_source
    assert "sandra_burden" not in social_source


def test_sandra_dress_change_is_direct_action_not_refresh_dispatcher():
    dress_source = SANDRA_DRESS.read_text(encoding="utf-8-sig")
    talk_source = SANDRA_TALK.read_text(encoding="utf-8-sig")

    assert "def sandra_dress_change_can_buy" in dress_source
    assert "label IntSandraOfferBuyDress" in dress_source
    assert "label IntSandraDressChangeRefresh" not in dress_source
    assert "label IntSandraDressChangeApply" not in dress_source
    assert "label IntSandraDressChange(" not in dress_source
    assert "label int_sandra_dress_change" not in dress_source
    assert "IntSandraOfferBuyDress" in talk_source
    assert "IntSandraDressChangeApply" not in talk_source
    assert "main_ui_runtime.action_items" not in dress_source
    assert "MenuItem(" not in dress_source


def test_sandra_talk_is_direct_entry_not_refresh_apply_dispatcher():
    talk_source = SANDRA_TALK.read_text(encoding="utf-8-sig")
    dress_source = SANDRA_DRESS.read_text(encoding="utf-8-sig")
    social_source = SOCIAL_TOPICS.read_text(encoding="utf-8-sig")

    assert "label IntSandraTalk(" in talk_source
    assert "label IntSandraReconcile(" in talk_source
    assert "label IntSandraHouseholdInsight(" in talk_source
    assert "label IntSandraHouseholdPriorities(" in talk_source
    assert "label IntSandraTalkRefresh" not in talk_source
    assert "label IntSandraTalkApply" not in talk_source
    assert "label IntSandraTalkRestore" not in talk_source
    assert "call IntSandraTalkRefresh" not in talk_source
    assert '"IntSandraTalkApply"' not in talk_source
    assert '"IntSandraTalkRefresh"' not in dress_source
    assert "social_topic_return_label" not in social_source
    assert 'return "IntSandraTalkRefresh"' not in social_source
    assert "while True:" not in talk_source
    assert "jump IntSandraTalk" not in talk_source
    assert "main_ui_runtime.action_items" not in talk_source
    assert "MenuItem(" not in talk_source
    assert '"Попробовать помириться с Сандрой"' in talk_source
    assert '"Предложить купить Сандре обновку"' in talk_source
    assert "call OldPointSmallTalkMenu" not in talk_source
    assert "call OldPointFlirtAttempt" not in talk_source
    assert "call PlayerCardGiftToFixedTargetMenu" in talk_source
    assert '"Заняться сексом с Сандрой"' in talk_source
    assert 'call HouseholdSexEngine(girl_name, rooms.current_code, "sex")' in talk_source
    assert '"Попросить Сандру помочь рукой"' in talk_source
    assert 'call HouseholdSexEngine(girl_name, rooms.current_code, "handjob")' in talk_source
    assert '"Попросить Сандру сделать минет"' in talk_source
    assert 'call HouseholdSexEngine(girl_name, rooms.current_code, "blowjob")' in talk_source
    assert "call OldPointKinoAttempt" not in talk_source
    assert "call OldPointApology" not in talk_source
    assert 'if not getPersonInfo(girl_name).social_action_allowed("talk"):' not in talk_source
    assert "menu:" in talk_source
    assert "$ main_ui_end_talk_state()" in talk_source


def test_sandra_weekly_rewards_use_player_system_and_story_thread_authorities():
    init_source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    chores_source = PLAYER_CHORES.read_text(encoding="utf-8-sig")
    player_source = PLAYER_RUNTIME.read_text(encoding="utf-8-sig")
    events_source = SANDRA_EVENTS.read_text(encoding="utf-8-sig")
    room_source = SANDRA_ROOM.read_text(encoding="utf-8-sig")
    story_source = STORY_RUNTIME.read_text(encoding="utf-8-sig")
    thread_source = THREAD_RUNTIME.read_text(encoding="utf-8-sig")
    next_day_source = NEXT_DAY.read_text(encoding="utf-8-sig")

    assert "self.last_score = 0" in player_source
    assert 'self.last_evaluation = ""' in player_source
    assert "def weekly_report_finished" not in init_source
    assert "def weekly_thanks_wake_seen" not in init_source
    assert "def night_thanks_seen" not in init_source
    assert "sandra_friend=Sandra.rel" in chores_source
    assert "sandra_state={" not in chores_source
    assert "player.chores.last_score" in chores_source
    assert "player.chores.last_evaluation" in chores_source
    assert "sandra_flags=Sandra.var" not in chores_source
    assert 'sandra_thread = threads["sandraWeeklyEvaluation"]' in chores_source
    assert "sandra_thread.forceEnable()" in chores_source
    assert "mc_visit_first_" not in chores_source
    assert 'Friends["sandra"] = max(0, _pc_to_int(preview.get("sandra_friend", 0), 0))' not in chores_source
    assert 'SandraVar["WeeklyChoreCheckCounter"]' not in chores_source
    assert "Sandra.weekly_thanks_wake_seen(" not in events_source
    assert "def sandra_week5_apply_step_gains" not in events_source
    assert 'SandraVar["Week5WakePending"] = 0' not in events_source
    assert 'SandraVar["NightThanksReady"] = 1' not in events_source
    assert "Sandra.night_thanks_seen()" not in events_source
    assert 'call HouseholdSexEngine("sandra", "TavernSandraRoom")' in events_source
    sex_engine = HOUSEHOLD_SEX.read_text(encoding="utf-8-sig")
    assert '$ pregnancy_check(_hse_girl, "tits", 1, "Вы")' in sex_engine
    assert '"sandraWeeklyEvaluationEnabled"' in story_source
    assert '"TavernSandraNightThanksScene"' in story_source
    assert 'threads["sandraWeeklyEvaluation"].advance()' in events_source
    assert 'threads["sandraWeeklyEvaluation"].disable()' in events_source
    assert "def disable(self):" in thread_source
    assert 'call checkTriggers("TavernMyRoom", "sleep", 0)' in next_day_source
    assert "nextday_pick_post_sleep_event_label" not in next_day_source
    assert 'SandraVar["NightThanksReady"] = 0' not in room_source
    assert 'Friends["sandra"] = min(20, int(Friends.get("sandra", 0) or 0) + 2)' not in room_source
    assert 'self.stats["sexacts"] = people_to_int(self.stats.get("sexacts", 0), 0) + 1' not in init_source
    assert 'Sandra.stats["sexacts"] = int(Sandra.stats.get("sexacts", 0) or 0) + 1' not in events_source
    assert "apply_to_sandra_maps" not in init_source
    assert "Sandra.apply" not in chores_source
    assert "Sandra.apply" not in events_source
    assert "Sandra.apply" not in room_source


def test_sandra_object_owns_its_intimacy_unlock_and_date_capability():
    init_source = SANDRA_INIT.read_text(encoding="utf-8-sig")
    sex_source = HOUSEHOLD_SEX.read_text(encoding="utf-8-sig")
    breakfast_source = (PROJECT_ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")

    assert "def intimacy_story_ready(self):" in init_source
    assert 'thread = threads["sandraWeeklyEvaluation"]' in init_source
    assert "def relationship_allows(self, action_code=\"talk\"):" in init_source
    assert 'return self.intimacy_story_ready() and self.can_have_sex_today()' in init_source
    assert 'if girl in ("melissa", "sandra"):' in sex_source
    assert "threads[\"sandraWeeklyEvaluation\"]" not in sex_source
    date_gate = breakfast_source.split("def tavern_breakfast_private_date_available", 1)[1].split("def tavern_breakfast_player_perk_score", 1)[0]
    assert "info.date_intimacy_available()" in date_gate
    assert "sandraWeeklyEvaluation" not in date_gate
    outdoor = breakfast_source.split("label TavernKitchenBreakfastOutdoorDate", 1)[1].split("label TavernKitchenBreakfastTalkAbsent", 1)[0]
    assert '_outdoor_date_info.date_intimacy_available()' in outdoor
    assert 'call HouseholdSexEngine(_outdoor_date_girl, "ForestLake")' in outdoor
