label IntAmandaTalk(girl_name="amanda"):
    $ main_ui_begin_talk_state("Разговор с Амандой", girl_name)
    $ current_action_title = "Разговор с Амандой"
    $ current_action_content = None
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Аманда смотрит на вас с привычным любопытством, ожидая продолжения разговора."
        $ CurLocDesc = MainTxt
    call IntAmandaTalkRefresh(girl_name)
    return


label IntAmandaTalkRefresh(girl_name="amanda"):
    $ main_ui_begin_talk_state("Разговор с Амандой", girl_name)
    $ current_action_title = "Разговор с Амандой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, girl_name, CurLoc)))
    if TalkedToday.get(girl_name, 0) == 0:
        $ current_action_items.append(MenuItem("Поболтать", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "talk")))
    if FlirtedToday.get(girl_name, 0) == 0 and family_social_threshold_met(girl_name, "flirt"):
        $ current_action_items.append(MenuItem("Пофлиртовать", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "flirt")))
    if GiftedToday.get(girl_name, 0) == 0 and family_social_threshold_met(girl_name, "gift"):
        $ current_action_items.append(MenuItem("Подарить что-нибудь", Function(main_ui_call_label, "PlayerCardGiftToFixedTargetMenu", girl_name)))
        if player_card_has_shareable_items() and family_social_threshold_met(girl_name, "share"):
            $ current_action_items.append(MenuItem("Поделиться угощением", Function(main_ui_call_label, "PlayerCardShareToFixedTargetMenu", girl_name)))
    $ _legare_text = "Запретить ей %s с месье Легаре" % ("гулять" if virginity.get("amanda", 0) else "трахаться")
    $ _can_dress_change = amanda_dress_change_has_options(girl_name)

    if Talked.get(girl_name, 0) < 3 and Friends.get(girl_name, 0) < 5:
        $ current_action_items.append(MenuItem("Попробовать помириться с Амандой", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "reconcile")))

    if Talked.get(girl_name, 0) < 3 and AmandaVar.get("alberprohibit", 0) > 0:
        $ current_action_items.append(MenuItem("Сказать Аманде что вы передумали и она может встречаться с Альбером", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "allow_alber")))

    if Talked.get(girl_name, 0) < 3 and AmandaVar.get("prohibitliza", 0) > 0:
        $ current_action_items.append(MenuItem("Разрешить Аманде болтать с Лизеттой", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "allow_liza")))

    if Talked.get(girl_name, 0) < 3 and AmandaVar.get("gloryscold", 0) > 0:
        $ current_action_items.append(MenuItem("Сказать Аманде что она может ходить к Лизетте в глорихолл", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "allow_glory")))

    if Talked.get(girl_name, 0) < 3 and AmandaVar.get("prohibitwithguys", 0) > 0:
        $ current_action_items.append(MenuItem("Сказать Аманде что она может встречаться с парнями", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "allow_guys")))

    if Talked.get(girl_name, 0) < 3 and AmandaVar.get("warnnotwork", 0) > 0:
        $ current_action_items.append(MenuItem("Сказать Аманде что она может иногда брать перерывы", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "allow_breaks")))

    if AskedToday.get(girl_name, 0) == 0 and Talked.get(girl_name, 0) < 3 and AmandaVar.get("knownotvirgin", 0) > 0 and AmandaVar.get("knowdeflowerlegare", 0) == 0 and AmandaVar.get("deflowerlegare", 0) > 0:
        $ current_action_items.append(MenuItem("Спросить где она потеряла девственность", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "ask_virginity")) )

    if Talked.get(girl_name, 0) < 3 and AmandaVar.get("knowlegaresex", 0) > 0 and AmandaVar.get("alberprohibit", 0) == 0:
        $ current_action_items.append(MenuItem(_legare_text, Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "ban_alber")))

    if Talked.get(girl_name, 0) < 3 and AmandaVar.get("sawwithguys", 0) > 0 and AmandaVar.get("prohibitwithguys", 0) == 0:
        $ current_action_items.append(MenuItem("Запретить ей трахаться с соседскими парнями", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "ban_guys")))

    if AskedToday.get(girl_name, 0) == 0 and Talked.get(girl_name, 0) < 3 and AmandaVar.get("knowsexactive", 0) > 0 and pregnancy.get(girl_name, 0) < 120 and AmandaVar.get("askzalettoday", 0) == 0 and virginity.get("amanda", 0) == 0:
        $ current_action_items.append(MenuItem("Спросить не боиться ли она залететь", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "ask_pregnancy"))) 

    if AskedToday.get(girl_name, 0) == 0 and Talked.get(girl_name, 0) < 3 and Friends.get(girl_name, 0) >= 8 and pregnancy.get(girl_name, 0) >= 120:
        $ _dad_phrase = DaddyAskBuildPhrase(girl_name)
        if str(_dad_phrase or "") != "":
            $ current_action_items.append(MenuItem("Спросить, знает ли она от кого пузо нагуляла", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "ask_dad"))) 

    if AskedToday.get(girl_name, 0) == 0 and Talked.get(girl_name, 0) < 3 and amanda_can_be_asked_for_night_bowl():
        $ current_action_items.append(MenuItem("Попросить у Аманды ее ночную миску", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "ask_night_bowl")))

    if amanda_can_receive_fancy_night_bowl():
        $ current_action_items.append(MenuItem("Подарить Аманде красивую ночную миску", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "gift_fancy_night_bowl")))
    if AskedToday.get(girl_name, 0) == 0 and household_special_talk_available(girl_name):
        $ _amanda_special_entry = household_special_talk_entry(girl_name)
        if _amanda_special_entry is not None:
            $ current_action_items.append(MenuItem(str(_amanda_special_entry.get("label", "Спросить о чем-то важном") or "Спросить о чем-то важном"), Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "insight")))
    if AskedToday.get(girl_name, 0) == 0 and int(Friends.get(girl_name, 0) or 0) >= 15:
        $ current_action_items.append(MenuItem("Спросить, чего ей сейчас хочется больше всего", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "priorities")))

    if _can_dress_change:
        $ current_action_items.append(MenuItem("Переодеть Аманду", Function(main_ui_call_label, "IntAmandaTalkApply", girl_name, "dress")))
    $ current_action_items.append(MenuItem("Уйти", Function(main_ui_end_talk_state)))
    return


label IntAmandaTalkApply(girl_name="amanda", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "reconcile":
        $ MainTxt = "Вы подошли к Аманде и извинились за то, что были к ней несколько невнимательны и грубы последнее время. В свое оправдание вы заметили, что уберечь трактир от разорения очень сложно и всем вам нужно дружно работать вместе, чтобы преуспеть."
        if renpy.random.randint(1, 3) == 1:
            $ MainTxt += "\n\nАманда благосклонно выслушала вас, трогательно обняла и сказала, что очень к вам привязана!"
            call SlutFriendsIncrease(girl_name, 6, 1, 1, 0, 0, 0)
        else:
            $ MainTxt += "\n\nАманда холодно выслушала вас, фыркнула и пошла прочь."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "talk":
        $ _talk_result = player_talk_to(girl_name)
        $ MainTxt = str(_talk_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "flirt":
        $ _flirt_result = player_flirt_with(girl_name)
        $ MainTxt = str(_flirt_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "allow_alber":
        $ MainTxt = "Вы подошли к Аманде и сказали, что, успокоившись и подумав, вы поменяли свое мнение и теперь не имеете ничего против того, чтобы она встречалась с Альбером Легаре."
        if AmandaVar.get("alberfriends", 0) >= 9:
            $ MainTxt += "\n\nАманда взвизгнула от радости, обняла вас и поцеловала, сказав что она вас очень любит."
            call SlutFriendsIncrease(girl_name, 10, 1, 2, 20, 1, 1)
        else:
            $ MainTxt += "\n\nАманда поблагодарила вас за доверие."
            call SlutFriendsIncrease(girl_name, 10, 1, 1, 20, 1, 1)
        $ Friends["alber"] = Friends.get("alber", 0) + 2
        if week == 5 and time < 3:
            call amanda_legare_dance_sequence
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["alberprohibit"] = 0
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "allow_liza":
        $ MainTxt = "Вы подошли к Аманде и сказали ей, что передумали. Конечно, ей нужна подруга, а так как в пределах досягаемости есть лишь Лизетта, то так тому и быть. Вы только надеетесь, что она будет использовать ум, фильтровать ее слова и не принимать все за чистую монету.\n\nАманда чмокнула вас в щечку и сказала, что всегда верила в ваш разум."
        call SlutFriendsIncrease(girl_name, 10, 1, 1, 20, 1, 1)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["prohibitliza"] = 0
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "allow_glory":
        $ MainTxt = "Вы подошли к Аманде и, собрав волю в кулак, сказали, что все не так страшно. Она уже взрослая, опыт ей пригодится, и лучше, чтобы этот опыт она получила в более-менее безопасной обстановке. Каковой вы считаете глорихол.\n\nА что? Ширмочка есть, анонимность гарантируется, и вы не собираетесь устраивать из этого трагедию.\n\nАманда чмокнула вас в щечку и сказала, что всегда верила в ваш разум."
        call SlutFriendsIncrease(girl_name, 10, 1, 1, 20, 1, 1)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["gloryscold"] = 0
        $ AmandaVar["glorywalkout"] = 0
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "allow_guys":
        $ MainTxt = "Вы подошли к Аманде и спокойно сказали ей, что обдумали ситуацию и поменяли свое мнение. Конечно, ей надо встречаться со сверстниками, и конечно парни такого возраста только и думают что о потрахушках. Ничего в этом неестественного нет. Так что если она хочет крутить роман где-то на стороне, вы не против.\n\nАманда поцеловала вас в губы, провела рукой по вашей ширинке и, довольная, убежала."
        call SlutFriendsIncrease(girl_name, 15, 1, 1, 42, 1, 1)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["prohibitwithguys"] = 0
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "allow_breaks":
        $ MainTxt = "Вы подошли к Аманде и сказали ей, что погорячились. Конечно, вы не хотите, чтобы она сидела безвылазно в трактире с утра до ночи. Если хочет отдохнуть, прогуляться - то пожалуйста. Даже свежим воздухом подышать может, ну если, конечно, ветер не от смолокурен с верфей дует.\n\nАманда обрадовалась и убежала."
        call SlutFriendsIncrease(girl_name, 12, 1, 1, 0, 0, 0)
        if renpy.random.randint(1, 5) == 1:
            $ cooking[girl_name] = cooking.get(girl_name, 0) + 2
            $ cleaning[girl_name] = cleaning.get(girl_name, 0) + 2
            $ waitress[girl_name] = waitress.get(girl_name, 0) + 2
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["warnnotwork"] = 0
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_virginity":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ MainTxt = "\"Амандочка!\" как можно ласковей подкатились вы к Аманде. \"Я знаю, что ты уже не девочка. А может ты раскажешь мне, с кем это ты так умудрилась?\""
        if Friends.get(girl_name, 0) > 11 and AmandaVar.get("alberprohibit", 0) == 0:
            $ MainTxt += "\n\n\"Ну, чего же не рассказать? С Альберчиком мой первый раз был. Мы с ним танцевали-плясали, а потом к нему пошли, на задний двор. Там все и случилось.\"\n\"Как с Альбером!\" Потрясенно сказали вы. Он же наверное втрое тебя старше, и семья у него!\"\n\"Ну и что? Жена у него давалка, вот и он развлекается как может. Вдруг мне удасться его в себя влюбить, выйду я за него, буду не у тебя тут в трактире болтаться, а уважаемой женой уважаемого торговца!\"\n\"Да ты сама в это веришь?\"\n\"Ну конечно, что же здесь невероятного?\"\nВы не нашлись с ответом."
            call SlutFriendsIncrease(girl_name, 12, 1, 1, 0, 0, 0)
            $ AmandaVar["knowdeflowerlegare"] = 1
            $ AmandaVar["knowlegaresex"] = 1
        else:
            $ MainTxt += "\n\n\"Знаешь что, это мое дело, моя личная жизнь и ты в нее не лезь,\" отозвалась Аманда. Вы попробовали от нее добиться ответа еще пару раз, но все было бесполезно."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ban_alber":
        if AmandaVar.get("sawlegaresex", 0):
            $ MainTxt = "\"Знаешь что, Аманда! Я видел, как ты трахалась с этим старым козлом, этим месье Легаре, и мне это не понравилось!\""
        else:
            $ MainTxt = "\"Аманда! Я знаю, что ты даешь этому похотливому козлу, этому, как его, месье Легаре. Это мне совсем не по нраву!\""
        $ MainTxt += "\n\nогорошили вы Аманду. И, не давая ей опомнится, вы продолжили: \"Ты вообще думала, когда с ним путалась? Он старше тебе даже не вдвое, а наверное втрое и женат! Так вот, я не желаю чтобы это повторялось, понятно!\"\nАманда попыталась было вам что-то возразить, но вы и слушать не стали ее лепет, лишь повторили: \"Понятно?!\" и, не дожидаясь ответа ушли. "
        call SlutFriendsIncrease(girl_name, 4, 1, -2, 0, 0, 0)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["alberprohibit"] = 1
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ban_guys":
        $ MainTxt = "\"Знаешь что, подруга,\" подступили вы к Аманде. \"Ты себе репутацию подстилки устраиваешь, и мне это не нравится. Чтобы с этого момента никаких потрахушек по амбарам и дворикам, понятно?\"\nАманда попыталась было вам что-то возразить, но вы и слушать не стали ее лепет, лишь повторили: \"Понятно?!\" и, не дожидаясь ответа, ушли."
        call SlutFriendsIncrease(girl_name, 4, 1, -2, 35, 1, -2)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["prohibitwithguys"] = 1
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_pregnancy":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ MainTxt = "\"Аманда, я знаю, что ты начала трахаться."
        if AmandaVar.get("fuckyou", 0):
            $ MainTxt += "\nТем более что я и сам тебя поимел."
        $ MainTxt += "\nТы не боишься залететь? В тебя часто кончают?\" задали вы деликатный вопрос Аманде."
        if cuminside.get(girl_name, 0) > 15:
            $ MainTxt += "\n\n\"Знаешь, Стефан, часто. Я даже удивляюсь порой как мне везет пока что. "
        elif cuminside.get(girl_name, 0) == 0:
            $ MainTxt += "\n\n\"Пока ни разу! Ты меня за дурочку не держи, я осторожна! "
        else:
            $ MainTxt += "\n\n\"Когда как, время от времени. Думаю что ничего страшного. "
        if sluttiness.get(girl_name, 0) >= 50:
            $ MainTxt += "А вообще я думаю так, чему быть - того не миновать. Трахаться я люблю, а при трахе порой и в киску кончают. Если меня кто обрюхатит, то так тому и быть.\" цинично ответила вам Аманда."
            call SlutFriendsIncrease(girl_name, 12, 1, 1, 56, 3, 1)
        else:
            $ MainTxt += "А так боюсь, конечно. Каждый раз, как меня сношают, я держу пальцы скрещенными и надеюсь на лучшее. Раньше я думала что для того, чтобы не залететь надо ноги держать скрещенными, но теперь поняла что это слишком тяжко. Что ж, думаю все будет хорошо.\" вздохнула Аманда."
            call SlutFriendsIncrease(girl_name, 12, 1, 1, 35, 3, -1)
        call SlutFriendsIncrease(girl_name, 4, 1, -2, 35, 1, -2)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ AmandaVar["askzalettoday"] = 1
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_dad":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ MainTxt = str(DaddyAskBuildPhrase(girl_name) or "")
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "ask_night_bowl":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ _bowl_result = amanda_night_bowl_request_result(False)
        if bool(_bowl_result.get("granted", False)):
            $ MainTxt = "Вы осторожно объясняете Аманде, что для мыловарения вам нужна подходящая посудина, и обещаете потом купить ей новую, поизящнее нынешней. Заодно добавляете, что если ей неловко носить ночную миску в комнату, то во дворе все равно стоит нужник.\n\nАманда мнется, краснеет, но в конце концов вздыхает и отдает вам свою ночную миску. \"Ладно уж. Только смотри потом и правда купи мне что-нибудь поприличнее,\" ворчит она."
        elif str(_bowl_result.get("reason", "") or "") == "unavailable":
            $ MainTxt = "Сейчас к этой просьбе лучше не возвращаться."
        else:
            $ MainTxt = "Вы начинаете аккуратно уговаривать Аманду отдать вам ночную миску для хозяйственного дела, обещая потом купить ей новую и даже посимпатичнее. Аманда вспыхивает до самых ушей и энергично мотает головой.\n\n\"Нет уж, Стефан. Я к своему горшку привыкла, а ночью во двор бегать мне страшновато. Обойдешься пока без него,\" отвечает она."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "gift_fancy_night_bowl":
        $ _player_remove_item_by_id("fancy_night_bowl_001", 1)
        $ AmandaVar["got_fancy_night_bowl"] = 1
        $ _backyard_relief_pref = amanda_pick_backyard_relief_preference()
        $ MainTxt = "Вы вручаете Аманде купленную красивую ночную миску. Аманда сначала смотрит на нее с недоверием, потом осторожно проводит пальцами по гладкой расписной глине и заметно смягчается.\n\n\"Вот это уже другое дело,\" говорит она, улыбаясь. \"Спасибо. С такой штукой и в комнате держать не так стыдно.\""
        if int(_backyard_relief_pref or 0) == 1:
            $ MainTxt += "\n\nПомявшись, Аманда признается, что за это время успела даже привыкнуть иногда выбегать ночью во двор. \"Может, и с новым горшком все равно буду иногда так делать. На воздухе будто легче,\" смущенно добавляет она."
        else:
            $ MainTxt += "\n\nПод конец Аманда облегченно добавляет, что теперь ей уже не придется красться ночью во двор без особой нужды. Похоже, новая миска и правда пришлась ей по душе."
        $ Friends[girl_name] = int(Friends.get(girl_name, 0) or 0) + 1
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        call SlutFriendsIncrease(girl_name, 8, 1, 1, 0, 0, 0)
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "insight":
        $ _special_entry = household_special_talk_entry(girl_name)
        if _special_entry is None:
            call IntAmandaTalkRefresh(girl_name)
            return
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ household_advance_special_talk(girl_name)
        $ MainTxt = str(_special_entry.get("text", "") or "")
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "priorities":
        $ AskedToday[girl_name] = int(AskedToday.get(girl_name, 0) or 0) + 1
        $ Talked[girl_name] = int(Talked.get(girl_name, 0) or 0) + 1
        $ Friends[girl_name] = min(20, int(Friends.get(girl_name, 0) or 0) + 1)
        $ otkroven[girl_name] = min(20, int(otkroven.get(girl_name, 0) or 0) + 1)
        $ MainTxt = "Вы спрашиваете Аманду, чего ей сейчас хочется больше всего. Аманда сначала фыркает, будто вопрос слишком простой, но потом неожиданно отвечает вполне серьезно.\n\n\"Чтобы дома было повеселее, чтобы меня не только гоняли с подносами и чтобы иногда можно было почувствовать себя красивой, а не только полезной. И еще... чтобы ты иногда спрашивал меня не только о работе, но и о том, чего я сама хочу,\" признается она, уже куда тише под конец."
        $ CurLocDesc = MainTxt
        call IntAmandaTalkRefresh(girl_name)
        return

    if str(choice_code or "") == "dress":
        call int_amanda_dress_change
        return

    return


label IntAmandaTalkRestore:
    $ main_ui_end_talk_state()
    return
