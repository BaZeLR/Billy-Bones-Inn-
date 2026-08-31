# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntAmandaTalk(girl_name="amanda"):
    $ renpy.dynamic("_legare_text", "_can_dress_change", "_dad_phrase", "_amanda_special_entry", "_amanda_repeat_menu")
    $ main_ui_begin_talk_state("Разговор с Амандой", girl_name)
    $ main_ui_runtime.action_title = "Разговор с Амандой"
    $ main_ui_runtime.action_content = None
    if str(scene_runtime.text or "").strip() == "":
        $ scene_runtime.text = "Аманда смотрит на вас с привычным любопытством, ожидая продолжения разговора."
        $ scene_runtime.location_text = scene_runtime.text
    $ _legare_text = "Запретить ей %s с месье Легаре" % ("гулять" if Amanda.sex_stat("virginity", True) else "трахаться")
    $ _can_dress_change = Amanda.dress_change_has_options()
    $ _dad_phrase = DaddyAskBuildPhrase(girl_name) if int(Amanda.asked_today or 0) == 0 and int(Amanda.talked_today or 0) < 3 and int(Amanda.rel or 0) >= 8 and Amanda.pregnancy_days() >= 120 else ""
    $ _amanda_special_entry = household_special_talk_entry(girl_name) if int(Amanda.asked_today or 0) == 0 and household_special_talk_available(girl_name) else None
    $ _amanda_repeat_menu = True
    while _amanda_repeat_menu:
        $ _amanda_repeat_menu = False
        menu:
            "Осмотреть":
                call ShowGirlCard(girl_name)
            "Поговорить" if social_has_visible_topics(girl_name, "talk"):
                call SocialTalkTopicMenu(girl_name, "talk")
                $ _amanda_repeat_menu = True
            "Флиртовать" if old_point_action_unlocked(girl_name, "flirt"):
                call OldPointFlirtAttempt(girl_name)
            "Подарить маленький подарок" if old_point_action_unlocked(girl_name, "gift"):
                call PlayerCardGiftToFixedTargetMenu(girl_name)
            "Коснуться ее смелее" if old_point_action_unlocked(girl_name, "kino"):
                call OldPointKinoAttempt(girl_name)
            "Попросить Аманду о сексуальном одолжении" if Amanda.can_grant_sexual_favor():
                $ main_ui_end_talk_state()
                $ scene_runtime.text = "Вы тихо просите Аманду помочь вам без лишних свидетелей. Она оценивает ваш тон, отношения между вами и, наконец, с озорной улыбкой ведет вас в укромный угол трактира."
                $ scene_runtime.location_text = scene_runtime.text
                call IntAmandaSex(girl_name, "kitchen", "minet")
                return
            "Извиниться перед Амандой" if old_point_apology_available(girl_name):
                call OldPointApology(girl_name)
            "Сказать Аманде что вы передумали и она может встречаться с Альбером" if int(Amanda.talked_today or 0) < 3 and Amanda.legare_forbidden:
                call IntAmandaAllowAlber(girl_name)
            "Разрешить Аманде болтать с Лизеттой" if int(Amanda.talked_today or 0) < 3 and Amanda.var_int("prohibitliza", 0) > 0:
                call IntAmandaAllowLiza(girl_name)
            "Сказать Аманде что она может ходить к Лизетте в глорихолл" if int(Amanda.talked_today or 0) < 3 and Amanda.var_int("gloryscold", 0) > 0:
                call IntAmandaAllowGlory(girl_name)
            "Сказать Аманде что она может встречаться с парнями" if int(Amanda.talked_today or 0) < 3 and Amanda.var_int("prohibitwithguys", 0) > 0:
                call IntAmandaAllowGuys(girl_name)
            "Сказать Аманде что она может иногда брать перерывы" if int(Amanda.talked_today or 0) < 3 and Amanda.warned_about_not_working:
                call IntAmandaAllowBreaks(girl_name)
            "Спросить где она потеряла девственность" if int(Amanda.asked_today or 0) == 0 and int(Amanda.talked_today or 0) < 3 and Amanda.var_int("knownotvirgin", 0) > 0 and not Amanda.player_knows_legare_deflowered and Amanda.lost_virginity_to_legare:
                call IntAmandaAskVirginity(girl_name)
            "[_legare_text]" if int(Amanda.talked_today or 0) < 3 and Amanda.player_knows_legare_sex and not Amanda.legare_forbidden:
                call IntAmandaBanAlber(girl_name)
            "Запретить ей трахаться с соседскими парнями" if int(Amanda.talked_today or 0) < 3 and Amanda.var_int("sawwithguys", 0) > 0 and Amanda.var_int("prohibitwithguys", 0) == 0:
                call IntAmandaBanGuys(girl_name)
            "Спросить не боиться ли она залететь" if int(Amanda.asked_today or 0) == 0 and int(Amanda.talked_today or 0) < 3 and Amanda.var_int("knowsexactive", 0) > 0 and Amanda.pregnancy_days() < 120 and not Amanda.pregnancy_risk_asked_today and not Amanda.sex_stat("virginity", True):
                call IntAmandaAskPregnancy(girl_name)
            "Спросить, знает ли она от кого пузо нагуляла" if str(_dad_phrase or "") != "":
                call IntAmandaAskDad(girl_name)
            "Попросить у Аманды ее ночную миску" if int(Amanda.asked_today or 0) == 0 and int(Amanda.talked_today or 0) < 3 and Amanda.can_be_asked_for_night_bowl():
                call IntAmandaAskNightBowl(girl_name)
            "Подарить Аманде красивую ночную миску" if Amanda.can_receive_fancy_night_bowl():
                call IntAmandaGiftFancyNightBowl(girl_name)
            "[_amanda_special_entry.get('label', 'Спросить о чем-то важном')]" if _amanda_special_entry is not None:
                call IntAmandaHouseholdInsight(girl_name)
            "Спросить, чего ей сейчас хочется больше всего" if int(Amanda.asked_today or 0) == 0 and int(Amanda.rel or 0) >= 15:
                call IntAmandaHouseholdPriorities(girl_name)
            "Переодеть Аманду" if _can_dress_change:
                call int_amanda_dress_change(girl_name)
            "Назад":
                $ main_ui_end_talk_state()
                return
    return


label IntAmandaReconcile(girl_name="amanda"):
    $ scene_runtime.text = "Вы подошли к Аманде и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
    if procedural_randint(1, 3, key="procedural:NPC/Girls/Amanda/IntAmandaTalk.rpy:procedural_randint:97:1") == 1:
        $ scene_runtime.text += "\n\nАманда благосклонно выслушала вас, трогательно обняла и сказала, что очень к вам привязана!"
        $ Amanda.rel = max(5, min(20, int(Amanda.rel or 0) + 1))
        $ Amanda.openness = min(100, int(Amanda.openness or 0) + 1)
        $ Amanda.anger_with_player = max(0, int(Amanda.anger_with_player or 0) - 3)
        $ Amanda.mood = "softened"
    else:
        $ scene_runtime.text += "\n\nАманда холодно выслушала вас, фыркнула и пошла прочь."
        $ Amanda.anger_with_player = min(100, int(Amanda.anger_with_player or 0) + 1)
        $ Amanda.mood = "cold"
    $ Amanda.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    $ main_ui_runtime.action_title = "Разговор с Амандой"
    $ main_ui_runtime.action_content = None
    return


label IntAmandaAllowAlber(girl_name="amanda"):
    $ scene_runtime.text = "Вы подошли к Аманде и сказали, что, успокоившись и подумав, вы поменяли свое мнение и теперь не имеете ничего против того, чтобы она встречалась с Альбером Легаре."
    if Amanda.legare_affection >= 9:
        $ scene_runtime.text += "\n\nАманда взвизгнула от радости, обняла вас и поцеловала, сказав что она вас очень любит."
        $ Amanda.apply_social_chance(10, 1, 2, 20, 1, 1, "talk_allow_alber")
    else:
        $ scene_runtime.text += "\n\nАманда поблагодарила вас за доверие."
        $ Amanda.apply_social_chance(10, 1, 1, 20, 1, 1, "talk_allow_alber")
    $ Alber.add_relation(2)
    if int(calendar_v2.week or 0) == 5 and int(calendar_v2.time_slot() or 0) < 3:
        call AmandaLegareDanceSequence
    $ Amanda.mark_talked()
    $ Amanda.legare_forbidden = False
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAllowLiza(girl_name="amanda"):
    $ scene_runtime.text = "Вы подошли к Аманде и сказали ей, что передумали. Конечно, ей нужна подруга, а так как в пределах досягаемости есть лишь Лизетта, то так тому и быть. Вы только надеетесь, что она будет использовать ум, фильтровать ее слова и не принимать все за чистую монету.\n\nАманда чмокнула вас в щечку и сказала, что всегда верила в ваш разум."
    $ Amanda.apply_social_chance(10, 1, 1, 20, 1, 1, "talk_allow_liza")
    $ Amanda.mark_talked()
    $ Amanda.set_var_int("prohibitliza", 0)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAllowGlory(girl_name="amanda"):
    $ scene_runtime.text = "Вы подошли к Аманде и, собрав волю в кулак, сказали, что все не так страшно. Она уже взрослая, опыт ей пригодится, и лучше, чтобы этот опыт она получила в более-менее безопасной обстановке. Каковой вы считаете глорихол.\n\nА что? Ширмочка есть, анонимность гарантируется, и вы не собираетесь устраивать из этого трагедию.\n\nАманда чмокнула вас в щечку и сказала, что всегда верила в ваш разум."
    $ Amanda.apply_social_chance(10, 1, 1, 20, 1, 1, "talk_allow_glory")
    $ Amanda.mark_talked()
    $ Amanda.set_var_int("gloryscold", 0)
    $ Amanda.set_var_int("glorywalkout", 0)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAllowGuys(girl_name="amanda"):
    $ scene_runtime.text = "Вы подошли к Аманде и спокойно сказали ей, что обдумали ситуацию и поменяли свое мнение. Конечно, ей надо встречаться со сверстниками, и конечно парни такого возраста только и думают что о потрахушках. Ничего в этом неестественного нет. Так что если она хочет крутить роман где-то на стороне, вы не против.\n\nАманда поцеловала вас в губы, провела рукой по вашей ширинке и, довольная, убежала."
    $ Amanda.apply_social_chance(15, 1, 1, 42, 1, 1, "talk_allow_guys")
    $ Amanda.mark_talked()
    $ Amanda.set_var_int("prohibitwithguys", 0)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAllowBreaks(girl_name="amanda"):
    $ scene_runtime.text = "Вы подошли к Аманде и сказали ей, что погорячились. Конечно, вы не хотите, чтобы она сидела безвылазно в трактире с утра до ночи. Если хочет отдохнуть, прогуляться - то пожалуйста. Даже свежим воздухом подышать может, ну если, конечно, ветер не от смолокурен с верфей дует.\n\nАманда обрадовалась и убежала."
    $ Amanda.apply_social_chance(12, 1, 1, 0, 0, 0, "talk_allow_breaks")
    if procedural_randint(1, 5, key="procedural:NPC/Girls/Amanda/IntAmandaTalk.rpy:procedural_randint:175:2") == 1:
        $ Amanda.change_skill("cooking", 2)
        $ Amanda.change_skill("cleaning", 2)
        $ Amanda.change_skill("waitress", 2)
    $ Amanda.mark_talked()
    $ Amanda.warned_about_not_working = False
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAskVirginity(girl_name="amanda"):
    $ Amanda.mark_asked()
    $ scene_runtime.text = "\"Амандочка!\" как можно ласковей подкатились вы к Аманде. \"Я знаю, что ты уже не девочка. А может ты раскажешь мне, с кем это ты так умудрилась?\""
    if int(Amanda.rel or 0) > 11 and not Amanda.legare_forbidden:
        $ scene_runtime.text += "\n\n\"Ну, чего же не рассказать? С Альберчиком мой первый раз был. Мы с ним танцевали-плясали, а потом к нему пошли, на задний двор. Там все и случилось.\"\n\"Как с Альбером!\" Потрясенно сказали вы. Он же наверное втрое тебя старше, и семья у него!\"\n\"Ну и что? Жена у него давалка, вот и он развлекается как может. Вдруг мне удасться его в себя влюбить, выйду я за него, буду не у тебя тут в трактире болтаться, а уважаемой женой уважаемого торговца!\"\n\"Да ты сама в это веришь?\"\n\"Ну конечно, что же здесь невероятного?\"\nВы не нашлись с ответом."
        $ Amanda.apply_social_chance(12, 1, 1, 0, 0, 0, "talk_ask_virginity")
        $ Amanda.player_knows_legare_deflowered = True
        $ Amanda.player_knows_legare_sex = True
    else:
        $ scene_runtime.text += "\n\n\"Знаешь что, это мое дело, моя личная жизнь и ты в нее не лезь,\" отозвалась Аманда. Вы попробовали от нее добиться ответа еще пару раз, но все было бесполезно."
    $ Amanda.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaBanAlber(girl_name="amanda"):
    if Amanda.player_saw_legare_sex:
        $ scene_runtime.text = "\"Знаешь что, Аманда! Я видел, как ты трахалась с этим старым козлом, этим месье Легаре, и мне это не понравилось!\""
    else:
        $ scene_runtime.text = "\"Аманда! Я знаю, что ты даешь этому похотливому козлу, этому, как его, месье Легаре. Это мне совсем не по нраву!\""
    $ scene_runtime.text += "\n\nогорошили вы Аманду. И, не давая ей опомнится, вы продолжили: \"Ты вообще думала, когда с ним путалась? Он старше тебе даже не вдвое, а наверное втрое и женат! Так вот, я не желаю чтобы это повторялось, понятно!\"\nАманда попыталась было вам что-то возразить, но вы и слушать не стали ее лепет, лишь повторили: \"Понятно?!\" и, не дожидаясь ответа ушли. "
    $ Amanda.apply_social_chance(4, 1, -2, 0, 0, 0, "talk_ban_alber")
    $ Amanda.mark_talked()
    $ Amanda.legare_forbidden = True
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaBanGuys(girl_name="amanda"):
    $ scene_runtime.text = "\"Знаешь что, подруга,\" подступили вы к Аманде. \"Ты себе репутацию подстилки устраиваешь, и мне это не нравится. Чтобы с этого момента никаких потрахушек по амбарам и дворикам, понятно?\"\nАманда попыталась было вам что-то возразить, но вы и слушать не стали ее лепет, лишь повторили: \"Понятно?!\" и, не дожидаясь ответа, ушли."
    $ Amanda.apply_social_chance(4, 1, -2, 35, 1, -2, "talk_ban_guys")
    $ Amanda.mark_talked()
    $ Amanda.set_var_int("prohibitwithguys", 1)
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAskPregnancy(girl_name="amanda"):
    $ Amanda.mark_asked()
    $ scene_runtime.text = "\"Аманда, я знаю, что ты начала трахаться."
    if Amanda.var_int("fuckyou", 0):
        $ scene_runtime.text += "\nТем более что я и сам тебя поимел."
    $ scene_runtime.text += "\nТы не боишься залететь? В тебя часто кончают?\" задали вы деликатный вопрос Аманде."
    if Amanda.sex_stat("cuminside", 0) > 15:
        $ scene_runtime.text += "\n\n\"Знаешь, Стефан, часто. Я даже удивляюсь порой как мне везет пока что. "
    elif Amanda.sex_stat("cuminside", 0) == 0:
        $ scene_runtime.text += "\n\n\"Пока ни разу! Ты меня за дурочку не держи, я осторожна! "
    else:
        $ scene_runtime.text += "\n\n\"Когда как, время от времени. Думаю что ничего страшного. "
    if Amanda.corruption >= 50:
        $ scene_runtime.text += "А вообще я думаю так, чему быть - того не миновать. Трахаться я люблю, а при трахе порой и в киску кончают. Если меня кто обрюхатит, то так тому и быть.\" цинично ответила вам Аманда."
        $ Amanda.apply_social_chance(12, 1, 1, 56, 3, 1, "talk_ask_pregnancy")
    else:
        $ scene_runtime.text += "А так боюсь, конечно. Каждый раз, как меня сношают, я держу пальцы скрещенными и надеюсь на лучшее. Раньше я думала что для того, чтобы не залететь надо ноги держать скрещенными, но теперь поняла что это слишком тяжко. Что ж, думаю все будет хорошо.\" вздохнула Аманда."
        $ Amanda.apply_social_chance(12, 1, 1, 35, 3, -1, "talk_ask_pregnancy")
    $ Amanda.apply_social_chance(4, 1, -2, 35, 1, -2, "talk_ask_pregnancy")
    $ Amanda.mark_talked()
    $ Amanda.pregnancy_risk_asked_today = True
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAskDad(girl_name="amanda"):
    $ Amanda.mark_asked()
    $ scene_runtime.text = str(DaddyAskBuildPhrase(girl_name) or "")
    $ Amanda.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaAskNightBowl(girl_name="amanda"):
    $ renpy.dynamic("_bowl_result")
    $ Amanda.mark_asked()
    $ _bowl_result = Amanda.night_bowl_request_result(False)
    if bool(_bowl_result.get("granted", False)):
        $ scene_runtime.text = "Вы осторожно объясняете Аманде, что для мыловарения вам нужна подходящая посудина, и обещаете потом купить ей новую, поизящнее нынешней. Заодно добавляете, что если ей неловко носить ночную миску в комнату, то во дворе все равно стоит нужник.\n\nАманда мнется, краснеет, но в конце концов вздыхает и отдает вам свою ночную миску. \"Ладно уж. Только смотри потом и правда купи мне что-нибудь поприличнее,\" ворчит она."
    elif str(_bowl_result.get("reason", "") or "") == "unavailable":
        $ scene_runtime.text = "Сейчас к этой просьбе лучше не возвращаться."
    else:
        $ scene_runtime.text = "Вы начинаете аккуратно уговаривать Аманду отдать вам ночную миску для хозяйственного дела, обещая потом купить ей новую и даже посимпатичнее. Аманда вспыхивает до самых ушей и энергично мотает головой.\n\n\"Нет уж, Стефан. Я к своему горшку привыкла, а ночью во двор бегать мне страшновато. Обойдешься пока без него,\" отвечает она."
    $ Amanda.mark_talked()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaGiftFancyNightBowl(girl_name="amanda"):
    $ renpy.dynamic("_backyard_relief_pref")
    $ player.remove_item("fancy_night_bowl_001", 1)
    $ Amanda.fancy_night_bowl_received = True
    $ _backyard_relief_pref = Amanda.pick_backyard_relief_preference()
    $ scene_runtime.text = "Вы вручаете Аманде купленную красивую ночную миску. Аманда сначала смотрит на нее с недоверием, потом осторожно проводит пальцами по гладкой расписной глине и заметно смягчается.\n\n\"Вот это уже другое дело,\" говорит она, улыбаясь. \"Спасибо. С такой штукой и в комнате держать не так стыдно.\""
    if int(_backyard_relief_pref or 0) == 1:
        $ scene_runtime.text += "\n\nПомявшись, Аманда признается, что за это время успела даже привыкнуть иногда выбегать ночью во двор. \"Может, и с новым горшком все равно буду иногда так делать. На воздухе будто легче,\" смущенно добавляет она."
    else:
        $ scene_runtime.text += "\n\nПод конец Аманда облегченно добавляет, что теперь ей уже не придется красться ночью во двор без особой нужды. Похоже, новая миска и правда пришлась ей по душе."
    $ Amanda.change_social(friend_delta=1, open_delta=1)
    $ Amanda.apply_social_chance(8, 1, 1, 0, 0, 0, "talk_gift_night_bowl")
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaHouseholdInsight(girl_name="amanda"):
    $ renpy.dynamic("_special_entry")
    $ _special_entry = household_special_talk_entry(girl_name)
    if _special_entry is None:
        return
    $ Amanda.mark_asked()
    $ Amanda.mark_talked()
    $ Amanda.change_social(friend_delta=1, open_delta=1)
    $ household_advance_special_talk(girl_name)
    $ scene_runtime.text = str(_special_entry.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntAmandaHouseholdPriorities(girl_name="amanda"):
    $ Amanda.mark_asked()
    $ Amanda.mark_talked()
    $ Amanda.change_social(friend_delta=1, open_delta=1)
    $ scene_runtime.text = "Вы спрашиваете Аманду, чего ей сейчас хочется больше всего. Аманда сначала фыркает, будто вопрос слишком простой, но потом неожиданно отвечает вполне серьезно.\n\n\"Чтобы дома было повеселее, чтобы меня не только гоняли с подносами и чтобы иногда можно было почувствовать себя красивой, а не только полезной. И еще... чтобы ты иногда спрашивал меня не только о работе, но и о том, чего я сама хочу,\" признается она, уже куда тише под конец."
    $ scene_runtime.location_text = scene_runtime.text
    return
