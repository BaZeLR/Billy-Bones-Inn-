from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GEORGETT_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "InitGeorgett.rpy"
LIZA_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "InitLiza.rpy"
GEORGETT_TALK = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "IntGeorgettTalk.rpy"
LIZA_TALK = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "IntLizaTalk.rpy"
PORT_STREETS = PROJECT_ROOT / "game" / "Town" / "PortStreets.rpy"
STREET_CLIENTS = PROJECT_ROOT / "game" / "Utilities" / "General" / "Sex" / "StreetClients.rpy"
STORY_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
GEORGETT_CHURCH = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "IntGeorgettAfterCermon.rpy"
GEORGETT_CHURCH_EVENTS = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Georgett" / "InitGeorgettChurch.rpy"
LIZA_CHURCH = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Liza" / "IntLizettAfterCermon.rpy"
CHURCH_AFTER_CERMON = PROJECT_ROOT / "game" / "Town" / "Church" / "ChurchAfterCermon.rpy"
CHURCH_ISPOVED = PROJECT_ROOT / "game" / "Town" / "Church" / "ChurchIspoved.rpy"
CHURCH_ROOM = PROJECT_ROOT / "game" / "Town" / "Church" / "Church.rpy"
NEXT_DAY_NEW_EVENTS = PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay_NewDayEvents.rpy"


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
    assert "peopleData[GirlName] = GeorgettStaticData" in source
    assert "peopleInfo[GirlName] = Georgett" in source
    assert "class Georgett(Girl):" not in source


def test_liza_uses_data_info_runtime_shape():
    source = _source(LIZA_INIT)

    assert "class LizaData(PeopleData):" in source
    assert "class LizaInfo(Girl):" in source
    assert "define LizaStaticData = LizaData()" in source
    assert "default Liza = LizaInfo()" in source
    assert "peopleData[GirlName] = LizaStaticData" in source
    assert "peopleInfo[GirlName] = Liza" in source
    assert "class Liza(Girl):" not in source


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
        assert "def ensure_story_defaults" in source
        assert "def sync_from_%s_maps" % name in source
        assert "def sync_%s_maps" % name in source
        assert "def reset_daily" in source
        assert "def pregnancy_stage" in source
        assert '"pregnancy": 0' in source
        assert '"pregfather": ""' in source
        assert '"breastfeed": 0' in source
        assert "self.flirted_today" not in source
        assert "FlirtedToday" not in source
        assert "def mark_asked_topic" in source
        assert "def can_ask_topic" in source
        assert "def finish_talk" in source


def test_georgett_liza_hired_flag_is_runtime_state_and_syncs_jobs():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)
    talk = _source(GEORGETT_TALK)

    for source, sync_name in [(georgett, "sync_georgett_maps"), (liza, "sync_liza_maps")]:
        assert "self.hired = False" in source
        assert "def set_hired(self, hired=True):" in source
        assert 'self.jobs["jobWhoreAvail"] = 1 if self.hired else 0' in source
        assert 'self.jobs["jobwhore"] = 1 if self.hired else 0' in source
        assert 'self.current_location = "TavernMain" if self.hired else "PortStreets"' in source
        assert f"self.{sync_name}()" in source
        assert "def can_work_tavern(self):" in source
        assert "return self.hired" in source

    assert "Georgett.set_hired(True)" in talk
    assert "Liza.set_hired(True)" in talk
    assert 'Georgett.jobs["jobWhoreAvail"] = 1' not in talk
    assert 'Liza.jobs["jobWhoreAvail"] = 1' not in talk


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


def test_georgett_liza_talk_labels_use_class_topic_state():
    georgett = _source(GEORGETT_TALK)
    liza = _source(LIZA_TALK)

    assert 'Georgett.can_ask_topic("clients")' in georgett
    assert 'Georgett.mark_asked_topic("askclients")' in georgett
    assert "Georgett.finish_talk()" in georgett
    assert "GeorgettVar[" not in georgett
    assert "GeorgettVar.get" not in georgett

    assert 'Liza.can_ask_topic("clients")' in liza
    assert 'Liza.mark_asked_topic("askclients")' in liza
    assert "Liza.finish_talk()" in liza
    assert "LizaVar.setdefault" not in liza
    assert "GeorgettVar.setdefault" not in liza
    assert "LizaVar[" not in liza
    assert "LizaVar.get" not in liza


def test_portstreets_clients_are_repeatable_action_events_from_classes():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)
    port = _source(PORT_STREETS)
    clients = _source(STREET_CLIENTS)
    runtime = _source(STORY_RUNTIME)

    assert "def portstreet_client_event_available" in georgett
    assert "def portstreet_client_event_available" in liza
    assert "calendar_v2.clock_minutes()" in georgett
    assert "calendar_v2.clock_minutes()" in liza
    assert 'CheckIfSexEventExist(self.code_name, 3, "Prostitution")' in georgett
    assert 'CheckIfSexEventExist(self.code_name, 3, "Prostitution")' in liza

    assert '"story_georgett_portstreet_clients"' in runtime
    assert '"story_liza_portstreet_clients"' in runtime
    assert '"street_clients_georgett"' in runtime
    assert '"street_clients_liza"' in runtime
    assert '"#Georgett.portstreet_client_event_available()"' in runtime
    assert '"#Liza.portstreet_client_event_available()"' in runtime
    assert "threaded=False" in runtime

    assert 'Call("StreetClients"' not in port
    assert 'Call("checkTriggers", "PortStreets", _port_clients_action, 0)' in port
    assert 'GeorgettVar.get("TalkChurchAfterCermonLiza"' not in port
    assert 'LizaVar.get("ProstStart"' not in port
    assert 'CheckIfSexEventExist(GirlNamePS1, time, "Prostitution")' not in port
    assert "time in (0, 1, 2)" not in port

    assert 'LizaVar["seeclients"]' not in clients
    assert 'GeorgettVar["seeclients"]' not in clients
    assert "label story_georgett_portstreet_clients:" in clients
    assert "label story_liza_portstreet_clients:" in clients
    assert 'GetSexEventFromTable(girl_name, 3, "Prostitution")' in clients


def test_church_after_sermon_events_are_threaded_from_classes():
    georgett = _source(GEORGETT_INIT)
    liza = _source(LIZA_INIT)
    runtime = _source(STORY_RUNTIME)
    church_entry = _source(CHURCH_AFTER_CERMON)
    georgett_scene = _source(GEORGETT_CHURCH)
    liza_scene = _source(LIZA_CHURCH)
    confession = _source(CHURCH_ISPOVED)
    next_day = _source(NEXT_DAY_NEW_EVENTS)

    assert "def church_after_sermon_event_available" in georgett
    assert "def church_after_sermon_event_available" in liza
    assert "def can_trigger_church_service_event" in liza
    assert 'CheckIfSexEventExist(self.code_name, 99, "Priest")' in georgett
    assert 'CheckIfSexEventExist(self.code_name, 99, "Priest")' in liza

    assert '"story_georgett_church_after_sermon"' in runtime
    assert '"story_liza_church_after_sermon"' in runtime
    assert '"after_cermon_walk"' in runtime
    assert '"#church_after_cermon_action_visible()"' in runtime
    assert '"#Georgett.church_after_sermon_event_available()"' in runtime
    assert '"#Liza.church_after_sermon_event_available()"' in runtime

    assert "church_aftercermon_pick_scene_code" not in church_entry
    assert 'call checkTriggers("Church", "after_cermon_walk", 0)' in church_entry

    assert "label story_georgett_church_after_sermon:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_1:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_2:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_3:" in georgett_scene
    assert "label story_georgett_church_after_sermon_look_4:" in georgett_scene
    assert "label AfterCermonGeorgett:" not in georgett_scene
    assert "label IntGeorgettAfterCermon:" not in georgett_scene
    assert "MenuItem(" not in georgett_scene
    assert "current_action_items" not in georgett_scene
    assert "renpy.restart_interaction" not in georgett_scene
    assert "ChurchRestore" not in georgett_scene
    assert "calendar_v2.advance_minutes(60)" in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispoved1.jpg"' in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispovedstep2_1.jpg"' in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispovedstep2_2.jpg"' in georgett_scene
    assert 'vscene "images/georgett/ispoved/ispovedstep4.jpg"' in georgett_scene
    assert "label story_liza_church_after_sermon:" in liza_scene
    assert 'GeorgettVar.get("SawChurchAfterCermon"' not in georgett_scene
    assert 'GeorgettVar["SawChurchAfterCermon"]' not in georgett_scene
    assert 'LizaVar.get("SawChurchAfterCermon"' not in liza_scene
    assert 'LizaVar["SawChurchAfterCermon"]' not in liza_scene

    assert 'Georgett.set_story_value("georgettadmit", 1)' in confession
    assert 'Georgett.set_story_value("churchgeorgettadmit", 1)' in confession
    assert 'Georgett.set_story_value("churchlizaadmit", 1)' in confession
    assert "Georgett.can_trigger_after_sermon_event()" in next_day
    assert "Liza.can_trigger_church_service_event()" in next_day


def test_georgett_church_service_events_are_threaded_from_explicit_conditions():
    georgett = _source(GEORGETT_INIT)
    georgett_church_events = _source(GEORGETT_CHURCH_EVENTS)
    runtime = _source(STORY_RUNTIME)
    church = _source(CHURCH_ROOM)

    assert "def church_service_quick_sex_event_available" not in georgett
    assert "def can_trigger_church_service_event" not in georgett
    assert "def knows_player" not in georgett
    assert '"church_bench_seen": 0' in georgett
    assert '"church_doggy_seen": 0' in georgett
    assert '"church_liza_seen": 0' in georgett

    assert '"ChurchServiceBench"' in runtime
    assert '"ChurchServiceDoggy"' in runtime
    assert '"ChurchServiceWithLiza"' in runtime
    assert '"story_georgett_church_service_bench"' in runtime
    assert '"story_georgett_church_service_doggy"' in runtime
    assert '"story_georgett_church_service_with_liza"' in runtime
    assert '7, (8, 9), None' in runtime
    assert '"#church_service_action_visible()"' in runtime
    assert '"#bool(Georgett.known) or bool(knowsMC.get(\'georgett\', False)) or people_to_int(Georgett.rel, 0) > 0"' in runtime
    assert '"#npc_schedule_georgett_church_visible()"' in runtime
    assert '"#people_to_int(Georgett.story_value(\'foundinchurch\', 0), 0) > 0"' in runtime
    assert '"#people_to_int(Georgett.story_value(\'askkids\', 0), 0) > 0"' in runtime
    assert '"#people_to_int(Georgett.story_value(\'fuckinchurch\', 0), 0) > 0"' in runtime
    assert '"#people_to_int(cametoday, 0) < people_to_int(cancumdaily, 0)"' in runtime
    assert '"#people_to_int(Friends.get(\'georgett\', Georgett.rel), 0) >= 6"' in runtime
    assert '"#people_to_int(Georgett.rel, 0) >= 6"' in runtime
    assert '"#people_to_int(sluttiness.get(\'georgett\', Georgett.corruption), 0) >= 50"' in runtime
    assert '"#people_to_int(Georgett.corruption, 0) >= 50"' in runtime
    assert '"#people_to_int(HadSex.get(\'georgett\', 0), 0) >= 3"' in runtime
    assert '"Church"' in runtime
    assert '"georgett_church_service_bench"' in runtime
    assert '"georgett_church_service_doggy"' in runtime
    assert '"georgett_church_service_with_liza"' in runtime

    assert "def church_georgett_quick_sex_visible" not in church
    assert 'Function(main_ui_call_label, "ChurchServiceGeorgett")' in church
    assert 'Georgett.can_trigger_church_service_event()' not in church
    assert "label ChurchServiceGeorgett:" not in church
    assert "label story_georgett_church_service_bench:" not in church
    assert "label story_georgett_church_service_doggy:" not in church
    assert "label story_georgett_church_service_with_liza:" not in church
    assert "label ChurchServiceGeorgett:" in georgett_church_events
    assert "label story_georgett_church_service_bench:" in georgett_church_events
    assert "label story_georgett_church_service_doggy:" in georgett_church_events
    assert "label story_georgett_church_service_with_liza:" in georgett_church_events
    assert 'story_event_available("Church", "georgett_church_service_bench")' in georgett_church_events
    assert 'story_event_available("Church", "georgett_church_service_doggy")' in georgett_church_events
    assert 'story_event_available("Church", "georgett_church_service_with_liza")' in georgett_church_events
    assert 'findAvailableEvents(True)' in georgett_church_events
    assert 'call checkTriggers("Church", "georgett_church_service_bench", 0)' in georgett_church_events
    assert 'call checkTriggers("Church", "georgett_church_service_doggy", 0)' in georgett_church_events
    assert 'call checkTriggers("Church", "georgett_church_service_with_liza", 0)' in georgett_church_events
    assert 'call ChurchRestore' not in georgett_church_events
    assert 'AdvanceTimeAndRestore' not in georgett_church_events
    assert 'call AdvanceTime(' not in georgett_church_events
    assert 'jump Church' in georgett_church_events
    assert 'calendar_v2.advance_minutes(60)' in georgett_church_events
    assert 'vscene "images/georgett/church/cermon.jpg"' in georgett_church_events
    assert 'vscene "images/georgett/church/cermonliza.jpg"' in georgett_church_events
    assert 'vscene "images/georgett/church/bench/bench1.jpg"' in georgett_church_events
    assert 'vscene "images/georgett/church/doggy/doggy1.jpg"' in georgett_church_events
    assert 'vscene "images/georgett/church/withLiza.jpg/withliza1.jpg"' in georgett_church_events
    assert 'Georgett.set_story_value("church_bench_seen", 1)' in georgett_church_events
    assert 'Georgett.set_story_value("church_doggy_seen", 1)' in georgett_church_events
    assert 'Georgett.set_story_value("church_liza_seen", 1)' in georgett_church_events
    assert 'player_record_orgasm("georgett_church_bench", "georgett")' in georgett_church_events
    assert 'player_record_orgasm("georgett_church_doggy", "georgett")' in georgett_church_events
    assert 'player_record_orgasm("georgett_church_liza", "georgett")' in georgett_church_events
    assert "fun = min(100, int(fun or 0) + 4)" in georgett_church_events
    assert "label church_georgett_sex:" not in church
    assert 'GeorgettVar["foundinchurch"]' not in church
    assert 'GeorgettVar["fuckinchurch"]' not in church
    assert 'GeorgettVar["lizasawinchurch"]' not in church

    confession = _source(CHURCH_ISPOVED)
    assert 'Georgett.story_value("church_bench_seen", 0)' in confession
    assert 'Georgett.story_value("church_doggy_seen", 0)' in confession
    assert 'Georgett.story_value("church_liza_seen", 0)' in confession
    assert 'ChurchIspovedChoice", "church_bench"' in confession
    assert 'ChurchIspovedChoice", "church_doggy"' in confession
    assert 'ChurchIspovedChoice", "church_liza"' in confession
