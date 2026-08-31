from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_npc_location_has_one_schedule_authority_after_load():
    save_source = _source("game/TractirSaveSync.rpy")
    runtime_source = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    sex_source = _source("game/Utilities/General/Sex/ShowCurrentSex.rpy")

    assert 'delattr(person_info, "location")' in save_source
    assert 'delattr(self, "location")' in runtime_source
    assert 'getattr(girl, "location", "")' not in sex_source
    assert 'location_code = str(girl.getLocation() or "")' in sex_source


def test_francheska_story_state_is_instance_owned():
    init_source = _source("game/NPC/Secondary/InitFrancheska.rpy")
    talk_source = _source("game/NPC/Secondary/IntFrancheskaTalk.rpy")
    secondary_source = _source("game/NPC/Secondary/InitSecondaryNPC.rpy")
    stat_source = _source("game/Utilities/General/Screens/stat.rpy")

    combined = "\n".join((init_source, talk_source, secondary_source, stat_source))
    assert "FranVar" not in combined
    assert 'self.var = dict(kwargs.get("var", {}) or {})' not in init_source
    assert "STORY_DEFAULTS" not in init_source
    assert "ensure_story_defaults" not in init_source
    assert "Francheska.var" not in talk_source
    assert "Francheska.var" not in stat_source
    for field_name in (
        "met", "asked_about_ellona", "graces_stage", "asked_about_duchess",
        "asked_about_duke", "asked_about_stark", "asked_about_duchy",
        "asked_about_king", "asked_about_kingdom_relations",
        "asked_about_aliens", "sunday_stories_seen_day",
    ):
        assert "self.%s =" % field_name in init_source
    assert '"var": Francheska.var' not in secondary_source
    assert "peopleInfo[npc_key].var = var_table" not in secondary_source


def test_francheska_v57_migration_consumes_old_story_and_schedule_maps():
    migration = _source("game/TractirSaveSync.rpy")
    block = migration.split("def updateSave_V57():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 73" in migration
    assert "if loaded_version < 58:" in migration
    assert "updateSave_V57()" in migration
    for old_key, field_name in (
        ("meet", "met"),
        ("ellonaask", "asked_about_ellona"),
        ("graceask", "graces_stage"),
        ("conchitaask", "asked_about_duchess"),
        ("dukeask", "asked_about_duke"),
        ("starkask", "asked_about_stark"),
        ("stateask", "asked_about_duchy"),
        ("kingask", "asked_about_king"),
        ("rebelask", "asked_about_kingdom_relations"),
        ("alienask", "asked_about_aliens"),
        ("sunday_stories_seen_day", "sunday_stories_seen_day"),
    ):
        assert 'fran_var.pop("%s"' % old_key in block
        assert "Francheska.%s =" % field_name in block
    assert 'globals().pop("FranVar", None)' in block
    assert 'globals().pop("FranBusy", None)' in block


def test_secondary_npc_var_state_is_instance_owned():
    source = _source("game/NPC/Secondary/InitSecondaryNPC.rpy")
    runtime = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")

    for legacy_name in (
        "LuisaVar", "SergioVar", "LucasVar", "GerhardVar",
        "ClaraFianceVar", "SergioPetVar",
    ):
        assert legacy_name not in source
    assert source.count('self.var = dict(kwargs.get("var", {}) or {})') == 3
    assert source.count("STORY_DEFAULTS = {") == 2
    assert "class SergioPetData" not in source
    assert "class SergioPetInfo" not in source
    assert "default SergioPet" not in source
    assert "register_sergio_pet_secondary" not in source + runtime
    assert "self.var.setdefault(k, v)" not in source
    assert "self.promote_from_var(self.var)" not in source
    assert "SECONDARY_NPC_KEYS" not in source
    assert 'registry_group = "secondary"' in runtime
    assert 'registry_group = "girl"' in runtime


def test_secondary_story_state_has_no_write_only_event_echo_flags():
    sources = "\n".join(
        (ROOT / relative_path).read_text(encoding="utf-8-sig")
        for relative_path in (
            "game/NPC/Secondary/InitAlber.rpy",
            "game/NPC/Secondary/InitMongol.rpy",
            "game/NPC/Secondary/InitRobin.rpy",
            "game/NPC/Secondary/SherwoodTravel.rpy",
            "game/NPC/Girls/Clara/ClaraBookletMarketThread.rpy",
            "game/NPC/Girls/Clara/ClaraPaintingsThread.rpy",
        )
    )

    for dead_flag in (
        "clara_paintings_enemy",
        "GuardGiftSent",
        "MongolSafePassUsed",
        "BlackwoodRoadSeen",
    ):
        assert dead_flag not in sources


def test_hunter_club_and_guard_state_have_domain_owners():
    hunter_source = _source("game/Town/HunterClub.rpy")
    room_source = _source("game/Utilities/General/Classes/RoomTemplate.rpy")
    town_source = _source("game/Town/RandomTownEvents.rpy")
    events_source = _source("game/Utilities/General/Classes/StoryEventRuntime.rpy")
    zimmer_source = _source("game/NPC/Secondary/InitZimmer.rpy")

    assert "HunterClubVar" not in hunter_source
    assert "rooms.get(\"HunterClub\").state" in hunter_source
    assert 'self.state = dict(state or {})' in room_source
    assert '"state": dict(state.get("state", {}) or {})' in room_source
    assert "GuardCaptainVar" not in town_source
    assert "GuardCaptainVar" not in events_source
    assert 'TownStreet.patrol_allowed(rooms.current_code)' in events_source
    assert "bool(Zimmer.street_patrol_pass)" in town_source
    assert "self.street_patrol_pass = False" in zimmer_source


def test_npc_var_state_is_not_promoted_into_duplicate_fields():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "promote_from_var" not in game_sources
    assert "story_flags" not in game_sources


def test_mutable_story_api_exists_only_on_people_info():
    runtime = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    data_block, info_block = runtime.split("class PeopleData(object):", 1)[1].split("class PeopleInfo(object):", 1)

    for method in (
        "var_state",
        "var_value",
        "set_var",
        "var_int",
        "set_var_int",
        "story_value",
        "set_story_value",
        "set_story_value_min",
    ):
        assert "def %s(" % method not in data_block
        assert "def %s(" % method in info_block


def test_base_npc_value_queries_do_not_initialize_state():
    runtime = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    var_reader = runtime.split("def var_state(self):", 1)[1].split("def var_value", 1)[0]
    sex_stat_reader = runtime.split("def sex_stat(self, key, default=0):", 1)[1].split(
        "def set_sex_stat", 1
    )[0]
    location_update = runtime.split("def update(self):", 1)[1].split("def var_state", 1)[0]

    assert "self.var =" not in var_reader
    assert "ensure_story_defaults" not in var_reader
    assert "self.stats =" not in sex_stat_reader
    assert "PeopleData(self.name)" not in location_update


def test_npc_known_and_location_state_have_no_global_maps():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "knowsMC" not in game_sources
    assert "knows_mc" not in game_sources
    assert "default CurrentLoc =" not in game_sources
    assert "CurrentLoc.get(" not in game_sources
    assert "CurrentLoc.setdefault(" not in game_sources


def test_inga_story_state_has_no_legacy_var_readers():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "IngaVar[" not in game_sources
    assert "IngaVar.get(" not in game_sources


def test_pregnancy_progress_is_owned_by_each_npc_stats():
    script_source = _source("game/script.rpy")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    daily_source = _source("game/Utilities/General/NPC/DailySetstatdefault.rpy")
    mom_dress_source = _source("game/NPC/Girls/Common/MomDressComplaint.rpy")

    assert "default pregnancy =" not in script_source
    assert "pregnancy.get(" not in game_sources
    assert "pregnancy[" not in game_sources
    assert '_dssd_info.set_sex_stat("pregnancy"' in daily_source
    assert "info.pregnancy_days()" in mom_dress_source
    assert 'info.var["MomDressComplaint"]' in mom_dress_source


def test_daily_openness_relationship_rule_is_npc_owned():
    people_source = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    georgett_source = _source("game/NPC/Girls/Georgett/InitGeorgett.rpy")
    liza_source = _source("game/NPC/Girls/Liza/InitLiza.rpy")
    daily_source = _source("game/Utilities/General/NPC/DailySetstatdefault.rpy")

    assert "def reset_openness_from_relationship(self):" in people_source
    assert "OPENNESS_RELATIONSHIP_STEPS = ((6, 3), (8, 5), (11, 6), (13, 7))" in people_source
    assert "OPENNESS_RELATIONSHIP_STEPS = ((5, 3), (8, 5), (9, 6), (10, 7))" in georgett_source
    assert "OPENNESS_RELATIONSHIP_STEPS = ((4, 3), (7, 5), (6, 6), (8, 7))" in liza_source
    assert "_dssd_info.reset_openness_from_relationship()" in daily_source
    assert "adjust_otkroven" not in daily_source


def test_end_of_day_uses_the_registry_computed_girl_view_once():
    source = _source("game/Utilities/Time/NextDay_FinishDayEvents.rpy")

    assert "_ndf_all_girl_names = [info.name for info in people.girl_values()]" in source
    assert "_ndf_all_girl_names = list(AllGirlNames)" not in source


def test_kid_counts_are_owned_by_each_mother_stats():
    script_source = _source("game/script.rpy")
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    kids_source = _source("game/Utilities/General/Sex/KidsFunctions.rpy")

    assert "default kids =" not in script_source
    assert "kids.get(" not in game_sources
    assert "kids[" not in game_sources
    assert 'mom_info.set_sex_stat("kids"' in kids_source


def test_npc_skills_and_tavern_jobs_have_no_global_state_maps():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    service_source = _source("game/Utilities/General/NPC/SetTavernServiceLevels.rpy")
    player_source = _source("game/Utilities/General/Player/Player.rpy")

    for map_name in (
        "beauty", "cooking", "cleaning", "waitress",
        "jobkitchen", "jobcleaning", "jobwaitress", "jobwhore", "jobgloryhole",
        "jobHallAvail", "jobWhoreAvail", "jobGloryHoleAvail",
        "jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow",
        "jobwhoreTommorow", "jobgloryholeTommorow",
    ):
        assert f"default {map_name} =" not in game_sources
        assert f"{map_name}.get(" not in game_sources
        assert f"{map_name}[" not in game_sources
    assert 'Sandra.skill_value("cooking", 0)' in service_source
    assert 'Sandra.job_value("jobkitchen", 0)' in service_source
    assert "store.tavern" not in service_source
    assert "service = player.tavern_management.service" in service_source
    assert "service.kitchen_score = kitchen_score" in service_source
    assert "service.cleanliness_score = clean_score" in service_source
    assert "service.waitress_score = waitress_score" in service_source
    assert "class PlayerTavernServiceState(object):" in player_source
    assert "self.service = PlayerTavernServiceState()" in player_source


def test_npc_sex_and_daily_social_state_have_no_global_maps():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    legacy_maps = (
        "pregnancy", "kids", "PussyWetStart", "Drunk", "Breastfeed", "Lactate",
        "virginity", "pregfather", "sexacts", "cuminside", "ConceptionChance",
        "HadSex", "GiveOrgasms", "LickPussy", "DayLastOrgasmGiven",
        "CumFaceYou", "CumFaceOthers", "CumTitsYou", "CumTitsOthers",
        "CumInsideYou", "CumInsideOthers", "CockInMouth", "CockInPussy",
        "CockInTits", "CockInAss", "SexInsertedContainer", "EddieCockInMouth",
        "EddieCockInPussy", "EddieCockInTits", "GrupenSex", "cametoday_npc",
        "cancumdaily_npc", "TitsVisible", "PussyVisible", "ShortSkirtNoPanties",
        "FlirtedToday", "GiftedToday", "FuckedToday", "AskedToday",
    )
    for map_name in legacy_maps:
        assert f"default {map_name} =" not in game_sources
    assert "publish_visibility_state" not in game_sources
    assert 'def ensure_sex_state(self):' in game_sources
    assert "self.sex_history" not in game_sources
    assert "self.detailed_sex_history" in game_sources
    assert "self.lunar_fertility" not in game_sources
    for dead_map in ("clothing", "body_state", "body_layers", "insertion_state", "clothing_layers"):
        assert f"self.{dead_map} =" not in game_sources


def test_household_openness_and_rebellion_are_npc_owned():
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "default otkroven =" not in game_sources
    assert "default neshlush =" not in game_sources
    assert "neshlush[" not in game_sources
    assert "neshlush.get(" not in game_sources
    assert "self.rebel_baseline = 0" in game_sources


def test_secondary_npcs_register_directly_without_init_or_auto_wrappers():
    people = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    sources = "\n".join(
        _source(path)
        for path in (
            "game/NPC/Secondary/InitZimmer.rpy",
            "game/NPC/Secondary/InitRobin.rpy",
            "game/NPC/Secondary/InitMongol.rpy",
            "game/NPC/Secondary/InitEddie.rpy",
            "game/NPC/Secondary/InitDraupnir.rpy",
            "game/NPC/Secondary/InitFrancheska.rpy",
            "game/NPC/Secondary/InitSecondaryNPC.rpy",
            "game/NPC/Secondary/InitAlber.rpy",
        )
    )

    for npc_id in ("robin", "zimmer", "eddie", "francheska", "draupnir", "mongol"):
        assert f"call register_{npc_id}_secondary" in people
    assert "label _auto_register_" not in sources
    for label_name in ("InitZimmer", "InitRobin", "InitMongol", "InitEddie", "InitDraupnir", "InitFrancheska"):
        assert f"label {label_name}:" not in sources
