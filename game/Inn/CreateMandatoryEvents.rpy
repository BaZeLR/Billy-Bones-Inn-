label CreateMandatoryEvents:
    $ TimePeriod = 10
    $ EventsCount[TimePeriod] = 0

    if week == 4:
        $ NewEvents[str(TimePeriod) + '_' + str(EventsCount[TimePeriod])] = 'WineForDance'
        $ EventsCount[TimePeriod] += 1

    call AmandaLegareDanceSequence
    return
