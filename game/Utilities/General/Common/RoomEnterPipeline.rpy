# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label RoomEnterEventGate(room_code="", include_daily=True):
    $ renpy.dynamic("_room_enter_code", "_room_enter_daily_ids", "_room_enter_daily_npc", "_household_seen_before")
    $ _room_enter_code = str(room_code or rooms.current_code or "").strip()

    if _room_enter_code != "" and story_event_available(_room_enter_code, "enter"):
        call checkTriggers(_room_enter_code, "enter", 0)
        if _return:
            return True

    if include_daily:
        $ _room_enter_daily_ids = list(people.ids_at(_room_enter_code) or [])
        while len(_room_enter_daily_ids) > 0:
            $ _room_enter_daily_npc = str(_room_enter_daily_ids.pop(0) or "").strip()
            if _room_enter_daily_npc != "":
                call check_daily_event(_room_enter_daily_npc, None, _room_enter_code, calendar_v2.time_slot())
                if _return:
                    return True

    if _room_enter_code != "":
        $ _household_seen_before = len(household.seen)
        call HouseholdEvent_Try(_room_enter_code, "room")
        if len(household.seen) > _household_seen_before:
            return True

    return False
