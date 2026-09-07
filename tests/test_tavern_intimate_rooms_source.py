import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def test_intimate_jobs_place_each_worker_in_the_room_owned_by_that_job():
    for person in ("georgett", "liza"):
        schedule = json.loads(_source("game/NPC/Schedules/%s.json" % person))
        rows = schedule["entries"]
        whore_rows = [row for row in rows if row["label"] in ("tavern_whore_shift", "friday_shift", "friday_tavern_whore_shift_before_dance")]
        glory_rows = [row for row in rows if "glory_hole_shift" in row["label"]]

        assert len(whore_rows) == 2
        assert len(glory_rows) == 2
        for row in whore_rows:
            assert row["location"] == "TavernMain"
            assert row["condition"] == {
                "rule": "any_job_assigned",
                "people": [person],
                "job": "jobwhore",
            }
        for row in glory_rows:
            assert row["location"] == "TavernGloryHole"
            assert row["condition"] == {
                "rule": "any_job_assigned",
                "people": [person],
                "job": "jobgloryhole",
            }


def test_completed_glory_hole_is_a_room_with_a_separate_check_scene():
    glory = _source("game/Inn/TavernGloryHole.rpy")
    main = _source("game/Inn/TavernMain.rpy")

    assert 'RoomExit(label="Идти к глорихолу", target="TavernGloryHole", condition=tavern_main_glory_hole_visible)' in main
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
