# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

label IntEddieTalk(preserve_text=False):
    $ Becky.update()
    $ _eddie_name = "eddie"
    $ eddie_talk_init_state()
    $ Eddie.ensure_story_defaults()
    $ _eddie_var = Eddie.var
    $ _becky_var = Becky.var
    $ _eddie_picture = ""
    if str(CurLoc or "") == "GroceryStore":
        $ _eddie_picture = grocery_store_grocer_picture("eddie")
    else:
        $ _eddie_picture = str(Eddie.data.portrait or "images/eddie/portraits/portrait_0.png")
    if str(_eddie_picture or "").strip():
        vscene _eddie_picture
    $ main_ui_begin_talk_state("Разговор с Эдди", _eddie_name)
    $ current_action_title = "Разговор с Эдди"
    $ current_action_content = None
    if not preserve_text:
        $ MainTxt = eddie_talk_intro_text()
        $ CurLocDesc = MainTxt
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Поболтать с Эдди о разной фигне.", Call("IntEddieTalkSmalltalk")))

    if eddie_talk_can_personal(_eddie_name):
        $ current_action_items.append(MenuItem("Поболтать с Эдди о личных вещах.", Call("IntEddieTalkPersonal")))

    if eddie_talk_can_whores(_eddie_var, _eddie_name):
        $ current_action_items.append(MenuItem("Рассказать Эдди о том, что у вас теперь работают девочки.", Call("IntEddieTalkWhores")))

    if eddie_talk_can_girls(_eddie_var, _eddie_name):
        $ current_action_items.append(MenuItem("Поинтересоваться у Эдди как ему ваши девочки.", Call("IntEddieTalkGirls")))

    if eddie_talk_can_mom_helper(_eddie_var, _becky_var, _eddie_name):
        $ current_action_items.append(MenuItem("Предложить помочь подкатится к хозяйке лавки.", Call("IntEddieTalkMomHelper")))

    if eddie_talk_can_bruise(_eddie_var, _becky_var, _eddie_name):
        $ current_action_items.append(MenuItem("Спросить о синяке.", Call("IntEddieTalkBruise")))

    if eddie_talk_can_who_hit(_eddie_var, _becky_var, _eddie_name):
        $ current_action_items.append(MenuItem("А все таки расскажи, кто это тебе так вмазал?", Call("IntEddieTalkWhoHit")))

    if eddie_talk_can_destination(_eddie_var, _becky_var, _eddie_name):
        $ current_action_items.append(MenuItem("А куда это ты ездил?", Call("IntEddieTalkDestination")))

    if eddie_talk_can_complain(_eddie_var, _becky_var, _eddie_name):
        $ current_action_items.append(MenuItem("Страже жаловался?", Call("IntEddieTalkComplain")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntEddieTalkSmalltalk:
    $ Eddie.ensure_story_defaults()
    $ _eddie_talk_count = int(Eddie.talked_today or 0)
    $ MainTxt = "Вы некоторое время болтаете с Эдди о несущественных вещах."
    if _eddie_talk_count <= 2 and procedural_randint(1, 2, "eddie_smalltalk_%s_%s" % (dayspassed, _eddie_talk_count)) == 1 and int(Eddie.rel or 0) <= 5:
        $ MainTxt += "\n\nВы немного сдружились с Эдди."
        $ Eddie.change_social(friend_delta=1)
    elif _eddie_talk_count > 2:
        $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkPersonal:
    $ Eddie.ensure_story_defaults()
    $ _eddie_talk_count = int(Eddie.talked_today or 0)
    $ MainTxt = "Вы некоторое время болтаете с Эдди о том, кто сколько выпил и о том, какие девушки кому нравятся."
    if _eddie_talk_count <= 2 and procedural_randint(1, 2, "eddie_personal_%s_%s" % (dayspassed, _eddie_talk_count)) == 1 and int(Eddie.rel or 0) <= 10:
        $ MainTxt += "\n\nВы немного сдружились с Эдди."
        $ Eddie.change_social(friend_delta=1)
    elif _eddie_talk_count > 2:
        $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkWhores:
    $ Eddie.ensure_story_defaults()
    $ _eddie_var = Eddie.var
    $ MainTxt = "Вы как бы между делом замечаете, что у вас теперь работают девочки не самого тяжелого поведения. Глаза рыжего Эдди загораются, хотя на словах он никак не показывает своей заинтересованности. Вернее, он старательно показывает что ему пофигу."
    $ Eddie.change_social(friend_delta=1)
    $ _eddie_var["TalkedAboutWhores"] = 1
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkGirls:
    $ Eddie.ensure_story_defaults()
    $ _eddie_var = Eddie.var
    $ MainTxt = "Ведя общий разговор вы неожиданно спрашиваете Эдди, как ему Жоржетта. Эдди густо краснеет, запинается, но все таки отмечает, что она очень даже ничего. При этом парень вас внимательно изучает, как бы пытаясь понять что вам известно. Вы делаете безразличный вид и переводите разговор на другую тему."
    vscene "images/eddie/portraits/surprised.png"
    $ Eddie.change_social(friend_delta=1)
    $ _eddie_var["TalkedAboutGeorgett"] = 1
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkMomHelper:
    $ Becky.update()
    $ Eddie.ensure_story_defaults()
    $ _becky_var = Becky.var
    if _becky_var.get("EddieTryToFuck", 0) == 0:
        $ MainTxt = "\"Эй, Эдди, я прекрасно знаю чего тебе хочется,\" сказали вы юному бакалейщику. \"Думаешь я не видел, какие ты взгляды на хозяйку лавки кидаешь? Или не знаю в какие ты игры с Жоржеттой играешься?\""
        if int(Eddie.rel or 0) < 9:
            $ MainTxt += "\n\n\"Не понимаю, мастер Стефан, о чем это вы,\" ответил вам Эдди слегка покраснев. Все ваши дальнейшие попытки разговорить его упирались в стену молчания. Судя по всему он вас плохо знает и не доверяет."
        else:
            $ MainTxt += "\n\n\"Это мое дело\", буркнул парень, \"и тебя оно не касается.\" \"Зря ты так,\" вы отнюдь не обиделись на данный им отпор, \"я же помочь тебе хочу. Слушай, когда я в следующий раз после ужина пойду с твоей хозяйкой в спальню, я оставлю дверь открытой. Ты подожди пару минут и заходи. Бекки сама тебя хочет, только решиться не может.\""
            $ MainTxt += "\n\n\"Правда что ли?\" глаза Эдди стали как плошки."
            $ MainTxt += "\n\n\"Точно тебе говорю,\" заверили наивного юношу вы."
            $ MainTxt += "\n\n\"Ну спасибо тебе, не ожидал.\""
            $ _becky_var["EddieTryToFuck"] = 1
        vscene "images/eddie/portraits/surprised.png"
    elif _becky_var.get("EddieTryToFuck", 0) in [2, 3]:
        $ MainTxt = "\"Эй Эдди, насчет прошлого раза,\" начали вы свою речь."
        if int(Eddie.rel or 0) < 10:
            $ MainTxt += "\n\n\"Да пошел ты,\" ответил вам Эдди, с ненавистью глядя на вас, \"куда подальше. Не поддамся я еще раз на твое издевательство.\""
            $ MainTxt += "\n\nС этими словами бакалейщик отвернулся и на дальнейшие попытки завязать разговор не реагировал."
        elif _becky_var.get("EddieFailures", 0) > 2:
            $ MainTxt += "\n\n\"Да пошел ты,\" ответил вам Эдди, с ненавистью глядя на вас, \"куда подальше. Со своими подколками. Несколько раз тебе верил, но теперь все, в очередной раз ты меня больше не надуешь.\""
            $ MainTxt += "\n\nС этими словами бакалейщик отвернулся и на дальнейшие попытки завязать разговор не реагировал."
        else:
            $ MainTxt += "\n\n\"Это ты поиздеваться решил надо мной, да?\" ответил вам Эдди смерив вас тяжелым недобрым взглядом."
            if _becky_var.get("EddieTryToFuck", 0) == 3:
                $ MainTxt += "\n\n\"Я сделал все так, как ты сказал, а дверь была заперта.\""
                $ MainTxt += "\n\n\"Эээ, извини, я просто забыл засов отодвинуть, в следующий раз обязательно открою, это я не специально.\" заверили вы своего нового друга."
            else:
                $ MainTxt += "\n\n\"Ты говорил, что она сама хочет, а она меня выкинула из комнаты, обозвала подонком и извращенцем и весь день со мной не разговаривала.\""
                $ MainTxt += "\n\n\"Эээ, даже не знаю, что на нее нашло, но я все уладил, все обговорил. Попробуй еще раз зайти, все будет классно, не дрейфь!\" заверили вы своего нового друга."
            $ MainTxt += "\n\n\"Правда что ли?\""
            $ MainTxt += "\n\n\"Точно тебе говорю\""
            $ MainTxt += "\n\n\"Ну ладно, а я уж подумал было...\""
            $ _becky_var["EddieTryToFuck"] = 1
        vscene "images/eddie/portraits/surprised.png"
    elif _becky_var.get("EddieTryToFuck", 0) >= 4 and _becky_var.get("visitedhome", 0) < 7:
        $ MainTxt = "\"И как тебе ночка с хозяйкой лавки?\" подмигнули вы Эдди, делая рукой неприличный жест."
        $ MainTxt += "\n\n\"Ух, классно, спасибо тебе Стефан, ты настоящий друг. Госпожа Блэнкеншип сказала, что теперь я каждый день могу ее трахать, и даже спать с ней иногда,\" сказал Эдди с блаженной улобкой на лице."
        $ MainTxt += "\n\n\"Но и ты, конечно, всегда будешь желанным гостем в нашем доме,\" быстро поправился он."
    else:
        $ MainTxt = "\"И как у тебя идут дела с твоей сисястой начальницей?\" цинично поинтересовались вы у Эдди."
        $ MainTxt += "\n\n\"Благодаря тебе, Стефан, более чем хорошо,\" довольно ответил тот."
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkBruise:
    $ Becky.update()
    $ Eddie.ensure_story_defaults()
    $ _eddie_var = Eddie.var
    $ _becky_var = Becky.var
    $ MainTxt = "\"Слышь, а где это тебя отоварили?\" спросили вы Эдди."
    $ MainTxt += "\n\n\"Да этого, того в общем не с теми связался.\""
    $ MainTxt += "\n\n\"С кем это, не с теми?\" решили уточнить вы."
    $ MainTxt += "\n\n\"Ну не с теми значит не с теми. Мое дело. И вообще, Бекки не велела говорить,\" отбрехался ваш знакомый."
    $ _becky_var["SherwoodSuspect"] = _becky_var.get("SherwoodSuspect", 0) + 1
    $ _eddie_var["FingalTalk"] = 1
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkWhoHit:
    $ Becky.update()
    $ Eddie.ensure_story_defaults()
    $ _eddie_var = Eddie.var
    $ _becky_var = Becky.var
    if _becky_var.get("visitedhome", 0) >= 7 and int(Eddie.rel or 0) >= 9:
        $ MainTxt = "\"Знаешь, ты мне удружил, и мою хозяйку мы с тобой классно оттрахали. Врядли бы она мне дала, если бы не ты. Так что скажу, хоть она и не велела. Только ты меня не запали, хорошо? В общем меня уроды эти, из Шервудского леса, отмудохали. Обычно нормально можно было проехать, дашь им пару десятков монет и едешь себе. А надысь еду - только их встретил так мне сразу в табло засветили. Хоть бы объяснили, за что. Деньги отобрали, лошадь забрали. Вот пидорасы!\""
        $ _becky_var["SherwoodSuspect"] = _becky_var.get("SherwoodSuspect", 0) + 10
        $ _eddie_var["FingalTalk"] = 2
        $ _becky_var["KnowSherwood"] = 1
    else:
        $ MainTxt = "\"Я тебе уже все что хотел сказал. Мало того, что огреб, так еще ты тут с распросами дурацкими. Кто ты такой, что мне вопросы задавать?\" отбрил вас Эдди."
        if int(Eddie.rel or 0) >= 5:
            $ Eddie.change_social(friend_delta=-procedural_randint(0, 1, "eddie_who_hit_rel_%s_%s" % (dayspassed, int(Eddie.talked_today or 0))))
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkDestination:
    $ Eddie.ensure_story_defaults()
    $ _eddie_var = Eddie.var
    $ MainTxt = "\"По делам. Я и так уже слишком много тебе рассказал.\""
    $ _eddie_var["FingalTalkDestination"] = 1
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return


label IntEddieTalkComplain:
    $ Eddie.ensure_story_defaults()
    $ _eddie_var = Eddie.var
    $ MainTxt = "\"Ну ты шутник,\" развеселился Эдди. \"Я чего, дурак? Денег они слупят, типа за хлопоты, но вряд ли будут связываться. Тем более, что сам Циммерман раньше трепался, что мол ентот лес ничейный, и никого они там ловить не обязанны.\""
    $ _eddie_var["FingalTalkComplain"] = 1
    $ Eddie.mark_talked()
    $ CurLocDesc = MainTxt
    call IntEddieTalk(True)
    return
