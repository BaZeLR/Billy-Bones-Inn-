# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

init -39 python:
    SOCIAL_TALK_SESSION_LIMIT = 10

    SOCIAL_TALK_TOPICS = [
        {"id": "job_routine", "label": "О работе и распорядке"},
        {"id": "chat", "label": "Просто поболтать"},
        {"id": "dances", "label": "О танцах"},
        {"id": "gossip", "label": "О слухах"},
        {"id": "forest", "label": "О лесе"},
        {"id": "stories", "label": "Послушать истории"},
        {"id": "food", "label": "О еде"},
        {"id": "fashion", "label": "Об одежде и внешности"},
        {"id": "money", "label": "О деньгах"},
        {"id": "family_life", "label": "О семье и доме"},
    ]

    SOCIAL_FLIRT_TOPICS = [
        {"id": "joke", "label": "Сказать игривую шутку", "min_friend": 5, "min_open": 0, "min_slut": 0},
        {"id": "kino", "label": "Мягко перейти к прикосновениям", "min_friend": 6, "min_open": 2, "min_slut": 0},
        {"id": "flirt", "label": "Открыто заигрывать", "min_friend": 7, "min_open": 3, "min_slut": 4},
        {"id": "sex_topics", "label": "Заговорить о близости", "min_friend": 9, "min_open": 5, "min_slut": 8},
    ]

    SOCIAL_NPC_TOPIC_PACKS = {
        "amanda": {
            "flirt": [
                {"id": "amanda_tease", "label": "Мягко подразнить Аманду", "min_friend": 6, "min_open": 1, "min_slut": 0},
                {"id": "amanda_dance_hint", "label": "Намекнуть на танцы и взгляды", "min_friend": 8, "min_open": 3, "min_slut": 4},
            ],
        },
        "melissa": {
            "flirt": [
                {"id": "melissa_gentle", "label": "Сблизиться без нажима", "min_friend": 7, "min_open": 2, "min_slut": 0},
                {"id": "melissa_private_place", "label": "Намекнуть на укромное место", "min_friend": 10, "min_open": 5, "min_slut": 8},
            ],
        },
        "sandra": {
            "flirt": [
                {"id": "sandra_respect", "label": "Сделать уважительный комплимент", "min_friend": 7, "min_open": 2, "min_slut": 0},
                {"id": "sandra_warmth", "label": "Поблагодарить ее теплее обычного", "min_friend": 10, "min_open": 4, "min_slut": 0},
            ],
        },
        "clara": {
            "flirt": [
                {"id": "clara_clever_game", "label": "Затеять светскую игру", "min_friend": 5, "min_open": 2, "min_slut": 0},
                {"id": "clara_between_lines", "label": "Говорить намеками", "min_friend": 8, "min_open": 4, "min_slut": 2},
            ],
        },
    }

    SOCIAL_DEFAULT_FLIRT_PROFILE = {"joke": 1, "kino": 1, "flirt": 1, "sex_topics": 1}

    SOCIAL_FLIRT_STAT_REQUIREMENTS = {
        "amanda": {"look": 45},
        "melissa": {"charisma": 40},
        "sandra": {"reputation": 20},
        "clara": {"charisma": 70, "exploration": 50},
    }

    def social_person_info(girl_name=""):
        return people.get_info(social_topic_key(girl_name))

    def social_rel_value(girl_name=""):
        info = social_person_info(girl_name)
        return int(getattr(info, "rel", 0) or 0) if info is not None else 0

    def social_open_value(girl_name=""):
        info = social_person_info(girl_name)
        return int(getattr(info, "openness", 0) or 0) if info is not None else 0

    def social_corruption_value(girl_name=""):
        info = social_person_info(girl_name)
        return int(getattr(info, "corruption", 0) or 0) if info is not None else 0

    def social_flirted_today_value(girl_name=""):
        info = social_person_info(girl_name)
        return int(getattr(info, "flirted_today", 0) or 0) if info is not None else 0

    def social_gifted_today_value(girl_name=""):
        info = social_person_info(girl_name)
        return int(getattr(info, "gifted_today", 0) or 0) if info is not None else 0

    def social_talked_today_value(girl_name=""):
        info = social_person_info(girl_name)
        return int(getattr(info, "talked_today", 0) or 0) if info is not None else 0

    def social_drunk_value(girl_name=""):
        info = social_person_info(girl_name)
        return int(getattr(info, "drunk", 0) or 0) if info is not None else 0

    SOCIAL_FLIRT_PROFILES = {
        "amanda": {
            "flirt": {"joke": 3, "kino": 2, "flirt": 3, "sex_topics": 2, "amanda_tease": 3, "amanda_dance_hint": 4},
        },
        "melissa": {
            "flirt": {"joke": 1, "kino": 2, "flirt": 1, "sex_topics": -2, "melissa_gentle": 4, "melissa_private_place": 3},
        },
        "sandra": {
            "flirt": {"joke": 0, "kino": -1, "flirt": -2, "sex_topics": -4, "sandra_respect": 3, "sandra_warmth": 2},
        },
        "clara": {
            "flirt": {"joke": 2, "kino": 3, "flirt": 4, "sex_topics": 3, "clara_clever_game": 4, "clara_between_lines": 4},
        },
        "becky": {
            "flirt": {"joke": 3, "kino": 2, "flirt": 3, "sex_topics": 2},
        },
        "irma": {
            "flirt": {"joke": 1, "kino": 1, "flirt": 2, "sex_topics": 0},
        },
        "inga": {
            "flirt": {"joke": 1, "kino": 1, "flirt": 1, "sex_topics": 0},
        },
        "liza": {
            "flirt": {"joke": 2, "kino": 2, "flirt": 3, "sex_topics": 2},
        },
        "georgett": {
            "flirt": {"joke": 2, "kino": 2, "flirt": 3, "sex_topics": 3},
        },
    }

    SOCIAL_CUSTOM_GIFT_AFFINITY = {
        "amanda": {
            "good": ("lavender_001", "wild_rose_001", "luxury_soap_001", "libido_tincture_001"),
            "bad": ("lumber_001", "chopped_wood_001"),
        },
        "melissa": {
            "good": ("honeycomb_001", "berries_001", "energy_tea_001", "bandage_001"),
            "bad": ("libido_tincture_001",),
        },
        "sandra": {
            "good": ("soap_001", "luxury_soap_001", "energy_tea_001", "food_bale_001"),
            "bad": ("libido_tincture_001",),
        },
        "clara": {
            "good": ("lavender_001", "wild_rose_001", "luxury_soap_001", "special_mushroom_001", "libido_tincture_001"),
            "bad": ("chopped_wood_001",),
        },
    }

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
            "family_life": {
                "good": "Вы говорите о доме и семье без нажима. {name} слышит в этом не приказ, а попытку понять, как ей живется рядом с вами.",
                "neutral": "Разговор о доме проходит спокойно. {name} отвечает осторожно, но не уходит от темы.",
                "bad": "Тема семьи звучит неуклюже. {name} воспринимает ее как попытку напомнить о долге вместо живого внимания.",
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

    SOCIAL_CUSTOM_TOPIC_TEXT = {
        "flirt": {
            "amanda_tease": {
                "good": "Вы мягко поддразниваете Аманду, и она отвечает той же монетой. В этот раз дерзость работает на сближение.",
                "neutral": "Аманда подхватывает шутку, но держит флирт на легкой дистанции.",
                "bad": "Поддразнивание звучит слишком остро. Аманда улыбается, но улыбка выходит колючей.",
            },
            "amanda_dance_hint": {
                "good": "Намек на танцы и взгляды попадает в настроение Аманды. Она явно понимает подтекст и не спешит уходить от игры.",
                "neutral": "Аманда замечает намек, но пока отвечает только насмешливым взглядом.",
                "bad": "Намек на танцы звучит не к месту. Аманда быстро переводит разговор.",
            },
            "melissa_gentle": {
                "good": "Вы сближаетесь с Мелиссой без нажима. Именно эта мягкость позволяет ей не отступить.",
                "neutral": "Мелисса замечает теплый тон, но осторожность пока сильнее ответного движения.",
                "bad": "Даже мягкий флирт сейчас оказывается лишним. Мелисса закрывается.",
            },
            "melissa_private_place": {
                "good": "Намек на укромное место звучит тихо и достаточно бережно. Мелисса смущается, но не обрывает разговор.",
                "neutral": "Мелисса понимает намек и отвечает неопределенно. Решение она оставляет на потом.",
                "bad": "Намек оказывается слишком ранним. Мелисса дает понять, что сейчас это давит на нее.",
            },
            "sandra_respect": {
                "good": "Вы делаете Сандре комплимент через уважение, а не пустые сладкие слова. Такой тон она принимает гораздо охотнее.",
                "neutral": "Сандра выслушивает комплимент спокойно. Ей приятно, но она не показывает этого прямо.",
                "bad": "Комплимент звучит для Сандры как попытка отвлечь ее от дел. Она не подыгрывает.",
            },
            "sandra_warmth": {
                "good": "Вы благодарите Сандру теплее обычного. Она отвечает сдержанно, но между вами становится мягче.",
                "neutral": "Сандра принимает теплую благодарность без лишних слов.",
                "bad": "Теплый тон выходит неожиданно неловким. Сандра решает, что за ним что-то скрывается.",
            },
            "clara_clever_game": {
                "good": "Вы затеваете с Клариссой светскую игру, и она охотно входит в нее. Флирт получается умным и живым.",
                "neutral": "Кларисса принимает игру, но держит инициативу при себе.",
                "bad": "Игра кажется Клариссе слишком простой. Она улыбается вежливо и ускользает из темы.",
            },
            "clara_between_lines": {
                "good": "Вы говорите с Клариссой намеками. Она отвечает тем же, и разговор становится куда интимнее прямых слов.",
                "neutral": "Кларисса слышит подтекст, но оставляет вам только тонкую улыбку вместо ясного ответа.",
                "bad": "Намеки звучат неуклюже. Кларисса делает вид, что не поняла, и этим закрывает флирт.",
            },
        },
    }

    def social_topic_key(girl_name=""):
        key = str(girl_name or "").strip().lower()
        if key == "clarissa":
            return "clara"
        return key

    def social_topic_seen_key(girl_name="", mode="talk", topic_id=""):
        return "%s:%s:%s:%s" % (int(current_game_day() or 0), social_topic_key(girl_name), str(mode or "talk").strip().lower(), str(topic_id or "").strip())

    def social_topic_seen_state(girl_name=""):
        info = social_person_info(girl_name)
        if info is None:
            return {}
        if not isinstance(info.var, dict):
            info.var = {}
        state = info.var.get("social_topic_seen", None)
        if not isinstance(state, dict):
            state = {}
            info.var["social_topic_seen"] = state
        return state

    def social_topic_already_seen(girl_name="", mode="talk", topic_id=""):
        return social_topic_seen_key(girl_name, mode, topic_id) in social_topic_seen_state(girl_name)

    def social_topic_seen_count(girl_name="", mode="talk"):
        prefix = "%s:%s:%s:" % (int(current_game_day() or 0), social_topic_key(girl_name), str(mode or "talk").strip().lower())
        count = 0
        for seen_key in list(social_topic_seen_state(girl_name).keys()):
            if str(seen_key or "").startswith(prefix):
                count += 1
        return count

    def social_talk_session_remaining(girl_name=""):
        return max(0, int(SOCIAL_TALK_SESSION_LIMIT or 10) - social_topic_seen_count(girl_name, "talk"))

    def social_player_stat_value(stat_name=""):
        stat_key = str(stat_name or "").strip().lower()
        try:
            if stat_key == "charisma":
                return int(player_charisma_breakdown().get("charisma", 0) or 0)
            if stat_key == "look":
                return int(player_look_breakdown().get("look", 0) or 0)
            if stat_key == "reputation":
                return int(player_reputation_breakdown().get("reputation", 0) or 0)
            if stat_key == "exploration":
                return int(effective_player_exploration() or 0)
        except Exception:
            return 0
        return 0

    def social_external_requirement_met(girl_name="", action=""):
        key = social_topic_key(girl_name)
        action_key = str(action or "").strip().lower()
        if action_key != "flirt":
            return True
        requirements = dict(SOCIAL_FLIRT_STAT_REQUIREMENTS.get(key, {}) or {})
        for stat_key, needed in requirements.items():
            if social_player_stat_value(stat_key) < int(needed or 0):
                return False
        return True

    def social_topic_entries(mode="talk", girl_name=""):
        mode_key = str(mode or "").strip().lower()
        key = social_topic_key(girl_name)
        base_rows = list(SOCIAL_FLIRT_TOPICS if mode_key == "flirt" else SOCIAL_TALK_TOPICS)
        if mode_key == "talk":
            return base_rows
        custom_rows = list(dict(SOCIAL_NPC_TOPIC_PACKS.get(key, {}) or {}).get(mode_key, []) or [])
        rows = list(custom_rows)
        rows.extend(base_rows)
        return rows

    def social_topic_label(mode="talk", topic_id="", girl_name=""):
        topic_key = str(topic_id or "").strip()
        for row in social_topic_entries(mode, girl_name):
            if str(row.get("id", "") or "") == topic_key:
                return str(row.get("label", "") or topic_key)
        return topic_key

    def social_flirt_topic_profile(girl_name=""):
        key = social_topic_key(girl_name)
        profile = dict(SOCIAL_DEFAULT_FLIRT_PROFILE)
        profile.update(dict(dict(SOCIAL_FLIRT_PROFILES.get(key, {}) or {}).get("flirt", {}) or {}))
        return profile

    def social_favorite_topic_ids(girl_name=""):
        info = people.get_info(girl_name)
        preferences = getattr(info, "talk_preferences", {}) if info is not None else {}
        return [str(row or "").strip() for row in list(dict(preferences or {}).get("favorite_topics", []) or []) if str(row or "").strip()]

    def social_topic_visible(girl_name="", mode="talk", topic_id=""):
        key = social_topic_key(girl_name)
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        if key == "":
            return False
        if key == "clara" and mode_key == "flirt":
            if not Clara.can_start_social_events():
                return False
        if mode_key == "talk" and social_talk_session_remaining(key) <= 0:
            return False
        if mode_key == "talk" and social_topic_already_seen(key, mode_key, topic_key):
            return False
        if mode_key == "talk":
            return any(str(row.get("id", "") or "") == topic_key for row in SOCIAL_TALK_TOPICS)
        if mode_key == "flirt" and social_flirted_today_value(key) > 0:
            return False
        if mode_key == "flirt" and not social_external_requirement_met(key, "flirt"):
            return False
        allowed, reason = relationship_social_action_allowed(key, mode_key)
        if not allowed:
            return False
        for row in social_topic_entries(mode_key, key):
            if str(row.get("id", "") or "") != topic_key:
                continue
            if social_rel_value(key) < int(row.get("min_friend", 0) or 0):
                return False
            if social_open_value(key) < int(row.get("min_open", 0) or 0):
                return False
            if mode_key == "flirt" and social_corruption_value(key) < int(row.get("min_slut", 0) or 0):
                return False
            return True
        return False

    def social_visible_topic_entries(girl_name="", mode="talk"):
        rows = []
        for row in social_topic_entries(mode, girl_name):
            if social_topic_visible(girl_name, mode, row.get("id", "")):
                rows.append(dict(row))
        return rows

    def social_has_visible_topics(girl_name="", mode="talk"):
        if str(mode or "talk").strip().lower() == "talk" and social_talked_today_value(girl_name) > 0:
            return False
        return len(social_visible_topic_entries(girl_name, mode)) > 0

    def social_topic_score(girl_name="", mode="talk", topic_id=""):
        key = social_topic_key(girl_name)
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        if mode_key == "talk":
            points = procedural_randint(1, 2, "social_talk_%s_%s_%s" % (key, topic_key, current_game_day()))
            return points if topic_key in social_favorite_topic_ids(key) else -points
        base = int(social_flirt_topic_profile(key).get(topic_key, 0) or 0)
        mood = 0
        if social_rel_value(key) >= 10:
            mood += 1
        if social_open_value(key) >= 8:
            mood += 1
        if mode_key == "flirt" and social_corruption_value(key) >= 15:
            mood += 1
        if social_drunk_value(key) > 0:
            mood += 1
        adjusted = relationship_adjust_social_score(key, mode_key, max(-5, min(5, base + mood)))
        try:
            adjusted = player_social_adjusted_delta(key, mode_key, adjusted)
        except Exception:
            pass
        return adjusted

    def social_topic_notify_result(girl_name="", mode="talk", topic_id="", topic_score=0, final_score=0, relation_delta=0):
        topic_name = social_topic_label(mode, topic_id, girl_name)
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
        if mode_key == "talk":
            kind = "good" if int(score or 0) > 0 else "bad"
        else:
            kind = social_topic_result_kind(score)
        text = str(dict(dict(SOCIAL_CUSTOM_TOPIC_TEXT.get(mode_key, {}) or {}).get(topic_key, {}) or {}).get(kind, "") or "")
        if not text:
            text = str(dict(dict(SOCIAL_TOPIC_TEXT.get(mode_key, {}) or {}).get(topic_key, {}) or {}).get(kind, "") or "")
        if not text:
            text = "Вы некоторое время говорите с {name}."
        return text.format(name=_action_display_name(girl_name))

    def social_apply_topic(girl_name="", mode="talk", topic_id=""):
        key = social_topic_key(girl_name)
        mode_key = str(mode or "talk").strip().lower()
        topic_key = str(topic_id or "").strip()
        if not social_topic_visible(key, mode_key, topic_key):
            allowed, reason = relationship_social_action_allowed(key, mode_key)
            return {"ok": False, "text": str(reason or "Сейчас этот разговор не складывается."), "score": 0}
        friends_before = social_rel_value(key)
        score = social_topic_score(key, mode_key, topic_key)
        topic_score = score if mode_key == "talk" else int(social_flirt_topic_profile(key).get(topic_key, 0) or 0)
        if mode_key == "flirt":
            apply_social_interaction_base(key, "flirt", score, 2 if score > 0 else 0, 30, 1, 1, 0, 0)
            if score > 0:
                info = social_person_info(key)
                if info is not None:
                    info.change_social(corruption_delta=max(1, score))
            elif score < 0:
                info = social_person_info(key)
                if info is not None:
                    info.change_social(open_delta=score)
        else:
            talk_already_today = social_talked_today_value(key) > 0
            talk_today_delta = 0 if talk_already_today else 1
            apply_social_interaction_base(key, "talk", score, 0, 5, 0, 0, 0, talk_today_delta)
        actual_score = social_score_delta_for(key, friends_before)
        social_topic_seen_state(key)[social_topic_seen_key(key, mode_key, topic_key)] = score
        relationship_after_social_result(key, mode_key, score, True)
        if mode_key == "talk":
            result_text = append_social_score_message(social_topic_text(key, mode_key, topic_key, score), actual_score, False)
        else:
            result_text = append_social_score_message(social_topic_text(key, mode_key, topic_key, score), actual_score, True)
            social_topic_notify_result(key, mode_key, topic_key, topic_score, score, actual_score)
            try:
                player_social_condition_notify(key)
            except Exception:
                pass
        return {"ok": True, "text": result_text, "score": actual_score, "raw_score": score}

    def social_gift_score(girl_name="", item_id="", base_gain=2):
        key = social_topic_key(girl_name)
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
        elif relationship_is_care_gift(item_key):
            score = max(1, min(4, base))
        else:
            score = 0
            if key in SOCIAL_FLIRT_PROFILES and social_rel_value(key) < 5:
                score = -2
        affinity = social_custom_gift_affinity(key, item_key)
        if affinity > 0:
            score = max(score, base + affinity)
        elif affinity < 0:
            score += affinity
        if social_rel_value(key) >= 10:
            score += 1
        if social_gifted_today_value(key) > 0:
            score -= 3
        return relationship_adjust_social_score(key, "gift", max(-5, min(5, score)))

    def social_gift_acceptance(girl_name="", item_id="", base_gain=2):
        key = social_topic_key(girl_name)
        item_key = str(item_id or "").strip()
        allowed, reason = relationship_social_action_allowed(key, "gift", item_key)
        if not allowed:
            return False, -3
        score = social_gift_score(key, item_key, base_gain)
        if relationship_is_care_gift(item_key):
            return True, score
        if key in SOCIAL_FLIRT_PROFILES and social_rel_value(key) < 3 and score <= 0:
            return False, score
        return True, score

    def social_gift_text(girl_name="", gift_name="", item_id="", score=0):
        key = social_topic_key(girl_name)
        gift = str(gift_name or "подарок").strip()
        item_key = str(item_id or "").strip()
        value = int(score or 0)
        name = _action_display_name(key)
        affinity = social_custom_gift_affinity(key, item_key)
        if affinity > 0 and value > 0:
            return "%s принимает %s с личным интересом. Видно, что этот подарок подходит именно ей, и разговор сразу становится теплее." % (name, gift)
        if affinity < 0 and value < 0:
            return "%s смотрит на %s без радости. Для нее это выглядит не как внимание, а как неверно выбранный жест." % (name, gift)
        if value >= 3:
            return "%s принимает %s с явным удовольствием. Похоже, вы угадали не только с вещью, но и с моментом." % (name, gift)
        if value > 0:
            return "%s принимает %s спокойно, но теплеет к вам: подарок оказался уместным." % (name, gift)
        if value == 0:
            return "%s принимает %s вежливо. Это не задевает ее, но и особенного впечатления не производит." % (name, gift)
        return "%s не хочет брать %s. Сейчас такой подарок кажется ей не заботой, а давлением." % (name, gift)

    def social_custom_gift_affinity(girl_name="", item_id=""):
        key = social_topic_key(girl_name)
        item_key = str(item_id or "").strip()
        row = dict(SOCIAL_CUSTOM_GIFT_AFFINITY.get(key, {}) or {})
        if item_key != "" and item_key in tuple(row.get("good", ()) or ()):
            return 2
        if item_key != "" and item_key in tuple(row.get("bad", ()) or ()):
            return -2
        return 0

    def social_interaction_allowed_for_npc(girl_name="", action="", item_id=""):
        key = social_topic_key(girl_name)
        action_key = str(action or "").strip().lower()
        item_key = str(item_id or "").strip()
        if key == "":
            return False
        info = people.get_info(key)
        if info is not None and hasattr(info, "social_action_allowed"):
            if not info.social_action_allowed(action_key, item_key):
                return False
        if key == "melissa" and action_key in ("flirt", "gift", "share"):
            if action_key in ("gift", "share") and social_flirted_today_value(key) <= 0:
                return False
            return bool(Melissa.relationship_allows(action_key))
        if key == "clara":
            if action_key == "flirt":
                return bool(Clara.can_start_social_events()) and social_external_requirement_met(key, "flirt")
            if action_key == "gift":
                if social_flirted_today_value(key) <= 0:
                    return False
                return bool((Clara.can_receive_gifts() or Clara.has_caught_cat_gift()) and Clara.has_giftable_entries())
            if action_key == "share":
                if social_flirted_today_value(key) <= 0:
                    return False
                allowed, reason = relationship_social_action_allowed(key, action_key, item_key)
                return bool(allowed)
        if action_key == "flirt" and not social_external_requirement_met(key, "flirt"):
            return False
        if action_key == "gift":
            if social_flirted_today_value(key) <= 0:
                return False
            return bool(relationship_any_gift_allowed(key))
        if action_key == "share" and social_flirted_today_value(key) <= 0:
            return False
        allowed, reason = relationship_social_action_allowed(key, action_key, item_key)
        return bool(allowed)

label SocialTalkTopicMenu(girl_name="", mode="talk", _social_girl="", _social_mode="", _social_parent_mode="", _social_visible_ids=None, _social_topic_id="", _social_result=None, _social_busy_text=""):
    $ _social_girl = social_topic_key(girl_name)
    $ _social_mode = str(mode or "talk").strip().lower()
    $ _social_parent_mode = str(main_ui_runtime.mode or "scene")
    if _social_parent_mode != "talk":
        $ main_ui_begin_talk_state("Разговор с %s" % _action_display_name(_social_girl), _social_girl)
    $ _social_busy_text = social_person_info(_social_girl).interrupt_work()
    if _social_busy_text:
        $ scene_runtime.text = _social_busy_text
        $ scene_runtime.location_text = scene_runtime.text
        if _social_parent_mode != "talk":
            "[_social_busy_text]"
            $ main_ui_end_talk_state()
        return
    if _social_mode == "talk" and social_talked_today_value(_social_girl) > 0:
        if _social_parent_mode != "talk":
            $ main_ui_end_talk_state()
        return
    if _social_mode == "talk":
        $ social_person_info(_social_girl).mark_talked()
    while True:
        $ _social_visible_ids = {str(row.get("id", "") or "") for row in social_visible_topic_entries(_social_girl, _social_mode)}
        if not _social_visible_ids:
            if _social_parent_mode != "talk":
                $ main_ui_end_talk_state()
            return
        $ _social_topic_id = ""
        menu:
            "О работе и распорядке" if _social_mode == "talk" and "job_routine" in _social_visible_ids:
                $ _social_topic_id = "job_routine"
            "Просто поболтать" if _social_mode == "talk" and "chat" in _social_visible_ids:
                $ _social_topic_id = "chat"
            "О танцах" if _social_mode == "talk" and "dances" in _social_visible_ids:
                $ _social_topic_id = "dances"
            "О слухах" if _social_mode == "talk" and "gossip" in _social_visible_ids:
                $ _social_topic_id = "gossip"
            "О лесе" if _social_mode == "talk" and "forest" in _social_visible_ids:
                $ _social_topic_id = "forest"
            "Послушать истории" if _social_mode == "talk" and "stories" in _social_visible_ids:
                $ _social_topic_id = "stories"
            "О еде" if _social_mode == "talk" and "food" in _social_visible_ids:
                $ _social_topic_id = "food"
            "Об одежде и внешности" if _social_mode == "talk" and "fashion" in _social_visible_ids:
                $ _social_topic_id = "fashion"
            "О деньгах" if _social_mode == "talk" and "money" in _social_visible_ids:
                $ _social_topic_id = "money"
            "О семье и доме" if _social_mode == "talk" and "family_life" in _social_visible_ids:
                $ _social_topic_id = "family_life"
            "Сказать игривую шутку" if _social_mode == "flirt" and "joke" in _social_visible_ids:
                $ _social_topic_id = "joke"
            "Мягко перейти к прикосновениям" if _social_mode == "flirt" and "kino" in _social_visible_ids:
                $ _social_topic_id = "kino"
            "Открыто заигрывать" if _social_mode == "flirt" and "flirt" in _social_visible_ids:
                $ _social_topic_id = "flirt"
            "Заговорить о близости" if _social_mode == "flirt" and "sex_topics" in _social_visible_ids:
                $ _social_topic_id = "sex_topics"
            "Мягко подразнить Аманду" if _social_mode == "flirt" and _social_girl == "amanda" and "amanda_tease" in _social_visible_ids:
                $ _social_topic_id = "amanda_tease"
            "Намекнуть на танцы и взгляды" if _social_mode == "flirt" and _social_girl == "amanda" and "amanda_dance_hint" in _social_visible_ids:
                $ _social_topic_id = "amanda_dance_hint"
            "Сблизиться без нажима" if _social_mode == "flirt" and _social_girl == "melissa" and "melissa_gentle" in _social_visible_ids:
                $ _social_topic_id = "melissa_gentle"
            "Намекнуть на укромное место" if _social_mode == "flirt" and _social_girl == "melissa" and "melissa_private_place" in _social_visible_ids:
                $ _social_topic_id = "melissa_private_place"
            "Сделать уважительный комплимент" if _social_mode == "flirt" and _social_girl == "sandra" and "sandra_respect" in _social_visible_ids:
                $ _social_topic_id = "sandra_respect"
            "Поблагодарить ее теплее обычного" if _social_mode == "flirt" and _social_girl == "sandra" and "sandra_warmth" in _social_visible_ids:
                $ _social_topic_id = "sandra_warmth"
            "Затеять светскую игру" if _social_mode == "flirt" and _social_girl == "clara" and "clara_clever_game" in _social_visible_ids:
                $ _social_topic_id = "clara_clever_game"
            "Говорить намеками" if _social_mode == "flirt" and _social_girl == "clara" and "clara_between_lines" in _social_visible_ids:
                $ _social_topic_id = "clara_between_lines"
            "Закончить разговор" if _social_mode == "talk":
                $ scene_runtime.text = "Вы заканчиваете разговор."
                $ scene_runtime.location_text = scene_runtime.text
                if _social_parent_mode != "talk":
                    $ main_ui_end_talk_state()
                return
            "Назад" if _social_mode != "talk":
                if _social_parent_mode != "talk":
                    $ main_ui_end_talk_state()
                return
        $ _social_result = social_apply_topic(_social_girl, _social_mode, _social_topic_id)
        $ scene_runtime.text = str(_social_result.get("text", "") or "")
        $ scene_runtime.location_text = scene_runtime.text
        $ update_stat_state()
        if _social_mode != "talk":
            if _social_parent_mode != "talk":
                $ main_ui_end_talk_state()
            return
        if social_talk_session_remaining(_social_girl) <= 0:
            if _social_parent_mode != "talk":
                $ main_ui_end_talk_state()
            return
