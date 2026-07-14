# ================================================================================
# YOU ARE NOT ALLOWED TO CHANGE THE STRUCTURE THE MECHAANICS THE WORDING OF CODE BASE FILE WHITOUOUT EXPLICIT PERMISSION IN PERMISSION YOU WILL ARGUMENT WHY THIS CHANGE IS GOOD FOR CODE QUAITY IMPROVEMENT ! ! ! OR PRESENTING A BETTER SOLUTION
# ================================================================================

label IntZimmerTalk(preserve_text=False):
    $ Zimmer.mark_known()
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    $ _becky_var = Becky.var
    $ _mongol_var = peopleInfo["mongol"].var
    $ main_ui_begin_talk_state("Разговор с Циммерманом", _zimmer_name)
    $ current_action_title = "Разговор с Циммерманом"
    $ current_action_content = None
    if not preserve_text:
        $ MainTxt = "Десятник Циммерман внимательно смотрит на вас, ожидая, что вы скажете."
        $ CurLocDesc = MainTxt
    $ current_action_items = []
    $ current_action_items.append(MenuItem("Посмотреть на десятника", Call("IntZimmerTalkLook")))

    if int(Zimmer.talked_today or 0) < 2 and StolenHorseDays > 0 and _zimmer_var.get("ComplainHorse", 0) == 0:
        $ current_action_items.append(MenuItem("Сообщить о краже лошади", Call("IntZimmerTalkHorseReport")))

    if int(Zimmer.talked_today or 0) < 2 and StolenHorseDays > 0 and _zimmer_var.get("ComplainHorse", 0) == 1:
        $ current_action_items.append(MenuItem("Узнать, как продвигаются поиски украденной лошади", Call("IntZimmerTalkHorseProgress")))

    if int(Zimmer.talked_today or 0) < 2 and _becky_var.get("KnowSherwood", 0) == 1 and _zimmer_var.get("SherwoodStory", 0) == 0:
        $ current_action_items.append(MenuItem("Спросить о Шервудском лесе", Call("IntZimmerTalkSherwoodStory1")))

    if int(Zimmer.talked_today or 0) < 2 and _becky_var.get("KnowSherwood", 0) == 1 and _zimmer_var.get("SherwoodStory", 0) == 1:
        $ current_action_items.append(MenuItem("И что с лесом теперь?", Call("IntZimmerTalkSherwoodStory2")))

    if int(Zimmer.talked_today or 0) < 2 and Robin.var_int("RobbedNum", 0) > 0 and _zimmer_var.get("ComplainRobin", 0) == 0:
        $ current_action_items.append(MenuItem("Пожаловаться на Робин Гуда", Call("IntZimmerTalkRobinReport")))

    if int(Zimmer.talked_today or 0) < 2 and _zimmer_var.get("ComplainRobin", 0) == 1 and money >= 100:
        $ current_action_items.append(MenuItem("Отдать сотню мараведи", Call("IntZimmerTalkPay100")))
        $ current_action_items.append(MenuItem("Поторговаться", Call("IntZimmerTalkHaggle")))

    if int(Zimmer.talked_today or 0) < 2 and _zimmer_var.get("ComplainRobin", 0) == 2:
        $ current_action_items.append(MenuItem("Узнать как там расследование", Call("IntZimmerTalkInvestigation")))

    if (
        int(Zimmer.talked_today or 0) < 2
        and int(_mongol_var.get("StocksSeen", 0) or 0) == 1
        and int(_mongol_var.get("StocksFoodDay", -1)) >= 0
        and int(DraupnirVar.get("MongolLockpickOrderDay", -1)) >= 0
        and int(_mongol_var.get("StocksReleased", 0) or 0) == 0
        and int(_mongol_var.get("GuardCaptainKnown", 0) or 0) == 0
        and int(winenum or 0) > 0
    ):
        $ current_action_items.append(MenuItem("Похвастаться вином для ночной стражи", Call("IntZimmerTalkMongolWineDistraction")))

    $ current_action_items.append(MenuItem("Закончить разговор", Function(main_ui_end_talk_state)))
    return


label IntZimmerTalkLook:
    $ MainTxt = "Десятник Циммерман не очень-то похож на подтянутых молодцев с расписных досок. Бравый десятник стар, низок ростом, носат, кучеряв и слегка картавит."
    vscene "images/zimmer/Portrait1.jpg"
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkHorseReport:
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    $ _mongol_var = peopleInfo["mongol"].var
    $ MainTxt = "\"Ай-яй, молодой человек, какие ужасы вы рассказываете!\" поразился десятник Циммерман. \"Прямо из конюшни увели! Ну надо же, какая наглость!\nИ ведь не первый раз уже! Ничего, не волнуйтесь, будем искать. А тем временем замок, что ли смените. Или сторожите лошадь вашу.\""
    $ _mongol_var["ZimmerKnow"] = 1
    $ _zimmer_var["ComplainHorse"] = 1
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkHorseProgress:
    $ _zimmer_name = "zimmer"
    $ MainTxt = "\"Ничего, не волнуйтесь, ищем. Это наша работа!\""
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkSherwoodStory1:
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    $ MainTxt = "\"Шервудский лес?\" переспросил старый десятник. \"О, молодой человек, это был прекрасный лес. Пока эльфы эти его не испортили.\""
    $ MainTxt += "\n\n\"И как же они его испортили?\" удивились вы. \"Эльфы же любят лес?\""
    $ MainTxt += "\n\n\"Так они его любят, что там мол и деревца не сруби. В стародавние времена эти лопухие наших лесорубов прямо по опушкам развешивали, мол не руби. Но нрав у Ее Милости крутой, она их от таких шуток отучила. Но этот Шервудский лес по договору все равно был их, так что рубить деревья там запрещалось. Оно конечно и верно, лес-то их, но что же, из-за этого недоразумения уже и воз дров не наруби? Ну или там парочку-троечку? Это ж ерунда, от леса не убудет.\""
    $ MainTxt += "\n\n\"Мой десяток там лес с нашей стороны охранял. Эх молодой человек, золотое это было время, скажу я вам. Я тогда себе, не поверите, два дома отстроил и коляску с парой лошадей купил. Зажил по человечески, сыночков своих хорошо пристроил.\""
    $ MainTxt += "\n\n\"А потом бац - и заявляются эти лопухие. Говорят мол нет леса, все вырубили. Приходим и действительно, одни пни стоят. Его Светлость маркиз Рамон, как ряды пеньков увидел, так разозлиться изволил, подать сюда этих охранников изволил покричать.\""
    $ MainTxt += "\n\n\"И что же вам его Светлость сказать изволил?\" заинтересованно спросили вы."
    $ MainTxt += "\n\n\"Мне? Ничего. Заболел я тяжело, старость не радость. Не смог я поговорить с его Светлостью. А докторишкам, не поверишь, пришлось и коляску с лошадьми, и второй дом отдать. Кровососы! Так и не смог я объяснить его Светлости, что это наверняка эльфы весь лес вырубили. Лицемеры ушастые! Ведь мы, со своей стороны, уж так сторожили, так сторожили!\""
    $ _zimmer_var["SherwoodStory"] = 1
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkSherwoodStory2:
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    $ _becky_var = Becky.var
    $ MainTxt = "\"А что с ним? Эти ушастики из Куниделла большой шум подняли. Мол как так, был лес и нет. Но что теперь сделаешь? Никто там за порядком не следит, наша стража - потому что это эльфийская земля, не положенно, а эльфы - потому, что им мол в мертвом лесу находиться, видите ли, неприятно. Так теперь там лихие люди порой шастают, нет на них никакой управы.\""
    $ _becky_var["SherwoodSuspect"] = _becky_var.get("SherwoodSuspect", 0) + 5
    $ _zimmer_var["SherwoodStory"] = 2
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkRobinReport:
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    $ MainTxt = "\"Ай-ай молодой человек, какие вы ужасы рассказываете. Грабеж? И где вы говорите это произошло? На Шервудской вырубке? Очень, очень жаль. Мы должны защищать добрых горожан нашего славного Коитополиса, однако ж эта вырубка находится далековато. Так что порядок мы там, сами понимаете, поддерживать не можем. Правда, если вы решите компенсировать нам расходы, связанные с расследованием, мы можем и поискать грабителей. Путь неблизкий, но из сочуствия и уважения к вам я готов таки удовлетворится сотней мараведи.\""
    vscene "images/zimmer/Talk.jpg"
    $ _zimmer_var["ComplainRobin"] = 1
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkPay100:
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    $ MainTxt = "\"Таки вы сделали правильный выбор, молодой человек, старый Циммерман все сделает. Завтра же поищу негодяев,\" заверил вас десятник, ловко пряча монеты в карман."
    vscene "images/zimmer/Talk.jpg"
    $ _zimmer_var["ComplainRobin"] = 2
    $ _zimmer_var["RobinInvestigationDay"] = dayspassed + procedural_randint(9, 14, "zimmer_robin_investigation_%s" % dayspassed)
    $ money -= 100
    call stat
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkHaggle:
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    $ MainTxt = "\"Господин Циммерман, вы же сами понимаете, я жертва ограбления, денег у меня мало. Вы уж войдите в мое бедственное положение. Помогите сиротинушке! 50 мараведи?\""
    if money >= 500:
        $ MainTxt += "\n\n\"Не дурите старого Циммермана, молодой человек. Я же прекрасно знаю, сколько у вас на самом деле денег,\" отбрил вас десятник."
    else:
        $ MainTxt += "\n\nДесятник осмотрел вас скептически, но все таки сказал:\n\"98 мараведи\"\n\"60\"\n\"97\"\n\"70\"\n\"Ладно, 95\"\n\"80, больше нет!\"\n\"Вы меня совсем по миру пустить хотите, молодой человек, 90! Больше уступить не могу!\"\n\"Согласен!\" радостно заорали вы, и быстро, пока он не передумал отсчитали монеты.\n\"Все моя доброта,\" понуро заявил Циммерман, \"Завтра же пойду и поищу негодяев.\"\nЧерез некоторое время радость от удачной сделки улеглась и вам почему-то стало казаться, что вас накололи.\n\"Странно, с чего бы это?\" подумали вы."
        $ _zimmer_var["ComplainRobin"] = 2
        $ _zimmer_var["RobinInvestigationDay"] = dayspassed + procedural_randint(9, 14, "zimmer_robin_haggle_%s" % dayspassed)
        $ money -= 90
        call stat
    vscene "images/zimmer/Talk.jpg"
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkInvestigation:
    $ Zimmer.ensure_story_defaults()
    $ _zimmer_name = "zimmer"
    $ _zimmer_var = Zimmer.var
    if _zimmer_var.get("RobinInvestigationDay", 0) > dayspassed:
        $ MainTxt = "\"Не волнуйтесь молодой человек. Ваше дело в надежных руках! Если старый Циммерман сказал, что найдет негодяев, будьте таки уверены, он их найдет!\" заверил вас бравый десятник."
    else:
        $ MainTxt = "\"Молодой человек!\" торжественно сказал десятник. \"Ваше сообщение полностью подтвердилось! Как я и обещал, я сходил к Шервудкому лесу. И шо вы таки думаете? Все как вы и говорили. Разбойнички именно там и обнаружились. Всей бандой, голубчики.\""
        $ MainTxt += "\n\n\"Так вы их наконец-то арестовали?\" радостно воскликнули вы. Про свои деньги вы осмотрительно решили спросить попозже."
        $ MainTxt += "\n\n\"Как так арестовал?\" удивился Циммерман. \"За кого вы меня принимаете, молодой человек? За светлейшего и храбрейшего рыцаря дона Байярда? Я старый человек. У меня семья, дети, любовницы, дети от любовниц. А вы видели сколько там бандитов? Это таки совершенейшие головорезы, скажу я вам. Нет, мы с вами, молодой человек, договаривались, что я поищу бандитов. Я их таки нашел, уговор я выполнил.\""
        $ MainTxt += "\n\n\"Но стражи же много?\" неуверенно начали вы."
        $ MainTxt += "\n\n\"У них тоже у всех семьи. А лес этот вовсе и не наших землях. Я, молодой человек, дожил до седин отнюдь не из-за мальчишеского задора. Я их нашел, как и уговаривались, но арестовать мы бандитов сейчас не можем. Впрочем если вы их сможете поймать и привести, стража Куниделла будет в долгу перед вами.\""
        $ MainTxt += "\n\nВам почему-то захотелось вдарить десятнику Циммерману. Однако титаническим усилием воли вы сдержались, благо драка с десятником была чревата последствиями. Да и в самом деле, успокоили себя вы, ведь стража сделала, что могла? Сделала. Разве их вина, что она не смогла поймать разбойников? Ну конечно же не их! Так чего же сердится?"
        $ _zimmer_var["ComplainRobin"] = _zimmer_var.get("ComplainRobin", 0) + 1
    vscene "images/zimmer/Talk.jpg"
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return


label IntZimmerTalkMongolWineDistraction:
    $ _zimmer_name = "zimmer"
    $ _mongol_var = peopleInfo["mongol"].var
    $ MainTxt = "Вы как бы между делом рассказываете Циммерману, что в трактире остался отличный бочонок, который не стыдно отправить доблестным ночным стражникам у караулки. Десятник заметно оживляется и тут же начинает рассуждать, как важно поддерживать людей на посту.\n\n\"Вот это, молодой человек, правильное понимание общественного порядка,\" важно кивает он. \"У хорошего хозяина и стража сыта, и город спокоен.\""
    vscene "images/zimmer/Talk.jpg"
    $ _mongol_var["GuardCaptainKnown"] = 1
    $ Zimmer.change_social(friend_delta=1)
    $ Zimmer.mark_talked(1)
    $ CurLocDesc = MainTxt
    call IntZimmerTalk(True)
    return
