from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MELISSA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "InitMelissa.rpy"
MELISSA_TALK = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaTalk.rpy"
MELISSA_DRESS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaDressChange.rpy"
MELISSA_SEX = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "IntMelissaSex.rpy"
MELISSA_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "MelissaEvents.rpy"
MELISSA_EVENT_MODEL = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Melissa" / "MelissaEventModel.rpy"
WERECAT_QUEST = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "MelissaWerecatQuest.rpy"
HOUSEHOLD_EVENTS = PROJECT_ROOT / "game" / "Inn" / "HouseholdRuntimeEvents.rpy"
MELISSA_ROOM = PROJECT_ROOT / "game" / "Inn" / "TavernMelissaRoom.rpy"
TAVERN_ATTIC = PROJECT_ROOT / "game" / "Inn" / "TavernAtic.rpy"
PEOPLE_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
GIRL_DECISION = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "GirlDecisionModel.rpy"


def test_melissa_uses_data_info_runtime_shape():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")

    assert "class MelissaData(PeopleData):" in source
    assert "class MelissaInfo(Girl):" in source
    assert "define MelissaStaticData = MelissaData()" in source
    assert "default Melissa = MelissaInfo()" in source
    assert "people.register(MelissaStaticData, Melissa)" in source
    assert "register_melissa_runtime" not in source


def test_melissa_data_keeps_identity_not_runtime_maps():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    data_block = source.split("class MelissaData(PeopleData):", 1)[1].split("class MelissaInfo(Girl):", 1)[0]

    assert "code_name = \"melissa\"" in data_block
    assert "fullname=\"Мелисса\"" in data_block
    assert "birth_date" in data_block
    assert "card_image" in data_block
    assert "schedule_source" in data_block
    assert "self.stats" not in data_block
    assert "self.jobs" not in data_block
    assert "self.wardrobe" not in data_block
    assert "self.var" not in data_block


def test_people_data_owns_shared_image_manifest_api_and_melissa_owns_its_catalog():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    data_block, info_block = source.split("class MelissaData(PeopleData):", 1)[1].split("class MelissaInfo(Girl):", 1)
    people_source = PEOPLE_RUNTIME.read_text(encoding="utf-8-sig")
    game_source = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (PROJECT_ROOT / "game").rglob("*.rpy")
    )

    assert "self.image_manifest = {" in data_block
    assert "def image_sequence(self" in people_source
    assert "def image_path(self" in people_source
    assert "def cycle_image(self" in people_source
    assert game_source.count("def image_sequence(self") == 1
    assert game_source.count("def image_path(self") == 1
    assert game_source.count("def cycle_image(self") == 1
    assert "def image_sequence(self" not in data_block
    assert "def image_path(self" not in data_block
    assert "def cycle_image(self" not in data_block
    assert "def image_sequence(self" not in info_block
    assert "def image_path(self" not in info_block
    assert "def cycle_image(self" not in info_block
    assert "Melissa.image_sequence(" not in game_source
    assert "Melissa.image_path(" not in game_source
    assert "Melissa.cycle_image(" not in game_source
    assert "MelissaStaticData.image_path(" in game_source


def test_melissa_story_state_has_explicit_npc_properties_without_var_authority():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    info_block = source.split("class MelissaInfo(Girl):", 1)[1]
    required_properties = [
        "mom_dress_complaint_count",
        "asked_about_clara_day",
        "private_context_day",
        "private_context_origin",
        "storage_thanks_day",
        "temp_room_code",
        "storage_rat_help_day",
        "bat_attic_check_day",
        "drawings_found",
        "drawings_booklet_left",
        "drawings_booklet_read",
        "drawings_returned",
        "roof_repair_complete_day",
        "breakfast_tease_day",
    ]

    for property_name in required_properties:
        assert f"self.{property_name} =" in source

    assert "STORY_DEFAULTS = {" not in info_block
    assert "self.var =" not in info_block
    assert "self.ensure_story_defaults()" not in info_block
    assert "def ensure_story_defaults(" not in info_block
    assert "try:" not in info_block
    assert "except" not in info_block

    for retired_key in (
        "RoomProblemAskDay",
        "AtticFindingsDay",
        "bat_recipe_clue_seen",
        "bats_episode",
        "ratKilled",
        "AskedMCToSolveRoomProblem",
        "bats_completed",
        "room_returned",
        "sex_engine_unlocked",
        "drawings_booklet_taken",
        "drawings_booklet_opened",
        "drawings_spy_option_unlocked",
        "bat_recipe_unlocked",
        "private_context_place",
        "private_place_heat",
        "sex_times_today",
        "room_pests_last_help_day",
        "bats_completion_day",
    ):
        assert f'"{retired_key}"' not in source


def test_melissa_live_runtime_has_no_var_map_reads_or_writes():
    game_root = PROJECT_ROOT / "game"
    runtime_source = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in game_root.rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    assert "Melissa.var" not in runtime_source
    assert "Melissa.set_var" not in runtime_source
    assert "Melissa.var_int" not in runtime_source


def test_melissa_save_migration_consumes_legacy_map_once():
    migration = (PROJECT_ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    block = migration.split("def updateSave_V50():", 1)[1].split("label before_load:", 1)[0]

    for legacy_key in (
        "MomDressComplaint", "AskedAboutClaraDay", "StartDay", "StartCount", "StartTotal",
        "private_context_day", "private_context_origin", "StorageThanksDay", "temp_room",
        "storage_rat_cleared", "storage_rat_last_help_day", "bat_attic_check_day",
        "drawings_ready_day", "drawings_found", "drawings_booklet_left",
        "drawings_booklet_read", "drawings_returned", "roof_repair_order_day",
        "roof_repair_complete_day", "breakfast_tease_day", "work_attitude",
    ):
        assert f'"{legacy_key}"' in block
    assert "def updateSave_V50():" in migration
    assert "if loaded_version < 51:" in migration
    assert "updateSave_V50()" in migration
    for retired_field in (
        "intimacy_start_day", "intimacy_start_count", "intimacy_start_total", "drawings_ready_day",
    ):
        assert f'self.{retired_field} =' not in MELISSA_INIT.read_text(encoding="utf-8-sig")
        assert f'"{retired_field}"' in migration


def test_melissa_revealing_dress_request_is_thread_owned_and_code_backed():
    init_source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    household = HOUSEHOLD_EVENTS.read_text(encoding="utf-8-sig")
    story = (PROJECT_ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    tavern_main = (PROJECT_ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    breakfast = (PROJECT_ROOT / "game/Inn/TavernKitchenBreakfast.rpy").read_text(encoding="utf-8-sig")
    migration = (PROJECT_ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert 'self.revealing_dress_code = ""' in init_source
    assert 'LThreadData(0, "melissa", "RevealingDressRequest"' in story
    assert story.count('"MelissaDressRequestEvent"') >= 2
    assert '"TavernMain", "melissa_dress_request"' in story
    assert '"TavernKitchen", "melissa_dress_request"' in story
    assert 'Melissa.revealing_dress_code = dress_name' in household
    assert '$ threads["melissaRevealingDressRequest"].complete()' in household
    assert "melissa_revealing_dress_request_ready" not in household + tavern_main + breakfast
    assert 'story_event_available("TavernMain", "melissa_dress_request")' in tavern_main
    assert 'story_event_available("TavernKitchen", "melissa_dress_request")' in breakfast
    for retired_key in ("revealing_dress_ordered", "revealing_dress_request_seen"):
        assert f'Melissa.var.get("{retired_key}"' not in household
        assert f'Melissa.var["{retired_key}"]' not in household

    migration_block = migration.split("def updateSave_V49():", 1)[1].split("label before_load:", 1)[0]
    assert 'Melissa.revealing_dress_code = ""' in migration_block
    assert 'melissa_var.pop("revealing_dress_ordered", None)' in migration_block
    assert 'melissa_var.pop("revealing_dress_request_seen", 0)' in migration_block
    assert 'threads.get("melissaRevealingDressRequest", None)' in migration_block


def test_melissa_recipe_unlock_has_one_recipe_book_authority():
    init_source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    event_source = MELISSA_EVENTS.read_text(encoding="utf-8-sig")
    recipe_source = (PROJECT_ROOT / "game" / "Items" / "Core" / "CraftingRecipes.rpy").read_text(encoding="utf-8-sig")
    craft_source = (PROJECT_ROOT / "game" / "Items" / "Crafting" / "SoapCraftAndAtticItems.rpy").read_text(encoding="utf-8-sig")

    assert 'recipe_book_item_state()["hidden_recipes_revealed"] = True' in recipe_source
    assert "unlock_condition=recipe_book_hidden_recipes_revealed" in craft_source
    assert "bat_recipe_unlocked" not in init_source
    assert "bat_recipe_unlocked" not in event_source
    assert "Melissa.bat_repellent_recipe_unlocked" not in craft_source

    migration_source = (PROJECT_ROOT / "game" / "TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    migration_block = migration_source.split("def updateSave_V48():", 1)[1].split("label before_load:", 1)[0]
    for retired_key in (
        "bat_recipe_unlocked", "private_context_place", "private_place_heat", "sex_times_today",
        "room_pests_last_help_day", "bats_completion_day",
    ):
        assert f'"{retired_key}"' in migration_block


def test_melissa_room_uses_thread_events_without_disabled_pests_duplicate():
    room_source = MELISSA_ROOM.read_text(encoding="utf-8-sig")
    household_source = HOUSEHOLD_EVENTS.read_text(encoding="utf-8-sig")

    assert "call RoomEnterEventGate(rooms.current_code, False)" in room_source
    assert "tavern_melissa_room_pests_event_ready" not in room_source
    assert "tavern_melissa_room_pests_event_ready" not in household_source
    assert "label MelissaRoomPestsEvent" not in household_source


def test_melissa_info_owns_runtime_defaults_without_legacy_sync():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    runtime = PEOPLE_RUNTIME.read_text(encoding="utf-8-sig")

    for token in [
        "self.rel = 5",
        "self.openness = 0",
        "self.corruption = 3",
        "self.energy = 100",
        "self.mana = 10",
        "self.talked_today = 0",
        "self.flirted_today = 0",
        "self.gifted_today = 0",
        "self.asked_today = 0",
        "self.fucked_today = 0",
        "self.drunk = 0",
        "\"beauty\": 55",
        "\"ConceptionChance\": 15",
        "\"PussyWetStart\": 10",
        "\"virginity\": True",
        "\"cooking\": 30",
        "\"cleaning\": 40",
        "\"waitress\": 30",
        "\"jobcleaning\": 1",
        "\"jobwaitress\": 1",
    ]:
        assert token in source

    for token in [
        "def sync_from_melissa_maps",
        "def sync_melissa_maps",
        "Melissa.var =",
        "MelissaVar",
        "sync_room_problem_state",
    ]:
        assert token not in source

    for token in [
        "def reset_daily",
        "def mana_bad_probability",
        "def reward_need_fulfilled",
        "def punish_need_unfulfilled",
        "def decision_profile",
        "def decide",
        "def decision_good_probability",
        "def record_reaction",
        "def last_decision_reaction",
        "def apply_decision_reaction",
    ]:
        assert token in runtime

    melissa_info_block = source.split("class MelissaInfo(Girl):", 1)[1]
    for token in [
        "def decision_profile",
        "def decide",
        "def decision_good_probability",
        "def record_reaction",
        "def last_decision_reaction",
        "def apply_decision_reaction",
    ]:
        assert token not in melissa_info_block

    decision_source = GIRL_DECISION.read_text(encoding="utf-8-sig")
    for token in [
        'GIRL_DECISION_CORE_IDS = ("amanda", "melissa", "sandra")',
        "girl_info = people.get_info(girl)",
        "girl in GIRL_DECISION_CORE_IDS",
        '"mana_bad_probability": girl_info.mana_bad_probability()',
        "in GIRL_DECISION_CORE_IDS:",
    ]:
        assert token in decision_source


def test_melissa_has_five_valid_favorite_talk_topics():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")

    assert '"favorite_topics": ["job_routine", "family_life", "forest", "stories", "food"]' in source
    assert '"clothes"' not in source


def test_melissa_talk_keeps_native_flow_and_room_problem_choices_reachable():
    talk_source = MELISSA_TALK.read_text(encoding="utf-8-sig")
    household_source = HOUSEHOLD_EVENTS.read_text(encoding="utf-8-sig")

    talk_menu = talk_source.split('label IntMelissaTalk(girl_name="melissa"):', 1)[1].split("label IntMelissaStartMenu", 1)[0]
    assert "while True:" not in talk_menu
    assert '"Обсудить, где Мелиссе переночевать" if melissa_room_problem_available():' in talk_source
    assert "call IntMelissaRoomProblemAdviceMenu(girl_name)" in talk_source
    assert 'label IntMelissaRoomProblemAdviceMenu(girl_name="melissa"):' in talk_source
    assert '"Предложить пока ночевать у вас":' in talk_source
    assert '"Предложить перебраться к Аманде":' in talk_source
    assert '"Предложить занять пустую комнату":' in talk_source
    assert "if _melissa_talk_new:" in talk_menu
    assert "jump IntMelissaTalk" not in talk_menu
    assert talk_menu.rstrip().endswith("return")
    assert "jump IntMelissaStartMenu" not in talk_source
    assert "call OldPointSmallTalkMenu" not in talk_menu
    assert "call OldPointFlirtAttempt" not in talk_menu
    assert "call PlayerCardGiftToFixedTargetMenu(girl_name)" in talk_menu
    assert "call OldPointKinoAttempt" not in talk_menu
    assert "call OldPointApology" not in talk_menu
    assert "call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)" in talk_menu
    assert "Melissa.change_social(friend_delta=6" not in talk_menu
    assert "RoomProblemAskDay" not in talk_source
    assert "and stage == 3" in household_source
    assert 'and temp_room == ""' in household_source


def test_melissa_custom_relationship_and_intimacy_policy_is_object_owned():
    init_source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    talk_source = MELISSA_TALK.read_text(encoding="utf-8-sig")
    sex_source = MELISSA_SEX.read_text(encoding="utf-8-sig")

    for method_name in (
        "relationship_stage",
        "intimacy_story_ready",
        "relationship_allows",
        "room_is_private",
        "private_place_offer",
    ):
        assert f"def {method_name}(self" in init_source
        assert f"def melissa_{method_name}(" not in talk_source
    for removed_parallel_flow in (
        "start_action_available",
        "start_scene_count",
        "start_scene_remaining",
        "start_intro_text",
        "IntMelissaStartMenu",
    ):
        assert removed_parallel_flow not in init_source + talk_source
    assert 'and threads["melissaCourtship"].completed' in init_source
    assert 'self.intimacy_story_ready()' in init_source
    assert 'self.can_have_sex_today()' in init_source
    assert '_hse_info.can_have_sex_today()' in sex_source
    assert '_hse_daily_limit' not in sex_source
    assert 'Melissa.relationship_allows("intimacy")' in talk_source
    assert "Melissa.private_place_offer(" in talk_source
    assert 'story_event_available("talk_melissa", "melissa_intimacy")' not in talk_source
    assert 'call checkTriggers("talk_melissa", "melissa_intimacy", 0)' not in talk_source
    invite_branch = talk_source.split('"Попросить Мелиссу прийти завтра на общий завтрак"', 1)[1]
    assert '$ _melissa_repeat_menu = True' in invite_branch.split('"Обсудить, где Мелиссе переночевать"', 1)[0]
    intimacy_call = talk_source.split('call HouseholdSexEngine(girl_name, rooms.current_code)', 1)[1]
    assert intimacy_call.split("\n", 2)[1].strip() == "return"
    assert 'return bool(info.relationship_allows(action_code))' in sex_source
    assert '$ _hse_info.mark_fucked()' in sex_source
    assert 'if int(player.intimacy.came_today or 0) == _hse_start_player_cums:' in sex_source


def test_melissa_courtship_is_one_ordered_story_thread_without_parallel_counters():
    runtime_source = (PROJECT_ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    event_source = MELISSA_EVENTS.read_text(encoding="utf-8-sig")
    runtime_courtship = runtime_source.split('LThreadData(0, "melissa", "Courtship"', 1)[1].split(
        'LThreadData(0, "melissa", "RatProblem"', 1
    )[0]
    courtship_block = event_source.split("label story_melissa_courtship_amanda_talk_0:", 1)[1].split(
        "label event_melissa_waitress_fall", 1
    )[0]

    assert 'LThreadData(0, "melissa", "Courtship"' in runtime_source
    assert '"talk_melissa", "melissa_intimacy", 0' not in runtime_source
    assert runtime_courtship.count('"TavernMyRoom", "sleep", 0') == 4
    assert runtime_source.count("None, None, 1,") >= 4
    for stage_label in (
        "story_melissa_courtship_amanda_talk_0",
        "story_melissa_courtship_storm_1",
        "story_melissa_courtship_mutual_2",
        "story_melissa_courtship_touch_him_3",
        "story_melissa_courtship_taste_4",
    ):
        assert f"label {stage_label}:" in event_source
    assert courtship_block.count("$ event_runtime.active_thread.advance()") == 5
    assert "$ Melissa.mark_fucked()" not in courtship_block
    assert "#Liza.is_working()" in runtime_source
    assert "#int(Amanda.var_int('lizafriends', 0)) > 0" in runtime_source
    assert "#int(Amanda.sex_stat('sexacts', 0) or 0) > 0" in runtime_source
    for retired_counter in ("intimacy_start_day", "intimacy_start_count", "intimacy_start_total"):
        assert retired_counter not in runtime_source + event_source


def test_melissa_courtship_save_upgrade_promotes_only_recorded_sex_history():
    migration_source = (PROJECT_ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    migration = migration_source.split("def updateSave_V69():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 82" in migration_source
    assert 'courtship = threads["melissaCourtship"]' in migration
    assert 'Melissa.sex_stat("sexacts", 0)' in migration
    assert "courtship.advanceTo(courtship.data.length, complete_at_end=True)" in migration
    assert "Melissa.rel" not in migration
    assert "Melissa.openness" not in migration
    assert "Melissa.corruption" not in migration


def test_melissa_intimacy_uses_one_native_scene_until_explicit_finish():
    sex_source = MELISSA_SEX.read_text(encoding="utf-8-sig")
    sex_menu = sex_source.split('label HouseholdSexEngine(girl_name="melissa", source_room="", initial_action="sex"):', 1)[1].split(
        'label HouseholdSexState(girl_name="melissa", full_engine=False):', 1
    )[0]

    assert 'main_ui_begin_native_scene_state(_hse_display)' in sex_menu
    assert "while True:" in sex_menu
    assert '"Остановиться":' in sex_menu
    assert "call HouseholdSexFinish" in sex_menu
    assert 'vscene scene_runtime.picture' in sex_menu
    assert '"[scene_runtime.text]"' not in sex_menu
    assert "call ShowCurrentSex" not in sex_menu
    assert "main_ui_end_native_scene_state()" in sex_source


def test_melissa_intimacy_refresh_does_not_reset_arousal_or_proxy_owned_state():
    source = MELISSA_SEX.read_text(encoding="utf-8-sig")

    for helper_name in (
        "_ims_player_cum_count",
        "_ims_player_cum_limit",
        "_ims_set_arousal",
        "_ims_arousal",
        "_ims_prepare_scene_state",
        "_ims_clear_contact_states",
        "_ims_set_inserted_container",
        "_ims_current_inserted_container",
    ):
        assert helper_name not in source
    assert 'Melissa.set_arousal(int(Melissa.stats.get("PussyWetStart"' not in source
    assert "player.intimacy.arousal_value()" in source
    assert "_hse_info.arousal_value()" in source


def test_melissa_werecat_event_labels_own_their_scenes_and_thread_advancement():
    event_source = MELISSA_EVENTS.read_text(encoding="utf-8-sig")
    werecat_source = WERECAT_QUEST.read_text(encoding="utf-8-sig")

    intro_block = event_source.split("label story_melissa_werecat_intro_0:", 1)[1].split("\nlabel ", 1)[0]
    assert 'vscene MelissaStaticData.image_path("bats", "sleepless")' in intro_block
    assert 'vscene MelissaStaticData.image_path("bats", "yawns")' in intro_block
    assert 'vscene "images/kitchen/need_kitty_1.png"' in intro_block
    assert 'vscene "images/kitchen/need_kitty_2.png"' in intro_block
    assert intro_block.index('"sleepless"') < intro_block.index('"yawns"')
    assert intro_block.index('"yawns"') < intro_block.index("need_kitty_1.png")
    assert intro_block.index("need_kitty_1.png") < intro_block.index("need_kitty_2.png")
    assert intro_block.count('"Продолжить":') == 4
    assert '"Закончить завтрак":' in intro_block
    assert '"rat_breakfast_seen"' not in intro_block
    assert "vscene tavern_kitchen_breakfast_picture()" not in intro_block

    for label_name in (
        "story_melissa_werecat_home_0",
        "story_melissa_werecat_home_1",
    ):
        block = event_source.split(f"label {label_name}:", 1)[1].split("\nlabel ", 1)[0]
        assert "vscene tavern_kitchen_breakfast_picture()" in block
        assert "event_runtime.active_thread.advance()" in block
    for wrapper_name in (
        "MelissaRatBreakfastScene",
        "WerecatAdoptionBreakfastScene",
        "WerecatMonthThanksScene",
    ):
        assert f"call {wrapper_name}" not in event_source
        assert f"label {wrapper_name}:" not in werecat_source


def test_werecat_intro_thread_stage_is_the_only_breakfast_progress_owner():
    runtime_source = (PROJECT_ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    owner_source = (PROJECT_ROOT / "game/NPC/Secondary/WerecatNPC.rpy").read_text(encoding="utf-8-sig")
    migration_source = (PROJECT_ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    thread_block = runtime_source.split('LThreadData(0, "melissa", "WerecatProblem", None, [', 1)[1].split(
        "    ], highlight=False, threaded=True),", 1
    )[0]

    assert thread_block.index('"story_melissa_werecat_intro_0"') < thread_block.index('"story_melissa_werecat_rumor_0"')
    assert '"TavernKitchen"' in thread_block
    assert '"HunterClub"' in thread_block
    assert '"rat_breakfast_seen"' not in runtime_source
    assert '"rat_breakfast_seen"' not in owner_source
    assert 'state.pop("rat_breakfast_seen", None)' in migration_source


def test_melissa_bat_breakfast_has_one_authored_finish_and_no_second_hub():
    source = MELISSA_EVENTS.read_text(encoding="utf-8-sig")
    scene = source.split("label story_melissa_bat_problem_0:", 1)[1].split(
        "label story_melissa_bat_problem_1:", 1
    )[0]

    assert 'main_ui_begin_native_scene_state("Завтрак: летучие мыши")' in scene
    assert scene.count('"Продолжить":') >= 6
    assert scene.count('"Закончить завтрак":') == 1
    assert scene.count("call TavernKitchenFinishBreakfastEvent") == 1
    assert "call TavernKitchenBreakfastMenu" not in scene
    assert '"[scene_runtime.text]"' not in scene
    assert "event_runtime.active_thread.advance()" in scene
    assert "main_ui_end_native_scene_state()" in scene


def test_melissa_dress_action_does_not_open_a_duplicate_menu():
    talk_source = MELISSA_TALK.read_text(encoding="utf-8-sig")
    dress_source = MELISSA_DRESS.read_text(encoding="utf-8-sig")

    assert '"Предложить купить Мелиссе обновку" if' in talk_source
    assert "call IntMelissaDressChange(girl_name)" in talk_source
    assert "menu:" not in dress_source
    assert '"Назад":' not in dress_source
    assert "daily_events.add(" in dress_source


def test_melissa_room_time_logic_uses_hour_schedule_not_display_slots():
    household_source = HOUSEHOLD_EVENTS.read_text(encoding="utf-8-sig")
    room_source = MELISSA_ROOM.read_text(encoding="utf-8-sig")

    assert "calendar_v2.time_slot()" not in household_source.split("def melissa_room_problem_available():", 1)[1].split("def melissa_temp_room_text():", 1)[0]
    assert "int(calendar_v2.hour or 0) >= 16" in household_source
    assert 'not people.is_awake("melissa")' in room_source
    assert "calendar_v2.time_slot()" not in room_source


def test_melissa_room_object_menu_has_no_unused_text_dispatcher():
    room_source = MELISSA_ROOM.read_text(encoding="utf-8-sig")

    assert "def tavern_melissa_room_text():" in room_source
    assert "TavernMelissaRoomObjectText" not in room_source
    assert '_room_action.hook == "text"' not in room_source
    assert room_source.count("tavern_melissa_room_text()") >= 3


def test_melissa_uses_common_relationship_mutator_without_alias_methods():
    init_source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    event_source = MELISSA_EVENTS.read_text(encoding="utf-8-sig")
    werecat_source = WERECAT_QUEST.read_text(encoding="utf-8-sig")

    assert "def add_trust(" not in init_source
    assert "def add_openness(" not in init_source
    assert "Melissa.add_trust(" not in event_source + werecat_source
    assert "Melissa.add_openness(" not in event_source + werecat_source
    assert "Melissa.change_social(" in event_source


def test_melissa_attic_actions_have_one_event_owned_path():
    attic_source = TAVERN_ATTIC.read_text(encoding="utf-8-sig")

    assert 'story_event_available("TavernAtic", "melissa_bats")' in attic_source
    assert 'Call("checkTriggers", "TavernAtic", "melissa_bats", 0)' in attic_source
    for dead_label in (
        "MelissaAtticColonySearch",
        "MelissaAtticWindowPeek",
        "MelissaBurnAtticColony",
        "MelissaOrderRoofRepair",
        "MelissaCheckRoofRepair",
    ):
        assert f"label {dead_label}:" not in attic_source


def test_melissa_removed_hidden_conditional_class_registration():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")

    assert "class Melissa(Girl):" not in source
    assert "isinstance(peopleInfo.get('melissa'), Melissa)" not in source
    assert "peopleInfo['melissa'] = Melissa" not in source
    assert "dir()" not in source
    assert "globals()" not in source
    assert "renpy.store" not in source
    assert "calendar_make_birth_record" not in source


def test_melissa_bat_progress_uses_the_story_thread_directly():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")

    assert "def bats_stage(self):" not in source
    assert 'threads["melissaBatProblem"].num' in source
    assert '_story_thread_lookup("melissaBatProblem")' not in source
    assert 'self.var["bats_episode"]' not in source


def test_melissa_temporary_bed_does_not_replace_day_schedule():
    source = MELISSA_INIT.read_text(encoding="utf-8-sig")
    temp_room = source.split("def temp_room_active(self", 1)[1].split(
        "def attic_scandal_ready", 1
    )[0]

    assert 'return scheduled_room == "TavernMelissaRoom"' in temp_room
    assert "return hour_num < 10" not in temp_room


def test_melissa_booklet_aftermath_is_one_ordered_thread_flow():
    runtime_source = (PROJECT_ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(encoding="utf-8-sig")
    event_source = MELISSA_EVENTS.read_text(encoding="utf-8-sig")
    event_model_source = MELISSA_EVENT_MODEL.read_text(encoding="utf-8-sig")
    talk_source = MELISSA_TALK.read_text(encoding="utf-8-sig")
    amanda_room_source = (PROJECT_ROOT / "game/Inn/TavernAmandaRoom.rpy").read_text(encoding="utf-8-sig")
    migration_source = (PROJECT_ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    bat_thread = runtime_source.split('LThreadData(0, "melissa", "BatProblem"', 1)[1].split('], highlight=False, threaded=True)', 1)[0]
    ordered_labels = (
        "story_melissa_bat_problem_breakfast_invite",
        "story_melissa_bat_problem_breakfast_argument",
        "story_melissa_bat_problem_5",
        "story_melissa_bat_problem_booklet_search",
        "story_melissa_bat_problem_6",
    )
    positions = [bat_thread.index(label) for label in ordered_labels]
    assert positions == sorted(positions)
    assert '"talk_melissa",\n                "melissa_breakfast_invite"' in bat_thread
    breakfast_invite = bat_thread.split(
        '"story_melissa_bat_problem_breakfast_invite"', 1
    )[1].split('"melissa_breakfast_invite"', 1)[0]
    assert "rooms.current_code" not in breakfast_invite
    assert '"TavernKitchen",\n            "enter"' in bat_thread
    assert '"TavernAmandaRoom",\n            "melissa_bats"' in bat_thread
    assert '"Попросить Мелиссу прийти завтра на общий завтрак"' in talk_source
    assert 'call checkTriggers(rooms.current_code, "melissa_talk", 0)' in talk_source
    assert "tavern_amanda_room_locked_for_melissa_booklet" not in amanda_room_source
    assert 'LThreadData(0, "melissa", "AmandaRoomShare"' in runtime_source
    assert "MelissaAmandaRoomShare," in runtime_source
    assert "class MelissaAmandaRoomShareEvent(Event):" in event_model_source
    assert '"TavernAmandaRoom"' in event_model_source
    assert '"melissa_amanda_locked"' in event_model_source
    assert "self.repeatable = True" in event_model_source
    assert 'story_event_available("TavernAmandaRoom", "melissa_amanda_locked")' in amanda_room_source
    assert 'call checkTriggers("TavernAmandaRoom", "melissa_amanda_locked", 0)' in amanda_room_source
    assert "label story_melissa_amanda_room_locked:" in event_source
    assert "Дверь заперта изнутри" in event_source
    assert "breakfast_invited" not in runtime_source + event_source + migration_source
    assert "def updateSave_V72():" in migration_source
