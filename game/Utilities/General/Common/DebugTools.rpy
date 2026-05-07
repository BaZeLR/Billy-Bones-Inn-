# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    import renpy.exports as renpy

    def _dbg_i(v, d=0):
        try:
            return int(v)
        except Exception:
            return d

    def _dbg_get(name, default=None):
        key = str(name or "")
        try:
            if key == "time":
                return time
            if key == "week":
                return week
            if key == "day":
                return day
            if key == "EventsCount":
                return EventsCount
            if key == "NewEvents":
                return NewEvents
            if key == "_mui_location_char_keys":
                return _mui_location_char_keys
            if key == "_mui_dialog_rows":
                return _mui_dialog_rows
            if key == "build_tavern_events_queue_python":
                return build_tavern_events_queue_python
            if key == "ensure_default_tavern_jobs":
                return ensure_default_tavern_jobs
            if key == "DisplayTavernEventShort":
                return DisplayTavernEventShort
        except NameError:
            return default
        return default

    def _dbg_set(name, value):
        global time, week, day, EventsCount, NewEvents
        key = str(name or "")
        if key == "time":
            calendar_set_time_slot(value)
        elif key == "week":
            week = value
            calendar_sync_state()
        elif key == "day":
            day = value
            calendar_sync_state()
        elif key == "EventsCount":
            EventsCount = value
        elif key == "NewEvents":
            NewEvents = value
        return value

    def _dbg_del(name):
        key = str(name or "")
        if key == "time":
            _dbg_set("time", 0)
        elif key == "week":
            _dbg_set("week", 1)
        elif key == "day":
            _dbg_set("day", 1)
        elif key == "EventsCount":
            _dbg_set("EventsCount", {})
        elif key == "NewEvents":
            _dbg_set("NewEvents", {})

    def _dbg_ensure_event_maps():
        ecount = _dbg_get("EventsCount", None)
        if not isinstance(ecount, dict):
            ecount = _dbg_set("EventsCount", {})
        nevents = _dbg_get("NewEvents", None)
        if not isinstance(nevents, dict):
            nevents = _dbg_set("NewEvents", {})
        return ecount, nevents

    def _dbg_queue_for_period(period):
        out = []
        try:
            p = _dbg_i(period, 0)
            ecount, nevents = _dbg_ensure_event_maps()
            if not isinstance(ecount, dict) or not isinstance(nevents, dict):
                return out
            cnt = max(0, _dbg_i(ecount.get(p, 0), 0))
            for idx in range(cnt):
                code = str(nevents.get(str(p) + "_" + str(idx), "") or "")
                if code:
                    out.append(code)
        except Exception:
            return out
        return out

    def _dbg_build_queue(include_mandatory=True):
        builder = _dbg_get("build_tavern_events_queue_python", None)
        if callable(builder):
            builder(bool(include_mandatory))
            return True
        _dbg_ensure_event_maps()
        return False

    def _dbg_queue_day_map():
        out = {}
        for period in (10, 0, 1, 2, 3, 4):
            out[int(period)] = list(_dbg_queue_for_period(period))
        return out

    def _dbg_ensure_queue_for_debug():
        """
        Build queue for debug visibility. If RNG yields empty day, inject one
        known random event so debug UI always has something to show/dispatch.
        """
        _dbg_build_queue(True)
        day_map = _dbg_queue_day_map()
        total = 0
        for period in (10, 0, 1, 2, 3, 4):
            total += len(day_map.get(period, []))
        if total > 0:
            return day_map

        # Deterministic fallback for debug-only visibility.
        ecount, nevents = _dbg_ensure_event_maps()
        period = _dbg_i(_dbg_get("time", 0), 0)
        if period < 0 or period > 4:
            period = 0
        ecount[period] = 1
        nevents[str(period) + "_0"] = "CleaningHarass"
        return _dbg_queue_day_map()

    def _dbg_image_exists(*paths):
        for p in paths:
            if str(p or "").strip() and renpy.loadable(str(p)):
                return True
        return False

    def debug_shop_flow_probe():
        """
        Validate shop/location dialog wiring for:
        GroceryStore, WineStore, DressShop, StolyarWorkshop.
        """
        result = {"ok": True, "lines": []}
        prev_time = _dbg_get("time", 0)
        prev_week = _dbg_get("week", 1)
        try:
            keys_fn = _dbg_get("_mui_location_char_keys", None)
            rows_fn = _dbg_get("_mui_dialog_rows", None)
            if not callable(keys_fn) or not callable(rows_fn):
                return {"ok": False, "lines": ["UI dialog helpers not found."]}

            checks = [
                ("Grocery morning", "GroceryStore", 0, 1, "eddie", "IntEddieTalk"),
                ("Grocery day", "GroceryStore", 1, 1, "becky", "IntBeckyTalk"),
                ("Wine morning", "WineStore", 0, 1, "clara", "IntClaraTalk"),
                ("Wine day", "WineStore", 1, 1, "alber", "IntAlberTalk"),
                ("Tailor", "DressShop", 1, 1, "irma", "IntIrmaTalk"),
                ("Carpenter", "StolyarWorkshop", 1, 1, "draupnir", "IntDraupnirTalk"),
            ]
            for title, loc, slot, week_val, char_key, talk_label in checks:
                _dbg_set("time", int(slot))
                _dbg_set("week", int(week_val))
                present = char_key in set(keys_fn(loc))
                dialog = rows_fn(loc, char_key)
                rows = list(dialog.get("rows", []) or [])
                talk_ok = any(
                    str(r.get("kind", "")) == "call_label_args"
                    and str(r.get("value", "")) == str(talk_label)
                    for r in rows
                )
                label_ok = bool(renpy.has_label(str(talk_label)))
                passed = bool(present and talk_ok and label_ok)
                if not passed:
                    result["ok"] = False
                result["lines"].append(
                    "[%s] %s | present=%s talk_row=%s label=%s"
                    % (("PASS" if passed else "FAIL"), title, str(present), str(talk_ok), str(label_ok))
                )

            image_checks = [
                ("Grocery image", _dbg_image_exists("images/eddie/portraits/portrait_1.png", "images/becky/portraits/portrait_1.png")),
                ("Wine image", _dbg_image_exists("images/clara/portrait1.jpg", "images/Alber/portrait7.jpg", "images/alber/portrait7.jpg")),
                ("Tailor image", _dbg_image_exists("images/irma/portraits/portrait1.jpg")),
                ("Carpenter image", _dbg_image_exists("images/draupnir/dwarf1.jpg")),
            ]
            for title, ok in image_checks:
                if not ok:
                    result["ok"] = False
                result["lines"].append("[%s] %s" % (("PASS" if ok else "FAIL"), title))

        except Exception as ex:
            result["ok"] = False
            result["lines"].append("ERROR: " + str(ex))
        finally:
            _dbg_set("time", prev_time)
            _dbg_set("week", prev_week)
        return result

    def debug_tavern_events_strict_assert():
        """
        Deterministic assertion flow requested by user.
        Mirrors queue build/dispatch checks:
        - seed RNG
        - force time/week/day
        - build queue
        - assert queue exists
        - dispatch once and assert decrement happened
        """
        # Keep previous values so gameplay state is not polluted by debug check.
        prev_time = _dbg_get("time", None)
        prev_week = _dbg_get("week", None)
        prev_day = _dbg_get("day", None)
        prev_events_count = _dbg_get("EventsCount", None)
        prev_new_events = _dbg_get("NewEvents", None)

        try:
            # 1) deterministic setup
            renpy.random.seed(123)
            _dbg_set("time", 0)
            _dbg_set("week", 1)
            _dbg_set("day", 1)
            ecount, nevents = _dbg_ensure_event_maps()

            # 2) build queue
            _dbg_build_queue(True)

            # 3) verify queue exists
            assert isinstance(ecount, dict)
            assert isinstance(nevents, dict)
            assert int(ecount.get(_dbg_get("time", 0), 0)) > 0 or int(ecount.get(10, 0)) > 0

            # 4) dispatch one event and verify decrement
            b_t = int(ecount.get(_dbg_get("time", 0), 0))
            b_m = int(ecount.get(10, 0))
            _dbg_dispatch_unused = _dbg_get("DisplayTavernEventShort", lambda *_args, **_kwargs: "")(_dbg_get("time", 0), 1)
            a_t = int(ecount.get(_dbg_get("time", 0), 0))
            a_m = int(ecount.get(10, 0))
            assert (a_t == b_t - 1) or (a_m == b_m - 1)

            q_today = _dbg_queue_for_period(_dbg_get("time", 0))
            q_mand = _dbg_queue_for_period(10)
            renpy.log("STRICT DBG Tavern queue for today (slot 0):")
            if q_today:
                for idx, ev in enumerate(q_today):
                    renpy.log("  [" + str(idx) + "] " + str(ev))
            else:
                renpy.log("  <empty>")
            renpy.log("STRICT DBG Tavern mandatory queue (slot 10):")
            if q_mand:
                for idx, ev in enumerate(q_mand):
                    renpy.log("  [" + str(idx) + "] " + str(ev))
            else:
                renpy.log("  <empty>")

            return {
                "ok": True,
                "before_cur": b_t,
                "before_mandatory": b_m,
                "after_cur": a_t,
                "after_mandatory": a_m,
                "queue_today": q_today,
                "queue_mandatory": q_mand,
            }
        finally:
            # Restore state.
            if prev_time is None:
                _dbg_del("time")
            else:
                _dbg_set("time", prev_time)
            if prev_week is None:
                _dbg_del("week")
            else:
                _dbg_set("week", prev_week)
            if prev_day is None:
                _dbg_del("day")
            else:
                _dbg_set("day", prev_day)

            if isinstance(prev_events_count, dict):
                _dbg_set("EventsCount", prev_events_count)
            else:
                _dbg_del("EventsCount")
            if isinstance(prev_new_events, dict):
                _dbg_set("NewEvents", prev_new_events)
            else:
                _dbg_del("NewEvents")

    def debug_tavern_events_probe(run_dispatch=True):
        result = {
            "ok": True,
            "error": "",
            "time": _dbg_i(_dbg_get("time", 0), 0),
            "before_cur": 0,
            "before_mandatory": 0,
            "after_build_cur": 0,
            "after_build_mandatory": 0,
            "after_dispatch_cur": 0,
            "after_dispatch_mandatory": 0,
            "dispatch_text": "",
            "queue_today": [],
            "queue_mandatory": [],
        }
        try:
            ensure_jobs = _dbg_get("ensure_default_tavern_jobs", None)
            if callable(ensure_jobs):
                ensure_jobs(False)

            ecount, _dbg_unused_events = _dbg_ensure_event_maps()

            t = result["time"]
            result["before_cur"] = _dbg_i(ecount.get(t, 0), 0)
            result["before_mandatory"] = _dbg_i(ecount.get(10, 0), 0)

            _dbg_build_queue(True)

            result["after_build_cur"] = _dbg_i(ecount.get(t, 0), 0)
            result["after_build_mandatory"] = _dbg_i(ecount.get(10, 0), 0)
            result["queue_today"] = _dbg_queue_for_period(t)
            result["queue_mandatory"] = _dbg_queue_for_period(10)

            if run_dispatch:
                dispatcher = _dbg_get("DisplayTavernEventShort", None)
                if callable(dispatcher):
                    result["dispatch_text"] = str(dispatcher(t, 1) or "")
                else:
                    result["dispatch_text"] = "DisplayTavernEventShort not found."

            result["after_dispatch_cur"] = _dbg_i(ecount.get(t, 0), 0)
            result["after_dispatch_mandatory"] = _dbg_i(ecount.get(10, 0), 0)

        except Exception as ex:
            result["ok"] = False
            result["error"] = str(ex)
        return result

    def debug_tavern_events_snapshot_fn():
        """
        Console-safe snapshot test without label calls.
        Use from console:
            store.debug_tavern_events_snapshot_fn()
        """
        renpy.random.seed(123)
        _dbg_set("time", 0)
        _dbg_set("week", 1)
        _dbg_set("day", 1)
        _dbg_ensure_event_maps()

        _dbg_build_queue(True)

        t = _dbg_i(_dbg_get("time", 0), 0)
        snap = {
            "time": t,
            "events_count": dict(_dbg_get("EventsCount", {})),
            "today_queue": _dbg_queue_for_period(t),
            "mandatory_queue": _dbg_queue_for_period(10),
        }
        renpy.log("SNAPSHOT today queue: " + (", ".join(snap["today_queue"]) if snap["today_queue"] else "<empty>"))
        renpy.log("SNAPSHOT mandatory queue: " + (", ".join(snap["mandatory_queue"]) if snap["mandatory_queue"] else "<empty>"))
        return snap

    def debug_tavern_events_unit_fn():
        """
        Console-safe deterministic unit check.
        Use from console:
            store.debug_tavern_events_unit_fn()
        """
        renpy.random.seed(123)
        _dbg_set("time", 0)
        _dbg_set("week", 1)
        _dbg_set("day", 1)
        ecount, nevents = _dbg_ensure_event_maps()

        _dbg_build_queue(True)

        assert isinstance(ecount, dict)
        assert isinstance(nevents, dict)
        t = _dbg_i(_dbg_get("time", 0), 0)
        assert int(ecount.get(t, 0)) > 0 or int(ecount.get(10, 0)) > 0

        b_t = int(ecount.get(t, 0))
        b_m = int(ecount.get(10, 0))
        _dbg_dispatch_unused = _dbg_get("DisplayTavernEventShort", lambda *_args, **_kwargs: "")(t, 1)
        a_t = int(ecount.get(t, 0))
        a_m = int(ecount.get(10, 0))
        assert (a_t == b_t - 1) or (a_m == b_m - 1)

        out = {
            "ok": True,
            "before_cur": b_t,
            "before_mandatory": b_m,
            "after_cur": a_t,
            "after_mandatory": a_m,
            "today_queue": _dbg_queue_for_period(t),
            "mandatory_queue": _dbg_queue_for_period(10),
        }
        renpy.log("UNIT PASS: " + repr(out))
        return out

    # Simple console aliases (no label names needed).
    def dbg_events_queue():
        return debug_tavern_events_snapshot_fn()

    def dbg_events_unit():
        return debug_tavern_events_unit_fn()


label debug_tavern_events_check:
    python:
        _r = debug_tavern_events_probe(True)
        _lines = []
        _lines.append("DEBUG: Tavern events check")
        _lines.append("time slot = " + str(_r.get("time", 0)))
        _lines.append("before build: cur=" + str(_r.get("before_cur", 0)) + ", mandatory=" + str(_r.get("before_mandatory", 0)))
        _lines.append("after build: cur=" + str(_r.get("after_build_cur", 0)) + ", mandatory=" + str(_r.get("after_build_mandatory", 0)))
        _lines.append("after dispatch: cur=" + str(_r.get("after_dispatch_cur", 0)) + ", mandatory=" + str(_r.get("after_dispatch_mandatory", 0)))
        _q_today = list(_r.get("queue_today", []) or [])
        _q_mand = list(_r.get("queue_mandatory", []) or [])
        _lines.append("queue today (" + str(len(_q_today)) + "): " + (", ".join(_q_today) if _q_today else "<empty>"))
        _lines.append("queue mandatory (" + str(len(_q_mand)) + "): " + (", ".join(_q_mand) if _q_mand else "<empty>"))
        _dispatch = str(_r.get("dispatch_text", "") or "").strip()
        if _dispatch:
            _lines.append("dispatch text:")
            _lines.append(_dispatch)
        else:
            _lines.append("dispatch text: <empty>")
        if not bool(_r.get("ok", True)):
            _lines.append("ERROR: " + str(_r.get("error", "")))
        _msg = "\n".join(_lines)
        renpy.log("DBG Tavern queue for today (slot " + str(_r.get("time", 0)) + "):")
        if _q_today:
            for _idx, _ev in enumerate(_q_today):
                renpy.log("  [" + str(_idx) + "] " + str(_ev))
        else:
            renpy.log("  <empty>")
        renpy.log("DBG Tavern mandatory queue (slot 10):")
        if _q_mand:
            for _idx, _ev in enumerate(_q_mand):
                renpy.log("  [" + str(_idx) + "] " + str(_ev))
        else:
            renpy.log("  <empty>")
    "[_msg]"
    return


label debug_tavern_events_check_strict:
    python:
        try:
            _r = debug_tavern_events_strict_assert()
            _msg = (
                "STRICT DEBUG: PASS\n"
                + "before: cur=" + str(_r.get("before_cur", 0)) + ", mandatory=" + str(_r.get("before_mandatory", 0)) + "\n"
                + "after: cur=" + str(_r.get("after_cur", 0)) + ", mandatory=" + str(_r.get("after_mandatory", 0)) + "\n"
                + "queue today (" + str(len(_r.get("queue_today", []) or [])) + "): "
                + (", ".join(_r.get("queue_today", []) or []) or "<empty>") + "\n"
                + "queue mandatory (" + str(len(_r.get("queue_mandatory", []) or [])) + "): "
                + (", ".join(_r.get("queue_mandatory", []) or []) or "<empty>")
            )
        except Exception as ex:
            _msg = "STRICT DEBUG: FAIL\n" + str(ex)
    "[_msg]"
    return


label debug_tavern_events_build_only:
    python:
        _r = debug_tavern_events_probe(False)
        _msg = (
            "DEBUG build only\n"
            + "slot: " + str(_r.get("time", 0)) + "\n"
            + "before: cur=" + str(_r.get("before_cur", 0)) + ", mandatory=" + str(_r.get("before_mandatory", 0)) + "\n"
            + "after: cur=" + str(_r.get("after_build_cur", 0)) + ", mandatory=" + str(_r.get("after_build_mandatory", 0))
        )
        if not bool(_r.get("ok", True)):
            _msg += "\nERROR: " + str(_r.get("error", ""))
    "[_msg]"
    return


label debug_tavern_events_day_queue:
    python:
        _day = _dbg_ensure_queue_for_debug()
        _parts = []
        _parts.append("DEBUG day queue (10,0..4):")
        for _period in (10, 0, 1, 2, 3, 4):
            _evs = list(_day.get(_period, []) or [])
            _parts.append(
                "slot %s (%d): %s"
                % (str(_period), len(_evs), (", ".join(_evs) if _evs else "<empty>"))
            )
            renpy.log(
                "DBG day queue slot "
                + str(_period)
                + ": "
                + (", ".join(_evs) if _evs else "<empty>")
            )
        _msg = "\n".join(_parts)
    "[_msg]"
    return


label debug_tavern_event_live_once:
    python:
        _dbg_ensure_queue_for_debug()
        _ecount, _dbg_unused_events = _dbg_ensure_event_maps()
        _slot = _dbg_i(_dbg_get("time", 0), 0)
        _b_cur = _dbg_i(_ecount.get(_slot, 0), 0)
        _b_m = _dbg_i(_ecount.get(10, 0), 0)
    call DisplayTavernEventShort(time, 1)
    $ _event_txt = str(_return or "")
    python:
        _ecount, _dbg_unused_events = _dbg_ensure_event_maps()
        _a_cur = _dbg_i(_ecount.get(_slot, 0), 0)
        _a_m = _dbg_i(_ecount.get(10, 0), 0)
        _msg = (
            "LIVE event dispatch\n"
            + "slot=" + str(_slot) + " before(cur=" + str(_b_cur) + ", mandatory=" + str(_b_m) + ")\n"
            + "after(cur=" + str(_a_cur) + ", mandatory=" + str(_a_m) + ")\n"
            + ("event text:\n" + _event_txt if _event_txt else "event text: <empty>")
        )
    "[_msg]"
    return


label debug_shop_flow_check:
    python:
        _r = debug_shop_flow_probe()
        _head = "DEBUG shops check: " + ("PASS" if bool(_r.get("ok", False)) else "FAIL")
        _msg = _head + "\n" + "\n".join(list(_r.get("lines", []) or []))
    "[_msg]"
    return


label debug_tavern_events_dispatch_once:
    python:
        t = _dbg_i(_dbg_get("time", 0), 0)
        _ecount, _dbg_unused_events = _dbg_ensure_event_maps()
        _before_cur = _dbg_i(_ecount.get(t, 0), 0)
        _before_m = _dbg_i(_ecount.get(10, 0), 0)
        _dispatcher = _dbg_get("DisplayTavernEventShort", None)
        if callable(_dispatcher):
            _text = str(_dispatcher(t, 1) or "")
        else:
            _text = "DisplayTavernEventShort not found."
        _after_cur = _dbg_i(_ecount.get(t, 0), 0)
        _after_m = _dbg_i(_ecount.get(10, 0), 0)
        _msg = (
            "DEBUG dispatch once\n"
            + "before: cur=" + str(_before_cur) + ", mandatory=" + str(_before_m) + "\n"
            + "after: cur=" + str(_after_cur) + ", mandatory=" + str(_after_m) + "\n"
            + ("text:\n" + _text if str(_text).strip() else "text: <empty>")
        )
    "[_msg]"
    return


label DebugTestRoom:
    call EnterLocation("DebugTestRoom")
    python:
        _dbg_desc = "Тестовая комната. Здесь можно проверять таверн-события, показывать картинки и запускать диалоги."
        MainTxt = _dbg_desc
        CurLocDesc = _dbg_desc
        UI_mode = "scene"
        UI_selected_char = ""
        UI_char_dropdown = False

    # Try to present a known safe image for visual checks.
    if renpy.loadable("images/General/LocStreetTavern1.jpg"):
        $ _layout_last_picture = "images/General/LocStreetTavern1.jpg"
    elif renpy.loadable("images/general/LocStreetTavern1.jpg"):
        $ _layout_last_picture = "images/general/LocStreetTavern1.jpg"
    else:
        show bg TavernMain at master

    "Вы в тестовой комнате."

    label debug_test_room_menu:
        menu:
            "Показать очередь событий (все слоты дня)":
                call debug_tavern_events_day_queue
                jump debug_test_room_menu
            "Показать и запустить 1 таверн-событие":
                call debug_tavern_event_live_once
                jump debug_test_room_menu
            "Проверить таверн-события (build + dispatch)":
                call debug_tavern_events_check
                jump debug_test_room_menu
            "Собрать очередь событий (без dispatch)":
                call debug_tavern_events_build_only
                jump debug_test_room_menu
            "Прогнать один dispatch сейчас":
                call debug_tavern_events_dispatch_once
                jump debug_test_room_menu
            "Проверка shop flow (dialog + images)":
                call debug_shop_flow_check
                jump debug_test_room_menu
            "Тест: продуктовая лавка (утро)":
                $ week = 1
                $ calendar_set_time_slot(0)
                jump GroceryStore
            "Тест: винный погребок (утро)":
                $ week = 1
                $ calendar_set_time_slot(0)
                jump WineStore
            "Тест: лавка Ирмы":
                $ week = 1
                $ calendar_set_time_slot(1)
                jump DressShop
            "Тест: мастерская Драупнира":
                $ week = 1
                $ calendar_set_time_slot(1)
                jump StolyarWorkshop
            "Показать портрет Сандры":
                call ShowImageSeq("sandra", "portraits", "portrait", 4)
                jump debug_test_room_menu
            "Показать портрет Мелиссы":
                call ShowImage("melissa", "", "portrait")
                jump debug_test_room_menu
            "Показать портрет Аманды":
                call ShowAmandaPortrait
                jump debug_test_room_menu
            "Диалог Сандры":
                call IntSandraTalk
                jump debug_test_room_menu
            "Диалог Мелиссы":
                call IntMelissaTalk
                jump debug_test_room_menu
            "Диалог Аманды":
                call IntAmandaTalk
                jump debug_test_room_menu
            "Вернуться в трактир":
                jump TavernMain


label debug_test_room:
    jump DebugTestRoom


label debug_tavern_events_snapshot:
    python:
        # Deterministic setup for console/manual verification.
        renpy.random.seed(123)
        _dbg_set("time", 0)
        _dbg_set("week", 1)
        _dbg_set("day", 1)
        _dbg_ensure_event_maps()

    call CreateTavernEvents

    python:
        _t = _dbg_i(_dbg_get("time", 0), 0)
        _snapshot = {
            "time": _t,
            "events_count": dict(_dbg_get("EventsCount", {})),
            "today_queue": _dbg_queue_for_period(_t),
            "mandatory_queue": _dbg_queue_for_period(10),
        }
        _return = _snapshot
    return
