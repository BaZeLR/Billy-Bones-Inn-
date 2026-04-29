# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    # Backward-compatible wrappers.
    # Canonical calendar logic lives in game/script.rpy (calendar_* functions).

    def ensure_calendar_state():
        return calendar_sync_state()

    def advance_minutes(minutes_to_add):
        return calendar_advance_minutes(minutes_to_add)
