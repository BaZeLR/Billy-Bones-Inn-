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


def test_room_entry_event_gate_does_not_own_room_media_or_scratch_globals():
    source = read_rel("game/Utilities/General/Common/RoomEnterPipeline.rpy")
    gate = source.split('label RoomEnterEventGate(room_code="", include_daily=True):', 1)[1]

    assert "_layout_last_picture" not in gate
    assert "scene_image" not in gate
    assert "bg_picture" not in gate
    assert 'room_enter_story_action_ready(_room_enter_code, "enter")' in gate
    assert "default RoomEnterPresentIds" not in source
    assert "default RoomEnterLastRoom" not in source
    assert "default RoomEnterLastEventFired" not in source
    assert "room_enter_capture_presence" not in source
    assert "room_enter_present_ids(_room_enter_code)" in gate


def test_room_owns_first_visit_state_in_custom_properties():
    source = read_rel("game/Utilities/General/Classes/RoomTemplate.rpy")
    room_block = source.split("class Room(object):", 1)[1].split('label MoveToRoom(target_label="", movement_minutes=0):', 1)[0]

    assert "default roomFirstVisit" not in source
    assert 'self.custom_properties.get("_visited", False)' in room_block
    assert 'self.custom_properties["_visited"] = True' in room_block


def test_room_custom_properties_are_in_save_restore_payload():
    source = read_rel("game/Utilities/General/Classes/RoomTemplate.rpy")
    restore_block = source.split('def restore_room_runtime(room_code="", payload=None):', 1)[1].split("class RoomExit(object):", 1)[0]
    reduce_block = source.split("def __reduce__(self):", 1)[1].split('label MoveToRoom(target_label="", movement_minutes=0):', 1)[0]

    assert 'if "custom_properties" in payload:' in restore_block
    assert 'restored.custom_properties = dict(payload.get("custom_properties", {}) or {})' in restore_block
    assert '"custom_properties": dict(state.get("custom_properties", {}) or {})' in reduce_block


def test_forest_spawned_items_are_room_owned_and_transfer_to_player_inventory():
    source = read_rel("game/Forest/Forest.rpy")
    forest_class = source.split("class Forest(Room):", 1)[1].split("def forest_room_spawn", 1)[0]
    take_block = source.split('label ForestTakeSpawnedItem(item_id=""):', 1)[1].split("label ForestSubroomBuildActions:", 1)[0]

    assert 'self.custom_properties["spawned_items"]' in forest_class
    assert 'self.custom_properties["spawn_day"] = day_value' in forest_class
    assert 'int(self.custom_properties.get("spawn_day", -1)) == day_value' in forest_class
    assert "ForestRoom.remove_spawned_item(item_id)" in take_block
    assert "_player_add_item_by_id" in take_block
    assert "picked_item" not in source.lower()
    assert "pickeditem" not in source.lower()


def test_main_forest_uses_vertical_slice_without_location_mirrors():
    source = read_rel("game/Forest/Forest.rpy")
    entry = source.split("label Forest:", 1)[1].split("label ForestBuildActions:", 1)[0]
    actions = source.split("label ForestBuildActions:", 1)[1].split("label ForestObjectMenu", 1)[0]

    assert '$ CurLoc = "Forest"' in entry
    assert "get_registered_room(CurLoc) or ForestRoom" in entry
    assert "$ CurrentRoom =" not in entry
    assert "$ location =" not in entry
    assert "call RoomEnterEventGate(CurLoc, False)" in entry
    assert entry.index("call RoomEnterEventGate(CurLoc, False)") < entry.index("forest_pick_background()")
    assert "_forest_room.spawn()" in entry
    assert "get_registered_room(CurLoc) or ForestRoom" in actions
    assert 'Call("MoveToRoom", _forest_exit.target' in actions
