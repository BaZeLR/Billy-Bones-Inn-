# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -34 python:
    import math

    GIRL_DECISION_CORE_IDS = ("amanda", "melissa", "sandra")
    GIRL_DECISION_CYCLE_IDS = ("amanda", "melissa", "sandra", "clara", "irma", "inga", "becky")

    GIRL_DECISION_PREFS = {
        "amanda": {
            "watching": 2,
            "being_watched": 1,
            "teasing": 2,
            "nipple": 2,
            "oral": 1,
            "anal": 0,
            "spanking": 0,
            "cowgirl": 0,
        },
        "melissa": {
            "watching": 1,
            "being_watched": 2,
            "teasing": 1,
            "nipple": 0,
            "oral": 2,
            "anal": 2,
            "spanking": 0,
            "girls": 2,
        },
        "sandra": {
            "watching": 0,
            "being_watched": 1,
            "teasing": 1,
            "nipple": 0,
            "oral": 2,
            "anal": 0,
            "spanking": 2,
            "cowgirl": 2,
        },
    }

    GIRL_DECISION_ACTION_WEIGHTS = {
        "peek_window_confront": {
            "good": {
                "trust": 2.0,
                "openness": 1.6,
                "sexual_openness": 2.2,
                "arousal": 1.1,
                "wetness": 1.0,
                "player_history": 1.6,
                "watching_pref": 0.8,
                "soap_bonus": 0.4,
                "barber_bonus": 0.4,
                "cycle_horny": 0.5,
                "rebel": -1.2,
                "anger": -2.4,
                "jealousy": -0.8,
            },
            "bad": {
                "anger": 2.0,
                "rebel": 1.5,
                "jealousy": 1.0,
                "trust": -1.1,
                "openness": -0.8,
                "player_history": -1.0,
                "sexual_openness": -0.8,
            },
        },
        "breakfast_alt_cure": {
            "good": {
                "trust": 1.2,
                "openness": 1.3,
                "sexual_openness": 2.0,
                "arousal": 1.4,
                "wetness": 1.4,
                "watching_pref": 0.6,
                "teasing_pref": 0.5,
                "breakfast_perk": 0.6,
                "cycle_horny": 0.4,
                "anger": -1.6,
                "rebel": -0.6,
            },
            "bad": {
                "anger": 1.4,
                "rebel": 0.9,
                "trust": -0.7,
                "openness": -0.6,
            },
        },
        "tease": {
            "good": {
                "trust": 1.0,
                "openness": 1.2,
                "sexual_openness": 1.6,
                "teasing_pref": 0.8,
                "soap_bonus": 0.5,
                "barber_bonus": 0.7,
                "breakfast_perk": 0.9,
                "cycle_horny": 0.5,
                "anger": -1.2,
            },
            "bad": {
                "anger": 1.4,
                "rebel": 0.6,
                "jealousy": 0.8,
                "trust": -0.5,
            },
        },
        "favor": {
            "good": {
                "trust": 1.8,
                "openness": 0.9,
                "soap_bonus": 0.4,
                "barber_bonus": 0.3,
                "church_obey": 0.8,
                "need_pressure": 0.7,
                "anger": -1.5,
                "rebel": -1.2,
            },
            "bad": {
                "anger": 1.7,
                "rebel": 1.4,
                "trust": -0.9,
                "church_obey": -0.4,
            },
        },
        "intimate_help": {
            "good": {
                "trust": 1.7,
                "openness": 1.3,
                "sexual_openness": 2.4,
                "arousal": 1.5,
                "wetness": 1.2,
                "player_history": 1.5,
                "oral_pref": 0.8,
                "teasing_pref": 0.6,
                "cycle_horny": 0.7,
                "anger": -2.2,
                "rebel": -0.5,
            },
            "bad": {
                "anger": 2.0,
                "rebel": 1.1,
                "trust": -1.0,
                "openness": -0.7,
                "sexual_openness": -1.0,
                "church_obey": 0.8,
            },
        },
    }

    def girl_decision_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return int(default or 0)

    def girl_decision_clamp(value, low=0.0, high=1.0):
        try:
            number = float(value)
        except Exception:
            number = float(low)
        return max(float(low), min(float(high), number))

    def girl_decision_ratio(value, scale):
        return girl_decision_clamp(float(girl_decision_int(value, 0)) / max(1.0, float(scale or 1.0)))

    def girl_decision_sigmoid(score):
        try:
            return 1.0 / (1.0 + math.exp(-float(score)))
        except Exception:
            return 0.5

    def girl_decision_pref(girl_name="", pref_name=""):
        girl = str(girl_name or "").strip().lower()
        pref = str(pref_name or "").strip().lower()
        return girl_decision_ratio(dict(GIRL_DECISION_PREFS.get(girl, {}) or {}).get(pref, 0), 2)

    def girl_decision_cycle_state(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl not in GIRL_DECISION_CYCLE_IDS:
            return {"phase": "none", "horny": 0.0, "critical": 0.0, "fertility": 0.0}
        offset = (sum([ord(ch) for ch in girl]) + girl_decision_int(people_birth_date(girl).get("day", 0), 0)) % 28
        day_index = (current_game_day() + offset) % 28
        if day_index in (0, 1, 2):
            return {"phase": "critical", "horny": 0.05, "critical": 1.0, "fertility": 0.25}
        if 10 <= day_index <= 15:
            return {"phase": "fertile", "horny": 0.35, "critical": 0.0, "fertility": 1.0}
        if 21 <= day_index <= 27:
            return {"phase": "restless", "horny": 0.20, "critical": 0.0, "fertility": 0.35}
        return {"phase": "steady", "horny": 0.10, "critical": 0.0, "fertility": 0.45}

    def girl_decision_recent_barber_bonus(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        last_day = girl_decision_int(household.barber_visit_last_day.get(girl, -99), -99)
        if last_day >= 0 and current_game_day() - last_day <= 14:
            return 1.0
        if int(household.barber_appointments.get(girl, 0) or 0) == 1:
            return 0.35
        return 0.0

    def girl_decision_soap_bonus(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        score = 0.0
        try:
            if int(crafting.soap_requests.get(girl, 0) or 0) > 0:
                score += 0.25
        except Exception:
            pass
        try:
            if current_game_day() - int(household.soap_request_last_day.get(girl, -99) or -99) <= 7:
                score += 0.20
        except Exception:
            pass
        return girl_decision_clamp(score)

    def girl_decision_church_obey_bonus(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        score = 0.0
        try:
            if int(calendar_v2.week or 0) == 7 and str(people.location(girl) or "") == "Church":
                score += 0.35
        except Exception:
            pass
        try:
            if int(player.economy.church_donated_today or 0) > 0:
                score += 0.15
            score += min(0.35, max(0.0, float(girl_decision_int(player.economy.church_donated_amount, 0)) / 1000.0))
        except Exception:
            pass
        return girl_decision_clamp(score)

    def girl_decision_breakfast_perk(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        try:
            return girl_decision_clamp(float(tavern_breakfast_player_perk_score(girl)) / 20.0)
        except Exception:
            pass
        return 0.0

    def girl_decision_need_pressure(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        score = 0.0
        try:
            issue = str(household_morning_issue_type(girl) or "")
            if issue == "sick":
                score += 0.5
            elif issue == "sleepy":
                score += 0.3
        except Exception:
            pass
        try:
            if int(crafting.soap_requests.get(girl, 0) or 0) > 0:
                score += 0.25
        except Exception:
            pass
        return girl_decision_clamp(score)

    def girl_decision_jealousy(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        if girl == "amanda":
            score = 0.0
            if Amanda.legare_affection >= 10 and not Amanda.legare_forbidden:
                score += 0.25
            if Amanda.var_int("prohibitwithguys", 0) > 0:
                score += 0.25
            if Amanda.var_int("sawwithguys", 0) > 0 and int(Amanda.rel or 0) >= 10:
                score += 0.20
            return girl_decision_clamp(score)
        return 0.0

    def build_girl_decision_profile(girl_name=""):
        girl = str(girl_name or "").strip().lower()
        cycle = girl_decision_cycle_state(girl)
        girl_info = people.get_info(girl)
        if girl_info is not None:
            friend = girl_decision_int(getattr(girl_info, "rel", 0), 0)
            open_value = girl_decision_int(getattr(girl_info, "openness", 0), 0)
            slut_value = girl_decision_int(getattr(girl_info, "corruption", 0), 0)
            stats = getattr(girl_info, "stats", {})
            if not isinstance(stats, dict):
                stats = {}
            if hasattr(girl_info, "arousal_value"):
                arousal_value = girl_decision_int(girl_info.arousal_value(), 0)
            else:
                arousal_value = girl_decision_int(stats.get("arousal", 0), 0)
            wet_value = max(girl_decision_int(stats.get("PussyWetStart", 0), 0), arousal_value)
        else:
            friend = 0
            open_value = 0
            slut_value = 0
            arousal_value = 0
            wet_value = 0
        anger_value = relationship_anger(girl)
        rebel_value = girl_decision_int(getattr(girl_info, "rebellion", 0), 0) if girl_info is not None else 0

        player_history = 0
        if girl == "amanda":
            player_history = 1 if Amanda.var_int("suckyou", 0) or Amanda.var_int("fuckyou", 0) else 0
        elif girl_info is not None:
            player_history = 1 if girl_decision_int(girl_info.sex_stat("sexacts", 0), 0) > 0 else 0

        profile = {
            "girl": girl,
            "friend_value": friend,
            "openness_value": open_value,
            "sexual_openness_value": slut_value,
            "arousal_value": arousal_value,
            "wetness_value": wet_value,
            "anger_value": anger_value,
            "rebel_value": rebel_value,
            "trust": girl_decision_ratio(friend, 20),
            "openness": girl_decision_ratio(open_value, 20),
            "sexual_openness": girl_decision_ratio(slut_value, 100),
            "arousal": girl_decision_ratio(arousal_value, 100),
            "wetness": girl_decision_ratio(wet_value, 100),
            "anger": girl_decision_ratio(anger_value, 5),
            "rebel": girl_decision_ratio(rebel_value, 5),
            "mana_value": girl_decision_int(getattr(girl_info, "mana", 0), 0) if girl_info is not None and girl in GIRL_DECISION_CORE_IDS else 0,
            "mana_bad_probability": girl_info.mana_bad_probability() if girl_info is not None and girl in GIRL_DECISION_CORE_IDS else 0.0,
            "player_history": float(player_history),
            "likes_player": 1.0 if friend >= 10 else 0.0,
            "soap_bonus": girl_decision_soap_bonus(girl),
            "barber_bonus": girl_decision_recent_barber_bonus(girl),
            "church_obey": girl_decision_church_obey_bonus(girl),
            "breakfast_perk": girl_decision_breakfast_perk(girl),
            "need_pressure": girl_decision_need_pressure(girl),
            "jealousy": girl_decision_jealousy(girl),
            "cycle_phase": str(cycle.get("phase", "none") or "none"),
            "cycle_horny": float(cycle.get("horny", 0.0) or 0.0),
            "cycle_critical": float(cycle.get("critical", 0.0) or 0.0),
            "cycle_fertility": float(cycle.get("fertility", 0.0) or 0.0),
            "watching_pref": girl_decision_pref(girl, "watching"),
            "being_watched_pref": girl_decision_pref(girl, "being_watched"),
            "teasing_pref": girl_decision_pref(girl, "teasing"),
            "nipple_pref": girl_decision_pref(girl, "nipple"),
            "oral_pref": girl_decision_pref(girl, "oral"),
            "anal_pref": girl_decision_pref(girl, "anal"),
            "spanking_pref": girl_decision_pref(girl, "spanking"),
            "cowgirl_pref": girl_decision_pref(girl, "cowgirl"),
        }

        if girl == "amanda":
            profile.update({
                "amanda_suckyou": girl_decision_int(Amanda.var_int("suckyou", 0), 0),
                "amanda_fuckyou": girl_decision_int(Amanda.var_int("fuckyou", 0), 0),
                "amanda_knowsexactive": girl_decision_int(Amanda.var_int("knowsexactive", 0), 0),
                "amanda_alberfriends": girl_decision_int(Amanda.legare_affection, 0),
                "amanda_lizafriends": girl_decision_int(Amanda.var_int("lizafriends", 0), 0),
                "amanda_alberprohibit": girl_decision_int(Amanda.legare_forbidden, 0),
                "amanda_prohibitwithguys": girl_decision_int(Amanda.var_int("prohibitwithguys", 0), 0),
            })
        return profile

    def girl_decision_score(profile=None, action_name="", bucket="good"):
        data = dict(profile or {})
        action_key = str(action_name or "").strip().lower()
        bucket_key = str(bucket or "good").strip().lower()
        weights = dict(dict(GIRL_DECISION_ACTION_WEIGHTS.get(action_key, GIRL_DECISION_ACTION_WEIGHTS.get("favor", {})) or {}).get(bucket_key, {}) or {})
        score = 0.0
        for key, weight in weights.items():
            try:
                score += float(data.get(key, 0.0) or 0.0) * float(weight or 0.0)
            except Exception:
                pass
        return score

    def girl_decision_probabilities(girl_name="", action_name="", profile=None):
        data = dict(profile or build_girl_decision_profile(girl_name))
        action_key = str(action_name or "favor").strip().lower()
        good_score = girl_decision_score(data, action_key, "good") - 1.15
        bad_score = girl_decision_score(data, action_key, "bad") - 1.05
        p_good = girl_decision_clamp(girl_decision_sigmoid(good_score))
        p_bad = girl_decision_clamp(girl_decision_sigmoid(bad_score))
        if str(data.get("girl", "") or "").strip().lower() in GIRL_DECISION_CORE_IDS:
            p_bad = girl_decision_clamp(data.get("mana_bad_probability", 0.0))
            p_good = girl_decision_clamp(p_good * (1.0 - p_bad), 0.0, 1.0 - p_bad)
            p_neutral = max(0.0, 1.0 - p_good - p_bad)
            return {
                "good": p_good,
                "neutral": p_neutral,
                "bad": p_bad,
                "capricious_good_is_bad": 0.0,
                "capricious_bad_is_good": 0.0,
                "caprice": 0.0,
                "good_score": good_score,
                "bad_score": bad_score,
                "mana_bad_probability": p_bad,
            }
        if p_good + p_bad > 0.92:
            scale = 0.92 / (p_good + p_bad)
            p_good *= scale
            p_bad *= scale
        caprice = girl_decision_clamp(0.10 + data.get("rebel", 0.0) * 0.22 + data.get("cycle_horny", 0.0) * 0.18 + data.get("jealousy", 0.0) * 0.15 - data.get("church_obey", 0.0) * 0.12, 0.02, 0.38)
        p_good_bad = girl_decision_clamp(caprice * (1.0 - p_good), 0.0, 0.18)
        p_bad_good = girl_decision_clamp(caprice * (1.0 - p_bad), 0.0, 0.18)
        p_neutral = max(0.0, 1.0 - p_good - p_bad - p_good_bad - p_bad_good)
        return {
            "good": p_good,
            "neutral": p_neutral,
            "bad": p_bad,
            "capricious_good_is_bad": p_good_bad,
            "capricious_bad_is_good": p_bad_good,
            "caprice": caprice,
            "good_score": good_score,
            "bad_score": bad_score,
        }

    def girl_decision_roll_value(girl_name="", action_name=""):
        seed = (
            current_game_day() * 37
            + girl_decision_int(calendar_v2.hour, 0) * 11
            + girl_decision_int(calendar_v2.minute, 0) * 3
            + girl_decision_int(calendar_v2.time_slot(), 0) * 19
            + sum([ord(ch) for ch in str(girl_name or "") + ":" + str(action_name or "")])
        ) % 1000
        return float(seed) / 1000.0

    def girl_decide(girl_name="", action_name="", profile=None, roll=None):
        girl = str(girl_name or "").strip().lower()
        action_key = str(action_name or "favor").strip().lower()
        data = dict(profile or build_girl_decision_profile(girl))
        probs = girl_decision_probabilities(girl, action_key, data)
        roll_value = girl_decision_roll_value(girl, action_key) if roll is None else girl_decision_clamp(roll)
        cursor = 0.0
        reaction = "neutral"
        for key in ("good", "capricious_good_is_bad", "bad", "capricious_bad_is_good", "neutral"):
            cursor += float(probs.get(key, 0.0) or 0.0)
            if roll_value <= cursor:
                reaction = key
                break
        result = {
            "girl": girl,
            "action": action_key,
            "reaction": reaction,
            "roll": roll_value,
            "profile": data,
            "probabilities": probs,
        }
        info = people.get_info(girl)
        if info is not None:
            info.var.setdefault("decision_results", {})[action_key] = dict(result)
        return result

    def girl_decision_good_probability(girl_name="", action_name="", profile=None):
        probs = girl_decision_probabilities(girl_name, action_name, profile)
        return girl_decision_clamp(float(probs.get("good", 0.0) or 0.0) + float(probs.get("capricious_bad_is_good", 0.0) or 0.0))

    def girl_decision_reaction_score(reaction=""):
        key = str(reaction or "").strip().lower()
        if key in ("good", "capricious_bad_is_good"):
            return 1
        if key in ("bad", "capricious_good_is_bad"):
            return -1
        return 0

    def girl_decision_status_label(girl_name=""):
        profile = build_girl_decision_profile(girl_name)
        if profile.get("anger", 0.0) > 0.0:
            return "angry"
        if profile.get("rebel", 0.0) >= 0.6:
            return "rebellious"
        if profile.get("player_history", 0.0) > 0.0:
            return "intimate"
        if profile.get("trust", 0.0) >= 0.5 and profile.get("openness", 0.0) >= 0.25:
            return "trusting"
        return "distant"
