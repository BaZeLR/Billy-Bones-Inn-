# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label CreateMandatoryEvents:
    $ TimePeriod = 10
    $ EventsCount[TimePeriod] = 0

    if week ==3:
        $ NewEvents[str(TimePeriod) + '_' + str(EventsCount[TimePeriod])] = 'WineForDance'
        $ EventsCount[TimePeriod] += 1

    call AmandaLegareDanceSequence
    return
