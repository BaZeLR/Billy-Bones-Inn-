label check_daily_event_exists(girlname=None, eventtype=None, location=None):
    $ Result = DailyEventsList_Exists(girlname, eventtype, location)
    return Result


label CheckDailyEventExists(girlname=None, eventtype=None, location=None):
    call check_daily_event_exists(girlname, eventtype, location)
    return
