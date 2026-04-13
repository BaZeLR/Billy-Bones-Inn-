label CreateTavernEventsPeriod(TimePeriod):
    $ EventsCount[TimePeriod] = 0
    python:
        tp = int(TimePeriod or 0)
        try:
            job_whore_avail = jobWhoreAvail
        except NameError:
            job_whore_avail = {}
        try:
            job_glory = jobgloryhole
        except NameError:
            job_glory = {}
        liza_whore_ok = 0
        liza_glory = 0
        if isinstance(job_whore_avail, dict):
            liza_whore_ok = int(job_whore_avail.get("liza", 0) or 0)
        if isinstance(job_glory, dict):
            liza_glory = int(job_glory.get("liza", 0) or 0)
        events_i_counter = 0
        while events_i_counter <= 2:
            rand_create_event = renpy.random.randint(1, 20)

            # TXT parity: evening/night weighting.
            if tp > 3:
                rand_create_event = 20

            selected = ""
            if tp >= 3 and rand_create_event <= 1:
                selected = "FightSmall"
            elif rand_create_event == 3:
                selected = "CleaningHarass"
            elif rand_create_event == 5 or rand_create_event == 6 or (tp >= 3 and (rand_create_event == 7 or rand_create_event == 8)):
                selected = "WaitressHarass"
            elif (rand_create_event >= 9 and rand_create_event <= 11) and (tp == 2 or tp == 1) and liza_whore_ok and (liza_glory == 0 or tp < 2):
                selected = "AmandaLizaTalk"

            if selected:
                event_idx = int(EventsCount.get(tp, 0) or 0)
                NewEvents[str(tp) + "_" + str(event_idx)] = selected
                EventsCount[tp] = event_idx + 1

            events_i_counter += 1
    return
