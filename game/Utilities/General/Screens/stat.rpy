# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init python:
    import renpy.exports as renpy_module

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
        dress_map = dict(DressLookValue or {})
        if code in dress_map:
            return _player_int(dress_map.get(code, 15), 15)
        if code == "nightshirt":
            return 8
        if code in tuple(MaleDressCodes or []):
            return 20
        return 24

    def player_haircut_look_value(haircut_days=None):
        appearance = player.appearance
        days = _player_int(appearance.days_since_haircut if haircut_days is None else haircut_days, 0)
        return 15 if days < appearance.HAIRCUT_FRESH_DAYS else -40

    def player_hygiene_look_value(wash_days=None):
        appearance = player.appearance
        days = _player_int(appearance.days_since_wash if wash_days is None else wash_days, 0)
        if days <= 0:
            return 20
        if days <= 1:
            return 12
        if days < appearance.WASH_FRESH_DAYS:
            return 4
        return -10

    def player_costume_condition_look_value(condition_value=None):
        appearance = player.appearance
        condition = _player_clamp_stat(appearance.dress_condition() if condition_value is None else condition_value, 0, 100)
        return _player_int(round(float(condition) / 4.0), 0)

    def player_haircut_elapsed_days():
        return max(0, _player_int(player.appearance.days_since_haircut, 0))

    def player_current_dress_age_days(dress_code=""):
        appearance = player.appearance
        code = str(dress_code or appearance.current_dress or "").strip()
        if not code:
            return 0
        return appearance.dress_age_days(code, current_game_day())

    def player_look_breakdown():
        appearance = player.appearance
        haircut_days = player_haircut_elapsed_days()
        dress_age_days = player_current_dress_age_days(appearance.current_dress)
        dress_value = player_dress_look_value(appearance.current_dress)
        condition_value = player_costume_condition_look_value(appearance.dress_condition(appearance.current_dress))
        haircut_value = player_haircut_look_value(haircut_days)
        hygiene_value = player_hygiene_look_value(appearance.days_since_wash)
        soap_bonus = _player_int(appearance.soap_look_bonus, 0) if current_game_day() <= int(appearance.soap_look_bonus_until_day or -1) else 0
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
        return current_game_day() <= int(player.appearance.soap_look_bonus_until_day or -1)

    def player_condition_warning_lines():
        appearance = player.appearance
        lines = []
        wash_days = _player_int(appearance.days_since_wash, 0)
        haircut_days = _player_int(player_haircut_elapsed_days(), 0)
        dress_condition = _player_int(appearance.dress_condition(appearance.current_dress), 100)

        if wash_days >= 3:
            lines.append("От вас уже ощутимо несет потом и грязью. Это портит внешний вид и мешает нормальному разговору.")
        elif wash_days >= 2:
            lines.append("Вы заметно грязны после работы и дороги. Стоит помыться, пока запах не стал явным.")

        if haircut_days >= appearance.HAIRCUT_FRESH_DAYS:
            lines.append("Волосы отросли и выглядят неопрятно. Пора зайти к цирюльнику.")

        if str(appearance.current_dress or "").strip() != "":
            if dress_condition <= 25:
                lines.append("Одежда уже совсем потрепана и тянет ваш вид вниз. Нужен другой костюм или замена.")
            elif dress_condition <= 60:
                lines.append("Одежда заметно поношена. Пока в ней можно ходить, но она уже портит впечатление.")

        if int(appearance.soap_look_bonus_until_day or -1) >= 0 and not player_soap_freshness_active() and wash_days > 0:
            lines.append("Запах мыла уже выветрился. Свежий вид от последнего мытья больше не держится.")

        return lines

    def player_condition_warning_text():
        return "\n\n".join(player_condition_warning_lines())

    def _player_condition_notice_state():
        return player.condition.notice_state

    def _player_condition_notice_seen(key):
        state = _player_condition_notice_state()
        notice_key = str(key or "")
        day_key = str(current_game_day())
        return str(state.get(notice_key, "")) == day_key

    def _player_condition_mark_notice_seen(key):
        state = _player_condition_notice_state()
        state[str(key or "")] = str(current_game_day())

    def player_condition_daily_notice_lines():
        appearance = player.appearance
        lines = []
        wash_days = _player_int(appearance.days_since_wash, 0)
        haircut_days = _player_int(player_haircut_elapsed_days(), 0)
        dress_condition = _player_int(appearance.dress_condition(appearance.current_dress), 100)

        if wash_days >= 3 and not _player_condition_notice_seen("stink"):
            lines.append("От вас уже ощутимо несет грязью. Помыться нужно при первой возможности.")
            _player_condition_mark_notice_seen("stink")
        elif wash_days >= 2 and not _player_condition_notice_seen("dirty"):
            lines.append("Вы заметно грязны. Мытье сейчас даст пользу внешности и общению.")
            _player_condition_mark_notice_seen("dirty")

        if haircut_days >= appearance.HAIRCUT_FRESH_DAYS and not _player_condition_notice_seen("haircut"):
            lines.append("Волосы отросли. Цирюльник уже не роскошь, а необходимость.")
            _player_condition_mark_notice_seen("haircut")

        if str(appearance.current_dress or "").strip() != "":
            if dress_condition <= 25 and not _player_condition_notice_seen("clothes_bad"):
                lines.append("Одежда выглядит совсем изношенной.")
                _player_condition_mark_notice_seen("clothes_bad")
            elif dress_condition <= 60 and not _player_condition_notice_seen("clothes_worn"):
                lines.append("Одежда заметно поношена.")
                _player_condition_mark_notice_seen("clothes_worn")

        soap_until = _player_int(appearance.soap_look_bonus_until_day, -1)
        if soap_until >= 0 and current_game_day() > soap_until and not _player_condition_notice_seen("soap_faded_%s" % soap_until):
            lines.append("Свежий запах мыла уже выветрился.")
            _player_condition_mark_notice_seen("soap_faded_%s" % soap_until)

        return lines

    def player_condition_maybe_notify():
        notice_lines = player_condition_daily_notice_lines()
        if len(notice_lines) <= 0:
            return
        renpy_module.notify(" ".join(notice_lines[:2]))

    def player_children_count():
        return len(_kids_list())

    def effective_player_exploration():
        base_value = _player_int(player.stats.exploration, 0)
        if dog.owned:
            base_value += 25
        return max(0, base_value)

    def player_quest_progress_score():
        score = 0

        if not rooms.get("Forest").is_first_visit():
            score += 10
        if Mongol.known:
            score += 10
        if Francheska.met:
            score += 10
        if Liza.prostitution_started:
            score += 10
        if Draupnir.glory_hole_quote_received or _player_int(player.tavern_management.glory_hole, 0) > 0:
            score += 15
        if threads["beckyHome"].completed:
            score += 15
        if _player_int(Becky.admitted_sherwood_stage, 0) > 0 or _player_int(Becky.robin_robbery_stage, 0) >= 2:
            score += 15
        if Amanda.player_knows_legare_sex or Amanda.legare_affection >= 9:
            score += 10
        if _player_int(Zimmer.robin_investigation_day, 0) > 0:
            score += 5

        return _player_clamp_stat(score, 0, 100)

    def tavern_improvements_score():
        score = 0

        slogan_state = _player_int(player.tavern_management.slogan_state, 0)
        if slogan_state > 1:
            score += 20
        elif slogan_state == 1:
            score += 10
        if _player_int(player.tavern_management.client_room_hole, 0) > 0:
            score += 10
        glory_state = _player_int(player.tavern_management.glory_hole, 0)
        if glory_state >= 2:
            score += 20
        elif glory_state == 1:
            score += 10
        score += min(20, max(0, int(round(float(_player_int(player.tavern_management.cleanliness, 0)) / 5.0)) - 10))

        return _player_clamp_stat(score, 0, 100)

    def tavern_reputation_score():
        visitors_score = _player_clamp_stat(_player_int(player.tavern_management.visitors, 0), 0, 100)
        fame_score = _player_clamp_stat(50 + (_player_int(player.economy.tavern_fame, 0) * 5), 0, 100)
        improvements_score = tavern_improvements_score()
        dog_bonus = 1 if dog.owned else 0
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
        dress_condition = _player_int(appearance.dress_condition(appearance.current_dress), 100)

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

        if haircut_days >= appearance.HAIRCUT_FRESH_DAYS:
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
        girl_info = people.get_info(key)
        if girl_info is not None:
            girl_info.var["player_social_condition_last"] = {
            "day": current_game_day(),
            "interaction": interaction,
            "score": condition_score,
            "reasons": list(info.get("reasons", []) or []),
            "base": base_value,
            "total": max(-5, min(5, base_value + condition_score)),
        }
        return max(-5, min(5, base_value + condition_score))

    def player_social_condition_notice_text(girl_name=""):
        key = str(girl_name or "").strip().lower()
        girl_info = people.get_info(key)
        row = dict(getattr(girl_info, "var", {}).get("player_social_condition_last", {}) or {})
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
        renpy_module.notify(text)
        return text

    def preferred_gift_item_ids(girl_name=""):
        key = str(girl_name or "").strip()
        return [str(row or "").strip() for row in people_gift_preferences(key) if str(row or "").strip()]

    def resolve_player_social_delta(girl_name="", interaction_type="talk", base_gain=None, gift_item_id=""):
        key = str(girl_name or "").strip()
        interaction = str(interaction_type or "talk").strip().lower()
        if key == "":
            return 0

        social_bonus = int(player_social_interaction_bonus() or 0)
        tavern_bonus = int(tavern_crew_interaction_bonus(key) or 0)
        info = people.get_info(key)
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
            repeats_today = int(getattr(info, "gifted_today", 0) or 0) if info is not None else 0
            default_gain = int(base_gain if base_gain is not None else 2)

        if repeats_today > 0:
            if girl_uses_behavioral_social_reactions(key):
                repeat_roll = procedural_randint(1, 3, "social_repeat_%s_%s_%s_%s" % (key, interaction, current_game_day(), repeats_today))
                return player_social_adjusted_delta(key, interaction, -1 if repeat_roll == 1 else 0)
            return player_social_adjusted_delta(key, interaction, 0)

        if interaction == "gift":
            preferred_items = preferred_gift_item_ids(key)
            item_id = str(gift_item_id or "").strip()
            if item_id != "":
                if item_id in preferred_items:
                    return player_social_adjusted_delta(key, interaction, max(1, default_gain + social_bonus + tavern_bonus))
                if girl_uses_behavioral_social_reactions(key):
                    gift_roll = procedural_randint(1, 2, "social_gift_%s_%s_%s" % (key, item_id, current_game_day()))
                    return player_social_adjusted_delta(key, interaction, -1 if gift_roll == 1 else 0)
                return player_social_adjusted_delta(key, interaction, 0)

        if girl_uses_behavioral_social_reactions(key):
            roll = procedural_randint(1, 6, "social_reaction_%s_%s_%s_%s" % (key, interaction, current_game_day(), repeats_today))
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
        progression_value = _player_int(player.stats.charisma, 0)
        charisma_value = _player_clamp_stat(progression_value + look_value + exploration_score, 0, 100)
        return {
            "progression": progression_value,
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
        horse_score = 5 if player.horse.owns_horse() else 0
        hunter_score = min(20, max(0, _player_int(rooms.get("HunterClub").state.get("reputation", 0), 0)))
        progression_value = _player_int(player.stats.reputation, 0)
        reputation_value = _player_clamp_stat(round(
            (look_value * 0.60)
            + (quest_score * 0.15)
            + (exploration_score * 0.15)
            + (children_score * 0.10)
        ) + progression_value + horse_score + hunter_score, 0, 100)
        return {
            "progression": progression_value,
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
        player_condition_maybe_notify()


label stat:
    $ update_stat_state()
    return
