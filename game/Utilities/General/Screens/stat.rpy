        global player.stats.look, player.stats.reputation, player.stats.charismadefault PlayerConditionNoticeState = {}
default PlayerSocialConditionLast = {}        global PlayerSocialConditionLast        try:
            sync_soap_batches_with_day()
        except Exception:
            pass
        try:
            soap_expire_if_needed()
        except Exception:
            pass        global player.stats.look, player.stats.reputation, player.stats.charismadefault PlayerConditionNoticeState = {}
default PlayerSocialConditionLast = {}        global PlayerSocialConditionLast        try:
            sync_soap_batches_with_day()
        except Exception:
            pass
        try:
            soap_expire_if_needed()
        except Exception:
            pass        global player.stats.look, player.stats.reputation, player.stats.charismadefault PlayerConditionNoticeState = {}
default PlayerSocialConditionLast = {}        global PlayerSocialConditionLast        try:
            sync_soap_batches_with_day()
        except Exception:
            pass
        try:
            soap_expire_if_needed()
        except Exception:
            pass# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    import renpy.exports as renpy_module
    import renpy.store as store
    import renpy.store as store
    import renpy.store as store

    def _player_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _player_clamp_stat(value, low=0, high=100):
        return max(int(low), min(int(high), _player_int(value, low)))

    def player_dress_look_value(dress_code=""):
        appearance = player.appearance
        code = str(dress_code or appearance.current_dress or "").strip()
        if not code:
            return 15
        try:
            dress_map = dict(DressLookValue or {})
        except Exception:
            dress_map = {}
        if code in dress_map:
            return _player_int(dress_map.get(code, 15), 15)
        if code == "nightshirt":
            return 8
        if code in tuple(getattr(store, "MaleDressCodes", []) or []):
            return 20
        return 24

    def player_haircut_look_value(haircut_days=None):
        appearance = player.appearance
        days = _player_int(appearance.days_since_haircut if haircut_days is None else haircut_days, 0)
        return 15 if days < _player_int(getattr(appearance, "HAIRCUT_FRESH_DAYS", 14), 14) else -40

    def player_haircut_due_day():
        marker = _player_int(player.appearance.haircut_day, 0)
        return marker + _player_int(getattr(player.appearance, "HAIRCUT_FRESH_DAYS", 14), 14)

    def player_hygiene_look_value(wash_days=None):
        appearance = player.appearance
        days = _player_int(appearance.days_since_wash if wash_days is None else wash_days, 0)
        if days <= 0:
            return 20
        if days <= 1:
            return 12
        if days <= 2:
            return 4
        return -10

    def player_costume_condition_look_value(condition_value=None):
        appearance = player.appearance
        condition = _player_clamp_stat(appearance.costume_condition if condition_value is None else condition_value, 0, 100)
        return _player_int(round(float(condition) / 4.0), 0)

    def player_haircut_elapsed_days():
        appearance = player.appearance
        try:
            marker = _player_int(appearance.haircut_day, 0)
        except Exception:
            marker = 0
        elapsed = max(0, _player_int(dayspassed, 0) - marker)
        return max(elapsed, _player_int(appearance.days_since_haircut, 0))

    def player_current_dress_age_days(dress_code=""):
        appearance = player.appearance
        code = str(dress_code or appearance.current_dress or "").strip()
        if not code:
            return 0
        return appearance.dress_age_days(code, _player_int(dayspassed, 0))

    def player_dress_condition_from_age(dress_age_days=None):
        age_days = _player_int(player_current_dress_age_days() if dress_age_days is None else dress_age_days, 0)
        if age_days >= 42:
            return 0
        return max(0, 100 - int(round((float(age_days) / 42.0) * 50.0)))

    def player_look_breakdown():
        appearance = player.appearance
        haircut_days = player_haircut_elapsed_days()
        dress_age_days = player_current_dress_age_days(appearance.current_dress)
        dress_value = player_dress_look_value(appearance.current_dress)
        condition_value = player_costume_condition_look_value(player_dress_condition_from_age(dress_age_days))
        haircut_value = player_haircut_look_value(haircut_days)
        hygiene_value = player_hygiene_look_value(appearance.days_since_wash)
        soap_bonus = 10 if int(dayspassed or 0) <= int(SoapLookBonusUntilDay or -1) else 0
        appearance = _player_clamp_stat(dress_value + condition_value + haircut_value + hygiene_value + soap_bonus, 0, 100)
        return {
            "dress": dress_value,
            "condition": condition_value,
            "haircut": haircut_value,
            "hygiene": hygiene_value,
            "soap_bonus": soap_bonus,
            "haircut_days": haircut_days,
            "dress_age_days": dress_age_days,
            "look": appearance,
        }

    def player_soap_freshness_active():
        try:
            return int(dayspassed or 0) <= int(SoapLookBonusUntilDay or -1)
        except Exception:
            return False

    def player_condition_warning_lines():
        appearance = player.appearance
        lines = []
        wash_days = _player_int(appearance.days_since_wash, 0)
        haircut_days = _player_int(player_haircut_elapsed_days(), 0)
        dress_condition = _player_int(player_dress_condition_from_age(player_current_dress_age_days(appearance.current_dress)), 100)

        if wash_days >= 3:
            lines.append("От вас уже ощутимо несет потом и грязью. Это портит внешний вид и мешает нормальному разговору.")
        elif wash_days >= 2:
            lines.append("Вы заметно грязны после работы и дороги. Стоит помыться, пока запах не стал явным.")

        if haircut_days >= _player_int(getattr(appearance, "HAIRCUT_FRESH_DAYS", 14), 14):
            lines.append("Волосы отросли и выглядят неопрятно. Пора зайти к цирюльнику.")

        if str(appearance.current_dress or "").strip() != "":
            if dress_condition <= 25:
                lines.append("Одежда уже совсем потрепана и тянет ваш вид вниз. Нужен другой костюм или замена.")
            elif dress_condition <= 60:
                lines.append("Одежда заметно поношена. Пока в ней можно ходить, но она уже портит впечатление.")

        if int(crafting.soap_look_bonus_until_day or -1) >= 0 and not player_soap_freshness_active() and wash_days > 0:
            lines.append("Запах мыла уже выветрился. Свежий вид от последнего мытья больше не держится.")

        return lines

    def player_condition_warning_text():
        return "\n\n".join(player_condition_warning_lines())

    def _player_condition_notice_state():
        global PlayerConditionNoticeState
        if not isinstance(PlayerConditionNoticeState, dict):
            PlayerConditionNoticeState = {}
        return PlayerConditionNoticeState

    def _player_condition_notice_seen(key):
        state = _player_condition_notice_state()
        notice_key = str(key or "")
        day_key = str(dayspassed or 0)
        return str(state.get(notice_key, "")) == day_key

    def _player_condition_mark_notice_seen(key):
        state = _player_condition_notice_state()
        state[str(key or "")] = str(dayspassed or 0)

    def player_condition_daily_notice_lines():
        appearance = player.appearance
        lines = []
        wash_days = _player_int(appearance.days_since_wash, 0)
        haircut_days = _player_int(player_haircut_elapsed_days(), 0)
        dress_condition = _player_int(player_dress_condition_from_age(player_current_dress_age_days(appearance.current_dress)), 100)

        if wash_days >= 3 and not _player_condition_notice_seen("stink"):
            lines.append("От вас уже ощутимо несет грязью. Помыться нужно при первой возможности.")
            _player_condition_mark_notice_seen("stink")
        elif wash_days >= 2 and not _player_condition_notice_seen("dirty"):
            lines.append("Вы заметно грязны. Мытье сейчас даст пользу внешности и общению.")
            _player_condition_mark_notice_seen("dirty")

        if haircut_days >= _player_int(getattr(appearance, "HAIRCUT_FRESH_DAYS", 14), 14) and not _player_condition_notice_seen("haircut"):
            lines.append("Волосы отросли. Цирюльник уже не роскошь, а необходимость.")
            _player_condition_mark_notice_seen("haircut")

        if str(appearance.current_dress or "").strip() != "":
            if dress_condition <= 25 and not _player_condition_notice_seen("clothes_bad"):
                lines.append("Одежда выглядит совсем изношенной.")
                _player_condition_mark_notice_seen("clothes_bad")
            elif dress_condition <= 60 and not _player_condition_notice_seen("clothes_worn"):
                lines.append("Одежда заметно поношена.")
                _player_condition_mark_notice_seen("clothes_worn")

        soap_until = _player_int(crafting.soap_look_bonus_until_day, -1)
        if soap_until >= 0 and _player_int(dayspassed, 0) > soap_until and not _player_condition_notice_seen("soap_faded_%s" % soap_until):
            lines.append("Свежий запах мыла уже выветрился.")
            _player_condition_mark_notice_seen("soap_faded_%s" % soap_until)

        return lines

    def player_condition_maybe_notify():
        notice_lines = player_condition_daily_notice_lines()
        if len(notice_lines) <= 0:
            return
        try:
            renpy_module.notify(" ".join(notice_lines[:2]))
        except Exception:
            pass

    def player_children_count():
        try:
            return max(0, len(list(KidsList or [])))
        except Exception:
            return 0

    def effective_player_exploration():
        base_value = _player_int(exploration, 0)
        try:
            if bool(getattr(dog, "owned", False)):
                base_value += 25
        except Exception:
            pass
        return max(0, base_value)

    def player_quest_progress_score():
        score = 0

        try:
            if bool(roomFirstVisit.get("Forest", False)):
                score += 10
        except Exception:
            pass

        try:
            if _player_int(KnowMongol, 0) > 0:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(FranVar.get("meet", 0), 0) > 0:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(Liza.story_value("ProstStart", 0), 0) > 0:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(DraupnirVar.get("GloryHoleAsked", 0), 0) > 0 or _player_int(TavernGloryHole, 0) > 0:
                score += 15
        except Exception:
            pass

        try:
            if _player_int(Becky.var.get("visitedhome", 0), 0) >= 3:
                score += 15
        except Exception:
            pass

        try:
            if _player_int(Becky.var.get("AdmitSherwood", 0), 0) > 0 or _player_int(Becky.var.get("RobbedByRobin", 0), 0) >= 2:
                score += 15
        except Exception:
            pass

        try:
            if Amanda.var_int("knowlegaresex", 0) > 0 or Amanda.var_int("alberfriends", 0) >= 9:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(Zimmer.var.get("RobinInvestigationDay", 0), 0) > 0:
                score += 5
        except Exception:
            pass

        return _player_clamp_stat(score, 0, 100)

    def tavern_improvements_score():
        score = 0

        try:
            slogan_state = _player_int(player.tavern_management.slogan_state, 0)
            if slogan_state > 1:
                score += 20
            elif slogan_state == 1:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(player.tavern_management.client_room_hole, 0) > 0:
                score += 10
        except Exception:
            pass

        try:
            glory_state = _player_int(TavernGloryHole, 0)
            if glory_state >= 2:
                score += 20
            elif glory_state == 1:
                score += 10
        except Exception:
            pass

        try:
            score += min(20, max(0, int(round(float(_player_int(taverncleanliness, 0)) / 5.0)) - 10))
        except Exception:
            pass

        return _player_clamp_stat(score, 0, 100)

    def tavern_reputation_score():
        visitors_score = _player_clamp_stat(_player_int(player.tavern_management.visitors, 0), 0, 100)
        fame_score = _player_clamp_stat(50 + (_player_int(player.economy.tavern_fame, 0) * 5), 0, 100)
        improvements_score = tavern_improvements_score()
        dog_bonus = 0
        try:
            if bool(getattr(dog, "owned", False)):
                dog_bonus = 1
        except Exception:
            dog_bonus = 0
        return _player_clamp_stat(round((visitors_score * 0.45) + (fame_score * 0.30) + (improvements_score * 0.25)) + dog_bonus, 0, 100)

    def tavern_crew_interaction_bonus(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if key not in ("sandra", "melissa", "amanda"):
            return 0

        player_rep = _player_int(player_reputation_breakdown().get("reputation", 0), 0)
        tavern_rep = _player_int(tavern_reputation_score(), 0)
        bonus = 0
        if player_rep >= 50:
            bonus += 1
        if tavern_rep >= 50:
            bonus += 1
        return min(2, bonus)

    def girl_uses_behavioral_social_reactions(girl_name=""):
        return str(girl_name or "").strip().lower() in ("sandra", "melissa", "amanda", "clara")

    def player_social_condition_modifier(girl_name="", interaction_type="talk"):
        key = str(girl_name or "").strip().lower()
        interaction = str(interaction_type or "talk").strip().lower()
        if key not in ("sandra", "melissa", "amanda", "clara"):
            return {"score": 0, "reasons": []}

        breakdown = player_look_breakdown()
        charisma_info = player_charisma_breakdown()
        look_value = _player_int(breakdown.get("look", 0), 0)
        charisma_value = _player_int(charisma_info.get("charisma", 0), 0)
        appearance = player.appearance
        wash_days = _player_int(appearance.days_since_wash, 0)
        haircut_days = _player_int(breakdown.get("haircut_days", 0), 0)
        dress_condition = _player_int(player_dress_condition_from_age(player_current_dress_age_days(appearance.current_dress)), 100)

        score = 0
        reasons = []

        if look_value >= 85:
            score += 1
            reasons.append("опрятный вид")
        elif look_value <= 35:
            score -= 1
            reasons.append("плохой вид")

        if charisma_value >= 80:
            score += 1
            reasons.append("уверенная подача")

        if wash_days >= 3:
            score -= 2
            reasons.append("запах грязи")
        elif wash_days >= 2:
            score -= 1
            reasons.append("грязь после работы")

        if haircut_days >= _player_int(getattr(appearance, "HAIRCUT_FRESH_DAYS", 14), 14):
            score -= 1
            reasons.append("заросшая стрижка")

        if str(appearance.current_dress or "").strip() == "":
            score -= 1
            reasons.append("нет нормальной одежды")
        elif dress_condition <= 25:
            score -= 2
            reasons.append("изношенная одежда")
        elif dress_condition <= 60:
            score -= 1
            reasons.append("поношенная одежда")

        if interaction == "flirt" and key == "clara" and score < 0:
            score -= 1
            reasons.append("Кларисса особенно замечает небрежность")
        elif interaction in ("gift", "share") and key == "sandra" and score < 0:
            score -= 1
            reasons.append("Сандра видит хозяйскую небрежность")

        score = max(-3, min(2, score))
        return {"score": score, "reasons": reasons}

    def player_social_adjusted_delta(girl_name="", interaction_type="talk", base_score=0):
        key = str(girl_name or "").strip().lower()
        interaction = str(interaction_type or "talk").strip().lower()
        base_value = _player_int(base_score, 0)
        info = dict(player_social_condition_modifier(key, interaction) or {})
        condition_score = _player_int(info.get("score", 0), 0)
        if not isinstance(PlayerSocialConditionLast, dict):
            PlayerSocialConditionLast = {}
        PlayerSocialConditionLast[key] = {
            "day": _player_int(dayspassed, 0),
            "interaction": interaction,
            "score": condition_score,
            "reasons": list(info.get("reasons", []) or []),
            "base": base_value,
            "total": max(-5, min(5, base_value + condition_score)),
        }
        return max(-5, min(5, base_value + condition_score))

    def player_social_condition_notice_text(girl_name=""):
        key = str(girl_name or "").strip().lower()
        try:
            row = dict(PlayerSocialConditionLast.get(key, {}) or {})
        except Exception:
            row = {}
        score = _player_int(row.get("score", 0), 0)
        reasons = [str(reason or "").strip() for reason in list(row.get("reasons", []) or []) if str(reason or "").strip()]
        if score == 0 or not reasons:
            return ""
        sign = "+%d" % score if score > 0 else str(score)
        return "Влияние внешности: %s (%s)." % (sign, ", ".join(reasons[:3]))

    def player_social_condition_notify(girl_name=""):
        text = player_social_condition_notice_text(girl_name)
        if not text:
            return ""
        try:
            renpy_module.notify(text)
        except Exception:
            pass
        return text

    def preferred_gift_item_ids(girl_name=""):
        key = str(girl_name or "").strip()
        if not isinstance(GiftPreferences, dict):
            return []
        if not isinstance(GiftPreferences, dict):
            return []
        return [str(row or "").strip() for row in list(GiftPreferences.get(key, []) or []) if str(row or "").strip()]

    def resolve_player_social_delta(girl_name="", interaction_type="talk", base_gain=None, gift_item_id=""):
        import random

        key = str(girl_name or "").strip()
        interaction = str(interaction_type or "talk").strip().lower()
        if key == "":
            return 0

        social_bonus = int(player_social_interaction_bonus() or 0)
        tavern_bonus = int(tavern_crew_interaction_bonus(key) or 0)
        info = getPersonInfo(key)
        mood_points = 0
        mood_points += min(4, max(0, _player_int(getattr(info, "rel", 0), 0) // 5)) if info is not None else 0
        mood_points += min(2, max(0, _player_int(getattr(info, "corruption", 0), 0) // 20)) if info is not None else 0
        mood_points += min(2, social_bonus + tavern_bonus)
        if info is not None and int(getattr(info, "drunk", 0) or 0) > 0:
            mood_points += 1

        if interaction == "talk":
            repeats_today = int(getattr(info, "talked_today", 0) or 0) if info is not None else 0
            default_gain = 1
        elif interaction == "flirt":
            repeats_today = int(getattr(info, "flirted_today", 0) or 0) if info is not None else 0
            default_gain = 1
        else:
            repeats_today = int(GiftedToday.get(key, 0) or 0)
            default_gain = int(base_gain if base_gain is not None else 2)

        if repeats_today > 0:
            if girl_uses_behavioral_social_reactions(key):
                return player_social_adjusted_delta(key, interaction, -1 if random.randint(1, 3) == 1 else 0)
            return player_social_adjusted_delta(key, interaction, 0)

        if interaction == "gift":
            preferred_items = preferred_gift_item_ids(key)
            item_id = str(gift_item_id or "").strip()
            if item_id != "":
                if item_id in preferred_items:
                    return player_social_adjusted_delta(key, interaction, max(1, default_gain + social_bonus + tavern_bonus))
                if girl_uses_behavioral_social_reactions(key):
                    return player_social_adjusted_delta(key, interaction, -1 if random.randint(1, 2) == 1 else 0)
                return player_social_adjusted_delta(key, interaction, 0)

        if girl_uses_behavioral_social_reactions(key):
            roll = random.randint(1, 6)
            if interaction == "flirt":
                if mood_points >= roll + 2:
                    return player_social_adjusted_delta(key, interaction, max(1, default_gain + social_bonus))
                if mood_points + 1 >= roll:
                    return player_social_adjusted_delta(key, interaction, 0)
                return player_social_adjusted_delta(key, interaction, -1)
            if interaction == "talk":
                if mood_points >= roll + 1:
                    return player_social_adjusted_delta(key, interaction, max(1, default_gain + social_bonus))
                if mood_points >= roll - 1:
                    return player_social_adjusted_delta(key, interaction, 0)
                return player_social_adjusted_delta(key, interaction, -1)
            if mood_points >= roll + 1:
                return player_social_adjusted_delta(key, interaction, max(1, default_gain + social_bonus))
            if mood_points >= roll - 1:
                return player_social_adjusted_delta(key, interaction, 0)
            return player_social_adjusted_delta(key, interaction, -1)

        return player_social_adjusted_delta(key, interaction, max(0, default_gain + social_bonus + (1 if tavern_bonus >= 2 else 0)))

    def player_charisma_breakdown():
        look_value = _player_int(player_look_breakdown().get("look", 0), 0)
        exploration_score = min(20, effective_player_exploration() * 2)
        charisma_value = _player_clamp_stat(look_value + exploration_score, 0, 100)
        return {
            "look": look_value,
            "exploration": exploration_score,
            "charisma": charisma_value,
        }

    def player_social_interaction_bonus():
        charisma_value = _player_int(player_charisma_breakdown().get("charisma", 0), 0)
        if charisma_value >= 90:
            return 2
        if charisma_value >= 70:
            return 1
        return 0

    def player_reputation_breakdown():
        look_value = _player_int(player_look_breakdown().get("look", 0), 0)
        quest_score = _player_int(player_quest_progress_score(), 0)
        children_score = min(100, player_children_count() * 20)
        exploration_score = min(100, effective_player_exploration() * 5)
        horse_score = 5 if bool(str(MyStallion or "").strip()) else 0
        hunter_score = min(20, max(0, _player_int(globals().get("HunterClubVar", {}).get("reputation", 0), 0)))
        reputation_value = _player_clamp_stat(round(
            (look_value * 0.60)
            + (quest_score * 0.15)
            + (exploration_score * 0.15)
            + (children_score * 0.10)
        ) + horse_score + hunter_score, 0, 100)
        return {
            "look": look_value,
            "quest": quest_score,
            "children": children_score,
            "exploration": exploration_score,
            "horse": horse_score,
            "hunter": hunter_score,
            "reputation": reputation_value,
            "children_count": player_children_count(),
        }

    def update_stat_state():
        global look, reputation, charisma

        try:
        except Exception:
            pass
        global look, reputation, charisma, charisma

        appearance = player.appearance
        appearance.days_since_haircut = _player_int(player_haircut_elapsed_days(), 0)
        appearance.hairCutdays = max(0, _player_int(getattr(appearance, "HAIRCUT_FRESH_DAYS", 14), 14) - appearance.days_since_haircut)
        appearance.washDays = max(0, _player_int(getattr(appearance, "WASH_FRESH_DAYS", 3), 3) - _player_int(appearance.days_since_wash, 0))
        appearance.costume_condition = _player_int(player_dress_condition_from_age(player_current_dress_age_days(appearance.current_dress)), 0)
        look = _player_int(player_look_breakdown().get("look", 0), 0)
        reputation = _player_int(player_reputation_breakdown().get("reputation", 0), 0)
        charisma = _player_int(player_charisma_breakdown().get("charisma", 0), 0)
        look = _player_int(player_look_breakdown().get("look", 0), 0)
        reputation = _player_int(player_reputation_breakdown().get("reputation", 0), 0)
        charisma = _player_int(player_charisma_breakdown().get("charisma", 0), 0)
        look = _player_int(player_look_breakdown().get("look", 0), 0)
        reputation = _player_int(player_reputation_breakdown().get("reputation", 0), 0)
        charisma = _player_int(player_charisma_breakdown().get("charisma", 0), 0)
        player_condition_maybe_notify()


label stat:
    $ update_stat_state()
    return
