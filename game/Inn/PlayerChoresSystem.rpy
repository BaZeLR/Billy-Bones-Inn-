# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -45 python:
    import renpy.exports as renpy

    PLAYER_CHORE_KEYS = ("bring_woods", "chop_wood", "make_fire", "clean_ashes", "boil_water", "clean_upstairs_rooms")
    PLAYER_CHORE_TARGETS = {k: (7 if k == "boil_water" else 3) for k in PLAYER_CHORE_KEYS}

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
        return player.item_count(item_key) > 0

    def _pc_advance_minutes(minutes_to_add):
        try:
            calendar_v2.advance_minutes(_pc_to_int(minutes_to_add, 0))
        except Exception:
            pass

    def _pc_fire_object(where_id="", object_id=""):
        object_key = get_object_id(object_id)
        if object_key in ("kitchen_hearth_001", "hearth_001", "cauldron_001") or str(where_id or "") == "TavernKitchen":
            return TavernKitchenHearthObject
        return TavernMainFireplaceObject

    def _pc_water_object(where_id="", object_id=""):
        return TavernKitchenCauldronObject

    def _pc_room_by_code(where_id=""):
        room_code = str(where_id or getattr(rooms.current, "code_name", "") or rooms.current_code or "").strip()
        if room_code == "TavernKitchen":
            try:
                return rooms.get("TavernKitchen")
            except Exception:
                return rooms.current
        if room_code == "TavernMain":
            try:
                return rooms.get("TavernMain")
            except Exception:
                return rooms.current
        return rooms.current

    def _pc_calendar_total_minutes():
        return current_game_day() * 1440 + (_pc_to_int(calendar_v2.hour, 0) * 60) + _pc_to_int(calendar_v2.minute, 0)

    def _pc_fire_duration_minutes():
        return 12 * 60

    def _pc_fire_until_minute(fire_object):
        if fire_object is None:
            return 0
        return _object_state_int(fire_object, "fire_until_minute", 0)

    def _pc_fire_started_minute(fire_object):
        if fire_object is None:
            return 0
        started_minute = _object_state_int(fire_object, "fire_started_minute", 0)
        until_minute = _pc_fire_until_minute(fire_object)
        if started_minute <= 0 and until_minute > _pc_calendar_total_minutes():
            started_minute = max(0, until_minute - _pc_fire_duration_minutes())
            _set_object_state_int(fire_object, "fire_started_minute", started_minute)
        return started_minute

    def _pc_fire_elapsed_minutes(fire_object):
        started_minute = _pc_fire_started_minute(fire_object)
        if started_minute <= 0:
            return 0
        return max(0, _pc_calendar_total_minutes() - started_minute)

    def _pc_fire_remaining_minutes(fire_object):
        return max(0, _pc_fire_until_minute(fire_object) - _pc_calendar_total_minutes())

    def _pc_hot_water_until_minute(water_object):
        if water_object is None:
            return 0
        return _object_state_int(water_object, "hot_water_until_minute", 0)

    def _pc_fire_is_active(fire_object):
        return _pc_fire_until_minute(fire_object) > _pc_calendar_total_minutes()

    def _pc_hot_water_is_ready(water_object):
        return _pc_hot_water_until_minute(water_object) > _pc_calendar_total_minutes()

    def tavern_kitchen_reset_daily_hearth_state():
        _set_object_state_int(TavernKitchenHearthObject, "madeFireToday", 0)
        _set_object_state_int(TavernKitchenCauldronObject, "boiledWaterToday", 0)
        return True

    def _pc_fire_fuel_available(where_id="", object_id=""):
        room_obj = _pc_room_by_code(where_id)
        fire_object = _pc_fire_object(where_id, object_id)
        return (
            _pc_player_has_item("chopped_wood_001")
            or _room_has_item_by_id(room_obj, "chopped_wood_001")
            or _object_state_int(fire_object, "chopped_wood_stock", 0) > 0
        )

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
        return max(1, _pc_to_int(PLAYER_CHORE_TARGETS.get(key, 3), 3))

    def _pc_register_chore_success(chore_key):
        key = str(chore_key or "").strip()
        cur = _pc_to_int(player.chores.weekly.get(key, 0), 0)
        player.chores.weekly[key] = cur + 1
        return True

    def can_do_player_chore(chore_key, where_id="", object_id=""):
        _ensure_player_chores_state()
        key = str(chore_key or "").strip()
        if key not in PLAYER_CHORE_KEYS:
            return False, "Такого дела сейчас нет."
        restriction = str(action_restriction_message("chore") or "").strip()
        if restriction:
            return False, restriction
        if _pc_to_int(player.condition.fun, 0) < 26:
            return False, "У вас слишком плохое настроение для такой работы."
        if _pc_to_int(player.condition.energy, 0) <= 0:
            return False, "У вас не осталось сил."
        if key == "bring_woods" and not _pc_player_has_item("old_axe_001"):
            return False, "Без топора идти за дровами бессмысленно."
        if key == "chop_wood":
            if not _pc_player_has_item("old_axe_001"):
                return False, "Без топора колоть дрова не выйдет."
            if not _room_has_item_by_id(rooms.get("Shed"), "lumber_001") and not _pc_player_has_item("lumber_001"):
                return False, "Сначала нужно принести бревна."
        if key == "make_fire" and not _pc_fire_fuel_available(where_id, object_id):
            room_obj = _pc_room_by_code(where_id)
            if _pc_player_has_item("lumber_001") or _room_has_item_by_id(room_obj, "lumber_001") or _room_has_item_by_id(rooms.get("Shed"), "lumber_001"):
                return False, "Сначала нужно наколоть бревна на дрова."
            return False, "Нечем топить камин."
        if key == "boil_water":
            if not _pc_fire_is_active(_pc_fire_object(where_id, object_id)):
                return False, "Сначала нужно разжечь огонь."
        return True, ""

    def _ensure_player_chores_state():
        if not isinstance(player.chores.weekly, dict):
            player.chores.weekly = {}
        for key in PLAYER_CHORE_KEYS:
            player.chores.weekly[key] = max(0, _pc_to_int(player.chores.weekly.get(key, 0), 0))
        player.chores.last_score = max(0, _pc_to_int(getattr(player.chores, "last_score", 0), 0))
        player.chores.last_evaluation = str(getattr(player.chores, "last_evaluation", "") or "")

        if not isinstance(player.tavern_management.weekly_visitors, dict):
            player.tavern_management.weekly_visitors = {}
        player.tavern_management.weekly_visitors["sum"] = max(0, _pc_to_int(player.tavern_management.weekly_visitors.get("sum", 0), 0))
        player.tavern_management.weekly_visitors["days"] = max(0, _pc_to_int(player.tavern_management.weekly_visitors.get("days", 0), 0))
        try:
            player.tavern_management.weekly_visitors["prev_avg"] = float(player.tavern_management.weekly_visitors.get("prev_avg", 0.0) or 0.0)
        except Exception:
            player.tavern_management.weekly_visitors["prev_avg"] = 0.0

        if not isinstance(player.tavern_management.weekly_chores_last_eval_stamp, str):
            player.tavern_management.weekly_chores_last_eval_stamp = str(player.tavern_management.weekly_chores_last_eval_stamp or "")

        for girl in PLAYER_CORE_OTHER_GIRLS:
            info = people.get_info(girl)
            if info is not None and not hasattr(info, "rebel_baseline"):
                info.rebel_baseline = max(0, 5 - int(info.openness or 0))

    def get_player_chores_ui_state():
        _ensure_player_chores_state()
        return {k: int(player.chores.weekly.get(k, 0) or 0) for k in PLAYER_CHORE_KEYS}

    def do_player_chore(chore_key, where_id="", object_id=""):
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
            player.change_stat("fun", 25)
            player.change_stat("energy", -40)
            player.change_stat("exploration", 1)
            player.tavern_management.cleanliness = _pc_clamp(player.tavern_management.cleanliness - 15, 0, 100)
            _room_add_item_by_id(rooms.get("Shed"), "lumber_001")
            result_text = "Вы уходите в лес за дровами. К вечеру удается притащить {b}одно крепкое бревно{/b} для хозяйства."
        elif key == "chop_wood":
            if _pc_player_has_item("lumber_001"):
                player.remove_item("lumber_001")
            else:
                _room_remove_item_by_id(rooms.get("Shed"), "lumber_001")
            _room_add_item_units(rooms.get("Shed"), "chopped_wood_001", 10)
            _pc_advance_minutes(60)
            player.change_stat("fun", 5)
            player.change_stat("energy", -20)
            player.change_stat("exploration", 3)
            _total_wood = _room_item_count_by_id(rooms.get("Shed"), "chopped_wood_001")
            result_text = "Вы ставите бревно на колоду и рубите его на поленья. В сарае теперь {b}%s{/b} единиц колотых дров." % str(_total_wood)
        elif key == "make_fire":
            _fire_object = _pc_fire_object(where_id, object_id)
            _fuel_room = _pc_room_by_code(where_id)
            _fire_was_active = _pc_fire_is_active(_fire_object)
            _fire_now = _pc_calendar_total_minutes()
            if _object_state_int(_fire_object, "chopped_wood_stock", 0) > 0:
                _add_object_state_int(_fire_object, "chopped_wood_stock", -1, 0)
            elif _pc_player_has_item("chopped_wood_001"):
                player.remove_item("chopped_wood_001")
            elif _room_has_item_by_id(_fuel_room, "chopped_wood_001"):
                _room_remove_item_by_id(_fuel_room, "chopped_wood_001")
            _set_object_state_int(_fire_object, "fire_started_minute", _fire_now)
            _set_object_state_int(_fire_object, "fire_until_minute", _fire_now + _pc_fire_duration_minutes())
            _set_object_state_int(_fire_object, "madeFireToday", 1)
            _set_object_state_int(_fire_object, "ash_dirty", 1)
            if _fire_was_active:
                _add_object_state_int(_fire_object, "fire_adds", 1, 0)
            else:
                _set_object_state_int(_fire_object, "fire_adds", 0)
            player.change_stat("fun", 5)
            player.change_stat("energy", -5)
            player.change_stat("exploration", 1)
            if _fire_was_active:
                result_text = "Вы подкладываете колотые дрова в {b}%s{/b}. Огонь снова будет держаться примерно {b}двенадцать часов{/b}." % str(_fire_object.name).strip().lower()
            else:
                result_text = "Вы подкладываете колотые дрова и разводите огонь. В {b}%s{/b} тепла должно хватить примерно на {b}двенадцать часов{/b}." % str(_fire_object.name).strip().lower()
        elif key == "clean_ashes":
            _fire_object = _pc_fire_object(where_id, object_id)
            _set_object_state_int(_fire_object, "ash_dirty", 0)
            player.tavern_management.ashes_dirty_days = 0
            _pc_advance_minutes(30)
            player.change_stat("fun", -10)
            player.change_stat("energy", -20)
            player.appearance.increment_wash_days(1)
            player.change_stat("exploration", 1)
            result_text = "Вы выгребаете золу и приводите очаг в порядок."
        elif key == "boil_water":
            _fire_object = _pc_fire_object(where_id, object_id)
            _water_object = _pc_water_object(where_id, object_id)
            _pc_advance_minutes(60)
            _set_object_state_int(_water_object, "hot_water_until_minute", _pc_calendar_total_minutes() + (24 * 60))
            _set_object_state_int(_water_object, "boiledWaterToday", 1)
            player.change_stat("fun", -10)
            player.change_stat("energy", -5)
            player.tavern_management.cleanliness = _pc_clamp(player.tavern_management.cleanliness - 4, 0, 100)
            player.change_stat("exploration", 1)
            result_text = "Вы ставите воду греться. В {b}%s{/b} теперь будет горячая вода до {b}следующего дня{/b}." % str(_water_object.name).strip().lower()
        elif key == "clean_upstairs_rooms":
            player.change_stat("fun", -25)
            player.change_stat("energy", -15)
            player.appearance.increment_wash_days(1)
            player.change_stat("exploration", 1)
            player.tavern_management.upstairs_rooms_dirty = 0
            result_text = "Вы тратите время на уборку комнат наверху и к концу работы валитесь с ног."
        else:
            result_text = "Дело выполнено."

        renpy.notify("Зачтено: %s" % _pc_chore_display_name(key))
        return {"ok": True, "text": result_text, "chore_key": key}

    def record_weekly_tavern_visitors(visitors_count):
        _ensure_player_chores_state()
        if not isinstance(player.tavern_management.weekly_visitors, dict):
            player.tavern_management.weekly_visitors = {}
        player.tavern_management.weekly_visitors["sum"] = max(0, _pc_to_int(player.tavern_management.weekly_visitors.get("sum", 0), 0)) + max(0, _pc_to_int(visitors_count, 0))
        player.tavern_management.weekly_visitors["days"] = max(0, _pc_to_int(player.tavern_management.weekly_visitors.get("days", 0), 0)) + 1

    def _friends_add(girl_key, delta):
        key = str(girl_key or "").strip()
        if not key:
            return
        info = people.get_info(key)
        if info is not None:
            info.change_social(friend_delta=_pc_to_int(delta, 0))

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
        rebel_state=None,
        hour_now=None,
    ):
        chores_state = dict(chores_state or {})
        visitors_track = dict(visitors_track or {})
        rebel_state = dict(rebel_state or {})

        chores = {key: max(0, _pc_to_int(chores_state.get(key, 0), 0)) for key in PLAYER_CHORE_KEYS}
        week_vis = {
            "sum": max(0, _pc_to_int(visitors_track.get("sum", 0), 0)),
            "days": max(0, _pc_to_int(visitors_track.get("days", 0), 0)),
            "prev_avg": float(visitors_track.get("prev_avg", 0.0) or 0.0),
        }
        sandra_friend_value = max(0, _pc_to_int(sandra_friend, 0))
        next_rebel = {girl: max(0, _pc_to_int(rebel_state.get(girl, 0), 0)) for girl in PLAYER_CORE_OTHER_GIRLS}

        week_value = _pc_to_int(week_now, 1)
        time_value = _pc_to_int(time_now, 0)
        hour_value = _pc_to_int(hour_now, 0)
        finishing_sunday_after_midnight = hour_now is not None and week_value == 1 and 0 <= hour_value < 6
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
            "chore_score": 0,
            "chore_evaluation": "",
            "rebel": next_rebel,
        }

        if week_value != 7 and not finishing_sunday_after_midnight:
            return preview
        if week_value == 7 and time_value < 3:
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
        if chore_score >= 5:
            chore_evaluation = "good"
            reward_lines.append("Сандра признала, что по хозяйству неделя вышла {b}хорошей{/b}.")
        elif chore_score >= 3:
            chore_evaluation = "neutral"
            reward_lines.append("Сандра признала, что по хозяйству неделя вышла {b}средней{/b}.")
        else:
            chore_evaluation = "bad"
            reward_lines.append("Сандра признала, что по хозяйству неделя вышла {b}плохой{/b}.")
        if chore_score >= 4:
            reward_lines.append("Сандра отметила, что по хозяйству вы закрыли %d из %d еженедельных дел." % (chore_score, len(PLAYER_CHORE_KEYS)))
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
        preview["chore_score"] = chore_score
        preview["chore_evaluation"] = chore_evaluation
        preview["rebel"] = next_rebel
        preview["message"] = ("<br>" + "<br>".join(reward_lines) + "<br>") if reward_lines else ""
        return preview

    def evaluate_weekly_chores_and_rewards():
        _ensure_player_chores_state()

        preview = weekly_chores_evaluation_preview(
            week_now=calendar_v2.week,
            time_now=calendar_v2.time_slot(),
            hour_now=calendar_v2.hour,
            year_now=calendar_v2.cycle,
            month_now=calendar_v2.period,
            day_now=calendar_v2.day,
            last_stamp=player.tavern_management.weekly_chores_last_eval_stamp,
            chores_state=player.chores.weekly,
            visitors_track=player.tavern_management.weekly_visitors,
            sandra_friend=Sandra.rel,
            rebel_state={girl: int(people.get_info(girl).rebel_baseline or 0) for girl in PLAYER_CORE_OTHER_GIRLS if people.get_info(girl) is not None},
        )
        if not bool(preview.get("applied", False)):
            return ""

        player.tavern_management.weekly_chores_last_eval_stamp = str(preview.get("stamp", "") or player.tavern_management.weekly_chores_last_eval_stamp)
        player.chores.last_score = max(0, _pc_to_int(preview.get("chore_score", 0), 0))
        player.chores.last_evaluation = str(preview.get("chore_evaluation", "") or "").strip().lower()
        Sandra.rel = max(0, min(20, _pc_to_int(preview.get("sandra_friend", Sandra.rel), Sandra.rel)))
        if player.chores.last_evaluation == "good":
            Sandra.change_mana(3, "weekly_check_good")
            Sandra.change_fear(-5, "weekly_check_good")
            Sandra.trust = max(0, min(100, _pc_to_int(Sandra.trust, 0) + 3))
        elif player.chores.last_evaluation == "bad":
            Sandra.change_mana(-3, "weekly_check_bad")
            Sandra.change_fear(5, "weekly_check_bad")
            if _pc_to_int(Sandra.anger_with_player, 0) > 40:
                Sandra.rebellion = max(0, min(100, _pc_to_int(Sandra.rebellion, 0) + 2))

        sandra_thread = threads["sandraWeeklyEvaluation"]
        if player.chores.last_score >= 4 and not sandra_thread.completed:
            sandra_thread.forceEnable()
            sandra_thread.day = int(current_game_day() or 0)

        preview_rebel = dict(preview.get("rebel", {}) or {})
        for girl in PLAYER_CORE_OTHER_GIRLS:
            info = people.get_info(girl)
            if info is not None:
                info.rebel_baseline = max(0, _pc_to_int(preview_rebel.get(girl, info.rebel_baseline), 0))

        relationship_apply_weekly_chore_evaluation(preview)

        preview_chores = dict(preview.get("chores", {}) or {})
        for key in PLAYER_CHORE_KEYS:
            player.chores.weekly[key] = max(0, _pc_to_int(preview_chores.get(key, 0), 0))
        preview_visitors = dict(preview.get("visitors", {}) or {})
        player.tavern_management.weekly_visitors["prev_avg"] = float(preview_visitors.get("prev_avg", 0.0) or 0.0)
        player.tavern_management.weekly_visitors["sum"] = max(0, _pc_to_int(preview_visitors.get("sum", 0), 0))
        player.tavern_management.weekly_visitors["days"] = max(0, _pc_to_int(preview_visitors.get("days", 0), 0))
        return str(preview.get("message", "") or "")
