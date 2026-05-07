# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default RelationshipMoodState = {}
default RelationshipInteractionScore = {}

init -42 python:
    RELATIONSHIP_HOUSEHOLD_NPCS = ("amanda", "melissa", "sandra")
    RELATIONSHIP_CORE_NPCS = ("amanda", "melissa", "sandra", "clara", "becky", "irma", "inga", "liza", "georgett")
    RELATIONSHIP_CARE_GIFTS = ("soap_001", "luxury_soap_001", "energy_tea_001", "berries_001", "lavender_001", "wild_rose_001")
    RELATIONSHIP_ACTION_REQUIREMENTS = {
        "_default": {
            "talk": {"score": 0, "friend": 0, "open": 0, "slut": 0},
            "private_talk": {"score": 10, "friend": 3, "open": 2, "slut": 0},
            "care_gift": {"score": 0, "friend": 0, "open": 0, "slut": 0},
            "gift": {"score": 8, "friend": 3, "open": 0, "slut": 0},
            "share": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "flirt": {"score": 25, "friend": 5, "open": 1, "slut": 0},
        },
        "amanda": {
            "private_talk": {"score": 12, "friend": 4, "open": 2, "slut": 0},
            "gift": {"score": 8, "friend": 3, "open": 0, "slut": 0},
            "share": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "flirt": {"score": 25, "friend": 5, "open": 1, "slut": 0},
        },
        "melissa": {
            "private_talk": {"score": 10, "friend": 4, "open": 2, "slut": 0},
            "gift": {"score": 8, "friend": 3, "open": 0, "slut": 0},
            "share": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "flirt": {"score": 25, "friend": 5, "open": 1, "slut": 0},
        },
        "sandra": {
            "private_talk": {"score": 15, "friend": 5, "open": 3, "slut": 0},
            "gift": {"score": 10, "friend": 4, "open": 0, "slut": 0},
            "share": {"score": 6, "friend": 3, "open": 0, "slut": 0},
            "flirt": {"score": 30, "friend": 7, "open": 2, "slut": 0},
        },
        "clara": {
            "private_talk": {"score": 10, "friend": 3, "open": 2, "slut": 0},
            "gift": {"score": 12, "friend": 4, "open": 1, "slut": 0},
            "share": {"score": 7, "friend": 3, "open": 0, "slut": 0},
            "flirt": {"score": 20, "friend": 5, "open": 2, "slut": 0},
        },
        "becky": {
            "private_talk": {"score": 8, "friend": 2, "open": 1, "slut": 0},
            "gift": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "share": {"score": 4, "friend": 1, "open": 0, "slut": 0},
            "flirt": {"score": 15, "friend": 4, "open": 1, "slut": 0},
        },
        "irma": {
            "private_talk": {"score": 8, "friend": 2, "open": 1, "slut": 0},
            "gift": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "share": {"score": 4, "friend": 1, "open": 0, "slut": 0},
            "flirt": {"score": 15, "friend": 4, "open": 1, "slut": 0},
        },
        "inga": {
            "private_talk": {"score": 8, "friend": 2, "open": 1, "slut": 0},
            "gift": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "share": {"score": 4, "friend": 1, "open": 0, "slut": 0},
            "flirt": {"score": 15, "friend": 4, "open": 1, "slut": 0},
        },
        "liza": {
            "private_talk": {"score": 8, "friend": 2, "open": 1, "slut": 0},
            "gift": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "share": {"score": 4, "friend": 1, "open": 0, "slut": 0},
            "flirt": {"score": 15, "friend": 4, "open": 1, "slut": 0},
        },
        "georgett": {
            "private_talk": {"score": 8, "friend": 2, "open": 1, "slut": 0},
            "gift": {"score": 5, "friend": 2, "open": 0, "slut": 0},
            "share": {"score": 4, "friend": 1, "open": 0, "slut": 0},
            "flirt": {"score": 15, "friend": 4, "open": 1, "slut": 0},
        },
    }

    def relationship_int(value, default=0):
        try:
            return int(value)
        except Exception:
            return int(default or 0)

    def relationship_key(person=""):
        return str(person or "").strip().lower()

    def relationship_state(person=""):
        global RelationshipMoodState
        key = relationship_key(person)
        if not key:
            return {}
        if not isinstance(RelationshipMoodState, dict):
            RelationshipMoodState = {}
        row = RelationshipMoodState.get(key, None)
        if not isinstance(row, dict):
            row = {}
            RelationshipMoodState[key] = row
        row.setdefault("anger", 0)
        row.setdefault("anger_until_day", -1)
        row.setdefault("anger_reason", "")
        row.setdefault("last_bad_action_day", -1)
        return row

    def relationship_interaction_score(person=""):
        key = relationship_key(person)
        if not key:
            return 0
        friend_value = relationship_int(Friends.get(key, 0), 0) if isinstance(Friends, dict) else 0
        open_value = relationship_int(otkroven.get(key, 0), 0) if isinstance(otkroven, dict) else 0
        talked_value = relationship_int(Talked.get(key, 0), 0) if isinstance(Talked, dict) else 0
        inferred = max(0, friend_value * 3 + open_value + min(10, talked_value * 2))
        if not isinstance(RelationshipInteractionScore, dict):
            return inferred
        return max(inferred, relationship_int(RelationshipInteractionScore.get(key, 0), 0))

    def relationship_add_interaction_score(person="", action="", raw_score=0):
        global RelationshipInteractionScore
        key = relationship_key(person)
        if not key:
            return 0
        if not isinstance(RelationshipInteractionScore, dict):
            RelationshipInteractionScore = {}
        action_key = str(action or "").strip().lower()
        score = max(0, relationship_int(raw_score, 0))
        if score <= 0:
            return relationship_interaction_score(key)
        gain = max(1, score)
        RelationshipInteractionScore[key] = min(999, relationship_interaction_score(key) + gain)
        return relationship_interaction_score(key)

    def relationship_action_requirement_key(action="", item_id=""):
        action_key = str(action or "").strip().lower()
        item_key = str(item_id or "").strip()
        if action_key == "gift" and item_key in RELATIONSHIP_CARE_GIFTS:
            return "care_gift"
        return action_key

    def relationship_action_requirement(person="", action="", item_id=""):
        key = relationship_key(person)
        requirement_key = relationship_action_requirement_key(action, item_id)
        base = dict(RELATIONSHIP_ACTION_REQUIREMENTS.get("_default", {}).get(requirement_key, {}) or {})
        personal = dict(RELATIONSHIP_ACTION_REQUIREMENTS.get(key, {}).get(requirement_key, {}) or {})
        base.update(personal)
        base.setdefault("score", 0)
        base.setdefault("friend", 0)
        base.setdefault("open", 0)
        base.setdefault("slut", 0)
        return base

    def relationship_requirement_block_text(person="", action="", item_id=""):
        key = relationship_key(person)
        action_key = str(action or "").strip().lower()
        name = _action_display_name(key)
        requirement = relationship_action_requirement(key, action_key, item_id)
        score_need = relationship_int(requirement.get("score", 0), 0)
        friend_need = relationship_int(requirement.get("friend", 0), 0)
        open_need = relationship_int(requirement.get("open", 0), 0)
        slut_need = relationship_int(requirement.get("slut", 0), 0)
        score_value = relationship_interaction_score(key)
        friend_value = relationship_int(Friends.get(key, 0), 0) if isinstance(Friends, dict) else 0
        open_value = relationship_int(otkroven.get(key, 0), 0) if isinstance(otkroven, dict) else 0
        slut_value = relationship_int(sluttiness.get(key, 0), 0) if isinstance(sluttiness, dict) else 0
        if score_value < score_need:
            return "Сначала нужны обычные разговоры с %s. Сейчас между вами еще мало накопленного доверия." % name
        if friend_value < friend_need:
            return "%s пока держит дистанцию. Нужны более теплые отношения." % name
        if open_value < open_need:
            return "%s пока не готова говорить и реагировать так откровенно." % name
        if slut_value < slut_need:
            return "%s пока не готова к такому тону." % name
        return relationship_block_text(key, action_key)

    def relationship_requirement_met(person="", action="", item_id=""):
        key = relationship_key(person)
        if not key:
            return False, "Некого выбрать."
        requirement = relationship_action_requirement(key, action, item_id)
        score_value = relationship_interaction_score(key)
        friend_value = relationship_int(Friends.get(key, 0), 0) if isinstance(Friends, dict) else 0
        open_value = relationship_int(otkroven.get(key, 0), 0) if isinstance(otkroven, dict) else 0
        slut_value = relationship_int(sluttiness.get(key, 0), 0) if isinstance(sluttiness, dict) else 0
        if score_value < relationship_int(requirement.get("score", 0), 0):
            return False, relationship_requirement_block_text(key, action, item_id)
        if friend_value < relationship_int(requirement.get("friend", 0), 0):
            return False, relationship_requirement_block_text(key, action, item_id)
        if open_value < relationship_int(requirement.get("open", 0), 0):
            return False, relationship_requirement_block_text(key, action, item_id)
        if slut_value < relationship_int(requirement.get("slut", 0), 0):
            return False, relationship_requirement_block_text(key, action, item_id)
        return True, ""

    def relationship_requirement_value(person="", action="", field="score", item_id=""):
        requirement = relationship_action_requirement(person, action, item_id)
        return relationship_int(requirement.get(str(field or "score"), 0), 0)

    def relationship_anger(person=""):
        row = relationship_state(person)
        if not row:
            return 0
        anger = max(0, relationship_int(row.get("anger", 0), 0))
        until_day = relationship_int(row.get("anger_until_day", -1), -1)
        if anger > 0 and until_day >= 0 and relationship_int(dayspassed, 0) > until_day:
            row["anger"] = 0
            row["anger_reason"] = ""
            return 0
        return anger

    def relationship_set_anger(person="", amount=1, days=1, reason=""):
        row = relationship_state(person)
        if not row:
            return 0
        current = relationship_anger(person)
        row["anger"] = max(0, min(5, current + relationship_int(amount, 1)))
        row["anger_until_day"] = max(relationship_int(row.get("anger_until_day", -1), -1), relationship_int(dayspassed, 0) + max(1, relationship_int(days, 1)))
        row["anger_reason"] = str(reason or row.get("anger_reason", "") or "bad_action")
        row["last_bad_action_day"] = relationship_int(dayspassed, 0)
        return relationship_anger(person)

    def relationship_calm(person="", amount=1):
        row = relationship_state(person)
        if not row:
            return 0
        row["anger"] = max(0, relationship_anger(person) - max(1, relationship_int(amount, 1)))
        if relationship_int(row.get("anger", 0), 0) <= 0:
            row["anger_until_day"] = -1
            row["anger_reason"] = ""
        return relationship_anger(person)

    def relationship_weekly_chore_eval():
        try:
            return str(SandraVar.get("WeeklyChoreCheckEval", "") or "").strip().lower()
        except Exception:
            return ""

    def relationship_rebel_value(person=""):
        key = relationship_key(person)
        try:
            return max(0, relationship_int(neshlush.get(key, 0), 0))
        except Exception:
            return 0

    def relationship_has_talked_today(person=""):
        key = relationship_key(person)
        try:
            if relationship_int(TalkedToday.get(key, 0), 0) > 0:
                return True
        except Exception:
            pass
        try:
            info = getPersonInfo(key)
            if info is not None and len(getattr(info, "talkToday", set()) or set()) > 0:
                return True
        except Exception:
            pass
        return False

    def relationship_social_stage(person=""):
        key = relationship_key(person)
        friend_value = relationship_int(Friends.get(key, 0), 0) if isinstance(Friends, dict) else 0
        open_value = relationship_int(otkroven.get(key, 0), 0) if isinstance(otkroven, dict) else 0
        corruption_value = relationship_int(sluttiness.get(key, 0), 0) if isinstance(sluttiness, dict) else 0
        stage = 0
        if friend_value >= 2:
            stage = 1
        if friend_value >= 5 and open_value >= 1:
            stage = 2
        if friend_value >= 8 and open_value >= 3:
            stage = 3
        if friend_value >= 10 and (open_value >= 5 or corruption_value >= 8):
            stage = 4
        return stage

    def relationship_block_text(person="", action=""):
        key = relationship_key(person)
        name = _action_display_name(key)
        action_key = str(action or "").strip().lower()
        anger = relationship_anger(key)
        if anger > 0:
            return "%s сейчас сердится. Сначала стоит спокойно поговорить и дать ей время остыть." % name
        if action_key == "gift":
            return "Подарок сейчас будет выглядеть слишком внезапно. Сначала лучше поговорить и понять настроение %s." % name
        if action_key == "share":
            return "Сейчас лучше сначала втянуть %s в обычный разговор, а уже потом что-то предлагать." % name
        if action_key == "flirt":
            return "%s пока не готова к такому тону. Нужны обычные разговоры, доверие и подходящий момент." % name
        return "Сейчас это будет неуместно."

    def relationship_social_action_allowed(person="", action="", item_id=""):
        key = relationship_key(person)
        action_key = str(action or "").strip().lower()
        item_key = str(item_id or "").strip()
        if not key:
            return False, "Некого выбрать."
        if action_key in ("talk", "look"):
            return True, ""

        anger = relationship_anger(key)
        if anger > 0:
            return False, relationship_block_text(key, action_key)

        friend_value = relationship_int(Friends.get(key, 0), 0) if isinstance(Friends, dict) else 0
        weekly_eval = relationship_weekly_chore_eval()

        if key in RELATIONSHIP_HOUSEHOLD_NPCS and weekly_eval == "bad" and friend_value < 10:
            if action_key in ("gift", "share", "flirt"):
                return False, "После плохой недели по хозяйству домочадцы не готовы к таким жестам. Сначала нужно вернуть уважение делом."

        if action_key == "gift":
            return relationship_requirement_met(key, action_key, item_key)

        if action_key == "share":
            return relationship_requirement_met(key, action_key, item_key)

        if action_key == "flirt":
            return relationship_requirement_met(key, action_key, item_key)

        if action_key == "private_talk":
            return relationship_requirement_met(key, action_key, item_key)

        return True, ""

    def relationship_any_gift_allowed(person=""):
        key = relationship_key(person)
        if not key:
            return False
        allowed, reason = relationship_social_action_allowed(key, "gift")
        if allowed:
            return True
        try:
            for item_id in list(player_card_giftable_item_ids() or []):
                item_allowed, item_reason = relationship_social_action_allowed(key, "gift", item_id)
                if item_allowed:
                    return True
        except Exception:
            pass
        return False

    def relationship_adjust_social_score(person="", action="", score=0):
        key = relationship_key(person)
        action_key = str(action or "").strip().lower()
        value = relationship_int(score, 0)
        anger = relationship_anger(key)
        rebel = relationship_rebel_value(key)
        weekly_eval = relationship_weekly_chore_eval()
        if anger > 0:
            value -= anger
        if key in RELATIONSHIP_HOUSEHOLD_NPCS and rebel > 0:
            value -= min(2, rebel)
        if key in RELATIONSHIP_HOUSEHOLD_NPCS and weekly_eval == "bad" and action_key in ("gift", "share", "flirt"):
            value -= 2
        elif key in RELATIONSHIP_HOUSEHOLD_NPCS and weekly_eval == "neutral" and action_key in ("gift", "flirt"):
            value -= 1
        return max(-5, min(5, value))

    def relationship_after_social_result(person="", action="", raw_score=0, accepted=True):
        key = relationship_key(person)
        action_key = str(action or "").strip().lower()
        score = relationship_int(raw_score, 0)
        if not key:
            return
        if not bool(accepted) or score < 0:
            relationship_set_anger(key, 1 if score >= -2 else 2, 1 if action_key == "talk" else 2, action_key)
            if key in RELATIONSHIP_HOUSEHOLD_NPCS and isinstance(neshlush, dict):
                neshlush[key] = max(0, relationship_int(neshlush.get(key, 0), 0) + 1)
        elif score > 0:
            relationship_calm(key, 1)
            relationship_add_interaction_score(key, action_key, score)
            if key in RELATIONSHIP_HOUSEHOLD_NPCS and isinstance(neshlush, dict):
                neshlush[key] = max(0, relationship_int(neshlush.get(key, 0), 0) - 1)
        try:
            people_sync_person(key)
        except Exception:
            pass

    def relationship_apply_weekly_chore_evaluation(preview=None):
        result = ""
        score = 0
        if isinstance(preview, dict):
            flags = dict(preview.get("sandra_flags", {}) or {})
            result = str(flags.get("WeeklyChoreCheckEval", "") or "").strip().lower()
            score = relationship_int(flags.get("WeeklyChoreCheckScore", 0), 0)
        if not result:
            result = relationship_weekly_chore_eval()
            try:
                score = relationship_int(SandraVar.get("WeeklyChoreCheckScore", 0), 0)
            except Exception:
                score = 0
        if result == "good":
            for person in RELATIONSHIP_HOUSEHOLD_NPCS:
                relationship_calm(person, 2)
        elif result == "neutral":
            relationship_calm("sandra", 1)
        elif result == "bad":
            relationship_set_anger("sandra", 2, 3, "weekly_chores")
            for person in ("amanda", "melissa"):
                relationship_set_anger(person, 1, 2, "weekly_chores")
                if isinstance(neshlush, dict):
                    neshlush[person] = max(0, relationship_int(neshlush.get(person, 0), 0) + 1)
        return score

    def relationship_card_status_line(person=""):
        key = relationship_key(person)
        if not key:
            return ""
        anger = relationship_anger(key)
        rebel = relationship_rebel_value(key)
        weekly_eval = relationship_weekly_chore_eval()
        parts = []
        if anger > 0:
            parts.append("сердится")
        elif relationship_social_stage(key) >= 3:
            parts.append("доверяет")
        elif relationship_social_stage(key) >= 1:
            parts.append("привыкает")
        else:
            parts.append("держит дистанцию")
        if rebel > 0:
            parts.append("строптивость %s" % rebel)
        if key in RELATIONSHIP_HOUSEHOLD_NPCS and weekly_eval:
            parts.append("неделя: %s" % weekly_eval)
        return ", ".join(parts)
