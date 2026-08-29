# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
label IntLizaTalk(girl_name_ilt="liza", girl_loc_ilt=""):
    $ renpy.dynamic("_liza_talk_new")
    $ girl_name_ilt = str(girl_name_ilt or Liza.code_name)
    if girl_loc_ilt:
        $ girl_loc_ilt = str(girl_loc_ilt)
    elif str(rooms.current_code or "") == "TavernMain":
        $ girl_loc_ilt = "tavern"
    else:
        $ girl_loc_ilt = "street"
    $ _liza_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != str(girl_name_ilt or "liza").strip().lower()
    $ main_ui_begin_talk_state("Разговор с Лизеттой", girl_name_ilt)
    if _liza_talk_new:
        $ scene_runtime.text = "Лизетта смотрит на вас с живым любопытством, явно ожидая, о чем вы заговорите."
        $ scene_runtime.location_text = scene_runtime.text

    while True:
        menu:
            "Осмотреть":
                call ShowGirlCard(girl_name_ilt)
            "Болтать":
                call IntLizaTalkSmalltalk(girl_name_ilt, girl_loc_ilt)
            "Спросить о клиентах" if Liza.can_ask_topic("clients"):
                call IntLizaTalkAskClients(girl_name_ilt, girl_loc_ilt)
            "Спросить о сексе" if Liza.can_ask_topic("sex"):
                call IntLizaTalkAskSex(girl_name_ilt, girl_loc_ilt)
            "Спросить о беременности" if Liza.can_ask_topic("sex"):
                call IntLizaTalkAskPregnancy(girl_name_ilt, girl_loc_ilt)
            "Рассказать про ее мать и отца Герхарда" if Liza.can_ask_topic("georgett_gerhard"):
                call IntLizaTalkTellGeorgettGerhard(girl_name_ilt, girl_loc_ilt)
            "Спросить как работается у вас в трактире" if Liza.can_ask_topic("work"):
                call IntLizaTalkAskWork(girl_name_ilt, girl_loc_ilt)
            "Спросить о таинственном 'Холглоре' в 'Пьяном Пирате'" if Liza.can_ask_topic("holglor"):
                call IntLizaTalkAskHolglor(girl_name_ilt, girl_loc_ilt)
            "Снять" if (player.economy.money >= 8 or (player.economy.money >= 4 and girl_loc_ilt == "tavern")) and player.intimacy.came_today < player.intimacy.can_cum_daily:
                call IntLizaTalkHire(girl_name_ilt, girl_loc_ilt)
            "Лапать":
                call IntLizaTalkGrope(girl_name_ilt, girl_loc_ilt)
            "Поинтересоваться, знает ли она кто ей ребенка заделал" if Liza.can_talk_today() and Liza.rel >= 8 and Liza.pregnancy_days() >= 120:
                call IntLizaTalkAskDad(girl_name_ilt, girl_loc_ilt)
            "Обсудить одежду" if girl_loc_ilt == "tavern":
                call IntLizaDressChange(girl_name_ilt)
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return
        if str(main_ui_runtime.mode or "") != "talk":
            return


label IntLizaTalkSmalltalk(girl_name_ilt="liza", girl_loc_ilt="", _liza_busy_text=""):
    $ renpy.dynamic("girl_friends", "give_orgasms_count", "lick_pussy_count")
    $ _liza_busy_text = Liza.interrupt_work()
    if _liza_busy_text:
        $ scene_runtime.text = _liza_busy_text
        $ scene_runtime.location_text = scene_runtime.text
        return
    python:
        scene_runtime.text = "Вы некоторое время болтаете с Лизеттой о разных вещах."
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
                scene_runtime.text = str(scene_runtime.text or "") + "\n\nВы чуть лучше узнали Лизетту."
                Liza.add_relation(1)
            elif girl_friends < 5:
                scene_runtime.text = str(scene_runtime.text or "") + "\n\nИз уклончивых ответов девушки вы поняли, что она вам еще мало доверяет. Может, если бы вы узнали ее получше или доставили ей приятное, она бы с вами поделилась еще чем-то."

        if Liza.talk_count() > 2:
            scene_runtime.text = str(scene_runtime.text or "") + "\n\nНичего нового из разговора вы не узнали."

        Liza.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntLizaTalkAskClients(girl_name_ilt="liza", girl_loc_ilt=""):
    $ scene_runtime.text = "«За вечер меня хотят обычно три-четыре дяденьки. С некоторыми очень хорошо бывает, пока он закончит успеваешь сама спустить, а порой и несколько раз. А некоторые дяденьки так быстро заканчивают, что только начинаешь входить в охотку, а он уже все», - говорит Лизетта, автоматически поглаживая промежность сквозь юбку."
    if Liza.corruption < 50 and Liza.pregnancy_days() < 120:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n«Только вот как не прошу я их чтобы внутрь не спускали, а они почти все либо делают вид что не слышат, либо отвечают, что платят деньги и спускают куда хотят. И в моей бедной киске теперь постоянно сперма хлюпает. А я не хочу залететь!» - добавляет Лизетта."
    elif Liza.pregnancy_days() >= 120:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n«Только вот как не просила я дяденек не спускать в меня, никто меня не слушал и теперь я залетела», - грустно добавляет Лизетта, проводя рукой по своему округлившемуся животику."
    if not Liza.asked_about_clients:
        $ Liza.asked_about_clients = True
        $ Liza.add_relation(1)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВас немного возбудил рассказ Лизетты."
    $ Liza.mark_asked()
    $ Liza.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntLizaTalkAskSex(girl_name_ilt="liza", girl_loc_ilt=""):
    $ scene_runtime.text = "«Ох, нравится мне трахаться! Маменька рассказывала как это хорошо, да и сама я за маменькой подсматривала, и за бабушкой, и за тетями моими и за дядями. Так что как мальчишки соседские начали мне под юбку лезть, то я сразу ножки и раздвинула. И не пожалела. А сейчас, как с мамочкой работать вместе начала, сладко мне каждый день бывает!» - говорит Лизетта."
    if not Liza.asked_about_sex:
        $ Liza.asked_about_sex = True
        $ Liza.add_relation(1)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВас немного возбудил рассказ Лизетты."
    $ Liza.mark_asked()
    $ Liza.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntLizaTalkAskPregnancy(girl_name_ilt="liza", girl_loc_ilt=""):
    python:
        if Liza.corruption < 50 and Liza.pregnancy_days() < 120 and int(Liza.stats.get("kids", 0) or 0) > 0:
            scene_runtime.text = "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Ребеночка мне уже заделали, скоро такими темпами еще будет!» - говорит Лизетта."
        elif Liza.corruption < 50 and Liza.pregnancy_days() < 120:
            scene_runtime.text = "«Эх, как я не прошу дяденек чтобы в серединку мне не спускали, а они все равно! Все время во мне семя чье-то! Мамочка говорит что я ее скоро бабушкой сделаю, а я не хочу, я еще слишком молодая!» - говорит Лизетта."
        elif Liza.pregnancy_days() >= 120:
            scene_runtime.text = "«Эх, баловалась я, баловалась вот и добаловалась - залетела. Столько меня имели, что теперь и предположить от кого - сложно.» - говорит Лизетта, проводя рукой по своему округлившемуся животику."
        else:
            scene_runtime.text = "«Маменька говорит, что любишь гулять - непременно пузо нагуляешь. А я гулять люблю, без чьего-нибудь колышка у себя в серединке и дня прожить трудно. Так что чему быть - того не миновать», - философски замечает Лизетта."

        if not Liza.asked_about_pregnancy:
            Liza.asked_about_pregnancy = True
            Liza.add_relation(1)
            scene_runtime.text = str(scene_runtime.text or "") + "\n\nВас немного возбудил рассказ Лизетты."

        Liza.mark_asked()
        Liza.finish_talk()
        scene_runtime.location_text = scene_runtime.text
    return


label IntLizaTalkTellGeorgettGerhard(girl_name_ilt="liza", girl_loc_ilt=""):
    $ scene_runtime.text = "Вы рассказываете Лизетте что вы видели как отец Герхард трахал ее мамочку после воскресной службы.\n\n«Ух мама, и ты тоже с падре перепихнулась! Но я-то помоложе буду, я докажу отцу Герхарду что я лучшая любовница и больше достойна благословления Ильматера!» - отвечает Лизетта."
    if not Liza.discussed_georgett_gerhard:
        $ Liza.discussed_georgett_gerhard = True
        $ Liza.add_relation(1)
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\nВас немного возбудил рассказ Лизетты."
    $ Liza.mark_asked()
    $ Liza.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntLizaTalkAskWork(girl_name_ilt="liza", girl_loc_ilt=""):
    $ scene_runtime.text = "Вы спрашиваете Лизетту как ей работается у вас в трактире."
    if player.tavern_management.glory_hole == 2:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n«Ой, - отвечает она, - здесь так здорово! Мне все нравится. А теперь еще и этот, холгло.., тьфу, в смысле глорихол есть! Все круто, куда круче чем на улице!»"
    elif Liza.glory_hole_asked:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n«Ой, - отвечает она, - здесь так здорово! Мне все нравится!»"
    else:
        $ scene_runtime.text = str(scene_runtime.text or "") + "\n\n«Ой, - отвечает она, - здесь так здорово! Мне все нравится. Правда мама говорила, что когда она подрабатывала в Пьяном Пирате, там была какая-то штука, не помню как называется. Холглор или еще как-то так. А у вас ее нет.»"
    $ Liza.glory_hole_mentioned = True
    $ Liza.mark_asked()
    $ Liza.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntLizaTalkAskHolglor(girl_name_ilt="liza", girl_loc_ilt=""):
    $ scene_runtime.text = "Вы просите Лизетту рассказать вам больше.\n\n«Мама говорила что это такая ширмочка с дыркой, в которую дяденьки суют свои штуки, - рассказывает вам девчонка. - А мама с другой стороны их отсасывает. Ну или, если в охотку, писечкой насаживается. И никто никого не видит!»"
    $ Liza.glory_hole_asked = True
    $ Liza.mark_asked()
    $ Liza.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntLizaTalkHire(girl_name_ilt="liza", girl_loc_ilt=""):
    if girl_loc_ilt == "tavern":
        $ player.spend_money(4)
        call SexProstTavern(1, "liza")
    else:
        $ player.spend_money(8)
        call SexPort(1, "liza")
    return


label IntLizaTalkGrope(girl_name_ilt="liza", girl_loc_ilt=""):
    $ renpy.dynamic("_liza_name", "_liza_name2")
    python:
        _liza_name = Liza.data.fullname
        _liza_name2 = Liza.data.genitive
        if Liza.rel >= 5:
            scene_runtime.text = "Вы начали гладить маленькие сисечки %s через тонкую ткань ее блузки." % _liza_name2
            if Liza.current_underwear("panties", ""):
                scene_runtime.text += "\n\nВы сунули руку под платьичко вашей подружки и начали натирать ее киску сквозь панталончики."
            else:
                scene_runtime.text += "\n\nВы сунули руку под короткое платьичко вашей любовницы и стали наминать ее юную вульвочку."

            if not Liza.current_underwear("panties", ""):
                if Liza.cum_state("cum_inside_you") > 0:
                    scene_runtime.text += "\n\nВы почувствовали свою сперму в пещерке %s." % _liza_name2
                elif Liza.cum_state("cum_inside_others") > 0:
                    scene_runtime.text += "\n\nВаши пальцы заскользили по пещерке %s, похоже кто-то уже кончил в нее." % _liza_name2
        else:
            scene_runtime.text = "«Эй, дяденка, не так быстро!» останавливает вас %s. «Мамочка говорит, что ты сначала заплатить должен, а потом уже лапать!»" % _liza_name
        scene_runtime.location_text = scene_runtime.text
    call ShowCurrentSex(girl_name_ilt)
    return


label IntLizaTalkAskDad(girl_name_ilt="liza", girl_loc_ilt=""):
    $ scene_runtime.text = str(DaddyAskBuildPhrase(girl_name_ilt) or "")
    $ scene_runtime.location_text = scene_runtime.text
    $ Liza.finish_talk()
    return
