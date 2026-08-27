# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -25 python:
    import renpy.exports as renpy

    def _daily_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default


    def _daily_match_time(cur_time, row_time, op_expr):
        op = str(op_expr or "=").strip()
        if op == "==":
            op = "="
        if op == "!=":
            op = "<>"

        left = _daily_int(cur_time, 0)
        right = _daily_int(row_time, 0)

        if op == "=":
            return left == right
        if op == "<>":
            return left != right
        if op == ">":
            return left > right
        if op == "<":
            return left < right
        if op == ">=":
            return left >= right
        if op == "<=":
            return left <= right
        return left == right


    class DailyEventRuntime(object):
        def __init__(self, rows=None):
            self.rows = list(rows or [])

        def add(self, girl_name="", location_name="", event_time=0, time_check_expr="=", chance_to_meet=1, keep_next_day=0, event_type="", event_code="", call_mode="none"):
            self.rows.append({
                "GirlName": str(girl_name or ""),
                "Location": str(location_name or ""),
                "Time": _daily_int(event_time, 0),
                "TimeCheckExpr": str(time_check_expr or "="),
                "ChanceToMeet": max(1, _daily_int(chance_to_meet, 1)),
                "KeepNextDay": _daily_int(keep_next_day, 0),
                "EventType": str(event_type or ""),
                "EventCode": str(event_code or ""),
                "CallMode": str(call_mode or "none"),
            })
            return len(self.rows)

        def exists(self, girl_name="", event_type="", location_name="", current_time=None):
            filter_girl = str(girl_name or "").strip()
            filter_event_type = str(event_type or "").strip()
            filter_location = str(location_name or "").strip().lower()
            for row in self.rows:
                row_girl = str(row.get("GirlName", "") or "").strip()
                row_event = str(row.get("EventType", "") or "").strip()
                row_loc = str(row.get("Location", "") or "").strip().lower()
                if filter_girl != "" and row_girl != filter_girl:
                    continue
                if filter_event_type != "" and row_event != filter_event_type:
                    continue
                if filter_location != "" and row_loc not in ("", "alllocs", filter_location):
                    continue
                if current_time is not None and not _daily_match_time(current_time, row.get("Time", 0), row.get("TimeCheckExpr", "=")):
                    continue
                return 1
            return 0

        def delete(self, girl_name="", event_type="", location_name=""):
            filter_girl = str(girl_name or "").strip().lower()
            filter_event_type = str(event_type or "").strip()
            filter_location = str(location_name or "").strip().lower()
            self.rows[:] = [
                row for row in self.rows
                if not (
                    (filter_girl == "" or str(row.get("GirlName", "") or "").strip().lower() == filter_girl)
                    and (filter_event_type == "" or str(row.get("EventType", "") or "").strip() == filter_event_type)
                    and (filter_location == "" or str(row.get("Location", "") or "").strip().lower() in ("alllocs", filter_location))
                )
            ]
            return 0

        def pop_match(self, girl_name=None, event_type=None, cur_loc=None, cur_time=None):
            filter_girl = str(girl_name or "").strip()
            filter_event_type = str(event_type or "").strip()
            current_loc_l = str(cur_loc or "").strip().lower()
            current_time = _daily_int(cur_time, 0)
            for index, row in enumerate(self.rows):
                row_girl = str(row.get("GirlName", "") or "").strip()
                row_loc_l = str(row.get("Location", "") or "").strip().lower()
                row_chance = max(1, _daily_int(row.get("ChanceToMeet", 1), 1))
                row_event_type = str(row.get("EventType", "") or "").strip()
                if filter_girl != "" and row_girl != filter_girl:
                    continue
                if filter_event_type != "" and row_event_type != filter_event_type:
                    continue
                if filter_event_type == "" and row_event_type == "MorningSickness":
                    continue
                if row_loc_l not in ("", "alllocs", current_loc_l):
                    continue
                if not _daily_match_time(current_time, row.get("Time", 0), row.get("TimeCheckExpr", "=")):
                    continue
                if procedural_randint(1, row_chance, key="procedural:Utilities/General/Common/CheckDailyEvent.rpy:procedural_randint:201:1") != 1:
                    continue
                return self.rows.pop(index)
            return {}

        def end_day(self, week_value):
            index = 0
            while index < len(self.rows):
                row = self.rows[index]
                keep_next_day = _daily_int(row.get("KeepNextDay", 0), 0)
                event_type = str(row.get("EventType", "") or "")
                girl_name = str(row.get("GirlName", "") or "")
                if keep_next_day < 0:
                    self.rows.pop(index)
                    continue
                row["KeepNextDay"] = keep_next_day - 1
                if event_type == "DressNoShow":
                    row["Time"] = -1
                if event_type == "BuyDressTom" and week_value != 7:
                    self.add(girl_name, "dressshop", 0, "=", 1, 0, "BuyDress", "GirlDressBuy", "girl_location")
                    self.add(girl_name, "alllocs", 0, ">", 1, 5 + procedural_randint(1, 5, key="procedural:Utilities/General/Common/CheckDailyEvent.rpy:procedural_randint:227:2"), "DressNoShow", "DressNoShow", "girl")
                    self.rows.pop(index)
                    continue
                index += 1
            return 0


default daily_events = DailyEventRuntime()


label check_daily_event(girlname=None, eventtype=None, curloc=None, checktime=None):
    $ renpy.dynamic("_daily_found", "_daily_event_label", "_daily_event_girl", "_daily_event_loc", "_daily_call_mode", "_daily_row")
    python:
        _daily_found = 0
        _daily_event_label = ""
        _daily_event_girl = ""
        _daily_event_loc = ""
        _daily_call_mode = "none"
        _daily_row = daily_events.pop_match(girlname, eventtype, curloc if curloc is not None else rooms.current_code, checktime if checktime is not None else calendar_v2.time_slot())

        if _daily_row:
            _daily_found = 1
            _daily_event_label = str(_daily_row.get("EventCode", "") or "").strip()
            _daily_event_girl = str(_daily_row.get("GirlName", "") or "")
            _daily_event_loc = str((curloc if curloc is not None else rooms.current_code) or "").lower()
            _daily_call_mode = str(_daily_row.get("CallMode", "none") or "none")
            if not renpy.has_label(_daily_event_label):
                _daily_event_label = ""
    if _daily_found and _daily_event_label != "":
        if _daily_call_mode == "girl_location":
            call expression _daily_event_label pass (_daily_event_girl, _daily_event_loc)
        elif _daily_call_mode == "girl":
            call expression _daily_event_label pass (_daily_event_girl,)
        else:
            call expression _daily_event_label
    return _daily_found



