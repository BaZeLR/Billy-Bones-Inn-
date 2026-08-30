import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GEORGETT_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "InitGeorgett.rpy"
GEORGETT_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "GeorgettEvents.rpy"
LIZA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "InitLiza.rpy"
GEORGETT_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "georgett.json"
LIZA_SCHEDULE = PROJECT_ROOT / "game" / "NPC" / "Schedules" / "liza.json"
LIZA_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "LizaEvents.rpy"
GEORGETT_TALK = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "IntGeorgettTalk.rpy"
LIZA_TALK = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "IntLizaTalk.rpy"
LIZA_SEX = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "IntLizaSex.rpy"
PORT_STREETS = PROJECT_ROOT / "game" / "Town" / "PortStreets.rpy"
STREET_CLIENTS = PROJECT_ROOT / "game" / "Utilities" / "General" / "Sex" / "StreetClients.rpy"
STORY_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
EVENTS = PROJECT_ROOT / "game" / "Utilities" / "General" / "Events" / "events.rpy"
GEORGETT_CHURCH = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "IntGeorgettAfterCermon.rpy"
GEORGETT_CHURCH_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "InitGeorgettChurch.rpy"
LIZA_CHURCH = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "IntLizettAfterCermon.rpy"
CHURCH_AFTER_CERMON = PROJECT_ROOT / "game" / "Town" / "Church" / "ChurchAfterCermon.rpy"
CHURCH_ISPOVED = PROJECT_ROOT / "game" / "Town" / "Church" / "ChurchIspoved.rpy"
CHURCH_ROOM = PROJECT_ROOT / "game" / "Town" / "Church" / "Church.rpy"
NEXT_DAY_NEW_EVENTS = PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay_NewDayEvents.rpy"
PEOPLE_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
MIGRATION = PROJECT_ROOT / "game" / "TractirSaveSync.rpy"
STORY_BOARD = PROJECT_ROOT / "game" / "Utilities" / "General" / "Screens" / "StoryThreadBoard.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def _data_block(source, data_class, info_class):
    return source.split(data_class, 1)[1].split(info_class, 1)[0]


def test_georgett_uses_data_info_runtime_shape():
    source = _source(GEORGETT_INIT)

    assert "class GeorgettData(PeopleData):" in source
    assert "class GeorgettInfo(Girl):" in source
    assert "define GeorgettStaticData = GeorgettData()" in source
    assert "default Georgett = GeorgettInfo()" in source
    assert "people.register(GeorgettStaticData, Georgett)" in source
    assert "class Georgett(Girl):" not in source


def test_georgett_owns_room_specific_talk_arguments_and_portrait_data():
    source = _source(GEORGETT_INIT)

    assert 'def action_data(self, where_id=""):' in source
    assert 'if room_key == "PortStreets":' in source
    assert 'data["talk_args"] = (self.name, "street")' in source
    assert 'data["picture_path"] = "images/georgett/portraits/portrait.jpg"' in source
    assert 'elif room_key == "TavernMain":' in source
    assert 'data["talk_args"] = (self.name, "tavern")' in source


def test_liza_uses_data_info_runtime_shape():
    source = _source(LIZA_INIT)

    assert "class LizaData(PeopleData):" in source
    assert "class LizaInfo(Girl):" in source
    assert "define LizaStaticData = LizaData()" in source
    assert "default Liza = LizaInfo()" in source
    assert "people.register(LizaStaticData, Liza)" in source
    assert "class Liza(Girl):" not in source
    assert 'unknown_name = "Молодая женщина"' in source
    assert "self.known = False" in source


def test_liza_has_no_legacy_var_runtime_owner():
    liza = _source(LIZA_INIT)

    assert "self.uses_own_var_state = True" not in liza
    assert "STORY_DEFAULTS" not in liza
    assert "self.var =" not in liza
    assert "Liza.var = LizaVar" not in liza
    assert "self.var = LizaVar" not in liza
    assert "def sync_liza_maps" not in liza
    assert "def sync_from_liza_maps" not in liza
    assert "sync_shared_state" not in liza
    assert "sync_from_shared_state" not in liza
    assert "LizaVar" not in liza
    assert "sync_shared_state" not in liza
    assert "sync_from_shared_state" not in liza
    assert "sync_shared_state" not in liza
    assert "sync_from_shared_state" not in liza
    assert "sync_shared_state" not in liza
    assert "sync_from_shared_state" not in liza

    for path in (PROJECT_ROOT / "game").rglob("*"):
        if "saves" in path.parts:
            continue
        if path == MIGRATION:
            continue
        if path.suffix.lower() not in {".rpy", ".json"}:
            continue
        source = _source(path)
        assert "LizaVar" not in source, str(path)


def test_georgett_liza_data_classes_keep_static_identity_only():
    georgett = _data_block(_source(GEORGETT_INIT), "class GeorgettData(PeopleData):", "class GeorgettInfo(Girl):")
    liza = _data_block(_source(LIZA_INIT), "class LizaData(PeopleData):", "class LizaInfo(Girl):")

    for block, code_name, display_name in [
        (georgett, "georgett", "Жоржетта"),
        (liza, "liza", "Лизетта"),
    ]:
        assert f'code_name = "{code_name}"' in block
        assert f'fullname="{display_name}"' in block
        assert "birth_date" in block
        assert "schedule_source" in block
        assert "card_image" not in block
        assert "age=" not in block
        assert "self.stats" not in block
        assert "self.jobs" not in block
        assert "self.wardrobe" not in block
        assert "self.var" not in block


def test_georgett_liza_runtime_owns_stats_jobs_story_and_pregnancy():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)

    for source, name in [(georgett, "georgett"), (liza, "liza")]:
        assert "self.stats = {" in source
        assert "self.jobs = {" in source
        assert "self.wardrobe = {" in source
        assert "def reset_daily" in source
        assert '"pregnancy":' in source
        assert "def pregnancy_stage" not in source
        assert '"pregnancy": 0' in source
        assert '"pregfather": ""' in source
        assert '"breastfeed": 0' in source
        assert "self.flirted_today" not in source
        assert "FlirtedToday" not in source
        assert "def can_ask_topic" in source

    assert "self.ensure_story_defaults()" in georgett
    assert "self.ensure_story_defaults()" not in liza
    for field_name in (
        "witnessed_church_after_sermon", "discussed_georgett_gerhard",
        "prostitution_started", "has_seen_clients", "asked_about_clients",
        "asked_about_pregnancy", "asked_about_sex", "glory_hole_mentioned",
        "glory_hole_asked", "portstreet_clients_seen_today",
    ):
        assert "self.%s =" % field_name in liza


def test_georgett_and_liza_inherit_common_npc_state_methods_without_shadow_copies():
    character_blocks = [
        _source(GEORGETT_INIT).split("class GeorgettInfo(Girl):", 1)[1],
        _source(LIZA_INIT).split("class LizaInfo(Girl):", 1)[1],
    ]
    runtime = _source(PEOPLE_RUNTIME)

    assert "STORY_DEFAULTS = {" in character_blocks[0]
    assert "STORY_DEFAULTS" not in character_blocks[1]
    for block in character_blocks:
        for method in [
            "ensure_story_defaults",
            "story_value",
            "set_story_value",
            "getLocation",
            "talk_count",
            "can_talk_today",
            "add_relation",
            "finish_talk",
            "mark_asked_topic",
        ]:
            assert f"def {method}(" not in block
            assert f"def {method}(" in runtime

    georgett = character_blocks[0]
    for method in [
        "display_name",
        "arousal_value",
        "set_arousal",
        "add_arousal",
        "set_cock_position",
        "cock_in",
        "sex_busy",
        "set_sex_busy",
        "cum_state",
        "pregnancy_days",
        "record_orgasm_given",
        "player_cum",
    ]:
        assert f"def {method}(" not in georgett
        assert f"def {method}(" in runtime

    assert "def ensure_sex_state(self):" in georgett
    assert "def reset_daily(self, full=False):" in georgett
    assert "def clear_cum(self, *keys):" in georgett


def test_georgett_liza_hired_flag_is_runtime_state_and_syncs_jobs():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)
    talk = _source(GEORGETT_TALK)
    runtime = _source(PEOPLE_RUNTIME)

    for source in (georgett, liza):
        assert "self.hired" not in source
        assert "def set_hired(self, hired=True):" not in source
        assert "def can_work_tavern(self):" not in source
        assert "def can_use_gloryhole(self):" not in source
        assert "self.current_location" not in source
        info_block = source.split("Info(Girl):", 1)[1]
        assert "self.schedule_source" not in info_block
        assert 'self.location = ""' not in source

    girl_block = runtime.split("class Girl(BaseNPC):", 1)[1]
    assert "def set_hired(self, hired=True):" in girl_block
    assert 'self.jobs["jobWhoreAvail"] = 1 if hired_value else 0' in girl_block
    assert 'self.jobs["jobwhore"] = 1 if hired_value else 0' in girl_block
    assert "def can_work_tavern(self):" in girl_block
    assert 'return people_to_int(self.jobs.get("jobWhoreAvail", 0), 0) > 0' in girl_block
    assert "def can_use_gloryhole(self):" in girl_block

    assert "Georgett.set_hired(True)" in talk
    assert "Liza.set_hired(True)" in talk
    assert 'Georgett.jobs["jobWhoreAvail"] = 1' not in talk
    assert 'Liza.jobs["jobWhoreAvail"] = 1' not in talk
    assert "jump StreetTavern" not in talk
    assert "jump PortStreets" not in talk

    native_menu = talk.split("label IntGeorgettTalk", 1)[1]
    assert "elif Liza.rel < 8:" in native_menu
    assert "else:" in native_menu
    assert "Georgett.set_hired(True)" in native_menu
    assert "Liza.set_hired(True)" in native_menu
    assert 'IntGeorgettTalkApply(girl_name, girl_loc, "invite_tavern")' not in talk


def test_georgett_liza_removed_hidden_wrapper_patterns():
    combined = _source(GEORGETT_INIT) + "\n" + _source(LIZA_INIT)

    for forbidden in [
        "globals()",
        "renpy.store",
        "dir()",
        "after_load_update",
        "config.after_load_callbacks",
        "calendar_make_birth_record",
        "peopleInfo['georgett']",
        "peopleInfo['liza']",
    ]:
        assert forbidden not in combined


def test_georgett_liza_share_live_portstreet_behavior_without_dead_planned_methods():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)
    runtime = _source(PEOPLE_RUNTIME)
    girl_block = runtime.split("class Girl(BaseNPC):", 1)[1]

    for source in (georgett, liza):
        assert "def portstreet_visible_now(self):" not in source
        assert "def mark_portstreet_clients_seen(self):" not in source
        assert "def can_ask_about_priest(self):" not in source
        assert "def can_schedule_dress_shop_visit(self):" not in source
        assert "def can_schedule_barber_visit(self):" not in source

    assert "def portstreet_visible_now(self):" in girl_block
    assert "def mark_portstreet_clients_seen(self):" in girl_block
    assert 'self.var["portstreet_clients_seen_today"] = 1' in girl_block
    assert 'return self.set_story_value("seeclients", 1)' in girl_block
    assert "self.portstreet_clients_seen_today = False" in liza
    clients = _source(STREET_CLIENTS)
    assert "Liza.portstreet_clients_seen_today = True" in clients
    assert "Liza.has_seen_clients = True" in clients
    assert "Liza.mark_portstreet_clients_seen()" not in clients


def test_georgett_liza_talk_labels_use_class_topic_state():
    georgett = _source(GEORGETT_TALK)
    liza = _source(LIZA_TALK)

    assert 'Georgett.can_ask_topic("clients")' in georgett
    assert 'Georgett.mark_asked_topic("askclients")' in georgett
    assert "Georgett.finish_talk()" in georgett
    assert "GeorgettVar[" not in georgett
    assert "GeorgettVar.get" not in georgett

    assert 'Liza.can_ask_topic("clients")' in liza
    assert "Liza.asked_about_clients = True" in liza
    assert "Liza.asked_about_sex = True" in liza
    assert "Liza.asked_about_pregnancy = True" in liza
    assert "Liza.discussed_georgett_gerhard = True" in liza
    assert "Liza.glory_hole_mentioned = True" in liza
    assert "Liza.glory_hole_asked = True" in liza
    assert "Liza.mark_asked_topic(" not in liza
    assert "Liza.finish_talk()" in liza
    assert "label IntLizaTalkMenu" not in liza
    assert "while True:" in liza
    assert "jump IntLizaTalkMenu" not in liza
    assert "label IntLizaTalkRefresh" not in liza
    assert "label IntLizaTalkApply" not in liza
    assert "main_ui_runtime.action_items" not in liza
    assert "MenuItem(" not in liza
    assert "choice_code" not in liza
    assert "if _liza_talk_new:" in liza
    assert "call ShowGirlCard(girl_name_ilt)" in liza
    assert "jump IntLizaTalk" not in liza
    assert "GirlNameILT" not in liza
    assert "GirlLocILT" not in liza
    assert "NpcActionLookState" not in liza
    assert "LizaVar.setdefault" not in liza
    assert "GeorgettVar.setdefault" not in liza
    assert "LizaVar[" not in liza
    assert "LizaVar.get" not in liza


def test_liza_v55_migration_consumes_legacy_state_once():
    migration = _source(MIGRATION)
    block = migration.split("def updateSave_V55():", 1)[1].split("label before_load:", 1)[0]

    assert "define currentVersion = 71" in migration
    assert "if loaded_version < 56:" in migration
    assert "updateSave_V55()" in migration
    for old_key, field_name in (
        ("SawChurchAfterCermon", "witnessed_church_after_sermon"),
        ("TalkChurchAfterCermonGeorgett", "discussed_georgett_gerhard"),
        ("ProstStart", "prostitution_started"),
        ("seeclients", "has_seen_clients"),
        ("askclients", "asked_about_clients"),
        ("askpregnancy", "asked_about_pregnancy"),
        ("asksex", "asked_about_sex"),
        ("GloryHoleMentioned", "glory_hole_mentioned"),
        ("GloryHoleAsked", "glory_hole_asked"),
        ("portstreet_clients_seen_today", "portstreet_clients_seen_today"),
    ):
        assert 'liza_var.pop("%s"' % old_key in block
        assert "Liza.%s =" % field_name in block
    assert 'liza_var.pop("TalkChurchAfterCermon", None)' in block
    assert 'globals().pop("LizaVar", None)' in block

    identity_migration = migration.split("def updateSave_V70():", 1)[1].split(
        "# Saved objects must be upgraded", 1
    )[0]
    assert "if loaded_version < 71:" in migration
    assert "updateSave_V70()" in migration
    assert "Liza.known = bool(" in identity_migration
    assert "people_to_int(Liza.rel, 0) > 0" in identity_migration


def test_georgett_first_meeting_is_owned_by_the_scheduled_npc_talk_label():
    port = _source(PORT_STREETS)
    talk = _source(GEORGETT_TALK)
    georgett = _source(GEORGETT_INIT)

    entry = port.split("label PortStreets:", 1)[1].split("label PortStreetsBackAlley", 1)[0]
    assert '$ main_ui_runtime.mode = "scene"' in entry
    assert '$ main_ui_runtime.selected_char = ""' in entry
    assert '$ main_ui_runtime.talk_picture = ""' in entry
    assert "$ main_ui_runtime.clear_contexts()" in entry
    assert '$ main_ui_runtime.girl_key = ""' in entry
    assert '$ main_ui_runtime.object_id = ""' in entry
    assert "people_to_int(Georgett.rel, 0) == 0" in port
    assert 'action_id="meet_georgett"' not in port
    assert 'target="PortStreetsMeetGeorgett"' not in port
    assert "label PortStreetsMeetGeorgett:" not in port
    assert "На углу стоит молодая женщина" in port
    assert 'vscene "images/georgett/Port/wait.jpg"' in port
    assert "return self.portstreet_visible_now()" in georgett
    assert "return self.portstreet_visible_now() and people_to_int(self.rel, 0) != 0" not in georgett

    first_talk = talk.split('label IntGeorgettTalk(girl_name="georgett", girl_loc=""):', 1)[1].split(
        "label IntGeorgettSmalltalk", 1
    )[0]
    assert "Georgett.mark_known()" in first_talk
    assert "-Привет красавчик!" in first_talk
    assert "Georgett.add_relation(1)" in first_talk
    assert 'girl_loc == "street" and not bool(Georgett.known)' in first_talk
    assert 'girl_loc == "street" and people_to_int(Georgett.rel, 0) <= 0' not in first_talk
    assert "Как прошел твой день?" in first_talk


def test_portstreets_clients_are_repeatable_action_events_from_classes():
    georgett = _source(GEORGETT_INIT)
    georgett_events = _source(GEORGETT_EVENTS)
    liza = _source(LIZA_INIT)
    liza_events = _source(LIZA_EVENTS)
    port = _source(PORT_STREETS)
    clients = _source(STREET_CLIENTS)
    runtime = _source(STORY_RUNTIME)

    assert "def portstreet_client_event_available" in georgett
    assert "def portstreet_client_event_available" in liza
    georgett_schedule = _source(GEORGETT_SCHEDULE)
    liza_schedule = _source(LIZA_SCHEDULE)
    assert '"weekdays": [1, 2, 3, 4, 6, 7]' in georgett_schedule
    assert '"start": "19:00"' in georgett_schedule
    assert '"end": "21:30"' in georgett_schedule
    assert '"weekdays": [1, 2, 3, 4, 6, 7]' in liza_schedule
    assert '"start": "19:00"' in liza_schedule
    assert '"end": "21:30"' in liza_schedule
    assert "def portstreet_work_hour" not in georgett
    assert "def portstreet_work_hour" not in liza
    assert "calendar_v2.clock_minutes()" not in georgett
    assert "calendar_v2.clock_minutes()" not in liza
    assert 'CheckIfSexEventExist(self.code_name, 3, "Prostitution")' in georgett
    assert 'CheckIfSexEventExist(self.code_name, 3, "Prostitution")' in liza
    assert 'return people_to_int(self.rel, 0) > 0 and self.portstreet_work_active()' in georgett

    georgett_schedule_data = json.loads(georgett_schedule)
    georgett_port_entry = next(
        entry for entry in georgett_schedule_data["entries"] if entry["label"] == "portstreets_work"
    )
    assert georgett_port_entry["talkable"] is True
    assert georgett_port_entry.get("working", False) is False

    assert '"story_georgett_portstreet_clients"' in runtime
    assert '"story_liza_portstreet_clients"' in runtime
    assert '"#Georgett.portstreet_client_event_available()"' in runtime
    assert '"#Liza.portstreet_client_event_available()"' in runtime
    assert "threaded=False" in runtime

    assert 'Call("StreetClients"' not in port
    assert "_port_clients_action" not in port
    assert "rooms.current.build_action_items()" in port
    assert "set_portstreet_visible" not in port
    assert '"street_clients_georgett"' not in runtime
    assert '"street_clients_liza"' not in runtime
    assert '"street_clients"' in runtime
    assert 'story_event_available("PortStreets", "street_clients")' in port
    assert 'if location_key == "PortStreets"' not in _source(EVENTS)
    assert 'GeorgettVar.get("TalkChurchAfterCermonLiza"' not in port
    assert 'LizaVar.get("ProstStart"' not in port
    assert 'CheckIfSexEventExist(GirlNamePS1, time, "Prostitution")' not in port
    assert "time in (0, 1, 2)" not in port
    assert 'LizaVar["seeclients"]' not in clients
    assert 'GeorgettVar["seeclients"]' not in clients
    assert "call screen main_ui" not in clients
    assert "main_ui_runtime.action_items" not in clients
    assert "jump PortStreets" not in clients
    assert "menu:" in clients
    assert "label story_georgett_portstreet_clients:" not in clients
    assert "label story_liza_portstreet_clients:" not in clients
    assert "label story_georgett_portstreet_clients:" in georgett_events
    assert "label story_liza_portstreet_clients:" in liza_events
    assert "jump PortStreets" not in georgett_events
    assert "jump PortStreets" not in liza_events
    assert 'GetSexEventFromTable(girl_name, 3, "Prostitution")' in clients
    assert "$ main_ui_begin_native_scene_state(\"Подворотня\")" in clients
    assert "show screen main_ui" in clients
    assert '"Вернуться в переулок"' in clients


def test_port_back_alley_uses_native_menu_and_returns_to_event_owner():
    port = _source(PORT_STREETS)
    back_alley = port.split("label PortStreetsBackAlley", 1)[1].split(
        "label PortStreetsBottleMenu", 1
    )[0]

    assert "menu:" in back_alley
    assert "main_ui_runtime.action_items" not in back_alley
    assert "call screen main_ui" not in back_alley
    assert "$ main_ui_begin_native_scene_state(\"Подворотня\")" in back_alley
    assert "show screen main_ui" in back_alley
    assert "jump PortStreets" not in back_alley
    assert "call street_clients_watch" in back_alley
    assert "_port_ui_return" not in port


def test_portstreets_explains_georgett_client_absence_from_npc_authority():
    port = _source(PORT_STREETS)
    entry = port.split("label PortStreets:", 1)[1].split("label PortStreetsBackAlley", 1)[0]

    assert "if Georgett.portstreet_client_event_available():" in entry
    assert "Почему-то Жоржетты сейчас нет на ее обычном месте. Где же она может быть?" in entry


def test_georgett_and_liza_extend_the_shared_sex_state_schema():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)
    georgett_state = georgett.split("def ensure_sex_state(self):", 1)[1].split(
        "def initialize_new_game_state", 1
    )[0]
    liza_state = liza.split("def ensure_sex_state(self):", 1)[1].split(
        "def sex_setup", 1
    )[0]

    assert "super(GeorgettInfo, self).ensure_sex_state()" in georgett_state
    assert "super(LizaInfo, self).ensure_sex_state()" in liza_state
    for shared_key in ("arousal", "somebody_cums", "cock_position", "cum_inside_you"):
        assert f'"{shared_key}"' not in georgett_state
        assert f'"{shared_key}"' not in liza_state


def test_liza_uses_player_intimacy_authority_without_npc_wrappers():
    liza = _source(LIZA_INIT)
    sex = _source(LIZA_SEX)

    for method_name in (
        "player_arousal",
        "set_player_arousal",
        "add_player_arousal",
        "can_player_cum",
    ):
        assert "def %s(" % method_name not in liza
        assert "Liza.%s(" % method_name not in sex

    assert "_you_arousal = player.intimacy.arousal_value()" in sex
    assert "_can_player_cum = player.intimacy.can_cum()" in sex
    assert "player.intimacy.add_arousal(" in sex
    assert "player.intimacy.set_arousal(0)" in sex
    assert "or player.intimacy.arousal_value() >= 100" not in liza + sex


def test_church_after_sermon_events_are_threaded_from_classes():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)
    people_runtime = _source(PEOPLE_RUNTIME)
    runtime = _source(STORY_RUNTIME)
    church_entry = _source(CHURCH_AFTER_CERMON)
    georgett_scene = _source(GEORGETT_CHURCH)
    liza_scene = _source(LIZA_CHURCH)
    confession = _source(CHURCH_ISPOVED)
    next_day = _source(NEXT_DAY_NEW_EVENTS)

    assert "def church_after_sermon_event_available" in people_runtime
    assert "def church_after_sermon_event_available" not in georgett
    assert "def church_after_sermon_event_available" not in liza
    assert "after_sermon_stage" not in georgett
    assert "after_sermon_stage" not in liza
    assert "def can_trigger_after_sermon_event" in georgett
    assert "def can_trigger_after_sermon_event" in liza
    assert "def can_trigger_church_service_event" not in liza
    assert 'CheckIfSexEventExist(self.code_name, 99, "Priest")' in people_runtime
    assert 'CheckIfSexEventExist(self.code_name, 99, "Priest")' not in georgett
    assert 'CheckIfSexEventExist(self.code_name, 99, "Priest")' not in liza

    assert '"story_georgett_church_after_sermon"' in runtime
    assert '"story_liza_church_after_sermon"' in runtime
    assert '"after_cermon_walk"' in runtime
    assert '"#Georgett.church_after_sermon_event_available()"' in runtime
    assert '"#Liza.church_after_sermon_event_available()"' in runtime
    georgett_after = runtime.split('"story_georgett_church_after_sermon"', 1)[1].split('define franThreadList', 1)[0]
    liza_after = runtime.split('"story_liza_church_after_sermon"', 1)[1].split('define georgettThreadList', 1)[0]
    assert '"#church_after_cermon_action_visible()"' not in georgett_after
    assert '"#church_after_cermon_action_visible()"' not in liza_after

    assert "church_aftercermon_pick_scene_code" not in church_entry
    assert 'call checkTriggers("Church", "after_cermon_walk", 0)' in church_entry
    assert "AfterCermonLizett" not in _source(CHURCH_ROOM)
    assert "after_liza" not in _source(CHURCH_ROOM)

    assert "label story_georgett_church_after_sermon:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_1:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_2:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_3:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_4:" in georgett_scene
    assert "label AfterCermonGeorgett:" not in georgett_scene
    assert "label IntGeorgettAfterCermon:" not in georgett_scene
    assert "MenuItem(" not in georgett_scene
    assert "main_ui_runtime.action_items" not in georgett_scene
    assert "renpy.restart_interaction" not in georgett_scene
    assert "ChurchRestore" not in georgett_scene
    assert "ChurchAfterCermon[" not in georgett_scene
    assert "ChurchAfterCermon.get" not in georgett_scene
    assert "after_sermon_stage" not in georgett_scene
    assert "calendar_v2.advance_minutes(60)" in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispoved1.jpg"' in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispovedstep2_1.jpg"' in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispovedstep2_2.jpg"' in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispovedstep4.jpg"' in georgett_scene
    assert "label story_liza_church_after_sermon:" in liza_scene
    assert "label story_liza_church_after_sermon_look_1:" in liza_scene
    assert "label story_liza_church_after_sermon_look_2:" in liza_scene
    assert "label story_liza_church_after_sermon_look_3:" in liza_scene
    assert "label story_liza_church_after_sermon_look_4:" in liza_scene
    assert "label AfterCermonLizett:" not in liza_scene
    assert "label IntLizettAfterCermon:" not in liza_scene
    assert "MenuItem(" not in liza_scene
    assert "main_ui_runtime.action_items" not in liza_scene
    assert "renpy.restart_interaction" not in liza_scene
    assert "ChurchAfterCermon[" not in liza_scene
    assert "ChurchAfterCermon.get" not in liza_scene
    assert "after_sermon_stage" not in liza_scene
    assert 'vscene "images/liza/ispoved/ispoved1.jpg"' in liza_scene
    assert 'vscene "images/liza/ispoved/ispovedstep2_1.jpg"' in liza_scene
    assert 'vscene "images/liza/ispoved/ispovedstep4_1.jpg"' in liza_scene
    assert 'GeorgettVar.get("SawChurchAfterCermon"' not in georgett_scene
    assert 'GeorgettVar["SawChurchAfterCermon"]' not in georgett_scene
    assert 'LizaVar.get("SawChurchAfterCermon"' not in liza_scene
    assert 'LizaVar["SawChurchAfterCermon"]' not in liza_scene

    assert 'Georgett.set_story_value("georgettadmit", 1)' in confession
    assert 'Georgett.set_story_value("churchgeorgettadmit", 1)' in confession
    assert 'Georgett.set_story_value("churchlizaadmit", 1)' in confession
    assert "Georgett.can_trigger_after_sermon_event()" in next_day
    assert "Liza.can_trigger_after_sermon_event()" in next_day
    assert "Liza.can_trigger_church_service_event()" not in next_day


def test_georgett_church_service_preserves_the_single_authored_action_flow():
    georgett = _source(GEORGETT_INIT)
    georgett_church_events = _source(GEORGETT_CHURCH_EVENTS)
    runtime = _source(STORY_RUNTIME)
    story_board = _source(STORY_BOARD)
    church = _source(CHURCH_ROOM)

    assert "def church_service_quick_sex_event_available" not in georgett
    assert "def can_trigger_church_service_event" not in georgett
    assert "def knows_player" not in georgett
    assert '"church_bench_seen": 0' not in georgett
    assert '"church_doggy_seen": 0' not in georgett
    assert '"church_liza_seen": 0' not in georgett
    assert '"ChurchServiceBench"' not in runtime
    assert '"ChurchServiceDoggy"' not in runtime
    assert '"ChurchServiceWithLiza"' not in runtime
    assert "georgett_church_service_bench" not in story_board
    assert "georgett_church_service_doggy" not in story_board
    assert "georgett_church_service_with_liza" not in story_board

    assert "label ChurchServiceGeorgett:" not in church
    assert "label ChurchServiceGeorgett:" in georgett_church_events
    assert "label ChurchGeorgettQuickSex:" in georgett_church_events
    service_menu = church.split("label ChurchServiceMenu", 1)[1].split("label ChurchServiceMother", 1)[0]
    attendee_text = church.split("def church_service_attendees_text():", 1)[1].split(
        "ChurchRoomDefinition = Room(", 1
    )[0]
    assert "info = people.get_info(key)" in attendee_text
    assert "info.display_name()" in attendee_text
    assert "people_display_name(key)" not in attendee_text
    assert 'MenuItem("Предложить Жоржетте перепихнуться по быстрому", Call("ChurchGeorgettQuickSex"))' not in service_menu
    assert 'MenuItem("Предложить Жоржетте перепихнуться по быстрому", Call("ChurchGeorgettQuickSex"))' in georgett_church_events
    assert 'player.intimacy.can_cum()' in georgett_church_events
    assert 'people_to_int(Georgett.rel, 0) >= 2' in georgett_church_events
    assert 'people_to_int(Georgett.sex_stat("sexacts", 0), 0) >= 3' in georgett_church_events
    assert 'Georgett.corruption' not in church.split("label ChurchServiceMenu", 1)[1].split("label ChurchServiceMother", 1)[0]
    assert '$ Georgett.set_story_value("foundinchurch", 0)' in church
    assert '$ Georgett.set_story_value("foundinchurch", 1)' in georgett_church_events
    assert 'if Georgett.rel < 6:' in georgett_church_events
    assert '"Ты что, сдурел!' in georgett_church_events
    assert '$ main_ui_runtime.action_title = "Жоржетта"' in georgett_church_events
    assert '$ main_ui_runtime.action_title = "Разговор с Жоржеттой"' in georgett_church_events
    assert 'MenuItem("Назад", Call("ChurchServiceMenu", True))' in georgett_church_events
    assert 'main_ui_runtime.action_items = [MenuItem("Назад", Call("ChurchServiceGeorgett"))]' in georgett_church_events
    assert 'procedural_randint(1, 2, "church_georgett_variant_' in georgett_church_events
    assert 'if Georgett.story_value("askkids", 0):' in georgett_church_events
    assert '$ Liza.mark_known()' in georgett_church_events
    assert '$ _church_georgett_variant = "withliza"' in georgett_church_events
    assert 'call ChurchRestore' not in georgett_church_events
    assert 'AdvanceTimeAndRestore' not in georgett_church_events
    assert 'call AdvanceTime(' not in georgett_church_events
    assert 'jump Church' in georgett_church_events
    assert 'calendar_v2.advance_minutes(60)' in georgett_church_events
    assert 'vscene "images/georgett/church/cermon.jpg"' in georgett_church_events
    assert 'vscene "images/georgett/church/cermonliza.jpg"' in georgett_church_events
    assert '"images/georgett/church/bench/bench"' in georgett_church_events
    assert '"images/georgett/church/doggy/doggy"' in georgett_church_events
    assert '"images/georgett/church/withLiza.jpg/withliza"' in georgett_church_events
    assert 'Georgett.set_story_value("fuckinchurch", 1)' in georgett_church_events
    assert 'Georgett.set_story_value("lizasawinchurch", 1)' in georgett_church_events
    assert 'player_record_orgasm("georgett_church", "georgett")' not in georgett_church_events
    assert 'player.change_stat("fun"' not in georgett_church_events
    assert 'GeorgettVar["foundinchurch"]' not in church
    assert 'GeorgettVar["fuckinchurch"]' not in church
    assert 'GeorgettVar["lizasawinchurch"]' not in church

    confession = _source(CHURCH_ISPOVED)
    assert 'Georgett.story_value("fuckinchurch", 0)' in confession
    assert 'Georgett.story_value("lizasawinchurch", 0)' in confession
    assert 'Georgett.story_value("church_bench_seen", 0)' not in confession
    assert 'Georgett.story_value("church_doggy_seen", 0)' not in confession
    assert 'Georgett.story_value("church_liza_seen", 0)' not in confession
    assert "menu:" in confession
    assert "main_ui_runtime.action_items" not in confession
    assert "ChurchIspovedChoice" not in confession
    assert "ChurchIspovedMenu" not in confession
