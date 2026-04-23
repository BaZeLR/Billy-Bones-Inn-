label IntEddieTalk:
    $ main_ui_begin_talk_state("Разговор с Эдди", "eddie")
    $ current_action_title = "Разговор с Эдди"
    $ current_action_content = None
    $ MainTxt = "Эдди вопросительно смотрит на вас, ожидая, о чем вы заговорите."
    $ CurLocDesc = MainTxt
    call IntEddieTalkRefresh
    return


label IntEddieTalkRefresh:
    $ _eddie_name = "eddie"
    $ main_ui_begin_talk_state("Разговор с Эдди", _eddie_name)
    $ current_action_title = "Разговор с Эдди"
    $ current_action_content = None
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Поболтать с Эдди о разной фигне.", Function(main_ui_call_label, "IntEddieTalkApply", "smalltalk")))

    if Friends.get(_eddie_name, 0) >= 5:
        $ current_action_items.append(MenuItem("Поболтать с Эдди о личных вещах.", Function(main_ui_call_label, "IntEddieTalkApply", "personal")))

    if Friends.get(_eddie_name, 0) >= 5 and CurrentLoc.get("georgett", "") == "TavernMain" and EddieVar.get("TalkedAboutWhores", 0) == 0 and Talked.get(_eddie_name, 0) < 2:
        $ current_action_items.append(MenuItem("Рассказать Эдди о том, что у вас теперь работают девочки.", Function(main_ui_call_label, "IntEddieTalkApply", "whores")))

    if Friends.get(_eddie_name, 0) >= 5 and CurrentLoc.get("georgett", "") == "TavernMain" and EddieVar.get("SawWithGeorgett", 0) > 0 and EddieVar.get("TalkedAboutGeorgett", 0) == 0 and Talked.get(_eddie_name, 0) < 2:
        $ current_action_items.append(MenuItem("Поинтересоваться у Эдди как ему ваши девочки.", Function(main_ui_call_label, "IntEddieTalkApply", "girls")))

    if Friends.get(_eddie_name, 0) >= 3 and BeckyVar.get("HomeSex", 0) > 0 and EddieVar.get("SawMomSex", 0) > 0 and EddieVar.get("SawWithGeorgett", 0) > 0 and BeckyVar.get("EddieTryToFuck", 0) != 1 and Talked.get(_eddie_name, 0) < 2:
        $ current_action_items.append(MenuItem("Предложить помочь подкатится к его мамаше.", Function(main_ui_call_label, "IntEddieTalkApply", "mom_helper")))

    if Friends.get(_eddie_name, 0) >= 3 and Talked.get(_eddie_name, 0) < 2 and BeckyVar.get("EddieRobbedDay", 0) > 0 and BeckyVar.get("EddieRobbedDay", 0) + 12 >= dayspassed and EddieVar.get("FingalTalk", 0) == 0:
        $ current_action_items.append(MenuItem("Спросить о синяке.", Function(main_ui_call_label, "IntEddieTalkApply", "bruise")))

    if Friends.get(_eddie_name, 0) >= 7 and Talked.get(_eddie_name, 0) < 2 and BeckyVar.get("EddieRobbedDay", 0) > 0 and BeckyVar.get("EddieRobbedDay", 0) + 12 >= dayspassed and EddieVar.get("FingalTalk", 0) == 1:
        $ current_action_items.append(MenuItem("А все таки расскажи, кто это тебе так вмазал?", Function(main_ui_call_label, "IntEddieTalkApply", "who_hit")) )

    if Friends.get(_eddie_name, 0) >= 7 and Talked.get(_eddie_name, 0) < 2 and BeckyVar.get("EddieRobbedDay", 0) > 0 and BeckyVar.get("EddieRobbedDay", 0) + 12 >= dayspassed and EddieVar.get("FingalTalk", 0) == 2 and EddieVar.get("FingalTalkDestination", 0) == 0:
        $ current_action_items.append(MenuItem("А куда это ты ездил?", Function(main_ui_call_label, "IntEddieTalkApply", "destination")))

    if Friends.get(_eddie_name, 0) >= 7 and Talked.get(_eddie_name, 0) < 2 and BeckyVar.get("EddieRobbedDay", 0) > 0 and BeckyVar.get("EddieRobbedDay", 0) + 12 >= dayspassed and EddieVar.get("FingalTalk", 0) == 2 and EddieVar.get("FingalTalkComplain", 0) == 0:
        $ current_action_items.append(MenuItem("Страже жаловался?", Function(main_ui_call_label, "IntEddieTalkApply", "complain")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntEddieTalkApply(choice_code=""):
    $ _eddie_name = "eddie"

    if str(choice_code or "") == "smalltalk":
        $ MainTxt = "Вы некоторое время болтаете с Эдди о несущественных вещах."
        if Talked.get(_eddie_name, 0) <= 2 and renpy.random.randint(1, 2) == 1 and Friends.get(_eddie_name, 0) <= 5:
            $ MainTxt += "\n\nВы немного сдружились с Эдди."
            $ Friends[_eddie_name] = Friends.get(_eddie_name, 0) + 1
        elif Talked.get(_eddie_name, 0) > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "personal":
        $ MainTxt = "Вы некоторое время болтаете с Эдди о том, кто сколько выпил и о том, какие девушки кому нравятся."
        if Talked.get(_eddie_name, 0) <= 2 and renpy.random.randint(1, 2) == 1 and Friends.get(_eddie_name, 0) <= 10:
            $ MainTxt += "\n\nВы немного сдружились с Эдди."
            $ Friends[_eddie_name] = Friends.get(_eddie_name, 0) + 1
        elif Talked.get(_eddie_name, 0) > 2:
            $ MainTxt += "\n\nНичего нового из разговора вы не узнали."
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "whores":
        $ MainTxt = "Вы как бы между делом замечаете, что у вас теперь работают девочки не самого тяжелого поведения. Глаза рыжего Эдди загораются, хотя на словах он никак не показывает своей заинтересованности. Вернее, он старательно показывает что ему пофигу."
        $ Friends[_eddie_name] = Friends.get(_eddie_name, 0) + 1
        $ EddieVar["TalkedAboutWhores"] = 1
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "girls":
        $ MainTxt = "Ведя общий разговор вы неожиданно спрашиваете Эдди, как ему Жоржетта. Эдди густо краснеет, запинается, но все таки отмечает, что она очень даже ничего. При этом парень вас внимательно изучает, как бы пытаясь понять что вам известно. Вы делаете безразличный вид и переводите разговор на другую тему."
        call ShowImage("eddie", "portraits", "surprised")
        $ Friends[_eddie_name] = Friends.get(_eddie_name, 0) + 1
        $ EddieVar["TalkedAboutGeorgett"] = 1
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "mom_helper":
        if BeckyVar.get("EddieTryToFuck", 0) == 0:
            $ MainTxt = "\"Эй, Эдди, я прекрасно знаю чего тебе хочется,\" сказали вы юному бакалейщику. \"Думаешь я не видел, какие ты взгляды на мамочку свою кидаешь? Или не знаю в какие ты игры с Жоржеттой играешься?\""
            if Friends.get(_eddie_name, 0) < 9:
                $ MainTxt += "\n\n\"Не понимаю, мастер Стефан, о чем это вы,\" ответил вам Эдди слегка покраснев. Все ваши дальнейшие попытки разговорить его упирались в стену молчания. Судя по всему он вас плохо знает и не доверяет."
            else:
                $ MainTxt += "\n\n\"Это мое дело\", буркнул парень, \"и тебя оно не касается.\" \"Зря ты так,\" вы отнюдь не обиделись на данный им отпор, \"я же помочь тебе хочу. Слушай, когда я в следующий раз после ужина пойду с твоей мамочкой в спальню, я оставлю дверь открытой. Ты подожди пару минут и заходи. Твоя мать сама тебя хочет, только решиться не может.\""
                $ MainTxt += "\n\n\"Правда что ли?\" глаза Эдди стали как плошки."
                $ MainTxt += "\n\n\"Точно тебе говорю,\" заверили наивного юношу вы."
                $ MainTxt += "\n\n\"Ну спасибо тебе, не ожидал.\""
                $ BeckyVar["EddieTryToFuck"] = 1
            call ShowImage("eddie", "portraits", "surprised")
        elif BeckyVar.get("EddieTryToFuck", 0) in [2, 3]:
            $ MainTxt = "\"Эй Эдди, насчет прошлого раза,\" начали вы свою речь."
            if Friends.get(_eddie_name, 0) < 10:
                $ MainTxt += "\n\n\"Да пошел ты,\" ответил вам Эдди, с ненавистью глядя на вас, \"куда подальше. Не поддамся я еще раз на твое издевательство.\""
                $ MainTxt += "\n\nС этими словами бакалейщик отвернулся и на дальнейшие попытки завязать разговор не реагировал."
            elif BeckyVar.get("EddieFailures", 0) > 2:
                $ MainTxt += "\n\n\"Да пошел ты,\" ответил вам Эдди, с ненавистью глядя на вас, \"куда подальше. Со своими подколками. Несколько раз тебе верил, но теперь все, в очередной раз ты меня больше не надуешь.\""
                $ MainTxt += "\n\nС этими словами бакалейщик отвернулся и на дальнейшие попытки завязать разговор не реагировал."
            else:
                $ MainTxt += "\n\n\"Это ты поиздеваться решил надо мной, да?\" ответил вам Эдди смерив вас тяжелым недобрым взглядом."
                if BeckyVar.get("EddieTryToFuck", 0) == 3:
                    $ MainTxt += "\n\n\"Я сделал все так, как ты сказал, а дверь была заперта.\""
                    $ MainTxt += "\n\n\"Эээ, извини, я просто забыл засов отодвинуть, в следующий раз обязательно открою, это я не специально.\" заверили вы своего нового друга."
                else:
                    $ MainTxt += "\n\n\"Ты говорил, что она сама хочет, а она меня выкинула из комнаты, обозвала подонком и извращенцем и весь день со мной не разговаривала.\""
                    $ MainTxt += "\n\n\"Эээ, даже не знаю, что на нее нашло, но я все уладил, все обговорил. Попробуй еще раз зайти, все будет классно, не дрейфь!\" заверили вы своего нового друга."
                $ MainTxt += "\n\n\"Правда что ли?\""
                $ MainTxt += "\n\n\"Точно тебе говорю\""
                $ MainTxt += "\n\n\"Ну ладно, а я уж подумал было...\""
                $ BeckyVar["EddieTryToFuck"] = 1
            call ShowImage("eddie", "portraits", "surprised")
        elif BeckyVar.get("EddieTryToFuck", 0) >= 4 and BeckyVar.get("visitedhome", 0) < 7:
            $ MainTxt = "\"И как тебе ночка с мамкой?\" подмигнули вы Эдди, делая рукой неприличный жест."
            $ MainTxt += "\n\n\"Ух, классно, спасибо тебе Стефан, ты настоящий друг. Мамочка сказала, что теперь я каждый день могу ее трахать, и даже спать с ней иногда,\" сказал Эдди с блаженной улобкой на лице."
            $ MainTxt += "\n\n\"Но и ты, конечно, всегда будешь желанным гостем в нашем доме,\" быстро поправился он."
        else:
            $ MainTxt = "\"И как у тебя идут дела с твоей сисястой родительнецей?\" цинично поинтересовались вы у Эдди."
            $ MainTxt += "\n\n\"Благодаря тебе, Стефан, более чем хорошо,\" довольно ответил тот."
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "bruise":
        $ MainTxt = "\"Слышь, а где это тебя отоварили?\" спросили вы Эдди."
        $ MainTxt += "\n\n\"Да этого, того в общем не с теми связался.\""
        $ MainTxt += "\n\n\"С кем это, не с теми?\" решили уточнить вы."
        $ MainTxt += "\n\n\"Ну не с теми значит не с теми. Мое дело. И вообще, мамка не велела говорить,\" отбрехался ваш знакомый."
        $ BeckyVar["SherwoodSuspect"] = BeckyVar.get("SherwoodSuspect", 0) + 1
        $ EddieVar["FingalTalk"] = 1
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "who_hit":
        if BeckyVar.get("visitedhome", 0) >= 7 and Friends.get(_eddie_name, 0) >= 9:
            $ MainTxt = "\"Знаешь, ты мне удружил, и мою мамку мы с тобой классно оттрахали. Врядли бы она мне дала, если бы не ты. Так что скажу, хоть она и не велела. Только ты меня не запали, хорошо? В общем меня уроды эти, из Шервудского леса, отмудохали. Обычно нормально можно было проехать, дашь им пару десятков монет и едешь себе. А надысь еду - только их встретил так мне сразу в табло засветили. Хоть бы объяснили, за что. Деньги отобрали, лошадь забрали. Вот пидорасы!\""
            $ BeckyVar["SherwoodSuspect"] = BeckyVar.get("SherwoodSuspect", 0) + 10
            $ EddieVar["FingalTalk"] = 2
            $ BeckyVar["KnowSherwood"] = 1
        else:
            $ MainTxt = "\"Я тебе уже все что хотел сказал. Мало того, что огреб, так еще ты тут с распросами дурацкими. Кто ты такой, что мне вопросы задавать?\" отбрил вас Эдди."
            if Friends.get(_eddie_name, 0) >= 5:
                $ Friends[_eddie_name] = Friends.get(_eddie_name, 0) - renpy.random.randint(0, 1)
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "destination":
        $ MainTxt = "\"По делам. Я и так уже слишком много тебе рассказал.\""
        $ EddieVar["FingalTalkDestination"] = 1
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    if str(choice_code or "") == "complain":
        $ MainTxt = "\"Ну ты шутник,\" развеселился Эдди. \"Я чего, дурак? Денег они слупят, типа за хлопоты, но вряд ли будут связываться. Тем более, что сам Циммерман раньше трепался, что мол ентот лес ничейный, и никого они там ловить не обязанны.\""
        $ EddieVar["FingalTalkComplain"] = 1
        $ Talked[_eddie_name] = Talked.get(_eddie_name, 0) + 1
        $ CurLocDesc = MainTxt
        call IntEddieTalkRefresh
        return

    call GroceryStoreRestore
    return
