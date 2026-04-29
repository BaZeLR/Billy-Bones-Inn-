# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Time advancement function - moves time forward or advances to the next day
# Converted from QSP AdvanceTime to Ren'Py

label AdvanceTime(return_location=None):
    """
    Advances the game time by one unit or moves to the next day if at the end of the day
    
    Args:
        return_location: The location to return to after advancing time
    """
    $ retlocname = return_location if return_location else "TavernMain"
    
    $ ensure_calendar_state()

    if int(time or 0) < 4:
        $ calendar_set_time_slot(int(time or 0) + 1)
        $ npc_schedule_sync_all()
        $ werecat_sync_profile()
        call stat
        $ checkpoint_tractir_progress("advance_time")
        jump expression retlocname
    else:
        call NextDay(retlocname, 1)
        
    return
