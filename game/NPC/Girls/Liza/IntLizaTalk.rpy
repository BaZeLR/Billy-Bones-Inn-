label IntLizaTalkDress(girl_name_ilt="liza", girl_loc_ilt=""):
    call IntLizaDressChange(girl_name_ilt)
    call IntLizaTalkMenu(GirlNameILT, GirlLocILT)
    return

label IntLizaTalkDress(girl_name_ilt="liza", girl_loc_ilt=""):
    call IntLizaDressChange(girl_name_ilt)
    returnlabel IntLizaTalkDress(girl_name_ilt="liza", girl_loc_ilt=""):
    call IntLizaDressChange(girl_name_ilt)
    call IntLizaTalkMenu(GirlNameILT, GirlLocILT)
    return

label IntLizaTalkDress(girl_name_ilt="liza", girl_loc_ilt=""):
    call IntLizaDressChange(girl_name_ilt)
    returnlabel IntLizaTalkDress(girl_name_ilt="liza", girl_loc_ilt=""):
    call IntLizaDressChange(girl_name_ilt)
    call IntLizaTalkMenu(GirlNameILT, GirlLocILT)
    return

label IntLizaTalkDress(girl_name_ilt="liza", girl_loc_ilt=""):
    call IntLizaDressChange(girl_name_ilt)
    return# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntLizaTalk(girl_name_ilt="liza", girl_loc_ilt=""):
    $ GirlNameILT = str(girl_name_ilt or Liza.code_name)
    if girl_loc_ilt:
        $ GirlLocILT = str(girl_loc_ilt)
    elif str(CurLoc or "") == "TavernMain":
        $ GirlLocILT = "tavern"
    else:
        $ GirlLocILT = "street"
    $ main_ui_begin_talk_state("Разговор с Лизеттой", GirlNameILT)
    if str(MainTxt or "").strip() == "":
        $ MainTxt = "Лизетта смотрит на вас с живым любопытством, явно ожидая, о чем вы заговорите."
        $ CurLocDesc = MainTxt
    call IntLizaTalkMenu(GirlNameILT, GirlLocILT)
    return


label IntLizaTalkMenu:
    menu:
            "Осмотреть":
                $ NpcActionLookState(GirlNameILT, CurLoc)
            "Болтать":
                call IntLizaTalkSmalltalk(GirlNameILT, GirlLocILT)
            "Спросить о клиентах" if Liza.can_ask_topic("clients"):
                call IntLizaTalkAskClients(GirlNameILT, GirlLocILT)
            "Спросить о сексе" if Liza.can_ask_topic("sex"):
                call IntLizaTalkAskSex(GirlNameILT, GirlLocILT)
            "Спросить о беременности" if Liza.can_ask_topic("sex"):
                call IntLizaTalkAskPregnancy(GirlNameILT, GirlLocILT)
            "Рассказать про ее мать и отца Герхарда" if Liza.can_ask_topic("georgett_gerhard"):
                call IntLizaTalkTellGeorgettGerhard(GirlNameILT, GirlLocILT)
            "Спросить как работается у вас в трактире" if Liza.can_ask_topic("work"):
                call IntLizaTalkAskWork(GirlNameILT, GirlLocILT)
            "Спросить о таинственном 'Холглоре' в 'Пьяном Пирате'" if Liza.can_ask_topic("holglor"):
                call IntLizaTalkAskHolglor(GirlNameILT, GirlLocILT)
            "Снять" if (player.economy.money >= 8 or (player.economy.money >= 4 and GirlLocILT == "tavern")) and player.intimacy.came_today < player.intimacy.can_cum_daily:
                call IntLizaTalkHire(GirlNameILT, GirlLocILT)
            "Лапать":
                call IntLizaTalkGrope(GirlNameILT, GirlLocILT)
            "Поинтересоваться, знает ли она кто ей ребенка заделал" if Liza.can_talk_today() and Liza.rel >= 8 and Liza.pregnancy_days() >= 120:
                call IntLizaTalkAskDad(GirlNameILT, GirlLocILT)
            "Обсудить одежду" if GirlLocILT == "tavern":
                call IntLizaTalkDress(GirlNameILT, GirlLocILT)
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return
    return


label IntLizaTalkSmalltalk(girl_name_ilt="liza", girl_loc_ilt=""):
    python:
        MainTxt = "Вы некоторое время болтаете с Лизеттой о разных вещах."
        if Liza.talk_count() <= 2 and procedural_randint(1, 2, key="procedural:NPC/Girls/Liza/IntLizaTalk.rpy:procedural_randint:86:1") == 1:
            girl_friends = Liza.rel
            lick_pussy_count = Liza.lick_pussy_count()
            give_orgasms_count = Liza.sex_stat("orgasms_given", 0)

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

        if Liza.talk_count() > 2:
            MainTxt = str(MainTxt or "") + "\n\nНичего нового из разговора вы не узнали."

        Liza.finish_talk()
    $ CurLocDesc = MainTxt
    return


label IntLizaTalkAskClients(girl_name_ilt="liza", girl_loc_ilt=""):
    $ MainTxt = "«За вечер меня хотят обычно три-четыре дяденьки. С некоторыми очень хорошо бывает, пока он закончит успеваешь сама спустить, а порой и несколько раз. А некоторые дяденьки так быстро заканчивают, что только начинаешь входить в охотку, а он уже все», - говорит Лизетта, автоматически поглаживая промежность сквозь юбку."
    if Liza.corruption < 50 and Liza.pregnancy_days() < 120:
        $ MainTxt = str(MainTxt or "") + "\n\n«Только вот как не прошу я их чтобы внутрь не спускали, а они почти все либо делают вид что не слышат, либо отвечают, что платят деньги и спускают куда хотят. И в моей бедной киске теперь постоянно сперма хлюпает. А я не хочу залететь!» - добавляет Лизетта."
    elif Liza.pregnancy_days() >= 120:
        $ MainTxt = str(MainTxt or "") + "\n\n«Только вот как не просила я дяденек не спускать в меня, никто меня не слушал и теперь я залетела», - грустно добавляет Лизетта, проводя рукой по своему округлившемуся животику."
    if Liza.mark_asked_topic("askclients"):
        $ MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."
    $ Liza.finish_talk()
    $ CurLocDesc = MainTxt
    return


label IntLizaTalkAskSex(girl_name_ilt="liza", girl_loc_ilt=""):
    $ MainTxt = "«Ох, нравится мне трахаться! Маменька рассказывала как это хорошо, да и сама я за маменькой подсматривала, и за бабушкой, и за тетями моими и за дядями. Так что как мальчишки соседские начали мне под юбку лезть, то я сразу ножки и раздвинула. И не пожалела. А сейчас, как с мамочкой работать вместе начала, сладко мне каждый день бывает!» - говорит Лизетта."
    if Liza.mark_asked_topic("asksex"):
        $ MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."
    $ Liza.finish_talk()
    $ CurLocDesc = MainTxt
    return


label IntLizaTalkAskPregnancy(girl_name_ilt="liza", girl_loc_ilt=""):
    python:
        if Liza.corruption < 50 and Liza.pregnancy_days() < 120 and int(Liza.stats.get("kids", 0) or 0) > 0:
            MainTxt = "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Ребеночка мне уже заделали, скоро такими темпами еще будет!» - говорит Лизетта."
        elif Liza.corruption < 50 and Liza.pregnancy_days() < 120:
            MainTxt = "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Мамочка говорит что я ее скоро бабушкой сделаю, а я не хочу, я еще слишком молодая!» - говорит Лизетта."
        elif Liza.pregnancy_days() >= 120:
            MainTxt = "«Эх, баловалась я, баловалась вот и добаловалась - залетела. Столько меня имели, что теперь и предположить от кого - сложно.» - говорит Лизетта, проводя рукой по своему округлившемуся животику."
        else:
            MainTxt = "«Маменька говорит, что любишь гулять - непременно пузо нагуляешь. А я гулять люблю, без чьего-нибудь колышка у себя в серединке и дня прожить трудно. Так что чему быть - того не миновать», - философски замечает Лизетта."

        if Liza.mark_asked_topic("askpregnancy"):
            MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."

        Liza.finish_talk()
        CurLocDesc = MainTxt
    return


label IntLizaTalkTellGeorgettGerhard(girl_name_ilt="liza", girl_loc_ilt=""):
    $ MainTxt = "Вы рассказываете Лизетте что вы видели как отец Герхард трахал ее мамочку после воскресной службы.\n\n«Ух мама, и ты тоже с падре перепихнулась! Но я-то помоложе буду, я докажу отцу Герхарду что я лучшая любовница и больше достойна благословления Ильматера!» - отвечает Лизетта."
    if Liza.mark_asked_topic("TalkChurchAfterCermonGeorgett"):
        $ MainTxt = str(MainTxt or "") + "\n\nВас немного возбудил рассказ Лизетты."
    $ Liza.finish_talk()
    $ CurLocDesc = MainTxt
    return


label IntLizaTalkAskWork(girl_name_ilt="liza", girl_loc_ilt=""):
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
    return


label IntLizaTalkAskHolglor(girl_name_ilt="liza", girl_loc_ilt=""):
    $ MainTxt = "Вы просите Лизетту рассказать вам больше.\n\n«Мама говорила что это такая ширмочка с дыркой, в которую дяденьки суют свои штуки, - рассказывает вам девчонка. - А мама с другой стороны их отсасывает. Ну или, если в охотку, писечкой насаживается. И никто никого не видит!»"
    $ Liza.mark_asked_topic("GloryHoleAsked", 0)
    $ Liza.finish_talk()
    $ CurLocDesc = MainTxt
    return


label IntLizaTalkHire(girl_name_ilt="liza", girl_loc_ilt=""):
    if girl_loc_ilt == "tavern":
        $ money -= 4
        call SexProstTavern(1, "liza")
    else:
        $ money -= 8
        call SexPort(1, "liza")
    return


label IntLizaTalkGrope(girl_name_ilt="liza", girl_loc_ilt=""):
    python:
        _liza_name = Liza.data.fullname
        _liza_name2 = Liza.data.genitive
        if Liza.rel >= 5:
            MainTxt = "Вы начали гладить маленькие сисечки %s через тонкую ткань ее блузки." % _liza_name2
            if Liza.current_underwear("panties", ""):
                MainTxt += "\n\nВы сунули руку под платьичко вашей подружки и начали натирать ее киску сквозь панталончики."
            else:
                MainTxt += "\n\nВы сунули руку под короткое платьичко вашей любовницы и стали наминать ее юную вульвочку."

            if not Liza.current_underwear("panties", ""):
                if Liza.cum_state("cum_inside_you") > 0:
                    MainTxt += "\n\nВы почувствовали свою сперму в пещерке %s." % _liza_name2
                elif Liza.cum_state("cum_inside_others") > 0:
                    MainTxt += "\n\nВаши пальцы заскользили по пещерке %s, похоже кто-то уже кончил в нее." % _liza_name2
        else:
            MainTxt = "«Эй, дяденка, не так быстро!» останавливает вас %s. «Мамочка говорит, что ты сначала заплатить должен, а потом уже лапать!»" % _liza_name
        CurLocDesc = MainTxt
    call ShowCurrentSex(girl_name_ilt)
    return


label IntLizaTalkAskDad(girl_name_ilt="liza", girl_loc_ilt=""):
    $ MainTxt = str(DaddyAskBuildPhrase(girl_name_ilt) or "")
    $ CurLocDesc = MainTxt
    $ Liza.finish_talk()
    return


