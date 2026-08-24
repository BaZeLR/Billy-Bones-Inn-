# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -20 python:
    RELATIONSHIP_FRIEND_THRESHOLDS = (5, 8, 11, 15)
    RELATIONSHIP_CORRUPTION_THRESHOLDS = (10, 20, 35, 55)

    RELATIONSHIP_FRIEND_LABELS = (
        "чужая",
        "знакомая",
        "дружелюбная",
        "близкая",
        "преданная",
    )

    RELATIONSHIP_CORRUPTION_LABELS = (
        "скромная",
        "любопытная",
        "смелая",
        "раскованная",
        "бесстыдная",
    )

    RELATIONSHIP_PHASE_ROWS = (
        ("distant", "чужая"),
        ("familiar", "знакомая"),
        ("friendly", "подруга"),
        ("trusted", "доверяет"),
        ("flirty", "кокетливая"),
        ("intimate", "близкая"),
        ("devoted", "очень близкая"),
    )

    def _relationship_int(value, default=0):
        try:
            return int(value)
        except Exception:
            try:
                return int(float(value))
            except Exception:
                return default

    def npc_friend_value(npc_id=""):
        key = str(npc_id or "").strip().lower()
        info = people.get_info(key)
        return _relationship_int(getattr(info, "rel", 0), 0) if info is not None and key else 0

    def npc_corruption_value(npc_id=""):
        key = str(npc_id or "").strip().lower()
        info = people.get_info(key)
        return _relationship_int(getattr(info, "corruption", 0), 0) if info is not None and key else 0

    def _relationship_level_from_thresholds(value, thresholds):
        score = _relationship_int(value, 0)
        level = 0
        for idx, threshold in enumerate(tuple(thresholds or ())):
            if score >= _relationship_int(threshold, 0):
                level = idx + 1
        return max(0, min(4, level))

    def npc_friend_level(npc_id=""):
        return _relationship_level_from_thresholds(npc_friend_value(npc_id), RELATIONSHIP_FRIEND_THRESHOLDS)

    def npc_corruption_level(npc_id=""):
        return _relationship_level_from_thresholds(npc_corruption_value(npc_id), RELATIONSHIP_CORRUPTION_THRESHOLDS)

    def npc_relationship_phase(npc_id=""):
        friend_level = npc_friend_level(npc_id)
        corruption_level = npc_corruption_level(npc_id)

        if friend_level >= 4 and corruption_level >= 4:
            return {"key": "devoted", "label": "очень близкая", "index": 6}
        if friend_level >= 3 and corruption_level >= 3:
            return {"key": "intimate", "label": "близкая", "index": 5}
        if friend_level >= 2 and corruption_level >= 2:
            return {"key": "flirty", "label": "кокетливая", "index": 4}
        if friend_level >= 3:
            return {"key": "trusted", "label": "доверяет", "index": 3}
        if friend_level >= 2:
            return {"key": "friendly", "label": "подруга", "index": 2}
        if friend_level >= 1:
            return {"key": "familiar", "label": "знакомая", "index": 1}
        return {"key": "distant", "label": "чужая", "index": 0}

    def build_npc_relationship_level(npc_id=""):
        key = str(npc_id or "").strip().lower()
        if key == "":
            return {}

        friend_value = npc_friend_value(key)
        corruption_value = npc_corruption_value(key)
        friend_level = npc_friend_level(key)
        corruption_level = npc_corruption_level(key)
        phase = npc_relationship_phase(key)

        return {
            "npc_id": key,
            "friend_value": friend_value,
            "corruption_value": corruption_value,
            "friend_level": friend_level,
            "corruption_level": corruption_level,
            "friend_label": str(RELATIONSHIP_FRIEND_LABELS[friend_level]),
            "corruption_label": str(RELATIONSHIP_CORRUPTION_LABELS[corruption_level]),
            "phase_key": str(phase.get("key", "") or ""),
            "phase_label": str(phase.get("label", "") or ""),
            "phase_index": _relationship_int(phase.get("index", 0), 0),
        }

    def npc_relationship_level(npc_id=""):
        key = str(npc_id or "").strip().lower()
        if key == "":
            return {}
        return build_npc_relationship_level(key)

    def npc_relationship_label(npc_id=""):
        return str(npc_relationship_level(npc_id).get("phase_label", "") or "")
