# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -40 python:
    OLD_POINT_TALK_UNLOCKS = {
        "flirt": 10,
        "gift": 30,
        "kino": 100,
    }

    def old_point_talk_info(girl_name=""):
        return people.get_info(str(girl_name or "").strip().lower())

    def old_point_rel_cap(info=None):
        if info is None:
            return 100
        return max(20, people_to_int(getattr(info, "relationship_cap", 100), 100))

    def old_point_change_relation(girl_name="", amount=0):
        info = old_point_talk_info(girl_name)
        if info is None:
            return 0
        cap = old_point_rel_cap(info)
        info.rel = max(0, min(cap, people_to_int(getattr(info, "rel", 0), 0) + people_to_int(amount, 0)))
        return info.rel

    def old_point_action_unlocked(girl_name="", action_name=""):
        info = old_point_talk_info(girl_name)
        action_key = str(action_name or "").strip().lower()
        if info is None:
            return False
        if relationship_anger(girl_name) > 0:
            return False
        need = OLD_POINT_TALK_UNLOCKS.get(action_key, 0)
        return people_to_int(getattr(info, "rel", 0), 0) >= need

    def old_point_apology_available(girl_name=""):
        return relationship_anger(girl_name) > 0

    def old_point_social_attempt_score(girl_name="", action_name=""):
        key = str(girl_name or "").strip().lower()
        info = old_point_talk_info(key)
        if info is None:
            return -5
        base = resolve_player_social_delta(key, action_name)
        base = relationship_adjust_social_score(key, action_name, base)
        if people_to_int(getattr(info, "corruption", 0), 0) >= 30:
            base += 1
        if people_to_int(getattr(info, "mana", 0), 0) >= 55:
            base += 1
        if people_to_int(getattr(info, "anger_with_player", 0), 0) >= 30:
            base -= 2
        return max(-5, min(5, base))

    def old_point_flirt_attempt(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if not old_point_action_unlocked(key, "flirt"):
            return {"ok": False, "text": relationship_block_text(key, "flirt"), "gain": 0}
        info = old_point_talk_info(key)
        before = people_to_int(getattr(info, "rel", 0), 0)
        score = old_point_social_attempt_score(key, "flirt")
        gain = 1 if score > 1 else (-1 if score < 0 else 0)
        apply_social_interaction_base(key, "flirt", gain, 4, 30, 1, 1, 0, 0)
        relationship_after_social_result(key, "flirt", score, score >= 0)
        actual = people_to_int(getattr(info, "rel", 0), 0) - before
        if score > 1:
            text = "%s принимает ваш флирт и отвечает теплее, чем просто вежливостью." % _action_display_name(key)
        elif score < 0:
            text = "%s явно не в том настроении. Флирт звучит не вовремя и только портит воздух между вами." % _action_display_name(key)
        else:
            text = "%s замечает ваш тон, но оставляет его без ясного ответа." % _action_display_name(key)
        if actual != 0:
            text += "\n\nОтношения: %+d." % actual
        return {"ok": True, "text": text, "gain": actual}

    def old_point_kino_attempt(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if not old_point_action_unlocked(key, "kino"):
            return {"ok": False, "text": "%s пока не готова к такой близости." % _action_display_name(key), "gain": 0}
        info = old_point_talk_info(key)
        before = people_to_int(getattr(info, "rel", 0), 0)
        score = old_point_social_attempt_score(key, "kino")
        gain = 1 if score > 0 else (-1 if score < -1 else 0)
        apply_social_interaction_base(key, "kino", gain, 5, 30, 1, 0, 0, 0)
        if score > 0:
            info.change_social(corruption_delta=1)
            relationship_after_social_result(key, "kino", score, True)
            text = "%s не отстраняется от вашей близости. На этот раз прикосновение становится частью разговора, а не ошибкой." % _action_display_name(key)
        elif score < -1:
            relationship_after_social_result(key, "kino", score, False)
            text = "%s резко дает понять, что сейчас вы перешли границу." % _action_display_name(key)
        else:
            relationship_after_social_result(key, "kino", 0, True)
            text = "%s позволяет моменту повиснуть, но не развивает его дальше." % _action_display_name(key)
        actual = people_to_int(getattr(info, "rel", 0), 0) - before
        if actual != 0:
            text += "\n\nОтношения: %+d." % actual
        return {"ok": True, "text": text, "gain": actual}

    def old_point_apology_apply(girl_name=""):
        key = str(girl_name or "").strip().lower()
        info = old_point_talk_info(key)
        if info is None:
            return "Сейчас рядом нет собеседницы."
        reason = str(relationship_state(key).get("anger_reason", "") or "bad_action")
        relationship_calm(key, 2)
        if relationship_anger(key) <= 0:
            old_point_change_relation(key, 1)
            if hasattr(info, "anger_with_player"):
                info.anger_with_player = max(0, people_to_int(getattr(info, "anger_with_player", 0), 0) - 20)
            result = "%s выслушивает извинение. Обиды не исчезают мгновенно, но она видит, что вы признаете ошибку." % _action_display_name(key)
            result += "\n\nОтношения: +1."
        else:
            result = "%s все еще сердится. Слова помогают, но ей нужно больше времени и нормального поведения." % _action_display_name(key)
        if reason:
            result = "Причина ссоры: %s.\n\n%s" % (reason, result)
        info.mark_talked()
        calendar_v2.advance_minutes(10)
        return result


label OldPointFlirtAttempt(girl_name=""):
    $ renpy.dynamic("_old_flirt_result")
    $ _old_flirt_result = old_point_flirt_attempt(girl_name)
    $ scene_runtime.text = str(_old_flirt_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    return


label OldPointKinoAttempt(girl_name=""):
    $ renpy.dynamic("_old_kino_result")
    $ _old_kino_result = old_point_kino_attempt(girl_name)
    $ scene_runtime.text = str(_old_kino_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    return


label OldPointApology(girl_name=""):
    $ scene_runtime.text = old_point_apology_apply(girl_name)
    $ scene_runtime.location_text = scene_runtime.text
    return
