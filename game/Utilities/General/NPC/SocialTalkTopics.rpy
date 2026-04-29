# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
default SocialTalkTopicSeen = {}

init -39 python:
    SOCIAL_TALK_TOPICS = [
        {"id": "job_routine", "label": "О работе и распорядке", "min_friend": 0, "min_open": 0},
        {"id": "chat", "label": "Просто поболтать", "min_friend": 0, "min_open": 0},
        {"id": "dances", "label": "О танцах", "min_friend": 2, "min_open": 0},
        {"id": "gossip", "label": "О слухах", "min_friend": 2, "min_open": 1},
        {"id": "forest", "label": "О лесе", "min_friend": 1, "min_open": 0},
        {"id": "stories", "label": "Послушать истории", "min_friend": 3, "min_open": 2},
        {"id": "food", "label": "О еде", "min_friend": 0, "min_open": 0},
        {"id": "fashion", "label": "Об одежде и внешности", "min_friend": 3, "min_open": 2},
        {"id": "money", "label": "О деньгах", "min_friend": 4, "min_open": 2},
    ]

    SOCIAL_FLIRT_TOPICS = [
        {"id": "joke", "label": "Сказать игривую шутку", "min_friend": 5, "min_open": 0, "min_slut": 0},
        {"id": "kino", "label": "Мягко перейти к прикосновениям", "min_friend": 6, "min_open": 2, "min_slut": 0},
        {"id": "flirt", "label": "Открыто заигрывать", "min_friend": 7, "min_open": 3, "min_slut": 4},
        {"id": "sex_topics", "label": "Заговорить о близости", "min_friend": 9, "min_open": 5, "min_slut": 8},
    ]

    SOCIAL_TALK_PROFILES = {
        "amanda": {
            "talk": {"job_routine": -1, "chat": 2, "dances": 4, "gossip": 2, "forest": 0, "stories": 1, "food": 1, "fashion": 4, "money": 1},
            "flirt": {"joke": 3, "kino": 2, "flirt": 3, "sex_topics": 2},
        },
        "melissa": {
            "talk": {"job_routine": 3, "chat": 1, "dances": 0, "gossip": -1, "forest": 2, "stories": 3, "food": 2, "fashion": 1, "money": 0},
            "flirt": {"joke": 1, "kino": 2, "flirt": 1, "sex_topics": -2},
        },
        "sandra": {
            "talk": {"job_routine": 4, "chat": 0, "dances": -1, "gossip": 1, "forest": 1, "stories": 0, "food": 4, "fashion": 2, "money": 3},
            "flirt": {"joke": 0, "kino": -1, "flirt": -2, "sex_topics": -4},
        },
        "clara": {
            "talk": {"job_routine": 1, "chat": 2, "dances": 2, "gossip": 4, "forest": 3, "stories": 3, "food": 0, "fashion": 4, "money": 2},
            "flirt": {"joke": 2, "kino": 3, "flirt": 4, "sex_topics": 3},
        },
    }

    SOCIAL_EARLY_CARE_GIFT_IDS = ("soap_001", "luxury_soap_001", "energy_tea_001", "berries_001", "lavender_001", "wild_rose_001")

    SOCIAL_TOPIC_TEXT = {
        "talk": {
            "job_routine": {
                "good": "Вы обсуждаете работу в трактире спокойно и по делу. {name} отвечает охотно: ей нравится, когда вы говорите не приказами, а как хозяин, который понимает общий труд.",
                "neutral": "Вы говорите о работе и распорядке. {name} слушает, отвечает коротко и без особого тепла, но разговор остается полезным.",
                "bad": "Вы заводите разговор о работе неудачно. {name} явно слышит в этом очередную придирку и отвечает холоднее обычного.",
            },
            "chat": {
                "good": "Вы просто болтаете с {name} о пустяках, и разговор неожиданно выходит теплым. Несколько минут проходят легко.",
                "neutral": "Вы немного болтаете с {name}. Ничего важного не всплывает, но и неловкости не возникает.",
                "bad": "Вы пытаетесь поболтать с {name}, но настроение не сходится. Разговор быстро вязнет.",
            },
            "dances": {
                "good": "Разговор о танцах оживляет {name}. В голосе появляется улыбка, а вместе с ней и больше доверия.",
                "neutral": "Вы говорите о танцах. {name} поддерживает тему, но без особого блеска.",
                "bad": "Тема танцев сейчас задевает {name} не с той стороны. Она отвечает сухо и быстро переводит разговор.",
            },
            "gossip": {
                "good": "{name} охотно делится парой трактирных слухов. Вы оба понимаете, что такие разговоры иногда полезны для дела.",
                "neutral": "Вы осторожно обсуждаете слухи. {name} слушает, но лишнего не говорит.",
                "bad": "{name} не нравится, что вы тянете ее в сплетни. Разговор становится заметно прохладнее.",
            },
            "forest": {
                "good": "Вы говорите о лесе, дороге и добыче. {name} слушает внимательно и явно ценит, что это связано с выживанием трактира.",
                "neutral": "Разговор о лесе выходит спокойным, но коротким. {name} признает, что знать это полезно.",
                "bad": "Вы заводите тему леса не к месту. {name} отмахивается: сейчас у нее хватает дел в доме.",
            },
            "stories": {
                "good": "{name} задерживается рядом и слушает историю до конца. В ответ она тоже рассказывает немного больше, чем собиралась.",
                "neutral": "Вы рассказываете историю. {name} слушает вежливо, но держит привычную дистанцию.",
                "bad": "История не цепляет {name}. Она выслушивает из вежливости и явно ждет, когда можно будет вернуться к делам.",
            },
            "food": {
                "good": "Разговор о еде быстро становится разговором о том, как сделать общий стол лучше. {name} явно нравится такой практичный подход.",
                "neutral": "Вы обсуждаете еду и запасы. {name} кивает: тема полезная, пусть и будничная.",
                "bad": "{name} воспринимает разговор о еде как мелочную проверку и отвечает раздраженно.",
            },
            "fashion": {
                "good": "Вы говорите об одежде и чистом виде без грубости. {name} слышит в этом заботу, а не насмешку.",
                "neutral": "Тема одежды проходит ровно. {name} не возражает, но и особенно не раскрывается.",
                "bad": "Вы задеваете тему внешности слишком неуклюже. {name} принимает это как давление.",
            },
            "money": {
                "good": "Вы говорите о деньгах прямо: трактиру нужно выжить, а хороший доход значит больше уважения и лучшую жизнь для всех. {name} принимает этот довод всерьез.",
                "neutral": "Разговор о деньгах выходит сухим, но понятным. {name} соглашается, что без счета трактир не удержать.",
                "bad": "Денежный разговор звучит для {name} слишком холодно. Она отвечает, что люди не монеты в трактирной книге.",
            },
        },
        "flirt": {
            "joke": {
                "good": "Вы отпускаете легкую игривую шутку. {name} улыбается и отвечает уже заметно мягче.",
                "neutral": "Шутка выходит осторожной. {name} замечает ее, но не спешит подыгрывать.",
                "bad": "Шутка попадает мимо. {name} смотрит на вас так, что продолжать сейчас явно не стоит.",
            },
            "kino": {
                "good": "Вы осторожно сокращаете дистанцию, не давя. {name} не отстраняется, и между вами становится теплее.",
                "neutral": "Вы пробуете перейти к более близкому тону. {name} позволяет это, но держит границу.",
                "bad": "Вы торопитесь с близостью. {name} отстраняется и дает понять, что сейчас это лишнее.",
            },
            "flirt": {
                "good": "Вы заигрываете открыто, но без нажима. {name} отвечает взглядом и явно запоминает этот тон.",
                "neutral": "Вы флиртуете с {name}. Ответ сдержанный, но дверь не закрыта.",
                "bad": "Флирт звучит слишком рано или слишком резко. {name} холодеет и закрывается.",
            },
            "sex_topics": {
                "good": "Вы осторожно переводите разговор к близости. {name} краснеет, но не уходит от темы.",
                "neutral": "Вы пробуете заговорить о близости. {name} слушает настороженно и отвечает очень аккуратно.",
                "bad": "Тема близости оказывается преждевременной. {name} резко обрывает разговор.",
            },
        },
    }

    def social_topic_return_label(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if key == "amanda":
            return "IntAmandaTalkRefresh"
        if key == "melissa":
            return "IntMelissaTalkRefresh"
        if key == "sandra":
            return "IntSandraTalkRefresh"
        if key == "clara":
            return "IntClaraTalkRefresh"
        return ""

    def social_topic_entries(mode="talk"):
        return list(SOCIAL_FLIRT_TOPICS if str(mode or "").strip().lower() == "flirt" else SOCIAL_TALK_TOPICS)

    def social_topic_label(mode="talk", topic_id=""):
        topic_key = str(topic_id or "").strip()
        for row in social_topic_entries(mode):
            if str(row.get("id", "") or "") == topic_key:
                return str(row.get("label", "") or topic_key)
        return topic_key

    def social_topic_profile(girl_name="", mode="talk"):
        key = str(girl_name or "").strip().lower()
        mode_key = str(mode or "talk").strip().lower()
        return dict(dict(SOCIAL_TALK_PROFILES.get(key, {}) or {}).get(mode_key, {}) or {})

    def social_topic_visible(girl_name="", mode="talk", topic_id=""):
        key = str(girl_name or "").strip().lower()
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        if key not in SOCIAL_TALK_PROFILES:
            return False
        if key == "clara" and mode_key == "flirt":
            try:
                if not clara_can_start_social_events():
                    return False
            except Exception:
                return False
        if mode_key == "talk" and int(TalkedToday.get(key, 0) or 0) > 0:
            return False
        if mode_key == "flirt" and int(FlirtedToday.get(key, 0) or 0) > 0:
            return False
        allowed, reason = relationship_social_action_allowed(key, mode_key)
        if not allowed:
            return False
        for row in social_topic_entries(mode_key):
            if str(row.get("id", "") or "") != topic_key:
                continue
            if int(Friends.get(key, 0) or 0) < int(row.get("min_friend", 0) or 0):
                return False
            if int(otkroven.get(key, 0) or 0) < int(row.get("min_open", 0) or 0):
                return False
            if mode_key == "flirt" and int(sluttiness.get(key, 0) or 0) < int(row.get("min_slut", 0) or 0):
                return False
            return True
        return False

    def social_visible_topic_entries(girl_name="", mode="talk"):
        rows = []
        for row in social_topic_entries(mode):
            if social_topic_visible(girl_name, mode, row.get("id", "")):
                rows.append(dict(row))
        return rows

    def social_has_visible_topics(girl_name="", mode="talk"):
        return len(social_visible_topic_entries(girl_name, mode)) > 0

    def social_topic_score(girl_name="", mode="talk", topic_id=""):
        key = str(girl_name or "").strip().lower()
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        base = int(social_topic_profile(key, mode_key).get(topic_key, 0) or 0)
        mood = 0
        if int(Friends.get(key, 0) or 0) >= 10:
            mood += 1
        if int(otkroven.get(key, 0) or 0) >= 8:
            mood += 1
        if mode_key == "flirt" and int(sluttiness.get(key, 0) or 0) >= 15:
            mood += 1
        if int(Drunk.get(key, 0) or 0) > 0:
            mood += 1
        adjusted = relationship_adjust_social_score(key, mode_key, max(-5, min(5, base + mood)))
        try:
            adjusted = player_social_adjusted_delta(key, mode_key, adjusted)
        except Exception:
            pass
        return adjusted

    def social_topic_notify_result(girl_name="", mode="talk", topic_id="", topic_score=0, final_score=0, relation_delta=0):
        topic_name = social_topic_label(mode, topic_id)
        base_value = int(topic_score or 0)
        final_value = int(final_score or 0)
        relation_value = int(relation_delta or 0)
        base_text = "+%d" % base_value if base_value > 0 else str(base_value)
        final_text = "+%d" % final_value if final_value > 0 else str(final_value)
        relation_text = "+%d" % relation_value if relation_value > 0 else str(relation_value)
        if base_value == final_value:
            message = "Тема: %s (%s). Отношения: %s." % (topic_name, base_text, relation_text)
        else:
            message = "Тема: %s (%s -> %s). Отношения: %s." % (topic_name, base_text, final_text, relation_text)
        try:
            renpy.notify(message)
        except Exception:
            pass
        return message

    def social_topic_result_kind(score=0):
        value = int(score or 0)
        if value >= 2:
            return "good"
        if value <= -2:
            return "bad"
        return "neutral"

    def social_topic_text(girl_name="", mode="talk", topic_id="", score=0):
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        kind = social_topic_result_kind(score)
        text = str(dict(dict(SOCIAL_TOPIC_TEXT.get(mode_key, {}) or {}).get(topic_key, {}) or {}).get(kind, "") or "")
        if not text:
            text = "Вы некоторое время говорите с {name}."
        return text.format(name=_action_display_name(girl_name))

    def social_apply_topic(girl_name="", mode="talk", topic_id=""):
        key = str(girl_name or "").strip().lower()
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        if not social_topic_visible(key, mode_key, topic_key):
            allowed, reason = relationship_social_action_allowed(key, mode_key)
            return {"ok": False, "text": str(reason or "Сейчас этот разговор не складывается."), "score": 0}
        friends_before = int(Friends.get(key, 0) or 0)
        topic_score = int(social_topic_profile(key, mode_key).get(topic_key, 0) or 0)
        score = social_topic_score(key, mode_key, topic_key)
        if mode_key == "flirt":
            apply_social_interaction_base(key, "flirt", score, 2 if score > 0 else 0, 30, 1, 1, 0, 0, True)
            if score > 0:
                add_to_stat_dict(sluttiness, key, max(1, score), 0, 100)
            elif score < 0:
                add_to_stat_dict(otkroven, key, score, 0, 20)
        else:
            apply_social_interaction_base(key, "talk", score, 1 if score > 0 else 0, 30, 1, 0, 0, 1, True)
            if score > 0:
                add_to_stat_dict(otkroven, key, max(1, score // 2), 0, 20)
        actual_score = social_score_delta_for(key, friends_before)
        SocialTalkTopicSeen["%s:%s:%s:%s" % (int(dayspassed or 0), key, mode_key, topic_key)] = score
        try:
            info = getPersonInfo(key)
            if info is not None and mode_key == "talk":
                info.talkToday.add(topic_key)
        except Exception:
            pass
        relationship_after_social_result(key, mode_key, score, True)
        result_text = append_social_score_message(social_topic_text(key, mode_key, topic_key, score), actual_score, False)
        social_topic_notify_result(key, mode_key, topic_key, topic_score, score, actual_score)
        try:
            player_social_condition_notify(key)
        except Exception:
            pass
        return {"ok": True, "text": result_text, "score": actual_score, "raw_score": score}

    def social_gift_score(girl_name="", item_id="", base_gain=2):
        key = str(girl_name or "").strip().lower()
        item_key = str(item_id or "").strip()
        allowed, reason = relationship_social_action_allowed(key, "gift", item_key)
        if not allowed:
            return -3
        base = max(0, min(5, int(base_gain or 0)))
        try:
            preferred = item_key in tuple(preferred_gift_item_ids(key) or ())
        except Exception:
            preferred = False
        if preferred:
            score = max(2, base + 1)
        elif item_key in SOCIAL_EARLY_CARE_GIFT_IDS:
            score = max(1, min(4, base))
        else:
            score = 0
            if key in SOCIAL_TALK_PROFILES and int(Friends.get(key, 0) or 0) < 5:
                score = -2
        if int(Friends.get(key, 0) or 0) >= 10:
            score += 1
        if int(GiftedToday.get(key, 0) or 0) > 0:
            score -= 3
        return relationship_adjust_social_score(key, "gift", max(-5, min(5, score)))

    def social_gift_acceptance(girl_name="", item_id="", base_gain=2):
        key = str(girl_name or "").strip().lower()
        item_key = str(item_id or "").strip()
        allowed, reason = relationship_social_action_allowed(key, "gift", item_key)
        if not allowed:
            return False, -3
        score = social_gift_score(key, item_key, base_gain)
        if item_key in SOCIAL_EARLY_CARE_GIFT_IDS:
            return True, score
        if key in SOCIAL_TALK_PROFILES and int(Friends.get(key, 0) or 0) < 3 and score <= 0:
            return False, score
        return True, score

    def social_gift_text(girl_name="", gift_name="", item_id="", score=0):
        key = str(girl_name or "").strip().lower()
        gift = str(gift_name or "подарок").strip()
        value = int(score or 0)
        name = _action_display_name(key)
        if value >= 3:
            return "%s принимает %s с явным удовольствием. Похоже, вы угадали не только с вещью, но и с моментом." % (name, gift)
        if value > 0:
            return "%s принимает %s спокойно, но теплеет к вам: подарок оказался уместным." % (name, gift)
        if value == 0:
            return "%s принимает %s вежливо. Это не задевает ее, но и особенного впечатления не производит." % (name, gift)
        return "%s не хочет брать %s. Сейчас такой подарок кажется ей не заботой, а давлением." % (name, gift)


label SocialTalkTopicMenu(girl_name="", mode="talk", return_label=""):
    $ _social_girl = str(girl_name or "").strip().lower()
    $ _social_mode = str(mode or "talk").strip().lower()
    $ _social_return = str(return_label or social_topic_return_label(_social_girl) or "").strip()
    $ main_ui_begin_talk_state("Разговор с %s" % _action_display_name(_social_girl), _social_girl)
    $ current_action_title = "О чем говорить" if _social_mode == "talk" else "Как флиртовать"
    $ current_action_content = None
    $ current_action_items = []
    python:
        for _topic in social_visible_topic_entries(_social_girl, _social_mode):
            current_action_items.append(MenuItem(str(_topic.get("label", "") or ""), Function(main_ui_call_label, "SocialTalkTopicApply", _social_girl, _social_mode, str(_topic.get("id", "") or ""), _social_return)))
        if len(current_action_items) <= 0:
            MainTxt = "Сейчас подходящих тем нет."
            CurLocDesc = MainTxt
    if _social_return != "":
        $ current_action_items.append(MenuItem("Назад", Function(main_ui_call_label, _social_return, _social_girl)))
    else:
        $ current_action_items.append(MenuItem("Назад", Function(main_ui_end_talk_state)))
    return


label SocialTalkTopicApply(girl_name="", mode="talk", topic_id="", return_label=""):
    $ _social_girl = str(girl_name or "").strip().lower()
    $ _social_return = str(return_label or social_topic_return_label(_social_girl) or "").strip()
    $ _social_result = social_apply_topic(_social_girl, mode, topic_id)
    $ MainTxt = str(_social_result.get("text", "") or "")
    $ CurLocDesc = MainTxt
    $ update_stat_state()
    if _social_return != "":
        call expression _social_return pass (_social_girl)
    return
