# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default NPCSchedules = {}
default NPCDailyScheduleTemplates = {}
default NPCDailySchedulePlans = {}
default NPCDailySchedulePlanDay = -1
default NPCDailyScheduleMonthlyCounters = {}

init python:
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
                    return bool(clara_melissa_visit_active(None, None, int(rule.get("slot", time) or time or 0)))
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
                    return int(SandraVar.get("NightThanksReady", 0) or 0) > 0 and int(SandraVar.get("NightThanksLastDay", -1) or -1) != int(dayspassed or 0)
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
        entries = npc_daily_schedule_entries(npc_id) + npc_schedule_list(npc_id)
        return sorted(entries, key=lambda row: int(getattr(row, "priority", 0) or 0), reverse=True)

    def npc_schedule_resolve(npc_id="", weekday_value=None, time_value=None):
        for entry in npc_schedule_sorted_entries(npc_id):
            if entry.matches(weekday_value, time_value):
                return entry
        return None

    def npc_schedule_location(npc_id="", weekday_value=None, time_value=None):
        entry = npc_schedule_resolve(npc_id, weekday_value, time_value)
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
                "location": str(CurrentLoc.get(str(npc_id or "").strip(), "") or ""),
                "awake": True,
                "talkable": True,
                "venue_open_required": False,
                "label": "",
            }
        return {
            "location": str(getattr(entry, "location", "") or ""),
            "awake": bool(getattr(entry, "awake", True)),
            "talkable": bool(getattr(entry, "talkable", True)),
            "venue_open_required": bool(getattr(entry, "venue_open_required", False)),
            "label": str(getattr(entry, "label", "") or ""),
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
        try:
            if bool(TavernBreakfastEventActive) and isinstance(TavernBreakfastPresentIds, list):
                if key.lower() in [str(row or "").strip().lower() for row in list(TavernBreakfastPresentIds or [])]:
                    return "TavernKitchen"
        except Exception:
            pass
        try:
            return str(_tavern_effective_location(key, time_value) or "")
        except Exception:
            pass
        return str(npc_schedule_location(key, weekday_value, time_value) or CurrentLoc.get(key, "") or "")

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
            NPCScheduleEntry(location=sleep_location, weekdays=[1, 2, 3, 4, 5, 6, 7], time_slots=[4], awake=False, talkable=False, priority=10, label="sleep"),
        ]
