from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def test_schedule_location_is_resolved_without_copying_it_into_npc_state():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )
    get_location = runtime.split("def getLocation(self, wday=None, hour=None):", 2)[2].split(
        "def isInLocation", 1
    )[0]

    assert "npc_schedule_sync_currentloc" not in game_sources
    assert "npc_schedule_sync_all" not in game_sources
    assert 'return "TavernKitchen"' in get_location
    assert "authored_location" not in get_location
    assert 'getattr(self, "location"' not in get_location
    assert 'scheduled_location = str(data_owner.getLocation(wday, hour) or "")' in get_location
    assert "return scheduled_location" in get_location
    assert "self.data =" not in get_location
    assert "self.location = str(self.data.getLocation" not in get_location


def test_live_npcs_do_not_store_schedule_location_mirrors():
    npc_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game" / "NPC").rglob("*.rpy")
    )
    secondary = (ROOT / "game/NPC/Secondary/InitSecondaryNPC.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert ".location =" not in npc_sources
    assert "secondary_npc_default_profiles" not in secondary
    assert "init_secondary_npc_profiles" not in secondary


def test_interval_schedule_files_do_not_repeat_labels():
    for path in (ROOT / "game/NPC/Schedules").glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        labels = [str(row.get("label", "") or "") for row in payload.get("entries", [])]
        assert len(labels) == len(set(labels)), path.name


def test_character_location_reads_do_not_repair_saved_state():
    character_sources = "\n".join(
        (ROOT / relative_path).read_text(encoding="utf-8-sig")
        for relative_path in (
            "game/NPC/Girls/Melissa/InitMelissa.rpy",
            "game/NPC/Girls/Liza/InitLiza.rpy",
            "game/NPC/Girls/Georgett/InitGeorgett.rpy",
        )
    )

    assert 'self.location = ""' not in character_sources
    assert "updateSave_V3" in (ROOT / "game/TractirSaveSync.rpy").read_text(
        encoding="utf-8-sig"
    )


def test_tavern_client_room_is_a_transient_projection_not_a_schedule_override():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    tavern = (ROOT / "game/Inn/TavernMain.rpy").read_text(encoding="utf-8-sig")
    liza = (ROOT / "game/NPC/Girls/Liza/InitLiza.rpy").read_text(encoding="utf-8-sig")
    georgett = (ROOT / "game/NPC/Girls/Georgett/InitGeorgett.rpy").read_text(encoding="utf-8-sig")
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert 'uses_tavern_client_room = True' in liza
    assert 'uses_tavern_client_room = True' in georgett
    assert 'rooms.get(\"TavernMain\").state.get("client_room_girl", "")' in runtime
    assert 'return "TavernClientRoom"' in runtime
    assert 'peopleInfo[GirlNameTS1].location =' not in tavern
    assert 'peopleInfo[GirlNameTS2].location =' not in tavern
    assert 'str(people.location("liza") or "") == rooms.current_code and int(Liza.job_value("jobwhore", 0) or 0) == 1' in tavern
    assert "define currentVersion = 70" in migration
    assert "def updateSave_V15():" in migration


def test_npc_events_do_not_create_a_parallel_current_location_field():
    live_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game/NPC").rglob("*.rpy")
    )

    assert ".current_location =" not in live_sources


def test_story_location_changes_are_bounded_or_schedule_derived():
    clara_init = (ROOT / "game/NPC/Girls/Clara/InitClara.rpy").read_text(encoding="utf-8-sig")
    clara_talk = (ROOT / "game/NPC/Girls/Clara/IntClaraTalk.rpy").read_text(encoding="utf-8-sig")
    draupnir = (ROOT / "game/Town/StolyarWorkshop.rpy").read_text(encoding="utf-8-sig")
    robin = (ROOT / "game/NPC/Secondary/SherwoodTravel.rpy").read_text(encoding="utf-8-sig")
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    assert 'self.day_location_override_day = -1' in clara_init
    assert 'self.day_location_override_code = ""' in clara_init
    assert "def set_day_location_override(self" in clara_init
    assert "override_day == int(calendar_v2.daysInGame or 0)" in clara_init
    assert 'Clara.set_day_location_override("WineStore")' in clara_talk
    assert 'Clara.set_day_location_override("MarketPlace")' in clara_talk
    assert "Clara.location =" not in clara_talk
    assert "Draupnir.location =" not in draupnir
    assert "Robin.location =" not in robin
    assert 'for character_name in ("Clara", "Draupnir", "Robin")' in migration


def test_normal_venue_compatibility_clears_run_only_in_save_migration():
    live_sources = "\n".join(
        (ROOT / relative_path).read_text(encoding="utf-8-sig")
        for relative_path in (
            "game/NPC/Secondary/InitEddie.rpy",
            "game/NPC/Secondary/InitAlber.rpy",
            "game/NPC/Girls/Inga/InitInga.rpy",
            "game/NPC/Secondary/InitMongol.rpy",
            "game/NPC/Secondary/InitSecondaryNPC.rpy",
        )
    )
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")

    for token in ("self.location =", "self.current_location =", "clear_normal_venue"):
        assert token not in live_sources
    for venue in ("GroceryStore", "WineStore", "BeckyHome", "ArtisansQuarter"):
        assert f'"{venue}"' in migration
    assert "def updateSave_V18():" in migration


def test_schedule_reads_are_pure_and_state_changes_invalidate_only_the_owner():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    dog = (ROOT / "game/NPC/Secondary/DogCompanion.rpy").read_text(encoding="utf-8-sig")
    werecat = (ROOT / "game/NPC/Secondary/MelissaWerecatQuest.rpy").read_text(
        encoding="utf-8-sig"
    )
    allowed_block = runtime.split("def daily_schedule_choice_allowed(self, choice):", 1)[1].split(
        "def daily_schedule_mark_choice", 1
    )[0]

    assert "self.schedule_monthly_counters[monthly_key] = row_count" not in allowed_block
    assert "schedule_monthly_counters" not in runtime
    assert "def daily_schedule_mark_choice" not in runtime
    assert "def invalidate_daily_schedule(self):" in runtime
    assert 'def npc_daily_schedule_invalidate(npc_id=""):' not in runtime
    assert "plan_day = int(self.daily_schedule_plan_day if self.daily_schedule_plan_day is not None else -1)" in runtime
    assert 'choice_key = "%s:%s:%s:%s" % (week_value, start_minute, end_minute, str(data.get("label", "") or ""))' in runtime
    assert "npc_daily_schedule_build_all(True)" not in dog + werecat
    assert "DogStaticData.invalidate_daily_schedule()" in dog
    assert "WerecatStaticData.invalidate_daily_schedule()" in werecat
    assert "calendar_v2.time_slot()" not in dog
    assert "def dog_prepare_current_spawn" not in dog
    assert "npc_daily_schedule_random_interval(\n                13, 16," in dog


def test_debug_time_controls_use_live_schedule_resolution_without_removed_rebuild_fallback():
    debug_tools = (ROOT / "game/Utilities/General/Common/DebugTools.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "npc_daily_schedule_build_all" not in debug_tools
    refresh_block = debug_tools.split("def debug_builder_refresh_runtime():", 1)[1].split(
        "def debug_builder_set_time_slot_control", 1
    )[0]
    assert "_ensure_player_chores_state()" in refresh_block
    assert "except Exception" not in refresh_block


def test_schedule_source_metadata_belongs_only_to_people_data():
    for relative_path, info_marker in (
        ("game/NPC/Girls/Amanda/InitAmanda.rpy", "class AmandaInfo(Girl):"),
        ("game/NPC/Girls/Becky/InitBecky.rpy", "class BeckyInfo(Girl):"),
        ("game/NPC/Girls/Clara/InitClara.rpy", "class ClaraInfo(Girl):"),
        ("game/NPC/Girls/Georgett/InitGeorgett.rpy", "class GeorgettInfo(Girl):"),
        ("game/NPC/Girls/Irma/InitIrma.rpy", "class IrmaInfo(Girl):"),
        ("game/NPC/Girls/Liza/InitLiza.rpy", "class LizaInfo(Girl):"),
        ("game/NPC/Girls/Melissa/InitMelissa.rpy", "class MelissaInfo(Girl):"),
        ("game/NPC/Girls/Sandra/InitSandra.rpy", "class SandraInfo(Girl):"),
    ):
        source = (ROOT / relative_path).read_text(encoding="utf-8-sig")
        data_block, info_block = source.split(info_marker, 1)
        assert "self.schedule_source" in data_block, relative_path
        assert "self.schedule_source" not in info_block, relative_path


def test_interval_schedules_load_once_after_all_npcs_are_registered():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    init_sources = "\n".join(
        (ROOT / relative_path).read_text(encoding="utf-8-sig")
        for relative_path in (
            "game/NPC/Girls/Amanda/InitAmanda.rpy",
            "game/NPC/Girls/Becky/InitBecky.rpy",
            "game/NPC/Girls/Clara/InitClara.rpy",
            "game/NPC/Girls/Irma/InitIrma.rpy",
            "game/NPC/Girls/Melissa/InitMelissa.rpy",
            "game/NPC/Girls/Sandra/InitSandra.rpy",
        )
    )

    init_game = runtime.split("label InitGameNPCs:", 1)[1]
    assert "$ npc_interval_schedule_load_all(True)" in init_game
    assert "npc_interval_schedule_load_file" not in init_sources
    assert "def install_schedule(self):" not in init_sources


def test_schedule_projection_queries_do_not_replace_the_current_day_cache():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "cache_current_day = week_value == current_week" in runtime
    assert "if cache_current_day and plan_day == day_value:" in runtime
    assert "if cache_current_day:\n                self.daily_schedule_plan = plan" in runtime
    assert "self.schedule_entries_for_today(weekday_value)" in runtime


def test_after_load_rebuilds_only_derived_schedule_state_on_people_data_owners():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    save_sync = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    after_load = save_sync.split("label after_load:", 1)[1].split("return", 1)[0]

    assert "def npc_schedule_after_load():" in runtime
    assert "data.ensure_schedule_runtime_state()" in runtime
    assert "data.invalidate_daily_schedule()" in runtime
    assert "data.load_interval_schedule(True)" in runtime
    assert "$ npc_schedule_after_load()" in after_load
    assert "peopleInfo" not in after_load


def test_people_location_panel_reports_schedule_without_teleporting_story_flow():
    source = (ROOT / "game/Utilities/General/NPC/PeopleLocateOverlay.rpy").read_text(
        encoding="utf-8-sig"
    )
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    assert "screen people_locate_overlay" not in source
    assert "standalone" not in source
    assert "Jump(_loc)" not in source
    assert '"location": loc' in source
    assert '"state": people_locate_state_text(key, loc)' in source
    assert "info.talk_available_in_room(room_key)" in source
    assert "def talk_available_in_room(self, room_code=\"\"):" in runtime
    assert "people.action_data_for_room(self.name, room_key) is not None" in runtime
    assert "def npc_social_actions_available_in_room" not in runtime


def test_live_schedule_entries_use_exact_clock_intervals_not_slots():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    game_sources = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (ROOT / "game").rglob("*.rpy")
    )

    assert "time_slots=[" not in game_sources
    assert "npc_daily_schedule_slot" not in game_sources
    assert "npc_daily_schedule_random_slot" not in game_sources
    assert '"default_slots"' not in runtime
    assert '"random_slots"' not in runtime
    constructor = runtime.split("class NPCScheduleEntry(object):", 1)[1].split(
        "def selected_location", 1
    )[0]
    assert "time_slots" not in constructor
    assert "self.start_minute" in constructor
    assert "self.end_minute" in constructor
    assert 'pop("time_slots", [])' not in runtime
    migration = (ROOT / "game/TractirSaveSync.rpy").read_text(encoding="utf-8-sig")
    assert 'state.pop("time_slots", [])' in migration
    assert 'template.pop(old_key, [])' in migration


def test_schedule_diagnostic_reports_exact_clock_intervals_not_legacy_slots():
    source = (ROOT / "game/Utilities/General/Common/DebugTools.rpy").read_text(
        encoding="utf-8-sig"
    )
    report = source.split("def debug_builder_schedule_report():", 1)[1].split(
        "def debug_builder_time_slot_lines():", 1
    )[0]

    assert "entry.start_minute" in report
    assert "entry.end_minute" in report
    assert 'interval_text = "clock=%02d:%02d-%02d:%02d"' in report
    assert 'interval_text = "slots="' not in report
    assert 'getattr(entry, "time_slots"' not in report


def test_json_schedule_boundaries_keep_minute_precision():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    hour_entry = runtime.split("class NPCHourScheduleEntry", 1)[1].split(
        "def selected_location", 1
    )[0]
    matches = runtime.split("def matches(self, weekday_value=None, time_value=None):", 1)[1].split(
        "def __getstate__", 1
    )[0]

    assert "start_parts" in hour_entry
    assert "end_parts" in hour_entry
    assert "end_minute += 1" in hour_entry
    assert "npc_schedule_clock_minute(time_value)" in matches
    assert "self.start_minute <= minute_value < self.end_minute" in matches


def test_json_schedule_loader_has_no_stale_cache_or_misspelled_schema_fallback():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    loader = runtime.split("def load_interval_schedule(self, force=False):", 1)[1].split(
        "def schedule_entries_for_today", 1
    )[0]
    choices = runtime.split("def interval_location_choices_from_json", 1)[1].split(
        "def interval_schedule_entry_from_json", 1
    )[0]

    assert "previous_entries" not in loader
    assert "raise ValueError(self.interval_schedule_load_error)" in loader
    assert 'renpy.file(path).read().decode("utf-8")' in loader
    assert "except Exception" not in loader
    assert 'path = "NPC/Schedules/%s.json" % self.name' not in loader
    assert 'data.get("location_probabilities", [])' in choices
    assert "locaation probability" not in choices


def test_every_json_schedule_is_explicitly_owned_by_its_people_data_object():
    schedule_ids = {
        path.stem for path in (ROOT / "game/NPC/Schedules").glob("*.json")
    }
    owned_ids = set()
    for path in (ROOT / "game/NPC").rglob("*.rpy"):
        source = path.read_text(encoding="utf-8-sig")
        for npc_id in schedule_ids:
            if 'self.schedule_source = "schedules/%s.json"' % npc_id in source:
                owned_ids.add(npc_id)

    assert owned_ids == schedule_ids


def test_location_reads_use_people_data_without_a_duplicate_schedule_wrapper():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    inga = (ROOT / "game/NPC/Girls/Inga/InitInga.rpy").read_text(
        encoding="utf-8-sig"
    )
    melissa = (ROOT / "game/NPC/Girls/Melissa/InitMelissa.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "def npc_schedule_location(" not in runtime
    assert 'people.get_data("eddie").getLocation(week_now, calendar_v2.hour)' in inga
    assert "self.data.getLocation(week_num, hour_num)" in melissa


def test_unused_schedule_method_wrappers_are_absent():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )

    for wrapper_name in (
        "people_schedule_data",
        "getNPCids",
        "getNPCnames",
        "isLocationEmpty",
        "npc_schedule_resolve",
        "npc_schedule_state",
        "npc_can_talk_now",
        "npc_is_awake",
        "npc_daily_schedule_invalidate",
        "npc_schedule_set",
        "npc_schedule_add",
        "npc_schedule_list",
        "npc_daily_schedule_set",
        "npc_daily_schedule_invalidate_all",
        "npc_interval_schedule_load_file",
        "npc_interval_schedule_list",
        "npc_interval_schedule_has_contract",
    ):
        assert "def %s(" % wrapper_name not in runtime

    assert '\n    def getLocation(person=""' not in runtime

    registry = runtime.split("class PeopleRegistry(object):", 1)[1].split(
        "def npc_schedule_clock_minute", 1
    )[0]
    assert 'def location(self, person=""' in registry
    assert 'def ids_at(self, location=""' in registry
    assert 'def schedule_entry(self, person=""' in registry
    assert 'def can_talk(self, person=""' in registry


def test_json_owned_characters_have_no_competing_rpy_baseline_schedule():
    for relative_path in (
        "game/NPC/Girls/Amanda/InitAmanda.rpy",
        "game/NPC/Girls/Sandra/InitSandra.rpy",
    ):
        source = (ROOT / relative_path).read_text(encoding="utf-8-sig")
        assert "self.schedule_source" in source
        assert "npc_schedule_set(" not in source


def test_remaining_inga_schedule_uses_clock_boundaries_not_display_slots():
    source = (ROOT / "game/NPC/Girls/Inga/InitInga.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "time_slots" not in source
    assert "calendar_v2.time_slot()" not in source
    assert 'default_location=""' in source
    assert "start_hour=6" in source
    assert "end_hour=8" in source
    assert "start_minute=8 * 60" in source
    assert "end_minute=9 * 60 + 30" in source
    assert "end_hour=23" in source
    assert "start_hour=23" in source
    assert "end_hour=6" in source


def test_schedule_owned_npcs_have_no_venue_fallback_location():
    for relative_path in (
        "game/NPC/Secondary/InitAlber.rpy",
        "game/NPC/Secondary/InitEddie.rpy",
        "game/NPC/Secondary/InitFrancheska.rpy",
        "game/NPC/Girls/Amanda/InitAmanda.rpy",
        "game/NPC/Girls/Becky/InitBecky.rpy",
        "game/NPC/Girls/Georgett/InitGeorgett.rpy",
        "game/NPC/Girls/Irma/InitIrma.rpy",
        "game/NPC/Girls/Liza/InitLiza.rpy",
    ):
        source = (ROOT / relative_path).read_text(encoding="utf-8-sig")
        assert 'default_location=""' in source, relative_path


def test_francheska_birth_duty_is_an_exact_clock_schedule_not_a_slot_map():
    source = (ROOT / "game/NPC/Secondary/InitFrancheska.rpy").read_text(
        encoding="utf-8-sig"
    )
    next_day = (ROOT / "game/Utilities/Time/NextDay_NewDayEvents.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "self.set_daily_schedule(random_intervals=[" in source
    assert '"start_minute": start_minute' in source
    assert '"end_minute": end_minute' in source
    assert '"location": "EllonaBirthRoom"' in source
    assert '"location": "EllonaTemple"' in source
    assert "busy_slots" not in source + next_day
    assert "calendar_v2.time_slot()" not in source + next_day
    assert "clock_minutes or 0" not in source
    assert "FranStaticData.invalidate_daily_schedule()" in next_day


def test_sergio_shop_presence_has_one_hourly_json_authority():
    source = (ROOT / "game/NPC/Secondary/InitSecondaryNPC.rpy").read_text(
        encoding="utf-8-sig"
    )
    schedule = (ROOT / "game/NPC/Schedules/sergio.json").read_text(
        encoding="utf-8-sig"
    )
    data_class = source.split("class SergioData(PeopleData):", 1)[1].split(
        "class SergioInfo(BaseNPC):", 1
    )[0]

    assert 'self.schedule_source = "schedules/sergio.json"' in data_class
    assert "schedule_entries=[" not in data_class
    assert "def getLocation(" not in data_class
    assert "calendar_v2.time_slot()" not in data_class
    assert '"start": "12:00"' in schedule
    assert schedule.count('"end": "17:59"') == 2
    assert '"start": "08:00"' in schedule
    assert '"end": "11:59"' in schedule


def test_static_venue_npcs_own_exact_hour_schedules_without_permanent_location_fallbacks():
    secondary = (ROOT / "game/NPC/Secondary/InitSecondaryNPC.rpy").read_text(
        encoding="utf-8-sig"
    )
    draupnir = (ROOT / "game/NPC/Secondary/InitDraupnir.rpy").read_text(
        encoding="utf-8-sig"
    )
    zimmer = (ROOT / "game/NPC/Secondary/InitZimmer.rpy").read_text(
        encoding="utf-8-sig"
    )

    luisa_data = secondary.split("class LuisaData(PeopleData):", 1)[1].split(
        "class LuisaInfo(BaseNPC):", 1
    )[0]
    gerhard_data = secondary.split("class GerhardData(PeopleData):", 1)[1].split(
        "class GerhardInfo(BaseNPC):", 1
    )[0]
    draupnir_data = draupnir.split("class DraupnirData(PeopleData):", 1)[1].split(
        "class DraupnirInfo(BaseNPC):", 1
    )[0]
    zimmer_data = zimmer.split("class ZimmerData(PeopleData):", 1)[1].split(
        "class ZimmerInfo(BaseNPC):", 1
    )[0]

    for data_block in (luisa_data, gerhard_data, draupnir_data, zimmer_data):
        assert 'default_location=""' in data_block
        assert "NPCScheduleEntry(" in data_block
        assert "calendar_v2.time_slot()" not in data_block

    assert 'location="HunterClub"' in luisa_data
    assert "weekdays=[1, 2, 3, 4, 6]" in luisa_data
    assert "start_hour=8" in luisa_data and "end_hour=19" in luisa_data

    assert 'location="StolyarWorkshop"' in draupnir_data
    assert "weekdays=[1, 2, 3, 4, 5, 6]" in draupnir_data
    assert "start_hour=6" in draupnir_data and "end_hour=18" in draupnir_data

    assert zimmer_data.count('location="CityGuard"') == 2
    assert "weekdays=[2]" in zimmer_data and "weekdays=[5]" in zimmer_data
    assert "start_hour=11" in zimmer_data and "end_hour=13" in zimmer_data
    assert "start_hour=6" in zimmer_data and "end_hour=8" in zimmer_data

    assert 'location="Church"' in gerhard_data
    assert "weekdays=[7]" in gerhard_data
    assert "start_hour=8" in gerhard_data and "end_hour=13" in gerhard_data


def test_visible_venue_npc_buttons_replace_duplicate_room_talk_actions():
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    registry = runtime.split("class PeopleRegistry(object):", 1)[1].split(
        "def npc_schedule_clock_minute", 1
    )[0]
    hunter = (ROOT / "game/Town/HunterClub.rpy").read_text(encoding="utf-8-sig")
    guard = (ROOT / "game/Town/CityGuard.rpy").read_text(encoding="utf-8-sig")
    church = (ROOT / "game/Town/Church/Church.rpy").read_text(encoding="utf-8-sig")
    talk_owners = {
        "HunterClubLuiseTalk": ROOT / "game/NPC/Secondary/InitSecondaryNPC.rpy",
        "IntZimmerTalk": ROOT / "game/NPC/Secondary/InitZimmer.rpy",
        "ChurchIspoved": ROOT / "game/NPC/Secondary/InitSecondaryNPC.rpy",
        "IntRobinTalk": ROOT / "game/NPC/Secondary/InitRobin.rpy",
    }

    for talk_label, owner_path in talk_owners.items():
        owner = owner_path.read_text(encoding="utf-8-sig")
        assert 'talk_label = "%s"' % talk_label in owner
        assert talk_label not in registry

    assert "NPC_META" not in registry
    assert "return info.action_data(room_key)" in registry
    assert 'action_id="talk_luise"' not in hunter
    assert 'Call("IntZimmerTalk")' not in guard
    assert 'action_id="confession"' not in church
    gerhard_owner = talk_owners["ChurchIspoved"].read_text(encoding="utf-8-sig")
    assert 'str(room_code or "").strip() == "Church"' in gerhard_owner
    assert "return church_confession_action_visible()" in gerhard_owner


def test_lucas_remains_an_authored_scene_participant_not_a_permanent_room_npc():
    secondary = (ROOT / "game/NPC/Secondary/InitSecondaryNPC.rpy").read_text(
        encoding="utf-8-sig"
    )
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    becky_home = (ROOT / "game/Town/BeckyHome.rpy").read_text(encoding="utf-8-sig")
    becky_front = (ROOT / "game/Town/BeckyHomeFront.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "class LucasData" not in secondary
    assert "class LucasInfo" not in secondary
    assert "register_lucas_secondary" not in secondary + runtime
    assert '"lucas": {' not in runtime
    assert 'key in ("inga", "lucas")' not in runtime
    assert "Лукас" in becky_home + becky_front


def test_clara_fiance_remains_a_thread_participant_not_a_registered_npc():
    secondary = (ROOT / "game/NPC/Secondary/InitSecondaryNPC.rpy").read_text(
        encoding="utf-8-sig"
    )
    runtime = (ROOT / "game/Utilities/General/NPC/PeopleRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    events = (ROOT / "game/Utilities/General/Classes/StoryEventRuntime.rpy").read_text(
        encoding="utf-8-sig"
    )
    story = (ROOT / "game/NPC/Girls/Clara/ClaraPaintingsThread.rpy").read_text(
        encoding="utf-8-sig"
    )
    zimmer = (ROOT / "game/NPC/Secondary/InitZimmer.rpy").read_text(
        encoding="utf-8-sig"
    )

    assert "class ClaraFianceData" not in secondary
    assert "class ClaraFianceInfo" not in secondary
    assert "register_clara_fiance_secondary" not in secondary + runtime
    assert "clara_fiance_visit_seen" not in secondary
    assert "ClaraFianceCaseSolved" not in zimmer + story
    assert '"BarberShop",\n            "clara_fiance",' in events
    assert "столичного жениха" in story
