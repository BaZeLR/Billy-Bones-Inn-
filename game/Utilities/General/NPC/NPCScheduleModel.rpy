# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default NPCSchedules = {}
default NPCDailyScheduleTemplates = {}
default NPCDailySchedulePlans = {}
default NPCDailySchedulePlanDay = -1
default NPCDailyScheduleMonthlyCounters = {}
default NPCIntervalSchedules = {}
default NPCIntervalScheduleLoaded = False
default NPCIntervalScheduleLoadErrors = {}

init python:
    import json

    def _npc_schedule_store():
        global NPCSchedules
        try:
            schedules = NPCSchedules
        except NameError:
            schedules = {}
            NPCSchedules = schedules
        if not isinstance(schedules, dict):
            schedules = {}
            NPCSchedules = schedules
        return schedules

    def _npc_daily_schedule_template_store():
        global NPCDailyScheduleTemplates
        try:
            templates = NPCDailyScheduleTemplates
        except NameError:
            templates = {}
            NPCDailyScheduleTemplates = templates
        if not isinstance(templates, dict):
            templates = {}
            NPCDailyScheduleTemplates = templates
        return templates

    def _npc_daily_schedule_plan_store():
        global NPCDailySchedulePlans
        try:
            plans = NPCDailySchedulePlans
        except NameError:
            plans = {}
            NPCDailySchedulePlans = plans
        if not isinstance(plans, dict):
            plans = {}
            NPCDailySchedulePlans = plans
        return plans

    def _npc_daily_schedule_counter_store():
        global NPCDailyScheduleMonthlyCounters
        try:
            counters = NPCDailyScheduleMonthlyCounters
        except NameError:
            counters = {}
            NPCDailyScheduleMonthlyCounters = counters
        if not isinstance(counters, dict):
            counters = {}
            NPCDailyScheduleMonthlyCounters = counters
        return counters

    def _npc_interval_schedule_store():
        global NPCIntervalSchedules
        try:
            schedules = NPCIntervalSchedules
        except NameError:
            schedules = {}
            NPCIntervalSchedules = schedules
        if not isinstance(schedules, dict):
            schedules = {}
            NPCIntervalSchedules = schedules
        return schedules

    def npc_schedule_time_to_minutes(value, default=0):
        text = str(value or "").strip()
        if ":" not in text:
            try:
                return max(0, min(1439, int(text)))
            except Exception:
                return int(default or 0)
        try:
            h_text, m_text = text.split(":", 1)
            hour_value = max(0, min(23, int(h_text or 0)))
            minute_value = max(0, min(59, int(m_text or 0)))
            return hour_value * 60 + minute_value
        except Exception:
            return int(default or 0)

    def npc_schedule_minutes_to_time(value):
        minute_value = int(value or 0) % 1440
        return "%02d:%02d" % (minute_value // 60, minute_value % 60)

    def npc_interval_condition_from_json(row):
        data = dict(row or {})
        condition = data.get("condition", None)
        try:
            condition_data = dict(condition or {})
        except Exception:
            condition_data = {}
        if condition_data:
            rule_kind = str(condition_data.get("rule", condition_data.get("__schedule_rule__", "")) or "").strip()
            if rule_kind:
                payload = dict(condition_data)
                payload.pop("rule", None)
                payload.pop("__schedule_rule__", None)
                return npc_schedule_rule(rule_kind, **payload)
        return condition

    class NPCIntervalScheduleEntry(object):
        def __init__(
            self,
            npc_id="",
            location="",
            location_choices=None,
            weekdays=None,
            start="00:00",
            end="23:59",
            awake=True,
            talkable=True,
            condition=None,
            priority=600,
            label="",
            source="json",
        ):
            self.npc_id = str(npc_id or "").strip()
            self.location = str(location or "").strip()
            self.location_choices = list(location_choices or [])
            self.weekdays = list(weekdays or [])
            self.start_minute = npc_schedule_time_to_minutes(start, 0)
            self.end_minute = npc_schedule_time_to_minutes(end, 1439)
            self.awake = bool(awake)
            self.talkable = bool(talkable)
            self.condition = condition
            self.priority = int(priority or 600)
            self.label = str(label or "").strip()
            self.source = str(source or "json")

        def selected_location(self):
            choices = []
            for row in list(self.location_choices or []):
                data = dict(row or {})
                loc = str(data.get("location", "") or "").strip()
                if not loc:
                    continue
                try:
                    probability = float(data.get("probability", data.get("weight", 1.0)) or 0.0)
                except Exception:
                    probability = 0.0
                if probability > 0:
                    choices.append({"location": loc, "probability": probability})

            if not choices:
                return str(self.location or "")

            total_probability = sum([max(0.0, float(row.get("probability", 0.0) or 0.0)) for row in choices])
            if total_probability <= 0:
                return ""

            scale = 10000
            if total_probability <= 1.000001:
                roll = procedural_randint(1, scale, "npc_interval_%s_%s_%s_%s" % (self.npc_id, self.label, dayspassed, self.start_minute))
                cursor = 0
                for row in choices:
                    cursor += int(round(max(0.0, float(row.get("probability", 0.0) or 0.0)) * scale))
                    if roll <= cursor:
                        return str(row.get("location", "") or "")
                return ""

            roll = procedural_randint(1, int(round(total_probability * scale)), "npc_interval_%s_%s_%s_%s" % (self.npc_id, self.label, dayspassed, self.start_minute))
            cursor = 0
            for row in choices:
                cursor += int(round(max(0.0, float(row.get("probability", 0.0) or 0.0)) * scale))
                if roll <= cursor:
                    return str(row.get("location", "") or "")
            return str(choices[-1].get("location", "") or "")

        def matches(self, weekday_value=None, time_value=None):
            week_value = int(week if weekday_value is None else weekday_value or 0)
            if self.weekdays and week_value not in self.weekdays:
                return False
            if time_value is None:
                minute_value = int(clock_minutes or 0) % 1440
            else:
                try:
                    minute_value = int(time_value) % 1440
                    if 0 <= minute_value <= 7:
                        minute_value = (6, 8, 11, 13, 16, 18, 21, 23)[minute_value] * 60
                except Exception:
                    minute_value = int(clock_minutes or 0) % 1440
            if self.start_minute <= self.end_minute:
                if not (self.start_minute <= minute_value <= self.end_minute):
                    return False
            else:
                if not (minute_value >= self.start_minute or minute_value <= self.end_minute):
                    return False
            if not str(self.selected_location() or "").strip():
                return False
            return npc_schedule_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))

    def npc_interval_location_choices_from_json(data):
        raw_location = data.get("location", "")
        probabilities = data.get("location_probabilities", data.get("location probability", data.get("locaation probability", [])))
        has_probability_contract = False
        try:
            has_probability_contract = len(list(probabilities or [])) > 0
        except Exception:
            has_probability_contract = False
        if isinstance(raw_location, str):
            if not has_probability_contract:
                return []
            raw_locations = [raw_location]
        else:
            try:
                raw_locations = list(raw_location or [])
            except Exception:
                return []
        try:
            probabilities = list(probabilities or [])
        except Exception:
            probabilities = []
        choices = []
        count = len(raw_locations)
        fallback_probability = (1.0 / count) if count > 0 else 0.0
        for index, loc in enumerate(raw_locations):
            try:
                probability = float(probabilities[index])
            except Exception:
                probability = fallback_probability
            choices.append({"location": str(loc or "").strip(), "probability": probability})
        return choices

    def npc_interval_schedule_entry_from_json(row, npc_id=""):
        data = dict(row or {})
        raw_location = data.get("location", "")
        location_choices = npc_interval_location_choices_from_json(data)
        location_value = "" if location_choices else str(raw_location or "")
        return NPCIntervalScheduleEntry(
            npc_id=str(npc_id or ""),
            location=location_value,
            location_choices=location_choices,
            weekdays=list(data.get("weekdays", []) or []),
            start=str(data.get("start", "00:00") or "00:00"),
            end=str(data.get("end", "23:59") or "23:59"),
            awake=bool(data.get("awake", True)),
            talkable=bool(data.get("talkable", True)),
            condition=npc_interval_condition_from_json(data),
            priority=int(data.get("priority", 600) or 600),
            label=str(data.get("label", "") or ""),
            source=str(data.get("source", "json") or "json"),
        )

    def npc_interval_schedule_set(npc_id="", entries=None):
        key = str(npc_id or "").strip()
        if not key:
            return
        schedules = _npc_interval_schedule_store()
        schedules[key] = list(entries or [])

    def npc_interval_schedule_list(npc_id=""):
        schedules = _npc_interval_schedule_store()
        return list(schedules.get(str(npc_id or "").strip(), []) or [])

    def npc_interval_schedule_has_contract(npc_id=""):
        npc_interval_schedule_load_all(False)
        return len(npc_interval_schedule_list(npc_id)) > 0

    def npc_interval_schedule_load_file(npc_id=""):
        key = str(npc_id or "").strip()
        if not key:
            return False
        path = "NPC/Schedules/%s.json" % key
        try:
            if not renpy.loadable(path):
                try:
                    NPCIntervalScheduleLoadErrors.pop(key, None)
                except Exception:
                    pass
                return False
        except Exception:
            pass
        try:
            raw = renpy.file(path).read()
            if hasattr(raw, "decode"):
                raw = raw.decode("utf-8")
            payload = json.loads(raw)
        except Exception as ex:
            try:
                NPCIntervalScheduleLoadErrors[key] = "%s: %s" % (path, ex)
            except Exception:
                pass
            return False
        entries = []
        for row in list(dict(payload or {}).get("entries", []) or []):
            entry = npc_interval_schedule_entry_from_json(row, key)
            if entry.location or entry.location_choices:
                entries.append(entry)
        if entries:
            npc_interval_schedule_set(key, entries)
            try:
                NPCIntervalScheduleLoadErrors.pop(key, None)
            except Exception:
                pass
            return True
        try:
            NPCIntervalScheduleLoadErrors[key] = "%s: no entries" % path
        except Exception:
            pass
        return False

    def npc_interval_schedule_load_all(force=False):
        global NPCIntervalScheduleLoaded
        if bool(NPCIntervalScheduleLoaded) and not bool(force):
            return _npc_interval_schedule_store()
        if bool(force):
            _npc_interval_schedule_store().clear()
            try:
                NPCIntervalScheduleLoadErrors.clear()
            except Exception:
                pass
        keys = set()
        try:
            keys.update([str(row or "").strip() for row in list(AllGirlNames or [])])
        except Exception:
            pass
        try:
            keys.update([str(row or "").strip() for row in list(SECONDARY_NPC_KEYS or [])])
        except Exception:
            pass
        try:
            keys.update(["amanda", "melissa", "sandra", "clara", "irma", "becky", "eddie", "alber"])
        except Exception:
            pass
        for key in sorted([row for row in keys if row]):
            npc_interval_schedule_load_file(key)
        NPCIntervalScheduleLoaded = True
        return _npc_interval_schedule_store()

    def npc_daily_schedule_month_key():
        return int(year or 0) * 100 + int(month or 0)

    def npc_daily_schedule_slot(slot=0, location="", awake=True, talkable=True, label="", priority=500):
        return {
            "slot": int(slot or 0),
            "location": str(location or "").strip(),
            "awake": bool(awake),
            "talkable": bool(talkable),
            "label": str(label or "").strip(),
            "priority": int(priority or 500),
        }

    def npc_daily_schedule_choice(location="", weight=1, awake=True, talkable=True, label="", condition=None, monthly_key="", monthly_limit=0):
        return {
            "location": str(location or "").strip(),
            "weight": max(0, int(weight or 0)),
            "awake": bool(awake),
            "talkable": bool(talkable),
            "label": str(label or "").strip(),
            "condition": condition,
            "monthly_key": str(monthly_key or "").strip(),
            "monthly_limit": int(monthly_limit or 0),
        }

    def npc_daily_schedule_random_slot(slot=0, choices=None, weekdays=None, label="", priority=500):
        return {
            "slot": int(slot or 0),
            "choices": list(choices or []),
            "weekdays": list(weekdays or []),
            "label": str(label or "").strip(),
            "priority": int(priority or 500),
        }

    def npc_daily_schedule_set(npc_id="", default_slots=None, random_slots=None):
        key = str(npc_id or "").strip()
        if not key:
            return
        templates = _npc_daily_schedule_template_store()
        templates[key] = {
            "default_slots": list(default_slots or []),
            "random_slots": list(random_slots or []),
        }

    def npc_daily_schedule_choice_allowed(choice):
        row = dict(choice or {})
        location_code = str(row.get("location", "") or "").strip()
        if not location_code:
            return False
        condition = row.get("condition", None)
        if condition is not None and not npc_schedule_rule_true(condition):
            return False
        monthly_key = str(row.get("monthly_key", "") or "").strip()
        monthly_limit = int(row.get("monthly_limit", 0) or 0)
        if monthly_key and monthly_limit > 0:
            counters = _npc_daily_schedule_counter_store()
            row_count = dict(counters.get(monthly_key, {}) or {})
            current_month = npc_daily_schedule_month_key()
            if int(row_count.get("month", -1) or -1) != current_month:
                row_count = {"month": current_month, "count": 0}
                counters[monthly_key] = row_count
            if int(row_count.get("count", 0) or 0) >= monthly_limit:
                return False
        return True

    def npc_daily_schedule_mark_choice(choice):
        row = dict(choice or {})
        monthly_key = str(row.get("monthly_key", "") or "").strip()
        monthly_limit = int(row.get("monthly_limit", 0) or 0)
        if not monthly_key or monthly_limit <= 0:
            return
        counters = _npc_daily_schedule_counter_store()
        row_count = dict(counters.get(monthly_key, {}) or {})
        current_month = npc_daily_schedule_month_key()
        if int(row_count.get("month", -1) or -1) != current_month:
            row_count = {"month": current_month, "count": 0}
        row_count["month"] = current_month
        row_count["count"] = int(row_count.get("count", 0) or 0) + 1
        counters[monthly_key] = row_count

    def npc_daily_schedule_pick_choice(choices):
        allowed = [dict(choice or {}) for choice in list(choices or []) if npc_daily_schedule_choice_allowed(choice)]
        if not allowed:
            return None
        total_weight = sum([max(0, int(row.get("weight", 1) or 1)) for row in allowed])
        if total_weight <= 0:
            return allowed[0]
        roll = renpy.random.randint(1, total_weight)
        cursor = 0
        for row in allowed:
            cursor += max(0, int(row.get("weight", 1) or 1))
            if roll <= cursor:
                npc_daily_schedule_mark_choice(row)
                return row
        npc_daily_schedule_mark_choice(allowed[-1])
        return allowed[-1]

    def npc_daily_schedule_entry_from_row(row, slot_value=None):
        data = dict(row or {})
        slot = int(data.get("slot", slot_value if slot_value is not None else 0) or 0)
        return NPCScheduleEntry(
            location=str(data.get("location", "") or ""),
            weekdays=[int(week or 0)],
            time_slots=[slot],
            awake=bool(data.get("awake", True)),
            talkable=bool(data.get("talkable", True)),
            priority=int(data.get("priority", 500) or 500),
            label=str(data.get("label", "") or ""),
        )

    def npc_daily_schedule_build(npc_id="", day_marker=None, weekday_value=None):
        key = str(npc_id or "").strip()
        templates = _npc_daily_schedule_template_store()
        template = dict(templates.get(key, {}) or {})
        if not key or not template:
            return []
        week_value = int(week if weekday_value is None else weekday_value or 0)
        slot_rows = {}
        for row in list(template.get("default_slots", []) or []):
            data = dict(row or {})
            slot = int(data.get("slot", 0) or 0)
            weekdays = list(data.get("weekdays", []) or [])
            condition = data.get("condition", None)
            if weekdays and week_value not in weekdays:
                continue
            if condition is not None and not npc_schedule_rule_true(condition):
                continue
            slot_rows[slot] = data
        for random_row in list(template.get("random_slots", []) or []):
            data = dict(random_row or {})
            slot = int(data.get("slot", 0) or 0)
            weekdays = list(data.get("weekdays", []) or [])
            if weekdays and week_value not in weekdays:
                continue
            choice = npc_daily_schedule_pick_choice(data.get("choices", []))
            if choice is None:
                continue
            choice["slot"] = slot
            choice["priority"] = int(data.get("priority", 500) or 500)
            if not str(choice.get("label", "") or "").strip():
                choice["label"] = str(data.get("label", "") or "")
            slot_rows[slot] = choice
        return [npc_daily_schedule_entry_from_row(slot_rows[slot], slot) for slot in sorted(slot_rows.keys())]

    def npc_daily_schedule_build_all(force=False):
        global NPCDailySchedulePlanDay
        day_value = int(dayspassed or 0)
        plans = _npc_daily_schedule_plan_store()
        if not force and int(NPCDailySchedulePlanDay or -1) == day_value:
            return plans
        plans.clear()
        NPCDailySchedulePlanDay = day_value
        for npc_id in list(_npc_daily_schedule_template_store().keys()):
            plans[npc_id] = npc_daily_schedule_build(npc_id, day_value, int(week or 0))
        return plans

    def npc_daily_schedule_entries(npc_id=""):
        npc_daily_schedule_build_all(False)
        plans = _npc_daily_schedule_plan_store()
        return list(plans.get(str(npc_id or "").strip(), []) or [])

    def npc_daily_schedule_rows(npc_id=""):
        rows = []
        for entry in npc_daily_schedule_entries(npc_id):
            rows.append({
                "slot": list(getattr(entry, "time_slots", []) or [None])[0],
                "location": str(getattr(entry, "location", "") or ""),
                "awake": bool(getattr(entry, "awake", True)),
                "talkable": bool(getattr(entry, "talkable", True)),
                "label": str(getattr(entry, "label", "") or ""),
            })
        return rows

    def npc_schedule_rule(kind="", **kwargs):
        payload = {"__schedule_rule__": str(kind or "").strip()}
        for key, value in dict(kwargs or {}).items():
            payload[str(key)] = value
        return payload

    def npc_schedule_stable_index(count=0, key=""):
        count_value = int(count or 0)
        if count_value <= 0:
            return 0
        key_total = 0
        for index, char_value in enumerate(str(key or "")):
            key_total += (index + 1) * ord(char_value)
        return abs(int(key_total)) % count_value

    def npc_schedule_stable_percent(key=""):
        return npc_schedule_stable_index(100, key) + 1

    def npc_schedule_eddie_absent_week():
        try:
            day_value = int(day or 0)
        except Exception:
            day_value = 0
        return 22 <= day_value <= 28

    def npc_schedule_any_job_assigned(job_name="", people=None):
        job_key = str(job_name or "").strip()
        job_map = globals().get(job_key, {})
        if not isinstance(job_map, dict):
            return False
        if people is None:
            people = list(job_map.keys())
        for person_key in list(people or []):
            if int(job_map.get(str(person_key or "").strip(), 0) or 0) > 0:
                return True
        return False

    def npc_schedule_liza_portstreets_whore_active():
        try:
            return (
                int(LizaVar.get("ProstStart", 0) or 0) > 0
                and int(jobwhore.get("liza", 0) or 0) > 0
                and str(getLocation("liza") or "") == "PortStreets"
            )
        except Exception:
            return False

    def npc_schedule_georgett_portstreets_work_active():
        try:
            return int(jobWhoreAvail.get("georgett", 0) or 0) <= 0
        except Exception:
            return False

    def npc_schedule_liza_portstreets_work_active():
        try:
            return int(LizaVar.get("ProstStart", 0) or 0) > 0 and int(jobWhoreAvail.get("liza", 0) or 0) <= 0
        except Exception:
            return False

    def npc_schedule_tavern_whore_work_active(person_key=""):
        try:
            key = str(person_key or "").strip()
            return int(jobWhoreAvail.get(key, 0) or 0) > 0 and int(jobwhore.get(key, 0) or 0) > 0
        except Exception:
            return False

    def npc_schedule_georgett_church_visible():
        try:
            return bool(knowsMC.get("georgett", False)) or int(Friends.get("georgett", 0) or 0) > 0
        except Exception:
            return False

    def npc_schedule_liza_church_with_georgett_visible():
        try:
            if not npc_schedule_georgett_church_visible():
                return False
            return (
                int(GeorgettVar.get("askkids", 0) or 0) > 0
                or int(Friends.get("liza", 0) or 0) > 0
                or int(LizaVar.get("ProstStart", 0) or 0) > 0
            )
        except Exception:
            return False

    def npc_schedule_becky_sandra_kitchen_visit_active():
        try:
            if int(dayspassed or 0) <= 30:
                return False
            if int(week or 0) not in (2, 4):
                return False
            if int(Friends.get("becky", 0) or 0) < 15 or int(Friends.get("sandra", 0) or 0) < 15:
                return False
            if int(HadSex.get("becky", 0) or 0) <= 0 and int(BeckyVar.get("HomeSex", 0) or 0) <= 0:
                return False
            fortnight = int(dayspassed or 0) // 14
            if npc_schedule_stable_percent("becky_sandra_visit_chance_%s" % fortnight) > 45:
                return False
            visit_weekday = (2, 4)[npc_schedule_stable_index(2, "becky_sandra_visit_weekday_%s" % fortnight)]
            return int(week or 0) == visit_weekday
        except Exception:
            return False

    def npc_schedule_rule_true(rule):
        if isinstance(rule, dict):
            rule_kind = str(rule.get("__schedule_rule__", "") or "").strip()
            if rule_kind == "tavern_team_match":
                return tavern_team_schedule_match(
                    str(rule.get("person", "") or ""),
                    str(rule.get("location", "") or ""),
                    str(rule.get("mode", "morning") or "morning"),
                )
            if rule_kind == "clara_extra_location":
                return str(clara_extra_location_code() or "") == str(rule.get("location", "") or "")
            if rule_kind == "clara_visible_friday_dance":
                try:
                    return bool(clara_visible_at_friday_dance())
                except Exception:
                    return False
            if rule_kind == "clara_melissa_visit":
                try:
                    time_safe = globals().get("time", 0)
                    slot_val = rule.get("slot", time_safe)
                    return bool(clara_melissa_visit_active(None, None, int(slot_val or time_safe or 0)))
                except Exception:
                    return False
            if rule_kind == "clara_paintings_confession":
                try:
                    return bool(clara_paintings_confession_schedule_active())
                except Exception:
                    return False
            if rule_kind == "clara_paintings_evening_watch":
                try:
                    return bool(clara_paintings_evening_watch_schedule_active())
                except Exception:
                    return False
            if rule_kind == "werecat_active":
                try:
                    return bool(werecat_is_living_with_household())
                except Exception:
                    return False
            if rule_kind == "werecat_roam_match":
                try:
                    return bool(werecat_is_living_with_household()) and str(werecat_roam_location() or "") == str(rule.get("location", "") or "")
                except Exception:
                    return False
            if rule_kind == "dog_home_roam":
                try:
                    return bool(dog_home_roam_active())
                except Exception:
                    return False
            if rule_kind == "sandra_night_thanks_ready":
                try:
                    SandraVar_safe = globals().get("SandraVar", {})
                    dayspassed_safe = globals().get("dayspassed", 0)
                    return int(SandraVar_safe.get("NightThanksReady", 0) or 0) > 0 and int(SandraVar_safe.get("NightThanksLastDay", -1) or -1) != int(dayspassed_safe or 0)
                except Exception:
                    return False
            if rule_kind == "job_assigned":
                try:
                    job_name = str(rule.get("job", "") or "").strip()
                    person_key = str(rule.get("person", "") or "").strip()
                    job_map = globals().get(job_name, {})
                    return isinstance(job_map, dict) and int(job_map.get(person_key, 0) or 0) > 0
                except Exception:
                    return False
            if rule_kind == "saddled_horse_available":
                try:
                    return bool(str(MyStallion or "").strip()) and int(HorseSaddled or 0) == 1
                except Exception:
                    return False
            if rule_kind == "eddie_absent_week":
                return npc_schedule_eddie_absent_week()
            if rule_kind == "eddie_in_town":
                return not npc_schedule_eddie_absent_week()
            if rule_kind == "becky_sandra_kitchen_visit":
                return npc_schedule_becky_sandra_kitchen_visit_active()
            if rule_kind == "liza_portstreets_whore_active":
                return npc_schedule_liza_portstreets_whore_active()
            if rule_kind in ("georgett_portstreets_work_active", "georgett_portstreets"):
                return npc_schedule_georgett_portstreets_work_active()
            if rule_kind in ("liza_portstreets_work_active", "liza_portstreets"):
                return npc_schedule_liza_portstreets_work_active()
            if rule_kind in ("tavern_whore_work_active", "tavern_hired"):
                return npc_schedule_tavern_whore_work_active(str(rule.get("person", "") or ""))
            if rule_kind == "georgett_church_visible":
                return npc_schedule_georgett_church_visible()
            if rule_kind == "liza_church_with_georgett_visible":
                return npc_schedule_liza_church_with_georgett_visible()
            if rule_kind == "any_job_assigned":
                try:
                    return npc_schedule_any_job_assigned(
                        str(rule.get("job", "") or ""),
                        list(rule.get("people", []) or []),
                    )
                except Exception:
                    return False
        return room_rule_true(rule)

    class NPCScheduleEntry(object):
        def __init__(
            self,
            location="",
            weekdays=None,
            time_slots=None,
            awake=True,
            talkable=True,
            venue_open_required=False,
            condition=None,
            priority=0,
            label="",
        ):
            self.location = str(location or "").strip()
            self.weekdays = list(weekdays or [])
            self.time_slots = list(time_slots or [])
            self.awake = bool(awake)
            self.talkable = bool(talkable)
            self.venue_open_required = bool(venue_open_required)
            self.condition = condition
            self.priority = int(priority or 0)
            self.label = str(label or "").strip()

        def matches(self, weekday_value=None, time_value=None):
            week_value = int(week if weekday_value is None else weekday_value or 0)
            slot_value = int(time if time_value is None else time_value or 0)
            if self.weekdays and week_value not in self.weekdays:
                return False
            if self.time_slots and slot_value not in self.time_slots:
                return False
            return npc_schedule_rule_true(self.condition)

        def __getstate__(self):
            state = dict(self.__dict__)
            state["condition"] = room_rule_serialize(state.get("condition", None))
            return state

        def __setstate__(self, state):
            self.__dict__.update(dict(state or {}))

    def npc_schedule_list(npc_id=""):
        schedules = _npc_schedule_store()
        return list(schedules.get(str(npc_id or "").strip(), []) or [])

    def npc_schedule_set(npc_id="", entries=None):
        key = str(npc_id or "").strip()
        if not key:
            return
        schedules = _npc_schedule_store()
        schedules[key] = list(entries or [])

    def npc_schedule_add(npc_id="", entry=None):
        key = str(npc_id or "").strip()
        if not key or entry is None:
            return
        schedules = _npc_schedule_store()
        schedules.setdefault(key, [])
        schedules[key].append(entry)

    def npc_schedule_sorted_entries(npc_id=""):
        npc_interval_schedule_load_all(False)
        interval_entries = npc_interval_schedule_list(npc_id)
        if interval_entries:
            entries = interval_entries
        else:
            entries = npc_daily_schedule_entries(npc_id) + npc_schedule_list(npc_id)
        return sorted(entries, key=lambda row: int(getattr(row, "priority", 0) or 0), reverse=True)

    def npc_schedule_resolve(npc_id="", weekday_value=None, time_value=None):
        for entry in npc_schedule_sorted_entries(npc_id):
            if entry.matches(weekday_value, time_value):
                return entry
        return None

    def npc_schedule_location(npc_id="", weekday_value=None, time_value=None):
        entry = npc_schedule_resolve(npc_id, weekday_value, time_value)
        if entry is not None and hasattr(entry, "selected_location"):
            return str(entry.selected_location() or "")
        return str(getattr(entry, "location", "") or "")

    def npc_is_awake(npc_id="", weekday_value=None, time_value=None):
        entry = npc_schedule_resolve(npc_id, weekday_value, time_value)
        if entry is None:
            return True
        return bool(getattr(entry, "awake", True))

    def npc_can_talk_now(npc_id="", weekday_value=None, time_value=None):
        entry = npc_schedule_resolve(npc_id, weekday_value, time_value)
        if entry is None:
            return True
        if not bool(getattr(entry, "awake", True)):
            return False
        return bool(getattr(entry, "talkable", True))

    def npc_schedule_state(npc_id="", weekday_value=None, time_value=None):
        entry = npc_schedule_resolve(npc_id, weekday_value, time_value)
        if entry is None:
            return {
                "location": "",
                "awake": True,
                "talkable": True,
                "venue_open_required": False,
                "label": "",
                "interval": "",
                "source": "",
            }
        interval_text = ""
        if hasattr(entry, "start_minute") and hasattr(entry, "end_minute"):
            interval_text = "%s-%s" % (npc_schedule_minutes_to_time(getattr(entry, "start_minute", 0)), npc_schedule_minutes_to_time(getattr(entry, "end_minute", 0)))
        else:
            interval_text = ",".join([str(row) for row in list(getattr(entry, "time_slots", []) or [])])
        return {
            "location": str(entry.selected_location() if hasattr(entry, "selected_location") else getattr(entry, "location", "") or ""),
            "awake": bool(getattr(entry, "awake", True)),
            "talkable": bool(getattr(entry, "talkable", True)),
            "venue_open_required": bool(getattr(entry, "venue_open_required", False)),
            "label": str(getattr(entry, "label", "") or ""),
            "interval": interval_text,
            "source": str(getattr(entry, "source", "rpy") or "rpy"),
        }

    def npc_schedule_sync_currentloc(npc_id="", weekday_value=None, time_value=None):
        key = str(npc_id or "").strip()
        if not key:
            return ""
        location_code = npc_schedule_location(key, weekday_value, time_value)
        if location_code:
            CurrentLoc[key] = location_code
        return str(CurrentLoc.get(key, "") or "")

    def npc_schedule_sync_all(weekday_value=None, time_value=None):
        npc_daily_schedule_build_all(False)
        for npc_id in list(_npc_schedule_store().keys()):
            npc_schedule_sync_currentloc(npc_id, weekday_value, time_value)
        for npc_id in list(_npc_daily_schedule_template_store().keys()):
            npc_schedule_sync_currentloc(npc_id, weekday_value, time_value)
        for npc_id in list(_npc_interval_schedule_store().keys()):
            npc_schedule_sync_currentloc(npc_id, weekday_value, time_value)

    def _npc_display_name(npc_id=""):
        key = str(npc_id or "").strip()
        if not key:
            return ""
        try:
            return str(RealName.get(key, key) or key)
        except Exception:
            return key

    def _npc_known_ids():
        keys = set()
        try:
            keys.update([str(row or "").strip() for row in list(_npc_schedule_store().keys())])
        except Exception:
            pass
        try:
            npc_interval_schedule_load_all(False)
            keys.update([str(row or "").strip() for row in list(_npc_interval_schedule_store().keys())])
        except Exception:
            pass
        try:
            keys.update([str(row or "").strip() for row in list(CurrentLoc.keys())])
        except Exception:
            pass
        try:
            keys.update([str(row or "").strip() for row in list(peopleInfo.keys())])
        except Exception:
            pass
        return [row for row in list(keys) if row]

    def getLocation(person="", weekday_value=None, time_value=None):
        key = str(person or "").strip()
        if not key:
            return ""
        if key.lower() == "mongol":
            try:
                return "MarketPlace" if marketplace_mongol_visible() else ""
            except Exception:
                return ""
        try:
            if bool(TavernBreakfastEventActive):
                if key.lower() in [str(row or "").strip().lower() for row in list(TavernBreakfastPresentIds or [])]:
                    return "TavernKitchen"
        except Exception:
            pass
        try:
            info = peopleInfo.get(key, None)
            if isinstance(info, PeopleInfo):
                return str(info.getLocation(weekday_value, time_value) or "")
        except Exception:
            pass
        schedule_location = str(npc_schedule_location(key, weekday_value, time_value) or "")
        if schedule_location:
            return schedule_location
        if npc_interval_schedule_has_contract(key):
            return ""
        try:
            return str(_tavern_effective_location(key, time_value) or "")
        except Exception:
            pass
        return ""

    def getNPCids(location="", weekday_value=None, time_value=None):
        room_key = str(location or "").strip()
        if not room_key:
            return []
        present = []
        for npc_id in _npc_known_ids():
            if str(getLocation(npc_id, weekday_value, time_value) or "") == room_key:
                present.append(npc_id)
        return sorted(present, key=lambda row: _npc_display_name(row).lower())

    def getNPCnames(location="", weekday_value=None, time_value=None):
        return [_npc_display_name(npc_id) for npc_id in getNPCids(location, weekday_value, time_value)]

    def isLocationEmpty(location="", weekday_value=None, time_value=None):
        return len(getNPCids(location, weekday_value, time_value)) <= 0

    def tavern_team_schedule_match(person="", expected_location="", mode="morning"):
        npc_id = str(person or "").strip().lower()
        target = str(expected_location or "").strip()
        mode_key = str(mode or "morning").strip().lower()
        if not npc_id or not target:
            return False
        try:
            if mode_key == "morning":
                return str(_tavern_household_preopening_location(npc_id) or "") == target
            if mode_key == "sunday":
                return str(_tavern_household_sunday_location(npc_id) or "") == target
            if mode_key == "friday_evening":
                return str(_tavern_household_friday_evening_location(npc_id) or "") == target
        except Exception:
            pass
        return False

    def tavern_team_default_schedule_entries(work_location="TavernMain", sleep_location="TavernMyRoom", weekend_location="TavernMain"):
        return [
            NPCScheduleEntry(location=work_location, weekdays=[1, 2, 3, 4, 5, 6], time_slots=[0], awake=True, talkable=True, priority=100, label="morning"),
            NPCScheduleEntry(location=work_location, weekdays=[1, 2, 3, 4, 5, 6], time_slots=[1, 2], awake=True, talkable=True, priority=100, label="working_day"),
            NPCScheduleEntry(location=work_location, weekdays=[1, 2, 3, 4, 6], time_slots=[3], awake=True, talkable=True, priority=90, label="late_evening"),
            NPCScheduleEntry(location=weekend_location, weekdays=[7], time_slots=[0, 1, 2, 3], awake=True, talkable=True, priority=80, label="sunday"),
            NPCScheduleEntry(location=sleep_location, weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[7], awake=False, talkable=False, priority=10, label="sleep"),
        ]
