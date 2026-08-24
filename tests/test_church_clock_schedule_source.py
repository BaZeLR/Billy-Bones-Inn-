from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHURCH_ROOM = PROJECT_ROOT / "game" / "Town" / "Church" / "Church.rpy"
CHURCH_AFTER = PROJECT_ROOT / "game" / "Town" / "Church" / "ChurchAfterCermon.rpy"
BECKY_CHURCH = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Becky" / "IntBeckyAfterCermon.rpy"
BECKY_INIT = PROJECT_ROOT / "game" / "NPC" / "Girls" / "Becky" / "InitBecky.rpy"
STORY_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"
PEOPLE_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "NPC" / "PeopleRuntime.rpy"
FINISH_DAY = PROJECT_ROOT / "game" / "Utilities" / "Time" / "NextDay_FinishDayEvents.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def test_church_uses_calendar_hour_minute_for_open_service_confession_and_after_ceremony():
    source = _source(CHURCH_ROOM)

    assert "def church_time_slot_visible" not in source
    minutes_now = source.split("def church_minutes_now():", 1)[1].split("\n    def ", 1)[0]
    assert "calendar_v2.sync_state()" not in minutes_now
    assert "calendar_v2.hour" in minutes_now
    assert "calendar_v2.minute" in minutes_now
    assert "clock_minutes" not in minutes_now
    assert "return int(calendar_v2.week or 0) == 7 and church_minutes_between(8 * 60, 12 * 60 + 59)" in source
    assert "return int(calendar_v2.week or 0) == 7 and church_minutes_between(8 * 60, 9 * 60 + 29)" in source
    assert "return int(calendar_v2.week or 0) == 7 and church_minutes_between(9 * 60 + 30, 10 * 60 + 59)" in source
    assert "return int(calendar_v2.week or 0) == 7 and church_minutes_between(11 * 60, 12 * 60 + 59)" in source
    assert 'start="08:00"' in source
    assert 'end="12:59"' in source
    assert "$ church_apply_sunday_purity()" in source


def test_church_purity_state_has_one_room_owner():
    source = _source(CHURCH_ROOM)
    girl_card = _source(PROJECT_ROOT / "game" / "NPC" / "Girls" / "Common" / "GirlCard.rpy")

    assert 'state={"purity_last_day": -1, "purity_report": {}}' in source
    assert 'rooms.get(\"Church\").state["purity_last_day"] = today' in source
    assert 'rooms.get(\"Church\").state["purity_report"] = dict(report)' in source
    assert "church_state = rooms.get(\"Church\").state" in girl_card
    assert "ChurchPurityLastDay" not in source + girl_card
    assert "ChurchPurityReport" not in source + girl_card


def test_sunday_service_npc_schedules_match_the_church_clock_phase():
    schedule_dir = PROJECT_ROOT / "game" / "NPC" / "Schedules"

    for npc_id in ("amanda", "melissa", "sandra", "becky", "alber", "georgett", "liza"):
        payload = json.loads((schedule_dir / (npc_id + ".json")).read_text(encoding="utf-8-sig"))
        church_entries = [
            row for row in payload["entries"]
            if row.get("location") == "Church" and "after_mass" not in str(row.get("label", ""))
        ]
        assert len(church_entries) == 1, npc_id
        assert church_entries[0]["weekdays"] == [7], npc_id
        assert church_entries[0]["start"] == "08:00", npc_id
        assert church_entries[0]["end"] == "09:29", npc_id

    for npc_id in ("georgett", "liza"):
        payload = json.loads((schedule_dir / (npc_id + ".json")).read_text(encoding="utf-8-sig"))
        after_mass = [row for row in payload["entries"] if "after_mass" in str(row.get("label", ""))]
        assert len(after_mass) == 1, npc_id
        assert after_mass[0]["start"] == "11:00", npc_id
        assert after_mass[0]["end"] == "12:59", npc_id


def test_church_room_phase_pictures_use_church_folder_vscene_assets():
    source = _source(CHURCH_ROOM)

    assert 'bg_picture="images/church/locChurchClosed_day.png"' in source
    assert 'def church_closed_picture()' in source
    assert 'def church_phase_picture()' not in source
    assert 'return "images/church/locChurchClosed_day.png"' in source
    assert 'return "images/church/locChurchClosed_night.png"' in source
    assert 'vscene church_closed_picture()' in source
    assert 'vscene "images/church/churchEntryDay.png"' in source
    assert 'vscene "images/church/confessionEntry.png"' in source
    assert 'vscene "images/gerhard/talkTogerhardt.png"' in source
    assert 'call ShowImage("gerhard", "", "gerhard")' not in source
    assert 'call ShowImageSeq("general", "", "LocChurchClosed", 2)' not in source


def test_church_location_files_do_not_use_old_general_church_pictures():
    church_dir = PROJECT_ROOT / "game" / "Town" / "Church"
    combined = "\n".join(path.read_text(encoding="utf-8-sig") for path in church_dir.glob("*.rpy"))

    assert 'call ShowImage("general", "", "LocChurchIspoved1")' not in combined
    assert 'call ShowImage("general", "", "LocChurchIspoved2")' not in combined
    assert 'call ShowImageSeq("general", "", "LocChurchClosed", 2)' not in combined
    assert 'vscene "images/church/confessionEntry.png"' in combined
    assert 'vscene "images/gerhard/gerhardispoved.jpg"' in combined


def test_church_event_rows_show_same_clock_gate_conditions():
    runtime = _source(STORY_RUNTIME)
    people_runtime = _source(PEOPLE_RUNTIME)

    assert '"#church_service_action_visible()"' in runtime
    assert "church_after_cermon_action_visible()" in people_runtime
    assert '"#church_after_cermon_action_visible()"' not in runtime
    assert '7, (8, 9), None' in runtime
    assert '7, (6, 7), None' not in runtime[runtime.find("define georgettThreadList"):]


def test_becky_after_ceremony_is_thread_event_with_clock_conditions():
    runtime = _source(STORY_RUNTIME)
    church_after = _source(CHURCH_AFTER)
    becky_scene = _source(BECKY_CHURCH)
    becky_init = _source(BECKY_INIT)
    people_runtime = _source(PEOPLE_RUNTIME)
    finish_day = _source(FINISH_DAY)

    assert "def church_after_sermon_event_available" in people_runtime
    assert "def church_after_sermon_event_available" not in becky_init
    assert "def can_trigger_after_sermon_event" in becky_init
    assert '"story_becky_church_after_sermon"' in runtime
    becky_thread = runtime.split('"story_becky_church_after_sermon"', 1)[1].split('define eddieThreadList', 1)[0]
    assert '7, (11, 12), None' in becky_thread
    assert "clock_minutes" not in becky_thread
    assert '"#Becky.church_after_sermon_event_available()"' in runtime
    assert "#CheckIfSexEventExist('becky', 99, 'Priest') > 0" not in becky_thread
    assert "after_sermon_stage" not in runtime
    assert "after_sermon_stage" not in becky_init
    assert "after_sermon_stage" not in becky_scene
    assert 'CheckIfSexEventExist("becky", 99, "Priest") > 0' in finish_day
    assert "Becky.after_sermon_stage()" not in finish_day

    assert "call IntBeckyAfterCermon" not in church_after
    assert "AfterCermonBecky" not in church_after
    assert "label IntBeckyAfterCermon:" not in becky_scene
    assert "label AfterCermonBecky:" not in becky_scene
    assert "label story_becky_church_after_sermon:" in becky_scene
    assert "label story_becky_church_after_sermon_look:" in becky_scene
    assert "BeckyVar" not in becky_scene
    assert 'Becky.var["priest_incest_agree"]' not in becky_scene
    assert "call AdvanceTime(\"Church\")" not in becky_scene
    assert "calendar_v2.advance_minutes(60)" in becky_scene


def test_church_after_ceremony_returns_without_action_panel_or_room_jump():
    source = _source(CHURCH_AFTER)

    assert "main_ui_runtime.action_items" not in source
    assert "MenuItem(" not in source
    assert "jump Church" not in source
    assert "renpy.restart_interaction" not in source
    assert '"[scene_runtime.text]"' in source
