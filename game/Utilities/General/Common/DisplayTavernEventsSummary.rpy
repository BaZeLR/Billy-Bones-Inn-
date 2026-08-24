# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
# Display Tavern Events Summary (Event Summary Dispatcher)
# Converted from legacy script. Loops through all time periods and displays event summaries for the day.
# To be called to generate a summary of all tavern events for the day.

label DisplayTavernEventsSummary(day, month, year, result="", time_period_events=0, today_events_summary="", today_events_summary_tmp=""):
    $ time_period_events = 0
    $ today_events_summary = ''
    while tavern_work_has_period(10, True):
        call DisplayTavernEventShort(10, 0)
        $ today_events_summary_tmp = _return
        if today_events_summary_tmp != '':
            $ today_events_summary += '\n\n' + today_events_summary_tmp
    while time_period_events < 5:
        while tavern_work_has_period(time_period_events, False):
            call DisplayTavernEventShort(time_period_events, 0)
            $ today_events_summary_tmp = _return
            if today_events_summary_tmp != '':
                $ today_events_summary += '\n\n' + today_events_summary_tmp
        $ time_period_events += 1
    if today_events_summary == '':
        $ today_events_summary = '\n\nНичего не произошло!'
    $ today_events_summary = "\n\n{i}События за [calendar_v2.format_date_ru(day, month, year, None, False)]{/i}" + today_events_summary
    $ result = today_events_summary
    return result
