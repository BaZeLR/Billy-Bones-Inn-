init -25 python:
    import re
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


    def _daily_camel_to_snake(name):
        text = str(name or "").strip()
        if text == "":
            return ""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


    def _daily_extract_label_name(event_code):
        code = str(event_code or "").strip()
        if code == "":
            return ""

        if renpy.has_label(code):
            return code

        code_norm = code.replace("''", "'").replace('""', '"')
        lowered = code_norm.lower()
        if lowered.startswith("gt ") or lowered.startswith("gs "):
            code_norm = code_norm[2:].strip()

        if code_norm.startswith("'"):
            quote_pos = code_norm.find("'", 1)
            if quote_pos > 1:
                code_norm = code_norm[1:quote_pos].strip()
        elif code_norm.startswith('"'):
            quote_pos = code_norm.find('"', 1)
            if quote_pos > 1:
                code_norm = code_norm[1:quote_pos].strip()
        else:
            code_norm = code_norm.split(",", 1)[0].strip()
            code_norm = code_norm.split(" ", 1)[0].strip()

        if renpy.has_label(code_norm):
            return code_norm

        snake_name = _daily_camel_to_snake(code_norm)
        if snake_name != "" and renpy.has_label(snake_name):
            return snake_name

        return ""


    def _daily_dispatch_args(label_name, girl_name="", cur_loc=""):
        label = str(label_name or "").strip()
        girl = str(girl_name or "")
        loc = str(cur_loc or "")

        zero_arg_labels = {
            "BeckyQuestInit",
            "UITestDailyEventSinkZero",
        }
        one_arg_labels = {
            "MorningSickness",
            "GiveBirth",
            "MomDressComplaint",
            "DressNoShow",
            "UITestDailyEventSinkOne",
        }

        if label in zero_arg_labels:
            return ()
        if label in one_arg_labels:
            return (girl,)
        if girl != "" and loc != "":
            return (girl, loc)
        if girl != "":
            return (girl,)
        if loc != "":
            return (loc,)
        return ()


    def DailyEventsList_Add(girl_name="", location_name="", event_time=0, time_check_expr="=", chance_to_meet=1, keep_next_day=0, event_type="", event_code=""):
        DailyEventsList.append({
            "GirlName": str(girl_name or ""),
            "Location": str(location_name or ""),
            "Time": _daily_int(event_time, 0),
            "TimeCheckExpr": str(time_check_expr or "="),
            "ChanceToMeet": max(1, _daily_int(chance_to_meet, 1)),
            "KeepNextDay": _daily_int(keep_next_day, 0),
            "EventType": str(event_type or ""),
            "EventCode": str(event_code or ""),
        })
        return len(DailyEventsList)


    def DailyEventsList_Exists(girl_name="", event_type="", location_name=""):
        filter_girl = str(girl_name or "").strip()
        filter_event_type = str(event_type or "").strip()
        filter_location = str(location_name or "").strip().lower()

        for row in DailyEventsList:
            row_girl = str(row.get("GirlName", "") or "").strip()
            row_event = str(row.get("EventType", "") or "").strip()
            row_loc = str(row.get("Location", "") or "").strip().lower()

            if filter_girl != "" and row_girl != filter_girl:
                continue
            if filter_event_type != "" and row_event != filter_event_type:
                continue
            if filter_location != "" and row_loc not in ("alllocs", filter_location):
                continue
            return 1

        return 0


    def CheckDailyEventExists(girl_name="", event_type="", location=""):
        return DailyEventsList_Exists(girl_name, event_type, location)


    def DailyEventsList_Delete(girl_name="", event_type="", location_name=""):
        filter_girl = str(girl_name or "").strip().lower()
        filter_event_type = str(event_type or "").strip()
        filter_location = str(location_name or "").strip().lower()

        DailyEventsList[:] = [
            row for row in DailyEventsList
            if not (
                (filter_girl == "" or str(row.get("GirlName", "") or "").strip().lower() == filter_girl)
                and (filter_event_type == "" or str(row.get("EventType", "") or "").strip() == filter_event_type)
                and (filter_location == "" or str(row.get("Location", "") or "").strip().lower() in ("alllocs", filter_location))
            )
        ]
        return 0


    def DeleteDailyEvent(girl_name="", event_type="", location=""):
        return DailyEventsList_Delete(girl_name, event_type, location)


    def DailyEventsList_PopMatch(girl_name=None, event_type=None, cur_loc=None, cur_time=None):
        filter_girl = str(girl_name or "").strip()
        filter_event_type = str(event_type or "").strip()
        current_loc = str(cur_loc or "").strip()
        current_loc_l = current_loc.lower()
        current_time = _daily_int(cur_time, 0)

        for index, row in enumerate(DailyEventsList):
            row_girl = str(row.get("GirlName", "") or "").strip()
            row_loc = str(row.get("Location", "") or "").strip()
            row_loc_l = row_loc.lower()
            row_time = row.get("Time", 0)
            row_time_expr = row.get("TimeCheckExpr", "=")
            row_chance = max(1, _daily_int(row.get("ChanceToMeet", 1), 1))
            row_event_type = str(row.get("EventType", "") or "").strip()

            if filter_girl != "" and row_girl != filter_girl:
                continue
            if filter_event_type != "" and row_event_type != filter_event_type:
                continue
            if row_loc_l != "" and row_loc_l != "alllocs" and row_loc_l != current_loc_l:
                continue
            if not _daily_match_time(current_time, row_time, row_time_expr):
                continue
            if renpy.random.randint(1, row_chance) != 1:
                continue

            return DailyEventsList.pop(index)

        return {}


    def DailyEventsList_EndDayUpdate(week_value):
        index = 0
        while index < len(DailyEventsList):
            row = DailyEventsList[index]
            keep_next_day = _daily_int(row.get("KeepNextDay", 0), 0)
            event_type = str(row.get("EventType", "") or "")
            girl_name = str(row.get("GirlName", "") or "")

            if keep_next_day < 0:
                DailyEventsList.pop(index)
                continue

            row["KeepNextDay"] = keep_next_day - 1
            if event_type == "DressNoShow":
                row["Time"] = -1

            if event_type == "BuyDressTom" and week_value != 6:
                DailyEventsList_Add(girl_name, "dressshop", 0, "=", 1, 1 if week_value == 6 else 0, "BuyDress", "GirlDressBuy")
                DailyEventsList_Add(girl_name, "alllocs", 0, ">", 1, 5 + renpy.random.randint(1, 5), "DressNoShow", "DressNoShow")
                DailyEventsList.pop(index)
                continue

            index += 1

        return 0


label check_daily_event(girlname=None, eventtype=None, curloc=None, checktime=None):
    $ _story_event_type = str(eventtype or "")
    if _story_event_type.startswith("_story_"):
        python:
            try:
                _story_find_available = findAvailableEvents
            except NameError:
                _story_find_available = None
            _story_triggers_label_exists = renpy.has_label("checkTriggers")
            if callable(_story_find_available):
                _story_find_available(True)
        if _story_triggers_label_exists:
            call checkTriggers(curloc if curloc is not None else CurLoc, _story_event_type[7:], 0)
        return 0

    python:
        _daily_found = 0
        _daily_event_label = ""
        _daily_call_args = ()
        _daily_event_girl = ""
        _daily_event_loc = ""
        _daily_row = DailyEventsList_PopMatch(girlname, eventtype, curloc if curloc is not None else CurLoc, checktime if checktime is not None else time)

        if _daily_row:
            SignalBlockTime = 1
            _daily_found = 1
            _daily_event_label = _daily_extract_label_name(_daily_row.get("EventCode", ""))
            _daily_event_girl = str(_daily_row.get("GirlName", "") or "")
            _daily_event_loc = str((curloc if curloc is not None else CurLoc) or "").lower()
            _daily_call_args = _daily_dispatch_args(_daily_event_label, _daily_event_girl, _daily_event_loc)
            Result = _daily_found
        else:
            Result = 0

    if _daily_found and _daily_event_label != "":
        if len(_daily_call_args) <= 0:
            call expression _daily_event_label
        elif len(_daily_call_args) == 1:
            call expression _daily_event_label pass (_daily_call_args[0],)
        elif len(_daily_call_args) == 2:
            call expression _daily_event_label pass (_daily_call_args[0], _daily_call_args[1])
        elif len(_daily_call_args) == 3:
            call expression _daily_event_label pass (_daily_call_args[0], _daily_call_args[1], _daily_call_args[2])
        else:
            call expression _daily_event_label pass (_daily_call_args[0], _daily_call_args[1], _daily_call_args[2], _daily_call_args[3])
    return _daily_found


label CheckDailyEvent(girlname=None, eventtype=None, curloc=None, checktime=None):
    call check_daily_event(girlname, eventtype, curloc, checktime)
    return

