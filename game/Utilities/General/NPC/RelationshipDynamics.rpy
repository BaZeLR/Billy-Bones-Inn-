# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default RelationshipMoodState = {}

init -42 python:
    RELATIONSHIP_HOUSEHOLD_NPCS = ("amanda", "melissa", "sandra")
    RELATIONSHIP_CORE_NPCS = ("amanda", "melissa", "sandra", "clara")
    RELATIONSHIP_CARE_GIFTS = ("soap_001", "luxury_soap_001", "energy_tea_001", "berries_001", "lavender_001", "wild_rose_001")

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
        open_value = relationship_int(otkroven.get(key, 0), 0) if isinstance(otkroven, dict) else 0
        talked_today = relationship_has_talked_today(key)
        stage = relationship_social_stage(key)
        weekly_eval = relationship_weekly_chore_eval()

        if key in RELATIONSHIP_HOUSEHOLD_NPCS and weekly_eval == "bad" and friend_value < 10:
            if action_key in ("gift", "share", "flirt"):
                return False, "После плохой недели по хозяйству домочадцы не готовы к таким жестам. Сначала нужно вернуть уважение делом."

        if action_key == "gift":
            if item_key in RELATIONSHIP_CARE_GIFTS and (talked_today or friend_value >= 3 or stage >= 1):
                return True, ""
            if not talked_today and friend_value < 5:
                return False, relationship_block_text(key, action_key)
            if stage < 1:
                return False, relationship_block_text(key, action_key)
            return True, ""

        if action_key == "share":
            if talked_today or friend_value >= 3 or stage >= 1:
                return True, ""
            return False, relationship_block_text(key, action_key)

        if action_key == "flirt":
            if friend_value < 5 or open_value < 1:
                return False, relationship_block_text(key, action_key)
            if not talked_today and friend_value < 8:
                return False, relationship_block_text(key, action_key)
            return True, ""

        return True, ""

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
