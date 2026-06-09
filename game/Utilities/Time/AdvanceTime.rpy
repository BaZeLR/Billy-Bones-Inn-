# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Time advancement function - moves time forward or advances to the next day
# Converted from QSP AdvanceTime to Ren'Py

default LastAdvancedMinutes = 0

init python:
    def advance_time_runtime(minutes_to_add=60):
        global LastAdvancedMinutes

        calendar_v2.sync_state()
        LastAdvancedMinutes = max(0, int(minutes_to_add or 60))
        calendar_v2.advance_minutes(LastAdvancedMinutes)
        return LastAdvancedMinutes


label AdvanceTimeOnly(minutes_to_add=60):
    $ _advance_minutes = advance_time_runtime(minutes_to_add)
    if int(_advance_minutes or 0) > 0:
        $ npc_schedule_sync_all()
        $ werecat_sync_profile()
        call stat
        $ checkpoint_tractir_progress("advance_time")
    return _advance_minutes


label AdvanceTimeAndRestore(restore_label=""):
    call AdvanceTimeOnly(60)
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
    
    if int(clock_minutes or 0) + 60 < 1440:
        call AdvanceTimeOnly(60)
        jump expression retlocname
    else:
        call NextDay(retlocname, 1)
        
    return
