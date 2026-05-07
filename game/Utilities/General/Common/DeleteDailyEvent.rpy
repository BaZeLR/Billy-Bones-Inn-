# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label delete_daily_event(girlname="", eventtype="", location=""):
    $ DailyEventsList_Delete(girlname, eventtype, location)
    return


label DeleteDailyEvent(girlname="", eventtype="", location=""):
    call delete_daily_event(girlname, eventtype, location)
    return
