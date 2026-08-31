from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AMANDA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmanda.rpy"
AMANDA_LEGARE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaLegareDanceSequence.rpy"
AMANDA_DANCE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "IntAmandaDance.rpy"
AMANDA_DRESS_CHANGE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "IntAmandaDressChange.rpy"
AMANDA_DANCE_EVENT_MODEL = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaDanceEventModel.rpy"
AMANDA_EVENT_MODEL = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaEventModel.rpy"
AMANDA_AFTER_DANCE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaSexDanceStreet.rpy"
AMANDA_STREET_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaLegareStreetEvents.rpy"
AMANDA_PORTRAIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "ShowAmandaPortrait.rpy"
MAIN_LAYOUT = PROJECT_ROOT / "game" / "Utilities" / "General" / "Screens" / "main_layout.rpy"
GIRL_CARD = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Common" / "GirlCard.rpy"
AMANDA_LIZA_GLORY_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaLizaGloryEvents.rpy"
AMANDA_LIZA_TALK_ITEMS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmandaLizaTalkItems.rpy"
AMANDA_AT_GLORY_HOLE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaAtGloryHole.rpy"
AMANDA_PREGNANCY_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaPregnancyEvents.rpy"
AMANDA_AT_HOME = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaAtHomeCode.rpy"
AMANDA_AFTER_LEGARE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AfterDanceLegare.rpy"
AMANDA_AFTER_LEGARE_SEX = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AfterDanceSexLegare.rpy"
SECONDARY_INIT = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "InitSecondaryNPC.rpy"
ALBER_INIT = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "InitAlber.rpy"
ALBER_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "alber.json"
ALBER_TALK = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "IntAlberTalk.rpy"
NEXT_DAY_NEW_EVENTS = PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay_NewDayEvents.rpy"
NEXT_DAY_FINISH_EVENTS = PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay_FinishDayEvents.rpy"
FRIDAY_DANCE = PROJECT_ROOT / "game" / "Town" / "Market" / "FridayDance.rpy"
STORY_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
TAVERN_RANDOM_EVENTS = PROJECT_ROOT / "game" / "Inn" / "TavernRandomEvents.rpy"
TAVERN_GLORY_HOLE = PROJECT_ROOT / "game" / "Inn" / "TavernGloryHole.rpy"
TAVERN_AMANDA_ROOM = PROJECT_ROOT / "game" / "Inn" / "TavernAmandaRoom.rpy"
TAVERN_AMANDA_BED = PROJECT_ROOT / "game" / "Inn" / "TavernAmandaBed001.rpy"
TAVERN_MAIN = PROJECT_ROOT / "game" / "Inn" / "TavernMain.rpy"
TAVERN_KITCHEN = PROJECT_ROOT / "game" / "Inn" / "TavernKitchen.rpy"
TAVERN_MY_ROOM = PROJECT_ROOT / "game" / "Inn" / "TavernMyRoom.rpy"
TAVERN_STORAGE = PROJECT_ROOT / "game" / "Inn" / "TavernStorage.rpy"
CHARACTER_ACTION_HUB = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "CharacterActionHub.rpy"
PEOPLE_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def test_amanda_uses_data_info_runtime_shape():
    source = _source(AMANDA_INIT)

    assert "class AmandaData(PeopleData):" in source
    assert "class AmandaInfo(Girl):" in source
    assert "define AmandaStaticData = AmandaData()" in source
    assert "default Amanda = AmandaInfo()" in source
    assert "people.register(AmandaStaticData, Amanda)" in source
    assert "default AmandaNPC" not in source


def test_amanda_portrait_path_comes_only_from_static_data():
    init_source = _source(AMANDA_INIT)
    street_events = _source(AMANDA_STREET_EVENTS)
    portrait = _source(AMANDA_PORTRAIT)
    layout = _source(MAIN_LAYOUT)
    card = _source(GIRL_CARD)

    assert 'portrait="images/amanda/amanda_portrait.jpg"' in init_source
    assert street_events.count('call ShowImage("", "", AmandaStaticData.portrait)') == 3
    assert 'call ShowImage("amanda", "", "amanda_portrait.jpg")' not in street_events
    assert '_amanda_portrait_picture = str(AmandaStaticData.portrait or "")' in portrait
    assert "candidates.append(AmandaStaticData.portrait)" in layout
    assert "else AmandaStaticData.portrait" in card


def test_amanda_data_keeps_static_identity_only():
    source = _source(AMANDA_INIT)
    data_block = source.split("class AmandaData(PeopleData):", 1)[1].split("class AmandaInfo(Girl):", 1)[0]

    assert 'code_name = "amanda"' in data_block
    assert 'fullname="Аманда"' in data_block
    assert "birth_date" in data_block
    assert "card_image" in data_block
    assert "schedule_source" in data_block
    assert "self.stats" not in data_block
    assert "self.jobs" not in data_block
    assert "self.wardrobe" not in data_block
    assert "self.var" not in data_block


def test_amanda_info_owns_runtime_state_and_story_defaults():
    source = _source(AMANDA_INIT)

    for token in [
        "self.rel = 5",
        "self.openness = 3",
        "self.corruption = 0",
        "self.mana = 10",
        "self.mana_corrupted = False",
        "self.reaction_log = []",
        "self.reaction_state = {",
        "self.mana_reaction_table = {",
        "\"beauty\": 52",
        "\"ConceptionChance\": 10",
        "\"PussyWetStart\": 0",
        "\"virginity\": True",
        "\"cooking\": 20",
        "\"cleaning\": 30",
        "\"waitress\": 15",
        "\"jobcleaning\": 1",
        "\"jobwaitress\": 1",
        "def mana_profile",
        "def reaction_score",
        "def cycle_state",
        "def fertility_state",
        "def pregnancy_state",
        "def pregnancy_check",
        "def birth_ready",
        "def apply_body_state",
        "def body_state_line",
        "def legare_intro_ready",
        "def mark_legare_intro_seen",
        "def dynamic_roll",
        "def happy_confirm_text",
        "def sex_offer_reaction",
        "def legare_sex_type",
        "def resolve_legare_let_go",
        "def nesluh_value",
        "def lover_sex_calc",
        "def yell_not_work",
        "def dress_change_other_saw_text",
        '"favorite_topics": ["fashion", "dances", "gossip", "money", "stories"]',
    ]:
        assert token in source

    for field_name in [
        "legare_affection",
        "dancing_with_legare",
        "left_friday_dance",
        "legare_forbidden",
        "legare_departure_code",
        "escaped_dance_unnoticed",
        "performed_oral_with_legare",
        "had_sex_with_legare",
        "lost_virginity_to_legare",
        "player_knows_legare_deflowered",
        "player_knows_legare_sex",
        "player_saw_legare_sex",
        "knows_player_saw_legare_sex",
        "knows_player_is_watching_legare_sex",
    ]:
        assert f"self.{field_name} =" in source

    for legacy_token in [
        "def sync_from_amanda_maps",
        "def sync_amanda_maps",
        "Amanda.var = AmandaVar",
        "self.var = AmandaVar",
        "AmandaVar",
        "AmandaInfo.dynamic_roll",
        "AmandaDynamicCommonBlocks",
        '"alberdanceadvance"',
        '"legare_dance_thread_stage"',
        '"legare_dance_private_seen"',
        "def amanda_story_defaults",
    ]:
        assert legacy_token not in source

    people_runtime = _source(PEOPLE_RUNTIME)
    for inherited_method in [
        "ensure_story_defaults",
        "reset_daily",
        "story_value",
        "set_story_value",
        "decision_profile",
        "decide",
        "decision_good_probability",
        "mana_bad_probability",
        "change_mana",
        "reward_need_fulfilled",
        "punish_need_unfulfilled",
        "record_reaction",
        "last_decision_reaction",
        "apply_decision_reaction",
        "var_int",
        "set_var_int",
        "add_var_int",
    ]:
        assert f"def {inherited_method}(" not in source
        assert f"def {inherited_method}(" in people_runtime

    dress_change = _source(AMANDA_DRESS_CHANGE)
    assert "def amanda_dress_change_other_saw_text" not in dress_change
    assert "Amanda.dress_change_other_saw_text(GirlNameIAT, agreed_to_redress)" in dress_change

    assert "self.age" not in source


def test_amanda_night_bowl_facts_are_explicit_instance_state():
    init_source = _source(AMANDA_INIT)
    event_source = _source(AMANDA_EVENT_MODEL)
    talk_source = _source(PROJECT_ROOT / "game/NPC/Girls/Amanda/IntAmandaTalk.rpy")
    grocery_source = _source(PROJECT_ROOT / "game/Town/GroceryStore.rpy")
    combined = "\n".join((init_source, event_source, talk_source, grocery_source))

    for field_name in (
        "night_bowl_given",
        "night_bowl_request_day",
        "fancy_night_bowl_received",
        "backyard_relief_preference",
    ):
        assert "self.%s =" % field_name in init_source

    for old_key in (
        "gave_night_bowl",
        "got_fancy_night_bowl",
        "prefers_backyard_relief\"",
    ):
        assert old_key not in combined

    assert "Amanda.night_bowl_given and not Amanda.fancy_night_bowl_received" in grocery_source
    assert "Amanda.fancy_night_bowl_received = True" in talk_source
    assert "not Amanda.fancy_night_bowl_received" in event_source
    assert "Amanda.backyard_relief_preference == 1" in event_source


def test_amanda_v63_migration_consumes_old_night_bowl_keys_once():
    migration = _source(PROJECT_ROOT / "game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V63():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 73" in migration
    assert "if loaded_version < 64:" in migration
    assert "updateSave_V63()" in migration
    for old_key, field_name in (
        ("gave_night_bowl", "night_bowl_given"),
        ("night_bowl_request_day", "night_bowl_request_day"),
        ("got_fancy_night_bowl", "fancy_night_bowl_received"),
        ("prefers_backyard_relief", "backyard_relief_preference"),
    ):
        assert 'amanda_var.pop("%s"' % old_key in block
        assert "Amanda.%s =" % field_name in block


def test_amanda_attic_breakfast_state_is_explicit_and_fall_stage_is_thread_owned():
    init_source = _source(AMANDA_INIT)
    breakfast_source = _source(PROJECT_ROOT / "game/Inn/TavernKitchenBreakfast.rpy")
    melissa_events = _source(PROJECT_ROOT / "game/NPC/Girls/Melissa/MelissaEvents.rpy")
    story_runtime = _source(STORY_RUNTIME)
    combined = "\n".join((init_source, breakfast_source, melissa_events, story_runtime))

    for field_name in (
        "attic_window_breakfast_bj_day",
        "attic_mock_response_day",
        "attic_mock_stopped",
        "attic_mock_exposed",
        "attic_window_favor_stage",
        "breakfast_tease_day",
    ):
        assert "self.%s =" % field_name in init_source

    assert '"attic_window_busted"' not in combined
    assert 'Amanda.set_var_int("attic_window_busted"' not in combined
    assert 'return threads["melissaBatProblem"].num >= 6' in init_source
    assert '"#threads[\'melissaBatProblem\'].num >= 6"' in story_runtime
    assert "Amanda.attic_window_breakfast_bj_day" in breakfast_source
    assert "Amanda.attic_mock_response_day" in breakfast_source
    assert "Amanda.attic_mock_stopped" in breakfast_source
    assert "Amanda.attic_mock_exposed" in breakfast_source
    assert "_tease_info.breakfast_tease_day" in breakfast_source


def test_amanda_window_secret_favor_uses_one_object_stage_and_story_event():
    init_source = _source(AMANDA_INIT)
    event_model = _source(AMANDA_EVENT_MODEL)
    runtime = _source(STORY_RUNTIME)
    room = _source(TAVERN_AMANDA_ROOM)
    kitchen = _source(PROJECT_ROOT / "game/Inn/TavernKitchen.rpy")
    breakfast = _source(PROJECT_ROOT / "game/Inn/TavernKitchenBreakfast.rpy")
    migration = _source(PROJECT_ROOT / "game/TractirSaveSync.rpy")

    assert "self.attic_window_favor_stage = 0" in init_source
    assert "class AmandaKitchenWindowFavorEvent(AmandaEvent):" in event_model
    assert '"story_amanda_kitchen_window_favor_0"' in event_model
    assert '"TavernKitchen"' in event_model and '"enter"' in event_model
    assert '"KitchenWindowFavor"' in runtime
    assert "AmandaKitchenWindowFavor" in runtime
    assert "Amanda.attic_window_favor_stage = 1" in room
    assert "label story_amanda_kitchen_window_favor_0:" in kitchen
    assert 'call IntAmandaSex("amanda", "kitchen", "minet")' in kitchen
    assert 'elif GirlLocASDS == "kitchen":' in _source(PROJECT_ROOT / "game/NPC/Girls/Amanda/IntAmandaSex.rpy")
    assert "Amanda.attic_window_favor_stage = 3" in kitchen
    assert "Amanda.attic_window_favor_stage = 3" in breakfast
    assert 'not hasattr(amanda_obj, "attic_window_favor_stage")' in migration
    assert "attic_window_favor_stage" not in _source(PROJECT_ROOT / "game/script.rpy")


def test_amanda_v64_migration_discards_attic_mirror_and_consumes_breakfast_keys():
    migration = _source(PROJECT_ROOT / "game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V64():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 73" in migration
    assert "if loaded_version < 65:" in migration
    assert "updateSave_V64()" in migration
    assert 'amanda_var.pop("attic_window_busted", None)' in block
    for old_key, field_name in (
        ("attic_window_breakfast_bj_day", "attic_window_breakfast_bj_day"),
        ("attic_mock_response_day", "attic_mock_response_day"),
        ("attic_mock_stopped", "attic_mock_stopped"),
        ("attic_mock_exposed", "attic_mock_exposed"),
        ("breakfast_tease_day", "breakfast_tease_day"),
    ):
        assert 'amanda_var.pop("%s"' % old_key in block
        assert "Amanda.%s =" % field_name in block


def test_amanda_daily_and_misc_facts_are_explicit_instance_state():
    init_source = _source(AMANDA_INIT)
    talk_source = _source(PROJECT_ROOT / "game/NPC/Girls/Amanda/IntAmandaTalk.rpy")
    finish_day = _source(NEXT_DAY_FINISH_EVENTS)
    daily_defaults = _source(PROJECT_ROOT / "game/Utilities/General/NPC/DailySetstatdefault.rpy")
    complaint = _source(PROJECT_ROOT / "game/NPC/Girls/Common/MomDressComplaint.rpy")
    combined = "\n".join((init_source, talk_source, finish_day, daily_defaults, complaint))

    for field_name in (
        "warned_about_not_working",
        "pregnancy_risk_asked_today",
        "mom_dress_complaint_count",
    ):
        assert "self.%s =" % field_name in init_source

    for old_key in ('"warnnotwork"', '"askzalettoday"'):
        assert old_key not in combined
    assert 'Amanda.var_int("MomDressComplaint"' not in combined
    assert 'Amanda.var["MomDressComplaint"]' not in combined

    assert "Amanda.warned_about_not_working = False" in talk_source
    assert "Amanda.pregnancy_risk_asked_today = True" in talk_source
    assert "Amanda.pregnancy_risk_asked_today = False" in finish_day
    assert "Amanda.mom_dress_complaint_count" in daily_defaults
    assert "Amanda.mom_dress_complaint_count = seen_before + 1" in complaint


def test_amanda_v65_migration_consumes_daily_and_misc_keys_once():
    migration = _source(PROJECT_ROOT / "game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V65():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 73" in migration
    assert "if loaded_version < 66:" in migration
    assert "updateSave_V65()" in migration
    for old_key, field_name in (
        ("warnnotwork", "warned_about_not_working"),
        ("askzalettoday", "pregnancy_risk_asked_today"),
        ("MomDressComplaint", "mom_dress_complaint_count"),
    ):
        assert 'amanda_var.pop("%s"' % old_key in block
        assert "Amanda.%s =" % field_name in block


def test_amanda_room_rejection_state_is_explicit_and_preserves_authored_flow():
    init_source = _source(AMANDA_INIT)
    home = _source(PROJECT_ROOT / "game/NPC/Girls/Amanda/AmandaAtHomeCode.rpy")
    room = _source(PROJECT_ROOT / "game/Inn/TavernAmandaRoom.rpy")
    upstairs = _source(PROJECT_ROOT / "game/Inn/TavernUpstairs.rpy")
    event_model = _source(AMANDA_EVENT_MODEL)
    liza_talk = _source(PROJECT_ROOT / "game/NPC/Girls/Amanda/InitAmandaLizaTalkItems.rpy")
    finish_day = _source(NEXT_DAY_FINISH_EVENTS)
    combined = "\n".join((init_source, home, room, upstairs, event_model, liza_talk, finish_day))

    for field_name in (
        "room_entry_blocked_today",
        "room_rejection_count",
        "room_rescue_called",
    ):
        assert "self.%s =" % field_name in init_source

    for old_key in ("kickyoufromroom", "kickyoufromroomcount", "kickedwithmomhelp"):
        assert '"%s"' % old_key not in combined

    assert "if Amanda.room_rejection_count >= 3:" in home
    assert "Amanda.room_rejection_count += 1" in home
    assert "Amanda.room_rescue_called = True" in home
    assert "return not Amanda.room_entry_blocked_today" in upstairs
    assert "Amanda.room_entry_blocked_today = False" in finish_day
    assert "and not Amanda.room_entry_blocked_today" in event_model
    assert "Amanda.room_rescue_called" in liza_talk


def test_amanda_v66_migration_consumes_room_rejection_keys_once():
    migration = _source(PROJECT_ROOT / "game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V66():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 73" in migration
    assert "if loaded_version < 67:" in migration
    assert "updateSave_V66()" in migration
    for old_key, field_name in (
        ("kickyoufromroom", "room_entry_blocked_today"),
        ("kickyoufromroomcount", "room_rejection_count"),
        ("kickedwithmomhelp", "room_rescue_called"),
    ):
        assert 'amanda_var.pop("%s"' % old_key in block
        assert "Amanda.%s =" % field_name in block


def test_amanda_legare_mechanic_is_direct_object_state_without_wrapper_plan():
    init_source = _source(AMANDA_INIT)
    legare_source = _source(AMANDA_LEGARE)
    live_sources = "\n".join(
        _source(path)
        for path in (PROJECT_ROOT / "game").rglob("*.rpy")
        if path.name != "TractirSaveSync.rpy"
    )

    for field_name in (
        "legare_affection",
        "dancing_with_legare",
        "left_friday_dance",
        "legare_forbidden",
        "legare_departure_code",
        "escaped_dance_unnoticed",
        "performed_oral_with_legare",
        "had_sex_with_legare",
        "lost_virginity_to_legare",
        "player_knows_legare_deflowered",
        "player_knows_legare_sex",
        "player_saw_legare_sex",
        "knows_player_saw_legare_sex",
        "knows_player_is_watching_legare_sex",
    ):
        assert "self.%s =" % field_name in init_source

    for old_key in (
        "alberfriends", "albernowdances", "leftdances", "alberprohibit",
        "LegareGo", "EscapeUnnoticed", "sucklegare", "fucklegare",
        "deflowerlegare", "knowdeflowerlegare", "knowlegaresex",
        "sawlegaresex", "knowyousawlegaresex", "knowyouseesex",
    ):
        assert 'Amanda.var_int("%s"' % old_key not in live_sources
        assert 'Amanda.set_var_int("%s"' % old_key not in live_sources
        assert 'Amanda.add_var_int("%s"' % old_key not in live_sources

    assert "def resolve_legare_let_go(self, use_forced_type=0, forced_type=0):" in init_source
    assert "sex_type = self.legare_sex_type()" in init_source
    assert 'self.dynamic_roll(1, 6, "legare_let_go_type_2") <= 5' in init_source
    assert 'self.pregnancy_check("mouth", 1, "legare")' in init_source
    assert 'self.pregnancy_check("inside", 1, "legare")' in init_source
    assert 'self.pregnancy_check("outside", 1, "legare")' in init_source
    assert "build_legare_amanda_let_go_plan" not in live_sources
    assert "apply_legare_amanda_let_go_code" not in live_sources
    assert "label LegareAmandaLetGoCode" not in legare_source


def test_amanda_v67_migration_consumes_complete_legare_state_once():
    migration = _source(PROJECT_ROOT / "game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V67():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 73" in migration
    assert "if loaded_version < 68:" in migration
    assert "updateSave_V67()" in migration
    assert 'amanda_var.pop("alberfriends", 0)' in block
    assert 'amanda_var.pop("LegareGo", 0)' in block
    for old_key, field_name in (
        ("albernowdances", "dancing_with_legare"),
        ("leftdances", "left_friday_dance"),
        ("alberprohibit", "legare_forbidden"),
        ("EscapeUnnoticed", "escaped_dance_unnoticed"),
        ("sucklegare", "performed_oral_with_legare"),
        ("fucklegare", "had_sex_with_legare"),
        ("deflowerlegare", "lost_virginity_to_legare"),
        ("knowdeflowerlegare", "player_knows_legare_deflowered"),
        ("knowlegaresex", "player_knows_legare_sex"),
        ("sawlegaresex", "player_saw_legare_sex"),
        ("knowyousawlegaresex", "knows_player_saw_legare_sex"),
        ("knowyouseesex", "knows_player_is_watching_legare_sex"),
    ):
        assert '("%s", "%s")' % (old_key, field_name) in block
    assert "amanda_var.pop(old_key, 0)" in block


def test_amanda_revealing_dress_request_is_thread_owned_and_code_backed():
    init_source = _source(AMANDA_INIT)
    story = _source(STORY_RUNTIME)
    household = _source(PROJECT_ROOT / "game/Inn/HouseholdRuntimeEvents.rpy")
    tavern_main = _source(TAVERN_MAIN)
    breakfast = _source(PROJECT_ROOT / "game/Inn/TavernKitchenBreakfast.rpy")
    migration = _source(PROJECT_ROOT / "game/TractirSaveSync.rpy")

    assert 'self.revealing_dress_code = ""' in init_source
    assert '"revealing_dress_request_seen"' not in init_source
    assert '"revealing_dress_ordered"' not in init_source
    assert 'LThreadData(0, "amanda", "RevealingDressRequest"' in story
    assert story.count('"AmandaDressRequestEvent"') >= 2
    assert '"TavernMain", "amanda_dress_request"' in story
    assert '"TavernKitchen", "amanda_dress_request"' in story
    assert 'Amanda.revealing_dress_code = dress_name' in household
    assert '$ threads["amandaRevealingDressRequest"].complete()' in household
    assert "amanda_revealing_dress_request_ready" not in household + tavern_main + breakfast
    assert 'story_event_available("TavernMain", "amanda_dress_request")' in tavern_main
    assert 'story_event_available("TavernKitchen", "amanda_dress_request")' in breakfast
    assert 'Amanda.var_int("revealing_dress_ordered"' not in household
    assert 'Amanda.var_int("revealing_dress_request_seen"' not in household

    migration_block = migration.split("def updateSave_V49():", 1)[1].split("label before_load:", 1)[0]
    assert 'Amanda.revealing_dress_code = ""' in migration_block
    assert 'amanda_var.pop("revealing_dress_ordered", None)' in migration_block
    assert 'amanda_var.pop("revealing_dress_request_seen", 0)' in migration_block
    assert 'threads.get("amandaRevealingDressRequest", None)' in migration_block


def test_amanda_inherits_common_decision_state_and_keeps_custom_fertility_model():
    source = _source(AMANDA_INIT)
    people_runtime = _source(PEOPLE_RUNTIME)

    for token in [
        "return build_girl_decision_profile(self.code_name)",
        "result = girl_decide(self.code_name, action_name, profile, roll)",
        "self.record_reaction(action_name",
        "return girl_decision_good_probability(self.code_name, action_name, profile)",
        "girl_decision_reaction_score(reaction_key)",
        'self.var.get("decision_results", {}).get(action_key, {})',
        "def mana_bad_probability(self):",
        "1.0 - (float(people_to_int(getattr(self, \"mana\", 0), 0)) / 100.0)",
        "return self.change_mana(abs(people_to_int(amount, 1)), reason)",
        "return self.change_mana(-abs(people_to_int(amount, 1)), reason)",
    ]:
        assert token in people_runtime

    for token in [
        "return dict(girl_decision_cycle_state(self.code_name) or {})",
        "self.stats[\"PussyWetStart\"] = max(",
    ]:
        assert token in source

    assert "def morning_issue" not in source
    assert "def morning_sickness_active" not in source
    assert "callable(tavern_kitchen_fertility_bonus_active)" not in source
    assert "if tavern_kitchen_fertility_bonus_active():" in source


def test_amanda_legare_thread_is_wired_to_event_runtime():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(AMANDA_DANCE_EVENT_MODEL)
    friday = _source(FRIDAY_DANCE)
    legare = _source(AMANDA_LEGARE)
    dance = _source(AMANDA_DANCE)
    after_dance = _source(AMANDA_AFTER_DANCE)

    assert "class AmandaDanceEvent(Event):" in event_model
    assert "def canTrigger(self, evtDay=0):" not in event_model
    assert "def amanda_dance_event(" not in event_model
    assert "return bool(Amanda.dance_event_conditions_met(self))" in event_model
    assert "define amandaThreadList = [" in runtime
    assert 'LThreadData(0, "amanda", "LegareDance"' in runtime
    assert '"story_amanda_legare_dance_0"' in event_model
    assert '"story_amanda_legare_dance_1"' in event_model
    assert '"story_amanda_legare_dance_2"' in event_model
    assert '"story_amanda_legare_dance_3"' in event_model
    assert '"story_amanda_legare_dance_4"' in event_model
    for event_name in (
        "AmandaLegareDanceIntro",
        "AmandaLegareDanceTalking",
        "AmandaLegareDanceGroping",
        "AmandaLegareDanceKissing",
        "AmandaLegareDanceAfter",
        "AmandaFridayDanceMC",
        "AmandaFridayDanceLegare",
    ):
        assert event_name in event_model
        assert event_name in runtime
    assert "amanda_dance_event(" not in runtime
    assert 'LThreadData(0, "amanda", "FridayDanceMC"' in runtime
    assert 'LThreadData(0, "amanda", "FridayDanceLegare"' in runtime
    assert '"story_amanda_friday_dance_mc_0"' in event_model
    assert '"story_amanda_friday_dance_legare_0"' in event_model
    assert '"FridayDance"' in event_model
    assert '"enter"' in event_model
    assert '"amanda_dance_mc"' in event_model
    assert '"amanda_dance_legare"' in event_model
    assert 'call checkTriggers("FridayDance", "enter", 0)' in friday
    assert 'call checkTriggers("FridayDance", "amanda_dance_legare", 0)' in friday
    assert 'call checkTriggers("FridayDance", "amanda_dance_mc", 0)' in friday
    assert "call IntAmandaDance" not in friday
    assert "label story_amanda_legare_dance_0:" in legare
    assert "label story_amanda_legare_dance_1:" in legare
    assert "label story_amanda_legare_dance_2:" in legare
    assert "label story_amanda_legare_dance_3:" in legare
    assert "label story_amanda_legare_dance_4:" in legare
    amanda_init = _source(AMANDA_INIT)
    assert "def legare_claims_first_friday_dance(self):" in amanda_init
    assert 'str(people.location("alber") or "") == "FridayDance"' in amanda_init
    assert 'str(people.location("clara") or "") != "FridayDance"' in amanda_init
    assert "force_legare_first_dance = Amanda.legare_claims_first_friday_dance()" in legare
    assert "if force_legare_first_dance and dance_index == 0:" in legare
    assert "GirlDance_Add('amanda', 'legare', 1" in legare
    assert 'vscene "images/market/LocFridayDance.jpg"' in legare
    assert "Amanda.mark_legare_intro_seen()" in legare
    assert legare.count("$ event_runtime.active_thread.advance()") == 5
    assert "legare_dance_thread_stage" not in legare
    assert "legare_dance_private_seen" not in legare
    assert "legare_dance_pending" not in amanda_init + friday + legare + dance
    assert "CheckIfDanceExist('amanda', 'legare', rooms.get(\"FridayDance\").dance_count) > 0" in friday
    assert 'GetDanceFromTable("amanda", "legare", rooms.get("FridayDance").dance_count)' in legare
    assert 'GetDanceFromTable("amanda", "legare", rooms.get("FridayDance").dance_count)' in dance
    assert "Amanda.legare_affection" in legare
    assert 'Amanda.change_mana(-1, "friday_dance_legare_pressure")' in legare
    assert "event_runtime.active_thread.advance()" in legare
    assert "Amanda.set_story_value" not in legare
    assert "Amanda.story_value" not in legare
    assert "AmandaVar[" not in legare
    assert "label story_amanda_friday_dance_mc_0:" in dance
    assert "label story_amanda_friday_dance_legare_0:" in dance
    assert "call EventAmandaLegareCreateDance" in dance
    assert "call IntAmandaDance" in dance
    assert "menu amanda_dance_menu:" in dance
    assert "jump AmandaAfterDanceMC" in dance
    assert "AmandaVar[" not in dance
    assert "label AmandaAfterDanceMC:" in after_dance
    assert "label AmandaAfterDanceMCMakeOut:" in after_dance
    assert "label AmandaAfterDanceMCWalkHome:" in after_dance
    assert "label AmandaAfterDanceMCReturn:" in after_dance
    assert "label AmandaSexDanceStreet:" in after_dance
    assert '"Увести ее глубже в переулок"' in after_dance
    assert "jump AmandaSexDanceStreet" in after_dance
    assert "jump AmandaAfterDanceMCFinish" in after_dance
    assert "Amanda.change_mana(1, \"friday_dance_makeout\")" in after_dance
    assert "Amanda.change_mana(1, \"friday_dance_after_sex\")" in after_dance
    assert "AmandaVar[" not in after_dance


def test_legare_connected_events_use_secondary_npc_class_state():
    secondary = _source(SECONDARY_INIT)
    alber_init = _source(ALBER_INIT)
    after_legare = _source(AMANDA_AFTER_LEGARE)
    after_legare_sex = _source(AMANDA_AFTER_LEGARE_SEX)
    talk = _source(ALBER_TALK)
    next_day = _source(NEXT_DAY_NEW_EVENTS)

    for token in [
        "class AlberData(PeopleData):",
        "class AlberInfo(BaseNPC):",
        "define AlberStaticData = AlberData()",
        "default Alber = AlberInfo()",
        "people.register(AlberStaticData, Alber)",
        "self.liza_encounter_seen = False",
        "self.talked_about_liza = False",
        "self.heard_about_wife = False",
        "self.amanda_conflict_stage = 0",
        "whore_visit_frequency = 3",
    ]:
        assert token in alber_init
    assert "STORY_DEFAULTS" not in alber_init
    assert "uses_own_var_state" not in alber_init
    assert "self.ensure_story_defaults()" not in alber_init

    people_runtime = _source(PROJECT_ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy")
    assert "def story_value(self, key, default=0):" in people_runtime
    assert "def set_story_value(self, key, value):" in people_runtime
    assert "def add_relation(self, amount=1, cap=20):" in people_runtime
    assert "def finish_talk(self):" in people_runtime
    assert "def add_relation(self, amount=1, cap=20):" not in alber_init
    assert "def finish_talk(self):" not in alber_init
    assert "def story_value(self, key, default=0):" not in alber_init

    assert "class AlberData" not in secondary
    assert "class AlberInfo" not in secondary

    assert "Alber.amanda_conflict_stage = 1" in after_legare
    assert "Alber.heard_about_wife = True" in after_legare_sex
    assert "not Alber.heard_about_wife" in after_legare_sex
    assert "label AmandaLegareReactOnYouSee:" in after_legare_sex
    assert "label AmandaLegareMinetFinish:" in after_legare_sex
    assert "label AmandaLegareSexFinish(tmpLegareSexType):" in after_legare_sex
    assert "call AmandaLegareMinetFinish" in after_legare_sex
    assert "call AmandaLegareSexFinish(tmpLegareSexType)" in after_legare_sex
    assert "_adsl_" not in after_legare_sex
    assert "except Exception" not in after_legare_sex
    assert "Alber.amanda_conflict_stage > 0" in talk
    assert "Alber.amanda_conflict_stage = 0" in talk
    assert "Alber.whore_visit_frequency" in next_day

    connected = "\n".join([secondary, alber_init, after_legare, after_legare_sex, talk, next_day])
    assert "default AlberVar" not in connected
    assert "AlberVar[" not in connected
    assert "AlberVar.get" not in connected
    assert "Alber.var_int(" not in connected
    assert "Alber.set_var_int(" not in connected
    assert "alber_story_value" not in connected
    assert "alber_set_story_value" not in connected
    assert "alber_info" not in connected
    assert "class Alber(BaseNPC):" not in secondary + alber_init
    assert "Alber(var=AlberVar)" not in secondary + alber_init


def test_amanda_legare_street_and_tavern_events_use_thread_model_and_txt_logic():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(AMANDA_EVENT_MODEL)
    amanda_init = _source(AMANDA_INIT)
    alber_init = _source(ALBER_INIT)
    street_events = _source(AMANDA_STREET_EVENTS)
    next_day = _source(NEXT_DAY_NEW_EVENTS)
    finish_day = _source(NEXT_DAY_FINISH_EVENTS)

    for token in [
        '"TavernSeductions"',
        '"LegareTavernVisits"',
        '"StreetLegareSightings"',
        '"StreetLoverEncounters"',
        "AmandaTavernSeduction",
        "AmandaLegareTavernVisit",
        "AmandaStreetLegareSightingStreet",
        "AmandaStreetLegareSightingMarket",
        "AmandaStreetLoverEncounterStreet",
        "AmandaStreetLoverEncounterMarket",
    ]:
        assert token in runtime

    assert "[AmandaStreetLegareSightingStreet, AmandaStreetLegareSightingMarket]" in runtime
    assert "[AmandaStreetLoverEncounterStreet, AmandaStreetLoverEncounterMarket]" in runtime

    for token in (
        "class AmandaTavernSeductionEvent(AmandaEvent):",
        "class AmandaLegareTavernVisitEvent(AmandaEvent):",
        "class AmandaStreetLegareSightingEvent(AmandaEvent):",
        "class AmandaStreetLoverEncounterEvent(AmandaEvent):",
        '"story_amanda_tavern_seduction_0"',
        '"story_amanda_legare_tavern_visit_0"',
        '"story_amanda_street_legare_sighting_0"',
        '"story_amanda_street_lover_encounter_0"',
    ):
        assert token in event_model

    for token in (
        "tavern_seduction_seen_day",
        "legare_tavern_visit_seen_day",
        "street_legare_sighting_seen_day",
        "street_lover_encounter_seen_day",
    ):
        assert token not in amanda_init + street_events

    alber_schedule = ALBER_SCHEDULE.read_text(encoding="utf-8")
    assert 'npc_schedule_set("alber"' not in alber_init
    assert '"label": "amanda_tavern_visit"' in alber_schedule
    assert '"rule": "alber_tavern_visit_ready"' in alber_schedule
    assert '"label": "friday_dance"' in alber_schedule
    assert '"label": "sunday_church"' in alber_schedule

    for token in [
        "label story_amanda_tavern_seduction_0:",
        "label story_amanda_legare_tavern_visit_0:",
        "label story_amanda_street_legare_sighting_0:",
        "label story_amanda_street_lover_encounter_0:",
            'CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun")',
            'GetSexEventFromTable("amanda", calendar_v2.time_slot(), "legarerun")',
        "jump AfterDanceSexLegare",
            'CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "lovermeet")',
            'GetSexEventFromTable("amanda", calendar_v2.time_slot(), "lovermeet")',
        "jump AmandaLoverSex",
        "Amanda.yell_not_work()",
        "Amanda.resolve_legare_let_go()",
    ]:
        assert token in street_events

    assert "def amanda_tavern_seduction_ready" not in street_events
    assert "def amanda_legare_tavern_visit_ready" not in street_events
    assert "def amanda_street_legare_sighting_ready" not in street_events
    assert "def amanda_street_lover_encounter_ready" not in street_events
    assert 'CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "legarerun")' in event_model
    assert 'CheckIfSexEventExist("amanda", calendar_v2.time_slot(), "lovermeet")' in event_model

    assert "TodaySexEvents_Add('amanda', 3, 99, 'legarerun')" in next_day
    assert "TodaySexEvents_Add('amanda', 2, 99, 'lovermeet')" in next_day
    assert 'place == "legarerun"' in finish_day
    assert 'Amanda.resolve_legare_let_go()' in finish_day
    assert 'place == "lovermeet"' in finish_day
    assert 'Amanda.lover_sex_calc()' in finish_day


def test_amanda_liza_work_talk_uses_real_source_event_without_invented_bridge():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(AMANDA_EVENT_MODEL)
    amanda_init = _source(AMANDA_INIT)
    glory_events = _source(AMANDA_LIZA_GLORY_EVENTS)
    liza_items = _source(AMANDA_LIZA_TALK_ITEMS)
    tavern_random = _source(TAVERN_RANDOM_EVENTS)
    amanda_room = _source(TAVERN_AMANDA_ROOM)

    assert '"LizaWorkTalk"' in runtime
    assert "AmandaLizaWorkTalk" in runtime
    assert "class AmandaLizaWorkTalkEvent(AmandaEvent):" in event_model
    assert '"story_amanda_liza_talk_work_0"' in event_model
    assert 'tavern_work_pop_planned_code("AmandaLizaTalk", calendar_v2.time_slot(), True, "TavernMain")' in glory_events
    assert "call EventAmandaLizettTalk(1)" in glory_events
    amanda_liza_talk = _source(PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "EventAmandaLizettTalk.rpy")
    assert "not_to_speak=0" in amanda_liza_talk
    assert "NotToSpeak" not in amanda_liza_talk
    assert "YourReaction1" not in amanda_liza_talk
    assert "def tavern_work_pop_planned_code" in tavern_random
    assert '"Condition": lambda:' in liza_items
    assert '"Reaction": (' in liza_items
    assert '"Condition": "' not in liza_items
    assert '"Code":' not in liza_items
    assert "eval(" not in liza_items
    assert "except Exception" not in liza_items
    assert '_amanda_liza_reaction_values = tuple(_amanda_liza_row.get("Reaction", ()))' in _source(
        PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "EventAmandaLizettTalk2.rpy"
    )

    invented_tokens = (
        '"LizaGloryInvite"',
        '"GloryAftermath"',
        "AmandaLizaGloryInvite",
        "AmandaGloryTavernAftermath",
        "AmandaGloryNightAfter",
        "story_amanda_liza_glory_invite_0",
        "story_amanda_glory_tavern_aftermath_0",
        "story_amanda_night_after_glory_0",
        "amanda_liza_apply_story_marks",
        "liza_glory_hint_seen_day",
        "glory_liza_invite_seen",
        "glory_liza_invite_day",
        "glory_last_event_day",
        "liza_talk_seen_day",
        "liza_glory_invite_event_seen_day",
        "glory_tavern_aftermath_seen_day",
        "night_after_glory_seen_day",
    )
    live_source = runtime + event_model + amanda_init + glory_events + liza_items
    for token in invented_tokens:
        assert token not in live_source

    assert "AmandaVar" not in glory_events
    assert "AmandaVar" not in liza_items
    assert "call RoomEnterEventGate(rooms.current_code, False)" in amanda_room


def test_amanda_talk_and_dress_are_direct_menus_while_room_actions_use_events():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(AMANDA_EVENT_MODEL)
    talk = _source(PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "IntAmandaTalk.rpy")
    room = _source(TAVERN_AMANDA_ROOM)
    bed = _source(TAVERN_AMANDA_BED)
    amanda_init = _source(PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmanda.rpy")

    for token in [
        '"RoomNightApproach"',
        '"MorningWindowEpisode"',
        '"NightBowlWindow"',
        "AmandaRoomNightApproach",
        "AmandaMorningWindowEpisode",
        "AmandaNightBowlWindow",
    ]:
        assert token in runtime

    for token in (
        "class AmandaRoomNightApproachEvent(AmandaEvent):",
        "class AmandaMorningWindowEpisodeEvent(AmandaEvent):",
        "class AmandaNightBowlWindowEvent(AmandaEvent):",
        '"story_amanda_room_grope_0"',
        '"story_amanda_room_morning_window_0"',
        '"story_amanda_night_bowl_window_0"',
    ):
        assert token in event_model

    removed_menu_plumbing = runtime + event_model + talk
    for token in (
        '"TalkHub"',
        '"DressChange"',
        "AmandaTalkHub",
        "AmandaDressChange",
        "AmandaTalkHubEventEntry",
        "story_amanda_talk_hub_0",
        "story_amanda_dress_change_0",
    ):
        assert token not in removed_menu_plumbing

    assert 'talk_label = "IntAmandaTalk"' in amanda_init
    assert not CHARACTER_ACTION_HUB.exists()
    assert 'label IntAmandaTalk(girl_name="amanda"):' in talk
    assert "while True:" not in talk
    assert "call int_amanda_dress_change(girl_name)" in talk
    assert "jump IntAmandaTalk" not in talk
    assert "label IntAmandaTalkApply" not in talk
    assert "choice_code" not in talk
    assert "main_ui_runtime.action_items" not in talk
    assert 'target="checkTriggers"' in bed
    assert 'args=("TavernAmandaRoom", "amanda_grope", 0)' in bed
    assert "condition=AmandaRoomNightApproach.canTrigger" in bed
    assert "roomActionAvailable" not in event_model + bed
    assert "label AmandaRoomGropeEventEntry:" not in room
    assert "label story_amanda_room_grope_0:" in room
    assert "TavernAmandaRoomGropeAction" not in room


def test_amanda_gloryhole_try_enters_through_thread_event():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(AMANDA_EVENT_MODEL)
    glory_hole = _source(TAVERN_GLORY_HOLE)
    amanda_glory = _source(AMANDA_AT_GLORY_HOLE)

    for token in [
        '"GloryHoleTry"',
        "AmandaGloryHoleTry",
    ]:
        assert token in runtime

    assert "class AmandaGloryHoleTryEvent(AmandaEvent):" in event_model
    assert '"story_amanda_gloryhole_try_0"' in event_model
    assert "def amanda_gloryhole_try_ready():" not in amanda_glory
    assert "label AmandaAtGloryHoleEventEntry:" not in amanda_glory
    assert "label story_amanda_gloryhole_try_0:" in amanda_glory
    assert 'call checkTriggers("TavernGloryHole", "amanda_gloryhole_try", 0)' in glory_hole
    assert "AmandaAtGloryHoleEventEntry" not in glory_hole
    assert "Реакция для этой сцены пока недоступна" not in glory_hole
    assert "ClientsSaw" not in glory_hole
    assert "call AmandaAtGloryHole\n" not in glory_hole


def test_amanda_external_intent_layer_is_removed_from_runtime_flow():
    runtime = _source(STORY_RUNTIME)
    room_sources = "\n".join([
        _source(TAVERN_MAIN),
        _source(TAVERN_KITCHEN),
        _source(TAVERN_AMANDA_ROOM),
        _source(TAVERN_MY_ROOM),
        _source(TAVERN_STORAGE),
    ])

    for path in [
        PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / ("Amanda" + "AI_Bridge.rpy"),
        PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / ("Amanda" + "Intent_ren.py"),
    ]:
        assert not path.exists()

    for token in [
        "AI" + "MiniRoom",
        "AI" + "MiniBreakfast",
        "story_amanda_" + "ai_room_mini_0",
        "story_amanda_" + "ai_breakfast_mini_0",
        "amanda_" + "ai_room_mini",
        "amanda_" + "ai_breakfast_mini",
        "Amanda" + "MiniEventEntry",
        "Amanda" + "MiniEventTry",
        "amanda_" + "ai_mini_event_ready",
        "amanda_" + "ai_mini_event_pop",
    ]:
        assert token not in runtime
        assert token not in room_sources


def test_amanda_birth_and_pregnancy_check_are_owned_by_amanda_thread():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(AMANDA_EVENT_MODEL)
    amanda_init = _source(AMANDA_INIT)
    pregnancy_events = _source(AMANDA_PREGNANCY_EVENTS)
    at_home = _source(AMANDA_AT_HOME)

    for token in [
        '"Birth"',
        "AmandaBirth",
    ]:
        assert token in runtime

    amanda_birth_section = runtime.split('LThreadData(0, "amanda", "Birth"', 1)[1].split('LThreadData(0, "amanda", "LegareTavernVisits"', 1)[0]
    assert '("story_give_birth_amanda"' not in runtime
    assert "AmandaBirth" in amanda_birth_section
    assert "class AmandaBirthEvent(AmandaEvent):" in event_model
    assert '"story_amanda_give_birth_0"' in event_model
    assert "def pregnancy_state(self):" in amanda_init
    assert "def pregnancy_check(self, cum_place" in amanda_init
    assert "def birth_ready(self):" in amanda_init
    assert 'self.set_sex_stat("pregnancy", 1)' in amanda_init
    assert 'self.set_sex_stat("pregfather", dad)' in amanda_init
    assert 'self.detailed_sex_history.append({' in amanda_init
    assert "self.sync_from_amanda_maps()" not in amanda_init
    assert "label story_amanda_give_birth_0:" in pregnancy_events
    assert 'call GiveBirth("amanda")' in pregnancy_events
    assert "def amanda_birth_ready():" not in pregnancy_events
    assert "def amanda_pregnancy_check(cum_place" not in pregnancy_events
    assert 'Amanda.pregnancy_check("inside", 1, "Вы")' in at_home
    assert 'Amanda.pregnancy_check("mouthface", 1, "Вы")' in at_home
    assert "_aah_pregnancy_check" not in at_home
