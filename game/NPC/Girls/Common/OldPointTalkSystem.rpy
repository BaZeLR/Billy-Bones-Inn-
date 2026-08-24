            info.relationship = info.rel            info.relationship = info.rel            info.relationship = info.rel# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init -40 python:
    OLD_POINT_TALK_TOPICS = (
        ("job_routine", "О работе в трактире"),
        ("chat", "О простой болтовне"),
        ("dances", "О танцах"),
        ("gossip", "О городских слухах"),
        ("forest", "О лесе и прогулках"),
        ("stories", "О старых историях"),
        ("food", "О еде и угощениях"),
        ("fashion", "О платьях и внешности"),
        ("money", "О деньгах и выгоде"),
        ("family_life", "О доме и семье"),
    )

    OLD_POINT_TALK_TOPIC_IDS = tuple(row[0] for row in OLD_POINT_TALK_TOPICS)
    OLD_POINT_TALK_UNLOCKS = {
        "flirt": 10,
        "gift": 30,
        "kino": 100,
    }

    def old_point_talk_info(girl_name=""):
        return getPersonInfo(str(girl_name or "").strip().lower())

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
        if hasattr(info, "relationship"):
        return info.rel

    def old_point_preferred_topics(girl_name=""):
        info = old_point_talk_info(girl_name)
        preferences = getattr(info, "talk_preferences", {}) if info is not None else {}
        favorites = []
        if isinstance(preferences, dict):
            favorites = list(preferences.get("favorite_topics", []) or [])
        return tuple(topic for topic in favorites if topic in OLD_POINT_TALK_TOPIC_IDS)

    def old_point_smalltalk_done_today(girl_name=""):
        info = old_point_talk_info(girl_name)
        if info is None:
            return False
        var = getattr(info, "var", None)
        if not isinstance(var, dict):
            return people_to_int(getattr(info, "talked_today", 0), 0) > 0
        return people_to_int(var.get("smalltalk_finished_day", -1), -1) == people_to_int(current_game_day(), 0)

    def old_point_smalltalk_start(girl_name=""):
        info = old_point_talk_info(girl_name)
        if info is None or not isinstance(getattr(info, "var", None), dict):
            return []
        day_value = people_to_int(current_game_day(), 0)
        if people_to_int(info.var.get("smalltalk_active_day", -1), -1) != day_value:
            info.var["smalltalk_active_day"] = day_value
            info.var["smalltalk_seen_topics"] = []
            info.var["smalltalk_positive_count"] = 0
        if not isinstance(info.var.get("smalltalk_seen_topics", []), list):
            info.var["smalltalk_seen_topics"] = []
        return list(info.var.get("smalltalk_seen_topics", []) or [])

    def old_point_smalltalk_seen_topics(girl_name=""):
        info = old_point_talk_info(girl_name)
        if info is None or not isinstance(getattr(info, "var", None), dict):
            return []
        if people_to_int(info.var.get("smalltalk_active_day", -1), -1) != people_to_int(current_game_day(), 0):
            return []
        return list(info.var.get("smalltalk_seen_topics", []) or [])

    def old_point_smalltalk_turn_count(girl_name=""):
        return min(10, len(old_point_smalltalk_seen_topics(girl_name)))

    def old_point_smalltalk_topic_available(girl_name="", topic_id=""):
        topic_key = str(topic_id or "").strip().lower()
        if topic_key not in OLD_POINT_TALK_TOPIC_IDS:
            return False
        if old_point_smalltalk_done_today(girl_name):
            return False
        if old_point_smalltalk_turn_count(girl_name) >= 10:
            return False
        return topic_key not in old_point_smalltalk_seen_topics(girl_name)

    def old_point_smalltalk_finish(girl_name=""):
        key = str(girl_name or "").strip().lower()
        info = old_point_talk_info(key)
        if info is None:
            return "Разговор закончен."
        turn_count = old_point_smalltalk_turn_count(key)
        if turn_count <= 0:
            return "Вы пока не начали обычную болтовню."
        if isinstance(getattr(info, "var", None), dict):
            info.var["smalltalk_finished_day"] = people_to_int(current_game_day(), 0)
            info.var["smalltalk_last_turns"] = turn_count
        info.mark_talked()
        calendar_v2.advance_minutes(20)
        player.change_stat("fun", 15)
        return "Вы заканчиваете обычную болтовню. Разговор занял двадцать минут и немного развеял скуку."

    def old_point_smalltalk_available(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if not key or old_point_smalltalk_done_today(key):
            return False
        if relationship_anger(key) > 0:
            return False
        return old_point_talk_info(key) is not None

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

    def old_point_smalltalk_apply(girl_name="", topic_id=""):
        key = str(girl_name or "").strip().lower()
        topic_key = str(topic_id or "").strip().lower()
        info = old_point_talk_info(key)
        if info is None:
            return {"ok": False, "text": "Сейчас рядом нет собеседницы.", "gain": 0, "preferred": False}
        if old_point_smalltalk_done_today(key):
            return {"ok": False, "text": "%s сегодня уже говорила с вами достаточно." % _action_display_name(key), "gain": 0, "preferred": False}
        if topic_key not in OLD_POINT_TALK_TOPIC_IDS:
            return {"ok": False, "text": "Такой темы сейчас нет в обычной болтовне.", "gain": 0, "preferred": False}
        seen_topics = old_point_smalltalk_start(key)
        if len(seen_topics) >= 10:
            return {"ok": False, "text": "На сегодня вы уже перебрали все обычные темы.", "gain": 0, "preferred": False}
        if topic_key in seen_topics:
            return {"ok": False, "text": "Эту тему вы сегодня уже обсудили.", "gain": 0, "preferred": False}

        preferred = topic_key in old_point_preferred_topics(key)
        gain = 0
        if preferred:
            gain = 1 + (procedural_randint(1, 2, "old_smalltalk_%s_%s_%s" % (key, topic_key, current_game_day())) - 1)
            old_point_change_relation(key, gain)
            relationship_after_social_result(key, "talk", gain, True)
        else:
            relationship_after_social_result(key, "talk", 0, True)

        if isinstance(getattr(info, "var", None), dict):
            seen_topics.append(topic_key)
            info.var["smalltalk_seen_topics"] = seen_topics
            info.var["last_smalltalk_topic"] = topic_key
            info.var["last_smalltalk_preferred"] = 1 if preferred else 0
            if preferred and gain > 0:
                info.var["smalltalk_positive_count"] = people_to_int(info.var.get("smalltalk_positive_count", 0), 0) + 1

        if preferred:
            text = "%s охотно поддерживает эту тему. Разговор выходит живее обычного, и вы чувствуете, что попали в то, что ей действительно интересно." % _action_display_name(key)
        else:
            text = "%s отвечает вежливо, но без настоящего интереса. Тема не цепляет ее, хотя сама болтовня все равно немного развеивает скуку." % _action_display_name(key)
        text += "\n\nТем в этой болтовне: %s из 10." % old_point_smalltalk_turn_count(key)
        if gain > 0:
            text += "\n\nОтношения: +%s." % gain
        return {"ok": True, "text": text, "gain": gain, "preferred": preferred}

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
        apply_social_interaction_base(key, "flirt", gain, 4, 30, 1, 1, 0, 0, True)
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
        apply_social_interaction_base(key, "kino", gain, 5, 30, 1, 0, 0, 0, True)
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


label OldPointSmallTalkMenu(girl_name=""):
    $ _old_talk_name = str(girl_name or "").strip().lower()
    $ main_ui_begin_talk_state("Обычный разговор", _old_talk_name)
    if not old_point_smalltalk_available(_old_talk_name):
        $ MainTxt = "%s сегодня не готова к обычной болтовне." % _action_display_name(_old_talk_name)
        $ CurLocDesc = MainTxt
        return
    $ old_point_smalltalk_start(_old_talk_name)
    while old_point_smalltalk_available(_old_talk_name) and old_point_smalltalk_turn_count(_old_talk_name) < 10:
        menu:
            "О работе в трактире" if old_point_smalltalk_topic_available(_old_talk_name, "job_routine"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "job_routine")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О простой болтовне" if old_point_smalltalk_topic_available(_old_talk_name, "chat"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "chat")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О танцах" if old_point_smalltalk_topic_available(_old_talk_name, "dances"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "dances")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О городских слухах" if old_point_smalltalk_topic_available(_old_talk_name, "gossip"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "gossip")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О лесе и прогулках" if old_point_smalltalk_topic_available(_old_talk_name, "forest"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "forest")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О старых историях" if old_point_smalltalk_topic_available(_old_talk_name, "stories"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "stories")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О еде и угощениях" if old_point_smalltalk_topic_available(_old_talk_name, "food"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "food")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О платьях и внешности" if old_point_smalltalk_topic_available(_old_talk_name, "fashion"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "fashion")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О деньгах и выгоде" if old_point_smalltalk_topic_available(_old_talk_name, "money"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "money")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "О доме и семье" if old_point_smalltalk_topic_available(_old_talk_name, "family_life"):
                $ _old_talk_result = old_point_smalltalk_apply(_old_talk_name, "family_life")
                $ MainTxt = str(_old_talk_result.get("text", "") or "")
                $ CurLocDesc = MainTxt
            "Закончить болтовню" if old_point_smalltalk_turn_count(_old_talk_name) > 0:
                $ MainTxt = old_point_smalltalk_finish(_old_talk_name)
                $ CurLocDesc = MainTxt
                return
            "Назад":
                if old_point_smalltalk_turn_count(_old_talk_name) > 0:
                    $ MainTxt = old_point_smalltalk_finish(_old_talk_name)
                $ CurLocDesc = MainTxt
                return
    if old_point_smalltalk_turn_count(_old_talk_name) >= 10 and not old_point_smalltalk_done_today(_old_talk_name):
        $ MainTxt = old_point_smalltalk_finish(_old_talk_name)
        $ CurLocDesc = MainTxt
    return


label OldPointSmallTalkApply(girl_name="", topic_id=""):
    $ _old_talk_result = old_point_smalltalk_apply(girl_name, topic_id)
    $ MainTxt = str(_old_talk_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    return


label OldPointSmallTalkFinish(girl_name=""):
    $ MainTxt = old_point_smalltalk_finish(girl_name)
    $ CurLocDesc = MainTxt
    return


label OldPointSmallTalkApply(girl_name="", topic_id=""):
    $ _old_talk_result = old_point_smalltalk_apply(girl_name, topic_id)
    $ MainTxt = str(_old_talk_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    return


label OldPointSmallTalkFinish(girl_name=""):
    $ MainTxt = old_point_smalltalk_finish(girl_name)
    $ CurLocDesc = MainTxt
    return


label OldPointSmallTalkApply(girl_name="", topic_id=""):
    $ _old_talk_result = old_point_smalltalk_apply(girl_name, topic_id)
    $ MainTxt = str(_old_talk_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    return


label OldPointSmallTalkFinish(girl_name=""):
    $ MainTxt = old_point_smalltalk_finish(girl_name)
    $ CurLocDesc = MainTxt
    return


label OldPointFlirtAttempt(girl_name=""):
    $ _old_flirt_result = old_point_flirt_attempt(girl_name)
    $ MainTxt = str(_old_flirt_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    return


label OldPointKinoAttempt(girl_name=""):
    $ _old_kino_result = old_point_kino_attempt(girl_name)
    $ MainTxt = str(_old_kino_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    return


label OldPointApology(girl_name=""):
    $ MainTxt = old_point_apology_apply(girl_name)
    $ CurLocDesc = MainTxt
    return
