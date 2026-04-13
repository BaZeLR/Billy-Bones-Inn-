label delete_daily_event(girlname="", eventtype="", location=""):
    $ DailyEventsList_Delete(girlname, eventtype, location)
    return


label DeleteDailyEvent(girlname="", eventtype="", location=""):
    call delete_daily_event(girlname, eventtype, location)
    return
