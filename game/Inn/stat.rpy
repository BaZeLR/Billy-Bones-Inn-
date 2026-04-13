init python:
    def _player_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return default

    def _player_clamp_stat(value, low=0, high=100):
        return max(int(low), min(int(high), _player_int(value, low)))

    def player_dress_look_value(dress_code=""):
        code = str(dress_code or MyCurDress or "").strip()
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
        if code in tuple(globals().get("MaleDressCodes", []) or []):
            return 20
        return 24

    def player_haircut_look_value(haircut_days=None):
        days = _player_int(dayssincehaircut if haircut_days is None else haircut_days, 0)
        return 15 if days <= 25 else -40

    def player_haircut_due_day():
        marker = _player_int(PlayerHaircutDaySt, 0)
        return marker + 25

    def player_hygiene_look_value(wash_days=None):
        days = _player_int(dayssincewash if wash_days is None else wash_days, 0)
        if days <= 0:
            return 20
        if days <= 1:
            return 16
        if days <= 2:
            return 10
        if days <= 3:
            return 4
        if days <= 4:
            return 0
        return -10

    def player_costume_condition_look_value(condition_value=None):
        condition = _player_clamp_stat(costumecondition if condition_value is None else condition_value, 0, 100)
        return _player_int(round(float(condition) / 4.0), 0)

    def player_haircut_elapsed_days():
        try:
            marker = _player_int(PlayerHaircutDaySt, 0)
        except Exception:
            marker = 0
        elapsed = max(0, _player_int(dayspassed, 0) - marker)
        return max(elapsed, _player_int(dayssincehaircut, 0))

    def player_current_dress_age_days(dress_code=""):
        code = str(dress_code or MyCurDress or "").strip()
        if not code:
            return 0
        try:
            if not isinstance(PlayerDressDaySt, dict):
                globals()["PlayerDressDaySt"] = {}
            dress_days = PlayerDressDaySt
        except Exception:
            globals()["PlayerDressDaySt"] = {}
            dress_days = PlayerDressDaySt
        if code not in dress_days:
            dress_days[code] = _player_int(dayspassed, 0)
        return max(0, _player_int(dayspassed, 0) - _player_int(dress_days.get(code, 0), 0))

    def player_dress_condition_from_age(dress_age_days=None):
        age_days = _player_int(player_current_dress_age_days() if dress_age_days is None else dress_age_days, 0)
        if age_days >= 42:
            return 0
        return max(0, 100 - int(round((float(age_days) / 42.0) * 50.0)))

    def player_look_breakdown():
        haircut_days = player_haircut_elapsed_days()
        dress_age_days = player_current_dress_age_days(MyCurDress)
        dress_value = player_dress_look_value(MyCurDress)
        condition_value = player_costume_condition_look_value(player_dress_condition_from_age(dress_age_days))
        haircut_value = player_haircut_look_value(haircut_days)
        hygiene_value = player_hygiene_look_value(dayssincewash)
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
            if _player_int(LizaVar.get("ProstStart", 0), 0) > 0:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(DraupnirVar.get("GloryHoleAsked", 0), 0) > 0 or _player_int(TavernGloryHole, 0) > 0:
                score += 15
        except Exception:
            pass

        try:
            if _player_int(BeckyVar.get("visitedhome", 0), 0) >= 3:
                score += 15
        except Exception:
            pass

        try:
            if _player_int(BeckyVar.get("AdmitSherwood", 0), 0) > 0 or _player_int(BeckyVar.get("RobbedByRobin", 0), 0) >= 2:
                score += 15
        except Exception:
            pass

        try:
            if _player_int(AmandaVar.get("knowlegaresex", 0), 0) > 0 or _player_int(AmandaVar.get("alberfriends", 0), 0) >= 9:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(ZimmerVar.get("RobinInvestigationDay", 0), 0) > 0:
                score += 5
        except Exception:
            pass

        return _player_clamp_stat(score, 0, 100)

    def tavern_improvements_score():
        score = 0

        try:
            slogan_state = _player_int(SloganFixed, 0)
            if slogan_state > 1:
                score += 20
            elif slogan_state == 1:
                score += 10
        except Exception:
            pass

        try:
            if _player_int(TavernHole, 0) > 0:
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
        visitors_score = _player_clamp_stat(_player_int(tavernvisitors, 0), 0, 100)
        fame_score = _player_clamp_stat(50 + (_player_int(tavernfame, 0) * 5), 0, 100)
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

    def preferred_gift_item_ids(girl_name=""):
        key = str(girl_name or "").strip()
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
        mood_points = 0
        mood_points += min(4, max(0, _player_int(Friends.get(key, 0), 0) // 5))
        mood_points += min(2, max(0, _player_int(sluttiness.get(key, 0), 0) // 20))
        mood_points += min(2, social_bonus + tavern_bonus)
        if int(Drunk.get(key, 0) or 0) > 0:
            mood_points += 1

        if interaction == "talk":
            repeats_today = int(TalkedToday.get(key, 0) or 0)
            default_gain = 1
        elif interaction == "flirt":
            repeats_today = int(FlirtedToday.get(key, 0) or 0)
            default_gain = 1
        else:
            repeats_today = int(GiftedToday.get(key, 0) or 0)
            default_gain = int(base_gain if base_gain is not None else 2)

        if repeats_today > 0:
            if girl_uses_behavioral_social_reactions(key):
                return -1 if random.randint(1, 3) == 1 else 0
            return 0

        if interaction == "gift":
            preferred_items = preferred_gift_item_ids(key)
            item_id = str(gift_item_id or "").strip()
            if item_id != "":
                if item_id in preferred_items:
                    return max(1, default_gain + social_bonus + tavern_bonus)
                if girl_uses_behavioral_social_reactions(key):
                    return -1 if random.randint(1, 2) == 1 else 0
                return 0

        if girl_uses_behavioral_social_reactions(key):
            roll = random.randint(1, 6)
            if interaction == "flirt":
                if mood_points >= roll + 2:
                    return max(1, default_gain + social_bonus)
                if mood_points + 1 >= roll:
                    return 0
                return -1
            if interaction == "talk":
                if mood_points >= roll + 1:
                    return max(1, default_gain + social_bonus)
                if mood_points >= roll - 1:
                    return 0
                return -1
            if mood_points >= roll + 1:
                return max(1, default_gain + social_bonus)
            if mood_points >= roll - 1:
                return 0
            return -1

        return max(0, default_gain + social_bonus + (1 if tavern_bonus >= 2 else 0))

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
        reputation_value = _player_clamp_stat(round(
            (look_value * 0.60)
            + (quest_score * 0.15)
            + (exploration_score * 0.15)
            + (children_score * 0.10)
        ) + horse_score, 0, 100)
        return {
            "look": look_value,
            "quest": quest_score,
            "children": children_score,
            "exploration": exploration_score,
            "horse": horse_score,
            "reputation": reputation_value,
            "children_count": player_children_count(),
        }

    def update_stat_state():
        calendar_sync_state()
        try:
            fight_sync_level_from_exploration()
            fight_sync_supply_from_inventory()
        except Exception:
            pass
        try:
            soap_expire_if_needed()
        except Exception:
            pass
        globals()["dayssincehaircut"] = _player_int(player_haircut_elapsed_days(), 0)
        globals()["costumecondition"] = _player_int(player_dress_condition_from_age(player_current_dress_age_days(MyCurDress)), 0)
        globals()["look"] = _player_int(player_look_breakdown().get("look", 0), 0)
        globals()["notoriety"] = _player_int(player_reputation_breakdown().get("reputation", 0), 0)
        globals()["charisma"] = _player_int(player_charisma_breakdown().get("charisma", 0), 0)


label stat:
    $ update_stat_state()
    return
