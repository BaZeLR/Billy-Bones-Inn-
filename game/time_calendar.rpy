init python:
    # Backward-compatible wrappers.
    # Canonical calendar logic lives in game/script.rpy (calendar_* functions).

    def ensure_calendar_state():
        return calendar_sync_state()

    def advance_minutes(minutes_to_add):
        return calendar_advance_minutes(minutes_to_add)
