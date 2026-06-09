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

    def _dtes_events_count():
        return EventsCount

    def _dtes_new_events():
        return NewEvents

    def _dtes_mandatory_event_allowed(event_code, room_code=""):
        code = str(event_code or "")
        if code == "WineForDance":
            return str(room_code or CurLoc or "") == "TavernKitchen"
        return True

    def tavern_event_pop_code(time_period, require_room_match=False, room_code=""):
        return tavern_work_pop_planned_event(time_period, require_room_match, room_code)

    def DisplayTavernEventShort(time_period, eyewitness):
        """
        Python compatibility dispatcher.
        Dequeues one event from mandatory slot 10 first, then from current slot.
        This path is side-effect-light and used by debug/unit helpers.
        """
        global CurEventCode, Result
        EventsCount = _dtes_events_count()
        NewEvents = _dtes_new_events()

        tp = _dtes_i(time_period, 0)
        text = ""

        _event_pick = tavern_event_pop_code(tp)
        CurEventCode = str(_event_pick.get("code", "") or "")
        if CurEventCode:
            Result = text
            return text if text else CurEventCode

        Result = ""
        return ""

label DisplayTavernEventShort(time_period, eyewitness):
    $ CurEventDescFin = ''
    $ _event_pick = tavern_event_pop_code(time_period, eyewitness > 0, CurLoc)
    $ CurEventCode = str(_event_pick.get("code", "") or "")
    if CurEventCode == 'WineForDance':
        call EventWineForDance(eyewitness)
        $ CurEventDescFin = _return
    elif CurEventCode == 'FightSmall':
        call EventFightSmall(eyewitness)
        $ CurEventDescFin = _return
    elif CurEventCode == 'CleaningHarass':
        call event_cleaning_harrass(eyewitness)
        $ CurEventDescFin = _return
    elif CurEventCode == 'WaitressHarass':
        call event_waitress_harrass(eyewitness)
        $ CurEventDescFin = _return
    elif CurEventCode == 'AmandaLizaTalk':
        call EventAmandaLizettTalk(eyewitness)
        $ CurEventDescFin = _return
    $ Result = CurEventDescFin
    return CurEventDescFin

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
