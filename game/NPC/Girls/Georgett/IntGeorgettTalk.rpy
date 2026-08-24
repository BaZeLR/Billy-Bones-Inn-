# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================
init python:
    def georgett_grope_outcome(girl_name="georgett", girl_loc="street"):
        loc_key = str(girl_loc or "street")
        has_paid_context = (player.economy.money >= 8 or (player.economy.money >= 4 and loc_key == "tavern")) and player.intimacy.can_cum()

        if not has_paid_context:
            if not player.intimacy.can_cum():
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
    $ renpy.dynamic("_georgett_talk_new", "_georgett_picture")
    if not girl_loc:
        $ girl_loc = "tavern" if str(rooms.current_code or "") == "TavernMain" else "street"
    $ _georgett_talk_new = str(main_ui_runtime.mode or "") != "talk" or str(main_ui_runtime.selected_char or main_ui_runtime.girl_key or "").strip().lower() != str(girl_name or "georgett").strip().lower()
    $ main_ui_begin_talk_state("Разговор с Жоржеттой", girl_name)
    $ _georgett_picture = "images/georgett/Port/wait.jpg" if girl_loc == "street" and renpy.loadable("images/georgett/Port/wait.jpg") else str(girl_card_portrait_path(girl_name) or "")
    if _georgett_talk_new and _georgett_picture and renpy.loadable(_georgett_picture):
        $ scene_runtime.picture = _georgett_picture
    if _georgett_talk_new:
        $ scene_runtime.text = "Жоржетта вопросительно смотрит на вас, ожидая, о чем вы захотите поговорить."
        $ scene_runtime.location_text = scene_runtime.text
    while True:
        menu:
            "Осмотреть":
                call ShowGirlCard(girl_name)
            "Болтать":
                call IntGeorgettSmalltalk(girl_name, girl_loc)
            "Спросить о клиентах" if Georgett.can_ask_topic("clients"):
                call IntGeorgettAskClients(girl_name, girl_loc)
            "Спросить о сексе" if Georgett.can_ask_topic("sex"):
                call IntGeorgettAskSex(girl_name, girl_loc)
            "Спросить о семье" if Georgett.can_ask_topic("family"):
                call IntGeorgettAskFamily(girl_name, girl_loc)
            "Спросить о беременности" if Georgett.can_ask_topic("pregnancy"):
                call IntGeorgettAskPregnancy(girl_name, girl_loc)
            "Спросить о детях" if Georgett.can_ask_topic("kids"):
                call IntGeorgettAskKids(girl_name, girl_loc)
            "Спросить об отце Герхарде" if Georgett.can_ask_topic("gerhard"):
                call IntGeorgettAskGerhard(girl_name, girl_loc)
            "Рассказать про Лизетту и отца Герхарда" if Liza.witnessed_church_after_sermon and Georgett.can_talk_today():
                call IntGeorgettTellLizaGerhard(girl_name, girl_loc)
            "Предложить работать у себя в трактире" if Georgett.can_invite_to_tavern() and Georgett.can_talk_today():
                call IntGeorgettInviteTavern(girl_name, girl_loc)
            "Спросить как работается у вас в трактире" if Georgett.can_work_tavern() and Georgett.can_talk_today():
                call IntGeorgettAskWork(girl_name, girl_loc)
            "Спросить про работу в Пьяном Пирате" if Georgett.can_work_tavern() and Georgett.can_talk_today() and Liza.glory_hole_asked and int(Georgett.story_value("GloryHoleExplained",0) or 0)==0:
                call IntGeorgettAskPirate(girl_name, girl_loc)
            "Договориться об условиях работы у глорихола" if Georgett.can_work_tavern() and Georgett.can_talk_today() and player.tavern_management.glory_hole==2 and int(Georgett.story_value("GloryHoleAgreed",0) or 0)==0:
                call IntGeorgettGloryholeTerms(girl_name, girl_loc)
            "Обсудить Эдди" if Georgett.can_talk_today() and ((int(Georgett.story_value("TellAboutEddieMomSex",0) or 0)==0 and (Becky.eddie_join_stage==4 or Becky.home_visit_stage>=7)) or (Becky.eddie_georgett_stage==0 and Eddie.talked_about_georgett and Becky.home_visit_stage>=3 and (Eddie.saw_mother_sex or Becky.home_sex_unlocked))):
                call IntGeorgettTalkEddie(girl_name, girl_loc)
            "Предложить Жоржетте проспонсировать ее визит к Эдди домой" if Becky.eddie_georgett_stage>0 and Becky.eddie_home_visit_state==0 and (player.economy.money>25 or (Becky.eddie_georgett_stage>1 and player.economy.money>10)) and Georgett.talk_count()<2:
                call IntGeorgettSponsorEddieHome(girl_name, girl_loc)
            "Спросить, не приходил ли Эдди" if Becky.eddie_georgett_stage>0 and int(calendar_v2.hour or 0)<=15:
                call IntGeorgettAskEddieVisit(girl_name, girl_loc)
            "Снять" if (player.economy.money>=8 or (player.economy.money>=4 and girl_loc=="tavern")) and player.intimacy.can_cum():
                call IntGeorgettHire(girl_name, girl_loc)
            "Лапать":
                call IntGeorgettGrope(girl_name, girl_loc)
            "Поинтересоваться, знает ли она от кого залетела" if Georgett.can_talk_today() and int(Georgett.rel or 0)>=8 and int(Georgett.stats.get("pregnancy",0) or 0)>=120 and str(DaddyAskBuildPhrase(girl_name) or "")!="":
                call IntGeorgettAskDad(girl_name, girl_loc)
            "Обсудить одежду" if girl_loc == "tavern":
                call IntGeorgettDressChange(girl_name)
            "Закончить разговор":
                $ main_ui_end_talk_state()
                return
        if str(main_ui_runtime.mode or "") != "talk":
            return

label IntGeorgettSmalltalk(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "Вы некоторое время болтаете с Жоржеттой о разных вещах."
    if Georgett.talk_count() <= 2 and procedural_randint(1, 2, key="procedural:NPC/Girls/Georgett/IntGeorgettTalk.rpy:procedural_randint:148:1") == 1:
        if Georgett.rel < 3 or (Georgett.sex_state.get("lick_pussy", 0) >= 4 and Georgett.rel < 5) or (int(Georgett.sex_stat("orgasms_given", 0) or 0) >= 2 and Georgett.sex_state.get("lick_pussy", 0) >= 4 and Georgett.rel < 7):
            $ scene_runtime.text += "\n\nВы чуть лучше узнали Жоржетту."
            $ Georgett.add_relation(1)
        elif Georgett.rel < 7:
            $ scene_runtime.text += "\n\nИз уклончивых ответов девушки вы поняли, что она вам еще мало доверяет. Может, если бы вы узнали ее получше или доставили ей приятное, она бы с вами поделилась еще чем-то."
    if Georgett.talk_count() > 2:
        $ scene_runtime.text += "\n\nНичего нового из разговора вы не узнали."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskClients(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "«Ну в день у меня обычно бывает от трех до пяти клиентов. Хотя конечно день на день не приходится, например, помню, в гавань зашла военная эскадра. Ох, как тогда имели всех девочек! Меня отодрали человек двадцать, наверное, а то и больше. Я спускала и спускала, ох, как же сладко было тогда!» - говорит Жоржетта, автоматически поглаживая промежность сквозь юбку."
    if Georgett.mark_asked_topic("askclients"):
        $ scene_runtime.text += "\n\nВас немного возбудил рассказ Жоржетты."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskSex(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "«Ох, красавчик, мне всегда нравился секс. Маленькой еще была, за другими подсматривала и писю теребила. За сестренками старшими, как они с мальчишками то на сеновале, то в саду забавлялись, за маменькой как она то с папкой, то с дядей мельником, то с дядей молочником, то с сестренкиными дружками кувыркалась. За папкой, как он с соседками да с сестриными подружками сношался. Ну а когда Кристоф и Мишель, парни с соседней улицы, после танцев меня в уголке зажали и стали лапать, то я и не ломалась совсем и вскоре у меня в киске вместо девственной плевы было две порции свежего семени. Ну а потом пошло-поехало, никому я почитай и не отказывала, больно приятно это было. Потом я здесь, в городе устроилась, здесь мне за это и деньги платят. Вот еще бы все клиенты были как ты, внимательные. А то многие только о себе и думают, а девушке кончить не дают. Бывает за день только пару раз и разрядишься.» - рассказывает Жоржетта."
    if Georgett.mark_asked_topic("asksex"):
        $ scene_runtime.text += "\n\nВас немного возбудил рассказ Жоржетты."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskFamily(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "«Даже не знаю, папка мой действительно ли мне папка, мамочка-то моя на передок всегда слаба была. Да и батяня за всеми юбками бегал, да и сейчас бегает. Любили они потрахаться, и от нас даже этого не скрывали. А уж на праздниках-то! Помню, однажды на празднике урожая мамка моя, сестренка старшая, Симона, и Жанна, мельникова дочка, в такой раж вошли что голыми на столах танцевали. Ну а уж после их гости и оприходовали. Папенька тот тоже, Симоне борозду-то распахал и засеял, не посмотрел что дочка. Симонка-то после того случая понесла ведь, и не поймешь от кого, может и от папки. Ну а вообще да, хорошо жили, дружно. Я тоже с папкой да с братцами несколько раз перепихнулась.» - рассказывает Жоржетта."
    if Georgett.mark_asked_topic("askparents"):
        $ scene_runtime.text += "\n\nВас немного возбудил рассказ Жоржетты."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskPregnancy(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "«Беременность? Ну а как же без нее-то? Мужики они-то любят девушкам своим семенем прямо в маточку брызнуть, а от этого, как всем известно, детки родятся. Вот Симонка, сестра моя старшая, прежде чем замуж выскочила, целых троих нагуляла. А себя вспомнить - первый раз у меня животик округлился когда только-только первые волосики на письке пробиваться начали. Но мамочка моя всегда говорила, что ребенок есть ребенок, ему всегда рады, и ничего страшного в залете нет.» - поведала вам Жоржетта."
    if Georgett.mark_asked_topic("askpregnancy"):
        $ scene_runtime.text += "\n\nВас немного возбудил рассказ Жоржетты."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskKids(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "«Дети? Четверо у меня их. Первую свою доченьку Лизку, Лизетту то есть, я даже знаю от кого родила. Ну, почти. Неделя только прошла как я девства лишилась и на рынок мы поехали. А там у купца одного из дальних стран носильщики - один другого мускулистее. А трое из них и вовсе на наших не похожи - кожа как уголь. Ну и услышала я как мама тете Франсуазе говорит что мол пошли, опробуем их. Стала я проситься с ними пойти, мама удивилась, спросила не мала ли я, но разрешила. Зашли мы за шатер с ними и часа два нас имели. Тогда, кстати, я у мамы первый раз киску-то и полизала. А через 9 месяцев Лизетта-то мулаточкой у меня и родилась.»"
    if not Liza.prostitution_started:
        $ scene_runtime.text += "\n\n«Насчет остальных же троих я не так уверенна. От кого угодно могла я залететь. Детки же мои сейчас с мамой и папой моими живут, Лизетта вот только порой ко мне приезжает.»"
    else:
        $ scene_runtime.text += "\n\n«Насчет остальных же троих я не так уверенна. От кого угодно могла я залететь. Детки же мои сейчас с мамой и папой моими живут, а Лизетта вот уже ко мне перебралась, помогает.»"
    if Georgett.mark_asked_topic("askkids"):
        $ scene_runtime.text += "\n\nВас немного возбудил рассказ Жоржетты."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskGerhard(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "«Отец Герхард? Кто-то, наверное ты, негодник, рассказал ему что мы с тобой во время службы трахались. Вот он меня и раскрутил на исповеди. Теперь он меня порой после воскресной службы потрахивает. Оргазм и благословление это конечно не мараведи, но тоже неплохо, так что я не в обиде.»"
    if Georgett.mark_asked_topic("TalkChurchAfterCermon"):
        $ scene_runtime.text += "\n\nВас немного возбудил рассказ Жоржетты."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettTellLizaGerhard(girl_name="georgett", girl_loc="street"):
    if int(Georgett.story_value("TalkChurchAfterCermonLiza", 0) or 0) == 0:
        $ scene_runtime.text = "Вы рассказываете Жоржетте что вы видели как отец Герхард соблазнил ее дочь после воскресной службы. Также вы упоминаете что Лизетта и до встречи с похотливым жрецом не отказывала мальчикам.\n«Ох дочка, повзрослела уже, а мне ничего не сказала! А я уже волноваться начала, подрастает, а мальчиками ничего нет» - реагирует Жоржетта. «А отец Герхард-то, хорош, дочку мою трахнул, а мне и не подумал сказать. Ну, раз девочка большая уже выросла, будет мне помогать», - решает она.\n\n«Ну, Стефан, завтра встречай нас обеих», - и с этими словами она удаляется."
        $ Georgett.mark_asked_topic("TalkChurchAfterCermonLiza")
        $ Georgett.finish_talk()
        $ scene_runtime.location_text = scene_runtime.text
        return
    $ scene_runtime.text = "Вы рассказываете Жоржетте что вы снова видели как отец Герхард трахал ее дочь после воскресной службы.\n«Молодец дочка, благословление Ильматера лишним не будет, да и любовник отец Герхард хороший!» - отвечает Жоржетта."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettInviteTavern(girl_name="georgett", girl_loc="street"):
    if Georgett.rel < 10:
        $ scene_runtime.text = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«Не, мил человек», - отвечает Жоржетта, «не могу я тебе еще доверять. А вдруг обманешь? Мы пока здесь, как привыкли, поработаем.»"
        $ Georgett.finish_talk()
        $ scene_runtime.location_text = scene_runtime.text
        return
    elif Liza.rel < 8:
        $ scene_runtime.text = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«Не, мил человек», - отвечает Жоржетта, «я бы с радостью, но доча моя в тебе еще сомневается. Не могу я ее пока убедить. Так что мы пока здесь, как привыкли, поработаем.»"
        $ Georgett.finish_talk()
        $ scene_runtime.location_text = scene_runtime.text
        return
    else:
        $ scene_runtime.text = "Вы подходите к Жоржетте и предлагаете ей с дочкой работать у себя трактире. Так как вы предоставите ей комнату, то они смогут брать по 10 мараведи с клиента и из них 3 оставлять вам - за кров и за еду. Ну еще вы за сношение с ними будете платить только 4 мараведи. Работать в комнате им будет удобнее, а клиентов будет даже больше, так как в ваш трактир многие захаживают.\n«А что?», - говорит Жоржетта, «почему бы и нет? Ты мне нравишься, доча моя тоже в тебе души не чает, отчего бы и не начать работать у тебя? Согласные мы!»\nВы приводите маму с дочкой в свой трактир, представляете их Сандре и домочадцам, объясняете в чем заключается их промысел и что заниматься им отныне они будут у вас. Сандра воспринимает известие спокойно, остальные слегка шокированы. Но владелец трактира - вы, так что у них нет выбора кроме как покориться. Обсуждение деталей затягивается до вечера, так что приступить к делу новая парочка ваших работниц сможет только на следующий день."
        $ Georgett.add_relation(1)
        $ Georgett.set_hired(True)
        $ Liza.set_hired(True)
        $ player.tavern_management.breakfast.georgett_liza_pending = 1
        $ player.tavern_management.household_members = int(player.tavern_management.household_members) + 2 + kids_count_for_mothers("georgett", "liza")
        $ Georgett.finish_talk()
        call NextDay("TavernMain", 1)
    return


label IntGeorgettAskWork(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "Вы спрашиваете Жоржетту как ей работается у вас в трактире.\n"
    if player.tavern_management.glory_hole == 2:
        $ scene_runtime.text += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает. А теперь, когда есть глорихол, наши заработки еще повысились!»"
    elif int(Georgett.story_value("GloryHoleExplained", 0) or 0) == 1:
        $ scene_runtime.text += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает. Разве что если бы еще глорихол был, то можно бы было еще больше денег заработать, наверное.»"
    else:
        $ scene_runtime.text += "«Очень хорошо, и клиентов много, и кормят неплохо, и комната всем устраивает.» Однако у вас остается впечатление что она хотела еще что-то сказать, но предпочла промолчать."
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskPirate(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "Вы расспрашиваете Жоржетту про ее работу в трактире «Пьяный Пират».\n«Ох Лизетта, Лизетта! Вечно все перепутает! Не Холглор, а глорихол! Занятная штука. С ним на одного клиента меньше времени уходит, поэтому можно дешевле брать и люди им чаще пользуются. И работать с ним удобно! Все хотела спросить почему у тебя такого нет, но решила что тебе виднее и промолчала.»\nВас заинтересовал рассказ девушки и вы уточнили у нее устройство данной конструкции.\n«Хм, а ведь хороший мастер такое должен бы быстро суметь сделать...» - подумали вы, выслушав ее рассказ."
    $ Georgett.mark_asked_topic("GloryHoleExplained", 0)
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettGloryholeTerms(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "Вы рассказываете Жоржетте про устроенный вами глорихол. Вы предлагаете установить прейскурант за такой сервис на уровне 6 мараведи. В конечном итоге вы вынуждены согласиться с тем, что вам пойдут только два мараведи, а остальные четыре - в карман трудящихся. Единственное, что утешило вас, так это то, что вы смогли добиться согласия на бесплатный отсос для себя."
    $ Georgett.mark_asked_topic("GloryHoleAgreed", 0)
    $ Georgett.jobs["jobGloryHoleAvail"] = 1
    $ Liza.jobs["jobGloryHoleAvail"] = 1
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettTalkEddie(girl_name="georgett", girl_loc="street"):
    if Becky.eddie_join_stage == 4 or Becky.home_visit_stage >= 7:
        $ scene_runtime.text = "«Жоржетт, ты была права. Эдди действительно по своей хозяйке сох. Я им все подстроил, дверь в спальню отпер, Бекки раздел и внимание ее отвлек. Ну а Эдди предупредил заранее, что может заходить на огонек. Так он паршивец ни секунды не сомневался, забежал и засадил своей леди-босс!»\n«А она что?»\n«А ничего, подмахивать ему стала как ни в чем не бывало.»\n«Ну, я чего-то в таком роде и ожидала с первого раза как он меня снял. Что ж, теперь, когда его мечта сбылась, наверное ко мне он будет захаживать пореже.»"
        $ Georgett.mark_asked_topic("TellAboutEddieMomSex", 0)
    else:
        $ scene_runtime.text = "Вы рассказываете Жоржетте про сальные взгляды, которые бросает Эдди каждый раз, когда подозревает, что его хозяйка позволяет вам какие-нибудь вольности. Жоржетта не остается в долгу и в свою очередь со смехом рассказывает вам, что когда Эдди ее снимает, он просит, чтобы она изображала строгую леди-босс.\nОтсмеявшись, она предлагает вам разнообразить половую жизнь Эдди, зайдя к нему домой. Вы соглашаетесь."
        $ Becky.eddie_georgett_stage = 1
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettSponsorEddieHome(girl_name="georgett", girl_loc="street"):
    if Becky.eddie_georgett_stage == 1:
        $ scene_runtime.text = "Вы вручаете Жоржетте 25 мараведи и говорите, что очень бы хотели посмотреть на то, как она займется любовью с Эдди на глазах у Бекки."
        $ player.spend_money(25)
    elif Becky.eddie_georgett_stage == 2 and Becky.home_visit_stage == 5:
        $ scene_runtime.text = "Вы вручаете Жоржетте 10 мараведи и говорите, что хотите повторения."
        $ player.spend_money(10)
    else:
        $ scene_runtime.text = "Вы вручаете Жоржетте 10 мараведи и говорите, что хотели бы еще раз посмотреть на выражение лица вдовы Блэнкеншип."
        $ player.spend_money(10)
    $ scene_runtime.text += "\n\nЖоржетта с радостью берет деньги и заверяет вас, что при встрече c Эдди непременно предложит ему навестить его у него дома за ужином."
    $ Becky.eddie_home_visit_state = 1
    $ Georgett.finish_talk()
    call stat
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettAskEddieVisit(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = "«Эй, Жоржи, наш друг Эдди к тебе случаем не захаживал?» - осведомляетесь вы у своей работницы."
    if Becky.eddie_home_visit_state <= 1:
        if Becky.home_visit_stage >= 7:
            $ scene_runtime.text += "\n\n«Не, он говорит что теперь с хозяйкой своей все больше перепихивается, а на мне экономит.»"
        else:
            $ scene_runtime.text += "\n\n«Не, сегодня его не было. Может завтра зайдет.»"
    else:
        $ scene_runtime.text += "\n\n«Заходил.»"
        if Becky.eddie_georgett_stage == 1:
            if Becky.eddie_home_visit_state == 4:
                if Becky.home_visit_stage >= 7:
                    $ scene_runtime.text += "\n\n«Согласился, говорит что пусть его леди-босс посмотрит, поучится, разогреется.»"
                else:
                    $ scene_runtime.text += "\n\n«Пришел в восторг от моего предложения, сказал чтобы сегодня я к нему домой на огонек заглянула.»"
                $ scene_runtime.text += "\n\n«Так что если хочешь посмотреть - заглядывай и ты к вдове на огонек.»"
            else:
                $ scene_runtime.text += "\n\n«Отказался.»"
                if Becky.home_visit_stage < 5:
                    $ scene_runtime.text += "\n\n«Объяснил, сказал что хозяйка его больно строгая, вышвырнет его за такие шутки.»"
                elif not Eddie.saw_mother_sex or not Becky.home_sex_unlocked:
                    $ scene_runtime.text += "\n\n«Объяснил, сказал что хоть Бекки и разрешила домашним водить своих любовников домой, но он все-таки еще стесняется, не хочет быть первым.»"
                elif Becky.eddie_home_visit_state == 2:
                    $ scene_runtime.text += "\n\n«Объяснил, сказал что идея хорошая, только вот больно дорого я с него запросила, нету у него столько.»"
                else:
                    $ scene_runtime.text += "\n\n«Объяснил, сказал что в другой раз такое замутим, но сейчас ему мол нет мочи терпеть, так что он сразу отымел меня и ушел.»"
        else:
            if Becky.eddie_home_visit_state == 4:
                $ scene_runtime.text += "\n\n«Согласился, конечно. Говорит прошлый раз было здорово, надо повторить. Сказал чтобы сегодня я к нему домой на огонек заглянула. Так что если хочешь посмотреть - заглядывай и ты к вдовушке на огонек.»"
            else:
                $ scene_runtime.text += "\n\n«Отказался, сказал что ему прямо сейчас хочется, мол нет мочи терпеть.»"
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return


label IntGeorgettHire(girl_name="georgett", girl_loc="street"):
    if girl_loc == "tavern":
        $ player.spend_money(4)
        call IntGeorgettSex("georgett", "tavern")
        $ scene_runtime.location_text = scene_runtime.text
    else:
        $ player.spend_money(8)
        call IntGeorgettSex("georgett", "street")
        $ scene_runtime.location_text = scene_runtime.text
        $ main_ui_end_talk_state()
    return


label IntGeorgettGrope(girl_name="georgett", girl_loc="street"):
    $ renpy.dynamic("_grope_result")
    $ _grope_result = georgett_grope_outcome(girl_name, girl_loc)
    $ scene_runtime.text = str(_grope_result.get("text", "") or "")
    $ scene_runtime.location_text = scene_runtime.text
    if bool(_grope_result.get("show_current_sex", False)):
        call ShowCurrentSex(girl_name)
    return


label IntGeorgettAskDad(girl_name="georgett", girl_loc="street"):
    $ scene_runtime.text = DaddyAskBuildPhrase(girl_name)
    $ Georgett.finish_talk()
    $ scene_runtime.location_text = scene_runtime.text
    return
