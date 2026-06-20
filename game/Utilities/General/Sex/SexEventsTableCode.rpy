# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label SexEventsTableCode:
    return

# Core daily and history tables for sex events (RPy equivalent of original QSP TodaySexEvent tables)
# These must exist for any girl. Used for daily prostitution/glory events in tavern and side effects.
default TodaySexEvents = []
default GirlDance = []
default DanceWatchLine = {}
default sex_history_by_girl = {}

init -44 python:
    import renpy

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

    def _sexevents_history_table(girl_name):
        return "SexHistoryList" + str(girl_name or "")

    def _SexEventsHistoryTable(girl_name):
        return _sexevents_history_table(girl_name)

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

    def _sexevents_store_attr(name, default):
        return getattr(renpy.store, name, default)

    def _sexevents_table_rows(table_name):
        row_ids = list(_sexevents_store_attr("table_%s_rows" % table_name, []) or [])
        columns = list(_sexevents_store_attr("table_%s_columns" % table_name, []) or [])
        data = _sexevents_store_attr("table_%s_data" % table_name, {}) or {}
        rows = []

        for row_id in row_ids:
            row = {"RowId": _sexevents_int(row_id, 0)}
            for column in columns:
                row[str(column)] = data.get("%s_%s" % (row_id, column), "")
            rows.append(row)

        return rows

    def _sexevents_repo_rows(girl_name):
        repo = getattr(renpy.store, "sex_history_by_girl", {}) or {}
        rows = repo.get(str(girl_name or ""), [])
        return list(rows or [])

    def sex_history_rows(girl_name):
        repo_rows = _sexevents_repo_rows(girl_name)
        if repo_rows:
            return repo_rows
        return _sexevents_table_rows(_sexevents_history_table(girl_name))

    def TodaySexEvents_Clear():
        del TodaySexEvents[:]
        return 0

    def TodaySexEvents_Add(girl_name="", event_time=99, event_type=0, place_name=""):
        TodaySexEvents.append({
            "GirlName": str(girl_name or ""),
            "Time": _sexevents_int(event_time, 99),
            "EventType": _sexevents_int(event_type, 0),
            "Place": str(place_name or ""),
        })
        return len(TodaySexEvents)

    def TodaySexEvents_FindIndex(girl_name="", event_time=99, place_name=""):
        girl_value = str(girl_name or "")
        time_value = _sexevents_int(event_time, 99)
        place_value = str(place_name or "")
        for index, row in enumerate(TodaySexEvents, start=1):
            if str(row.get("GirlName", "") or "") != girl_value:
                continue
            if time_value < 99 and _sexevents_int(row.get("Time", 99), 99) != time_value:
                continue
            if place_value != "" and str(row.get("Place", "") or "") != place_value:
                continue
            return index
        return -1

    def TodaySexEvents_FindEvent(girl_name="", event_type=0):
        girl_value = str(girl_name or "")
        event_value = _sexevents_int(event_type, 0)
        for index, row in enumerate(TodaySexEvents, start=1):
            if str(row.get("GirlName", "") or "") != girl_value:
                continue
            if _sexevents_int(row.get("EventType", 0), 0) == event_value:
                return index
        return 0

    def TodaySexEvents_Pop(girl_name="", event_time=99, place_name=""):
        row_index = TodaySexEvents_FindIndex(girl_name, event_time, place_name)
        if row_index <= 0:
            return 0
        row = TodaySexEvents.pop(row_index - 1)
        return _sexevents_int(row.get("EventType", 0), 0)

    def TodaySexEvents_PopFirst():
        if not TodaySexEvents:
            return {}
        return TodaySexEvents.pop(0)

    def TodaySexEvents_DeleteGirl(girl_name=""):
        girl_value = str(girl_name or "")
        TodaySexEvents[:] = [
            row for row in TodaySexEvents
            if str(row.get("GirlName", "") or "") != girl_value
        ]
        return 0

    def GirlDance_Clear():
        del GirlDance[:]
        return 0

    def GirlDance_Add(girl_name="", partner_name="", dance_num=0, go_out=0, go_phrase=""):
        GirlDance.append({
            "GirlName": str(girl_name or ""),
            "PartnerName": str(partner_name or ""),
            "DanceNum": _sexevents_int(dance_num, 0),
            "GoOut": _sexevents_int(go_out, 0),
            "GoPhrase": str(go_phrase or ""),
        })
        return len(GirlDance)

    def GirlDance_FindIndex(girl_name="", partner_name="", dance_num=0):
        girl_value = str(girl_name or "")
        partner_value = str(partner_name or "")
        dance_need = _sexevents_int(dance_num, 0) + 1
        for index, row in enumerate(GirlDance, start=1):
            if str(row.get("GirlName", "") or "") != girl_value:
                continue
            if str(row.get("PartnerName", "") or "") != partner_value:
                continue
            if _sexevents_int(row.get("DanceNum", 0), 0) != dance_need:
                continue
            return index
        return -1

    def GirlDance_PopFirst():
        if not GirlDance:
            return {}
        return GirlDance.pop(0)

    def GirlDance_DeleteGirl(girl_name=""):
        girl_value = str(girl_name or "")
        GirlDance[:] = [
            row for row in GirlDance
            if str(row.get("GirlName", "") or "") != girl_value
        ]
        return 0

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

        row = GirlDance.pop(row_index - 1)
        if str(GirlNameSE or "") == "amanda":
            DanceWatchLine[6] = str(row.get("GoPhrase", "") or "")
            Amanda.set_var_int("LegareGo", _sexevents_int(row.get("GoOut", 0), 0))

        return row_index

    def GetDanceJustLeft(GirlNameSE, PartnerNameSE, DanceNumSE):
        prev_dance_num = _sexevents_int(DanceNumSE, 0) - 1
        row_index = GirlDance_FindIndex(GirlNameSE, PartnerNameSE, prev_dance_num)
        if row_index <= 0:
            return 0

        row = GirlDance[row_index - 1]
        if str(GirlNameSE or "") == "amanda" and _sexevents_int(row.get("GoOut", 0), 0) == 1:
            GirlDance.pop(row_index - 1)
            return row_index
        return 0

    def GetLastSexDays(GirlNameSE, DudeNameSE="", CumTargetSE="", SignSE=""):
        dude_value = _sexevents_normalize_dude_name(DudeNameSE).lower()
        cum_value = str(CumTargetSE or "").lower()
        sign_value = str(SignSE or "")
        tmp_cur_day = 0

        for row in sex_history_rows(GirlNameSE):
            row_dude = str(row.get("DudeName", "") or "").lower()
            row_cum = str(row.get("CumTarget", "") or "").lower()
            row_day = _sexevents_int(row.get("Day", 0), 0)
            tmp_line_match = 1

            if dude_value != "" and row_dude != dude_value:
                tmp_line_match = 0
            if cum_value != "" and sign_value == "<>" and row_cum == cum_value:
                tmp_line_match = 0
            if cum_value != "" and sign_value != "<>" and row_cum != cum_value:
                tmp_line_match = 0

            if tmp_line_match == 1:
                tmp_cur_day = max(tmp_cur_day, row_day)

        if tmp_cur_day > 0:
            return dayspassed + 1 - tmp_cur_day
        return -1

    def GetSexNum(GirlNameSE, DudeNameSE="", CumTargetSE="", SignSE="", StartDaySE=0):
        dude_value = _sexevents_normalize_dude_name(DudeNameSE).lower()
        cum_value = str(CumTargetSE or "").lower()
        sign_value = str(SignSE or "")
        start_day_value = _sexevents_int(StartDaySE, 0)
        count_sex = 0

        for row in sex_history_rows(GirlNameSE):
            row_dude = str(row.get("DudeName", "") or "").lower()
            row_cum = str(row.get("CumTarget", "") or "").lower()
            row_day = _sexevents_int(row.get("Day", 0), 0)
            tmp_line_match = 1

            if dude_value != "" and row_dude != dude_value:
                tmp_line_match = 0
            if cum_value != "" and sign_value == "<>" and row_cum == cum_value:
                tmp_line_match = 0
            if cum_value != "" and sign_value != "<>" and row_cum != cum_value:
                tmp_line_match = 0
            if start_day_value > 0 and row_day < start_day_value + 1:
                tmp_line_match = 0

            if tmp_line_match == 1:
                count_sex += 1

        return count_sex

    def dyneval_CheckIfEventAlreadyExist(*ArgsSE, **KwArgsSE):
        return CheckIfEventAlreadyExist(*ArgsSE, **KwArgsSE)
