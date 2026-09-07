import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_intimate_jobs_place_each_worker_in_the_room_owned_by_that_job():
    runtime = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    for person in ("georgett", "liza"):
        schedule = json.loads(_source("game/NPC/Schedules/%s.json" % person))
        assert all("tavern_whore_shift" not in row["label"] for row in schedule["entries"])
        assert all("glory_hole_shift" not in row["label"] for row in schedule["entries"])

    schedule_owner = runtime.split("def tavern_service_schedule_entry", 1)[1].split("def schedule_entry", 1)[0]
    assert 'location="TavernGloryHole" if target == "gloryhole" else "TavernMain"' in schedule_owner
    assert 'player.tavern_management.is_open_at(weekday_value, time_value)' in schedule_owner
    assert 'label="tavern_glory_hole_shift" if target == "gloryhole" else "tavern_intimate_shift"' in schedule_owner


def test_completed_glory_hole_is_a_room_with_a_separate_check_scene():
    glory = _source("game/Inn/TavernGloryHole.rpy")
    main = _source("game/Inn/TavernMain.rpy")

    assert 'RoomExit(label="Идти к глорихолу", target="TavernGloryHole", condition=tavern_main_glory_hole_visible)' in main
    assert 'return player.tavern_management.glory_hole == 2' in main
    assert 'RoomAction(action_id="check_glory_hole", label="Проверить, что происходит", hook="call", target="TavernGloryHoleCheck")' in glory
    assert 'label TavernGloryHoleCheck:' in glory
    assert 'girls_by_job("jobgloryhole", "TavernGloryHole")' in glory
    assert 'tavern_glory_hole_waiting_text(_tgh_worker)' in glory
    assert '$ main_ui_begin_native_scene_state("Глорихол")' in glory
    assert '"Вернуться в комнату":' in glory
    assert '$ main_ui_end_native_scene_state()' in glory


def test_guest_room_keeps_its_save_id_but_uses_its_new_room_identity():
    room = _source("game/Inn/TavernEmptyRoom.rpy")
    upstairs = _source("game/Inn/TavernUpstairs.rpy")
    migration = _source("game/TractirSaveSync.rpy")

    assert 'code_name="TavernEmptyRoom"' in room
    assert 'display_name="Гостевая комната"' in room
    assert 'RoomExit(label="Зайти в гостевую комнату", target="TavernEmptyRoom")' in upstairs
    assert '("TavernGloryHole", "TavernEmptyRoom", "TavernUpstairs")' in migration


def test_eddie_and_legare_learn_about_live_npc_owned_service_jobs():
    eddie = _source("game/NPC/Secondary/InitEddieTalk.rpy")
    alber_data = _source("game/NPC/Secondary/InitAlber.rpy")
    alber_talk = _source("game/NPC/Secondary/IntAlberTalk.rpy")
    new_day = _source("game/Utilities/Time/NextDay_NewDayEvents.rpy")

    for job_key in ("jobwhore", "jobgloryhole"):
        assert '_girl_job_value("georgett", "%s")' % job_key in eddie
        assert job_key in alber_talk
    assert "self.told_about_tavern_whores = False" in alber_data
    assert "Рассказать мессиру Легаре, что девушки теперь работают в трактире" in alber_talk
    assert 'Alber.told_about_tavern_whores and _liza_work_location in ("TavernMain", "TavernGloryHole")' in new_day


def test_all_service_workers_share_one_npc_job_and_client_pipeline():
    runtime = _source("game/Utilities/General/NPC/PeopleRuntime.rpy")
    lookup = _source("game/NPC/Girls/Common/GetRandomGirlByJob.rpy")
    rollover = _source("game/Utilities/Time/NextDay_TavernDaily.rpy")
    clients = _source("game/Utilities/Time/NextDay_NewDayEvents.rpy")
    report = _source("game/Utilities/Time/NextDay.rpy")
    dinner = _source("game/Inn/TavernKitchenBreakfast.rpy")

    assert "def assign_tavern_service(self, target=\"\", tomorrow=True):" in runtime
    assert "def apply_tavern_service_plan(self):" in runtime
    assert "for girl_key, girl_info in people.girl_items():" in lookup
    assert "for _service_worker in people.girl_values():" in rollover
    assert "_service_worker.apply_tavern_service_plan()" in rollover
    assert "[girl for girl in people.girl_values() if girl.tavern_client_generation_enabled()]" in clients
    assert "sum(TotalWhoreClients.values()) * 3" in report
    assert "sum(TotalGloryHoleClients.values()) * 2" in report
    assert '"Спросить, кто хочет дополнительно заработать"' in dinner
    assert '_service_offer_info.enable_tavern_service("intimate")' in dinner
    assert '_service_offer_info.enable_tavern_service("gloryhole")' in dinner
    assert "sunday_service" not in runtime + dinner
