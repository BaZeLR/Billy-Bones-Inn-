            CurrentLoc.setdefault(person, "TavernMain")default HouseholdMorningState = {}        global HouseholdMorningState
        global HouseholdMorningState
                Melissa.sync_room_problem_state()                Melissa.sync_room_problem_state()    def _tavern_effective_location(person, time_value=None):
        key = str(person or "").strip().lower()
        if not key:
            return
        if target == "gloryhole":
            jobgloryholeTommorow[person] = 1
            jobwhoreTommorow[person] = 0
        elif target == "whore":
            jobgloryholeTommorow[person] = 0
            jobwhoreTommorow[person] = 1
        _tavern_restart_interaction() ""

        current_locations = _tavern_dict_value(CurrentLoc)
        explicit_loc = str(current_locations.get(key, "") or "")
        tavern_rooms = {
            "TavernMain",
            "TavernKitchen",
            "TavernSandraRoom",
            "TavernMelissaRoom",
            "TavernAmandaRoom",
        }

        hour_value = _tavern_int(calendar_v2.hour if time_value is None else time_value, 0)
        if key == "melissa":
            try:
                if Melissa.temp_room_active("TavernMyRoom", hour_value):
                    return "TavernMyRoom"
                if Melissa.temp_room_active("TavernAmandaRoom", hour_value):
                    return "TavernAmandaRoom"
                if Melissa.temp_room_active("TavernEmptyRoom", hour_value):
                    return "TavernEmptyRoom"
            except Exception:
                pass
        if explicit_loc == "TavernKitchen" and slot == 0 and _tavern_int(calendar_v2.hour, 8) < 12:
            return explicit_loc
        morning_issue = household_morning_issue_type(key, slot, calendar_v2.hour)
        if morning_issue in ("sick", "sleepy"):
            return _tavern_private_room(key)

        schedule_time_value = None if time_value is None else slot
        schedule_loc = str(npc_schedule_location(key, _tavern_int(calendar_v2.week, 1), schedule_time_value) or "")
        if schedule_loc:
            return schedule_loc

        if explicit_loc and explicit_loc not in tavern_rooms:
            return explicit_loc

        sunday_loc = _tavern_household_sunday_location(key, slot)
        if sunday_loc:
            return sunday_loc

        friday_evening_loc = _tavern_household_friday_evening_location(key, slot)
        if friday_evening_loc:
            return friday_evening_loc

        preopening_loc = _tavern_household_preopening_location(key, slot)
        if preopening_loc:
            return preopening_loc

        private_room = _tavern_private_room(key)
        if private_room and slot >= 4:
            return private_room

        if key in ("sandra", "melissa", "amanda"):
            if _girl_job_value(key, "jobkitchen"):
                return "TavernKitchen"
            if _girl_job_value(key, "jobcleaning"):
                return "TavernMain"
            if _girl_job_value(key, "jobwaitress"):
                return "TavernMain"
            if private_room:
                return private_room

        return explicit_loc
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))label menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    returnlabel menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    return

label menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    return    def _tavern_household_seed(person, hour_value=None, day_marker=None, weekday=None):
        key = str(person or "").strip().lower()
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        day_num = _tavern_int(dayspassed if day_marker is None else day_marker, 0)
        week_num = _tavern_int(week if weekday is None else weekday, 1)
        offsets = {"sandra": 1, "melissa": 3, "amanda": 5}
        return day_num + week_num + hour_num + int(offsets.get(key, 0))

    def _tavern_household_preopening_location(person, time_value=None, hour_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        weekday_num = _tavern_int(week, 1)

        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num == 7:
            return ""
        if slot >= 4 or hour_num >= 12:
            return ""
        if hour_num < 9:
            return "TavernKitchen"

        if hour_num < 10:
            options_map = {
                "sandra": ["TavernKitchen", "TavernStorage", "TavernKitchen", "TavernMain"],
                "melissa": ["TavernKitchen", "TavernStorage", "TavernMain", "Backyard"],
                "amanda": ["TavernKitchen", "TavernMain", "Backyard", "TavernAmandaRoom"],
            }
        elif hour_num < 11:
            options_map = {
                "sandra": ["TavernStorage", "TavernMain", "TavernKitchen", "Backyard"],
                "melissa": ["TavernStorage", "TavernMain", "Backyard", "TavernKitchen"],
                "amanda": ["TavernMain", "Backyard", "TavernStorage", "TavernAmandaRoom"],
            }
        else:
            options_map = {
                "sandra": ["TavernMain", "TavernKitchen", "TavernStorage", "Backyard"],
                "melissa": ["TavernMain", "TavernKitchen", "Backyard", "TavernMelissaRoom"],
                "amanda": ["TavernMain", "TavernKitchen", "Backyard", "TavernAmandaRoom"],
            }

        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, hour_num) % len(options)]

    def _tavern_household_sunday_location(person, time_value=None, hour_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        weekday_num = _tavern_int(week, 1)

        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num != 7:
            return ""
        if slot <= 1:
            return "Church"
        if hour_num >= 18:
            return _tavern_private_room(key) or "TavernMain"

        options_map = {
            "sandra": ["TavernKitchen", "Backyard", "TavernSandraRoom", "TavernMain"],
            "melissa": ["TavernMelissaRoom", "Backyard", "TavernMain", "TavernKitchen"],
            "amanda": ["TavernAmandaRoom", "Backyard", "TavernMain", "TavernKitchen"],
        }
        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, hour_num) % len(options)]

    def _tavern_household_friday_evening_location(person, time_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        weekday_num = _tavern_int(week, 1)
        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num != 5 or slot != 3:
            return ""
        if key == "amanda":
            return "FridayDance"
        options_map = {
            "sandra": ["FridayDance", "TavernSandraRoom"],
            "melissa": ["FridayDance", "TavernMelissaRoom"],
        }
        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, 18) % len(options)]
    def _tavern_effective_location(person, time_value=None):
        key = str(person or "").strip().lower()
        if not key:
            return ""

        info = getPersonInfo(key)
        explicit_loc = str(getattr(info, "location", "") or "")
        tavern_rooms = {
            "TavernMain",
            "TavernKitchen",
            "TavernSandraRoom",
            "TavernMelissaRoom",
            "TavernAmandaRoom",
        }

        hour_value = _tavern_int(calendar_v2.hour if time_value is None else time_value, 0)
        if key == "melissa":
            try:
                Melissa.sync_room_problem_state()
                if Melissa.temp_room_active("TavernMyRoom", hour_value):
                    return "TavernMyRoom"
                if Melissa.temp_room_active("TavernAmandaRoom", hour_value):
                    return "TavernAmandaRoom"
                if Melissa.temp_room_active("TavernEmptyRoom", hour_value):
                    return "TavernEmptyRoom"
            except Exception:
                pass
        if explicit_loc == "TavernKitchen" and slot == 0 and _tavern_int(hour, 8) < 12:
            return explicit_loc
        morning_issue = household_morning_issue_type(key, slot, hour)
        if morning_issue in ("sick", "sleepy"):
            return _tavern_private_room(key)

        schedule_time_value = None if time_value is None else slot
        schedule_loc = str(npc_schedule_location(key, _tavern_int(week, 1), schedule_time_value) or "")
        if schedule_loc:
            return schedule_loc

        if explicit_loc and explicit_loc not in tavern_rooms:
            return explicit_loc

        sunday_loc = _tavern_household_sunday_location(key, slot)
        if sunday_loc:
            return sunday_loc

        friday_evening_loc = _tavern_household_friday_evening_location(key, slot)
        if friday_evening_loc:
            return friday_evening_loc

        preopening_loc = _tavern_household_preopening_location(key, slot)
        if preopening_loc:
            return preopening_loc

        private_room = _tavern_private_room(key)
        if private_room and slot >= 4:
            return private_room

        if key in ("sandra", "melissa", "amanda"):
            if _girl_job_value(key, "jobkitchen"):
                return "TavernKitchen"
            if _girl_job_value(key, "jobcleaning"):
                return "TavernMain"
            if _girl_job_value(key, "jobwaitress"):
                return "TavernMain"
            if private_room:
                return private_room

        return explicit_loc
            CurrentLoc.setdefault(person, "TavernMain")default HouseholdMorningState = {}        global HouseholdMorningState
        global HouseholdMorningState
                Melissa.sync_room_problem_state()                Melissa.sync_room_problem_state()    def _tavern_effective_location(person, time_value=None):
        key = str(person or "").strip().lower()
        if not key:
            return
        if target == "gloryhole":
            jobgloryholeTommorow[person] = 1
            jobwhoreTommorow[person] = 0
        elif target == "whore":
            jobgloryholeTommorow[person] = 0
            jobwhoreTommorow[person] = 1
        _tavern_restart_interaction() ""

        current_locations = _tavern_dict_value(CurrentLoc)
        explicit_loc = str(current_locations.get(key, "") or "")
        tavern_rooms = {
            "TavernMain",
            "TavernKitchen",
            "TavernSandraRoom",
            "TavernMelissaRoom",
            "TavernAmandaRoom",
        }

        hour_value = _tavern_int(calendar_v2.hour if time_value is None else time_value, 0)
        if key == "melissa":
            try:
                if Melissa.temp_room_active("TavernMyRoom", hour_value):
                    return "TavernMyRoom"
                if Melissa.temp_room_active("TavernAmandaRoom", hour_value):
                    return "TavernAmandaRoom"
                if Melissa.temp_room_active("TavernEmptyRoom", hour_value):
                    return "TavernEmptyRoom"
            except Exception:
                pass
        if explicit_loc == "TavernKitchen" and slot == 0 and _tavern_int(calendar_v2.hour, 8) < 12:
            return explicit_loc
        morning_issue = household_morning_issue_type(key, slot, calendar_v2.hour)
        if morning_issue in ("sick", "sleepy"):
            return _tavern_private_room(key)

        schedule_time_value = None if time_value is None else slot
        schedule_loc = str(npc_schedule_location(key, _tavern_int(calendar_v2.week, 1), schedule_time_value) or "")
        if schedule_loc:
            return schedule_loc

        if explicit_loc and explicit_loc not in tavern_rooms:
            return explicit_loc

        sunday_loc = _tavern_household_sunday_location(key, slot)
        if sunday_loc:
            return sunday_loc

        friday_evening_loc = _tavern_household_friday_evening_location(key, slot)
        if friday_evening_loc:
            return friday_evening_loc

        preopening_loc = _tavern_household_preopening_location(key, slot)
        if preopening_loc:
            return preopening_loc

        private_room = _tavern_private_room(key)
        if private_room and slot >= 4:
            return private_room

        if key in ("sandra", "melissa", "amanda"):
            if _girl_job_value(key, "jobkitchen"):
                return "TavernKitchen"
            if _girl_job_value(key, "jobcleaning"):
                return "TavernMain"
            if _girl_job_value(key, "jobwaitress"):
                return "TavernMain"
            if private_room:
                return private_room

        return explicit_loc
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))label menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    returnlabel menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    return

label menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    return    def _tavern_household_seed(person, hour_value=None, day_marker=None, weekday=None):
        key = str(person or "").strip().lower()
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        day_num = _tavern_int(dayspassed if day_marker is None else day_marker, 0)
        week_num = _tavern_int(week if weekday is None else weekday, 1)
        offsets = {"sandra": 1, "melissa": 3, "amanda": 5}
        return day_num + week_num + hour_num + int(offsets.get(key, 0))

    def _tavern_household_preopening_location(person, time_value=None, hour_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        weekday_num = _tavern_int(week, 1)

        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num == 7:
            return ""
        if slot >= 4 or hour_num >= 12:
            return ""
        if hour_num < 9:
            return "TavernKitchen"

        if hour_num < 10:
            options_map = {
                "sandra": ["TavernKitchen", "TavernStorage", "TavernKitchen", "TavernMain"],
                "melissa": ["TavernKitchen", "TavernStorage", "TavernMain", "Backyard"],
                "amanda": ["TavernKitchen", "TavernMain", "Backyard", "TavernAmandaRoom"],
            }
        elif hour_num < 11:
            options_map = {
                "sandra": ["TavernStorage", "TavernMain", "TavernKitchen", "Backyard"],
                "melissa": ["TavernStorage", "TavernMain", "Backyard", "TavernKitchen"],
                "amanda": ["TavernMain", "Backyard", "TavernStorage", "TavernAmandaRoom"],
            }
        else:
            options_map = {
                "sandra": ["TavernMain", "TavernKitchen", "TavernStorage", "Backyard"],
                "melissa": ["TavernMain", "TavernKitchen", "Backyard", "TavernMelissaRoom"],
                "amanda": ["TavernMain", "TavernKitchen", "Backyard", "TavernAmandaRoom"],
            }

        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, hour_num) % len(options)]

    def _tavern_household_sunday_location(person, time_value=None, hour_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        weekday_num = _tavern_int(week, 1)

        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num != 7:
            return ""
        if slot <= 1:
            return "Church"
        if hour_num >= 18:
            return _tavern_private_room(key) or "TavernMain"

        options_map = {
            "sandra": ["TavernKitchen", "Backyard", "TavernSandraRoom", "TavernMain"],
            "melissa": ["TavernMelissaRoom", "Backyard", "TavernMain", "TavernKitchen"],
            "amanda": ["TavernAmandaRoom", "Backyard", "TavernMain", "TavernKitchen"],
        }
        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, hour_num) % len(options)]

    def _tavern_household_friday_evening_location(person, time_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        weekday_num = _tavern_int(week, 1)
        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num != 5 or slot != 3:
            return ""
        if key == "amanda":
            return "FridayDance"
        options_map = {
            "sandra": ["FridayDance", "TavernSandraRoom"],
            "melissa": ["FridayDance", "TavernMelissaRoom"],
        }
        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, 18) % len(options)]
    def _tavern_effective_location(person, time_value=None):
        key = str(person or "").strip().lower()
        if not key:
            return ""

        info = getPersonInfo(key)
        explicit_loc = str(getattr(info, "location", "") or "")
        tavern_rooms = {
            "TavernMain",
            "TavernKitchen",
            "TavernSandraRoom",
            "TavernMelissaRoom",
            "TavernAmandaRoom",
        }

        hour_value = _tavern_int(calendar_v2.hour if time_value is None else time_value, 0)
        if key == "melissa":
            try:
                Melissa.sync_room_problem_state()
                if Melissa.temp_room_active("TavernMyRoom", hour_value):
                    return "TavernMyRoom"
                if Melissa.temp_room_active("TavernAmandaRoom", hour_value):
                    return "TavernAmandaRoom"
                if Melissa.temp_room_active("TavernEmptyRoom", hour_value):
                    return "TavernEmptyRoom"
            except Exception:
                pass
        if explicit_loc == "TavernKitchen" and slot == 0 and _tavern_int(hour, 8) < 12:
            return explicit_loc
        morning_issue = household_morning_issue_type(key, slot, hour)
        if morning_issue in ("sick", "sleepy"):
            return _tavern_private_room(key)

        schedule_time_value = None if time_value is None else slot
        schedule_loc = str(npc_schedule_location(key, _tavern_int(week, 1), schedule_time_value) or "")
        if schedule_loc:
            return schedule_loc

        if explicit_loc and explicit_loc not in tavern_rooms:
            return explicit_loc

        sunday_loc = _tavern_household_sunday_location(key, slot)
        if sunday_loc:
            return sunday_loc

        friday_evening_loc = _tavern_household_friday_evening_location(key, slot)
        if friday_evening_loc:
            return friday_evening_loc

        preopening_loc = _tavern_household_preopening_location(key, slot)
        if preopening_loc:
            return preopening_loc

        private_room = _tavern_private_room(key)
        if private_room and slot >= 4:
            return private_room

        if key in ("sandra", "melissa", "amanda"):
            if _girl_job_value(key, "jobkitchen"):
                return "TavernKitchen"
            if _girl_job_value(key, "jobcleaning"):
                return "TavernMain"
            if _girl_job_value(key, "jobwaitress"):
                return "TavernMain"
            if private_room:
                return private_room

        return explicit_loc
            CurrentLoc.setdefault(person, "TavernMain")default HouseholdMorningState = {}        global HouseholdMorningState
        global HouseholdMorningState
                Melissa.sync_room_problem_state()                Melissa.sync_room_problem_state()    def _tavern_effective_location(person, time_value=None):
        key = str(person or "").strip().lower()
        if not key:
            return
        if target == "gloryhole":
            jobgloryholeTommorow[person] = 1
            jobwhoreTommorow[person] = 0
        elif target == "whore":
            jobgloryholeTommorow[person] = 0
            jobwhoreTommorow[person] = 1
        _tavern_restart_interaction() ""

        current_locations = _tavern_dict_value(CurrentLoc)
        explicit_loc = str(current_locations.get(key, "") or "")
        tavern_rooms = {
            "TavernMain",
            "TavernKitchen",
            "TavernSandraRoom",
            "TavernMelissaRoom",
            "TavernAmandaRoom",
        }

        hour_value = _tavern_int(calendar_v2.hour if time_value is None else time_value, 0)
        if key == "melissa":
            try:
                if Melissa.temp_room_active("TavernMyRoom", hour_value):
                    return "TavernMyRoom"
                if Melissa.temp_room_active("TavernAmandaRoom", hour_value):
                    return "TavernAmandaRoom"
                if Melissa.temp_room_active("TavernEmptyRoom", hour_value):
                    return "TavernEmptyRoom"
            except Exception:
                pass
        if explicit_loc == "TavernKitchen" and slot == 0 and _tavern_int(calendar_v2.hour, 8) < 12:
            return explicit_loc
        morning_issue = household_morning_issue_type(key, slot, calendar_v2.hour)
        if morning_issue in ("sick", "sleepy"):
            return _tavern_private_room(key)

        schedule_time_value = None if time_value is None else slot
        schedule_loc = str(npc_schedule_location(key, _tavern_int(calendar_v2.week, 1), schedule_time_value) or "")
        if schedule_loc:
            return schedule_loc

        if explicit_loc and explicit_loc not in tavern_rooms:
            return explicit_loc

        sunday_loc = _tavern_household_sunday_location(key, slot)
        if sunday_loc:
            return sunday_loc

        friday_evening_loc = _tavern_household_friday_evening_location(key, slot)
        if friday_evening_loc:
            return friday_evening_loc

        preopening_loc = _tavern_household_preopening_location(key, slot)
        if preopening_loc:
            return preopening_loc

        private_room = _tavern_private_room(key)
        if private_room and slot >= 4:
            return private_room

        if key in ("sandra", "melissa", "amanda"):
            if _girl_job_value(key, "jobkitchen"):
                return "TavernKitchen"
            if _girl_job_value(key, "jobcleaning"):
                return "TavernMain"
            if _girl_job_value(key, "jobwaitress"):
                return "TavernMain"
            if private_room:
                return private_room

        return explicit_loc
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))label menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    returnlabel menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    return

label menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    return    def _tavern_household_seed(person, hour_value=None, day_marker=None, weekday=None):
        key = str(person or "").strip().lower()
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        day_num = _tavern_int(dayspassed if day_marker is None else day_marker, 0)
        week_num = _tavern_int(week if weekday is None else weekday, 1)
        offsets = {"sandra": 1, "melissa": 3, "amanda": 5}
        return day_num + week_num + hour_num + int(offsets.get(key, 0))

    def _tavern_household_preopening_location(person, time_value=None, hour_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        weekday_num = _tavern_int(week, 1)

        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num == 7:
            return ""
        if slot >= 4 or hour_num >= 12:
            return ""
        if hour_num < 9:
            return "TavernKitchen"

        if hour_num < 10:
            options_map = {
                "sandra": ["TavernKitchen", "TavernStorage", "TavernKitchen", "TavernMain"],
                "melissa": ["TavernKitchen", "TavernStorage", "TavernMain", "Backyard"],
                "amanda": ["TavernKitchen", "TavernMain", "Backyard", "TavernAmandaRoom"],
            }
        elif hour_num < 11:
            options_map = {
                "sandra": ["TavernStorage", "TavernMain", "TavernKitchen", "Backyard"],
                "melissa": ["TavernStorage", "TavernMain", "Backyard", "TavernKitchen"],
                "amanda": ["TavernMain", "Backyard", "TavernStorage", "TavernAmandaRoom"],
            }
        else:
            options_map = {
                "sandra": ["TavernMain", "TavernKitchen", "TavernStorage", "Backyard"],
                "melissa": ["TavernMain", "TavernKitchen", "Backyard", "TavernMelissaRoom"],
                "amanda": ["TavernMain", "TavernKitchen", "Backyard", "TavernAmandaRoom"],
            }

        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, hour_num) % len(options)]

    def _tavern_household_sunday_location(person, time_value=None, hour_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        weekday_num = _tavern_int(week, 1)

        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num != 7:
            return ""
        if slot <= 1:
            return "Church"
        if hour_num >= 18:
            return _tavern_private_room(key) or "TavernMain"

        options_map = {
            "sandra": ["TavernKitchen", "Backyard", "TavernSandraRoom", "TavernMain"],
            "melissa": ["TavernMelissaRoom", "Backyard", "TavernMain", "TavernKitchen"],
            "amanda": ["TavernAmandaRoom", "Backyard", "TavernMain", "TavernKitchen"],
        }
        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, hour_num) % len(options)]

    def _tavern_household_friday_evening_location(person, time_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        weekday_num = _tavern_int(week, 1)
        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if weekday_num != 5 or slot != 3:
            return ""
        if key == "amanda":
            return "FridayDance"
        options_map = {
            "sandra": ["FridayDance", "TavernSandraRoom"],
            "melissa": ["FridayDance", "TavernMelissaRoom"],
        }
        options = list(options_map.get(key, []))
        if not options:
            return ""
        return options[_tavern_household_seed(key, 18) % len(options)]
    def _tavern_effective_location(person, time_value=None):
        key = str(person or "").strip().lower()
        if not key:
            return ""

        info = getPersonInfo(key)
        explicit_loc = str(getattr(info, "location", "") or "")
        tavern_rooms = {
            "TavernMain",
            "TavernKitchen",
            "TavernSandraRoom",
            "TavernMelissaRoom",
            "TavernAmandaRoom",
        }

        hour_value = _tavern_int(calendar_v2.hour if time_value is None else time_value, 0)
        if key == "melissa":
            try:
                Melissa.sync_room_problem_state()
                if Melissa.temp_room_active("TavernMyRoom", hour_value):
                    return "TavernMyRoom"
                if Melissa.temp_room_active("TavernAmandaRoom", hour_value):
                    return "TavernAmandaRoom"
                if Melissa.temp_room_active("TavernEmptyRoom", hour_value):
                    return "TavernEmptyRoom"
            except Exception:
                pass
        if explicit_loc == "TavernKitchen" and slot == 0 and _tavern_int(hour, 8) < 12:
            return explicit_loc
        morning_issue = household_morning_issue_type(key, slot, hour)
        if morning_issue in ("sick", "sleepy"):
            return _tavern_private_room(key)

        schedule_time_value = None if time_value is None else slot
        schedule_loc = str(npc_schedule_location(key, _tavern_int(week, 1), schedule_time_value) or "")
        if schedule_loc:
            return schedule_loc

        if explicit_loc and explicit_loc not in tavern_rooms:
            return explicit_loc

        sunday_loc = _tavern_household_sunday_location(key, slot)
        if sunday_loc:
            return sunday_loc

        friday_evening_loc = _tavern_household_friday_evening_location(key, slot)
        if friday_evening_loc:
            return friday_evening_loc

        preopening_loc = _tavern_household_preopening_location(key, slot)
        if preopening_loc:
            return preopening_loc

        private_room = _tavern_private_room(key)
        if private_room and slot >= 4:
            return private_room

        if key in ("sandra", "melissa", "amanda"):
            if _girl_job_value(key, "jobkitchen"):
                return "TavernKitchen"
            if _girl_job_value(key, "jobcleaning"):
                return "TavernMain"
            if _girl_job_value(key, "jobwaitress"):
                return "TavernMain"
            if private_room:
                return private_room

        return explicit_loc
# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    import renpy.exports as renpy_module
    import random as tavern_random
    import random as tavern_random
    import random as tavern_random
    import random as tavern_random
    import random as tavern_random
    import random as tavern_random

    def _tavern_dict_value(value):
        return value if isinstance(value, dict) else {}

    def _tavern_restart_interaction():
        fn = getattr(renpy_module, "restart_interaction", None)
        if callable(fn):
            fn()

    def show_tavern_report_main_ui_state(person=""):
        global TavernReportSelectedPerson, UI_mode, current_action_content, current_action_title, current_action_items
        TavernReportSelectedPerson = str(person or "")
        UI_mode = "tavern"
        current_action_content = None
        if TavernReportSelectedPerson:
            current_action_title = "Назначения: " + _tavern_name(TavernReportSelectedPerson)
            current_action_items = _tavern_worker_action_items(TavernReportSelectedPerson, "__main_ui__")
        else:
            current_action_title = "Трактир"
            current_action_items = _tavern_report_action_items("__main_ui__")
        _tavern_restart_interaction()

    def _tavern_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def ensure_default_tavern_jobs(sync_tomorrow=True):
        hall_workers = {
            "sandra": {"kitchen": 1, "cleaning": 0, "waitress": 0},
            "melissa": {"kitchen": 0, "cleaning": 1, "waitress": 1},
            "amanda": {"kitchen": 0, "cleaning": 1, "waitress": 1},
        }
        optional_workers = ("georgett", "liza", "becky", "irma", "inga", "clara")

        for person, jobs in hall_workers.items():
            jobHallAvail.setdefault(person, 1)
            jobWhoreAvail.setdefault(person, 0)
            jobGloryHoleAvail.setdefault(person, 0)
            jobkitchen.setdefault(person, jobs["kitchen"])
            jobcleaning.setdefault(person, jobs["cleaning"])
            jobwaitress.setdefault(person, jobs["waitress"])
            jobwhore.setdefault(person, 0)
            jobgloryhole.setdefault(person, 0)
            if sync_tomorrow:
                jobkitchentomorrow.setdefault(person, jobkitchen.get(person, 0))
                jobcleaningtomorrow.setdefault(person, jobcleaning.get(person, 0))
                jobwaitresstomorrow.setdefault(person, jobwaitress.get(person, 0))
                jobwhoreTommorow.setdefault(person, jobwhore.get(person, 0))
                jobgloryholeTommorow.setdefault(person, jobgloryhole.get(person, 0))

        for person in optional_workers:
            jobHallAvail.setdefault(person, 0)
            jobWhoreAvail.setdefault(person, 0)
            jobGloryHoleAvail.setdefault(person, 0)
            jobkitchen.setdefault(person, 0)
            jobcleaning.setdefault(person, 0)
            jobwaitress.setdefault(person, 0)
            jobwhore.setdefault(person, 0)
            jobgloryhole.setdefault(person, 0)
            if sync_tomorrow:
                jobkitchentomorrow.setdefault(person, jobkitchen.get(person, 0))
                jobcleaningtomorrow.setdefault(person, jobcleaning.get(person, 0))
                jobwaitresstomorrow.setdefault(person, jobwaitress.get(person, 0))
                jobwhoreTommorow.setdefault(person, jobwhore.get(person, 0))
                jobgloryholeTommorow.setdefault(person, jobgloryhole.get(person, 0))

        return True

    def ensure_default_tavern_jobs(sync_tomorrow=True):
        hall_workers = {
            "sandra": {"kitchen": 1, "cleaning": 0, "waitress": 0},
            "melissa": {"kitchen": 0, "cleaning": 1, "waitress": 1},
            "amanda": {"kitchen": 0, "cleaning": 1, "waitress": 1},
        }
        optional_workers = ("georgett", "liza", "becky", "irma", "inga", "clara")

        for person, jobs in hall_workers.items():
            jobHallAvail.setdefault(person, 1)
            jobWhoreAvail.setdefault(person, 0)
            jobGloryHoleAvail.setdefault(person, 0)
            jobkitchen.setdefault(person, jobs["kitchen"])
            jobcleaning.setdefault(person, jobs["cleaning"])
            jobwaitress.setdefault(person, jobs["waitress"])
            jobwhore.setdefault(person, 0)
            jobgloryhole.setdefault(person, 0)
            if sync_tomorrow:
                jobkitchentomorrow.setdefault(person, jobkitchen.get(person, 0))
                jobcleaningtomorrow.setdefault(person, jobcleaning.get(person, 0))
                jobwaitresstomorrow.setdefault(person, jobwaitress.get(person, 0))
                jobwhoreTommorow.setdefault(person, jobwhore.get(person, 0))
                jobgloryholeTommorow.setdefault(person, jobgloryhole.get(person, 0))

        for person in optional_workers:
            jobHallAvail.setdefault(person, 0)
            jobWhoreAvail.setdefault(person, 0)
            jobGloryHoleAvail.setdefault(person, 0)
            jobkitchen.setdefault(person, 0)
            jobcleaning.setdefault(person, 0)
            jobwaitress.setdefault(person, 0)
            jobwhore.setdefault(person, 0)
            jobgloryhole.setdefault(person, 0)
            if sync_tomorrow:
                jobkitchentomorrow.setdefault(person, jobkitchen.get(person, 0))
                jobcleaningtomorrow.setdefault(person, jobcleaning.get(person, 0))
                jobwaitresstomorrow.setdefault(person, jobwaitress.get(person, 0))
                jobwhoreTommorow.setdefault(person, jobwhore.get(person, 0))
                jobgloryholeTommorow.setdefault(person, jobgloryhole.get(person, 0))

        return True

    def ensure_default_tavern_jobs(sync_tomorrow=True):
        hall_workers = {
            "sandra": {"kitchen": 1, "cleaning": 0, "waitress": 0},
            "melissa": {"kitchen": 0, "cleaning": 1, "waitress": 1},
            "amanda": {"kitchen": 0, "cleaning": 1, "waitress": 1},
        }
        optional_workers = ("georgett", "liza", "becky", "irma", "inga", "clara")

        for person, jobs in hall_workers.items():
            jobHallAvail.setdefault(person, 1)
            jobWhoreAvail.setdefault(person, 0)
            jobGloryHoleAvail.setdefault(person, 0)
            jobkitchen.setdefault(person, jobs["kitchen"])
            jobcleaning.setdefault(person, jobs["cleaning"])
            jobwaitress.setdefault(person, jobs["waitress"])
            jobwhore.setdefault(person, 0)
            jobgloryhole.setdefault(person, 0)
            if sync_tomorrow:
                jobkitchentomorrow.setdefault(person, jobkitchen.get(person, 0))
                jobcleaningtomorrow.setdefault(person, jobcleaning.get(person, 0))
                jobwaitresstomorrow.setdefault(person, jobwaitress.get(person, 0))
                jobwhoreTommorow.setdefault(person, jobwhore.get(person, 0))
                jobgloryholeTommorow.setdefault(person, jobgloryhole.get(person, 0))

        for person in optional_workers:
            jobHallAvail.setdefault(person, 0)
            jobWhoreAvail.setdefault(person, 0)
            jobGloryHoleAvail.setdefault(person, 0)
            jobkitchen.setdefault(person, 0)
            jobcleaning.setdefault(person, 0)
            jobwaitress.setdefault(person, 0)
            jobwhore.setdefault(person, 0)
            jobgloryhole.setdefault(person, 0)
            if sync_tomorrow:
                jobkitchentomorrow.setdefault(person, jobkitchen.get(person, 0))
                jobcleaningtomorrow.setdefault(person, jobcleaning.get(person, 0))
                jobwaitresstomorrow.setdefault(person, jobwaitress.get(person, 0))
                jobwhoreTommorow.setdefault(person, jobwhore.get(person, 0))
                jobgloryholeTommorow.setdefault(person, jobgloryhole.get(person, 0))

        return True

    def ensure_default_tavern_jobs(sync_tomorrow=True):
        hall_workers = {
            "sandra": {"kitchen": 1, "cleaning": 0, "waitress": 0},
            "melissa": {"kitchen": 0, "cleaning": 1, "waitress": 1},
            "amanda": {"kitchen": 0, "cleaning": 1, "waitress": 1},
        }
        optional_workers = ("georgett", "liza", "becky", "irma", "inga", "clara")

        for person, jobs in hall_workers.items():
            info = _tavern_person_info(person)
            if info is None:
                continue
            defaults = {
                "jobHallAvail": 1, "jobWhoreAvail": 0, "jobGloryHoleAvail": 0,
                "jobkitchen": jobs["kitchen"], "jobcleaning": jobs["cleaning"],
                "jobwaitress": jobs["waitress"], "jobwhore": 0, "jobgloryhole": 0,
            }
            for job_key, value in defaults.items():
                info.jobs.setdefault(job_key, value)
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))

        for person in optional_workers:
            info = _tavern_person_info(person)
            if info is None:
                continue
            for job_key in ("jobHallAvail", "jobWhoreAvail", "jobGloryHoleAvail", "jobkitchen", "jobcleaning", "jobwaitress", "jobwhore", "jobgloryhole"):
                info.jobs.setdefault(job_key, 0)
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))

        return True

    def ensure_default_tavern_jobs(sync_tomorrow=True):
        hall_workers = {
            "sandra": {"kitchen": 1, "cleaning": 0, "waitress": 0},
            "melissa": {"kitchen": 0, "cleaning": 1, "waitress": 1},
            "amanda": {"kitchen": 0, "cleaning": 1, "waitress": 1},
        }
        optional_workers = ("georgett", "liza", "becky", "irma", "inga", "clara")

        for person, jobs in hall_workers.items():
            info = _tavern_person_info(person)
            if info is None:
                continue
            defaults = {
                "jobHallAvail": 1, "jobWhoreAvail": 0, "jobGloryHoleAvail": 0,
                "jobkitchen": jobs["kitchen"], "jobcleaning": jobs["cleaning"],
                "jobwaitress": jobs["waitress"], "jobwhore": 0, "jobgloryhole": 0,
            }
            for job_key, value in defaults.items():
                info.jobs.setdefault(job_key, value)
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))

        for person in optional_workers:
            info = _tavern_person_info(person)
            if info is None:
                continue
            for job_key in ("jobHallAvail", "jobWhoreAvail", "jobGloryHoleAvail", "jobkitchen", "jobcleaning", "jobwaitress", "jobwhore", "jobgloryhole"):
                info.jobs.setdefault(job_key, 0)
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))

        return True

    def ensure_default_tavern_jobs(sync_tomorrow=True):
        hall_workers = {
            "sandra": {"kitchen": 1, "cleaning": 0, "waitress": 0},
            "melissa": {"kitchen": 0, "cleaning": 1, "waitress": 1},
            "amanda": {"kitchen": 0, "cleaning": 1, "waitress": 1},
        }
        optional_workers = ("georgett", "liza", "becky", "irma", "inga", "clara")

        for person, jobs in hall_workers.items():
            info = _tavern_person_info(person)
            if info is None:
                continue
            defaults = {
                "jobHallAvail": 1, "jobWhoreAvail": 0, "jobGloryHoleAvail": 0,
                "jobkitchen": jobs["kitchen"], "jobcleaning": jobs["cleaning"],
                "jobwaitress": jobs["waitress"], "jobwhore": 0, "jobgloryhole": 0,
            }
            for job_key, value in defaults.items():
                info.jobs.setdefault(job_key, value)
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))

        for person in optional_workers:
            info = _tavern_person_info(person)
            if info is None:
                continue
            for job_key in ("jobHallAvail", "jobWhoreAvail", "jobGloryHoleAvail", "jobkitchen", "jobcleaning", "jobwaitress", "jobwhore", "jobgloryhole"):
                info.jobs.setdefault(job_key, 0)
            if sync_tomorrow:
                info.jobs.setdefault("jobkitchentomorrow", info.job_value("jobkitchen", 0))
                info.jobs.setdefault("jobcleaningtomorrow", info.job_value("jobcleaning", 0))
                info.jobs.setdefault("jobwaitresstomorrow", info.job_value("jobwaitress", 0))
                info.jobs.setdefault("jobwhoreTommorow", info.job_value("jobwhore", 0))
                info.jobs.setdefault("jobgloryholeTommorow", info.job_value("jobgloryhole", 0))

        return True

    def _tavern_get_stat(mapping, person, default=0):
        mapping = _tavern_dict_value(mapping)
        if person in mapping:
            return mapping.get(person, default)
        person_l = str(person).lower()
        for k, v in mapping.items():
            if str(k).lower() == person_l:
                return v
        return default

    def _tavern_name(person):
        display = people_display_name(person)
        if str(display or "").strip():
            return str(display)
        return str(person).capitalize()

    def _tavern_person_info(person):
        return getPersonInfo(str(person or "").strip().lower())

    def _tavern_person_corruption(person):
        info = _tavern_person_info(person)
        return _tavern_int(getattr(info, "corruption", 0), 0)

    def _tavern_person_relation(person):
        info = _tavern_person_info(person)
        return _tavern_int(getattr(info, "rel", 0), 0)

    def _tavern_private_room(person):
        key = str(person or "").strip().lower()
        return {
            "sandra": "TavernSandraRoom",
            "melissa": "TavernMelissaRoom",
            "amanda": "TavernAmandaRoom",
        }.get(key, "")

    def _household_morning_state_key(person="", day_marker=None):
        return "%s:%s" % (str(person or "").strip().lower(), int(dayspassed if day_marker is None else day_marker or 0))

    def _household_sleep_indecent_possible(person=""):
        key = str(person or "").strip().lower()
        if key == "amanda":
            return _tavern_person_corruption("amanda") >= 30 or int(Amanda.var.get("suckyou", 0) or 0) > 0 or int(Amanda.var.get("fuckyou", 0) or 0) > 0
        if key == "melissa":
            return _tavern_person_corruption("melissa") >= 18 or _tavern_person_relation("melissa") >= 10
        if key == "sandra":
            return _tavern_person_corruption("sandra") >= 20 or _tavern_person_relation("sandra") >= 10
        return False

    def _ensure_household_morning_state(person="", day_marker=None):
        key = str(person or "").strip().lower()
        if key not in ("sandra", "melissa", "amanda"):
            return {"issue": "", "resolved": 1, "indecent": 0}
        state_key = _household_morning_state_key(key, day_marker)
        entry = household.morning_state.get(state_key)
        if not isinstance(entry, dict):
            issue_code = ""
            indecent_flag = 0
            if int(week or 0) != 7 and tavern_random.randint(1, 100) <= 15:
                issue_code = "sick" if tavern_random.randint(1, 2) == 1 else "sleepy"
                if issue_code == "sleepy" and _household_sleep_indecent_possible(key) and tavern_random.randint(1, 100) <= 45:
                    indecent_flag = 1
            entry = {
                "issue": issue_code,
                "resolved": 0,
                "indecent": indecent_flag,
            }
            household.morning_state[state_key] = entry
        return household.morning_state.get(state_key, {"issue": "", "resolved": 1, "indecent": 0})

    def household_morning_issue_type(person="", time_value=None, hour_value=None):
        key = str(person or "").strip().lower()
        slot = _tavern_int(time if time_value is None else time_value, 0)
        hour_num = _tavern_int(hour if hour_value is None else hour_value, 8)
        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if _tavern_int(week, 1) == 7 or slot >= 4 or hour_num >= 12:
            return ""
        entry = _ensure_household_morning_state(key)
        if int(entry.get("resolved", 0) or 0) != 0:
            return ""
        return str(entry.get("issue", "") or "").strip()

    def household_morning_issue_indecent(person=""):
        entry = _ensure_household_morning_state(person)
        return int(entry.get("indecent", 0) or 0) == 1 and household_morning_issue_type(person) == "sleepy"

    def household_clear_morning_issue(person=""):
        key = str(person or "").strip().lower()
        if key not in ("sandra", "melissa", "amanda"):
            return 0
        entry = dict(_ensure_household_morning_state(key) or {})
        entry["resolved"] = 1
        household.morning_state[_household_morning_state_key(key)] = entry
        return 1

    def household_needs_reconcile(person=""):
        key = str(person or "").strip().lower()
        info = _tavern_person_info(key)
        talked_today = _tavern_int(getattr(info, "talked_today", 0), 0)
        return key in ("sandra", "melissa", "amanda") and _tavern_person_relation(key) < 5 and talked_today < 3

    def player_recent_sex_count(day_span=2):
        min_day = max(0, int(dayspassed or 0) - max(1, int(day_span or 2)) + 1)
        total = 0
        seen_rows = set()
        for girl_name in list(AllGirlNames or []):
            for row in sex_history_rows(girl_name):
                try:
                    row_day = int(row.get("Day", 0) or 0)
                except Exception:
                    row_day = 0
                if row_day < min_day:
                    continue
                dude_name = str(row.get("DudeName", "") or "").strip().lower()
                if dude_name not in ("вы", "you"):
                    continue
                row_token = (
                    str(girl_name or ""),
                    int(row.get("RowId", 0) or 0),
                    row_day,
                )
                if row_token in seen_rows:
                    continue
                seen_rows.add(row_token)
                total += 1
        return total

    def player_has_visible_morning_bulge():
        return int(player_recent_sex_count(2) or 0) > 2

    def household_breakfast_attendee_ids():
        if bool(player.tavern_management.breakfast.event_active) and player.tavern_management.breakfast.present_ids is not None:
            return [str(row or "").strip().lower() for row in list(player.tavern_management.breakfast.present_ids or []) if str(row or "").strip()]

        try:
            visible_ids = set([str(row or "").strip().lower() for row in list(getNPCids("TavernKitchen") or [])])
        except Exception:
            visible_ids = set()
            for npc_id in ("sandra", "melissa", "amanda", "becky"):
                if str(getLocation(npc_id) or "") == "TavernKitchen":
                    visible_ids.add(npc_id)

        return [npc_id for npc_id in ("sandra", "melissa", "amanda", "becky") if npc_id in visible_ids]

    def household_breakfast_absence_lines():
        lines = []
        absent_ids = set()
        try:
            absent_ids = set(tavern_breakfast_absent_ids() or [])
        except Exception:
            absent_ids = set()
        for npc_id in ("sandra", "melissa", "amanda"):
            if absent_ids and npc_id not in absent_ids:
                continue
            if str(getLocation(npc_id) or "") == "TavernKitchen":
                continue
            npc_name = _tavern_name(npc_id)
            issue_code = household_morning_issue_type(npc_id)
            if issue_code == "sick":
                lines.append("%s с утра расклеилась и осталась в своей комнате. Без лечебного зелья сегодня ее к столу не вытащить." % npc_name)
            elif issue_code == "sleepy":
                lines.append("%s все еще отсыпается у себя и пока не явилась к общему столу." % npc_name)
        return lines

    def household_room_issue_notice_text(person=""):
        key = str(person or "").strip().lower()
        lines = []
        if key == "melissa":
            try:
                Melissa.sync_room_problem_state()
            except Exception:
                pass
            try:
            except Exception:
                pass
            if Melissa.bats_stage() >= 7 and Melissa.bats_stage() < 8:
                repair_day = int(Melissa.var.get("roof_repair_complete_day", -1) or -1)
                if repair_day > int(dayspassed or 0):
                    days_left = repair_day - int(dayspassed or 0)
                    lines.append("Над комнатой Мелиссы уже заказана починка крыши. Мастерам осталось еще примерно %s дн., прежде чем можно будет окончательно считать дело закрытым." % days_left)
                elif Melissa.bats_repair_complete():
                    lines.append("Похоже, мастера уже закончили с крышей: над комнатой стало тихо, щели подлатаны, и теперь можно сказать Мелиссе, что она может окончательно возвращаться к себе.")
        issue_code = household_morning_issue_type(key)
        if issue_code == "sick":
            lines.append("%s выглядит нездорово и явно не собирается сегодня вставать без посторонней помощи." % _tavern_name(key))
        elif issue_code == "sleepy":
            lines.append("%s все еще валяется в постели и явно проспала общий подъем." % _tavern_name(key))
        return "\n\n".join([line for line in lines if str(line or "").strip() != ""])

    def _tavern_join_names(keys):
        names = [_tavern_name(k) for k in keys if str(k).strip()]
        if not names:
            return "никто"
        if len(names) == 1:
            return names[0]
        if len(names) == 2:
            return names[0] + " и " + names[1]
        return ", ".join(names[:-1]) + " и " + names[-1]

    def tavern_household_present_names(room_code=""):
        room_key = str(room_code or "").strip()
        keys = [name for name in ("sandra", "melissa", "amanda") if str(getLocation(name) or "") == room_key]
        return _tavern_join_names(keys)

    def _tavern_job_room(job_type):
        return {
            "jobkitchen": "TavernKitchen",
            "jobcleaning": "TavernMain",
            "jobwaitress": "TavernMain",
        }.get(str(job_type or ""), "")

    def _tavern_job_keys(job_type, room_code=None):
        target_room = str(room_code or _tavern_job_room(job_type) or "")
        return girls_by_job(job_type, target_room)

    def NamesList(job_type, room_code=None):
        """Строка имен для выбранного типа работы."""
        return _tavern_join_names(_tavern_job_keys(job_type, room_code))

    def DispFrac(value):
        """
        QSP parity:
        17 -> "1,7", 10 -> "1", 3 -> "0,3".
        """
        try:
            num = int(value or 0)
        except Exception:
            num = 0

        frac_part = num % 10
        int_part = (num - frac_part) // 10
        if frac_part == 0:
            return str(int_part)
        return str(int_part) + "," + str(frac_part)

    def _tavern_worker_dress(person):
        dressdefault_map = _tavern_dict_value(dressdefault)
        dressdesc_map = _tavern_dict_value(DressDesc)
        fulldesc_map = _tavern_dict_value(FullDressDesc)
        topdress_map = _tavern_dict_value(topdress)
        bottomdress_map = _tavern_dict_value(bottomdress)
        dress_top_map = _tavern_dict_value(DressTopPart)
        dress_bottom_map = _tavern_dict_value(DressBottomPart)
        part_desc_map = _tavern_dict_value(DressPartDesc)

        dress_code = str(dressdefault_map.get(person, ""))
        if dress_code and dress_code in dressdesc_map:
            return str(dressdesc_map[dress_code])

        top_code = str(topdress_map.get(person, "")) or str(dress_top_map.get(dress_code, ""))
        bottom_code = str(bottomdress_map.get(person, "")) or str(dress_bottom_map.get(dress_code, ""))
        top_line = str(part_desc_map.get(top_code, "")).strip()
        bottom_line = str(part_desc_map.get(bottom_code, "")).strip()
        if top_line and bottom_line:
            return top_line + ", " + bottom_line
        if top_line:
            return top_line
        if bottom_line:
            return bottom_line

        if dress_code and dress_code in fulldesc_map:
            return str(fulldesc_map[dress_code])
        if dress_code:
            return dress_code
        return "обычная рабочая одежда"

    def _tavern_worker_summary(person):
        info = _tavern_person_info(person)
        skills = getattr(info, "skills", {}) if info is not None else {}
        cooking_value = _tavern_int(skills.get("cooking", 0), 0)
        cleaning_value = _tavern_int(skills.get("cleaning", 0), 0)
        waitress_value = _tavern_int(skills.get("waitress", 0), 0)
        friends_value = _tavern_person_relation(person)

        current_jobs = []
        if _girl_job_value(person, "jobkitchen"):
            current_jobs.append("кухня")
        if _girl_job_value(person, "jobcleaning"):
            current_jobs.append("уборка")
        if _girl_job_value(person, "jobwaitress"):
            current_jobs.append("зал")
        if _girl_job_value(person, "jobwhore"):
            current_jobs.append("интим")
        if _girl_job_value(person, "jobgloryhole"):
            current_jobs.append("глорихол")

        jobs_text = ", ".join(current_jobs) if current_jobs else "без смены"
        return "Навыки: кухня %d / уборка %d / зал %d. Дружба: %d. Сейчас: %s." % (
            cooking_value,
            cleaning_value,
            waitress_value,
            friends_value,
            jobs_text,
        )

    def _tavern_worker_tomorrow_jobs(person):
        tomorrow_jobs = []
        if _tavern_int(_tavern_dict_value(jobkitchentomorrow).get(person, 0), 0):
            tomorrow_jobs.append("кухня")
        if _tavern_int(_tavern_dict_value(jobcleaningtomorrow).get(person, 0), 0):
            tomorrow_jobs.append("уборка")
        if _tavern_int(_tavern_dict_value(jobwaitresstomorrow).get(person, 0), 0):
            tomorrow_jobs.append("зал")
        if _girl_job_value(person, "jobwhoreTommorow"):
            tomorrow_jobs.append("интим")
        if _girl_job_value(person, "jobgloryholeTommorow"):
            tomorrow_jobs.append("глорихол")
        if not tomorrow_jobs:
            return "без назначения"
        return ", ".join(tomorrow_jobs)

    def _tavern_job_button_caption(job_dict, person, title):
        if job_dict is jobwhoreTommorow:
            assigned = _girl_job_value(person, "jobwhoreTommorow")
        elif job_dict is jobgloryholeTommorow:
            assigned = _girl_job_value(person, "jobgloryholeTommorow")
        else:
            assigned = _tavern_int(_tavern_dict_value(job_dict).get(person, 0), 0)
        prefix = "(x) " if assigned else "( ) "
        return prefix + title

    def _tavern_team_keys():
        ordered = []
        roster = list(AllGirlNames) if isinstance(AllGirlNames, list) else []
        hall_tomorrow = (
            _tavern_dict_value(jobkitchentomorrow),
            _tavern_dict_value(jobcleaningtomorrow),
            _tavern_dict_value(jobwaitresstomorrow),
        )
        special_tomorrow_keys = ("jobwhoreTommorow", "jobgloryholeTommorow")

        def add(person):
            if person and person not in ordered:
                ordered.append(person)

        def in_any(person, mappings):
            for mapping in mappings:
                if _tavern_int(mapping.get(person, 0), 0) != 0:
                    return True
            return False

        def in_any_job(person, job_keys):
            for job_key in job_keys:
                if _girl_job_value(person, job_key):
                    return True
            return False

        for mapping in hall_tomorrow:
            for person, value in mapping.items():
                if _tavern_int(value, 0) != 0:
                    add(person)

        for mapping in hall_tomorrow:
            for person, value in mapping.items():
                if _tavern_int(value, 0) != 0:
                    add(person)

        for mapping in hall_tomorrow:
            for person, value in mapping.items():
                if _tavern_int(value, 0) != 0:
                    add(person)

        for person in roster:
            info = _tavern_person_info(person)
            jobs = getattr(info, "jobs", {}) if info is not None else {}
            if _tavern_int(jobs.get("jobHallAvail", 0), 0) != 0:
                add(person)
                continue
            if _girl_job_value(person, "jobkitchen") or _girl_job_value(person, "jobcleaning") or _girl_job_value(person, "jobwaitress") or in_any(person, hall_tomorrow):
                add(person)
                continue
            if _tavern_int(jobs.get("jobWhoreAvail", 0), 0) != 0 or _tavern_int(jobs.get("jobGloryHoleAvail", 0), 0) != 0 or _girl_job_value(person, "jobwhore") or _girl_job_value(person, "jobgloryhole") or in_any_job(person, special_tomorrow_keys):
                add(person)

        for person in roster:
            if in_any_job(person, special_tomorrow_keys):
                add(person)

        return ordered

    def _tavern_can_assign_gloryhole(person):
        avail = _girl_job_value(person, "jobGloryHoleAvail")
        tomorrow = _girl_job_value(person, "jobgloryholeTommorow")
        busy = 0
        try:
            busy = 1 if glory_hole_busy(person) else 0
        except Exception:
            busy = 0
        return bool(avail and tomorrow == 0 and busy == 0)

    def _tavern_can_assign_whore(person):
        avail = _girl_job_value(person, "jobWhoreAvail")
        tomorrow = _girl_job_value(person, "jobwhoreTommorow")
        return bool(avail and tomorrow == 0)

    def toggle_job_assignment(job_dict, person):
        """Переключает назначение сотрудника в указанном словаре на завтра."""
        job_dict[person] = (job_dict.get(person, 0) + 1) % 2
        _tavern_restart_interaction()

    def _tavern_job_load(job_dict):
        if not isinstance(job_dict, dict):
            return 0
        total = 0
        for _job_key, assigned in job_dict.items():
            if _tavern_int(assigned, 0) != 0:
                total += 1
        return total

    def _tavern_can_toggle_hall_job(job_dict, person, max_slots=3):
        current = _tavern_int(job_dict.get(person, 0), 0)
        if current != 0:
            return True
        return _tavern_job_load(job_dict) < _tavern_int(max_slots, 3)

    def toggle_hall_job_with_limit(job_dict, person, max_slots=3):
        """
        Переключает назначение на завтра по работе в зале с лимитом слотов.
        По умолчанию лимит = 3 человека на позицию.
        """
        if not isinstance(job_dict, dict) or not person:
            return

        current = _tavern_int(job_dict.get(person, 0), 0)
        if current != 0:
            job_dict[person] = 0
            _tavern_restart_interaction()
            return

        if _tavern_job_load(job_dict) >= _tavern_int(max_slots, 3):
            renpy.notify("Лимит: %d/%d на этой позиции." % (_tavern_job_load(job_dict), _tavern_int(max_slots, 3)))
            return

        job_dict[person] = 1
        _tavern_restart_interaction()

    def assign_special_job(person, target):
        """Переназначает сотрудника на особую работу (глорихол или шлюха)."""
        info = _tavern_person_info(person)
        if info is not None and hasattr(info, "set_job_value"):
            if target == "gloryhole":
                info.set_job_value("jobgloryholeTommorow", 1)
                info.set_job_value("jobwhoreTommorow", 0)
            elif target == "whore":
                info.set_job_value("jobgloryholeTommorow", 0)
                info.set_job_value("jobwhoreTommorow", 1)
            _tavern_restart_interaction()
            return

    def BuildTavernReport():
        try:
            ensure_default_tavern_jobs(False)
        except NameError:
            pass

        try:
            update_tavern_service_levels()
        except NameError:
            pass
        except Exception:
            pass

        kitchen_keys = _tavern_job_keys("jobkitchen")
        cleaning_keys = _tavern_job_keys("jobcleaning")
        waitress_keys = _tavern_job_keys("jobwaitress")
        whore_keys = _tavern_job_keys("jobwhore")
        gloryhole_keys = _tavern_job_keys("jobgloryhole")

        try:
            visitors_value = player.tavern_management.visitors
        except NameError:
            visitors_value = 40
        try:
            kitchen_quality_value = tavernkitchen
        except NameError:
            kitchen_quality_value = "пальчики оближешь"
        try:
            clean_quality_value = tavernclean
        except NameError:
            clean_quality_value = "грязновато"
        try:
            service_quality_value = tavernwaitress
        except NameError:
            service_quality_value = "почти не производится"
        try:
            products_value = player.tavern_management.productnum
        except NameError:
            products_value = 20
        try:
            wine_value = player.tavern_management.winenum
        except NameError:
            wine_value = 10
        try:
            gloryhole_level = TavernGloryHole
        except NameError:
            gloryhole_level = 0

        return {
            "visitors": _tavern_int(visitors_value, 40),
            "kitchen_quality": str(kitchen_quality_value),
            "clean_quality": str(clean_quality_value),
            "service_quality": str(service_quality_value),
            "products": DispFrac(products_value),
            "wine": DispFrac(wine_value),
            "kitchen_list": _tavern_join_names(kitchen_keys),
            "cleaning_list": _tavern_join_names(cleaning_keys),
            "waitress_list": _tavern_join_names(waitress_keys),
            "whore_list": _tavern_join_names(whore_keys),
            "gloryhole_list": _tavern_join_names(gloryhole_keys),
            "gloryhole_level": _tavern_int(gloryhole_level, 0),
            "kitchen_slots": _tavern_job_load(jobkitchentomorrow),
            "cleaning_slots": _tavern_job_load(jobcleaningtomorrow),
            "waitress_slots": _tavern_job_load(jobwaitresstomorrow),
            "team_keys": _tavern_team_keys(),
        }
    def _tavern_report_label(report):
        lines = [
            "Трактир \"Дикий Жеребец\":",
            "Вас обычно посещают около %s человек за день." % report["visitors"],
            "Кормят в вашем трактире %s." % report["kitchen_quality"],
            "В вашем трактире %s." % report["clean_quality"],
            "Обслуживание посетителей %s." % report["service_quality"],
            "",
            "На кухне остается %s мешков продуктов." % report["products"],
            "В погребе остается %s бочонков вина." % report["wine"],
            "",
            "На кухне работают: %s" % report["kitchen_list"],
            "За уборку отвечают: %s" % report["cleaning_list"],
            "Посетителям разносят еду и выпивку: %s" % report["waitress_list"],
        ]

        if report["whore_list"] != "никто":
            lines.append("На интимном фронте работают: %s" % report["whore_list"])
        if report["gloryhole_level"] == 2 and report["gloryhole_list"] != "никто":
            lines.append("У глорихола трудится: %s" % report["gloryhole_list"])

        lines.extend([
            "Слоты на завтра: кухня %d/3, уборка %d/3, обслуживание %d/3." % (
                report["kitchen_slots"],
                report["cleaning_slots"],
                report["waitress_slots"],
            ),
            "",
            "У вас трудятся следующие работницы и работники:",
        ])
        for person in report["team_keys"]:
            lines.append("%s: завтра %s." % (_tavern_name(person), _tavern_worker_tomorrow_jobs(person)))
        return "\n".join(lines)

    def _tavern_worker_label(person):
        return "\n".join([
            _tavern_name(person),
            _tavern_worker_summary(person),
            "Завтра: %s." % _tavern_worker_tomorrow_jobs(person),
            "Одежда: %s." % _tavern_worker_dress(person),
        ])

    def _tavern_report_action_items(return_label=""):
        report = BuildTavernReport()
        items = []
        for person in report["team_keys"]:
            items.append(MenuItem("Назначения: " + _tavern_name(person), Call("ShowTavernReportPerson", person, return_label)))
        items.append(MenuItem("Закрыть", Call("HideTavernReport", return_label)))
        return items

    def _tavern_worker_action_items(person, return_label=""):
        items = []

        if renpy.game.script.has_label("ShowGirlCard"):
            items.append(MenuItem("Осмотреть", [Hide("tavern_report_card_overlay"), Call("ShowGirlCard", person, "")]))

        items.append(MenuItem(JobMenuDesc(jobkitchentomorrow.get(person, 0), 1), Call("TavernReportApplyAction", person, "kitchen", return_label)))
        items.append(MenuItem(JobMenuDesc(jobcleaningtomorrow.get(person, 0), 2), Call("TavernReportApplyAction", person, "cleaning", return_label)))
        items.append(MenuItem(JobMenuDesc(jobwaitresstomorrow.get(person, 0), 3), Call("TavernReportApplyAction", person, "waitress", return_label)))

        if _tavern_can_assign_gloryhole(person):
            items.append(MenuItem("Назначить завтра работать у глорихола", Call("TavernReportApplyAction", person, "gloryhole", return_label)))
        if _tavern_can_assign_whore(person):
            items.append(MenuItem("Назначить завтра работать шлюхой", Call("TavernReportApplyAction", person, "whore", return_label)))

        items.append(MenuItem("Общий отчет", Call("ShowTavernReport", return_label)))
        items.append(MenuItem("Закрыть", Call("HideTavernReport", return_label)))
        return items


default TavernReportSelectedPerson = ""


label ShowTavernReport(return_label=""):
    $ TavernReportSelectedPerson = ""
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state("")
        return
    $ current_action_title = "Трактир"
    $ current_action_content = None
    $ current_action_items = _tavern_report_action_items(return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label ShowTavernReportPerson(person="", return_label=""):
    $ TavernReportSelectedPerson = str(person or "")
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state(TavernReportSelectedPerson)
        return
    $ current_action_title = "Назначения: " + _tavern_name(TavernReportSelectedPerson)
    $ current_action_content = None
    $ current_action_items = _tavern_worker_action_items(TavernReportSelectedPerson, return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit(jobkitchentomorrow, _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit(jobcleaningtomorrow, _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit(jobwaitresstomorrow, _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit(jobkitchentomorrow, _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit(jobcleaningtomorrow, _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit(jobwaitresstomorrow, _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label HideTavernReport(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ TavernReportSelectedPerson = ""
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
        return
    hide screen tavern_report_card_overlay
    $ TavernReportSelectedPerson = ""
    if CurrentRoom is not None:
        $ current_action_title = "Действия"
        $ current_action_content = None
        $ current_action_items = build_room_action_items(CurrentRoom)
    if str(return_label or "") == "__hide__":
        return
    if str(return_label or "") != "":
        call expression return_label
    return


default TavernReportSelectedPerson = ""


label ShowTavernReport(return_label=""):
    $ TavernReportSelectedPerson = ""
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state("")
        return
    $ current_action_title = "Трактир"
    $ current_action_content = None
    $ current_action_items = _tavern_report_action_items(return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label ShowTavernReportPerson(person="", return_label=""):
    $ TavernReportSelectedPerson = str(person or "")
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state(TavernReportSelectedPerson)
        return
    $ current_action_title = "Назначения: " + _tavern_name(TavernReportSelectedPerson)
    $ current_action_content = None
    $ current_action_items = _tavern_worker_action_items(TavernReportSelectedPerson, return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit(jobkitchentomorrow, _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit(jobcleaningtomorrow, _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit(jobwaitresstomorrow, _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit(jobkitchentomorrow, _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit(jobcleaningtomorrow, _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit(jobwaitresstomorrow, _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label HideTavernReport(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ TavernReportSelectedPerson = ""
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
        return
    hide screen tavern_report_card_overlay
    $ TavernReportSelectedPerson = ""
    if CurrentRoom is not None:
        $ current_action_title = "Действия"
        $ current_action_content = None
        $ current_action_items = build_room_action_items(CurrentRoom)
    if str(return_label or "") == "__hide__":
        return
    if str(return_label or "") != "":
        call expression return_label
    return


default TavernReportSelectedPerson = ""


label ShowTavernReport(return_label=""):
    $ TavernReportSelectedPerson = ""
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state("")
        return
    $ current_action_title = "Трактир"
    $ current_action_content = None
    $ current_action_items = _tavern_report_action_items(return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label ShowTavernReportPerson(person="", return_label=""):
    $ TavernReportSelectedPerson = str(person or "")
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state(TavernReportSelectedPerson)
        return
    $ current_action_title = "Назначения: " + _tavern_name(TavernReportSelectedPerson)
    $ current_action_content = None
    $ current_action_items = _tavern_worker_action_items(TavernReportSelectedPerson, return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit(jobkitchentomorrow, _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit(jobcleaningtomorrow, _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit(jobwaitresstomorrow, _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit(jobkitchentomorrow, _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit(jobcleaningtomorrow, _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit(jobwaitresstomorrow, _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label HideTavernReport(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ TavernReportSelectedPerson = ""
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
        return
    hide screen tavern_report_card_overlay
    $ TavernReportSelectedPerson = ""
    if CurrentRoom is not None:
        $ current_action_title = "Действия"
        $ current_action_content = None
        $ current_action_items = build_room_action_items(CurrentRoom)
    if str(return_label or "") == "__hide__":
        return
    if str(return_label or "") != "":
        call expression return_label
    return


label ShowTavernReport(return_label=""):
    $ main_ui_runtime.tavern_report_person = ""
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state("")
        return
    $ current_action_title = "Трактир"
    $ current_action_content = None
    $ current_action_items = _tavern_report_action_items(return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label ShowTavernReportPerson(person="", return_label=""):
    $ main_ui_runtime.tavern_report_person = str(person or "")
    if str(return_label or "") == "__main_ui__":
        $ show_tavern_report_main_ui_state(main_ui_runtime.tavern_report_person)
        return
    $ current_action_title = "Назначения: " + _tavern_name(main_ui_runtime.tavern_report_person)
    $ current_action_content = None
    $ current_action_items = _tavern_worker_action_items(main_ui_runtime.tavern_report_person, return_label)
    show screen tavern_report_card_overlay(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label TavernReportApplyAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReportPerson(_tavern_person, return_label)
    return


label TavernReportApplyOverviewAction(person="", action_code="", return_label=""):
    $ _tavern_person = str(person or "")
    $ _tavern_action = str(action_code or "")
    if _tavern_action == "kitchen":
        $ toggle_hall_job_with_limit("jobkitchentomorrow", _tavern_person, 2)
    elif _tavern_action == "cleaning":
        $ toggle_hall_job_with_limit("jobcleaningtomorrow", _tavern_person, 2)
    elif _tavern_action == "waitress":
        $ toggle_hall_job_with_limit("jobwaitresstomorrow", _tavern_person, 2)
    elif _tavern_action == "gloryhole":
        $ assign_special_job(_tavern_person, "gloryhole")
    elif _tavern_action == "whore":
        $ assign_special_job(_tavern_person, "whore")
    call ShowTavernReport(return_label)
    return


label HideTavernReport(return_label=""):
    if str(return_label or "") == "__main_ui__":
        $ main_ui_runtime.tavern_report_person = ""
        $ _room_label = str(CurLoc or getattr(CurrentRoom, "code_name", "") or "").strip()
        if _room_label:
            jump expression _room_label
        return
    hide screen tavern_report_card_overlay
    $ main_ui_runtime.tavern_report_person = ""
    if CurrentRoom is not None:
        $ current_action_title = "Действия"
        $ current_action_content = None
        $ current_action_items = build_room_action_items(CurrentRoom)
    if str(return_label or "") == "__hide__":
        return
    if str(return_label or "") != "":
        call expression return_label
    return
