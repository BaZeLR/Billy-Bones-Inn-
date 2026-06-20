# ================================================================================
# Player intimacy, sleep layer, and arousal state.
# (Defaults centralized in script.rpy to avoid duplicate default errors)
# ================================================================================

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
        try:
            if isinstance(cametoday, dict):
                return player_intimacy_int(cametoday.get("You", cametoday.get("you", 0)), 0)
            return player_intimacy_int(cametoday, 0)
        except Exception:
            return 0

    def player_cum_limit():
        try:
            if isinstance(cancumdaily, dict):
                return max(1, player_intimacy_int(cancumdaily.get("You", cancumdaily.get("you", 1)), 1))
            return max(1, player_intimacy_int(cancumdaily, 1))
        except Exception:
            return 1

    def player_set_cum_count(value):
        global cametoday
        count = max(0, player_intimacy_int(value, 0))
        if isinstance(cametoday, dict):
            cametoday["You"] = count
            cametoday["you"] = count
        else:
            cametoday = count
        return count

    def player_mark_sex_day(reason="", target=""):
        global LastDaySex, PlayerLastCumDay
        LastDaySex = player_intimacy_int(dayspassed, 0)
        PlayerLastCumDay = player_intimacy_int(dayspassed, 0)
        return LastDaySex

    def player_record_orgasm(reason="", target=""):
        global SomebodyCums
        player_set_cum_count(player_cum_count() + 1)
        if isinstance(HadSex, dict):
            HadSex["You"] = player_intimacy_int(HadSex.get("You", 0), 0) + 1
            target_key = str(target or "").strip().lower()
            if target_key:
                HadSex[target_key] = player_intimacy_int(HadSex.get(target_key, 0), 0) + 1
        player_mark_sex_day(reason, target)
        if isinstance(Arousal, dict):
            Arousal["You"] = 0
            Arousal["you"] = 0
        SomebodyCums = 1
        return player_cum_count()

    def player_days_without_sex():
        last_day = player_intimacy_int(LastDaySex, -1)
        today = player_intimacy_int(dayspassed, 0)
        if last_day < 0:
            return max(0, today)
        return max(0, today - last_day)

    def player_ensure_nightwear_in_chest():
        appearance = player_state().appearance
        appearance.ensure_nightwear(player_intimacy_int(dayspassed, 0))
        appearance.apply_to_store()
        return True

    def player_sync_body_state():
        key = "You"
        topdress.setdefault(key, "")
        bottomdress.setdefault(key, "")
        bra[key] = ""
        panties[key] = ""
        legs.setdefault(key, "")
        shoes.setdefault(key, "")
        topraised[key] = 0
        bottomraised[key] = 0
        appearance = player_state().appearance
        if appearance.is_naked():
            topdress[key] = ""
            bottomdress[key] = ""
            legs[key] = ""
            shoes[key] = ""
        else:
            dress_code = "nightshirt" if appearance.is_nightwear() else str(appearance.current_dress or "")
            topdress[key] = str(DressTopPart.get(dress_code, "") or "")
            bottomdress[key] = str(DressBottomPart.get(dress_code, "") or "")
        try:
            return bodymodel_sync_character(key, "Стефан", "male")
        except Exception:
            return {}

    def player_set_sleep_layer(mode="daywear"):
        appearance = player_state().appearance
        appearance.set_sleep_layer(mode, player_intimacy_int(dayspassed, 0))
        appearance.apply_to_store()
        player_sync_body_state()
        return appearance.sleep_bottom_layer

    def player_is_naked():
        return player_state().appearance.is_naked()

    def player_is_in_nightwear():
        return player_state().appearance.is_nightwear()

    def player_public_movement_block_text():
        if player_is_naked():
            return "Сначала нужно одеться. Голым дальше второго этажа вы не пойдете."
        return ""

    def player_can_leave_second_floor():
        return not player_is_naked()

    def player_arousal_state_line():
        value = player_intimacy_int(Arousal.get("You", 0), 0) if isinstance(Arousal, dict) else 0
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
        player_sync_body_state()
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
        if str(PlayerWakeStateNotice or "").strip() and player_intimacy_int(PlayerMorningArousalDay, -1) == player_intimacy_int(dayspassed, 0):
            lines.append(str(PlayerWakeStateNotice))
        try:
            body_text = bodymodel_profile_summary_text(BodyInteractionProfiles.get("You", {}) or {})
            if body_text:
                lines.append(body_text)
        except Exception:
            pass
        return [str(line) for line in lines if str(line or "").strip()]

    def player_apply_arousal_trigger(trigger_code="", amount=0):
        global PlayerArousalReasons
        if not isinstance(Arousal, dict):
            return 0
        trigger_key = str(trigger_code or "context").strip()
        current = player_intimacy_int(Arousal.get("You", 0), 0)
        if player_cum_count() >= player_cum_limit():
            Arousal["You"] = 0
            Arousal["you"] = 0
            return 0
        new_value = player_intimacy_clamp(current + player_intimacy_int(amount, 0), 0, 95)
        Arousal["You"] = new_value
        Arousal["you"] = new_value
        if not isinstance(PlayerArousalReasons, list):
            PlayerArousalReasons = []
        if trigger_key and trigger_key not in PlayerArousalReasons:
            PlayerArousalReasons.append(trigger_key)
        return new_value

    def player_apply_morning_state(location_code=""):
        global PlayerMorningArousalDay, PlayerWakeStateNotice
        if str(location_code or CurLoc or "") != "TavernMyRoom":
            return ""
        today = player_intimacy_int(dayspassed, 0)
        if player_intimacy_int(PlayerMorningArousalDay, -1) == today:
            return str(PlayerWakeStateNotice or "")
        PlayerMorningArousalDay = today
        days_wait = player_days_without_sex()
        seed = (today * 37 + player_intimacy_int(hour, 0) * 11 + player_intimacy_int(time, 0) * 19) % 100
        should_rise = int(time or 0) == 0 and (days_wait >= 2 or seed < 18 or player_is_naked() or player_is_in_nightwear())
        if not should_rise:
            PlayerWakeStateNotice = ""
            return ""
        amount = 18 + min(35, days_wait * 8)
        if player_is_naked() or player_is_in_nightwear():
            amount += 7
        player_apply_arousal_trigger("wake", amount)
        PlayerWakeStateNotice = "Вы проснулись с заметным утренним стояком."
        return PlayerWakeStateNotice

    def player_npc_exposed_for_arousal(npc_id=""):
        key = str(npc_id or "").strip().lower()
        if not key:
            return False
        try:
            profile = bodymodel_sync_character(key, RealName.get(key, key), "female")
            if bool(profile.get("naked", False)):
                return True
            access = dict(profile.get("access", {}) or {})
            nipples = bodymodel_target_block_state(profile, "nipples")
            pussy = bodymodel_target_block_state(profile, "pussy")
            if int(nipples.get("level", 2) or 2) == 0 or int(pussy.get("level", 2) or 2) == 0:
                return True
        except Exception:
            pass
        return int(TitsVisible.get(key, 0) or 0) > 0 or int(PussyVisible.get(key, 0) or 0) > 0

    def player_observe_npc_body(npc_id="", where_id=""):
        key = str(npc_id or "").strip().lower()
        if not key or not player_npc_exposed_for_arousal(key):
            return 0
        if not isinstance(PlayerObservedNakedNpcDay, dict):
            return 0
        today = player_intimacy_int(dayspassed, 0)
        if player_intimacy_int(PlayerObservedNakedNpcDay.get(key, -1), -1) == today:
            return player_intimacy_int(Arousal.get("You", 0), 0)
        PlayerObservedNakedNpcDay[key] = today
        return player_apply_arousal_trigger("saw_naked_" + key, 12 + min(18, player_days_without_sex() * 3))

    def player_intimacy_help_kind(girl_name="", profile=None):
        data = dict(profile or build_girl_decision_profile(girl_name))
        oral_score = float(data.get("oral_pref", 0.0) or 0.0) + float(data.get("sexual_openness", 0.0) or 0.0) + float(data.get("arousal", 0.0) or 0.0)
        seed = (player_intimacy_int(dayspassed, 0) * 29 + sum([ord(ch) for ch in str(girl_name or "")])) % 100
        if oral_score >= 1.15 and seed < int(35 + oral_score * 25):
            return "blowjob"
        return "handjob"

    def player_apply_intimacy_help_penalty(girl_name=""):
        key = str(girl_name or "").strip().lower()
        before = player_intimacy_int(sluttiness.get(key, 0), 0) if isinstance(sluttiness, dict) else 0
        reduction = max(1, int(round(float(before) * 0.35))) if before > 0 else 0
        if isinstance(sluttiness, dict):
            sluttiness[key] = max(0, before - reduction)
        if isinstance(Friends, dict):
            Friends[key] = max(-100, player_intimacy_int(Friends.get(key, 0), 0) - 10)
        try:
            relationship_set_anger(key, 2, 1, "intimacy_help_insult")
        except Exception:
            pass
        return {"before": before, "after": max(0, before - reduction), "reduction": reduction}

    def player_intimacy_help_result(girl_name="", forced_roll=None):
        global PlayerLastHelpResult
        key = str(girl_name or "").strip().lower()
        if key == "":
            return {"ok": False, "girl": "", "text": "Сейчас некого просить."}
        profile = build_girl_decision_profile(key) if "build_girl_decision_profile" in globals() else {}
        roll_value = forced_roll
        decision = girl_decide(key, "intimate_help", profile, roll_value) if "girl_decide" in globals() else {"reaction": "neutral", "profile": profile}
        reaction = str(decision.get("reaction", "neutral") or "neutral")
        positive = reaction in ("good", "capricious_bad_is_good")
        name = str(RealName.get(key, key) or key)
        if positive:
            kind = player_intimacy_help_kind(key, decision.get("profile", profile))
            if kind == "blowjob":
                text = "%s соглашается помочь и выбирает самый прямой способ: опускается перед вами, доводит дело ртом и не отпускает, пока напряжение не уходит." % name
            else:
                text = "%s соглашается помочь без лишнего шума. Она устраивается ближе, берет ваш член рукой и доводит вас до разрядки быстрым, уверенным движением." % name
            player_record_orgasm("npc_help_" + kind, key)
            if isinstance(Friends, dict):
                Friends[key] = min(100, player_intimacy_int(Friends.get(key, 0), 0) + 1)
            if isinstance(sluttiness, dict):
                sluttiness[key] = min(100, player_intimacy_int(sluttiness.get(key, 0), 0) + 1)
            result = {"ok": True, "girl": key, "kind": kind, "reaction": reaction, "text": text}
        else:
            penalty = player_apply_intimacy_help_penalty(key)
            text = "%s воспринимает просьбу как оскорбление. Она резко отстраняется, смотрит холодно и дает понять, что вы перепутали близость с правом требовать. Ее доверие падает, а распущенность заметно остывает." % name
            result = {"ok": False, "girl": key, "kind": "", "reaction": reaction, "penalty": penalty, "text": text}
        PlayerLastHelpResult = dict(result)
        return dict(result)

    def player_can_ask_intimacy_help(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if key == "":
            return False
        if player_cum_count() >= player_cum_limit():
            return False
        if player_intimacy_int(Arousal.get("You", 0), 0) < 40:
            return False
        return True


label PlayerIntimacyHelpAsk(girl_name="", return_label=""):
    $ _pih_result = player_intimacy_help_result(girl_name)
    if str(girl_name or "").strip().lower() == "amanda":
        $ AmandaVar["night_tease_resolved"] = 1
        $ AmandaVar["night_tease_scene_active"] = 0
        if bool(_pih_result.get("ok", False)) and str(CurLoc or "") == "TavernMyRoom":
            $ amanda_ai_clear_room_presence("TavernMyRoom")
    $ MainTxt = str(_pih_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    "[MainTxt]"
    $ current_action_title = "Просьба о помощи"
    $ current_action_content = None
    $ current_action_items = []
    if str(return_label or "").strip() != "":
        $ current_action_items.append(MenuItem("Назад", Call(return_label)))
    else:
        $ current_action_items.append(MenuItem("Назад", Jump(str(CurLoc or ""))))
    $ renpy.restart_interaction()
    return
