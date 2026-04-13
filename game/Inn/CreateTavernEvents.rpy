label CreateTavernEvents:
    python:
        TimePeriodsEvents = 0
        EventsCount = {}
        NewEvents = {}

    while TimePeriodsEvents < 5:
        call CreateTavernEventsPeriod(TimePeriodsEvents)
        $ TimePeriodsEvents += 1

    python:
        _total_random = 0
        for _tp in range(5):
            try:
                _total_random += int(EventsCount.get(_tp, 0) or 0)
            except Exception:
                pass
        if _total_random <= 0:
            EventsCount[2] = 1
            NewEvents["2_0"] = "WaitressHarass"

    call CreateMandatoryEvents
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
        EventsCount = {}
        NewEvents = {}

        job_whore_avail = {}
        if isinstance(jobWhoreAvail, dict):
            job_whore_avail = jobWhoreAvail

        job_glory = {}
        if isinstance(jobgloryhole, dict):
            job_glory = jobgloryhole

        liza_whore_ok = _cte_i(job_whore_avail.get("liza", 0), 0)
        liza_glory = _cte_i(job_glory.get("liza", 0), 0)

        for tp in range(5):
            EventsCount[tp] = 0
            for _unused_event_roll in range(3):
                rand_create_event = renpy.random.randint(1, 20)
                if tp > 3:
                    rand_create_event = 20

                selected = ""
                if tp >= 3 and rand_create_event <= 1:
                    selected = "FightSmall"
                elif rand_create_event == 3:
                    selected = "CleaningHarass"
                elif rand_create_event in (5, 6) or (tp >= 3 and rand_create_event in (7, 8)):
                    selected = "WaitressHarass"
                elif (9 <= rand_create_event <= 11) and (tp in (1, 2)) and liza_whore_ok and (liza_glory == 0 or tp < 2):
                    selected = "AmandaLizaTalk"

                if selected:
                    event_idx = _cte_i(EventsCount.get(tp, 0), 0)
                    NewEvents[str(tp) + "_" + str(event_idx)] = selected
                    EventsCount[tp] = event_idx + 1

        total_random = 0
        for tp in range(5):
            total_random += _cte_i(EventsCount.get(tp, 0), 0)
        if total_random <= 0:
            EventsCount[2] = 1
            NewEvents["2_0"] = "WaitressHarass"

        if include_mandatory:
            EventsCount[10] = 0
            if _cte_i(week, 1) == 4:
                NewEvents["10_0"] = "WineForDance"
                EventsCount[10] = 1

        return {"EventsCount": EventsCount, "NewEvents": NewEvents}
