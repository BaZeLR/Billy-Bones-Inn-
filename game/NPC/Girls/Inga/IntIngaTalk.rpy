# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntIngaTalk(show_menu=True):
    if not bool(show_menu):
        if str(rooms.current_code or "") == "GroceryStore":
            vscene "images/inga/newInga/inga_store_openworkdress.png"
        call GirlsDesc("inga")
        return

    $ Inga.mark_known()
    $ main_ui_begin_talk_state("Разговор с Ингенборг", "inga")
    if str(rooms.current_code or "") == "GroceryStore":
        $ scene_runtime.picture = "images/inga/newInga/inga_store_closeup_unlaced_breakfast.png"
        vscene scene_runtime.picture
        $ scene_runtime.text = "«Привет, милая, — игриво говорите вы. — Вижу, ты уже успела позавтракать своим любимым завтраком»."
        $ scene_runtime.location_text = scene_runtime.text
        menu:
            "Продолжить":
                pass
        $ scene_runtime.text = "«Да, милый, я и правда им позавтракала!» — отвечает Инга с довольной улыбкой. От этого зрелища ваш член заметно твердеет."
        $ scene_runtime.location_text = scene_runtime.text
        $ player_apply_arousal_trigger("inga_breakfast_closeup", max(0, 40 - int(player.intimacy.arousal_value() or 0)))
        menu:
            "Продолжить разговор":
                pass
        $ scene_runtime.picture = "images/inga/newInga/inga_store_closeup_unlaced_clean.png"
        vscene scene_runtime.picture
        $ scene_runtime.text = "Инга проводит по губам платком и снова смотрит на вас с невинной улыбкой."
        $ scene_runtime.location_text = scene_runtime.text
    while True:
        menu:
            "Осмотреть":
                call GirlsDesc("inga")
                if str(rooms.current_code or "") == "GroceryStore":
                    $ scene_runtime.picture = "images/inga/newInga/inga_store_closeup_unlaced_clean.png"
                    vscene scene_runtime.picture
            "Подарить маленький подарок" if social_interaction_allowed_for_npc("inga", "gift"):
                call PlayerCardGiftToFixedTargetMenu("inga")
                if str(rooms.current_code or "") == "GroceryStore":
                    $ scene_runtime.picture = "images/inga/newInga/inga_store_closeup_unlaced_clean.png"
                    vscene scene_runtime.picture
            "Попросить Ингу позаботиться и о вас" if str(rooms.current_code or "") == "GroceryStore" and npc_friend_level("inga") >= 2 and player.intimacy.can_cum() and Inga.can_have_sex_today():
                $ scene_runtime.picture = "images/inga/newInga/inga_store_openworkdress.png"
                vscene scene_runtime.picture
                $ scene_runtime.text = "Инга окидывает вас понимающим взглядом, выходит из-за прилавка и опускается перед вами на колени. Ее теплые губы мягко обхватывают ваш член, а язык начинает неспешную игру."
                $ scene_runtime.location_text = scene_runtime.text
                $ Inga.set_cock_position("mouth")
                menu:
                    "Продолжить":
                        pass
                $ scene_runtime.text = "Инга нежно сосет вас, постепенно ускоряясь, и не останавливается, пока не высасывает все до последней капли."
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Кончить":
                        $ Inga.player_cum("mouth")
                        $ Inga.set_sex_busy(False)
                        $ Inga.change_social(friend_delta=1, open_delta=1)
                $ scene_runtime.picture = "images/inga/newInga/inga_store_closeup_unlaced_breakfast.png"
                vscene scene_runtime.picture
                $ scene_runtime.text = "«Бедный-бедный хозяин трактира, — поддразнивает Инга. — Разве твои девочки не должны о тебе заботиться?»"
                $ scene_runtime.location_text = scene_runtime.text
                menu:
                    "Вернуться к разговору":
                        pass
                $ scene_runtime.picture = "images/inga/newInga/inga_store_closeup_unlaced_clean.png"
                vscene scene_runtime.picture
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return
