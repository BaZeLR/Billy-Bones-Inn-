# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
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


label RoomEnterEventGate(room_code="", include_daily=True):
    $ _room_enter_code = str(room_code or CurLoc or "").strip()
    if _room_enter_code != "" and room_in_group(_room_enter_code, ROOM_GROUP_CITY):
        $ dog_prepare_current_spawn()

    # Entry dispatch does not own room presentation. The room decides its normal
    # picture/text; an event decides its temporary scene while it is playing.
    if room_enter_story_action_ready(_room_enter_code, "enter"):
        call checkTriggers(_room_enter_code, "enter", 0)
        if _return:
            return True

    if include_daily:
        $ _room_enter_daily_ids = list(room_enter_present_ids(_room_enter_code) or [])
        while len(_room_enter_daily_ids) > 0:
            $ _room_enter_daily_npc = str(_room_enter_daily_ids.pop(0) or "").strip()
            if _room_enter_daily_npc != "":
                # Legacy daily-event tables still use the display slot. New room,
                # schedule and story-event code must use calendar clock hours.
                call CheckDailyEvent(_room_enter_daily_npc, None, _room_enter_code, time)
                if _return:
                    return True

    if _room_enter_code != "" and "household_ai_pick_event" in globals() and renpy.has_label("HouseholdEvent_Try"):
        $ _household_seen_before = len(HouseholdAISeen) if isinstance(globals().get("HouseholdAISeen", None), dict) else 0
        call HouseholdEvent_Try(_room_enter_code, "room")
        if isinstance(globals().get("HouseholdAISeen", None), dict) and len(HouseholdAISeen) > _household_seen_before:
            return True

    return False
