# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default EventsCount = {}
default NewEvents = {}

label CreateTavernEvents:
    $ tavern_work_build_daily_plan()
    return


init python:
    import renpy.exports as renpy

    def _cte_i(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def build_tavern_events_queue_python(include_mandatory=True):
        planned_before = list(tavern_work_events or [])
        played_before = list(TavernPlayedEventsToday or [])
        report_before = list(TavernEventReportRows or [])
        events_count_before = dict(EventsCount or {})
        new_events_before = dict(NewEvents or {})
        tavern_work_build_daily_plan()
        if not include_mandatory:
            tavern_work_events[:] = [row for row in list(tavern_work_events or []) if not bool(row.get("mandatory", False))]
            tavern_work_sync_legacy_queue()
        result = {"EventsCount": dict(EventsCount or {}), "NewEvents": dict(NewEvents or {})}
        tavern_work_events[:] = planned_before
        TavernPlayedEventsToday[:] = played_before
        TavernEventReportRows[:] = report_before
        EventsCount.clear()
        EventsCount.update(events_count_before)
        NewEvents.clear()
        NewEvents.update(new_events_before)
        return result
