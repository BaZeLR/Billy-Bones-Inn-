# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Display Tavern Event Short (Event Dispatcher)
# Converted from legacy script. Dispatches and displays short tavern events.
# To be called with time period and eyewitness as arguments.

init python:
    def _dtes_i(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def _dtes_mandatory_event_allowed(event_code, room_code=""):
        code = str(event_code or "")
        if code == "WineForDance":
            return str(room_code or rooms.current_code or "") == "TavernKitchen"
        return True

label DisplayTavernEventShort(time_period, eyewitness):
    $ renpy.dynamic("_event_pick", "_event_code", "_event_target", "_event_result")
    $ _event_pick = tavern_work_pop_planned_event(time_period, eyewitness > 0, rooms.current_code)
    $ _event_code = str(_event_pick.get("code", "") or "")
    $ _event_target = {
        "WineForDance": "EventWineForDance",
        "FightSmall": "EventFightSmall",
        "CleaningHarass": "event_cleaning_harrass",
        "WaitressHarass": "event_waitress_harrass",
        "AmandaLizaTalk": "EventAmandaLizettTalk",
    }.get(_event_code, "")
    if not _event_target:
        return ""
    call expression _event_target pass (eyewitness,)
    $ _event_result = _return
    return _event_result

# # Helper event labels (stubs)
# label event_fight_small(eyewitness):
#     # ...event logic...
#     return

# label event_cleaning_harrass(eyewitness):
#     # ...event logic...
#     return

# label event_waitress_harrass(eyewitness):
#     # ...event logic...
#     return

# label event_amanda_lizett_talk(eyewitness):
#     # ...event logic...
#     return
