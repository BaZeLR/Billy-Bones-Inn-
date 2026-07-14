        "self.fertility_cycle = {",        "cycle_phase",
        "cycle_day",        "self.fertility_cycle = {",        "cycle_phase",
        "cycle_day",        "self.fertility_cycle = {",        "cycle_phase",
        "cycle_day",from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AMANDA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmanda.rpy"
AMANDA_LEGARE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaLegareDanceSequence.rpy"
AMANDA_DANCE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "IntAmandaDance.rpy"
AMANDA_DANCE_EVENT_MODEL = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaDanceEventModel.rpy"
AMANDA_AFTER_DANCE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaSexDanceStreet.rpy"
AMANDA_STREET_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaLegareStreetEvents.rpy"
AMANDA_LIZA_GLORY_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaLizaGloryEvents.rpy"
AMANDA_LIZA_TALK_ITEMS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "InitAmandaLizaTalkItems.rpy"
AMANDA_AT_GLORY_HOLE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaAtGloryHole.rpy"
AMANDA_PREGNANCY_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaPregnancyEvents.rpy"
AMANDA_AT_HOME = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AmandaAtHomeCode.rpy"
AMANDA_AFTER_LEGARE = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AfterDanceLegare.rpy"
AMANDA_AFTER_LEGARE_SEX = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "AfterDanceSexLegare.rpy"
SECONDARY_INIT = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "InitSecondaryNPC.rpy"
ALBER_INIT = PROJECT_ROOT / "game" / "NPC" / "Secondary" / "InitAlber.rpy"
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


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def test_amanda_uses_data_info_runtime_shape():
    source = _source(AMANDA_INIT)

    assert "class AmandaData(PeopleData):" in source
    assert "class AmandaInfo(Girl):" in source
    assert "define AmandaStaticData = AmandaData()" in source
    assert "default Amanda = AmandaInfo()" in source
    assert "peopleData[GirlName] = AmandaStaticData" in source
    assert "peopleInfo[GirlName] = Amanda" in source
    assert "default AmandaNPC" not in source


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
        "def reset_daily",
        "def decision_profile",
        "def decide",
        "def decision_good_probability",
        "def mana_profile",
        "def change_mana",
        "def reaction_score",
        "def record_reaction",
        "def last_decision_reaction",
        "def apply_decision_reaction",
        "def cycle_state",
        "def fertility_state",
        "def pregnancy_state",
        "def pregnancy_check",
        "def birth_ready",
        "def apply_body_state",
        "def body_state_line",
        "def morning_issue",
        "def morning_sickness_active",
        "def legare_intro_ready",
        "def mark_legare_intro_seen",
        "def dynamic_roll",
        "def happy_confirm_text",
        "def sex_offer_reaction",
        "def legare_sex_type",
        "def nesluh_value",
        "def lover_sex_calc",
        "def yell_not_work",
        '"favorite_topics": ["fashion", "dances", "gossip", "money", "stories"]',
    ]:
        assert token in source

    for key in [
        "alberfriends",
        "alberprohibit",
        "LegareGo",
        "legare_dance_thread_stage",
        "legare_dance_private_seen",
        "leftdances",
        "sucklegare",
        "fucklegare",
        "deflowerlegare",
        "attic_window_busted",
        "revealing_dress_ordered",
        "beauty_help_terms_accepted",
        "mc_dance_after_seen",
        "mc_dance_makeout_seen",
        "mc_dance_sex_seen",
        "mc_dance_private_walks",
        "mc_dance_last_day",
        "body_state_stamp",
        "needs_bandage",
    ]:
        assert f'"{key}"' in source

    for legacy_token in [
        "def sync_from_amanda_maps",
        "def sync_amanda_maps",
        "Amanda.var = AmandaVar",
        "self.var = AmandaVar",
        "AmandaVar",
        "AmandaInfo.dynamic_roll",
        "AmandaDynamicCommonBlocks",
    ]:
        assert legacy_token not in source

    assert "self.age" not in source


def test_amanda_class_delegates_decision_fertility_and_sickness_to_runtime_models():
    source = _source(AMANDA_INIT)

    for token in [
        "return build_girl_decision_profile(self.code_name)",
        "result = girl_decide(self.code_name, action_name, profile, roll)",
        "self.record_reaction(action_name",
        "return girl_decision_good_probability(self.code_name, action_name, profile)",
        "girl_decision_reaction_score(reaction_key)",
        "GirlDecisionLast.get(\"%s:%s\" % (self.code_name, action_key)",
        "def mana_bad_probability(self):",
        "1.0 - (float(people_to_int(self.mana, 0)) / 100.0)",
        "return self.change_mana(abs(people_to_int(amount, 1)), reason)",
        "return self.change_mana(-abs(people_to_int(amount, 1)), reason)",
        "state = dict(girl_decision_cycle_state(self.code_name) or {})",
        "self.stats[\"PussyWetStart\"] = max(",
        "household_morning_issue_type(self.code_name, time_value, hour_value)",
        "morning_sickness_daily_event_ready(self.code_name, location_name",
    ]:
        assert token in source


def test_amanda_legare_thread_is_wired_to_event_runtime():
    runtime = _source(STORY_RUNTIME)
    event_model = _source(AMANDA_DANCE_EVENT_MODEL)
    friday = _source(FRIDAY_DANCE)
    legare = _source(AMANDA_LEGARE)
    dance = _source(AMANDA_DANCE)
    after_dance = _source(AMANDA_AFTER_DANCE)

    assert "class AmandaDanceEvent(Event):" in event_model
    assert "def canTrigger(self, evtDay=0):" in event_model
    assert "return bool(Amanda.dance_event_conditions_met(self))" in event_model
    assert "define amandaThreadList = [" in runtime
    assert 'LThreadData(0, "amanda", "LegareDance"' in runtime
    assert '"story_amanda_legare_dance_0"' in runtime
    assert '"story_amanda_legare_dance_1"' in runtime
    assert '"story_amanda_legare_dance_2"' in runtime
    assert '"story_amanda_legare_dance_3"' in runtime
    assert '"story_amanda_legare_dance_4"' in runtime
    assert 'amanda_dance_event("AmandaLegareDance_4"' in runtime
    assert 'LThreadData(0, "amanda", "FridayDanceMC"' in runtime
    assert 'LThreadData(0, "amanda", "FridayDanceLegare"' in runtime
    assert '"story_amanda_friday_dance_mc_0"' in runtime
    assert '"story_amanda_friday_dance_legare_0"' in runtime
    assert '"FridayDance"' in runtime
    assert '"enter"' in runtime
    assert '"amanda_dance_mc"' in runtime
    assert '"amanda_dance_legare"' in runtime
    assert 'call checkTriggers("FridayDance", "enter", 0)' in friday
    assert 'call checkTriggers("FridayDance", "amanda_dance_legare", 0)' in friday
    assert 'call checkTriggers("FridayDance", "amanda_dance_mc", 0)' in friday
    assert "call IntAmandaDance" not in friday
    assert "label story_amanda_legare_dance_0:" in legare
    assert "label story_amanda_legare_dance_1:" in legare
    assert "label story_amanda_legare_dance_2:" in legare
    assert "label story_amanda_legare_dance_3:" in legare
    assert "label story_amanda_legare_dance_4:" in legare
    assert "def amanda_legare_claims_first_friday_dance" in legare
    assert 'str(getLocation("alber") or "") != "FridayDance"' in legare
    assert 'str(getLocation("clara") or "") == "FridayDance"' in legare
    assert "ForceLegareFirstDance = amanda_legare_claims_first_friday_dance()" in legare
    assert "if ForceLegareFirstDance and i == 0:" in legare
    assert "GirlDance_Add('amanda', 'legare', 1" in legare
    assert 'vscene "images/market/LocFridayDance.jpg"' in legare
    assert "Amanda.mark_legare_intro_seen()" in legare
    assert 'Amanda.set_var_int("legare_dance_thread_stage", 1)' in legare
    assert 'Amanda.set_var_int("legare_dance_thread_stage", 2)' in legare
    assert 'Amanda.set_var_int("legare_dance_thread_stage", 3)' in legare
    assert 'Amanda.set_var_int("legare_dance_thread_stage", 4)' in legare
    assert 'Amanda.set_var_int("legare_dance_private_seen", 1)' in legare
    assert 'Amanda.var_int("alberfriends", 0)' in legare
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
    assert 'Amanda.add_var_int("mc_dance_sex_seen", 1)' in after_dance
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
        "def alber_story_defaults():",
        "class AlberData(PeopleData):",
        "class AlberInfo(BaseNPC):",
        "uses_own_var_state = True",
        "define AlberStaticData = AlberData()",
        "default Alber = AlberInfo()",
        "peopleData[\"alber\"] = AlberStaticData",
        "self.ensure_story_defaults()",
        "peopleInfo[\"alber\"] = Alber",
        "def story_value(self, key, default=0):",
        "def set_story_value(self, key, value):",
        "def story_value(self, key, default=0):",
        "def set_story_value(self, key, value):",
        "def story_value(self, key, default=0):",
        "def set_story_value(self, key, value):",
        "def add_relation(self, amount=1, cap=20):",
        "def finish_talk(self):",
    ]:
        assert token in alber_init

    assert '"alber"' in secondary

    assert 'Alber.set_var_int("FightYouAmanda", 1)' in after_legare
    assert 'Alber.set_var_int("hearabouthiswife", 1)' in after_legare_sex
    assert 'Alber.var_int("hearabouthiswife", 0)' in after_legare_sex
    assert 'Alber.var_int("FightYouAmanda", 0)' in talk
    assert 'Alber.set_var_int("FightYouAmanda", 0)' in talk
    assert 'Alber.var_int("WhoreVisitFreq", 3)' in next_day

    connected = "\n".join([secondary, alber_init, after_legare, after_legare_sex, talk, next_day])
    assert "default AlberVar" not in connected
    assert "AlberVar[" not in connected
    assert "AlberVar.get" not in connected
    assert "alber_story_value" not in connected
    assert "alber_set_story_value" not in connected
    assert "alber_info" not in connected
    assert "class Alber(BaseNPC):" not in secondary + alber_init
    assert "Alber(var=AlberVar)" not in secondary + alber_init


def test_amanda_legare_street_and_tavern_events_use_thread_model_and_txt_logic():
    runtime = _source(STORY_RUNTIME)
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
        '"story_amanda_tavern_seduction_0"',
        '"story_amanda_legare_tavern_visit_0"',
        '"story_amanda_street_legare_sighting_0"',
        '"story_amanda_street_lover_encounter_0"',
        '"TavernMain"',
        '"StreetTavern"',
        '"MarketPlace"',
        '"enter"',
    ]:
        assert token in runtime

    for token in [
        '"tavern_seduction_seen_day": -1',
        '"legare_tavern_visit_seen_day": -1',
        '"street_legare_sighting_seen_day": -1',
        '"street_lover_encounter_seen_day": -1',
    ]:
        assert token in amanda_init

    assert 'npc_schedule_set("alber"' in alber_init
    assert 'NPCScheduleEntry(location="TavernMain"' in alber_init
    assert 'condition=alber_tavern_visit_ready' in alber_init
    assert 'NPCScheduleEntry(location="FridayDance"' in alber_init

    for token in [
        "def amanda_tavern_seduction_ready():",
        "def amanda_legare_tavern_visit_ready():",
        "def amanda_street_legare_sighting_ready(location_name=\"\"):",
        "def amanda_street_lover_encounter_ready(location_name=\"\"):",
        "label story_amanda_tavern_seduction_0:",
        "label story_amanda_legare_tavern_visit_0:",
        "label story_amanda_street_legare_sighting_0:",
        "label story_amanda_street_lover_encounter_0:",
            'CheckIfSexEventExist("amanda", time, "legarerun")',
            'GetSexEventFromTable("amanda", time, "legarerun")',
        "jump AfterDanceSexLegare",
            'CheckIfSexEventExist("amanda", time, "lovermeet")',
            'GetSexEventFromTable("amanda", time, "lovermeet")',
        "jump AmandaLoverSex",
        "Amanda.yell_not_work()",
        "apply_legare_amanda_let_go_code()",
    ]:
        assert token in street_events

    assert "TodaySexEvents_Add('amanda', 3, 99, 'legarerun')" in next_day
    assert "TodaySexEvents_Add('amanda', 2, 99, 'lovermeet')" in next_day
    assert 'place == "legarerun"' in finish_day
    assert 'apply_legare_amanda_let_go_code()' in finish_day
    assert 'place == "lovermeet"' in finish_day
    assert 'Amanda.lover_sex_calc()' in finish_day


def test_amanda_liza_glory_chain_uses_thread_events_and_amanda_state():
    runtime = _source(STORY_RUNTIME)
    amanda_init = _source(AMANDA_INIT)
    glory_events = _source(AMANDA_LIZA_GLORY_EVENTS)
    liza_items = _source(AMANDA_LIZA_TALK_ITEMS)
    tavern_random = _source(TAVERN_RANDOM_EVENTS)
    glory_hole = _source(TAVERN_GLORY_HOLE)
    amanda_room = _source(TAVERN_AMANDA_ROOM)

    for token in [
        '"LizaWorkTalk"',
        '"LizaGloryInvite"',
        '"GloryAftermath"',
        '"story_amanda_liza_talk_work_0"',
        '"story_amanda_liza_glory_invite_0"',
        '"story_amanda_glory_tavern_aftermath_0"',
        '"story_amanda_night_after_glory_0"',
        '"TavernMain"',
        '"tavern_work"',
        '"TavernAmandaRoom"',
        '"enter"',
    ]:
        assert token in runtime

    for token in [
        '"liza_talk_seen_day": -1',
        '"liza_glory_hint_seen_day": -1',
        '"glory_liza_invite_seen": 0',
        '"glory_liza_invite_day": -1',
        '"liza_glory_invite_event_seen_day": -1',
        '"glory_last_event_day": -1',
        '"glory_tavern_aftermath_seen_day": -1',
        '"night_after_glory_seen_day": -1',
    ]:
        assert token in amanda_init

    assert "amanda_liza_apply_story_marks(selected_row)" in liza_items
    assert 'Amanda.set_var_int("glory_liza_invite_seen", 1)' in liza_items
    assert 'Amanda.set_var_int("glory_liza_invite_day", current_day)' in liza_items
    assert "AmandaVar" not in glory_events
    assert "AmandaVar" not in liza_items
    assert "def tavern_work_pop_planned_code" in tavern_random
    assert 'tavern_work_pop_planned_code("AmandaLizaTalk", time, True, "TavernMain")' in glory_events
    assert "call EventAmandaLizettTalk(1)" in glory_events
    assert "jump TavernGloryHole" in glory_events
    assert "amanda_glory_tavern_aftermath_ready" in glory_events
    assert "amanda_night_after_glory_ready" in glory_events
    assert 'Amanda.set_var_int("glory_last_event_day", int(dayspassed or 0))' in glory_hole
    assert "call RoomEnterEventGate(CurLoc, False)" in amanda_room


def test_amanda_talk_dress_and_room_actions_enter_through_thread_events():
    runtime = _source(STORY_RUNTIME)
    talk = _source(PROJECT_ROOT / "game" / "NPC" / "Girls" / "Amanda" / "IntAmandaTalk.rpy")
    room = _source(TAVERN_AMANDA_ROOM)
    bed = _source(TAVERN_AMANDA_BED)
    hub = _source(CHARACTER_ACTION_HUB)

    for token in [
        '"TalkHub"',
        '"DressChange"',
        '"RoomNightApproach"',
        '"story_amanda_talk_hub_0"',
        '"story_amanda_dress_change_0"',
        '"story_amanda_room_grope_0"',
        '"talk"',
        '"amanda"',
        '"talk_amanda"',
        '"dress_change"',
        '"amanda_grope"',
    ]:
        assert token in runtime

    assert '"talk_label": "AmandaTalkHubEventEntry"' in hub
    assert 'label AmandaTalkHubEventEntry(girl_name="amanda", where_id="", entity_data=None):' in talk
    assert 'call checkTriggers("talk", "amanda", 0)' in talk
    assert "label story_amanda_talk_hub_0:" in talk
    assert "label story_amanda_dress_change_0:" in talk
    assert 'call checkTriggers("talk_amanda", "dress_change", 0)' in talk
    assert 'target="checkTriggers"' in bed
    assert 'args=("TavernAmandaRoom", "amanda_grope", 0)' in bed
    assert "label AmandaRoomGropeEventEntry:" not in room
    assert "label story_amanda_room_grope_0:" in room


def test_amanda_gloryhole_try_enters_through_thread_event():
    runtime = _source(STORY_RUNTIME)
    glory_hole = _source(TAVERN_GLORY_HOLE)
    amanda_glory = _source(AMANDA_AT_GLORY_HOLE)

    for token in [
        '"GloryHoleTry"',
        '"story_amanda_gloryhole_try_0"',
        '"TavernGloryHole"',
        '"amanda_gloryhole_try"',
        "#amanda_gloryhole_try_ready()",
    ]:
        assert token in runtime

    assert "def amanda_gloryhole_try_ready():" in amanda_glory
    assert "label AmandaAtGloryHoleEventEntry:" in amanda_glory
    assert 'call checkTriggers("TavernGloryHole", "amanda_gloryhole_try", 0)' in amanda_glory
    assert "label story_amanda_gloryhole_try_0:" in amanda_glory
    assert "call AmandaAtGloryHoleEventEntry" in glory_hole
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
    amanda_init = _source(AMANDA_INIT)
    pregnancy_events = _source(AMANDA_PREGNANCY_EVENTS)
    at_home = _source(AMANDA_AT_HOME)

    for token in [
        '"Birth"',
        '"story_amanda_give_birth_0"',
        "#amanda_birth_ready()",
        '"TavernMain"',
        '"enter"',
    ]:
        assert token in runtime

    amanda_birth_section = runtime.split('LThreadData(0, "amanda", "Birth"', 1)[1].split('LThreadData(0, "amanda", "LegareTavernVisits"', 1)[0]
    assert '("story_give_birth_amanda"' not in runtime
    assert '"story_amanda_give_birth_0"' in amanda_birth_section
    assert "def pregnancy_state(self):" in amanda_init
    assert "def pregnancy_check(self, cum_place" in amanda_init
    assert "def birth_ready(self):" in amanda_init
    assert 'self.set_sex_stat("pregnancy", 1)' in amanda_init
    assert 'self.set_sex_stat("pregfather", dad)' in amanda_init
    assert 'self.detailed_sex_history.append({' in amanda_init
    assert "self.sync_from_amanda_maps()" not in amanda_init
    assert "label story_amanda_give_birth_0:" in pregnancy_events
    assert 'call GiveBirth("amanda")' in pregnancy_events
    assert "def amanda_birth_ready():" in pregnancy_events
    assert "def amanda_pregnancy_check(cum_place" not in pregnancy_events
    assert 'Amanda.pregnancy_check("inside", 1, "Вы")' in at_home
    assert 'Amanda.pregnancy_check("mouthface", 1, "Вы")' in at_home
    assert "_aah_pregnancy_check" not in at_home
