"""renpy
init -1 python:
    pass
"""

# Pure Python Amanda intent model with mini-event scoring.
#
# This module does not read Ren'Py store state directly. The Ren'Py bridge should
# build a context dict from current save variables, call these functions, then
# apply the returned intent in normal labels/screens.

from copy import deepcopy


AMANDA_PRIVATE_LOCATIONS = {
    "TavernAmandaRoom",
    "TavernMyRoom",
    "TavernStorage",
    "Shed",
    "BackyardQuiet",
}

AMANDA_SEMI_PRIVATE_LOCATIONS = {
    "TavernKitchen",
    "TavernStable",
    "TavernUpstairs",
    "WineStoreBasement",
}

AMANDA_BASE_PREFERENCES = {
    "watching": 2,
    "being_watched": 1,
    "teasing": 2,
    "nipple": 2,
    "oral": 1,
    "anal": 0,
    "spanking": 0,
    "cowgirl": 0,
}

AMANDA_INTENTS = {
    "ask_player_money": {
        "target": "player",
        "public_ok": True,
        "weights": {
            "money": 1.9,
            "resource_pressure": 0.8,
            "amanda_drive": 0.5,
            "approval": 0.8,
            "attention": 0.5,
            "trust": 0.7,
            "anger": -0.8,
            "work_bad": -0.5,
        },
    },
    "ask_player_beauty_help": {
        "target": "player",
        "public_ok": True,
        "weights": {
            "beauty": 2.1,
            "cloth_access": 0.5,
            "amanda_drive": 0.4,
            "approval": 0.8,
            "attention": 0.8,
            "trust": 0.7,
            "work_good": 0.7,
            "work_bad": -0.8,
            "anger": -0.6,
        },
    },
    "ask_player_reward_for_work": {
        "target": "player",
        "public_ok": True,
        "weights": {
            "approval": 1.4,
            "money": 0.9,
            "beauty": 0.8,
            "work_good": 1.4,
            "attention": 0.5,
            "trust": 0.5,
        },
    },
    "ask_melissa_loan_or_favor": {
        "target": "melissa",
        "public_ok": False,
        "weights": {
            "money": 1.3,
            "beauty": 0.8,
            "attention": 0.4,
            "melissa_trust": 0.9,
            "player_blocked": 1.0,
            "jealousy": -0.4,
        },
    },
    "ask_legare_help": {
        "target": "legare",
        "public_ok": True,
        "weights": {
            "money": 1.5,
            "beauty": 1.2,
            "attention": 0.9,
            "freedom": 1.0,
            "rebel": 1.2,
            "legare_connection": 1.4,
            "player_blocked": 1.2,
            "safety": -1.1,
            "trust": -0.5,
        },
    },
    "private_tease_player": {
        "target": "player",
        "public_ok": False,
        "weights": {
            "attention": 1.2,
            "amanda_drive": 0.8,
            "household_friction": 0.4,
            "desire": 1.0,
            "teasing_pref": 0.9,
            "private": 1.2,
            "trust": 0.8,
            "sexual_openness": 0.9,
            "anger": -0.8,
        },
    },
    "visit_player_room": {
        "target": "player",
        "public_ok": False,
        "weights": {
            "attention": 1.0,
            "desire": 1.2,
            "trust": 1.0,
            "sexual_openness": 1.0,
            "owner_goodnight_oral": 1.2,
            "night": 0.8,
            "anger": -1.0,
            "safety": -0.4,
        },
    },
    "expect_spanking": {
        "target": "player",
        "public_ok": False,
        "weights": {
            "private": 1.0,
            "expects_spanking": 1.8,
            "anger": 1.0,
            "rebel": 0.5,
            "trust": 0.2,
            "night": 0.2,
        },
    },
    "seek_private_satisfaction": {
        "target": "self",
        "public_ok": False,
        "weights": {
            "desire": 1.8,
            "private": 1.1,
            "watching_pref": 0.5,
            "safety": 0.6,
            "attention": -0.4,
            "anger": 0.2,
        },
    },
    "obey_and_work": {
        "target": "household",
        "public_ok": True,
        "weights": {
            "approval": 1.2,
            "household_convergence": 0.8,
            "assigned_work": 0.5,
            "safety": 1.0,
            "future_security": 0.9,
            "work_bad": 1.2,
            "trust": 0.7,
            "rebel": -1.2,
            "work_avoidance": -1.0,
        },
    },
    "avoid_work": {
        "target": "self",
        "public_ok": True,
        "weights": {
            "work_avoidance": 1.7,
            "household_friction": 0.6,
            "resource_pressure": 0.3,
            "rest": 1.0,
            "rebel": 0.9,
            "anger": 0.6,
            "approval": -0.9,
            "safety": -0.4,
        },
    },
}


def clamp(value, low=0.0, high=1.0):
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = float(low)
    return max(float(low), min(float(high), number))


def ratio(value, scale):
    try:
        number = float(value or 0.0)
    except (TypeError, ValueError):
        number = 0.0
    try:
        scale_number = float(scale or 1.0)
    except (TypeError, ValueError):
        scale_number = 1.0
    return clamp(number / max(1.0, scale_number))


def int_value(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return int(default or 0)


def amanda_cycle_state(day_count=0, offset=0):
    day_index = (int_value(day_count) + int_value(offset)) % 28
    if day_index in (0, 1, 2):
        return {
            "day": day_index,
            "phase": "critical",
            "desire": 0.05,
            "rest": 0.65,
            "safety": 0.75,
            "fertility": 0.25,
        }
    if 10 <= day_index <= 15:
        return {
            "day": day_index,
            "phase": "fertile",
            "desire": 0.35,
            "rest": 0.15,
            "safety": 0.35,
            "fertility": 1.0,
        }
    if 21 <= day_index <= 27:
        return {
            "day": day_index,
            "phase": "restless",
            "desire": 0.20,
            "rest": 0.25,
            "safety": 0.45,
            "fertility": 0.35,
        }
    return {
        "day": day_index,
        "phase": "steady",
        "desire": 0.10,
        "rest": 0.20,
        "safety": 0.45,
        "fertility": 0.45,
    }


def context_get(context, key, default=0):
    if not isinstance(context, dict):
        return default
    return context.get(key, default)


def nested_get(context, map_name, key, default=0):
    mapping = context_get(context, map_name, {})
    if isinstance(mapping, dict):
        return mapping.get(key, default)
    return default


def location_privacy(location):
    loc = str(location or "")
    if loc in AMANDA_PRIVATE_LOCATIONS:
        return "private"
    if loc in AMANDA_SEMI_PRIVATE_LOCATIONS:
        return "semi_private"
    return "public"


def amanda_work_report(context):
    report = deepcopy(context_get(context, "daily_work_report", {}) or {})
    cleaning_result = str(report.get("cleaning", "none") or "none")
    waitress_result = str(report.get("waitress", "none") or "none")
    cooking_result = str(report.get("cooking", "none") or "none")
    complaints = int_value(report.get("complaints", 0), 0)
    rude_clients = int_value(report.get("rude_clients", 0), 0)
    tips = int_value(report.get("tips", 0), 0)

    good_count = sum(1 for value in (cleaning_result, waitress_result, cooking_result) if value == "good")
    bad_count = sum(1 for value in (cleaning_result, waitress_result, cooking_result) if value in ("bad", "skipped"))
    work_good = clamp((good_count * 0.35) + ratio(tips, 20), 0.0, 1.0)
    work_bad = clamp((bad_count * 0.35) + ratio(complaints, 3) + ratio(rude_clients, 4) * 0.4, 0.0, 1.0)

    return {
        "cleaning": cleaning_result,
        "waitress": waitress_result,
        "cooking": cooking_result,
        "complaints": complaints,
        "rude_clients": rude_clients,
        "tips": tips,
        "work_good": work_good,
        "work_bad": work_bad,
    }


def amanda_appearance_state(context):
    state = deepcopy(context_get(context, "appearance", {}) or {})
    return {
        "hygiene": clamp(state.get("hygiene", 0.0)),
        "skin": clamp(state.get("skin", 0.0)),
        "scent": clamp(state.get("scent", 0.0)),
        "hair": clamp(state.get("hair", 0.0)),
        "body_grooming": clamp(state.get("body_grooming", 0.0)),
        "dress": clamp(state.get("dress", 0.0)),
        "manners": clamp(state.get("manners", 0.0)),
        "clara_training": clamp(state.get("clara_training", 0.0)),
    }


def amanda_preference_profile(context):
    known = deepcopy(context_get(context, "preference_known", {}) or {})
    learned = deepcopy(context_get(context, "preference_weights", {}) or {})
    profile = {}
    for pref, base in AMANDA_BASE_PREFERENCES.items():
        profile[pref + "_known"] = 1.0 if int_value(known.get(pref, 0), 0) > 0 else 0.0
        profile[pref + "_pref"] = ratio(learned.get(pref, base), 2)
    return profile


def amanda_build_profile(context):
    flags = deepcopy(context_get(context, "amanda_var", {}) or {})
    cycle = amanda_cycle_state(context_get(context, "day", 0), context_get(context, "cycle_offset", 0))
    work = amanda_work_report(context)
    appearance = amanda_appearance_state(context)
    location = str(context_get(context, "location", "") or "")
    privacy = location_privacy(location)
    witnesses = list(context_get(context, "witnesses", []) or [])
    hour = int_value(context_get(context, "hour", 0), 0)

    friend = int_value(context_get(context, "friend", 0), 0)
    openness = int_value(context_get(context, "openness", 0), 0)
    sexual_openness = int_value(context_get(context, "sexual_openness", 0), 0)
    arousal = int_value(context_get(context, "arousal", 0), 0)
    wetness = int_value(context_get(context, "wetness", arousal), arousal)
    anger = int_value(context_get(context, "anger", 0), 0)
    rebel = int_value(context_get(context, "rebel", 0), 0)
    pregnancy = int_value(context_get(context, "pregnancy", 0), 0)

    profile = {
        "friend_value": friend,
        "openness_value": openness,
        "sexual_openness_value": sexual_openness,
        "arousal_value": arousal,
        "wetness_value": wetness,
        "anger_value": anger,
        "rebel_value": rebel,
        "pregnancy_value": pregnancy,
        "trust": ratio(friend, 20),
        "openness": ratio(openness, 20),
        "sexual_openness": ratio(sexual_openness, 100),
        "arousal": ratio(arousal, 100),
        "wetness": ratio(wetness, 100),
        "anger": ratio(anger, 5),
        "rebel": ratio(rebel, 5),
        "cycle_day": cycle["day"],
        "cycle_phase": cycle["phase"],
        "cycle_desire": cycle["desire"],
        "cycle_rest": cycle["rest"],
        "cycle_safety": cycle["safety"],
        "cycle_fertility": cycle["fertility"],
        "location": location,
        "privacy": privacy,
        "private": 1.0 if privacy == "private" else 0.0,
        "semi_private": 1.0 if privacy == "semi_private" else 0.0,
        "public": 1.0 if privacy == "public" else 0.0,
        "night": 1.0 if hour >= 21 or hour < 6 else 0.0,
        "witness_count": len(witnesses),
        "sandra_witness": 1.0 if "sandra" in witnesses else 0.0,
        "melissa_witness": 1.0 if "melissa" in witnesses else 0.0,
        "legare_connection": 1.0 if int_value(flags.get("alberfriends", 0), 0) > 0 or int_value(flags.get("albernowdances", 0), 0) > 0 else 0.0,
        "legare_prohibited": 1.0 if int_value(flags.get("alberprohibit", 0), 0) > 0 else 0.0,
        "lizette_connection": ratio(flags.get("lizafriends", 0), 20),
        "player_blocked": 1.0 if int_value(context_get(context, "player_blocked_recent_need", 0), 0) > 0 else 0.0,
        "melissa_trust": ratio(context_get(context, "melissa_friend", 0), 20),
        "beauty_help_satisfied": 1.0 if int_value(context_get(context, "beauty_help_satisfied", 0), 0) > 0 else 0.0,
        "resource_pressure": clamp(context_get(context, "household_pressure", context_get(context, "money_pressure", 0.0))),
        "household_friction": clamp(context_get(context, "household_friction", 0.0)),
        "household_convergence": clamp(context_get(context, "household_convergence", 0.0)),
        "external_threat": clamp(context_get(context, "external_threat", 0.0)),
        "amanda_drive": clamp(context_get(context, "amanda_drive", 0.0)),
        "sandra_pressure": clamp(context_get(context, "sandra_drive", 0.0)),
        "melissa_pressure": clamp(context_get(context, "melissa_drive", 0.0)),
        "assigned_work": 1.0 if str(context_get(context, "assigned_work", "") or "") not in ("", "none") else 0.0,
        "cloth_access": clamp(context_get(context, "cloth_access", 0.0)),
        "food_security": clamp(context_get(context, "food_security", 0.5)),
    }
    profile["owner_goodnight_oral"] = 1.0 if int_value(flags.get("suckyou", 0), 0) > 0 or int_value(flags.get("goodnight_blowjob", 0), 0) > 0 else 0.0
    profile["expects_spanking"] = 1.0 if anger >= 3 and privacy == "private" else 0.0
    profile.update(work)
    profile.update(appearance)
    profile.update(amanda_preference_profile(context))
    return profile


def amanda_calculate_needs(context, profile=None):
    data = dict(profile or amanda_build_profile(context))
    money_pressure = clamp(context_get(context, "money_pressure", 0.0))
    household_order = clamp(context_get(context, "household_order", 0.5))
    attention_gap = clamp(context_get(context, "attention_gap", 0.0))
    jealousy = clamp(context_get(context, "jealousy", 0.0))
    work_bad = data.get("work_bad", 0.0)
    work_good = data.get("work_good", 0.0)
    beauty_gap = 1.0 - clamp(
        (data.get("hygiene", 0.0) * 0.20)
        + (data.get("skin", 0.0) * 0.15)
        + (data.get("scent", 0.0) * 0.15)
        + (data.get("hair", 0.0) * 0.15)
        + (data.get("body_grooming", 0.0) * 0.15)
        + (data.get("dress", 0.0) * 0.20)
    )

    needs = {
        "money": clamp(money_pressure + work_good * 0.25 + work_bad * 0.15),
        "beauty": clamp(beauty_gap + data.get("clara_training", 0.0) * 0.15),
        "attention": clamp(attention_gap + jealousy * 0.35 + data.get("teasing_pref", 0.0) * 0.15),
        "desire": clamp(data.get("arousal", 0.0) * 0.45 + data.get("wetness", 0.0) * 0.35 + data.get("cycle_desire", 0.0)),
        "rest": clamp(data.get("cycle_rest", 0.0) + work_bad * 0.25),
        "safety": clamp(data.get("cycle_safety", 0.0) + (1.0 - household_order) * 0.3 + ratio(data.get("pregnancy_value", 0), 180) * 0.4),
        "approval": clamp((1.0 - data.get("anger", 0.0)) * 0.35 + work_good * 0.45 + data.get("trust", 0.0) * 0.25),
        "freedom": clamp(data.get("rebel", 0.0) * 0.8 + data.get("player_blocked", 0.0) * 0.35),
        "work_avoidance": clamp(data.get("rebel", 0.0) * 0.35 + data.get("rest", 0.0) * 0.35 + work_bad * 0.25),
        "future_security": clamp((1.0 - household_order) * 0.45 + ratio(data.get("pregnancy_value", 0), 180) * 0.45 + money_pressure * 0.25),
        "jealousy": jealousy,
    }
    return needs


def amanda_memory_row(memory, intent):
    if not isinstance(memory, dict):
        memory = {}
    row = deepcopy(memory.get(intent, {}) or {})
    row.setdefault("attempts", 0)
    row.setdefault("successes", 0)
    row.setdefault("failures", 0)
    row.setdefault("public_refusals", 0)
    row.setdefault("private_refusals", 0)
    row.setdefault("last_day", -1)
    row.setdefault("bias", 0.0)
    return row


def amanda_intent_gate(intent, context, profile, needs):
    privacy = profile.get("privacy", "public")
    config = AMANDA_INTENTS.get(intent, {})
    mode = str(context_get(context, "mode", "room") or "room")
    if privacy == "public" and not config.get("public_ok", False):
        return False, "needs_private_or_overheard"
    if intent == "ask_legare_help":
        if profile.get("legare_connection", 0.0) <= 0.0:
            return False, "no_legare_connection"
        if profile.get("legare_prohibited", 0.0) > 0.0 and profile.get("rebel", 0.0) < 0.5:
            return False, "legare_blocked_and_not_rebellious"
    if intent == "ask_player_beauty_help" and profile.get("beauty_help_satisfied", 0.0) > 0.0:
        return False, "beauty_help_already_done"
    if intent == "ask_melissa_loan_or_favor" and profile.get("melissa_trust", 0.0) < 0.25:
        return False, "not_enough_melissa_trust"
    if intent == "visit_player_room" and mode == "breakfast":
        return False, "not_breakfast_flow"
    if intent == "visit_player_room" and str(context_get(context, "location", "")) != "TavernMyRoom":
        return False, "not_player_room"
    if intent in ("private_tease_player", "visit_player_room") and profile.get("trust", 0.0) < 0.25:
        return False, "not_enough_trust"
    if intent == "seek_private_satisfaction" and needs.get("desire", 0.0) < 0.35:
        return False, "desire_too_low"
    if intent == "expect_spanking" and profile.get("expects_spanking", 0.0) <= 0.0:
        return False, "owner_not_angry"
    return True, ""


def amanda_score_intents(context, memory=None):
    profile = amanda_build_profile(context)
    needs = amanda_calculate_needs(context, profile)
    rows = []
    memory = memory if isinstance(memory, dict) else {}

    model_values = {}
    model_values.update(profile)
    model_values.update(needs)

    for intent, config in AMANDA_INTENTS.items():
        allowed, reason = amanda_intent_gate(intent, context, profile, needs)
        row = amanda_memory_row(memory, intent)
        raw_score = -99.0
        if allowed:
            raw_score = float(row.get("bias", 0.0) or 0.0)
            for key, weight in (config.get("weights", {}) or {}).items():
                raw_score += float(model_values.get(key, 0.0) or 0.0) * float(weight or 0.0)
            raw_score -= 0.55
        rows.append({
            "intent": intent,
            "target": config.get("target", ""),
            "allowed": allowed,
            "blocked_reason": reason,
            "score": round(raw_score, 4),
        })

    rows.sort(key=lambda item: (item["allowed"], item["score"], item["intent"]), reverse=True)
    return {
        "profile": profile,
        "needs": needs,
        "intents": rows,
    }


def amanda_choose_intent(context, memory=None, threshold=0.35):
    state = amanda_score_intents(context, memory)
    chosen = None
    for row in state["intents"]:
        if row["allowed"] and row["score"] >= float(threshold):
            chosen = row
            break
    state["chosen"] = deepcopy(chosen)
    return state


def amanda_apply_feedback(memory, intent, outcome, day=0, public=False):
    updated = deepcopy(memory if isinstance(memory, dict) else {})
    key = str(intent or "")
    row = amanda_memory_row(updated, key)
    result = str(outcome or "neutral")

    row["attempts"] = int_value(row.get("attempts", 0), 0) + 1
    row["last_day"] = int_value(day, 0)

    if result in ("approved", "rewarded", "success"):
        row["successes"] = int_value(row.get("successes", 0), 0) + 1
        row["bias"] = clamp(float(row.get("bias", 0.0) or 0.0) + 0.12, -0.75, 0.75)
    elif result in ("refused_with_reason", "failed_soft"):
        row["failures"] = int_value(row.get("failures", 0), 0) + 1
        row["private_refusals"] = int_value(row.get("private_refusals", 0), 0) + (0 if public else 1)
        row["public_refusals"] = int_value(row.get("public_refusals", 0), 0) + (1 if public else 0)
        row["bias"] = clamp(float(row.get("bias", 0.0) or 0.0) - (0.06 if not public else 0.10), -0.75, 0.75)
    elif result in ("refused_badly", "humiliated", "punished"):
        row["failures"] = int_value(row.get("failures", 0), 0) + 1
        row["private_refusals"] = int_value(row.get("private_refusals", 0), 0) + (0 if public else 1)
        row["public_refusals"] = int_value(row.get("public_refusals", 0), 0) + (1 if public else 0)
        row["bias"] = clamp(float(row.get("bias", 0.0) or 0.0) - (0.14 if not public else 0.22), -0.75, 0.75)
    else:
        row["bias"] = clamp(float(row.get("bias", 0.0) or 0.0) - 0.02, -0.75, 0.75)

    updated[key] = row
    return updated


def amanda_visible_status(profile, needs):
    phase = str(profile.get("cycle_phase", "steady"))
    parts = []
    if needs.get("rest", 0.0) >= 0.65:
        parts.append("tired")
    if needs.get("beauty", 0.0) >= 0.65:
        parts.append("wants_attention_to_appearance")
    if needs.get("money", 0.0) >= 0.65:
        parts.append("money_pressure")
    if profile.get("work_bad", 0.0) >= 0.55:
        parts.append("work_trouble")
    elif profile.get("work_good", 0.0) >= 0.45:
        parts.append("worked_well")
    if needs.get("desire", 0.0) >= 0.55:
        parts.append("restless")
    if profile.get("anger", 0.0) >= 0.5:
        parts.append("angry")
    if not parts:
        parts.append("ordinary")
    return {
        "cycle": phase,
        "labels": parts,
    }


# =============================================================================
# Amanda mini-event selector.
# Pure Python only: reads context dict, never Ren'Py store directly.
# Bridge calls this to convert household pressure and Amanda context into a
# playable mini-event label. This is intentionally separate from AMANDA_INTENTS
# so long-form intent requests and small ambient events remain independently
# scoreable.
# =============================================================================

AMANDA_MINI_EVENTS = {
    "amanda_morning_hover": {
        "locations": {"TavernKitchen", "TavernMain", "TavernMyRoom"},
        "modes": {"room", "breakfast"},
        "weights": {"attention": 0.9, "amanda_drive": 0.5, "household_friction": 0.2},
    },
    "amanda_sits_on_leg": {
        "locations": {"TavernMain", "TavernKitchen"},
        "modes": {"room", "breakfast"},
        "weights": {"attention": 0.8, "teasing_pref": 0.8, "trust": 0.5, "amanda_drive": 0.6},
    },
    "amanda_bed_edge_talk": {
        "locations": {"TavernMyRoom"},
        "modes": {"room"},
        "weights": {"night": 0.8, "attention": 0.7, "trust": 0.5, "amanda_drive": 0.8},
    },
    "amanda_storm_fear": {
        "locations": {"TavernMyRoom", "TavernAmandaRoom"},
        "modes": {"room"},
        "weights": {"safety": 0.8, "night": 0.4, "trust": 0.4},
    },
    "amanda_kitchen_jealousy": {
        "locations": {"TavernKitchen", "TavernMain"},
        "modes": {"room", "breakfast"},
        "weights": {"jealousy": 1.0, "household_friction": 0.7, "melissa_pressure": 0.3},
    },
    "amanda_new_dress_pressure": {
        "locations": {"TavernKitchen", "TavernMain", "TavernAmandaRoom"},
        "modes": {"room", "breakfast"},
        "weights": {"beauty": 1.0, "cloth_access": 0.5, "money": 0.4, "attention": 0.3},
    },
    "amanda_eavesdrop_caught": {
        "locations": {"TavernMyRoom", "TavernStorage", "TavernKitchen"},
        "modes": {"room"},
        "weights": {"attention": 0.4, "rebel": 0.4, "household_friction": 0.5, "private": 0.3},
    },
    "amanda_hunting_interest": {
        "locations": {"TavernMain", "TavernKitchen", "TavernMyRoom"},
        "modes": {"room"},
        "weights": {"money": 0.4, "beauty": 0.4, "future_security": 0.6, "resource_pressure": 0.2},
    },
    "amanda_breakfast_mockery": {
        "locations": {"TavernKitchen"},
        "modes": {"breakfast", "room"},
        "weights": {"household_friction": 1.0, "rebel": 0.5, "amanda_drive": 0.4},
    },
    "amanda_late_night_window": {
        "locations": {"TavernMyRoom", "TavernAmandaRoom", "TavernUpstairs"},
        "modes": {"room"},
        "weights": {"night": 0.8, "rest": 0.4, "attention": 0.4, "future_security": 0.4},
    },
    "amanda_asks_work_direction": {
        "locations": {"TavernKitchen", "TavernMain", "TavernStorage"},
        "modes": {"room", "breakfast"},
        "weights": {"assigned_work": 0.5, "approval": 0.6, "work_bad": 0.5, "household_convergence": 0.4},
    },
    "amanda_poverty_complaint": {
        "locations": {"TavernKitchen", "TavernMain", "TavernAmandaRoom"},
        "modes": {"room", "breakfast"},
        "weights": {"resource_pressure": 1.0, "money": 0.7, "beauty": 0.4, "household_friction": 0.5},
    },
}


def amanda_event_score(event_code, context, profile=None, needs=None):
    data = dict(profile or amanda_build_profile(context))
    data.update(needs or amanda_calculate_needs(context, data))
    config = AMANDA_MINI_EVENTS.get(str(event_code or ""), {})
    location = str(context_get(context, "location", "") or "")
    mode = str(context_get(context, "mode", "room") or "room")

    locations = config.get("locations", set())
    modes = config.get("modes", set())
    if locations and location not in locations:
        return -99.0, "wrong_location"
    if modes and mode not in modes:
        return -99.0, "wrong_mode"

    # Early private content gate. Private room events need trust and not too much anger.
    if event_code in ("amanda_bed_edge_talk", "amanda_late_night_window", "amanda_storm_fear"):
        if data.get("trust", 0.0) < 0.20:
            return -99.0, "not_enough_trust"
        if data.get("anger", 0.0) > 0.65:
            return -99.0, "too_angry"

    score = 0.0
    for key, weight in (config.get("weights", {}) or {}).items():
        score += float(data.get(key, 0.0) or 0.0) * float(weight or 0.0)

    # Amanda should not fire the same kind of scene constantly; bridge handles exact seen-key,
    # model adds a soft day memory penalty when available.
    event_memory = context_get(context, "mini_event_memory", {})
    if isinstance(event_memory, dict):
        row = event_memory.get(event_code, {}) or {}
        if int_value(row.get("last_day", -99), -99) == int_value(context_get(context, "day", 0), 0):
            score -= 1.0
        score -= clamp(int_value(row.get("recent_count", 0), 0) / 5.0, 0.0, 0.5)

    return round(score - 0.45, 4), ""


def amanda_choose_mini_event(context, memory=None, threshold=0.30):
    profile = amanda_build_profile(context)
    needs = amanda_calculate_needs(context, profile)
    rows = []
    context = deepcopy(context if isinstance(context, dict) else {})
    if isinstance(memory, dict):
        context["mini_event_memory"] = memory

    for event_code in AMANDA_MINI_EVENTS:
        score, reason = amanda_event_score(event_code, context, profile, needs)
        rows.append({
            "event": event_code,
            "allowed": score > -90.0,
            "blocked_reason": reason,
            "score": score,
        })

    rows.sort(key=lambda item: (item["allowed"], item["score"], item["event"]), reverse=True)
    chosen = None
    for row in rows:
        if row["allowed"] and row["score"] >= float(threshold):
            chosen = row
            break

    return {
        "profile": profile,
        "needs": needs,
        "events": rows,
        "chosen": deepcopy(chosen),
    }


"""renpy
init python:
    pass
"""
