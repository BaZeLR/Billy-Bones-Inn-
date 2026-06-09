# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def liza_talk_resolve_location(girl_loc_ilt=""):
        if str(girl_loc_ilt or ""):
            return str(girl_loc_ilt or "")
        if CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "TavernMain":
            return "tavern"
        if CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "PortStreets":
            return "street"
        if str(CurLoc or "") == "TavernMain":
            return "tavern"
        return "street"

    def liza_talk_prepare_state(girl_name_ilt="liza", girl_loc_ilt=""):
        girl_name = str(girl_name_ilt or Liza.code_name)
        girl_loc = liza_talk_resolve_location(girl_loc_ilt)
        if girl_name == Liza.code_name:
            Liza.sync_from_liza_maps()
        return girl_name, girl_loc


label IntLizaTalk(girl_name_ilt="liza", girl_loc_ilt=""):
    python:
        GirlNameILT, GirlLocILT = liza_talk_prepare_state(girl_name_ilt, girl_loc_ilt)

    $ main_ui_begin_talk_state("Разговор с Лизеттой", GirlNameILT)
    $ current_action_title = "Разговор с Лизеттой"
    $ current_action_content = None
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Лизетта смотрит на вас с живым любопытством, явно ожидая, о чем вы заговорите."
        $ CurLocDesc = MainTxt
    call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
    return


label IntLizaTalkRefresh(girl_name_ilt="liza", girl_loc_ilt=""):
    python:
        GirlNameILT, GirlLocILT = liza_talk_prepare_state(girl_name_ilt, girl_loc_ilt)

    $ main_ui_begin_talk_state("Разговор с Лизеттой", GirlNameILT)
    $ current_action_title = "Разговор с Лизеттой"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, GirlNameILT, CurLoc)))
    $ current_action_items.append(MenuItem("Болтать", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "smalltalk")))

    if Liza.can_ask_topic("clients"):
        $ current_action_items.append(MenuItem("Спросить о клиентах", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "ask_clients")))

    if Liza.can_ask_topic("sex"):
        $ current_action_items.append(MenuItem("Спросить о сексе", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "ask_sex")))
        $ current_action_items.append(MenuItem("Спросить о беременности", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "ask_pregnancy")))

    if Liza.can_ask_topic("georgett_gerhard"):
        $ current_action_items.append(MenuItem("Рассказать про ее мать и отца Герхарда", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "tell_georgett_gerhard")))

    if Liza.can_ask_topic("work"):
        $ current_action_items.append(MenuItem("Спросить как работается у вас в трактире", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "ask_work")))

    if Liza.can_ask_topic("holglor"):
        $ current_action_items.append(MenuItem("Спросить о таинственном \"Холглоре\" в \"Пьяном Пирате\"", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "ask_holglor")))

    if (money >= 8 or (money >= 4 and GirlLocILT == "tavern")) and cametoday < cancumdaily:
        $ current_action_items.append(MenuItem("Снять", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "hire")))

    $ current_action_items.append(MenuItem("Лапать", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "grope")))

    if Liza.can_talk_today() and Liza.rel >= 8 and int(Liza.stats.get("pregnancy", 0) or 0) >= 120:
        $ current_action_items.append(MenuItem("Поинтересоваться, знает ли она кто ей ребенка заделал", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "ask_dad")))

    if GirlLocILT == "tavern":
        $ current_action_items.append(MenuItem("Обсудить одежду", Function(main_ui_call_label, "IntLizaTalkApply", GirlNameILT, GirlLocILT, "dress")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntLizaTalkApply(girl_name_ilt="liza", girl_loc_ilt="", choice_code=""):
    python:
        GirlNameILT, GirlLocILT = liza_talk_prepare_state(girl_name_ilt, girl_loc_ilt)

    if str(choice_code or "") == "smalltalk":
        $ MainTxt = "Вы некоторое время болтаете с Лизеттой о разных вещах."
        python:
            if Talked.get(GirlNameILT, 0) <= 2 and renpy.random.randint(1, 2) == 1:
                girl_friends = Liza.rel
                lick_pussy_count = LickPussy.get(GirlNameILT, 0)
                give_orgasms_count = GiveOrgasms.get(GirlNameILT, 0)

                if (
                    girl_friends < 3
                    or (lick_pussy_count >= 7 and girl_friends < 4)
                    or (
                        give_orgasms_count >= 3
                        and lick_pussy_count >= 7
                        and girl_friends < 5
                    )
                ):
                    MainTxt = str(MainTxt or "") + "\n\nВы чуть лучше узнали Лизетту."
                    Liza.add_relation(1)
                elif girl_friends < 5:
                    MainTxt = str(MainTxt or "") + "\n\nИз уклончивых ответов девушки вы поняли, что она вам еще мало доверяет. Может, если бы вы узнали ее получше или доставили ей приятное, она бы с вами поделилась еще чем-то."

            if Talked.get(GirlNameILT, 0) > 2:
                MainTxt = str(MainTxt or "") + "\n\nНичего нового из разговора вы не узнали."

            Liza.finish_talk()
        $ CurLocDesc = MainTxt
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "ask_clients":
        $ MainTxt = "«За вечер меня хотят обычно три-четыре дяденьки. С некоторыми очень хорошо бывает, пока он закончит успеваешь сама спустить, а порой и несколько раз. А некоторые дяденьки так быстро заканчивают, что только начинаешь входить в охотку, а он уже все», - говорит Лизетта, автоматически поглаживая промежность сквозь юбку."
        if Liza.corruption < 50 and int(Liza.stats.get("pregnancy", 0) or 0) < 120:
            $ MainTxt = str(MainTxt or "") + "\n\n«Только вот как не прошу я их чтобы внутрь не спускали, а они почти все либо делают вид что не слышат, либо отвечают, что платят деньги и спускают куда хотят. И в моей бедной киске теперь постоянно сперма хлюпает. А я не хочу залететь!» - добавляет Лизетта."
        elif int(Liza.stats.get("pregnancy", 0) or 0) >= 120:
            $ MainTxt = str(MainTxt or "") + "\n\n«Только вот как не просила я дяденек не спускать в меня, никто меня не слушал и теперь я залетела», - грустно добавляет Лизетта, проводя рукой по своему округлившемуся животику."
        if Liza.mark_asked_topic("askclients"):
            $ MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."
        $ Liza.finish_talk()
        $ CurLocDesc = MainTxt
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "ask_sex":
        $ MainTxt = "«Ох, нравится мне трахаться! Маменька рассказывала как это хорошо, да и сама я за маменькой подсматривала, и за бабушкой, и за тетями моими и за дядями. Так что как мальчишки соседские начали мне под юбку лезть, то я сразу ножки и раздвинула. И не пожалела. А сейчас, как с мамочкой работать вместе начала, сладко мне каждый день бывает!» - говорит Лизетта."
        if Liza.mark_asked_topic("asksex"):
            $ MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."
        $ Liza.finish_talk()
        $ CurLocDesc = MainTxt
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "ask_pregnancy":
        python:
            if Liza.corruption < 50 and int(Liza.stats.get("pregnancy", 0) or 0) < 120 and int(Liza.stats.get("kids", 0) or 0) > 0:
                MainTxt = "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Ребеночка мне уже заделали, скоро такими темпами еще будет!» - говорит Лизетта."
            elif Liza.corruption < 50 and int(Liza.stats.get("pregnancy", 0) or 0) < 120:
                MainTxt = "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Мамочка говорит что я ее скоро бабушкой сделаю, а я не хочу, я еще слишком молодая!» - говорит Лизетта."
            elif int(Liza.stats.get("pregnancy", 0) or 0) >= 120:
                MainTxt = "«Эх, баловалась я, баловалась вот и добаловалась - залетела. Столько меня имели, что теперь и предположить от кого - сложно.» - говорит Лизетта, проводя рукой по своему округлившемуся животику."
            else:
                MainTxt = "«Маменька говорит, что любишь гулять - непременно пузо нагуляешь. А я гулять люблю, без чьего-нибудь колышка у себя в серединке и дня прожить трудно. Так что чему быть - того не миновать», - философски замечает Лизетта."

            if Liza.mark_asked_topic("askpregnancy"):
                MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."

            Liza.finish_talk()
            CurLocDesc = MainTxt
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "tell_georgett_gerhard":
        $ MainTxt = "Вы рассказываете Лизетте что вы видели как отец Герхард трахал ее мамочку после воскресной службы.\n\n«Ух мама, и ты тоже с падре перепихнулась! Но я-то помоложе буду, я докажу отцу Герхарду что я лучшая любовница и больше достойна благословления Ильматера!» - отвечает Лизетта."
        if Liza.mark_asked_topic("TalkChurchAfterCermonGeorgett"):
            $ MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."
        $ Liza.finish_talk()
        $ CurLocDesc = MainTxt
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "ask_work":
        $ MainTxt = "Вы спрашиваете Лизетту как ей работается у вас в трактире."
        if TavernGloryHole == 2:
            $ MainTxt = str(MainTxt or "") + "\n\n«Ой, - отвечает она, - здесь так здорово! Мне все нравится. А теперь еще и этот, холгло.., тьфу, в смысле глорихол есть! Все круто, куда круче чем на улице!»"
        elif int(Liza.story_value("GloryHoleAsked", 0) or 0) == 1:
            $ MainTxt = str(MainTxt or "") + "\n\n«Ой, - отвечает она, - здесь так здорово! Мне все нравится!»"
        else:
            $ MainTxt = str(MainTxt or "") + "\n\n«Ой, - отвечает она, - здесь так здорово! Мне все нравится. Правда мама говорила, что когда она подрабатывала в Пьяном Пирате, там была какая-то штука, не помню как называется. Холглор или еще как-то так. А у вас ее нет.»"
        $ Liza.mark_asked_topic("GloryHoleMentioned", 0)
        $ Liza.finish_talk()
        $ CurLocDesc = MainTxt
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "ask_holglor":
        $ MainTxt = "Вы просите Лизетту рассказать вам больше.\n\n«Мама говорила что это такая ширмочка с дыркой, в которую дяденьки суют свои штуки, - рассказывает вам девчонка. - А мама с другой стороны их отсасывает. Ну или, если в охотку, писечкой насаживается. И никто никого не видит!»"
        $ Liza.mark_asked_topic("GloryHoleAsked", 0)
        $ Liza.finish_talk()
        $ CurLocDesc = MainTxt
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "hire":
        if GirlLocILT == "tavern":
            $ money -= 4
            call SexProstTavern(1, "liza")
        else:
            $ money -= 8
            call SexPort(1, "liza")
        return

    if str(choice_code or "") == "grope":
        python:
            if Liza.rel >= 5:
                MainTxt = "Вы начали гладить маленькие сисечки %s через тонкую ткань ее блузки." % RealName2.get(GirlNameILT, GirlNameILT)
                if panties.get(GirlNameILT, ""):
                    MainTxt += "\n\nВы сунули руку под платьичко вашей подружки и начали натирать ее киску сквозь панталончики."
                else:
                    MainTxt += "\n\nВы сунули руку под короткое платьичко вашей любовницы и стали наминать ее юную вульвочку."

                if not panties.get(GirlNameILT, ""):
                    if CumInsideYou.get(GirlNameILT, 0) > 0:
                        MainTxt += "\n\nВы почувствовали свою сперму в пещерке %s." % RealName2.get(GirlNameILT, GirlNameILT)
                    elif CumInsideOthers.get(GirlNameILT, 0) > 0:
                        MainTxt += "\n\nВаши пальцы заскользили по пещерке %s, похоже кто-то уже кончил в нее." % RealName2.get(GirlNameILT, GirlNameILT)
            else:
                MainTxt = "«Эй, дяденка, не так быстро!» останавливает вас %s. «Мамочка говорит, что ты сначала заплатить должен, а потом уже лапать!»" % RealName.get(GirlNameILT, GirlNameILT)
            CurLocDesc = MainTxt
        call ShowCurrentSex(GirlNameILT)
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "ask_dad":
        $ MainTxt = str(DaddyAskBuildPhrase(GirlNameILT) or "")
        $ CurLocDesc = MainTxt
        $ Liza.finish_talk()
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    if str(choice_code or "") == "dress":
        call IntLizaDressChange(GirlNameILT)
        call IntLizaTalkRefresh(GirlNameILT, GirlLocILT)
        return

    $ main_ui_end_talk_state()
    return
