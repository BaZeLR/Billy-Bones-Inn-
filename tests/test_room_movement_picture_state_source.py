from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_rel(path):
    return (PROJECT_ROOT / path).read_text(encoding="utf-8-sig")


def test_advance_movement_time_clears_selected_object_and_npc_before_jump():
    source = read_rel("game/Utilities/Time/TimeTurnSystem.rpy")
    label = source.split('label AdvanceMovementTime(target_label=""):', 1)[1].split("if renpy.has_label(movement_target):", 1)[0]

    assert '$ current_object_id = ""' in label
    assert '$ current_girl_key = ""' in label


def test_move_to_room_uses_curloc_as_single_location_truth():
    source = read_rel("game/Utilities/General/Classes/RoomTemplate.rpy")
    label = source.split('label MoveToRoom(target_label="", movement_minutes=0):', 1)[1].split('"DEBUG: missing target label', 1)[0]

    assert '$ CurLoc = movement_target' in label
    assert '$ location =' not in label
    assert '$ CurrentRoom =' not in label
    assert 'get_registered_room(CurLoc)' in label


def test_room_schedule_uses_clock_hours_not_display_time_slot():
    source = read_rel("game/Utilities/General/Classes/RoomTemplate.rpy")
    schedule = source.split("class RoomSchedule(object):", 1)[1].split("class Room(object):", 1)[0]

    assert "calendar_v2.hour" in schedule
    assert "time_slots" not in schedule
    assert "slot_from_hour" not in schedule


def test_room_entry_event_gate_does_not_own_room_media():
    source = read_rel("game/Utilities/General/Common/RoomEnterPipeline.rpy")
    gate = source.split('label RoomEnterEventGate(room_code="", include_daily=True):', 1)[1]

    assert "_layout_last_picture" not in gate
    assert "scene_image" not in gate
    assert "bg_picture" not in gate
    assert 'room_enter_story_action_ready(_room_enter_code, "enter")' in gate
