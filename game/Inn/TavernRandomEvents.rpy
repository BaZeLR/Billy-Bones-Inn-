
init -20 python:
    class TavernWorkEventDefinition(object):
        def __init__(self, code, event_type, label, periods=None, chance=0, mandatory=False, priority=0, required_job="", condition=None, play_condition=None, report_label=None):
            self.code = str(code or "")
            self.event_type = str(event_type or "")
            self.label = str(label or self.code)
            self.periods = list(periods or [])
            self.chance = max(0, min(100, int(chance or 0)))
            self.mandatory = bool(mandatory)
            self.priority = int(priority or 0)
            self.required_job = str(required_job or "")
            self.condition = condition
            self.play_condition = play_condition
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

        def can_play(self, room_code=""):
            if self.required_job and len(tavern_work_job_candidates(self.required_job, room_code)) <= 0:
                return False
            if callable(self.play_condition):
                return bool(self.play_condition(str(room_code or "")))
            return True


    def tavern_work_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default


    def tavern_work_job_candidates(job_code, room_code=""):
        return list(girls_by_job(str(job_code or ""), str(room_code or "") or None) or [])


    def tavern_work_liza_talk_ready():
        return (
            Liza.can_work_tavern()
            and (
                not Liza.can_use_gloryhole()
                or tavern_work_int(calendar_v2.time_slot(), 0) < 2
            )
        )


    def tavern_work_wine_for_dance_ready():
        return tavern_work_int(calendar_v2.week, 0) == 3


    def tavern_work_melissa_waitress_fall_scheduled():
        return int(Melissa.job_value("jobwaitress", 0) or 0) > 0


    def tavern_work_melissa_waitress_fall_playable(room_code=""):
        return (
            str(room_code or "") == "TavernMain"
            and int(Melissa.job_value("jobwaitress", 0) or 0) > 0
            and str(people.location("melissa") or "") == "TavernMain"
        )


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
        loc_key = str(location_name or rooms.current_code or "")
        if loc_key != "TavernMain":
            return False
        if tavern_work_int(calendar_v2.week, 0) == 7 or tavern_preopening_mode():
            return False
        tp = tavern_work_int(calendar_v2.time_slot() if time_period is None else time_period, 0)
        for row in list(event_runtime.tavern_work_events or []):
            if bool(row.get("mandatory", False)):
                continue
            if code_key and str(row.get("code", "") or "") != code_key:
                continue
            if tavern_work_int(row.get("period", 0), 0) == tp:
                event_def = tavern_work_definition(str(row.get("code", "") or ""))
                if event_def is not None and not event_def.can_play(loc_key):
                    continue
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


    def tavern_work_codes_for_period(period, include_mandatory=True):
        period_value = tavern_work_int(period, 0)
        codes = []
        for row in list(event_runtime.tavern_work_events or []):
            mandatory = bool(row.get("mandatory", False))
            if mandatory:
                if include_mandatory and period_value == 10:
                    codes.append(str(row.get("code", "") or ""))
                continue
            if tavern_work_int(row.get("period", 0), 0) == period_value:
                codes.append(str(row.get("code", "") or ""))
        return [code for code in codes if code]

    def tavern_work_has_period(period, include_mandatory=True):
        return len(tavern_work_codes_for_period(period, include_mandatory)) > 0


    def tavern_work_add_report_row(row, witnessed):
        report = {
            "day": current_game_day(),
            "code": str(row.get("code", "") or ""),
            "type": str(row.get("type", "") or ""),
            "period": tavern_work_int(row.get("period", 0), 0),
            "witnessed": bool(witnessed),
        }
        event_runtime.tavern_report_rows.append(report)
        return report


    def tavern_work_build_daily_plan():
        event_runtime.tavern_work_events[:] = []
        event_runtime.tavern_played_today[:] = []
        event_runtime.tavern_report_rows[:] = []

        current_day = current_game_day()
        event_runtime.tavern_work_plan_day = current_day
        for event_type in tavern_work_random_type_order:
            candidates = [row for row in tavern_work_events_by_type.get(event_type, []) if row.can_schedule()]
            if len(candidates) <= 0:
                continue
            if event_type == "harrass":
                for event_def in candidates:
                    periods = list(event_def.periods or [])
                    if len(periods) <= 0:
                        continue
                    first_period_index = procedural_randint(0, len(periods) - 1, "tavern_work_%s_%s_first_period" % (event_def.code, current_day))
                    for period_offset in range(min(2, len(periods))):
                        period = periods[(first_period_index + period_offset) % len(periods)]
                        event_runtime.tavern_work_events.append(tavern_work_plan_row(event_def, period))
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
            event_runtime.tavern_work_events.append(tavern_work_plan_row(selected, period))

        for event_def in tavern_work_events_by_type.get("mandatory", []):
            if event_def.can_schedule():
                period = event_def.periods[0] if len(event_def.periods) > 0 else 10
                event_runtime.tavern_work_events.append(tavern_work_plan_row(event_def, period))

        event_runtime.tavern_work_events.sort(key=lambda row: (0 if bool(row.get("mandatory", False)) else 1, tavern_work_int(row.get("period", 0), 0), tavern_work_int(row.get("priority", 0), 0)))
        return list(event_runtime.tavern_work_events)


    def tavern_work_pending_mandatory_code(code="", room_code=""):
        code_key = str(code or "")
        room_key = str(room_code or rooms.current_code or "")
        for row in list(event_runtime.tavern_work_events or []):
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
        room_key = str(room_code or rooms.current_code or "")
        for index, row in enumerate(list(event_runtime.tavern_work_events or [])):
            if not bool(row.get("mandatory", False)):
                continue
            if code_key and str(row.get("code", "") or "") != code_key:
                continue
            if str(row.get("code", "") or "") == "WineForDance" and room_key != "TavernKitchen":
                continue
            popped = event_runtime.tavern_work_events.pop(index)
            tavern_work_add_report_row(popped, True)
            event_runtime.tavern_played_today.append(str(popped.get("code", "") or ""))
            return str(popped.get("code", "") or "")
        return ""


    def tavern_work_pop_planned_event(time_period, require_room_match=False, room_code=""):
        tp = tavern_work_int(time_period, 0)
        room_key = str(room_code or rooms.current_code or "")

        for index, row in enumerate(list(event_runtime.tavern_work_events or [])):
            code = str(row.get("code", "") or "")
            if not bool(row.get("mandatory", False)):
                continue
            if code == "WineForDance" and require_room_match and room_key != "TavernKitchen":
                continue
            popped = event_runtime.tavern_work_events.pop(index)
            tavern_work_add_report_row(popped, bool(require_room_match))
            event_runtime.tavern_played_today.append(code)
            result = dict(popped)
            result["slot"] = 10
            return result

        for index, row in enumerate(list(event_runtime.tavern_work_events or [])):
            if bool(row.get("mandatory", False)):
                continue
            if tavern_work_int(row.get("period", 0), 0) != tp:
                continue
            if require_room_match:
                event_def = tavern_work_definition(str(row.get("code", "") or ""))
                if event_def is not None and not event_def.can_play(room_key):
                    continue
            popped = event_runtime.tavern_work_events.pop(index)
            code = str(popped.get("code", "") or "")
            tavern_work_add_report_row(popped, bool(require_room_match))
            event_runtime.tavern_played_today.append(code)
            result = dict(popped)
            result["slot"] = tp
            return result

        return {"code": "", "slot": tp}


    def tavern_work_pop_planned_code(code="", time_period=None, require_room_match=False, room_code=""):
        code_key = str(code or "")
        tp = tavern_work_int(calendar_v2.time_slot() if time_period is None else time_period, 0)
        for index, row in enumerate(list(event_runtime.tavern_work_events or [])):
            if bool(row.get("mandatory", False)):
                continue
            if str(row.get("code", "") or "") != code_key:
                continue
            if tavern_work_int(row.get("period", 0), 0) != tp:
                continue
            popped = event_runtime.tavern_work_events.pop(index)
            tavern_work_add_report_row(popped, bool(require_room_match))
            event_runtime.tavern_played_today.append(code_key)
            return dict(popped or {})
        return {}


define tavern_work_type_chances = {
    "harrass": 55,
    "work_mishap": 25,
    "small_fight": 20,
    "tavern_story": 25,
    "theft": 0,
    "big_fight": 0,
}

define tavern_work_random_type_order = ("harrass", "work_mishap", "small_fight", "tavern_story", "theft", "big_fight")

define tavern_work_events_by_type = {
    "harrass": [
        TavernWorkEventDefinition("WaitressHarass", "harrass", "event_waitress_harrass", periods=(2, 3, 4), chance=55, required_job="jobwaitress", priority=20),
        TavernWorkEventDefinition("CleaningHarass", "harrass", "event_cleaning_harrass", periods=(2, 3, 4), chance=55, required_job="jobcleaning", priority=30),
    ],
    "work_mishap": [
        TavernWorkEventDefinition(
            "MelissaWaitressFall",
            "work_mishap",
            "event_melissa_waitress_fall",
            periods=(2, 3, 4),
            chance=25,
            required_job="jobwaitress",
            condition=tavern_work_melissa_waitress_fall_scheduled,
            play_condition=tavern_work_melissa_waitress_fall_playable,
            priority=25,
        ),
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
    $ renpy.dynamic("_tavern_event_text")
    call DisplayTavernEventShort(calendar_v2.time_slot(), 1)
    $ _tavern_event_text = str(_return or "")
    if str(_tavern_event_text or "").strip():
        $ scene_runtime.text = _tavern_event_text
        $ scene_runtime.location_text = scene_runtime.text
        return True
    return True
