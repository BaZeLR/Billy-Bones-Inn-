# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default RoomEnterPresentIds = []
default RoomEnterLastRoom = ""
default RoomEnterLastEventFired = False

init python:
    def room_enter_present_ids(room_code=""):
        room_key = str(room_code or CurLoc or "").strip()
        if not room_key:
            return []
        try:
            return list(getNPCids(room_key) or [])
        except Exception:
            return []

    def room_enter_story_action_ready(room_code="", action_name="enter"):
        room_key = str(room_code or CurLoc or "").strip()
        action_key = str(action_name or "enter").strip()
        if not room_key or not action_key:
            return False
        try:
            return bool(story_event_available(room_key, action_key))
        except Exception:
            return False

    def room_enter_capture_presence(room_code=""):
        global RoomEnterPresentIds, RoomEnterLastRoom
        RoomEnterLastRoom = str(room_code or CurLoc or "").strip()
        RoomEnterPresentIds = list(room_enter_present_ids(RoomEnterLastRoom) or [])
        return list(RoomEnterPresentIds or [])


label RoomEnterEventGate(room_code="", include_daily=True):
    $ _room_enter_code = str(room_code or CurLoc or "").strip()
    if _room_enter_code != "" and room_in_group(_room_enter_code, ROOM_GROUP_CITY):
        $ dog_prepare_current_spawn()
    $ _room_enter_obj = get_registered_room(_room_enter_code)
    if _room_enter_obj is not None and str(getattr(_room_enter_obj, "bg_picture", "") or "").strip():
        $ _layout_last_picture = str(getattr(_room_enter_obj, "bg_picture", "") or "").strip()
        $ scene_image = _layout_last_picture
    $ RoomEnterLastEventFired = False
    $ room_enter_capture_presence(_room_enter_code)

    if room_enter_story_action_ready(_room_enter_code, "enter"):
        call checkTriggers(_room_enter_code, "enter", 0)
        if _return:
            $ RoomEnterLastEventFired = True
            return True

    if include_daily:
        $ _room_enter_daily_ids = list(RoomEnterPresentIds or [])
        while len(_room_enter_daily_ids) > 0:
            $ _room_enter_daily_npc = str(_room_enter_daily_ids.pop(0) or "").strip()
            if _room_enter_daily_npc != "":
                call check_daily_event(_room_enter_daily_npc, None, _room_enter_code, time)
                if _return:
                    $ RoomEnterLastEventFired = True
                    return True

    if _room_enter_code != "" and "household_ai_pick_event" in globals() and renpy.has_label("HouseholdEvent_Try"):
        $ _household_seen_before = len(household.seen)
        call HouseholdEvent_Try(_room_enter_code, "room")
        if len(household.seen) > _household_seen_before:
            $ RoomEnterLastEventFired = True
            return True

    return False
