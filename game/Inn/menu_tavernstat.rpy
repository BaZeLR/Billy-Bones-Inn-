# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

define TAVERN_HALL_JOB_CAPACITY = 3

init python:
    import renpy.exports as renpy_module

    def _tavern_dict_value(value):
        return value if isinstance(value, dict) else {}

    def _tavern_restart_interaction():
        fn = getattr(renpy_module, "restart_interaction", None)
        if callable(fn):
            fn()

    def show_tavern_report_main_ui_state(person=""):
        if str(main_ui_runtime.mode or "") != "tavern" and main_ui_runtime.tavern_report_origin is None:
            main_ui_runtime.tavern_report_origin = main_ui_context_snapshot()
        main_ui_runtime.tavern_report_person = str(person or "")
        main_ui_runtime.mode = "tavern"
        main_ui_runtime.action_content = None
        if main_ui_runtime.tavern_report_person:
            main_ui_runtime.action_title = "Назначения: " + _tavern_name(main_ui_runtime.tavern_report_person)
            main_ui_runtime.action_items = _tavern_worker_action_items(main_ui_runtime.tavern_report_person, "__main_ui__")
        else:
            main_ui_runtime.action_title = "Трактир"
            main_ui_runtime.action_items = _tavern_report_action_items("__main_ui__")
        _tavern_restart_interaction()

    def hide_tavern_report_main_ui_state():
        origin = main_ui_runtime.tavern_report_origin
        main_ui_runtime.tavern_report_origin = None
        main_ui_runtime.tavern_report_person = ""
        if origin is not None:
            main_ui_restore_context(origin)
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
        display = people_display_name(person)
        if str(display or "").strip():
            return str(display)
        return str(person).capitalize()

    def _tavern_person_info(person):
        return people.get_info(str(person or "").strip().lower())

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
        return "%s:%s" % (str(person or "").strip().lower(), current_game_day() if day_marker is None else int(day_marker or 0))

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
            if int(calendar_v2.week or 0) != 7 and procedural_randint(1, 100, "household_morning_issue_%s_%s" % (key, current_game_day())) <= 15:
                issue_code = "sick" if procedural_randint(1, 2, "household_morning_kind_%s_%s" % (key, current_game_day())) == 1 else "sleepy"
                if issue_code == "sleepy" and _household_sleep_indecent_possible(key) and procedural_randint(1, 100, "household_morning_indecent_%s_%s" % (key, current_game_day())) <= 45:
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
        slot = _tavern_int(calendar_v2.time_slot() if time_value is None else time_value, 0)
        hour_num = _tavern_int(calendar_v2.hour if hour_value is None else hour_value, 8)
        if key not in ("sandra", "melissa", "amanda"):
            return ""
        if _tavern_int(calendar_v2.week, 1) == 7 or slot >= 4 or hour_num >= 12:
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
        min_day = max(0, current_game_day() - max(1, int(day_span or 2)) + 1)
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
            visible_ids = set([str(row or "").strip().lower() for row in list(people.ids_at("TavernKitchen") or [])])
        except Exception:
            visible_ids = set()
            for npc_id in ("sandra", "melissa", "amanda", "becky"):
                if str(people.location(npc_id) or "") == "TavernKitchen":
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
            if str(people.location(npc_id) or "") == "TavernKitchen":
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
            if threads["melissaBatProblem"].num >= 7 and threads["melissaBatProblem"].num < 8:
                repair_day = people_to_int(Melissa.roof_repair_complete_day, -1)
                if repair_day > current_game_day():
                    days_left = repair_day - current_game_day()
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
        keys = [name for name in ("sandra", "melissa", "amanda") if str(people.location(name) or "") == room_key]
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
        dressdesc_map = _tavern_dict_value(DressDesc)
        fulldesc_map = _tavern_dict_value(FullDressDesc)
        part_desc_map = _tavern_dict_value(DressPartDesc)

        info = people.get_info(person)
        dress_code = str(info.current_dress() if info is not None and hasattr(info, "current_dress") else "")
        if dress_code and dress_code in dressdesc_map:
            return str(dressdesc_map[dress_code])

        top_code = str(info.clothing_layer("top") if info is not None and hasattr(info, "clothing_layer") else "")
        bottom_code = str(info.clothing_layer("bottom") if info is not None and hasattr(info, "clothing_layer") else "")
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

    def _tavern_worker_current_jobs(person):
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
        return ", ".join(current_jobs) if current_jobs else "без смены"

    def _tavern_worker_summary(person):
        info = _tavern_person_info(person)
        skills = getattr(info, "skills", {}) if info is not None else {}
        cooking_value = _tavern_int(skills.get("cooking", 0), 0)
        cleaning_value = _tavern_int(skills.get("cleaning", 0), 0)
        waitress_value = _tavern_int(skills.get("waitress", 0), 0)
        friends_value = _tavern_person_relation(person)

        return "Навыки: кухня %d / уборка %d / зал %d. Дружба: %d. Сейчас: %s." % (
            cooking_value,
            cleaning_value,
            waitress_value,
            friends_value,
            _tavern_worker_current_jobs(person),
        )

    def _tavern_worker_tomorrow_jobs(person):
        tomorrow_jobs = []
        if _girl_job_value(person, "jobkitchentomorrow"):
            tomorrow_jobs.append("кухня")
        if _girl_job_value(person, "jobcleaningtomorrow"):
            tomorrow_jobs.append("уборка")
        if _girl_job_value(person, "jobwaitresstomorrow"):
            tomorrow_jobs.append("зал")
        if _girl_job_value(person, "jobwhoreTommorow"):
            tomorrow_jobs.append("интим")
        if _girl_job_value(person, "jobgloryholeTommorow"):
            tomorrow_jobs.append("глорихол")
        if not tomorrow_jobs:
            return "без назначения"
        return ", ".join(tomorrow_jobs)

    def _tavern_job_button_caption(job_key, person, title):
        assigned = _girl_job_value(person, job_key)
        prefix = "(x) " if assigned else "( ) "
        return prefix + title

    def _tavern_team_keys():
        ordered = []
        roster = list(AllGirlNames) if isinstance(AllGirlNames, list) else []
        hall_tomorrow = ("jobkitchentomorrow", "jobcleaningtomorrow", "jobwaitresstomorrow")
        special_tomorrow_keys = ("jobwhoreTommorow", "jobgloryholeTommorow")

        def add(person):
            if person and person not in ordered:
                ordered.append(person)

        def in_any(person, job_keys):
            for job_key in job_keys:
                if _girl_job_value(person, job_key):
                    return True
            return False

        def in_any_job(person, job_keys):
            for job_key in job_keys:
                if _girl_job_value(person, job_key):
                    return True
            return False

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

    def toggle_job_assignment(job_key, person):
        info = _tavern_person_info(person)
        if info is None:
            return
        info.set_job_value(job_key, (people_to_int(info.job_value(job_key, 0), 0) + 1) % 2)
        _tavern_restart_interaction()

    def _tavern_job_load(job_key):
        return sum(1 for person in list(AllGirlNames or []) if _girl_job_value(person, job_key))

    def _tavern_can_toggle_hall_job(job_key, person):
        current = _girl_job_value(person, job_key)
        if current != 0:
            return True
        return _tavern_job_load(job_key) < TAVERN_HALL_JOB_CAPACITY

    def toggle_hall_job_with_limit(job_key, person):
        info = _tavern_person_info(person)
        if info is None or not person:
            return

        current = _girl_job_value(person, job_key)
        if current != 0:
            info.set_job_value(job_key, 0)
            _tavern_restart_interaction()
            return

        if _tavern_job_load(job_key) >= TAVERN_HALL_JOB_CAPACITY:
            renpy.notify("Лимит: %d/%d на этой позиции." % (_tavern_job_load(job_key), TAVERN_HALL_JOB_CAPACITY))
            return

        info.set_job_value(job_key, 1)
        _tavern_restart_interaction()

    def assign_special_job(person, target):
        """Переназначает сотрудника на особую работу (глорихол или шлюха)."""
        info = _tavern_person_info(person)
        if info is not None:
            if target == "gloryhole":
                info.set_job_value("jobgloryholeTommorow", 1)
                info.set_job_value("jobwhoreTommorow", 0)
            elif target == "whore":
                info.set_job_value("jobgloryholeTommorow", 0)
                info.set_job_value("jobwhoreTommorow", 1)
            _tavern_restart_interaction()
            return

    def BuildTavernReport():
        update_tavern_service_levels()

        kitchen_keys = _tavern_job_keys("jobkitchen")
        cleaning_keys = _tavern_job_keys("jobcleaning")
        waitress_keys = _tavern_job_keys("jobwaitress")
        whore_keys = _tavern_job_keys("jobwhore")
        gloryhole_keys = _tavern_job_keys("jobgloryhole")

        visitors_value = player.tavern_management.visitors
        kitchen_quality_value = player.tavern_management.service.kitchen_quality
        clean_quality_value = player.tavern_management.service.cleanliness_quality
        service_quality_value = player.tavern_management.service.waitress_quality
        products_value = player.tavern_management.productnum
        wine_value = player.tavern_management.winenum
        gloryhole_level = player.tavern_management.glory_hole

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
            "kitchen_slots": _tavern_job_load("jobkitchentomorrow"),
            "cleaning_slots": _tavern_job_load("jobcleaningtomorrow"),
            "waitress_slots": _tavern_job_load("jobwaitresstomorrow"),
            "hall_job_capacity": TAVERN_HALL_JOB_CAPACITY,
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
            "Слоты на завтра: кухня %d/%d, уборка %d/%d, обслуживание %d/%d." % (
                report["kitchen_slots"],
                report["hall_job_capacity"],
                report["cleaning_slots"],
                report["hall_job_capacity"],
                report["waitress_slots"],
                report["hall_job_capacity"],
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
        items.append(MenuItem("Назад", Call("HideTavernReport", return_label)))
        return items

    def _tavern_worker_action_items(person, return_label=""):
        items = []

        if renpy.game.script.has_label("ShowGirlCard"):
            items.append(MenuItem("Осмотреть", Call("ShowGirlCard", person)))

        items.append(MenuItem(JobMenuDesc(_girl_job_value(person, "jobkitchentomorrow"), 1), [Function(toggle_hall_job_with_limit, "jobkitchentomorrow", person), Function(show_tavern_report_main_ui_state, person)]))
        items.append(MenuItem(JobMenuDesc(_girl_job_value(person, "jobcleaningtomorrow"), 2), [Function(toggle_hall_job_with_limit, "jobcleaningtomorrow", person), Function(show_tavern_report_main_ui_state, person)]))
        items.append(MenuItem(JobMenuDesc(_girl_job_value(person, "jobwaitresstomorrow"), 3), [Function(toggle_hall_job_with_limit, "jobwaitresstomorrow", person), Function(show_tavern_report_main_ui_state, person)]))

        if _tavern_can_assign_gloryhole(person):
            items.append(MenuItem("Назначить завтра работать у глорихола", [Function(assign_special_job, person, "gloryhole"), Function(show_tavern_report_main_ui_state, person)]))
        if _tavern_can_assign_whore(person):
            items.append(MenuItem("Назначить завтра работать шлюхой", [Function(assign_special_job, person, "whore"), Function(show_tavern_report_main_ui_state, person)]))

        items.append(MenuItem("Общий отчет", Call("ShowTavernReport", return_label)))
        items.append(MenuItem("Назад", Call("HideTavernReport", return_label)))
        return items


label ShowTavernReport(return_label=""):
    $ show_tavern_report_main_ui_state("")
    return


label ShowTavernReportPerson(person="", return_label=""):
    $ show_tavern_report_main_ui_state(person)
    return


label HideTavernReport(return_label=""):
    $ hide_tavern_report_main_ui_state()
    return
