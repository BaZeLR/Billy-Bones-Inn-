# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Time advancement function - moves time forward or advances to the next day
# Converted from QSP AdvanceTime to Ren'Py

default LastAdvancedMinutes = 0
default LastAdvancedTimeSlots = 0

init python:
    def calendar_total_minutes_runtime():
        try:
            calendar_sync_state()
        except Exception:
            pass
        return (int(dayspassed or 0) * 1440) + (int(hour or 0) * 60) + int(minute or 0)

    def advance_time_slot_runtime(slots_to_add=1):
        global LastAdvancedMinutes, LastAdvancedTimeSlots

        ensure_calendar_state()
        before_minutes = calendar_total_minutes_runtime()
        slots = max(1, int(slots_to_add or 1))
        advanced_slots = 0

        while advanced_slots < slots and int(time or 0) < 4:
            calendar_set_time_slot(int(time or 0) + 1)
            advanced_slots += 1

        after_minutes = calendar_total_minutes_runtime()
        LastAdvancedMinutes = max(0, after_minutes - before_minutes)
        LastAdvancedTimeSlots = advanced_slots
        return LastAdvancedMinutes


label AdvanceTimeOnly(slots_to_add=1):
    $ _advance_minutes = advance_time_slot_runtime(slots_to_add)
    if int(_advance_minutes or 0) > 0:
        $ npc_schedule_sync_all()
        $ werecat_sync_profile()
        call stat
        $ checkpoint_tractir_progress("advance_time")
    return _advance_minutes


label AdvanceTimeAndRestore(restore_label=""):
    call AdvanceTimeOnly(1)
    $ _advance_minutes = _return
    $ _restore_label = str(restore_label or "").strip()
    if _restore_label != "" and renpy.has_label(_restore_label):
        call expression _restore_label
    return _advance_minutes

label AdvanceTime(return_location=None):
    """
    Advances the game time by one unit or moves to the next day if at the end of the day
    
    Args:
        return_location: The location to return to after advancing time
    """
    $ retlocname = return_location if return_location else "TavernMain"
    
    if int(time or 0) < 4:
        call AdvanceTimeOnly(1)
        jump expression retlocname
    else:
        call NextDay(retlocname, 1)
        
    return
