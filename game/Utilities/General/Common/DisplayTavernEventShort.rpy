# ================================================================================
# Runs the next planned tavern event. The event definition owns its target label.
# ================================================================================

label DisplayTavernEventShort(time_period, eyewitness):
    $ renpy.dynamic("_event_pick", "_event_target", "_event_result")
    $ _event_pick = tavern_work_pop_planned_event(time_period, eyewitness > 0, rooms.current_code)
    $ _event_target = str(_event_pick.get("label", "") or "")
    if not _event_target:
        return ""
    call expression _event_target pass (eyewitness,)
    $ _event_result = _return
    return _event_result
