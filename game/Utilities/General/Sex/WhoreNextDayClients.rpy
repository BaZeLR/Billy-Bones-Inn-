# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label WhoreNextDayClients(girl_name="", max_clients=0, glory_hole_max=0):
    python:
        g = str(girl_name or "")
        if not g and _args:
            g = str(_args[0] or "")

        try:
            max_clients_i = int(max_clients)
        except Exception:
            max_clients_i = 0

        try:
            glory_max_i = int(glory_hole_max)
        except Exception:
            glory_max_i = 0

        # === SIMPLE & CLEAN - This is what should have been done ===
        calendar_v2.sync_state()        # This updates all your calendar variables properly

        week_val = int(week)         # direct access after sync
        current_time = int(time)     # direct access after sync

        glory_max_i = min(10, max(0, glory_max_i))
        if week_val == 5:
            glory_max_i = glory_max_i // 2
        if week_val == 7:
            glory_max_i = (glory_max_i * 3) // 4

        clients_day_total = ClientsDayTotal

        # Keep both spellings compatible with converted code variants.
        job_glory_tomorrow = jobgloryholeTommorow

        if int(job_glory_tomorrow.get(g, 0) or 0) != 0:
            clients_day_total[g] = (glory_max_i * (75 + 5 * renpy.random.randint(1, 10))) // 100
            needed = int(clients_day_total[g] or 0)
            created = 0
            safety = 0
            while created < needed and safety < 400:
                safety += 1
                time_whore_event = renpy.random.randint(2, 3)
                if week_val == 5:
                    time_whore_event = 2
                if week_val == 7:
                    time_whore_event = 3

                event_type = renpy.random.randint(1, 11)
                if event_type == 1 and current_time == 2:
                    event_type = 6
                if event_type == 3 and current_time == 2:
                    event_type = 9
                if event_type == 4 and week_val == 7:
                    event_type = 11

                try:
                    already_exists = int(CheckIfEventAlreadyExist(g, event_type) or 0)
                except Exception:
                    already_exists = 0

                if event_type > 4 or already_exists == 0:
                    TodaySexEvents_Add(g, time_whore_event, event_type, "Glory")
                    created += 1
        else:
            if max_clients_i > 0:
                clients_day_total[g] = renpy.random.randint(1, max_clients_i)
            else:
                clients_day_total[g] = 0
            if week_val == 5:
                clients_day_total[g] = 0

            needed = int(clients_day_total[g] or 0)
            created = 0
            prostitution_max_type = 3 if g == "liza" else 4
            while created < needed:
                event_type = renpy.random.randint(1, prostitution_max_type)
                TodaySexEvents_Add(g, 3, event_type, "Prostitution")
                created += 1
    return
