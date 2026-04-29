# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default NPCSchedules = {}

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
        entries = npc_schedule_list(npc_id)
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
        for npc_id in list(_npc_schedule_store().keys()):
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
