from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHURCH_ROOM = PROJECT_ROOT / "game" / "Town" / "Church" / "Church.rpy"
STORY_RUNTIME = PROJECT_ROOT / "game" / "Utilities" / "General" / "Classes" / "StoryEventRuntime.rpy"


def _source(path):
    return path.read_text(encoding="utf-8-sig")


def test_church_uses_clock_minutes_for_open_service_confession_and_after_ceremony():
    source = _source(CHURCH_ROOM)

    assert "def church_time_slot_visible" not in source
    assert "return week == 7 and church_minutes_between(8 * 60, 12 * 60 + 59)" in source
    assert "return week == 7 and church_minutes_between(8 * 60, 9 * 60 + 29)" in source
    assert "return week == 7 and church_minutes_between(9 * 60 + 30, 10 * 60 + 59)" in source
    assert "return week == 7 and church_minutes_between(11 * 60, 12 * 60 + 59)" in source
    assert 'start="08:00"' in source
    assert 'end="12:59"' in source
    assert "$ church_apply_sunday_purity()" in source


def test_church_room_phase_pictures_use_church_folder_vscene_assets():
    source = _source(CHURCH_ROOM)

    assert 'bg_picture="images/church/locChurchClosed_day.png"' in source
    assert 'vscene "images/church/locChurchClosed_day.png"' in source
    assert 'vscene "images/church/churchEntryDay.png"' in source
    assert 'vscene "images/church/confessionEntry.png"' in source
    assert 'call ShowImage("gerhard", "", "gerhard")' not in source
    assert 'call ShowImageSeq("general", "", "LocChurchClosed", 2)' not in source


def test_church_location_files_do_not_use_old_general_church_pictures():
    church_dir = PROJECT_ROOT / "game" / "Town" / "Church"
    combined = "\n".join(path.read_text(encoding="utf-8-sig") for path in church_dir.glob("*.rpy"))

    assert 'call ShowImage("general", "", "LocChurchIspoved1")' not in combined
    assert 'call ShowImage("general", "", "LocChurchIspoved2")' not in combined
    assert 'call ShowImageSeq("general", "", "LocChurchClosed", 2)' not in combined
    assert 'vscene "images/church/confessionEntry.png"' in combined


def test_church_event_rows_show_same_clock_gate_conditions():
    runtime = _source(STORY_RUNTIME)

    assert '"#church_service_action_visible()"' in runtime
    assert '"#church_after_cermon_action_visible()"' in runtime
    assert '7, (8, 9), None' in runtime
    assert '7, (6, 7), None' not in runtime[runtime.find("define georgettThreadList"):]
