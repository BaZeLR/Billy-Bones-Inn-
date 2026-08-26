# ================================================================================
# Player intimacy, sleep layer, and arousal state.
# (Defaults centralized in script.rpy to avoid duplicate default errors)
# ================================================================================

define PLAYER_DAILY_EXHAUSTION_TEXT = "То что упало - подняться не может. По крайней мере сегодня. Вот завтра силы к вам, быть может, вернутся."

init python:
    def player_intimacy_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return int(default or 0)

    def player_intimacy_clamp(value, low=0, high=100):
        return max(int(low), min(int(high), player_intimacy_int(value, low)))

    def player_cum_count():
        return player_intimacy_int(player.intimacy.came_today, 0)

    def player_cum_limit():
        return max(1, player_intimacy_int(player.intimacy.can_cum_daily, 1))

    def player_set_cum_count(value):
        count = max(0, player_intimacy_int(value, 0))
        intimacy = player.intimacy
        intimacy.came_today = count
        return count

    def player_mark_sex_day(reason="", target=""):
        intimacy = player.intimacy
        intimacy.last_sex_day = current_game_day()
        intimacy.last_cum_day = current_game_day()
        return intimacy.last_sex_day

    def player_record_orgasm(reason="", target=""):
        intimacy = player.intimacy
        result = intimacy.record_cum(current_game_day())
        target_key = str(target or "").strip().lower()
        if target_key:
            partner = people.get_info(target_key)
            if partner is not None:
                partner.mark_fucked(1)
                partner.record_sex_history("You", str(reason or ""), "orgasm")
        return result

    def player_days_without_sex():
        last_day = player_intimacy_int(player.intimacy.last_sex_day, -1)
        today = current_game_day()
        if last_day < 0:
            return max(0, today)
        return max(0, today - last_day)

    def player_ensure_nightwear_in_chest():
        appearance = player.appearance
        appearance.ensure_nightwear(current_game_day())
        return True

    def player_body_profile():
        try:
            return bodymodel_build_profile("You", "Стефан", "male")
        except Exception:
            return {}

    def player_set_sleep_layer(mode="daywear"):
        appearance = player.appearance
        appearance.set_sleep_layer(mode, current_game_day())
        player_body_profile()
        return appearance.sleep_bottom_layer

    def player_is_naked():
        return player.appearance.is_naked()

    def player_is_in_nightwear():
        return player.appearance.is_nightwear()

    def player_public_movement_block_text():
        if player_is_naked():
            return "Сначала нужно одеться. Голым дальше второго этажа вы не пойдете."
        return ""

    def player_can_leave_second_floor():
        return not player_is_naked()

    def player_arousal_state_line():
        value = player.intimacy.arousal_value()
        if player_cum_count() >= player_cum_limit():
            return "Мужская сила на сегодня уже истрачена."
        if value < 20:
            return "Член спокоен."
        if value < 45:
            return "Член налился и уже заметно приподнят."
        if value < 75:
            return "Стояк крепкий, тело явно требует разрядки."
        if value < 100:
            return "Вы сильно возбуждены и держитесь на грани."
        return "Вы уже не можете сдерживаться."

    def player_body_state_lines():
        player_profile = player_body_profile()
        lines = []
        if player_is_naked():
            lines.append("На вас сейчас нет одежды.")
        elif player_is_in_nightwear():
            lines.append("На вас ночная рубашка из ларя, пригодная для сна, но слишком домашняя для трактира.")
        else:
            lines.append("На вас дневная одежда.")
        if player_is_naked():
            lines.append("Нижний слой: ничего.")
        elif player_is_in_nightwear():
            lines.append("Нижний слой: одежда для сна.")
        else:
            lines.append("Нижний слой: дневная одежда.")
        lines.append(player_arousal_state_line())
        days_wait = player_days_without_sex()
        if days_wait >= 2:
            lines.append("Без секса уже %s дня; тело реагирует быстрее обычного." % days_wait)
        if str(player.intimacy.wake_state_notice or "").strip() and player_intimacy_int(player.intimacy.morning_arousal_day, -1) == current_game_day():
            lines.append(str(player.intimacy.wake_state_notice))
        try:
            body_text = bodymodel_profile_summary_text(player_profile)
            if body_text:
                lines.append(body_text)
        except Exception:
            pass
        return [str(line) for line in lines if str(line or "").strip()]

    def player_apply_arousal_trigger(trigger_code="", amount=0):
        trigger_key = str(trigger_code or "context").strip()
        intimacy = player.intimacy
        current = player_intimacy_int(intimacy.arousal_value(), 0)
        if player_cum_count() >= player_cum_limit():
            intimacy.set_arousal(0)
            return 0
        new_value = player_intimacy_clamp(current + player_intimacy_int(amount, 0), 0, 95)
        intimacy.set_arousal(new_value)
        if trigger_key and trigger_key not in player.intimacy.arousal_reasons:
            player.intimacy.arousal_reasons.append(trigger_key)
        return new_value

    def player_apply_morning_state(location_code=""):
        if str(location_code or rooms.current_code or "") != "TavernMyRoom":
            return ""
        today = current_game_day()
        if player_intimacy_int(player.intimacy.morning_arousal_day, -1) == today:
            return str(player.intimacy.wake_state_notice or "")
        player.intimacy.morning_arousal_day = today
        days_wait = player_days_without_sex()
        seed = (today * 37 + int(calendar_v2.hour or 0) * 11 + int(calendar_v2.time_slot()) * 19) % 100
        should_rise = int(calendar_v2.time_slot()) == 0 and (days_wait >= 2 or seed < 18 or player_is_naked() or player_is_in_nightwear())
        if not should_rise:
            player.intimacy.wake_state_notice = ""
            return ""
        amount = 18 + min(35, days_wait * 8)
        if player_is_naked() or player_is_in_nightwear():
            amount += 7
        player_apply_arousal_trigger("wake", amount)
        player.intimacy.wake_state_notice = "Вы проснулись с заметным утренним стояком."
        return player.intimacy.wake_state_notice

    def player_npc_exposed_for_arousal(npc_id=""):
        key = str(npc_id or "").strip().lower()
        if not key:
            return False
        try:
            profile = bodymodel_build_profile(key, people_display_name(key), "female")
            if bool(profile.get("naked", False)):
                return True
            access = dict(profile.get("access", {}) or {})
            nipples = bodymodel_target_block_state(profile, "nipples")
            pussy = bodymodel_target_block_state(profile, "pussy")
            if int(nipples.get("level", 2) or 2) == 0 or int(pussy.get("level", 2) or 2) == 0:
                return True
        except Exception:
            pass
        info = people.get_info(key)
        return bool(info is not None and (info.tits_visible() or info.pussy_visible()))

    def player_observe_npc_body(npc_id="", where_id=""):
        key = str(npc_id or "").strip().lower()
        if not key or not player_npc_exposed_for_arousal(key):
            return 0
        if not isinstance(player.intimacy.observed_naked_npc_day, dict):
            return 0
        today = current_game_day()
        if player_intimacy_int(player.intimacy.observed_naked_npc_day.get(key, -1), -1) == today:
            return player.intimacy.arousal_value()
        player.intimacy.observed_naked_npc_day[key] = today
        return player_apply_arousal_trigger("saw_naked_" + key, 12 + min(18, player_days_without_sex() * 3))

    def player_intimacy_help_kind(girl_name="", profile=None):
        data = dict(profile or build_girl_decision_profile(girl_name))
        oral_score = float(data.get("oral_pref", 0.0) or 0.0) + float(data.get("sexual_openness", 0.0) or 0.0) + float(data.get("arousal", 0.0) or 0.0)
        seed = (current_game_day() * 29 + sum([ord(ch) for ch in str(girl_name or "")])) % 100
        if oral_score >= 1.15 and seed < int(35 + oral_score * 25):
            return "blowjob"
        return "handjob"

    def player_apply_intimacy_help_penalty(girl_name=""):
        key = str(girl_name or "").strip().lower()
        info = people.get_info(key)
        before = player_intimacy_int(getattr(info, "corruption", 0), 0) if info is not None else 0
        reduction = max(1, int(round(float(before) * 0.35))) if before > 0 else 0
        if info is not None:
            info.corruption = max(0, before - reduction)
            info.rel = max(0, player_intimacy_int(getattr(info, "rel", 0), 0) - 10)
        try:
            relationship_set_anger(key, 2, 1, "intimacy_help_insult")
        except Exception:
            pass
        return {"before": before, "after": max(0, before - reduction), "reduction": reduction}

    def player_intimacy_help_result(girl_name="", forced_roll=None):
        key = str(girl_name or "").strip().lower()
        if key == "":
            return {"ok": False, "girl": "", "text": "Сейчас некого просить."}
        try:
            profile = build_girl_decision_profile(key)
        except Exception:
            profile = {}
        roll_value = forced_roll
        try:
            decision = girl_decide(key, "intimate_help", profile, roll_value)
        except Exception:
            decision = {"reaction": "neutral", "profile": profile}
        reaction = str(decision.get("reaction", "neutral") or "neutral")
        positive = reaction in ("good", "capricious_bad_is_good")
        name = str(people_display_name(key) or key)
        if positive:
            kind = player_intimacy_help_kind(key, decision.get("profile", profile))
            if kind == "blowjob":
                text = "%s соглашается помочь и выбирает самый прямой способ: опускается перед вами, доводит дело ртом и не отпускает, пока напряжение не уходит." % name
            else:
                text = "%s соглашается помочь без лишнего шума. Она устраивается ближе, берет ваш член рукой и доводит вас до разрядки быстрым, уверенным движением." % name
            player_record_orgasm("npc_help_" + kind, key)
            info = people.get_info(key)
            if info is not None:
                info.change_social(friend_delta=1, corruption_delta=1)
            result = {"ok": True, "girl": key, "kind": kind, "reaction": reaction, "text": text}
        else:
            penalty = player_apply_intimacy_help_penalty(key)
            text = "%s воспринимает просьбу как оскорбление. Она резко отстраняется, смотрит холодно и дает понять, что вы перепутали близость с правом требовать. Ее доверие падает, а распущенность заметно остывает." % name
            result = {"ok": False, "girl": key, "kind": "", "reaction": reaction, "penalty": penalty, "text": text}
        player.intimacy.last_help_result = dict(result)
        return dict(result)

    def player_can_ask_intimacy_help(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if key == "":
            return False
        if player_cum_count() >= player_cum_limit():
            return False
        if player_intimacy_int(player.intimacy.arousal_value(), 0) < 40:
            return False
        return True


label PlayerIntimacyHelpAsk(girl_name="", return_label=""):
    $ renpy.dynamic("_pih_result")
    $ _pih_result = player_intimacy_help_result(girl_name)
    $ scene_runtime.text = str(_pih_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    "[scene_runtime.text]"
    $ main_ui_runtime.action_title = "Просьба о помощи"
    $ main_ui_runtime.action_content = None
    $ main_ui_runtime.action_items = []
    if str(return_label or "").strip() != "":
        $ main_ui_runtime.action_items.append(MenuItem("Назад", Call(return_label)))
    else:
        $ main_ui_runtime.action_items.append(MenuItem("Назад", Jump(str(rooms.current_code or ""))))
    $ renpy.restart_interaction()
    return
