init -45 python:
    import renpy.exports as renpy

    PLAYER_CHORE_KEYS = (
        "bring_woods",
        "chop_wood",
        "make_fire",
        "clean_ashes",
        "boil_water",
        "clean_upstairs_rooms",
    )
    PLAYER_CHORE_TARGET = 3
    PLAYER_CHORE_TARGETS = {
        "bring_woods": 3,
        "chop_wood": 3,
        "make_fire": 3,
        "clean_ashes": 3,
        "boil_water": 7,
        "clean_upstairs_rooms": 3,
    }
    PLAYER_CORE_OTHER_GIRLS = ("amanda", "melissa")

    def _pc_to_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _pc_clamp(value, low, high):
        return max(low, min(high, _pc_to_int(value, low)))

    def _pc_player_has_item(item_id):
        item_key = str(item_id or "").strip()
        if not item_key:
            return False
        return _player_has_item_by_id(item_key)

    def _pc_advance_minutes(minutes_to_add):
        try:
            calendar_advance_minutes(_pc_to_int(minutes_to_add, 0))
        except Exception:
            pass

    def _pc_fire_object(where_id="", object_id=""):
        object_key = get_object_id(object_id)
        if object_key == "kitchen_hearth_001" or str(where_id or "") == "TavernKitchen":
            return TavernKitchenHearthObject
        return TavernMainFireplaceObject

    def _pc_water_object(where_id="", object_id=""):
        return TavernKitchenCauldronObject

    def _pc_room_by_code(where_id=""):
        room_code = str(where_id or getattr(CurrentRoom, "code_name", "") or CurLoc or "").strip()
        if room_code == "TavernKitchen":
            try:
                return TavernKitchenRoom
            except Exception:
                return CurrentRoom
        if room_code == "TavernMain":
            try:
                return TavernMainRoom
            except Exception:
                return CurrentRoom
        return CurrentRoom

    def _pc_calendar_total_minutes():
        calendar_sync_state()
        return max(0, _pc_to_int(dayspassed, 0)) * 1440 + (_pc_to_int(hour, 0) * 60) + _pc_to_int(minute, 0)

    def _pc_fire_until_minute(fire_object):
        if fire_object is None:
            return 0
        until_minute = _object_state_int(fire_object, "fire_until_minute", 0)
        legacy_units = _object_state_int(fire_object, "fire_units", 0)
        if until_minute <= 0 and legacy_units > 0:
            until_minute = _pc_calendar_total_minutes() + (legacy_units * 8 * 60)
            _set_object_state_int(fire_object, "fire_until_minute", until_minute)
            _set_object_state_int(fire_object, "fire_units", 0)
        return until_minute

    def _pc_hot_water_until_minute(water_object):
        if water_object is None:
            return 0
        until_minute = _object_state_int(water_object, "hot_water_until_minute", 0)
        legacy_units = _object_state_int(water_object, "hot_water_units", 0)
        if until_minute <= 0 and legacy_units > 0:
            until_minute = _pc_calendar_total_minutes() + (legacy_units * 24 * 60)
            _set_object_state_int(water_object, "hot_water_until_minute", until_minute)
            _set_object_state_int(water_object, "hot_water_units", 0)
        return until_minute

    def _pc_fire_is_active(fire_object):
        return _pc_fire_until_minute(fire_object) > _pc_calendar_total_minutes()

    def _pc_hot_water_is_ready(water_object):
        return _pc_hot_water_until_minute(water_object) > _pc_calendar_total_minutes()

    def _pc_fire_fuel_available(where_id="", object_id=""):
        room_obj = _pc_room_by_code(where_id)
        fire_object = _pc_fire_object(where_id, object_id)
        return (
            _pc_player_has_item("chopped_wood_001")
            or _room_has_item_by_id(room_obj, "chopped_wood_001")
            or _object_state_int(fire_object, "chopped_wood_stock", 0) > 0
        )

    def _pc_sync_ui_chores():
        UI_chores.clear()
        UI_chores.update({key: int(PlayerChoresWeek.get(key, 0) or 0) for key in PLAYER_CHORE_KEYS})

    def _pc_chore_display_name(chore_key):
        names = {
            "bring_woods": "принести дрова",
            "chop_wood": "наколоть дров",
            "make_fire": "разжечь огонь",
            "clean_ashes": "вычистить золу",
            "boil_water": "вскипятить воду",
            "clean_upstairs_rooms": "убрать комнаты наверху",
        }
        return names.get(str(chore_key or "").strip(), str(chore_key or "").strip())

    def player_chore_target(chore_key):
        key = str(chore_key or "").strip()
        return max(1, _pc_to_int(PLAYER_CHORE_TARGETS.get(key, PLAYER_CHORE_TARGET), PLAYER_CHORE_TARGET))

    def _pc_register_chore_success(chore_key):
        key = str(chore_key or "").strip()
        cur = _pc_to_int(PlayerChoresWeek.get(key, 0), 0)
        PlayerChoresWeek[key] = cur + 1
        _pc_sync_ui_chores()
        return True

    def can_do_player_chore(chore_key, where_id="", object_id=""):
        _ensure_player_chores_state()
        key = str(chore_key or "").strip()
        if key not in PLAYER_CHORE_KEYS:
            return False, "Такого дела сейчас нет."
        if _pc_to_int(fun, 0) < 26:
            return False, "У вас слишком плохое настроение для такой работы."
        if _pc_to_int(energy, 0) <= 0:
            return False, "У вас не осталось сил."
        if key == "bring_woods" and not _pc_player_has_item("old_axe_001"):
            return False, "Без топора идти за дровами бессмысленно."
        if key == "chop_wood":
            if not _pc_player_has_item("old_axe_001"):
                return False, "Без топора колоть дрова не выйдет."
            if not _room_has_item_by_id(ShedRoom, "lumber_001") and not _pc_player_has_item("lumber_001"):
                return False, "Сначала нужно принести бревна."
        if key == "make_fire" and not _pc_fire_fuel_available(where_id, object_id):
            return False, "Нечем топить камин."
        if key == "boil_water":
            if not _pc_fire_is_active(_pc_fire_object(where_id, object_id)):
                return False, "Сначала нужно разжечь огонь."
        return True, ""

    def _ensure_player_chores_state():
        global PlayerChoresWeek, UI_chores, WeeklyVisitorsTrack, WeeklyChoresLastEvalStamp
        global Friends, SandraVar, otkroven, neshlush
        if not isinstance(PlayerChoresWeek, dict):
            PlayerChoresWeek = {}
        for key in PLAYER_CHORE_KEYS:
            PlayerChoresWeek[key] = max(0, _pc_to_int(PlayerChoresWeek.get(key, 0), 0))

        if not isinstance(UI_chores, dict):
            UI_chores = {}
        _pc_sync_ui_chores()

        if not isinstance(WeeklyVisitorsTrack, dict):
            WeeklyVisitorsTrack = {}
        WeeklyVisitorsTrack["sum"] = max(0, _pc_to_int(WeeklyVisitorsTrack.get("sum", 0), 0))
        WeeklyVisitorsTrack["days"] = max(0, _pc_to_int(WeeklyVisitorsTrack.get("days", 0), 0))
        try:
            WeeklyVisitorsTrack["prev_avg"] = float(WeeklyVisitorsTrack.get("prev_avg", 0.0) or 0.0)
        except Exception:
            WeeklyVisitorsTrack["prev_avg"] = 0.0

        if not isinstance(WeeklyChoresLastEvalStamp, str):
            WeeklyChoresLastEvalStamp = str(WeeklyChoresLastEvalStamp)

        if not isinstance(Friends, dict):
            Friends = {}
        if not isinstance(SandraVar, dict):
            SandraVar = {}

        if not isinstance(otkroven, dict):
            otkroven = {}
        if not isinstance(neshlush, dict):
            neshlush = {}
        for girl in PLAYER_CORE_OTHER_GIRLS:
            if girl not in neshlush:
                # Rebel baseline: inverse of current openness (otkroven), clamped.
                neshlush[girl] = max(0, 5 - _pc_to_int(otkroven.get(girl, 0), 0))

    def get_player_chores_ui_state():
        _ensure_player_chores_state()
        return {k: int(PlayerChoresWeek.get(k, 0) or 0) for k in PLAYER_CHORE_KEYS}

    def do_player_chore(chore_key, where_id="", object_id=""):
        global fun, energy, exploration, taverncleanliness
        global ashesdirtydays, upstairsroomsdirty, FightLevel, dayssincewash
        _ensure_player_chores_state()
        key = str(chore_key or "").strip()
        allowed, reason = can_do_player_chore(key, where_id, object_id)
        if not allowed:
            renpy.notify(reason)
            return {"ok": False, "text": reason}

        _pc_register_chore_success(key)

        result_text = ""

        if key == "bring_woods":
            _pc_advance_minutes(8 * 60)
            fun = _pc_clamp(fun + 25, 0, 100)
            energy = _pc_clamp(energy - 40, 0, 100)
            exploration = max(0, _pc_to_int(exploration, 0) + 1)
            taverncleanliness = _pc_clamp(taverncleanliness - 15, 0, 100)
            _room_add_item_by_id(ShedRoom, "lumber_001")
            result_text = "Вы уходите в лес за дровами. К вечеру удается притащить {b}одно крепкое бревно{/b} для хозяйства."
        elif key == "chop_wood":
            if _pc_player_has_item("lumber_001"):
                _player_remove_item_by_id("lumber_001")
            else:
                _room_remove_item_by_id(ShedRoom, "lumber_001")
            _room_add_item_units(ShedRoom, "chopped_wood_001", 10)
            _pc_advance_minutes(60)
            fun = _pc_clamp(fun + 5, 0, 100)
            energy = _pc_clamp(energy - 20, 0, 100)
            exploration = max(0, _pc_to_int(exploration, 0) + 3)
            _total_wood = _room_item_count_by_id(ShedRoom, "chopped_wood_001")
            result_text = "Вы ставите бревно на колоду и рубите его на поленья. В сарае теперь {b}%s{/b} единиц колотых дров." % str(_total_wood)
        elif key == "make_fire":
            _fire_object = _pc_fire_object(where_id, object_id)
            _fuel_room = _pc_room_by_code(where_id)
            if _pc_player_has_item("chopped_wood_001"):
                _player_remove_item_by_id("chopped_wood_001")
            elif _object_state_int(_fire_object, "chopped_wood_stock", 0) > 0:
                _add_object_state_int(_fire_object, "chopped_wood_stock", -1, 0)
            else:
                _room_remove_item_by_id(_fuel_room, "chopped_wood_001")
            _set_object_state_int(_fire_object, "fire_until_minute", _pc_calendar_total_minutes() + (8 * 60))
            _set_object_state_int(_fire_object, "fire_units", 0)
            _set_object_state_int(_fire_object, "ash_dirty", 1)
            fun = _pc_clamp(fun + 5, 0, 100)
            energy = _pc_clamp(energy - 5, 0, 100)
            exploration = max(0, _pc_to_int(exploration, 0) + 1)
            result_text = "Вы подкладываете колотые дрова и разводите огонь. В {b}%s{/b} тепла должно хватить примерно на {b}восемь часов{/b}." % str(_fire_object.name).strip().lower()
        elif key == "clean_ashes":
            _fire_object = _pc_fire_object(where_id, object_id)
            _set_object_state_int(_fire_object, "ash_dirty", 0)
            ashesdirtydays = 0
            _pc_advance_minutes(30)
            fun = _pc_clamp(fun - 10, 0, 100)
            energy = _pc_clamp(energy - 20, 0, 100)
            dayssincewash = max(0, _pc_to_int(dayssincewash, 0) + 1)
            exploration = max(0, _pc_to_int(exploration, 0) + 1)
            result_text = "Вы выгребаете золу и приводите очаг в порядок."
        elif key == "boil_water":
            _fire_object = _pc_fire_object(where_id, object_id)
            _water_object = _pc_water_object(where_id, object_id)
            _pc_advance_minutes(60)
            _set_object_state_int(_water_object, "hot_water_until_minute", _pc_calendar_total_minutes() + (24 * 60))
            _set_object_state_int(_water_object, "hot_water_units", 0)
            fun = _pc_clamp(fun - 10, 0, 100)
            energy = _pc_clamp(energy - 5, 0, 100)
            taverncleanliness = _pc_clamp(taverncleanliness - 4, 0, 100)
            exploration = max(0, _pc_to_int(exploration, 0) + 1)
            result_text = "Вы ставите воду греться. В {b}%s{/b} теперь будет горячая вода до {b}следующего дня{/b}." % str(_water_object.name).strip().lower()
        elif key == "clean_upstairs_rooms":
            fun = _pc_clamp(fun - 25, 0, 100)
            energy = _pc_clamp(energy - 15, 0, 100)
            dayssincewash = max(0, _pc_to_int(dayssincewash, 0) + 1)
            exploration = max(0, _pc_to_int(exploration, 0) + 1)
            upstairsroomsdirty = 0
            result_text = "Вы тратите время на уборку комнат наверху и к концу работы валитесь с ног."
        else:
            result_text = "Дело выполнено."

        renpy.notify("Зачтено: %s" % _pc_chore_display_name(key))
        return {"ok": True, "text": result_text, "chore_key": key}

    def record_weekly_tavern_visitors(visitors_count):
        _ensure_player_chores_state()
        WeeklyVisitorsTrack["sum"] = max(0, _pc_to_int(WeeklyVisitorsTrack.get("sum", 0), 0)) + max(0, _pc_to_int(visitors_count, 0))
        WeeklyVisitorsTrack["days"] = max(0, _pc_to_int(WeeklyVisitorsTrack.get("days", 0), 0)) + 1

    def _friends_add(girl_key, delta):
        key = str(girl_key or "").strip()
        if not key:
            return
        cur = _pc_to_int(Friends.get(key, 0), 0)
        Friends[key] = max(0, min(20, cur + _pc_to_int(delta, 0)))

    def weekly_chores_evaluation_preview(
        week_now=1,
        time_now=0,
        year_now=1100,
        month_now=1,
        day_now=1,
        last_stamp="",
        chores_state=None,
        visitors_track=None,
        sandra_friend=0,
        sandra_flags=None,
        rebel_state=None,
        hour_now=None,
    ):
        chores_state = dict(chores_state or {})
        visitors_track = dict(visitors_track or {})
        sandra_flags = dict(sandra_flags or {})
        rebel_state = dict(rebel_state or {})

        chores = {key: max(0, _pc_to_int(chores_state.get(key, 0), 0)) for key in PLAYER_CHORE_KEYS}
        week_vis = {
            "sum": max(0, _pc_to_int(visitors_track.get("sum", 0), 0)),
            "days": max(0, _pc_to_int(visitors_track.get("days", 0), 0)),
            "prev_avg": float(visitors_track.get("prev_avg", 0.0) or 0.0),
        }
        sandra_friend_value = max(0, _pc_to_int(sandra_friend, 0))
        next_flags = {
            "MCVisitFirstReady": max(0, _pc_to_int(sandra_flags.get("MCVisitFirstReady", 0), 0)),
            "MCVisitFirstPending": max(0, _pc_to_int(sandra_flags.get("MCVisitFirstPending", 0), 0)),
            "WeeklyChoreCheckScore": max(0, _pc_to_int(sandra_flags.get("WeeklyChoreCheckScore", 0), 0)),
            "WeeklyChoreCheckCounter": max(0, _pc_to_int(sandra_flags.get("WeeklyChoreCheckCounter", 0), 0)),
            "Week5WakePending": max(0, _pc_to_int(sandra_flags.get("Week5WakePending", 0), 0)),
            "WeeklyChoreCheckEval": str(sandra_flags.get("WeeklyChoreCheckEval", "") or ""),
        }
        next_rebel = {girl: max(0, _pc_to_int(rebel_state.get(girl, 0), 0)) for girl in PLAYER_CORE_OTHER_GIRLS}

        week_value = _pc_to_int(week_now, 1)
        time_value = _pc_to_int(time_now, 0)
        stamp = "%s:%s:%s:%s" % (
            _pc_to_int(year_now, 1100),
            _pc_to_int(month_now, 1),
            _pc_to_int(day_now, 1),
            week_value,
        )

        preview = {
            "applied": False,
            "message": "",
            "stamp": str(last_stamp or ""),
            "chores": chores,
            "visitors": week_vis,
            "sandra_friend": sandra_friend_value,
            "sandra_flags": next_flags,
            "rebel": next_rebel,
        }

        if week_value != 7:
            return preview
        if time_value < 3:
            return preview
        if time_value >= 4 and hour_now is not None and _pc_to_int(hour_now, 23) < 22:
            return preview
        if str(last_stamp or "") == stamp:
            return preview

        reward_lines = []
        sandra_gain = 0
        chore_score = 0

        chores_ok = True
        for key in PLAYER_CHORE_KEYS:
            if _pc_to_int(chores.get(key, 0), 0) >= player_chore_target(key):
                chore_score += 1
            else:
                chores_ok = False
        next_flags["WeeklyChoreCheckScore"] = chore_score
        if chore_score >= 5:
            next_flags["WeeklyChoreCheckEval"] = "good"
            reward_lines.append("Сандра признала, что по хозяйству неделя вышла {b}хорошей{/b}.")
        elif chore_score >= 3:
            next_flags["WeeklyChoreCheckEval"] = "neutral"
            reward_lines.append("Сандра признала, что по хозяйству неделя вышла {b}средней{/b}.")
        else:
            next_flags["WeeklyChoreCheckEval"] = "bad"
            reward_lines.append("Сандра признала, что по хозяйству неделя вышла {b}плохой{/b}.")
        if chore_score >= 4:
            next_flags["WeeklyChoreCheckCounter"] = max(0, _pc_to_int(next_flags.get("WeeklyChoreCheckCounter", 0), 0)) + 1
            next_flags["Week5WakePending"] = 1
            reward_lines.append("Сандра отметила, что по хозяйству вы закрыли %d из %d еженедельных дел." % (chore_score, len(PLAYER_CHORE_KEYS)))
        else:
            next_flags["Week5WakePending"] = 0
        if chores_ok:
            sandra_gain += 1
            reward_lines.append("Сандра заметила, что вы не запускали хозяйские дела всю неделю.")

        days = max(0, _pc_to_int(week_vis.get("days", 0), 0))
        visitors_sum = max(0, _pc_to_int(week_vis.get("sum", 0), 0))
        prev_avg = float(week_vis.get("prev_avg", 0.0) or 0.0)
        cur_avg = (float(visitors_sum) / float(days)) if days > 0 else 0.0
        if days > 0 and prev_avg > 0.0 and cur_avg > prev_avg:
            sandra_gain += 1
            reward_lines.append("Средняя посещаемость трактира за неделю выросла.")

        if sandra_gain > 0:
            sandra_friend_value = max(0, min(20, sandra_friend_value + sandra_gain))
            reward_lines.append("Уровень дружбы Сандры вырос на %d." % sandra_gain)

            reduced = []
            for girl in PLAYER_CORE_OTHER_GIRLS:
                old = _pc_to_int(next_rebel.get(girl, 0), 0)
                if old > 0:
                    next_rebel[girl] = old - 1
                    reduced.append(girl)
            if reduced:
                reward_lines.append("После ее благодарности остальные стали посговорчивее.")

        if sandra_friend_value >= 10 and _pc_to_int(next_flags.get("MCVisitFirstReady", 0), 0) == 0:
            next_flags["MCVisitFirstReady"] = 1
            next_flags["MCVisitFirstPending"] = 1
            reward_lines.append("Сандра явно готова впервые зайти к вам утром в комнату.")

        for key in PLAYER_CHORE_KEYS:
            chores[key] = 0
        week_vis["prev_avg"] = cur_avg
        week_vis["sum"] = 0
        week_vis["days"] = 0

        preview["applied"] = True
        preview["stamp"] = stamp
        preview["chores"] = chores
        preview["visitors"] = week_vis
        preview["sandra_friend"] = sandra_friend_value
        preview["sandra_flags"] = next_flags
        preview["rebel"] = next_rebel
        preview["message"] = ("<br>" + "<br>".join(reward_lines) + "<br>") if reward_lines else ""
        return preview

    def evaluate_weekly_chores_and_rewards():
        global week, time, year, month, day, WeeklyChoresLastEvalStamp
        global PlayerChoresWeek, WeeklyVisitorsTrack, neshlush, SandraVar, Friends, UI_chores
        _ensure_player_chores_state()
        preview = weekly_chores_evaluation_preview(
            week_now=week,
            time_now=time,
            hour_now=hour,
            year_now=year,
            month_now=month,
            day_now=day,
            last_stamp=WeeklyChoresLastEvalStamp,
            chores_state=PlayerChoresWeek,
            visitors_track=WeeklyVisitorsTrack,
            sandra_friend=(Friends or {}).get("sandra", 0),
            sandra_flags=SandraVar,
            rebel_state=neshlush,
        )
        if not bool(preview.get("applied", False)):
            return ""

        WeeklyChoresLastEvalStamp = str(preview.get("stamp", "") or WeeklyChoresLastEvalStamp)
        Friends["sandra"] = max(0, _pc_to_int(preview.get("sandra_friend", 0), 0))

        preview_flags = dict(preview.get("sandra_flags", {}) or {})
        SandraVar["MCVisitFirstReady"] = max(0, _pc_to_int(preview_flags.get("MCVisitFirstReady", 0), 0))
        SandraVar["MCVisitFirstPending"] = max(0, _pc_to_int(preview_flags.get("MCVisitFirstPending", 0), 0))
        SandraVar["WeeklyChoreCheckScore"] = max(0, _pc_to_int(preview_flags.get("WeeklyChoreCheckScore", 0), 0))
        SandraVar["WeeklyChoreCheckCounter"] = max(0, _pc_to_int(preview_flags.get("WeeklyChoreCheckCounter", 0), 0))
        SandraVar["Week5WakePending"] = max(0, _pc_to_int(preview_flags.get("Week5WakePending", 0), 0))
        SandraVar["WeeklyChoreCheckEval"] = str(preview_flags.get("WeeklyChoreCheckEval", "") or "")

        preview_rebel = dict(preview.get("rebel", {}) or {})
        for girl in PLAYER_CORE_OTHER_GIRLS:
            neshlush[girl] = max(0, _pc_to_int(preview_rebel.get(girl, neshlush.get(girl, 0)), 0))

        preview_chores = dict(preview.get("chores", {}) or {})
        for key in PLAYER_CHORE_KEYS:
            PlayerChoresWeek[key] = max(0, _pc_to_int(preview_chores.get(key, 0), 0))
        _pc_sync_ui_chores()

        preview_visitors = dict(preview.get("visitors", {}) or {})
        WeeklyVisitorsTrack["prev_avg"] = float(preview_visitors.get("prev_avg", 0.0) or 0.0)
        WeeklyVisitorsTrack["sum"] = max(0, _pc_to_int(preview_visitors.get("sum", 0), 0))
        WeeklyVisitorsTrack["days"] = max(0, _pc_to_int(preview_visitors.get("days", 0), 0))

        return str(preview.get("message", "") or "")
