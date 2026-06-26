# ================================================================================
# Daily sex/dance event runtime. Public functions stay as direct label helpers;
# state is owned by the SexEvents object.
# ================================================================================

label SexEventsTableCode:
    return

init -44 python:
    class SexEventRuntime(object):
        def __init__(self):
            self.today_events = []
            self.girl_dance = []
            self.dance_watch_line = {}

        def clear_today(self):
            del self.today_events[:]
            return 0

        def add_today(self, girl_name="", event_time=99, event_type=0, place_name=""):
            self.today_events.append({
                "GirlName": str(girl_name or ""),
                "Time": _sexevents_int(event_time, 99),
                "EventType": _sexevents_int(event_type, 0),
                "Place": str(place_name or ""),
            })
            return len(self.today_events)

        def today_index(self, girl_name="", event_time=99, place_name=""):
            girl_value = str(girl_name or "")
            time_value = _sexevents_int(event_time, 99)
            place_value = str(place_name or "")
            for index, row in enumerate(self.today_events, start=1):
                if str(row.get("GirlName", "") or "") != girl_value:
                    continue
                if time_value < 99 and _sexevents_int(row.get("Time", 99), 99) != time_value:
                    continue
                if place_value != "" and str(row.get("Place", "") or "") != place_value:
                    continue
                return index
            return -1

        def today_event_index(self, girl_name="", event_type=0):
            girl_value = str(girl_name or "")
            event_value = _sexevents_int(event_type, 0)
            for index, row in enumerate(self.today_events, start=1):
                if str(row.get("GirlName", "") or "") == girl_value and _sexevents_int(row.get("EventType", 0), 0) == event_value:
                    return index
            return 0

        def pop_today(self, girl_name="", event_time=99, place_name=""):
            row_index = self.today_index(girl_name, event_time, place_name)
            if row_index <= 0:
                return 0
            row = self.today_events.pop(row_index - 1)
            return _sexevents_int(row.get("EventType", 0), 0)

        def pop_first_today(self):
            if not self.today_events:
                return {}
            return self.today_events.pop(0)

        def delete_girl_today(self, girl_name=""):
            girl_value = str(girl_name or "")
            self.today_events[:] = [row for row in self.today_events if str(row.get("GirlName", "") or "") != girl_value]
            return 0

        def clear_dance(self):
            del self.girl_dance[:]
            return 0

        def add_dance(self, girl_name="", partner_name="", dance_num=0, go_out=0, go_phrase=""):
            self.girl_dance.append({
                "GirlName": str(girl_name or ""),
                "PartnerName": str(partner_name or ""),
                "DanceNum": _sexevents_int(dance_num, 0),
                "GoOut": _sexevents_int(go_out, 0),
                "GoPhrase": str(go_phrase or ""),
            })
            return len(self.girl_dance)

        def dance_index(self, girl_name="", partner_name="", dance_num=0):
            girl_value = str(girl_name or "")
            partner_value = str(partner_name or "")
            dance_need = _sexevents_int(dance_num, 0) + 1
            for index, row in enumerate(self.girl_dance, start=1):
                if str(row.get("GirlName", "") or "") == girl_value and str(row.get("PartnerName", "") or "") == partner_value and _sexevents_int(row.get("DanceNum", 0), 0) == dance_need:
                    return index
            return -1

        def pop_first_dance(self):
            if not self.girl_dance:
                return {}
            return self.girl_dance.pop(0)

        def delete_girl_dance(self, girl_name=""):
            girl_value = str(girl_name or "")
            self.girl_dance[:] = [row for row in self.girl_dance if str(row.get("GirlName", "") or "") != girl_value]
            return 0

    def _sexevents_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def _SexEventsInt(value, default=0):
        return _sexevents_int(value, default)

    def _sexevents_normalize_dude_name(dude_name):
        dude_value = str(dude_name or "")
        if dude_value.lower() == "you":
            return "Вы"
        if dude_value.lower() == "eddie":
            return "Эдди"
        if dude_value.lower() == "legare":
            return "Мессир Легаре"
        return dude_value

    def _SexEventsNormalizeDudeName(dude_name):
        return _sexevents_normalize_dude_name(dude_name)

    def sex_history_rows(girl_name):
        girl = getPersonInfo(girl_name)
        rows = list(getattr(girl, "detailed_sex_history", []) or []) if girl is not None else []
        normalized = []
        for index, row in enumerate(rows, start=1):
            normalized.append({
                "RowId": _sexevents_int(row.get("RowId", row.get("row_id", index)), index),
                "DudeName": str(row.get("DudeName", row.get("partner", "")) or ""),
                "DudeNameType": str(row.get("DudeNameType", row.get("partner_type", "")) or ""),
                "CumTarget": str(row.get("CumTarget", row.get("cum_target", "")) or ""),
                "Day": _sexevents_int(row.get("Day", row.get("day", 0)), 0),
            })
        return normalized

    def TodaySexEvents_Clear():
        return SexEvents.clear_today()

    def TodaySexEvents_Add(girl_name="", event_time=99, event_type=0, place_name=""):
        return SexEvents.add_today(girl_name, event_time, event_type, place_name)

    def TodaySexEvents_FindIndex(girl_name="", event_time=99, place_name=""):
        return SexEvents.today_index(girl_name, event_time, place_name)

    def TodaySexEvents_FindEvent(girl_name="", event_type=0):
        return SexEvents.today_event_index(girl_name, event_type)

    def TodaySexEvents_Pop(girl_name="", event_time=99, place_name=""):
        return SexEvents.pop_today(girl_name, event_time, place_name)

    def TodaySexEvents_PopFirst():
        return SexEvents.pop_first_today()

    def TodaySexEvents_DeleteGirl(girl_name=""):
        return SexEvents.delete_girl_today(girl_name)

    def GirlDance_Clear():
        return SexEvents.clear_dance()

    def GirlDance_Add(girl_name="", partner_name="", dance_num=0, go_out=0, go_phrase=""):
        return SexEvents.add_dance(girl_name, partner_name, dance_num, go_out, go_phrase)

    def GirlDance_FindIndex(girl_name="", partner_name="", dance_num=0):
        return SexEvents.dance_index(girl_name, partner_name, dance_num)

    def GirlDance_PopFirst():
        return SexEvents.pop_first_dance()

    def GirlDance_DeleteGirl(girl_name=""):
        return SexEvents.delete_girl_dance(girl_name)

    def CheckIfSexEventExist(GirlNameSE, timeSE, PlaceSE=""):
        return TodaySexEvents_FindIndex(GirlNameSE, timeSE, PlaceSE)

    def CheckIfEventAlreadyExist(GirlNameSE, EventTypeSE):
        return TodaySexEvents_FindEvent(GirlNameSE, EventTypeSE)

    def GetSexEventFromTable(GirlNameSE, timeSE, PlaceSE=""):
        return TodaySexEvents_Pop(GirlNameSE, timeSE, PlaceSE)

    def CheckIfDanceExist(GirlNameSE, PartnerNameSE, DanceNumSE):
        return GirlDance_FindIndex(GirlNameSE, PartnerNameSE, DanceNumSE)

    def GetDanceFromTable(GirlNameSE, PartnerNameSE, DanceNumSE):
        row_index = GirlDance_FindIndex(GirlNameSE, PartnerNameSE, DanceNumSE)
        if row_index <= 0:
            return 0
        row = SexEvents.girl_dance.pop(row_index - 1)
        if str(GirlNameSE or "") == "amanda":
            SexEvents.dance_watch_line[6] = str(row.get("GoPhrase", "") or "")
            Amanda.set_var_int("LegareGo", _sexevents_int(row.get("GoOut", 0), 0))
        return row_index

    def GetDanceJustLeft(GirlNameSE, PartnerNameSE, DanceNumSE):
        prev_dance_num = _sexevents_int(DanceNumSE, 0) - 1
        row_index = GirlDance_FindIndex(GirlNameSE, PartnerNameSE, prev_dance_num)
        if row_index <= 0:
            return 0
        row = SexEvents.girl_dance[row_index - 1]
        if str(GirlNameSE or "") == "amanda" and _sexevents_int(row.get("GoOut", 0), 0) == 1:
            SexEvents.girl_dance.pop(row_index - 1)
            return row_index
        return 0

    def GetLastSexDays(GirlNameSE, DudeNameSE="", CumTargetSE="", SignSE=""):
        dude_value = _sexevents_normalize_dude_name(DudeNameSE).lower()
        cum_value = str(CumTargetSE or "").lower()
        sign_value = str(SignSE or "")
        latest_day = 0
        for row in sex_history_rows(GirlNameSE):
            row_dude = str(row.get("DudeName", "") or "").lower()
            row_cum = str(row.get("CumTarget", "") or "").lower()
            row_day = _sexevents_int(row.get("Day", 0), 0)
            matched = True
            if dude_value != "" and row_dude != dude_value:
                matched = False
            if cum_value != "" and sign_value == "<>" and row_cum == cum_value:
                matched = False
            if cum_value != "" and sign_value != "<>" and row_cum != cum_value:
                matched = False
            if matched:
                latest_day = max(latest_day, row_day)
        if latest_day > 0:
            return dayspassed + 1 - latest_day
        return -1

    def GetSexNum(GirlNameSE, DudeNameSE="", CumTargetSE="", SignSE="", StartDaySE=0):
        dude_value = _sexevents_normalize_dude_name(DudeNameSE).lower()
        cum_value = str(CumTargetSE or "").lower()
        sign_value = str(SignSE or "")
        start_day_value = _sexevents_int(StartDaySE, 0)
        count = 0
        for row in sex_history_rows(GirlNameSE):
            row_dude = str(row.get("DudeName", "") or "").lower()
            row_cum = str(row.get("CumTarget", "") or "").lower()
            row_day = _sexevents_int(row.get("Day", 0), 0)
            matched = True
            if dude_value != "" and row_dude != dude_value:
                matched = False
            if cum_value != "" and sign_value == "<>" and row_cum == cum_value:
                matched = False
            if cum_value != "" and sign_value != "<>" and row_cum != cum_value:
                matched = False
            if start_day_value > 0 and row_day < start_day_value + 1:
                matched = False
            if matched:
                count += 1
        return count

    def dyneval_CheckIfEventAlreadyExist(*ArgsSE, **KwArgsSE):
        return CheckIfEventAlreadyExist(*ArgsSE, **KwArgsSE)

default SexEvents = SexEventRuntime()
