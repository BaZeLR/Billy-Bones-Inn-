# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntMelissaTalk(girl_name="melissa"):
    $ renpy.dynamic("_melissa_talk_new", "_melissa_special_entry", "_melissa_repeat_menu")
    $ _melissa_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != str(girl_name or "melissa").strip().lower()
    $ main_ui_begin_talk_state("Разговор с Мелиссой", girl_name)
    $ main_ui_runtime.action_title = "Разговор с Мелиссой"
    $ main_ui_runtime.action_content = None
    if _melissa_talk_new:
        $ scene_runtime.text = "Мелисса вопросительно смотрит на вас, ожидая продолжения разговора."
        $ scene_runtime.location_text = scene_runtime.text
    if story_event_available(str(rooms.current_code or ""), "melissa_talk"):
        call checkTriggers(rooms.current_code, "melissa_talk", 0)
    $ _melissa_special_entry = household_special_talk_entry(girl_name) if int(Melissa.asked_today or 0) == 0 and household_special_talk_available(girl_name) else None
    $ _melissa_repeat_menu = True
    while _melissa_repeat_menu:
        $ _melissa_repeat_menu = False
        menu:
            "Осмотреть":
                call ShowGirlCard(girl_name)
            "Поговорить" if social_has_visible_topics(girl_name, "talk"):
                call SocialTalkTopicMenu(girl_name, "talk")
                $ _melissa_repeat_menu = True
            "Флиртовать" if social_interaction_allowed_for_npc(girl_name, "flirt"):
                call SocialTalkTopicMenu(girl_name, "flirt")
                $ _melissa_repeat_menu = True
            "Подарить маленький подарок" if social_interaction_allowed_for_npc(girl_name, "gift"):
                call PlayerCardGiftToFixedTargetMenu(girl_name)
                $ _melissa_repeat_menu = True
            "Послушать, что Мелисса скажет о кладовой" if melissa_storage_thanks_available():
                $ Melissa.storage_thanks_day = int(current_game_day() or 0)
                $ Melissa.change_social(friend_delta=1)
                $ scene_runtime.text = "Мелисса сама возвращается к теме кладовой и уже без колкости благодарит вас за помощь. \"Когда знаешь, что с этой дрянью внизу не придется возиться одной, работать куда легче,\" говорит она. Потом, помедлив, добавляет, что если крысы опять полезут к мешкам, она скорее позовет вас сразу, чем будет молча злиться."
                $ scene_runtime.location_text = scene_runtime.text
            "Спросить Мелиссу о найденных рисунках" if story_event_available("talk_melissa", "clara_paintings"):
                call checkTriggers("talk_melissa", "clara_paintings", 0)
            "Попросить Мелиссу прийти завтра на общий завтрак" if story_event_available("talk_melissa", "melissa_breakfast_invite"):
                call checkTriggers("talk_melissa", "melissa_breakfast_invite", 0)
                $ _melissa_repeat_menu = True
            "Обсудить, где Мелиссе переночевать" if melissa_room_problem_available():
                call IntMelissaRoomProblemAdviceMenu(girl_name)
            "Сблизиться с Мелиссой" if story_event_available("talk_melissa", "melissa_intimacy"):
                $ main_ui_end_talk_state()
                call checkTriggers("talk_melissa", "melissa_intimacy", 0)
                return
            "Попросить Мелиссу о сексуальном одолжении" if not Melissa.is_working() and Melissa.relationship_allows("intimacy") and Melissa.room_is_private(rooms.current_code):
                $ main_ui_end_talk_state()
                call HouseholdSexEngine(girl_name, rooms.current_code)
                return
            "Попросить Мелиссу найти укромное место" if not Melissa.is_working() and Melissa.relationship_allows("intimacy") and not Melissa.room_is_private(rooms.current_code) and bool(Melissa.private_place_offer(rooms.current_code).get("ok", False)):
                $ main_ui_end_talk_state()
                call IntMelissaFindPrivatePlace(girl_name, rooms.current_code)
                return
            "Спросить Мелиссу о Клариссе" if str(rooms.current_code or "") == "TavernMain" and str(people.location("clara") or "") == "TavernMain" and people_to_int(Melissa.asked_about_clara_day, -1) != int(current_game_day() or 0) and int(Melissa.asked_today or 0) == 0:
                $ Melissa.mark_asked()
                $ Melissa.asked_about_clara_day = int(current_game_day() or 0)
                $ Melissa.change_social(friend_delta=1)
                $ scene_runtime.text = "Вы осторожно расспрашиваете Мелиссу о Клариссе. Мелисса с улыбкой признается, что Кларисса любит заглядывать к вам не только ради болтовни, а еще потому, что у вас в трактире ей заметно свободнее дышится. «Она хорошая, просто привыкла скрывать это за светскими манерами», - тихо добавляет Мелисса."
                $ scene_runtime.location_text = scene_runtime.text
            "[_melissa_special_entry.get('label', 'Спросить о чем-то важном')]" if _melissa_special_entry is not None:
                $ Melissa.mark_asked()
                $ Melissa.mark_talked()
                $ Melissa.change_social(friend_delta=1, open_delta=1)
                $ household_advance_special_talk(girl_name)
                $ scene_runtime.text = str(_melissa_special_entry.get("text", "") or "")
                $ scene_runtime.location_text = scene_runtime.text
            "Попробовать помириться с Мелиссой" if int(Melissa.talked_today or 0) < 3 and int(Melissa.rel or 0) < 5:
                $ scene_runtime.text = "Вы подошли к своей сестренке и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и вы все должны дружно работать вместе, чтобы преуспеть."
                if procedural_randint(1, 3, key="procedural:NPC/Girls/Melissa/IntMelissaTalk.rpy:reconcile") == 1:
                    $ scene_runtime.text += "\n\nМелисса благосклонно выслушала вас, обняла, поцеловала в щечку и сказала, что вы для нее всегда будете любимым братом и она все понимает!"
                    call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
                else:
                    $ scene_runtime.text += "\n\nМелисса холодно выслушала вас, презрительно отвернулась и пошла прочь."
                $ Melissa.mark_talked()
                $ scene_runtime.location_text = scene_runtime.text
            "Предложить купить сестренке обновку" if int(Melissa.rel or 0) > 8 and daily_events.exists("", "BuyDressTom") == 0 and daily_events.exists(girl_name, "BuyDress") == 0 and int(Melissa.talked_today or 0) < 2 and int(calendar_v2.week or 0) != 6:
                call IntMelissaDressChange(girl_name)
            "Спросить, что для нее сейчас важнее всего" if int(Melissa.asked_today or 0) == 0 and int(Melissa.rel or 0) >= 15:
                $ Melissa.mark_asked()
                $ Melissa.mark_talked()
                $ Melissa.change_social(friend_delta=1, open_delta=1)
                $ scene_runtime.text = "Вы спрашиваете Мелиссу, что для нее сейчас важнее всего. Она на миг задумывается, потом отвечает спокойно и неожиданно открыто.\n\n\"Чтобы в доме было тише и ровнее. Чтобы можно было работать без постоянной ругани и чтобы меня не дергали по пустякам. Но еще мне важно знать, что меня здесь слушают, а не просто считают одной из рабочих рук,\" говорит Мелисса, поднимая на вас внимательный взгляд."
                $ scene_runtime.location_text = scene_runtime.text
            "Назад":
                $ main_ui_end_talk_state()
                return
    return


label IntMelissaFindPrivatePlace(girl_name="melissa", source_room=""):
    $ renpy.dynamic("_melissa_private_offer")
    $ _melissa_private_offer = Melissa.private_place_offer(source_room)
    if not bool(_melissa_private_offer.get("ok", False)):
        $ scene_runtime.text = "Здесь слишком открыто, а Мелисса сейчас не готова сама искать место, где вас не увидят."
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ Melissa.private_context_day = int(current_game_day() or 0)
    $ Melissa.private_context_origin = str(source_room or rooms.current_code or "")
    $ scene_runtime.text = str(_melissa_private_offer.get("text", "") or "Мелисса сама находит место в стороне, где вы можете остаться без чужих взглядов.")
    $ scene_runtime.location_text = scene_runtime.text
    call HouseholdSexEngine(girl_name, source_room)
    return


label IntMelissaRoomProblemAdviceMenu(girl_name="melissa"):
    $ Melissa.change_social(friend_delta=1)
    $ main_ui_runtime.action_title = "Комната Мелиссы"
    $ main_ui_runtime.action_content = None
    $ scene_runtime.text = "После осмотра комнаты все выглядит куда хуже, чем Мелиссе хотелось бы признавать вслух. Под самым потолком видны щели, доски местами подгнили, а из-за перекосившейся обшивки тянет сыростью прямо сверху.\n\n\"Вот видишь? Я же не выдумывала,\" тихо говорит Мелисса. Теперь вопрос уже не в том, есть ли там дрянь под крышей, а в том, где ей ночевать, пока вы не доберетесь до чердака и не разберетесь с этим как следует."
    $ scene_runtime.location_text = scene_runtime.text
    menu:
        "Предложить пока ночевать у вас":
            $ Melissa.temp_room_code = "TavernMyRoom"
            $ Melissa.change_social(corruption_delta=1)
            $ scene_runtime.text = "На предложение перебраться пока к вам Мелисса сперва вспыхивает до самых ушей, но отказываться не спешит. \"Это... может и лучше, чем слушать эту дрянь под крышей. Только временно, пока ты не разберешься с комнатой. И без глупостей,\" добавляет она уже тише.\n\nВы подтверждаете, что сначала проверите ее комнату, потом чердак, и не оставите это на словах."
        "Предложить перебраться к Аманде":
            $ Melissa.temp_room_code = "TavernAmandaRoom"
            $ scene_runtime.text = "На предложение уйти к Аманде Мелисса кривится почти сразу. \"Она храпит, как пьяный матрос, и пинается во сне не хуже жеребца,\" бурчит она. Но после короткой паузы все же соглашается, что это лучше, чем снова лежать под шорохом и писком.\n\nВы обещаете, что это только временная мера, пока не выясните, что именно творится под крышей."
        "Предложить занять пустую комнату":
            $ Melissa.temp_room_code = "TavernEmptyRoom"
            $ scene_runtime.text = "Пустая комната Мелиссе совсем не по душе. \"Там холодно, сыро и так уныло, будто сразу в камеру посадили,\" признается она. Но если других вариантов не останется, она готова переждать там несколько ночей.\n\nВы говорите, что это лишь временно, а сами собираетесь осмотреть ее комнату и разобраться с чердаком."
        "Назад":
            $ main_ui_runtime.action_title = "Разговор с Мелиссой"
            return
    $ Melissa.change_social(friend_delta=1)
    $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВы желаете Мелиссе спокойной ночи и решаете, что утром пора наконец проверить чердак над ее комнатой."
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Разговор с Мелиссой"
    return
