label IntClaraTalk(girl_name="clara"):
    $ renpy.dynamic("_clara_picture", "_clara_talk_new", "_clara_talk_picture", "_clara_flirted_before", "_clara_ride_location")
    $ _clara_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != str(girl_name or "clara").strip().lower()
    if _clara_talk_new and str(rooms.current_code or "") == "WineStore":
        $ _clara_talk_picture = str(Clara.wine_store_talk_picture() or "").strip()
        if _clara_talk_picture:
            vscene _clara_talk_picture
    $ main_ui_begin_talk_state("Разговор с Клариссой", girl_name)
    $ update_stat_state()
    if str(scene_runtime.text or "").strip() == "":
        $ scene_runtime.text = "Кларисса вопросительно смотрит на вас, ожидая, что вы скажете дальше."
        $ scene_runtime.location_text = scene_runtime.text
    menu:
            "Осмотреть":
                call ShowGirlCard(girl_name)

            "Поговорить" if social_interaction_allowed_for_npc(girl_name, "talk"):
                call SocialTalkTopicMenu(girl_name, "talk")

            "Флиртовать" if social_interaction_allowed_for_npc(girl_name, "flirt"):
                $ _clara_flirted_before = Clara.flirted_today
                if str(rooms.current_code or "") in ("ForestClearing", "ForestSpring", "ForestLake"):
                    $ _clara_picture = Clara.forest_picture(str(rooms.current_code or ""))
                    if str(_clara_picture or "").strip():
                        vscene _clara_picture
                elif str(rooms.current_code or "") == "WineStore":
                    $ _clara_picture = Clara.wine_store_flirt_picture()
                    if str(_clara_picture or "").strip():
                        vscene _clara_picture
                call SocialTalkTopicMenu(girl_name, "flirt")
                if Clara.flirted_today > _clara_flirted_before:
                    $ Clara.flirt_count = max(0, int(Clara.flirt_count or 0)) + 1

            "Подарить маленький подарок" if old_point_action_unlocked(girl_name, "gift") and Clara.has_giftable_entries():
                call IntClaraGiftMenu(girl_name)

            "Коснуться ее смелее" if old_point_action_unlocked(girl_name, "kino"):
                call OldPointKinoAttempt(girl_name)

            "Извиниться перед Клариссой" if old_point_apology_available(girl_name):
                call OldPointApology(girl_name)

            "Проследить за Клариссой по рынку" if str(rooms.current_code or "") == "MarketPlace" and int(player.stats.exploration or 0) >= 100 and int(Clara.asked_today or 0) == 0:
                $ Clara.mark_asked()
                $ Clara.mark_talked()
                $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
                $ scene_runtime.text = "Вы не навязываетесь Клариссе разговором, а просто держитесь чуть поодаль и смотрите, куда она направится дальше. Девушка делает круг по рыночным рядам, будто проверяя, нет ли за ней чужих глаз, а затем уверенно уходит к знакомому входу в винную лавку Легаре.\n\nПохоже, даже на рынке Кларисса все время держит в уме путь обратно в винную лавку семьи."
                $ scene_runtime.location_text = scene_runtime.text
                $ Clara.set_day_location_override("WineStore")
                $ main_ui_end_talk_state()
                return

            "Осторожно заговорить о ее вечерних делах" if story_event_available("WineStore", "clara_talk"):
                call checkTriggers("WineStore", "clara_talk", 0)

            "Поговорить с Клариссой о рисунках" if story_event_available("WineStore", "clara_paintings"):
                call checkTriggers("WineStore", "clara_paintings", 0)

            "Спросить Клариссу о семье" if int(Clara.asked_today or 0) == 0 and int(Clara.rel or 0) >= 6:
                $ Clara.mark_asked()
                $ Clara.mark_talked()
                $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
                $ Clara.change_social(friend_delta=1)
                $ scene_runtime.text = "Вы осторожно спрашиваете Клариссу о ее семье. Девушка сначала держится по-прежнему светски, но потом все же смягчается.\n\n\"У нас дома все устроено правильно и чинно, но иногда от этой правильности устаешь сильнее, чем от любой работы,\" признается она. — \"Отец много требует, мать следит за внешними приличиями, а мне все чаще хочется хоть иногда бывать там, где можно говорить свободнее.\""
                $ scene_runtime.location_text = scene_runtime.text

            "Спросить Клариссу о ней самой" if int(Clara.asked_today or 0) == 0 and int(Clara.rel or 0) >= 6:
                $ Clara.mark_asked()
                $ Clara.mark_talked()
                $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
                $ Clara.change_social(friend_delta=1)
                $ scene_runtime.text = "Вы просите Клариссу рассказать о себе самой, а не о том, что от нее ждут дома. Она коротко смеется и, поколебавшись, все же отвечает честнее обычного.\n\n\"Я люблю смотреть, как люди ведут дела и как один и тот же город меняется в зависимости от того, с кем ты говоришь. Наверное, мне нравится наблюдать и делать выводы. Просто дома не всякому понравится, если девушка слишком много замечает,\" говорит Кларисса."
                $ scene_runtime.location_text = scene_runtime.text

            "Спросить Клариссу об укромных местах" if int(Clara.asked_today or 0) == 0 and int(Clara.rel or 0) >= 6 and not bool(Clara.old_water_pump_hint_seen) and threads["melissaBatProblem"].num >= 5:
                $ Clara.mark_asked()
                $ Clara.mark_talked()
                $ Clara.old_water_pump_hint_seen = True
                $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
                $ Clara.change_social(friend_delta=1)
                $ scene_runtime.text = "Кларисса, чуть усмехнувшись, признает, что в городе есть места, куда люди ходят не за водой и не за прогулкой.\n\n\"У старой водокачки, за лесной тропой, часто встречаются те, кому не хочется лишних глаз,\" говорит она. — \"Если после того, что ты уже слышал с чердака, тебе все еще нужны доказательства, ищи не на главной дороге. Секреты любят обходные тропы.\""
                $ scene_runtime.location_text = scene_runtime.text

            "Осторожно заговорить о ее тайных рисунках" if int(Clara.asked_today or 0) == 0 and int(Clara.rel or 0) >= 6 and (bool(Clara.drawings_secret_known) or bool(Melissa.drawings_found)):
                $ Clara.mark_asked()
                $ Clara.mark_talked()
                $ Clara.trust = min(20, int(Clara.trust or 0) + 2)
                $ Clara.change_social(friend_delta=1)
                $ scene_runtime.text = "Вы осторожно даете Клариссе понять, что знаете о ее тайных непристойных рисунках и не собираетесь поднимать из-за этого шум. Она сперва цепенеет, но потом, поняв ваш тон, только шумно выдыхает.\n\n\"Дома за такое меня бы живьем съели,\" признается она. — \"Отец требует приличий, мать — судьбы по правилам, а мне иногда хочется хотя бы на бумаге жить не так, как велено. Потому я и наблюдаю за людьми, и слушаю лишнее. Иначе совсем задохнешься в чужих ожиданиях.\""
                $ scene_runtime.location_text = scene_runtime.text

            "Предложить подвезти Клариссу на коне" if Clara.can_accept_horse_ride(rooms.current_code):
                $ _clara_ride_location = str(rooms.current_code or "")
                if _clara_ride_location == "ForestLake" and int(Clara.rel or 0) < 8:
                    $ scene_runtime.text = "Вы предлагаете Клариссе место в седле, но девушка с улыбкой качает головой. «Спасибо, Стефан, но здесь у озера на удивление хорошо. Я еще немного побуду здесь, а потом вернусь сама», - отвечает она."
                else:
                    $ Clara.change_social(friend_delta=1)
                    $ Clara.trust = min(20, int(Clara.trust or 0) + 1)
                    $ Clara.set_day_location_override("MarketPlace")
                    if _clara_ride_location == "ForestLake":
                        $ scene_runtime.text = "Вы предлагаете Клариссе место в седле. Она сначала говорит, что у озера ей очень нравится, но потом все же принимает ваше предложение. По дороге обратно в город девушка заметно расслабляется и благодарит вас за поездку."
                    else:
                        $ scene_runtime.text = "Вы предлагаете Клариссе место в седле и подвозите ее обратно к городу. Девушка сначала смеется над неожиданной затеей, а потом явно начинает смотреть на вас теплее."
                $ scene_runtime.location_text = scene_runtime.text
                $ main_ui_end_talk_state()
                return

            "Назад":
                $ main_ui_end_talk_state()
                return
    return


label IntClaraGiftMenu(girl_name="clara"):
    $ renpy.dynamic("_clara_gift_ids")
    $ scene_runtime.text = "Вы прикидываете, что из имеющегося при себе может понравиться Клариссе."
    $ scene_runtime.location_text = scene_runtime.text
    $ _clara_gift_ids = [str(row.get("gift_id", "") or "") for row in Clara.giftable_entries()]
    menu:
        "Кусок мыла" if "soap_001" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "soap_001")
        "Особый гриб" if "special_mushroom_001" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "special_mushroom_001")
        "Лаванда" if "lavender_001" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "lavender_001")
        "Роскошное мыло" if "luxury_soap_001" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "luxury_soap_001")
        "Пряная настойка" if "libido_tincture_001" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "libido_tincture_001")
        "Воровское платье" if "dress_thiefdress" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "dress_thiefdress")
        "Простой лиф" if "dress_simplebra" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "dress_simplebra")
        "Простые панталоны" if "dress_simplepanties" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "dress_simplepanties")
        "Черные чулки" if "dress_blackstockings" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "dress_blackstockings")
        "Красные чулки" if "dress_redstockings" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "dress_redstockings")
        "Пойманная лесная кошка" if "werecat_caught_cat" in _clara_gift_ids:
            call ClaraGiveGift(girl_name, "werecat_caught_cat")
        "Назад":
            return
    return


label ClaraGiveGift(girl_name="clara", gift_id=""):
    $ renpy.dynamic("_selected", "_gift_name", "_gift_id", "_gift_base", "_friends_before", "_accepts", "_gift_score", "_gift_result", "_effect", "row")
    python:
        _selected = next((dict(row) for row in Clara.giftable_entries() if str(row.get("gift_id", "") or "") == str(gift_id or "")), None)
        if _selected is None:
            scene_runtime.text = "Подарок уже недоступен."
        else:
            _gift_name = str(_selected.get("gift_name", "") or "подарок")
            _gift_id = str(_selected.get("gift_id", "") or "")
            _gift_base = 3 if _gift_id in tuple(preferred_gift_item_ids("clara") or ()) else 1
            _friends_before = int(Clara.rel or 0)
            _accepts, _gift_score = social_gift_acceptance("clara", _gift_id, _gift_base)
            if not _accepts:
                _gift_result = player_gift_to("clara", _gift_name, _gift_base, _gift_id, False)
                scene_runtime.text = append_social_score_message(str(_gift_result.get("text", "") or ""), social_score_delta_for("clara", _friends_before))
            elif not Clara.remove_gift_entry(_selected):
                scene_runtime.text = "Подарок уже недоступен."
            else:
                apply_social_interaction_base("clara", "gift", _gift_score, 0, 0, 1, 0, 1, 0)
                Clara.trust = max(0, min(20, int(Clara.trust or 0) + (max(1, _gift_score // 2) if _gift_score > 0 else _gift_score)))
                _effect = player_apply_item_social_effects("clara", _gift_id, True) if str(_selected.get("source", "") or "") == "item" else {"text": ""}
                scene_runtime.text = "Кларисса принимает пойманную лесную кошку не как безделушку, а как редкий и опасный знак доверия." if _gift_id == "werecat_caught_cat" else social_gift_text("clara", _gift_name, _gift_id, _gift_score)
                if str(_effect.get("text", "") or "").strip():
                    scene_runtime.text = str(scene_runtime.text or "") + " " + str(_effect.get("text", "") or "").strip()
                scene_runtime.text = append_social_score_message(scene_runtime.text, social_score_delta_for("clara", _friends_before))
        scene_runtime.location_text = scene_runtime.text
    return
