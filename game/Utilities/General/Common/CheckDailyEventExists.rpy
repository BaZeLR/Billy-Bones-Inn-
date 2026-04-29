# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label check_daily_event_exists(girlname=None, eventtype=None, location=None):
    $ Result = DailyEventsList_Exists(girlname, eventtype, location)
    return Result


label CheckDailyEventExists(girlname=None, eventtype=None, location=None):
    call check_daily_event_exists(girlname, eventtype, location)
    return
