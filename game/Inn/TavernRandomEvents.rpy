default TavernPlayedEventsToday = []
default TavernEventReportRows = []

init -20 python:
    class TavernWorkEventDefinition(object):
        def __init__(self, code, event_type, label, periods=None, chance=0, mandatory=False, priority=0, required_job="", condition=None, report_label=None):
            self.code = str(code or "")
            self.event_type = str(event_type or "")
            self.label = str(label or self.code)
            self.periods = list(periods or [])
            self.chance = max(0, min(100, int(chance or 0)))
            self.mandatory = bool(mandatory)
            self.priority = int(priority or 0)
            self.required_job = str(required_job or "")
            self.condition = condition
            self.report_label = str(report_label or self.label)
            self.event = Event(
                (
                    self.label,
                    None,
                    None,
                    None,
                    1,
                    None,
                    None,
                    None,
                    "TavernMain",
                    "tavern_work",
                    self.priority,
                ),
                "tavern_work_random",
                False,
            )

        def can_schedule(self):
            if self.required_job and len(tavern_work_job_candidates(self.required_job)) <= 0:
                return False
            if callable(self.condition):
                return bool(self.condition())
            return True


    def tavern_work_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default


    def tavern_work_job_map(job_code):
        key = str(job_code or "")
        if key == "jobwaitress":
            return jobwaitress
        if key == "jobcleaning":
            return jobcleaning
        if key == "jobkitchen":
            return jobkitchen
        return {}


    def tavern_work_job_candidates(job_code):
        source = tavern_work_job_map(job_code)
        if not isinstance(source, dict):
            return []
        out = []
        for person, value in source.items():
            if tavern_work_int(value, 0) != 0:
                out.append(str(person or ""))
        return [person for person in out if person]


    def tavern_work_liza_talk_ready():
        return (
            tavern_work_int(jobWhoreAvail.get("liza", 0), 0) != 0
            and (
                tavern_work_int(jobgloryhole.get("liza", 0), 0) == 0
                or tavern_work_int(time, 0) < 2
            )
        )


    def tavern_work_wine_for_dance_ready():
        return tavern_work_int(week, 0) == 3


    def tavern_work_roll(chance, key):
        chance_value = max(0, min(100, tavern_work_int(chance, 0)))
        if chance_value <= 0:
            return False
        if chance_value >= 100:
            return True
        return procedural_randint(1, 100, key) <= chance_value


    def tavern_work_choice(values, key):
        rows = list(values or [])
        if len(rows) <= 0:
            return None
        return rows[procedural_randint(0, len(rows) - 1, key)]


    def tavern_work_definition(code):
        code_key = str(code or "")
        for defs in tavern_work_events_by_type.values():
            for event_def in defs:
                if event_def.code == code_key:
                    return event_def
        return None


    def tavern_work_planned_for(code="", location_name="", time_period=None):
        code_key = str(code or "")
        loc_key = str(location_name or CurLoc or "")
        if loc_key != "TavernMain":
            return False
        if tavern_work_int(week, 0) == 7 or tavern_preopening_mode():
            return False
        tp = tavern_work_int(time if time_period is None else time_period, 0)
        for row in list(tavern_work_events or []):
            if bool(row.get("mandatory", False)):
                continue
            if str(row.get("code", "") or "") != code_key:
                continue
            if tavern_work_int(row.get("period", 0), 0) == tp:
                return True
        return False


    def tavern_work_plan_row(event_def, period):
        return {
            "code": event_def.code,
            "type": event_def.event_type,
            "label": event_def.label,
            "period": tavern_work_int(period, 0),
            "mandatory": bool(event_def.mandatory),
            "priority": int(event_def.priority or 0),
        }


    def tavern_work_sync_legacy_queue():
        EventsCount.clear()
        NewEvents.clear()
        for row in list(tavern_work_events or []):
            slot = 10 if bool(row.get("mandatory", False)) else tavern_work_int(row.get("period", 0), 0)
            index = tavern_work_int(EventsCount.get(slot, 0), 0)
            NewEvents[str(slot) + "_" + str(index)] = str(row.get("code", "") or "")
            EventsCount[slot] = index + 1


    def tavern_work_add_report_row(row, witnessed):
        report = {
            "day": tavern_work_int(dayspassed, 0),
            "code": str(row.get("code", "") or ""),
            "type": str(row.get("type", "") or ""),
            "period": tavern_work_int(row.get("period", 0), 0),
            "witnessed": bool(witnessed),
        }
        TavernEventReportRows.append(report)
        return report


    def tavern_work_build_daily_plan():
        tavern_work_events[:] = []
        TavernPlayedEventsToday[:] = []
        TavernEventReportRows[:] = []

        current_day = tavern_work_int(dayspassed, 0)
        for event_type in tavern_work_random_type_order:
            candidates = [row for row in tavern_work_events_by_type.get(event_type, []) if row.can_schedule()]
            if len(candidates) <= 0:
                continue
            type_chance = tavern_work_type_chances.get(event_type, 0)
            if not tavern_work_roll(type_chance, "tavern_work_%s_%s_roll" % (event_type, current_day)):
                continue
            selected = tavern_work_choice(candidates, "tavern_work_%s_%s_choice" % (event_type, current_day))
            if selected is None:
                continue
            period = tavern_work_choice(selected.periods, "tavern_work_%s_%s_period" % (selected.code, current_day))
            if period is None:
                continue
            tavern_work_events.append(tavern_work_plan_row(selected, period))

        for event_def in tavern_work_events_by_type.get("mandatory", []):
            if event_def.can_schedule():
                period = event_def.periods[0] if len(event_def.periods) > 0 else 10
                tavern_work_events.append(tavern_work_plan_row(event_def, period))

        tavern_work_events.sort(key=lambda row: (0 if bool(row.get("mandatory", False)) else 1, tavern_work_int(row.get("period", 0), 0), tavern_work_int(row.get("priority", 0), 0)))
        tavern_work_sync_legacy_queue()
        return list(tavern_work_events)


    def tavern_work_pending_mandatory_code(code="", room_code=""):
        code_key = str(code or "")
        room_key = str(room_code or CurLoc or "")
        for row in list(tavern_work_events or []):
            if not bool(row.get("mandatory", False)):
                continue
            if code_key and str(row.get("code", "") or "") != code_key:
                continue
            if str(row.get("code", "") or "") == "WineForDance" and room_key != "TavernKitchen":
                continue
            return str(row.get("code", "") or "")
        return ""


    def tavern_work_pop_mandatory_code(code="", room_code=""):
        code_key = str(code or "")
        room_key = str(room_code or CurLoc or "")
        for index, row in enumerate(list(tavern_work_events or [])):
            if not bool(row.get("mandatory", False)):
                continue
            if code_key and str(row.get("code", "") or "") != code_key:
                continue
            if str(row.get("code", "") or "") == "WineForDance" and room_key != "TavernKitchen":
                continue
            popped = tavern_work_events.pop(index)
            tavern_work_add_report_row(popped, True)
            TavernPlayedEventsToday.append(str(popped.get("code", "") or ""))
            tavern_work_sync_legacy_queue()
            return str(popped.get("code", "") or "")
        return ""


    def tavern_work_pop_planned_event(time_period, require_room_match=False, room_code=""):
        tp = tavern_work_int(time_period, 0)
        room_key = str(room_code or CurLoc or "")

        for index, row in enumerate(list(tavern_work_events or [])):
            code = str(row.get("code", "") or "")
            if not bool(row.get("mandatory", False)):
                continue
            if code == "WineForDance" and require_room_match and room_key != "TavernKitchen":
                continue
            popped = tavern_work_events.pop(index)
            tavern_work_add_report_row(popped, bool(require_room_match))
            TavernPlayedEventsToday.append(code)
            tavern_work_sync_legacy_queue()
            return {"code": code, "slot": 10}

        for index, row in enumerate(list(tavern_work_events or [])):
            if bool(row.get("mandatory", False)):
                continue
            if tavern_work_int(row.get("period", 0), 0) != tp:
                continue
            popped = tavern_work_events.pop(index)
            code = str(popped.get("code", "") or "")
            tavern_work_add_report_row(popped, bool(require_room_match))
            TavernPlayedEventsToday.append(code)
            tavern_work_sync_legacy_queue()
            return {"code": code, "slot": tp}

        return {"code": "", "slot": tp}


    def tavern_work_pop_planned_code(code="", time_period=None, require_room_match=False, room_code=""):
        code_key = str(code or "")
        tp = tavern_work_int(time if time_period is None else time_period, 0)
        for index, row in enumerate(list(tavern_work_events or [])):
            if bool(row.get("mandatory", False)):
                continue
            if str(row.get("code", "") or "") != code_key:
                continue
            if tavern_work_int(row.get("period", 0), 0) != tp:
                continue
            popped = tavern_work_events.pop(index)
            tavern_work_add_report_row(popped, bool(require_room_match))
            TavernPlayedEventsToday.append(code_key)
            tavern_work_sync_legacy_queue()
            return dict(popped or {})
        return {}


define tavern_work_type_chances = {
    "harrass": 55,
    "small_fight": 20,
    "tavern_story": 25,
    "theft": 0,
    "big_fight": 0,
}

define tavern_work_random_type_order = ("harrass", "small_fight", "tavern_story", "theft", "big_fight")

define tavern_work_events_by_type = {
    "harrass": [
        TavernWorkEventDefinition("WaitressHarass", "harrass", "event_waitress_harrass", periods=(0, 1, 2, 3, 4), chance=55, required_job="jobwaitress", priority=20),
        TavernWorkEventDefinition("CleaningHarass", "harrass", "event_cleaning_harrass", periods=(0, 1, 2, 3, 4), chance=55, required_job="jobcleaning", priority=30),
    ],
    "small_fight": [
        TavernWorkEventDefinition("FightSmall", "small_fight", "EventFightSmall", periods=(3, 4), chance=20, priority=40),
    ],
    "tavern_story": [
        TavernWorkEventDefinition("AmandaLizaTalk", "tavern_story", "EventAmandaLizettTalk", periods=(1, 2), chance=25, condition=tavern_work_liza_talk_ready, priority=50),
    ],
    "theft": [],
    "big_fight": [],
    "mandatory": [
        TavernWorkEventDefinition("WineForDance", "mandatory", "EventWineForDance", periods=(10,), mandatory=True, condition=tavern_work_wine_for_dance_ready, priority=0),
    ],
}


label TavernWorkEventTrigger:
    $ SignalBlockTime = 1
    call DisplayTavernEventShort(time, 1)
    $ TavernEventOngoing = str(_return or "")
    if str(TavernEventOngoing or "").strip():
        $ MainTxt = TavernEventOngoing
        $ CurLocDesc = MainTxt
        call screen main_ui
        return True
    return False
