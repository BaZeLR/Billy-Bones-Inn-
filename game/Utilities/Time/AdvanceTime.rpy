# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Time advancement function - moves time forward or advances to the next day
# Converted from QSP AdvanceTime to Ren'Py

init python:
    def advance_time_runtime(minutes_to_add=60):
        advanced_minutes = max(0, int(minutes_to_add or 60))
        calendar_v2.advance_minutes(advanced_minutes)
        return advanced_minutes


label AdvanceTimeOnly(minutes_to_add=60):
    $ renpy.dynamic("_advance_minutes")
    $ _advance_minutes = advance_time_runtime(minutes_to_add)
    if int(_advance_minutes or 0) > 0:
        call stat
        # A scheduled visitor can arrive while MC remains in the kitchen.
        if str(rooms.current_code or "") == "TavernKitchen" and main_ui_runtime.mode == "scene" and story_event_available("TavernKitchen", "enter"):
            call checkTriggers("TavernKitchen", "enter", 0)
    return _advance_minutes
