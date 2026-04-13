init python:
    def georgett_grope_outcome(girl_name="georgett", girl_loc="street"):
        girl_key = str(girl_name or "georgett")
        loc_key = str(girl_loc or "street")
        has_paid_context = (money >= 8 or (money >= 4 and loc_key == "tavern")) and cametoday < cancumdaily

        if not has_paid_context:
            if cametoday >= cancumdaily:
                grope_text = "«На сегодня с тебя уже хватит, красавчик», - усмехнулась %s. «Приходи завтра, если захочешь еще.»" % RealName.get(girl_key, girl_key)
            else:
                grope_text = "«Эй, осади лошадей!» говорит вам %s. «Сначала заплати, а потом уже лапай!»" % RealName.get(girl_key, girl_key)
            return {"text": grope_text, "show_current_sex": False}

        if Friends.get(girl_key, 0) >= 10:
            grope_text = "Вы начали мять сиськи %s через тонкую ткань ее блузки.\nВы сунули руку под короткую юбочку вашей любовницы и стали наминать ее вульву." % RealName2.get(girl_key, girl_key)
            if CumInsideYou.get(girl_key, 0) > 0:
                grope_text += "\n\nВы почувствовали свою сперму в пещерке %s." % RealName2.get(girl_key, girl_key)
            elif CumInsideOthers.get(girl_key, 0) > 0:
                grope_text += "\n\nВаши пальцы заскользили по пещерке %s, похоже кто-то уже кончил в нее." % RealName2.get(girl_key, girl_key)
        else:
            grope_text = "«Эй, осади лошадей!» говорит вам %s. «Сначала заплати, а потом уже лапай!»" % RealName.get(girl_key, girl_key)

        return {"text": grope_text, "show_current_sex": True}


label IntGeorgettTalk(girl_name="georgett", girl_loc=""):
    if str(girl_loc or "") == "":
        if CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "TavernMain":
            $ girl_loc = "tavern"
        elif CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "PortStreets":
            $ girl_loc = "street"
        elif str(CurLoc or "") == "TavernMain":
            $ girl_loc = "tavern"
        else:
            $ girl_loc = "street"

    if str(girl_loc or "") == "street" and str(girl_name or "") == "georgett" and int(Friends.get("georgett", 0) or 0) <= 0:
        $ MainTxt = "-Привет красавчик! Не хочешь ли поразвлечься? Всего восемь мараведи!\n\nВы поговорили с ней и узнали, что ее зовут Жоржетта Брюно, она шлюха и промышляет здесь уже давно."
        $ CurLocDesc = MainTxt
        $ Friends["georgett"] = int(Friends.get("georgett", 0) or 0) + 1

    $ main_ui_begin_talk_state("Разговор с Жоржеттой", girl_name)
    $ current_action_title = "Разговор с Жоржеттой"
    $ current_action_content = None
    python:
        _georgett_picture = str(girl_card_portrait_path(girl_name) or "").strip()
        if _georgett_picture and renpy.loadable(_georgett_picture):
            scene_image = _georgett_picture
            _layout_last_picture = _georgett_picture
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Жоржетта вопросительно смотрит на вас, ожидая, о чем вы захотите поговорить."
        $ CurLocDesc = MainTxt
    call IntGeorgettTalkRefresh(girl_name, girl_loc)
    return


label IntGeorgettTalkRefresh(girl_name="georgett", girl_loc="street"):
    $ main_ui_begin_talk_state("Разговор с Жоржеттой", girl_name)
    $ current_action_title = "Разговор с Жоржеттой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(show_girl_card_main_ui_state, girl_name)))
    $ current_action_items.append(MenuItem("Болтать", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "smalltalk")))

    if GeorgettVar.get("seeclients", 0) and Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 7:
        $ current_action_items.append(MenuItem("Спросить о клиентах", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_clients")))

    if GeorgettVar.get("askclients", 0) and Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 7 and GiveOrgasms.get(girl_name, 0) >= 3:
        $ current_action_items.append(MenuItem("Спросить о сексе", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_sex")))

    if GeorgettVar.get("asksex", 0) and Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 7 and GiveOrgasms.get(girl_name, 0) >= 4:
        $ current_action_items.append(MenuItem("Спросить о семье", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_family")))

    if GeorgettVar.get("askparents", 0) and Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 7 and GiveOrgasms.get(girl_name, 0) >= 4:
        $ current_action_items.append(MenuItem("Спросить о беременности", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_pregnancy")))

    if GeorgettVar.get("askpregnancy", 0) and Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 7 and GiveOrgasms.get(girl_name, 0) >= 5:
        $ current_action_items.append(MenuItem("Спросить о детях", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_kids")))

    if GeorgettVar.get("SawChurchAfterCermon", 0) and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Спросить об отце Герхарде", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_gerhard")))

    if LizaVar.get("SawChurchAfterCermon", 0) and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Рассказать про Лизетту и отца Герхарда", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "tell_liza_gerhard")))

    if AlberVar.get("talkedaboutliza", 0) and Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 7 and CurrentLoc.get(girl_name, "") == "PortStreets":
        $ current_action_items.append(MenuItem("Предложить работать у себя в трактире", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "invite_tavern")))

    if jobWhoreAvail.get(girl_name, 0) and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Спросить как работается у вас в трактире", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_work")))

    if jobWhoreAvail.get(girl_name, 0) and Talked.get(girl_name, 0) < 2 and LizaVar.get("GloryHoleAsked", 0) == 1 and GeorgettVar.get("GloryHoleExplained", 0) == 0:
        $ current_action_items.append(MenuItem("Спросить про работу в \"Пьяном Пирате\"", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_pirate")) )

    if jobWhoreAvail.get(girl_name, 0) and Talked.get(girl_name, 0) < 2 and TavernGloryHole == 2 and GeorgettVar.get("GloryHoleAgreed", 0) == 0:
        $ current_action_items.append(MenuItem("Договориться об условиях работы у глорихола", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "gloryhole_terms")) )

    if (((GeorgettVar.get("TellAboutEddieMomSex", 0) == 0 and (BeckyVar.get("EddieTryToFuck", 0) == 4 or BeckyVar.get("visitedhome", 0) >= 7)) or (BeckyVar.get("EddieGeorg", 0) == 0 and EddieVar.get("TalkedAboutGeorgett", 0) == 1 and BeckyVar.get("visitedhome", 0) >= 3 and (EddieVar.get("SawMomSex", 0) > 0 or BeckyVar.get("HomeSex", 0) > 0))) and Talked.get(girl_name, 0) < 2):
        $ current_action_items.append(MenuItem("Обсудить Эдди", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "talk_eddie")))

    if BeckyVar.get("EddieGeorg", 0) > 0 and BeckyVar.get("EddieWhoreHome", 0) == 0 and (money > 25 or (BeckyVar.get("EddieGeorg", 0) > 1 and money > 10)) and Talked.get(girl_name, 0) < 2:
        $ current_action_items.append(MenuItem("Предложить Жоржетте проспонсировать ее визит к Эдди домой", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "sponsor_eddie_home")) )

    if BeckyVar.get("EddieGeorg", 0) > 0 and time <= 3:
        $ current_action_items.append(MenuItem("Спросить, не приходил ли Эдди", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_eddie_visit")) )

    if (money >= 8 or (money >= 4 and girl_loc == "tavern")) and cametoday < cancumdaily:
        $ current_action_items.append(MenuItem("Снять", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "hire")) )

    $ current_action_items.append(MenuItem("Лапать", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "grope")))

    if Talked.get(girl_name, 0) < 2 and Friends.get(girl_name, 0) >= 8 and pregnancy.get(girl_name, 0) >= 120:
        $ _dad_phrase = DaddyAskBuildPhrase(girl_name)
        if str(_dad_phrase or "") != "":
            $ current_action_items.append(MenuItem("Поинтересоваться, знает ли она от кого залетела", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "ask_dad")) )

    if girl_loc == "tavern":
        $ current_action_items.append(MenuItem("Обсудить одежду", Function(main_ui_call_label, "IntGeorgettTalkApply", girl_name, girl_loc, "dress")) )

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntGeorgettTalkApply(girl_name="georgett", girl_loc="street", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "smalltalk":
        $ MainTxt = "Вы некоторое время болтаете с Жоржеттой о разных вещах."
        if Talked.get(girl_name, 0) <= 2 and renpy.random.randint(1, 2) == 1:
            if Friends.get(girl_name, 0) < 3 or (LickPussy.get(girl_name, 0) >= 4 and Friends.get(girl_name, 0) < 5) or (GiveOrgasms.get(girl_name, 0) >= 2 and LickPussy.get(girl_name, 0) >= 4 and Friends.get(girl_name, 0) < 7):
                $ MainTxt += "\n\nВы чуть лучше узнали Жоржетту."
                $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
            elif Friends.get(girl_name, 0) < 7:
                $ MainTxt += "\n\nИз уклончивых ответов девушки вы поняли, что она вам еще мало доверяет. Может, если бы вы узнали ее получше или доставили ей приятное, она бы с вами поделилась еще чем-то."
        if Talked.get(girl_name, 0) > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_clients":
        $ MainTxt = "«Ну в день у меня обычно бывает от трех до пяти клиентов. Хотя конечно день на день не приходится, например, помню, в гавань зашла военная эскадра. Ох, как тогда имели всех девочек! Меня отодрали человек двадцать, наверное, а то и больше. Я спускала и спускала, ох, как же сладко было тогда!» - говорит Жоржетта, автоматически поглаживая промежность сквозь юбку."
        if GeorgettVar.get("askclients", 0) == 0:
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
            $ GeorgettVar["askclients"] = 1
            $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_sex":
        $ MainTxt = "«Ох, красавчик, мне всегда нравился секс. Маленькой еще была, за другими подсматривала и писю теребила. За сестренками старшими, как они с мальчишками то на сеновале, то в саду забавлялись, за маменькой как она то с папкой, то с дядей мельником, то с дядей молочником, то с сестренкиными дружками кувыркалась. За папкой, как он с соседками да с сестриными подружками сношался. Ну а когда Кристоф и Мишель, парни с соседней улицы, после танцев меня в уголке зажали и стали лапать, то я и не ломалась совсем и вскоре у меня в киске вместо девственной плевы было две порции свежего семени. Ну а потом пошло-поехало, никому я почитай и не отказывала, больно приятно это было. Потом я здесь, в городе устроилась, здесь мне за это и деньги платят. Вот еще бы все клиенты были как ты, внимательные. А то многие только о себе и думают, а девушке кончить не дают. Бывает за день только пару раз и разрядишься.» - рассказывает Жоржетта."
        if GeorgettVar.get("asksex", 0) == 0:
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
            $ GeorgettVar["asksex"] = 1
            $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_family":
        $ MainTxt = "«Даже не знаю, папка мой действительно ли мне папка, мамочка-то моя на передок всегда слаба была. Да и батяня за всеми юбками бегал, да и сейчас бегает. Любили они потрахаться, и от нас даже этого не скрывали. А уж на праздниках-то! Помню, однажды на празднике урожая мамка моя, сестренка старшая, Симона, и Жанна, мельникова дочка, в такой раж вошли что голыми на столах танцевали. Ну а уж после их гости и оприходовали. Папенька тот тоже, Симоне борозду-то распахал и засеял, не посмотрел что дочка. Симонка-то после того случая понесла ведь, и не поймешь от кого, может и от папки. Ну а вообще да, хорошо жили, дружно. Я тоже с папкой да с братцами несколько раз перепихнулась.» - рассказывает Жоржетта."
        if GeorgettVar.get("askparents", 0) == 0:
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
            $ GeorgettVar["askparents"] = 1
            $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_pregnancy":
        $ MainTxt = "«Беременность? Ну а как же без нее-то? Мужики они-то любят девушкам своим семенем прямо в маточку брызнуть, а от этого, как всем известно, детки родятся. Вот Симонка, сестра моя старшая, прежде чем замуж выскочила, целых троих нагуляла. А себя вспомнить - первый раз у меня животик округлился когда только-только первые волосики на письке пробиваться начали. Но мамочка моя всегда говорила, что ребенок есть ребенок, ему всегда рады, и ничего страшного в залете нет.» - поведала вам Жоржетта."
        if GeorgettVar.get("askpregnancy", 0) == 0:
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
            $ GeorgettVar["askpregnancy"] = 1
            $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_kids":
        $ MainTxt = "«Дети? Четверо у меня их. Первую свою доченьку Лизку, Лизетту то есть, я даже знаю от кого родила. Ну, почти. Неделя только прошла как я девства лишилась и на рынок мы поехали. А там у купца одного из дальних стран носильщики - один другого мускулистее. А трое из них и вовсе на наших не похожи - кожа как уголь. Ну и услышала я как мама тете Франсуазе говорит что мол пошли, опробуем их. Стала я проситься с ними пойти, мама удивилась, спросила не мала ли я, но разрешила. Зашли мы за шатер с ними и часа два нас имели. Тогда, кстати, я у мамы первый раз киску-то и полизала. А через 9 месяцев Лизетта-то мулаточкой у меня и родилась.»"
        if LizaVar.get("ProstStart", 0) == 0:
            $ MainTxt += "\n\n«Насчет остальных же троих я не так уверенна. От кого угодно могла я залететь. Детки же мои сейчас с мамой и папой моими живут, Лизетта вот только порой ко мне приезжает.»"
        else:
            $ MainTxt += "\n\n«Насчет остальных же троих я не так уверенна. От кого угодно могла я залететь. Детки же мои сейчас с мамой и папой моими живут, а Лизетта вот уже ко мне перебралась, помогает.»"
        if GeorgettVar.get("askkids", 0) == 0:
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
            $ GeorgettVar["askkids"] = 1
            $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_gerhard":
        $ MainTxt = "«Отец Герхард? Кто-то, наверное ты, негодник, рассказал ему что мы с тобой во время службы трахались. Вот он меня и раскрутил на исповеди. Теперь он меня порой после воскресной службы потрахивает. Оргазм и благословление это конечно не мараведи, но тоже неплохо, так что я не в обиде.»"
        if GeorgettVar.get("TalkChurchAfterCermon", 0) == 0:
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
            $ GeorgettVar["TalkChurchAfterCermon"] = 1
            $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "tell_liza_gerhard":
        if GeorgettVar.get("TalkChurchAfterCermonLiza", 0) == 0:
            $ MainTxt = "Вы рассказываете Жоржетте что вы видели как отец Герхард соблазнил ее дочь после воскресной службы. Также вы упоминаете что Лизетта и до встречи с похотливым жрецом не отказывала мальчикам.\n«Ох дочка, повзрослела уже, а мне ничего не сказала! А я уже волноваться начала, подрастает, а мальчиками ничего нет» - реагирует Жоржетта. «А отец Герхард-то, хорош, дочку мою трахнул, а мне и не подумал сказать. Ну, раз девочка большая уже выросла, будет мне помогать», - решает она.\n\n«Ну, Стефан, завтра встречай нас обеих», - и с этими словами она удаляется."
            $ GeorgettVar["TalkChurchAfterCermonLiza"] = 1
            $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
            $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
            $ CurLocDesc = MainTxt
            jump StreetTavern
        $ MainTxt = "Вы рассказываете Жоржетте что вы снова видели как отец Герхард трахал ее дочь после воскресной службы.\n«Молодец дочка, благословление Ильматера лишним не будет, да и любовник отец Герхард хороший!» - отвечает Жоржетта."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "invite_tavern":
        if Friends.get(girl_name, 0) < 10:
            $ MainTxt = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«Не, мил человек», - отвечает Жоржетта, «не могу я тебе еще доверять. А вдруг обманешь? Мы пока здесь, как привыкли, поработаем.»"
            $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
            $ CurLocDesc = MainTxt
            call IntGeorgettTalkRefresh(girl_name, girl_loc)
            return
        if Friends.get("liza", 0) < 8:
            $ MainTxt = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«Не, мил человек», - отвечает Жоржетта, «я бы с радостью, но доча моя в тебе еще сомневается. Не могу я ее пока убедить. Так что мы пока здесь, как привыкли, поработаем.»"
            $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
            $ CurLocDesc = MainTxt
            call IntGeorgettTalkRefresh(girl_name, girl_loc)
            return
        $ MainTxt = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«А что?», - говорит Жоржетта, «почему бы и нет? Ты мне нравишься, доча моя тоже в тебе души не чает, отчего бы и не начать работать у тебя? Согласные мы!»\nВы приводите маму с дочкой в свой трактир, представляете их маме и сестрам, объясняете в чем заключается их промысел и что заниматься им отныне они будут у вас. Мама воспринимает известие спокойно, сестры слегка шокированы. Но владелец трактира - вы, так что у них нет выбора кроме как покориться. Обсуждение деталей затягивается до вечера, так что приступить к делу новая парочка ваших работниц сможет только на следующий день."
        $ Friends[girl_name] = Friends.get(girl_name, 0) + 1
        $ CurrentLoc["georgett"] = "TavernMain"
        $ CurrentLoc["liza"] = "TavernMain"
        $ jobWhoreAvail["georgett"] = 1
        $ jobwhore["georgett"] = 1
        $ jobWhoreAvail["liza"] = 1
        $ jobwhore["liza"] = 1
        $ householdmembers = int(householdmembers) + 2 + int(ProstitutesKids)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        call NextDay("TavernMain", 1)
        return

    if str(choice_code or "") == "ask_work":
        $ MainTxt = "Вы спрашиваете Жоржетту как ей работается у вас в трактире.\n"
        if TavernGloryHole == 2:
            $ MainTxt += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает. А теперь, когда есть глорихол, наши заработки еще повысились!»"
        elif GeorgettVar.get("GloryHoleExplained", 0) == 1:
            $ MainTxt += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает. Разве что если бы еще глорихол был, то можно бы было еще больше денег заработать, наверное.»"
        else:
            $ MainTxt += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает.» Однако у вас остается впечатление что она хотела еще что-то сказать, но предпочла промолчать."
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_pirate":
        $ MainTxt = "Вы расспрашиваете Жоржетту про ее работу в трактире «Пьяный Пират».\n«Ох Лизетта, Лизетта! Вечно все перепутает! Не Холглор, а глорихол! Занятная штука. С ним на одного клиента меньше времени уходит, поэтому можно дешевле брать и люди им чаще пользуются. И работать с ним удобно! Все хотела спросить почему у тебя такого нет, но решила что тебе виднее и промолчала.»\nВас заинтересовал рассказ девушки и вы уточнили у нее устройство данной конструкции.\n«Хм, а ведь хороший мастер такое должен бы быстро суметь сделать...» - подумали вы, выслушав ее рассказ."
        $ GeorgettVar["GloryHoleExplained"] = 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "gloryhole_terms":
        $ MainTxt = "Вы рассказываете Жоржетте про устроенный вами глорихол. Вы предлагаете установить прейскурант за такой сервис на уровне 6 мараведи. В конечном итоге вы вынуждены согласиться с тем, что вам пойдут только два мараведи, а остальные четыре - в карман трудящихся. Единственное, что утешило вас, так это то, что вы смогли добиться согласия на бесплатный отсос для себя."
        $ GeorgettVar["GloryHoleAgreed"] = 1
        $ jobGloryHoleAvail["georgett"] = 1
        $ jobGloryHoleAvail["liza"] = 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "talk_eddie":
        if BeckyVar.get("EddieTryToFuck", 0) == 4 or BeckyVar.get("visitedhome", 0) >= 7:
            $ MainTxt = "«Жоржетт, ты была права. Эдди действительно по своей мамочке сох. Я им все подстроил, дверь в спальню отпер, Бекки раздел и внимание ее отвлек. Ну а Эдди предупредил заранее, что может заходить на огонек. Так он паршивец ни секунды не сомневался, забежал и засадил мамке своей!»\n«А она что?»\n«А ничего, подмахивать ему стала как ни в чем не бывало.»\n«Ну, я чего-то в таком роде и ожидала с первого раза как он меня снял. Что ж, теперь, когда его мечта сбылась, наверное ко мне он будет захаживать пореже.»"
            $ GeorgettVar["TellAboutEddieMomSex"] = 1
        else:
            $ MainTxt = "Вы рассказываете Жоржетте про сальные взгляды, которые бросает Эдди каждый раз, когда подозревает, что его мамаша позволяет вам какие-нибудь вольности. Жоржетта не остается в долгу и в свою очередь со смехом рассказывает вам, что когда Эдди ее снимает, он просит, чтобы она изображала его маму.\nОтсмеявшись, она предлагает вам разнообразить половую жизнь Эдди, зайдя к нему домой. Вы соглашаетесь."
            $ BeckyVar["EddieGeorg"] = 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "sponsor_eddie_home":
        if BeckyVar.get("EddieGeorg", 0) == 1:
            $ MainTxt = "Вы вручаете Жоржетте 25 мараведи и говорите, что очень бы хотели посмотреть на то, как она займется любовью с Эдди на глазах у Бекки."
            $ money -= 25
        elif BeckyVar.get("EddieGeorg", 0) == 2 and BeckyVar.get("visitedhome", 0) == 5:
            $ MainTxt = "Вы вручаете Жоржетте 10 мараведи и говорите, что хотите повторения."
            $ money -= 10
        else:
            $ MainTxt = "Вы вручаете Жоржетте 10 мараведи и говорите, что хотели бы еще раз посмотреть на выражение лица вдовы Блэнкеншип."
            $ money -= 10
        $ MainTxt += "\n\nЖоржетта с радостью берет деньги и заверяет вас, что при встрече c Эдди непременно предложит ему навестить его у него дома за ужином."
        $ BeckyVar["EddieWhoreHome"] = 1
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        call stat
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_eddie_visit":
        $ MainTxt = "«Эй, Жоржи, наш друг Эдди к тебе случаем не захаживал?» - осведомляетесь вы у своей работницы."
        if BeckyVar.get("EddieWhoreHome", 0) <= 1:
            if BeckyVar.get("visitedhome", 0) >= 7:
                $ MainTxt += "\n\n«Не, он говорит что теперь с мамкой своей все больше перепихивается, а на мне экономит.»"
            else:
                $ MainTxt += "\n\n«Не, сегодня его не было. Может завтра зайдет.»"
        else:
            $ MainTxt += "\n\n«Заходил.»"
            if BeckyVar.get("EddieGeorg", 0) == 1:
                if BeckyVar.get("EddieWhoreHome", 0) == 4:
                    if BeckyVar.get("visitedhome", 0) >= 7:
                        $ MainTxt += "\n\n«Согласился, говорит что пусть его мамашка посмотрит, поучится, разогреется.»"
                    else:
                        $ MainTxt += "\n\n«Пришел в восторг от моего предложения, сказал чтобы сегодня я к нему домой на огонек заглянула.»"
                    $ MainTxt += "\n\n«Так что если хочешь посмотреть - заглядывай и ты к вдове на огонек.»"
                else:
                    $ MainTxt += "\n\n«Отказался.»"
                    if BeckyVar.get("visitedhome", 0) < 5:
                        $ MainTxt += "\n\n«Объяснил, сказал что мамашка его больно строгая, вышвырнет его за такие шутки.»"
                    elif EddieVar.get("SawMomSex", 0) == 0 or BeckyVar.get("HomeSex", 0) == 0:
                        $ MainTxt += "\n\n«Объяснил, сказал что хоть мама и разрешила всем детям водить своих любовников домой, но он все-таки еще стесняется, не хочет быть первым.»"
                    elif BeckyVar.get("EddieWhoreHome", 0) == 2:
                        $ MainTxt += "\n\n«Объяснил, сказал что идея хорошая, только вот больно дорого я с него запросила, нету у него столько.»"
                    else:
                        $ MainTxt += "\n\n«Объяснил, сказал что в другой раз такое замутим, но сейчас ему мол нет мочи терпеть, так что он сразу отымел меня и ушел.»"
            else:
                if BeckyVar.get("EddieWhoreHome", 0) == 4:
                    $ MainTxt += "\n\n«Согласился, конечно. Говорит прошлый раз было здорово, надо повторить. Сказал чтобы сегодня я к нему домой на огонек заглянула. Так что если хочешь посмотреть - заглядывай и ты к вдовушке на огонек.»"
                else:
                    $ MainTxt += "\n\n«Отказался, сказал что ему прямо сейчас хочется, мол нет мочи терпеть.»"
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "hire":
        if girl_loc == "tavern":
            $ money -= 4
            call SexProstTavern(1, "georgett")
        else:
            $ money -= 8
            call SexPort(1, "georgett")
        return

    if str(choice_code or "") == "grope":
        $ _grope_result = georgett_grope_outcome(girl_name, girl_loc)
        $ MainTxt = str(_grope_result.get("text", "") or "")
        $ CurLocDesc = MainTxt
        if bool(_grope_result.get("show_current_sex", False)):
            $ GirlLocIGSS = girl_loc
            call ShowCurrentSex(girl_name)
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_dad":
        $ MainTxt = DaddyAskBuildPhrase(girl_name)
        $ Talked[girl_name] = Talked.get(girl_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "dress":
        call IntGeorgettDressChange(girl_name)
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    call IntGeorgettTalkRestore(girl_loc)
    return


label IntGeorgettTalkRestore(girl_loc="street"):
    if str(girl_loc or "") == "street":
        jump PortStreets
    elif str(girl_loc or "") == "tavern":
        jump TavernMain
    $ main_ui_end_talk_state()
    return
