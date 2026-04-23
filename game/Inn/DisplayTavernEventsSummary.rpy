# Display Tavern Events Summary (Event Summary Dispatcher)
# Converted from legacy script. Loops through all time periods and displays event summaries for the day.
# To be called to generate a summary of all tavern events for the day.

label DisplayTavernEventsSummary(day, month, year):
    $ TimePeriodEvents = 0
    $ TodayEventsSummary = ''
    while TimePeriodEvents < 5:
        while EventsCount.get(TimePeriodEvents, 0) > 0:
            call DisplayTavernEventShort(TimePeriodEvents, 0)
            $ TodayEventsSummaryTmp = _return
            if TodayEventsSummaryTmp != '':
                $ TodayEventsSummary += '\n\n' + TodayEventsSummaryTmp
        $ TimePeriodEvents += 1
    if TodayEventsSummary == '':
        $ TodayEventsSummary = '\n\nНичего не произошло!'
    $ TodayEventsSummary = "\n\n{i}События за [calendar_format_date_ru(day, month, year, None, False)]{/i}" + TodayEventsSummary
    $ Result = TodayEventsSummary
    return Result
