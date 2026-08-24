# ================================================================================
# Daily sex-work event generation.
# ================================================================================

label WhoreNextDayClients(girl_name="", max_clients=0, glory_hole_max=0):
    $ renpy.dynamic("_wnd_girl_name", "_wnd_girl", "max_clients_i", "glory_max_i", "week_val", "current_time", "day_value", "generated_clients", "created", "safety", "event_hour", "event_type", "already_exists", "prostitution_max_type")
    $ _wnd_girl_name = str(girl_name or (_args[0] if _args else "") or "")
    $ _wnd_girl = people.get_info(_wnd_girl_name)
    if _wnd_girl is None:
        return

    python:
        max_clients_i = people_to_int(max_clients, 0)
        glory_max_i = min(10, max(0, people_to_int(glory_hole_max, 0)))

        week_val = people_to_int(calendar_v2.week, 0)
        current_time = people_to_int(calendar_v2.time_slot(), 0)
        day_value = current_game_day()

        if week_val == 5:
            glory_max_i = glory_max_i // 2
        if week_val == 7:
            glory_max_i = (glory_max_i * 3) // 4

        if people_to_int(_wnd_girl.job_value("jobgloryholeTommorow", 0), 0) != 0:
            generated_clients = (glory_max_i * (75 + 5 * procedural_randint(1, 10, "glory_clients_%s_%s" % (_wnd_girl_name, day_value)))) // 100
            _wnd_girl.set_sex_stat("clients_day_total", generated_clients)
            created = 0
            safety = 0
            while created < generated_clients and safety < 400:
                safety += 1
                event_hour = procedural_randint(2, 3, "glory_time_%s_%s_%s" % (_wnd_girl_name, day_value, safety))
                if week_val == 5:
                    event_hour = 2
                if week_val == 7:
                    event_hour = 3

                event_type = procedural_randint(1, 11, "glory_type_%s_%s_%s" % (_wnd_girl_name, day_value, safety))
                if event_type == 1 and current_time == 2:
                    event_type = 6
                if event_type == 3 and current_time == 2:
                    event_type = 9
                if event_type == 4 and week_val == 7:
                    event_type = 11

                try:
                    already_exists = int(CheckIfEventAlreadyExist(_wnd_girl_name, event_type) or 0)
                except Exception:
                    already_exists = 0

                if event_type > 4 or already_exists == 0:
                    TodaySexEvents_Add(_wnd_girl_name, event_hour, event_type, "Glory")
                    created += 1
        else:
            if max_clients_i > 0:
                generated_clients = procedural_randint(1, max_clients_i, "port_clients_%s_%s" % (_wnd_girl_name, day_value))
            else:
                generated_clients = 0
            if week_val == 5:
                generated_clients = 0
            _wnd_girl.set_sex_stat("clients_day_total", generated_clients)

            created = 0
            prostitution_max_type = 3 if _wnd_girl_name == "liza" else 4
            while created < generated_clients:
                event_type = procedural_randint(1, prostitution_max_type, "port_client_type_%s_%s_%s" % (_wnd_girl_name, day_value, created))
                TodaySexEvents_Add(_wnd_girl_name, 3, event_type, "Prostitution")
                created += 1
    return
