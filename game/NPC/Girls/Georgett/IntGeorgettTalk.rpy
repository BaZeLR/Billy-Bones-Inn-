# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def georgett_grope_outcome(girl_name="georgett", girl_loc="street"):
        loc_key = str(girl_loc or "street")
        has_paid_context = (money >= 8 or (money >= 4 and loc_key == "tavern")) and Georgett.can_player_cum()

        if not has_paid_context:
            if not Georgett.can_player_cum():
                grope_text = "«На сегодня с тебя уже хватит, красавчик», - усмехнулась %s. «Приходи завтра, если захочешь еще.»" % Georgett.real_name()
            else:
                grope_text = "«Эй, осади лошадей!» говорит вам %s. «Сначала заплати, а потом уже лапай!»" % Georgett.real_name()
            return {"text": grope_text, "show_current_sex": False}

        if Georgett.rel >= 10:
            grope_text = "Вы начали мять сиськи %s через тонкую ткань ее блузки.\nВы сунули руку под короткую юбочку вашей любовницы и стали наминать ее вульву." % Georgett.real_name2()
            if Georgett.cum_state("cum_inside_you") > 0:
                grope_text += "\n\nВы почувствовали свою сперму в пещерке %s." % Georgett.real_name2()
            elif Georgett.cum_state("cum_inside_others") > 0:
                grope_text += "\n\nВаши пальцы заскользили по пещерке %s, похоже кто-то уже кончил в нее." % Georgett.real_name2()
        else:
            grope_text = "«Эй, осади лошадей!» говорит вам %s. «Сначала заплати, а потом уже лапай!»" % Georgett.real_name()

        return {"text": grope_text, "show_current_sex": True}


label IntGeorgettTalk(girl_name="georgett", girl_loc=""):
    $ Georgett.mark_known()
    if str(girl_loc or "") == "":
        if CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "TavernMain":
            $ girl_loc = "tavern"
        elif CurrentRoom is not None and str(getattr(CurrentRoom, "code_name", "") or "") == "PortStreets":
            $ girl_loc = "street"
        elif str(CurLoc or "") == "TavernMain":
            $ girl_loc = "tavern"
        else:
            $ girl_loc = "street"

    if str(girl_loc or "") == "street" and str(girl_name or "") == "georgett" and int(Georgett.rel or 0) <= 0:
        $ MainTxt = "-Привет красавчик! Не хочешь ли поразвлечься? Всего восемь мараведи!\n\nВы поговорили с ней и узнали, что ее зовут Жоржетта Брюно, она шлюха и промышляет здесь уже давно."
        $ CurLocDesc = MainTxt
        $ Georgett.add_relation(1)

    $ main_ui_begin_talk_state("Разговор с Жоржеттой", girl_name)
    $ current_action_title = "Разговор с Жоржеттой"
    $ current_action_content = None
    python:
        if str(girl_loc or "") == "street" and str(girl_name or "").strip().lower() == "georgett" and renpy.loadable("images/georgett/Port/wait.jpg"):
            _georgett_picture = "images/georgett/Port/wait.jpg"
        else:
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
    $ current_action_items.append(MenuItem("Осмотреть", Function(NpcActionLookState, girl_name, CurLoc)))
    $ current_action_items.append(MenuItem("Болтать", Call("IntGeorgettTalkApply", girl_name, girl_loc, "smalltalk")))

    if Georgett.can_ask_topic("clients"):
        $ current_action_items.append(MenuItem("Спросить о клиентах", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_clients")))

    if Georgett.can_ask_topic("sex"):
        $ current_action_items.append(MenuItem("Спросить о сексе", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_sex")))

    if Georgett.can_ask_topic("family"):
        $ current_action_items.append(MenuItem("Спросить о семье", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_family")))

    if Georgett.can_ask_topic("pregnancy"):
        $ current_action_items.append(MenuItem("Спросить о беременности", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_pregnancy")))

    if Georgett.can_ask_topic("kids"):
        $ current_action_items.append(MenuItem("Спросить о детях", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_kids")))

    if Georgett.can_ask_topic("gerhard"):
        $ current_action_items.append(MenuItem("Спросить об отце Герхарде", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_gerhard")))

    if int(Liza.story_value("SawChurchAfterCermon", 0) or 0) and Georgett.can_talk_today():
        $ current_action_items.append(MenuItem("Рассказать про Лизетту и отца Герхарда", Call("IntGeorgettTalkApply", girl_name, girl_loc, "tell_liza_gerhard")))

    if Georgett.can_invite_to_tavern() and Georgett.can_talk_today():
        $ current_action_items.append(MenuItem("Предложить работать у себя в трактире", Call("IntGeorgettTalkApply", girl_name, girl_loc, "invite_tavern")))

    if Georgett.can_work_tavern() and Georgett.can_talk_today():
        $ current_action_items.append(MenuItem("Спросить как работается у вас в трактире", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_work")))

    if Georgett.can_work_tavern() and Georgett.can_talk_today() and int(Liza.story_value("GloryHoleAsked", 0) or 0) == 1 and int(Georgett.story_value("GloryHoleExplained", 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Спросить про работу в \"Пьяном Пирате\"", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_pirate")) )

    if Georgett.can_work_tavern() and Georgett.can_talk_today() and TavernGloryHole == 2 and int(Georgett.story_value("GloryHoleAgreed", 0) or 0) == 0:
        $ current_action_items.append(MenuItem("Договориться об условиях работы у глорихола", Call("IntGeorgettTalkApply", girl_name, girl_loc, "gloryhole_terms")) )

    if (
        (
            int(Georgett.story_value("TellAboutEddieMomSex", 0) or 0) == 0
            and (Becky.var.get("EddieTryToFuck", 0) == 4 or Becky.var.get("visitedhome", 0) >= 7)
        )
        or (
            Becky.var.get("EddieGeorg", 0) == 0
            and Eddie.var.get("TalkedAboutGeorgett", 0) == 1
            and Becky.var.get("visitedhome", 0) >= 3
            and (Eddie.var.get("SawMomSex", 0) > 0 or Becky.var.get("HomeSex", 0) > 0)
        )
    ) and Georgett.can_talk_today():
        $ current_action_items.append(MenuItem("Обсудить Эдди", Call("IntGeorgettTalkApply", girl_name, girl_loc, "talk_eddie")))

    if Becky.var.get("EddieGeorg", 0) > 0 and Becky.var.get("EddieWhoreHome", 0) == 0 and (money > 25 or (Becky.var.get("EddieGeorg", 0) > 1 and money > 10)) and Georgett.talk_count() < 2:
        $ current_action_items.append(MenuItem("Предложить Жоржетте проспонсировать ее визит к Эдди домой", Call("IntGeorgettTalkApply", girl_name, girl_loc, "sponsor_eddie_home")) )

    if Becky.var.get("EddieGeorg", 0) > 0 and int(calendar_v2.hour or 0) <= 15:
        $ current_action_items.append(MenuItem("Спросить, не приходил ли Эдди", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_eddie_visit")) )

    if (money >= 8 or (money >= 4 and girl_loc == "tavern")) and Georgett.can_player_cum():
        $ current_action_items.append(MenuItem("Снять", Call("IntGeorgettTalkApply", girl_name, girl_loc, "hire")) )

    $ current_action_items.append(MenuItem("Лапать", Call("IntGeorgettTalkApply", girl_name, girl_loc, "grope")))

    if Georgett.can_talk_today() and int(Georgett.rel or 0) >= 8 and int(Georgett.stats.get("pregnancy", 0) or 0) >= 120:
        $ _dad_phrase = DaddyAskBuildPhrase(girl_name)
        if str(_dad_phrase or "") != "":
            $ current_action_items.append(MenuItem("Поинтересоваться, знает ли она от кого залетела", Call("IntGeorgettTalkApply", girl_name, girl_loc, "ask_dad")) )

    if girl_loc == "tavern":
        $ current_action_items.append(MenuItem("Обсудить одежду", Call("IntGeorgettTalkApply", girl_name, girl_loc, "dress")) )

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntGeorgettTalkApply(girl_name="georgett", girl_loc="street", choice_code=""):
    if str(choice_code or "") == "inspect":
        call ShowGirlCard(girl_name)
        return

    if str(choice_code or "") == "smalltalk":
        $ MainTxt = "Вы некоторое время болтаете с Жоржеттой о разных вещах."
        if Georgett.talk_count() <= 2 and procedural_randint(1, 2, key="procedural:NPC/Girls/Georgett/IntGeorgettTalk.rpy:procedural_randint:148:1") == 1:
            if Georgett.rel < 3 or (Georgett.sex_state.get("lick_pussy", 0) >= 4 and Georgett.rel < 5) or (Georgett.orgasm_count_given() >= 2 and Georgett.sex_state.get("lick_pussy", 0) >= 4 and Georgett.rel < 7):
                $ MainTxt += "\n\nВы чуть лучше узнали Жоржетту."
                $ Georgett.add_relation(1)
            elif Georgett.rel < 7:
                $ MainTxt += "\n\nИз уклончивых ответов девушки вы поняли, что она вам еще мало доверяет. Может, если бы вы узнали ее получше или доставили ей приятное, она бы с вами поделилась еще чем-то."
        if Georgett.talk_count() > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_clients":
        $ MainTxt = "«Ну в день у меня обычно бывает от трех до пяти клиентов. Хотя конечно день на день не приходится, например, помню, в гавань зашла военная эскадра. Ох, как тогда имели всех девочек! Меня отодрали человек двадцать, наверное, а то и больше. Я спускала и спускала, ох, как же сладко было тогда!» - говорит Жоржетта, автоматически поглаживая промежность сквозь юбку."
        if Georgett.mark_asked_topic("askclients"):
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_sex":
        $ MainTxt = "«Ох, красавчик, мне всегда нравился секс. Маленькой еще была, за другими подсматривала и писю теребила. За сестренками старшими, как они с мальчишками то на сеновале, то в саду забавлялись, за маменькой как она то с папкой, то с дядей мельником, то с дядей молочником, то с сестренкиными дружками кувыркалась. За папкой, как он с соседками да с сестриными подружками сношался. Ну а когда Кристоф и Мишель, парни с соседней улицы, после танцев меня в уголке зажали и стали лапать, то я и не ломалась совсем и вскоре у меня в киске вместо девственной плевы было две порции свежего семени. Ну а потом пошло-поехало, никому я почитай и не отказывала, больно приятно это было. Потом я здесь, в городе устроилась, здесь мне за это и деньги платят. Вот еще бы все клиенты были как ты, внимательные. А то многие только о себе и думают, а девушке кончить не дают. Бывает за день только пару раз и разрядишься.» - рассказывает Жоржетта."
        if Georgett.mark_asked_topic("asksex"):
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_family":
        $ MainTxt = "«Даже не знаю, папка мой действительно ли мне папка, мамочка-то моя на передок всегда слаба была. Да и батяня за всеми юбками бегал, да и сейчас бегает. Любили они потрахаться, и от нас даже этого не скрывали. А уж на праздниках-то! Помню, однажды на празднике урожая мамка моя, сестренка старшая, Симона, и Жанна, мельникова дочка, в такой раж вошли что голыми на столах танцевали. Ну а уж после их гости и оприходовали. Папенька тот тоже, Симоне борозду-то распахал и засеял, не посмотрел что дочка. Симонка-то после того случая понесла ведь, и не поймешь от кого, может и от папки. Ну а вообще да, хорошо жили, дружно. Я тоже с папкой да с братцами несколько раз перепихнулась.» - рассказывает Жоржетта."
        if Georgett.mark_asked_topic("askparents"):
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_pregnancy":
        $ MainTxt = "«Беременность? Ну а как же без нее-то? Мужики они-то любят девушкам своим семенем прямо в маточку брызнуть, а от этого, как всем известно, детки родятся. Вот Симонка, сестра моя старшая, прежде чем замуж выскочила, целых троих нагуляла. А себя вспомнить - первый раз у меня животик округлился когда только-только первые волосики на письке пробиваться начали. Но мамочка моя всегда говорила, что ребенок есть ребенок, ему всегда рады, и ничего страшного в залете нет.» - поведала вам Жоржетта."
        if Georgett.mark_asked_topic("askpregnancy"):
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_kids":
        $ MainTxt = "«Дети? Четверо у меня их. Первую свою доченьку Лизку, Лизетту то есть, я даже знаю от кого родила. Ну, почти. Неделя только прошла как я девства лишилась и на рынок мы поехали. А там у купца одного из дальних стран носильщики - один другого мускулистее. А трое из них и вовсе на наших не похожи - кожа как уголь. Ну и услышала я как мама тете Франсуазе говорит что мол пошли, опробуем их. Стала я проситься с ними пойти, мама удивилась, спросила не мала ли я, но разрешила. Зашли мы за шатер с ними и часа два нас имели. Тогда, кстати, я у мамы первый раз киску-то и полизала. А через 9 месяцев Лизетта-то мулаточкой у меня и родилась.»"
        if int(Liza.story_value("ProstStart", 0) or 0) == 0:
            $ MainTxt += "\n\n«Насчет остальных же троих я не так уверенна. От кого угодно могла я залететь. Детки же мои сейчас с мамой и папой моими живут, Лизетта вот только порой ко мне приезжает.»"
        else:
            $ MainTxt += "\n\n«Насчет остальных же троих я не так уверенна. От кого угодно могла я залететь. Детки же мои сейчас с мамой и папой моими живут, а Лизетта вот уже ко мне перебралась, помогает.»"
        if Georgett.mark_asked_topic("askkids"):
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_gerhard":
        $ MainTxt = "«Отец Герхард? Кто-то, наверное ты, негодник, рассказал ему что мы с тобой во время службы трахались. Вот он меня и раскрутил на исповеди. Теперь он меня порой после воскресной службы потрахивает. Оргазм и благословление это конечно не мараведи, но тоже неплохо, так что я не в обиде.»"
        if Georgett.mark_asked_topic("TalkChurchAfterCermon"):
            $ MainTxt += "\n\nВас немного возбудил рассказ Жоржетты."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "tell_liza_gerhard":
        if int(Georgett.story_value("TalkChurchAfterCermonLiza", 0) or 0) == 0:
            $ MainTxt = "Вы рассказываете Жоржетте что вы видели как отец Герхард соблазнил ее дочь после воскресной службы. Также вы упоминаете что Лизетта и до встречи с похотливым жрецом не отказывала мальчикам.\n«Ох дочка, повзрослела уже, а мне ничего не сказала! А я уже волноваться начала, подрастает, а мальчиками ничего нет» - реагирует Жоржетта. «А отец Герхард-то, хорош, дочку мою трахнул, а мне и не подумал сказать. Ну, раз девочка большая уже выросла, будет мне помогать», - решает она.\n\n«Ну, Стефан, завтра встречай нас обеих», - и с этими словами она удаляется."
            $ Georgett.mark_asked_topic("TalkChurchAfterCermonLiza")
            $ Georgett.finish_talk()
            $ CurLocDesc = MainTxt
            jump StreetTavern
        $ MainTxt = "Вы рассказываете Жоржетте что вы снова видели как отец Герхард трахал ее дочь после воскресной службы.\n«Молодец дочка, благословление Ильматера лишним не будет, да и любовник отец Герхард хороший!» - отвечает Жоржетта."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "invite_tavern":
        if Georgett.rel < 10:
            $ MainTxt = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«Не, мил человек», - отвечает Жоржетта, «не могу я тебе еще доверять. А вдруг обманешь? Мы пока здесь, как привыкли, поработаем.»"
            $ Georgett.finish_talk()
            $ CurLocDesc = MainTxt
            call IntGeorgettTalkRefresh(girl_name, girl_loc)
            return
        if Liza.rel < 8:
            $ MainTxt = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«Не, мил человек», - отвечает Жоржетта, «я бы с радостью, но доча моя в тебе еще сомневается. Не могу я ее пока убедить. Так что мы пока здесь, как привыкли, поработаем.»"
            $ Georgett.finish_talk()
            $ CurLocDesc = MainTxt
            call IntGeorgettTalkRefresh(girl_name, girl_loc)
            return
        $ MainTxt = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«А что?», - говорит Жоржетта, «почему бы и нет? Ты мне нравишься, доча моя тоже в тебе души не чает, отчего бы и не начать работать у тебя? Согласные мы!»\nВы приводите маму с дочкой в свой трактир, представляете их Сандре и домочадцам, объясняете в чем заключается их промысел и что заниматься им отныне они будут у вас. Сандра воспринимает известие спокойно, остальные слегка шокированы. Но владелец трактира - вы, так что у них нет выбора кроме как покориться. Обсуждение деталей затягивается до вечера, так что приступить к делу новая парочка ваших работниц сможет только на следующий день."
        $ Georgett.add_relation(1)
        $ Georgett.set_hired(True)
        $ Liza.set_hired(True)
        $ TavernBreakfastGeorgetteLizaPending = 1
        $ householdmembers = int(householdmembers) + 2 + int(ProstitutesKids)
        $ Georgett.finish_talk()
        call NextDay("TavernMain", 1)
        return

    if str(choice_code or "") == "ask_work":
        $ MainTxt = "Вы спрашиваете Жоржетту как ей работается у вас в трактире.\n"
        if TavernGloryHole == 2:
            $ MainTxt += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает. А теперь, когда есть глорихол, наши заработки еще повысились!»"
        elif int(Georgett.story_value("GloryHoleExplained", 0) or 0) == 1:
            $ MainTxt += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает. Разве что если бы еще глорихол был, то можно бы было еще больше денег заработать, наверное.»"
        else:
            $ MainTxt += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает.» Однако у вас остается впечатление что она хотела еще что-то сказать, но предпочла промолчать."
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_pirate":
        $ MainTxt = "Вы расспрашиваете Жоржетту про ее работу в трактире «Пьяный Пират».\n«Ох Лизетта, Лизетта! Вечно все перепутает! Не Холглор, а глорихол! Занятная штука. С ним на одного клиента меньше времени уходит, поэтому можно дешевле брать и люди им чаще пользуются. И работать с ним удобно! Все хотела спросить почему у тебя такого нет, но решила что тебе виднее и промолчала.»\nВас заинтересовал рассказ девушки и вы уточнили у нее устройство данной конструкции.\n«Хм, а ведь хороший мастер такое должен бы быстро суметь сделать...» - подумали вы, выслушав ее рассказ."
        $ Georgett.mark_asked_topic("GloryHoleExplained", 0)
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "gloryhole_terms":
        $ MainTxt = "Вы рассказываете Жоржетте про устроенный вами глорихол. Вы предлагаете установить прейскурант за такой сервис на уровне 6 мараведи. В конечном итоге вы вынуждены согласиться с тем, что вам пойдут только два мараведи, а остальные четыре - в карман трудящихся. Единственное, что утешило вас, так это то, что вы смогли добиться согласия на бесплатный отсос для себя."
        $ Georgett.mark_asked_topic("GloryHoleAgreed", 0)
        $ Georgett.jobs["jobGloryHoleAvail"] = 1
        $ Liza.jobs["jobGloryHoleAvail"] = 1
        $ Liza.sync_shared_state()
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "talk_eddie":
        if Becky.var.get("EddieTryToFuck", 0) == 4 or Becky.var.get("visitedhome", 0) >= 7:
            $ MainTxt = "«Жоржетт, ты была права. Эдди действительно по своей хозяйке сох. Я им все подстроил, дверь в спальню отпер, Бекки раздел и внимание ее отвлек. Ну а Эдди предупредил заранее, что может заходить на огонек. Так он паршивец ни секунды не сомневался, забежал и засадил своей леди-босс!»\n«А она что?»\n«А ничего, подмахивать ему стала как ни в чем не бывало.»\n«Ну, я чего-то в таком роде и ожидала с первого раза как он меня снял. Что ж, теперь, когда его мечта сбылась, наверное ко мне он будет захаживать пореже.»"
            $ Georgett.mark_asked_topic("TellAboutEddieMomSex", 0)
        else:
            $ MainTxt = "Вы рассказываете Жоржетте про сальные взгляды, которые бросает Эдди каждый раз, когда подозревает, что его хозяйка позволяет вам какие-нибудь вольности. Жоржетта не остается в долгу и в свою очередь со смехом рассказывает вам, что когда Эдди ее снимает, он просит, чтобы она изображала строгую леди-босс.\nОтсмеявшись, она предлагает вам разнообразить половую жизнь Эдди, зайдя к нему домой. Вы соглашаетесь."
            $ Becky.var["EddieGeorg"] = 1
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "sponsor_eddie_home":
        if Becky.var.get("EddieGeorg", 0) == 1:
            $ MainTxt = "Вы вручаете Жоржетте 25 мараведи и говорите, что очень бы хотели посмотреть на то, как она займется любовью с Эдди на глазах у Бекки."
            $ money -= 25
        elif Becky.var.get("EddieGeorg", 0) == 2 and Becky.var.get("visitedhome", 0) == 5:
            $ MainTxt = "Вы вручаете Жоржетте 10 мараведи и говорите, что хотите повторения."
            $ money -= 10
        else:
            $ MainTxt = "Вы вручаете Жоржетте 10 мараведи и говорите, что хотели бы еще раз посмотреть на выражение лица вдовы Блэнкеншип."
            $ money -= 10
        $ MainTxt += "\n\nЖоржетта с радостью берет деньги и заверяет вас, что при встрече c Эдди непременно предложит ему навестить его у него дома за ужином."
        $ Becky.var["EddieWhoreHome"] = 1
        $ Georgett.finish_talk()
        call stat
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "ask_eddie_visit":
        $ MainTxt = "«Эй, Жоржи, наш друг Эдди к тебе случаем не захаживал?» - осведомляетесь вы у своей работницы."
        if Becky.var.get("EddieWhoreHome", 0) <= 1:
            if Becky.var.get("visitedhome", 0) >= 7:
                $ MainTxt += "\n\n«Не, он говорит что теперь с хозяйкой своей все больше перепихивается, а на мне экономит.»"
            else:
                $ MainTxt += "\n\n«Не, сегодня его не было. Может завтра зайдет.»"
        else:
            $ MainTxt += "\n\n«Заходил.»"
            if Becky.var.get("EddieGeorg", 0) == 1:
                if Becky.var.get("EddieWhoreHome", 0) == 4:
                    if Becky.var.get("visitedhome", 0) >= 7:
                        $ MainTxt += "\n\n«Согласился, говорит что пусть его леди-босс посмотрит, поучится, разогреется.»"
                    else:
                        $ MainTxt += "\n\n«Пришел в восторг от моего предложения, сказал чтобы сегодня я к нему домой на огонек заглянула.»"
                    $ MainTxt += "\n\n«Так что если хочешь посмотреть - заглядывай и ты к вдове на огонек.»"
                else:
                    $ MainTxt += "\n\n«Отказался.»"
                    if Becky.var.get("visitedhome", 0) < 5:
                        $ MainTxt += "\n\n«Объяснил, сказал что хозяйка его больно строгая, вышвырнет его за такие шутки.»"
                    elif Eddie.var.get("SawMomSex", 0) == 0 or Becky.var.get("HomeSex", 0) == 0:
                        $ MainTxt += "\n\n«Объяснил, сказал что хоть Бекки и разрешила домашним водить своих любовников домой, но он все-таки еще стесняется, не хочет быть первым.»"
                    elif Becky.var.get("EddieWhoreHome", 0) == 2:
                        $ MainTxt += "\n\n«Объяснил, сказал что идея хорошая, только вот больно дорого я с него запросила, нету у него столько.»"
                    else:
                        $ MainTxt += "\n\n«Объяснил, сказал что в другой раз такое замутим, но сейчас ему мол нет мочи терпеть, так что он сразу отымел меня и ушел.»"
            else:
                if Becky.var.get("EddieWhoreHome", 0) == 4:
                    $ MainTxt += "\n\n«Согласился, конечно. Говорит прошлый раз было здорово, надо повторить. Сказал чтобы сегодня я к нему домой на огонек заглянула. Так что если хочешь посмотреть - заглядывай и ты к вдовушке на огонек.»"
                else:
                    $ MainTxt += "\n\n«Отказался, сказал что ему прямо сейчас хочется, мол нет мочи терпеть.»"
        $ Georgett.finish_talk()
        $ CurLocDesc = MainTxt
        call IntGeorgettTalkRefresh(girl_name, girl_loc)
        return

    if str(choice_code or "") == "hire":
        if girl_loc == "tavern":
            $ money -= 4
            call IntGeorgettSex("georgett", "tavern")
            $ CurLocDesc = MainTxt
            call IntGeorgettTalkRefresh(girl_name, girl_loc)
        else:
            $ money -= 8
            call IntGeorgettSex("georgett", "street")
            $ CurLocDesc = MainTxt
            jump PortStreets
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
        $ Georgett.finish_talk()
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
    $ main_ui_end_talk_state()
    return
