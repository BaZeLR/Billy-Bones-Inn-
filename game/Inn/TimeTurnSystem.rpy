init -115 python:
    import renpy.exports as renpy

    MOVEMENT_TIME_COST_MINUTES = 30

    def _turn_i(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _time_advancement_allowed():
        if str(CurLoc or "") == "Intro":
            return False
        if _turn_i(BlockTimeAdvance, 0) != 0:
            return False
        return True

    def _apply_movement_time_cost_without_sleep(minutes_to_add):
        global hour, minute, time

        ensure_calendar_state()
        current_minutes = (_turn_i(hour, 0) * 60) + _turn_i(minute, 0)
        target_minutes = current_minutes + max(0, _turn_i(minutes_to_add, 0))
        if target_minutes >= 1440:
            # Movement is never allowed to roll the calendar into the next day.
            hour = 23
            minute = 59
            time = 4
            calendar_sync_state()
            return False
        calendar_advance_minutes(max(0, _turn_i(minutes_to_add, 0)))
        return True

label AdvanceMovementTime(target_label=""):
    $ movement_target = str(target_label or CurLoc or "TavernMain")
    if _time_advancement_allowed():
        $ _movement_time_changed = _apply_movement_time_cost_without_sleep(MOVEMENT_TIME_COST_MINUTES)
        call stat
        if _movement_time_changed:
            $ checkpoint_tractir_progress("movement_time")
    if renpy.has_label(movement_target):
        jump expression movement_target
    jump TavernMain
