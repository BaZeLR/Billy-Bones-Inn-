default HouseholdMorningState = {}

init python:
    import renpy.exports as renpy_module
    import random as tavern_random

    def _tavern_dict_value(value):
        return value if isinstance(value, dict) else {}

    def _tavern_restart_interaction():
        fn = getattr(renpy_module, "restart_interaction", None)
        if callable(fn):
            fn()

    def show_tavern_report_main_ui_state(person=""):
        store = renpy.store
        store.TavernReportSelectedPerson = str(person or "")
        store.UI_mode = "tavern"
        store.current_action_content = None
        if store.TavernReportSelectedPerson:
            store.current_action_title = "Назначения: " + _tavern_name(store.TavernReportSelectedPerson)
            store.current_action_items = _tavern_worker_action_items(store.TavernReportSelectedPerson, "__main_ui__")
        else:
            store.current_action_title = "Трактир"
            store.current_action_items = _tavern_report_action_items("__main_ui__")
        _tavern_restart_interaction()

    def _tavern_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

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
        real_names = _tavern_dict_value(RealName)
        if person in real_names and str(real_names[person]).strip():
            return str(real_names[person])
        return str(person).capitalize()

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
            return int(sluttiness.get("amanda", 0) or 0) >= 30 or int(AmandaVar.get("suckyou", 0) or 0) > 0 or int(AmandaVar.get("fuckyou", 0) or 0) > 0
        if key == "melissa":
            return int(sluttiness.get("melissa", 0) or 0) >= 18 or int(Friends.get("melissa", 0) or 0) >= 10
        if key == "sandra":
            return int(sluttiness.get("sandra", 0) or 0) >= 20 or int(Friends.get("sandra", 0) or 0) >= 10
        return False

    def _ensure_household_morning_state(person="", day_marker=None):
        global HouseholdMorningState

        key = str(person or "").strip().lower()
        if key not in ("sandra", "melissa", "amanda"):
            return {"issue": "", "resolved": 1, "indecent": 0}
        if not isinstance(HouseholdMorningState, dict):
            HouseholdMorningState = {}

        state_key = _household_morning_state_key(key, day_marker)
        entry = HouseholdMorningState.get(state_key)
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
            HouseholdMorningState[state_key] = entry
        return HouseholdMorningState.get(state_key, {"issue": "", "resolved": 1, "indecent": 0})

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
        global HouseholdMorningState

        key = str(person or "").strip().lower()
        if key not in ("sandra", "melissa", "amanda"):
            return 0
        entry = dict(_ensure_household_morning_state(key) or {})
        entry["resolved"] = 1
        HouseholdMorningState[_household_morning_state_key(key)] = entry
        return 1

    def household_needs_reconcile(person=""):
        key = str(person or "").strip().lower()
        return key in ("sandra", "melissa", "amanda") and int(Friends.get(key, 0) or 0) < 5 and int(Talked.get(key, 0) or 0) < 3

    def player_recent_sex_count(day_span=2):
        min_day = max(0, int(dayspassed or 0) - max(1, int(day_span or 2)) + 1)
        total = 0
        seen_rows = set()
        history_repo = sex_history_by_girl if isinstance(sex_history_by_girl, dict) else {}
        for girl_rows in list(history_repo.values()):
            for row in list(girl_rows or []):
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
                    str(row.get("GirlName", "") or ""),
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
        attendees = []
        for npc_id in ("sandra", "melissa", "amanda"):
            if household_morning_issue_type(npc_id) != "":
                continue
            if household_needs_reconcile(npc_id):
                continue
            attendees.append(npc_id)
        if int(BeckyKitchenVisitActive or 0) == 1:
            attendees.append("becky")
        return attendees

    def household_breakfast_absence_lines():
        lines = []
        for npc_id in ("sandra", "melissa", "amanda"):
            npc_name = _tavern_name(npc_id)
            issue_code = household_morning_issue_type(npc_id)
            if issue_code == "sick":
                lines.append("%s с утра расклеилась и осталась в своей комнате. Без лечебного зелья сегодня ее к столу не вытащить." % npc_name)
            elif issue_code == "sleepy":
                lines.append("%s все еще отсыпается у себя и пока не явилась к общему столу." % npc_name)
            elif household_needs_reconcile(npc_id):
                lines.append("%s держится в стороне и не спешит садиться с вами за один стол, пока вы не сгладите напряжение между вами." % npc_name)
        return lines

    def household_room_issue_notice_text(person=""):
        key = str(person or "").strip().lower()
        issue_code = household_morning_issue_type(key)
        if issue_code == "sick":
            return "%s выглядит нездорово и явно не собирается сегодня вставать без посторонней помощи." % _tavern_name(key)
        if issue_code == "sleepy":
            return "%s все еще валяется в постели и явно проспала общий подъем." % _tavern_name(key)
        return ""

    def _tavern_household_seed(person, hour_value=None, day_marker=None, weekday=None):
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
        keys = [name for name in ("sandra", "melissa", "amanda") if _tavern_is_in_room(name, room_key)]
        return _tavern_join_names(keys)

    def _tavern_effective_location(person, time_value=None):
        key = str(person or "").strip().lower()
        if not key:
            return ""

        current_locations = _tavern_dict_value(CurrentLoc)
        explicit_loc = str(current_locations.get(key, "") or "")
        tavern_rooms = {
            "TavernMain",
            "TavernKitchen",
            "TavernSandraRoom",
            "TavernMelissaRoom",
            "TavernAmandaRoom",
        }

        if explicit_loc and explicit_loc not in tavern_rooms:
            return explicit_loc

        slot = _tavern_int(time if time_value is None else time_value, 0)
        sunday_loc = _tavern_household_sunday_location(key, slot)
        if sunday_loc:
            return sunday_loc

        friday_evening_loc = _tavern_household_friday_evening_location(key, slot)
        if friday_evening_loc:
            return friday_evening_loc

        morning_issue = household_morning_issue_type(key, slot, hour)
        if morning_issue in ("sick", "sleepy"):
            return _tavern_private_room(key)

        preopening_loc = _tavern_household_preopening_location(key, slot)
        if preopening_loc:
            return preopening_loc

        private_room = _tavern_private_room(key)
        if private_room and slot >= 4:
            return private_room

        if key in ("sandra", "melissa", "amanda"):
            if _tavern_int(_tavern_dict_value(jobkitchen).get(key, 0), 0):
                return "TavernKitchen"
            if _tavern_int(_tavern_dict_value(jobcleaning).get(key, 0), 0):
                return "TavernMain"
            if _tavern_int(_tavern_dict_value(jobwaitress).get(key, 0), 0):
                return "TavernMain"
            if private_room:
                return private_room

        return explicit_loc

    def _tavern_is_in_room(person, room_code, time_value=None):
        return str(_tavern_effective_location(person, time_value) or "") == str(room_code or "")

    def _tavern_job_room(job_type):
        return {
            "jobkitchen": "TavernKitchen",
            "jobcleaning": "TavernMain",
            "jobwaitress": "TavernMain",
        }.get(str(job_type or ""), "")

    def _tavern_job_keys(job_type, room_code=None):
        mapping = {
            "jobkitchen": _tavern_dict_value(jobkitchen),
            "jobcleaning": _tavern_dict_value(jobcleaning),
            "jobwaitress": _tavern_dict_value(jobwaitress),
            "jobwhore": _tavern_dict_value(jobwhore),
            "jobgloryhole": _tavern_dict_value(jobgloryhole),
        }
        source = mapping.get(job_type, {})
        keys = [name for name, assigned in source.items() if _tavern_int(assigned, 0) != 0]
        target_room = str(room_code or _tavern_job_room(job_type) or "")
        if not target_room:
            return keys
        return [name for name in keys if _tavern_is_in_room(name, target_room)]

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
        cooking_value = _tavern_int(_tavern_get_stat(cooking, person, 0), 0)
        cleaning_value = _tavern_int(_tavern_get_stat(cleaning, person, 0), 0)
        waitress_value = _tavern_int(_tavern_get_stat(waitress, person, 0), 0)
        friends_value = _tavern_int(_tavern_get_stat(Friends, person, 0), 0)

        current_jobs = []
        if _tavern_int(_tavern_dict_value(jobkitchen).get(person, 0), 0):
            current_jobs.append("кухня")
        if _tavern_int(_tavern_dict_value(jobcleaning).get(person, 0), 0):
            current_jobs.append("уборка")
        if _tavern_int(_tavern_dict_value(jobwaitress).get(person, 0), 0):
            current_jobs.append("зал")
        if _tavern_int(_tavern_dict_value(jobwhore).get(person, 0), 0):
            current_jobs.append("интим")
        if _tavern_int(_tavern_dict_value(jobgloryhole).get(person, 0), 0):
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
        if _tavern_int(_tavern_dict_value(jobwhoreTommorow).get(person, 0), 0):
            tomorrow_jobs.append("интим")
        if _tavern_int(_tavern_dict_value(jobgloryholeTommorow).get(person, 0), 0):
            tomorrow_jobs.append("глорихол")
        if not tomorrow_jobs:
            return "без назначения"
        return ", ".join(tomorrow_jobs)

    def _tavern_job_button_caption(job_dict, person, title):
        assigned = _tavern_int(_tavern_dict_value(job_dict).get(person, 0), 0)
        prefix = "(x) " if assigned else "( ) "
        return prefix + title

    def _tavern_team_keys():
        ordered = []
        roster = list(AllGirlNames) if isinstance(AllGirlNames, list) else []
        hall_avail = _tavern_dict_value(jobHallAvail)
        hall_current = (
            _tavern_dict_value(jobkitchen),
            _tavern_dict_value(jobcleaning),
            _tavern_dict_value(jobwaitress),
        )
        hall_tomorrow = (
            _tavern_dict_value(jobkitchentomorrow),
            _tavern_dict_value(jobcleaningtomorrow),
            _tavern_dict_value(jobwaitresstomorrow),
        )
        special_avail = (
            _tavern_dict_value(jobWhoreAvail),
            _tavern_dict_value(jobGloryHoleAvail),
        )
        special_current = (
            _tavern_dict_value(jobwhore),
            _tavern_dict_value(jobgloryhole),
        )
        special_tomorrow = (
            _tavern_dict_value(jobwhoreTommorow),
            _tavern_dict_value(jobgloryholeTommorow),
        )

        def add(person):
            if person and person not in ordered:
                ordered.append(person)

        def in_any(person, mappings):
            for mapping in mappings:
                if _tavern_int(mapping.get(person, 0), 0) != 0:
                    return True
            return False

        for person in roster:
            if _tavern_int(hall_avail.get(person, 0), 0) != 0:
                add(person)
                continue
            if in_any(person, hall_current) or in_any(person, hall_tomorrow):
                add(person)
                continue
            if in_any(person, special_avail) or in_any(person, special_current) or in_any(person, special_tomorrow):
                add(person)

        for mapping in hall_current + hall_tomorrow + special_avail + special_current + special_tomorrow:
            for person, value in mapping.items():
                if _tavern_int(value, 0) != 0:
                    add(person)

        return ordered

    def _tavern_can_assign_gloryhole(person):
        avail = _tavern_int(_tavern_dict_value(jobGloryHoleAvail).get(person, 0), 0)
        tomorrow = _tavern_int(_tavern_dict_value(jobgloryholeTommorow).get(person, 0), 0)
        busy = 0
        if renpy_module.has_label("GloryHoleBusy"):
            try:
                busy = _tavern_int(renpy_module.call("GloryHoleBusy", person), 0)
            except Exception:
                busy = 0
        return bool(avail and tomorrow == 0 and busy == 0)

    def _tavern_can_assign_whore(person):
        avail = _tavern_int(_tavern_dict_value(jobWhoreAvail).get(person, 0), 0)
        tomorrow = _tavern_int(_tavern_dict_value(jobwhoreTommorow).get(person, 0), 0)
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

    def _tavern_can_toggle_hall_job(job_dict, person, max_slots=2):
        current = _tavern_int(job_dict.get(person, 0), 0)
        if current != 0:
            return True
        return _tavern_job_load(job_dict) < _tavern_int(max_slots, 2)

    def toggle_hall_job_with_limit(job_dict, person, max_slots=2):
        """
        Переключает назначение на завтра по работе в зале с лимитом слотов.
        По умолчанию лимит = 2 человека на позицию.
        """
        if not isinstance(job_dict, dict) or not person:
            return

        current = _tavern_int(job_dict.get(person, 0), 0)
        if current != 0:
            job_dict[person] = 0
            _tavern_restart_interaction()
            return

        if _tavern_job_load(job_dict) >= _tavern_int(max_slots, 2):
            renpy.notify("Лимит: %d/%d на этой позиции." % (_tavern_job_load(job_dict), _tavern_int(max_slots, 2)))
            return

        job_dict[person] = 1
        _tavern_restart_interaction()

    def assign_special_job(person, target):
        """Переназначает сотрудника на особую работу (глорихол или шлюха)."""
        if target == "gloryhole":
            jobgloryholeTommorow[person] = 1
            jobwhoreTommorow[person] = 0
        elif target == "whore":
            jobgloryholeTommorow[person] = 0
            jobwhoreTommorow[person] = 1
        _tavern_restart_interaction()

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
            visitors_value = tavernvisitors
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
            products_value = productnum
        except NameError:
            products_value = 20
        try:
            wine_value = winenum
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
            "Слоты на завтра: кухня %d/2, уборка %d/2, обслуживание %d/2." % (
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

        if renpy_module.has_label("ShowGirlCard"):
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
        $ main_ui_restore_room_scene_state()
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


screen tavern_report_card_overlay(return_label=""):
    zorder 120

    $ _report = BuildTavernReport()
    $ _person = str(TavernReportSelectedPerson or "")
    $ _title = _tavern_name(_person) if _person else "ТРАКТИР"
    $ _body = _tavern_worker_label(_person) if _person else _tavern_report_label(_report)
    $ _textbox_h = int(getattr(gui, "textbox_height", 278))
    $ _usable_h = max(360, int(config.screen_height) - _textbox_h)
    $ _left_w = int((config.screen_width - 36) * 0.72)
    $ _left_h = _usable_h - 24

    fixed:
        xpos 12
        ypos 12
        xsize _left_w
        ysize _left_h

        add im.Scale("images/rpg_message_bg.png", _left_w, _left_h)

        vbox:
            xpos 28
            ypos 24
            xmaximum _left_w - 56
            spacing 10

            text _title.upper() size 30 color "#000000" italic True xalign 0.5
            text _body size 18 color "#000000"

            if not _person and _report["team_keys"]:
                null height 4
                text "Завтрашняя смена" size 22 color "#000000" italic True

                vbox:
                    spacing 6

                    for _worker in _report["team_keys"]:
                        hbox:
                            spacing 8
                            xfill True

                            textbutton _tavern_name(_worker):
                                xminimum 180
                                text_size 20
                                text_bold True
                                text_color "#f7f0de"
                                background "#3a2214"
                                hover_background "#5a3420"
                                action Call("ShowTavernReportPerson", _worker, return_label)

                            textbutton _tavern_job_button_caption(jobkitchentomorrow, _worker, "Кухня"):
                                xminimum 120
                                text_size 18
                                text_bold True
                                text_color "#f7f0de"
                                background "#3a2214"
                                hover_background "#5a3420"
                                action Call("TavernReportApplyOverviewAction", _worker, "kitchen", return_label)

                            textbutton _tavern_job_button_caption(jobcleaningtomorrow, _worker, "Уборка"):
                                xminimum 130
                                text_size 18
                                text_bold True
                                text_color "#f7f0de"
                                background "#3a2214"
                                hover_background "#5a3420"
                                action Call("TavernReportApplyOverviewAction", _worker, "cleaning", return_label)

                            textbutton _tavern_job_button_caption(jobwaitresstomorrow, _worker, "Зал"):
                                xminimum 100
                                text_size 18
                                text_bold True
                                text_color "#f7f0de"
                                background "#3a2214"
                                hover_background "#5a3420"
                                action Call("TavernReportApplyOverviewAction", _worker, "waitress", return_label)

label menu_tavernstat:
    call ShowTavernReport("")
    return

label menu_tavernstat_overview:
    call ShowTavernReport("")
    return

label menu_tavernstat_person(person):
    call ShowTavernReportPerson(person, "")
    return
